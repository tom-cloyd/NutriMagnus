"""Formatting checks over user-manual.md that don't belong in build_manual.py's
runtime path but should still fail CI, not just a manually-run build.
Docs: user-manual.md, Appendix A changelog entry for 2026-09-03.
"""
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from build_manual import SOURCE, check_adjacent_footnotes  # noqa: E402


def test_no_adjacent_footnotes_without_separator() -> None:
    raw = SOURCE.read_text(encoding="utf-8")
    bad_pairs = check_adjacent_footnotes(raw)
    assert not bad_pairs, (
        "Adjacent footnote refs render as run-together digits (e.g. \"45\") "
        "unless separated by a superscript comma, e.g. [^4]<sup>,</sup>[^5]. "
        f"Found: {bad_pairs}"
    )
