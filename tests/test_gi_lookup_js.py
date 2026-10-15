"""The Annotate page's GI lookup results, as its own script draws them.

The rows, the "no row is X itself" note and the stand-ins table are built in
client-side JavaScript, so the route tests in test_web.py can't see them; a
refactor once drew every row as "undefined". This renders the real page, lifts
its lookup script out, and runs it under Node with a stubbed DOM and a stubbed
fetch answering the way the gi-lookup route does. Skipped where Node isn't
installed.
Docs: user-manual.md, "Choosing a GI value" (#gi-stand-in); README-numa-documentation.md,
"GI reference table lookup".
"""
import json
import re
import shutil
import subprocess

import pytest
from fastapi.testclient import TestClient

import web.backend as backend

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="needs Node")

_STUB = r"""
var els = {};
function el(id) {
  if (!els[id]) els[id] = {
    id: id, value: '', innerHTML: '', open: true, classList: {add() {}, remove() {}},
    addEventListener(type, fn) { this['on' + type] = fn; },
    dispatchEvent() {}, focus() {}, querySelectorAll() { return []; },
  };
  return els[id];
}
var document = {getElementById: el};
function Event() {}
el('gi-lookup-query').value = QUERY;
el('gi-lookup-population').value = 'both';
el('gi-no-match-help').innerHTML = '<p>No matches found.</p>';
var fetch = function () {
  return Promise.resolve({json: function () { return Promise.resolve(DATA); }});
};
"""


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path, monkeypatch) -> None:
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)
    from numa_app.services import manual_build as _manual_build
    monkeypatch.setattr(_manual_build, "rebuild_manual_if_stale", lambda: None)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


def _row(name, gi=14.0):
    return {"name": name, "gi_glucose": gi, "sem": None, "year": 2001, "country": None,
            "population": "normal", "subjects_type": None, "subjects_n": None,
            "iso": True, "edition": 2021, "ref": None, "score": 0.9}


def _results_html(page: str, query: str, data: dict) -> str:
    scripts = re.findall(r"<script>(.*?)</script>", page, re.S)
    script = next((s for s in scripts if "gi-lookup-search" in s), None)
    assert script, "GI lookup script not found on the page"
    js = (_STUB.replace("QUERY", json.dumps(query)).replace("DATA", json.dumps(data))
          + script
          + "\nel('gi-lookup-search').onclick();"
            "\nsetTimeout(function () { console.log(el('gi-lookup-results').innerHTML); }, 0);\n")
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return out.stdout


def test_results_note_and_stand_ins_are_drawn(client, cached_food) -> None:
    page = client.get(f"/food/annotate/{cached_food['fdcId']}").text
    data = {"results": [_row("Biscuits, filled with peanut butter", 40.0)],
            "direct_match": False,
            "stand_ins": [{"word": "peanut", "rows": [_row("Peanuts")]}]}
    html = _results_html(page, "peanut butter", data)
    assert "undefined" not in html
    assert "No row in the table is “peanut butter” itself" in html
    assert html.count('class="gi-pick-row"') == 2
    assert "Biscuits, filled with peanut butter" in html and "Peanuts" in html
    # A picked stand-in's saved source says what it stood in for.
    m = re.search(r'data-name="Peanuts" data-source="([^"]*)"', html)
    assert m and "used as a stand-in for “peanut butter”" in m.group(1)


def test_a_direct_match_draws_no_note_and_no_stand_ins(client, cached_food) -> None:
    page = client.get(f"/food/annotate/{cached_food['fdcId']}").text
    html = _results_html(page, "peanuts",
                         {"results": [_row("Peanuts")], "direct_match": True, "stand_ins": []})
    assert "undefined" not in html
    assert "itself" not in html and "stand-in" not in html
    assert html.count('class="gi-pick-row"') == 1
