"""Populate oxalate.db from oxalate_source_data.py.

Run once (or to refresh after updating source data):
    python build_oxalate_db.py

The generated oxalate.db is committed to the repo so end users
do not need to run this script.
"""

import pathlib
import sqlite3
import sys

from oxalate_source_data import OXALATE_FOODS, SOURCE_URL, SOURCE_CREDIT, SOURCE_DATE

DB_PATH = pathlib.Path(__file__).parent / "oxalate.db"


def build() -> None:
    DB_PATH.unlink(missing_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            CREATE TABLE oxalate_foods (
                id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                food_group              TEXT NOT NULL,
                food_name               TEXT NOT NULL,
                serving_size            TEXT,
                oxalate_mg_per_serving  REAL,
                oxalate_mg_per_100g     REAL,
                category                TEXT,
                directly_measured       INTEGER DEFAULT 0,
                source_note             TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE source_info (
                key   TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.executemany(
            "INSERT INTO source_info VALUES (?, ?)",
            [
                ("url",    SOURCE_URL),
                ("credit", SOURCE_CREDIT),
                ("date",   SOURCE_DATE),
            ],
        )
        rows = [
            (
                f["group"],
                f["food_name"],
                f["serving_size"],
                f["oxalate_mg_per_serving"],
                f["oxalate_mg_per_100g"],
                f["category"],
                1 if f["directly_measured"] else 0,
                SOURCE_CREDIT,
            )
            for f in OXALATE_FOODS
        ]
        conn.executemany(
            """INSERT INTO oxalate_foods
               (food_group, food_name, serving_size, oxalate_mg_per_serving,
                oxalate_mg_per_100g, category, directly_measured, source_note)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            rows,
        )
        conn.commit()
        print(f"Built {DB_PATH} — {len(rows)} foods inserted.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    build()
    sys.exit(0)
