"""
Tests for cnf_api.py — id assignment, local name-search over a mocked food
list, and nutrient mapping. All network calls are mocked via _http_get, so
none of this hits the real Canadian Nutrient File API.
"""

import pytest

import cnf_api as _cnf


@pytest.fixture(autouse=True)
def no_cnf():
    """Shadow conftest's autouse no_cnf stub for this file only — these tests
    exercise the real cnf_api functions, with the network mocked via
    _http_get instead of the whole module being stubbed out."""
    yield


@pytest.fixture(autouse=True)
def reset_food_list_cache():
    """_food_list() caches its result at module scope — reset it around every
    test so one test's mocked data can't leak into the next."""
    _cnf.__dict__["_food_list_cache"] = None
    yield
    _cnf.__dict__["_food_list_cache"] = None


SAMPLE_FOODS = [
    {"food_code": 1704, "food_description": "Banana, raw"},
    {"food_code": 1705, "food_description": "Banana, dehydrated, or banana powder"},
    {"food_code": 2, "food_description": "Chicken, broiler, breast, meat only, cooked, roasted"},
]

SAMPLE_NUTRIENT_AMOUNTS = [
    {"nutrient_symbol": "KCAL", "nutrient_value": 89.0},
    {"nutrient_symbol": "PROT", "nutrient_value": 1.09},
    {"nutrient_symbol": "CARB", "nutrient_value": 22.8},
    {"nutrient_symbol": "TRP",  "nutrient_value": 0.0091},
    {"nutrient_symbol": "LEU",  "nutrient_value": 0.0678},
    {"nutrient_symbol": "18:3undiff", "nutrient_value": 0.027},
    {"nutrient_symbol": "SOME_UNMAPPED_SYMBOL", "nutrient_value": 999.0},
    {"nutrient_symbol": "CA", "nutrient_value": None},  # null value — must be skipped, not crash
]


class TestIdAssignment:
    def test_round_trip(self):
        fdc_id = _cnf.cnf_id(1704)
        assert _cnf.is_cnf_id(fdc_id)

    def test_distinct_codes_distinct_ids(self):
        assert _cnf.cnf_id(1704) != _cnf.cnf_id(1705)

    def test_in_reserved_range(self):
        # See numa_app.services.food_ids._SYNTHETIC_ID_RANGES: CNF reserved
        # -4_000_000_000 .. -3_000_000_000.
        fdc_id = _cnf.cnf_id(1704)
        assert -4_000_000_000 <= fdc_id <= -3_000_000_000

    def test_not_off_range(self):
        import openfoodfacts as _off
        fdc_id = _cnf.cnf_id(1704)
        assert not _off.is_off_id(fdc_id)

    def test_positive_usda_id_not_cnf_id(self):
        assert not _cnf.is_cnf_id(12345)


class TestSearchFoods:
    def test_matches_by_substring(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_FOODS)
        results = _cnf.search_foods("banana")
        assert len(results) == 2
        assert all("banana" in r["description"].lower() for r in results)

    def test_all_query_words_must_match(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_FOODS)
        results = _cnf.search_foods("banana dehydrated")
        assert len(results) == 1
        assert results[0]["description"] == "Banana, dehydrated, or banana powder"

    def test_no_match_returns_empty(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_FOODS)
        assert _cnf.search_foods("nonexistent food xyz") == []

    def test_empty_query_returns_empty(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_FOODS)
        assert _cnf.search_foods("") == []

    def test_result_shape(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_FOODS)
        r = _cnf.search_foods("banana")[0]
        assert r["_from_cnf"] is True
        assert r["dataType"] == "Canadian Nutrient File"
        assert _cnf.is_cnf_id(r["fdcId"])

    def test_respects_page_size(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_FOODS)
        assert len(_cnf.search_foods("banana", page_size=1)) == 1

    def test_network_error_returns_empty(self, monkeypatch):
        def _raise(url):
            raise _cnf.CNFError("network error")
        monkeypatch.setattr(_cnf, "_http_get", _raise)
        assert _cnf.search_foods("banana") == []

    def test_food_list_fetched_once(self, monkeypatch):
        calls = []
        def _tracked(url):
            calls.append(url)
            return SAMPLE_FOODS
        monkeypatch.setattr(_cnf, "_http_get", _tracked)
        _cnf.search_foods("banana")
        _cnf.search_foods("chicken")
        assert len(calls) == 1


class TestGetFoodDetail:
    def test_maps_known_symbols(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_NUTRIENT_AMOUNTS)
        detail = _cnf.get_food_detail({"description": "Banana, raw", "_cnf_code": 1704})
        assert detail["nutrients"]["calories"] == pytest.approx(89.0)
        assert detail["nutrients"]["protein_g"] == pytest.approx(1.09)
        assert detail["nutrients"]["carbs_g"] == pytest.approx(22.8)
        assert detail["nutrients"]["aa_tryptophan_g"] == pytest.approx(0.0091)
        assert detail["nutrients"]["aa_leucine_g"] == pytest.approx(0.0678)

    def test_g_to_mg_conversion_for_omega3(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_NUTRIENT_AMOUNTS)
        detail = _cnf.get_food_detail({"description": "Banana, raw", "_cnf_code": 1704})
        assert detail["nutrients"]["omega3_ala_mg"] == pytest.approx(27.0)

    def test_unmapped_symbol_ignored(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_NUTRIENT_AMOUNTS)
        detail = _cnf.get_food_detail({"description": "Banana, raw", "_cnf_code": 1704})
        assert "SOME_UNMAPPED_SYMBOL" not in detail["nutrients"]
        assert set(detail["nutrients"]) <= set(v[0] for v in _cnf._NUTRIENT_MAP.values())

    def test_null_value_skipped_not_crashed(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_NUTRIENT_AMOUNTS)
        detail = _cnf.get_food_detail({"description": "Banana, raw", "_cnf_code": 1704})
        assert "calcium_mg" not in detail["nutrients"]

    def test_result_shape(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_NUTRIENT_AMOUNTS)
        detail = _cnf.get_food_detail({"description": "Banana, raw", "_cnf_code": 1704})
        assert detail["fdcId"] == _cnf.cnf_id(1704)
        assert detail["name"] == "Banana, raw"
        assert detail["dataType"] == "Canadian Nutrient File"
        assert detail["portions"] == []
        assert detail["_from_cnf"] is True

    def test_missing_code_raises(self):
        with pytest.raises(_cnf.CNFError):
            _cnf.get_food_detail({"description": "no code here"})


class TestGetFoodDetailById:
    def test_recovers_food_code_and_fetches_detail(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url:
                             SAMPLE_FOODS if "food/" in url else SAMPLE_NUTRIENT_AMOUNTS)
        fdc_id = _cnf.cnf_id(1704)
        detail = _cnf.get_food_detail_by_id(fdc_id)
        assert detail is not None
        assert detail["name"] == "Banana, raw"
        assert detail["nutrients"]["calories"] == pytest.approx(89.0)

    def test_unknown_id_returns_none(self, monkeypatch):
        monkeypatch.setattr(_cnf, "_http_get", lambda url: SAMPLE_FOODS)
        detail = _cnf.get_food_detail_by_id(_cnf.cnf_id(999999))
        assert detail is None

    def test_network_error_returns_none(self, monkeypatch):
        def _raise(url):
            raise _cnf.CNFError("network error")
        monkeypatch.setattr(_cnf, "_http_get", _raise)
        assert _cnf.get_food_detail_by_id(_cnf.cnf_id(1704)) is None
