#!/usr/bin/env python3
"""List the user-manual.md sections whose text changed since the last weekly
sweep, so their *Search terms* lines get reread (weekly sweep item 10).

Compares user-manual.md as it is now (uncommitted edits included) with its
copy at an earlier commit, section by section (every ##/###/#### heading),
and prints two lists:

  1. changed sections that HAVE a Search terms line: reread the list against
     the new text, dropping terms it no longer covers, adding any it needs;
  2. changed or new sections WITHOUT one: decide whether they need one.

The Recent program updates log (Part 11) is left out; its entries are
never searched for by topic. Nothing is written; no state is kept.

Usage:
  python scripts/search_terms_review.py              # since the last sweep commit
  python scripts/search_terms_review.py --since 1aa274c
  python scripts/search_terms_review.py --since 2026-10-14

The default starting point is the newest commit whose message mentions
"sweep" (that is how sweep commits are named); it is printed, so check it.
A date means the last commit on or before that day.

Docs: CLAUDE.md, "Search terms lines"; README-numa-documentation.md,
Maintenance -> Weekly sweep, item 10.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANUAL = "user-manual.md"
LOG_MARKER = "<!-- Insert new updates below here -->"
_HEADING_RE = re.compile(r"^(#{2,4}) (.+?)\s*$", re.MULTILINE)
_TERMS_RE = re.compile(r"^\*Search terms: [^*\n]+\*[ \t]*$", re.MULTILINE)
# Lines the build regenerates on its own: Part reading times.
_GENERATED_RE = re.compile(r"^\*\(Reading time: [^)]*\)\*[ \t]*$", re.MULTILINE)


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def heading_key(raw: str) -> str:
    """A heading's identity: its text without {: #anchor} or <!-- --> tags,
    so a re-stamped review date or added anchor isn't a different section."""
    raw = re.sub(r"<!--.*?-->", "", raw)
    raw = re.sub(r"\{:[^}]*\}", "", raw)
    return raw.strip()


def sections(text: str) -> dict[str, str]:
    """{heading key: body} for every ##-#### section before the updates log.
    A repeated heading (several "Step 1" under different parents) is keyed
    with its parent headings, so each stays distinct."""
    cut = text.find(LOG_MARKER)
    if cut != -1:
        text = text[:cut]
    heads = list(_HEADING_RE.finditer(text))
    out: dict[str, str] = {}
    trail: dict[int, str] = {}
    for i, h in enumerate(heads):
        level = len(h.group(1))
        key = heading_key(h.group(2))
        trail[level] = key
        for deeper in [lv for lv in trail if lv > level]:
            del trail[deeper]
        full = " › ".join(trail[lv] for lv in sorted(trail))
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = _GENERATED_RE.sub("", text[h.end():end])
        out[full] = body
    return out


def _normalize(body: str) -> str:
    return re.sub(r"\s+", " ", body).strip()


def resolve_since(since: str | None) -> str:
    if since is None:
        ref = _git("log", "-1", "--format=%H", "-i", "--grep=sweep").strip()
        if not ref:
            sys.exit("No commit mentions 'sweep'; pass --since <commit or date>.")
        return ref
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", since):
        ref = _git("rev-list", "-1", f"--before={since} 23:59:59", "HEAD").strip()
        if not ref:
            sys.exit(f"No commit on or before {since}.")
        return ref
    return _git("rev-parse", since).strip()


def review(old_text: str, new_text: str) -> tuple[list[str], list[str]]:
    old, new = sections(old_text), sections(new_text)
    with_terms, without = [], []
    for key, body in new.items():
        before = old.get(key)
        if before is not None and _normalize(before) == _normalize(body):
            continue
        # A section whose only change is its own terms line was just reviewed.
        if before is not None and _normalize(_TERMS_RE.sub("", before)) == _normalize(_TERMS_RE.sub("", body)):
            continue
        label = key + ("  (new)" if before is None else "")
        (with_terms if _TERMS_RE.search(body) else without).append(label)
    return with_terms, without


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--since", help="commit or YYYY-MM-DD (default: last commit mentioning 'sweep')")
    args = ap.parse_args()
    ref = resolve_since(args.since)
    info = _git("log", "-1", "--format=%h %ad %s", "--date=short", ref).strip()
    old_text = _git("show", f"{ref}:{MANUAL}")
    new_text = (ROOT / MANUAL).read_text(encoding="utf-8")
    with_terms, without = review(old_text, new_text)

    print(f"Comparing {MANUAL} now with {info}\n")
    print(f"1. Changed, HAS a Search terms line — reread it ({len(with_terms)}):")
    for k in with_terms:
        print(f"   - {k}")
    if not with_terms:
        print("   (none)")
    print(f"\n2. Changed or new, NO Search terms line — does it need one? ({len(without)}):")
    for k in without:
        print(f"   - {k}")
    if not without:
        print("   (none)")


if __name__ == "__main__":
    main()
