"""
import_json_folder.py — import one food per JSON file dropped into food_imports/.

Usage:
    1. Save each food as its own file in food_imports/, e.g. food_imports/triscuit.json.
       Shape (same as one Claude-response block — see import_foods.py docstring for
       the full nutrient key list and rules):

           {
             "name": "Full food name",
             "fdc_id": 123456,
             "fdc_type": "Branded",
             "source": "...",
             "confidence_note": "...",
             "calories": 0, "protein_g": 0, ...
           }

       For label data, use "serving_size_g" + "nutrition_per_serving" (same
       nutrient key names) instead of flat per-100g keys — numa converts to
       per-100g automatically.

    2. Run:  python import_json_folder.py

    3. Review the summary, confirm with y, and each file is imported and
       moved to food_imports/imported/.

Safe to re-run: cache_food() uses INSERT OR REPLACE.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import db as _db
from numa_app.services.food_import import convert_per_serving, validate_and_strip

_IMPORT_DIR = pathlib.Path(__file__).parent / "food_imports"
_DONE_DIR = _IMPORT_DIR / "imported"

_VALID_FDC_TYPES = {
    "Foundation", "SR Legacy", "Branded", "Survey (FNDDS)", "User Drafted", "OFF",
}


def _load_food(path: pathlib.Path) -> dict | None:
    try:
        block = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"  ✗  {path.name}: invalid JSON ({exc}) — skipped.")
        return None

    name = block.get("name")
    fdc_id = block.get("fdc_id")
    if not name or not isinstance(fdc_id, int):
        print(f"  ✗  {path.name}: missing 'name' or integer 'fdc_id' — skipped.")
        return None

    fdc_type = block.get("fdc_type", "User Drafted")
    if fdc_type not in _VALID_FDC_TYPES:
        print(f"  ⚠  {path.name}: unknown fdc_type {fdc_type!r} — using 'User Drafted'.")
        fdc_type = "User Drafted"

    notes_parts = []
    if block.get("source"):
        notes_parts.append(f"Source: {block['source']}")
    if block.get("confidence_note"):
        notes_parts.append(f"Confidence: {block['confidence_note']}")

    per_serving = block.get("nutrition_per_serving")
    serving_size_g = block.get("serving_size_g")
    if per_serving is not None:
        if not isinstance(serving_size_g, (int, float)) or serving_size_g <= 0:
            print(f"  ✗  {path.name}: 'nutrition_per_serving' given without a valid "
                  f"'serving_size_g' — skipped.")
            return None
        clean, stripped = validate_and_strip(per_serving)
        nutrients = convert_per_serving(clean, float(serving_size_g))
        factor = 100 / float(serving_size_g)
        notes_parts.append(f"Converted from per-{serving_size_g:g}g label values (×{factor:.3f}).")
    else:
        meta_keys = {"name", "fdc_id", "fdc_type", "source", "confidence_note",
                     "serving_size_g", "nutrition_per_serving"}
        nutrients, stripped = validate_and_strip(
            {k: v for k, v in block.items() if k not in meta_keys}
        )

    if stripped:
        print(f"  [{path.name}] stripped unrecognised keys: {', '.join(stripped)}")

    return {
        "path": path,
        "name": name,
        "fdc_id": fdc_id,
        "fdc_type": fdc_type,
        "notes": "  |  ".join(notes_parts) or None,
        "nutrients": nutrients,
    }


def main() -> None:
    _IMPORT_DIR.mkdir(exist_ok=True)
    files = sorted(_IMPORT_DIR.glob("*.json"))
    if not files:
        print(f"No .json files in {_IMPORT_DIR} — nothing to import.")
        return

    print(f"Found {len(files)} file(s) in {_IMPORT_DIR}. Validating…\n")
    foods = [f for f in (_load_food(p) for p in files) if f]
    if not foods:
        print("\nNo valid food records after validation.")
        return

    print()
    for f in foods:
        n = f["nutrients"]
        aa_count = sum(1 for k in n if k.startswith("aa_"))
        print(f"  {f['name']}  (FDC {f['fdc_id']}, {f['fdc_type']})  "
              f"— {n.get('calories', 0):.0f} cal, {n.get('protein_g', 0):.1f}g protein, "
              f"{aa_count} AAs")

    answer = input(f"\nImport {len(foods)} food(s) into cache? [y/N] ").strip().lower()
    if answer != "y":
        print("Cancelled — no files moved.")
        return

    _DONE_DIR.mkdir(exist_ok=True)
    with _db.get_db() as conn:
        for f in foods:
            _db.cache_food(
                conn,
                fdc_id=f["fdc_id"],
                name=f["name"],
                data_type=f["fdc_type"],
                brand=None,
                serving_size=None,
                serving_unit=None,
                nutrients=f["nutrients"],
                notes=f["notes"],
                user_drafted=True,
            )
            f["path"].rename(_DONE_DIR / f["path"].name)

    print(f"\nDone. Imported {len(foods)} food(s); files moved to {_DONE_DIR}.")


if __name__ == "__main__":
    main()
