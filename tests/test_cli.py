"""
Tests for the numa CLI (numa_app package).

Strategy:
  - NumaTestRunner replaces typer CliRunner. It calls run_app() directly,
    replacing sys.stdin with io.StringIO(input) and redirecting the rich
    Console to a buffer so output is capturable.
  - _prompt() falls back to rich Prompt.ask() when stdin is not a tty (the
    io.StringIO case), which calls input() — reading from sys.stdin.
  - USDA API calls are mocked at the usda.search_foods / usda.get_food_detail
    level so tests never hit the network.
  - The food cache (db.foods) is pre-populated via the `cached_food` fixture
    when a test needs a known food available locally.
  - _offer_export() is mocked to a no-op via the autouse `no_export` fixture,
    so tests don't write real files and don't need extra input lines.

Input sequence notation used in comments:
    Main menu choices: 1=Foods, 2=Recipes, 3=Meals, 4=Analysis, 5=Settings, q=Quit
    Analysis submenu:  1=Daily summary - DCP and goals, 2=Food use in meals, m=Main, q=Quit
    Foods submenu:     1=Search, 2=Analyze USDA portion, 3=Analyze recipe portion,
                       4=Convert, 5=View cached, 6=Pantry, b=Back, q=Quit
    Recipes submenu:   1=Create, 2=Browse (action+id: v/e/x/a/d/c), 3=Develop, b=Back, q=Quit
    Settings submenu:  1=Theme, 2=User profile, 3=Daily targets, 4=Dietary prefs,
                       5=Editor, 6=Display settings, 7=Advanced (API key/DB/DIAAS), b=Back
"""

import json
import subprocess
import sys
from datetime import date, timedelta
from unittest.mock import patch

import pytest

import db as _db
import profile as _profile
import usda as _usda
import usda_api as _usda_api
from numa_app.services.portions import _parse_portion_input
from numa_app.ui.render import _volume_hint
from tests.conftest import (
    SAMPLE_FDC_ID,
    SAMPLE_FOOD_DETAIL,
    SAMPLE_NUTRIENTS,
    SAMPLE_NUTRIENTS_2,
    SAMPLE_SEARCH_RESULTS,
    NumaTestRunner,
    nutrient_target_menu_index,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_api(monkeypatch: pytest.MonkeyPatch):
    """
    Patch out both USDA API functions.
    search_foods returns SAMPLE_SEARCH_RESULTS.
    get_food_detail returns SAMPLE_FOOD_DETAIL.
    get_api_key returns a dummy key so _ensure_api_key() passes immediately.
    """
    monkeypatch.setattr(_usda, "search_foods", lambda *a, **kw: SAMPLE_SEARCH_RESULTS)
    monkeypatch.setattr(_usda, "get_food_detail", lambda *a, **kw: SAMPLE_FOOD_DETAIL)
    monkeypatch.setattr(_usda, "get_api_key", lambda: "TESTKEY123")


# ---------------------------------------------------------------------------
# _parse_portion_input
# ---------------------------------------------------------------------------

SAMPLE_PORTIONS = [
    {"description": "1 cup",  "gram_weight": 240.0},
    {"description": "1 tbsp", "gram_weight":  15.0},
]


class TestParsePortionInput:
    def test_plain_number_is_piece_count(self):
        grams, label = _parse_portion_input("150", [])
        assert grams == pytest.approx(0.0)
        assert "pc" in label

    def test_grams_unit(self):
        grams, label = _parse_portion_input("200 g", [])
        assert grams == pytest.approx(200.0)

    def test_gr_unit(self):
        grams, label = _parse_portion_input("65 gr", [])
        assert grams == pytest.approx(65.0)

    def test_ounces(self):
        grams, label = _parse_portion_input("3 oz", [])
        assert grams == pytest.approx(3 * 28.3495)
        assert "oz" in label

    def test_pounds(self):
        grams, label = _parse_portion_input("0.5 lb", [])
        assert grams == pytest.approx(0.5 * 453.592)

    def test_kg(self):
        grams, label = _parse_portion_input("0.2 kg", [])
        assert grams == pytest.approx(200.0)

    def test_portion_shortcut_p1(self):
        grams, label = _parse_portion_input("p1", SAMPLE_PORTIONS)
        assert grams == pytest.approx(240.0)
        assert "1 cup" in label

    def test_portion_shortcut_p2(self):
        grams, label = _parse_portion_input("p2", SAMPLE_PORTIONS)
        assert grams == pytest.approx(15.0)

    def test_fractional_portion_multiplier(self):
        grams, label = _parse_portion_input("1.5 p1", SAMPLE_PORTIONS)
        assert grams == pytest.approx(1.5 * 240.0)
        assert "1.5" in label
        assert "1 cup" in label

    def test_fraction_less_than_one(self):
        grams, label = _parse_portion_input("0.5 p2", SAMPLE_PORTIONS)
        assert grams == pytest.approx(0.5 * 15.0)

    def test_truly_unknown_unit_returns_none(self):
        assert _parse_portion_input("2 furlongs", []) is None

    def test_out_of_range_p_returns_none(self):
        assert _parse_portion_input("p5", SAMPLE_PORTIONS) is None

    def test_empty_string_returns_none(self):
        assert _parse_portion_input("", []) is None

    def test_non_numeric_returns_none(self):
        assert _parse_portion_input("lots", []) is None

    # --- fraction parsing ---

    def test_plain_fraction_is_piece_count(self):
        grams, label = _parse_portion_input("1/4", [])
        assert grams == pytest.approx(0.0)
        assert "pc" in label

    def test_mixed_number_is_piece_count(self):
        grams, label = _parse_portion_input("1 1/2", [])
        assert grams == pytest.approx(0.0)
        assert "pc" in label

    # --- volume inputs ---

    def test_volume_with_known_density_food_name(self):
        # nutritional yeast density ≈ 0.61 g/ml; 1/8 cup = 29.575 ml
        grams, label = _parse_portion_input("1/8 cup", [], food_name="Nutritional yeast")
        assert grams == pytest.approx(0.125 * 236.6 * 0.61, rel=0.05)
        assert "cup" in label

    def test_volume_with_portions_derived_density(self):
        # SAMPLE_PORTIONS has "1 cup" = 240 g → density = 240 / 236.6 ≈ 1.015 g/ml
        grams, label = _parse_portion_input("2 tbsp", SAMPLE_PORTIONS, food_name="")
        expected = 2 * 14.8 * (240.0 / 236.6)
        assert grams == pytest.approx(expected, rel=0.01)

    def test_volume_unknown_density_returns_none_grams(self):
        # No portions, food name not in density table → (None, vol_display)
        # Caller uses this to ask the user for grams instead.
        result = _parse_portion_input("2 tbsp", [], food_name="mystery ingredient xyz")
        assert isinstance(result, tuple)
        assert result[0] is None
        assert "tbsp" in result[1]

    def test_shorthand_c_is_cup(self):
        grams, _ = _parse_portion_input("1 c", [], food_name="Nutritional yeast")
        assert grams == pytest.approx(1 * 236.6 * 0.61, rel=0.05)

    def test_shorthand_capital_T_is_tablespoon(self):
        grams, _ = _parse_portion_input("2 T", SAMPLE_PORTIONS, food_name="")
        expected = 2 * 14.8 * (240.0 / 236.6)
        assert grams == pytest.approx(expected, rel=0.01)

    def test_shorthand_lowercase_t_is_teaspoon(self):
        grams, _ = _parse_portion_input("3 t", SAMPLE_PORTIONS, food_name="")
        expected = 3 * 4.9 * (240.0 / 236.6)
        assert grams == pytest.approx(expected, rel=0.01)

    def test_capital_T_and_lowercase_t_differ(self):
        # T=tablespoon (14.8 ml), t=teaspoon (4.9 ml) — must not be equal
        density = 240.0 / 236.6
        grams_T, _ = _parse_portion_input("1 T", SAMPLE_PORTIONS)
        grams_t, _ = _parse_portion_input("1 t", SAMPLE_PORTIONS)
        assert grams_T == pytest.approx(14.8 * density, rel=0.01)
        assert grams_t == pytest.approx(4.9 * density, rel=0.01)
        assert grams_T != pytest.approx(grams_t)


# ---------------------------------------------------------------------------
# Basic startup / help
# ---------------------------------------------------------------------------

class TestStartup:
    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, "numa.py", "--help"],
            capture_output=True, text=True,
            cwd="/home/tomc/Dropbox/www/__Active/Obsidian-vault/_sync2/Python-work/numa",
        )
        assert result.returncode == 0
        assert "numa" in result.stdout.lower()

    def test_api_key_flag_saves_and_exits(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        config_file = tmp_path / "config.json"
        monkeypatch.setattr(_usda_api, "_CONFIG_FILE", config_file)
        result = runner.invoke(api_key="MYKEY123")
        assert result.exit_code == 0
        assert "saved" in result.output.lower()
        assert "MYKEY123" in config_file.read_text()

    def test_quit_from_main_menu(self, runner: NumaTestRunner):
        result = runner.invoke(input="q\n")
        assert result.exit_code == 0

    def test_invalid_main_menu_choice_reprompts(self, runner: NumaTestRunner):
        # Enter an invalid choice, then quit
        result = runner.invoke(input="z\nq\n")
        assert result.exit_code == 0
        assert "valid" in result.output.lower()


# ---------------------------------------------------------------------------
# Foods menu
# ---------------------------------------------------------------------------

class TestFoodsMenu:
    def test_enter_and_back(self, runner: NumaTestRunner):
        # Main: 1 (Foods) → Foods: b (Back) → Main: q (Quit)
        result = runner.invoke(input="1\nb\nq\n")
        assert result.exit_code == 0
        assert "Foods" in result.output

    def test_search_displays_results(self, runner: NumaTestRunner, monkeypatch):
        _mock_api(monkeypatch)
        # Main: 1 → Foods: 1 (Search) → query: "chicken" → pick: 1 → n (skip portion) → b → q
        result = runner.invoke(input="1\n1\nchicken\n1\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "Chicken" in result.output

    def test_search_shows_nutrient_table(self, runner: NumaTestRunner, monkeypatch):
        _mock_api(monkeypatch)
        # Main: 1 → Foods: 1 (Search) → query: "chicken" → pick: 1 → n (skip portion) → b → q
        result = runner.invoke(input="1\n1\nchicken\n1\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output
        assert "Calories" in result.output

    def test_analyze_portion_scales_nutrients(self, runner: NumaTestRunner, monkeypatch):
        _mock_api(monkeypatch)
        # pick food, enter 200g portion (double the 100g base)
        result = runner.invoke(input="1\n2\nchicken\n1\n200 g\nb\nq\n")
        assert result.exit_code == 0
        # 31g protein * 2 = 62g
        assert "62" in result.output

    def test_empty_search_query_returns_to_menu(self, runner: NumaTestRunner, monkeypatch):
        _mock_api(monkeypatch)
        # Empty query → no search → back → quit
        result = runner.invoke(input="1\n1\n\nb\nq\n")
        assert result.exit_code == 0

    def test_list_cached_foods_empty(self, runner: NumaTestRunner):
        # Foods item 6 = View cached (item 5 is now Compare foods)
        result = runner.invoke(input="1\n6\nb\nq\n")
        assert result.exit_code == 0
        assert "cached" in result.output.lower() or "No foods" in result.output

    def test_list_cached_foods_shows_entry(self, runner: NumaTestRunner, cached_food):
        result = runner.invoke(input="1\n6\nb\nq\n")
        assert result.exit_code == 0
        assert "Chicken" in result.output

    def test_prune_unused_deletes_unreferenced_food(self, runner: NumaTestRunner, cached_food):
        # cached_food is not referenced by any pantry entry, recipe, or meal.
        # Foods(1) -> Food Cache(6) -> prune(u) -> confirm(y) -> back -> quit
        result = runner.invoke(input="1\n6\nu\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "Pruned 1 unused food" in result.output
        with _db.get_db() as conn:
            assert _db.get_cached_food(conn, cached_food["fdcId"]) is None

    def test_prune_unused_none_to_prune(self, runner: NumaTestRunner, db_conn, cached_food):
        # Reference the food from the pantry so it's no longer "unused"
        with _db.get_db() as conn:
            _db.pantry_add(conn, cached_food["name"], cached_food["fdcId"])
        result = runner.invoke(input="1\n6\nu\nb\nq\n")
        assert result.exit_code == 0
        assert "No unused foods to prune" in result.output
        with _db.get_db() as conn:
            assert _db.get_cached_food(conn, cached_food["fdcId"]) is not None

    def test_search_offers_portion_analysis_accept(self, runner: NumaTestRunner, monkeypatch):
        """After viewing per-100g nutrients, pressing y leads to scaled portion output."""
        _mock_api(monkeypatch)
        # Foods: 1 (Search) → chicken → pick 1 → y → 200g → back → quit
        result = runner.invoke(input="1\n1\nchicken\n1\ny\n200 g\nb\nq\n")
        assert result.exit_code == 0
        assert "62" in result.output   # 31g protein × 2

    def test_search_offers_portion_analysis_decline(self, runner: NumaTestRunner, monkeypatch):
        """Pressing n at the portion offer returns to the foods menu without scaling."""
        _mock_api(monkeypatch)
        result = runner.invoke(input="1\n1\nchicken\n1\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output
        assert "62.00" not in result.output   # no 200g scaled result (31g × 2)

    def test_search_shows_optimal_column_when_configured(self, runner: NumaTestRunner, monkeypatch):
        """Configuring a Profile Optimal target for Vitamin D adds the 'Profile Optimal'
        column group to the food nutrient table."""
        _mock_api(monkeypatch)
        idx = nutrient_target_menu_index("vitamin_d_mcg")
        # Settings(5) → Nutrient targets(9) → Vitamin D → Optimal target(1) → 50 → back(b) → main(m)
        # → Foods(1) → Search(1) → chicken → pick 1 → n (skip portion) → b → q
        result = runner.invoke(
            input=f"5\n9\n{idx}\n1\n50\nb\nm\n1\n1\nchicken\n1\nn\nb\nq\n"
        )
        assert result.exit_code == 0
        assert "Profile Optimal" in result.output
        assert "50.0 mcg" in result.output

    def test_search_no_optimal_column_when_unconfigured(self, runner: NumaTestRunner, monkeypatch):
        """Without any Profile Optimal targets set, the food nutrient table renders
        exactly as before — no 'Profile Optimal' column group."""
        _mock_api(monkeypatch)
        result = runner.invoke(input="1\n1\nchicken\n1\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "Profile Optimal" not in result.output

    def test_invalid_portion_input_retries(self, runner: NumaTestRunner, monkeypatch):
        """Bad portion input shows an error and re-prompts rather than dropping to the menu."""
        _mock_api(monkeypatch)
        # Foods: 2 (Analyze) → bad input → valid 200g → scaled nutrients shown
        result = runner.invoke(input="1\n2\nchicken\n1\nbadstuff\n200 g\nb\nq\n")
        assert result.exit_code == 0
        assert "Unrecognized" in result.output or "recognised" in result.output.lower()
        assert "62" in result.output   # recovered and computed 31g × 2


# ---------------------------------------------------------------------------
# Foods menu — analyze recipe portion (item 3)
# ---------------------------------------------------------------------------

class TestFoodsRecipePortionAnalysis:
    def test_analyze_recipe_portion_shows_nutrients(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """Foods → 3 analyzes a saved recipe by portion and prints a nutrient table."""
        _mock_api(monkeypatch)
        # Create a recipe with 2 servings of 200g chicken
        # Sequence: name → desc → servings → serving_size(skip) → vol(skip) → weight(skip) →
        #           complete(n) → search → pick → amount g → note(skip) → no more → editor(b=skip) → quit
        runner.invoke(input="2\n1\nChicken Dish\n\n2\n\n\n\nn\nchicken\n1\n200 g\n\nn\nb\nq\n")

        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]

        # Foods → 3 → list-all(empty) → recipe id → 1 serving → back → quit
        result = runner.invoke(input=f"1\n3\n\n{rid}\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output

    def test_analyze_recipe_portion_back_on_empty_id(
        self, runner: NumaTestRunner, cached_food
    ):
        """Pressing Enter (empty ID) at the recipe ID prompt returns without error."""
        result = runner.invoke(input="1\n3\n\nb\nq\n")
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Recipes menu
# ---------------------------------------------------------------------------

class TestRecipesMenu:
    def test_enter_and_back(self, runner: NumaTestRunner):
        result = runner.invoke(input="2\nb\nq\n")
        assert result.exit_code == 0
        assert "Recipe" in result.output

    def test_list_empty(self, runner: NumaTestRunner):
        result = runner.invoke(input="2\n2\nb\nq\n")
        assert result.exit_code == 0
        assert "No recipes" in result.output

    def test_create_recipe(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Recipes: 1 (Create) → name → description → servings → serving_size(skip) →
        # vol(skip) → weight(skip) → complete(n) →
        # search "chicken" → pick 1 → amount 150 → note(skip) →
        # add another? n → editor(b=skip) → q
        inp = "2\n1\nChicken Salad\nA fresh salad\n2\n\n\n\nn\nchicken\n1\n150\n\nn\nb\nq\n"
        result = runner.invoke(input=inp)
        assert result.exit_code == 0
        assert "saved" in result.output.lower() or "created" in result.output.lower()

        with _db.get_db() as conn:
            recipes = _db.recipe_list(conn)
        assert len(recipes) == 1
        assert recipes[0]["name"] == "Chicken Salad"

    def test_create_recipe_saves_ingredients(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        inp = "2\n1\nMy Recipe\n\n1\n\n\n\nn\nchicken\n1\n100 g\n\nn\nb\nq\n"
        runner.invoke(input=inp)

        with _db.get_db() as conn:
            recipes = _db.recipe_list(conn)
            rid = recipes[0]["id"]
            ings = _db.recipe_get_ingredients(conn, rid)
        assert len(ings) == 1
        assert ings[0]["fdc_id"] == SAMPLE_FDC_ID

    def test_list_recipe_after_create(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Create one recipe
        runner.invoke(input="2\n1\nSoup\n\n1\n\n\n\nn\nchicken\n1\n100\n\nn\nb\nq\n")
        # List recipes: empty search → list all → auto-returns (single page) → quit
        result = runner.invoke(input="2\n2\n\nq\n")
        assert "Soup" in result.output

    def test_delete_recipe(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Create
        runner.invoke(input="2\n1\nDeleteMe\n\n1\n\n\n\nn\nchicken\n1\n100 g\n\nn\nb\nq\n")

        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]

        # Delete (Recipes: 2=Browse → d{id} → confirm y → q=quit)
        result = runner.invoke(input=f"2\n2\nd{rid}\ny\nq\n")
        assert result.exit_code == 0
        assert "Deleted" in result.output

        with _db.get_db() as conn:
            assert _db.recipe_list(conn) == []

    def test_recreate_recipe_offers_relink_to_broken_meal_ref(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Create "Beef Stew", reference it from a meal, then delete it —
        # leaving the meal item's recipe_id dangling.
        runner.invoke(input="2\n1\nBeef Stew\n\n1\n\n\n\nn\nchicken\n1\n100 g\n\nn\nb\nq\n")
        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]
            meal_id = _db.meal_create(conn, "Dinner", "2026-07-15")
            _db.meal_add_recipe(conn, meal_id, rid, "Beef Stew", 1)
        runner.invoke(input=f"2\n2\nd{rid}\ny\nq\n")

        # Re-create as "Chicken Stew" (fuzzy match: shares the word "Stew") —
        # name → description → servings → serving_size/vol/weight (skip) →
        # complete(n) → relink prompt (y) → ingredient loop (b=skip) →
        # editor (b=skip) → q
        result = runner.invoke(input="2\n1\nChicken Stew\n\n1\n\n\n\nn\ny\nb\nb\nq\n")
        assert result.exit_code == 0
        assert "Found broken recipe references that may belong to" in result.output
        assert "Beef Stew" in result.output
        assert "Relinked 1 meal item(s)" in result.output

        with _db.get_db() as conn:
            new_rid = [r["id"] for r in _db.recipe_list(conn) if r["id"] != rid][0]
            item = _db.meal_get_items(conn, meal_id)[0]
        assert item["recipe_id"] == new_rid

    def test_broken_recipe_refs_menu_lists_dangling_meal_ref(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="2\n1\nChili\n\n1\n\n\n\nn\nchicken\n1\n100 g\n\nn\nb\nq\n")
        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]
            meal_id = _db.meal_create(conn, "Lunch", "2026-07-15")
            _db.meal_add_recipe(conn, meal_id, rid, "Chili", 1)
        runner.invoke(input=f"2\n2\nd{rid}\ny\nq\n")

        # Recipes menu → 6 (Broken recipe references) → back → quit
        result = runner.invoke(input="2\n6\nb\nq\n")
        assert result.exit_code == 0
        assert "Broken recipe references" in result.output
        assert "Chili" in result.output
        assert "Lunch" in result.output

    def test_view_recipe_shows_nutrients(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="2\n1\nChicken Dish\n\n2\n\n\n\nn\nchicken\n1\n200 g\n\nn\nb\nq\n")

        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]

        # Recipes: 2=Browse → a{id} (analyze) → q=quit; export is mocked to no-op
        result = runner.invoke(input=f"2\n2\na{rid}\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output


# ---------------------------------------------------------------------------
# Meals menu
# ---------------------------------------------------------------------------

class TestMealsMenu:
    def test_enter_and_back(self, runner: NumaTestRunner):
        result = runner.invoke(input="3\nb\nq\n")
        assert result.exit_code == 0
        assert "Meal" in result.output

    def test_log_meal_with_food(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Meals: n (new) → date → name → add item: 1 (food) → search → pick → amount → done: d
        inp = "3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n150\ny\n\nd\nb\nq\n"
        result = runner.invoke(input=inp)
        assert result.exit_code == 0
        assert "logged" in result.output.lower() or "Meal" in result.output

        with _db.get_db() as conn:
            meals = _db.meal_list_by_date(conn, "2025-03-15")
        assert len(meals) == 1
        assert meals[0]["name"] == "Lunch"

    def test_log_meal_saves_food_item(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        inp = "3\nn\n2025-03-15\nDinner\n1\nchicken\n1\n200 g\n\nd\nb\nq\n"
        runner.invoke(input=inp)

        with _db.get_db() as conn:
            meals = _db.meal_list_by_date(conn, "2025-03-15")
            items = _db.meal_get_items(conn, meals[0]["id"])
        assert len(items) == 1
        assert items[0]["amount"] == 200.0

    def test_view_meals_empty_date(self, runner: NumaTestRunner):
        result = runner.invoke(input="3\nq\n")
        assert result.exit_code == 0
        assert "No meals" in result.output

    def test_view_meals_shows_entry(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nBreakfast\n1\nchicken\n1\n100\ny\n\nd\nb\nq\n")
        # v1 = view meal ID 1, then b=back from action loop, q=quit
        result = runner.invoke(input="3\nv1\nb\nq\n")
        assert "Breakfast" in result.output

    def test_view_meals_shows_food_items(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n150 g\n\nd\nb\nq\n")
        result = runner.invoke(input="3\nv1\nb\nq\n")
        assert result.exit_code == 0
        assert "Chicken" in result.output
        assert "150" in result.output

    def test_view_meals_delete_item(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n200 g\n\nd\nb\nq\n")

        with _db.get_db() as conn:
            mid = _db.meal_list_by_date(conn, "2025-03-15")[0]["id"]
            iid = _db.meal_get_items(conn, mid)[0]["id"]

        # v1=view meal ID 1 → action 3 (delete item) → item id → b → q
        result = runner.invoke(input=f"3\nv1\n3\n{iid}\nb\nq\n")
        assert result.exit_code == 0
        assert "removed" in result.output.lower()

        with _db.get_db() as conn:
            assert _db.meal_get_items(conn, mid) == []

    def test_analyze_meal_shows_nutrients(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")

        # a1=analyze meal ID 1; only 1 meal on that date so no scope prompt
        # n = decline "Refresh AA data from USDA?" prompt at end of analysis
        result = runner.invoke(input="3\na1\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output

    def test_delete_meal(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100\ny\n\nd\nb\nq\n")

        # d1=delete meal ID 1, confirm y, then q
        result = runner.invoke(input="3\nd1\ny\nq\n")
        assert result.exit_code == 0
        assert "Deleted" in result.output

        with _db.get_db() as conn:
            assert _db.meal_list_by_date(conn, "2025-03-15") == []

    # ------------------------------------------------------------------
    # DCP columns and p-command
    # ------------------------------------------------------------------

    def test_meal_set_bcp_stores_value(self, db_conn):
        """meal_set_bcp writes bcp_g and bcp_computed_at; meal_get returns them."""
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Test", "2025-04-01")
        _db.meal_set_bcp(db_conn, mid, 24.5)
        db_conn.commit()
        row = _db.meal_get(db_conn, mid)
        assert row["bcp_g"] == pytest.approx(24.5)
        assert row["bcp_computed_at"] is not None

    def test_meal_set_bcp_null_stores_null(self, db_conn):
        """meal_set_bcp with None marks computed_at but leaves bcp_g NULL (no AA data)."""
        with _db.get_db() as conn:
            mid = _db.meal_create(conn, "Test", "2025-04-01")
        _db.meal_set_bcp(db_conn, mid, None)
        db_conn.commit()
        row = _db.meal_get(db_conn, mid)
        assert row["bcp_g"] is None
        assert row["bcp_computed_at"] is not None

    def test_compute_meal_bcp_returns_float_for_food_with_aa(self, runner, monkeypatch, cached_food):
        """_compute_meal_bcp returns a positive float when meal has AA-complete food."""
        from numa_app.workflows.meals import _compute_meal_bcp
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        with _db.get_db() as conn:
            mid = _db.meal_list_by_date(conn, "2025-03-15")[0]["id"]
        bcp = _compute_meal_bcp(mid)
        assert bcp is not None
        assert bcp > 0.0

    def test_bcp_columns_shown_in_table(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Meal DCP and Day DCP column headers always appear in the meals list."""
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="3\nb\nq\n")
        assert result.exit_code == 0
        assert "Meal DCP" in result.output
        assert "Day DCP" in result.output

    def test_bcp_footer_explains_abbreviation(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Footer below the table explains what DCP means and that p recomputes."""
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="3\nb\nq\n")
        assert "bioavailable" in result.output
        assert "digestible" in result.output

    def _setup_complete_meal(self, runner, monkeypatch, date="2025-03-15", name="Lunch"):
        """Helper: create a meal with 100 g chicken and mark it complete."""
        _mock_api(monkeypatch)
        # n=new → date → name → 1=add items → search → pick → 100g → note → d=done → 6=mark complete → b=back
        runner.invoke(
            input=f"3\nn\n{date}\n{name}\n1\nchicken\n1\n100 g\n\n\nd\n6\nb\nq\n"
        )

    def test_p_command_computes_bcp_for_complete_meal(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Pressing p computes DCP and it appears in the table output."""
        self._setup_complete_meal(runner, monkeypatch)
        # c=calculate, Enter=default "all meals and days" → table re-renders with value → b=back → q=quit
        result = runner.invoke(input="3\nc\n\nb\nq\n")
        assert result.exit_code == 0
        # DCP value should appear as "XX.X g" in the output
        assert " g" in result.output
        # Stored in DB
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, "2025-03-15")[0]
        assert row["bcp_g"] is not None
        assert row["bcp_g"] > 0.0

    def test_p_command_no_complete_meals_shows_message(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Pressing p when no meals are complete shows an informative message."""
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="3\nc\n\nb\nq\n")
        assert result.exit_code == 0
        assert "No complete meals" in result.output

    def test_bcp_persists_across_sessions(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """DCP computed via p is stored in the DB and shown in subsequent sessions."""
        self._setup_complete_meal(runner, monkeypatch)
        runner.invoke(input="3\nc\n\nb\nq\n")  # compute and store
        # Fresh session: visit meals list without pressing p
        result = runner.invoke(input="3\nb\nq\n")
        assert result.exit_code == 0
        # A numeric DCP value (not just "—") should appear
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, "2025-03-15")[0]
        stored = row["bcp_g"]
        assert stored is not None
        assert f"{stored:.1f} g" in result.output

    def test_day_bcp_sums_complete_meals_on_same_date(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Day DCP = sum of DCP for all complete meals on the date, shown only on the topmost row."""
        self._setup_complete_meal(runner, monkeypatch, name="Breakfast")
        runner.invoke(
            input="3\nn\n2025-03-15\nDinner\n1\nchicken\n1\n100 g\n\n\nd\n6\nb\nq\n"
        )
        runner.invoke(input="3\nc\n\nb\nq\n")  # compute DCPs
        with _db.get_db() as conn:
            meals = _db.meal_list_by_date(conn, "2025-03-15")
        bcps = [m["bcp_g"] for m in meals if m["bcp_g"] is not None]
        assert len(bcps) == 2
        expected_day = sum(bcps)
        expected_str = f"{expected_day:.1f} g"
        result = runner.invoke(input="3\nb\nq\n")
        assert result.output.count(expected_str) == 1  # appears exactly once (topmost row)

    def test_pct_goal_column_header_always_shown(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """'% profile goal' column header appears in the meals table regardless of profile."""
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="3\nb\nq\n")
        assert "% profile goal" in result.output

    def test_pct_goal_dash_without_profile(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Without a profile the % goal cell stays '—' after p is pressed."""
        # Remove the Default profile the autouse fixture created so there's truly no profile.
        for f in _profile._PROFILES_DIR.glob("*.json"):
            f.unlink()
        self._setup_complete_meal(runner, monkeypatch)
        runner.invoke(input="3\nc\n\nb\nq\n")
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, "2025-03-15")[0]
        assert row["day_pct_goal"] is None

    def test_pct_goal_computed_with_profile(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """With a profile set, p stores a positive day_pct_goal and renders it in the table."""
        # Set up profile: age=35, sex=m, weight=80 kg, height=178 cm, activity=3
        runner.invoke(input="5\n2\n35\nm\n80\n178\n3\nb\nq\n")
        self._setup_complete_meal(runner, monkeypatch)
        runner.invoke(input="3\nc\n\nb\nq\n")
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, "2025-03-15")[0]
        assert row["day_pct_goal"] is not None
        assert row["day_pct_goal"] > 0.0
        # Value shows in the table; title shows the goal in grams
        result = runner.invoke(input="3\nb\nq\n")
        assert f"{row['day_pct_goal']:.0f}%" in result.output
        assert "daily DCP goal" in result.output
        assert "grams" in result.output

    def test_pct_goal_shown_only_on_topmost_row(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """% goal appears exactly once per date — on the topmost row only."""
        runner.invoke(input="5\n2\n35\nm\n80\n178\n3\nb\nq\n")
        self._setup_complete_meal(runner, monkeypatch, name="Breakfast")
        runner.invoke(
            input="3\nn\n2025-03-15\nDinner\n1\nchicken\n1\n100 g\n\n\nd\n6\nb\nq\n"
        )
        runner.invoke(input="3\nc\n\nb\nq\n")
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, "2025-03-15")[0]
        pct_str = f"{row['day_pct_goal']:.0f}%"
        result = runner.invoke(input="3\nb\nq\n")
        assert result.output.count(pct_str) == 1

    def test_pct_goal_persists_across_sessions(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """day_pct_goal stored by p is visible in a later session without re-running p."""
        runner.invoke(input="5\n2\n35\nm\n80\n178\n3\nb\nq\n")
        self._setup_complete_meal(runner, monkeypatch)
        runner.invoke(input="3\nc\n\nb\nq\n")
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, "2025-03-15")[0]
        stored_pct = row["day_pct_goal"]
        assert stored_pct is not None
        result = runner.invoke(input="3\nb\nq\n")
        assert f"{stored_pct:.0f}%" in result.output

    def test_c_command_stores_calories_too(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """The c command computes and stores calories alongside DCP."""
        self._setup_complete_meal(runner, monkeypatch)
        result = runner.invoke(input="3\nc\n\nb\nq\n")
        assert result.exit_code == 0
        assert "Calories" in result.output
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, "2025-03-15")[0]
        assert row["calories"] is not None
        assert row["calories"] > 0.0

    def test_c_command_last_10_days_scope(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Choosing option 2 ('Last 10 days') still computes DCP/calories for a recent meal."""
        today = date.today().isoformat()
        _mock_api(monkeypatch)
        runner.invoke(
            input=f"3\nn\n{today}\nLunch\n1\nchicken\n1\n100 g\n\n\nd\n6\nb\nq\n"
        )
        # c=calculate → 3=last 10 days → b=back → q=quit
        result = runner.invoke(input="3\nc\n3\nb\nq\n")
        assert result.exit_code == 0
        with _db.get_db() as conn:
            row = _db.meal_list_by_date(conn, today)[0]
        assert row["bcp_g"] is not None
        assert row["calories"] is not None

    def test_analyzing_a_meal_saves_dcp_and_calories(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Viewing 'Analyze this meal' persists DCP + calories without running c."""
        self._setup_complete_meal(runner, monkeypatch)
        with _db.get_db() as conn:
            meal_id = _db.meal_list_by_date(conn, "2025-03-15")[0]["id"]
        # v{id}=view meal → 4=analyze this meal → Enter=skip AA refresh prompt → b=back → b=back → q=quit
        result = runner.invoke(input=f"3\nv{meal_id}\n4\nn\nb\nb\nq\n")
        assert result.exit_code == 0
        with _db.get_db() as conn:
            row = _db.meal_get(conn, meal_id)
        assert row["bcp_g"] is not None
        assert row["calories"] is not None


# ---------------------------------------------------------------------------
# Daily summary menu
# ---------------------------------------------------------------------------

class TestSummaryMenu:
    def test_enter_and_back(self, runner: NumaTestRunner):
        result = runner.invoke(input="4\nb\nq\n")
        assert result.exit_code == 0
        assert "Analysis" in result.output

    def test_today_summary_no_meals(self, runner: NumaTestRunner):
        result = runner.invoke(input="4\n1\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "No meals" in result.output

    def test_summary_for_date_shows_totals(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Log a meal on a known date
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        # View summary for that date; 'n' declines the RDA comparison shown when a profile exists
        result = runner.invoke(input="4\n1\n2\n2025-03-15\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "Calories" in result.output
        assert "Protein" in result.output

    def test_recent_days_shows_dates(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100\ny\n\nd\nb\nq\n")
        result = runner.invoke(input="4\n1\n3\nb\nq\n")
        assert result.exit_code == 0
        assert "2025-03-15" in result.output


# ---------------------------------------------------------------------------
# Settings menu
# ---------------------------------------------------------------------------

class TestSettingsMenu:
    def test_enter_and_back(self, runner: NumaTestRunner):
        result = runner.invoke(input="s\nb\nq\n")
        assert result.exit_code == 0
        assert "Settings" in result.output

    def test_set_api_key(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        config_file = tmp_path / "config.json"
        monkeypatch.setattr(_usda_api, "_CONFIG_FILE", config_file)
        # Settings: 8 (Advanced) → 2 (API key) → enter key → b (back from advanced) → b → q
        result = runner.invoke(input="5\n8\n2\nMYNEWKEY\nb\nb\nq\n")
        assert result.exit_code == 0
        assert "saved" in result.output.lower()
        assert config_file.exists()

    def test_change_theme(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        from numa_app.config import theme as _theme_mod
        theme_file = tmp_path / "theme"
        monkeypatch.setattr(_theme_mod, "_THEME_FILE", theme_file)
        # Settings: 1 (Theme) → pick 3 (neutral) → b → q
        result = runner.invoke(input="5\n1\n3\nb\nq\n")
        assert result.exit_code == 0
        assert "neutral" in result.output.lower()


# ---------------------------------------------------------------------------
# Dietary preferences (Settings menu → item 3)
# ---------------------------------------------------------------------------

class TestDietaryPrefs:
    def test_toggle_to_plant_based(self, runner: NumaTestRunner):
        # 5=Settings → 4=Dietary prefs → n (plant-based only) → b → q
        result = runner.invoke(input="5\n4\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "plant" in result.output.lower()

    def test_toggle_to_animal_included(self, runner: NumaTestRunner):
        # 5=Settings → 4=Dietary prefs → y (include animal foods) → b → q
        result = runner.invoke(input="5\n4\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "animal" in result.output.lower()

    def test_enter_keeps_current(self, runner: NumaTestRunner):
        # Empty Enter at the prompt keeps the current preference without error
        result = runner.invoke(input="5\n4\n\nb\nq\n")
        assert result.exit_code == 0

    def test_plant_only_shows_iron_zinc_bioavailability_note_on_goals_screen(
        self, runner: NumaTestRunner
    ):
        # Settings(5) → Dietary prefs(4) → 3=plant-based only → back(b)
        # → View goals(3) → back(b) → q
        result = runner.invoke(input="5\n4\n3\nb\n3\nb\nq\n")
        assert result.exit_code == 0
        assert "iron and zinc" in result.output.lower()
        assert "?diet-bioavailability" in result.output

    def test_all_animal_foods_shows_no_bioavailability_note(self, runner: NumaTestRunner):
        # Default diet_pref is "all" — the goals screen shouldn't mention it.
        result = runner.invoke(input="5\n3\nb\nq\n")
        assert result.exit_code == 0
        assert "iron and zinc" not in result.output.lower()


# ---------------------------------------------------------------------------
# _volume_hint
# ---------------------------------------------------------------------------

class TestVolumeHint:
    def test_cup_fraction_three_quarters(self):
        # 100g hemp seeds @ 0.57 g/ml = 175 ml = 0.74 cups → ¾ cup
        assert _volume_hint(100, "Seeds, hemp seed, hulled") == "≈ 3/4 cup"

    def test_cup_fraction_half(self):
        # 65g hemp seeds @ 0.57 g/ml = 114 ml = 0.48 cups → 1/2 cup
        assert _volume_hint(65, "Hemp seeds") == "≈ 1/2 cup"

    def test_cup_fraction_one_third(self):
        # 50g nutritional yeast @ 0.61 g/ml = 82.0 ml = 0.346 cups → 1/3 cup
        assert _volume_hint(50, "Nutritional yeast") == "≈ 1/3 cup"

    def test_cups_plural_over_one(self):
        # 200g quinoa @ 0.71 g/ml = 281.7 ml = 1.19 cups → 1 1/4 cups
        assert _volume_hint(200, "Quinoa, cooked") == "≈ 1 1/4 cups"

    def test_tablespoon_range(self):
        # 10g hemp seeds @ 0.57 g/ml = 17.5 ml ≈ 1.18 tbsp → rounds to 1 tbsp
        assert _volume_hint(10, "Hemp seeds") == "≈ 1 tbsp"

    def test_unknown_food_returns_none(self):
        assert _volume_hint(100, "mystery unrecognized food xyz") is None

    def test_sub_teaspoon_returns_none(self):
        # 1g hemp seeds @ 0.57 g/ml = 1.75 ml < 4.9 ml (1 tsp) — too small
        assert _volume_hint(1, "Hemp seeds") is None

    def test_eighth_cup(self):
        # 20g nutritional yeast @ 0.61 g/ml = 32.8 ml = 0.139 cups → 1/8 cup
        assert _volume_hint(20, "Nutritional yeast") == "≈ 1/8 cup"

    def test_tablespoon_below_cup_threshold(self):
        # 15g nutritional yeast @ 0.61 g/ml = 24.6 ml ≈ 1.5 tbsp — below cup threshold
        result = _volume_hint(15, "Nutritional yeast")
        assert result is not None
        assert "tbsp" in result


# ---------------------------------------------------------------------------
# User profile — Settings menu
# ---------------------------------------------------------------------------

class TestUserProfileSettings:
    def test_profile_option_visible_in_settings(self, runner: NumaTestRunner):
        """Settings menu must show a User profile option."""
        result = runner.invoke(input="5\nb\nq\n")
        assert result.exit_code == 0
        assert "profile" in result.output.lower()


# ---------------------------------------------------------------------------
# Optimal targets / max limits — Settings menu → Nutrient targets
# ---------------------------------------------------------------------------

class TestNutrientTargetsSettings:
    def test_nutrient_targets_option_visible_in_settings(self, runner: NumaTestRunner):
        result = runner.invoke(input="5\nb\nq\n")
        assert result.exit_code == 0
        assert "nutrient targets" in result.output.lower()

    def test_set_optimal_target_saves_to_profile(self, runner: NumaTestRunner):
        idx = nutrient_target_menu_index("vitamin_d_mcg")
        # Settings(5) → Nutrient targets(9) → Vitamin D → Optimal target(1) → 50 → back(b) → back(b) → q
        result = runner.invoke(input=f"5\n9\n{idx}\n1\n50\nb\nb\nq\n")
        assert result.exit_code == 0
        saved = _profile._PROFILES_DIR / "Default.json"
        data = json.loads(saved.read_text())
        assert data["optimal_targets"] == {"vitamin_d_mcg": 50.0}

    def test_set_max_limit_saves_to_profile(self, runner: NumaTestRunner):
        idx = nutrient_target_menu_index("sodium_mg")
        # Settings(5) → Nutrient targets(9) → Sodium → Max limit(2) → 2000 → back(b) → back(b) → q
        result = runner.invoke(input=f"5\n9\n{idx}\n2\n2000\nb\nb\nq\n")
        assert result.exit_code == 0
        saved = _profile._PROFILES_DIR / "Default.json"
        data = json.loads(saved.read_text())
        assert data["max_limits"] == {"sodium_mg": 2000.0}

    def test_clear_optimal_target(self, runner: NumaTestRunner):
        idx = nutrient_target_menu_index("vitamin_d_mcg")
        runner.invoke(input=f"5\n9\n{idx}\n1\n50\nb\nb\nq\n")
        result = runner.invoke(input=f"5\n9\n{idx}\n3\nb\nb\nq\n")
        assert result.exit_code == 0
        saved = _profile._PROFILES_DIR / "Default.json"
        data = json.loads(saved.read_text())
        assert data["optimal_targets"] == {}

    def test_no_profile_shows_message(self, runner: NumaTestRunner):
        for f in _profile._PROFILES_DIR.glob("*.json"):
            f.unlink()
        result = runner.invoke(input="5\n9\nb\nq\n")
        assert result.exit_code == 0
        assert "no profile set" in result.output.lower()

    def test_load_recommended_optimal_defaults(self, runner: NumaTestRunner):
        # Settings(5) → Nutrient targets(9) → l=load defaults → back(b) → q
        result = runner.invoke(input="5\n9\nl\nb\nq\n")
        assert result.exit_code == 0
        assert "loaded recommended optimal targets" in result.output.lower()
        saved = _profile._PROFILES_DIR / "Default.json"
        data = json.loads(saved.read_text())
        assert data["optimal_targets"] == {
            "vitamin_d_mcg": 50.0,
            "omega3_epa_mg": 250.0,
            "omega3_dha_mg": 250.0,
        }

    def test_load_recommended_optimal_defaults_skips_customized(self, runner: NumaTestRunner):
        idx = nutrient_target_menu_index("vitamin_d_mcg")
        # Set a custom Vitamin D target first, then load defaults — it must survive untouched.
        result = runner.invoke(input=f"5\n9\n{idx}\n1\n99\nl\nb\nq\n")
        assert result.exit_code == 0
        saved = _profile._PROFILES_DIR / "Default.json"
        data = json.loads(saved.read_text())
        assert data["optimal_targets"]["vitamin_d_mcg"] == 99.0
        assert data["optimal_targets"]["omega3_epa_mg"] == 250.0

    def test_set_profile_saves_file(self, runner: NumaTestRunner):
        """Walking through the profile form saves a JSON file."""
        # Settings: 2 (Manage profiles) → e (edit active) → age=35 → sex=m →
        # weight=80 → height=178 → activity=3 (moderate) → b → b → q
        result = runner.invoke(input="5\n2\n35\nm\n80\n178\n3\nb\nq\n")
        assert result.exit_code == 0
        saved = _profile._PROFILES_DIR / "Default.json"
        assert saved.exists()
        data = json.loads(saved.read_text())
        assert data["age"] == 35
        assert data["sex"] == "male"

    def test_set_profile_shows_calorie_target(self, runner: NumaTestRunner):
        """After saving, the response shows the estimated calorie target."""
        # Settings(5) → Manage profiles(2) → edit #1(e1) → age/sex/weight/height/activity → back → quit
        result = runner.invoke(input="5\n2\ne1\n35\nm\n80\n178\n3\nb\nq\n")
        assert result.exit_code == 0
        assert "kcal" in result.output.lower() or "calorie" in result.output.lower()

    def test_invalid_age_reprompts(self, runner: NumaTestRunner):
        """Non-numeric age input triggers re-prompt before accepting a valid entry."""
        # Settings(5) → Manage profiles(2) → edit #1(e1) → bad age → valid age → ... → back → quit
        result = runner.invoke(input="5\n2\ne1\nnotanage\n35\nm\n80\n178\n3\nb\nq\n")
        assert result.exit_code == 0
        saved = _profile._PROFILES_DIR / "Default.json"
        assert saved.exists()
        assert json.loads(saved.read_text())["age"] == 35

    def test_profile_status_shows_not_set(self, runner: NumaTestRunner):
        """Settings menu shows 'not set' when no profile exists."""
        # Remove the Default profile the autouse fixture created.
        for f in _profile._PROFILES_DIR.glob("*.json"):
            f.unlink()
        result = runner.invoke(input="5\nb\nq\n")
        assert result.exit_code == 0
        assert "not set" in result.output.lower()

    def test_profile_status_shows_details_when_set(self, runner: NumaTestRunner):
        """After setting a profile, Settings menu shows age/sex/weight in status line."""
        # Settings(5) → Manage profiles(2) → edit #1(e1) → age=40,sex=f,weight,height,activity → back → quit
        runner.invoke(input="5\n2\ne1\n40\nf\n62\n165\n2\nb\nq\n")
        # Now open settings again — status line should show updated details
        result = runner.invoke(input="5\nb\nq\n")
        assert result.exit_code == 0
        assert "40" in result.output   # age
        assert "female" in result.output


# ---------------------------------------------------------------------------
# Daily summary — RDA comparison
# ---------------------------------------------------------------------------

class TestDailySummaryRDA:
    def test_no_profile_shows_tip(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Without a profile, daily summary shows a tip to set one up."""
        _mock_api(monkeypatch)
        # Remove the Default profile so there's truly no profile.
        for f in _profile._PROFILES_DIR.glob("*.json"):
            f.unlink()
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100\ny\n\nd\nb\nq\n")
        result = runner.invoke(input="4\n1\n2\n2025-03-15\nb\nq\n")
        assert result.exit_code == 0
        assert "profile" in result.output.lower()

    def test_with_profile_offers_rda_comparison(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """With a profile set, daily summary prompts to compare against RDA."""
        _mock_api(monkeypatch)
        # Log a meal
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        # View summary: decline complement → accept RDA comparison
        result = runner.invoke(input="4\n1\n2\n2025-03-15\nn\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "rda" in result.output.lower() or "recommended" in result.output.lower()

    def test_rda_comparison_shows_protein(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """RDA comparison table includes Protein row."""
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="4\n1\n2\n2025-03-15\nn\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output

    def test_rda_comparison_shows_optimal_and_max_limit_help(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """With an Optimal target and a custom max limit configured, the RDA
        comparison table's help footers mention both topics."""
        _mock_api(monkeypatch)
        idx = nutrient_target_menu_index("sodium_mg")
        # Settings(5) → Nutrient targets(9) → Sodium → Max limit(2) → 50 → back(b) → quit
        runner.invoke(input=f"5\n9\n{idx}\n2\n50\nb\nq\n")
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="4\n1\n2\n2025-03-15\nn\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "?maxlimits" in result.output

    def test_rda_comparison_shows_max_limit_help_from_built_in_uls_alone(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """Built-in safe upper limits (iron, zinc, vitamin A, B6, iodine,
        selenium) apply automatically even when the user hasn't configured any
        max limit themselves, so the help footer still appears."""
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="4\n1\n2\n2025-03-15\nn\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "?maxlimits" in result.output

    def test_rda_comparison_decline_skips_table(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """Declining the RDA comparison prompt does not print the table."""
        _mock_api(monkeypatch)
        runner.invoke(input="3\nn\n2025-03-15\nLunch\n1\nchicken\n1\n100\ny\n\nd\nb\nq\n")
        result = runner.invoke(input="4\n1\n2\n2025-03-15\nn\nn\nb\nq\n")
        assert result.exit_code == 0
        # Table header should not appear
        assert "% of RDA" not in result.output


class TestNutrientTrend:
    def test_no_profile_shows_message(self, runner: NumaTestRunner):
        for f in _profile._PROFILES_DIR.glob("*.json"):
            f.unlink()
        # Analysis(4) → Daily summary(1) → N-day trend(4) → back(b) → q
        result = runner.invoke(input="4\n1\n4\nb\nq\n")
        assert result.exit_code == 0
        assert "no profile set" in result.output.lower()

    def test_no_meals_in_window_shows_message(self, runner: NumaTestRunner):
        # Analysis(4) → Daily summary(1) → N-day trend(4) → 1=last 7 days → back(b) → q
        result = runner.invoke(input="4\n1\n4\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "no meals logged between" in result.output.lower()

    def test_averages_across_logged_days(self, runner: NumaTestRunner, monkeypatch, cached_food):
        """Logging the same food on today and yesterday shows a 2-day average,
        not a 7-day average diluted by unlogged days."""
        _mock_api(monkeypatch)
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        for d in (today, yesterday):
            runner.invoke(input=f"3\nn\n{d}\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")

        result = runner.invoke(input="4\n1\n4\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "averaging over 2 logged day(s) out of the last 7" in result.output.lower()
        assert "2-day average" in result.output.lower()
        assert "Protein" in result.output

    def test_complete_protein_shows_no_complement_suggestions(
        self, runner: NumaTestRunner, monkeypatch, cached_food
    ):
        """Chicken breast (SAMPLE_NUTRIENTS) has no amino acid gaps, so the
        pooled multi-day complement section stays silent (silent_if_complete)."""
        _mock_api(monkeypatch)
        today = date.today().isoformat()
        runner.invoke(input=f"3\nn\n{today}\nLunch\n1\nchicken\n1\n100 g\n\nd\nb\nq\n")
        result = runner.invoke(input="4\n1\n4\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein Complement Suggestions" not in result.output

    def test_pooled_gap_across_days_shows_complement_suggestions(
        self, runner: NumaTestRunner, db_conn
    ):
        """A lysine gap that shows up across multiple logged days (not just
        one) is pooled and surfaced with forward-looking 'upcoming meals'
        framing, not the single-day 'add to your day' framing."""
        low_lysine = dict(SAMPLE_NUTRIENTS)
        low_lysine["aa_lysine_g"] = 0.6  # push below the FAO reference to create a real gap
        fdc_id = 900001
        db_conn.execute(
            "INSERT OR REPLACE INTO foods (fdc_id, name, data_type, nutrients_json) VALUES (?, ?, ?, ?)",
            (fdc_id, "Low-lysine test food", "SR Legacy", json.dumps(low_lysine)),
        )
        db_conn.commit()

        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        with _db.get_db() as conn:
            for d in (today, yesterday):
                meal_id = _db.meal_create(conn, "Lunch", d)
                _db.meal_add_food(conn, meal_id, fdc_id, "Low-lysine test food", 150.0, "g")

        result = runner.invoke(input="4\n1\n4\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein Complement Suggestions" in result.output
        assert "pooled across 2 logged day(s)" in result.output
        assert "Add to upcoming meals" in result.output


# ---------------------------------------------------------------------------
# Food use in meals analysis
# ---------------------------------------------------------------------------

class TestFoodUseAnalysis:
    def _seed(self, db_conn, cached_food):
        """Second cached food + a 2-ingredient recipe logged into two meals on two dates."""
        second_fdc_id = 999999
        db_conn.execute("""
            INSERT INTO foods (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (second_fdc_id, "Brown rice, cooked", "SR Legacy", None, 100.0, "g",
              json.dumps(SAMPLE_NUTRIENTS_2), json.dumps([])))
        db_conn.commit()

        with _db.get_db() as conn:
            recipe_id = _db.recipe_create(conn, "Chicken and Rice", "", 2, "")
            _db.recipe_add_ingredient(conn, recipe_id, cached_food["fdcId"], cached_food["name"], 150.0, "g")
            _db.recipe_add_ingredient(conn, recipe_id, second_fdc_id, "Brown rice, cooked", 200.0, "g")

            meal1 = _db.meal_create(conn, "Lunch", "2026-01-01")
            _db.meal_add_food(conn, meal1, cached_food["fdcId"], cached_food["name"], 100.0, "g")

            meal2 = _db.meal_create(conn, "Dinner", "2026-01-02")
            _db.meal_add_recipe(conn, meal2, recipe_id, "Chicken and Rice", 1.0, "servings")

        return meal1, meal2

    def test_meal_ids_ranks_and_expands_recipe(self, runner: NumaTestRunner, db_conn, cached_food):
        meal1, meal2 = self._seed(db_conn, cached_food)

        # Analysis(4) -> Food use in meals(2) -> select by Meal IDs(2) -> both IDs -> All foods(1) -> quit
        result = runner.invoke(input=f"4\n2\n2\n{meal1} {meal2}\n1\nq\n")
        assert result.exit_code == 0
        assert "Food Use in Meals" in result.output
        # Chicken appears standalone (meal1) and expanded from the recipe (meal2).
        # The table column truncates long names, so match a safe prefix.
        chicken_prefix = cached_food["name"][:20]
        assert chicken_prefix in result.output
        # Recipe row and its expanded rice ingredient both appear
        assert "Chicken and Rice" in result.output
        assert "Brown rice, cooked" in result.output
        # Chicken (2 days) ranks above the recipe / rice (1 day each)
        chicken_pos = result.output.index(chicken_prefix)
        rice_pos = result.output.index("Brown rice, cooked")
        assert chicken_pos < rice_pos

    def test_date_range_covers_both_meals(self, runner: NumaTestRunner, db_conn, cached_food):
        meal1, meal2 = self._seed(db_conn, cached_food)

        # Analysis(4) -> Food use in meals(2) -> select by Date range(s)(1) -> one range covering both dates -> All foods(1) -> quit
        result = runner.invoke(input="4\n2\n1\n2026-01-01\n2026-01-02\nn\n1\nq\n")
        assert result.exit_code == 0
        assert "2 meal(s) across 2 distinct day(s)" in result.output
        assert cached_food["name"][:20] in result.output
        assert "Chicken and Rice" in result.output

    def test_no_selection_shows_message(self, runner: NumaTestRunner):
        # Select by Meal IDs(2), leave the ID field blank
        result = runner.invoke(input="4\n2\n2\n\nq\n")
        assert result.exit_code == 0
        assert "nothing to analyze" in result.output.lower()

    def test_protein_only_filter_excludes_zero_protein_food(self, runner: NumaTestRunner, db_conn, cached_food):
        # A zero-protein food logged standalone on a separate date
        zero_protein_nutrients = dict(SAMPLE_NUTRIENTS_2)
        zero_protein_nutrients["protein_g"] = 0.0
        db_conn.execute("""
            INSERT INTO foods (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (777777, "Olive oil", "SR Legacy", None, 100.0, "g",
              json.dumps(zero_protein_nutrients), json.dumps([])))
        db_conn.commit()

        with _db.get_db() as conn:
            meal1 = _db.meal_create(conn, "Lunch", "2026-02-01")
            _db.meal_add_food(conn, meal1, cached_food["fdcId"], cached_food["name"], 100.0, "g")

            meal2 = _db.meal_create(conn, "Dinner", "2026-02-02")
            _db.meal_add_food(conn, meal2, 777777, "Olive oil", 15.0, "g")

        # Select by Meal IDs(2) -> both -> Only protein-containing foods(2) -> quit
        result = runner.invoke(input=f"4\n2\n2\n{meal1} {meal2}\n2\nq\n")
        assert result.exit_code == 0
        assert "protein-containing foods only" in result.output
        assert cached_food["name"][:20] in result.output
        assert "Olive oil" not in result.output
