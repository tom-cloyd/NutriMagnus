"""
recipe_dcp.py — shared auto-recompute of a recipe's per-serving DCP, used by
CLI (recipes.py, recipe_edit.py) and web (backend.py) after any recipe or
ingredient edit, and by the web app's bulk "Compute DCP" action.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/recipe_dcp.py — recipe DCP auto-recompute"
"""
import json
from datetime import datetime, timezone

import db as _db
import diaas as _diaas
import usda as _usda

from .recipe_nutrients import atomic_recipe_ingredients, expand_recipe_ingredients


# An ingredient missing amino acid data blocks DCP unless its own protein
# contribution is negligible — matches the "minor ingredients w/o AA data
# excluded" threshold already used for the live per-serving display in
# recipes.py's _compute_recipe_protein_summary. The absolute gram floor
# stands alone: an ingredient under 1 g of protein is negligible regardless
# of what fraction of the recipe's (possibly small) total protein that is —
# a low-total-protein recipe shouldn't make trivial contributors count more.
_MINOR_PROTEIN_G = 1.0


def recompute_recipe_dcp(recipe_id: int, conn) -> float | None:
    """Recompute and persist a recipe's per-serving DCP, or clear it to NC —
    then cascade the same recompute up to every recipe that uses this one as
    a sub-recipe ingredient (directly or transitively), so a change deep in a
    nested recipe is never left silently stale in its ancestors.

    Ingredients missing amino acid data are excluded from the digestible
    total rather than blocking the whole calculation, as long as each one's
    protein contribution is minor (<1 g — e.g. spices, oil, salt). If any
    ingredient with 1 g or more of protein is missing amino acid data, no
    value is saved — an approximate/best-guess DCP is never silently
    persisted.
    Returns the saved value for `recipe_id` itself (not its ancestors), or
    None if that recipe isn't computable right now (0 servings, no weighed
    ingredients, or missing amino acid data on a significant protein source).
    """
    own_result = _recompute_single_recipe_dcp(recipe_id, conn)
    _cascade_to_ancestors(recipe_id, conn, seen={recipe_id})
    return own_result


def _cascade_to_ancestors(recipe_id: int, conn, *, seen: set[int]) -> None:
    """Recompute every recipe that references `recipe_id` as a sub-recipe
    ingredient, then their own referencing recipes, and so on. `seen` guards
    against re-visiting a recipe (diamond-shaped references) or looping
    forever if a reference cycle ever exists."""
    for row in _db.recipe_referencing_subrecipe(conn, recipe_id):
        parent_id = row["id"]
        if parent_id in seen:
            continue
        seen.add(parent_id)
        _recompute_single_recipe_dcp(parent_id, conn)
        _cascade_to_ancestors(parent_id, conn, seen=seen)


def _recompute_single_recipe_dcp(recipe_id: int, conn) -> float | None:
    """Recompute and persist just this recipe's own per-serving DCP (no
    cascade). A sub-recipe ingredient is pooled as one atomic food using its
    own already-computed nutrient profile rather than decomposed into its raw
    ingredients — see atomic_recipe_ingredients() for why."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return None
    servings = float(recipe["servings"] or 0)
    if servings <= 0:
        _clear_recipe_dcp_and_nutrients(conn, recipe_id)
        return None

    leaves = atomic_recipe_ingredients(recipe_id, conn, portion_factor=1.0 / servings)
    diaas_ingredients = [
        {
            "food_name":      leaf["food_name"],
            "nutrients_100g": leaf["nutrients_100g"],
            "grams":          leaf["grams"],
            "fdc_id":         leaf["fdc_id"],
        }
        for leaf in leaves if leaf["grams"] > 0
    ]
    if not diaas_ingredients:
        _clear_recipe_dcp_and_nutrients(conn, recipe_id)
        return None

    result = _diaas.meal_level_diaas(diaas_ingredients, conn)
    dcp_g = result.get("digestible_complete_protein_g")
    if dcp_g is None:
        _clear_recipe_dcp_and_nutrients(conn, recipe_id)
        return None

    for ing in result.get("ingredients", []):
        if ing.get("has_aa_data") or ing.get("protein_g", 0.0) <= 0:
            continue
        p = ing["protein_g"]
        is_minor = p < _MINOR_PROTEIN_G
        if not is_minor:
            _db.recipe_set_dcp(conn, recipe_id, None)
            return None

    dcp_g = round(dcp_g, 2)
    now_utc = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
    _db.recipe_set_dcp(conn, recipe_id, dcp_g, now_utc)
    _save_recipe_nutrients_100g(recipe_id, conn)
    return dcp_g


def _clear_recipe_dcp_and_nutrients(conn, recipe_id: int) -> None:
    """Clear both DCP and cached nutrients so a stale profile never lingers
    as a complement-suggestion candidate once a recipe becomes uncomputable."""
    _db.recipe_set_dcp(conn, recipe_id, None)
    try:
        _db.recipe_save_nutrients(conn, recipe_id, None)
    except Exception:
        pass


def _save_recipe_nutrients_100g(recipe_id: int, conn) -> None:
    """Cache the recipe's whole-batch per-100g nutrient profile.

    This is what makes an analyzed recipe eligible to appear as a protein
    complement candidate elsewhere (CLI and web share the same
    `recipes.nutrients_json` column, read by _load_recipe_candidates /
    _web_recipe_candidates). Best-effort — failure here must never affect
    the DCP value already saved above.
    """
    try:
        whole_batch_leaves = expand_recipe_ingredients(recipe_id, conn, portion_factor=1.0)
        total_weight_g = sum(leaf["grams"] for leaf in whole_batch_leaves if leaf["grams"] > 0)
        if total_weight_g <= 0:
            return
        total = {}
        for leaf in whole_batch_leaves:
            if leaf["grams"] <= 0:
                continue
            scaled = _usda.scale_nutrients(leaf["nutrients_100g"], leaf["grams"], base_size=100.0)
            total = _usda.sum_nutrients(total, scaled)
        per_100g = _usda.scale_nutrients(total, 100.0, base_size=total_weight_g)
        _db.recipe_save_nutrients(conn, recipe_id, json.dumps(per_100g))
    except Exception:
        pass
