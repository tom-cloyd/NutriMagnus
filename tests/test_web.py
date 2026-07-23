"""
test_web.py — smoke tests for the FastAPI web app (web/backend.py).

Uses fastapi.testclient.TestClient (requires httpx — not in requirements.txt,
same as pytest; install separately: pip install httpx).

Reuses the CLI test suite's autouse fixtures (use_test_db, use_test_profile,
use_test_prefs) from conftest.py for DB/profile isolation, plus a
web-specific fixture below since web/backend.py keeps its own _PREFS_FILE
module constant rather than sharing numa_app.config.prefs._PREFS_FILE.
"""
import datetime
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import diaas as _diaas
import profile as _profile
import web.backend as backend
from tests.conftest import SAMPLE_NUTRIENTS
from tests.test_cli import _mock_api


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect web/backend.py's own _PREFS_FILE constant to a temp path."""
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({"include_animal_foods": True}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


def test_web_app_self_migrates_without_cli(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression test: the web server used to depend on the CLI having called
    db.init_db() first (they're separate processes). A web server launched on
    its own against a brand-new or un-migrated database would 500 with
    'no such column: archived' (or any other pending migration). The web app's
    lifespan handler must run init_db() itself so it's self-sufficient."""
    fresh_db = tmp_path / "never_touched_by_cli.db"
    monkeypatch.setattr(_db, "_DB_PATH", fresh_db)
    assert not fresh_db.exists()
    with TestClient(backend.app) as fresh_client:
        resp = fresh_client.get("/recipes")
        assert resp.status_code == 200
    assert fresh_db.exists()


# GET routes that take no path params — smoke-test that each renders without error.
_SMOKE_ROUTES = [
    "/",
    "/food/search",
    "/food/analyze-portion",
    "/food/convert",
    "/food/cache",
    "/food/cache/prune",
    "/pantry",
    "/food/custom-profiles",
    "/food/annotate",
    "/meals",
    "/meals/search",
    "/settings",
    "/recipes",
    "/recipe/new",
    "/summary",
    "/analysis/food-use",
]


@pytest.mark.parametrize("path", _SMOKE_ROUTES)
def test_page_renders(client: TestClient, path: str) -> None:
    resp = client.get(path)
    assert resp.status_code == 200


def test_food_search_by_name(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    _mock_api(monkeypatch)
    resp = client.get("/food/search", params={"query": "Chicken"})
    assert resp.status_code == 200
    assert "Chicken" in resp.text


def test_food_detail_page(client: TestClient, cached_food) -> None:
    resp = client.get(f"/food/{cached_food['fdcId']}")
    assert resp.status_code == 200


def test_unknown_food_detail_404s_gracefully(client: TestClient) -> None:
    resp = client.get("/food/999999999")
    assert resp.status_code in (200, 404)


# ---------------------------------------------------------------------------
# POST routes — mutating workflows (pantry, meals, recipes, settings, cache)
# ---------------------------------------------------------------------------

def test_pantry_add_and_remove(client: TestClient, db_conn) -> None:
    resp = client.post("/pantry/add", data={"food_name": "Oats"}, follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == "/pantry?added=1"
    row = db_conn.execute("SELECT * FROM pantry WHERE food_name = 'Oats'").fetchone()
    assert row is not None

    resp = client.post(f"/pantry/remove/{row['id']}", follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute("SELECT * FROM pantry WHERE id = ?", (row["id"],)).fetchone() is None


def test_meal_create_add_food_complete_delete(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post(
        "/meals/create", data={"name": "Breakfast", "meal_date": "2026-07-11"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    meal_id = int(resp.headers["location"].rsplit("/", 1)[-1])

    resp = client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    items = db_conn.execute("SELECT * FROM meal_items WHERE meal_id = ?", (meal_id,)).fetchall()
    assert len(items) == 1
    assert items[0]["amount"] == 150.0

    resp = client.post(f"/meal/{meal_id}/complete", follow_redirects=False)
    assert resp.status_code == 303
    meal = db_conn.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone()
    assert meal["complete"] == 1

    resp = client.post(f"/meal/{meal_id}/delete", follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone() is None


def test_recipe_new_edit_and_add_ingredient(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post(
        "/recipe/new",
        data={"name": "Lentil Soup", "servings": 4},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    recipe_id = int(resp.headers["location"].split("/recipe/")[1].split("/")[0])

    resp = client.post(
        f"/recipe/{recipe_id}/edit",
        data={"name": "Lentil Soup", "description": "Hearty", "servings": 6},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    recipe = db_conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    assert recipe["servings"] == 6
    assert recipe["description"] == "Hearty"

    resp = client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "200 g"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    ingredients = db_conn.execute(
        "SELECT * FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,)
    ).fetchall()
    assert len(ingredients) == 1
    assert ingredients[0]["amount"] == 200.0


def test_recipe_edit_ingredient_search_shows_id_and_brand(client: TestClient, cached_food) -> None:
    """The ingredient-search table on a recipe's edit page must show each
    result's FDC ID and brand — otherwise same-named foods (e.g. many
    Branded "Tomato Sauce" entries) are indistinguishable in the list."""
    resp = client.post(
        "/recipe/new",
        data={"name": "Chicken Dish", "servings": 2},
        follow_redirects=False,
    )
    recipe_id = int(resp.headers["location"].split("/recipe/")[1].split("/")[0])

    resp = client.get(f"/recipe/{recipe_id}/edit", params={"q": "chicken"})
    assert resp.status_code == 200
    assert 'class="col-id' in resp.text
    assert str(cached_food["fdcId"]) in resp.text


def test_recipe_ingredient_add_error_preserves_search_results(client: TestClient, cached_food) -> None:
    """Regression test: a bad portion string (e.g. a volume unit with no
    density data) used to redirect back to the edit page without the search
    query, wiping the whole result list and forcing the user to re-search
    from scratch. The redirect must carry `q` through so results stay put."""
    resp = client.post(
        "/recipe/new",
        data={"name": "Chicken Dish", "servings": 2},
        follow_redirects=False,
    )
    recipe_id = int(resp.headers["location"].split("/recipe/")[1].split("/")[0])

    resp = client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={
            "fdc_id": cached_food["fdcId"],
            "food_name": cached_food["name"],
            "portion_str": "1 zz",
            "q": "chicken",
        },
        follow_redirects=False,
    )
    assert resp.status_code == 303
    location = resp.headers["location"]
    assert "q=chicken" in location
    assert "error=" in location

    resp = client.get(location)
    assert resp.status_code == 200
    assert str(cached_food["fdcId"]) in resp.text
    assert "not recognised" in resp.text


def test_custom_profile_create(client: TestClient, db_conn) -> None:
    resp = client.post(
        "/food/custom-profiles/create", data={"name": "My Homemade Granola"}, follow_redirects=False,
    )
    assert resp.status_code == 303
    row = db_conn.execute(
        "SELECT * FROM foods WHERE name = 'My Homemade Granola' AND user_drafted = 1"
    ).fetchone()
    assert row is not None


def test_settings_profile_update(client: TestClient) -> None:
    resp = client.post(
        "/settings",
        data={"age": 40, "sex": "female", "weight": 65, "activity_level": "moderate"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=profile"

    profile = _profile.load_profile()
    assert profile.age == 40
    assert profile.sex == "female"


def test_summary_shows_diet_aware_notes_for_plant_only(client: TestClient, cached_food) -> None:
    client.post("/settings/diet", data={"diet_pref": "plant_only"}, follow_redirects=False)

    resp = client.post(
        "/meals/create", data={"name": "Breakfast", "meal_date": "2026-07-11"},
        follow_redirects=False,
    )
    meal_id = int(resp.headers["location"].rsplit("/", 1)[-1])
    client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
        follow_redirects=False,
    )

    resp = client.get("/summary/2026-07-11")
    assert resp.status_code == 200
    assert "iron and zinc" in resp.text.lower()
    # SAMPLE_NUTRIENTS has no b12_mcg key → 0 intake → well under 50% of RDA
    assert "B12" in resp.text
    assert "supplement or fortified food" in resp.text


def test_summary_shows_no_diet_notes_for_all_animal_foods(client: TestClient, cached_food) -> None:
    resp = client.post(
        "/meals/create", data={"name": "Breakfast", "meal_date": "2026-07-11"},
        follow_redirects=False,
    )
    meal_id = int(resp.headers["location"].rsplit("/", 1)[-1])
    client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
        follow_redirects=False,
    )

    resp = client.get("/summary/2026-07-11")
    assert resp.status_code == 200
    assert "iron and zinc" not in resp.text.lower()
    assert "supplement or fortified food" not in resp.text


def test_optimal_and_max_limit_columns_render(client: TestClient, cached_food, db_conn) -> None:
    """Configuring a Profile Optimal target and a max limit adds the corresponding
    columns/rows to the food, meal, and daily-summary nutrient tables without error."""
    profile = _profile.load_profile()
    profile.optimal_targets = {"vitamin_d_mcg": 50.0}
    profile.max_limits = {"sodium_mg": 0.01}  # trivially low — always triggers the warning
    _profile.save_profile(profile)

    resp = client.get(f"/food/{cached_food['fdcId']}")
    assert resp.status_code == 200
    assert "optimal goal" in resp.text
    assert "% of optimal" in resp.text

    resp = client.post(
        "/meals/create", data={"name": "Breakfast", "meal_date": "2026-07-11"},
        follow_redirects=False,
    )
    meal_id = int(resp.headers["location"].rsplit("/", 1)[-1])
    client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
        follow_redirects=False,
    )

    resp = client.get(f"/meal/{meal_id}")
    assert resp.status_code == 200
    assert "optimal goal" in resp.text
    assert "limit-near" in resp.text or "limit-over" in resp.text

    resp = client.get("/summary/2026-07-11")
    assert resp.status_code == 200
    assert "optimal goal" in resp.text


def test_settings_nutrient_target_set_and_clear(client: TestClient) -> None:
    resp = client.get("/settings")
    assert resp.status_code == 200
    assert "Nutrient Targets" in resp.text

    resp = client.post(
        "/settings/nutrient-target",
        data={"key": "vitamin_d_mcg", "optimal": "50", "limit": ""},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=nutrient_target"
    profile = _profile.load_profile()
    assert profile.optimal_targets == {"vitamin_d_mcg": 50.0}

    resp = client.get("/settings")
    assert "value=\"50.0\"" in resp.text

    # Clearing: empty optimal field removes the entry
    client.post(
        "/settings/nutrient-target",
        data={"key": "vitamin_d_mcg", "optimal": "", "limit": ""},
        follow_redirects=False,
    )
    profile = _profile.load_profile()
    assert profile.optimal_targets == {}


def test_settings_nutrient_target_load_defaults(client: TestClient) -> None:
    resp = client.post("/settings/nutrient-target/load-defaults", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=nutrient_target_defaults"
    profile = _profile.load_profile()
    assert profile.optimal_targets == {
        "vitamin_d_mcg": 50.0,
        "omega3_epa_mg": 250.0,
        "omega3_dha_mg": 250.0,
    }

    resp = client.get("/settings?saved=nutrient_target_defaults")
    assert "Loaded recommended optimal targets" in resp.text


def test_settings_nutrient_target_load_defaults_skips_customized(client: TestClient) -> None:
    client.post(
        "/settings/nutrient-target",
        data={"key": "vitamin_d_mcg", "optimal": "99", "limit": ""},
        follow_redirects=False,
    )
    client.post("/settings/nutrient-target/load-defaults", follow_redirects=False)
    profile = _profile.load_profile()
    assert profile.optimal_targets["vitamin_d_mcg"] == 99.0
    assert profile.optimal_targets["omega3_epa_mg"] == 250.0


def test_settings_meal_nutrients_save_and_render(client: TestClient, cached_food) -> None:
    """Saving Sodium at position 1 in Settings shows it as a column on /meals."""
    resp = client.post(
        "/settings/meal-nutrients", data={"pos_sodium_mg": "1"}, follow_redirects=False,
    )
    assert resp.status_code == 303
    prefs_data = json.loads(backend._PREFS_FILE.read_text())
    assert prefs_data["meal_list_nutrients"] == ["sodium_mg"]

    resp = client.get("/settings")
    assert resp.status_code == 200
    assert "Meals &amp; Log columns" in resp.text

    client.post(
        "/meals/create", data={"name": "Dinner", "meal_date": "2026-07-11"}, follow_redirects=False,
    )
    resp = client.get("/meals")
    assert resp.status_code == 200
    assert "Sodium" in resp.text


def test_settings_meal_nutrients_caps_and_orders(client: TestClient) -> None:
    """Positions are sanitized (unknown/duplicate/over-cap) and applied in order."""
    from numa_app.services.meal_list_columns import MAX_MEAL_LIST_NUTRIENTS
    client.post(
        "/settings/meal-nutrients",
        data={"pos_fiber_g": "1", "pos_sodium_mg": "2"},
        follow_redirects=False,
    )
    prefs_data = json.loads(backend._PREFS_FILE.read_text())
    assert prefs_data["meal_list_nutrients"] == ["fiber_g", "sodium_mg"]
    assert len(prefs_data["meal_list_nutrients"]) <= MAX_MEAL_LIST_NUTRIENTS


def test_meal_nutrient_column_shows_computed_value(client: TestClient, cached_food, db_conn) -> None:
    """After a meal is analyzed (its detail page visited), the chosen nutrient
    column shows the persisted snapshot value on /meals rather than n/a or —."""
    client.post("/settings/meal-nutrients", data={"pos_sodium_mg": "1"}, follow_redirects=False)

    resp = client.post(
        "/meals/create", data={"name": "Dinner", "meal_date": "2026-07-11"},
        follow_redirects=False,
    )
    meal_id = int(resp.headers["location"].rsplit("/", 1)[-1])
    client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
        follow_redirects=False,
    )
    # Visiting the meal detail page computes and persists the nutrient snapshot
    # (same as _compute_and_store_meal_bcp does for bcp_g/calories).
    client.get(f"/meal/{meal_id}")

    row = db_conn.execute("SELECT nutrients_snapshot_json FROM meals WHERE id = ?", (meal_id,)).fetchone()
    assert row["nutrients_snapshot_json"] is not None
    snapshot = json.loads(row["nutrients_snapshot_json"])
    assert snapshot["sodium_mg"] == pytest.approx(74.0 * 1.5)

    resp = client.get("/meals")
    assert "111" in resp.text


def test_summary_trend_no_meals(client: TestClient) -> None:
    resp = client.get("/summary/trend")
    assert resp.status_code == 200
    assert "No meals logged between" in resp.text


def test_summary_trend_averages_across_logged_days(client: TestClient, cached_food) -> None:
    today = datetime.date.today().isoformat()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    for i, meal_date in enumerate((today, yesterday)):
        resp = client.post(
            "/meals/create", data={"name": f"Meal {i}", "meal_date": meal_date},
            follow_redirects=False,
        )
        meal_id = int(resp.headers["location"].rsplit("/", 1)[-1])
        client.post(
            f"/meal/{meal_id}/add",
            data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
            follow_redirects=False,
        )

    resp = client.get("/summary/trend?days=7")
    assert resp.status_code == 200
    assert "Averaging over 2 logged day(s) out of the last 7" in resp.text
    assert "2-Day Avg" in resp.text
    assert "Protein" in resp.text

    # Invalid days value falls back to 7, not a 500
    resp = client.get("/summary/trend?days=999")
    assert resp.status_code == 200


def test_summary_trend_shows_pooled_complement_suggestions(client: TestClient) -> None:
    """A lysine gap spread across two logged days is pooled and shown with
    forward-looking 'upcoming meals' framing on the trend page."""
    low_lysine = dict(SAMPLE_NUTRIENTS)
    low_lysine["aa_lysine_g"] = 0.6  # push below the FAO reference to create a real gap
    fdc_id = 900002

    with _db.get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO foods (fdc_id, name, data_type, nutrients_json) VALUES (?, ?, ?, ?)",
            (fdc_id, "Low-lysine test food", "SR Legacy", json.dumps(low_lysine)),
        )
        conn.commit()
        today = datetime.date.today().isoformat()
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        for d in (today, yesterday):
            meal_id = _db.meal_create(conn, "Lunch", d)
            _db.meal_add_food(conn, meal_id, fdc_id, "Low-lysine test food", 150.0, "g")
        conn.commit()

    resp = client.get("/summary/trend?days=7")
    assert resp.status_code == 200
    assert "Protein Complement Suggestions" in resp.text
    assert "Add to upcoming meals" in resp.text


def test_settings_diet_pref_raises_iron_zinc_rda(client: TestClient) -> None:
    # Baseline: use_test_web_prefs defaults to include_animal_foods=True → "all"
    resp = client.get("/settings")
    assert resp.status_code == 200
    assert "<td>Iron</td>\n        <td class=\"num-col\">8.0</td>" in resp.text
    assert "<td>Zinc</td>\n        <td class=\"num-col\">11.0</td>" in resp.text

    client.post("/settings/diet", data={"diet_pref": "plant_only"}, follow_redirects=False)
    resp = client.get("/settings")
    assert resp.status_code == 200
    # male_35 fixture profile: iron 8.0*1.8=14.4, zinc 11.0*1.5=16.5
    assert "<td>Iron</td>\n        <td class=\"num-col\">14.4</td>" in resp.text
    assert "<td>Zinc</td>\n        <td class=\"num-col\">16.5</td>" in resp.text


def test_settings_profile_update_preserves_nutrient_targets(client: TestClient) -> None:
    """Saving the basic profile form must not wipe previously-set nutrient targets."""
    client.post(
        "/settings/nutrient-target",
        data={"key": "sodium_mg", "optimal": "", "limit": "2000"},
        follow_redirects=False,
    )
    client.post(
        "/settings",
        data={"age": 40, "sex": "female", "weight": 65, "activity_level": "moderate"},
        follow_redirects=False,
    )
    profile = _profile.load_profile()
    assert profile.max_limits == {"sodium_mg": 2000.0}


def test_food_cache_delete_and_prune(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post("/food/cache/delete", data={"fdc_id": cached_food["fdcId"]}, follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute(
        "SELECT * FROM foods WHERE fdc_id = ?", (cached_food["fdcId"],)
    ).fetchone() is None


def test_food_cache_prune_deletes_unreferenced(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post("/food/cache/prune", follow_redirects=False)
    assert resp.status_code == 303
    assert "pruned=1" in resp.headers["location"]
    assert db_conn.execute(
        "SELECT * FROM foods WHERE fdc_id = ?", (cached_food["fdcId"],)
    ).fetchone() is None


def test_food_cache_archive_hides_and_restore_reveals(client: TestClient, cached_food, db_conn) -> None:
    fdc_id = cached_food["fdcId"]
    resp = client.post(f"/food/cache/{fdc_id}/archive", follow_redirects=False)
    assert resp.status_code == 303
    assert "archived=1" in resp.headers["location"]
    assert db_conn.execute(
        "SELECT archived FROM foods WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()["archived"] == 1

    resp = client.get("/food/cache")
    assert cached_food["name"] not in resp.text

    resp = client.get("/food/cache?show_archived=1")
    assert cached_food["name"] in resp.text
    assert "Archived" in resp.text

    resp = client.post(f"/food/cache/{fdc_id}/archive", follow_redirects=False)
    assert resp.status_code == 303
    assert "restored=1" in resp.headers["location"]
    assert db_conn.execute(
        "SELECT archived FROM foods WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()["archived"] == 0

    resp = client.get("/food/cache")
    assert cached_food["name"] in resp.text


def test_food_cache_search_by_query_renders(client: TestClient, cached_food) -> None:
    """Regression test: search_cached_foods() previously omitted nutrients_json,
    which crashed /food/cache?q=... with a 500 as soon as any result was returned."""
    resp = client.get("/food/cache?q=chicken")
    assert resp.status_code == 200
    assert cached_food["name"] in resp.text


def test_food_cache_archive_referenced_food_still_flags_still_used(client: TestClient, cached_food, db_conn) -> None:
    fdc_id = cached_food["fdcId"]
    db_conn.execute(
        "INSERT INTO pantry (food_name, fdc_id) VALUES (?, ?)", (cached_food["name"], fdc_id)
    )
    db_conn.commit()
    resp = client.post(f"/food/cache/{fdc_id}/archive", follow_redirects=False)
    assert "still_used=1" in resp.headers["location"]


def test_pantry_archive_hides_and_restore_reveals(client: TestClient, cached_food, db_conn) -> None:
    add_resp = client.post(
        "/pantry/add", data={"food_name": cached_food["name"], "fdc_id": cached_food["fdcId"]},
        follow_redirects=False,
    )
    assert add_resp.status_code == 303
    pid = db_conn.execute("SELECT id FROM pantry").fetchone()["id"]

    resp = client.post(f"/pantry/{pid}/archive", follow_redirects=False)
    assert resp.status_code == 303
    assert "archived=1" in resp.headers["location"]

    resp = client.get("/pantry")
    assert cached_food["name"] not in resp.text

    resp = client.get("/pantry?show_archived=1")
    assert cached_food["name"] in resp.text
    assert "Archived" in resp.text

    resp = client.post(f"/pantry/{pid}/archive", follow_redirects=False)
    assert "restored=1" in resp.headers["location"]
    resp = client.get("/pantry")
    assert cached_food["name"] in resp.text


def test_food_compare_add(client: TestClient, cached_food) -> None:
    resp = client.post(
        "/food/compare/add", data={"fdc_id": cached_food["fdcId"]}, follow_redirects=False,
    )
    assert resp.status_code == 303
    assert f"ids={cached_food['fdcId']}" in resp.headers["location"]


@pytest.fixture()
def second_cached_food(db_conn) -> dict:
    """A second cache food (distinct fdc_id) for tests that need >=2 foods."""
    row = {"fdcId": 999001, "name": "Second Test Food"}
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json) "
        "VALUES (?, ?, 'SR Legacy', '{}', '[]')",
        (row["fdcId"], row["name"]),
    )
    db_conn.commit()
    return row


def test_recipe_ingredient_edit_and_move(client: TestClient, cached_food, second_cached_food, db_conn) -> None:
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Salad", "servings": 2}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "100 g"},
        follow_redirects=False,
    )
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": second_cached_food["fdcId"], "food_name": second_cached_food["name"], "portion_str": "50 g"},
        follow_redirects=False,
    )
    ings = db_conn.execute(
        "SELECT * FROM recipe_ingredients WHERE recipe_id = ? ORDER BY id", (recipe_id,)
    ).fetchall()
    assert len(ings) == 2
    first_id, second_id = ings[0]["id"], ings[1]["id"]

    resp = client.post(
        f"/recipe/{recipe_id}/ingredient/{first_id}/edit",
        data={"portion_str": "200 g", "food_name": cached_food["name"]},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    updated = db_conn.execute("SELECT * FROM recipe_ingredients WHERE id = ?", (first_id,)).fetchone()
    assert updated["amount"] == 200.0

    resp = client.post(
        f"/recipe/{recipe_id}/ingredient/{second_id}/move",
        data={"direction": "up"}, follow_redirects=False,
    )
    assert resp.status_code == 303
    reordered = db_conn.execute(
        "SELECT * FROM recipe_ingredients WHERE recipe_id = ? ORDER BY COALESCE(sort_order, id), id",
        (recipe_id,),
    ).fetchall()
    assert reordered[0]["id"] == second_id


def test_recipe_delete_and_copy(client: TestClient, cached_food, db_conn) -> None:
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Stew", "servings": 3}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "100 g"},
        follow_redirects=False,
    )

    resp = client.post(f"/recipe/{recipe_id}/copy", follow_redirects=False)
    assert resp.status_code == 303
    new_id = int(resp.headers["location"].split("/recipe/")[1].split("/")[0])
    assert new_id != recipe_id
    copied = db_conn.execute("SELECT * FROM recipes WHERE id = ?", (new_id,)).fetchone()
    assert copied["name"] == "Copy of Stew"
    copied_ings = db_conn.execute(
        "SELECT * FROM recipe_ingredients WHERE recipe_id = ?", (new_id,)
    ).fetchall()
    assert len(copied_ings) == 1

    resp = client.post(f"/recipe/{recipe_id}/delete", follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone() is None


def test_recipe_archive_hides_and_restore_reveals(client: TestClient, db_conn) -> None:
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Soup", "servings": 1}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )

    resp = client.post(f"/recipe/{recipe_id}/archive", follow_redirects=False)
    assert resp.status_code == 303
    assert "archived=1" in resp.headers["location"]
    assert db_conn.execute(
        "SELECT archived FROM recipes WHERE id = ?", (recipe_id,)
    ).fetchone()["archived"] == 1

    resp = client.get("/recipes")
    assert "Soup" not in resp.text

    resp = client.get("/recipes?show_archived=1")
    assert "Soup" in resp.text
    assert "Archived" in resp.text

    resp = client.post(f"/recipe/{recipe_id}/archive", follow_redirects=False)
    assert "restored=1" in resp.headers["location"]
    resp = client.get("/recipes")
    assert "Soup" in resp.text


def test_recreated_recipe_offers_relink_to_broken_refs(client: TestClient, db_conn) -> None:
    """Deleting a recipe used in a meal leaves a dangling reference; a
    re-created recipe with a fuzzily-matching name (shares a word, not
    necessarily identical) should surface a relink offer on its edit page,
    and posting to /relink should reattach the meal item."""
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Beef Stew", "servings": 3}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    meal_id = int(
        client.post("/meals/create", data={"name": "Dinner", "meal_date": "2026-07-15"}, follow_redirects=False)
        .headers["location"].rsplit("/", 1)[-1]
    )
    client.post(
        f"/meal/{meal_id}/add-recipe",
        data={"recipe_id": recipe_id, "recipe_name": "Beef Stew", "servings": 1, "mode": "recipe"},
        follow_redirects=False,
    )
    client.post(f"/recipe/{recipe_id}/delete", follow_redirects=False)

    new_id = int(
        client.post("/recipe/new", data={"name": "Chicken Stew", "servings": 4}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    assert new_id != recipe_id

    resp = client.get(f"/recipe/{new_id}/edit")
    assert resp.status_code == 200
    assert "still reference a deleted recipe" in resp.text
    assert "Beef Stew" in resp.text

    resp = client.post(f"/recipe/{new_id}/relink", data={"matched_name": "Beef Stew"}, follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == f"/recipe/{new_id}/edit?relinked=1,0"

    item = db_conn.execute("SELECT * FROM meal_items WHERE meal_id = ?", (meal_id,)).fetchone()
    assert item["recipe_id"] == new_id

    resp = client.get(f"/recipe/{new_id}/edit?relinked=1,0")
    assert "Relinked 1 meal item(s)" in resp.text
    assert "still reference a deleted recipe" not in resp.text


def test_broken_recipe_refs_listing_page(client: TestClient) -> None:
    """/recipes/broken-refs lists every dangling reference for browsing,
    independent of any specific recipe being (re-)created."""
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Chili", "servings": 3}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    meal_id = int(
        client.post("/meals/create", data={"name": "Lunch", "meal_date": "2026-07-15"}, follow_redirects=False)
        .headers["location"].rsplit("/", 1)[-1]
    )
    client.post(
        f"/meal/{meal_id}/add-recipe",
        data={"recipe_id": recipe_id, "recipe_name": "Chili", "servings": 1, "mode": "recipe"},
        follow_redirects=False,
    )
    client.post(f"/recipe/{recipe_id}/delete", follow_redirects=False)

    resp = client.get("/recipes/broken-refs")
    assert resp.status_code == 200
    assert "Chili" in resp.text
    assert "Lunch" in resp.text


def test_meal_add_recipe_rename_merge_refresh_aa(client: TestClient, cached_food, db_conn) -> None:
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Chili", "servings": 2}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "100 g"},
        follow_redirects=False,
    )

    meal_id = int(
        client.post("/meals/create", data={"name": "Dinner", "meal_date": "2026-07-11"}, follow_redirects=False)
        .headers["location"].rsplit("/", 1)[-1]
    )
    resp = client.post(
        f"/meal/{meal_id}/add-recipe",
        data={"recipe_id": recipe_id, "recipe_name": "Chili", "servings": 1, "mode": "recipe"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    items = db_conn.execute("SELECT * FROM meal_items WHERE meal_id = ?", (meal_id,)).fetchall()
    assert len(items) == 1
    assert items[0]["item_type"] == "recipe"

    resp = client.post(
        f"/meal/{meal_id}/rename", data={"name": "Renamed Dinner", "meal_date": "2026-07-11"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    meal = db_conn.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone()
    assert meal["name"] == "Renamed Dinner"

    resp = client.post(f"/meal/{meal_id}/refresh-aa", follow_redirects=False)
    assert resp.status_code == 303

    second_meal_id = int(
        client.post("/meals/create", data={"name": "Leftovers", "meal_date": "2026-07-11"}, follow_redirects=False)
        .headers["location"].rsplit("/", 1)[-1]
    )
    resp = client.post(
        f"/meal/{meal_id}/merge",
        data={"new_name": "Combined Meal", "merge_ids": [meal_id, second_meal_id]},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    merged_id = int(resp.headers["location"].rsplit("/", 1)[-1])
    merged_items = db_conn.execute("SELECT * FROM meal_items WHERE meal_id = ?", (merged_id,)).fetchall()
    assert len(merged_items) == 1


def test_food_use_analysis_shows_recipe_current_name_after_rename(client: TestClient) -> None:
    """Regression test: renaming a recipe used in a meal used to make it
    vanish from Food Use in Meals (it was keyed/labeled by the frozen name
    snapshot taken when added to the meal, not the recipe's stable id)."""
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Chili", "servings": 3}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    meal_id = int(
        client.post("/meals/create", data={"name": "Dinner", "meal_date": "2026-07-15"}, follow_redirects=False)
        .headers["location"].rsplit("/", 1)[-1]
    )
    client.post(
        f"/meal/{meal_id}/add-recipe",
        data={"recipe_id": recipe_id, "recipe_name": "Chili", "servings": 1, "mode": "recipe"},
        follow_redirects=False,
    )

    resp = client.get("/analysis/food-use", params={"ranges_raw": "2026-07-01:2026-07-31"})
    assert "Chili" in resp.text

    client.post(
        f"/recipe/{recipe_id}/edit",
        data={"name": "Chili Verde", "description": "", "servings": 3},
        follow_redirects=False,
    )

    resp = client.get("/analysis/food-use", params={"ranges_raw": "2026-07-01:2026-07-31"})
    assert "Chili Verde" in resp.text
    assert "<strong>Chili</strong>" not in resp.text


def test_food_annotate_edit_skip_forever_and_clear(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post(
        f"/food/annotate/{cached_food['fdcId']}",
        data={"gi_estimate": "55", "diaas_estimate": "0.9"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    ann = db_conn.execute(
        "SELECT * FROM food_annotations WHERE fdc_id = ?", (cached_food["fdcId"],)
    ).fetchone()
    assert ann["gi_estimate"] == 55.0
    assert ann["diaas_estimate"] == 0.9

    resp = client.post(f"/food/annotate/{cached_food['fdcId']}/skip-forever", follow_redirects=False)
    assert resp.status_code == 303
    ann = db_conn.execute(
        "SELECT * FROM food_annotations WHERE fdc_id = ?", (cached_food["fdcId"],)
    ).fetchone()
    assert ann["gi_no_prompt"] == 1

    resp = client.post(f"/food/annotate/{cached_food['fdcId']}/clear", follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute(
        "SELECT * FROM food_annotations WHERE fdc_id = ?", (cached_food["fdcId"],)
    ).fetchone() is None


def test_settings_diaas_override_set_and_delete(client: TestClient) -> None:
    resp = client.post(
        "/settings/diaas-override",
        data={"food_name": "Lentils, cooked", "digestibility": 0.85, "notes": "test"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=diaas"

    with backend._db.get_db() as conn:
        override = _diaas.diaas_override_get(conn, "Lentils, cooked")
    assert override is not None

    resp = client.post(
        "/settings/diaas-override/delete", data={"food_name": "Lentils, cooked"}, follow_redirects=False,
    )
    assert resp.status_code == 303
    with backend._db.get_db() as conn:
        assert _diaas.diaas_override_get(conn, "Lentils, cooked") is None


def test_food_compare_add_multiple_remove_amounts(client: TestClient, cached_food, second_cached_food) -> None:
    resp = client.post(
        "/food/compare/add-multiple",
        data={"fdc_id": [cached_food["fdcId"], second_cached_food["fdcId"]]},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    location = resp.headers["location"]
    assert str(cached_food["fdcId"]) in location
    assert str(second_cached_food["fdcId"]) in location

    resp = client.post(
        "/food/compare/remove",
        data={"remove_id": second_cached_food["fdcId"],
              "ids": f"{cached_food['fdcId']},{second_cached_food['fdcId']}",
              "amounts": "100.0,100.0"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert str(second_cached_food["fdcId"]) not in resp.headers["location"]

    resp = client.post(
        "/food/compare/amounts",
        data={"ids": str(cached_food["fdcId"]), f"amounts_{cached_food['fdcId']}": "150"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert "amounts=150.0" in resp.headers["location"]


def test_food_compare_save_load_rename_delete(client: TestClient, cached_food, second_cached_food, db_conn) -> None:
    resp = client.post(
        "/food/compare/save",
        data={"name": "My Comparison",
              "ids": f"{cached_food['fdcId']},{second_cached_food['fdcId']}",
              "amounts": "100.0,100.0"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    row = db_conn.execute("SELECT * FROM saved_comparisons WHERE name = 'My Comparison'").fetchone()
    assert row is not None
    cmp_id = row["id"]

    resp = client.get(f"/food/compare/load/{cmp_id}", follow_redirects=False)
    assert resp.status_code == 303
    assert str(cached_food["fdcId"]) in resp.headers["location"]

    resp = client.post(
        "/food/compare/saved/rename", data={"cmp_id": cmp_id, "name": "Renamed Comparison"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    renamed = db_conn.execute("SELECT * FROM saved_comparisons WHERE id = ?", (cmp_id,)).fetchone()
    assert renamed["name"] == "Renamed Comparison"

    resp = client.post("/food/compare/saved/delete", data={"cmp_id": cmp_id}, follow_redirects=False)
    assert resp.status_code == 303
    assert db_conn.execute("SELECT * FROM saved_comparisons WHERE id = ?", (cmp_id,)).fetchone() is None
