"""
tests/e2e/test_search_e2e.py — browser-level coverage for the JS async
handoff pattern used by /food/search, /food/analyze-portion, and a meal's
Add Food panel: the page renders local (cache-only) results first, then JS
fetches the merged local+external result set and replaces the table body
with it. Existing behavioral tests (tests/test_web.py) only confirm the
HTML contains the right fetch() call — these confirm the JS actually runs
and updates the DOM.

External sources are stubbed to return [] (see conftest.py's live_server /
_run_isolated_server.py), so the merged result set these tests see is just
the local demo data seeded on a fresh install (demo_data.py) — "Chickpeas"
is one of those seeded foods.

Docs: TESTING-ROADMAP.md, item #4.
"""
import pytest

pytestmark = pytest.mark.e2e


def test_food_search_fetch_replaces_table_with_merged_results(live_server, page):
    # The initial GET already renders local matches server-side (see
    # _search_logic()'s comment on why: instant local-only response, no
    # network stall) — so "Chickpeas" alone appearing in #search-tbody
    # proves nothing about the JS. What's actually new here vs. the existing
    # HTML-only tests is confirming the browser really issues the
    # /food/search-api-results fetch and gets a real response back —
    # page.expect_response fails the test outright if that never happens.
    with page.expect_response(lambda r: "/food/search-api-results" in r.url) as resp_info:
        page.goto(f"{live_server}/food/search?query=Chickpeas")
    response = resp_info.value
    assert response.status == 200
    assert "Chickpeas" in response.text()

    # Once that response lands, JS replaces #search-tbody's innerHTML
    # wholesale with it — confirm the DOM actually reflects it.
    page.wait_for_selector("#search-tbody >> text=Chickpeas", timeout=10_000)
    assert page.query_selector("#search-api-loading") is None


def test_analyze_portion_fetch_replaces_table_with_merged_results(live_server, page):
    # Unlike /food/search, GET /food/analyze-portion takes no query string —
    # only the POST form does (food_analyze_portion_get() always renders an
    # empty query) — so drive the search box directly instead. The POST
    # response itself already renders local matches synchronously (same
    # _search_logic() as above), so again the fetch response is what proves
    # the JS actually ran, not the presence of "Chickpeas" alone.
    page.goto(f"{live_server}/food/analyze-portion")
    with page.expect_response(lambda r: "/food/analyze-portion-api-results" in r.url) as resp_info:
        page.fill("input[name=query]", "Chickpeas")
        page.click("button[type=submit]")
    response = resp_info.value
    assert response.status == 200
    assert "Chickpeas" in response.text()

    page.wait_for_selector("#ap-tbody >> text=Chickpeas", timeout=10_000)
    assert page.query_selector("#ap-api-loading") is None


def test_meal_add_food_fetch_replaces_table_with_merged_results(live_server, page):
    # This route needs an actual meal to attach the search to — create one
    # via a real POST, the same way a user would from the Meals & Log page,
    # then read the meal id back off the post-create redirect target
    # (/meals/create redirects to /meal/{meal_id}).
    create_resp = page.request.post(
        f"{live_server}/meals/create",
        form={"name": "E2E Test Meal", "meal_date": "2026-01-01"},
    )
    assert create_resp.ok
    meal_id = create_resp.url.rstrip("/").rsplit("/", 1)[-1]
    assert meal_id.isdigit()

    page.goto(f"{live_server}/meal/{meal_id}")
    with page.expect_response(lambda r: f"/meal/{meal_id}/search-api-results" in r.url) as resp_info:
        page.fill("input[name=q]", "Chickpeas")
        # #add-food-details' form has two submit buttons ("Search" and,
        # once results exist, "Redo search") — match "Search" exactly so
        # this doesn't become ambiguous once the page has results.
        page.click('#add-food-details >> text="Search"')
    response = resp_info.value
    assert response.status == 200
    assert "Chickpeas" in response.text()

    page.wait_for_selector("#add-food-tbody >> text=Chickpeas", timeout=10_000)
    assert page.query_selector("#add-food-api-loading") is None


def test_gi_lookup_row_click_fills_the_gi_field(live_server, page):
    """Regression: only the "Use" button carried a click handler, so clicking
    the food name — the obvious thing to try — did nothing at all, with no
    visible response of any kind."""
    page.goto(f"{live_server}/food/annotate?q=Chickpeas")
    page.click("a.btn:has-text('Edit')")
    page.click("#gi-lookup-details summary")
    page.fill("#gi-lookup-query", "Chickpeas")
    with page.expect_response(lambda r: "/gi-lookup?" in r.url):
        page.click("#gi-lookup-search")
    page.wait_for_selector(".gi-pick-row", timeout=10_000)

    row = page.query_selector(".gi-pick-row")
    expected = row.get_attribute("data-gi")
    # Click the name cell, not the button.
    row.query_selector("td").click()

    assert page.input_value("#gi_estimate") == expected
    # The list of matches goes away and the panel closes, so the filled GI box
    # and the Save button are what's left on screen — a note at the foot of a
    # long result list would just be scrolled past.
    assert page.query_selector(".gi-pick-row") is None
    assert page.eval_on_selector("#gi-lookup-details", "el => el.open") is False
    # The value is only in the form at this point, so Save has to be unmissable.
    save = page.query_selector("#save-annotation-btn")
    assert "btn-save-pending" in save.get_attribute("class")
    assert page.evaluate("document.activeElement.id") == "save-annotation-btn"


def test_meal_item_submits_save_the_scroll_offset(live_server, page):
    """Editing/adding/removing a meal item posts and redirects back to the same
    page — a fresh navigation, which the browser scrolls to the top. meal.html
    saves the offset in sessionStorage just before those submits and restores
    it on the way back.

    What is checked here is the save half, and specifically the action-URL test
    that gates it: that regex is the part that silently stops matching when a
    route is renamed or added, and nothing else would notice. Restoring is one
    scrollTo on the next load. Deliberately not asserting a pixel offset after
    a real round trip: page height, viewport and the add-panel's own autofocus
    all move that number around, and a test tuned to them would break for
    reasons that have nothing to do with this feature."""
    resp = page.request.post(f"{live_server}/meals/create",
                             form={"name": "Scroll Test Meal", "meal_date": "2026-09-23"})
    assert resp.ok
    meal_url = resp.url
    meal_id = meal_url.rstrip("/").split("/")[-1]

    page.goto(f"{meal_url}?q=Chickpeas")
    page.wait_for_selector("input[name=portion_str]")   # visible; fdc_id beside it is hidden
    add = page.request.post(
        f"{live_server}/meal/{meal_id}/add",
        form={"fdc_id": page.get_attribute("input[name=fdc_id]", "value"),
              "food_name": page.get_attribute("input[name=food_name]", "value"),
              "off_code": "", "q": "", "portion_str": "100"})
    assert add.ok

    page.goto(f"{meal_url}?q=")
    page.wait_for_selector("details.popup-edit")
    key = f"numa-meal-scroll-{meal_id}"
    assert page.evaluate(f"sessionStorage.getItem('{key}')") is None

    # A bubbling submit event runs the page's listener without navigating, so
    # this observes exactly what the listener does with this form's action.
    saved = page.evaluate("""() => {
        window.scrollTo(0, 120);
        // By action, not position: the first popup-edit form on the page is
        // Rename / change date, which correctly does NOT save an offset.
        const form = document.querySelector("form[action*='/update/']");
        form.dispatchEvent(new Event('submit', {bubbles: true, cancelable: true}));
        return sessionStorage.getItem('numa-meal-scroll-""" + meal_id + """');
    }""")
    assert saved is not None, (
        "submitting a meal item's edit form no longer matches the action-URL "
        "test in meal.html's scroll-restore script"
    )

    # And a form that does not change the item list must NOT hijack the offset.
    page.goto(f"{meal_url}?q=")
    ignored = page.evaluate("""() => {
        sessionStorage.clear();
        const f = document.createElement('form');
        f.setAttribute('action', '/settings');
        document.body.appendChild(f);
        f.dispatchEvent(new Event('submit', {bubbles: true, cancelable: true}));
        return sessionStorage.length;
    }""")
    assert ignored == 0
