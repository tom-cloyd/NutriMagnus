"""numa_app/services/supplements.py and the pages built on it: a food marked
as a supplement skips every food check, weighs nothing, stays out of glycemic
load, reads per tablet, and its nutrients show as "from supplements" in
meal, day and summary totals.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/supplements.py — supplements and the from-supplements split"
"""
import json
import pathlib
from datetime import date

import pytest
from fastapi.testclient import TestClient

import db as _db
from numa_app.services import data_quality as dq
from numa_app.services import supplements as supps
from numa_app.services.recipe_nutrients import expand_recipe_ingredients
from web import backend

B12_ID, LENTIL_ID = -998001, 998002
DAY = date.today().isoformat()   # the trend page counts back from today


@pytest.fixture(autouse=True)
def _prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    f = tmp_path / "prefs.json"
    f.write_text(json.dumps({"include_animal_foods": True}))
    monkeypatch.setattr(backend, "_PREFS_FILE", f)
    from numa_app.services import manual_build
    monkeypatch.setattr(manual_build, "rebuild_manual_if_stale", lambda: None)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


def _b12(conn, *, flag=True):
    """A B12 tablet the supplement-mode way: 1 tablet = the internal 100 g,
    with nothing but B12 (and a trace of sugar from the coating)."""
    _db.cache_food(conn, B12_ID, "B12 tablet test", "User Drafted", None, 1.0, "tablet",
                   {"b12_mcg": 250.0, "carbs_g": 0.4},
                   [{"description": "1 tablet", "gram_weight": 100.0}], user_drafted=True)
    if flag:
        _db.set_food_is_supplement(conn, B12_ID, True)


def _lentil(conn):
    _db.cache_food(conn, LENTIL_ID, "Lentil test", "SR Legacy", None, 100.0, "g",
                   {"calories": 116.0, "protein_g": 9.0, "carbs_g": 20.0, "fat_g": 0.4,
                    "b12_mcg": 0.0, "iron_mg": 3.3}, [])


def test_tag_and_amount():
    tagged = supps.tag({"b12_mcg": 250.0, "water_drinks_g": 0.0}, True)
    assert supps.supp_amount(tagged, "b12_mcg") == 250.0
    assert "water_drinks_g__supp" not in tagged          # only tracked nutrients
    assert supps.tag({"b12_mcg": 1.0}, False) == {"b12_mcg": 1.0}
    assert supps.unit_name(1, "Tablets") == "tablet"
    assert supps.unit_name(2, "tablet") is None


def test_a_supplement_skips_every_food_check():
    with _db.get_db() as conn:
        _b12(conn)
        rid = _db.recipe_create(conn, "Uses it", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, B12_ID, "B12 tablet test", 100, "1 tablet")
        assert dq.issues_for_food(conn, B12_ID) == []            # no "no calorie value"
        scan = dq.scan(conn)
        assert not [r for r in scan["food_issues"] if r["fdc_id"] == B12_ID]
        assert not [g for g in scan["gaps"] if g["fdc_id"] == B12_ID]
        for rows in (dq.missing_aa_in_use(conn), dq.missing_portions_in_use(conn), dq.missing_gi_in_use(conn)):
            assert B12_ID not in {r["fdc_id"] for r in rows}
        # Unmarked, the same tablet is a food with no calorie value.
        _db.set_food_is_supplement(conn, B12_ID, False)
        assert [i["kind"] for i in dq.issues_for_food(conn, B12_ID)] == ["calories_missing"]


def test_a_supplement_weighs_nothing_and_stays_out_of_gl():
    from numa_app.services.glycemic_load import recipe_gl
    with _db.get_db() as conn:
        _b12(conn)
        _lentil(conn)
        rid = _db.recipe_create(conn, "Lentils with B12", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, LENTIL_ID, "Lentil test", 200, "g")
        _db.recipe_add_ingredient(conn, rid, B12_ID, "B12 tablet test", 100, "1 tablet")
        assert _db.recipe_compute_weight(conn, rid) == (200.0, True)
        leaves = expand_recipe_ingredients(rid, conn)
        assert [lf["is_supplement"] for lf in leaves] == [False, True]
        gl = recipe_gl(conn, rid)
        assert not [g for g in gl["gaps"] if g["fdc_id"] == B12_ID]


def test_bare_number_counts_tablets_for_a_supplement():
    portions = [{"description": "1 tablet", "gram_weight": 100.0}]
    assert backend._parse_portion_str("2", portions, "B12")[0] == 200.0
    assert backend._parse_portion_str("1/2", portions, "B12")[0] == 50.0
    assert backend._parse_portion_str("2", [{"description": "1 cup", "gram_weight": 240.0}], "Milk")[0] == 2.0


def test_meal_day_and_summary_show_the_from_supplements_split(client):
    with _db.get_db() as conn:
        _b12(conn)
        _lentil(conn)
        mid = _db.meal_create(conn, "Lunch", DAY)
    r = client.post(f"/meal/{mid}/add", data={"fdc_id": LENTIL_ID, "food_name": "Lentil test",
                                              "portion_str": "200 g"}, follow_redirects=False)
    assert r.status_code == 303
    client.post(f"/meal/{mid}/add", data={"fdc_id": B12_ID, "food_name": "B12 tablet test",
                                          "portion_str": "2"}, follow_redirects=False)
    with _db.get_db() as conn:
        grams = sorted(i["amount"] for i in _db.meal_get_items(conn, mid))
    assert grams == [200.0, 200.0]                                 # 2 tablets, 200 g lentils
    for page in (f"/meal/{mid}", f"/meal/{mid}/day", f"/summary/{DAY}",
                 "/summary/trend?days=7"):
        text = client.get(page).text
        assert "all from supplements" in text, page               # B12 came only from the tablets
        assert "no calorie value" not in text, page


def test_the_food_page_switch_and_per_tablet_reading(client):
    with _db.get_db() as conn:
        _b12(conn, flag=False)
    page = client.get(f"/food/{B12_ID}").text
    assert 'id="supplement-toggle"' in page and 'id="is_supplement"' in page
    client.post(f"/food/{B12_ID}/supplement", data={"is_supplement": "1"})
    page = client.get(f"/food/{B12_ID}").text
    assert ">1 tablet</th>" in page                               # per tablet, not per 100 g
    assert "drink-toggle" not in page
    with _db.get_db() as conn:
        assert B12_ID in _db.supplement_ids(conn)
    client.post(f"/food/{B12_ID}/supplement", data={})
    with _db.get_db() as conn:
        assert B12_ID not in _db.supplement_ids(conn)


def test_supplement_mode_save_marks_it_a_supplement(client):
    with _db.get_db() as conn:
        _db.cache_food(conn, -998003, "D3 test", "User Drafted", None, 100.0, "g", {}, [], user_drafted=True)
    client.post("/food/custom-profiles/-998003/edit",
                data={"name": "D3 test", "serving_size": "1", "serving_unit": "softgel", "vitamin_d_mcg": "25"})
    with _db.get_db() as conn:
        assert -998003 in _db.supplement_ids(conn)


def test_meal_pages_show_a_supplement_as_tablets_not_grams(client):
    """A supplement's internal 100 g per tablet is not a weight: meal, day
    and summary pages read "2 tablets" / "0.5 tablet", even for an old line
    whose saved label is "200 g", and the Edit box offers the count."""
    with _db.get_db() as conn:
        _b12(conn)
        mid = _db.meal_create(conn, "Lunch", DAY)
        _db.meal_add_food(conn, mid, B12_ID, "B12 tablet test", 200.0, "200 g")
    page = client.get(f"/meal/{mid}").text
    assert "2 tablets" in page and "200.0&thinsp;g" not in page
    assert 'name="amount" value="2 tablets"' in page
    for url in (f"/meal/{mid}/day", f"/summary/{DAY}"):
        assert "2 tablets" in client.get(url).text, url
    with _db.get_db() as conn:
        item = _db.meal_get_items(conn, mid)[0]
    client.post(f"/meal/{mid}/update/{item['id']}", data={"amount": "1/2"}, follow_redirects=False)
    with _db.get_db() as conn:
        assert _db.meal_get_items(conn, mid)[0]["amount"] == 50.0
    page = client.get(f"/meal/{mid}").text
    assert "0.5 tablet" in page and "0.5 tablets" not in page


def test_recipe_pages_link_custom_foods_and_supplements(client):
    """An ingredient with a negative ID (custom food, supplement) links to
    its own page on the recipe page and Edit Recipe, like a USDA food."""
    with _db.get_db() as conn:
        _b12(conn)
        rid = _db.recipe_create(conn, "Supplements daily test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, B12_ID, "B12 tablet test", 100.0, "1 tablet")
    for url in (f"/recipe/{rid}", f"/recipe/{rid}/edit"):
        page = client.get(url).text
        assert f'<a href="/food/{B12_ID}' in page, url
    assert client.get(f"/food/{B12_ID}").status_code == 200
