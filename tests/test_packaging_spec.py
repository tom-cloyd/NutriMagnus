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
