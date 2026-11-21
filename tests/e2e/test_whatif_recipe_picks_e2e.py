"""
tests/e2e/test_whatif_recipe_picks_e2e.py — What-if: Recipes' pickers: "By
name" lists the recipes its words select as you type, and for Remove and
Change amount the "Food or recipe" box lists the chosen recipes' ingredients
when clicked (Add and Replace search every food instead).

The live server is a seeded fresh install (see conftest.py); its first starter
recipe has ingredients.

Docs: README-numa-documentation.md, Test Suite.
"""
import json
import re
import urllib.parse
import urllib.request

import pytest

pytestmark = pytest.mark.e2e


def _first_recipe(live_server) -> tuple[str, str]:
    html = urllib.request.urlopen(f"{live_server}/recipes", timeout=10).read().decode()
    rid = re.search(r'href="/recipe/(\d+)/edit"', html).group(1)
    data = json.loads(urllib.request.urlopen(
        f"{live_server}/analysis/whatif-recipes/name-matches?recipe_name=R{rid}", timeout=10).read())
    return rid, data["recipes"][0]["name"]


def test_by_name_preview_and_ingredient_list(live_server, page):
    rid, name = _first_recipe(live_server)
    page.goto(f"{live_server}/analysis/whatif-recipes")
    page.locator("#mode-name").check()
    page.locator("#recipe_name").fill(name)
    page.wait_for_selector("#name-matches a")
    assert "recipe(s) match" in page.locator("#name-matches").inner_text()
    assert name in page.locator("#name-matches").inner_text()

    # Remove (the default): clicking the box lists the chosen recipe's ingredients.
    row = page.locator(".whatif-row").first
    row.locator(".js-pick").first.click()
    results = row.locator(".js-pick-results").first
    results.locator("button").first.wait_for()
    assert "Ingredients of the" in results.inner_text()
    first = results.locator("button").first.inner_text()
    results.locator("button").first.click()
    picked = row.locator(".js-pick").first.input_value()
    assert re.match(r"[A-Z]+\d", picked) and first.startswith(picked)
    assert row.locator(".js-item-label").inner_text() == "Ingredient of the chosen recipes"

    # Add searches every food: an empty box opens no list.
    row.locator(".js-op").select_option("add")
    row.locator(".js-pick").first.fill("")
    row.locator(".js-pick").first.click()
    page.wait_for_timeout(300)
    assert results.locator("button").count() == 0
    assert row.locator(".js-item-label").inner_text() == "Food or recipe to add"
