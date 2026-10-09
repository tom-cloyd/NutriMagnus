"""
glycemic_load.py — glycemic load (GL) for foods, recipes, meals and days,
used by the web backend (backend.py).

GL = GI x carbohydrate grams / 100, summed over every food eaten. A recipe's GL
is worked out live from its ingredients, through any sub-recipes, rather than
read from a saved figure, so it is never stale and never missing just because
nobody "analyzed" the recipe. A food with no GI value can't be counted; instead
of hiding the whole figure, the result keeps the GL of everything that could be
counted and lists each food that couldn't, with the reason — so a page can say
"at least 14.2, incomplete" and name what is missing.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/glycemic_load.py — GL aggregation"
"""
import json

import db as _db

# A food without a GI whose carbohydrate in the amount eaten is under this
# counts as zero rather than as missing data: its GL can be at most 1 even at
# GI 100. The same idea as DCP's 1 g protein floor for foods with no amino
# acid data (recipe_dcp.py), so a pinch of spice or a splash of oil never
# makes a recipe's GL "incomplete".
NEGLIGIBLE_CARBS_G = 1.0

# Why a food's share of the GL could not be counted (gap["reason"]).
GAP_NO_GI      = "no_gi"       # no GI recorded yet
GAP_NOT_WANTED = "not_wanted"  # GI marked "don't prompt me" (or GI opted out in Settings)
GAP_NO_DATA    = "no_data"     # the food has no nutrient data at all
GAP_NO_RECIPE  = "no_recipe"   # a logged recipe that has since been deleted


def _ingredient_line_items(conn, recipe_id: int) -> list[dict]:
    return [
        {
            # A sub-recipe whose recipe was deleted keeps its line, flagged.
            "kind":      "recipe" if ing["ref_recipe_id"] or ing["ref_recipe_deleted"] else "food",
            "name":      ing["food_name"],
            "amount":    ing["amount"] or 0.0,
            "fdc_id":    None if ing["ref_recipe_id"] or ing["ref_recipe_deleted"] else ing["fdc_id"],
            "recipe_id": ing["ref_recipe_id"],
        }
        for ing in _db.recipe_get_ingredients(conn, recipe_id)
    ]


def _add_gap(gaps: list[dict], gap: dict) -> None:
    """Append `gap` unless the same food or recipe is already listed — a food
    used in two recipes of one meal is one thing to fix, not two."""
    def key(g):
        return (g["fdc_id"], g["recipe_id"]) if g["fdc_id"] or g["recipe_id"] else g["name"]
    if all(key(g) != key(gap) for g in gaps):
        gaps.append(gap)


def _food_share(nutrients: dict, grams: float, ann, gi_opt_out: bool) -> tuple[float, str | None]:
    """(GL of `grams` of a food, gap reason or None). A food with no
    carbohydrate value at all (an oil, say) counts as carbohydrate-free, the
    same as every other nutrient total treats it."""
    carbs_g = (nutrients.get("carbs_g") or 0.0) * grams / 100.0
    if ann is not None and ann["gi_estimate"] is not None:
        return ann["gi_estimate"] * carbs_g / 100.0, None
    if carbs_g < NEGLIGIBLE_CARBS_G:
        return 0.0, None
    not_wanted = gi_opt_out or (ann is not None and ann["gi_no_prompt"])
    return 0.0, GAP_NOT_WANTED if not_wanted else GAP_NO_GI


def _accumulate(line_items, conn, scale, seen, gaps, gi_opt_out) -> float:
    """GL of `line_items` x `scale`, appending a gap per item that can't be
    counted. `seen` holds the recipes already being expanded on this path, so
    a reference cycle stops instead of recursing forever."""
    food_ids = [li["fdc_id"] for li in line_items if li["kind"] == "food" and li.get("fdc_id")]
    ann_map = _db.annotations_for_fdcids(conn, food_ids) if food_ids else {}
    total = 0.0

    def gap(name, fdc_id, recipe_id, reason):
        _add_gap(gaps, {"name": name, "fdc_id": fdc_id, "recipe_id": recipe_id, "reason": reason})

    for li in line_items:
        if li["kind"] == "recipe":
            rid = li.get("recipe_id")
            recipe = _db.recipe_get(conn, rid) if rid else None
            if recipe is None:
                gap(li["name"], None, rid, GAP_NO_RECIPE)
                continue
            if rid in seen:
                continue
            servings = recipe["servings"] or 1
            total += _accumulate(_ingredient_line_items(conn, rid), conn,
                                 scale * (li["amount"] or 0.0) / servings,
                                 seen | {rid}, gaps, gi_opt_out)
            continue

        cached = _db.get_cached_food(conn, li["fdc_id"]) if li.get("fdc_id") else None
        if not cached or not cached["nutrients_json"]:
            gap(li["name"], li.get("fdc_id"), None, GAP_NO_DATA)
            continue
        share, reason = _food_share(json.loads(cached["nutrients_json"]),
                                    (li["amount"] or 0.0) * scale,
                                    ann_map.get(li["fdc_id"]), gi_opt_out)
        total += share
        if reason:
            gap(li["name"], li["fdc_id"], None, reason)
    return total


def _result(total: float, gaps: list[dict]) -> dict:
    """{"total", "complete", "gaps"}. total is the GL of everything that could
    be counted, rounded — a lower bound when gaps is non-empty — or None when
    nothing with carbohydrate could be counted at all ("at least 0" would say
    nothing). complete is True only when nothing was left out."""
    return {
        "total":    None if gaps and total <= 0 else round(total, 1),
        "complete": not gaps,
        "gaps":     gaps,
    }


def gl_for_items(line_items: list[dict], conn, *, scale: float = 1.0,
                 gi_opt_out: bool = False) -> dict:
    """GL of a list of line items, as a result dict (see _result()).

    Each line item: {"kind": "food" | "recipe", "name": str, "amount": float,
                      "fdc_id": int | None, "recipe_id": int | None}
    `amount` is grams for "food" items, servings for "recipe" items.
    gi_opt_out: the user doesn't record GI at all (Settings), so every food
    without one is reported as not wanted rather than as still to do.
    """
    gaps: list[dict] = []
    total = _accumulate(line_items, conn, scale, frozenset(), gaps, gi_opt_out)
    return _result(total, gaps)


def food_gl(name: str, fdc_id: int, nutrients: dict, grams: float, ann, *,
            gi_opt_out: bool = False) -> dict:
    """GL of `grams` of one food, from nutrients and an annotation row the
    caller already has (the food page may show a food not yet cached)."""
    share, reason = _food_share(nutrients, grams, ann, gi_opt_out)
    gaps = [{"name": name, "fdc_id": fdc_id, "recipe_id": None, "reason": reason}] if reason else []
    return _result(share, gaps)


def recipe_gl(conn, recipe_id: int, servings: float = 1.0, *, gi_opt_out: bool = False) -> dict:
    """GL of `servings` servings of a recipe."""
    recipe = _db.recipe_get(conn, recipe_id)
    name = recipe["name"] if recipe else str(recipe_id)
    return gl_for_items([{"kind": "recipe", "name": name, "amount": servings,
                          "fdc_id": None, "recipe_id": recipe_id}], conn, gi_opt_out=gi_opt_out)


def meal_gl(conn, meal_id: int, *, gi_opt_out: bool = False) -> dict:
    """GL of everything logged in one meal."""
    return gl_for_items(meal_line_items(conn, meal_id), conn, gi_opt_out=gi_opt_out)


def combine_gl(results: list[dict]) -> dict:
    """Sum several GL results (a day's meals), keeping every gap once."""
    total = sum(r["total"] for r in results if r["total"] is not None)
    gaps: list[dict] = []
    for r in results:
        for g in r["gaps"]:
            _add_gap(gaps, g)
    return _result(total, gaps)


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
    """A meal's items in the shape gl_for_items() expects."""
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
    """Total GL for every meal logged on meal_date, or None if it is
    incomplete (a food on that day had carbohydrate but no GI). None means
    "unknown", never zero -- trends and plots average across days, and a
    partial total would read as a lower GL than the day really had.

    Returns None for a date with no meals at all, which callers treat the
    same way nutrient averaging does: a day that was never logged is absent
    from the average, not a zero-intake day.
    """
    meals = _db.meal_list_by_date(conn, meal_date)
    if not meals:
        return None
    day = combine_gl([meal_gl(conn, m["id"]) for m in meals])
    return day["total"] if day["complete"] else None


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
