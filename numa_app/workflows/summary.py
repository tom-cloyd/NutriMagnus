"""
summary.py — Daily summary - DCP and goals: today's, by-date, and recent-days nutrient summaries with RDA comparison.
Docs: README-numa-documentation.md, Menu Structure: "4. Analysis"
"""
from datetime import date

import db as _db
import profile as _profile
import usda as _usda
from rich.table import Table
from .. import state
from ..ui.common import _safe_call, _show_menu, section_title, table_footer, help_footer
from ..ui.prompts import Cancelled, _ask_date, _prompt
from ..ui.render import _print_complement_suggestions, _print_meal_diaas, _print_nutrient_table, _print_protein_adequacy, _print_rda_comparison
from .meals import _compute_meal_ingredient_list, _compute_meal_nutrients

def _menu_daily_summary() -> bool:
    """Daily summary submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Daily Summary — DCP and Goals", [
            ("1", "Today's summary"),
            ("2", "Summary for a specific date"),
            ("3", "Recent days  (list dates with meals)"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[grey62]Cancelled.[/grey62]")
            return True

        if choice == "1":
            _safe_call(_do_daily_summary, date.today().isoformat())
        elif choice == "2":
            try:
                d = _ask_date("Date")
            except Cancelled:
                continue
            if d:
                _safe_call(_do_daily_summary, d)
        elif choice == "3":
            _safe_call(_do_list_recent_days)
        elif choice == "m":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_daily_summary(meal_date: str) -> None:
    with _db.get_db() as conn:
        meals = _db.meal_list_by_date(conn, meal_date)
    if not meals:
        state.console.print(f"[grey62]No meals logged for {meal_date}.[/grey62]")
        return
    combined: dict[str, float] = {}
    all_ings: list[dict] = []
    state.console.print()
    with state.console.status("[bold]Fetching amino acid data…[/bold]", spinner="dots"):
        for meal in meals:
            n = _compute_meal_nutrients(meal["id"])
            if n:
                combined = _usda.sum_nutrients(combined, n)
            all_ings.extend(_compute_meal_ingredient_list(meal["id"]))
    if not combined:
        state.console.print("[grey62]No nutrient data found for this day.[/grey62]")
        return
    meal_names = ", ".join(m["name"] for m in meals)
    user_profile = _profile.load_profile()
    rda = _profile.compute_rda(user_profile) if user_profile else None
    _print_nutrient_table(combined, title=f"Daily Total — {meal_date}",
                          per_label=f"meals: {meal_names}",
                          daily_nutrients=combined, rda=rda, show_meal_pct=False)
    missing_aa, _dcp_g, day_diaas = _print_meal_diaas(all_ings)
    aa_nutrients = _usda.sum_nutrients(*[
        _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
        for ing in all_ings
        if _usda.has_amino_acid_data(ing["nutrients_100g"])
    ]) if all_ings else {}
    if user_profile:
        _print_protein_adequacy(combined, user_profile, context_label=f"Daily total ({meal_date})", dcp_g=_dcp_g)
    if aa_nutrients:
        _print_complement_suggestions(aa_nutrients, context="daily", offer_if_covered=True,
                                      base_diaas=day_diaas)

    # Offer RDA comparison if a profile is set
    user_profile = _profile.load_profile()
    if user_profile:
        try:
            ans = _prompt(
                f"\nCompare to your personalized RDA targets?  [{state.T['accent']}]y[/{state.T['accent']}]/[grey62]N[/grey62]",
                choices=["y", "n"], default="n",
            )
        except Cancelled:
            ans = "n"
        if ans == "y":
            _print_rda_comparison(combined, user_profile)
    else:
        state.console.print(
            f"\n  [grey62]Tip: set a user profile under Settings → User profile"
            f" to compare your intake against personalized RDA targets.[/grey62]"
        )


def _do_list_recent_days() -> None:
    with _db.get_db() as conn:
        rows = _db.meal_dates_with_bcp(conn, limit=30)
    if not rows:
        state.console.print("[grey62]No meals logged yet.[/grey62]")
        return

    user_profile = _profile.load_profile()
    protein_goal: float | None = None
    if user_profile:
        rda = _profile.compute_rda(user_profile)
        if "protein_g" in rda:
            protein_goal = rda["protein_g"][0]

    section_title("Recent days with meals")
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Date",    min_width=12)
    tbl.add_column("Day DCP", justify="right", min_width=9)
    if protein_goal:
        tbl.add_column("% goal", justify="right", min_width=7)

    s = state.T["success"]
    for row in rows:
        day_bcp = row["day_bcp"]
        if day_bcp is not None:
            bcp_cell = f"[{s}]{day_bcp:.1f} g[/{s}]"
            pct_cell = (f"[{s}]{day_bcp / protein_goal * 100:.0f}%[/{s}]"
                        if protein_goal else "")
        else:
            bcp_cell = "[grey62]--[/grey62]"
            pct_cell = "[grey62]--[/grey62]"

        cells = [row["meal_date"], bcp_cell]
        if protein_goal:
            cells.append(pct_cell)
        tbl.add_row(*cells)

    state.console.print(tbl)
    footer_lines = ["  [grey62]DCP = bioavailable complete protein  ·  -- = not yet computed[/grey62]"]
    if protein_goal:
        footer_lines.append(f"  [grey62]% goal = Day DCP ÷ {protein_goal:.0f} g daily protein target[/grey62]")
    else:
        footer_lines.append("  [grey62]Set a user profile (Settings) to see % of daily protein goal[/grey62]")
    table_footer(*footer_lines)
    help_footer("dcp")
