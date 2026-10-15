"""base.html's search-button script: a Search/Filter button lights up
(class btn-search-ready) while its text box has something in it.

Runs the shipped script under Node with a stubbed page. Skipped where Node
isn't installed.
Docs: README-numa-documentation.md, "Search buttons light up when there's text to search".
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="needs Node")

BASE = Path(__file__).resolve().parent.parent / "web" / "templates" / "base.html"


def _script() -> str:
    m = re.search(r"<script>\s*// Search buttons light up.*?</script>", BASE.read_text(), re.S)
    assert m, "search-button script not found in base.html"
    return m.group(0)[len("<script>"):-len("</script>")]


_STUB = r"""
function mkInput(value) {
  return {value: value, handlers: {},
          addEventListener(t, f) { this.handlers[t] = f; }};
}
function mkButton(label, input, attrs) {
  var cls = new Set();
  var group = {querySelector() { return input; }};
  return {textContent: label, cls: cls, parentElement: group,
          hasAttribute(a) { return (attrs || []).indexOf(a) !== -1; },
          closest() { return group; },
          classList: {toggle(c, on) { if (on) cls.add(c); else cls.delete(c); }}};
}
var CASES = CASES_JSON;
var buttons = CASES.map(function (c) {
  var input = c.no_input ? null : mkInput(c.value);
  var b = mkButton(c.label, input, c.attrs);
  b.input = input;
  return b;
});
var document = {querySelectorAll() { return buttons; }};
"""


def _run(cases, then=""):
    js = (_STUB.replace("CASES_JSON", json.dumps(cases)) + _script() + then +
          "\nconsole.log(JSON.stringify(buttons.map(function (b) {"
          " return b.cls.has('btn-search-ready'); })));")
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_lights_only_search_buttons_with_text() -> None:
    lit = _run([{"label": "Search", "value": "peanut"},
                {"label": "Search", "value": "   "},
                {"label": "Filter this list", "value": "oat"},
                {"label": "Search online", "value": "oat"},
                {"label": "Save", "value": "oat"},
                {"label": "Go", "value": "x", "attrs": ["data-search-button"]},
                {"label": "Search", "value": "", "no_input": True}])
    assert lit == [True, False, True, False, False, True, False]


def test_follows_typing_and_clearing() -> None:
    lit = _run([{"label": "Search", "value": ""}, {"label": "Filter", "value": "oat"}],
               then="\nbuttons[0].input.value = 'rice'; buttons[0].input.handlers.input();"
                    "\nbuttons[1].input.value = ''; buttons[1].input.handlers.input();")
    assert lit == [True, False]
