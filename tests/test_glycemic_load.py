"""
Tests for numa_app/services/glycemic_load.py — GL aggregation used by the web
backend (backend.py): partial totals with the foods left out, recipes worked
out live from their ingredients, and day totals.
"""
import json

import pytest

import db as _db
from numa_app.services.glycemic_load import (GAP_NO_DATA, GAP_NO_GI, GAP_NO_RECIPE, GAP_NOT_WANTED,
                                             average_day_gl, combine_gl, day_gl_total,
                                             day_gl_totals, food_gl, gl_band, gl_band_caveat,
                                             gl_for_items, meal_gl, meal_line_items, recipe_gl)


@pytest.fixture()
def rice_food(db_conn):
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (1, "Rice", "SR Legacy", json.dumps({"carbs_g": 28.0}), "[]"),
    )
    db_conn.commit()
    return 1


def _food_item(fdc_id, name, amount):
    return {"kind": "food", "name": name, "amount": amount, "fdc_id": fdc_id, "recipe_id": None}


def _recipe_item(rid, name, servings):
    return {"kind": "recipe", "name": name, "amount": servings, "fdc_id": None, "recipe_id": rid}


def _annotate(conn, fdc_id, gi):
    _db.set_food_annotation(conn, fdc_id, gi_estimate=gi, gi_no_prompt=False, diaas_estimate=None,
                            diaas_no_prompt=False, prep_context=None)


def _add_food(conn, fdc_id, name, nutrients_json):
    conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (fdc_id, name, "SR Legacy", nutrients_json, "[]"),
    )


def _gaps(result):
    return [(g["name"], g["fdc_id"], g["recipe_id"], g["reason"]) for g in result["gaps"]]


def _ingredient(conn, rid, fdc_id, name, grams):
    _db.recipe_add_ingredient(conn, rid, fdc_id, name, grams, "g")


def _subrecipe(conn, rid, sub_id, name, servings):
    _db.recipe_add_ingredient(conn, rid, 0, name, servings, "serving", ref_recipe_id=sub_id)


class TestGlForItems:
    def test_food_with_gi_computes_gl(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        db_conn.commit()
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0)], db_conn)
        # carbs_g=28 per 100g * 70 GI / 100 = 19.6
        assert r == {"total": 19.6, "complete": True, "gaps": []}

    def test_food_without_gi_is_not_available_not_zero(self, db_conn, rice_food):
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0)], db_conn)
        assert r["total"] is None
        assert r["complete"] is False
        assert _gaps(r) == [("Rice", rice_food, None, GAP_NO_GI)]

    def test_partial_total_is_kept_and_marked_incomplete(self, db_conn, rice_food):
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        _annotate(db_conn, rice_food, 70.0)
        db_conn.commit()
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0), _food_item(2, "Bread", 100.0)], db_conn)
        assert r["total"] == 19.6
        assert r["complete"] is False
        assert _gaps(r) == [("Bread", 2, None, GAP_NO_GI)]

    def test_dont_prompt_food_is_reported_as_not_wanted(self, db_conn, rice_food):
        _db.set_food_annotation(db_conn, rice_food, gi_estimate=None, gi_no_prompt=True, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None)
        db_conn.commit()
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0)], db_conn)
        assert _gaps(r) == [("Rice", rice_food, None, GAP_NOT_WANTED)]

    def test_global_opt_out_reports_every_missing_gi_as_not_wanted(self, db_conn, rice_food):
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0)], db_conn, gi_opt_out=True)
        assert _gaps(r) == [("Rice", rice_food, None, GAP_NOT_WANTED)]

    def test_negligible_carbohydrate_without_gi_counts_as_zero(self, db_conn, rice_food):
        # 3 g of rice holds 0.84 g carbohydrate: under the 1 g floor.
        r = gl_for_items([_food_item(rice_food, "Rice", 3.0)], db_conn)
        assert r == {"total": 0.0, "complete": True, "gaps": []}
        # 4 g holds 1.12 g: now it matters.
        assert gl_for_items([_food_item(rice_food, "Rice", 4.0)], db_conn)["complete"] is False

    def test_food_with_no_carbs_value_contributes_zero(self, db_conn):
        _add_food(db_conn, 4, "Oil", json.dumps({"fat_g": 100.0}))
        db_conn.commit()
        assert gl_for_items([_food_item(4, "Oil", 100.0)], db_conn) == {"total": 0.0, "complete": True, "gaps": []}

    def test_food_with_no_nutrient_data_is_a_gap(self, db_conn):
        _add_food(db_conn, 3, "Mystery", "")
        _annotate(db_conn, 3, 50.0)
        db_conn.commit()
        assert _gaps(gl_for_items([_food_item(3, "Mystery", 100.0)], db_conn)) == [("Mystery", 3, None, GAP_NO_DATA)]

    def test_deleted_recipe_is_a_gap_under_the_line_item_name(self, db_conn):
        r = gl_for_items([_recipe_item(9999, "Deleted recipe", 1.0)], db_conn)
        assert _gaps(r) == [("Deleted recipe", None, 9999, GAP_NO_RECIPE)]

    def test_items_after_each_kind_of_gap_still_count(self, db_conn, rice_food):
        """A gap skips only its own item — `continue`, never `break`."""
        _annotate(db_conn, rice_food, 70.0)
        _add_food(db_conn, 2, "Unannotated", json.dumps({"carbs_g": 10.0}))
        _add_food(db_conn, 3, "No data", "")
        db_conn.commit()
        r = gl_for_items([
            _recipe_item(9999, "Gone", 1.0),
            _food_item(2, "Unannotated", 100.0),
            _food_item(3, "No data", 100.0),
            _food_item(rice_food, "Rice", 100.0),
        ], db_conn)
        assert r["total"] == 19.6
        assert [g[3] for g in _gaps(r)] == [GAP_NO_RECIPE, GAP_NO_GI, GAP_NO_DATA]


class TestRecipeGl:
    """A recipe's GL is worked out from its ingredients. It used to be read
    from recipes.gl_g, which nothing ever wrote, so every recipe — and every
    meal or day containing one — showed no GL at all."""

    def test_recipe_gl_per_serving_from_its_ingredients(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        rid = _db.recipe_create(db_conn, name="Rice bowl", description="", servings=2, instructions="")
        _ingredient(db_conn, rid, rice_food, "Rice", 200.0)
        db_conn.commit()
        # 200 g rice = GL 39.2 for the pot; one of two servings = 19.6
        assert recipe_gl(db_conn, rid)["total"] == 19.6
        assert recipe_gl(db_conn, rid, 2.0)["total"] == 39.2

    def test_recipe_in_a_meal_scales_by_servings_eaten(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        rid = _db.recipe_create(db_conn, name="Rice bowl", description="", servings=4, instructions="")
        _ingredient(db_conn, rid, rice_food, "Rice", 400.0)
        db_conn.commit()
        assert gl_for_items([_recipe_item(rid, "Rice bowl", 1.5)], db_conn)["total"] == pytest.approx(29.4)

    def test_sub_recipes_are_followed(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        base = _db.recipe_create(db_conn, name="Cooked rice", description="", servings=2, instructions="")
        _ingredient(db_conn, base, rice_food, "Rice", 200.0)
        dish = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
        _subrecipe(db_conn, dish, base, "Cooked rice", 1.0)
        db_conn.commit()
        assert recipe_gl(db_conn, dish)["total"] == 19.6

    def test_gap_inside_a_sub_recipe_reaches_the_top(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        base = _db.recipe_create(db_conn, name="Base", description="", servings=1, instructions="")
        _ingredient(db_conn, base, 2, "Bread", 50.0)
        dish = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
        _ingredient(db_conn, dish, rice_food, "Rice", 100.0)
        _subrecipe(db_conn, dish, base, "Base", 1.0)
        db_conn.commit()
        r = recipe_gl(db_conn, dish)
        assert r["total"] == 19.6 and r["complete"] is False
        assert _gaps(r) == [("Bread", 2, None, GAP_NO_GI)]

    def test_deleted_sub_recipe_is_a_gap(self, db_conn):
        dish = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(db_conn, dish, 0, "Old sauce", 1.0, "serving",
                                  ref_recipe_id=None, ref_recipe_deleted=True)
        db_conn.commit()
        assert _gaps(recipe_gl(db_conn, dish)) == [("Old sauce", None, None, GAP_NO_RECIPE)]

    def test_recipe_with_no_servings_counts_as_one(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        rid = _db.recipe_create(db_conn, name="A", description="", servings=1, instructions="")
        _ingredient(db_conn, rid, rice_food, "Rice", 100.0)
        db_conn.execute("UPDATE recipes SET servings = 0 WHERE id = ?", (rid,))
        db_conn.commit()
        assert recipe_gl(db_conn, rid)["total"] == 19.6

    def test_a_reference_cycle_stops(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        a = _db.recipe_create(db_conn, name="A", description="", servings=1, instructions="")
        b = _db.recipe_create(db_conn, name="B", description="", servings=1, instructions="")
        _ingredient(db_conn, a, rice_food, "Rice", 100.0)
        _subrecipe(db_conn, a, b, "B", 1.0)
        _subrecipe(db_conn, b, a, "A", 1.0)
        db_conn.commit()
        # B holds only A, which is not expanded a second time: just the rice.
        assert recipe_gl(db_conn, a)["total"] == 19.6

    def test_the_same_food_twice_is_listed_once(self, db_conn):
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        rid = _db.recipe_create(db_conn, name="A", description="", servings=1, instructions="")
        _ingredient(db_conn, rid, 2, "Bread", 50.0)
        _ingredient(db_conn, rid, 2, "Bread, toasted", 50.0)
        db_conn.commit()
        assert len(recipe_gl(db_conn, rid)["gaps"]) == 1


class TestFoodGl:
    def test_food_gl_from_given_nutrients(self):
        ann = {"gi_estimate": 70.0, "gi_no_prompt": 0}
        assert food_gl("Rice", 1, {"carbs_g": 28.0}, 50.0, ann)["total"] == 9.8

    def test_no_annotation_is_a_gap(self):
        r = food_gl("Rice", 1, {"carbs_g": 28.0}, 100.0, None)
        assert r["total"] is None and _gaps(r) == [("Rice", 1, None, GAP_NO_GI)]


class TestCombineGl:
    def test_sums_totals_and_merges_gaps(self):
        gap = {"name": "Bread", "fdc_id": 2, "recipe_id": None, "reason": GAP_NO_GI}
        r = combine_gl([
            {"total": 10.0, "complete": True, "gaps": []},
            {"total": 5.0, "complete": False, "gaps": [gap]},
            {"total": None, "complete": False, "gaps": [dict(gap)]},
        ])
        assert r == {"total": 15.0, "complete": False, "gaps": [gap]}


class TestMealLineItems:
    def test_food_and_recipe_items_map_to_the_compute_shape(self, db_conn, rice_food):
        rid = _db.recipe_create(db_conn, name="Bowl", description="", servings=2, instructions="")
        mid = _db.meal_create(db_conn, "Lunch", "2026-09-20")
        _db.meal_add_food(db_conn, mid, rice_food, "Rice", 100.0, "g")
        _db.meal_add_recipe(db_conn, mid, rid, "Bowl", 1.5)
        db_conn.commit()
        assert meal_line_items(db_conn, mid) == [
            {"kind": "food", "name": "Rice", "amount": 100.0, "fdc_id": rice_food, "recipe_id": None},
            {"kind": "recipe", "name": "Bowl", "amount": 1.5, "fdc_id": None, "recipe_id": rid},
        ]

class TestGlBand:
    """The per-serving and per-day scales are different, and using the wrong
    one labelled every real day "High" on the Daily Summary until 2026-09-27."""

    @pytest.mark.parametrize("total,expected", [
        (0.0, "Low"), (9.9, "Low"), (10.0, "Low"),
        (10.1, "Medium"), (15.0, "Medium"), (19.9, "Medium"),
        (20.0, "High"), (150.0, "High"),
    ])
    def test_serving_scale(self, total, expected):
        assert gl_band(total, "serving") == expected

    @pytest.mark.parametrize("total,expected", [
        (0.0, "Low"), (79.9, "Low"),
        (80.0, "Moderate"), (100.0, "Moderate"), (120.0, "Moderate"),
        (120.1, "High"), (300.0, "High"),
    ])
    def test_day_scale(self, total, expected):
        assert gl_band(total, "day") == expected

    def test_a_typical_day_total_is_not_high_on_the_day_scale(self):
        # The regression this banding exists to prevent: 95 is an ordinary day,
        # but reads "High" against the per-serving bands.
        assert gl_band(95.0, "serving") == "High"
        assert gl_band(95.0, "day") == "Moderate"

    def test_none_total_has_no_band(self):
        assert gl_band(None, "day") is None
        assert gl_band(None, "serving") is None

    def test_unknown_scope_falls_back_to_serving(self):
        assert gl_band(15.0, "nonsense") == gl_band(15.0, "serving")

    def test_only_the_day_scale_carries_a_caveat(self):
        assert gl_band_caveat("serving") is None
        assert gl_band_caveat("day") == (
            "Day-scale bands (under 80 low, 80-120 moderate, over 120 high) are a "
            "common convention, not a validated clinical target -- and a day's GL "
            "rises with how much you eat, so a larger or more active person will "
            "naturally run higher.")


@pytest.fixture()
def rice_with_gi(db_conn, rice_food):
    _db.set_food_annotation(db_conn, rice_food, gi_estimate=70.0, gi_no_prompt=False,
                            diaas_estimate=None, diaas_no_prompt=False, prep_context=None)
    db_conn.commit()
    return rice_food


class TestDayGlTotals:
    def test_sums_every_meal_on_the_date(self, db_conn, rice_with_gi):
        for name in ("Breakfast", "Lunch"):
            mid = _db.meal_create(db_conn, name, "2026-09-20")
            _db.meal_add_food(db_conn, mid, rice_with_gi, "Rice", 100.0, "g")
        db_conn.commit()
        assert day_gl_total(db_conn, "2026-09-20") == pytest.approx(39.2)

    def test_a_single_blocker_makes_the_whole_day_unknown(self, db_conn, rice_with_gi):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (2, "Bread", "SR Legacy", json.dumps({"carbs_g": 49.0}), "[]"),
        )
        mid = _db.meal_create(db_conn, "Lunch", "2026-09-21")
        _db.meal_add_food(db_conn, mid, rice_with_gi, "Rice", 100.0, "g")
        _db.meal_add_food(db_conn, mid, 2, "Bread", 100.0, "g")
        db_conn.commit()
        # Not a partial total — an unannotated food would understate the day.
        assert day_gl_total(db_conn, "2026-09-21") is None

    def test_a_recipe_in_a_meal_uses_its_gl(self, db_conn, rice_with_gi):
        rid = _db.recipe_create(db_conn, name="Bowl", description="", servings=2, instructions="")
        _db.recipe_add_ingredient(db_conn, rid, rice_with_gi, "Rice", 100.0, "g")
        mid = _db.meal_create(db_conn, "Lunch", "2026-09-25")
        _db.meal_add_recipe(db_conn, mid, rid, "Bowl", 1.0)
        db_conn.commit()
        assert day_gl_total(db_conn, "2026-09-25") == pytest.approx(9.8)

    def test_total_is_rounded_to_one_decimal(self, db_conn, rice_with_gi):
        mid = _db.meal_create(db_conn, "Snack", "2026-09-26")
        _db.meal_add_food(db_conn, mid, rice_with_gi, "Rice", 33.0, "g")
        db_conn.commit()
        # 28 * 0.33 * 0.70 = 6.468
        assert day_gl_total(db_conn, "2026-09-26") == 6.5

    def test_a_date_with_no_meals_is_unknown_not_zero(self, db_conn):
        assert day_gl_total(db_conn, "2026-09-22") is None

    def test_every_requested_date_appears_in_the_batch(self, db_conn, rice_with_gi):
        mid = _db.meal_create(db_conn, "Dinner", "2026-09-23")
        _db.meal_add_food(db_conn, mid, rice_with_gi, "Rice", 50.0, "g")
        db_conn.commit()
        totals = day_gl_totals(db_conn, ["2026-09-23", "2026-09-24"])
        assert totals == {"2026-09-23": pytest.approx(9.8), "2026-09-24": None}


class TestAverageDayGl:
    def test_skips_unknown_days_and_reports_the_count(self):
        avg, days = average_day_gl({"a": 100.0, "b": None, "c": 50.0})
        assert (avg, days) == (75.0, 2)

    def test_average_is_rounded_to_one_decimal(self):
        assert average_day_gl({"a": 1.0, "b": 2.0, "c": 2.0}) == (1.7, 3)

    def test_no_known_day_averages_to_nothing(self):
        assert average_day_gl({"a": None, "b": None}) == (None, 0)

    def test_empty_window(self):
        assert average_day_gl({}) == (None, 0)


class TestGlMutationGaps:
    """Survivors from the 2026-10-09 mutmut run on the rewritten module."""

    def test_exactly_one_gram_of_carbohydrate_needs_a_gi(self, db_conn):
        _add_food(db_conn, 5, "Exact", json.dumps({"carbs_g": 10.0}))
        db_conn.commit()
        # 10 g of a 10%-carb food = exactly 1.0 g: no longer negligible.
        r = gl_for_items([_food_item(5, "Exact", 10.0)], db_conn)
        assert _gaps(r) == [("Exact", 5, None, GAP_NO_GI)]

    def test_items_after_a_reference_cycle_still_count(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        a = _db.recipe_create(db_conn, name="A", description="", servings=1, instructions="")
        _subrecipe(db_conn, a, a, "A again", 1.0)
        _ingredient(db_conn, a, rice_food, "Rice", 100.0)
        db_conn.commit()
        assert recipe_gl(db_conn, a)["total"] == 19.6

    def test_gi_opt_out_reaches_foods_inside_sub_recipes(self, db_conn, rice_food):
        base = _db.recipe_create(db_conn, name="Base", description="", servings=1, instructions="")
        _ingredient(db_conn, base, rice_food, "Rice", 100.0)
        dish = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
        _subrecipe(db_conn, dish, base, "Base", 1.0)
        db_conn.commit()
        assert [g[3] for g in _gaps(recipe_gl(db_conn, dish, gi_opt_out=True))] == [GAP_NOT_WANTED]
        assert [g[3] for g in _gaps(recipe_gl(db_conn, dish))] == [GAP_NO_GI]

    def test_food_gl_honours_gi_opt_out(self):
        r = food_gl("Rice", 1, {"carbs_g": 28.0}, 100.0, None, gi_opt_out=True)
        assert r["gaps"][0]["reason"] == GAP_NOT_WANTED

    def test_meal_gl_honours_gi_opt_out_and_defaults_off(self, db_conn, rice_food):
        mid = _db.meal_create(db_conn, "Lunch", "2026-09-20")
        _db.meal_add_food(db_conn, mid, rice_food, "Rice", 100.0, "g")
        db_conn.commit()
        assert meal_gl(db_conn, mid)["gaps"][0]["reason"] == GAP_NO_GI
        assert meal_gl(db_conn, mid, gi_opt_out=True)["gaps"][0]["reason"] == GAP_NOT_WANTED

    def test_a_missing_amount_counts_as_nothing(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        db_conn.commit()
        item = _food_item(rice_food, "Rice", None)
        assert gl_for_items([item], db_conn)["total"] == 0.0
        rid = _db.recipe_create(db_conn, name="Bowl", description="", servings=1, instructions="")
        _ingredient(db_conn, rid, rice_food, "Rice", 100.0)
        db_conn.commit()
        assert gl_for_items([_recipe_item(rid, "Bowl", None)], db_conn)["total"] == 0.0

    def test_a_small_partial_total_is_still_shown(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        db_conn.commit()
        # 2 g rice: 0.56 g carbs x 0.70 = GL 0.39 — tiny but known, so "at least 0.4".
        r = gl_for_items([_food_item(rice_food, "Rice", 2.0), _food_item(2, "Bread", 50.0)], db_conn)
        assert r["total"] == 0.4 and r["complete"] is False

    def test_gaps_without_an_id_are_told_apart_by_name(self, db_conn):
        dish = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
        for name in ("Old sauce", "Old dressing", "Old sauce"):
            _db.recipe_add_ingredient(db_conn, dish, 0, name, 1.0, "serving",
                                      ref_recipe_id=None, ref_recipe_deleted=True)
        db_conn.commit()
        assert [g[0] for g in _gaps(recipe_gl(db_conn, dish))] == ["Old sauce", "Old dressing"]

    def test_a_deleted_recipe_is_named_by_its_number(self, db_conn):
        r = recipe_gl(db_conn, 9999)
        assert _gaps(r) == [("9999", None, 9999, GAP_NO_RECIPE)]

    def test_items_after_a_recipe_still_count(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        rid = _db.recipe_create(db_conn, name="Bowl", description="", servings=1, instructions="")
        _ingredient(db_conn, rid, rice_food, "Rice", 100.0)
        db_conn.commit()
        r = gl_for_items([_recipe_item(rid, "Bowl", 1.0), _food_item(rice_food, "Rice", 100.0)], db_conn)
        assert r["total"] == 39.2
