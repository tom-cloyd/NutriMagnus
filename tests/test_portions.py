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
    amount fails with 'Unit "×" not recognised'."""
    from numa_app.services.portions import _parse_portion_input

    portions = [{"description": "1 large egg", "gram_weight": 50.0}]
    assert _parse_portion_input("2 × 1 large egg", portions) == (100.0, "2 × 1 large egg")
    assert _parse_portion_input("1.5 x 1 Large  Egg", portions) == (75.0, "1.5 × 1 large egg")
    assert _parse_portion_input("1 large egg", portions) == (50.0, "1 large egg")
    assert _parse_portion_input("2 × 1 small egg", portions) is None        # portion gone
    # Ordinary input is untouched by the portion-label reading.
    assert _parse_portion_input("150 g", portions)[0] == 150.0
