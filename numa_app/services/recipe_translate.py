"""
recipe_translate.py — prompt-building and response-parsing for the
manual-paste recipe translation workflow behind a recipe's print/export page.

Mirrors the shape of claude_fetch.py: numa builds a prompt containing the
recipe's translatable text, the user pastes it into their own AI chat tool,
translates it, and pastes the reply back here for parsing/validation. No
API key, no network call, no cost — pure functions only, no HTML output.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/recipe_translate.py — recipe translation workflow"
"""
from __future__ import annotations

import json
import re

RECIPE_TEXT_KEYS = ["name", "description", "introduction", "instructions", "notes", "disclaimer"]
INGREDIENT_TEXT_KEYS = ["food_name", "notes", "volume_display"]

DISCLAIMER_TEMPLATE = (
    "This is a {language} translation of the original English-language recipe. "
    "Ingredient units show the English original in parentheses after the translated term."
)

PROMPT_TEMPLATE = """\
Please translate the string values in the JSON below into {language}.

Rules:
1. Translate ONLY the string values — never the JSON keys, never numbers.
2. Keep the exact same JSON structure: the same top-level keys, and the same
   number of objects in the "ingredients" array, in the same order.
3. Return a translated value for EVERY key present in the input, even one you
   find hard to translate well — in that case, do your best rather than
   omitting the key. Do not add or remove any key.
4. Ingredient names should be natural, recognizable translations for a cook
   shopping in that language — not overly literal.
5. Some fields may be empty strings ("") — return them as empty strings, not
   translated placeholder text.
6. Return ONLY the translated JSON in a single fenced ```json code block, and
   nothing else — no commentary before or after.

```json
{payload}
```"""


def _text_or_empty(value) -> str:
    return value if isinstance(value, str) else ""


def extract_ingredient_fields(ingredients: list[dict]) -> list[dict]:
    """Reduce full ingredient rows to just the fields translation touches,
    in a stable order, with missing values normalized to "" ."""
    return [
        {
            "food_name":      _text_or_empty(ing.get("food_name")),
            "notes":          _text_or_empty(ing.get("notes")),
            "volume_display": _text_or_empty(ing.get("volume_display")),
        }
        for ing in ingredients
    ]


def build_translate_prompt(recipe: dict, ingredients: list[dict], target_language: str) -> str:
    """Build the paste-into-your-AI-chat prompt for translating one recipe."""
    payload = {key: _text_or_empty(recipe.get(key)) for key in RECIPE_TEXT_KEYS if key != "disclaimer"}
    payload["disclaimer"] = DISCLAIMER_TEMPLATE.format(language=target_language)
    payload["ingredients"] = extract_ingredient_fields(ingredients)
    return PROMPT_TEMPLATE.format(
        language=target_language,
        payload=json.dumps(payload, indent=2, ensure_ascii=False),
    )


def parse_translation_response(text: str) -> dict | None:
    """Extract the single translated JSON object from a pasted AI reply.

    Handles a fenced ```json block first, falling back to brace-matching the
    first bare JSON object found. Returns None if nothing parseable is found.
    """
    for m in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL):
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue

    # Fallback: brace-match the first top-level { } in the text.
    i = 0
    while i < len(text):
        if text[i] != "{":
            i += 1
            continue
        depth, in_str, esc, j = 0, False, False, i
        while j < len(text):
            ch = text[j]
            if esc:
                esc = False
            elif ch == "\\" and in_str:
                esc = True
            elif ch == '"':
                in_str = not in_str
            elif not in_str:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            obj = json.loads(text[i : j + 1])
                            if isinstance(obj, dict):
                                return obj
                        except json.JSONDecodeError:
                            pass
                        break
            j += 1
        i = j + 1
    return None


def validate_translation(
    original_recipe: dict,
    original_ingredients: list[dict],
    translated: dict | None,
) -> tuple[dict | None, list[str], bool]:
    """Validate a parsed translation against the original recipe fields.

    Returns (clean_dict, warnings, hard_fail):
    - hard_fail=True (clean_dict=None) when the ingredients array length
      doesn't match the original — row alignment can't be trusted, so this
      isn't recoverable by falling back field-by-field.
    - hard_fail=False otherwise; any missing/non-string field falls back to
      the original English text, with a warning naming it.
    """
    warnings: list[str] = []

    if not isinstance(translated, dict):
        return None, ["Could not find a JSON object in the pasted reply — nothing to review."], True

    orig_ingredients = extract_ingredient_fields(original_ingredients)
    translated_ingredients_raw = translated.get("ingredients")

    if not isinstance(translated_ingredients_raw, list) or len(translated_ingredients_raw) != len(orig_ingredients):
        got = len(translated_ingredients_raw) if isinstance(translated_ingredients_raw, list) else 0
        warnings.append(
            f"Expected {len(orig_ingredients)} ingredient(s) in the reply, got {got} — "
            "the ingredient list can't be safely matched up. Please resubmit."
        )
        return None, warnings, True

    clean: dict = {}
    for key in RECIPE_TEXT_KEYS:
        original_value = _text_or_empty(original_recipe.get(key)) if key != "disclaimer" else original_recipe.get("disclaimer", "")
        value = translated.get(key)
        if isinstance(value, str) and value.strip():
            clean[key] = value
        else:
            clean[key] = original_value
            if original_value:
                warnings.append(f"'{key}' was missing from the reply — kept the original English text.")

    clean_ingredients = []
    for idx, (orig, trans) in enumerate(zip(orig_ingredients, translated_ingredients_raw), 1):
        row = {}
        if not isinstance(trans, dict):
            trans = {}
        for key in INGREDIENT_TEXT_KEYS:
            value = trans.get(key)
            if isinstance(value, str) and value.strip():
                row[key] = value
            else:
                row[key] = orig[key]
                if orig[key]:
                    warnings.append(f"Ingredient {idx}: '{key}' was missing from the reply — kept the original English text.")
        clean_ingredients.append(row)
    clean["ingredients"] = clean_ingredients

    return clean, warnings, False
