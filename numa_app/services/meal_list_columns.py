"""
meal_list_columns.py — shared nutrient-column picker logic for the Meals & Log
list (CLI + web): which nutrients can be tracked, short labels, and the cap.
Also used by the Recent Days / Daily Summary list, which aggregates the same
user-chosen columns per date instead of per meal, and by the web Nutrient
Plot picker.
Docs: README-numa-documentation.md
"""
import json

import db as _db
import usda as _usda

MAX_MEAL_LIST_NUTRIENTS = 6

# Ordered choices for the picker — every NUTRIENT_MAP key except calories,
# which is always shown as its own fixed column.
AVAILABLE_NUTRIENTS: list[tuple[str, str, str]] = [
    (key, label, unit)
    for key, label, unit in _usda.NUTRIENT_MAP.values()
    if key != "calories"
]

# format_value/day_nutrient_values are general-purpose (any NUTRIENT_MAP key
# can be passed in, not just the picker-eligible AVAILABLE_NUTRIENTS ones —
# e.g. Recent Days' mandatory Calories column below), so this is built from
# the full map, not the calories-excluding AVAILABLE_NUTRIENTS.
_BY_KEY = {key: (label, unit) for key, label, unit in _usda.NUTRIENT_MAP.values()}
_AVAILABLE_KEYS = {key for key, _label, _unit in AVAILABLE_NUTRIENTS}

# Recent Days (Daily Summary) always shows these four, right after Day DCP —
# unlike AVAILABLE_NUTRIENTS above, they aren't a user choice. Day DCP is
# digestibility-adjusted; Protein here is the raw (unadjusted) total, which
# is why it needs its own column instead of just reusing Day DCP.
MANDATORY_DAY_COLUMNS: list[tuple[str, str, str | None]] = [
    ("protein_g", "Protein (g)",  "Raw protein — not digestibility-adjusted. See Day DCP for the digestible complete protein figure."),
    ("calories",  "Calories",     None),
    ("carbs_g",   "Carbs (g)",    "Carbohydrates (sugars, starches)"),
    ("fiber_g",   "Fiber (g)",    None),
]
MANDATORY_DAY_KEYS: list[str] = [key for key, _label, _tip in MANDATORY_DAY_COLUMNS]

# Same four, first, for the web Nutrient Plot picker — it has no separate
# fixed Calories column making it redundant there, so Calories is included
# (AVAILABLE_NUTRIENTS above deliberately excludes it).
_PLOT_HEAD_KEYS = MANDATORY_DAY_KEYS
_PLOT_LABEL_OVERRIDES = {"carbs_g": "Carbohydrates (Sugars, starches)"}


def label_for(key: str) -> str:
    """Short column label for a nutrient key, e.g. 'Protein (g)'."""
    label, unit = _BY_KEY.get(key, (key, ""))
    return f"{label} ({unit})" if unit else label


def sanitize(keys: list[str]) -> list[str]:
    """Drop unknown keys and enforce the display cap, preserving order.
    Checked against AVAILABLE_NUTRIENTS (not the broader _BY_KEY), so
    calories can't be picked here — it's always shown via its own fixed
    column on Meals & Log. This picker is shared with Recent Days, where
    Protein/Carbs/Fiber are also separately mandatory (see
    MANDATORY_DAY_KEYS) — callers building Recent Days' optional columns
    should drop those themselves rather than lose them here, since Meals &
    Log still offers them as a normal choice."""
    return [k for k in keys if k in _AVAILABLE_KEYS][:MAX_MEAL_LIST_NUTRIENTS]


def format_value(key: str, value: float) -> str:
    """Render a nutrient value at a precision appropriate to its unit."""
    _, unit = _BY_KEY.get(key, ("", "g"))
    return f"{value:.1f}" if unit == "g" else f"{value:.0f}"


def plot_nutrient_choices() -> list[tuple[str, str]]:
    """(key, display label) pairs for the web Nutrient Plot picker, in display
    order: Protein/Calories/Carbs/Fiber first (see MANDATORY_DAY_COLUMNS),
    then every other tracked nutrient in NUTRIENT_MAP's declared order."""
    ordered_keys = _PLOT_HEAD_KEYS + [k for k in _BY_KEY if k not in _PLOT_HEAD_KEYS]
    choices = []
    for key in ordered_keys:
        label, unit = _BY_KEY[key]
        label = _PLOT_LABEL_OVERRIDES.get(key, label)
        choices.append((key, f"{label} ({unit})" if unit else label))
    return choices


def day_nutrient_values(conn, meal_date: str, keys: list[str]) -> dict[str, str | None]:
    """Sum each meal's stored nutrient snapshot across meal_date, formatted
    per key. A key is None for that date if no meal on it has a snapshot yet
    (matches the day-total convention used elsewhere: any meal with computed
    data counts, regardless of whether it's marked complete)."""
    totals: dict[str, float] = {}
    for m in _db.meal_list_by_date(conn, meal_date):
        if not m["nutrients_snapshot_json"]:
            continue
        snapshot = json.loads(m["nutrients_snapshot_json"])
        for key in keys:
            val = snapshot.get(key)
            if val is not None:
                totals[key] = totals.get(key, 0.0) + val
    return {key: (format_value(key, totals[key]) if key in totals else None) for key in keys}
