"""Value-level edit tracking: foods.source_json (the source's own values)
and user_edited derived from where a food now differs from it — db.py
"Source copy" section, plus the Refresh review screen and food page."""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import web.backend as backend
from tests.conftest import _mock_api, SAMPLE_FDC_ID, SAMPLE_NUTRIENTS


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)

N = {"calories": 100.0, "protein_g": 10.0, "fat_g": 2.0, "carbs_g": 12.0, "iron_mg": 1.0}
P = [{"description": "1 cup", "gram_weight": 80.0}]


def _cache(fdc_id=5, nutrients=N, portions=P):
    with _db.get_db() as conn:
        _db.cache_food(conn, fdc_id, "Oats", "SR Legacy", None, 100.0, "g", dict(nutrients),
                       portions=list(portions))


def _edit(fdc_id=5, **nutrients):
    with _db.get_db() as conn:
        row = _db.get_cached_food(conn, fdc_id)
        n = {**json.loads(row["nutrients_json"]), **nutrients}
        _db.update_cached_food_profile(conn, fdc_id, row["name"], n, data_type=row["data_type"],
                                       serving_size=row["serving_size"], serving_unit=row["serving_unit"],
                                       portions=json.loads(row["portions_json"]))


def _state(fdc_id=5):
    with _db.get_db() as conn:
        return bool(_db.get_cached_food(conn, fdc_id)["user_edited"]), _db.food_edited_keys(conn, fdc_id)


def test_fresh_food_is_its_own_source_and_unedited():
    _cache()
    assert _state() == (False, [])


def test_changing_a_value_edits_and_changing_it_back_clears():
    _cache()
    _edit(iron_mg=9.9)
    assert _state() == (True, ["iron_mg"])
    _edit(iron_mg=1.0)
    assert _state() == (False, [])


def test_an_edit_that_changes_nothing_is_not_an_edit():
    _cache()
    with _db.get_db() as conn:
        _db.mark_user_edited(conn, 5)
    assert _state() == (False, [])


def test_own_portion_is_an_edit_and_removing_it_clears():
    _cache()
    with _db.get_db() as conn:
        _db.update_food_portions(conn, 5, P + [{"description": "1 bowl", "gram_weight": 40.0}])
    assert _state() == (True, ["portion:1 bowl"])
    with _db.get_db() as conn:
        _db.update_food_portions(conn, 5, P)
    assert _state() == (False, [])


def test_clearing_the_last_annotation_ends_edited_status():
    _cache()
    with _db.get_db() as conn:
        kw = dict(gi_no_prompt=False, diaas_no_prompt=False, prep_context=None)
        _db.set_food_annotation(conn, 5, gi_estimate=None, diaas_estimate=0.8, **kw)
        assert _db.get_cached_food(conn, 5)["user_edited"] == 1
        _db.set_food_annotation(conn, 5, gi_estimate=None, diaas_estimate=None, **kw)
        assert _db.get_cached_food(conn, 5)["user_edited"] == 0


def test_estimated_calories_are_not_an_edit():
    _cache(nutrients={k: v for k, v in N.items() if k != "calories"})
    with _db.get_db() as conn:
        assert "calories" in json.loads(_db.get_cached_food(conn, 5)["nutrients_json"])
    _edit(fat_g=3.0)   # the estimate follows the macros; only fat is the user's
    assert _state() == (True, ["fat_g"])


def test_refresh_taking_everything_clears_and_keeping_one_value_keeps_it():
    _cache()
    _edit(iron_mg=9.9, protein_g=11.0)
    fresh = {"nutrients": {**N, "protein_g": 12.0, "zinc_mg": 2.0}, "portions": P}
    with _db.get_db() as conn:
        assert _db.edits_left_after_full_refresh(conn, 5, fresh) is False
        _db.merge_user_supplied_nutrients(conn, 5, {"iron_mg": 1.0, "zinc_mg": 2.0}, overwrite=True,
                                          mark_edited=False)
        _db.rebase_food_source(conn, 5, fresh)
    # protein kept at the user's 11.0 while USDA now says 12.0
    assert _state() == (True, ["protein_g"])
    with _db.get_db() as conn:
        _db.merge_user_supplied_nutrients(conn, 5, {"protein_g": 12.0}, overwrite=True, mark_edited=False)
        _db.rebase_food_source(conn, 5, fresh)
    assert _state() == (False, [])


def test_value_the_source_dropped_is_not_counted_as_the_users():
    _cache()
    fresh = {"nutrients": {k: v for k, v in N.items() if k != "iron_mg"}, "portions": P}
    with _db.get_db() as conn:
        _db.rebase_food_source(conn, 5, fresh)
    assert _state() == (False, [])


def test_old_portion_weight_kept_by_refresh_is_not_the_users():
    _cache()
    fresh = {"nutrients": N, "portions": [{"description": "1 cup", "gram_weight": 85.0}]}
    with _db.get_db() as conn:
        _db.rebase_food_source(conn, 5, fresh)
    assert _state() == (False, [])


def test_legacy_edited_food_without_source_keeps_flag_until_refreshed():
    _cache()
    with _db.get_db() as conn:
        conn.execute("UPDATE foods SET source_json = NULL, user_edited = 1 WHERE fdc_id = 5")
        _db.mark_user_edited(conn, 5)
    assert _state() == (True, None)
    with _db.get_db() as conn:
        _db.rebase_food_source(conn, 5, {"nutrients": {**N, "iron_mg": 2.0}, "portions": P})
    assert _state() == (True, ["iron_mg"])


def test_migration_gives_unedited_foods_a_source_copy_and_leaves_edited_ones_unknown():
    _cache(5)
    _cache(6)
    with _db.get_db() as conn:
        conn.execute("ALTER TABLE foods DROP COLUMN source_json")
        conn.execute("UPDATE foods SET user_edited = 1 WHERE fdc_id = 6")
    _db.init_db()
    with _db.get_db() as conn:
        assert _db.food_source(conn, 5)["nutrients"]["iron_mg"] == 1.0
        assert _db.food_source(conn, 6) is None


def test_imported_user_values_are_an_edit():
    _cache()
    with _db.get_db() as conn:
        _db.cache_user_supplied_food(conn, fdc_id=5, name="Oats", data_type="User Drafted", brand=None,
                                     serving_size=100.0, serving_unit="g", nutrients={**N, "iron_mg": 4.0},
                                     portions=P)
    assert _state() == (True, ["iron_mg"])


# ── screens ─────────────────────────────────────────────────────────────

def test_refresh_screen_ticks_usdas_updates_but_not_your_values(client, monkeypatch):
    _mock_api(monkeypatch)
    _cache(SAMPLE_FDC_ID, nutrients={**SAMPLE_NUTRIENTS, "iron_mg": 1.0, "protein_g": 1.0}, portions=[])
    _edit(SAMPLE_FDC_ID, iron_mg=9.9)
    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=usda").text
    assert 'value="protein_g" id="key-protein_g" checked' in page     # USDA's update, never touched
    assert 'value="iron_mg" id="key-iron_mg" >' in page               # yours: kept unless ticked
    assert "<strong>yours</strong>" in page
    assert 'id="edited-status-note"' in page and 'data-edited-now="1"' in page and 'data-edits-left="0"' in page


def test_food_page_lists_your_changes_beside_the_original(client):
    _cache(SAMPLE_FDC_ID)
    _edit(SAMPLE_FDC_ID, iron_mg=9.9)
    page = client.get(f"/food/{SAMPLE_FDC_ID}").text
    assert "Your changes to this food's original values (1)" in page
    assert "9.9 mg" in page and "1 mg" in page


# ── older versions kept at a Refresh (db.create_food_version) ───────────

def _meal(date, fdc_id=5):
    with _db.get_db() as conn:
        mid = _db.meal_create(conn, "M", date)
        _db.meal_add_food(conn, mid, fdc_id, "Oats", 100, "g")
    return mid


def _meal_food(mid):
    with _db.get_db() as conn:
        return conn.execute("SELECT fdc_id FROM meal_items WHERE meal_id = ?", (mid,)).fetchone()[0]


def test_version_keeps_old_values_for_past_meals_only():
    from numa_app.services.food_ids import classify_food_id, parse_code
    _cache()
    with _db.get_db() as conn:
        _db.upsert_food_annotation(conn, 5, gi_estimate=55.0)
    old, new = _meal("2026-09-01"), _meal("2026-10-05")
    with _db.get_db() as conn:
        kept = _db.create_food_version(conn, 5, "2026-10-01")
        _db.merge_user_supplied_nutrients(conn, 5, {"iron_mg": 3.0}, overwrite=True, mark_edited=False)
    vid = kept["fdc_id"]
    assert kept["num"] == 1 and kept["meal_items"] == 1
    assert _meal_food(old) == vid and _meal_food(new) == 5
    with _db.get_db() as conn:
        v = _db.get_cached_food(conn, vid)
        assert json.loads(v["nutrients_json"])["iron_mg"] == 1.0
        assert v["archived"] == 1 and v["data_type"].startswith("SR Legacy · 20")
        assert _db.get_food_annotation(conn, vid)["gi_estimate"] == 55.0
        assert json.loads(_db.get_cached_food(conn, 5)["nutrients_json"])["iron_mg"] == 3.0
    assert classify_food_id(vid) == ("U5.1", "Older version")
    assert parse_code("u5.1") == ("food", vid)
    with _db.get_db() as conn:
        assert _db.create_food_version(conn, 5, "2026-10-02")["num"] == 2
    assert classify_food_id(vid - 1)[0] == "U5.2"


def test_parse_code_rejects_a_missing_version():
    import pytest as _pt
    from numa_app.services.food_ids import parse_code
    _cache()
    with _pt.raises(ValueError, match="no older version"):
        parse_code("U5.3")


def test_version_codes_sort_after_their_food():
    from numa_app.services.food_ids import code_sort_key, code_source_name
    assert sorted(["U6", "U5.1", "U5", "U5.10", "U5.2"], key=code_sort_key) == ["U5", "U5.1", "U5.2", "U5.10", "U6"]
    assert code_source_name("U5.1") == "older version of a USDA FoodData Central food"


def test_version_is_not_a_duplicate_of_its_food():
    from numa_app.services import data_quality
    _cache()
    with _db.get_db() as conn:
        _db.create_food_version(conn, 5, "2026-10-01")
        assert data_quality.duplicate_groups(conn) == []


def test_refresh_screen_keeps_a_version_for_past_meals(client, monkeypatch):
    _mock_api(monkeypatch)
    _cache(SAMPLE_FDC_ID, nutrients={**SAMPLE_NUTRIENTS, "protein_g": 1.0}, portions=[])
    old = _meal("2026-01-01", SAMPLE_FDC_ID)
    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=usda").text
    assert 'name="keep_version"' in page and "1 meal item" in page
    resp = client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data={
        "source": "usda", "next": f"/food/{SAMPLE_FDC_ID}", "keys": ["protein_g"],
        "incoming_json": json.dumps({"nutrients": SAMPLE_NUTRIENTS}),
        "keep_version": "1", "keep_before": "2026-06-01"}, follow_redirects=False)
    assert "version_kept=" in resp.headers["location"]
    vid = _meal_food(old)
    assert _db.is_version_id(vid)
    detail = client.get(resp.headers["location"]).text
    assert f"U{SAMPLE_FDC_ID}.1" in detail and "Older versions kept for past meals" in detail
    vpage = client.get(f"/food/{vid}").text
    assert "older version" in vpage and "Refresh from USDA &rarr;" not in vpage
