"""
Property-based tests for diaas.py's meal_level_diaas() and get_digestibility().

Complements tests/test_diaas.py, which checks specific known food combinations
(soy, pea, pumpkin seed, etc.) against hand-verified expected scores. These
tests instead generate many random-but-plausible ingredient lists and check
invariants that must hold for ANY input, not just the examples someone
thought to write by hand — item #2 from the "elevating automated testing"
plan (2026-08-28 discussion).

No database is touched: meal_level_diaas()'s conn parameter is optional and
only used for user digestibility overrides, so passing None exercises the
pure calculation path.

Run just these (slower/randomized — see .github/workflows/tests.yml for how
they fit into the CI gate):
    pytest tests/test_diaas_properties.py -q
"""
import pytest
from hypothesis import given, settings, strategies as st

import diaas as _diaas
from diaas import FAO_REFERENCE, get_digestibility, meal_level_diaas

_protein_g = st.floats(min_value=0.1, max_value=95.0, allow_nan=False, allow_infinity=False)
_aa_fraction = st.floats(min_value=0.0, max_value=0.15, allow_nan=False, allow_infinity=False)
_grams = st.floats(min_value=1.0, max_value=1000.0, allow_nan=False, allow_infinity=False)
_food_name = st.text(min_size=1, max_size=40)

_full_aa_fractions = st.fixed_dictionaries({k: _aa_fraction for k in FAO_REFERENCE})


def _nutrients(protein_g: float, fractions: dict[str, float]) -> dict:
    nuts = {"protein_g": protein_g}
    for key, frac in fractions.items():
        nuts[key] = round(protein_g * frac, 4)
    return nuts


_ingredient = st.builds(
    lambda name, protein, fractions, grams: {
        "food_name": name,
        "nutrients_100g": _nutrients(protein, fractions),
        "grams": grams,
    },
    name=_food_name,
    protein=_protein_g,
    fractions=_full_aa_fractions,
    grams=_grams,
)

_ingredients_list = st.lists(_ingredient, min_size=1, max_size=3)


# ---------------------------------------------------------------------------
# get_digestibility
# ---------------------------------------------------------------------------

@settings(max_examples=150)
@given(food_name=_food_name)
def test_digestibility_always_in_valid_physical_range(food_name):
    """A true ileal digestibility coefficient is a fraction of protein
    absorbed — it cannot be <= 0 or > 1.0 for any food, real or randomly
    generated. This is a plausibility guard on the _DIGESTIBILITY_TABLE /
    _CATEGORY_DEFAULTS data itself: a typo like 9.6 instead of 0.96 would
    trip this immediately."""
    dig, source = get_digestibility(food_name, conn=None)
    assert 0.0 < dig <= 1.0
    assert isinstance(source, str) and source


# ---------------------------------------------------------------------------
# meal_level_diaas
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(ingredients=_ingredients_list)
def test_total_protein_g_matches_manual_sum(ingredients):
    """Accounting identity: total_protein_g must equal the sum of each
    ingredient's own protein_g * grams/100, regardless of AA content."""
    result = meal_level_diaas(ingredients, conn=None)
    expected = sum(
        ing["nutrients_100g"].get("protein_g", 0.0) * ing["grams"] / 100.0
        for ing in ingredients
    )
    assert result["total_protein_g"] == pytest.approx(expected, rel=1e-6)


@settings(max_examples=100)
@given(ingredients=_ingredients_list)
def test_diaas_is_none_or_non_negative(ingredients):
    """diaas is documented as possibly exceeding 1.0 (it is NOT capped —
    see diaas.py's meal_level_diaas docstring), but it can never be
    negative: every IAA ratio is pooled-digestible-grams / reference-grams,
    both of which are non-negative by construction."""
    result = meal_level_diaas(ingredients, conn=None)
    if result["diaas"] is not None:
        assert result["diaas"] >= 0.0


@settings(max_examples=100)
@given(ingredients=_ingredients_list)
def test_dcp_never_exceeds_digestible_protein_ceiling(ingredients):
    """digestible_complete_protein_g is documented as capped at
    aa_dig_protein_g (the digestibility-corrected protein from AA-analyzed
    foods) — that's a physical ceiling, you can't have more "complete
    digestible protein" than digestible protein. Also must never be
    negative."""
    result = meal_level_diaas(ingredients, conn=None)
    dcp = result["digestible_complete_protein_g"]
    if dcp is not None:
        assert dcp >= 0.0
        assert dcp <= result["aa_dig_protein_g"] + 1e-6


@settings(max_examples=100)
@given(ingredients=_ingredients_list)
def test_single_ingredient_diaas_matches_its_own_limiting_ratio(ingredients):
    """Sanity cross-check against a second, independent computation path:
    for a single-ingredient meal, the pooled composite DIAAS must equal the
    worst (minimum) of that food's own digestibility-adjusted IAA ratios,
    computed directly from FAO_REFERENCE rather than via meal_level_diaas'
    internal pooling — catches a pooling-logic regression that a
    single-ingredient case should never be able to trigger in the first
    place."""
    if len(ingredients) != 1:
        return
    ing = ingredients[0]
    nuts = ing["nutrients_100g"]
    protein_g = nuts["protein_g"]
    dig, _ = get_digestibility(ing["food_name"], conn=None)

    expected_ratios = {}
    for aa_key, ref_mg_per_g in FAO_REFERENCE.items():
        raw_g = nuts.get(aa_key, 0.0)
        if raw_g <= 0:
            continue  # matches meal_level_diaas: an AA with 0 g is excluded
            # from scoring entirely, not treated as a ratio of 0 — see its
            # pooled_counts[aa_key] > 0 gate.
        ref_g = ref_mg_per_g / 1000.0 * protein_g
        if ref_g > 0:
            expected_ratios[aa_key] = (raw_g * dig) / ref_g
    if not expected_ratios:
        return
    expected_diaas = min(expected_ratios.values())

    result = meal_level_diaas(ingredients, conn=None)
    assert result["diaas"] == pytest.approx(expected_diaas, rel=1e-6)
