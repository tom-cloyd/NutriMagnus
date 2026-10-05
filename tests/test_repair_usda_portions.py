"""scripts/repair_usda_portions.py: correcting portions an older NuMa misread
from USDA (SR Legacy amounts dropped, Foundation portions dropped), without
touching the user's own portions or making a food count as user-edited."""
import json
import sys
from pathlib import Path

import pytest

import db as _db
import usda as _usda

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import repair_usda_portions as repair  # noqa: E402

# Real shapes: broccoli, cooked (SR Legacy 168510) and sugars, granulated (Foundation 746784).
BROCCOLI_RAW = [
    {"amount": 1.0, "modifier": "spear (about 5\" long)", "gramWeight": 37.0, "measureUnit": {"name": "undetermined"}},
    {"amount": 0.5, "modifier": "cup, chopped", "gramWeight": 78.0, "measureUnit": {"name": "undetermined"}},
]
SUGAR_RAW = [
    {"amount": 1.0, "modifier": None, "gramWeight": 188.0, "measureUnit": {"name": "cup"}},
    {"amount": 1.0, "modifier": None, "gramWeight": 8.0, "measureUnit": {"name": "RACC"}},
]


def test_renames_misread_portion_and_keeps_users_own():
    stored = [{"description": "spear (about 5\" long)", "gram_weight": 37.0},
              {"description": "cup, chopped", "gram_weight": 78.0},
              {"description": "1 cup", "gram_weight": 150.0}]          # the user's own
    assert repair.repaired(stored, BROCCOLI_RAW) == [
        {"description": "spear (about 5\" long)", "gram_weight": 37.0},
        {"description": "0.5 cup, chopped", "gram_weight": 78.0},
        {"description": "1 cup", "gram_weight": 150.0},
    ]


def test_user_edited_weight_is_not_renamed():
    stored = [{"description": "cup, chopped", "gram_weight": 156.0}]   # user fixed the grams
    assert repair.repaired(stored, BROCCOLI_RAW) is None


def test_adds_dropped_foundation_portions_and_is_idempotent():
    fixed = repair.repaired(None, SUGAR_RAW)
    assert fixed == [{"description": "1 cup", "gram_weight": 188.0}]
    assert repair.repaired(fixed, SUGAR_RAW) is None


def test_apply_fixes_portions_and_source_without_marking_edited(monkeypatch: pytest.MonkeyPatch):
    with _db.get_db() as conn:
        _db.cache_food(conn, 168510, "Broccoli test", "SR Legacy", None, 100.0, "g",
                       {"calories": 35.0}, [{"description": "cup, chopped", "gram_weight": 78.0}])
        _db.snapshot_food_source(conn, 168510)
        assert not conn.execute("SELECT user_edited FROM foods WHERE fdc_id = 168510").fetchone()[0]
    monkeypatch.setattr(_usda, "get_food_portions_raw", lambda fid: BROCCOLI_RAW if fid == 168510 else [])
    monkeypatch.setattr(repair.shutil, "copy2", lambda *a, **k: None)
    assert repair.main(["--apply"]) == 0
    with _db.get_db() as conn:
        row = conn.execute("SELECT portions_json, source_json, user_edited FROM foods WHERE fdc_id = 168510").fetchone()
    assert json.loads(row["portions_json"])[0]["description"] == "0.5 cup, chopped"
    assert json.loads(row["source_json"])["portions"][0]["description"] == "0.5 cup, chopped"
    assert not row["user_edited"]
