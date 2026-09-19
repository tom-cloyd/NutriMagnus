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
        """Abridged endpoint uses 'number' as a string, in USDA's separate
        'nutrient number' ID space (not nutrient.id) — "208" is calories there,
        not "1008" (which is the nutrient.id scheme's calories key)."""
        response = self._make_usda_response([
            {"number": "208", "value": 300.0}
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
# get_food_detail — the abridged-format fallback when a full-format response
# has real nutrient rows but none carry a parseable nutrient id (found live
# via TESTING-ROADMAP.md item #1's USDA fixture recording, 2026-09-11: some
# Branded records return foodNutrients items shaped like
# {"type": "FoodNutrient", "id": <row id>, "amount": ...} — no nutrient.id/
# nutrientId at all — so _parse_food() silently produces an empty nutrients
# dict despite real data being present).
# ---------------------------------------------------------------------------

import usda_api as _usda_api

class TestGetFoodDetailAbridgedFallback:
    _FULL_UNPARSEABLE = {
        "fdcId": 999, "description": "Mystery Branded Food", "dataType": "Branded",
        "brandOwner": "Some Brand", "servingSize": 100.0, "servingSizeUnit": "g",
        "householdServingFullText": "1 serving",
        "foodPortions": [{"portionDescription": "1 serving", "gramWeight": 50.0}],
        # Every item has only an opaque row id, not a nutrient-type id.
        "foodNutrients": [
            {"type": "FoodNutrient", "id": 1, "amount": 20.4},
            {"type": "FoodNutrient", "id": 2, "amount": 8.1},
        ],
    }
    _ABRIDGED_PARSEABLE = {
        "fdcId": 999, "description": "Mystery Branded Food", "dataType": "Branded",
        "foodNutrients": [
            {"number": "203", "name": "Protein", "amount": 20.4},
            {"number": "204", "name": "Total lipid (fat)", "amount": 8.1},
        ],
    }

    def test_retries_abridged_when_full_format_yields_no_nutrients(self, monkeypatch):
        calls = []

        def fake_get(path, params):
            calls.append(dict(params))
            if params.get("format") == "abridged":
                return self._ABRIDGED_PARSEABLE
            return self._FULL_UNPARSEABLE

        monkeypatch.setattr(_usda_api, "_get", fake_get)
        result = _usda_api.get_food_detail(999)

        assert len(calls) == 2, "must retry with format=abridged, not give up on empty nutrients"
        assert result["nutrients"]["protein_g"] == pytest.approx(20.4)
        assert result["nutrients"]["fat_g"] == pytest.approx(8.1)
        # Portions/brand must still come from the full-format response —
        # abridged doesn't carry foodPortions at all.
        assert result["portions"] == [{"description": "1 serving", "gram_weight": 50.0}]
        assert result["brand"] == "Some Brand"

    def test_does_not_retry_when_full_format_already_has_nutrients(self, monkeypatch):
        calls = []

        def fake_get(path, params):
            calls.append(dict(params))
            return {
                "fdcId": 1, "description": "Normal Food", "dataType": "SR Legacy",
                "foodNutrients": [{"nutrientId": 1003, "value": 10.0}],
            }

        monkeypatch.setattr(_usda_api, "_get", fake_get)
        result = _usda_api.get_food_detail(1)

        assert len(calls) == 1, "must not make a second call when the first already parsed fine"
        assert result["nutrients"]["protein_g"] == pytest.approx(10.0)

    def test_does_not_retry_when_food_genuinely_has_no_nutrient_rows(self, monkeypatch):
        # An empty nutrients dict because the raw response had NO nutrient
        # rows at all (not because they were unparseable) must not trigger
        # a pointless second network call.
        calls = []

        def fake_get(path, params):
            calls.append(dict(params))
            return {"fdcId": 2, "description": "No Data Food", "dataType": "Branded",
                     "foodNutrients": []}

        monkeypatch.setattr(_usda_api, "_get", fake_get)
        result = _usda_api.get_food_detail(2)

        assert len(calls) == 1
        assert result["nutrients"] == {}


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
                    "gaps_closed", "protein_added", "digestible_protein_added",
                    "recipe_id", "serving_weight_g", "estimated", "fdc_id"):
            assert key in s, f"Missing key: {key}"

    def test_suggestion_diaas_reflects_candidate_own_value_not_lookup(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found
        # "cand.get('diaas')" had a survived key-literal mutation
        # ("cand.get(None)") — undetected because every prior test either
        # passed diaas=None explicitly (where the mutant's None result is
        # indistinguishable) or never checked the resulting "diaas" field
        # against the input at all. Brazil nuts (0.54) is not this base's
        # own default lookup value, so the field must reflect the input
        # exactly, not some other value get_diaas() would return.
        pantry = [{"name": "Brazil nuts",
                   "nutrients": {
                       "protein_g": 14.32, "aa_methionine_g": 1.008, "aa_cystine_g": 0.342,
                       "aa_lysine_g": 0.492, "aa_tryptophan_g": 0.141, "aa_threonine_g": 0.362,
                       "aa_isoleucine_g": 0.516, "aa_leucine_g": 1.155,
                       "aa_phenylalanine_g": 0.630, "aa_valine_g": 0.756, "aa_histidine_g": 0.235,
                   },
                   "diaas": 0.54}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        assert len(result["pantry"]) == 1
        assert result["pantry"][0]["diaas"] == 0.54

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

    def test_diet_pref_all_includes_meat_and_dairy(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found
        # diet_pref filtering had zero test coverage at all — no test ever
        # passed anything but the "all" default. "Chicken breast, cooked"
        # (animal=True, dairy_egg=None/False) and "Cheese, cheddar"
        # (animal=True, dairy_egg=True) both qualify against this base's
        # gaps and should both appear when nothing is excluded.
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [], diet_pref="all")
        names = [s["name"] for s in result["general"]]
        assert "Chicken breast, cooked" in names
        assert "Cheese, cheddar" in names

    def test_diet_pref_default_is_all_not_something_else(self):
        # diet_pref's own default value ("all") — a mutation changing the
        # default string literal (e.g. to a typo'd variant) would survive
        # every test that passes diet_pref explicitly, since the default
        # is never actually reached. This test omits the parameter entirely.
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        names = [s["name"] for s in result["general"]]
        assert "Chicken breast, cooked" in names
        assert "Cheese, cheddar" in names

    def test_diet_pref_default_all_does_not_filter_pantry(self):
        # A companion mutation on the actual comparison ("if diet_pref !=
        # 'all':") survived the test above because it used an EMPTY
        # pantry — filtering an empty list is a no-op regardless of the
        # mutant, so the comparison's truth value was never observable.
        # A pantry candidate matching a curated meat entry by name must
        # survive through when diet_pref is omitted (defaults to "all").
        pantry = [{"name": "Chicken breast, cooked", "nutrients": None, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        assert any(s["name"] == "Chicken breast, cooked" for s in result["pantry"])

    def test_diet_pref_vegetarian_excludes_meat_but_keeps_dairy(self):
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [], diet_pref="vegetarian")
        names = [s["name"] for s in result["general"]]
        assert "Chicken breast, cooked" not in names
        assert "Cheese, cheddar" in names

    def test_diet_pref_plant_only_excludes_meat_and_dairy(self):
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [], diet_pref="plant_only")
        names = [s["name"] for s in result["general"]]
        assert "Chicken breast, cooked" not in names
        assert "Cheese, cheddar" not in names

    def test_diet_pref_by_name_filters_pantry_candidates_too(self):
        # _diet_allows_by_name() — the pantry-side counterpart, matched
        # against the curated table by name rather than an "animal" flag
        # carried on the candidate dict itself. A pantry food with no
        # nutrients of its own (falls through to the curated-table lookup)
        # named after a known meat entry must be excluded under plant_only.
        pantry = [{"name": "Chicken breast, cooked", "nutrients": None, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry, diet_pref="plant_only")
        assert result["pantry"] == []

    def test_diet_pref_by_name_allows_unmatched_pantry_food(self):
        # A pantry food with no curated-table keyword match has no basis to
        # exclude and must be let through regardless of diet_pref.
        pantry = [{"name": "Xyzzy Homemade Protein Mix",
                   "nutrients": {
                       "protein_g": 20.0, "aa_lysine_g": 1.5, "aa_methionine_g": 0.5,
                       "aa_cystine_g": 0.3, "aa_tryptophan_g": 0.3, "aa_threonine_g": 0.9,
                       "aa_isoleucine_g": 1.1, "aa_leucine_g": 1.9, "aa_phenylalanine_g": 1.1,
                       "aa_valine_g": 1.1, "aa_histidine_g": 0.5,
                   }, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry, diet_pref="plant_only")
        assert any(s["name"] == "Xyzzy Homemade Protein Mix" for s in result["pantry"])

    def test_exclude_names_removes_pantry_candidate(self):
        # exclude_names also had zero test coverage — used by the web app's
        # per-suggestion "ignore" checkboxes (see complements.py docs).
        pantry = [{"name": "Lentils, cooked", "nutrients": None, "diaas": None}]
        result = _usda.suggest_complements(
            _DEFICIENT_NUTRIENTS, pantry, exclude_names={"Lentils, cooked"}
        )
        assert result["pantry"] == []

    def test_exclude_names_is_case_insensitive(self):
        pantry = [{"name": "Lentils, cooked", "nutrients": None, "diaas": None}]
        result = _usda.suggest_complements(
            _DEFICIENT_NUTRIENTS, pantry, exclude_names={"LENTILS, COOKED"}
        )
        assert result["pantry"] == []

    def test_exclude_names_removes_general_candidate(self):
        result = _usda.suggest_complements(
            _DEFICIENT_NUTRIENTS, [], exclude_names={"Cheese, cheddar"}
        )
        names = [s["name"] for s in result["general"]]
        assert "Cheese, cheddar" not in names

    def test_exclude_names_does_not_remove_unrelated_candidates(self):
        # Guards against an overbroad mutation (e.g. excluding everything,
        # or excluding nothing) — the general tier must still contain some
        # non-excluded, otherwise-qualifying candidate.
        baseline = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        baseline_names = {s["name"] for s in baseline["general"]}
        assert len(baseline_names) > 1, "need at least 2 candidates for this test to mean anything"
        one_name = next(iter(baseline_names))
        result = _usda.suggest_complements(
            _DEFICIENT_NUTRIENTS, [], exclude_names={one_name}
        )
        remaining_names = {s["name"] for s in result["general"]}
        assert remaining_names == baseline_names - {one_name}

    def test_pantry_candidate_own_diaas_survives_curated_table_fallback(self):
        # "cand_diaas = cand_diaas or entry['diaas']" had a survived
        # mutation ("cand_diaas = None") for a pantry candidate that has
        # no nutrients of its own (falls to the curated-table lookup) but
        # DOES already carry its own explicit diaas value — that value
        # must be preserved, not silently discarded in favor of the
        # curated table's generic figure (or None).
        pantry = [{"name": "Lentils, cooked", "nutrients": None, "diaas": 0.99}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        assert result["pantry"]
        assert result["pantry"][0]["diaas"] == 0.99

    def test_pantry_gap_closer_recipe_id_reflects_input(self):
        # A dict-key-literal mutation on "recipe_id" (-> a lookup that
        # never matches) survived because no test checked this field's
        # value for an actual non-None recipe_id.
        base = {
            "protein_g": 10.0,
            "aa_methionine_g": 0.05, "aa_cystine_g": 0.03,
            "aa_lysine_g": 0.30,
        }
        pantry = [{"name": "RecipeCand", "diaas": None, "recipe_id": 42,
                   "nutrients": {"protein_g": 100.0, "aa_methionine_g": 3.0, "aa_cystine_g": 2.0}}]
        result = _usda.suggest_complements(base, pantry)
        assert result["pantry"]
        assert result["pantry"][0]["recipe_id"] == 42

    def test_general_curated_candidate_fdc_id_reflects_table_entry(self):
        # Same class of bug, for the curated-table branch of
        # general_candidates construction (no cache_candidates match).
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        lentils = next(s for s in result["general"] if s["name"] == "Lentils, cooked")
        assert lentils["fdc_id"] == 172421

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

    def test_primary_gap_closer_sorts_before_secondary_even_needing_more_grams(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found the
        # gap-closer sort key's primary-gap tiebreaker — "not r.get('closes_primary')"
        # — had no test distinguishing it from a broken version that ignores
        # closes_primary entirely and sorts by grams alone. Constructed so a
        # candidate that closes the PRIMARY gap needs far MORE grams (75g)
        # than one that only closes the SECONDARY gap (~1.18g) — under the
        # real sort key, the primary-gap closer still sorts first regardless;
        # under a broken one, the cheaper secondary-gap closer would win.
        base = {
            "protein_g": 10.0,
            "aa_methionine_g": 0.05, "aa_cystine_g": 0.03,  # score ~0.35 — primary (worst)
            "aa_lysine_g": 0.30,                             # score 0.625 — secondary
        }
        gaps = get_aa_gaps(base, digestibility=1.0)
        assert [g[0] for g in gaps] == ["aa_methionine_g", "aa_lysine_g"]

        # Closes methionine (primary) but needs 75g to do it.
        closes_primary_food = {"name": "PrimaryCloser",
            "nutrients": {"protein_g": 100.0, "aa_methionine_g": 2.0, "aa_cystine_g": 0.5},
            "diaas": None}
        # Closes only lysine (secondary) — no methionine/cystine at all — but
        # needs only ~1.18g.
        closes_secondary_food = {"name": "SecondaryCloser",
            "nutrients": {"protein_g": 100.0, "aa_lysine_g": 20.0},
            "diaas": None}

        result = _usda.suggest_complements(base, [closes_primary_food, closes_secondary_food])
        by_name = {s["name"]: s for s in result["pantry"]}
        assert by_name["PrimaryCloser"]["closes_primary"] is True
        assert by_name["SecondaryCloser"]["closes_primary"] is False
        assert by_name["PrimaryCloser"]["grams"] > by_name["SecondaryCloser"]["grams"]

        assert result["pantry"][0]["name"] == "PrimaryCloser", (
            "the primary-gap closer must sort first even though it needs more "
            f"grams than the secondary-gap closer; got order: "
            f"{[s['name'] for s in result['pantry']]}"
        )

    def test_more_gaps_closed_sorts_before_fewer_even_needing_more_grams(self):
        # The sort key's second tiebreaker ("-r['gaps_closed']") had no
        # test distinguishing it from a version that drops the "-" (or
        # drops the key from the tuple entirely) and falls through to
        # sorting by grams alone. Both candidates here close the primary
        # gap (so the first tiebreak is tied); B closes BOTH gaps but
        # needs 21g, A closes only the primary gap but needs just 6g — B
        # must still sort first.
        base = {
            "protein_g": 10.0,
            "aa_methionine_g": 0.05, "aa_cystine_g": 0.03,  # primary gap
            "aa_lysine_g": 0.30,                             # secondary gap
        }
        gaps = get_aa_gaps(base, digestibility=1.0)
        assert [g[0] for g in gaps] == ["aa_methionine_g", "aa_lysine_g"]

        a = {"name": "A_PrimaryOnly",
             "nutrients": {"protein_g": 100.0, "aa_methionine_g": 3.0, "aa_cystine_g": 2.0},
             "diaas": None}
        b = {"name": "B_ClosesBoth",
             "nutrients": {"protein_g": 100.0, "aa_methionine_g": 2.0, "aa_cystine_g": 1.0,
                            "aa_lysine_g": 6.0},
             "diaas": None}

        result = _usda.suggest_complements(base, [a, b])
        by_name = {s["name"]: s for s in result["pantry"]}
        assert by_name["A_PrimaryOnly"]["closes_primary"] is True
        assert by_name["B_ClosesBoth"]["closes_primary"] is True
        assert by_name["A_PrimaryOnly"]["gaps_closed"] == 1
        assert by_name["B_ClosesBoth"]["gaps_closed"] == 2
        assert by_name["B_ClosesBoth"]["grams"] > by_name["A_PrimaryOnly"]["grams"]

        assert result["pantry"][0]["name"] == "B_ClosesBoth", (
            "the candidate closing more gaps must sort first even though it "
            f"needs more grams; got order: {[s['name'] for s in result['pantry']]}"
        )


# ---------------------------------------------------------------------------
# suggest_complements — auto-estimate fallback + cache_candidates preference
# ---------------------------------------------------------------------------

class TestSuggestComplementsAutoEstimate:
    def test_complement_table_names_includes_known_entries(self):
        names = _usda.complement_table_names()
        assert "Nutritional yeast" in names
        assert len(names) > 10

    def test_pantry_food_missing_aa_is_auto_estimated(self):
        # Real pantry food, real macros, no AA data of its own — name matches
        # the curated "Nutritional yeast" entry by keyword.
        pantry = [{"name": "Nutritional Yeast Flakes", "fdc_id": 42,
                   "nutrients": {"protein_g": 45.0}, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        assert len(result["pantry"]) == 1
        s = result["pantry"][0]
        assert s["name"] == "Nutritional Yeast Flakes"
        assert s["fdc_id"] == 42
        assert s["estimated"] is True

    def test_estimate_scales_to_real_food_protein_not_curated_protein(self):
        # The curated "Nutritional yeast" entry is 52g protein/100g. A real
        # product with less protein (45g/100g) needs correspondingly MORE
        # grams to deliver the same amino acid payload — the estimate must
        # scale to the real food's own protein, not silently reuse the
        # curated table's own gram figure.
        curated_result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [])
        curated_grams = next(
            s["grams"] for s in curated_result["general"] if s["name"] == "Nutritional yeast"
        )
        pantry = [{"name": "Nutritional Yeast Flakes", "fdc_id": 42,
                   "nutrients": {"protein_g": 45.0}, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        assert result["pantry"][0]["grams"] > curated_grams

    def test_pantry_food_missing_aa_with_no_curated_match_is_dropped(self):
        # Real macros, no AA data, and no keyword match in the curated table —
        # should be silently excluded rather than crash or appear un-scored.
        pantry = [{"name": "Mystery Protein Bar", "fdc_id": 43,
                   "nutrients": {"protein_g": 20.0}, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry)
        assert result["pantry"] == []
        assert not any(s["name"] == "Mystery Protein Bar" for s in result["general"])

    def test_duplicate_candidate_name_scored_only_once(self):
        # "seen_names" dedup — a name that appears twice in pantry_candidates
        # (real-world data could plausibly have this) must only be scored
        # and listed once, not appear twice in the result.
        base = {
            "protein_g": 10.0,
            "aa_methionine_g": 0.05, "aa_cystine_g": 0.03,
            "aa_lysine_g": 0.30,
        }
        cand_nutrients = {"protein_g": 100.0, "aa_methionine_g": 3.0, "aa_cystine_g": 2.0}
        pantry = [
            {"name": "DupFood", "nutrients": cand_nutrients, "diaas": None},
            {"name": "DupFood", "nutrients": cand_nutrients, "diaas": None},
        ]
        result = _usda.suggest_complements(base, pantry)
        names = [s["name"] for s in result["pantry"]]
        assert names.count("DupFood") == 1

    def test_general_tier_prefers_cache_candidate_with_real_aa_data(self):
        real_yeast = {
            "name": "Nutritional Yeast Flakes", "fdc_id": 555,
            "nutrients": {
                "protein_g": 40.0,
                "aa_tryptophan_g": 0.5, "aa_threonine_g": 1.9, "aa_isoleucine_g": 1.9,
                "aa_leucine_g": 2.8, "aa_lysine_g": 2.4, "aa_methionine_g": 0.66,
                "aa_cystine_g": 0.18, "aa_phenylalanine_g": 1.5, "aa_valine_g": 2.1,
                "aa_histidine_g": 0.9,
            },
            "diaas": 0.7,
        }
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [], cache_candidates=[real_yeast])
        matches = [s for s in result["general"] if "yeast" in s["name"].lower()]
        assert len(matches) == 1
        assert matches[0]["name"] == "Nutritional Yeast Flakes"
        assert matches[0]["fdc_id"] == 555
        assert matches[0]["estimated"] is False

    def test_general_tier_auto_estimates_cache_candidate_missing_aa(self):
        real_yeast_no_aa = {"name": "Nutritional Yeast Flakes", "fdc_id": 777,
                             "nutrients": {"protein_g": 40.0}, "diaas": None}
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, [], cache_candidates=[real_yeast_no_aa])
        matches = [s for s in result["general"] if "yeast" in s["name"].lower()]
        assert len(matches) == 1
        assert matches[0]["fdc_id"] == 777
        assert matches[0]["estimated"] is True

    def test_cache_candidate_ignored_when_name_already_in_pantry(self):
        # Pantry already covers this name — cache_candidates shouldn't
        # duplicate it into the general tier.
        pantry = [{"name": "Nutritional yeast", "fdc_id": 1,
                   "nutrients": {"protein_g": 52.0}, "diaas": 0.72}]
        cache_dup = [{"name": "Nutritional Yeast Flakes", "fdc_id": 999,
                      "nutrients": {"protein_g": 40.0}, "diaas": None}]
        result = _usda.suggest_complements(_DEFICIENT_NUTRIENTS, pantry, cache_candidates=cache_dup)
        general_names = [s["name"].lower() for s in result["general"]]
        assert not any("yeast" in n for n in general_names)

    def test_excluded_cache_candidate_does_not_hide_later_curated_entries(self):
        # The general_candidates loop's "if real is not None and
        # real['name'].lower() in exclude_lower: continue" had a survived
        # continue->break mutation — since it iterates the ~25-entry
        # curated table in a fixed order, breaking out early on the FIRST
        # excluded cache-matched entry would silently wipe out every
        # curated suggestion that comes after it too. "Lentils, cooked" is
        # first in the table; excluding its cache match must not affect
        # entries later in the table (e.g. "Chickpeas, cooked", "Salmon,
        # cooked").
        cache = [{"name": "Lentils Product", "fdc_id": 999,
                  "nutrients": {"protein_g": 9.0}, "diaas": None}]
        result = _usda.suggest_complements(
            _DEFICIENT_NUTRIENTS, [], cache_candidates=cache, exclude_names={"Lentils Product"}
        )
        general_names = [s["name"] for s in result["general"]]
        assert not any("lentil" in n.lower() for n in general_names)
        assert "Chickpeas, cooked" in general_names
        assert "Salmon, cooked" in general_names


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
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found that
        # new_complete/gaps_closed had no exact-value coverage — a mutant
        # reading the wrong dict key for "complete" (defaulting to False)
        # survived every existing test because none of them exercised a
        # scenario where new_complete is actually True. This BASE/BRAZIL
        # pairing closes every essential AA at once, so it's the one
        # scenario in this class where that's the case.
        assert result["new_complete"] is True
        assert result["gaps_closed"] == 1

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
        # gaps_closed = len(base_gaps) - len(new_gaps): Met+Cys closes but
        # lysine opens, so the count nets to zero — a mutation changing this
        # to "+" would give 2 instead, undetected by the opens_new_gap check
        # alone since that only inspects set membership, not counts.
        assert result["gaps_closed"] == 0
        assert result["remaining_gaps"] == 1

    def test_brazil_no_new_gap_with_sufficient_lysine(self):
        # _BASE has lysine=1.00g with 20g protein → score 1.04, well above threshold.
        # Adding ~15g Brazil nuts adds a small amount of lysine; the combined score
        # stays above 0.95, so opens_new_gap should be False.
        gaps = get_aa_gaps(self._BASE)
        result = _score_one_complement(self._BASE, gaps, 1.0, self._BRAZIL, 0.54, "aa_methionine_g")
        assert result is not None
        assert result["opens_new_gap"] is False

    def test_exact_grams_and_predicted_diaas_match_hand_calculation(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found this
        # function's core formula only ever checked for a "reasonable-looking"
        # result (grams > 0, score >= 1.0), never an exact value — so a real
        # arithmetic mistake (e.g. a multiply silently becoming a divide in
        # the predicted_diaas formula) could pass every existing test. This
        # uses a sparse nutrient profile (only protein_g/methionine/cystine
        # present, everything else literally absent — not just zero, since
        # get_aa_gaps() skips a key that's missing entirely) so every number
        # in the formula can be derived by hand instead of just asserted
        # against the function's own output.
        base = {"protein_g": 10.0, "aa_methionine_g": 0.10, "aa_cystine_g": 0.06}
        cand = {"protein_g": 100.0, "aa_methionine_g": 1.5, "aa_cystine_g": 1.5}
        base_gaps = get_aa_gaps(base, digestibility=1.0)
        assert [g[0] for g in base_gaps] == ["aa_methionine_g"]  # only AA present

        result = _score_one_complement(base, base_gaps, 1.0, cand, 0.5, "aa_methionine_g")
        assert result is not None

        # alpha=(1.5+1.5)/100=0.03, beta=1.0, R=23/1000=0.023, denom=0.007
        # base_aa=0.10+0.06=0.16, base_protein=10
        # grams=(0.023*10-0.16)/0.007=(0.23-0.16)/0.007=10.0 exactly
        assert result["grams"] == 10
        assert result["closes_primary"] is True
        assert result["opens_new_gap"] is False
        assert result["remaining_gaps"] == 0
        assert result["protein_added"] == pytest.approx(10.0)          # 100*10/100
        assert result["digestible_protein_added"] == pytest.approx(5.0)  # 10*0.5
        assert result["comp_nutrients"] == cand

        # predicted_diaas: only methionine+cystine contributes (every other
        # essential AA is absent from both base and cand, so skipped by the
        # "base_aa<=0 and comp_aa<=0: continue" guard) —
        # combined_protein = 10 + 100*(10/100) = 20
        # base_aa=0.16, comp_aa=(1.5+1.5)*10/100=0.30, ref_g=23/1000*20=0.46
        # predicted_diaas = (0.16*1.0 + 0.30*0.5) / 0.46
        expected_predicted_diaas = (0.16 * 1.0 + 0.30 * 0.5) / 0.46
        assert result["predicted_diaas"] == pytest.approx(expected_predicted_diaas)

    def test_denom_exactly_zero_returns_none(self):
        # Candidate's AA/protein ratio exactly equals the reference ratio —
        # the boundary the "denom <= 0" guard exists for. A previous survivor
        # (a mutation-testing pass changed it to "denom < 0") let exactly
        # this case fall through into a division by zero instead of the
        # documented None return.
        base = {"protein_g": 10.0, "aa_methionine_g": 0.10, "aa_cystine_g": 0.06}
        # protein=100 -> beta=1.0; methionine+cystine=2.3 -> alpha=0.023=R*beta exactly
        cand = {"protein_g": 100.0, "aa_methionine_g": 2.3, "aa_cystine_g": 0.0}
        base_gaps = get_aa_gaps(base, digestibility=1.0)
        assert _score_one_complement(base, base_gaps, 1.0, cand, 0.5, "aa_methionine_g") is None

    def test_grams_exactly_zero_returns_none(self):
        # Boundary for the "grams <= 0 or grams > MAX_PRACTICAL_GAP_CLOSER_GRAMS"
        # guard. Chosen so the solved (unrounded) grams is exactly 0.0: base
        # already sits exactly at the reference ratio for lysine
        # (R*base_protein == base_aa), so no additional grams are needed. A
        # mutation changing "or" to "and" makes this guard unsatisfiable (grams
        # can never be both <=0 and over the cap at once) and a mutation
        # changing "<=" to "<" both let this case fall through into a spurious
        # zero-grams "result" instead of the documented None.
        base = {"protein_g": 10.0, "aa_lysine_g": 0.48}  # R=0.048 * 10 = 0.48 exactly
        cand = {"protein_g": 100.0, "aa_lysine_g": 6.0}
        gaps = get_aa_gaps(base)
        assert _score_one_complement(base, gaps, 1.0, cand, 0.5, "aa_lysine_g") is None

    def test_grams_over_practical_cap_returns_none(self):
        # The other half of the same guard: a huge base deficit relative to
        # a candidate whose ratio barely exceeds the reference solves for
        # grams far past MAX_PRACTICAL_GAP_CLOSER_GRAMS — the practical
        # single-serving cap (a food that only marginally clears the reference
        # ratio needs an implausibly large amount to close the gap; see
        # usda_nutrients.MAX_PRACTICAL_GAP_CLOSER_GRAMS's docstring).
        base = {"protein_g": 500.0, "aa_lysine_g": 1.0}
        cand = {"protein_g": 100.0, "aa_lysine_g": 4.9}
        gaps = get_aa_gaps(base)
        assert _score_one_complement(base, gaps, 1.0, cand, 0.5, "aa_lysine_g") is None

    def test_grams_at_practical_cap_boundary(self):
        # Exact-boundary counterpart to test_grams_over_practical_cap_returns_none:
        # solved grams lands exactly at MAX_PRACTICAL_GAP_CLOSER_GRAMS, which must
        # still qualify (the guard is "> cap", not ">= cap"). Catches a mutation
        # changing "> MAX_PRACTICAL_GAP_CLOSER_GRAMS" to ">=".
        # alpha=0.049, beta=1.0, R=0.048, denom=0.001
        # base_aa=0.20, base_protein=10 -> grams=(0.048*10-0.20)/0.001=280... too high;
        # solve directly for grams==200: base_aa chosen so
        # (R*base_protein - base_aa)/denom == MAX_PRACTICAL_GAP_CLOSER_GRAMS exactly.
        base_protein = 10.0
        cand = {"protein_g": 100.0, "aa_lysine_g": 4.9}  # alpha=0.049, beta=1.0
        R = 0.048
        denom = 0.049 - R * 1.0  # 0.001
        base_aa = R * base_protein - denom * _usda.MAX_PRACTICAL_GAP_CLOSER_GRAMS
        base = {"protein_g": base_protein, "aa_lysine_g": base_aa}
        gaps = get_aa_gaps(base)
        result = _score_one_complement(base, gaps, 1.0, cand, 0.5, "aa_lysine_g")
        assert result is not None
        assert result["grams"] == _usda.MAX_PRACTICAL_GAP_CLOSER_GRAMS

    def test_R_uses_digestibility_divide_not_multiply(self):
        # R = AA_REFERENCE/1000/max(base_digestibility, 0.01). A mutation
        # changing that "/" to "*" survived every prior test because they
        # all used base_digestibility=1.0, where divide and multiply by 1
        # are indistinguishable. base_digestibility=0.5 here makes the two
        # formulas diverge sharply — R=0.096 (divide) vs R=0.024 (multiply)
        # — cascading into a completely different grams/predicted_diaas.
        base = {"protein_g": 10.0, "aa_lysine_g": 0.05}
        cand = {"protein_g": 100.0, "aa_lysine_g": 10.0}
        bd = 0.5
        gaps = get_aa_gaps(base, digestibility=bd)
        result = _score_one_complement(base, gaps, bd, cand, 0.5, "aa_lysine_g")
        assert result is not None
        assert result["grams"] == 227
        assert result["predicted_diaas"] == pytest.approx(1.0)

    def test_predicted_diaas_guard_rejects_pairing_below_base_digestibility(self):
        # The final guard rejects a candidate whose predicted pooled DIAAS
        # would fall below the base meal's own digestibility — but only
        # when base_digestibility < 1.0 (every other test in this class
        # uses the 1.0 default, where the guard is a no-op by design). A
        # mutation flipping "is not None" to "is None" here, or "<" to
        # "<=", survived because nothing exercised the actual rejection
        # path. This candidate closes the lysine gap in raw terms but its
        # own poor digestibility (0.2) drags the pooled prediction (~0.21)
        # below the base's 0.9 — must be rejected.
        base = {
            "protein_g": 10.0, "aa_lysine_g": 0.30,
            "aa_methionine_g": 0.10, "aa_cystine_g": 0.06,
        }
        bd = 0.9
        cand = {
            "protein_g": 100.0, "aa_lysine_g": 6.0,
            "aa_methionine_g": 0.5, "aa_cystine_g": 0.5,
        }
        gaps = get_aa_gaps(base, digestibility=bd)
        assert _score_one_complement(base, gaps, bd, cand, 0.2, "aa_lysine_g") is None

    def test_dig_scores_includes_aa_present_in_either_food_not_only_both(self):
        # predicted_diaas's per-AA loop skips an AA only when it's absent
        # from BOTH base and candidate ("base_aa <= 0 and comp_aa <= 0:
        # continue"). A mutation changing that "and" to "or" survived
        # every prior test because none of them used a candidate carrying
        # an essential AA the base lacks entirely. Here the candidate adds
        # threonine (absent from base) with a low enough ratio to become
        # the new minimum, so its ratio — not lysine's — determines
        # predicted_diaas; the "or" mutant would wrongly skip it.
        base = {"protein_g": 10.0, "aa_lysine_g": 0.10}
        cand = {"protein_g": 100.0, "aa_lysine_g": 6.0, "aa_threonine_g": 0.02}
        gaps = get_aa_gaps(base)
        result = _score_one_complement(base, gaps, 1.0, cand, 0.5, "aa_lysine_g")
        assert result is not None
        assert result["predicted_diaas"] == pytest.approx(0.00304)

    def test_comp_dig_defaults_to_1_not_2_when_cand_diaas_is_none(self):
        # Both dig_added's and predicted_diaas's fallback for a candidate
        # with no known DIAAS score is documented as 1.0 (assume fully
        # digestible absent better data). A mutation changing either
        # fallback to 2.0 survived because no test here passed
        # cand_diaas=None while also checking an exact dependent value.
        base = {"protein_g": 10.0, "aa_lysine_g": 0.10}
        cand = {"protein_g": 100.0, "aa_lysine_g": 6.0}
        gaps = get_aa_gaps(base)
        result = _score_one_complement(base, gaps, 1.0, cand, None, "aa_lysine_g")
        assert result is not None
        assert result["digestible_protein_added"] == pytest.approx(result["protein_added"])
        assert result["predicted_diaas"] == pytest.approx(1.0)

    def test_closes_primary_false_when_base_gaps_empty(self):
        # closes_primary's ternary has a documented else-branch (False when
        # base_gaps is empty) that every other test in this class never
        # exercises, since they all pass a real, non-empty gaps list. A
        # mutation flipping that else-value to True survived undetected.
        base = {"protein_g": 10.0, "aa_lysine_g": 0.10}
        cand = {"protein_g": 100.0, "aa_lysine_g": 6.0}
        result = _score_one_complement(base, [], 1.0, cand, 0.5, "aa_lysine_g")
        assert result is not None
        assert result["closes_primary"] is False

    # NOTE: a mutation-testing pass (TESTING-ROADMAP.md item #5) found that
    # dropping the `digestibility=base_digestibility` kwarg on the internal
    # protein_completeness() call survives every test here. An attempted fix
    # (comparing new_scores at two digestibility levels) turned out to rest
    # on a wrong premise: new_scores are documented as always RAW
    # (pre-digestibility) — digestibility only affects protein_completeness()'s
    # internal "complete"/"limiting_aa" determination, not the scores dict
    # itself. A clean, non-flaky test for that narrower effect wasn't found
    # in the time available (the target AA's own solved score sits right at
    # a floating-point boundary by construction, and "limiting_aa" doesn't
    # change with digestibility since it scales every AA's score equally).
    # Left as a real, known, unresolved gap rather than a fragile test.


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
            for key in ("name", "grams", "protein_added", "dig_added",
                        "fdc_id", "recipe_id", "serving_weight_g", "diaas", "comp_nutrients"):
                assert key in f, f"Missing food key: {key}"
        # comp_nutrients must carry the actual nutrient dict used to score
        # this food, not None/a placeholder — several dict-key-literal
        # mutations on this field survived because no test checked it.
        for f in result["pairs"][0]["foods"]:
            assert f["comp_nutrients"] is not None
            assert f["comp_nutrients"].get("protein_g", 0) > 0

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

    def test_rejected_second_leg_does_not_abort_the_whole_search(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found the
        # "continue" in "if b_m['remaining_gaps'] > 0 or b_m['opens_new_gap']:
        # continue" had a survived mutation to "break" — which would abandon
        # the search for a valid second leg entirely the moment ANY
        # candidate fails, instead of trying the next one. B_Bad (pure
        # lysine, dilutes every other AA) is placed in pantry BEFORE B_Good
        # (a well-rounded profile that fully closes the cascade) so the
        # inner loop must reject B_Bad and continue on to find B_Good.
        base = {
            "protein_g":          20.0,
            "aa_tryptophan_g":    0.20, "aa_threonine_g":     0.60,
            "aa_isoleucine_g":    0.80, "aa_leucine_g":       1.40,
            "aa_lysine_g":        0.924,
            "aa_methionine_g":    0.200, "aa_cystine_g":       0.108,
            "aa_phenylalanine_g": 0.90, "aa_valine_g":        0.90,
            "aa_histidine_g":     0.40,
        }
        a = {"name": "A_Brazil", "diaas": 0.54, "nutrients": {
            "protein_g": 14.32, "aa_methionine_g": 1.008, "aa_cystine_g": 0.342,
            "aa_lysine_g": 0.492, "aa_tryptophan_g": 0.141, "aa_threonine_g": 0.362,
            "aa_isoleucine_g": 0.516, "aa_leucine_g": 1.155, "aa_phenylalanine_g": 0.630,
            "aa_valine_g": 0.756, "aa_histidine_g": 0.235,
        }}
        b_bad = {"name": "B_Bad", "diaas": None,
                 "nutrients": {"protein_g": 100.0, "aa_lysine_g": 5.0}}
        b_good = {"name": "B_Good", "diaas": None, "nutrients": {
            "protein_g": 86.04, "aa_methionine_g": 1.145, "aa_cystine_g": 0.833,
            "aa_lysine_g": 5.379, "aa_tryptophan_g": 1.143, "aa_threonine_g": 3.579,
            "aa_isoleucine_g": 4.382, "aa_leucine_g": 7.133, "aa_phenylalanine_g": 4.870,
            "aa_valine_g": 4.487, "aa_histidine_g": 2.425,
        }}

        result = _usda.suggest_complements(base, [a, b_bad, b_good])
        pair_keys = [frozenset(f["name"] for f in p["foods"]) for p in result["pairs"]]
        assert frozenset(["A_Brazil", "B_Good"]) in pair_keys, (
            "B_Good must still be found as A_Brazil's second leg even though "
            "B_Bad (which fails the accept check) comes first in candidate order"
        )
        assert frozenset(["A_Brazil", "B_Bad"]) not in pair_keys

    def test_pair_summary_fields_match_independent_two_leg_recompute(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found every
        # test above only checks structure/relationships (right keys,
        # sorted order, no duplicates) — none pins an exact value on
        # total_protein_added/total_dig_added/predicted_diaas/new_complete/
        # new_scores, so a dict-key-literal or rounding mutation on any of
        # them would survive undetected. This independently recomputes both
        # legs via direct _score_one_complement() calls (the same building
        # blocks _build_pairs() itself uses) and cross-checks every
        # pair-level summary field against them.
        from usda_nutrients import scale_nutrients, sum_nutrients
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [])
        assert result["pairs"]
        pair = result["pairs"][0]
        a, b = pair["foods"]

        gaps = get_aa_gaps(_PAIR_CASCADE_NUTRIENTS)
        primary_aa = gaps[0][0]
        a_nutrients = _usda.get_complement_nutrients(a["name"])
        assert a_nutrients is not None
        a_m = _score_one_complement(
            _PAIR_CASCADE_NUTRIENTS, gaps, 1.0, a_nutrients, a["diaas"], primary_aa,
        )
        assert a_m is not None
        assert a["grams"] == a_m["grams"]

        combined_after_a = sum_nutrients(
            _PAIR_CASCADE_NUTRIENTS, scale_nutrients(a_nutrients, a_m["grams"])
        )
        gaps_after_a = get_aa_gaps(combined_after_a)
        b_target_aa = gaps_after_a[0][0]
        b_nutrients = _usda.get_complement_nutrients(b["name"])
        assert b_nutrients is not None
        b_m = _score_one_complement(
            combined_after_a, gaps_after_a, 1.0, b_nutrients, b["diaas"], b_target_aa,
        )
        assert b_m is not None
        assert b["grams"] == b_m["grams"]

        a_prot = a_nutrients.get("protein_g", 0) * a_m["grams"] / 100
        b_prot = b_nutrients.get("protein_g", 0) * b_m["grams"] / 100
        a_dig = a_prot * (a["diaas"] if a["diaas"] is not None else 1.0)
        b_dig = b_prot * (b["diaas"] if b["diaas"] is not None else 1.0)

        assert pair["total_protein_added"] == pytest.approx(round(a_prot + b_prot, 1))
        assert pair["total_dig_added"] == pytest.approx(round(a_dig + b_dig, 1))
        assert pair["new_complete"] == b_m["new_complete"]
        assert pair["new_scores"] == b_m["new_scores"]
        assert pair["predicted_diaas"] == b_m.get("predicted_diaas")
        assert pair["gaps_closed"] == (b_m["remaining_gaps"] == 0)
        # Per-leg fields — a survived "round(a_dig, None)" mutation (which
        # rounds to the nearest int instead of 1 decimal place) wasn't
        # caught by the total-level checks above alone.
        assert a["protein_added"] == pytest.approx(round(a_prot, 1))
        assert a["dig_added"] == pytest.approx(round(a_dig, 1))
        assert b["protein_added"] == pytest.approx(round(b_prot, 1))
        assert b["dig_added"] == pytest.approx(round(b_dig, 1))

    def test_pantry_sourced_pairs_candidate_fields_reflect_input(self):
        # _build_pairs()'s OWN candidate-pool resolution (all_candidates_ordered)
        # re-extracts fdc_id/recipe_id/serving_weight_g from the pantry
        # input via its own separate .get() calls — a distinct code path
        # from _build_suggestions's identically-named field extraction
        # tested elsewhere, with its own separate dict-key-literal
        # mutations that survived. A pantry food with nutrients=None
        # (forcing the curated-table fallback inside this same
        # candidate-pool-building loop) matching "Lentils, cooked" by
        # name, carrying explicit identifying fields, must show up with
        # those exact fields intact wherever it appears as a pair leg.
        # diaas=0.99 (truthy) plus the curated-table fallback (nutrients=None)
        # also exercises the "cand_d = cand_d or entry['diaas']" line here —
        # a survived "or"->"and" mutation would silently replace 0.99 with
        # the curated table's own generic diaas instead of preserving it.
        pantry = [{"name": "Lentils, cooked", "nutrients": None, "diaas": 0.99,
                   "fdc_id": 777, "recipe_id": 55, "serving_weight_g": 123.4}]
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, pantry)
        assert result["pairs"]
        matches = [f for p in result["pairs"] for f in p["foods"] if f["name"] == "Lentils, cooked"]
        assert matches, "Lentils, cooked (pantry-sourced) should appear as a pair leg"
        for f in matches:
            assert f["fdc_id"] == 777
            assert f["recipe_id"] == 55
            assert f["serving_weight_g"] == 123.4
            assert f["diaas"] == 0.99

    def test_pantry_sourced_leg_a_fields_reflect_input(self):
        # The test above's candidate only ever lands as leg B (the second
        # food). cand_a's own separate field extraction, a few lines
        # earlier in the same function, had several of the same class of
        # survived mutation (a_diaas forced to None, a_recipe_id/
        # a_serving_wt key-literal mutations) that a B-only test can't
        # reach. This candidate mirrors Brazil nuts' real profile (which
        # reliably lands as leg A against _PAIR_CASCADE_NUTRIENTS) so it's
        # guaranteed to be scored as leg A instead.
        pantry = [{"name": "MyBrazilClone", "diaas": 0.77,
                   "fdc_id": 888, "recipe_id": 66, "serving_weight_g": 45.6,
                   "nutrients": {
                       "protein_g": 14.32, "aa_methionine_g": 1.008, "aa_cystine_g": 0.342,
                       "aa_lysine_g": 0.492, "aa_tryptophan_g": 0.141, "aa_threonine_g": 0.362,
                       "aa_isoleucine_g": 0.516, "aa_leucine_g": 1.155, "aa_phenylalanine_g": 0.630,
                       "aa_valine_g": 0.756, "aa_histidine_g": 0.235,
                   }}]
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, pantry)
        assert result["pairs"]
        a_leg = next(p["foods"][0] for p in result["pairs"] if p["foods"][0]["name"] == "MyBrazilClone")
        assert a_leg["diaas"] == 0.77
        assert a_leg["fdc_id"] == 888
        assert a_leg["recipe_id"] == 66
        assert a_leg["serving_weight_g"] == 45.6

    def test_leg_b_dig_added_defaults_diaas_to_one_not_two(self):
        # "b_dig = b_prot * (b_diaas if b_diaas is not None else 1.0)" had
        # a survived mutation changing that fallback to 2.0. Every prior
        # pairs test's B leg resolved to a real (non-None) diaas via the
        # curated table, masking this. This candidate has real nutrients
        # (skips the curated-table fallback) but no diaas and no
        # curated-table name match, so its true diaas is None.
        pantry = [{"name": "ZZZ Unknown Soy Blend", "diaas": None, "nutrients": {
            "protein_g": 86.04, "aa_methionine_g": 1.145, "aa_cystine_g": 0.833,
            "aa_lysine_g": 5.379, "aa_tryptophan_g": 1.143, "aa_threonine_g": 3.579,
            "aa_isoleucine_g": 4.382, "aa_leucine_g": 7.133, "aa_phenylalanine_g": 4.870,
            "aa_valine_g": 4.487, "aa_histidine_g": 2.425,
        }}]
        result = _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, pantry)
        assert result["pairs"]
        matches = [f for p in result["pairs"] for f in p["foods"] if f["name"] == "ZZZ Unknown Soy Blend"]
        assert matches
        for f in matches:
            assert f["diaas"] is None
            assert f["dig_added"] == pytest.approx(f["protein_added"])


# ---------------------------------------------------------------------------
# suggest_complements — diaas_improvers tier (_diaas_improver_score, a
# module-internal closure with no direct entry point — tested only through
# suggest_complements()'s "diaas_improvers" output key). A mutation-testing
# pass (TESTING-ROADMAP.md item #5) found this ~95-line closure had ZERO
# test coverage of any kind before this class — not even a smoke test
# confirming the tier ever produces output.
# ---------------------------------------------------------------------------

class TestDiaasImprovers:
    # Candidate whose every essential AA sits EXACTLY at the FAO reference
    # ratio (mg AA / g protein) — this makes _score_one_complement's
    # denom == 0 for every possible target AA, so the gap-closer path
    # always returns None and the candidate falls through to the
    # diaas-improver path instead. Its name deliberately matches no
    # keyword in diaas.py's digestibility table, so get_digestibility()
    # falls through to the 0.82 overall default — a known, fixed value.
    _REF_EXACT_CANDIDATE = {"protein_g": 100.0}
    from usda_api import AA_REFERENCE_MG_PER_G_PROTEIN as _REF
    for _aa, _ref in _REF.items():
        _REF_EXACT_CANDIDATE[_aa] = _ref / 10.0  # mg/g protein -> g/100g @ 100g protein/100g food
    _REF_EXACT_CANDIDATE["aa_cystine_g"] = 0.0
    _REF_EXACT_CANDIDATE["aa_tyrosine_g"] = 0.0
    del _aa, _ref, _REF

    _BASE = {
        "protein_g": 10.0,
        "aa_tryptophan_g": 0.05, "aa_threonine_g": 0.15,
        "aa_isoleucine_g": 0.20, "aa_leucine_g": 0.35,
        "aa_lysine_g": 0.25, "aa_methionine_g": 0.05, "aa_cystine_g": 0.03,
        "aa_phenylalanine_g": 0.25, "aa_valine_g": 0.25, "aa_histidine_g": 0.10,
    }

    def _independent_pooled_diaas(self, X, comp_name="ZZZ Test Complement"):
        # Reimplements the documented formula from _diaas_improver_score's
        # own docstring, independently of the (inaccessible — it's a
        # closure, not a module-level function) implementation, using the
        # same base_tid/d_comp sources it does.
        import diaas as _diaas
        base_tid = 1.0  # base_food_name not passed -> falls back to base_digestibility (1.0 default)
        d_comp, _ = _diaas.get_digestibility(comp_name)
        base_protein = self._BASE["protein_g"]
        comp_protein = self._REF_EXACT_CANDIDATE["protein_g"]
        Q = comp_protein / 100.0
        new_protein = base_protein + Q * X
        ratios = {}
        for aa_key, ref_mg_per_g in _diaas.FAO_REFERENCE.items():
            secondary = _diaas._IAA_PAIRS.get(aa_key)
            base_aa = self._BASE.get(aa_key, 0.0)
            comp_aa = self._REF_EXACT_CANDIDATE.get(aa_key, 0.0)
            if secondary:
                base_aa += self._BASE.get(secondary, 0.0)
                comp_aa += self._REF_EXACT_CANDIDATE.get(secondary, 0.0)
            if base_aa <= 0 and comp_aa <= 0:
                continue
            pooled = base_aa * base_tid + comp_aa / 100.0 * X * d_comp
            ref_g = ref_mg_per_g / 1000.0 * new_protein
            if ref_g > 0:
                ratios[aa_key] = pooled / ref_g
        return min(ratios.values()) if ratios else 0.0

    def test_reference_exact_candidate_never_qualifies_as_gap_closer(self):
        # Sanity check on the scenario's own construction: denom == 0 for
        # every AA means _score_one_complement must reject this candidate
        # for every gap, so it can only appear in diaas_improvers, never
        # in pantry/general.
        pantry = [{"name": "ZZZ Test Complement", "nutrients": self._REF_EXACT_CANDIDATE, "diaas": None}]
        result = _usda.suggest_complements(self._BASE, pantry)
        assert result["pantry"] == []

    def test_current_diaas_matches_independent_pooled_formula_at_zero_grams(self):
        pantry = [{"name": "ZZZ Test Complement", "nutrients": self._REF_EXACT_CANDIDATE, "diaas": None}]
        result = _usda.suggest_complements(self._BASE, pantry)
        assert len(result["diaas_improvers"]) == 1
        imp = result["diaas_improvers"][0]
        expected_current = self._independent_pooled_diaas(0.0)
        assert imp["current_diaas"] == pytest.approx(round(expected_current, 2))

    def test_steps_and_new_diaas_match_independent_pooled_formula(self):
        pantry = [{"name": "ZZZ Test Complement", "nutrients": self._REF_EXACT_CANDIDATE, "diaas": None}]
        result = _usda.suggest_complements(self._BASE, pantry)
        imp = result["diaas_improvers"][0]
        # Every reported step's new_diaas must match the independently
        # recomputed pooled DIAAS at that exact gram amount — catches
        # arithmetic mutations anywhere in the pooling/ratio formula.
        for step in imp["steps"]:
            expected = self._independent_pooled_diaas(step["grams"])
            assert step["new_diaas"] == pytest.approx(round(expected, 2))
            expected_dcp = round((10.0 + 1.0 * step["grams"]) * min(1.0, expected), 1)
            assert step["dcp"] == pytest.approx(expected_dcp)
        # The ranking fields mirror the last (largest/best) step.
        assert imp["grams"] == imp["steps"][-1]["grams"]
        assert imp["new_diaas"] == imp["steps"][-1]["new_diaas"]

    def test_protein_and_digestible_protein_added_use_best_step_grams(self):
        pantry = [{"name": "ZZZ Test Complement", "nutrients": self._REF_EXACT_CANDIDATE, "diaas": None}]
        result = _usda.suggest_complements(self._BASE, pantry)
        imp = result["diaas_improvers"][0]
        best_grams = imp["steps"][-1]["grams"]
        # comp_diaas_val is None here, so dig_added falls back to d_comp
        # (0.82, the overall default — this candidate's name matches no
        # digestibility-table keyword).
        expected_protein_added = 1.0 * best_grams  # Q=1.0 (100g protein/100g food)
        assert imp["protein_added"] == pytest.approx(expected_protein_added)
        assert imp["digestible_protein_added"] == pytest.approx(expected_protein_added * 0.82)
        # A dict-key-literal mutation on "diaas" (-> a differently-spelled
        # key) survived because no test checked this field's identity.
        assert imp["diaas"] is None

    def test_no_improvers_when_base_already_meets_target(self):
        # current_diaas_val >= target(0.90) -> returns None immediately,
        # before any of the step-search logic runs at all. Tryptophan sits
        # at score 0.917 — a real gap (below the 0.95 get_aa_gaps()
        # threshold, so suggest_complements doesn't early-return) but still
        # above the diaas-improver tier's separate 0.90 pooled-DIAAS target.
        near_complete = {
            "protein_g": 20.0,
            "aa_tryptophan_g": 0.121, "aa_threonine_g": 0.60,
            "aa_isoleucine_g": 0.80, "aa_leucine_g": 1.40,
            "aa_lysine_g": 1.00, "aa_methionine_g": 0.50, "aa_cystine_g": 0.30,
            "aa_phenylalanine_g": 0.90, "aa_valine_g": 0.90, "aa_histidine_g": 0.40,
        }
        gaps = get_aa_gaps(near_complete)
        assert gaps, "need at least one small gap so suggest_complements doesn't early-return"
        pantry = [{"name": "ZZZ Test Complement", "nutrients": self._REF_EXACT_CANDIDATE, "diaas": None}]
        result = _usda.suggest_complements(near_complete, pantry)
        assert result["diaas_improvers"] == []

    def test_base_food_name_looks_up_real_tid_instead_of_base_digestibility(self):
        # base_tid (used only by the diaas-improver tier) is looked up from
        # base_food_name via diaas.get_digestibility() when given, falling
        # back to base_digestibility only when base_food_name is None — no
        # existing test ever passed base_food_name to suggest_complements,
        # so a mutation always using the base_digestibility fallback (or
        # never taking the lookup branch at all) would survive undetected.
        # "My Lentil Soup" keyword-matches the curated digestibility table
        # (0.83), distinct from base_digestibility=1.0 passed alongside it.
        pantry = [{"name": "ZZZ Test Complement", "nutrients": self._REF_EXACT_CANDIDATE, "diaas": None}]
        result = _usda.suggest_complements(
            self._BASE, pantry, base_digestibility=1.0, base_food_name="My Lentil Soup",
        )
        imp = result["diaas_improvers"][0]
        expected = self._independent_pooled_diaas(0.0)  # uses base_tid=1.0 by default
        assert imp["current_diaas"] != pytest.approx(round(expected, 2)), (
            "current_diaas should differ from the base_digestibility=1.0 fallback "
            "value once a real base_food_name with a different curated TID is given"
        )
        # Independent recompute using the real base_tid this time.
        import diaas as _diaas
        base_tid, _ = _diaas.get_digestibility("My Lentil Soup")
        assert base_tid != 1.0
        ratios = {}
        for aa_key, ref_mg_per_g in _diaas.FAO_REFERENCE.items():
            secondary = _diaas._IAA_PAIRS.get(aa_key)
            base_aa = self._BASE.get(aa_key, 0.0)
            if secondary:
                base_aa += self._BASE.get(secondary, 0.0)
            if base_aa <= 0:
                continue
            ref_g = ref_mg_per_g / 1000.0 * self._BASE["protein_g"]
            if ref_g > 0:
                ratios[aa_key] = (base_aa * base_tid) / ref_g
        assert imp["current_diaas"] == pytest.approx(round(min(ratios.values()), 2))

    def test_max_improver_grams_kwarg_actually_passed_through(self):
        # suggest_complements()'s max_improver_grams kwarg had a survived
        # mutation dropping it from the internal _diaas_improver_score()
        # call entirely, silently falling back to that function's own
        # default (300) regardless of what the caller asked for. The
        # docstring explicitly promises 120 for meal/food/daily contexts
        # vs 300 for recipe contexts — a real, user-visible difference.
        pantry = [{"name": "ZZZ Test Complement", "nutrients": self._REF_EXACT_CANDIDATE, "diaas": None}]
        r120 = _usda.suggest_complements(self._BASE, pantry, max_improver_grams=120)
        r300 = _usda.suggest_complements(self._BASE, pantry, max_improver_grams=300)
        assert r120["diaas_improvers"][0]["grams"] == 120
        assert r300["diaas_improvers"][0]["grams"] == 300

    def test_secondary_aa_is_added_not_subtracted_in_pooled_formula(self):
        # _pooled_diaas()'s comp_aa accumulation for a paired AA (Met+Cys,
        # Phe+Tyr) had a survived "+="->"-=" mutation. self._REF_EXACT_CANDIDATE
        # zeros out cystine/tyrosine entirely (so the bug is unreachable
        # through it), masking this for every existing test in this class.
        # This candidate splits the same total methionine+cystine ratio
        # across both keys instead of putting it all on methionine — the
        # correctly-summed result must be identical to the all-methionine
        # version (0.35 at zero grams, matching test_current_diaas_...).
        from usda_api import AA_REFERENCE_MG_PER_G_PROTEIN as _REF
        split_candidate = {"protein_g": 100.0}
        for aa, ref in _REF.items():
            split_candidate[aa] = ref / 10.0
        met_total = split_candidate["aa_methionine_g"]
        split_candidate["aa_methionine_g"] = met_total * 0.6
        split_candidate["aa_cystine_g"] = met_total * 0.4
        split_candidate["aa_tyrosine_g"] = 0.0

        pantry = [{"name": "ZZZ Test Complement", "nutrients": split_candidate, "diaas": None}]
        result = _usda.suggest_complements(self._BASE, pantry)
        assert result["diaas_improvers"]
        imp = result["diaas_improvers"][0]
        assert imp["current_diaas"] == pytest.approx(0.35)


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

    def test_protein_isolate_and_concentrate_have_density(self):
        """Regression test: user-reported bug — "Soy protein isolate" had no
        density data, so volume units (e.g. "2 T") were rejected."""
        assert _usda.get_density_g_per_ml("Soy protein isolate", []) == pytest.approx(0.50)
        assert _usda.get_density_g_per_ml("Pea protein concentrate", []) == pytest.approx(0.50)

    # -----------------------------------------------------------------
    # USDA-portion fallback path — a mutation-testing pass (TESTING-ROADMAP.md
    # item #5) found this whole function had 53 survivors despite the
    # keyword-table tests above; almost all of them were in the portion-
    # parsing fallback below, which had only one narrow test
    # (test_usda_tablespoon_portion_used) exercising it at all.
    # -----------------------------------------------------------------

    def test_fraction_count_parsed_correctly(self):
        # "1/2 cup" -> count=0.5, not 1.0 (a mutation swapping the
        # numerator/denominator division, or falling back to the plain
        # decimal regex which wouldn't match "1/2" as a whole, would
        # silently mis-parse this).
        portions = [{"description": "1/2 cup", "gram_weight": 118.3}]
        density = _usda.get_density_g_per_ml("Unknown Food A", portions)
        assert density == pytest.approx(118.3 / (0.5 * 236.6))

    def test_capital_T_abbreviation_means_tablespoon(self):
        portions = [{"description": "1 T", "gram_weight": 14.8}]
        density = _usda.get_density_g_per_ml("Unknown Food B", portions)
        assert density == pytest.approx(14.8 / 14.8)

    def test_lowercase_t_abbreviation_means_teaspoon(self):
        portions = [{"description": "1 t", "gram_weight": 4.9}]
        density = _usda.get_density_g_per_ml("Unknown Food C", portions)
        assert density == pytest.approx(4.9 / 4.9)

    def test_lowercase_c_abbreviation_means_cup(self):
        portions = [{"description": "1 c", "gram_weight": 236.6}]
        density = _usda.get_density_g_per_ml("Unknown Food D", portions)
        assert density == pytest.approx(1.0)

    def test_missing_leading_number_defaults_count_to_one(self):
        portions = [{"description": "cup", "gram_weight": 236.6}]
        density = _usda.get_density_g_per_ml("Unknown Food E", portions)
        assert density == pytest.approx(236.6 / 236.6)

    def test_zero_gram_weight_portion_is_skipped(self):
        portions = [{"description": "1 cup", "gram_weight": 0}]
        assert _usda.get_density_g_per_ml("Unknown Food F", portions) is None

    def test_out_of_bounds_density_falls_through_to_next_portion(self):
        # First portion's implied density (1000g/236.6ml ≈ 4.2 g/ml) is
        # outside the plausible 0.15-1.6 g/ml range and must be rejected —
        # not returned, and not treated as a hard stop; the loop must
        # continue on to the next portion, which is plausible.
        portions = [
            {"description": "1 cup", "gram_weight": 1000.0},
            {"description": "1 tablespoon", "gram_weight": 15.0},
        ]
        density = _usda.get_density_g_per_ml("Unknown Food G", portions)
        assert density == pytest.approx(15.0 / 14.8)

    def test_fl_oz_keyword_recognized(self):
        portions = [{"description": "1 fl oz", "gram_weight": 29.6}]
        density = _usda.get_density_g_per_ml("Unknown Food H", portions)
        assert density == pytest.approx(1.0)

    def test_teaspoon_full_word_and_tbs_abbreviation_recognized(self):
        portions_tsp = [{"description": "1 teaspoon", "gram_weight": 4.9}]
        assert _usda.get_density_g_per_ml("Unknown Food I", portions_tsp) == pytest.approx(1.0)
        portions_tbs = [{"description": "1 tbs", "gram_weight": 14.8}]
        assert _usda.get_density_g_per_ml("Unknown Food J", portions_tbs) == pytest.approx(1.0)

    def test_none_portions_returns_none_not_crash(self):
        assert _usda.get_density_g_per_ml("Unknown Food K", None) is None

    def test_portion_with_no_volume_keyword_is_ignored(self):
        # A description with no recognized volume word (e.g. "1 container")
        # contributes nothing and must not crash or be mistaken for a match.
        portions = [{"description": "1 container", "gram_weight": 200.0}]
        assert _usda.get_density_g_per_ml("Unknown Food L", portions) is None

    def test_multiplier_count_scales_ml_correctly(self):
        # "2 tablespoons" -> count=2, so density = gw / (2 * 14.8), not
        # gw / 14.8 — a mutation dropping the count multiplier entirely
        # would give a density double the real value.
        portions = [{"description": "2 tablespoons", "gram_weight": 29.6}]
        density = _usda.get_density_g_per_ml("Unknown Food M", portions)
        assert density == pytest.approx(1.0)

    def test_tbsp_keyword_recognized(self):
        # A mutation-testing pass (TESTING-ROADMAP.md item #5) found "tbsp"
        # specifically (distinct from "tablespoon" and "tbs", both already
        # tested) had never been exercised.
        portions = [{"description": "1 tbsp", "gram_weight": 14.8}]
        density = _usda.get_density_g_per_ml("Unknown Food N", portions)
        assert density == pytest.approx(1.0)

    def test_tsp_keyword_recognized_unexpanded(self):
        # "tsp" as the literal keyword text (not via the "t" -> "teaspoon"
        # abbreviation expansion, which the existing lowercase-t test
        # already covers and which masks this keyword never being reached
        # directly).
        portions = [{"description": "2 tsp", "gram_weight": 9.8}]
        density = _usda.get_density_g_per_ml("Unknown Food O", portions)
        assert density == pytest.approx(9.8 / (2 * 4.9))

    def test_small_but_plausible_gram_weight_is_not_skipped(self):
        # The "gw <= 0" skip guard had a survived "gw <= 1" boundary
        # mutation — gram_weight=1 is a real, non-degenerate value (not
        # "missing/zero" data) that happens to yield a perfectly plausible
        # density (≈0.204 g/ml) for a teaspoon-sized portion; it must not
        # be treated as if it were zero/missing.
        portions = [{"description": "1 teaspoon", "gram_weight": 1.0}]
        density = _usda.get_density_g_per_ml("Unknown Food P", portions)
        assert density == pytest.approx(1.0 / 4.9)

    def test_zero_gram_weight_portion_does_not_abort_later_portions(self):
        # The "gw <= 0: continue" had a survived continue->break mutation —
        # a single bad (zero-weight) portion earlier in the list must not
        # prevent a later, valid portion from being used.
        portions = [
            {"description": "1 cup", "gram_weight": 0},
            {"description": "1 tablespoon", "gram_weight": 15.0},
        ]
        density = _usda.get_density_g_per_ml("Unknown Food Q", portions)
        assert density == pytest.approx(15.0 / 14.8)

    def test_density_bounds_are_inclusive_at_both_ends(self):
        # The "0.15 <= density <= 1.6" plausibility bounds had survived
        # mutations making either end exclusive, and a mutation widening
        # the upper bound to 2.6. Test both boundary values exactly
        # (inclusive — must be accepted) and a value between 1.6 and 2.6
        # (must be rejected, confirming the upper bound is really 1.6).
        assert _usda.get_density_g_per_ml(
            "Unknown Food R", [{"description": "1 tablespoon", "gram_weight": 2.22}]
        ) == pytest.approx(0.15)
        assert _usda.get_density_g_per_ml(
            "Unknown Food S", [{"description": "1 tablespoon", "gram_weight": 23.68}]
        ) == pytest.approx(1.6)
        assert _usda.get_density_g_per_ml(
            "Unknown Food T", [{"description": "1 tablespoon", "gram_weight": 29.6}]
        ) is None
