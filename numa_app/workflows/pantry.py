import json

import db as _db
import usda as _usda
from rich.table import Table
from .. import state
from ..services.search import _search_and_pick_food
from ..services.portions import _normalize_unit_display, _pick_portion
from ..ui.prompts import Cancelled, _prompt

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
        with _db.get_db() as conn:
            rows = _db.pantry_list(conn)
        state.console.print(f"\n  [{state.T['hi']}]My Pantry — protein sources on hand[/{state.T['hi']}]")
        state.console.rule()
        if not rows:
            state.console.print("  [dim](empty — no foods added yet)[/dim]")
        else:
            tbl = Table(show_header=True, header_style=state.T["accent_plain"],
                        box=None, padding=(0, 1))
            tbl.add_column("#",    justify="right", min_width=3)
            tbl.add_column("Food", min_width=36)
            tbl.add_column("USDA linked", min_width=12)
            tbl.add_column("Notes", min_width=20)
            for row in rows:
                linked = f"fdc:{row['fdc_id']}" if row["fdc_id"] else "[dim]name only[/dim]"
                tbl.add_row(str(row["id"]), row["food_name"], linked, row["notes"] or "")
            state.console.print(tbl)
        state.console.print()
        state.console.print(f"  [{state.T['accent']}]a.[/{state.T['accent']}] Add a food")
        state.console.print(f"  [{state.T['accent']}]e.[/{state.T['accent']}] Edit an entry")
        state.console.print(f"  [{state.T['accent']}]r.[/{state.T['accent']}] Remove a food")
        state.console.print(f"  [dim]b.[/dim] Back")
        state.console.print()
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return
        if choice == "a":
            _safe_call(_do_pantry_add)
        elif choice == "e":
            if rows:
                _safe_call(_do_pantry_edit)
        elif choice == "r":
            if rows:
                _safe_call(_do_pantry_remove)
        elif choice == "b":
            return
        elif choice == "q":
            raise SystemExit(0)
        elif choice != "":
            state.console.print(f"[{state.T['warning']}]Please enter a valid option (a / e / r / b / q).[/{state.T['warning']}]")


def _do_pantry_add() -> None:
    """Add a food to the pantry, optionally via USDA search for full AA data."""
    state.console.print("\n  Add via USDA search for best results (gives full amino acid data),")
    state.console.print("  or add by name only for a quick entry.\n")
    try:
        method = _prompt("Search USDA or enter name?  [dim](u=USDA / n=name)[/dim]",
                         choices=["u", "n"], default="u").strip().lower()
    except Cancelled:
        return

    if method == "u":
        food = _search_and_pick_food()
        if food is None:
            return
        food_name = food["name"]
        fdc_id = food["fdcId"]
        try:
            notes = _prompt("Notes (optional)", default="").strip()
        except Cancelled:
            return
        with _db.get_db() as conn:
            _db.pantry_add(conn, food_name, fdc_id=fdc_id, notes=notes or None)
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food_name}")
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
                      f"[dim](name only — no USDA amino acid data)[/dim]")


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
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Removed: {row['food_name']}")


def _do_pantry_edit() -> None:
    """Edit an existing pantry entry — name, USDA link, or notes."""
    try:
        raw = _prompt("Pantry ID to edit").strip()
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

    food_name = row["food_name"]
    fdc_id = row["fdc_id"]
    notes = row["notes"] or ""

    state.console.print(f"\n  Editing: [bold]{food_name}[/bold]"
                  f"  [dim](Enter to keep current value)[/dim]")

    # Name
    try:
        new_name = _prompt("Food name", default=food_name, prefill=True).strip()
    except Cancelled:
        return
    if new_name:
        food_name = new_name

    # USDA link — offer to re-link or clear
    linked_str = f"fdc:{fdc_id}" if fdc_id else "none"
    state.console.print(f"  Current USDA link: [dim]{linked_str}[/dim]")
    state.console.print(f"  [{state.T['accent']}]u[/{state.T['accent']}] Re-link via USDA search  "
                  f"[dim]c[/dim] Clear link  "
                  f"[dim]Enter[/dim] Keep current")
    try:
        link_choice = _prompt("USDA link", default="").strip().lower()
    except Cancelled:
        return
    if link_choice == "u":
        food = _search_and_pick_food()
        if food is not None:
            food_name = food["name"]
            fdc_id = food["fdcId"]
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Linked to: {food_name}")
    elif link_choice == "c":
        fdc_id = None
        state.console.print("  [dim]USDA link cleared.[/dim]")

    # Notes
    try:
        new_notes = _prompt("Notes", default=notes, prefill=True).strip()
    except Cancelled:
        return
    notes = new_notes

    with _db.get_db() as conn:
        _db.pantry_update(conn, pid, food_name, fdc_id, notes or None)
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Updated: {food_name}")


def _do_list_cached_foods() -> None:
    with _db.get_db() as conn:
        foods = _db.list_cached_foods(conn)
    if not foods:
        state.console.print("[dim]No foods cached yet.[/dim]")
        return

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("#",      justify="right", min_width=3)
    tbl.add_column("Name",   min_width=40)
    tbl.add_column("Type",   min_width=12)
    tbl.add_column("Brand",  min_width=20)
    for i, f in enumerate(foods, 1):
        tbl.add_row(str(i), f["name"], f["data_type"] or "", f["brand"] or "")
    state.console.print(tbl)

    try:
        raw = _prompt("Pick number  (Enter/b=back, q=quit)").strip().lower()
    except Cancelled:
        return
    if not raw or raw == "b":
        return
    if raw == "q":
        raise SystemExit(0)
    try:
        idx = int(raw) - 1
        if idx < 0 or idx >= len(foods):
            raise ValueError
    except ValueError:
        state.console.print(f"[{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
        return

    row = foods[idx]
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, row["fdc_id"])
    if not cached:
        state.console.print(f"[{state.T['error']}]Food not found in cache.[/{state.T['error']}]")
        return

    food = {
        "fdcId":           cached["fdc_id"],
        "name":            cached["name"],
        "dataType":        cached["data_type"],
        "brand":           cached["brand"],
        "servingSize":     cached["serving_size"],
        "servingUnit":     cached["serving_unit"],
        "householdServing": None,
        "nutrients":       json.loads(cached["nutrients_json"]),
        "portions":        json.loads(cached["portions_json"]),
    }

    try:
        action = _prompt("View nutrients [dim](v)[/dim] or analyze portion [dim](a)[/dim]",
                         choices=["v", "a"], default="v").strip().lower()
    except Cancelled:
        return

    if action == "a":
        result = _pick_portion(food)
        if result is None:
            return
        grams, label, scaled = result
        _print_nutrient_table(scaled, title=food["name"], per_label=label)
        _print_protein_completeness(scaled)
    else:
        _print_nutrient_table(food["nutrients"], title=food["name"], per_label="per 100g")
        _print_protein_completeness(food["nutrients"])
