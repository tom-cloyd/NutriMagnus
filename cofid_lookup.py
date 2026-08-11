"""
cofid_lookup.py — local name search over the bundled UK CoFID dataset.

CoFID (McCance and Widdowson's Composition of Foods Integrated Dataset,
2021) has no live API — only a downloadable spreadsheet. cofid_data.json is
the one-time ingest result (see scripts/build_cofid_data.py): ~2,900 UK
foods, already mapped onto numa's shared per-100g nutrient keys. This module
is registered as a "static" source in web/backend.py's source registry —
an external database with its own citation, like USDA/OFF/CNF, but searched
instantly (no network call) the same way Pantry/Food Cache are.

No amino-acid data: CoFID's public dataset has no amino-acid sheet at all
(unlike Canadian Nutrient File or AFCD) — see scripts/build_cofid_data.py's
docstring for exactly what it does and doesn't cover.

The actual local-search/lookup logic lives in
numa_app.services.static_source_lookup.StaticSource, shared with
afcd_lookup.py and ciqual_lookup.py — this module is just that class pointed
at CoFID's own data file and reserved id range.

Synthetic fdc_id assignment:
  CoFID food codes are strings (e.g. "18-070"), not USDA FDC IDs. We assign
  deterministic negative IDs in the range -5_000_000_000 to -4_000_000_000
  (see food_ids._SYNTHETIC_ID_RANGES), well separated from OFF's and CNF's.
Docs: README-numa-documentation.md, Architecture: "cofid_lookup.py — CoFID local search"
"""
from pathlib import Path

from numa_app.services.static_source_lookup import StaticSource

_DATA_PATH = Path(__file__).parent / "cofid_data.json"

# Synthetic fdc_id base for CoFID foods — see food_ids._SYNTHETIC_ID_RANGES.
_COFID_ID_BASE = -4_000_000_000

_source = StaticSource(_DATA_PATH, _COFID_ID_BASE, "CoFID")


def cofid_id(food_code: str) -> int:
    return _source.food_id(food_code)


def is_cofid_id(fdc_id: int) -> bool:
    return _source.is_id(fdc_id)


def search_foods(query: str, page_size: int = 15) -> list[dict]:
    return _source.search_foods(query, page_size)


def get_food_detail(cofid_result: dict) -> dict:
    return _source.get_food_detail(cofid_result)


def get_food_detail_by_id(fdc_id: int) -> dict | None:
    return _source.get_food_detail_by_id(fdc_id)
