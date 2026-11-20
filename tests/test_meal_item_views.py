"""
Tests for numa_app/services/meal_item_views.py and the meal page's Items
"View" selector: As logged, Foods (recipes broken down), Foods & recipes
(each recipe kept whole, even one logged as separate ingredients).
"""
import json

import pytest

import db as _db
from numa_app.services import meal_item_views as _miv

OATS, MILK, LENTILS = 1, 2, 3


@pytest.fixture()
def meal(db_conn):
    """'Oat base' (2 servings: 200 g oats + 500 g milk) inside 'Bowl'
    (1 serving: 50 g oats + 1 serving Oat base). 'Lentil soup' (2 servings:
    300 g lentils). The meal: Bowl x1 logged whole, 30 g oats on its own, and
    Lentil soup logged as one separate ingredient (150 g lentils)."""
    for fdc_id, name in ((OATS, "Oats"), (MILK, "Almond milk"), (LENTILS, "Lentils")):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (fdc_id, name, "SR Legacy", json.dumps({"calories": 100.0, "protein_g": 5.0}), "[]"))
    sub = _db.recipe_create(db_conn, name="Oat base", description="", servings=2, instructions="",
                            total_weight=700.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, sub, OATS, "Oats", 200.0, "g")
    _db.recipe_add_ingredient(db_conn, sub, MILK, "Almond milk", 500.0, "g")
    bowl = _db.recipe_create(db_conn, name="Bowl", description="", servings=1, instructions="",
                             total_weight=400.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, bowl, OATS, "Oats", 50.0, "g")
    _db.recipe_add_ingredient(db_conn, bowl, 0, "Oat base", 1.0, "serving", ref_recipe_id=sub)
    soup = _db.recipe_create(db_conn, name="Lentil soup", description="", servings=2, instructions="",
                             total_weight=300.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, soup, LENTILS, "Lentils", 300.0, "g")
    mid = _db.meal_create(db_conn, "Lunch", "2026-01-05")
    _db.meal_add_recipe(db_conn, mid, bowl, "Bowl", 1.0, added_time="12:00")
    _db.meal_add_food(db_conn, mid, OATS, "Oats", 30.0, "g", added_time="12:01")
    _db.meal_add_food(db_conn, mid, LENTILS, "Lentils", 150.0, "g", added_time="12:02",
                      from_recipe_id=soup)
    db_conn.commit()
    return {"id": mid, "bowl": bowl, "soup": soup}


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient
    from web import backend
    return TestClient(backend.app)


def _items(meal_id):
    from web.backend import _meal_totals
    return _meal_totals(meal_id)[0]


def test_foods_view_breaks_recipes_down_and_combines_a_food(meal):
    with _db.get_db() as conn:
        rows = _miv.foods_view(_items(meal["id"]), conn)
    by_name = {r["food_name"]: r for r in rows}
    # Oats: 50 g in Bowl + 100 g via Oat base (half a batch) + 30 g on its own.
    assert by_name["Oats"]["grams"] == pytest.approx(180.0)
    assert by_name["Oats"]["sources"] == ["Bowl", ""]
    assert by_name["Almond milk"]["grams"] == pytest.approx(250.0)
    assert by_name["Lentils"]["grams"] == pytest.approx(150.0)
    assert by_name["Lentils"]["sources"] == ["Lentil soup"]
    assert len(rows) == 3


def test_whole_view_gathers_separately_logged_ingredients(meal):
    rows = _miv.whole_view(_items(meal["id"]))
    assert [r["food_name"] for r in rows] == ["Bowl", "Oats", "Lentil soup"]
    soup = rows[2]
    assert soup["gathered"] and soup["recipe_id"] == meal["soup"]
    assert soup["grams"] == pytest.approx(150.0) and soup["parts"] == 1


def test_sort_rows_alphabetical_or_as_given():
    rows = [{"food_name": "b"}, {"food_name": "A"}]
    assert [r["food_name"] for r in _miv.sort_rows(rows, "alpha")] == ["A", "b"]
    assert _miv.sort_rows(rows, "entry") == rows


def test_meal_page_view_selector(meal, client):
    page = client.get(f"/meal/{meal['id']}?item_view=foods").text
    assert 'value="foods" selected' in page
    assert "Items (3)" in page and "logged on its own" in page and "Almond milk" in page
    # The choice is remembered.
    assert 'value="foods" selected' in client.get(f"/meal/{meal['id']}").text
    page = client.get(f"/meal/{meal['id']}?item_view=whole").text
    assert "logged as 1 separate ingredient" in page and "Items (3)" in page
    page = client.get(f"/meal/{meal['id']}?item_view=logged").text
    assert "part of" in page and "Almond milk" not in page.split('id="sec-items"')[1].split("</section>")[0]
    # An unknown value falls back to the saved choice.
    assert 'value="logged" selected' in client.get(f"/meal/{meal['id']}?item_view=bogus").text
