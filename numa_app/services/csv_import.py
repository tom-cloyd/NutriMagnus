"""
csv_import.py — Food Cache CSV import: parse a CSV in the shape
csv_export.foods_to_csv() produces into validated food dicts, then write
them to the cache.

Pure parsing only in parse_foods_csv() — no HTML/DB there — web/backend.py
wraps it in the same preview/confirm pattern already used for the Claude AI
import flow (numa_app/services/claude_fetch.py).
Docs: README-numa-documentation.md, Project Structure
"""
from __future__ import annotations

import csv
import io
import json

from .csv_export import NUTRIENT_COLUMNS

_KNOWN_COLUMNS = set(NUTRIENT_COLUMNS) | {
    "fdc_id", "name", "data_type", "brand",
    "serving_size", "serving_unit", "notes", "portions",
}


def parse_foods_csv(content: str) -> tuple[list[dict], list[str]]:
    """Parse CSV text into (valid_foods, warnings).

    Each valid_foods entry: {name, data_type, brand, serving_size,
    serving_unit, notes, portions, nutrients}. A row's own 'fdc_id' column
    (if present) is ignored — it belongs to whatever install exported it
    and would collide with unrelated foods here; import_foods() allocates
    a fresh one. Rows missing a name or any usable nutrient value are
    skipped and reported as a warning rather than failing the whole file.
    """
    warnings: list[str] = []
    reader = csv.DictReader(io.StringIO(content))
    fieldnames = reader.fieldnames or []

    if "name" not in fieldnames:
        warnings.append("CSV has no 'name' column — nothing to import.")
        return [], warnings

    unknown = [f for f in fieldnames if f not in _KNOWN_COLUMNS]
    if unknown:
        warnings.append(f"Ignoring unrecognised column(s): {', '.join(unknown)}")

    valid: list[dict] = []
    for i, row in enumerate(reader, 1):
        name = (row.get("name") or "").strip()
        if not name:
            warnings.append(f"Row {i}: missing 'name' — skipped.")
            continue

        nutrients: dict[str, float] = {}
        for key in NUTRIENT_COLUMNS:
            raw = (row.get(key) or "").strip()
            if not raw:
                continue
            try:
                nutrients[key] = float(raw)
            except ValueError:
                warnings.append(f"Row {i} ({name!r}): {key!r} value {raw!r} is not a number — skipped.")

        portions = _parse_portions_cell(row.get("portions"), i, name, warnings)

        serving_size_raw = (row.get("serving_size") or "").strip()
        serving_size = None
        if serving_size_raw:
            try:
                serving_size = float(serving_size_raw)
            except ValueError:
                warnings.append(
                    f"Row {i} ({name!r}): 'serving_size' value {serving_size_raw!r} is not a number — ignored."
                )

        if not nutrients:
            warnings.append(f"Row {i} ({name!r}): no usable nutrient values — skipped.")
            continue

        valid.append({
            "name":         name,
            "data_type":    (row.get("data_type") or "").strip() or "User Drafted",
            "brand":        (row.get("brand") or "").strip() or None,
            "serving_size": serving_size,
            "serving_unit": (row.get("serving_unit") or "").strip() or None,
            "notes":        (row.get("notes") or "").strip() or None,
            "portions":     portions,
            "nutrients":    nutrients,
        })

    return valid, warnings


def _parse_portions_cell(raw_cell: str | None, row_num: int, name: str, warnings: list[str]) -> list[dict]:
    raw = (raw_cell or "").strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        warnings.append(f"Row {row_num} ({name!r}): 'portions' is not valid JSON — ignored.")
        return []
    if not isinstance(parsed, list):
        warnings.append(f"Row {row_num} ({name!r}): 'portions' is not a list — ignored.")
        return []

    portions: list[dict] = []
    for p in parsed:
        if not isinstance(p, dict) or "description" not in p or "gram_weight" not in p:
            warnings.append(f"Row {row_num} ({name!r}): skipped a malformed portion entry.")
            continue
        try:
            portions.append({
                "description": str(p["description"]),
                "gram_weight": float(p["gram_weight"]),
            })
        except (TypeError, ValueError):
            warnings.append(f"Row {row_num} ({name!r}): skipped a portion with a non-numeric gram_weight.")
    return portions


def _create_food(conn, f: dict) -> int:
    import db as _db
    fdc_id = _db.next_user_drafted_fdc_id(conn)
    _db.cache_food(
        conn,
        fdc_id=fdc_id,
        name=f["name"],
        data_type=f["data_type"],
        brand=f["brand"],
        serving_size=f["serving_size"],
        serving_unit=f["serving_unit"],
        nutrients=f["nutrients"],
        portions=f["portions"],
        user_drafted=True,
        notes=f["notes"],
    )
    return fdc_id


def import_foods(conn, valid: list[dict]) -> list[int]:
    """Write validated food dicts to the cache as user-drafted foods with
    freshly-allocated IDs, always creating a new entry. Returns the assigned
    fdc_ids. Used by the plain Food Cache import flow, where the user has
    already previewed and confirmed each row themselves."""
    return [_create_food(conn, f) for f in valid]


def resolve_or_import_foods(conn, valid: list[dict]) -> dict[str, int]:
    """Like import_foods(), but reuses an existing cache entry when its name
    already matches (case-insensitively) instead of creating a duplicate.
    Returns {lowercased name: fdc_id} for every food in `valid`, whether
    newly created or matched to an existing entry.

    Used by recipe import, where a common ingredient (salt, water, an
    already-owned food) often already exists in the destination cache, and
    creating a fresh duplicate of it on every recipe import would clutter
    it — unlike a direct food import, nobody previews these individually."""
    import db as _db
    existing = {r["name"].strip().lower(): r["fdc_id"]
                for r in _db.list_cached_foods(conn, include_archived=True)}
    result: dict[str, int] = {}
    for f in valid:
        key = f["name"].strip().lower()
        if key in existing:
            result[key] = existing[key]
            continue
        fdc_id = _create_food(conn, f)
        existing[key] = fdc_id
        result[key] = fdc_id
    return result
