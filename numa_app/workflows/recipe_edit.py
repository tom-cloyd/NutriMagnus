"""
recipe_edit.py — recipe editing workflow for numa.

Contains _do_recipe_edit (menu option 4 "Edit recipe").  Called from recipes.py.
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
from ..ui.common import _id_cell, ID_KEY, _open_in_editor, _safe_call
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_nutrient_table
from .recipes import _do_recipe_list, _parse_measure, _compute_recipe_dcp

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

    # Edit metadata (name/description/servings) with back-navigation.
    # _meta_complete stays True only if the user steps through every field.
    # On b / Ctrl+C we break early but still fall through to save whatever
    # was already changed before returning.
    _meta_fields = [
        ("Name",        "name",        recipe["name"],                "str"),
        ("Description", "description", recipe["description"] or "",   "str"),
        ("Servings  [dim](0 = analyze by weight/volume)[/dim]", "servings", str(recipe["servings"]), "int"),
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
        else:
            _meta_vals[_key] = _val
        _mi += 1
    name     = _meta_vals["name"]
    desc     = _meta_vals["description"]
    servings = _meta_vals["servings"]

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
            # Keep whatever volume/weight existed; still save meta changes above.
            total_volume      = recipe["total_volume"]
            total_volume_unit = recipe["total_volume_unit"]
            total_weight      = recipe["total_weight"]
            total_weight_unit = recipe["total_weight_unit"]
            _meta_complete = False
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
        or total_volume  != recipe["total_volume"]
        or total_volume_unit != (recipe["total_volume_unit"] or None)
        or total_weight  != recipe["total_weight"]
        or total_weight_unit != (recipe["total_weight_unit"] or None)
    )
    if meta_changed:
        with _db.get_db() as conn:
            _db.recipe_update(conn, rid, name, desc, servings, recipe["instructions"] or "",
                              total_volume, total_volume_unit, total_weight, total_weight_unit)
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
            state.console.print()
            state.console.print(f"[{state.T['accent']}]Current recipe ingredients[/{state.T['accent']}]  {ID_KEY}")
            has_notes = any(ing["notes"] for ing in ingredients)
            tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl.add_column("#",    justify="right", min_width=3)
            tbl.add_column("Amount", min_width=14)
            tbl.add_column("ID", justify="right", min_width=7)
            tbl.add_column("Food", min_width=32)
            if has_notes:
                tbl.add_column("Note", min_width=20)
            for i, ing in enumerate(ingredients, 1):
                row = [str(i), _normalize_unit_display(ing["unit"]), _id_cell(ing["fdc_id"]), ing["food_name"]]
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
                          recipe["servings"], instructions,
                          recipe["total_volume"], recipe["total_volume_unit"],
                          recipe["total_weight"], recipe["total_weight_unit"])
    if ingredients_changed:
        dcp = _compute_recipe_dcp(rid)
        ts = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat() if dcp is not None else None
        with _db.get_db() as conn:
            _db.recipe_set_dcp(conn, rid, dcp, ts)
    state.console.print(f"[{state.T['success']}]Recipe saved.[/{state.T['success']}]")


