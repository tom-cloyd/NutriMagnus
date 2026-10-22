"""base.html's input-ready script: a quiet (outline/secondary) submit button
turns solid blue (class btn-input-ready) while its form has something typed
or picked in a box to act on.

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
    m = re.search(r"<script>\s*// Buttons that act on what's typed.*?</script>", BASE.read_text(), re.S)
    assert m, "input-ready script not found in base.html"
    return m.group(0)[len("<script>"):-len("</script>")]


_STUB = r"""
var CASES = CASES_JSON;
var buttons = CASES.map(function (c) {
  var cls = new Set();
  var form = {handlers: {}, elements: c.boxes.map(function (b) {
                return {type: b[0], value: b[1], disabled: false}; }),
              addEventListener(t, f) { this.handlers[t] = f; }};
  return {textContent: c.label, cls: cls, form: c.no_form ? null : form,
          matches() { return c.quiet !== false; },
          hasAttribute(a) { return (c.attrs || []).indexOf(a) !== -1; },
          classList: {toggle(k, on) { if (on) cls.add(k); else cls.delete(k); }}};
});
var document = {querySelectorAll() { return buttons; }};
"""


def _run(cases, then=""):
    js = (_STUB.replace("CASES_JSON", json.dumps(cases)) + _script() + then +
          "\nconsole.log(JSON.stringify(buttons.map(function (b) {"
          " return b.cls.has('btn-input-ready'); })));")
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_lights_quiet_buttons_with_something_to_act_on() -> None:
    lit = _run([{"label": "Show", "boxes": [["number", "30"]]},
                {"label": "Calculate", "boxes": [["select-one", "all"], ["hidden", "x"]]},
                {"label": "Filter", "boxes": [["date", ""]]},
                {"label": "Show", "boxes": [["number", "  "]]},
                {"label": "Remove", "boxes": [["hidden", "7"]]},
                {"label": "Save changes", "boxes": [["text", "oat"]]},
                {"label": "Search", "boxes": [["text", "oat"]]},
                {"label": "Go", "boxes": [["text", "oat"]], "attrs": ["data-search-button"]},
                {"label": "Delete", "boxes": [["text", "oat"]], "quiet": False},
                {"label": "Tick", "boxes": [["checkbox", "on"]]},
                {"label": "Show", "boxes": [], "no_form": True}])
    assert lit == [True, True, False, False, False, False, False, False, False, False, False]


def test_follows_typing_and_clearing() -> None:
    lit = _run([{"label": "Show", "boxes": [["number", ""]]},
                {"label": "Rename", "boxes": [["text", "oat"]]}],
               then="\nbuttons[0].form.elements[0].value = '9'; buttons[0].form.handlers.input();"
                    "\nbuttons[1].form.elements[0].value = ''; buttons[1].form.handlers.input();")
    assert lit == [True, False]
