"""Tests for numa_app.services.food_ids.classify_food_id()."""
from numa_app.services.food_ids import classify_food_id


def test_usda_id():
    assert classify_food_id(171477) == ("171477", "USDA")


def test_off_id():
    assert classify_food_id(-2_500_000_000) == ("-2500000000", "OFF")


def test_cnf_id():
    assert classify_food_id(-3_500_000_000) == ("-3500000000", "CNF")


def test_user_drafted_id_gets_ud_label():
    # db.next_user_drafted_fdc_id() allocates -1, -2, -3, ... — well outside
    # every _SYNTHETIC_ID_RANGES block, which all start at -2_000_000_000 or
    # below.
    assert classify_food_id(-1) == ("UD1", "User-drafted")
    assert classify_food_id(-5) == ("UD5", "User-drafted")
    assert classify_food_id(-42) == ("UD42", "User-drafted")


def test_recipe_id_takes_priority():
    assert classify_food_id(171477, recipe_id=9) == ("9", "Recipe")


def test_none_fdc_id_and_no_recipe_id_returns_none():
    assert classify_food_id(None) is None
