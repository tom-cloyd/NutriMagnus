"""
Tests for afcd_lookup.py — id assignment and local name-search/lookup over
a fixture food list. No network involved (AFCD has no live API — see the
module docstring), so tests inject a small fixture list directly into the
shared StaticSource's cache instead of loading the real ~1,600-food
afcd_data.json.
"""

import pytest

import afcd_lookup as _afcd

SAMPLE_RECORDS = [
    {"food_code": "F002258", "name": "Cardamom seed, dried, ground",
     "nutrients": {"protein_g": 10.8, "fat_g": 6.7, "calories": 295.4,
                   "aa_tryptophan_g": 0.155}},
    {"food_code": "F001234", "name": "Chicken, breast, raw, lean",
     "nutrients": {"protein_g": 23.1, "fat_g": 1.2, "calories": 108.0,
                   "aa_leucine_g": 1.75, "aa_lysine_g": 2.0}},
    {"food_code": "F001235", "name": "Chicken, thigh, raw, lean",
     "nutrients": {"protein_g": 20.0, "fat_g": 5.0, "calories": 130.0}},
]


@pytest.fixture(autouse=True)
def fixture_records(monkeypatch):
    """Inject SAMPLE_RECORDS directly into the shared StaticSource's cache so
    tests never touch the real bundled afcd_data.json, and reset caches
    around every test so one test's data can't leak into the next."""
    monkeypatch.setattr(_afcd._source, "_records_cache", list(SAMPLE_RECORDS))
    monkeypatch.setattr(_afcd._source, "_id_index_cache", None)
    yield


class TestIdAssignment:
    def test_round_trip(self):
        fdc_id = _afcd.afcd_id("F002258")
        assert _afcd.is_afcd_id(fdc_id)

    def test_distinct_codes_distinct_ids(self):
        assert _afcd.afcd_id("F002258") != _afcd.afcd_id("F001234")

    def test_in_reserved_range(self):
        # See numa_app.services.food_ids._SYNTHETIC_ID_RANGES: AFCD reserved
        # -6_000_000_000 .. -5_000_000_000.
        fdc_id = _afcd.afcd_id("F002258")
        assert -6_000_000_000 <= fdc_id <= -5_000_000_000

    def test_not_other_source_ranges(self):
        import openfoodfacts as _off
        import cnf_api as _cnf
        import cofid_lookup as _cofid
        fdc_id = _afcd.afcd_id("F002258")
        assert not _off.is_off_id(fdc_id)
        assert not _cnf.is_cnf_id(fdc_id)
        assert not _cofid.is_cofid_id(fdc_id)

    def test_positive_usda_id_not_afcd_id(self):
        assert not _afcd.is_afcd_id(12345)


class TestSearchFoods:
    def test_matches_by_substring(self):
        results = _afcd.search_foods("chicken")
        assert len(results) == 2

    def test_all_query_words_must_match(self):
        results = _afcd.search_foods("chicken breast")
        assert len(results) == 1
        assert results[0]["description"] == "Chicken, breast, raw, lean"

    def test_no_match_returns_empty(self):
        assert _afcd.search_foods("nonexistent food xyz") == []

    def test_empty_query_returns_empty(self):
        assert _afcd.search_foods("") == []

    def test_result_shape(self):
        r = _afcd.search_foods("cardamom")[0]
        assert r["_static_code"] == "F002258"
        assert r["dataType"] == "AFCD"
        assert _afcd.is_afcd_id(r["fdcId"])

    def test_respects_page_size(self):
        assert len(_afcd.search_foods("chicken", page_size=1)) == 1


class TestGetFoodDetail:
    def test_returns_nutrients_including_amino_acids(self):
        result = _afcd.search_foods("cardamom")[0]
        detail = _afcd.get_food_detail(result)
        assert detail["nutrients"]["protein_g"] == pytest.approx(10.8)
        assert detail["nutrients"]["aa_tryptophan_g"] == pytest.approx(0.155)

    def test_result_shape(self):
        result = _afcd.search_foods("cardamom")[0]
        detail = _afcd.get_food_detail(result)
        assert detail["fdcId"] == _afcd.afcd_id("F002258")
        assert detail["name"] == "Cardamom seed, dried, ground"
        assert detail["dataType"] == "AFCD"
        assert detail["portions"] == []

    def test_unknown_code_returns_empty_nutrients(self):
        detail = _afcd.get_food_detail({"description": "made up", "_static_code": "F999999"})
        assert detail["nutrients"] == {}


class TestGetFoodDetailById:
    def test_recovers_record_and_nutrients(self):
        fdc_id = _afcd.afcd_id("F001234")
        detail = _afcd.get_food_detail_by_id(fdc_id)
        assert detail is not None
        assert detail["name"] == "Chicken, breast, raw, lean"
        assert detail["nutrients"]["aa_leucine_g"] == pytest.approx(1.75)

    def test_unknown_id_returns_none(self):
        assert _afcd.get_food_detail_by_id(-5_999_999_999) is None
