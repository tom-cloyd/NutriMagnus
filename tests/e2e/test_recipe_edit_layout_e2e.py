"""
tests/e2e/test_recipe_edit_layout_e2e.py — browser-level coverage for the
Edit Recipe page's top section: the Introduction, Instructions and Notes boxes
are fitted so they end level with Running totals, at any window width, which
leaves both columns the same distance above Add Ingredient.

The live server is a seeded fresh install (see conftest.py); its first starter
recipe has ingredients, so it shows a Running totals card.

Docs: README-numa-documentation.md, Test Suite.
"""
import re
import urllib.request

import pytest

pytestmark = pytest.mark.e2e

_BOTTOMS = """() => [
  document.getElementById('notes').getBoundingClientRect().bottom,
  document.getElementById('recipe-running-totals').getBoundingClientRect().bottom,
]"""


@pytest.mark.parametrize("width", [1000, 1280, 1440, 1920])
def test_notes_box_ends_level_with_running_totals(live_server, page, width):
    html = urllib.request.urlopen(f"{live_server}/recipes", timeout=10).read().decode()
    rid = re.search(r'href="/recipe/(\d+)/edit"', html).group(1)
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(f"{live_server}/recipe/{rid}/edit")
    notes, card = page.evaluate(_BOTTOMS)
    assert abs(notes - card) < 1.5

    # Refits when the window changes.
    page.set_viewport_size({"width": width + 150, "height": 900})
    page.wait_for_timeout(100)
    notes, card = page.evaluate(_BOTTOMS)
    assert abs(notes - card) < 1.5


def test_stacked_layout_keeps_full_size_boxes(live_server, page):
    html = urllib.request.urlopen(f"{live_server}/recipes", timeout=10).read().decode()
    rid = re.search(r'href="/recipe/(\d+)/edit"', html).group(1)
    page.set_viewport_size({"width": 800, "height": 900})
    page.goto(f"{live_server}/recipe/{rid}/edit")
    assert page.evaluate("document.getElementById('notes').style.height") == ""
