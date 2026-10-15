"""
Tests for gi_lookup.py — fuzzy name search over the bundled Atkinson
glycemic index reference table.
"""
import json

import gi_lookup


def test_search_finds_a_known_food_on_the_glucose_scale() -> None:
    results = gi_lookup.search("banana", population="both")
    assert results
    # Published GI values do exceed 100 on the glucose scale (sucrose reaches
    # 132 in one study in these tables), so the bound is only a sanity check.
    assert all("gi_glucose" in r and 0 <= r["gi_glucose"] <= 200 for r in results)


def test_search_respects_population_filter() -> None:
    normal_only = gi_lookup.search("white bread", population="normal")
    assert normal_only
    # Rows whose subject group the source left unstated are returned for either
    # population rather than withheld from both, so "normal" means "normal or
    # unstated" — never impaired.
    assert all(r["population"] in ("normal", "unknown") for r in normal_only)


def test_search_never_returns_the_other_population() -> None:
    for population, forbidden in (("normal", "impaired"), ("impaired", "normal")):
        for query in ("bread", "rice", "potato"):
            results = gi_lookup.search(query, population=population)
            assert all(r["population"] != forbidden for r in results), (
                f"{population} search for {query!r} leaked a {forbidden} row"
            )


def test_search_reports_edition_and_year_of_test() -> None:
    """Every candidate must say which edition it came from, and 2021 rows must
    carry the study's own year — that is the date shown in the picker."""
    results = gi_lookup.search("bread", population="both", limit=40)
    assert results
    assert all(r["edition"] in (2008, 2021) for r in results)
    for row in results:
        if row["edition"] == 2008:
            # The 2008 extraction never captured a year, and the edition year is
            # not a measurement date, so it must stay empty rather than be filled in.
            assert row["year"] is None
            assert row["iso"] is None


def _active_rows() -> list[dict]:
    """Every row of whichever table is actually in use — the bundled 2008
    baseline in a clean checkout, or a locally-built 2021 table if the developer
    running the suite has made one. Both configurations must pass."""
    path = gi_lookup.active_table_path()
    assert path is not None, "no GI table found at all"
    data = json.loads(path.read_text(encoding="utf-8"))
    return [r for pool in data.values() for r in pool]


def test_every_row_has_the_fields_the_picker_displays() -> None:
    fields = ("name", "gi_glucose", "sem", "year", "country", "population",
              "subjects_type", "subjects_n", "category", "iso", "edition", "ref")
    rows = _active_rows()
    assert len(rows) > 2000, "expected at least the bundled 2008 baseline"
    for row in rows:
        missing = [f for f in fields if f not in row]
        assert not missing, f"{row.get('name')!r} missing {missing}"
        assert row["gi_glucose"] is not None
        assert row["population"] in ("normal", "impaired", "unknown")


def test_bundled_baseline_is_the_2008_edition_only() -> None:
    """NuMa ships the Creative Commons 2008 table. The 2021 edition forbids
    redistribution, so a table built from it must never reach gi_data.json —
    scripts/build_gi_data.py writes gi_data_local.json instead."""
    data = json.loads(gi_lookup._DATA_PATH.read_text(encoding="utf-8"))
    rows = [r for pool in data.values() for r in pool]
    assert rows
    assert {r["edition"] for r in rows} == {2008}, (
        "gi_data.json contains rows from an edition other than 2008 — it must "
        "not be built from the 2021 tables, whose licence forbids redistributing "
        "them. Build to gi_data_local.json instead."
    )
    # That edition published no year of test, and the edition year is not a
    # measurement date, so none may be invented for these rows.
    assert all(r["year"] is None for r in rows)


def test_iso_consistent_rows_all_report_a_standard_error() -> None:
    """Supplemental Table 1 of the 2021 edition publishes a SEM for every row it
    contains; only the method-deviation table has rows carrying a bare GI. Skipped
    unless a locally-built 2021 table is present."""
    iso_rows = [r for r in _active_rows() if r["edition"] == 2021 and r["iso"]]
    if not iso_rows:
        return                      # 2008 baseline only: nothing to check
    assert all(r["sem"] is not None for r in iso_rows)


def test_a_local_2021_table_keeps_legacy_rows_to_a_minority() -> None:
    """When a 2021 table has been built, the 2008 rows it carries forward are
    only what 2021 does not cover. A large legacy tier would mean the name
    matching in the merge had stopped working."""
    rows = _active_rows()
    if not any(r["edition"] == 2021 for r in rows):
        return                      # 2008 baseline only: the merge never ran
    legacy = [r for r in rows if r["edition"] == 2008]
    assert 0 < len(legacy) < 0.2 * len(rows)


def test_a_local_table_supersedes_the_bundled_one() -> None:
    """gi_data_local.json, when the user has built it, is what gets searched —
    the builder folds the uncovered 2008 rows into its own output, so the two
    are not merged at read time."""
    local = gi_lookup.Path(gi_lookup.__file__).parent / gi_lookup._LOCAL_NAME
    if local.exists():
        assert gi_lookup.active_table_path() != gi_lookup._DATA_PATH
    else:
        assert gi_lookup.active_table_path() == gi_lookup._DATA_PATH


def test_active_table_info_reports_which_edition_is_in_use() -> None:
    """The Annotate page and Settings both show this, so that a locally-built
    2021 table's presence — and its silent absence — is visible rather than
    guessed at. Must be right in either configuration."""
    info = gi_lookup.active_table_info()
    rows = _active_rows()
    assert info["rows"] == len(rows)
    assert info["rows_2021"] + info["rows_2008"] == info["rows"]
    assert info["normal"] + info["impaired"] + info["unknown"] == info["rows"]
    assert info["path"] == str(gi_lookup.active_table_path())
    if gi_lookup.active_table_path() == gi_lookup._DATA_PATH:
        assert info["edition"] == 2008 and not info["is_local"]
        assert info["rows_2021"] == 0
    else:
        assert info["edition"] == 2021 and info["is_local"]
        assert info["rows_2021"] > info["rows_2008"]


def test_active_table_info_survives_having_no_table_at_all(monkeypatch) -> None:
    """A missing gi_data.json must produce a reportable state, not an
    exception — Settings says so outright rather than the page failing."""
    monkeypatch.setattr(gi_lookup, "active_table_path", lambda: None)
    monkeypatch.setattr(gi_lookup, "_data_cache", None)
    info = gi_lookup.active_table_info()
    assert info["path"] is None and info["edition"] is None
    assert info["rows"] == 0


def test_local_table_candidates_are_ordered_data_dir_first() -> None:
    """A packaged install cannot write beside the module, so the data directory
    has to be searched first for Settings to point a user anywhere useful."""
    paths = gi_lookup.local_table_candidates()
    assert paths
    assert all(p.endswith(gi_lookup._LOCAL_NAME) for p in paths)
    assert str(gi_lookup.Path(gi_lookup.__file__).parent) in paths[-1]


def test_plain_ingredient_ranks_above_dishes_that_contain_it(monkeypatch) -> None:
    """Every name containing the query ties on score, so a common ingredient
    must not be buried under dish names that merely mention it."""
    def row(name):
        return {"name": name, "gi_glucose": 50.0, "population": "normal"}
    rows = [row("Sponge cake, soft wheat flour, filled with chocolate cream"),
            row("Muffin, plain, made from wheat flour"),
            row("White wheat flour bread, hard, toasted"),
            row("Wheat flour bread, wholemeal, stoneground"),
            row("Wheat flour, raw, consumed suspended in 250 mL water")]
    monkeypatch.setattr(gi_lookup, "_data_cache",
                        {"normal": rows, "impaired": [], "unknown": []})
    names = [r["name"] for r in gi_lookup.search("wheat flour", limit=5)]
    assert names == ["Wheat flour, raw, consumed suspended in 250 mL water",
                     "Wheat flour bread, wholemeal, stoneground",
                     "White wheat flour bread, hard, toasted",
                     "Muffin, plain, made from wheat flour",
                     "Sponge cake, soft wheat flour, filled with chocolate cream"]


def _fake_table(monkeypatch, names):
    rows = [{"name": n, "gi_glucose": 50.0, "population": "normal"} for n in names]
    monkeypatch.setattr(gi_lookup, "_data_cache",
                        {"normal": rows, "impaired": [], "unknown": []})


def test_branded_rows_rank_below_generic_ones_on_equal_score(monkeypatch) -> None:
    _fake_table(monkeypatch, ["Peanut Butter Chocolate bar (Beachbody, LLC)",
                              "Munch Peanut Butter bar (M&M/Mars, USA)",
                              "Biscuits, wholegrain, filled with peanut butter"])
    names = [r["name"] for r in gi_lookup.search("peanut butter")]
    assert names[0] == "Biscuits, wholegrain, filled with peanut butter"


def test_is_branded_tells_a_product_from_a_described_food() -> None:
    assert gi_lookup.is_branded("Munch Peanut Butter bar (M&M/Mars, USA)")
    assert gi_lookup.is_branded("Chocapic™, wheat-based flaked cereal")
    assert gi_lookup.is_branded("Kingston cookies (Arnott’s Pty Ltd, Australia)")
    assert not gi_lookup.is_branded("Peanuts (Canada)4")
    assert not gi_lookup.is_branded("Lentil (Lens culinaris medic, S. massoor parippu) curry")
    assert not gi_lookup.is_branded("Barley (six-rowed, hulled, normal barley), boiled")


def test_direct_match_means_a_row_is_the_food_itself() -> None:
    rows = [{"name": n} for n in ("Biscuits, filled with peanut butter", "Peanuts",
                                  "Bread, white", "Cornflakes")]
    def direct(q):
        return gi_lookup.has_direct_match(q, rows)
    assert not direct("peanut butter")
    assert direct("peanut")          # plural on the row
    assert direct("white bread")     # word order
    assert direct("corn flakes")     # run together on the row


def test_stand_ins_offer_plain_rows_for_each_word(monkeypatch) -> None:
    _fake_table(monkeypatch, ["Biscuits, filled with peanut butter",
                              "Peanuts, crushed", "Peanuts", "Peanut Butter bar (Mars, USA)"])
    groups = gi_lookup.stand_ins("peanut butter")
    assert [g["word"] for g in groups] == ["peanut"]
    assert [r["name"] for r in groups[0]["rows"]] == ["Peanuts", "Peanuts, crushed"]
    assert gi_lookup.stand_ins("peanut") == []      # a one-word search has no parts
    assert gi_lookup.stand_ins("peanut butter", exclude=("Peanuts", "Peanuts, crushed")) == []


def test_a_usda_style_name_is_matched_by_its_words(monkeypatch) -> None:
    """A long comma-separated name resembles no row as a whole string; its
    first part is the food, the rest describe it."""
    _fake_table(monkeypatch, ["Cassava, boiled, with salt",
                              "Peas, dried, boiled", "Chickpeas", "Pea, frozen",
                              "Almond bar (Mars, USA)", "Apricot and Almond bar"])
    names = [r["name"] for r in gi_lookup.search(
        "Peas, split, mature seeds, cooked, boiled, without salt")]
    assert names == ["Peas, dried, boiled", "Pea, frozen"]
    # A category first ("Nuts,") gives way to the food named second; generic
    # rows come before branded ones.
    names = [r["name"] for r in gi_lookup.search("Nuts, almonds, dry roasted")]
    assert names == ["Apricot and Almond bar", "Almond bar (Mars, USA)"]
    # No row has every word of the first part: its first word alone is tried.
    assert [r["name"] for r in gi_lookup.search("Chickpeas flour, raw")] == ["Chickpeas"]
