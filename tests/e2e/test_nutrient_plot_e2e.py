"""
tests/e2e/test_nutrient_plot_e2e.py — browser-level coverage for the
Nutrient Plot page's instant Legend placement change: it redraws the plot
without a Plot click, updates the address bar so a reload keeps it, and,
while the plot is on the Home page, saves it there too.

The live server is a seeded fresh install (see conftest.py); the test logs
one meal for today over plain HTTP so there is something to plot.

Docs: README-numa-documentation.md, Test Suite.
"""
import datetime
import re
import urllib.parse
import urllib.request

import pytest

pytestmark = pytest.mark.e2e


def _post(url: str, data: dict) -> str:
    body = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=10) as r:
        return r.geturl()


def test_legend_change_reaches_address_bar_and_home_page(live_server, page):
    html = urllib.request.urlopen(f"{live_server}/food/cache", timeout=10).read().decode()
    fid = re.search(r'href="/food/(-?\d+)"', html).group(1)
    meal_url = _post(f"{live_server}/meals/create",
                     {"name": "Plot meal", "meal_date": datetime.date.today().isoformat()})
    meal_id = re.search(r"/meal/(\d+)", meal_url).group(1)
    _post(f"{live_server}/meal/{meal_id}/add", {"fdc_id": fid, "food_name": "x", "portion_str": "100 g"})

    page.goto(f"{live_server}/summary/nutrient-plot?submitted=1&nutrients=calories&nutrients=protein_g")
    with page.expect_navigation():
        page.locator("#home-plot-toggle").check()
    assert page.locator("#home-plot-toggle").is_checked()

    with page.expect_response(lambda r: "/summary/nutrient-plot/home-pref" in r.url):
        page.locator("#legend").select_option("right")
    assert "legend=right" in page.url
    assert "legend=right" in (page.locator("#plot-src-wide").get_attribute("srcset") or "")
    img_src = page.locator("#plot-img").get_attribute("src") or ""
    assert "legend=right" in img_src and "narrow=1" in img_src

    home = urllib.request.urlopen(f"{live_server}/", timeout=10).read().decode()
    assert "legend=right" in home
