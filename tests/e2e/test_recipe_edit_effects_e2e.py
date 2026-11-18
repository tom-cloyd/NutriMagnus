"""
tests/e2e/test_recipe_edit_effects_e2e.py — browser-level coverage for the
recipe Edit page's change-effect reports and its food-details panel: the
offer after a change, writing a report, the Show button, and a food's page
opening over the Edit page (navbar hidden) and closing back to it.

The live server is a seeded fresh install (see conftest.py); its first starter
recipe has ingredients.

Docs: README-numa-documentation.md, Test Suite.
"""
import re
import urllib.request

import pytest

pytestmark = pytest.mark.e2e


def _first_recipe(live_server) -> str:
    html = urllib.request.urlopen(f"{live_server}/recipes", timeout=10).read().decode()
    return re.search(r'href="/recipe/(\d+)/edit"', html).group(1)


def test_change_offer_report_and_show(live_server, page):
    rid = _first_recipe(live_server)
    page.goto(f"{live_server}/recipe/{rid}")
    page.goto(f"{live_server}/recipe/{rid}/edit")
    assert page.locator("#effects-offer").count() == 0
    assert page.locator("#effects-file").is_hidden()

    page.locator("#sec-ingredients button[aria-label=Remove]").last.click()
    page.wait_for_load_state("load")
    offer = page.locator("#effects-offer")
    assert offer.is_visible() and "Removed" in offer.inner_text()

    offer.locator("[data-effects=yes]").click()
    page.locator("#effects-all").check()
    assert page.locator("[data-effects-group]").first.is_disabled()
    page.locator("#effects-all5").check()
    assert not page.locator("#effects-all").is_checked()
    offer.locator("button[type=submit]").click()
    # The box says the report is written and shows it from there.
    offer.locator("[data-effects=show]").click()
    page.wait_for_selector("#effects-offer", state="detached")
    page.wait_for_selector("#effects-content h2")
    assert "Report 1" in page.locator("#effects-content").inner_text()
    assert page.locator("#effects-path").inner_text().endswith("recipe-edit-effects-data.md")
    assert page.locator("#effects-file").is_visible()

    # The button above Add Ingredient hides and shows it again.
    page.locator("#effects-show-btn").click()
    assert page.locator("#effects-panel").is_hidden()
    page.locator("#effects-show-btn").click()
    assert page.locator("#effects-panel").is_visible()


def test_food_name_opens_in_a_panel_over_the_page(live_server, page):
    rid = _first_recipe(live_server)
    page.goto(f"{live_server}/recipe/{rid}/edit")
    page.locator("#name").fill("Unsaved name")
    link = page.locator('#sec-ingredients a[href^="/food/"]').first
    link.click()
    dlg = page.locator("#details-overlay")
    assert dlg.is_visible()
    frame = page.frame_locator("#details-overlay-frame")
    frame.locator("body").wait_for()
    assert frame.locator("#main-navbar").is_hidden()
    page.locator("#details-overlay-close").click()
    assert dlg.is_hidden()
    assert page.url.endswith(f"/recipe/{rid}/edit")
    assert page.locator("#name").input_value() == "Unsaved name"


def test_esc_closes_the_change_box(live_server, page):
    rid = _first_recipe(live_server)
    page.goto(f"{live_server}/recipe/{rid}")
    page.goto(f"{live_server}/recipe/{rid}/edit")
    page.locator("#sec-ingredients button[aria-label=Remove]").last.click()
    page.wait_for_load_state("load")
    assert "(Esc)" in page.locator("#effects-offer [data-effects=no]").first.inner_text()
    page.keyboard.press("Escape")
    assert page.locator("#effects-offer").count() == 0
