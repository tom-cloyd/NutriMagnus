"""
water.py — water intake, split into water from drinks and water from food.

A food's own nutrient data carries one value, water_g (total moisture per
100 g — USDA nutrient 1051). Whether that water counts as "from drinks" is a
property of the food (foods.is_drink) or of a recipe (recipes.is_drink — then
ALL its water counts as drinks, even from ingredients that aren't drinks on
their own: a smoothie's banana). The split exists only once a meal, recipe or
day is totalled: tag() adds the two derived keys to one food's per-100 g
nutrients at that point, so every ordinary sum carries the split along with
everything else, into meal nutrient snapshots, day totals, columns and plots.
The two always add up to water_g. A food page shows water_g alone.

Docs: README-numa-documentation.md, Architecture: "numa_app/services/water.py — water from drinks vs food"
"""
from __future__ import annotations

import re

WATER_KEY = "water_g"
# The two derived keys; their labels are in usda.DERIVED_NUTRIENTS.
DRINKS_KEY = "water_drinks_g"
FOOD_KEY = "water_food_g"
ALL_KEYS = frozenset({WATER_KEY, DRINKS_KEY, FOOD_KEY})


def tag(nutrients: dict, is_drink: bool) -> dict:
    """`nutrients` plus the drinks/food split of its water_g, ready to be
    summed. No water_g (never measured) adds nothing, so a missing value
    stays "no data" rather than becoming 0 from drinks and 0 from food."""
    water = nutrients.get(WATER_KEY)
    if water is None:
        return nutrients
    water = float(water)
    return {**nutrients,
            DRINKS_KEY: water if is_drink else 0.0,
            FOOD_KEY:   0.0 if is_drink else water}


def as_drink(nutrients: dict) -> dict:
    """Re-tag an already-summed total so all of its water counts as drinks —
    for a recipe marked as a drink."""
    water = nutrients.get(WATER_KEY)
    if water is None:
        return nutrients
    return {**nutrients, DRINKS_KEY: float(water), FOOD_KEY: 0.0}


def is_drink(row) -> bool:
    """The is_drink flag of a foods or recipes row (False for no row, or a
    row selected without that column)."""
    try:
        return bool(row["is_drink"])
    except (IndexError, KeyError, TypeError):
        return False


def estimate_water(nutrients: dict) -> float | None:
    """Water per 100 g by difference — 100 minus protein, carbs and fat — for
    a drink whose data has no water value (branded labels never list it).
    Ignores ash and alcohol, so it runs a little high; close for juices,
    sodas and milks. None unless all three macros are present, or when they
    leave nothing over."""
    if any(nutrients.get(k) is None for k in ("protein_g", "carbs_g", "fat_g")):
        return None
    water = 100.0 - float(nutrients["protein_g"]) - float(nutrients["carbs_g"]) - float(nutrients["fat_g"])
    return round(water, 1) if water > 0 else None


def looks_like_drink(name: str | None, category: str | None) -> bool:
    """Best guess, for a newly cached food, at whether it is a drink: USDA
    files drinks under a "Beverages" category (Foundation / SR Legacy),
    "... beverages" (Survey), or names them "Beverages, ..." (SR Legacy).
    Milk, soups and smoothies aren't guessed — the user ticks those."""
    if category and "beverage" in category.lower():
        return True
    return bool(name) and name.strip().lower().startswith("beverages,")


# ---------------------------------------------------------------------------
# Wet food picked for a dry one
# ---------------------------------------------------------------------------
# A name that says the food is dry, on a food whose data says it is mostly
# water, is nearly always the wrong record: USDA's okara is the wet pulp
# (82% water) while okara flour is ~8%, and protein, calories and everything
# else differ about fivefold with it. Water shows it where the name can't.
#
# Only this direction is checked. The reverse ("cooked"/"raw" but little
# water) has too many real exceptions: raw nuts are ~4% water, cooked bacon
# ~12%. The threshold sits above the wettest genuinely dried foods (prunes,
# dried apricots and figs run ~30-35%).
WET_DRY_THRESHOLD_G = 40.0

_DRY_WORDS_RE = re.compile(r"\b(flour|powder|powdered|dried|dehydrated|freeze-dried|dry)\b", re.IGNORECASE)
# Words that make a dry-sounding name genuinely wet: a dry ingredient made up
# into something ("chocolate powder, prepared with milk"), packed in liquid
# ("tomatoes, sun-dried, packed in oil"), or a drink that is "dry" in taste.
_WET_CONTEXT_RE = re.compile(
    r"\b(prepared|reconstituted|rehydrated|made with|cooked|boiled|stewed|soaked|"
    r"packed in|in oil|in water|in syrup|in juice|wine|sherry|vermouth|cider|champagne|"
    r"martini|sake|beer|ale)\b", re.IGNORECASE)


def dry_word(name: str | None) -> str | None:
    """The word in `name` that says the food is dry ("flour", "dried", ...),
    or None — also None when the rest of the name says it's been made wet."""
    if not name or _WET_CONTEXT_RE.search(name):
        return None
    m = _DRY_WORDS_RE.search(name)
    return m.group(1).lower() if m else None


def wet_dry_conflict(names, nutrients: dict) -> dict | None:
    """{"name", "word", "water"} when one of `names` (the food's own name,
    and the name typed for it in a recipe or meal) says dry while the food's
    water is over WET_DRY_THRESHOLD_G per 100 g; else None. No water value,
    no verdict."""
    water = nutrients.get(WATER_KEY)
    if water is None or float(water) <= WET_DRY_THRESHOLD_G:
        return None
    for name in names:
        word = dry_word(name)
        if word:
            return {"name": name, "word": word, "water": float(water)}
    return None
