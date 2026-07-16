"""
Tests for usda.py — pure functions only, no network calls.

scale_nutrients, sum_nutrients, _parse_food, protein_completeness,
and nutrient_label are all deterministic and need no mocking.
"""

import pytest

import usda as _usda
from tests.conftest import SAMPLE_NUTRIENTS, SAMPLE_NUTRIENTS_2


# ---------------------------------------------------------------------------
# scale_nutrients
# ---------------------------------------------------------------------------

class TestScaleNutrients:
    def test_scale_double(self):
        result = _usda.scale_nutrients({"calories": 100.0, "protein_g": 20.0}, 200.0)
        assert result["calories"] == pytest.approx(200.0)
        assert result["protein_g"] == pytest.approx(40.0)

    def test_scale_half(self):
        result = _usda.scale_nutrients({"calories": 200.0}, 50.0)
        assert result["calories"] == pytest.approx(100.0)

    def test_scale_same_size_returns_same(self):
        result = _usda.scale_nutrients({"calories": 165.0}, 100.0)
        assert result["calories"] == pytest.approx(165.0)

    def test_scale_custom_base_size(self):
        # base_size of 150g: 30 calories per 150g → 20 calories per 100g
        result = _usda.scale_nutrients({"calories": 30.0}, 100.0, base_size=150.0)
        assert result["calories"] == pytest.approx(20.0)

    def test_all_keys_scaled(self):
        nutrients = {"calories": 100.0, "protein_g": 10.0, "fat_g": 5.0}
        result = _usda.scale_nutrients(nutrients, 50.0)
        assert set(result.keys()) == set(nutrients.keys())

    def test_zero_amount_returns_zeros(self):
        result = _usda.scale_nutrients({"calories": 100.0}, 0.0)
        assert result["calories"] == 0.0


# ---------------------------------------------------------------------------
# sum_nutrients
# ---------------------------------------------------------------------------

class TestSumNutrients:
    def test_sum_two_dicts(self):
        a = {"calories": 100.0, "protein_g": 10.0}
        b = {"calories": 200.0, "protein_g":  5.0}
        result = _usda.sum_nutrients(a, b)
        assert result["calories"] == pytest.approx(300.0)
        assert result["protein_g"] == pytest.approx(15.0)

    def test_sum_disjoint_keys(self):
        a = {"calories": 100.0}
        b = {"protein_g": 5.0}
        result = _usda.sum_nutrients(a, b)
        assert result["calories"] == pytest.approx(100.0)
        assert result["protein_g"] == pytest.approx(5.0)

    def test_sum_three_dicts(self):
        n = {"calories": 50.0}
        result = _usda.sum_nutrients(n, n, n)
        assert result["calories"] == pytest.approx(150.0)

    def test_sum_empty_dict(self):
        a = {"calories": 100.0}
        result = _usda.sum_nutrients(a, {})
        assert result["calories"] == pytest.approx(100.0)

    def test_sum_no_args_returns_empty(self):
        result = _usda.sum_nutrients()
        assert result == {}

    def test_original_dicts_not_mutated(self):
        a = {"calories": 100.0}
        b = {"calories": 200.0}
        _usda.sum_nutrients(a, b)
        assert a["calories"] == 100.0
        assert b["calories"] == 200.0


# ---------------------------------------------------------------------------
# _parse_food
# ---------------------------------------------------------------------------

class TestParseFood:
    def _make_usda_response(self, nutrients: list[dict]) -> dict:
        return {
            "fdcId": 12345,
            "description": "Test Food",
            "dataType": "SR Legacy",
            "brandOwner": None,
            "servingSize": 100.0,
            "servingSizeUnit": "g",
            "householdServingFullText": "1 cup",
            "foodNutrients": nutrients,
        }

    def test_parses_basic_macros(self):
        response = self._make_usda_response([
            {"nutrientId": 1008, "value": 165.0},   # calories
            {"nutrientId": 1003, "value":  31.0},   # protein
            {"nutrientId": 1004, "value":   3.6},   # fat
        ])
        result = _usda._parse_food(response)
        assert result["nutrients"]["calories"] == pytest.approx(165.0)
        assert result["nutrients"]["protein_g"] == pytest.approx(31.0)
        assert result["nutrients"]["fat_g"] == pytest.approx(3.6)

    def test_ignores_unknown_nutrient_ids(self):
        response = self._make_usda_response([
            {"nutrientId": 1008, "value": 100.0},
            {"nutrientId": 9999, "value": 999.0},   # unknown ID
        ])
        result = _usda._parse_food(response)
        assert len(result["nutrients"]) == 1
        assert "calories" in result["nutrients"]

    def test_parses_metadata(self):
        response = self._make_usda_response([])
        result = _usda._parse_food(response)
        assert result["fdcId"] == 12345
        assert result["name"] == "Test Food"
        assert result["dataType"] == "SR Legacy"
        assert result["servingSize"] == 100.0
        assert result["householdServing"] == "1 cup"
        assert "portions" in result

    def test_parses_food_portions(self):
        response = self._make_usda_response([])
        response["foodPortions"] = [
            {"portionDescription": "1 cup", "gramWeight": 240.0},
            {"portionDescription": "1 tbsp", "gramWeight": 15.0},
            {"portionDescription": "", "gramWeight": 50.0},   # blank desc — should be skipped
            {"modifier": "1 oz", "gramWeight": 28.0},         # uses modifier fallback
        ]
        result = _usda._parse_food(response)
        assert len(result["portions"]) == 3
        assert result["portions"][0] == {"description": "1 cup",  "gram_weight": 240.0}
        assert result["portions"][1] == {"description": "1 tbsp", "gram_weight": 15.0}
        assert result["portions"][2] == {"description": "1 oz",   "gram_weight": 28.0}

    def test_parses_food_portions_empty_when_absent(self):
        response = self._make_usda_response([])
        # Remove household serving so the synthesis fallback doesn't fire
        response["householdServingFullText"] = None
        result = _usda._parse_food(response)
        assert result["portions"] == []

    def test_handles_nested_nutrient_format(self):
        """Detailed endpoint wraps the ID inside a 'nutrient' object."""
        response = self._make_usda_response([
            {"nutrient": {"id": 1008}, "amount": 200.0}
        ])
        result = _usda._parse_food(response)
        assert result["nutrients"]["calories"] == pytest.approx(200.0)

    def test_handles_string_number_format(self):
        """Abridged endpoint uses 'number' as a string for the nutrient ID."""
        response = self._make_usda_response([
            {"number": "1008", "value": 300.0}
        ])
        result = _usda._parse_food(response)
        assert result["nutrients"]["calories"] == pytest.approx(300.0)

    def test_missing_value_skipped(self):
        response = self._make_usda_response([
            {"nutrientId": 1008, "value": None},
        ])
        result = _usda._parse_food(response)
        assert "calories" not in result["nutrients"]


# ---------------------------------------------------------------------------
# protein_completeness
# ---------------------------------------------------------------------------

class TestProteinCompleteness:
    def test_complete_protein(self):
        """Chicken breast has all essential AAs above reference levels."""
        result = _usda.protein_completeness(SAMPLE_NUTRIENTS)
        assert result["has_data"] is True
        assert result["complete"] is True
        assert result["limiting_aa"] is not None   # still identifies the minimum
        assert all(v > 0 for v in result["scores"].values())

    def test_incomplete_protein(self):
        """Strip out most AAs to simulate an incomplete protein source."""
        nutrients = {
            "protein_g": 10.0,
            "aa_tryptophan_g": 0.001,    # far below reference
            "aa_threonine_g":  1.0,
            "aa_isoleucine_g": 1.0,
            "aa_leucine_g":    1.0,
            "aa_lysine_g":     1.0,
            "aa_methionine_g": 1.0,
            "aa_phenylalanine_g": 1.0,
            "aa_valine_g":     1.0,
            "aa_histidine_g":  1.0,
        }
        result = _usda.protein_completeness(nutrients)
        assert result["has_data"] is True
        assert result["complete"] is False
        assert result["limiting_aa"] == "aa_tryptophan_g"

    def test_no_protein_returns_no_data(self):
        result = _usda.protein_completeness({"calories": 100.0})
        assert result["has_data"] is False

    def test_insufficient_aa_data_returns_no_data(self):
        """Only 2 AAs present — below the 5-AA threshold."""
        nutrients = {
            "protein_g": 10.0,
            "aa_lysine_g": 0.5,
            "aa_leucine_g": 0.8,
        }
        result = _usda.protein_completeness(nutrients)
        assert result["has_data"] is False

    def test_zero_valued_aa_keys_treated_as_no_data(self):
        """5+ AA keys present but all zero — branded foods include keys with 0.0 values.
        These must NOT count as 'has data' or all AA scores will be 0.00."""
        nutrients = {
            "protein_g": 20.0,
            "aa_tryptophan_g":    0.0,
            "aa_threonine_g":     0.0,
            "aa_isoleucine_g":    0.0,
            "aa_leucine_g":       0.0,
            "aa_lysine_g":        0.0,
            "aa_methionine_g":    0.0,
            "aa_phenylalanine_g": 0.0,
            "aa_valine_g":        0.0,
            "aa_histidine_g":     0.0,
        }
        result = _usda.protein_completeness(nutrients)
        assert result["has_data"] is False

    def test_scores_keyed_by_aa_key(self):
        result = _usda.protein_completeness(SAMPLE_NUTRIENTS)
        for key in result["scores"]:
            assert key.startswith("aa_")

    def test_zero_protein_returns_no_data(self):
        nutrients = {"protein_g": 0.0, "aa_lysine_g": 1.0}
        result = _usda.protein_completeness(nutrients)
        assert result["has_data"] is False


# ---------------------------------------------------------------------------
# has_amino_acid_data
# ---------------------------------------------------------------------------

class TestHasAminoAcidData:
    def test_full_aa_profile_returns_true(self):
        assert _usda.has_amino_acid_data(SAMPLE_NUTRIENTS) is True

    def test_no_protein_returns_true(self):
        # No protein means AA data is irrelevant — don't flag as missing
        assert _usda.has_amino_acid_data({"calories": 50.0}) is True

    def test_zero_protein_returns_true(self):
        assert _usda.has_amino_acid_data({"protein_g": 0.0}) is True

    def test_insufficient_aa_count_returns_false(self):
        # Has protein but only 2 AAs — below threshold
        nutrients = {"protein_g": 10.0, "aa_lysine_g": 0.5, "aa_leucine_g": 0.8}
        assert _usda.has_amino_acid_data(nutrients) is False

    def test_all_zero_aa_values_returns_false(self):
        # 9 AAs present but all zero — branded food pattern
        nutrients = {
            "protein_g": 20.0,
            "aa_tryptophan_g": 0.0, "aa_threonine_g": 0.0,
            "aa_isoleucine_g": 0.0, "aa_leucine_g":   0.0,
            "aa_lysine_g":     0.0, "aa_methionine_g": 0.0,
            "aa_phenylalanine_g": 0.0, "aa_valine_g":  0.0,
            "aa_histidine_g":  0.0,
        }
        assert _usda.has_amino_acid_data(nutrients) is False

    def test_five_nonzero_amino_acids_returns_true(self):
        # Exactly at the threshold
        nutrients = {
            "protein_g": 10.0,
            "aa_tryptophan_g": 0.1, "aa_threonine_g": 0.2,
            "aa_isoleucine_g": 0.3, "aa_leucine_g":   0.4,
            "aa_lysine_g":     0.5,
        }
        assert _usda.has_amino_acid_data(nutrients) is True

    def test_new_entries_flaxseed_and_yeast_resolve(self):
        # Confirm get_diaas resolves the two recently added entries
        assert _usda.get_diaas("ORGANIC GROUND FLAX SEED") == pytest.approx(0.52)
        assert _usda.get_diaas("NUTRITIONAL YEAST FLAKES") == pytest.approx(0.72)


# ---------------------------------------------------------------------------
# nutrient_label
# ---------------------------------------------------------------------------

class TestGetDIAAS:
    def test_known_plant_protein(self):
        assert _usda.get_diaas("Lentils, mature seeds, cooked, boiled") == pytest.approx(0.75)

    def test_known_animal_protein_capped_at_1(self):
        # Egg DIAAS is 1.13 in the table but must be capped at 1.0
        assert _usda.get_diaas("Egg, whole, raw") == pytest.approx(1.0)

    def test_case_insensitive(self):
        assert _usda.get_diaas("CHICKPEAS, COOKED") == pytest.approx(0.83)

    def test_unknown_food_returns_none(self):
        assert _usda.get_diaas("mystery surprise ingredient") is None

    def test_specific_entry_before_generic(self):
        # "soy protein isolate" should match its specific entry (0.97),
        # not the generic soy/tofu entry (0.84)
        assert _usda.get_diaas("soy protein isolate") == pytest.approx(0.97)

    def test_generic_soy_matches_tofu_entry(self):
        assert _usda.get_diaas("Tofu, raw, firm") == pytest.approx(0.84)

    def test_quinoa(self):
        assert _usda.get_diaas("Quinoa, cooked") == pytest.approx(0.85)

    def test_wheat(self):
        score = _usda.get_diaas("Bread, whole wheat")
        assert score == pytest.approx(0.46)


class TestGetAntinutrientFlags:
    """
    get_antinutrient_flags returns a list of dicts:
      {"problem": str, "cause": str, "solutions": [(label, description), ...]}
    Entries sharing the same group (e.g. both legume and seed phytate rules) are
    consolidated into a single flag with multiple solutions.
    """

    @staticmethod
    def _all_text(flags: list[dict]) -> str:
        """Flatten all flag text fields for substring assertions."""
        parts = []
        for f in flags:
            parts.append(f["problem"])
            parts.append(f["cause"])
            for label, sol in f["solutions"]:
                parts.append(label or "")
                parts.append(sol or "")
        return " ".join(parts).lower()

    def test_raw_beans_get_phytate_and_lectin_flags(self):
        flags = _usda.get_antinutrient_flags("kidney beans, raw")
        text = self._all_text(flags)
        assert "phytate" in text
        assert "lectin" in text

    def test_cooked_beans_suppress_lectin_flag(self):
        flags = _usda.get_antinutrient_flags("black beans, cooked, boiled")
        text = self._all_text(flags)
        assert "phytate" in text
        assert "lectin" not in text

    def test_phytate_solutions_are_listed(self):
        # Raw legume should have at least one solution (soak/sprout)
        flags = _usda.get_antinutrient_flags("kidney beans, raw")
        phytate = next(f for f in flags if "phytate" in f["cause"])
        assert len(phytate["solutions"]) >= 1
        sol_text = " ".join(s for _, s in phytate["solutions"]).lower()
        assert "soak" in sol_text or "sprout" in sol_text

    def test_food_matching_both_phytate_rules_gets_one_consolidated_flag(self):
        # USDA names like "Beans, snap, seeds, mature" match both the legume rule
        # and the nut/seed rule — they must consolidate into a single phytate flag.
        flags = _usda.get_antinutrient_flags("beans, snap, seeds, mature")
        phytate_flags = [f for f in flags if "phytate" in f["cause"]]
        assert len(phytate_flags) == 1, "two phytate rules on same food must merge"
        assert len(phytate_flags[0]["solutions"]) >= 2

    def test_spinach_oxalate_flag(self):
        flags = _usda.get_antinutrient_flags("Spinach, raw")
        text = self._all_text(flags)
        assert "oxalate" in text

    def test_animal_protein_no_flags(self):
        assert _usda.get_antinutrient_flags("Chicken breast, cooked") == []

    def test_corn_gets_niacin_flag(self):
        flags = _usda.get_antinutrient_flags("Corn, yellow, raw")
        text = self._all_text(flags)
        assert "niacin" in text

    def test_corn_nixtamalization_suppresses_niacin(self):
        flags = _usda.get_antinutrient_flags("Tortillas, ready-to-bake, corn, masa")
        text = self._all_text(flags)
        assert "niacin" not in text

    def test_oats_phytate_flag(self):
        flags = _usda.get_antinutrient_flags("Oats, rolled, raw")
        text = self._all_text(flags)
        assert "phytate" in text

    def test_peanut_gets_legume_phytate_not_seed_phytate(self):
        # Peanuts are legumes — should get "soak/sprout" solution, not "roasting"
        flags = _usda.get_antinutrient_flags("peanuts, dry-roasted")
        phytate = next((f for f in flags if "phytate" in f["cause"]), None)
        assert phytate is not None
        sol_text = " ".join(s for _, s in phytate["solutions"]).lower()
        assert "soak" in sol_text or "sprout" in sol_text

    def test_empty_string_returns_empty(self):
        assert _usda.get_antinutrient_flags("") == []


class TestNutrientLabel:
    def test_known_key_returns_label_and_unit(self):
        label, unit = _usda.nutrient_label("calories")
        assert label == "Calories"
        assert unit == "kcal"

    def test_protein_label(self):
        label, unit = _usda.nutrient_label("protein_g")
        assert "Protein" in label
        assert unit == "g"

    def test_unknown_key_returns_key_and_empty_unit(self):
        label, unit = _usda.nutrient_label("made_up_key")
        assert label == "made_up_key"
        assert unit == ""

    def test_all_nutrient_map_keys_round_trip(self):
        """Every key in NUTRIENT_MAP can be looked up via nutrient_label."""
        for _nid, (key, expected_label, expected_unit) in _usda.NUTRIENT_MAP.items():
            label, unit = _usda.nutrient_label(key)
            assert label == expected_label
            assert unit == expected_unit


# ---------------------------------------------------------------------------
# get_aa_gaps
# ---------------------------------------------------------------------------

# Minimal complete-protein nutrients (all AAs above reference)
_COMPLETE_NUTRIENTS = {
    "protein_g":          20.0,
    "aa_tryptophan_g":    0.20,   # ref 7 mg/g → need 0.14g → have 0.20 ✓
    "aa_threonine_g":     0.60,   # ref 23 → need 0.46 ✓
    "aa_isoleucine_g":    0.80,   # ref 30 → need 0.60 ✓
    "aa_leucine_g":       1.40,   # ref 59 → need 1.18 ✓
    "aa_lysine_g":        1.00,   # ref 45 → need 0.90 ✓
    "aa_methionine_g":    0.60,   # ref 22 → need 0.44 ✓
    "aa_phenylalanine_g": 0.90,   # ref 38 → need 0.76 ✓
    "aa_valine_g":        0.90,   # ref 39 → need 0.78 ✓
    "aa_histidine_g":     0.40,   # ref 15 → need 0.30 ✓
}

# Nutrients deficient in lysine and tryptophan (all others fine)
_DEFICIENT_NUTRIENTS = {
    "protein_g":          20.0,
    "aa_tryptophan_g":    0.08,   # ref 7 mg/g → need 0.14g → score 0.57 ✗
    "aa_threonine_g":     0.60,
    "aa_isoleucine_g":    0.80,
    "aa_leucine_g":       1.40,
    "aa_lysine_g":        0.50,   # ref 45 mg/g → need 0.90g → score 0.56 ✗
    "aa_methionine_g":    0.60,
    "aa_phenylalanine_g": 0.90,
    "aa_valine_g":        0.90,
    "aa_histidine_g":     0.40,
}


class TestGetAaGaps:
    def test_complete_protein_returns_empty(self):
        assert _usda.get_aa_gaps(_COMPLETE_NUTRIENTS) == []

    def test_identifies_deficient_aas(self):
        gaps = _usda.get_aa_gaps(_DEFICIENT_NUTRIENTS)
        gap_keys = [g[0] for g in gaps]
        assert "aa_tryptophan_g" in gap_keys
        assert "aa_lysine_g" in gap_keys

    def test_sorted_most_limiting_first(self):
        gaps = _usda.get_aa_gaps(_DEFICIENT_NUTRIENTS)
        scores = [g[1] for g in gaps]
        assert scores == sorted(scores)

    def test_deficit_g_is_positive(self):
        gaps = _usda.get_aa_gaps(_DEFICIENT_NUTRIENTS)
        for _key, _score, deficit in gaps:
            assert deficit > 0

    def test_no_protein_returns_empty(self):
        assert _usda.get_aa_gaps({"protein_g": 0.0, "aa_lysine_g": 1.0}) == []

    def test_missing_protein_key_returns_empty(self):
        assert _usda.get_aa_gaps({"aa_lysine_g": 1.0}) == []

    def test_near_complete_aa_not_reported_as_gap(self):
        # AAs scoring ≥ 0.95 should not appear — they are too close to adequate
        # to generate practical complement suggestions (e.g. pinto bean isoleucine
        # at score 0.994 used to produce trivial 1g suggestions).
        nutrients = dict(_COMPLETE_NUTRIENTS)
        nutrients["aa_isoleucine_g"] = nutrients["aa_isoleucine_g"] * 0.97  # score ~0.97 < 1.0 but ≥ 0.95
        # Lysine far below threshold — should appear
        nutrients["aa_lysine_g"] = 0.2  # score ≈ 0.22
        gaps = _usda.get_aa_gaps(nutrients)
        gap_keys = [g[0] for g in gaps]
        assert "aa_lysine_g" in gap_keys
        assert "aa_isoleucine_g" not in gap_keys


# ---------------------------------------------------------------------------
# suggest_complements
# ---------------------------------------------------------------------------

class TestSuggestComplements:
    def test_complete_protein_returns_no_suggestions(self):
        result = _usda.suggest_complements(_COMPLETE_NUTRIENTS, [])
        assert result["pantry"] == []
        assert result["general"] == []

    def test_general_suggestions_returned_when_pantry_empty(self):
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        assert len(result["general"]) > 0

    def test_suggestion_has_required_keys(self):
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        s = result["general"][0]
        for key in ("name", "grams", "new_scores", "new_complete",
                    "gaps_closed", "protein_added", "digestible_protein_added"):
            assert key in s, f"Missing key: {key}"

    def test_suggestion_closes_primary_gap(self):
        gaps_before = _usda.get_aa_gaps(_DEFICIENT_NUTRIENTS)
        primary_aa = gaps_before[0][0]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        s = result["general"][0]
        assert s["new_scores"].get(primary_aa, 0) >= 0.95

    def test_pantry_candidate_with_nutrients_used(self):
        # Lentils are high in lysine — should appear as a pantry suggestion
        lentil_nutrients = {
            "protein_g": 9.02,
            "aa_tryptophan_g": 0.077, "aa_threonine_g": 0.355,
            "aa_isoleucine_g": 0.374, "aa_leucine_g": 0.636,
            "aa_lysine_g": 0.624,     "aa_methionine_g": 0.077,
            "aa_phenylalanine_g": 0.450, "aa_valine_g": 0.432,
            "aa_histidine_g": 0.254,
        }
        pantry = [{"name": "Lentils, cooked", "nutrients": lentil_nutrients, "diaas": 0.75}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        assert len(result["pantry"]) == 1
        assert result["pantry"][0]["name"] == "Lentils, cooked"

    def test_pantry_food_excluded_from_general(self):
        pantry = [{"name": "Lentils, cooked", "nutrients": None, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        general_names = [s["name"] for s in result["general"]]
        assert "Lentils, cooked" not in general_names

    def test_grams_is_positive_integer(self):
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        for s in result["general"]:
            assert isinstance(s["grams"], int)
            assert s["grams"] > 0

    def test_digestible_protein_less_than_raw(self):
        # For foods with DIAAS < 1.0, digestible < raw
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        for s in result["general"]:
            if s.get("diaas") and s["diaas"] < 1.0:
                assert s["digestible_protein_added"] < s["protein_added"]

    def test_secondary_gap_foods_included(self):
        # Nutrients where methionine is the primary gap (legumes can't fix it —
        # their met/protein ratio is below reference) and lysine is secondary.
        # After the fix, lentils should appear because they CAN close the lysine gap.
        nutrients = {
            "protein_g":          20.0,
            "aa_tryptophan_g":    0.20,
            "aa_threonine_g":     0.60,
            "aa_isoleucine_g":    0.80,
            "aa_leucine_g":       1.40,
            "aa_lysine_g":        0.50,   # score ≈ 0.56 — secondary gap
            "aa_methionine_g":    0.20,   # score ≈ 0.45 — primary gap
            "aa_phenylalanine_g": 0.90,
            "aa_valine_g":        0.90,
            "aa_histidine_g":     0.40,
        }
        result = _usda.suggest_complements(nutrients, [])
        general_names = [s["name"] for s in result["general"]]
        # Lentils, chickpeas, and similar legumes are rich in lysine and should
        # now appear even though they cannot address the primary methionine gap.
        legume_present = any(
            name in general_names
            for name in ("Lentils, cooked", "Chickpeas, cooked", "Black beans, cooked",
                         "Kidney beans, cooked", "Edamame, cooked")
        )
        assert legume_present, f"No legume found; got: {general_names}"

    def test_secondary_gap_suggestion_improves_that_gap(self):
        # Same methionine-primary setup.  Each suggestion must improve at least
        # one gap AA score compared to the base.
        nutrients = {
            "protein_g":          20.0,
            "aa_tryptophan_g":    0.20,
            "aa_threonine_g":     0.60,
            "aa_isoleucine_g":    0.80,
            "aa_leucine_g":       1.40,
            "aa_lysine_g":        0.50,
            "aa_methionine_g":    0.20,
            "aa_phenylalanine_g": 0.90,
            "aa_valine_g":        0.90,
            "aa_histidine_g":     0.40,
        }
        base_pc = _usda.protein_completeness(nutrients)
        base_scores = base_pc["scores"]
        result = _usda.suggest_complements(nutrients, [])
        for s in result["general"]:
            improved = any(
                s["new_scores"].get(aa, 0) > base_scores.get(aa, 0)
                for aa in base_scores
            )
            assert improved, f"{s['name']} did not improve any AA score"


# ---------------------------------------------------------------------------
# _score_one_complement  (module-level helper, tested directly)
# ---------------------------------------------------------------------------

from usda_nutrients import _score_one_complement, get_aa_gaps

class TestScoreOneComplement:
    # Base with Met+Cys gap only (score ~0.70)
    _BASE = {
        "protein_g":          20.0,
        "aa_tryptophan_g":    0.20,
        "aa_threonine_g":     0.60,
        "aa_isoleucine_g":    0.80,
        "aa_leucine_g":       1.40,
        "aa_lysine_g":        1.00,   # ref=48 mg/g → need 0.96g → score 1.04 ✓
        "aa_methionine_g":    0.200,  # Met+Cys score ~0.70 (primary gap)
        "aa_cystine_g":       0.108,
        "aa_phenylalanine_g": 0.90,
        "aa_valine_g":        0.90,
        "aa_histidine_g":     0.40,
    }
    # Brazil nuts: Met+Cys ratio ~94 mg/g protein — well above 22 mg/g reference
    _BRAZIL = {
        "protein_g":        14.32,
        "aa_methionine_g":  1.008, "aa_cystine_g": 0.342,
        "aa_lysine_g":      0.492,
        "aa_tryptophan_g":  0.141, "aa_threonine_g":   0.362,
        "aa_isoleucine_g":  0.516, "aa_leucine_g":     1.155,
        "aa_phenylalanine_g": 0.630, "aa_valine_g":    0.756,
        "aa_histidine_g":   0.235,
    }
    # Soy protein isolate: Met+Cys ratio ~23 mg/g — just barely above reference
    _SOY = {
        "protein_g":        86.04,
        "aa_methionine_g":  1.145, "aa_cystine_g": 0.833,
        "aa_lysine_g":      5.379,
        "aa_tryptophan_g":  1.143, "aa_threonine_g":  3.579,
        "aa_isoleucine_g":  4.382, "aa_leucine_g":    7.133,
        "aa_phenylalanine_g": 4.870, "aa_valine_g":   4.487,
        "aa_histidine_g":   2.425,
    }
    # All-rice "food": met+cys ratio ~20 mg/g — below 22 mg/g reference
    _LOW_MET_CYS = {
        "protein_g":        7.0,
        "aa_methionine_g":  0.088, "aa_cystine_g": 0.048,  # combined 1.94 g/100g but ratio < ref
        "aa_lysine_g":      0.210,
        "aa_tryptophan_g":  0.077, "aa_threonine_g":  0.256,
        "aa_isoleucine_g":  0.307, "aa_leucine_g":    0.588,
        "aa_phenylalanine_g": 0.371, "aa_valine_g":   0.438,
        "aa_histidine_g":   0.142,
    }

    def test_brazil_closes_met_cys_gap(self):
        gaps = get_aa_gaps(self._BASE)
        primary_aa = "aa_methionine_g"
        result = _score_one_complement(self._BASE, gaps, 1.0, self._BRAZIL, 0.54, primary_aa)
        assert result is not None
        assert result["grams"] > 0
        assert result["new_scores"].get(primary_aa, 0) >= 1.0

    def test_below_reference_returns_none(self):
        # Rice-like food has Met+Cys/protein below the FAO reference — cannot close gap.
        gaps = get_aa_gaps(self._BASE)
        result = _score_one_complement(
            self._BASE, gaps, 1.0, self._LOW_MET_CYS, None, "aa_methionine_g"
        )
        assert result is None

    def test_returns_required_keys(self):
        gaps = get_aa_gaps(self._BASE)
        result = _score_one_complement(self._BASE, gaps, 1.0, self._BRAZIL, 0.54, "aa_methionine_g")
        assert result is not None
        for key in ("grams", "new_scores", "new_complete", "gaps_closed",
                    "opens_new_gap", "closes_primary", "remaining_gaps",
                    "protein_added", "digestible_protein_added", "diaas"):
            assert key in result, f"Missing key: {key}"

    def test_no_private_fields_leaked(self):
        # Brazil nuts have a high Met+Cys ratio — reliably non-None for this gap.
        gaps = get_aa_gaps(self._BASE)
        result = _score_one_complement(self._BASE, gaps, 1.0, self._BRAZIL, 0.54, "aa_methionine_g")
        assert result is not None
        assert "_combined_nutrients" not in result
        assert "_new_gaps" not in result

    def test_brazil_opens_new_gap_when_lysine_borderline(self):
        # Lysine FAO reference = 48 mg/g (not 45). With 20g protein, threshold is 0.95*0.96 = 0.912g.
        # Use 0.924g → score 0.9625 (above threshold but vulnerable to dilution by Brazil nuts).
        base = dict(self._BASE)
        base["aa_lysine_g"] = 0.924  # score ~0.9625 — above 0.95 threshold, but borderline
        gaps = get_aa_gaps(base)
        assert not any(aa == "aa_lysine_g" for aa, _, _ in gaps), "lysine should not be a gap initially"
        result = _score_one_complement(base, gaps, 1.0, self._BRAZIL, 0.54, "aa_methionine_g")
        assert result is not None
        assert result["opens_new_gap"] is True

    def test_brazil_no_new_gap_with_sufficient_lysine(self):
        # _BASE has lysine=1.00g with 20g protein → score 1.04, well above threshold.
        # Adding ~15g Brazil nuts adds a small amount of lysine; the combined score
        # stays above 0.95, so opens_new_gap should be False.
        gaps = get_aa_gaps(self._BASE)
        result = _score_one_complement(self._BASE, gaps, 1.0, self._BRAZIL, 0.54, "aa_methionine_g")
        assert result is not None
        assert result["opens_new_gap"] is False


# ---------------------------------------------------------------------------
# suggest_complements — gap-cascade pairs
# ---------------------------------------------------------------------------

# Nutrients with Met+Cys gap (primary) and lysine just above threshold.
# Adding Brazil nuts closes Met+Cys but dilutes lysine below 0.95 → opens lysine gap.
# A lysine-rich legume then closes the lysine gap → valid pair.
_PAIR_CASCADE_NUTRIENTS = {
    # Met+Cys primary gap; lysine borderline — Brazil nuts close Met+Cys but open
    # a lysine gap, requiring a lysine-rich legume as the second food in a pair.
    # Lysine ref = 48 mg/g; threshold at score 0.95 = 0.912g with 20g protein.
    # 0.924g → score 0.9625 (above threshold but diluted below 0.95 by ~15g Brazil nuts).
    "protein_g":          20.0,
    "aa_tryptophan_g":    0.20,
    "aa_threonine_g":     0.60,
    "aa_isoleucine_g":    0.80,
    "aa_leucine_g":       1.40,
    "aa_lysine_g":        0.924,    # score ~0.9625 — above threshold, vulnerable to dilution
    "aa_methionine_g":    0.200,    # Met+Cys score ~0.70 — primary gap
    "aa_cystine_g":       0.108,
    "aa_phenylalanine_g": 0.90,
    "aa_valine_g":        0.90,
    "aa_histidine_g":     0.40,
}

class TestComplementPairs:
    def test_pairs_key_always_present(self):
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        assert "pairs" in result

    def test_complete_nutrients_no_pairs(self):
        result = _usda.suggest_complements(_COMPLETE_NUTRIENTS, [])
        assert result["pairs"] == []

    def test_cascade_scenario_produces_pairs(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        assert len(result["pairs"]) > 0, "Expected at least one two-food pair from cascade scenario"

    def test_pair_has_exactly_two_foods(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        for pair in result["pairs"]:
            assert len(pair["foods"]) == 2

    def test_pair_has_required_keys(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        assert result["pairs"], "Need at least one pair to test structure"
        p = result["pairs"][0]
        for key in ("foods", "total_grams", "new_complete",
                    "new_scores", "total_protein_added", "total_dig_added"):
            assert key in p, f"Missing pair key: {key}"

    def test_pair_food_has_required_keys(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        assert result["pairs"]
        for f in result["pairs"][0]["foods"]:
            for key in ("name", "grams", "protein_added", "dig_added"):
                assert key in f, f"Missing food key: {key}"

    def test_pair_closes_all_gaps(self):
        # Every pair must bring all AAs to score ≥ 0.95 (no remaining gaps).
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        for pair in result["pairs"]:
            assert pair["gaps_closed"] is True, (
                f"Pair {pair['foods'][0]['name']} + {pair['foods'][1]['name']} "
                f"should close all gaps (score ≥ 0.95 on every AA)"
            )

    def test_pair_total_grams_matches_sum(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        for pair in result["pairs"]:
            expected = pair["foods"][0]["grams"] + pair["foods"][1]["grams"]
            assert pair["total_grams"] == expected

    def test_pairs_sorted_ascending_by_total_grams(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        pairs = result["pairs"]
        if len(pairs) >= 2:
            total_grams = [p["total_grams"] for p in pairs]
            assert total_grams == sorted(total_grams), f"Pairs not sorted: {total_grams}"

    def test_pair_foods_are_different(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        for pair in result["pairs"]:
            assert pair["foods"][0]["name"] != pair["foods"][1]["name"]

    def test_no_duplicate_pairs(self):
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        seen: set[frozenset] = set()
        for pair in result["pairs"]:
            key = frozenset(f["name"] for f in pair["foods"])
            assert key not in seen, f"Duplicate pair: {key}"
            seen.add(key)

    def test_first_food_opens_new_gap(self):
        # Verify the invariant that food A (the first leg of every cascade pair)
        # opens a new gap when added alone to the base.
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        gaps_before = set(aa for aa, _, _ in _usda.get_aa_gaps(_PAIR_CASCADE_NUTRIENTS))
        for pair in result["pairs"]:
            a_name = pair["foods"][0]["name"]
            a_grams = pair["foods"][0]["grams"]
            # Resolve A's nutrients via the complement table
            comp_n = _usda.get_complement_nutrients(a_name)
            if comp_n is None:
                continue  # pantry food without nutrients — skip structural check
            from usda_nutrients import scale_nutrients, sum_nutrients
            after_a = sum_nutrients(_PAIR_CASCADE_NUTRIENTS, scale_nutrients(comp_n, a_grams))
            gaps_after_a = set(aa for aa, _, _ in _usda.get_aa_gaps(after_a))
            new_gaps_opened = gaps_after_a - gaps_before
            assert new_gaps_opened, (
                f"First food '{a_name}' should open a new gap but didn't. "
                f"Gaps before: {gaps_before}, after: {gaps_after_a}"
            )


# ---------------------------------------------------------------------------
# get_density_g_per_ml
# ---------------------------------------------------------------------------

class TestGetDensityGPerMl:
    def test_known_seed_matched_by_keyword(self):
        assert _usda.get_density_g_per_ml("Seeds, hemp seed, hulled", []) == pytest.approx(0.57)

    def test_nutritional_yeast(self):
        assert _usda.get_density_g_per_ml("Nutritional yeast flakes", []) == pytest.approx(0.61)

    def test_pumpkin_seeds(self):
        assert _usda.get_density_g_per_ml("Pumpkin seeds, roasted", []) == pytest.approx(0.46)

    def test_unknown_food_returns_none(self):
        assert _usda.get_density_g_per_ml("mystery unrecognized food xyz", []) is None

    def test_static_table_takes_priority_over_usda_portions(self):
        # Static table lookup wins even when USDA portion data is provided.
        # Nutritional yeast table entry is 0.61 g/ml; the USDA cup portion
        # (90g/cup = 0.380 g/ml) is ignored because the table matched first.
        portions = [{"description": "1 cup", "gram_weight": 90.0}]
        density = _usda.get_density_g_per_ml("Nutritional yeast", portions)
        assert density == pytest.approx(0.61, rel=0.01)

    def test_usda_tablespoon_portion_used(self):
        portions = [{"description": "1 tablespoon", "gram_weight": 15.0}]
        density = _usda.get_density_g_per_ml("Some unknown food", portions)
        assert density == pytest.approx(15.0 / 14.8, rel=0.01)

    def test_case_insensitive_keyword_match(self):
        assert _usda.get_density_g_per_ml("QUINOA, cooked", []) == pytest.approx(0.71)

    def test_red_pepper_flakes_has_density(self):
        """Regression test: user-reported bug — volume units for red pepper
        flakes were rejected for lack of density data."""
        assert _usda.get_density_g_per_ml("Red pepper flakes", []) == pytest.approx(0.35)
        assert _usda.get_density_g_per_ml("Spices, pepper, red or cayenne", []) == pytest.approx(0.45)

    def test_generic_spice_fallback(self):
        """Any USDA "Spices, ..." food not individually itemized still gets an
        approximate density rather than failing outright."""
        assert _usda.get_density_g_per_ml("Spices, savory, ground", []) == pytest.approx(0.40)

    def test_sage_keyword_does_not_match_sausage(self):
        """"sage" must not match as a substring of "sausage" (false positive
        density from an unrelated spice keyword)."""
        assert _usda.get_density_g_per_ml("Sausage, pork, fresh, cooked", []) is None
