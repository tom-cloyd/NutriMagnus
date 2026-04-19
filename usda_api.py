"""
usda_api.py — USDA FoodData Central HTTP client for numa.

Handles API key management, food search, and detail fetching.
Called via usda.py which re-exports everything as usda.<name>.
Docs: README-numa-documentation.md, Architecture: "usda_api.py — USDA HTTP client"
"""
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request
from typing import Any

_CONFIG_FILE = pathlib.Path.home() / ".config" / "numa" / "config.json"
_BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# Nutrients we extract from USDA responses, keyed by USDA nutrient ID.
# Value is (our_key, display_label, unit).
NUTRIENT_MAP: dict[int, tuple[str, str, str]] = {
    # Macros
    1008: ("calories",          "Calories",           "kcal"),
    1003: ("protein_g",         "Protein",            "g"),
    1005: ("carbs_g",           "Carbohydrate",       "g"),
    1004: ("fat_g",             "Total Fat",          "g"),
    1079: ("fiber_g",           "Fiber",              "g"),
    1063: ("sugar_g",           "Sugars",             "g"),
    1258: ("saturated_fat_g",   "Saturated Fat",      "g"),
    1292: ("mono_fat_g",        "Monounsaturated Fat","g"),
    1293: ("poly_fat_g",        "Polyunsaturated Fat","g"),
    # Minerals
    1087: ("calcium_mg",        "Calcium",            "mg"),
    1089: ("iron_mg",           "Iron",               "mg"),
    1090: ("magnesium_mg",      "Magnesium",          "mg"),
    1091: ("phosphorus_mg",     "Phosphorus",         "mg"),
    1092: ("potassium_mg",      "Potassium",          "mg"),
    1093: ("sodium_mg",         "Sodium",             "mg"),
    1095: ("zinc_mg",           "Zinc",               "mg"),
    # Vitamins
    1106: ("vitamin_a_mcg",     "Vitamin A",          "mcg RAE"),
    1162: ("vitamin_c_mg",      "Vitamin C",          "mg"),
    1114: ("vitamin_d_mcg",     "Vitamin D",          "mcg"),
    1109: ("vitamin_e_mg",      "Vitamin E",          "mg"),
    1183: ("vitamin_k_mcg",     "Vitamin K",          "mcg"),
    1165: ("thiamin_mg",        "Thiamin (B1)",        "mg"),
    1166: ("riboflavin_mg",     "Riboflavin (B2)",     "mg"),
    1167: ("niacin_mg",         "Niacin (B3)",         "mg"),
    1175: ("b6_mg",             "Vitamin B6",          "mg"),
    1177: ("folate_mcg",        "Folate (B9)",         "mcg"),
    1178: ("b12_mcg",           "Vitamin B12",         "mcg"),
    # Phytonutrients / bioactive compounds
    1107: ("beta_carotene_mcg", "Beta-carotene",      "mcg"),
    1108: ("alpha_carotene_mcg","Alpha-carotene",     "mcg"),
    1122: ("lycopene_mcg",      "Lycopene",           "mcg"),
    1123: ("lutein_zeaxanthin_mcg", "Lutein+Zeaxanthin", "mcg"),
    1180: ("choline_mg",        "Choline",            "mg"),
    1285: ("beta_sitosterol_mg","Beta-sitosterol",    "mg"),
    1340: ("isoflavones_mg",    "Isoflavones",        "mg"),
    # Amino acids (essential)
    1210: ("aa_tryptophan_g",   "Tryptophan",         "g"),
    1211: ("aa_threonine_g",    "Threonine",          "g"),
    1212: ("aa_isoleucine_g",   "Isoleucine",         "g"),
    1213: ("aa_leucine_g",      "Leucine",            "g"),
    1214: ("aa_lysine_g",       "Lysine",             "g"),
    1215: ("aa_methionine_g",   "Methionine",         "g"),
    1216: ("aa_cystine_g",      "Cystine",            "g"),
    1217: ("aa_phenylalanine_g","Phenylalanine",      "g"),
    1218: ("aa_tyrosine_g",     "Tyrosine",           "g"),
    1219: ("aa_valine_g",       "Valine",             "g"),
    1221: ("aa_histidine_g",    "Histidine",          "g"),
}

# Essential amino acids (those humans cannot synthesize)
ESSENTIAL_AMINO_ACIDS = [
    "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
    "aa_lysine_g", "aa_methionine_g", "aa_phenylalanine_g", "aa_valine_g",
    "aa_histidine_g",
]

# WHO/FAO reference pattern for essential amino acids (mg per g of protein)
# Source: FAO 2013 dietary protein quality evaluation
AA_REFERENCE_MG_PER_G_PROTEIN = {
    "aa_tryptophan_g":    7,
    "aa_threonine_g":    23,
    "aa_isoleucine_g":   30,
    "aa_leucine_g":      59,
    "aa_lysine_g":       45,
    "aa_methionine_g":   22,   # methionine + cystine combined; simplified here
    "aa_phenylalanine_g":38,   # phe + tyr combined; simplified
    "aa_valine_g":       39,
    "aa_histidine_g":    15,
}


class USDAError(Exception):
    pass


def _load_config() -> dict:
    if _CONFIG_FILE.exists():
        return json.loads(_CONFIG_FILE.read_text())
    return {}


def _save_config(cfg: dict) -> None:
    _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(json.dumps(cfg, indent=2) + "\n")


def get_api_key() -> str | None:
    return _load_config().get("api_key")


def set_api_key(key: str) -> None:
    cfg = _load_config()
    cfg["api_key"] = "".join(c for c in key if c.isprintable()).strip()
    _save_config(cfg)


def _get(path: str, params: dict) -> Any:
    key = get_api_key() or "DEMO_KEY"
    params["api_key"] = key
    qs = urllib.parse.urlencode(params)
    url = f"{_BASE_URL}/{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "numa/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise USDAError(f"HTTP {e.code}: {body[:300]}") from e
    except urllib.error.URLError as e:
        raise USDAError(f"Network error: {e.reason}") from e


# Foods that the USDA search index fails to surface reliably, mapped to their
# FDC IDs and data type. Add entries here when a food is known to exist but
# search doesn't find it.
_SEARCH_ALIASES: list[tuple[tuple[str, ...], int, str, str]] = [
    # (keywords,                        fdc_id,  description,              data_type)
    # Note: nutritional yeast has no SR Legacy entry; AA data comes from complement table
    (("flax", "linseed"),               169414,  "Seeds, flaxseed",                            "SR Legacy"),
    (("chia",),                         170554,  "Seeds, chia seeds, dried",                   "SR Legacy"),
    (("okara",),                        2346405, "Okara",                                      "SR Legacy"),
    (("hemp seed", "hemp protein"),     170148,  "Seeds, hemp seed, hulled",                   "SR Legacy"),
    (("oat",),                          173904,  "Cereals, oats, regular and quick, not fortified, dry", "SR Legacy"),
]


def _alias_matches(query: str) -> list[dict]:
    """Return stub result dicts for any alias entries matching the query."""
    q = query.lower()
    matches = []
    for keywords, fdc_id, description, data_type in _SEARCH_ALIASES:
        if any(kw in q for kw in keywords):
            matches.append({
                "fdcId":        fdc_id,
                "description":  description,
                "dataType":     data_type,
                "brandOwner":   None,
                "brandName":    None,
                "_alias_has_aa": True,   # verified — skip cache lookup for AA status
            })
    return matches


def search_foods(query: str, page_size: int = 15,
                 data_types: list[str] | None = None) -> list[dict]:
    """
    Search USDA FoodData Central. Returns a list of result dicts with keys:
        fdcId, description, dataType, brandOwner, servingSize, servingSizeUnit,
        householdServingFullText

    Post-filters results so that every word in the query appears in the food
    description (case-insensitive). Fetches extra results to compensate for
    items removed by the filter.
    """
    if data_types is None:
        data_types = ["Foundation", "SR Legacy", "Branded"]
    params = {
        "query": query,
        "dataType": ",".join(data_types),
        "pageSize": page_size * 3,
        "pageNumber": 1,
    }
    data = _get("foods/search", params)
    all_results = data.get("foods", [])

    # Inject known aliases that the search index may not surface
    alias_ids = {r["fdcId"] for r in all_results}
    for alias in _alias_matches(query):
        if alias["fdcId"] not in alias_ids:
            all_results.insert(0, alias)
            alias_ids.add(alias["fdcId"])

    if not all_results:
        return []

    query_words = query.lower().split()
    if not query_words:
        return all_results[:page_size]

    def _score(food: dict) -> int:
        desc = food.get("description", "").lower()
        return sum(1 for w in query_words if w in desc)

    scored = sorted(all_results, key=_score, reverse=True)
    best = _score(scored[0])
    # If any result matches all words use strict threshold; otherwise allow within 1 of best
    threshold = len(query_words) if best == len(query_words) else max(1, best - 1)
    filtered = [f for f in scored if _score(f) >= threshold]
    return (filtered or scored)[:page_size]


def get_food_detail(fdc_id: int) -> dict:
    """
    Fetch full nutrient detail for one food. Returns a normalized dict with:
        fdcId, name, dataType, brand, servingSize, servingUnit,
        householdServing, nutrients (our key → value mapping)
    """
    data = _get(f"food/{fdc_id}", {})
    return _parse_food(data)


def _parse_food(data: dict) -> dict:
    """Normalize a USDA food response into our internal format."""
    fdc_id   = data.get("fdcId")
    name     = data.get("description", "Unknown")
    dtype    = data.get("dataType", "")
    brand    = data.get("brandOwner") or data.get("brandName")

    serving_size  = data.get("servingSize")
    serving_unit  = data.get("servingSizeUnit")
    household     = data.get("householdServingFullText")

    nutrients: dict[str, float] = {}

    # USDA returns nutrients as a list of objects; key format varies by endpoint
    raw_nutrients = data.get("foodNutrients", [])
    for item in raw_nutrients:
        # abridged endpoint uses "number" (string) as the nutrient ID
        nutrient_id = None
        if "nutrient" in item:
            # detailed endpoint
            nutrient_id = item["nutrient"].get("id")
        elif "nutrientId" in item:
            nutrient_id = item["nutrientId"]
        elif "number" in item:
            try:
                nutrient_id = int(item["number"])
            except (ValueError, TypeError):
                pass

        if nutrient_id is None:
            continue

        value = item.get("value") or item.get("amount")
        if value is None:
            continue

        if nutrient_id in NUTRIENT_MAP:
            key = NUTRIENT_MAP[nutrient_id][0]
            nutrients[key] = float(value)

    portions = []
    for p in data.get("foodPortions", []):
        desc = p.get("portionDescription") or p.get("modifier", "")
        gw = p.get("gramWeight")
        if desc and gw:
            portions.append({"description": desc, "gram_weight": float(gw)})

    # If USDA has no explicit portions but the food has a household serving description
    # (e.g. "1 Cup") paired with a numeric servingSize, synthesize a portion from it.
    # servingSize for Foundation/SR Legacy foods is typically in g or ml (≈g for liquids).
    if not portions and serving_size and household:
        portions.append({"description": household, "gram_weight": float(serving_size)})

    return {
        "fdcId":           fdc_id,
        "name":            name,
        "dataType":        dtype,
        "brand":           brand,
        "servingSize":     serving_size,
        "servingUnit":     serving_unit,
        "householdServing":household,
        "nutrients":       nutrients,
        "portions":        portions,
    }

