"""
tests/e2e/test_annotate_skip_e2e.py — browser-level coverage for the Annotate
page's Skip button beside the GI "Asking for this one" badge: when DIAAS is
asked for too, clicking it moves the cursor to the DIAAS box and scrolls it
into view, rather than leaving the page.

Docs: README-numa-documentation.md, Test Suite.
"""
import re
import urllib.request

import pytest

pytestmark = pytest.mark.e2e


def test_gi_skip_moves_to_the_diaas_box(live_server, page):
    html = urllib.request.urlopen(f"{live_server}/food/cache", timeout=10).read().decode()
    fid = re.search(r'href="/food/(-?\d+)"', html).group(1)
    page.set_viewport_size({"width": 1000, "height": 500})
    page.goto(f"{live_server}/food/annotate/{fid}?next=/pantry")
    skip = page.locator("#gi-skip-btn")
    if not skip.count():
        pytest.skip("this starter food already has a GI or DIAAS on file")
    label_top = lambda: page.evaluate(
        "document.getElementById('diaas-label').getBoundingClientRect().top")
    before = label_top()
    skip.click()
    assert page.url.endswith(f"/food/annotate/{fid}?next=/pantry")   # stayed put
    assert page.evaluate("document.activeElement.id") == "diaas_estimate"
    assert page.locator("#diaas_estimate").is_visible()
    # Bootstrap's smooth scrolling animates the move, so wait for it to land:
    # just below the sticky header (scroll-padding), not at the very top.
    page.wait_for_function(
        "document.getElementById('diaas-label').getBoundingClientRect().top < 120",
        timeout=5000)
    assert label_top() < before
