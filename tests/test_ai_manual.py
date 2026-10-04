"""Tests for scripts/build_ai_manual.py — the AI edition of the manual.

Docs: README-numa-documentation.md, "AI help edition of the manual".
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_ai_manual  # noqa: E402
from build_manual import SOURCE  # noqa: E402

_SAMPLE = """\
# NutriMagnus User Manual

*Updated 2026-09-30:1200* / Reading time: 6 hours, 18 minutes

## Part 1 — Start {: #start}

*(Reading time: 5 minutes)*

See [Backing up your data](#backup), the [DIAAS](#gloss-diaas) score,
[how](#backup) to do it, [the log](#updates-log), [an entry](#jan-entry),
[settings](/settings) and [USDA](https://fdc.nal.usda.gov/).
A cited fact.[^1]

<!-- hidden scope text -->

### Backing up your data {: #backup}

Copy the folder.

## Part 11 — Recent program updates log {: #updates-log}

#### January entry {: #jan-entry}

OLD LOG TEXT

## Notes

[^1]: The source.
"""


def _build(text=_SAMPLE):
    doc, unresolved = build_ai_manual.build(text)
    return doc, unresolved


def test_reading_times_comments_and_part_11_are_removed() -> None:
    doc, _ = _build()
    assert "Reading time" not in doc
    assert "hidden scope text" not in doc and "<!--" not in doc
    assert "OLD LOG TEXT" not in doc and "January entry" not in doc
    assert "Updated 2026-09-30:1200" in doc


def test_links_become_plain_text_naming_their_destination() -> None:
    doc, unresolved = _build()
    assert unresolved == []
    # Link text already names the destination: just add the Part.
    assert "See Backing up your data (Part 1)" in doc
    # Other wording: name the destination.
    assert "how (see “Backing up your data”, Part 1)" in doc
    # Glossary links keep only the word.
    assert "the DIAAS score" in doc
    # Into the omitted Part 11 -- the heading itself or anything inside it.
    assert "the log (not included in this edition)" in doc
    assert "an entry (not included in this edition)" in doc
    # App routes lose the link; external links keep it.
    assert "settings and" in doc
    assert 'href="https://fdc.nal.usda.gov/"' in doc
    assert not re.search(r'href="(?!https?:|mailto:)', doc)


def test_footnotes_become_plain_markers() -> None:
    doc, _ = _build()
    assert "A cited fact.<sup>[1]</sup>" in doc
    assert "The source." in doc
    assert "footnote-backref" not in doc


def test_real_manual_builds_cleanly() -> None:
    raw = SOURCE.read_text(encoding="utf-8")
    doc, unresolved = build_ai_manual.build(raw)
    assert unresolved == []
    assert "Reading time" not in doc and "<!--" not in doc
    assert "Insert new updates below here" not in doc
    assert "Next release summary" not in doc
    assert not re.search(r'href="(?!https?:|mailto:)', doc)
    # A Google Doc holds at most ~1.02 million characters.
    assert len(re.sub(r"<[^>]+>", "", doc)) < 900_000
