"""
Shared fixtures for the numa test suite.

Key fixtures:
  use_test_db       — autouse; redirects all db.get_db() calls to a per-test
                      temp database so tests never touch ~/.local/share/numa/numa.db
  use_test_profile  — autouse; redirects profile._PROFILES_DIR/_ACTIVE_NAME_FILE to temp paths
  no_off            — autouse; stubs Open Food Facts search/barcode lookup
  no_cnf            — autouse; stubs Canadian Nutrient File search/detail lookup
  db_conn           — direct sqlite3 connection to the temp DB for assertions
  cached_food       — inserts SAMPLE_FOOD_DETAIL into the temp DB cache; use this
                      in any test that needs a food available without hitting the API
"""

import json
import pathlib
import sqlite3

import pytest

import db as _db
import profile as _profile
import usda as _usda


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
    # Essential amino acids (chicken breast values per 100g, USDA FDC 171477)
    # aa_tyrosine_g and aa_cystine_g included so Phe+Tyr and Met+Cys pairs
    # score correctly against the updated FAO 2013 combined-pair references.
    "aa_tryptophan_g":    0.38,
    "aa_threonine_g":     1.38,
    "aa_isoleucine_g":    1.49,
    "aa_leucine_g":       2.42,
    "aa_lysine_g":        2.78,
    "aa_methionine_g":    0.89,
    "aa_cystine_g":       0.36,
    "aa_phenylalanine_g": 1.19,
    "aa_tyrosine_g":      1.01,
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


def _mock_api(monkeypatch: pytest.MonkeyPatch):
    """
    Patch out both USDA API functions.
    search_foods returns SAMPLE_SEARCH_RESULTS.
    get_food_detail returns SAMPLE_FOOD_DETAIL.
    get_api_key returns a dummy key so _ensure_api_key() passes immediately.
    """
    monkeypatch.setattr(_usda, "search_foods", lambda *a, **kw: SAMPLE_SEARCH_RESULTS)
    monkeypatch.setattr(_usda, "get_food_detail", lambda *a, **kw: SAMPLE_FOOD_DETAIL)
    monkeypatch.setattr(_usda, "get_api_key", lambda: "TESTKEY123")


# ---------------------------------------------------------------------------
# Database isolation
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_path(tmp_path: pathlib.Path) -> pathlib.Path:
    """A fresh temporary database file, initialized with the numa schema."""
    path = tmp_path / "test_numa.db"
    original = _db._DB_PATH
    _db._DB_PATH = path
    _db.init_db()
    _db._DB_PATH = original
    return path


@pytest.fixture(autouse=True)
def use_test_db(db_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Redirect every db.get_db() call to the per-test temp database.
    Applied automatically to every test.
    """
    monkeypatch.setattr(_db, "_DB_PATH", db_path)


@pytest.fixture(autouse=True)
def use_test_profile(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Redirect profile storage to per-test temp directories so tests never
    read or write the real ~/.config/numa/ profile files.
    Applied automatically to every test.
    """
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    active_file = tmp_path / "active_profile.txt"
    legacy_file = tmp_path / "profile.json"  # prevent migration from real legacy file
    monkeypatch.setattr(_profile, "_PROFILES_DIR", profiles_dir)
    monkeypatch.setattr(_profile, "_ACTIVE_NAME_FILE", active_file)
    monkeypatch.setattr(_profile, "_LEGACY_FILE", legacy_file)
    # Pre-populate a Default profile so load_profile() returns a valid object.
    default_profile = _profile.UserProfile(
        age=35, sex="male", weight_kg=75.0, height_cm=178.0,
        activity_level="moderate", name="Default",
    )
    import dataclasses, json as _json
    (profiles_dir / "Default.json").write_text(
        _json.dumps(dataclasses.asdict(default_profile), indent=2) + "\n"
    )


@pytest.fixture(autouse=True)
def no_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Stub out Open Food Facts search/barcode lookup to return no results so
    tests never hit the network and OFF results don't appear in search output
    or affect pick ordering. Applied automatically to every test.
    """
    import openfoodfacts as _off
    monkeypatch.setattr(_off, "search_foods", lambda *a, **kw: [])
    monkeypatch.setattr(_off, "lookup_by_barcode", lambda *a, **kw: None)


@pytest.fixture(autouse=True)
def no_cnf(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Stub out Canadian Nutrient File search/detail lookup to return no results
    so tests never hit the network and CNF results don't appear in search
    output or affect pick ordering. Applied automatically to every test —
    same role as no_off above.
    """
    import cnf_api as _cnf
    monkeypatch.setattr(_cnf, "search_foods", lambda *a, **kw: [])
    monkeypatch.setattr(_cnf, "get_food_detail_by_id", lambda *a, **kw: None)


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
