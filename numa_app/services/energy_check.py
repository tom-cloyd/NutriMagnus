"""
energy_check.py — calories that are missing, or that don't add up.

A food can arrive by any route (USDA, Open Food Facts, the other national
databases, CSV, Claude, a typed custom food) with protein, carbs and fat but
no calories — USDA Foundation foods did exactly that until usda_api read their
Atwater energy values. Nothing noticed: every meal and recipe using such a
food silently came out hundreds of kcal short.

Two checks, both from a food's own macronutrients (per 100 g):

- missing: no calorie value, but protein, carbs and fat are all present.
  db fills calories with the Atwater general estimate (4/4/9 kcal per g, the
  same basis as USDA's "Energy (Atwater General Factors)") and marks the key
  estimated (foods.estimated_keys_json), so a later refresh with a measured
  value replaces it. With any of the three macros absent there is nothing
  sound to estimate from; the food is left alone and shows as missing
  macronutrients in the completeness check instead.
- mismatch: a stored calorie value far from what the macros imply. Flags,
  never changes anything — the gap can be real (alcohol, sugar alcohols and
  very high fibre all carry energy 4/4/9 doesn't model), so the user decides.

Docs: README-numa-documentation.md, Architecture: "numa_app/services/energy_check.py — calorie checks"
"""
from __future__ import annotations

_MACROS = ("protein_g", "carbs_g", "fat_g")

# A stored value outside [low, high] of the macro-based estimate counts as a
# mismatch. Two estimates bound the plausible range: general 4/4/9, and one
# counting fibre at 0 kcal/g (high-fibre foods measure well under 4/4/9). The 25% band plus a 25 kcal floor keep very-low-calorie foods (herbs,
# broth, greens) from tripping it on rounding alone.
MISMATCH_FRACTION = 0.25
MISMATCH_FLOOR_KCAL = 25.0
# A mismatch is named on a meal/recipe/day page only when it moves that
# total by at least this much — 1 g of vanilla extract (mostly alcohol) is
# a genuine mismatch but not worth a warning.
NOTE_MIN_KCAL = 10.0


def atwater_estimate(nutrients: dict) -> float | None:
    """Calories per 100 g from protein, carbs and fat at 4/4/9 kcal/g, or
    None unless all three are present."""
    if any(nutrients.get(k) is None for k in _MACROS):
        return None
    return (4 * float(nutrients["protein_g"]) + 4 * float(nutrients["carbs_g"])
            + 9 * float(nutrients["fat_g"]))


def _fibre_adjusted_estimate(nutrients: dict) -> float | None:
    base = atwater_estimate(nutrients)
    if base is None:
        return None
    fibre = min(float(nutrients.get("fiber_g") or 0), float(nutrients["carbs_g"]))
    # Fibre at 0 kcal: the low end of what's measured (cocoa powder, 37 g
    # fibre, is 228 kcal against a 4/4/9 433).
    return base - 4 * fibre


def calories_missing(nutrients: dict) -> bool:
    """No calorie value at all. (Callers skip foods whose macronutrients the
    user marked "not needed" — a pinch of a spice.)"""
    return nutrients.get("calories") is None


def fill_missing_calories(nutrients: dict) -> bool:
    """Set nutrients["calories"] from atwater_estimate() when it is missing
    and an estimate is possible. Returns True if it filled one."""
    if nutrients.get("calories") is not None:
        return False
    est = atwater_estimate(nutrients)
    if est is None or est <= 0:
        return False
    nutrients["calories"] = round(est, 1)
    return True


def calorie_mismatch(nutrients: dict) -> dict | None:
    """{"stored", "expected_low", "expected_high"} when the stored calories are
    implausible for the food's macros, else None (also None when either side
    is unknown)."""
    stored = nutrients.get("calories")
    general = atwater_estimate(nutrients)
    if stored is None or general is None:
        return None
    fibre_adj = _fibre_adjusted_estimate(nutrients)
    low = min(general, fibre_adj) * (1 - MISMATCH_FRACTION) - MISMATCH_FLOOR_KCAL
    high = max(general, fibre_adj) * (1 + MISMATCH_FRACTION) + MISMATCH_FLOOR_KCAL
    stored = float(stored)
    if low <= stored <= high:
        return None
    return {"stored": stored, "expected_low": max(low, 0.0), "expected_high": high,
            "expected": general}
