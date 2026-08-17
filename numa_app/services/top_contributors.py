"""
top_contributors.py — rank a meal's or recipe's ingredient-level items by
their contribution to one nutrient, for the "Top Contributors" analysis
section on meal and recipe detail pages.

Operates on the {"food_name", "fdc_id", "nutrients_100g", "grams"} shape
already produced by numa_app.services.recipe_nutrients.expand_recipe_ingredients()
/ atomic_recipe_ingredients() and the web backend's own meal ingredient
expansion — no new nutrient math, just resorting numbers already computed
for totals.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/top_contributors.py — nutrient contributor ranking"
"""
import sqlite3

import diaas as _diaas

Nutrients = dict[str, float]


def rank_contributors(ingredients: list[dict], nutrient_key: str) -> dict:
    """Rank ingredient-level items by their contribution to one nutrient, descending.

    ingredients: [{"food_name", "fdc_id", "recipe_id"?, "nutrients_100g", "grams"}, ...]
    Returns {"items": [{"food_name", "fdc_id", "recipe_id", "amount", "pct"}, ...],
    "total": float} for items with a nonzero contribution. `amount` is in the
    nutrient's native unit; `pct` is each item's share of `total` (the summed
    contribution across all items — not a comparison against an RDA/goal).
    """
    contributions = []
    total = 0.0
    for ing in ingredients:
        per100 = ing.get("nutrients_100g") or {}
        val = per100.get(nutrient_key)
        if not val:
            continue
        amount = val * ing["grams"] / 100.0
        if amount <= 0:
            continue
        contributions.append({
            "food_name": ing["food_name"],
            "fdc_id":    ing.get("fdc_id"),
            "recipe_id": ing.get("recipe_id"),
            "amount":    amount,
        })
        total += amount
    contributions.sort(key=lambda c: c["amount"], reverse=True)
    for c in contributions:
        c["pct"] = round(c["amount"] / total * 100, 1) if total else 0.0
    return {"items": contributions, "total": total}


def rank_contributors_by_dcp(ingredients: list[dict], conn: sqlite3.Connection | None) -> dict:
    """Rank ingredients by each one's own *standalone* digestible complete
    protein (DCP) — the DCP that food would have if it were the entire meal,
    via diaas.meal_level_diaas() run on it alone.

    This is NOT each food's share of the meal's actual pooled DCP: DIAAS
    complementarity means combining foods can raise the meal's real DCP
    above what any of them would score alone, so these standalone numbers
    do not sum to the meal's real DCP (shown in Protein Summary) — they only
    rank which foods are independently strong protein sources. Foods with no
    amino acid data score no DCP and are omitted, same as elsewhere on the
    page.

    Returns the same {"items", "total"} shape as rank_contributors().
    """
    contributions = []
    total = 0.0
    for ing in ingredients:
        result = _diaas.meal_level_diaas([ing], conn)
        dcp = result.get("digestible_complete_protein_g")
        if not dcp:
            continue
        contributions.append({
            "food_name": ing["food_name"],
            "fdc_id":    ing.get("fdc_id"),
            "recipe_id": ing.get("recipe_id"),
            "amount":    dcp,
        })
        total += dcp
    contributions.sort(key=lambda c: c["amount"], reverse=True)
    for c in contributions:
        c["pct"] = round(c["amount"] / total * 100, 1) if total else 0.0
    return {"items": contributions, "total": total}
