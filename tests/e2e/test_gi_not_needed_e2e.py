"""
tests/e2e/test_gi_not_needed_e2e.py — browser-level coverage for Foods → 9's
"Foods you use with no GI" list: the reminder beside "Also list foods for
which the GI is marked 'not needed'" turns into a warning once a box is
changed, that button offers to save the change before reloading, and
leaving by a link asks first (base.html's data-leave-guard).

The live server is a seeded fresh install (see conftest.py); the test marks
one starter food's GI not needed over plain HTTP first, so the longer list
has a row to work with whatever the starter data holds.

Docs: README-numa-documentation.md, Test Suite.
"""
import re
import urllib.parse
import urllib.request

import pytest

pytestmark = pytest.mark.e2e


def _post(url: str, data: dict) -> None:
    body = urllib.parse.urlencode(data).encode()
    urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=10)


def test_gi_not_needed_reminder_and_save_before_leaving(live_server, page):
    html = urllib.request.urlopen(f"{live_server}/food/cache", timeout=10).read().decode()
    fid = re.search(r'href="/food/(-?\d+)"', html).group(1)
    _post(f"{live_server}/food/cache/db-check/completeness",
          {"shown": f"{fid}:gi", "ignore": f"{fid}:gi", "back": "missing-gi"})

    page.goto(f"{live_server}/food/cache/db-check?gi_show_ignored=true#missing-gi")
    note = page.locator("#missing-gi-save-reminder")
    assert "Ticked or unticked" in note.inner_text()
    box = page.locator(f'#missing-gi-form input[name=ignore][value="{fid}:gi"]')
    assert box.is_checked()

    box.uncheck()
    assert "1 “not needed” change is not saved yet" in note.inner_text()
    assert "text-danger" in (note.get_attribute("class") or "")

    # Leaving by a link asks to save first; Cancel to both questions stays put.
    seen, answer = [], {"accept": False}

    def on_dialog(d):
        seen.append(d.message)
        d.accept() if answer["accept"] else d.dismiss()
    page.on("dialog", on_dialog)
    page.locator(f'#missing-gi-form a[href="/food/{fid}"]').click()
    assert seen and "Save those changes before leaving" in seen[0]
    assert "db-check" in page.url and not box.is_checked()

    # The list button offers to save first; OK saves, then reloads the list.
    seen.clear()
    answer["accept"] = True
    with page.expect_navigation():
        page.locator("#gi-show-ignored-form button").click()
    assert seen and "not saved yet" in seen[0]
    assert "gi_show_ignored=false" in page.url
    page.goto(f"{live_server}/food/cache/db-check?gi_show_ignored=true#missing-gi")
    # Saved: the food is no longer marked (it may still be listed, unticked,
    # if it is used and has carbohydrate but no GI).
    after = page.locator(f'#missing-gi-form input[name=ignore][value="{fid}:gi"]')
    assert after.count() == 0 or not after.is_checked()


def test_amino_acid_and_portion_lists_have_the_same_reminder(live_server, page):
    page.goto(f"{live_server}/food/cache/db-check?show_ignored=true")
    page.evaluate("document.querySelectorAll('#missing-aa, #missing-portions').forEach(d => d.open = true)")
    forms = [sid for sid in ("missing-aa", "missing-portions") if page.locator(f"#{sid}-form").count()]
    assert forms, "starter data gave neither list a row to test with"
    for sid in forms:
        note = page.locator(f"#{sid}-save-reminder")
        assert "Ticked or unticked" in note.inner_text()
        assert note.locator(f'a[href="#{sid}-save-btn"]').count() == 1
        box = page.locator(f"#{sid}-form input[name=ignore]").first
        box.set_checked(not box.is_checked())
        assert "1 “not needed” change is not saved yet" in note.inner_text()
        box.set_checked(not box.is_checked())
        assert "Ticked or unticked" in note.inner_text()
    if "missing-portions" in forms and page.locator(".js-check-all-not-needed").count():
        boxes = page.locator("#missing-portions-form input[name=ignore]")
        unticked = sum(1 for i in range(boxes.count()) if not boxes.nth(i).is_checked())
        page.locator(".js-check-all-not-needed").click()
        n = unticked or boxes.count()   # all ticked already: the button unticks them all
        assert f"{n} “not needed” change" in page.locator("#missing-portions-save-reminder").inner_text()


def test_annotate_save_button_lights_up_on_a_dont_prompt_box(live_server, page):
    html = urllib.request.urlopen(f"{live_server}/food/cache", timeout=10).read().decode()
    fid = re.search(r'href="/food/(-?\d+)"', html).group(1)
    page.goto(f"{live_server}/food/annotate/{fid}")
    btn = page.locator("#save-annotation-btn")
    assert "btn-dirty" not in (btn.get_attribute("class") or "")
    for box_id in ("#diaas_no_prompt", "#gi_no_prompt"):
        box = page.locator(box_id)
        box.set_checked(not box.is_checked())
        assert "btn-dirty" in btn.get_attribute("class")
        box.set_checked(not box.is_checked())
        assert "btn-dirty" not in btn.get_attribute("class")
    assert page.evaluate("getComputedStyle(document.querySelector('#save-annotation-btn')).fontWeight") != "700"
    page.locator("#gi_no_prompt").set_checked(not page.locator("#gi_no_prompt").is_checked())
    page.wait_for_timeout(500)   # Bootstrap animates a button's colors
    style = page.evaluate("(() => { const s = getComputedStyle(document.querySelector('#save-annotation-btn'));"
                          " return [s.backgroundColor, s.color, s.fontWeight]; })()")
    assert style == ["rgb(13, 110, 253)", "rgb(255, 255, 255)", "700"]
