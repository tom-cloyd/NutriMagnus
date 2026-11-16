"""scripts/create_release.py's changelog handling since the 2026-11-14 split:
release notes come from the manual's What's new section, and a release
marks itself in docs/updates-log-details.md.

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

- **2.** Newer change.
- **1.** Older change.

#### Release v2026-01-01-0000 summary

- **1.** Shipped before.

## Notes
"""


def test_notes_are_the_pending_summary(tmp_path, monkeypatch) -> None:
    manual = tmp_path / "user-manual.md"
    manual.write_text(_MANUAL)
    monkeypatch.setattr(create_release, "MANUAL_FILE", manual)
    notes = create_release._release_notes()
    assert notes.startswith("#### Summary")
    assert "Newer change." in notes and "Older change." in notes
    assert "Shipped before." not in notes


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
