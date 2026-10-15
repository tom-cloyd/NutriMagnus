"""
test_slow_cooker_beans.py — the food-safety warning on a recipe that uses
dried beans and whose instructions mention a slow cooker (FDA: slow cookers
don't destroy kidney-bean lectin), on the recipe page and its printout
(usda_nutrients.slow_cooker_bean_risk; manual #antinutrients).
"""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import web.backend as backend

KIDNEY, ONION = 173744, 170000


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


def _recipe(instructions, bean_name="Beans, kidney, red, mature seeds, raw", *, in_sub=False):
    with _db.get_db() as conn:
        _db.cache_food(conn, KIDNEY, bean_name, "SR Legacy", None, None, None,
                       {"calories": 333.0, "protein_g": 23.6, "carbs_g": 60.0, "fat_g": 0.8})
        _db.cache_food(conn, ONION, "Onions, raw", "SR Legacy", None, None, None,
                       {"calories": 40.0, "protein_g": 1.1, "carbs_g": 9.3, "fat_g": 0.1})
        if in_sub:
            sub = _db.recipe_create(conn, "Bean base", "", 1, "Rinse the beans.")
            _db.recipe_add_ingredient(conn, sub, KIDNEY, bean_name, 200.0, "g")
            rid = _db.recipe_create(conn, "Chili", "", 4, instructions)
            _db.recipe_add_ingredient(conn, rid, 0, "Bean base", 1.0, "serving", ref_recipe_id=sub)
        else:
            rid = _db.recipe_create(conn, "Chili", "", 4, instructions)
            _db.recipe_add_ingredient(conn, rid, KIDNEY, bean_name, 200.0, "g")
        _db.recipe_add_ingredient(conn, rid, ONION, "Onions, raw", 100.0, "g")
    return rid


def test_warning_on_the_recipe_page(client):
    rid = _recipe("Put everything in the slow cooker on low for 8 hours.")
    page = client.get(f"/recipe/{rid}").text
    assert 'id="slow-cooker-beans"' in page
    assert "Food safety: dried beans in a slow cooker" in page
    assert "Beans, kidney, red, mature seeds, raw" in page.split('id="slow-cooker-beans"')[1][:600]


def test_warning_reaches_beans_inside_a_sub_recipe(client):
    rid = _recipe("Crock-Pot, low, 8 hours.", in_sub=True)
    page = client.get(f"/recipe/{rid}").text
    assert 'id="slow-cooker-beans"' in page and 'id="sec-antinutrients"' in page


def test_no_warning_without_a_slow_cooker(client):
    rid = _recipe("Soak overnight, then boil 30 minutes.")
    assert 'id="slow-cooker-beans"' not in client.get(f"/recipe/{rid}").text


def test_no_warning_for_canned_beans(client):
    rid = _recipe("Slow cooker, 6 hours.", bean_name="Beans, kidney, red, canned")
    assert 'id="slow-cooker-beans"' not in client.get(f"/recipe/{rid}").text


def test_warning_is_printed_with_the_instructions(client):
    rid = _recipe("Slow cooker on low for 8 hours.")
    page = client.get(f"/recipe/{rid}/print").text
    if "Instructions</h2>" in page:
        assert 'id="slow-cooker-beans"' in page.split("Instructions</h2>")[1][:1500]
    else:   # the printout's default sections may leave the instructions out
        page = client.get(f"/recipe/{rid}/print", params={"sections": "procedure"}).text
        assert 'id="slow-cooker-beans"' in page
