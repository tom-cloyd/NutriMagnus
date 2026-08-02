"""
Shared fixtures for the numa test suite.

Key fixtures:
  use_test_db       — autouse; redirects all db.get_db() calls to a per-test
                      temp database so tests never touch ~/.local/share/numa/numa.db
  use_test_profile  — autouse; redirects profile._PROFILES_DIR/_ACTIVE_NAME_FILE to temp paths
  use_test_prefs    — autouse; pre-populates a temp prefs file and patches both
                      prefs._PREFS_FILE and main._PREFS_FILE so _load_prefs()
                      and the main menu guard both see the temp file
  no_export         — autouse; stubs _offer_export to a no-op so tests don't
                      write real files to ~/.numa/reports/ and don't need extra
                      input lines to decline the export prompt
  db_conn           — direct sqlite3 connection to the temp DB for assertions
  runner            — NumaTestRunner: invoke run_app() with captured I/O
  cached_food       — inserts SAMPLE_FOOD_DETAIL into the temp DB cache; use this
                      in any test that needs a food available without hitting the API
"""

import io
import json
import pathlib
import sqlite3

import pytest

import db as _db
import profile as _profile


def nutrient_target_menu_index(key: str) -> str:
    """Return the 1-based menu index (as a string) for `key` in the Settings →
    Nutrient targets list, computed from the live group definitions so tests
    don't hardcode numbers that silently go stale whenever a nutrient is added
    to numa_app.workflows.settings._NUTRIENT_TARGET_GROUPS."""
    from numa_app.workflows.settings import _NUTRIENT_TARGET_GROUPS
    idx = 1
    for _group_name, keys in _NUTRIENT_TARGET_GROUPS:
        for k in keys:
            if k == key:
                return str(idx)
            idx += 1
    raise KeyError(f"{key!r} not found in _NUTRIENT_TARGET_GROUPS")


def meal_column_menu_index(key: str) -> str:
    """Return the 1-based menu index (as a string) for `key` in the Settings ->
    Meals & Log columns picker, computed from the live group definitions
    (same groups as nutrient_target_menu_index, minus 'calories' which that
    screen doesn't offer)."""
    from numa_app.workflows.settings import _NUTRIENT_TARGET_GROUPS
    idx = 1
    for _group_name, keys in _NUTRIENT_TARGET_GROUPS:
        for k in keys:
            if k == "calories":
                continue
            if k == key:
                return str(idx)
            idx += 1
    raise KeyError(f"{key!r} not found in meal-columns picker")


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


# ---------------------------------------------------------------------------
# NumaTestRunner
# ---------------------------------------------------------------------------

class NumaResult:
    def __init__(self, output: str, exit_code: int):
        self.output = output
        self.exit_code = exit_code


class NumaTestRunner:
    """
    Invoke run_app() with captured I/O, no real tty.

    When sys.stdin is not a tty, _prompt() falls back to rich Prompt.ask()
    which calls input() — reading from whatever sys.stdin points to.
    We replace sys.stdin with io.StringIO(input) and redirect the rich
    Console to a StringIO buffer to capture all output.
    """

    def invoke(self, input: str = "", *, api_key=None, theme=None) -> NumaResult:
        import sys
        from rich.console import Console
        from numa_app import state
        from numa_app.main import run_app

        buf = io.StringIO()
        new_console = Console(file=buf, highlight=False, force_terminal=False, width=200)
        old_stdin = sys.stdin
        old_console = state.app_ctx.console
        exit_code = 0
        try:
            sys.stdin = io.StringIO(input)
            state.app_ctx.console = new_console
            state.sync_globals()
            run_app(theme=theme, api_key=api_key)
        except SystemExit as e:
            exit_code = e.code if isinstance(e.code, int) else 0
        finally:
            sys.stdin = old_stdin
            state.app_ctx.console = old_console
            state.sync_globals()
        return NumaResult(buf.getvalue(), exit_code)


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
def use_test_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Pre-populate a temp prefs file and patch both prefs._PREFS_FILE and
    main._PREFS_FILE so that initialize_app() never shows the first-run
    animal foods prompt and _load_prefs() reads from the temp file.
    Applied automatically to every test.
    """
    from numa_app.config import prefs as _prefs
    from numa_app import main as _main

    prefs_file = tmp_path / "test_prefs.json"
    prefs_file.write_text(json.dumps({"include_animal_foods": True}))
    monkeypatch.setattr(_prefs, "_PREFS_FILE", prefs_file)
    monkeypatch.setattr(_main, "_PREFS_FILE", prefs_file)


@pytest.fixture(autouse=True)
def no_export(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Stub out _offer_export to a no-op so tests never write real report files
    and don't need extra input lines to decline the export prompt.
    Applied automatically to every test.
    """
    from numa_app.services import reports as _reports
    monkeypatch.setattr(_reports, "_offer_export", lambda *a, **kw: None)


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
def runner() -> NumaTestRunner:
    """NumaTestRunner: invokes run_app() with captured stdin/stdout."""
    return NumaTestRunner()


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
