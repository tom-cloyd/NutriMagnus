"""
Tests for ciqual_lookup.py — id assignment and local name-search/lookup over
a fixture food list. No network involved (CIQUAL has no live API — see the
module docstring), so tests inject a small fixture list directly into the
shared StaticSource's cache instead of loading the real ~3,200-food
ciqual_data.json.
"""

import pytest

import ciqual_lookup as _ciqual

SAMPLE_RECORDS = [
    {"food_code": 8030, "name": "Rillettes, goose",
     "nutrients": {"protein_g": 14.9, "fat_g": 33.4, "calories": 364.0}},
    {"food_code": 25192, "name": "Ravioli filled with vegetables, in tomato sauce, canned",
     "nutrients": {"protein_g": 2.88, "fat_g": 2.45, "calories": 91.1}},
    {"food_code": 25193, "name": "Ravioli filled with meat, in tomato sauce, canned",
     "nutrients": {"protein_g": 4.5, "fat_g": 3.1, "calories": 105.0}},
]


@pytest.fixture(autouse=True)
def fixture_records(monkeypatch):
    """Inject SAMPLE_RECORDS directly into the shared StaticSource's cache so
    tests never touch the real bundled ciqual_data.json, and reset caches
    around every test so one test's data can't leak into the next."""
    monkeypatch.setattr(_ciqual._source, "_records_cache", list(SAMPLE_RECORDS))
    monkeypatch.setattr(_ciqual._source, "_id_index_cache", None)
    yield


class TestIdAssignment:
    def test_round_trip(self):
        fdc_id = _ciqual.ciqual_id(8030)
        assert _ciqual.is_ciqual_id(fdc_id)

    def test_distinct_codes_distinct_ids(self):
        assert _ciqual.ciqual_id(8030) != _ciqual.ciqual_id(25192)

    def test_in_reserved_range(self):
        # See numa_app.services.food_ids._SYNTHETIC_ID_RANGES: CIQUAL
        # reserved -7_000_000_000 .. -6_000_000_000.
        fdc_id = _ciqual.ciqual_id(8030)
        assert -7_000_000_000 <= fdc_id <= -6_000_000_000

    def test_not_other_source_ranges(self):
        import openfoodfacts as _off
        import cnf_api as _cnf
        import cofid_lookup as _cofid
        import afcd_lookup as _afcd
        fdc_id = _ciqual.ciqual_id(8030)
        assert not _off.is_off_id(fdc_id)
        assert not _cnf.is_cnf_id(fdc_id)
        assert not _cofid.is_cofid_id(fdc_id)
        assert not _afcd.is_afcd_id(fdc_id)

    def test_positive_usda_id_not_ciqual_id(self):
        assert not _ciqual.is_ciqual_id(12345)


class TestSearchFoods:
    def test_matches_by_substring(self):
        results = _ciqual.search_foods("ravioli")
        assert len(results) == 2

    def test_all_query_words_must_match(self):
        results = _ciqual.search_foods("ravioli meat")
        assert len(results) == 1
        assert results[0]["description"] == "Ravioli filled with meat, in tomato sauce, canned"

    def test_no_match_returns_empty(self):
        assert _ciqual.search_foods("nonexistent food xyz") == []

    def test_empty_query_returns_empty(self):
        assert _ciqual.search_foods("") == []

    def test_result_shape(self):
        r = _ciqual.search_foods("goose")[0]
        assert r["_static_code"] == 8030
        assert r["dataType"] == "CIQUAL"
        assert _ciqual.is_ciqual_id(r["fdcId"])

    def test_respects_page_size(self):
        assert len(_ciqual.search_foods("ravioli", page_size=1)) == 1


class TestGetFoodDetail:
    def test_returns_nutrients(self):
        result = _ciqual.search_foods("goose")[0]
        detail = _ciqual.get_food_detail(result)
        assert detail["nutrients"]["protein_g"] == pytest.approx(14.9)
        assert detail["nutrients"]["calories"] == pytest.approx(364.0)

    def test_no_amino_acid_keys_ever(self):
        result = _ciqual.search_foods("goose")[0]
        detail = _ciqual.get_food_detail(result)
        assert not any(k.startswith("aa_") for k in detail["nutrients"])

    def test_result_shape(self):
        result = _ciqual.search_foods("goose")[0]
        detail = _ciqual.get_food_detail(result)
        assert detail["fdcId"] == _ciqual.ciqual_id(8030)
        assert detail["name"] == "Rillettes, goose"
        assert detail["dataType"] == "CIQUAL"
        assert detail["portions"] == []

    def test_unknown_code_returns_empty_nutrients(self):
        detail = _ciqual.get_food_detail({"description": "made up", "_static_code": 999999})
        assert detail["nutrients"] == {}


class TestGetFoodDetailById:
    def test_recovers_record_and_nutrients(self):
        fdc_id = _ciqual.ciqual_id(25192)
        detail = _ciqual.get_food_detail_by_id(fdc_id)
        assert detail is not None
        assert detail["name"] == "Ravioli filled with vegetables, in tomato sauce, canned"
        assert detail["nutrients"]["protein_g"] == pytest.approx(2.88)

    def test_unknown_id_returns_none(self):
        assert _ciqual.get_food_detail_by_id(-6_999_999_999) is None
