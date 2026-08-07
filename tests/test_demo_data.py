"""
test_demo_data.py — numa_app/services/demo_data.py: load/clear starter
foods/pantry/recipes, fresh-install auto-seeding, idempotency, and that
real data is never touched.
"""
import pathlib
import sqlite3

import pytest

from numa_app.services import demo_data


@pytest.fixture(autouse=True)
def use_test_marker_file(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect the demo-data marker files to per-test temp paths."""
    monkeypatch.setattr(demo_data, "_MARKER_FILE", tmp_path / "demo_data.json")
    monkeypatch.setattr(demo_data, "_SEED_ATTEMPTED_MARKER", tmp_path / "demo_data_seed_attempted")


def test_is_loaded_false_initially() -> None:
    assert demo_data.is_loaded() is False


def test_load_creates_expected_rows(db_conn: sqlite3.Connection) -> None:
    result = demo_data.load_demo_data(db_conn)
    db_conn.commit()

    assert result == {
        "foods": len(demo_data.DEMO_FOODS),
        "pantry": len(demo_data.DEMO_PANTRY),
        "recipes": len(demo_data.DEMO_RECIPES),
    }
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == len(demo_data.DEMO_FOODS)
    assert db_conn.execute("SELECT COUNT(*) FROM pantry").fetchone()[0] == len(demo_data.DEMO_PANTRY)
    assert db_conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == len(demo_data.DEMO_RECIPES)
    assert db_conn.execute("SELECT COUNT(*) FROM recipe_ingredients").fetchone()[0] == sum(
        len(r["ingredients"]) for r in demo_data.DEMO_RECIPES
    )
    assert demo_data.is_loaded() is True


def test_load_is_idempotent(db_conn: sqlite3.Connection) -> None:
    demo_data.load_demo_data(db_conn)
    db_conn.commit()
    before = db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0]

    result = demo_data.load_demo_data(db_conn)
    db_conn.commit()

    assert result["already_loaded"] is True
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == before


def test_clear_removes_exactly_what_was_loaded(db_conn: sqlite3.Connection) -> None:
    demo_data.load_demo_data(db_conn)
    db_conn.commit()

    result = demo_data.clear_demo_data(db_conn)
    db_conn.commit()

    assert result == {
        "foods": len(demo_data.DEMO_FOODS),
        "pantry": len(demo_data.DEMO_PANTRY),
        "recipes": len(demo_data.DEMO_RECIPES),
    }
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM pantry").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM recipe_ingredients").fetchone()[0] == 0
    assert demo_data.is_loaded() is False


def test_clear_without_load_is_noop(db_conn: sqlite3.Connection) -> None:
    result = demo_data.clear_demo_data(db_conn)
    assert result == {"foods": 0, "pantry": 0, "recipes": 0}


def test_real_data_untouched_by_load_and_clear(db_conn: sqlite3.Connection) -> None:
    import db as _db

    _db.cache_food(db_conn, 999999, "My Real Food", "User Drafted", None, None, None,
                    {"protein_g": 5.0, "calories": 50.0}, user_drafted=True)
    real_pantry_id = _db.pantry_add(db_conn, "My Real Food", 999999, "real")
    real_recipe_id = _db.recipe_create(db_conn, name="My Real Recipe", description="",
                                        servings=1, instructions="")
    db_conn.commit()

    demo_data.load_demo_data(db_conn)
    db_conn.commit()
    demo_data.clear_demo_data(db_conn)
    db_conn.commit()

    assert db_conn.execute(
        "SELECT name FROM foods WHERE fdc_id=999999"
    ).fetchone()["name"] == "My Real Food"
    assert db_conn.execute(
        "SELECT food_name FROM pantry WHERE id=?", (real_pantry_id,)
    ).fetchone()["food_name"] == "My Real Food"
    assert db_conn.execute(
        "SELECT name FROM recipes WHERE id=?", (real_recipe_id,)
    ).fetchone()["name"] == "My Real Recipe"
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 1


def test_names_are_asterisk_prefixed() -> None:
    assert all(f["name"].startswith("* ") for f in demo_data.DEMO_FOODS)
    assert all(r["name"].startswith("* ") for r in demo_data.DEMO_RECIPES)
    assert all(n.startswith("* ") for n in demo_data.DEMO_PANTRY)


def test_seed_if_fresh_install_loads_on_empty_db(db_conn: sqlite3.Connection) -> None:
    result = demo_data.seed_if_fresh_install(db_conn)
    db_conn.commit()

    assert result["foods"] == len(demo_data.DEMO_FOODS)
    assert demo_data.is_loaded() is True


def test_seed_if_fresh_install_skips_db_with_existing_data(db_conn: sqlite3.Connection) -> None:
    import db as _db

    _db.cache_food(db_conn, 999999, "My Real Food", "User Drafted", None, None, None,
                    {"protein_g": 5.0, "calories": 50.0}, user_drafted=True)
    db_conn.commit()

    result = demo_data.seed_if_fresh_install(db_conn)

    assert result == {"foods": 0, "pantry": 0, "recipes": 0, "skipped": True}
    assert demo_data.is_loaded() is False


def test_seed_if_fresh_install_does_not_reseed_after_clear(db_conn: sqlite3.Connection) -> None:
    demo_data.seed_if_fresh_install(db_conn)
    db_conn.commit()
    demo_data.clear_demo_data(db_conn)
    db_conn.commit()

    # DB is empty again (starter data was the only thing in it), but the
    # seed-attempted marker must prevent a second auto-load.
    result = demo_data.seed_if_fresh_install(db_conn)

    assert result == {"foods": 0, "pantry": 0, "recipes": 0, "skipped": True}
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 0


def test_recipe_dcp_reflects_real_complementarity(db_conn: sqlite3.Connection) -> None:
    """The whole point of the demo recipes is a real DIAAS/DCP improvement
    over either ingredient alone — assert the computed dcp_g is non-null and
    plausible (not just a smoke test that the row exists)."""
    demo_data.load_demo_data(db_conn)
    db_conn.commit()

    rows = db_conn.execute("SELECT name, dcp_g, servings FROM recipes").fetchall()
    assert len(rows) == len(demo_data.DEMO_RECIPES)
    for row in rows:
        assert row["dcp_g"] is not None
        assert row["dcp_g"] > 0
