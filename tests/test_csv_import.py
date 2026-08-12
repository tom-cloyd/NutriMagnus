"""
Tests for numa_app/services/csv_import.py — Food Cache CSV import parsing.
"""
import json

from numa_app.services.csv_export import CSV_COLUMNS, foods_to_csv
from numa_app.services.csv_import import parse_foods_csv


def _row(**overrides) -> str:
    fields = {k: "" for k in CSV_COLUMNS}
    fields.update(overrides)
    header = ",".join(CSV_COLUMNS)
    from csv import writer
    import io
    buf = io.StringIO()
    w = writer(buf)
    w.writerow([fields[k] for k in CSV_COLUMNS])
    return header + "\r\n" + buf.getvalue()


class TestParseFoodsCsv:
    def test_valid_row_parses(self):
        content = _row(name="Test Bar", protein_g="5.0", calories="120")
        valid, warnings = parse_foods_csv(content)
        assert len(valid) == 1
        assert valid[0]["name"] == "Test Bar"
        assert valid[0]["nutrients"]["protein_g"] == 5.0
        assert valid[0]["nutrients"]["calories"] == 120.0
        assert not warnings

    def test_missing_name_column_returns_no_rows(self):
        valid, warnings = parse_foods_csv("a,b,c\n1,2,3\n")
        assert valid == []
        assert any("name" in w for w in warnings)

    def test_row_missing_name_is_skipped_with_warning(self):
        content = _row(name="", protein_g="5.0")
        valid, warnings = parse_foods_csv(content)
        assert valid == []
        assert any("missing 'name'" in w for w in warnings)

    def test_row_with_no_nutrients_is_skipped_with_warning(self):
        content = _row(name="Empty Food")
        valid, warnings = parse_foods_csv(content)
        assert valid == []
        assert any("no usable nutrient values" in w for w in warnings)

    def test_non_numeric_nutrient_dropped_but_row_kept(self):
        content = _row(name="Test Food", protein_g="not-a-number", calories="100")
        valid, warnings = parse_foods_csv(content)
        assert len(valid) == 1
        assert "protein_g" not in valid[0]["nutrients"]
        assert valid[0]["nutrients"]["calories"] == 100.0
        assert any("protein_g" in w and "not a number" in w for w in warnings)

    def test_unknown_column_is_reported_once(self):
        content = "name,mystery_col,calories\nFoo,xyz,100\n"
        valid, warnings = parse_foods_csv(content)
        assert len(valid) == 1
        assert any("mystery_col" in w for w in warnings)

    def test_portions_json_round_trips(self):
        portions = [{"description": "1 bar", "gram_weight": 40.0}]
        content = _row(name="Test Bar", calories="100", portions=json.dumps(portions))
        valid, warnings = parse_foods_csv(content)
        assert valid[0]["portions"] == portions
        assert not warnings

    def test_malformed_portions_json_ignored_with_warning(self):
        content = _row(name="Test Bar", calories="100", portions="not json")
        valid, warnings = parse_foods_csv(content)
        assert valid[0]["portions"] == []
        assert any("not valid JSON" in w for w in warnings)

    def test_portion_missing_gram_weight_skipped(self):
        portions = [{"description": "1 bar"}]
        content = _row(name="Test Bar", calories="100", portions=json.dumps(portions))
        valid, warnings = parse_foods_csv(content)
        assert valid[0]["portions"] == []
        assert any("malformed portion" in w for w in warnings)

    def test_own_fdc_id_column_is_ignored_not_an_error(self):
        content = _row(name="Test Bar", calories="100", fdc_id="999999")
        valid, warnings = parse_foods_csv(content)
        assert len(valid) == 1
        assert "fdc_id" not in valid[0]
        assert not any("fdc_id" in w for w in warnings)

    def test_round_trips_through_foods_to_csv(self):
        row = {
            "fdc_id": 1, "name": "Round Trip Food", "data_type": "Foundation",
            "brand": None, "serving_size": None, "serving_unit": None,
            "notes": None, "nutrients_json": json.dumps({"calories": 50.0, "protein_g": 2.0}),
            "portions_json": json.dumps([{"description": "1 cup", "gram_weight": 120.0}]),
        }
        content = foods_to_csv([row])
        valid, warnings = parse_foods_csv(content)
        assert not warnings
        assert len(valid) == 1
        assert valid[0]["name"] == "Round Trip Food"
        assert valid[0]["nutrients"] == {"calories": 50.0, "protein_g": 2.0}
        assert valid[0]["portions"] == [{"description": "1 cup", "gram_weight": 120.0}]
