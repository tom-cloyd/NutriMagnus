"""
nutrient_trend.py — shared multi-day nutrient averaging, used by CLI
(workflows/summary.py) and web (backend.py) for the N-day nutrient trend view.

Single-day summaries only ever show a snapshot; a nutrient that's chronically
low (B12, iron, iodine, vitamin D) over many days is invisible if you only
ever look at one day at a time. This averages per-nutrient totals across the
days that actually had a meal logged, so the RDA comparison rendering (see
render._print_rda_comparison) can show a pattern instead of a snapshot.

CLI and web each expand a meal's items into per-nutrient totals differently
(numa_app.workflows.meals._compute_meal_nutrients vs. web/backend.py's
_meal_expand_for_diaas) — this module only covers the shared averaging step,
not the per-meal expansion itself.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/nutrient_trend.py — multi-day nutrient averaging"
"""


def average_from_daily_totals(
    daily_totals: dict[str, dict[str, float]],
) -> tuple[dict[str, float], int]:
    """Given {meal_date: nutrients_dict} for days that had at least one meal
    logged, return (per-nutrient average across those days, day count).

    Averages only over days present in `daily_totals` — days with no meals
    logged are simply absent, not treated as a zero-intake day. Conflating
    "didn't log" with "ate nothing" would understate the average and could
    mask exactly the chronic shortfall this view exists to surface.
    """
    num_days = len(daily_totals)
    if num_days == 0:
        return {}, 0

    summed: dict[str, float] = {}
    for day_nutrients in daily_totals.values():
        for key, val in day_nutrients.items():
            summed[key] = summed.get(key, 0.0) + val

    return {key: val / num_days for key, val in summed.items()}, num_days
