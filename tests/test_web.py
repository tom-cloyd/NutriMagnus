"""
test_web.py — smoke tests for the FastAPI web app (web/backend.py).

Uses fastapi.testclient.TestClient (requires httpx — not in requirements.txt,
same as pytest; install separately: pip install httpx).

Reuses the CLI test suite's autouse fixtures (use_test_db, use_test_profile,
use_test_prefs) from conftest.py for DB/profile isolation, plus a
web-specific fixture below since web/backend.py keeps its own _PREFS_FILE
module constant rather than sharing numa_app.config.prefs._PREFS_FILE.
"""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import profile as _profile
import web.backend as backend
from tests.test_cli import _mock_api


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect web/backend.py's own _PREFS_FILE constant to a temp path."""
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({"include_animal_foods": True}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


# GET routes that take no path params — smoke-test that each renders without error.
_SMOKE_ROUTES = [
    "/",
    "/food/search",
    "/food/analyze-portion",
    "/food/convert",
    "/food/cache",
    "/food/cache/prune",
    "/pantry",
    "/food/custom-profiles",
    "/food/annotate",
    "/meals",
    "/meals/search",
    "/settings",
    "/recipes",
    "/recipe/new",
    "/summary",
    "/analysis/food-use",
]


@pytest.mark.parametrize("path", _SMOKE_ROUTES)
def test_page_renders(client: TestClient, path: str) -> None:
    resp = client.get(path)
    assert resp.status_code == 200


def test_food_search_by_name(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    _mock_api(monkeypatch)
    resp = client.get("/food/search", params={"query": "Chicken"})
    assert resp.status_code == 200
    assert "Chicken" in resp.text


def test_food_detail_page(client: TestClient, cached_food) -> None:
    resp = client.get(f"/food/{cached_food['fdcId']}")
    assert resp.status_code == 200


def test_unknown_food_detail_404s_gracefully(client: TestClient) -> None:
    resp = client.get("/food/999999999")
    assert resp.status_code in (200, 404)


# ---------------------------------------------------------------------------
# POST routes — mutating workflows (pantry, meals, recipes, settings, cache)
# ---------------------------------------------------------------------------

def test_pantry_add_and_remove(client: TestClient, db_conn) -> None:
    resp = client.post("/pantry/add", data={"food_name": "Oats"}, follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == "/pantry?added=1"
    row = db_conn.execute("SELECT * FROM pantry WHERE food_name = 'Oats'").fetchone()
    assert row is not None

    resp = client.post(f"/pantry/remove/{row['id']}", follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute("SELECT * FROM pantry WHERE id = ?", (row["id"],)).fetchone() is None


def test_meal_create_add_food_complete_delete(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post(
        "/meals/create", data={"name": "Breakfast", "meal_date": "2026-07-11"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    meal_id = int(resp.headers["location"].rsplit("/", 1)[-1])

    resp = client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    items = db_conn.execute("SELECT * FROM meal_items WHERE meal_id = ?", (meal_id,)).fetchall()
    assert len(items) == 1
    assert items[0]["amount"] == 150.0

    resp = client.post(f"/meal/{meal_id}/complete", follow_redirects=False)
    assert resp.status_code == 303
    meal = db_conn.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone()
    assert meal["complete"] == 1

    resp = client.post(f"/meal/{meal_id}/delete", follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone() is None


def test_recipe_new_edit_and_add_ingredient(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post(
        "/recipe/new",
        data={"name": "Lentil Soup", "servings": 4},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    recipe_id = int(resp.headers["location"].split("/recipe/")[1].split("/")[0])

    resp = client.post(
        f"/recipe/{recipe_id}/edit",
        data={"name": "Lentil Soup", "description": "Hearty", "servings": 6},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    recipe = db_conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    assert recipe["servings"] == 6
    assert recipe["description"] == "Hearty"

    resp = client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "200 g"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    ingredients = db_conn.execute(
        "SELECT * FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,)
    ).fetchall()
    assert len(ingredients) == 1
    assert ingredients[0]["amount"] == 200.0


def test_custom_profile_create(client: TestClient, db_conn) -> None:
    resp = client.post(
        "/food/custom-profiles/create", data={"name": "My Homemade Granola"}, follow_redirects=False,
    )
    assert resp.status_code == 303
    row = db_conn.execute(
        "SELECT * FROM foods WHERE name = 'My Homemade Granola' AND user_drafted = 1"
    ).fetchone()
    assert row is not None


def test_settings_profile_update(client: TestClient) -> None:
    resp = client.post(
        "/settings",
        data={"age": 40, "sex": "female", "weight": 65, "activity_level": "moderate"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=profile"

    profile = _profile.load_profile()
    assert profile.age == 40
    assert profile.sex == "female"


def test_food_cache_delete_and_prune(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post("/food/cache/delete", data={"fdc_id": cached_food["fdcId"]}, follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute(
        "SELECT * FROM foods WHERE fdc_id = ?", (cached_food["fdcId"],)
    ).fetchone() is None


def test_food_cache_prune_deletes_unreferenced(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post("/food/cache/prune", follow_redirects=False)
    assert resp.status_code == 303
    assert "pruned=1" in resp.headers["location"]
    assert db_conn.execute(
        "SELECT * FROM foods WHERE fdc_id = ?", (cached_food["fdcId"],)
    ).fetchone() is None


def test_food_compare_add(client: TestClient, cached_food) -> None:
    resp = client.post(
        "/food/compare/add", data={"fdc_id": cached_food["fdcId"]}, follow_redirects=False,
    )
    assert resp.status_code == 303
    assert f"ids={cached_food['fdcId']}" in resp.headers["location"]
