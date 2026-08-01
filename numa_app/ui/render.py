"""
render.py — terminal output rendering: nutrient tables, protein completeness, bioavailability, RDA comparison.
Docs: README-numa-documentation.md, Architecture: "numa_app/ui/render.py — output rendering"
"""
import json
import textwrap

from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich.padding import Padding
from rich.console import Group
from rich.text import Text

import db as _db
import diaas as _diaas
import usda as _usda
import profile as _profile
from .. import state
from ..services import complements as _complements
from ..services.portions import amount_note as _amount_note
from ..services.portions import volume_hint as _volume_hint
from ..services.rda_status import rda_status, limit_warning
from ..services.diet_aware import b12_deficiency_note, iron_zinc_bioavailability_note
from ..ui.common import _id_cell, ID_KEY, dot_cell, table_title, section_title, table_footer, help_footer, food_id_tag
from ..ui.prompts import Cancelled, ReturnToMain, _prompt


# FAO 2013 scores Met+Cys and Phe+Tyr as combined pairs; use these labels
# wherever amino acid completeness scores are displayed.
_AA_PAIR_LABELS: dict[str, str] = {
    "aa_methionine_g":    "Met+Cys",
    "aa_phenylalanine_g": "Phe+Tyr",
}


def _aa_label(aa_key: str) -> str:
    """Return display label for an AA key, using combined form for paired AAs."""
    return _AA_PAIR_LABELS.get(aa_key) or _usda.nutrient_label(aa_key)[0]


def _load_pantry_candidates() -> list[dict]:
    """Return pantry foods usable for complement suggestions.

    Always safe: returns [] if pantry data is unavailable.
    """
    try:
        with _db.get_db() as conn:
            rows = _db.pantry_list(conn)
    except Exception:
        return []

    candidates: list[dict] = []
    for row in rows:
        nutrients = None
        fdc_id = row["fdc_id"]
        food_name = row["food_name"] or ""
        try:
            if fdc_id is not None:
                with _db.get_db() as conn:
                    cached = _db.get_cached_food(conn, fdc_id)
                if cached and cached["nutrients_json"]:
                    nutrients = json.loads(cached["nutrients_json"])
        except Exception:
            nutrients = None
        candidates.append({
            "name": food_name,
            "fdc_id": fdc_id,
            "nutrients": nutrients,
            "diaas": _usda.get_diaas(food_name),
        })
    return candidates

def _load_recipe_candidates() -> list[dict]:
    """Return recipes with cached per-100g nutrients usable for complement suggestions.

    Always safe: returns [] if recipe data is unavailable.
    """
    try:
        with _db.get_db() as conn:
            rows = conn.execute(
                "SELECT id, name, servings, dcp_g, total_weight, total_weight_unit, nutrients_json"
                " FROM recipes WHERE nutrients_json IS NOT NULL"
            ).fetchall()
    except Exception:
        return []

    candidates: list[dict] = []
    for row in rows:
        try:
            nutrients = json.loads(row["nutrients_json"])
        except Exception:
            continue
        if not nutrients:
            continue

        # Compute serving weight in grams for the servings hint
        servings = row["servings"] or 1
        try:
            total_weight = float(row["total_weight"]) if row["total_weight"] else None
        except Exception:
            total_weight = None
        serving_weight_g = (total_weight / servings) if total_weight else None

        # Derive effective DIAAS from stored dcp_g / protein_per_serving
        diaas_val: float | None = None
        dcp_g = row["dcp_g"]
        if dcp_g and serving_weight_g and nutrients.get("protein_g", 0) > 0:
            protein_per_serving = nutrients["protein_g"] * serving_weight_g / 100
            if protein_per_serving > 0:
                diaas_val = min(1.0, dcp_g / protein_per_serving)

        candidates.append({
            "name": row["name"],
            "fdc_id": None,
            "recipe_id": row["id"],
            "nutrients": nutrients,
            "diaas": diaas_val,
            "serving_weight_g": serving_weight_g,
        })
    return candidates


def _get_daily_context(
    meal_date: "str | None" = None,
) -> "tuple[dict[str, float] | None, dict | None, dict | None, dict | None]":
    """Return (daily_nutrients, rda, optimal, max_limits) for today;
    (None, None, None, None) if no user profile.

    daily_nutrients is {} when a profile exists but no meals are logged today.
    Uses a lazy import from meals.py to avoid a circular import at module load time.
    """
    from datetime import date as _date
    profile = _profile.load_profile()
    if not profile:
        return None, None, None, None
    rda = _profile.compute_rda(profile, diet_pref=state._diet_pref)
    optimal = _profile.compute_optimal(profile)
    max_limits = _profile.get_max_limits(profile)
    today = meal_date or _date.today().isoformat()
    with _db.get_db() as conn:
        today_meals = _db.meal_list_by_date(conn, today)
    if not today_meals:
        return {}, rda, optimal, max_limits
    from ..workflows.meals import _compute_meal_nutrients
    daily_parts = [n for m in today_meals if (n := _compute_meal_nutrients(m["id"]))]
    daily_nutrients = _usda.sum_nutrients(*daily_parts) if daily_parts else {}
    return daily_nutrients, rda, optimal, max_limits


def _print_nutrient_table(
    nutrients: dict[str, float],
    title: str = "Nutrients",
    per_label: str = "",
    *,
    daily_nutrients: "dict[str, float] | None" = None,
    rda: "dict | None" = None,
    optimal: "dict | None" = None,
    max_limits: "dict[str, float] | None" = None,
    show_meal_pct: bool = True,
    fdc_id: int | None = None,
    recipe_id: int | None = None,
) -> None:
    """Render a rich table of nutrients grouped by category.

    daily_nutrients + rda: when both provided, adds % columns and Daily goal.
    optimal: when non-empty, adds a second "Profile Optimal" triplet of columns
        (meal %, day total %, goal) alongside the RDA triplet, for nutrients the
        user has configured a custom optimal target for (see profile.compute_optimal).
        Nutrients without a configured optimal show "–" in those columns.
    max_limits: nutrient_key -> user-defined per-day cap (profile.get_max_limits).
        When the day total is within 10% of (or over) a configured limit, that
        nutrient's label and amount are colored as a warning/error.
    show_meal_pct=False: suppress the 'meal %' column (use when nutrients IS the day total).
    """
    groups = [
        ("Macronutrients", [
            "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
            "saturated_fat_g", "mono_fat_g", "poly_fat_g",
            "omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg",
        ]),
        ("Minerals", [
            "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
            "potassium_mg", "sodium_mg", "zinc_mg", "iodine_mcg", "selenium_mcg",
        ]),
        ("Vitamins", [
            "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
            "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
            "b6_mg", "folate_mcg", "b12_mcg",
        ]),
        ("Phytonutrients", [
            "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
            "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg",
            "isoflavones_mg",
        ]),
    ]

    sub = f"({per_label})" if per_label else ""
    section_title(title + food_id_tag(fdc_id, recipe_id), sub)

    show_pct = daily_nutrients is not None and rda is not None
    show_optimal = show_pct and bool(optimal)
    max_limits = max_limits or {}

    def _rda_color(pct: float, rda_type: str) -> str:
        if rda_type == "limit":
            return state.T["success"] if pct <= 80 else (state.T["warning"] if pct <= 100 else state.T["error"])
        return state.T["success"] if pct >= 100 else (state.T["warning"] if pct >= 70 else state.T["error"])

    def _limit_color(key: str) -> "str | None":
        limit = max_limits.get(key)
        if not limit or daily_nutrients is None:
            return None
        day_total = daily_nutrients.get(key, 0.0)
        if not limit_warning(day_total, limit):
            return None
        return state.T["error"] if day_total >= limit else state.T["warning"]

    _NUT_W = 28
    _AMT_W, _UNIT_W = 10, 8
    _MEAL_W, _DAY_W, _GOAL_W = 8, 11, 14

    # Meta-header labeling the RDA vs. Optimal column groups (Rich Table has no
    # native spanning header, so this is a manually-aligned line printed above it).
    if show_optimal:
        base_w = (_NUT_W + 2) + (_AMT_W + 2) + (_UNIT_W + 2)
        grp_w = ((_MEAL_W + 2) if show_meal_pct else 0) + (_DAY_W + 2) + (_GOAL_W + 2)
        meta = (" " * base_w
                + "Profile RDA".center(grp_w)
                + "Profile Optimal".center(grp_w))
        state.console.print(f"[{state.T['hi']}]{meta}[/{state.T['hi']}]", highlight=False)

    tbl = Table(show_header=True, header_style=state.T["accent"], box=None, padding=(0, 1))
    tbl.add_column("Nutrient", style="", min_width=_NUT_W, max_width=_NUT_W, no_wrap=True)
    tbl.add_column("Amount", justify="right", min_width=_AMT_W)
    tbl.add_column("Unit", style="dim", min_width=_UNIT_W)
    if show_pct:
        if show_meal_pct:
            tbl.add_column("meal %", justify="right", min_width=_MEAL_W, max_width=_MEAL_W)
        tbl.add_column("day total %", justify="right", min_width=_DAY_W, max_width=_DAY_W)
        tbl.add_column("Daily goal", justify="right", min_width=_GOAL_W, max_width=_GOAL_W)
        if show_optimal:
            if show_meal_pct:
                tbl.add_column("meal %", justify="right", min_width=_MEAL_W, max_width=_MEAL_W)
            tbl.add_column("day total %", justify="right", min_width=_DAY_W, max_width=_DAY_W)
            tbl.add_column("Optimal goal", justify="right", min_width=_GOAL_W, max_width=_GOAL_W)

    triplet_w = (1 if show_meal_pct else 0) + 2  # columns per pct triplet

    for group_name, keys in groups:
        present = [(k, nutrients[k]) for k in keys if k in nutrients]
        if not present:
            continue
        extra_blanks = triplet_w * (2 if show_optimal else 1)
        header_row = [f"[{state.T['hi']}]{group_name}[/{state.T['hi']}]", "", ""]
        tbl.add_row(*(header_row + ([""] * extra_blanks if show_pct else [])))
        for key, val in present:
            label, unit = _usda.nutrient_label(key)
            limit_color = _limit_color(key)
            visible = f"  {label}"
            dots = "·" * max(0, _NUT_W - len(visible) - 1)
            name_cell = f"{visible} [grey62]{dots}[/grey62]"
            amt_cell = f"{val:.2f}"
            if limit_color:
                name_cell = f"[{limit_color}]{visible}[/{limit_color}] [grey62]{dots}[/grey62]"
                amt_cell = f"[{limit_color}]{val:.2f}[/{limit_color}]"
            if not show_pct:
                tbl.add_row(name_cell, amt_cell, unit)
                continue

            row = [name_cell, amt_cell, unit]

            def _pct_cells(entry, val=val) -> list[str]:
                if not (entry and entry[0] > 0):
                    return [""] * triplet_w
                t_val, t_unit, t_type = entry
                day_pct = daily_nutrients.get(key, 0.0) / t_val * 100.0
                cells = []
                if show_meal_pct:
                    meal_pct = val / t_val * 100.0
                    cells.append(f"[{_rda_color(meal_pct, t_type)}]{meal_pct:.0f}%[/]")
                cells.append(f"[{_rda_color(day_pct, t_type)}]{day_pct:.0f}%[/]")
                cells.append(f"[grey62]{t_val:.1f} {t_unit}[/grey62]")
                return cells

            row.extend(_pct_cells(rda.get(key) if rda else None))
            if show_optimal:
                opt_entry = optimal.get(key) if optimal else None
                if opt_entry:
                    row.extend(_pct_cells(opt_entry))
                else:
                    row.extend(["–"] * triplet_w)
            tbl.add_row(*row)

    state.console.print(tbl)
    if show_pct:
        state.console.print()
        if show_meal_pct:
            state.console.print("  [grey62]meal % = this meal ÷ daily goal[/grey62]")
        state.console.print("  [grey62]day total % = all meals logged today ÷ daily goal[/grey62]")
        if show_optimal:
            state.console.print("  [grey62]Profile Optimal = your custom target, where configured (\"–\" = not set, uses RDA only)[/grey62]")
            help_footer("optimal")
        if max_limits:
            state.console.print(
                f"  [grey62]Highlighted nutrient in [/grey62][{state.T['warning']}]yellow[/{state.T['warning']}]"
                f"[grey62] = day total within 10% of its max limit (your custom setting, or a built-in safe upper limit"
                f" where you haven't set one); in [/grey62][{state.T['error']}]red[/{state.T['error']}]"
                f"[grey62] = at/over it[/grey62]"
            )
            help_footer("maxlimits")
    if any(k in nutrients for k in
           ("omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg")):
        help_footer("omega3")
    help_footer("nutrients")


def _print_protein_completeness(
    nutrients: dict[str, float],
    *,
    food_name: str | None = None,
    context_label: str | None = None,
    partial_data_note: str | None = None,
) -> bool:
    """Print protein completeness assessment if amino acid data is available.
    Returns True if amino acid data was present, False otherwise.

    food_name: when provided, DIAAS is looked up and applied so that
        complete/incomplete classification reflects bioavailable amino acids.
    """
    digestibility = (_usda.get_diaas(food_name) or 1.0) if food_name else 1.0
    result = _usda.protein_completeness(nutrients, digestibility=digestibility)
    if not result["has_data"]:
        state.console.print("[grey62]  (No amino acid data available for protein completeness analysis.)[/grey62]")
        return False

    if context_label:
        table_title(f"PROTEIN QUALITY — {context_label}")
    status = (f"[{state.T['success']}]Complete protein — no complement needed[/{state.T['success']}]"
              if result["complete"]
              else f"[{state.T['warning']}]Incomplete protein[/{state.T['warning']}]")
    state.console.print()
    state.console.print(f"  Protein Quality: {status}")
    state.console.print(
        "  [grey62]Ratios below compare this protein's amino acid pattern per gram of protein[/grey62]",
        highlight=False,
    )
    state.console.print(
        "  [grey62]against the FAO adult reference pattern (a fixed quality standard, not a personalized target).[/grey62]",
        highlight=False,
    )

    if not result["complete"] and result["limiting_aa"]:
        state.console.print(f"  Most limiting amino acid: [{state.T['warning']}]{_aa_label(result['limiting_aa'])}[/{state.T['warning']}]")

    _AA_W = 22
    show_adj = digestibility < 1.0
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Amino Acid", min_width=_AA_W, max_width=_AA_W, no_wrap=True)
    tbl.add_column("Raw ratio", justify="right", min_width=5)
    if show_adj:
        tbl.add_column(f"Adj. ({digestibility:.2f})", justify="right", min_width=5)
    tbl.add_column("", justify="left", min_width=10, no_wrap=True)
    for aa_key, score in result["scores"].items():
        label = _aa_label(aa_key)
        adj_score = score * digestibility if show_adj else score
        bar = "█" * min(int(adj_score * 10), 20)
        raw_color = state.T["success"] if score >= 1.0 else state.T["warning"]
        adj_color = state.T["success"] if adj_score >= 1.0 else state.T["warning"]
        row = [dot_cell(label, _AA_W), f"[{raw_color}]{score:.2f}[/{raw_color}]"]
        if show_adj:
            row.append(f"[{adj_color}]{adj_score:.2f}[/{adj_color}]")
        row.append(f"[{adj_color}]{bar}[/{adj_color}]")
        tbl.add_row(*row)
    state.console.print()
    state.console.print(tbl)
    footer = [
        "  [grey62]Interpretation: 1.0 = meets the FAO pattern · >1.0 = exceeds it · <1.0 = limiting[/grey62]",
        "  [grey62]Met+Cys and Phe+Tyr are combined per FAO 2013 where data is available[/grey62]",
    ]
    if show_adj:
        footer.append(
            f"  [grey62]Adj. = raw ratio × DIAAS ({digestibility:.2f}); bar and completeness "
            f"classification use the adjusted value[/grey62]"
        )
    if partial_data_note:
        footer.append(f"  [grey62]{partial_data_note}[/grey62]")
    table_footer(*footer)
    help_footer("protein-quality")
    return True


def _print_protein_adequacy(
    nutrients: dict[str, float],
    profile: "_profile.UserProfile",
    *,
    context_label: str | None = None,
    dcp_g: float | None = None,
    dcp_total_g: float | None = None,
    servings: float | None = None,
) -> None:
    """Print personalized protein adequacy vs. the user's profile-derived target.

    dcp_g: when provided (from DIAAS analysis), used as the effective protein intake
           figure instead of the raw total protein from nutrients.
    dcp_total_g/servings: when the recipe has more than one serving, also print the
    whole-recipe DCP total alongside the per-serving figure.
    """
    if profile is None:
        return
    protein_target = _profile.compute_rda(profile).get("protein_g", (0.0, "g", "minimum"))[0]
    if protein_target <= 0:
        return

    if dcp_g is not None:
        protein_intake = dcp_g
        intake_label = "Digestible complete protein"
    else:
        protein_intake = nutrients.get("protein_g", 0.0)
        intake_label = "Protein here"
    pct = (protein_intake / protein_target * 100.0) if protein_target > 0 else 0.0
    title = f"Personalized protein adequacy — {context_label}" if context_label else "Personalized protein adequacy"
    section_title(title)
    state.console.print(
        f"  [grey62]Profile-adjusted protein target: {protein_target:.1f} g/day"
        f"  ({_profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level)})[/grey62]",
        highlight=False,
    )
    color = state.T["success"] if pct >= 100 else (state.T["warning"] if pct >= 50 else state.T["error"])
    state.console.print(
        f"  {intake_label}: [{color}]{protein_intake:.1f} g[/{color}]  [grey62]({pct:.0f}% of daily target)[/grey62]",
        highlight=False,
    )
    if dcp_g is not None and servings is not None and servings > 1 and dcp_total_g is not None:
        state.console.print(
            f"  [grey62]Per serving: [{color}]{dcp_g:.1f}g[/{color}]"
            f"   ·   Whole recipe ({servings:g} servings): [{color}]{dcp_total_g:.1f}g[/{color}][/grey62]",
            highlight=False,
        )


def _print_meal_diaas(
    ingredient_list: list[dict],
    profile: "_profile.UserProfile | None" = None,
    title: str = "Meal-Level Complete Protein Analysis",
) -> tuple[list[str], float | None]:
    """
    Print meal-level DIAAS analysis for a list of ingredients.

    Each dict in ingredient_list must have:
        "food_name":      str
        "nutrients_100g": dict[str, float]
        "grams":          float

    profile: when provided, prints a compact adequacy line right after the DCP line.

    Returns (missing_aa_names, dcp_g, diaas):
        missing_aa_names: food names excluded due to missing AA data; empty = analysis complete.
        dcp_g: digestible complete protein in grams, or None if DIAAS analysis unavailable.
        diaas: meal DIAAS (capped at 1.0), or None if unavailable. Pass as base_diaas to
               _print_complement_suggestions so its DCP projections use the correct baseline.
    """
    if not ingredient_list:
        return [], None, None

    with _db.get_db() as conn:
        result = _diaas.meal_level_diaas(ingredient_list, conn)

    if result["diaas"] is None:
        if not result["missing_aa_names"]:
            state.console.print(
                "\n  [grey62](No amino acid data available for meal-level DIAAS analysis.)[/grey62]"
            )
        else:
            state.console.print(
                "\n  [grey62](Meal-level DIAAS analysis unavailable — "
                "no amino acid data for any ingredient.)[/grey62]"
            )
        return result["missing_aa_names"], None, None

    section_title(title,
                  "pooled across foods, digestibility-corrected (DIAAS)")

    # Per-food digestibility table
    table_title("MEAL FOODS: PROTEIN DIGESTIBILITY ANALYSIS")
    state.console.print(
        f"  [grey62]Digestibility color key:[/grey62]  "
        f"[{state.T['success']}]≥0.90 good[/{state.T['success']}]  "
        f"[{state.T['warning']}]0.80–0.89 fair[/{state.T['warning']}]  "
        f"[{state.T['error']}]<0.80 poor[/{state.T['error']}]  ·  {ID_KEY}  ·  [grey62]zero-protein foods omitted[/grey62]",
        highlight=False,
    )
    _FOOD_COL_W = 48
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID",        justify="right", min_width=7)
    tbl.add_column("Food",      min_width=_FOOD_COL_W, max_width=_FOOD_COL_W, no_wrap=True)
    tbl.add_column("Food tot. gr.", justify="right", min_width=12)
    tbl.add_column("Protein",         justify="right", min_width=8)
    tbl.add_column("Digestibility",   justify="right", min_width=14)
    tbl.add_column("Digestible prot", justify="right", min_width=15)
    tbl.add_column("AA",              justify="center", min_width=3)

    total_grams = 0.0
    total_protein = 0.0
    total_dig_p = 0.0
    for ing in sorted((i for i in result["ingredients"] if i["protein_g"] >= 1.0), key=lambda x: x["food_name"].lower()):
        p = ing["protein_g"]
        d = ing["digestibility"]
        dig_p = p * d  # digestibility applies regardless of whether AA data is present
        total_grams   += ing["grams"]
        total_protein += p
        total_dig_p   += dig_p
        source_tag = ""
        src = ing["dig_source"]
        if "user override" in src:
            source_tag = f"  [grey62]↑ user[/grey62]"
        elif "category estimate" in src or "default estimate" in src:
            source_tag = f"  [grey62]~est[/grey62]"
        color = state.T["success"] if d >= 0.90 else (state.T["warning"] if d >= 0.80 else state.T["error"])
        aa_cell = (f"[{state.T['success']}]✓[/{state.T['success']}]"
                   if ing["has_aa_data"]
                   else f"[{state.T['error']}]✗[/{state.T['error']}]")
        food_cell = dot_cell(ing['food_name'], _FOOD_COL_W)
        tbl.add_row(
            _id_cell(ing.get("fdc_id")),
            food_cell,
            f"{ing['grams']:.1f}g",
            f"{p:.1f}g",
            f"[{color}]{d:.2f}[/{color}]{source_tag}",
            f"{dig_p:.1f}g",
            aa_cell,
        )
    state.console.print()
    state.console.print(tbl, highlight=False)

    # Totals row: dim rule + aligned totals table
    state.console.print(Rule(style="grey62 dim"), highlight=False)
    totals_tbl = Table(show_header=False, box=None, padding=(0, 1))
    totals_tbl.add_column(justify="right", min_width=7)
    totals_tbl.add_column(min_width=_FOOD_COL_W, max_width=_FOOD_COL_W, no_wrap=True)
    totals_tbl.add_column(justify="right", min_width=12)
    totals_tbl.add_column(justify="right", min_width=8)
    totals_tbl.add_column(justify="right", min_width=14)
    totals_tbl.add_column(justify="right", min_width=15)
    totals_tbl.add_column(justify="center", min_width=3)
    totals_tbl.add_row(
        "", "[grey62]TOTAL[/grey62]",
        f"[grey62]{total_grams:.1f}g[/grey62]",
        f"[grey62]{total_protein:.1f}g[/grey62]",
        "",
        f"[grey62]{total_dig_p:.1f}g[/grey62]",
        "",
    )
    state.console.print(Padding(totals_tbl, (0, 0, 0, 1)), highlight=False)

    state.console.print()
    state.console.print(
        f"  [grey62]Total digestible protein of [bold]{total_dig_p:.1f}g[/bold]"
        f" = per-food protein × digestibility, before limiting-amino-acid scoring[/grey62]",
        highlight=False,
    )

    # IAA composite ratio table
    iaa_ratios = result["iaa_ratios"]
    if iaa_ratios:
        iaa_key = (
            f"[grey62](digestible AA supply ÷ FAO reference  |  DIAAS = lowest ratio  |  color:[/grey62]"
            f"  [{state.T['success']}]≥1.0[/{state.T['success']}]"
            f"  [{state.T['warning']}]0.80–0.99[/{state.T['warning']}]"
            f"  [{state.T['error']}]<0.80[/{state.T['error']}]"
            f"[grey62])[/grey62]"
        )
        table_title("MEAL AMINO ACID RATIOS", iaa_key)
        _MAA_W = 22
        aa_tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        aa_tbl.add_column("Amino Acid", min_width=_MAA_W, max_width=_MAA_W, no_wrap=True)
        aa_tbl.add_column("Ratio",      justify="right", min_width=7)
        aa_tbl.add_column("",           min_width=22)

        for aa_key in _diaas.FAO_REFERENCE:
            if aa_key not in iaa_ratios:
                continue
            ratio = iaa_ratios[aa_key]
            label = _diaas.IAA_LABELS[aa_key]
            is_limiting = (aa_key == result["limiting_iaa"])
            bar_len = min(int(ratio * 10), 20)
            bar = "█" * bar_len
            if ratio >= 1.0:
                color = state.T["success"]
            elif ratio >= 0.80:
                color = state.T["warning"]
            else:
                color = state.T["error"]
            limiting_tag = f"  [grey62]← LIMITING[/grey62]" if is_limiting else ""
            aa_tbl.add_row(
                dot_cell(label, _MAA_W),
                f"[{color}]{ratio:.3f}[/{color}]{limiting_tag}",
                f"[{color}]{bar}[/{color}]",
            )

        if result["phe_tyr_gap"]:
            aa_tbl.add_row(f"[grey62]{dot_cell('Phe+Tyr', _MAA_W)}[/grey62]", "[grey62]n/a[/grey62]",
                           "[grey62](tyrosine absent from USDA data)[/grey62]")
        state.console.print(aa_tbl, highlight=False)

    # DCP + adequacy — same detailed section as recipe analysis
    total_p = result["total_protein_g"]
    _print_dcp_adequacy_section(result, {"protein_g": total_p}, profile)

    protein_by_name = {
        ing["food_name"]: ing.get("protein_g", 0.0)
        for ing in result.get("ingredients", [])
    }

    if result["missing_aa_names"]:
        with_protein = [n for n in result["missing_aa_names"] if protein_by_name.get(n, 0.0) >= 1.0]
        if with_protein:
            n_missing = len(with_protein)
            state.console.print(
                f"\n  [{state.T['warning']}]⚠  DIAAS figure above may be unreliable.[/{state.T['warning']}] "
                f"{n_missing} ingredient{'s' if n_missing != 1 else ''} with protein have no amino acid profile\n"
                f"  in the USDA database and were excluded from the calculation:",
                highlight=False,
            )
            for name in with_protein:
                protein = protein_by_name[name]
                state.console.print(f"    • {name}  [grey62]({protein:.1f}g protein)[/grey62]")
            food_word = "this food" if n_missing == 1 else "any of these foods"
            state.console.print(
                f"  [grey62]This is a problem only if significant protein exists in {food_word}.[/grey62]",
                highlight=False,
            )
            if len(result["missing_aa_names"]) > n_missing:
                state.console.print(
                    "  [grey62]Foods with no protein are omitted from this list.[/grey62]",
                    highlight=False,
                )

    if result["estimate_sources"]:
        est_with_protein = [s for s in result["estimate_sources"] if protein_by_name.get(s, 0.0) >= 1.0]
        if est_with_protein:
            state.console.print(
                "\n  [grey62]  Digestibility estimated (literature average) for:[/grey62]",
                highlight=False,
            )
            for _src in est_with_protein:
                state.console.print(f"  [grey62]    • {_src}[/grey62]", highlight=False)

    help_footer("meal-diaas", "iaa-ratios")
    raw_diaas = result.get("diaas")
    capped_diaas = min(raw_diaas, 1.0) if raw_diaas is not None else None
    return result["missing_aa_names"], result.get("digestible_complete_protein_g"), capped_diaas

def _print_recipe_bioavailability(
    ingredient_stats: list[dict],
    analysis_nutrients: dict[str, float],
    meal_result: dict | None = None,
) -> None:
    """Print per-ingredient digestibility breakdown and pooled meal DIAAS for a recipe."""
    total_protein = analysis_nutrients.get("protein_g", 0.0)
    if total_protein <= 0:
        return

    # Digestibility coefficients from pooled meal result (true ileal digestibility)
    dig_by_name: dict[str, float] = {}
    if meal_result:
        for r in meal_result.get("ingredients", []):
            dig_by_name[r["food_name"]] = r["digestibility"]

    legend = (
        f"[grey62](Digestibility: [{state.T['success']}]≥0.90 high[/{state.T['success']}]"
        f" · [{state.T['warning']}]≥0.70 moderate[/{state.T['warning']}]"
        f" · [{state.T['error']}]<0.70 low[/{state.T['error']}]"
        f"  ·  {ID_KEY})[/grey62]"
    )
    table_title("BIOAVAILABILITY — PER SERVING", legend)

    _ING_W = 30
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID", justify="right", min_width=7)
    tbl.add_column("Ingredient", min_width=_ING_W, max_width=_ING_W, no_wrap=True)
    tbl.add_column("Serving", justify="right", min_width=7)
    tbl.add_column("Crude protein", justify="right", min_width=13)
    tbl.add_column("Digestibility", justify="right", min_width=13)
    tbl.add_column("Limiting IAA", min_width=16)
    tbl.add_column("Digestible", justify="right", min_width=10)

    total_digestible = 0.0
    for s in ingredient_stats:
        p = s["protein_g"]
        amount_g = s.get("display_g", s.get("amount_g"))
        limiting_aa = s.get("limiting_aa")

        # Prefer true ileal digestibility from pooled result; fall back to static DIAAS
        if s["name"] in dig_by_name:
            dig_coeff: float | None = dig_by_name[s["name"]]
        else:
            dig_coeff = s.get("diaas")

        if dig_coeff is not None:
            dig = p * dig_coeff
            coeff_str = f"{dig_coeff:.2f}"
        else:
            dig = p
            coeff_str = "?"
        total_digestible += dig
        score = dig_coeff if dig_coeff is not None else 1.0
        color = state.T["success"] if score >= 0.90 else (state.T["warning"] if score >= 0.70 else state.T["error"])

        amount_str = f"{amount_g:.4g}g" if amount_g else "—"
        if limiting_aa:
            lim_label, _ = _usda.nutrient_label(limiting_aa)
        else:
            lim_label = "— (complete)" if s.get("has_aa") else "—"
        lim_cell = (f"[grey62]{lim_label}[/grey62]" if "complete" in lim_label
                    else f"[{state.T['warning']}]{lim_label}[/{state.T['warning']}]")

        tbl.add_row(
            _id_cell(s.get("fdc_id")),
            dot_cell(s['name'], _ING_W),
            amount_str,
            f"{p:.1f}g",
            f"[{color}]{coeff_str}[/{color}]",
            lim_cell,
            f"{dig:.1f}g",
        )

    state.console.print(tbl, highlight=False)

    if not (meal_result and meal_result.get("diaas") is not None):
        eff = total_digestible / total_protein if total_protein > 0 else 0.0
        color = state.T["success"] if eff >= 0.90 else (state.T["warning"] if eff >= 0.70 else state.T["error"])
        state.console.print(
            f"\n  [{state.T['warning']}]Total digestible protein: {total_digestible:.1f}g[/{state.T['warning']}]"
            f"  [grey62](from {total_protein:.1f}g, eff. digestibility [{color}]{eff:.2f}[/{color}])[/grey62]",
            highlight=False,
        )
    help_footer("bioavailability")


def _print_bioavailability(food_name: str, nutrients: dict[str, float]) -> None:
    """Print DIAAS-adjusted protein and anti-nutrient flags for a single food."""
    diaas = _usda.get_diaas(food_name)
    flags = _usda.get_antinutrient_flags(food_name)

    if diaas is None and not flags:
        return

    table_title("BIOAVAILABILITY")

    if diaas is not None:
        protein_raw = nutrients.get("protein_g", 0.0)
        protein_adj = protein_raw * diaas
        bar_len = min(int(diaas * 20), 20)
        color = state.T["success"] if diaas >= 0.90 else (state.T["warning"] if diaas >= 0.70 else state.T["error"])
        state.console.print(
            f"  Protein digestibility (est. DIAAS): [{color}]{diaas:.2f}  "
            f"{'█' * bar_len}[/{color}]"
        )
        if protein_raw > 0:
            state.console.print(
                f"  Digestible protein: [{state.T['hi']}]{protein_adj:.1f}g[/{state.T['hi']}]"
                f"  [grey62](from {protein_raw:.1f}g raw)[/grey62]",
                highlight=False,
            )
            pc = _usda.protein_completeness(nutrients)
            if pc.get("has_data"):
                limiting_score = min(pc["scores"].values())
                dig_complete = protein_adj * min(1.0, limiting_score)
                if pc.get("complete"):
                    dcp_color = state.T["success"]
                    dcp_line = Text.from_markup(
                        f"  [bold][{dcp_color}]Digestible complete protein: {dig_complete:.1f}g[/{dcp_color}][/bold]"
                    )
                else:
                    limiting_label = _usda.nutrient_label(pc["limiting_aa"])[0] if pc.get("limiting_aa") else "?"
                    dcp_color = state.T["warning"]
                    dcp_line = Text.from_markup(
                        f"  [bold][{dcp_color}]Digestible complete protein: {dig_complete:.1f}g[/{dcp_color}][/bold]"
                        f"  [grey62](limited by {limiting_label} — score {limiting_score:.2f})[/grey62]"
                    )
                state.console.print()
                state.console.print(
                    Panel(
                        Group(Rule(style=dcp_color), dcp_line, Rule(style=dcp_color)),
                        border_style=dcp_color, padding=(0, 1), width=100,
                    ),
                    highlight=False,
                )

    for flag in flags:
        state.console.print(f"  [{state.T['warning']}]Note:[/{state.T['warning']}] "
                      f"{flag['problem']} — {flag['cause']}")
        for label, sol in flag["solutions"]:
            state.console.print(f"    [grey62]* {label}: {sol}[/grey62]")
    help_footer("bioavailability")


def _print_complement_suggestions(
    base_nutrients: dict[str, float],
    context: str = "meal",  # "recipe", "meal", "daily", "food", "trend"
    offer_if_covered: bool = False,  # kept for call-site compat, no longer used
    base_food_name: str | None = None,
    basis_label: str | None = None,  # e.g. "per serving" or "whole recipe (7 servings)"
    base_diaas: float | None = None,  # pass effective DIAAS directly (e.g. for multi-ingredient recipes)
    silent_if_complete: bool = False,  # if True, print nothing when no gaps (avoids duplicate messages)
    recipe_servings: float | None = None,  # when base_nutrients is a whole-recipe total (servings > 1),
                                            # also show the per-serving DCP alongside each total
) -> None:
    """
    Display protein complement suggestions.
    context: controls framing text ("add to recipe" vs "add to meal" etc.)
    base_food_name: when provided, used to look up DIAAS for the base food so
                    the total digestible protein line is accurate.
    basis_label: appended to the section header to clarify what the gram amounts refer to.
    silent_if_complete: when True, return without printing anything if there are no AA gaps.
    recipe_servings: only pass when base_nutrients is a whole-recipe total; used solely to
                      show the equivalent per-serving DCP alongside each achieved-DCP figure.
    """
    if base_diaas is None:
        base_diaas = _usda.get_diaas(base_food_name) if base_food_name else None
    _digestibility = base_diaas if base_diaas is not None else 1.0

    gaps = _usda.get_aa_gaps(base_nutrients, digestibility=_digestibility)
    if not gaps:
        if not silent_if_complete:
            section_title("Protein Complement Suggestions")
            state.console.print("  [grey62]No complement suggestions are needed.[/grey62]")
        return

    try:
        pantry = _load_pantry_candidates()
    except Exception:
        pantry = []
    try:
        recipe_candidates = _load_recipe_candidates()
    except Exception:
        recipe_candidates = []
    pantry_and_recipes = pantry + recipe_candidates
    cache_candidates = _complements.load_cache_candidates(
        {c["name"].lower() for c in pantry_and_recipes}
    )
    max_improver_grams = 300 if context == "recipe" else 120
    suggestions = _usda.suggest_complements(
        base_nutrients, pantry_and_recipes, diet_pref=state._diet_pref,
        base_digestibility=_digestibility,
        base_food_name=base_food_name,
        max_improver_grams=max_improver_grams,
        cache_candidates=cache_candidates,
    )

    base_protein = base_nutrients.get("protein_g", 0.0)
    base_digestible = base_protein * base_diaas if base_diaas else base_protein

    pantry_suggs = suggestions["pantry"]
    general_suggs = suggestions["general"]
    pair_suggs = suggestions.get("pairs", [])
    diaas_improvers = suggestions.get("diaas_improvers", [])

    if pantry is None:
        pantry = []

    def _ranking_key(s: dict) -> tuple[float, float, float]:
        grams = float(s.get("grams", 10**9) or 10**9)
        # Completeness bonus only applies to practical servings (≤50g). A food
        # that needs 94g to achieve completeness shouldn't outrank a 7g option
        # that merely closes the gap — the large serving is the worse choice.
        practical = grams <= 50
        complete_bonus = 0.0 if (s.get("new_complete", False) and practical) else 1.0
        digestible = -float(s.get("digestible_protein_added", 0.0) or 0.0)
        return (complete_bonus, grams, digestible)

    pantry_suggs = sorted(pantry_suggs, key=_ranking_key)
    general_suggs = sorted(general_suggs, key=_ranking_key)

    # Determine whether pantry adequately covers all gaps
    pantry_covers = bool(pantry_suggs and pantry_suggs[0].get("new_complete", False))

    section_title("Protein Complement Suggestions", basis_label or "")
    _sugg_w = min(100, state.console.width)
    _sources: list[str] = []
    if pantry:
        _sources.append(f"{len(pantry)} pantry item{'s' if len(pantry) != 1 else ''}")
    if recipe_candidates:
        _sources.append(f"{len(recipe_candidates)} analyzed recipe{'s' if len(recipe_candidates) != 1 else ''}")
    _sources.append("built-in list of ~30 common protein sources")
    state.console.print(f"[grey62]{textwrap.fill('Considered: ' + ', '.join(_sources) + '.', width=_sugg_w - 2, initial_indent='  ', subsequent_indent='  ')}[/grey62]")
    state.console.print(f"[grey62]{textwrap.fill('Ranked by grams needed (smallest first). Exception: an option that fully completes the amino acid profile is promoted to the top — but only if its serving is 50 g or less.', width=_sugg_w - 2, initial_indent='  ', subsequent_indent='  ')}[/grey62]")
    gap_labels = ", ".join(
        _aa_label(aa) + f" ({score:.2f})"
        for aa, score, _ in gaps
    )
    state.console.print(f"  [grey62]Gaps: {gap_labels}[/grey62]")

    if not pantry:
        state.console.print(
            "  [grey62](No pantry items saved yet — add protein sources via Foods → My Pantry.)[/grey62]"
        )
    if pantry and not pantry_suggs:
        state.console.print(
            "  [grey62](Pantry items found but none qualify: their amino acid/protein ratio "
            "for the limiting amino acid falls below the FAO reference.)[/grey62]"
        )

    if context == "recipe":
        add_verb = "Add to recipe"
        pair_verb = "Serve alongside"
    elif context == "daily":
        add_verb = "Add to your day"
        pair_verb = "Pair with a meal"
    elif context == "trend":
        add_verb = "Add to upcoming meals"
        pair_verb = "Pair with an upcoming meal"
    elif context == "food":
        add_verb = "Add to food above"
        pair_verb = "Serve alongside"
    else:
        add_verb = "Add to meal"
        pair_verb = "Serve alongside"

    def _serving_hint(grams: float, serving_weight_g: float | None) -> str:
        if not serving_weight_g or serving_weight_g <= 0:
            return ""
        count = grams / serving_weight_g
        unit = "serving" if abs(count - 1.0) < 0.05 else "servings"
        return f"{count:.1f} {unit}"

    _GRAD_THRESHOLD = 30  # grams; above this, show graduated scale instead of single amount

    saw_estimate_or_generic = False

    def _source_tag(s: dict) -> str:
        nonlocal saw_estimate_or_generic
        if not s.get("fdc_id") and not s.get("recipe_id"):
            saw_estimate_or_generic = True
            return "  [grey62](generic estimate)[/grey62]"
        if s.get("estimated"):
            saw_estimate_or_generic = True
            return "  [grey62](estimated)[/grey62]"
        return ""

    def _show_suggestion(s: dict, label: str) -> None:
        diaas_str = f"  [grey62]DIAAS {s['diaas']:.2f}[/grey62]" if s.get("diaas") else ""
        state.console.print(f"\n  [{state.T['accent']}]{label}[/{state.T['accent']}] "
                      f"[bold]{s['name']}[/bold]{food_id_tag(s.get('fdc_id'), recipe_id=s.get('recipe_id'))}"
                      f"{_source_tag(s)}{diaas_str}")
        full_grams = s["grams"]

        if full_grams > _GRAD_THRESHOLD:
            # Graduated display: 4 steps at 25/50/75/100% of the full amount.
            raw_steps = [max(1, round(full_grams * f)) for f in (0.25, 0.50, 0.75, 1.0)]
            seen_g: set[int] = set()
            steps = [g for g in raw_steps if not (g in seen_g or seen_g.add(g))]  # type: ignore[func-returns-value]
            step_fracs = [g / full_grams for g in steps]

            # Volume hints: smallest and largest step.
            if s.get("recipe_id"):
                min_hint = _serving_hint(steps[0], s.get("serving_weight_g"))
                max_hint = _serving_hint(steps[-1], s.get("serving_weight_g"))
            else:
                min_hint = _volume_hint(steps[0], s["name"])
                max_hint = _volume_hint(steps[-1], s["name"])
            if min_hint and max_hint and min_hint != max_hint:
                vol_str = f"  [grey62]({min_hint} to {max_hint})[/grey62]"
            elif max_hint:
                vol_str = f"  [grey62]({max_hint})[/grey62]"
            elif s.get("recipe_id"):
                vol_str = ""
            else:
                # No cup/tbsp density available (weight-measured food) —
                # give an ounces reference for the full-serving amount instead.
                vol_str = f"  [grey62]({_amount_note(steps[-1], s['name'])})[/grey62]"

            grams_list = ", ".join(f"{g}g" for g in steps)
            state.console.print(f"    {add_verb}: [bold]{grams_list}[/bold]{vol_str}")

            # Primary-gap AA score at each step (linear interpolation: 0g→full).
            # orig_score is digestibility-adjusted; new_scores are raw — scale to match.
            if gaps:
                primary_aa, orig_score, _ = gaps[0]
                new_raw = s["new_scores"].get(primary_aa)
                if new_raw is not None and _digestibility > 0:
                    new_score_full = new_raw * _digestibility
                    aa_scores = [orig_score + frac * (new_score_full - orig_score)
                                 for frac in step_fracs]
                    def _fmt_aa(sc: float, is_last: bool) -> str:
                        if is_last:
                            c = state.T["success"] if sc >= 1.0 else state.T["warning"]
                            return f"[{c}]{sc:.2f}[/{c}]"
                        return f"{sc:.2f}"
                    score_strs = [_fmt_aa(sc, i == len(aa_scores) - 1)
                                  for i, sc in enumerate(aa_scores)]
                    state.console.print(
                        f"    {_aa_label(primary_aa)}: {', '.join(score_strs)}"
                    )

            # Digestible protein added at each step (exact linear scaling).
            dig_full = s["digestible_protein_added"]
            raw_full = s["protein_added"]
            dig_list = ", ".join(f"{dig_full * frac:.1f}g" for frac in step_fracs)
            state.console.print(
                f"    Adds: [bold]{dig_list}[/bold] digestible protein "
                f"[grey62](full serving: {raw_full:.1f}g raw)[/grey62]",
                highlight=False,
            )

            # Total digestible complete protein at each step.
            total_list = ", ".join(
                f"{base_digestible + dig_full * frac:.1f}g" for frac in step_fracs
            )
            state.console.print(
                f"    Total digestible complete protein: "
                f"[{state.T['success']}]{total_list}[/{state.T['success']}]",
                highlight=False,
            )
            if recipe_servings and recipe_servings > 1:
                per_serving_list = ", ".join(
                    f"{(base_digestible + dig_full * frac) / recipe_servings:.1f}g" for frac in step_fracs
                )
                state.console.print(
                    f"    [grey62]Per serving ({recipe_servings:g} servings): "
                    f"{per_serving_list}[/grey62]",
                    highlight=False,
                )

        else:
            # Single-amount display (unchanged for practical servings ≤ 30g).
            if s.get("recipe_id"):
                hint = _serving_hint(s["grams"], s.get("serving_weight_g"))
            else:
                hint = _amount_note(s["grams"], s["name"])
            vol_str = f"  [grey62]({hint})[/grey62]" if hint else ""
            state.console.print(f"    {add_verb}: [bold]{s['grams']}g[/bold]{vol_str}")
            # Show AA scores before → after for the most affected gaps.
            score_parts = []
            for (aa, orig_score, _), effect in zip(gaps[:3], _complements.aa_effects(s, gaps, digestibility=_digestibility)):
                label_aa = _aa_label(aa)
                arrow = f"[{state.T['success']}]{effect['after']:.2f}[/{state.T['success']}]" if effect["met"] \
                    else f"[{state.T['warning']}]{effect['after']:.2f}[/{state.T['warning']}]"
                score_parts.append(f"{label_aa}: {orig_score:.2f}→{arrow}")
            state.console.print(f"    Effect: {' · '.join(score_parts)}")
            dig = s["digestible_protein_added"]
            raw = s["protein_added"]
            if s.get("predicted_diaas") is not None:
                total_dig = (base_protein + raw) * min(1.0, s["predicted_diaas"])
            elif s.get("new_scores") and _digestibility > 0:
                new_raw_min = min(s["new_scores"].values())
                total_dig = (base_protein + raw) * min(1.0, _digestibility * new_raw_min)
            else:
                total_dig = base_digestible + dig
            state.console.print(f"    Adds: [bold]{dig:.1f}g[/bold] digestible protein "
                          f"[grey62](from {raw:.1f}g raw)[/grey62]", highlight=False)
            state.console.print(f"    Total digestible complete protein now = "
                          f"[{state.T['success']}]{total_dig:.1f}g[/{state.T['success']}]",
                          highlight=False)
            if recipe_servings and recipe_servings > 1:
                state.console.print(
                    f"    [grey62]Per serving ({recipe_servings:g} servings): "
                    f"{total_dig / recipe_servings:.1f}g[/grey62]",
                    highlight=False,
                )

        if s.get("opens_new_gap"):
            state.console.print(f"    [{state.T['warning']}]Note: closes the above gap but opens a new one "
                          f"— consider layering with a second complement.[/{state.T['warning']}]")
        if context == "recipe":
            state.console.print(f"    [grey62]{pair_verb}: serve {full_grams}g alongside[/grey62]")

    def _show_paged(suggs: list[dict], section_label: str, page_size: int = 3) -> None:
        """Display suggestions in pages of page_size, prompting for more after each."""
        if not suggs:
            return
        state.console.print(f"\n  [grey62]— {section_label} —[/grey62]")
        offset = 0
        while offset < len(suggs):
            batch = suggs[offset:offset + page_size]
            for i, s in enumerate(batch, offset + 1):
                _show_suggestion(s, f"Option {i}")
            offset += page_size
            if offset < len(suggs):
                try:
                    ans = _prompt(
                        f"More suggestions?  [grey62]({len(suggs) - offset} remaining — y/N)[/grey62]",
                        default="n").strip().lower()
                except Cancelled:
                    break
                if ans == "m":
                    raise ReturnToMain()
                if ans == "q":
                    raise SystemExit(0)
                if ans == "b":
                    raise Cancelled
                if ans != "y":
                    break

    def _show_pair_suggestion(p: dict, label: str) -> None:
        foods = p["foods"]
        closed_str = f"  [{state.T['success']}]✓ closes all gaps[/{state.T['success']}]" \
            if p.get("gaps_closed") else ""
        state.console.print(f"\n  [{state.T['accent']}]{label}[/{state.T['accent']}]  "
                      f"[bold]{foods[0]['name']}[/bold]{food_id_tag(foods[0].get('fdc_id'), recipe_id=foods[0].get('recipe_id'))}"
                      f"  +  [bold]{foods[1]['name']}[/bold]{food_id_tag(foods[1].get('fdc_id'), recipe_id=foods[1].get('recipe_id'))}{closed_str}")
        for f in foods:
            diaas_str = f"  [grey62]DIAAS {f['diaas']:.2f}[/grey62]" if f.get("diaas") else ""
            if f.get("recipe_id"):
                hint = _serving_hint(f["grams"], f.get("serving_weight_g"))
            else:
                hint = _amount_note(f["grams"], f["name"])
            vol_str = f"  [grey62]({hint})[/grey62]" if hint else ""
            state.console.print(f"    {add_verb}: [bold]{f['grams']}g[/bold]{vol_str}  "
                          f"[bold]{f['name']}[/bold]{food_id_tag(f.get('fdc_id'), recipe_id=f.get('recipe_id'))}{diaas_str}")
        # Show AA scores before → after for the top gaps.
        score_parts = []
        for (aa, orig_score, _), effect in zip(gaps[:3], _complements.aa_effects(p, gaps, digestibility=_digestibility)):
            label_aa = _aa_label(aa)
            arrow = f"[{state.T['success']}]{effect['after']:.2f}[/{state.T['success']}]" if effect["met"] \
                else f"[{state.T['warning']}]{effect['after']:.2f}[/{state.T['warning']}]"
            score_parts.append(f"{label_aa}: {orig_score:.2f}→{arrow}")
        if score_parts:
            state.console.print(f"    Effect: {' · '.join(score_parts)}")
        state.console.print(
            f"    Combined: [bold]{p['total_grams']}g[/bold] total  ·  "
            f"[bold]{p['total_dig_added']:.1f}g[/bold] digestible protein added "
            f"[grey62](from {p['total_protein_added']:.1f}g raw)[/grey62]",
            highlight=False,
        )
        if p.get("predicted_diaas") is not None:
            total_dig = (base_protein + p["total_protein_added"]) * min(1.0, p["predicted_diaas"])
        elif p.get("new_scores") and _digestibility > 0:
            new_raw_min = min(p["new_scores"].values())
            total_dig = (base_protein + p["total_protein_added"]) * min(1.0, _digestibility * new_raw_min)
        else:
            total_dig = base_digestible + p["total_dig_added"]
        state.console.print(
            f"    Total digestible complete protein now = "
            f"[{state.T['success']}]{total_dig:.1f}g[/{state.T['success']}]",
            highlight=False,
        )

    def _show_paged_pairs(pairs: list[dict], section_label: str, page_size: int = 3) -> None:
        if not pairs:
            return
        state.console.print(f"\n  [{state.T['hi']}]{section_label}[/{state.T['hi']}]")
        state.console.print(
            "  [grey62]Two-food combinations: food A closes the primary gap (but opens a new one);\n"
            "  food B closes what A left behind.  Both together achieve a complete amino acid profile.[/grey62]"
        )
        offset = 0
        while offset < len(pairs):
            batch = pairs[offset:offset + page_size]
            for i, p in enumerate(batch, offset + 1):
                _show_pair_suggestion(p, f"Combo {i}")
            offset += page_size
            if offset < len(pairs):
                try:
                    ans = _prompt(
                        f"More combinations?  [grey62]({len(pairs) - offset} remaining — y/N)[/grey62]",
                        default="n").strip().lower()
                except Cancelled:
                    break
                if ans == "m":
                    raise ReturnToMain()
                if ans == "q":
                    raise SystemExit(0)
                if ans == "b":
                    raise Cancelled
                if ans != "y":
                    break

    # Per-AA note about which common foods typically fall below the FAO reference
    # and therefore cannot close that gap regardless of quantity.
    def _general_exhausted_msg(n_shown: int, n_already_shown: int = 0) -> None:
        limiting_aa = gaps[0][0] if gaps else None
        limiting_label = _aa_label(limiting_aa) if limiting_aa else "this amino acid"
        low_in = _complements.AA_LOW_IN.get(limiting_aa or "", "many plant foods")
        if n_shown > 0:
            prefix = "All options that qualify are shown above — no others meet the criteria."
        elif n_already_shown > 0:
            prefix = "No additional qualifying options found in the database."
        else:
            prefix = "No qualifying options found in the database."
        state.console.print(
            f"\n  [grey62]{prefix}[/grey62]\n"
            f"  [grey62]A qualifying complement must have a {limiting_label}/protein ratio above[/grey62]\n"
            f"  [grey62]the FAO reference to close the gap to score 1.0 in a practical serving (≤ 500g).[/grey62]\n"
            f"  [grey62]Score 1.0 = meets human requirements (the floor, not an aspirational target).[/grey62]\n"
            f"  [grey62]Foods that don't qualify for a {limiting_label} gap: {low_in}.[/grey62]\n"
            f"  [grey62]Their ratio falls below the reference — adding them dilutes the score further.[/grey62]"
        )

    def _show_diaas_improver(s: dict, label: str) -> None:
        diaas_str = f"  [grey62]DIAAS {s['diaas']:.2f}[/grey62]" if s.get("diaas") else ""
        state.console.print(f"\n  [{state.T['accent']}]{label}[/{state.T['accent']}] "
                      f"[bold]{s['name']}[/bold]{food_id_tag(s.get('fdc_id'))}{_source_tag(s)}{diaas_str}")
        cur = s.get("current_diaas", 0.0)
        cur_color = state.T["warning"] if cur < 0.9 else state.T["success"]
        for step in s.get("steps", []):
            g = step["grams"]
            new = step["new_diaas"]
            dcp = step.get("dcp")
            vol = _amount_note(g, s["name"])
            vol_str = f"  [grey62]({vol})[/grey62]" if vol else ""
            new_color = state.T["success"] if new >= 0.9 else state.T["warning"]
            dcp_str = (f"  →  DCP [{state.T['success']}]{dcp:.1f}g[/{state.T['success']}]"
                       if dcp is not None else "")
            state.console.print(
                f"    {add_verb} [bold]{g}g[/bold]{vol_str}:  "
                f"Meal DIAAS [{cur_color}]{cur:.2f}[/{cur_color}]"
                f" → [{new_color}]{new:.2f}[/{new_color}]{dcp_str}",
                highlight=False,
            )

    def _show_paged_improvers(suggs: list[dict], section_label: str, page_size: int = 3) -> None:
        if not suggs:
            return
        state.console.print(f"\n  [grey62]— {section_label} —[/grey62]")
        offset = 0
        while offset < len(suggs):
            batch = suggs[offset:offset + page_size]
            for i, s in enumerate(batch, offset + 1):
                _show_diaas_improver(s, f"Option {i}")
            offset += page_size
            if offset < len(suggs):
                try:
                    ans = _prompt(
                        f"More suggestions?  [grey62]({len(suggs) - offset} remaining — y/N)[/grey62]",
                        default="n").strip().lower()
                except Cancelled:
                    break
                if ans == "m":
                    raise ReturnToMain()
                if ans == "q":
                    raise SystemExit(0)
                if ans == "b":
                    raise Cancelled
                if ans != "y":
                    break

    try:
        if pantry_suggs:
            _show_paged(pantry_suggs, "From your pantry")
            if general_suggs:
                try:
                    ans = _prompt("Look elsewhere for more options?  [grey62](y/N)[/grey62]",
                                  default="n").strip().lower()
                except Cancelled:
                    help_footer("comp")
                    return
                if ans == "m":
                    raise ReturnToMain()
                if ans == "q":
                    raise SystemExit(0)
                if ans == "b":
                    help_footer("comp")
                    return
                if ans == "y":
                    _show_paged(general_suggs, "Other options", page_size=5)
                    _general_exhausted_msg(len(general_suggs))
            else:
                _general_exhausted_msg(0, n_already_shown=len(pantry_suggs))
        else:
            if general_suggs:
                _show_paged(general_suggs, "Suggestions", page_size=5)
                _general_exhausted_msg(len(general_suggs))
            else:
                _general_exhausted_msg(0)
    except Cancelled:
        help_footer("comp")
        return

    if pair_suggs:
        try:
            _show_paged_pairs(pair_suggs, "Two-food combinations")
        except Cancelled:
            pass

    if diaas_improvers:
        have_gap_closers = bool(pantry_suggs or general_suggs)
        state.console.print(
            f"\n  [{state.T['hi']}]DIAAS-boosting options[/{state.T['hi']}]",
            highlight=False,
        )
        if have_gap_closers:
            state.console.print(
                "  [grey62]These foods can't close a specific AA gap on their own, but raise "
                "the meal's overall DIAAS score toward 0.90 via protein pooling.[/grey62]"
            )
        else:
            state.console.print(
                "  [grey62]No single food can close the specific AA gap at a practical serving size.[/grey62]\n"
                "  [grey62]These options instead raise the meal's overall DIAAS score toward 0.90[/grey62]\n"
                "  [grey62]by pooling their digestible amino acids with the base food.[/grey62]"
            )
        try:
            _show_paged_improvers(diaas_improvers[:3], "DIAAS-boosting options", page_size=3)
        except Cancelled:
            pass

    # Two-step combinations: top gap-closer paired with best DIAAS-booster for
    # the resulting pool.  Only offered when both tiers produced results.
    top_gap_closers = (pantry_suggs + general_suggs)[:3]
    if top_gap_closers and diaas_improvers:
        try:
            ans = _prompt(
                "\nSee two-step combinations (gap-closer + DIAAS boost)?  [grey62](Y/n)[/grey62]",
                default="y").strip().lower()
        except Cancelled:
            ans = "n"
        if ans == "m":
            raise ReturnToMain()
        if ans == "q":
            raise SystemExit(0)
        if ans in ("y", ""):
            state.console.print(
                f"\n  [{state.T['hi']}]Two-step combinations[/{state.T['hi']}]\n"
                "  [grey62]Each pairs a gap-closer (Step 1) with the best DIAAS-booster "
                "for the resulting protein pool (Step 2).[/grey62]"
            )
            for i, gc in enumerate(top_gap_closers, 1):
                combo = _complements.two_step_combo(
                    gc, base_nutrients,
                    base_protein=base_protein, base_digestible=base_digestible,
                    pantry_candidates=pantry_and_recipes, diet_pref=state._diet_pref,
                    gaps=gaps, max_improver_grams=max_improver_grams,
                    fallback_digestibility=_digestibility, aa_effects_limit=2,
                )
                if combo is None:
                    continue
                step1, step2, gc_diaas = combo["step1"], combo["step2"], combo["gc_diaas"]
                gc_name = step1["name"]
                fdc_str = food_id_tag(step1.get("fdc_id"), recipe_id=step1.get("recipe_id"))
                vol1 = step1.get("amount_note")
                vol1_str = f"  [grey62]({vol1})[/grey62]" if vol1 else ""
                gc_color = state.T["warning"] if gc_diaas < 0.9 else state.T["success"]
                state.console.print(
                    f"\n  [{state.T['accent']}]Combination {i}[/{state.T['accent']}]"
                )
                state.console.print(
                    f"    Step 1 — {add_verb} [bold]{step1['grams']}g[/bold]{vol1_str}  "
                    f"[bold]{gc_name}[/bold]{fdc_str}{_source_tag(step1)}",
                    highlight=False,
                )
                score_parts = []
                for (aa, orig_score, _), effect in zip(gaps[:2], step1["aa_effects"]):
                    label_aa = _aa_label(aa)
                    arrow = (f"[{state.T['success']}]{effect['after']:.2f}[/{state.T['success']}]"
                             if effect["met"]
                             else f"[{state.T['warning']}]{effect['after']:.2f}[/{state.T['warning']}]")
                    score_parts.append(f"{label_aa}: {orig_score:.2f}→{arrow}")
                if score_parts:
                    state.console.print(f"      AA effect: {' · '.join(score_parts)}")
                state.console.print(
                    f"      DCP: [{state.T['success']}]{step1['dcp_before']:.1f}g[/{state.T['success']}]"
                    f" → [{gc_color}]{step1['dcp_after']:.1f}g[/{gc_color}]",
                    highlight=False,
                )
                if step2 is None:
                    state.console.print(
                        "    Step 2 — [grey62]no available food improves on the DIAAS "
                        "already achieved by Step 1[/grey62]"
                    )
                    continue
                b_color = state.T["success"] if step2["new_diaas"] >= 0.9 else state.T["warning"]
                vol2 = step2.get("amount_note")
                vol2_str = f"  [grey62]({vol2})[/grey62]" if vol2 else ""
                b_fdc = food_id_tag(step2.get("fdc_id"), recipe_id=step2.get("recipe_id"))
                state.console.print(
                    f"    Step 2 — {add_verb} [bold]{step2['grams']}g[/bold]{vol2_str}  "
                    f"[bold]{step2['name']}[/bold]{b_fdc}{_source_tag(step2)}",
                    highlight=False,
                )
                state.console.print(
                    f"      Meal DIAAS [{gc_color}]{gc_diaas:.2f}[/{gc_color}]"
                    f" → [{b_color}]{step2['new_diaas']:.2f}[/{b_color}]",
                    highlight=False,
                )
                if step2["dcp_after"] is not None:
                    total_gain = step2["net_gain"]
                    gain_str = f"+{total_gain:.1f}g" if total_gain >= 0 else f"{total_gain:.1f}g"
                    state.console.print(
                        f"      DCP: [{gc_color}]{step2['dcp_before']:.1f}g[/{gc_color}]"
                        f" → [{b_color}]{step2['dcp_after']:.1f}g[/{b_color}]"
                        f"  [grey62](net gain from base: {gain_str})[/grey62]",
                        highlight=False,
                    )

    if saw_estimate_or_generic:
        state.console.print(
            f"\n  [grey62]{textwrap.fill(_complements.ESTIMATE_NOTE, width=_sugg_w - 2, initial_indent='', subsequent_indent='  ')}[/grey62]"
        )

    if top_gap_closers and diaas_improvers:
        help_footer("comb", "comp", "comp-estimate")
    else:
        help_footer("comp", "comp-estimate")

def _print_dcp_adequacy_section(
    meal_result: "dict | None",
    analysis_nutrients: dict[str, float],
    profile: "_profile.UserProfile | None",
    *,
    dcp_g: float | None = None,
    dcp_skip: bool = False,
    dcp_approximate: bool = False,
    dcp_notes: "list[str] | None" = None,
    context_label: "str | None" = None,
    dcp_total_g: float | None = None,
    servings: float | None = None,
) -> None:
    """Combined DCP summary + personalized protein adequacy, shown after BIOAVAILABILITY.

    When meal DIAAS is available, renders: DIAAS explanation, DCP panel with adequacy
    merged inside.  Falls back to _print_protein_adequacy when DIAAS is not available.

    dcp_total_g/servings: when the recipe has more than one serving, also print the
    whole-recipe DCP total alongside the per-serving figure so the two aren't confused.
    """
    total_protein = analysis_nutrients.get("protein_g", 0.0)

    if dcp_skip or not (meal_result and meal_result.get("diaas") is not None):
        _print_protein_adequacy(
            analysis_nutrients, profile,
            context_label=context_label,
            dcp_g=None if dcp_skip else dcp_g,
            dcp_total_g=None if dcp_skip else dcp_total_g,
            servings=servings,
        )
        return

    meal_diaas = meal_result["diaas"]
    dcp = meal_result.get("digestible_complete_protein_g") or 0.0
    limiting_label = meal_result.get("limiting_label") or ""
    aa_p = meal_result.get("aa_protein_g", total_protein)
    color = state.T["success"] if meal_diaas >= 0.90 else (state.T["warning"] if meal_diaas >= 0.70 else state.T["error"])

    title = f"Protein Adequacy — {context_label}" if context_label else "Protein Adequacy"
    section_title(title)

    # Gather DIAAS explanation data
    limiting_iaa = meal_result.get("limiting_iaa") or ""
    iaa_ratios   = meal_result.get("iaa_ratios") or {}
    lim_ratio    = iaa_ratios.get(limiting_iaa)
    fao_ref      = _diaas.FAO_REFERENCE.get(limiting_iaa) if limiting_iaa else None
    protein_note = (f"{aa_p:.1f}g (from AA-analyzed ingredients)"
                    if aa_p < total_protein - 0.05 else f"{total_protein:.1f}g")

    # DCP result — Rules above and below, no surrounding box
    aa_dig_p = meal_result.get("aa_dig_protein_g")
    uncapped = aa_p * min(meal_diaas, 1.0)
    dcp_was_capped = aa_dig_p is not None and dcp < uncapped - 0.05
    protein_basis = aa_p if aa_p < total_protein - 0.05 else total_protein
    basis_label = "raw protein (AA-analyzed)" if aa_p < total_protein - 0.05 else "raw protein"
    _W = min(100, state.console.width)
    state.console.print()
    state.console.print(Rule(style=color), width=_W)
    if dcp_was_capped:
        avg_dig = aa_dig_p / protein_basis if protein_basis > 0 else 0.0
        state.console.print(
            f"  [bold][{color}]Digestible complete protein = {dcp:.1f}g:[/{color}][/bold]"
            f"  [grey62]{protein_basis:.1f}g {basis_label}"
            f" × [{color}]{meal_diaas:.2f}[/{color}] DIAAS = {uncapped:.1f}g.[/grey62]",
            highlight=False,
        )
        _cap_plain = (
            f"This figure is adjusted down (capped) to {dcp:.1f}g. This is needed because"
            f" the DIAAS formula's projection of {uncapped:.1f}g exceeds the {dcp:.1f}g of"
            f" protein actually absorbed from these foods ({protein_basis:.1f}g raw ×"
            f" weighted-average digestibility {avg_dig:.2f} = {dcp:.1f}g absorbed, weighted"
            f" from per-ingredient estimates). DCP cannot exceed absorbed protein, so it is"
            f" capped here. Type ?dcp-cap for a full explanation."
        )
        _wrapped = textwrap.fill(
            _cap_plain, width=_W - 2,
            initial_indent="  ", subsequent_indent="  ",
        )
        state.console.print(f"[grey62]{_wrapped}[/grey62]", highlight=False)
    else:
        state.console.print(
            f"  [bold][{color}]Digestible complete protein = {dcp:.1f}g,[/{color}][/bold]"
            f"  [grey62]from {protein_basis:.1f}g {basis_label}"
            f" × [{color}]{meal_diaas:.2f}[/{color}] meal DIAAS (see below)[/grey62]",
            highlight=False,
        )

    if servings is not None and servings > 1 and dcp_total_g is not None:
        state.console.print(
            f"  [grey62]Per serving: [{color}]{dcp:.1f}g[/{color}]"
            f"   ·   Whole recipe ({servings:g} servings): [{color}]{dcp_total_g:.1f}g[/{color}][/grey62]",
            highlight=False,
        )

    if dcp_approximate and dcp_notes:
        for note in dcp_notes:
            state.console.print(f"  [grey62]↳ {note}[/grey62]", highlight=False)

    if meal_result.get("missing_aa_names"):
        n = len(meal_result["missing_aa_names"])
        state.console.print(
            f"  [grey62](⚑ {n} ingredient{'s' if n != 1 else ''} missing AA data — see analysis below)[/grey62]",
            highlight=False,
        )

    if profile is not None:
        protein_target = _profile.compute_rda(profile).get("protein_g", (0.0,))[0]
        if protein_target > 0:
            pct = dcp / protein_target * 100.0
            activity = _profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level).lower()
            pct_color = state.T["success"] if pct >= 100 else (state.T["warning"] if pct >= 50 else state.T["error"])
            state.console.print(
                f"  [grey62]This is [{pct_color}]{pct:.0f}%[/{pct_color}]"
                f" of the daily profile (\"{activity}\") target of {protein_target:.1f} g/day.[/grey62]",
                highlight=False,
            )

    state.console.print(Rule(style=color), width=_W)

    # DIAAS explanation + actual computation below the result
    state.console.print(
        f"\n  [grey62]The total amounts of essential amino acids (EAA) in the meal are summed across\n"
        f"  each ingredient, then each sum is divided by the FAO 2013 reference requirement for that\n"
        f"  EAA (expressed per gram of total protein). The smallest resulting ratio is the meal DIAAS.[/grey62]",
        highlight=False,
    )
    if limiting_label and lim_ratio is not None and fao_ref is not None:
        supply = lim_ratio * fao_ref
        state.console.print(
            f"\n  [grey62][{color}]{limiting_label}[/{color}] is the most limiting EAA:"
            f" this meal supplies {supply:.1f} mg of {limiting_label} per gram of protein.[/grey62]",
            highlight=False,
        )
        state.console.print(
            f"  [grey62]{supply:.1f} mg/g protein ÷ FAO req. for {limiting_label}"
            f" ({fao_ref:.1f} mg/g protein) = [{color}]{lim_ratio:.3f}[/{color}]"
            f"  →  meal DIAAS = [{color}]{meal_diaas:.2f}[/{color}][/grey62]",
            highlight=False,
        )
    elif limiting_label and lim_ratio is not None:
        state.console.print(
            f"\n  [grey62][{color}]{limiting_label}[/{color}] is the most limiting EAA"
            f" — ratio = [{color}]{lim_ratio:.3f}[/{color}]  →  meal DIAAS = [{color}]{meal_diaas:.2f}[/{color}][/grey62]",
            highlight=False,
        )
    state.console.print(
        f"  [grey62]DCP = {protein_note} × [{color}]{meal_diaas:.2f}[/{color}]"
        f" = [{color}]{dcp:.1f}g[/{color}] digestible complete protein per serving.[/grey62]",
        highlight=False,
    )
    state.console.print(
        f"\n  [{state.T['warning']}]At any prompt, type ?EAA (essential amino acids),"
        f" ?DIAAS, or ?FRR (FAO reference requirement) for help with these topics.[/{state.T['warning']}]",
        highlight=False,
    )


def _print_rda_targets(profile: "_profile.UserProfile") -> None:
    """Print a table of personalized daily nutrient targets derived from the user's profile."""
    rda = _profile.compute_rda(profile, diet_pref=state._diet_pref)
    optimal = _profile.compute_optimal(profile)
    max_limits = dict(profile.max_limits)
    built_in_limits = {k: v for k, v in _profile.compute_upper_limits(profile).items()
                        if k not in max_limits}

    section_title("Daily Nutrient Targets")
    state.console.print(
        f"  Profile: age {profile.age}  ·  {profile.sex}"
        f"  ·  {_profile.format_weight(profile.weight_kg, profile.weight_unit)}"
        f"  ·  {_profile.format_height(profile.height_cm, profile.height_unit)}"
        f"  ·  {_profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level)}\n",
        highlight=False,
    )

    groups = [
        ("Macronutrients", ["calories", "protein_g", "carbs_g", "fiber_g", "omega3_ala_mg"]),
        ("Minerals", ["calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
                      "potassium_mg", "sodium_mg", "zinc_mg", "iodine_mcg", "selenium_mcg"]),
        ("Vitamins", ["vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
                      "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
                      "b6_mg", "folate_mcg", "b12_mcg", "choline_mg"]),
    ]

    _RDA_W = 30
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Nutrient",   min_width=_RDA_W, max_width=_RDA_W, no_wrap=True)
    tbl.add_column("Daily Goal", justify="right", min_width=14)
    tbl.add_column("Goal Type",  min_width=14)
    if optimal:
        tbl.add_column("Optimal", justify="right", min_width=14)

    for group_name, keys in groups:
        present = [(k, rda[k]) for k in keys if k in rda]
        if not present:
            continue
        tbl.add_row(*([f"[{state.T['hi']}]{group_name}[/{state.T['hi']}]", "", ""] + ([""] if optimal else [])))
        for key, (val, unit, rda_type) in present:
            label_info = _usda.nutrient_label(key)
            label = label_info[0] if label_info else key.replace("_", " ").title()
            if rda_type == "limit":
                type_color = state.T["warning"]
                type_label = "limit (max)"
            elif rda_type == "target":
                type_color = state.T["hi"]
                type_label = "target"
            else:
                type_color = state.T["success"]
                type_label = "minimum"
            row = [
                dot_cell(label, _RDA_W),
                f"{val:.1f} {unit}",
                f"[{type_color}]{type_label}[/{type_color}]",
            ]
            if optimal:
                opt_entry = optimal.get(key)
                row.append(f"{opt_entry[0]:.1f} {opt_entry[1]}" if opt_entry else "–")
            tbl.add_row(*row)

    state.console.print(tbl, highlight=False)
    table_footer(
        "  [grey62]Minimum = daily requirement  ·  Target = recommended intake  ·  Limit = upper safe intake[/grey62]",
        "  [grey62]Targets are personalized to your age, sex, weight, height, and activity level.[/grey62]",
    )
    diet_note = iron_zinc_bioavailability_note(state._diet_pref)
    if diet_note:
        state.console.print(f"  [{state.T['warning']}]{diet_note}[/{state.T['warning']}]", highlight=False)
        help_footer("diet-bioavailability")
    if optimal:
        table_footer("  [grey62]Optimal = your custom Profile Optimal target, where configured — see Settings → Nutrient targets[/grey62]")
        help_footer("optimal")

    def _print_limit_table(title: str, entries: dict[str, float]) -> None:
        state.console.print()
        table_title(title)
        limit_tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        limit_tbl.add_column("Nutrient", min_width=_RDA_W, max_width=_RDA_W, no_wrap=True)
        limit_tbl.add_column("Max limit", justify="right", min_width=14)
        for key, val in entries.items():
            label_info = _usda.nutrient_label(key)
            label = label_info[0] if label_info else key.replace("_", " ").title()
            unit = label_info[1] if label_info else ""
            limit_tbl.add_row(dot_cell(label, _RDA_W), f"{val:.1f} {unit}")
        state.console.print(limit_tbl, highlight=False)

    if max_limits:
        _print_limit_table("Your custom max limits", max_limits)
    if built_in_limits:
        _print_limit_table("Built-in safe upper limits (applied automatically unless you set your own above)",
                            built_in_limits)
    if max_limits or built_in_limits:
        help_footer("maxlimits")

    help_footer("goals")


def _print_rda_comparison(nutrients: dict[str, float], profile: "_profile.UserProfile", *,
                          title: str = "Daily Intake vs. Recommended Values",
                          intake_label: str = "Intake") -> None:
    """Print a table comparing daily nutrient totals against personalized RDA (and, where
    configured, Profile Optimal) targets, flagging any nutrient near a custom max limit.

    title/intake_label let callers reuse this for non-daily comparisons — e.g. the
    multi-day nutrient trend view passes an N-day average in `nutrients` with an
    "N-day Average" intake_label, so the exact same status coloring, diet-aware
    notes, and Optimal/max-limit columns apply without duplicating this function.
    """
    rda = _profile.compute_rda(profile, diet_pref=state._diet_pref)
    optimal = _profile.compute_optimal(profile)
    max_limits = _profile.get_max_limits(profile)
    nutrient_label = _usda.nutrient_label  # (key) → (label, unit) | None

    section_title(title)
    state.console.print(
        f"  Profile: age {profile.age}  ·  {profile.sex}"
        f"  ·  {_profile.format_weight(profile.weight_kg, profile.weight_unit)}"
        f"  ·  {_profile.format_height(profile.height_cm, profile.height_unit)}"
        f"  ·  {_profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level)}\n",
        highlight=False,
    )

    _RDA_W = 30
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Nutrient",  min_width=_RDA_W, max_width=_RDA_W, no_wrap=True)
    tbl.add_column(intake_label, justify="right", min_width=12)
    tbl.add_column("Target",    justify="right", min_width=12)
    tbl.add_column("% of RDA",  justify="right", min_width=10)
    tbl.add_column("Status",    min_width=28)
    if optimal:
        tbl.add_column("Optimal target", justify="right", min_width=14)
        tbl.add_column("% of Optimal",   justify="right", min_width=12)

    BAR_WIDTH = 16
    b12_pct: "float | None" = None

    for key, (rda_val, unit, rda_type) in rda.items():
        intake = nutrients.get(key, 0.0)
        label_info = nutrient_label(key)
        label = label_info[0] if label_info else key.replace("_", " ").title()

        if rda_val and rda_val > 0:
            pct = (intake / rda_val) * 100.0
        else:
            pct = 0.0

        if key == "b12_mcg":
            b12_pct = pct

        # Format intake and target
        if unit in ("kcal", "g"):
            intake_str = f"{intake:.1f} {unit}"
            target_str = f"{rda_val:.1f} {unit}"
        else:
            intake_str = f"{intake:.1f} {unit}"
            target_str = f"{rda_val:.1f} {unit}"
        pct_str = f"{pct:.0f}%"

        # Status bar and color
        tier = rda_status(pct, rda_type)
        bar_color = {"met": state.T["success"], "near": state.T["warning"],
                     "low": state.T["error"], "over": state.T["error"]}[tier]
        if rda_type == "limit":
            status_note = {"met": "within limit", "near": "approaching limit"}.get(
                tier, f"over limit by {pct - 100:.0f}%"
            )
            filled = min(int(BAR_WIDTH * min(pct, 200) / 200), BAR_WIDTH)
        else:
            status_note = "met" if tier == "met" else f"{100 - pct:.0f}% short"
            filled = min(int(BAR_WIDTH * min(pct, 100) / 100), BAR_WIDTH)

        bar = f"[{bar_color}]{'█' * filled}[/{bar_color}]{'░' * (BAR_WIDTH - filled)}"
        status_cell = f"{bar}  [{bar_color}]{status_note}[/{bar_color}]"

        limit = max_limits.get(key)
        label_cell = dot_cell(label, _RDA_W)
        if limit and limit_warning(intake, limit):
            lc = state.T["error"] if intake >= limit else state.T["warning"]
            label_cell = f"[{lc}]{label_cell}[/{lc}]"

        row = [label_cell, intake_str, target_str, pct_str, status_cell]
        if optimal:
            opt_entry = optimal.get(key)
            if opt_entry and opt_entry[0] > 0:
                opt_val, opt_unit, opt_type = opt_entry
                opt_pct = intake / opt_val * 100.0
                opt_color = rda_status(opt_pct, opt_type)
                opt_bar_color = {"met": state.T["success"], "near": state.T["warning"],
                                  "low": state.T["error"], "over": state.T["error"]}[opt_color]
                row.append(f"{opt_val:.1f} {opt_unit}")
                row.append(f"[{opt_bar_color}]{opt_pct:.0f}%[/{opt_bar_color}]")
            else:
                row.extend(["–", "–"])
        tbl.add_row(*row)

    state.console.print(tbl, highlight=False)
    table_footer("  [grey62]Target = RDA or Adequate Intake  ·  Limit = Tolerable Upper Intake Level[/grey62]")
    if optimal:
        table_footer("  [grey62]Optimal target = your custom Profile Optimal setting, where configured (\"–\" = not set)[/grey62]")
        help_footer("optimal")
    if max_limits:
        help_footer("maxlimits")

    diet_note = iron_zinc_bioavailability_note(state._diet_pref)
    if diet_note:
        state.console.print(f"\n  [{state.T['warning']}]{diet_note}[/{state.T['warning']}]", highlight=False)
        help_footer("diet-bioavailability")

    if b12_pct is not None:
        b12_note = b12_deficiency_note(state._diet_pref, b12_pct)
        if b12_note:
            state.console.print(f"\n  [{state.T['error']}]⚠ {b12_note}[/{state.T['error']}]", highlight=False)
            help_footer("diet-bioavailability")

    help_footer("rda")
