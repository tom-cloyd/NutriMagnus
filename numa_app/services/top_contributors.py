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
from urllib.parse import urlencode

import db as _db
import diaas as _diaas
import usda as _usda
from numa_app.services import glycemic_load as _gl

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
        c["pct"] = round(c["amount"] / total * 100, 4) if total else 0.0
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
        c["pct"] = round(c["amount"] / total * 100, 4) if total else 0.0
    return {"items": contributions, "total": total}


def rank_contributors_by_gl(ingredients: list[dict], conn: sqlite3.Connection,
                            gi_opt_out: bool = False) -> dict:
    """Rank leaf foods by their glycemic load (GI x carbohydrate g / 100).

    Unlike DCP, GL is additive: the items sum to the meal's or recipe's GL
    (the counted part — see glycemic_load). `ingredients` must be leaf foods
    (sub-recipes opened up), since a GI belongs to a food. The same food
    reached twice (in two sub-recipes) is one row.

    Returns rank_contributors()'s {"items", "total"} plus "gaps" (foods with
    carbohydrate but no GI — glycemic_load gap dicts) and "coverage_pct".
    Each item also carries "gi", "grams" and "carbs_100g", which lower-GL
    swap suggestions (gl_swaps.py) work from, and "impaired" (its GI was
    measured in people with impaired glucose tolerance or diabetes).
    """
    whole = _gl.gl_for_leaves(ingredients, conn, gi_opt_out=gi_opt_out)
    ids = list({i["fdc_id"] for i in ingredients if i.get("fdc_id")})
    ann_map = _db.annotations_for_fdcids(conn, ids)
    by_food: dict = {}
    for ing in ingredients:
        fid = ing.get("fdc_id")
        ann = ann_map.get(fid)
        if not fid or ann is None or ann["gi_estimate"] is None:
            continue
        nuts = ing.get("nutrients_100g") or {}
        row = by_food.setdefault(fid, {
            "food_name": ing["food_name"], "fdc_id": fid, "recipe_id": None,
            "amount": 0.0, "grams": 0.0, "gi": ann["gi_estimate"],
            "carbs_100g": nuts.get("carbs_g") or 0.0,
            "impaired": _gl.gi_measured_impaired(ann["gi_source"]),
        })
        row["grams"] += ing["grams"]
        row["amount"] += ann["gi_estimate"] * (nuts.get("carbs_g") or 0.0) * ing["grams"] / 10000.0
    contributions = [c for c in by_food.values() if c["amount"] > 0]
    total = sum(c["amount"] for c in contributions)
    contributions.sort(key=lambda c: c["amount"], reverse=True)
    for c in contributions:
        c["pct"] = round(c["amount"] / total * 100, 4) if total else 0.0
    return {"items": contributions, "total": total,
            "gaps": [g for g in whole["gaps"] if g["reason"] == _gl.GAP_NO_GI],
            "coverage_pct": whole["coverage_pct"]}


# Each nutrient's entry in the manual's Appendix G (Full Nutrient Key), whose
# "Where to find it" line says where to get data a food lacks. Amino acids
# (DCP) have no G entry of their own; their advice is under #key-sources.
_SOURCE_ANCHORS = {
    "calories": "key-calories", "protein_g": "key-protein", "carbs_g": "key-carbs",
    "fiber_g": "key-fiber", "sugar_g": "key-sugar", "fat_g": "key-fat",
    "saturated_fat_g": "key-saturated-fat", "mono_fat_g": "key-mono-fat", "poly_fat_g": "key-poly-fat",
    "water_g": "key-water", "water_drinks_g": "key-water", "water_food_g": "key-water",
    "omega3_ala_mg": "key-ala", "omega3_epa_mg": "key-epa", "omega3_dha_mg": "key-dha", "omega6_la_mg": "key-la",
    "calcium_mg": "key-calcium", "iron_mg": "key-iron", "magnesium_mg": "key-magnesium",
    "phosphorus_mg": "key-phosphorus", "potassium_mg": "key-potassium", "sodium_mg": "key-sodium",
    "zinc_mg": "key-zinc", "iodine_mcg": "key-iodine", "selenium_mcg": "key-selenium",
    "vitamin_a_mcg": "key-vitamin-a", "vitamin_c_mg": "key-vitamin-c", "vitamin_d_mcg": "key-vitamin-d",
    "vitamin_e_mg": "key-vitamin-e", "vitamin_k_mcg": "key-vitamin-k", "thiamin_mg": "key-thiamin",
    "riboflavin_mg": "key-riboflavin", "niacin_mg": "key-niacin", "b6_mg": "key-b6",
    "folate_mcg": "key-folate", "b12_mcg": "key-b12",
    "beta_carotene_mcg": "key-beta-carotene", "alpha_carotene_mcg": "key-alpha-carotene",
    "lycopene_mcg": "key-lycopene", "lutein_zeaxanthin_mcg": "key-lutein", "choline_mg": "key-choline",
    "beta_sitosterol_mg": "key-beta-sitosterol", "isoflavones_mg": "key-isoflavones",
}


def source_anchor(nutrient_key: str, *, is_dcp: bool = False) -> str:
    """Manual anchor saying where to find data for `nutrient_key` (with
    is_dcp, amino acids) — linked from the no-data table under Top
    Contributors. Falls back to the general ranked list of sources."""
    if is_dcp:
        return "key-sources-aa"
    return _SOURCE_ANCHORS.get(nutrient_key, "key-sources")


def fill_url(row: dict, nutrient_key: str, *, is_dcp: bool = False, custom_profile: bool = False) -> str | None:
    """Where to fill in a no-data food from another food, searching for its
    own name: Fill in nutrients from another food, or a custom profile's
    Edit page (which has the same searches, one for amino acids and one for
    other nutrients). None for a recipe or a name-only food. `want` names
    the nutrient the search is for (aa for amino acids)."""
    fdc_id = row.get("fdc_id")
    if not fdc_id or row.get("recipe_id"):
        return None
    name = row["food_name"].lstrip("* ").strip()
    want = "aa" if is_dcp else nutrient_key
    if custom_profile:
        field = "aa_source_q" if is_dcp else "nutrient_source_q"
        return f"/food/custom-profiles/{fdc_id}/edit?" + urlencode({field: name})
    return f"/food/{fdc_id}/fill-from?" + urlencode({"q": name, "want": want})


def missing_contributors(ingredients: list[dict], nutrient_key: str, *, is_dcp: bool = False) -> list[dict]:
    """Foods in `ingredients` with no data for `nutrient_key` — the key is
    absent from their per-100 g nutrients (a stored 0 is data, and is not
    listed). With is_dcp, foods with protein but no amino acid data instead
    (they score no DCP), or with no protein figure at all. These can't be
    ranked, so a meal's or recipe's total may be understated by them.

    `ingredients` should be leaf foods, so a sub-recipe's own gaps show.
    The same food reached twice is one row. Returns [{"food_name", "fdc_id",
    "recipe_id", "grams"}], heaviest first."""
    rows: dict = {}
    for ing in ingredients:
        grams = ing.get("grams") or 0.0
        if grams <= 0:
            continue
        per100 = ing.get("nutrients_100g") or {}
        if is_dcp:
            protein = per100.get("protein_g")
            lacking = protein is None or (protein > 0 and not _usda.has_amino_acid_data(per100))
        else:
            lacking = per100.get(nutrient_key) is None
        if not lacking:
            continue
        rid = ing.get("recipe_id")
        key = ing.get("fdc_id") or (("r", rid) if rid else ("n", ing["food_name"]))
        row = rows.setdefault(key, {"food_name": ing["food_name"], "fdc_id": ing.get("fdc_id"),
                                    "recipe_id": ing.get("recipe_id"), "grams": 0.0})
        row["grams"] += grams
    return sorted(rows.values(), key=lambda r: r["grams"], reverse=True)
