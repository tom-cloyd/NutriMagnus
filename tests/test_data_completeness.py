"""
test_data_completeness.py — the nutrient-group completeness check, its
per-food "not needed" choices, the targeted Claude AI prompt they feed, and
the fill-in-only import that follows.
"""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import web.backend as backend
from numa_app.services import claude_fetch as _cf
from numa_app.services import data_completeness as _dc

# Olive oil as USDA Foundation actually returned it (FDC 748608): fat
# subtypes and omega values, but no calories/protein/carbs/fat.
OLIVE_OIL = {"saturated_fat_g": 15.4, "mono_fat_g": 69.2, "poly_fat_g": 9.07,
             "omega3_ala_mg": 651.0, "beta_sitosterol_mg": 1.02, "omega6_la_mg": 8400.0}


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


def _cache(fdc_id, name, nutrients, portions=None):
    with _db.get_db() as conn:
        _db.cache_food(conn, fdc_id=fdc_id, name=name, data_type="Foundation", brand=None,
                       serving_size=None, serving_unit=None, nutrients=nutrients,
                       portions=portions)


def _nutrients(fdc_id):
    with _db.get_db() as conn:
        return json.loads(_db.get_cached_food(conn, fdc_id)["nutrients_json"])


class TestMissingGroups:
    def test_olive_oil_missing_macros_minerals_vitamins_not_omega_or_aa(self):
        gaps = _dc.missing_groups(OLIVE_OIL)
        assert gaps == ["macros", "minerals", "vitamins"]

    def test_one_absent_core_macro_counts_as_missing(self):
        assert "macros" in _dc.missing_groups({"calories": 1, "protein_g": 1, "carbs_g": 1})

    def test_partial_group_is_not_missing(self):
        assert "minerals" not in _dc.missing_groups({"iron_mg": 1.0})

    def test_aa_missing_only_with_protein(self):
        assert "aa" in _dc.missing_groups({"protein_g": 10})
        assert "aa" not in _dc.missing_groups({"protein_g": 0})
        assert "aa" not in _dc.missing_groups({})

    def test_active_gaps_drops_ignored_and_unchecked(self):
        assert _dc.active_gaps(OLIVE_OIL, {"macros"}) == ["minerals", "vitamins"]
        assert _dc.active_gaps(OLIVE_OIL, set(), {"vitamins"}) == ["vitamins"]

    def test_requested_keys_skips_values_present(self):
        keys = _dc.requested_keys(OLIVE_OIL, ["macros"])
        assert keys == ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g"]

    def test_zero_aa_placeholders_count_as_blank_for_a_protein_food(self):
        n = {"protein_g": 10, "aa_lysine_g": 0}
        assert "aa_lysine_g" in _dc.requested_keys(n, ["aa"])


class TestTargetedPrompt:
    def test_lists_only_requested_keys_and_not_needed_groups(self):
        prompt = _cf.build_prompt([(748608, "Oil, olive")],
                                  {748608: (["calories", "fat_g"], ["Minerals"])})
        assert "provide only: calories, fat_g" in prompt
        assert "not needed (user's choice, do not supply): Minerals" in prompt
        assert "include ONLY the nutrient keys listed" in prompt
        assert "I need complete nutritional data" not in prompt

    def test_without_requests_still_asks_for_everything(self):
        prompt = _cf.build_prompt([(1, "X")])
        assert "I need complete nutritional data" in prompt
        assert "provide only" not in prompt
        assert "8b." not in prompt


class TestFillInImport:
    def _valid(self, fdc_id, nutrients, name="Renamed by Claude"):
        return [{"name": name, "fdc_id": fdc_id, "fdc_type": "User Drafted",
                 "source": "USDA", "confidence_note": None, "nutrients": nutrients}]

    def test_existing_food_gains_missing_values_and_keeps_its_own(self):
        _cache(748608, "Oil, olive, extra virgin", OLIVE_OIL, portions=[{"label": "1 tbsp", "grams": 13.5}])
        with _db.get_db() as conn:
            _cf.import_foods(conn, self._valid(748608, {"calories": 884, "fat_g": 100,
                                                       "saturated_fat_g": 99.0}), None)
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, 748608)
        n = json.loads(row["nutrients_json"])
        assert n["calories"] == 884 and n["fat_g"] == 100
        assert n["saturated_fat_g"] == 15.4          # kept, not overwritten
        assert row["name"] == "Oil, olive, extra virgin"   # name kept
        assert row["data_type"] == "Foundation"
        assert json.loads(row["portions_json"]) == [{"label": "1 tbsp", "grams": 13.5}]
        assert row["user_edited"] == 1

    def test_overwrite_replaces_existing_values(self):
        _cache(748608, "Oil", OLIVE_OIL)
        with _db.get_db() as conn:
            _cf.import_foods(conn, self._valid(748608, {"saturated_fat_g": 14.0}), None, overwrite=True)
        assert _nutrients(748608)["saturated_fat_g"] == 14.0

    def test_new_food_is_stored_whole(self):
        with _db.get_db() as conn:
            _cf.import_foods(conn, self._valid(9000002, {"calories": 5}, name="New"), None)
        with _db.get_db() as conn:
            assert _db.get_cached_food(conn, 9000002)["name"] == "New"

    def test_plan_reports_adds_and_keeps(self):
        _cache(748608, "Oil", OLIVE_OIL)
        with _db.get_db() as conn:
            plan = _cf.plan_import(conn, self._valid(748608, {"calories": 884,
                                                             "saturated_fat_g": 99.0,
                                                             "mono_fat_g": 69.2}))
        assert plan == [{"existing": True, "add": ["calories"], "keep": ["saturated_fat_g"],
                     "ann_add": [], "ann_keep": []}]


class TestWeb:
    def test_food_page_offers_claude_and_not_needed_for_missing_macros(self, client):
        _cache(748608, "Oil, olive, extra virgin", OLIVE_OIL)
        resp = client.get("/food/748608")
        assert "Some core macronutrients are missing" in resp.text
        assert "calories, protein, carbohydrate, fat" in resp.text
        assert "Ask Claude AI for the missing data" in resp.text
        assert 'action="/food/748608/data-ignore"' in resp.text

    def test_not_needed_hides_the_alert(self, client):
        _cache(748608, "Oil", OLIVE_OIL)
        client.post("/food/748608/data-ignore", data={"group": "macros"})
        resp = client.get("/food/748608")
        assert "Some core macronutrients are missing" not in resp.text
        assert "Marked not needed for this food:" in resp.text and "(undo)" in resp.text

    def test_fetch_prompt_skips_ignored_group_and_says_so(self, client):
        _cache(748608, "Oil", OLIVE_OIL)
        with _db.get_db() as conn:
            _db.set_food_data_ignore(conn, 748608, "macros", True)
        resp = client.post("/food/cache/claude-fetch", data={"fdc_id": [748608]})
        assert "provide only: calcium_mg" in resp.text
        assert "calories" not in resp.text.split("provide only:")[1].split("\n")[0]
        assert "do not supply): Macronutrients" in resp.text

    def test_fetch_leaves_out_food_with_nothing_missing(self, client):
        _cache(748608, "Oil", OLIVE_OIL)
        for g in ("macros", "minerals", "vitamins"):
            with _db.get_db() as conn:
                _db.set_food_data_ignore(conn, 748608, g, True)
        resp = client.post("/food/cache/claude-fetch", data={"fdc_id": [748608]})
        assert "nothing missing to ask for" in resp.text
        assert "Copy prompt to clipboard" not in resp.text

    def test_check_page_lists_gaps_and_saves_not_needed(self, client):
        _cache(748608, "Oil, olive", OLIVE_OIL)
        resp = client.get("/food/cache/db-check")
        assert 'value="748608:macros"' in resp.text
        client.post("/food/cache/db-check/completeness",
                    data={"shown": ["748608:macros", "748608:minerals"],
                          "ignore": ["748608:macros"]})
        with _db.get_db() as conn:
            assert _db.food_data_ignores(conn) == {748608: {"macros"}}
        # Unchecking a shown cell removes its ignore.
        client.post("/food/cache/db-check/completeness", data={"shown": ["748608:macros"]})
        with _db.get_db() as conn:
            assert _db.food_data_ignores(conn) == {}

    def test_check_page_group_filter_is_remembered(self, client):
        _cache(748608, "Oil, olive", OLIVE_OIL)
        resp = client.get("/food/cache/db-check?check=aa")
        assert "748608:macros" not in resp.text
        resp = client.get("/food/cache/db-check")
        assert "748608:macros" not in resp.text

    def test_ignores_go_when_the_food_is_deleted(self):
        _cache(748608, "Oil", OLIVE_OIL)
        with _db.get_db() as conn:
            _db.set_food_data_ignore(conn, 748608, "macros", True)
            _db.delete_cached_food(conn, 748608)
        with _db.get_db() as conn:
            assert _db.food_data_ignores(conn) == {}


class TestPerGapSelection:
    def test_check_page_defaults_to_no_omega_or_phyto(self, client):
        _cache(748608, "Oil, olive", {"protein_g": 0})  # missing omega and phyto too
        text = client.get("/food/cache/db-check").text
        assert 'value="748608:macros"' in text
        assert 'value="748608:omega"' not in text
        assert 'value="748608:phyto"' not in text

    def test_check_page_has_per_gap_ask_ai_boxes(self, client):
        _cache(748608, "Oil, olive", OLIVE_OIL)
        text = client.get("/food/cache/db-check").text
        assert 'name="want" value="748608:minerals"' in text

    def test_want_limits_prompt_to_chosen_food_and_group(self, client):
        _cache(748608, "Oil, olive", OLIVE_OIL)
        _cache(748609, "Other oil", OLIVE_OIL)
        resp = client.post("/food/cache/claude-fetch", data={"want": ["748608:minerals"]})
        line = resp.text.split("provide only:")[1].split("\n")[0]
        assert line.strip().startswith("calcium_mg") and "calories" not in line and "vitamin" not in line
        assert "748609" not in resp.text


def test_food_page_undoes_not_needed_for_this_food_only(client, cached_food, db_conn):
    """The food page offers a per-group undo for this food, not a link to the
    site-wide completeness list."""
    fid = cached_food["fdcId"]
    _db.set_food_data_ignore(db_conn, fid, "omega", True)
    db_conn.commit()
    html = client.get(f"/food/{fid}").text
    assert "Marked not needed for this food:" in html
    assert 'name="ignored" value="0"' in html
    assert "db-check#completeness" not in html
    client.post(f"/food/{fid}/data-ignore", data={"group": "omega", "ignored": "0"})
    assert "Marked not needed for this food:" not in client.get(f"/food/{fid}").text
