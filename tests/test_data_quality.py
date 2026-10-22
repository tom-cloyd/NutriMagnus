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


def test_keep_as_entered_rewrites_the_amount_as_its_own_weight(client):
    with _db.get_db() as conn:
        _food(conn, 997021, "Yeast keep test", {**GOOD}, [{"description": "1 tbsp", "gram_weight": 2.6}])
        rid = _db.recipe_create(conn, "Smoothie keep test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997021, "Yeast keep test", 18.06, "2 T")
        _db.recipe_add_ingredient(conn, rid, 997021, "Yeast keep test", 2309.216, "8 c (2309 gr)")
        rows = dq.stale_amounts(conn, fdc_id=997021, include_bracketed=True)
    assert len(rows) == 2

    r = client.post("/food/cache/db-check/stale-amounts", follow_redirects=False,
                    data={"portions_fdc_id": 997021, "action": "keep",
                          "item": [f"recipe:{a['item_id']}" for a in rows]})
    assert r.headers["location"] == "/food/cache/997021/portions?amounts_kept=2#stale-amounts"
    page = client.get(r.headers["location"]).text
    assert "Kept 2 amounts as entered" in page
    assert "Amounts of this food that no longer match" not in page and "kept as entered</h4>" not in page
    with _db.get_db() as conn:
        assert dq.stale_amounts(conn, include_bracketed=True, include_kept=True) == []
        got = conn.execute("SELECT amount, unit FROM recipe_ingredients WHERE recipe_id = ? ORDER BY id",
                           (rid,)).fetchall()
        assert _db.amount_keeps(conn) == {}
    assert [(g["amount"], g["unit"]) for g in got] == [(pytest.approx(18.06), "18.1 g (2 T)"),
                                                       (pytest.approx(2309.216), "2309.2 g (8 c)")]   # grams untouched
    assert "Smoothie keep test" not in client.get("/food/cache/db-check").text


@pytest.mark.parametrize("unit,grams,expect", [
    ("2 T", 18.06, "18.1 g (2 T)"),
    ("8 c (2309 gr)", 2309.216, "2309.2 g (8 c)"),
    ("1/3 c (~42 g)", 42.0, "42 g (1/3 c)"),
    ("42 g", 42.0, None),
    ("200 g (1 3/5 c)", 200.0, None),
    ("", 5.0, None),
])
def test_own_weight_text(unit, grams, expect):
    assert dq.own_weight_text(unit, grams) == expect


def test_old_keeps_are_converted_at_startup():
    with _db.get_db() as conn:
        _food(conn, 997022, "Yeast convert test", {**GOOD}, [{"description": "1 tbsp", "gram_weight": 2.6}])
        rid = _db.recipe_create(conn, "Convert keep test", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997022, "Yeast convert test", 18.06, "2 T")
        _db.recipe_add_ingredient(conn, rid, 997022, "Yeast convert test", 12.0, "2 T")
        ids = [r[0] for r in conn.execute("SELECT id FROM recipe_ingredients WHERE recipe_id = ? ORDER BY id", (rid,))]
        _db.amount_keep(conn, "recipe", ids[0], 18.06)
        _db.amount_keep(conn, "recipe", ids[1], 10.0)                       # edited since it was kept
        assert dq.convert_keeps(conn) == 1
        units = [r[0] for r in conn.execute("SELECT unit FROM recipe_ingredients WHERE recipe_id = ? ORDER BY id", (rid,))]
        assert units == ["18.1 g (2 T)", "2 T"]
        assert _db.amount_keeps(conn) == {}
        assert len(dq.stale_amounts(conn, fdc_id=997022)) == 1               # the edited one is listed again


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
    # Their calories differ, so Keep goes to the review step first.
    r = client.post("/food/cache/duplicates/keep", data={"group_key": pb["key"], "keep": 997201},
                    follow_redirects=False)
    assert r.headers["location"].startswith("/food/cache/duplicates/review?")
    review = client.get(r.headers["location"]).text
    assert "Choose values to keep" in review and 'name="pick_calories"' in review
    with _db.get_db() as conn:
        assert _db.get_cached_food(conn, 997202) is not None
    r = client.post("/food/cache/duplicates/keep", data={"group_key": pb["key"], "keep": 997201,
                                                         "reviewed": "1", "pick_calories": "keep"},
                    follow_redirects=False)
    assert "merged=1" in r.headers["location"] and "copied" not in r.headers["location"]
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


def test_duplicates_merge_identical_skips_review(client):
    with _db.get_db() as conn:
        _food(conn, 997211, "Hemp seed test", {**GOOD})
        _food(conn, 997212, "HEMP SEED TEST", {**GOOD})
        key = next(g["key"] for g in dq.duplicate_groups(conn) if "hemp" in g["name"].lower())
    page = client.get("/food/cache/duplicates").text
    assert "reviewing the others" not in page
    r = client.post("/food/cache/duplicates/keep", data={"group_key": key, "keep": 997211},
                    follow_redirects=False)
    assert "merged=1" in r.headers["location"]


def test_merge_review_prefers_the_users_edits():
    with _db.get_db() as conn:
        _food(conn, 997221, "Lentils test", {**GOOD})
        _food(conn, 997222, "LENTILS TEST", {**GOOD, "iron_mg": 2.0, "zinc_mg": 3.0},
              [{"description": "1 cup", "gram_weight": 198.0}])
        # The user corrected iron on the copy that's about to be dropped.
        _db.merge_user_supplied_nutrients(conn, 997222, {"iron_mg": 6.5}, overwrite=True)
        g = next(g for g in dq.duplicate_groups(conn) if "lentils" in g["name"].lower())
        edited = {f["fdc_id"]: f["edited"] for f in g["foods"]}
        review = dq.merge_review(conn, 997221, [997221, 997222], [("All", [
            ("iron_mg", "Iron", "mg"), ("zinc_mg", "Zinc", "mg"), ("protein_g", "Protein", "g")])])
    assert edited == {997221: [], 997222: ["Iron"]}
    fields = {f["key"]: f for f in review["groups"][0]["fields"]}
    assert set(fields) == {"iron_mg", "zinc_mg"}                    # protein agrees: not listed
    assert fields["iron_mg"]["pick"] == 997222 and fields["iron_mg"]["options"][0]["mine"]
    assert fields["zinc_mg"]["pick"] == 997222                      # fills a blank
    assert [p["portion"]["description"] for p in review["portions"]] == ["1 cup"]


def test_merge_review_keeps_kept_foods_own_edit():
    with _db.get_db() as conn:
        _food(conn, 997231, "Oats test", {**GOOD})
        _food(conn, 997232, "OATS TEST", {**GOOD})
        _db.merge_user_supplied_nutrients(conn, 997231, {"iron_mg": 4.0}, overwrite=True)
        _db.merge_user_supplied_nutrients(conn, 997232, {"iron_mg": 5.0}, overwrite=True)
        review = dq.merge_review(conn, 997231, [997231, 997232], [("All", [("iron_mg", "Iron", "mg")])])
    f = review["groups"][0]["fields"][0]
    assert f["current_mine"] and f["pick"] is None


def test_duplicates_merge_copies_chosen_values_as_edits(client):
    with _db.get_db() as conn:
        _food(conn, 997241, "Tahini test", {**GOOD})
        _food(conn, 997242, "TAHINI TEST", {**GOOD, "calcium_mg": 420.0},
              [{"description": "1 tbsp", "gram_weight": 15.0}])
        _db.merge_user_supplied_nutrients(conn, 997242, {"iron_mg": 8.9}, overwrite=True)
        key = next(g["key"] for g in dq.duplicate_groups(conn) if "tahini" in g["name"].lower())
    assert "reviewing the others" in client.get("/food/cache/duplicates").text
    r = client.post("/food/cache/duplicates/keep",
                    data={"group_key": key, "keep": 997241, "reviewed": "1", "pick_iron_mg": "997242",
                          "pick_calcium_mg": "997242", "portion": "997242|1 tbsp"},
                    follow_redirects=False)
    assert "merged=1" in r.headers["location"] and "copied=3" in r.headers["location"]
    with _db.get_db() as conn:
        kept = _db.get_cached_food(conn, 997241)
        nutrients = json.loads(kept["nutrients_json"])
        assert nutrients["iron_mg"] == 8.9 and nutrients["calcium_mg"] == 420.0
        assert [p["description"] for p in json.loads(kept["portions_json"])] == ["1 tbsp"]
        # Copied in as the user's own, so a USDA refresh won't take them back silently.
        assert {"iron_mg", "calcium_mg"} <= set(_db.food_edited_keys(conn, 997241))
        assert "Merged from duplicate TAHINI TEST" in (kept["notes"] or "")
        assert _db.get_cached_food(conn, 997242) is None


def test_merging_foods_leaves_one_pantry_entry(client):
    with _db.get_db() as conn:
        _food(conn, 997251, "Chia test", {**GOOD})
        _food(conn, 997252, "CHIA TEST", {**GOOD})
        conn.execute("INSERT INTO pantry (food_name, fdc_id, notes) VALUES ('Chia test', 997251, 'bulk bin')")
        conn.execute("INSERT INTO pantry (food_name, fdc_id, notes) VALUES ('CHIA TEST', 997252, 'organic')")
        _db.merge_food_into(conn, 997251, 997252)
        rows = conn.execute("SELECT fdc_id, notes FROM pantry WHERE fdc_id = 997251").fetchall()
    assert len(rows) == 1 and rows[0]["notes"] == "bulk bin  |  organic"


def test_pantry_add_does_not_duplicate():
    with _db.get_db() as conn:
        _food(conn, 997261, "Flax test", {**GOOD})
        a = _db.pantry_add(conn, "Flax test", 997261)
        _db.set_pantry_archived(conn, a, True)
        b = _db.pantry_add(conn, "Flax test", 997261, "ground")
        row = _db.pantry_get(conn, a)
    assert a == b and row["archived"] == 0 and row["notes"] == "ground"


def test_pantry_duplicates_listed_and_merged(client):
    with _db.get_db() as conn:
        _food(conn, 997271, "Hemp hearts test", {**GOOD})
        for notes, archived in (("Starter data", 1), (None, 1), ("raw", 0)):
            conn.execute("INSERT INTO pantry (food_name, fdc_id, notes, archived) VALUES (?, 997271, ?, ?)",
                         ("Hemp hearts test", notes, archived))
        ids = [r[0] for r in conn.execute("SELECT id FROM pantry WHERE fdc_id = 997271 ORDER BY id")]
    page = client.get("/food/cache/duplicates").text
    assert "Foods in your pantry more than once" in page and "Hemp hearts test" in page
    r = client.post("/food/cache/duplicates/pantry", data={"fdc_id": 997271}, follow_redirects=False)
    assert "pantry_merged=2" in r.headers["location"]
    with _db.get_db() as conn:
        rows = conn.execute("SELECT id, notes, archived FROM pantry WHERE fdc_id = 997271").fetchall()
        assert _db.pantry_duplicate_groups(conn) == []
    # The starter entry isn't the one kept (clearing starter data deletes those).
    assert [(r["id"], r["notes"], r["archived"]) for r in rows] == [(ids[1], "raw", 0)]


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


# ── Starter data never greets a new user with data problems (2026-10-04) ──

def test_starter_problems_are_seen_but_users_own_are_not(client, tmp_path, monkeypatch):
    from numa_app.services import demo_data
    monkeypatch.setattr(demo_data, "_MARKER_FILE", tmp_path / "demo_data.json")
    monkeypatch.setattr(demo_data, "_SEED_ATTEMPTED_MARKER", tmp_path / "seeded")
    bad = {"fdc_id": 997101, "name": "* Bad starter salt", "data_type": "SR Legacy",
           "nutrients": {"calories": 0, "protein_g": 0, "carbs_g": 1333, "fat_g": 0}, "portions": []}
    monkeypatch.setattr(demo_data, "DEMO_FOODS", [bad])
    monkeypatch.setattr(demo_data, "DEMO_PANTRY", [])
    monkeypatch.setattr(demo_data, "DEMO_RECIPES", [])
    with client:                                   # startup: fresh install, seeded
        assert "DATA CHECK:" not in client.get("/").text
        assert "1333 g of carbohydrate" in client.get("/food/cache/db-check").text  # still listed
        with _db.get_db() as conn:
            _food(conn, 997102, "My own bad food", {"calories": 0, "protein_g": 0, "carbs_g": 500, "fat_g": 0})
        assert "DATA CHECK:" in client.get("/").text


def test_calories_confirmed_right_stops_the_mismatch_check(client):
    vanilla = {"calories": 288.0, "protein_g": 0.06, "carbs_g": 12.65, "fat_g": 0.06}
    with _db.get_db() as conn:
        _food(conn, 997103, "Vanilla test", vanilla)
    page = client.get("/food/997103").text
    assert "far from what its" in page and "These calories are right" in page
    client.post("/food/997103/data-ignore", data={"group": dq.CALORIES_OK_KEY})
    page = client.get("/food/997103").text
    assert "far from what its" not in page and "Check them again" in page
    with _db.get_db() as conn:
        assert not {k for k in dq.scan(conn)["keys"] if k.startswith("food:997103:")}
    client.post("/food/997103/data-ignore", data={"group": dq.CALORIES_OK_KEY, "ignored": "0"})
    assert "far from what its" in client.get("/food/997103").text


def test_misspelled_carb_key_is_renamed_on_startup():
    with _db.get_db() as conn:
        _food(conn, 997104, "Old OFF tomatoes", {"calories": 21, "protein_g": 0.8, "carb_g": 5.0, "fat_g": 0})
        conn.execute("UPDATE foods SET source_json = ? WHERE fdc_id = 997104",
                     (json.dumps({"nutrients": {"carb_g": 5.0}, "portions": []}),))
        meal_id = _db.meal_create(conn, "Lunch", "2026-07-11")
        conn.execute("INSERT INTO meal_items (meal_id, item_type, fdc_id, food_name, amount, unit) "
                     "VALUES (?, 'food', 997104, 'Old OFF tomatoes', 100, 'g')", (meal_id,))
    _db.init_db()
    with _db.get_db() as conn:
        row = conn.execute("SELECT nutrients_json, source_json FROM foods WHERE fdc_id = 997104").fetchone()
        assert json.loads(row[0])["carbs_g"] == 5.0 and "carb_g" not in json.loads(row[0])
        assert json.loads(row[1])["nutrients"] == {"carbs_g": 5.0}
        assert conn.execute("SELECT 1 FROM stale_meals WHERE meal_id = ?", (meal_id,)).fetchone()


def test_meal_add_keeps_typed_amount_so_portion_fixes_reach_it(client):
    """Adding a food to a meal stores what was typed ("1/3 c"), like a recipe
    ingredient, so a later portion correction finds the meal entry too."""
    with _db.get_db() as conn:
        _food(conn, 997031, "Okara meal test", {**GOOD}, [{"description": "1 cup", "gram_weight": 125.4}])
        mid = _db.meal_create(conn, "Typed lunch test", "2026-10-01")
    client.post(f"/meal/{mid}/add", data={"fdc_id": 997031, "portion_str": "1/3 c"},
                follow_redirects=False)
    with _db.get_db() as conn:
        row = conn.execute("SELECT id, amount, unit FROM meal_items WHERE meal_id = ?", (mid,)).fetchone()
    assert (row["amount"], row["unit"]) == (pytest.approx(41.8), "0.333333 c")   # as recipes store it
    page = client.get(f"/meal/{mid}").text
    assert "41.8&thinsp;g" in page and "(1/3 c)" in page
    assert 'value="1/3 c"' in page                       # Edit box offers what was typed

    client.post(f"/meal/{mid}/update/{row['id']}", data={"amount": "1/2 c"}, follow_redirects=False)
    with _db.get_db() as conn:
        assert conn.execute("SELECT unit FROM meal_items WHERE id = ?", (row["id"],)).fetchone()[0] == "0.5 c"
        _food(conn, 997031, "Okara meal test", {**GOOD}, [{"description": "1 cup", "gram_weight": 99.0}])
        stale = dq.stale_amounts(conn, fdc_id=997031)
    assert [(s["where"], s["typed"], round(s["now_g"], 1)) for s in stale] == [("meal", "0.5 c", 49.5)]


def _days_eaten_setup(conn):
    """Rice (no GI) eaten on its own one day and inside a sub-recipe another;
    cinnamon (no GI, a pinch) and a carb-less supplement (no carbs value)."""
    _food(conn, 997101, "Rice test", {"carbs_g": 28.0, "protein_g": 2.7, "fat_g": 0.3})
    _food(conn, 997102, "Cinnamon test", {"carbs_g": 80.0, "protein_g": 4.0, "fat_g": 1.2})
    _food(conn, 997103, "Vitamin test", {"vitamin_c_mg": 1000.0})
    inner = _db.recipe_create(conn, "Inner test", "", 1, "")
    _db.recipe_add_ingredient(conn, inner, 997101, "Rice test", 150.0, "150 g")
    outer = _db.recipe_create(conn, "Outer test", "", 1, "")
    _db.recipe_add_ingredient(conn, outer, 0, "Inner test", 1.0, "servings", ref_recipe_id=inner)
    m1 = _db.meal_create(conn, "Lunch", "2026-10-01")
    _db.meal_add_food(conn, m1, 997101, "Rice test", 150.0, "g")
    _db.meal_add_food(conn, m1, 997102, "Cinnamon test", 0.5, "g")
    _db.meal_add_food(conn, m1, 997103, "Vitamin test", 1.0, "g")
    m2 = _db.meal_create(conn, "Lunch", "2026-10-02")
    _db.meal_add_recipe(conn, m2, outer, "Outer test", 1.0)
    m3 = _db.meal_create(conn, "Lunch", "2026-09-01")   # outside the span
    _db.meal_add_food(conn, m3, 997101, "Rice test", 150.0, "g")


def test_foods_days_eaten_counts_foods_inside_recipes():
    with _db.get_db() as conn:
        _days_eaten_setup(conn)
        rows = {r["name"]: r for r in dq.foods_days_eaten(conn, "2026-10-02", 30)}
    assert (rows["Rice test"]["days"], rows["Rice test"]["recipe_days"]) == (2, 1)
    assert rows["Rice test"]["gi_gap_days"] == 2
    # A pinch is too little carbohydrate to leave glycemic load incomplete.
    assert rows["Cinnamon test"]["days"] == 1 and rows["Cinnamon test"]["gi_gap_days"] == 0
    assert rows["Vitamin test"]["carbs"] is None
    with _db.get_db() as conn:
        assert [r["name"] for r in dq.foods_days_eaten(conn, "2026-10-02", 1)] == ["Rice test"]


def test_days_eaten_section_on_db_check(client):
    with _db.get_db() as conn:
        _days_eaten_setup(conn)
    page = client.get("/food/cache/db-check?de_days=30&de_end=2026-10-02").text
    assert 'id="days-eaten" class="mt-4" open' in page
    assert "2026-09-03 to 2026-10-02" in page
    no_gi = page.split('id="days-eaten-no-gi"')[1].split('id="days-eaten-no-carbs"')[0]
    assert "Rice test" in no_gi and "Cinnamon test" not in no_gi
    no_carbs = page.split('id="days-eaten-no-carbs"')[1].split("</details>")[0]
    assert "Vitamin test" in no_carbs
    # Bad input falls back to the defaults instead of failing.
    assert client.get("/food/cache/db-check?de_days=abc&de_end=nope").status_code == 200


# --- One-click fixes for food data problems (Foods → 9) -------------------

def _fix_ids(n, **kw):
    return [f["id"] for i in dq.food_issues(n, **kw) for f in i["fixes"]]


def test_kilojoules_entered_as_calories_offers_the_conversion_first():
    n = {"calories": 1550.0, "protein_g": 10.0, "carbs_g": 60.0, "fat_g": 15.0}   # 4/4/9 = 415
    issue = dq.food_issues(n)[0]
    assert issue["kind"] == "calories_mismatch"
    assert [f["id"] for f in issue["fixes"]] == ["kj_to_kcal", "use_estimate"]
    assert issue["fixes"][0]["changes"] == {"calories": round(1550 / 4.184, 1)}
    assert "kilojoules" in issue["fixes"][0]["hint"]


def test_per_serving_calories_recognised_from_the_serving_weight():
    n = {"calories": 120.0, "protein_g": 10.0, "carbs_g": 60.0, "fat_g": 15.0}    # 415 per 100 g
    assert _fix_ids(n, serving_g=30.0) == ["per_serving", "use_estimate"]
    fix = dq.food_issues(n, serving_g=30.0)[0]["fixes"][0]
    assert fix["changes"] == {"calories": 400.0}
    # Without a serving weight there's no telling: only the estimate is offered.
    assert _fix_ids(n) == ["use_estimate"]


def test_missing_calories_offers_the_estimate_only_when_one_is_possible():
    assert _fix_ids({"protein_g": 10.0, "carbs_g": 20.0, "fat_g": 5.0}) == ["estimate_calories"]
    assert _fix_ids({"protein_g": 10.0}) == []


@pytest.mark.parametrize("n,fix_id,changes", [
    ({"carbs_g": 1333.33, "protein_g": 0, "fat_g": 0, "calories": 0}, "mg_to_g:carbs_g", {"carbs_g": 1.3333}),
    ({"carbs_g": 10, "sugar_g": 20}, "sugar_to_carbs", {"sugar_g": 10}),
    ({"fat_g": 40, "saturated_fat_g": 10, "mono_fat_g": 20, "poly_fat_g": 16.7}, "fat_from_parts", {"fat_g": 46.7}),
    ({"iron_mg": -1, "zinc_mg": -2}, "remove_negative", {"iron_mg": None, "zinc_mg": None}),
])
def test_impossible_values_offer_a_fix(n, fix_id, changes):
    fix = next(f for i in dq.food_issues(n) for f in i["fixes"] if f["id"] == fix_id)
    assert fix["changes"] == changes


def test_macros_over_100_g_offer_no_fix():
    """NuMa can't tell which of the three is wrong."""
    n = {"protein_g": 40, "carbs_g": 40, "fat_g": 40, "calories": 680}
    assert dq.food_issues(n)[0]["fixes"] == []


def test_a_fix_corrects_the_value_logs_why_and_counts_as_the_users_edit(client):
    n = {"calories": 1550.0, "protein_g": 10.0, "carbs_g": 60.0, "fat_g": 15.0}
    with _db.get_db() as conn:
        _food(conn, 997201, "Kilojoule test", n)
        rid = _db.recipe_create(conn, "Uses it", "", 1, "")
        _db.recipe_add_ingredient(conn, rid, 997201, "Kilojoule test", 100, "g")
    page = client.get("/food/cache/db-check").text
    assert "Convert from kilojoules" in page and "looks like kilojoules entered as calories" in page
    # The ways to fix it by hand: a USDA food (positive id) can be refreshed;
    # only a custom food gets Edit values.
    assert "/food/997201/review-incoming?source=usda" in page
    assert "/food/997201/fill-from?q=Kilojoule+test" in page
    assert "/food/custom-profiles/997201/edit" not in page
    resp = client.post("/food/997201/data-fix", data={"fix": "kj_to_kcal"}, follow_redirects=False)
    assert resp.status_code == 303 and resp.headers["location"].startswith("/food/cache/db-check?fixed=997201")
    page = client.get(resp.headers["location"]).text
    assert "Corrected" in page and "divided by 4.184" in page
    with _db.get_db() as conn:
        food = _db.get_cached_food(conn, 997201)
        assert json.loads(food["nutrients_json"])["calories"] == round(1550 / 4.184, 1)
        assert "calories" in (_db.food_edited_keys(conn, 997201) or [])     # yours, so Refresh won't take it back
        assert not dq.issues_for_food(conn, 997201)
        [c] = _db.food_corrections(conn, 997201)
        assert (c["key"], c["from"], c["to"]) == ("calories", 1550.0, round(1550 / 4.184, 1))
    detail = client.get("/food/997201").text
    assert 'id="corrections"' in detail and "divided by 4.184" in detail
    # The same fix again: the problem is gone, so nothing is written.
    resp = client.post("/food/997201/data-fix", data={"fix": "kj_to_kcal"}, follow_redirects=False)
    assert "fix_stale=1" in resp.headers["location"]


def test_a_correction_stops_showing_once_the_value_changes_again():
    with _db.get_db() as conn:
        _food(conn, 997202, "Sugar test", {"calories": 40, "protein_g": 0, "carbs_g": 10, "fat_g": 0, "sugar_g": 20})
        assert dq.apply_fix(conn, 997202, "sugar_to_carbs")
        assert [c["key"] for c in _db.food_corrections(conn, 997202)] == ["sugar_g"]
        _db.update_food_nutrients_partial(conn, 997202, {"sugar_g": 8.0})
        assert _db.food_corrections(conn, 997202) == []


def test_estimate_fix_marks_calories_estimated():
    with _db.get_db() as conn:
        _food(conn, 997203, "Mismatch test", {"calories": 900.0, "protein_g": 10.0, "carbs_g": 10.0, "fat_g": 1.0})
        assert dq.apply_fix(conn, 997203, "use_estimate")
        assert "calories" in _db.estimated_keys(conn, 997203)
        assert [i["kind"] for i in dq.issues_for_food(conn, 997203)] == ["calories_estimated"]
