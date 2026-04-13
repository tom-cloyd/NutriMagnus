import json
import re
from fractions import Fraction
from datetime import datetime, timezone

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..services.portions import _normalize_unit_display, _pick_portion
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food
from ..services.reports import _offer_export
from ..ui.common import _open_in_editor, _safe_call, _show_menu
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_complement_suggestions, _print_nutrient_table, _print_protein_completeness, _print_recipe_bioavailability

def _pick_recipe() -> dict | None:
    """
    Search recipes by name fragment (or list all), show a filtered table, and
    return the selected recipe dict. Returns None if cancelled or not found.
    """
    with _db.get_db() as conn:
        all_recipes = _db.recipe_list(conn)
    if not all_recipes:
        state.console.print("[dim]No recipes saved yet.[/dim]")
        return None

    try:
        query = _prompt("Search recipes  [dim](Enter to list all, b=back, m=main, q=quit)[/dim]", default="", free_text=True).strip()
    except Cancelled:
        return None
    if query.lower() == "q":
        raise SystemExit(0)
    if query.lower() == "m":
        raise ReturnToMain()
    if query.lower() in ("b", ""):
        recipes = all_recipes
        query = ""
    else:
        recipes = [r for r in all_recipes if query.lower() in r["name"].lower()]
        if not recipes:
            state.console.print(f"[{state.T['warning']}]No recipes matching '{query}'.[/{state.T['warning']}]")
            return None

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID",       justify="right", min_width=4)
    tbl.add_column("Name",     min_width=30)
    tbl.add_column("Servings", justify="right", min_width=8)
    tbl.add_column("DCP/srv",  justify="right", min_width=9)
    tbl.add_column("Created",  min_width=12)
    for r in recipes:
        dcp_str = f"{r['dcp_g'] / r['servings']:.1f}g" if r["dcp_g"] is not None and r["servings"] > 0 else "[dim]—[/dim]"
        tbl.add_row(str(r["id"]), r["name"], str(r["servings"]), dcp_str, r["created_at"])
    state.console.print(tbl)

    rid = _ask_int("Recipe ID")
    if rid is None:
        return None
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
    if recipe is None:
        state.console.print(f"[{state.T['warning']}]Recipe not found.[/{state.T['warning']}]")
        return None
    return recipe


def _compute_recipe_dcp(rid: int) -> float | None:
    """
    Compute digestible complete protein (g, whole recipe) from cached ingredient data.
    Returns None if AA profile data is unavailable.
    """
    with _db.get_db() as conn:
        ingredients = _db.recipe_get_ingredients(conn, rid)

    combined: dict[str, float] = {}
    total_digestible = 0.0
    has_protein = False
    for ing in ingredients:
        _refresh_cache_if_missing_aa(ing["fdc_id"])
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, ing["fdc_id"])
        if not cached:
            continue
        scaled = _usda.scale_nutrients(
            json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
        )
        combined = _usda.sum_nutrients(combined, scaled)
        p = scaled.get("protein_g", 0.0)
        if p > 0:
            has_protein = True
            diaas = _usda.get_diaas(ing["food_name"])
            total_digestible += p * (diaas if diaas is not None else 1.0)

    if not has_protein:
        return None
    return total_digestible


def _augment_aa_from_curated(
    nutrients: dict[str, float],
    stats: list[dict],
) -> tuple[dict[str, float], bool]:
    """
    Return (augmented_nutrients, was_augmented).

    For each ingredient in stats that lacks USDA AA data (has_aa=False), look up
    its amino acid profile in the curated complement table and add scaled AA amounts.
    Preserves any existing USDA AA values — only adds for ingredients without them.
    Used to get reliable gap scores when the USDA cache has no AA records for
    branded products.
    """
    augmented = dict(nutrients)
    was_augmented = False
    for s in stats:
        if s.get("has_aa"):
            continue
        curated = _usda.get_complement_nutrients(s["name"])
        if not curated or curated.get("protein_g", 0) <= 0:
            continue
        scale = s["protein_g"] / curated["protein_g"]
        for aa_key in _usda.ESSENTIAL_AMINO_ACIDS:
            if aa_key in curated:
                augmented[aa_key] = augmented.get(aa_key, 0.0) + curated[aa_key] * scale
                was_augmented = True
    return augmented, was_augmented


def _parse_serving_amount(raw: str) -> float | None:
    """Parse a recipe serving amount like 1, 0.5, 1/2, or 1 1/2."""
    raw = raw.strip().lower()
    if not raw or raw in {"b", "back"}:
        return None
    try:
        parts = raw.split()
        if len(parts) == 2 and "/" in parts[1]:
            return float(parts[0]) + float(Fraction(parts[1]))
        if "/" in raw:
            return float(Fraction(raw))
        return float(raw)
    except (ValueError, ZeroDivisionError):
        return None


def _format_recipe_portion_label(servings: float) -> str:
    if abs(servings - 1.0) < 1e-9:
        return "1 serving"
    if servings.is_integer():
        return f"{int(servings)} servings"
    return f"{servings:g} servings"


def _get_recipe_total_nutrients(recipe_id: int) -> tuple[object | None, list, dict[str, float]]:
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        ingredients = _db.recipe_get_ingredients(conn, recipe_id) if recipe else []

    combined: dict[str, float] = {}
    if recipe and ingredients:
        for ing in ingredients:
            _refresh_cache_if_missing_aa(ing["fdc_id"])
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, ing["fdc_id"])
            if cached:
                scaled = _usda.scale_nutrients(
                    json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
                )
                combined = _usda.sum_nutrients(combined, scaled)
    return recipe, ingredients, combined


def _pick_recipe_portion(recipe: object) -> tuple[float, str] | None:
    while True:
        try:
            raw = _prompt(
                "Recipe portion in servings  [dim](examples: 1, 1/2, 1.5 · Enter/b=back, m=main, q=quit)[/dim]",
                default="1",
            ).strip()
        except Cancelled:
            return None
        lowered = raw.lower()
        if not lowered or lowered in ("b", "back"):
            return None
        if lowered == "m":
            raise ReturnToMain()
        if lowered == "q":
            raise SystemExit(0)
        servings = _parse_serving_amount(raw)
        if servings is None or servings <= 0:
            state.console.print(f"[{state.T['warning']}]Enter a positive number of servings.[/{state.T['warning']}]")
            continue
        return servings, _format_recipe_portion_label(servings)

def _menu_recipes() -> bool:
    """Recipes submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Recipes", [
            ("1", "Create new recipe"),
            ("2", "List recipes"),
            ("3", "View / analyze recipe"),
            ("4", "Edit recipe"),
            ("5", "Delete recipe"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[dim]Cancelled.[/dim]")
            return True

        if choice == "1":
            _safe_call(_do_recipe_create)
        elif choice == "2":
            _safe_call(_do_recipe_list)
        elif choice == "3":
            _safe_call(_do_recipe_view)
        elif choice == "4":
            _safe_call(_do_recipe_edit)
        elif choice == "5":
            _safe_call(_do_recipe_delete)
        elif choice == "m":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_recipe_create() -> None:
    try:
        name = _prompt("Recipe name", free_text=True).strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return

    try:
        description = _prompt("Description (optional)", default="", free_text=True).strip()
        raw_servings = _prompt("Number of servings", default="1", free_text=True).strip()
        servings = int(raw_servings) if raw_servings.isdigit() else 1
        state.console.print("  [dim]Opening editor for Procedure (close/save to continue, leave blank to skip)…[/dim]")
        instructions = _open_in_editor("").strip()
    except Cancelled:
        return

    with _db.get_db() as conn:
        recipe_id = _db.recipe_create(conn, name, description, servings, instructions)

    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Recipe [{state.T['hi']}]{name}[/{state.T['hi']}] "
                  f"created (ID {recipe_id}).  Now add ingredients.")

    # Add ingredients loop
    while True:
        state.console.print()
        food = _search_and_pick_food()
        if food is None:
            break
        result = _pick_portion(food)
        if result is None:
            break
        grams, label, _ = result
        try:
            notes = _prompt("Note for this ingredient  [dim](optional, Enter to skip)[/dim]", default="", free_text=True).strip() or None
        except Cancelled:
            notes = None
        with _db.get_db() as conn:
            _db.recipe_add_ingredient(conn, recipe_id, food["fdcId"],
                                      food["name"], grams, label, notes)
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")
        try:
            cont = _prompt("Add another ingredient?", choices=["y", "n", "q"], default="y")
        except Cancelled:
            break
        if cont.lower() == "q":
            raise SystemExit(0)
        if cont.lower() != "y":
            break

    state.console.print(f"[{state.T['success']}]Recipe saved.[/{state.T['success']}]")


def _do_recipe_list() -> None:
    with _db.get_db() as conn:
        recipes = _db.recipe_list(conn)
    if not recipes:
        state.console.print("[dim]No recipes saved yet.[/dim]")
        return
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID",       justify="right", min_width=4)
    tbl.add_column("Name",     min_width=30)
    tbl.add_column("Servings", justify="right", min_width=8)
    tbl.add_column("DCP/srv",  justify="right", min_width=9)
    tbl.add_column("Created",  min_width=12)
    for r in recipes:
        if r["dcp_g"] is not None and r["servings"] > 0:
            dcp_str = f"{r['dcp_g'] / r['servings']:.1f}g"
        else:
            dcp_str = "[dim]—[/dim]"
        tbl.add_row(str(r["id"]), r["name"], str(r["servings"]), dcp_str, r["created_at"])
    state.console.print(tbl)


def _resolve_recipe_dcp_data(
    recipe_id: int,
    ingredients: list,
    ingredient_stats: list[dict],
    combined: dict[str, float],
) -> tuple[list[dict], dict[str, float], bool, list[str]] | None:
    """
    Detect missing data that blocks or degrades DCP calculation.
    Prompts the user to provide data, calculate with assumptions, or skip.

    Returns (updated_stats, updated_combined, approximate, notes),
    None if the user chooses to skip DCP entirely,
    or the string "rerun" if ingredients were replaced and analysis should restart.
    """
    zero_weight = [ing for ing in ingredients if "(weight not known)" in (ing["unit"] or "")]
    no_diaas    = [s for s in ingredient_stats if s["diaas"] is None]
    no_aa_ings  = [s for s in ingredient_stats if not s.get("has_aa", True)]
    pc          = _usda.protein_completeness(combined)
    no_aa       = not pc.get("has_data")

    if not zero_weight and not no_diaas and not no_aa:
        return ingredient_stats, combined, False, []

    state.console.print(f"\n  [{state.T['warning']}]⚠  Missing data for digestible complete protein (DCP):[/{state.T['warning']}]")
    for ing in zero_weight:
        state.console.print(f"    • {ing['food_name']} — weight unknown ({_normalize_unit_display(ing['unit'])})")
    for s in no_diaas:
        state.console.print(f"    • {s['name']} — no digestibility (DIAAS) score in database")
    if no_aa:
        if no_aa_ings:
            for s in no_aa_ings:
                state.console.print(f"    • {s['name']} — no amino acid profile in USDA data")
        else:
            state.console.print("    • No amino acid profile available in USDA data for these ingredients.")

    # Build numbered options dynamically, preserving the action key internally
    action_items: list[tuple[str, str]] = []  # (action_key, label)
    if no_aa and no_aa_ings:
        action_items.append(("f", "Fix: replace affected ingredients via Foundation Foods search"))
    if zero_weight or no_diaas:
        action_items.append(("p", "Provide missing data now"))
    action_items.append(("c", "Calculate anyway  (result flagged as approximate)"))
    action_items.append(("s", "Skip DCP calculation"))

    numbered: list[tuple[str, str]] = [(str(i + 1), label) for i, (_, label) in enumerate(action_items)]
    numbered.append(("b", "Back to previous menu"))
    numbered.append(("m", "Return to main menu"))
    numbered.append(("q", "Quit"))
    _show_menu("Options", numbered)

    valid_nums = {str(i + 1) for i in range(len(action_items))}
    while True:
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return "back"  # type: ignore[return-value]
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
            state.console.print(
                f"\n  Replacing: [{state.T['accent']}]{ing['food_name']}[/{state.T['accent']}]\n"
                "  [dim]Search for a Foundation Foods replacement:[/dim]"
            )
            food = _search_and_pick_food(data_types=["Foundation", "SR Legacy"], show_aa_status=True, allow_research=True)
            if food is None:
                state.console.print("  [dim]Skipped.[/dim]")
                continue
            result = _pick_portion(food)
            if result is None:
                state.console.print("  [dim]Skipped.[/dim]")
                continue
            grams, label, _ = result
            with _db.get_db() as conn:
                _db.recipe_remove_ingredient(conn, ing["id"])
                _db.recipe_add_ingredient(conn, recipe_id, food["fdcId"], food["name"], grams, label)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Replaced with: {food['name']}  {label}")
            replaced_any = True
        if replaced_any:
            return "rerun"  # type: ignore[return-value]
        return None

    approximate = False
    notes: list[str] = []

    if action == "p":
        new_combined  = dict(combined)
        new_stats     = list(ingredient_stats)

        for ing in zero_weight:
            vol_display = _normalize_unit_display(ing["unit"]).replace(" (weight not known)", "")
            state.console.print(f"\n  [{state.T['accent']}]{ing['food_name']}[/{state.T['accent']}]"
                          f"  [dim]({vol_display})[/dim]")
            try:
                w_raw = _prompt("Weight in grams  (Enter=skip)", free_text=True).strip()
            except Cancelled:
                w_raw = ""
            if w_raw.lower() == "q":
                raise SystemExit(0)
            if w_raw and w_raw.lower() not in ("b", "s"):
                try:
                    grams = float(w_raw)
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, ing["fdc_id"])
                    if cached:
                        scaled = _usda.scale_nutrients(
                            json.loads(cached["nutrients_json"]), grams, base_size=100.0
                        )
                        new_combined = _usda.sum_nutrients(new_combined, scaled)
                        p = scaled.get("protein_g", 0.0)
                        if p > 0:
                            new_stats.append({
                                "name": ing["food_name"],
                                "protein_g": p,
                                "diaas": _usda.get_diaas(ing["food_name"]),
                            })
                    notes.append(f"{ing['food_name']}: {grams:.0f}g (user-provided, not saved)")
                    approximate = True  # user-supplied value, not from DB
                except ValueError:
                    approximate = True
                    notes.append(f"{ing['food_name']}: skipped (invalid weight)")
            else:
                approximate = True
                notes.append(f"{ing['food_name']}: excluded (weight not provided)")

        for s in no_diaas:
            state.console.print(
                f"\n  [{state.T['accent']}]{s['name']}[/{state.T['accent']}]  [dim]— DIAAS unknown[/dim]\n"
                "  [dim]Reference: eggs 0.99 · whey 0.97 · meat/fish 0.90–0.95 · soy 0.91 "
                "· legumes 0.64–0.75 · wheat 0.46[/dim]"
            )
            try:
                d_raw = _prompt("DIAAS value (0.0–1.0)  (Enter=skip → assume 1.0)", free_text=True).strip()
            except Cancelled:
                d_raw = ""
            if d_raw.lower() == "q":
                raise SystemExit(0)
            if d_raw and d_raw.lower() not in ("b", "s"):
                try:
                    diaas = max(0.0, min(1.0, float(d_raw)))
                    s["diaas"] = diaas
                    notes.append(f"{s['name']}: DIAAS {diaas:.2f} (user-provided)")
                    approximate = True
                except ValueError:
                    approximate = True
                    notes.append(f"{s['name']}: DIAAS assumed 1.0 (invalid input)")
            else:
                approximate = True
                notes.append(f"{s['name']}: DIAAS assumed 1.0")

        return new_stats, new_combined, approximate, notes

    else:  # action == "c" — calculate anyway
        approximate = True
        for ing in zero_weight:
            notes.append(f"{ing['food_name']}: excluded (weight not known)")
        for s in no_diaas:
            notes.append(f"{s['name']}: DIAAS assumed 1.0")
        if no_aa:
            notes.append("amino acid completeness: unknown — no AA data in USDA cache")
        return ingredient_stats, combined, True, notes


def _do_recipe_view() -> None:
    _do_recipe_list()
    rid = _ask_int("Recipe ID")
    if rid is None:
        return
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
        if recipe is None:
            state.console.print(f"[{state.T['warning']}]Recipe {rid} not found.[/{state.T['warning']}]")
            return
        ingredients = _db.recipe_get_ingredients(conn, rid)

    if not ingredients:
        state.console.print("[dim]This recipe has no ingredients.[/dim]")
        return

    while True:
        # Reload recipe + ingredients on rerun (ingredients may have been replaced)
        with _db.get_db() as conn:
            recipe     = _db.recipe_get(conn, rid)
            ingredients = _db.recipe_get_ingredients(conn, rid)

        state.console.print(f"\n[{state.T['accent']}]{recipe['name']}[/{state.T['accent']}]  "
                      f"[dim]{recipe['servings']} serving(s)[/dim]")
        if recipe["description"]:
            state.console.print(f"  {recipe['description']}")

        # Ingredient list with amounts — shown before DCP prompts so user can see the recipe
        state.console.print(f"\n[{state.T['accent']}]Ingredients:[/{state.T['accent']}]")
        for ing in ingredients:
            note_tag = f"  [dim]({ing['notes']})[/dim]" if ing["notes"] else ""
            state.console.print(f"  • {_normalize_unit_display(ing['unit'])}  {ing['food_name']}{note_tag}")

        if recipe["instructions"]:
            state.console.print(f"\n[{state.T['accent']}]Procedure:[/{state.T['accent']}]")
            state.console.print(f"  {recipe['instructions']}")
        state.console.rule()

        # Build combined nutrients and per-ingredient protein+DIAAS (silent — before display)
        combined: dict[str, float] = {}
        ingredient_stats: list[dict] = []
        for ing in ingredients:
            _refresh_cache_if_missing_aa(ing["fdc_id"])
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, ing["fdc_id"])
            if cached:
                scaled = _usda.scale_nutrients(
                    json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
                )
                combined = _usda.sum_nutrients(combined, scaled)
                ing_protein = scaled.get("protein_g", 0.0)
                if ing_protein > 0:
                    ingredient_stats.append({
                        "name": ing["food_name"],
                        "protein_g": ing_protein,
                        "diaas": _usda.get_diaas(ing["food_name"]),
                        "has_aa": _usda.protein_completeness(scaled).get("has_data", False),
                    })

        # Resolve missing DCP data before displaying tables so totals reflect any user input
        dcp_skip = False
        dcp_approximate = False
        dcp_notes: list[str] = []
        if combined:
            resolved = _resolve_recipe_dcp_data(recipe["id"], ingredients, ingredient_stats, combined)
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
        _print_nutrient_table(combined, title="Total recipe",
                              per_label=f"whole recipe ({recipe['servings']} servings)")
        # Per-serving (skip when servings=1 — identical to total)
        if recipe["servings"] > 1:
            per_serving = {k: v / recipe["servings"] for k, v in combined.items()}
            _print_nutrient_table(per_serving, title="Per serving")
            analysis_nutrients = per_serving
        else:
            analysis_nutrients = combined

        # Compute DCP, save to DB, and always display it as a summary line
        now_utc = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
        if dcp_skip:
            with _db.get_db() as conn:
                _db.recipe_set_dcp(conn, recipe["id"], None)
            state.console.print("\n  [dim]Digestible complete protein: skipped.[/dim]")
        else:
            if ingredient_stats:
                total_digestible = sum(
                    s["protein_g"] * (s["diaas"] if s["diaas"] is not None else 1.0)
                    for s in ingredient_stats
                )
                total_protein_whole = sum(s["protein_g"] for s in ingredient_stats)
                dcp_per_serving = total_digestible / max(1, recipe["servings"])
                eff_diaas = total_digestible / total_protein_whole if total_protein_whole > 0 else 0.0
                # Only save to DB if all data was authoritative (not approximate)
                save_ts = now_utc if not dcp_approximate else None
                was_missing = recipe["dcp_g"] is None
                with _db.get_db() as conn:
                    _db.recipe_set_dcp(conn, recipe["id"], None if dcp_approximate else dcp_per_serving, save_ts)
                color = state.T["success"] if eff_diaas >= 0.90 else (state.T["warning"] if eff_diaas >= 0.70 else state.T["error"])
                approx_tag = f"  [{state.T['warning']}]⚠ approximate[/{state.T['warning']}]" if dcp_approximate else ""
                if was_missing and not dcp_approximate:
                    state.console.print(
                        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  [dim]Recipe data now complete"
                        f" — DCP can be calculated.[/dim]"
                    )
                state.console.print(
                    f"\n  Digestible complete protein: [{color}]{dcp_per_serving:.1f}g[/{color}]"
                    f"  [dim]per serving[/dim]{approx_tag}",
                    highlight=False,
                )
                if dcp_approximate:
                    if dcp_notes:
                        for note in dcp_notes:
                            state.console.print(f"    [dim]↳ {note}[/dim]")
                else:
                    state.console.print(
                        f"  [dim]↳ Saved to recipe · computed {now_utc}[/dim]",
                        highlight=False,
                    )
            else:
                with _db.get_db() as conn:
                    _db.recipe_set_dcp(conn, recipe["id"], None)
                state.console.print(
                    "\n  [dim]Digestible complete protein: not available "
                    "(no amino acid data for these ingredients)[/dim]"
                )
                if dcp_notes:
                    for note in dcp_notes:
                        state.console.print(f"    [dim]↳ {note}[/dim]")

        # Offer full protein analysis
        try:
            ans = _prompt("Show protein analysis?  [dim](y/N)[/dim]", default="n").strip().lower()
        except Cancelled:
            ans = "n"
        if ans == "y":
            servings = max(1, recipe["servings"])
            if ingredient_stats:
                per_serving_stats = [
                    {**s, "protein_g": s["protein_g"] / servings}
                    for s in ingredient_stats
                ]
                augmented_analysis, aa_augmented = _augment_aa_from_curated(
                    analysis_nutrients, per_serving_stats
                )
            else:
                per_serving_stats = []
                augmented_analysis = analysis_nutrients
                aa_augmented = False

            has_aa = _print_protein_completeness(augmented_analysis)
            if ingredient_stats:
                _print_recipe_bioavailability(per_serving_stats, analysis_nutrients)
            if aa_augmented:
                state.console.print(
                    "  [dim](⚑ Amino acid scores above estimated using curated literature data "
                    "for ingredients without USDA amino acid records.)[/dim]",
                    highlight=False,
                )
            if has_aa and _usda.get_aa_gaps(augmented_analysis):
                state.console.print(
                    f"\n  Complement suggestions basis:\n"
                    f"  [dim]1[/dim]  Per serving\n"
                    f"  [dim]2[/dim]  Whole recipe  ({servings} serving(s))"
                )
                try:
                    basis_choice = _prompt("Choice", choices=["1", "2"], default="1").strip()
                except Cancelled:
                    basis_choice = "1"
                if basis_choice == "2":
                    sugg_nutrients, _ = _augment_aa_from_curated(combined, ingredient_stats)
                    basis_label = f"whole recipe — {servings} serving(s)"
                else:
                    sugg_nutrients = augmented_analysis
                    basis_label = "per serving"
                _print_complement_suggestions(sugg_nutrients, context="recipe",
                                              offer_if_covered=True,
                                              basis_label=basis_label)
        _offer_export(recipe["name"], [
            {"type": "ingredient_list", "title": "Ingredients",
             "items": [{"food_name": i["food_name"], "amount": i["amount"],
                        "unit": i["unit"]} for i in ingredients]},
            {"type": "nutrient_table", "title": "Total recipe", "nutrients": combined,
             "per_label": f"whole recipe, {recipe['servings']} servings"},
            {"type": "nutrient_table", "title": "Per serving", "nutrients": analysis_nutrients},
            {"type": "protein_completeness", "nutrients": analysis_nutrients},
        ])


def _do_recipe_edit() -> None:
    _do_recipe_list()
    rid = _ask_int("Recipe ID to edit")
    if rid is None:
        return
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
    if recipe is None:
        state.console.print(f"[{state.T['warning']}]Recipe {rid} not found.[/{state.T['warning']}]")
        return

    state.console.print(f"\n[{state.T['accent']}]Editing: {recipe['name']}[/{state.T['accent']}]")
    state.console.print("[dim]Press Enter to keep current value.  p = previous field,  b = back to menu.[/dim]\n")

    # Edit metadata (name/description/servings) with back-navigation
    _meta_fields = [
        ("Name",        "name",        recipe["name"],                "str"),
        ("Description", "description", recipe["description"] or "",   "str"),
        ("Servings",    "servings",    str(recipe["servings"]),        "int"),
    ]
    _meta_vals: dict = {f[1]: f[2] for f in _meta_fields}
    _mi = 0
    while _mi < len(_meta_fields):
        _label, _key, _, _typ = _meta_fields[_mi]
        _cur = str(_meta_vals[_key])
        # Show current value in the label but NOT as _prompt default, so that
        # pressing Enter always returns "" and never falsely triggers b/p/q checks.
        _hint = f"[{state.T['default_hint']}]({_cur})[/{state.T['default_hint']}]"
        _display_label = f"{_label} {_hint}" if _cur else _label
        try:
            _raw = _prompt(_display_label, free_text=True).strip()
        except Cancelled:
            return
        if _raw.lower() == "q":
            raise SystemExit(0)
        if _raw.lower() == "b":
            return
        if _raw.lower() == "p":
            if _mi > 0:
                _mi -= 1
            continue
        _val = _raw if _raw else _meta_vals[_key]
        if _typ == "int":
            if _val.isdigit():
                _meta_vals[_key] = int(_val)
            else:
                state.console.print(f"  [{state.T['warning']}]Enter a whole number.[/{state.T['warning']}]")
                continue
        else:
            _meta_vals[_key] = _val
        _mi += 1
    name     = _meta_vals["name"]
    desc     = _meta_vals["description"]
    servings = _meta_vals["servings"]
    meta_changed = (
        name != recipe["name"]
        or desc != (recipe["description"] or "")
        or servings != recipe["servings"]
    )
    if meta_changed:
        with _db.get_db() as conn:
            _db.recipe_update(conn, rid, name, desc, servings, recipe["instructions"] or "")
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Recipe details updated.")

    # Show and manage ingredients
    # done=True means proceed to instructions; False means back/cancel
    ingredients_done = False
    ingredients_changed = False
    while True:
        with _db.get_db() as conn:
            ingredients = _db.recipe_get_ingredients(conn, rid)

        if ingredients:
            state.console.print(f"[{state.T['accent']}]Current recipe ingredients[/{state.T['accent']}]")
            has_notes = any(ing["notes"] for ing in ingredients)
            tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl.add_column("#",    justify="right", min_width=3)
            tbl.add_column("Amount", min_width=14)
            tbl.add_column("Food", min_width=40)
            if has_notes:
                tbl.add_column("Note", min_width=20)
            for i, ing in enumerate(ingredients, 1):
                row = [str(i), _normalize_unit_display(ing["unit"]), ing["food_name"]]
                if has_notes:
                    row.append(ing["notes"] or "")
                tbl.add_row(*row)
            state.console.print(tbl)
        else:
            state.console.print("[dim]No ingredients yet.[/dim]")

        _show_menu("Ingredients", [
            ("1", "Add ingredient"),
            ("2", "Edit ingredient"),
            ("3", "Remove ingredient"),
            ("4", "Reorder ingredients"),
            ("d", "Done — save and edit Procedure"),
            ("b", "Back to previous menu"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            break

        if choice == "b":
            ingredients_done = False
            break
        if choice == "d":
            ingredients_done = True
            break
        if choice == "m":
            raise ReturnToMain()
        if choice == "q":
            raise SystemExit(0)
        elif choice == "1":
            food = _search_and_pick_food()
            if food is None:
                continue
            result = _pick_portion(food)
            if result is None:
                continue
            grams, label, _ = result
            try:
                notes = _prompt("Note for this ingredient  [dim](optional, Enter to skip)[/dim]", default="", free_text=True).strip() or None
            except Cancelled:
                notes = None
            with _db.get_db() as conn:
                _db.recipe_add_ingredient(conn, rid, food["fdcId"], food["name"], grams, label, notes)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")
            ingredients_changed = True
        elif choice == "2":
            if not ingredients:
                state.console.print(f"[{state.T['warning']}]No ingredients to edit.[/{state.T['warning']}]")
                continue
            idx = _ask_int("Ingredient # to edit")
            if idx is None or idx < 1 or idx > len(ingredients):
                state.console.print(f"[{state.T['warning']}]Invalid number.[/{state.T['warning']}]")
                continue
            ing = ingredients[idx - 1]
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, ing["fdc_id"])
            if cached is None:
                state.console.print(f"[{state.T['warning']}]Food details not in cache; remove and re-add this ingredient.[/{state.T['warning']}]")
                continue
            food = {
                "fdcId":    cached["fdc_id"],
                "name":     cached["name"],
                "dataType": cached["data_type"],
                "brand":    cached["brand"],
                "servingSize": cached["serving_size"],
                "servingUnit": cached["serving_unit"],
                "nutrients": json.loads(cached["nutrients_json"]),
                "portions":  json.loads(cached["portions_json"]) if cached["portions_json"] else [],
            }
            try:
                food_name_new = _prompt(
                    f"Name [{state.T['default_hint']}]({ing['food_name']})[/{state.T['default_hint']}]",
                    free_text=True
                ).strip() or ing["food_name"]
            except Cancelled:
                continue
            cur_portion = (
                f"{_normalize_unit_display(ing['unit'])}  ({ing['amount']:.4g} g)"
                if ing["amount"] else None
            )
            result = _pick_portion(food, current=cur_portion)
            if result is None:
                continue
            grams, label, _ = result
            try:
                notes_new = _prompt("Note  [dim](Enter to keep current, '-' to clear)[/dim]",
                                    default=ing["notes"] or "", free_text=True).strip()
            except Cancelled:
                notes_new = ing["notes"] or ""
            if notes_new == "-":
                notes_new = ""
            with _db.get_db() as conn:
                _db.recipe_update_ingredient(conn, ing["id"], grams, label, food_name_new,
                                             notes_new or None)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Updated: {food_name_new}  {label}")
            ingredients_changed = True
        elif choice == "3":
            if not ingredients:
                state.console.print(f"[{state.T['warning']}]No ingredients to remove.[/{state.T['warning']}]")
                continue
            idx = _ask_int("Ingredient # to remove")
            if idx is None or idx < 1 or idx > len(ingredients):
                state.console.print(f"[{state.T['warning']}]Invalid number.[/{state.T['warning']}]")
                continue
            ing = ingredients[idx - 1]
            with _db.get_db() as conn:
                _db.recipe_remove_ingredient(conn, ing["id"])
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Removed: {ing['food_name']}")
            ingredients_changed = True
        elif choice == "4":
            if len(ingredients) < 2:
                state.console.print(f"[{state.T['warning']}]Nothing to reorder.[/{state.T['warning']}]")
                continue
            state.console.print("[dim]Enter ingredient numbers in the new order, space- or comma-separated "
                          f"(e.g. 3 1 2 4 for {len(ingredients)} ingredients):[/dim]")
            try:
                raw_order = _prompt("New order", free_text=True).strip()
            except Cancelled:
                continue
            if not raw_order or raw_order.lower() in ("b", "q"):
                if raw_order.lower() == "q":
                    raise SystemExit(0)
                continue
            tokens = re.split(r'[\s,]+', raw_order.strip())
            try:
                new_order = [int(t) for t in tokens if t]
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Enter numbers only.[/{state.T['warning']}]")
                continue
            if sorted(new_order) != list(range(1, len(ingredients) + 1)):
                state.console.print(f"[{state.T['warning']}]Must include each number 1–{len(ingredients)} exactly once.[/{state.T['warning']}]")
                continue
            reordered = [ingredients[i - 1] for i in new_order]
            with _db.get_db() as conn:
                conn.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (rid,))
                for ing in reordered:
                    _db.recipe_add_ingredient(conn, rid, ing["fdc_id"], ing["food_name"],
                                              ing["amount"], ing["unit"], ing["notes"])
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Ingredients reordered.")
            ingredients_changed = True
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")

    # Edit instructions only when user chose 'd' (done), not 'b' (back)
    if not ingredients_done:
        if ingredients_changed:
            dcp = _compute_recipe_dcp(rid)
            ts = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat() if dcp is not None else None
            with _db.get_db() as conn:
                _db.recipe_set_dcp(conn, rid, dcp, ts)
        return
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
    # Strip non-printable characters from stored instructions before showing as default
    stored_instructions = "".join(
        c for c in (recipe["instructions"] or "") if c.isprintable()
    )
    state.console.print(
        f"\n  [{state.T['accent']}]Procedure[/{state.T['accent']}]"
        "  [dim]— an editor will open. Save and close it to continue.[/dim]"
    )
    state.console.print("  [dim]Press Enter to open the editor, or b to skip.[/dim]")
    try:
        go = _prompt("").strip().lower()
    except Cancelled:
        go = "b"
    if go == "b":
        instructions = stored_instructions
    else:
        instructions = _open_in_editor(stored_instructions)
    with _db.get_db() as conn:
        _db.recipe_update(conn, rid, recipe["name"], recipe["description"] or "",
                          recipe["servings"], instructions)
    if ingredients_changed:
        dcp = _compute_recipe_dcp(rid)
        ts = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat() if dcp is not None else None
        with _db.get_db() as conn:
            _db.recipe_set_dcp(conn, rid, dcp, ts)
    state.console.print(f"[{state.T['success']}]Recipe saved.[/{state.T['success']}]")


def _do_recipe_delete() -> None:
    _do_recipe_list()
    rid = _ask_int("Recipe ID to delete")
    if rid is None:
        return
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
    if recipe is None:
        state.console.print(f"[{state.T['warning']}]Recipe {rid} not found.[/{state.T['warning']}]")
        return
    try:
        confirm = _prompt(
            f"Delete [{state.T['hi']}]{recipe['name']}[/{state.T['hi']}]?",
            choices=["y", "n"], default="n"
        )
    except Cancelled:
        return
    if confirm.lower() == "y":
        with _db.get_db() as conn:
            _db.recipe_delete(conn, rid)
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Deleted.")
    else:
        state.console.print("[dim]Cancelled.[/dim]")
