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
