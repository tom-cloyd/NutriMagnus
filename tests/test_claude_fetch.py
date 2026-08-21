"""
tests/test_claude_fetch.py — coverage for numa_app/services/claude_fetch.py,
the prompt-building and response-parsing logic behind the web app's
Food Cache -> "Fetch missing data from Claude AI" / "Import Claude response"
workflow. Previously untested despite being pure, easily-testable logic with
real arithmetic (the per-serving-to-per-100g conversion).
"""
import db as _db
from numa_app.services import claude_fetch as _cf


class TestBuildPrompt:
    def test_includes_food_count_and_names(self):
        prompt = _cf.build_prompt([(123, "Chicken breast"), (None, "Homemade granola")])
        assert "2 food(s)" in prompt
        assert "123  Chicken breast" in prompt
        assert "(no FDC ID)  Homemade granola" in prompt

    def test_empty_selection(self):
        prompt = _cf.build_prompt([])
        assert "0 food(s)" in prompt


class TestParseResponse:
    def test_fenced_json_block_parsed(self):
        text = '''Here you go:
```json
{"name": "Chicken breast", "fdc_id": 171477, "protein_g": 31.0}
```
'''
        blocks, curator_text, warnings = _cf.parse_response(text)
        assert len(blocks) == 1
        assert blocks[0]["name"] == "Chicken breast"
        assert warnings == []

    def test_multiple_fenced_blocks(self):
        text = (
            '```json\n{"name": "A", "fdc_id": 1, "protein_g": 1}\n```\n'
            '```json\n{"name": "B", "fdc_id": 2, "protein_g": 2}\n```'
        )
        blocks, _curator, warnings = _cf.parse_response(text)
        assert [b["name"] for b in blocks] == ["A", "B"]
        assert warnings == []

    def test_malformed_json_in_fence_produces_warning_not_crash(self):
        text = '```json\n{"name": "Bad", "fdc_id": }\n```'
        blocks, _curator, warnings = _cf.parse_response(text)
        assert blocks == []
        assert any("JSON parse error" in w for w in warnings)

    def test_curator_text_extracted_around_json(self):
        text = (
            "Note: I used SR Legacy data throughout.\n"
            '```json\n{"name": "A", "fdc_id": 1, "protein_g": 1}\n```\n'
            "Let me know if you need more foods."
        )
        _blocks, curator_text, _warnings = _cf.parse_response(text)
        assert "SR Legacy" in curator_text
        assert "more foods" in curator_text

    def test_bare_json_fallback_when_no_fenced_blocks(self):
        """Claude sometimes replies without ```json fences — the brace-matching
        fallback must still find well-formed objects that include fdc_id."""
        text = 'Here is the data: {"name": "Chicken breast", "fdc_id": 171477, "protein_g": 31.0} — done.'
        blocks, _curator, warnings = _cf.parse_response(text)
        assert len(blocks) == 1
        assert blocks[0]["fdc_id"] == 171477
        assert any("No fenced JSON" in w for w in warnings)

    def test_bare_json_without_fdc_id_is_ignored(self):
        """The bare-object fallback requires 'fdc_id' as a signal that this is
        really a food block, not incidental JSON-looking text in the reply."""
        text = 'Some prose with a {"note": "not a food block"} aside.'
        blocks, _curator, _warnings = _cf.parse_response(text)
        assert blocks == []

    def test_no_json_at_all(self):
        blocks, curator_text, warnings = _cf.parse_response("Sorry, I don't have data for that food.")
        assert blocks == []
        assert curator_text is None
        assert any("No fenced JSON" in w for w in warnings)


class TestValidateBlock:
    def test_valid_block_passes(self):
        block = {"name": "Chicken breast", "fdc_id": 171477, "fdc_type": "SR Legacy",
                  "protein_g": 31.0, "aa_leucine_g": 2.4}
        result, warnings = _cf.validate_block(block, 1)
        assert result["name"] == "Chicken breast"
        assert result["fdc_id"] == 171477
        assert result["nutrients"] == {"protein_g": 31.0, "aa_leucine_g": 2.4}
        assert warnings == []

    def test_missing_name_skipped(self):
        result, warnings = _cf.validate_block({"fdc_id": 1, "protein_g": 1}, 1)
        assert result is None
        assert any("missing 'name'" in w for w in warnings)

    def test_missing_fdc_id_skipped(self):
        result, warnings = _cf.validate_block({"name": "X", "protein_g": 1}, 1)
        assert result is None
        assert any("missing/invalid 'fdc_id'" in w for w in warnings)

    def test_string_fdc_id_coerced_to_int(self):
        result, warnings = _cf.validate_block({"name": "X", "fdc_id": "171477", "protein_g": 1}, 1)
        assert result["fdc_id"] == 171477
        assert warnings == []

    def test_non_numeric_string_fdc_id_skipped(self):
        result, warnings = _cf.validate_block({"name": "X", "fdc_id": "not-a-number", "protein_g": 1}, 1)
        assert result is None
        assert any("missing/invalid 'fdc_id'" in w for w in warnings)

    def test_invalid_fdc_type_falls_back_to_user_drafted(self):
        result, warnings = _cf.validate_block(
            {"name": "X", "fdc_id": 1, "fdc_type": "Not A Real Type", "protein_g": 1}, 1
        )
        assert result["fdc_type"] == "User Drafted"
        assert any("unknown fdc_type" in w for w in warnings)

    def test_unrecognized_keys_stripped_and_reported(self):
        result, warnings = _cf.validate_block(
            {"name": "X", "fdc_id": 1, "protein_g": 1, "made_up_field": 42}, 1
        )
        assert "made_up_field" not in result["nutrients"]
        assert any("made_up_field" in w for w in warnings)

    def test_non_numeric_nutrient_value_skipped(self):
        result, warnings = _cf.validate_block(
            {"name": "X", "fdc_id": 1, "protein_g": "a lot"}, 1
        )
        assert "protein_g" not in result["nutrients"]
        assert any("non-numeric" in w for w in warnings)

    def test_per_serving_conversion_arithmetic(self):
        """Computational validation: a 28g-serving label (120 cal, 3g protein)
        must scale to per-100g by the documented factor 100/serving_size_g."""
        block = {
            "name": "Protein bar", "fdc_id": 1, "fdc_type": "Branded",
            "serving_size_g": 28, "nutrition_per_serving": {"calories": 120, "protein_g": 3},
        }
        result, warnings = _cf.validate_block(block, 1)
        factor = 100 / 28
        assert result["nutrients"]["calories"] == 120 * factor
        assert result["nutrients"]["protein_g"] == 3 * factor
        assert "Converted from per-28g label values" in result["confidence_note"]
        assert warnings == []

    def test_per_serving_without_valid_serving_size_is_skipped(self):
        block = {
            "name": "Protein bar", "fdc_id": 1,
            "nutrition_per_serving": {"protein_g": 3},
        }
        result, warnings = _cf.validate_block(block, 1)
        assert result["nutrients"] == {}
        assert any("without a valid 'serving_size_g'" in w for w in warnings)


class TestValidateAll:
    def test_aggregates_valid_foods_and_warnings_across_blocks(self):
        blocks = [
            {"name": "Good food", "fdc_id": 1, "protein_g": 10},
            {"fdc_id": 2, "protein_g": 5},  # missing name
        ]
        valid, warnings = _cf.validate_all(blocks)
        assert len(valid) == 1
        assert valid[0]["name"] == "Good food"
        assert any("missing 'name'" in w for w in warnings)


class TestBuildNotes:
    def test_combines_source_and_confidence(self):
        note = _cf.build_notes({"source": "USDA FDC 1", "confidence_note": "measured"})
        assert note == "Source: USDA FDC 1  |  Confidence: measured"

    def test_none_when_neither_present(self):
        assert _cf.build_notes({}) is None

    def test_source_only(self):
        assert _cf.build_notes({"source": "USDA FDC 1"}) == "Source: USDA FDC 1"


class TestImportFoods:
    def test_writes_validated_foods_to_cache(self):
        valid = [{
            "name": "Chicken breast", "fdc_id": 171477, "fdc_type": "SR Legacy",
            "source": "USDA FDC 171477", "confidence_note": "measured",
            "nutrients": {"protein_g": 31.0},
        }]
        with _db.get_db() as conn:
            _cf.import_foods(conn, valid, curator_text="Used SR Legacy throughout.")
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, 171477)
        assert cached["name"] == "Chicken breast"
        assert cached["curator_notes"] == "Used SR Legacy throughout."
        assert "Source: USDA FDC 171477" in cached["notes"]
