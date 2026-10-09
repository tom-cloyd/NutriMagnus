"""
data_quality.py — every data-quality check NuMa runs, in one place.

The Database check page (Foods → 9), the Home page reminder, the note shown
right after a food is added to a meal or recipe, and a food's own page all
read from here, so they can't drift apart. The checks themselves:

- food_issues(): one food's problems — no calories, calories estimated from
  protein/carbs/fat, calories that don't fit them (energy_check.py), and
  impossible values (impossible_values()).
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
- duplicate_groups(): foods with the same name once case, a "* " starter
  prefix, "Copy of " and "(FDC n)" are ignored; run on request only.
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


def impossible_values(nutrients: dict) -> list[str]:
    """Plain-language descriptions of values that can't be right per 100 g:
    negatives, any one macronutrient over 100 g, protein + carbs + fat over
    100 g, sugars more than carbohydrate, or the three fat types more than
    total fat (each is a part of the other)."""
    out = []
    neg = [k for k, v in nutrients.items() if isinstance(v, (int, float)) and v < 0]
    if neg:
        out.append("negative value" + ("s" if len(neg) > 1 else "") + " (" + ", ".join(sorted(neg)) + ")")
    for k in _GRAM_KEYS:
        v = nutrients.get(k)
        if v is not None and v > _SINGLE_LIMIT_G:
            out.append(f"{v:g} g of {_LABELS[k]} per 100 g")
    p, c, f = (nutrients.get(k) for k in ("protein_g", "carbs_g", "fat_g"))
    if None not in (p, c, f) and p + c + f > _MACRO_SUM_LIMIT_G and not any(
            nutrients.get(k, 0) > _SINGLE_LIMIT_G for k in ("protein_g", "carbs_g", "fat_g")):
        out.append(f"protein, carbohydrate and fat add up to {p + c + f:.0f} g per 100 g")
    sugar = nutrients.get("sugar_g")
    if sugar is not None and c is not None and sugar > c * 1.05 + 0.5:
        out.append(f"more sugars ({sugar:g} g) than carbohydrate ({c:g} g)")
    parts = [nutrients.get(k) for k in ("saturated_fat_g", "mono_fat_g", "poly_fat_g")]
    if f is not None and any(x is not None for x in parts):
        total = sum(x or 0 for x in parts)
        if total > f * 1.1 + 0.5:
            out.append(f"the three fat types ({total:.1f} g) add up to more than total fat ({f:g} g)")
    return out


def food_issues(nutrients: dict, *, estimated: set[str] = frozenset(),
                ignored: set[str] = frozenset()) -> list[dict]:
    """One food's data problems as [{"kind", "severity", "text"}], worst
    first. kind: impossible | calories_missing | calories_mismatch |
    calories_estimated. severity "problem" or "note" (an estimate is
    information, not something wrong). Calorie checks are skipped for a food
    whose macronutrients the user marked "not needed"; the mismatch check
    alone is skipped for one whose calories they confirmed (CALORIES_OK_KEY)."""
    out = [{"kind": "impossible", "severity": "problem", "text": t}
           for t in impossible_values(nutrients)]
    if "macros" not in ignored:
        if _energy.calories_missing(nutrients):
            out.append({"kind": "calories_missing", "severity": "problem",
                        "text": "no calorie value, so it adds nothing to any calorie total"})
        elif "calories" in estimated:
            out.append({"kind": "calories_estimated", "severity": "note",
                        "text": "calories estimated from its protein, carbs and fat (its source gave none)"})
        elif CALORIES_OK_KEY not in ignored:
            mm = _energy.calorie_mismatch(nutrients)
            if mm:
                out.append({"kind": "calories_mismatch", "severity": "problem",
                            "text": (f"its calories ({mm['stored']:.0f} kcal per 100 g) are far from what its "
                                     f"protein, carbs and fat imply (about {mm['expected']:.0f})")})
    return out


def issues_for_food(conn, fdc_id: int) -> list[dict]:
    row = _db.get_cached_food(conn, fdc_id)
    if not row:
        return []
    try:
        nutrients = json.loads(row["nutrients_json"] or "{}")
    except (ValueError, TypeError):
        return []
    return food_issues(nutrients, estimated=_db.estimated_keys(conn, fdc_id),
                       ignored=_db.food_data_ignores(conn).get(fdc_id, set()))


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
    for row in conn.execute("SELECT fdc_id, name, nutrients_json FROM foods WHERE archived = 0 ORDER BY name"):
        try:
            n = json.loads(row["nutrients_json"] or "{}")
        except (ValueError, TypeError):
            continue
        if not isinstance(n, dict):
            continue
        ign = ignores.get(row["fdc_id"], set())
        issues = food_issues(n, estimated=estimated.get(row["fdc_id"], set()), ignored=ign)
        if issues:
            food_rows.append({"fdc_id": row["fdc_id"], "name": row["name"], "issues": issues})
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
    for row in conn.execute("SELECT fdc_id, name, nutrients_json, portions_json FROM foods WHERE archived = 0"):
        if row["fdc_id"] not in usage:
            continue
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


def _dup_name(name: str) -> str:
    n = name.lower().strip()
    n = re.sub(r"^\*\s*", "", n)
    n = re.sub(r"^copy of\s+", "", n)
    n = re.sub(r"\(fdc\s*\d+\)", "", n)
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", n).split())


def duplicate_groups(conn, *, include_dismissed: bool = False) -> list[dict]:
    """[{"key", "name", "dismissed", "foods": [{"fdc_id", "name", "data_type",
    "use", "nutrient_count", "archived"}]}] — two or more foods whose names
    match once case, punctuation, a "* " prefix, "Copy of " and "(FDC n)" are
    ignored. key = the group's sorted fdc_ids, which is what a "not
    duplicates" dismissal remembers."""
    usage = usage_counts(conn)
    dismissed = _db.duplicate_dismissals(conn)
    by_name: dict[str, list] = {}
    for row in conn.execute("SELECT fdc_id, name, data_type, nutrients_json, archived FROM foods ORDER BY fdc_id"):
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
                          "nutrient_count": count, "archived": bool(r["archived"])})
        out.append({"key": key, "name": rows[0]["name"], "dismissed": key in dismissed, "foods": foods})
    out.sort(key=lambda g: g["name"].lower())
    return out

