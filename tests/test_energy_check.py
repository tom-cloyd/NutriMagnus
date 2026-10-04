"""Calorie checks: energy_check.py and db's save-time fill (_calorie_check)."""
import json

import pytest

import db as _db
from numa_app.services import energy_check as ec


def test_atwater_estimate_needs_all_three_macros():
    assert ec.atwater_estimate({"protein_g": 10, "carbs_g": 20, "fat_g": 5}) == pytest.approx(165)
    assert ec.atwater_estimate({"protein_g": 10, "fat_g": 5}) is None


def test_fill_missing_calories():
    n = {"protein_g": 21.2, "carbs_g": 21.6, "fat_g": 49.9}
    assert ec.fill_missing_calories(n) is True
    assert n["calories"] == pytest.approx(620.3, abs=0.1)
    assert ec.fill_missing_calories(n) is False  # already present


def test_fill_skips_incomplete_macros():
    n = {"fat_g": 81.0}
    assert ec.fill_missing_calories(n) is False
    assert "calories" not in n
    assert ec.calories_missing(n) is True
    assert ec.calories_missing({"fiber_g": 4.0}) is True   # raisins: no macros either
    assert ec.calories_missing({"calories": 0.0}) is False  # 0 is a value (salt, water)


@pytest.mark.parametrize("n,flagged", [
    ({"calories": 584, "protein_g": 21.2, "carbs_g": 21.6, "fat_g": 49.9}, False),   # almonds
    ({"calories": 216, "protein_g": 15.6, "carbs_g": 64.5, "fat_g": 4.3, "fiber_g": 42.8}, False),  # wheat bran
    ({"calories": 23, "protein_g": 2.9, "carbs_g": 3.6, "fat_g": 0.4}, False),       # spinach
    ({"calories": 0, "protein_g": 0, "carbs_g": 1000, "fat_g": 150}, True),          # broken salt record
    ({"calories": 900, "protein_g": 1, "carbs_g": 10, "fat_g": 1}, True),
])
def test_calorie_mismatch(n, flagged):
    assert (ec.calorie_mismatch(n) is not None) is flagged


def _store(conn, fdc_id, nutrients):
    _db.cache_food(conn, fdc_id, "Test food", "Foundation", None, 100.0, "g", nutrients)
    row = _db.get_cached_food(conn, fdc_id)
    return json.loads(row["nutrients_json"]), _db.estimated_keys(conn, fdc_id)


def test_cache_food_fills_and_marks_missing_calories():
    with _db.get_db() as conn:
        n, est = _store(conn, 990101, {"protein_g": 10, "carbs_g": 20, "fat_g": 5})
    assert n["calories"] == pytest.approx(165)
    assert "calories" in est


def test_estimate_follows_macro_edits_and_real_value_clears_mark():
    with _db.get_db() as conn:
        _store(conn, 990102, {"protein_g": 10, "carbs_g": 20, "fat_g": 5})
        _db.update_food_nutrients_partial(conn, 990102, {"fat_g": 10})
        n = json.loads(_db.get_cached_food(conn, 990102)["nutrients_json"])
        assert n["calories"] == pytest.approx(210)  # re-estimated, still marked
        assert "calories" in _db.estimated_keys(conn, 990102)
        _db.merge_user_supplied_nutrients(conn, 990102, {"calories": 200.0}, overwrite=True)
        n = json.loads(_db.get_cached_food(conn, 990102)["nutrients_json"])
        assert n["calories"] == 200.0
        assert "calories" not in _db.estimated_keys(conn, 990102)


def test_measured_calories_never_marked():
    with _db.get_db() as conn:
        n, est = _store(conn, 990103, {"calories": 584, "protein_g": 21, "carbs_g": 22, "fat_g": 50})
    assert n["calories"] == 584 and "calories" not in est
