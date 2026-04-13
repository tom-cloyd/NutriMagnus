import json

from rich.table import Table

import db as _db
import diaas as _diaas
import usda as _usda
import profile as _profile
from .. import state
from ..ui.prompts import Cancelled, _prompt


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
        try:
            if row.get("fdc_id") is not None:
                with _db.get_db() as conn:
                    cached = _db.get_cached_food(conn, row["fdc_id"])
                if cached and cached.get("nutrients_json"):
                    nutrients = json.loads(cached["nutrients_json"])
        except Exception:
            nutrients = None
        candidates.append({
            "name": row.get("food_name", ""),
            "fdc_id": row.get("fdc_id"),
            "nutrients": nutrients,
            "diaas": _usda.get_diaas(row.get("food_name", "")),
        })
    return candidates

def _print_nutrient_table(nutrients: dict[str, float], title: str = "Nutrients",
                           per_label: str = "") -> None:
    """Render a rich table of nutrients grouped by category."""
    groups = [
        ("Macronutrients", [
            "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
            "saturated_fat_g", "mono_fat_g", "poly_fat_g",
        ]),
        ("Minerals", [
            "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
            "potassium_mg", "sodium_mg", "zinc_mg",
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

    heading = title
    if per_label:
        heading += f"  [dim]({per_label})[/dim]"
    state.console.print(f"\n[{state.T['accent']}]{heading}[/{state.T['accent']}]")
    state.console.rule()

    tbl = Table(show_header=True, header_style=state.T["accent"], box=None, padding=(0, 2))
    tbl.add_column("Nutrient", style="", min_width=24)
    tbl.add_column("Amount", justify="right", min_width=10)
    tbl.add_column("Unit", style="dim", min_width=8)

    for group_name, keys in groups:
        present = [(k, nutrients[k]) for k in keys if k in nutrients]
        if not present:
            continue
        tbl.add_row(f"[{state.T['hi']}]{group_name}[/{state.T['hi']}]", "", "")
        for key, val in present:
            label, unit = _usda.nutrient_label(key)
            tbl.add_row(f"  {label}", f"{val:.2f}", unit)

    state.console.print(tbl)


def _print_protein_completeness(
    nutrients: dict[str, float],
    *,
    context_label: str | None = None,
    partial_data_note: str | None = None,
) -> bool:
    """Print protein completeness assessment if amino acid data is available.
    Returns True if amino acid data was present, False otherwise."""
    result = _usda.protein_completeness(nutrients)
    if not result["has_data"]:
        state.console.print("[dim]  (No amino acid data available for protein completeness analysis.)[/dim]")
        return False

    if context_label:
        state.console.print(
            f"\n  [{state.T['hi']}]Protein quality — {context_label}[/{state.T['hi']}]",
            highlight=False,
        )
    status = (f"[{state.T['success']}]Complete protein[/{state.T['success']}]"
              if result["complete"]
              else f"[{state.T['warning']}]Incomplete protein[/{state.T['warning']}]")
    state.console.print(f"  Protein Quality: {status}")
    state.console.print(
        "  [dim]Ratios below compare this protein's amino acid pattern per gram of protein[/dim]",
        highlight=False,
    )
    state.console.print(
        "  [dim]against the FAO adult reference pattern (a fixed quality standard, not a personalized target).[/dim]",
        highlight=False,
    )

    if not result["complete"] and result["limiting_aa"]:
        aa_label, _ = _usda.nutrient_label(result["limiting_aa"])
        state.console.print(f"  Most limiting amino acid: [{state.T['warning']}]{aa_label}[/{state.T['warning']}]")

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 2))
    tbl.add_column("Amino Acid", min_width=18)
    tbl.add_column("Ratio vs. FAO pattern", justify="right", min_width=22)
    for aa_key, score in result["scores"].items():
        label, _ = _usda.nutrient_label(aa_key)
        bar = "█" * min(int(score * 10), 20)
        color = state.T["success"] if score >= 1.0 else state.T["warning"]
        tbl.add_row(label, f"[{color}]{score:.2f}  {bar}[/{color}]")
    state.console.print(tbl)
    state.console.print(
        "  [dim]Interpretation: 1.0 = meets the FAO pattern · >1.0 = exceeds it · <1.0 = limiting[/dim]",
        highlight=False,
    )
    if partial_data_note:
        state.console.print(f"  [dim]{partial_data_note}[/dim]", highlight=False)
    return True


def _print_protein_adequacy(
    nutrients: dict[str, float],
    profile: "_profile.UserProfile",
    *,
    context_label: str | None = None,
) -> None:
    """Print personalized protein adequacy vs. the user's profile-derived target."""
    protein_target = _profile.compute_rda(profile).get("protein_g", (0.0, "g", "minimum"))[0]
    if protein_target <= 0:
        return

    protein_intake = nutrients.get("protein_g", 0.0)
    pct = (protein_intake / protein_target * 100.0) if protein_target > 0 else 0.0
    title = f"Personalized protein adequacy — {context_label}" if context_label else "Personalized protein adequacy"
    state.console.print(f"\n  [{state.T['hi']}]{title}[/{state.T['hi']}]", highlight=False)
    state.console.print(
        f"  [dim]Profile-adjusted protein target: {protein_target:.1f} g/day"
        f"  ({_profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level)})[/dim]",
        highlight=False,
    )
    color = state.T["success"] if pct >= 100 else (state.T["warning"] if pct >= 50 else state.T["error"])
    state.console.print(
        f"  Protein here: [{color}]{protein_intake:.1f} g[/{color}]  [dim]({pct:.0f}% of daily target)[/dim]",
        highlight=False,
    )


def _print_meal_diaas(ingredient_list: list[dict]) -> list[str]:
    """
    Print meal-level DIAAS analysis for a list of ingredients.

    Each dict in ingredient_list must have:
        "food_name":      str
        "nutrients_100g": dict[str, float]
        "grams":          float

    Returns a list of food names that were excluded due to missing AA data.
    Empty list means analysis was complete.
    Callers should suppress complement suggestions when non-empty.
    """
    if not ingredient_list:
        return []

    with _db.get_db() as conn:
        result = _diaas.meal_level_diaas(ingredient_list, conn)

    if result["diaas"] is None:
        if not result["missing_aa_names"]:
            state.console.print(
                "\n  [dim](No amino acid data available for meal-level DIAAS analysis.)[/dim]"
            )
        else:
            state.console.print(
                "\n  [dim](Meal-level DIAAS analysis unavailable — "
                "no amino acid data for any ingredient.)[/dim]"
            )
        return result["missing_aa_names"]

    state.console.print(f"\n  [{state.T['hi']}]Meal-Level DIAAS Complete Protein Analysis[/{state.T['hi']}]"
                  f"  [dim](digestibility-corrected, pooled across foods)[/dim]",
                  highlight=False)
    state.console.rule()

    # Per-food digestibility table
    state.console.print(f"\n  [{state.T['accent_plain']}]Meal Foods: Digestibility Analysis[/{state.T['accent_plain']}]", highlight=False)
    state.console.print()
    state.console.print(
        f"  [dim]Digestibility color key:[/dim]  "
        f"[{state.T['success']}]≥0.90 good[/{state.T['success']}]  "
        f"[{state.T['warning']}]0.80–0.89 fair[/{state.T['warning']}]  "
        f"[{state.T['error']}]<0.80 poor[/{state.T['error']}]",
        highlight=False,
    )
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Food",      min_width=48)
    tbl.add_column("Protein",         justify="right", min_width=8)
    tbl.add_column("Digestibility",   justify="right", min_width=14)
    tbl.add_column("Digestible prot", justify="right", min_width=15)

    for ing in result["ingredients"]:
        p = ing["protein_g"]
        d = ing["digestibility"]
        dig_p = p * d if ing["has_aa_data"] else p  # if no AA data, digestibility still applies to protein
        source_tag = ""
        src = ing["dig_source"]
        if "user override" in src:
            source_tag = f"  [dim]↑ user[/dim]"
        elif "category estimate" in src or "default estimate" in src:
            source_tag = f"  [dim]~est[/dim]"
        color = state.T["success"] if d >= 0.90 else (state.T["warning"] if d >= 0.80 else state.T["error"])
        tbl.add_row(
            ing["food_name"][:50],
            f"{p:.1f}g",
            f"[{color}]{d:.2f}[/{color}]{source_tag}",
            f"{dig_p:.1f}g",
        )
    state.console.print()
    state.console.print(tbl, highlight=False)

    total_dig_p = sum(
        ing["protein_g"] * ing["digestibility"] if ing["has_aa_data"] else ing["protein_g"]
        for ing in result["ingredients"]
    )
    state.console.print(
        f"  [dim]Total digestible protein (before meal-level AA analysis): "
        f"[bold]{total_dig_p:.1f}g[/bold][/dim]",
        highlight=False,
    )

    # IAA composite ratio table
    iaa_ratios = result["iaa_ratios"]
    if iaa_ratios:
        state.console.print(
            f"\n  [{state.T['accent_plain']}]Meal Amino Acid Ratios for DIAAS[/{state.T['accent_plain']}]"
            f"  [dim](≥1.0 = meets reference  |  color:[/dim]"
            f"  [{state.T['success']}]≥1.0[/{state.T['success']}]"
            f"  [{state.T['warning']}]0.80–0.99[/{state.T['warning']}]"
            f"  [{state.T['error']}]<0.80[/{state.T['error']}]",
            highlight=False,
        )
        aa_tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        aa_tbl.add_column("Amino Acid", min_width=14)
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
            limiting_tag = f"  [dim]← LIMITING[/dim]" if is_limiting else ""
            aa_tbl.add_row(
                label,
                f"[{color}]{ratio:.3f}[/{color}]{limiting_tag}",
                f"[{color}]{bar}[/{color}]",
            )

        if result["phe_tyr_gap"]:
            aa_tbl.add_row("[dim]Phe+Tyr[/dim]", "[dim]n/a[/dim]",
                           "[dim](tyrosine absent from USDA data)[/dim]")
        state.console.print()
        state.console.print(aa_tbl, highlight=False)

    # Summary line
    diaas_val = result["diaas"]
    dcp = result["digestible_complete_protein_g"]
    total_p = result["total_protein_g"]
    color = state.T["success"] if diaas_val >= 1.0 else (state.T["warning"] if diaas_val >= 0.80 else state.T["error"])
    eff_pct = min(diaas_val, 1.0) * 100

    state.console.print(
        f"\n  Composite DIAAS: [{color}]{diaas_val:.3f}[/{color}]"
        f"  [dim](utilization efficiency: {eff_pct:.0f}%)[/dim]",
        highlight=False,
    )
    if dcp is not None:
        state.console.print(
            f"  Digestible complete protein: [{color}]{dcp:.1f}g[/{color}]"
            f"  [dim]from {total_p:.1f}g total[/dim]",
            highlight=False,
        )

    if result["missing_aa_names"]:
        state.console.print(
            f"\n  [{state.T['warning']}]⚠  DIAAS figure above is unreliable[/{state.T['warning']}] — "
            f"{len(result['missing_aa_names'])} of your ingredients have no amino acid profile\n"
            f"  in the USDA database and were excluded from the calculation:",
            highlight=False,
        )
        # Build protein lookup from ingredient results for context
        protein_by_name = {
            ing["food_name"]: ing.get("protein_g", 0.0)
            for ing in result.get("ingredients", [])
        }
        for name in result["missing_aa_names"]:
            protein = protein_by_name.get(name, 0.0)
            protein_str = f"  [dim]({protein:.1f}g protein)[/dim]" if protein > 0 else "  [dim](trace protein)[/dim]"
            state.console.print(f"    • {name}{protein_str}")

    if result["estimate_sources"]:
        state.console.print(
            f"\n  [dim]  Digestibility estimated (literature average) for: "
            f"{', '.join(result['estimate_sources'][:4])}"
            + (f" + {len(result['estimate_sources']) - 4} more" if len(result["estimate_sources"]) > 4 else "")
            + "[/dim]",
            highlight=False,
        )

    return result["missing_aa_names"]

def _print_recipe_bioavailability(
    ingredient_stats: list[dict],  # [{"name": str, "protein_g": float, "diaas": float|None}]
    analysis_nutrients: dict[str, float],
) -> None:
    """Print per-ingredient DIAAS breakdown and total digestible protein for a recipe."""
    total_protein = analysis_nutrients.get("protein_g", 0.0)
    if total_protein <= 0:
        return

    state.console.print(f"\n  [{state.T['hi']}]Bioavailability — per serving[/{state.T['hi']}]"
                  f"  [dim](DIAAS: [{state.T['success']}]≥0.90 good[/{state.T['success']}]"
                  f" · [{state.T['warning']}]≥0.70 moderate[/{state.T['warning']}]"
                  f" · [{state.T['error']}]<0.70 poor[/{state.T['error']}])[/dim]",
                  highlight=False)

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 2))
    tbl.add_column("Ingredient", min_width=32)
    tbl.add_column("Protein", justify="right", min_width=8)
    tbl.add_column("DIAAS", justify="right", min_width=7)
    tbl.add_column("Digestible", justify="right", min_width=10)

    total_digestible = 0.0
    unknown_count = 0
    for s in ingredient_stats:
        p = s["protein_g"]
        diaas = s["diaas"]
        if diaas is not None:
            dig = p * diaas
            score = diaas
            diaas_str = f"{diaas:.2f}"
        else:
            dig = p
            score = 1.0
            diaas_str = "?"
            unknown_count += 1
        total_digestible += dig
        color = state.T["success"] if score >= 0.90 else (state.T["warning"] if score >= 0.70 else state.T["error"])
        tbl.add_row(
            s["name"][:34],
            f"{p:.1f}g",
            f"[{color}]{diaas_str}[/{color}]",
            f"{dig:.1f}g",
        )

    state.console.print(tbl, highlight=False)

    eff_diaas = total_digestible / total_protein if total_protein > 0 else 0.0
    color = state.T["success"] if eff_diaas >= 0.90 else (state.T["warning"] if eff_diaas >= 0.70 else state.T["error"])
    state.console.print(
        f"  Total digestible protein: [{state.T['hi']}]{total_digestible:.1f}g[/{state.T['hi']}]"
        f"  [dim](from {total_protein:.1f}g, effective DIAAS [{color}]{eff_diaas:.2f}[/{color}])[/dim]",
        highlight=False,
    )
    if unknown_count:
        state.console.print(
            f"  [dim]  ({unknown_count} ingredient(s) had no DIAAS data — assumed fully digestible)[/dim]",
            highlight=False,
        )


def _print_bioavailability(food_name: str, nutrients: dict[str, float]) -> None:
    """Print DIAAS-adjusted protein and anti-nutrient flags for a single food."""
    diaas = _usda.get_diaas(food_name)
    flags = _usda.get_antinutrient_flags(food_name)

    if diaas is None and not flags:
        return

    state.console.print(f"\n  [{state.T['hi']}]Bioavailability[/{state.T['hi']}]")

    if diaas is not None:
        protein_raw = nutrients.get("protein_g", 0.0)
        protein_adj = protein_raw * diaas
        bar_len = min(int(diaas * 20), 20)
        color = state.T["success"] if diaas >= 0.90 else (state.T["warning"] if diaas >= 0.70 else state.T["error"])
        state.console.print(
            f"  Protein digestibility (DIAAS): [{color}]{diaas:.2f}  "
            f"{'█' * bar_len}[/{color}]"
        )
        if protein_raw > 0:
            state.console.print(
                f"  Digestible protein: [{state.T['hi']}]{protein_adj:.1f}g[/{state.T['hi']}]"
                f"  [dim](from {protein_raw:.1f}g raw)[/dim]"
            )
            pc = _usda.protein_completeness(nutrients)
            if pc.get("has_data"):
                limiting_score = min(pc["scores"].values())
                dig_complete = protein_adj * min(1.0, limiting_score)
                if pc.get("complete"):
                    state.console.print(
                        f"  Digestible complete protein: [{state.T['success']}]{dig_complete:.1f}g[/{state.T['success']}]"
                        f"  [dim](protein is complete)[/dim]"
                    )
                else:
                    limiting_label = _usda.nutrient_label(pc["limiting_aa"])[0] if pc.get("limiting_aa") else "?"
                    state.console.print(
                        f"  Digestible complete protein: [{state.T['warning']}]{dig_complete:.1f}g[/{state.T['warning']}]"
                        f"  [dim](limited by {limiting_label} — score {limiting_score:.2f})[/dim]"
                    )

    for flag in flags:
        state.console.print(f"  [{state.T['warning']}]Note:[/{state.T['warning']}] "
                      f"{flag['problem']} — {flag['cause']}")
        for label, sol in flag["solutions"]:
            state.console.print(f"    [dim]* {label}: {sol}[/dim]")

def _volume_hint(grams: float, food_name: str) -> str | None:
    """Return a human-readable volume equivalent for *grams* of *food_name*, or None."""
    density = _usda.get_density_g_per_ml(food_name, [])
    if density is None:
        return None
    ml = grams / density
    # Standard measuring cup fractions (value, unicode glyph)
    _CUP_FRACS = [
        (0.125, "1/8"), (0.25, "1/4"), (0.333, "1/3"),
        (0.5, "1/2"),   (0.667, "2/3"), (0.75, "3/4"),
    ]
    if ml >= 29.6:  # ≥ 2 tbsp — show in cups or tbsp
        cups = ml / 236.6
        whole = int(cups)
        frac = cups - whole
        if frac < 0.063:
            frac_str = ""
        elif frac > 0.875:
            whole += 1
            frac_str = ""
        else:
            frac_str = min(_CUP_FRACS, key=lambda f: abs(f[0] - frac))[1]
        if whole == 0 and not frac_str:
            # Less than ⅛ cup but ≥ 2 tbsp — fall through to tbsp display
            tbsp = ml / 14.8
            rounded = round(tbsp * 2) / 2
            val = f"{rounded:.1f}".rstrip("0").rstrip(".")
            return f"≈ {val} tbsp"
        cup_str = (frac_str if whole == 0 else
                   f"{whole} {frac_str}" if frac_str else str(whole))
        unit = "cup" if whole <= 1 and not (whole == 1 and frac_str) else "cups"
        return f"≈ {cup_str} {unit}"
    elif ml >= 4.9:  # ≥ 1 tsp
        tbsp = ml / 14.8
        if tbsp >= 1:
            rounded = round(tbsp * 2) / 2
            val = f"{rounded:.1f}".rstrip("0").rstrip(".")
            return f"≈ {val} tbsp"
        tsp = ml / 4.9
        rounded = round(tsp * 4) / 4
        val = f"{rounded:.2f}".rstrip("0").rstrip(".")
        return f"≈ {val} tsp"
    return None  # too small to be useful


def _print_complement_suggestions(
    base_nutrients: dict[str, float],
    context: str = "meal",  # "recipe", "meal", "daily", "food"
    offer_if_covered: bool = False,  # kept for call-site compat, no longer used
    base_food_name: str | None = None,
    basis_label: str | None = None,  # e.g. "per serving" or "whole recipe (7 servings)"
) -> None:
    """
    Display protein complement suggestions.
    context: controls framing text ("add to recipe" vs "add to meal" etc.)
    base_food_name: when provided, used to look up DIAAS for the base food so
                    the total digestible protein line is accurate.
    basis_label: appended to the section header to clarify what the gram amounts refer to.
    """
    gaps = _usda.get_aa_gaps(base_nutrients)
    if not gaps:
        state.console.print(f"\n  [{state.T['hi']}]Protein Complement Suggestions[/{state.T['hi']}]")
        state.console.print("  [dim]No complement suggestions are needed.[/dim]")
        return

    try:
        pantry = _load_pantry_candidates()
    except Exception:
        pantry = []
    suggestions = _usda.suggest_complements(
        base_nutrients, pantry, exclude_animal=not state._include_animal_foods
    )

    base_protein = base_nutrients.get("protein_g", 0.0)
    base_diaas = _usda.get_diaas(base_food_name) if base_food_name else None
    base_digestible = base_protein * base_diaas if base_diaas else base_protein

    pantry_suggs = suggestions["pantry"]
    general_suggs = suggestions["general"]

    if pantry is None:
        pantry = []

    if not pantry:
        state.console.print(
            "[dim](No pantry items saved yet — add protein sources via Foods → My Pantry.)[/dim]"
        )
    elif not pantry_suggs:
        state.console.print(
            "[dim](Pantry items found but none qualify: their amino acid/protein ratio "
            "for the limiting amino acid falls below the FAO reference.)[/dim]"
        )

    def _ranking_key(s: dict) -> tuple[float, float, str]:
        grams = float(s.get("grams", 10**9) or 10**9)
        complete_bonus = 0.0 if s.get("new_complete", False) else 1.0
        digestible = -float(s.get("digestible_protein_added", 0.0) or 0.0)
        return (complete_bonus, grams, digestible)

    pantry_suggs = sorted(pantry_suggs, key=_ranking_key)
    general_suggs = sorted(general_suggs, key=_ranking_key)

    # Determine whether pantry adequately covers all gaps
    pantry_covers = bool(pantry_suggs and pantry_suggs[0].get("new_complete", False))

    basis_tag = f"  [dim]— {basis_label}[/dim]" if basis_label else ""
    state.console.print(f"\n  [{state.T['hi']}]Protein complement suggestions[/{state.T['hi']}]{basis_tag}",
                        highlight=False)
    state.console.print("  [dim]Ranked by the smallest practical amount needed to close the main amino acid gap.[/dim]")
    gap_labels = ", ".join(
        _usda.nutrient_label(aa)[0] + f" ({score:.2f})"
        for aa, score, _ in gaps
    )
    state.console.print(f"  [dim]Gaps: {gap_labels}[/dim]")

    if context == "recipe":
        add_verb = "Add to recipe"
        pair_verb = "Serve alongside"
    elif context == "daily":
        add_verb = "Add to your day"
        pair_verb = "Pair with a meal"
    elif context == "food":
        add_verb = "Add to food above"
        pair_verb = "Serve alongside"
    else:
        add_verb = "Add to meal"
        pair_verb = "Serve alongside"

    def _show_suggestion(s: dict, label: str) -> None:
        diaas_str = f"  [dim]DIAAS {s['diaas']:.2f}[/dim]" if s.get("diaas") else ""
        state.console.print(f"\n  [{state.T['accent']}]{label}[/{state.T['accent']}] "
                      f"[bold]{s['name']}[/bold]{diaas_str}")
        vol = _volume_hint(s["grams"], s["name"])
        vol_str = f"  [dim]({vol})[/dim]" if vol else ""
        state.console.print(f"    {add_verb}: [bold]{s['grams']}g[/bold]{vol_str}")
        # Show AA scores before → after for the most affected gaps
        score_parts = []
        for aa, orig_score, _ in gaps[:3]:
            new_score = s["new_scores"].get(aa, orig_score)
            label_aa, _ = _usda.nutrient_label(aa)
            arrow = f"[{state.T['success']}]{new_score:.2f}[/{state.T['success']}]" if new_score >= 1.0 \
                else f"[{state.T['warning']}]{new_score:.2f}[/{state.T['warning']}]"
            score_parts.append(f"{label_aa}: {orig_score:.2f}→{arrow}")
        state.console.print(f"    Effect: {' · '.join(score_parts)}")
        dig = s["digestible_protein_added"]
        raw = s["protein_added"]
        state.console.print(f"    Adds: [bold]{dig:.1f}g[/bold] digestible protein "
                      f"[dim](from {raw:.1f}g raw)[/dim]")
        total_dig = base_digestible + dig
        state.console.print(f"    Total bioavailable complete protein now = "
                      f"[{state.T['success']}]{total_dig:.1f}g[/{state.T['success']}]")
        if s.get("opens_new_gap"):
            state.console.print(f"    [{state.T['warning']}]Note: closes the above gap but opens a new one "
                          f"— consider layering with a second complement.[/{state.T['warning']}]")
        if context == "recipe":
            state.console.print(f"    [dim]{pair_verb}: serve {s['grams']}g alongside[/dim]")

    def _show_paged(suggs: list[dict], section_label: str, page_size: int = 3) -> None:
        """Display suggestions in pages of page_size, prompting for more after each."""
        if not suggs:
            return
        state.console.print(f"\n  [dim]— {section_label} —[/dim]")
        offset = 0
        while offset < len(suggs):
            batch = suggs[offset:offset + page_size]
            for i, s in enumerate(batch, offset + 1):
                _show_suggestion(s, f"Option {i}")
            offset += page_size
            if offset < len(suggs):
                try:
                    ans = _prompt(
                        f"More suggestions?  [dim]({len(suggs) - offset} remaining — y/N)[/dim]",
                        default="n").strip().lower()
                except Cancelled:
                    break
                if ans != "y":
                    break

    # Per-AA note about which common foods typically fall below the FAO reference
    # and therefore cannot close that gap regardless of quantity.
    _AA_LOW_IN: dict[str, str] = {
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

    def _general_exhausted_msg(n_shown: int) -> None:
        limiting_aa = gaps[0][0] if gaps else None
        limiting_label = _usda.nutrient_label(limiting_aa)[0] if limiting_aa else "this amino acid"
        low_in = _AA_LOW_IN.get(limiting_aa or "", "many plant foods")
        prefix = "These are all qualifying options." if n_shown > 0 \
                 else "No qualifying options found in the database."
        state.console.print(
            f"\n  [dim]{prefix}[/dim]\n"
            f"  [dim]A qualifying complement must have a {limiting_label}/protein ratio above[/dim]\n"
            f"  [dim]the FAO reference to close the gap to score 1.0 in a practical serving (≤ 500g).[/dim]\n"
            f"  [dim]Score 1.0 = meets human requirements (the floor, not an aspirational target).[/dim]\n"
            f"  [dim]Foods that don't qualify for a {limiting_label} gap: {low_in}.[/dim]\n"
            f"  [dim]Their ratio falls below the reference — adding them dilutes the score further.[/dim]"
        )

    if pantry_suggs:
        _show_paged(pantry_suggs, "From your pantry")
        if general_suggs:
            try:
                ans = _prompt("Look elsewhere for more options?  [dim](y/N)[/dim]",
                              default="n").strip().lower()
            except Cancelled:
                return
            if ans == "y":
                _show_paged(general_suggs, "Other good options", page_size=5)
                _general_exhausted_msg(len(general_suggs))
        else:
            _general_exhausted_msg(0)
    else:
        if general_suggs:
            _show_paged(general_suggs, "Other good options", page_size=5)
            _general_exhausted_msg(len(general_suggs))
        else:
            _general_exhausted_msg(0)

def _print_rda_comparison(nutrients: dict[str, float], profile: "_profile.UserProfile") -> None:
    """Print a table comparing daily nutrient totals against personalized RDA targets."""
    rda = _profile.compute_rda(profile)
    nutrient_label = _usda.nutrient_label  # (key) → (label, unit) | None

    state.console.print(f"\n[{state.T['accent']}]Daily Intake vs. Recommended Values[/{state.T['accent']}]")
    state.console.rule()
    state.console.print(
        f"  Profile: age {profile.age}  ·  {profile.sex}"
        f"  ·  {_profile.format_weight(profile.weight_kg, profile.weight_unit)}"
        f"  ·  {_profile.format_height(profile.height_cm, profile.height_unit)}"
        f"  ·  {_profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level)}\n",
        highlight=False,
    )

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Nutrient",  min_width=26)
    tbl.add_column("Intake",    justify="right", min_width=12)
    tbl.add_column("Target",    justify="right", min_width=12)
    tbl.add_column("% of RDA",  justify="right", min_width=10)
    tbl.add_column("Status",    min_width=28)

    BAR_WIDTH = 16

    for key, (rda_val, unit, rda_type) in rda.items():
        intake = nutrients.get(key, 0.0)
        label_info = nutrient_label(key)
        label = label_info[0] if label_info else key.replace("_", " ").title()

        if rda_val and rda_val > 0:
            pct = (intake / rda_val) * 100.0
        else:
            pct = 0.0

        # Format intake and target
        if unit in ("kcal", "g"):
            intake_str = f"{intake:.1f} {unit}"
            target_str = f"{rda_val:.1f} {unit}"
        else:
            intake_str = f"{intake:.1f} {unit}"
            target_str = f"{rda_val:.1f} {unit}"
        pct_str = f"{pct:.0f}%"

        # Status bar and color
        if rda_type == "limit":
            # For limits: green if under, yellow if near (80-100%), red if over
            if pct <= 80:
                bar_color = state.T["success"]
                status_note = "within limit"
            elif pct <= 100:
                bar_color = state.T["warning"]
                status_note = "approaching limit"
            else:
                bar_color = state.T["error"]
                status_note = f"over limit by {pct - 100:.0f}%"
            filled = min(int(BAR_WIDTH * min(pct, 200) / 200), BAR_WIDTH)
        else:
            # For minimums/targets: red < 70%, yellow 70-99%, green 100%+
            if pct >= 100:
                bar_color = state.T["success"]
                status_note = "met"
            elif pct >= 70:
                bar_color = state.T["warning"]
                status_note = f"{100 - pct:.0f}% short"
            else:
                bar_color = state.T["error"]
                status_note = f"{100 - pct:.0f}% short"
            filled = min(int(BAR_WIDTH * min(pct, 100) / 100), BAR_WIDTH)

        bar = f"[{bar_color}]{'█' * filled}[/{bar_color}]{'░' * (BAR_WIDTH - filled)}"
        status_cell = f"{bar}  [{bar_color}]{status_note}[/{bar_color}]"

        tbl.add_row(label, intake_str, target_str, pct_str, status_cell)

    state.console.print(tbl, highlight=False)
    state.console.print(
        "  [dim]Target = RDA or Adequate Intake  ·  Limit = Tolerable Upper Intake Level[/dim]\n"
    )
