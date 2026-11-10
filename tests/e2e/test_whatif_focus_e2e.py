"""
tests/e2e/test_whatif_focus_e2e.py — the What-if pages put the cursor in the
selection box the checked choice uses (Dates / Meal IDs, or Recipe IDs /
By date created), on load and when the choice is switched.

Docs: README-numa-documentation.md, Test Suite.
"""
import pytest

pytestmark = pytest.mark.e2e


def _focused_id(page) -> str:
    return page.evaluate("document.activeElement && document.activeElement.id")


def test_whatif_meals_focuses_the_checked_box(live_server, page):
    page.goto(f"{live_server}/analysis/whatif")
    assert _focused_id(page) == "ranges_raw"
    page.locator("#mode-ids").check()
    assert _focused_id(page) == "meal_ids"
    page.goto(f"{live_server}/analysis/whatif?mode=ids&meal_ids=12")
    assert _focused_id(page) == "meal_ids"
    assert page.evaluate("document.activeElement.selectionStart") == 2      # cursor at the end


def test_whatif_recipes_focuses_the_checked_box(live_server, page):
    page.goto(f"{live_server}/analysis/whatif-recipes?mode=ids")
    assert _focused_id(page) == "recipe_ids"
    page.locator("#mode-range").check()
    assert _focused_id(page) == "ranges_raw"
    page.locator("#mode-all").check()
    assert _focused_id(page) != "ranges_raw"
