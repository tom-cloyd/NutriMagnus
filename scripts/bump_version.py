#!/usr/bin/env python3
"""Bump version.py's VERSION stamp to now and auto-increment RELEASE_VERSION's
pre-release counter (the trailing -rc.N / -beta.N / -alpha.N number).

Docs: README-numa-documentation.md, Maintenance section.

Run this instead of hand-editing version.py whenever CLAUDE.md's "bump
version.py before ending a session that changed behavior" rule applies.
NEW_VERSION_NOTE still needs a manual edit (it's a human summary), and the
manual's own timestamp is separate — see CLAUDE.md.
"""
import re
import subprocess
from pathlib import Path

VERSION_PATH = Path(__file__).resolve().parent.parent / "version.py"

_RELEASE_RE = re.compile(r'^(RELEASE_VERSION = ")(.*?)(-(?:rc|beta|alpha)\.)(\d+)("\s*)$', re.M)
_STAMP_RE = re.compile(r'^(VERSION = ")[^"]*(")', re.M)


def bump(text: str, now: str) -> str:
    text = _STAMP_RE.sub(lambda m: f"{m.group(1)}{now}{m.group(2)}", text, count=1)

    def _incr(m: re.Match) -> str:
        return f"{m.group(1)}{m.group(2)}{m.group(3)}{int(m.group(4)) + 1}{m.group(5)}"

    new_text = _RELEASE_RE.sub(_incr, text, count=1)
    if new_text == text:
        raise SystemExit(
            "RELEASE_VERSION has no -rc./-beta./-alpha.N suffix to bump "
            "(e.g. it may already be a plain 1.0.0 release) -- edit version.py by hand."
        )
    return new_text


def main() -> None:
    now = subprocess.check_output(["date", "+%Y-%m-%d:%H%M"], text=True).strip()
    original = VERSION_PATH.read_text()
    updated = bump(original, now)
    VERSION_PATH.write_text(updated)

    old_stamp = re.search(r'VERSION = "([^"]*)"', original).group(1)
    old_release = re.search(r'RELEASE_VERSION = "([^"]*)"', original).group(1)
    new_release = re.search(r'RELEASE_VERSION = "([^"]*)"', updated).group(1)
    print(f"VERSION:         {old_stamp} -> {now}")
    print(f"RELEASE_VERSION: {old_release} -> {new_release}")


if __name__ == "__main__":
    main()
