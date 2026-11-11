"""
tests/e2e/test_new_tab_notice_e2e.py — the new-tab notice in NuMa's own
window (base.html): a Ctrl+click on a NuMa link there first explains that
the page opens in a browser tab, Cancel keeps you put, Open it opens the
tab, "Don't show this again" turns the notice off, and an ordinary tab
never shows it. Client-side JS keyed on window.name, so only a real browser
exercises it.

Docs: user-manual.md, Part 3 B "Working in two windows" (#two-windows).
"""
import urllib.parse
import urllib.request

import pytest

pytestmark = pytest.mark.e2e

_LINK = 'a[href="/disclaimer"]'


def _set_notice(base: str, on: bool) -> None:
    body = urllib.parse.urlencode({"on": "1" if on else "0"}).encode()
    urllib.request.urlopen(urllib.request.Request(f"{base}/prefs/new-tab-notice", data=body))


def test_new_tab_notice_in_numa_window(live_server, page):
    _set_notice(live_server, True)
    try:
        # Arriving at the app window's start address names the window and
        # drops the marker from the address.
        page.goto(f"{live_server}/nutrimagnus-source")
        assert page.url == f"{live_server}/"
        assert page.evaluate("window.name") == "numa-app-window"

        dialog = page.locator("#new-tab-notice")
        context = page.context

        # Cancel: nothing opens, the page stays.
        page.locator(_LINK).first.click(modifiers=["Control"])
        assert dialog.is_visible()
        page.locator('#new-tab-notice [data-act="cancel"]').click()
        assert dialog.is_hidden()
        assert len(context.pages) == 1 and page.url == f"{live_server}/"

        # Open it: the page opens in a tab of its own, which is an ordinary
        # tab (not named), and this window stays where it was.
        page.locator(_LINK).first.click(modifiers=["Control"])
        with context.expect_page() as new:
            page.locator('#new-tab-notice [data-act="open"]').click()
        tab = new.value
        tab.wait_for_load_state()
        assert tab.url == f"{live_server}/disclaimer"
        assert tab.evaluate("window.name") != "numa-app-window"
        assert page.url == f"{live_server}/"

        # In that ordinary tab a Ctrl+click just opens another tab.
        tab.goto(f"{live_server}/")
        with context.expect_page() as other:
            tab.locator(_LINK).first.click(modifiers=["Control"])
        other.value.close()
        assert tab.locator("#new-tab-notice").count() == 0
        tab.close()

        # "Don't show this again": saved, and a reload of NuMa's window opens
        # the next Ctrl+click straight away.
        page.locator(_LINK).first.click(modifiers=["Control"])
        page.locator("#new-tab-notice-off").check()
        with context.expect_page() as new:
            page.locator('#new-tab-notice [data-act="open"]').click()
        new.value.close()
        page.reload()
        assert page.evaluate("window.name") == "numa-app-window"
        with context.expect_page() as new:
            page.locator(_LINK).first.click(modifiers=["Control"])
        new.value.close()
        assert page.locator("#new-tab-notice").count() == 0
    finally:
        _set_notice(live_server, True)
