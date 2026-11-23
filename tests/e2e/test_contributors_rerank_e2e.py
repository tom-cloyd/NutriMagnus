"""
tests/e2e/test_contributors_rerank_e2e.py — browser-level coverage for
_top_contributors.html's in-place re-ranking: changing Rank by or Show on a
meal page fetches the page with the new choice and swaps in only
#sec-contributors, so the window doesn't move and focus stays on the picker.
A full reload used to go to the top first, and with a remembered search in
the meal's search box (base.html puts it back into the URL with a second
load) it stayed at the top.

The meal gets six foods, so Show has more than one option.

Docs: README-numa-documentation.md, Test Suite.
"""
import urllib.parse
import urllib.request

import pytest

pytestmark = pytest.mark.e2e

_FOODS = ["Quinoa", "Onions", "pinto", "Chickpeas", "Eggs", "Pasta"]


def _post(url: str, data: dict) -> str:
    body = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=10) as r:
        return r.url


def _add(page, meal_url: str, term: str) -> None:
    page.goto(f"{meal_url}?q={urllib.parse.quote(term)}")
    page.wait_for_load_state("load")
    page.evaluate("document.querySelector('#add-food-details').open = true")
    box = page.locator('.add-food-form input[name="portion_str"]').first
    box.fill("100 g")
    with page.expect_navigation():
        box.press("Enter")
    page.wait_for_load_state("load")


def _change(page, select_id: str, index: int) -> int:
    """Centre the picker, note where the window is, pick option `index`, and
    wait for the swapped-in section. Returns the scroll position before."""
    page.evaluate("(id) => document.getElementById(id).scrollIntoView({block: 'center', behavior: 'instant'})",
                  select_id)
    page.wait_for_timeout(100)
    y = page.evaluate("window.scrollY")
    # Tag the current content: the swap replaces it, tag and all.
    page.evaluate("document.querySelector('#sec-contributors > *').dataset.old = '1'")
    page.select_option(f"#{select_id}", index=index)
    page.wait_for_function(
        "() => { const s = document.getElementById('sec-contributors');"
        " return !s.querySelector('[data-old]') && !s.hasAttribute('aria-busy'); }",
        timeout=10_000)
    page.wait_for_timeout(300)
    return y


def test_rank_by_and_show_rerank_in_place(live_server, page):
    page.set_viewport_size({"width": 1100, "height": 800})
    meal_url = _post(f"{live_server}/meals/create", {"name": "Re-rank in place"})
    for term in _FOODS:
        _add(page, meal_url, term)
    # The last add leaves "Pasta" as the meal's remembered search.
    page.goto(meal_url.split("?")[0] + "?rank=protein_g")
    page.wait_for_load_state("load")
    page.evaluate("window.__sameDocument = true")
    assert page.locator("#sec-contributors table").first.locator("tbody tr").count() == 6

    y = _change(page, "rank_nutrient", 0)
    assert page.evaluate("window.__sameDocument") is True, "the page reloaded"
    assert abs(page.evaluate("window.scrollY") - y) < 2
    assert page.evaluate("document.activeElement.id") == "rank_nutrient"
    rank = page.evaluate("document.getElementById('rank_nutrient').value")
    assert rank != "protein_g"
    query = urllib.parse.parse_qs(page.evaluate("location.search")[1:])
    assert query["rank"] == [rank] and query["q"] == ["Pasta"]

    # Back to protein, then Show: 5.
    _change(page, "rank_nutrient", page.evaluate(
        "[...document.getElementById('rank_nutrient').options].findIndex(o => o.value === 'protein_g')"))
    five = page.evaluate("[...document.getElementById('contrib_top_n').options].findIndex(o => o.value === '5')")
    y = _change(page, "contrib_top_n", five)
    assert page.evaluate("window.__sameDocument") is True
    assert abs(page.evaluate("window.scrollY") - y) < 2
    assert page.evaluate("document.activeElement.id") == "contrib_top_n"
    assert page.locator("#sec-contributors table tbody tr").first.is_visible()
    assert page.locator("#sec-contributors table").first.locator("tbody tr").count() == 5

    # The URL carries the choice, so a reload shows the same table.
    page.reload()
    page.wait_for_load_state("load")
    assert page.evaluate("document.getElementById('contrib_top_n').value") == "5"
