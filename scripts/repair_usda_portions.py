#!/usr/bin/env python3
"""
repair_usda_portions.py — re-read cached USDA foods' portions from USDA and
correct the ones an older NuMa misread.

Until 2026-10-04, NuMa read a USDA portion's description from
portionDescription or, failing that, modifier — and ignored the amount and
measure unit beside them (usda_api.usda_portion_description() now reads all
three). Two kinds of food were affected:

  - SR Legacy: amount 0.5 + modifier "cup, chopped" was stored as
    "cup, chopped" = 78 g, so every cup of that food counted half its weight.
  - Foundation: amount 1 + measureUnit "cup", with no description or
    modifier, was dropped, so these foods arrived with no portions at all.

For each cached USDA food this fetches its foodPortions once and works out
both readings. A stored portion matching the OLD reading (same description,
same grams) gets the corrected description; its grams never change.
Portions the old reading dropped are added at the end of the list, so the
p1, p2 ... shortcuts of existing portions keep their meaning. Any other
portion — one the user added or edited — is left exactly as it is. The
food's source copy (source_json) is corrected the same way, so the repair
never makes a food count as user-edited. Nutrients are never touched.

Afterwards, recipe and meal amounts entered by volume for a repaired food may
no longer match their stored grams: the food's Portions page and Foods -> 9
("Amounts that no longer match") list them for review.

    python scripts/repair_usda_portions.py           # report only (default)
    python scripts/repair_usda_portions.py --apply   # back up the DB, then update

Docs: README-numa-documentation.md, Architecture: "usda_api.py — USDA HTTP client" (USDA portions)
"""
import argparse
import datetime
import json
import pathlib
import re
import shutil
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import db as _db
import usda as _usda
from numa_app.services.food_ids import classify_food_id


def _old_description(p: dict) -> str:
    """How NuMa read a foodPortions entry before 2026-10-04."""
    desc = p.get("portionDescription") or p.get("modifier", "") or ""
    return re.sub(r'^\d+\s+(?=\d)', '', desc.strip(), count=1)


def _key(desc: str, grams) -> tuple[str, float]:
    return desc.strip().lower(), round(float(grams or 0), 2)


def repaired(portions: list[dict] | None, raw: list[dict]) -> list[dict] | None:
    """`portions` with old-reading USDA entries renamed and dropped ones
    appended, or None if nothing changes."""
    portions = [dict(p) for p in (portions or []) if isinstance(p, dict)]
    renames: dict[tuple[str, float], str] = {}
    additions: list[dict] = []
    for p in raw:
        gw = p.get("gramWeight")
        new = _usda.usda_portion_description(p)
        if not gw or not new:
            continue
        old = _old_description(p)
        if old:
            if old != new:
                renames[_key(old, gw)] = new
        else:
            additions.append({"description": new, "gram_weight": float(gw)})
    changed = False
    for p in portions:
        new = renames.get(_key(p.get("description") or "", p.get("gram_weight")))
        if new:
            p["description"] = new
            changed = True
    have = {(p.get("description") or "").strip().lower() for p in portions}
    for a in additions:
        if a["description"].lower() not in have:
            portions.append(a)
            have.add(a["description"].lower())
            changed = True
    return portions if changed else None


def _candidates() -> list[dict]:
    with _db.get_db() as conn:
        rows = conn.execute(
            "SELECT fdc_id, name, portions_json, source_json FROM foods WHERE fdc_id > 0 ORDER BY name"
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="write the changes (default: report only)")
    args = parser.parse_args(argv)

    plans: list[tuple[int, list[dict], dict | None]] = []
    for food in _candidates():
        try:
            raw = _usda.get_food_portions_raw(food["fdc_id"])
        except Exception as exc:  # network, rate limit, an id USDA no longer serves
            print(f"  {food['fdc_id']:>9}  {food['name']}: USDA lookup failed ({exc}) — left as is")
            continue
        current = json.loads(food["portions_json"] or "null") or []
        new_current = repaired(current, raw)
        source = json.loads(food["source_json"]) if food["source_json"] else None
        new_source = None
        if isinstance(source, dict):
            new_source_portions = repaired(source.get("portions"), raw)
            if new_source_portions is not None:
                new_source = {**source, "portions": new_source_portions}
        if new_current is None and new_source is None:
            continue
        print(f"  {food['fdc_id']:>9}  {food['name']}")
        before = {_key(p.get("description") or "", p.get("gram_weight")) for p in current}
        for p in new_current or []:
            if _key(p["description"], p["gram_weight"]) not in before:
                print(f"               -> {p['description']} = {p['gram_weight']:g} g")
        plans.append((food["fdc_id"], new_current if new_current is not None else current, new_source))

    if not plans:
        print("Nothing to repair.")
        return 0
    if not args.apply:
        print(f"\n{len(plans)} food(s) would be repaired. Run again with --apply to write them.")
        return 0

    db_path = _db.get_db_path()
    backup = db_path.with_name(f"{db_path.name}.before-portions-{datetime.datetime.now():%Y%m%d-%H%M%S}")
    shutil.copy2(db_path, backup)
    print(f"\nBacked up the database to {backup}")
    _db.init_db()
    with _db.get_db() as conn:
        for fdc_id, portions, source in plans:
            if source is not None:
                conn.execute("UPDATE foods SET source_json = ? WHERE fdc_id = ?", (json.dumps(source), fdc_id))
            _db.update_food_fields(conn, fdc_id, portions=portions)   # re-derives user_edited
    print(f"Repaired {len(plans)} food(s). Foods -> 9 now lists any amounts that no longer match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
