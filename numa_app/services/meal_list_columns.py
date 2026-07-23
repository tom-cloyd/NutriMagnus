"""
meal_list_columns.py — shared nutrient-column picker logic for the Meals & Log
list (CLI + web): which nutrients can be tracked, short labels, and the cap.
Docs: README-numa-documentation.md
"""
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
