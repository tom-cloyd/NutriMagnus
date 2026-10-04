"""Tests for numa_app.services.food_ids: display codes (U171477, UD4, R21,
OFF3, ...) and the db.food_codes numbering behind outside-source codes."""
import db as _db
from numa_app.services.food_ids import classify_food_id, code_sort_key, code_source_name


def _cache(fdc_id: int, name: str = "x") -> None:
    with _db.get_db() as conn:
        _db.cache_food(conn, fdc_id=fdc_id, name=name, data_type="OFF", brand=None,
                       serving_size=100.0, serving_unit="g", nutrients={"protein_g": 1})


def test_usda_id():
    assert classify_food_id(171477) == ("U171477", "USDA")


def test_uncached_outside_source_food_shows_bare_prefix():
    assert classify_food_id(-2_500_000_000) == ("OFF", "OFF")
    assert classify_food_id(-3_500_000_000) == ("CNF", "CNF")


def test_outside_source_foods_numbered_per_source_in_arrival_order():
    _cache(-2_500_000_000)
    _cache(-3_500_000_000)
    _cache(-2_018_273_699)
    assert classify_food_id(-2_500_000_000) == ("OFF1", "OFF")
    assert classify_food_id(-2_018_273_699) == ("OFF2", "OFF")
    assert classify_food_id(-3_500_000_000) == ("CNF1", "CNF")


def test_outside_source_code_survives_delete_and_recache():
    _cache(-2_500_000_000)
    _cache(-2_600_000_000)
    with _db.get_db() as conn:
        _db.delete_cached_food(conn, -2_500_000_000)
    _cache(-2_500_000_000)
    assert classify_food_id(-2_500_000_000)[0] == "OFF1"


def test_recache_does_not_renumber():
    _cache(-2_500_000_000, "first")
    _cache(-2_500_000_000, "renamed")
    _cache(-2_600_000_000)
    assert classify_food_id(-2_600_000_000)[0] == "OFF2"


def test_init_db_backfills_foods_cached_before_codes_existed():
    with _db.get_db() as conn:
        conn.execute("DROP TRIGGER trg_foods_assign_code")
        conn.execute("INSERT INTO foods (fdc_id, name, nutrients_json) VALUES (-5100000000, 'a', '{}')")
        conn.execute("DELETE FROM food_codes")
    _db.init_db()
    assert classify_food_id(-5_100_000_000)[0] == "AFCD1"


def test_user_drafted_id_gets_ud_label():
    # db.next_user_drafted_fdc_id() allocates -1, -2, -3, ... — well outside
    # every _SYNTHETIC_ID_RANGES block, which all start at -2_000_000_000 or
    # below.
    assert classify_food_id(-1) == ("UD1", "User-drafted")
    assert classify_food_id(-5) == ("UD5", "User-drafted")
    assert classify_food_id(-42) == ("UD42", "User-drafted")


def test_recipe_id_takes_priority():
    assert classify_food_id(171477, recipe_id=9) == ("R9", "Recipe")


def test_none_fdc_id_and_no_recipe_id_returns_none():
    assert classify_food_id(None) is None


def test_code_source_name_prefers_longest_prefix():
    assert code_source_name("UD4").startswith("user-drafted")
    assert code_source_name("U171477").startswith("USDA")
    assert code_source_name("R21") == "recipe"
    assert code_source_name("CIQUAL5").startswith("French")
    assert code_source_name("XYZ") == ""


def test_code_sort_key_groups_by_prefix_then_numeric():
    codes = ["R10", "UD2", "R9", "U500", "OFF1", "", "U20"]
    assert sorted(codes, key=code_sort_key) == ["U20", "U500", "UD2", "R9", "R10", "OFF1", ""]


def test_parse_code_round_trips_every_kind():
    import pytest
    from numa_app.services.food_ids import parse_code
    _cache(-2_018_273_699)
    assert parse_code("U171477") == ("food", 171477)
    assert parse_code(" ud4 ") == ("food", -4)
    assert parse_code("r21") == ("recipe", 21)
    assert parse_code("OFF1") == ("food", -2_018_273_699)
    with pytest.raises(ValueError, match="No food has the code OFF9"):
        parse_code("OFF9")
    for bad in ("", "171477", "X5", "R", "R2a"):
        with pytest.raises(ValueError):
            parse_code(bad)
