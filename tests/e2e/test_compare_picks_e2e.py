"""
tests/e2e/test_compare_picks_e2e.py — Compare picks carried across searches
and lists (base.html's "Compare picks" script): a tick in one search's
Compare column survives a new search and a move to another list, the note
under the Compare button lists every pick, and the Compare button sends
them all — and they are still picked on coming back.

Uses the demo data seeded on a fresh install (demo_data.py): the foods
"Quinoa, cooked" and "Onions, raw" and the recipe "Walnut milk".

Docs: README-numa-documentation.md → Test Suite → Browser-level end-to-end tests.
"""
import re

import pytest

pytestmark = pytest.mark.e2e


def _tick_first(page, table_sel, text):
    row = page.locator(f"{table_sel} tr", has_text=text).first
    row.locator("input[type=checkbox][form]").last.check()


def test_picks_survive_searches_and_lists_then_all_go_to_compare(live_server, page):
    page.goto(f"{live_server}/food/search?query=Quinoa")
    page.wait_for_selector("#search-tbody >> text=Quinoa")
    _tick_first(page, "#search-tbody", "Quinoa, cooked")
    note = page.locator('[data-compare-picks-for="compare-form"]')
    assert "Picked for comparison (1 of 8)" in note.inner_text()

    # A new search: the earlier pick is still listed.
    page.goto(f"{live_server}/food/search?query=Onions")
    page.wait_for_selector("#search-tbody >> text=Onions")
    assert "Quinoa, cooked" in note.inner_text()
    _tick_first(page, "#search-tbody", "Onions, raw")

    # Another list (Recipes): both picks listed; tick a recipe too.
    page.goto(f"{live_server}/recipes")
    recipes_note = page.locator('[data-compare-picks-for="compare-recipe-form"]')
    text = recipes_note.inner_text()
    assert "Picked for comparison (2 of 8)" in text
    assert "Quinoa" in text and "Onions" in text
    page.locator("tr", has_text="Walnut milk").first.locator(
        'input[form="compare-recipe-form"]').check()

    page.click('button[form="compare-recipe-form"]')
    page.wait_for_url(re.compile(r"/compare\?items="))
    items = re.search(r"items=([^&]+)", page.url).group(1)
    assert len(items.replace("%2C", ",").split(",")) == 3
    # The picks are kept after comparing: back on the list, still ticked.
    page.go_back()
    page.wait_for_url(re.compile(r"/recipes"))
    assert "Picked for comparison (3 of 8)" in recipes_note.inner_text()
    assert page.locator("tr", has_text="Walnut milk").first.locator(
        'input[form="compare-recipe-form"]').is_checked()


def test_unpicking_from_the_note_unticks_the_box(live_server, page):
    page.goto(f"{live_server}/food/search?query=Quinoa")
    page.wait_for_selector("#search-tbody >> text=Quinoa")
    _tick_first(page, "#search-tbody", "Quinoa, cooked")
    page.click("[data-compare-unpick]")
    note = page.locator('[data-compare-picks-for="compare-form"]')
    assert "Ticks are kept when you search again" in note.inner_text()
    assert page.locator('#search-tbody input[form="compare-form"]:checked').count() == 0


def test_food_cache_pantry_and_compare_show_the_picks(live_server, page):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"{live_server}/food/cache")
    page.locator('tr', has_text="Quinoa, cooked").first.locator(
        'input[form="compare-form"]').check()
    for url, form_id in ((f"{live_server}/pantry?search=Onions", "compare-search-form"),
                         (f"{live_server}/compare?search=Onions", "compare-add-form"),
                         (f"{live_server}/food/cache", "compare-form")):
        page.goto(url)
        note = page.locator(f'[data-compare-picks-for="{form_id}"]')
        note.wait_for()
        assert "Quinoa, cooked" in note.inner_text(), url
    # The box on the page where it was ticked is still ticked.
    assert page.locator('tr', has_text="Quinoa, cooked").first.locator(
        'input[form="compare-form"]').is_checked()
    assert not errors


def test_custom_profile_edit_keeps_its_own_picks(live_server, page):
    # A draft copy of a demo food gives a custom profile to edit.
    page.goto(f"{live_server}/food/search?query=Quinoa")
    page.wait_for_selector("#search-tbody >> text=Quinoa")
    page.locator("#search-tbody tr", has_text="Quinoa, cooked").first.locator(
        "text=Copy as custom-food draft").click()
    page.wait_for_url(re.compile(r"/food/custom-profiles/-?\d+/edit"))
    edit_url = page.url.split("#")[0].split("?")[0]

    page.goto(f"{edit_url}?nutrient_source_q=Onions")
    page.locator('input[name="pick"][form="compare-nutrient-picks"]').first.check()
    page.goto(f"{edit_url}?nutrient_source_q=Chickpeas")
    note = page.locator('[data-compare-picks-for="compare-nutrient-picks"]')
    assert "Onions" in note.inner_text()
    page.locator('input[name="pick"][form="compare-nutrient-picks"]').first.check()
    # The general picks list is untouched by these.
    assert page.evaluate("sessionStorage.getItem('numa_compare_picks')") is None

    page.click('#compare-nutrient-picks button[type="submit"]')
    page.wait_for_url(re.compile(r"/compare\?items="))
    items = re.search(r"items=([^&]+)", page.url).group(1)
    assert len(items.replace("%2C", ",").split(",")) == 3


def test_fill_from_page_keeps_picks_across_searches(live_server, page):
    page.goto(f"{live_server}/food/search?query=Quinoa")
    page.wait_for_selector("#search-tbody >> text=Quinoa")
    fdc_id = page.locator("#search-tbody tr", has_text="Quinoa, cooked").first.locator(
        'input[form="compare-form"]').get_attribute("value")
    page.goto(f"{live_server}/food/{fdc_id}/fill-from?q=Onions")
    button = page.locator('#fill-compare-picks button[type="submit"]')
    assert "btn-outline-secondary" in button.get_attribute("class")
    page.locator('input[name="pick"][form="fill-compare-picks"]').first.check()
    # One pick is enough beside this page's own food: the button turns blue.
    assert "btn-primary" in button.get_attribute("class")
    page.goto(f"{live_server}/food/{fdc_id}/fill-from?q=Chickpeas")
    note = page.locator('[data-compare-picks-for="fill-compare-picks"]')
    assert "Onions" in note.inner_text()
    page.locator('input[name="pick"][form="fill-compare-picks"]').first.check()
    page.click('#fill-compare-picks button[type="submit"]')
    page.wait_for_url(re.compile(r"/compare\?items="))
    items = re.search(r"items=([^&]+)", page.url).group(1)
    assert len(items.replace("%2C", ",").split(",")) == 3
    # Back on the page, the ticks are still there, and the button still blue.
    page.go_back()
    page.wait_for_url(re.compile(r"/fill-from\?q=Chickpeas"))
    assert page.locator('input[name="pick"][form="fill-compare-picks"]').first.is_checked()
    assert "Onions" in page.locator('[data-compare-picks-for="fill-compare-picks"]').inner_text()
    assert "btn-primary" in page.locator('#fill-compare-picks button[type="submit"]').get_attribute("class")
