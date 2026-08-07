"""
glycemic_load.py — glycemic load (GL) aggregation across a list of line items
(foods and/or recipes), used by the web backend (backend.py). Extracted after
web's two separate call sites independently recomputed this same accumulation
loop and both lacked the recipe-GL rollup via recipes.gl_g, always treating a
nested recipe/sub-recipe line item as an unconditional blocker instead of
using its precomputed GL.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/glycemic_load.py — GL aggregation"
"""
import json

import db as _db


def compute_glycemic_load(line_items: list[dict], conn) -> tuple[float, list[tuple[str, int | None, int | None]]]:
    """Compute total glycemic load across a list of line items.

    Each line item: {"kind": "food" | "recipe", "name": str, "amount": float,
                      "fdc_id": int | None, "recipe_id": int | None}
    `amount` is grams for "food" items, servings consumed for "recipe" items.

    Recipe items use the recipe's own precomputed gl_g (GL per serving, set
    via db.recipe_set_gl after analyzing that recipe) scaled by servings
    consumed; a recipe with no gl_g yet becomes a blocker.

    Returns (gl_total, blockers). gl_total accumulates every line item that
    *could* be computed, even when blockers is non-empty — callers decide
    whether a partial total is worth showing or whether any blocker should
    suppress the total entirely (existing call sites differ on this).
    blockers is a list of (label, fdc_id, recipe_id) tuples so callers can show
    each blocker's ID + source alongside its name; label already includes any
    trailing note (e.g. "(no GL — analyze it first)") for recipe blockers.
    """
    food_ids = [li["fdc_id"] for li in line_items if li["kind"] == "food" and li.get("fdc_id")]
    ann_map = _db.annotations_for_fdcids(conn, food_ids) if food_ids else {}

    blockers: list[tuple[str, int | None, int | None]] = []
    gl_total = 0.0

    for li in line_items:
        if li["kind"] == "recipe":
            recipe = _db.recipe_get(conn, li["recipe_id"]) if li.get("recipe_id") else None
            if recipe is None or recipe["gl_g"] is None:
                name = recipe["name"] if recipe else li["name"]
                blockers.append((f"{name} (no GL — analyze it first)", None, li.get("recipe_id")))
                continue
            servings = recipe["servings"] or 1
            gl_total += recipe["gl_g"] * (li["amount"] / servings)
            continue

        ann = ann_map.get(li["fdc_id"])
        if ann is None or ann["gi_estimate"] is None:
            blockers.append((li["name"], li.get("fdc_id"), None))
            continue

        cached = _db.get_cached_food(conn, li["fdc_id"])
        if not cached or not cached["nutrients_json"]:
            blockers.append((li["name"], li.get("fdc_id"), None))
            continue

        carbs_g = json.loads(cached["nutrients_json"]).get("carbs_g", 0.0) * li["amount"] / 100.0
        gl_total += ann["gi_estimate"] * carbs_g / 100.0

    return gl_total, blockers
