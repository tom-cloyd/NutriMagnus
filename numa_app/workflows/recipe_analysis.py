"""
recipe_analysis.py — recipe nutrition analysis workflow for numa.

Contains _resolve_recipe_dcp_data, helper converters, and _do_recipe_view
(menu option 5 "Analyze recipe").  Called from recipes.py.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/recipe_analysis.py — analyze recipe workflow"
"""
import json
from datetime import datetime, timezone
from typing import Literal

import export as _export

import diaas as _diaas
from rich.rule import Rule
from rich.table import Table

import db as _db
import usda as _usda
import profile as _profile
from .. import state
from ..services.portions import _normalize_unit_display, _parse_portion_input, _pick_portion, _try_resolve_unknown_weight, _UNIT_TO_GRAMS, _VOLUME_TO_ML
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food, _simplify_food_query
from ..services.reports import _offer_export
from ..ui.common import _id_cell, ID_KEY, _safe_call, _show_menu, section_title, help_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import (
    _print_complement_suggestions, _get_daily_context, _print_nutrient_table,
    _print_protein_adequacy, _print_protein_completeness, _print_recipe_bioavailability,
    _print_dcp_adequacy_section,
)
from .recipes import (
    _pick_recipe_portion, _compute_recipe_dcp, _compute_recipe_gl,
    _augment_aa_from_curated, _format_recipe_portion_label, _recipe_ing_id_cell,
)

def _resolve_recipe_dcp_data(
    recipe_id: int,
    ingredients: list,
    ingredient_stats: list[dict],
    combined: dict[str, float],
    resolved_ing_ids: set[int] | None = None,
) -> tuple[list[dict], dict[str, float], bool, list[str]] | Literal["rerun", "back"] | None:
    """
    Detect missing data that blocks or degrades DCP calculation.
    Prompts the user to provide data, calculate with assumptions, or skip.

    Returns (updated_stats, updated_combined, approximate, notes) on success.
    Returns None if the user chooses to skip DCP entirely.
    Returns "rerun" if ingredients were replaced and _do_recipe_view should restart.
    Returns "back" if the user cancelled out (caller should return immediately).
    """
    zero_weight = [
        ing for ing in ingredients
        if "(weight not known)" in (ing["unit"] or "")
        and ing["id"] not in (resolved_ing_ids or set())
    ]
    no_aa_ings  = [s for s in ingredient_stats if not s.get("has_aa", True)
                   and s.get("protein_g", 0) >= 0.1]
    pc          = _usda.protein_completeness(combined)
    no_aa       = not pc.get("has_data")

    if not zero_weight and not no_aa and not no_aa_ings:
        return ingredient_stats, combined, False, []

    state.console.print(f"\n  [{state.T['warning']}]⚠  Missing data for digestible complete protein (DCP):[/{state.T['warning']}]")
    for ing in zero_weight:
        state.console.print(f"    • {ing['food_name']} — weight unknown ({_normalize_unit_display(ing['unit'])})")
    if no_aa and not no_aa_ings:
        state.console.print("    • No amino acid profile available in USDA data for these ingredients.")
    if no_aa_ings:
        for s in no_aa_ings:
            state.console.print(f"    • {s['name']} — no amino acid profile in USDA data")
    state.console.print(
        f"  [grey62]If any flagged ingredient is not a significant protein source "
        f"(e.g. spices, oil, salt), its missing data can safely be ignored.[/grey62]"
    )

    # Build numbered options dynamically, preserving the action key internally
    action_items: list[tuple[str, str]] = []  # (action_key, label)
    if no_aa_ings:
        action_items.append(("f", "Fix: replace affected ingredients via Foundation Foods search"))
    if zero_weight:
        action_items.append(("p", "Provide missing data now"))
    action_items.append(("c", "Calculate anyway  (result flagged as approximate)"))
    action_items.append(("s", "Skip DCP calculation"))

    numbered: list[tuple[str, str]] = [(str(i + 1), label) for i, (_, label) in enumerate(action_items)]
    numbered.append(("b", "Back to previous menu"))
    numbered.append(("m", "Return to main menu"))
    numbered.append(("q", "Quit"))
    valid_nums = {str(i + 1) for i in range(len(action_items))}

    while True:
        _show_menu("Options", numbered)
        while True:
            try:
                choice = _prompt("Choice").strip().lower()
            except Cancelled:
                return "back"
            if choice in valid_nums or choice in ("b", "m", "q"):
                break
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")

        if choice == "b":
            return "back"  # type: ignore[return-value]
        if choice == "m":
            raise ReturnToMain()
        if choice == "q":
            raise SystemExit(0)

        # Map number back to action key
        action = action_items[int(choice) - 1][0]

        if action == "s":
            return None

        if action == "f":
            # Replace each affected ingredient with a Foundation Foods version
            affected_names = {s["name"].lower() for s in no_aa_ings}
            with _db.get_db() as conn:
                all_ings = _db.recipe_get_ingredients(conn, recipe_id)
            replaced_any = False
            for ing in all_ings:
                if ing["food_name"].lower() not in affected_names:
                    continue
                suggested = _simplify_food_query(ing["food_name"].split(",")[0].strip())
                state.console.print(
                    f"\n  Replacing: [{state.T['accent']}]{ing['food_name']}[/{state.T['accent']}]\n"
                    f"  [grey62]Suggested search: '{suggested}'[/grey62]"
                )
                try:
                    raw_sq = _prompt(
                        "Search Foundation Foods + SR Legacy  [grey62](Enter to use suggestion · b=skip)[/grey62]",
                        free_text=True,
                    ).strip()
                except Cancelled:
                    state.console.print("  [grey62]Skipped.[/grey62]")
                    continue
                if raw_sq.lower() in ("b", "back"):
                    state.console.print("  [grey62]Skipped.[/grey62]")
                    continue
                search_query = raw_sq or suggested
                food = _search_and_pick_food(
                    data_types=["Foundation", "SR Legacy"],
                    initial_query=search_query,
                    show_aa_status=True,
                    allow_research=True,
                )
                if food is None:
                    state.console.print("  [grey62]Skipped.[/grey62]")
                    continue
                orig_label = _normalize_unit_display(ing["unit"]) if ing["unit"] else None
                if ing["amount"] and ing["amount"] > 0:
                    orig_str = f"{ing['amount']:g} g"
                    if orig_label and orig_label != "—":
                        orig_str = f"{orig_label}  ({ing['amount']:g} g)"
                    state.console.print(f"  [grey62]Original amount: [bold]{orig_str}[/bold][/grey62]")
                result = _pick_portion(food)
                if result is None:
                    state.console.print("  [grey62]Skipped.[/grey62]")
                    continue
                grams, label, _ = result
                with _db.get_db() as conn:
                    _db.recipe_remove_ingredient(conn, ing["id"])
                    _db.recipe_add_ingredient(conn, recipe_id, food["fdcId"], food["name"], grams, label)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Replaced with: {food['name']}  {label}")
                replaced_any = True
            if replaced_any:
                return "rerun"
            return None

        approximate = False
        notes: list[str] = []

        if action == "p":
            new_combined  = dict(combined)
            new_stats     = list(ingredient_stats)
            _back = False

            for ing in zero_weight:
                vol_display = _normalize_unit_display(ing["unit"]).replace(" (weight not known)", "")
                state.console.print(f"\n  [{state.T['accent']}]{ing['food_name']}[/{state.T['accent']}]"
                              f"  [grey62]({vol_display})[/grey62]")
                try:
                    w_raw = _prompt("Weight in grams  (Enter=skip, b=back)", free_text=True).strip()
                except Cancelled:
                    w_raw = ""
                if w_raw.lower() == "q":
                    raise SystemExit(0)
                if w_raw.lower() == "b":
                    _back = True
                    break
                if w_raw and w_raw.lower() != "s":
                    try:
                        grams = float(w_raw)
                        with _db.get_db() as conn:
                            cached = _db.get_cached_food(conn, ing["fdc_id"])
                        if cached:
                            nuts_100g = json.loads(cached["nutrients_json"])
                            scaled = _usda.scale_nutrients(nuts_100g, grams, base_size=100.0)
                            new_combined = _usda.sum_nutrients(new_combined, scaled)
                            p = scaled.get("protein_g", 0.0)
                            if p > 0:
                                pc_ing = _usda.protein_completeness(scaled)
                                new_stats.append({
                                    "name": ing["food_name"],
                                    "fdc_id": ing["fdc_id"],
                                    "protein_g": p,
                                    "amount_g": grams,
                                    "nutrients_100g": nuts_100g,
                                    "diaas": _usda.get_diaas(ing["food_name"]),
                                    "has_aa": pc_ing.get("has_data", False),
                                    "limiting_aa": pc_ing.get("limiting_aa"),
                                })
                        notes.append(f"{ing['food_name']}: {grams:.0f}g (user-provided, not saved)")
                        approximate = True  # user-supplied value, not from DB
                    except ValueError:
                        approximate = True
                        notes.append(f"{ing['food_name']}: skipped (invalid weight)")
                else:
                    approximate = True
                    notes.append(f"{ing['food_name']}: excluded (weight not provided)")

            if _back:
                continue  # re-show the options menu

            return new_stats, new_combined, approximate, notes

        else:  # action == "c" — calculate anyway
            approximate = True
            for ing in zero_weight:
                notes.append(f"{ing['food_name']}: excluded (weight not known)")
            if no_aa:
                notes.append("amino acid completeness: unknown — no AA data in USDA cache")
            return ingredient_stats, combined, True, notes


def _recipe_weight_to_g(amount: float | None, unit: str | None) -> float | None:
    """Convert a recipe total_weight value to grams. Returns None if unknown."""
    if amount is None or amount <= 0:
        return None
    if not unit:
        return float(amount)          # assume grams
    factor = _UNIT_TO_GRAMS.get(unit.strip().lower())
    return amount * factor if factor is not None else None


def _recipe_vol_to_ml(amount: float | None, unit: str | None) -> float | None:
    """Convert a recipe total_volume value to ml. Returns None if unknown."""
    if amount is None or amount <= 0:
        return None
    if not unit:
        return float(amount)          # assume ml
    u = unit.strip().lower()
    # _VOLUME_TO_ML keys are case-sensitive (T vs t); check original case first
    factor = _VOLUME_TO_ML.get(unit.strip()) or _VOLUME_TO_ML.get(u)
    return amount * factor if factor is not None else None


def _do_recipe_view(recipe=None, *, save_analysis: bool = False) -> None:
    if recipe is None:
        from .recipes import _pick_recipe
        recipe = _pick_recipe()
    if recipe is None:
        return
    rid = recipe["id"]
    with _db.get_db() as conn:
        _db.recipe_touch(conn, rid)
    with _db.get_db() as conn:
        for _ing in _db.recipe_get_ingredients(conn, rid):
            if _ing["fdc_id"] and not _ing["ref_recipe_id"]:
                _try_resolve_unknown_weight(conn, _ing)
    with _db.get_db() as conn:
        ingredients = _db.recipe_get_ingredients(conn, rid)

    if not ingredients:
        state.console.print("[grey62]This recipe has no ingredients.[/grey62]")
        return

    while True:
        # Reload recipe + ingredients on rerun (ingredients may have been replaced)
        with _db.get_db() as conn:
            recipe     = _db.recipe_get(conn, rid)
            ingredients = _db.recipe_get_ingredients(conn, rid)

        srv_tag = (
            "[grey62]whole recipe[/grey62]"
            if recipe["servings"] == 0
            else f"[grey62]{recipe['servings']} serving(s)[/grey62]"
        )
        state.console.print(
            f"\n[{state.T['accent']}]{recipe['name']}[/{state.T['accent']}]  {srv_tag}"
        )
        if recipe["description"]:
            state.console.print(f"  {recipe['description']}")

        # Ingredient list with amounts — shown before DCP prompts so user can see the recipe
        state.console.print(f"\n[{state.T['accent']}]Ingredients:[/{state.T['accent']}]  {ID_KEY}")
        for ing in ingredients:
            note_tag = f"  [grey62]({ing['notes']})[/grey62]" if ing["notes"] else ""
            amt = (_format_recipe_portion_label(ing["amount"])
                   if ing["ref_recipe_id"] else _normalize_unit_display(ing["unit"]))
            state.console.print(f"  • {amt}  {_recipe_ing_id_cell(ing)}  {ing['food_name']}{note_tag}")

        state.console.print(f"\n[{state.T['accent']}]Procedure:[/{state.T['accent']}]")
        if recipe["instructions"] and recipe["instructions"].strip():
            state.console.print(f"  {recipe['instructions']}")
        else:
            state.console.print("  [grey62](none given)[/grey62]")
        state.console.print(Rule(), width=min(100, state.console.width))

        # Build combined nutrients and per-ingredient protein+DIAAS (silent — before display)
        with state.console.status("[grey62]Analysis being computed...[/grey62]"):
            combined: dict[str, float] = {}
            ingredient_stats: list[dict] = []
            volume_only_warnings: list[str] = []   # ingredients where weight couldn't be derived
            resolved_ing_ids: set[int] = set()     # volume ingredients successfully converted to grams
            for ing in ingredients:
                if ing["ref_recipe_deleted"]:
                    volume_only_warnings.append(
                        f"{ing['food_name']} — this sub-recipe was deleted; excluded from totals"
                    )
                    continue
                if ing["ref_recipe_id"]:
                    from .recipes import _get_recipe_total_nutrients  # lazy — avoids circular import
                    _, _, sub_nutrients = _get_recipe_total_nutrients(ing["ref_recipe_id"])
                    with _db.get_db() as conn:
                        sub_recipe = _db.recipe_get(conn, ing["ref_recipe_id"])
                    if sub_recipe and sub_nutrients and sub_recipe["servings"] and sub_recipe["servings"] > 0:
                        scale = ing["amount"] / sub_recipe["servings"]
                        scaled = {k: v * scale for k, v in sub_nutrients.items()}
                        combined = _usda.sum_nutrients(combined, scaled)
                        sub_protein = scaled.get("protein_g", 0.0)
                        if sub_protein > 0:
                            ingredient_stats.append({
                                "name": ing["food_name"],
                                "fdc_id": None,
                                "amount_g": 100.0,      # normalization sentinel: DIAAS math = scaled * 100/100
                                "display_g": None,       # render shows "—" in Serving column
                                "protein_g": sub_protein,
                                "nutrients_100g": scaled,   # absolute scaled nutrients treated as per-100g basis
                                "diaas": None,
                                "has_aa": _usda.has_amino_acid_data(scaled),
                                "limiting_aa": None,
                            })
                    continue
                amount = ing["amount"]
                # amount=0 means no explicit weight was entered — try to derive from the unit string
                if amount == 0.0 and ing["unit"]:
                    _refresh_cache_if_missing_aa(ing["fdc_id"])
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, ing["fdc_id"])
                    portions = json.loads(cached["portions_json"]) if cached else []
                    unit_str = ing["unit"].replace(" (weight not known)", "").strip()
                    result = _parse_portion_input(unit_str, portions, food_name=ing["food_name"])
                    if result is not None:
                        derived_g, _ = result
                        if derived_g and derived_g > 0:
                            amount = derived_g
                            resolved_ing_ids.add(ing["id"])
                        else:
                            volume_only_warnings.append(
                                f"{ing['food_name']} ({ing['unit']}) — no density (weight) data to convert volume to grams"
                            )
                            continue
                    else:
                        volume_only_warnings.append(
                            f"{ing['food_name']} ({ing['unit']}) — could not parse unit"
                        )
                        continue
                elif amount == 0.0:
                    continue   # no weight and no unit — silently skip
                else:
                    _refresh_cache_if_missing_aa(ing["fdc_id"])
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, ing["fdc_id"])
                if cached:
                    nuts_100g = json.loads(cached["nutrients_json"])
                    scaled = _usda.scale_nutrients(nuts_100g, amount, base_size=100.0)
                    combined = _usda.sum_nutrients(combined, scaled)
                    ing_protein = scaled.get("protein_g", 0.0)
                    if ing_protein > 0:
                        pc = _usda.protein_completeness(scaled)
                        ingredient_stats.append({
                            "name": ing["food_name"],
                            "fdc_id": ing["fdc_id"],
                            "amount_g": amount,
                            "protein_g": ing_protein,
                            "nutrients_100g": nuts_100g,
                            "diaas": _usda.get_diaas(ing["food_name"]),
                            "has_aa": pc.get("has_data", False),
                            "limiting_aa": pc.get("limiting_aa"),
                        })
        # end of spinner context — warnings and DCP resolution follow
        if volume_only_warnings:
            state.console.print(
                f"\n  [{state.T['warning']}]⚠  Could not compute weight for the following ingredients "
                f"— they are excluded from the analysis:[/{state.T['warning']}]"
            )
            for w in volume_only_warnings:
                state.console.print(f"    [grey62]• {w}[/grey62]")

        # Resolve missing DCP data before displaying tables so totals reflect any user input
        dcp_skip = False
        dcp_approximate = False
        dcp_notes: list[str] = []
        if combined:
            resolved = _resolve_recipe_dcp_data(recipe["id"], ingredients, ingredient_stats, combined, resolved_ing_ids)
            if resolved == "rerun":
                continue
            if resolved == "back":
                return
            if resolved is None:
                dcp_skip = True
            else:
                ingredient_stats, combined, dcp_approximate, dcp_notes = resolved
        break

    if combined:
        state.console.print()
        no_servings = recipe["servings"] == 0
        daily_nutrients, rda = _get_daily_context()

        if no_servings:
            # No serving count — show whole-recipe totals, then per-100g / per-volume
            # if the user recorded a total weight or volume.
            _print_nutrient_table(combined, title="Total recipe",
                                  per_label="whole recipe (no serving count)",
                                  daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
            analysis_nutrients = combined

            wt_g = _recipe_weight_to_g(recipe["total_weight"], recipe["total_weight_unit"])
            if wt_g:
                per_100g = {k: v / wt_g * 100 for k, v in combined.items()}
                _print_nutrient_table(per_100g, title="Per 100 g",
                                      per_label="based on recorded recipe weight",
                                      daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
                analysis_nutrients = per_100g

            vol_ml = _recipe_vol_to_ml(recipe["total_volume"], recipe["total_volume_unit"])
            if vol_ml:
                per_100ml = {k: v / vol_ml * 100 for k, v in combined.items()}
                _print_nutrient_table(per_100ml, title="Per 100 ml",
                                      per_label="based on recorded recipe volume",
                                      daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
                per_cup = {k: v / vol_ml * 236.6 for k, v in combined.items()}
                _print_nutrient_table(per_cup, title="Per 1 cup (236 ml)",
                                      per_label="based on recorded recipe volume",
                                      daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
                if not wt_g:
                    analysis_nutrients = per_100ml
        else:
            _print_nutrient_table(combined, title="Total recipe",
                                  per_label=f"whole recipe ({recipe['servings']} servings)",
                                  daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
            if recipe["servings"] > 1:
                per_serving = {k: v / recipe["servings"] for k, v in combined.items()}
                _print_nutrient_table(per_serving, title="Per serving",
                                      daily_nutrients=daily_nutrients, rda=rda)
                analysis_nutrients = per_serving
            else:
                analysis_nutrients = combined

        # Cache per-100g nutrients for complement suggestions (needs total_weight)
        _cache_wt_g = _recipe_weight_to_g(recipe["total_weight"], recipe["total_weight_unit"])
        if _cache_wt_g and _cache_wt_g > 0 and not no_servings:
            _cache_per100g = {k: v / _cache_wt_g * 100 for k, v in combined.items()}
            with _db.get_db() as conn:
                _db.recipe_save_nutrients(conn, recipe["id"], json.dumps(_cache_per100g))

        # Compute DCP, save to DB, and display it as a summary line
        now_utc = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
        # When servings=0 the "per serving" concept doesn't apply; treat as 1 for math.
        effective_servings = recipe["servings"] if recipe["servings"] > 0 else 1
        dcp_label = "per serving" if recipe["servings"] > 1 else "whole recipe"

        eff_diaas: float | None = None
        pooled_tid: float | None = None   # weighted-average true ileal digestibility for complement sizing
        dcp_amount: float | None = None

        # Compute meal-level pooled DIAAS from actual AA data — captures complementarity
        meal_result: dict | None = None
        if not dcp_skip and ingredient_stats:
            diaas_ingredients = [
                {
                    "food_name": s["name"],
                    "nutrients_100g": s.get("nutrients_100g", {}),
                    "grams": s.get("amount_g", 0.0),
                    "fdc_id": s.get("fdc_id"),
                }
                for s in ingredient_stats
                if s.get("nutrients_100g") and s.get("amount_g", 0.0) > 0
            ]
            if diaas_ingredients:
                with _db.get_db() as conn:
                    meal_result = _diaas.meal_level_diaas(diaas_ingredients, conn)

        if dcp_skip:
            with _db.get_db() as conn:
                _db.recipe_set_dcp(conn, recipe["id"], None)
        else:
            if ingredient_stats:
                if meal_result and meal_result.get("diaas") is not None:
                    eff_diaas = meal_result["diaas"]
                    dcp_amount = (meal_result.get("digestible_complete_protein_g") or 0.0) / effective_servings
                    # Compute pooled TID (weighted avg digestibility) — DIAAS != TID and must
                    # not be used as digestibility in complement sizing (inflates R by 1/DIAAS,
                    # causing 5-10× oversized suggestions when DIAAS is low due to AA imbalance).
                    aa_ings = [
                        i for i in (meal_result.get("ingredients") or [])
                        if i.get("has_aa_data") and i.get("protein_g", 0) > 0
                    ]
                    _aa_protein_sum = sum(i["protein_g"] for i in aa_ings)
                    if _aa_protein_sum > 0:
                        pooled_tid = sum(i["protein_g"] * i["digestibility"] for i in aa_ings) / _aa_protein_sum
                else:
                    # Fall back to per-ingredient weighted average when AA data is unavailable
                    total_digestible = sum(
                        s["protein_g"] * (s["diaas"] if s["diaas"] is not None else 1.0)
                        for s in ingredient_stats
                    )
                    total_protein_whole = sum(s["protein_g"] for s in ingredient_stats)
                    dcp_amount = total_digestible / effective_servings
                    eff_diaas = total_digestible / total_protein_whole if total_protein_whole > 0 else 0.0
                # When servings=0 dcp_g per-serving is meaningless — don't save it.
                save_ts = now_utc if not dcp_approximate else None
                save_dcp = None if (dcp_approximate or no_servings) else dcp_amount
                with _db.get_db() as conn:
                    _db.recipe_set_dcp(conn, recipe["id"], save_dcp, save_ts if save_dcp is not None else None)
            else:
                with _db.get_db() as conn:
                    _db.recipe_set_dcp(conn, recipe["id"], None)

        # Meal-Level Complete Protein Analysis (steps 3+4 in plan)
        servings = max(1, recipe["servings"])
        if ingredient_stats:
            per_serving_stats = [
                {**s, "protein_g": s["protein_g"] / servings,
                 "amount_g": (s["amount_g"] or 0.0) / servings}
                for s in ingredient_stats
            ]
            per_serving_meal_result: dict | None = None
            if meal_result:
                per_serving_meal_result = {
                    **meal_result,
                    "digestible_complete_protein_g": (
                        (meal_result.get("digestible_complete_protein_g") or 0.0) / servings
                    ),
                }
            augmented_analysis, aa_augmented = _augment_aa_from_curated(
                analysis_nutrients, per_serving_stats
            )
        else:
            per_serving_stats = []
            per_serving_meal_result = None
            augmented_analysis = analysis_nutrients
            aa_augmented = False

        has_aa = _print_protein_completeness(augmented_analysis)
        if ingredient_stats:
            _print_recipe_bioavailability(per_serving_stats, analysis_nutrients, per_serving_meal_result)
        if aa_augmented:
            state.console.print(
                "  [grey62](⚑ Amino acid scores above estimated using curated literature data "
                "for ingredients without USDA amino acid records.)[/grey62]",
                highlight=False,
            )
        # Missing Amino Acid Profiles (step 4)
        if not has_aa and analysis_nutrients.get("protein_g", 0) > 0:
            state.console.print(
                f"\n  [{state.T['warning']}]⚑  Insufficient amino acid data to assess protein completeness.[/{state.T['warning']}]",
                highlight=False,
            )
            state.console.print(
                "  [grey62]Recipe ingredients lack USDA amino acid records. If this recipe relies "
                "mainly on plant proteins, consider pairing with a complementary source "
                "(e.g. legumes + grains, or dairy / eggs / soy) to improve amino acid balance.[/grey62]",
                highlight=False,
            )
        else:
            # Partial AA gap: some ingredients have AA data, others don't
            missing_aa_ings = [s["name"] for s in ingredient_stats
                               if not s.get("has_aa") and s.get("protein_g", 0) >= 0.1]
            if missing_aa_ings:
                names_str = ", ".join(missing_aa_ings)
                state.console.print(
                    f"\n  [{state.T['warning']}]⚠  These ingredient(s) have no amino acid profile "
                    f"— AA completeness scores are partial:[/{state.T['warning']}]"
                    f"\n    [grey62]{names_str}[/grey62]",
                    highlight=False,
                )

        # Protein adequacy — merged with DCP result and DIAAS explanation (step 5)
        profile = _profile.load_profile()
        _print_dcp_adequacy_section(
            per_serving_meal_result,
            analysis_nutrients,
            profile,
            dcp_g=dcp_amount,
            dcp_skip=dcp_skip,
            dcp_approximate=dcp_approximate,
            dcp_notes=dcp_notes,
            context_label=recipe["name"],
        )

        # Protein Complement Suggestions (step 6)
        if has_aa:
            if no_servings:
                wt_g = _recipe_weight_to_g(recipe["total_weight"], recipe["total_weight_unit"])
                vol_ml = _recipe_vol_to_ml(recipe["total_volume"], recipe["total_volume_unit"])
                if wt_g:
                    basis_label = "per 100 g"
                elif vol_ml:
                    basis_label = "per 100 ml"
                else:
                    basis_label = "whole recipe"
                sugg_nutrients = augmented_analysis
                _print_complement_suggestions(sugg_nutrients, context="recipe",
                                              offer_if_covered=True,
                                              basis_label=basis_label,
                                              base_diaas=pooled_tid)
            else:
                gaps = _usda.get_aa_gaps(augmented_analysis, digestibility=pooled_tid if pooled_tid is not None else 1.0)
                if servings > 1 and gaps:
                    state.console.print(
                        f"\n  Complement suggestions basis:\n"
                        f"  [grey62]1[/grey62]  Per serving  [grey62](default)[/grey62]\n"
                        f"  [grey62]2[/grey62]  Whole recipe  ({servings} serving(s))"
                    )
                    try:
                        basis_choice = _prompt("Choice  (Enter=per serving)", choices=["1", "2"], default="1").strip()
                    except Cancelled:
                        basis_choice = "1"
                else:
                    basis_choice = "1"
                if basis_choice == "2":
                    sugg_nutrients, _ = _augment_aa_from_curated(combined, ingredient_stats)
                    basis_label = f"whole recipe — {servings} serving(s)"
                else:
                    sugg_nutrients = augmented_analysis
                    basis_label = "per serving"
                _print_complement_suggestions(sugg_nutrients, context="recipe",
                                              offer_if_covered=True,
                                              basis_label=basis_label,
                                              base_diaas=pooled_tid)

        # Glycemic load (step 7)
        gl_whole, gl_blockers = _compute_recipe_gl(recipe["id"])
        section_title("Glycemic load")
        if gl_blockers:
            with _db.get_db() as conn:
                _db.recipe_set_gl(conn, recipe["id"], None)
            state.console.print(
                f"  [{state.T['warning']}]Not available — GI annotation missing for:[/{state.T['warning']}]"
            )
            for name in gl_blockers:
                state.console.print(f"    [grey62]• {name}[/grey62]")
            state.console.print(
                "  [grey62]Annotate foods under Foods → View / edit / delete cached foods → pick food → Annotate.[/grey62]"
            )
        else:
            save_gl = None if no_servings else gl_whole
            with _db.get_db() as conn:
                _db.recipe_set_gl(conn, recipe["id"], save_gl)
            gl_per_serving = gl_whole / effective_servings if effective_servings > 0 else gl_whole
            color = (state.T["success"] if gl_per_serving <= 10
                     else state.T["warning"] if gl_per_serving <= 19
                     else state.T["error"])
            state.console.print(
                f"  [{color}]{gl_per_serving:.1f}[/{color}]  [grey62]{dcp_label}[/grey62]",
                highlight=False,
            )
            if save_gl is not None:
                state.console.print("  [grey62]↳ Saved to recipe[/grey62]", highlight=False)
        help_footer("glycemic")

        # Oxalate step — only if profile has use_oxalate_data=True
        from ..services.oxalate_link import maybe_show_oxalate
        import oxalate as _ox
        if profile and profile.use_oxalate_data and _ox.is_available():
            section_title("Oxalate")
            state.console.print(
                "  [grey62]Linking recipe ingredients to oxalate reference data...[/grey62]",
                highlight=False,
            )
            for s in ingredient_stats:
                if s.get("fdc_id") is not None:
                    maybe_show_oxalate(s["fdc_id"], s["name"])
            # Summarize confirmed oxalate totals for the recipe
            total_ox_mg: float = 0.0
            confirmed_count: int = 0
            with _db.get_db() as conn:
                for s in ingredient_stats:
                    if s.get("fdc_id") is None:
                        continue
                    link = _db.oxalate_link_get(conn, s["fdc_id"])
                    if not link or link["no_match"] or not link["oxalate_food_id"]:
                        continue
                    try:
                        with _ox.get_oxalate_db() as ox_conn:
                            ox_row = _ox.get_by_id(ox_conn, link["oxalate_food_id"])
                        if ox_row and ox_row["oxalate_mg_per_100g"] is not None:
                            amount_g = s.get("amount_g", 0.0) or 0.0
                            if amount_g > 0:
                                total_ox_mg += ox_row["oxalate_mg_per_100g"] * amount_g / 100.0
                                confirmed_count += 1
                    except FileNotFoundError:
                        pass
            if confirmed_count > 0:
                ox_per_serving = total_ox_mg / effective_servings if effective_servings > 0 else total_ox_mg
                state.console.print(
                    f"\n  [bold]Estimated oxalate — total recipe:[/bold]  {total_ox_mg:.0f} mg",
                    highlight=False,
                )
                if recipe["servings"] and recipe["servings"] > 1:
                    state.console.print(
                        f"  [bold]Per serving:[/bold]  {ox_per_serving:.0f} mg  "
                        f"[grey62]({confirmed_count} ingredient(s) with per-100g data)[/grey62]",
                        highlight=False,
                    )
                state.console.print(
                    "  [grey62]Note: ingredients with only volumetric oxalate data are excluded from this total.[/grey62]",
                    highlight=False,
                )

        if no_servings:
            export_per_label = "whole recipe (no serving count)"
            export_analysis_title = "Per 100 g" if _recipe_weight_to_g(
                recipe["total_weight"], recipe["total_weight_unit"]
            ) else "Per 100 ml" if _recipe_vol_to_ml(
                recipe["total_volume"], recipe["total_volume_unit"]
            ) else "Whole recipe"
        else:
            export_per_label = f"whole recipe, {recipe['servings']} serving(s)"
            export_analysis_title = "Per serving"

        export_sections: list[dict] = [
            {"type": "ingredient_list", "title": "Ingredients",
             "items": [{"food_name": i["food_name"], "amount": i["amount"],
                        "unit": i["unit"]} for i in ingredients]},
            {"type": "nutrient_table", "title": "Total recipe", "nutrients": combined,
             "per_label": export_per_label},
            {"type": "nutrient_table", "title": export_analysis_title,
             "nutrients": analysis_nutrients},
            {"type": "protein_completeness", "nutrients": analysis_nutrients},
        ]
        if per_serving_stats:
            export_sections.append({
                "type": "recipe_bioavailability",
                "ingredient_stats": per_serving_stats,
                "total_protein": analysis_nutrients.get("protein_g", 0.0),
                "meal_result": per_serving_meal_result,
            })
        if per_serving_stats and _usda.get_aa_gaps(augmented_analysis):
            export_sections.append({
                "type": "complement_suggestions",
                "nutrients": augmented_analysis,
                "base_diaas": pooled_tid,
            })
        _offer_export(recipe["name"], export_sections)

        if save_analysis:
            now = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
            text = _export.build_report(recipe["name"], export_sections, "txt",
                                        diet_pref=state._diet_pref)
            with _db.get_db() as conn:
                _db.recipe_set_saved_analysis(conn, rid, text, now)
            state.console.print(
                f"  [{state.T['success']}]✓[/{state.T['success']}]  Analysis saved.",
                highlight=False,
            )


