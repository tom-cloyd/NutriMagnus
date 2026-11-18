"""
tests/e2e/test_go_to_id_e2e.py — opening a row of a list by its ID
(base.html, "Go to a row by its ID"): on a page whose rows carry data-go-id
(Recipes, Meals & Log, meal search), Alt+Shift+G starts "go to ID", the
digits typed next build an ID, and Enter opens that row. The key handling
is JavaScript, so only a real browser exercises it.

Docs: README-numa-documentation.md, "Keyboard shortcuts";
user-manual.md, "B. Finding your way around" (#go-to-id)
"""
import re
import urllib.request

import pytest

pytestmark = pytest.mark.e2e


def _type_id(page, digits, enter=True):
    page.keyboard.press("Alt+Shift+KeyG")
    for d in digits:
        page.keyboard.press(f"Digit{d}")
    if enter:
        page.keyboard.press("Enter")


def test_alt_shift_g_then_digits_and_enter_open_the_recipe_with_that_id(live_server, page):
    html = urllib.request.urlopen(f"{live_server}/recipes", timeout=10).read().decode()
    ids = re.findall(r'data-go-id="(\d+)"', html)
    assert ids, "Recipes list rows should carry data-go-id"
    rid = max(ids, key=len)  # prefer a multi-digit ID
    page.goto(f"{live_server}/recipes")
    _type_id(page, rid, enter=False)
    box = page.locator("#go-id-box")
    assert box.is_visible()
    assert box.inner_text().startswith(f"Go to ID {rid}: R{rid} ")
    page.keyboard.press("Enter")
    page.wait_for_url(f"**/recipe/{rid}")


def test_an_id_not_in_the_list_stays_put_and_says_so(live_server, page):
    page.goto(f"{live_server}/recipes")
    _type_id(page, "987654")
    box = page.locator("#go-id-box")
    assert box.inner_text() == "No ID 987654 in this list"
    assert page.url.endswith("/recipes")


def test_escape_cancels_go_to_id(live_server, page):
    page.goto(f"{live_server}/recipes")
    _type_id(page, "12", enter=False)
    page.keyboard.press("Escape")
    assert page.locator("#go-id-box").is_hidden()
    page.keyboard.press("Enter")
    assert page.url.endswith("/recipes")


def test_settings_digits_still_open_sections(live_server, page):
    """Settings has no ID list, so Alt+Shift+3 keeps opening section 3."""
    page.goto(f"{live_server}/settings")
    page.keyboard.press("Alt+Shift+Digit3")
    page.wait_for_function(
        "document.querySelector('summary[data-ak=\"3\"]').parentElement.open")
    assert page.locator("#go-id-box").count() == 0
