"""
Tests for numa_app/services/recipe_nutrients.py — the recursive
recipe-ingredient expansion used by the web backend (backend.py).
Previously reimplemented independently in five separate places before
being extracted here.
"""
import json

import pytest

import db as _db
from numa_app.services import recipe_nutrients as _rn


@pytest.fixture()
def nested_recipe(db_conn):
    """Oats + Almond milk cached; 'Oat base' sub-recipe (2 servings); 'Breakfast
    bowl' top recipe (1 serving) with 50g direct oats + 1 serving of Oat base."""
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (1, "Oats", "SR Legacy", json.dumps({"protein_g": 13.0, "calories": 389.0}), "[]"),
    )
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (2, "Almond milk", "SR Legacy", json.dumps({"protein_g": 0.4, "calories": 15.0}), "[]"),
    )
    sub_id = _db.recipe_create(db_conn, name="Oat base", description="", servings=2, instructions="")
    _db.recipe_add_ingredient(db_conn, sub_id, 1, "Oats", 200.0, "g")
    _db.recipe_add_ingredient(db_conn, sub_id, 2, "Almond milk", 500.0, "g")
    top_id = _db.recipe_create(db_conn, name="Breakfast bowl", description="", servings=1, instructions="")
    _db.recipe_add_ingredient(db_conn, top_id, 1, "Oats", 50.0, "g")
    _db.recipe_add_ingredient(db_conn, top_id, 0, "Oat base", 1.0, "serving", ref_recipe_id=sub_id)
    db_conn.commit()
    return {"sub_id": sub_id, "top_id": top_id}


class TestExpandRecipeIngredients:
    def test_flattens_nested_subrecipe_into_leaf_foods(self, db_conn, nested_recipe):
        leaves = _rn.expand_recipe_ingredients(nested_recipe["top_id"], db_conn)
        # 50g direct oats + (100g oats, 250g almond milk) from half the sub-recipe batch
        by_name = {}
        for leaf in leaves:
            by_name.setdefault(leaf["food_name"], 0.0)
            by_name[leaf["food_name"]] += leaf["grams"]
        assert by_name["Oats"] == pytest.approx(150.0)
        assert by_name["Almond milk"] == pytest.approx(250.0)

    def test_portion_factor_scales_everything_linearly(self, db_conn, nested_recipe):
        full = _rn.expand_recipe_ingredients(nested_recipe["top_id"], db_conn, portion_factor=1.0)
        half = _rn.expand_recipe_ingredients(nested_recipe["top_id"], db_conn, portion_factor=0.5)
        full_total = sum(leaf["grams"] for leaf in full)
        half_total = sum(leaf["grams"] for leaf in half)
        assert half_total == pytest.approx(full_total * 0.5)


class TestRecipeTotalNutrients:
    def test_sums_across_nested_subrecipe(self, db_conn, nested_recipe):
        total = _rn.recipe_total_nutrients(nested_recipe["top_id"], db_conn)
        # 50g oats + 100g oats (half of sub's 200g) + 250g almond milk (half of sub's 500g)
        assert total["protein_g"] == pytest.approx(150 * 0.13 + 250 * 0.004, abs=0.01)
        assert total["calories"] == pytest.approx(150 * 3.89 + 250 * 0.15, abs=0.1)

    def test_matches_manual_per_serving_calc(self, db_conn, nested_recipe):
        # The top recipe has 1 serving, so its total == its "per serving" value.
        total = _rn.recipe_total_nutrients(nested_recipe["top_id"], db_conn)
        per_serving = {k: v / 1.0 for k, v in total.items()}
        assert per_serving == total


class TestAtomicRecipeIngredients:
    """atomic_recipe_ingredients() had ZERO test coverage until a mutation-
    testing pass (TESTING-ROADMAP.md item #5) found it — a real gap, since
    it feeds a recipe's own DIAAS/digestibility pooling and its whole reason
    to exist is keeping a sub-recipe as ONE atomic entry rather than
    decomposing it into raw ingredients (see its own docstring on why: a
    sub-recipe's deliberate AA complementarity would otherwise get hidden)."""

    def test_direct_food_and_subrecipe_both_kept_atomic(self, db_conn, nested_recipe):
        result = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn)
        # Exactly 2 entries — NOT the 3 raw-leaf items expand_recipe_ingredients()
        # would produce (Oats x2 + Almond milk) — the sub-recipe stays atomic.
        assert len(result) == 2
        by_name = {r["food_name"]: r for r in result}

        direct = by_name["Oats"]
        assert direct["fdc_id"] == 1
        assert direct["recipe_id"] is None
        assert direct["grams"] == pytest.approx(50.0)
        assert direct["nutrients_100g"]["protein_g"] == pytest.approx(13.0)

        # "Oat base" is 1 of 2 servings of a 200g-oats/500g-almond-milk batch —
        # scale = 1/2 = 0.5, applied to the sub-recipe's own totals, not
        # decomposed into its Oats/Almond milk components.
        sub = by_name["Oat base"]
        assert sub["fdc_id"] is None
        assert sub["recipe_id"] == nested_recipe["sub_id"]
        assert sub["grams"] == pytest.approx(100.0)
        expected_sub_protein = (200 * 0.13 + 500 * 0.004) * 0.5
        assert sub["nutrients_100g"]["protein_g"] == pytest.approx(expected_sub_protein, abs=0.01)

    def test_portion_factor_scales_both_kinds_of_entry(self, db_conn, nested_recipe):
        full = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn, portion_factor=1.0)
        half = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn, portion_factor=0.5)
        full_by_name = {r["food_name"]: r for r in full}
        half_by_name = {r["food_name"]: r for r in half}

        # Direct ingredient: portion_factor scales grams, not the per-100g profile.
        assert half_by_name["Oats"]["grams"] == pytest.approx(full_by_name["Oats"]["grams"] * 0.5)
        assert half_by_name["Oats"]["nutrients_100g"]["protein_g"] == pytest.approx(
            full_by_name["Oats"]["nutrients_100g"]["protein_g"])

        # Sub-recipe: portion_factor scales the pre-baked nutrients_100g
        # itself (grams stays fixed at 100.0 — see the function's docstring).
        assert half_by_name["Oat base"]["grams"] == pytest.approx(100.0)
        assert half_by_name["Oat base"]["nutrients_100g"]["protein_g"] == pytest.approx(
            full_by_name["Oat base"]["nutrients_100g"]["protein_g"] * 0.5)


class TestBestAANutrients:
    def test_returns_unchanged_when_aa_data_present(self):
        nutrients = {"protein_g": 20.0, "aa_lysine_g": 1.0, "aa_leucine_g": 1.5,
                     "aa_isoleucine_g": 1.0, "aa_valine_g": 1.0, "aa_threonine_g": 0.8}
        result = _rn.best_aa_nutrients(nutrients, "Chicken breast")
        assert result == nutrients

    def test_returns_none_without_complement_match(self):
        result = _rn.best_aa_nutrients({"protein_g": 5.0}, "Totally Unknown Food XYZ123")
        assert result is None
