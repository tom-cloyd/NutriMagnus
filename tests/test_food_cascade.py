"""
Tests for the food-edit -> recipe DCP cascade (numa_app/services/recipe_dcp.py
cascade_food_change) and the recompute_errors log it feeds when a cascade step
fails. Before this, editing a food's nutrients (including AA import) left any
recipe's cached dcp_g silently stale.
"""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import web.backend as backend
from numa_app.services import recipe_dcp as _recipe_dcp
from tests.conftest import SAMPLE_FDC_ID, _mock_api


@pytest.fixture()
def recipe_with_food(db_conn):
    """A recipe using fdc_id=1 as a direct ingredient, with a stale dcp_g set."""
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
        (1, "Mystery Blend", "Branded", json.dumps({"protein_g": 10.0}), "[]"),
    )
    rid = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
    _db.recipe_add_ingredient(db_conn, rid, 1, "Mystery Blend", 200.0, "g")
    _db.recipe_set_dcp(db_conn, rid, 18.0)
    db_conn.commit()
    return rid


class TestRecipesContainingFood:
    def test_finds_recipe_using_food_directly(self, db_conn, recipe_with_food):
        rows = _db.recipes_containing_food(db_conn, 1)
        assert [r["id"] for r in rows] == [recipe_with_food]

    def test_empty_for_unused_food(self, db_conn):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (2, "Unused Food", "Branded", json.dumps({"protein_g": 5.0}), "[]"),
        )
        db_conn.commit()
        assert _db.recipes_containing_food(db_conn, 2) == []


class TestCascadeFoodChange:
    def test_recomputes_every_recipe_using_the_food(self, db_conn, recipe_with_food, monkeypatch):
        recomputed_ids = []
        monkeypatch.setattr(
            _recipe_dcp, "recompute_recipe_dcp",
            lambda recipe_id, conn: recomputed_ids.append(recipe_id),
        )
        _recipe_dcp.cascade_food_change(1, db_conn)
        assert recomputed_ids == [recipe_with_food]

    def test_noop_for_food_not_used_in_any_recipe(self, db_conn, monkeypatch):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (2, "Unused Food", "Branded", json.dumps({"protein_g": 5.0}), "[]"),
        )
        db_conn.commit()
        recomputed_ids = []
        monkeypatch.setattr(
            _recipe_dcp, "recompute_recipe_dcp",
            lambda recipe_id, conn: recomputed_ids.append(recipe_id),
        )
        _recipe_dcp.cascade_food_change(2, db_conn)
        assert recomputed_ids == []

    def test_recompute_failure_is_logged_not_raised(self, db_conn, recipe_with_food, monkeypatch):
        def _boom(recipe_id, conn):
            raise RuntimeError("diaas blew up")
        monkeypatch.setattr(_recipe_dcp, "recompute_recipe_dcp", _boom)

        _recipe_dcp.cascade_food_change(1, db_conn)  # must not raise

        errors = _db.list_unresolved_recompute_errors(db_conn)
        assert len(errors) == 1
        assert errors[0]["entity_type"] == "recipe"
        assert errors[0]["entity_id"] == recipe_with_food
        assert "diaas blew up" in errors[0]["message"]

    def test_one_recipe_failing_does_not_block_others(self, db_conn, monkeypatch):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (1, "Mystery Blend", "Branded", json.dumps({"protein_g": 10.0}), "[]"),
        )
        rid_a = _db.recipe_create(db_conn, name="Dish A", description="", servings=1, instructions="")
        rid_b = _db.recipe_create(db_conn, name="Dish B", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(db_conn, rid_a, 1, "Mystery Blend", 200.0, "g")
        _db.recipe_add_ingredient(db_conn, rid_b, 1, "Mystery Blend", 100.0, "g")
        db_conn.commit()

        recomputed_ids = []

        def _maybe_boom(recipe_id, conn):
            if recipe_id == rid_a:
                raise RuntimeError("boom")
            recomputed_ids.append(recipe_id)

        monkeypatch.setattr(_recipe_dcp, "recompute_recipe_dcp", _maybe_boom)
        _recipe_dcp.cascade_food_change(1, db_conn)

        assert recomputed_ids == [rid_b]
        errors = _db.list_unresolved_recompute_errors(db_conn)
        assert len(errors) == 1
        assert errors[0]["entity_id"] == rid_a


class TestRecomputeErrorsLog:
    def test_log_and_list_unresolved(self, db_conn):
        _db.log_recompute_error(db_conn, "recipe", 5, "something failed")
        db_conn.commit()
        errors = _db.list_unresolved_recompute_errors(db_conn)
        assert len(errors) == 1
        assert errors[0]["message"] == "something failed"
        assert errors[0]["banner_ack_at"] is None

    def test_resolve_removes_from_unresolved_list(self, db_conn):
        _db.log_recompute_error(db_conn, "recipe", 5, "something failed")
        db_conn.commit()
        error_id = _db.list_unresolved_recompute_errors(db_conn)[0]["id"]
        assert _db.resolve_recompute_error(db_conn, error_id) is True
        assert _db.list_unresolved_recompute_errors(db_conn) == []

    def test_resolve_nonexistent_returns_false(self, db_conn):
        assert _db.resolve_recompute_error(db_conn, 999) is False

    def test_ack_banner_hides_from_unacked_but_not_unresolved(self, db_conn):
        _db.log_recompute_error(db_conn, "recipe", 5, "something failed")
        db_conn.commit()
        assert len(_db.list_unacked_recompute_errors(db_conn)) == 1

        _db.ack_recompute_errors_banner(db_conn)
        db_conn.commit()

        assert _db.list_unacked_recompute_errors(db_conn) == []
        assert len(_db.list_unresolved_recompute_errors(db_conn)) == 1

    def test_new_error_after_ack_reappears_in_banner(self, db_conn):
        _db.log_recompute_error(db_conn, "recipe", 5, "first failure")
        db_conn.commit()
        _db.ack_recompute_errors_banner(db_conn)
        db_conn.commit()

        _db.log_recompute_error(db_conn, "recipe", 6, "second failure")
        db_conn.commit()

        unacked = _db.list_unacked_recompute_errors(db_conn)
        assert len(unacked) == 1
        assert unacked[0]["entity_id"] == 6

    def test_update_recompute_error_refreshes_in_place(self, db_conn):
        """A failed retry must update the existing row, not add a duplicate."""
        _db.log_recompute_error(db_conn, "recipe", 5, "first failure")
        db_conn.commit()
        error_id = _db.list_unresolved_recompute_errors(db_conn)[0]["id"]
        _db.ack_recompute_errors_banner(db_conn)
        db_conn.commit()

        _db.update_recompute_error(db_conn, error_id, "retry failed too")
        db_conn.commit()

        errors = _db.list_unresolved_recompute_errors(db_conn)
        assert len(errors) == 1
        assert errors[0]["id"] == error_id
        assert errors[0]["message"] == "retry failed too"
        # A failed retry is functionally a new failure — banner should re-arm.
        assert len(_db.list_unacked_recompute_errors(db_conn)) == 1


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect web/backend.py's own _PREFS_FILE constant to a temp path (mirrors test_web.py)."""
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({"include_animal_foods": True}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


class TestWebRoutesTriggerCascade:
    """Each food-nutrient-write route must call cascade_food_change with the
    edited food's fdc_id — verified via a monkeypatch spy rather than full
    DIAAS math, since that's already covered by TestCascadeFoodChange above."""

    def test_custom_profile_edit_triggers_cascade(self, client: TestClient, db_conn, monkeypatch):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json, user_drafted) "
            "VALUES (?,?,?,?,?,1)",
            (SAMPLE_FDC_ID, "Draft food", "User Drafted", json.dumps({"protein_g": 5.0}), "[]"),
        )
        db_conn.commit()
        calls = []
        monkeypatch.setattr(_recipe_dcp, "cascade_food_change", lambda fdc_id, conn: calls.append(fdc_id))
        resp = client.post(f"/food/custom-profiles/{SAMPLE_FDC_ID}/edit", data={"name": "Draft food"})
        assert resp.status_code == 200
        assert calls == [SAMPLE_FDC_ID]

    def test_copy_aa_triggers_cascade(self, client: TestClient, db_conn, monkeypatch):
        _mock_api(monkeypatch)
        target_id = -1
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json, user_drafted) "
            "VALUES (?,?,?,?,?,1)",
            (target_id, "Draft food", "User Drafted", json.dumps({"protein_g": 20.0}), "[]"),
        )
        db_conn.commit()
        calls = []
        monkeypatch.setattr(_recipe_dcp, "cascade_food_change", lambda fdc_id, conn: calls.append(fdc_id))
        resp = client.post(
            f"/food/custom-profiles/{target_id}/copy-aa",
            data={"source_fdc_id": SAMPLE_FDC_ID},
            follow_redirects=False,
        )
        assert resp.status_code == 303
        # The source food isn't cached yet, so the route also caches it via
        # cache_food() (cascading for it too, harmlessly, before the target edit).
        assert calls == [SAMPLE_FDC_ID, target_id]

    def test_refresh_triggers_cascade(self, client: TestClient, db_conn, monkeypatch):
        _mock_api(monkeypatch)
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (SAMPLE_FDC_ID, "Chicken", "SR Legacy", json.dumps({"protein_g": 31.0}), "[]"),
        )
        db_conn.commit()
        calls = []
        monkeypatch.setattr(_recipe_dcp, "cascade_food_change", lambda fdc_id, conn: calls.append(fdc_id))
        resp = client.post(f"/food/cache/{SAMPLE_FDC_ID}/refresh", follow_redirects=False)
        assert resp.status_code in (200, 303)
        assert calls == [SAMPLE_FDC_ID]


class TestRecomputeErrorRetryRoute:
    """The Settings 'Retry' button (settings_recompute_error_resolve) must
    actually re-run the recompute, and only resolve the log entry if that
    succeeds — it must never just hide a still-broken recipe."""

    def test_successful_retry_resolves_and_redirects_with_status(
        self, client: TestClient, db_conn, monkeypatch
    ):
        db_conn.execute(
            "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) VALUES (?,?,?,?,?)",
            (1, "Mystery Blend", "Branded", json.dumps({"protein_g": 10.0}), "[]"),
        )
        rid = _db.recipe_create(db_conn, name="Dish", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(db_conn, rid, 1, "Mystery Blend", 200.0, "g")
        _db.recipe_set_dcp(db_conn, rid, 18.0)
        _db.log_recompute_error(db_conn, "recipe", rid, "boom")
        db_conn.commit()
        error_id = _db.list_unresolved_recompute_errors(db_conn)[0]["id"]

        monkeypatch.setattr(_recipe_dcp, "recompute_recipe_dcp", lambda recipe_id, conn: None)
        resp = client.post(f"/settings/recompute-error/{error_id}/resolve", follow_redirects=False)

        assert resp.status_code == 303
        assert "recompute_retry=resolved" in resp.headers["location"]
        assert _db.list_unresolved_recompute_errors(db_conn) == []

    def test_failed_retry_keeps_entry_and_updates_message(self, client: TestClient, db_conn, monkeypatch):
        _db.log_recompute_error(db_conn, "recipe", 99, "original failure")
        db_conn.commit()
        error_id = _db.list_unresolved_recompute_errors(db_conn)[0]["id"]

        def _boom(recipe_id, conn):
            raise RuntimeError("still broken")
        monkeypatch.setattr(_recipe_dcp, "recompute_recipe_dcp", _boom)

        resp = client.post(f"/settings/recompute-error/{error_id}/resolve", follow_redirects=False)

        assert resp.status_code == 303
        assert "recompute_retry=still_failing" in resp.headers["location"]
        errors = _db.list_unresolved_recompute_errors(db_conn)
        assert len(errors) == 1
        assert errors[0]["id"] == error_id
        assert "still broken" in errors[0]["message"]

    def test_resolve_unknown_error_id_is_a_noop(self, client: TestClient, db_conn):
        resp = client.post("/settings/recompute-error/999/resolve", follow_redirects=False)
        assert resp.status_code == 303
        assert "recompute_retry=not_found" in resp.headers["location"]
