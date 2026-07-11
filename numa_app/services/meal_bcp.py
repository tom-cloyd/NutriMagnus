"""
meal_bcp.py — shared fallback for a meal's digestible complete protein (DCP/BCP)
when ingredient-level AA data isn't available. Used by CLI (meals.py) and web
(backend.py); web previously lacked this fallback entirely, silently storing
None for any meal whose foods lack raw AA data even when its recipe item(s)
already have a precomputed dcp_g.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/meal_bcp.py — meal DCP fallback"
"""
import db as _db


def recipe_dcp_fallback(meal_id: int, conn) -> float | None:
    """Sum stored per-serving DCP from this meal's recipe items that have been analyzed.

    Use when the primary DIAAS-based DCP computation (from ingredient-level AA
    data) is unavailable — e.g. cached nutrients lack raw AA data but a recipe
    item already has a precomputed recipes.dcp_g from its own analysis.
    Returns None if no recipe item in the meal has a usable dcp_g.
    """
    items = _db.meal_get_items(conn, meal_id)
    total_dcp = 0.0
    has_any = False
    for item in items:
        if item["item_type"] != "recipe":
            continue
        recipe = _db.recipe_get(conn, item["recipe_id"])
        if recipe and recipe["dcp_g"] is not None:
            total_dcp += recipe["dcp_g"] * item["amount"]
            has_any = True
    return total_dcp if has_any else None
