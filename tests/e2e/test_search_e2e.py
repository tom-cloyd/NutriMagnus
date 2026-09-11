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
