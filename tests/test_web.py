"""
test_web.py — smoke tests for the FastAPI web app (web/backend.py).

Uses fastapi.testclient.TestClient (requires httpx — not in requirements.txt,
same as pytest; install separately: pip install httpx).

Reuses the shared autouse fixtures (use_test_db, use_test_profile) from
conftest.py for DB/profile isolation, plus a web-specific fixture below
since web/backend.py keeps its own _PREFS_FILE module constant.
"""
import datetime
import io
import json
import pathlib
import re
import zipfile

import pytest
from fastapi.testclient import TestClient

import db as _db
import diaas as _diaas
import profile as _profile
import web.backend as backend
from tests.conftest import SAMPLE_NUTRIENTS, _mock_api


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
    "/analysis/food-use-recipes",
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


def test_food_search_page_defers_usda_off_to_async_endpoint(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The initial /food/search response must not block on USDA/OFF — those
    results are fetched by the browser afterward from /food/search-api-results
    (see _search_logic's cache-only fast path)."""
    _mock_api(monkeypatch)
    resp = client.get("/food/search", params={"query": "Chicken"})
    assert resp.status_code == 200
    assert "broilers or fryers" not in resp.text
    assert "search-api-results" in resp.text  # JS fetch call is present

    api_resp = client.get("/food/search-api-results", params={"query": "Chicken"})
    assert api_resp.status_code == 200
    assert "broilers or fryers" in api_resp.text


def test_analyze_portion_page_defers_usda_off_to_async_endpoint(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _mock_api(monkeypatch)
    resp = client.post("/food/analyze-portion", data={"query": "Chicken"})
    assert resp.status_code == 200
    assert "broilers or fryers" not in resp.text
    assert "analyze-portion-api-results" in resp.text

    api_resp = client.get("/food/analyze-portion-api-results", params={"query": "Chicken"})
    assert api_resp.status_code == 200
    assert "broilers or fryers" in api_resp.text


def test_food_search_source_filter_isolates_usda(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    """The Source dropdown should let a user isolate one data source — here,
    nothing is cached/pantried, so 'usda' keeps the mocked USDA hit and
    'off' (stubbed to return nothing by the autouse no_off fixture) hides it."""
    _mock_api(monkeypatch)
    usda_only = client.get("/food/search-api-results", params={"query": "Chicken", "source": "usda"})
    assert usda_only.status_code == 200
    assert "broilers or fryers" in usda_only.text

    off_only = client.get("/food/search-api-results", params={"query": "Chicken", "source": "off"})
    assert off_only.status_code == 200
    assert "broilers or fryers" not in off_only.text


def test_food_search_source_filter_option_labels_show_abbreviation_and_full_name(client: TestClient) -> None:
    resp = client.get("/food/search", params={"query": "Chicken"})
    assert resp.status_code == 200
    assert "USDA — USDA FoodData Central" in resp.text
    assert "OFF — Open Food Facts" in resp.text


def test_meal_add_food_source_filter_isolates_usda(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Same source filter, wired into the meal add-food search's async endpoint."""
    import datetime as _dt
    _mock_api(monkeypatch)
    with _db.get_db() as conn:
        meal_id = _db.meal_create(conn, "Test meal", _dt.date.today().isoformat())

    usda_only = client.get(f"/meal/{meal_id}/search-api-results", params={"q": "Chicken", "source": "usda"})
    assert usda_only.status_code == 200
    assert "broilers or fryers" in usda_only.text

    off_only = client.get(f"/meal/{meal_id}/search-api-results", params={"q": "Chicken", "source": "off"})
    assert off_only.status_code == 200
    assert "broilers or fryers" not in off_only.text


def test_food_search_by_barcode_found_via_off(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    barcode = "012345678905"  # UPC-A, 12 digits

    def fake_lookup(bc: str) -> dict:
        assert bc == barcode
        return {
            "fdcId": -2000000001, "name": "Test Bar", "dataType": "Open Food Facts",
            "brand": "Acme", "servingSize": 40.0, "servingUnit": "g",
            "nutrients": {"protein_g": 10.0}, "portions": [],
        }

    monkeypatch.setattr("web.backend._off.lookup_by_barcode", fake_lookup)
    resp = client.get("/food/search", params={"query": barcode})
    assert resp.status_code == 200
    assert "Test Bar" in resp.text

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, -2000000001)
    assert cached is not None
    assert cached["name"] == "Test Bar"


def test_food_cache_export_csv(client: TestClient) -> None:
    with _db.get_db() as conn:
        _db.cache_food(
            conn, 111111, "Exportable Bar", "Foundation",
            "Test Brand", 40.0, "g", {"protein_g": 5.0, "calories": 120.0},
            [{"description": "1 bar", "gram_weight": 40.0}],
        )
    resp = client.get("/food/cache/export.csv")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/csv")
    body = resp.text
    assert "Exportable Bar" in body
    assert "Test Brand" in body
    assert "1 bar" in body
    header = body.splitlines()[0]
    assert "protein_g" in header
    assert "portions" in header


def test_food_cache_import_csv_preview_then_confirm(client: TestClient) -> None:
    csv_text = (
        "name,calories,protein_g,portions\r\n"
        'Imported Bar,150,6.0,"[{""description"": ""1 bar"", ""gram_weight"": 45.0}]"\r\n'
    )
    preview = client.post("/food/cache/import-csv", data={"action": "preview", "csv_text": csv_text})
    assert preview.status_code == 200
    assert "Imported Bar" in preview.text
    assert "Import 1 food into cache" in preview.text

    confirm = client.post(
        "/food/cache/import-csv", data={"action": "confirm", "csv_text": csv_text}, follow_redirects=False
    )
    assert confirm.status_code == 303
    assert "imported=1" in confirm.headers["location"]

    with _db.get_db() as conn:
        rows = _db.list_cached_foods(conn)
    imported = [r for r in rows if r["name"] == "Imported Bar"]
    assert len(imported) == 1
    assert imported[0]["fdc_id"] < 0
    nutrients = json.loads(imported[0]["nutrients_json"])
    assert nutrients["calories"] == 150.0
    portions = json.loads(imported[0]["portions_json"])
    assert portions == [{"description": "1 bar", "gram_weight": 45.0}]


def test_food_cache_import_csv_bad_row_shows_warning_not_500(client: TestClient) -> None:
    resp = client.post("/food/cache/import-csv", data={"action": "preview", "csv_text": "a,b\n1,2\n"})
    assert resp.status_code == 200
    assert "No valid food records" in resp.text
    assert "name" in resp.text


def test_recipe_export_csv_then_import_round_trip(client: TestClient) -> None:
    with _db.get_db() as conn:
        _db.cache_food(conn, 222222, "Round Trip Quinoa", "Foundation", None, None, None,
                        {"calories": 100.0, "protein_g": 5.0}, [])
        sub_id = _db.recipe_create(conn, "Round Trip Cooked Quinoa", "", 2, "Boil it.")
        _db.recipe_add_ingredient(conn, sub_id, 222222, "Round Trip Quinoa", 100.0, "100 g")
        main_id = _db.recipe_create(conn, "Round Trip Quinoa Bowl", "tasty", 1, "Combine.")
        _db.recipe_add_ingredient(conn, main_id, 0, "Round Trip Cooked Quinoa", 1.0,
                                   "1 serving", ref_recipe_id=sub_id)

    export_resp = client.get(f"/recipe/{main_id}/export.csv")
    assert export_resp.status_code == 200
    assert export_resp.headers["content-type"] == "application/zip"
    zf = zipfile.ZipFile(io.BytesIO(export_resp.content))
    recipes_text = zf.read("recipes.csv").decode("utf-8")
    foods_text = zf.read("foods.csv").decode("utf-8")
    assert "Round Trip Quinoa Bowl" in recipes_text
    assert "Round Trip Cooked Quinoa" in recipes_text
    assert "Round Trip Quinoa" in foods_text

    # Import into a database that doesn't have any of this yet — delete the originals first.
    with _db.get_db() as conn:
        _db.recipe_delete(conn, main_id)
        _db.recipe_delete(conn, sub_id)
        _db.delete_cached_food(conn, 222222)

    preview = client.post("/recipe/import-csv", data={
        "action": "preview", "recipes_text": recipes_text, "foods_text": foods_text,
    })
    assert preview.status_code == 200
    assert "Round Trip Quinoa Bowl" in preview.text
    assert "Round Trip Cooked Quinoa" in preview.text

    confirm = client.post("/recipe/import-csv", data={
        "action": "confirm", "recipes_text": recipes_text, "foods_text": foods_text,
    }, follow_redirects=False)
    assert confirm.status_code == 303
    assert "recipes_created=2" in confirm.headers["location"]

    with _db.get_db() as conn:
        recipes = {r["name"]: r["id"] for r in _db.recipe_list(conn)}
        assert "Round Trip Quinoa Bowl" in recipes
        assert "Round Trip Cooked Quinoa" in recipes
        bowl_ings = _db.recipe_get_ingredients(conn, recipes["Round Trip Quinoa Bowl"])
        assert bowl_ings[0]["ref_recipe_id"] == recipes["Round Trip Cooked Quinoa"]
        sub_ings = _db.recipe_get_ingredients(conn, recipes["Round Trip Cooked Quinoa"])
        assert sub_ings[0]["food_name"] == "Round Trip Quinoa"
        foods = [f["name"] for f in _db.list_cached_foods(conn)]
        assert "Round Trip Quinoa" in foods


def test_recipe_edit_running_totals_include_subrecipe_ingredient(client: TestClient) -> None:
    with _db.get_db() as conn:
        _db.cache_food(conn, 222223, "Running Totals Quinoa", "Foundation", None, None, None,
                        {"calories": 100.0, "protein_g": 5.0}, [])
        sub_id = _db.recipe_create(conn, "Running Totals Cooked Quinoa", "", 2, "Boil it.")
        _db.recipe_add_ingredient(conn, sub_id, 222223, "Running Totals Quinoa", 100.0, "100 g")
        main_id = _db.recipe_create(conn, "Running Totals Quinoa Bowl", "", 1, "Combine.")
        _db.recipe_add_ingredient(conn, main_id, 0, "Running Totals Cooked Quinoa", 1.0,
                                   "1 serving", ref_recipe_id=sub_id)

    resp = client.get(f"/recipe/{main_id}/edit")
    assert resp.status_code == 200
    # Sub-recipe is 2 servings of 100 g quinoa (5 g protein/100 g) = 5 g protein
    # for the whole batch; the main recipe uses 1 of those 2 servings, so its
    # running total must include 2.5 g of protein from the sub-recipe alone —
    # a hand-rolled direct-ingredients-only loop would show 0 g here.
    assert "2.5&thinsp;g" in resp.text


def test_food_search_by_barcode_prefers_cache_over_off(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    barcode = "012345678905"
    import openfoodfacts as _off
    off_fdc_id = _off.off_id(barcode)
    with _db.get_db() as conn:
        _db.cache_food(
            conn, off_fdc_id, "Already Cached Bar", "Open Food Facts",
            None, None, None, {"protein_g": 5.0}, None,
        )

    def fail_lookup(bc: str) -> None:
        raise AssertionError("should not hit Open Food Facts when already cached")

    monkeypatch.setattr("web.backend._off.lookup_by_barcode", fail_lookup)
    resp = client.get("/food/search", params={"query": barcode})
    assert resp.status_code == 200
    assert "Already Cached Bar" in resp.text


def test_food_search_by_barcode_not_found(client: TestClient) -> None:
    resp = client.get("/food/search", params={"query": "012345678905"})
    assert resp.status_code == 200
    assert "not found" in resp.text.lower()


def test_food_detail_page(client: TestClient, cached_food) -> None:
    resp = client.get(f"/food/{cached_food['fdcId']}")
    assert resp.status_code == 200


def test_food_detail_ul_column_has_asterisk_and_footnote(client: TestClient, cached_food) -> None:
    resp = client.get(f"/food/{cached_food['fdcId']}")
    assert resp.status_code == 200
    assert "UL*" in resp.text
    assert "Tolerable Upper Intake Level" in resp.text
    assert "Nutrient Targets" in resp.text


def test_unknown_food_detail_404s_gracefully(client: TestClient) -> None:
    resp = client.get("/food/999999999")
    assert resp.status_code in (200, 404)


def test_food_print_defaults_to_all_available_sections(client: TestClient, cached_food) -> None:
    resp = client.get(f"/food/{cached_food['fdcId']}/print")
    assert resp.status_code == 200
    assert "Nutrient Table" in resp.text
    assert "Protein Summary" in resp.text
    assert "Protein Quality" in resp.text


def test_food_print_section_selection_is_remembered(client: TestClient, cached_food) -> None:
    fdc_id = cached_food["fdcId"]
    resp = client.get(f"/food/{fdc_id}/print", params={
        "sections": ["protein_summary"], "sections_submitted": "1",
    })
    assert resp.status_code == 200
    assert "Nutrient Table" not in resp.text
    assert "Protein Summary" in resp.text

    resp2 = client.get(f"/food/{fdc_id}/print")
    assert "Nutrient Table" not in resp2.text
    assert "Protein Summary" in resp2.text


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


def test_meal_update_item_to_zero_grams(client: TestClient, cached_food, db_conn) -> None:
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
    item_id = db_conn.execute(
        "SELECT id FROM meal_items WHERE meal_id = ?", (meal_id,)
    ).fetchone()["id"]

    resp = client.post(
        f"/meal/{meal_id}/update/{item_id}", data={"amount": "0"}, follow_redirects=False,
    )
    assert resp.status_code == 303
    item = db_conn.execute("SELECT * FROM meal_items WHERE id = ?", (item_id,)).fetchone()
    assert item["amount"] == 0.0


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


def test_recipe_introduction_save_and_display(client: TestClient, db_conn) -> None:
    resp = client.post("/recipe/new", data={"name": "Chili", "servings": 4}, follow_redirects=False)
    recipe_id = int(resp.headers["location"].split("/recipe/")[1].split("/")[0])

    resp = client.post(
        f"/recipe/{recipe_id}/introduction",
        data={"introduction": "A family recipe from grandma."},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    recipe = db_conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    assert recipe["introduction"] == "A family recipe from grandma."

    # Shows on the edit page, right after Ingredients.
    edit_resp = client.get(f"/recipe/{recipe_id}/edit")
    assert edit_resp.text.index("sec-ingredients") < edit_resp.text.index("sec-introduction")
    assert "A family recipe from grandma." in edit_resp.text

    # Shows on the detail page and the print page, right after the title.
    detail_resp = client.get(f"/recipe/{recipe_id}")
    assert "A family recipe from grandma." in detail_resp.text

    print_resp = client.get(f"/recipe/{recipe_id}/print")
    assert print_resp.text.index("Chili") < print_resp.text.index("A family recipe from grandma.")
    assert "Introduction" in print_resp.text  # section checkbox label

    # Unchecking "Introduction" in the print section picker hides it — it is
    # not mandatory.
    hidden_resp = client.get(f"/recipe/{recipe_id}/print", params={
        "sections": ["ingredients"], "sections_submitted": "1",
    })
    assert "A family recipe from grandma." not in hidden_resp.text

    # Saving other recipe metadata must not clobber the introduction.
    client.post(
        f"/recipe/{recipe_id}/edit",
        data={"name": "Chili", "description": "Spicy", "servings": 6},
        follow_redirects=False,
    )
    recipe = db_conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    assert recipe["introduction"] == "A family recipe from grandma."


def test_recipe_print_defaults_to_all_available_sections(client: TestClient, cached_food, db_conn) -> None:
    resp = client.post("/recipe/new", data={"name": "Chicken Bowl", "servings": 2}, follow_redirects=False)
    recipe_id = int(resp.headers["location"].split("/recipe/")[1].split("/")[0])
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "200 g"},
        follow_redirects=False,
    )

    resp = client.get(f"/recipe/{recipe_id}/print")
    assert resp.status_code == 200
    assert "Ingredients" in resp.text
    assert "Nutrient Table" in resp.text
    assert "Protein Summary" in resp.text

    resp2 = client.get(f"/recipe/{recipe_id}/print", params={
        "sections": ["ingredients"], "sections_submitted": "1",
    })
    assert "Nutrient Table" not in resp2.text
    assert "Ingredients" in resp2.text

    resp3 = client.get(f"/recipe/{recipe_id}/print")
    assert "Nutrient Table" not in resp3.text
    assert "Ingredients" in resp3.text


def test_meal_print_defaults_to_all_available_sections(client: TestClient, cached_food) -> None:
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

    resp = client.get(f"/meal/{meal_id}/print")
    assert resp.status_code == 200
    assert "Foods &amp; Recipes" in resp.text
    assert "Nutrient Table" in resp.text


def test_meal_day_print_smoke(client: TestClient, cached_food) -> None:
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

    resp = client.get(f"/meal/{meal_id}/day/print")
    assert resp.status_code == 200
    assert "Meals" in resp.text
    assert "Nutrient Table" in resp.text


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


def test_food_detail_bare_gram_amount_recovers_piece_portion_label(client: TestClient, db_conn) -> None:
    import json as _json
    # A "piece" food whose portion gram_weight is a scaling placeholder, not
    # a literal weight — e.g. a supplement where "1 tablet" == 100 g so its
    # per-100g nutrients scale to "1 tablet" correctly.
    fdc_id = 999004
    portions = [{"description": "1 tablet", "gram_weight": 100.0}]
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (fdc_id, "Vitamin D Tablets", "User Drafted", None, None, None,
         _json.dumps({"vitamin_d_mcg": 25.0}), _json.dumps(portions)),
    )
    db_conn.commit()

    # A recipe/meal ingredient link passes only a bare gram total (no
    # portion_str) — here, 2 tablets' worth.
    resp = client.get(f"/food/{fdc_id}", params={"amount": "200"})
    assert resp.status_code == 200
    assert "2 × 1 tablet" in resp.text
    assert "200 g" not in resp.text


def test_nutrient_sections_ul_css_reflects_near_and_over_limit() -> None:
    max_limits = {"sodium_mg": 2300.0}
    # Under 90% of the limit: no warning at all.
    rows = backend._nutrient_sections(
        {"sodium_mg": 500.0}, daily_nutrients={"sodium_mg": 1000.0}, max_limits=max_limits,
    )
    row = next(r for s in rows for r in s["rows"] if r["label"].lower().startswith("sodium"))
    assert row["ul_css"] is None

    # 95% of the limit: "near" warning.
    rows = backend._nutrient_sections(
        {"sodium_mg": 500.0}, daily_nutrients={"sodium_mg": 2185.0}, max_limits=max_limits,
    )
    row = next(r for s in rows for r in s["rows"] if r["label"].lower().startswith("sodium"))
    assert row["ul_css"] == "limit-near"

    # At/over the limit: "over" warning.
    rows = backend._nutrient_sections(
        {"sodium_mg": 500.0}, daily_nutrients={"sodium_mg": 2400.0}, max_limits=max_limits,
    )
    row = next(r for s in rows for r in s["rows"] if r["label"].lower().startswith("sodium"))
    assert row["ul_css"] == "limit-over"


def test_custom_profile_copy_nutrients_overwrites_with_source_values(
    client: TestClient, db_conn, cached_food: dict
) -> None:
    resp = client.post(
        "/food/custom-profiles/create", data={"name": "Blank Draft"}, follow_redirects=False,
    )
    draft_id = int(resp.headers["location"].rsplit("/", 1)[-1].split("?")[0])

    resp = client.post(
        f"/food/custom-profiles/{draft_id}/copy-nutrients",
        data={"source_fdc_id": cached_food["fdcId"]},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert "nutrients_applied=ok" in resp.headers["location"]

    row = db_conn.execute("SELECT nutrients_json FROM foods WHERE fdc_id = ?", (draft_id,)).fetchone()
    copied = json.loads(row["nutrients_json"])
    # A raw, unscaled copy of the source's per-100g values — not scaled to
    # the draft's own (nonexistent) protein content.
    assert copied["protein_g"] == cached_food["nutrients"]["protein_g"]
    assert copied["aa_lysine_g"] == cached_food["nutrients"]["aa_lysine_g"]


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
    assert "Revised Optimal goal" in resp.text
    assert "% of Revised Optimal" in resp.text

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
    assert "Revised Optimal goal" in resp.text
    assert "limit-near" in resp.text or "limit-over" in resp.text

    resp = client.get("/summary/2026-07-11")
    assert resp.status_code == 200
    assert "Revised Optimal goal" in resp.text


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
    assert "Loaded recommended Revised Optimal targets" in resp.text


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


def test_settings_demo_data_load_and_clear(client: TestClient, tmp_path: pathlib.Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
    from numa_app.services import demo_data
    monkeypatch.setattr(demo_data, "_MARKER_FILE", tmp_path / "demo_data.json")

    resp = client.get("/settings")
    assert "Load starter data" in resp.text
    assert "Clear starter data" not in resp.text

    resp = client.post("/settings/starter-data/load", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=starter_data_loaded"

    with _db.get_db() as conn:
        assert conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == len(demo_data.DEMO_FOODS)
        assert conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == len(demo_data.DEMO_RECIPES)

    resp = client.get("/settings")
    assert "Clear starter data" in resp.text

    resp = client.post("/settings/starter-data/clear", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=starter_data_cleared"

    with _db.get_db() as conn:
        assert conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 0

    resp = client.get("/settings")
    assert "Load starter data" in resp.text


def test_settings_starter_data_restore_selected(client: TestClient, tmp_path: pathlib.Path,
                                                  monkeypatch: pytest.MonkeyPatch) -> None:
    from numa_app.services import demo_data
    monkeypatch.setattr(demo_data, "_MARKER_FILE", tmp_path / "demo_data.json")

    food = demo_data.DEMO_FOODS[0]
    resp = client.get("/settings")
    assert f"{food['fdc_id']} — {food['name']}" in resp.text

    resp = client.post(
        "/settings/starter-data/restore",
        data={"food_fdc_id": [str(food["fdc_id"])]},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == "/settings?saved=starter_data_restored#starter-data"

    with _db.get_db() as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM foods WHERE fdc_id=?", (food["fdc_id"],)
        ).fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 1

    resp = client.get("/settings")
    # No longer offered as a restore checkbox (it's present now)...
    assert f'value="{food["fdc_id"]}"' not in resp.text
    # ...but still listed in the always-visible "View all starter data" list.
    assert f"{food['fdc_id']} — {food['name']}" in resp.text


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


def test_meal_complement_sort_toggle_and_persistence(client: TestClient) -> None:
    """comp_sort/diaas_sort query params reorder the meal's suggestion sections
    and are remembered on later requests that omit them (like other list sorts,
    e.g. Food Cache's sort dropdown)."""
    low_lysine = dict(SAMPLE_NUTRIENTS)
    low_lysine["aa_lysine_g"] = 0.6
    fdc_id = 900003

    with _db.get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO foods (fdc_id, name, data_type, nutrients_json) VALUES (?, ?, ?, ?)",
            (fdc_id, "Low-lysine test food", "SR Legacy", json.dumps(low_lysine)),
        )
        conn.commit()
        meal_id = _db.meal_create(conn, "Lunch", datetime.date.today().isoformat())
        _db.meal_add_food(conn, meal_id, fdc_id, "Low-lysine test food", 150.0, "g")
        conn.commit()

    resp = client.get(f"/meal/{meal_id}")
    assert resp.status_code == 200
    assert "greatest effect" in resp.text.lower()
    assert '<option value="effect" selected>' in resp.text

    resp = client.get(f"/meal/{meal_id}?comp_sort=grams")
    assert resp.status_code == 200
    assert "smallest addition" in resp.text.lower()
    assert '<option value="grams" selected>' in resp.text

    # A later request that omits comp_sort still reflects the remembered choice.
    resp = client.get(f"/meal/{meal_id}")
    assert resp.status_code == 200
    assert '<option value="grams" selected>' in resp.text


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


def test_food_cache_delete_preserves_search_filter(client: TestClient, cached_food, db_conn) -> None:
    """Regression test: deleting from a filtered /food/cache?q=... view previously
    redirected to the unfiltered list, dropping q/sort/show_archived — making a
    successful delete look like it silently failed."""
    resp = client.post(
        "/food/cache/delete",
        data={"fdc_id": cached_food["fdcId"], "q": "chicken", "sort": "type", "show_archived": 1},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    location = resp.headers["location"]
    assert "q=chicken" in location
    assert "sort=type" in location
    assert "show_archived=1" in location
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


def _make_recipe(client: TestClient, name: str, servings: float, fdc_id: int, food_name: str,
                  portion_str: str) -> int:
    recipe_id = int(
        client.post("/recipe/new", data={"name": name, "servings": servings}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": fdc_id, "food_name": food_name, "portion_str": portion_str},
        follow_redirects=False,
    )
    return recipe_id


def test_recipe_compare_add_remove_and_cap(client: TestClient, cached_food) -> None:
    r1 = _make_recipe(client, "Recipe One", 1, cached_food["fdcId"], cached_food["name"], "100 g")
    r2 = _make_recipe(client, "Recipe Two", 1, cached_food["fdcId"], cached_food["name"], "100 g")

    resp = client.post("/recipe/compare/add", data={"recipe_id": r1, "ids": ""}, follow_redirects=False)
    assert resp.status_code == 303
    location = resp.headers["location"]
    assert f"ids={r1}" in location

    resp = client.post("/recipe/compare/add", data={"recipe_id": r2, "ids": str(r1)}, follow_redirects=False)
    ids_param = resp.headers["location"].split("ids=")[1].split("&")[0]
    assert ids_param == f"{r1},{r2}"

    resp = client.get(f"/recipe/compare?ids={r1},{r2}")
    assert resp.status_code == 200
    assert "Recipe One" in resp.text
    assert "Recipe Two" in resp.text
    assert "Nutrient comparison" in resp.text

    resp = client.post(
        "/recipe/compare/remove",
        data={"remove_id": r1, "ids": f"{r1},{r2}"},
        follow_redirects=False,
    )
    ids_param = resp.headers["location"].split("ids=")[1].split("&")[0]
    assert ids_param == str(r2)

    # Cap at _MAX_COMPARE_RECIPES (6): pad ids with dummy ids just under the cap.
    padded_ids = ",".join(str(i) for i in range(100, 106))
    resp = client.post(
        "/recipe/compare/add", data={"recipe_id": r1, "ids": padded_ids}, follow_redirects=False,
    )
    assert "error=Maximum" in resp.headers["location"]


def test_recipe_compare_ingredient_table_shows_shared_and_unique(
    client: TestClient, cached_food, second_cached_food,
) -> None:
    r1 = _make_recipe(client, "Shares Chicken", 1, cached_food["fdcId"], cached_food["name"], "100 g")
    client.post(
        f"/recipe/{r1}/ingredient/add",
        data={"fdc_id": second_cached_food["fdcId"], "food_name": second_cached_food["name"], "portion_str": "50 g"},
        follow_redirects=False,
    )
    r2 = _make_recipe(client, "Also Chicken", 1, cached_food["fdcId"], cached_food["name"], "200 g")

    resp = client.get(f"/recipe/compare?ids={r1},{r2}")
    assert resp.status_code == 200
    # Shared ingredient shows both amounts.
    assert "100.0" in resp.text or "100" in resp.text
    assert "200.0" in resp.text or "200" in resp.text
    # Unique-to-one-recipe ingredient still listed, with a "—" for the other.
    assert second_cached_food["name"] in resp.text
    assert "—" in resp.text


def test_recipe_compare_nutrient_scaling_per_serving_vs_batch(client: TestClient, cached_food) -> None:
    # 2 servings, 200g of a food with 31.0 g protein/100g => 62g total, 31g/serving.
    r1 = _make_recipe(client, "Scaled Recipe", 2, cached_food["fdcId"], cached_food["name"], "200 g")
    r2 = _make_recipe(client, "Other Recipe", 1, cached_food["fdcId"], cached_food["name"], "100 g")

    resp = client.get(f"/recipe/compare?ids={r1},{r2}&unit=serving")
    assert resp.status_code == 200
    assert "31.0" in resp.text  # per-serving protein for both recipes

    resp = client.get(f"/recipe/compare?ids={r1},{r2}&unit=batch")
    assert resp.status_code == 200
    assert "62.0" in resp.text  # whole-batch protein for the 2-serving recipe


def test_recipe_compare_protein_quality_section(client: TestClient, cached_food) -> None:
    r1 = _make_recipe(client, "AA Recipe One", 1, cached_food["fdcId"], cached_food["name"], "100 g")
    r2 = _make_recipe(client, "AA Recipe Two", 1, cached_food["fdcId"], cached_food["name"], "200 g")

    resp = client.get(f"/recipe/compare?ids={r1},{r2}")
    assert resp.status_code == 200
    assert "Protein quality comparison" in resp.text
    assert "Composite DIAAS score" in resp.text
    assert "Digestible complete protein (DCP)" in resp.text
    assert "Limiting amino acid" in resp.text


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


def test_food_use_recipes_page_lists_ingredient_usage(client: TestClient, cached_food: dict) -> None:
    recipe_id = int(
        client.post("/recipe/new", data={"name": "Chicken Bowl", "servings": 2}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "200 g"},
        follow_redirects=False,
    )

    resp = client.get("/analysis/food-use-recipes")
    assert resp.status_code == 200
    assert cached_food["name"] in resp.text
    assert "Chicken Bowl" not in resp.text  # the container recipe itself isn't a row; its ingredients are


def test_food_use_recipes_shows_subrecipe_as_its_own_row(client: TestClient, cached_food: dict) -> None:
    """A sub-recipe used as an ingredient of another recipe should appear as
    its own row (like a directly-added recipe does on Food Use in Meals), not
    just get silently flattened into its base ingredients."""
    sub_id = int(
        client.post("/recipe/new", data={"name": "House Dressing", "servings": 4}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{sub_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "100 g"},
        follow_redirects=False,
    )
    outer_id = int(
        client.post("/recipe/new", data={"name": "Salad", "servings": 2}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{outer_id}/ingredient/add-recipe",
        data={"ref_recipe_id": sub_id, "recipe_name": "House Dressing", "servings": 1},
        follow_redirects=False,
    )

    resp = client.get("/analysis/food-use-recipes")
    assert "House Dressing" in resp.text
    assert cached_food["name"] in resp.text


def test_substitute_food_in_meals(client: TestClient, cached_food: dict, db_conn) -> None:
    """Replacing a food across the currently-selected meals updates the
    meal_items rows in place (by ID, not by re-adding), including relabeling
    them with the replacement food's current name."""
    _db.cache_food(
        db_conn, fdc_id=999001, name="Natural Peanut Butter", data_type="Foundation",
        brand=None, serving_size=100.0, serving_unit="g", nutrients={"calories": 588, "protein_g": 25},
    )
    db_conn.commit()

    meal_id = int(
        client.post("/meals/create", data={"name": "Breakfast", "meal_date": "2026-07-20"}, follow_redirects=False)
        .headers["location"].rsplit("/", 1)[-1]
    )
    client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "150 g"},
        follow_redirects=False,
    )

    resp = client.post(
        "/analysis/food-use/substitute",
        data={
            "mode": "range", "ranges_raw": "2026-07-01:2026-07-31",
            "old_kind": "food", "old_id": cached_food["fdcId"],
            "new_kind": "food", "new_id": 999001,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert "substituted=1" in resp.headers["location"]

    item = db_conn.execute("SELECT * FROM meal_items WHERE meal_id = ?", (meal_id,)).fetchone()
    assert item["fdc_id"] == 999001
    assert item["food_name"] == "Natural Peanut Butter"
    assert item["amount"] == 150  # amount/unit carry over unchanged


def test_substitute_recipe_ingredient_recomputes_dcp(client: TestClient, cached_food: dict, db_conn) -> None:
    """Replacing an ingredient's underlying food across the selected recipes
    updates recipe_ingredients in place and recomputes the recipe's DCP —
    the same recompute that runs after any manual ingredient edit."""
    _db.cache_food(
        db_conn, fdc_id=999002, name="Chicken Thigh, raw", data_type="Foundation",
        brand=None, serving_size=100.0, serving_unit="g", nutrients=SAMPLE_NUTRIENTS,
    )
    db_conn.commit()

    recipe_id = int(
        client.post("/recipe/new", data={"name": "Dinner Bowl", "servings": 1}, follow_redirects=False)
        .headers["location"].split("/recipe/")[1].split("/")[0]
    )
    client.post(
        f"/recipe/{recipe_id}/ingredient/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "300 g"},
        follow_redirects=False,
    )
    before = db_conn.execute("SELECT dcp_g FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    assert before["dcp_g"] is not None

    resp = client.post(
        "/analysis/food-use-recipes/substitute",
        data={
            "mode": "ids", "recipe_ids": str(recipe_id),
            "old_kind": "food", "old_id": cached_food["fdcId"],
            "new_kind": "food", "new_id": 999002,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert "substituted=1" in resp.headers["location"]

    ing = db_conn.execute("SELECT * FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,)).fetchone()
    assert ing["fdc_id"] == 999002
    assert ing["food_name"] == "Chicken Thigh, raw"
    assert ing["amount"] == 300
    after = db_conn.execute("SELECT dcp_g FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    assert after["dcp_g"] is not None


def test_substitute_rejects_unknown_replacement(client: TestClient, cached_food: dict) -> None:
    meal_id = int(
        client.post("/meals/create", data={"name": "Lunch", "meal_date": "2026-07-20"}, follow_redirects=False)
        .headers["location"].rsplit("/", 1)[-1]
    )
    client.post(
        f"/meal/{meal_id}/add",
        data={"fdc_id": cached_food["fdcId"], "food_name": cached_food["name"], "portion_str": "100 g"},
        follow_redirects=False,
    )
    resp = client.post(
        "/analysis/food-use/substitute",
        data={
            "mode": "range", "ranges_raw": "2026-07-01:2026-07-31",
            "old_kind": "food", "old_id": cached_food["fdcId"],
            "new_kind": "food", "new_id": 424242,
        },
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert "error=" in resp.headers["location"]


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


def test_food_compare_uncached_food_shows_add_button_then_caches(
    client: TestClient, cached_food, monkeypatch, db_conn,
) -> None:
    import usda as _usda
    from tests.conftest import SAMPLE_FOOD_DETAIL

    uncached_fdc_id = 999123
    monkeypatch.setattr(_usda, "get_food_detail", lambda *a, **kw: (_ for _ in ()).throw(Exception("offline")))

    resp = client.get(
        "/food/compare",
        params={"ids": f"{cached_food['fdcId']},{uncached_fdc_id}", "amounts": "100.0,100.0"},
    )
    assert resp.status_code == 200
    assert "Add to food cache" in resp.text
    assert db_conn.execute("SELECT * FROM foods WHERE fdc_id = ?", (uncached_fdc_id,)).fetchone() is None

    fetched_detail = {**SAMPLE_FOOD_DETAIL, "fdcId": uncached_fdc_id}
    monkeypatch.setattr(_usda, "get_food_detail", lambda *a, **kw: fetched_detail)
    resp = client.post(
        "/food/compare/cache-food",
        data={"fdc_id": uncached_fdc_id,
              "ids": f"{cached_food['fdcId']},{uncached_fdc_id}", "amounts": "100.0,100.0"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert db_conn.execute("SELECT * FROM foods WHERE fdc_id = ?", (uncached_fdc_id,)).fetchone() is not None

    resp = client.get(resp.headers["location"])
    assert "In food cache" in resp.text


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


def test_unusable_protein_line_renders_for_incomplete_food(client: TestClient, db_conn):
    import json as _json
    nutrients = dict(SAMPLE_NUTRIENTS)
    nutrients["aa_lysine_g"] = 0.2  # force a limiting amino acid gap
    fdc_id = 999001
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (fdc_id, "Chicken, broilers or fryers, breast, meat only, raw", "SR Legacy", None, 100.0, "g", _json.dumps(nutrients), "[]"),
    )
    db_conn.commit()
    resp = client.get(f"/food/{fdc_id}", params={"amount": "100"})
    assert resp.status_code == 200
    html = resp.text
    assert "cannot be built into tissue" in html
    assert "unusable-protein-fate" in html
    # Numeric cross-check: the displayed grams and percent must agree with
    # each other and with the 31 g raw protein SAMPLE_NUTRIENTS carries at a
    # 100 g portion — not just that the line renders at all.
    m = re.search(r'([\d.]+)&thinsp;g \((\d+)%\) of that protein cannot be built', html)
    assert m is not None
    unusable_g, unusable_pct = float(m.group(1)), int(m.group(2))
    raw_protein_g = 31.0
    assert 0 < unusable_g < raw_protein_g
    assert unusable_pct == round(100 * unusable_g / raw_protein_g)


def test_food_detail_dcp_summary_line_percent_matches_grams(client: TestClient, db_conn):
    import json as _json
    nutrients = dict(SAMPLE_NUTRIENTS)
    nutrients["aa_lysine_g"] = 0.2  # force a limiting amino acid gap
    fdc_id = 999003
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (fdc_id, "Chicken, broilers or fryers, breast, meat only, raw", "SR Legacy", None, 100.0, "g", _json.dumps(nutrients), "[]"),
    )
    db_conn.commit()
    resp = client.get(f"/food/{fdc_id}", params={"amount": "100"})
    assert resp.status_code == 200
    html = resp.text
    m = re.search(r'([\d.]+)&thinsp;g digestible complete protein &mdash; (\d+)% of ([\d.]+)&thinsp;g raw protein', html)
    assert m is not None
    dcp_g, pct, raw_g = float(m.group(1)), int(m.group(2)), float(m.group(3))
    assert raw_g == 31.0  # SAMPLE_NUTRIENTS protein_g at a 100 g portion
    assert 0 < dcp_g < raw_g
    assert pct == round(100 * dcp_g / raw_g)


def test_unusable_protein_line_absent_for_complete_food(client: TestClient, db_conn):
    import json as _json
    fdc_id = 999002
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (fdc_id, "Chicken, broilers or fryers, breast, meat only, raw", "SR Legacy", None, 100.0, "g", _json.dumps(SAMPLE_NUTRIENTS), "[]"),
    )
    db_conn.commit()
    resp = client.get(f"/food/{fdc_id}", params={"amount": "100"})
    assert resp.status_code == 200
    # A DIAAS of 1.0 (complete protein, no limiting amino acid) leaves
    # unusable_g at 0, and the line must be suppressed entirely — not shown
    # as "0.0 g (0%)".
    assert "cannot be built into tissue" not in resp.text
