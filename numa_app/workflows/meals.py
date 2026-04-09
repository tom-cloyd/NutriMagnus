import json
from datetime import date

from rich.table import Table

import db as _db
import profile as _profile
import usda as _usda
from .. import state
from ..services.portions import _normalize_unit_display, _pick_portion
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food, _simplify_food_query
from ..services.reports import _offer_export
from ..ui.common import _safe_call, _show_menu
from ..ui.prompts import Cancelled, _ask_date, _ask_int, _prompt
from ..ui.render import _print_complement_suggestions, _print_meal_diaas, _print_nutrient_table, _print_protein_adequacy
from .recipes import _do_recipe_list, _format_recipe_portion_label, _parse_serving_amount

def _fix_meal_aa_profiles(meal_id: int, missing_names: list[str]) -> bool:
    """
    For each meal food item lacking AA data, offer a search-and-replace flow.
    The search results show Type (SR Legacy / Foundation / Branded) so the user
    can pick an entry that is likely to have AA profile data.
    Returns True if any items were replaced.
    """
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)

    missing_lower = {n.lower() for n in missing_names}
    affected = [it for it in items
                if it["item_type"] == "food" and it["food_name"].lower() in missing_lower]
    if not affected:
        return False

    state.console.print(
        f"\n  [dim]Some of these may be minor ingredients (fruit, garnishes, etc.) with\n"
        f"  negligible protein — those can safely be ignored here. Only proceed if\n"
        f"  one or more of them are meaningful protein sources in your meal.\n"
        f"  If none are, enter [bold]n[/bold].[/dim]"
    )
    try:
        go = _prompt(
            f"Obtain missing amino acid (AA) profiles for {len(affected)} ingredient(s)?",
            choices=["y", "n"], default="n",
        )
    except Cancelled:
        return False
    if go != "y":
        return False

    state.console.print(
        f"\n  [dim]For each ingredient, search for a replacement with AA data.\n"
        f"  In results, prefer [bold]SR Legacy[/bold] or [bold]Foundation[/bold] entries"
        f" — these typically include full amino acid profiles.\n"
        f"  Press Enter to skip an ingredient.[/dim]"
    )

    replaced_any = False
    for item in affected:
        state.console.print(f"\n  [{state.T['accent']}]{item['food_name']}[/{state.T['accent']}]"
                      f"  [dim]({_normalize_unit_display(item['unit'])})[/dim]")
        suggested = _simplify_food_query(item["food_name"].split(",")[0].strip())
        state.console.print(f"  [dim]Searching SR Legacy + Foundation for: '{suggested}'[/dim]")
        food = _search_and_pick_food(
            data_types=["Foundation", "SR Legacy"],
            initial_query=suggested,
            show_aa_status=True,
            allow_research=False,
        )
        if food is None:
            state.console.print("  [dim]Skipped.[/dim]")
            continue

        has_aa = _usda.has_amino_acid_data(food["nutrients"])
        if not has_aa:
            state.console.print(
                f"  [{state.T['warning']}]⚠  This food also has no AA profile "
                f"(Type: {food.get('dataType', '?')}). Replace anyway?[/{state.T['warning']}]"
            )
            try:
                confirm = _prompt("Replace?", choices=["y", "n"], default="n")
            except Cancelled:
                confirm = "n"
            if confirm != "y":
                continue

        grams, label = None, None
        if item["amount"] and item["amount"] > 0 and item["unit"] and item["unit"] != "—":
            state.console.print(f"  [dim]Original amount: [bold]{_normalize_unit_display(item['unit'])}[/bold]"
                          f"  ({item['amount']:.0f} g)[/dim]")
            try:
                keep = _prompt("Keep this amount for the replacement?  [dim](Y/n)[/dim]",
                               default="y").strip().lower()
            except Cancelled:
                keep = "y"
            if keep != "n":
                grams = item["amount"]
                label = item["unit"]
        if grams is None:
            result = _pick_portion(food)
            if result is None:
                state.console.print("  [dim]Skipped.[/dim]")
                continue
            grams, label, _ = result

        with _db.get_db() as conn:
            _db.meal_remove_item(conn, item["id"], meal_id)
            _db.meal_add_food(conn, meal_id, food["fdcId"], food["name"], grams, label)

        aa_tag = (f"[{state.T['success']}]✓ has AA data[/{state.T['success']}]" if has_aa
                  else f"[{state.T['warning']}]⚠ no AA data[/{state.T['warning']}]")
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Replaced with: {food['name']}  {label}  {aa_tag}")
        replaced_any = True

    if replaced_any:
        state.console.print(
            f"\n  [{state.T['success']}]✓[/{state.T['success']}]  [dim]Ingredients updated."
            f" Re-analyze this meal to see the updated DIAAS results.[/dim]"
        )
    return replaced_any

def _menu_meals() -> bool:
    """Meals submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Meals & Log", [
            ("1", "Log a new meal"),
            ("2", "View/edit meals for a date"),
            ("3", "Analyze a logged meal"),
            ("4", "Delete a meal"),
            ("b", "Back to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[dim]Cancelled.[/dim]")
            return True

        if choice == "1":
            _safe_call(_do_meal_log)
        elif choice == "2":
            _safe_call(_do_meal_view_by_date)
        elif choice == "3":
            _safe_call(_do_meal_analyze)
        elif choice == "4":
            _safe_call(_do_meal_delete)
        elif choice == "b":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _meal_add_items(meal_id: int) -> None:
    """Interactive loop to add food/recipe items to an existing meal."""
    while True:
        state.console.print()
        state.console.print(f"  [{state.T['accent']}]1.[/{state.T['accent']}] Add a food item")
        state.console.print(f"  [{state.T['accent']}]2.[/{state.T['accent']}] Add a recipe (by serving)")
        state.console.print(f"  [dim]b.[/dim] Done / back")
        state.console.print(f"  [dim]q.[/dim] Quit")
        state.console.print()
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            break

        if choice == "1":
            food = _search_and_pick_food()
            if food is None:
                continue
            result = _pick_portion(food)
            if result is None:
                continue
            grams, label, _ = result
            with _db.get_db() as conn:
                _db.meal_add_food(conn, meal_id, food["fdcId"], food["name"], grams, label)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")

        elif choice == "2":
            _do_recipe_list()
            rid = _ask_int("Recipe ID")
            if rid is None:
                continue
            with _db.get_db() as conn:
                recipe = _db.recipe_get(conn, rid)
            if recipe is None:
                state.console.print(f"[{state.T['warning']}]Recipe not found.[/{state.T['warning']}]")
                continue
            try:
                raw_srv = _prompt("Recipe portion in servings  [dim](examples: 1, 1/2, 1.5 · b=back, q=quit)[/dim]",
                                  default="1").strip()
                lowered = raw_srv.lower()
                if not raw_srv or lowered in ("b", "back"):
                    continue
                if lowered == "q":
                    raise SystemExit(0)
                servings = _parse_serving_amount(raw_srv)
                if servings is None or servings <= 0:
                    raise ValueError
            except Cancelled:
                continue
            with _db.get_db() as conn:
                _db.meal_add_recipe(conn, meal_id, rid, recipe["name"], servings)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {recipe['name']}  {_format_recipe_portion_label(servings)}")

        elif choice in ("b", "d"):
            break
        elif choice == "q":
            raise SystemExit(0)
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_meal_log() -> None:
    try:
        meal_date = _ask_date("Date", default=date.today().isoformat())
    except Cancelled:
        return
    if meal_date is None:
        return

    try:
        name = _prompt("Meal name", default="Meal").strip() or "Meal"
    except Cancelled:
        return

    with _db.get_db() as conn:
        meal_id = _db.meal_create(conn, name, meal_date)
    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Meal [{state.T['hi']}]{name}[/{state.T['hi']}] "
                  f"on {meal_date} created (ID {meal_id}).")
    _meal_add_items(meal_id)
    state.console.print(f"[{state.T['success']}]Meal logged.[/{state.T['success']}]")


def _print_meal_items(meal_id: int, meal_name: str) -> list:
    """Print items for a meal and return the list of items."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
    state.console.print(f"\n  [{state.T['accent']}]{meal_name}[/{state.T['accent']}] (ID {meal_id})")
    if not items:
        state.console.print("    [dim]No items logged.[/dim]")
    else:
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None,
                    padding=(0, 1), pad_edge=False)
        tbl.add_column("ID", justify="right", min_width=4)
        tbl.add_column("Amount", min_width=10)
        tbl.add_column("Food / Recipe", min_width=30)
        for it in items:
            if it["item_type"] == "recipe":
                amount_label = _format_recipe_portion_label(float(it["amount"]))
            else:
                amount_label = _normalize_unit_display(it["unit"])
            tbl.add_row(str(it["id"]), amount_label, it["food_name"])
        state.console.print(tbl)
    return list(items)


def _do_meal_view_by_date() -> None:
    try:
        meal_date = _ask_date("Date", default=date.today().isoformat())
    except Cancelled:
        return
    if meal_date is None:
        return
    with _db.get_db() as conn:
        meals = _db.meal_list_by_date(conn, meal_date)
    if not meals:
        state.console.print(f"[dim]No meals logged for {meal_date}.[/dim]")
        return

    # Show all meals with their items
    for m in meals:
        _print_meal_items(m["id"], m["name"])

    def _pick_meal_id(verb: str) -> int | None:
        """Return a valid meal ID for the current day, or None on cancel/error.
        Skips the prompt when only one meal is on the day."""
        if len(meals) == 1:
            return meals[0]["id"]
        ids_hint = "/".join(str(m["id"]) for m in meals)
        try:
            raw = _prompt(f"Meal ID to {verb}  [dim]({ids_hint})[/dim]").strip()
        except Cancelled:
            return None
        try:
            mid = int(raw)
        except ValueError:
            mid = None
        if mid is None or not any(m["id"] == mid for m in meals):
            state.console.print(f"[{state.T['warning']}]Invalid meal ID.[/{state.T['warning']}]")
            return None
        return mid

    # Action loop
    while True:
        state.console.print()
        state.console.print(f"  [{state.T['accent']}]a.[/{state.T['accent']}] Add items to a meal")
        state.console.print(f"  [{state.T['accent']}]e.[/{state.T['accent']}] Edit an item amount")
        state.console.print(f"  [{state.T['accent']}]d.[/{state.T['accent']}] Delete an item from a meal")
        state.console.print(f"  [dim]b.[/dim] Back")
        state.console.print(f"  [dim]q.[/dim] Quit")
        state.console.print()
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            break

        if choice == "a":
            mid = _pick_meal_id("add items to")
            if mid is None:
                continue
            _meal_add_items(mid)
            # Refresh display for that meal
            meal_name = next(m["name"] for m in meals if m["id"] == mid)
            _print_meal_items(mid, meal_name)

        elif choice == "e":
            mid = _pick_meal_id("edit item in")
            if mid is None:
                continue
            meal_name = next(m["name"] for m in meals if m["id"] == mid)
            items = _print_meal_items(mid, meal_name)
            if not items:
                continue
            try:
                raw_iid = _prompt("Item ID to edit").strip()
            except Cancelled:
                continue
            iid = None
            try:
                iid = int(raw_iid)
            except ValueError:
                pass
            item = next((it for it in items if it["id"] == iid), None)
            if item is None:
                state.console.print(f"[{state.T['warning']}]Invalid item ID.[/{state.T['warning']}]")
                continue
            if item["item_type"] == "recipe":
                # Recipe items: edit number of servings
                try:
                    raw_sv = _prompt("Recipe portion in servings", default=str(item["amount"])).strip()
                except Cancelled:
                    continue
                try:
                    servings = _parse_serving_amount(raw_sv)
                    if servings is None or servings <= 0:
                        raise ValueError
                except ValueError:
                    state.console.print(f"[{state.T['warning']}]Enter a number.[/{state.T['warning']}]")
                    continue
                with _db.get_db() as conn:
                    _db.meal_update_item(conn, iid, mid, servings, item["unit"])
                state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Updated to {_format_recipe_portion_label(servings)}.")
            else:
                # Food items: loop until user is done editing
                cur_fdc_id   = item["fdc_id"]
                cur_name     = item["food_name"]
                cur_amount   = item["amount"]
                cur_unit     = item["unit"]
                changed = False

                while True:
                    amt_display = (f"{_normalize_unit_display(cur_unit)}  ({cur_amount:.0f} g)"
                                   if cur_amount and cur_amount > 0 and cur_unit and cur_unit != "—"
                                   else "—")
                    state.console.print(f"\n  [dim]Editing:[/dim] [bold]{cur_name}[/bold]  {amt_display}")
                    state.console.print(f"  [{state.T['accent']}]f.[/{state.T['accent']}] Change food (search by new name)")
                    state.console.print(f"  [{state.T['accent']}]a.[/{state.T['accent']}] Change amount")
                    state.console.print(f"  [dim]d / done  — save and exit[/dim]")
                    try:
                        sub = _prompt("Choice").strip().lower()
                    except Cancelled:
                        break
                    if sub in ("done", "d", "b", ""):
                        break

                    if sub == "f":
                        try:
                            query = _prompt("Search for food").strip()
                        except Cancelled:
                            continue
                        if not query:
                            continue
                        new_food = _search_and_pick_food(initial_query=query)
                        if new_food is None:
                            state.console.print(f"  [{state.T['warning']}]Food not changed "
                                          f"(selection cancelled or fetch failed).[/{state.T['warning']}]")
                            continue
                        cur_fdc_id = new_food["fdcId"]
                        cur_name   = new_food["name"]
                        changed = True
                        state.console.print(f"  [dim]Food set to: {cur_name}[/dim]")

                    elif sub == "a":
                        # Load food from cache (may be the newly chosen food)
                        with _db.get_db() as conn:
                            cached = _db.get_cached_food(conn, cur_fdc_id)
                        if cached is None:
                            state.console.print(f"[{state.T['warning']}]Food not in cache yet; add it first.[/{state.T['warning']}]")
                            continue
                        food_dict = {
                            "fdcId":       cached["fdc_id"],
                            "name":        cached["name"],
                            "dataType":    cached["data_type"],
                            "brand":       cached["brand"],
                            "servingSize": cached["serving_size"],
                            "servingUnit": cached["serving_unit"],
                            "nutrients":   json.loads(cached["nutrients_json"]),
                            "portions":    json.loads(cached["portions_json"]) if cached["portions_json"] else [],
                        }
                        result = _pick_portion(food_dict)
                        if result is None:
                            continue
                        cur_amount, cur_unit, _ = result
                        changed = True

                if changed:
                    with _db.get_db() as conn:
                        _db.meal_replace_food(conn, iid, mid, cur_fdc_id,
                                              cur_name, cur_amount, cur_unit)
                    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Saved: {cur_name}  "
                                  f"{_normalize_unit_display(cur_unit)}")
            _print_meal_items(mid, meal_name)

        elif choice == "d":
            mid = _pick_meal_id("delete item from")
            if mid is None:
                continue
            meal_name = next(m["name"] for m in meals if m["id"] == mid)
            items = _print_meal_items(mid, meal_name)
            if not items:
                continue
            try:
                raw_iid = _prompt("Item ID to delete").strip()
            except Cancelled:
                continue
            iid = None
            try:
                iid = int(raw_iid)
            except ValueError:
                pass
            if iid is None or not any(it["id"] == iid for it in items):
                state.console.print(f"[{state.T['warning']}]Invalid item ID.[/{state.T['warning']}]")
                continue
            with _db.get_db() as conn:
                removed = _db.meal_remove_item(conn, iid, mid)
            if removed:
                state.console.print(f"[{state.T['success']}]Item removed.[/{state.T['success']}]")
                _print_meal_items(mid, meal_name)
            else:
                state.console.print(f"[{state.T['warning']}]Could not remove item.[/{state.T['warning']}]")

        elif choice in ("b", ""):
            break
        elif choice == "q":
            raise SystemExit(0)
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _compute_meal_nutrients(meal_id: int) -> dict[str, float] | None:
    """Return combined nutrients for all items in a meal, or None if no data."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
    combined: dict[str, float] = {}
    for item in items:
        if item["item_type"] == "food":
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, item["fdc_id"])
            if cached:
                scaled = _usda.scale_nutrients(
                    json.loads(cached["nutrients_json"]), item["amount"], base_size=100.0
                )
                combined = _usda.sum_nutrients(combined, scaled)
        elif item["item_type"] == "recipe":
            with _db.get_db() as conn:
                ings = _db.recipe_get_ingredients(conn, item["recipe_id"])
                recipe = _db.recipe_get(conn, item["recipe_id"])
            if recipe and ings:
                recipe_total: dict[str, float] = {}
                for ing in ings:
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, ing["fdc_id"])
                    if cached:
                        scaled = _usda.scale_nutrients(
                            json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
                        )
                        recipe_total = _usda.sum_nutrients(recipe_total, scaled)
                # Scale by requested servings / total servings
                portion = item["amount"] / recipe["servings"]
                scaled_recipe = {k: v * portion for k, v in recipe_total.items()}
                combined = _usda.sum_nutrients(combined, scaled_recipe)
    return combined if combined else None


def _compute_meal_ingredient_list(meal_id: int) -> list[dict]:
    """
    Return per-ingredient data for a meal, suitable for meal-level DIAAS calculation.

    Each returned dict has:
        "food_name":      str
        "nutrients_100g": dict[str, float]   — USDA nutrients per 100g
        "grams":          float              — actual grams consumed

    Recipe items are expanded into their constituent ingredients (scaled by serving portion).
    """
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)

    def _best_nutrients(fdc_id: int, food_name: str) -> dict[str, float] | None:
        """Return the best available nutrient dict for a food, with AA data if possible."""
        refreshed = _refresh_cache_if_missing_aa(fdc_id)
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached is None:
            return None
        nutrients = refreshed if refreshed is not None else json.loads(cached["nutrients_json"])
        # If still missing AA data, try merging from the complement table
        if not _usda.has_amino_acid_data(nutrients):
            complement = _usda.get_complement_nutrients(food_name)
            if complement and _usda.has_amino_acid_data(complement):
                # Scale complement table AAs to match actual protein content
                actual_protein = nutrients.get("protein_g", 0)
                ref_protein = complement.get("protein_g", 0)
                if ref_protein > 0 and actual_protein > 0:
                    scale = actual_protein / ref_protein
                    merged = dict(nutrients)
                    for k, v in complement.items():
                        if k.startswith("aa_") and k not in merged:
                            merged[k] = v * scale
                    return merged
        return nutrients

    result: list[dict] = []
    for item in items:
        if item["item_type"] == "food":
            nutrients = _best_nutrients(item["fdc_id"], item["food_name"])
            if nutrients is not None:
                result.append({
                    "food_name":      item["food_name"],
                    "nutrients_100g": nutrients,
                    "grams":          item["amount"],
                })
        elif item["item_type"] == "recipe":
            with _db.get_db() as conn:
                ings = _db.recipe_get_ingredients(conn, item["recipe_id"])
                recipe = _db.recipe_get(conn, item["recipe_id"])
            if recipe and ings:
                portion = item["amount"] / recipe["servings"] if recipe["servings"] > 0 else 1.0
                for ing in ings:
                    nutrients = _best_nutrients(ing["fdc_id"], ing["food_name"])
                    if nutrients is not None:
                        result.append({
                            "food_name":      ing["food_name"],
                            "nutrients_100g": nutrients,
                            "grams":          ing["amount"] * portion,
                        })
    return result


def _do_meal_analyze() -> None:
    try:
        meal_date = _ask_date("Date", default=date.today().isoformat())
    except Cancelled:
        return
    if meal_date is None:
        return
    with _db.get_db() as conn:
        meals = _db.meal_list_by_date(conn, meal_date)
    if not meals:
        state.console.print(f"[dim]No meals for {meal_date}.[/dim]")
        return

    # If only one meal, analyze it directly; otherwise let user choose
    if len(meals) == 1:
        meal = meals[0]
    else:
        _do_meal_view_by_date.__wrapped__ = None   # already printed above if needed
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("ID",   justify="right", min_width=4)
        tbl.add_column("Name", min_width=24)
        for m in meals:
            tbl.add_row(str(m["id"]), m["name"])
        state.console.print(tbl)
        mid = _ask_int("Meal ID to analyze (0 = all meals for the day)")
        if mid is None:
            return
        if mid == 0:
            # Combine all meals for the day
            combined: dict[str, float] = {}
            all_ings: list[dict] = []
            with state.console.status("[dim]Fetching amino acid data…[/dim]", spinner="dots"):
                for m in meals:
                    n = _compute_meal_nutrients(m["id"])
                    if n:
                        combined = _usda.sum_nutrients(combined, n)
                    all_ings.extend(_compute_meal_ingredient_list(m["id"]))
            if combined:
                title = f"All meals — {meal_date}"
                _print_nutrient_table(combined, title=title)
                missing_aa = _print_meal_diaas(all_ings)
                aa_nutrients = _usda.sum_nutrients(*[
                    _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
                    for ing in all_ings
                    if _usda.has_amino_acid_data(ing["nutrients_100g"])
                ]) if all_ings else {}
                profile = _profile.load_profile()
                if profile:
                    _print_protein_adequacy(combined, profile, context_label=title)
                if not missing_aa:
                    _print_complement_suggestions(combined, context="meal", offer_if_covered=True)
                _offer_export(title, [
                    {"type": "nutrient_table", "title": title, "nutrients": combined},
                    {"type": "protein_completeness", "nutrients": combined},
                ])
            else:
                state.console.print(f"[dim]No nutrient data found.[/dim]")
            return
        matched = [m for m in meals if m["id"] == mid]
        if not matched:
            state.console.print(f"[{state.T['warning']}]Meal {mid} not found.[/{state.T['warning']}]")
            return
        meal = matched[0]

    nutrients = _compute_meal_nutrients(meal["id"])
    if nutrients is None:
        state.console.print("[dim]No nutrient data found for this meal. "
                      "Ensure all ingredients are in the cache.[/dim]")
        return
    _print_nutrient_table(nutrients,
                          title=f"{meal['name']} — {meal['meal_date']}")
    with state.console.status("[dim]Fetching amino acid data…[/dim]", spinner="dots"):
        ing_list = _compute_meal_ingredient_list(meal["id"])
    missing_aa = _print_meal_diaas(ing_list)
    if missing_aa:
        _fix_meal_aa_profiles(meal["id"], missing_aa)

    # Build nutrients from only AA-complete ingredients for protein completeness
    # and complement suggestions — mixing full protein with partial AA data
    # produces inflated gaps and unrealistic suggestion amounts.
    aa_nutrients = _usda.sum_nutrients(*[
        _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
        for ing in ing_list
        if _usda.has_amino_acid_data(ing["nutrients_100g"])
    ]) if ing_list else {}

    profile = _profile.load_profile()
    if profile:
        _print_protein_adequacy(nutrients, profile, context_label=f"{meal['name']} ({meal['meal_date']})")
    if not missing_aa:
        _print_complement_suggestions(nutrients, context="meal", offer_if_covered=True)


def _do_meal_delete() -> None:
    try:
        meal_date = _ask_date("Date", default=date.today().isoformat())
    except Cancelled:
        return
    if meal_date is None:
        return
    with _db.get_db() as conn:
        meals = _db.meal_list_by_date(conn, meal_date)
    if not meals:
        state.console.print(f"[dim]No meals for {meal_date}.[/dim]")
        return
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID",   justify="right", min_width=4)
    tbl.add_column("Name", min_width=24)
    for m in meals:
        tbl.add_row(str(m["id"]), m["name"])
    state.console.print(tbl)
    mid = _ask_int("Meal ID to delete")
    if mid is None:
        return
    matched = [m for m in meals if m["id"] == mid]
    if not matched:
        state.console.print(f"[{state.T['warning']}]Meal {mid} not found.[/{state.T['warning']}]")
        return
    meal = matched[0]
    try:
        confirm = _prompt(f"Delete [{state.T['hi']}]{meal['name']}[/{state.T['hi']}]?",
                          choices=["y", "n"], default="n")
    except Cancelled:
        return
    if confirm.lower() == "y":
        with _db.get_db() as conn:
            _db.meal_delete(conn, mid)
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Deleted.")
    else:
        state.console.print("[dim]Cancelled.[/dim]")
