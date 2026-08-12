"""
recipe_csv.py — Recipe CSV export/import: a companion pair of CSV files
(recipes.csv + foods.csv) so a recipe travels with everything it needs to
recreate itself on another install — every sub-recipe it references, at any
depth, plus every distinct food ingredient's full nutrient/portion data —
rather than bare names that might not resolve on the receiving end.

foods.csv reuses csv_export.foods_to_csv() / csv_import.parse_foods_csv() /
csv_import.resolve_or_import_foods() verbatim; this module adds the
recipe/ingredient layer plus the DB-aware glue (dependency-closure
collection on export, two-pass dedup-and-create on import) that plain food
CSV import doesn't need.
Docs: README-numa-documentation.md, Project Structure
"""
from __future__ import annotations

import csv
import io

from .csv_export import foods_to_csv
from .csv_import import resolve_or_import_foods

RECIPE_COLUMNS = [
    "recipe_name", "recipe_description", "servings", "total_weight", "total_weight_unit",
    "instructions", "ingredient_food_name", "ingredient_amount", "ingredient_unit",
    "ingredient_notes", "ingredient_is_subrecipe",
]


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def recipes_to_csv(recipes: list[dict]) -> str:
    """recipes: [{"row": recipe row, "ingredients": [ingredient row, ...]}, ...].

    One row per ingredient; a recipe with no ingredients gets a single row
    with blank ingredient_* fields. Sub-recipes appear as ordinary entries
    in `recipes` (matched by name on import) — this function doesn't walk
    dependencies itself; that's collect_recipe_bundle()'s job.
    """
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=RECIPE_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for entry in recipes:
        row = entry["row"]
        base = {
            "recipe_name":        row["name"],
            "recipe_description": row["description"] or "",
            "servings":           row["servings"],
            "total_weight":       row["total_weight"] if row["total_weight"] is not None else "",
            "total_weight_unit":  row["total_weight_unit"] or "",
            "instructions":       row["instructions"] or "",
        }
        ingredients = entry["ingredients"]
        if not ingredients:
            writer.writerow(base)
            continue
        for ing in ingredients:
            writer.writerow({
                **base,
                "ingredient_food_name":    ing["food_name"],
                "ingredient_amount":       ing["amount"],
                "ingredient_unit":         ing["unit"] or "",
                "ingredient_notes":        ing["notes"] or "",
                "ingredient_is_subrecipe": "1" if ing["ref_recipe_id"] else "",
            })
    return buf.getvalue()


def collect_recipe_bundle(conn, recipe_ids: list[int]) -> tuple[list[dict], list]:
    """Return (recipes, food_rows): recipes covers every requested recipe
    plus every sub-recipe it transitively references, each included once;
    food_rows is the deduped set of every distinct food ingredient
    referenced anywhere in that closure (raw `foods` table rows, suitable
    for csv_export.foods_to_csv())."""
    import db as _db
    recipes: dict[int, dict] = {}
    food_ids: set[int] = set()
    queue = list(recipe_ids)
    while queue:
        rid = queue.pop(0)
        if rid in recipes:
            continue
        row = _db.recipe_get(conn, rid)
        if not row:
            continue
        ingredients = _db.recipe_get_ingredients(conn, rid)
        recipes[rid] = {"row": row, "ingredients": ingredients}
        for ing in ingredients:
            if ing["ref_recipe_id"]:
                queue.append(ing["ref_recipe_id"])
            elif ing["fdc_id"]:
                food_ids.add(ing["fdc_id"])
    food_rows = []
    for fid in sorted(food_ids):
        f = _db.get_cached_food(conn, fid)
        if f:
            food_rows.append(f)
    return list(recipes.values()), food_rows


def render_recipe_export(conn, recipe_ids: list[int]) -> tuple[str, str]:
    """Return (recipes_csv_text, foods_csv_text) for the given recipe(s)
    plus every sub-recipe and food ingredient they depend on."""
    recipes, food_rows = collect_recipe_bundle(conn, recipe_ids)
    return recipes_to_csv(recipes), foods_to_csv(food_rows)


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

def parse_recipes_csv(content: str) -> tuple[list[dict], list[str]]:
    """Parse recipes.csv text into (recipes, warnings).

    Each recipe dict: {name, description, servings, total_weight,
    total_weight_unit, instructions, ingredients: [{food_name, amount, unit,
    notes, is_subrecipe}, ...]}. Rows are grouped by recipe_name in order of
    first appearance; a recipe's metadata is taken from its first row.
    """
    warnings: list[str] = []
    reader = csv.DictReader(io.StringIO(content))
    fieldnames = reader.fieldnames or []

    if "recipe_name" not in fieldnames:
        warnings.append("CSV has no 'recipe_name' column — nothing to import.")
        return [], warnings

    order: list[str] = []
    by_name: dict[str, dict] = {}
    for i, row in enumerate(reader, 1):
        name = (row.get("recipe_name") or "").strip()
        if not name:
            warnings.append(f"Row {i}: missing 'recipe_name' — skipped.")
            continue

        if name not in by_name:
            servings_raw = (row.get("servings") or "").strip()
            servings = 1.0
            if servings_raw:
                try:
                    servings = float(servings_raw)
                except ValueError:
                    warnings.append(
                        f"Row {i} ({name!r}): 'servings' value {servings_raw!r} is not a number — defaulting to 1."
                    )
            total_weight_raw = (row.get("total_weight") or "").strip()
            total_weight = None
            if total_weight_raw:
                try:
                    total_weight = float(total_weight_raw)
                except ValueError:
                    warnings.append(
                        f"Row {i} ({name!r}): 'total_weight' value {total_weight_raw!r} is not a number — ignored."
                    )
            by_name[name] = {
                "name":              name,
                "description":       (row.get("recipe_description") or "").strip(),
                "servings":          servings,
                "total_weight":      total_weight,
                "total_weight_unit": (row.get("total_weight_unit") or "").strip() or None,
                "instructions":      (row.get("instructions") or "").strip(),
                "ingredients":       [],
            }
            order.append(name)

        food_name = (row.get("ingredient_food_name") or "").strip()
        if not food_name:
            continue  # metadata-only row — a recipe with no ingredients
        amount_raw = (row.get("ingredient_amount") or "").strip()
        try:
            amount = float(amount_raw) if amount_raw else 0.0
        except ValueError:
            warnings.append(
                f"Row {i} ({name!r}): ingredient {food_name!r} amount {amount_raw!r} is not a number — skipped."
            )
            continue
        by_name[name]["ingredients"].append({
            "food_name":    food_name,
            "amount":       amount,
            "unit":         (row.get("ingredient_unit") or "").strip(),
            "notes":        (row.get("ingredient_notes") or "").strip() or None,
            "is_subrecipe": (row.get("ingredient_is_subrecipe") or "").strip() not in ("", "0"),
        })

    return [by_name[n] for n in order], warnings


def import_recipe_bundle(conn, recipes: list[dict], food_rows_valid: list[dict]) -> dict:
    """Two-pass import: (1) resolve or create every food (deduped by name
    against the destination cache) and every recipe shell (deduped by name
    against existing recipes), (2) add ingredients now that every food and
    recipe referenced anywhere in the bundle is guaranteed to exist —
    regardless of what order they appeared in the file. A recipe whose name
    already matches an existing one is treated as already present and left
    untouched (its ingredients are not re-added), the same rule food import
    uses to avoid duplicating something the user already has.

    Returns {"recipes_created", "recipes_reused", "foods_created", "warnings"}.
    """
    import db as _db
    from . import recipe_dcp as _recipe_dcp

    before_food_ids = {r["fdc_id"] for r in _db.list_cached_foods(conn, include_archived=True)}
    food_name_to_id = resolve_or_import_foods(conn, food_rows_valid)
    after_food_ids = {r["fdc_id"] for r in _db.list_cached_foods(conn, include_archived=True)}
    foods_created = len(after_food_ids - before_food_ids)

    existing_recipes = {r["name"].strip().lower(): r["id"] for r in _db.recipe_list(conn, include_archived=True)}
    name_to_id: dict[str, int] = {}
    created_keys: set[str] = set()
    for r in recipes:
        key = r["name"].strip().lower()
        if key in existing_recipes:
            name_to_id[key] = existing_recipes[key]
            continue
        rid = _db.recipe_create(
            conn, r["name"], r["description"], r["servings"], r["instructions"],
            total_weight=r["total_weight"], total_weight_unit=r["total_weight_unit"],
        )
        name_to_id[key] = rid
        existing_recipes[key] = rid
        created_keys.add(key)

    warnings: list[str] = []
    for r in recipes:
        key = r["name"].strip().lower()
        if key not in created_keys:
            continue  # already existed at the destination — left as-is
        rid = name_to_id[key]
        for ing in r["ingredients"]:
            if ing["is_subrecipe"]:
                ref_id = name_to_id.get(ing["food_name"].strip().lower())
                if ref_id is None or ref_id == rid:
                    warnings.append(
                        f"{r['name']!r}: sub-recipe ingredient {ing['food_name']!r} could not be resolved — skipped."
                    )
                    continue
                _db.recipe_add_ingredient(conn, rid, 0, ing["food_name"], ing["amount"],
                                          ing["unit"], ing["notes"], ref_recipe_id=ref_id)
            else:
                fdc_id = food_name_to_id.get(ing["food_name"].strip().lower())
                if fdc_id is None:
                    warnings.append(
                        f"{r['name']!r}: ingredient {ing['food_name']!r} could not be resolved — skipped."
                    )
                    continue
                _db.recipe_add_ingredient(conn, rid, fdc_id, ing["food_name"], ing["amount"],
                                          ing["unit"], ing["notes"])
        _db.recipe_auto_weight(conn, rid)
        _recipe_dcp.recompute_recipe_dcp(rid, conn)

    return {
        "recipes_created": len(created_keys),
        "recipes_reused":  len(recipes) - len(created_keys),
        "foods_created":   foods_created,
        "warnings":        warnings,
    }
