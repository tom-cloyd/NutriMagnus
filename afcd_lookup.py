"""
afcd_lookup.py — local name search over the bundled Australian Food
Composition Database (AFCD) dataset.

AFCD (FSANZ, Release 3) has no live API — only downloadable spreadsheets.
afcd_data.json is the one-time ingest result (see scripts/build_afcd_data.py):
1,588 Australian foods, already mapped onto numa's shared per-100g nutrient
keys. This module is registered as a "static" source in web/backend.py's
source registry — an external database with its own citation, like
USDA/OFF/CNF, but searched instantly (no network call) the same way
Pantry/Food Cache are.

Unlike CoFID, AFCD DOES have amino-acid data — see
scripts/build_afcd_data.py's docstring for coverage details.

The actual local-search/lookup logic lives in
numa_app.services.static_source_lookup.StaticSource, shared with
cofid_lookup.py and ciqual_lookup.py — this module is just that class
pointed at AFCD's own data file and reserved id range.

Synthetic fdc_id assignment:
  AFCD food codes are strings ("Public Food Key", e.g. "F002258"), not USDA
  FDC IDs. We assign deterministic negative IDs in the range
  -6_000_000_000 to -5_000_000_000 (see food_ids._SYNTHETIC_ID_RANGES),
  well separated from OFF's, CNF's, and CoFID's.
Docs: README-numa-documentation.md, Architecture: "afcd_lookup.py — AFCD local search"
"""
from pathlib import Path

from numa_app.services.static_source_lookup import StaticSource

_DATA_PATH = Path(__file__).parent / "afcd_data.json"

# Synthetic fdc_id base for AFCD foods — see food_ids._SYNTHETIC_ID_RANGES.
_AFCD_ID_BASE = -5_000_000_000

_source = StaticSource(_DATA_PATH, _AFCD_ID_BASE, "AFCD")


def afcd_id(food_code: str) -> int:
    return _source.food_id(food_code)


def is_afcd_id(fdc_id: int) -> bool:
    return _source.is_id(fdc_id)


def search_foods(query: str, page_size: int = 15) -> list[dict]:
    return _source.search_foods(query, page_size)


def get_food_detail(afcd_result: dict) -> dict:
    return _source.get_food_detail(afcd_result)


def get_food_detail_by_id(fdc_id: int) -> dict | None:
    return _source.get_food_detail_by_id(fdc_id)
