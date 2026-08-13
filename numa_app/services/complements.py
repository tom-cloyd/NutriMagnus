"""
complements.py — protein-complement display math used by the web backend
(web/backend.py). Originally shared with the interactive terminal CLI (removed
2026-08-04); kept as its own module since AA-gap scoring and two-step combo
pairing benefit from staying separate from the route/template code.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/complements.py — complement display math"
"""
import json

import db as _db
import usda as _usda
from .portions import amount_note as _amount_note

Nutrients = dict[str, float]
Gaps = list[tuple[str, float, float]]  # (aa_key, orig_score, deficit_g) from usda.get_aa_gaps


def exact_dcp(ingredients: list[dict] | None, extra: list[tuple[str, dict | None, float]]) -> float | None:
    """Recompute the real digestible complete protein (g) for `ingredients` plus
    hypothetical `extra` foods, via diaas.meal_level_diaas — the same per-ingredient,
    true-digestibility engine used for the meal/day/recipe's own displayed DCP.

    `ingredients`: the base's real per-food breakdown — list of
        {"food_name", "nutrients_100g", "grams"}. None when the caller has no such
        breakdown (e.g. a single-food base, which needs no recomputation since its
        own DIAAS is already an exact flat digestibility, not a pooled approximation).
    `extra`: (food_name, nutrients_100g, grams) tuples for the food(s) being
        hypothetically added, at the amount to preview.

    Returns None when `ingredients` or `extra` isn't usable — callers should fall
    back to the linear-interpolation approximation (_dcp_at_frac/_total_dig) in
    that case, matching prior behavior for contexts with no ingredient list.
    """
    if not ingredients:
        return None
    extra_ings = [
        {"food_name": name, "nutrients_100g": nuts, "grams": grams}
        for name, nuts, grams in extra
        if nuts and grams and grams > 0
    ]
    if not extra_ings:
        return None
    import diaas as _diaas
    with _db.get_db() as conn:
        result = _diaas.meal_level_diaas(list(ingredients) + extra_ings, conn)
    dcp = result.get("digestible_complete_protein_g")
    return round(dcp, 1) if dcp is not None else None


def load_cache_candidates(exclude_names_lower: set[str] | None = None) -> list[dict]:
    """Search the user's broader food cache (not just pantry) for a real match to
    each entry in the internal curated complement table.

    Used so suggest_complements()'s "general" tier prefers a real cached food
    (with its own fdc_id and, if present, its own real AA data) over the curated
    table's generic literature profile. Always safe: returns [] on any DB error.
    """
    exclude_names_lower = exclude_names_lower or set()
    candidates: list[dict] = []
    seen_fdc_ids: set[int] = set()
    try:
        with _db.get_db() as conn:
            for name in _usda.complement_table_names():
                if name.lower() in exclude_names_lower:
                    continue
                for row in _db.search_cached_foods(conn, name)[:1]:
                    if row["fdc_id"] in seen_fdc_ids:
                        continue
                    seen_fdc_ids.add(row["fdc_id"])
                    nutrients = json.loads(row["nutrients_json"]) if row["nutrients_json"] else None
                    candidates.append({
                        "name":      row["name"],
                        "fdc_id":    row["fdc_id"],
                        "nutrients": nutrients,
                        "diaas":     _usda.get_diaas(row["name"]),
                    })
    except Exception:
        return []
    return candidates


ESTIMATE_NOTE = (
    "These estimates are computed fresh each time from a small built-in reference table "
    "(~20 common foods), scaled to this food's own protein content — they are not saved to "
    "the food and are not the same as the \"estimate amino acids from another food\" tool, "
    "which lets you pick your own comparison food and save it permanently. For any food you "
    "rely on often, consider running that tool instead — it's more accurate and only has to "
    "be done once. See ?comp-estimate for more."
)


AA_LOW_IN: dict[str, str] = {
    "aa_methionine_g":    "grains (rice, wheat, quinoa) and most legumes",
    "aa_lysine_g":        "grains (rice, wheat, corn, oats)",
    "aa_threonine_g":     "wheat and refined grains",
    "aa_leucine_g":       "most plant foods other than soy",
    "aa_isoleucine_g":    "legumes and most plant foods",
    "aa_valine_g":        "most plant foods",
    "aa_tryptophan_g":    "untreated corn-based foods",
    "aa_histidine_g":     "most plant foods",
    "aa_phenylalanine_g": "most plant foods",
}


def aa_effects(s: dict, gaps: Gaps, *, digestibility: float = 1.0, limit: int = 3) -> list[dict]:
    """Before/after AA scores for a single suggestion, against the top `limit` gaps.

    `digestibility` scales the suggestion's raw new_scores onto the same basis
    as `gaps`' orig_scores (which were computed at some fixed digestibility —
    1.0 for meal/daily contexts, the food's own DIAAS for food/recipe contexts).
    Falls back to orig_score when the suggestion has no new_scores entry for an AA.
    """
    effects = []
    new_scores = s.get("new_scores", {})
    for aa, orig_score, _ in gaps[:limit]:
        new_raw = new_scores.get(aa)
        if new_raw is not None and digestibility > 0:
            new_score = new_raw * digestibility
        else:
            new_score = orig_score
        effects.append({
            "label":  _usda.nutrient_label(aa)[0],
            "before": round(orig_score, 2),
            "after":  round(new_score, 2),
            "met":    new_score >= 1.0,
        })
    return effects


def two_step_combo(
    gc: dict,
    base_nutrients: Nutrients,
    *,
    base_protein: float,
    base_digestible: float,
    pantry_candidates: list[dict],
    diet_pref: str,
    gaps: Gaps,
    max_improver_grams: float,
    fallback_digestibility: float = 1.0,
    aa_effects_limit: int = 3,
    ingredients: list[dict] | None = None,
    exclude_names: set[str] | None = None,
) -> dict | None:
    """Pair a gap-closer (Step 1) with the best DIAAS-booster for the resulting
    protein pool (Step 2, if one qualifies). Returns None if `gc` has no cached
    nutrient profile to build a pool from.

    fallback_digestibility: the base food's own digestibility (1.0 for meal/daily
    contexts; the food's actual DIAAS for food/recipe contexts) — used both as the
    default pool digestibility when `gc` has no predicted_diaas, and to scale
    Step 1's aa_effects onto the same basis as `gaps`.
    """
    comp_nutrients = gc.get("comp_nutrients")
    if not comp_nutrients:
        return None

    gc_grams = gc["grams"]
    gc_name = gc.get("name", "")
    gc_raw = float(gc.get("protein_added") or 0)
    gc_diaas = gc.get("predicted_diaas") or fallback_digestibility
    gc_dcp = exact_dcp(ingredients, [(gc_name, comp_nutrients, gc_grams)])
    if gc_dcp is None:
        gc_dcp = round((base_protein + gc_raw) * min(1.0, gc_diaas), 1)

    combined = _usda.sum_nutrients(
        base_nutrients, _usda.scale_nutrients(comp_nutrients, gc_grams)
    )
    sub = _usda.suggest_complements(
        combined, pantry_candidates, diet_pref=diet_pref,
        base_digestibility=gc_diaas, max_improver_grams=max_improver_grams,
        exclude_names=exclude_names,
    )
    qualifying = [
        b for b in sub.get("diaas_improvers", [])
        if b.get("steps") and b["steps"][0]["new_diaas"] > gc_diaas
    ]

    step1 = {
        "name":       gc_name,
        "fdc_id":     gc.get("fdc_id"),
        "estimated":  gc.get("estimated", False),
        "diaas":      round(gc["diaas"], 2) if gc.get("diaas") else None,
        "grams":      gc_grams,
        "amount_note": _amount_note(gc_grams, gc.get("name", "")) if gc_grams else None,
        "aa_effects": aa_effects(gc, gaps, digestibility=fallback_digestibility, limit=aa_effects_limit),
        "dcp_before": round(base_digestible, 1),
        "dcp_after":  gc_dcp,
    }

    step2 = None
    if qualifying:
        b = qualifying[0]
        b_step = b["steps"][0]
        b_dcp = exact_dcp(ingredients, [
            (gc_name, comp_nutrients, gc_grams),
            (b.get("name", ""), b.get("comp_nutrients"), b_step["grams"]),
        ])
        if b_dcp is None:
            b_dcp = b_step.get("dcp")
        step2 = {
            "name":       b.get("name", ""),
            "fdc_id":     b.get("fdc_id"),
            "estimated":  b.get("estimated", False),
            "diaas":      round(b["diaas"], 2) if b.get("diaas") else None,
            "grams":      b_step["grams"],
            "amount_note": _amount_note(b_step["grams"], b.get("name", "")) if b_step.get("grams") else None,
            "new_diaas":  b_step["new_diaas"],
            "dcp_before": gc_dcp,
            "dcp_after":  b_dcp,
            "net_gain":   round(b_dcp - base_digestible, 1) if b_dcp is not None else None,
        }

    return {"step1": step1, "step2": step2, "gc_diaas": gc_diaas}


_GRAD_THRESHOLD = 30  # grams; above this, show a graduated 25/50/75/100% scale


def build_complement_display(
    base_nutrients: Nutrients,
    pantry_candidates: list[dict],
    *,
    diet_pref: str = "all",
    digestibility: float = 1.0,
    base_food_name: str | None = None,
    max_improver_grams: float = 120,
    pantry_limit: int = 3,
    general_limit: int = 6,
    pair_limit: int = 6,
    improver_limit: int = 3,
    two_step_limit: int = 3,
    cache_candidates: list[dict] | None = None,
    ingredients: list[dict] | None = None,
    exclude_names: set[str] | None = None,
    comp_sort: str = "effect",
    diaas_sort: str = "effect",
) -> dict:
    """Build the full complement-suggestion display structure for one base food/meal/recipe.

    `digestibility` is the basis gaps/scores are computed and compared at: 1.0 for
    meal/daily contexts (a pooled DIAAS can't be re-applied as a per-food multiplier),
    or the food's own DIAAS for single-food/recipe contexts. All internal AA-score
    comparisons are done on this same basis — usda.suggest_complements()'s "new_scores"
    are always raw (pre-digestibility) per its docstring, so every comparison against
    `gaps`' digestibility-adjusted orig_scores must first rescale new_scores by
    `digestibility`; skipping that step (as the web backend previously did for
    single-food pages) silently overstates AA "after" scores whenever digestibility < 1.0.

    `ingredients`: the base's real per-food breakdown (list of {"food_name",
    "nutrients_100g", "grams"}), when available — meal/daily/recipe contexts have
    one; a single-food base does not (context="food"). When provided, every
    displayed "DCP achieved"/"total_dig" figure is computed by exact_dcp() — a
    real diaas.meal_level_diaas recompute of ingredients + the candidate at that
    gram amount — instead of the flat-digestibility linear approximation. That
    approximation (still used as a fallback when `ingredients` is absent) can be
    off by 15-20g on a real meal, because it applies one composite ratio to every
    amino acid instead of each ingredient's own true digestibility.

    exclude_names: suggestion names (case-insensitive) the user has flagged to
        ignore — omitted from every tier (pantry, general, pairs, diaas_improvers,
        two_step_combos).

    comp_sort: "effect" (default; most gaps closed, then most digestible protein
        added) or "grams" (smallest serving needed) — controls Pantry/General tier
        order. A full profile-completer is always promoted to the top of its tier
        regardless of mode. two_step_combos inherits this order (Step 1 candidates
        come from the same sorted list).
    diaas_sort: "effect" (default; highest resulting DIAAS first) or "grams"
        (smallest serving first) — controls the diaas_improvers tier order.

    Returns {"no_data": True}, {"no_gaps": True}, or the full display dict consumed
    by the web templates.
    """
    if not base_nutrients or base_nutrients.get("protein_g", 0) <= 0:
        return {"no_data": True}
    try:
        gaps = _usda.get_aa_gaps(base_nutrients, digestibility=digestibility)
    except Exception:
        return {"no_data": True}
    if not gaps:
        return {"no_gaps": True}

    try:
        suggestions = _usda.suggest_complements(
            base_nutrients, pantry_candidates, diet_pref=diet_pref,
            base_digestibility=digestibility,
            base_food_name=base_food_name,
            max_improver_grams=max_improver_grams,
            cache_candidates=cache_candidates,
            exclude_names=exclude_names,
        )
    except Exception:
        return {"no_data": True}

    base_protein = base_nutrients.get("protein_g", 0.0)
    base_digestible = base_protein * digestibility

    def _adj_min(new_scores: dict) -> float:
        """Rescale the raw new_scores' minimum onto the digestibility-adjusted basis."""
        return min(new_scores.values()) * digestibility

    def _total_dig(s: dict) -> float:
        raw = float(s.get("protein_added") or 0)
        dig = float(s.get("digestible_protein_added") or 0)
        new_scores = s.get("new_scores", {})
        if new_scores and gaps:
            old_adj_min = gaps[0][1]
            new_adj_min = _adj_min(new_scores)
            scale = (new_adj_min / old_adj_min) if old_adj_min > 0 else 1.0
            return round((base_protein + raw) * min(1.0, scale), 1)
        return round(base_digestible + dig, 1)

    def _dcp_at_frac(frac: float, raw_full: float, new_scores_full: dict) -> float | None:
        """DCP of the combined pool (base + frac*complement) using the weighted-pool IAA formula."""
        if not gaps or not new_scores_full or raw_full <= 0:
            return None
        total_p = base_protein + frac * raw_full
        if total_p <= 0:
            return None
        min_score = 1.0
        for aa_key, base_score_i, *_ in gaps:
            if aa_key not in new_scores_full:
                continue
            new_adj = new_scores_full[aa_key] * digestibility
            comp_aa = new_adj * (base_protein + raw_full) - base_score_i * base_protein
            score_at_f = (base_score_i * base_protein + frac * comp_aa) / total_p
            min_score = min(min_score, score_at_f)
        return round(total_p * min(1.0, min_score), 1)

    def _grad_steps(full_grams: float | None, dig_full: float, food_name: str,
                    raw_full: float = 0.0, new_scores_full: dict | None = None,
                    comp_nutrients: dict | None = None) -> list[dict]:
        if not full_grams or full_grams <= _GRAD_THRESHOLD:
            return []
        seen: set[int] = set()
        steps = []
        for frac in (0.25, 0.50, 0.75, 1.0):
            g = max(1, round(full_grams * frac))
            if g not in seen:
                seen.add(g)
                dcp = exact_dcp(ingredients, [(food_name, comp_nutrients, g)])
                if dcp is None:
                    dcp = _dcp_at_frac(frac, raw_full, new_scores_full or {})
                pct_increase = (round((dcp - base_digestible) / base_digestible * 100, 1)
                                if dcp is not None and base_digestible > 0 else None)
                steps.append({
                    "grams": g, "amount_note": _amount_note(g, food_name),
                    "dig_protein": round(dig_full * frac, 1), "dcp": dcp,
                    "pct_increase": pct_increase,
                })
        return steps

    def _fmt(s: dict) -> dict:
        raw = float(s.get("protein_added") or 0)
        dig = float(s.get("digestible_protein_added") or 0)
        full_grams = s.get("grams")
        name = s.get("name", "")
        new_scores = s.get("new_scores", {})
        comp_nutrients = s.get("comp_nutrients")
        total_dig = exact_dcp(ingredients, [(name, comp_nutrients, full_grams)]) if full_grams else None
        if total_dig is None:
            total_dig = _total_dig(s)
        return {
            "name":              name,
            "grams":             full_grams,
            "amount_note":       _amount_note(full_grams, name) if full_grams else None,
            "grad_steps":        _grad_steps(full_grams, dig, name, raw_full=raw, new_scores_full=new_scores,
                                              comp_nutrients=comp_nutrients),
            "fdc_id":            s.get("fdc_id"),
            "recipe_id":         s.get("recipe_id"),
            "serving_weight_g":  s.get("serving_weight_g"),
            "diaas":             round(s["diaas"], 2) if s.get("diaas") else None,
            "new_complete":      s.get("new_complete", False),
            "dig_protein_added": round(dig, 1),
            "protein_added":     round(raw, 1),
            "opens_new_gap":     s.get("opens_new_gap", False),
            "aa_effects":        aa_effects(s, gaps, digestibility=digestibility),
            "total_dig":         total_dig,
            "estimated":         s.get("estimated", False),
        }

    def _fmt_improver(s: dict) -> dict:
        raw = float(s.get("protein_added") or 0)
        dig = float(s.get("digestible_protein_added") or 0)
        new_diaas = s.get("new_diaas") or 0.0
        grams = s.get("grams")
        name = s.get("name", "")
        comp_nutrients = s.get("comp_nutrients")
        total_dig = exact_dcp(ingredients, [(name, comp_nutrients, grams)]) if grams else None
        if total_dig is None:
            total_dig = (round((base_protein + raw) * min(1.0, new_diaas), 1) if new_diaas
                         else round(base_digestible + dig, 1))
        steps_out = []
        for step in s.get("steps", []):
            step_dcp = exact_dcp(ingredients, [(name, comp_nutrients, step.get("grams"))])
            steps_out.append({
                **step,
                "amount_note": _amount_note(step["grams"], name) if step.get("grams") else None,
                "dcp": step_dcp if step_dcp is not None else step.get("dcp"),
            })
        return {
            "name":              name,
            "grams":             grams,
            "amount_note":       _amount_note(grams, name) if grams else None,
            "fdc_id":            s.get("fdc_id"),
            "recipe_id":         s.get("recipe_id"),
            "serving_weight_g":  s.get("serving_weight_g"),
            "diaas":             round(s["diaas"], 2) if s.get("diaas") else None,
            "current_diaas":     s.get("current_diaas"),
            "new_diaas":         s.get("new_diaas"),
            "steps":             steps_out,
            "dig_protein_added": round(dig, 1),
            "protein_added":     round(raw, 1),
            "total_dig":         total_dig,
            "estimated":         s.get("estimated", False),
        }

    def _fmt_pair(p: dict) -> dict:
        foods_out = [
            {
                "name":          f.get("name", ""),
                "fdc_id":        f.get("fdc_id"),
                "recipe_id":     f.get("recipe_id"),
                "diaas":         round(f["diaas"], 2) if f.get("diaas") else None,
                "grams":         f.get("grams"),
                "amount_note":   _amount_note(f["grams"], f.get("name", "")) if f.get("grams") else None,
                "protein_added": f.get("protein_added", 0),
                "dig_added":     f.get("dig_added", 0),
            }
            for f in p.get("foods", [])
        ]
        new_scores = p.get("new_scores", {})
        total_raw  = base_protein + float(p.get("total_protein_added") or 0)
        pair_extra = [
            (f.get("name", ""), f.get("comp_nutrients"), f.get("grams"))
            for f in p.get("foods", [])
        ]
        total_dig_complete = exact_dcp(ingredients, pair_extra)
        if total_dig_complete is None:
            if new_scores and gaps:
                old_adj_min = gaps[0][1]
                new_adj_min = _adj_min(new_scores)
                scale = (new_adj_min / old_adj_min) if old_adj_min > 0 else 1.0
                total_dig_complete = round(total_raw * min(1.0, scale), 1)
            else:
                total_dig_complete = round(base_digestible + float(p.get("total_dig_added") or 0), 1)
        return {
            "foods":               foods_out,
            "total_grams":         p.get("total_grams"),
            "gaps_closed":         p.get("gaps_closed", False),
            "new_complete":        p.get("new_complete", False),
            "total_protein_added": p.get("total_protein_added", 0),
            "total_dig_added":     p.get("total_dig_added", 0),
            "total_dig_complete":  total_dig_complete,
            "aa_effects":          aa_effects({"new_scores": new_scores}, gaps, digestibility=digestibility),
        }

    if comp_sort == "grams":
        sort_key = lambda s: (0 if s.get("new_complete") else 1, float(s.get("grams") or 999))
    else:
        sort_key = lambda s: (0 if s.get("new_complete") else 1,
                               -(s.get("gaps_closed") or 0),
                               -(s.get("digestible_protein_added") or 0))
    pantry_suggs    = sorted(suggestions.get("pantry",  []), key=sort_key)[:pantry_limit]
    general_suggs   = sorted(suggestions.get("general", []), key=sort_key)[:general_limit]
    pair_suggs      = suggestions.get("pairs", [])[:pair_limit]

    if diaas_sort == "grams":
        diaas_sort_key = lambda s: (float(s.get("grams") or 999), -(s.get("new_diaas") or 0))
    else:
        diaas_sort_key = lambda s: (-(s.get("new_diaas") or 0), float(s.get("grams") or 999))
    diaas_improvers = sorted(suggestions.get("diaas_improvers", []), key=diaas_sort_key)[:improver_limit]

    two_step_combos: list[dict] = []
    top_gap_closers = (pantry_suggs + general_suggs)[:two_step_limit]
    if top_gap_closers and diaas_improvers:
        for gc in top_gap_closers:
            combo = two_step_combo(
                gc, base_nutrients,
                base_protein=base_protein, base_digestible=base_digestible,
                pantry_candidates=pantry_candidates, diet_pref=diet_pref,
                gaps=gaps, max_improver_grams=max_improver_grams,
                fallback_digestibility=digestibility,
                ingredients=ingredients,
                exclude_names=exclude_names,
            )
            if combo is not None:
                two_step_combos.append(combo)

    pantry_fmt = [_fmt(s) for s in pantry_suggs]
    general_fmt = [_fmt(s) for s in general_suggs]
    improvers_fmt = [_fmt_improver(s) for s in diaas_improvers]

    def _is_generic(row: dict) -> bool:
        return not row.get("fdc_id") and not row.get("recipe_id")

    has_estimate_or_generic = any(
        row.get("estimated") or _is_generic(row)
        for row in pantry_fmt + general_fmt + improvers_fmt
    )

    gap_rows = [{"label": _usda.nutrient_label(k)[0], "score": round(v, 3)} for k, v, _ in gaps[:4]]
    limiting_aa = gaps[0][0] if gaps else None
    limiting_label = _usda.nutrient_label(limiting_aa)[0] if limiting_aa else "this amino acid"
    low_in = AA_LOW_IN.get(limiting_aa or "", "many plant foods")
    n_shown = len(pantry_suggs) + len(general_suggs)
    exhausted_prefix = ("All options that qualify are shown above — no others meet the criteria."
                        if n_shown > 0 else "No qualifying options found in the database.")

    if comp_sort == "grams":
        comp_ranking_note = ("Ranked by smallest addition: fewest grams needed. Exception: an option "
                              "that fully completes the amino acid profile is always promoted to the top.")
    else:
        comp_ranking_note = ("Ranked by greatest effect: most amino-acid gaps closed, then most digestible "
                              "protein added. Exception: an option that fully completes the amino acid "
                              "profile is always promoted to the top.")
    if diaas_sort == "grams":
        diaas_ranking_note = "Ranked by smallest addition: fewest grams needed."
    else:
        diaas_ranking_note = "Ranked by greatest effect: highest resulting DIAAS score first."
    pairs_ranking_note = ("Ranked by smallest combined addition (both foods' grams added together). "
                          "A combination that fully closes every gap in 50 g total or less is promoted to the top.")
    two_step_ranking_note = ("Step 1 options follow the same order as Protein Complement Suggestions above; "
                             "Step 2 is the best-available DIAAS booster for the resulting protein pool.")

    return {
        "no_gaps":              False,
        "gaps":                 gap_rows,
        "comp_ranking_note":    comp_ranking_note,
        "diaas_ranking_note":   diaas_ranking_note,
        "pairs_ranking_note":   pairs_ranking_note,
        "two_step_ranking_note": two_step_ranking_note,
        "comp_sort":            comp_sort,
        "diaas_sort":           diaas_sort,
        "pantry_empty":      not pantry_candidates,
        "pantry_no_qualify": bool(pantry_candidates) and not pantry_suggs,
        "pantry":            pantry_fmt,
        "general":           general_fmt,
        "pairs":             [_fmt_pair(p) for p in pair_suggs],
        "diaas_improvers":   improvers_fmt,
        "two_step_combos":   two_step_combos,
        "have_gap_closers":  bool(pantry_suggs or general_suggs),
        "has_estimate_or_generic": has_estimate_or_generic,
        "estimate_note": ESTIMATE_NOTE if has_estimate_or_generic else None,
        "exhausted_msg": (
            f"{exhausted_prefix} A qualifying complement must have a {limiting_label}/protein ratio "
            f"above the FAO reference to close the gap to score 1.0 in a practical serving (≤ 500 g). "
            f"Score 1.0 = meets human requirements (the floor, not an aspirational target). "
            f"Foods that don't qualify for a {limiting_label} gap: {low_in}. "
            f"Their ratio falls below the reference — adding them dilutes the score further."
        ),
    }
