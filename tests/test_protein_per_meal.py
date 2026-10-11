"""
Tests for numa_app/services/protein_per_meal.py and its display on the meal
and day pages.
"""
import json

import pytest

import db as _db
from numa_app.services import protein_per_meal as ppm


class _P:
    def __init__(self, age, weight_kg):
        self.age, self.weight_kg = age, weight_kg


def test_adult_amount_scales_with_weight():
    a = ppm.per_meal_amount(_P(40, 80.0))
    assert (a["low_g"], a["high_g"], a["basis"]) == (20.0, 32.0, "adult")
    assert (a["leucine_low_g"], a["leucine_high_g"]) == (0.7, 3.0)


def test_older_adult_uses_prot_age():
    a = ppm.per_meal_amount(_P(65, 80.0))
    assert (a["low_g"], a["high_g"], a["leucine_low_g"], a["basis"]) == (25.0, 30.0, 2.5, "older")


def test_no_profile_uses_general_dose():
    assert ppm.per_meal_amount(None)["basis"] == "general"


def test_meal_check_prefers_dcp_and_never_flags_too_much():
    a = ppm.per_meal_amount(_P(40, 80.0))
    c = ppm.meal_check(18.0, 30.0, 1.9, a)
    assert c["is_dcp"] and c["protein_g"] == 18.0 and not c["reached"] and c["leucine_reached"]
    big = ppm.meal_check(90.0, 100.0, 8.0, a)
    assert big["reached"] and set(big) == {"protein_g", "is_dcp", "reached", "leucine_g", "leucine_reached"}
    raw = ppm.meal_check(None, 25.0, None, a)
    assert not raw["is_dcp"] and raw["reached"] and raw["leucine_reached"] is None


def test_meal_and_day_pages_show_protein_per_meal(db_conn):
    from fastapi.testclient import TestClient
    from web import backend
    db_conn.execute("INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
                    (991, "Tofu test", "SR Legacy",
                     json.dumps({"calories": 144, "protein_g": 17.0, "carbs_g": 3.0, "fat_g": 9.0,
                                 "aa_leucine_g": 1.3}), "[]"))
    db_conn.commit()
    client = TestClient(backend.app)
    meal_id = int(client.post("/meals/create", data={"name": "Dinner", "meal_date": "2026-07-20"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    client.post(f"/meal/{meal_id}/add", data={"fdc_id": 991, "food_name": "Tofu test", "portion_str": "200 g"},
                follow_redirects=False)
    html = client.get(f"/meal/{meal_id}").text
    assert "Protein per meal:" in html and "/manual#protein-per-meal" in html
    day = client.get("/summary/2026-07-20").text
    assert "Protein per meal:" in day and f'href="/meal/{meal_id}">Dinner</a>' in day
