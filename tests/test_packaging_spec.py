"""
Regression test for nutrimagnus.spec's PyInstaller `datas` list.

web/backend.py resolves a handful of root-level files (the manual,
DISCLAIMER.md) relative to _PROJECT_ROOT, which becomes sys._MEIPASS
inside a packaged build. A file referenced there but missing from the
spec's datas silently 404s only in a packaged install -- never in a dev
checkout or the normal test suite, since _PROJECT_ROOT there is just the
repo root where every file already exists. This caught DISCLAIMER.md
missing from datas (found via manual testing of a packaged Windows build,
2026-09-13) with no earlier warning from pytest.

The same trap applies to the bundled static reference datasets, which each
module loads as `Path(__file__).parent / "<name>.json"` -- that resolves into
sys._MEIPASS in a packaged build, so an absent file means the lookup quietly
returns nothing rather than failing. All four were in fact missing from datas
(found 2026-09-27 while replacing the glycemic index table), which would have
silently emptied the GI, CoFID, AFCD and CIQUAL lookups in every packaged
build shipped to date.

Docs: README-numa-documentation.md (Web app section).
"""
import re
import subprocess
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _root_relative_files_used_by_backend() -> set[str]:
    """Every `_PROJECT_ROOT / "some-file"` literal in web/backend.py."""
    text = (_PROJECT_ROOT / "web" / "backend.py").read_text(encoding="utf-8")
    return set(re.findall(r'_PROJECT_ROOT\s*/\s*"([^"]+)"', text))


def _spec_bundled_root_files() -> set[str]:
    """Every top-level ('some-file', '.') entry in nutrimagnus.spec's datas."""
    text = (_PROJECT_ROOT / "nutrimagnus.spec").read_text(encoding="utf-8")
    return set(re.findall(r"\(\s*'([^']+)'\s*,\s*'\.'\s*\)", text))


def _root_data_files_loaded_by_modules() -> set[str]:
    """Every `Path(__file__).parent / "some.json"` literal in a root module."""
    found: set[str] = set()
    for module in _PROJECT_ROOT.glob("*.py"):
        text = module.read_text(encoding="utf-8")
        found.update(re.findall(
            r'Path\(__file__\)\.parent\s*/\s*"([^"]+\.json)"', text))
    return found


def test_every_bundled_reference_dataset_is_in_the_spec():
    used = _root_data_files_loaded_by_modules()
    assert used, "sanity check: at least one root module should load a JSON dataset"
    missing = used - _spec_bundled_root_files()
    assert not missing, (
        f"nutrimagnus.spec's datas is missing {sorted(missing)} -- the lookups "
        "that read them will silently return no results in a packaged build, "
        "since Path(__file__).parent resolves into sys._MEIPASS there while "
        "pointing at the repo root in a dev checkout."
    )


# Files in the spec's datas that git does not track because a build step
# generates them, mapped to the script that generates them. Anything here must
# be produced before PyInstaller runs, or the build fails on a fresh clone where
# the file does not exist yet.
_GENERATED_BY = {
    "user-manual.html": "scripts/build_manual.py",
}


def _spec_data_sources() -> set[str]:
    """Every source path in nutrimagnus.spec's datas, whatever its destination."""
    text = (_PROJECT_ROOT / "nutrimagnus.spec").read_text(encoding="utf-8")
    return set(re.findall(r"\(\s*'([^']+)'\s*,\s*'[^']*'\s*\)", text))


def _is_tracked(path: str) -> bool:
    """Whether git tracks `path` -- or, for a directory, anything inside it."""
    target = _PROJECT_ROOT / path
    args = ["git", "ls-files", "--error-unmatch", path] if target.is_file() \
        else ["git", "ls-files", path]
    done = subprocess.run(args, cwd=_PROJECT_ROOT, capture_output=True, text=True)
    return done.returncode == 0 and (target.is_file() or bool(done.stdout.strip()))


def _make_rules() -> dict[str, tuple[list[str], list[str]]]:
    """Makefile targets -> (prerequisites, recipe lines)."""
    rules: dict[str, tuple[list[str], list[str]]] = {}
    current = None
    for line in (_PROJECT_ROOT / "Makefile").read_text(encoding="utf-8").splitlines():
        if line.startswith("\t") and current:
            rules[current][1].append(line.strip())
            continue
        m = re.match(r"^([A-Za-z0-9_.\-]+)\s*:(?!=)\s*(.*)$", line)
        if m:
            current = m.group(1)
            rules[current] = (m.group(2).split(), [])
        elif not line.startswith("\t"):
            current = None
    return rules


def _commands_for(target: str, rules, seen=None) -> list[str]:
    """A target's recipe lines plus those of its prerequisites, recursively --
    `release-linux: build` gets whatever `build` runs."""
    seen = seen if seen is not None else set()
    if target in seen or target not in rules:
        return []
    seen.add(target)
    prereqs, recipe = rules[target]
    out = list(recipe)
    for prereq in prereqs:
        out += _commands_for(prereq, rules, seen)
    return out


def test_every_bundled_file_is_tracked_or_generated_by_a_declared_step():
    """A spec datas entry that git ignores does not exist in a fresh clone, so
    PyInstaller fails on it -- and only on someone else's machine, or yours after
    a clean checkout, never on the machine where the file happens to be lying
    around. Either git tracks it, or _GENERATED_BY has to say what makes it."""
    missing = []
    for source in sorted(_spec_data_sources()):
        if _is_tracked(source) or source in _GENERATED_BY:
            continue
        missing.append(source)
    assert not missing, (
        f"nutrimagnus.spec bundles {missing}, which git neither tracks nor "
        "_GENERATED_BY explains. A fresh clone will not have them and the build "
        "will fail there. Commit the file, or add it to _GENERATED_BY naming the "
        "script that generates it."
    )


def test_every_bundle_build_generates_the_files_it_bundles():
    """Every Makefile target that produces a bundle must first run the generator
    for each generated file the spec bundles. `build-windows` did not (it only
    tars the working tree and builds in the VM), so it depended on
    user-manual.html already existing -- invisible until a fresh clone."""
    rules = _make_rules()
    builders = [t for t in rules
                if any(re.search(r"pyinstaller|build-windows\.sh", c)
                       for c in _commands_for(t, rules))]
    assert builders, "sanity check: expected at least one bundle-building target"
    problems = []
    for target in sorted(builders):
        commands = " ; ".join(_commands_for(target, rules))
        for generated, generator in _GENERATED_BY.items():
            if generator not in commands:
                problems.append(f"{target} bundles {generated} but never runs {generator}")
    assert not problems, (
        "Bundle builds that do not generate a file the spec bundles:\n  "
        + "\n  ".join(problems)
    )


def test_the_locally_built_gi_table_is_never_bundled():
    """gi_data_local.json is built from the Atkinson 2021 tables, whose licence
    permits text and data mining but forbids redistribution. Shipping it inside a
    packaged build would be redistribution, so it must stay out of datas however
    convenient it looks on a developer machine that happens to have one."""
    bundled = _spec_bundled_root_files()
    assert "gi_data_local.json" not in bundled, (
        "nutrimagnus.spec bundles gi_data_local.json -- that table is built from "
        "a source that forbids redistribution. Ship gi_data.json (the Creative "
        "Commons 2008 baseline) and scripts/build_gi_data.py instead."
    )


def test_every_backend_root_file_is_bundled_in_the_spec():
    used = _root_relative_files_used_by_backend()
    assert used, "sanity check: backend.py should reference at least one _PROJECT_ROOT file"
    bundled = _spec_bundled_root_files()
    missing = used - bundled
    assert not missing, (
        f"nutrimagnus.spec's datas is missing {missing} -- these files will "
        "404 in any packaged (PyInstaller) build even though they work fine "
        "in a dev checkout, since _PROJECT_ROOT only equals the repo root "
        "unpackaged."
    )


# ── README test-suite section ─────────────────────────────────────────────
# The "## Test Suite" section of README-numa-documentation.md is hand-written
# and was only ever checked by the monthly accuracy pass, so it drifted badly
# (it claimed 733 tests when the suite had grown past 1,100, and was missing
# a dozen test files). The mechanical parts of it are checkable on every run,
# which is what this does — the prose descriptions still need a human.

_README = _PROJECT_ROOT / "README-numa-documentation.md"
# Infrastructure, not test files: no behavior of their own to describe, and
# the e2e directory gets its own prose section rather than table rows.
_NOT_TABLE_ROWS = {"tests/__init__.py", "tests/conftest.py"}


def _readme_listed_test_files() -> set[str]:
    rows = re.findall(r"^\|\s*`(tests/[\w/]+\.py)`", _README.read_text(encoding="utf-8"), re.M)
    return set(rows)


def _actual_test_files() -> set[str]:
    return {
        p.relative_to(_PROJECT_ROOT).as_posix()
        for p in (_PROJECT_ROOT / "tests").rglob("test_*.py")
        if "__pycache__" not in p.parts and "e2e" not in p.parts
    }


def test_readme_test_table_lists_every_test_file():
    missing = _actual_test_files() - _readme_listed_test_files() - _NOT_TABLE_ROWS
    assert not missing, (
        f"README-numa-documentation.md's Test Suite table is missing {sorted(missing)} — "
        "add a row describing what each one covers."
    )


def test_readme_test_table_has_no_rows_for_deleted_files():
    stale = {f for f in _readme_listed_test_files() if not (_PROJECT_ROOT / f).exists()}
    assert not stale, (
        f"README-numa-documentation.md's Test Suite table still lists {sorted(stale)}, "
        "which no longer exist."
    )
