"""
tests/test_recipe_translate.py — coverage for
numa_app/services/recipe_translate.py, the prompt-building and
response-parsing logic behind a recipe's manual-paste "Translate for
printing" workflow.
"""
import json

from numa_app.services import recipe_translate as _rt


ORIGINAL_RECIPE = {
    "name": "Chicken Soup",
    "description": "A comforting classic.",
    "introduction": "Great for cold days.",
    "instructions": "Simmer everything for an hour.",
    "disclaimer": _rt.DISCLAIMER_TEMPLATE.format(language="Spanish"),
}

ORIGINAL_INGREDIENTS = [
    {"food_name": "Chicken breast", "notes": "boneless", "volume_display": "1 cup"},
    {"food_name": "Carrot", "notes": "", "volume_display": "2 whole"},
]


class TestBuildTranslatePrompt:
    def test_includes_language_and_payload(self):
        prompt = _rt.build_translate_prompt(ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, "Spanish")
        assert "Spanish" in prompt
        assert "Chicken Soup" in prompt
        assert "Chicken breast" in prompt
        assert "```json" in prompt

    def test_disclaimer_language_substituted(self):
        prompt = _rt.build_translate_prompt(ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, "French")
        assert "French translation of the original English-language recipe" in prompt


class TestParseTranslationResponse:
    def test_fenced_json_parsed(self):
        text = '```json\n{"name": "Sopa de Pollo"}\n```'
        result = _rt.parse_translation_response(text)
        assert result == {"name": "Sopa de Pollo"}

    def test_bare_json_fallback(self):
        text = 'Here is the translation: {"name": "Sopa de Pollo"} — enjoy!'
        result = _rt.parse_translation_response(text)
        assert result == {"name": "Sopa de Pollo"}

    def test_garbage_returns_none_not_crash(self):
        assert _rt.parse_translation_response("no json here at all") is None
        assert _rt.parse_translation_response("") is None


class TestValidateTranslation:
    def _translated(self, **overrides):
        base = {
            "name": "Sopa de Pollo",
            "description": "Un clásico reconfortante.",
            "introduction": "Ideal para días fríos.",
            "instructions": "Cocine todo a fuego lento durante una hora.",
            "disclaimer": "Esta es una traducción al español...",
            "ingredients": [
                {"food_name": "Pechuga de pollo", "notes": "deshuesada", "volume_display": "1 taza"},
                {"food_name": "Zanahoria", "notes": "", "volume_display": "2 enteras"},
            ],
        }
        base.update(overrides)
        return base

    def test_clean_roundtrip(self):
        clean, warnings, hard_fail = _rt.validate_translation(
            ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, self._translated()
        )
        assert hard_fail is False
        assert warnings == []
        assert clean["name"] == "Sopa de Pollo"
        assert clean["ingredients"][0]["food_name"] == "Pechuga de pollo"

    def test_dropped_field_falls_back_to_english_with_warning(self):
        translated = self._translated()
        del translated["introduction"]
        clean, warnings, hard_fail = _rt.validate_translation(
            ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, translated
        )
        assert hard_fail is False
        assert clean["introduction"] == ORIGINAL_RECIPE["introduction"]
        assert any("introduction" in w for w in warnings)

    def test_dropped_ingredient_field_falls_back_with_warning(self):
        translated = self._translated()
        del translated["ingredients"][0]["notes"]
        clean, warnings, hard_fail = _rt.validate_translation(
            ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, translated
        )
        assert hard_fail is False
        assert clean["ingredients"][0]["notes"] == "boneless"
        assert any("Ingredient 1" in w and "notes" in w for w in warnings)

    def test_ingredient_count_mismatch_hard_fails(self):
        translated = self._translated()
        translated["ingredients"] = translated["ingredients"][:1]
        clean, warnings, hard_fail = _rt.validate_translation(
            ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, translated
        )
        assert hard_fail is True
        assert clean is None
        assert any("resubmit" in w.lower() for w in warnings)

    def test_non_dict_translated_hard_fails(self):
        clean, warnings, hard_fail = _rt.validate_translation(
            ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, None
        )
        assert hard_fail is True
        assert clean is None

    def test_missing_ingredients_key_hard_fails(self):
        translated = self._translated()
        del translated["ingredients"]
        clean, warnings, hard_fail = _rt.validate_translation(
            ORIGINAL_RECIPE, ORIGINAL_INGREDIENTS, translated
        )
        assert hard_fail is True
        assert clean is None
