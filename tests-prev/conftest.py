"""
Shared fixtures for the numa test suite.

Key fixtures:
  use_test_db   — autouse; redirects all db.get_db() calls to a per-test
                  temp database so tests never touch ~/.local/share/numa/numa.db
  db_conn       — direct sqlite3 connection to the temp DB for assertions
  runner        — typer CliRunner with wide terminal (no truncated tables)
  sample_food   — a realistic food dict in our internal format
  cached_food   — inserts sample_food into the temp DB cache; use this in
                  any test that needs a food available without hitting the API
"""

import json
import pathlib
import sqlite3

import pytest
from typer.testing import CliRunner

import db as _db
import profile as _profile


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_NUTRIENTS: dict = {
    "calories":        165.0,
    "protein_g":       31.0,
    "carbs_g":          0.0,
    "fat_g":            3.6,
    "fiber_g":          0.0,
    "sugar_g":          0.0,
    "saturated_fat_g":  1.0,
    "calcium_mg":      15.0,
    "iron_mg":          1.0,
    "potassium_mg":   256.0,
    "sodium_mg":       74.0,
    "vitamin_c_mg":     0.0,
    "vitamin_d_mcg":    0.1,
    # Essential amino acids (chicken breast values per 100g)
    "aa_tryptophan_g":    0.38,
    "aa_threonine_g":     1.38,
    "aa_isoleucine_g":    1.49,
    "aa_leucine_g":       2.42,
    "aa_lysine_g":        2.78,
    "aa_methionine_g":    0.89,
    "aa_phenylalanine_g": 1.19,
    "aa_valine_g":        1.58,
    "aa_histidine_g":     0.90,
}

SAMPLE_FDC_ID = 171477

# What usda.search_foods() returns (list of USDA search result objects)
SAMPLE_SEARCH_RESULTS: list[dict] = [
    {
        "fdcId":       SAMPLE_FDC_ID,
        "description": "Chicken, broilers or fryers, breast, meat only, raw",
        "dataType":    "SR Legacy",
        "brandOwner":  None,
    }
]

# What usda.get_food_detail() returns (our normalized dict)
SAMPLE_FOOD_DETAIL: dict = {
    "fdcId":           SAMPLE_FDC_ID,
    "name":            "Chicken, broilers or fryers, breast, meat only, raw",
    "dataType":        "SR Legacy",
    "brand":           None,
    "servingSize":     100.0,
    "servingUnit":     "g",
    "householdServing":"1 breast",
    "nutrients":       SAMPLE_NUTRIENTS,
    "portions":        [{"description": "1 breast", "gram_weight": 174.0}],
}

# A second food for sum / combination tests
SAMPLE_NUTRIENTS_2: dict = {
    "calories":     89.0,
    "protein_g":     1.1,
    "carbs_g":      23.0,
    "fat_g":         0.3,
    "fiber_g":       2.6,
    "sugar_g":      12.2,
    "potassium_mg": 358.0,
    "vitamin_c_mg":  8.7,
}


# ---------------------------------------------------------------------------
# Database isolation
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_path(tmp_path: pathlib.Path) -> pathlib.Path:
    """A fresh temporary database file, initialized with the numa schema."""
    path = tmp_path / "test_numa.db"
    # Temporarily override the module-level path so init_db writes here
    original = _db._DB_PATH
    _db._DB_PATH = path
    _db.init_db()
    _db._DB_PATH = original
    return path


@pytest.fixture(autouse=True)
def use_test_db(db_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Redirect every db.get_db() call to the per-test temp database.
    Also patch get_db_path() so Settings menu shows the temp path.
    Applied automatically to every test.
    """
    monkeypatch.setattr(_db, "_DB_PATH", db_path)


@pytest.fixture(autouse=True)
def use_test_profile(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Redirect profile._PROFILE_FILE to a per-test temp path so tests never
    read or write the real ~/.config/numa/profile.json.
    Applied automatically to every test.
    """
    monkeypatch.setattr(_profile, "_PROFILE_FILE", tmp_path / "test_profile.json")


# ---------------------------------------------------------------------------
# Direct DB connection for assertions
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_conn(db_path: pathlib.Path):
    """Raw sqlite3.Row connection for direct DB assertions inside tests."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# CLI runner
# ---------------------------------------------------------------------------

@pytest.fixture()
def runner() -> CliRunner:
    """Typer test runner with a wide terminal so tables aren't truncated."""
    return CliRunner(env={"COLUMNS": "200"})


# ---------------------------------------------------------------------------
# Food fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def cached_food(db_conn: sqlite3.Connection) -> dict:
    """
    Insert SAMPLE_FOOD_DETAIL into the food cache and return it.
    Use this in any test that needs a real food in the DB without an API call.
    """
    f = SAMPLE_FOOD_DETAIL
    db_conn.execute("""
        INSERT OR REPLACE INTO foods
            (fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (f["fdcId"], f["name"], f["dataType"], f["brand"],
          f["servingSize"], f["servingUnit"],
          json.dumps(f["nutrients"]), json.dumps(f["portions"])))
    db_conn.commit()
    return f
