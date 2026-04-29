"""
recipe_edit.py — recipe editing workflow for numa.

Contains _do_recipe_edit (menu option 4 "Edit recipe").  Called from recipes.py.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/recipe_edit.py — edit recipe workflow"
"""
import json
from datetime import datetime, timezone

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..services.portions import (
    _normalize_unit_display, _parse_portion_input, _pick_portion,
    _UNIT_TO_GRAMS, _VOLUME_TO_ML,
)
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food
from ..ui.common import _id_cell, ID_KEY, _open_in_editor, _safe_call, _show_menu, dot_cell, table_title, table_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_nutrient_table
from .recipes import _parse_measure, _compute_recipe_dcp, _compute_recipe_gl, _format_recipe_portion_label, _parse_serving_amount

def _do_recipe_edit(recipe=None) -> None:
    if recipe is None:
        from .recipes import _pick_recipe
        recipe = _pick_recipe()
    if recipe is None:
        return
    rid = recipe["id"]

    with _db.get_db() as conn:
        _db.recipe_touch(conn, rid)
    state.console.print(f"\n[{state.T['accent']}]Editing: {recipe['name']}[/{state.T['accent']}]")
    state.console.print("[dim]Press Enter to keep current value.  p = previous field,  b = back to menu.[/dim]\n")

    # Edit metadata (name/description/servings) with back-navigation.
    # _meta_complete stays True only if the user steps through every field.
    # On b / Ctrl+C we break early but still fall through to save whatever
    # was already changed before returning.
    _meta_fields = [
        ("Name",        "name",        recipe["name"],                "str"),
        ("Description", "description", recipe["description"] or "",   "str"),
        ("Servings  [dim](0 = analyze by weight/volume)[/dim]", "servings", str(recipe["servings"]), "int"),
        ("Serving size  [dim](e.g. 1 cup, 1 slice — Enter to skip)[/dim]", "serving_size", recipe["serving_size"] or "", "str"),
        ("Complete?  [dim](y/n)[/dim]", "complete", "y" if recipe["complete"] else "n", "bool"),
    ]
    _meta_vals: dict = {f[1]: f[2] for f in _meta_fields}
    _meta_complete = True
    _meta_quit = False
    _mi = 0
    while _mi < len(_meta_fields):
        _label, _key, _, _typ = _meta_fields[_mi]
        _cur = str(_meta_vals[_key])
        # Show current value in the label but NOT as _prompt default, so that
        # pressing Enter always returns "" and never falsely triggers b/p/q checks.
        _hint = f"(Press enter to keep [{state.T['default_hint']}]{_cur}[/{state.T['default_hint']}])"
        _display_label = f"{_label} {_hint}" if _cur else _label
        try:
            _raw = _prompt(_display_label, free_text=True).strip()
        except Cancelled:
            _meta_complete = False
            break
        if _raw.lower() == "q":
            _meta_complete = False
            _meta_quit = True
            break
        if _raw.lower() == "b":
            _meta_complete = False
            break
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
        elif _typ == "bool":
            if _val.lower() in ("y", "n", "yes", "no"):
                _meta_vals[_key] = "y" if _val.lower() in ("y", "yes") else "n"
            else:
                state.console.print(f"  [{state.T['warning']}]Enter y or n.[/{state.T['warning']}]")
                continue
        else:
            _meta_vals[_key] = _val
        _mi += 1
    name         = _meta_vals["name"]
    desc         = _meta_vals["description"]
    servings     = _meta_vals["servings"]
    serving_size = _meta_vals["serving_size"] or None
    complete     = _meta_vals["complete"] == "y"

    # Volume and weight — only prompt when the meta loop completed; otherwise
    # keep existing values so we don't prompt for more after a b/Ctrl+C.
    def _fmt_measure(val, unit) -> str:
        if val is None:
            return ""
        return f"{val:g} {unit}" if unit else f"{val:g}"

    if _meta_complete:
        cur_vol_str = _fmt_measure(recipe["total_volume"],  recipe["total_volume_unit"])
        cur_wt_str  = _fmt_measure(recipe["total_weight"],  recipe["total_weight_unit"])
        try:
            raw_vol = _prompt(
                "Total volume  [dim](e.g. 4 cups, 500 ml — Enter to skip)[/dim]",
                default=cur_vol_str, free_text=True,
            ).strip()
            total_volume, total_volume_unit = _parse_measure(raw_vol)
            raw_wt = _prompt(
                "Total weight  [dim](e.g. 800 g, 1.5 lb — Enter to skip)[/dim]",
                default=cur_wt_str, free_text=True,
            ).strip()
            total_weight, total_weight_unit = _parse_measure(raw_wt)
        except Cancelled:
            # Keep existing vol/wt; still proceed to ingredient management.
            total_volume      = recipe["total_volume"]
            total_volume_unit = recipe["total_volume_unit"]
            total_weight      = recipe["total_weight"]
            total_weight_unit = recipe["total_weight_unit"]
    else:
        total_volume      = recipe["total_volume"]
        total_volume_unit = recipe["total_volume_unit"]
        total_weight      = recipe["total_weight"]
        total_weight_unit = recipe["total_weight_unit"]

    # Always save any meta changes made before the exit point.
    meta_changed = (
        name != recipe["name"]
        or desc != (recipe["description"] or "")
        or servings != recipe["servings"]
        or serving_size != (recipe["serving_size"] or None)
        or complete != bool(recipe["complete"])
        or total_volume  != recipe["total_volume"]
        or total_volume_unit != (recipe["total_volume_unit"] or None)
        or total_weight  != recipe["total_weight"]
        or total_weight_unit != (recipe["total_weight_unit"] or None)
    )
    if meta_changed:
        with _db.get_db() as conn:
            _db.recipe_update(conn, rid, name, desc, servings, recipe["instructions"] or "",
                              total_volume, total_volume_unit, total_weight, total_weight_unit,
                              serving_size, complete)
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Recipe details updated.")

    # If the user backed out during meta/vol/wt prompts, stop here — changes above are saved.
    if not _meta_complete:
        if _meta_quit:
            raise SystemExit(0)
        return

    # Show and manage ingredients
    # done=True means proceed to instructions; False means back/cancel
    ingredients_done = False
    ingredients_changed = False
    while True:
        with _db.get_db() as conn:
            ingredients = _db.recipe_get_ingredients(conn, rid)

        if ingredients:
            table_title("CURRENT RECIPE INGREDIENTS")
            has_notes = any(ing["notes"] for ing in ingredients)
            _RFOOD_W = 36
            tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl.add_column("#",    justify="right", min_width=3)
            tbl.add_column("Amount", min_width=14)
            tbl.add_column("ID", justify="right", min_width=7)
            tbl.add_column("Food", min_width=_RFOOD_W, max_width=_RFOOD_W, no_wrap=True)
            if has_notes:
                tbl.add_column("Note", min_width=20)
            for i, ing in enumerate(ingredients, 1):
                id_cell = "[dim]recipe[/dim]" if ing["ref_recipe_id"] else _id_cell(ing["fdc_id"])
                row = [str(i), _normalize_unit_display(ing["unit"]), id_cell, dot_cell(ing["food_name"], _RFOOD_W)]
                if has_notes:
                    row.append(ing["notes"] or "")
                tbl.add_row(*row)
            state.console.print(tbl)
            table_footer(f"  {ID_KEY}")
        else:
            state.console.print("[dim]No ingredients yet.[/dim]")

        _show_menu("Ingredients", [
            ("1", "Add ingredient"),
            ("2", "Edit ingredient"),
            ("3", "Remove ingredient"),
            ("4", "Reorder ingredients"),
            ("d", "Done — proceed to Procedure"),
            ("b", "Done — proceed to Procedure"),
            ("m", "Return to main menu  [dim](skips Procedure)[/dim]"),
            ("q", "Quit  [dim](skips Procedure)[/dim]"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            break

        if choice in ("b", "d"):
            ingredients_done = True
            break
        if choice == "m":
            raise ReturnToMain()
        if choice == "q":
            raise SystemExit(0)
        elif choice == "1":
            state.console.print()
            try:
                query = _prompt("Search food or recipe", free_text=True).strip()
            except Cancelled:
                continue
            ql = query.lower()
            if not query or ql == "b":
                continue
            if ql == "m":
                raise ReturnToMain()
            if ql == "q":
                raise SystemExit(0)
            with _db.get_db() as conn:
                all_recipes = _db.recipe_list(conn)
            query_words = ql.split()
            matching_recipes = sorted(
                [r for r in all_recipes
                 if r["id"] != rid and any(w in r["name"].lower() for w in query_words)],
                key=lambda r: (-sum(1 for w in query_words if w in r["name"].lower()), r["name"].lower()),
            )
            food = _search_and_pick_food(
                initial_query=query,
                prepend_recipes=matching_recipes or None,
            )
            if food is None:
                continue

            if food.get("_type") == "recipe":
                sub_rid  = food["id"]
                sub_name = food["name"]
                try:
                    raw_srv = _prompt(
                        "Servings of this recipe  [dim](e.g. 1, 0.5, 2 — b=back)[/dim]",
                        default="1",
                    ).strip()
                except Cancelled:
                    continue
                if not raw_srv or raw_srv.lower() == "b":
                    continue
                servings = _parse_serving_amount(raw_srv)
                if servings is None or servings <= 0:
                    state.console.print(f"[{state.T['warning']}]Enter a positive number.[/{state.T['warning']}]")
                    continue
                try:
                    notes = _prompt("Note  [dim](optional, Enter to skip)[/dim]", default="", free_text=True).strip() or None
                except Cancelled:
                    notes = None
                label = _format_recipe_portion_label(servings)
                with _db.get_db() as conn:
                    _db.recipe_add_ingredient(conn, rid, 0, sub_name, servings, "servings", notes, ref_recipe_id=sub_rid)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added recipe: {sub_name}  {label}")
                ingredients_changed = True
            else:
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

            if ing["ref_recipe_id"]:
                try:
                    raw_srv = _prompt(
                        f"Servings  [dim](current: {ing['amount']:g})[/dim]",
                        default=str(ing["amount"]),
                    ).strip()
                except Cancelled:
                    continue
                servings = _parse_serving_amount(raw_srv)
                if servings is None or servings <= 0:
                    state.console.print(f"[{state.T['warning']}]Enter a positive number.[/{state.T['warning']}]")
                    continue
                try:
                    notes_new = _prompt("Note  [dim](Enter to keep current)[/dim]", default=ing["notes"] or "", free_text=True).strip() or None
                except Cancelled:
                    notes_new = ing["notes"]
                with _db.get_db() as conn:
                    _db.recipe_update_ingredient(conn, ing["id"], servings, "servings", ing["food_name"], notes_new)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Updated to {_format_recipe_portion_label(servings)}.")
                ingredients_changed = True
                continue

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
                    f"Name (Press enter to keep [{state.T['default_hint']}]{ing['food_name']}[/{state.T['default_hint']}])",
                    free_text=True
                ).strip() or ing["food_name"]
            except Cancelled:
                continue
            unit_display = _normalize_unit_display(ing["unit"]) if ing["unit"] else None
            if ing["amount"]:
                amt_str = f"{ing['amount']:.4g} g"
                # Only append gram weight if it isn't already expressed in the unit string
                if unit_display and amt_str not in unit_display:
                    cur_portion = f"{unit_display}  ({amt_str})"
                else:
                    cur_portion = unit_display or amt_str
            else:
                cur_portion = unit_display  # volume only — no gram weight yet
            result = _pick_portion(food, current=cur_portion,
                                   current_grams=ing["amount"], current_label=ing["unit"] or "")
            if result is None:
                continue
            grams, label, _ = result
            state.console.print(f"  Portion set to: [{state.T['hi']}]{label}[/{state.T['hi']}]")
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
            while True:
                with _db.get_db() as conn:
                    ingredients = _db.recipe_get_ingredients(conn, rid)
                if not ingredients:
                    state.console.print("[dim]No ingredients remaining.[/dim]")
                    break
                _RFOOD_W2 = 36
                tbl2 = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
                tbl2.add_column("#", justify="right", min_width=3)
                tbl2.add_column("Amount", min_width=14)
                tbl2.add_column("Food", min_width=_RFOOD_W2, max_width=_RFOOD_W2, no_wrap=True)
                for i, ing in enumerate(ingredients, 1):
                    tbl2.add_row(str(i), _normalize_unit_display(ing["unit"]), ing["food_name"])
                state.console.print(tbl2)
                try:
                    raw_idx = _prompt("Ingredient # to remove  [dim](d=done)[/dim]", free_text=True).strip().lower()
                except Cancelled:
                    break
                if raw_idx in ("d", "b", ""):
                    break
                if raw_idx == "m":
                    raise ReturnToMain()
                if raw_idx == "q":
                    raise SystemExit(0)
                try:
                    idx = int(raw_idx)
                except ValueError:
                    state.console.print(f"[{state.T['warning']}]Enter a number or d.[/{state.T['warning']}]")
                    continue
                if idx < 1 or idx > len(ingredients):
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
            gl, gl_blockers = _compute_recipe_gl(rid)
            with _db.get_db() as conn:
                _db.recipe_set_gl(conn, rid, gl if not gl_blockers else None)
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
                          recipe["servings"], instructions,
                          recipe["total_volume"], recipe["total_volume_unit"],
                          recipe["total_weight"], recipe["total_weight_unit"],
                          recipe["serving_size"], bool(recipe["complete"]))
    if ingredients_changed:
        dcp = _compute_recipe_dcp(rid)
        ts = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat() if dcp is not None else None
        with _db.get_db() as conn:
            _db.recipe_set_dcp(conn, rid, dcp, ts)
        gl, gl_blockers = _compute_recipe_gl(rid)
        with _db.get_db() as conn:
            _db.recipe_set_gl(conn, rid, gl if not gl_blockers else None)
    state.console.print(f"[{state.T['success']}]Recipe saved.[/{state.T['success']}]")


