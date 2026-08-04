"""
search.py — cache-freshness helper shared by numa_app/services/recipe_nutrients.py.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/search.py — food lookup flow"
"""
import json

import db as _db
import usda as _usda


def _refresh_cache_if_missing_aa(fdc_id: int) -> dict | None:
    """
    If a cached food lacks amino acid data and is SR Legacy or Foundation,
    re-fetch it from the USDA API and update the cache.
    Returns the updated nutrients dict on success, None if not applicable or failed.
    Branded foods are skipped — they genuinely lack AA data in USDA.
    """
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if cached is None:
        return None
    if cached["user_drafted"]:
        return None  # never overwrite user-edited nutrient profiles
    nutrients = json.loads(cached["nutrients_json"])
    data_type = cached["data_type"] or ""
    if data_type == "Branded":
        return None  # branded foods won't have AA data regardless
    # Re-fetch if AA data is missing, OR if protein is 0 in an SR Legacy/Foundation food
    # (protein=0 in a curated food almost always means a corrupted/incomplete cache entry,
    # because has_amino_acid_data() short-circuits to True for protein=0 and would otherwise
    # silently suppress the refresh).
    protein_zero_suspect = (
        nutrients.get("protein_g", 0) == 0
        and data_type in ("SR Legacy", "Foundation")
    )
    if _usda.has_amino_acid_data(nutrients) and not protein_zero_suspect:
        return None  # already has AA data, nothing to do
    # Re-fetch full detail from API
    try:
        detail = _usda.get_food_detail(fdc_id)
    except (KeyboardInterrupt, _usda.USDAError):
        return None
    if not _usda.has_amino_acid_data(detail["nutrients"]):
        return None  # API also lacks AA data — nothing gained
    with _db.get_db() as conn:
        _db.cache_food(
            conn,
            detail["fdcId"], detail["name"], detail["dataType"], detail["brand"],
            detail["servingSize"], detail["servingUnit"], detail["nutrients"],
            detail.get("portions"),
        )
    return detail["nutrients"]
