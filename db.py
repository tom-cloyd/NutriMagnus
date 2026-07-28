"""
db.py — SQLite database for numa nutritional analysis program.

Database location: ~/.local/share/numa/numa.db (Linux) / %LOCALAPPDATA%/numa/numa.db (Windows)
Docs: README-numa-documentation.md, Architecture: "db.py — SQLite database"
"""

import json
import pathlib
import re as _re
import sqlite3
from contextlib import contextmanager
from typing import Generator

import platform_utils as _platform_utils

_DB_PATH = _platform_utils.get_data_dir() / "numa.db"


def get_db_path() -> pathlib.Path:
    return _DB_PATH


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Yield a sqlite3.Connection; commits on clean exit, rolls back on exception.
    Never hold the connection across a _prompt() call — open, query, close, prompt, reopen."""
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create all tables if they don't already exist."""
    with get_db() as conn:
        conn.executescript("""
            
            CREATE TABLE IF NOT EXISTS foods (
                fdc_id      INTEGER PRIMARY KEY,
                name        TEXT    NOT NULL,
                data_type   TEXT,
                brand       TEXT,
                serving_size     REAL,
                serving_unit     TEXT,
                nutrients_json   TEXT    NOT NULL,
                portions_json    TEXT    DEFAULT 'null',
                user_drafted     INTEGER DEFAULT 0,
                notes            TEXT,
                curator_notes    TEXT,
                cached_at        TEXT    DEFAULT (datetime('now'))
            );
            
            CREATE TABLE IF NOT EXISTS recipes (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT    NOT NULL,
                description     TEXT,
                servings        INTEGER NOT NULL DEFAULT 1,
                serving_size    TEXT,
                complete        INTEGER NOT NULL DEFAULT 0,
                instructions    TEXT,
                dcp_g           REAL,
                dcp_computed_at TEXT,
                created_at      TEXT    DEFAULT (date('now'))
            );

            CREATE TABLE IF NOT EXISTS recipe_ingredients (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id     INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
                fdc_id        INTEGER NOT NULL,
                food_name     TEXT    NOT NULL,
                amount        REAL    NOT NULL,
                unit          TEXT    NOT NULL,
                notes         TEXT,
                ref_recipe_id INTEGER REFERENCES recipes(id),
                ref_recipe_deleted INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS meals (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                meal_date   TEXT    NOT NULL,
                complete    INTEGER NOT NULL DEFAULT 0,
                created_at  TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS meal_items (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id     INTEGER NOT NULL REFERENCES meals(id) ON DELETE CASCADE,
                item_type   TEXT    NOT NULL CHECK(item_type IN ('food', 'recipe')),
                fdc_id      INTEGER,
                recipe_id   INTEGER,
                food_name   TEXT    NOT NULL,
                amount      REAL    NOT NULL,
                unit        TEXT    NOT NULL,
                notes       TEXT
            );

            CREATE TABLE IF NOT EXISTS pantry (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name   TEXT    NOT NULL,
                fdc_id      INTEGER,
                notes       TEXT,
                added_at    TEXT    DEFAULT (date('now'))
            );

            CREATE TABLE IF NOT EXISTS diaas_overrides (
                food_name       TEXT    PRIMARY KEY,
                digestibility   REAL    NOT NULL CHECK(digestibility >= 0.0 AND digestibility <= 1.0),
                notes           TEXT,
                updated_at      TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS food_annotations (
                fdc_id          INTEGER PRIMARY KEY REFERENCES foods(fdc_id) ON DELETE CASCADE,
                gi_estimate     REAL,
                gi_no_prompt    INTEGER DEFAULT 0,
                diaas_estimate  REAL,
                diaas_no_prompt INTEGER DEFAULT 0,
                prep_context    TEXT,
                updated_at      TEXT    DEFAULT (datetime('now'))
            );
        """)
        # Migrate: add portions_json column if absent (pre-portions-feature DB)
        try:
            conn.execute("ALTER TABLE foods ADD COLUMN portions_json TEXT DEFAULT 'null'")
        except sqlite3.OperationalError:
            pass  # column already exists
        # Migrate: add dcp_g / dcp_computed_at / gl_g columns if absent
        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN dcp_g REAL")
        except sqlite3.OperationalError:
            pass  # column already exists
        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN dcp_computed_at TEXT")
        except sqlite3.OperationalError:
            pass  # column already exists
        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN gl_g REAL")
        except sqlite3.OperationalError:
            pass  # column already exists
        # Migrate: add total volume / weight columns if absent
        for _col in (
            "total_volume      REAL",
            "total_volume_unit TEXT",
            "total_weight      REAL",
            "total_weight_unit TEXT",
        ):
            try:
                conn.execute(f"ALTER TABLE recipes ADD COLUMN {_col}")
            except sqlite3.OperationalError:
                pass  # column already exists
        # Migrate: reset rows cached before portions were fetched so they re-fetch once.
        # '[]' with the old NOT NULL DEFAULT meant "never fetched"; 'null' now means the same.
        # Using JSON 'null' (not SQL NULL) so this works even on old NOT NULL columns.
        conn.execute("UPDATE foods SET portions_json = 'null' WHERE portions_json = '[]'")

        try:
            conn.execute("ALTER TABLE foods ADD COLUMN user_drafted INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        
        try:
            conn.execute("ALTER TABLE foods ADD COLUMN notes TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE foods ADD COLUMN curator_notes TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipe_ingredients ADD COLUMN notes TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipe_ingredients ADD COLUMN ref_recipe_id INTEGER REFERENCES recipes(id)")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipe_ingredients ADD COLUMN ref_recipe_deleted INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN serving_size TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN complete INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        
        try:
            conn.execute("ALTER TABLE meal_items ADD COLUMN notes TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE meals ADD COLUMN complete INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN last_accessed_at TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN saved_analysis_at TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN saved_analysis_text TEXT")
        except sqlite3.OperationalError:
            pass

        for _col in ("gi_no_prompt INTEGER DEFAULT 0", "diaas_no_prompt INTEGER DEFAULT 0"):
            try:
                conn.execute(f"ALTER TABLE food_annotations ADD COLUMN {_col}")
            except sqlite3.OperationalError:
                pass

        try:
            conn.execute("ALTER TABLE recipe_ingredients ADD COLUMN sort_order INTEGER")
        except sqlite3.OperationalError:
            pass

        conn.execute("""
            CREATE TABLE IF NOT EXISTS saved_comparisons (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                fdc_ids    TEXT    NOT NULL,
                amounts    TEXT    NOT NULL,
                created_at TEXT    DEFAULT (datetime('now'))
            )
        """)

        for _col in ("bcp_g REAL", "bcp_computed_at TEXT", "day_pct_goal REAL", "calories REAL",
                     "nutrients_snapshot_json TEXT"):
            try:
                conn.execute(f"ALTER TABLE meals ADD COLUMN {_col}")
            except sqlite3.OperationalError:
                pass

        conn.execute("""
            CREATE TABLE IF NOT EXISTS oxalate_links (
                fdc_id          INTEGER PRIMARY KEY REFERENCES foods(fdc_id) ON DELETE CASCADE,
                oxalate_food_id INTEGER,
                user_confirmed  INTEGER DEFAULT 0,
                confirmed_at    TEXT,
                no_match        INTEGER DEFAULT 0
            )
        """)

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN nutrients_json TEXT")
        except sqlite3.OperationalError:
            pass

        conn.execute("""
            CREATE TABLE IF NOT EXISTS day_bcp_cache (
                meal_date   TEXT PRIMARY KEY,
                dcp_g       REAL NOT NULL,
                computed_at TEXT DEFAULT (datetime('now'))
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS day_profile (
                meal_date    TEXT PRIMARY KEY,
                profile_name TEXT NOT NULL,
                profile_json TEXT NOT NULL,
                pinned_at    TEXT DEFAULT (datetime('now')),
                overridden   INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Migrate: add archived flag to foods/pantry/recipes (reserve/hide-without-losing feature)
        try:
            conn.execute("ALTER TABLE foods ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE pantry ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass

# ---------------------------------------------------------------------------
# Food cache
# ---------------------------------------------------------------------------

def cache_food(conn: sqlite3.Connection, fdc_id: int, name: str, data_type: str,
               brand: str | None, serving_size: float | None, serving_unit: str | None,
               nutrients: dict[str, float], portions: list[dict] | None = None,
               *, user_drafted: bool = False, notes: str | None = None,
               curator_notes: str | None = None) -> None:
    conn.execute("""
        INSERT OR REPLACE INTO foods
            (fdc_id, name, data_type, brand, serving_size, serving_unit,
             nutrients_json, portions_json, user_drafted, notes, curator_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        fdc_id, name, data_type, brand, serving_size, serving_unit,
        json.dumps(nutrients), json.dumps(portions or []),
        1 if user_drafted else 0, notes or None, curator_notes or None
    ))


def get_cached_food(conn: sqlite3.Connection, fdc_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM foods WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()


def list_cached_foods(conn: sqlite3.Connection, *, include_archived: bool = False) -> list[sqlite3.Row]:
    archived_clause = "" if include_archived else "WHERE archived = 0"
    return conn.execute(
        "SELECT fdc_id, name, data_type, brand, serving_size, serving_unit, "
        "nutrients_json, notes, curator_notes, archived "
        f"FROM foods {archived_clause} ORDER BY name"
    ).fetchall()


def delete_cached_food(conn: sqlite3.Connection, fdc_id: int) -> bool:
    """Delete a food from the cache. Returns True if a row was deleted."""
    cur = conn.execute("DELETE FROM foods WHERE fdc_id = ?", (fdc_id,))
    return cur.rowcount > 0


def set_food_archived(conn: sqlite3.Connection, fdc_id: int, archived: bool) -> None:
    """Archive (hide from search/complements/default lists, protect from prune) or restore a cached food."""
    conn.execute("UPDATE foods SET archived = ? WHERE fdc_id = ?", (1 if archived else 0, fdc_id))


def food_references(conn: sqlite3.Connection, fdc_id: int) -> dict[str, int]:
    """Return counts of pantry entries, recipe ingredients, and meal items still referencing this food."""
    pantry_n = conn.execute(
        "SELECT COUNT(*) FROM pantry WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()[0]
    recipe_n = conn.execute(
        "SELECT COUNT(*) FROM recipe_ingredients WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()[0]
    meal_n = conn.execute(
        "SELECT COUNT(*) FROM meal_items WHERE item_type = 'food' AND fdc_id = ?", (fdc_id,)
    ).fetchone()[0]
    return {"pantry": pantry_n, "recipes": recipe_n, "meals": meal_n}


def list_unused_cached_foods(conn: sqlite3.Connection, *, include_drafted: bool = False) -> list[sqlite3.Row]:
    """Return cache foods referenced by no pantry entry, recipe ingredient, or logged meal item.

    By default excludes user_drafted foods (custom profiles created manually,
    which often exist before they've been used anywhere) — pass
    include_drafted=True to consider them for pruning too. Archived foods are
    always excluded — archiving protects a food from being pruned.
    """
    drafted_clause = "" if include_drafted else "AND user_drafted = 0"
    return conn.execute(f"""
        SELECT fdc_id, name, data_type, brand, user_drafted
        FROM foods
        WHERE fdc_id NOT IN (SELECT fdc_id FROM pantry WHERE fdc_id IS NOT NULL)
          AND fdc_id NOT IN (SELECT fdc_id FROM recipe_ingredients)
          AND fdc_id NOT IN (SELECT fdc_id FROM meal_items WHERE item_type = 'food' AND fdc_id IS NOT NULL)
          AND archived = 0
          {drafted_clause}
        ORDER BY name
    """).fetchall()


def prune_unused_cached_foods(conn: sqlite3.Connection, *, include_drafted: bool = False) -> list[sqlite3.Row]:
    """Delete every cache food not referenced by pantry, recipes, or meals.

    Returns the rows that were deleted (fdc_id, name, data_type, brand,
    user_drafted), so a caller can report or log what was removed. See
    list_unused_cached_foods() for the include_drafted semantics — callers
    that want a confirm-before-delete flow should call that first and pass
    the same include_drafted value here.
    """
    unused = list_unused_cached_foods(conn, include_drafted=include_drafted)
    for row in unused:
        conn.execute("DELETE FROM foods WHERE fdc_id = ?", (row["fdc_id"],))
    return unused


def search_cached_foods(conn: sqlite3.Connection, query: str, *, include_archived: bool = False) -> list[sqlite3.Row]:
    words = query.split()
    if not words:
        return []
    # Bare-digit words (e.g. the "1" in "coffee 1") match almost any dosage or
    # serving-size substring — excluding them from the OR match keeps unrelated
    # user-drafted foods like "B12 5000mcg" from surfacing for "coffee 1".
    match_words = [w for w in words if not w.isdigit()] or words
    select = "SELECT fdc_id, name, data_type, brand, portions_json, notes, nutrients_json, archived FROM foods"
    params = [f"%{w}%" for w in match_words]
    archived_clause = "" if include_archived else "AND archived = 0"
    # All-words match for the general cache
    and_cond = " AND ".join("name LIKE ?" for _ in match_words)
    and_rows = conn.execute(f"{select} WHERE {and_cond} {archived_clause} ORDER BY name", params).fetchall()
    # Any-word match for user-drafted foods — so "vitamin d" finds "D3 50 mcg" etc.
    or_cond = " OR ".join("name LIKE ?" for _ in match_words)
    or_rows = conn.execute(
        f"{select} WHERE user_drafted = 1 AND ({or_cond}) {archived_clause} ORDER BY name", params
    ).fetchall()
    seen = {r["fdc_id"] for r in and_rows}
    return list(and_rows) + [r for r in or_rows if r["fdc_id"] not in seen]


# ---------------------------------------------------------------------------
# Food annotations (user-supplied GI / DIAAS estimates)
# ---------------------------------------------------------------------------

def get_food_annotation(conn: sqlite3.Connection, fdc_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM food_annotations WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()


def upsert_food_annotation(
    conn: sqlite3.Connection,
    fdc_id: int,
    *,
    gi_estimate: float | None = None,
    gi_no_prompt: int | None = None,
    diaas_estimate: float | None = None,
    diaas_no_prompt: int | None = None,
    prep_context: str | None = None,
) -> None:
    """Update annotation fields for a food. Pass None to leave a field unchanged.
    gi_no_prompt / diaas_no_prompt: 0 = re-enable prompts, 1 = suppress prompts."""
    conn.execute("""
        INSERT INTO food_annotations
            (fdc_id, gi_estimate, gi_no_prompt, diaas_estimate, diaas_no_prompt, prep_context, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(fdc_id) DO UPDATE SET
            gi_estimate     = COALESCE(excluded.gi_estimate,     gi_estimate),
            gi_no_prompt    = COALESCE(excluded.gi_no_prompt,    gi_no_prompt),
            diaas_estimate  = COALESCE(excluded.diaas_estimate,  diaas_estimate),
            diaas_no_prompt = COALESCE(excluded.diaas_no_prompt, diaas_no_prompt),
            prep_context    = COALESCE(excluded.prep_context,    prep_context),
            updated_at      = datetime('now')
    """, (fdc_id, gi_estimate, gi_no_prompt, diaas_estimate, diaas_no_prompt, prep_context))


def set_food_annotation(
    conn: sqlite3.Connection,
    fdc_id: int,
    *,
    gi_estimate: float | None,
    gi_no_prompt: bool,
    diaas_estimate: float | None,
    diaas_no_prompt: bool,
    prep_context: str | None,
) -> None:
    """Write all annotation fields at once (explicit NULLs clear existing values).
    Use this for web forms; use upsert_food_annotation for CLI (field-at-a-time) updates."""
    conn.execute("""
        INSERT INTO food_annotations
            (fdc_id, gi_estimate, gi_no_prompt, diaas_estimate, diaas_no_prompt, prep_context, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(fdc_id) DO UPDATE SET
            gi_estimate     = excluded.gi_estimate,
            gi_no_prompt    = excluded.gi_no_prompt,
            diaas_estimate  = excluded.diaas_estimate,
            diaas_no_prompt = excluded.diaas_no_prompt,
            prep_context    = excluded.prep_context,
            updated_at      = datetime('now')
    """, (fdc_id, gi_estimate, 1 if gi_no_prompt else 0,
          diaas_estimate, 1 if diaas_no_prompt else 0, prep_context))


def delete_food_annotation(conn: sqlite3.Connection, fdc_id: int) -> None:
    conn.execute("DELETE FROM food_annotations WHERE fdc_id = ?", (fdc_id,))


def annotations_for_fdcids(
    conn: sqlite3.Connection, fdc_ids: list[int]
) -> dict[int, sqlite3.Row]:
    """Bulk-fetch annotations for a list of fdc_ids. Returns {fdc_id: row}."""
    if not fdc_ids:
        return {}
    placeholders = ",".join("?" * len(fdc_ids))
    rows = conn.execute(
        f"SELECT * FROM food_annotations WHERE fdc_id IN ({placeholders})", fdc_ids
    ).fetchall()
    return {row["fdc_id"]: row for row in rows}


# ---------------------------------------------------------------------------
# Recipes
# ---------------------------------------------------------------------------

def recipe_create(conn: sqlite3.Connection, name: str, description: str,
                  servings: float, instructions: str,
                  total_volume: float | None = None,
                  total_volume_unit: str | None = None,
                  total_weight: float | None = None,
                  total_weight_unit: str | None = None,
                  serving_size: str | None = None,
                  complete: bool = False) -> int:
    cur = conn.execute("""
        INSERT INTO recipes (name, description, servings, instructions,
                             total_volume, total_volume_unit,
                             total_weight, total_weight_unit,
                             serving_size, complete)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, description or None, servings, instructions or None,
          total_volume, total_volume_unit or None,
          total_weight, total_weight_unit or None,
          serving_size or None, 1 if complete else 0))
    assert cur.lastrowid is not None
    return cur.lastrowid


def _recipe_invalidate_dcp(conn: sqlite3.Connection, recipe_id: int) -> None:
    """Clear a recipe's stored DCP so stale values aren't shown after an edit."""
    conn.execute(
        "UPDATE recipes SET dcp_g=NULL, dcp_computed_at=NULL WHERE id=?",
        (recipe_id,)
    )


def recipe_add_ingredient(conn: sqlite3.Connection, recipe_id: int, fdc_id: int,
                          food_name: str, amount: float, unit: str,
                          notes: str | None = None,
                          *, ref_recipe_id: int | None = None,
                          ref_recipe_deleted: bool = False) -> None:
    conn.execute("""
        INSERT INTO recipe_ingredients (recipe_id, fdc_id, food_name, amount, unit, notes, ref_recipe_id, ref_recipe_deleted)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (recipe_id, fdc_id, food_name, amount, unit, notes or None, ref_recipe_id, 1 if ref_recipe_deleted else 0))
    _recipe_invalidate_dcp(conn, recipe_id)


def recipe_set_dcp(
    conn: sqlite3.Connection,
    recipe_id: int,
    dcp_g: float | None,
    computed_at: str | None = None,
) -> None:
    conn.execute(
        "UPDATE recipes SET dcp_g = ?, dcp_computed_at = ? WHERE id = ?",
        (dcp_g, computed_at, recipe_id),
    )


def recipe_save_nutrients(
    conn: sqlite3.Connection,
    recipe_id: int,
    nutrients_json_str: str,
) -> None:
    """Cache per-100g nutrient profile for a recipe (used for complement suggestions)."""
    conn.execute(
        "UPDATE recipes SET nutrients_json = ? WHERE id = ?",
        (nutrients_json_str, recipe_id),
    )


def recipe_set_gl(conn: sqlite3.Connection, recipe_id: int, gl_g: float | None) -> None:
    """Store whole-recipe glycemic load (GL). None means GI data incomplete."""
    conn.execute("UPDATE recipes SET gl_g = ? WHERE id = ?", (gl_g, recipe_id))


def recipe_set_saved_analysis(conn: sqlite3.Connection, recipe_id: int,
                               text: str, timestamp: str) -> None:
    """Store a plain-text analysis snapshot with an ISO timestamp."""
    conn.execute(
        "UPDATE recipes SET saved_analysis_at = ?, saved_analysis_text = ? WHERE id = ?",
        (timestamp, text, recipe_id),
    )


def recipe_count(conn: sqlite3.Connection, *, include_archived: bool = False) -> int:
    archived_clause = "" if include_archived else "WHERE archived = 0"
    return conn.execute(f"SELECT COUNT(*) FROM recipes {archived_clause}").fetchone()[0]


def recipe_list(conn: sqlite3.Connection, *, include_archived: bool = False) -> list[sqlite3.Row]:
    archived_clause = "" if include_archived else "WHERE archived = 0"
    return conn.execute(
        "SELECT id, name, description, servings, dcp_g, dcp_computed_at, created_at, complete,"
        " last_accessed_at, total_weight, total_weight_unit, total_volume, total_volume_unit, archived"
        f" FROM recipes {archived_clause} ORDER BY name"
    ).fetchall()


def recipe_list_recent(conn: sqlite3.Connection, limit: int = 20, *, include_archived: bool = False) -> list[sqlite3.Row]:
    archived_clause = "" if include_archived else "WHERE archived = 0"
    return conn.execute(
        "SELECT id, name, description, servings, dcp_g, dcp_computed_at, created_at, complete,"
        " last_accessed_at, total_weight, total_weight_unit, total_volume, total_volume_unit, archived"
        f" FROM recipes {archived_clause} ORDER BY COALESCE(last_accessed_at, created_at) DESC LIMIT ?",
        (limit,)
    ).fetchall()


def set_recipe_archived(conn: sqlite3.Connection, recipe_id: int, archived: bool) -> None:
    """Archive (hide from default lists/search) or restore a recipe."""
    conn.execute("UPDATE recipes SET archived = ? WHERE id = ?", (1 if archived else 0, recipe_id))


def recipe_references(conn: sqlite3.Connection, recipe_id: int) -> dict[str, int]:
    """Return counts of sub-recipe references and logged meal items still referencing this recipe."""
    subrecipe_n = conn.execute(
        "SELECT COUNT(*) FROM recipe_ingredients WHERE ref_recipe_id = ?", (recipe_id,)
    ).fetchone()[0]
    meal_n = conn.execute(
        "SELECT COUNT(*) FROM meal_items WHERE item_type = 'recipe' AND recipe_id = ?", (recipe_id,)
    ).fetchone()[0]
    return {"recipes": subrecipe_n, "meals": meal_n}


def recipe_touch(conn: sqlite3.Connection, recipe_id: int) -> None:
    conn.execute(
        "UPDATE recipes SET last_accessed_at = datetime('now') WHERE id = ?",
        (recipe_id,)
    )


def recipe_get(conn: sqlite3.Connection, recipe_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM recipes WHERE id = ?", (recipe_id,)
    ).fetchone()


def recipe_get_ingredients(conn: sqlite3.Connection, recipe_id: int) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM recipe_ingredients WHERE recipe_id = ? ORDER BY COALESCE(sort_order, id), id",
        (recipe_id,)
    ).fetchall()


def recipe_reorder_ingredients(conn: sqlite3.Connection, ordered_ids: list[int]) -> None:
    """Assign sort_order 1..N to ingredients given by their IDs in the desired order."""
    for pos, ing_id in enumerate(ordered_ids, start=1):
        conn.execute(
            "UPDATE recipe_ingredients SET sort_order = ? WHERE id = ?",
            (pos, ing_id),
        )


def recipe_auto_weight(conn: sqlite3.Connection, recipe_id: int) -> float | None:
    """Compute and store total_weight from ingredient gram amounts if not already set.

    Direct food ingredients contribute their stored gram amount.  Sub-recipe
    ingredients contribute (sub_recipe.total_weight / sub_recipe.servings) × amount.
    Returns the computed weight if stored, None if already set or data is incomplete.
    """
    row = conn.execute(
        "SELECT total_weight, servings FROM recipes WHERE id = ?", (recipe_id,)
    ).fetchone()
    if not row or row["total_weight"]:
        return None
    ingredients = recipe_get_ingredients(conn, recipe_id)
    if not ingredients:
        return None
    total = 0.0
    for ing in ingredients:
        if ing["ref_recipe_id"]:
            sub = conn.execute(
                "SELECT total_weight, servings FROM recipes WHERE id = ?",
                (ing["ref_recipe_id"],),
            ).fetchone()
            if not sub or not sub["total_weight"] or not sub["servings"]:
                return None
            total += (sub["total_weight"] / sub["servings"]) * ing["amount"]
        else:
            if not ing["amount"] or ing["amount"] <= 0:
                return None
            total += ing["amount"]
    if total <= 0:
        return None
    conn.execute(
        "UPDATE recipes SET total_weight = ?, total_weight_unit = 'g' WHERE id = ?",
        (round(total, 1), recipe_id),
    )
    return total


def recipe_compute_weight(conn: sqlite3.Connection,
                          recipe_id: int) -> tuple[float, bool] | None:
    """Return (computed_grams, is_complete) for a recipe's ingredient sum.

    is_complete is False when any ingredient has unknown/zero weight or a
    sub-recipe lacks weight data — the returned value is then a lower bound.
    Returns None only when there are no ingredients at all.
    """
    ingredients = recipe_get_ingredients(conn, recipe_id)
    if not ingredients:
        return None
    total = 0.0
    complete = True
    for ing in ingredients:
        if ing["ref_recipe_id"]:
            sub = conn.execute(
                "SELECT total_weight, servings FROM recipes WHERE id = ?",
                (ing["ref_recipe_id"],),
            ).fetchone()
            if not sub or not sub["total_weight"] or not sub["servings"]:
                complete = False
            else:
                total += (sub["total_weight"] / sub["servings"]) * ing["amount"]
        else:
            if not ing["amount"] or ing["amount"] <= 0:
                complete = False
            else:
                total += ing["amount"]
    return (total, complete)


def recipe_update(conn: sqlite3.Connection, recipe_id: int, name: str,
                  description: str, servings: float, instructions: str,
                  total_volume: float | None = None,
                  total_volume_unit: str | None = None,
                  total_weight: float | None = None,
                  total_weight_unit: str | None = None,
                  serving_size: str | None = None,
                  complete: bool = False) -> None:
    conn.execute(
        "UPDATE recipes SET name=?, description=?, servings=?, instructions=?, "
        "total_volume=?, total_volume_unit=?, total_weight=?, total_weight_unit=?, "
        "serving_size=?, complete=? WHERE id=?",
        (name, description or None, servings, instructions or None,
         total_volume, total_volume_unit or None,
         total_weight, total_weight_unit or None,
         serving_size or None, 1 if complete else 0, recipe_id)
    )
    conn.execute(
        "UPDATE meal_items SET food_name=? WHERE item_type='recipe' AND recipe_id=?",
        (name, recipe_id)
    )
    conn.execute(
        "UPDATE recipe_ingredients SET food_name=? WHERE ref_recipe_id=?",
        (name, recipe_id)
    )
    _recipe_invalidate_dcp(conn, recipe_id)


def recipe_update_ingredient(conn: sqlite3.Connection, ingredient_id: int,
                             amount: float, unit: str, food_name: str,
                             notes: str | None = None) -> None:
    row = conn.execute(
        "SELECT recipe_id FROM recipe_ingredients WHERE id=?", (ingredient_id,)
    ).fetchone()
    conn.execute(
        "UPDATE recipe_ingredients SET amount=?, unit=?, food_name=?, notes=? WHERE id=?",
        (amount, unit, food_name, notes or None, ingredient_id)
    )
    if row:
        _recipe_invalidate_dcp(conn, row["recipe_id"])


def recipe_remove_ingredient(conn: sqlite3.Connection, ingredient_id: int) -> bool:
    row = conn.execute(
        "SELECT recipe_id FROM recipe_ingredients WHERE id=?", (ingredient_id,)
    ).fetchone()
    cur = conn.execute("DELETE FROM recipe_ingredients WHERE id = ?", (ingredient_id,))
    if row:
        _recipe_invalidate_dcp(conn, row["recipe_id"])
    return cur.rowcount > 0


def recipe_referencing_subrecipe(conn: sqlite3.Connection, recipe_id: int) -> list[sqlite3.Row]:
    """Return (id, name) rows for recipes that use `recipe_id` as a sub-recipe ingredient."""
    return conn.execute("""
        SELECT DISTINCT r.id, r.name
        FROM recipe_ingredients ri
        JOIN recipes r ON r.id = ri.recipe_id
        WHERE ri.ref_recipe_id = ?
        ORDER BY r.name
    """, (recipe_id,)).fetchall()


def recipe_delete(conn: sqlite3.Connection, recipe_id: int) -> bool:
    """Delete a recipe. Any other recipe that used it as a sub-recipe keeps its
    ingredient row (food_name snapshot intact) but is flagged via
    ref_recipe_deleted so displays can show it as a broken reference instead
    of silently losing it or failing on the FK constraint."""
    conn.execute(
        "UPDATE recipe_ingredients SET ref_recipe_id = NULL, ref_recipe_deleted = 1 WHERE ref_recipe_id = ?",
        (recipe_id,)
    )
    cur = conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    return cur.rowcount > 0


_WORD_RE = _re.compile(r"[A-Za-z0-9]+")


def _name_words(s: str) -> set[str]:
    return {w.lower() for w in _WORD_RE.findall(s or "")}


def _all_broken_recipe_refs(conn: sqlite3.Connection) -> tuple[list[sqlite3.Row], list[sqlite3.Row]]:
    """Every meal_items / recipe_ingredients row left dangling by some deleted
    recipe, each carrying the original recipe's name as `matched_name`."""
    meals = conn.execute("""
        SELECT DISTINCT m.id AS meal_id, m.name AS meal_name, m.meal_date, mi.food_name AS matched_name
        FROM meal_items mi
        JOIN meals m ON m.id = mi.meal_id
        WHERE mi.item_type = 'recipe' AND mi.recipe_id NOT IN (SELECT id FROM recipes)
        ORDER BY mi.food_name, m.meal_date
    """).fetchall()
    recipes = conn.execute("""
        SELECT DISTINCT r.id AS recipe_id, r.name AS recipe_name, ri.food_name AS matched_name
        FROM recipe_ingredients ri
        JOIN recipes r ON r.id = ri.recipe_id
        WHERE ri.ref_recipe_deleted = 1
        ORDER BY ri.food_name, r.name
    """).fetchall()
    return meals, recipes


def find_broken_recipe_refs(conn: sqlite3.Connection, name: str) -> dict:
    """Fuzzy-find meal_items and recipe_ingredients rows left dangling by a
    deleted recipe, for offering to relink them when a recipe is (re-)created.
    A row matches if it shares at least one word (case-insensitive) with
    `name` — e.g. creating "Chicken Stew" will surface a broken reference
    stored as "Beef Stew" or just "Stew", not only an exact-name match.

    Because a fuzzy search can turn up broken refs left by more than one
    distinct deleted recipe, each row carries its original name as
    `matched_name` — callers should offer/relink one matched_name group at a
    time (see relink_recipe_refs) rather than assuming every match belongs
    to the same original recipe.

    Returns {"meals": [rows...], "recipes": [rows...]}.
    """
    words = _name_words(name)
    if not words:
        return {"meals": [], "recipes": []}
    all_meals, all_recipes = _all_broken_recipe_refs(conn)
    meals = [row for row in all_meals if _name_words(row["matched_name"]) & words]
    recipes = [row for row in all_recipes if _name_words(row["matched_name"]) & words]
    return {"meals": meals, "recipes": recipes}


def list_all_broken_recipe_refs(conn: sqlite3.Connection) -> dict:
    """Every broken recipe reference in the database, for browsing
    independent of any specific new recipe's name (see find_broken_recipe_refs
    for the fuzzy-match version used at recipe-creation time).

    Returns {"meals": [rows...], "recipes": [rows...]}.
    """
    meals, recipes = _all_broken_recipe_refs(conn)
    return {"meals": meals, "recipes": recipes}


def relink_recipe_refs(conn: sqlite3.Connection, name: str, new_recipe_id: int) -> tuple[int, int]:
    """Relink broken meal_items/recipe_ingredients references (matched by the
    stored food_name snapshot) to a newly (re-)created recipe of that name.
    Returns (meal_items_relinked, recipe_ingredients_relinked)."""
    meal_cur = conn.execute("""
        UPDATE meal_items SET recipe_id = ?
        WHERE item_type = 'recipe' AND food_name = ?
          AND recipe_id NOT IN (SELECT id FROM recipes)
    """, (new_recipe_id, name))
    ing_cur = conn.execute("""
        UPDATE recipe_ingredients SET ref_recipe_id = ?, ref_recipe_deleted = 0
        WHERE ref_recipe_deleted = 1 AND food_name = ?
    """, (new_recipe_id, name))
    return meal_cur.rowcount, ing_cur.rowcount


# ---------------------------------------------------------------------------
# Meals
# ---------------------------------------------------------------------------

def meal_create(conn: sqlite3.Connection, name: str, meal_date: str) -> int:
    cur = conn.execute(
        "INSERT INTO meals (name, meal_date) VALUES (?, ?)",
        (name, meal_date)
    )
    assert cur.lastrowid is not None
    return cur.lastrowid


def meal_add_food(conn: sqlite3.Connection, meal_id: int, fdc_id: int,
                  food_name: str, amount: float, unit: str,
                  notes: str | None = None) -> None:
    conn.execute("""
        INSERT INTO meal_items (meal_id, item_type, fdc_id, food_name, amount, unit, notes)
        VALUES (?, 'food', ?, ?, ?, ?, ?)
    """, (meal_id, fdc_id, food_name, amount, unit, notes or None))


def meal_add_recipe(conn: sqlite3.Connection, meal_id: int, recipe_id: int,
                    recipe_name: str, servings: float, unit: str = "servings") -> None:
    conn.execute("""
        INSERT INTO meal_items
            (meal_id, item_type, recipe_id, food_name, amount, unit)
        VALUES (?, 'recipe', ?, ?, ?, ?)
    """, (meal_id, recipe_id, recipe_name, servings, unit))


def meal_list_by_date(conn: sqlite3.Connection, meal_date: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM meals WHERE meal_date = ? ORDER BY created_at",
        (meal_date,)
    ).fetchall()


def meal_list_dates(conn: sqlite3.Connection, limit: int = 30) -> list[sqlite3.Row]:
    """Return distinct dates that have meals, most recent first."""
    return conn.execute(
        "SELECT DISTINCT meal_date FROM meals ORDER BY meal_date DESC LIMIT ?",
        (limit,)
    ).fetchall()


def day_bcp_cache_set(conn: sqlite3.Connection, meal_date: str, dcp_g: float) -> None:
    """Persist the day-level pooled DCP computed by the summary analysis."""
    conn.execute(
        "INSERT OR REPLACE INTO day_bcp_cache (meal_date, dcp_g, computed_at) VALUES (?, ?, datetime('now'))",
        (meal_date, dcp_g),
    )


def meal_dates_with_bcp(conn: sqlite3.Connection, limit: int = 30) -> list[sqlite3.Row]:
    """Return recent meal dates with aggregated DCP data.

    Columns: meal_date, day_bcp (NULL if no meal that day has bcp_g computed
    yet — this counts every meal with a computed value, not just ones marked
    complete: DCP is auto-saved as items are added, so an in-progress meal
    already contributes to the day total, same as the day-detail page's own
    pooled DIAAS analysis and the CLI's day summary), day_pct_goal (the
    %-of-profile-goal value already stored per meal by refresh_day_pct_goal —
    every meal on a date shares the same value, so MAX just picks it up).
    Prefers the pooled day-level DCP from day_bcp_cache when available.
    """
    return conn.execute(
        """
        SELECT
            m.meal_date,
            COALESCE(c.dcp_g,
                SUM(CASE WHEN m.bcp_g IS NOT NULL THEN m.bcp_g END)
            ) AS day_bcp,
            MAX(m.day_pct_goal) AS day_pct_goal
        FROM meals m
        LEFT JOIN day_bcp_cache c ON c.meal_date = m.meal_date
        GROUP BY m.meal_date
        ORDER BY m.meal_date DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def day_profile_get(conn: sqlite3.Connection, meal_date: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM day_profile WHERE meal_date = ?", (meal_date,)
    ).fetchone()


def day_profile_upsert(conn: sqlite3.Connection, meal_date: str, profile_name: str,
                        profile_json: str, overridden: bool = False) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO day_profile
            (meal_date, profile_name, profile_json, pinned_at, overridden)
        VALUES (?, ?, ?, datetime('now'), ?)
        """,
        (meal_date, profile_name, profile_json, int(overridden)),
    )


def day_profile_dates_missing(conn: sqlite3.Connection) -> list[str]:
    """Distinct meal_dates that have meals but no day_profile row yet."""
    return [
        r["meal_date"] for r in conn.execute(
            """
            SELECT DISTINCT meal_date FROM meals
            WHERE meal_date NOT IN (SELECT meal_date FROM day_profile)
            """
        ).fetchall()
    ]


_MEAL_SORT_ORDER_BY = {
    "date":      "m.meal_date DESC, m.created_at DESC",
    "name":      "m.name COLLATE NOCASE ASC, m.meal_date DESC",
    "meal_bcp":  "m.bcp_g IS NULL, m.bcp_g DESC, m.meal_date DESC",
    "calories":  "m.calories IS NULL, m.calories DESC, m.meal_date DESC",
}


def meal_list_recent(
    conn: sqlite3.Connection,
    limit: int = 9,
    offset: int = 0,
    before_date: str | None = None,
    sort: str = "date",
) -> list[sqlite3.Row]:
    """Return meals ordered most-recent first (or by `sort`), with item count, for the picker UI."""
    where = "WHERE m.meal_date <= :before_date" if before_date else ""
    params: dict = {"limit": limit, "offset": offset}
    if before_date:
        params["before_date"] = before_date
    order_by = _MEAL_SORT_ORDER_BY.get(sort, _MEAL_SORT_ORDER_BY["date"])
    return conn.execute(
        f"""
        SELECT m.*, COUNT(mi.id) AS item_count
        FROM meals m
        LEFT JOIN meal_items mi ON mi.meal_id = m.id
        {where}
        GROUP BY m.id
        ORDER BY {order_by}
        LIMIT :limit OFFSET :offset
        """,
        params,
    ).fetchall()


def meal_count_recent(
    conn: sqlite3.Connection,
    before_date: str | None = None,
) -> int:
    """Return total number of meals (with optional before_date filter) for pagination display."""
    where = "WHERE meal_date <= :before_date" if before_date else ""
    params: dict = {}
    if before_date:
        params["before_date"] = before_date
    row = conn.execute(f"SELECT COUNT(*) FROM meals {where}", params).fetchone()
    return row[0] if row else 0


def meal_list_complete(
    conn: sqlite3.Connection,
    id_min: int | None = None,
    id_max: int | None = None,
) -> list[sqlite3.Row]:
    """Return all complete meals, optionally filtered to an ID range."""
    clauses = ["complete = 1"]
    params: list = []
    if id_min is not None:
        clauses.append("id >= ?")
        params.append(id_min)
    if id_max is not None:
        clauses.append("id <= ?")
        params.append(id_max)
    where = " AND ".join(clauses)
    return conn.execute(f"SELECT * FROM meals WHERE {where} ORDER BY id", params).fetchall()


def meal_list_complete_since(conn: sqlite3.Connection, since_date: str) -> list[sqlite3.Row]:
    """Return all complete meals on or after since_date (YYYY-MM-DD)."""
    return conn.execute(
        "SELECT * FROM meals WHERE complete = 1 AND meal_date >= ? ORDER BY id",
        (since_date,),
    ).fetchall()


def meals_missing_nutrient_snapshot(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Meals with at least one item but no nutrients_snapshot_json — meals
    whose bcp_g/calories were computed (or the meal predates the snapshot
    column's meaning) before the per-meal nutrient snapshot existed, so the
    Meals & Log / Daily Summary extra-column feature has nothing to show for
    them. Used for a one-time startup backfill."""
    return conn.execute(
        "SELECT DISTINCT m.* FROM meals m "
        "JOIN meal_items mi ON mi.meal_id = m.id "
        "WHERE m.nutrients_snapshot_json IS NULL"
    ).fetchall()


def dates_missing_day_pct_goal(conn: sqlite3.Connection) -> list[str]:
    """Dates with at least one meal that has bcp_g computed but no
    day_pct_goal stored — from before day_pct_goal counted meals not marked
    complete (or a meal that simply hasn't triggered a refresh yet). Used for
    a one-time startup backfill alongside meals_missing_nutrient_snapshot."""
    return [
        row["meal_date"] for row in conn.execute(
            "SELECT DISTINCT meal_date FROM meals "
            "WHERE bcp_g IS NOT NULL AND day_pct_goal IS NULL"
        ).fetchall()
    ]


def meal_get(conn: sqlite3.Connection, meal_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone()


def meal_get_items(conn: sqlite3.Connection, meal_id: int) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM meal_items WHERE meal_id = ? ORDER BY id",
        (meal_id,)
    ).fetchall()


def meal_list_by_date_range(conn: sqlite3.Connection, start_date: str, end_date: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM meals WHERE meal_date BETWEEN ? AND ? ORDER BY meal_date, created_at",
        (start_date, end_date)
    ).fetchall()


def meal_list_by_ids(conn: sqlite3.Connection, ids: list[int]) -> list[sqlite3.Row]:
    """Return meals matching the given IDs, ordered by date. Missing IDs are silently omitted."""
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    return conn.execute(
        f"SELECT * FROM meals WHERE id IN ({placeholders}) ORDER BY meal_date, created_at",
        ids
    ).fetchall()


def meal_expand_food_items(conn: sqlite3.Connection, meal_id: int) -> list[tuple[int | None, str, str, bool, bool, int | None]]:
    """Flatten a meal's items into (fdc_id, name, kind, has_protein, deleted, recipe_id) tuples.

    Plain food items yield one ("food") tuple. Recipe items yield one ("recipe")
    tuple for the recipe itself, plus one ("food") tuple per base ingredient
    (recursively expanded through nested sub-recipes via ref_recipe_id).

    has_protein reflects the food's cached protein_g > 0 (False if the food
    isn't cached). A recipe row's has_protein is True if any of its
    (recursively) expanded ingredients has_protein.

    deleted is True for a "recipe" row whose recipe_id no longer exists in the
    recipes table (the recipe was deleted after this meal referenced it). The
    meal item's stored food_name is used as a fallback label in that case, and
    it has no expanded ingredients.

    recipe_id is the stable identifier for a "recipe" row — always meal_items'
    recipe_id for a directly-added recipe (even after deletion, since that
    column is never cleared), or None for "food" rows and for a nested
    sub-recipe that was itself deleted (ref_recipe_id is cleared on delete, so
    no id survives — see recipe_delete()). Callers should key/group recipe
    rows by recipe_id when present rather than by name, since a recipe's name
    can change after a meal references it while its id stays fixed.
    """
    def _food_has_protein(fdc_id: int) -> bool:
        cached = get_cached_food(conn, fdc_id)
        if not cached:
            return False
        nutrients = json.loads(cached["nutrients_json"])
        return nutrients.get("protein_g", 0) > 0

    def _expand_recipe(recipe_id: int) -> list[tuple[int | None, str, str, bool, bool, int | None]]:
        out: list[tuple[int | None, str, str, bool, bool, int | None]] = []
        for ing in recipe_get_ingredients(conn, recipe_id):
            if ing["ref_recipe_deleted"]:
                out.append((None, ing["food_name"], "recipe", False, True, None))
            elif ing["ref_recipe_id"]:
                out.extend(_expand_recipe(ing["ref_recipe_id"]))
            else:
                out.append((ing["fdc_id"], ing["food_name"], "food", _food_has_protein(ing["fdc_id"]), False, None))
        return out

    result: list[tuple[int | None, str, str, bool, bool, int | None]] = []
    for item in meal_get_items(conn, meal_id):
        if item["item_type"] == "food":
            result.append((item["fdc_id"], item["food_name"], "food", _food_has_protein(item["fdc_id"]), False, None))
        elif item["item_type"] == "recipe":
            live_recipe = recipe_get(conn, item["recipe_id"])
            recipe_deleted = live_recipe is None
            expanded = [] if recipe_deleted else _expand_recipe(item["recipe_id"])
            display_name = live_recipe["name"] if live_recipe else item["food_name"]
            result.append((None, display_name, "recipe", any(e[3] for e in expanded), recipe_deleted, item["recipe_id"]))
            result.extend(expanded)
    return result


def meal_update_item(conn: sqlite3.Connection, item_id: int, meal_id: int,
                     amount: float, unit: str) -> None:
    conn.execute(
        "UPDATE meal_items SET amount=?, unit=? WHERE id=? AND meal_id=?",
        (amount, unit, item_id, meal_id)
    )


def meal_replace_food(conn: sqlite3.Connection, item_id: int, meal_id: int,
                      fdc_id: int, food_name: str, amount: float, unit: str,
                      notes: str | None = None) -> None:
    conn.execute(
        "UPDATE meal_items SET fdc_id=?, food_name=?, amount=?, unit=?, notes=? WHERE id=? AND meal_id=?",
        (fdc_id, food_name, amount, unit, notes or None, item_id, meal_id)
    )


def meal_remove_item(conn: sqlite3.Connection, item_id: int, meal_id: int) -> bool:
    cur = conn.execute(
        "DELETE FROM meal_items WHERE id = ? AND meal_id = ?", (item_id, meal_id)
    )
    return cur.rowcount > 0


def search_meal_history(
    conn: sqlite3.Connection, query: str
) -> list[sqlite3.Row]:
    """Search food items across all meals by name (LIKE) and by fdc_id cross-reference.
    Returns rows ordered by meal_date DESC. Includes both food and recipe items."""
    like = f"%{query}%"
    return conn.execute(
        """
        SELECT m.meal_date, m.name AS meal_name, m.id AS meal_id,
               mi.id AS item_id, mi.item_type, mi.food_name, mi.fdc_id,
               mi.recipe_id, mi.amount, mi.unit, mi.notes
        FROM meal_items mi
        JOIN meals m ON mi.meal_id = m.id
        WHERE (
            mi.food_name LIKE ?
            OR (mi.fdc_id IS NOT NULL AND mi.fdc_id IN (
                SELECT DISTINCT fdc_id FROM meal_items
                WHERE food_name LIKE ? AND fdc_id IS NOT NULL
            ))
        )
        ORDER BY m.meal_date DESC, m.id, mi.id
        """,
        (like, like),
    ).fetchall()


def meal_delete(conn: sqlite3.Connection, meal_id: int) -> bool:
    cur = conn.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
    return cur.rowcount > 0


def meal_delete_by_date(conn: sqlite3.Connection, meal_date: str) -> int:
    """Delete every meal on meal_date. Returns the number of meals deleted."""
    cur = conn.execute("DELETE FROM meals WHERE meal_date = ?", (meal_date,))
    return cur.rowcount


def meal_set_complete(conn: sqlite3.Connection, meal_id: int, complete: bool) -> None:
    conn.execute(
        "UPDATE meals SET complete = ? WHERE id = ?",
        (1 if complete else 0, meal_id)
    )


def meal_rename(conn: sqlite3.Connection, meal_id: int, new_name: str) -> None:
    conn.execute("UPDATE meals SET name = ? WHERE id = ?", (new_name, meal_id))


def meal_set_date(conn: sqlite3.Connection, meal_id: int, new_date: str) -> None:
    conn.execute("UPDATE meals SET meal_date = ? WHERE id = ?", (new_date, meal_id))


def meal_set_bcp(conn: sqlite3.Connection, meal_id: int, bcp_g: float | None,
                 calories: float | None = None,
                 nutrients: dict[str, float] | None = None) -> None:
    conn.execute(
        "UPDATE meals SET bcp_g=?, calories=?, bcp_computed_at=datetime('now'), "
        "nutrients_snapshot_json=? WHERE id=?",
        (bcp_g, calories, json.dumps(nutrients) if nutrients is not None else None, meal_id),
    )


def meal_set_day_pct_goal(conn: sqlite3.Connection, meal_id: int, pct: float | None) -> None:
    conn.execute(
        "UPDATE meals SET day_pct_goal=? WHERE id=?",
        (pct, meal_id),
    )


def meal_copy_items(conn: sqlite3.Connection, from_meal_id: int, to_meal_id: int) -> int:
    """Copy all items from one meal to another. Returns count of items copied."""
    cur = conn.execute("""
        INSERT INTO meal_items (meal_id, item_type, fdc_id, recipe_id, food_name, amount, unit, notes)
        SELECT ?, item_type, fdc_id, recipe_id, food_name, amount, unit, notes
        FROM meal_items WHERE meal_id = ?
    """, (to_meal_id, from_meal_id))
    return cur.rowcount


# ---------------------------------------------------------------------------
# Pantry
# ---------------------------------------------------------------------------

def pantry_add(conn: sqlite3.Connection, food_name: str,
               fdc_id: int | None = None, notes: str | None = None) -> int:
    cur = conn.execute(
        "INSERT INTO pantry (food_name, fdc_id, notes) VALUES (?, ?, ?)",
        (food_name, fdc_id, notes or None)
    )
    assert cur.lastrowid is not None
    return cur.lastrowid


def pantry_update(conn: sqlite3.Connection, pantry_id: int,
                  food_name: str, fdc_id: int | None, notes: str | None) -> bool:
    cur = conn.execute(
        "UPDATE pantry SET food_name = ?, fdc_id = ?, notes = ? WHERE id = ?",
        (food_name, fdc_id, notes or None, pantry_id)
    )
    return cur.rowcount > 0


def pantry_remove(conn: sqlite3.Connection, pantry_id: int) -> bool:
    cur = conn.execute("DELETE FROM pantry WHERE id = ?", (pantry_id,))
    return cur.rowcount > 0


def set_pantry_archived(conn: sqlite3.Connection, pantry_id: int, archived: bool) -> None:
    """Archive (hide from default list/complement candidates) or restore a pantry entry."""
    conn.execute("UPDATE pantry SET archived = ? WHERE id = ?", (1 if archived else 0, pantry_id))


def pantry_list(conn: sqlite3.Connection, *, include_archived: bool = False) -> list[sqlite3.Row]:
    archived_clause = "" if include_archived else "WHERE archived = 0"
    return conn.execute(
        f"SELECT id, food_name, fdc_id, notes, added_at, archived FROM pantry {archived_clause} ORDER BY food_name"
    ).fetchall()


def pantry_get(conn: sqlite3.Connection, pantry_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM pantry WHERE id = ?", (pantry_id,)
    ).fetchone()


# ---------------------------------------------------------------------------
# User-drafted foods
# ---------------------------------------------------------------------------

def next_user_drafted_fdc_id(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT MIN(fdc_id) AS min_id FROM foods WHERE fdc_id < 0").fetchone()
    min_id = row["min_id"] if row and row["min_id"] is not None else 0
    return int(min_id) - 1 if min_id <= 0 else -1


def list_user_drafted_foods(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT fdc_id, name, data_type, brand, serving_size, serving_unit, notes, cached_at "
        "FROM foods WHERE user_drafted = 1 ORDER BY name"
    ).fetchall()


def update_food_nutrients_partial(conn: sqlite3.Connection, fdc_id: int, new_nutrients: dict) -> None:
    """Merge new_nutrients into an existing food's nutrients_json without touching other fields."""
    row = conn.execute("SELECT nutrients_json FROM foods WHERE fdc_id = ?", (fdc_id,)).fetchone()
    if not row:
        return
    existing = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
    existing.update(new_nutrients)
    conn.execute(
        "UPDATE foods SET nutrients_json = ?, cached_at = datetime('now') WHERE fdc_id = ?",
        (json.dumps(existing), fdc_id),
    )


# ---------------------------------------------------------------------------
# Saved comparisons
# ---------------------------------------------------------------------------

def saved_comparison_save(
    conn: sqlite3.Connection,
    name: str,
    fdc_ids: list[int],
    amounts: list[float],
) -> int:
    cur = conn.execute(
        "INSERT INTO saved_comparisons (name, fdc_ids, amounts) VALUES (?, ?, ?)",
        (name, json.dumps(fdc_ids), json.dumps(amounts)),
    )
    return cur.lastrowid


def saved_comparison_list(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id, name, fdc_ids, amounts, created_at FROM saved_comparisons ORDER BY created_at DESC"
    ).fetchall()


def saved_comparison_get(conn: sqlite3.Connection, cmp_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT id, name, fdc_ids, amounts, created_at FROM saved_comparisons WHERE id = ?",
        (cmp_id,),
    ).fetchone()


def saved_comparison_rename(conn: sqlite3.Connection, cmp_id: int, name: str) -> bool:
    cur = conn.execute("UPDATE saved_comparisons SET name = ? WHERE id = ?", (name, cmp_id))
    return cur.rowcount > 0


def saved_comparison_delete(conn: sqlite3.Connection, cmp_id: int) -> bool:
    cur = conn.execute("DELETE FROM saved_comparisons WHERE id = ?", (cmp_id,))
    return cur.rowcount > 0


def update_food_portions(conn: sqlite3.Connection, fdc_id: int, portions: list[dict]) -> None:
    """Patch only the portions_json column for a cached food."""
    conn.execute(
        "UPDATE foods SET portions_json=? WHERE fdc_id=?",
        (json.dumps(portions), fdc_id),
    )


def update_cached_food_profile(
    conn: sqlite3.Connection,
    fdc_id: int,
    name: str,
    nutrients: dict[str, float],
    *,
    data_type: str | None = None,
    brand: str | None = None,
    serving_size: float | None = None,
    serving_unit: str | None = None,
    portions: list[dict] | None = None,
    notes: str | None = None,
    user_drafted: bool = True,
) -> None:
    conn.execute(
        "UPDATE foods SET name=?, data_type=?, brand=?, serving_size=?, serving_unit=?, "
        "nutrients_json=?, portions_json=?, user_drafted=?, notes=?, cached_at=(datetime('now')) "
        "WHERE fdc_id=?",
        (
            name, data_type, brand, serving_size, serving_unit,
            json.dumps(nutrients), json.dumps(portions or []),
            1 if user_drafted else 0, notes or None, fdc_id,
        ),
    )


# ---------------------------------------------------------------------------
# Oxalate links
# ---------------------------------------------------------------------------

def oxalate_link_get(conn: sqlite3.Connection, fdc_id: int) -> sqlite3.Row | None:
    """Return the oxalate_links row for fdc_id, or None if not yet linked."""
    return conn.execute(
        "SELECT * FROM oxalate_links WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()


def oxalate_link_save(
    conn: sqlite3.Connection,
    fdc_id: int,
    *,
    oxalate_food_id: int | None,
    no_match: bool,
) -> None:
    """Upsert an oxalate link for fdc_id.
    Set no_match=True when the user confirmed no oxalate record applies.
    Set oxalate_food_id to the matching oxalate.db row id when confirmed.

    No-ops if fdc_id isn't in the foods cache (e.g. pruned after a recipe/meal
    was built from it) — oxalate_links.fdc_id has a FK to foods(fdc_id).
    """
    if get_cached_food(conn, fdc_id) is None:
        return
    conn.execute(
        """INSERT INTO oxalate_links
               (fdc_id, oxalate_food_id, user_confirmed, confirmed_at, no_match)
           VALUES (?, ?, 1, datetime('now'), ?)
           ON CONFLICT(fdc_id) DO UPDATE SET
               oxalate_food_id = excluded.oxalate_food_id,
               user_confirmed  = 1,
               confirmed_at    = excluded.confirmed_at,
               no_match        = excluded.no_match
        """,
        (fdc_id, oxalate_food_id, 1 if no_match else 0),
    )
