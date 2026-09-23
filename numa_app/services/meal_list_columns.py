"""
meal_list_columns.py — nutrient-column picker logic for the Meals & Log
list: which nutrients can be tracked, short labels, and the cap.
Also used by the Recent Days / Daily Summary list, which aggregates the same
user-chosen columns per date instead of per meal, and by the web Nutrient
Plot picker.
Docs: README-numa-documentation.md
"""
import json

import db as _db
import usda as _usda

MAX_MEAL_LIST_NUTRIENTS = 6

# Ordered choices for the picker — every NUTRIENT_MAP key. Each consuming
# list (Meals & Log, Recent Days) drops whichever keys it already shows via
# its own fixed column, so the same picker/positions can be shared between
# them without ever duplicating a column — see MEALS_LIST_FIXED_KEYS and
# MANDATORY_DAY_KEYS below.
AVAILABLE_NUTRIENTS: list[tuple[str, str, str]] = list(_usda.NUTRIENT_MAP.values())

_BY_KEY = {key: (label, unit) for key, label, unit in _usda.NUTRIENT_MAP.values()}
_AVAILABLE_KEYS = {key for key, _label, _unit in AVAILABLE_NUTRIENTS}

# Meals & Log always shows Calories as its own fixed column (meals.html) —
# picking it here would just duplicate it, so _meals_list_ctx() (backend.py)
# drops it from that list's own picker-driven columns.
MEALS_LIST_FIXED_KEYS = {"calories"}

# Recent Days (Daily Summary) always shows Protein first, ahead of even Day
# DCP — unlike AVAILABLE_NUTRIENTS above, it isn't a user choice. Day DCP is
# digestibility-adjusted; Protein here is the raw (unadjusted) total, which
# is why it needs its own column instead of just reusing Day DCP. Calories/
# Carbs/Fiber used to be mandatory here too; they're now ordinary picker
# choices like any other nutrient, dropped from Meals & Log only if that
# list's own MEALS_LIST_FIXED_KEYS applies to them (it doesn't).
MANDATORY_DAY_COLUMNS: list[tuple[str, str, str | None]] = [
    ("protein_g", "Protein (g)",  "Raw protein — not digestibility-adjusted. See Day DCP for the digestible complete protein figure."),
]
MANDATORY_DAY_KEYS: list[str] = [key for key, _label, _tip in MANDATORY_DAY_COLUMNS]

# Display order for the web Nutrient Plot picker: Protein/Calories/Carbs/
# Fiber first, then everything else — independent of MANDATORY_DAY_KEYS
# above (that's about which Recent Days columns are fixed, not display
# order), so shrinking the mandatory set doesn't reshuffle this picker.
_PLOT_HEAD_KEYS = ["protein_g", "calories", "carbs_g", "fiber_g"]
_PLOT_LABEL_OVERRIDES = {"carbs_g": "Carbohydrates (Sugars, starches)"}


def label_for(key: str) -> str:
    """Short column label for a nutrient key, e.g. 'Protein (g)'."""
    label, unit = _BY_KEY.get(key, (key, ""))
    return f"{label} ({unit})" if unit else label


def sanitize(keys: list[str]) -> list[str]:
    """Drop unknown keys and enforce the display cap, preserving order.
    This picker/its positions are shared by Meals & Log and Recent Days;
    each of those drops whatever it already shows via its own fixed
    column(s) — MEALS_LIST_FIXED_KEYS and MANDATORY_DAY_KEYS respectively —
    from what sanitize() returns here, rather than losing it from the
    shared picker entirely (the other list may still want to show it)."""
    return [k for k in keys if k in _AVAILABLE_KEYS][:MAX_MEAL_LIST_NUTRIENTS]


def format_value(key: str, value: float) -> str:
    """Render a nutrient value at a precision appropriate to its unit."""
    _, unit = _BY_KEY.get(key, ("", "g"))
    return f"{value:.1f}" if unit == "g" else f"{value:.0f}"


def plot_nutrient_choices() -> list[tuple[str, str]]:
    """(key, display label) pairs for the web Nutrient Plot picker, in display
    order: Protein/Calories/Carbs/Fiber first (see _PLOT_HEAD_KEYS), then
    every other tracked nutrient in NUTRIENT_MAP's declared order."""
    ordered_keys = _PLOT_HEAD_KEYS + [k for k in _BY_KEY if k not in _PLOT_HEAD_KEYS]
    choices = []
    for key in ordered_keys:
        label, unit = _BY_KEY[key]
        label = _PLOT_LABEL_OVERRIDES.get(key, label)
        choices.append((key, f"{label} ({unit})" if unit else label))
    return choices


def day_nutrient_raw_totals(conn, meal_date: str, keys: list[str]) -> dict[str, float]:
    """Sum each meal's stored nutrient snapshot across meal_date, unformatted
    -- e.g. for computing a percent-of-RDA rather than displaying the total
    directly. See day_nutrient_values (built on this) for the formatted,
    display-ready version; a key absent here means no meal on meal_date had
    a snapshot with that key (matches the day-total convention used
    elsewhere: any meal with computed data counts, regardless of whether
    it's marked complete)."""
    totals: dict[str, float] = {}
    for m in _db.meal_list_by_date(conn, meal_date):
        if not m["nutrients_snapshot_json"]:
            continue
        snapshot = json.loads(m["nutrients_snapshot_json"])
        for key in keys:
            val = snapshot.get(key)
            if val is not None:
                totals[key] = totals.get(key, 0.0) + val
    return totals


def day_nutrient_values(conn, meal_date: str, keys: list[str]) -> dict[str, str | None]:
    """Sum each meal's stored nutrient snapshot across meal_date, formatted
    per key. A key is None for that date if no meal on it has a snapshot yet
    (matches the day-total convention used elsewhere: any meal with computed
    data counts, regardless of whether it's marked complete)."""
    totals = day_nutrient_raw_totals(conn, meal_date, keys)
    return {key: (format_value(key, totals[key]) if key in totals else None) for key in keys}
