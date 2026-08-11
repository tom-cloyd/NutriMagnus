"""
static_source_lookup.py — shared local-search machinery for bundled,
network-free food-composition datasets: CoFID, AFCD, CIQUAL, and any future
source that's a one-time download rather than a live API (see user-manual.md
Part 9, "Additional food nutrition database access").

Each concrete source (cofid_lookup.py, afcd_lookup.py, ciqual_lookup.py) is a
thin wrapper around one StaticSource instance, pointed at its own bundled
JSON file (see the matching scripts/build_<source>_data.py for how that JSON
is generated) and its own reserved synthetic-id range (see
numa_app.services.food_ids._SYNTHETIC_ID_RANGES). This was factored out of
cofid_lookup.py once a second source (AFCD) needed the identical logic —
CoFID's module-level public API (cofid_id(), search_foods(), etc.) is
unchanged, just delegating to a StaticSource internally now.

Docs: README-numa-documentation.md, Architecture: "static_source_lookup.py — shared static-dataset search"
"""
import hashlib
import json
from pathlib import Path


class StaticSource:
    def __init__(self, data_path: Path, id_base: int, data_type_label: str):
        self.data_path = data_path
        self.id_base = id_base
        self.data_type_label = data_type_label
        self._records_cache: list[dict] | None = None
        self._id_index_cache: dict[int, dict] | None = None

    def _records(self) -> list[dict]:
        """All records, loaded once and cached for the life of the process.
        Returns [] if the data file hasn't been generated (see this source's
        scripts/build_<source>_data.py) rather than raising, so the app
        degrades gracefully — search just finds nothing — instead of crashing."""
        if self._records_cache is None:
            if self.data_path.exists():
                self._records_cache = json.loads(self.data_path.read_text(encoding="utf-8"))
            else:
                self._records_cache = []
        return self._records_cache

    def _id_index(self) -> dict[int, dict]:
        if self._id_index_cache is None:
            self._id_index_cache = {self.food_id(r["food_code"]): r for r in self._records()}
        return self._id_index_cache

    def food_id(self, food_code) -> int:
        """Deterministic negative fdc_id for a source-specific food code —
        same hash-bucket approach openfoodfacts.off_id() uses for non-numeric ids."""
        bucket = int(hashlib.md5(str(food_code).encode()).hexdigest()[:8], 16) % 1_000_000_000
        return self.id_base - bucket

    def is_id(self, fdc_id: int) -> bool:
        """Return True if this fdc_id was assigned by this source instance."""
        return self.id_base - 1_000_000_000 <= fdc_id <= self.id_base

    def search_foods(self, query: str, page_size: int = 15) -> list[dict]:
        """
        Search by food name (local substring match — every query word must
        appear in the name). Returns a list of result dicts with the same
        keys used by usda.search_foods().
        """
        words = query.lower().split()
        if not words:
            return []
        results = []
        for rec in self._records():
            name = rec.get("name") or ""
            if not all(w in name.lower() for w in words):
                continue
            results.append({
                "fdcId":       self.food_id(rec["food_code"]),
                "description": name,
                "dataType":    self.data_type_label,
                "brandOwner":  None,
                "brandName":   None,
                "_static_code": rec["food_code"],
            })
            if len(results) >= page_size:
                break
        return results

    def get_food_detail(self, result: dict) -> dict:
        """
        Build a full food detail dict from a search_foods() result (or any
        dict carrying '_static_code'). No network call — the whole dataset
        is already in memory. Returns the same format as usda.get_food_detail().
        """
        code = result.get("_static_code")
        rec = self._id_index().get(self.food_id(code)) if code is not None else None
        return {
            "fdcId":            self.food_id(code) if code is not None else result.get("fdcId"),
            "name":             result.get("description") or (rec["name"] if rec else "Unknown"),
            "dataType":         self.data_type_label,
            "brand":            None,
            "servingSize":      None,
            "servingUnit":      None,
            "householdServing": None,
            "nutrients":        dict(rec["nutrients"]) if rec else {},
            "portions":         [],
            "_static_code":     code,
        }

    def get_food_detail_by_id(self, fdc_id: int) -> dict | None:
        """Look up full detail directly by a source-scoped fdc_id (no cached
        search result on hand). Returns None if not found."""
        rec = self._id_index().get(fdc_id)
        if rec is None:
            return None
        return self.get_food_detail({"description": rec["name"], "_static_code": rec["food_code"]})
