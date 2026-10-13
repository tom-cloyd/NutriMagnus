"""
tests/e2e/test_manual_bookmarks_e2e.py — the user manual's bookmarks
(build_manual.JS's Bookmarks script): bookmark the section being read, the
drop-down list, the ★/☆ marks in the table of contents, removing one and
clearing all. All client-side JS over localStorage, so only a real browser
exercises it.

Docs: user-manual.md, Part 7 F "Bookmarking sections of this manual"
(#bookmarks-howto).
"""
import pytest

pytestmark = pytest.mark.e2e


def _goto(page, base, anchor, heading_words):
    """Open the manual at a section and wait until the scroll-spy has made
    it the section "Bookmark this section" would bookmark."""
    page.goto(f"{base}/manual#{anchor}")
    page.wait_for_function(
        "w => document.getElementById('bm-toggle').title.indexOf(w) !== -1", arg=heading_words
    )


def test_bookmark_list_toc_marks_remove_and_clear(live_server, page):
    page.goto(f"{live_server}/manual")
    page.evaluate("localStorage.clear()")

    _goto(page, live_server, "toc-howto", "Finding your way around")
    toggle = page.locator("#bm-toggle")
    assert toggle.inner_text() == "Bookmark this section"
    toggle.click()
    assert toggle.inner_text() == "Remove this bookmark"

    _goto(page, live_server, "search-howto", "search")
    page.locator("#bm-toggle").click()
    assert page.locator("#bm-count").inner_text() == "2"

    # ★ on the bookmarked entries, ☆ on the Part that holds them.
    assert page.locator('#toc-sidebar .toc a.toc-bookmarked').count() == 2
    assert page.locator('#toc-sidebar .toc a.toc-bookmark-inside').count() >= 1

    # Drop-down: closed until asked, manual order (D before E), then jump.
    menu = page.locator("#bm-menu")
    assert menu.is_hidden()
    page.locator("#bm-menu-btn").click()
    assert menu.is_visible()
    hrefs = page.locator("#bm-list a").evaluate_all("els => els.map(a => a.getAttribute('href'))")
    assert hrefs == ["#search-howto", "#toc-howto"]
    assert "Part 7" in page.locator("#bm-list a").first.inner_text()
    page.keyboard.press("Escape")
    assert menu.is_hidden()

    # Survives a reload.
    page.reload()
    assert page.locator("#bm-count").inner_text() == "2"

    # × removes just that one.
    page.locator("#bm-menu-btn").click()
    page.locator("#bm-list li").first.locator("button.bm-remove").click()
    assert page.locator("#bm-count").inner_text() == "1"
    assert page.locator("#bm-list a").get_attribute("href") == "#toc-howto"

    # Clear all asks first; dismissing keeps them.
    page.once("dialog", lambda d: d.dismiss())
    page.locator("#bm-clear-all").click()
    assert page.locator("#bm-count").inner_text() == "1"
    page.once("dialog", lambda d: d.accept())
    page.locator("#bm-clear-all").click()
    assert page.locator("#bm-count").inner_text() == "0"
    assert page.locator("#bm-empty").is_visible()
    assert page.locator('#toc-sidebar .toc a.toc-bookmarked').count() == 0


def test_bookmark_of_a_vanished_section_stays_listed(live_server, page):
    page.goto(f"{live_server}/manual")
    page.evaluate(
        "localStorage.setItem('numa_manual_bookmarks',"
        " JSON.stringify([{id: 'no-such-section', text: 'Old section'}]))"
    )
    page.reload()
    page.locator("#bm-menu-btn").click()
    assert "Old section (this section is no longer in the manual)" in page.locator("#bm-list").inner_text()
    page.locator("#bm-list button.bm-remove").click()
    assert page.locator("#bm-count").inner_text() == "0"
