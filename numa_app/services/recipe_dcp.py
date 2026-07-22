"""
recipe_dcp.py — shared auto-recompute of a recipe's per-serving DCP, used by
CLI (recipes.py, recipe_edit.py) and web (backend.py) after any recipe or
ingredient edit, and by the web app's bulk "Compute DCP" action.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/recipe_dcp.py — recipe DCP auto-recompute"
"""
from datetime import datetime, timezone

import db as _db
import diaas as _diaas

from .recipe_nutrients import expand_recipe_ingredients


# An ingredient missing amino acid data blocks DCP unless its own protein
# contribution is negligible — matches the "minor ingredients w/o AA data
# excluded" threshold already used for the live per-serving display in
# recipes.py's _compute_recipe_protein_summary.
_MINOR_PROTEIN_G = 1.0
_MINOR_PROTEIN_FRACTION = 0.05


def recompute_recipe_dcp(recipe_id: int, conn) -> float | None:
    """Recompute and persist a recipe's per-serving DCP, or clear it to NC.

    Ingredients missing amino acid data are excluded from the digestible
    total rather than blocking the whole calculation, as long as each one's
    protein contribution is minor (<1 g and <5% of the recipe's total
    protein — e.g. spices, oil, salt). If any ingredient with a significant
    protein contribution is missing amino acid data, no value is saved — an
    approximate/best-guess DCP is never silently persisted.
    Returns the saved value, or None if the recipe isn't computable right now
    (0 servings, no weighed ingredients, or missing amino acid data on a
    significant protein source).
    """
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return None
    servings = float(recipe["servings"] or 0)
    if servings <= 0:
        _db.recipe_set_dcp(conn, recipe_id, None)
        return None

    leaves = expand_recipe_ingredients(recipe_id, conn, portion_factor=1.0 / servings)
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
        _db.recipe_set_dcp(conn, recipe_id, None)
        return None

    result = _diaas.meal_level_diaas(diaas_ingredients, conn)
    dcp_g = result.get("digestible_complete_protein_g")
    if dcp_g is None:
        _db.recipe_set_dcp(conn, recipe_id, None)
        return None

    total_protein_g = result.get("total_protein_g", 0.0)
    for ing in result.get("ingredients", []):
        if ing.get("has_aa_data") or ing.get("protein_g", 0.0) <= 0:
            continue
        p = ing["protein_g"]
        is_minor = p < _MINOR_PROTEIN_G and (
            total_protein_g > 0 and p / total_protein_g < _MINOR_PROTEIN_FRACTION
        )
        if not is_minor:
            _db.recipe_set_dcp(conn, recipe_id, None)
            return None

    dcp_g = round(dcp_g, 2)
    now_utc = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
    _db.recipe_set_dcp(conn, recipe_id, dcp_g, now_utc)
    return dcp_g
