"""
test_export_starter_data.py — scripts/export_starter_data.py: a starred
recipe pulls in its non-starred ingredient foods (prefixing their exported
name so every starter item stays "* "-prefixed), and a sub-recipe
"ingredient" is skipped with a warning rather than exported broken.
"""
import importlib.util
import json
import pathlib
import sqlite3
import sys

import pytest

import db as _db

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "export_starter_data", REPO_ROOT / "scripts" / "export_starter_data.py"
)
export_starter_data = importlib.util.module_from_spec(_SPEC)
sys.modules["export_starter_data"] = export_starter_data
_SPEC.loader.exec_module(export_starter_data)


def _add_food(conn: sqlite3.Connection, fdc_id: int, name: str) -> None:
    _db.cache_food(
        conn, fdc_id, name, "User Drafted", None, None, None,
        {"protein_g": 5.0, "calories": 50.0}, user_drafted=True,
    )


def test_recipe_auto_includes_non_starred_ingredient(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Starred Beans")
        _add_food(conn, 2, "Unstarred Rice")  # not renamed with the "* " prefix
        rid = _db.recipe_create(conn, name="* Starred Recipe", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, rid, 1, "* Starred Beans", 100, "g")
        _db.recipe_add_ingredient(conn, rid, 2, "Unstarred Rice", 100, "g")

    output = tmp_path / "starter_data.json"
    monkeypatch.setattr(export_starter_data, "OUTPUT", output)

    assert export_starter_data.main() == 0
    data = json.loads(output.read_text())

    food_names = {f["name"] for f in data["foods"]}
    assert "* Starred Beans" in food_names
    assert "Unstarred Rice" not in food_names
    assert "* Unstarred Rice" in food_names  # auto-included, and prefixed on export
    assert all(f["name"].startswith("* ") for f in data["foods"])
    assert [r["name"] for r in data["recipes"]] == ["* Starred Recipe"]

    # The recipe's ingredient reference must use the same (now-prefixed)
    # name as the foods list, since demo_data.load_demo_data() resolves
    # fdc_ids by looking up each ingredient's food name among DEMO_FOODS.
    recipe = data["recipes"][0]
    ingredient_names = {name for name, _amount, _unit, _kind in recipe["ingredients"]}
    assert ingredient_names == {"* Starred Beans", "* Unstarred Rice"}


def test_star_without_trailing_space_is_recognized_and_normalized(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "*Beans")  # starred, but no space after the "*"
        _db.pantry_add(conn, "*Beans", 1, "")
        rid = _db.recipe_create(conn, name="*Bean Bowl", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, rid, 1, "*Beans", 100, "g")

    output = tmp_path / "starter_data.json"
    monkeypatch.setattr(export_starter_data, "OUTPUT", output)

    assert export_starter_data.main() == 0
    data = json.loads(output.read_text())

    assert [f["name"] for f in data["foods"]] == ["* Beans"]
    assert data["pantry"] == []  # the pantry always ships empty
    assert data["recipes"][0]["name"] == "* Bean Bowl"


def test_recipe_referencing_subrecipe_is_exported_after_it(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, capsys,
) -> None:
    """A sub-recipe ingredient exports as a "recipe"-kind entry, and the
    sub-recipe is listed BEFORE the recipe that uses it — load_demo_data()
    needs its new id in hand before it can link the parent."""
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Starred Beans")
        sub_rid = _db.recipe_create(conn, name="* Sub Recipe", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, sub_rid, 1, "* Starred Beans", 100, "g")
        outer_rid = _db.recipe_create(conn, name="* Outer Recipe", description="", servings=1, instructions="")
        # A sub-recipe ingredient uses fdc_id=0 as a sentinel (see
        # web/backend.py recipe_ingredient_add_recipe) plus ref_recipe_id.
        _db.recipe_add_ingredient(conn, outer_rid, 0, "* Sub Recipe", 1, "1 serving",
                                   ref_recipe_id=sub_rid)

    output = tmp_path / "starter_data.json"
    monkeypatch.setattr(export_starter_data, "OUTPUT", output)

    assert export_starter_data.main() == 0
    data = json.loads(output.read_text())

    assert [r["name"] for r in data["recipes"]] == ["* Sub Recipe", "* Outer Recipe"]
    outer = data["recipes"][1]
    assert outer["ingredients"] == [["* Sub Recipe", 1.0, "1 serving", "recipe"]]
    # The sub-recipe is not a food, so it must not be faked into the foods list.
    assert "* Sub Recipe" not in {f["name"] for f in data["foods"]}


def test_unstarred_subrecipe_is_auto_included(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, capsys,
) -> None:
    """Same convenience starred recipes get for their ingredient foods: a
    sub-recipe you never starred still ships, prefixed on export only."""
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Starred Beans")
        sub_rid = _db.recipe_create(conn, name="Plain Sub", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, sub_rid, 1, "* Starred Beans", 100, "g")
        outer_rid = _db.recipe_create(conn, name="* Outer Recipe", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, outer_rid, 0, "Plain Sub", 2, "servings",
                                   ref_recipe_id=sub_rid)

    output = tmp_path / "starter_data.json"
    monkeypatch.setattr(export_starter_data, "OUTPUT", output)

    assert export_starter_data.main() == 0
    data = json.loads(output.read_text())

    assert [r["name"] for r in data["recipes"]] == ["* Plain Sub", "* Outer Recipe"]
    assert data["recipes"][1]["ingredients"] == [["* Plain Sub", 2.0, "servings", "recipe"]]
    assert "auto-including recipe" in capsys.readouterr().err


def test_recipe_is_skipped_when_its_subrecipe_was_deleted(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, capsys,
) -> None:
    """db.recipe_delete() leaves the ingredient row behind with ref_recipe_id
    NULL, ref_recipe_deleted 1 and fdc_id 0 — no food and no recipe to point
    at, so the recipe carrying it is skipped instead of being followed into a
    food lookup that cannot succeed."""
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Starred Beans")
        sub_rid = _db.recipe_create(conn, name="* Sub Recipe", description="", servings=1, instructions="")
        rid = _db.recipe_create(conn, name="* Outer Recipe", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, rid, 1, "* Starred Beans", 100, "g")
        _db.recipe_add_ingredient(conn, rid, 0, "* Sub Recipe", 1, "1 serving",
                                   ref_recipe_id=sub_rid)
        _db.recipe_delete(conn, sub_rid)

    output = tmp_path / "starter_data.json"
    monkeypatch.setattr(export_starter_data, "OUTPUT", output)

    assert export_starter_data.main() == 0
    data = json.loads(output.read_text())

    assert [r["name"] for r in data["recipes"]] == []
    assert "has been deleted" in capsys.readouterr().err


def test_only_redistributable_gi_values_are_exported(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GI from the 2008 tables or typed in by hand ships; GI from the
    Atkinson 2021 tables never does (their licence forbids redistribution),
    nor does a source label NuMa doesn't recognise."""
    with _db.get_db() as conn:
        for fdc_id, source in [
            (1, "Atkinson 2008 international GI tables (carried forward; year of test not recorded): “X”"),
            (2, "Foster-Powell 2008 reference table, Table A1 (normal): X"),
            (3, None),  # typed in by hand
            (4, "Atkinson 2021 international GI tables, Supplemental Table 1 (ISO 26642:2010 method): “X”"),
            (5, "Some web page"),
        ]:
            _add_food(conn, fdc_id, f"* Food {fdc_id}")
            _db.upsert_food_annotation(conn, fdc_id, gi_estimate=40.0 + fdc_id, gi_source=source)
        _add_food(conn, 6, "* No GI")

    output = tmp_path / "starter_data.json"
    monkeypatch.setattr(export_starter_data, "OUTPUT", output)
    assert export_starter_data.main() == 0
    gi = {f["fdc_id"]: f.get("gi") for f in json.loads(output.read_text())["foods"]}

    assert gi[1]["estimate"] == 41.0 and gi[1]["source"].startswith("Atkinson 2008")
    assert gi[2]["source"].startswith("Foster-Powell 2008")
    assert gi[3] == {"estimate": 43.0, "source": None}
    assert gi[4] is None
    assert gi[5] is None
    assert gi[6] is None


def test_recipes_ship_a_permanent_uid_not_the_curators_recipe_id(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Beans")
        rid = _db.recipe_create(conn, name="* Bean Bowl", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, rid, 1, "* Beans", 100, "g")

    output = tmp_path / "starter_data.json"
    monkeypatch.setattr(export_starter_data, "OUTPUT", output)
    assert export_starter_data.main() == 0
    first = json.loads(output.read_text())["recipes"][0]
    assert "source_recipe_id" not in first
    with _db.get_db() as conn:
        stamped = conn.execute("SELECT starter_uid FROM recipes WHERE id = ?", (rid,)).fetchone()[0]
    assert first["uid"] == stamped

    assert export_starter_data.main() == 0  # exporting again keeps the same uid
    assert json.loads(output.read_text())["recipes"][0]["uid"] == stamped
