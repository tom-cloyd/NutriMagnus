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


def _item_id(meal_id, name):
    return next(it["id"] for it in _items(meal_id) if it["food_name"] == name)


def test_view_rows_carry_the_logged_items_a_remove_can_take_out(meal):
    oats, lentils = _item_id(meal["id"], "Oats"), _item_id(meal["id"], "Lentils")
    with _db.get_db() as conn:
        by_name = {r["food_name"]: r for r in _miv.foods_view(_items(meal["id"]), conn)}
    # Oats: logged on its own (removable) and inside Bowl, logged whole (not).
    assert by_name["Oats"]["item_ids"] == [oats]
    assert by_name["Oats"]["whole_recipes"] == ["Bowl"]
    # Almond milk is only inside Bowl: nothing here to remove.
    assert by_name["Almond milk"]["item_ids"] == []
    assert by_name["Lentils"]["item_ids"] == [lentils]
    assert by_name["Lentils"]["whole_recipes"] == []
    soup = _miv.whole_view(_items(meal["id"]))[2]
    assert soup["item_ids"] == [lentils]


def test_add_recipe_as_ingredients_then_undo_removes_just_those(meal, client):
    from urllib.parse import parse_qs, urlsplit
    before = {it["id"] for it in _items(meal["id"])}
    resp = client.post(f"/meal/{meal['id']}/add-recipe",
                       data={"recipe_id": meal["bowl"], "amount": "1 serving", "mode": "ingredients"},
                       follow_redirects=False)
    params = parse_qs(urlsplit(resp.headers["location"]).query)
    added = [int(x) for x in params["added_ids"][0].split(",")]
    assert len(added) == 3  # Oats, then Oat base's oats and milk
    assert {it["id"] for it in _items(meal["id"])} == before | set(added)

    page = client.get(resp.headers["location"]).text
    assert f'name="item_ids" value="{params["added_ids"][0]}"' in page and ">Undo</button>" in page

    resp = client.post(f"/meal/{meal['id']}/remove-items",
                       data={"item_ids": params["added_ids"][0], "name": "Bowl"},
                       follow_redirects=False)
    assert {it["id"] for it in _items(meal["id"])} == before
    assert "removed=Bowl" in resp.headers["location"]
    assert "Removed Bowl from this meal" in client.get(resp.headers["location"]).text


def test_remove_items_ignores_another_meals_items(meal, client):
    with _db.get_db() as conn:
        other = _db.meal_create(conn, "Dinner", "2026-01-05")
        other_item = _db.meal_add_food(conn, other, OATS, "Oats", 10.0, "g")
    resp = client.post(f"/meal/{meal['id']}/remove-items",
                       data={"item_ids": f"{other_item},junk", "name": "Oats"}, follow_redirects=False)
    assert "removed" not in resp.headers["location"]
    with _db.get_db() as conn:
        assert conn.execute("SELECT 1 FROM meal_items WHERE id = ?", (other_item,)).fetchone()
    assert len(_items(meal["id"])) == 3


def test_foods_and_whole_views_show_remove_buttons(meal, client):
    lentils = _item_id(meal["id"], "Lentils")
    page = client.get(f"/meal/{meal['id']}?item_view=foods").text
    assert page.count('action="/meal/%d/remove-items"' % meal["id"]) == 2  # Oats, Lentils
    assert "in a recipe</small>" in page  # Almond milk, only inside Bowl
    assert "the part inside Bowl stays" in page
    page = client.get(f"/meal/{meal['id']}?item_view=whole").text
    assert page.count('action="/meal/%d/remove-items"' % meal["id"]) == 3
    assert f'name="item_ids" value="{lentils}"' in page
    assert "its one separately logged ingredient" in page


def _amount(item_id):
    with _db.get_db() as conn:
        return conn.execute("SELECT amount FROM meal_items WHERE id = ?", (item_id,)).fetchone()[0]


def test_scale_items_sets_a_new_total_keeping_proportions(meal, client):
    from urllib.parse import parse_qs, urlsplit
    lentils = _item_id(meal["id"], "Lentils")
    client.post(f"/meal/{meal['id']}/scale-items",
                data={"item_ids": str(lentils), "amount": "300", "name": "Lentil soup"})
    assert _amount(lentils) == pytest.approx(300.0)
    # Servings of the recipe, at its serving weight now (150 g).
    client.post(f"/meal/{meal['id']}/scale-items",
                data={"item_ids": str(lentils), "amount": "1 srv", "name": "Lentil soup",
                      "recipe_id": str(meal["soup"])})
    assert _amount(lentils) == pytest.approx(150.0)

    # Several items: Bowl added again as individual ingredients (3 foods, 250 g).
    resp = client.post(f"/meal/{meal['id']}/add-recipe",
                       data={"recipe_id": meal["bowl"], "amount": "1 serving", "mode": "ingredients"},
                       follow_redirects=False)
    ids = [int(x) for x in parse_qs(urlsplit(resp.headers["location"]).query)["added_ids"][0].split(",")]
    before = [_amount(i) for i in ids]
    client.post(f"/meal/{meal['id']}/scale-items",
                data={"item_ids": ",".join(map(str, ids)), "amount": f"{sum(before) * 2} g", "name": "Bowl"})
    assert [_amount(i) for i in ids] == pytest.approx([b * 2 for b in before])

    resp = client.post(f"/meal/{meal['id']}/scale-items",
                       data={"item_ids": str(lentils), "amount": "lots", "name": "Lentil soup"},
                       follow_redirects=False)
    assert "add_error=Lentil+soup" in resp.headers["location"]
    assert _amount(lentils) == pytest.approx(150.0)
    # Another meal's item isn't touched.
    with _db.get_db() as conn:
        other = _db.meal_create(conn, "Dinner", "2026-01-05")
        other_item = _db.meal_add_food(conn, other, OATS, "Oats", 10.0, "g")
    client.post(f"/meal/{meal['id']}/scale-items", data={"item_ids": str(other_item), "amount": "99"})
    assert _amount(other_item) == pytest.approx(10.0)


def test_foods_and_whole_views_show_edit_buttons(meal, client):
    oats, lentils = _item_id(meal["id"], "Oats"), _item_id(meal["id"], "Lentils")
    page = client.get(f"/meal/{meal['id']}?item_view=foods").text
    # Oats (logged once) and Lentils open their item's own Edit; Almond milk has none.
    assert f'action="/meal/{meal["id"]}/update/{oats}"' in page
    assert f'action="/meal/{meal["id"]}/update/{lentils}"' in page
    assert "Changes the Oats you logged yourself. The part inside Bowl stays as it is." in page
    assert page.count(">Edit</summary>") == 2
    page = client.get(f"/meal/{meal['id']}?item_view=whole").text
    bowl = _item_id(meal["id"], "Bowl")
    assert f'action="/meal/{meal["id"]}/update/{bowl}"' in page
    assert f'action="/meal/{meal["id"]}/scale-items"' in page  # Lentil soup, gathered
    assert page.count(">Edit</summary>") == 3


def test_added_line_has_edit(meal, client):
    oats = _item_id(meal["id"], "Oats")
    page = client.get(f"/meal/{meal['id']}?added=Oats&added_amount=30+g&added_ids={oats}").text
    added = page.split('id="just-added"')[1].split('id="sec-items"')[0]
    assert f'action="/meal/{meal["id"]}/update/{oats}"' in added
    assert "Change what you just added: Oats" in added and ">Undo</button>" in added
    resp = client.post(f"/meal/{meal['id']}/add-recipe",
                       data={"recipe_id": meal["bowl"], "amount": "1 serving", "mode": "ingredients"},
                       follow_redirects=False)
    added = client.get(resp.headers["location"]).text.split('id="just-added"')[1].split('id="sec-items"')[0]
    assert f'action="/meal/{meal["id"]}/scale-items"' in added
    assert 'name="recipe_id" value="%d"' % meal["bowl"] in added
    # An id no longer in the meal gets neither Edit nor Undo.
    added = client.get(f"/meal/{meal['id']}?added=Gone&added_ids=999999").text.split('id="just-added"')[1]
    assert ">Undo</button>" not in added.split("</div>\n  </div>")[0]
