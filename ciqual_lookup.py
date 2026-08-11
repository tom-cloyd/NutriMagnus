"""
ciqual_lookup.py — local name search over the bundled French CIQUAL dataset.

CIQUAL (ANSES, 2020) has no live API — only a downloadable spreadsheet.
ciqual_data.json is the one-time ingest result (see
scripts/build_ciqual_data.py): ~3,186 French foods, already mapped onto
numa's shared per-100g nutrient keys. This module is registered as a
"static" source in web/backend.py's source registry — an external database
with its own citation, like USDA/OFF/CNF, but searched instantly (no
network call) the same way Pantry/Food Cache are.

No amino-acid data: CIQUAL's public dataset has none (unlike Canadian
Nutrient File or AFCD) — see scripts/build_ciqual_data.py's docstring.

The actual local-search/lookup logic lives in
numa_app.services.static_source_lookup.StaticSource, shared with
cofid_lookup.py and afcd_lookup.py — this module is just that class pointed
at CIQUAL's own data file and reserved id range.

Synthetic fdc_id assignment:
  CIQUAL food codes ("alim_code") are plain integers, but not USDA FDC IDs.
  We assign deterministic negative IDs in the range -7_000_000_000 to
  -6_000_000_000 (see food_ids._SYNTHETIC_ID_RANGES), well separated from
  OFF's, CNF's, CoFID's, and AFCD's.
Docs: README-numa-documentation.md, Architecture: "ciqual_lookup.py — CIQUAL local search"
"""
from pathlib import Path

from numa_app.services.static_source_lookup import StaticSource

_DATA_PATH = Path(__file__).parent / "ciqual_data.json"

# Synthetic fdc_id base for CIQUAL foods — see food_ids._SYNTHETIC_ID_RANGES.
_CIQUAL_ID_BASE = -6_000_000_000

_source = StaticSource(_DATA_PATH, _CIQUAL_ID_BASE, "CIQUAL")


def ciqual_id(food_code: int) -> int:
    return _source.food_id(food_code)


def is_ciqual_id(fdc_id: int) -> bool:
    return _source.is_id(fdc_id)


def search_foods(query: str, page_size: int = 15) -> list[dict]:
    return _source.search_foods(query, page_size)


def get_food_detail(ciqual_result: dict) -> dict:
    return _source.get_food_detail(ciqual_result)


def get_food_detail_by_id(fdc_id: int) -> dict | None:
    return _source.get_food_detail_by_id(fdc_id)
