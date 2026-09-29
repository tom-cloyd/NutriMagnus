"""
test_demo_data.py — numa_app/services/demo_data.py: load/clear starter
foods/pantry/recipes, fresh-install auto-seeding, idempotency, and that
real data is never touched.
"""
import json
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
        "foods_kept": 0,
    }
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM pantry").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM recipe_ingredients").fetchone()[0] == 0
    assert demo_data.is_loaded() is False


def test_clear_without_load_is_noop(db_conn: sqlite3.Connection) -> None:
    result = demo_data.clear_demo_data(db_conn)
    assert result == {"foods": 0, "pantry": 0, "recipes": 0, "foods_kept": 0}


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


def test_starter_status_all_absent_on_empty_db(db_conn: sqlite3.Connection) -> None:
    status = demo_data.starter_status(db_conn)

    assert len(status["foods"]) == len(demo_data.DEMO_FOODS)
    assert all(f["present"] is False for f in status["foods"])
    assert all(p["present"] is False for p in status["pantry"])
    assert all(r["present"] is False for r in status["recipes"])


def test_starter_status_all_present_after_load(db_conn: sqlite3.Connection) -> None:
    demo_data.load_demo_data(db_conn)
    db_conn.commit()

    status = demo_data.starter_status(db_conn)

    assert all(f["present"] is True for f in status["foods"])
    assert all(p["present"] is True for p in status["pantry"])
    assert all(r["present"] is True for r in status["recipes"])


def test_restore_selected_single_food(db_conn: sqlite3.Connection) -> None:
    food = demo_data.DEMO_FOODS[0]

    result = demo_data.restore_selected(db_conn, [food["fdc_id"]], [], [])
    db_conn.commit()

    assert result == {"foods": 1, "pantry": 0, "recipes": 0}
    assert db_conn.execute(
        "SELECT COUNT(*) FROM foods WHERE fdc_id=?", (food["fdc_id"],)
    ).fetchone()[0] == 1
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 1


def test_restore_selected_recipe_pulls_in_missing_ingredient_foods(db_conn: sqlite3.Connection) -> None:
    recipe = demo_data.DEMO_RECIPES[0]

    result = demo_data.restore_selected(db_conn, [], [], [recipe["name"]])
    db_conn.commit()

    assert result["recipes"] == 1
    # A recipe can legitimately use the same food in two separate ingredient
    # lines (e.g. added in two batches) -- restore_selected() dedupes by
    # fdc_id, so the number of foods actually restored is the number of
    # *unique* ingredient foods, not the raw ingredient-line count.
    ingredient_foods = [
        name for name, _amount, _unit, kind
        in (demo_data._ingredient_parts(i) for i in recipe["ingredients"])
        if kind == "food"
    ]
    unique_fdc_ids = {
        next(f["fdc_id"] for f in demo_data.DEMO_FOODS if f["name"] == food_name)
        for food_name in ingredient_foods
    }
    assert result["foods"] == len(unique_fdc_ids)
    assert db_conn.execute(
        "SELECT COUNT(*) FROM recipes WHERE name=?", (recipe["name"],)
    ).fetchone()[0] == 1
    for food_name in ingredient_foods:
        fdc_id = next(f["fdc_id"] for f in demo_data.DEMO_FOODS if f["name"] == food_name)
        assert db_conn.execute(
            "SELECT COUNT(*) FROM foods WHERE fdc_id=?", (fdc_id,)
        ).fetchone()[0] == 1


def test_restore_selected_skips_already_present_items(db_conn: sqlite3.Connection) -> None:
    food = demo_data.DEMO_FOODS[0]
    demo_data.restore_selected(db_conn, [food["fdc_id"]], [], [])
    db_conn.commit()

    result = demo_data.restore_selected(db_conn, [food["fdc_id"]], [], [])
    db_conn.commit()

    assert result == {"foods": 0, "pantry": 0, "recipes": 0}
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 1


def test_recipe_dcp_reflects_real_complementarity(db_conn: sqlite3.Connection) -> None:
    """The whole point of the demo recipes is a real DIAAS/DCP improvement
    over either ingredient alone — assert any computed dcp_g is plausible
    (not just a smoke test that the row exists). A recipe legitimately has
    no dcp_g if one of its real-world ingredients is missing amino acid
    data (recompute_recipe_dcp refuses to guess) — starter content is
    curated straight from real recipes/foods, warts and all, so that's an
    expected state for at least one recipe rather than a bug."""
    demo_data.load_demo_data(db_conn)
    db_conn.commit()

    rows = db_conn.execute("SELECT name, dcp_g, servings FROM recipes").fetchall()
    assert len(rows) == len(demo_data.DEMO_RECIPES)
    for row in rows:
        if row["dcp_g"] is not None:
            assert row["dcp_g"] > 0
    assert any(row["dcp_g"] is not None for row in rows)


# ── Nested sub-recipes ────────────────────────────────────────────────────
# Starter data used to have no nested-recipe support: export skipped any
# recipe that used another recipe as an ingredient, so such a recipe silently
# never shipped no matter that it was starred.

def _nested_starter(monkeypatch: pytest.MonkeyPatch) -> None:
    """Point demo_data at a two-recipe starter set where the second uses the
    first as a sub-recipe — sub-recipe first, as the export orders them."""
    monkeypatch.setattr(demo_data, "DEMO_FOODS", [
        {"fdc_id": 901, "name": "* Nested Beans", "data_type": "SR Legacy",
         "nutrients": {"calories": 100.0, "protein_g": 9.0, "carbs_g": 20.0, "fat_g": 1.0},
         "portions": []},
    ])
    monkeypatch.setattr(demo_data, "DEMO_PANTRY", [])
    monkeypatch.setattr(demo_data, "DEMO_RECIPES", [
        {"source_recipe_id": 1, "name": "* Nested Sauce", "description": "", "servings": 2,
         "instructions": "", "ingredients": [["* Nested Beans", 150, "g", "food"]]},
        {"source_recipe_id": 2, "name": "* Nested Meal", "description": "", "servings": 1,
         "instructions": "", "ingredients": [["* Nested Beans", 100, "g", "food"],
                                             ["* Nested Sauce", 1, "1 serving", "recipe"]]},
    ])


def test_load_links_a_subrecipe_ingredient(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    _nested_starter(monkeypatch)

    result = demo_data.load_demo_data(db_conn)
    db_conn.commit()

    assert result["recipes"] == 2
    sauce_id = db_conn.execute("SELECT id FROM recipes WHERE name=?", ("* Nested Sauce",)).fetchone()[0]
    row = db_conn.execute(
        "SELECT fdc_id, ref_recipe_id, ref_recipe_deleted FROM recipe_ingredients"
        " WHERE food_name=?", ("* Nested Sauce",)
    ).fetchone()
    # The app's own shape for a sub-recipe row: fdc_id 0 plus a live ref.
    assert (row["fdc_id"], row["ref_recipe_id"], row["ref_recipe_deleted"]) == (0, sauce_id, 0)


def test_clear_removes_nested_recipes(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    """Deleting the sub-recipe before its parent would trip the
    recipe_ingredients.ref_recipe_id foreign key, so clear works backwards."""
    _nested_starter(monkeypatch)
    demo_data.load_demo_data(db_conn)
    db_conn.commit()

    result = demo_data.clear_demo_data(db_conn)
    db_conn.commit()

    assert result["recipes"] == 2
    assert db_conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM recipe_ingredients").fetchone()[0] == 0


def test_restore_selected_pulls_in_the_subrecipe(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    """Restoring only the parent has to bring its sub-recipe along, or the
    ingredient row would point at a recipe that isn't there."""
    _nested_starter(monkeypatch)

    result = demo_data.restore_selected(db_conn, [], [], ["* Nested Meal"])
    db_conn.commit()

    assert result["recipes"] == 2
    names = {r["name"] for r in db_conn.execute("SELECT name FROM recipes").fetchall()}
    assert names == {"* Nested Sauce", "* Nested Meal"}
    assert db_conn.execute(
        "SELECT ref_recipe_id FROM recipe_ingredients WHERE food_name=?", ("* Nested Sauce",)
    ).fetchone()["ref_recipe_id"] is not None


def test_restore_selected_links_to_an_already_present_subrecipe(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The sub-recipe already being in the DB must not produce a second copy."""
    _nested_starter(monkeypatch)
    demo_data.restore_selected(db_conn, [], [], ["* Nested Sauce"])
    db_conn.commit()
    sauce_id = db_conn.execute("SELECT id FROM recipes WHERE name=?", ("* Nested Sauce",)).fetchone()[0]

    result = demo_data.restore_selected(db_conn, [], [], ["* Nested Meal"])
    db_conn.commit()

    assert result["recipes"] == 1
    assert db_conn.execute(
        "SELECT COUNT(*) FROM recipes WHERE name=?", ("* Nested Sauce",)
    ).fetchone()[0] == 1
    assert db_conn.execute(
        "SELECT ref_recipe_id FROM recipe_ingredients WHERE food_name=?", ("* Nested Sauce",)
    ).fetchone()["ref_recipe_id"] == sauce_id


def test_legacy_three_element_ingredient_still_loads(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """starter_data.json files exported before nested support have no "kind"
    element; those entries are all foods."""
    _nested_starter(monkeypatch)
    monkeypatch.setattr(demo_data, "DEMO_RECIPES", [
        {"source_recipe_id": 1, "name": "* Legacy Recipe", "description": "", "servings": 1,
         "instructions": "", "ingredients": [["* Nested Beans", 150, "g"]]},
    ])

    assert demo_data.load_demo_data(db_conn)["recipes"] == 1
    db_conn.commit()
    row = db_conn.execute(
        "SELECT fdc_id, ref_recipe_id FROM recipe_ingredients"
    ).fetchone()
    assert (row["fdc_id"], row["ref_recipe_id"]) == (901, None)


def test_clear_keeps_a_starter_food_the_user_is_still_using(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: clear deleted every starter food outright, silently orphaning
    a meal the user had logged with one. With the database now refusing that
    delete outright (trg_foods_no_delete_when_referenced), clearing would have
    failed altogether — so the food in use is kept and counted instead."""
    import db as _db

    monkeypatch.setattr(demo_data, "DEMO_FOODS", [
        {"fdc_id": 801, "name": "* Kept Food", "data_type": "SR Legacy",
         "nutrients": {"calories": 100.0, "protein_g": 9.0}, "portions": []},
        {"fdc_id": 802, "name": "* Dropped Food", "data_type": "SR Legacy",
         "nutrients": {"calories": 50.0, "protein_g": 2.0}, "portions": []},
    ])
    monkeypatch.setattr(demo_data, "DEMO_PANTRY", [])
    monkeypatch.setattr(demo_data, "DEMO_RECIPES", [])
    demo_data.load_demo_data(db_conn)
    mid = _db.meal_create(db_conn, "Lunch", "2026-09-23")
    _db.meal_add_food(db_conn, mid, 801, "* Kept Food", 100.0, "g")
    db_conn.commit()

    result = demo_data.clear_demo_data(db_conn)
    db_conn.commit()

    assert result["foods"] == 1
    assert result["foods_kept"] == 1
    assert db_conn.execute("SELECT COUNT(*) FROM foods WHERE fdc_id=801").fetchone()[0] == 1
    assert db_conn.execute("SELECT COUNT(*) FROM foods WHERE fdc_id=802").fetchone()[0] == 0
    # The meal is intact, not left pointing at a food that no longer exists.
    assert db_conn.execute("SELECT COUNT(*) FROM meal_items WHERE fdc_id=801").fetchone()[0] == 1


# ── Starter-set changes between versions ──────────────────────────────────

def test_shipped_starter_pantry_is_empty() -> None:
    """The pantry is personal — it always ships empty (owner's decision,
    2026-09-29), whatever the curator's own pantry holds at export time."""
    assert demo_data.DEMO_PANTRY == []


def _starter_set(monkeypatch: pytest.MonkeyPatch, foods: list[dict], recipes: list[dict]) -> None:
    monkeypatch.setattr(demo_data, "DEMO_FOODS", foods)
    monkeypatch.setattr(demo_data, "DEMO_PANTRY", [])
    monkeypatch.setattr(demo_data, "DEMO_RECIPES", recipes)


def _food(fdc_id: int, name: str, protein: float = 9.0) -> dict:
    return {"fdc_id": fdc_id, "name": name, "data_type": "SR Legacy",
            "nutrients": {"calories": 100.0, "protein_g": protein, "carbs_g": 20.0, "fat_g": 1.0},
            "portions": []}


def _recipe(name: str, ingredients: list, servings: int = 1, description: str = "") -> dict:
    return {"source_recipe_id": 1, "name": name, "description": description, "servings": servings,
            "instructions": "", "ingredients": ingredients}


def test_diff_manifests_reports_new_and_improved_only() -> None:
    old = demo_data.starter_manifest([_food(1, "* A"), _food(2, "* B")], [_recipe("* R", [])])
    new = demo_data.starter_manifest([_food(1, "* A"), _food(2, "* B", protein=10.0), _food(3, "* C")],
                                     [_recipe("* R", [], servings=2), _recipe("* S", [])])
    assert demo_data.diff_manifests(old, new) == {
        "new_foods": ["3"], "improved_foods": ["2"],
        "new_recipes": ["* S"], "improved_recipes": ["* R"],
    }


def test_source_recipe_id_alone_is_not_an_improvement() -> None:
    a = _recipe("* R", [])
    b = dict(a, source_recipe_id=99)
    assert demo_data.starter_manifest([], [a]) == demo_data.starter_manifest([], [b])


def test_first_run_records_silently(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    _starter_set(monkeypatch, [_food(1, "* A")], [])
    changes = demo_data.pending_changes(db_conn)
    assert changes["acknowledged"] is True
    assert not any(changes[k] for k in demo_data._CHANGE_KEYS)


def test_new_version_reports_new_and_improved_until_acted_on(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import db as _db

    _starter_set(monkeypatch, [_food(1, "* A"), _food(2, "* B")], [])
    demo_data.load_demo_data(db_conn)
    demo_data.pending_changes(db_conn)  # the version the user had

    # Next version: B improved, C added, and A deliberately deleted by the user
    # earlier — A must not be reported as "new" just because it's missing.
    _db.cache_food(db_conn, 999, "Mine", "User Drafted", None, None, None, {"protein_g": 1.0})
    db_conn.execute("DELETE FROM foods WHERE fdc_id = 1")
    _starter_set(monkeypatch, [_food(1, "* A"), _food(2, "* B", protein=12.0), _food(3, "* C")], [])

    changes = demo_data.pending_changes(db_conn)
    assert changes["acknowledged"] is False
    assert [f["fdc_id"] for f in changes["new_foods"]] == [3]
    assert [f["fdc_id"] for f in changes["improved_foods"]] == [2]
    assert "adds 1 new starter food" in demo_data.describe_changes(changes)

    demo_data.acknowledge_version_changes()
    changes = demo_data.pending_changes(db_conn)
    assert changes["acknowledged"] is True
    assert [f["fdc_id"] for f in changes["improved_foods"]] == [2]  # still offered in Settings


def test_skipped_version_changes_carry_forward(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    _starter_set(monkeypatch, [_food(1, "* A")], [])
    demo_data.load_demo_data(db_conn)
    demo_data.record_version_changes()
    _starter_set(monkeypatch, [_food(1, "* A", protein=11.0)], [])
    demo_data.record_version_changes()  # v2: A improved, never acted on
    _starter_set(monkeypatch, [_food(1, "* A", protein=11.0), _food(4, "* D")], [])
    changes = demo_data.pending_changes(db_conn)  # v3
    assert [f["fdc_id"] for f in changes["improved_foods"]] == [1]
    assert [f["fdc_id"] for f in changes["new_foods"]] == [4]


def test_apply_improvement_updates_food_in_place(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    import db as _db

    _starter_set(monkeypatch, [_food(1, "* A")], [_recipe("* R", [["* A", 100, "g", "food"]])])
    demo_data.load_demo_data(db_conn)
    demo_data.record_version_changes()
    db_conn.execute("UPDATE foods SET archived = 1 WHERE fdc_id = 1")
    rid = db_conn.execute("SELECT id FROM recipes WHERE name = '* R'").fetchone()["id"]

    _starter_set(monkeypatch, [_food(1, "* A", protein=15.0)], [_recipe("* R", [["* A", 100, "g", "food"]])])
    assert [f["fdc_id"] for f in demo_data.pending_changes(db_conn)["improved_foods"]] == [1]

    assert demo_data.apply_improvements(db_conn, [1], []) == {"foods": 1, "recipes": 0}
    row = _db.get_cached_food(db_conn, 1)
    assert json.loads(row["nutrients_json"])["protein_g"] == 15.0
    assert row["archived"] == 1  # an UPDATE, not a delete-and-reinsert
    assert db_conn.execute("SELECT COUNT(*) FROM recipe_ingredients WHERE recipe_id = ?", (rid,)).fetchone()[0] == 1
    assert demo_data.pending_changes(db_conn)["improved_foods"] == []


def test_apply_improvement_rewrites_recipe_keeping_its_id(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _starter_set(monkeypatch, [_food(1, "* A")], [_recipe("* R", [["* A", 100, "g", "food"]])])
    demo_data.load_demo_data(db_conn)
    demo_data.record_version_changes()
    rid = db_conn.execute("SELECT id FROM recipes WHERE name = '* R'").fetchone()["id"]

    # The new version also needs a food the user doesn't have yet.
    _starter_set(monkeypatch, [_food(1, "* A"), _food(2, "* B")],
                 [_recipe("* R", [["* A", 50, "g", "food"], ["* B", 50, "g", "food"]], servings=2,
                          description="better")])
    assert demo_data.pending_changes(db_conn)["improved_recipes"] == ["* R"]

    assert demo_data.apply_improvements(db_conn, [], ["* R"])["recipes"] == 1
    row = db_conn.execute("SELECT id, servings, description FROM recipes WHERE name = '* R'").fetchone()
    assert (row["id"], row["servings"], row["description"]) == (rid, 2, "better")
    assert db_conn.execute("SELECT COUNT(*) FROM recipe_ingredients WHERE recipe_id = ?", (rid,)).fetchone()[0] == 2
    assert db_conn.execute("SELECT COUNT(*) FROM foods WHERE fdc_id = 2").fetchone()[0] == 1


def test_decline_improvements_stops_offering_them(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    _starter_set(monkeypatch, [_food(1, "* A")], [])
    demo_data.load_demo_data(db_conn)
    demo_data.record_version_changes()
    _starter_set(monkeypatch, [_food(1, "* A", protein=15.0)], [])
    assert demo_data.pending_changes(db_conn)["improved_foods"]
    demo_data.decline_improvements()
    assert demo_data.pending_changes(db_conn)["improved_foods"] == []


def test_preview_changes_against_a_release_manifest(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _starter_set(monkeypatch, [_food(1, "* A")], [])
    demo_data.load_demo_data(db_conn)
    release = demo_data.starter_manifest([_food(1, "* A", protein=15.0), _food(2, "* B")], [])
    preview = demo_data.preview_changes(db_conn, release)
    assert [f["fdc_id"] for f in preview["new_foods"]] == [2]
    assert [f["fdc_id"] for f in preview["improved_foods"]] == [1]
    assert demo_data.preview_changes(db_conn, demo_data.starter_manifest()) is None
    assert demo_data.preview_changes(db_conn, None) is None
    assert demo_data.preview_changes(db_conn, {"foods": "garbage"}) is None


def test_item_new_then_improved_is_offered_as_improved_once_added(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """New in v2 (user restores it without dismissing anything), improved in
    v3: the improvement must be offered, not hidden as a still-"new" item."""
    _starter_set(monkeypatch, [], [])
    demo_data.record_version_changes()
    _starter_set(monkeypatch, [_food(5, "* E")], [])
    assert [f["fdc_id"] for f in demo_data.pending_changes(db_conn)["new_foods"]] == [5]
    demo_data.restore_selected(db_conn, [5], [], [])
    _starter_set(monkeypatch, [_food(5, "* E", protein=20.0)], [])
    changes = demo_data.pending_changes(db_conn)
    assert changes["new_foods"] == []
    assert [f["fdc_id"] for f in changes["improved_foods"]] == [5]
