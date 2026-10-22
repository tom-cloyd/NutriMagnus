"""Search terms lines in user-manual.md: hidden on the built page, still
searchable, and a malformed one fails the build instead of showing.
Docs: CLAUDE.md, "Search terms lines"; README-numa-documentation.md,
Manual updates / Search terms lines.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from build_manual import (  # noqa: E402
    JS, SOURCE, check_search_terms, count_words, hide_search_terms,
)


def test_line_becomes_hidden_span():
    out = hide_search_terms("#### Water\n\n*Search terms: seniors, over 65.*\n\nText.\n")
    assert '<span class="search-terms" hidden>Search terms: seniors, over 65.</span>' in out
    assert "*Search terms" not in out


def test_malformed_lines_are_reported():
    raw = ("*Search terms: fine, ok.*\n"
           "*Search terms: trailing prose.* More words here.\n"
           "Search terms: no italics\n"
           "*Search terms: unclosed\n")
    assert [n for n, _ in check_search_terms(raw)] == [2, 3, 4]


def test_lines_left_out_of_reading_time():
    assert count_words("Hello world.\n\n*Search terms: a, b, c, d, e.*\n") == 2


def test_highlighter_skips_hidden_terms():
    assert ".search-terms" in JS


def test_manual_source_has_no_malformed_lines():
    assert check_search_terms(SOURCE.read_text(encoding="utf-8")) == []


def test_review_lists_changed_sections():
    from search_terms_review import review
    old = ("## Part 1\n\n### A. Install {: #a}\n\n*Search terms: setup.*\n\nOld text.\n\n"
           "### B. Tips\n\nSame.\n\n### C. Backup\n\nOld.\n\n### D. Terms only\n\nSame.\n\n"
           "<!-- Insert new updates below here -->\n\n#### Log\n\nOld log.\n")
    new = ("## Part 1\n\n### A. Install {: #a} <!-- t:26-10-21 -->\n\n*Search terms: setup.*\n\nNew text.\n\n"
           "### B. Tips\n\nSame.\n\n### C. Backup\n\nNew.\n\n"
           "### D. Terms only\n\n*Search terms: just added.*\n\nSame.\n\n### E. Fresh\n\nHi.\n\n"
           "<!-- Insert new updates below here -->\n\n#### Log\n\nNew log.\n")
    with_terms, without = review(old, new)
    assert with_terms == ["Part 1 › A. Install"]
    assert without == ["Part 1 › C. Backup", "Part 1 › E. Fresh  (new)"]
