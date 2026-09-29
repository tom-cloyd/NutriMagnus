"""
Tests for numa_app/services/gi_table_build.py — building the user's own
gi_data_local.json from the Atkinson 2021 International Tables supplemental
PDFs (Settings -> Glycemic Index Reference Table, or scripts/build_gi_data.py).

The PDFs themselves are not in the repo (their licence forbids redistribution),
so these cover the decision logic rather than the PDF reading: which population
a row belongs to, which 2008 rows survive the merge, the cell parsing that the
column windows feed, and build_table()'s refusal to replace a working table
with a bad one.
"""
import json
import time
from pathlib import Path

import pytest

import gi_lookup
from numa_app.services import gi_table_build as build_gi_data


# --- population, which is a per-row fact and not a property of the table ----

def test_impaired_subject_groups_are_classified_as_impaired() -> None:
    for subj in ("Type 1", "Type 2", "Type 2 diabetes", "IGT", "GDM", "Mixed"):
        assert build_gi_data._classify_population(subj, iso=False) == "impaired"


def test_normal_subjects_in_the_method_deviation_table_stay_normal() -> None:
    """Supplemental Table 2 is split off for method reasons, not population, so
    its normal-tolerance rows must not be mislabelled impaired."""
    assert build_gi_data._classify_population("Normal", iso=False) == "normal"


def test_unreadable_subject_cell_falls_back_by_table() -> None:
    # Table 1 requires normal glucose tolerance of every row it contains, so an
    # unparsed cell there is still normal; Table 2 mixes groups, so it is not.
    assert build_gi_data._classify_population(None, iso=True) == "normal"
    assert build_gi_data._classify_population(None, iso=False) == "unknown"
    assert build_gi_data._classify_population("NS", iso=False) == "unknown"


# --- GI cell parsing ------------------------------------------------------

def test_gi_with_standard_error_is_split() -> None:
    assert build_gi_data._parse_gi("20±4") == (20.0, 4.0)
    assert build_gi_data._parse_gi("73 ± 12") == (73.0, 12.0)


def test_bare_gi_without_a_standard_error_is_accepted() -> None:
    assert build_gi_data._parse_gi("45") == (45.0, None)


def test_gi_above_one_hundred_is_kept() -> None:
    """Sucrose reaches 132 on the glucose scale in these tables; a cap at 100
    or 110 would silently drop those rows."""
    assert build_gi_data._parse_gi("132") == (132.0, None)
    assert build_gi_data._parse_gi("110±21") == (110.0, 21.0)


def test_empty_or_implausible_gi_cell_yields_nothing() -> None:
    assert build_gi_data._parse_gi("") == (None, None)
    assert build_gi_data._parse_gi("NS") == (None, None)
    assert build_gi_data._parse_gi("9999") == (None, None)


# --- the merge rule -------------------------------------------------------

def _keys(*names: str) -> tuple[set[str], dict[str, set[str]]]:
    keys = {build_gi_data._merge_key(n) for n in names}
    return keys, {k: set(k.split()) for k in keys}


def test_identical_name_counts_as_superseded() -> None:
    keys, tokens = _keys("Banana cake, made with sugar")
    assert build_gi_data._superseded(
        build_gi_data._merge_key("Banana cake, made with sugar"), keys, tokens)


def test_reworded_2021_description_still_counts_as_superseded() -> None:
    """2021 moved brands out of parentheses and reordered descriptions, so exact
    equality alone would keep thousands of duplicates in the legacy tier."""
    keys, tokens = _keys("Flax bread made from flax meal wheat flour")
    key = build_gi_data._merge_key(
        "Bread, flax, made from flax meal & wheat flour (Canada)")
    assert build_gi_data._superseded(key, keys, tokens)


def test_a_food_2021_does_not_cover_is_not_superseded() -> None:
    keys, tokens = _keys("White bread", "Banana, raw")
    key = build_gi_data._merge_key(
        "Divine Date spread (Buderim Ginger, Buderim, QLD, Australia)")
    assert not build_gi_data._superseded(key, keys, tokens)


def test_short_fragment_does_not_match_by_containment() -> None:
    """"peas" is a substring of many names; containment needs a minimum length
    or a fragment would wrongly retire unrelated 2021 rows."""
    keys, tokens = _keys("Split peas, yellow, boiled")
    assert not build_gi_data._superseded("peas", keys, tokens)


# --- legacy name repair ---------------------------------------------------

def test_fragmentary_legacy_name_regains_its_category() -> None:
    assert build_gi_data._repair_legacy_name("Type NS (India)", "Millet") == \
        "Millet, Type NS (India)"
    assert build_gi_data._repair_legacy_name("New (Canada)", "Potatoes") == \
        "Potatoes, New (Canada)"


def test_a_full_legacy_name_is_left_alone() -> None:
    name = "Lamingtons (sponge dipped in chocolate and coconut)"
    assert build_gi_data._repair_legacy_name(name, "Cakes") == name


def test_wrecked_category_is_not_prepended() -> None:
    """Some 2008 categories are themselves debris from that parser's heuristic;
    prefixing with those would compound the mess rather than fix it."""
    assert build_gi_data._repair_legacy_name(
        "Brown (Canada)", "(Cyamoposis tetragonolobus) (soluble fiber)") == \
        "Brown (Canada)"


def test_category_already_in_the_name_is_not_repeated() -> None:
    assert build_gi_data._repair_legacy_name("Muesli (Canada)", "Muesli") == \
        "Muesli (Canada)"


# --- column geometry ------------------------------------------------------

def test_name_column_boundary_falls_between_the_two_clusters() -> None:
    """Line starts cluster at the food-number column and the name column; the
    boundary must separate them, and the margin differs between the tables."""
    starts = [35.0] * 250 + [62.0] * 380 + [29.0]
    boundary = build_gi_data._name_column_x0(starts)
    assert 35.0 < boundary < 62.0


def test_food_numbers_reject_a_stray_integer_outside_the_column() -> None:
    candidates = [(100.0, 1, 53.0), (130.0, 2, 53.0), (140.0, 200, 180.0)]
    assert build_gi_data._food_numbers(candidates) == [(100.0, 1), (130.0, 2)]


def test_food_numbers_keep_a_misprinted_out_of_sequence_number() -> None:
    """Two rows carry a wrong number in the published PDF. The number is only a
    label, so the row must survive it."""
    candidates = [(100.0, 2210, 53.0), (130.0, 2111, 53.0), (160.0, 2212, 53.0)]
    assert build_gi_data._food_numbers(candidates) == [
        (100.0, 2210), (130.0, 2111), (160.0, 2212)]


# --- build_table(): which file is which, and refusing bad input ------------

def _heading_page(n: int) -> list[tuple[float, float, str]]:
    words = f"Supplemental Table {n}. Glycemic index (GI) values".split()
    return [(40.0 + i * 30, 50.0, w) for i, w in enumerate(words)]


def test_table_number_is_read_from_the_heading() -> None:
    assert build_gi_data._table_number([_heading_page(1)]) == 1
    assert build_gi_data._table_number([[], _heading_page(2)]) == 2
    assert build_gi_data._table_number([[(40.0, 50.0, "Something else")]]) is None


def _fake_rows(n: int, iso: bool) -> list[dict]:
    return [{"food_number": i, "name": f"Food {iso} {i}", "gi_glucose": 50.0,
             "sem": None, "year": 2000, "country": None, "subjects_type": "Normal",
             "subjects_n": 10, "category": None, "subcategory": None, "iso": iso,
             "edition": 2021, "ref": "", "population": "normal"} for i in range(n)]


def _stub_pdfs(monkeypatch, tables: dict[str, int | None], rows: int = 2000) -> None:
    """Make _pdf_pages report each file's table number from `tables` (by file
    name), and _parse_pages return `rows` rows per table."""
    monkeypatch.setattr(build_gi_data, "_pdf_pages",
                        lambda path: [_heading_page(tables[path.name])] if tables[path.name] else [[]])
    monkeypatch.setattr(build_gi_data, "_parse_pages",
                        lambda pages, iso: (_fake_rows(rows, iso), []))
    monkeypatch.setattr(build_gi_data, "BASELINE", Path("/nonexistent/gi_data.json"))


def test_build_accepts_the_two_tables_in_either_order(tmp_path, monkeypatch) -> None:
    _stub_pdfs(monkeypatch, {"a.pdf": 2, "b.pdf": 1})
    out = tmp_path / "gi_data_local.json"
    result = build_gi_data.build_table([tmp_path / "a.pdf", tmp_path / "b.pdf"], out)
    assert (result["table1"], result["table2"]) == (2000, 2000)
    data = json.loads(out.read_text())
    assert sum(1 for r in data["normal"] if r["iso"]) == 2000   # table 1 parsed as ISO


@pytest.mark.parametrize("tables, message", [
    ({"a.pdf": 1, "b.pdf": 1}, "Both files are Supplemental Table 1"),
    ({"a.pdf": 1, "b.pdf": None}, "doesn't look like either supplemental table"),
])
def test_build_refuses_wrong_files_and_writes_nothing(tmp_path, monkeypatch, tables, message) -> None:
    _stub_pdfs(monkeypatch, tables)
    out = tmp_path / "gi_data_local.json"
    out.write_text("existing")
    with pytest.raises(build_gi_data.BuildError, match=message):
        build_gi_data.build_table([tmp_path / "a.pdf", tmp_path / "b.pdf"], out)
    assert out.read_text() == "existing"


def test_build_refuses_a_table_that_yields_too_few_rows(tmp_path, monkeypatch) -> None:
    _stub_pdfs(monkeypatch, {"a.pdf": 1, "b.pdf": 2}, rows=40)
    out = tmp_path / "gi_data_local.json"
    with pytest.raises(build_gi_data.BuildError, match="Only 40 foods"):
        build_gi_data.build_table([tmp_path / "a.pdf", tmp_path / "b.pdf"], out)
    assert not out.exists()


def test_build_rejects_a_file_that_is_not_a_pdf(tmp_path) -> None:
    junk = tmp_path / "notes.pdf"
    junk.write_text("not a pdf at all")
    with pytest.raises(build_gi_data.BuildError, match="could not be read as a PDF"):
        build_gi_data.build_table([junk, junk], tmp_path / "out.json")


def test_a_finished_build_is_picked_up_without_a_restart(tmp_path, monkeypatch) -> None:
    """gi_lookup caches its table for the life of the process; the build must
    invalidate that, or the new table stays invisible until restart."""
    _stub_pdfs(monkeypatch, {"a.pdf": 1, "b.pdf": 2})
    out = tmp_path / "gi_data_local.json"
    monkeypatch.setattr(gi_lookup, "_local_paths", lambda: [out])
    gi_lookup.reload()
    assert gi_lookup.active_table_info()["edition"] == 2008
    build_gi_data.build_table([tmp_path / "a.pdf", tmp_path / "b.pdf"], out)
    assert gi_lookup.active_table_info()["edition"] == 2021
    gi_lookup.reload()


def test_background_build_reports_its_outcome(tmp_path, monkeypatch) -> None:
    _stub_pdfs(monkeypatch, {"a.pdf": 1, "b.pdf": 1})
    scratch = tmp_path / "uploads"
    scratch.mkdir()
    assert build_gi_data.start_build([tmp_path / "a.pdf", tmp_path / "b.pdf"],
                                     tmp_path / "out.json", cleanup_dir=scratch)
    for _ in range(200):
        if not build_gi_data.build_status()["running"]:
            break
        time.sleep(0.01)
    status = build_gi_data.build_status()
    assert status["error"] and "Both files are Supplemental Table 1" in status["error"]
    assert not scratch.exists()          # uploads removed either way
    build_gi_data.clear_status()
    assert build_gi_data.build_status()["error"] is None
