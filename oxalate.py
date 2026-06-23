"""oxalate.py — Access the oxalate reference database (oxalate.db).

oxalate.db is a static SQLite file bundled with the app and populated from
oxalate_source_data.py by running build_oxalate_db.py. It is never written
to at runtime — all user-specific data (which food maps to which oxalate
record) lives in the user's numa.db via the oxalate_links table.

Docs: README-numa-documentation.md, Architecture: "Oxalate Data"
"""

from __future__ import annotations

import difflib
import pathlib
import sqlite3
from contextlib import contextmanager
from typing import Generator

_OXALATE_DB_PATH = pathlib.Path(__file__).parent / "oxalate.db"

CATEGORY_ORDER = ("very high", "high", "moderate", "low", "negligible")


@contextmanager
def get_oxalate_db() -> Generator[sqlite3.Connection, None, None]:
    """Yield a read-only sqlite3.Connection to oxalate.db.
    Raises FileNotFoundError if oxalate.db has not been built yet."""
    if not _OXALATE_DB_PATH.exists():
        raise FileNotFoundError(
            f"oxalate.db not found at {_OXALATE_DB_PATH}. "
            "Run  python build_oxalate_db.py  to build it."
        )
    conn = sqlite3.connect(f"file:{_OXALATE_DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def is_available() -> bool:
    """Return True if oxalate.db exists and is queryable."""
    return _OXALATE_DB_PATH.exists()


def get_by_id(conn: sqlite3.Connection, oxalate_id: int) -> sqlite3.Row | None:
    """Fetch a single oxalate_foods row by its primary key."""
    return conn.execute(
        "SELECT * FROM oxalate_foods WHERE id = ?", (oxalate_id,)
    ).fetchone()


def search_similar(
    conn: sqlite3.Connection,
    food_name: str,
    top_n: int = 5,
) -> list[tuple[float, sqlite3.Row]]:
    """Return up to top_n (score, row) pairs for oxalate_foods records similar to food_name.

    Uses a two-pass approach:
    1. SQLite LIKE query for broad candidate retrieval (first word of food_name).
    2. difflib.SequenceMatcher for ranking (stdlib, no external deps).

    Returned list is sorted by score descending (best match first).
    Scores are in [0, 1]; 1.0 = identical string.
    """
    name_lower = food_name.lower().strip()
    first_word = name_lower.split()[0] if name_lower.split() else name_lower

    # Broad candidate pool: first word LIKE match + all "very high" / "high" foods
    rows = conn.execute(
        """
        SELECT * FROM oxalate_foods
        WHERE lower(food_name) LIKE ?
           OR category IN ('very high', 'high')
        """,
        (f"%{first_word}%",),
    ).fetchall()

    # Also pull a general substring match on any word of the query
    for word in name_lower.split()[1:]:
        if len(word) >= 4:
            extra = conn.execute(
                "SELECT * FROM oxalate_foods WHERE lower(food_name) LIKE ?",
                (f"%{word}%",),
            ).fetchall()
            seen_ids = {r["id"] for r in rows}
            rows += [r for r in extra if r["id"] not in seen_ids]

    # Score with SequenceMatcher
    scored = []
    for row in rows:
        ratio = difflib.SequenceMatcher(
            None, name_lower, row["food_name"].lower()
        ).ratio()
        scored.append((ratio, row))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_n]


def format_oxalate(row: sqlite3.Row) -> str:
    """Return a concise display string for an oxalate record, e.g. '72.0 mg / 1 oz  [high]'."""
    parts = []
    if row["oxalate_mg_per_serving"] is not None:
        parts.append(f"{row['oxalate_mg_per_serving']:.1f} mg")
    if row["serving_size"]:
        parts.append(f"/ {row['serving_size']}")
    if row["oxalate_mg_per_100g"] is not None:
        parts.append(f"= {row['oxalate_mg_per_100g']:.0f} mg/100g")
    cat = row["category"] or ""
    cat_str = f"  [{cat}]" if cat else ""
    return "  ".join(parts) + cat_str


def category_label(category: str | None) -> str:
    """Return a short display label for a category string."""
    labels = {
        "very high":  "Very High",
        "high":       "High",
        "moderate":   "Moderate",
        "low":        "Low",
        "negligible": "Negligible",
    }
    return labels.get(category or "", category or "Unknown")
