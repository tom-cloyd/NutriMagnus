"""
Tests for numa_app/services/whatif.py — non-destructive what-if analysis
across a set of meals (remove / add / replace / scale, at every depth).
"""
import hashlib
import json

import pytest

import db as _db
from numa_app.services import whatif as _wi
from numa_app.services.whatif import Edit

GROUPS = [
    ("Macronutrients", ["calories", "protein_g"]),
    ("Minerals", ["iron_mg", "iodine_mcg"]),
]

OATS, MILK, LENTILS, KELP = 1, 2, 3, 4


@pytest.fixture()
def data(db_conn):
    """Oats/almond milk/lentils/kelp cached. 'Oat base' (2 servings: 200 g
    oats + 500 g milk, complete weight) inside 'Bowl' (1 serving: 50 g oats +
    1 serving Oat base). Day 1: Bowl x1 and 100 g oats. Day 2: 200 g milk.
    Day 1 therefore holds 250 g oats and 250 g milk; day 2 holds 200 g milk."""
    foods = {
        OATS:    ("Oats", {"calories": 389.0, "protein_g": 13.0, "iron_mg": 4.0, "iodine_mcg": 0.0}),
        MILK:    ("Almond milk", {"calories": 15.0, "protein_g": 0.4, "iron_mg": 0.3, "iodine_mcg": 0.0}),
        LENTILS: ("Lentils", {"calories": 116.0, "protein_g": 9.0, "iron_mg": 3.3}),
        KELP:    ("Kelp", {"calories": 43.0, "iodine_mcg": 1000.0, "polyphenols_mg": 50.0}),
    }
    for fdc_id, (name, nuts) in foods.items():
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (fdc_id, name, "SR Legacy", json.dumps(nuts), "[]"),
        )
    sub = _db.recipe_create(db_conn, name="Oat base", description="", servings=2, instructions="",
                            total_weight=700.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, sub, OATS, "Oats", 200.0, "g")
    _db.recipe_add_ingredient(db_conn, sub, MILK, "Almond milk", 500.0, "g")
    bowl = _db.recipe_create(db_conn, name="Bowl", description="", servings=1, instructions="",
                             total_weight=400.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, bowl, OATS, "Oats", 50.0, "g")
    _db.recipe_add_ingredient(db_conn, bowl, 0, "Oat base", 1.0, "serving", ref_recipe_id=sub)
    soup = _db.recipe_create(db_conn, name="Lentil soup", description="", servings=2, instructions="",
                             total_weight=300.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, soup, LENTILS, "Lentils", 300.0, "g")
    m1 = _db.meal_create(db_conn, "Breakfast", "2026-01-01")
    _db.meal_add_recipe(db_conn, m1, bowl, "Bowl", 1.0)
    m2 = _db.meal_create(db_conn, "Snack", "2026-01-01")
    _db.meal_add_food(db_conn, m2, OATS, "Oats", 100.0, "g")
    m3 = _db.meal_create(db_conn, "Drink", "2026-01-02")
    _db.meal_add_food(db_conn, m3, MILK, "Almond milk", 200.0, "g")
    db_conn.commit()
    meals = [dict(r) for r in db_conn.execute("SELECT * FROM meals ORDER BY id")]
    return {"sub": sub, "bowl": bowl, "soup": soup, "meals": meals, "m1": m1, "m2": m2, "m3": m3}


def run(data, edits):
    with _db.get_db() as conn:
        return _wi.evaluate_meals(conn, data["meals"], edits, groups=GROUPS)


def row(result, key):
    for sec in result["sections"]:
        for r in sec["rows"]:
            if r["key"] == key:
                return r
    return None


class TestNoEdits:
    def test_before_equals_after(self, data):
        res = run(data, [])
        for sec in res["sections"]:
            for r in sec["rows"]:
                assert r["after"] == pytest.approx(r["before"])
                assert not r["changed"]

    def test_daily_average_is_over_logged_days(self, data):
        # Day 1: 250 g oats + 250 g milk; day 2: 200 g milk.
        protein = row(run(data, []), "protein_g")
        day1 = 250 * 0.13 + 250 * 0.004
        day2 = 200 * 0.004
        assert protein["before"] == pytest.approx((day1 + day2) / 2)

    def test_meal_nutrients_matches_meal_page_totals(self, data):
        from web.backend import _meal_expand_for_diaas
        with _db.get_db() as conn:
            for m in data["meals"]:
                _, page_totals, _ = _meal_expand_for_diaas(m["id"], conn)
                mine = _wi.meal_nutrients(m["id"], conn)
                assert mine.keys() == page_totals.keys()
                for k in mine:
                    assert mine[k] == pytest.approx(page_totals[k])


class TestOperations:
    def test_remove_reaches_every_depth(self, data):
        res = run(data, [Edit("remove", ("food", OATS))])
        protein = row(res, "protein_g")
        day1 = 250 * 0.004       # only the milk left
        day2 = 200 * 0.004
        assert protein["after"] == pytest.approx((day1 + day2) / 2)
        assert res["edits"][0]["meals"] == 2 and res["edits"][0]["days"] == 1

    def test_replace_same_weight(self, data):
        res = run(data, [Edit("replace", ("food", OATS), ("food", LENTILS))])
        protein = row(res, "protein_g")
        day1 = 250 * 0.09 + 250 * 0.004
        assert protein["after"] == pytest.approx((day1 + 200 * 0.004) / 2)

    def test_replace_stated_amount_at_each_place(self, data):
        # Three places hold oats on day 1: the snack, Bowl, and Oat base.
        res = run(data, [Edit("replace", ("food", OATS), ("food", LENTILS),
                              amount=10.0, unit="g", basis="stated")])
        protein = row(res, "protein_g")
        # Bowl and snack: 10 g each; inside half a batch of Oat base: 10 g * 0.5.
        day1 = (10 + 10 + 5) * 0.09 + 250 * 0.004
        assert protein["after"] == pytest.approx((day1 + 200 * 0.004) / 2)

    def test_replace_recipe_by_servings(self, data):
        res = run(data, [Edit("replace", ("recipe", data["bowl"]), ("recipe", data["sub"]), basis="servings")])
        # Day 1: snack oats 100 g + one serving of Oat base (100 g oats, 250 g milk).
        protein = row(res, "protein_g")
        day1 = 200 * 0.13 + 250 * 0.004
        assert protein["after"] == pytest.approx((day1 + 200 * 0.004) / 2)

    def test_replace_food_with_recipe_by_weight(self, data):
        # Every gram of milk becomes a gram of Lentil soup (all lentils).
        res = run(data, [Edit("replace", ("food", MILK), ("recipe", data["soup"]))])
        iron = row(res, "iron_mg")
        day1 = 250 * 0.04 + 250 * 0.033
        day2 = 200 * 0.033
        assert iron["after"] == pytest.approx((day1 + day2) / 2)

    def test_replacement_recipe_containing_target_is_refused(self, data):
        with pytest.raises(_wi.WhatIfError, match="round in circles"):
            run(data, [Edit("replace", ("food", MILK), ("recipe", data["sub"]))])

    def test_scale(self, data):
        res = run(data, [Edit("scale", ("food", OATS), amount=0.5)])
        protein = row(res, "protein_g")
        day1 = 125 * 0.13 + 250 * 0.004
        assert protein["after"] == pytest.approx((day1 + 200 * 0.004) / 2)

    def test_add_lands_once_on_each_logged_day_only(self, data):
        res = run(data, [Edit("add", ("food", KELP), amount=2.0)])
        iodine = row(res, "iodine_mcg")
        # 20 mcg on each of the 2 logged days, nothing for unlogged days.
        assert iodine["after"] - iodine["before"] == pytest.approx(20.0)
        assert res["edits"][0]["days"] == 2

    def test_add_recipe_by_servings(self, data):
        res = run(data, [Edit("add", ("recipe", data["sub"]), amount=1.0, unit="servings")])
        protein = row(res, "protein_g")
        assert protein["delta"] == pytest.approx(100 * 0.13 + 250 * 0.004)

    def test_remove_plus_add_is_a_substitution_on_every_day(self, data):
        res = run(data, [Edit("remove", ("food", MILK)), Edit("add", ("food", LENTILS), amount=100.0)])
        iron = row(res, "iron_mg")
        day1 = 250 * 0.04 + 100 * 0.033
        day2 = 100 * 0.033
        assert iron["after"] == pytest.approx((day1 + day2) / 2)

    def test_edit_that_matches_nothing_is_reported(self, data):
        res = run(data, [Edit("remove", ("food", KELP))])
        assert res["edits"][0]["meals"] == 0


class TestDataQuality:
    def test_missing_value_on_added_food_is_flagged_not_silent(self, data):
        res = run(data, [Edit("add", ("food", LENTILS), amount=100.0)])
        assert row(res, "iodine_mcg")["unknown"] == ["Lentils"]
        assert row(res, "iron_mg")["unknown"] == []

    def test_unapplied_replacement_is_not_flagged(self, data):
        res = run(data, [Edit("replace", ("food", KELP), ("food", LENTILS))])
        assert row(res, "iodine_mcg")["unknown"] == []

    def test_new_nutrient_key_shows_under_other(self, data):
        res = run(data, [Edit("add", ("food", KELP), amount=2.0)])
        other = [s for s in res["sections"] if s["name"] == "Other"]
        assert other and other[0]["rows"][0]["key"] == "polyphenols_mg"

    def test_targets_and_days_unmet(self, data):
        res = run(data, [])
        iron = row(res, "iron_mg")
        assert iron["target"] and iron["days_unmet_before"] is not None
        res2 = run(data, [Edit("add", ("food", LENTILS), amount=1000.0)])
        iron2 = row(res2, "iron_mg")
        assert iron2["days_unmet_after"] < iron2["days_unmet_before"] or iron2["days_unmet_before"] == 0
        assert iron2["status_after"] == "met"


class TestValidation:
    def test_replacement_containing_target_is_refused(self, data):
        with pytest.raises(_wi.WhatIfError, match="round in circles"):
            run(data, [Edit("replace", ("food", OATS), ("recipe", data["bowl"]))])

    def test_same_servings_needs_two_recipes(self, data):
        with pytest.raises(_wi.WhatIfError, match="recipe for recipe"):
            run(data, [Edit("replace", ("food", OATS), ("food", LENTILS), basis="servings")])

    def test_food_cannot_be_added_in_servings(self, data):
        with pytest.raises(_wi.WhatIfError, match="not servings"):
            run(data, [Edit("add", ("food", KELP), amount=1.0, unit="servings")])

    def test_recipe_without_serving_weight_by_weight_is_refused(self, data, db_conn):
        bare = _db.recipe_create(db_conn, name="Bare", description="", servings=1, instructions="")
        db_conn.commit()
        with pytest.raises(_wi.WhatIfError, match="serving weight"):
            run(data, [Edit("replace", ("food", MILK), ("recipe", bare))])


def test_never_writes(data, db_path):
    digest = hashlib.sha256(db_path.read_bytes()).hexdigest()
    with _db.get_db() as conn:
        before_changes = conn.total_changes
        _wi.evaluate_meals(conn, data["meals"], [
            Edit("remove", ("food", OATS)),
            Edit("replace", ("food", MILK), ("recipe", data["soup"])),
            Edit("scale", ("recipe", data["bowl"]), amount=2.0),
            Edit("add", ("food", KELP), amount=2.0),
        ], groups=GROUPS)
        assert conn.total_changes == before_changes
    assert hashlib.sha256(db_path.read_bytes()).hexdigest() == digest
