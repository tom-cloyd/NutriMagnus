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
        "recipes_kept": 0,
        "edited_kept": 0,
    }
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM pantry").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM recipe_ingredients").fetchone()[0] == 0
    assert demo_data.is_loaded() is False


def test_clear_without_load_is_noop(db_conn: sqlite3.Connection) -> None:
    result = demo_data.clear_demo_data(db_conn)
    assert result == {"foods": 0, "pantry": 0, "recipes": 0, "foods_kept": 0, "recipes_kept": 0, "edited_kept": 0}


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


def test_starter_status_codes_are_this_dbs_not_the_starter_ids(
        db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings lists starter foods by display code. A custom starter food is
    renumbered on load and an outside-source one gets a local short number,
    so the code must come from this DB, not from the starter id."""
    import db as _db
    nutr = {"calories": 100.0, "protein_g": 9.0, "carbs_g": 20.0, "fat_g": 1.0}
    _db.cache_food(db_conn, fdc_id=-1, name="Mine", data_type="User", brand=None,
                   serving_size=None, serving_unit=None, nutrients=nutr, user_drafted=True)
    db_conn.commit()
    monkeypatch.setattr(demo_data, "DEMO_FOODS", [
        {"fdc_id": 901, "name": "* Beans", "data_type": "SR Legacy", "nutrients": nutr, "portions": []},
        {"fdc_id": -1, "name": "* Custom", "data_type": "User", "nutrients": nutr, "portions": []},
        {"fdc_id": -2_619_937_325, "name": "* Vitamins", "data_type": "OFF", "nutrients": nutr, "portions": []},
    ])
    monkeypatch.setattr(demo_data, "DEMO_PANTRY", [])
    monkeypatch.setattr(demo_data, "DEMO_RECIPES", [])

    before = {f["name"]: f["code"] for f in demo_data.starter_status(db_conn)["foods"]}
    assert before == {"* Beans": "U901", "* Custom": "UD", "* Vitamins": "OFF"}

    demo_data.load_demo_data(db_conn)
    db_conn.commit()
    after = {f["name"]: f["code"] for f in demo_data.starter_status(db_conn)["foods"]}
    assert after == {"* Beans": "U901", "* Custom": "UD2", "* Vitamins": "OFF1"}


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


def test_shipped_starter_data_carries_no_2021_gi_values() -> None:
    """Licence guard on the file that actually ships."""
    for food in demo_data.DEMO_FOODS:
        gi = food.get("gi")
        if gi and gi.get("source"):
            assert gi["source"].startswith(demo_data._SHIPPABLE_GI_SOURCES), food["name"]


def test_starter_gi_is_loaded_with_its_source(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    import db as _db

    typed = dict(_food(1, "* A"), gi={"estimate": 55.0, "source": None})
    picked = dict(_food(2, "* B"), gi={"estimate": 70.0, "source": "Atkinson 2008 international GI tables: x"})
    _starter_set(monkeypatch, [typed, picked, _food(3, "* C")], [])
    demo_data.load_demo_data(db_conn)

    a = _db.get_food_annotation(db_conn, 1)
    assert (a["gi_estimate"], a["gi_source"]) == (55.0, demo_data._CURATOR_GI_SOURCE)
    assert _db.get_food_annotation(db_conn, 2)["gi_source"].startswith("Atkinson 2008")
    assert _db.get_food_annotation(db_conn, 3) is None
    # A curator estimate that arrived this way still ships if exported again.
    assert demo_data.shippable_gi(a) == {"estimate": 55.0, "source": demo_data._CURATOR_GI_SOURCE}


def test_restoring_starter_items_leaves_the_users_own_food_and_gi_alone(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import db as _db

    _starter_set(monkeypatch, [dict(_food(2, "* B"), gi={"estimate": 70.0, "source": None})], [])
    _db.cache_food(db_conn, 2, "My B", "SR Legacy", None, None, None, {"protein_g": 1.0})
    _db.upsert_food_annotation(db_conn, 2, gi_estimate=66.0, gi_source=None)
    demo_data.restore_selected(db_conn, [2], [], [])
    assert _db.get_food_annotation(db_conn, 2)["gi_estimate"] == 66.0
    assert _db.get_cached_food(db_conn, 2)["name"] == "My B"


def test_improving_a_food_updates_its_gi(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    import db as _db

    _starter_set(monkeypatch, [_food(1, "* A")], [])
    demo_data.load_demo_data(db_conn)
    demo_data.record_version_changes()
    _starter_set(monkeypatch, [dict(_food(1, "* A"), gi={"estimate": 48.0, "source": None})], [])
    assert [f["fdc_id"] for f in demo_data.pending_changes(db_conn)["improved_foods"]] == [1]
    demo_data.apply_improvements(db_conn, [1], [])
    assert _db.get_food_annotation(db_conn, 1)["gi_estimate"] == 48.0


# ── Starter identity: never overwrite, fresh local ids, recipe uids ───────

def test_load_never_overwrites_a_food_the_user_already_has(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import db as _db

    _starter_set(monkeypatch, [dict(_food(2, "* B"), gi={"estimate": 70.0, "source": None})], [])
    _db.cache_food(db_conn, 2, "My B", "SR Legacy", None, None, None, {"protein_g": 1.0})
    _db.upsert_food_annotation(db_conn, 2, gi_estimate=66.0, gi_source=None, diaas_estimate=0.8)

    assert demo_data.load_demo_data(db_conn)["foods"] == 0
    row = _db.get_cached_food(db_conn, 2)
    assert row["name"] == "My B"
    ann = _db.get_food_annotation(db_conn, 2)
    assert (ann["gi_estimate"], ann["diaas_estimate"]) == (66.0, 0.8)
    # Not recorded as starter content, so clearing never deletes it.
    demo_data.clear_demo_data(db_conn)
    assert _db.get_cached_food(db_conn, 2) is not None


def test_custom_starter_food_gets_a_fresh_local_id(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    import db as _db

    # The user's own custom food already sits at -3, the curator's id.
    _db.cache_food(db_conn, -3, "My oatmeal", "User Drafted", None, None, None, {"protein_g": 5.0},
                   user_drafted=True)
    starter = dict(_food(-3, "* Crackers"), data_type="User Drafted")
    _starter_set(monkeypatch, [starter], [_recipe("* Snack", [["* Crackers", 30, "g", "food"]])])

    demo_data.load_demo_data(db_conn)
    assert _db.get_cached_food(db_conn, -3)["name"] == "My oatmeal"  # untouched
    copy = db_conn.execute("SELECT fdc_id FROM foods WHERE starter_key = '-3'").fetchone()
    assert copy is not None and copy["fdc_id"] not in (-3,) and copy["fdc_id"] < 0
    rid = db_conn.execute("SELECT id FROM recipes WHERE name = '* Snack'").fetchone()["id"]
    ing = db_conn.execute("SELECT fdc_id FROM recipe_ingredients WHERE recipe_id = ?", (rid,)).fetchone()
    assert ing["fdc_id"] == copy["fdc_id"]  # the recipe uses the copy, not the user's oatmeal
    assert all(f["present"] for f in demo_data.starter_status(db_conn)["foods"])

    demo_data.clear_demo_data(db_conn)
    assert _db.get_cached_food(db_conn, -3)["name"] == "My oatmeal"
    assert db_conn.execute("SELECT COUNT(*) FROM foods WHERE starter_key = '-3'").fetchone()[0] == 0


def test_same_name_user_recipe_is_not_mistaken_for_a_starter_recipe(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import db as _db

    _db.recipe_create(db_conn, name="* Bowl", description="mine", servings=1, instructions="")
    # Two recipes of the user's named "* Bowl" means none can be adopted by name.
    _db.recipe_create(db_conn, name="* Bowl", description="mine too", servings=1, instructions="")
    _starter_set(monkeypatch, [_food(1, "* A")],
                 [dict(_recipe("* Bowl", [["* A", 100, "g", "food"]]), uid="u-bowl")])

    assert demo_data.load_demo_data(db_conn)["recipes"] == 1
    rows = db_conn.execute("SELECT description, starter_uid FROM recipes WHERE name = '* Bowl' "
                           "ORDER BY id").fetchall()
    assert [(r["description"] or "", r["starter_uid"]) for r in rows] == [
        ("mine", None), ("mine too", None), ("", "u-bowl")]


def test_starter_recipe_loaded_before_uids_is_adopted(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    _starter_set(monkeypatch, [_food(1, "* A")], [_recipe("* Bowl", [["* A", 100, "g", "food"]])])
    demo_data.load_demo_data(db_conn)  # an older starter file: no uid
    monkeypatch.setattr(demo_data, "DEMO_RECIPES",
                        [dict(_recipe("* Bowl", [["* A", 100, "g", "food"]]), uid="u-bowl")])
    assert all(r["present"] for r in demo_data.starter_status(db_conn)["recipes"])
    assert db_conn.execute("SELECT starter_uid FROM recipes WHERE name = '* Bowl'").fetchone()[0] == "u-bowl"


def test_manifest_switch_from_names_to_uids_reports_nothing_new() -> None:
    old = demo_data.starter_manifest([], [_recipe("* Bowl", [])])
    old["recipes"] = {k: {"hash": v["hash"]} for k, v in old["recipes"].items()}  # old format: no name field
    new = demo_data.starter_manifest([], [dict(_recipe("* Bowl", []), uid="u-bowl")])
    assert demo_data.diff_manifests(old, new) == demo_data._empty_changes()


def test_recipe_updated_at_tracks_content_edits_only(db_conn: sqlite3.Connection) -> None:
    import db as _db

    rid = _db.recipe_create(db_conn, name="R", description="", servings=1, instructions="")
    stamp = lambda: db_conn.execute("SELECT updated_at FROM recipes WHERE id = ?", (rid,)).fetchone()[0]
    reset = lambda: db_conn.execute("UPDATE recipes SET updated_at = '2000-01-01' WHERE id = ?", (rid,))
    assert stamp() is not None

    for not_an_edit in ("UPDATE recipes SET last_accessed_at = datetime('now') WHERE id = ?",
                        "UPDATE recipes SET dcp_g = 5 WHERE id = ?",
                        "UPDATE recipes SET archived = 1 WHERE id = ?"):
        reset()
        db_conn.execute(not_an_edit, (rid,))
        assert stamp() == "2000-01-01", not_an_edit

    for edit in (lambda: db_conn.execute("UPDATE recipes SET name = 'R2' WHERE id = ?", (rid,)),
                 lambda: _db.recipe_add_ingredient(db_conn, rid, 1, "x", 10, "g"),
                 lambda: db_conn.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (rid,))):
        reset()
        edit()
        assert stamp() != "2000-01-01"



# ── Clear keeps what the user has made their own ─────────────────────────

def _loaded_small_set(db_conn, monkeypatch) -> int:
    _starter_set(monkeypatch, [_food(1, "* A"), _food(2, "* B")],
                 [_recipe("* R", [["* A", 100, "g", "food"]])])
    demo_data.load_demo_data(db_conn)
    return db_conn.execute("SELECT id FROM recipes WHERE name = '* R'").fetchone()["id"]


@pytest.mark.parametrize("edit", [
    "UPDATE foods SET name = 'B, mine' WHERE fdc_id = 2",                       # renamed ("*" removed)
    "UPDATE foods SET nutrients_json = '{\"protein_g\": 1.0}' WHERE fdc_id = 2",  # nutrients edited
    "UPDATE foods SET portions_json = '[{\"label\": \"1 cup\", \"grams\": 200}]' WHERE fdc_id = 2",
    "INSERT INTO food_annotations (fdc_id, gi_estimate) VALUES (2, 50)",       # annotated: counts as an edit
    "INSERT INTO food_annotations (fdc_id, diaas_estimate) VALUES (2, 0.7)",
])
def test_clear_keeps_an_edited_starter_food(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch, edit) -> None:
    _loaded_small_set(db_conn, monkeypatch)
    db_conn.execute(edit)
    result = demo_data.clear_demo_data(db_conn)
    assert result["edited_kept"] == 1
    assert db_conn.execute("SELECT COUNT(*) FROM foods WHERE fdc_id = 2").fetchone()[0] == 1
    assert db_conn.execute("SELECT COUNT(*) FROM foods WHERE fdc_id = 1").fetchone()[0] == 0  # unedited: removed


def test_clear_keeps_an_edited_starter_recipe_and_its_foods(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import db as _db

    rid = _loaded_small_set(db_conn, monkeypatch)
    _db.recipe_add_ingredient(db_conn, rid, 2, "* B", 20, "g")
    result = demo_data.clear_demo_data(db_conn)
    assert result["edited_kept"] == 1
    assert _db.recipe_get(db_conn, rid) is not None
    # Its foods stay too: the kept recipe still uses them.
    assert result["foods_kept"] == 2


def test_clear_keeps_a_starter_recipe_logged_in_a_meal(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    import db as _db

    rid = _loaded_small_set(db_conn, monkeypatch)
    mid = _db.meal_create(db_conn, "Lunch", "2026-09-29")
    _db.meal_add_recipe(db_conn, mid, rid, "* R", 1)
    result = demo_data.clear_demo_data(db_conn)
    assert result["recipes_kept"] == 1
    assert _db.recipe_get(db_conn, rid) is not None


def test_clear_with_an_old_marker_compares_against_the_bundled_set(
    db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _loaded_small_set(db_conn, monkeypatch)
    marker = json.loads(demo_data._MARKER_FILE.read_text())
    del marker["fingerprints"]  # as written before fingerprints existed
    demo_data._MARKER_FILE.write_text(json.dumps(marker))
    db_conn.execute("UPDATE foods SET name = 'B, mine' WHERE fdc_id = 2")
    result = demo_data.clear_demo_data(db_conn)
    assert result["edited_kept"] == 1
    assert result["foods"] == 1 and result["recipes"] == 1


def test_an_improvement_numa_applied_is_not_an_edit(db_conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> None:
    _loaded_small_set(db_conn, monkeypatch)
    demo_data.record_version_changes()
    _starter_set(monkeypatch, [_food(1, "* A"), _food(2, "* B", protein=20.0)],
                 [_recipe("* R", [["* A", 100, "g", "food"]])])
    demo_data.apply_improvements(db_conn, [2], [])
    result = demo_data.clear_demo_data(db_conn)
    assert result["edited_kept"] == 0
    assert db_conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 0


def test_starter_status_says_which_recipes_use_each_food(monkeypatch: pytest.MonkeyPatch, db_conn) -> None:
    _starter_set(monkeypatch, [_food(1, "* Beans"), _food(2, "* Salt"), _food(3, "* Walnuts")],
                 [_recipe("* Bowl", [["* Beans", 100, "g", "food"], ["* Salt", 1, "g", "food"]]),
                  _recipe("* Soup", [["* Beans", 50, "g", "food"]])])
    used = {f["name"]: f["used_in"] for f in demo_data.starter_status(db_conn)["foods"]}
    assert used == {"* Beans": ["* Bowl", "* Soup"], "* Salt": ["* Bowl"], "* Walnuts": []}
