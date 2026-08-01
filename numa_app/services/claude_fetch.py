"""
claude_fetch.py — shared prompt-building and response-parsing for the
Claude AI amino-acid/nutrient fetch workflow (CLI Food Cache i/r commands,
and the web app's equivalent Food Cache pages).

Pure functions only — no console/HTML output here, so both the CLI
(numa_app/workflows/foods.py) and the web app (web/backend.py) can wrap the
same logic in their own presentation.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/claude_fetch.py — Claude fetch/import workflow"
"""
from __future__ import annotations

import json
import re

from .food_import import VALID_NUTRIENT_KEYS, convert_per_serving, validate_and_strip

META_KEYS = {
    "name", "fdc_id", "fdc_type", "source", "confidence_note",
    "serving_size_g", "nutrition_per_serving",
}

AA_KEYS = {k for k in VALID_NUTRIENT_KEYS if k.startswith("aa_")}

VALID_FDC_TYPES = {
    "Foundation", "SR Legacy", "Branded", "Survey (FNDDS)", "User Drafted", "OFF",
}

PROMPT_TEMPLATE = """\
I need complete nutritional data for {n} food(s), formatted as JSON for direct import into a Python nutrition app.

Output ALL foods in a SINGLE reply — one fenced ```json ... ``` block per food, all in the same response. Do not split your answer across multiple messages. Each block must follow this exact structure — metadata keys first, then all available nutrient keys:

```json
{{
  "name": "Full food name",
  "fdc_id": 123456,
  "fdc_type": "SR Legacy",
  "source": "USDA FoodData Central FDC 123456 (measured values)",
  "confidence_note": "Brief note on data quality and any estimates made",
  "calories": 0,
  "protein_g": 0
}}
```

All nutrient values are per 100 g edible portion. Use exactly these key names (omit any key whose value is genuinely unknown — never substitute 0 for unknown):

    calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g,
    saturated_fat_g, mono_fat_g, poly_fat_g,
    omega3_ala_mg, omega3_epa_mg, omega3_dha_mg, omega6_la_mg,
    calcium_mg, iron_mg, magnesium_mg, phosphorus_mg,
    potassium_mg, sodium_mg, zinc_mg, iodine_mcg, selenium_mcg,
    vitamin_a_mcg, vitamin_c_mg, vitamin_d_mcg, vitamin_e_mg,
    vitamin_k_mcg, thiamin_mg, riboflavin_mg, niacin_mg,
    b6_mg, folate_mcg, b12_mcg,
    beta_carotene_mcg, alpha_carotene_mcg, lycopene_mcg,
    lutein_zeaxanthin_mcg, choline_mg, beta_sitosterol_mg, isoflavones_mg,
    aa_tryptophan_g, aa_threonine_g, aa_isoleucine_g, aa_leucine_g,
    aa_lysine_g, aa_methionine_g, aa_cystine_g, aa_phenylalanine_g,
    aa_tyrosine_g, aa_valine_g, aa_histidine_g

Critical rules:
1. Amino acid values are per 100 g FOOD, in grams (not mg, not per g protein).
2. aa_methionine_g and aa_cystine_g are always separate keys — never combined.
3. aa_phenylalanine_g and aa_tyrosine_g are always separate keys — never combined.
4. Omit any key where the value is genuinely unknown; do not estimate 0.
5. For true zeros (e.g. vitamin B12 in plant foods), include the key explicitly with value 0.
6. Source hierarchy: prefer USDA FoodData Central (cite FDC ID), then USDA SR Legacy (cite FDC ID), then peer-reviewed literature (cite paper), then estimate (flag clearly in confidence_note). Note: direct access to the USDA database is not possible — use your training data, which mirrors these sources.
7. fdc_type must be exactly one of: "Foundation", "SR Legacy", "Branded", "Survey (FNDDS)", "User Drafted".
8. If scaling from a non-100 g reference portion, show the calculation in confidence_note — UNLESS rule 9 applies.
9. For a packaged/branded product where you have the manufacturer's Nutrition Facts label (per-serving values), do NOT do the per-100g arithmetic yourself. Instead replace the flat nutrient keys with:
     "serving_size_g": 28,
     "nutrition_per_serving": {{ "calories": 120, "protein_g": 3, ... }}
   numa converts this to per-100g automatically, which is more reliable than an LLM doing the scaling in prose. Use the same key names as above inside nutrition_per_serving.

Foods ({n} total — USDA FDC IDs provided where known):
{food_list}"""


def build_prompt(selected: list[tuple[int | None, str]]) -> str:
    """Build the Claude prompt text for a list of (fdc_id, name) foods."""
    lines = "\n".join(
        f"    {fdc_id}  {name}" if fdc_id else f"    (no FDC ID)  {name}"
        for fdc_id, name in selected
    )
    return PROMPT_TEMPLATE.format(n=len(selected), food_list=lines)


def parse_response(text: str) -> tuple[list[dict], str | None, list[str]]:
    """Parse Claude's response into (food_blocks, curator_text, warnings).

    Handles fenced ```json blocks and bare JSON objects. Any non-JSON text
    (curator notes, recommendations, caveats) is returned as curator_text.
    """
    blocks: list[dict] = []
    spans: list[tuple[int, int]] = []  # character spans of JSON content to strip
    warnings: list[str] = []

    # Primary: fenced ```json ... ``` blocks
    for m in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL):
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                blocks.append(obj)
                spans.append((m.start(), m.end()))
        except json.JSONDecodeError as exc:
            preview = m.group(1)[:60].replace("\n", " ")
            warnings.append(f"JSON parse error in fenced block: {preview!r} ({exc})")

    if not blocks:
        # Fallback: bare JSON objects — brace-match to find each top-level { }
        warnings.append("No fenced JSON blocks found — scanning for bare JSON objects…")
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
                                if isinstance(obj, dict) and "fdc_id" in obj:
                                    blocks.append(obj)
                                    spans.append((i, j + 1))
                            except json.JSONDecodeError:
                                pass
                            break
                j += 1
            i = j + 1

    # Extract non-JSON text (curator notes) by removing JSON spans
    curator_text: str | None = None
    if spans:
        remaining = text
        for start, end in sorted(spans, reverse=True):
            remaining = remaining[:start] + remaining[end:]
        lines = [ln for ln in remaining.split("\n") if ln.strip()]
        curator_text = "\n".join(lines).strip() or None

    return blocks, curator_text, warnings


def validate_block(block: dict, idx: int) -> tuple[dict | None, list[str]]:
    """Validate and clean one food block. Returns (cleaned dict or None, warnings)."""
    warnings: list[str] = []
    name   = block.get("name")
    fdc_id = block.get("fdc_id")

    if not name:
        warnings.append(f"Block {idx}: missing 'name' — skipped.")
        return None, warnings

    if isinstance(fdc_id, str):
        try:
            fdc_id = int(fdc_id)
        except ValueError:
            fdc_id = None
    if not isinstance(fdc_id, int):
        warnings.append(f"Block {idx} ({name!r}): missing/invalid 'fdc_id' — skipped.")
        return None, warnings

    fdc_type = block.get("fdc_type", "User Drafted")
    if fdc_type not in VALID_FDC_TYPES:
        warnings.append(f"Block {idx} ({name!r}): unknown fdc_type {fdc_type!r} — using 'User Drafted'.")
        fdc_type = "User Drafted"

    nutrients: dict[str, float] = {}
    stripped: list[str] = []
    for k, v in block.items():
        if k in META_KEYS:
            continue
        if k in VALID_NUTRIENT_KEYS:
            if isinstance(v, (int, float)):
                nutrients[k] = float(v)
            else:
                warnings.append(f"Block {idx} ({name!r}): {k!r} is non-numeric — skipped.")
        else:
            stripped.append(k)

    if stripped:
        warnings.append(f"Block {idx} ({name!r}): stripped unrecognised keys: {', '.join(stripped)}")

    confidence_note = block.get("confidence_note")

    # Alternate input shape: per-serving values + serving_size_g, for label-sourced
    # data (e.g. a packaged product's Nutrition Facts panel). Converted to per-100g.
    per_serving = block.get("nutrition_per_serving")
    serving_size_g = block.get("serving_size_g")
    if per_serving is not None:
        if not isinstance(serving_size_g, (int, float)) or serving_size_g <= 0:
            warnings.append(
                f"Block {idx} ({name!r}): 'nutrition_per_serving' given "
                f"without a valid 'serving_size_g' — per-serving values skipped."
            )
        else:
            per_serving_clean, per_serving_stripped = validate_and_strip(per_serving)
            if per_serving_stripped:
                warnings.append(
                    f"Block {idx} ({name!r}): stripped unrecognised per-serving keys: "
                    f"{', '.join(per_serving_stripped)}"
                )
            converted = convert_per_serving(per_serving_clean, float(serving_size_g))
            nutrients.update(converted)
            factor = 100 / float(serving_size_g)
            note = f"Converted from per-{serving_size_g:g}g label values (×{factor:.3f})."
            confidence_note = f"{confidence_note}  {note}" if confidence_note else note

    return {
        "name":            name,
        "fdc_id":          fdc_id,
        "fdc_type":        fdc_type,
        "source":          block.get("source"),
        "confidence_note": confidence_note,
        "nutrients":       nutrients,
    }, warnings


def validate_all(raw_blocks: list[dict]) -> tuple[list[dict], list[str]]:
    """Validate every block, returning (valid_foods, all_warnings)."""
    valid: list[dict] = []
    warnings: list[str] = []
    for i, block in enumerate(raw_blocks, 1):
        result, block_warnings = validate_block(block, i)
        warnings.extend(block_warnings)
        if result:
            valid.append(result)
    return valid, warnings


def build_notes(food: dict) -> str | None:
    """Build the source/confidence notes string stored with an imported food."""
    parts = []
    if food.get("source"):
        parts.append(f"Source: {food['source']}")
    if food.get("confidence_note"):
        parts.append(f"Confidence: {food['confidence_note']}")
    return "  |  ".join(parts) if parts else None


def import_foods(conn, valid: list[dict], curator_text: str | None) -> None:
    """Write validated food blocks to the cache. Shared final step for CLI and web."""
    import db as _db
    for f in valid:
        _db.cache_food(
            conn,
            fdc_id=f["fdc_id"],
            name=f["name"],
            data_type=f["fdc_type"],
            brand=None,
            serving_size=None,
            serving_unit=None,
            nutrients=f["nutrients"],
            notes=build_notes(f),
            curator_notes=curator_text,
        )
