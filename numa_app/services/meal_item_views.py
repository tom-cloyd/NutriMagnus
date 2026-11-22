"""
meal_item_views.py — the meal page's three ways of listing one meal's items.

- "logged": the items as entered (a recipe logged whole is one row; a recipe
  logged as its separate ingredients is several food rows, each "part of" it).
  That list is built by web/backend.py; this module leaves it alone.
- "foods": every food eaten, recipes broken down to their foods (sub-recipes
  too), the same food from several places combined into one row.
- "whole": foods and recipes, each recipe kept whole — ingredients logged
  separately are gathered back under their recipe.

Reads only; the remove buttons built on "item_ids" post to the meal's
/remove-items route. Docs: README-numa-documentation.md, Architecture: "numa_app/services/meal_item_views.py"; user-manual.md #meal-detail
"""

import db as _db
from numa_app.services.recipe_nutrients import expand_recipe_ingredients

VIEWS = ("logged", "foods", "whole")


def foods_view(items: list[dict], conn) -> list[dict]:
    """[{"food_name", "fdc_id", "grams", "is_supplement", "sources",
    "item_ids", "whole_recipes"}] in the order first reached. `items` is the meal page's logged list (entry order).
    A supplement's "grams" is its internal 100 g per unit (supplements.py).
    "sources" names where the food came from: a recipe's name for each recipe
    it is in, or "" when it was logged on its own. Inside a recipe, a food
    with no nutrient data isn't counted (expand_recipe_ingredients() skips it).
    "item_ids" are the logged items holding the food itself (on its own, or
    as one of a recipe's separately logged ingredients), the ones a remove
    button can take out, and "item_grams" their total; "whole_recipes" names the recipes logged whole that
    contain it, which only a change to the recipe (or removing it) affects."""
    rows: dict[object, dict] = {}

    def _add(name, fdc_id, grams, supplement, source, item_id=None):
        key = fdc_id or (name or "").lower()
        row = rows.get(key)
        if row is None:
            row = rows[key] = {"food_name": name, "fdc_id": fdc_id, "grams": 0.0,
                               "is_supplement": supplement, "sources": [],
                               "item_ids": [], "item_grams": 0.0, "whole_recipes": []}
        row["grams"] += grams
        if source not in row["sources"]:
            row["sources"].append(source)
        if item_id is not None:
            row["item_ids"].append(item_id)
            row["item_grams"] += grams
        elif source not in row["whole_recipes"]:
            row["whole_recipes"].append(source)

    for it in items:
        if it.get("recipe_id"):
            if it.get("recipe_deleted"):
                continue
            recipe = _db.recipe_get(conn, it["recipe_id"])
            servings = float(recipe["servings"] or 1) if recipe else 1.0
            factor = float(it["amount"] or 0) / servings
            for leaf in expand_recipe_ingredients(it["recipe_id"], conn, portion_factor=factor):
                _add(leaf["food_name"], leaf.get("fdc_id"), leaf["grams"],
                     bool(leaf.get("is_supplement")), it["food_name"])
        elif it.get("fdc_id"):
            source = it["from_recipe"]["name"] if it.get("from_recipe") else ""
            _add(it["food_name"], it["fdc_id"], float(it["amount"] or 0),
                 bool(it.get("supp_count")), source, item_id=it["id"])
    return list(rows.values())


def whole_view(items: list[dict]) -> list[dict]:
    """The logged list with each recipe's separately logged ingredients
    gathered into one row: {"food_name", "recipe_id", "grams", "parts",
    "item_ids", "added_time", "gathered": True}, where "parts" is how many
    logged items it stands for and "item_ids" their ids. A gathered row sits where its first ingredient was. Every
    other item is passed through unchanged."""
    out: list[dict] = []
    gathered: dict[int, dict] = {}
    for it in items:
        src = it.get("from_recipe")
        if not src:
            out.append(it)
            continue
        row = gathered.get(src["id"])
        if row is None:
            row = gathered[src["id"]] = {"food_name": src["name"], "recipe_id": src["id"],
                                         "fdc_id": None, "grams": 0.0, "parts": 0,
                                         "item_ids": [],
                                         "added_time": it.get("added_time") or "",
                                         "gathered": True}
            out.append(row)
        row["grams"] += float(it["amount"] or 0)
        row["parts"] += 1
        row["item_ids"].append(it["id"])
    return out


def sort_rows(rows: list[dict], item_sort: str) -> list[dict]:
    """Alphabetical by name, or as given (entry / first-reached order)."""
    if item_sort == "entry":
        return rows
    return sorted(rows, key=lambda r: (r.get("food_name") or "").lower())
