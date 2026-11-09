"""
tests/e2e/test_search_lands_on_results_e2e.py — browser-level coverage for
base.html's data-search-form handling: running a search brings that search's
section (or its form) to the top of the window and puts focus on the first
result, on every page with a search; any other submit keeps your place.

The window is kept short so every page really has something to scroll. The
live server is a seeded fresh install (see conftest.py) and "Chickpeas" one of
its starter foods; online sources are stubbed to return nothing, but their
fetch still runs and still replaces the rows, so focus surviving that swap is
covered here too.

Docs: README-numa-documentation.md, Test Suite.
"""
import re
import urllib.parse
import urllib.request

import pytest

pytestmark = pytest.mark.e2e

_FOCUS_IN_FIRST_ROW = """
() => {
  const at = document.activeElement;
  const rows = [...document.querySelectorAll(
    '[data-search-output] tbody tr, [data-search-output] .list-group-item')]
    .filter(r => r.querySelector('a[href], input:not([type=hidden]), button'));
  if (!rows.length || !at || at === document.body) return false;
  const row = at.closest('tr, .list-group-item');
  return row === rows[0] || row === rows[1];
}
"""

# How far the section's top sits from just under the sticky navbar; 0 when
# the page ended before it could rise any further.
_TOP_GAP = """
(sel) => {
  const box = document.querySelector(sel);
  const section = box.closest('details') || box.form;
  const top = section.getBoundingClientRect().top;
  const nav = document.getElementById('main-navbar').getBoundingClientRect().height;
  const room = document.documentElement.scrollHeight - window.innerHeight - window.scrollY;
  return room < 1 ? 0 : Math.abs(top - nav);
}
"""


def _post(url: str, data: dict) -> str:
    body = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=10) as r:
        return r.url


def _search(page, url: str, box: str, term: str) -> None:
    page.set_viewport_size({"width": 1100, "height": 900})
    page.goto(url)
    page.evaluate("(sel) => { const d = document.querySelector(sel).closest('details'); if (d) d.open = true; }", box)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.locator(box).fill(term)
    with page.expect_navigation():
        page.locator(box).press("Enter")
    page.wait_for_function(_FOCUS_IN_FIRST_ROW, timeout=10_000)
    # Let the deferred online fetch land: focus has to survive it.
    page.wait_for_function("!document.querySelector('.online-search-notice')", timeout=10_000)
    page.wait_for_load_state("load")
    page.wait_for_timeout(200)
    page.wait_for_function(_FOCUS_IN_FIRST_ROW, timeout=10_000)
    # The focused row is on screen, whatever else happened.
    assert page.evaluate("""() => {
      const r = document.activeElement.getBoundingClientRect();
      return r.top >= 0 && r.bottom <= window.innerHeight + 1;
    }""")


@pytest.mark.parametrize("path, field", [
    ("/food/search", "query"),
    ("/food/analyze-portion", "query"),
    ("/food/cache", "q"),
    ("/food/convert", "q"),
    ("/food/annotate", "q"),
    ("/pantry", "search"),
    ("/compare", "search"),
    ("/food/custom-profiles", "copy_q"),
])
def test_search_lands_on_first_result(live_server, page, path, field):
    box = f'form[data-search-form] input[name="{field}"]'
    _search(page, f"{live_server}{path}", box, "Chickpeas")
    assert page.evaluate(_TOP_GAP, box) < 2


def test_recipe_search_puts_add_ingredient_at_top_and_cursor_in_amount(live_server, page):
    url = _post(f"{live_server}/recipe/new", {"name": "Search landing", "servings": "1"})
    rid = re.search(r"/recipe/(\d+)", url).group(1)
    edit = f"{live_server}/recipe/{rid}/edit"
    box = "#add-ingredient-section input[name=q]"
    _search(page, edit, box, "Chickpeas")
    assert page.evaluate(_TOP_GAP, box) < 2
    assert page.evaluate("document.activeElement.name") in ("portion_str", "amount")


def test_meal_search_puts_panel_at_top_and_adding_keeps_your_place(live_server, page):
    url = _post(f"{live_server}/meals/create", {"name": "Search landing"})
    box = "#add-food-details input[name=q]"
    _search(page, url, box, "Chickpeas")
    assert page.evaluate(_TOP_GAP, box) < 2
    assert page.evaluate("document.activeElement.name") in ("portion_str", "amount")

    # Any other submit is not a search: the results' own filter form comes
    # back to the same place, not pulled up to the panel.
    page.evaluate("window.scrollTo({top: 60, behavior: 'instant'})")
    y = page.evaluate("window.scrollY")
    with page.expect_navigation():
        page.evaluate("document.querySelector('[data-search-output] form[method=get]').requestSubmit()")
    page.wait_for_load_state("load")
    # Bootstrap's smooth scrolling is still carrying the page back here.
    page.wait_for_function("(y) => Math.abs(window.scrollY - y) < 2", arg=y, timeout=5_000)


def test_empty_search_box_does_not_jump(live_server, page):
    page.set_viewport_size({"width": 1100, "height": 900})
    page.goto(f"{live_server}/food/cache")
    page.evaluate("window.scrollTo({top: 100, behavior: 'instant'})")
    y = page.evaluate("window.scrollY")
    box = 'form[data-search-form] input[name="q"]'
    page.locator(box).fill("")
    page.evaluate("document.querySelector('form[data-search-form]').requestSubmit()")
    page.wait_for_load_state("load")
    # Bootstrap's smooth scrolling is still carrying the page back here.
    page.wait_for_function("(y) => Math.abs(window.scrollY - y) < 2", arg=y, timeout=5_000)
