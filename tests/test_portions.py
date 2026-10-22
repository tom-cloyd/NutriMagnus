"""
Tests for numa_app/services/portions.py — _ing_amount_display() had zero
coverage before this was added (found in a 2026-08-17 weekly maintenance
sweep test-coverage audit) despite fixing a real save-rejection bug: the
previous version appended a density/volume estimate like "(≈ 120 g)" to the
displayed amount, and re-parsing that same string on inline edit failed
unless the user manually stripped the estimate back out first.
"""
from numa_app.services.portions import _ing_amount_display


def test_ing_amount_display_never_appends_an_estimate() -> None:
    # A label that already contains a number is returned as typed, with no
    # parenthetical estimate tacked on — the bug this function's docstring
    # describes fixing.
    result = _ing_amount_display("1/2 cup", 120.0, "Flour")
    assert "≈" not in result
    assert "(" not in result


def test_ing_amount_display_round_trips_through_reparse() -> None:
    from numa_app.services.portions import _parse_portion_input

    displayed = _ing_amount_display("150 g", 150.0, "Rice")
    reparsed = _parse_portion_input(displayed, [])
    assert reparsed is not None


def test_ing_amount_display_legacy_bare_unit_falls_back_to_grams() -> None:
    # A legacy row with no quantity baked into the unit label (just "cup")
    # falls back to the known gram weight so the string still starts with a
    # re-parseable number instead of a bare, quantity-less unit.
    result = _ing_amount_display("cup", 120.0, "Flour")
    assert result == "120 g"


def test_ing_amount_display_no_grams_returns_label_unchanged() -> None:
    result = _ing_amount_display("2 tbsp", None, "Oil")
    assert result == "2 tbsp"


def test_stored_portion_label_reads_back() -> None:
    """"2 p1" is stored as "2 × 1 large egg" and "p1" as "1 large egg"; both
    must read back, at the portion's weight now, or re-saving an unchanged
    amount fails with 'Unit "×" not recognized'."""
    from numa_app.services.portions import _parse_portion_input

    portions = [{"description": "1 large egg", "gram_weight": 50.0}]
    assert _parse_portion_input("2 × 1 large egg", portions) == (100.0, "2 × 1 large egg")
    assert _parse_portion_input("1.5 x 1 Large  Egg", portions) == (75.0, "1.5 × 1 large egg")
    assert _parse_portion_input("1 large egg", portions) == (50.0, "1 large egg")
    assert _parse_portion_input("2 × 1 small egg", portions) is None        # portion gone
    # Ordinary input is untouched by the portion-label reading.
    assert _parse_portion_input("150 g", portions)[0] == 150.0


# --- parse_recipe_amount(): what can be typed for a recipe in a meal --------

import pytest

from numa_app.services.entry_parse import EntryError
from numa_app.services.portions import parse_recipe_amount

_MARINARA = {"servings": 11.74, "serving_size": "2/3 cup", "total_weight": 1542.0,
             "total_weight_unit": "g", "total_volume": None, "total_volume_unit": None}


@pytest.mark.parametrize("typed", ["1⅛ srv", "1 1/8 servings", "1.125 srv", "1.125 Servings",
                                   "1.125 servings (1.13 servings)"])
def test_recipe_amount_servings(typed) -> None:
    # The meal page's number box was held to 0.01 steps, so 1.125 couldn't go in.
    assert parse_recipe_amount(typed, _MARINARA, 131.3)[0] == pytest.approx(1.125)


@pytest.mark.parametrize("typed", ["29", "29 g", "29 gr"])
def test_recipe_amount_bare_number_is_grams(typed) -> None:
    # As for a food: "29" meant as grams used to become 29 servings.
    assert parse_recipe_amount(typed, _MARINARA, 58.0)[0] == pytest.approx(0.5)


def test_recipe_amount_bare_number_needs_a_serving_weight() -> None:
    with pytest.raises(EntryError, match="on its own means grams"):
        parse_recipe_amount("29", _MARINARA, None)


def test_recipe_amount_volume_through_serving_description() -> None:
    # No Total yield volume, but the serving is "2/3 cup": 3/4 c = 1.125 servings.
    assert parse_recipe_amount("3/4 c", _MARINARA, None) == (pytest.approx(1.125), "3/4 c")


def test_recipe_amount_volume_through_total_volume() -> None:
    r = dict(_MARINARA, total_volume=2.0, total_volume_unit="l")
    assert parse_recipe_amount("500 ml", r, None)[0] == pytest.approx(11.74 / 4)


def test_recipe_amount_weight_through_serving_grams() -> None:
    assert parse_recipe_amount("200 g", _MARINARA, 100.0)[0] == pytest.approx(2.0)


@pytest.mark.parametrize("typed,serving_g,serving_size,needle", [
    ("200 g", None, "2/3 cup", "weighs"),
    ("1 cup", 100.0, "1 bowl", "volume"),
    ("2 handfuls", 100.0, "2/3 cup", "unit"),
    ("0", 100.0, "2/3 cup", "more than zero"),
    ("lots", 100.0, "2/3 cup", "isn.t an amount"),
    ("", 100.0, "2/3 cup", "Nothing"),
])
def test_recipe_amount_refusals_say_why(typed, serving_g, serving_size, needle) -> None:
    with pytest.raises(EntryError, match=needle):
        parse_recipe_amount(typed, dict(_MARINARA, serving_size=serving_size), serving_g)
