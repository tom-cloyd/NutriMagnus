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


# ── GL classification bands ───────────────────────────────────────────────
#
# Two different scales, and using the wrong one is not a rounding error: the
# per-serving bands applied to a whole-day total label every real day "High",
# which is how the Daily Summary read until 2026-09-27.
#
# "serving" — per food/serving/meal. Low <=10, Medium 11-19, High >=20.
#   The per-serving classification associated with the University of Sydney GI
#   tables (Atkinson et al. 2021).
# "day" — whole-day total. Low <80, Moderate 80-120, High >120.
#   A widely-repeated convention, NOT a validated clinical target, and defined
#   inconsistently even by expert groups — hence gl_band_caveat() below, which
#   callers should show alongside a day-scoped band.
# Each entry is (low_max, low_op, low_label, mid_max, mid_op, mid_label), where
# op is "le" or "lt". The two scales are published with different boundary
# wording — serving as "<=10 / 11-19 / >=20", day as "under 80 / 80-120 / over
# 120" — so each band carries its own comparison rather than one shared rule.
GL_BANDS = {
    "serving": (10.0, "le", "Low", 20.0, "lt", "Medium"),
    "day":     (80.0, "lt", "Low", 120.0, "le", "Moderate"),
}


def gl_band(total: float | None, scope: str = "serving") -> str | None:
    """Classify a GL figure as Low / Medium-or-Moderate / High for `scope`.

    scope is "serving" (a food, serving, meal or recipe portion) or "day" (a
    whole-day total). Returns None for a None total so templates can guard on
    one value. Boundaries are inclusive of the lower band: a serving GL of
    exactly 10 is Low, exactly 20 is High.
    """
    if total is None:
        return None
    low_max, low_op, low_label, mid_max, mid_op, mid_label = GL_BANDS.get(scope, GL_BANDS["serving"])
    if total <= low_max if low_op == "le" else total < low_max:
        return low_label
    if total <= mid_max if mid_op == "le" else total < mid_max:
        return mid_label
    return "High"


def gl_band_caveat(scope: str = "serving") -> str | None:
    """A one-line caveat to show beside a band, or None when none is needed.

    Only the day-scale bands get one: unlike the per-serving bands, they are a
    convention rather than a validated clinical target, and a day's GL rises
    with energy intake, so a large or active person naturally runs higher.
    """
    if scope != "day":
        return None
    return ("Day-scale bands (under 80 low, 80-120 moderate, over 120 high) are a "
            "common convention, not a validated clinical target -- and a day's GL "
            "rises with how much you eat, so a larger or more active person will "
            "naturally run higher.")


# ── Day-level GL, for trends and plots ────────────────────────────────────

def meal_line_items(conn, meal_id: int) -> list[dict]:
    """A meal's items in the shape compute_glycemic_load() expects."""
    return [
        {
            "kind":      "recipe" if item["item_type"] == "recipe" else "food",
            "name":      item["food_name"],
            "amount":    item["amount"],
            "fdc_id":    item["fdc_id"],
            "recipe_id": item["recipe_id"],
        }
        for item in _db.meal_get_items(conn, meal_id)
    ]


def day_gl_total(conn, meal_date: str) -> float | None:
    """Total GL for every meal logged on meal_date, or None if any item on
    that day blocks the calculation (no GI annotation, or a recipe with no
    computed GL yet). None means "unknown", never zero -- a day with partial
    GI coverage would otherwise read as a lower GL than it really is.

    Returns None for a date with no meals at all, which callers treat the
    same way nutrient averaging does: a day that was never logged is absent
    from the average, not a zero-intake day.
    """
    meals = _db.meal_list_by_date(conn, meal_date)
    if not meals:
        return None
    total = 0.0
    for meal in meals:
        meal_total, blockers = compute_glycemic_load(meal_line_items(conn, meal["id"]), conn)
        if blockers:
            return None
        total += meal_total
    return round(total, 1)


def day_gl_totals(conn, dates: list[str]) -> dict[str, float | None]:
    """day_gl_total() for several dates over one connection — the shape the
    GL trend and the Nutrient Plot's GL series both need. Every requested
    date is present as a key, with None where the day's GL is unknown."""
    return {d: day_gl_total(conn, d) for d in dates}


def average_day_gl(day_totals: dict[str, float | None]) -> tuple[float | None, int]:
    """Mean GL across the days that actually have a computable total, plus
    how many days that was.

    Days whose GL is unknown are skipped rather than counted as zero, and
    the returned count is what a caller should disclose beside the average:
    "GL averaged over 5 of the last 7 days" is honest in a way that a bare
    average over a partially-annotated window is not.
    """
    known = [v for v in day_totals.values() if v is not None]
    if not known:
        return None, 0
    return round(sum(known) / len(known), 1), len(known)
