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
    Main menu choices: 1=Foods, 2=Recipes, 3=Meals, 4=Summary, d=Dietary prefs,
                       s=Settings, q=Quit
    Foods submenu:     1=Search, 2=Analyze USDA portion, 3=Analyze recipe portion,
                       4=Convert, 5=View cached, 6=Pantry, b=Back, q=Quit
    Recipes submenu:   1=Create, 2=List, 3=View/analyze, 4=Edit, 5=Delete, b=Back
    Settings submenu:  1=API key, 2=Theme, 3=DB path, 4=DIAAS overrides,
                       5=Dietary prefs, 6=User profile, b=Back
"""

import json
import subprocess
import sys
from unittest.mock import patch

import pytest

import db as _db
import profile as _profile
import usda as _usda
from numa_app.services.portions import _parse_portion_input
from numa_app.ui.render import _volume_hint
from tests.conftest import (
    SAMPLE_FDC_ID,
    SAMPLE_FOOD_DETAIL,
    SAMPLE_NUTRIENTS,
    SAMPLE_SEARCH_RESULTS,
    NumaTestRunner,
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
    def test_plain_number_is_grams(self):
        grams, label = _parse_portion_input("150", [])
        assert grams == pytest.approx(150.0)
        assert "150" in label

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

    def test_plain_fraction_is_grams(self):
        grams, label = _parse_portion_input("1/4", [])
        assert grams == pytest.approx(0.25)

    def test_mixed_number_is_grams(self):
        grams, label = _parse_portion_input("1 1/2", [])
        assert grams == pytest.approx(1.5)

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
        monkeypatch.setattr(_usda, "_CONFIG_FILE", config_file)
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
        # Main: 1 → Foods: 1 (Search) → query: "chicken" → pick: 1 → Foods: b → Main: q
        result = runner.invoke(input="1\n1\nchicken\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "Chicken" in result.output

    def test_search_shows_nutrient_table(self, runner: NumaTestRunner, monkeypatch):
        _mock_api(monkeypatch)
        result = runner.invoke(input="1\n1\nchicken\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output
        assert "Calories" in result.output

    def test_analyze_portion_scales_nutrients(self, runner: NumaTestRunner, monkeypatch):
        _mock_api(monkeypatch)
        # pick food, enter 200g portion (double the 100g base)
        result = runner.invoke(input="1\n2\nchicken\n1\n200\nb\nq\n")
        assert result.exit_code == 0
        # 31g protein * 2 = 62g
        assert "62" in result.output

    def test_empty_search_query_returns_to_menu(self, runner: NumaTestRunner, monkeypatch):
        _mock_api(monkeypatch)
        # Empty query → no search → back → quit
        result = runner.invoke(input="1\n1\n\nb\nq\n")
        assert result.exit_code == 0

    def test_list_cached_foods_empty(self, runner: NumaTestRunner):
        # Foods item 5 = View cached (was item 4 before new item 3 was added)
        result = runner.invoke(input="1\n5\nb\nq\n")
        assert result.exit_code == 0
        assert "cached" in result.output.lower() or "No foods" in result.output

    def test_list_cached_foods_shows_entry(self, runner: NumaTestRunner, cached_food):
        result = runner.invoke(input="1\n5\nb\nq\n")
        assert result.exit_code == 0
        assert "Chicken" in result.output

    def test_search_offers_portion_analysis_accept(self, runner: NumaTestRunner, monkeypatch):
        """After viewing per-100g nutrients, pressing y leads to scaled portion output."""
        _mock_api(monkeypatch)
        # Foods: 1 (Search) → chicken → pick 1 → y → 200g → back → quit
        result = runner.invoke(input="1\n1\nchicken\n1\ny\n200\nb\nq\n")
        assert result.exit_code == 0
        assert "62" in result.output   # 31g protein × 2

    def test_search_offers_portion_analysis_decline(self, runner: NumaTestRunner, monkeypatch):
        """Pressing n at the portion offer returns to the foods menu without scaling."""
        _mock_api(monkeypatch)
        result = runner.invoke(input="1\n1\nchicken\n1\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output
        assert "62" not in result.output   # no 200g scaled result

    def test_invalid_portion_input_retries(self, runner: NumaTestRunner, monkeypatch):
        """Bad portion input shows an error and re-prompts rather than dropping to the menu."""
        _mock_api(monkeypatch)
        # Foods: 2 (Analyze) → bad input → valid 200g → scaled nutrients shown
        result = runner.invoke(input="1\n2\nchicken\n1\nbadstuff\n200\nb\nq\n")
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
        runner.invoke(input="2\n1\nChicken Dish\n\n2\nd\nchicken\n1\n200\nn\nb\nq\n")

        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]

        # Foods → 3 → recipe id → 1 serving → back → quit
        result = runner.invoke(input=f"1\n3\n{rid}\n1\nb\nq\n")
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
        # Recipes: 1 (Create) → name → description → servings → instructions (d=skip) →
        # add ingredient: search "chicken" → pick 1 → amount 150 →
        # add another? n → b → q
        inp = "2\n1\nChicken Salad\nA fresh salad\n2\nd\nchicken\n1\n150\nn\nb\nq\n"
        result = runner.invoke(input=inp)
        assert result.exit_code == 0
        assert "saved" in result.output.lower() or "created" in result.output.lower()

        with _db.get_db() as conn:
            recipes = _db.recipe_list(conn)
        assert len(recipes) == 1
        assert recipes[0]["name"] == "Chicken Salad"

    def test_create_recipe_saves_ingredients(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        inp = "2\n1\nMy Recipe\n\n1\nd\nchicken\n1\n100\nn\nb\nq\n"
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
        runner.invoke(input="2\n1\nSoup\n\n1\nd\nchicken\n1\n100\nn\nb\nq\n")
        # List recipes
        result = runner.invoke(input="2\n2\nb\nq\n")
        assert "Soup" in result.output

    def test_delete_recipe(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Create
        runner.invoke(input="2\n1\nDeleteMe\n\n1\nd\nchicken\n1\n100\nn\nb\nq\n")

        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]

        # Delete (Recipes: 5 → show list → enter id → confirm y)
        result = runner.invoke(input=f"2\n5\n{rid}\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "Deleted" in result.output

        with _db.get_db() as conn:
            assert _db.recipe_list(conn) == []

    def test_view_recipe_shows_nutrients(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="2\n1\nChicken Dish\n\n2\nd\nchicken\n1\n200\nn\nb\nq\n")

        with _db.get_db() as conn:
            rid = _db.recipe_list(conn)[0]["id"]

        # n=skip protein analysis; export is mocked to no-op
        result = runner.invoke(input=f"2\n3\n{rid}\nn\nb\nq\n")
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
        # Meals: 1 (Log) → date → name → add item: 1 (food) → search → pick → amount → done: d
        inp = "3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n150\nd\nb\nq\n"
        result = runner.invoke(input=inp)
        assert result.exit_code == 0
        assert "logged" in result.output.lower() or "Meal" in result.output

        with _db.get_db() as conn:
            meals = _db.meal_list_by_date(conn, "2025-03-15")
        assert len(meals) == 1
        assert meals[0]["name"] == "Lunch"

    def test_log_meal_saves_food_item(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        inp = "3\n1\n2025-03-15\nDinner\n1\nchicken\n1\n200\nd\nb\nq\n"
        runner.invoke(input=inp)

        with _db.get_db() as conn:
            meals = _db.meal_list_by_date(conn, "2025-03-15")
            items = _db.meal_get_items(conn, meals[0]["id"])
        assert len(items) == 1
        assert items[0]["amount"] == 200.0

    def test_view_meals_empty_date(self, runner: NumaTestRunner):
        result = runner.invoke(input="3\n2\n2025-01-01\nb\nq\n")
        assert result.exit_code == 0
        assert "No meals" in result.output

    def test_view_meals_shows_entry(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\n1\n2025-03-15\nBreakfast\n1\nchicken\n1\n100\nd\nb\nq\n")
        # Extra b: one for the view action loop, one for the meals submenu
        result = runner.invoke(input="3\n2\n2025-03-15\nb\nb\nq\n")
        assert "Breakfast" in result.output

    def test_view_meals_shows_food_items(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n150\nd\nb\nq\n")
        result = runner.invoke(input="3\n2\n2025-03-15\nb\nb\nq\n")
        assert result.exit_code == 0
        assert "Chicken" in result.output
        assert "150" in result.output

    def test_view_meals_delete_item(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n200\nd\nb\nq\n")

        with _db.get_db() as conn:
            mid = _db.meal_list_by_date(conn, "2025-03-15")[0]["id"]
            iid = _db.meal_get_items(conn, mid)[0]["id"]

        # View → d → meal id → item id → b (action loop) → b (meals menu) → q
        result = runner.invoke(input=f"3\n2\n2025-03-15\nd\n{mid}\n{iid}\nb\nb\nq\n")
        assert result.exit_code == 0
        assert "removed" in result.output.lower()

        with _db.get_db() as conn:
            assert _db.meal_get_items(conn, mid) == []

    def test_analyze_meal_shows_nutrients(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")

        result = runner.invoke(input="3\n3\n2025-03-15\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output

    def test_delete_meal(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")

        with _db.get_db() as conn:
            mid = _db.meal_list_by_date(conn, "2025-03-15")[0]["id"]

        result = runner.invoke(input=f"3\n4\n2025-03-15\n{mid}\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "Deleted" in result.output

        with _db.get_db() as conn:
            assert _db.meal_list_by_date(conn, "2025-03-15") == []


# ---------------------------------------------------------------------------
# Daily summary menu
# ---------------------------------------------------------------------------

class TestSummaryMenu:
    def test_enter_and_back(self, runner: NumaTestRunner):
        result = runner.invoke(input="4\nb\nq\n")
        assert result.exit_code == 0
        assert "Summary" in result.output

    def test_today_summary_no_meals(self, runner: NumaTestRunner):
        result = runner.invoke(input="4\n1\nb\nq\n")
        assert result.exit_code == 0
        assert "No meals" in result.output

    def test_summary_for_date_shows_totals(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        # Log a meal on a known date
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")
        # View summary for that date
        result = runner.invoke(input="4\n2\n2025-03-15\nb\nq\n")
        assert result.exit_code == 0
        assert "Calories" in result.output
        assert "Protein" in result.output

    def test_recent_days_shows_dates(self, runner: NumaTestRunner, monkeypatch, cached_food):
        _mock_api(monkeypatch)
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")
        result = runner.invoke(input="4\n3\nb\nq\n")
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
        monkeypatch.setattr(_usda, "_CONFIG_FILE", config_file)
        # Settings: 1 (API key) → enter key → b → q
        result = runner.invoke(input="s\n1\nMYNEWKEY\nb\nq\n")
        assert result.exit_code == 0
        assert "saved" in result.output.lower()
        assert config_file.exists()

    def test_change_theme(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        from numa_app.config import theme as _theme_mod
        theme_file = tmp_path / "theme"
        monkeypatch.setattr(_theme_mod, "_THEME_FILE", theme_file)
        # Settings: 2 (Theme) → pick 3 (neutral) → b → q
        result = runner.invoke(input="s\n2\n3\nb\nq\n")
        assert result.exit_code == 0
        assert "neutral" in result.output.lower()


# ---------------------------------------------------------------------------
# Dietary preferences (main menu 'd')
# ---------------------------------------------------------------------------

class TestDietaryPrefs:
    def test_toggle_to_plant_based(self, runner: NumaTestRunner):
        # d = dietary prefs → n (plant-based only) → q
        result = runner.invoke(input="d\nn\nq\n")
        assert result.exit_code == 0
        assert "plant" in result.output.lower()

    def test_toggle_to_animal_included(self, runner: NumaTestRunner):
        # d = dietary prefs → y (include animal foods) → q
        result = runner.invoke(input="d\ny\nq\n")
        assert result.exit_code == 0
        assert "animal" in result.output.lower()

    def test_enter_keeps_current(self, runner: NumaTestRunner):
        # Empty Enter at the prompt keeps the current preference without error
        result = runner.invoke(input="d\n\nq\n")
        assert result.exit_code == 0


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
        result = runner.invoke(input="s\nb\nq\n")
        assert result.exit_code == 0
        assert "profile" in result.output.lower()

    def test_set_profile_saves_file(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        """Walking through the profile form saves a JSON file."""
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        # Settings: 6 (User profile) → age=35 → sex=m → weight=80 → height=178 →
        # activity=3 (moderate) → b → q
        result = runner.invoke(input="s\n6\n35\nm\n80\n178\n3\nb\nq\n")
        assert result.exit_code == 0
        assert pf.exists()
        data = json.loads(pf.read_text())
        assert data["age"] == 35
        assert data["sex"] == "male"

    def test_set_profile_shows_calorie_target(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        """After saving, the response shows the estimated calorie target."""
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        result = runner.invoke(input="s\n6\n35\nm\n80\n178\n3\nb\nq\n")
        assert result.exit_code == 0
        assert "kcal" in result.output.lower() or "calorie" in result.output.lower()

    def test_invalid_age_reprompts(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        """Non-numeric age input triggers re-prompt before accepting a valid entry."""
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        # bad age → valid age → sex → weight → height → activity → back → quit
        result = runner.invoke(input="s\n6\nnotanage\n35\nm\n80\n178\n3\nb\nq\n")
        assert result.exit_code == 0
        assert pf.exists()
        assert json.loads(pf.read_text())["age"] == 35

    def test_profile_status_shows_not_set(self, runner: NumaTestRunner, tmp_path, monkeypatch):
        """Settings menu shows 'not set' when no profile exists."""
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        result = runner.invoke(input="s\nb\nq\n")
        assert result.exit_code == 0
        assert "not set" in result.output.lower()

    def test_profile_status_shows_details_when_set(
        self, runner: NumaTestRunner, tmp_path, monkeypatch
    ):
        """After setting a profile, Settings menu shows age/sex/weight in status line."""
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        # Set profile first
        runner.invoke(input="s\n6\n40\nf\n62\n165\n2\nb\nq\n")
        # Now open settings again — status line should show details
        result = runner.invoke(input="s\nb\nq\n")
        assert result.exit_code == 0
        assert "40" in result.output   # age
        assert "female" in result.output


# ---------------------------------------------------------------------------
# Daily summary — RDA comparison
# ---------------------------------------------------------------------------

class TestDailySummaryRDA:
    def test_no_profile_shows_tip(self, runner: NumaTestRunner, monkeypatch, cached_food, tmp_path):
        """Without a profile, daily summary shows a tip to set one up."""
        _mock_api(monkeypatch)
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")
        result = runner.invoke(input="4\n2\n2025-03-15\nn\nb\nq\n")
        assert result.exit_code == 0
        assert "profile" in result.output.lower()

    def test_with_profile_offers_rda_comparison(
        self, runner: NumaTestRunner, monkeypatch, cached_food, tmp_path
    ):
        """With a profile set, daily summary prompts to compare against RDA."""
        _mock_api(monkeypatch)
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        # Set profile
        runner.invoke(input="s\n6\n35\nm\n80\n178\n3\nb\nq\n")
        # Log a meal
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")
        # View summary: decline complement → accept RDA comparison
        result = runner.invoke(input="4\n2\n2025-03-15\nn\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "rda" in result.output.lower() or "recommended" in result.output.lower()

    def test_rda_comparison_shows_protein(
        self, runner: NumaTestRunner, monkeypatch, cached_food, tmp_path
    ):
        """RDA comparison table includes Protein row."""
        _mock_api(monkeypatch)
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        runner.invoke(input="s\n6\n35\nm\n80\n178\n3\nb\nq\n")
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")
        result = runner.invoke(input="4\n2\n2025-03-15\nn\ny\nb\nq\n")
        assert result.exit_code == 0
        assert "Protein" in result.output

    def test_rda_comparison_decline_skips_table(
        self, runner: NumaTestRunner, monkeypatch, cached_food, tmp_path
    ):
        """Declining the RDA comparison prompt does not print the table."""
        _mock_api(monkeypatch)
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        runner.invoke(input="s\n6\n35\nm\n80\n178\n3\nb\nq\n")
        runner.invoke(input="3\n1\n2025-03-15\nLunch\n1\nchicken\n1\n100\nd\nb\nq\n")
        result = runner.invoke(input="4\n2\n2025-03-15\nn\nn\nb\nq\n")
        assert result.exit_code == 0
        # Table header should not appear
        assert "% of RDA" not in result.output
