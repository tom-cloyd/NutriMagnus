"""
Tests for openfoodfacts.py — nutrient-key mapping and product parsing.
_parse_product()/get_food_detail() never touch the network (a search result
already embeds the product's own nutriment data), so nothing here needs
mocking beyond the module's own no_off autouse fixture (which only stubs
search_foods/lookup_by_barcode, not the parsing path used here).
"""

import pytest

import openfoodfacts as _off


class TestParseProduct:
    def _off_result(self, nutriments: dict, fdc_id: int = -2000000001) -> dict:
        return {"fdcId": fdc_id, "_off_data": {
            "product_name": "Test Product",
            "brands": "TestBrand,OtherBrand",
            "code": "1234567890",
            "serving_size": "30 g",
            "nutriments": nutriments,
        }}

    def test_maps_every_nutrient_key_to_the_canonical_name(self):
        # A mutation-testing-adjacent finding (TESTING-ROADMAP.md item #1,
        # 2026-09-11): carbohydrates_100g mapped to "carb_g", not the
        # canonical "carbs_g" used everywhere else in the app (usda_api.py's
        # NUTRIENT_MAP, cnf_api.py, CLAUDE.md's documented Nutrients Dict) —
        # every Open Food Facts food's carb value was silently unreadable
        # by the rest of the app. Caught only because a real fixture-
        # recording run surfaced it, not by any existing test. This test
        # pins every mapped key to its canonical name so a future typo like
        # this fails immediately instead of silently dropping data.
        nutriments = {
            "energy-kcal_100g": 200.0, "proteins_100g": 10.0, "fat_100g": 5.0,
            "carbohydrates_100g": 25.0, "fiber_100g": 3.0, "sugars_100g": 8.0,
            "saturated-fat_100g": 2.0, "monounsaturated-fat_100g": 1.5,
            "polyunsaturated-fat_100g": 0.8, "sodium_100g": 0.4,
            "calcium_100g": 0.1, "iron_100g": 0.002, "magnesium_100g": 0.03,
            "potassium_100g": 0.5, "zinc_100g": 0.001, "vitamin-c_100g": 0.01,
        }
        result = _off._parse_product(self._off_result(nutriments)["_off_data"], -1)
        expected = {
            "calories": 200.0, "protein_g": 10.0, "fat_g": 5.0, "carbs_g": 25.0,
            "fiber_g": 3.0, "sugar_g": 8.0, "saturated_fat_g": 2.0,
            "mono_fat_g": 1.5, "poly_fat_g": 0.8,
            "sodium_mg": pytest.approx(400.0), "calcium_mg": pytest.approx(100.0),
            "iron_mg": pytest.approx(2.0), "magnesium_mg": pytest.approx(30.0),
            "potassium_mg": pytest.approx(500.0), "zinc_mg": pytest.approx(1.0),
            "vitamin_c_mg": pytest.approx(10.0),
        }
        for key, value in expected.items():
            assert result["nutrients"].get(key) == value, f"missing/wrong: {key}"
        assert set(result["nutrients"].keys()) == set(expected.keys())

    def test_get_food_detail_matches_direct_parse(self):
        nutriments = {"proteins_100g": 12.0, "carbohydrates_100g": 30.0}
        off_result = self._off_result(nutriments)
        result = _off.get_food_detail(off_result)
        assert result["nutrients"]["protein_g"] == 12.0
        assert result["nutrients"]["carbs_g"] == 30.0
        assert result["fdcId"] == -2000000001

    def test_missing_nutrient_key_omitted(self):
        result = _off._parse_product(self._off_result({"proteins_100g": 5.0})["_off_data"], -1)
        assert result["nutrients"] == {"protein_g": 5.0}

    def test_unparseable_nutrient_value_skipped_not_crashed(self):
        result = _off._parse_product(
            self._off_result({"proteins_100g": "not a number"})["_off_data"], -1
        )
        assert "protein_g" not in result["nutrients"]
