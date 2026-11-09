"""
tests/e2e/test_portions_layout_e2e.py — browser-level coverage for a food's
Portions page: typing in a portion's Description box shows the row's
"Unsaved changes" note without resizing the box (the note's room is kept
from the start — .portions-table in style.css).

The live server is a seeded fresh install (see conftest.py); some starter
foods have portions.

Docs: README-numa-documentation.md, Test Suite.
"""
import re
import urllib.request

import pytest

pytestmark = pytest.mark.e2e


def _food_with_portions(base: str) -> str:
    html = urllib.request.urlopen(f"{base}/food/cache", timeout=10).read().decode()
    for fid in dict.fromkeys(re.findall(r'href="/food/cache/(-?\d+)/portions"', html)):
        page = urllib.request.urlopen(f"{base}/food/cache/{fid}/portions", timeout=10).read().decode()
        if 'form="edit-0"' in page:
            return fid
    pytest.skip("no starter food with portions")


_WIDTH = "() => document.querySelector('input[name=description][form=\"edit-0\"]').getBoundingClientRect().width"


def test_description_box_keeps_its_size_while_editing(live_server, page):
    fid = _food_with_portions(live_server)
    page.set_viewport_size({"width": 1280, "height": 900})
    page.goto(f"{live_server}/food/cache/{fid}/portions")
    before = page.evaluate(_WIDTH)
    box = page.locator('input[name=description][form="edit-0"]')
    box.click()
    box.press("End")
    box.type(" x")
    assert page.locator("#edit-0 .unsaved-badge").is_visible()
    assert abs(page.evaluate(_WIDTH) - before) < 1
