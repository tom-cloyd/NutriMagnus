#!/usr/bin/env python3
"""
restore_food_origins.py — give back their real origin to USDA foods whose
type was overwritten with "User Drafted", and mark them user-edited.

A food's data_type says where it came from ("SR Legacy", "Branded",
"Foundation", ...); whether the user has changed it is a separate fact,
foods.user_edited (see db.py). Before the two were separated, editing or
importing data for a USDA food could replace its type with "User Drafted",
losing the origin. The only reliable way to recover it is to ask USDA, one
request per food, which is what this does.

Nutrients, portions, names and annotations are never touched: only
data_type, and user_edited = 1 (the food was, after all, changed by the
user — that's how it got relabelled).

Custom foods (local ids, see db.next_user_drafted_fdc_id()) and Open Food
Facts foods are skipped: "User Drafted" is their true origin, or USDA has
nothing to say about them.

    python scripts/restore_food_origins.py           # report only (default)
    python scripts/restore_food_origins.py --apply   # back up the DB, then update

Docs: README-numa-documentation.md, "Origin and user edits are separate"
"""
import argparse
import datetime
import pathlib
import shutil
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import db as _db
import usda as _usda


def _candidates() -> list[tuple[int, str]]:
    with _db.get_db() as conn:
        return [(r["fdc_id"], r["name"]) for r in conn.execute(
            "SELECT fdc_id, name FROM foods WHERE data_type = 'User Drafted' AND fdc_id > 0 ORDER BY fdc_id"
        ).fetchall()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="write the changes (default: report only)")
    args = parser.parse_args(argv)

    found: list[tuple[int, str, str]] = []
    for fdc_id, name in _candidates():
        try:
            origin = (_usda.get_food_detail(fdc_id) or {}).get("dataType")
        except Exception as exc:  # network, rate limit, unknown id
            print(f"  {fdc_id:>9}  {name}: USDA lookup failed ({exc}) — left as is")
            continue
        if not origin or origin == "User Drafted":
            print(f"  {fdc_id:>9}  {name}: USDA gave no type — left as is")
            continue
        print(f"  {fdc_id:>9}  {name}: User Drafted -> {origin} · user-edited")
        found.append((fdc_id, name, origin))

    if not found:
        print("Nothing to restore.")
        return 0
    if not args.apply:
        print(f"\n{len(found)} food(s) would be restored. Run again with --apply to write them.")
        return 0

    db_path = _db.get_db_path()
    backup = db_path.with_name(f"{db_path.name}.before-origins-{datetime.datetime.now():%Y%m%d-%H%M%S}")
    shutil.copy2(db_path, backup)
    print(f"\nBacked up the database to {backup}")
    _db.init_db()  # the same migrations the app runs (adds foods.user_edited)
    with _db.get_db() as conn:
        for fdc_id, _name, origin in found:
            conn.execute("UPDATE foods SET data_type = ?, user_edited = 1 WHERE fdc_id = ?", (origin, fdc_id))
    print(f"Restored {len(found)} food(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
