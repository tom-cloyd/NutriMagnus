"""
recipe_edit.py — recipe editing workflow for numa.

Contains _do_recipe_edit (menu option 4 "Edit recipe").  Called from recipes.py.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/recipe_edit.py — edit recipe workflow"
"""
import json
import re
from datetime import datetime, timezone

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..services.portions import (
    _normalize_unit_display, _ing_amount_display, _parse_portion_input, _pick_portion,
    _try_resolve_unknown_weight, _UNIT_TO_GRAMS, _VOLUME_TO_ML,
)
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food
from ..ui.common import _id_cell, ID_KEY, _open_in_editor, _safe_call, _show_menu, dot_cell, table_title, table_footer, help_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_nutrient_table
from ..services.reports import _offer_export
from .recipes import _parse_measure, _compute_recipe_dcp, _compute_recipe_gl, _compute_recipe_protein_summary, _format_recipe_portion_label, _parse_serving_amount, _recipe_ing_id_cell

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
    state.console.print("[grey62]Press Enter to keep current value.  p = previous field,  b or Ctrl+C = back to menu.[/grey62]\n")

    # Edit metadata (name/description/servings) with back-navigation.
    # _meta_complete stays True only if the user steps through every field.
    # On b / Ctrl+C we break early but still fall through to save whatever
    # was already changed before returning.
    # (label, key, initial_value, type, allow_empty)
    _meta_fields = [
        ("[underline]Name[/underline]",        "name",        recipe["name"],                "str",  False),
        ("[underline]Description[/underline]", "description", recipe["description"] or "",   "str",  True),
        ("[underline]Servings[/underline]  [grey62](0 = analyze by weight/volume)[/grey62]", "servings", str(recipe["servings"]), "serving", False),
        ("[underline]Serving size[/underline]  [grey62](e.g. 1 cup, 1 slice — Enter to skip)[/grey62]", "serving_size", recipe["serving_size"] or "", "str", True),
        ("[underline]Complete?[/underline]  [grey62](y/n)[/grey62]", "complete", "y" if recipe["complete"] else "n", "bool", False),
    ]
    _meta_vals: dict = {f[1]: f[2] for f in _meta_fields}
    _meta_complete = True
    _meta_quit = False
    _mi = 0
    while _mi < len(_meta_fields):
        _label, _key, _, _typ, _allow_empty = _meta_fields[_mi]
        _cur = str(_meta_vals[_key])
        try:
            if _cur:
                _raw = _prompt(_label, default=_cur, prefill=True, free_text=True, two_line=True, allow_empty=_allow_empty).strip()
            else:
                _raw = _prompt(_label, free_text=True, two_line=True).strip()
        except Cancelled:
            _meta_complete = False
            state.console.print("  [grey62]Cancelled.[/grey62]")
            break
        if _raw.lower() == "q":
            _meta_complete = False
            _meta_quit = True
            break
        if _raw.lower() == "m":
            raise ReturnToMain()
        if _raw.lower() == "b":
            _meta_complete = False
            break
        if _raw.lower() == "p":
            if _mi > 0:
                _mi -= 1
            continue
        _val = _raw if _raw else _meta_vals[_key]
        if _typ == "serving":
            _sv = _parse_serving_amount(_val)
            if _sv is not None and _sv >= 0:
                _meta_vals[_key] = _sv
            else:
                state.console.print(f"  [{state.T['warning']}]Enter a number (e.g. 4, 1.5, 1/2, or 0).[/{state.T['warning']}]")
                continue
        elif _typ == "int":
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
                "[underline]Total volume[/underline]  [grey62](e.g. 4 cups, 500 ml — Enter to skip)[/grey62]",
                default=cur_vol_str, prefill=bool(cur_vol_str), free_text=True, two_line=True,
            ).strip()
            total_volume, total_volume_unit = _parse_measure(raw_vol)
            raw_wt = _prompt(
                "[underline]Total weight[/underline]  [grey62](e.g. 800 g, 1.5 lb — Enter to skip)[/grey62]",
                default=cur_wt_str, prefill=bool(cur_wt_str), free_text=True, two_line=True,
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

    # Resolve any 'weight not known' ingredient labels using current cache data.
    with _db.get_db() as conn:
        for _ing in _db.recipe_get_ingredients(conn, rid):
            if _ing["fdc_id"] and not _ing["ref_recipe_id"]:
                _try_resolve_unknown_weight(conn, _ing)

    # Warn if stored weight differs from computed ingredient sum.
    with _db.get_db() as conn:
        _recipe_now = _db.recipe_get(conn, rid)
        _cw = _db.recipe_compute_weight(conn, rid)
    if _recipe_now and _recipe_now["total_weight"] and _cw is not None:
        _computed_g, _cw_complete = _cw
        _incomplete_note = "  [grey62](some weights unknown — lower bound)[/grey62]" if not _cw_complete else ""
        if abs(_computed_g - _recipe_now["total_weight"]) > 1.0:
            state.console.print(
                f"\n  [{state.T['warning']}]⚠  Weight mismatch:[/{state.T['warning']}]"
                f"  stored {_recipe_now['total_weight']:g} g"
                f"  vs  computed {_computed_g:.1f} g from ingredients.{_incomplete_note}"
                f"\n  [grey62](This is normal for cooked recipes where liquids are absorbed.)[/grey62]",
                highlight=False,
            )
            if _cw_complete:
                try:
                    _wt_choice = _prompt("Replace stored weight with computed sum?", choices=["y", "n"], default="n")
                except Cancelled:
                    _wt_choice = "n"
                if _wt_choice == "y":
                    with _db.get_db() as conn:
                        _db.recipe_update(
                            conn, rid,
                            _recipe_now["name"], _recipe_now["description"] or "",
                            _recipe_now["servings"], _recipe_now["instructions"] or "",
                            _recipe_now["total_volume"], _recipe_now["total_volume_unit"],
                            round(_computed_g, 1), "g",
                            _recipe_now["serving_size"], bool(_recipe_now["complete"]),
                        )
                    state.console.print(
                        f"  [{state.T['success']}]✓[/{state.T['success']}] Total weight updated to {_computed_g:.1f} g.",
                        highlight=False,
                    )

    # done=True means proceed to instructions; False means back/cancel
    ingredients_done = False
    ingredients_changed = False
    while True:
        with _db.get_db() as conn:
            ingredients = _db.recipe_get_ingredients(conn, rid)

        if ingredients:
            table_title(f"Recipe: {name}")
            if desc:
                state.console.print(f"  [grey62]({desc})[/grey62]")
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
                id_cell = _recipe_ing_id_cell(ing)
                amt = (_format_recipe_portion_label(ing["amount"], ing["ref_recipe_id"])
                       if ing["ref_recipe_id"] else _ing_amount_display(ing["unit"], ing["amount"]))
                row = [str(i), amt, id_cell, dot_cell(ing["food_name"], _RFOOD_W)]
                if has_notes:
                    row.append(ing["notes"] or "")
                tbl.add_row(*row)
            state.console.print(tbl)
            table_footer(f"  {ID_KEY}")
            _raw_prot, _dcp, _minor_skipped = _compute_recipe_protein_summary(rid)
            _dcp_str = f"{_dcp:.1f} g" if _dcp is not None else "[grey62]— (AA data missing)[/grey62]"
            _minor_note = "  [grey62](minor ingredients w/o AA data excluded)[/grey62]" if (_dcp is not None and _minor_skipped) else ""
            state.console.print(
                f"  [grey62]Protein:[/grey62]  raw {_raw_prot:.1f} g  "
                f"[grey62]·[/grey62]  complete (DCP) {_dcp_str}{_minor_note}"
            )
            help_footer("recipe-ingredients")
        else:
            state.console.print("[grey62]No ingredients yet.[/grey62]")

        _show_menu("Ingredients", [
            ("1", "Add ingredient"),
            ("2", "Edit ingredient  [grey62](name, amount, etc. — not ingredient ID)[/grey62]"),
            ("3", "Remove ingredient"),
            ("4", "Reorder ingredients"),
            ("a", "Analyze recipe"),
            ("x", "Export recipe  [grey62](ingredients + procedure, optional nutrition)[/grey62]"),
            ("d", "Done — proceed to Procedure"),
            ("b", "Back — skip Procedure"),
            ("m", "Return to main menu  [grey62](skips Procedure)[/grey62]"),
            ("q", "Quit  [grey62](skips Procedure)[/grey62]"),
        ])
        state.console.print(f"  [grey62]To change an ingredient ID, delete the old one and add the new one.[/grey62]\n")
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            break

        if choice == "d":
            ingredients_done = True
            break
        if choice == "b":
            break
        if choice == "m":
            raise ReturnToMain()
        if choice == "q":
            raise SystemExit(0)
        elif choice == "1":
            state.console.print()
            try:
                query = _prompt("Search food or recipe  [grey62](name · FDC ID · barcode · Enter/b=back)[/grey62]", free_text=True).strip()
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
                with _db.get_db() as conn:
                    _db.recipe_auto_weight(conn, sub_rid)
                try:
                    raw_srv = _prompt(
                        "Servings of this recipe  [grey62](e.g. 1, 0.5, 2 — b=back)[/grey62]",
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
                    notes = _prompt("Note  [grey62](optional, Enter to skip)[/grey62]", default="", free_text=True).strip() or None
                except Cancelled:
                    notes = None
                label = _format_recipe_portion_label(servings)
                with _db.get_db() as conn:
                    _db.recipe_add_ingredient(conn, rid, 0, sub_name, servings, "servings", notes, ref_recipe_id=sub_rid)
                    _db.recipe_auto_weight(conn, rid)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added recipe: {sub_name}  {label}")
                ingredients_changed = True
            else:
                result = _pick_portion(food)
                if result is None:
                    continue
                grams, label, _ = result
                try:
                    notes = _prompt("Note for this ingredient  [grey62](optional, Enter to skip)[/grey62]", default="", free_text=True).strip() or None
                except Cancelled:
                    notes = None
                with _db.get_db() as conn:
                    _db.recipe_add_ingredient(conn, rid, food["fdcId"], food["name"], grams, label, notes)
                    _db.recipe_auto_weight(conn, rid)
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
                        f"Servings  [grey62](current: {ing['amount']:g})[/grey62]",
                        default=str(ing["amount"]),
                    ).strip()
                except Cancelled:
                    continue
                servings = _parse_serving_amount(raw_srv)
                if servings is None or servings <= 0:
                    state.console.print(f"[{state.T['warning']}]Enter a positive number.[/{state.T['warning']}]")
                    continue
                try:
                    notes_new = _prompt("Note  [grey62](Enter to keep current)[/grey62]", default=ing["notes"] or "", free_text=True).strip() or None
                except Cancelled:
                    notes_new = ing["notes"]
                with _db.get_db() as conn:
                    _db.recipe_update_ingredient(conn, ing["id"], servings, "servings", ing["food_name"], notes_new)
                    _db.recipe_auto_weight(conn, rid)
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
                    "Food name (edit or press Enter to keep)",
                    default=ing["food_name"], prefill=True, free_text=True, two_line=True,
                ).strip()
            except Cancelled:
                continue
            if not food_name_new:
                food_name_new = ing["food_name"]
            elif food_name_new.lower() == "b":
                continue
            elif food_name_new.lower() == "m":
                raise ReturnToMain()
            elif food_name_new.lower() == "q":
                raise SystemExit(0)
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
                notes_new = _prompt("Note  [grey62](Enter to keep current, '-' to clear)[/grey62]",
                                    default=ing["notes"] or "", free_text=True).strip()
            except Cancelled:
                notes_new = ing["notes"] or ""
            if notes_new == "-":
                notes_new = ""
            with _db.get_db() as conn:
                _db.recipe_update_ingredient(conn, ing["id"], grams, label, food_name_new,
                                             notes_new or None)
                _db.recipe_auto_weight(conn, rid)
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
                    state.console.print("[grey62]No ingredients remaining.[/grey62]")
                    break
                _RFOOD_W2 = 36
                tbl2 = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
                tbl2.add_column("#", justify="right", min_width=3)
                tbl2.add_column("Amount", min_width=14)
                tbl2.add_column("Food", min_width=_RFOOD_W2, max_width=_RFOOD_W2, no_wrap=True)
                for i, ing in enumerate(ingredients, 1):
                    tbl2.add_row(str(i), _ing_amount_display(ing["unit"], ing["amount"]), ing["food_name"])
                state.console.print(tbl2)
                help_footer("recipe-ingredients")
                try:
                    raw_idx = _prompt("Ingredient # to remove  [grey62](d=done)[/grey62]", free_text=True).strip().lower()
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
                    _db.recipe_auto_weight(conn, rid)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Removed: {ing['food_name']}")
                ingredients_changed = True
        elif choice == "4":
            if len(ingredients) < 2:
                state.console.print(f"[{state.T['warning']}]Nothing to reorder.[/{state.T['warning']}]")
                continue
            state.console.print("[grey62]Enter ingredient numbers in the new order, space- or comma-separated "
                          f"(e.g. 3 1 2 4 for {len(ingredients)} ingredients):[/grey62]")
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
                _db.recipe_auto_weight(conn, rid)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Ingredients reordered.")
            ingredients_changed = True
        elif choice == "a":
            with _db.get_db() as conn:
                _recipe_for_view = _db.recipe_get(conn, rid)
            if _recipe_for_view:
                from .recipe_analysis import _do_recipe_view
                _safe_call(_do_recipe_view, _recipe_for_view)
        elif choice == "x":
            with _db.get_db() as conn:
                _rx = _db.recipe_get(conn, rid)
                _ings_x = _db.recipe_get_ingredients(conn, rid)
            if not _rx:
                continue
            # Build ingredient display items
            _export_items = []
            for _ing in _ings_x:
                _amt = (_format_recipe_portion_label(_ing["amount"], _ing["ref_recipe_id"])
                        if _ing["ref_recipe_id"] else _ing_amount_display(_ing["unit"], _ing["amount"]))
                _export_items.append({
                    "food_name": _ing["food_name"],
                    "amount_display": _amt,
                    "notes": _ing["notes"] or "",
                })
            # Ask whether to include nutrition summary
            try:
                _inc_nut = _prompt(
                    "Include per-serving nutrition summary?",
                    choices=["y", "n"], default="y",
                )
            except Cancelled:
                continue
            _nutrition_nutrients: dict | None = None
            _dcp_g: float | None = _rx["dcp_g"]
            if _inc_nut == "y":
                _srv_count = max(1, _rx["servings"] or 1)
                _combined: dict[str, float] = {}
                with _db.get_db() as conn:
                    for _ing in _ings_x:
                        if _ing["ref_recipe_id"] or not _ing["fdc_id"] or not _ing["amount"]:
                            continue
                        _cached = _db.get_cached_food(conn, _ing["fdc_id"])
                        if _cached and _cached["nutrients_json"]:
                            _nuts = json.loads(_cached["nutrients_json"])
                            _scaled = _usda.scale_nutrients(_nuts, _ing["amount"], base_size=100.0)
                            _combined = _usda.sum_nutrients(_combined, _scaled)
                if _combined:
                    _nutrition_nutrients = {k: v / _srv_count for k, v in _combined.items()}
            _servings_label = (
                f"per serving (of {_rx['servings']})" if (_rx["servings"] or 0) > 1
                else "whole recipe"
            )
            _export_sections: list[dict] = [
                {
                    "type": "recipe_card",
                    "title": _rx["name"],
                    "description": _rx["description"] or "",
                    "servings": _rx["servings"] or 0,
                    "serving_size": _rx["serving_size"] or "",
                    "items": _export_items,
                    "procedure": _rx["instructions"] or "",
                },
            ]
            if _nutrition_nutrients is not None:
                _export_sections.append({
                    "type": "recipe_nutrition_brief",
                    "nutrients": _nutrition_nutrients,
                    "dcp_g": _dcp_g,
                    "servings_label": _servings_label,
                })
            _offer_export(_rx["name"], _export_sections)
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
        "  [grey62]— an editor will open. Save and close it to continue.[/grey62]"
    )
    state.console.print("  [grey62]Press Enter to open the editor, or b to skip.[/grey62]")
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


