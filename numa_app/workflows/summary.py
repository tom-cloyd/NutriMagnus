"""
summary.py — Daily summary - DCP and goals: today's, by-date, and recent-days nutrient summaries with RDA comparison.
Docs: README-numa-documentation.md, Menu Structure: "4. Analysis"
"""
from datetime import date, timedelta

import db as _db
import profile as _profile
import usda as _usda
from rich.table import Table
from .. import state
from ..services.nutrient_trend import average_from_daily_totals
from ..services import day_profile as _day_profile
from ..services.meal_list_columns import (
    label_for as _ml_label_for, day_nutrient_values as _ml_day_nutrient_values,
    MANDATORY_DAY_COLUMNS, MANDATORY_DAY_KEYS,
)
from ..ui.common import _safe_call, _show_menu, _prompt_with_options, section_title, table_footer, help_footer
from ..ui.prompts import Cancelled, _ask_date, _prompt
from ..ui.render import _print_complement_suggestions, _print_meal_diaas, _print_nutrient_table, _print_protein_adequacy, _print_rda_comparison
from .meals import _compute_meal_ingredient_list, _compute_meal_nutrients, _refresh_day_pct_goal

def _menu_daily_summary() -> bool:
    """Daily summary submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Daily Summary — DCP and Goals", [
            ("1", "Today's summary"),
            ("2", "Summary for a specific date"),
            ("3", "Recent days  (list dates with meals)"),
            ("4", "Multiday nutrient trend  (average vs. RDA — spot chronic shortfalls)"),
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
        elif choice == "4":
            _safe_call(_do_nutrient_trend)
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
    with _db.get_db() as conn:
        day_row = _db.day_profile_get(conn, meal_date)
        user_profile = _day_profile.get_profile_for_date(conn, meal_date)
    if day_row:
        override_tag = "  [grey62](manually set)[/grey62]" if day_row["overridden"] else ""
        state.console.print(f"  [grey62]Profile: {day_row['profile_name']}{override_tag}[/grey62]")
    rda = _profile.compute_rda(user_profile, diet_pref=state._diet_pref) if user_profile else None
    optimal = _profile.compute_optimal(user_profile) if user_profile else None
    max_limits = _profile.get_max_limits(user_profile) if user_profile else None
    _print_nutrient_table(combined, title=f"Daily Total — {meal_date}",
                          per_label=f"meals: {meal_names}",
                          daily_nutrients=combined, rda=rda,
                          optimal=optimal, max_limits=max_limits, show_meal_pct=False)
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

    _maybe_change_day_profile(meal_date)


def _maybe_change_day_profile(meal_date: str) -> None:
    """Offer to reassign which profile this day's comparisons use."""
    names = _profile.list_profiles()
    if len(names) < 2:
        return
    try:
        ans = _prompt(
            f"\nChange the profile used for {meal_date}?  [{state.T['accent']}]y[/{state.T['accent']}]/[grey62]N[/grey62]",
            choices=["y", "n"], default="n",
        )
    except Cancelled:
        return
    if ans != "y":
        return
    try:
        choice = _prompt_with_options(
            "Profile for this day",
            [(str(i), nm) for i, nm in enumerate(names, start=1)],
        )
    except Cancelled:
        return
    chosen = next((nm for i, nm in enumerate(names, start=1) if str(i) == choice), None)
    if not chosen:
        return
    with _db.get_db() as conn:
        ok = _day_profile.set_day_profile_override(conn, meal_date, chosen)
    if ok:
        _refresh_day_pct_goal(meal_date)
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] {meal_date} now uses profile '{chosen}'.")


def _do_list_recent_days() -> None:
    with _db.get_db() as conn:
        rows = _db.meal_dates_with_bcp(conn, limit=30)
    if not rows:
        state.console.print("[grey62]No meals logged yet.[/grey62]")
        return

    # % goal is read per-date from the stored day_pct_goal (already scored
    # against whichever profile was pinned to that date), not recomputed
    # here against a single current profile — a day logged under a past
    # profile must keep its own target, not today's. The goal itself (grams)
    # is stated explicitly per day since different days can be pinned to
    # different profiles with different targets.
    show_pct = any(row["day_pct_goal"] is not None for row in rows)
    show_profile = len(_profile.list_profiles()) > 1
    profile_names: dict[str, str | None] = {}
    goal_grams: dict[str, float | None] = {}
    # Drop any mandatory key also picked as a Meals & Log column — Recent
    # Days already shows it via its own fixed column below.
    extra_keys = [k for k in state.app_ctx.meal_list_nutrients if k not in MANDATORY_DAY_KEYS]
    nutrient_values: dict[str, dict[str, str | None]] = {}
    mandatory_values: dict[str, dict[str, str | None]] = {}
    with _db.get_db() as conn:
        for row in rows:
            d = row["meal_date"]
            if show_profile:
                dp = _db.day_profile_get(conn, d)
                profile_names[d] = dp["profile_name"] if dp else None
            goal_grams[d] = _day_profile.protein_target_for_date(conn, d, diet_pref=state._diet_pref)
            mandatory_values[d] = _ml_day_nutrient_values(conn, d, MANDATORY_DAY_KEYS)
            if extra_keys:
                nutrient_values[d] = _ml_day_nutrient_values(conn, d, extra_keys)

    section_title("Recent days with meals")
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Date",    min_width=12)
    tbl.add_column("Day DCP", justify="right", min_width=11)
    for key, label, _tip in MANDATORY_DAY_COLUMNS:
        tbl.add_column(label, justify="right", min_width=8)
    if show_pct:
        tbl.add_column("Goal",   justify="right", min_width=7)
        tbl.add_column("% goal", justify="right", min_width=7)
    if show_profile:
        tbl.add_column("Profile", min_width=10)
    for key in extra_keys:
        tbl.add_column(_ml_label_for(key), justify="right", min_width=8)

    s = state.T["success"]
    for row in rows:
        d = row["meal_date"]
        day_bcp = row["day_bcp"]
        pct = row["day_pct_goal"]
        goal = goal_grams.get(d)
        if day_bcp is not None:
            bcp_cell = f"[{s}]{day_bcp:.1f} g[/{s}]"
            pct_cell = f"[{s}]{pct:.0f}%[/{s}]" if pct is not None else "[grey62]--[/grey62]"
        else:
            bcp_cell = "[grey62]--[/grey62]"
            pct_cell = "[grey62]--[/grey62]"
        goal_cell = f"{goal:.0f} g" if goal else "[grey62]--[/grey62]"

        cells = [d, bcp_cell]
        for key in MANDATORY_DAY_KEYS:
            val = mandatory_values.get(d, {}).get(key)
            cells.append(val if val is not None else "[grey62]--[/grey62]")
        if show_pct:
            cells.append(goal_cell)
            cells.append(pct_cell)
        if show_profile:
            cells.append(profile_names.get(d) or "[grey62]--[/grey62]")
        for key in extra_keys:
            val = nutrient_values.get(d, {}).get(key)
            cells.append(val if val is not None else "[grey62]--[/grey62]")
        tbl.add_row(*cells)

    state.console.print(tbl)
    footer_lines = ["  [grey62]DCP = bioavailable complete protein  ·  Protein = raw, not digestibility-adjusted  ·  "
                    "Carbs = carbohydrates (sugars, starches)  ·  -- = not yet computed[/grey62]"]
    if show_pct:
        footer_lines.append("  [grey62]Goal = that day's own protein target  ·  % goal = Day DCP ÷ Goal (see ?day-profile)[/grey62]")
    else:
        footer_lines.append("  [grey62]Set a user profile (Settings) to see your daily protein goal[/grey62]")
    table_footer(*footer_lines)
    help_footer("dcp", "day-profile", "meal-columns")


def _do_nutrient_trend() -> None:
    """Multiday average nutrient intake vs. RDA — surfaces chronic shortfalls
    (B12, iron, iodine, vitamin D, ...) that a single day's snapshot can't."""
    if not _profile.load_profile():
        state.console.print(
            "\n  [grey62]No profile set. Go to Settings → User profile to compare against RDA targets.[/grey62]"
        )
        return

    try:
        window = _prompt_with_options(
            "Average over how many days?",
            [("1", "Last 7 days"), ("2", "Last 14 days"), ("3", "Last 30 days")],
            default="1",
        )
    except Cancelled:
        return
    days = {"1": 7, "2": 14, "3": 30}.get(window)
    if days is None:
        return

    end = date.today()
    start = end - timedelta(days=days - 1)

    with _db.get_db() as conn:
        meals = _db.meal_list_by_date_range(conn, start.isoformat(), end.isoformat())
        # RDA targets reflect the profile pinned to the *end* of the window
        # (today, for the common case). If any logged day in the window was
        # pinned to a different profile, that's disclosed below rather than
        # silently blended into one average.
        user_profile = _day_profile.get_profile_for_date(conn, end.isoformat())
        window_dates = {m["meal_date"] for m in meals}
        end_profile_name = (_db.day_profile_get(conn, end.isoformat()) or {"profile_name": None})["profile_name"]
        differing_dates = sorted(
            d for d in window_dates
            if (_db.day_profile_get(conn, d) or {"profile_name": None})["profile_name"] != end_profile_name
        )
    if not user_profile:
        state.console.print(
            "\n  [grey62]No profile set. Go to Settings → User profile to compare against RDA targets.[/grey62]"
        )
        return

    daily_totals: dict[str, dict[str, float]] = {}
    all_ings: list[dict] = []
    day_dcp: dict[str, float] = {}
    for meal in meals:
        nutrients = _compute_meal_nutrients(meal["id"])
        if nutrients:
            day = daily_totals.setdefault(meal["meal_date"], {})
            for key, val in nutrients.items():
                day[key] = day.get(key, 0.0) + val
        all_ings.extend(_compute_meal_ingredient_list(meal["id"]))
        if meal["bcp_g"] is not None:
            day_dcp[meal["meal_date"]] = day_dcp.get(meal["meal_date"], 0.0) + meal["bcp_g"]

    avg_nutrients, num_days = average_from_daily_totals(daily_totals)
    if num_days == 0:
        state.console.print(
            f"\n  [grey62]No meals logged between {start.isoformat()} and {end.isoformat()}.[/grey62]"
        )
        return

    state.console.print(
        f"\n  [grey62]Averaging over {num_days} logged day(s) out of the last {days} "
        f"calendar day(s) ({start.isoformat()} to {end.isoformat()}).[/grey62]"
    )
    if differing_dates:
        state.console.print(
            f"  [{state.T['warning']}]Note:[/{state.T['warning']}] RDA targets below reflect your "
            f"'{end_profile_name}' profile (as of {end.isoformat()}); "
            f"{len(differing_dates)} day(s) in this window used a different profile at the time: "
            + ", ".join(differing_dates)
        )

    # Lead with DCP, not raw protein — raw protein overstates what the body
    # can actually use, and that gap is exactly what this view exists to
    # catch over a chronic window, not just a single day.
    protein_target = _profile.compute_rda(user_profile, diet_pref=state._diet_pref).get("protein_g", (0.0,))[0]
    if day_dcp:
        avg_dcp = sum(day_dcp.values()) / len(day_dcp)
        pct = (avg_dcp / protein_target * 100.0) if protein_target > 0 else 0.0
        color = state.T["success"] if pct >= 100 else (state.T["warning"] if pct >= 50 else state.T["error"])
        section_title(f"Average Day DCP — over {len(day_dcp)} day(s) with computed DCP")
        state.console.print(
            f"  [grey62]Profile-adjusted protein target: {protein_target:.1f} g/day[/grey62]",
            highlight=False,
        )
        state.console.print(
            f"  Digestible complete protein: [{color}]{avg_dcp:.1f} g[/{color}]  "
            f"[grey62]({pct:.0f}% of daily target)[/grey62]",
            highlight=False,
        )
    else:
        state.console.print(
            "\n  [grey62]DCP not yet computed for any day in this window — "
            "raw protein below is not a substitute; run 'c' on Meals & Log to compute it.[/grey62]"
        )

    _print_rda_comparison(
        avg_nutrients, user_profile,
        title=f"{num_days}-Day Average vs. Recommended Values",
        intake_label=f"{num_days}-Day Avg",
    )
    help_footer("trend", "dcp")

    # Pool amino acids across the whole window (not averaged — gap scoring is
    # a ratio to total protein, so the pooled total and a per-day average
    # produce identical gaps; the pooled total also reflects what's actually
    # available to complement across the real foods logged in the window).
    aa_nutrients = _usda.sum_nutrients(*[
        _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
        for ing in all_ings
        if _usda.has_amino_acid_data(ing["nutrients_100g"])
    ]) if all_ings else {}
    if aa_nutrients:
        _print_complement_suggestions(
            aa_nutrients, context="trend",
            basis_label=f"pooled across {num_days} logged day(s)",
            silent_if_complete=True,
        )
