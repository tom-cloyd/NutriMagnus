#!/usr/bin/env python3
"""
export_starter_data.py — regenerate numa_app/services/starter_data.json from
whatever foods/pantry/recipes in the real database are marked as starter
content by a leading "* " in their name.

This is how starter content is curated: rename or create a food/pantry entry/
recipe in the app itself with a name starting with "* ", then run this script
before cutting a release. numa_app/services/demo_data.py reads the resulting
JSON — it has no starter data of its own baked in.

A recipe is only exported if every one of its ingredients is also a starred
food, since numa_app.services.demo_data.load_demo_data() resolves ingredient
fdc_ids by looking up each ingredient's food name among the starred foods.
Recipes that reference a non-starred ingredient are skipped, with a warning.

Run from the repo root:
    python scripts/export_starter_data.py
"""
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import db as _db

OUTPUT = REPO_ROOT / "numa_app" / "services" / "starter_data.json"
_PREFIX = "* "


def main() -> int:
    with _db.get_db() as conn:
        food_rows = conn.execute(
            "SELECT fdc_id, name, data_type, nutrients_json, portions_json "
            "FROM foods WHERE name LIKE ? AND archived = 0",
            (_PREFIX + "%",),
        ).fetchall()
        foods = [
            {
                "fdc_id": row["fdc_id"],
                "name": row["name"],
                "data_type": row["data_type"],
                "nutrients": json.loads(row["nutrients_json"]),
                "portions": json.loads(row["portions_json"] or "[]"),
            }
            for row in food_rows
        ]
        starred_food_names = {f["name"] for f in foods}

        pantry_rows = _db.pantry_list(conn)
        pantry = [
            row["food_name"] for row in pantry_rows
            if row["food_name"].startswith(_PREFIX) and row["food_name"] in starred_food_names
        ]

        recipes = []
        for summary in _db.recipe_list(conn):
            if not summary["name"].startswith(_PREFIX):
                continue
            full = _db.recipe_get(conn, summary["id"])
            ingredient_rows = _db.recipe_get_ingredients(conn, summary["id"])
            ingredients = [(r["food_name"], r["amount"], r["unit"]) for r in ingredient_rows]
            bad = [name for name, _, _ in ingredients if name not in starred_food_names]
            if bad:
                print(f"WARNING: skipping recipe {full['name']!r} — "
                      f"ingredient(s) not starred: {bad}", file=sys.stderr)
                continue
            recipes.append({
                "name": full["name"],
                "description": full["description"] or "",
                "servings": full["servings"],
                "instructions": full["instructions"] or "",
                "ingredients": ingredients,
            })

    OUTPUT.write_text(json.dumps(
        {"foods": foods, "pantry": pantry, "recipes": recipes}, indent=2,
    ) + "\n")
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}: "
          f"{len(foods)} foods, {len(pantry)} pantry, {len(recipes)} recipes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
