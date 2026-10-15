"""
test_vitamin_k_repair.py — vitamin K is USDA's phylloquinone (nutrient 1185 /
number "430"), and the one-time correction of foods cached while NuMa read
menaquinone-4 (1183) instead (numa_app/services/vitamin_k_repair.py).
"""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import usda as _usda
import usda_api as _usda_api
import web.backend as backend
from numa_app.services import vitamin_k_repair as _vk

SPINACH, CHICKEN, EDITED, GONE = 168462, 171477, 170000, 170001


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)
    from numa_app.services import manual_build as _manual_build
    monkeypatch.setattr(_manual_build, "rebuild_manual_if_stale", lambda: None)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


def _cache(conn, fdc_id, name, nutrients, *, checked=False):
    _db.cache_food(conn, fdc_id=fdc_id, name=name, data_type="SR Legacy", brand=None,
                   serving_size=None, serving_unit=None, nutrients=nutrients,
                   vitamin_k_checked=checked)


def _nutrients(fdc_id):
    with _db.get_db() as conn:
        row = _db.get_cached_food(conn, fdc_id)
        return json.loads(row["nutrients_json"]), json.loads(row["source_json"] or "null"), row["vitamin_k_checked"]


@pytest.fixture()
def old_foods():
    """Foods cached by the old parser: spinach with no vitamin K, chicken with
    its MK-4 figure, one the user corrected by hand, one USDA no longer returns."""
    with _db.get_db() as conn:
        _cache(conn, SPINACH, "Spinach, raw", {"calories": 23.0})
        _cache(conn, CHICKEN, "Chicken breast", {"calories": 120.0, "vitamin_k_mcg": 8.4})
        _cache(conn, EDITED, "Kale, raw", {"calories": 35.0, "vitamin_k_mcg": 1.0})
        _cache(conn, GONE, "Withdrawn food", {"calories": 50.0, "vitamin_k_mcg": 2.0})
        row = _db.get_cached_food(conn, EDITED)
        nuts = json.loads(row["nutrients_json"])
        nuts["vitamin_k_mcg"] = 390.0            # the user's own figure
        conn.execute("UPDATE foods SET nutrients_json = ? WHERE fdc_id = ?", (json.dumps(nuts), EDITED))


class TestParser:
    def test_detail_fetch_reads_phylloquinone_not_menaquinone(self):
        data = {"fdcId": SPINACH, "description": "Spinach, raw", "foodNutrients": [
            {"nutrient": {"id": 1185}, "amount": 482.9},
            {"nutrient": {"id": 1183}, "amount": 0.0},
        ]}
        assert _usda_api._parse_food(data)["nutrients"]["vitamin_k_mcg"] == 482.9

    def test_menaquinone_alone_is_not_vitamin_k(self):
        data = {"fdcId": CHICKEN, "description": "Chicken", "foodNutrients": [
            {"nutrient": {"id": 1183}, "amount": 8.4}]}
        assert "vitamin_k_mcg" not in _usda_api._parse_food(data)["nutrients"]

    def test_both_endpoints_agree(self):
        assert _usda_api.NUTRIENT_NUMBER_MAP["430"] == "vitamin_k_mcg"
        assert _usda_api.NUTRIENT_MAP[1185][0] == "vitamin_k_mcg"
        assert 1183 not in _usda_api.NUTRIENT_MAP


class TestGetNutrientValues:
    def test_keeps_only_foods_asked_for_and_marks_missing_values(self, monkeypatch):
        reply = [
            {"fdcId": SPINACH, "description": "s", "foodNutrients": [{"number": "430", "amount": 483}]},
            {"fdcId": CHICKEN, "description": "c", "foodNutrients": []},
            {"fdcId": 999, "description": "unrelated", "foodNutrients": [{"number": "430", "amount": 5}]},
        ]
        monkeypatch.setattr(_usda_api, "_get", lambda path, params: reply)
        assert _usda.get_nutrient_values([SPINACH, CHICKEN, GONE], "430") == {SPINACH: 483.0, CHICKEN: None}

    def test_water_values_drop_missing(self, monkeypatch):
        reply = [{"fdcId": 1, "description": "a", "foodNutrients": [{"number": "255", "amount": 90}]},
                 {"fdcId": 2, "description": "b", "foodNutrients": []}]
        monkeypatch.setattr(_usda_api, "_get", lambda path, params: reply)
        assert _usda.get_water_values([1, 2]) == {1: 90.0}

    def test_requests_twenty_at_a_time(self, monkeypatch):
        calls = []
        monkeypatch.setattr(_usda_api, "_get", lambda path, params: calls.append(params["fdcIds"]) or [])
        _usda.get_nutrient_values(list(range(1, 46)), "430")
        assert [len(c.split(",")) for c in calls] == [20, 20, 5]


class TestCheckedFlag:
    def test_fresh_fetch_is_checked_and_old_data_is_not(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, 1, "Fresh", "SR Legacy", None, None, None, {"calories": 1.0})
            _cache(conn, 2, "Old", {"calories": 1.0})
            _db.cache_food(conn, -5, "Mine", "User Drafted", None, None, None, {"calories": 1.0},
                           user_drafted=True, vitamin_k_checked=False)
            assert _vk.candidates(conn) == [2]

    def test_starter_copies_of_usda_foods_wait_for_the_repair(self):
        from numa_app.services import demo_data as _demo
        with _db.get_db() as conn:
            _demo._insert_food(conn, {"fdc_id": SPINACH, "name": "* Spinach", "data_type": "SR Legacy",
                                      "nutrients": {"calories": 23.0}, "portions": []})
            assert SPINACH in _vk.candidates(conn)


class TestReplaceSourceNutrient:
    def test_replaces_in_food_and_source_copy(self, old_foods):
        with _db.get_db() as conn:
            assert _db.replace_source_nutrient(conn, CHICKEN, "vitamin_k_mcg", 0.3) is True
        nuts, src, _ = _nutrients(CHICKEN)
        assert nuts["vitamin_k_mcg"] == src["nutrients"]["vitamin_k_mcg"] == 0.3

    def test_none_removes_the_value(self, old_foods):
        with _db.get_db() as conn:
            assert _db.replace_source_nutrient(conn, CHICKEN, "vitamin_k_mcg", None) is True
        nuts, src, _ = _nutrients(CHICKEN)
        assert "vitamin_k_mcg" not in nuts and "vitamin_k_mcg" not in src["nutrients"]

    def test_adds_a_missing_value(self, old_foods):
        with _db.get_db() as conn:
            assert _db.replace_source_nutrient(conn, SPINACH, "vitamin_k_mcg", 483.0) is True
        assert _nutrients(SPINACH)[0]["vitamin_k_mcg"] == 483.0

    def test_keeps_the_users_own_edit(self, old_foods):
        with _db.get_db() as conn:
            assert _db.replace_source_nutrient(conn, EDITED, "vitamin_k_mcg", 389.6) is False
        assert _nutrients(EDITED)[0]["vitamin_k_mcg"] == 390.0

    def test_unchanged_value_reports_no_change(self, old_foods):
        with _db.get_db() as conn:
            assert _db.replace_source_nutrient(conn, CHICKEN, "vitamin_k_mcg", 8.4) is False
            assert _db.replace_source_nutrient(conn, SPINACH, "vitamin_k_mcg", None) is False


class TestRun:
    @pytest.fixture()
    def usda_reply(self, monkeypatch):
        values = {SPINACH: 483.0, CHICKEN: 0.3, EDITED: 389.6}     # GONE not returned
        monkeypatch.setattr(_usda, "get_nutrient_values",
                            lambda ids, number: {i: values[i] for i in ids if i in values})

        def detail(fdc_id):          # nor singly: the network let us down
            raise _usda.USDAError("Network error: timed out")
        monkeypatch.setattr(_usda, "get_food_detail", detail)

    def test_corrects_skips_edits_and_retries_what_usda_did_not_return(self, old_foods, usda_reply):
        _vk.run()
        assert _nutrients(SPINACH)[0]["vitamin_k_mcg"] == 483.0
        assert _nutrients(CHICKEN)[0]["vitamin_k_mcg"] == 0.3
        assert _nutrients(EDITED)[0]["vitamin_k_mcg"] == 390.0
        assert _nutrients(GONE)[0]["vitamin_k_mcg"] == 2.0
        s = _vk.status()
        assert (s["checked"], s["changed"], s["not_found"], s["error"]) == (4, 2, ["Withdrawn food"], None)
        with _db.get_db() as conn:
            assert _vk.candidates(conn) == [GONE]

    def test_a_food_the_batch_skips_is_fetched_on_its_own(self, old_foods, monkeypatch):
        """USDA's bulk request leaves out some Branded records its single-food
        lookup still serves; those were retried forever, changing nothing."""
        monkeypatch.setattr(_usda, "get_nutrient_values",
                            lambda ids, number: {i: None for i in ids if i != GONE})
        monkeypatch.setattr(_usda, "get_food_detail",
                            lambda fdc_id: {"nutrients": {"calories": 50.0, "vitamin_k_mcg": 0.7}})
        _vk.run()
        assert _nutrients(GONE)[0]["vitamin_k_mcg"] == 0.7
        assert _vk.status()["not_found"] == []
        with _db.get_db() as conn:
            assert _vk.candidates(conn) == []

    def test_a_food_usda_has_no_record_of_is_not_asked_about_again(self, old_foods, monkeypatch):
        monkeypatch.setattr(_usda, "get_nutrient_values",
                            lambda ids, number: {i: None for i in ids if i != GONE})

        def detail(fdc_id):
            raise _usda.USDAError("USDA API 404: endpoint not found — possible API change")
        monkeypatch.setattr(_usda, "get_food_detail", detail)
        _vk.run()
        assert _nutrients(GONE)[0]["vitamin_k_mcg"] == 2.0          # left as it was
        s = _vk.status()
        assert (s["not_found"], s["not_in_usda"]) == ([], ["Withdrawn food"])
        with _db.get_db() as conn:
            assert _vk.candidates(conn) == []

    def test_meals_using_a_corrected_food_are_recalculated(self, old_foods, usda_reply):
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Lunch", "2026-10-01")
            _db.meal_add_food(conn, mid, SPINACH, "Spinach", 50.0, "g")
        _vk.run()
        with _db.get_db() as conn:
            assert mid in _db.meals_using_food(conn, SPINACH)
            assert conn.execute("SELECT 1 FROM stale_meals WHERE meal_id = ?", (mid,)).fetchone()

    def test_a_failed_request_keeps_earlier_batches(self, old_foods, monkeypatch):
        def fail(ids, number):
            raise _usda.USDAError("USDA API 503: unavailable")
        monkeypatch.setattr(_usda, "get_nutrient_values", fail)
        _vk.run()
        assert "503" in _vk.status()["error"]
        with _db.get_db() as conn:
            assert len(_vk.candidates(conn)) == 4


class TestPages:
    def test_foods_9_offers_the_correction(self, client, old_foods):
        page = client.get("/food/cache/db-check").text
        assert 'id="vitamin-k-repair"' in page
        assert "Correct vitamin K for 4 USDA foods from USDA" in page

    def test_home_notice_until_corrected(self, client, old_foods, monkeypatch):
        assert 'id="vitamin-k-notice"' in client.get("/").text
        with _db.get_db() as conn:
            for fid in (SPINACH, CHICKEN, EDITED, GONE):
                _db.mark_vitamin_k_checked(conn, fid)
        assert 'id="vitamin-k-notice"' not in client.get("/").text
        assert "Correct vitamin K for" not in client.get("/food/cache/db-check").text

    def test_button_starts_the_repair(self, client, monkeypatch):
        started = []
        monkeypatch.setattr(_vk, "start", lambda: started.append(1) or True)
        r = client.post("/food/cache/vitamin-k-repair", follow_redirects=False)
        assert r.status_code == 303 and r.headers["location"].endswith("#vitamin-k-repair")
        assert started == [1]
