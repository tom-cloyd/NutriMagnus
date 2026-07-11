"""
Tests for numa_app/services/glycemic_load.py — shared GL aggregation used by
CLI (recipes.py, meals.py) and web (backend.py). web's two implementations
previously always treated a recipe/sub-recipe line item as an unconditional
blocker instead of using the recipe's own precomputed gl_g, unlike the CLI.
"""
import json

import pytest

import db as _db
from numa_app.services.glycemic_load import compute_glycemic_load


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
        assert blockers == ["Rice"]

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
        assert blockers == ["Unanalyzed recipe (no GL — analyze it first)"]

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
        assert blockers == ["Unanalyzed recipe (no GL — analyze it first)"]
