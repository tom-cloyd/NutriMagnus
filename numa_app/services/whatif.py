"""
whatif.py — non-destructive "what if I removed / added / replaced / scaled X"
analysis across a chosen set of meals: daily nutrient totals before and after
a scenario (a list of edits), without writing anything.

The edits reach every depth through the optional `rewrite` hook on
recipe_nutrients.expand_recipe_ingredients() — a food used inside a recipe
inside a meal is removed or replaced just like one logged on the meal
directly. "add" puts an item on every day in the selection that has at least
one meal logged (never on days with nothing logged, matching
nutrient_trend.average_from_daily_totals: "didn't log" is not "ate nothing").

Read-only by design: meals store nutrient snapshots and recipe edits trigger
DCP recomputes, so nothing here may call a write helper. Even the day-profile
lookup is done without day_profile.ensure_day_profile()'s pinning.
Docs: README-numa-documentation.md, "analysis_whatif.html" and the Architecture tree entry for whatif.py; user-manual.md #whatif
"""
import json
from dataclasses import dataclass, field

import db as _db
import diaas as _diaas
import profile as _profile
import usda as _usda
from numa_app.services.rda_status import rda_status
from numa_app.services.recipe_nutrients import expand_recipe_ingredients, recipe_serving_grams

Item = tuple[str, int]          # ("food", fdc_id) | ("recipe", recipe_id)

OPS = ("remove", "add", "replace", "scale")
REPLACE_BASES = ("grams", "servings", "stated")

# An added recipe ingredient this share of the recipe's weight or more, with
# no value for a nutrient, marks that nutrient's "after" as possibly low.
_UNKNOWN_SHARE = 0.10

SUMMARY_KEYS = ("calories", "protein_g", "dcp", "carbs_g", "sugar_g", "fat_g", "fiber_g")


class WhatIfError(ValueError):
    """A scenario that can't be evaluated as written (user-readable message)."""


@dataclass(frozen=True)
class Edit:
    """One change in a scenario.

    remove:  item, wherever it appears.
    scale:   item, wherever it appears, times `amount` (0.5 = half).
    replace: item -> replacement, wherever item appears. basis "grams" keeps
             the same weight, "servings" the same servings count (recipe to
             recipe only), "stated" uses `amount` in `unit` at each place.
    add:     item, `amount` in `unit`, once on every logged day.
    unit is "g" or "servings" (servings only for a recipe).
    """
    op: str
    item: Item
    replacement: Item | None = None
    amount: float | None = None
    unit: str = "g"
    basis: str = "grams"


@dataclass
class _Ctx:
    conn: object
    edits: list[Edit]
    serving_g: dict[int, float | None] = field(default_factory=dict)
    recipe_servings: dict[int, float | None] = field(default_factory=dict)
    food_nuts: dict[int, dict] = field(default_factory=dict)
    current_meal: dict | None = None
    hits: dict[int, set[int]] = field(default_factory=dict)   # edit index -> meal ids

    def grams_per_serving(self, recipe_id: int) -> float | None:
        if recipe_id not in self.serving_g:
            self.serving_g[recipe_id] = recipe_serving_grams(recipe_id, self.conn)
        return self.serving_g[recipe_id]

    def servings_of(self, recipe_id: int) -> float | None:
        """A recipe's batch servings count, None if the recipe is gone."""
        if recipe_id not in self.recipe_servings:
            row = _db.recipe_get(self.conn, recipe_id)
            self.recipe_servings[recipe_id] = float(row["servings"] or 1) if row else None
        return self.recipe_servings[recipe_id]

    def nutrients_100g(self, fdc_id: int) -> dict:
        if fdc_id not in self.food_nuts:
            cached = _db.get_cached_food(self.conn, fdc_id)
            self.food_nuts[fdc_id] = (json.loads(cached["nutrients_json"])
                                      if cached and cached["nutrients_json"] else {})
        return self.food_nuts[fdc_id]

    def _to_grams(self, kind: str, item_id: int, qty: float) -> float:
        if kind == "food":
            return qty
        per = self.grams_per_serving(item_id)
        if not per:
            raise WhatIfError(f"{item_name(self.conn, (kind, item_id))} has no known serving weight, "
                              "so it can't be matched by weight. Give it a total weight, or match by servings.")
        return qty * per

    def _from_grams(self, kind: str, item_id: int, grams: float) -> float:
        if kind == "food":
            return grams
        per = self.grams_per_serving(item_id)
        if not per:
            raise WhatIfError(f"{item_name(self.conn, (kind, item_id))} has no known serving weight, "
                              "so it can't be used by weight. Give it a total weight, or use servings.")
        return grams / per

    def rewrite(self, kind: str, item_id: int, qty: float) -> list[tuple[str, int, float]]:
        """The recipe_nutrients.Rewrite hook: every scale edit on this item
        applies, then the first remove/replace. A replacement is not itself
        rewritten at this level (its own ingredients still are, deeper down)."""
        for i, e in enumerate(self.edits):
            if e.op == "scale" and e.item == (kind, item_id):
                qty *= e.amount
                self._hit(i)
        for i, e in enumerate(self.edits):
            if e.item != (kind, item_id) or e.op not in ("remove", "replace"):
                continue
            self._hit(i)
            if e.op == "remove":
                return []
            new_kind, new_id = e.replacement
            if e.basis == "servings":
                new_qty = qty
            elif e.basis == "stated":
                new_qty = e.amount if e.unit == "servings" else self._from_grams(new_kind, new_id, e.amount)
            else:
                new_qty = self._from_grams(new_kind, new_id, self._to_grams(kind, item_id, qty))
            return [(new_kind, new_id, new_qty)]
        return [(kind, item_id, qty)]

    def _hit(self, i: int) -> None:
        if self.current_meal is not None:
            self.hits.setdefault(i, set()).add(self.current_meal["id"])

    def item_breakdown(self, kind: str, item_id: int, qty: float, *, rewrite,
                       name: str | None = None) -> tuple[dict, list[dict]]:
        """(nutrients, leaf foods) for qty of one item — grams of a food,
        servings of a recipe. Leaves are what diaas.meal_level_diaas() takes;
        `name` is the logged food name (DIAAS overrides are keyed by name)."""
        if kind == "food":
            nuts = self.nutrients_100g(item_id)
            leaves = [{"food_name": name or item_name(self.conn, (kind, item_id)), "fdc_id": item_id,
                       "nutrients_100g": nuts, "grams": qty}] if nuts else []
            return _usda.scale_nutrients(nuts, qty), leaves
        servings = self.servings_of(item_id)
        if servings is None:
            return {}, []
        leaves = expand_recipe_ingredients(item_id, self.conn, portion_factor=qty / servings, rewrite=rewrite)
        total: dict[str, float] = {}
        for leaf in leaves:
            _add(total, _usda.scale_nutrients(leaf["nutrients_100g"], leaf["grams"]))
        return total, leaves


def item_name(conn, item: Item) -> str:
    """A food's or recipe's display name."""
    kind, item_id = item
    if kind == "recipe":
        row = _db.recipe_get(conn, item_id)
        return row["name"] if row else f"recipe {item_id}"
    row = _db.get_cached_food(conn, item_id)
    return row["name"] if row else f"food {item_id}"


def _add(total: dict, more: dict) -> None:
    for k, v in more.items():
        total[k] = total.get(k, 0.0) + v


def meal_breakdown(meal_id: int, conn, ctx: _Ctx | None = None) -> tuple[dict[str, float], list[dict]]:
    """A meal's (nutrient total, leaf foods), with ctx's edits applied when
    ctx is given.

    Without ctx the total equals the total_nutrients of web/backend.py's
    _meal_expand_for_diaas() (tests hold the two together); it is kept
    separate because that function also builds the meal page's display rows
    and records serving weights (a write)."""
    ctx = ctx or _Ctx(conn, [])
    rewrite = ctx.rewrite if ctx.edits else None
    total: dict[str, float] = {}
    leaves: list[dict] = []
    for row in _db.meal_get_items(conn, meal_id):
        if row["item_type"] == "food" and row["fdc_id"]:
            entries = [("food", row["fdc_id"], float(row["amount"]))]
        elif row["item_type"] == "recipe" and row["recipe_id"]:
            entries = [("recipe", row["recipe_id"], float(row["amount"]))]
        else:
            continue
        logged = entries[0][:2]
        if rewrite:
            entries = rewrite(*entries[0])
        for kind, item_id, qty in entries:
            nuts, item_leaves = ctx.item_breakdown(
                kind, item_id, qty, rewrite=rewrite,
                name=row["food_name"] if (kind, item_id) == logged else None)
            _add(total, nuts)
            leaves.extend(item_leaves)
    return total, leaves


def meal_nutrients(meal_id: int, conn, ctx: _Ctx | None = None) -> dict[str, float]:
    """meal_breakdown()'s nutrient total alone."""
    return meal_breakdown(meal_id, conn, ctx)[0]


def day_dcp(leaves: list[dict], conn) -> float | None:
    """A day's Digestible Complete Protein (g) from all its leaf foods pooled,
    as the Daily Summary computes it; None when it can't be worked out (no
    amino-acid data, no protein)."""
    if not leaves:
        return None
    try:
        result = _diaas.meal_level_diaas(leaves, conn)
    except Exception:
        return None
    if not result or not result.get("diaas") or result.get("total_protein_g", 0) <= 0:
        return None
    return result.get("digestible_complete_protein_g") or 0.0


def _contains(conn, recipe_id: int, item: Item, seen: set[int] | None = None) -> bool:
    """True if `item` is used anywhere inside recipe_id (any depth)."""
    seen = seen if seen is not None else set()
    if recipe_id in seen:
        return False
    seen.add(recipe_id)
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_id"]:
            if item == ("recipe", ing["ref_recipe_id"]) or _contains(conn, ing["ref_recipe_id"], item, seen):
                return True
        elif ing["fdc_id"] and item == ("food", ing["fdc_id"]):
            return True
    return False


def validate(edits: list[Edit], conn) -> list[str]:
    """User-readable problems with a scenario, [] if it can be evaluated."""
    problems = []
    for n, e in enumerate(edits, 1):
        where = f"Change {n}"
        if e.op not in OPS:
            problems.append(f"{where}: unknown action \"{e.op}\".")
            continue
        if e.op == "replace" and e.replacement is None:
            problems.append(f"{where}: choose what to replace it with.")
            continue
        if e.op == "replace" and e.replacement == e.item:
            problems.append(f"{where}: an item can't replace itself.")
        if e.op == "scale" and (e.amount is None or e.amount < 0):
            problems.append(f"{where}: give a multiplier, such as 0.5 for half.")
        added = e.item if e.op == "add" else e.replacement
        needs_amount = e.op == "add" or (e.op == "replace" and e.basis == "stated")
        if needs_amount and (e.amount is None or e.amount <= 0):
            problems.append(f"{where}: give an amount.")
        if needs_amount and e.unit == "servings" and added and added[0] != "recipe":
            problems.append(f"{where}: a food is measured by weight or portion, not servings.")
        if e.op == "replace" and e.basis == "servings" and (e.item[0], e.replacement[0]) != ("recipe", "recipe"):
            problems.append(f"{where}: \"same servings\" only works recipe for recipe; use same weight instead.")
        if e.op == "replace" and e.replacement[0] == "recipe" and _contains(conn, e.replacement[1], e.item):
            problems.append(f"{where}: {item_name(conn, e.replacement)} itself contains "
                            f"{item_name(conn, e.item)}, so the replacement would go round in circles.")
        for kind, item_id in filter(None, (e.item, e.replacement)):
            if kind == "recipe" and _db.recipe_get(conn, item_id) is None:
                problems.append(f"{where}: recipe R{item_id} doesn't exist.")
            elif kind == "food" and _db.get_cached_food(conn, item_id) is None:
                problems.append(f"{where}: that food isn't in your Food Cache.")
    return problems


def _missing_keys(ctx: _Ctx, item: Item, keys: list[str]) -> set[str]:
    """Nutrient keys an added item has no value for (see _UNKNOWN_SHARE)."""
    kind, item_id = item
    if kind == "food":
        nuts = ctx.nutrients_100g(item_id)
        return {k for k in keys if nuts.get(k) is None}
    leaves = expand_recipe_ingredients(item_id, ctx.conn)
    weight = sum(leaf["grams"] for leaf in leaves)
    if weight <= 0:
        return set(keys)
    missing = set()
    for k in keys:
        lacking = sum(leaf["grams"] for leaf in leaves if leaf["nutrients_100g"].get(k) is None)
        if lacking / weight >= _UNKNOWN_SHARE:
            missing.add(k)
    return missing


def _profile_for_date(conn, meal_date: str, fallback):
    """The profile pinned to meal_date, read-only: an unpinned date falls
    back to the active profile without pinning it (pinning writes)."""
    row = _db.day_profile_get(conn, meal_date)
    if row is None:
        return fallback
    return _profile.UserProfile(**json.loads(row["profile_json"]))


def _row_keys(groups: list[tuple[str, list[str]]], *totals: dict) -> list[tuple[str, list[str]]]:
    """Display groups, plus "Other" for any non-amino-acid key present in the
    totals but not in a group — new nutrients show up without code changes."""
    known = {k for _, keys in groups for k in keys}
    extra = sorted({k for t in totals for k in t if k not in known and not k.startswith("aa_")})
    return list(groups) + ([("Other", extra)] if extra else [])


def evaluate_meals(conn, meals: list[dict], edits: list[Edit], *,
                   groups: list[tuple[str, list[str]]], diet_pref: str = "all",
                   days: str = "all") -> dict:
    """Before/after daily totals for `meals` (rows with id, meal_date) under
    `edits`. Raises WhatIfError if an edit can't be applied (e.g. a recipe
    with no serving weight matched by weight). Writes nothing.

    days="all" averages over every day in the selection with a meal logged;
    days="touched" only over the days a remove/replace/scale edit actually
    found its item (an add lands on every day, so it doesn't narrow them).
    With no such edit, "touched" falls back to "all"."""
    problems = validate(edits, conn)
    if problems:
        raise WhatIfError(" ".join(problems))

    base_ctx = _Ctx(conn, [])
    ctx = _Ctx(conn, edits)
    before: dict[str, dict] = {}
    after: dict[str, dict] = {}
    leaves_before: dict[str, list] = {}
    leaves_after: dict[str, list] = {}
    for meal in sorted(meals, key=lambda m: (m["meal_date"], m["id"])):
        d = meal["meal_date"]
        nuts, leaves = meal_breakdown(meal["id"], conn, base_ctx)
        _add(before.setdefault(d, {}), nuts)
        leaves_before.setdefault(d, []).extend(leaves)
        ctx.current_meal = meal
        nuts, leaves = meal_breakdown(meal["id"], conn, ctx)
        _add(after.setdefault(d, {}), nuts)
        leaves_after.setdefault(d, []).extend(leaves)
    ctx.current_meal = None

    # Like nutrient_trend: a day counts once something with nutrients is logged.
    dates = sorted(d for d in before if before[d])
    rewrite = ctx.rewrite if edits else None
    for i, e in enumerate(edits):
        if e.op != "add" or not dates:
            continue
        kind, item_id = e.item
        qty = e.amount if e.unit == "servings" else ctx._from_grams(kind, item_id, e.amount)
        added, added_leaves = ctx.item_breakdown(kind, item_id, qty, rewrite=rewrite)
        for d in dates:
            _add(after[d], added)
            leaves_after[d].extend(added_leaves)
        ctx.hits[i] = {m["id"] for m in meals}

    all_dates = dates
    date_of = {m["id"]: m["meal_date"] for m in meals}
    targeted = any(e.op != "add" for e in edits)
    touched = sorted({date_of[mid] for i, e in enumerate(edits) if e.op != "add"
                      for mid in ctx.hits.get(i, ())})
    days_mode = "touched" if days == "touched" and targeted else "all"
    if days_mode == "touched":
        dates = touched

    # Targets from each day's own pinned profile.
    active = _profile.load_profile()
    rda_by_day, ul_by_day = {}, {}
    for d in dates:
        p = _profile_for_date(conn, d, active)
        rda_by_day[d] = _profile.compute_rda(p, diet_pref=diet_pref) if p else {}
        ul_by_day[d] = _profile.get_max_limits(p) if p else {}

    n = len(dates)
    avg_before = {k: sum(before[d].get(k, 0.0) for d in dates) / n for k in _keys(before)} if n else {}
    avg_after = {k: sum(after[d].get(k, 0.0) for d in dates) / n for k in _keys(after)} if n else {}

    sections = _row_keys(groups, avg_before, avg_after)
    all_keys = [k for _, keys in sections for k in keys]
    added_items = [e.item if e.op == "add" else e.replacement for i, e in enumerate(edits)
                   if e.op in ("add", "replace") and ctx.hits.get(i)]
    unknown: dict[str, list[str]] = {}
    for item in dict.fromkeys(added_items):
        for k in _missing_keys(ctx, item, all_keys):
            unknown.setdefault(k, []).append(item_name(conn, item))

    out_sections = []
    for group_name, keys in sections:
        rows = []
        for key in keys:
            row = _nutrient_row(key, dates, before, after, avg_before, avg_after,
                                rda_by_day, ul_by_day, unknown.get(key, []))
            if row:
                rows.append(row)
        if rows:
            out_sections.append({"name": group_name, "rows": rows})

    edit_report = []
    for i, e in enumerate(edits):
        meal_ids = ctx.hits.get(i, set())
        days = {m["meal_date"] for m in meals if m["id"] in meal_ids}
        edit_report.append({"edit": e, "item_name": item_name(conn, e.item),
                            "replacement_name": item_name(conn, e.replacement) if e.replacement else None,
                            "meals": len(meal_ids), "days": len(days)})

    return {
        "dates":    dates,
        "meals":    sum(1 for m in meals if m["meal_date"] in set(dates)),
        "all_days": len(all_dates),
        "touched_days": len(touched) if targeted else None,
        "days_mode": days_mode,
        "sections": out_sections,
        "summary":  [_dcp_cell(conn, dates, leaves_before, leaves_after) if k == "dcp"
                     else _summary_cell(k, avg_before, avg_after) for k in SUMMARY_KEYS],
        "edits":    edit_report,
        "has_profile": any(rda_by_day.values()),
    }


def _keys(by_day: dict[str, dict]) -> set[str]:
    return {k for day in by_day.values() for k in day}


def _dcp_cell(conn, dates, leaves_before, leaves_after) -> dict:
    """Average daily DCP before and after, over the days where it could be
    worked out both times (days lacking amino-acid data are counted in
    `days` vs `of_days` rather than averaged in as zero)."""
    pairs = []
    for d in dates:
        b, a = day_dcp(leaves_before[d], conn), day_dcp(leaves_after[d], conn)
        if b is not None or a is not None:
            pairs.append((b or 0.0, a or 0.0))
    n = len(pairs)
    b = sum(p[0] for p in pairs) / n if n else 0.0
    a = sum(p[1] for p in pairs) / n if n else 0.0
    return {"key": "dcp", "label": "Protein (DCP)", "unit": "g", "before": b, "after": a,
            "delta": a - b, "days": n, "of_days": len(dates)}


def _summary_cell(key: str, avg_before: dict, avg_after: dict) -> dict:
    label, unit = _usda.nutrient_label(key)
    b, a = avg_before.get(key, 0.0), avg_after.get(key, 0.0)
    return {"key": key, "label": label, "unit": unit, "before": b, "after": a, "delta": a - b}


def _nutrient_row(key, dates, before, after, avg_before, avg_after,
                  rda_by_day, ul_by_day, unknown_names) -> dict | None:
    b, a = avg_before.get(key, 0.0), avg_after.get(key, 0.0)
    targets = [rda_by_day[d][key] for d in dates if key in rda_by_day[d] and rda_by_day[d][key][0] > 0]
    if not b and not a and not targets:
        return None
    label, unit = _usda.nutrient_label(key)
    row = {
        "key": key, "label": label, "unit": unit,
        "before": b, "after": a, "delta": a - b,
        "delta_pct": (a - b) / b * 100 if b else None,
        "changed": abs(a - b) > 1e-9,
        "unknown": unknown_names,
        "target": None, "target_type": None,
        "pct_before": None, "pct_after": None,
        "status_before": None, "status_after": None,
        "days_unmet_before": None, "days_unmet_after": None,
        "ul": None, "days_over_ul_before": None, "days_over_ul_after": None,
    }
    if targets:
        rda_type = targets[0][2]
        target = sum(t[0] for t in targets) / len(targets)
        row.update(target=target, target_type=rda_type,
                   pct_before=b / target * 100, pct_after=a / target * 100)
        row["status_before"] = rda_status(row["pct_before"], rda_type)
        row["status_after"] = rda_status(row["pct_after"], rda_type)

        def unmet(by_day):
            count = 0
            for d in dates:
                t = rda_by_day[d].get(key)
                if t and t[0] > 0 and rda_status(by_day[d].get(key, 0.0) / t[0] * 100, t[2]) != "met":
                    count += 1
            return count
        row["days_unmet_before"], row["days_unmet_after"] = unmet(before), unmet(after)
    uls = [ul_by_day[d][key] for d in dates if ul_by_day[d].get(key)]
    if uls:
        row["ul"] = sum(uls) / len(uls)

        def over(by_day):
            return sum(1 for d in dates
                       if ul_by_day[d].get(key) and by_day[d].get(key, 0.0) > ul_by_day[d][key])
        row["days_over_ul_before"], row["days_over_ul_after"] = over(before), over(after)
    return row
