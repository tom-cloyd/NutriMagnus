"""
Tests for logged recipe amounts shown as servings AND grams, and the
serving-weight safeguard (meal_items.serving_grams): a meal stores recipe
amounts in servings, so when the recipe's serving weight changes after
logging, the meal page asks whether to keep the grams originally logged.
See web/backend.py _annotate_recipe_amounts() and templates/_recipe_amount.html.
"""
import json

import pytest
from fastapi.testclient import TestClient

import db as _db
import web.backend as backend


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


def _food(db_conn, fdc_id=1):
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (fdc_id, "Lentil Mush", "Branded", json.dumps({"calories": 100.0, "protein_g": 9.0}), "[]"),
    )


@pytest.fixture()
def weighed(db_conn):
    """A 4-serving recipe of 1200 g (300 g/serving), logged as 1 serving."""
    _food(db_conn)
    rid = _db.recipe_create(db_conn, name="Stew", description="", servings=4, instructions="")
    _db.recipe_add_ingredient(db_conn, rid, 1, "Lentil Mush", 1200.0, "g")
    mid = _db.meal_create(db_conn, "Lunch", "2026-09-10")
    _db.meal_add_recipe(db_conn, mid, rid, "Stew", 1.0, "1 serving")
    db_conn.commit()
    item_id = db_conn.execute("SELECT id FROM meal_items WHERE meal_id = ?", (mid,)).fetchone()["id"]
    return {"recipe": rid, "meal": mid, "item": item_id}


def _item(db_conn, item_id):
    return db_conn.execute("SELECT amount, unit, serving_grams FROM meal_items WHERE id = ?", (item_id,)).fetchone()


def _set_servings(db_conn, rid, servings):
    db_conn.execute("UPDATE recipes SET servings = ? WHERE id = ?", (servings, rid))
    db_conn.commit()


class TestAmountDisplay:
    def test_meal_page_shows_servings_and_grams_with_footnote(self, client, weighed):
        html = client.get(f"/meal/{weighed['meal']}").text
        assert "1&thinsp;serving" in html
        assert "(300&thinsp;g)" in html
        assert 'id="recipe-weight-note"' in html

    def test_weight_unknown_when_serving_weight_cannot_be_worked_out(self, client, db_conn):
        _food(db_conn)
        rid = _db.recipe_create(db_conn, name="Soup", description="", servings=2, instructions="")
        _db.recipe_add_ingredient(db_conn, rid, 1, "Lentil Mush", 0.0, "a handful (weight not known)")
        mid = _db.meal_create(db_conn, "Dinner", "2026-09-10")
        _db.meal_add_recipe(db_conn, mid, rid, "Soup", 2.0, "2 servings")
        db_conn.commit()
        html = client.get(f"/meal/{mid}").text
        assert "2&thinsp;servings" in html
        assert "weight unknown" in html

    def test_food_only_meal_has_no_footnote(self, client, db_conn):
        _food(db_conn)
        mid = _db.meal_create(db_conn, "Snack", "2026-09-10")
        _db.meal_add_food(db_conn, mid, 1, "Lentil Mush", 50.0, "g")
        db_conn.commit()
        assert 'id="recipe-weight-note"' not in client.get(f"/meal/{mid}").text

    def test_day_page_and_search_show_grams(self, client, weighed):
        assert "(300&thinsp;g)" in client.get(f"/meal/{weighed['meal']}/day").text
        assert "(300&thinsp;g)" in client.get("/meals/search?q=Stew").text

    def test_print_page_shows_grams(self, client, weighed):
        assert "(300&thinsp;g)" in client.get(f"/meal/{weighed['meal']}/print").text


class TestServingWeightSafeguard:
    def test_serving_weight_recorded_on_first_view(self, client, db_conn, weighed):
        assert _item(db_conn, weighed["item"])["serving_grams"] is None
        client.get(f"/meal/{weighed['meal']}")
        assert _item(db_conn, weighed["item"])["serving_grams"] == pytest.approx(300.0)

    def test_changed_servings_count_shows_warning(self, client, db_conn, weighed):
        client.get(f"/meal/{weighed['meal']}")
        _set_servings(db_conn, weighed["recipe"], 2)  # now 600 g per serving
        html = client.get(f"/meal/{weighed['meal']}").text
        assert "serving size has changed since you logged it" in html
        assert "Keep the 300&thinsp;g I logged (change to 0.5 servings)" in html
        assert "review on the meal page" in client.get(f"/meal/{weighed['meal']}/day").text

    def test_keep_rescales_servings_to_logged_grams(self, client, db_conn, weighed):
        client.get(f"/meal/{weighed['meal']}")
        _set_servings(db_conn, weighed["recipe"], 2)
        client.post(f"/meal/{weighed['meal']}/item/{weighed['item']}/serving-weight", data={"choice": "keep"})
        row = _item(db_conn, weighed["item"])
        assert row["amount"] == pytest.approx(0.5)
        assert row["unit"] == "0.5 servings"
        assert row["serving_grams"] == pytest.approx(600.0)
        assert "serving size has changed" not in client.get(f"/meal/{weighed['meal']}").text

    def test_accept_keeps_servings_count(self, client, db_conn, weighed):
        client.get(f"/meal/{weighed['meal']}")
        _set_servings(db_conn, weighed["recipe"], 2)
        client.post(f"/meal/{weighed['meal']}/item/{weighed['item']}/serving-weight", data={"choice": "accept"})
        row = _item(db_conn, weighed["item"])
        assert row["amount"] == pytest.approx(1.0)
        assert row["serving_grams"] == pytest.approx(600.0)
        assert "serving size has changed" not in client.get(f"/meal/{weighed['meal']}").text

    def test_editing_servings_reconfirms_current_weight(self, client, db_conn, weighed):
        client.get(f"/meal/{weighed['meal']}")
        _set_servings(db_conn, weighed["recipe"], 2)
        client.post(f"/meal/{weighed['meal']}/update/{weighed['item']}", data={"amount": "1.5"})
        row = _item(db_conn, weighed["item"])
        assert row["amount"] == pytest.approx(1.5)
        assert row["serving_grams"] == pytest.approx(600.0)

    def test_small_rounding_difference_is_not_a_change(self):
        assert not backend._serving_weight_changed(300.0, 300.4)
        assert backend._serving_weight_changed(300.0, 310.0)
        assert not backend._serving_weight_changed(None, 300.0)
        assert not backend._serving_weight_changed(300.0, None)
