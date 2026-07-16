"""
food_use.py — Food Use in Meals analysis: tabulate which foods were used across a
user-selected set of meals (by date range OR by meal ID), ranked by frequency.
Docs: README-numa-documentation.md, Menu Structure: "4. Analysis"
"""
import re

import db as _db
from rich.table import Table
from .. import state
from ..ui.common import ID_KEY, _id_cell, _prompt_with_options, dot_cell, help_footer, section_title, table_footer
from ..ui.prompts import Cancelled, _ask_date, _prompt

_BAR_WIDTH = 24
_NAME_WIDTH = 30


def _choose_option(label: str, options: list[tuple[str, str]], default: str) -> str | None:
    """Loop _prompt_with_options until a valid key is chosen. Returns None on Cancelled."""
    valid = {key for key, _ in options}
    while True:
        try:
            choice = _prompt_with_options(label, options, default=default)
        except Cancelled:
            return None
        if choice in valid:
            return choice
        state.console.print(f"[{state.T['warning']}]Enter one of: {', '.join(sorted(valid))}[/{state.T['warning']}]")


def _do_food_use_analysis() -> None:
    mode = _choose_option(
        "Select meals by",
        [("1", "Date range(s)"), ("2", "Meal IDs")],
        default="1",
    )
    if mode is None:
        return

    meals_by_id: dict[int, dict] = {}

    if mode == "1":
        while True:
            try:
                start = None
                while start is None:
                    start = _ask_date("Start date")
                end = None
                while end is None:
                    end = _ask_date("End date")
            except Cancelled:
                break
            if start > end:
                start, end = end, start
            with _db.get_db() as conn:
                rows = _db.meal_list_by_date_range(conn, start, end)
            for row in rows:
                meals_by_id[row["id"]] = dict(row)
            state.console.print(f"  [grey62]{len(rows)} meal(s) found for {start} to {end}.[/grey62]")
            try:
                again = _prompt(
                    f"Add another date range?  [{state.T['accent']}]y[/{state.T['accent']}]/[grey62]N[/grey62]",
                    choices=["y", "n"], default="n",
                )
            except Cancelled:
                break
            if again != "y":
                break
    else:
        try:
            raw_ids = _prompt("Meal IDs (comma/space separated)", free_text=True).strip()
        except Cancelled:
            raw_ids = ""
        if raw_ids:
            requested_ids: list[int] = []
            for token in re.split(r"[\s,]+", raw_ids):
                if not token:
                    continue
                try:
                    requested_ids.append(int(token))
                except ValueError:
                    state.console.print(f"[{state.T['warning']}]Ignoring non-numeric meal ID: {token}[/{state.T['warning']}]")
            with _db.get_db() as conn:
                rows = _db.meal_list_by_ids(conn, requested_ids)
            found_ids = {row["id"] for row in rows}
            missing = [i for i in requested_ids if i not in found_ids]
            if missing:
                state.console.print(
                    f"[{state.T['warning']}]Meal ID(s) not found: {', '.join(str(m) for m in missing)}[/{state.T['warning']}]"
                )
            for row in rows:
                meals_by_id[row["id"]] = dict(row)

    if not meals_by_id:
        state.console.print("[grey62]No meals selected — nothing to analyze.[/grey62]")
        return

    protein_choice = _choose_option(
        "Include",
        [("1", "All foods"), ("2", "Only protein-containing foods")],
        default="1",
    )
    protein_only = protein_choice == "2"

    agg: dict[tuple, dict] = {}
    for meal_id, meal in meals_by_id.items():
        with _db.get_db() as conn:
            items = _db.meal_expand_food_items(conn, meal_id)
        seen_this_meal = set()
        for fdc_id, name, kind, has_protein, deleted, recipe_id in items:
            if fdc_id is not None:
                key = (fdc_id, kind)
            elif recipe_id is not None:
                key = (kind, recipe_id)
            else:
                key = (kind, name)
            if key in seen_this_meal:
                continue
            seen_this_meal.add(key)
            entry = agg.setdefault(key, {
                "name": name, "fdc_id": fdc_id, "kind": kind, "has_protein": has_protein,
                "deleted": deleted, "meal_ids": set(), "days": set(),
            })
            entry["meal_ids"].add(meal_id)
            entry["days"].add(meal["meal_date"])

    rows_all = list(agg.values())
    if protein_only:
        rows_all = [r for r in rows_all if r["has_protein"]]

    rows_out = sorted(
        rows_all,
        key=lambda e: (-len(e["days"]), -len(e["meal_ids"]), e["name"].lower()),
    )

    total_days = len({m["meal_date"] for m in meals_by_id.values()})
    total_meals = len(meals_by_id)

    subtitle = f"{total_meals} meal(s) across {total_days} distinct day(s)"
    if protein_only:
        subtitle += " · protein-containing foods only"
    section_title("Food Use in Meals", subtitle)

    if not rows_out:
        state.console.print("[grey62]No foods matched this filter.[/grey62]")
        return

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID", min_width=5)
    tbl.add_column("Food", min_width=_NAME_WIDTH)
    tbl.add_column("Kind", min_width=6)
    tbl.add_column("Days used", justify="right", min_width=9)
    tbl.add_column("Meals", justify="right", min_width=6)
    tbl.add_column("", min_width=_BAR_WIDTH)

    max_days = len(rows_out[0]["days"]) if rows_out else 0
    a = state.T["accent"]
    for row in rows_out:
        n_days = len(row["days"])
        n_meals = len(row["meal_ids"])
        filled = min(int(_BAR_WIDTH * n_days / max_days), _BAR_WIDTH) if max_days else 0
        bar = f"[{a}]{'█' * filled}[/{a}]{'░' * (_BAR_WIDTH - filled)}"
        if row["kind"] != "recipe":
            kind_label = ""
        elif row["deleted"]:
            kind_label = f"[{state.T['error']}]recipe (deleted)[/{state.T['error']}]"
        else:
            kind_label = "recipe"
        tbl.add_row(
            _id_cell(row["fdc_id"]),
            dot_cell(row["name"], _NAME_WIDTH, bold=(row["kind"] == "recipe")),
            kind_label,
            str(n_days),
            str(n_meals),
            bar,
        )
    state.console.print(tbl, highlight=False)
    table_footer(
        f"  {ID_KEY}",
        "  [grey62]Days used = distinct calendar days the food appeared in this analysis set.[/grey62]",
        "  [grey62]Recipe rows show the recipe itself; its ingredients are also listed individually.[/grey62]",
        "  [grey62]\"recipe (deleted)\" means the recipe was removed after being used in that meal; its own ingredient breakdown is no longer available.[/grey62]",
    )
    help_footer("fooduse")
