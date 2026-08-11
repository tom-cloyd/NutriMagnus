"""
test_refresh_starter_data.py — scripts/refresh_starter_data.py: existing
starter_data.json entries are refreshed from the live cache by stable ID
(fdc_id for foods, source_recipe_id for recipes) rather than by name, and
nothing is ever dropped just because its live counterpart is gone.
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
    "refresh_starter_data", REPO_ROOT / "scripts" / "refresh_starter_data.py"
)
refresh_starter_data = importlib.util.module_from_spec(_SPEC)
sys.modules["refresh_starter_data"] = refresh_starter_data
_SPEC.loader.exec_module(refresh_starter_data)


def _add_food(conn: sqlite3.Connection, fdc_id: int, name: str, **nutrients) -> None:
    _db.cache_food(
        conn, fdc_id, name, "User Drafted", None, None, None,
        {"protein_g": 5.0, "calories": 50.0, **nutrients}, user_drafted=True,
    )


def _write_starter_data(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, data: dict) -> pathlib.Path:
    path = tmp_path / "starter_data.json"
    path.write_text(json.dumps(data))
    monkeypatch.setattr(refresh_starter_data, "STARTER_DATA_FILE", path)
    return path


def test_food_refreshed_from_cache_by_fdc_id(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Renamed Beans", protein_g=9.5)

    starter = {
        "foods": [{"fdc_id": 1, "name": "* Old Beans", "data_type": "User Drafted",
                    "nutrients": {"protein_g": 5.0, "calories": 50.0}, "portions": []}],
        "pantry": ["* Old Beans"],
        "recipes": [],
    }
    path = _write_starter_data(tmp_path, monkeypatch, starter)

    assert refresh_starter_data.main() == 0
    data = json.loads(path.read_text())

    assert data["foods"][0]["name"] == "* Renamed Beans"
    assert data["foods"][0]["nutrients"]["protein_g"] == 9.5
    assert data["pantry"] == ["* Renamed Beans"]  # tracked the rename


def test_food_not_in_cache_is_left_untouched(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    starter = {
        "foods": [{"fdc_id": 999, "name": "* Gone Food", "data_type": "User Drafted",
                    "nutrients": {"protein_g": 1.0}, "portions": []}],
        "pantry": [],
        "recipes": [],
    }
    path = _write_starter_data(tmp_path, monkeypatch, starter)

    assert refresh_starter_data.main() == 0
    data = json.loads(path.read_text())

    assert data["foods"] == starter["foods"]  # untouched, not dropped


def test_recipe_matched_by_source_id_survives_rename(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Beans")
        rid = _db.recipe_create(conn, name="* Renamed Recipe", description="new desc",
                                 servings=2, instructions="new steps")
        _db.recipe_add_ingredient(conn, rid, 1, "* Beans", 100, "g")

    starter = {
        "foods": [{"fdc_id": 1, "name": "* Beans", "data_type": "User Drafted",
                    "nutrients": {"protein_g": 5.0}, "portions": []}],
        "pantry": [],
        "recipes": [{"source_recipe_id": rid, "name": "* Old Recipe Name",
                      "description": "old desc", "servings": 1, "instructions": "old steps",
                      "ingredients": [["* Beans", 100, "g"]]}],
    }
    path = _write_starter_data(tmp_path, monkeypatch, starter)

    assert refresh_starter_data.main() == 0
    data = json.loads(path.read_text())

    recipe = data["recipes"][0]
    assert recipe["name"] == "* Renamed Recipe"
    assert recipe["description"] == "new desc"
    assert recipe["servings"] == 2
    assert recipe["instructions"] == "new steps"


def test_legacy_recipe_without_source_id_matched_by_name_and_backfilled(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Beans")
        rid = _db.recipe_create(conn, name="* Legacy Recipe", description="live desc",
                                 servings=1, instructions="")
        _db.recipe_add_ingredient(conn, rid, 1, "* Beans", 100, "g")

    starter = {
        "foods": [{"fdc_id": 1, "name": "* Beans", "data_type": "User Drafted",
                    "nutrients": {"protein_g": 5.0}, "portions": []}],
        "pantry": [],
        "recipes": [{"name": "* Legacy Recipe", "description": "stale desc",
                      "servings": 1, "instructions": "", "ingredients": [["* Beans", 100, "g"]]}],
    }
    path = _write_starter_data(tmp_path, monkeypatch, starter)

    assert refresh_starter_data.main() == 0
    data = json.loads(path.read_text())

    recipe = data["recipes"][0]
    assert recipe["source_recipe_id"] == rid  # backfilled for next time
    assert recipe["description"] == "live desc"


def test_recipe_with_no_live_match_left_untouched(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    starter = {
        "foods": [],
        "pantry": [],
        "recipes": [{"source_recipe_id": 999, "name": "* Deleted Recipe",
                      "description": "d", "servings": 1, "instructions": "",
                      "ingredients": []}],
    }
    path = _write_starter_data(tmp_path, monkeypatch, starter)

    assert refresh_starter_data.main() == 0
    data = json.loads(path.read_text())

    assert data["recipes"] == starter["recipes"]  # untouched, not dropped


def test_new_live_ingredient_is_auto_included(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Beans")
        _add_food(conn, 2, "* Rice")  # added to the recipe live, never exported
        rid = _db.recipe_create(conn, name="* Combo", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, rid, 1, "* Beans", 100, "g")
        _db.recipe_add_ingredient(conn, rid, 2, "* Rice", 50, "g")

    starter = {
        "foods": [{"fdc_id": 1, "name": "* Beans", "data_type": "User Drafted",
                    "nutrients": {"protein_g": 5.0}, "portions": []}],
        "pantry": [],
        "recipes": [{"source_recipe_id": rid, "name": "* Combo", "description": "",
                      "servings": 1, "instructions": "", "ingredients": [["* Beans", 100, "g"]]}],
    }
    path = _write_starter_data(tmp_path, monkeypatch, starter)

    assert refresh_starter_data.main() == 0
    data = json.loads(path.read_text())

    food_fdc_ids = {f["fdc_id"] for f in data["foods"]}
    assert food_fdc_ids == {1, 2}
    ingredient_names = {name for name, _amount, _unit in data["recipes"][0]["ingredients"]}
    assert ingredient_names == {"* Beans", "* Rice"}


def test_subrecipe_ingredient_leaves_recipe_untouched(
    db_conn: sqlite3.Connection, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, capsys,
) -> None:
    with _db.get_db() as conn:
        _add_food(conn, 1, "* Beans")
        sub_rid = _db.recipe_create(conn, name="* Sub", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, sub_rid, 1, "* Beans", 100, "g")
        outer_rid = _db.recipe_create(conn, name="* Outer", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, outer_rid, 0, "* Sub", 1, "1 serving", ref_recipe_id=sub_rid)

    starter = {
        "foods": [{"fdc_id": 1, "name": "* Beans", "data_type": "User Drafted",
                    "nutrients": {"protein_g": 5.0}, "portions": []}],
        "pantry": [],
        "recipes": [{"source_recipe_id": outer_rid, "name": "* Outer", "description": "",
                      "servings": 1, "instructions": "", "ingredients": []}],
    }
    path = _write_starter_data(tmp_path, monkeypatch, starter)

    assert refresh_starter_data.main() == 0
    data = json.loads(path.read_text())

    assert data["recipes"] == starter["recipes"]  # untouched
    assert "sub-recipe" in capsys.readouterr().err
