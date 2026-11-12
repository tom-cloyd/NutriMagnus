"""
tests/e2e/test_search_arrow_keys_e2e.py — browser-level coverage for
base.html's Up/Down arrow keys in search-result lists ([data-search-output]):
the focused result moves one result down or up, and coming Back from a
result opened with Enter puts focus on that same result again.

Uses the seeded fresh install's starter recipes (see conftest.py) on the
Recipes page, whose filter lists them by name link.

Docs: README-numa-documentation.md, Test Suite.
"""
import pytest

pytestmark = pytest.mark.e2e

_FOCUSED = "() => { const e = document.activeElement; return e.tagName + '|' + (e.getAttribute('href') || ''); }"


def test_arrow_keys_move_between_results_and_back_returns_to_the_same_one(page, live_server):
    page.set_viewport_size({"width": 1100, "height": 900})
    page.goto(live_server + "/recipes")
    page.fill("input[name=q]", "e")
    page.press("input[name=q]", "Enter")
    page.wait_for_load_state("load")
    page.wait_for_timeout(300)

    links = page.eval_on_selector_all(
        "[data-search-output] tbody tr td.js-name-cell a[href]", "as => as.map(a => a.getAttribute('href'))")
    assert len(links) >= 3, links
    assert page.evaluate(_FOCUSED) == f"A|{links[0]}"     # lands on the first result

    page.keyboard.press("ArrowDown")
    page.keyboard.press("ArrowDown")
    assert page.evaluate(_FOCUSED) == f"A|{links[2]}"
    page.keyboard.press("ArrowUp")
    assert page.evaluate(_FOCUSED) == f"A|{links[1]}"
    page.keyboard.press("ArrowUp")
    page.keyboard.press("ArrowUp")                        # already at the top: stays there
    assert page.evaluate(_FOCUSED) == f"A|{links[0]}"

    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.wait_for_url("**" + links[1])
    page.go_back()
    page.wait_for_load_state("load")
    page.wait_for_timeout(300)
    assert page.evaluate(_FOCUSED) == f"A|{links[1]}"
