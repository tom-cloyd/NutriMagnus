"""
incoming_review.py — compare a cached food with incoming data and decide,
value by value, what to take.

Two kinds of incoming data share one review screen:

  * a fresh copy of the same food from USDA (Refresh), and
  * another food's values (Fill in nutrients from another food).

Each nutrient is classified against what the food has now:

  fill     — the food has no usable value (data_completeness.is_blank) and
             the incoming data does. Always ticked by default.
  differs  — both have a value and they differ. Ticked by default only when
             prefer_incoming is True: a USDA refresh of a food the user has
             never edited, where the old value is just USDA's older figure.
             On an edited food, or from another food, the current value wins
             unless the user ticks it.
  same     — nothing to decide; shown as a count only.
  dropped  — the food has a value the incoming data lacks. Never removed;
             listed so the user knows (only meaningful for a USDA refresh).

Estimated values yield to measured ones: a value NuMa estimated or borrowed
(see db.estimated_keys — anything filled in from another food, amino acids
scaled to this food's protein) is ticked for replacement by default when a
USDA refresh brings a measured figure for it (`estimated`, flag on the row).

From another food, amino acids are not copied raw: they're scaled to this
food's protein (aa_estimate.scaled_aa) — to the incoming protein if that is
ticked too, which the screen shows live and the apply step recomputes.

Name / brand / serving fields follow the same fill/differs rules (USDA
refresh only). Portions are never replaced, because logged amounts such as
"p1" point into the existing list; incoming portions whose description the
food doesn't already have are offered as additions, ticked by default.

Docs: README-numa-documentation.md → "Reviewing incoming data (refresh and fill-from)"
"""
from __future__ import annotations

import math

from numa_app.services.data_completeness import is_blank

META_FIELDS: list[tuple[str, str]] = [
    ("name",         "Name"),
    ("brand",        "Brand"),
    ("data_type",    "Type"),
    ("serving_size", "Serving size"),
    ("serving_unit", "Serving unit"),
]


# Meta fields whose edits count (db._TRACKED_SCALARS); name/brand/type don't.
TRACKED_META = ("serving_size", "serving_unit")


def _same(a, b) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=1e-6, abs_tol=1e-9)
    except (TypeError, ValueError):
        return a == b


def nutrient_review(current: dict, incoming: dict, groups, *, prefer_incoming: bool,
                    estimated: "set[str] | frozenset[str]" = frozenset(),
                    mine: "set[str] | None" = None) -> dict:
    """Classify every nutrient in `groups` ([(group_name, [(key, label, unit)])])
    that either side has. Returns {"groups": [{"name", "fields": [...]}],
    "same_count": int, "dropped": [field, ...]}; each field is
    {key, label, unit, current, incoming, status, checked, estimated}.
    `estimated`: keys whose current value is an estimate — a differing
    incoming (measured) value is ticked for those.
    `mine`: the keys whose current value is the user's own edit (db.
    food_edited_keys), when known. Then it decides per value instead of
    prefer_incoming: a differing value is ticked unless it's the user's.
    Each field carries `mine` for the screen to say so."""
    out_groups, dropped, same_count = [], [], 0
    for group_name, fields in groups:
        rows = []
        for key, label, unit in fields:
            cur_blank = is_blank(key, current)
            inc_blank = is_blank(key, incoming)
            row = {"key": key, "label": label, "unit": unit,
                   "current": None if cur_blank else current[key],
                   "incoming": None if inc_blank else incoming[key],
                   "estimated": key in estimated and not cur_blank,
                   "mine": mine is not None and key in mine and not cur_blank}
            if inc_blank:
                if not cur_blank and key not in incoming:
                    dropped.append({**row, "status": "dropped", "checked": False})
                continue
            if cur_blank:
                rows.append({**row, "status": "fill", "checked": True})
            elif _same(current[key], incoming[key]):
                same_count += 1
            else:
                take = (key not in mine) if mine is not None else prefer_incoming
                rows.append({**row, "status": "differs",
                             "checked": take or row["estimated"]})
        if rows:
            out_groups.append({"name": group_name, "fields": rows})
    return {"groups": out_groups, "same_count": same_count, "dropped": dropped}


def meta_review(current: dict, incoming: dict, *, prefer_incoming: bool,
                mine: "set[str] | None" = None) -> list[dict]:
    """Rows for the name/brand/type/serving fields whose incoming value is
    non-empty and differs from the food's own. `mine` as in
    nutrient_review(), for the tracked ones (serving size and unit); name,
    brand and type aren't tracked, so they follow prefer_incoming."""
    rows = []
    for key, label in META_FIELDS:
        inc = incoming.get(key)
        if inc in (None, ""):
            continue
        cur = current.get(key)
        if cur not in (None, "") and _same(cur, inc):
            continue
        status = "fill" if cur in (None, "") else "differs"
        tracked = key in TRACKED_META
        take = (key not in mine) if (mine is not None and tracked) else prefer_incoming
        rows.append({"key": key, "label": label, "current": cur, "incoming": inc,
                     "status": status, "checked": status == "fill" or take, "tracked": tracked,
                     "mine": mine is not None and tracked and key in mine and status == "differs"})
    return rows


def new_portions(current_portions: list[dict], incoming_portions: list[dict]) -> list[dict]:
    """Incoming portions the food doesn't already have (matched on
    description, case-insensitively). Existing portions are never touched."""
    have = {str(p.get("description", "")).strip().lower() for p in current_portions or []}
    out = []
    for p in incoming_portions or []:
        desc = str(p.get("description", "")).strip()
        if desc and desc.lower() not in have and p.get("gram_weight"):
            have.add(desc.lower())
            out.append(p)
    return out
