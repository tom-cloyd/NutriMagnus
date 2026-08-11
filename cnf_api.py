"""
cnf_api.py — Canadian Nutrient File API client for numa.

API docs: https://food-nutrition.canada.ca/api/canadian-nutrient-file/
No API key required. Data is Health Canada's reference database.

Unlike USDA/Open Food Facts, CNF has no server-side "search by name" endpoint
— it only serves bulk dumps of its relational tables. /food/?type=json returns
every food (food_code + food_description) in one call; nutrient amounts for a
specific food come from a separate /nutrientamount/?type=json&id=<food_code>
call. So "search" here means: fetch the full food list once (cached for the
life of the process — it changes rarely), then filter it locally by name,
the same way a bundled static dataset would. Detail lookups are still a real
network call per food, so this is registered as a "live" source, not static.

Nutrient values are per 100 g. Amino acids and most nutrients map cleanly by
CNF's stable nutrient_symbol (see _NUTRIENT_MAP) — confirmed against the
/nutrientname/?type=json endpoint, not the numeric nutrient_name_id, since
symbols are the more stable/documented identifier.

Synthetic fdc_id assignment:
  CNF food_codes are not USDA FDC IDs. We assign deterministic negative IDs
  in the range -4_000_000_000 to -3_000_000_000 (see food_ids._SYNTHETIC_ID_RANGES),
  well separated from Open Food Facts' and user-drafted foods' ranges.
Docs: README-numa-documentation.md, Architecture: "cnf_api.py — Canadian Nutrient File API client"
"""

import json
import urllib.error
import urllib.parse
import urllib.request

_BASE_URL = "https://food-nutrition.canada.ca/api/canadian-nutrient-file"

# Synthetic fdc_id base for CNF foods — see food_ids._SYNTHETIC_ID_RANGES.
_CNF_ID_BASE = -3_000_000_000

# Maps CNF nutrient_symbol (per 100 g) → (our_key, multiplier). Multiplier
# converts from CNF's unit to ours (most are 1.0; CNF's omega fatty acids are
# in g, ours are in mg). Iodine has no CNF entry, so it's simply absent here.
_NUTRIENT_MAP: dict[str, tuple[str, float]] = {
    "KCAL":       ("calories",         1.0),
    "PROT":       ("protein_g",        1.0),
    "CARB":       ("carbs_g",          1.0),
    "FAT":        ("fat_g",            1.0),
    "TDF":        ("fiber_g",          1.0),
    "TSUG":       ("sugar_g",          1.0),
    "TSAT":       ("saturated_fat_g",  1.0),
    "MUFA":       ("mono_fat_g",       1.0),
    "PUFA":       ("poly_fat_g",       1.0),
    "18:3undiff": ("omega3_ala_mg",    1000.0),
    "20:5n-3EPA": ("omega3_epa_mg",    1000.0),
    "22:6n-3DHA": ("omega3_dha_mg",    1000.0),
    "18:2undiff": ("omega6_la_mg",     1000.0),
    "CA":         ("calcium_mg",       1.0),
    "FE":         ("iron_mg",          1.0),
    "MG":         ("magnesium_mg",     1.0),
    "P":          ("phosphorus_mg",    1.0),
    "K":          ("potassium_mg",     1.0),
    "NA":         ("sodium_mg",        1.0),
    "ZN":         ("zinc_mg",          1.0),
    "SE":         ("selenium_mcg",     1.0),
    # Retinol only — CNF's closest single field to our vitamin_a_mcg, not a
    # full RAE figure that also accounts for provitamin-A carotenoids.
    "RT-µG":      ("vitamin_a_mcg",    1.0),
    "VITC":       ("vitamin_c_mg",     1.0),
    "D3+D2-µG":   ("vitamin_d_mcg",    1.0),
    "ATMG":       ("vitamin_e_mg",     1.0),
    "VITK":       ("vitamin_k_mcg",    1.0),
    "THIA":       ("thiamin_mg",       1.0),
    "RIBO":       ("riboflavin_mg",    1.0),
    "N-MG":       ("niacin_mg",        1.0),
    "B6":         ("b6_mg",            1.0),
    "FOLA":       ("folate_mcg",       1.0),
    "B12":        ("b12_mcg",          1.0),
    "CHOLN":      ("choline_mg",       1.0),
    "TRP":        ("aa_tryptophan_g",    1.0),
    "THR":        ("aa_threonine_g",     1.0),
    "ISO":        ("aa_isoleucine_g",    1.0),
    "LEU":        ("aa_leucine_g",       1.0),
    "LYS":        ("aa_lysine_g",        1.0),
    "MET":        ("aa_methionine_g",    1.0),
    "CYS":        ("aa_cystine_g",       1.0),
    "PHE":        ("aa_phenylalanine_g", 1.0),
    "TYR":        ("aa_tyrosine_g",      1.0),
    "VAL":        ("aa_valine_g",        1.0),
    "HIS":        ("aa_histidine_g",     1.0),
}

# Cache of the full food list — one bulk fetch per process lifetime rather
# than per search, since /food/?type=json takes no filter param and the
# reference data changes rarely. None until first search_foods() call.
_food_list_cache: list[dict] | None = None


class CNFError(Exception):
    pass


def cnf_id(food_code: int) -> int:
    """Return a deterministic negative fdc_id for a CNF food_code."""
    return _CNF_ID_BASE - (food_code % 1_000_000_000)


def is_cnf_id(fdc_id: int) -> bool:
    """Return True if this fdc_id was assigned by the CNF client."""
    return _CNF_ID_BASE - 1_000_000_000 <= fdc_id <= _CNF_ID_BASE


def _http_get(url: str) -> object:
    req = urllib.request.Request(
        url, headers={"User-Agent": "numa/0.1 (nutritional-analysis; contact via github)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise CNFError(f"HTTP {e.code}") from e
    except urllib.error.URLError as e:
        raise CNFError(f"Network error: {e.reason}") from e


def _food_list() -> list[dict]:
    """Every CNF food (food_code + food_description), fetched once and cached
    for the life of the process. Raises CNFError on failure — callers decide
    whether to degrade gracefully."""
    global _food_list_cache
    if _food_list_cache is None:
        data = _http_get(f"{_BASE_URL}/food/?type=json")
        _food_list_cache = data if isinstance(data, list) else []
    return _food_list_cache


def search_foods(query: str, page_size: int = 15) -> list[dict]:
    """
    Search CNF by food name (local substring match over the cached bulk food
    list — see module docstring). Returns a list of result dicts with the
    same keys used by usda.search_foods() plus a '_from_cnf' marker.

    Returns [] silently on any network or API error so callers can degrade
    gracefully, matching usda.search_foods()/openfoodfacts.search_foods().
    """
    try:
        foods = _food_list()
    except CNFError:
        return []

    words = query.lower().split()
    if not words:
        return []
    results = []
    for food in foods:
        desc = (food.get("food_description") or "").strip()
        code = food.get("food_code")
        if not desc or code is None:
            continue
        desc_lower = desc.lower()
        if not all(w in desc_lower for w in words):
            continue
        results.append({
            "fdcId":       cnf_id(code),
            "description": desc,
            "dataType":    "Canadian Nutrient File",
            "brandOwner":  None,
            "brandName":   None,
            "_from_cnf":   True,
            "_cnf_code":   code,
        })
        if len(results) >= page_size:
            break
    return results


def get_food_detail(cnf_result: dict) -> dict:
    """
    Fetch full nutrient detail for a search result from search_foods() (or
    any dict carrying '_cnf_code'). One network call — CNF's search step is
    local, but detail is not cached client-side like OFF's search response.
    Returns the same format as usda.get_food_detail(). Raises CNFError on
    failure so callers can show/handle it (matching usda.get_food_detail()'s
    behavior, unlike the empty-list-on-error style of search_foods()).
    """
    code = cnf_result.get("_cnf_code")
    if code is None:
        raise CNFError("missing CNF food_code")
    fdc_id = cnf_id(code)
    amounts = _http_get(f"{_BASE_URL}/nutrientamount/?type=json&id={code}")
    nutrients: dict[str, float] = {}
    if isinstance(amounts, list):
        for entry in amounts:
            symbol = entry.get("nutrient_symbol")
            mapped = _NUTRIENT_MAP.get(symbol)
            if not mapped:
                continue
            our_key, multiplier = mapped
            val = entry.get("nutrient_value")
            if val is None:
                continue
            try:
                nutrients[our_key] = float(val) * multiplier
            except (TypeError, ValueError):
                pass

    return {
        "fdcId":            fdc_id,
        "name":             cnf_result.get("description", "Unknown"),
        "dataType":         "Canadian Nutrient File",
        "brand":            None,
        "servingSize":      None,
        "servingUnit":      None,
        "householdServing": None,
        "nutrients":        nutrients,
        "portions":         [],
        "_from_cnf":        True,
        "_cnf_code":        code,
    }


def get_food_detail_by_id(fdc_id: int) -> dict | None:
    """Look up full detail directly by a CNF-scoped fdc_id (no cached search
    result on hand) — used when re-fetching a not-yet-cached food, the same
    role openfoodfacts.lookup_by_barcode() plays for OFF. Requires the food
    list to already be cached (i.e. a search has run this process) to recover
    the description and real food_code from the synthetic id; returns None if
    not found there or on any network error."""
    code = _CNF_ID_BASE - fdc_id
    try:
        foods = _food_list()
    except CNFError:
        return None
    match = next((f for f in foods if f.get("food_code") == code), None)
    if match is None:
        return None
    try:
        return get_food_detail({"description": match.get("food_description", ""), "_cnf_code": code})
    except CNFError:
        return None
