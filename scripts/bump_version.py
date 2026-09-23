#!/usr/bin/env python3
"""Bump version.py's VERSION stamp to now.

Docs: README-numa-documentation.md, Maintenance section.

Run this instead of hand-editing version.py whenever CLAUDE.md's "bump
version.py before ending a session that changed behavior" rule applies.
NEW_VERSION_NOTE still needs a manual edit (it's a human summary), and the
manual's own timestamp is separate — see CLAUDE.md.

RELEASE_VERSION's -rc.N/-beta.N/-alpha.N counter is deliberately NOT touched
here (decided 2026-09-21) — it now advances only when an actual release is
cut, not on every dev-session bump, so it means something (see version.py's
own comment above RELEASE_VERSION).
"""
import re
import subprocess
from pathlib import Path

VERSION_PATH = Path(__file__).resolve().parent.parent / "version.py"

_STAMP_RE = re.compile(r'^(VERSION = ")[^"]*(")', re.M)


def bump(text: str, now: str) -> str:
    return _STAMP_RE.sub(lambda m: f"{m.group(1)}{now}{m.group(2)}", text, count=1)


def main() -> None:
    now = subprocess.check_output(["date", "+%Y-%m-%d:%H%M"], text=True).strip()
    original = VERSION_PATH.read_text()
    updated = bump(original, now)
    VERSION_PATH.write_text(updated)

    old_stamp = re.search(r'VERSION = "([^"]*)"', original).group(1)
    print(f"VERSION: {old_stamp} -> {now}")


if __name__ == "__main__":
    main()
