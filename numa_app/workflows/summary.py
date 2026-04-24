"""
summary.py — Daily Summary menu: today's, by-date, and recent-days nutrient summaries with RDA comparison.
Docs: README-numa-documentation.md, Menu Structure: "4. Daily Summary"
"""
from datetime import date

import db as _db
import profile as _profile
import usda as _usda
from .. import state
from ..ui.common import _safe_call, _show_menu
from ..ui.prompts import Cancelled, _ask_date, _prompt
from ..ui.render import _print_complement_suggestions, _print_meal_diaas, _print_nutrient_table, _print_protein_adequacy, _print_rda_comparison
from .meals import _compute_meal_ingredient_list, _compute_meal_nutrients

def _menu_summary() -> bool:
    """Daily summary submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Daily Nutrition Summary", [
            ("1", "Today's summary"),
            ("2", "Summary for a specific date"),
            ("3", "Recent days  (list dates with meals)"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[dim]Cancelled.[/dim]")
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
        state.console.print(f"[dim]No meals logged for {meal_date}.[/dim]")
        return
    combined: dict[str, float] = {}
    all_ings: list[dict] = []
    with state.console.status("[dim]Fetching amino acid data…[/dim]", spinner="dots"):
        for meal in meals:
            n = _compute_meal_nutrients(meal["id"])
            if n:
                combined = _usda.sum_nutrients(combined, n)
            all_ings.extend(_compute_meal_ingredient_list(meal["id"]))
    if not combined:
        state.console.print("[dim]No nutrient data found for this day.[/dim]")
        return
    meal_names = ", ".join(m["name"] for m in meals)
    _print_nutrient_table(combined, title=f"Daily Total — {meal_date}",
                          per_label=f"meals: {meal_names}")
    missing_aa, _dcp_g = _print_meal_diaas(all_ings)
    aa_nutrients = _usda.sum_nutrients(*[
        _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
        for ing in all_ings
        if _usda.has_amino_acid_data(ing["nutrients_100g"])
    ]) if all_ings else {}
    user_profile = _profile.load_profile()
    if user_profile:
        _print_protein_adequacy(combined, user_profile, context_label=f"Daily total ({meal_date})", dcp_g=_dcp_g)
    if aa_nutrients:
        _print_complement_suggestions(aa_nutrients, context="daily", offer_if_covered=True)

    # Offer RDA comparison if a profile is set
    user_profile = _profile.load_profile()
    if user_profile:
        try:
            ans = _prompt(
                f"\nCompare to your personalized RDA targets?  [{state.T['accent']}]y[/{state.T['accent']}]/[dim]N[/dim]",
                choices=["y", "n"], default="n",
            )
        except Cancelled:
            ans = "n"
        if ans == "y":
            _print_rda_comparison(combined, user_profile)
    else:
        state.console.print(
            f"\n  [dim]Tip: set a user profile under Settings → User profile"
            f" to compare your intake against personalized RDA targets.[/dim]"
        )


def _do_list_recent_days() -> None:
    with _db.get_db() as conn:
        rows = _db.meal_list_dates(conn, limit=30)
    if not rows:
        state.console.print("[dim]No meals logged yet.[/dim]")
        return
    state.console.print(f"\n[{state.T['accent']}]Recent days with meals[/{state.T['accent']}]")
    state.console.rule()
    for row in rows:
        state.console.print(f"  {row['meal_date']}")
