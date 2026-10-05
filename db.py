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
                introduction    TEXT,
                notes           TEXT,
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
                gi_source       TEXT,
                gi_no_prompt    INTEGER DEFAULT 0,
                diaas_estimate  REAL,
                diaas_no_prompt INTEGER DEFAULT 0,
                prep_context    TEXT,
                -- 1 once the user has saved the Annotate form for this food,
                -- i.e. has seen the GI/DIAAS prompt and made their choices
                -- (including deliberately leaving one blank). Distinct from
                -- the two no_prompt flags: those say "never ask about THIS
                -- estimate", while this says "stop interrupting me about
                -- this food" -- see _annotation_prompt_needed() in
                -- web/backend.py.
                reviewed        INTEGER DEFAULT 0,
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
            "introduction      TEXT",
            "notes             TEXT",
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
        # Migrate: clear curator notes holding no words at all. The Claude
        # fetch import used to save the commas left between foods, when a reply
        # listed them as a bare JSON array, as every imported food's "curator
        # notes" (e.g. ",\n  ,\n  ,"). claude_fetch.parse_response() no longer
        # keeps such lines; this removes the ones already saved. Idempotent.
        conn.execute("UPDATE foods SET curator_notes = NULL "
                     "WHERE curator_notes IS NOT NULL AND curator_notes NOT GLOB '*[A-Za-z0-9]*'")

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

        # Grams one serving of a logged recipe weighed when it was logged (or
        # when its servings were last edited/confirmed). A meal stores recipe
        # amounts in servings, so if the recipe's serving weight later changes
        # (e.g. its servings count is edited) the meal page can ask whether
        # the logged amount should keep its grams. NULL = not yet recorded;
        # filled lazily by web/backend.py's _annotate_recipe_amounts().
        try:
            conn.execute("ALTER TABLE meal_items ADD COLUMN serving_grams REAL")
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

        for _col in ("gi_no_prompt INTEGER DEFAULT 0", "diaas_no_prompt INTEGER DEFAULT 0",
                     "gi_source TEXT", "reviewed INTEGER DEFAULT 0"):
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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS saved_recipe_comparisons (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                recipe_ids TEXT    NOT NULL,
                unit       TEXT    NOT NULL DEFAULT 'serving',
                created_at TEXT    DEFAULT (datetime('now'))
            )
        """)

        # Superseded 2026-09 by the unified /compare (mixes foods and recipes,
        # up to 8 items) — saved_comparisons/saved_recipe_comparisons above
        # are kept (unused) so any pre-existing rows aren't dropped, but new
        # saves go here. `items` is a JSON array of {"kind": "food"|"recipe",
        # "id": int} — every comparison is judged per 100g of each item, so
        # there's no per-item amount to store.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS saved_mixed_comparisons (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                items      TEXT    NOT NULL,
                created_at TEXT    DEFAULT (datetime('now'))
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS recipe_translations (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id  INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
                language   TEXT    NOT NULL,
                data_json  TEXT    NOT NULL,
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

        # Nutrient groups the user marked "not needed" for one food, so the
        # data-completeness check stops flagging them (e.g. macronutrients for
        # a spice) — see numa_app/services/data_completeness.py.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS food_data_ignores (
                fdc_id     INTEGER NOT NULL REFERENCES foods(fdc_id) ON DELETE CASCADE,
                group_key  TEXT    NOT NULL,
                PRIMARY KEY (fdc_id, group_key)
            )
        """)

        try:
            conn.execute("ALTER TABLE recipes ADD COLUMN nutrients_json TEXT")
        except sqlite3.OperationalError:
            pass

        # Migrate: drop a stray "amounts" column some installs' saved_mixed_comparisons
        # table was created with before the schema was finalized (it was never part of
        # any committed CREATE TABLE) — its NOT NULL constraint broke every save.
        try:
            conn.execute("ALTER TABLE saved_mixed_comparisons DROP COLUMN amounts")
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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS recompute_errors (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                occurred_at  TEXT    NOT NULL DEFAULT (datetime('now')),
                entity_type  TEXT    NOT NULL,
                entity_id    INTEGER,
                message      TEXT    NOT NULL,
                resolved_at  TEXT,
                banner_ack_at TEXT
            )
        """)

        # Recipe ingredients / logged meal foods the user chose to keep at
        # their stored grams although their typed volume or portion now works
        # out differently ("Keep as entered" on a food's Portions page or
        # Foods -> 9). `kind` is "recipe" (recipe_ingredients.id) or "meal"
        # (meal_items.id); the keep holds only while the item's grams are
        # still `stored_g`, so editing the amount ends it. See amount_keeps().
        conn.execute("""
            CREATE TABLE IF NOT EXISTS amount_keeps (
                kind      TEXT    NOT NULL,
                item_id   INTEGER NOT NULL,
                stored_g  REAL    NOT NULL,
                kept_at   TEXT    NOT NULL DEFAULT (datetime('now')),
                PRIMARY KEY (kind, item_id)
            )
        """)

        # Meals whose stored bcp_g/calories/nutrient snapshot went stale
        # because a food or recipe they use changed — see
        # mark_meals_stale_for_food()/mark_meals_stale_for_recipes(). Drained
        # by web/backend.py's _refresh_stale_meals() before the next page load.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stale_meals (
                meal_id   INTEGER PRIMARY KEY,
                marked_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)

        # Why a meal's totals were last recalculated by something other than
        # editing the meal itself — a food it uses had its data changed, or
        # one of its amounts was corrected. Past days' totals move when that
        # happens; the meal and Daily Summary pages say so from this log.
        # Duplicate-food groups the user said are NOT duplicates (Foods → 9 →
        # Find duplicate foods). Keyed by the group's sorted fdc_ids, so a new
        # copy turning up later is reported again.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS food_duplicate_dismissals (
                group_key    TEXT PRIMARY KEY,
                dismissed_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS meal_recalc_log (
                id        INTEGER PRIMARY KEY,
                meal_id   INTEGER NOT NULL REFERENCES meals(id) ON DELETE CASCADE,
                reason    TEXT NOT NULL,
                logged_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)

        # Deleting a food that a pantry entry, recipe, or logged meal still
        # points at leaves that reference aimed at an fdc_id with nothing
        # behind it — the orphan class check_db_integrity() reports and
        # repair_db_integrity() cleans up. The delete routes have refused it
        # in application code for a while (see web/backend.py
        # food_cache_delete), but nothing stopped a new code path, a script,
        # or a hand-edited database from doing it anyway. This enforces it at
        # the database itself, where it cannot be forgotten.
        #
        # A trigger rather than a foreign key on recipe_ingredients.fdc_id,
        # for two reasons a real FK can't handle: a sub-recipe ingredient row
        # stores fdc_id 0, which matches no food and never will, and adding an
        # FK to an existing table would require rebuilding it and repairing
        # every pre-existing orphan first — a trigger guards new deletions
        # without touching damage already on disk.
        #
        # "Referenced" is deliberately the same three tables, with the same
        # conditions, that food_references() reports to the user.
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_foods_no_delete_when_referenced
            BEFORE DELETE ON foods
            FOR EACH ROW
            WHEN EXISTS (SELECT 1 FROM pantry WHERE fdc_id = OLD.fdc_id)
              OR EXISTS (SELECT 1 FROM recipe_ingredients WHERE fdc_id = OLD.fdc_id)
              OR EXISTS (SELECT 1 FROM meal_items
                          WHERE item_type = 'food' AND fdc_id = OLD.fdc_id)
            BEGIN
                SELECT RAISE(ABORT,
                    'cannot delete a food still used by a pantry entry, recipe, or meal');
            END
        """)

        # Starter-data identity (see numa_app/services/demo_data.py).
        # foods.starter_key: which starter food a row was loaded from, when it
        # was given a fresh local id on load (custom foods only; a USDA or Open
        # Food Facts id means the same food everywhere and is kept as is).
        # recipes.starter_uid: a starter recipe's permanent identity, stamped
        # by scripts/export_starter_data.py — so a recipe of the user's own with
        # the same name is never mistaken for it.
        for _table, _col in (("foods", "starter_key TEXT"), ("recipes", "starter_uid TEXT"),
                             ("recipes", "updated_at TEXT")):
            try:
                conn.execute(f"ALTER TABLE {_table} ADD COLUMN {_col}")
            except sqlite3.OperationalError:
                pass
        conn.execute("UPDATE recipes SET updated_at = created_at WHERE updated_at IS NULL")

        # foods.user_edited: the user has changed this USDA / Open Food Facts
        # food's data — nutrients, portions, or its annotations (owner's
        # decision: an annotation is an edit). Kept apart from data_type, which
        # says only where the food came from, so a food can be "SR Legacy" AND
        # user-edited; shown as "SR Legacy · user-edited". Never set on a
        # custom food, whose origin already says the user made it.
        try:
            conn.execute("ALTER TABLE foods ADD COLUMN user_edited INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        else:
            # One-time backfill, only when the column is new. Before it
            # existed, user_drafted = 1 on a USDA/OFF food was the only sign of
            # an edit, except on starter foods, which load with user_drafted = 1
            # unedited. A starter GI value alone isn't the user's edit either.
            conn.execute(f"""
                UPDATE foods SET user_edited = 1
                WHERE NOT ({_LOCAL_ID_SQL}) AND (
                    (user_drafted = 1 AND COALESCE(notes, '') <> 'Starter data')
                    OR fdc_id IN (SELECT fdc_id FROM food_annotations
                                  WHERE diaas_estimate IS NOT NULL OR COALESCE(prep_context, '') <> ''
                                     OR (gi_estimate IS NOT NULL
                                         AND COALESCE(gi_source, '') <> 'Starter data (curator''s estimate)'))
                )
            """)
        # foods.source_json: what the food's own source (USDA, Open Food
        # Facts, the starter set ...) last supplied for the values NuMa
        # tracks edits on — nutrients, serving size/unit, portions. Which
        # values the user edited is then simply where the food now differs
        # from it (food_edited_keys), so no edit path has to remember to
        # record anything. NULL on custom foods, and on foods edited before
        # this existed (their source values are unknown until a refresh).
        try:
            conn.execute("ALTER TABLE foods ADD COLUMN source_json TEXT")
        except sqlite3.OperationalError:
            pass
        else:
            for _row in conn.execute(f"SELECT * FROM foods WHERE NOT ({_LOCAL_ID_SQL}) "
                                     "AND user_edited = 0").fetchall():
                conn.execute("UPDATE foods SET source_json = ? WHERE fdc_id = ?",
                             (json.dumps(_food_state(_row)), _row["fdc_id"]))
        # foods.estimated_keys_json: the nutrient keys whose values NuMa
        # estimated rather than measured — amino acids scaled from another
        # food to this one's protein (incoming_review.py). A Refresh from
        # USDA ticks a measured value over one of these by default; writing a
        # measured value clears the key. NULL = none estimated.
        try:
            conn.execute("ALTER TABLE foods ADD COLUMN estimated_keys_json TEXT")
        except sqlite3.OperationalError:
            pass
        # recipes.updated_at: when the recipe's content last changed — its own
        # fields or its ingredient list. Kept by triggers so no code path can
        # forget it. Deliberately NOT bumped by viewing (last_accessed_at), by
        # archiving, or by the automatic DCP/nutrient recalculation, none of
        # which is an edit.
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_recipes_set_updated_at_on_insert
            AFTER INSERT ON recipes FOR EACH ROW WHEN NEW.updated_at IS NULL
            BEGIN
                UPDATE recipes SET updated_at = datetime('now') WHERE id = NEW.id;
            END
        """)
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_recipes_updated_at
            AFTER UPDATE OF name, description, servings, serving_size, complete,
                            instructions, introduction, notes, total_weight,
                            total_weight_unit, total_volume, total_volume_unit
            ON recipes FOR EACH ROW
            BEGIN
                UPDATE recipes SET updated_at = datetime('now') WHERE id = NEW.id;
            END
        """)
        for _event, _row in (("INSERT", "NEW"), ("UPDATE", "NEW"), ("DELETE", "OLD")):
            conn.execute(f"""
                CREATE TRIGGER IF NOT EXISTS trg_recipe_ingredients_{_event.lower()}_touches_recipe
                AFTER {_event} ON recipe_ingredients FOR EACH ROW
                BEGIN
                    UPDATE recipes SET updated_at = datetime('now') WHERE id = {_row}.recipe_id;
                END
            """)

        _init_food_codes(conn)
        # food_versions: an older version of a food, kept on request at a
        # Refresh so past meals keep the values they were logged with (see
        # create_food_version()). The version is a foods row of its own under
        # an id in VERSION_ID range; this table ties it to its food.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS food_versions (
                fdc_id        INTEGER PRIMARY KEY,
                parent_fdc_id INTEGER NOT NULL,
                num           INTEGER NOT NULL,
                label_date    TEXT,
                before_date   TEXT,
                created_at    TEXT DEFAULT (datetime('now')),
                UNIQUE (parent_fdc_id, num)
            )
        """)

def _init_food_codes(conn: sqlite3.Connection) -> None:
    """food_codes: the short per-source number behind a food's display code
    (OFF3, AFCD1, ...) for foods from the outside sources, whose fdc_id is a
    huge synthetic negative number (see food_ids._SYNTHETIC_ID_RANGES).
    Numbered 1, 2, 3, ... per source in the order the foods arrived, and
    never deleted, so a food removed from the cache and later re-added keeps
    the code it had. A trigger assigns the number, so no insert path can
    forget to; existing foods are backfilled here, oldest first."""
    from numa_app.services.food_ids import _SYNTHETIC_ID_RANGES
    conn.execute("""
        CREATE TABLE IF NOT EXISTS food_codes (
            fdc_id  INTEGER PRIMARY KEY,
            prefix  TEXT    NOT NULL,
            num     INTEGER NOT NULL,
            UNIQUE (prefix, num)
        )
    """)
    # Same first-match-wins order as classify_food_id(), so a boundary value
    # shared by two ranges gets the same prefix in both places.
    case = " ".join(f"WHEN NEW.fdc_id BETWEEN {start} AND {end} THEN '{label}'"
                    for _k, start, end, label in _SYNTHETIC_ID_RANGES)
    conn.execute("DROP TRIGGER IF EXISTS trg_foods_assign_code")
    conn.execute(f"""
        CREATE TRIGGER trg_foods_assign_code
        AFTER INSERT ON foods FOR EACH ROW
        WHEN (CASE {case} END) IS NOT NULL
        BEGIN
            INSERT OR IGNORE INTO food_codes (fdc_id, prefix, num)
            SELECT NEW.fdc_id, p.prefix,
                   COALESCE((SELECT MAX(num) FROM food_codes WHERE prefix = p.prefix), 0) + 1
            FROM (SELECT CASE {case} END AS prefix) AS p;
        END
    """)
    for _k, start, end, label in _SYNTHETIC_ID_RANGES:
        missing = conn.execute(
            "SELECT fdc_id FROM foods WHERE fdc_id BETWEEN ? AND ? "
            "AND fdc_id NOT IN (SELECT fdc_id FROM food_codes) ORDER BY cached_at, fdc_id",
            (start, end)).fetchall()
        for row in missing:
            conn.execute(
                "INSERT INTO food_codes (fdc_id, prefix, num) SELECT ?, ?, "
                "COALESCE((SELECT MAX(num) FROM food_codes WHERE prefix = ?), 0) + 1",
                (row["fdc_id"], label, label))


# ---------------------------------------------------------------------------
# Older versions of a food (food_versions)
# ---------------------------------------------------------------------------
# A kept version is an ordinary foods row — so every meal, recipe and
# nutrient calculation that looks a food up by id works on it unchanged —
# under an id from its own band, below every source's synthetic range (see
# food_ids._SYNTHETIC_ID_RANGES). It's archived, so it stays out of search
# and pickers, and its code is its food's plus ".n" (U171477.1).

VERSION_ID_TOP = -8_000_000_000
VERSION_ID_BOTTOM = -9_000_000_000


def is_version_id(fdc_id: int | None) -> bool:
    return fdc_id is not None and VERSION_ID_BOTTOM < fdc_id <= VERSION_ID_TOP


def food_version_info(fdc_id: int) -> dict | None:
    """{"parent_fdc_id", "num", "label_date", "before_date"} for a version id, else None."""
    if not is_version_id(fdc_id):
        return None
    with get_db() as conn:
        row = conn.execute("SELECT parent_fdc_id, num, label_date, before_date FROM food_versions "
                           "WHERE fdc_id = ?", (fdc_id,)).fetchone()
    return dict(row) if row else None


def food_version_id(parent_fdc_id: int, num: int) -> int | None:
    with get_db() as conn:
        row = conn.execute("SELECT fdc_id FROM food_versions WHERE parent_fdc_id = ? AND num = ?",
                           (parent_fdc_id, num)).fetchone()
    return row["fdc_id"] if row else None


def food_versions_of(conn: sqlite3.Connection, parent_fdc_id: int) -> list[dict]:
    """A food's kept older versions, newest first, each with how many meal
    items use it."""
    return [dict(r) for r in conn.execute("""
        SELECT v.fdc_id, v.num, v.label_date, v.before_date,
               (SELECT COUNT(*) FROM meal_items mi WHERE mi.item_type = 'food' AND mi.fdc_id = v.fdc_id) AS meal_items
        FROM food_versions v WHERE v.parent_fdc_id = ? ORDER BY v.num DESC
    """, (parent_fdc_id,)).fetchall()]


def meal_items_before(conn: sqlite3.Connection, fdc_id: int, before_date: str) -> int:
    """How many meal items use this food in meals dated before before_date."""
    return conn.execute("""
        SELECT COUNT(*) FROM meal_items WHERE item_type = 'food' AND fdc_id = ?
          AND meal_id IN (SELECT id FROM meals WHERE meal_date < ?)
    """, (fdc_id, before_date)).fetchone()[0]


def _copy_row(conn: sqlite3.Connection, table: str, fdc_id: int, new_id: int, **overrides) -> None:
    cols = [r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    row = conn.execute(f"SELECT * FROM {table} WHERE fdc_id = ?", (fdc_id,)).fetchone()
    if row is None:
        return
    values = [new_id if c == "fdc_id" else overrides.get(c, row[c]) for c in cols]
    conn.execute(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})", values)


def create_food_version(conn: sqlite3.Connection, fdc_id: int, before_date: str) -> dict | None:
    """Keep the food's current values as an older version, and point every
    meal dated before before_date at it, so those meals keep the values they
    were logged with when the food itself is then updated. Recipes keep
    using the food (a recipe has no date). Its origin label gets the date
    the kept values were last written ("Branded · 2025-07-13"); its GI /
    DIAAS / prep notes and source copy go with it. Returns {"fdc_id", "num",
    "meal_items"} or None if the food isn't cached."""
    row = get_cached_food(conn, fdc_id)
    if row is None or is_version_id(fdc_id):
        return None
    num = conn.execute("SELECT COALESCE(MAX(num), 0) + 1 FROM food_versions WHERE parent_fdc_id = ?",
                       (fdc_id,)).fetchone()[0]
    lowest = conn.execute("SELECT MIN(fdc_id) FROM food_versions").fetchone()[0]
    new_id = VERSION_ID_TOP if lowest is None else lowest - 1
    label_date = (row["cached_at"] or "")[:10] or None
    data_type = f"{row['data_type']} · {label_date}" if row["data_type"] and label_date else row["data_type"]
    _copy_row(conn, "foods", fdc_id, new_id, data_type=data_type, archived=1)
    _copy_row(conn, "food_annotations", fdc_id, new_id)
    conn.execute("INSERT INTO food_versions (fdc_id, parent_fdc_id, num, label_date, before_date) "
                 "VALUES (?, ?, ?, ?, ?)", (new_id, fdc_id, num, label_date, before_date))
    moved = conn.execute("""
        UPDATE meal_items SET fdc_id = ? WHERE item_type = 'food' AND fdc_id = ?
          AND meal_id IN (SELECT id FROM meals WHERE meal_date < ?)
    """, (new_id, fdc_id, before_date)).rowcount
    return {"fdc_id": new_id, "num": num, "meal_items": moved}


def food_code_fdc_id(prefix: str, num: int) -> int | None:
    """Reverse of food_code_num(): the fdc_id behind an outside-source code
    such as OFF3, or None if no food has that code."""
    with get_db() as conn:
        row = conn.execute("SELECT fdc_id FROM food_codes WHERE prefix = ? AND num = ?",
                           (prefix, num)).fetchone()
    return row["fdc_id"] if row else None


def food_code_num(fdc_id: int) -> int | None:
    """The short per-source number for an outside-source food (see
    _init_food_codes), or None if it has none — e.g. a search result that
    was never added to the cache."""
    with get_db() as conn:
        row = conn.execute("SELECT num FROM food_codes WHERE fdc_id = ?", (fdc_id,)).fetchone()
    return row["num"] if row else None


# ---------------------------------------------------------------------------
# Food cache
# ---------------------------------------------------------------------------

def _calorie_check(conn: sqlite3.Connection, fdc_id: int,
                   nutrients: dict[str, float]) -> tuple[dict[str, float], str | None]:
    """The save-time calorie check every write to foods.nutrients_json goes
    through (cache_food, merge_user_supplied_nutrients,
    update_food_nutrients_partial, update_cached_food_profile, and
    demo_data.apply_improvements' starter refresh), so no route can leave a food with
    protein/carbs/fat but no calories (energy_check.py has the why).

    Returns (nutrients to store, "add" | "remove" | None for the calories
    estimated mark — applied by _apply_calorie_mark() once the row exists):
    - no calories, all three macros present: fill the 4/4/9 estimate, "add".
    - calories already an estimate and carried over unchanged (a save that
      didn't touch them): re-estimate from the macros as they are now, so
      editing fat updates the estimate too.
    - calories already an estimate, now a different value: someone supplied
      a real figure, "remove"."""
    from numa_app.services import energy_check as _energy
    nutrients = dict(nutrients)
    row = conn.execute("SELECT nutrients_json FROM foods WHERE fdc_id = ?", (fdc_id,)).fetchone()
    prior = json.loads(row[0]) if row and row[0] else {}
    is_estimate = "calories" in estimated_keys(conn, fdc_id) if row else False
    cal = nutrients.get("calories")
    if cal is None:
        return (nutrients, "add") if _energy.fill_missing_calories(nutrients) else (nutrients, None)
    if is_estimate:
        if prior.get("calories") is not None and float(cal) == float(prior["calories"]):
            est = _energy.atwater_estimate(nutrients)
            if est is not None and est > 0:
                nutrients["calories"] = round(est, 1)
            return nutrients, None
        return nutrients, "remove"
    return nutrients, None


def _apply_calorie_mark(conn: sqlite3.Connection, fdc_id: int, mark: str | None) -> None:
    if mark == "add":
        update_estimated_keys(conn, fdc_id, add={"calories"})
    elif mark == "remove":
        update_estimated_keys(conn, fdc_id, remove={"calories"})


def cache_food(conn: sqlite3.Connection, fdc_id: int, name: str, data_type: str,
               brand: str | None, serving_size: float | None, serving_unit: str | None,
               nutrients: dict[str, float], portions: list[dict] | None = None,
               *, user_drafted: bool = False, notes: str | None = None,
               curator_notes: str | None = None, from_source: bool = True) -> None:
    """Store a food, or overwrite the data columns of one already cached.

    from_source (the default): the data is the food's own source's — a USDA
    or Open Food Facts fetch, a bundled dataset, the starter set — so it
    also becomes the food's source copy (foods.source_json). Pass False for
    data the user brought in (imports), which is an edit of the food.

    An upsert, not INSERT OR REPLACE. REPLACE deletes the existing row and
    inserts a new one, and that delete sets off food_annotations' ON DELETE
    CASCADE: re-caching a food silently erased its GI / DIAAS / prep-note
    annotations, and reset its archived flag and every column not listed
    here (user_edited, starter_key). Updating in place keeps all of them."""
    nutrients, calorie_mark = _calorie_check(conn, fdc_id, nutrients)
    conn.execute("""
        INSERT INTO foods
            (fdc_id, name, data_type, brand, serving_size, serving_unit,
             nutrients_json, portions_json, user_drafted, notes, curator_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(fdc_id) DO UPDATE SET
            name = excluded.name, data_type = excluded.data_type, brand = excluded.brand,
            serving_size = excluded.serving_size, serving_unit = excluded.serving_unit,
            nutrients_json = excluded.nutrients_json, portions_json = excluded.portions_json,
            user_drafted = excluded.user_drafted, notes = excluded.notes,
            curator_notes = excluded.curator_notes, cached_at = datetime('now')
    """, (
        fdc_id, name, data_type, brand, serving_size, serving_unit,
        json.dumps(nutrients), json.dumps(portions or []),
        1 if user_drafted else 0, notes or None, curator_notes or None
    ))
    _apply_calorie_mark(conn, fdc_id, calorie_mark)
    if from_source and not is_custom_food_id(fdc_id):
        snapshot_food_source(conn, fdc_id)


def get_cached_food(conn: sqlite3.Connection, fdc_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM foods WHERE fdc_id = ?", (fdc_id,)
    ).fetchone()


def list_cached_foods(conn: sqlite3.Connection, *, include_archived: bool = False) -> list[sqlite3.Row]:
    archived_clause = "" if include_archived else "WHERE archived = 0"
    return conn.execute(
        "SELECT fdc_id, name, data_type, brand, serving_size, serving_unit, "
        "nutrients_json, portions_json, notes, curator_notes, archived "
        f"FROM foods {archived_clause} ORDER BY name"
    ).fetchall()


def delete_cached_food(conn: sqlite3.Connection, fdc_id: int) -> bool:
    """Delete a food from the cache. Returns True if a row was deleted."""
    cur = conn.execute("DELETE FROM foods WHERE fdc_id = ?", (fdc_id,))
    return cur.rowcount > 0


def set_food_archived(conn: sqlite3.Connection, fdc_id: int, archived: bool) -> None:
    """Archive (hide from search/complements/default lists, protect from prune) or restore a cached food."""
    conn.execute("UPDATE foods SET archived = ? WHERE fdc_id = ?", (1 if archived else 0, fdc_id))


def food_references(conn: sqlite3.Connection, fdc_id: int) -> dict[str, list[int]]:
    """Return the ids of pantry entries, recipes, and meals still referencing this food.

    Each list is truthy/falsy exactly like the counts this used to return, so
    callers that only check `if refs["pantry"]` etc. still work unchanged.
    """
    pantry_ids = [r[0] for r in conn.execute(
        "SELECT id FROM pantry WHERE fdc_id = ?", (fdc_id,)
    ).fetchall()]
    recipe_ids = [r[0] for r in conn.execute(
        "SELECT DISTINCT recipe_id FROM recipe_ingredients WHERE fdc_id = ?", (fdc_id,)
    ).fetchall()]
    meal_ids = [r[0] for r in conn.execute(
        "SELECT DISTINCT meal_id FROM meal_items WHERE item_type = 'food' AND fdc_id = ?", (fdc_id,)
    ).fetchall()]
    return {"pantry": pantry_ids, "recipes": recipe_ids, "meals": meal_ids}


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


def prune_unused_cached_foods(
    conn: sqlite3.Connection, *, include_drafted: bool = False, keep_ids: set[int] | None = None
) -> list[sqlite3.Row]:
    """Delete cache foods not referenced by pantry, recipes, or meals.

    `keep_ids`: fdc_ids to leave alone even though they're unused — e.g. rows
    the user unchecked on the prune-preview page. None (the default) deletes
    every unused food, matching the old all-or-nothing behavior.

    Returns the rows that were deleted (fdc_id, name, data_type, brand,
    user_drafted), so a caller can report or log what was removed. Re-derives
    the unused set itself rather than trusting a caller-supplied id list, so a
    food that became referenced (or was archived) between page load and
    submit can't be deleted by a stale/tampered form. See
    list_unused_cached_foods() for the include_drafted semantics — callers
    that want a confirm-before-delete flow should call that first and pass
    the same include_drafted value here.
    """
    unused = list_unused_cached_foods(conn, include_drafted=include_drafted)
    to_delete = [row for row in unused if not keep_ids or row["fdc_id"] not in keep_ids]
    for row in to_delete:
        conn.execute("DELETE FROM foods WHERE fdc_id = ?", (row["fdc_id"],))
    return to_delete


def check_db_integrity(conn: sqlite3.Connection) -> dict[str, list[dict]]:
    """Scan for referential-integrity problems the app's own code paths should
    never create, but a past bug (or a manually edited DB) can — chiefly a
    pantry/recipe/meal row that still points at an fdc_id no longer in the
    foods cache (e.g. deleted via /food/cache/delete before that route
    refused to delete still-referenced foods). Opening such a food's page
    fails, since it's treated as "not cached" and the app tries to re-fetch
    it from USDA by fdc_id — which errors for negative (Open Food Facts)
    fdc_ids and returns the wrong food for reused-looking positive ones.

    Read-only — does not modify the database. See repair_db_integrity() to
    clean up what this finds.

    Returns a dict keyed by issue category, each a list of plain dicts
    describing the offending row:
        orphaned_pantry            — pantry entries pointing at a missing food
        orphaned_recipe_ingredients — recipe ingredients pointing at a missing
                                      food (sub-recipe ingredients are excluded;
                                      those are tracked separately via
                                      ref_recipe_id/ref_recipe_deleted, see
                                      orphaned_recipe_refs)
        orphaned_meal_items        — meal items pointing at a missing food or recipe
        orphaned_recipe_refs       — recipe-ingredient sub-recipe references
                                      pointing at a missing recipe without
                                      ref_recipe_deleted having been set (should
                                      be unreachable via delete_recipe(), which
                                      sets that flag itself — a backstop for drift)
        bad_json                   — foods rows whose nutrients_json/portions_json
                                      isn't valid JSON
    """
    issues: dict[str, list[dict]] = {
        "orphaned_pantry": [], "orphaned_recipe_ingredients": [],
        "orphaned_meal_items": [], "orphaned_recipe_refs": [], "bad_json": [],
    }

    for row in conn.execute("""
        SELECT id, food_name, fdc_id FROM pantry
        WHERE fdc_id IS NOT NULL AND fdc_id NOT IN (SELECT fdc_id FROM foods)
    """):
        issues["orphaned_pantry"].append(dict(row))

    for row in conn.execute("""
        SELECT ri.id, ri.recipe_id, r.name AS recipe_name, ri.food_name, ri.fdc_id
        FROM recipe_ingredients ri
        LEFT JOIN recipes r ON r.id = ri.recipe_id
        WHERE ri.ref_recipe_id IS NULL AND ri.fdc_id != 0
          AND ri.fdc_id NOT IN (SELECT fdc_id FROM foods)
    """):
        issues["orphaned_recipe_ingredients"].append(dict(row))

    for row in conn.execute("""
        SELECT mi.id, mi.meal_id, m.meal_date, mi.food_name, mi.fdc_id
        FROM meal_items mi
        LEFT JOIN meals m ON m.id = mi.meal_id
        WHERE mi.item_type = 'food' AND mi.fdc_id IS NOT NULL
          AND mi.fdc_id NOT IN (SELECT fdc_id FROM foods)
    """):
        issues["orphaned_meal_items"].append(dict(row))

    for row in conn.execute("""
        SELECT mi.id, mi.meal_id, m.meal_date, mi.food_name, mi.recipe_id
        FROM meal_items mi
        LEFT JOIN meals m ON m.id = mi.meal_id
        WHERE mi.item_type = 'recipe' AND mi.recipe_id IS NOT NULL
          AND mi.recipe_id NOT IN (SELECT id FROM recipes)
    """):
        issues["orphaned_meal_items"].append(dict(row))

    for row in conn.execute("""
        SELECT id, recipe_id, food_name, ref_recipe_id FROM recipe_ingredients
        WHERE ref_recipe_id IS NOT NULL AND ref_recipe_deleted = 0
          AND ref_recipe_id NOT IN (SELECT id FROM recipes)
    """):
        issues["orphaned_recipe_refs"].append(dict(row))

    for row in conn.execute("SELECT fdc_id, name, nutrients_json, portions_json FROM foods"):
        for field in ("nutrients_json", "portions_json"):
            val = row[field]
            if val is None:
                continue
            try:
                json.loads(val)
            except (ValueError, TypeError):
                issues["bad_json"].append({"fdc_id": row["fdc_id"], "name": row["name"], "field": field})

    return issues


REPAIRABLE_ISSUE_CATEGORIES = (
    "orphaned_pantry", "orphaned_recipe_ingredients", "orphaned_meal_items", "orphaned_recipe_refs",
)


def repair_db_integrity(conn: sqlite3.Connection, categories: set[str] | None = None) -> dict[str, int]:
    """Remove or fix the dangling rows check_db_integrity() finds — the food
    or recipe they point at is genuinely gone, so there's nothing left to
    repoint them at. Re-scans internally rather than trusting a
    caller-supplied issue list, for the same staleness reason
    prune_unused_cached_foods() re-scans.

    `categories`: which of REPAIRABLE_ISSUE_CATEGORIES to act on. None (the
    default) acts on all of them. Lets the web UI offer one "Remove these"
    button per category — each has a very different real-world consequence
    (deleting a pantry entry vs. deleting an ingredient out of a recipe vs.
    deleting a food from a day's logged meal history vs. flagging a
    sub-recipe reference as deleted, non-destructively), so bundling them
    into one action would hide that from the user.

    bad_json is deliberately never auto-repaired, in any category set — a
    malformed nutrients blob needs a human decision (fix by hand, delete, or
    re-fetch), not a silent deletion.

    Returns counts of rows removed/fixed per category.
    """
    issues = check_db_integrity(conn)
    active = categories if categories is not None else set(REPAIRABLE_ISSUE_CATEGORIES)
    counts: dict[str, int] = {}

    if "orphaned_pantry" in active and issues["orphaned_pantry"]:
        ids = [r["id"] for r in issues["orphaned_pantry"]]
        conn.executemany("DELETE FROM pantry WHERE id = ?", [(i,) for i in ids])
        counts["orphaned_pantry"] = len(ids)

    if "orphaned_recipe_ingredients" in active and issues["orphaned_recipe_ingredients"]:
        ids = [r["id"] for r in issues["orphaned_recipe_ingredients"]]
        conn.executemany("DELETE FROM recipe_ingredients WHERE id = ?", [(i,) for i in ids])
        counts["orphaned_recipe_ingredients"] = len(ids)

    if "orphaned_meal_items" in active and issues["orphaned_meal_items"]:
        ids = [r["id"] for r in issues["orphaned_meal_items"]]
        conn.executemany("DELETE FROM meal_items WHERE id = ?", [(i,) for i in ids])
        counts["orphaned_meal_items"] = len(ids)

    if "orphaned_recipe_refs" in active and issues["orphaned_recipe_refs"]:
        ids = [r["id"] for r in issues["orphaned_recipe_refs"]]
        conn.executemany(
            "UPDATE recipe_ingredients SET ref_recipe_id = NULL, ref_recipe_deleted = 1 WHERE id = ?",
            [(i,) for i in ids],
        )
        counts["orphaned_recipe_refs"] = len(ids)

    return counts


# Generic prep/state and marketing/descriptor words common across many
# unrelated food names — too weak to justify surfacing a user-drafted food
# on their own in the OR-fallback search (see search_cached_foods). E.g.
# "triskitt original" (a typo'd "triskitt" plus "original") must not surface
# "Triscuit Organic Original Crackers" on "original" alone.
_OR_FALLBACK_STOPWORDS = {
    "raw", "cooked", "fresh", "dried", "frozen", "canned", "whole",
    "ground", "sliced", "diced", "chopped", "boiled", "roasted", "baked",
    "grilled", "steamed", "plain",
    "original", "organic", "classic", "traditional",
}


def _singular_variant(word: str) -> str | None:
    """Return a plausible singular form of `word`, or None if not plural-looking."""
    lw = word.lower()
    if lw.endswith("ies") and len(lw) > 3:
        return lw[:-3] + "y"
    if lw.endswith("es") and len(lw) > 2:
        return lw[:-2]
    if lw.endswith("s") and len(lw) > 1:
        return lw[:-1]
    return None


def search_cached_foods(conn: sqlite3.Connection, query: str, *, include_archived: bool = False) -> list[sqlite3.Row]:
    words = query.split()
    if not words:
        return []
    # Bare-digit words (e.g. the "1" in "coffee 1") match almost any dosage or
    # serving-size substring — excluding them from the OR match keeps unrelated
    # user-drafted foods like "B12 5000mcg" from surfacing for "coffee 1".
    match_words = [w for w in words if not w.isdigit()] or words
    select = ("SELECT fdc_id, name, data_type, brand, serving_size, serving_unit, "
               "portions_json, notes, nutrients_json, archived FROM foods")
    archived_clause = "" if include_archived else "AND archived = 0"
    # Each query word also tries its singular form, so e.g. "potatoes" matches
    # cached/drafted names stored as singular "Potato, cooked".
    word_variants = [[w] + ([_singular_variant(w)] if _singular_variant(w) and _singular_variant(w) != w else []) for w in match_words]
    # All-words match for the general cache — each word may match by either form
    and_groups = []
    and_params: list[str] = []
    for variants in word_variants:
        and_groups.append("(" + " OR ".join("name LIKE ?" for _ in variants) + ")")
        and_params.extend(f"%{v}%" for v in variants)
    and_cond = " AND ".join(and_groups)
    and_rows = conn.execute(f"{select} WHERE {and_cond} {archived_clause} ORDER BY name", and_params).fetchall()
    # Any-word match for user-drafted foods — so "vitamin d" finds "D3 50 mcg" etc.
    # Generic prep/state words are excluded from triggering this fallback on
    # their own: "orange raw" shouldn't surface "Raw Brazil Nuts" just because
    # both happen to contain "raw" — that's a coincidence, not a real match.
    or_match_words = [w for w in match_words if w.lower() not in _OR_FALLBACK_STOPWORDS] or match_words
    or_word_variants = [[w] + ([_singular_variant(w)] if _singular_variant(w) and _singular_variant(w) != w else []) for w in or_match_words]
    or_params = [f"%{v}%" for variants in or_word_variants for v in variants]
    or_cond = " OR ".join("name LIKE ?" for _ in or_params)
    or_rows = conn.execute(
        f"{select} WHERE user_drafted = 1 AND ({or_cond}) {archived_clause} ORDER BY name", or_params
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
    gi_source: str | None = None,
) -> None:
    """Update annotation fields for a food. Pass None to leave a field unchanged.
    gi_no_prompt / diaas_no_prompt: 0 = re-enable prompts, 1 = suppress prompts.

    Any caller writing gi_estimate should write gi_source too (even to say where
    a hand-typed value came from): the fields are only meaningful together, and
    leaving gi_source alone here would keep an older value's provenance beside a
    new number."""
    conn.execute("""
        INSERT INTO food_annotations
            (fdc_id, gi_estimate, gi_source, gi_no_prompt, diaas_estimate, diaas_no_prompt,
             prep_context, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(fdc_id) DO UPDATE SET
            gi_estimate     = COALESCE(excluded.gi_estimate,     gi_estimate),
            gi_source       = COALESCE(excluded.gi_source,       gi_source),
            gi_no_prompt    = COALESCE(excluded.gi_no_prompt,    gi_no_prompt),
            diaas_estimate  = COALESCE(excluded.diaas_estimate,  diaas_estimate),
            diaas_no_prompt = COALESCE(excluded.diaas_no_prompt, diaas_no_prompt),
            prep_context    = COALESCE(excluded.prep_context,    prep_context),
            updated_at      = datetime('now')
    """, (fdc_id, gi_estimate, gi_source, gi_no_prompt, diaas_estimate, diaas_no_prompt,
          prep_context))


def set_food_annotation(
    conn: sqlite3.Connection,
    fdc_id: int,
    *,
    gi_estimate: float | None,
    gi_no_prompt: bool,
    diaas_estimate: float | None,
    diaas_no_prompt: bool,
    prep_context: str | None,
    gi_source: str | None = None,
    reviewed: bool = True,
) -> None:
    """Write all annotation fields at once (explicit NULLs clear existing values).
    Use this for web forms; use upsert_food_annotation for a single field-at-a-time update.

    reviewed defaults to True because this is the whole-form writer: saving the
    Annotate form means the user has been shown both estimates and settled them,
    even if they left one blank on purpose. That stops the add-a-food detour
    firing again for this food (see _annotation_prompt_needed()). Pass False to
    write annotation values without counting as a review.

    gi_source is the provenance of gi_estimate — the reference-table row a value
    was picked from (see gi_lookup.py). It is descriptive text only, and is
    meaningless without gi_estimate, so it is dropped whenever that is None."""
    if gi_estimate is None:
        gi_source = None
    conn.execute("""
        INSERT INTO food_annotations
            (fdc_id, gi_estimate, gi_source, gi_no_prompt, diaas_estimate, diaas_no_prompt,
             prep_context, reviewed, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(fdc_id) DO UPDATE SET
            gi_estimate     = excluded.gi_estimate,
            gi_source       = excluded.gi_source,
            gi_no_prompt    = excluded.gi_no_prompt,
            diaas_estimate  = excluded.diaas_estimate,
            diaas_no_prompt = excluded.diaas_no_prompt,
            prep_context    = excluded.prep_context,
            -- Never un-reviews a food: a later non-review write (a GI seed
            -- import, say) must not make an already-settled food start
            -- interrupting again.
            reviewed        = MAX(excluded.reviewed, food_annotations.reviewed),
            updated_at      = datetime('now')
    """, (fdc_id, gi_estimate, gi_source, 1 if gi_no_prompt else 0,
          diaas_estimate, 1 if diaas_no_prompt else 0, prep_context,
          1 if reviewed else 0))
    # Clearing the last annotation can end a food's user-edited status.
    refresh_user_edited(conn, fdc_id)


def delete_food_annotation(conn: sqlite3.Connection, fdc_id: int) -> None:
    conn.execute("DELETE FROM food_annotations WHERE fdc_id = ?", (fdc_id,))
    refresh_user_edited(conn, fdc_id)


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
                  complete: bool = False,
                  introduction: str | None = None,
                  notes: str | None = None) -> int:
    cur = conn.execute("""
        INSERT INTO recipes (name, description, servings, instructions,
                             total_volume, total_volume_unit,
                             total_weight, total_weight_unit,
                             serving_size, complete, introduction, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, description or None, servings, instructions or None,
          total_volume, total_volume_unit or None,
          total_weight, total_weight_unit or None,
          serving_size or None, 1 if complete else 0, introduction or None,
          notes or None))
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
        "SELECT id, name, description, servings, serving_size, dcp_g, dcp_computed_at, created_at, complete,"
        " last_accessed_at, total_weight, total_weight_unit, total_volume, total_volume_unit, archived"
        f" FROM recipes {archived_clause} ORDER BY name"
    ).fetchall()


def recipe_list_recent(conn: sqlite3.Connection, limit: int = 20, *, include_archived: bool = False) -> list[sqlite3.Row]:
    archived_clause = "" if include_archived else "WHERE archived = 0"
    return conn.execute(
        "SELECT id, name, description, servings, serving_size, dcp_g, dcp_computed_at, created_at, complete,"
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


def recipe_translation_create(conn: sqlite3.Connection, recipe_id: int, language: str, data: dict) -> int:
    cur = conn.execute(
        "INSERT INTO recipe_translations (recipe_id, language, data_json) VALUES (?, ?, ?)",
        (recipe_id, language, json.dumps(data)),
    )
    return cur.lastrowid


def recipe_translation_list(conn: sqlite3.Connection, recipe_id: int) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id, recipe_id, language, created_at FROM recipe_translations "
        "WHERE recipe_id = ? ORDER BY created_at DESC",
        (recipe_id,),
    ).fetchall()


def recipe_translation_get(conn: sqlite3.Connection, translation_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM recipe_translations WHERE id = ?", (translation_id,)
    ).fetchone()


def recipe_translation_delete(conn: sqlite3.Connection, translation_id: int) -> bool:
    cur = conn.execute("DELETE FROM recipe_translations WHERE id = ?", (translation_id,))
    return cur.rowcount > 0


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
                  complete: bool = False,
                  introduction: str | None = None,
                  notes: str | None = None) -> None:
    """Every text field is written on every call, so a caller that edits one
    of them (e.g. the Instructions or Introduction save buttons, each of
    which posts its own route) has to pass the recipe's current values for
    the others through, or they are cleared."""
    conn.execute(
        "UPDATE recipes SET name=?, description=?, servings=?, instructions=?, "
        "total_volume=?, total_volume_unit=?, total_weight=?, total_weight_unit=?, "
        "serving_size=?, complete=?, introduction=?, notes=? WHERE id=?",
        (name, description or None, servings, instructions or None,
         total_volume, total_volume_unit or None,
         total_weight, total_weight_unit or None,
         serving_size or None, 1 if complete else 0, introduction or None,
         notes or None, recipe_id)
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


def recipes_containing_food(conn: sqlite3.Connection, fdc_id: int) -> list[sqlite3.Row]:
    """Return (id, name) rows for recipes that use `fdc_id` as a direct ingredient."""
    return conn.execute("""
        SELECT DISTINCT r.id, r.name
        FROM recipe_ingredients ri
        JOIN recipes r ON r.id = ri.recipe_id
        WHERE ri.fdc_id = ?
        ORDER BY r.name
    """, (fdc_id,)).fetchall()


def recipes_missing_dcp(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return (id, name) rows for recipes with no stored per-serving DCP —
    the ones the recipes list shows as "NC". Used for the startup repair
    pass that gives each of them one recompute attempt, so a recipe left
    stale by a write that changed an ingredient's nutrients without
    cascading can't sit at NC while its own page computes a real DCP."""
    return conn.execute(
        "SELECT id, name FROM recipes WHERE dcp_g IS NULL ORDER BY id"
    ).fetchall()


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


MIN_RELINK_SHARED_WORDS = 2


def _name_matches_for_relink(candidate_name: str, target_name: str, target_words: set[str]) -> bool:
    """True if `candidate_name` is plausibly the same recipe as `target_name`:
    either an exact match (case/whitespace-insensitive — always allowed, even
    for a single-word name like "Chili" recreated as "Chili"), or sharing at
    least MIN_RELINK_SHARED_WORDS words. A single shared word (e.g. both
    names merely containing "protein") is too weak a signal on its own — see
    recipe_edit's broken_groups for the false-match case this was tightened
    to avoid."""
    if candidate_name.strip().lower() == target_name.strip().lower():
        return True
    return len(_name_words(candidate_name) & target_words) >= MIN_RELINK_SHARED_WORDS


def find_broken_recipe_refs(conn: sqlite3.Connection, name: str) -> dict:
    """Fuzzy-find meal_items and recipe_ingredients rows left dangling by a
    deleted recipe, for offering to relink them when a recipe is (re-)created.
    See _name_matches_for_relink for the match rule.

    Because a fuzzy search can turn up broken refs left by more than one
    distinct deleted recipe, each row carries its original name as
    `matched_name` — callers should offer/relink one matched_name group at a
    time (see relink_recipe_refs) rather than assuming every match belongs
    to the same original recipe. See find_relink_candidates() for offering
    alternative target recipes beyond the one currently being edited.

    Returns {"meals": [rows...], "recipes": [rows...]}.
    """
    words = _name_words(name)
    if not words:
        return {"meals": [], "recipes": []}
    all_meals, all_recipes = _all_broken_recipe_refs(conn)
    meals = [row for row in all_meals if _name_matches_for_relink(row["matched_name"], name, words)]
    recipes = [row for row in all_recipes if _name_matches_for_relink(row["matched_name"], name, words)]
    return {"meals": meals, "recipes": recipes}


def find_relink_candidates(conn: sqlite3.Connection, matched_name: str) -> list[dict]:
    """Live recipes plausibly matching `matched_name` (the deleted recipe's
    original name) per _name_matches_for_relink, ranked by how many words
    they share — offered as alternative relink targets alongside whichever
    recipe the user happens to be editing, since that may not be the recipe
    they actually meant to recreate.

    Returns [{"id", "name", "shared_words"}, ...] sorted by shared_words desc,
    then name.
    """
    words = _name_words(matched_name)
    if not words:
        return []
    candidates = []
    for row in conn.execute("SELECT id, name FROM recipes"):
        if _name_matches_for_relink(row["name"], matched_name, words):
            shared = len(_name_words(row["name"]) & words)
            candidates.append({"id": row["id"], "name": row["name"], "shared_words": shared})
    candidates.sort(key=lambda c: (-c["shared_words"], c["name"].lower()))
    return candidates


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
    pooled DIAAS analysis), day_pct_goal (the
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


def day_completion_map(conn: sqlite3.Connection) -> dict[str, bool]:
    """meal_date -> True if every meal logged on that date is marked
    complete. Used by the Recent Days table (Daily Summary and its /summary
    landing page) so a day with an in-progress meal is visibly flagged,
    matching the same "day_provisional" concept Meals & Log already shows
    per meal — see last_complete_meal_date below for the related
    single-most-recent-date lookup used by the Nutrient Plot's rolling
    anchor."""
    rows = conn.execute(
        """
        SELECT meal_date, SUM(CASE WHEN complete = 0 THEN 1 ELSE 0 END) AS incomplete_count
        FROM meals
        GROUP BY meal_date
        """
    ).fetchall()
    return {r["meal_date"]: r["incomplete_count"] == 0 for r in rows}


def last_complete_meal_date(conn: sqlite3.Connection) -> str | None:
    """Most recent meal_date where every meal is marked complete, or None if
    no such date exists (no meals logged at all, or even the earliest day
    still has an incomplete meal). Used by "roll to the last complete day"
    features (e.g. the Nutrient Plot) instead of assuming "yesterday" —
    a day the user has explicitly marked done can be today."""
    row = conn.execute(
        """
        SELECT meal_date
        FROM meals
        GROUP BY meal_date
        HAVING SUM(CASE WHEN complete = 0 THEN 1 ELSE 0 END) = 0
        ORDER BY meal_date DESC
        LIMIT 1
        """
    ).fetchone()
    return row["meal_date"] if row else None


def meal_dates_with_incomplete(conn: sqlite3.Connection) -> set[str]:
    """Every meal_date with at least one meal not marked complete — days the
    Nutrient Plot's "always end on the last complete day" mode leaves out (as
    a break in the line), since a partly logged day's totals would drag the
    line down."""
    return {r[0] for r in conn.execute("SELECT DISTINCT meal_date FROM meals WHERE complete = 0")}


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
    tuple for the recipe itself, plus one ("food") tuple per base ingredient,
    recursively expanded through nested sub-recipes via ref_recipe_id — each
    nested sub-recipe also gets its own ("recipe") tuple, so a sub-recipe that
    is eaten only inside other recipes still shows up as consumed.

    has_protein reflects the food's cached protein_g > 0 (False if the food
    isn't cached). A recipe row's has_protein is True if any of its
    (recursively) expanded ingredients has_protein.

    deleted is True for a "recipe" row whose recipe_id no longer exists in the
    recipes table (the recipe was deleted after this meal referenced it). The
    meal item's stored food_name is used as a fallback label in that case, and
    it has no expanded ingredients.

    recipe_id is the stable identifier for a "recipe" row — always meal_items'
    recipe_id for a directly-added recipe (even after deletion, since that
    column is never cleared), the ref_recipe_id for a live nested sub-recipe,
    or None for "food" rows and for a nested sub-recipe that was itself deleted (ref_recipe_id is cleared on delete, so
    no id survives — see recipe_delete()). Callers should key/group recipe
    rows by recipe_id when present rather than by name, since a recipe's name
    can change after a meal references it while its id stays fixed.

    A "food" row's name is the food's *current* cached name, not the label
    stored on the meal item/ingredient at the time it was added — a food can
    be renamed later (e.g. via Edit Food), and every past reference should
    read with its current name rather than a stale snapshot. Falls back to
    the stored label if the food is no longer in the cache at all.
    """
    def _expand_recipe(recipe_id: int) -> list[tuple[int | None, str, str, bool, bool, int | None]]:
        out: list[tuple[int | None, str, str, bool, bool, int | None]] = []
        for ing in recipe_get_ingredients(conn, recipe_id):
            if ing["ref_recipe_deleted"]:
                out.append((None, ing["food_name"], "recipe", False, True, None))
            elif ing["ref_recipe_id"]:
                sub = recipe_get(conn, ing["ref_recipe_id"])
                sub_rows = _expand_recipe(ing["ref_recipe_id"]) if sub else []
                name = sub["name"] if sub else ing["food_name"]
                out.append((None, name, "recipe", any(r[3] for r in sub_rows), False, ing["ref_recipe_id"]))
                out.extend(sub_rows)
            else:
                out.append((ing["fdc_id"], _current_food_name(conn, ing["fdc_id"], ing["food_name"]),
                            "food", _food_has_protein(conn, ing["fdc_id"]), False, None))
        return out

    result: list[tuple[int | None, str, str, bool, bool, int | None]] = []
    for item in meal_get_items(conn, meal_id):
        if item["item_type"] == "food":
            result.append((item["fdc_id"], _current_food_name(conn, item["fdc_id"], item["food_name"]),
                          "food", _food_has_protein(conn, item["fdc_id"]), False, None))
        elif item["item_type"] == "recipe":
            live_recipe = recipe_get(conn, item["recipe_id"])
            recipe_deleted = live_recipe is None
            expanded = [] if recipe_deleted else _expand_recipe(item["recipe_id"])
            display_name = live_recipe["name"] if live_recipe else item["food_name"]
            result.append((None, display_name, "recipe", any(e[3] for e in expanded), recipe_deleted, item["recipe_id"]))
            result.extend(expanded)
    return result


def _food_has_protein(conn: sqlite3.Connection, fdc_id: int) -> bool:
    cached = get_cached_food(conn, fdc_id)
    if not cached:
        return False
    nutrients = json.loads(cached["nutrients_json"])
    return nutrients.get("protein_g", 0) > 0


def _current_food_name(conn: sqlite3.Connection, fdc_id: int, fallback: str) -> str:
    cached = get_cached_food(conn, fdc_id)
    return cached["name"] if cached else fallback


def recipe_expand_ingredient_use(conn: sqlite3.Connection, recipe_id: int) -> list[tuple[int | None, str, str, bool, int | None]]:
    """Flatten a recipe's ingredient tree into (fdc_id, name, kind, has_protein, ref_recipe_id)
    rows, for the "Food Use in Recipes" analysis — like meal_expand_food_items's
    _expand_recipe, a sub-recipe ingredient gets its own "recipe" row *and* its
    ingredients are also recursed into, so a frequently-reused sub-recipe (e.g. a
    house dressing) is visible as its own line.

    A "food" row's name is the food's current cached name (see
    meal_expand_food_items's docstring for why); a "recipe" row's name is the
    sub-recipe's current name.
    """
    out: list[tuple[int | None, str, str, bool, int | None]] = []
    for ing in recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_deleted"]:
            out.append((None, ing["food_name"], "recipe", False, None))
        elif ing["ref_recipe_id"]:
            sub = recipe_get(conn, ing["ref_recipe_id"])
            sub_rows = recipe_expand_ingredient_use(conn, ing["ref_recipe_id"]) if sub else []
            name = sub["name"] if sub else ing["food_name"]
            out.append((None, name, "recipe", any(r[3] for r in sub_rows), ing["ref_recipe_id"]))
            out.extend(sub_rows)
        else:
            out.append((ing["fdc_id"], _current_food_name(conn, ing["fdc_id"], ing["food_name"]),
                        "food", _food_has_protein(conn, ing["fdc_id"]), None))
    return out


def recipe_list_by_created_range(conn: sqlite3.Connection, start_date: str, end_date: str) -> list[sqlite3.Row]:
    """Recipes created within [start_date, end_date] (inclusive, by calendar day)."""
    return conn.execute(
        "SELECT * FROM recipes WHERE date(created_at) BETWEEN ? AND ? ORDER BY created_at",
        (start_date, end_date)
    ).fetchall()


def recipe_list_by_ids(conn: sqlite3.Connection, ids: list[int]) -> list[sqlite3.Row]:
    """Return recipes matching the given IDs, ordered by name. Missing IDs are silently omitted."""
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    return conn.execute(
        f"SELECT * FROM recipes WHERE id IN ({placeholders}) ORDER BY name",
        ids
    ).fetchall()


def item_current_name(conn: sqlite3.Connection, kind: str, item_id: int) -> str | None:
    """Current display name of a food (kind="food", item_id=fdc_id) or recipe
    (kind="recipe", item_id=recipe id), or None if it no longer exists —
    used to validate a substitution's replacement target before writing it
    everywhere, and to label the new rows with a real, current name."""
    if kind == "food":
        row = get_cached_food(conn, item_id)
        return row["name"] if row else None
    row = recipe_get(conn, item_id)
    return row["name"] if row else None


def substitute_item_in_meals(conn: sqlite3.Connection, meal_ids: list[int],
                             old_kind: str, old_id: int, new_kind: str, new_id: int) -> int:
    """Replace direct meal-item references to (old_kind, old_id) with
    (new_kind, new_id), restricted to meal_items belonging to meal_ids.
    Returns the number of rows changed.

    Only *directly added* meal items are reachable this way — a food used as
    an ingredient inside a recipe that a meal references isn't touched (that
    recipe's ingredient list is a shared, recipe-level thing; substitute
    inside it via substitute_item_in_recipes instead, scoped to that recipe).
    """
    if not meal_ids or old_kind not in ("food", "recipe") or new_kind not in ("food", "recipe"):
        return 0
    new_name = item_current_name(conn, new_kind, new_id)
    if new_name is None:
        raise ValueError("Replacement food/recipe not found.")
    placeholders = ",".join("?" * len(meal_ids))
    old_col = "fdc_id" if old_kind == "food" else "recipe_id"
    if new_kind == "food":
        set_sql = "item_type='food', fdc_id=?, recipe_id=NULL, food_name=?"
    else:
        set_sql = "item_type='recipe', fdc_id=NULL, recipe_id=?, food_name=?"
    cur = conn.execute(
        f"UPDATE meal_items SET {set_sql} "
        f"WHERE meal_id IN ({placeholders}) AND item_type=? AND {old_col}=?",
        (new_id, new_name, *meal_ids, old_kind, old_id)
    )
    return cur.rowcount


def substitute_item_in_recipes(conn: sqlite3.Connection, recipe_ids: list[int],
                               old_kind: str, old_id: int, new_kind: str, new_id: int) -> list[int]:
    """Replace ingredient references to (old_kind, old_id) with (new_kind, new_id)
    across the ingredient lists of recipe_ids. Returns the distinct container
    recipe ids that had at least one ingredient changed, so the caller can
    recompute their DCP (recompute_recipe_dcp already cascades up to any
    ancestor recipe that in turn uses one of these as a sub-recipe).

    A recipe is never allowed to end up referencing itself as an ingredient
    (matches the same guard used when adding a sub-recipe ingredient by
    hand) — a container recipe is skipped if new_kind is "recipe" and new_id
    equals that container's own id.
    """
    if not recipe_ids or old_kind not in ("food", "recipe") or new_kind not in ("food", "recipe"):
        return []
    new_name = item_current_name(conn, new_kind, new_id)
    if new_name is None:
        raise ValueError("Replacement food/recipe not found.")
    placeholders = ",".join("?" * len(recipe_ids))
    old_col = "fdc_id" if old_kind == "food" else "ref_recipe_id"
    self_ref_guard = " AND recipe_id != ?" if new_kind == "recipe" else ""
    params: list = [old_id]
    if new_kind == "recipe":
        params.append(new_id)

    affected = conn.execute(
        f"SELECT DISTINCT recipe_id FROM recipe_ingredients "
        f"WHERE recipe_id IN ({placeholders}) AND {old_col}=?{self_ref_guard}",
        (*recipe_ids, *params)
    ).fetchall()
    affected_ids = [row["recipe_id"] for row in affected]
    if not affected_ids:
        return []

    if new_kind == "food":
        set_sql = "fdc_id=?, ref_recipe_id=NULL, ref_recipe_deleted=0, food_name=?"
    else:
        set_sql = "fdc_id=0, ref_recipe_id=?, ref_recipe_deleted=0, food_name=?"
    conn.execute(
        f"UPDATE recipe_ingredients SET {set_sql} "
        f"WHERE recipe_id IN ({placeholders}) AND {old_col}=?{self_ref_guard}",
        (new_id, new_name, *recipe_ids, *params)
    )
    return affected_ids


def meal_update_item(conn: sqlite3.Connection, item_id: int, meal_id: int,
                     amount: float, unit: str) -> None:
    conn.execute(
        "UPDATE meal_items SET amount=?, unit=? WHERE id=? AND meal_id=?",
        (amount, unit, item_id, meal_id)
    )


def meal_item_set_serving_grams(conn: sqlite3.Connection, item_id: int,
                                serving_grams: float | None) -> None:
    conn.execute("UPDATE meal_items SET serving_grams=? WHERE id=?", (serving_grams, item_id))


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
               mi.recipe_id, mi.amount, mi.unit, mi.notes, mi.serving_grams
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
    # A per-meal bcp_g change can make the pooled day-level snapshot in
    # day_bcp_cache stale (it's only refreshed by visiting /summary/{date}),
    # so drop it and let meal_dates_with_bcp() fall back to summing bcp_g
    # until the pooled value is recomputed.
    conn.execute(
        "DELETE FROM day_bcp_cache WHERE meal_date = "
        "(SELECT meal_date FROM meals WHERE id = ?)",
        (meal_id,),
    )


def mark_meals_stale_for_food(conn: sqlite3.Connection, fdc_id: int) -> None:
    """Flag every meal that logs `fdc_id` directly as a food item, so its
    stored DCP/calories/nutrient snapshot is recomputed (meals using the food
    through a recipe are flagged via mark_meals_stale_for_recipes())."""
    conn.execute(
        "INSERT OR IGNORE INTO stale_meals (meal_id) "
        "SELECT DISTINCT meal_id FROM meal_items WHERE item_type = 'food' AND fdc_id = ?",
        (fdc_id,),
    )


def mark_meals_stale_for_recipes(conn: sqlite3.Connection, recipe_ids) -> None:
    """Flag every meal that logs any of `recipe_ids` as a recipe item."""
    ids = list(recipe_ids)
    if not ids:
        return
    placeholders = ",".join("?" * len(ids))
    conn.execute(
        "INSERT OR IGNORE INTO stale_meals (meal_id) "
        f"SELECT DISTINCT meal_id FROM meal_items WHERE item_type = 'recipe' AND recipe_id IN ({placeholders})",
        ids,
    )


def recipes_using_food(conn: sqlite3.Connection, fdc_id: int) -> list[int]:
    """Every recipe that uses `fdc_id`, directly or inside a sub-recipe at
    any depth."""
    return [r[0] for r in conn.execute("""
        WITH RECURSIVE r(id) AS (
            SELECT recipe_id FROM recipe_ingredients WHERE fdc_id = ?
            UNION
            SELECT ri.recipe_id FROM recipe_ingredients ri JOIN r ON ri.ref_recipe_id = r.id
        )
        SELECT id FROM r ORDER BY id
    """, (fdc_id,))]


def meals_using_food(conn: sqlite3.Connection, fdc_id: int) -> list[int]:
    """Every logged meal that includes `fdc_id`, directly or through a recipe."""
    recipe_ids = recipes_using_food(conn, fdc_id)
    placeholders = ",".join("?" * len(recipe_ids)) or "NULL"
    return [r[0] for r in conn.execute(
        "SELECT DISTINCT meal_id FROM meal_items WHERE (item_type = 'food' AND fdc_id = ?) "
        f"OR (item_type = 'recipe' AND recipe_id IN ({placeholders})) ORDER BY meal_id",
        (fdc_id, *recipe_ids))]


def recipe_and_ancestors(conn: sqlite3.Connection, recipe_id: int) -> list[int]:
    """`recipe_id` plus every recipe that uses it as a sub-recipe, at any depth."""
    return [r[0] for r in conn.execute("""
        WITH RECURSIVE r(id) AS (
            SELECT ?
            UNION
            SELECT ri.recipe_id FROM recipe_ingredients ri JOIN r ON ri.ref_recipe_id = r.id
        )
        SELECT id FROM r ORDER BY id
    """, (recipe_id,))]


def meals_using_recipes(conn: sqlite3.Connection, recipe_ids) -> list[int]:
    ids = list(recipe_ids)
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    return [r[0] for r in conn.execute(
        f"SELECT DISTINCT meal_id FROM meal_items WHERE item_type = 'recipe' AND recipe_id IN ({placeholders})",
        ids)]


def duplicate_dismissals(conn: sqlite3.Connection) -> set[str]:
    return {r[0] for r in conn.execute("SELECT group_key FROM food_duplicate_dismissals")}


def dismiss_duplicate_group(conn: sqlite3.Connection, group_key: str) -> None:
    conn.execute("INSERT OR IGNORE INTO food_duplicate_dismissals (group_key) VALUES (?)", (group_key,))


def merge_food_into(conn: sqlite3.Connection, keep_id: int, drop_id: int) -> dict[str, int]:
    """Replace food `drop_id` with `keep_id` everywhere — recipe ingredients,
    logged meal items, pantry entries — then delete `drop_id`. Each line keeps
    its own name and grams (same as a rename: the line's label is a record).
    GI/DIAAS annotations and the oxalate link move over only where the kept
    food has none. Returns how many rows were re-pointed, per table. The
    caller recomputes (recipe_dcp.cascade_food_change(keep_id))."""
    counts = {}
    for table, extra in (("recipe_ingredients", ""), ("meal_items", " AND item_type = 'food'"), ("pantry", "")):
        cur = conn.execute(f"UPDATE {table} SET fdc_id = ? WHERE fdc_id = ?{extra}", (keep_id, drop_id))
        counts[table] = cur.rowcount
    for table in ("food_annotations", "oxalate_links"):
        if not conn.execute(f"SELECT 1 FROM {table} WHERE fdc_id = ?", (keep_id,)).fetchone():
            conn.execute(f"UPDATE {table} SET fdc_id = ? WHERE fdc_id = ?", (keep_id, drop_id))
    delete_cached_food(conn, drop_id)
    return counts


def amount_keeps(conn: sqlite3.Connection) -> dict[tuple[str, int], float]:
    """{(kind, item_id): stored_g} for every "Keep as entered" choice — see
    the amount_keeps table and data_quality.stale_amounts()."""
    return {(r[0], r[1]): r[2] for r in conn.execute("SELECT kind, item_id, stored_g FROM amount_keeps")}


def amount_keep(conn: sqlite3.Connection, kind: str, item_id: int, stored_g: float) -> None:
    conn.execute("INSERT OR REPLACE INTO amount_keeps (kind, item_id, stored_g) VALUES (?, ?, ?)",
                 (kind, item_id, stored_g))


def amount_unkeep(conn: sqlite3.Connection, kind: str, item_id: int) -> None:
    conn.execute("DELETE FROM amount_keeps WHERE kind = ? AND item_id = ?", (kind, item_id))


def mark_meal_stale(conn: sqlite3.Connection, meal_id: int) -> None:
    conn.execute("INSERT OR IGNORE INTO stale_meals (meal_id) VALUES (?)", (meal_id,))


def log_meal_recalc(conn: sqlite3.Connection, meal_ids, reason: str) -> None:
    conn.executemany("INSERT INTO meal_recalc_log (meal_id, reason) VALUES (?, ?)",
                     [(m, reason) for m in meal_ids])


def meal_recalc_notes(conn: sqlite3.Connection, meal_ids, limit: int = 3) -> list[sqlite3.Row]:
    """The latest distinct recalculation reasons for these meals, newest first."""
    ids = list(meal_ids)
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    return conn.execute(
        "SELECT reason, MAX(logged_at) AS logged_at FROM meal_recalc_log "
        f"WHERE meal_id IN ({placeholders}) GROUP BY reason ORDER BY logged_at DESC LIMIT ?",
        (*ids, limit)).fetchall()


def stale_meal_ids(conn: sqlite3.Connection) -> list[int]:
    return [r["meal_id"] for r in conn.execute("SELECT meal_id FROM stale_meals ORDER BY meal_id")]


def clear_stale_meal(conn: sqlite3.Connection, meal_id: int) -> None:
    conn.execute("DELETE FROM stale_meals WHERE meal_id = ?", (meal_id,))


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

# A custom food's id: a purely local counter (see next_user_drafted_fdc_id()).
# Anything else is a USDA id (positive) or a deterministic Open Food Facts id
# (-1,000,000,000 or below), which names the same food in every database.
_LOCAL_ID_SQL = "fdc_id < 0 AND fdc_id > -1000000000"


def is_custom_food_id(fdc_id: int) -> bool:
    return -1_000_000_000 < fdc_id < 0


def mark_user_edited(conn: sqlite3.Connection, fdc_id: int) -> None:
    """Record that the user may have changed this food's data (see
    foods.user_edited). With a source copy the flag is worked out from it
    (refresh_user_edited) — so an "edit" that leaves every value as the
    source has it isn't one. Without one (an edit from before source copies
    existed, or user data for a food never fetched from its source) there's
    nothing to compare against, so the flag is simply set. A no-op on a
    custom food."""
    if is_custom_food_id(fdc_id):
        return
    row = conn.execute("SELECT source_json FROM foods WHERE fdc_id = ?", (fdc_id,)).fetchone()
    if row is None:
        return
    if row["source_json"] is None:
        conn.execute("UPDATE foods SET user_edited = 1 WHERE fdc_id = ?", (fdc_id,))
    else:
        refresh_user_edited(conn, fdc_id)


# ---------------------------------------------------------------------------
# Source copy — value-level edit tracking (foods.source_json)
# ---------------------------------------------------------------------------
# Tracked: every nutrient, serving size and unit, and portions. Not tracked:
# name, brand and type — renaming a food was never an edit of its data.

_TRACKED_SCALARS = ("serving_size", "serving_unit")
PORTION_KEY_PREFIX = "portion:"


def _food_state(row) -> dict:
    """The tracked values of a foods row, in source_json's shape."""
    return {
        "nutrients": json.loads(row["nutrients_json"]) if row["nutrients_json"] else {},
        "portions": (json.loads(row["portions_json"]) if row["portions_json"] else None) or [],
        "serving_size": row["serving_size"],
        "serving_unit": row["serving_unit"],
    }


def _same_value(a, b) -> bool:
    if a in (None, "") and b in (None, ""):
        return True
    if a in (None, "") or b in (None, ""):
        return False
    try:
        return abs(float(a) - float(b)) <= max(1e-9, 1e-6 * max(abs(float(a)), abs(float(b))))
    except (TypeError, ValueError):
        return str(a).strip() == str(b).strip()


def _portion_desc(p: dict) -> str:
    """A portion's name — "description" in the app's own shape; anything
    else falls back to the whole entry, so an unexpected shape still
    compares rather than being silently skipped."""
    desc = str(p.get("description") or p.get("label") or "").strip()
    return desc or json.dumps(p, sort_keys=True)


def _portion_grams(p: dict):
    return p.get("gram_weight", p.get("grams"))


def _portions_by_desc(portions) -> dict[str, dict]:
    return {_portion_desc(p).lower(): p for p in portions or [] if isinstance(p, dict)}


def diff_from_source(current: dict, source: dict, *, estimated: "set[str] | frozenset[str]" = frozenset()) -> list[str]:
    """The tracked values where `current` differs from `source` (both in
    _food_state's shape): nutrient keys, "serving_size"/"serving_unit", and
    "portion:<description>" for a portion the source doesn't have or has
    with a different weight. Portions are one-way — a source portion the
    food lacks (an offered addition left unticked) isn't the user's value.
    A calorie figure NuMa estimated isn't either."""
    from numa_app.services.data_completeness import is_blank
    cur_n, src_n = current.get("nutrients") or {}, source.get("nutrients") or {}
    keys = []
    for k in sorted(set(cur_n) | set(src_n)):
        cur_blank, src_blank = is_blank(k, cur_n), is_blank(k, src_n)
        if cur_blank and src_blank:
            continue
        # A calorie figure NuMa estimated from the macros is never the
        # user's value (one they type stops being an estimate), and it
        # follows the macros, so it's judged through them instead.
        if k == "calories" and "calories" in estimated:
            continue
        if cur_blank != src_blank or not _same_value(cur_n[k], src_n[k]):
            keys.append(k)
    for f in _TRACKED_SCALARS:
        if not _same_value(current.get(f), source.get(f)):
            keys.append(f)
    src_p = _portions_by_desc(source.get("portions"))
    for desc, p in _portions_by_desc(current.get("portions")).items():
        if desc not in src_p or not _same_value(_portion_grams(p), _portion_grams(src_p[desc])):
            keys.append(PORTION_KEY_PREFIX + _portion_desc(p))
    return keys


def food_source(conn: sqlite3.Connection, fdc_id: int) -> dict | None:
    """The food's source copy, or None (custom food, or source unknown)."""
    row = conn.execute("SELECT source_json FROM foods WHERE fdc_id = ?", (fdc_id,)).fetchone()
    if not row or not row["source_json"]:
        return None
    try:
        return json.loads(row["source_json"])
    except ValueError:
        return None


def food_edited_keys(conn: sqlite3.Connection, fdc_id: int) -> list[str] | None:
    """Which tracked values the user has changed from the source's (see
    diff_from_source), or None when that can't be known: a custom food (all
    its values are the user's), or a food edited before source copies
    existed and not refreshed since."""
    if is_custom_food_id(fdc_id):
        return None
    row = get_cached_food(conn, fdc_id)
    source = food_source(conn, fdc_id)
    if row is None or source is None:
        return None
    return diff_from_source(_food_state(row), source, estimated=estimated_keys(conn, fdc_id))


def has_user_annotation(conn: sqlite3.Connection, fdc_id: int) -> bool:
    """A GI / DIAAS / prep note the user added — an edit (owner's decision).
    A starter GI value isn't the user's."""
    return conn.execute("""
        SELECT 1 FROM food_annotations WHERE fdc_id = ? AND (
            diaas_estimate IS NOT NULL OR COALESCE(prep_context, '') <> ''
            OR (gi_estimate IS NOT NULL
                AND COALESCE(gi_source, '') <> 'Starter data (curator''s estimate)'))
    """, (fdc_id,)).fetchone() is not None


def refresh_user_edited(conn: sqlite3.Connection, fdc_id: int) -> None:
    """Re-derive foods.user_edited from the source copy and annotations. Left
    alone when there's no source copy (see mark_user_edited)."""
    if is_custom_food_id(fdc_id) or food_source(conn, fdc_id) is None:
        return
    edited = bool(food_edited_keys(conn, fdc_id)) or has_user_annotation(conn, fdc_id)
    conn.execute("UPDATE foods SET user_edited = ? WHERE fdc_id = ?", (1 if edited else 0, fdc_id))


def set_food_source(conn: sqlite3.Connection, fdc_id: int, source: dict) -> None:
    if is_custom_food_id(fdc_id):
        return
    conn.execute("UPDATE foods SET source_json = ? WHERE fdc_id = ?", (json.dumps(source), fdc_id))
    refresh_user_edited(conn, fdc_id)


def snapshot_food_source(conn: sqlite3.Connection, fdc_id: int) -> None:
    """The food's values as they are now ARE its source's (just fetched, or
    reset to the starter version): make them its source copy."""
    row = get_cached_food(conn, fdc_id)
    if row is not None:
        set_food_source(conn, fdc_id, _food_state(row))


def rebase_food_source(conn: sqlite3.Connection, fdc_id: int, incoming: dict) -> None:
    """A fresh copy from the source has been reviewed (whatever was or wasn't
    taken from it): it becomes the source copy — see rebased_source(). A
    food with no source copy (edited before they existed) gets its first
    one here."""
    row = get_cached_food(conn, fdc_id)
    if row is not None:
        set_food_source(conn, fdc_id, rebased_source(food_source(conn, fdc_id), _food_state(row), incoming))


def rebased_source(old: dict | None, current: dict, incoming: dict) -> dict:
    """The source copy after a fresh copy `incoming` arrives. What the fresh
    copy lacks, the old copy still vouches for — a value the source dropped,
    or an old portion the refresh doesn't replace — so a value the user
    never touched doesn't start counting as their edit."""
    from numa_app.services.data_completeness import is_blank
    old = old or {}
    inc_n = incoming.get("nutrients") or {}
    nutrients = {k: v for k, v in inc_n.items() if not is_blank(k, inc_n)}
    for k, v in (old.get("nutrients") or {}).items():
        if k not in nutrients:
            nutrients[k] = v
    new = {"nutrients": nutrients}
    for f in _TRACKED_SCALARS:
        # USDA leaves serving size out for most non-branded foods; with no
        # earlier copy to say otherwise, the food's own is taken as the
        # source's rather than counted as the user's.
        fallback = old.get(f) if old else current.get(f)
        new[f] = incoming.get(f) if incoming.get(f) not in (None, "") else fallback
    cur_p = _portions_by_desc(current.get("portions"))
    old_p = _portions_by_desc(old.get("portions"))
    portions, seen = [], set()
    for p in incoming.get("portions") or []:
        if not isinstance(p, dict):
            continue
        desc = _portion_desc(p).lower()
        if desc in seen:
            continue
        seen.add(desc)
        # Refresh never replaces a portion the food has; if the food still has
        # the old source weight, that's the source's too, not the user's.
        mine = cur_p.get(desc)
        if (mine is not None and desc in old_p
                and _same_value(_portion_grams(mine), _portion_grams(old_p[desc]))):
            portions.append(old_p[desc])
        else:
            portions.append(p)
    portions += [p for d, p in old_p.items() if d not in seen]
    new["portions"] = portions
    return new


def edits_left_after_full_refresh(conn: sqlite3.Connection, fdc_id: int, incoming: dict) -> bool:
    """Would this food still be user-edited after taking EVERY value a fresh
    copy offers? True when something no tick can undo remains: a GI / DIAAS /
    prep note, a portion of the user's own, or a value of the user's that
    the source no longer lists. The review screen adds any unticked value."""
    row = get_cached_food(conn, fdc_id)
    if row is None or is_custom_food_id(fdc_id):
        return False
    if has_user_annotation(conn, fdc_id):
        return True
    current = _food_state(row)
    new_base = rebased_source(food_source(conn, fdc_id), current, incoming)
    taken = dict(current)
    taken["nutrients"] = {**current["nutrients"],
                          **{k: v for k, v in (incoming.get("nutrients") or {}).items() if v is not None}}
    for f in _TRACKED_SCALARS:
        if incoming.get(f) not in (None, ""):
            taken[f] = incoming[f]
    return bool(diff_from_source(taken, new_base, estimated=estimated_keys(conn, fdc_id)))


_FOOD_FIELD_COLUMNS = ("name", "brand", "data_type", "serving_size", "serving_unit", "portions")


def update_food_fields(conn: sqlite3.Connection, fdc_id: int, **fields) -> None:
    """Change only the named descriptive columns of a cached food (name,
    brand, data_type, serving_size, serving_unit, portions — the last as a
    list, stored as JSON), leaving nutrients, flags and notes alone. Used by
    the incoming-data review (numa_app/services/incoming_review.py)."""
    sets, values = [], []
    for key, value in fields.items():
        if key not in _FOOD_FIELD_COLUMNS:
            raise ValueError(f"not an updatable food field: {key}")
        if key == "portions":
            sets.append("portions_json = ?")
            values.append(json.dumps(value or []))
        else:
            sets.append(f"{key} = ?")
            values.append(value)
    if sets:
        conn.execute(f"UPDATE foods SET {', '.join(sets)} WHERE fdc_id = ?", (*values, fdc_id))
        refresh_user_edited(conn, fdc_id)


def estimated_keys(conn: sqlite3.Connection, fdc_id: int) -> set[str]:
    """Nutrient keys on this food whose values are estimates (see
    foods.estimated_keys_json)."""
    row = conn.execute("SELECT estimated_keys_json FROM foods WHERE fdc_id = ?", (fdc_id,)).fetchone()
    if not row or not row[0]:
        return set()
    try:
        return set(json.loads(row[0]))
    except ValueError:
        return set()


def update_estimated_keys(conn: sqlite3.Connection, fdc_id: int, *,
                          add: "set[str] | list[str]" = (), remove: "set[str] | list[str]" = ()) -> None:
    """Mark keys as estimated (add) or measured again (remove)."""
    keys = (estimated_keys(conn, fdc_id) | set(add)) - set(remove)
    conn.execute("UPDATE foods SET estimated_keys_json = ? WHERE fdc_id = ?",
                 (json.dumps(sorted(keys)) if keys else None, fdc_id))


def cache_user_supplied_food(conn: sqlite3.Connection, *, fdc_id: int, data_type: str, **kwargs) -> None:
    """cache_food() for data the user brought in themselves (the Claude
    fetch/import workflows, import_foods.py, import_json_folder.py).

    For a USDA or Open Food Facts food this is the user's edit of that food:
    it is marked user-edited, and its origin is kept. Those imports label
    everything "User Drafted", which used to overwrite a USDA food's real
    type ("SR Legacy", "Branded", ...) for good."""
    prior = get_cached_food(conn, fdc_id)
    if (not is_custom_food_id(fdc_id) and data_type == "User Drafted" and prior is not None
            and prior["data_type"] and prior["data_type"] != "User Drafted"):
        data_type = prior["data_type"]
    cache_food(conn, fdc_id=fdc_id, data_type=data_type, from_source=False, **kwargs)
    mark_user_edited(conn, fdc_id)


def merge_user_supplied_nutrients(conn: sqlite3.Connection, fdc_id: int, new: dict[str, float],
                                  *, overwrite: bool = False, notes: str | None = None,
                                  curator_notes: str | None = None,
                                  mark_edited: bool = True) -> tuple[list[str], list[str]]:
    """Add imported nutrient values to a food already in the cache, leaving
    every other column (name, type, portions, brand, ...) as it is.

    Only blank values are filled (data_completeness.is_blank) unless
    overwrite=True. Returns (keys written, keys left alone because the food
    already had a value). Notes are appended, not replaced."""
    from numa_app.services.data_completeness import is_blank
    row = get_cached_food(conn, fdc_id)
    existing = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
    written, kept = [], []
    for k, v in new.items():
        if overwrite or is_blank(k, existing):
            written.append(k)
        else:
            kept.append(k)
    existing.update({k: new[k] for k in written})
    existing, calorie_mark = _calorie_check(conn, fdc_id, existing)

    def _append(old, extra):
        if not extra or (old and extra in old):
            return old
        return f"{old}  |  {extra}" if old else extra

    conn.execute(
        "UPDATE foods SET nutrients_json = ?, notes = ?, curator_notes = ?, "
        "cached_at = datetime('now') WHERE fdc_id = ?",
        (json.dumps(existing), _append(row["notes"], notes),
         _append(row["curator_notes"], curator_notes), fdc_id),
    )
    _apply_calorie_mark(conn, fdc_id, calorie_mark)
    # mark_edited=False: the values are the food's own source's (a USDA
    # refresh), so they go into its source copy too rather than counting as
    # the user's edit.
    if written and mark_edited:
        mark_user_edited(conn, fdc_id)
    elif written:
        source = food_source(conn, fdc_id)
        if source is not None:
            source.setdefault("nutrients", {}).update({k: existing[k] for k in written})
            set_food_source(conn, fdc_id, source)
    return written, kept


def food_data_ignores(conn: sqlite3.Connection) -> dict[int, set[str]]:
    """fdc_id -> nutrient groups the user marked not needed for that food."""
    out: dict[int, set[str]] = {}
    for r in conn.execute("SELECT fdc_id, group_key FROM food_data_ignores"):
        out.setdefault(r["fdc_id"], set()).add(r["group_key"])
    return out


def set_food_data_ignore(conn: sqlite3.Connection, fdc_id: int, group_key: str, ignored: bool) -> None:
    if ignored:
        conn.execute("INSERT OR IGNORE INTO food_data_ignores (fdc_id, group_key) VALUES (?, ?)",
                     (fdc_id, group_key))
    else:
        conn.execute("DELETE FROM food_data_ignores WHERE fdc_id = ? AND group_key = ?",
                     (fdc_id, group_key))


def user_edited_ids(conn: sqlite3.Connection) -> set[int]:
    return {r[0] for r in conn.execute("SELECT fdc_id FROM foods WHERE user_edited = 1").fetchall()}


def next_user_drafted_fdc_id(conn: sqlite3.Connection) -> int:
    # Scoped to (-1_000_000_000, 0) so this never wanders into a reserved
    # external-source range (see food_ids._SYNTHETIC_ID_RANGES /
    # openfoodfacts._OFF_ID_BASE), which would mislabel the new draft.
    row = conn.execute(
        "SELECT MIN(fdc_id) AS min_id FROM foods WHERE fdc_id < 0 AND fdc_id > -1000000000"
    ).fetchone()
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
    existing, calorie_mark = _calorie_check(conn, fdc_id, existing)
    conn.execute(
        "UPDATE foods SET nutrients_json = ?, cached_at = datetime('now') WHERE fdc_id = ?",
        (json.dumps(existing), fdc_id),
    )
    _apply_calorie_mark(conn, fdc_id, calorie_mark)
    refresh_user_edited(conn, fdc_id)


# ---------------------------------------------------------------------------
# Saved comparisons
# ---------------------------------------------------------------------------

def saved_mixed_comparison_save(
    conn: sqlite3.Connection,
    name: str,
    items: list[dict],
) -> int:
    cur = conn.execute(
        "INSERT INTO saved_mixed_comparisons (name, items) VALUES (?, ?)",
        (name, json.dumps(items)),
    )
    return cur.lastrowid


def saved_mixed_comparison_list(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id, name, items, created_at FROM saved_mixed_comparisons ORDER BY created_at DESC"
    ).fetchall()


def saved_mixed_comparison_get(conn: sqlite3.Connection, cmp_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT id, name, items, created_at FROM saved_mixed_comparisons WHERE id = ?",
        (cmp_id,),
    ).fetchone()


def saved_mixed_comparison_rename(conn: sqlite3.Connection, cmp_id: int, name: str) -> bool:
    cur = conn.execute("UPDATE saved_mixed_comparisons SET name = ? WHERE id = ?", (name, cmp_id))
    return cur.rowcount > 0


def saved_mixed_comparison_delete(conn: sqlite3.Connection, cmp_id: int) -> bool:
    cur = conn.execute("DELETE FROM saved_mixed_comparisons WHERE id = ?", (cmp_id,))
    return cur.rowcount > 0


def update_food_portions(conn: sqlite3.Connection, fdc_id: int, portions: list[dict]) -> None:
    """Patch only the portions_json column for a cached food. Only the
    Portions editor calls this, so it is always the user's edit."""
    conn.execute(
        "UPDATE foods SET portions_json=? WHERE fdc_id=?",
        (json.dumps(portions), fdc_id),
    )
    mark_user_edited(conn, fdc_id)


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
    nutrients, calorie_mark = _calorie_check(conn, fdc_id, nutrients)
    conn.execute(
        "UPDATE foods SET name=?, data_type=?, brand=?, serving_size=?, serving_unit=?, "
        "nutrients_json=?, portions_json=?, user_drafted=?, notes=?, cached_at=(datetime('now')) "
        "WHERE fdc_id=?",
        (
            name, data_type, brand, serving_size, serving_unit,
            json.dumps(nutrients), json.dumps(portions or []),
            1 if user_drafted else 0, notes or None,
            fdc_id,
        ),
    )
    # user_drafted=True is a user's edit; False is a fresh copy of the
    # source's data (the full USDA refresh), which becomes the source copy.
    _apply_calorie_mark(conn, fdc_id, calorie_mark)
    if user_drafted:
        mark_user_edited(conn, fdc_id)
    else:
        snapshot_food_source(conn, fdc_id)


def rename_cached_food(conn: sqlite3.Connection, fdc_id: int, new_name: str) -> None:
    """Change only a cached food's name, touching nothing else -- notably
    NOT user_drafted, unlike update_cached_food_profile() above. Used for
    the "* " starter-data name toggle on a real USDA/OFF food's detail page:
    that toggle must not mark the food user-modified, or it would silently
    block that food from ever refreshing from USDA again (see the
    "Edit protection" behavior in user-manual.md)."""
    conn.execute("UPDATE foods SET name=? WHERE fdc_id=?", (new_name, fdc_id))


# ---------------------------------------------------------------------------
# Recompute error log
# ---------------------------------------------------------------------------

def log_recompute_error(conn: sqlite3.Connection, entity_type: str, entity_id: int | None, message: str) -> None:
    """Record a cascade/recompute failure so it's visible later instead of vanishing
    into a swallowed exception. Not for expected non-computability (e.g. a recipe
    missing amino acid data) — only for genuine failures during a cascade step."""
    conn.execute(
        "INSERT INTO recompute_errors (entity_type, entity_id, message) VALUES (?, ?, ?)",
        (entity_type, entity_id, message),
    )


def get_recompute_error(conn: sqlite3.Connection, error_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT id, occurred_at, entity_type, entity_id, message FROM recompute_errors WHERE id = ?",
        (error_id,),
    ).fetchone()


def list_unresolved_recompute_errors(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id, occurred_at, entity_type, entity_id, message, banner_ack_at "
        "FROM recompute_errors WHERE resolved_at IS NULL ORDER BY occurred_at DESC"
    ).fetchall()


def list_unacked_recompute_errors(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Unresolved errors the home-page banner hasn't been dismissed for yet."""
    return conn.execute(
        "SELECT id, occurred_at, entity_type, entity_id, message "
        "FROM recompute_errors WHERE resolved_at IS NULL AND banner_ack_at IS NULL "
        "ORDER BY occurred_at DESC"
    ).fetchall()


def update_recompute_error(conn: sqlite3.Connection, error_id: int, message: str) -> None:
    """Refresh an existing unresolved entry's message/timestamp after a failed
    retry, instead of piling up a new row for every retry attempt on the same
    recipe. Also re-arms the home-page banner (clears banner_ack_at) since
    this is functionally a new failure the user hasn't seen yet."""
    conn.execute(
        "UPDATE recompute_errors SET message = ?, occurred_at = datetime('now'), banner_ack_at = NULL "
        "WHERE id = ?",
        (message, error_id),
    )


def resolve_recompute_error(conn: sqlite3.Connection, error_id: int) -> bool:
    cur = conn.execute(
        "UPDATE recompute_errors SET resolved_at = datetime('now') WHERE id = ?", (error_id,)
    )
    return cur.rowcount > 0


def ack_recompute_errors_banner(conn: sqlite3.Connection) -> None:
    """'Got it, don't remind again' — silences the home-page banner for every
    currently-outstanding error without marking them resolved; they still show
    on the Settings page until actually addressed."""
    conn.execute(
        "UPDATE recompute_errors SET banner_ack_at = datetime('now') "
        "WHERE resolved_at IS NULL AND banner_ack_at IS NULL"
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
