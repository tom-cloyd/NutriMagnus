"""The recipe Edit page's "effect of this change" reports
(numa_app/services/recipe_edit_effects.py and its routes in web/backend.py)."""
import re

from fastapi.testclient import TestClient

import web.backend as backend
from numa_app.services import recipe_edit_effects as _effects


def _client() -> TestClient:
    return TestClient(backend.app)


def _new_recipe(client, servings=2) -> int:
    resp = client.post("/recipe/new", data={"name": "Effects Soup", "servings": servings}, follow_redirects=False)
    return int(resp.headers["location"].split("/recipe/")[1].split("/")[0])


def _edit_page(client, rid, *, from_page=None):
    """The Edit page, arriving from from_page (default: the page itself, as
    after an add or remove)."""
    return client.get(f"/recipe/{rid}/edit",
                      headers={"referer": from_page or f"http://testserver/recipe/{rid}/edit"})


def _add(client, rid, food, amount="100 g"):
    resp = client.post(f"/recipe/{rid}/ingredient/add",
                       data={"fdc_id": food["fdcId"], "food_name": food["name"], "portion_str": amount},
                       follow_redirects=False)
    assert resp.status_code == 303


def _ingredient_ids(db_conn, rid):
    return [r["id"] for r in db_conn.execute(
        "SELECT id FROM recipe_ingredients WHERE recipe_id = ? ORDER BY id", (rid,))]


def _report(client, rid, *choices):
    return client.post(f"/recipe/{rid}/edit-effects/report", data={"choice": list(choices)}).json()


def test_a_change_offers_a_report_once_and_writes_it(cached_food) -> None:
    client = _client()
    rid = _new_recipe(client)
    page = _edit_page(client, rid, from_page="http://testserver/recipes").text
    assert 'id="effects-offer"' not in page
    assert 'id="effects-file" class="mt-3" hidden' in page

    _add(client, rid, cached_food, "200 g")
    page = _edit_page(client, rid).text
    assert 'id="effects-offer"' in page and "Added " + cached_food["name"] in page
    # Shown once: ignoring it is the same as No.
    assert 'id="effects-offer"' not in _edit_page(client, rid).text

    d = _report(client, rid, "Macronutrients")
    assert d["ok"], d
    text = _effects.read_file()
    assert text.startswith("# Recipe edit effects: Effects Soup")
    assert "## Report 1" in text and "Added " + cached_food["name"] in text
    assert re.search(r"\| Calories \(kcal\) \| 0(\.0+)? \| \d", text) and "### Macronutrients" in text
    assert "### Minerals" not in text
    page = _edit_page(client, rid).text
    assert 'id="effects-file" class="mt-3">' in page    # the Show button stays


def test_an_exchange_is_one_report_and_the_next_report_appends(cached_food, db_conn) -> None:
    client = _client()
    rid = _new_recipe(client)
    _edit_page(client, rid, from_page="http://testserver/recipes")
    _add(client, rid, cached_food, "100 g")
    assert _report(client, rid, _effects.ALL)["ok"]

    # Remove it (no report), then add it back at 150 g: one report, both changes.
    client.post(f"/recipe/{rid}/ingredient/{_ingredient_ids(db_conn, rid)[0]}/remove", follow_redirects=False)
    _add(client, rid, cached_food, "150 g")
    page = _edit_page(client, rid).text
    assert "Changes since the last report:" in page
    assert _report(client, rid, _effects.ALL)["ok"]
    text = _effects.read_file()
    report2 = text.split("## Report 2")[1]
    assert "## Report 1" in text
    assert "1. Removed " + cached_food["name"] in report2
    assert "2. Added " + cached_food["name"] in report2
    assert "+50.0%" in report2      # 100 g before, 150 g after
    # A column per step: before, after the removal (nothing), after the add.
    assert "| Nutrient | Before | After 1 | After 2 | Change | Change % |" in report2
    assert "| Total Fat (g) | 1.80 | 0.00 | 2.70 | +0.90 | +50.0% |" in report2, report2

    # Nothing changed since: nothing to report.
    d = _report(client, rid, _effects.ALL)
    assert not d["ok"] and "no change" in d["error"]


def test_a_new_session_replaces_the_file_at_its_first_report(cached_food) -> None:
    client = _client()
    rid = _new_recipe(client)
    _edit_page(client, rid, from_page="http://testserver/recipes")
    _add(client, rid, cached_food)
    _report(client, rid, "Minerals")
    assert "## Report 1" in _effects.read_file()

    # Arriving from another page starts a new session: the remembered
    # choice is gone, and the old file stays until the new session reports.
    page = _edit_page(client, rid, from_page=f"http://testserver/recipe/{rid}").text
    assert 'id="effects-file" class="mt-3" hidden' in page
    assert "## Report 1" in _effects.read_file()
    _add(client, rid, cached_food, "50 g")
    page = _edit_page(client, rid).text
    i = page.index('value="Minerals"')
    assert "checked" not in page[i:i + 160]
    _report(client, rid, "Vitamins")
    text = _effects.read_file()
    assert text.count("## Report") == 1 and "### Minerals" not in text

    # Within a session the choice is remembered for the next offer.
    _add(client, rid, cached_food, "10 g")
    page = _edit_page(client, rid).text
    i = page.index('value="Vitamins"')
    assert "checked" in page[i:i + 160]


def test_amount_edits_offer_a_report_but_name_edits_dont(cached_food, db_conn) -> None:
    client = _client()
    rid = _new_recipe(client)
    _edit_page(client, rid, from_page="http://testserver/recipes")
    _add(client, rid, cached_food, "100 g")
    _edit_page(client, rid)     # the add's offer, not taken
    ing = _ingredient_ids(db_conn, rid)[0]
    client.post(f"/recipe/{rid}/ingredient/{ing}/edit",
                data={"portion_str": "100 g", "food_name": "Renamed"}, follow_redirects=False)
    assert 'id="effects-offer"' not in _edit_page(client, rid).text
    client.post(f"/recipe/{rid}/ingredient/{ing}/edit",
                data={"portion_str": "120 g", "food_name": "Renamed"}, follow_redirects=False)
    page = _edit_page(client, rid).text
    assert "Changed Renamed from 100" in page and "to 120" in page


def test_a_report_needs_a_choice(cached_food) -> None:
    client = _client()
    rid = _new_recipe(client)
    _edit_page(client, rid, from_page="http://testserver/recipes")
    _add(client, rid, cached_food)
    d = _report(client, rid)
    assert not d["ok"] and "Choose" in d["error"]
    assert _effects.read_file() == ""


def test_show_returns_the_file_as_html(cached_food) -> None:
    client = _client()
    rid = _new_recipe(client)
    _edit_page(client, rid, from_page="http://testserver/recipes")
    _add(client, rid, cached_food)
    _report(client, rid, _effects.ALL)
    d = client.get(f"/recipe/{rid}/edit-effects").json()
    assert d["path"].endswith(_effects.FILE_NAME)
    assert "<table>" in d["html"] and "<h2>Report 1" in d["html"]


def test_all_changed_keeps_only_changes_of_5_percent_or_more() -> None:
    groups = [("Macronutrients", ["calories", "protein_g"]), ("Minerals", ["iron_mg"])]
    before = {"per_serving": {"calories": 100.0, "protein_g": 10.0, "iron_mg": 2.0},
              "servings": 1, "dcp": None, "gl": None, "gl_complete": True}
    after = {"per_serving": {"calories": 104.0, "protein_g": 12.0, "iron_mg": 2.0, "zinc_mg": 1.0},
             "servings": 1, "dcp": None, "gl": None, "gl_complete": True}
    sections = dict(_effects.build_sections(before, after, groups, [_effects.ALL_CHANGED]))
    assert [r["label"] for r in sections["Macronutrients"]] == ["Protein", "Protein (DCP)"]
    assert "Minerals" not in sections
    assert [r["label"] for r in sections["Other"]][0].startswith("Zinc")   # new: 0 -> 1
    every = dict(_effects.build_sections(before, after, groups, [_effects.ALL]))
    assert len(every["Macronutrients"]) == 3 and "Minerals" in every


def test_the_food_details_panel_and_the_embedded_navbar_rule(cached_food) -> None:
    client = _client()
    rid = _new_recipe(client)
    page = _edit_page(client, rid, from_page="http://testserver/recipes").text
    assert 'id="details-overlay"' in page
    assert "numa-embedded" in client.get("/recipes").text


def test_dcp_is_reported_beside_protein_even_with_no_value() -> None:
    groups = [("Macronutrients", ["calories", "protein_g"])]
    snap = lambda p: {"per_serving": {"calories": 100.0, "protein_g": p}, "servings": 1,
                      "dcp": None, "gl": None, "gl_complete": True}
    rows = dict(_effects.build_sections(snap(10.0), snap(12.0), groups, ["Macronutrients"]))["Macronutrients"]
    assert [r["label"] for r in rows] == ["Calories", "Protein", "Protein (DCP)"]
    assert rows[2]["before"] is None and rows[2]["after"] is None
    # Kept by the 5% filter too: an unknown change can't be ruled small.
    rows = dict(_effects.build_sections(snap(10.0), snap(12.0), groups, [_effects.ALL_CHANGED]))["Macronutrients"]
    assert [r["label"] for r in rows] == ["Protein", "Protein (DCP)"]
