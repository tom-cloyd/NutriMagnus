"""scripts/create_release.py's changelog handling since the 2026-11-14 split:
release notes are the SUMMARY from the manual's What's new section plus a
pointer line, and a release marks itself in docs/updates-log-details.md.

Docs: docs/claude/changelog.md; user-manual.md #updates-log.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import create_release  # noqa: E402

_MANUAL = """# Manual

## Part 8 — Your data

Text.

## What's new {: #updates-log}

<!-- Insert new updates below here -->

#### Next release summary to this point

Version overview:

SUMMARY: Short summary.

DETAILS: Long details.

- **2.** Newer change.
- **1.** Older change.

#### Release v2026-01-01-0000 summary

- **1.** Shipped before.

## Notes
"""


def test_notes_are_just_the_summary_and_the_pointer(tmp_path, monkeypatch) -> None:
    manual = tmp_path / "user-manual.md"
    manual.write_text(_MANUAL)
    monkeypatch.setattr(create_release, "MANUAL_FILE", manual)
    assert create_release._release_notes() == (
        "Short summary.\n\nSee full list of changes in the User Manual's 'What's New' section")


def test_one_line_overview_still_read_and_no_summary_stops_the_release(tmp_path, monkeypatch) -> None:
    """The older one-line overview (SUMMARY and DETAILS on one line) still
    works; with no SUMMARY at all, main() refuses before contacting GitHub."""
    manual = tmp_path / "user-manual.md"
    monkeypatch.setattr(create_release, "MANUAL_FILE", manual)
    manual.write_text(_MANUAL.replace(
        "Version overview:\n\nSUMMARY: Short summary.\n\nDETAILS: Long details.",
        "Version overview: SUMMARY: One-liner. DETAILS: Long details."))
    assert create_release._release_notes().startswith("One-liner.\n\n")

    manual.write_text(_MANUAL.replace("SUMMARY: Short summary.", ""))
    assert create_release._release_notes() is None
    monkeypatch.setenv("GITHUB_TOKEN", "x")
    monkeypatch.setattr(create_release, "_manual_links_ok", lambda: True)
    monkeypatch.setattr(create_release, "_write_starter_manifest", lambda: None)
    monkeypatch.setattr(create_release, "_ASSETS", [])

    def _no_api(*a, **kw):
        raise AssertionError("contacted GitHub")
    monkeypatch.setattr(create_release, "_api_request", _no_api)
    assert create_release.main() == 1


def test_rolling_a_release_renames_the_summary_and_marks_the_details_file(tmp_path, monkeypatch) -> None:
    manual = tmp_path / "user-manual.md"
    manual.write_text(_MANUAL)
    details = tmp_path / "updates-log-details.md"
    details.write_text("# Details\n\n<!-- Insert new updates below here -->\n\n#### Jan 5 updates\n\nEntry.\n")
    monkeypatch.setattr(create_release, "MANUAL_FILE", manual)
    monkeypatch.setattr(create_release, "DETAILS_FILE", details)
    assert create_release._roll_release_summary("v2026-02-01-0000")
    assert "#### Release v2026-02-01-0000 summary\n" in manual.read_text()
    text = details.read_text()
    assert text.index("## Release v2026-02-01-0000") < text.index("#### Jan 5 updates")
