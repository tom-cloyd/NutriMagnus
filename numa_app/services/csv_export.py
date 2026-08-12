"""
csv_export.py — Food Cache CSV export.

Flat, one-row-per-food dump for trading foods between users or opening in a
spreadsheet: identity/metadata columns, then a JSON-encoded portions cell,
then one column per nutrient key (per 100g, same convention as
foods.nutrients_json). Column order is driven by usda.NUTRIENT_MAP so it
can't drift out of sync with the nutrients numa actually understands.

Import (numa_app/services/csv_import.py, not yet written) is expected to
read back exactly these columns.
Docs: README-numa-documentation.md, Project Structure
"""
import csv
import io
import json

import usda as _usda

NUTRIENT_COLUMNS: list[str] = [v[0] for v in _usda.NUTRIENT_MAP.values()]

_META_COLUMNS = ["fdc_id", "name", "data_type", "brand", "serving_size", "serving_unit",
                  "notes", "portions"]

CSV_COLUMNS: list[str] = _META_COLUMNS + NUTRIENT_COLUMNS


def foods_to_csv(rows: list) -> str:
    """Render cached-food rows (sqlite3.Row, as from db.list_cached_foods) to CSV text."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        nutrients = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
        portions_json = row["portions_json"]
        portions = json.loads(portions_json) if portions_json and portions_json != "null" else []
        record = {
            "fdc_id":       row["fdc_id"],
            "name":         row["name"],
            "data_type":    row["data_type"] or "",
            "brand":        row["brand"] or "",
            "serving_size": row["serving_size"] if row["serving_size"] is not None else "",
            "serving_unit": row["serving_unit"] or "",
            "notes":        row["notes"] or "",
            "portions":     json.dumps(portions),
        }
        for key in NUTRIENT_COLUMNS:
            if key in nutrients:
                record[key] = nutrients[key]
        writer.writerow(record)
    return buf.getvalue()
