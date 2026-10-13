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
                                             gl_for_items, meal_gl, meal_line_items, recipe_gl,
                                             available_carbs_100g, gi_band, gi_near_band, looks_uncooked)
from numa_app.services.food_ids import _SYNTHETIC_ID_RANGES


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
        assert r == {"total": 19.6, "complete": True, "gaps": [],
                     "carbs_with_gi_g": 28.0, "carbs_g": 28.0, "coverage_pct": 100, "impaired": [],
                     "mixture": True, "gi": 70, "gi_band": "High", "gi_near": "Medium",
                     "gi_too_little_carb": False, "uncooked": []}

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

    def test_coverage_is_share_of_carbs_from_foods_with_gi(self, db_conn, rice_food):
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        _add_food(db_conn, 3, "Toast", json.dumps({"carbs_g": 50.0}))
        _annotate(db_conn, rice_food, 70.0)
        _db.set_food_annotation(db_conn, 3, gi_estimate=None, gi_no_prompt=True, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None)
        db_conn.commit()
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0), _food_item(2, "Bread", 100.0),
                          _food_item(3, "Toast", 100.0)], db_conn)
        # 28 g with GI of 28 + 49 counted; Toast's GI is "not wanted", so left out.
        assert (r["carbs_with_gi_g"], r["carbs_g"], r["coverage_pct"]) == (28.0, 77.0, 36)

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
        assert r == {"total": 0.0, "complete": True, "gaps": [], "carbs_with_gi_g": 0.0, "carbs_g": 0.0, "coverage_pct": None, "impaired": [],
                     "mixture": True, "gi": None, "gi_band": None, "gi_near": None, "gi_too_little_carb": False, "uncooked": []}
        # 4 g holds 1.12 g: now it matters.
        assert gl_for_items([_food_item(rice_food, "Rice", 4.0)], db_conn)["complete"] is False

    def test_food_with_no_carbs_value_contributes_zero(self, db_conn):
        _add_food(db_conn, 4, "Oil", json.dumps({"fat_g": 100.0}))
        db_conn.commit()
        assert gl_for_items([_food_item(4, "Oil", 100.0)], db_conn) == {"total": 0.0, "complete": True, "gaps": [], "carbs_with_gi_g": 0.0, "carbs_g": 0.0, "coverage_pct": None, "impaired": [],
                     "mixture": True, "gi": None, "gi_band": None, "gi_near": None, "gi_too_little_carb": False, "uncooked": []}

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


class TestGlForLeaves:
    def test_matches_gl_for_items(self, db_conn, rice_food):
        from numa_app.services.glycemic_load import gl_for_leaves
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        _annotate(db_conn, rice_food, 70.0)
        db_conn.commit()
        leaves = [{"food_name": "Rice", "fdc_id": rice_food, "nutrients_100g": {"carbs_g": 28.0}, "grams": 100.0},
                  {"food_name": "Bread", "fdc_id": 2, "nutrients_100g": {"carbs_g": 49.0}, "grams": 100.0}]
        r = gl_for_leaves(leaves, db_conn)
        assert r == gl_for_items([_food_item(rice_food, "Rice", 100.0), _food_item(2, "Bread", 100.0)], db_conn)
        assert r["coverage_pct"] == 36


class TestImpairedPopulation:
    IMPAIRED_SRC = ("Atkinson 2021 international GI tables, Supplemental Table 1: \u201cRice\u201d"
                    " \u00b7 Impaired glucose tolerance (Type 2, n=9)")

    def test_counted_food_measured_in_impaired_is_named(self, db_conn, rice_food):
        _db.set_food_annotation(db_conn, rice_food, gi_estimate=70.0, gi_no_prompt=False, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None, gi_source=self.IMPAIRED_SRC)
        db_conn.commit()
        assert gl_for_items([_food_item(rice_food, "Rice", 100.0)], db_conn)["impaired"] == ["Rice"]
        # A negligible amount isn't worth a warning.
        assert gl_for_items([_food_item(rice_food, "Rice", 3.0)], db_conn)["impaired"] == []

    def test_normal_population_is_not_named(self, db_conn, rice_food):
        _db.set_food_annotation(db_conn, rice_food, gi_estimate=70.0, gi_no_prompt=False, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None,
                                gi_source="Atkinson 2021 ...: \u201cRice\u201d \u00b7 Normal glucose tolerance")
        db_conn.commit()
        assert gl_for_items([_food_item(rice_food, "Rice", 100.0)], db_conn)["impaired"] == []

    def test_combine_keeps_each_name_once(self):
        r = combine_gl([{"total": 1.0, "complete": True, "gaps": [], "impaired": ["Rice"]},
                        {"total": 1.0, "complete": True, "gaps": [], "impaired": ["Rice", "Bread"]}])
        assert r["impaired"] == ["Rice", "Bread"]


class TestCombineGl:
    def test_coverage_sums_carbs(self):
        r = combine_gl([
            {"total": 10.0, "complete": True, "gaps": [], "carbs_with_gi_g": 20.0, "carbs_g": 20.0},
            {"total": 5.0, "complete": True, "gaps": [], "carbs_with_gi_g": 10.0, "carbs_g": 40.0},
        ])
        assert r["coverage_pct"] == 50

    def test_sums_totals_and_merges_gaps(self):
        gap = {"name": "Bread", "fdc_id": 2, "recipe_id": None, "reason": GAP_NO_GI}
        r = combine_gl([
            {"total": 10.0, "complete": True, "gaps": []},
            {"total": 5.0, "complete": False, "gaps": [gap]},
            {"total": None, "complete": False, "gaps": [dict(gap)]},
        ])
        assert r["total"] == 15.0 and r["complete"] is False and r["gaps"] == [gap]


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


class TestGlTargetOptions:
    def test_scaled_fixed_and_step_down(self):
        from numa_app.services.glycemic_load import gl_target_options
        o = gl_target_options(2400.0, 100.0, 12)
        assert o["scaled"] == 96 and o["fixed"] == 80
        assert o["step_down_range"] == (80, 90) and o["step_down"] == 85

    def test_missing_inputs_withhold_options(self):
        from numa_app.services.glycemic_load import gl_target_options
        o = gl_target_options(None, 100.0, 6)        # no calories; too few days
        assert o["scaled"] is None and o["step_down"] is None and o["fixed"] == 80


def _source_id(key):
    """A synthetic fdc_id in `key`'s outside-source range."""
    return next(start for k, start, _end, _label in _SYNTHETIC_ID_RANGES if k == key)


class TestAvailableCarbs:
    """GI and GL are defined on available carbohydrate. USDA's carbs_g is total
    carbohydrate by difference, fiber included; CoFID, AFCD and CIQUAL already
    report available carbohydrate."""

    def test_total_carbohydrate_sources_have_fiber_taken_off(self):
        n = {"carbs_g": 60.0, "fiber_g": 15.0}
        assert available_carbs_100g(n, 171477) == 45.0      # USDA
        assert available_carbs_100g(n, -4) == 45.0          # user-drafted
        assert available_carbs_100g(n, None) == 45.0
        for key in ("cnf", "off"):
            assert available_carbs_100g(n, _source_id(key)) == 45.0

    @pytest.mark.parametrize("key", ["cofid", "afcd", "ciqual"])
    def test_available_carbohydrate_sources_are_used_as_stored(self, key):
        assert available_carbs_100g({"carbs_g": 60.0, "fiber_g": 15.0}, _source_id(key)) == 60.0

    def test_never_below_zero_and_missing_fiber_takes_nothing_off(self):
        assert available_carbs_100g({"carbs_g": 5.0, "fiber_g": 8.0}, 1) == 0.0
        assert available_carbs_100g({"carbs_g": 28.0}, 1) == 28.0
        assert available_carbs_100g({}, 1) == 0.0

    def test_gl_counts_available_carbohydrate(self, db_conn):
        _add_food(db_conn, 5, "Beans", json.dumps({"carbs_g": 60.0, "fiber_g": 34.0}))
        _annotate(db_conn, 5, 27.0)
        db_conn.commit()
        r = gl_for_items([_food_item(5, "Beans", 100.0)], db_conn)
        # (60 - 34) x 27 / 100 = 7.02, not 60 x 27 / 100 = 16.2
        assert (r["total"], r["carbs_g"]) == (7.0, 26.0)

    def test_food_gl_takes_the_source_from_its_id(self):
        ann = {"gi_estimate": 50.0, "gi_no_prompt": 0}
        n = {"carbs_g": 40.0, "fiber_g": 10.0}
        assert food_gl("x", 1, n, 100.0, ann)["total"] == 15.0
        assert food_gl("x", _source_id("cofid"), n, 100.0, ann)["total"] == 20.0


class TestMixtureGi:
    """The estimated GI of a meal or recipe: carbohydrate-weighted mean of its
    foods' GIs (100 x GL / carbohydrate with a GI), with its conditions."""

    def _two_foods(self, db_conn, sugar_g=4.0, milk_g=1.5):
        _add_food(db_conn, 11, "Sugar", json.dumps({"carbs_g": 100.0}))
        _add_food(db_conn, 12, "Milk", json.dumps({"carbs_g": 100.0}))
        _annotate(db_conn, 11, 65.0)
        _annotate(db_conn, 12, 39.0)
        db_conn.commit()
        return gl_for_items([_food_item(11, "Sugar", sugar_g), _food_item(12, "Milk", milk_g)], db_conn)

    def test_weighted_by_carbohydrate(self, db_conn):
        r = self._two_foods(db_conn, 40.0, 15.0)
        # (40 x 65 + 15 x 39) / 55 = 57.9
        assert (r["gi"], r["gi_band"], r["gi_near"]) == (58, "Medium", "Low")

    def test_not_given_under_ten_grams_of_carbohydrate(self, db_conn):
        # the coffee example: 4 g sugar + 1.5 g lactose
        r = self._two_foods(db_conn)
        assert r["gi"] is None and r["gi_too_little_carb"] is True
        assert r["total"] == 3.2        # GL is still given

    def test_ten_grams_is_enough(self, db_conn):
        r = self._two_foods(db_conn, 10.0, 0.0)
        assert r["gi"] == 65 and r["gi_too_little_carb"] is False

    def test_partial_coverage_describes_only_the_foods_with_a_gi(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        db_conn.commit()
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0), _food_item(2, "Bread", 100.0)], db_conn)
        assert (r["gi"], r["coverage_pct"]) == (70, 36)

    def test_nothing_with_a_gi_gives_no_figure_and_no_floor_note(self, db_conn, rice_food):
        r = gl_for_items([_food_item(rice_food, "Rice", 100.0)], db_conn)
        assert r["gi"] is None and r["gi_too_little_carb"] is False

    def test_a_single_food_is_not_a_mixture(self):
        r = food_gl("Rice", 1, {"carbs_g": 28.0}, 100.0, {"gi_estimate": 70.0, "gi_no_prompt": 0})
        assert r["mixture"] is False and r["gi"] == 70

    def test_combined_day_gi(self):
        r = combine_gl([
            {"total": 14.0, "complete": True, "gaps": [], "carbs_with_gi_g": 20.0, "carbs_g": 20.0},
            {"total": 12.0, "complete": True, "gaps": [], "carbs_with_gi_g": 30.0, "carbs_g": 30.0},
        ])
        assert r["gi"] == 52

    @pytest.mark.parametrize("gi, band, near", [
        (40, "Low", None), (50, "Low", None), (51, "Low", "Medium"), (55, "Low", "Medium"),
        (56, "Medium", "Low"), (60, "Medium", "Low"), (61, "Medium", None), (64, "Medium", None),
        (65, "Medium", "High"), (69, "Medium", "High"), (70, "High", "Medium"),
        (74, "High", "Medium"), (75, "High", None), (None, None, None),
    ])
    def test_bands_and_closeness(self, gi, band, near):
        assert (gi_band(gi), gi_near_band(gi)) == (band, near)


class TestUncookedIngredients:
    """A recipe ingredient whose name says raw, dry, uncooked or flour may not
    be eaten in the form its GI describes; each recipe can be marked as eaten
    as listed (recipes.gi_as_eaten) to stop the flag."""

    @pytest.mark.parametrize("name, expected", [
        ("Wheat flour, white, all-purpose", True),
        ("Pasta, dry, unenriched", True),
        ("Rice, white, long-grain, regular, raw, enriched", True),
        ("Oats, uncooked", True),
        ("Apricots, dried, sulfured, uncooked", False),
        ("Rice, white, cooked", False),
        ("Strawberry jam", False),
        ("Drywall", False),
        (None, False),
    ])
    def test_name_match(self, name, expected):
        assert looks_uncooked(name) is expected

    def _recipe(self, db_conn, name="Flatbread"):
        _add_food(db_conn, 21, "Wheat flour, white", json.dumps({"carbs_g": 76.0}))
        _add_food(db_conn, 22, "Rice, cooked", json.dumps({"carbs_g": 28.0}))
        _annotate(db_conn, 21, 70.0)
        _annotate(db_conn, 22, 70.0)
        rid = _db.recipe_create(db_conn, name=name, description="", servings=1, instructions="")
        _ingredient(db_conn, rid, 21, "Wheat flour, white", 50.0)
        _ingredient(db_conn, rid, 22, "Rice, cooked", 50.0)
        db_conn.commit()
        return rid

    def test_recipe_flags_its_uncooked_ingredients(self, db_conn):
        rid = self._recipe(db_conn)
        assert recipe_gl(db_conn, rid)["uncooked"] == [
            {"name": "Wheat flour, white", "fdc_id": 21, "recipe_id": rid, "recipe": "Flatbread"}]

    def test_marked_as_eaten_stops_the_flag(self, db_conn):
        rid = self._recipe(db_conn)
        _db.set_recipe_gi_as_eaten(db_conn, rid, True)
        r = recipe_gl(db_conn, rid)
        assert r["uncooked"] == [] and r["gi"] == 70

    def test_foods_eaten_directly_in_a_meal_are_not_flagged(self, db_conn):
        _add_food(db_conn, 23, "Apples, raw", json.dumps({"carbs_g": 14.0}))
        _annotate(db_conn, 23, 36.0)
        db_conn.commit()
        assert gl_for_items([_food_item(23, "Apples, raw", 150.0)], db_conn)["uncooked"] == []

    def test_flag_reaches_a_meal_through_its_recipe(self, db_conn):
        rid = self._recipe(db_conn)
        r = gl_for_items([_recipe_item(rid, "Flatbread", 1.0)], db_conn)
        assert [u["name"] for u in r["uncooked"]] == ["Wheat flour, white"]

    def test_each_recipe_mark_covers_only_its_own_ingredients(self, db_conn):
        sub = self._recipe(db_conn)
        dish = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
        _subrecipe(db_conn, dish, sub, "Flatbread", 1.0)
        _db.set_recipe_gi_as_eaten(db_conn, dish, True)
        db_conn.commit()
        assert [u["recipe"] for u in recipe_gl(db_conn, dish)["uncooked"]] == ["Flatbread"]

    def test_negligible_or_gi_less_ingredients_are_not_flagged(self, db_conn):
        _add_food(db_conn, 24, "Flour, no GI", json.dumps({"carbs_g": 76.0}))
        rid = self._recipe(db_conn)
        _ingredient(db_conn, rid, 24, "Flour, no GI", 50.0)
        _ingredient(db_conn, rid, 21, "Wheat flour, white", 0.5)   # 0.38 g carbs, already listed anyway
        db_conn.commit()
        assert [u["name"] for u in recipe_gl(db_conn, rid)["uncooked"]] == ["Wheat flour, white"]

    def test_combine_keeps_each_flag_once(self, db_conn):
        rid = self._recipe(db_conn)
        one = gl_for_items([_recipe_item(rid, "Flatbread", 1.0)], db_conn)
        assert len(combine_gl([one, one])["uncooked"]) == 1


class TestGlMutationGaps20261013:
    """Gaps found by the 2026-10-13 mutation run (after the available-
    carbohydrate and estimated-GI changes)."""

    def test_uncooked_and_impaired_notes_start_at_exactly_one_gram(self, db_conn):
        _add_food(db_conn, 31, "Wheat flour, white", json.dumps({"carbs_g": 100.0}))
        _db.set_food_annotation(db_conn, 31, gi_estimate=70.0, gi_no_prompt=False, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None,
                                gi_source="Atkinson 2021 — Impaired glucose tolerance: x")
        rid = _db.recipe_create(db_conn, name="Pinch", description="", servings=1, instructions="")
        _ingredient(db_conn, rid, 31, "Wheat flour, white", 1.0)      # exactly 1 g carbohydrate
        db_conn.commit()
        r = recipe_gl(db_conn, rid)
        assert [u["name"] for u in r["uncooked"]] == ["Wheat flour, white"]
        assert r["impaired"] == ["Wheat flour, white"]

    def test_under_one_gram_with_a_gi_still_gives_a_gi(self, db_conn, rice_food):
        # 0.5 g sugar (GI 65) in a meal whose other 10 g carbohydrate has no GI
        _add_food(db_conn, 11, "Sugar", json.dumps({"carbs_g": 100.0}))
        _annotate(db_conn, 11, 65.0)
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 50.0}))
        db_conn.commit()
        r = gl_for_items([_food_item(11, "Sugar", 0.5), _food_item(2, "Bread", 20.0)], db_conn)
        assert (r["gi"], r["coverage_pct"]) == (65, 5)

    def test_under_one_gram_in_all_is_too_little_and_has_coverage(self, db_conn):
        _add_food(db_conn, 11, "Sugar", json.dumps({"carbs_g": 100.0}))
        _annotate(db_conn, 11, 65.0)
        db_conn.commit()
        r = gl_for_items([_food_item(11, "Sugar", 0.5)], db_conn)
        assert (r["gi"], r["gi_too_little_carb"], r["coverage_pct"]) == (None, True, 100)

    def test_carbohydrate_is_rounded_to_a_tenth(self, db_conn):
        _add_food(db_conn, 11, "Sugar", json.dumps({"carbs_g": 100.0}))
        _annotate(db_conn, 11, 65.0)
        db_conn.commit()
        r = gl_for_items([_food_item(11, "Sugar", 12.345)], db_conn)
        assert (r["carbs_with_gi_g"], r["carbs_g"]) == (12.3, 12.3)

    def test_gl_for_leaves_passes_name_source_and_opt_out_on(self, db_conn):
        from numa_app.services.glycemic_load import gl_for_leaves
        cofid = _source_id("cofid")
        _add_food(db_conn, cofid, "Porridge oats", json.dumps({"carbs_g": 60.0, "fiber_g": 9.0}))
        _db.set_food_annotation(db_conn, cofid, gi_estimate=50.0, gi_no_prompt=False, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None,
                                gi_source="Atkinson 2021 — Impaired glucose tolerance: x")
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 50.0}))
        db_conn.commit()
        leaf = {"food_name": "Porridge oats", "fdc_id": cofid, "grams": 100.0,
                "nutrients_100g": {"carbs_g": 60.0, "fiber_g": 9.0}}
        r = gl_for_leaves([leaf], db_conn)
        assert (r["total"], r["impaired"]) == (30.0, ["Porridge oats"])   # fiber not taken off
        bread = {"food_name": "Bread", "fdc_id": 2, "grams": 100.0, "nutrients_100g": {"carbs_g": 50.0}}
        assert gl_for_leaves([bread], db_conn, gi_opt_out=True)["gaps"][0]["reason"] == GAP_NOT_WANTED

    def test_food_gl_names_an_impaired_value(self):
        ann = {"gi_estimate": 50.0, "gi_no_prompt": 0, "gi_source": "Impaired glucose tolerance"}
        assert food_gl("Oats", 1, {"carbs_g": 60.0}, 100.0, ann)["impaired"] == ["Oats"]

    def test_a_zero_gram_ingredient_counts_as_nothing(self, db_conn, rice_food):
        _annotate(db_conn, rice_food, 70.0)
        rid = _db.recipe_create(db_conn, name="Bowl", description="", servings=1, instructions="")
        _ingredient(db_conn, rid, rice_food, "Rice", 0.0)
        db_conn.commit()
        assert recipe_gl(db_conn, rid)["total"] == 0.0


class TestGlTargetOptionsExact:
    def test_every_field(self):
        from numa_app.services.glycemic_load import gl_target_options
        assert gl_target_options(2012.75, 100.0, 7) == {
            "scaled": 81, "fixed": 80, "step_down": 85, "step_down_range": (80, 90),
            "recent_avg": 100.0, "recent_days": 7}


class TestGlTargetStatus:
    """A day's GL against the profile's daily target (rda_status "limit":
    met <=80%, near 80-100%, over >100%)."""

    @pytest.mark.parametrize("total, complete, expected", [
        (60.0, True,  {"target": 80.0, "pct": 75,  "status": "met",     "over": False}),
        (72.0, True,  {"target": 80.0, "pct": 90,  "status": "near",    "over": False}),
        (80.0, True,  {"target": 80.0, "pct": 100, "status": "near",    "over": False}),
        (88.0, True,  {"target": 80.0, "pct": 110, "status": "over",    "over": True}),
        (60.0, False, {"target": 80.0, "pct": 75,  "status": "unknown", "over": False}),
        (88.0, False, {"target": 80.0, "pct": 110, "status": "over",    "over": True}),
    ])
    def test_classification(self, total, complete, expected):
        from numa_app.services.glycemic_load import gl_target_status
        assert gl_target_status(total, complete, 80.0) == expected

    @pytest.mark.parametrize("total, target", [(50.0, None), (50.0, 0.0), (50.0, -5.0), (None, 80.0)])
    def test_nothing_to_compare(self, total, target):
        from numa_app.services.glycemic_load import gl_target_status
        assert gl_target_status(total, True, target) is None

    def test_rounds_the_percentage(self):
        from numa_app.services.glycemic_load import gl_target_status
        assert gl_target_status(50.0, True, 60.0)["pct"] == 83


class TestDayGl:
    def test_keeps_a_partial_total_with_its_gaps(self, db_conn, rice_with_gi):
        from numa_app.services.glycemic_load import day_gl
        _add_food(db_conn, 2, "Bread", json.dumps({"carbs_g": 49.0}))
        m1 = _db.meal_create(db_conn, "Breakfast", "2026-10-01")
        m2 = _db.meal_create(db_conn, "Lunch", "2026-10-01")
        _db.meal_add_food(db_conn, m1, rice_with_gi, "Rice", 100.0, "g")
        _db.meal_add_food(db_conn, m2, 2, "Bread", 100.0, "g")
        _db.meal_create(db_conn, "Other day", "2026-10-02")
        db_conn.commit()
        r = day_gl(db_conn, "2026-10-01")
        assert (r["total"], r["complete"], _gaps(r)) == (19.6, False, [("Bread", 2, None, GAP_NO_GI)])

    def test_passes_gi_opt_out_on(self, db_conn, rice_food):
        from numa_app.services.glycemic_load import day_gl
        m = _db.meal_create(db_conn, "Breakfast", "2026-10-01")
        _db.meal_add_food(db_conn, m, rice_food, "Rice", 100.0, "g")
        db_conn.commit()
        assert _gaps(day_gl(db_conn, "2026-10-01", gi_opt_out=True))[0][3] == GAP_NOT_WANTED
        assert _gaps(day_gl(db_conn, "2026-10-01"))[0][3] == GAP_NO_GI

    def test_a_date_with_no_meals_is_none(self, db_conn):
        from numa_app.services.glycemic_load import day_gl
        assert day_gl(db_conn, "2026-10-01") is None
