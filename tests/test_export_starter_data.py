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
    ingredient_names = {name for name, _amount, _unit in recipe["ingredients"]}
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
    assert data["pantry"] == ["* Beans"]
    assert data["recipes"][0]["name"] == "* Bean Bowl"


def test_recipe_referencing_subrecipe_is_skipped(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, capsys,
) -> None:
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

    recipe_names = {r["name"] for r in data["recipes"]}
    assert "* Sub Recipe" in recipe_names
    assert "* Outer Recipe" not in recipe_names
    assert "sub-recipe" in capsys.readouterr().err
