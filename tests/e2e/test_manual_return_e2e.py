"""
tests/e2e/test_manual_return_e2e.py — the manual's "Return to …" button
(manual_frame.html): after several jumps inside the manual, one press of
Alt+Shift+U goes straight back to the NuMa page the manual was opened from,
and Manual in the menu then reopens the manual at the section last read.
The return target comes from document.referrer and the reading place from
localStorage, so only a real browser exercises it.

Docs: user-manual.md, "J. The Manual" (#manual-menu)
"""
import pytest

pytestmark = pytest.mark.e2e


def _frame(page):
    page.wait_for_selector("#manual-frame")
    frame = page.frame_locator("#manual-frame")
    frame.locator("#bm-toggle").wait_for()
    return page.frame(url=lambda u: "/manual/page" in u)


def test_return_skips_manual_jumps_and_manual_reopens_in_place(live_server, page):
    page.goto(f"{live_server}/meals")
    page.evaluate("localStorage.removeItem('numa_manual_last_section')")
    page.locator('nav.navbar a[data-section="manual"]').click()
    page.wait_for_url("**/manual")
    frame = _frame(page)

    assert page.locator("#manual-return-name").inner_text() == "Meals & Log"
    assert page.locator("#manual-return").get_attribute("href") == "/meals"

    # Several jumps inside the manual (each one a history step).
    for anchor in ("search-howto", "toc-howto", "bookmarks-howto"):
        frame.evaluate("a => { location.hash = a; }", anchor)
        page.wait_for_timeout(400)
    frame.wait_for_function(
        "localStorage.getItem('numa_manual_last_section') === 'bookmarks-howto'")

    # One keypress, straight back — not one step at a time.
    page.keyboard.press("Alt+Shift+U")
    page.wait_for_url("**/meals")

    # Manual in the menu reopens at the section last read.
    page.locator('nav.navbar a[data-section="manual"]').click()
    page.wait_for_url("**/manual")
    frame = _frame(page)
    frame.wait_for_function(
        "Math.abs(document.getElementById('bookmarks-howto').getBoundingClientRect().top) < 200")
