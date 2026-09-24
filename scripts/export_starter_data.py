#!/usr/bin/env python3
"""
export_starter_data.py — regenerate numa_app/services/starter_data.json from
whatever foods/pantry/recipes in the real database are marked as starter
content by a leading "*" in their name.

This is how starter content is curated: rename or create a food/pantry entry/
recipe in the app itself with a name starting with "*", then run this script
before cutting a release. numa_app/services/demo_data.py reads the resulting
JSON — it has no starter data of its own baked in. The leading "*" doesn't
need a following space to count as starred ("*Foo" and "* Foo" both match) —
whatever you typed, the exported name is always normalized to the canonical
"* " (asterisk + space) form.

A starred recipe's ingredients do NOT also need to be renamed by hand: any
ingredient food that isn't already starred is auto-included in the exported
foods list, keyed off its fdc_id (which recipe_ingredients rows carry
regardless of the food's own name), and given the "* " prefix in the
exported JSON only — the real DB row is never renamed. This is deliberate,
not just a convenience — an ingredient food with real-world problems
(missing amino acid data, an odd portion, whatever) is auto-included warts
and all, since that's useful raw material for future workflow examples or
tutorials on spotting and fixing exactly those problems. Every food, pantry
item, and recipe in starter_data.json ends up "* "-prefixed as an invariant
numa_app.services.demo_data relies on (see its is-starter-content naming
convention).

A sub-recipe used as an ingredient is exported the same way: the referenced
recipe is exported too (auto-included, with a NOTE, if it isn't itself
starred), and the exported recipes list is ordered so a sub-recipe always
appears BEFORE any recipe that uses it — demo_data.load_demo_data() relies
on that order to have the sub-recipe's new id in hand when it links the
parent. Each ingredient entry is [name, amount, unit, kind] where kind is
"food" or "recipe". A recipe is skipped, with a warning, only if a sub-recipe
it needs can't be exported at all (its recipe row is gone, or the references
form a cycle).

Each exported recipe carries a "source_recipe_id" field — the live recipes.id
it was pulled from. demo_data.py ignores it (recipes are recreated fresh on
load, getting new ids), but scripts/refresh_starter_data.py uses it to
re-locate the same recipe later even if its name has since changed.

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


def _is_starred(name: str) -> bool:
    return name.startswith("*")


def _canonical_name(name: str) -> str:
    """Normalize any starred name ("*Foo", "* Foo", "*  Foo", ...) to the
    canonical "* Foo" form every exported name must use."""
    return _PREFIX + name[1:].lstrip()


def _food_dict(row, *, name: str | None = None) -> dict:
    return {
        "fdc_id": row["fdc_id"],
        "name": name if name is not None else row["name"],
        "data_type": row["data_type"],
        "nutrients": json.loads(row["nutrients_json"]),
        "portions": json.loads(row["portions_json"] or "[]"),
    }


def main() -> int:
    with _db.get_db() as conn:
        food_rows = conn.execute(
            "SELECT fdc_id, name, data_type, nutrients_json, portions_json "
            "FROM foods WHERE name LIKE '*%' AND archived = 0"
        ).fetchall()
        # Keyed by fdc_id (not name) since auto-included ingredient foods
        # below are looked up by fdc_id, and that's also the identity
        # load_demo_data() ultimately writes into the foods table.
        foods_by_fdc_id = {
            row["fdc_id"]: _food_dict(row, name=_canonical_name(row["name"]))
            for row in food_rows
        }
        starred_food_names = {f["name"] for f in foods_by_fdc_id.values()}

        pantry_rows = _db.pantry_list(conn)
        pantry = [
            _canonical_name(row["food_name"]) for row in pantry_rows
            if _is_starred(row["food_name"]) and _canonical_name(row["food_name"]) in starred_food_names
        ]

        # Insertion-ordered: a recipe is added only after every sub-recipe it
        # uses, which is exactly the order load_demo_data() needs.
        recipes_by_id: dict[int, dict] = {}
        exported_recipe_names: dict[int, str] = {}
        being_exported: set[int] = set()

        def _export_recipe(recipe_id: int, *, needed_by: str | None = None) -> str | None:
            """Export one recipe plus every sub-recipe it depends on.

            Returns its exported name, or None if it can't be exported (a
            missing recipe row, a reference cycle, or a sub-recipe that hit
            either of those) — the caller then skips it too."""
            if recipe_id in exported_recipe_names:
                return exported_recipe_names[recipe_id]
            if recipe_id in being_exported:
                print(f"WARNING: skipping recipe {needed_by!r} — its sub-recipe "
                      "references form a cycle", file=sys.stderr)
                return None
            full = _db.recipe_get(conn, recipe_id)
            if full is None:
                print(f"WARNING: skipping recipe {needed_by!r} — the sub-recipe it "
                      f"uses (id {recipe_id}) no longer exists", file=sys.stderr)
                return None
            recipe_name = _canonical_name(full["name"]) if _is_starred(full["name"]) \
                else _PREFIX + full["name"]
            if needed_by is not None and not _is_starred(full["name"]):
                print(f"NOTE: auto-including recipe {full['name']!r} as "
                      f"{recipe_name!r} — used as a sub-recipe in "
                      f"{needed_by!r} but not itself starred", file=sys.stderr)

            being_exported.add(recipe_id)
            try:
                ingredients = []
                for ing in _db.recipe_get_ingredients(conn, recipe_id):
                    if ing["ref_recipe_id"]:
                        sub_name = _export_recipe(ing["ref_recipe_id"], needed_by=recipe_name)
                        if sub_name is None:
                            return None
                        ingredients.append([sub_name, ing["amount"], ing["unit"], "recipe"])
                        continue
                    if ing["ref_recipe_deleted"]:
                        # db.recipe_delete() nulls ref_recipe_id and sets this
                        # flag, leaving a row with fdc_id 0 and no food behind
                        # it — following it into the food branch below would
                        # look up a food that cannot exist.
                        print(f"WARNING: skipping recipe {recipe_name!r} — its sub-recipe "
                              f"{ing['food_name']!r} has been deleted", file=sys.stderr)
                        return None
                    if ing["fdc_id"] not in foods_by_fdc_id:
                        food_row = _db.get_cached_food(conn, ing["fdc_id"])
                        export_name = _canonical_name(food_row["name"]) if _is_starred(food_row["name"]) \
                            else _PREFIX + food_row["name"]
                        foods_by_fdc_id[ing["fdc_id"]] = _food_dict(food_row, name=export_name)
                        starred_food_names.add(export_name)
                        print(f"NOTE: auto-including {food_row['name']!r} as "
                              f"{export_name!r} — used as an ingredient in "
                              f"{recipe_name!r} but not itself starred", file=sys.stderr)
                    # Use the exported (possibly now-prefixed) name so it matches
                    # the foods list — demo_data.load_demo_data() resolves each
                    # ingredient's fdc_id via by_name[food_name] on that list.
                    ingredients.append([foods_by_fdc_id[ing["fdc_id"]]["name"], ing["amount"],
                                        ing["unit"], "food"])
            finally:
                being_exported.discard(recipe_id)

            exported_recipe_names[recipe_id] = recipe_name
            recipes_by_id[recipe_id] = {
                "source_recipe_id": full["id"],
                "name": recipe_name,
                "description": full["description"] or "",
                "servings": full["servings"],
                "instructions": full["instructions"] or "",
                "ingredients": ingredients,
            }
            return recipe_name

        for summary in _db.recipe_list(conn):
            if _is_starred(summary["name"]):
                _export_recipe(summary["id"])
        recipes = list(recipes_by_id.values())

    foods = list(foods_by_fdc_id.values())

    OUTPUT.write_text(json.dumps(
        {"foods": foods, "pantry": pantry, "recipes": recipes}, indent=2,
    ) + "\n")
    try:
        display_path = OUTPUT.relative_to(REPO_ROOT)
    except ValueError:
        display_path = OUTPUT  # e.g. under test, OUTPUT is monkeypatched outside REPO_ROOT
    print(f"Wrote {display_path}: "
          f"{len(foods)} foods, {len(pantry)} pantry, {len(recipes)} recipes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
