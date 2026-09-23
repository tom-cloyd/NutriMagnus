"""
Tests for numa_app/services/complements.py — the complement-suggestion
display math used by the web backend (web/backend.py).
"""
import json
import sqlite3

import pytest

import usda as _usda
from numa_app.services import complements as _complements
from numa_app.services.portions import amount_note as _amount_note
from tests.conftest import SAMPLE_NUTRIENTS

_DEFICIENT_NUTRIENTS = {
    "protein_g":          20.0,
    "aa_tryptophan_g":    0.08,
    "aa_threonine_g":     0.60,
    "aa_isoleucine_g":    0.80,
    "aa_leucine_g":       1.40,
    "aa_lysine_g":        0.50,
    "aa_methionine_g":    0.60,
    "aa_phenylalanine_g": 0.90,
    "aa_valine_g":        0.90,
    "aa_histidine_g":     0.40,
}


# ---------------------------------------------------------------------------
# aa_effects
# ---------------------------------------------------------------------------

class TestAAEffects:
    def test_scales_raw_new_score_by_digestibility(self):
        # usda.suggest_complements' new_scores are always raw (pre-digestibility);
        # aa_effects must rescale them onto the same basis as gaps' orig_scores
        # before comparing, or a food with real DIAAS < 1.0 looks falsely "met".
        gaps = [("aa_lysine_g", 0.92, 5.0)]
        suggestion = {"new_scores": {"aa_lysine_g": 1.10}}

        effects = _complements.aa_effects(suggestion, gaps, digestibility=0.88)
        assert effects[0]["after"] == pytest.approx(1.10 * 0.88, abs=0.01)
        assert effects[0]["met"] is False

    def test_digestibility_1_0_is_a_no_op(self):
        gaps = [("aa_lysine_g", 0.92, 5.0)]
        suggestion = {"new_scores": {"aa_lysine_g": 1.10}}
        effects = _complements.aa_effects(suggestion, gaps, digestibility=1.0)
        assert effects[0]["after"] == pytest.approx(1.10)
        assert effects[0]["met"] is True

    def test_falls_back_to_orig_score_when_aa_missing(self):
        gaps = [("aa_lysine_g", 0.92, 5.0)]
        effects = _complements.aa_effects({"new_scores": {}}, gaps, digestibility=0.88)
        assert effects[0]["after"] == pytest.approx(0.92)

    def test_respects_limit(self):
        gaps = [("aa_lysine_g", 0.5, 1), ("aa_leucine_g", 0.6, 1), ("aa_valine_g", 0.7, 1)]
        effects = _complements.aa_effects({"new_scores": {}}, gaps, limit=2)
        assert len(effects) == 2

    def test_label_and_before_match_the_input_exactly(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found nothing
        # checked "label"'s or "before"'s actual value — a survivor read
        # nutrient_label(aa)[1] (the unit, e.g. "g") instead of [0] (the
        # display name, e.g. "Lysine") for "label", and several more mutated
        # "before"'s rounding/key without any test noticing.
        gaps = [("aa_lysine_g", 0.9234, 5.0)]
        effects = _complements.aa_effects({"new_scores": {}}, gaps)
        assert effects[0]["label"] == "Lysine"
        assert effects[0]["before"] == pytest.approx(0.92)  # rounded to 2 dp

    def test_met_is_true_at_exactly_1_0(self):
        # A survivor changed "new_score >= 1.0" to "> 1.0" — a suggestion
        # that lands EXACTLY at the reference score (not above it) must
        # still count as having met the gap.
        gaps = [("aa_lysine_g", 0.92, 5.0)]
        suggestion = {"new_scores": {"aa_lysine_g": 1.0}}
        effects = _complements.aa_effects(suggestion, gaps, digestibility=1.0)
        assert effects[0]["after"] == pytest.approx(1.0)
        assert effects[0]["met"] is True


# ---------------------------------------------------------------------------
# exact_dcp
# ---------------------------------------------------------------------------

_OATS_100G = {
    "protein_g": 13.0, "aa_lysine_g": 0.5, "aa_methionine_g": 0.2, "aa_cystine_g": 0.15,
    "aa_threonine_g": 0.4, "aa_tryptophan_g": 0.15, "aa_isoleucine_g": 0.5,
    "aa_leucine_g": 0.9, "aa_phenylalanine_g": 0.6, "aa_valine_g": 0.6, "aa_histidine_g": 0.25,
}
_PEANUT_BUTTER_100G = {
    "protein_g": 25.0, "aa_lysine_g": 0.9, "aa_methionine_g": 0.3, "aa_cystine_g": 0.3,
    "aa_threonine_g": 0.8, "aa_tryptophan_g": 0.25, "aa_isoleucine_g": 0.9,
    "aa_leucine_g": 1.6, "aa_phenylalanine_g": 1.3, "aa_valine_g": 1.1, "aa_histidine_g": 0.6,
}


class TestExactDcp:
    # exact_dcp() had NO direct tests before a mutation-testing pass
    # (TESTING-ROADMAP.md item #5) — every other test in this file passes
    # ingredients=None specifically to force its early "if not ingredients:
    # return None" return, so the real DB-backed success path (the whole
    # reason this function exists) was completely unexercised. One survivor
    # inverted "if dcp is not None else None" to "if dcp is None else None"
    # — meaning exact_dcp would ALWAYS return None whenever it actually had
    # a real value to return.

    def test_none_without_ingredients(self):
        assert _complements.exact_dcp(None, [("Food", {"protein_g": 10}, 50)]) is None

    def test_none_without_usable_extra(self):
        ingredients = [{"food_name": "Base", "nutrients_100g": {"protein_g": 10}, "grams": 100}]
        assert _complements.exact_dcp(ingredients, []) is None
        assert _complements.exact_dcp(ingredients, [("X", None, 50)]) is None
        assert _complements.exact_dcp(ingredients, [("X", {"protein_g": 10}, 0)]) is None

    def test_real_dcp_matches_independent_meal_level_diaas_call(self, db_conn):
        import diaas as _diaas
        ingredients = [{"food_name": "Oats", "nutrients_100g": _OATS_100G, "grams": 100.0}]
        extra = [("Peanut butter", _PEANUT_BUTTER_100G, 50.0)]

        result = _complements.exact_dcp(ingredients, extra)

        # Independently recompute via a direct meal_level_diaas() call — a
        # different call path than exact_dcp()'s internals — rather than
        # re-deriving the DCP math by hand, which diaas.py's own dedicated
        # tests already cover extensively.
        extra_ings = [{"food_name": n, "nutrients_100g": nuts, "grams": g} for n, nuts, g in extra]
        expected = _diaas.meal_level_diaas(ingredients + extra_ings, db_conn)
        expected_dcp = round(expected["digestible_complete_protein_g"], 1)

        assert result is not None
        assert result == pytest.approx(expected_dcp)


# ---------------------------------------------------------------------------
# two_step_combo
# ---------------------------------------------------------------------------

class TestTwoStepCombo:
    def test_none_without_comp_nutrients(self):
        combo = _complements.two_step_combo(
            {"grams": 50, "protein_added": 5}, SAMPLE_NUTRIENTS,
            base_protein=20.0, base_digestible=20.0,
            pantry_candidates=[], diet_pref="all",
            gaps=[("aa_lysine_g", 0.9, 2.0)], max_improver_grams=120,
        )
        assert combo is None

    def test_step1_fields_match_gc_and_dcp_fallback_formula(self):
        # This was the ONLY test for two_step_combo() before a mutation-testing
        # pass (TESTING-ROADMAP.md item #5) — and it only exercised the early
        # "no comp_nutrients" None-return, never the actual step1-building
        # success path. 191 survivors, almost all dict-key-literal or
        # dropped-argument mutations nothing here would have caught.
        gc = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])["general"][0]
        gaps = _usda.get_aa_gaps(_DEFICIENT_NUTRIENTS)
        base_protein = _DEFICIENT_NUTRIENTS["protein_g"]
        base_digestible = base_protein  # digestibility=1.0

        combo = _complements.two_step_combo(
            gc, _DEFICIENT_NUTRIENTS,
            base_protein=base_protein, base_digestible=base_digestible,
            pantry_candidates=[], diet_pref="all", gaps=gaps,
            max_improver_grams=120,
            # ingredients=None forces exact_dcp() to return None immediately
            # (see its own "if not ingredients: return None"), so dcp_after
            # below must come from the documented fallback formula, not a
            # real per-ingredient recompute.
            ingredients=None,
        )
        assert combo is not None
        step1 = combo["step1"]
        assert step1["name"] == gc["name"]
        assert step1["fdc_id"] == gc.get("fdc_id")
        assert step1["estimated"] == gc.get("estimated", False)
        assert step1["grams"] == gc["grams"]
        assert step1["diaas"] == (round(gc["diaas"], 2) if gc.get("diaas") else None)
        assert step1["amount_note"] == _amount_note(gc["grams"], gc["name"], fdc_id=gc.get("fdc_id"))
        assert step1["dcp_before"] == round(base_digestible, 1)
        # aa_effects() is independently tested elsewhere (TestAAEffects) —
        # here we're only checking step1 actually plumbs gc/gaps/
        # fallback_digestibility/aa_effects_limit into it correctly.
        assert step1["aa_effects"] == _complements.aa_effects(gc, gaps, digestibility=1.0, limit=3)

        # gc_diaas is capped at 1.0 — predicted_diaas is an uncapped per-AA-score
        # minimum and can mathematically exceed 1.0 when the combined pool
        # over-supplies every essential amino acid; DIAAS itself never does.
        gc_diaas = min(1.0, gc.get("predicted_diaas") or 1.0)  # fallback_digestibility default
        assert combo["gc_diaas"] == gc_diaas
        expected_dcp_after = round(
            (base_protein + gc.get("protein_added", 0)) * min(1.0, gc_diaas), 1
        )
        assert step1["dcp_after"] == expected_dcp_after

    def test_step1_dcp_after_uses_real_exact_dcp_when_ingredients_provided(self):
        # Every two_step_combo() test above uses ingredients=None, only ever
        # exercising the dcp_after fallback formula — never gc_dcp's real
        # per-ingredient exact_dcp() recompute (the reason `ingredients` is
        # a parameter at all). Same base/gc as the "sparse profile" tests
        # elsewhere in this class, this time with a real ingredients list.
        base = {
            "protein_g": 20.0,
            "aa_methionine_g": 0.10, "aa_cystine_g": 0.06,
            "aa_lysine_g": 0.30,
        }
        gc = {
            "name": "GapCloser", "fdc_id": None, "grams": 10, "protein_added": 10.0,
            "diaas": 0.5, "predicted_diaas": 0.5,
            "comp_nutrients": {"protein_g": 100.0, "aa_methionine_g": 1.5, "aa_cystine_g": 1.5},
        }
        gaps = _usda.get_aa_gaps(base)
        ingredients = [{"food_name": "BaseFood", "nutrients_100g": base, "grams": 100.0}]

        combo = _complements.two_step_combo(
            gc, base, base_protein=20.0, base_digestible=20.0,
            pantry_candidates=[], diet_pref="all", gaps=gaps,
            max_improver_grams=300, ingredients=ingredients,
        )
        assert combo is not None
        expected = _complements.exact_dcp(ingredients, [("GapCloser", gc["comp_nutrients"], 10)])
        assert expected is not None
        assert combo["step1"]["dcp_after"] == pytest.approx(expected)
        # Same scenario without ingredients (see the sparse-profile test
        # above) gives dcp_after=15.0 via the fallback formula — confirm
        # the real per-ingredient path gives a genuinely different number,
        # not a coincidental match with the fallback.
        assert combo["step1"]["dcp_after"] != pytest.approx(15.0)
        # step2's own dcp_before must track step1's dcp_after here too.
        if combo["step2"] is not None:
            assert combo["step2"]["dcp_before"] == combo["step1"]["dcp_after"]

    def test_step2_fields_when_a_qualifying_diaas_improver_exists(self):
        # step2 (the DIAAS-booster pairing) had no test at all — every
        # earlier attempt at constructing a scenario where a qualifying
        # improver exists failed; this one works: a low-digestibility (0.5)
        # gap-closer leaves the Met+Cys gap closed but Lysine still short,
        # which the curated table's own strong-lysine entries can improve.
        base = {
            "protein_g": 20.0,
            "aa_methionine_g": 0.10, "aa_cystine_g": 0.06,
            "aa_lysine_g": 0.30,
        }
        gc = {
            "name": "GapCloser", "fdc_id": None, "grams": 10, "protein_added": 10.0,
            "diaas": 0.5, "predicted_diaas": 0.5,
            "comp_nutrients": {"protein_g": 100.0, "aa_methionine_g": 1.5, "aa_cystine_g": 1.5},
        }
        gaps = _usda.get_aa_gaps(base)

        combo = _complements.two_step_combo(
            gc, base, base_protein=20.0, base_digestible=20.0,
            pantry_candidates=[], diet_pref="all", gaps=gaps,
            max_improver_grams=300, ingredients=None,
        )
        assert combo is not None
        step2 = combo["step2"]
        assert step2 is not None, "expected a qualifying DIAAS-improver for this scenario"

        # This scenario deterministically picks "Soy protein isolate" from
        # the curated table (verified stable across repeated runs) — pin
        # every field, not just a couple, per the comprehensive-field-test
        # technique from the previous round (proved far more efficient than
        # one narrow test per mutant sampled).
        assert step2["name"] == "Soy protein isolate"
        assert step2["fdc_id"] == 174276
        assert step2["estimated"] is False
        assert step2["diaas"] == pytest.approx(0.97)
        assert step2["grams"] == 30
        assert step2["amount_note"] == _amount_note(30, "Soy protein isolate", fdc_id=174276)
        assert step2["new_diaas"] == pytest.approx(0.57)
        # step2's "dcp_before" must be exactly step1's "dcp_after" — the pool
        # after step1 is the starting point step2 improves on.
        assert step2["dcp_before"] == combo["step1"]["dcp_after"]
        assert step2["dcp_after"] == pytest.approx(32.0)
        assert step2["net_gain"] == pytest.approx(round(step2["dcp_after"] - 20.0, 1))

    def test_step2_dcp_after_uses_real_exact_dcp_when_ingredients_provided(self):
        # The one incomplete corner of the "ingredients provided" dimension
        # (TESTING-ROADMAP.md item #5, round 6): step2's own b_dcp exact_dcp()
        # call, with a real ingredients list. Same deterministic scenario as
        # the sparse-profile tests above (always picks "Soy protein isolate"),
        # now with ingredients provided — usda.get_complement_nutrients()
        # gives an independent way to fetch that winner's real curated
        # nutrient profile for the cross-check, without hard-coding it.
        base = {
            "protein_g": 20.0,
            "aa_methionine_g": 0.10, "aa_cystine_g": 0.06,
            "aa_lysine_g": 0.30,
        }
        gc = {
            "name": "GapCloser", "fdc_id": None, "grams": 10, "protein_added": 10.0,
            "diaas": 0.5, "predicted_diaas": 0.5,
            "comp_nutrients": {"protein_g": 100.0, "aa_methionine_g": 1.5, "aa_cystine_g": 1.5},
        }
        gaps = _usda.get_aa_gaps(base)
        ingredients = [{"food_name": "BaseFood", "nutrients_100g": base, "grams": 100.0}]

        combo = _complements.two_step_combo(
            gc, base, base_protein=20.0, base_digestible=20.0,
            pantry_candidates=[], diet_pref="all", gaps=gaps,
            max_improver_grams=300, ingredients=ingredients,
        )
        assert combo is not None
        step2 = combo["step2"]
        assert step2 is not None

        b_comp_nutrients = _usda.get_complement_nutrients(step2["name"])
        assert b_comp_nutrients is not None
        expected = _complements.exact_dcp(ingredients, [
            ("GapCloser", gc["comp_nutrients"], gc["grams"]),
            (step2["name"], b_comp_nutrients, step2["grams"]),
        ])
        assert expected is not None
        assert step2["dcp_after"] == pytest.approx(expected)
        # Note: unlike step1's dcp_after (which clearly differs from its
        # ingredients=None counterpart, 5.1 vs 15.0), this scenario's real
        # and fallback b_dcp values happen to coincide at 32.0 — a genuine
        # coincidence of this specific base/candidate combination, not
        # evidence the real path isn't being exercised (the cross-check
        # against an independent exact_dcp() call above already proves that).

    def test_step1_aa_effects_respects_aa_effects_limit(self):
        # A survivor dropped aa_effects_limit entirely from step1's internal
        # aa_effects() call (passing limit=None instead) — invisible in the
        # tests above since their scenarios only ever had 1-2 gaps, below
        # the default limit of 3. This base has 9.
        base = {
            "protein_g": 20.0,
            "aa_tryptophan_g": 0.05, "aa_threonine_g": 0.20, "aa_isoleucine_g": 0.20,
            "aa_leucine_g": 0.30, "aa_lysine_g": 0.20, "aa_methionine_g": 0.10,
            "aa_phenylalanine_g": 0.20, "aa_valine_g": 0.20, "aa_histidine_g": 0.10,
        }
        gc = {"name": "Any", "fdc_id": None, "grams": 10, "protein_added": 5.0, "diaas": None,
              "comp_nutrients": {"protein_g": 100.0, "aa_lysine_g": 5.0}}
        gaps = _usda.get_aa_gaps(base)
        assert len(gaps) > 2, "test scenario needs more gaps than aa_effects_limit to prove anything"

        combo = _complements.two_step_combo(
            gc, base, base_protein=20.0, base_digestible=20.0,
            pantry_candidates=[], diet_pref="all", gaps=gaps, max_improver_grams=120,
            ingredients=None, aa_effects_limit=2,
        )
        assert combo is not None
        assert len(combo["step1"]["aa_effects"]) == 2

    def test_step2_respects_exclude_names(self):
        # step2's internal suggest_complements() call had exclude_names
        # flagged (not yet confirmed) as a possible drop during the last
        # mutation-testing round — same base/gc scenario as the test above,
        # confirmed here: excluding step2's own winning candidate by name
        # must remove it from consideration, not silently ignore the filter.
        base = {
            "protein_g": 20.0,
            "aa_methionine_g": 0.10, "aa_cystine_g": 0.06,
            "aa_lysine_g": 0.30,
        }
        gc = {
            "name": "GapCloser", "fdc_id": None, "grams": 10, "protein_added": 10.0,
            "diaas": 0.5, "predicted_diaas": 0.5,
            "comp_nutrients": {"protein_g": 100.0, "aa_methionine_g": 1.5, "aa_cystine_g": 1.5},
        }
        gaps = _usda.get_aa_gaps(base)
        kwargs = dict(
            base_protein=20.0, base_digestible=20.0,
            pantry_candidates=[], diet_pref="all", gaps=gaps,
            max_improver_grams=300, ingredients=None,
        )

        unfiltered = _complements.two_step_combo(gc, base, **kwargs)
        assert unfiltered["step2"] is not None
        winner_name = unfiltered["step2"]["name"].lower()

        filtered = _complements.two_step_combo(gc, base, exclude_names={winner_name}, **kwargs)
        assert filtered["step2"] is None or filtered["step2"]["name"].lower() != winner_name


# ---------------------------------------------------------------------------
# build_complement_display
# ---------------------------------------------------------------------------

class TestBuildComplementDisplay:
    def test_no_data_without_protein(self):
        result = _complements.build_complement_display({"protein_g": 0}, [])
        assert result == {"no_data": True}

    def test_no_gaps_for_complete_protein(self):
        # SAMPLE_NUTRIENTS is a complete high-quality protein (chicken breast) —
        # no essential AA gaps expected at full digestibility.
        result = _complements.build_complement_display(SAMPLE_NUTRIENTS, [], digestibility=1.0)
        assert result == {"no_gaps": True}

    def test_gap_detected_when_digestibility_reduced(self):
        nutrients = dict(SAMPLE_NUTRIENTS)
        nutrients["aa_lysine_g"] = 0.6  # push lysine down to create a real gap
        result = _complements.build_complement_display(
            nutrients, [], digestibility=0.5, diet_pref="all",
        )
        assert result["no_gaps"] is False
        assert result["gaps"][0]["label"] == "Lysine"

    def test_pantry_suggestions_produce_output_at_reduced_digestibility(self):
        nutrients = dict(SAMPLE_NUTRIENTS)
        nutrients["aa_lysine_g"] = 0.6
        pantry = [{"name": "Soy protein isolate", "nutrients": None, "diaas": 0.97}]
        result = _complements.build_complement_display(
            nutrients, pantry, digestibility=0.88, diet_pref="all",
        )
        assert result["pantry"] or result["general"]

    def test_no_estimate_flag_when_all_suggestions_are_real_or_curated_with_fdc(self):
        # SAMPLE_NUTRIENTS' gap is closed by curated entries that happen to carry
        # a real fdc_id (Tempeh, Egg, Whey, Tofu, Soy protein isolate) — none
        # should be flagged as estimated or generic.
        nutrients = dict(SAMPLE_NUTRIENTS)
        nutrients["aa_lysine_g"] = 0.6
        result = _complements.build_complement_display(nutrients, [], digestibility=0.5, diet_pref="all")
        assert result["has_estimate_or_generic"] is False
        assert result["estimate_note"] is None

    def test_estimate_flag_set_when_pantry_food_is_auto_estimated(self):
        pantry = [{"name": "Nutritional Yeast Flakes", "fdc_id": 42,
                   "nutrients": {"protein_g": 45.0}, "diaas": None}]
        result = _complements.build_complement_display(
            _DEFICIENT_NUTRIENTS, pantry, digestibility=1.0, diet_pref="all",
        )
        assert result["has_estimate_or_generic"] is True
        assert result["estimate_note"] == _complements.ESTIMATE_NOTE
        matches = [s for s in result["pantry"] if s["name"] == "Nutritional Yeast Flakes"]
        assert matches and matches[0]["estimated"] is True
        assert matches[0]["fdc_id"] == 42

    def test_estimate_flag_true_from_estimated_alone_when_nothing_is_generic(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found
        # "row.get('estimated')" survived as "row.get(None)" (always falsy)
        # — the test above didn't catch it because its result happened to
        # ALSO include a generic (no fdc_id) curated entry, so
        # has_estimate_or_generic stayed True by accident via _is_generic()
        # alone. Excluding the curated table's two no-fdc_id entries here
        # isolates the "estimated" check specifically: every remaining
        # suggestion has a real fdc_id, so only "estimated" being read
        # correctly can make this True.
        from tests.conftest import SAMPLE_NUTRIENTS
        nutrients = dict(SAMPLE_NUTRIENTS)
        nutrients["aa_lysine_g"] = 0.6
        pantry = [{"name": "Nutritional Yeast Flakes", "fdc_id": 42,
                   "nutrients": {"protein_g": 45.0}, "diaas": None}]
        result = _complements.build_complement_display(
            nutrients, pantry, digestibility=1.0, diet_pref="all",
            exclude_names={"pea protein powder", "nutritional yeast"},
        )
        all_rows = result["pantry"] + result["general"] + result["diaas_improvers"]
        assert all_rows, "test scenario produced no suggestions to check"
        assert all(row.get("fdc_id") or row.get("recipe_id") for row in all_rows), (
            "test scenario must have zero generic rows for this to isolate anything"
        )
        assert result["has_estimate_or_generic"] is True

    def test_grad_steps_have_real_dcp_via_fallback_when_no_ingredients_given(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found a real,
        # significant bug: _grad_steps()'s "if dcp is None: dcp = _dcp_at_frac(...)"
        # fallback had a survivor that inverted it to "if dcp is not None:". No
        # `ingredients` list is passed here (as in any single-food context —
        # exact_dcp() always returns None immediately without one, per its own
        # "if not ingredients: return None"), so under that inverted condition
        # EVERY graduated dosage step (25/50/75/100%) would silently show
        # dcp=None and pct_increase=None instead of the intended approximation.
        nutrients = {
            "protein_g":          20.0,
            "aa_tryptophan_g":    0.08, "aa_threonine_g":    0.30,
            "aa_isoleucine_g":    0.30, "aa_leucine_g":      0.50,
            "aa_lysine_g":        0.20, "aa_methionine_g":   0.10,
            "aa_phenylalanine_g": 0.30, "aa_valine_g":       0.30,
            "aa_histidine_g":     0.10,
        }
        result = _complements.build_complement_display(nutrients, [], digestibility=1.0)
        # Need a suggestion needing > _GRAD_THRESHOLD (30g) to get any grad_steps at all.
        with_grad_steps = [s for s in result["general"] if s["grad_steps"]]
        assert with_grad_steps, "no suggestion needed enough grams to produce grad_steps"
        # base_digestible = base protein_g * digestibility(1.0) = 20.0 — pinning
        # this also guards against base_nutrients.get("protein_g") silently
        # reading the wrong key (a survived mutant did exactly that), since a
        # wrong/zero base_protein would make base_digestible 0 and this whole
        # formula check fail.
        base_digestible = 20.0
        for s in with_grad_steps:
            for step in s["grad_steps"]:
                assert step["dcp"] is not None
                assert "grams" in step and isinstance(step["grams"], int)
                # pct_increase must be the documented percentage-change formula —
                # a survived mutant swapped the "/" for a "*" here.
                expected_pct = round((step["dcp"] - base_digestible) / base_digestible * 100, 1)
                assert step["pct_increase"] == pytest.approx(expected_pct)

    def test_anchor_overrides_pins_grad_steps_to_a_chosen_serving_size(self):
        # anchor_overrides (the "pin the graduated table to your own serving
        # size" feature) had zero test coverage despite spanning
        # _grad_steps()/build_complement_display() here and several backend
        # route wirings (web/backend.py's _parse_anchor_overrides()).
        nutrients = {
            "protein_g":          20.0,
            "aa_tryptophan_g":    0.08, "aa_threonine_g":    0.30,
            "aa_isoleucine_g":    0.30, "aa_leucine_g":      0.50,
            "aa_lysine_g":        0.20, "aa_methionine_g":   0.10,
            "aa_phenylalanine_g": 0.30, "aa_valine_g":       0.30,
            "aa_histidine_g":     0.10,
        }
        baseline = _complements.build_complement_display(nutrients, [], digestibility=1.0)
        with_grad_steps = [s for s in baseline["general"] if s["grad_steps"]]
        assert with_grad_steps, "no suggestion needed enough grams to produce grad_steps"
        target = with_grad_steps[0]
        name = target["name"]
        full_grams = target["grams"]
        override_grams = 10.0
        assert override_grams != full_grams, "override must differ from the math-derived full amount"

        anchored = _complements.build_complement_display(
            nutrients, [], digestibility=1.0,
            anchor_overrides={name.lower(): override_grams},
        )
        anchored_row = next(s for s in anchored["general"] if s["name"] == name)
        assert anchored_row["anchor_grams"] == override_grams
        # 100% step should now land at the override amount, not full_grams.
        assert anchored_row["grad_steps"][-1]["grams"] == round(override_grams)
        # full_closure_grams surfaces the true math-derived amount only when
        # it differs meaningfully from the override, per _fmt()'s own rule.
        assert anchored_row["full_closure_grams"] == full_grams

        # A suggestion the user didn't anchor is unaffected.
        other_rows = [s for s in anchored["general"] if s["name"] != name]
        if other_rows:
            assert other_rows[0]["anchor_grams"] is None


# ---------------------------------------------------------------------------
# comp_sort / diaas_sort — comp_sort has 4 modes: "dcp" (default), "digestible_protein",
# "gap_effect", "grams". diaas_sort keeps its original 2: "effect" (default), "grams".
# ---------------------------------------------------------------------------

class TestSortModes:
    """These bypass the real AA-gap/DIAAS science (stubbed via monkeypatch) to
    test purely the sort-key logic in build_complement_display() in isolation —
    the science itself is already covered by TestBuildComplementDisplay above."""

    # "Small but weak" closes more AA gaps (3) but adds far less digestible
    # protein (2.0g) than "Big but strong" (1 gap, 15.0g) — this separates
    # "gap_effect" (ranks gap count first) from "dcp"/"digestible_protein"
    # (rank the protein/DCP total first), which is the point of the test data.
    _RAW_PANTRY = [
        {"name": "Small but weak", "fdc_id": 1, "grams": 10, "new_complete": False,
         "gaps_closed": 3, "digestible_protein_added": 2.0, "protein_added": 2.0,
         "new_scores": {}, "comp_nutrients": None, "estimated": False,
         "serving_weight_g": None, "recipe_id": None},
        {"name": "Big but strong", "fdc_id": 2, "grams": 80, "new_complete": False,
         "gaps_closed": 1, "digestible_protein_added": 15.0, "protein_added": 15.0,
         "new_scores": {}, "comp_nutrients": None, "estimated": False,
         "serving_weight_g": None, "recipe_id": None},
    ]

    _RAW_IMPROVERS = [
        {"name": "Small effect", "fdc_id": 3, "grams": 15, "new_diaas": 0.80,
         "current_diaas": 0.70, "protein_added": 3.0, "digestible_protein_added": 2.4,
         "diaas": 0.85, "estimated": False, "steps": [],
         "recipe_id": None, "serving_weight_g": None},
        {"name": "Big effect", "fdc_id": 4, "grams": 100, "new_diaas": 0.95,
         "current_diaas": 0.70, "protein_added": 20.0, "digestible_protein_added": 17.0,
         "diaas": 0.90, "estimated": False, "steps": [],
         "recipe_id": None, "serving_weight_g": None},
    ]

    def _stub(self, monkeypatch, pantry=None, improvers=None, pairs=None):
        monkeypatch.setattr(_complements._usda, "get_aa_gaps",
                             lambda *a, **kw: [("aa_lysine_g", 0.5, 2.0)])
        monkeypatch.setattr(_complements._usda, "suggest_complements",
                             lambda *a, **kw: {"pantry": pantry or [], "general": [],
                                                "pairs": pairs or [], "diaas_improvers": improvers or []})

    def test_comp_sort_dcp_ranks_by_greatest_resulting_dcp(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="dcp")
        assert [s["name"] for s in result["pantry"]] == ["Big but strong", "Small but weak"]
        assert "dcp achieved" in result["comp_ranking_note"].lower()

    def test_comp_sort_digestible_protein_ranks_by_most_digestible_protein_added(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="digestible_protein")
        assert [s["name"] for s in result["pantry"]] == ["Big but strong", "Small but weak"]
        assert "digestible protein added" in result["comp_ranking_note"].lower()

    def test_comp_sort_gap_effect_ranks_by_gaps_closed(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="gap_effect")
        assert [s["name"] for s in result["pantry"]] == ["Small but weak", "Big but strong"]
        assert "amino acid gap" in result["comp_ranking_note"].lower()

    def test_comp_sort_gap_effect_reorders_even_when_input_order_is_reversed(self, monkeypatch):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found the test
        # above didn't actually prove the sort worked: it changed
        # "-(gaps_closed or 0)" to "-(gaps_closed and 0)", which evaluates to
        # 0 for BOTH entries here (both have nonzero gaps_closed) — neutering
        # the sort key entirely. Python's stable sort then just left the
        # input list's own order untouched, which happened to already match
        # the expected output, silently passing. Feeding the SAME two
        # candidates in the opposite starting order forces the sort to
        # actually prove itself — a broken sort key would now produce the
        # wrong order instead of accidentally the right one.
        reversed_pantry = list(reversed(self._RAW_PANTRY))
        self._stub(monkeypatch, pantry=reversed_pantry)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="gap_effect")
        assert [s["name"] for s in result["pantry"]] == ["Small but weak", "Big but strong"]

    def test_comp_sort_grams_ranks_by_smallest_serving(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="grams")
        assert [s["name"] for s in result["pantry"]] == ["Small but weak", "Big but strong"]
        assert "smallest addition" in result["comp_ranking_note"].lower()

    def test_comp_sort_grams_reorders_even_when_input_order_is_reversed(self, monkeypatch):
        # Same sneaky pattern as the gap_effect test above: a survivor
        # renamed "grams" to "GRAMS" in this sort key, making every row
        # fall back to the same "999" default and tie — Python's stable
        # sort then just kept _RAW_PANTRY's own list order, which happened
        # to already match the correct grams-ascending order.
        self._stub(monkeypatch, pantry=list(reversed(self._RAW_PANTRY)))
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="grams")
        assert [s["name"] for s in result["pantry"]] == ["Small but weak", "Big but strong"]

    def test_comp_sort_default_is_dcp(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [])
        assert [s["name"] for s in result["pantry"]] == ["Big but strong", "Small but weak"]

    def test_new_complete_always_promoted_to_top_regardless_of_sort_mode(self, monkeypatch):
        # Documented in build_complement_display()'s own docstring ("A full
        # profile-completer is always promoted to the top of its tier
        # regardless of mode") but never actually tested by any sort-mode
        # test above — all of them only ever compare two new_complete=False
        # candidates. Here "CompleteButBig" is worse by EVERY other metric
        # (needs far more grams, closes fewer gaps, adds less digestible
        # protein) than "IncompleteButSmall", yet must still sort first in
        # all four comp_sort modes purely because it completes the profile.
        complete_but_big = {
            "name": "CompleteButBig", "fdc_id": 1, "grams": 100, "new_complete": True,
            "gaps_closed": 1, "digestible_protein_added": 1.0, "protein_added": 1.0,
            "new_scores": {}, "comp_nutrients": None, "estimated": False,
            "serving_weight_g": None, "recipe_id": None,
        }
        incomplete_but_small = {
            "name": "IncompleteButSmall", "fdc_id": 2, "grams": 5, "new_complete": False,
            "gaps_closed": 3, "digestible_protein_added": 10.0, "protein_added": 10.0,
            "new_scores": {}, "comp_nutrients": None, "estimated": False,
            "serving_weight_g": None, "recipe_id": None,
        }
        self._stub(monkeypatch, pantry=[incomplete_but_small, complete_but_big])
        for mode in ("grams", "digestible_protein", "gap_effect", "dcp"):
            result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort=mode)
            assert result["pantry"][0]["name"] == "CompleteButBig", (
                f"comp_sort={mode!r}: new_complete promotion not honored, "
                f"got order {[s['name'] for s in result['pantry']]}"
            )

    def test_diaas_sort_effect_ranks_by_highest_resulting_diaas(self, monkeypatch):
        self._stub(monkeypatch, improvers=self._RAW_IMPROVERS)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], diaas_sort="effect")
        assert [s["name"] for s in result["diaas_improvers"]] == ["Big effect", "Small effect"]
        assert "greatest effect" in result["diaas_ranking_note"].lower()

    def test_diaas_sort_grams_ranks_by_smallest_serving(self, monkeypatch):
        self._stub(monkeypatch, improvers=self._RAW_IMPROVERS)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], diaas_sort="grams")
        assert [s["name"] for s in result["diaas_improvers"]] == ["Small effect", "Big effect"]
        assert "smallest addition" in result["diaas_ranking_note"].lower()

    def test_diaas_sort_grams_reorders_even_when_input_order_is_reversed(self, monkeypatch):
        # Same coincidental-order risk as the comp_sort tests above — this
        # test's expected order happens to match _RAW_IMPROVERS' own given
        # order, so a broken sort key could pass by accident. Reversing the
        # input forces the sort to actually prove itself.
        self._stub(monkeypatch, improvers=list(reversed(self._RAW_IMPROVERS)))
        result = _complements.build_complement_display({"protein_g": 20.0}, [], diaas_sort="grams")
        assert [s["name"] for s in result["diaas_improvers"]] == ["Small effect", "Big effect"]

    def test_pair_total_dig_complete_scale_formula(self, monkeypatch):
        # The "pairs" tier's _fmt_pair() had NO test at all before a
        # mutation-testing pass (TESTING-ROADMAP.md item #5) found it — a
        # survivor swapped a "*" for a "/" in its total_dig_complete
        # fallback formula (used whenever exact_dcp() has no `ingredients`
        # to recompute from, the same "no ingredients" case exercised
        # throughout this file). scale < 1.0 here specifically, so multiply
        # and divide give very different numbers.
        pair = {
            "foods": [
                {"name": "A", "fdc_id": 1, "grams": 20, "comp_nutrients": None,
                 "diaas": 0.654, "protein_added": 3.0, "dig_added": 2.5},
                {"name": "B", "fdc_id": 2, "grams": 30, "comp_nutrients": None,
                 "diaas": None, "protein_added": 2.0, "dig_added": 1.5},
            ],
            "total_grams": 50, "gaps_closed": True, "new_complete": False,
            "total_protein_added": 5.0, "total_dig_added": 4.0,
            "new_scores": {"aa_lysine_g": 0.3},
        }
        self._stub(monkeypatch, pairs=[pair])
        result = _complements.build_complement_display({"protein_g": 20.0}, [])
        # base_digestible = 20.0 (protein_g * digestibility 1.0);
        # old_adj_min = gaps[0][1] = 0.5 (stubbed); new_adj_min = 0.3
        # scale = 0.3/0.5 = 0.6; total_raw = 20.0 + 5.0 = 25.0
        # total_dig_complete = round(25.0 * 0.6, 1) = 15.0 -- NOT 41.7,
        # which is what round(25.0 / 0.6, 1) (the mutant) would give.
        fmt_pair = result["pairs"][0]
        assert fmt_pair["total_dig_complete"] == pytest.approx(15.0)
        assert fmt_pair["total_grams"] == 50
        assert fmt_pair["gaps_closed"] is True
        assert fmt_pair["new_complete"] is False
        assert fmt_pair["total_protein_added"] == pytest.approx(5.0)
        assert fmt_pair["total_dig_added"] == pytest.approx(4.0)
        food_a, food_b = fmt_pair["foods"]
        assert food_a["name"] == "A"
        assert food_a["fdc_id"] == 1
        assert food_a["diaas"] == pytest.approx(0.65)  # round(0.654, 2)
        assert food_a["protein_added"] == pytest.approx(3.0)
        assert food_a["dig_added"] == pytest.approx(2.5)
        assert food_b["diaas"] is None  # falsy source value -> None, not round(None)

    def test_pair_total_dig_complete_uses_real_exact_dcp_when_ingredients_provided(self, monkeypatch):
        # Same gap as the other "ingredients provided" tests in this class,
        # for _fmt_pair()'s own exact_dcp() call — every existing pairs
        # test used ingredients=None, only ever exercising the fallback
        # scale formula, never a real two-food per-ingredient recompute.
        cheese = {"protein_g": 20.0, "aa_lysine_g": 1.5}
        ingredients = [{"food_name": "Oats", "nutrients_100g": _OATS_100G, "grams": 100.0}]
        pair = {
            "foods": [
                {"name": "Peanut butter", "fdc_id": 1, "grams": 20, "comp_nutrients": _PEANUT_BUTTER_100G,
                 "diaas": 0.85, "protein_added": 5.0, "dig_added": 4.0},
                {"name": "Cheese", "fdc_id": 2, "grams": 15, "comp_nutrients": cheese,
                 "diaas": 0.9, "protein_added": 3.0, "dig_added": 2.5},
            ],
            "total_grams": 35, "gaps_closed": True, "new_complete": False,
            "total_protein_added": 8.0, "total_dig_added": 6.5,
            "new_scores": {"aa_lysine_g": 0.3},
        }
        self._stub(monkeypatch, pairs=[pair])
        result = _complements.build_complement_display({"protein_g": 13.0}, [], ingredients=ingredients)
        total_dig_complete = result["pairs"][0]["total_dig_complete"]

        expected = _complements.exact_dcp(
            ingredients, [("Peanut butter", _PEANUT_BUTTER_100G, 20), ("Cheese", cheese, 15)]
        )
        assert expected is not None
        assert total_dig_complete == pytest.approx(expected)

    def test_fmt_gap_closer_all_fields_match_hand_calculation(self, monkeypatch):
        # _fmt() (the pantry/general gap-closer formatter) never had a test
        # checking more than one or two of its ~14 output fields at once —
        # this pins every field against a hand-computed expected value from
        # one fully-controlled input dict.
        s = {
            "name": "TestFood", "fdc_id": 99, "recipe_id": None, "serving_weight_g": 15.0,
            "grams": 20, "diaas": 0.876, "new_complete": True,
            "digestible_protein_added": 3.456, "protein_added": 4.567,
            "opens_new_gap": True, "estimated": True,
            "new_scores": {}, "comp_nutrients": None,
        }
        self._stub(monkeypatch, pantry=[s])
        result = _complements.build_complement_display({"protein_g": 20.0}, [])
        fmt = result["pantry"][0]

        assert fmt["name"] == "TestFood"
        assert fmt["fdc_id"] == 99
        assert fmt["recipe_id"] is None
        assert fmt["serving_weight_g"] == pytest.approx(15.0)
        assert fmt["grams"] == 20
        assert fmt["amount_note"] == _amount_note(20, "TestFood", fdc_id=99)
        assert fmt["grad_steps"] == []  # grams(20) <= _GRAD_THRESHOLD(30)
        assert fmt["diaas"] == pytest.approx(0.88)  # round(0.876, 2)
        assert fmt["new_complete"] is True
        assert fmt["dig_protein_added"] == pytest.approx(3.5)   # round(3.456, 1)
        assert fmt["protein_added"] == pytest.approx(4.6)       # round(4.567, 1)
        assert fmt["opens_new_gap"] is True
        assert fmt["estimated"] is True
        # new_scores={} (falsy) -> _total_dig() falls to the
        # base_digestible + dig branch: round(20.0 + 3.456, 1) = 23.5
        assert fmt["total_dig"] == pytest.approx(23.5)
        # new_scores={} -> aa_effects() falls back to gaps' own orig_score
        # (stubbed gaps = [("aa_lysine_g", 0.5, 2.0)]).
        assert fmt["aa_effects"] == [
            {"label": "Lysine", "before": 0.5, "after": 0.5, "met": False}
        ]

    def test_total_dig_scale_formula_branch(self, monkeypatch):
        # The test above only exercises _total_dig()'s "else" branch
        # (new_scores={} falsy -> base_digestible + dig). Its OTHER branch
        # — the "new_scores and gaps" scale formula, used whenever a
        # suggestion's predicted new_scores are available — had no
        # exact-value test of its own.
        s = {
            "name": "ScaleTest", "fdc_id": 1, "recipe_id": None, "serving_weight_g": None,
            "grams": 20, "diaas": None, "new_complete": False,
            "digestible_protein_added": 8.0, "protein_added": 10.0,
            "opens_new_gap": False, "estimated": False,
            "new_scores": {"aa_lysine_g": 0.4}, "comp_nutrients": None,
        }
        self._stub(monkeypatch, pantry=[s])
        result = _complements.build_complement_display({"protein_g": 20.0}, [])
        # gaps=[("aa_lysine_g", 0.5, 2.0)] (stubbed) -> old_adj_min=0.5
        # new_adj_min = min(0.4) * digestibility(1.0) = 0.4
        # scale = 0.4 / 0.5 = 0.8 -> min(1.0, 0.8) = 0.8
        # total_dig = round((20.0 + 10.0) * 0.8, 1) = 24.0
        assert result["pantry"][0]["total_dig"] == pytest.approx(24.0)

    def test_dcp_at_frac_weighted_pool_formula_across_all_grad_steps(self, monkeypatch):
        # _dcp_at_frac() (the weighted-pool IAA formula behind _grad_steps()'s
        # dcp fallback) was only ever exercised indirectly (via
        # test_grad_steps_have_real_dcp_via_fallback_when_no_ingredients_given,
        # which only checks pct_increase's formula, not _dcp_at_frac's own
        # per-AA weighted math). Hand-computed here for all four grad steps.
        s = {
            "name": "BigFood", "fdc_id": 7, "recipe_id": None, "serving_weight_g": None,
            "grams": 40, "diaas": None, "new_complete": False,
            "digestible_protein_added": 18.0, "protein_added": 20.0,
            "opens_new_gap": False, "estimated": False,
            "new_scores": {"aa_lysine_g": 0.9}, "comp_nutrients": None,
        }
        self._stub(monkeypatch, pantry=[s])
        result = _complements.build_complement_display({"protein_g": 20.0}, [])
        steps = result["pantry"][0]["grad_steps"]
        assert len(steps) == 4

        # base_protein=20.0, raw_full=protein_added=20.0, digestibility=1.0
        # gaps=[("aa_lysine_g", base_score_i=0.5, ...)], new_scores_full={"aa_lysine_g": 0.9}
        # new_adj = 0.9 * 1.0 = 0.9
        # comp_aa = 0.9*(20+20) - 0.5*20 = 36 - 10 = 26
        for frac, step in zip((0.25, 0.50, 0.75, 1.0), steps):
            total_p = 20.0 + frac * 20.0
            score_at_f = (0.5 * 20.0 + frac * 26.0) / total_p
            expected_dcp = round(total_p * min(1.0, score_at_f), 1)
            assert step["dcp"] == pytest.approx(expected_dcp)
            assert step["dig_protein"] == pytest.approx(round(18.0 * frac, 1))

    def test_total_dig_uses_real_exact_dcp_when_ingredients_provided(self, monkeypatch):
        # A gap named in TESTING-ROADMAP.md item #5: every other test in
        # this file passes ingredients=None, so exact_dcp() always
        # short-circuits to None and every "total_dig"/"dcp" value comes
        # from a fallback approximation — the real per-ingredient recompute
        # path (the actual reason exact_dcp() exists) was never exercised.
        # This test provides a real `ingredients` list (a meal/recipe
        # context) and confirms the resulting total_dig (a) matches an
        # independent direct exact_dcp() call using the same data, and (b)
        # is NOT what the fallback formula would have given — proving the
        # real path actually ran instead of silently falling back.
        ingredients = [{"food_name": "Oats", "nutrients_100g": _OATS_100G, "grams": 100.0}]
        s = {
            "name": "Peanut butter", "fdc_id": 55, "recipe_id": None, "serving_weight_g": None,
            "grams": 30, "diaas": 0.85, "new_complete": False,
            "digestible_protein_added": 6.0, "protein_added": 7.5,
            "opens_new_gap": False, "estimated": False,
            "new_scores": {}, "comp_nutrients": _PEANUT_BUTTER_100G,
        }
        self._stub(monkeypatch, pantry=[s])
        result = _complements.build_complement_display({"protein_g": 13.0}, [], ingredients=ingredients)
        total_dig = result["pantry"][0]["total_dig"]

        expected = _complements.exact_dcp(
            ingredients, [("Peanut butter", _PEANUT_BUTTER_100G, 30)]
        )
        assert expected is not None, "exact_dcp() should produce a real value with real ingredients"
        assert total_dig == pytest.approx(expected)

        # The fallback formula (new_scores={} -> base_digestible + dig) would
        # give round(13.0 + 6.0, 1) = 19.0 -- confirm the real value differs,
        # so this isn't accidentally passing via the fallback path instead.
        fallback_value = round(13.0 + 6.0, 1)
        assert total_dig != pytest.approx(fallback_value)

    def test_grad_steps_use_real_exact_dcp_when_ingredients_provided(self, monkeypatch):
        # Same gap as the test above, but for _grad_steps()'s own per-step
        # exact_dcp() call (each of the 25/50/75/100% dosage previews) —
        # every existing grad_steps test used ingredients=None, only ever
        # exercising the _dcp_at_frac() approximation, never this.
        ingredients = [{"food_name": "Oats", "nutrients_100g": _OATS_100G, "grams": 100.0}]
        s = {
            "name": "Peanut butter", "fdc_id": 55, "recipe_id": None, "serving_weight_g": None,
            "grams": 60, "diaas": 0.85, "new_complete": False,
            "digestible_protein_added": 12.0, "protein_added": 15.0,
            "opens_new_gap": False, "estimated": False,
            "new_scores": {"aa_lysine_g": 0.9}, "comp_nutrients": _PEANUT_BUTTER_100G,
        }
        self._stub(monkeypatch, pantry=[s])
        result = _complements.build_complement_display({"protein_g": 13.0}, [], ingredients=ingredients)
        steps = result["pantry"][0]["grad_steps"]
        assert len(steps) == 4

        for step in steps:
            expected = _complements.exact_dcp(
                ingredients, [("Peanut butter", _PEANUT_BUTTER_100G, step["grams"])]
            )
            assert expected is not None
            assert step["dcp"] == pytest.approx(expected)

    def test_fmt_improver_all_fields_match_hand_calculation(self, monkeypatch):
        # _fmt_improver() (the DIAAS-improver tier formatter) — same gap as
        # _fmt() above, no test checking more than one or two fields.
        s = {
            "name": "ImproverFood", "fdc_id": 55, "recipe_id": None, "serving_weight_g": None,
            "grams": 40, "diaas": 0.91, "current_diaas": 0.7, "new_diaas": 0.85,
            "protein_added": 6.789, "digestible_protein_added": 5.432, "estimated": False,
            "comp_nutrients": None,
            "steps": [{"grams": 40, "new_diaas": 0.85, "dcp": 99.9}],
        }
        self._stub(monkeypatch, improvers=[s])
        result = _complements.build_complement_display({"protein_g": 20.0}, [])
        fmt = result["diaas_improvers"][0]

        assert fmt["name"] == "ImproverFood"
        assert fmt["fdc_id"] == 55
        assert fmt["recipe_id"] is None
        assert fmt["grams"] == 40
        assert fmt["amount_note"] == _amount_note(40, "ImproverFood", fdc_id=55)
        assert fmt["diaas"] == pytest.approx(0.91)
        assert fmt["current_diaas"] == pytest.approx(0.7)
        assert fmt["new_diaas"] == pytest.approx(0.85)
        assert fmt["dig_protein_added"] == pytest.approx(5.4)   # round(5.432, 1)
        assert fmt["protein_added"] == pytest.approx(6.8)       # round(6.789, 1)
        assert fmt["estimated"] is False
        # ingredients=None -> exact_dcp() always None -> fallback formula:
        # new_diaas truthy -> round((20.0 + 6.789) * min(1.0, 0.85), 1) = 22.8
        assert fmt["total_dig"] == pytest.approx(22.8)
        # step_dcp falls back to step["dcp"]=99.9 (exact_dcp also None here):
        # pct_increase = round((99.9 - 20.0) / 20.0 * 100, 1) = 399.5
        assert len(fmt["steps"]) == 1
        assert fmt["steps"][0]["dcp"] == pytest.approx(99.9)
        assert fmt["steps"][0]["pct_increase"] == pytest.approx(399.5)
        assert fmt["steps"][0]["amount_note"] == _amount_note(40, "ImproverFood", fdc_id=55)

    def test_top_level_summary_fields_match_hand_calculation(self, monkeypatch):
        # The top-level echo/summary fields (gap_rows' "score", the
        # exhausted_msg text, pantry_empty/pantry_no_qualify/
        # have_gap_closers) had no test pinning their actual values.
        s = {
            "name": "TestFood", "fdc_id": 99, "recipe_id": None, "serving_weight_g": None,
            "grams": 20, "diaas": 0.9, "new_complete": True, "digestible_protein_added": 3.0,
            "protein_added": 4.0, "opens_new_gap": False, "estimated": False,
            "new_scores": {}, "comp_nutrients": None,
        }
        monkeypatch.setattr(_complements._usda, "get_aa_gaps",
                             lambda *a, **kw: [("aa_lysine_g", 0.5321, 2.0)])
        monkeypatch.setattr(_complements._usda, "suggest_complements",
                             lambda *a, **kw: {"pantry": [s], "general": [],
                                                "pairs": [], "diaas_improvers": []})

        result = _complements.build_complement_display(
            {"protein_g": 20.0}, [{"name": "x"}], comp_sort="grams", diaas_sort="grams",
        )
        assert result["gaps"] == [{"label": "Lysine", "score": pytest.approx(0.532)}]
        assert result["comp_sort"] == "grams"
        assert result["diaas_sort"] == "grams"
        assert result["pantry_empty"] is False
        assert result["pantry_no_qualify"] is False
        assert result["have_gap_closers"] is True
        assert "Lysine/protein ratio" in result["exhausted_msg"]
        assert "grains (rice, wheat, corn, oats)" in result["exhausted_msg"]


# ---------------------------------------------------------------------------
# load_cache_candidates
# ---------------------------------------------------------------------------

class TestLoadCacheCandidates:
    def _insert_food(self, db_conn: sqlite3.Connection, fdc_id: int, name: str,
                      nutrients: dict | None) -> None:
        db_conn.execute("""
            INSERT OR REPLACE INTO foods
                (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (fdc_id, name, "Branded", None, None, None,
              json.dumps(nutrients) if nutrients is not None else None, json.dumps([])))
        db_conn.commit()

    def test_finds_real_food_matching_curated_entry_by_name(self, db_conn):
        self._insert_food(db_conn, 500, "Nutritional Yeast Flakes", {"protein_g": 45.0})
        candidates = _complements.load_cache_candidates()
        names = [c["name"] for c in candidates]
        assert "Nutritional Yeast Flakes" in names
        match = next(c for c in candidates if c["name"] == "Nutritional Yeast Flakes")
        assert match["fdc_id"] == 500
        assert match["nutrients"] == {"protein_g": 45.0}
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found nothing
        # checked "diaas"'s key or value — survivors renamed the key and
        # separately looked up the wrong row's name for it.
        assert match["diaas"] == _usda.get_diaas("Nutritional Yeast Flakes")

    def test_excludes_curated_names_already_covered_elsewhere(self, db_conn):
        # exclude_names_lower is checked against the curated table's own entry
        # name (e.g. a pantry item literally named "Nutritional yeast"), not
        # against whatever real product name the cache search would find —
        # this skips searching that curated slot at all.
        self._insert_food(db_conn, 500, "Nutritional Yeast Flakes", {"protein_g": 45.0})
        candidates = _complements.load_cache_candidates({"nutritional yeast"})
        assert not any(c["name"] == "Nutritional Yeast Flakes" for c in candidates)

    def test_excluded_name_does_not_stop_the_whole_search(self, db_conn):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found the
        # "if excluded: continue" in the curated-table loop had a survivor
        # changing it to "break" — which would silently stop searching the
        # REST of the curated table entirely after the first excluded name,
        # not just skip that one entry. The previous test alone couldn't
        # catch this: it only ever inserted one matching food, so even a
        # fully-broken loop would still "pass" (nothing else to find).
        # "Soy protein isolate" is the curated entry right after
        # "Nutritional yeast" in complement_table_names()'s own order.
        self._insert_food(db_conn, 500, "Nutritional Yeast Flakes", {"protein_g": 45.0})
        self._insert_food(db_conn, 501, "Soy Protein Isolate Powder", {"protein_g": 90.0})
        candidates = _complements.load_cache_candidates({"nutritional yeast"})
        names = [c["name"] for c in candidates]
        assert "Nutritional Yeast Flakes" not in names
        assert "Soy Protein Isolate Powder" in names

    def test_no_match_returns_nothing_for_that_food(self, db_conn):
        self._insert_food(db_conn, 501, "Frozen Pizza Rolls", {"protein_g": 8.0})
        candidates = _complements.load_cache_candidates()
        assert not any(c["name"] == "Frozen Pizza Rolls" for c in candidates)

    def test_empty_cache_returns_empty_list(self):
        assert _complements.load_cache_candidates() == []
