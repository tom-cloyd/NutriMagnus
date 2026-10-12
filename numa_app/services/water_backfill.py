"""
water_backfill.py — fill in USDA's water value for every cached USDA food
that lacks one (foods cached before numa recorded water, 2026-10-11), from
Foods → 9's "Fill in water from USDA" button, on a background thread.

Asks USDA for water alone, 20 foods per request (usda.get_water_values), and
writes with db.fill_source_nutrient(): blanks only, and into the source copy
too, so the value isn't taken for the user's edit. Foods marked "Water not
needed" are skipped. A failed request stops the run but keeps what earlier
batches wrote; running again picks up where it stopped, since filled foods
are no longer candidates. Afterwards every recipe using a changed food is
recomputed once and its meals flagged stale (recipe_dcp), as after any
food-nutrient write.

Docs: README-numa-documentation.md, Architecture: "numa_app/services/water.py — water from drinks vs food"
"""
from __future__ import annotations

import json
import threading

import db as _db
import usda as _usda

from . import recipe_dcp as _recipe_dcp
from .water import WATER_KEY

_BATCH = 20

_state_lock = threading.Lock()
_state: dict = {"running": False, "checked": 0, "total": 0, "filled": 0,
                "no_value": [], "error": None, "finished": False}


def candidates(conn) -> list[int]:
    """USDA foods (positive fdc_id) with no water value and no "not needed"
    mark for the Water group, in fdc_id order."""
    ignores = _db.food_data_ignores(conn)
    out = []
    for r in conn.execute("SELECT fdc_id, nutrients_json FROM foods WHERE fdc_id > 0 ORDER BY fdc_id"):
        nutrients = json.loads(r["nutrients_json"]) if r["nutrients_json"] else {}
        if WATER_KEY not in nutrients and "water" not in ignores.get(r["fdc_id"], set()):
            out.append(r["fdc_id"])
    return out


def status() -> dict:
    with _state_lock:
        return {**_state, "no_value": list(_state["no_value"])}


def clear_status() -> None:
    """Forget a finished run's outcome (after the page has shown it)."""
    with _state_lock:
        if not _state["running"]:
            _state.update(checked=0, total=0, filled=0, no_value=[], error=None, finished=False)


def _apply(values: dict[int, float], ids: list[int]) -> tuple[int, list[str]]:
    """Write one batch's values; returns (foods filled, names USDA had no value for)."""
    filled, no_value, changed = 0, [], []
    with _db.get_db() as conn:
        for fdc_id in ids:
            if fdc_id in values:
                if _db.fill_source_nutrient(conn, fdc_id, WATER_KEY, values[fdc_id]):
                    filled += 1
                    changed.append(fdc_id)
            else:
                row = _db.get_cached_food(conn, fdc_id)
                no_value.append(row["name"] if row else str(fdc_id))
        _cascade(conn, changed)
    return filled, no_value


def _cascade(conn, fdc_ids: list[int]) -> None:
    """Recompute each recipe using any of fdc_ids once (not once per food),
    and flag every meal using them stale."""
    recipe_ids: set[int] = set()
    meal_ids: set[int] = set()
    for fdc_id in fdc_ids:
        _db.mark_meals_stale_for_food(conn, fdc_id)
        meal_ids.update(_db.meals_using_food(conn, fdc_id))
        recipe_ids.update(r["id"] for r in _db.recipes_containing_food(conn, fdc_id))
    if meal_ids:
        _db.log_meal_recalc(conn, sorted(meal_ids), "Water values added from USDA")
    for rid in sorted(recipe_ids):
        try:
            _recipe_dcp.recompute_recipe_dcp(rid, conn)
        except Exception as exc:
            _db.log_recompute_error(conn, "recipe", rid, f"Recompute after adding water values failed: {exc}")


def run() -> None:
    """The whole backfill, synchronously (start() runs it on a thread)."""
    with _db.get_db() as conn:
        ids = candidates(conn)
    with _state_lock:
        _state.update(total=len(ids))
    try:
        for i in range(0, len(ids), _BATCH):
            chunk = ids[i:i + _BATCH]
            values = _usda.get_water_values(chunk)      # network: no DB connection open
            filled, no_value = _apply(values, chunk)
            with _state_lock:
                _state["checked"] += len(chunk)
                _state["filled"] += filled
                _state["no_value"] += no_value
    except _usda.USDAError as exc:
        with _state_lock:
            _state["error"] = str(exc)
    except Exception as exc:    # never leave the page spinning
        with _state_lock:
            _state["error"] = f"Stopped unexpectedly: {exc}"


def start() -> bool:
    """Run the backfill on a background thread. False if one is running."""
    with _state_lock:
        if _state["running"]:
            return False
        _state.update(running=True, checked=0, total=0, filled=0, no_value=[], error=None, finished=False)

    def go() -> None:
        try:
            run()
        finally:
            with _state_lock:
                _state.update(running=False, finished=True)

    threading.Thread(target=go, name="water-backfill", daemon=True).start()
    return True
