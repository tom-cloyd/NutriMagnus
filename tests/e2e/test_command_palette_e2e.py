"""
tests/e2e/test_command_palette_e2e.py — the command palette (base.html,
Alt+Shift+K or Ctrl+K): it lists every menu page with the keys that reach
it, read from the navbar; this page's own shortcuts; filters as you type;
runs a key command on the page underneath once it has closed; fits the
screen. All of it is JavaScript, so only a real browser exercises it.

Docs: README-numa-documentation.md, base.html → "Command palette";
user-manual.md, "B. Finding your way around" (#web-shortcuts)
"""
import pytest

pytestmark = pytest.mark.e2e


def _open(page, keys="Alt+Shift+K"):
    page.keyboard.press(keys)
    page.locator("#palette.show #palette-input").wait_for()
    page.wait_for_function("document.activeElement.id === 'palette-input'")


def _rows(page):
    return page.locator("#palette-results a.list-group-item").all_inner_texts()


def test_palette_lists_every_menu_page_with_its_keys(live_server, page):
    page.goto(f"{live_server}/food/search")
    _open(page)
    rows = _rows(page)
    menu = page.evaluate("""() => Array.from(document.querySelectorAll(
        '#main-nav .dropdown-item, #main-nav .nav-link[data-ak]:not(.dropdown-toggle)'))
        .map(a => a.getAttribute('href'))""")
    hrefs = page.evaluate("""() => Array.from(document.querySelectorAll(
        '#palette-results a.list-group-item')).map(a => a.getAttribute('href'))""")
    assert set(menu) <= set(hrefs)
    assert "Compare (Alt+Shift+C)" in rows
    assert any(r.startswith("Foods: Food Cache") and r.endswith("(Alt+Shift+F, then 5)") for r in rows)
    assert "Quit NuMa (Ctrl+Q)" in rows
    # This page's own shortcut (the food search box) comes first.
    assert rows[0] == "This page: Search box on this page (Alt+Shift+I)"


def test_filter_enter_navigates_and_typed_text_can_be_searched(live_server, page):
    page.goto(f"{live_server}/")
    _open(page, "Control+k")
    page.keyboard.type("food cache")
    rows = _rows(page)
    assert rows[0].startswith("Foods: Food Cache")
    assert 'Search foods for “food cache”' in rows
    page.keyboard.press("Enter")
    page.wait_for_url("**/food/cache")


def test_key_command_runs_on_the_page_once_closed(live_server, page):
    page.goto(f"{live_server}/settings")
    _open(page)
    page.keyboard.type("browser to launch")
    assert _rows(page)[0] == "This page: 13. Browser to Launch (Alt+Shift+B)"
    page.keyboard.press("Enter")
    page.wait_for_function("document.getElementById('browser-preference').open")
    assert not page.locator("#palette.show").count()


def test_settings_keyboard_section_moved_to_e(live_server, page):
    page.goto(f"{live_server}/settings")
    page.keyboard.press("Alt+Shift+E")
    page.wait_for_function(
        "document.querySelector('summary[data-ak=\"e\"]').parentElement.open")
    assert not page.locator("#palette.show").count()


def test_palette_fits_a_laptop_screen(live_server, page):
    page.set_viewport_size({"width": 1280, "height": 720})
    page.goto(f"{live_server}/")
    _open(page)
    bottom = page.evaluate(
        "document.querySelector('#palette .modal-content').getBoundingClientRect().bottom")
    scrolls = page.evaluate(
        "(b => b.scrollHeight > b.clientHeight + 1)(document.querySelector('#palette .modal-body'))")
    assert bottom <= 720 and not scrolls


def test_shortcuts_off_hides_hints_but_ctrl_k_still_opens(live_server, page):
    page.goto(f"{live_server}/")
    page.evaluate("localStorage.setItem('numa_accesskeys', 'false')")
    page.reload()
    page.keyboard.press("Alt+Shift+K")
    page.wait_for_timeout(300)
    assert not page.locator("#palette.show").count()
    _open(page, "Control+k")
    rows = _rows(page)
    assert "Compare" in rows and "Quit NuMa (Ctrl+Q)" in rows
    page.evaluate("localStorage.removeItem('numa_accesskeys')")
