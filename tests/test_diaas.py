"""
Tests for diaas.py — meal-level DIAAS calculation and digestibility lookups.

All tests are pure (no network calls).  DB override tests use the per-test
temp database via the use_test_db autouse fixture from conftest.py.
"""

import pytest
import sqlite3

import diaas as _diaas


# ---------------------------------------------------------------------------
# Shared test nutrients (per-100g profiles)
# ---------------------------------------------------------------------------

# Soy protein isolate — high DIAAS, good across all IAAs
_SOY_100G = {
    "protein_g":          90.0,
    "aa_tryptophan_g":    1.196,
    "aa_threonine_g":     3.164,
    "aa_isoleucine_g":    4.189,
    "aa_leucine_g":       7.011,
    "aa_lysine_g":        5.387,
    "aa_methionine_g":    1.340,
    "aa_cystine_g":       0.883,
    "aa_phenylalanine_g": 4.664,
    "aa_tyrosine_g":      3.400,
    "aa_valine_g":        4.275,
    "aa_histidine_g":     2.223,
}

# Pea protein — good except low Met+Cys
_PEA_100G = {
    "protein_g":          80.0,
    "aa_tryptophan_g":    0.730,
    "aa_threonine_g":     2.700,
    "aa_isoleucine_g":    3.440,
    "aa_leucine_g":       5.950,
    "aa_lysine_g":        5.360,
    "aa_methionine_g":    0.930,
    "aa_cystine_g":       0.000,
    "aa_phenylalanine_g": 3.760,
    "aa_tyrosine_g":      2.500,
    "aa_valine_g":        3.630,
    "aa_histidine_g":     1.550,
}

# Pumpkin seeds — high Met+Cys, complements pea protein
_PUMPKIN_100G = {
    "protein_g":          24.54,
    "aa_tryptophan_g":    0.330,
    "aa_threonine_g":     0.801,
    "aa_isoleucine_g":    1.239,
    "aa_leucine_g":       2.408,
    "aa_lysine_g":        0.979,
    "aa_methionine_g":    0.528,
    "aa_cystine_g":       0.216,
    "aa_phenylalanine_g": 1.558,
    "aa_tyrosine_g":      0.980,
    "aa_valine_g":        1.539,
    "aa_histidine_g":     0.745,
}

# Food with no amino acid data (e.g. branded item with incomplete USDA record)
_NO_AA_100G = {
    "protein_g": 5.0,
    "calories":  40.0,
}

# Food with zero protein
_ZERO_PROTEIN_100G = {
    "protein_g":          0.0,
    "aa_tryptophan_g":    0.0,
}


# ---------------------------------------------------------------------------
# get_digestibility — curated table
# ---------------------------------------------------------------------------

class TestGetDigestibilityCurated:
    def test_soy_protein_isolate(self):
        d, src = _diaas.get_digestibility("soy protein isolate")
        assert d == pytest.approx(0.95)
        assert "curated" in src

    def test_pea_protein(self):
        d, src = _diaas.get_digestibility("Pea protein powder")
        assert d == pytest.approx(0.92)
        assert "curated" in src

    def test_pea_protein_isolate_more_specific(self):
        # isolate entry (0.94) must match before generic pea protein (0.92)
        d, _ = _diaas.get_digestibility("pea protein isolate")
        assert d == pytest.approx(0.94)

    def test_nutritional_yeast(self):
        d, _ = _diaas.get_digestibility("Nutritional yeast flakes")
        assert d == pytest.approx(0.90)

    def test_ground_flax(self):
        d, _ = _diaas.get_digestibility("ground flax seed")
        assert d == pytest.approx(0.85)

    def test_chia_seed(self):
        d, _ = _diaas.get_digestibility("chia seed, ground")
        assert d == pytest.approx(0.82)

    def test_pumpkin_seed(self):
        d, _ = _diaas.get_digestibility("pumpkin seed, roasted")
        assert d == pytest.approx(0.85)

    def test_lentils(self):
        d, _ = _diaas.get_digestibility("lentils, cooked, boiled")
        assert d == pytest.approx(0.83)

    def test_chickpeas(self):
        d, _ = _diaas.get_digestibility("chickpeas, cooked")
        assert d == pytest.approx(0.82)

    def test_egg(self):
        d, _ = _diaas.get_digestibility("Egg, whole, raw")
        assert d == pytest.approx(0.98)

    def test_whey(self):
        d, _ = _diaas.get_digestibility("Whey protein concentrate")
        assert d == pytest.approx(1.00)

    def test_quinoa(self):
        d, _ = _diaas.get_digestibility("Quinoa, cooked")
        assert d == pytest.approx(0.85)

    def test_oats(self):
        d, _ = _diaas.get_digestibility("Rolled oats, dry")
        assert d == pytest.approx(0.82)

    def test_case_insensitive(self):
        d1, _ = _diaas.get_digestibility("Soy Protein Isolate")
        d2, _ = _diaas.get_digestibility("soy protein isolate")
        assert d1 == pytest.approx(d2)

    def test_peanut_butter_powder(self):
        d, _ = _diaas.get_digestibility("peanut butter powder")
        assert d == pytest.approx(0.87)

    def test_hemp_seed(self):
        d, _ = _diaas.get_digestibility("hemp seed, hulled")
        assert d == pytest.approx(0.87)

    def test_okara(self):
        d, _ = _diaas.get_digestibility("dry okara powder")
        assert d == pytest.approx(0.80)


# ---------------------------------------------------------------------------
# get_digestibility — category fallback
# ---------------------------------------------------------------------------

class TestGetDigestibilityCategory:
    def test_unknown_seed_falls_to_category(self):
        d, src = _diaas.get_digestibility("mystery seed extract")
        assert d == pytest.approx(0.82)
        assert "category estimate" in src
        assert "seed" in src

    def test_unknown_nut_falls_to_category(self):
        d, src = _diaas.get_digestibility("macadamia nut, salted")
        # macadamia is in the curated table under walnut/pecan/almond/cashew group
        assert d == pytest.approx(0.78)

    def test_unknown_protein_isolate_falls_to_category(self):
        d, src = _diaas.get_digestibility("cricket protein isolate")
        assert d == pytest.approx(0.92)
        assert "category estimate" in src

    def test_completely_unknown_food_returns_default(self):
        d, src = _diaas.get_digestibility("xyzzy mystery ingredient 42")
        assert d == pytest.approx(0.82)
        assert "default estimate" in src

    def test_source_tag_present_for_all_tiers(self):
        _, src1 = _diaas.get_digestibility("soy protein isolate")    # curated
        _, src2 = _diaas.get_digestibility("mystery seed powder")     # category
        _, src3 = _diaas.get_digestibility("zzz unknown zzz")         # default
        assert "curated" in src1
        assert "category estimate" in src2
        assert "default estimate" in src3


# ---------------------------------------------------------------------------
# get_digestibility — DB user override
# ---------------------------------------------------------------------------

class TestGetDigestibilityUserOverride:
    def test_override_takes_precedence_over_curated(self, db_conn):
        # soy protein isolate curated value is 0.95; override to 0.88
        _diaas.diaas_override_set(db_conn, "soy protein isolate", 0.88, "test override")
        db_conn.commit()
        d, src = _diaas.get_digestibility("soy protein isolate", conn=db_conn)
        assert d == pytest.approx(0.88)
        assert "user override" in src

    def test_override_case_insensitive_lookup(self, db_conn):
        _diaas.diaas_override_set(db_conn, "My Custom Food", 0.77)
        db_conn.commit()
        d, src = _diaas.get_digestibility("my custom food", conn=db_conn)
        assert d == pytest.approx(0.77)
        assert "user override" in src

    def test_no_conn_skips_override_lookup(self, db_conn):
        _diaas.diaas_override_set(db_conn, "soy protein isolate", 0.50)
        db_conn.commit()
        # Without conn, override is invisible — falls back to curated
        d, src = _diaas.get_digestibility("soy protein isolate", conn=None)
        assert d == pytest.approx(0.95)
        assert "curated" in src


# ---------------------------------------------------------------------------
# DB CRUD — diaas_overrides
# ---------------------------------------------------------------------------

class TestDiasOverridesCRUD:
    def test_set_and_get(self, db_conn):
        _diaas.diaas_override_set(db_conn, "Test Food", 0.75, "source note")
        db_conn.commit()
        row = _diaas.diaas_override_get(db_conn, "Test Food")
        assert row is not None
        assert float(row["digestibility"]) == pytest.approx(0.75)
        assert row["notes"] == "source note"

    def test_get_nonexistent_returns_none(self, db_conn):
        assert _diaas.diaas_override_get(db_conn, "nonexistent food") is None

    def test_upsert_replaces_existing(self, db_conn):
        _diaas.diaas_override_set(db_conn, "Test Food", 0.75)
        _diaas.diaas_override_set(db_conn, "Test Food", 0.88, "updated")
        db_conn.commit()
        row = _diaas.diaas_override_get(db_conn, "Test Food")
        assert float(row["digestibility"]) == pytest.approx(0.88)
        assert row["notes"] == "updated"

    def test_delete_existing(self, db_conn):
        _diaas.diaas_override_set(db_conn, "Test Food", 0.75)
        db_conn.commit()
        removed = _diaas.diaas_override_delete(db_conn, "Test Food")
        db_conn.commit()
        assert removed is True
        assert _diaas.diaas_override_get(db_conn, "Test Food") is None

    def test_delete_nonexistent_returns_false(self, db_conn):
        assert _diaas.diaas_override_delete(db_conn, "nonexistent food") is False

    def test_list_empty(self, db_conn):
        assert _diaas.diaas_override_list(db_conn) == []

    def test_list_multiple(self, db_conn):
        _diaas.diaas_override_set(db_conn, "Food B", 0.80)
        _diaas.diaas_override_set(db_conn, "Food A", 0.90)
        db_conn.commit()
        rows = _diaas.diaas_override_list(db_conn)
        assert len(rows) == 2
        assert rows[0]["food_name"] == "Food A"   # ordered by food_name

    def test_digestibility_clamped_to_0_1(self, db_conn):
        # The set function clamps the value; the DB CHECK constraint is the safety net
        _diaas.diaas_override_set(db_conn, "Too High", 1.5)
        db_conn.commit()
        row = _diaas.diaas_override_get(db_conn, "Too High")
        assert float(row["digestibility"]) <= 1.0

    def test_db_rejects_out_of_range_directly(self, db_conn):
        with pytest.raises(Exception):  # sqlite3.IntegrityError
            db_conn.execute(
                "INSERT INTO diaas_overrides (food_name, digestibility) VALUES (?, ?)",
                ("Bad Food", 1.5)
            )
            db_conn.commit()


# ---------------------------------------------------------------------------
# meal_level_diaas — edge cases
# ---------------------------------------------------------------------------

class TestMealLevelDiasEdgeCases:
    def test_empty_list_returns_none_diaas(self):
        result = _diaas.meal_level_diaas([])
        assert result["diaas"] is None
        assert result["total_protein_g"] == 0.0

    def test_zero_protein_returns_none_diaas(self):
        ings = [{"food_name": "Water", "nutrients_100g": _ZERO_PROTEIN_100G, "grams": 200}]
        result = _diaas.meal_level_diaas(ings)
        assert result["diaas"] is None

    def test_no_aa_data_returns_none_diaas_with_missing_list(self):
        ings = [{"food_name": "Mystery Sauce", "nutrients_100g": _NO_AA_100G, "grams": 100}]
        result = _diaas.meal_level_diaas(ings)
        assert result["diaas"] is None
        assert "Mystery Sauce" in result["missing_aa_names"]

    def test_partial_aa_data_computes_diaas_from_available(self):
        """One ingredient has AA data, one doesn't — DIAAS computed from the one that does."""
        ings = [
            {"food_name": "Soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 20},
            {"food_name": "Mystery Sauce",        "nutrients_100g": _NO_AA_100G, "grams": 50},
        ]
        result = _diaas.meal_level_diaas(ings)
        assert result["diaas"] is not None
        assert "Mystery Sauce" in result["missing_aa_names"]
        assert result["has_complete_data"] is False

    def test_has_complete_data_when_all_have_aa(self):
        ings = [
            {"food_name": "Soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 20},
            {"food_name": "Pea protein powder",  "nutrients_100g": _PEA_100G,  "grams": 10},
        ]
        result = _diaas.meal_level_diaas(ings)
        assert result["has_complete_data"] is True
        assert result["missing_aa_names"] == []


# ---------------------------------------------------------------------------
# meal_level_diaas — calculation correctness
# ---------------------------------------------------------------------------

class TestMealLevelDiasCalculation:
    def _single_soy(self, grams=20) -> dict:
        return _diaas.meal_level_diaas([
            {"food_name": "soy protein isolate", "nutrients_100g": _SOY_100G, "grams": grams}
        ])

    def test_single_ingredient_returns_result(self):
        result = self._single_soy()
        assert result["diaas"] is not None
        assert result["total_protein_g"] == pytest.approx(_SOY_100G["protein_g"] * 20 / 100)

    def test_dcp_equals_protein_times_min_diaas_1(self):
        result = self._single_soy()
        dcp_expected = result["total_protein_g"] * min(result["diaas"], 1.0)
        assert result["digestible_complete_protein_g"] == pytest.approx(dcp_expected)

    def test_soy_is_complete_protein(self):
        """Soy isolate should have all IAA ratios above 1.0."""
        result = self._single_soy()
        assert all(v >= 1.0 for v in result["iaa_ratios"].values()), \
            f"Failing ratios: {[(k, v) for k, v in result['iaa_ratios'].items() if v < 1.0]}"

    def test_pea_alone_is_met_cys_limited(self):
        result = _diaas.meal_level_diaas([
            {"food_name": "pea protein powder", "nutrients_100g": _PEA_100G, "grams": 10}
        ])
        assert result["limiting_iaa"] == "aa_methionine_g"
        assert result["iaa_ratios"]["aa_methionine_g"] < 1.0

    def test_complementarity_raises_diaas(self):
        """Pea (Met+Cys limited) + pumpkin seeds (Met+Cys-rich) should raise meal DIAAS."""
        pea_only = _diaas.meal_level_diaas([
            {"food_name": "pea protein powder", "nutrients_100g": _PEA_100G, "grams": 15}
        ])
        combined = _diaas.meal_level_diaas([
            {"food_name": "pea protein powder", "nutrients_100g": _PEA_100G,     "grams": 15},
            {"food_name": "pumpkin seeds",       "nutrients_100g": _PUMPKIN_100G, "grams": 30},
        ])
        assert combined["diaas"] > pea_only["diaas"]
        assert combined["iaa_ratios"]["aa_methionine_g"] > \
               pea_only["iaa_ratios"]["aa_methionine_g"]

    def test_limiting_iaa_is_minimum_ratio(self):
        result = _diaas.meal_level_diaas([
            {"food_name": "pea protein powder", "nutrients_100g": _PEA_100G, "grams": 10}
        ])
        limiting_ratio = result["iaa_ratios"][result["limiting_iaa"]]
        assert limiting_ratio == min(result["iaa_ratios"].values())

    def test_all_iaa_ratios_present_when_data_complete(self):
        result = self._single_soy()
        # Should have ratios for all 9 IAAs since soy data includes all of them
        assert len(result["iaa_ratios"]) == len(_diaas.FAO_REFERENCE)

    def test_met_cys_pair_combined(self):
        """Met+Cys should be the sum of methionine + cystine in IAA scoring."""
        # Build a food where cystine is the only sulfur AA meeting the reference
        nutrients = {
            "protein_g":          10.0,
            "aa_methionine_g":    0.001,   # near-zero methionine
            "aa_cystine_g":       0.300,   # enough cystine to push Met+Cys above reference
            "aa_tryptophan_g":    0.10,
            "aa_threonine_g":     0.40,
            "aa_isoleucine_g":    0.50,
            "aa_leucine_g":       1.00,
            "aa_lysine_g":        0.80,
            "aa_phenylalanine_g": 0.60,
            "aa_valine_g":        0.60,
            "aa_histidine_g":     0.25,
        }
        result = _diaas.meal_level_diaas([
            {"food_name": "test food", "nutrients_100g": nutrients, "grams": 100}
        ])
        # Met+Cys combined = (0.001 + 0.300) / 10.0 * 1000 mg/g = 30.1 mg/g vs ref 23 → ratio > 1
        assert result["iaa_ratios"]["aa_methionine_g"] > 1.0

    def test_phe_tyr_gap_flag_set_when_tyrosine_absent(self):
        nutrients_no_tyr = {k: v for k, v in _SOY_100G.items() if k != "aa_tyrosine_g"}
        result = _diaas.meal_level_diaas([
            {"food_name": "soy no tyr", "nutrients_100g": nutrients_no_tyr, "grams": 20}
        ])
        assert result["phe_tyr_gap"] is True

    def test_phe_tyr_gap_flag_clear_when_tyrosine_present(self):
        result = _diaas.meal_level_diaas([
            {"food_name": "soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 20}
        ])
        assert result["phe_tyr_gap"] is False

    def test_grams_scaling_applied(self):
        """10g of soy at 90g protein/100g should give 9g total protein."""
        result = _diaas.meal_level_diaas([
            {"food_name": "soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 10}
        ])
        assert result["total_protein_g"] == pytest.approx(9.0)

    def test_estimate_sources_tracked(self):
        """Foods matched by category/default should appear in estimate_sources."""
        result = _diaas.meal_level_diaas([
            {"food_name": "xyzzy unknown protein", "nutrients_100g": _PEA_100G, "grams": 10}
        ])
        assert "xyzzy unknown protein" in result["estimate_sources"]

    def test_curated_source_not_in_estimate_sources(self):
        result = _diaas.meal_level_diaas([
            {"food_name": "soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 20}
        ])
        assert "soy protein isolate" not in result["estimate_sources"]

    def test_ingredient_results_include_all_inputs(self):
        ings = [
            {"food_name": "soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 20},
            {"food_name": "Mystery Sauce",        "nutrients_100g": _NO_AA_100G, "grams": 50},
        ]
        result = _diaas.meal_level_diaas(ings)
        names = [i["food_name"] for i in result["ingredients"]]
        assert "soy protein isolate" in names
        assert "Mystery Sauce" in names

    def test_diaas_with_user_override(self, db_conn):
        """User override for digestibility should be reflected in the calculation."""
        # Override soy to 0.50 — should reduce digestible protein
        _diaas.diaas_override_set(db_conn, "soy protein isolate", 0.50)
        db_conn.commit()

        result_default = _diaas.meal_level_diaas([
            {"food_name": "soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 20}
        ], conn=None)
        result_override = _diaas.meal_level_diaas([
            {"food_name": "soy protein isolate", "nutrients_100g": _SOY_100G, "grams": 20}
        ], conn=db_conn)

        assert result_override["diaas"] < result_default["diaas"]
        ing_override = result_override["ingredients"][0]
        assert ing_override["digestibility"] == pytest.approx(0.50)
        assert ing_override["dig_source"] == "user override"


# ---------------------------------------------------------------------------
# Numerical regression — "Oatmeal high protein - 2, no okara" (recipe #17)
#
# Nutrient data (per 100g) taken directly from the numa food cache on 2026-06-03.
# Reference outputs computed independently by online Claude on the same date and
# cross-checked against the numa calculation after the pooled-DIAAS fix.
# Tolerances are set to ±1% on ratios and ±0.3g on protein values, to allow for
# minor floating-point variance while catching any algorithmic regression.
# ---------------------------------------------------------------------------

_R17_OATS = {           # fdc_id 2346396 — Oats, whole grain, rolled, old fashioned (dry)
    "protein_g":          13.5,
    "aa_tryptophan_g":     0.234,
    "aa_threonine_g":      0.575,
    "aa_isoleucine_g":     0.694,
    "aa_leucine_g":        1.284,
    "aa_lysine_g":         0.701,
    "aa_methionine_g":     0.312,
    "aa_cystine_g":        0.408,
    "aa_phenylalanine_g":  0.895,
    "aa_tyrosine_g":       0.573,
    "aa_valine_g":         0.937,
    "aa_histidine_g":      0.405,
}

_R17_HEMP = {           # fdc_id 170148 — Seeds, hemp seed, hulled
    "protein_g":          31.56,
    "aa_tryptophan_g":     0.369,
    "aa_threonine_g":      1.269,
    "aa_isoleucine_g":     1.286,
    "aa_leucine_g":        2.163,
    "aa_lysine_g":         1.276,
    "aa_methionine_g":     0.933,
    "aa_cystine_g":        0.672,
    "aa_phenylalanine_g":  1.447,
    "aa_valine_g":         1.777,
    "aa_histidine_g":      0.969,
}

_R17_YEAST = {          # fdc_id 2676401 — Nutritional Yeast Flakes (fortified)
    "protein_g":          50.0,
    "aa_tryptophan_g":     0.55,
    "aa_threonine_g":      2.30,
    "aa_isoleucine_g":     2.00,
    "aa_leucine_g":        3.30,
    "aa_lysine_g":         3.50,
    "aa_methionine_g":     0.70,
    "aa_cystine_g":        0.50,
    "aa_phenylalanine_g":  1.90,
    "aa_tyrosine_g":       1.10,
    "aa_valine_g":         2.50,
    "aa_histidine_g":      1.00,
}

_R17_PEA = {            # fdc_id 2477360 — Unsweetened Pea Protein Powder (isolate)
    "protein_g":          80.0,
    "aa_tryptophan_g":     0.94,
    "aa_threonine_g":      2.50,
    "aa_isoleucine_g":     2.30,
    "aa_leucine_g":        5.70,
    "aa_lysine_g":         4.70,
    "aa_methionine_g":     0.30,
    "aa_cystine_g":        0.20,
    "aa_phenylalanine_g":  3.70,
    "aa_tyrosine_g":       2.60,
    "aa_valine_g":         2.70,
    "aa_histidine_g":      1.60,
}

_R17_PEANUTS = {        # fdc_id 172430 — Peanuts, all types, raw
    "protein_g":          25.8,
    "aa_tryptophan_g":     0.250,
    "aa_threonine_g":      0.883,
    "aa_isoleucine_g":     0.907,
    "aa_leucine_g":        1.672,
    "aa_lysine_g":         0.926,
    "aa_methionine_g":     0.317,
    "aa_cystine_g":        0.331,
    "aa_phenylalanine_g":  1.377,
    "aa_valine_g":         1.082,
    "aa_histidine_g":      0.652,
}

_R17_INGREDIENTS = [
    {"food_name": "Oats, whole grain, rolled, old fashioned", "nutrients_100g": _R17_OATS,    "grams": 60},
    {"food_name": "Seeds, hemp seed, hulled",                 "nutrients_100g": _R17_HEMP,    "grams": 25},
    {"food_name": "NUTRITIONAL YEAST FLAKES",                 "nutrients_100g": _R17_YEAST,   "grams":  8},
    {"food_name": "UNSWEETENED PEA PROTEIN POWDER",           "nutrients_100g": _R17_PEA,     "grams": 33},
    {"food_name": "Peanuts, all types, raw",                  "nutrients_100g": _R17_PEANUTS, "grams": 35},
]


class TestNumericalRegressionOatmealRecipe:
    """Regression test for pooled meal-level DIAAS on a real five-food recipe.

    Verifies that the algorithm:
      - uses pooled AA data (not per-ingredient lookup) to capture complementarity
      - identifies Met+Cys as the limiting IAA for this meal
      - produces a DIAAS well above what any single ingredient achieves alone
      - computes bioavailable complete protein consistent with the reference
    """

    @pytest.fixture(autouse=True)
    def result(self):
        self._result = _diaas.meal_level_diaas(_R17_INGREDIENTS)

    def test_total_protein(self):
        # 60g×13.5% + 25g×31.56% + 8g×50% + 33g×80% + 35g×25.8% = 55.42g
        assert self._result["total_protein_g"] == pytest.approx(55.42, abs=0.1)

    def test_all_ingredients_have_aa_data(self):
        assert self._result["missing_aa_names"] == []
        assert self._result["has_complete_data"] is True

    def test_limiting_iaa_is_met_cys(self):
        # SAA (Met+Cys) is limiting for this combination of plant proteins
        assert self._result["limiting_iaa"] == "aa_methionine_g"
        assert self._result["limiting_label"] == "Met+Cys"

    def test_meal_diaas_in_expected_range(self):
        # Pooled DIAAS should be ~0.89 — well above per-ingredient weighted average (0.70)
        assert self._result["diaas"] == pytest.approx(0.893, abs=0.005)

    def test_diaas_exceeds_worst_single_ingredient(self):
        # Complementarity lifts the meal above the least-complete ingredient eaten alone.
        # (Adding lower-quality foods can reduce the meal DIAAS below the best ingredient,
        # but the meal must always beat the worst solo score.)
        solo_scores = [
            _diaas.meal_level_diaas([ing])["diaas"]
            for ing in _R17_INGREDIENTS
        ]
        worst_solo = min(s for s in solo_scores if s is not None)
        assert self._result["diaas"] > worst_solo

    def test_bioavailable_complete_protein(self):
        # DCP = total_protein × min(meal_diaas, 1.0) ≈ 55.42 × 0.893 ≈ 49.5g
        assert self._result["digestible_complete_protein_g"] == pytest.approx(49.5, abs=0.5)

    def test_saa_digestible_mg_per_g(self):
        # Met+Cys digestible: ratio × FAO_ref = 0.893 × 23 ≈ 20.5 mg/g meal protein
        ratio = self._result["iaa_ratios"]["aa_methionine_g"]
        mg_per_g = ratio * _diaas.FAO_REFERENCE["aa_methionine_g"]
        assert mg_per_g == pytest.approx(20.5, abs=0.3)

    def test_lysine_digestible_mg_per_g(self):
        ratio = self._result["iaa_ratios"]["aa_lysine_g"]
        mg_per_g = ratio * _diaas.FAO_REFERENCE["aa_lysine_g"]
        assert mg_per_g == pytest.approx(46.6, abs=0.5)

    def test_valine_digestible_mg_per_g(self):
        ratio = self._result["iaa_ratios"]["aa_valine_g"]
        mg_per_g = ratio * _diaas.FAO_REFERENCE["aa_valine_g"]
        assert mg_per_g == pytest.approx(39.3, abs=0.5)

    def test_met_cys_is_minimum_ratio(self):
        # Met+Cys (0.893) is strictly the minimum — all other IAAs score higher.
        # Lysine is the close second at ~0.971 but does not displace Met+Cys as limiting.
        met_cys_ratio = self._result["iaa_ratios"]["aa_methionine_g"]
        for aa_key, ratio in self._result["iaa_ratios"].items():
            if aa_key != "aa_methionine_g":
                assert ratio > met_cys_ratio, (
                    f"{_diaas.IAA_LABELS[aa_key]} ratio {ratio:.3f} is not above "
                    f"Met+Cys ratio {met_cys_ratio:.3f}"
                )
