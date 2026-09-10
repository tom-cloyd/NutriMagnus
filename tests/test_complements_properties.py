"""
Property-based tests for usda_nutrients.py's complement-suggestion engine:
get_aa_gaps(), _score_one_complement() (the shared gap-closing solver used by
both suggest_complements()'s single-food tiers and its two-food "pairs"
cascade), and suggest_complements() itself.

Complements tests/test_complements.py, which checks specific hand-picked food
combinations. These generate many random-but-plausible protein/amino-acid
profiles and check invariants that must hold for ANY input — item #2's
"harder half" from TESTING-ROADMAP.md (deferred on 2026-08-28 pending a full
read of suggest_complements(), done 2026-09-09).

No database is touched — every function under test here is pure, operating
only on plain nutrient dicts passed in directly.

Construction strategy: rather than generating fully random amino-acid panels
(which would almost never happen to contain an actual, closeable gap — the
precondition every function here requires to do anything interesting),
each test builds a base food with every essential AA "adequate" (at some
Hypothesis-chosen multiple of the FAO reference) except one deliberately
zeroed target AA, and a candidate food rich enough in that target AA to
close it (also Hypothesis-chosen). This mirrors the AA panels real foods
actually have — one or two limiting AAs, not all nine random — while still
exploring a wide range of protein amounts and margins. Preconditions that
can still fail for extreme draws (e.g. no valid closing solution, or a
suggestion small enough that integer-gram rounding could itself reopen the
gap — see the "grams >= 15" filters below, verified against 500 manual
trials before being written into the strategy) are filtered with assume().

Run just these:
    pytest tests/test_complements_properties.py -q
"""
from hypothesis import HealthCheck, assume, given, settings, strategies as st

import usda_nutrients as un
from usda_nutrients import AA_REFERENCE_MG_PER_G_PROTEIN as REF

_ESSENTIAL_AAS = list(REF.keys())

_protein_g = st.floats(min_value=5.0, max_value=40.0, allow_nan=False, allow_infinity=False)
_adequacy = st.floats(min_value=1.05, max_value=3.0, allow_nan=False, allow_infinity=False)
_rich_factor = st.floats(min_value=1.5, max_value=20.0, allow_nan=False, allow_infinity=False)


def _adequate_nutrients(protein_g: float, factor: float, zero: tuple[str, ...] = ()) -> dict:
    """A food with every essential AA at `factor` times the FAO reference
    ratio (comfortably non-gapped when factor > 1), except any AA named in
    `zero`, which is set to 0 g."""
    nuts = {"protein_g": protein_g}
    for aa in _ESSENTIAL_AAS:
        nuts[aa] = 0.0 if aa in zero else REF[aa] / 1000.0 * protein_g * factor
    return nuts


def _score_for(nutrients: dict, aa_key: str) -> float | None:
    return un.protein_completeness(nutrients)["scores"].get(aa_key)


# ---------------------------------------------------------------------------
# get_aa_gaps
# ---------------------------------------------------------------------------

@settings(max_examples=150)
@given(protein_g=_protein_g, adequacy=_adequacy)
def test_adequate_food_has_no_gaps(protein_g, adequacy):
    """A food with every essential AA at or above the reference ratio must
    never be reported as gapped — get_aa_gaps() should return []."""
    nuts = _adequate_nutrients(protein_g, adequacy)
    assert un.get_aa_gaps(nuts) == []


@settings(max_examples=150)
@given(protein_g=_protein_g, adequacy=_adequacy)
def test_zeroed_aa_always_appears_as_the_worst_gap(protein_g, adequacy):
    """A food with one essential AA at zero (everything else adequate) must
    report exactly that AA as a gap, and it must sort first (lowest score)
    since every other AA scores >= 1.0."""
    nuts = _adequate_nutrients(protein_g, adequacy, zero=("aa_lysine_g",))
    gaps = un.get_aa_gaps(nuts)
    assert gaps
    assert gaps[0][0] == "aa_lysine_g"
    assert gaps[0][1] == 0.0


# ---------------------------------------------------------------------------
# _score_one_complement — the shared gap-closing solver
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(
    base_protein=_protein_g, adequacy=_adequacy,
    cand_protein=_protein_g, lys_factor=_rich_factor,
)
def test_gap_closing_is_monotonic_in_grams_added(base_protein, adequacy, cand_protein, lys_factor):
    """Adding more of a food that's rich in the limiting AA (relative to its
    own protein) can never make that AA's score worse — scoring it at 0%,
    25%, 50%, 75%, and 100% of the solved gram amount must be non-decreasing.
    This is the "Monotonicity" invariant from TESTING-ROADMAP.md."""
    base = _adequate_nutrients(base_protein, adequacy, zero=("aa_lysine_g",))
    gaps = un.get_aa_gaps(base)
    cand = _adequate_nutrients(cand_protein, adequacy)
    cand["aa_lysine_g"] = REF["aa_lysine_g"] / 1000.0 * cand_protein * lys_factor

    metrics = un._score_one_complement(base, gaps, 1.0, cand, None, "aa_lysine_g")
    assume(metrics is not None)
    grams = metrics["grams"]

    scores = []
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        combined = un.sum_nutrients(base, un.scale_nutrients(cand, grams * frac))
        scores.append(_score_for(combined, "aa_lysine_g"))
    for earlier, later in zip(scores, scores[1:]):
        assert later >= earlier - 1e-9


@settings(max_examples=100)
@given(
    base_protein=_protein_g, adequacy=_adequacy,
    cand_protein=_protein_g, lys_factor=_rich_factor,
)
def test_suggested_grams_actually_closes_the_gap(base_protein, adequacy, cand_protein, lys_factor):
    """Suggestion self-consistency (TESTING-ROADMAP.md): whatever gram amount
    a gap-closer suggestion proposes, feeding that amount back in must
    actually clear the gap it claims to clear — checked here via the exact
    solver (_score_one_complement); the full public suggest_complements()
    path is checked end-to-end in test_pairs_cascade_closes_all_gaps below.
    Suggestions under 15 g are excluded: integer-gram display rounding can
    lose a large enough fraction of a tiny suggestion to reopen the gap by a
    few points (verified by hand against 500 generated cases before writing
    this filter) — a real, accepted display-rounding tradeoff, not the
    solver-correctness property this test is protecting."""
    base = _adequate_nutrients(base_protein, adequacy, zero=("aa_lysine_g",))
    gaps = un.get_aa_gaps(base)
    cand = _adequate_nutrients(cand_protein, adequacy)
    cand["aa_lysine_g"] = REF["aa_lysine_g"] / 1000.0 * cand_protein * lys_factor

    metrics = un._score_one_complement(base, gaps, 1.0, cand, None, "aa_lysine_g")
    assume(metrics is not None and metrics["grams"] >= 15)

    combined = un.sum_nutrients(base, un.scale_nutrients(cand, metrics["grams"]))
    remaining = un.get_aa_gaps(combined)
    assert not any(aa == "aa_lysine_g" for aa, _, _ in remaining)


# ---------------------------------------------------------------------------
# suggest_complements — the "pairs" gap-cascade tier
# ---------------------------------------------------------------------------

@settings(max_examples=60, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    base_protein=st.floats(min_value=5.0, max_value=20.0, allow_nan=False, allow_infinity=False),
    adequacy=st.floats(min_value=1.1, max_value=2.0, allow_nan=False, allow_infinity=False),
    a_protein=st.floats(min_value=10.0, max_value=40.0, allow_nan=False, allow_infinity=False),
    a_lys_factor=_rich_factor,
    b_protein=st.floats(min_value=5.0, max_value=30.0, allow_nan=False, allow_infinity=False),
    b_met_factor=_rich_factor,
    b_lys_factor=st.floats(min_value=0.8, max_value=3.0, allow_nan=False, allow_infinity=False),
)
def test_pairs_cascade_closes_all_gaps_and_ranking_is_consistent(
    base_protein, adequacy, a_protein, a_lys_factor, b_protein, b_met_factor, b_lys_factor,
):
    """Gap-cascade pairs (TESTING-ROADMAP.md "Ranking stability"): construct a
    base food gapped on lysine, a candidate A rich in lysine but with zero
    methionine (closes lysine, dilutes methionine into a new gap — this is
    the "opens_new_gap" case _build_pairs specifically looks for), and a
    candidate B rich in methionine (and carrying enough of its own lysine
    to not re-dilute it below the reference). Two properties, checked
    against the real public suggest_complements() output:

    1. The self-consistency property, end to end this time: the A+B pair
       suggest_complements() returns must show gaps_closed=True — i.e. the
       amounts it proposes for BOTH foods together really do clear every
       remaining gap, not just the one A was chosen for.
    2. The ranking-stability property: pairs.sort()'s promotion rule ("a
       pair that both closes every gap AND totals <= 50 g ranks before any
       pair that doesn't meet both") must hold over whatever the real sort
       produced — not just our constructed pair, but the full returned list.

    Preconditions (A actually opens a new gap; B actually closes it without
    reopening lysine or anything else; suggested amounts aren't tiny enough
    for rounding to matter — same 15g reasoning as the solver test above)
    fail for a meaningful fraction of draws, same as the geometric
    reasoning behind any two-food cascade — filtered with assume() rather
    than fought with narrower ranges, since narrower ranges would just
    trade unverified-by-hand-trial ranges for unverified-by-hand-trial
    ranges. Verified by hand (300 trials, plain Python, no Hypothesis) to
    keep ~38% of draws before writing this as the formal test.
    """
    base = _adequate_nutrients(base_protein, adequacy, zero=("aa_lysine_g",))
    base["aa_methionine_g"] = REF["aa_methionine_g"] / 1000.0 * base_protein  # right at threshold
    gaps = un.get_aa_gaps(base)
    assume(gaps and gaps[0][0] == "aa_lysine_g")

    cand_a = _adequate_nutrients(a_protein, adequacy)
    cand_a["aa_lysine_g"] = REF["aa_lysine_g"] / 1000.0 * a_protein * a_lys_factor
    cand_a["aa_methionine_g"] = 0.0

    a_metrics = un._score_one_complement(base, gaps, 1.0, cand_a, None, "aa_lysine_g")
    assume(a_metrics is not None and a_metrics["opens_new_gap"] and a_metrics["grams"] >= 10)

    combined_after_a = un.sum_nutrients(base, un.scale_nutrients(cand_a, a_metrics["grams"]))
    gaps_after_a = un.get_aa_gaps(combined_after_a)
    assume(gaps_after_a)
    target_b = gaps_after_a[0][0]

    cand_b = _adequate_nutrients(b_protein, adequacy)
    cand_b["aa_methionine_g"] = REF["aa_methionine_g"] / 1000.0 * b_protein * b_met_factor
    cand_b["aa_lysine_g"] = REF["aa_lysine_g"] / 1000.0 * b_protein * b_lys_factor

    b_metrics = un._score_one_complement(combined_after_a, gaps_after_a, 1.0, cand_b, None, target_b)
    assume(
        b_metrics is not None and b_metrics["remaining_gaps"] == 0
        and not b_metrics["opens_new_gap"] and b_metrics["grams"] >= 5
        # _build_pairs() itself rejects any pair whose combined amount
        # exceeds 600 g as impractical — found by a 10x-max_examples stress
        # run before this filter was added, where a real (large-quantity)
        # A+B combination correctly closed every gap by the solver's own
        # math but was then, correctly, absent from suggest_complements()'s
        # pairs tier for exceeding that cap.
        and a_metrics["grams"] + b_metrics["grams"] <= 600
    )

    result = un.suggest_complements(
        base,
        pantry_candidates=[
            {"name": "Candidate A", "nutrients": cand_a, "diaas": None},
            {"name": "Candidate B", "nutrients": cand_b, "diaas": None},
        ],
    )
    pairs = result["pairs"]

    target_pair_names = frozenset(["Candidate A", "Candidate B"])
    matches = [p for p in pairs if frozenset(f["name"] for f in p["foods"]) == target_pair_names]
    assert matches, "constructed A+B pair did not appear in suggest_complements()'s pairs tier"
    assert matches[0]["gaps_closed"], "A+B pair reported but does not actually close every gap"

    def _rank(p: dict) -> float:
        return 0.0 if (p["gaps_closed"] and p["total_grams"] <= 50) else 1.0

    ranks = [_rank(p) for p in pairs]
    assert ranks == sorted(ranks), "a promoted (gaps_closed, <=50g) pair sorted after a non-promoted one"
