"""
recipe_nutrients.py — recursive recipe-ingredient expansion and nutrient
totaling, used by the web backend (backend.py). Previously reimplemented
independently in five separate places before being extracted here.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/recipe_nutrients.py — recipe nutrient aggregation"
"""
import json

import db as _db
import usda as _usda

Nutrients = dict[str, float]


def expand_recipe_ingredients(
    recipe_id: int,
    conn,
    *,
    portion_factor: float = 1.0,
) -> list[dict]:
    """Recursively expand a recipe into its leaf food ingredients.

    Sub-recipe ingredients are expanded recursively, scaling by
    (sub-ingredient amount / sub-recipe servings) * portion_factor — i.e.
    portion_factor=1.0 means "one full batch of this recipe as authored".

    Returns [{"food_name", "fdc_id", "nutrients_100g", "grams"}, ...] — one
    entry per leaf food ingredient; sub-recipes themselves don't appear.
    """
    result: list[dict] = []
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_id"]:
            sub = _db.recipe_get(conn, ing["ref_recipe_id"])
            sub_servings = float(sub["servings"] or 1) if sub else 1.0
            sub_factor = float(ing["amount"]) / sub_servings * portion_factor
            result.extend(expand_recipe_ingredients(
                ing["ref_recipe_id"], conn,
                portion_factor=sub_factor,
            ))
        elif ing["fdc_id"]:
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                continue
            nuts_100g = json.loads(cached["nutrients_json"])
            if nuts_100g:
                result.append({
                    "food_name":      ing["food_name"],
                    "fdc_id":         ing["fdc_id"],
                    "nutrients_100g": nuts_100g,
                    "grams":          float(ing["amount"]) * portion_factor,
                })
    return result


def atomic_recipe_ingredients(
    recipe_id: int,
    conn,
    *,
    portion_factor: float = 1.0,
) -> list[dict]:
    """Expand a recipe into food-level dicts for DIAAS/digestibility pooling —
    direct ingredients expand as usual, but a sub-recipe ingredient is kept as
    ONE atomic food using its own already-computed whole-batch nutrient
    profile, rather than decomposed into its raw ingredients.

    A sub-recipe is often deliberately built from complementary foods to raise
    its own DCP (e.g. a nut butter blended with a seed to fill its limiting
    amino acid). Recursively flattening it for an outer recipe's digestibility
    breakdown would hide that complementarity behind tiny per-component
    protein amounts and misattribute its digestible protein to whichever raw
    ingredient happens to dominate its weight — "recipes taken as a whole" is
    the correct model here.

    Returns [{"food_name", "fdc_id", "recipe_id", "nutrients_100g", "grams"}, ...]
    — fdc_id is None for a sub-recipe entry, recipe_id is None for a direct food.
    Use expand_recipe_ingredients() instead when you need raw-leaf totals (e.g.
    summing calories/vitamins/minerals, where grouping makes no difference).
    """
    result: list[dict] = []
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_deleted"]:
            continue
        if ing["ref_recipe_id"]:
            sub = _db.recipe_get(conn, ing["ref_recipe_id"])
            sub_servings = float(sub["servings"] or 1) if sub else 0.0
            if not sub or sub_servings <= 0:
                continue
            sub_total = recipe_total_nutrients(ing["ref_recipe_id"], conn)
            scale = float(ing["amount"]) / sub_servings * portion_factor
            scaled = {k: v * scale for k, v in sub_total.items()}
            if scaled.get("protein_g", 0.0) <= 0:
                continue
            result.append({
                "food_name":      ing["food_name"],
                "fdc_id":         None,
                "recipe_id":      ing["ref_recipe_id"],
                "nutrients_100g": scaled,
                "grams":          100.0,
            })
        elif ing["fdc_id"]:
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                continue
            nuts_100g = json.loads(cached["nutrients_json"])
            if not nuts_100g:
                continue
            result.append({
                "food_name":      ing["food_name"],
                "fdc_id":         ing["fdc_id"],
                "recipe_id":      None,
                "nutrients_100g": nuts_100g,
                "grams":          float(ing["amount"]) * portion_factor,
            })
    return result


def recipe_total_nutrients(
    recipe_id: int,
    conn,
    *,
    portion_factor: float = 1.0,
) -> Nutrients:
    """Sum nutrients across a recipe's (recursively expanded) leaf ingredients.

    portion_factor=1.0 (default) returns totals for one full batch of the
    recipe as authored — callers scale by their own serving-consumption math.
    """
    total: Nutrients = {}
    for leaf in expand_recipe_ingredients(
        recipe_id, conn, portion_factor=portion_factor,
    ):
        scaled = _usda.scale_nutrients(leaf["nutrients_100g"], leaf["grams"], base_size=100.0)
        total = _usda.sum_nutrients(total, scaled)
    return total


def best_aa_nutrients(nutrients: Nutrients, food_name: str) -> Nutrients | None:
    """Merge in complement-table AA data if `nutrients` is missing it.

    Returns `nutrients` unchanged if it already has AA data. If not, tries to
    merge in AA values from usda.get_complement_nutrients(food_name), scaled
    to match the food's actual protein content. Returns None if no AA data is
    available from either source.
    """
    if _usda.has_amino_acid_data(nutrients):
        return nutrients
    complement = _usda.get_complement_nutrients(food_name)
    if complement and _usda.has_amino_acid_data(complement):
        actual_protein = nutrients.get("protein_g", 0)
        ref_protein = complement.get("protein_g", 0)
        if ref_protein > 0 and actual_protein > 0:
            scale = actual_protein / ref_protein
            merged = dict(nutrients)
            for k, v in complement.items():
                if k.startswith("aa_") and k not in merged:
                    merged[k] = v * scale
            return merged
    return None
