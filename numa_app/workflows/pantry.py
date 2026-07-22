"""
pantry.py — My Pantry menu: manage protein sources on hand (add, edit, remove); AA data status shown.
Docs: README-numa-documentation.md, Menu Structure: "Foods → 6. My pantry"
"""
import json

import db as _db
import usda as _usda
from rich.table import Table
from .. import state
from ..config import prefs as _prefs
from ..services.annotations import maybe_prompt_gi
from ..services.search import _search_and_pick_food, _suggest_foundation_search
from ..ui.prompts import Cancelled, ReturnToMain, _prompt, _ask_float
from ..ui.common import _safe_call, _prompt_with_options, _id_cell, ID_KEY, dot_cell, section_title, table_footer, help_footer, food_id_tag

def _load_pantry_candidates() -> list[dict]:
    """
    Load pantry foods from the DB and resolve their nutrient profiles.
    For USDA-linked entries, nutrients come from the food cache.
    For name-only entries, nutrients will be None (suggest_complements handles
    the fallback to the curated complement table by keyword).
    """
    with _db.get_db() as conn:
        rows = _db.pantry_list(conn)
    candidates = []
    for row in rows:
        nutrients = None
        if row["fdc_id"] is not None:
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, row["fdc_id"])
            if cached:
                nutrients = json.loads(cached["nutrients_json"])
        candidates.append({
            "name":      row["food_name"],
            "fdc_id":    row["fdc_id"],
            "nutrients": nutrients,
            "diaas":     _usda.get_diaas(row["food_name"]),
        })
    return candidates

def _do_pantry_menu() -> None:
    """My Pantry submenu — manage protein sources on hand."""
    while True:
        show_archived = state.get_list_filter("pantry")
        with _db.get_db() as conn:
            rows = _db.pantry_list(conn, include_archived=show_archived)
        section_title("My Pantry — protein sources on hand")
        if not rows:
            state.console.print("  [grey62](empty — no foods added yet)[/grey62]")
        else:
            _FOOD_W = 47
            tbl = Table(show_header=True, header_style=state.T["accent_plain"],
                        box=None, padding=(0, 1))
            tbl.add_column("#",    justify="right", min_width=3)
            tbl.add_column("ID",   justify="right", min_width=7)
            tbl.add_column("AA",   min_width=4)
            tbl.add_column("Food", min_width=_FOOD_W, max_width=_FOOD_W, no_wrap=True)
            tbl.add_column("Notes", min_width=20)
            if show_archived:
                tbl.add_column("ARCH", min_width=4, justify="center")
            for row in rows:
                fdc_id = row["fdc_id"]
                if fdc_id is None:
                    aa_cell = "[grey62]—[/grey62]"
                else:
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, fdc_id)
                    if cached is None:
                        aa_cell = "[grey62]?[/grey62]"
                    else:
                        nutrients = json.loads(cached["nutrients_json"])
                        if _usda.has_amino_acid_data(nutrients):
                            aa_cell = f"[{state.T['success']}]✓[/{state.T['success']}]"
                        else:
                            aa_cell = f"[{state.T['error']}]✗[/{state.T['error']}]"
                row_cells = [str(row["id"]), _id_cell(fdc_id),
                            aa_cell, dot_cell(row["food_name"], _FOOD_W), row["notes"] or ""]
                if show_archived:
                    row_cells.append("[grey62]●[/grey62]" if row["archived"] else "")
                tbl.add_row(*row_cells, style="dim" if row["archived"] else None)
            state.console.print(tbl)
            table_footer(
                f"  {ID_KEY}",
                f"  [grey62]AA: [{state.T['success']}]✓[/{state.T['success']}] amino acid data in cache  "
                f"[{state.T['error']}]✗[/{state.T['error']}] none — research needed  "
                f"[grey62]—[/grey62] name-only entry (add via USDA search)"
                f"{'  ·  ARCH = archived' if show_archived else ''}[/grey62]",
            )
            help_footer("pantry", "archive")
            state.console.rule(style="grey50")
        state.console.print()
        state.console.print(f"  [{state.T['accent']}]a.[/{state.T['accent']}] Add a food")
        state.console.print(f"  [{state.T['accent']}]r.[/{state.T['accent']}] Remove a food")
        state.console.print(f"  [{state.T['accent']}]x.[/{state.T['accent']}] Archive / restore a food  [grey62](hide from complement suggestions, reversible)[/grey62]")
        state.console.print(f"  [{state.T['accent']}]s.[/{state.T['accent']}] {'Hide' if show_archived else 'Show'} archived  [grey62](toggle archived pantry entries in this list)[/grey62]")
        state.console.print(f"  [{state.T['accent']}]c.[/{state.T['accent']}] Go to Food Cache  [grey62](edit nutrients there)[/grey62]")
        state.console.print(f"  [grey62]b.[/grey62] Back to Foods menu")
        state.console.print(f"  [grey62]m.[/grey62] Return to main menu")
        state.console.print()
        state.console.print(
            f"  [grey62]To edit or obtain nutrient data for any food, use the Food Cache (option c).\n"
            f"  All pantry foods may be managed there.[/grey62]"
        )
        state.console.print()
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return
        if choice == "a":
            _safe_call(_do_pantry_add)
        elif choice == "c":
            from ..workflows.foods import _do_list_cached_foods
            _do_list_cached_foods()
        elif choice == "r":
            if rows:
                _safe_call(_do_pantry_remove)
        elif choice == "x":
            _safe_call(_do_pantry_archive_toggle)
        elif choice == "s":
            _prefs.set_list_filter("pantry", not show_archived)
        elif choice == "b":
            return
        elif choice == "m":
            raise ReturnToMain()
        elif choice == "q":
            raise SystemExit(0)
        elif choice != "":
            state.console.print(f"[{state.T['warning']}]Please enter a valid option (a / r / x / s / c / b / m / q).[/{state.T['warning']}]")


def _offer_custom_portions(fdc_id: int, food_name: str, existing_portions: list[dict]) -> None:
    """Offer to add cup-weight and/or piece-weight portions to a food that has no USDA portion data."""
    state.console.print(
        f"\n  [grey62]{food_name} has no USDA portion data.[/grey62]"
        "  Add a custom portion to enable volume or count measures?"
    )
    try:
        choice = _prompt_with_options(
            "Add portion data",
            [
                ("1", "Cup weight — enables 'cup', 'tbsp', 'tsp' measures"),
                ("2", "Piece weight — enables '1 piece', '2 slices', etc."),
                ("3", "Both"),
                ("b", "Skip"),
            ],
            default="b",
        )
    except Cancelled:
        return
    if choice == "b":
        return

    new_portions = list(existing_portions)

    if choice in ("1", "3"):
        g = _ask_float(f"Grams per 1 cup of {food_name}")
        if g is not None and g > 0:
            new_portions.append({"description": "1 cup", "gram_weight": round(g, 1)})

    if choice in ("2", "3"):
        try:
            unit_name = _prompt(
                "Unit name (e.g. piece, slice, clove, tablet)",
                default="piece", free_text=True,
            ).strip() or "piece"
        except Cancelled:
            return
        g = _ask_float(f"Grams per 1 {unit_name} of {food_name}")
        if g is not None and g > 0:
            new_portions.append({"description": f"1 {unit_name}", "gram_weight": round(g, 1)})

    if len(new_portions) > len(existing_portions):
        with _db.get_db() as conn:
            _db.update_food_portions(conn, fdc_id, new_portions)
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Custom portion saved.")


def _do_pantry_add() -> None:
    """Add a food to the pantry, optionally via USDA search for full AA data."""
    state.console.print("\n  Add via USDA search for best results (gives full amino acid data),")
    state.console.print("  or add by name only for a quick entry.\n")
    try:
        method = _prompt_with_options(
            "Pantry entry method",
            [
                ("1", "Search USDA"),
                ("2", "Enter name only"),
            ],
            default="1",
        )
    except Cancelled:
        return

    if method == "1":
        foods = _search_and_pick_food(show_aa_status=True, multi_select=True)
        if not foods:
            return
        multi = len(foods) > 1
        for food in foods:
            if not _usda.has_amino_acid_data(food.get("nutrients") or {}):
                data_type = food.get("dataType", "")
                if data_type == "Branded":
                    state.console.print(
                        f"\n  [{state.T['warning']}]{food['name']}{food_id_tag(food['fdcId'])}: branded foods rarely include "
                        f"amino acid data. A Foundation or SR Legacy equivalent will have complete data.[/{state.T['warning']}]"
                    )
                else:
                    state.console.print(
                        f"\n  [{state.T['warning']}]{food['name']}{food_id_tag(food['fdcId'])}: no amino acid data.[/{state.T['warning']}]"
                    )
                if not multi:
                    alt = _suggest_foundation_search(food)
                    if alt is not None:
                        food = alt
            food_name = food["name"]
            fdc_id = food["fdcId"]
            notes = None
            if not multi:
                try:
                    notes = _prompt("Notes (optional)", default="").strip() or None
                except Cancelled:
                    return
            with _db.get_db() as conn:
                _db.pantry_add(conn, food_name, fdc_id=fdc_id, notes=notes)
            has_aa = _usda.has_amino_acid_data(food.get("nutrients") or {})
            aa_note = "" if has_aa else f"  [{state.T['warning']}](no AA data)[/{state.T['warning']}]"
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food_name}{food_id_tag(fdc_id)}{aa_note}")
            if not multi:
                try:
                    maybe_prompt_gi(fdc_id, food_name)
                except Cancelled:
                    pass
            if not multi and not food.get("portions"):
                _offer_custom_portions(fdc_id, food_name, [])
        if multi:
            state.console.print(f"  [grey62](Notes can be added per food via the Food Cache)[/grey62]")
    else:
        try:
            food_name = _prompt("Food name").strip()
        except Cancelled:
            return
        if not food_name:
            return
        try:
            notes = _prompt("Notes (optional)", default="").strip()
        except Cancelled:
            return
        with _db.get_db() as conn:
            _db.pantry_add(conn, food_name, notes=notes or None)
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food_name} "
                      f"[grey62](name only — no USDA amino acid data)[/grey62]")


def _do_pantry_remove() -> None:
    """Remove a food from the pantry by its list ID."""
    try:
        raw = _prompt("Pantry ID to remove").strip()
    except Cancelled:
        return
    pid = None
    try:
        pid = int(raw)
    except ValueError:
        pass
    if pid is None:
        state.console.print(f"[{state.T['warning']}]Invalid ID.[/{state.T['warning']}]")
        return
    with _db.get_db() as conn:
        row = _db.pantry_get(conn, pid)
        if row is None:
            state.console.print(f"[{state.T['warning']}]ID {pid} not found.[/{state.T['warning']}]")
            return
        _db.pantry_remove(conn, pid)
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Removed: {row['food_name']}{food_id_tag(row['fdc_id'])}")


def _do_pantry_archive_toggle() -> None:
    """Archive or restore a pantry entry by its list ID (one command, flips current state)."""
    try:
        raw = _prompt("Pantry ID to archive/restore").strip()
    except Cancelled:
        return
    try:
        pid = int(raw)
    except ValueError:
        state.console.print(f"[{state.T['warning']}]Invalid ID.[/{state.T['warning']}]")
        return
    with _db.get_db() as conn:
        row = _db.pantry_get(conn, pid)
        if row is None:
            state.console.print(f"[{state.T['warning']}]ID {pid} not found.[/{state.T['warning']}]")
            return
        newly_archived = not row["archived"]
        _db.set_pantry_archived(conn, pid, newly_archived)
    verb = "Archived" if newly_archived else "Restored"
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] {verb}: {row['food_name']}{food_id_tag(row['fdc_id'])}")



