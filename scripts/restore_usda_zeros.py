#!/usr/bin/env python3
"""
restore_usda_zeros.py — give cached USDA foods back the zeros USDA measured.

Until 2026-10-09, NuMa read a USDA nutrient with `value or amount`, so a
nutrient USDA had measured at 0 was dropped as if it had never been measured
(usda_api._parse_food() now keeps zeros). Nutrient tables now tell "0" (data:
the food has none) apart from "no data" (never recorded), so those foods show
"no data" for nutrients USDA actually knows are zero.

For each cached USDA food this fetches USDA's current copy once and adds
every nutrient USDA reports as exactly 0 that the food doesn't have at all.
Nothing else changes: a value the food already has — USDA's, an estimate, or
one the user edited — is never touched, and non-zero values USDA has that the
food lacks are left for Refresh from USDA, where the user reviews them. The
food's source copy (source_json) gets the same zeros, so the repair never
makes a food count as user-edited. Adding a zero changes no total.

    python scripts/restore_usda_zeros.py           # report only (default)
    python scripts/restore_usda_zeros.py --apply   # back up the DB, then update

Docs: README-numa-documentation.md, Architecture: "usda_api.py — USDA HTTP client"
"""
import argparse
import datetime
import json
import pathlib
import shutil
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import db as _db
import usda as _usda
from numa_app.services.food_ids import classify_food_id


def zeros_to_add(current: dict, incoming: dict) -> dict:
    """The nutrients USDA reports as exactly 0 that `current` has no value
    for at all — {key: 0.0}. A key `current` has, whatever its value, is
    never included."""
    return {k: 0.0 for k, v in (incoming or {}).items()
            if v == 0 and k not in (current or {})}


def _candidates() -> list[dict]:
    with _db.get_db() as conn:
        rows = conn.execute(
            "SELECT fdc_id, name, nutrients_json, source_json FROM foods WHERE fdc_id > 0 ORDER BY name"
        ).fetchall()
    out = []
    for r in rows:
        try:
            if classify_food_id(r["fdc_id"])[1] != "USDA":
                continue
        except Exception:
            continue
        out.append(dict(r))
    return out


def main(argv: list[str] | None = None, fetch=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="write the changes (default: report only)")
    args = parser.parse_args(argv)
    fetch = fetch or _usda.get_food_detail

    plans: list[tuple[int, dict, dict | None]] = []
    failed = 0
    foods = _candidates()
    for i, food in enumerate(foods, 1):
        try:
            incoming = (fetch(food["fdc_id"]) or {}).get("nutrients") or {}
        except Exception as exc:  # network, rate limit, an id USDA no longer serves
            failed += 1
            print(f"  {food['fdc_id']:>9}  {food['name']}: USDA lookup failed ({exc}) — left as is")
            continue
        current = json.loads(food["nutrients_json"] or "{}") or {}
        zeros = zeros_to_add(current, incoming)
        if not zeros:
            continue
        source = json.loads(food["source_json"]) if food["source_json"] else None
        new_source = None
        if isinstance(source, dict) and isinstance(source.get("nutrients"), dict):
            new_source = {**source, "nutrients": {**source["nutrients"],
                                                  **zeros_to_add(source["nutrients"], zeros)}}
        print(f"  {food['fdc_id']:>9}  {food['name']}: {len(zeros)} zero(s) — "
              + ", ".join(sorted(zeros)))
        plans.append((food["fdc_id"], {**current, **zeros}, new_source))

    print(f"\nChecked {len(foods)} USDA food(s); {failed} lookup(s) failed.")
    if not plans:
        print("Nothing to restore.")
        return 0
    if not args.apply:
        print(f"{len(plans)} food(s) would get their zeros back. Run again with --apply to write them.")
        return 0

    db_path = _db.get_db_path()
    backup = db_path.with_name(f"{db_path.name}.before-zeros-{datetime.datetime.now():%Y%m%d-%H%M%S}")
    shutil.copy2(db_path, backup)
    print(f"Backed up the database to {backup}")
    _db.init_db()
    with _db.get_db() as conn:
        for fdc_id, nutrients, source in plans:
            conn.execute("UPDATE foods SET nutrients_json = ? WHERE fdc_id = ?", (json.dumps(nutrients), fdc_id))
            if source is not None:
                conn.execute("UPDATE foods SET source_json = ? WHERE fdc_id = ?", (json.dumps(source), fdc_id))
            _db.refresh_user_edited(conn, fdc_id)
    print(f"Restored zeros on {len(plans)} food(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
