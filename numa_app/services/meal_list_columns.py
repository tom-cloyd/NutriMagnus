"""
meal_list_columns.py — shared nutrient-column picker logic for the Meals & Log
list (CLI + web): which nutrients can be tracked, short labels, and the cap.
Also used by the Recent Days / Daily Summary list, which aggregates the same
user-chosen columns per date instead of per meal.
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

_BY_KEY = {key: (label, unit) for key, label, unit in AVAILABLE_NUTRIENTS}


def label_for(key: str) -> str:
    """Short column label for a nutrient key, e.g. 'Protein (g)'."""
    label, unit = _BY_KEY.get(key, (key, ""))
    return f"{label} ({unit})" if unit else label


def sanitize(keys: list[str]) -> list[str]:
    """Drop unknown keys and enforce the display cap, preserving order."""
    return [k for k in keys if k in _BY_KEY][:MAX_MEAL_LIST_NUTRIENTS]


def format_value(key: str, value: float) -> str:
    """Render a nutrient value at a precision appropriate to its unit."""
    _, unit = _BY_KEY.get(key, ("", "g"))
    return f"{value:.1f}" if unit == "g" else f"{value:.0f}"


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
