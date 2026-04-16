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
from ..ui.prompts import Cancelled, ReturnToMain, _ask_date, _ask_int, _prompt
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
            _db.meal_add_food(conn, meal_id, food["fdcId"], food["name"], grams, label, item["notes"] or None)

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
            ("1", "Log a meal  (add to today's or create new)"),
            ("2", "View / edit a meal"),
            ("3", "Analyze a meal"),
            ("4", "Delete a meal"),
            ("m", "Return to main menu"),
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
        elif choice == "m":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _meal_add_items(meal_id: int) -> None:
    """Interactive loop to add food or recipe items to an existing meal.
    A single search finds both saved recipes (shown first as R#) and USDA/OFF foods."""
    state.console.print(f"\n  Search for a food or recipe name to add (Enter/b=back, m=main, q=quit)")
    while True:
        state.console.print()
        try:
            query = _prompt("Search", free_text=True).strip()
        except Cancelled:
            break
        ql = query.lower()
        if not query or ql == "b":
            break
        if ql == "m":
            raise ReturnToMain()
        if ql == "q":
            raise SystemExit(0)

        # Find matching recipes instantly from local DB
        with _db.get_db() as conn:
            all_recipes = _db.recipe_list(conn)
        query_words = ql.split()
        matching_recipes = [
            r for r in all_recipes
            if any(w in r["name"].lower() for w in query_words)
        ]

        result = _search_and_pick_food(
            initial_query=query,
            prepend_recipes=matching_recipes or None,
            allow_research=False,
        )
        if result is None:
            continue

        if result.get("_type") == "recipe":
            rid      = result["id"]
            rname    = result["name"]
            try:
                raw_srv = _prompt(
                    "Recipe portion in servings  [dim](examples: 1, 1/2, 1.5 · b=back, m=main, q=quit)[/dim]",
                    default="1",
                ).strip()
                lowered = raw_srv.lower()
                if not raw_srv or lowered in ("b", "back"):
                    continue
                if lowered == "m":
                    raise ReturnToMain()
                if lowered == "q":
                    raise SystemExit(0)
                servings = _parse_serving_amount(raw_srv)
                if servings is None or servings <= 0:
                    state.console.print(f"[{state.T['warning']}]Enter a positive number (e.g. 1, 1/2, 1.5).[/{state.T['warning']}]")
                    continue
            except Cancelled:
                continue
            with _db.get_db() as conn:
                _db.meal_add_recipe(conn, meal_id, rid, rname, servings)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {rname}  {_format_recipe_portion_label(servings)}")

        else:
            food = result
            portion = _pick_portion(food)
            if portion is None:
                continue
            grams, label, _ = portion
            try:
                notes = _prompt("Note for this item  [dim](optional, Enter to skip)[/dim]", default="", free_text=True).strip() or None
            except Cancelled:
                notes = None
            with _db.get_db() as conn:
                _db.meal_add_food(conn, meal_id, food["fdcId"], food["name"], grams, label, notes)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")


def _do_meal_log() -> None:
    today = date.today().isoformat()
    with _db.get_db() as conn:
        existing = _db.meal_list_by_date(conn, today)

    if existing:
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",    justify="right", min_width=3)
        tbl.add_column("ID",   justify="right", min_width=4)
        tbl.add_column("Meal", min_width=28)
        for i, m in enumerate(existing, 1):
            tbl.add_row(str(i), str(m["id"]), m["name"])
        state.console.print(f"\n  [dim]You already have {len(existing)} meal(s) logged today:[/dim]")
        state.console.print(tbl)
        try:
            raw = _prompt(
                "Add items to an existing meal (#), or log a new one  [dim](n=new, b=back, m=main)[/dim]"
            ).strip().lower()
        except Cancelled:
            return
        if raw in ("b", ""):
            return
        if raw == "m":
            raise ReturnToMain()
        if raw == "q":
            raise SystemExit(0)
        if raw != "n":
            try:
                idx = int(raw)
                if 1 <= idx <= len(existing):
                    _meal_add_items(existing[idx - 1]["id"])
                    state.console.print(f"[{state.T['success']}]Items added.[/{state.T['success']}]")
                    return
            except ValueError:
                pass
            state.console.print(f"[{state.T['warning']}]Enter a row number or n.[/{state.T['warning']}]")
            return

    try:
        meal_date = _ask_date("Date", default=today)
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
                name_cell = it["food_name"]
            else:
                amount_label = _normalize_unit_display(it["unit"])
                name_cell = f"[dim]{it['fdc_id']}[/dim]  {it['food_name']}"
            tbl.add_row(str(it["id"]), amount_label, name_cell)
        state.console.print(tbl)
    return list(items)


_MEAL_PAGE = 9


def _pick_meal(verb: str = "work with") -> "sqlite3.Row | None":
    """
    Show the most-recent meals in pages of 9, let the user pick one by row #,
    page forward with 'more', or jump to a date with 'd'.
    Returns the selected meal Row, or None if cancelled.
    """
    import sqlite3
    offset = 0
    while True:
        with _db.get_db() as conn:
            meals = _db.meal_list_recent(conn, limit=_MEAL_PAGE + 1, offset=offset)
        has_more = len(meals) > _MEAL_PAGE
        page = meals[:_MEAL_PAGE]

        if not page:
            if offset == 0:
                state.console.print("[dim]No meals logged yet.[/dim]")
            else:
                state.console.print("[dim]No more meals.[/dim]")
            return None

        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("ID",    justify="right", min_width=4)
        tbl.add_column("Date",  min_width=12)
        tbl.add_column("Meal",  min_width=28)
        tbl.add_column("Items", justify="right", min_width=5)
        for m in page:
            tbl.add_row(str(m["id"]), m["meal_date"], m["name"], str(m["item_count"]))
        state.console.print(tbl)

        hints = ["id=pick"]
        if has_more:
            hints.append("more=older")
        if offset > 0:
            hints.append("prev=newer")
        hints += ["d=by date", "b=back", "m=main"]
        try:
            raw = _prompt(f"Select meal to {verb}  [dim]({', '.join(hints)})[/dim]").strip().lower()
        except Cancelled:
            return None

        if raw in ("b", ""):
            return None
        if raw == "m":
            raise ReturnToMain()
        if raw == "q":
            raise SystemExit(0)
        if raw == "more" and has_more:
            offset += _MEAL_PAGE
            continue
        if raw == "prev" and offset > 0:
            offset = max(0, offset - _MEAL_PAGE)
            continue
        if raw == "d":
            try:
                meal_date = _ask_date("Date", default=date.today().isoformat())
            except Cancelled:
                continue
            if meal_date is None:
                continue
            with _db.get_db() as conn:
                date_meals = _db.meal_list_by_date(conn, meal_date)
            if not date_meals:
                state.console.print(f"[{state.T['warning']}]No meals for {meal_date}.[/{state.T['warning']}]")
                continue
            if len(date_meals) == 1:
                return date_meals[0]
            tbl2 = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl2.add_column("ID",   justify="right", min_width=4)
            tbl2.add_column("Meal", min_width=28)
            for m in date_meals:
                tbl2.add_row(str(m["id"]), m["name"])
            state.console.print(tbl2)
            try:
                raw2 = _prompt("Meal ID").strip()
            except Cancelled:
                continue
            try:
                picked_id = int(raw2)
                match = next((m for m in date_meals if m["id"] == picked_id), None)
                if match is not None:
                    return match
            except ValueError:
                pass
            state.console.print(f"[{state.T['warning']}]Invalid ID.[/{state.T['warning']}]")
            continue
        try:
            picked_id = int(raw)
            match = next((m for m in page if m["id"] == picked_id), None)
            if match is not None:
                return match
        except ValueError:
            pass
        state.console.print(f"[{state.T['warning']}]Enter a meal ID from the list{', more, prev,' if has_more else ','} d, or b.[/{state.T['warning']}]")


def _do_meal_view_by_date() -> None:
    while True:
        meal = _pick_meal("view / edit")
        if meal is None:
            return
        meal_id   = meal["id"]
        meal_date = meal["meal_date"]
        meal_name = meal["name"]

        # Show only the selected meal's items
        _print_meal_items(meal_id, meal_name)

        def _sibling_meals() -> list:
            """Other meals on the same date (for merge option)."""
            with _db.get_db() as conn:
                return [m for m in _db.meal_list_by_date(conn, meal_date) if m["id"] != meal_id]

        # Action loop; break with _back_to_list=True to re-show meal picker
        _back_to_list = False
        while True:
            siblings = _sibling_meals()
            menu_items = [
                ("1", "Add items"),
                ("2", "Edit an item"),
                ("3", "Delete an item"),
                ("4", "Delete this meal"),
            ]
            if siblings:
                menu_items.append(("5", "Merge with meal(s) on same date"))
            menu_items += [
                ("b", "Back to previous menu"),
                ("m", "Return to main menu"),
                ("q", "Quit"),
            ]
            _show_menu(f"Actions — {meal_name}", menu_items)
            try:
                choice = _prompt("Choice").strip().lower()
            except Cancelled:
                break

            if choice == "1":
                _meal_add_items(meal_id)
                _print_meal_items(meal_id, meal_name)

            elif choice == "2":
                items = _print_meal_items(meal_id, meal_name)
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
                        _db.meal_update_item(conn, iid, meal_id, servings, item["unit"])
                    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Updated to {_format_recipe_portion_label(servings)}.")
                else:
                    # Food items: loop until user is done editing
                    cur_fdc_id = item["fdc_id"]
                    cur_name   = item["food_name"]
                    cur_amount = item["amount"]
                    cur_unit   = item["unit"]
                    cur_notes  = item["notes"] or ""
                    changed    = False

                    while True:
                        amt_display = (f"{_normalize_unit_display(cur_unit)}  ({cur_amount:.0f} g)"
                                       if cur_amount and cur_amount > 0 and cur_unit and cur_unit != "—"
                                       else "—")
                        notes_display = f"  [dim]Note: {cur_notes}[/dim]" if cur_notes else ""
                        state.console.print(f"\n  [dim]Editing:[/dim] [bold]{cur_name}[/bold]  {amt_display}{notes_display}")
                        state.console.print(f"  [{state.T['accent']}]f.[/{state.T['accent']}] Change food (search by new name)")
                        state.console.print(f"  [{state.T['accent']}]a.[/{state.T['accent']}] Change amount")
                        state.console.print(f"  [{state.T['accent']}]n.[/{state.T['accent']}] Edit note")
                        state.console.print(f"  [dim]d / done  — save and exit[/dim]")
                        try:
                            sub = _prompt("Choice").strip().lower()
                        except Cancelled:
                            break
                        if sub in ("b", "d", "done", ""):
                            break
                        if sub == "q":
                            raise SystemExit(0)

                        if sub == "n":
                            try:
                                new_notes = _prompt("Note  [dim](Enter to clear)[/dim]", default=cur_notes, free_text=True).strip()
                            except Cancelled:
                                continue
                            cur_notes = new_notes
                            changed = True

                        elif sub == "f":
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
                            _db.meal_replace_food(conn, iid, meal_id, cur_fdc_id,
                                                  cur_name, cur_amount, cur_unit,
                                                  cur_notes or None)
                        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Saved: {cur_name}  "
                                      f"{_normalize_unit_display(cur_unit)}")
                _print_meal_items(meal_id, meal_name)

            elif choice == "3":
                items = _print_meal_items(meal_id, meal_name)
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
                    removed = _db.meal_remove_item(conn, iid, meal_id)
                if removed:
                    state.console.print(f"[{state.T['success']}]Item removed.[/{state.T['success']}]")
                    _print_meal_items(meal_id, meal_name)
                else:
                    state.console.print(f"[{state.T['warning']}]Could not remove item.[/{state.T['warning']}]")

            elif choice == "4":
                try:
                    confirm = _prompt(f"Delete '{meal_name}'?  [dim](y/n)[/dim]", default="n").strip().lower()
                except Cancelled:
                    continue
                if confirm != "y":
                    continue
                with _db.get_db() as conn:
                    _db.meal_delete(conn, meal_id)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Deleted: {meal_name}")
                break

            elif choice == "5" and siblings:
                # siblings already loaded at top of loop; show all meals on date including current
                with _db.get_db() as conn:
                    all_on_date = _db.meal_list_by_date(conn, meal_date)
                ids_str = "  ".join(f"{m['id']}={m['name']}" for m in all_on_date)
                state.console.print(f"  [dim]Meals on {meal_date}: {ids_str}[/dim]")
                try:
                    raw_ids = _prompt(
                        "Meal IDs to merge  [dim](space-separated, or 'all', b=back, m=main)[/dim]",
                        default="all",
                    ).strip().lower()
                except Cancelled:
                    continue
                if raw_ids in ("b", ""):
                    continue
                if raw_ids == "m":
                    raise ReturnToMain()
                if raw_ids == "q":
                    raise SystemExit(0)

                if raw_ids == "all":
                    selected = list(all_on_date)
                else:
                    selected_ids = []
                    valid = True
                    for tok in raw_ids.split():
                        try:
                            selected_ids.append(int(tok))
                        except ValueError:
                            state.console.print(f"[{state.T['warning']}]Invalid ID: {tok}[/{state.T['warning']}]")
                            valid = False
                            break
                    if not valid:
                        continue
                    selected = [m for m in all_on_date if m["id"] in selected_ids]
                    missing = set(selected_ids) - {m["id"] for m in selected}
                    if missing:
                        state.console.print(f"[{state.T['warning']}]IDs not found: {' '.join(str(x) for x in missing)}[/{state.T['warning']}]")
                        continue
                    if len(selected) < 2:
                        state.console.print(f"[{state.T['warning']}]Select at least 2 meals to merge.[/{state.T['warning']}]")
                        continue

                default_name = selected[0]["name"]
                try:
                    new_name = _prompt("Name for merged meal", default=default_name, prefill=True).strip() or default_name
                except Cancelled:
                    continue

                with _db.get_db() as conn:
                    new_mid = _db.meal_create(conn, new_name, meal_date)
                    total_items = sum(_db.meal_copy_items(conn, m["id"], new_mid) for m in selected)

                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Created '{new_name}' "
                              f"(ID {new_mid}) with {total_items} item(s).")
                try:
                    del_orig = _prompt("Delete original meals?  [dim](y/n)[/dim]", default="y").strip().lower()
                except Cancelled:
                    del_orig = "n"
                if del_orig == "y":
                    with _db.get_db() as conn:
                        for m in selected:
                            _db.meal_delete(conn, m["id"])
                    state.console.print(f"  [dim]Deleted {len(selected)} original meal(s).[/dim]")
                # If the current meal was deleted, exit the action loop
                if del_orig == "y" and any(m["id"] == meal_id for m in selected):
                    break
                # Otherwise show the current meal's items (may be unchanged or deleted)
                _print_meal_items(new_mid, new_name)

            elif choice in ("b", ""):
                _back_to_list = True
                break
            elif choice == "m":
                raise ReturnToMain()
            elif choice == "q":
                raise SystemExit(0)
            else:
                state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")

        if not _back_to_list:
            return
        # _back_to_list=True: loop back to _pick_meal


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
                    "fdc_id":         item["fdc_id"],
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
                            "fdc_id":         ing["fdc_id"],
                            "nutrients_100g": nutrients,
                            "grams":          ing["amount"] * portion,
                        })
    return result


def _do_meal_analyze() -> None:
    meal = _pick_meal("analyze")
    if meal is None:
        return
    meal_date = meal["meal_date"]

    # Offer to analyze just this meal or all meals on the same date
    with _db.get_db() as conn:
        meals = _db.meal_list_by_date(conn, meal_date)

    if len(meals) > 1:
        try:
            scope = _prompt(
                f"Analyze just [{state.T['hi']}]{meal['name']}[/{state.T['hi']}]"
                f" or all {len(meals)} meals on {meal_date}?",
                choices=["1", "2"],
                default="1",
            )
        except Cancelled:
            return
        if scope == "2":
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
                missing_aa, _dcp_g = _print_meal_diaas(all_ings)
                aa_nutrients = _usda.sum_nutrients(*[
                    _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
                    for ing in all_ings
                    if _usda.has_amino_acid_data(ing["nutrients_100g"])
                ]) if all_ings else {}
                profile = _profile.load_profile()
                if profile:
                    _print_protein_adequacy(combined, profile, context_label=title, dcp_g=_dcp_g)
                if aa_nutrients:
                    _print_complement_suggestions(aa_nutrients, context="meal", offer_if_covered=True)
                _offer_export(title, [
                    {"type": "nutrient_table", "title": title, "nutrients": combined},
                    {"type": "protein_completeness", "nutrients": combined},
                ])
            else:
                state.console.print("[dim]No nutrient data found.[/dim]")
            return

    nutrients = _compute_meal_nutrients(meal["id"])
    if nutrients is None:
        state.console.print("[dim]No nutrient data found for this meal. "
                      "Ensure all ingredients are in the cache.[/dim]")
        return
    _print_nutrient_table(nutrients,
                          title=f"{meal['name']} — {meal['meal_date']}")
    with state.console.status("[dim]Fetching amino acid data…[/dim]", spinner="dots"):
        ing_list = _compute_meal_ingredient_list(meal["id"])
    missing_aa, _dcp_g = _print_meal_diaas(ing_list)
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
        _print_protein_adequacy(nutrients, profile, context_label=f"{meal['name']} ({meal['meal_date']})", dcp_g=_dcp_g)
    if aa_nutrients:
        _print_complement_suggestions(aa_nutrients, context="meal", offer_if_covered=True)


def _do_meal_delete() -> None:
    meal = _pick_meal("delete")
    if meal is None:
        return
    try:
        confirm = _prompt(
            f"Delete [{state.T['hi']}]{meal['name']}[/{state.T['hi']}]"
            f" ({meal['meal_date']})?",
            choices=["y", "n"], default="n",
        )
    except Cancelled:
        return
    if confirm.lower() == "y":
        with _db.get_db() as conn:
            _db.meal_delete(conn, meal["id"])
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Deleted.")
    else:
        state.console.print("[dim]Cancelled.[/dim]")
