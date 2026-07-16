"""
Tests for numa_app/services/food_import.py — the shared per-serving conversion
and nutrient-key validation used by the Claude-import flow (workflows/foods.py),
import_foods.py, and import_json_folder.py.
"""
import pytest

from numa_app.services.food_import import VALID_NUTRIENT_KEYS, convert_per_serving, validate_and_strip


class TestValidNutrientKeys:
    def test_includes_omega_keys(self):
        # These were missing from the old hand-maintained key sets in both
        # foods.py and import_foods.py, despite being valid per CLAUDE.md.
        assert "omega3_ala_mg" in VALID_NUTRIENT_KEYS
        assert "omega3_epa_mg" in VALID_NUTRIENT_KEYS
        assert "omega3_dha_mg" in VALID_NUTRIENT_KEYS
        assert "omega6_la_mg" in VALID_NUTRIENT_KEYS

    def test_includes_macros_and_amino_acids(self):
        assert "calories" in VALID_NUTRIENT_KEYS
        assert "protein_g" in VALID_NUTRIENT_KEYS
        assert "aa_lysine_g" in VALID_NUTRIENT_KEYS
        assert "aa_cystine_g" in VALID_NUTRIENT_KEYS


class TestConvertPerServing:
    def test_scales_to_per_100g(self):
        # Triscuit Organic Original Crackers, 28g serving.
        per_serving = {"calories": 120, "protein_g": 3, "sodium_mg": 160}
        result = convert_per_serving(per_serving, 28)
        assert result["calories"] == pytest.approx(428.571, rel=1e-4)
        assert result["protein_g"] == pytest.approx(10.714, rel=1e-4)
        assert result["sodium_mg"] == pytest.approx(571.429, rel=1e-4)

    def test_100g_serving_is_identity(self):
        per_serving = {"calories": 200}
        assert convert_per_serving(per_serving, 100) == {"calories": 200}

    @pytest.mark.parametrize("bad_size", [0, -5])
    def test_rejects_non_positive_serving_size(self, bad_size):
        with pytest.raises(ValueError):
            convert_per_serving({"calories": 100}, bad_size)


class TestValidateAndStrip:
    def test_keeps_valid_numeric_keys(self):
        clean, stripped = validate_and_strip({"calories": 100, "protein_g": 5})
        assert clean == {"calories": 100.0, "protein_g": 5.0}
        assert stripped == []

    def test_strips_unknown_keys(self):
        clean, stripped = validate_and_strip({"calories": 100, "selenium_mcg": 40})
        assert clean == {"calories": 100.0}
        assert stripped == ["selenium_mcg"]

    def test_strips_non_numeric_values(self):
        clean, stripped = validate_and_strip({"calories": 100, "protein_g": "unknown"})
        assert clean == {"calories": 100.0}
        assert stripped == ["protein_g"]
