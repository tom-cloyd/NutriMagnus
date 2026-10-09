"""
Tests for scripts/restore_usda_zeros.py — the one-time repair that gives
cached USDA foods back the zeros USDA measured (dropped by usda_api before
2026-10-09).
"""
import json
import sys
from pathlib import Path

import db as _db

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import restore_usda_zeros as restore  # noqa: E402


def test_zeros_to_add_only_fills_absent_keys():
    current = {"protein_g": 10.0, "iron_mg": 2.0, "sodium_mg": 0.0}
    incoming = {"protein_g": 0.0, "iron_mg": 2.5, "sodium_mg": 0.0, "b12_mcg": 0.0, "fat_g": 1.0}
    # protein: the food has a value (USDA's 0 doesn't replace it); iron: not
    # a zero; sodium: already 0; fat: non-zero, left for Refresh.
    assert restore.zeros_to_add(current, incoming) == {"b12_mcg": 0.0}


def _food(fdc_id, nutrients, from_source=True):
    with _db.get_db() as conn:
        _db.cache_food(conn, fdc_id, f"Food {fdc_id}", "SR Legacy", None, 100.0, "g", nutrients,
                       from_source=from_source)


def _row(fdc_id):
    with _db.get_db() as conn:
        r = conn.execute("SELECT nutrients_json, source_json, user_edited FROM foods WHERE fdc_id = ?",
                         (fdc_id,)).fetchone()
    return json.loads(r[0]), (json.loads(r[1]) if r[1] else None), r[2]


def test_report_only_changes_nothing(capsys):
    _food(168917, {"protein_g": 4.4})
    assert restore.main([], fetch=lambda i: {"nutrients": {"protein_g": 4.4, "b12_mcg": 0.0}}) == 0
    assert _row(168917)[0] == {"protein_g": 4.4}
    assert "1 food(s) would get their zeros back" in capsys.readouterr().out


def test_apply_adds_zeros_to_food_and_source_without_marking_edited():
    _food(168917, {"protein_g": 4.4, "iron_mg": 1.5})
    restore.main(["--apply"], fetch=lambda i: {"nutrients": {"protein_g": 4.4, "iron_mg": 1.5,
                                                             "b12_mcg": 0.0, "vitamin_d_mcg": 0.0}})
    nutrients, source, edited = _row(168917)
    assert nutrients == {"protein_g": 4.4, "iron_mg": 1.5, "b12_mcg": 0.0, "vitamin_d_mcg": 0.0}
    assert source["nutrients"]["b12_mcg"] == 0.0
    assert not edited


def test_apply_never_touches_a_users_edit():
    _food(173796, {"protein_g": 9.0})
    with _db.get_db() as conn:   # the user edits iron in
        conn.execute("UPDATE foods SET nutrients_json = ? WHERE fdc_id = 173796",
                     (json.dumps({"protein_g": 9.0, "iron_mg": 7.0}),))
        _db.refresh_user_edited(conn, 173796)
    restore.main(["--apply"], fetch=lambda i: {"nutrients": {"protein_g": 9.0, "iron_mg": 0.0, "b12_mcg": 0.0}})
    nutrients, _source, edited = _row(173796)
    assert nutrients["iron_mg"] == 7.0 and nutrients["b12_mcg"] == 0.0
    assert edited   # still user-edited, because of the iron


def test_a_failed_lookup_is_reported_and_skipped(capsys):
    _food(168917, {"protein_g": 4.4})
    def boom(i):
        raise OSError("rate limited")
    restore.main(["--apply"], fetch=boom)
    assert _row(168917)[0] == {"protein_g": 4.4}
    assert "lookup failed" in capsys.readouterr().out


def test_non_usda_foods_are_not_looked_up():
    _food(-5, {"protein_g": 1.0}, from_source=False)
    seen = []
    restore.main([], fetch=lambda i: seen.append(i) or {"nutrients": {}})
    assert -5 not in seen
