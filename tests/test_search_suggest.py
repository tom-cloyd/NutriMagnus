"""
Tests for numa_app/services/search_suggest.py — "did you mean" suggestions
for a food/recipe search that returned no results.
"""
from numa_app.services import search_suggest


def test_suggest_corrects_a_word_against_the_bundled_static_datasets(db_conn) -> None:
    # "broccoli" appears in the bundled CoFID/AFCD/CIQUAL name lists, so this
    # needs nothing cached locally to work — a fresh install still helps.
    assert "broccoli" in search_suggest.suggest(db_conn, "brocoli")


def test_suggest_corrects_a_word_against_a_locally_cached_food(db_conn) -> None:
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json) VALUES (?, ?, ?, ?)",
        (700001, "Triscuit Original Crackers", "Branded", "{}"),
    )
    db_conn.commit()
    assert "triscuit" in search_suggest.suggest(db_conn, "trisket")


def test_suggest_preserves_other_words_in_a_multi_word_query(db_conn) -> None:
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json) VALUES (?, ?, ?, ?)",
        (700002, "Chicken Breast", "Foundation", "{}"),
    )
    db_conn.commit()
    assert "chicken breast" in search_suggest.suggest(db_conn, "chiken breast")


def test_suggest_corrects_two_misspelled_words_at_once(db_conn) -> None:
    # Fixing only one of two typos would still leave a broken re-search, so
    # the top suggestion must correct both words in the same string.
    db_conn.execute(
        "INSERT INTO foods (fdc_id, name, data_type, nutrients_json) VALUES (?, ?, ?, ?)",
        (700003, "Triscuit Original Crackers", "Branded", "{}"),
    )
    db_conn.commit()
    assert "triscuit original" == search_suggest.suggest(db_conn, "triskitt originle")[0]


def test_suggest_returns_nothing_for_a_blank_query(db_conn) -> None:
    assert search_suggest.suggest(db_conn, "") == []
    assert search_suggest.suggest(db_conn, "   ") == []


def test_suggest_returns_nothing_when_every_word_is_already_known(db_conn) -> None:
    # "salmon" is a real word in the bundled datasets — no correction to offer.
    assert search_suggest.suggest(db_conn, "salmon") == []


def test_suggest_respects_the_limit(db_conn) -> None:
    assert len(search_suggest.suggest(db_conn, "brocoli", limit=1)) <= 1
