"""
Tests for numa_app/services/entry_parse.py — tolerant reading of typed
numbers, nutrient amounts with units, and pasted amino acid tables.
"""
import pytest

from numa_app.services.entry_parse import (EntryError, field_unit, normalize, parse_aa_block,
                                           parse_nutrient, parse_number, supplement_portion)


class TestParseNumber:
    @pytest.mark.parametrize("raw,expected", [
        ("12", 12.0), ("12.5", 12.5), (".5", 0.5), ("1,200", 1200.0), ("1,200.5", 1200.5),
        ("12,5", 12.5), ("1/2", 0.5), ("1 1/2", 1.5), ("½", 0.5), ("1½", 1.5), ("1 ½", 1.5),
        ("  7 ", 7.0), ("1 000", None),
    ])
    def test_reads(self, raw, expected):
        if expected is None:
            with pytest.raises(EntryError):
                parse_number(raw)
        else:
            assert parse_number(raw) == pytest.approx(expected)

    @pytest.mark.parametrize("raw", ["", "abc", "1/0", "12 mg", "1..2"])
    def test_rejects(self, raw):
        with pytest.raises(EntryError):
            parse_number(raw)


class TestParseNutrient:
    def test_field_units(self):
        assert [field_unit(k) for k in ("calories", "protein_g", "iron_mg", "b12_mcg")] == \
            ["kcal", "g", "mg", "mcg"]

    @pytest.mark.parametrize("key,raw,value,noted", [
        ("vitamin_d_mcg", "400 IU", 10.0, True),
        ("vitamin_d_mcg", "400iu", 10.0, True),
        ("vitamin_a_mcg", "5000 IU", 1500.0, True),
        ("vitamin_e_mg", "30 IU", 20.1, True),
        ("vitamin_a_mcg", "900 mcg RAE", 900.0, False),
        ("iron_mg", "18", 18.0, False),
        ("iron_mg", "18 mg", 18.0, False),
        ("iron_mg", "0.018 g", 18.0, True),
        ("b12_mcg", "2.4 µg", 2.4, False),
        ("b12_mcg", "0.0024 mg", 2.4, True),
        ("protein_g", "1,200 mg", 1.2, True),
        ("calories", "250 kcal", 250.0, False),
        ("calories", "1046 kJ", 250.0, True),
        ("sodium_mg", "trace", 0.0, True),
        ("fiber_g", "2½", 2.5, False),
    ])
    def test_reads_and_converts(self, key, raw, value, noted):
        v, note = parse_nutrient(key, raw, "X")
        assert v == pytest.approx(value, rel=1e-3)
        assert (note is not None) is noted

    @pytest.mark.parametrize("raw", ["", "-", "n/a", "N/A", "—"])
    def test_blank_words_are_blank(self, raw):
        assert parse_nutrient("iron_mg", raw) == (None, None)

    @pytest.mark.parametrize("key,raw,fragment", [
        ("iron_mg", "400 IU", "only be converted for vitamins A, D and E"),
        ("iron_mg", "10%", "percent of daily value"),
        ("iron_mg", "<0.5", "is a limit"),
        ("iron_mg", "-3", "negative"),
        ("iron_mg", "3 cups", "isn't a unit"),
        ("calories", "250 g", "isn't an energy unit"),
        ("iron_mg", "lots", "has no number"),
    ])
    def test_errors_say_why(self, key, raw, fragment):
        with pytest.raises(EntryError) as e:
            parse_nutrient(key, raw, "Iron")
        assert fragment in str(e.value)


class TestParseAaBlock:
    TABLE = "Lysine 5.2\nLeucine: 7.9\nArginine\t8.0\nL-Methionine = 1.4\nTryptophan 1,2"

    def test_per_100g_protein_is_scaled_by_protein(self):
        values, notes, errors = parse_aa_block(self.TABLE, "g_per_100g_protein", 20.0)
        assert errors == []
        assert values == {"aa_lysine_g": 1.04, "aa_leucine_g": 1.58,
                          "aa_methionine_g": 0.28, "aa_tryptophan_g": 0.24}
        assert any("Arginine" in n for n in notes)

    def test_other_units(self):
        assert parse_aa_block("Lysine 520", "mg_per_100g_food", None)[0] == {"aa_lysine_g": 0.52}
        assert parse_aa_block("Lysine 0.52", "g_per_100g_food", None)[0] == {"aa_lysine_g": 0.52}
        assert parse_aa_block("Lysine 52", "mg_per_g_protein", 10.0)[0] == {"aa_lysine_g": 0.52}

    def test_per_protein_without_protein_is_an_error(self):
        values, _, errors = parse_aa_block("Lysine 5.2", "g_per_100g_protein", None)
        assert values == {} and "Enter Protein first" in errors[0]

    def test_unknown_names_and_bad_lines_are_reported(self):
        _, _, errors = parse_aa_block("Lysine 5\nBananine 3\njust words\nLysine 6", "g_per_100g_food", None)
        assert len(errors) == 3
        assert "Bananine" in errors[0] and "name and a number" in errors[1] and "twice" in errors[2]

    def test_unit_must_be_chosen(self):
        assert parse_aa_block("Lysine 5", "", None)[2]


class TestSupplementPortion:
    @pytest.mark.parametrize("size,unit,expected", [
        (1, "tablet", {"description": "1 tablet", "gram_weight": 100.0}),
        (1.0, "Capsules", {"description": "1 capsule", "gram_weight": 100.0}),
        (2, "tablet", None), (1, "g", None), (None, "tablet", None), (1, "", None),
    ])
    def test_cases(self, size, unit, expected):
        assert supplement_portion(size, unit) == expected


def test_normalize_spells_out_fractions():
    assert normalize("1½ c") == "1 1/2 c"
    assert normalize("¾ cup") == "3/4 cup"
