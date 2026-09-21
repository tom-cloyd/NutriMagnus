"""
Tests for numa_app/services/recipe_nutrients.py — the recursive
recipe-ingredient expansion used by the web backend (backend.py).
Previously reimplemented independently in five separate places before
being extracted here.
"""
import json

import pytest

import db as _db
import usda_nutrients
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

    def test_leaf_entries_carry_the_correct_fdc_id(self, db_conn, nested_recipe):
        # A mutation-testing pass found the "fdc_id" dict key itself (not
        # just the value) had no coverage — nothing read leaf["fdc_id"].
        leaves = _rn.expand_recipe_ingredients(nested_recipe["top_id"], db_conn)
        by_name = {leaf["food_name"]: leaf for leaf in leaves}
        assert by_name["Oats"]["fdc_id"] == 1
        assert by_name["Almond milk"]["fdc_id"] == 2

    def test_uncached_food_is_skipped_not_fatal(self, db_conn, nested_recipe):
        _db.recipe_add_ingredient(db_conn, nested_recipe["top_id"], 999, "Uncached food", 10.0, "g")
        leaves = _rn.expand_recipe_ingredients(nested_recipe["top_id"], db_conn)
        names = {leaf["food_name"] for leaf in leaves}
        assert "Uncached food" not in names
        assert "Oats" in names and "Almond milk" in names

    def test_subrecipe_servings_of_zero_defaults_to_one_not_two(self, db_conn):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (6, "Flour", "SR Legacy", json.dumps({"protein_g": 10.0}), "[]"),
        )
        zero_serving_sub = _db.recipe_create(db_conn, name="Zero-serving sub 2", description="", servings=0, instructions="")
        _db.recipe_add_ingredient(db_conn, zero_serving_sub, 6, "Flour", 100.0, "g")
        db_conn.execute("UPDATE recipes SET servings = 0 WHERE id = ?", (zero_serving_sub,))
        top_id = _db.recipe_create(db_conn, name="Outer 2", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(
            db_conn, top_id, 0, "Zero-serving sub 2", 1.0, "serving", ref_recipe_id=zero_serving_sub,
        )
        db_conn.commit()
        leaves = _rn.expand_recipe_ingredients(top_id, db_conn)
        # sub_servings falls back to 1 (correct) -> sub_factor = 1/1 = 1 -> 100g Flour.
        # If it had fallen back to 2 instead, this would be 50g.
        assert leaves[0]["grams"] == pytest.approx(100.0)


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


class TestAtomicRecipeIngredientsSkipBehavior:
    """Every "skip this one ingredient, keep processing the rest" branch in
    atomic_recipe_ingredients() had only ever been exercised by a single-bad-
    item-free fixture — a mutation-testing pass found a `continue` mutated to
    `break` on any of these branches survived, since nothing proved the loop
    keeps going past a skipped item rather than silently dropping every
    ingredient after it. Each test below adds one bad ingredient followed by
    one good one and asserts the good one still comes through."""

    def test_deleted_subrecipe_reference_is_skipped_not_fatal(self, db_conn, nested_recipe):
        _db.recipe_add_ingredient(
            db_conn, nested_recipe["top_id"], 0, "Ghost sub-recipe", 1.0, "serving",
            ref_recipe_id=None, ref_recipe_deleted=True,
        )
        result = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn)
        names = {r["food_name"] for r in result}
        assert "Ghost sub-recipe" not in names
        assert "Oats" in names and "Oat base" in names

    def test_zero_serving_subrecipe_is_skipped_not_fatal(self, db_conn, nested_recipe):
        empty_sub_id = _db.recipe_create(db_conn, name="Empty sub", description="", servings=0, instructions="")
        db_conn.commit()
        _db.recipe_add_ingredient(
            db_conn, nested_recipe["top_id"], 0, "Empty sub", 1.0, "serving",
            ref_recipe_id=empty_sub_id,
        )
        result = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn)
        names = {r["food_name"] for r in result}
        assert "Empty sub" not in names
        assert "Oats" in names and "Oat base" in names

    def test_subrecipe_ingredient_with_uncached_food_is_skipped_not_fatal(self, db_conn, nested_recipe):
        # fdc_id 999 was never inserted into `foods` — get_cached_food() returns None.
        _db.recipe_add_ingredient(db_conn, nested_recipe["top_id"], 999, "Uncached food", 10.0, "g")
        result = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn)
        names = {r["food_name"] for r in result}
        assert "Uncached food" not in names
        assert "Oats" in names and "Oat base" in names

    def test_subrecipe_ingredient_with_empty_nutrients_is_skipped_not_fatal(self, db_conn, nested_recipe):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (3, "Empty-nutrients food", "SR Legacy", json.dumps({}), "[]"),
        )
        _db.recipe_add_ingredient(db_conn, nested_recipe["top_id"], 3, "Empty-nutrients food", 10.0, "g")
        result = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn)
        names = {r["food_name"] for r in result}
        assert "Empty-nutrients food" not in names
        assert "Oats" in names and "Oat base" in names

    def test_subrecipe_scaling_to_zero_protein_is_skipped_not_fatal(self, db_conn, nested_recipe):
        # A sub-recipe with a protein-free ingredient scales to protein_g <= 0.
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (4, "Water", "SR Legacy", json.dumps({"protein_g": 0.0, "calories": 0.0}), "[]"),
        )
        water_sub_id = _db.recipe_create(db_conn, name="Water base", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(db_conn, water_sub_id, 4, "Water", 500.0, "g")
        db_conn.commit()
        _db.recipe_add_ingredient(
            db_conn, nested_recipe["top_id"], 0, "Water base", 1.0, "serving",
            ref_recipe_id=water_sub_id,
        )
        result = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn)
        names = {r["food_name"] for r in result}
        assert "Water base" not in names
        assert "Oats" in names and "Oat base" in names

    def test_zero_serving_subrecipe_and_existing_subrecipe_both_checked(self, db_conn, nested_recipe):
        # Boundary/logic check: "not sub or sub_servings <= 0" must not have
        # drifted to "and" (which would never skip an existing-but-empty
        # sub-recipe) — this only crashes (ZeroDivisionError) rather than
        # returning wrong data, so it's asserted via "does not raise."
        empty_sub_id = _db.recipe_create(db_conn, name="Empty sub 2", description="", servings=0, instructions="")
        db_conn.commit()
        _db.recipe_add_ingredient(
            db_conn, nested_recipe["top_id"], 0, "Empty sub 2", 1.0, "serving",
            ref_recipe_id=empty_sub_id,
        )
        result = _rn.atomic_recipe_ingredients(nested_recipe["top_id"], db_conn)  # must not raise
        assert "Empty sub 2" not in {r["food_name"] for r in result}

    def test_subrecipe_servings_of_zero_defaults_to_one_not_two(self, db_conn):
        # sub["servings"] or 1 — a recipe genuinely saved with servings=0
        # (falsy) must fall back to 1, not silently become 2.
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (5, "Flour", "SR Legacy", json.dumps({"protein_g": 10.0}), "[]"),
        )
        zero_serving_sub = _db.recipe_create(db_conn, name="Zero-serving sub", description="", servings=0, instructions="")
        _db.recipe_add_ingredient(db_conn, zero_serving_sub, 5, "Flour", 100.0, "g")
        # Force servings back to 0 (recipe_create may reject/clamp it otherwise).
        db_conn.execute("UPDATE recipes SET servings = 0 WHERE id = ?", (zero_serving_sub,))
        top_id = _db.recipe_create(db_conn, name="Outer", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(
            db_conn, top_id, 0, "Zero-serving sub", 1.0, "serving", ref_recipe_id=zero_serving_sub,
        )
        db_conn.commit()
        result = _rn.atomic_recipe_ingredients(top_id, db_conn)
        assert len(result) == 1
        # If sub_servings fell back to 1 (correct): scale = 1/1 = 1, so the
        # entry's protein equals the sub-recipe's own total (100g * 10%).
        # If it had fallen back to 2 instead: scale = 1/2, half that value.
        assert result[0]["nutrients_100g"]["protein_g"] == pytest.approx(10.0)


class TestBestAANutrients:
    # The merge/scale success path (complement match found, AA values scaled
    # to the food's own protein and merged in) had ZERO test coverage before
    # a mutation-testing pass found 34 survivors here — the two tests below
    # this comment only ever exercised the "already has data" and "no match"
    # branches, never the actual merge itself.

    def test_returns_unchanged_when_aa_data_present(self):
        nutrients = {"protein_g": 20.0, "aa_lysine_g": 1.0, "aa_leucine_g": 1.5,
                     "aa_isoleucine_g": 1.0, "aa_valine_g": 1.0, "aa_threonine_g": 0.8}
        result = _rn.best_aa_nutrients(nutrients, "Chicken breast")
        assert result == nutrients

    def test_returns_none_without_complement_match(self):
        result = _rn.best_aa_nutrients({"protein_g": 5.0}, "Totally Unknown Food XYZ123")
        assert result is None

    def test_merges_complement_aa_data_scaled_to_actual_protein(self):
        # "Lentils" is a real curated-table entry: protein_g 9.02, 10 aa_ keys.
        # Target has double that protein, so scale must be exactly 2.0.
        source = usda_nutrients._find_complement_by_name("Lentils")["nutrients"]
        target = {"protein_g": source["protein_g"] * 2.0, "calories": 150.0}
        result = _rn.best_aa_nutrients(target, "Lentils")
        assert result is not None
        # Non-AA fields untouched, present unchanged.
        assert result["protein_g"] == target["protein_g"]
        assert result["calories"] == 150.0
        # Every aa_ key from the source is present, scaled by exactly 2.0.
        aa_keys = [k for k in source if k.startswith("aa_")]
        assert aa_keys, "test fixture must have at least one aa_ key to check"
        for k in aa_keys:
            assert result[k] == pytest.approx(source[k] * 2.0)

    def test_does_not_overwrite_an_aa_key_already_present(self):
        source = usda_nutrients._find_complement_by_name("Lentils")["nutrients"]
        target = {
            "protein_g": source["protein_g"],
            "aa_lysine_g": 999.0,  # deliberately implausible, to prove it survives
        }
        result = _rn.best_aa_nutrients(target, "Lentils")
        assert result is not None
        assert result["aa_lysine_g"] == 999.0
        # A key NOT already present still gets merged in.
        assert result["aa_leucine_g"] == pytest.approx(source["aa_leucine_g"])

    def test_ref_protein_of_exactly_one_gram_still_succeeds(self, monkeypatch):
        # Boundary check: "ref_protein > 0" must not have drifted to ">= 0"
        # or "> 1" — 1.0g of protein on the complement entry is real data,
        # not "missing." Monkeypatch the complement lookup since no real
        # curated-table entry happens to have protein_g == 1.0 exactly.
        fake_complement = {
            "protein_g": 1.0, "aa_lysine_g": 0.1, "aa_leucine_g": 0.1,
            "aa_isoleucine_g": 0.1, "aa_valine_g": 0.1, "aa_threonine_g": 0.1,
        }
        monkeypatch.setattr(_rn._usda, "get_complement_nutrients", lambda name: fake_complement)
        result = _rn.best_aa_nutrients({"protein_g": 5.0}, "Fake Food")
        assert result is not None
        assert result["aa_lysine_g"] == pytest.approx(0.1 * 5.0)

    def test_actual_protein_of_exactly_one_gram_still_succeeds(self, monkeypatch):
        fake_complement = {
            "protein_g": 5.0, "aa_lysine_g": 0.5, "aa_leucine_g": 0.5,
            "aa_isoleucine_g": 0.5, "aa_valine_g": 0.5, "aa_threonine_g": 0.5,
        }
        monkeypatch.setattr(_rn._usda, "get_complement_nutrients", lambda name: fake_complement)
        result = _rn.best_aa_nutrients({"protein_g": 1.0}, "Fake Food")
        assert result is not None
        assert result["aa_lysine_g"] == pytest.approx(0.5 * (1.0 / 5.0))

    def test_zero_ref_protein_returns_none_instead_of_dividing_by_zero(self, monkeypatch):
        # Boundary check: "ref_protein > 0" must not have drifted to ">= 0",
        # which would let ref_protein == 0 through into `actual_protein /
        # ref_protein` and raise ZeroDivisionError instead of cleanly
        # returning None. A complement entry with protein_g == 0 still
        # passes has_confirmed_aa_data() (has_amino_acid_data()'s "no
        # protein" branch treats 0 as trivially "AA data not needed").
        fake_complement = {"protein_g": 0.0}
        monkeypatch.setattr(_rn._usda, "get_complement_nutrients", lambda name: fake_complement)
        result = _rn.best_aa_nutrients({"protein_g": 5.0}, "Fake Food")
        assert result is None

    def test_returns_none_when_target_has_no_macro_data_at_all(self):
        # An empty dict fails has_confirmed_aa_data's has_macro_data() check
        # (not "confirmed", so a complement lookup is attempted), then the
        # merge itself bails via "actual_protein > 0" — this is the one way
        # to actually reach that guard: any real macro key present (even
        # protein_g=0.0) already makes has_confirmed_aa_data() short-circuit
        # True higher up, in has_amino_acid_data()'s "no protein" branch.
        result = _rn.best_aa_nutrients({}, "Lentils")
        assert result is None
