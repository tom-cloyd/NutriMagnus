"""
Tests for numa_app/services/complements.py — the shared complement-suggestion
display math used by both the CLI (render.py) and web (backend.py).
"""
import pytest

from numa_app.services import complements as _complements
from tests.conftest import SAMPLE_NUTRIENTS


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
