#!/usr/bin/env python3
"""
refresh_starter_data.py — sync existing numa_app/services/starter_data.json
entries against the live database cache, without dropping anything.

Unlike export_starter_data.py (which rebuilds starter_data.json from scratch
from whatever is currently "*"-prefixed in the live DB — silently dropping
anything no longer starred), this script starts from the CURRENT
starter_data.json and only refreshes fields on entries it can still find
live, matched by stable ID rather than name (a starter item's name may have
been edited live since it was exported):

  - Foods: matched by fdc_id, which never changes even if the food is
    renamed. If still cached, name (re-prefixed), data_type, nutrients, and
    portions are refreshed from the live row — picking up e.g. a corrected
    portion or a re-pulled USDA value. If the fdc_id is no longer cached at
    all, the entry is left untouched.
  - Pantry: pantry entries are bare names tied 1:1 to a food entry. If that
    food's name changed above, the pantry name is updated to match so the
    by_name lookup in demo_data.py still resolves. Otherwise left as-is.
  - Recipes: matched by the "source_recipe_id" field export_starter_data.py
    stamps on each exported recipe (the live recipes.id at export time),
    not by name — a recipe survives being renamed live. Entries exported
    before this field existed have no source_recipe_id yet; those fall
    back to a one-time name match, and the discovered id is written back so
    every later refresh is ID-based. If a recipe's id no longer exists live
    (deleted), the entry is left untouched. An ingredient whose food isn't
    yet in starter_data.json's foods list (e.g. a new ingredient added live
    since the last export) is auto-included, the same way
    export_starter_data.py does it. A sub-recipe ingredient is unsupported,
    same as export_starter_data.py — that recipe entry is left untouched
    with a warning.

Nothing is ever removed — this script only updates fields on entries that
still resolve live; it never deletes an entry just because its live
counterpart is gone or unstarred. Run export_starter_data.py first to pick
up brand-new "* "-prefixed content; run this to catch up edits made to
already-exported starter items without needing to re-star them.

Run from the repo root:
    python scripts/refresh_starter_data.py
"""
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import db as _db

STARTER_DATA_FILE = REPO_ROOT / "numa_app" / "services" / "starter_data.json"
_PREFIX = "* "


def _is_starred(name: str) -> bool:
    return name.startswith("*")


def _canonical_name(name: str) -> str:
    """Normalize any starred name ("*Foo", "* Foo", "*  Foo", ...) to the
    canonical "* Foo" form; a live name with no "*" at all (destarred since
    the last export) still gets one, since this entry is already part of
    the starter set and must stay "* "-prefixed."""
    if _is_starred(name):
        return _PREFIX + name[1:].lstrip()
    return _PREFIX + name


def _food_dict(row, *, name: str | None = None) -> dict:
    return {
        "fdc_id": row["fdc_id"],
        "name": name if name is not None else row["name"],
        "data_type": row["data_type"],
        "nutrients": json.loads(row["nutrients_json"]),
        "portions": json.loads(row["portions_json"] or "[]"),
    }


def main() -> int:
    data = json.loads(STARTER_DATA_FILE.read_text())
    foods: list[dict] = data["foods"]
    pantry: list[str] = data["pantry"]
    recipes: list[dict] = data["recipes"]

    foods_by_fdc_id = {f["fdc_id"]: f for f in foods}
    name_changes: dict[str, str] = {}  # old starter name -> new starter name

    updated_foods = 0
    skipped_foods = 0
    added_foods = 0
    updated_recipes = 0
    skipped_recipes = 0

    with _db.get_db() as conn:
        for food in foods:
            row = _db.get_cached_food(conn, food["fdc_id"])
            if row is None:
                skipped_foods += 1
                continue
            new_food = _food_dict(row, name=_canonical_name(row["name"]))
            if new_food != food:
                if new_food["name"] != food["name"]:
                    name_changes[food["name"]] = new_food["name"]
                food.clear()
                food.update(new_food)
                updated_foods += 1

        for i, name in enumerate(pantry):
            if name in name_changes:
                pantry[i] = name_changes[name]

        for recipe in recipes:
            source_id = recipe.get("source_recipe_id")
            if source_id is None:
                # Legacy entry, exported before source_recipe_id existed:
                # match once by name, then self-heal the id for next time.
                legacy_match = next(
                    (r for r in _db.recipe_list(conn, include_archived=True)
                     if r["name"] == recipe["name"]),
                    None,
                )
                source_id = legacy_match["id"] if legacy_match else None

            full = _db.recipe_get(conn, source_id) if source_id is not None else None
            if full is None:
                skipped_recipes += 1
                continue

            ingredient_rows = _db.recipe_get_ingredients(conn, full["id"])
            recipe_name = _canonical_name(full["name"])

            skip_recipe = False
            new_ingredients = []
            for ing in ingredient_rows:
                if ing["ref_recipe_id"]:
                    print(f"WARNING: leaving recipe {recipe['name']!r} untouched — "
                          f"ingredient {ing['food_name']!r} is a sub-recipe, "
                          "which starter data doesn't support", file=sys.stderr)
                    skip_recipe = True
                    break
                if ing["fdc_id"] not in foods_by_fdc_id:
                    food_row = _db.get_cached_food(conn, ing["fdc_id"])
                    new_name = _canonical_name(food_row["name"])
                    new_food = _food_dict(food_row, name=new_name)
                    foods.append(new_food)
                    foods_by_fdc_id[ing["fdc_id"]] = new_food
                    added_foods += 1
                    print(f"NOTE: auto-including {food_row['name']!r} as "
                          f"{new_name!r} — used as an ingredient in "
                          f"{recipe_name!r} but not yet in starter_data.json", file=sys.stderr)
                new_ingredients.append(
                    [foods_by_fdc_id[ing["fdc_id"]]["name"], ing["amount"], ing["unit"]]
                )

            if skip_recipe:
                continue

            new_recipe = {
                "source_recipe_id": full["id"],
                "name": recipe_name,
                "description": full["description"] or "",
                "servings": full["servings"],
                "instructions": full["instructions"] or "",
                "ingredients": new_ingredients,
            }
            if new_recipe != recipe:
                recipe.clear()
                recipe.update(new_recipe)
                updated_recipes += 1

    STARTER_DATA_FILE.write_text(json.dumps(data, indent=2) + "\n")
    try:
        display_path = STARTER_DATA_FILE.relative_to(REPO_ROOT)
    except ValueError:
        display_path = STARTER_DATA_FILE  # e.g. under test, path is monkeypatched outside REPO_ROOT
    print(
        f"Refreshed {display_path}: "
        f"foods {updated_foods} updated / {added_foods} added / {skipped_foods} skipped (not cached); "
        f"recipes {updated_recipes} updated / {skipped_recipes} skipped (no live match)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
