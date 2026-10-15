"""
glycemic_load.py — glycemic load (GL) for foods, recipes, meals and days,
used by the web backend (backend.py).

GL = GI x available carbohydrate grams / 100, summed over every food eaten
(available_carbs_100g() — fiber excluded, as GI tables measure it). A recipe's GL
is worked out live from its ingredients, through any sub-recipes, rather than
read from a saved figure, so it is never stale and never missing just because
nobody "analyzed" the recipe. A food with no GI value can't be counted; instead
of hiding the whole figure, the result keeps the GL of everything that could be
counted and lists each food that couldn't, with the reason — so a page can say
"at least 14.2, incomplete" and name what is missing.

Every result from more than one food also carries an estimated GI of the
mixture — the carbohydrate-weighted average of its foods' GIs, which is just
100 x GL / carbohydrate with a GI — with the conditions that go with it: the
share of carbohydrate it covers, a floor below which it isn't given
(GI_MIN_CARBS_G), and any recipe ingredients whose GI may not describe them
as eaten (looks_uncooked()).
Docs: README-numa-documentation.md, Architecture: "numa_app/services/glycemic_load.py — GL aggregation"
"""
import json
import re

import db as _db
from numa_app.services.food_ids import source_key
from numa_app.services.rda_status import rda_status

# A food without a GI whose carbohydrate in the amount eaten is under this
# counts as zero rather than as missing data: its GL can be at most 1 even at
# GI 100. The same idea as DCP's 1 g protein floor for foods with no amino
# acid data (recipe_dcp.py), so a pinch of spice or a splash of oil never
# makes a recipe's GL "incomplete".
NEGLIGIBLE_CARBS_G = 1.0

# Below this much available carbohydrate a meal's or recipe's GI isn't given.
# GI is measured on 25-50 g portions; at 5 g, one person's response to the
# same food varies by about 65% from test to test (Spolar et al. 2006, CV
# 65 +/- 25% at 5 g vs 31 +/- 16% at 20 g) — see user-manual.md #mixture-gi.
GI_MIN_CARBS_G = 10.0

# GI bands (Atkinson et al. 2021): Low 55 or under, Medium 56-69, High 70 or
# over. A figure within GI_NEAR_BAND of a boundary is reported as close to
# the neighbouring band: a calculated meal GI isn't precise enough for 54 and
# 57 to be told apart (Dodd et al. 2011 found it 22-50% above measured).
GI_LOW_MAX = 55
GI_MEDIUM_MAX = 69
GI_NEAR_BAND = 5

# Sources whose carbs_g is already available carbohydrate (fiber not in it):
# UK CoFID, Australian AFCD and French CIQUAL all report it that way. USDA and
# CNF report total carbohydrate by difference, which includes fiber; so do US
# food labels, which most Open Food Facts and user-drafted foods come from.
# (An EU product on OFF already excludes fiber, so subtracting it there
# understates its carbohydrate — the label doesn't say which it is.) An older
# version of a food (db.create_food_version) is treated as total: nearly all
# are USDA refreshes.
_AVAILABLE_CARB_SOURCES = {"cofid", "afcd", "ciqual"}

# A recipe ingredient whose name says it is raw, dry, uncooked or a flour may
# be eaten in a different form from the one its GI describes — cooking,
# baking and grinding change how fast starch is digested, so flour + water +
# yeast is not bread. Dried fruit ("Apricots, dried, uncooked") is eaten as
# it is, so "dried" in a name cancels the match. A heuristic: it misses a
# food whose name doesn't say (a branded "SMALL RED BEANS"), and it flags
# raw fruit that really is eaten raw — hence recipes.gi_as_eaten.
_UNCOOKED_RE = re.compile(r"\b(raw|uncooked|unprepared|dry|flour)\b", re.I)
_DRIED_RE = re.compile(r"\bdried\b", re.I)


def looks_uncooked(name: str | None) -> bool:
    """True if a food's name says it is raw, dry, uncooked or a flour (see
    _UNCOOKED_RE) — and not dried fruit."""
    return bool(name) and bool(_UNCOOKED_RE.search(name)) and not _DRIED_RE.search(name)


def available_carbs_100g(nutrients: dict, fdc_id: int | None = None) -> float:
    """Available carbohydrate per 100 g — what GI and GL are defined on.
    carbs_g as stored, for a source that already reports it that way
    (_AVAILABLE_CARB_SOURCES); otherwise carbs_g minus fiber_g, never below
    zero. A food with no fiber figure keeps its whole carbs_g."""
    carbs = nutrients.get("carbs_g") or 0.0
    if source_key(fdc_id) in _AVAILABLE_CARB_SOURCES:
        return carbs
    return max(carbs - (nutrients.get("fiber_g") or 0.0), 0.0)


def gi_band(gi: float | None) -> str | None:
    """"Low" / "Medium" / "High" for a GI figure, or None."""
    if gi is None:
        return None
    if gi <= GI_LOW_MAX:
        return "Low"
    return "Medium" if gi <= GI_MEDIUM_MAX else "High"


def gi_near_band(gi: float | None) -> str | None:
    """The neighbouring band a GI figure is within GI_NEAR_BAND of, or None."""
    if gi is None:
        return None
    for boundary, below, above in ((GI_LOW_MAX + 0.5, "Low", "Medium"),
                                   (GI_MEDIUM_MAX + 0.5, "Medium", "High")):
        if abs(gi - boundary) < GI_NEAR_BAND:
            return above if gi < boundary else below
    return None


# Why a food's share of the GL could not be counted (gap["reason"]).
GAP_NO_GI      = "no_gi"       # no GI recorded yet
GAP_NOT_WANTED = "not_wanted"  # GI marked "don't prompt me" (or GI opted out in Settings)
GAP_NO_DATA    = "no_data"     # the food has no nutrient data at all
GAP_NO_RECIPE  = "no_recipe"   # a logged recipe that has since been deleted

# The GI lookup saves a picked row's subject group into gi_source as one of
# these labels (web/templates/food_annotate.html). A value measured only in
# people with impaired glucose tolerance or diabetes may not describe someone
# without it (and vice versa) — see user-manual.md #gi-populations.
IMPAIRED_LABEL = "Impaired glucose tolerance"


def gi_measured_impaired(gi_source) -> bool:
    """True if a saved GI's source says it was measured in people with
    impaired glucose tolerance or diabetes."""
    return bool(gi_source) and IMPAIRED_LABEL in gi_source


def _ann_source(ann):
    """An annotation's gi_source, or None — callers may pass a plain dict
    without that key, or a row from before the column existed."""
    try:
        return ann["gi_source"]
    except (KeyError, IndexError):
        return None


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


def _new_acc() -> dict:
    """Running tallies behind a result's coverage and population fields."""
    return {"with_gi": 0.0, "counted": 0.0, "impaired": [], "uncooked": []}


def _add_uncooked(acc: dict, entry: dict) -> None:
    if all((u["name"], u["recipe_id"]) != (entry["name"], entry["recipe_id"]) for u in acc["uncooked"]):
        acc["uncooked"].append(entry)


def _food_share(nutrients: dict, grams: float, ann, gi_opt_out: bool,
                acc: dict | None = None, name: str | None = None,
                fdc_id: int | None = None, in_recipe: dict | None = None) -> tuple[float, str | None]:
    """(GL of `grams` of a food, gap reason or None). A food with no
    carbohydrate value at all (an oil, say) counts as carbohydrate-free, the
    same as every other nutrient total treats it.

    `acc`, when given (see _new_acc()), collects carbs with a GI and carbs
    that count, for the coverage figure (see _result()) — a negligible amount
    and a food whose GI is "not wanted" count in neither — and `name` when
    the GI counted was measured in people with impaired glucose tolerance.

    Carbohydrate here is available carbohydrate (available_carbs_100g()).
    in_recipe ({"id", "name"}) is the recipe this food is a direct ingredient
    of, when that recipe's ingredients are being checked for looks_uncooked();
    a match whose GI counts is noted in acc["uncooked"]."""
    carbs_g = available_carbs_100g(nutrients, fdc_id) * grams / 100.0
    if ann is not None and ann["gi_estimate"] is not None:
        if acc is not None:
            acc["with_gi"] += carbs_g
            acc["counted"] += carbs_g
            if (name and carbs_g >= NEGLIGIBLE_CARBS_G and gi_measured_impaired(_ann_source(ann))
                    and name not in acc["impaired"]):
                acc["impaired"].append(name)
            if in_recipe and carbs_g >= NEGLIGIBLE_CARBS_G and looks_uncooked(name):
                _add_uncooked(acc, {"name": name, "fdc_id": fdc_id, "recipe_id": in_recipe["id"],
                                    "recipe": in_recipe["name"]})
        return ann["gi_estimate"] * carbs_g / 100.0, None
    if carbs_g < NEGLIGIBLE_CARBS_G:
        return 0.0, None
    not_wanted = gi_opt_out or (ann is not None and ann["gi_no_prompt"])
    if acc is not None and not not_wanted:
        acc["counted"] += carbs_g
    return 0.0, GAP_NOT_WANTED if not_wanted else GAP_NO_GI


def _accumulate(line_items, conn, scale, seen, gaps, gi_opt_out, acc,
                in_recipe: dict | None = None) -> float:
    """GL of `line_items` x `scale`, appending a gap per item that can't be
    counted. `seen` holds the recipes already being expanded on this path, so
    a reference cycle stops instead of recursing forever. in_recipe: see
    _food_share() — set for a recipe's own ingredients unless that recipe is
    marked gi_as_eaten; each recipe's mark covers its direct ingredients only."""
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
            check = None if recipe["gi_as_eaten"] else {"id": rid, "name": recipe["name"]}
            total += _accumulate(_ingredient_line_items(conn, rid), conn,
                                 scale * (li["amount"] or 0.0) / servings,
                                 seen | {rid}, gaps, gi_opt_out, acc, check)
            continue

        cached = _db.get_cached_food(conn, li["fdc_id"]) if li.get("fdc_id") else None
        if cached is not None and cached["is_supplement"]:
            continue   # a supplement stays out of glycemic load (supplements.py)
        if not cached or not cached["nutrients_json"]:
            gap(li["name"], li.get("fdc_id"), None, GAP_NO_DATA)
            continue
        share, reason = _food_share(json.loads(cached["nutrients_json"]),
                                    (li["amount"] or 0.0) * scale,
                                    ann_map.get(li["fdc_id"]), gi_opt_out, acc, li["name"],
                                    li["fdc_id"], in_recipe)
        total += share
        if reason:
            gap(li["name"], li["fdc_id"], None, reason)
    return total


def _result(total: float, gaps: list[dict], acc: dict | None = None,
            mixture: bool = True) -> dict:
    """{"total", "complete", "gaps", "carbs_with_gi_g", "carbs_g", "coverage_pct",
    "impaired", "mixture", "gi", "gi_band", "gi_near", "gi_too_little_carb",
    "uncooked"}.
    total is the GL of everything that could be counted, rounded — a lower
    bound when gaps is non-empty — or None when nothing with carbohydrate
    could be counted at all ("at least 0" would say nothing). total_exact is
    the same figure unrounded (0.0 rather than None): anything that adds GLs
    up — a day's meals, Top Contributors' items — adds these, so rounding
    happens once, at the end, not once per part. complete is True only when
    nothing was left out.

    coverage_pct is the share of the carbohydrate that counts (see
    _food_share()) that came from foods with a GI — "GL covers 72% of this
    meal's carbohydrate" — or None when there is none to cover.

    impaired names the counted foods whose GI was measured in people with
    impaired glucose tolerance or diabetes (gi_measured_impaired()).

    gi is the estimated GI of the mixture: carbohydrate-weighted mean of the
    GIs that count, = 100 x total / carbs_with_gi_g, so when coverage is under
    100 it describes only that share. None when nothing with a GI counted, or
    when the carbohydrate here is under GI_MIN_CARBS_G (gi_too_little_carb is
    then True). mixture is False for a single food (food_gl()), whose "GI"
    is just its own. uncooked: [{"name", "recipe_id", "recipe"}], recipe
    ingredients whose GI may not describe them as eaten (looks_uncooked())."""
    acc = acc or _new_acc()
    with_gi, counted = acc["with_gi"], acc["counted"]
    too_little = counted < GI_MIN_CARBS_G
    gi = round(100.0 * total / with_gi) if with_gi > 0 and not too_little else None
    return {
        "total":    None if gaps and total <= 0 else round(total, 1),
        "total_exact": total,
        "complete": not gaps,
        "gaps":     gaps,
        "carbs_with_gi_g": round(with_gi, 1),
        "carbs_g":         round(counted, 1),
        "coverage_pct":    round(with_gi / counted * 100) if counted > 0 else None,
        "impaired":        list(acc["impaired"]),
        "mixture":            mixture,
        "gi":                 gi,
        "gi_band":            gi_band(gi),
        "gi_near":            gi_near_band(gi),
        "gi_too_little_carb": too_little and with_gi > 0,
        "uncooked":           list(acc.get("uncooked", [])),
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
    acc = _new_acc()
    total = _accumulate(line_items, conn, scale, frozenset(), gaps, gi_opt_out, acc)
    return _result(total, gaps, acc)


def gl_for_leaves(leaves: list[dict], conn, *, gi_opt_out: bool = False) -> dict:
    """GL of already-expanded leaf foods — {"food_name", "fdc_id",
    "nutrients_100g", "grams"}, the shape recipe_nutrients and what-if
    produce — as a result dict (see _result()). What-if uses this so its
    edits, applied once during expansion, reach GL with no second
    expansion path."""
    ids = list({lf["fdc_id"] for lf in leaves if lf.get("fdc_id")})
    ann_map = _db.annotations_for_fdcids(conn, ids)
    gaps: list[dict] = []
    acc = _new_acc()
    total = 0.0
    for lf in leaves:
        if lf.get("is_supplement"):
            continue   # a supplement stays out of glycemic load (supplements.py)
        share, reason = _food_share(lf["nutrients_100g"], lf["grams"],
                                    ann_map.get(lf.get("fdc_id")), gi_opt_out, acc, lf["food_name"],
                                    lf.get("fdc_id"))
        total += share
        if reason:
            _add_gap(gaps, {"name": lf["food_name"], "fdc_id": lf.get("fdc_id"),
                            "recipe_id": None, "reason": reason})
    return _result(total, gaps, acc)


def food_gl(name: str, fdc_id: int, nutrients: dict, grams: float, ann, *,
            gi_opt_out: bool = False) -> dict:
    """GL of `grams` of one food, from nutrients and an annotation row the
    caller already has (the food page may show a food not yet cached)."""
    acc = _new_acc()
    share, reason = _food_share(nutrients, grams, ann, gi_opt_out, acc, name, fdc_id)
    gaps = [{"name": name, "fdc_id": fdc_id, "recipe_id": None, "reason": reason}] if reason else []
    return _result(share, gaps, acc, mixture=False)


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
    # Unrounded parts, so a day of small loads doesn't round away meal by meal.
    total = sum(r.get("total_exact", r["total"] or 0.0) for r in results)
    gaps: list[dict] = []
    for r in results:
        for g in r["gaps"]:
            _add_gap(gaps, g)
    acc = {"with_gi": sum(r.get("carbs_with_gi_g", 0.0) for r in results),
           "counted": sum(r.get("carbs_g", 0.0) for r in results),
           "impaired": list(dict.fromkeys(n for r in results for n in r.get("impaired", []))),
           "uncooked": []}
    for r in results:
        for u in r.get("uncooked", []):
            _add_uncooked(acc, u)
    return _result(total, gaps, acc)


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


# Daily GL target suggestions (Settings -> "Help me choose"; user-manual.md
# #gl-target-choose, where each option's criteria and sources are given).
# "Moderate GL diet": an average daily GL under 80 per 2,000 kcal (Barclay,
# GI Foundation, University of Sydney, 2021) — scaled to the user's calories.
GL_MODERATE_PER_2000_KCAL = 80.0
# The widely repeated "low GL day" ceiling (unsourced convention; see GL_BANDS).
GL_CONVENTIONAL_DAY_TARGET = 80.0
# "A step down from where you are": 10-20% under the recent average; the
# suggested figure is the middle of that range. Needs enough known days.
GL_STEP_DOWN = (0.10, 0.20)
GL_STEP_DOWN_MIN_DAYS = 7


def gl_target_options(calories: float | None, recent_avg: float | None,
                      recent_days: int) -> dict:
    """The three suggested daily GL targets: {"scaled", "fixed",
    "step_down", "step_down_range", "recent_avg", "recent_days"}.
    scaled is None without a calorie target; step_down (and its range) is
    None without GL_STEP_DOWN_MIN_DAYS days of known GL to average."""
    scaled = round(GL_MODERATE_PER_2000_KCAL * calories / 2000) if calories and calories > 0 else None
    step = rng = None
    if recent_avg and recent_days >= GL_STEP_DOWN_MIN_DAYS:
        lo, hi = GL_STEP_DOWN
        rng = (round(recent_avg * (1 - hi)), round(recent_avg * (1 - lo)))
        step = round(recent_avg * (1 - (lo + hi) / 2))
    return {"scaled": scaled, "fixed": round(GL_CONVENTIONAL_DAY_TARGET), "step_down": step,
            "step_down_range": rng, "recent_avg": recent_avg, "recent_days": recent_days}


def gl_target_status(total: float | None, complete: bool, target: float | None) -> dict | None:
    """A day's GL against the profile's personal daily target (a ceiling,
    classified like a nutrient maximum: rda_status(..., "limit")).

    Returns None when there is no target or no figure. Otherwise {"target",
    "pct", "status", "over"}: status is "met" / "near" / "over", or
    "unknown" for an incomplete day still under the target — its true GL is
    higher, so "under" can't be claimed (an incomplete day already over the
    target is over for certain)."""
    if not target or target <= 0 or total is None:
        return None
    pct = total / target * 100
    status = rda_status(pct, "limit")
    if not complete and status != "over":
        status = "unknown"
    return {"target": target, "pct": round(pct), "status": status, "over": total > target}


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


def day_gl(conn, meal_date: str, *, gi_opt_out: bool = False) -> dict | None:
    """Every meal on meal_date combined, as a result dict (see _result()) —
    the partial total and its gaps, for a page that can show "at least".
    None for a date with no meals. Trends and plots use day_gl_total(),
    which treats an incomplete day as unknown instead."""
    meals = _db.meal_list_by_date(conn, meal_date)
    if not meals:
        return None
    return combine_gl([meal_gl(conn, m["id"], gi_opt_out=gi_opt_out) for m in meals])


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


# The Nutrient Plot's own looser rule. A plot whose GL line only appears on
# fully annotated days drew nothing at all for a real 30-day range (every
# day had some carb food without a GI), so the plot also draws a partial
# day once at least this share of its carbohydrate has a GI, marked as
# partial. Averages (trends, the daily GL target) keep the strict rule.
PLOT_MIN_GL_COVERAGE_PCT = 80


def day_gl_plot_values(conn, dates: list[str],
                       min_coverage_pct: int = PLOT_MIN_GL_COVERAGE_PCT
                       ) -> dict[str, tuple[float | None, bool]]:
    """{date: (gl, partial)} for the Nutrient Plot. A complete day is
    (total, False); an incomplete one whose carbohydrate with a GI is at
    least min_coverage_pct of the total is (partial total, True) -- a lower
    bound, read as "at least"; anything less, or nothing logged, is
    (None, False)."""
    out: dict[str, tuple[float | None, bool]] = {}
    for d in dates:
        meals = _db.meal_list_by_date(conn, d)
        if not meals:
            out[d] = (None, False)
            continue
        day = combine_gl([meal_gl(conn, m["id"]) for m in meals])
        if day["complete"]:
            out[d] = (day["total"], False)
        elif (day["coverage_pct"] or 0) >= min_coverage_pct:
            out[d] = (day["total"], True)
        else:
            out[d] = (None, False)
    return out


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
