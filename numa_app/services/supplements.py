"""
supplements.py — dietary supplements (a B12 tablet, a vitamin D softgel):
items counted per unit, not foods with gaps.

A food marked as a supplement (foods.is_supplement — set automatically by
supplement mode, a serving of exactly 1 tablet / capsule / scoop ..., or by
the switch on the food's page) is stored the supplement-mode way: one unit
counts as 100 g internally, so its per-100 g figures are the label's
per-unit figures. Being a supplement then means:

1. No food checks: calories, amino acids, GI, DIAAS, portions, water, data
   problems and missing-data lists all skip it (is_supplement() at each).
2. Its nutrients still count everywhere, and toward upper limits.
3. It weighs nothing: 0 g in recipe weights and per-100 g figures, and it
   stays out of glycemic load.
4. Its page reads "per tablet" (unit_name()) and logging it defaults to
   one unit.

And the from-supplements split: tag() adds "<key>__supp" copies of a
supplement's nutrients at the point a meal, recipe or day is totalled (the
same place water.tag() adds the drinks/food split), so every sum carries how
much of each nutrient came from supplements; supp_amount() reads it back.

Docs: README-numa-documentation.md, Architecture: "numa_app/services/supplements.py — supplements and the from-supplements split"
"""
from __future__ import annotations

import usda as _usda
from numa_app.services.entry_parse import COUNT_UNITS

SUFFIX = "__supp"
# Every tracked nutrient key (usda.NUTRIENT_MAP is keyed by USDA nutrient id).
_TRACKED = frozenset(key for key, _label, _unit in _usda.NUTRIENT_MAP.values())


def is_supplement(row) -> bool:
    """The is_supplement flag of a foods row (False for no row, or a row
    selected without that column)."""
    try:
        return bool(row["is_supplement"])
    except (IndexError, KeyError, TypeError):
        return False


def looks_like_supplement(serving_size, serving_unit) -> bool:
    """Supplement mode: a serving of exactly 1 of a count unit (tablet,
    capsule, scoop ...) — see entry_parse.supplement_portion()."""
    return unit_name(serving_size, serving_unit) is not None


def unit_name(serving_size, serving_unit) -> str | None:
    """"tablet" for a 1-tablet serving (plural forms accepted), else None."""
    unit = (serving_unit or "").strip().lower()
    unit = unit[:-1] if unit.endswith("s") and unit[:-1] in COUNT_UNITS else unit
    try:
        one = serving_size is not None and float(serving_size) == 1.0
    except (TypeError, ValueError):
        one = False
    return unit if one and unit in COUNT_UNITS else None


def display_unit(row) -> str:
    """What one internal "100 g" of this supplement is: its own count unit,
    or "unit" when its serving says nothing usable."""
    try:
        return unit_name(row["serving_size"], row["serving_unit"]) or "unit"
    except (IndexError, KeyError, TypeError):
        return "unit"


def tag(nutrients: dict, is_supp: bool) -> dict:
    """`nutrients` plus a "<key>__supp" copy of every tracked nutrient when
    this is a supplement, ready to be summed; unchanged otherwise (no key
    means none from supplements)."""
    if not is_supp:
        return nutrients
    return {**nutrients, **{k + SUFFIX: float(v) for k, v in nutrients.items()
                            if k in _TRACKED and isinstance(v, (int, float))}}


def supp_amount(nutrients: dict, key: str) -> float:
    """How much of `key` in a summed total came from supplements."""
    return float(nutrients.get(key + SUFFIX) or 0.0)


def strip(nutrients: dict) -> dict:
    """`nutrients` without the split keys."""
    return {k: v for k, v in nutrients.items() if not k.endswith(SUFFIX)}
