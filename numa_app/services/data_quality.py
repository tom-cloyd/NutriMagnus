"""
data_quality.py — every data-quality check NuMa runs, in one place.

The Database check page (Foods → 9), the Home page reminder, the note shown
right after a food is added to a meal or recipe, and a food's own page all
read from here, so they can't drift apart. The checks themselves:

- food_issues(): one food's problems — no calories, calories estimated from
  protein/carbs/fat, calories that don't fit them (energy_check.py), and
  impossible values (impossible_values()) — each with the one-click fixes
  that can be offered for it (a likely cause such as kilojoules entered as
  calories, where the figures show one); apply_fix() applies one, logged
  with its reason (db.correct_food_values).
- stale_amounts(): recipe ingredients and logged meal foods entered as a
  volume or portion ("1/3 c", "2 T", "p1") whose stored grams no longer match
  what that entry works out to now — the food's portions changed, or NuMa's
  conversion did, after the amount was entered. Grams are fixed when an
  amount is entered, so nothing else ever notices. With include_bracketed,
  also volume amounts carrying a gram figure in brackets ("1/3 c (42 gr)"),
  which older versions wrote themselves (offered unticked, since the figure
  may equally be one the user weighed). "Keep as entered" (keep_as_entered())
  rewrites an amount in the typed-own-weight form ("2309.2 g (8 c)"), which
  is never listed; a leftover db.amount_keeps row is left out while its grams
  stay as kept, until convert_keeps() rewrites it the same way.
- generic_density_in_use(): foods whose volume amounts (in recipes or meals)
  were converted with the generic density table, because the food has no
  cup/spoon portion of its own — measuring one makes those amounts exact.
  An improvement, not an error: no reminder keys.
- old_usda_copies(): USDA foods not refreshed in over a year (USDA revises
  records; a Refresh shows what changed).
- missing_aa_in_use() / missing_portions_in_use(): foods you actually use
  (recipe, meal or pantry) with no amino-acid figures / no portion weights,
  most-used first. Only used foods: an unused one affects no result, and the
  full lists run to dozens. Improvements, not errors — no reminder keys.
- missing_gi_in_use(): foods you use with carbohydrate (5 g/100 g or more)
  but no GI, most-used first — they leave glycemic load incomplete and can't
  be offered as lower-GL swaps. "Not needed" here is the GI "don't prompt me"
  flag (food_annotations.gi_no_prompt), the one glycemic load already honours.
- gi_not_needed(): every cached food with that flag set, used or not, any
  carbohydrate, GI recorded or not — the full list behind Foods → 9's "Also
  list foods for which the GI is marked 'not needed'" button, so a choice
  made on an Annotate page can be found and undone later.
- foods_days_eaten(): every food eaten in a chosen span of days (on its own
  or inside a logged recipe), with how many days, for Foods → 9's "Foods:
  days eaten" — the page then picks out those that left a day's glycemic
  load incomplete (ranked by those days) and those with no carbohydrate value.
- wet_dry_in_use(): foods named dry ("okara flour") — by their own name or
  the name typed for them in a recipe or meal — whose data says mostly water,
  i.e. the wet record picked for the dry food (water.wet_dry_conflict()).
- duplicate_groups(): foods with the same name once case, a "* " starter
  prefix, "Copy of " and "(FDC n)" are ignored; run on request only.
  merge_review(): what keeping one of them would lose — values and
  portions the others have that it lacks or has differently — so the user
  can copy them over (their own edits first) before the merge.
- scan(): the whole database — the checks above plus the existing
  integrity check (db.check_db_integrity) and nutrient-group completeness
  (data_completeness.py) — as stable issue keys, so the reminder can tell
  new problems from ones the user has already seen.

Docs: README-numa-documentation.md, Architecture: "numa_app/services/data_quality.py — data-quality checks"
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone

import db as _db
import usda as _usda
from numa_app.services import data_completeness as _completeness
from numa_app.services import energy_check as _energy
from numa_app.services.portions import _parse_portion_input, generic_density_kind

# Per 100 g, protein + carbs + fat can't exceed 100 g; a little slack for
# rounding in published figures (pure oils list 100 g fat, sugar 100 g carbs).
_MACRO_SUM_LIMIT_G = 102.0
_SINGLE_LIMIT_G = 100.5
_GRAM_KEYS = ("protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
              "saturated_fat_g", "mono_fat_g", "poly_fat_g")
_LABELS = {"protein_g": "protein", "carbs_g": "carbohydrate", "fat_g": "fat",
           "fiber_g": "fiber", "sugar_g": "sugars", "saturated_fat_g": "saturated fat",
           "mono_fat_g": "monounsaturated fat", "poly_fat_g": "polyunsaturated fat"}

OLD_COPY_DAYS = 365
# food_data_ignores key for "these calories are right": stops the mismatch
# check for one food whose calories come from something the 4/4/9 estimate
# can't see (alcohol in vanilla extract, a source's own odd but real figure).
CALORIES_OK_KEY = "calories_ok"
# A stored amount within this of what its entry works out to now is fine.
_STALE_FRACTION = 0.02
_STALE_MIN_G = 0.5


def _fix(fix_id: str, label: str, changes: dict, reason: str, *, hint: str = "",
         estimated: tuple = ()) -> dict:
    """One offered correction: `changes` {key: new value, or None to remove},
    the `reason` logged with it (db.correct_food_values), and an optional
    `hint` saying what probably went wrong."""
    return {"id": fix_id, "label": label, "changes": changes, "reason": reason,
            "hint": hint, "estimated": list(estimated)}


def _impossible_items(nutrients: dict) -> list[tuple[str, list[dict]]]:
    """impossible_values(), each with the fixes that can be offered for it."""
    out = []
    neg = sorted(k for k, v in nutrients.items() if isinstance(v, (int, float)) and v < 0)
    if neg:
        out.append(("negative value" + ("s" if len(neg) > 1 else "") + " (" + ", ".join(neg) + ")",
                    [_fix("remove_negative", "Remove the negative value" + ("s" if len(neg) > 1 else ""),
                          {k: None for k in neg},
                          "a negative amount can't be right, so the value was removed")]))
    for k in _GRAM_KEYS:
        v = nutrients.get(k)
        if v is not None and v > _SINGLE_LIMIT_G:
            fixes = []
            if v / 1000 <= _SINGLE_LIMIT_G:
                fixes.append(_fix(f"mg_to_g:{k}", f"Divide by 1,000 ({v / 1000:g} g)",
                                  {k: round(v / 1000, 4)},
                                  f"{v:g} g of {_LABELS[k]} per 100 g can't be right; probably milligrams "
                                  "entered as grams, so divided by 1,000",
                                  hint="probably milligrams entered as grams"))
            out.append((f"{v:g} g of {_LABELS[k]} per 100 g", fixes))
    p, c, f = (nutrients.get(k) for k in ("protein_g", "carbs_g", "fat_g"))
    if None not in (p, c, f) and p + c + f > _MACRO_SUM_LIMIT_G and not any(
            nutrients.get(k, 0) > _SINGLE_LIMIT_G for k in ("protein_g", "carbs_g", "fat_g")):
        out.append((f"protein, carbohydrate and fat add up to {p + c + f:.0f} g per 100 g", []))
    sugar = nutrients.get("sugar_g")
    if sugar is not None and c is not None and sugar > c * 1.05 + 0.5:
        out.append((f"more sugars ({sugar:g} g) than carbohydrate ({c:g} g)",
                    [_fix("sugar_to_carbs", f"Set sugars to {c:g} g, the carbohydrate figure",
                          {"sugar_g": c},
                          f"sugars ({sugar:g} g) were more than carbohydrate ({c:g} g), which includes them; "
                          "set equal to carbohydrate")]))
    parts = [nutrients.get(k) for k in ("saturated_fat_g", "mono_fat_g", "poly_fat_g")]
    if f is not None and any(x is not None for x in parts):
        total = sum(x or 0 for x in parts)
        if total > f * 1.1 + 0.5:
            out.append((f"the three fat types ({total:.1f} g) add up to more than total fat ({f:g} g)",
                        [_fix("fat_from_parts", f"Set total fat to {total:.1f} g, the sum of its types",
                              {"fat_g": round(total, 2)},
                              f"the three fat types ({total:.1f} g) added up to more than total fat "
                              f"({f:g} g); total fat set to their sum")]))
    return out


def impossible_values(nutrients: dict) -> list[str]:
    """Plain-language descriptions of values that can't be right per 100 g:
    negatives, any one macronutrient over 100 g, protein + carbs + fat over
    100 g, sugars more than carbohydrate, or the three fat types more than
    total fat (each is a part of the other)."""
    return [text for text, _fixes in _impossible_items(nutrients)]


def _calorie_fixes(nutrients: dict, mm: dict, serving_g: float | None) -> list[dict]:
    """Fixes for calories that don't fit the macros: a likely cause first
    when the figure fits one (kilojoules entered as calories; a per-serving
    figure entered as per 100 g), then the 4/4/9 estimate."""
    stored, expected = mm["stored"], mm["expected"]
    fixes = []

    def fits(cal):
        return _energy.calorie_mismatch({**nutrients, "calories": cal}) is None

    if stored > 0 and fits(stored / 4.184):
        kcal = round(stored / 4.184, 1)
        fixes.append(_fix("kj_to_kcal", f"Convert from kilojoules: {kcal:g} kcal",
                          {"calories": kcal},
                          f"calories ({stored:g}) were about 4.2 times what protein, carbs and fat imply; "
                          "kilojoules entered as calories, so divided by 4.184",
                          hint="looks like kilojoules entered as calories"))
    elif serving_g and abs(serving_g - 100) > 5 and stored > 0 and fits(stored * 100 / serving_g):
        per100 = round(stored * 100 / serving_g, 1)
        fixes.append(_fix("per_serving", f"Convert to per 100 g: {per100:g} kcal",
                          {"calories": per100},
                          f"calories ({stored:g}) matched one {serving_g:g} g serving, not 100 g; "
                          "converted to per 100 g",
                          hint=f"looks like the calories for one {serving_g:g} g serving"))
    if expected > 0:
        fixes.append(_fix("use_estimate", f"Use the estimate: {expected:.0f} kcal",
                          {"calories": round(expected, 1)},
                          f"calories ({stored:g}) didn't fit protein, carbs and fat; replaced with "
                          "the 4/4/9 estimate", estimated=("calories",)))
    return fixes


def food_issues(nutrients: dict, *, estimated: set[str] = frozenset(),
                ignored: set[str] = frozenset(), serving_g: float | None = None) -> list[dict]:
    """One food's data problems as [{"kind", "severity", "text", "fixes"}],
    worst first. kind: impossible | calories_missing | calories_mismatch |
    calories_estimated. severity "problem" or "note" (an estimate is
    information, not something wrong). Calorie checks are skipped for a food
    whose macronutrients the user marked "not needed"; the mismatch check
    alone is skipped for one whose calories they confirmed (CALORIES_OK_KEY).

    "fixes": the one-click corrections Foods → 9 offers for the problem (see
    _fix(); applied by apply_fix()), most likely first; [] when NuMa can't
    tell which value is wrong. `serving_g`, the food's serving in grams,
    lets a per-serving calorie figure be recognised."""
    out = [{"kind": "impossible", "severity": "problem", "text": t, "fixes": fixes}
           for t, fixes in _impossible_items(nutrients)]
    if "macros" not in ignored:
        if _energy.calories_missing(nutrients):
            est = _energy.atwater_estimate(nutrients)
            fixes = [_fix("estimate_calories", f"Fill in calories from protein, carbs and fat: {est:.0f} kcal",
                          {"calories": round(est, 1)},
                          "no calorie value; estimated from protein, carbs and fat (4/4/9)",
                          estimated=("calories",))] if est and est > 0 else []
            out.append({"kind": "calories_missing", "severity": "problem",
                        "text": "no calorie value, so it adds nothing to any calorie total",
                        "fixes": fixes})
        elif "calories" in estimated:
            out.append({"kind": "calories_estimated", "severity": "note",
                        "text": "calories estimated from its protein, carbs and fat (its source gave none)",
                        "fixes": []})
        elif CALORIES_OK_KEY not in ignored:
            mm = _energy.calorie_mismatch(nutrients)
            if mm:
                out.append({"kind": "calories_mismatch", "severity": "problem",
                            "text": (f"its calories ({mm['stored']:.0f} kcal per 100 g) are far from what its "
                                     f"protein, carbs and fat imply (about {mm['expected']:.0f})"),
                            "fixes": _calorie_fixes(nutrients, mm, serving_g)})
    return out


def serving_grams(serving_size, serving_unit) -> float | None:
    """A food's serving in grams when its unit is grams, else None."""
    try:
        size = float(serving_size)
    except (TypeError, ValueError):
        return None
    unit = (serving_unit or "").strip().lower()
    return size if size > 0 and unit in ("g", "gr", "gram", "grams") else None


def apply_fix(conn, fdc_id: int, fix_id: str) -> dict | None:
    """Apply the fix `fix_id` if the food still has the problem it was
    offered for — worked out again from the food as it is now, so a stale
    page can't write a figure that no longer fits. Returns the fix applied,
    or None. Callers cascade (recipe_dcp.cascade_food_change)."""
    for issue in issues_for_food(conn, fdc_id):
        for fix in issue["fixes"]:
            if fix["id"] == fix_id:
                _db.correct_food_values(conn, fdc_id, fix["changes"], fix["reason"],
                                        estimated=fix["estimated"])
                return fix
    return None


def issues_for_food(conn, fdc_id: int) -> list[dict]:
    row = _db.get_cached_food(conn, fdc_id)
    if not row:
        return []
    try:
        nutrients = json.loads(row["nutrients_json"] or "{}")
    except (ValueError, TypeError):
        return []
    ignored = _db.food_data_ignores(conn).get(fdc_id, set())
    if row["is_supplement"]:
        ignored = ignored | SUPPLEMENT_SKIPS
    return food_issues(nutrients, estimated=_db.estimated_keys(conn, fdc_id),
                       ignored=ignored,
                       serving_g=serving_grams(row["serving_size"], row["serving_unit"]))


def _has_explicit_weight(unit: str) -> bool:
    return bool(re.search(r"\d\s*(?:g|gr|grams?|oz|ounces?|lbs?|pounds?|kg)\b", unit, re.IGNORECASE))


_BRACKETED_GRAMS_RE = re.compile(r"\(\s*[≈~]?\s*\d[\d.,/]*\s*(?:g|gr|grams?)\.?\s*\)", re.IGNORECASE)


def _bracketed_volume(unit: str) -> str | None:
    """"1/3 c (42 gr)" -> "1/3 c": a volume or portion with a gram figure in
    brackets after it, the form older versions of NuMa stored. None for
    anything else, including a weight typed on its own ("42 g") or inline
    ("2 T 15 g")."""
    if not _BRACKETED_GRAMS_RE.search(unit):
        return None
    rest = " ".join(_BRACKETED_GRAMS_RE.sub(" ", unit).split())
    return rest if rest and not _has_explicit_weight(rest) else None


def stale_amounts(conn, *, fdc_id: int | None = None, include_bracketed: bool = False,
                  include_kept: bool = False) -> list[dict]:
    """Recipe ingredients and logged meal foods whose stored grams no longer
    match what their typed volume/portion works out to now — for one food
    only if `fdc_id` is given.
    [{"where": "recipe"|"meal", "item_id", "owner_id", "owner_label",
      "fdc_id", "food_name", "typed", "stored_g", "now_g", "bracketed", "unit_after"}]
    "bracketed" rows (only with include_bracketed) are volumes stored with a
    gram figure in brackets; "unit_after" is the unit text to store on update
    (the bracketed figure dropped, since it would no longer be right).
    "kept" rows — the user chose "Keep as entered" and the grams haven't
    changed since (db.amount_keeps()) — are left out unless include_kept."""
    keeps = _db.amount_keeps(conn)
    foods = {r["fdc_id"]: r for r in conn.execute(
        "SELECT fdc_id, name, portions_json FROM foods")}
    rows = []
    sources = [
        ("recipe", conn.execute(
            "SELECT ri.id AS item_id, ri.recipe_id AS owner_id, r.name AS owner_label, ri.fdc_id, "
            "ri.food_name, ri.amount, ri.unit FROM recipe_ingredients ri JOIN recipes r ON r.id = ri.recipe_id "
            "WHERE ri.ref_recipe_id IS NULL AND ri.fdc_id IS NOT NULL" + (" AND ri.fdc_id = ?" if fdc_id is not None else ""),
            (fdc_id,) if fdc_id is not None else ()).fetchall()),
        ("meal", conn.execute(
            "SELECT mi.id AS item_id, mi.meal_id AS owner_id, m.meal_date || ' ' || m.name AS owner_label, "
            "mi.fdc_id, mi.food_name, mi.amount, mi.unit FROM meal_items mi JOIN meals m ON m.id = mi.meal_id "
            "WHERE mi.item_type = 'food' AND mi.fdc_id IS NOT NULL" + (" AND mi.fdc_id = ?" if fdc_id is not None else ""),
            (fdc_id,) if fdc_id is not None else ()).fetchall()),
    ]
    for where, items in sources:
        for it in items:
            food = foods.get(it["fdc_id"])
            unit = (it["unit"] or "").strip()
            if not food or not unit or not it["amount"]:
                continue
            unit_after = unit
            bracketed = False
            if _has_explicit_weight(unit):
                volume = _bracketed_volume(unit) if include_bracketed else None
                if volume is None:
                    continue
                unit_after, bracketed = volume, True
            try:
                portions = json.loads(food["portions_json"] or "[]") or []
            except (ValueError, TypeError):
                portions = []
            parsed = _parse_portion_input(unit_after, portions, food["name"])
            if not parsed or not parsed[0]:
                continue
            stored, now = float(it["amount"]), float(parsed[0])
            if abs(now - stored) >= max(_STALE_MIN_G, stored * _STALE_FRACTION):
                kept_g = keeps.get((where, it["item_id"]))
                kept = kept_g is not None and abs(kept_g - stored) < 0.005
                if kept and not include_kept:
                    continue
                rows.append({"where": where, "item_id": it["item_id"], "owner_id": it["owner_id"],
                             "owner_label": it["owner_label"], "fdc_id": it["fdc_id"],
                             "food_name": it["food_name"], "typed": unit,
                             "stored_g": stored, "now_g": now,
                             "bracketed": bracketed, "unit_after": unit_after, "kept": kept})
    rows.sort(key=lambda r: (r["where"], r["owner_label"].lower(), r["food_name"].lower()))
    return rows


def own_weight_text(unit: str, grams: float) -> str | None:
    """"8 c (2309 gr)" or "8 c" at 2309.216 g -> "2309.2 g (8 c)": the form
    NuMa stores for a weight typed with its volume. None if `unit` is already
    a weight of its own, or empty."""
    unit = (unit or "").strip()
    volume = _bracketed_volume(unit) or ("" if _has_explicit_weight(unit) else unit)
    if not volume or not grams:
        return None
    return f"{round(float(grams), 1):g} g ({volume})"


def keep_as_entered(conn, where: str, item_id: int) -> bool:
    """"Keep as entered": the stored grams are right (the user weighed it),
    so rewrite the amount's text in the form NuMa stores for a weight typed
    with its volume — "8 c (2309 gr)" or "8 c" stored as 2309.216 g becomes
    "2309.2 g (8 c)". That form is the user's own weight, so stale_amounts()
    never lists it again; there is nothing left to show or undo (editing the
    amount is the way to change it). Grams are untouched, so no totals move.
    Drops any db.amount_keeps row for the item. False if it isn't found."""
    table = "recipe_ingredients" if where == "recipe" else "meal_items"
    row = conn.execute(f"SELECT amount, unit FROM {table} WHERE id = ?", (item_id,)).fetchone()
    _db.amount_unkeep(conn, where, item_id)
    new = own_weight_text(row["unit"], row["amount"]) if row else None
    if new is None:
        return False
    conn.execute(f"UPDATE {table} SET unit = ? WHERE id = ?", (new, item_id))
    return True


def convert_keeps(conn) -> int:
    """Rewrite every db.amount_keeps row (from before keep_as_entered()
    rewrote the amount itself, or a starter recipe's shipped "kept") whose
    grams are still as kept; drop the rest. Run at startup; returns the
    number rewritten."""
    done = 0
    for (where, item_id), kept_g in _db.amount_keeps(conn).items():
        table = "recipe_ingredients" if where == "recipe" else "meal_items"
        row = conn.execute(f"SELECT amount FROM {table} WHERE id = ?", (item_id,)).fetchone()
        if row and row["amount"] is not None and abs(float(row["amount"]) - kept_g) < 0.005:
            done += keep_as_entered(conn, where, item_id)
        else:
            _db.amount_unkeep(conn, where, item_id)
    return done


def generic_density_in_use(conn) -> list[dict]:
    """Foods with volume amounts converted by the generic density table
    (portions.generic_density_kind()), most-used first:
    [{"fdc_id", "name", "uses_count", "uses": [{"where", "owner_id", "owner_label", "typed", "grams", "bracketed"}]}]"""
    foods = {r["fdc_id"]: r for r in conn.execute("SELECT fdc_id, name, portions_json FROM foods")}
    by_food: dict[int, dict] = {}
    sources = [
        ("recipe", "SELECT ri.recipe_id AS owner_id, r.name AS owner_label, ri.fdc_id, ri.unit, ri.amount "
                   "FROM recipe_ingredients ri JOIN recipes r ON r.id = ri.recipe_id "
                   "WHERE ri.ref_recipe_id IS NULL AND ri.fdc_id IS NOT NULL"),
        ("meal", "SELECT mi.meal_id AS owner_id, m.meal_date || ' ' || m.name AS owner_label, mi.fdc_id, mi.unit, "
                 "mi.amount FROM meal_items mi JOIN meals m ON m.id = mi.meal_id "
                 "WHERE mi.item_type = 'food' AND mi.fdc_id IS NOT NULL"),
    ]
    portions_cache: dict[int, list] = {}
    for where, sql in sources:
        for it in conn.execute(sql):
            food = foods.get(it["fdc_id"])
            if food is None:
                continue
            if it["fdc_id"] not in portions_cache:
                try:
                    portions_cache[it["fdc_id"]] = json.loads(food["portions_json"] or "[]") or []
                except (ValueError, TypeError):
                    portions_cache[it["fdc_id"]] = []
            kind = generic_density_kind(it["unit"], portions_cache[it["fdc_id"]], food["name"])
            if kind is None:
                continue
            entry = by_food.setdefault(it["fdc_id"], {"fdc_id": it["fdc_id"], "name": food["name"], "uses": []})
            entry["uses"].append({"where": where, "owner_id": it["owner_id"], "owner_label": it["owner_label"],
                                  "typed": it["unit"], "grams": it["amount"],
                                  "bracketed": kind == "bracketed"})
    for entry in by_food.values():
        entry["uses_count"] = len(entry["uses"])
    return sorted(by_food.values(), key=lambda f: (-f["uses_count"], f["name"].lower()))


def _is_usda_food(row) -> bool:
    from numa_app.services.food_ids import classify_food_id
    try:
        return classify_food_id(row["fdc_id"])[1] == "USDA" and not row["user_drafted"]
    except Exception:
        return False


def old_usda_copies(conn, *, days: int = OLD_COPY_DAYS) -> list[dict]:
    """USDA foods whose cached copy is more than `days` old."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    out = []
    for r in conn.execute("SELECT fdc_id, name, cached_at, user_drafted FROM foods "
                          "WHERE archived = 0 AND cached_at IS NOT NULL AND cached_at < ? "
                          "ORDER BY cached_at", (cutoff,)):
        if _is_usda_food(r):
            out.append({"fdc_id": r["fdc_id"], "name": r["name"], "cached_at": r["cached_at"]})
    return out


def scan(conn) -> dict:
    """Every current data problem in the database. Returns
    {"food_issues": [{"fdc_id", "name", "issues"}], "stale_amounts": [...],
     "gaps": [{"fdc_id", "name", "groups"}], "integrity": {...},
     "keys": set of stable issue keys (estimates and old copies excluded —
     they aren't problems, so they never trigger the reminder)}."""
    estimated = {r[0]: set(json.loads(r[1])) for r in conn.execute(
        "SELECT fdc_id, estimated_keys_json FROM foods WHERE estimated_keys_json IS NOT NULL")}
    ignores = _db.food_data_ignores(conn)
    checked = set(_completeness.DEFAULT_CHECKED)
    food_rows, gaps, keys = [], [], set()
    for row in conn.execute("SELECT fdc_id, name, nutrients_json, serving_size, serving_unit, user_drafted, "
                            "is_supplement FROM foods WHERE archived = 0 ORDER BY name"):
        try:
            n = json.loads(row["nutrients_json"] or "{}")
        except (ValueError, TypeError):
            continue
        if not isinstance(n, dict):
            continue
        ign = ignores.get(row["fdc_id"], set())
        if row["is_supplement"]:
            ign = ign | SUPPLEMENT_SKIPS
        issues = food_issues(n, estimated=estimated.get(row["fdc_id"], set()), ignored=ign,
                             serving_g=serving_grams(row["serving_size"], row["serving_unit"]))
        if issues:
            food_rows.append({"fdc_id": row["fdc_id"], "name": row["name"], "issues": issues,
                              "user_drafted": bool(row["user_drafted"])})
            keys |= {f"food:{row['fdc_id']}:{i['kind']}" for i in issues if i["severity"] == "problem"}
        active = _completeness.active_gaps(n, ign, checked)
        if active:
            gaps.append({"fdc_id": row["fdc_id"], "name": row["name"], "groups": active})
            keys |= {f"gap:{row['fdc_id']}:{g}" for g in active}
    stale = stale_amounts(conn, include_bracketed=True)
    keys |= {f"stale:{s['where']}:{s['item_id']}" for s in stale}
    integrity = _db.check_db_integrity(conn)
    for cat, items in integrity.items():
        for i, item in enumerate(items):
            ident = (item.get("id", item.get("fdc_id")) if isinstance(item, dict) else None)
            keys.add(f"integrity:{cat}:{ident if ident is not None else i}")
    return {"food_issues": food_rows, "stale_amounts": stale, "gaps": gaps,
            "integrity": integrity, "keys": keys}


# Group key for "not needed" on the portion list (food_data_ignores; the
# amino-acid list shares data_completeness's "aa" key).
PORTIONS_IGNORE_KEY = "portions"
# Everything a supplement (supplements.py) is never checked for: every
# nutrient group (so no calorie check and no missing-data gap), amino acids,
# portions. Applied as if marked "not needed", without writing those marks.
SUPPLEMENT_SKIPS = frozenset(_completeness.GROUP_KEYS) | {"aa", PORTIONS_IGNORE_KEY}


def usage_counts(conn) -> dict[int, dict]:
    """fdc_id -> {"recipes", "meals", "pantry", "total"} — distinct recipes
    and meals using the food directly, and pantry entries."""
    out: dict[int, dict] = {}

    def bump(fid, kind, n):
        d = out.setdefault(fid, {"recipes": 0, "meals": 0, "pantry": 0, "total": 0})
        d[kind] += n
        d["total"] += n
    for fid, n in conn.execute("SELECT fdc_id, COUNT(DISTINCT recipe_id) FROM recipe_ingredients "
                               "WHERE fdc_id IS NOT NULL AND ref_recipe_id IS NULL GROUP BY fdc_id"):
        bump(fid, "recipes", n)
    for fid, n in conn.execute("SELECT fdc_id, COUNT(DISTINCT meal_id) FROM meal_items "
                               "WHERE item_type = 'food' AND fdc_id IS NOT NULL GROUP BY fdc_id"):
        bump(fid, "meals", n)
    for fid, n in conn.execute("SELECT fdc_id, COUNT(*) FROM pantry WHERE fdc_id IS NOT NULL GROUP BY fdc_id"):
        bump(fid, "pantry", n)
    return out


def _foods_in_use(conn):
    usage = usage_counts(conn)
    ignores = _db.food_data_ignores(conn)
    for row in conn.execute("SELECT fdc_id, name, nutrients_json, portions_json, is_supplement "
                            "FROM foods WHERE archived = 0"):
        if row["fdc_id"] not in usage or row["is_supplement"]:
            continue   # a supplement has none of these food gaps
        try:
            n = json.loads(row["nutrients_json"] or "{}")
            portions = json.loads(row["portions_json"] or "[]") or []
        except (ValueError, TypeError):
            continue
        yield row, n, portions, usage[row["fdc_id"]], ignores.get(row["fdc_id"], set())


def missing_aa_in_use(conn) -> list[dict]:
    """Used foods with protein (≥ 1 g/100 g) but too few amino-acid values to
    score, most-used then most protein first. "ignored" = marked not needed."""
    from usda import has_amino_acid_data
    rows = []
    for row, n, _p, use, ign in _foods_in_use(conn):
        protein = float(n.get("protein_g") or 0)
        if protein >= 1 and not has_amino_acid_data(n):
            rows.append({"fdc_id": row["fdc_id"], "name": row["name"], "protein": protein,
                         "use": use, "ignored": "aa" in ign})
    rows.sort(key=lambda r: (-r["use"]["total"], -r["protein"], r["name"].lower()))
    return rows


def missing_portions_in_use(conn) -> list[dict]:
    """Used foods with no portion weights at all (no cup, spoon, piece...),
    so only a weight can be typed for them. Most-used first."""
    rows = []
    for row, _n, portions, use, ign in _foods_in_use(conn):
        if not portions:
            rows.append({"fdc_id": row["fdc_id"], "name": row["name"], "use": use,
                         "ignored": PORTIONS_IGNORE_KEY in ign})
    rows.sort(key=lambda r: (-r["use"]["total"], r["name"].lower()))
    return rows


# A food with less carbohydrate than this per 100 g isn't listed as missing a
# GI: a GI is barely meaningful for it, and in any normal amount its GL is tiny.
GI_LIST_MIN_CARBS = 5.0


def missing_gi_in_use(conn) -> list[dict]:
    """Used foods with GI_LIST_MIN_CARBS g or more carbohydrate per 100 g and
    no GI recorded, most-used then most carbohydrate first. "ignored" = GI
    marked "don't prompt me"."""
    ann = {r["fdc_id"]: r for r in conn.execute(
        "SELECT fdc_id, gi_estimate, gi_no_prompt FROM food_annotations")}
    rows = []
    for row, n, _p, use, _ign in _foods_in_use(conn):
        carbs = float(n.get("carbs_g") or 0)
        a = ann.get(row["fdc_id"])
        if carbs >= GI_LIST_MIN_CARBS and (a is None or a["gi_estimate"] is None):
            rows.append({"fdc_id": row["fdc_id"], "name": row["name"], "carbs": carbs,
                         "use": use, "ignored": bool(a is not None and a["gi_no_prompt"])})
    rows.sort(key=lambda r: (-r["use"]["total"], -r["carbs"], r["name"].lower()))
    return rows


def gi_not_needed(conn) -> list[dict]:
    """Every cached food whose GI is marked "don't prompt me" (not needed),
    whether or not it is used, low in carbohydrate or already has a GI.
    Rows match missing_gi_in_use()'s; "carbs" is None where unknown and
    "gi" is the recorded GI, if any. Alphabetical."""
    usage = usage_counts(conn)
    rows = []
    for row in conn.execute("SELECT f.fdc_id, f.name, f.nutrients_json, a.gi_estimate "
                            "FROM food_annotations a JOIN foods f ON f.fdc_id = a.fdc_id "
                            "WHERE a.gi_no_prompt = 1"):
        try:
            n = json.loads(row["nutrients_json"] or "{}")
        except (ValueError, TypeError):
            n = {}
        carbs = n.get("carbs_g") if isinstance(n, dict) else None
        rows.append({"fdc_id": row["fdc_id"], "name": row["name"],
                     "carbs": float(carbs) if carbs is not None else None,
                     "gi": row["gi_estimate"], "ignored": True,
                     "use": usage.get(row["fdc_id"], {"recipes": 0, "meals": 0, "pantry": 0, "total": 0})})
    rows.sort(key=lambda r: r["name"].lower())
    return rows


DAYS_EATEN_DEFAULT = 30


def _recipe_food_ids(conn, recipe_id: int, memo: dict[int, set[int]],
                     visiting: frozenset = frozenset()) -> set[int]:
    """Every food in a recipe, through its sub-recipes (a cycle stops)."""
    if recipe_id in memo:
        return memo[recipe_id]
    if recipe_id in visiting:
        return set()
    ids: set[int] = set()
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_id"]:
            ids |= _recipe_food_ids(conn, ing["ref_recipe_id"], memo, visiting | {recipe_id})
        elif ing["fdc_id"] is not None:
            ids.add(ing["fdc_id"])
    memo[recipe_id] = ids
    return ids


def foods_days_eaten(conn, end_date: str, days: int = DAYS_EATEN_DEFAULT) -> list[dict]:
    """Every food eaten in the `days` days ending on end_date (ISO), with
    the number of distinct days it was eaten — on its own in a meal, or
    inside a logged recipe (through sub-recipes). Most days first.

    Each row: fdc_id, name, days, recipe_days (days it came only from a
    recipe), carbs (per 100 g, None when the food has no carbohydrate
    value), carbs_not_needed (its macronutrients marked not needed, e.g. a
    supplement), gi_gap_days (days it left that day's glycemic load
    incomplete — glycemic_load's own rule, so a pinch of cinnamon, too
    little carbohydrate to matter, never counts) and gi_not_needed (GI
    "don't prompt me", which still leaves a day incomplete)."""
    from numa_app.services.glycemic_load import GAP_NO_GI, GAP_NOT_WANTED, combine_gl, meal_gl
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    start = (end - timedelta(days=max(days, 1) - 1)).isoformat()
    direct: dict[int, set[str]] = {}
    via_recipe: dict[int, set[str]] = {}
    memo: dict[int, set[int]] = {}
    gi_gap: dict[int, set[str]] = {}
    meals = _db.meal_list_by_date_range(conn, start, end.isoformat())
    by_date: dict[str, list] = {}
    for meal in meals:
        by_date.setdefault(meal["meal_date"], []).append(meal)
    for d, day_meals in by_date.items():
        for g in combine_gl([meal_gl(conn, m["id"]) for m in day_meals])["gaps"]:
            if g["reason"] in (GAP_NO_GI, GAP_NOT_WANTED) and g["fdc_id"] is not None:
                gi_gap.setdefault(g["fdc_id"], set()).add(d)
    for meal in meals:
        d = meal["meal_date"]
        for item in _db.meal_get_items(conn, meal["id"]):
            if item["item_type"] == "recipe" and item["recipe_id"]:
                for fid in _recipe_food_ids(conn, item["recipe_id"], memo):
                    via_recipe.setdefault(fid, set()).add(d)
            elif item["fdc_id"] is not None:
                direct.setdefault(item["fdc_id"], set()).add(d)
    ids = set(direct) | set(via_recipe)
    if not ids:
        return []
    ph = ",".join("?" * len(ids))
    foods = {r["fdc_id"]: r for r in conn.execute(
        f"SELECT fdc_id, name, nutrients_json, is_supplement FROM foods WHERE fdc_id IN ({ph})", list(ids))}
    ann = {r["fdc_id"]: r for r in conn.execute(
        f"SELECT fdc_id, gi_no_prompt FROM food_annotations WHERE fdc_id IN ({ph})", list(ids))}
    ignores = _db.food_data_ignores(conn)
    rows = []
    for fid in ids:
        food = foods.get(fid)
        if food is None:
            continue   # a food no longer cached; broken references are listed above
        try:
            n = json.loads(food["nutrients_json"] or "{}")
        except (ValueError, TypeError):
            n = {}
        if not isinstance(n, dict):
            n = {}
        carbs = n.get("carbs_g")
        carbs = float(carbs) if carbs is not None else None
        a = ann.get(fid)
        own = direct.get(fid, set())
        all_days = own | via_recipe.get(fid, set())
        rows.append({"fdc_id": fid, "name": food["name"], "days": len(all_days),
                     "recipe_days": len(all_days - own), "carbs": carbs,
                     # A supplement needs no carbohydrate value, as if marked not needed.
                     "carbs_not_needed": "macros" in ignores.get(fid, set()) or bool(food["is_supplement"]),
                     "is_supplement": bool(food["is_supplement"]),
                     "gi_gap_days": len(gi_gap.get(fid, set())),
                     "gi_not_needed": bool(a is not None and a["gi_no_prompt"])})
    rows.sort(key=lambda r: (-r["days"], r["name"].lower()))
    return rows


def wet_dry_in_use(conn) -> list[dict]:
    """Foods whose own name, or the name typed for them in a recipe or meal,
    says dry ("okara flour") while their data says mostly water
    (water.wet_dry_conflict) — most likely the wet record picked for the dry
    food. Each row names where it is used under a dry-sounding name
    ("recipes" / "meals": [{"id", "label", "typed"}]); used or not, a food
    whose OWN name conflicts is listed too. Only foods with a water value can
    be judged. Shown only while water tracking is on (Settings → 9)."""
    from numa_app.services import water as _water
    typed: dict[int, list[tuple[str, int, str, str]]] = {}
    for r in conn.execute("""SELECT ri.fdc_id, ri.food_name, r.id, r.name FROM recipe_ingredients ri
                             JOIN recipes r ON r.id = ri.recipe_id WHERE ri.fdc_id IS NOT NULL"""):
        typed.setdefault(r[0], []).append(("recipes", r[2], r[3], r[1] or ""))
    for r in conn.execute("""SELECT mi.fdc_id, mi.food_name, m.id, m.name, m.meal_date FROM meal_items mi
                             JOIN meals m ON m.id = mi.meal_id
                             WHERE mi.item_type = 'food' AND mi.fdc_id IS NOT NULL"""):
        typed.setdefault(r[0], []).append(("meals", r[2], f"{r[4]} {r[3]}", r[1] or ""))
    rows = []
    for row in conn.execute("SELECT fdc_id, name, nutrients_json FROM foods WHERE archived = 0"):
        try:
            n = json.loads(row["nutrients_json"] or "{}")
        except (ValueError, TypeError):
            continue
        own = _water.wet_dry_conflict([row["name"]], n)
        where: dict[str, list[dict]] = {"recipes": [], "meals": []}
        for kind, item_id, label, typed_name in typed.get(row["fdc_id"], []):
            if _water.wet_dry_conflict([typed_name], n) or own:
                if not any(w["id"] == item_id for w in where[kind]):
                    where[kind].append({"id": item_id, "label": label, "typed": typed_name})
        hit = own or next((_water.wet_dry_conflict([w["typed"]], n) for k in where for w in where[k]), None)
        if hit:
            rows.append({"fdc_id": row["fdc_id"], "name": row["name"], "water": hit["water"],
                         "word": hit["word"], "flagged_name": hit["name"], **where})
    rows.sort(key=lambda r: (-(len(r["recipes"]) + len(r["meals"])), r["name"].lower()))
    return rows


def _dup_name(name: str) -> str:
    n = name.lower().strip()
    n = re.sub(r"^\*\s*", "", n)
    n = re.sub(r"^copy of\s+", "", n)
    n = re.sub(r"\(fdc\s*\d+\)", "", n)
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", n).split())


def _edited_labels(conn, fdc_id: int, user_edited) -> "list[str] | None":
    """What the user has changed on this food, as labels ("Iron", "serving
    size", "portion “1 cup”"): [] when nothing, None when it was edited but
    which values can't be known (an edit from before source copies existed).
    A custom food's values are all the user's, so it isn't marked at all."""
    keys = _db.food_edited_keys(conn, fdc_id)
    if keys is None:
        return None if user_edited and not _db.is_custom_food_id(fdc_id) else []
    labels = []
    for k in keys:
        if k.startswith(_db.PORTION_KEY_PREFIX):
            labels.append(f"portion “{k[len(_db.PORTION_KEY_PREFIX):]}”")
        elif k in ("serving_size", "serving_unit"):
            if "serving size" not in labels:
                labels.append("serving size")
        else:
            labels.append(_usda.nutrient_label(k)[0])
    return labels


def duplicate_groups(conn, *, include_dismissed: bool = False) -> list[dict]:
    """[{"key", "name", "dismissed", "foods": [{"fdc_id", "name", "data_type",
    "use", "nutrient_count", "archived", "edited"}]}] — two or more foods whose
    names match once case, punctuation, a "* " prefix, "Copy of " and "(FDC n)"
    are ignored. key = the group's sorted fdc_ids, which is what a "not
    duplicates" dismissal remembers. edited: _edited_labels()."""
    usage = usage_counts(conn)
    dismissed = _db.duplicate_dismissals(conn)
    by_name: dict[str, list] = {}
    for row in conn.execute("SELECT fdc_id, name, data_type, nutrients_json, archived, user_edited "
                            "FROM foods ORDER BY fdc_id"):
        # A kept older version shares its food's name on purpose.
        if _db.is_version_id(row["fdc_id"]):
            continue
        by_name.setdefault(_dup_name(row["name"]), []).append(row)
    out = []
    for norm, rows in by_name.items():
        if len(rows) < 2 or not norm:
            continue
        key = ",".join(str(r["fdc_id"]) for r in sorted(rows, key=lambda r: r["fdc_id"]))
        if key in dismissed and not include_dismissed:
            continue
        foods = []
        for r in rows:
            try:
                count = len(json.loads(r["nutrients_json"] or "{}"))
            except (ValueError, TypeError):
                count = 0
            foods.append({"fdc_id": r["fdc_id"], "name": r["name"], "data_type": r["data_type"] or "",
                          "use": usage.get(r["fdc_id"], {"recipes": 0, "meals": 0, "pantry": 0, "total": 0}),
                          "nutrient_count": count, "archived": bool(r["archived"]),
                          "edited": _edited_labels(conn, r["fdc_id"], r["user_edited"])})
        out.append({"key": key, "name": rows[0]["name"], "dismissed": key in dismissed, "foods": foods})
    out.sort(key=lambda g: g["name"].lower())
    return out


def merge_review(conn, keep_id: int, drop_ids: list[int], groups) -> dict:
    """What merging `drop_ids` into `keep_id` would lose unless copied over:
    the values the dropped copies have that the kept one lacks or has
    differently, and their portions it doesn't have. For the review step
    before Keep this one (backend /food/cache/duplicates/review).

    Returns {"groups": [{"name", "fields": [{key, label, unit, current,
    current_mine, options: [{fdc_id, name, value, mine}], pick}]}],
    "portions": [{id, fdc_id, name, portion, mine}]}. `groups` is
    [(group_name, [(key, label, unit)])], as on the edit screens. One option
    per distinct value (two copies agreeing are offered once).

    pick = the default choice, an option's fdc_id or None to keep the kept
    food's value: a blank is filled (preferring a value the user edited); a
    value the user edited on a dropped copy wins over the kept food's,
    unless that one is the user's too. "mine" is known only for foods with a
    source copy (db.food_edited_keys) — otherwise nothing is presumed."""
    from numa_app.services.incoming_review import _same, new_portions

    def load(fid):
        row = _db.get_cached_food(conn, fid)
        if row is None:
            return None
        mine = _db.food_edited_keys(conn, fid)
        return {"fdc_id": fid, "name": row["name"],
                "nutrients": json.loads(row["nutrients_json"] or "{}"),
                "portions": json.loads(row["portions_json"] or "[]") or [],
                "mine": set(mine) if mine is not None else set()}
    keep = load(keep_id)
    others = [o for o in (load(d) for d in drop_ids if d != keep_id) if o]
    if keep is None:
        return {"groups": [], "portions": []}
    kn = keep["nutrients"]
    out_groups = []
    for group_name, fields in groups:
        rows = []
        for key, label, unit in fields:
            cur_blank = _completeness.is_blank(key, kn)
            opts: list[dict] = []
            for o in others:
                if _completeness.is_blank(key, o["nutrients"]):
                    continue
                v = o["nutrients"][key]
                if not cur_blank and _same(v, kn[key]):
                    continue
                same = next((x for x in opts if _same(x["value"], v)), None)
                if same:
                    same["mine"] = same["mine"] or key in o["mine"]
                    continue
                opts.append({"fdc_id": o["fdc_id"], "name": o["name"], "value": v, "mine": key in o["mine"]})
            if not opts:
                continue
            cur_mine = not cur_blank and key in keep["mine"]
            mine_opt = next((x["fdc_id"] for x in opts if x["mine"]), None)
            if cur_blank:
                pick = mine_opt or opts[0]["fdc_id"]
            else:
                pick = None if cur_mine else mine_opt
            rows.append({"key": key, "label": label, "unit": unit,
                         "current": None if cur_blank else kn[key], "current_mine": cur_mine,
                         "options": opts, "pick": pick})
        if rows:
            out_groups.append({"name": group_name, "fields": rows})
    portions = []
    have = list(keep["portions"])
    for o in others:
        for p in new_portions(have, o["portions"]):
            have.append(p)
            desc = str(p.get("description", "")).strip()
            portions.append({"id": f"{o['fdc_id']}|{desc}", "fdc_id": o["fdc_id"], "name": o["name"],
                             "portion": p, "mine": _db.PORTION_KEY_PREFIX + desc in o["mine"]})
    return {"groups": out_groups, "portions": portions}

