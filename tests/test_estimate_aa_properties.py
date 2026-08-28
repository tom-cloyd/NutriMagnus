"""
Property-based tests for numa_app/services/aa_estimate.py's estimate_aa().

The existing tests/test_aa_estimate.py checks a handful of hand-picked
target/source pairs against hand-computed expected numbers. That's the right
kind of test for "does this specific known case work" — but estimate_aa() is
really a general mathematical claim: scale a source food's AA grams onto a
target's protein content, and the result's AA/protein ratios must equal the
source's AA/protein ratios exactly, for ANY valid target/source pair.

These tests generate many random-but-plausible foods (via Hypothesis) and
check that claim directly, instead of only the cases someone thought to type
in by hand. This is item #2 from the "elevating automated testing" plan
(2026-08-28 discussion) — see CLAUDE.md / user-manual.md Part 2E for context
on the project's overall test tiers.

Also the load-bearing math check for #3's "estimation-path coverage" idea:
this is the same scaling formula that's the only route to usable AA data for
a CoFID/CIQUAL food (see tests/test_web.py's
test_copy_aa_estimates_amino_acids_for_source_with_no_native_aa_data for the
end-to-end route exercise).

Run just these (they're slower/randomized, so you may want to skip them on
every single push once the CI gate lands — see .github/workflows/tests.yml):
    pytest tests/test_estimate_aa_properties.py -q
"""
import pytest
from hypothesis import given, settings, strategies as st

from numa_app.services.aa_estimate import estimate_aa
from usda_api import ESSENTIAL_AMINO_ACIDS

# A plausible per-100g protein content: trace amounts up to a very
# protein-dense food (e.g. isolated protein powder tops out around 90g/100g).
_protein_g = st.floats(min_value=0.1, max_value=95.0, allow_nan=False, allow_infinity=False)

# A plausible AA gram value, generated as a fraction of protein_g directly
# so every generated food is physically sane by construction: no real food
# has more essential-AA-grams than protein-grams, and typical individual-AA
# ratios run roughly 1-9% of protein by weight. Values below 0.001 are
# snapped to exactly 0.0 — at the smallest protein_g this strategy generates
# (0.1g), estimate_aa()'s round(protein_g * frac, 4) would otherwise turn a
# technically-positive-but-tiny fraction (e.g. 1e-149) into a stored 0.0,
# silently defeating the "at least 5 non-zero AAs" filter below. Hypothesis
# found exactly this edge case on the first run of these tests.
_aa_fraction = st.floats(min_value=0.0, max_value=0.15, allow_nan=False, allow_infinity=False).map(
    lambda v: 0.0 if v < 0.001 else v
)

# A dict of {aa_key: fraction} covering all 9 essential AAs, filtered so at
# least 5 are non-zero — has_amino_acid_data() requires exactly that (see
# usda_nutrients.py), and without the filter Hypothesis reliably finds the
# all-zero (or <5-nonzero) case, which correctly triggers estimate_aa()'s
# "no amino acid data to copy" error path rather than the success path
# these tests are checking. That failure path is already covered by the
# hand-written tests in test_aa_estimate.py.
_full_aa_fractions = st.fixed_dictionaries(
    {k: _aa_fraction for k in ESSENTIAL_AMINO_ACIDS}
).filter(lambda d: sum(1 for v in d.values() if v > 0) >= 5)


def _food_with_aa(protein_g: float, fractions: dict[str, float]) -> dict:
    """Build a nutrients dict with protein_g and AA grams derived as
    fractions of that protein — same real-world shape as a cached
    USDA/CNF/AFCD food."""
    nuts = {"protein_g": protein_g}
    for key, frac in fractions.items():
        nuts[key] = round(protein_g * frac, 4)
    return nuts


@settings(max_examples=200)
@given(
    target_protein=_protein_g,
    source_protein=_protein_g,
    fractions=_full_aa_fractions,
)
def test_scaled_ratios_equal_source_ratios(target_protein, source_protein, fractions):
    """The whole point of estimate_aa()'s scaling approach: whatever AA/protein
    ratio the source food had, the target food must end up with that same
    ratio after estimation — that's what makes "borrow AA data from a similar
    food" a defensible estimate rather than an arbitrary number."""
    source = _food_with_aa(source_protein, fractions)
    target = {"protein_g": target_protein}

    updated, factor, err = estimate_aa(target, source)

    assert err is None
    assert updated is not None
    for key in ESSENTIAL_AMINO_ACIDS:
        source_ratio = source[key] / source_protein
        target_ratio = updated[key] / target_protein
        # Tolerance is wider than float-precision because estimate_aa() rounds
        # each scaled AA value to 4 decimal places (see aa_estimate.py), and
        # this test's own fixture data does the same when building `source` —
        # two independent roundings compound, most visibly when protein_g is
        # small (down to 0.1g here) and the rounding error is a larger share
        # of the ratio. 1e-3 absolute is still far tighter than anything that
        # would matter nutritionally (amino acids are reported to 2-3 decimals
        # at most in every real data source this app uses).
        assert target_ratio == pytest.approx(source_ratio, abs=1e-3)


@settings(max_examples=200)
@given(
    target_protein=_protein_g,
    source_protein=_protein_g,
    fractions=_full_aa_fractions,
)
def test_factor_is_target_over_source_protein(target_protein, source_protein, fractions):
    """factor is documented as target_protein / source_protein — pin that
    down directly so a future refactor can't quietly change the formula."""
    source = _food_with_aa(source_protein, fractions)
    target = {"protein_g": target_protein}

    _, factor, err = estimate_aa(target, source)

    assert err is None
    assert factor == pytest.approx(target_protein / source_protein)


@settings(max_examples=200)
@given(
    target_protein=_protein_g,
    source_protein=_protein_g,
    fractions=_full_aa_fractions,
)
def test_non_aa_fields_are_never_touched(target_protein, source_protein, fractions):
    """Regression guard matching test_aa_estimate.py's existing hand-written
    case, generalized: estimate_aa must only ever overwrite AA keys, never
    any other field already on the target (calories, other minerals, etc.)."""
    source = _food_with_aa(source_protein, fractions)
    target = {"protein_g": target_protein, "calories": 123.0, "fiber_g": 4.5}

    updated, _, err = estimate_aa(target, source)

    assert err is None
    assert updated["calories"] == 123.0
    assert updated["fiber_g"] == 4.5
    assert updated["protein_g"] == target_protein
