"""
Tests for numa_app/services/recipe_csv.py — recipe CSV export/import,
including sub-recipe closure collection and the two-pass dedup-and-create
import.
"""
import db as _db
from numa_app.services.recipe_csv import (
    collect_recipe_bundle,
    import_recipe_bundle,
    parse_recipes_csv,
    render_recipe_export,
)
from numa_app.services.csv_import import parse_foods_csv


def _make_food(conn, fdc_id: int, name: str, protein_g: float = 5.0) -> None:
    _db.cache_food(conn, fdc_id, name, "Foundation", None, None, None,
                    {"calories": 100.0, "protein_g": protein_g}, [])


class TestCollectAndExport:
    def test_simple_recipe_bundle_includes_its_foods(self) -> None:
        with _db.get_db() as conn:
            _make_food(conn, 1, "Flour")
            rid = _db.recipe_create(conn, "Bread", "", 4, "Mix and bake.")
            _db.recipe_add_ingredient(conn, rid, 1, "Flour", 200.0, "200 g")

            recipes, food_rows = collect_recipe_bundle(conn, [rid])
        assert len(recipes) == 1
        assert recipes[0]["row"]["name"] == "Bread"
        assert len(food_rows) == 1
        assert food_rows[0]["name"] == "Flour"

    def test_bundle_includes_transitive_subrecipes(self) -> None:
        with _db.get_db() as conn:
            _make_food(conn, 1, "Quinoa")
            sub_id = _db.recipe_create(conn, "Cooked Quinoa", "", 2, "Boil it.")
            _db.recipe_add_ingredient(conn, sub_id, 1, "Quinoa", 100.0, "100 g")

            main_id = _db.recipe_create(conn, "Quinoa Bowl", "", 1, "Combine.")
            _db.recipe_add_ingredient(conn, main_id, 0, "Cooked Quinoa", 1.0,
                                      "1 serving", ref_recipe_id=sub_id)

            recipes, food_rows = collect_recipe_bundle(conn, [main_id])
        names = {r["row"]["name"] for r in recipes}
        assert names == {"Quinoa Bowl", "Cooked Quinoa"}
        assert [f["name"] for f in food_rows] == ["Quinoa"]

    def test_render_recipe_export_round_trips_through_parsers(self) -> None:
        with _db.get_db() as conn:
            _make_food(conn, 1, "Quinoa")
            sub_id = _db.recipe_create(conn, "Cooked Quinoa", "", 2, "Boil it.")
            _db.recipe_add_ingredient(conn, sub_id, 1, "Quinoa", 100.0, "100 g")
            main_id = _db.recipe_create(conn, "Quinoa Bowl", "desc", 1, "Combine.")
            _db.recipe_add_ingredient(conn, main_id, 0, "Cooked Quinoa", 1.0,
                                      "1 serving", ref_recipe_id=sub_id)

            recipes_text, foods_text = render_recipe_export(conn, [main_id])

        recipes, r_warnings = parse_recipes_csv(recipes_text)
        foods, f_warnings = parse_foods_csv(foods_text)
        assert not r_warnings
        assert not f_warnings
        assert {r["name"] for r in recipes} == {"Quinoa Bowl", "Cooked Quinoa"}
        assert {f["name"] for f in foods} == {"Quinoa"}


class TestImportRecipeBundle:
    def test_imports_recipe_with_subrecipe_and_food_from_scratch(self) -> None:
        recipes = [
            {
                "name": "Cooked Quinoa", "description": "", "servings": 2.0,
                "total_weight": None, "total_weight_unit": None, "instructions": "Boil it.",
                "ingredients": [
                    {"food_name": "Quinoa", "amount": 100.0, "unit": "100 g",
                     "notes": None, "is_subrecipe": False},
                ],
            },
            {
                "name": "Quinoa Bowl", "description": "", "servings": 1.0,
                "total_weight": None, "total_weight_unit": None, "instructions": "Combine.",
                "ingredients": [
                    {"food_name": "Cooked Quinoa", "amount": 1.0, "unit": "1 serving",
                     "notes": None, "is_subrecipe": True},
                ],
            },
        ]
        food_valid = [{
            "name": "Quinoa", "data_type": "Foundation", "brand": None,
            "serving_size": None, "serving_unit": None, "notes": None,
            "portions": [], "nutrients": {"calories": 100.0, "protein_g": 5.0},
        }]

        with _db.get_db() as conn:
            result = import_recipe_bundle(conn, recipes, food_valid)
            assert result["recipes_created"] == 2
            assert result["recipes_reused"] == 0
            assert result["foods_created"] == 1
            assert result["warnings"] == []

            all_recipes = {r["name"]: r["id"] for r in _db.recipe_list(conn)}
        assert set(all_recipes) == {"Cooked Quinoa", "Quinoa Bowl"}

        with _db.get_db() as conn:
            bowl_ings = _db.recipe_get_ingredients(conn, all_recipes["Quinoa Bowl"])
            quinoa_ings = _db.recipe_get_ingredients(conn, all_recipes["Cooked Quinoa"])
        assert bowl_ings[0]["ref_recipe_id"] == all_recipes["Cooked Quinoa"]
        assert quinoa_ings[0]["food_name"] == "Quinoa"

    def test_existing_recipe_name_is_reused_not_duplicated(self) -> None:
        with _db.get_db() as conn:
            existing_id = _db.recipe_create(conn, "Cooked Quinoa", "mine", 3, "already here")

        recipes = [{
            "name": "Cooked Quinoa", "description": "imported version", "servings": 2.0,
            "total_weight": None, "total_weight_unit": None, "instructions": "Boil it.",
            "ingredients": [
                {"food_name": "Quinoa", "amount": 100.0, "unit": "100 g",
                 "notes": None, "is_subrecipe": False},
            ],
        }]
        food_valid = [{
            "name": "Quinoa", "data_type": "Foundation", "brand": None,
            "serving_size": None, "serving_unit": None, "notes": None,
            "portions": [], "nutrients": {"calories": 100.0, "protein_g": 5.0},
        }]

        with _db.get_db() as conn:
            result = import_recipe_bundle(conn, recipes, food_valid)
            assert result["recipes_created"] == 0
            assert result["recipes_reused"] == 1
            recipe_rows = _db.recipe_list(conn)
            assert len(recipe_rows) == 1
            unchanged = _db.recipe_get(conn, existing_id)
            assert unchanged["description"] == "mine"
            assert unchanged["servings"] == 3

    def test_existing_food_name_is_reused_not_duplicated(self) -> None:
        with _db.get_db() as conn:
            _make_food(conn, 42, "Quinoa", protein_g=9.0)

        recipes = [{
            "name": "Cooked Quinoa", "description": "", "servings": 2.0,
            "total_weight": None, "total_weight_unit": None, "instructions": "",
            "ingredients": [
                {"food_name": "Quinoa", "amount": 100.0, "unit": "100 g",
                 "notes": None, "is_subrecipe": False},
            ],
        }]
        food_valid = [{
            "name": "Quinoa", "data_type": "Foundation", "brand": None,
            "serving_size": None, "serving_unit": None, "notes": None,
            "portions": [], "nutrients": {"calories": 100.0, "protein_g": 5.0},
        }]

        with _db.get_db() as conn:
            import_recipe_bundle(conn, recipes, food_valid)
            foods = _db.list_cached_foods(conn)
            assert len(foods) == 1
            assert foods[0]["fdc_id"] == 42

    def test_unresolvable_ingredient_is_skipped_with_warning(self) -> None:
        recipes = [{
            "name": "Mystery Dish", "description": "", "servings": 1.0,
            "total_weight": None, "total_weight_unit": None, "instructions": "",
            "ingredients": [
                {"food_name": "Unobtainium", "amount": 10.0, "unit": "10 g",
                 "notes": None, "is_subrecipe": False},
            ],
        }]
        with _db.get_db() as conn:
            result = import_recipe_bundle(conn, recipes, [])
            assert result["recipes_created"] == 1
            assert any("Unobtainium" in w for w in result["warnings"])
            rid = _db.recipe_list(conn)[0]["id"]
            assert _db.recipe_get_ingredients(conn, rid) == []


class TestParseRecipesCsv:
    def test_missing_recipe_name_column(self) -> None:
        recipes, warnings = parse_recipes_csv("a,b\n1,2\n")
        assert recipes == []
        assert any("recipe_name" in w for w in warnings)

    def test_recipe_with_no_ingredients(self) -> None:
        content = "recipe_name,servings\nEmpty Recipe,2\n"
        recipes, warnings = parse_recipes_csv(content)
        assert len(recipes) == 1
        assert recipes[0]["ingredients"] == []
        assert not warnings
