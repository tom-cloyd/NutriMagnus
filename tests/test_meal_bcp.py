"""
Tests for numa_app/services/meal_bcp.py — the shared meal-DCP fallback used by
CLI (meals.py) and web (backend.py). web previously lacked this fallback
entirely: a meal whose foods lack raw AA data (so the primary DIAAS-based DCP
computation returns nothing) but whose recipe item already has a precomputed
dcp_g would silently persist bcp_g=None on the web route while the CLI still
computed a correct value.
"""
import json

import pytest

import db as _db
from numa_app.services.meal_bcp import recipe_dcp_fallback


@pytest.fixture()
def meal_with_analyzed_recipe(db_conn):
    """A meal containing one serving of a 2-serving recipe with dcp_g=18 already set."""
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (1, "Mystery Blend", "Branded", json.dumps({"protein_g": 10.0}), "[]"),
    )
    rid = _db.recipe_create(db_conn, name="Pre-analyzed dish", description="", servings=2, instructions="")
    _db.recipe_add_ingredient(db_conn, rid, 1, "Mystery Blend", 200.0, "g")
    _db.recipe_set_dcp(db_conn, rid, 18.0)
    meal_id = _db.meal_create(db_conn, "Dinner", "2026-07-11")
    _db.meal_add_recipe(db_conn, meal_id, rid, "Pre-analyzed dish", 1.0, unit="1 serving")
    db_conn.commit()
    return meal_id


class TestRecipeDCPFallback:
    def test_sums_precomputed_recipe_dcp(self, db_conn, meal_with_analyzed_recipe):
        result = recipe_dcp_fallback(meal_with_analyzed_recipe, db_conn)
        assert result == pytest.approx(18.0)

    def test_none_when_no_recipe_has_dcp(self, db_conn):
        meal_id = _db.meal_create(db_conn, "Empty meal", "2026-07-11")
        db_conn.commit()
        assert recipe_dcp_fallback(meal_id, db_conn) is None

    def test_none_for_recipe_without_dcp_computed_yet(self, db_conn):
        rid = _db.recipe_create(db_conn, name="Unanalyzed", description="", servings=1, instructions="")
        meal_id = _db.meal_create(db_conn, "Meal", "2026-07-11")
        _db.meal_add_recipe(db_conn, meal_id, rid, "Unanalyzed", 1.0, unit="1 serving")
        db_conn.commit()
        assert recipe_dcp_fallback(meal_id, db_conn) is None
