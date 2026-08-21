"""
Tests for db.py — schema, CRUD helpers, constraints, cascade deletes.
All DB calls hit the per-test temp database via the use_test_db autouse fixture.
"""

import json
import sqlite3

import pytest

import db as _db
from tests.conftest import SAMPLE_FDC_ID, SAMPLE_NUTRIENTS


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class TestSchema:
    def test_all_tables_created(self, db_conn: sqlite3.Connection):
        tables = {
            row[0]
            for row in db_conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        assert {"foods", "recipes", "recipe_ingredients", "meals", "meal_items"} <= tables

    def test_init_db_is_idempotent(self):
        # Running init_db twice should not raise
        _db.init_db()
        _db.init_db()

    def test_meal_items_type_check(self, db_conn: sqlite3.Connection):
        """item_type must be 'food' or 'recipe' — anything else is rejected."""
        db_conn.execute(
            "INSERT INTO meals (name, meal_date) VALUES ('lunch', '2025-01-01')"
        )
        mid = db_conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        with pytest.raises(sqlite3.IntegrityError):
            db_conn.execute("""
                INSERT INTO meal_items (meal_id, item_type, fdc_id, food_name, amount, unit)
                VALUES (?, 'snack', 1, 'foo', 100, 'g')
            """, (mid,))


# ---------------------------------------------------------------------------
# Food cache
# ---------------------------------------------------------------------------

class TestFoodCache:
    def test_cache_and_retrieve(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Chicken breast", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)

        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, SAMPLE_FDC_ID)

        assert row is not None
        assert row["name"] == "Chicken breast"
        assert json.loads(row["nutrients_json"])["protein_g"] == 31.0

    def test_cache_and_retrieve_portions(self):
        portions = [{"description": "1 cup", "gram_weight": 240.0}]
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Oats", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS, portions)
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, SAMPLE_FDC_ID)
        assert json.loads(row["portions_json"]) == portions

    def test_cache_without_portions_stores_empty_list(self):
        """Omitting portions stores '[]' — meaning 'fetched, confirmed none'."""
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Oats", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, SAMPLE_FDC_ID)
        assert json.loads(row["portions_json"]) == []

    def test_init_db_resets_stale_empty_portions_to_null(self, db_conn: sqlite3.Connection):
        """Rows with portions_json='[]' (pre-portions-feature cache) are reset to 'null' on init_db."""
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, nutrients_json, portions_json) "
            "VALUES (1, 'Old food', '{}', '[]')"
        )
        db_conn.commit()
        _db.init_db()
        row = db_conn.execute("SELECT portions_json FROM foods WHERE fdc_id=1").fetchone()
        assert row["portions_json"] == "null"

    def test_get_nonexistent_returns_none(self):
        with _db.get_db() as conn:
            assert _db.get_cached_food(conn, 999999) is None

    def test_cache_food_replace(self):
        """Inserting the same fdc_id twice updates, not duplicates."""
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Old name", "SR Legacy",
                           None, 100.0, "g", {})
            _db.cache_food(conn, SAMPLE_FDC_ID, "New name", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)

        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, SAMPLE_FDC_ID)
        assert row["name"] == "New name"

    def test_list_cached_foods(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, 1, "Apple", "Foundation", None, 100.0, "g", {})
            _db.cache_food(conn, 2, "Banana", "Foundation", None, 100.0, "g", {})

        with _db.get_db() as conn:
            foods = _db.list_cached_foods(conn)
        assert len(foods) == 2
        assert foods[0]["name"] == "Apple"   # ordered by name

    def test_search_cached_foods(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, 1, "Chicken breast", "SR Legacy", None, 100.0, "g", {})
            _db.cache_food(conn, 2, "Chicken thigh",  "SR Legacy", None, 100.0, "g", {})
            _db.cache_food(conn, 3, "Salmon, Atlantic", "SR Legacy", None, 100.0, "g", {})

        with _db.get_db() as conn:
            results = _db.search_cached_foods(conn, "Chicken")
        assert len(results) == 2
        names = {r["name"] for r in results}
        assert "Salmon, Atlantic" not in names


# ---------------------------------------------------------------------------
# Recipes
# ---------------------------------------------------------------------------

class TestRecipes:
    def test_create_recipe(self):
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Pasta", "Simple pasta", 4, "Boil water")

        assert isinstance(rid, int)
        with _db.get_db() as conn:
            recipe = _db.recipe_get(conn, rid)
        assert recipe["name"] == "Pasta"
        assert recipe["servings"] == 4

    def test_add_and_get_ingredients(self):
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Chicken salad", "", 2, "")
            _db.recipe_add_ingredient(conn, rid, SAMPLE_FDC_ID, "Chicken breast", 150.0, "g")
            _db.recipe_add_ingredient(conn, rid, 2, "Lettuce", 50.0, "g")

        with _db.get_db() as conn:
            ings = _db.recipe_get_ingredients(conn, rid)
        assert len(ings) == 2
        assert ings[0]["food_name"] == "Chicken breast"
        assert ings[0]["amount"] == 150.0

    def test_recipe_list(self):
        with _db.get_db() as conn:
            _db.recipe_create(conn, "Soup", "", 1, "")
            _db.recipe_create(conn, "Salad", "", 2, "")

        with _db.get_db() as conn:
            recipes = _db.recipe_list(conn)
        assert len(recipes) == 2
        assert recipes[0]["name"] == "Salad"    # ordered by name

    def test_get_nonexistent_recipe_returns_none(self):
        with _db.get_db() as conn:
            assert _db.recipe_get(conn, 9999) is None

    def test_delete_recipe_cascades_to_ingredients(self, db_conn: sqlite3.Connection):
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Stew", "", 4, "")
            _db.recipe_add_ingredient(conn, rid, SAMPLE_FDC_ID, "Chicken", 200.0, "g")

        with _db.get_db() as conn:
            deleted = _db.recipe_delete(conn, rid)
        assert deleted is True

        rows = db_conn.execute(
            "SELECT * FROM recipe_ingredients WHERE recipe_id = ?", (rid,)
        ).fetchall()
        assert rows == []

    def test_delete_nonexistent_recipe_returns_false(self):
        with _db.get_db() as conn:
            assert _db.recipe_delete(conn, 9999) is False

    def test_find_and_relink_broken_recipe_refs(self):
        """Deleting a recipe that's used in a meal and as a sub-recipe leaves
        dangling references; re-creating a recipe of the same name should be
        able to find and relink both kinds of reference."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Stew", "", 4, "")
            parent_rid = _db.recipe_create(conn, "Big Batch", "", 1, "")
            _db.recipe_add_ingredient(conn, parent_rid, 0, "Stew", 1, "servings", ref_recipe_id=rid)
            meal_id = _db.meal_create(conn, "Dinner", "2026-01-01")
            _db.meal_add_recipe(conn, meal_id, rid, "Stew", 1)

        with _db.get_db() as conn:
            _db.recipe_delete(conn, rid)

        with _db.get_db() as conn:
            broken = _db.find_broken_recipe_refs(conn, "Stew")
        assert len(broken["meals"]) == 1
        assert broken["meals"][0]["meal_id"] == meal_id
        assert len(broken["recipes"]) == 1
        assert broken["recipes"][0]["recipe_id"] == parent_rid

        with _db.get_db() as conn:
            new_rid = _db.recipe_create(conn, "Stew", "", 4, "")
            n_meals, n_recipes = _db.relink_recipe_refs(conn, "Stew", new_rid)
        assert (n_meals, n_recipes) == (1, 1)

        with _db.get_db() as conn:
            broken_after = _db.find_broken_recipe_refs(conn, "Stew")
            ings = _db.recipe_get_ingredients(conn, parent_rid)
            item = _db.meal_get_items(conn, meal_id)[0]
        assert broken_after == {"meals": [], "recipes": []}
        assert ings[0]["ref_recipe_id"] == new_rid
        assert ings[0]["ref_recipe_deleted"] == 0
        assert item["recipe_id"] == new_rid

    def test_relink_recipe_refs_ignores_unrelated_names(self):
        """relink_recipe_refs must only touch rows matching the given name,
        not other broken references that happen to exist."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Chili", "", 4, "")
            meal_id = _db.meal_create(conn, "Lunch", "2026-01-02")
            _db.meal_add_recipe(conn, meal_id, rid, "Chili", 1)
            _db.recipe_delete(conn, rid)
            new_rid = _db.recipe_create(conn, "Stew", "", 4, "")
            n_meals, n_recipes = _db.relink_recipe_refs(conn, "Stew", new_rid)
        assert (n_meals, n_recipes) == (0, 0)

        with _db.get_db() as conn:
            item = _db.meal_get_items(conn, meal_id)[0]
        assert item["recipe_id"] == rid

    def test_find_broken_recipe_refs_is_fuzzy_by_word(self):
        """A broken reference stored as "Beef Stew" should surface when
        creating a recipe named "Chicken Stew" (shared word "stew"), but not
        when creating one named "Chicken Soup" (no shared word)."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Beef Stew", "", 4, "")
            meal_id = _db.meal_create(conn, "Dinner", "2026-01-03")
            _db.meal_add_recipe(conn, meal_id, rid, "Beef Stew", 1)
            _db.recipe_delete(conn, rid)

        with _db.get_db() as conn:
            hit = _db.find_broken_recipe_refs(conn, "Chicken Stew")
            miss = _db.find_broken_recipe_refs(conn, "Chicken Soup")
        assert len(hit["meals"]) == 1
        assert hit["meals"][0]["matched_name"] == "Beef Stew"
        assert miss == {"meals": [], "recipes": []}

    def test_list_all_broken_recipe_refs(self):
        """list_all_broken_recipe_refs returns every dangling reference,
        independent of any candidate name."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Chili", "", 4, "")
            meal_id = _db.meal_create(conn, "Lunch", "2026-01-04")
            _db.meal_add_recipe(conn, meal_id, rid, "Chili", 1)
            _db.recipe_delete(conn, rid)

        with _db.get_db() as conn:
            broken = _db.list_all_broken_recipe_refs(conn)
        assert len(broken["meals"]) == 1
        assert broken["meals"][0]["matched_name"] == "Chili"

    def test_recipe_list_includes_dcp_g(self):
        """recipe_list rows must include a dcp_g field (None by default)."""
        with _db.get_db() as conn:
            _db.recipe_create(conn, "Soup", "", 2, "")

        with _db.get_db() as conn:
            recipes = _db.recipe_list(conn)
        assert "dcp_g" in recipes[0].keys()
        assert recipes[0]["dcp_g"] is None

    def test_recipe_set_dcp(self):
        """recipe_set_dcp() persists a dcp_g value that is returned by recipe_list."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "High-protein bowl", "", 1, "")

        with _db.get_db() as conn:
            _db.recipe_set_dcp(conn, rid, 24.7)

        with _db.get_db() as conn:
            recipes = _db.recipe_list(conn)
        assert recipes[0]["dcp_g"] == pytest.approx(24.7)

    def test_recipe_set_dcp_clears_to_none(self):
        """Passing None to recipe_set_dcp clears a previously stored value."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Bowl", "", 1, "")
            _db.recipe_set_dcp(conn, rid, 18.5)

        with _db.get_db() as conn:
            _db.recipe_set_dcp(conn, rid, None)

        with _db.get_db() as conn:
            recipes = _db.recipe_list(conn)
        assert recipes[0]["dcp_g"] is None


# ---------------------------------------------------------------------------
# Meals
# ---------------------------------------------------------------------------

class TestMeals:
    def test_create_meal(self):
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Lunch", "2025-03-15")

        assert isinstance(mid, int)
        with _db.get_db() as conn:
            meal = _db.meal_get(conn, mid)
        assert meal["name"] == "Lunch"
        assert meal["meal_date"] == "2025-03-15"

    def test_add_food_item(self):
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Dinner", "2025-03-15")
            _db.meal_add_food(conn, mid, SAMPLE_FDC_ID, "Chicken breast", 150.0, "g")

        with _db.get_db() as conn:
            items = _db.meal_get_items(conn, mid)
        assert len(items) == 1
        assert items[0]["item_type"] == "food"
        assert items[0]["amount"] == 150.0

    def test_add_recipe_item(self):
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Stew", "", 4, "")
            mid = _db.meal_create(conn, "Dinner", "2025-03-15")
            _db.meal_add_recipe(conn, mid, rid, "Stew", 2.0)

        with _db.get_db() as conn:
            items = _db.meal_get_items(conn, mid)
        assert items[0]["item_type"] == "recipe"
        assert items[0]["amount"] == 2.0

    def test_expand_recipe_item_reflects_current_name_after_rename(self):
        """meal_expand_food_items must show a recipe's CURRENT name, not the
        name snapshot stored in meal_items at add-time, and must carry the
        recipe_id through so callers can group/key by id rather than by a
        name that can change later."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Chili", "", 4, "")
            mid = _db.meal_create(conn, "Dinner", "2025-03-15")
            _db.meal_add_recipe(conn, mid, rid, "Chili", 1.0)

        with _db.get_db() as conn:
            _db.recipe_update(conn, rid, "Chili Verde", "", 4, "")

        with _db.get_db() as conn:
            items = _db.meal_expand_food_items(conn, mid)
        recipe_rows = [i for i in items if i[2] == "recipe"]
        assert len(recipe_rows) == 1
        fdc_id, name, kind, has_protein, deleted, recipe_id = recipe_rows[0]
        assert name == "Chili Verde"
        assert deleted is False
        assert recipe_id == rid

    def test_expand_recipe_item_keeps_recipe_id_after_delete(self):
        """Even after the recipe is deleted, recipe_id (from meal_items) is
        still surfaced — meal_items.recipe_id is a stable stale pointer, never
        cleared on delete — so a "recipe (deleted)" row can still be grouped
        consistently across multiple meals that used the same deleted recipe."""
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Chili", "", 4, "")
            mid = _db.meal_create(conn, "Dinner", "2025-03-15")
            _db.meal_add_recipe(conn, mid, rid, "Chili", 1.0)
            _db.recipe_delete(conn, rid)

        with _db.get_db() as conn:
            items = _db.meal_expand_food_items(conn, mid)
        recipe_rows = [i for i in items if i[2] == "recipe"]
        assert len(recipe_rows) == 1
        fdc_id, name, kind, has_protein, deleted, recipe_id = recipe_rows[0]
        assert name == "Chili"
        assert deleted is True
        assert recipe_id == rid

    def test_list_by_date(self):
        with _db.get_db() as conn:
            _db.meal_create(conn, "Breakfast", "2025-03-15")
            _db.meal_create(conn, "Lunch",     "2025-03-15")
            _db.meal_create(conn, "Dinner",    "2025-03-16")   # different date

        with _db.get_db() as conn:
            meals = _db.meal_list_by_date(conn, "2025-03-15")
        assert len(meals) == 2
        assert all(m["meal_date"] == "2025-03-15" for m in meals)

    def test_list_dates(self):
        with _db.get_db() as conn:
            _db.meal_create(conn, "Breakfast", "2025-03-15")
            _db.meal_create(conn, "Dinner",    "2025-03-16")

        with _db.get_db() as conn:
            dates = _db.meal_list_dates(conn)
        date_strs = [r["meal_date"] for r in dates]
        assert "2025-03-16" in date_strs
        assert "2025-03-15" in date_strs
        assert date_strs[0] == "2025-03-16"   # most recent first

    def test_delete_meal_cascades_to_items(self, db_conn: sqlite3.Connection):
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Lunch", "2025-03-15")
            _db.meal_add_food(conn, mid, SAMPLE_FDC_ID, "Chicken", 100.0, "g")

        with _db.get_db() as conn:
            deleted = _db.meal_delete(conn, mid)
        assert deleted is True

        items = db_conn.execute(
            "SELECT * FROM meal_items WHERE meal_id = ?", (mid,)
        ).fetchall()
        assert items == []

    def test_get_nonexistent_meal_returns_none(self):
        with _db.get_db() as conn:
            assert _db.meal_get(conn, 9999) is None

    def test_remove_meal_item(self):
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Lunch", "2025-03-15")
            _db.meal_add_food(conn, mid, SAMPLE_FDC_ID, "Chicken breast", 150.0, "g")

        with _db.get_db() as conn:
            items = _db.meal_get_items(conn, mid)
        iid = items[0]["id"]

        with _db.get_db() as conn:
            removed = _db.meal_remove_item(conn, iid, mid)
        assert removed is True

        with _db.get_db() as conn:
            assert _db.meal_get_items(conn, mid) == []

    def test_remove_meal_item_wrong_meal_returns_false(self):
        """Supplying the wrong meal_id must not delete the item."""
        with _db.get_db() as conn:
            mid1 = _db.meal_create(conn, "Lunch",  "2025-03-15")
            mid2 = _db.meal_create(conn, "Dinner", "2025-03-15")
            _db.meal_add_food(conn, mid1, SAMPLE_FDC_ID, "Chicken breast", 150.0, "g")

        with _db.get_db() as conn:
            items = _db.meal_get_items(conn, mid1)
        iid = items[0]["id"]

        with _db.get_db() as conn:
            removed = _db.meal_remove_item(conn, iid, mid2)   # wrong meal
        assert removed is False

        with _db.get_db() as conn:
            assert len(_db.meal_get_items(conn, mid1)) == 1   # item still there

    def test_remove_nonexistent_item_returns_false(self):
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Lunch", "2025-03-15")
            removed = _db.meal_remove_item(conn, 9999, mid)
        assert removed is False


# ---------------------------------------------------------------------------
# Context manager — rollback on error
# ---------------------------------------------------------------------------

class TestContextManager:
    def test_rollback_on_exception(self, db_conn: sqlite3.Connection):
        """If the body raises, changes must be rolled back."""
        try:
            with _db.get_db() as conn:
                conn.execute(
                    "INSERT INTO recipes (name, servings) VALUES ('Doomed', 1)"
                )
                raise RuntimeError("simulated failure")
        except RuntimeError:
            pass

        rows = db_conn.execute("SELECT * FROM recipes WHERE name='Doomed'").fetchall()
        assert rows == []


# ---------------------------------------------------------------------------
# Archiving (reserve area for foods / pantry / recipes)
# ---------------------------------------------------------------------------

class TestArchiving:
    def test_archived_food_excluded_by_default(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, 1, "Apple", "Foundation", None, 100.0, "g", {})
            _db.cache_food(conn, 2, "Banana", "Foundation", None, 100.0, "g", {})
            _db.set_food_archived(conn, 1, True)

        with _db.get_db() as conn:
            visible = _db.list_cached_foods(conn)
            all_rows = _db.list_cached_foods(conn, include_archived=True)
        assert {f["name"] for f in visible} == {"Banana"}
        assert {f["name"] for f in all_rows} == {"Apple", "Banana"}

    def test_food_archive_restore_roundtrip(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, 1, "Apple", "Foundation", None, 100.0, "g", {})
            _db.set_food_archived(conn, 1, True)
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, 1)
        assert row["archived"] == 1

        with _db.get_db() as conn:
            _db.set_food_archived(conn, 1, False)
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, 1)
            visible = _db.list_cached_foods(conn)
        assert row["archived"] == 0
        assert len(visible) == 1

    def test_archived_food_still_resolves_by_fdc_id(self):
        """Single-row lookup must never be filtered — existing references keep working."""
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Chicken breast", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)
            _db.set_food_archived(conn, SAMPLE_FDC_ID, True)
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, SAMPLE_FDC_ID)
        assert row is not None
        assert row["name"] == "Chicken breast"

    def test_archived_food_excluded_from_search(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, 1, "Chicken breast", "SR Legacy", None, 100.0, "g", {})
            _db.cache_food(conn, 2, "Chicken thigh", "SR Legacy", None, 100.0, "g", {})
            _db.set_food_archived(conn, 1, True)

        with _db.get_db() as conn:
            results = _db.search_cached_foods(conn, "Chicken")
        names = {r["name"] for r in results}
        assert names == {"Chicken thigh"}

    def test_food_references_counts_pantry_recipe_meal(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Chicken breast", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)
            _db.pantry_add(conn, "Chicken breast", fdc_id=SAMPLE_FDC_ID)
            rid = _db.recipe_create(conn, "Soup", "", 1, "")
            _db.recipe_add_ingredient(conn, rid, SAMPLE_FDC_ID, "Chicken breast", 100.0, "g")
            mid = _db.meal_create(conn, "Lunch", "2025-03-15")
            _db.meal_add_food(conn, mid, SAMPLE_FDC_ID, "Chicken breast", 100.0, "g")

        with _db.get_db() as conn:
            refs = _db.food_references(conn, SAMPLE_FDC_ID)
        assert refs == {"pantry": 1, "recipes": 1, "meals": 1}

    def test_archived_unreferenced_food_protected_from_prune(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, 1, "Apple", "Foundation", None, 100.0, "g", {})
            _db.set_food_archived(conn, 1, True)

        with _db.get_db() as conn:
            unused = _db.list_unused_cached_foods(conn)
        assert unused == []

        with _db.get_db() as conn:
            deleted = _db.prune_unused_cached_foods(conn)
        assert deleted == []
        with _db.get_db() as conn:
            assert _db.get_cached_food(conn, 1) is not None

    def test_check_db_integrity_clean_db_finds_nothing(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Chicken breast", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)
            _db.pantry_add(conn, "Chicken breast", fdc_id=SAMPLE_FDC_ID)
        with _db.get_db() as conn:
            issues = _db.check_db_integrity(conn)
        assert all(v == [] for v in issues.values())

    def test_check_db_integrity_finds_orphaned_pantry_entry(self):
        """Regression test: deleting a still-referenced cached food (possible
        before food_cache_delete() started refusing to do so) leaves a pantry
        entry pointing at an fdc_id with no data behind it — opening that
        food's page then fails since it's treated as "not cached" and the app
        tries to re-fetch it from USDA by fdc_id."""
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Chicken breast", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)
            _db.pantry_add(conn, "Chicken breast", fdc_id=SAMPLE_FDC_ID)
            # Simulate the food having been deleted out from under the pantry
            # entry (the exact scenario food_cache_delete() now refuses).
            conn.execute("DELETE FROM foods WHERE fdc_id = ?", (SAMPLE_FDC_ID,))

        with _db.get_db() as conn:
            issues = _db.check_db_integrity(conn)
        assert len(issues["orphaned_pantry"]) == 1
        assert issues["orphaned_pantry"][0]["fdc_id"] == SAMPLE_FDC_ID
        assert issues["orphaned_recipe_ingredients"] == []
        assert issues["orphaned_meal_items"] == []

    def test_repair_db_integrity_removes_orphaned_entries(self):
        with _db.get_db() as conn:
            _db.cache_food(conn, SAMPLE_FDC_ID, "Chicken breast", "SR Legacy",
                           None, 100.0, "g", SAMPLE_NUTRIENTS)
            _db.pantry_add(conn, "Chicken breast", fdc_id=SAMPLE_FDC_ID)
            rid = _db.recipe_create(conn, "Soup", "", 1, "")
            _db.recipe_add_ingredient(conn, rid, SAMPLE_FDC_ID, "Chicken breast", 100.0, "g")
            mid = _db.meal_create(conn, "Lunch", "2025-03-15")
            _db.meal_add_food(conn, mid, SAMPLE_FDC_ID, "Chicken breast", 100.0, "g")
            conn.execute("DELETE FROM foods WHERE fdc_id = ?", (SAMPLE_FDC_ID,))

        with _db.get_db() as conn:
            counts = _db.repair_db_integrity(conn)
        assert counts == {"orphaned_pantry": 1, "orphaned_recipe_ingredients": 1, "orphaned_meal_items": 1}

        with _db.get_db() as conn:
            issues = _db.check_db_integrity(conn)
        assert all(v == [] for v in issues.values())

    def test_pantry_archive_restore_roundtrip(self):
        with _db.get_db() as conn:
            pid = _db.pantry_add(conn, "Tofu")
            _db.set_pantry_archived(conn, pid, True)

        with _db.get_db() as conn:
            visible = _db.pantry_list(conn)
            all_rows = _db.pantry_list(conn, include_archived=True)
            row = _db.pantry_get(conn, pid)
        assert visible == []
        assert len(all_rows) == 1
        assert row["archived"] == 1

        with _db.get_db() as conn:
            _db.set_pantry_archived(conn, pid, False)
        with _db.get_db() as conn:
            visible = _db.pantry_list(conn)
        assert len(visible) == 1

    def test_recipe_archive_restore_roundtrip(self):
        with _db.get_db() as conn:
            rid = _db.recipe_create(conn, "Soup", "", 1, "")
            _db.set_recipe_archived(conn, rid, True)

        with _db.get_db() as conn:
            visible = _db.recipe_list(conn)
            all_rows = _db.recipe_list(conn, include_archived=True)
        assert visible == []
        assert len(all_rows) == 1
        assert all_rows[0]["archived"] == 1

        with _db.get_db() as conn:
            _db.set_recipe_archived(conn, rid, False)
        with _db.get_db() as conn:
            visible = _db.recipe_list(conn)
        assert len(visible) == 1
        assert visible[0]["archived"] == 0

    def test_recipe_references_counts_subrecipe_and_meal(self):
        with _db.get_db() as conn:
            sub_rid = _db.recipe_create(conn, "Sauce", "", 1, "")
            main_rid = _db.recipe_create(conn, "Pasta", "", 2, "")
            _db.recipe_add_ingredient(conn, main_rid, 0, "Sauce", 1.0, "recipe", ref_recipe_id=sub_rid)
            mid = _db.meal_create(conn, "Dinner", "2025-03-15")
            _db.meal_add_recipe(conn, mid, sub_rid, "Sauce", 1.0)

        with _db.get_db() as conn:
            refs = _db.recipe_references(conn, sub_rid)
        assert refs == {"recipes": 1, "meals": 1}
