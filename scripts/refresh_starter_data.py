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
    renamed. If still cached, name (re-prefixed), data_type, nutrients,
    portions and any redistributable GI value are refreshed from the live row — picking up e.g. a corrected
    portion or a re-pulled USDA value. If the fdc_id is no longer cached at
    all, the entry is left untouched.
  - Pantry: always written out empty — the pantry ships empty (owner's
    decision, 2026-09-29; see export_starter_data.py).
  - Recipes: matched by their "uid" (recipes.starter_uid here), not by
    name — a recipe survives being renamed live. Older entries carrying
    "source_recipe_id" (this database's recipes.id) instead are matched by
    that, and entries with neither once by name; either way the uid is
    stamped and written back, and source_recipe_id is dropped. If a
    recipe's id no longer exists live (deleted), the entry is left
    untouched. An ingredient whose food isn't
    yet in starter_data.json's foods list (e.g. a new ingredient added live
    since the last export) is auto-included, the same way
    export_starter_data.py does it. A sub-recipe ingredient is refreshed in
    place as [name, amount, unit, "recipe"], but only when that sub-recipe is
    already a starter recipe — pulling a brand-new one in (and ordering the
    recipes list so it precedes its user) is export_starter_data.py's job, so
    the entry is left untouched with a warning telling you to run that.

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
from numa_app.services import demo_data as _demo_data

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


def _food_dict(row, *, name: str | None = None, conn=None) -> dict:
    food = {
        "fdc_id": row["fdc_id"],
        "name": name if name is not None else row["name"],
        "data_type": row["data_type"],
        "nutrients": json.loads(row["nutrients_json"]),
        "portions": json.loads(row["portions_json"] or "[]"),
    }
    # The food's GI annotation, but only if it may be redistributed — see
    # demo_data.shippable_gi() (never a value from the Atkinson 2021 tables).
    if conn is not None:
        gi = _demo_data.shippable_gi(_db.get_food_annotation(conn, row["fdc_id"]))
        if gi:
            food["gi"] = gi
    return food


def main() -> int:
    _db.init_db()  # the same migrations the app runs (recipes.starter_uid etc.)
    data = json.loads(STARTER_DATA_FILE.read_text())
    foods: list[dict] = data["foods"]
    # The pantry always ships empty (see export_starter_data.py), so any
    # pantry list left in an older starter_data.json is dropped here.
    data["pantry"] = []
    recipes: list[dict] = data["recipes"]

    foods_by_fdc_id = {f["fdc_id"]: f for f in foods}

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
            new_food = _food_dict(row, name=_canonical_name(row["name"]), conn=conn)
            if new_food != food:
                food.clear()
                food.update(new_food)
                updated_foods += 1

        # Each starter recipe's live id in this database: by uid, else (older
        # starter data) by the source_recipe_id it was exported with, else once
        # by name. Resolved up front so sub-recipes can be matched by live id.
        all_live = _db.recipe_list(conn, include_archived=True)
        live_id_by_uid = {r["starter_uid"]: r["id"] for r in conn.execute(
            "SELECT id, starter_uid FROM recipes WHERE starter_uid IS NOT NULL").fetchall()}

        def _live_id(recipe: dict) -> int | None:
            if recipe.get("uid"):
                return live_id_by_uid.get(recipe["uid"])
            if recipe.get("source_recipe_id") is not None:
                row = _db.recipe_get(conn, recipe["source_recipe_id"])
                return row["id"] if row else None
            match = next((r for r in all_live if r["name"] == recipe["name"]), None)
            return match["id"] if match else None

        live_ids = [_live_id(r) for r in recipes]

        for recipe, source_id in zip(recipes, live_ids):
            # Rebuilt each time: a sub-recipe refreshed earlier in this loop
            # may have been renamed, and its users must pick up the new name.
            starter_name_by_live_id = {lid: r["name"] for r, lid in zip(recipes, live_ids) if lid is not None}
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
                    sub_name = starter_name_by_live_id.get(ing["ref_recipe_id"])
                    if sub_name is None:
                        print(f"WARNING: leaving recipe {recipe['name']!r} untouched — "
                              f"its sub-recipe {ing['food_name']!r} is not starter data "
                              "yet; run export_starter_data.py to add it", file=sys.stderr)
                        skip_recipe = True
                        break
                    new_ingredients.append([sub_name, ing["amount"], ing["unit"], "recipe"])
                    continue
                if ing["fdc_id"] not in foods_by_fdc_id:
                    food_row = _db.get_cached_food(conn, ing["fdc_id"])
                    new_name = _canonical_name(food_row["name"])
                    new_food = _food_dict(food_row, name=new_name, conn=conn)
                    foods.append(new_food)
                    foods_by_fdc_id[ing["fdc_id"]] = new_food
                    added_foods += 1
                    print(f"NOTE: auto-including {food_row['name']!r} as "
                          f"{new_name!r} — used as an ingredient in "
                          f"{recipe_name!r} but not yet in starter_data.json", file=sys.stderr)
                new_ingredients.append(
                    [foods_by_fdc_id[ing["fdc_id"]]["name"], ing["amount"], ing["unit"], "food"]
                )

            if skip_recipe:
                continue

            new_recipe = {
                "uid": _demo_data.ensure_recipe_uid(conn, full["id"]),
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
