"""
vitamin_k_repair.py — correct the vitamin K of every USDA food cached before
2026-10-14, from Foods → 9's "Correct vitamin K from USDA" button, on a
background thread.

Until then the full-detail USDA fetch read nutrient 1183 (menaquinone-4, a K2
form mostly found in animal foods) as vitamin K, not 1185 (phylloquinone, K1:
the form the RDA/AI is based on, and the one leafy greens carry). Raw spinach
came through with no vitamin K at all; chicken breast with 8.4 mcg of MK-4 in
place of its 0.3 mcg of phylloquinone. usda_api.NUTRIENT_MAP now reads 1185,
so only foods cached earlier (foods.vitamin_k_checked = 0) need this.

Asks USDA for phylloquinone alone, 20 foods per request
(usda.get_nutrient_values, nutrient "430"), and writes with
db.replace_source_nutrient(): the value replaces the old one in the food and
its source copy alike, or is removed when USDA has none; a value the user
edited is left alone. USDA's bulk request silently leaves out some foods
its single-food lookup still serves (several Branded records), so each food
the batch skips is asked for on its own (usda.get_food_detail). A food USDA
answers "not found" for (an id that isn't a USDA record) is marked checked
and listed, since asking again can't help; one that fails any other way
(network) stays unchecked, so running again retries it. Afterwards every recipe using a changed food is recomputed
once and its meals flagged stale, as after any food-nutrient write.

Docs: README-numa-documentation.md, Architecture: "numa_app/services/vitamin_k_repair.py — vitamin K correction"
"""
from __future__ import annotations

import threading

import db as _db
import usda as _usda

from .water_backfill import _cascade

KEY = "vitamin_k_mcg"
_NUMBER = "430"          # USDA nutrient number for phylloquinone
_WHAT = "Vitamin K corrected from USDA"
_BATCH = 20

_state_lock = threading.Lock()
_state: dict = {"running": False, "checked": 0, "total": 0, "changed": 0,
                "not_found": [], "not_in_usda": [], "error": None, "finished": False}


def candidates(conn) -> list[int]:
    """USDA foods (positive fdc_id, starter copies included) whose vitamin K
    hasn't been checked against USDA's phylloquinone value, in fdc_id order."""
    return [r["fdc_id"] for r in conn.execute(
        "SELECT fdc_id FROM foods WHERE fdc_id > 0 AND vitamin_k_checked = 0 ORDER BY fdc_id")]


def status() -> dict:
    with _state_lock:
        return {**_state, "not_found": list(_state["not_found"]),
                "not_in_usda": list(_state["not_in_usda"])}


def clear_status() -> None:
    """Forget a finished run's outcome (after the page has shown it)."""
    with _state_lock:
        if not _state["running"]:
            _state.update(checked=0, total=0, changed=0, not_found=[], not_in_usda=[],
                          error=None, finished=False)


def _apply(values: dict[int, float | None], ids: list[int],
           gone: frozenset[int] = frozenset()) -> tuple[int, list[str], list[str]]:
    """Write one batch; returns (foods whose vitamin K changed, names USDA
    didn't return, names USDA has no record of). `gone` foods are marked
    checked with their vitamin K left as it is."""
    changed, not_found, not_in_usda = [], [], []
    with _db.get_db() as conn:
        for fdc_id in ids:
            if fdc_id in gone:
                row = _db.get_cached_food(conn, fdc_id)
                not_in_usda.append(row["name"] if row else str(fdc_id))
                _db.mark_vitamin_k_checked(conn, fdc_id)
                continue
            if fdc_id not in values:
                row = _db.get_cached_food(conn, fdc_id)
                not_found.append(row["name"] if row else str(fdc_id))
                continue
            if _db.replace_source_nutrient(conn, fdc_id, KEY, values[fdc_id]):
                changed.append(fdc_id)
            _db.mark_vitamin_k_checked(conn, fdc_id)
        _cascade(conn, changed, _WHAT)
    return len(changed), not_found, not_in_usda


def _fetch_singly(ids: list[int], values: dict[int, float | None]) -> frozenset[int]:
    """Ask USDA one food at a time for each of `ids` the batch left out,
    adding what it finds to `values`. Returns the ids USDA has no record of
    (404). Any other failure leaves the food out, to be retried next run."""
    gone = set()
    for fdc_id in ids:
        try:
            values[fdc_id] = _usda.get_food_detail(fdc_id)["nutrients"].get(KEY)
        except _usda.USDAError as exc:
            if str(exc).startswith("USDA API 404"):
                gone.add(fdc_id)
    return frozenset(gone)


def run() -> None:
    """The whole repair, synchronously (start() runs it on a thread)."""
    with _db.get_db() as conn:
        ids = candidates(conn)
    with _state_lock:
        _state.update(total=len(ids), checked=0, changed=0, not_found=[], not_in_usda=[], error=None)
    try:
        for i in range(0, len(ids), _BATCH):
            chunk = ids[i:i + _BATCH]
            values = _usda.get_nutrient_values(chunk, _NUMBER)   # network: no DB connection open
            gone = _fetch_singly([f for f in chunk if f not in values], values)
            changed, not_found, not_in_usda = _apply(values, chunk, gone)
            with _state_lock:
                _state["checked"] += len(chunk)
                _state["changed"] += changed
                _state["not_found"] += not_found
                _state["not_in_usda"] += not_in_usda
    except _usda.USDAError as exc:
        with _state_lock:
            _state["error"] = str(exc)
    except Exception as exc:    # never leave the page spinning
        with _state_lock:
            _state["error"] = f"Stopped unexpectedly: {exc}"


def start() -> bool:
    """Run the repair on a background thread. False if one is running."""
    with _state_lock:
        if _state["running"]:
            return False
        _state.update(running=True, checked=0, total=0, changed=0, not_found=[], not_in_usda=[],
                      error=None, finished=False)

    def go() -> None:
        try:
            run()
        finally:
            with _state_lock:
                _state.update(running=False, finished=True)

    threading.Thread(target=go, name="vitamin-k-repair", daemon=True).start()
    return True
