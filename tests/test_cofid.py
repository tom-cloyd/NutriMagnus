"""
Tests for cofid_lookup.py — id assignment and local name-search/lookup over
a fixture food list. No network involved (CoFID has no live API — see the
module docstring), so tests inject a small fixture list directly into the
module-level cache instead of loading the real ~2,900-food cofid_data.json.
"""

import pytest

import cofid_lookup as _cofid

SAMPLE_RECORDS = [
    {"food_code": "18-070", "name": "Beef, sirloin steak, grilled medium-rare, lean",
     "nutrients": {"protein_g": 26.6, "fat_g": 7.7, "calories": 176.0}},
    {"food_code": "13-148", "name": "Alfalfa sprouts, raw",
     "nutrients": {"protein_g": 4.0, "fat_g": 0.7, "calories": 24.0}},
    {"food_code": "13-149", "name": "Alfalfa sprouts, cooked",
     "nutrients": {"protein_g": 3.5, "fat_g": 0.6, "calories": 20.0}},
]


@pytest.fixture(autouse=True)
def fixture_records(monkeypatch):
    """Inject SAMPLE_RECORDS directly into the module cache so tests never
    touch the real bundled cofid_data.json, and reset caches around every
    test so one test's data can't leak into the next."""
    monkeypatch.setattr(_cofid._source, "_records_cache", list(SAMPLE_RECORDS))
    monkeypatch.setattr(_cofid._source, "_id_index_cache", None)
    yield


class TestIdAssignment:
    def test_round_trip(self):
        fdc_id = _cofid.cofid_id("18-070")
        assert _cofid.is_cofid_id(fdc_id)

    def test_distinct_codes_distinct_ids(self):
        assert _cofid.cofid_id("18-070") != _cofid.cofid_id("13-148")

    def test_deterministic(self):
        assert _cofid.cofid_id("18-070") == _cofid.cofid_id("18-070")

    def test_in_reserved_range(self):
        # See numa_app.services.food_ids._SYNTHETIC_ID_RANGES: CoFID reserved
        # -5_000_000_000 .. -4_000_000_000.
        fdc_id = _cofid.cofid_id("18-070")
        assert -5_000_000_000 <= fdc_id <= -4_000_000_000

    def test_not_off_or_cnf_range(self):
        import openfoodfacts as _off
        import cnf_api as _cnf
        fdc_id = _cofid.cofid_id("18-070")
        assert not _off.is_off_id(fdc_id)
        assert not _cnf.is_cnf_id(fdc_id)

    def test_positive_usda_id_not_cofid_id(self):
        assert not _cofid.is_cofid_id(12345)


class TestSearchFoods:
    def test_matches_by_substring(self):
        results = _cofid.search_foods("alfalfa")
        assert len(results) == 2
        assert all("alfalfa" in r["description"].lower() for r in results)

    def test_all_query_words_must_match(self):
        results = _cofid.search_foods("alfalfa cooked")
        assert len(results) == 1
        assert results[0]["description"] == "Alfalfa sprouts, cooked"

    def test_no_match_returns_empty(self):
        assert _cofid.search_foods("nonexistent food xyz") == []

    def test_empty_query_returns_empty(self):
        assert _cofid.search_foods("") == []

    def test_result_shape(self):
        r = _cofid.search_foods("beef")[0]
        assert r["_static_code"] == "18-070"
        assert r["dataType"] == "CoFID"
        assert _cofid.is_cofid_id(r["fdcId"])

    def test_respects_page_size(self):
        assert len(_cofid.search_foods("alfalfa", page_size=1)) == 1


class TestGetFoodDetail:
    def test_returns_nutrients(self):
        result = _cofid.search_foods("beef")[0]
        detail = _cofid.get_food_detail(result)
        assert detail["nutrients"]["protein_g"] == pytest.approx(26.6)
        assert detail["nutrients"]["calories"] == pytest.approx(176.0)

    def test_no_amino_acid_keys_ever(self):
        result = _cofid.search_foods("beef")[0]
        detail = _cofid.get_food_detail(result)
        assert not any(k.startswith("aa_") for k in detail["nutrients"])

    def test_result_shape(self):
        result = _cofid.search_foods("beef")[0]
        detail = _cofid.get_food_detail(result)
        assert detail["fdcId"] == _cofid.cofid_id("18-070")
        assert detail["name"] == "Beef, sirloin steak, grilled medium-rare, lean"
        assert detail["dataType"] == "CoFID"
        assert detail["portions"] == []
        assert detail["_static_code"] == "18-070"

    def test_unknown_code_returns_empty_nutrients(self):
        detail = _cofid.get_food_detail({"description": "made up", "_static_code": "99-999"})
        assert detail["nutrients"] == {}


class TestGetFoodDetailById:
    def test_recovers_record_and_nutrients(self):
        fdc_id = _cofid.cofid_id("18-070")
        detail = _cofid.get_food_detail_by_id(fdc_id)
        assert detail is not None
        assert detail["name"] == "Beef, sirloin steak, grilled medium-rare, lean"
        assert detail["nutrients"]["protein_g"] == pytest.approx(26.6)

    def test_unknown_id_returns_none(self):
        assert _cofid.get_food_detail_by_id(-4_999_999_999) is None
