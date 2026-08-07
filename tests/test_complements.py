"""
Tests for numa_app/services/complements.py — the complement-suggestion
display math used by the web backend (web/backend.py).
"""
import json
import sqlite3

import pytest

from numa_app.services import complements as _complements
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


# ---------------------------------------------------------------------------
# comp_sort / diaas_sort — "greatest effect" (default) vs "smallest addition"
# ---------------------------------------------------------------------------

class TestSortModes:
    """These bypass the real AA-gap/DIAAS science (stubbed via monkeypatch) to
    test purely the sort-key logic in build_complement_display() in isolation —
    the science itself is already covered by TestBuildComplementDisplay above."""

    _RAW_PANTRY = [
        {"name": "Small but weak", "fdc_id": 1, "grams": 10, "new_complete": False,
         "gaps_closed": 1, "digestible_protein_added": 2.0, "protein_added": 2.0,
         "new_scores": {}, "comp_nutrients": None, "estimated": False,
         "serving_weight_g": None, "recipe_id": None},
        {"name": "Big but strong", "fdc_id": 2, "grams": 80, "new_complete": False,
         "gaps_closed": 3, "digestible_protein_added": 15.0, "protein_added": 15.0,
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

    def _stub(self, monkeypatch, pantry=None, improvers=None):
        monkeypatch.setattr(_complements._usda, "get_aa_gaps",
                             lambda *a, **kw: [("aa_lysine_g", 0.5, 2.0)])
        monkeypatch.setattr(_complements._usda, "suggest_complements",
                             lambda *a, **kw: {"pantry": pantry or [], "general": [],
                                                "pairs": [], "diaas_improvers": improvers or []})

    def test_comp_sort_effect_ranks_by_gaps_closed_then_dcp_added(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="effect")
        assert [s["name"] for s in result["pantry"]] == ["Big but strong", "Small but weak"]
        assert "greatest effect" in result["comp_ranking_note"].lower()

    def test_comp_sort_grams_ranks_by_smallest_serving(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [], comp_sort="grams")
        assert [s["name"] for s in result["pantry"]] == ["Small but weak", "Big but strong"]
        assert "smallest addition" in result["comp_ranking_note"].lower()

    def test_comp_sort_default_is_effect(self, monkeypatch):
        self._stub(monkeypatch, pantry=self._RAW_PANTRY)
        result = _complements.build_complement_display({"protein_g": 20.0}, [])
        assert [s["name"] for s in result["pantry"]] == ["Big but strong", "Small but weak"]

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

    def test_excludes_curated_names_already_covered_elsewhere(self, db_conn):
        # exclude_names_lower is checked against the curated table's own entry
        # name (e.g. a pantry item literally named "Nutritional yeast"), not
        # against whatever real product name the cache search would find —
        # this skips searching that curated slot at all.
        self._insert_food(db_conn, 500, "Nutritional Yeast Flakes", {"protein_g": 45.0})
        candidates = _complements.load_cache_candidates({"nutritional yeast"})
        assert not any(c["name"] == "Nutritional Yeast Flakes" for c in candidates)

    def test_no_match_returns_nothing_for_that_food(self, db_conn):
        self._insert_food(db_conn, 501, "Frozen Pizza Rolls", {"protein_g": 8.0})
        candidates = _complements.load_cache_candidates()
        assert not any(c["name"] == "Frozen Pizza Rolls" for c in candidates)

    def test_empty_cache_returns_empty_list(self):
        assert _complements.load_cache_candidates() == []
