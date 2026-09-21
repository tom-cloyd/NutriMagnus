"""
Tests for gi_lookup.py — fuzzy name search over the bundled Foster-Powell
glycemic index reference table.
"""
import gi_lookup


def test_search_finds_a_known_food_on_the_glucose_scale() -> None:
    results = gi_lookup.search("banana", population="both")
    assert results
    assert all("gi_glucose" in r and 0 <= r["gi_glucose"] <= 130 for r in results)


def test_search_respects_population_filter() -> None:
    normal_only = gi_lookup.search("white bread", population="normal")
    assert normal_only
    assert all(r["population"] == "normal" for r in normal_only)


def test_search_returns_multiple_candidates_not_just_one() -> None:
    results = gi_lookup.search("lentils", population="both")
    assert len(results) > 1


def test_search_blank_query_returns_nothing() -> None:
    assert gi_lookup.search("", population="both") == []


def test_search_nonsense_query_returns_nothing() -> None:
    assert gi_lookup.search("zzzqqqxxx99nonsense", population="both") == []
