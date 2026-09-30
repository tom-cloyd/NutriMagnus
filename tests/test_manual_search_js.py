"""The manual's search box "Match case" and "Whole words only" checkboxes.

Both live entirely in client-side JavaScript (build_manual.JS's wordRegex()),
so nothing in the Python suite exercised them until the 2026-09-30 weekly
sweep. This lifts that one function out of the shipped script and runs it
under Node with stubbed checkboxes. Skipped where Node isn't installed.
Docs: user-manual.md, "Using this manual's search" (#search-howto); README-numa-documentation.md,
Maintenance -> Weekly sweep, item 7.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from build_manual import JS  # noqa: E402

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="needs Node")


def _word_regex_source() -> str:
    m = re.search(r"function wordRegex\(w\) \{.*?\n  \}\n", JS, re.S)
    assert m, "wordRegex() not found in build_manual.JS"
    return m.group(0)


def _matches(term: str, text: str, *, case: bool, whole: bool) -> list[str]:
    script = (
        f"var caseCheckbox = {{checked: {json.dumps(case)}}};\n"
        f"var wordCheckbox = {{checked: {json.dumps(whole)}}};\n"
        + _word_regex_source()
        + f"console.log(JSON.stringify({json.dumps(text)}.match(wordRegex({json.dumps(term)})) || []));\n"
    )
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


TEXT = "GI and gi values; logic GI, not GIs. (AI) said: AI."


def test_default_is_case_insensitive_substring_match():
    assert _matches("gi", TEXT, case=False, whole=False) == ["GI", "gi", "gi", "GI", "GI"]


def test_match_case_keeps_only_the_exact_case():
    assert _matches("GI", TEXT, case=True, whole=False) == ["GI", "GI", "GI"]


def test_whole_words_skips_a_term_inside_another_word():
    # "logic" and "GIs" no longer match.
    assert _matches("gi", TEXT, case=False, whole=True) == ["GI", "gi", "GI"]


def test_both_together():
    assert _matches("GI", TEXT, case=True, whole=True) == ["GI", "GI"]


def test_whole_words_works_beside_punctuation():
    # Lookarounds, not \\b, so "(AI)" and "AI." still count as whole words.
    assert _matches("AI", TEXT, case=True, whole=True) == ["AI", "AI"]


def test_regex_metacharacters_in_the_query_are_literal():
    assert _matches("(AI)", TEXT, case=False, whole=False) == ["(AI)"]
