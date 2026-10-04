"""
test_incoming_review.py — the review screen for incoming food data
(numa_app/services/incoming_review.py): USDA Refresh and "Fill in nutrients
from another food" show incoming values beside the food's own and write only
the ticked ones; the meal page's "Refresh from USDA" fills blanks only.
"""
import html
import json
import pathlib
import re

import pytest
from fastapi.testclient import TestClient

import db as _db
import web.backend as backend
from numa_app.services import incoming_review as _ir
from tests.conftest import SAMPLE_FDC_ID, SAMPLE_FOOD_DETAIL, SAMPLE_NUTRIENTS, _mock_api

GROUPS = [("Macronutrients", [("calories", "Calories", "kcal"), ("protein_g", "Protein", "g")]),
          ("Minerals", [("iron_mg", "Iron", "mg"), ("zinc_mg", "Zinc", "mg")])]


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


def _food(fdc_id):
    with _db.get_db() as conn:
        return _db.get_cached_food(conn, fdc_id)


def _cache(fdc_id, name, nutrients, portions=None):
    with _db.get_db() as conn:
        _db.cache_food(conn, fdc_id=fdc_id, name=name, data_type="SR Legacy", brand=None,
                       serving_size=100.0, serving_unit="g", nutrients=nutrients,
                       portions=portions or [])


def _edit(fdc_id, nutrients):
    """The user's own values on top of an already-cached food — measured
    against its source copy (foods.source_json), so this is what makes it
    user-edited."""
    with _db.get_db() as conn:
        row = _db.get_cached_food(conn, fdc_id)
        _db.cache_food(conn, fdc_id=fdc_id, name=row["name"], data_type=row["data_type"], brand=None,
                       serving_size=row["serving_size"], serving_unit=row["serving_unit"],
                       nutrients=nutrients, portions=json.loads(row["portions_json"] or "[]"),
                       from_source=False)
        _db.mark_user_edited(conn, fdc_id)


def _post_data(pairs):
    """httpx wants repeated fields as {name: [values]}, not a pair list."""
    out: dict[str, list[str]] = {}
    for k, v in pairs:
        out.setdefault(k, []).append(v)
    return out


def _form(page_text):
    """The review form's hidden fields plus its ticked checkboxes, as a
    browser would submit it."""
    data = []
    for m in re.finditer(r'<input type="hidden" name="(\w+)" value="([^"]*)"', page_text):
        data.append((m.group(1), html.unescape(m.group(2))))
    for m in re.finditer(r'<input type="checkbox"[^>]*name="(\w+)" value="([^"]*)"[^>]*>', page_text):
        if " checked" in m.group(0):
            data.append((m.group(1), html.unescape(m.group(2))))
    return data


# ── classification ──────────────────────────────────────────────────────

def test_review_classifies_and_ticks_by_rule():
    current = {"calories": 100.0, "protein_g": 5.0, "iron_mg": 2.0}
    incoming = {"calories": 100.0, "protein_g": 6.0, "zinc_mg": 1.2}
    r = _ir.nutrient_review(current, incoming, GROUPS, prefer_incoming=False)
    fields = {f["key"]: f for g in r["groups"] for f in g["fields"]}
    assert fields["zinc_mg"]["status"] == "fill" and fields["zinc_mg"]["checked"]
    assert fields["protein_g"]["status"] == "differs" and not fields["protein_g"]["checked"]
    assert "calories" not in fields and r["same_count"] == 1
    assert [d["key"] for d in r["dropped"]] == ["iron_mg"]

    r2 = _ir.nutrient_review(current, incoming, GROUPS, prefer_incoming=True)
    fields2 = {f["key"]: f for g in r2["groups"] for f in g["fields"]}
    assert fields2["protein_g"]["checked"]


def test_new_portions_never_repeats_an_existing_description():
    have = [{"description": "1 Breast", "gram_weight": 170}]
    incoming = [{"description": "1 breast", "gram_weight": 174}, {"description": "1 cup", "gram_weight": 140}]
    assert _ir.new_portions(have, incoming) == [{"description": "1 cup", "gram_weight": 140}]


# ── USDA refresh ────────────────────────────────────────────────────────

def test_usda_refresh_of_edited_food_keeps_own_values_unless_ticked(client, monkeypatch):
    _mock_api(monkeypatch)
    mine = {k: v for k, v in SAMPLE_NUTRIENTS.items() if k != "sodium_mg"}
    mine["iron_mg"] = 9.9                      # the user's own figure
    _cache(SAMPLE_FDC_ID, "My chicken", SAMPLE_NUTRIENTS, portions=[{"description": "1 breast", "gram_weight": 170.0}])
    _edit(SAMPLE_FDC_ID, mine)

    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=usda")
    assert page.status_code == 200
    assert 'value="iron_mg"' in page.text and 'value="sodium_mg"' in page.text
    data = _form(page.text)
    assert ("keys", "sodium_mg") in data         # fills a blank: ticked
    assert ("keys", "iron_mg") not in data       # differs on an edited food: not ticked
    assert ("meta", "name") not in data          # own name kept on an edited food

    resp = client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data=_post_data(data), follow_redirects=False)
    assert resp.status_code == 303, resp.text[:300]
    assert resp.headers["location"].startswith(f"/food/{SAMPLE_FDC_ID}?incoming_applied=")
    row = _food(SAMPLE_FDC_ID)
    n = json.loads(row["nutrients_json"])
    assert n["iron_mg"] == 9.9
    assert n["sodium_mg"] == SAMPLE_NUTRIENTS["sodium_mg"]
    assert row["name"] == "My chicken"
    assert row["user_edited"] == 1
    # portions: the existing "1 breast" is untouched, nothing duplicated
    assert json.loads(row["portions_json"]) == [{"description": "1 breast", "gram_weight": 170.0}]


def test_usda_refresh_of_unedited_food_ticks_usda_values_and_adds_portions(client, monkeypatch):
    _mock_api(monkeypatch)
    old = dict(SAMPLE_NUTRIENTS, iron_mg=0.5)
    _cache(SAMPLE_FDC_ID, SAMPLE_FOOD_DETAIL["name"], old)
    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=usda")
    data = _form(page.text)
    assert ("keys", "iron_mg") in data
    assert ("portions", "1 breast") in data
    client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data=_post_data(data), follow_redirects=False)
    row = _food(SAMPLE_FDC_ID)
    assert json.loads(row["nutrients_json"])["iron_mg"] == SAMPLE_NUTRIENTS["iron_mg"]
    assert json.loads(row["portions_json"]) == SAMPLE_FOOD_DETAIL["portions"]
    assert row["user_edited"] == 0                # taking USDA's own values isn't an edit


def test_review_page_writes_nothing(client, monkeypatch):
    _mock_api(monkeypatch)
    _cache(SAMPLE_FDC_ID, "Mine", {"calories": 1.0})
    client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=usda")
    assert json.loads(_food(SAMPLE_FDC_ID)["nutrients_json"]) == {"calories": 1.0}


def test_review_next_must_stay_inside_numa(client, monkeypatch):
    _mock_api(monkeypatch)
    _cache(SAMPLE_FDC_ID, "Mine", {"calories": 1.0})
    resp = client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming",
                       data={"source": "usda", "incoming_json": "{}", "next": "//evil.example/"},
                       follow_redirects=False)
    assert resp.headers["location"].startswith(f"/food/{SAMPLE_FDC_ID}")


# ── fill from another food ──────────────────────────────────────────────

def test_fill_from_another_food_writes_ticked_values_and_marks_edited(client):
    _cache(SAMPLE_FDC_ID, "Target", {"calories": 100.0, "protein_g": 5.0})
    _cache(2002, "Source", {"calories": 120.0, "protein_g": 5.0, "iron_mg": 3.0})
    fill = client.get(f"/food/{SAMPLE_FDC_ID}/fill-from?q=Source")
    assert "Review values to copy" in fill.text and 'name="pick"' in fill.text

    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=food&source_fdc_id=2002")
    data = _form(page.text)
    assert ("keys", "iron_mg") in data and ("keys", "calories") not in data
    client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data=_post_data(data), follow_redirects=False)
    row = _food(SAMPLE_FDC_ID)
    assert json.loads(row["nutrients_json"]) == {"calories": 100.0, "protein_g": 5.0, "iron_mg": 3.0}
    assert row["user_edited"] == 1 and row["user_drafted"] == 0   # edited, not turned custom
    assert "Copied from Source" in (row["notes"] or "")


# ── meal "Refresh from USDA" ────────────────────────────────────────────

def test_meal_refresh_fills_blanks_only_and_lists_differences(client, monkeypatch):
    _mock_api(monkeypatch)
    mine = {k: v for k, v in SAMPLE_NUTRIENTS.items() if not k.startswith("aa_")}
    mine["iron_mg"] = 9.9
    _cache(SAMPLE_FDC_ID, "My chicken", mine)
    meal_id = int(client.post("/meals/create", data={"name": "Lunch", "meal_date": "2026-10-02"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    with _db.get_db() as conn:
        _db.meal_add_food(conn, meal_id, SAMPLE_FDC_ID, "My chicken", 100.0, "g")
    resp = client.post(f"/meal/{meal_id}/refresh-aa", follow_redirects=False)
    loc = resp.headers["location"]
    assert "aa_refreshed=1" in loc and f"aa_differs={SAMPLE_FDC_ID}" in loc
    n = json.loads(_food(SAMPLE_FDC_ID)["nutrients_json"])
    assert n["iron_mg"] == 9.9                                     # own value kept
    assert n["aa_lysine_g"] == SAMPLE_NUTRIENTS["aa_lysine_g"]     # blank filled
    assert _food(SAMPLE_FDC_ID)["user_edited"] == 0               # USDA's own values: not an edit
    page = client.get(loc.split("#")[0])
    assert 'id="aa-refresh-result"' in page.text
    assert f"/food/{SAMPLE_FDC_ID}/review-incoming?source=usda" in page.text


# ── amino acids from another food: scaled, and marked as estimates ──────

AA_SOURCE = {"protein_g": 20.0, "aa_tryptophan_g": 0.2, "aa_threonine_g": 0.8, "aa_isoleucine_g": 0.9,
             "aa_leucine_g": 1.6, "aa_lysine_g": 2.0, "aa_methionine_g": 0.5, "aa_valine_g": 1.0,
             "aa_histidine_g": 0.6, "aa_phenylalanine_g": 1.0}


def _estimated(fdc_id):
    with _db.get_db() as conn:
        return _db.estimated_keys(conn, fdc_id)


def test_scaled_aa_scales_by_protein_ratio():
    from numa_app.services import aa_estimate as _ae
    scaled, factor = _ae.scaled_aa(AA_SOURCE, 10.0)
    assert factor == 0.5 and scaled["aa_lysine_g"] == 1.0
    assert _ae.scaled_aa(AA_SOURCE, None) == ({}, None)


def test_fill_from_scales_amino_acids_to_this_foods_protein(client):
    _cache(SAMPLE_FDC_ID, "Target", {"protein_g": 10.0, "calories": 50.0})
    _cache(2002, "Source", dict(AA_SOURCE, iron_mg=3.0))
    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=food&source_fdc_id=2002")
    assert 'id="aa-scale-note"' in page.text
    assert 'data-aa-own="1.0" data-aa-alt="2.0"' in page.text      # lysine: own protein vs incoming
    data = _form(page.text)
    assert ("keys", "aa_lysine_g") in data and ("keys", "protein_g") not in data
    client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data=_post_data(data), follow_redirects=False)
    row = _food(SAMPLE_FDC_ID)
    n = json.loads(row["nutrients_json"])
    assert n["aa_lysine_g"] == 1.0 and n["protein_g"] == 10.0 and n["iron_mg"] == 3.0
    assert "AA data estimated by scaling from Source" in row["notes"]
    assert {"aa_lysine_g", "iron_mg"} <= _estimated(SAMPLE_FDC_ID)


def test_fill_from_with_protein_ticked_scales_to_incoming_protein(client):
    _cache(SAMPLE_FDC_ID, "Target", {"protein_g": 10.0})
    _cache(2002, "Source", AA_SOURCE)
    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=food&source_fdc_id=2002")
    data = _form(page.text) + [("keys", "protein_g")]
    client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data=_post_data(data), follow_redirects=False)
    n = json.loads(_food(SAMPLE_FDC_ID)["nutrients_json"])
    assert n["protein_g"] == 20.0 and n["aa_lysine_g"] == 2.0


def test_fill_from_without_any_protein_writes_no_amino_acids(client):
    _cache(SAMPLE_FDC_ID, "Target", {"calories": 50.0})
    _cache(2002, "Source", AA_SOURCE)
    data = [("source", "food"), ("source_fdc_id", "2002"), ("next", f"/food/{SAMPLE_FDC_ID}"),
            ("incoming_json", json.dumps({"nutrients": AA_SOURCE, "name": "Source"})),
            ("keys", "aa_lysine_g")]
    client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data=_post_data(data), follow_redirects=False)
    assert "aa_lysine_g" not in json.loads(_food(SAMPLE_FDC_ID)["nutrients_json"])


def test_usda_refresh_ticks_measured_value_over_an_estimate_and_clears_the_mark(client, monkeypatch):
    _mock_api(monkeypatch)
    mine = dict(SAMPLE_NUTRIENTS, aa_lysine_g=1.5, iron_mg=9.9)
    _cache(SAMPLE_FDC_ID, "Mine", SAMPLE_NUTRIENTS)
    _edit(SAMPLE_FDC_ID, mine)
    with _db.get_db() as conn:
        _db.update_estimated_keys(conn, SAMPLE_FDC_ID, add={"aa_lysine_g"})
    page = client.get(f"/food/{SAMPLE_FDC_ID}/review-incoming?source=usda")
    assert "yours is an estimate" in page.text
    data = _form(page.text)
    assert ("keys", "aa_lysine_g") in data and ("keys", "iron_mg") not in data
    client.post(f"/food/{SAMPLE_FDC_ID}/review-incoming", data=_post_data(data), follow_redirects=False)
    n = json.loads(_food(SAMPLE_FDC_ID)["nutrients_json"])
    assert n["aa_lysine_g"] == SAMPLE_NUTRIENTS["aa_lysine_g"] and n["iron_mg"] == 9.9
    assert "aa_lysine_g" not in _estimated(SAMPLE_FDC_ID)


def test_meal_refresh_replaces_estimated_amino_acids_with_measured(client, monkeypatch):
    _mock_api(monkeypatch)
    mine = dict(SAMPLE_NUTRIENTS, aa_lysine_g=1.5)
    _cache(SAMPLE_FDC_ID, "Mine", mine)
    with _db.get_db() as conn:
        _db.update_estimated_keys(conn, SAMPLE_FDC_ID, add={"aa_lysine_g"})
    meal_id = int(client.post("/meals/create", data={"name": "Lunch", "meal_date": "2026-10-02"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    with _db.get_db() as conn:
        _db.meal_add_food(conn, meal_id, SAMPLE_FDC_ID, "Mine", 100.0, "g")
    loc = client.post(f"/meal/{meal_id}/refresh-aa", follow_redirects=False).headers["location"]
    assert "aa_refreshed=1" in loc and "aa_differs" not in loc
    assert json.loads(_food(SAMPLE_FDC_ID)["nutrients_json"])["aa_lysine_g"] == SAMPLE_NUTRIENTS["aa_lysine_g"]
    assert _estimated(SAMPLE_FDC_ID) == set()
