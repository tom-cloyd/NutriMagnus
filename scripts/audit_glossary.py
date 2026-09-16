#!/usr/bin/env python3
"""
audit_glossary.py — Find candidate terms in user-manual.md that look like
they should have a Glossary entry (Part 9, `{: #gloss-*}`) but don't.

Not a link-density checker: Glossary linking has never been exhaustive by
design (see README-numa-documentation.md's Maintenance section) — most
occurrences of an already-glossaried term like DCP or DIAAS are deliberately
left unlinked, one link per passage being the convention, not one per
mention. This script only flags terms with NO glossary entry at all.

Candidates are all-caps tokens (2-6 letters, e.g. CSV, RDA, GI) that appear
more than once in the manual body. Fenced code blocks and hidden
`<!-- Scope: -->` developer comments are excluded, since identifiers and
internal notes there aren't reader-facing terms. The Glossary section
itself is excluded from candidate-scanning (a term shouldn't be flagged
against its own definition).

Output is a candidate list sorted by frequency — real gaps mixed with noise
(proper nouns, source-code identifiers, stray capitalized words). Triage is
a human/Claude judgment call, not automated further; see the Maintenance
section's "Quarterly glossary audit" procedure for how it's meant to be
used.

Run from the project root: python scripts/audit_glossary.py
Docs: README-numa-documentation.md, Maintenance -> Quarterly glossary audit
"""
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANUAL = PROJECT_ROOT / "user-manual.md"

# Tokens that are structurally certain to be noise, not candidate glossary
# terms, no matter how often they appear — Part/Appendix letters and Roman
# numerals used as list markers.
_ALWAYS_SKIP = {
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N",
    "O", "P", "Q", "R", "S", "T", "U", "W", "Y", "Z",
}

# Ordinary English words that happen to appear in all caps somewhere in the
# manual (most commonly: the "Recent program updates log"'s ALL-CAPS TITLE
# convention, one word of which alone might not be all-caps but the phrase
# is). Without this, an English sentence written in caps drowns out every
# real candidate below it. Extend if a future run surfaces more of these —
# it isn't meant to be a complete stopword list, just enough for this manual.
_ENGLISH_STOPWORDS = {
    "THE", "AND", "NOW", "TO", "IN", "NO", "YOU", "ONE", "IS", "FOR", "NEW",
    "ON", "CAN", "WITH", "ANY", "AS", "FROM", "IT", "NOT", "OF", "WHEN",
    "YOUR", "ABOUT", "AFTER", "AN", "ARE", "AT", "HAS", "HOW", "ITS",
    "THAT", "WHAT", "ACROSS", "BY", "COULD", "DID", "EVERY", "IF", "JUST",
    "ONCE", "OUT", "OWN", "PER", "RE", "SEE", "STILL", "TWO", "WHICH",
    "WHOLE", "TOP", "TOLD", "QUIT", "GETS", "FOUND", "BEHIND", "LAST",
    "EACH", "ALWAYS", "LONGER", "FIXED", "SHOWS", "SHOW", "STAYS", "NOTE",
    "RIGHT", "FROM", "LINK", "BUILD", "COPY", "EDIT", "FOODS", "NC",
    "STALE", "TIER", "CLICK", "COLUMN", "CUSTOM", "EASIER", "HAS", "LIST",
    "OFFERS", "RECENT", "ROLL", "TABLES", "UNITS", "VOLUME", "APP",
    "BUTTON", "CLOSED", "COLOR", "COVERS", "CURSOR", "DATE", "DETAIL",
    "DRAFT", "FACTOR", "FETCH", "FIELDS", "GAP", "GAPS", "GOAL", "LABEL",
    "LINE", "LOG", "MATCH", "NAME", "NEWER", "NUMBER", "OUT", "PAGES",
    "PRINT", "RESULT", "SCALE", "SORT", "SWEEP", "TABLE", "TARGET", "TEST",
    "TEXT", "TITLE", "WEEKLY", "WEIGHT", "PAGE", "PLOT", "UPDATE", "FOOD",
    "SEARCH", "HOME", "MANUAL", "MEAL", "RECIPE", "DAY", "DAYS", "FIX",
    "BUG", "DATA", "BANNER", "CHOOSE", "STAY",
}

_GLOSSARY_HEADING_RE = re.compile(r"^#{2,3}\s+.*Glossary", re.MULTILINE)
_NEXT_HEADING_RE = re.compile(r"^#{1,3}\s+", re.MULTILINE)
_GLOSSARY_TERM_RE = re.compile(r"^\*\*(.+?)\*\*(?:\{: #gloss-[\w-]+\})?\s+—", re.MULTILINE)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_CODE_FENCE_RE = re.compile(r"^```.*?\n^```[ \t]*$", re.DOTALL | re.MULTILINE)
_CHANGELOG_HEADING_RE = re.compile(r"^###\s+.*Recent program updates log", re.MULTILINE)
_ACRONYM_RE = re.compile(r"\b[A-Z]{2,6}\b")


def split_glossary_section(text: str) -> tuple[str, str]:
    """Return (body_without_glossary, glossary_section_text)."""
    m = _GLOSSARY_HEADING_RE.search(text)
    if not m:
        sys.exit("Could not find a '## ... Glossary' heading in user-manual.md")
    start = m.start()
    next_heading = _NEXT_HEADING_RE.search(text, m.end())
    end = next_heading.start() if next_heading else len(text)
    return text[:start] + text[end:], text[start:end]


def existing_glossary_terms(glossary_text: str) -> set[str]:
    """Every defined term's exact bolded text, e.g. {'AA', 'AI', 'CGM', ...}."""
    return {m.group(1).strip() for m in _GLOSSARY_TERM_RE.finditer(glossary_text)}


def strip_non_reader_text(text: str) -> str:
    """Remove hidden dev-facing content a reader never sees (HTML comments,
    i.e. Scope: blocks, and fenced code blocks), plus the "Recent program
    updates log" — its ALL-CAPS TITLE convention (see CLAUDE.md) generates
    huge amounts of incidental all-caps English noise unrelated to real
    terminology, and any genuinely new term worth defining will also appear
    in the manual's main body, not only in a changelog entry."""
    text = _HTML_COMMENT_RE.sub("", text)
    text = _CODE_FENCE_RE.sub("", text)
    m = _CHANGELOG_HEADING_RE.search(text)
    if m:
        end = _NEXT_HEADING_RE.search(text, m.end())
        text = text[:m.start()] + (text[end.start():] if end else "")
    return text


def find_candidates(body_text: str, known_terms: set[str]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for m in _ACRONYM_RE.finditer(body_text):
        token = m.group(0)
        if token in _ALWAYS_SKIP or token in known_terms or token in _ENGLISH_STOPWORDS:
            continue
        counts[token] = counts.get(token, 0) + 1
    # Only tokens appearing more than once are worth a look — a true one-off
    # is unlikely to need a standalone definition.
    return sorted(((t, c) for t, c in counts.items() if c > 1),
                   key=lambda tc: (-tc[1], tc[0]))


def main() -> None:
    text = MANUAL.read_text()
    body, glossary = split_glossary_section(text)
    known = existing_glossary_terms(glossary)
    scannable = strip_non_reader_text(body)
    candidates = find_candidates(scannable, known)

    print(f"{len(known)} existing glossary terms found.")
    print(f"{len(candidates)} candidate token(s) with no glossary entry, appearing >1 time:\n")
    for token, count in candidates:
        print(f"{count:4d}  {token}")


if __name__ == "__main__":
    main()
