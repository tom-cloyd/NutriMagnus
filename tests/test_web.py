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
