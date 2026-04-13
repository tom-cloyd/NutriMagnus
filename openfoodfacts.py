"""
openfoodfacts.py — Open Food Facts API client for numa.

API docs: https://openfoodfacts.github.io/openfoodfacts-server/api/
No API key required. Data is licensed CC BY-SA 4.0.

Nutrients in OFF responses are per 100 g, suffixed with _100g.
Minerals (sodium, calcium, iron, etc.) are in grams in OFF; we convert to mg.

Synthetic fdc_id assignment:
  OFF products do not have USDA FDC IDs. We assign deterministic negative IDs
  in the range -2_000_000_000 to -3_000_000_000 based on the product barcode,
  well separated from user-drafted foods (-1, -2, -3, …).
"""

import hashlib
import json
import re
import urllib.parse
import urllib.request

_BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"
_PRODUCT_URL = "https://world.openfoodfacts.org/api/v2/product"

# Synthetic fdc_id base for OFF products.
_OFF_ID_BASE = -2_000_000_000

# Maps OFF nutriment keys (per 100 g) → (our_key, multiplier).
# Multiplier converts from OFF unit to our unit (most are 1.0; minerals need *1000 g→mg).
_NUTRIENT_MAP: dict[str, tuple[str, float]] = {
    "energy-kcal_100g":           ("calories",         1.0),
    "proteins_100g":              ("protein_g",        1.0),
    "fat_100g":                   ("fat_g",            1.0),
    "carbohydrates_100g":         ("carb_g",           1.0),
    "fiber_100g":                 ("fiber_g",          1.0),
    "sugars_100g":                ("sugar_g",          1.0),
    "saturated-fat_100g":         ("saturated_fat_g",  1.0),
    "monounsaturated-fat_100g":   ("mono_fat_g",       1.0),
    "polyunsaturated-fat_100g":   ("poly_fat_g",       1.0),
    "sodium_100g":                ("sodium_mg",        1000.0),
    "calcium_100g":               ("calcium_mg",       1000.0),
    "iron_100g":                  ("iron_mg",          1000.0),
    "magnesium_100g":             ("magnesium_mg",     1000.0),
    "potassium_100g":             ("potassium_mg",     1000.0),
    "zinc_100g":                  ("zinc_mg",          1000.0),
    "vitamin-c_100g":             ("vitamin_c_mg",     1000.0),
}


class OFFError(Exception):
    pass


def off_id(barcode: str) -> int:
    """Return a deterministic negative fdc_id for an OFF product barcode."""
    try:
        n = int(barcode)
        bucket = n % 1_000_000_000
    except (ValueError, TypeError):
        bucket = int(hashlib.md5(str(barcode).encode()).hexdigest()[:8], 16) % 1_000_000_000
    return _OFF_ID_BASE - bucket


def is_off_id(fdc_id: int) -> bool:
    """Return True if this fdc_id was assigned by the OFF client."""
    return _OFF_ID_BASE - 1_000_000_000 <= fdc_id <= _OFF_ID_BASE


def _http_get(url: str) -> dict:
    req = urllib.request.Request(
        url, headers={"User-Agent": "numa/0.1 (nutritional-analysis; contact via github)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise OFFError(f"HTTP {e.code}") from e
    except urllib.error.URLError as e:
        raise OFFError(f"Network error: {e.reason}") from e


def search_foods(query: str, page_size: int = 8) -> list[dict]:
    """
    Search Open Food Facts. Returns a list of result dicts with the same keys
    used by usda.search_foods() plus '_from_off' and '_off_data' markers.

    Results are sorted by scan popularity (most-scanned = best-known products first).
    Returns [] silently on any network or API error so callers can degrade gracefully.
    """
    params = {
        "search_terms":  query,
        "action":        "process",
        "json":          "1",
        "page_size":     str(page_size),
        "sort_by":       "unique_scans_n",
        "fields":        "product_name,brands,nutriments,serving_size,serving_quantity,code",
    }
    url = f"{_BASE_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = _http_get(url)
    except OFFError:
        return []

    results = []
    for p in data.get("products", []):
        name = (p.get("product_name") or "").strip()
        barcode = (p.get("code") or "").strip()
        if not name or not barcode:
            continue
        brand = (p.get("brands") or "").split(",")[0].strip() or None
        fdc_id = off_id(barcode)
        results.append({
            "fdcId":       fdc_id,
            "description": name,
            "dataType":    "Open Food Facts",
            "brandOwner":  brand,
            "brandName":   brand,
            "_from_off":   True,
            "_off_code":   barcode,
            "_off_data":   p,
        })
    return results


def get_food_detail(off_result: dict) -> dict:
    """
    Build a full food detail dict from an OFF search result dict.
    The search result already contains nutrient data, so no second HTTP call
    is needed in the normal flow. Returns the same format as usda.get_food_detail().
    """
    return _parse_product(off_result.get("_off_data", {}), off_result["fdcId"])


def _parse_product(p: dict, fdc_id: int) -> dict:
    name = (p.get("product_name") or "Unknown").strip()
    brand = (p.get("brands") or "").split(",")[0].strip() or None
    barcode = p.get("code", "")

    # Parse serving size string, e.g. "30 g", "1 cup (240ml)", "28g"
    serving_size: float | None = None
    serving_unit: str | None = None
    srv_raw = (p.get("serving_size") or "").strip()
    if srv_raw:
        m = re.match(r"([\d.]+)\s*([a-zA-Z]+)", srv_raw)
        if m:
            try:
                serving_size = float(m.group(1))
                serving_unit = m.group(2).lower()
            except ValueError:
                pass

    nutriments = p.get("nutriments") or {}
    nutrients: dict[str, float] = {}
    for off_key, (our_key, multiplier) in _NUTRIENT_MAP.items():
        val = nutriments.get(off_key)
        if val is not None:
            try:
                nutrients[our_key] = float(val) * multiplier
            except (TypeError, ValueError):
                pass

    portions: list[dict] = []
    if serving_size and serving_unit and serving_unit in ("g", "gr", "gram", "grams"):
        portions.append({"description": srv_raw, "gram_weight": serving_size})

    return {
        "fdcId":            fdc_id,
        "name":             name,
        "dataType":         "Open Food Facts",
        "brand":            brand,
        "servingSize":      serving_size,
        "servingUnit":      serving_unit,
        "householdServing": srv_raw or None,
        "nutrients":        nutrients,
        "portions":         portions,
        "_from_off":        True,
        "_off_code":        barcode,
    }
