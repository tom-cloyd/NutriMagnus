"""
drafted_foods.py — user-drafted food profile management for numa.

Handles editing any cached food's nutrients, and the full drafted-profile
workflow (create, edit, delete, bulk AA import).  Called from foods.py.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/drafted_foods.py — cache editing and drafted profiles"
"""
import json
import re

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..services.search import _search_and_pick_food
from ..ui.common import _id_cell, ID_KEY, _show_menu, dot_cell, table_title, table_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_nutrient_table

def _do_edit_cached_food(fdc_id: int, cached) -> None:
    """
    Edit any cached food's profile — name, serving metadata, nutrients, note.
    After saving, marks the entry user_drafted=True so automatic re-fetches
    will not overwrite the changes.
    """
    existing_nutrients: dict = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
    existing_portions: list = []
    pj = cached["portions_json"]
    if pj and pj != "null":
        existing_portions = json.loads(pj)

    state.console.print(
        f"\n  [{state.T['hi']}]Editing:[/{state.T['hi']}] [bold]{cached['name']}[/bold]\n"
        f"  [dim]Press Enter to keep the current value for each field.[/dim]"
    )
    if not cached["user_drafted"]:
        state.console.print(
            f"\n  [dim]This is a cached {cached['data_type'] or 'external'} food. "
            f"Saving will mark it as user-modified — automatic re-fetches "
            f"will not overwrite your changes.[/dim]"
        )
    state.console.print()

    # Name
    try:
        name = _prompt("Food name", default=cached["name"]).strip()
    except Cancelled:
        return
    if not name:
        name = cached["name"]

    # Serving size / unit
    try:
        srv_raw = _prompt(
            "Serving size  [dim](Enter to keep)[/dim]",
            default=f"{cached['serving_size']:.0f}" if cached["serving_size"] else ""
        ).strip()
    except Cancelled:
        srv_raw = ""
    serving_size: float | None = cached["serving_size"]
    if srv_raw:
        try:
            serving_size = float(srv_raw)
        except ValueError:
            pass

    try:
        serving_unit = _prompt(
            "Serving unit  [dim](Enter to keep)[/dim]",
            default=cached["serving_unit"] or ""
        ).strip() or cached["serving_unit"]
    except Cancelled:
        serving_unit = cached["serving_unit"]

    # Nutrients
    nutrients = _prompt_nutrients(existing_nutrients)

    # Note
    try:
        notes = _prompt(
            "Note  [dim](Enter to keep, '-' to clear)[/dim]",
            default=cached["notes"] or ""
        ).strip()
    except Cancelled:
        notes = cached["notes"] or ""
    if notes == "-":
        notes = ""

    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id, name, nutrients,
            data_type="User Drafted",
            serving_size=serving_size,
            serving_unit=serving_unit,
            portions=existing_portions,
            notes=notes or None,
            user_drafted=True,
        )

    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Profile updated: [bold]{name}[/bold]"
    )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label="per 100g")


# ---------------------------------------------------------------------------
# Drafted food profiles
# ---------------------------------------------------------------------------

# Ordered list of (nutrient_key, display_label, unit) for user prompting.
# Split into two groups: basic macros (always prompted) and optional extras.
_DRAFT_MACROS = [
    ("calories",         "Calories",           "kcal"),
    ("protein_g",        "Protein",            "g"),
    ("fat_g",            "Total fat",          "g"),
    ("carb_g",           "Carbohydrates",      "g"),
    ("fiber_g",          "Fiber",              "g"),
    ("sugar_g",          "Sugars",             "g"),
    ("saturated_fat_g",  "Saturated fat",      "g"),
    ("sodium_mg",        "Sodium",             "mg"),
    ("calcium_mg",       "Calcium",            "mg"),
    ("iron_mg",          "Iron",               "mg"),
]

_DRAFT_AMINO_ACIDS = [
    ("aa_tryptophan_g",   "Tryptophan",    "g"),
    ("aa_threonine_g",    "Threonine",     "g"),
    ("aa_isoleucine_g",   "Isoleucine",    "g"),
    ("aa_leucine_g",      "Leucine",       "g"),
    ("aa_lysine_g",       "Lysine",        "g"),
    ("aa_methionine_g",   "Methionine",    "g"),
    ("aa_cystine_g",      "Cystine",       "g"),
    ("aa_phenylalanine_g","Phenylalanine", "g"),
    ("aa_tyrosine_g",     "Tyrosine",      "g"),
    ("aa_valine_g",       "Valine",        "g"),
    ("aa_histidine_g",    "Histidine",     "g"),
]

# Maps every name/abbreviation a literature source might use to the program's
# internal nutrient key.  Keys are lowercase; matching is case-insensitive.
_AA_NAME_LOOKUP: dict[str, str] = {
    # Tryptophan
    "tryptophan": "aa_tryptophan_g",  "trp": "aa_tryptophan_g",  "w": "aa_tryptophan_g",
    # Threonine
    "threonine":  "aa_threonine_g",   "thr": "aa_threonine_g",   "t": "aa_threonine_g",
    # Isoleucine
    "isoleucine": "aa_isoleucine_g",  "ile": "aa_isoleucine_g",  "i": "aa_isoleucine_g",
    # Leucine
    "leucine":    "aa_leucine_g",     "leu": "aa_leucine_g",     "l": "aa_leucine_g",
    # Lysine
    "lysine":     "aa_lysine_g",      "lys": "aa_lysine_g",      "k": "aa_lysine_g",
    # Methionine
    "methionine": "aa_methionine_g",  "met": "aa_methionine_g",  "m": "aa_methionine_g",
    # Cystine — accept cysteine too (they differ by one hydrogen; literature uses both)
    "cystine":    "aa_cystine_g",     "cysteine": "aa_cystine_g",
    "cys":        "aa_cystine_g",     "c": "aa_cystine_g",
    # Phenylalanine
    "phenylalanine": "aa_phenylalanine_g", "phe": "aa_phenylalanine_g", "f": "aa_phenylalanine_g",
    # Tyrosine
    "tyrosine":   "aa_tyrosine_g",    "tyr": "aa_tyrosine_g",    "y": "aa_tyrosine_g",
    # Valine
    "valine":     "aa_valine_g",      "val": "aa_valine_g",      "v": "aa_valine_g",
    # Histidine
    "histidine":  "aa_histidine_g",   "his": "aa_histidine_g",   "h": "aa_histidine_g",
}

# Non-essential AAs we recognize by name but do not store.
_AA_NON_ESSENTIAL: set[str] = {
    "arginine", "arg", "r",
    "alanine", "ala", "a",
    "aspartate", "aspartic", "aspartic acid", "asparagine", "asp", "asn", "d", "n",
    "glutamate", "glutamic", "glutamic acid", "glutamine", "glu", "gln", "e", "q",
    "glycine", "gly", "g",
    "proline", "pro", "p",
    "serine", "ser", "s",
    "hydroxyproline", "hyp",
    "selenocysteine", "sec", "u",
}


def _bulk_import_aa(protein_g: float | None) -> dict:
    """
    Accept amino acid values entered as 'name: value' pairs, one per prompt.
    If protein_g is provided, treats input as g per 100g protein and converts
    to g per 100g food.  If protein_g is None or 0, treats input as g per 100g
    food directly.  Returns a dict of {aa_key: value_per_100g_food}.
    """
    from_protein = (protein_g is not None and protein_g > 0)

    state.console.print(
        f"\n  [{state.T['accent']}]— Bulk amino acid import —[/{state.T['accent']}]"
    )
    if from_protein:
        state.console.print(
            f"  [dim]Input unit: [bold]g per 100g protein[/bold]  "
            f"(protein content: {protein_g:.2g} g/100g food)\n"
            f"  Values will be converted automatically: "
            f"aa_food = aa_protein × {protein_g:.2g} / 100[/dim]\n"
            f"  [dim]Accepted names: full name, 3-letter code, or 1-letter code "
            f"(e.g. tryptophan, trp, W)[/dim]\n"
            f"  [dim]Enter one amino acid per line as   name: value   "
            f"— press Enter on a blank line when done.[/dim]"
        )
    else:
        state.console.print(
            f"  [dim]Input unit: [bold]g per 100g food[/bold]\n"
            f"  Accepted names: full name, 3-letter code, or 1-letter code "
            f"(e.g. tryptophan, trp, W)\n"
            f"  Enter one amino acid per line as   name: value   "
            f"— press Enter on a blank line when done.[/dim]"
        )

    raw_entries: list[tuple[str, float]] = []   # (raw_name, raw_value)

    while True:
        try:
            line = _prompt("  AA").strip()
        except Cancelled:
            break
        if not line or line.lower() == "b":
            break
        if line.lower() == "q":
            raise SystemExit(0)

        # Accept "name: value", "name = value", or "name value"
        import re as _re
        m = _re.match(r"^([a-zA-Z][\w\s-]*)[\s:=]+([0-9.]+)\s*$", line)
        if not m:
            state.console.print(
                f"    [{state.T['warning']}]Format not recognised — "
                f"enter as  name: value  (e.g. lysine: 4.8)[/{state.T['warning']}]"
            )
            continue
        name_raw = m.group(1).strip()
        try:
            value = float(m.group(2))
        except ValueError:
            state.console.print(f"    [{state.T['warning']}]Value must be a number.[/{state.T['warning']}]")
            continue
        raw_entries.append((name_raw, value))

    if not raw_entries:
        return {}

    # Classify each entry
    stored:       list[tuple[str, str, float, float]] = []  # (raw_name, key, raw_val, stored_val)
    non_essential: list[tuple[str, float]] = []             # (raw_name, raw_val)
    unrecognized:  list[tuple[str, float]] = []             # (raw_name, raw_val)

    for name_raw, value in raw_entries:
        key_lookup = name_raw.lower().strip()
        if key_lookup in _AA_NAME_LOOKUP:
            aa_key = _AA_NAME_LOOKUP[key_lookup]
            stored_val = value * protein_g / 100.0 if from_protein else value
            stored.append((name_raw, aa_key, value, stored_val))
        elif key_lookup in _AA_NON_ESSENTIAL:
            non_essential.append((name_raw, value))
        else:
            unrecognized.append((name_raw, value))

    # Summary display
    state.console.print()
    if stored:
        state.console.print(f"  [{state.T['success']}]Recognized and stored:[/{state.T['success']}]")
        label_map = {key: label for key, label, _ in _DRAFT_AMINO_ACIDS}
        for name_raw, aa_key, raw_val, stored_val in stored:
            label = label_map.get(aa_key, aa_key)
            if from_protein:
                state.console.print(
                    f"    [{state.T['hi']}]{label:<16}[/{state.T['hi']}]"
                    f"  {raw_val:.4g} g/100g protein  →  {stored_val:.5g} g/100g food  "
                    f"[{state.T['success']}]✓[/{state.T['success']}]"
                )
            else:
                state.console.print(
                    f"    [{state.T['hi']}]{label:<16}[/{state.T['hi']}]"
                    f"  {stored_val:.5g} g/100g food  [{state.T['success']}]✓[/{state.T['success']}]"
                )
    if non_essential:
        state.console.print(f"  [dim]Not stored (non-essential, not tracked by this program):[/dim]")
        for name_raw, val in non_essential:
            state.console.print(f"    [dim]{name_raw}: {val:.4g}[/dim]")
    if unrecognized:
        state.console.print(f"  [{state.T['warning']}]Unrecognized names — not stored:[/{state.T['warning']}]")
        for name_raw, val in unrecognized:
            state.console.print(
                f"    [{state.T['warning']}]{name_raw}: {val:.4g}[/{state.T['warning']}]  "
                f"[dim](check spelling; accepted: full name, 3-letter, or 1-letter code)[/dim]"
            )

    return {aa_key: stored_val for _, aa_key, _, stored_val in stored}


def _list_drafted_foods() -> list:
    """Print a table of all user-drafted foods and return the rows."""
    with _db.get_db() as conn:
        rows = _db.list_user_drafted_foods(conn)
    if not rows:
        state.console.print("[dim]No drafted food profiles yet.[/dim]")
        return []
    table_title("DRAFTED FOOD PROFILES")
    _NAME_W = 36
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID",   justify="right", min_width=7)
    tbl.add_column("Name", min_width=_NAME_W, max_width=_NAME_W, no_wrap=True)
    tbl.add_column("Note", min_width=24)
    for r in rows:
        tbl.add_row(_id_cell(r["fdc_id"]), dot_cell(r["name"], _NAME_W), r["notes"] or "")
    state.console.print(tbl)
    table_footer(f"  {ID_KEY}")
    return list(rows)


def _prompt_nutrients(existing: dict | None = None) -> dict:
    """
    Interactively prompt for nutrient values (per 100 g).
    existing: pre-fill from this dict if provided (e.g. loaded from USDA cache).
    Returns a nutrients dict (may be partial if user exits early via Ctrl+C or 'b').
    Raises ReturnToMain if user types 'm'. Raises SystemExit on 'q'.
    """
    state.console.print(
        f"\n  [dim]Enter nutrient values per [bold]100 g[/bold]. "
        f"Press Enter to keep the current value, or enter a number to override. "
        f"Ctrl+C or [bold]b[/bold] to stop and continue.[/dim]"
    )
    nutrients: dict = {}

    state.console.print(f"\n  [{state.T['accent']}]— Basic nutrients —[/{state.T['accent']}]")
    for key, label, unit in _DRAFT_MACROS:
        current = existing.get(key) if existing else None
        default_str = f"{current:.4g}" if current is not None else None
        while True:
            try:
                raw = _prompt(
                    f"  {label} ({unit}/100g)",
                    default=default_str if default_str else ""
                ).strip()
            except Cancelled:
                return nutrients
            lower = raw.lower()
            if lower == "q":
                raise SystemExit(0)
            if lower == "m":
                raise ReturnToMain()
            if lower == "b":
                return nutrients
            if not raw:
                if current is not None:
                    nutrients[key] = current
                break
            try:
                nutrients[key] = float(raw)
                break
            except ValueError:
                state.console.print(f"    [{state.T['warning']}]Enter a number (or press Enter to skip).[/{state.T['warning']}]")

    # Amino acids are optional — offer three choices
    state.console.print()
    state.console.print(
        f"  [{state.T['accent']}]Amino acid profile[/{state.T['accent']}]"
        f"  [dim](enables protein completeness analysis)[/dim]"
    )
    state.console.print("  [dim]1[/dim]  Enter values one-by-one (g per 100g food)")
    state.console.print("  [dim]2[/dim]  Bulk import from literature (g per 100g protein — auto-converted)")
    state.console.print("  [dim]n[/dim]  Skip")

    while True:
        try:
            aa_choice = _prompt("  Choice", choices=["1", "2", "n"], default="n").strip().lower()
        except Cancelled:
            aa_choice = "n"
        if aa_choice in ("1", "2", "n"):
            break

    if aa_choice == "1":
        state.console.print(f"\n  [{state.T['accent']}]— Amino acids (g per 100g food) —[/{state.T['accent']}]")
        state.console.print("  [dim]All are optional. Press Enter to skip, Ctrl+C or 'b' to stop.[/dim]")
        for key, label, unit in _DRAFT_AMINO_ACIDS:
            current = existing.get(key) if existing else None
            default_str = f"{current:.5g}" if current is not None else None
            while True:
                try:
                    raw = _prompt(
                        f"  {label}",
                        default=default_str if default_str else ""
                    ).strip()
                except Cancelled:
                    return nutrients
                lower = raw.lower()
                if lower == "q":
                    raise SystemExit(0)
                if lower == "m":
                    raise ReturnToMain()
                if lower == "b":
                    return nutrients
                if not raw:
                    if current is not None:
                        nutrients[key] = current
                    break
                try:
                    nutrients[key] = float(raw)
                    break
                except ValueError:
                    state.console.print(f"    [{state.T['warning']}]Enter a number (or press Enter to skip).[/{state.T['warning']}]")

    elif aa_choice == "2":
        protein_g = nutrients.get("protein_g")
        bulk_result = _bulk_import_aa(protein_g)
        nutrients.update(bulk_result)

    return nutrients


def _do_copy_cached_food() -> None:
    """Search the cache, pick any food, copy its data into a new user-drafted entry."""
    state.console.print(
        f"\n  [{state.T['hi']}]Copy a cached food as a draft[/{state.T['hi']}]\n"
        f"  [dim]Copies nutrient data from any cached food into a new editable draft.[/dim]"
    )
    try:
        query = _prompt("Search cached foods", free_text=True).strip()
    except Cancelled:
        return
    if not query or query.lower() in ("b", ""):
        return

    with _db.get_db() as conn:
        rows = _db.search_cached_foods(conn, query)
    if not rows:
        state.console.print(f"[{state.T['warning']}]No cached foods matching '{query}'.[/{state.T['warning']}]")
        return

    _CNAME_W = 36
    _CBRAND_W = 24

    with _db.get_db() as _ann_conn:
        _anns = _db.annotations_for_fdcids(
            _ann_conn, [r["fdc_id"] for r in rows if isinstance(r["fdc_id"], int)]
        )

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("#",             justify="right", min_width=3)
    tbl.add_column("Type",          min_width=12)
    tbl.add_column("ID",            justify="right", min_width=7)
    tbl.add_column("Food / Recipe", min_width=_CNAME_W, max_width=_CNAME_W, no_wrap=True)
    tbl.add_column("Brand",         min_width=_CBRAND_W, max_width=_CBRAND_W, no_wrap=True)
    tbl.add_column("Ann",           min_width=5)
    tbl.add_column("AA data",       min_width=8)

    for _ci, r in enumerate(rows, 1):
        ann = _anns.get(r["fdc_id"])
        has_gi    = ann is not None and ann["gi_estimate"]    is not None
        has_diaas = ann is not None and ann["diaas_estimate"] is not None
        s = state.T["success"]
        if has_gi and has_diaas:
            ann_cell = f"[{s}]GI DI[/{s}]"
        elif has_gi:
            ann_cell = f"[{s}]GI[/{s}][dim] ··[/dim]"
        elif has_diaas:
            ann_cell = f"[dim]·· [/dim][{s}]DI[/{s}]"
        else:
            ann_cell = "[dim]·····[/dim]"

        nutrients = json.loads(r["nutrients_json"]) if r["nutrients_json"] else {}
        if _usda.has_amino_acid_data(nutrients):
            aa_cell = f"[{s}]✓[/{s}]"
        else:
            aa_cell = f"[{state.T['error']}]✗[/{state.T['error']}]"

        brand = r["brand"] or ""
        type_str = f"[{s}]★[/{s}] {r['data_type'] or ''}"
        if not brand:
            brand_cell = f"[dim]{'·' * _CBRAND_W}[/dim]"
        else:
            _bt = brand[:_CBRAND_W - 1]
            _bp = _CBRAND_W - len(_bt) - 1
            brand_cell = f"{_bt} [dim]{'·' * _bp}[/dim]" if _bp > 0 else _bt

        tbl.add_row(
            str(_ci), type_str, _id_cell(r["fdc_id"]),
            dot_cell(r["name"], _CNAME_W), brand_cell,
            ann_cell, aa_cell,
        )

    state.console.print()
    table_title("Food cache")
    state.console.print(tbl)
    table_footer(f"  {ID_KEY}")

    pick = _ask_int("Pick #")
    if pick is None:
        return
    if pick < 1 or pick > len(rows):
        state.console.print(f"[{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
        return

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, rows[pick - 1]["fdc_id"])
    fdc_id = rows[pick - 1]["fdc_id"]
    if cached is None:
        state.console.print(f"[{state.T['warning']}]Food not found in cache.[/{state.T['warning']}]")
        return

    existing_nutrients: dict = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
    existing_portions: list = []
    pj = cached["portions_json"]
    if pj and pj != "null":
        existing_portions = json.loads(pj)

    state.console.print(
        f"\n  [dim]Copying: [bold]{cached['name']}[/bold] — press Enter to keep each value.[/dim]\n"
    )

    try:
        name = _prompt("Food name", default=f"Copy of {cached['name']}").strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return

    try:
        srv_raw = _prompt(
            "Serving size",
            default=f"{cached['serving_size']:.0f}" if cached["serving_size"] else ""
        ).strip()
    except Cancelled:
        srv_raw = ""
    serving_size: float | None = cached["serving_size"]
    if srv_raw:
        try:
            serving_size = float(srv_raw)
        except ValueError:
            pass

    try:
        serving_unit = _prompt(
            "Serving unit",
            default=cached["serving_unit"] or ""
        ).strip() or cached["serving_unit"]
    except Cancelled:
        serving_unit = cached["serving_unit"]

    nutrients = _prompt_nutrients(existing_nutrients)

    try:
        notes = _prompt(
            "Note  [dim](Enter to keep, '-' to clear)[/dim]",
            default=cached["notes"] or ""
        ).strip()
    except Cancelled:
        notes = cached["notes"] or ""
    if notes == "-":
        notes = ""

    with _db.get_db() as conn:
        new_fdc_id = _db.next_user_drafted_fdc_id(conn)
        _db.cache_food(
            conn, new_fdc_id, name, "User Drafted",
            brand=cached["brand"],
            serving_size=serving_size,
            serving_unit=serving_unit,
            nutrients=nutrients,
            portions=existing_portions,
            user_drafted=True,
            notes=notes or None,
        )

    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Draft saved: [bold]{name}[/bold]  (ID {new_fdc_id})"
    )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label="per 100g")


def _do_drafted_foods_menu() -> None:
    while True:
        _show_menu("Drafted Food Profiles", [
            ("1", "List drafted profiles"),
            ("2", "Create new drafted profile"),
            ("3", "Edit a drafted profile"),
            ("4", "Delete a drafted profile"),
            ("5", "Copy a cached food as draft"),
            ("b", "Back to Foods menu"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return

        if choice == "1":
            _list_drafted_foods()

        elif choice == "2":
            _do_create_drafted_food()

        elif choice == "3":
            rows = _list_drafted_foods()
            if not rows:
                continue
            fdc_id = _ask_int("Profile ID to edit")
            if fdc_id is None:
                continue
            row = next((r for r in rows if r["fdc_id"] == fdc_id), None)
            if row is None:
                state.console.print(f"[{state.T['warning']}]ID {fdc_id} not found.[/{state.T['warning']}]")
                continue
            _do_edit_drafted_food(fdc_id, row)

        elif choice == "4":
            rows = _list_drafted_foods()
            if not rows:
                continue
            fdc_id = _ask_int("Profile ID to delete")
            if fdc_id is None:
                continue
            row = next((r for r in rows if r["fdc_id"] == fdc_id), None)
            if row is None:
                state.console.print(f"[{state.T['warning']}]ID {fdc_id} not found.[/{state.T['warning']}]")
                continue
            try:
                confirm = _prompt(
                    f"Delete [{state.T['hi']}]{row['name']}[/{state.T['hi']}]?",
                    choices=["y", "n"], default="n"
                )
            except Cancelled:
                continue
            if confirm.lower() == "y":
                with _db.get_db() as conn:
                    conn.execute("DELETE FROM foods WHERE fdc_id = ? AND user_drafted = 1", (fdc_id,))
                state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Deleted.")

        elif choice == "5":
            _do_copy_cached_food()

        elif choice == "b":
            return
        elif choice == "m":
            raise ReturnToMain()
        elif choice == "q":
            raise SystemExit(0)
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_create_drafted_food() -> None:
    state.console.print(
        f"\n  [{state.T['hi']}]Create a drafted food profile[/{state.T['hi']}]\n"
        f"  [dim]Drafted profiles let you build a best-guess nutrient profile for foods\n"
        f"  lacking complete official data. All values are per 100 g.[/dim]\n"
    )
    try:
        start = _prompt(
            "Start from a USDA food (pre-fill values) or from scratch?",
            choices=["u", "s"], default="s"
        ).strip().lower()
    except Cancelled:
        return

    existing_nutrients: dict = {}
    default_name = ""
    default_serving_size: float | None = None
    default_serving_unit: str | None = None

    if start == "u":
        food = _search_and_pick_food()
        if food is None:
            return
        existing_nutrients = dict(food.get("nutrients") or {})
        default_name = food.get("name", "")
        default_serving_size = food.get("servingSize")
        default_serving_unit = food.get("servingUnit")
        state.console.print(
            f"\n  [dim]Loaded: [bold]{default_name}[/bold] — "
            f"you can override any value below.[/dim]"
        )

    # Name
    try:
        name = _prompt("Food name", default=default_name).strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return

    # Serving size (optional metadata — not used in nutrient calculations)
    try:
        _srv_unit_hint = f" ({default_serving_unit})" if (default_serving_size and default_serving_unit) else ""
        srv_raw = _prompt(
            f"Serving size{_srv_unit_hint}" if default_serving_size else "Serving size  [dim](e.g. 30, or Enter to skip)[/dim]",
            default=f"{default_serving_size:.0f}" if default_serving_size else ""
        ).strip()
    except Cancelled:
        srv_raw = ""
    serving_size: float | None = None
    if srv_raw:
        try:
            serving_size = float(srv_raw)
        except ValueError:
            pass

    try:
        serving_unit = _prompt(
            "Serving unit" if default_serving_unit else "Serving unit  [dim](e.g. g, oz, cup — or Enter to skip)[/dim]",
            default=default_serving_unit or ""
        ).strip() or None
    except Cancelled:
        serving_unit = None

    # Nutrients
    nutrients = _prompt_nutrients(existing_nutrients if existing_nutrients else None)

    # Note
    try:
        notes = _prompt(
            "Note  [dim](document your sources/assumptions — optional)[/dim]",
            default=""
        ).strip() or None
    except Cancelled:
        notes = None

    # Confirm before saving
    state.console.print(
        f"\n  [dim]s[/dim]  Save draft"
        f"\n  [dim]d[/dim]  Discard"
        f"\n  [dim]m[/dim]  Discard and return to main menu"
    )
    try:
        action = _prompt("Action", choices=["s", "d", "m"], default="s")
    except Cancelled:
        action = "d"
    if action == "d":
        state.console.print(f"\n  [dim]Draft discarded.[/dim]")
        return
    if action == "m":
        state.console.print(f"\n  [dim]Draft discarded.[/dim]")
        raise ReturnToMain()

    # Assign a negative fdc_id and save
    with _db.get_db() as conn:
        fdc_id = _db.next_user_drafted_fdc_id(conn)
        _db.cache_food(
            conn, fdc_id, name, "User Drafted",
            brand=None,
            serving_size=serving_size,
            serving_unit=serving_unit,
            nutrients=nutrients,
            portions=[],
            user_drafted=True,
            notes=notes,
        )

    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Drafted profile saved: "
        f"[bold]{name}[/bold]  (ID {fdc_id})"
    )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label="per 100g")


def _do_edit_drafted_food(fdc_id: int, row) -> None:
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if cached is None:
        state.console.print(f"[{state.T['warning']}]Food not found in cache.[/{state.T['warning']}]")
        return
    _do_edit_cached_food(fdc_id, cached)
