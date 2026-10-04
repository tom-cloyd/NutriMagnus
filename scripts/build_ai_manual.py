#!/usr/bin/env python3
"""
build_ai_manual.py — Build the "AI edition" of the User Manual: a single
plain HTML file meant to be uploaded as a Google Doc and used as the source
for an AI notebook (Gemini Notebook / NotebookLM) that answers users'
questions about NuMa.

Run from the project root (or any directory):
    python scripts/build_ai_manual.py

Output: ai-edition/numa-manual-ai.html (git-ignored). Upload it with
scripts/upload_ai_manual.py, which runs this build first.

Differences from user-manual.html:
  - no reading times (header total and per-Part), no HTML comments
    (hidden Scope blocks and anything else commented out)
  - no Part 11 (Recent program updates log) — a historical record, not help;
    a note under the title says where to find it
  - no sidebar, search, script or styling
  - internal links become plain text, since they cannot work inside a Google
    Doc: a Glossary link keeps just its word; any other link keeps its text
    and names its destination, "(see “Heading”, Part N)", which gives the AI
    something to cite; a link into the omitted Part 11 says so instead
  - footnote references become plain "[N]" markers

Docs: README-numa-documentation.md, "AI help edition of the manual".
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.toc import TocExtension

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_manual import (  # noqa: E402
    _HEADER_LINE_RE,
    PROJECT_ROOT,
    SOURCE,
    strip_part_reading_times,
)

OUTPUT = PROJECT_ROOT / "ai-edition" / "numa-manual-ai.html"
OMITTED_PART_ID = "updates-log"
OMITTED_NOTE = "not included in this edition"

PREAMBLE = (
    "<p><em>This is the AI edition of the NutriMagnus (NuMa) User Manual, "
    "prepared as a reference for an AI assistant answering questions about "
    "NuMa. It omits Part 11, the Recent program updates log (a dated record "
    "of past changes). Cross-references to other sections are written as "
    "“(see …)”. The full manual, with working links and the updates log, "
    "opens from the Manual link at the top of every page in NuMa.</em></p>"
)

_TAG_RE = re.compile(r"<[^>]+>")
_HEADING_RE = re.compile(r'<h([1-6])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL)
_ID_RE = re.compile(r'<(\w+)\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</\1>', re.DOTALL)
_LINK_RE = re.compile(r'<a\b([^>]*)\bhref="([^"]*)"([^>]*)>(.*?)</a>', re.DOTALL)
_FOOTNOTE_REF_RE = re.compile(
    r'<sup id="fnref[^"]*"><a class="footnote-ref" href="#fn:[^"]*">([^<]*)</a></sup>'
)
_FOOTNOTE_BACKREF_RE = re.compile(r'\s*<a class="footnote-backref"[^>]*>.*?</a>', re.DOTALL)


def _text(fragment: str) -> str:
    return html.unescape(_TAG_RE.sub("", fragment)).strip()


def prepare_markdown(raw: str) -> str:
    """Source-level cleanup: reading times out, comments out."""
    text = strip_part_reading_times(raw)
    text = _HEADER_LINE_RE.sub(lambda m: m.group(1), text, count=1)
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def _render(md_text: str) -> str:
    md = markdown.Markdown(
        extensions=[
            TocExtension(permalink=False, toc_depth="1-4"),
            "tables",
            "fenced_code",
            "attr_list",
            "footnotes",
        ],
    )
    return md.convert(md_text)


def _omitted_span(body: str) -> tuple[int, int]:
    """Character span of the omitted Part 11 in the rendered body."""
    m = re.search(rf'<h2\s+id="{OMITTED_PART_ID}"', body)
    if not m:
        sys.exit(f"Error: no <h2 id=\"{OMITTED_PART_ID}\"> — has Part 11 moved?")
    nxt = re.compile(r"<h2\b|<div class=\"footnote\"").search(body, m.end())
    return m.start(), nxt.start() if nxt else len(body)


def _target_labels(body: str) -> dict[str, str]:
    """id -> (destination name, "Part N" it sits in, or "")."""
    headings = [
        (m.start(), int(m.group(1)), m.group(2), _text(m.group(3)))
        for m in _HEADING_RE.finditer(body)
    ]
    labels: dict[str, tuple[str, str]] = {}
    for m in _ID_RE.finditer(body):
        pos, id_ = m.start(), m.group(2)
        before = [h for h in headings if h[0] <= pos]
        if not before:
            continue
        own = before[-1] if before[-1][2] == id_ else None
        part = next((h for h in reversed(before) if h[1] == 2), None)
        if own:
            name = own[3]
        else:
            name = f"{_text(m.group(3))}” under “{before[-1][3]}"
        in_part = part[3].split(" — ")[0] if part and part[2] != id_ else ""
        labels[id_] = (name, in_part if in_part.startswith("Part ") else "")
    return labels


def _see(link_text: str, name: str, part: str) -> str:
    """The "(see …)" wording, without repeating what the link text says."""
    # "D. Using this manual's search" -> "using this manual's search"
    bare = re.sub(r"^[A-Z]\. ", "", name).casefold()
    if _text(link_text).casefold() in bare:
        return f" ({part})" if part else ""
    return f" (see “{name}”, {part})" if part else f" (see “{name}”)"


def build(raw: str) -> tuple[str, list[str]]:
    """Return (html document, list of unresolvable internal link targets)."""
    body = _render(prepare_markdown(raw))
    labels = _target_labels(body)
    start, end = _omitted_span(body)
    omitted_ids = set(re.findall(r'\bid="([^"]+)"', body[start:end]))
    body = body[:start] + body[end:]

    body = _FOOTNOTE_REF_RE.sub(r"<sup>[\1]</sup>", body)
    body = _FOOTNOTE_BACKREF_RE.sub("", body)

    unresolved: list[str] = []

    def relink(m: re.Match) -> str:
        href, inner = m.group(2), m.group(4)
        if href.startswith(("http://", "https://", "mailto:")):
            return m.group(0)
        if not href.startswith("#"):
            return inner                    # app route such as /disclaimer
        target = href[1:]
        if target.startswith("gloss-"):
            return inner
        if target in omitted_ids:
            return f"{inner} ({OMITTED_NOTE})"
        if target in labels:
            return inner + _see(inner, *labels[target])
        unresolved.append(target)
        return inner

    body = _LINK_RE.sub(relink, body)
    # Element ids are meaningless in a Google Doc; drop them to keep it lean.
    body = re.sub(r'\s+id="[^"]*"', "", body)
    body = body.replace("</h1>", "</h1>\n" + PREAMBLE, 1)

    doc = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        "<title>NutriMagnus User Manual — AI edition</title>\n</head>\n<body>\n"
        f"{body}\n</body>\n</html>\n"
    )
    return doc, unresolved


def main() -> Path:
    doc, unresolved = build(SOURCE.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(doc, encoding="utf-8")
    chars = len(_text(doc))
    print(f"Built: {OUTPUT}")
    print(f"  Size : {OUTPUT.stat().st_size / 1024:.1f} KB, {chars:,} text characters"
          " (a Google Doc holds at most ~1,020,000)")
    if unresolved:
        print(f"  Warning: {len(unresolved)} internal link(s) with no target, "
              f"left as plain text: {sorted(set(unresolved))}")
    return OUTPUT


if __name__ == "__main__":
    main()
