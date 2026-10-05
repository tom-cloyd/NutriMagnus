"""numa_app/services/data_quality.py and the pages built on it: impossible
values, stale amounts (and their fix + "what this change did"), the Home
page reminder, the note after adding a problem food, the recalculation log."""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
from numa_app.services import data_quality as dq
from web import backend


@pytest.fixture(autouse=True)
def _prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    f = tmp_path / "prefs.json"
    f.write_text(json.dumps({"include_animal_foods": True}))
    monkeypatch.setattr(backend, "_PREFS_FILE", f)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


GOOD = {"calories": 165.0, "protein_g": 31.0, "carbs_g": 0.0, "fat_g": 3.6,
        "sodium_mg": 74.0, "iron_mg": 1.0, "vitamin_a_mcg": 9.0}


@pytest.mark.parametrize("n,expect", [
    ({"carbs_g": 1333.33, "protein_g": 0, "fat_g": 0}, "1333.33 g of carbohydrate"),
    ({"protein_g": 40, "carbs_g": 40, "fat_g": 40}, "add up to 120 g"),
    ({"carbs_g": 10, "sugar_g": 20}, "more sugars"),
    ({"fat_g": 40, "saturated_fat_g": 10, "mono_fat_g": 20, "poly_fat_g": 16.7}, "three fat types"),
    ({"iron_mg": -1}, "negative value"),
])
def test_impossible_values(n, expect):
    assert any(expect in t for t in dq.impossible_values(n))


def test_plausible_foods_pass():
    assert dq.impossible_values({"fat_g": 100.0, "protein_g": 0, "carbs_g": 0}) == []      # oil
    assert dq.impossible_values({"carbs_g": 99.98, "sugar_g": 99.8, "protein_g": 0, "fat_g": 0}) == []  # sugar
    assert dq.impossible_values(GOOD) == []


def _food(conn, fid, name, nutrients, portions=None):
    _db.cache_food(conn, fid, name, "SR Legacy", None, 100.0, "g", nutrients, portions or [])


def test_stale_amount_found_fixed_with_impact(client):
    with _db.get_db() as conn:
        _food(conn, 997001, "Okara test", {**GOOD}, [{"description": "1 cup", "gram_weight": 125.4}])
        rid = _db.recipe_create(conn, "Soup test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997001, "Okara test", 41.8, "1/3 c")
        # The user later corrects the cup weight to 99 g.
        _db.update_food_fields(conn, 997001, portions=[{"description": "1 cup", "gram_weight": 99.0}])
        stale = dq.stale_amounts(conn)
    assert [(s["typed"], round(s["now_g"], 1)) for s in stale] == [("1/3 c", 33.0)]

    page = client.get("/food/cache/db-check").text
    assert 'id="stale-amounts"' in page and "1/3 c" in page
    r = client.post("/food/cache/db-check/stale-amounts", data={"item": f"recipe:{stale[0]['item_id']}"},
                    follow_redirects=False)
    assert "amounts_fixed=1" in r.headers["location"] and "impact=" in r.headers["location"]
    page = client.get(r.headers["location"]).text
    assert "What this change did" in page and "Soup test" in page
    with _db.get_db() as conn:
        assert dq.stale_amounts(conn) == []
        amt = conn.execute("SELECT amount, unit FROM recipe_ingredients WHERE recipe_id = ?", (rid,)).fetchone()
    assert amt["amount"] == pytest.approx(33.0) and amt["unit"] == "1/3 c"


def test_explicit_weight_never_stale():
    with _db.get_db() as conn:
        _food(conn, 997002, "Pea test", {**GOOD}, [{"description": "1 cup", "gram_weight": 99.0}])
        rid = _db.recipe_create(conn, "Shake test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997002, "Pea test", 15.0, "2 T (15 gr)")
        assert dq.stale_amounts(conn) == []


def test_bracketed_weight_only_offered_on_request():
    with _db.get_db() as conn:
        _food(conn, 997011, "Okara bracket test", {**GOOD}, [{"description": "1 cup", "gram_weight": 99.0}])
        rid = _db.recipe_create(conn, "Smoothie test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997011, "Okara bracket test", 41.8, "1/3 c (42 gr)")
        assert dq.stale_amounts(conn) == []
        rows = dq.stale_amounts(conn, fdc_id=997011, include_bracketed=True)
    assert [(r["bracketed"], r["unit_after"], round(r["now_g"], 1)) for r in rows] == [(True, "1/3 c", 33.0)]


def test_portion_edit_offers_this_foods_amounts_and_fixes_them(client):
    with _db.get_db() as conn:
        _food(conn, 997012, "Okara portions test", {**GOOD}, [{"description": "1 cup", "gram_weight": 125.4}])
        _food(conn, 997013, "Other food test", {**GOOD}, [{"description": "1 cup", "gram_weight": 50.0}])
        rid = _db.recipe_create(conn, "Tiger soup test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997012, "Okara portions test", 41.8, "1/3 c")
        _db.recipe_add_ingredient(conn, rid, 997012, "Okara portions test", 41.8, "1/3 c (42 gr)")
        _db.recipe_add_ingredient(conn, rid, 997013, "Other food test", 99.0, "1 c")   # another food: not listed
        mid = _db.meal_create(conn, "Lunch test", "2026-10-01")
        _db.meal_add_food(conn, mid, 997012, "Okara portions test", 41.8, "1/3 c")

    page = client.post("/food/cache/997012/portions/edit",
                       data={"portion_index": 0, "description": "1 cup", "gram_weight": "99"}).text
    assert "Amounts of this food that no longer match" in page
    assert "Other food test" not in page.split("Amounts of this food")[1].split("Add a portion")[0]
    with _db.get_db() as conn:
        rows = {(r["where"], r["bracketed"]): r for r in
                dq.stale_amounts(conn, fdc_id=997012, include_bracketed=True)}
    plain, bracketed, meal = rows[("recipe", False)], rows[("recipe", True)], rows[("meal", False)]
    # Recipe rows start ticked; meals and bracketed-weight rows start unticked.
    assert f'value="recipe:{plain["item_id"]}" checked' in page
    assert f'value="recipe:{bracketed["item_id"]}">' in page
    assert f'value="meal:{meal["item_id"]}">' in page

    r = client.post("/food/cache/db-check/stale-amounts", follow_redirects=False, data={
        "portions_fdc_id": 997012,
        "item": [f"recipe:{plain['item_id']}", f"recipe:{bracketed['item_id']}", f"meal:{meal['item_id']}"]})
    assert r.headers["location"].startswith("/food/cache/997012/portions?amounts_fixed=3")
    page = client.get(r.headers["location"]).text
    assert "Updated 3 amounts" in page and "What this change did" in page
    assert "Amounts of this food that no longer match" not in page
    with _db.get_db() as conn:
        got = {row["id"]: (row["amount"], row["unit"]) for row in
               conn.execute("SELECT id, amount, unit FROM recipe_ingredients WHERE recipe_id = ?", (rid,))}
        meal_row = conn.execute("SELECT amount, unit FROM meal_items WHERE id = ?", (meal["item_id"],)).fetchone()
    assert got[plain["item_id"]] == (pytest.approx(33.0), "1/3 c")
    assert got[bracketed["item_id"]] == (pytest.approx(33.0), "1/3 c")       # bracketed 42 gr dropped
    assert (meal_row["amount"], meal_row["unit"]) == (pytest.approx(33.0), "1/3 c")


def test_keep_as_entered_hides_then_unkeep_restores(client):
    with _db.get_db() as conn:
        _food(conn, 997021, "Yeast keep test", {**GOOD}, [{"description": "1 tbsp", "gram_weight": 2.6}])
        rid = _db.recipe_create(conn, "Smoothie keep test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997021, "Yeast keep test", 18.06, "2 T")
        (row,) = dq.stale_amounts(conn, fdc_id=997021)
    item = f"recipe:{row['item_id']}"

    r = client.post("/food/cache/db-check/stale-amounts", follow_redirects=False,
                    data={"portions_fdc_id": 997021, "item": item, "action": "keep"})
    assert r.headers["location"] == "/food/cache/997021/portions?amounts_kept=1#stale-amounts"
    page = client.get(r.headers["location"]).text
    assert "Kept 1 amount as entered" in page
    assert "Amounts of this food kept as entered" in page and "Kept as entered</span>" in page
    assert "Amounts of this food that no longer match" not in page
    with _db.get_db() as conn:
        assert dq.stale_amounts(conn) == []                                  # off Foods -> 9's list and the reminder
        amt = conn.execute("SELECT amount FROM recipe_ingredients WHERE id = ?", (row["item_id"],)).fetchone()[0]
    assert amt == pytest.approx(18.06)                                       # grams untouched
    db_page = client.get("/food/cache/db-check").text
    assert "Kept as entered" in db_page and "Smoothie keep test" in db_page

    r = client.post("/food/cache/db-check/stale-amounts", follow_redirects=False,
                    data={"portions_fdc_id": 997021, "item": item, "action": "unkeep"})
    page = client.get(r.headers["location"]).text
    assert "1 amount is listed for review again" in page
    assert "Amounts of this food that no longer match" in page


def test_keep_ends_when_the_amount_is_edited():
    with _db.get_db() as conn:
        _food(conn, 997022, "Yeast edit test", {**GOOD}, [{"description": "1 tbsp", "gram_weight": 2.6}])
        rid = _db.recipe_create(conn, "Edit keep test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997022, "Yeast edit test", 18.06, "2 T")
        (row,) = dq.stale_amounts(conn, fdc_id=997022)
        _db.amount_keep(conn, "recipe", row["item_id"], row["stored_g"])
        assert dq.stale_amounts(conn, fdc_id=997022) == []
        _db.recipe_update_ingredient(conn, row["item_id"], 12.0, "2 T", "Yeast edit test", None)
        assert len(dq.stale_amounts(conn, fdc_id=997022)) == 1


def test_database_check_lists_bracketed_rows_unticked(client):
    with _db.get_db() as conn:
        _food(conn, 997023, "Okara list test", {**GOOD}, [{"description": "1 cup", "gram_weight": 99.0}])
        rid = _db.recipe_create(conn, "Bracket list test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997023, "Okara list test", 41.8, "1/3 c (42 gr)")
        (row,) = dq.stale_amounts(conn, include_bracketed=True)
    page = client.get("/food/cache/db-check").text
    assert "Bracket list test" in page and "(with a weight in brackets)" in page
    assert f'value="recipe:{row["item_id"]}">' in page                      # not pre-ticked


@pytest.mark.parametrize("unit,portions,expect", [
    ("2 T", [], "typed"),                                               # table density for "protein isolate"
    ("2 T (14.7 gr)", [], "bracketed"),
    ("15 g", [], None),                                                 # a typed weight is presumed right
    ("2 T 15 g", [], None),
    ("p1", [{"description": "1 scoop", "gram_weight": 30.0}], None),
    ("2 T", [{"description": "1 cup", "gram_weight": 112.0}], None),   # the food's own cup
])
def test_generic_density_kind(unit, portions, expect):
    from numa_app.services.portions import generic_density_kind
    assert generic_density_kind(unit, portions, "Soy protein isolate") == expect


def test_generic_density_marked_listed_and_cleared_by_a_portion(client):
    with _db.get_db() as conn:
        _food(conn, 997031, "Soy protein isolate test", {**GOOD})
        rid = _db.recipe_create(conn, "Shake generic test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997031, "Soy protein isolate test", 14.8, "2 T")
    for url in (f"/recipe/{rid}", f"/recipe/{rid}/edit"):
        page = client.get(url).text
        assert "generic*</a>" in page and "converted it with a generic density" in page, url
        assert "/food/cache/997031/portions" in page
    db_page = client.get("/food/cache/db-check").text
    section = db_page.split('id="generic-density"')[1].split("</details>")[0]
    assert "Soy protein isolate test" in section and "Shake generic test" in section

    client.post("/food/cache/997031/portions/add", data={"description": "1 cup", "gram_weight": "112"})
    page = client.get(f"/recipe/{rid}").text
    assert "generic*</a>" not in page and "converted it with a generic density" not in page
    with _db.get_db() as conn:
        assert dq.generic_density_in_use(conn) == []
        assert len(dq.stale_amounts(conn, fdc_id=997031)) == 1               # now offered for correction


def test_home_reminder_shows_new_problems_then_clears(client):
    with _db.get_db() as conn:
        _food(conn, 997003, "Broken salt test", {"calories": 0, "protein_g": 0, "carbs_g": 1333, "fat_g": 0})
    assert "DATA CHECK:" in client.get("/").text
    client.get("/food/cache/db-check")           # reviewing marks everything seen
    assert "DATA CHECK:" not in client.get("/").text
    with _db.get_db() as conn:
        _food(conn, 997004, "Another bad test", {"protein_g": 50, "carbs_g": 50, "fat_g": 50, "calories": 900})
    assert "new data problem" in client.get("/").text
    client.post("/settings/data-check-reminder", data={"enabled": "0", "weeks": "0"})
    assert "DATA CHECK:" not in client.get("/").text


def test_note_after_adding_problem_food_to_meal(client):
    with _db.get_db() as conn:
        _food(conn, 997005, "No calorie test", {"fiber_g": 4.0, "iron_mg": 1.0})
    meal_id = int(client.post("/meals/create", data={"name": "Lunch", "meal_date": "2026-07-11"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    r = client.post(f"/meal/{meal_id}/add", data={"fdc_id": 997005, "food_name": "No calorie test",
                                                  "portion_str": "30 g"}, follow_redirects=False)
    # (It may detour via the GI/DIAAS annotate page first; the check rides along in next=.)
    assert "added_check" in r.headers["location"] and "997005" in r.headers["location"]
    page = client.get(f"/meal/{meal_id}?q=&added_check=997005").text
    assert "Check this food&rsquo;s data" in page and "no calorie value" in page


def test_food_change_logs_recalc_on_past_meals(client):
    with _db.get_db() as conn:
        _food(conn, 997006, "Almond log test", {**GOOD})
    meal_id = int(client.post("/meals/create", data={"name": "Breakfast", "meal_date": "2026-07-11"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    client.post(f"/meal/{meal_id}/add", data={"fdc_id": 997006, "food_name": "Almond log test",
                                              "portion_str": "50 g"}, follow_redirects=False)
    from numa_app.services import recipe_dcp
    with _db.get_db() as conn:
        _db.update_food_nutrients_partial(conn, 997006, {"calories": 600.0})
        recipe_dcp.cascade_food_change(997006, conn)
    page = client.get(f"/meal/{meal_id}").text
    assert "Totals recalculated:" in page and "Almond log test: its data changed" in page


def _used_in_recipe(conn, fid, name, rid=None):
    rid = rid or _db.recipe_create(conn, f"Recipe using {name}", "", 1, "")
    _db.recipe_add_ingredient(conn, rid, fid, name, 50.0, "50 g")
    return rid


def test_in_use_lists_skip_unused_and_honour_not_needed(client):
    with _db.get_db() as conn:
        _food(conn, 997101, "Used no AA", {**GOOD})                         # protein, no AA, no portions
        _food(conn, 997102, "Unused no AA", {**GOOD})
        _used_in_recipe(conn, 997101, "Used no AA")
        aa = [r["fdc_id"] for r in dq.missing_aa_in_use(conn)]
        por = [r["fdc_id"] for r in dq.missing_portions_in_use(conn)]
    assert 997101 in aa and 997102 not in aa
    assert 997101 in por and 997102 not in por
    page = client.get("/food/cache/db-check").text
    assert 'id="missing-aa"' in page and 'id="missing-portions"' in page and "Used no AA" in page
    r = client.post("/food/cache/db-check/completeness",
                    data={"shown": ["997101:portions"], "ignore": ["997101:portions"], "back": "missing-portions"},
                    follow_redirects=False)
    assert r.headers["location"].endswith("#missing-portions")
    with _db.get_db() as conn:
        assert [r["ignored"] for r in dq.missing_portions_in_use(conn) if r["fdc_id"] == 997101] == [True]


def test_duplicates_merge_and_dismiss(client):
    with _db.get_db() as conn:
        _food(conn, 997201, "Peanut Butter Powder", {**GOOD})
        _food(conn, 997202, "PEANUT BUTTER POWDER", {**GOOD, "calories": 400.0})
        _food(conn, 997203, "* Sugars, granulated", {"calories": 387, "protein_g": 0, "carbs_g": 100, "fat_g": 0})
        _food(conn, 997204, "Sugars, granulated", {"calories": 387, "protein_g": 0, "carbs_g": 100, "fat_g": 0})
        rid = _used_in_recipe(conn, 997202, "PEANUT BUTTER POWDER")
        groups = {g["name"].lower(): g for g in dq.duplicate_groups(conn)}
    pb = groups["peanut butter powder"]
    assert sorted(f["fdc_id"] for f in pb["foods"]) == [997201, 997202]

    page = client.get("/food/cache/duplicates").text
    assert "Keep this one" in page and "Not duplicates" in page
    r = client.post("/food/cache/duplicates/keep", data={"group_key": pb["key"], "keep": 997201},
                    follow_redirects=False)
    assert "merged=1" in r.headers["location"]
    with _db.get_db() as conn:
        assert _db.get_cached_food(conn, 997202) is None
        ing = conn.execute("SELECT fdc_id, food_name FROM recipe_ingredients WHERE recipe_id = ?", (rid,)).fetchone()
    assert ing["fdc_id"] == 997201 and ing["food_name"] == "PEANUT BUTTER POWDER"
    assert "What this change did" in client.get(r.headers["location"]).text  # 400 -> 165 kcal/100 g

    with _db.get_db() as conn:
        sugar_key = next(g["key"] for g in dq.duplicate_groups(conn) if "sugars" in g["name"].lower())
    client.post("/food/cache/duplicates/dismiss", data={"group_key": sugar_key})
    with _db.get_db() as conn:
        assert not any("sugars" in g["name"].lower() for g in dq.duplicate_groups(conn))
        assert any("sugars" in g["name"].lower() for g in dq.duplicate_groups(conn, include_dismissed=True))


def test_claude_import_shows_impact(client):
    with _db.get_db() as conn:
        _food(conn, 9000002, "Imported food", {"calories": 100, "protein_g": 10, "carbs_g": 5, "fat_g": 2})
        _used_in_recipe(conn, 9000002, "Imported food")
    text = ("```json\n"
            '{"fdc_id": 9000002, "name": "Imported food", "fdc_type": "User Drafted", '
            '"calories": 300, "protein_g": 10, "carbs_g": 5, "fat_g": 2}\n```')
    r = client.post("/food/cache/claude-import", data={"response_text": text, "action": "confirm", "overwrite": 1},
                    follow_redirects=False)
    assert "impact=" in r.headers["location"]
    assert "What this change did" in client.get(r.headers["location"]).text
