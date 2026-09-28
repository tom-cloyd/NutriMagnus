"""
Tests for numa_app/services/glycemic_load.py — GL aggregation used by the web
backend (backend.py). Its two previous separate implementations always
treated a recipe/sub-recipe line item as an unconditional blocker instead of
using the recipe's own precomputed gl_g.
"""
import json

import pytest

import db as _db
from numa_app.services.glycemic_load import (average_day_gl, compute_glycemic_load,
                                             day_gl_total, day_gl_totals, gl_band,
                                             gl_band_caveat)


@pytest.fixture()
def rice_food(db_conn):
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (1, "Rice", "SR Legacy", json.dumps({"carbs_g": 28.0}), "[]"),
    )
    db_conn.commit()
    return 1


class TestComputeGlycemicLoad:
    def test_food_item_without_gi_annotation_is_a_blocker(self, db_conn, rice_food):
        gl_total, blockers = compute_glycemic_load(
            [{"kind": "food", "name": "Rice", "amount": 100.0, "fdc_id": rice_food, "recipe_id": None}],
            db_conn,
        )
        assert gl_total == 0.0
        assert blockers == [("Rice", rice_food, None)]

    def test_food_item_with_gi_annotation_computes_gl(self, db_conn, rice_food):
        _db.set_food_annotation(db_conn, rice_food, gi_estimate=70.0, gi_no_prompt=False, diaas_estimate=None, diaas_no_prompt=False, prep_context=None)
        db_conn.commit()
        gl_total, blockers = compute_glycemic_load(
            [{"kind": "food", "name": "Rice", "amount": 100.0, "fdc_id": rice_food, "recipe_id": None}],
            db_conn,
        )
        # carbs_g=28 per 100g * 70 GI / 100 = 19.6
        assert gl_total == pytest.approx(19.6)
        assert blockers == []

    def test_recipe_item_uses_precomputed_gl_g(self, db_conn):
        rid = _db.recipe_create(db_conn, name="Rice bowl", description="", servings=2, instructions="")
        _db.recipe_set_gl(db_conn, rid, 30.0)
        db_conn.commit()
        gl_total, blockers = compute_glycemic_load(
            [{"kind": "recipe", "name": "Rice bowl", "amount": 1.0, "fdc_id": None, "recipe_id": rid}],
            db_conn,
        )
        # 1 serving consumed out of the recipe's 2 servings at gl_g=30 total
        assert gl_total == pytest.approx(15.0)
        assert blockers == []

    def test_recipe_item_without_gl_g_is_a_blocker(self, db_conn):
        rid = _db.recipe_create(db_conn, name="Unanalyzed recipe", description="", servings=1, instructions="")
        db_conn.commit()
        gl_total, blockers = compute_glycemic_load(
            [{"kind": "recipe", "name": "Unanalyzed recipe", "amount": 1.0, "fdc_id": None, "recipe_id": rid}],
            db_conn,
        )
        assert blockers == [("Unanalyzed recipe (no GL — analyze it first)", None, rid)]

    def test_mixed_items_accumulate_partial_total_alongside_blockers(self, db_conn, rice_food):
        _db.set_food_annotation(db_conn, rice_food, gi_estimate=70.0, gi_no_prompt=False, diaas_estimate=None, diaas_no_prompt=False, prep_context=None)
        rid = _db.recipe_create(db_conn, name="Unanalyzed recipe", description="", servings=1, instructions="")
        db_conn.commit()
        gl_total, blockers = compute_glycemic_load(
            [
                {"kind": "food", "name": "Rice", "amount": 100.0, "fdc_id": rice_food, "recipe_id": None},
                {"kind": "recipe", "name": "Unanalyzed recipe", "amount": 1.0, "fdc_id": None, "recipe_id": rid},
            ],
            db_conn,
        )
        assert gl_total == pytest.approx(19.6)
        assert blockers == [("Unanalyzed recipe (no GL — analyze it first)", None, rid)]


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
        assert "convention" in gl_band_caveat("day")


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

    def test_no_known_day_averages_to_nothing(self):
        assert average_day_gl({"a": None, "b": None}) == (None, 0)

    def test_empty_window(self):
        assert average_day_gl({}) == (None, 0)
