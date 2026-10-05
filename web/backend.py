"""
backend.py — FastAPI web interface for numa nutritional analysis.
Docs: README-numa-documentation.md, Architecture: "web/ — Local web app"
"""
import contextvars
import datetime
import io
import json
import math
import re
import shutil
import sys
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode

if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(Path(__file__).parent.parent))

import markdown as _md
from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool

import afcd_lookup as _afcd
import ciqual_lookup as _ciqual
import cnf_api as _cnf
import cofid_lookup as _cofid
import db as _db
import diaas as _diaas
import gi_lookup as _gi_lookup
import openfoodfacts as _off
import platform_utils as _platform_utils
import profile as _profile
import usda as _usda
from numa_app.services import claude_fetch as _claude_fetch
from numa_app.services import data_completeness as _data_completeness
from numa_app.services import energy_check as _energy_check
from numa_app.services import data_quality as _data_quality
from numa_app.services.food_ids import classify_food_id as _classify_food_id
from numa_app.services.food_ids import code_sort_key as _code_sort_key
from numa_app.services.food_ids import parse_code as _parse_code
from numa_app.services import complements as _complements
from numa_app.services import csv_export as _csv_export
from numa_app.services import csv_import as _csv_import
from numa_app.services import recipe_csv as _recipe_csv
from numa_app.services import recipe_translate as _recipe_translate
from numa_app.services import day_profile as _day_profile
from numa_app.services import gi_table_build as _gi_table_build
from numa_app.services import aa_estimate as _aa_estimate
from numa_app.services import incoming_review as _incoming_review
from numa_app.services.glycemic_load import (average_day_gl, compute_glycemic_load, day_gl_totals,
                                             gl_band, gl_band_caveat)
from numa_app.services.meal_bcp import recipe_dcp_fallback
from numa_app.services.nutrient_trend import average_from_daily_totals
from numa_app.services.portions import _ing_amount_display, _parse_portion_input, portion_amount_note
from numa_app.services.portions import generic_density_kind as _generic_density_kind
from numa_app.services.portions import match_portion_label as _match_portion_label
from numa_app.services.portions import _UNIT_TO_GRAMS as _PORTION_UNIT_TO_G
from version import VERSION, NEW_VERSION_NOTE, RELEASE_VERSION
from numa_app.services import update_check as _update_check
from numa_app.services import manual_update as _manual_update
from numa_app.services import self_update as _self_update
from numa_app.services.portions import _VOLUME_TO_ML as _PORTION_VOL_TO_ML
from numa_app.services.rda_status import rda_status, limit_warning
from numa_app.services.diet_aware import b12_deficiency_note, iron_zinc_bioavailability_note
from numa_app.services.recipe_nutrients import (
    atomic_recipe_ingredients, best_aa_nutrients, expand_recipe_ingredients,
    recipe_aa_indicator, recipe_serving_grams, recipe_total_nutrients,
)
from numa_app.services.top_contributors import rank_contributors, rank_contributors_by_dcp
from numa_app.services import recipe_dcp as _recipe_dcp
from numa_app.services import search_ranking as _search_ranking
from numa_app.services import search_suggest as _search_suggest
from numa_app.services import print_sections as _print_sections

# In a PyInstaller onefile build, backend.py is bundled as a flattened
# top-level module — there's no separate web/ subdirectory nested under a
# project root, both collapse to sys._MEIPASS. Source (non-frozen) layout
# still has web/backend.py one level below the real project root.
_WEB_DIR     = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
_PROJECT_ROOT = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else _WEB_DIR.parent
_MANUAL     = _PROJECT_ROOT / "user-manual.html"
_MANUAL_MD  = _PROJECT_ROOT / "user-manual.md"
_DISCLAIMER_MD = _PROJECT_ROOT / "DISCLAIMER.md"
_PREFS_FILE = _platform_utils.get_data_dir() / "prefs.json"

_HOME_CACHE = _WEB_DIR / "home_body.cache"

# The home page's about text used to live in its own home.md, hand-copied
# from the manual's Preface and prone to drifting out of sync with it. It's
# now excerpted live from user-manual.md instead — just the first 3 Preface
# paragraphs (lines 7-11), not the whole thing.
_HOME_CLOSING_PARAGRAPH = (
    "(This introduction is continued at the beginning of the User Manual, "
    "accessible from the main menu above.)"
)


def _extract_manual_preface() -> str:
    if not _MANUAL_MD.exists():
        return ""
    lines = _MANUAL_MD.read_text(encoding="utf-8").splitlines()
    # Lines 7-11 (1-indexed) — the first 3 Preface paragraphs.
    return "\n".join(lines[6:11]).strip()

# Strip these prep-state words from USDA API queries
_SEARCH_PREP_WORDS = {
    "peeled", "unpeeled", "sliced", "diced", "chopped", "minced", "grated",
    "shredded", "mashed", "pureed", "juiced", "squeezed", "seeded", "pitted",
    "skinless", "boneless", "trimmed", "halved", "quartered", "cubed",
    "cooked", "boiled", "steamed", "baked", "fried", "grilled", "sauteed",
    "blanched", "poached", "braised", "stewed", "microwaved",
    "frozen", "canned", "pickled", "smoked", "cured", "fermented",
    "fresh", "raw", "dried", "dehydrated", "reconstituted",
    "plain", "unseasoned", "seasoned", "marinated",
}
_SEARCH_META_WORDS = {"usda", "off", "openfoodfacts", "cnf"}

def _render_home_md() -> str:
    """Full-length home-page about text: the manual's Preface plus the
    closing paragraph, cached to web/home_body.cache (invalidated when
    user-manual.md is newer)."""
    if _HOME_CACHE.exists() and _MANUAL_MD.exists() and _HOME_CACHE.stat().st_mtime >= _MANUAL_MD.stat().st_mtime:
        return _HOME_CACHE.read_text(encoding="utf-8")
    preface = _extract_manual_preface()
    md_text = (preface + "\n\n" + _HOME_CLOSING_PARAGRAPH) if preface else _HOME_CLOSING_PARAGRAPH
    html = _md.markdown(md_text, extensions=["footnotes"])
    _HOME_CACHE.write_text(html, encoding="utf-8")
    return html


def _render_home_md_short() -> str:
    """First paragraph of the manual's Preface only, plus a link back to
    the manual — used in place of the full about text when a nutrient plot
    is also showing on the home page, so the two fit together."""
    preface = _extract_manual_preface()
    first_para = preface.split("\n\n", 1)[0] if preface else ""
    html = _md.markdown(first_para, extensions=["footnotes"]) if first_para else ""
    continued = ' (...continued at beginning of <a href="/manual">User Manual</a>.)'
    if html.endswith("</p>"):
        html = html[: -len("</p>")] + continued + "</p>"
    else:
        html += continued
    return html

# ---------------------------------------------------------------------------
# Portion-string parser (unit tables are numa_app.services.portions' — imported
# above as _PORTION_UNIT_TO_G / _PORTION_VOL_TO_ML — kept as the single source
# of truth for gram/ml conversion factors; the parsing function itself stays
# here since it needs web-specific fallback behavior for bare numbers and
# unknown-density volumes, tailored to the stateless form flow)
# ---------------------------------------------------------------------------


def _parse_portion_str(
    raw: str,
    portions: list[dict],
    food_name: str = "",
) -> tuple[float, str] | tuple[None, str]:
    """_parse_portion_str_raw(), plus reading back the label a "pN" amount is
    stored as ("2 × 1 large egg", "1 large egg"), so an Edit box showing it
    can be saved unchanged — see portions.match_portion_label()."""
    hit = _match_portion_label(raw, portions, allow_bare=False)
    if hit:
        return hit
    grams, msg = _parse_portion_str_raw(raw, portions, food_name)
    if grams is None:
        hit = _match_portion_label(raw, portions)
        if hit:
            return hit
    return grams, msg


def _parse_portion_str_raw(
    raw: str,
    portions: list[dict],
    food_name: str = "",
) -> tuple[float, str] | tuple[None, str]:
    """
    Parse a free-form portion string into (grams, display_label).
    Returns (None, error_message) on failure.

    Accepts: plain number (→ g), weight units (oz, lb, kg, g),
    volume units (cup, T, tsp, ml …), fractions (1/4, 1 1/2),
    and USDA preset codes (p1, p2 …).
    """
    raw = raw.strip()
    if not raw:
        return None, "Enter an amount."

    # Normalise "6p1" → "6 p1" so number and portion code can be parsed separately
    raw = re.sub(r'(?i)(\d+)(p\d+)', r'\1 \2', raw)

    # pN shortcut — USDA named portion (bare: "p1")
    m = re.fullmatch(r"(?i)p(\d+)", raw)
    if m:
        idx = int(m.group(1)) - 1
        if 0 <= idx < len(portions):
            p = portions[idx]
            return float(p["gram_weight"]), p["description"]
        return None, f"No preset p{idx + 1} for this food."

    # Tokenise: split on whitespace, keep "/" attached to adjacent digits,
    # then split any attached number+unit pairs (e.g. "31g" → ["31", "g"])
    tokens = re.findall(r"\d+/\d+|\S+", raw)
    expanded: list[str] = []
    for tok in tokens:
        if not tok.lower().startswith("p"):
            _m = re.match(r'^(\d[\d./]*)\s*([A-Za-z].*)$', tok)
            if _m:
                expanded.extend([_m.group(1), _m.group(2)])
                continue
        expanded.append(tok)
    tokens = expanded

    def _parse_num(toks: list[str]) -> tuple[float, int] | None:
        if not toks:
            return None
        t = toks[0]
        if re.fullmatch(r"\d+/\d+", t):
            num, den = t.split("/")
            return float(num) / float(den), 1
        try:
            whole = float(t)
        except ValueError:
            return None
        # Mixed number: "1 1/2"
        if len(toks) > 1 and re.fullmatch(r"\d+/\d+", toks[1]):
            num, den = toks[1].split("/")
            return whole + float(num) / float(den), 2
        return whole, 1

    parsed = _parse_num(tokens)
    if parsed is None:
        return None, f'Could not read a number from "{raw}".'
    number, consumed = parsed
    rest = tokens[consumed:]

    # No unit → grams
    if not rest:
        return number, f"{number:g} g"

    unit = rest[0]

    # NUMBER pN — multiple of a USDA named portion (e.g. "6 p1", "1.5 p2")
    pN = re.fullmatch(r"(?i)p(\d+)", unit)
    if pN:
        idx = int(pN.group(1)) - 1
        if 0 <= idx < len(portions):
            p = portions[idx]
            grams = round(number * float(p["gram_weight"]), 2)
            return grams, f"{number:g} × {p['description']}"
        return None, f"No preset p{idx + 1} for this food."

    # Weight unit
    factor = _PORTION_UNIT_TO_G.get(unit.lower())
    if factor is not None:
        grams = round(number * factor, 2)
        return grams, f"{number:g} {unit}"

    # Volume unit (case-sensitive for T vs t, fall back to lower)
    ml_per = _PORTION_VOL_TO_ML.get(unit) or _PORTION_VOL_TO_ML.get(unit.lower())
    if ml_per is not None:
        density = _usda.get_density_g_per_ml(food_name, portions)
        if density is None:
            return None, (
                f'Volume unit "{unit}" recognised, but no density data is available '
                f"for this food. Enter weight in g or oz instead."
            )
        grams = round(number * ml_per * density, 2)
        # Store exactly what was typed, not "2 T (≈ 27.23 g)" — the estimated
        # gram figure is a density guess, not a fact, and baking it into the
        # stored label meant re-submitting an unedited amount (e.g. re-saving
        # after just fixing a typo in the notes field) could fail to parse.
        return grams, f"{number:g} {unit}"

    return None, f'Unit "{unit}" not recognised. Try: g, oz, lb, cup, T, tsp, ml, p1, 6 p1.'


# ---------------------------------------------------------------------------

_DIET_LABELS = {
    "all":        "All animal foods (meat, fish, dairy, eggs)",
    "vegetarian": "Vegetarian (dairy + eggs only)",
    "plant_only": "Plant-based only",
}
_VALID_DIET_PREFS = {"all", "vegetarian", "plant_only"}

# Keys must match launcher.py's _BROWSER_PROCESSES (the process names it looks
# for with pgrep / launches directly) — "" means auto-detect the running browser.
# Chromium is one choice even though distros install it under either
# "chromium" or "chromium-browser": the launcher tries both (see its
# _BROWSER_ALTERNATES), so listing both here only showed Chromium twice.
_BROWSER_LABELS = {
    "":                 "Ask each time (default)",
    "firefox":          "Firefox",
    "google-chrome":    "Google Chrome",
    "chromium":         "Chromium",
    "brave-browser":    "Brave",
    "vivaldi":          "Vivaldi",
    "opera":            "Opera",
    "microsoft-edge":   "Microsoft Edge",
    "epiphany":         "GNOME Web (Epiphany)",
}
# "chromium-browser" stays valid so a pref saved before the merge still loads.
_VALID_BROWSER_PREFS = set(_BROWSER_LABELS) | {"chromium-browser"}


def _load_prefs_file() -> dict:
    if _PREFS_FILE.exists():
        try:
            data = json.loads(_PREFS_FILE.read_text())
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_prefs_file(updates: dict) -> None:
    data = _load_prefs_file()
    data.update(updates)
    _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _PREFS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def _is_ajax_row_action(request: Request) -> bool:
    """True when a row-action form (archive/restore/remove/delete on a list page)
    was submitted via the base.html fetch() handler rather than a normal browser
    POST — see the `js-row-remove`/`js-row-archive` script there. Callers branch
    to a small JSON reply instead of a redirect, so the list page doesn't reload
    and lose its current search/sort/filter state for a single row's change."""
    return request.headers.get("x-numa-ajax") == "1"


def _resolve_sort(sort: str | None, pref_key: str, default: str, valid: set[str]) -> str:
    """Resolve the sort choice for a list view: an explicit `sort` query param wins
    and is remembered as the new default; otherwise fall back to the saved pref."""
    prefs = _load_prefs_file()
    if sort is None:
        saved = prefs.get(pref_key, default)
        return saved if saved in valid else default
    if sort not in valid:
        sort = default
    if prefs.get(pref_key) != sort:
        _save_prefs_file({pref_key: sort})
    return sort


def _sort_meal_items_display(items: list[dict], item_sort: str | None = None) -> list[dict]:
    """Order a meal's items per the saved display preference: alphabetical by
    food/recipe name (default), or entry order (first added to last)."""
    resolved = item_sort or _resolve_sort(None, "sort_meal_items", "alpha", {"alpha", "entry"})
    if resolved == "entry":
        return items
    return sorted(items, key=lambda it: (it["food_name"] or "").lower())


def _resolve_bool_pref(value: bool | None, pref_key: str, default: bool = False) -> bool:
    """Resolve a sticky boolean list-view toggle (e.g. 'show archived'): an explicit
    query param wins and is remembered as the new default; otherwise use the saved pref."""
    prefs = _load_prefs_file()
    if value is None:
        return bool(prefs.get(pref_key, default))
    if bool(prefs.get(pref_key, default)) != value:
        _save_prefs_file({pref_key: value})
    return value


_SEARCH_CATEGORY_RANK = {"pantry": 0, "cache": 1, "recipe": 2, "usda": 3, "off": 3, "cnf": 3,
                          "cofid": 3, "afcd": 3, "ciqual": 3}
_SEARCH_SORT_MODES = {"grouped", "relevance"}

def _fetch_usda_candidates(api_query: str, limit: int, existing: list[dict]) -> list[dict]:
    general = _usda.search_foods(api_query, page_size=limit)
    # USDA's own relevance ranking can bury plain/raw preparations (the ones
    # with real amino-acid data) ~20 deep for a common single-word query —
    # see _search_logic for the "potato" case that exposed this. The result
    # cap is user-configurable (Settings → Advanced); 0 means no cap.
    foundation = _usda.search_foods(api_query, data_types=["Foundation", "SR Legacy"],
                                     page_size=_usda.get_search_boost_page_size())
    found_ids = {f["fdcId"] for f in foundation}
    return foundation + [f for f in general if f["fdcId"] not in found_ids]


def _fetch_off_candidates(api_query: str, limit: int, existing: list[dict]) -> list[dict]:
    found = []
    for food in _off.search_foods(api_query, page_size=limit):
        name_lower = food.get("description", "").lower()
        if not any(name_lower == f.get("description", "").lower() for f in existing + found):
            found.append(food)
    return found


def _fetch_cnf_candidates(api_query: str, limit: int, existing: list[dict]) -> list[dict]:
    return _cnf.search_foods(api_query, page_size=limit)


# Every live (network-backed) food-search source: (key, human name, fetch
# function). Single source of truth for that name, used both to build the
# "Searching X and Y…" status message (see _external_source_labels()) and by
# _external_food_search_results()'s fetch loop below — adding a future source
# (UK CoFID, etc. — see user-manual.md Part 9) is one entry here, not a
# change to the message or the fetch loop.
_LIVE_SOURCES = [
    ("usda", "USDA FoodData Central",     _fetch_usda_candidates),
    ("off",  "Open Food Facts",           _fetch_off_candidates),
    ("cnf",  "Canadian Nutrient File",    _fetch_cnf_candidates),
]

# Static (bundled-dataset, no network) external sources — searched instantly
# via _search_local_results()/_meal_add_food_local_results() rather than the
# async fetch loop _LIVE_SOURCES drives. (key, human name) — no fetch_fn here
# since each caller already knows how to merge its own static-source results
# inline; this list exists for the label, matching _LIVE_SOURCES' role.
_STATIC_SOURCES = [
    ("cofid",  "CoFID (UK Food Composition)"),
    ("afcd",   "AFCD (Australian Food Composition)"),
    ("ciqual", "CIQUAL (French Food Composition)"),
]
_STATIC_SOURCE_MODULES = {"cofid": _cofid, "afcd": _afcd, "ciqual": _ciqual}


def _static_source_candidates(query: str, keys: list[str] | None = None) -> list[dict]:
    """Results from every static (bundled-dataset, no network) source — or
    just `keys` if given — in the shared search-result shape used by
    _search_local_results()/_meal_add_food_local_results(). None of these
    sources' search stubs claim amino-acid data (even AFCD, which has real
    AA data for most but not all foods — "✗" here just means "unconfirmed
    until fetched," the same posture used for OFF/CNF search stubs)."""
    active = keys if keys is not None else [key for key, _label in _STATIC_SOURCES]
    results = []
    for key in active:
        module = _STATIC_SOURCE_MODULES.get(key)
        if module is None:
            continue
        for food in module.search_foods(query):
            results.append({
                "fdc_id":    food["fdcId"],
                "name":      food["description"],
                "data_type": food["dataType"],
                "brand":     "",
                "source":    key,
                "off_code":  "",
                "portions":  [],
                "aa":        "✗",
                "gi":        None,
                "diaas":     None,
                "has_notes": False,
            })
    return results

# Data-source filter for search results, offered next to the query box on
# every food-search screen in the app. A user can check any combination of
# sources; checking none is treated the same as checking all (there's no
# useful "show nothing" state). Order here is display/checkbox order — USDA
# and Open Food Facts (the two primary, most-used external sources) lead the
# external group, ahead of the smaller regional static datasets (CoFID/AFCD/
# CIQUAL) and Canadian Nutrient File.
_SEARCH_SOURCE_FILTERS = (["pantry", "cache", "recipe"]
                           + [key for key, _, _fn in _LIVE_SOURCES]
                           + [key for key, _ in _STATIC_SOURCES])
_SEARCH_SOURCE_LABELS = {
    "pantry": "PANTRY — Pantry",
    "cache":  "CACHE — Food Cache",
    "recipe": "RECIPE — Recipes",
    **{key: f"{key.upper()} — {name}" for key, name in _STATIC_SOURCES},
    **{key: f"{key.upper()} — {name}" for key, name, _fn in _LIVE_SOURCES},
}


def _external_source_labels(sources: list[str]) -> list[str]:
    """Human names of whichever live sources are in the current Source filter
    selection, in registry order — used to build an accurate "Searching X and
    Y…" status message that names exactly what's being queried, instead of a
    hardcoded pair. Empty when no live source is selected (nothing to fetch)."""
    return [name for key, name, _fn in _LIVE_SOURCES if key in sources]


def _fetch_uncached_food_detail(fdc_id: int, off_code: str = "") -> dict:
    """Fetch full detail for a search result not yet in the local cache,
    dispatching by which synthetic-ID range fdc_id falls in (or a real
    positive USDA id) — the shared "user clicked/added an external search
    result we haven't fetched before" path used by pantry add, meal add-food,
    and the custom-profile copy pickers. Raises on failure (network error, or
    a source that couldn't resolve the id) so existing callers' try/except
    Exception blocks handle it uniformly, matching usda.get_food_detail()'s
    own raise-on-failure behavior."""
    if fdc_id > 0:
        return _usda.get_food_detail(fdc_id)
    if _off.is_off_id(fdc_id):
        detail = _off.lookup_by_barcode(off_code) if off_code else None
        if not detail:
            raise _off.OFFError("lookup failed")
        return detail
    if _cnf.is_cnf_id(fdc_id):
        detail = _cnf.get_food_detail_by_id(fdc_id)
        if not detail:
            raise _cnf.CNFError("lookup failed")
        return detail
    if _cofid.is_cofid_id(fdc_id):
        detail = _cofid.get_food_detail_by_id(fdc_id)
        if not detail:
            raise LookupError("CoFID lookup failed")
        return detail
    if _afcd.is_afcd_id(fdc_id):
        detail = _afcd.get_food_detail_by_id(fdc_id)
        if not detail:
            raise LookupError("AFCD lookup failed")
        return detail
    if _ciqual.is_ciqual_id(fdc_id):
        detail = _ciqual.get_food_detail_by_id(fdc_id)
        if not detail:
            raise LookupError("CIQUAL lookup failed")
        return detail
    raise ValueError(f"fdc_id {fdc_id} is not in any known source's id range")


def _get_or_cache_source_food(fdc_id: int, off_code: str = "") -> "sqlite3.Row":
    """Return the cached Row for fdc_id, fetching-and-caching it first via
    _fetch_uncached_food_detail() if it isn't already cached — the shared
    "resolve a copy-aa/copy-nutrients source" step used by both custom-profile
    copy pickers. Raises whatever _fetch_uncached_food_detail() raises on
    failure; callers decide the user-facing redirect."""
    with _db.get_db() as conn:
        source = _db.get_cached_food(conn, fdc_id)
    if source:
        return source
    detail = _fetch_uncached_food_detail(fdc_id, off_code)
    with _db.get_db() as conn:
        _db.cache_food(
            conn, fdc_id=detail["fdcId"], name=detail["name"],
            data_type=detail.get("dataType", ""),
            brand=detail.get("brand"),
            serving_size=detail.get("servingSize"),
            serving_unit=detail.get("servingUnit"),
            nutrients=detail.get("nutrients", {}),
            portions=detail.get("portions", []),
        )
        _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
        return _db.get_cached_food(conn, fdc_id)


def _resolve_source_filter(raw: list[str] | None, pref_key: str,
                            valid_sources: list[str] = _SEARCH_SOURCE_FILTERS) -> list[str]:
    """Resolve a multi-select source filter: explicit `source` query values
    (possibly several, one per checked checkbox) win and are remembered as
    the new default; otherwise fall back to the saved pref. An empty or
    entirely-invalid selection (nothing checked) reverts to "all sources" —
    there's no point letting a user filter results down to nothing."""
    prefs = _load_prefs_file()
    if raw is None:
        raw = [s for s in prefs.get(pref_key, "").split(",") if s]
    valid = [s for s in raw if s in valid_sources]
    if not valid:
        valid = list(valid_sources)
    joined = ",".join(valid)
    if prefs.get(pref_key, "") != joined:
        _save_prefs_file({pref_key: joined})
    return valid


def _omitted_source_labels(sources: list[str], valid_sources: list[str] = _SEARCH_SOURCE_FILTERS) -> list[str]:
    """Short uppercase codes (PANTRY, USDA, ...) for every source currently
    unchecked in the Source filter, in filter order. The Source filter is
    "sticky" — a box unchecked once stays unchecked on every search box in
    the app until re-checked — which made a food silently and permanently
    missing from results easy to mistake for a search or ranking bug rather
    than a filter setting. Empty when every source is checked."""
    if set(sources) >= set(valid_sources):
        return []
    return [s.upper() for s in valid_sources if s not in sources]


def _filter_search_results_by_source(results: list[dict], sources: list[str] | None) -> list[dict]:
    """Restrict search results to the given data sources ('pantry', 'cache',
    'recipe', 'usda', 'off'), or return everything when sources is empty/unset
    (which _resolve_source_filter() never actually produces, but callers that
    bypass it — e.g. a hand-built filter — get the safe "no filter" behavior).
    Lets a user isolate one or more sources' results — e.g. to check whether
    a ranking oddity comes from a specific source's data rather than the
    ranking logic itself."""
    if not sources or set(sources) >= set(_SEARCH_SOURCE_FILTERS):
        return results
    allowed = set(sources)
    return [r for r in results if r.get("source") in allowed]


_LOCAL_SEARCH_SOURCES = {"pantry", "cache", "recipe"}


def _cap_results_preserving_local(results: list[dict], limit: int) -> list[dict]:
    """Cap a sorted, already-source-filtered result list to `limit`, and group
    it into two blocks — every local (pantry/cache/recipe) match first, then
    external (USDA/OFF/CNF) matches — each block keeping its existing
    relative (relevance) order. Templates render these as two visually
    distinct sections (see is_local_source()) so a food you already have
    never has to be found by scrolling past a wall of external results.

    `limit` exists to bound how many *external* results get fetched and
    shown — see _SEARCH_RESULT_LIMIT_DEFAULT's docstring — not to hide a food
    the user already has, so a local match can push the *count* of external
    results shown below `limit`, but a local match is never dropped or
    reordered behind a weaker external one to make room for it. Regression
    case: searching "vitamins daily" for a cached "Complete multivitamin"
    (a weak text match — no literal "daily" in the name) used to bury it,
    or drop it entirely, under dozens of branded USDA/OFF products literally
    named "Daily Vitamins".
    """
    local = [r for r in results if r.get("source") in _LOCAL_SEARCH_SOURCES]
    if len(results) <= limit:
        return local + [r for r in results if r.get("source") not in _LOCAL_SEARCH_SOURCES]
    if not local:
        return results[:limit]
    external_slots = max(0, limit - len(local))
    external = [r for r in results if r.get("source") not in _LOCAL_SEARCH_SOURCES][:external_slots]
    return local + external


def _is_local_source(source: str) -> bool:
    return source in _LOCAL_SEARCH_SOURCES

# How many results a food search shows by default, and the ceiling a user can
# raise it to via the "Show up to ___ search results" box next to the Source
# filter. Also used as the page_size requested from USDA/OFF, so raising it
# actually fetches more candidates rather than just changing a display cap.
_SEARCH_RESULT_LIMIT_DEFAULT = 25
_SEARCH_RESULT_LIMIT_MAX = 500


def _resolve_result_limit(raw: int | None, pref_key: str = "search_result_limit") -> int:
    """Resolve the "Show up to ___ results" cap: an explicit `limit` query/form
    value wins and is remembered as the new default; otherwise fall back to
    the saved pref. Clamped to [1, _SEARCH_RESULT_LIMIT_MAX] so a stray value
    (blank field, huge number) can't break the page or hammer the APIs."""
    prefs = _load_prefs_file()
    if raw is None:
        try:
            raw = int(prefs.get(pref_key, _SEARCH_RESULT_LIMIT_DEFAULT))
        except (TypeError, ValueError):
            raw = _SEARCH_RESULT_LIMIT_DEFAULT
    val = max(1, min(raw, _SEARCH_RESULT_LIMIT_MAX))
    if prefs.get(pref_key) != val:
        _save_prefs_file({pref_key: val})
    return val

# Matches plotting.MAX_SERIES — the nutrient-plot picker can't offer more
# lines than the fixed categorical color palette has colors for.
MAX_PLOT_NUTRIENTS = 8

# Day DCP isn't a NUTRIENT_MAP entry (it's a separately computed/stored
# column, not part of a meal's nutrient snapshot), so the Nutrient Plot
# picker treats it as a pseudo-nutrient with its own key.
_DCP_PLOT_KEY = "dcp"
_DCP_PLOT_LABEL = "Day DCP (g)"

# Daily glycemic load, same pseudo-nutrient treatment as Day DCP: it isn't a
# NUTRIENT_MAP entry either (it's derived per day from each food's annotated GI
# and the carbohydrate actually eaten), and it's unitless, so it never
# contributes a shared unit to the y-axis label. A day whose GI coverage is
# incomplete plots as a gap, not as a low value.
_GL_PLOT_KEY = "gl"
_GL_PLOT_LABEL = "Daily glycemic load"

# The "highlighted" nutrient (user-selectable, defaults to Day DCP if
# chosen) always draws in this fixed red and solid, so the one figure
# everything else is usually compared against stands out — regardless of
# which nutrient that is this time. In grayscale mode it's still the one
# solid line; everything else switches to a dash pattern instead of color.
_HIGHLIGHT_COLOR = "#e34948"


def _plot_label_for(key: str) -> str:
    if key == _DCP_PLOT_KEY:
        return _DCP_PLOT_LABEL
    if key == _GL_PLOT_KEY:
        return _GL_PLOT_LABEL
    from numa_app.services.meal_list_columns import label_for as _nutrient_label_for
    return _nutrient_label_for(key)


def _sort_search_results(results: list[dict], query: str, mode: str) -> list[dict]:
    """Order search results by match quality: how many query words a name
    contains (all > all-but-one > ...), with ties broken first by which
    specific words matched (earlier query words outrank later ones — see
    numa_app.services.search_ranking) and only then by source category
    (pantry/cache/recipe/external). "Pantry, Cache, then Other" mode instead
    breaks match-quality ties by source category before the rest of the
    relevance tiebreakers — own data sorts ahead of external only among
    results that matched the query equally well, never displacing a
    stronger external match."""
    if mode == "grouped":
        def _grouped_key(r):
            rel = _search_ranking.relevance_key(r["name"], query, data_type=r.get("data_type", ""))
            # Match quality (how many query words matched, then which ones)
            # always outranks source category — "own data first" only breaks
            # ties among results matching the query equally well, so a
            # weaker match from your own pantry/cache can never bury a
            # stronger match from an external source.
            return (rel[0], rel[1], _SEARCH_CATEGORY_RANK.get(r["source"], 9), rel)

        return sorted(results, key=_grouped_key)
    return sorted(
        results,
        key=lambda r: _search_ranking.relevance_key(r["name"], query, r["source"], r.get("data_type", "")),
    )


def _external_food_search_results(api_query: str, exclude_ids: set[int], q: str, sort: str,
                                   sources: list[str] | None = None,
                                   limit: int = _SEARCH_RESULT_LIMIT_DEFAULT) -> list[dict]:
    """Live-source search: one blocking network call per selected source in
    _LIVE_SOURCES (`sources` defaults to "all of them", for callers that
    don't filter by source at all) — skipping whichever are unchecked in the
    current Source filter. Callers on the web should run this out-of-band
    from the initial page render (see /meal/{meal_id}/search-api-results) so
    cached results aren't stuck waiting behind slow external APIs."""
    if sources is None:
        sources = [key for key, _name, _fn in _LIVE_SOURCES]
    raw_api: list[dict] = []
    for key, _name, fetch_fn in _LIVE_SOURCES:
        if key not in sources:
            continue
        try:
            raw_api.extend(fetch_fn(api_query, limit, raw_api))
        except Exception:
            pass

    candidate_ids = [f["fdcId"] for f in raw_api if isinstance(f.get("fdcId"), int)]
    with _db.get_db() as conn:
        annotations = _db.annotations_for_fdcids(conn, candidate_ids)
        cached_nutrients: dict[int, str | None] = {}
        for fid in candidate_ids:
            row = _db.get_cached_food(conn, fid)
            if row:
                cached_nutrients[fid] = row["nutrients_json"]

    def _aa_status(fdc_id: int, data_type: str, source: str) -> str:
        nuts_json = cached_nutrients.get(fdc_id)
        if nuts_json:
            return _usda.aa_indicator(json.loads(nuts_json))
        # Foundation/SR Legacy USDA entries reliably carry amino acid data
        # even before the first real fetch, so that guess is safe. OFF
        # (rarely has AA data) and CNF (has it for only a subset of foods —
        # no reliable "always has it" data_type to key off of) can't be
        # guessed with any confidence, so both show unconfirmed until fetched.
        if source == "usda" and data_type in ("Foundation", "SR Legacy"):
            return "~✓"
        return "✗"

    def _ann_gi(fdc_id: int) -> str:
        ann = annotations.get(fdc_id)
        if ann and ann["gi_estimate"] is not None:
            return str(int(round(ann["gi_estimate"])))
        return ""

    def _ann_gi_source(fdc_id: int) -> str:
        """Where a GI estimate came from, for the GI cell's tooltip — a rounded
        number in a narrow column says nothing about how trustworthy it is."""
        ann = annotations.get(fdc_id)
        if ann and ann["gi_estimate"] is not None and "gi_source" in ann.keys():
            return ann["gi_source"] or ""
        return ""

    def _ann_diaas(fdc_id: int) -> str:
        ann = annotations.get(fdc_id)
        if ann and ann["diaas_estimate"] is not None:
            return f"{ann['diaas_estimate']:.2f}"
        return ""

    results = []
    for food in raw_api:
        fid = food.get("fdcId")
        if not fid or fid in exclude_ids:
            continue
        exclude_ids.add(fid)
        if food.get("_from_off"):
            source, dtype = "off", "Open Food Facts"
        elif food.get("_from_cnf"):
            source, dtype = "cnf", "Canadian Nutrient File"
        else:
            source, dtype = "usda", food.get("dataType", "")
        results.append({
            "fdc_id":    fid,
            "name":      food.get("description", ""),
            "data_type": dtype,
            "brand":     food.get("brandOwner") or food.get("brandName") or "",
            "source":    source,
            "off_code":  food.get("_off_code", "") if source == "off" else "",
            "portions":  [],
            "aa":        _aa_status(fid, dtype, source),
            "gi":        _ann_gi(fid),
            "gi_source": _ann_gi_source(fid),
            "diaas":     _ann_diaas(fid),
        })
    return _sort_search_results(results, q, sort)


def _pantry_fdc_ids(conn) -> set[int]:
    return {r["fdc_id"] for r in _db.pantry_list(conn) if r["fdc_id"]}


def _pantry_id_by_fdc(conn) -> dict[int, int]:
    return {r["fdc_id"]: r["id"] for r in _db.pantry_list(conn) if r["fdc_id"]}


def _current_diet_pref() -> str:
    """Return the saved dietary preference, validated, defaulting to 'all'."""
    pref = _load_prefs_file().get("diet_pref", "all")
    return pref if pref in _VALID_DIET_PREFS else "all"


def _should_show_update_notice(tag: str) -> bool:
    """Whether the "update available" banner should be shown on this page
    load — True on every load for a given release, so it can't silently
    disappear before you've acted on it, unless you've explicitly dismissed
    that exact release via the banner's "Don't show this again for this
    version" checkbox. A release newer than the one you dismissed always
    gets through — dismissing one release never hides a later one."""
    return _load_prefs_file().get("update_notice_dismissed_tag") != tag

@asynccontextmanager
async def _lifespan(app: FastAPI):
    # Apply schema/migrations on web server startup, since the web app owns
    # the database and nothing else initializes it first.
    _db.init_db()
    with _db.get_db() as conn:
        from numa_app.services import demo_data as _demo_data
        if not _demo_data.seed_if_fresh_install(conn).get("skipped"):
            _mark_starter_problems_seen(conn)
        _day_profile.backfill_missing_day_profiles(conn)
        missing_snapshot_meals = _db.meals_missing_nutrient_snapshot(conn)
    # One-time backfill: meals whose bcp_g/calories predate the per-meal
    # nutrient snapshot (added for the Meals & Log / Daily Summary extra
    # columns feature) never got one written, so those columns show blank
    # for every day except ones recomputed since. Self-limiting — meals
    # already backfilled are excluded by the query above on future starts.
    for _meal in missing_snapshot_meals:
        _compute_and_store_meal_bcp(_meal["id"])
    with _db.get_db() as conn:
        missing_pct_dates = _db.dates_missing_day_pct_goal(conn)
    # Same idea for day_pct_goal: dates computed before it counted meals not
    # marked complete never got a value stored, so "% goal" shows blank on
    # the Daily Summary Recent Days table even though Day DCP now has one.
    for _meal_date in missing_pct_dates:
        _refresh_day_pct_goal(_meal_date)
    # Repair pass: give every recipe still showing NC one recompute attempt.
    # A recipe whose ingredient gained amino acid data through a path that
    # didn't cascade (bulk imports, older versions) would otherwise sit at
    # NC in the recipes list while its own /recipe/<id> page computes and
    # displays a real DCP. Genuinely-uncomputable recipes just stay NC, and
    # the cost is bounded by how many recipes are NC, not by the whole list.
    with _db.get_db() as conn:
        _stale_dcp_recipes = [r["id"] for r in _db.recipes_missing_dcp(conn)]
    for _rid in _stale_dcp_recipes:
        with _db.get_db() as conn:
            try:
                _recipe_dcp.recompute_recipe_dcp(_rid, conn)
            except Exception as _exc:
                _db.log_recompute_error(conn, "recipe", _rid,
                                        f"Startup DCP repair failed: {_exc}")
    yield

app = FastAPI(title="NuMa", lifespan=_lifespan)


@app.middleware("http")
async def _stale_meals_middleware(request: Request, call_next):
    """Before serving any page, recompute meals flagged stale by a food or
    recipe change (see _refresh_stale_meals), so Meals & Log, Daily Summary,
    trends and plots never show a stored DCP/nutrient snapshot computed from
    data that has since been edited."""
    if request.method == "GET" and not request.url.path.startswith("/static"):
        _refresh_stale_meals()
    return await call_next(request)
app.mount("/static", StaticFiles(directory=_WEB_DIR / "static"), name="static")
templates = Jinja2Templates(directory=_WEB_DIR / "templates")

# Custom Jinja2 filters
templates.env.filters["ftin_ft"]  = lambda cm: _profile.cm_to_ftin(cm)[0]
templates.env.filters["ftin_in"]  = lambda cm: round(_profile.cm_to_ftin(cm)[1], 1)
templates.env.filters["fromjson"] = json.loads


def _small_amount(value, places: int = 1) -> str:
    """Round to `places` decimals, but give a small non-zero value up to two
    more so it never shows as a bare 0 — a "0.0 g" row that still has a
    share of the total reads as an error to anyone not thinking about
    rounding. Anything too small even for that shows as "<0.001"."""
    if value is None:
        return ""
    for p in range(places, places + 3):
        text = f"{value:.{p}f}"
        if value == 0 or float(text) != 0:
            return text
    return "<" + f"{10 ** -(places + 2):.{places + 2}f}"


templates.env.filters["small_amount"] = _small_amount

def _manual_link(anchor: str, text: str = "Learn more") -> str:
    """Render an inline link to a user-manual section, opened in a new tab."""
    from markupsafe import Markup, escape
    return Markup(
        f'<a class="manual-link" href="/manual#{escape(anchor)}" target="_blank" rel="noopener">{escape(text)} &rarr;</a>'
    )

templates.env.globals["manual_link"] = _manual_link

# The set of user-edited food ids, loaded at most once per request (each
# request runs in its own context, so this never leaks between requests).
_user_edited_ids: contextvars.ContextVar[set[int] | None] = contextvars.ContextVar(
    "_user_edited_ids", default=None)


def _food_type(food, empty: str = "") -> str:
    """A food's type for display: its origin ("SR Legacy", "Branded", ...)
    plus " · user-edited" when the user has changed its data (see
    db.foods.user_edited). Every page that shows a food's type uses this.
    `food` is whatever row the page has (dict, sqlite3.Row or object) with
    a data_type and, ideally, an fdc_id."""
    def _field(key):
        try:
            return food[key]
        except (KeyError, IndexError, TypeError):
            return getattr(food, key, None)

    label = _field("data_type") or empty
    try:
        fid = int(_field("fdc_id"))
    except (TypeError, ValueError):
        return label
    return f"{label} · user-edited" if _is_user_edited(fid) and label else label


def _is_user_edited(fdc_id: int | None) -> bool:
    """db.foods.user_edited for one food, via the once-per-request id set."""
    if fdc_id is None:
        return False
    ids = _user_edited_ids.get()
    if ids is None:
        with _db.get_db() as conn:
            ids = _db.user_edited_ids(conn)
        _user_edited_ids.set(ids)
    return fdc_id in ids

templates.env.globals["food_type"] = _food_type


def _is_curator() -> bool:
    """True when NuMa runs from a source checkout rather than the packaged
    program every ordinary user downloads. Starter-data curation tools (the
    "Mark / Unmark as starter food" button) exist only then: the starter set
    is the project owner's to curate, and only the owner runs from source
    (owner's decision, 2026-09-29). A function, not a constant, so tests
    can switch it."""
    return not getattr(sys, "frozen", False)

templates.env.globals["is_curator"] = lambda: _is_curator()

_RELEASE_ANCHOR_RE = re.compile(r'<h4 id="(release-[^"]+-summary[^"]*)"')
_CHANGELOG_ANCHOR = "updates-log"
_release_anchor_cache: dict[str, tuple[float, str]] = {}

def _latest_release_anchor() -> str:
    """Anchor of the newest "Release <tag> summary" heading in the built manual.

    The home page's "see what changed" link points at what the running version
    actually shipped with — the most recent release summary — rather than the
    top of the log, which leads with the still-unreleased "Next release summary
    to this point". Falls back to the section heading if no release summary is
    found (a freshly pruned log, or a manual that failed to build).
    """
    try:
        path = _manual_update.get_active_manual(_MANUAL)["path"]
        mtime = path.stat().st_mtime
    except OSError:
        return _CHANGELOG_ANCHOR
    cached = _release_anchor_cache.get(str(path))
    if cached and cached[0] == mtime:
        return cached[1]
    try:
        m = _RELEASE_ANCHOR_RE.search(path.read_text(encoding="utf-8"))
    except OSError:
        return _CHANGELOG_ANCHOR
    anchor = m.group(1) if m else _CHANGELOG_ANCHOR
    _release_anchor_cache[str(path)] = (mtime, anchor)
    return anchor
templates.env.globals["is_local_source"] = _is_local_source

_EDITED_MARK = "\u270e"  # ✎ — beside a code, never part of it


def _code_display(fdc_id: int | None, recipe_id: int | None) -> tuple[str, str, bool] | None:
    """(code, hover title, edited) for a food/recipe, or None. edited = an
    outside-source food whose data the user has changed (foods.user_edited) —
    shown as a ✎ beside the code, so the code itself stays the same typed
    identifier whether or not the food was edited."""
    from numa_app.services.food_ids import classify_food_id, code_source_name
    classified = classify_food_id(fdc_id, recipe_id)
    if classified is None:
        return None
    code = classified[0]
    edited = recipe_id is None and _is_user_edited(fdc_id)
    title = code_source_name(code) + (", user-edited" if edited else "")
    return code, title, edited


def _food_id_tag(fdc_id: int | None, recipe_id: int | None = None) -> str:
    """Render the '(CODE)' annotation shown on its own line under a food/recipe
    name — the code's prefix already says the source, spelled out on hover;
    a ✎ follows the code on a user-edited food."""
    from markupsafe import Markup, escape
    shown = _code_display(fdc_id, recipe_id)
    if shown is None:
        return ""
    code, title, edited = shown
    mark = f" {_EDITED_MARK}" if edited else ""
    return Markup(f'<span class="food-id-tag" title="{escape(title)}">({escape(code)}{mark})</span>')

templates.env.globals["food_id_tag"] = _food_id_tag

def _food_id_short(fdc_id: int | None, recipe_id: int | None = None) -> str:
    """The display code for a compact standalone Code column (e.g. Food
    Cache), without food_id_tag()'s parentheses — plus the ✎ on a
    user-edited food. For display only: inside an attribute or form value
    use food_code(), which never carries the mark."""
    from markupsafe import Markup, escape
    shown = _code_display(fdc_id, recipe_id)
    if shown is None:
        return ""
    code, title, edited = shown
    if not edited:
        return code
    return Markup(f'<span title="{escape(title)}">{escape(code)} {_EDITED_MARK}</span>')


def _food_code(fdc_id: int | None, recipe_id: int | None = None) -> str:
    """The bare display code (U171477, R21 ...) — for form values and
    attributes, where food_id_short()'s ✎ markup doesn't belong."""
    classified = _classify_food_id(fdc_id, recipe_id)
    return classified[0] if classified else ""

templates.env.globals["food_id_short"] = _food_id_short
templates.env.globals["food_code"] = _food_code
from numa_app.services.food_ids import CODE_PREFIXES as _CODE_PREFIXES
templates.env.globals["code_prefixes"] = _CODE_PREFIXES
templates.env.globals["diet_labels"] = _DIET_LABELS
templates.env.globals["current_diet_pref"] = _current_diet_pref

# ---------------------------------------------------------------------------
# Nutrient display groups (ordered for presentation)
# ---------------------------------------------------------------------------

_NUTRIENT_GROUPS: list[tuple[str, list[str]]] = [
    # Each subtype row (_SUBTYPE_KEYS) directly follows its parent, so the
    # indent nests it under the right one: Fiber/Sugar under Carbohydrate,
    # the three fat types under Total Fat. With fat_g between carbs_g and
    # fiber_g, the indent read as "Fiber is part of fat".
    ("Macronutrients", [
        "calories", "protein_g", "carbs_g", "fiber_g", "sugar_g",
        "fat_g", "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    ]),
    ("Omega Fatty Acids", [
        "omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg",
    ]),
    ("Minerals", [
        "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
        "potassium_mg", "sodium_mg", "zinc_mg", "iodine_mcg", "selenium_mcg",
    ]),
    ("Vitamins", [
        "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
        "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
        "b6_mg", "folate_mcg", "b12_mcg",
    ]),
    ("Phytonutrients", [
        "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
        "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg", "isoflavones_mg",
    ]),
]

# Nutrients that are subsets of another row in the same table (Fiber/Sugar of
# Carbohydrates, the three fat types of Fat) rather than independent totals —
# rendered indented under their parent via the "subtype-row" CSS class.
_SUBTYPE_KEYS: set[str] = {
    "fiber_g", "sugar_g", "saturated_fat_g", "mono_fat_g", "poly_fat_g",
}

# Nutrients offered for Profile Optimal / max-limit configuration in Settings.
_NUTRIENT_TARGET_GROUPS: list[tuple[str, list[str]]] = [
    ("Macronutrients", ["calories", "protein_g", "carbs_g", "fiber_g", "sodium_mg",
                         "omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg"]),
    ("Minerals", ["calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
                  "potassium_mg", "zinc_mg", "iodine_mcg", "selenium_mcg"]),
    ("Vitamins", ["vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
                  "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
                  "b6_mg", "folate_mcg", "b12_mcg", "choline_mg"]),
    ("Phytonutrients", ["beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
                        "lutein_zeaxanthin_mcg", "beta_sitosterol_mg", "isoflavones_mg"]),
    ("Amino Acids", ["aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
                     "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
                     "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g"]),
]


def _rda_css(pct: float, rda_type: str) -> str:
    return "rda-" + rda_status(pct, rda_type)


_RDA_TYPE_ABBR = {"minimum": "min", "limit": "max", "target": "target"}
_RDA_TYPE_TITLE = {
    "minimum": "Minimum — aim to meet or exceed this amount",
    "limit": "Maximum — stay at or under this amount",
    "target": "Target — aim close to this amount, not just above or below it",
}


def _rda_type_abbr(rda_type: str | None) -> str:
    return _RDA_TYPE_ABBR.get(rda_type, "")


def _rda_type_title(rda_type: str | None) -> str:
    return _RDA_TYPE_TITLE.get(rda_type, "")


templates.env.globals["rda_type_abbr"] = _rda_type_abbr
templates.env.globals["rda_type_title"] = _rda_type_title

# GL band classification — "serving" for a food/meal/recipe portion, "day" for a
# whole-day total. Every GL display goes through these so the two scales can
# never drift apart again (they had, until 2026-09-27).
templates.env.globals["gl_band"] = gl_band
templates.env.globals["gl_band_caveat"] = gl_band_caveat


def _static_url(path: str) -> str:
    """/static/<path>?v=<mtime> — the mtime query string makes browsers fetch
    a static file afresh whenever it changes, instead of serving a stale cached
    copy on an ordinary refresh (hit 2026-10-02 with a style.css edit)."""
    try:
        mtime = int((_WEB_DIR / "static" / path).stat().st_mtime)
    except OSError:
        return f"/static/{path}"
    return f"/static/{path}?v={mtime}"


templates.env.globals["static_url"] = _static_url


def _nutrient_sections(nutrients: dict, rda: dict | None = None,
                       daily_nutrients: dict | None = None,
                       optimal: dict | None = None,
                       max_limits: dict | None = None,
                       dcp_g: float | None = None,
                       dcp_missing: list[str] | None = None) -> list[dict]:
    """dcp_g/dcp_missing insert a "(Digestible Complete Protein)" row right
    below Protein — the digestibility/amino-acid-adjusted figure a user
    actually gets to use, vs. the raw total USDA/OFF/etc. report. Only
    meaningful on pages analyzing what someone's eating (meal/day/recipe/
    food-portion), so callers with no DIAAS data simply pass nothing and get
    the old protein-only behavior. dcp_missing lists foods that had no
    amino-acid data and so were excluded from the DCP total — that makes the
    figure an understatement, flagged with an asterisk and a footnote."""
    max_limits = max_limits or {}
    sections = []
    for group_name, keys in _NUTRIENT_GROUPS:
        rows = []
        for key in keys:
            val = nutrients.get(key) or 0.0
            has_rda = rda and key in rda
            if not val and not has_rda:
                continue
            label, unit = _usda.nutrient_label(key)
            pct = rda_type = rda_css_val = None
            rda_minimum = rda_target = rda_maximum = None
            day_pct = day_rda_css = None
            if rda and key in rda:
                rda_val, rda_unit, rda_type = rda[key]
                if rda_val and rda_val > 0:
                    rda_goal = f"{rda_val:.1f} {rda_unit}"
                    if rda_type == "minimum":
                        rda_minimum = rda_goal
                    elif rda_type == "target":
                        rda_target = rda_goal
                    elif rda_type == "limit":
                        rda_maximum = rda_goal
                    pct = round(val / rda_val * 100, 0)
                    rda_css_val = _rda_css(pct, rda_type)
                    if daily_nutrients is not None:
                        day_pct = round(daily_nutrients.get(key, 0.0) / rda_val * 100, 0)
                        day_rda_css = _rda_css(day_pct, rda_type)

            opt_pct = opt_day_pct = opt_css = opt_day_css = opt_goal = opt_type = None
            if optimal and key in optimal:
                opt_val, opt_unit, opt_type = optimal[key]
                if opt_val and opt_val > 0:
                    opt_goal = f"{opt_val:.1f} {opt_unit}"
                    opt_pct = round(val / opt_val * 100, 0)
                    opt_css = _rda_css(opt_pct, opt_type)
                    if daily_nutrients is not None:
                        opt_day_pct = round(daily_nutrients.get(key, 0.0) / opt_val * 100, 0)
                        opt_day_css = _rda_css(opt_day_pct, opt_type)

            # UL (max limit) — shown as its own always-visible column (the
            # numeric ceiling itself) plus a near/over badge once there's a
            # day total to compare it against. limit_warn (used for the row's
            # own highlight class) and ul_css are the same value — one built-
            # in signal, shown two ways.
            ul_val = max_limits.get(key)
            ul_display = ul_pct = ul_css = None
            if ul_val:
                ul_display = f"{ul_val:.0f} {unit}"
                if daily_nutrients is not None:
                    day_total = daily_nutrients.get(key, 0.0)
                    ul_pct = round(day_total / ul_val * 100, 0)
                    if limit_warning(day_total, ul_val):
                        ul_css = "limit-over" if day_total >= ul_val else "limit-near"
            limit_warn = ul_css

            rows.append({
                "label":        label,
                "value":        round(val),
                "unit":         unit,
                "pct":          pct,
                "rda_type":     rda_type,
                "rda_css":      rda_css_val,
                "rda_minimum":  rda_minimum,
                "rda_target":   rda_target,
                "rda_maximum":  rda_maximum,
                "day_pct":      day_pct,
                "day_rda_css":  day_rda_css,
                "optimal_goal":     opt_goal,
                "optimal_type":     opt_type,
                "optimal_pct":      opt_pct,
                "optimal_css":      opt_css,
                "optimal_day_pct":  opt_day_pct,
                "optimal_day_css":  opt_day_css,
                "limit_warn":       limit_warn,
                "ul_val":       ul_val,
                "ul_display":   ul_display,
                "ul_pct":       ul_pct,
                "ul_css":       ul_css,
                "is_dcp_row":   False,
                "dcp_incomplete": False,
                "is_subtype":   key in _SUBTYPE_KEYS,
            })
            if key == "protein_g" and dcp_g is not None:
                # The DCP row is compared against the SAME protein target as
                # the raw-protein row above it. That is the comparison the
                # protein RDA is actually written for: 0.8 g/kg assumes
                # protein "of mixed quality as typically consumed", i.e.
                # highly digestible, so the target is effectively denominated
                # in reference-quality protein — which is exactly what DCP
                # measures. For an omnivore the two rows nearly coincide
                # (pooled DIAAS near 1.0); the gap between them widens as
                # protein quality falls, which is the whole point of showing
                # both. Leaving this row's percent blank (as it was) meant
                # the only percentage on the page was the raw-protein one,
                # which overstates adequacy for a plant-heavy diet.
                dcp_pct = dcp_css = None
                dcp_min = dcp_target = dcp_max = None
                dcp_type = None
                if rda and key in rda:
                    p_val, p_unit, dcp_type = rda[key]
                    if p_val and p_val > 0:
                        p_goal = f"{p_val:.1f} {p_unit}"
                        if dcp_type == "minimum":
                            dcp_min = p_goal
                        elif dcp_type == "target":
                            dcp_target = p_goal
                        elif dcp_type == "limit":
                            dcp_max = p_goal
                        dcp_pct = round(dcp_g / p_val * 100, 0)
                        dcp_css = _rda_css(dcp_pct, dcp_type)
                rows.append({
                    "label":        "(Digestible Complete Protein)" + ("\u00a0*" if dcp_missing else ""),
                    "value":        dcp_g,
                    "unit":         unit,
                    "pct": dcp_pct, "rda_type": dcp_type, "rda_css": dcp_css,
                    "rda_minimum": dcp_min, "rda_target": dcp_target, "rda_maximum": dcp_max,
                    "day_pct": None, "day_rda_css": None,
                    "optimal_goal": None, "optimal_type": None, "optimal_pct": None, "optimal_css": None,
                    "optimal_day_pct": None, "optimal_day_css": None,
                    "limit_warn": None, "ul_val": None, "ul_display": None, "ul_pct": None, "ul_css": None,
                    "is_dcp_row":   True,
                    "dcp_incomplete": bool(dcp_missing),
                    "is_subtype":   False,
                })
        if rows:
            sections.append({"name": group_name, "rows": rows})
    return sections


def _contributor_rank_options(nutrients: dict) -> list[tuple[str, list[tuple[str, str]]]]:
    """Nutrient picker options for the Top Contributors table: grouped like
    the main Nutritional Analysis table, filtered to nutrients with a
    nonzero total (no point offering to rank by something that's all zero)."""
    groups = []
    for group_name, keys in _NUTRIENT_GROUPS:
        opts = []
        for key in keys:
            if not nutrients.get(key):
                continue
            label, unit = _usda.nutrient_label(key)
            if key == "protein_g":
                label = "Protein — Digestible Complete"
            opts.append((key, f"{label} ({unit})"))
        if opts:
            groups.append((group_name, opts))
    return groups


def _default_rank_key(options: list[tuple[str, list[tuple[str, str]]]]) -> str | None:
    for _, opts in options:
        for key, _label in opts:
            if key == "protein_g":
                return key
    for _, opts in options:
        if opts:
            return opts[0][0]
    return None


_CONTRIBUTOR_TOP_N_OPTIONS = ["5", "10", "15", "20", "30", "all"]
_DEFAULT_CONTRIBUTOR_TOP_N = "10"


def _resolve_contributor_top_n(value: str | None) -> str:
    return value if value in _CONTRIBUTOR_TOP_N_OPTIONS else _DEFAULT_CONTRIBUTOR_TOP_N


def _build_contributors(ingredients: list[dict], rank: str | None, top_n: str, conn) -> dict:
    """Rank + slice ingredients for the Top Contributors table.

    Returns {"items", "total", "count", "top_n", "top_n_options", "is_dcp"} —
    `items` is sliced to top_n, `count` is how many nonzero contributors
    exist before slicing (for the "N of M shown" hint), `total` is the full
    sum across all contributors regardless of how many are shown.
    `top_n_options` is trimmed to values that would actually show fewer
    items than "all" — no point offering "Show 30" when only 6 foods
    contribute — and `top_n` is normalized to "all" if it wouldn't have
    trimmed anything anyway.

    Ranking by protein_g is special-cased to rank by each food's own
    standalone digestible complete protein (DCP) instead of raw protein
    grams — see rank_contributors_by_dcp() for why that's not the same as
    each food's share of the meal's real (complementarity-boosted) DCP."""
    if not rank:
        return {"items": [], "total": 0.0, "count": 0, "top_n": "all",
                "top_n_options": ["all"], "is_dcp": False}
    is_dcp = rank == "protein_g"
    result = rank_contributors_by_dcp(ingredients, conn) if is_dcp else rank_contributors(ingredients, rank)
    items = result["items"]
    count = len(items)
    top_n_options = [o for o in _CONTRIBUTOR_TOP_N_OPTIONS if o == "all" or int(o) < count] or ["all"]
    if top_n != "all" and int(top_n) >= count:
        top_n = "all"
    if top_n not in top_n_options:
        top_n = "all"
    if top_n != "all":
        items = items[:int(top_n)]
    return {"items": items, "total": result["total"], "count": count,
            "top_n": top_n, "top_n_options": top_n_options, "is_dcp": is_dcp}


def _load_rda(profile=None) -> dict | None:
    """Load the user profile and return computed RDA dict, or None if no profile set.

    Pass an explicit `profile` (e.g. from day_profile.get_profile_for_date)
    when scoring a specific logged date — otherwise this falls back to
    whatever profile is active right now, which is only correct for
    profile-less contexts (recipe/food analysis has no date to pin)."""
    if profile is None:
        profile = _profile.load_profile()
    if profile is None:
        return None
    return _profile.compute_rda(profile, diet_pref=_current_diet_pref())


def _diet_aware_daily_notes(nutrients: dict, rda: dict | None) -> dict:
    """Return {"iron_zinc": str|None, "b12": str|None} for a day's nutrient
    total, shown below the RDA comparison table."""
    diet_pref = _current_diet_pref()
    b12_note = None
    if rda and "b12_mcg" in rda:
        rda_val = rda["b12_mcg"][0]
        pct = (nutrients.get("b12_mcg", 0.0) / rda_val * 100.0) if rda_val > 0 else 0.0
        b12_note = b12_deficiency_note(diet_pref, pct)
    return {
        "iron_zinc": iron_zinc_bioavailability_note(diet_pref),
        "b12":       b12_note,
    }


def _load_optimal(profile=None) -> dict | None:
    """Load the user profile and return computed Profile Optimal dict, or None if no profile set."""
    if profile is None:
        profile = _profile.load_profile()
    if profile is None:
        return None
    return _profile.compute_optimal(profile)


def _load_max_limits(profile=None) -> dict | None:
    """Load the user profile and return configured max limits, or None if no profile set."""
    if profile is None:
        profile = _profile.load_profile()
    if profile is None:
        return None
    return _profile.get_max_limits(profile)


_OXALATE_SCORE_THRESHOLD = 0.50   # minimum fuzzy-match score
_OXALATE_STOP = frozenset({
    "raw", "cooked", "boiled", "baked", "roasted", "fried", "grilled", "steamed",
    "dried", "fresh", "frozen", "canned", "salted", "unsalted", "plain", "regular",
    "sweetened", "unsweetened", "whole", "ground", "crushed", "sliced", "diced",
    "chopped", "mashed", "shredded", "grated", "mixed", "with", "without", "and",
    "or", "the", "of", "in", "from", "for", "a", "an", "de", "mature", "seeds",
    "drained", "salt", "added", "flesh", "skin", "large", "medium", "small", "heat",
    "moist", "light", "dark", "heavy", "type", "types", "style",
})
_OXALATE_SERVING_UNITS: dict[str, float] = {
    "oz": 28.3495, "ounce": 28.3495, "ounces": 28.3495,
    "cup": 240.0, "cups": 240.0,
    "pint": 473.0,
    "tbsp": 15.0, "tbs": 15.0,
    "tsp": 5.0,
    "g": 1.0, "gram": 1.0, "grams": 1.0,
    "ml": 1.0,
    "lb": 453.592, "lbs": 453.592,
}
# Units where serving_size → grams conversion is reliable (true weight, not volume density)
_OXALATE_WEIGHT_UNITS = frozenset({"oz", "ounce", "ounces", "g", "gram", "grams", "lb", "lbs"})


def _parse_serving_qty(s: str):
    """Parse leading quantity from serving-size string. Returns (float, remainder) or (None, s)."""
    import re
    m = re.match(r'^(\d+)\s+(\d+)/(\d+)', s)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3)), s[m.end():]
    m = re.match(r'^(\d+)/(\d+)', s)
    if m:
        return int(m.group(1)) / int(m.group(2)), s[m.end():]
    m = re.match(r'^(\d+\.?\d*)', s)
    if m:
        return float(m.group(1)), s[m.end():]
    return None, s


def _serving_str_to_grams(serving_size: str) -> float | None:
    """Convert a serving-size string like '1/2 cup' or '1 1/2 oz' to grams."""
    if not serving_size:
        return None
    qty, rest = _parse_serving_qty(serving_size.strip().lower())
    if qty is None:
        return None
    unit_word = rest.strip().split()[0] if rest.strip() else ""
    grams_per_unit = _OXALATE_SERVING_UNITS.get(unit_word)
    if grams_per_unit is None:
        return None
    return qty * grams_per_unit


def _serving_is_weight(serving_size: str) -> bool:
    """True if serving_size is expressed in a true weight unit (oz, g, lb) vs volume."""
    if not serving_size:
        return False
    _, rest = _parse_serving_qty(serving_size.strip().lower())
    unit_word = rest.strip().split()[0] if rest.strip() else ""
    return unit_word in _OXALATE_WEIGHT_UNITS


def _oxalate_word_match(query: str, match_name: str) -> bool:
    """True if at least one significant word (≥4 chars, non-stop) from query is in match_name."""
    import re
    q_words = {w for w in re.findall(r'[a-z]+', query.lower())
               if len(w) >= 4 and w not in _OXALATE_STOP}
    m_words = set(re.findall(r'[a-z]+', match_name.lower()))
    return bool(q_words & m_words)


def _ann_source(ann) -> str:
    """The provenance of a row's GI estimate, or "" — for the GI cell tooltips in
    food/pantry/search listings, where the column is too narrow to show it.
    Empty unless there is a GI value for it to describe."""
    if ann is None or ann["gi_estimate"] is None:
        return ""
    return (ann["gi_source"] or "") if "gi_source" in ann.keys() else ""


def _oxalate_info(fdc_id: int | None, food_name: str) -> dict | None:
    """Return oxalate data for one food, auto-linking on first call if not yet linked.

    Returns None when oxalate.db is unavailable, fdc_id is invalid/negative, or no
    good match was found.  Returned dict keys:
        mg_per_100g (float|None), mg_per_serving (float|None), serving_size (str|None),
        category (str), ref_name (str), confirmed (bool), food_group (str),
        directly_measured (bool)

    directly_measured is the reference table's own asterisk: the value was
    measured in that food, rather than estimated from a similar one.
    """
    if not fdc_id or fdc_id < 0:
        return None
    import oxalate as _ox
    if not _ox.is_available():
        return None

    with _db.get_db() as conn:
        link = _db.oxalate_link_get(conn, fdc_id)
        # oxalate_links.fdc_id has a FK to foods(fdc_id) — a recipe/meal can
        # still reference a food that was later pruned from the cache, so
        # skip persisting a link (but still compute a result) in that case.
        food_cached = _db.get_cached_food(conn, fdc_id) is not None

    def _row_to_info(ox_row, confirmed: bool) -> dict | None:
        if ox_row is None:
            return None
        return {
            "mg_per_100g":   ox_row["oxalate_mg_per_100g"],
            "mg_per_serving": ox_row["oxalate_mg_per_serving"],
            "serving_size":  ox_row["serving_size"],
            "category":      ox_row["category"],
            "ref_name":      ox_row["food_name"],
            "confirmed":     confirmed,
            "food_group":    ox_row["food_group"] or "",
            "directly_measured": bool(ox_row["directly_measured"]),
        }

    if link is not None:
        if link["no_match"] or not link["oxalate_food_id"]:
            return None
        with _ox.get_oxalate_db() as ox_conn:
            ox_row = _ox.get_by_id(ox_conn, link["oxalate_food_id"])
        return _row_to_info(ox_row, bool(link["user_confirmed"]))

    # First time: fuzzy-match against the reference DB
    try:
        with _ox.get_oxalate_db() as ox_conn:
            candidates = _ox.search_similar(ox_conn, food_name, top_n=3)
    except Exception:
        return None

    best_match = None
    for score, row in candidates:
        if score >= _OXALATE_SCORE_THRESHOLD and _oxalate_word_match(food_name, row["food_name"]):
            best_match = (score, row)
            break

    if best_match:
        _, best = best_match
        if food_cached:
            with _db.get_db() as conn:
                conn.execute(
                    "INSERT INTO oxalate_links"
                    " (fdc_id, oxalate_food_id, user_confirmed, confirmed_at, no_match)"
                    " VALUES (?, ?, 0, datetime('now'), 0)"
                    " ON CONFLICT(fdc_id) DO NOTHING",
                    (fdc_id, best["id"]),
                )
        return _row_to_info(best, False)

    # No confident match — record to avoid re-querying
    if food_cached:
        with _db.get_db() as conn:
            conn.execute(
                "INSERT INTO oxalate_links"
                " (fdc_id, oxalate_food_id, user_confirmed, confirmed_at, no_match)"
                " VALUES (?, NULL, 0, datetime('now'), 1)"
                " ON CONFLICT(fdc_id) DO NOTHING",
                (fdc_id,),
            )
    return None


def _oxalate_for_items(items: list[dict]) -> dict | None:
    """Compute oxalate totals for a list of food items.

    Each item: {fdc_id, food_name, amount_g}.
    Returns {total_mg (exact portion where calculable), rows, qualitative, missing} or None.
    - rows: foods where mg/100g is known → exact mg computed
    - qualitative: foods with only per-serving data → category + reference serving shown
    - missing: foods with no oxalate data
    """
    import oxalate as _ox
    if not _ox.is_available():
        return None

    total_mg = 0.0
    rows: list[dict] = []
    qualitative: list[dict] = []
    qualitative_seen: set = set()
    missing: list[str] = []
    # The same food can arrive more than once (e.g. two servings of one
    # recipe, or a food both logged directly and inside a recipe) — sum it
    # into one row rather than listing it per occurrence.
    row_by_key: dict = {}

    def _add_row(fdc_id, name, amount_g, mg, info):
        key = fdc_id if fdc_id else name.lower()
        row = row_by_key.get(key)
        if row is None:
            row = {"name": name, "amount_g": 0.0, "mg": 0.0,
                   "category": info["category"], "confirmed": info["confirmed"]}
            row_by_key[key] = row
            rows.append(row)
        row["amount_g"] += amount_g
        row["mg"] += mg

    for item in items:
        fdc_id   = item.get("fdc_id")
        name     = item.get("food_name", "")
        amount_g = float(item.get("amount_g") or 0)
        if not amount_g:
            continue
        info = _oxalate_info(fdc_id, name)
        if not info:
            missing.append(name)
            continue

        if info["mg_per_100g"] is not None:
            mg = info["mg_per_100g"] * amount_g / 100.0
            total_mg += mg
            _add_row(fdc_id, name, amount_g, mg, info)
        elif info["mg_per_serving"] is not None:
            serving_g = _serving_str_to_grams(info["serving_size"] or "")
            if serving_g and serving_g > 0 and _serving_is_weight(info["serving_size"] or ""):
                # Weight-based serving → derive mg/100g and compute exact portion mg
                mg_per_100g = info["mg_per_serving"] / serving_g * 100.0
                mg = mg_per_100g * amount_g / 100.0
                total_mg += mg
                _add_row(fdc_id, name, amount_g, mg, info)
            else:
                # Volume-based serving — density unknown, category only.
                # It's a category, not a quantity, so the same food showing
                # up more than once in the meal/recipe shouldn't repeat here.
                dedupe_key = fdc_id if fdc_id else name.lower()
                if dedupe_key not in qualitative_seen:
                    qualitative_seen.add(dedupe_key)
                    qualitative.append({
                        "name":      name,
                        "category":  info["category"],
                        "confirmed": info["confirmed"],
                    })
        else:
            missing.append(name)

    if not rows and not qualitative:
        return None
    for row in rows:
        row["amount_g"] = round(row["amount_g"], 1)
        row["mg"] = round(row["mg"], 1)
    missing = list(dict.fromkeys(missing))
    cat_rank = {cat: i for i, cat in enumerate(_ox.CATEGORY_ORDER)}
    qualitative.sort(key=lambda r: (cat_rank.get(r["category"], len(cat_rank)), r["name"].lower()))
    return {
        "total_mg":   round(total_mg, 1) if rows else None,
        "rows":       rows,
        "qualitative": qualitative,
        "missing":    missing,
    }


def _protein_section(food_name: str, nutrients: dict) -> dict | None:
    if nutrients.get("protein_g", 0) <= 0:
        return None
    if not _usda.has_amino_acid_data(nutrients):
        return None
    # Use the same pure-digestibility table (and user overrides) as meal-level
    # DIAAS, not usda_nutrients.get_diaas() — that table stores full,
    # already AA-balance-adjusted literature DIAAS scores, and combining it
    # with protein_completeness()'s own limiting-AA ratio double-penalizes
    # amino acid limitation (e.g. bread's DCP came out ~30% low).
    with _db.get_db() as conn:
        digestibility, _digest_source = _diaas.get_digestibility(food_name, conn)
    pc = _usda.protein_completeness(nutrients, digestibility)
    if not pc["has_data"]:
        return None
    limiting_label = _usda.nutrient_label(pc["limiting_aa"])[0] if pc["limiting_aa"] else None
    aa_rows = [
        {
            "label": _usda.nutrient_label(k)[0],
            "score": round(v, 3),
            "met": v >= 1.0,
        }
        for k, v in sorted(pc["scores"].items(), key=lambda x: x[1])
    ]
    protein_raw = nutrients.get("protein_g", 0.0)
    protein_digestible = round(protein_raw * digestibility, 1)
    limiting_score = min(pc["scores"].values()) if pc["scores"] else None
    dcp_g = None
    if limiting_score is not None:
        dcp_g = round(protein_digestible * min(1.0, limiting_score), 1)
    return {
        "diaas":              digestibility,
        "diaas_pct":          min(100, round(digestibility * 100)),
        "diaas_level":        "good" if digestibility >= 0.90 else ("ok" if digestibility >= 0.70 else "low"),
        "complete":           pc["complete"],
        "limiting_aa":        limiting_label,
        "limiting_score":     round(limiting_score, 3) if limiting_score is not None else None,
        "aa_rows":            aa_rows,
        "protein_raw":        round(protein_raw, 1),
        "protein_digestible": protein_digestible,
        "dcp_g":              dcp_g,
    }


def _effective_ignored(ignore_complements: list[str], unignore: list[str]) -> set[str]:
    """Names in `ignore_complements` minus any the user has just checked to restore
    in the "manage ignored foods" panel. `ignore_complements` includes both the
    hidden inputs carrying forward previously-ignored names and any newly checked
    suggestion-card checkboxes from this submission."""
    unignore_lower = {n.lower() for n in unignore}
    return {n for n in ignore_complements if n.lower() not in unignore_lower}


def _parse_anchor_overrides(anchor_name: list[str], anchor_grams: list[str]) -> dict[str, float]:
    """Zip a complement page's parallel `anchor_name`/`anchor_grams` form fields
    into a {name.lower(): grams} map, skipping blank or non-positive entries.
    See complements.build_complement_display's anchor_overrides docstring."""
    overrides: dict[str, float] = {}
    for name, grams_str in zip(anchor_name, anchor_grams):
        if not name or not grams_str:
            continue
        try:
            grams = float(grams_str)
        except ValueError:
            continue
        if grams > 0:
            overrides[name.lower()] = grams
    return overrides


def _food_complement_section(food_name: str, nutrients: dict, exclude_names: set[str] | None = None,
                              comp_sort: str | None = None, diaas_sort: str | None = None,
                              anchor_overrides: dict[str, float] | None = None) -> dict:
    """Complement suggestions for a single food, using its own digestibility (diaas.get_digestibility, same table meal-level DIAAS uses)."""
    if not _usda.has_amino_acid_data(nutrients) or nutrients.get("protein_g", 0) <= 0:
        return {"no_data": True}
    with _db.get_db() as conn:
        digestibility, _digest_source = _diaas.get_digestibility(food_name, conn)
    prefs = _load_prefs_file()
    diet_pref = prefs.get("diet_pref", "all")
    pantry = _web_pantry_candidates() + _web_recipe_candidates()
    cache_candidates = _complements.load_cache_candidates({c["name"].lower() for c in pantry})
    comp_sort = comp_sort or _resolve_sort(None, "sort_complements", "dcp", _COMP_SORT_MODES)
    diaas_sort = diaas_sort or _resolve_sort(None, "sort_diaas_improvers", "effect", _DIAAS_SORT_MODES)
    return _complements.build_complement_display(
        nutrients, pantry, diet_pref=diet_pref,
        digestibility=digestibility, base_food_name=food_name,
        max_improver_grams=120, cache_candidates=cache_candidates,
        exclude_names=exclude_names,
        comp_sort=comp_sort,
        diaas_sort=diaas_sort,
        anchor_overrides=anchor_overrides,
    )


def _gi_opt_out() -> bool:
    """True when the user has said they do not record glycemic index data.

    It means numa stops ASKING: no GI in _missing_annotations(), so adding a
    food never detours to the Annotate page for a GI value alone, and no notice
    about which GI reference table is in use. It is the global form of the
    per-food gi_no_prompt flag, and it hides nothing that is already recorded —
    a GI value already saved is still shown and still used for glycemic load.
    """
    prefs = _load_prefs_file()
    # gi_notices_off was this setting's first, notices-only name.
    return bool(prefs.get("gi_opt_out", prefs.get("gi_notices_off")))


def _gi_table_home_notice() -> dict | None:
    """Home-page notice when GI lookups are NOT being answered by a locally-built
    2021 table. Returns None when they are, so the banner is self-clearing.

    The Annotate page and Settings both report the active table, but only when
    you go looking. The state worth interrupting for is the one you would not go
    looking for: a gi_data_local.json that has been moved, renamed or lost, after
    which every lookup silently falls back to the bundled 2008 edition. So the
    last edition seen is remembered in prefs, and losing a 2021 table is reported
    differently from never having built one.

    A dismissal is cleared again the moment a 2021 table is seen, so it silences
    the notice you have read rather than the next disappearance.
    """
    prefs = _load_prefs_file()
    info = _gi_lookup.active_table_info()
    last_seen = prefs.get("gi_table_last_seen_edition")
    edition = info["edition"]
    # "Lost" is sticky, not a one-load event: the transition is only visible on
    # the first page load after it happens, and softening the wording on the
    # second load would bury the very thing worth reporting.
    lost = bool(prefs.get("gi_table_lost")) or last_seen == 2021
    if edition != last_seen:
        updates = {"gi_table_last_seen_edition": edition}
        if edition == 2021:
            updates["gi_table_lost"] = False
            updates["gi_table_notice_dismissed"] = False
        elif last_seen == 2021:
            updates["gi_table_lost"] = True
        _save_prefs_file(updates)
    # Opted out of glycemic index data altogether: which table would answer a
    # lookup is then of no interest, including the case where none would. Note
    # this is checked AFTER the state above is recorded, not instead of it — a
    # table that goes missing during an opt-out must still be reported as
    # missing if the notices are ever turned back on.
    if _gi_opt_out():
        return None
    if edition == 2021:
        return None
    # A table that cannot be read at all is never silenced: nothing in the
    # program works around it, and no lookup will return anything.
    if edition is not None and prefs.get("gi_table_notice_dismissed"):
        return None
    return {"edition": edition, "rows": info["rows"], "lost": lost,
            "dismissible": edition is not None}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, updated: int = 0, update_error: str = "",
                manual_updated: int = 0, manual_update_error: str = ""):
    diet_pref = _current_diet_pref()
    diet_label = _DIET_LABELS.get(diet_pref, diet_pref)
    profile = _profile.load_profile()
    profile_label = None
    if profile:
        profile_label = (
            f"{profile.name} — age {profile.age}, {profile.sex}, "
            f"{_profile.format_weight(profile.weight_kg, profile.weight_unit)}, "
            f"{_profile.format_height(profile.height_cm, profile.height_unit)}, "
            f"{_profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level)}"
        )
    with _db.get_db() as conn:
        unacked_errors = [dict(r) for r in _db.list_unacked_recompute_errors(conn)]
        db_issues = _db.check_db_integrity(conn)
        has_any_meals = _db.meal_count_recent(conn) > 0
        # Starter foods/recipes this version added or improved since the
        # last version this install ran (see demo_data.record_version_changes).
        from numa_app.services import demo_data as _demo_data
        starter_changes = _demo_data.pending_changes(conn, silent=_is_curator())
    db_issue_count = sum(len(v) for v in db_issues.values())
    if starter_changes["acknowledged"] or not any(
            starter_changes[k] for k in ("new_foods", "improved_foods", "new_recipes", "improved_recipes")):
        starter_changes = None
    # Right after a successful self-update, the running process hasn't
    # restarted yet — VERSION in memory is still the old value, so the
    # check would (correctly, but confusingly) still report the release
    # just installed as "available." Skip it until the next real launch.
    update_available = None if updated else await run_in_threadpool(_update_check.check_for_update, VERSION)
    if update_available and not _should_show_update_notice(update_available["tag"]):
        update_available = None
    # What that release would change in the starter set, for its banner.
    starter_preview = None
    if update_available and update_available.get("starter_manifest"):
        with _db.get_db() as conn:
            starter_preview = _demo_data.preview_changes(conn, update_available["starter_manifest"])
    # Same stale-html rebuild /manual does, so the "Current manual version"
    # stamp below reflects the latest user-manual.md edit, not whatever
    # user-manual.html happened to be built from last.
    from numa_app.services.manual_build import rebuild_manual_if_stale
    await run_in_threadpool(rebuild_manual_if_stale)
    active_manual = _manual_update.get_active_manual(_MANUAL)
    manual_update_available = None if manual_updated else await run_in_threadpool(
        _manual_update.check_for_manual_update, active_manual["stamp"], VERSION)
    if manual_update_available and _load_prefs_file().get("manual_notice_dismissed_stamp") == manual_update_available["stamp"]:
        manual_update_available = None
    prefs = _load_prefs_file()
    home_plot_qs = prefs.get("home_nutrient_plot_qs") if prefs.get("home_nutrient_plot_enabled") else None
    # "Roll to last complete day" (see _nutrient_plot_params) truncates the
    # plotted date range at the most recent day whose meals are ALL marked
    # complete — so a day with even one still-incomplete meal, and anything
    # after it, silently disappears from the plot. The plot itself gives no
    # indication this is happening, so the Home page caption below it needs
    # to say so explicitly when this plot has that toggle on.
    plot_rolls_to_complete = bool(home_plot_qs) and parse_qs(home_plot_qs).get("rolling", ["0"])[0] == "1"
    home_plot_smoothing = None
    if home_plot_qs:
        _hq = parse_qs(home_plot_qs)
        _window = _parse_smoothing_window(_hq.get("smoothing", [None])[0])
        with _db.get_db() as conn:
            _chosen, _dates, _a = _nutrient_plot_params(
                conn, _hq.get("nutrients", []), _hq.get("days_back", [None])[0],
                _hq.get("anchor_date", [None])[0], rolling=_hq.get("rolling", ["0"])[0] == "1")
            _rolling = _hq.get("rolling", ["0"])[0] == "1"
            _data, _axis, _skipped = _plot_days(conn, _dates, _rolling)
            _skip = _db.meal_dates_with_incomplete(conn) if _rolling else set()
            _lead = _smoothing_lead_dates(conn, _data[0], _window, _skip) if _data else []
            home_plot_smoothing = _smoothing_info(_window, _lead, _data, _axis, _skipped)
    return templates.TemplateResponse(
        request, "home.html", {
            "home_body": _render_home_md_short() if home_plot_qs else _render_home_md(),
            "home_plot_qs": home_plot_qs,
            "plot_rolls_to_complete": plot_rolls_to_complete,
            "home_plot_smoothing": home_plot_smoothing,
            "show_plot_notice": has_any_meals and not home_plot_qs,
            "version": VERSION, "version_note": NEW_VERSION_NOTE,
            "version_date": VERSION, "release_version": RELEASE_VERSION,
            "diet_label": diet_label, "profile_label": profile_label,
            "unacked_errors": unacked_errors,
            "db_issue_count": db_issue_count,
            "data_check_reminder": _data_check_reminder(),
            "update_available": update_available,
            "self_update_available": _self_update.is_available(),
            "windows_exe_dir": _self_update.windows_exe_dir(),
            "starter_changes_text": _demo_data.describe_changes(starter_changes) if starter_changes else "",
            "starter_preview_text": _demo_data.describe_changes(starter_preview) if starter_preview else "",
            "updated": updated,
            "update_error": update_error,
            "manual_stamp": active_manual["stamp"],
            "changelog_anchor": _latest_release_anchor(),
            "manual_update_available": manual_update_available,
            "manual_updated": manual_updated,
            "manual_update_error": manual_update_error,
            "gi_table_notice": _gi_table_home_notice(),
        }
    )


@app.post("/manual-update-now")
async def manual_update_now():
    """Download, verify, and install the newest published User Manual —
    independent of program updates; see numa_app/services/manual_update.py.
    Takes effect immediately (no relaunch)."""
    current = _manual_update.get_active_manual(_MANUAL)["stamp"]
    result = await run_in_threadpool(_manual_update.install_update, current)
    if result["ok"]:
        return RedirectResponse("/?manual_updated=1", status_code=303)
    return RedirectResponse(f"/?{urlencode({'manual_update_error': result['error']})}", status_code=303)


@app.post("/settings/gi-notices", response_class=RedirectResponse)
async def settings_gi_notices_post(gi_opt_out: str = Form("")):
    """Opt out of (or back into) glycemic index data entirely: numa stops asking
    for GI values when a food is added, and stops reporting which GI reference
    table is in use. Separate from the home notice's own 'do not remind me
    again', which silences one message that has been read."""
    _save_prefs_file({"gi_opt_out": bool(gi_opt_out)})
    return RedirectResponse("/settings?saved=gi_notices#gi-table", status_code=303)


@app.post("/gi-table-notice/ack-banner", response_class=RedirectResponse)
async def gi_table_notice_ack_banner():
    """'Do not remind me again' on the home-page GI-table banner. Cleared
    automatically if a locally-built 2021 table is ever seen again, so a later
    disappearance of it is still reported."""
    _save_prefs_file({"gi_table_notice_dismissed": True})
    return RedirectResponse("/", status_code=303)


@app.post("/manual-notice/ack-banner", response_class=RedirectResponse)
async def manual_notice_ack_banner(stamp: str = Form(...)):
    """'Don't show this again' on the home-page manual-update banner —
    dismisses only that exact manual version."""
    _save_prefs_file({"manual_notice_dismissed_stamp": stamp})
    return RedirectResponse("/", status_code=303)


@app.post("/update-now")
async def update_now():
    """Download and install the latest release in place of the running
    packaged binary — see numa_app/services/self_update.py. The current
    session keeps running on its already-loaded binary; a relaunch is
    needed to pick up the new one."""
    result = await run_in_threadpool(_self_update.perform_update)
    if result["ok"]:
        return RedirectResponse("/?updated=1", status_code=303)
    return RedirectResponse(f"/?{urlencode({'update_error': result['error']})}", status_code=303)


@app.post("/recompute-errors/ack-banner", response_class=RedirectResponse)
async def recompute_errors_ack_banner():
    """'Got it, don't remind again' on the home-page system-issues banner —
    silences it for currently-outstanding errors without resolving them; they
    remain visible under Settings > System Issues until actually addressed."""
    with _db.get_db() as conn:
        _db.ack_recompute_errors_banner(conn)
    return RedirectResponse("/", status_code=303)


def _search_local_results(query: str) -> list[dict]:
    """Local (cache/pantry/recipe) candidates for a food-search query — the
    instant, no-network part of Food Search / Analyze a Food Portion. Shared
    by the initial synchronous render and the async '-api-results' endpoints,
    which merge this with external results before sorting so a weak local
    match never outranks a better external one just by rendering first."""
    results: list[dict] = []
    query_words = query.lower().split()
    with _db.get_db() as conn:
        all_recipes = _db.recipe_list(conn)
        cached = _db.search_cached_foods(conn, query)
        annotations = _db.annotations_for_fdcids(conn, [row["fdc_id"] for row in cached])
        pantry_id_by_fdc = _pantry_id_by_fdc(conn)
    for row in cached:
        with _db.get_db() as conn:
            full = _db.get_cached_food(conn, row["fdc_id"])
        nutrients = json.loads(full["nutrients_json"]) if full and full["nutrients_json"] else {}
        ann = annotations.get(row["fdc_id"])
        results.append({
            "fdc_id":    row["fdc_id"],
            "name":      row["name"],
            "data_type": row["data_type"],
            "brand":     row["brand"] or "",
            "source":    "pantry" if row["fdc_id"] in pantry_id_by_fdc else "cache",
            "pantry_id": pantry_id_by_fdc.get(row["fdc_id"]),
            "aa":        _usda.aa_indicator(nutrients),
            "gi":        round(ann["gi_estimate"]) if ann and ann["gi_estimate"] is not None else None,
            "gi_source": _ann_source(ann),
            "diaas":     round(ann["diaas_estimate"], 2) if ann and ann["diaas_estimate"] is not None else None,
            "has_notes": bool(row["notes"]),
        })
    matching_recipes = [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)]
    recipe_aa_status = _recipe_aa_status([r["id"] for r in matching_recipes])
    for r in matching_recipes:
        results.append({
            "_type":     "recipe",
            "recipe_id": r["id"],
            "name":      r["name"],
            "data_type": "Recipe",
            "brand":     "",
            "source":    "recipe",
            "aa":        recipe_aa_status[r["id"]],
            "gi":        None,
            "diaas":     None,
            "has_notes": False,
        })
    # Static (bundled-dataset, no network) external sources are instant like
    # Pantry/Cache/Recipe, so they're merged in here rather than through the
    # async external-fetch path used by USDA/OFF/CNF.
    results.extend(_static_source_candidates(query))
    return results


async def _search_logic(request: Request, query: str, template: str, extra_ctx: dict | None = None,
                         sort: str | None = None, source: list[str] | None = None,
                         limit: int | None = None):
    """Shared search logic for food search and analyze-portion pages."""
    query = query.strip()
    results = []
    error = None
    sort = _resolve_sort(sort, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)

    # Barcode detection: 12 or 13 consecutive digits (UPC-A or EAN-13).
    # Spaces and hyphens are stripped first so "0 12345 67890 1" also works.
    # Cache first, then a real Open Food Facts barcode lookup (not a text
    # search, which can't reliably match a GTIN). Typing the exact barcode is
    # itself the confirmation, so the match is shown as the one search result
    # rather than routed through a separate confirm step.
    _bc_digits = re.sub(r"[\s\-]", "", query)
    if _bc_digits.isdigit() and len(_bc_digits) in (12, 13):
        bc_fdc_id = _off.off_id(_bc_digits)
        with _db.get_db() as conn:
            bc_cached = _db.get_cached_food(conn, bc_fdc_id)
        if bc_cached:
            nutrients = json.loads(bc_cached["nutrients_json"]) if bc_cached["nutrients_json"] else {}
            results.append({
                "fdc_id":    bc_cached["fdc_id"],
                "name":      bc_cached["name"],
                "data_type": bc_cached["data_type"],
                "brand":     bc_cached["brand"] or "",
                "source":    "cache",
                "aa":        _usda.aa_indicator(nutrients),
                "gi":        None,
                "diaas":     None,
                "has_notes": bool(bc_cached["notes"]),
            })
        else:
            try:
                detail = _off.lookup_by_barcode(_bc_digits)
            except Exception as exc:
                detail = None
                error = f"Open Food Facts unavailable: {exc}"
            if detail is not None:
                with _db.get_db() as conn:
                    _db.cache_food(
                        conn, detail["fdcId"], detail["name"], detail.get("dataType", ""),
                        detail.get("brand"), detail.get("servingSize"), detail.get("servingUnit"),
                        detail.get("nutrients", {}), detail.get("portions"),
                    )
                    _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
                results.append({
                    "fdc_id":    detail["fdcId"],
                    "name":      detail["name"],
                    "data_type": detail.get("dataType", ""),
                    "brand":     detail.get("brand") or "",
                    "source":    "off",
                    "aa":        _usda.aa_indicator(detail.get("nutrients", {})),
                    "gi":        None,
                    "diaas":     None,
                    "has_notes": False,
                })
            elif not error:
                error = f"Barcode {_bc_digits} not found in Open Food Facts. Try searching by product name instead."
        ctx = {"results": results, "query": query, "error": error, "sort": sort, "source": source,
               "limit": limit, "external_source_labels": _external_source_labels(source),
               "source_filters": _SEARCH_SOURCE_FILTERS, "source_labels": _SEARCH_SOURCE_LABELS,
               "omitted_sources": _omitted_source_labels(source)}
        if extra_ctx:
            ctx.update(extra_ctx)
        return templates.TemplateResponse(request, template, ctx)

    if query:
        # USDA/Open Food Facts results are NOT fetched here — they're 2-3
        # blocking network calls that would stall this page behind them.
        # The browser fetches them separately once this (instant, local-only)
        # response has rendered — see /food/search-api-results and
        # /food/analyze-portion-api-results, same pattern as the meal
        # add-food panel's /meal/{meal_id}/search-api-results. Those async
        # endpoints re-fetch these same local results and merge+re-sort them
        # with the external ones, so a weak local match never outranks a
        # much better external one just by rendering first.
        results = _search_local_results(query)
        results = _sort_search_results(results, query, sort)
        results = _cap_results_preserving_local(_filter_search_results_by_source(results, source), limit)

    ctx = {"results": results, "query": query, "error": error, "sort": sort, "source": source,
           "limit": limit, "external_source_labels": _external_source_labels(source),
           "source_filters": _SEARCH_SOURCE_FILTERS, "source_labels": _SEARCH_SOURCE_LABELS,
           "omitted_sources": _omitted_source_labels(source)}
    if extra_ctx:
        ctx.update(extra_ctx)
    return templates.TemplateResponse(request, template, ctx)


@app.get("/food/search", response_class=HTMLResponse)
async def food_search_get(request: Request, query: str = Query(default=""), sort: str | None = None,
                           source: list[str] | None = Query(default=None), limit: int | None = None):
    if query.strip():
        return await _search_logic(request, query, "search.html", sort=sort, source=source, limit=limit)
    sort = _resolve_sort(sort, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    return templates.TemplateResponse(request, "search.html", {
        "results": [], "query": "", "sort": sort, "source": source, "limit": limit,
        "external_source_labels": _external_source_labels(source),
        "source_filters": _SEARCH_SOURCE_FILTERS, "source_labels": _SEARCH_SOURCE_LABELS,
    })


@app.post("/food/search", response_class=HTMLResponse)
async def food_search_post(request: Request, query: str = Form(""), limit: int | None = Form(None)):
    return await _search_logic(request, query, "search.html", limit=limit)


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(""), limit: int | None = Form(None)):
    """Legacy alias — same as POST /food/search."""
    return await _search_logic(request, query, "search.html", limit=limit)


@app.get("/food/search-api-results", response_class=HTMLResponse)
async def food_search_api_results(request: Request, query: str = "", sort: str | None = None,
                                   source: list[str] | None = Query(default=None),
                                   limit: int | None = None):
    """Fetched by JS on the Food Search page after the initial (cache-only)
    render. Returns the FULL result set — local results merged with USDA/OFF
    and re-sorted together, not just the external rows appended below — so a
    weak local match never outranks a much better external one just because
    the local pass rendered first. The JS replaces the table body with this
    response rather than appending to it."""
    sort = _resolve_sort(sort, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    query = query.strip()
    results: list[dict] = []
    if query:
        local = _search_local_results(query)
        exclude_ids = {r["fdc_id"] for r in local if r.get("fdc_id")}
        external = _external_food_search_results(query, exclude_ids, query, sort, sources=source, limit=limit)
        results = _sort_search_results(local + external, query, sort)
        results = _cap_results_preserving_local(_filter_search_results_by_source(results, source), limit)
    return templates.TemplateResponse(request, "_search_api_rows.html", {"results": results})


@app.get("/food/analyze-portion-api-results", response_class=HTMLResponse)
async def food_analyze_portion_api_results(request: Request, query: str = "", sort: str | None = None,
                                            source: list[str] | None = Query(default=None),
                                            limit: int | None = None):
    """Same as /food/search-api-results, for the Analyze a Food Portion page."""
    sort = _resolve_sort(sort, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    query = query.strip()
    results: list[dict] = []
    if query:
        local = _search_local_results(query)
        exclude_ids = {r["fdc_id"] for r in local if r.get("fdc_id")}
        external = _external_food_search_results(query, exclude_ids, query, sort, sources=source, limit=limit)
        results = _sort_search_results(local + external, query, sort)
        results = _cap_results_preserving_local(_filter_search_results_by_source(results, source), limit)
    return templates.TemplateResponse(request, "_analyze_portion_api_rows.html", {"results": results})


@app.get("/search/suggestions")
async def search_suggestions_api(query: str = "") -> dict:
    """Did-you-mean suggestions for a search box that came up empty —
    called by JS (see base.html's numaInitSearchSuggestions) once a page's
    own search-no-results element becomes visible. Shared by every search
    box in the app; see numa_app.services.search_suggest for how matches
    are found (fully local, no network call)."""
    with _db.get_db() as conn:
        return {"suggestions": _search_suggest.suggest(conn, query)}


@app.post("/food/confirm-aa", response_class=RedirectResponse)
async def food_confirm_aa(
    fdc_ids: list[int] = Form(...),
    query: str = Form(""),
    sort: str = Form(""),
    source: list[str] = Form([]),
    limit: int | None = Form(None),
):
    """Fetch and cache full USDA details for the selected search-result foods,
    so their amino-acid badge changes from the coarse '~✓' guess (search
    results carry no nutrient data, only name/type) to a confirmed ✓ or ✗ —
    without fetching details for every uncached result in the list, which
    would cost one USDA API call per result on every search."""
    for fdc_id in fdc_ids:
        if fdc_id <= 0:
            continue
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached:
            continue
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception:
            continue
        with _db.get_db() as conn:
            _db.cache_food(
                conn, fdc_id=detail["fdcId"], name=detail["name"],
                data_type=detail.get("dataType", ""),
                brand=detail.get("brand"),
                serving_size=detail.get("servingSize"),
                serving_unit=detail.get("servingUnit"),
                nutrients=detail.get("nutrients", {}),
                portions=detail.get("portions", []),
            )
            _recipe_dcp.cascade_food_change(detail["fdcId"], conn)

    from urllib.parse import urlencode
    params: dict[str, str | list[str]] = {"query": query}
    if sort:
        params["sort"] = sort
    if source:
        params["source"] = source
    if limit:
        params["limit"] = str(limit)
    return RedirectResponse(f"/food/search?{urlencode(params, doseq=True)}", status_code=303)


# ---------------------------------------------------------------------------
# Food sub-pages: analyze portion, analyze recipe portion, convert, compare,
#                 cache, pantry, custom profiles, annotate
# NOTE: /food/{fdc_id} is registered AFTER all literal /food/* paths so that
#       Starlette matches specific paths first (first-match routing).
# ---------------------------------------------------------------------------

@app.get("/food/analyze-portion", response_class=HTMLResponse)
async def food_analyze_portion_get(request: Request):
    sort = _resolve_sort(None, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    source = _resolve_source_filter(None, "sort_food_search_source")
    limit = _resolve_result_limit(None)
    return templates.TemplateResponse(request, "food_analyze_portion.html", {
        "results": [], "query": "", "sort": sort, "source": source, "limit": limit,
        "external_source_labels": _external_source_labels(source),
        "source_filters": _SEARCH_SOURCE_FILTERS, "source_labels": _SEARCH_SOURCE_LABELS,
    })


@app.post("/food/analyze-portion", response_class=HTMLResponse)
async def food_analyze_portion_post(request: Request, query: str = Form(""), source: list[str] = Form([]),
                                     limit: int | None = Form(None)):
    return await _search_logic(request, query, "food_analyze_portion.html", source=source, limit=limit)


@app.get("/food/analyze-recipe-portion", response_class=HTMLResponse)
async def food_analyze_recipe_portion_get(request: Request):
    with _db.get_db() as conn:
        recipes = [dict(r) for r in _db.recipe_list(conn)]
    return templates.TemplateResponse(request, "food_analyze_recipe_portion.html", {
        "recipes": recipes,
    })


@app.post("/food/analyze-recipe-portion", response_class=HTMLResponse)
async def food_analyze_recipe_portion_post(
    request: Request,
    recipe_id: int = Form(...),
    servings: float = Form(1.0),
):
    with _db.get_db() as conn:
        recipes = [dict(r) for r in _db.recipe_list(conn)]
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return templates.TemplateResponse(request, "food_analyze_recipe_portion.html", {
                "recipes": recipes,
                "error": f"Recipe {recipe_id} not found.",
            })
        per_serving = _recipe_nutrients_per_serving(recipe_id, conn)
        recipe_servings = float(recipe["servings"] or 1)

        all_ings = _db.recipe_get_ingredients(conn, recipe_id)
        display_ingredients = []
        diaas_ingredients = []
        for ing in all_ings:
            if ing["ref_recipe_id"]:
                n = ing["amount"]
                amt_str = f"{n:g} serving{'s' if n != 1 else ''}"
            else:
                amt_str = ing["unit"] or f"{ing['amount']:g} g"
            display_ingredients.append({
                "food_name":      ing["food_name"],
                "amount_str":     amt_str,
                "notes":          ing["notes"] or "",
                "fdc_id":         ing["fdc_id"],
                "ref_recipe_id":  ing["ref_recipe_id"],
            })
            if not ing["fdc_id"]:
                continue
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                continue
            diaas_ingredients.append({
                "food_name":      ing["food_name"],
                "nutrients_100g": json.loads(cached["nutrients_json"]),
                "grams":          float(ing["amount"]) / recipe_servings * servings,
                "fdc_id":         ing["fdc_id"],
            })

        diaas_result = None
        if diaas_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(diaas_ingredients, conn)
            except Exception:
                pass

    factor = servings  # per_serving already divides by recipe_servings
    scaled = {k: v * factor for k, v in per_serving.items()}
    rda = _load_rda()
    optimal = _load_optimal()
    max_limits = _load_max_limits()
    diaas_display = _build_diaas_display(diaas_result)

    return templates.TemplateResponse(request, "food_analyze_recipe_portion.html", {
        "recipes":            recipes,
        "selected_recipe":    dict(recipe),
        "servings_input":     servings,
        "analysis": {
            "recipe_name":       recipe["name"],
            "servings_analyzed": servings,
            "serving_size":      recipe["serving_size"],
        },
        "ingredients":        display_ingredients,
        "nutrient_sections":  _nutrient_sections(scaled, rda, optimal=optimal, max_limits=max_limits,
                                                 dcp_g=diaas_display["dcp_g"] if diaas_display else None,
                                                 dcp_missing=diaas_display["missing"] if diaas_display else None),
        "diaas_display":      diaas_display,
        "dcp_missing_names":  diaas_display["missing"] if diaas_display else [],
        "has_profile":        rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
        "protein_adequacy":   _protein_adequacy(scaled, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":        _complement_suggestions(scaled, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="recipe", exclude_recipe_id=recipe_id, ingredients=diaas_ingredients),
        "gl":                 _recipe_gl_web(recipe_id, recipe_servings, servings),
    })


@app.get("/food/convert", response_class=HTMLResponse)
async def food_convert_get(request: Request, q: str = "", source: list[str] | None = Query(default=None),
                            limit: int | None = None):
    search_results = []
    search_error = None
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    if q:
        q = q.strip()
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, q)
            pantry_ids = _pantry_fdc_ids(conn)
        seen: set[int] = set()
        for row in cached:
            seen.add(row["fdc_id"])
            search_results.append({
                "fdc_id":      row["fdc_id"],
                "name":        row["name"],
                "data_type":   row["data_type"],
                "brand":       row["brand"] or "",
                "source":      "pantry" if row["fdc_id"] in pantry_ids else "cache",
                "convert_url": f"/food/convert/{row['fdc_id']}",
            })
        try:
            for food in _usda.search_foods(q, page_size=limit):
                fid = food.get("fdcId")
                if fid and fid not in seen:
                    seen.add(fid)
                    search_results.append({
                        "fdc_id":      fid,
                        "name":        food.get("description", ""),
                        "data_type":   food.get("dataType", ""),
                        "brand":       food.get("brandOwner") or food.get("brandName") or "",
                        "source":      "usda",
                        "convert_url": f"/food/convert/{fid}",
                    })
        except Exception as exc:
            if not search_results:
                search_error = f"USDA API unavailable: {exc}"
        # Also search local recipes by name
        ql = q.lower()
        with _db.get_db() as conn:
            all_recipes = _db.recipe_list_recent(conn, limit=200)
        for r in all_recipes:
            if ql in r["name"].lower():
                search_results.append({
                    "fdc_id":      None,
                    "name":        r["name"],
                    "data_type":   f"{r['servings']} serving{'s' if r['servings'] != 1 else ''}",
                    "brand":       "",
                    "source":      "recipe",
                    "convert_url": f"/food/convert/recipe/{r['id']}",
                })
        search_results = _sort_search_results(search_results, q, _resolve_sort(None, "sort_food_search", "relevance", _SEARCH_SORT_MODES))
        search_results = _cap_results_preserving_local(_filter_search_results_by_source(search_results, source), limit)
    return templates.TemplateResponse(request, "food_convert.html", {
        "query":          q,
        "search_results": search_results,
        "search_error":   search_error,
        "source":         source,
        "limit":          limit,
        "source_filters": _SEARCH_SOURCE_FILTERS,
        "source_labels":  _SEARCH_SOURCE_LABELS,
    })


@app.get("/food/convert/{fdc_id}", response_class=HTMLResponse)
async def food_convert_detail(
    request: Request,
    fdc_id: int,
    portion_str: str = Query(default=""),
):
    food_data: dict = {}
    portions: list = []

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)

    if cached:
        portions = json.loads(cached["portions_json"] or "[]") or []
        food_data = {"fdc_id": cached["fdc_id"], "name": cached["name"], "brand": cached["brand"] or ""}
    else:
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception as exc:
            return templates.TemplateResponse(request, "food_convert.html", {
                "search_error": f"Could not load food {fdc_id}: {exc}",
            })
        portions = detail.get("portions", [])
        food_data = {"fdc_id": fdc_id, "name": detail["name"], "brand": detail.get("brand") or ""}
        with _db.get_db() as conn:
            _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                           data_type=detail.get("dataType", ""), brand=detail.get("brand"),
                           serving_size=detail.get("servingSize"),
                           serving_unit=detail.get("servingUnit"),
                           nutrients=detail.get("nutrients", {}), portions=portions)
            _recipe_dcp.cascade_food_change(detail["fdcId"], conn)

    density = _usda.get_density_g_per_ml(food_data["name"], portions)

    # Parse the free-form portion string → grams
    convert_grams: float | None = None
    convert_label: str | None = None
    convert_error: str | None = None
    convert_volume: float | None = None
    closest_portion = None

    if portion_str.strip():
        parsed_g, parsed_label = _parse_portion_str(portion_str.strip(), portions, food_data["name"])
        if parsed_g is None:
            convert_error = parsed_label
        else:
            convert_grams = parsed_g
            convert_label = parsed_label
            if density and convert_grams:
                convert_volume = round(convert_grams / density, 1)
            if convert_grams and portions:
                closest_portion = min(
                    portions, key=lambda p: abs(float(p.get("gram_weight", 0)) - convert_grams)
                )

    return templates.TemplateResponse(request, "food_convert.html", {
        "food":             food_data,
        "portions":         portions,
        "density":          density,
        "portion_str":      portion_str.strip(),
        "convert_grams":    convert_grams,
        "convert_label":    convert_label,
        "convert_error":    convert_error,
        "convert_volume":   convert_volume,
        "closest_portion":  closest_portion,
        "convert_url":      f"/food/convert/{fdc_id}",
    })


@app.get("/food/convert/recipe/{recipe_id}", response_class=HTMLResponse)
async def food_convert_recipe(
    request: Request,
    recipe_id: int,
    portion_str: str = Query(default=""),
):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return RedirectResponse("/food/convert", status_code=303)

    servings = float(recipe["servings"] or 1)
    total_weight = float(recipe["total_weight"]) if recipe["total_weight"] else None
    total_volume = float(recipe["total_volume"]) if recipe["total_volume"] else None
    vol_unit = (recipe["total_volume_unit"] or "").lower()

    # Build named portions from total_weight / servings
    portions: list[dict] = []
    if total_weight and servings > 0:
        serving_label = f"1 serving ({recipe['serving_size']})" if recipe["serving_size"] else "1 serving"
        portions = [{"description": serving_label, "gram_weight": round(total_weight / servings, 1)}]

    density: float | None = None
    if total_weight and total_volume and vol_unit in ("ml", "mL") and total_volume > 0:
        density = round(total_weight / total_volume, 3)

    food_data = {"name": recipe["name"], "brand": f"{servings:g}-serving recipe"}

    convert_grams: float | None = None
    convert_label: str | None = None
    convert_error: str | None = None
    convert_volume: float | None = None
    closest_portion = None

    if portion_str.strip():
        parsed_g, parsed_label = _parse_portion_str(portion_str.strip(), portions, recipe["name"])
        if parsed_g is None:
            convert_error = parsed_label
        else:
            convert_grams = parsed_g
            convert_label = parsed_label
            if density and convert_grams:
                convert_volume = round(convert_grams / density, 1)
            if convert_grams and portions:
                closest_portion = min(
                    portions, key=lambda p: abs(float(p.get("gram_weight", 0)) - convert_grams)
                )

    return templates.TemplateResponse(request, "food_convert.html", {
        "food":             food_data,
        "portions":         portions,
        "density":          density,
        "portion_str":      portion_str.strip(),
        "convert_grams":    convert_grams,
        "convert_label":    convert_label,
        "convert_error":    convert_error,
        "convert_volume":   convert_volume,
        "closest_portion":  closest_portion,
        "convert_url":      f"/food/convert/recipe/{recipe_id}",
    })


# ---------------------------------------------------------------------------
# Edit-form nutrient groups (key, label, unit) for custom profile editing
# ---------------------------------------------------------------------------

_EDIT_NUTRIENT_GROUPS: list[tuple[str, list[tuple[str, str, str]]]] = [
    ("Macronutrients", [
        ("calories",        "Calories",             "kcal"),
        ("protein_g",       "Protein",              "g"),
        ("carbs_g",         "Carbohydrate",         "g"),
        ("fat_g",           "Total Fat",            "g"),
        ("fiber_g",         "Fiber",                "g"),
        ("sugar_g",         "Sugars",               "g"),
        ("saturated_fat_g", "Saturated Fat",        "g"),
        ("mono_fat_g",      "Monounsaturated Fat",  "g"),
        ("poly_fat_g",      "Polyunsaturated Fat",  "g"),
    ]),
    ("Omega Fatty Acids", [
        ("omega3_ala_mg", "ALA (omega-3)",      "mg"),
        ("omega3_epa_mg", "EPA (omega-3)",      "mg"),
        ("omega3_dha_mg", "DHA (omega-3)",      "mg"),
        ("omega6_la_mg",  "Linoleic (omega-6)", "mg"),
    ]),
    ("Minerals", [
        ("calcium_mg",    "Calcium",    "mg"),
        ("iron_mg",       "Iron",       "mg"),
        ("magnesium_mg",  "Magnesium",  "mg"),
        ("phosphorus_mg", "Phosphorus", "mg"),
        ("potassium_mg",  "Potassium",  "mg"),
        ("sodium_mg",     "Sodium",     "mg"),
        ("zinc_mg",       "Zinc",       "mg"),
        ("iodine_mcg",    "Iodine",     "mcg"),
        ("selenium_mcg",  "Selenium",   "mcg"),
    ]),
    ("Vitamins", [
        ("vitamin_a_mcg",  "Vitamin A",       "mcg RAE"),
        ("vitamin_c_mg",   "Vitamin C",       "mg"),
        ("vitamin_d_mcg",  "Vitamin D",       "mcg"),
        ("vitamin_e_mg",   "Vitamin E",       "mg"),
        ("vitamin_k_mcg",  "Vitamin K",       "mcg"),
        ("thiamin_mg",     "Thiamin (B1)",    "mg"),
        ("riboflavin_mg",  "Riboflavin (B2)", "mg"),
        ("niacin_mg",      "Niacin (B3)",     "mg"),
        ("b6_mg",          "Vitamin B6",      "mg"),
        ("folate_mcg",     "Folate (B9)",     "mcg"),
        ("b12_mcg",        "Vitamin B12",     "mcg"),
    ]),
    ("Phytonutrients", [
        ("beta_carotene_mcg",      "Beta-carotene",     "mcg"),
        ("alpha_carotene_mcg",     "Alpha-carotene",    "mcg"),
        ("lycopene_mcg",           "Lycopene",          "mcg"),
        ("lutein_zeaxanthin_mcg",  "Lutein+Zeaxanthin", "mcg"),
        ("choline_mg",             "Choline",           "mg"),
        ("beta_sitosterol_mg",     "Beta-sitosterol",   "mg"),
        ("isoflavones_mg",         "Isoflavones",       "mg"),
    ]),
    ("Amino Acids", [
        ("aa_tryptophan_g",    "Tryptophan",    "g"),
        ("aa_threonine_g",     "Threonine",     "g"),
        ("aa_isoleucine_g",    "Isoleucine",    "g"),
        ("aa_leucine_g",       "Leucine",       "g"),
        ("aa_lysine_g",        "Lysine",        "g"),
        ("aa_methionine_g",    "Methionine",    "g"),
        ("aa_cystine_g",       "Cystine",       "g"),
        ("aa_phenylalanine_g", "Phenylalanine", "g"),
        ("aa_tyrosine_g",      "Tyrosine",      "g"),
        ("aa_valine_g",        "Valine",        "g"),
        ("aa_histidine_g",     "Histidine",     "g"),
    ]),
]

_ALL_NUTRIENT_KEYS: set[str] = {k for _, fields in _EDIT_NUTRIENT_GROUPS for k, _, _ in fields}


# Compare helpers
# ---------------------------------------------------------------------------

# Single source of truth: usda_nutrients.COMPARE_GROUPS
_COMPARE_GROUPS = _usda.COMPARE_GROUPS


def _build_compare_groups(entries: list[dict]) -> list[dict]:
    """Build comparison group rows from a list of {name, nutrients} dicts —
    `nutrients` is always per 100g of the item (see _load_compare_entry)."""
    groups = []
    for group_name, keys in _COMPARE_GROUPS:
        rows = []
        for key in keys:
            label, unit = _usda.nutrient_label(key)
            values = [round(e["nutrients"].get(key) or 0, 3) for e in entries]
            max_val = max(values) if any(v > 0 for v in values) else None
            cells = [
                {"value": v if v > 0 else None, "is_max": (max_val is not None and v == max_val and v > 0)}
                for v in values
            ]
            if any(c["value"] is not None for c in cells):
                rows.append({"label": label, "unit": unit, "cells": cells})
        if rows:
            groups.append({"name": group_name, "rows": rows})
    return groups


_FOOD_CACHE_SORT_KEYS = {
    "name":  lambda f: (f["name"] or "").lower(),
    "id":    lambda f: _code_sort_key((_classify_food_id(f["fdc_id"]) or ("",))[0]),
    "type":  lambda f: ((f["data_type"] or "").lower(), (f["name"] or "").lower()),
    "diaas": lambda f: (f["diaas"] is None, -(f["diaas"] or 0), (f["name"] or "").lower()),
    "gi":    lambda f: (f["gi"] is None, -(f["gi"] or 0), (f["name"] or "").lower()),
}


@app.get("/food/cache", response_class=HTMLResponse)
async def food_cache_get(request: Request, q: str = "", pruned: int = 0, sort: str | None = None,
                          show_archived: bool | None = None, archived: int = 0, restored: int = 0,
                          still_used: int = 0, imported: int = 0, delete_blocked: int = 0,
                          blocked_fdc_id: int | None = None,
                          blocked_pantry: str = "", blocked_recipes: str = "", blocked_meals: str = "",
                          impact: str = ""):
    sort = _resolve_sort(sort, "sort_food_cache", "name", set(_FOOD_CACHE_SORT_KEYS))
    show_archived = _resolve_bool_pref(show_archived, "show_archived_food_cache")
    with _db.get_db() as conn:
        if q.strip():
            rows = _db.search_cached_foods(conn, q.strip(), include_archived=show_archived)
        else:
            rows = _db.list_cached_foods(conn, include_archived=show_archived)
        fdc_ids = [r["fdc_id"] for r in rows]
        annotations = _db.annotations_for_fdcids(conn, fdc_ids) if fdc_ids else {}
        pantry_fdc_ids = {r["fdc_id"] for r in _db.pantry_list(conn, include_archived=True)}

    foods = []
    for row in rows:
        ann = annotations.get(row["fdc_id"])
        nuts = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
        has_aa = _usda.has_confirmed_aa_data(nuts)
        # A saved annotation always takes priority over the keyword-matched
        # reference table (see README "Per-food DIAAS via annotations").
        diaas_saved = ann["diaas_estimate"] if ann else None
        diaas = diaas_saved if diaas_saved is not None else (_usda.get_diaas(row["name"]) if has_aa else None)
        foods.append({
            "fdc_id":         row["fdc_id"],
            "name":           row["name"],
            "data_type":      row["data_type"] or "",
            "brand":          row["brand"] or "",
            "has_aa":         has_aa,
            "gi":             ann["gi_estimate"] if ann else None,
            "gi_source":      _ann_source(ann),
            "diaas":          diaas,
            "diaas_saved":    diaas_saved is not None,
            "notes":          row["notes"] or "",
            "curator_notes":  row["curator_notes"] or "" if "curator_notes" in row.keys() else "",
            "archived":       bool(row["archived"]),
            "in_pantry":      row["fdc_id"] in pantry_fdc_ids,
        })
    foods.sort(key=_FOOD_CACHE_SORT_KEYS[sort])
    return templates.TemplateResponse(request, "food_cache.html", {
        "foods":         foods,
        "q":             q,
        "pruned":        pruned,
        "sort":          sort,
        "show_archived": show_archived,
        "archived":      archived,
        "restored":      restored,
        "still_used":    still_used,
        "imported":      imported,
        "impact":        _impact_pop(impact),
        "delete_blocked": delete_blocked,
        "blocked_fdc_id":  blocked_fdc_id,
        "blocked_pantry":  [int(i) for i in blocked_pantry.split(",") if i],
        "blocked_recipes": [int(i) for i in blocked_recipes.split(",") if i],
        "blocked_meals":   [int(i) for i in blocked_meals.split(",") if i],
    })


@app.get("/food/cache/export.csv")
async def food_cache_export_csv(q: str = "", show_archived: bool | None = None):
    show_archived = _resolve_bool_pref(show_archived, "show_archived_food_cache")
    with _db.get_db() as conn:
        if q.strip():
            rows = _db.search_cached_foods(conn, q.strip(), include_archived=show_archived)
        else:
            rows = _db.list_cached_foods(conn, include_archived=show_archived)
    csv_text = _csv_export.foods_to_csv(rows)
    filename = f"numa_food_cache_{datetime.date.today().isoformat()}.csv"
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/food/cache/delete", response_class=RedirectResponse)
async def food_cache_delete(request: Request, fdc_id: int = Form(...), q: str = Form(""),
                             sort: str = Form(""), show_archived: int = Form(0)):
    """Delete a cached food — refused if a pantry entry, recipe, or meal still
    references it, since that would silently orphan the reference (it would
    keep pointing at an fdc_id with no data behind it, breaking that food's
    page). Use Archive instead to hide a still-referenced food."""
    params = {"q": q, "sort": sort, "show_archived": show_archived}
    ajax = _is_ajax_row_action(request)
    with _db.get_db() as conn:
        refs = _db.food_references(conn, fdc_id)
        if refs["pantry"] or refs["recipes"] or refs["meals"]:
            if ajax:
                # Blocked deletes need the full explanation page (which
                # pantry entry/recipe/meal is holding it) — not worth
                # reproducing that markup client-side, so fall back to a
                # normal navigation for this one case.
                return JSONResponse({"ok": False})
            params["delete_blocked"] = 1
            params["blocked_fdc_id"] = fdc_id
            if refs["pantry"]:
                params["blocked_pantry"] = ",".join(str(i) for i in refs["pantry"])
            if refs["recipes"]:
                params["blocked_recipes"] = ",".join(str(i) for i in refs["recipes"])
            if refs["meals"]:
                params["blocked_meals"] = ",".join(str(i) for i in refs["meals"])
            return RedirectResponse(f"/food/cache?{urlencode(params)}", status_code=303)
        _db.delete_cached_food(conn, fdc_id)
    if ajax:
        return JSONResponse({"ok": True})
    return RedirectResponse(f"/food/cache?{urlencode(params)}", status_code=303)


# ---------------------------------------------------------------------------
# Claude AI amino-acid/nutrient fetch workflow — see numa_app/services/
# claude_fetch.py for the prompt-building and response-parsing logic.
# ---------------------------------------------------------------------------

@app.post("/food/cache/claude-fetch", response_class=HTMLResponse)
async def food_cache_claude_fetch(request: Request, fdc_id: list[int] = Form(default=[]),
                                  group: list[str] = Form(default=[]),
                                  want: list[str] = Form(default=[])):
    """Build a prompt asking only for each selected food's missing nutrient
    groups (data_completeness.py), less any the user marked not needed for
    that food. `group` limits it to those groups; `want` ("fdc_id:group",
    the Data Completeness page's per-gap checkboxes) picks exact food/group
    pairs instead. A food with nothing missing is left out."""
    checked = set(group) or None
    wanted: dict[int, set[str]] = {}
    for cell in want:
        fid, _, g = cell.partition(":")
        if g in _data_completeness.GROUP_LABELS and fid.lstrip("-").isdigit():
            wanted.setdefault(int(fid), set()).add(g)
    fdc_id = list(dict.fromkeys(fdc_id + list(wanted)))
    selected, requests, nothing_missing = [], {}, []
    with _db.get_db() as conn:
        ignores = _db.food_data_ignores(conn)
        for fid in fdc_id:
            cached = _db.get_cached_food(conn, fid)
            if not cached:
                continue
            nutrients = json.loads(cached["nutrients_json"] or "{}")
            ignored = ignores.get(fid, set())
            gaps = _data_completeness.active_gaps(nutrients, ignored, wanted.get(fid, checked))
            keys = _data_completeness.requested_keys(nutrients, gaps)
            if not keys:
                nothing_missing.append(cached["name"])
                continue
            selected.append((fid, cached["name"]))
            requests[fid] = (keys, [_data_completeness.GROUP_LABELS[g]
                                    for g in _data_completeness.missing_groups(nutrients)
                                    if g in ignored])
    prompt = _claude_fetch.build_prompt(selected, requests) if selected else ""
    return templates.TemplateResponse(request, "claude_fetch.html", {
        "prompt":          prompt,
        "selected":        selected,
        "nothing_missing": nothing_missing,
        "group_labels":    {fid: [_data_completeness.GROUP_LABELS[g] for g in
                                  _data_completeness.groups_for_keys(keys)]
                            for fid, (keys, _) in requests.items()},
    })


@app.get("/food/cache/claude-import", response_class=HTMLResponse)
async def food_cache_claude_import_get(request: Request):
    return templates.TemplateResponse(request, "claude_import.html", {
        "response_text": "",
        "review":        None,
    })


@app.post("/food/cache/claude-import", response_class=HTMLResponse)
async def food_cache_claude_import_post(request: Request,
                                         response_text: str = Form(...),
                                         action: str = Form("preview"),
                                         overwrite: int = Form(0)):
    raw_blocks, curator_text, parse_warnings = _claude_fetch.parse_response(response_text)
    valid, validate_warnings = _claude_fetch.validate_all(raw_blocks)
    warnings = parse_warnings + validate_warnings

    if action == "confirm" and valid:
        targets = _impact_targets([f["fdc_id"] for f in valid])
        before = _impact_snapshot(*targets)
        with _db.get_db() as conn:
            _claude_fetch.import_foods(conn, valid, curator_text, overwrite=bool(overwrite))
            # An import changes an existing food's nutrients in place, so
            # every recipe using it needs its DCP recomputed — a food that
            # just gained amino acid data can turn an NC recipe computable.
            for _f in valid:
                _recipe_dcp.cascade_food_change(_f["fdc_id"], conn)
        token = _impact_store("Importing Claude AI's data",
                              before, _impact_snapshot(*targets))
        return RedirectResponse("/food/cache?imported=" + str(len(valid)) + (f"&impact={token}" if token else ""),
                                status_code=303)

    with _db.get_db() as conn:
        plans = _claude_fetch.plan_import(conn, valid)
    review_rows = []
    for f, plan in zip(valid, plans):
        n = f["nutrients"]
        review_rows.append({
            "name":      f["name"],
            "fdc_id":    f["fdc_id"],
            "calories":  int(n["calories"]) if "calories" in n else None,
            "protein_g": round(n["protein_g"], 1) if "protein_g" in n else None,
            "aa_count":  sum(1 for k in _claude_fetch.AA_KEYS if k in n),
            "existing":  plan["existing"],
            "add_n":     len(plan["add"]),
            "keep":      plan["keep"],
        })
    return templates.TemplateResponse(request, "claude_import.html", {
        "response_text": response_text,
        "review":        review_rows,
        "any_keep":      any(r["keep"] for r in review_rows),
        "warnings":      warnings,
        "curator_text":  curator_text,
        "no_blocks":     not raw_blocks,
    })


# ---------------------------------------------------------------------------
# CSV import workflow — see numa_app/services/csv_import.py for parsing;
# csv_export.py (same directory) produces the matching export format.
# ---------------------------------------------------------------------------

@app.get("/food/cache/import-csv", response_class=HTMLResponse)
async def food_cache_import_csv_get(request: Request):
    return templates.TemplateResponse(request, "food_cache_import_csv.html", {
        "csv_text": "",
        "review":   None,
    })


@app.post("/food/cache/import-csv", response_class=HTMLResponse)
async def food_cache_import_csv_post(request: Request,
                                      action: str = Form("preview"),
                                      csv_text: str = Form(""),
                                      csv_file: UploadFile | None = File(None)):
    if csv_file is not None and csv_file.filename:
        raw_bytes = await csv_file.read()
        csv_text = raw_bytes.decode("utf-8-sig", errors="replace")

    valid, warnings = _csv_import.parse_foods_csv(csv_text)

    if action == "confirm" and valid:
        with _db.get_db() as conn:
            new_ids = _csv_import.import_foods(conn, valid)
        return RedirectResponse("/food/cache?imported=" + str(len(new_ids)), status_code=303)

    with _db.get_db() as conn:
        existing_names = {r["name"].strip().lower() for r in _db.list_cached_foods(conn, include_archived=True)}

    review_rows = []
    for f in valid:
        n = f["nutrients"]
        review_rows.append({
            "name":          f["name"],
            "calories":      int(n.get("calories", 0)),
            "protein_g":     round(n.get("protein_g", 0), 1),
            "portion_count": len(f["portions"]),
            "duplicate":     f["name"].strip().lower() in existing_names,
        })
    return templates.TemplateResponse(request, "food_cache_import_csv.html", {
        "csv_text": csv_text,
        "review":   review_rows,
        "warnings": warnings,
    })


@app.post("/food/cache/{fdc_id}/archive", response_class=RedirectResponse)
async def food_cache_archive(request: Request, fdc_id: int, q: str = Form(""), sort: str = Form(""),
                              show_archived: int = Form(0)):
    """Archive or restore a cached food — flips whichever state it's currently in."""
    params = {"q": q, "sort": sort, "show_archived": show_archived}
    ajax = _is_ajax_row_action(request)
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        if not cached:
            if ajax:
                return JSONResponse({"ok": False})
            return RedirectResponse(f"/food/cache?{urlencode(params)}", status_code=303)
        newly_archived = not cached["archived"]
        still_used = 0
        if newly_archived:
            refs = _db.food_references(conn, fdc_id)
            still_used = int(bool(refs["pantry"] or refs["recipes"] or refs["meals"]))
        _db.set_food_archived(conn, fdc_id, newly_archived)
    if ajax:
        return JSONResponse({"ok": True, "archived": newly_archived, "still_used": bool(still_used)})
    params["archived" if newly_archived else "restored"] = 1
    if newly_archived and still_used:
        params["still_used"] = 1
    return RedirectResponse(f"/food/cache?{urlencode(params)}", status_code=303)


@app.get("/food/cache/prune", response_class=HTMLResponse)
async def food_cache_prune_get(request: Request):
    """Preview foods not referenced by any pantry entry, recipe, or meal before pruning."""
    with _db.get_db() as conn:
        unused = _db.list_unused_cached_foods(conn)
    return templates.TemplateResponse(request, "food_cache_prune.html", {
        "unused": unused,
    })


@app.post("/food/cache/prune", response_class=RedirectResponse)
async def food_cache_prune_post(request: Request):
    """Delete unused cache foods, except any the user unchecked on the preview
    page — `delete_ids` carries only the checked (still-checked) rows."""
    form = await request.form()
    delete_ids = {int(v) for v in form.getlist("delete_ids")}
    with _db.get_db() as conn:
        unused = _db.list_unused_cached_foods(conn)
        keep_ids = {row["fdc_id"] for row in unused if row["fdc_id"] not in delete_ids}
        deleted = _db.prune_unused_cached_foods(conn, keep_ids=keep_ids)
    return RedirectResponse(f"/food/cache?pruned={len(deleted)}", status_code=303)


@app.get("/food/cache/db-check", response_class=HTMLResponse)
async def food_cache_db_check_get(request: Request, repaired: int = 0, saved: int = 0, amounts_fixed: int = 0,
                                  amounts_kept: int = 0, amounts_unkept: int = 0,
                                  impact: str = "",
                                  check: list[str] | None = Query(default=None),
                                  show_ignored: bool | None = None):
    """Scan for referential-integrity problems (see db.check_db_integrity),
    then for cached foods missing whole nutrient groups (see
    numa_app/services/data_completeness.py). `check` picks which groups the
    completeness scan looks at; remembered like other list-view toggles."""
    show_ignored = _resolve_bool_pref(show_ignored, "data_check_show_ignored")
    if check is None:
        check = _load_prefs_file().get("data_check_groups", _data_completeness.DEFAULT_CHECKED)
    else:
        _save_prefs_file({"data_check_groups": check})
    checked = [g for g in _data_completeness.GROUP_KEYS if g in check]
    with _db.get_db() as conn:
        issues = _db.check_db_integrity(conn)
        ignores = _db.food_data_ignores(conn)
        foods = _db.list_cached_foods(conn)
    gap_rows = []
    for row in foods:
        try:
            nutrients = json.loads(row["nutrients_json"] or "{}")
        except (json.JSONDecodeError, TypeError):
            continue  # unreadable data is already reported in the bad_json list above
        if not isinstance(nutrients, dict):
            continue
        ignored = ignores.get(row["fdc_id"], set())
        missing = [g for g in _data_completeness.missing_groups(nutrients) if g in checked]
        active = [g for g in missing if g not in ignored]
        if active or (show_ignored and missing):
            gap_rows.append({"fdc_id": row["fdc_id"], "name": row["name"],
                             "missing": set(missing), "ignored": ignored & set(missing),
                             "active": bool(active)})
    gap_rows.sort(key=lambda r: r["name"].lower())
    with _db.get_db() as conn:
        quality = _data_quality.scan(conn)
        old_copies = _data_quality.old_usda_copies(conn)
        missing_aa = _data_quality.missing_aa_in_use(conn)
        missing_portions = _data_quality.missing_portions_in_use(conn)
        kept_amounts = [a for a in _data_quality.stale_amounts(conn, include_bracketed=True, include_kept=True)
                        if a["kept"]]
        generic_density = _data_quality.generic_density_in_use(conn)
    # Opening this page counts as reviewing every current problem: the Home
    # page reminder only raises ones that appear after this (_data_check_reminder()).
    _save_prefs_file({"data_check_seen": sorted(quality["keys"]),
                      "data_check_last_seen": datetime.date.today().isoformat()})
    total = sum(len(v) for v in issues.values())
    return templates.TemplateResponse(request, "food_cache_db_check.html", {
        "issues": issues,
        "total": total,
        "repairable": total - len(issues["bad_json"]),
        "repaired": repaired,
        "saved": saved,
        "groups": _data_completeness.GROUPS,
        "checked": checked,
        "show_ignored": show_ignored,
        "gap_rows": gap_rows,
        "active_gap_count": sum(1 for r in gap_rows if r["active"]),
        "food_issue_rows": quality["food_issues"],
        "food_problem_count": sum(1 for r in quality["food_issues"]
                                  if any(i["severity"] == "problem" for i in r["issues"])),
        "stale_amounts": quality["stale_amounts"],
        "old_copies": old_copies,
        "missing_aa": missing_aa,
        "missing_portions": missing_portions,
        "show_ignored_lists": show_ignored,
        "old_copy_days": _data_quality.OLD_COPY_DAYS,
        "amounts_fixed": amounts_fixed,
        "amounts_kept": amounts_kept,
        "amounts_unkept": amounts_unkept,
        "kept_amounts": kept_amounts,
        "generic_density": generic_density,
        "impact": _impact_pop(impact),
    })



@app.post("/food/cache/db-check/completeness", response_class=RedirectResponse)
async def food_cache_completeness_save(shown: list[str] = Form(default=[]),
                                       ignore: list[str] = Form(default=[]),
                                       back: str = Form("completeness")):
    """Save the Data Completeness table's "not needed" checkboxes. `shown`
    is every "fdc_id:group" cell the page displayed, so unchecking one
    removes its ignore; cells not on the page are left alone."""
    wanted = set(ignore)
    with _db.get_db() as conn:
        for cell in shown:
            fid, _, group = cell.partition(":")
            if ((group in _data_completeness.GROUP_LABELS or group == _data_quality.PORTIONS_IGNORE_KEY)
                    and fid.lstrip("-").isdigit()):
                _db.set_food_data_ignore(conn, int(fid), group, cell in wanted)
    anchor = back if back in ("completeness", "missing-aa", "missing-portions") else "completeness"
    return RedirectResponse(f"/food/cache/db-check?saved=1#{anchor}", status_code=303)


@app.post("/food/cache/db-check/stale-amounts", response_class=RedirectResponse)
async def food_cache_fix_stale_amounts(item: list[str] = Form(default=[]),
                                       portions_fdc_id: int | None = Form(default=None),
                                       action: str = Form(default="update")):
    """Set the ticked recipe ingredients / logged meal foods to the grams
    their typed volume or portion works out to now (data_quality.stale_amounts()),
    keeping what was typed — minus a bracketed gram figure ("1/3 c (42 gr)"),
    which would no longer be right. Recipes are recomputed (and their
    ancestors and meals flagged); meals are flagged stale and the reason
    logged. portions_fdc_id: sent from that food's Portions page, which this
    returns to instead of the Database check page.

    action="keep" instead records the ticked amounts as "Keep as entered"
    (db.amount_keep), so they stop being listed while their grams stay as
    they are; action="unkeep" removes that choice for the ticked ones."""
    wanted = set(item)
    if portions_fdc_id is not None:
        back = f"/food/cache/{portions_fdc_id}/portions"
    else:
        back = "/food/cache/db-check"
    if action in ("keep", "unkeep"):
        with _db.get_db() as conn:
            rows = [a for a in _data_quality.stale_amounts(conn, fdc_id=portions_fdc_id, include_bracketed=True,
                                                           include_kept=True)
                    if f"{a['where']}:{a['item_id']}" in wanted and a["kept"] == (action == "unkeep")]
            for a in rows:
                if action == "keep":
                    _db.amount_keep(conn, a["where"], a["item_id"], a["stored_g"])
                else:
                    _db.amount_unkeep(conn, a["where"], a["item_id"])
        param = "amounts_kept" if action == "keep" else "amounts_unkept"
        return RedirectResponse(f"{back}?{param}={len(rows)}#stale-amounts", status_code=303)
    with _db.get_db() as conn:
        stale = [a for a in _data_quality.stale_amounts(conn, fdc_id=portions_fdc_id, include_bracketed=True)
                 if f"{a['where']}:{a['item_id']}" in wanted]
        recipe_ids, meal_ids = set(), set()
        for a in stale:
            if a["where"] == "recipe":
                recipe_ids.update(_db.recipe_and_ancestors(conn, a["owner_id"]))
            else:
                meal_ids.add(a["owner_id"])
        meal_ids.update(_db.meals_using_recipes(conn, recipe_ids))
    if not stale:
        return RedirectResponse(f"{back}#stale-amounts", status_code=303)
    before = _impact_snapshot(sorted(recipe_ids), sorted(meal_ids))
    with _db.get_db() as conn:
        for a in stale:
            if a["where"] == "recipe":
                row = conn.execute("SELECT food_name, notes FROM recipe_ingredients WHERE id = ?",
                                   (a["item_id"],)).fetchone()
                if row:
                    _db.recipe_update_ingredient(conn, a["item_id"], a["now_g"], a["unit_after"],
                                                 row["food_name"], row["notes"])
            else:
                _db.meal_update_item(conn, a["item_id"], a["owner_id"], a["now_g"], a["unit_after"])
                _db.mark_meal_stale(conn, a["owner_id"])
                _db.log_meal_recalc(conn, [a["owner_id"]], f"{a['food_name']}: amount corrected")
        for rid in {a["owner_id"] for a in stale if a["where"] == "recipe"}:
            _recipe_dcp.recompute_recipe_dcp(rid, conn)
            _db.log_meal_recalc(conn, _db.meals_using_recipes(conn, _db.recipe_and_ancestors(conn, rid)),
                                "a recipe ingredient amount was corrected")
    after = _impact_snapshot(sorted(recipe_ids), sorted(meal_ids))
    token = _impact_store("Correcting " + (f"{len(stale)} amounts" if len(stale) != 1 else "that amount"),
                          before, after)
    return RedirectResponse(f"{back}?amounts_fixed={len(stale)}&impact={token}#stale-amounts",
                            status_code=303)


@app.get("/food/cache/duplicates", response_class=HTMLResponse)
async def food_cache_duplicates(request: Request, show_dismissed: int = 0, merged: int = 0,
                                dismissed: int = 0, impact: str = ""):
    """Duplicate foods (data_quality.duplicate_groups), run on request from
    Foods → 9: for each group keep one (the others are replaced by it
    everywhere and deleted) or mark the group "not duplicates"."""
    with _db.get_db() as conn:
        groups = _data_quality.duplicate_groups(conn, include_dismissed=bool(show_dismissed))
    return templates.TemplateResponse(request, "food_duplicates.html", {
        "groups": groups, "show_dismissed": bool(show_dismissed),
        "merged": merged, "dismissed": dismissed, "impact": _impact_pop(impact),
    })


@app.post("/food/cache/duplicates/keep", response_class=RedirectResponse)
async def food_cache_duplicates_keep(group_key: str = Form(...), keep: int = Form(...)):
    """Keep `keep`; every other food in the group is replaced by it in recipes,
    meals and pantry (db.merge_food_into) and deleted. The group must still
    match what the page showed, so a stale page can't merge the wrong foods."""
    with _db.get_db() as conn:
        group = next((g for g in _data_quality.duplicate_groups(conn, include_dismissed=True)
                      if g["key"] == group_key), None)
    ids = [f["fdc_id"] for f in group["foods"]] if group else []
    if keep not in ids:
        return RedirectResponse("/food/cache/duplicates", status_code=303)
    drop = [i for i in ids if i != keep]
    targets = _impact_targets(ids)
    before = _impact_snapshot(*targets)
    with _db.get_db() as conn:
        kept_name = _db.get_cached_food(conn, keep)["name"]
        for d in drop:
            _db.merge_food_into(conn, keep, d)
        _recipe_dcp.cascade_food_change(keep, conn)
        _db.log_meal_recalc(conn, _db.meals_using_food(conn, keep),
                            f"duplicates of {kept_name} merged into it")
    token = _impact_store(f"Merging duplicates into {kept_name}", before, _impact_snapshot(*targets))
    return RedirectResponse(f"/food/cache/duplicates?merged={len(drop)}" + (f"&impact={token}" if token else ""),
                            status_code=303)


@app.post("/food/cache/duplicates/dismiss", response_class=RedirectResponse)
async def food_cache_duplicates_dismiss(group_key: str = Form(...)):
    with _db.get_db() as conn:
        _db.dismiss_duplicate_group(conn, group_key)
    return RedirectResponse("/food/cache/duplicates?dismissed=1", status_code=303)


@app.post("/food/{fdc_id}/data-ignore", response_class=RedirectResponse)
async def food_data_ignore(fdc_id: int, group: str = Form(...), ignored: int = Form(1)):
    """Mark (or unmark) one nutrient group not needed for this food, from
    its own page. Also takes data_quality.CALORIES_OK_KEY, "these calories
    are right", from the food's data-problem note."""
    if group in _data_completeness.GROUP_LABELS or group == _data_quality.CALORIES_OK_KEY:
        with _db.get_db() as conn:
            if _db.get_cached_food(conn, fdc_id):
                _db.set_food_data_ignore(conn, fdc_id, group, bool(ignored))
    return RedirectResponse(f"/food/{fdc_id}", status_code=303)


@app.post("/food/cache/db-check/repair", response_class=RedirectResponse)
async def food_cache_db_check_repair(category: str = Form(default="")):
    """category: one of db.REPAIRABLE_ISSUE_CATEGORIES to fix just that kind
    of problem, or "" (the "Remove all" button) to fix every repairable kind
    at once."""
    categories = {category} if category else None
    with _db.get_db() as conn:
        counts = _db.repair_db_integrity(conn, categories=categories)
    return RedirectResponse(f"/food/cache/db-check?repaired={sum(counts.values())}", status_code=303)


def _portion_amounts_review(fdc_id: int) -> dict:
    """Template context for the Portions page's "Amounts that no longer
    match" panel: this food's recipe and meal amounts entered as a volume or
    portion whose stored grams differ from what they work out to with the
    portions as they are now. Shown after every portion change (and on a plain
    visit while any remain), so a corrected cup weight leads straight to the
    amounts it affects. Recipe rows start ticked; logged meals (a past
    record) and bracketed-weight rows (the figure may be one the user
    weighed) start unticked. Amounts the user kept as entered are listed
    separately, marked as such."""
    with _db.get_db() as conn:
        rows = _data_quality.stale_amounts(conn, fdc_id=fdc_id, include_bracketed=True, include_kept=True)
    for a in rows:
        a["ticked"] = a["where"] == "recipe" and not a["bracketed"]
    rows.sort(key=lambda a: (a["where"] != "recipe", a["bracketed"], a["owner_label"].lower()))
    return {"stale_amounts": [a for a in rows if not a["kept"]],
            "kept_amounts": [a for a in rows if a["kept"]]}


@app.get("/food/cache/{fdc_id}/portions", response_class=HTMLResponse)
async def food_cache_portions_get(request: Request, fdc_id: int, amounts_fixed: int = 0,
                                  amounts_kept: int = 0, amounts_unkept: int = 0,
                                  impact: str = ""):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        return RedirectResponse("/food/cache", status_code=303)
    portions = json.loads(cached["portions_json"] or "[]") or []
    return templates.TemplateResponse(request, "food_cache_portions.html", {
        "food":     {"fdc_id": cached["fdc_id"], "name": cached["name"]},
        "portions": portions,
        "saved":    False,
        "error":    None,
        "amounts_fixed": amounts_fixed,
        "amounts_kept": amounts_kept,
        "amounts_unkept": amounts_unkept,
        "impact":   _impact_pop(impact),
        **_portion_amounts_review(fdc_id),
    })


@app.post("/food/cache/{fdc_id}/portions/add", response_class=HTMLResponse)
async def food_cache_portions_add(
    request: Request,
    fdc_id: int,
    description: str = Form(...),
    gram_weight: str = Form(...),
):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        return RedirectResponse("/food/cache", status_code=303)
    portions = json.loads(cached["portions_json"] or "[]") or []
    error = None
    try:
        gw = float(gram_weight)
        if gw <= 0:
            raise ValueError
    except (ValueError, TypeError):
        error = "Gram weight must be a positive number."
    desc = description.strip()
    if not desc:
        error = "Description is required."
    if not error:
        portions.append({"description": desc, "gram_weight": round(gw, 2)})
        with _db.get_db() as conn:
            _db.update_food_portions(conn, fdc_id, portions)
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    portions = json.loads(cached["portions_json"] or "[]") or []
    return templates.TemplateResponse(request, "food_cache_portions.html", {
        "food":     {"fdc_id": fdc_id, "name": cached["name"]},
        "portions": portions,
        "saved":    not error,
        "error":    error,
        **_portion_amounts_review(fdc_id),
    })


@app.post("/food/cache/{fdc_id}/portions/edit", response_class=HTMLResponse)
async def food_cache_portions_edit(
    request: Request,
    fdc_id: int,
    portion_index: int = Form(...),
    description: str = Form(...),
    gram_weight: str = Form(...),
):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        return RedirectResponse("/food/cache", status_code=303)
    portions = json.loads(cached["portions_json"] or "[]") or []
    error = None
    gw = 0.0
    try:
        gw = float(gram_weight)
        if gw <= 0:
            raise ValueError
    except (ValueError, TypeError):
        error = "Gram weight must be a positive number."
    desc = description.strip()
    if not desc:
        error = "Description is required."
    if not error and not 0 <= portion_index < len(portions):
        error = "That portion no longer exists."
    if not error:
        portions[portion_index] = {**portions[portion_index], "description": desc,
                                   "gram_weight": round(gw, 2)}
        with _db.get_db() as conn:
            _db.update_food_portions(conn, fdc_id, portions)
    return templates.TemplateResponse(request, "food_cache_portions.html", {
        "food":          {"fdc_id": fdc_id, "name": cached["name"]},
        "portions":      portions,
        "saved":         not error,
        "flash_message": "Portion updated.",
        "error":         error,
        **_portion_amounts_review(fdc_id),
    })


@app.post("/food/cache/{fdc_id}/portions/delete", response_class=HTMLResponse)
async def food_cache_portions_delete(
    request: Request,
    fdc_id: int,
    portion_index: int = Form(...),
):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        return RedirectResponse("/food/cache", status_code=303)
    portions = json.loads(cached["portions_json"] or "[]") or []
    if 0 <= portion_index < len(portions):
        portions.pop(portion_index)
        with _db.get_db() as conn:
            _db.update_food_portions(conn, fdc_id, portions)
    return templates.TemplateResponse(request, "food_cache_portions.html", {
        "food":     {"fdc_id": fdc_id, "name": cached["name"]},
        "portions": portions,
        "saved":    False,
        "error":    None,
        **_portion_amounts_review(fdc_id),
    })


@app.post("/food/cache/{fdc_id}/portions/move", response_class=HTMLResponse)
async def food_cache_portions_move(
    request: Request,
    fdc_id: int,
    portion_index: int = Form(...),
    direction: str = Form(...),
):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        return RedirectResponse("/food/cache", status_code=303)
    portions = json.loads(cached["portions_json"] or "[]") or []
    swap_with = portion_index - 1 if direction == "up" else portion_index + 1
    moved = 0 <= portion_index < len(portions) and 0 <= swap_with < len(portions)
    if moved:
        portions[portion_index], portions[swap_with] = portions[swap_with], portions[portion_index]
        with _db.get_db() as conn:
            _db.update_food_portions(conn, fdc_id, portions)
    return templates.TemplateResponse(request, "food_cache_portions.html", {
        "food":          {"fdc_id": fdc_id, "name": cached["name"]},
        "portions":      portions,
        "saved":         moved,
        "flash_message": "Portion order updated.",
        "error":         None,
        **_portion_amounts_review(fdc_id),
    })


@app.post("/food/cache/{fdc_id}/refresh", response_class=HTMLResponse)
async def food_cache_refresh(request: Request, fdc_id: int):
    """Re-fetch nutrients from USDA and replace all cached nutrient data."""
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        return RedirectResponse("/food/cache", status_code=303)
    if fdc_id < 0:
        return RedirectResponse(f"/food/cache?error=off_no_refresh", status_code=303)
    error = None
    try:
        detail = _usda.get_food_detail(fdc_id)
        new_nutrients = detail.get("nutrients", {})
        new_portions = detail.get("portions") or json.loads(cached["portions_json"] or "[]")
        with _db.get_db() as conn:
            _db.update_cached_food_profile(
                conn, fdc_id,
                name=detail.get("name") or cached["name"],
                nutrients=new_nutrients,
                data_type=detail.get("dataType") or cached["data_type"],
                brand=detail.get("brand") or cached["brand"],
                serving_size=detail.get("servingSize") or cached["serving_size"],
                serving_unit=detail.get("servingUnit") or cached["serving_unit"],
                portions=new_portions,
                notes=cached["notes"],
                user_drafted=False,
            )
            _recipe_dcp.cascade_food_change(fdc_id, conn)
    except Exception as exc:
        error = str(exc)
    if error:
        with _db.get_db() as conn:
            rows = _db.list_cached_foods(conn)
            fdc_ids = [r["fdc_id"] for r in rows]
            annotations = _db.annotations_for_fdcids(conn, fdc_ids) if fdc_ids else {}
        foods = []
        for row in rows:
            ann = annotations.get(row["fdc_id"])
            nuts = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
            foods.append({
                "fdc_id":        row["fdc_id"],
                "name":          row["name"],
                "data_type":     row["data_type"] or "",
                "brand":         row["brand"] or "",
                "has_aa":        _usda.has_confirmed_aa_data(nuts),
                "gi":            ann["gi_estimate"] if ann else None,
                "gi_source":     _ann_source(ann),
                "diaas":         ann["diaas_estimate"] if ann else None,
                "notes":         row["notes"] or "",
                "curator_notes": row["curator_notes"] or "" if "curator_notes" in row.keys() else "",
                "archived":      bool(row["archived"]),
            })
        return templates.TemplateResponse(request, "food_cache.html", {
            "foods":         foods,
            "q":             "",
            "sort":          "name",
            "show_archived": False,
            "refresh_error": f"Refresh failed for FDC {fdc_id}: {error}",
        })
    return RedirectResponse(f"/food/{fdc_id}?refreshed=1", status_code=303)


@app.get("/pantry", response_class=HTMLResponse)
async def pantry_get(request: Request, added: str = "", linked: str = "",
                      search: str = "", link_id: int = 0,
                      show_archived: bool | None = None, archived: int = 0, restored: int = 0,
                      source: list[str] | None = Query(default=None), limit: int | None = None):
    show_archived = _resolve_bool_pref(show_archived, "show_archived_pantry")
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    with _db.get_db() as conn:
        rows = _db.pantry_list(conn, include_archived=show_archived)
        fdc_ids = [r["fdc_id"] for r in rows if r["fdc_id"]]
        annotations = _db.annotations_for_fdcids(conn, fdc_ids) if fdc_ids else {}
        items = []
        for r in rows:
            item = dict(r)
            cached = _db.get_cached_food(conn, r["fdc_id"]) if r["fdc_id"] else None
            nuts = json.loads(cached["nutrients_json"]) if cached and cached["nutrients_json"] else {}
            has_aa = _usda.has_confirmed_aa_data(nuts)
            ann = annotations.get(r["fdc_id"])
            diaas_saved = ann["diaas_estimate"] if ann else None
            diaas = diaas_saved if diaas_saved is not None else (_usda.get_diaas(r["food_name"]) if has_aa else None)
            item.update({
                "data_type":   cached["data_type"] if cached else "",
                "has_aa":      has_aa,
                "gi":          ann["gi_estimate"] if ann else None,
                "gi_source":   _ann_source(ann),
                "diaas":       diaas,
                "diaas_saved": diaas_saved is not None,
            })
            items.append(item)

    search = search.strip()
    search_results: list[dict] = []
    search_error: str | None = None
    if search:
        pantry_ids = {i["fdc_id"] for i in items if i["fdc_id"]}
        pantry_id_by_fdc = {i["fdc_id"]: i["id"] for i in items if i["fdc_id"]}
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, search)
        seen: set[int] = set()
        for row in cached:
            seen.add(row["fdc_id"])
            with _db.get_db() as conn:
                full = _db.get_cached_food(conn, row["fdc_id"])
            nuts = json.loads(full["nutrients_json"]) if full and full["nutrients_json"] else {}
            search_results.append({
                "fdc_id":    row["fdc_id"],
                "name":      row["name"],
                "data_type": row["data_type"] or "",
                "brand":     row["brand"] or "",
                "source":    "pantry" if row["fdc_id"] in pantry_ids else "cache",
                "off_code":  "",
                "aa":        _usda.aa_indicator(nuts),
                "pantry_id": pantry_id_by_fdc.get(row["fdc_id"]),
            })
        if "usda" in source:
            try:
                for food in _usda.search_foods(search, page_size=limit):
                    fid = food.get("fdcId")
                    if fid and fid not in seen:
                        seen.add(fid)
                        dtype = food.get("dataType", "")
                        search_results.append({
                            "fdc_id":    fid,
                            "name":      food.get("description", ""),
                            "data_type": dtype,
                            "brand":     food.get("brandOwner") or food.get("brandName") or "",
                            "source":    "usda",
                            "off_code":  "",
                            "aa":        "~✓" if dtype in ("Foundation", "SR Legacy") else "✗",
                        })
            except Exception as exc:
                if not search_results:
                    search_error = f"USDA API unavailable: {exc}"

        if "off" in source:
            try:
                for food in _off.search_foods(search, page_size=limit):
                    fid = food.get("fdcId")
                    if fid and fid not in seen:
                        seen.add(fid)
                        search_results.append({
                            "fdc_id":    fid,
                            "name":      food.get("description", ""),
                            "data_type": "Open Food Facts",
                            "brand":     food.get("brandOwner") or food.get("brandName") or "",
                            "source":    "off",
                            "off_code":  food.get("_off_code", ""),
                            "aa":        "✗",
                        })
            except Exception:
                pass

        search_results = _sort_search_results(search_results, search, _resolve_sort(None, "sort_food_search", "relevance", _SEARCH_SORT_MODES))
        search_results = _cap_results_preserving_local(_filter_search_results_by_source(search_results, source), limit)

    link_name = next((i["food_name"] for i in items if i["id"] == link_id), None) if link_id else None

    return templates.TemplateResponse(request, "pantry.html", {
        "items": items,
        "added": bool(added),
        "linked": bool(linked),
        "search": search,
        "search_results": search_results,
        "search_error": search_error,
        "link_id": link_id or None,
        "link_name": link_name,
        "show_archived": show_archived,
        "archived": archived,
        "source": source,
        "limit": limit,
        "source_filters": _SEARCH_SOURCE_FILTERS,
        "source_labels": _SEARCH_SOURCE_LABELS,
        "restored": restored,
    })


@app.post("/pantry/add", response_class=RedirectResponse)
async def pantry_add(
    food_name: str = Form(...),
    notes: str = Form(""),
    fdc_id: str = Form(""),
    off_code: str = Form(""),
    link_id: str = Form(""),
    next: str = Form(""),
):
    food_name = food_name.strip()
    # Where to land afterwards: Pantry by default, or back on the calling page
    # (the Food Cache's "Add to pantry" button). Local paths only.
    back = next if next.startswith("/") and not next.startswith("//") else ""
    notes = notes.strip() or None
    fdc_id_int: int | None = None
    try:
        fdc_id_int = int(fdc_id) if fdc_id.strip() else None
    except ValueError:
        pass
    link_id_int: int | None = None
    try:
        link_id_int = int(link_id) if link_id.strip() else None
    except ValueError:
        pass

    if fdc_id_int is not None:
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id_int)
        if not cached:
            try:
                detail = _fetch_uncached_food_detail(fdc_id_int, off_code)
                if detail:
                    with _db.get_db() as conn:
                        _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                                       data_type=detail.get("dataType", ""),
                                       brand=detail.get("brand"),
                                       serving_size=detail.get("servingSize"),
                                       serving_unit=detail.get("servingUnit"),
                                       nutrients=detail.get("nutrients", {}),
                                       portions=detail.get("portions", []))
                        _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
                    food_name = food_name or detail["name"]
            except Exception:
                pass

    result_flag = "added=1"
    if food_name:
        with _db.get_db() as conn:
            if link_id_int:
                existing = _db.pantry_get(conn, link_id_int)
                existing_notes = existing["notes"] if existing else None
                _db.pantry_update(conn, link_id_int, food_name, fdc_id_int, existing_notes)
                result_flag = "linked=1"
            else:
                _db.pantry_add(conn, food_name, fdc_id=fdc_id_int, notes=notes)
    dest = back or f"/pantry?{result_flag}"
    if fdc_id_int is not None and _annotation_prompt_needed(fdc_id_int):
        from urllib.parse import quote
        return RedirectResponse(
            f"/food/annotate/{fdc_id_int}?next={quote(dest)}", status_code=303
        )
    return RedirectResponse(dest, status_code=303)


@app.post("/pantry/remove/{pantry_id}", response_class=RedirectResponse)
async def pantry_remove(request: Request, pantry_id: int):
    with _db.get_db() as conn:
        _db.pantry_remove(conn, pantry_id)
    if _is_ajax_row_action(request):
        return JSONResponse({"ok": True})
    return RedirectResponse("/pantry", status_code=303)


@app.post("/pantry/{pantry_id}/archive", response_class=RedirectResponse)
async def pantry_archive(request: Request, pantry_id: int):
    """Archive or restore a pantry entry — flips whichever state it's currently in."""
    with _db.get_db() as conn:
        row = _db.pantry_get(conn, pantry_id)
        if not row:
            if _is_ajax_row_action(request):
                return JSONResponse({"ok": False})
            return RedirectResponse("/pantry", status_code=303)
        newly_archived = not row["archived"]
        _db.set_pantry_archived(conn, pantry_id, newly_archived)
    if _is_ajax_row_action(request):
        return JSONResponse({"ok": True, "archived": newly_archived})
    flag = "archived=1" if newly_archived else "restored=1"
    return RedirectResponse(f"/pantry?{flag}", status_code=303)


@app.get("/food/custom-profiles", response_class=HTMLResponse)
async def food_custom_profiles_get(request: Request, copy_q: str = Query(default=""),
                                    delete_blocked: int = 0, blocked_fdc_id: int | None = None,
                                    blocked_pantry: str = "",
                                    blocked_recipes: str = "", blocked_meals: str = ""):
    with _db.get_db() as conn:
        rows = _db.list_user_drafted_foods(conn)
        copy_results = []
        if copy_q.strip():
            copy_results = [dict(r) for r in _db.search_cached_foods(conn, copy_q.strip())]
    foods = [dict(r) for r in rows]
    return templates.TemplateResponse(request, "food_custom_profiles.html", {
        "foods": foods,
        "copy_q": copy_q.strip(),
        "copy_results": copy_results,
        "copied": False,
        "delete_blocked": delete_blocked,
        "blocked_fdc_id":  blocked_fdc_id,
        "blocked_pantry":  [int(i) for i in blocked_pantry.split(",") if i],
        "blocked_recipes": [int(i) for i in blocked_recipes.split(",") if i],
        "blocked_meals":   [int(i) for i in blocked_meals.split(",") if i],
    })


@app.post("/food/custom-profiles/create", response_class=RedirectResponse)
async def food_custom_profiles_create(name: str = Form(...)):
    name = name.strip()
    if not name:
        return RedirectResponse("/food/custom-profiles", status_code=303)
    with _db.get_db() as conn:
        fdc_id = _db.next_user_drafted_fdc_id(conn)
        _db.cache_food(
            conn,
            fdc_id=fdc_id,
            name=name,
            data_type="User Drafted",
            brand=None,
            serving_size=None,
            serving_unit=None,
            nutrients={},
            portions=[],
            user_drafted=True,
        )
    return RedirectResponse(f"/food/{fdc_id}", status_code=303)


@app.post("/food/custom-profiles/delete/{fdc_id}", response_class=RedirectResponse)
async def food_custom_profiles_delete(fdc_id: int):
    """Refused if still referenced — see food_cache_delete()'s docstring for why."""
    with _db.get_db() as conn:
        refs = _db.food_references(conn, fdc_id)
        if refs["pantry"] or refs["recipes"] or refs["meals"]:
            params: dict[str, str] = {"delete_blocked": "1", "blocked_fdc_id": str(fdc_id)}
            if refs["pantry"]:
                params["blocked_pantry"] = ",".join(str(i) for i in refs["pantry"])
            if refs["recipes"]:
                params["blocked_recipes"] = ",".join(str(i) for i in refs["recipes"])
            if refs["meals"]:
                params["blocked_meals"] = ",".join(str(i) for i in refs["meals"])
            return RedirectResponse(f"/food/custom-profiles?{urlencode(params)}", status_code=303)
        _db.delete_cached_food(conn, fdc_id)
    return RedirectResponse("/food/custom-profiles", status_code=303)


_SOURCE_PICKER_FILTERS = (["cache"] + [key for key, _name in _STATIC_SOURCES]
                           + [key for key, _name, _fn in _LIVE_SOURCES])


def _search_food_sources(conn, q: str, exclude_id: int, source: list[str] | None = None) -> list[dict]:
    """Shared search-cache-then-USDA-then-OFF lookup used by both the AA-copy and
    nutrient-copy pickers on the custom-profile edit page. `source` restricts
    results to any combination of _SOURCE_PICKER_FILTERS; empty/unset means
    all of them."""
    if not source:
        source = _SOURCE_PICKER_FILTERS
    results = []
    if "cache" in source:
        results = [
            dict(r) for r in _db.search_cached_foods(conn, q)
            if r["fdc_id"] != exclude_id
        ]
        for r in results:
            n = json.loads(r["nutrients_json"]) if r["nutrients_json"] else {}
            r["has_aa"] = _usda.has_confirmed_aa_data(n)
            r["source"] = "cache"
    seen_ids: set[int] = {exclude_id} | {r["fdc_id"] for r in results}

    # USDA/OFF search runs after the cache lookup above, and other than fdc_id
    # (needed to exclude self/dupes) uses no DB connection — a slow network
    # call must never run with a connection held open (see CLAUDE.md).
    if "usda" in source:
        try:
            general = _usda.search_foods(q)
            foundation = _usda.search_foods(q, data_types=["Foundation", "SR Legacy"])
            found_ids = {f["fdcId"] for f in foundation}
            for food in foundation + [f for f in general if f["fdcId"] not in found_ids]:
                fid = food.get("fdcId")
                if not fid or fid in seen_ids:
                    continue
                seen_ids.add(fid)
                dtype = food.get("dataType", "")
                results.append({
                    "fdc_id":    fid,
                    "name":      food.get("description", ""),
                    "data_type": dtype,
                    "has_aa":    dtype in ("Foundation", "SR Legacy"),
                    "source":    "usda",
                })
        except Exception:
            pass
    if "off" in source:
        try:
            for food in _off.search_foods(q):
                fid = food.get("fdcId")
                if not fid or fid in seen_ids:
                    continue
                seen_ids.add(fid)
                results.append({
                    "fdc_id":    fid,
                    "name":      food.get("description", ""),
                    "data_type": food.get("dataType", "Open Food Facts"),
                    "has_aa":    False,
                    "source":    "off",
                    "off_code":  food.get("_off_code", ""),
                })
        except Exception:
            pass
    if "cnf" in source:
        try:
            for food in _cnf.search_foods(q):
                fid = food.get("fdcId")
                if not fid or fid in seen_ids:
                    continue
                seen_ids.add(fid)
                results.append({
                    "fdc_id":    fid,
                    "name":      food.get("description", ""),
                    "data_type": food.get("dataType", "Canadian Nutrient File"),
                    "has_aa":    False,
                    "source":    "cnf",
                    "off_code":  "",
                })
        except Exception:
            pass
    for static_key, static_module in _STATIC_SOURCE_MODULES.items():
        if static_key not in source:
            continue
        for food in static_module.search_foods(q):
            fid = food.get("fdcId")
            if not fid or fid in seen_ids:
                continue
            seen_ids.add(fid)
            results.append({
                "fdc_id":    fid,
                "name":      food.get("description", ""),
                "data_type": food.get("dataType", static_key),
                "has_aa":    False,  # unconfirmed until fetched — see _static_source_candidates()
                "source":    static_key,
                "off_code":  "",
            })
    return _filter_search_results_by_source(results, source)


@app.get("/food/custom-profiles/{fdc_id}/edit", response_class=HTMLResponse)
async def food_custom_profiles_edit_get(request: Request, fdc_id: int, aa_source_q: str = Query(default=""),
                                        aa_applied: str = Query(default=""),
                                        aa_source: list[str] | None = Query(default=None),
                                        nutrient_source_q: str = Query(default=""),
                                        nutrients_applied: str = Query(default=""),
                                        nutrient_source: list[str] | None = Query(default=None)):
    aa_source = _resolve_source_filter(aa_source, "sort_aa_source_filter", _SOURCE_PICKER_FILTERS)
    nutrient_source = _resolve_source_filter(nutrient_source, "sort_nutrient_source_filter", _SOURCE_PICKER_FILTERS)
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        if not cached:
            return RedirectResponse("/food/custom-profiles", status_code=303)
        aa_source_results = []
        if aa_source_q.strip():
            aa_source_results = _search_food_sources(conn, aa_source_q.strip(), fdc_id, source=aa_source)
        nutrient_source_results = []
        if nutrient_source_q.strip():
            nutrient_source_results = _search_food_sources(conn, nutrient_source_q.strip(), fdc_id, source=nutrient_source)

    nutrients = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
    field_groups = [
        {
            "name": group_name,
            "fields": [
                {"key": k, "label": label, "unit": unit, "value": nutrients.get(k, "")}
                for k, label, unit in fields
            ],
        }
        for group_name, fields in _EDIT_NUTRIENT_GROUPS
    ]
    return templates.TemplateResponse(request, "food_custom_edit.html", {
        "food": dict(cached),
        "field_groups": field_groups,
        "saved": False,
        "aa_source_q": aa_source_q.strip(),
        "aa_source_results": aa_source_results,
        "aa_applied": aa_applied,
        "aa_source": aa_source,
        "aa_omitted_sources": _omitted_source_labels(aa_source, _SOURCE_PICKER_FILTERS),
        "nutrient_source_q": nutrient_source_q.strip(),
        "nutrient_source_results": nutrient_source_results,
        "nutrients_applied": nutrients_applied,
        "nutrient_source": nutrient_source,
        "nutrient_omitted_sources": _omitted_source_labels(nutrient_source, _SOURCE_PICKER_FILTERS),
        "source_filters": _SOURCE_PICKER_FILTERS,
        "source_labels": _SEARCH_SOURCE_LABELS,
    })


@app.post("/food/custom-profiles/{fdc_id}/edit", response_class=HTMLResponse)
async def food_custom_profiles_edit_post(request: Request, fdc_id: int):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        return RedirectResponse("/food/custom-profiles", status_code=303)
    form = await request.form()
    name = (form.get("name") or cached["name"]).strip() or cached["name"]
    serving_size: float | None = cached["serving_size"]
    srv_raw = (form.get("serving_size") or "").strip()
    if srv_raw:
        try:
            serving_size = float(srv_raw)
        except ValueError:
            pass
    serving_unit = (form.get("serving_unit") or cached["serving_unit"] or "").strip() or None
    notes = (form.get("notes") or "").strip() or None
    nutrients: dict[str, float] = {}
    for key in _ALL_NUTRIENT_KEYS:
        raw = (form.get(key) or "").strip()
        if raw:
            try:
                v = float(raw)
                if v != 0:
                    nutrients[key] = v
            except ValueError:
                pass
    portions_json = cached["portions_json"]
    portions: list[dict] = []
    if portions_json and portions_json != "null":
        portions = json.loads(portions_json)
    impact_targets = _impact_targets([fdc_id])
    impact_before = _impact_snapshot(*impact_targets)
    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id, name, nutrients,
            data_type=cached["data_type"] or "User Drafted",
            brand=cached["brand"],
            serving_size=serving_size,
            serving_unit=serving_unit,
            portions=portions,
            notes=notes,
            user_drafted=True,
        )
        _recipe_dcp.cascade_food_change(fdc_id, conn)
    impact = _impact_pop(_impact_store(f"Saving {name}", impact_before, _impact_snapshot(*impact_targets)))
    with _db.get_db() as conn:
        updated = _db.get_cached_food(conn, fdc_id)
    nutrients_reload = json.loads(updated["nutrients_json"]) if updated["nutrients_json"] else {}
    field_groups = [
        {
            "name": group_name,
            "fields": [
                {"key": k, "label": label, "unit": unit, "value": nutrients_reload.get(k, "")}
                for k, label, unit in fields
            ],
        }
        for group_name, fields in _EDIT_NUTRIENT_GROUPS
    ]
    return templates.TemplateResponse(request, "food_custom_edit.html", {
        "food": dict(updated),
        "field_groups": field_groups,
        "saved": True,
        "impact": impact,
        "aa_source_q": "",
        "aa_source_results": [],
        "aa_applied": "",
        "aa_source": _SOURCE_PICKER_FILTERS,
        "nutrient_source_q": "",
        "nutrient_source_results": [],
        "nutrients_applied": "",
        "nutrient_source": _SOURCE_PICKER_FILTERS,
        "source_filters": _SOURCE_PICKER_FILTERS,
        "source_labels": _SEARCH_SOURCE_LABELS,
    })


@app.post("/food/custom-profiles/{fdc_id}/copy-aa", response_class=RedirectResponse)
async def food_custom_profiles_copy_aa(fdc_id: int, source_fdc_id: int = Form(...), off_code: str = Form("")):
    """Estimate this food's amino acid profile by scaling a source food's AA
    values to this food's own protein content (see numa_app/services/aa_estimate.py).
    Marks the target user_drafted=True, same as any other in-place edit."""
    with _db.get_db() as conn:
        target = _db.get_cached_food(conn, fdc_id)
        if not target:
            return RedirectResponse("/food/custom-profiles", status_code=303)

    try:
        source = _get_or_cache_source_food(source_fdc_id, off_code)
    except Exception:
        return RedirectResponse(
            f"/food/custom-profiles/{fdc_id}/edit?aa_applied=source_fetch_failed", status_code=303
        )

    target_nutrients = json.loads(target["nutrients_json"]) if target["nutrients_json"] else {}
    source_nutrients = json.loads(source["nutrients_json"]) if source["nutrients_json"] else {}
    updated, factor, err = _aa_estimate.estimate_aa(target_nutrients, source_nutrients)
    if err:
        return RedirectResponse(
            f"/food/custom-profiles/{fdc_id}/edit?aa_applied=error", status_code=303
        )

    portions_json = target["portions_json"]
    portions: list[dict] = json.loads(portions_json) if portions_json and portions_json != "null" else []
    note = _aa_estimate.source_note(source["name"], source_fdc_id, factor)
    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id, target["name"], updated,
            data_type=target["data_type"] or "User Drafted",
            brand=target["brand"],
            serving_size=target["serving_size"],
            serving_unit=target["serving_unit"],
            portions=portions,
            notes=note,
            user_drafted=True,
        )
        _recipe_dcp.cascade_food_change(fdc_id, conn)
    return RedirectResponse(f"/food/custom-profiles/{fdc_id}/edit?aa_applied=ok", status_code=303)


@app.get("/food/custom-profiles/{fdc_id}/compare", response_class=RedirectResponse)
async def food_custom_profiles_compare(fdc_id: int, pick: list[str] = Query(default=[]),
                                       return_to: str = Query(default="")):
    """The edit page's "Compare checked foods": open Compare with the profile
    being edited first, then each checked search result, and a button back.
    Each `pick` is "<fdc_id>|<off_code>". Compare fetches an uncached USDA food
    live, but has no way to reach the other external sources, so those are
    cached first, exactly as "Choose fields to copy" does; one that can't be
    fetched is left out rather than failing the whole comparison."""
    item_list: list[tuple[str, int]] = [("food", fdc_id)]
    skipped = 0
    for raw in pick:
        id_str, _, off_code = raw.partition("|")
        try:
            pick_id = int(id_str)
        except ValueError:
            continue
        if ("food", pick_id) in item_list:
            continue
        if len(item_list) >= _MAX_COMPARE_ITEMS:
            skipped += 1
            continue
        if pick_id <= 0:
            try:
                _get_or_cache_source_food(pick_id, off_code)
            except Exception:
                skipped += 1
                continue
        item_list.append(("food", pick_id))
    url = f"/compare?items={_compare_items_str(item_list)}"
    if skipped:
        url += (f"&error={skipped}+checked+food{'s' if skipped != 1 else ''}+left+out"
                f"+%E2%80%94+could+not+be+fetched%2C+or+over+the+{_MAX_COMPARE_ITEMS}-item+maximum")
    return RedirectResponse(_with_return(url, return_to or f"/food/custom-profiles/{fdc_id}/edit"),
                            status_code=303)


@app.get("/food/custom-profiles/{fdc_id}/copy-nutrients/select", response_class=HTMLResponse)
async def food_custom_profiles_copy_nutrients_select(request: Request, fdc_id: int,
                                                       source_fdc_id: int = Query(...),
                                                       off_code: str = Query("")):
    """Let the user pick exactly which nutrient values to bring in from
    source_fdc_id, rather than an all-or-nothing whole-profile copy — the
    target food may only be missing a few fields (see copy-nutrients below).
    Only fields the source actually has a value for are offered."""
    with _db.get_db() as conn:
        target = _db.get_cached_food(conn, fdc_id)
        if not target:
            return RedirectResponse("/food/custom-profiles", status_code=303)

    try:
        source = _get_or_cache_source_food(source_fdc_id, off_code)
    except Exception:
        return RedirectResponse(
            f"/food/custom-profiles/{fdc_id}/edit?nutrients_applied=source_fetch_failed", status_code=303
        )

    source_nutrients = json.loads(source["nutrients_json"]) if source["nutrients_json"] else {}
    if not source_nutrients:
        return RedirectResponse(
            f"/food/custom-profiles/{fdc_id}/edit?nutrients_applied=error", status_code=303
        )

    target_nutrients = json.loads(target["nutrients_json"]) if target["nutrients_json"] else {}
    field_groups = []
    for group_name, fields in _EDIT_NUTRIENT_GROUPS:
        rows = [
            {
                "key":           k,
                "label":         label,
                "unit":          unit,
                "source_value":  source_nutrients[k],
                "target_value":  target_nutrients.get(k, ""),
            }
            for k, label, unit in fields if k in source_nutrients
        ]
        if rows:
            field_groups.append({"name": group_name, "fields": rows})

    return templates.TemplateResponse(request, "food_custom_copy_select.html", {
        "food":          dict(target),
        "source_name":   source["name"],
        "source_fdc_id": source_fdc_id,
        "off_code":      off_code,
        "field_groups":  field_groups,
    })


@app.post("/food/custom-profiles/{fdc_id}/copy-nutrients", response_class=RedirectResponse)
async def food_custom_profiles_copy_nutrients(fdc_id: int, source_fdc_id: int = Form(...),
                                               off_code: str = Form(""), keys: list[str] = Form(default=[])):
    """Copy only the selected nutrient keys from source_fdc_id's per-100g
    values onto this profile, raw and unscaled — everything else already on
    this profile (selected-but-absent-from-source fields aside, which can't
    happen since /copy-nutrients/select only ever offers keys the source
    actually has) is left untouched. Independent of copy-aa: either can
    overwrite the other's fields where they overlap."""
    with _db.get_db() as conn:
        target = _db.get_cached_food(conn, fdc_id)
        if not target:
            return RedirectResponse("/food/custom-profiles", status_code=303)

    try:
        source = _get_or_cache_source_food(source_fdc_id, off_code)
    except Exception:
        return RedirectResponse(
            f"/food/custom-profiles/{fdc_id}/edit?nutrients_applied=source_fetch_failed", status_code=303
        )

    source_nutrients = json.loads(source["nutrients_json"]) if source["nutrients_json"] else {}
    selected_keys = [k for k in keys if k in _ALL_NUTRIENT_KEYS and k in source_nutrients]
    if not selected_keys:
        return RedirectResponse(
            f"/food/custom-profiles/{fdc_id}/edit?nutrients_applied=none_selected", status_code=303
        )

    target_nutrients = json.loads(target["nutrients_json"]) if target["nutrients_json"] else {}
    updated = dict(target_nutrients)
    for k in selected_keys:
        updated[k] = source_nutrients[k]

    field_labels = [label for group_name, fields in _EDIT_NUTRIENT_GROUPS for k, label, unit in fields
                    if k in selected_keys]
    portions_json = target["portions_json"]
    portions: list[dict] = json.loads(portions_json) if portions_json and portions_json != "null" else []
    note = _aa_estimate.copy_nutrients_note(source["name"], source_fdc_id, field_labels)
    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id, target["name"], updated,
            data_type=target["data_type"] or "User Drafted",
            brand=target["brand"],
            serving_size=target["serving_size"],
            serving_unit=target["serving_unit"],
            portions=portions,
            notes=note,
            user_drafted=True,
        )
        _recipe_dcp.cascade_food_change(fdc_id, conn)
    return RedirectResponse(f"/food/custom-profiles/{fdc_id}/edit?nutrients_applied=ok", status_code=303)


def _duplicate_food_as_draft(conn, cached) -> int:
    """Create a new user-drafted food that's a nutrient-for-nutrient copy of
    an existing cached food, named "Copy of ...". Returns the new fdc_id."""
    new_id = _db.next_user_drafted_fdc_id(conn)
    nutrients = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
    portions_json = cached["portions_json"]
    portions: list[dict] = []
    if portions_json and portions_json != "null":
        portions = json.loads(portions_json)
    _db.cache_food(
        conn,
        fdc_id=new_id,
        name=f"Copy of {cached['name']}",
        data_type="User Drafted",
        brand=cached["brand"],
        serving_size=cached["serving_size"],
        serving_unit=cached["serving_unit"],
        nutrients=nutrients,
        portions=portions,
        user_drafted=True,
    )
    return new_id


@app.post("/food/custom-profiles/copy/{fdc_id}", response_class=RedirectResponse)
async def food_custom_profiles_copy(fdc_id: int):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        if not cached:
            return RedirectResponse("/food/custom-profiles", status_code=303)
        new_id = _duplicate_food_as_draft(conn, cached)
    return RedirectResponse(f"/food/custom-profiles/{new_id}/edit", status_code=303)


@app.post("/food/custom-profiles/copy-from-search", response_class=RedirectResponse)
async def food_custom_profiles_copy_from_search(fdc_id: int = Form(...), off_code: str = Form("")):
    """Shortcut from Food Search results: duplicate a search result as an
    editable custom-profile draft in one step, without a detour through the
    Custom Profiles page's own "copy a cached food as a draft" search box.
    Unlike copy/{fdc_id} above, the result may not be cached yet (a live
    USDA/OFF/etc. hit the user hasn't opened before), so it's fetched first
    same as pantry-add and meal-add-food do for uncached search results.
    Landing on the new draft's edit page, its AA-source search box is the
    next step for copying amino acid data from a different food (see
    numa_app/services/aa_estimate.py)."""
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        try:
            detail = _fetch_uncached_food_detail(fdc_id, off_code)
        except Exception:
            return RedirectResponse("/food/custom-profiles", status_code=303)
        with _db.get_db() as conn:
            _db.cache_food(
                conn, fdc_id=detail["fdcId"], name=detail["name"],
                data_type=detail.get("dataType", ""),
                brand=detail.get("brand"),
                serving_size=detail.get("servingSize"),
                serving_unit=detail.get("servingUnit"),
                nutrients=detail.get("nutrients", {}),
                portions=detail.get("portions", []),
            )
            _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
            cached = _db.get_cached_food(conn, detail["fdcId"])

    with _db.get_db() as conn:
        new_id = _duplicate_food_as_draft(conn, cached)
    return RedirectResponse(f"/food/custom-profiles/{new_id}/edit", status_code=303)


def _missing_annotations(ann) -> list[str]:
    """Which of GI / DIAAS this food still has no estimate for and hasn't been
    told to stop asking about. Drives both whether to detour to the Annotate
    page after adding a food and what that page says is missing.

    A global GI opt-out removes GI from this list for every food, which is what
    makes the opt-out mean "stop asking me" rather than only "stop warning me
    about the reference table": _annotation_prompt_needed() is built on this, so
    a food lacking nothing but a GI value no longer interrupts an add."""
    ask_gi = not _gi_opt_out()
    if ann is None:
        return ["GI", "DIAAS"] if ask_gi else ["DIAAS"]
    missing = []
    if ask_gi and ann["gi_estimate"] is None and not ann["gi_no_prompt"]:
        missing.append("GI")
    if ann["diaas_estimate"] is None and not ann["diaas_no_prompt"]:
        missing.append("DIAAS")
    return missing


def _annotation_prompt_needed(fdc_id: int) -> bool:
    """True if adding this food should detour to the Annotate page: it is
    still missing a GI or DIAAS estimate the user hasn't suppressed prompts
    for, AND they haven't already saved the Annotate form for it. An estimate
    that's already stored is never prompted for again — it's edited from the
    GI/DIAAS cells on the add-food row, or from Annotate a Food.

    The "reviewed" half matters because the detour is all-or-nothing across
    both estimates: before it existed, saving a GI (even with "don't prompt
    me for a GI again" ticked) still left DIAAS unsettled, so the very same
    food kept interrupting every time it was added, and the page it landed
    on looked exactly like the GI prompt the user thought they had just
    dismissed. Saving the form now means "I have seen both and made my
    choices" — deliberately leaving one blank included. "Skip for now"
    saves nothing, so it still asks again next time."""
    with _db.get_db() as conn:
        ann = _db.get_food_annotation(conn, fdc_id)
    if ann is not None and ann["reviewed"]:
        return False
    return bool(_missing_annotations(ann))


@app.get("/food/annotate", response_class=HTMLResponse)
async def food_annotate_list(request: Request, q: str = ""):
    with _db.get_db() as conn:
        if q.strip():
            rows = _db.search_cached_foods(conn, q.strip())
        else:
            rows = _db.list_cached_foods(conn)
        fdc_ids = [r["fdc_id"] for r in rows]
        annotations = _db.annotations_for_fdcids(conn, fdc_ids) if fdc_ids else {}

    foods = []
    for row in rows:
        ann = annotations.get(row["fdc_id"])
        foods.append({
            "fdc_id":    row["fdc_id"],
            "name":      row["name"],
            "data_type": row["data_type"] or "",
            "gi":        ann["gi_estimate"] if ann else None,
            "gi_source": _ann_source(ann),
            "diaas":     ann["diaas_estimate"] if ann else None,
        })
    return templates.TemplateResponse(request, "food_annotate.html", {
        "editing": False,
        "foods":   foods,
        "q":       q,
    })


@app.get("/food/annotate/{fdc_id}", response_class=HTMLResponse)
async def food_annotate_edit_get(request: Request, fdc_id: int, saved: str = "", next: str = ""):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        ann = _db.get_food_annotation(conn, fdc_id)
    food_name = cached["name"] if cached else f"Food {fdc_id}"
    profile = _profile.load_profile()
    gi_default_population = profile.glucose_tolerance if profile and profile.glucose_tolerance else "both"
    return templates.TemplateResponse(request, "food_annotate.html", {
        "editing":   True,
        "fdc_id":    fdc_id,
        "food_name": food_name,
        "annotation": dict(ann) if ann else None,
        "missing":   _missing_annotations(ann),
        "saved":     bool(saved),
        "next":      next,
        "gi_default_population": gi_default_population,
        "gi_table":  _gi_lookup.active_table_info(),
        "gi_opt_out": _gi_opt_out(),
    })


@app.get("/food/annotate/{fdc_id}/gi-lookup", response_class=JSONResponse)
async def food_annotate_gi_lookup(fdc_id: int, q: str = "", population: str = "both"):
    if population not in ("normal", "impaired", "both"):
        population = "both"
    results = _gi_lookup.search(q, population=population, limit=8)
    return JSONResponse({"results": results})


@app.post("/food/annotate/{fdc_id}", response_class=RedirectResponse)
async def food_annotate_edit_post(
    fdc_id: int,
    gi_estimate:     str = Form(""),
    gi_source:       str = Form(""),
    diaas_estimate:  str = Form(""),
    prep_context:    str = Form(""),
    gi_no_prompt:    str = Form(""),
    diaas_no_prompt: str = Form(""),
    next:            str = Form(""),
):
    gi   = float(gi_estimate)    if gi_estimate.strip()    else None
    dias = float(diaas_estimate) if diaas_estimate.strip() else None
    prep = prep_context.strip() or None
    # gi_source is filled in by the reference-table lookup on the page (and
    # cleared by it if the GI box is then hand-edited), so it arrives as
    # ordinary form text -- trimmed to a sane length before it is stored.
    src  = " ".join(gi_source.split())[:300] or None
    keep_gi_no_prompt = _gi_opt_out()
    with _db.get_db() as conn:
        if keep_gi_no_prompt:
            # The per-food "don't prompt me for a GI estimate" tick-box is not
            # rendered while the global opt-out is on, so the form cannot carry
            # its value -- and set_food_annotation() overwrites that column on
            # every save. Carry the stored value forward instead of letting an
            # absent checkbox clear a choice that matters again the moment the
            # opt-out is switched back off.
            existing = _db.get_food_annotation(conn, fdc_id)
            gi_no_prompt = bool(existing["gi_no_prompt"]) if existing else False
        _db.set_food_annotation(
            conn, fdc_id,
            gi_estimate=gi,
            gi_source=src,
            gi_no_prompt=bool(gi_no_prompt),
            diaas_estimate=dias,
            diaas_no_prompt=bool(diaas_no_prompt),
            prep_context=prep,
        )
        # An annotation is an edit (owner's decision) — see foods.user_edited.
        if gi is not None or dias is not None or prep:
            _db.mark_user_edited(conn, fdc_id)
    if next:
        return RedirectResponse(next, status_code=303)
    return RedirectResponse(f"/food/annotate/{fdc_id}?saved=1", status_code=303)


@app.post("/food/annotate/{fdc_id}/skip-forever", response_class=RedirectResponse)
async def food_annotate_skip_forever(fdc_id: int, next: str = Form("")):
    """Suppress future GI and DIAAS prompts for this food without touching any
    stored estimate. Both, because the button reads as "stop asking me about
    this food" — suppressing only one would keep the detour appearing."""
    with _db.get_db() as conn:
        _db.upsert_food_annotation(conn, fdc_id, gi_no_prompt=1, diaas_no_prompt=1)
    if next:
        return RedirectResponse(next, status_code=303)
    return RedirectResponse("/food/annotate", status_code=303)


@app.post("/food/annotate/{fdc_id}/clear", response_class=RedirectResponse)
async def food_annotate_clear(fdc_id: int):
    with _db.get_db() as conn:
        _db.delete_food_annotation(conn, fdc_id)
    return RedirectResponse(f"/food/annotate/{fdc_id}", status_code=303)


# /food/{fdc_id} must be registered LAST among /food/* routes so literal paths win.
def _food_detail_context(
    fdc_id: int,
    amount: float,
    portion_str: str,
    ignore_complements: list[str],
    unignore: list[str],
    comp_sort: str | None = None,
    diaas_sort: str | None = None,
    anchor_name: list[str] | None = None,
    anchor_grams: list[str] | None = None,
) -> dict:
    nutrients: dict = {}
    portions: list = []
    food: dict = {}

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)

    if cached:
        nutrients = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
        portions = json.loads(cached["portions_json"] or "[]") or []
        food = {
            "fdc_id":        cached["fdc_id"],
            "name":          cached["name"],
            "data_type":     cached["data_type"],
            "brand":         cached["brand"] or "",
            "serving_size":  cached["serving_size"],
            "serving_unit":  cached["serving_unit"] or "",
            "user_drafted":  bool(cached["user_drafted"]),
        }
    else:
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception as exc:
            return {"error": f"Could not load food {fdc_id}: {exc}"}
        nutrients = detail.get("nutrients", {})
        portions = detail.get("portions", [])
        food = {
            "fdc_id":       detail["fdcId"],
            "name":         detail["name"],
            "data_type":    detail.get("dataType", ""),
            "brand":        detail.get("brand") or "",
            "serving_size": detail.get("servingSize"),
            "serving_unit": detail.get("servingUnit") or "",
            "user_drafted": False,
        }
        with _db.get_db() as conn:
            _db.cache_food(
                conn,
                fdc_id=detail["fdcId"],
                name=detail["name"],
                data_type=detail.get("dataType", ""),
                brand=detail.get("brand"),
                serving_size=detail.get("servingSize"),
                serving_unit=detail.get("servingUnit"),
                nutrients=nutrients,
                portions=portions,
            )
            _recipe_dcp.cascade_food_change(detail["fdcId"], conn)

    # Resolve portion: free-form string takes priority over plain gram amount
    portion_error: str | None = None
    portion_label: str | None = None
    portion_density_hint = False
    if portion_str.strip():
        parsed_g, parsed_label = _parse_portion_str(portion_str.strip(), portions, food["name"])
        if parsed_g is None:
            portion_error = parsed_label  # error message
            portion_density_hint = "no density data is available" in parsed_label
            amount = 100.0
        else:
            amount = parsed_g if parsed_g > 0 else 100.0
            portion_label = parsed_label
    elif amount != 100.0 and portions:
        # A bare gram amount with no portion_str (e.g. a recipe/meal
        # ingredient's "view this food" link, which only passes the raw
        # gram total) can exactly match N of this food's defined portions.
        # That matters most for "piece" foods (tablet, egg, slice, …) whose
        # portion gram_weight is an internal scaling placeholder rather than
        # a literal weight — e.g. a user-drafted supplement's "1 tablet"
        # portion set to 100g purely so its per-100g-basis nutrients scale
        # to "1 tablet" correctly. Showing the raw figure there ("200 g")
        # reads as nonsense for something that's really "2 tablets". Recover
        # a portion-based label whenever the match is exact enough to be
        # intentional, not a coincidental round number.
        for _p in portions:
            _gw = _p.get("gram_weight") or 0
            if _gw <= 0:
                continue
            _multiple = amount / _gw
            if abs(_multiple - round(_multiple)) < 0.01:
                _n = round(_multiple)
                portion_label = _p["description"] if _n == 1 else f"{_n:g} × {_p['description']}"
                break

    # Scale nutrient display values; protein analysis uses per-100g ratios so stays unscaled
    display_nutrients = _usda.scale_nutrients(nutrients, amount) if amount != 100.0 else nutrients
    rda = _load_rda()
    optimal = _load_optimal()
    max_limits = _load_max_limits()
    # For RDA / Optimal % on food detail, scale the targets by the same portion factor
    rda_scaled: dict | None = None
    if rda and amount != 100.0:
        rda_scaled = {k: (v * (amount / 100.0), u, t) for k, (v, u, t) in rda.items()}
    optimal_scaled: dict | None = None
    if optimal and amount != 100.0:
        optimal_scaled = {k: (v * (amount / 100.0), u, t) for k, (v, u, t) in optimal.items()}
    antinutrient_flags = _usda.get_antinutrient_flags(food["name"])

    # Foundation fallback: protein present but no AA data — suggest a Foundation Foods search
    suggest_foundation: str | None = None
    if nutrients.get("protein_g", 0) > 0 and not _usda.has_amino_acid_data(nutrients):
        suggest_foundation = food["name"].split(",")[0].strip()

    # No usable nutrient data at all (missing every proximate, even after the
    # abridged-format retry in get_food_detail()) — flag it rather than show
    # a silently blank nutrient table.
    missing_macros = not _usda.has_macro_data(nutrients)

    oxalate = _oxalate_info(food["fdc_id"], food["name"])
    oxalate_mg_portion: float | None = None
    if oxalate and amount and oxalate.get("mg_per_100g") is not None:
        oxalate_mg_portion = round(oxalate["mg_per_100g"] * amount / 100.0, 1)

    with _db.get_db() as conn:
        ann = _db.get_food_annotation(conn, fdc_id)
        data_ignored = _db.food_data_ignores(conn).get(fdc_id, set())
    # Nutrient groups this food has no data for (data_completeness.py), split
    # into ones still to deal with and ones the user marked not needed.
    _all_gaps = _data_completeness.missing_groups(nutrients)
    data_gaps = [g for g in _all_gaps if g not in data_ignored]
    data_gaps_ignored = [g for g in _all_gaps if g in data_ignored]
    gi_estimate = ann["gi_estimate"] if ann else None
    gi_source   = (ann["gi_source"] if ann and "gi_source" in ann.keys() else None) \
                  if gi_estimate is not None else None

    # GL for the portion actually being analyzed. Both halves of the formula are
    # already here — the annotated GI and this portion's carbohydrate grams — so
    # showing only GI would leave the reader to do GI x carbs / 100 by hand on
    # the one page where portion experiments happen.
    gl_portion: float | None = None
    if gi_estimate is not None:
        gl_portion = round(gi_estimate * display_nutrients.get("carbs_g", 0.0) / 100.0, 1)

    protein_section = _protein_section(food["name"], display_nutrients)

    return {
        "food":               food,
        "amount":             amount,
        "portion_str":        portion_str.strip(),
        "portion_label":      portion_label,
        "portion_error":      portion_error,
        "portion_density_hint": portion_density_hint,
        "portions":           portions,
        "nutrient_sections":  _nutrient_sections(display_nutrients, rda_scaled or rda,
                                                 optimal=optimal_scaled or optimal, max_limits=max_limits,
                                                 dcp_g=protein_section["dcp_g"] if protein_section else None),
        "dcp_missing_names":  [],
        "protein":            protein_section,
        "complements":        _food_complement_section(food["name"], display_nutrients, exclude_names=_effective_ignored(ignore_complements, unignore), comp_sort=comp_sort, diaas_sort=diaas_sort, anchor_overrides=_parse_anchor_overrides(anchor_name or [], anchor_grams or [])),
        "ignored_complements": sorted(_effective_ignored(ignore_complements, unignore)),
        "antinutrients":      antinutrient_flags,
        "has_profile":        rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
        "suggest_foundation": suggest_foundation,
        "missing_macros":     missing_macros,
        "data_gaps":          data_gaps,
        "data_gaps_ignored":  data_gaps_ignored,
        "gap_labels":         _data_completeness.GROUP_LABELS,
        "no_nutrients":       not nutrients,
        "is_usda_food":       (_classify_food_id(fdc_id) or ("", ""))[1] == "USDA",
        "missing_core_macros": [lbl for k, lbl in (("calories", "calories"), ("protein_g", "protein"),
                                                   ("carbs_g", "carbohydrate"), ("fat_g", "fat"))
                                if k not in nutrients],
        "oxalate":            oxalate,
        "oxalate_mg_portion": oxalate_mg_portion,
        "gi_estimate":        gi_estimate,
        "gi_source":          gi_source,
        "diaas_estimate":     ann["diaas_estimate"] if ann else None,
        "gl_portion":         gl_portion,
    }


@app.get("/food/{fdc_id}", response_class=HTMLResponse)
async def food_detail(
    request: Request,
    fdc_id: int,
    amount: float = Query(default=100.0, gt=0),
    portion_str: str = Query(default=""),
    ignore_complements: list[str] = Query(default=[]),
    unignore: list[str] = Query(default=[]),
    comp_sort: str | None = None,
    diaas_sort: str | None = None,
    anchor_name: list[str] = Query(default=[]),
    anchor_grams: list[str] = Query(default=[]),
    from_context: str = Query(default=""),
):
    comp_sort = _resolve_sort(comp_sort, "sort_complements", "dcp", _COMP_SORT_MODES)
    diaas_sort = _resolve_sort(diaas_sort, "sort_diaas_improvers", "effect", _DIAAS_SORT_MODES)
    ctx = _food_detail_context(fdc_id, amount, portion_str, ignore_complements, unignore,
                                comp_sort=comp_sort, diaas_sort=diaas_sort,
                                anchor_name=anchor_name, anchor_grams=anchor_grams)
    if "error" in ctx:
        return templates.TemplateResponse(request, "search.html", {
            "results": [], "query": "", "error": ctx["error"],
        })
    ctx["from_context"] = from_context if from_context in ("recipe", "meal") else ""
    ctx["incoming_applied"] = request.query_params.get("incoming_applied", "")
    ctx["impact"] = _impact_pop(request.query_params.get("impact", ""))
    with _db.get_db() as conn:
        ctx["quality_issues"] = _data_quality.issues_for_food(conn, fdc_id)
        ctx["calories_ok"] = _data_quality.CALORIES_OK_KEY in _db.food_data_ignores(conn).get(fdc_id, set())
        ctx["your_changes"] = _your_changes(conn, fdc_id)
        ctx["older_versions"] = _db.food_versions_of(conn, fdc_id)
        ctx["version_info"] = _db.food_version_info(fdc_id)
        if ctx["version_info"]:
            ctx["version_parent"] = _db.get_cached_food(conn, ctx["version_info"]["parent_fdc_id"])
            ctx["version_meal_items"] = conn.execute(
                "SELECT COUNT(*) FROM meal_items WHERE item_type = 'food' AND fdc_id = ?", (fdc_id,)).fetchone()[0]
    try:
        ctx["version_kept"] = int(request.query_params.get("version_kept", ""))
        ctx["version_moved"] = int(request.query_params.get("version_moved", "0"))
    except ValueError:
        ctx["version_kept"] = None
    return templates.TemplateResponse(request, "food_detail.html", ctx)


def _your_changes(conn, fdc_id: int) -> list[dict] | None:
    """The values the user changed on an outside-source food, each beside the
    source's own (db.food_edited_keys) — [{label, yours, original}] — or
    None when that isn't known (a custom food, or one edited before NuMa
    tracked values one by one)."""
    keys = _db.food_edited_keys(conn, fdc_id)
    if keys is None:
        return None
    row = _db.get_cached_food(conn, fdc_id)
    current = _db._food_state(row)
    source = _db.food_source(conn, fdc_id) or {}
    src_portions = {str(p.get("description", "")).strip().lower(): p for p in source.get("portions") or []}

    def _num(v, unit=""):
        if v in (None, ""):
            return "—"
        return f"{v:g}{(' ' + unit) if unit else ''}" if isinstance(v, (int, float)) else str(v)

    out = []
    for k in keys:
        if k.startswith(_db.PORTION_KEY_PREFIX):
            desc = k[len(_db.PORTION_KEY_PREFIX):]
            mine = next((p for p in current["portions"] if str(p.get("description", "")).strip() == desc), {})
            theirs = src_portions.get(desc.lower(), {})
            out.append({"label": f"Portion: {desc}", "yours": _num(mine.get("gram_weight"), "g"),
                        "original": _num(theirs.get("gram_weight"), "g") if theirs else "(not listed)"})
        elif k in ("serving_size", "serving_unit"):
            out.append({"label": "Serving size" if k == "serving_size" else "Serving unit",
                        "yours": _num(current.get(k)), "original": _num(source.get(k))})
        else:
            label, unit = _usda.nutrient_label(k)
            out.append({"label": label, "yours": _num(current["nutrients"].get(k), unit),
                        "original": _num((source.get("nutrients") or {}).get(k), unit)})
    return out


def _local_next(next_url: str, fallback: str) -> str:
    """A post-action destination, only ever a path inside numa."""
    next_url = (next_url or "").strip()
    if not next_url.startswith("/") or next_url.startswith("//") or "\\" in next_url:
        return fallback
    return next_url


@app.get("/food/{fdc_id}/review-incoming", response_class=HTMLResponse)
async def food_review_incoming(request: Request, fdc_id: int, source: str = "usda",
                               source_fdc_id: int | None = None, off_code: str = "",
                               next: str = ""):
    """One review screen for incoming data (incoming_review.py): a fresh USDA
    copy of this food (source=usda, the Refresh buttons) or another food's
    values (source=food, Fill in nutrients from another food). Nothing is
    written here; the incoming values ride along in the form so the apply
    step writes exactly what was reviewed."""
    next = _local_next(next, f"/food/{fdc_id}")
    with _db.get_db() as conn:
        target = _db.get_cached_food(conn, fdc_id)
    if not target:
        return RedirectResponse(next, status_code=303)
    target_nutrients = json.loads(target["nutrients_json"]) if target["nutrients_json"] else {}
    target_portions = json.loads(target["portions_json"] or "[]") or []
    is_custom = _db.is_custom_food_id(fdc_id)
    edited = bool(target["user_edited"])
    with _db.get_db() as conn:
        estimated = _db.estimated_keys(conn, fdc_id)
    ctx = {"food": dict(target), "source": source, "next": next, "error": None,
           "source_name": "", "source_fdc_id": source_fdc_id, "off_code": off_code,
           "aa_note": None, "aa_alt": {}}
    incoming: dict = {}
    if source == "food":
        if source_fdc_id is None or source_fdc_id == fdc_id:
            return RedirectResponse(next, status_code=303)
        try:
            src = _get_or_cache_source_food(source_fdc_id, off_code)
            incoming = {"nutrients": json.loads(src["nutrients_json"]) if src["nutrients_json"] else {},
                        "name": src["name"]}
            ctx["source_name"] = src["name"]
        except Exception as exc:
            ctx["error"] = f"Couldn't fetch that food's details: {exc}"
        prefer_incoming = False
    else:
        source = ctx["source"] = "usda"
        if fdc_id <= 0:
            ctx["error"] = "Only foods from USDA can be refreshed from USDA."
        else:
            try:
                detail = _usda.get_food_detail(fdc_id)
                incoming = {"nutrients": detail.get("nutrients", {}) or {},
                            "name": detail.get("name") or "", "brand": detail.get("brand") or "",
                            "data_type": detail.get("dataType") or "",
                            "serving_size": detail.get("servingSize"),
                            "serving_unit": detail.get("servingUnit") or "",
                            "portions": detail.get("portions") or []}
                ctx["source_name"] = "USDA (fresh copy)"
                ctx["usda_data_type"] = incoming["data_type"]
                ctx["usda_brand"] = incoming["brand"]
            except Exception as exc:
                ctx["error"] = f"Couldn't reach USDA: {exc}"
        prefer_incoming = not edited and not is_custom
    # Which values are the user's own (db.food_edited_keys): known for any
    # food with a source copy. Then default ticks go value by value — USDA's
    # update to a value you never touched is ticked, your own value isn't.
    mine: set[str] | None = None
    if source == "usda" and not ctx["error"] and not is_custom:
        with _db.get_db() as conn:
            _keys = _db.food_edited_keys(conn, fdc_id)
            ctx["edits_left"] = _db.edits_left_after_full_refresh(conn, fdc_id, incoming)
        mine = set(_keys) if _keys is not None else None
    ctx["edits_known"] = mine is not None
    compare_to = incoming.get("nutrients", {}) if not ctx["error"] else {}
    if source == "food" and not ctx["error"]:
        # Amino acids from another food are scaled to protein, never raw:
        # to this food's protein, or the incoming protein if that is ticked
        # too (aa_alt — the screen swaps to those values live).
        raw = incoming["nutrients"]
        aa_keys = [k for k in raw if k.startswith("aa_")]
        if aa_keys and _usda.has_amino_acid_data(raw):
            own_scaled, _f = _aa_estimate.scaled_aa(raw, target_nutrients.get("protein_g"))
            inc_scaled, _f2 = _aa_estimate.scaled_aa(raw, raw.get("protein_g"))
            compare_to = {k: v for k, v in raw.items() if not k.startswith("aa_")}
            if own_scaled:
                compare_to.update(own_scaled)
                ctx["aa_note"] = (f"Amino acids are scaled to this food's protein "
                                  f"({target_nutrients.get('protein_g')} g per 100 g), not copied raw.")
            elif inc_scaled:
                compare_to.update(inc_scaled)
                ctx["aa_note"] = ("This food has no protein value yet, so amino acids are scaled to "
                                  f"{ctx['source_name']}'s protein — tick Protein too, or they can't be written.")
            else:
                ctx["aa_note"] = "Amino acids can't be copied: neither food has a protein value to scale by."
            ctx["aa_alt"] = inc_scaled if own_scaled else {}
            has_some = any(not _data_completeness.is_blank(k, target_nutrients) for k in aa_keys)
            missing_some = any(_data_completeness.is_blank(k, target_nutrients) for k in aa_keys)
            if has_some and missing_some:
                ctx["aa_note"] += (" This food already has some amino acid values: filling only the"
                                   " missing ones mixes two sources, which can skew its profile a little.")
        elif aa_keys:
            compare_to = {k: v for k, v in raw.items() if not k.startswith("aa_")}
    if not ctx["error"]:
        review = _incoming_review.nutrient_review(target_nutrients, compare_to,
                                                  _EDIT_NUTRIENT_GROUPS, prefer_incoming=prefer_incoming,
                                                  estimated=estimated if source == "usda" else frozenset(),
                                                  mine=mine)
        ctx.update(review)
        ctx["meta_rows"] = (_incoming_review.meta_review(dict(target), incoming, prefer_incoming=prefer_incoming,
                                                         mine=mine)
                            if source == "usda" else [])
        ctx["portion_rows"] = (_incoming_review.new_portions(target_portions, incoming.get("portions"))
                               if source == "usda" else [])
        ctx["incoming_json"] = json.dumps(incoming)
        if source == "usda":
            ctx["today"] = datetime.date.today().isoformat()
            with _db.get_db() as conn:
                ctx["meal_items_before_today"] = _db.meal_items_before(conn, fdc_id, ctx["today"])
        ctx["edited"] = edited
        ctx["prefer_incoming"] = prefer_incoming
    return templates.TemplateResponse(request, "food_review_incoming.html", ctx)


@app.post("/food/{fdc_id}/review-incoming", response_class=RedirectResponse)
async def food_review_incoming_apply(request: Request, fdc_id: int):
    """Write the values ticked on the review screen. Nutrients go in through
    merge_user_supplied_nutrients (only the ticked keys, other values left
    alone); descriptive fields through update_food_fields; incoming portions
    are appended, never replacing the food's own. A fill from another food
    is the user's edit; a USDA refresh makes USDA's fresh copy the food's
    source copy (db.rebase_food_source), so user-edited then means exactly
    "some value still differs from USDA's"."""
    form = await request.form()
    source = "food" if form.get("source") == "food" else "usda"
    next_url = _local_next(form.get("next") or "", f"/food/{fdc_id}")
    try:
        incoming = json.loads(form.get("incoming_json") or "{}")
    except ValueError:
        incoming = {}
    inc_nutrients = incoming.get("nutrients") or {}
    chosen: dict[str, float] = {}
    for key in form.getlist("keys"):
        if key in _ALL_NUTRIENT_KEYS and key in inc_nutrients:
            try:
                chosen[key] = float(inc_nutrients[key])
            except (TypeError, ValueError):
                pass
    fields: dict = {}
    if source == "usda":
        for key in form.getlist("meta"):
            if key in dict(_incoming_review.META_FIELDS) and incoming.get(key) not in (None, ""):
                fields[key] = incoming[key]
    impact_targets = _impact_targets([fdc_id]) if chosen else ([], [])
    impact_before = _impact_snapshot(*impact_targets) if chosen else {}
    # "Keep the current version for past meals": before anything is written,
    # the food's values as they are become an older version that meals
    # dated before keep_before now point at (db.create_food_version).
    keep_before = (form.get("keep_before") or "").strip() if form.get("keep_version") else ""
    if keep_before:
        try:
            keep_before = datetime.date.fromisoformat(keep_before).isoformat()
        except ValueError:
            keep_before = ""
    kept = None
    with _db.get_db() as conn:
        target = _db.get_cached_food(conn, fdc_id)
        if not target:
            return RedirectResponse(next_url, status_code=303)
        if source == "usda" and keep_before and (chosen or form.getlist("meta") or form.getlist("portions")):
            kept = _db.create_food_version(conn, fdc_id, keep_before)
        if source == "usda":
            current_portions = json.loads(target["portions_json"] or "[]") or []
            offered = _incoming_review.new_portions(current_portions, incoming.get("portions"))
            picked = {d.strip().lower() for d in form.getlist("portions")}
            additions = [p for p in offered if str(p.get("description", "")).strip().lower() in picked]
            if additions:
                fields["portions"] = current_portions + additions
        note = None
        if source == "food" and chosen:
            # Re-scale ticked amino acids here, never trusting the screen:
            # to the incoming protein if Protein is ticked, else this food's.
            current = json.loads(target["nutrients_json"]) if target["nutrients_json"] else {}
            aa_chosen = [k for k in chosen if k.startswith("aa_")]
            notes = []
            if aa_chosen:
                protein_after = chosen.get("protein_g", current.get("protein_g"))
                scaled, factor = _aa_estimate.scaled_aa(inc_nutrients, protein_after)
                for k in aa_chosen:
                    if k in scaled:
                        chosen[k] = scaled[k]
                    else:
                        del chosen[k]
                if scaled and any(k in chosen for k in aa_chosen):
                    notes.append(_aa_estimate.source_note(incoming.get("name") or "another food",
                                                          form.get("source_fdc_id") or None, factor))
            labels = [label for _g, fs in _EDIT_NUTRIENT_GROUPS for k, label, _u in fs
                      if k in chosen and not k.startswith("aa_")]
            if labels:
                notes.insert(0, _aa_estimate.copy_nutrients_note(incoming.get("name") or "another food",
                                                                 form.get("source_fdc_id") or None, labels))
            note = "  |  ".join(notes) or None
        if chosen:
            _db.merge_user_supplied_nutrients(conn, fdc_id, chosen, overwrite=True, notes=note,
                                              mark_edited=(source == "food"))
            # Values borrowed from another food are estimates for this one;
            # USDA's own values are measured, so they clear the mark.
            if source == "food":
                _db.update_estimated_keys(conn, fdc_id, add=chosen.keys())
            else:
                _db.update_estimated_keys(conn, fdc_id, remove=chosen.keys())
        if fields:
            _db.update_food_fields(conn, fdc_id, **fields)
        if source == "usda":
            # Whatever was or wasn't taken, USDA's fresh copy is now the
            # source copy edits are measured against — so taking all of it
            # ends user-edited status, keeping some of your own doesn't.
            _db.rebase_food_source(conn, fdc_id, incoming)
        if chosen or fields:
            _recipe_dcp.cascade_food_change(fdc_id, conn)
    count = len(chosen) + len(fields) - ("portions" in fields) + len(additions if source == "usda" else [])
    impact = ""
    if chosen:
        impact = _impact_store(f"Updating {target['name']}", impact_before, _impact_snapshot(*impact_targets))
    if next_url == f"/food/{fdc_id}":
        next_url += f"?incoming_applied={count}" + (f"&impact={impact}" if impact else "")
        if kept:
            next_url += f"&version_kept={kept['fdc_id']}&version_moved={kept['meal_items']}"
    return RedirectResponse(next_url, status_code=303)


@app.get("/food/{fdc_id}/fill-from", response_class=HTMLResponse)
async def food_fill_from(request: Request, fdc_id: int, q: str = "",
                         source: list[str] | None = Query(default=None)):
    """Fill in nutrients from another food, for a food that isn't a custom
    profile (those have the same search on Edit Custom Profile). Search,
    compare checked results with this food, then review values to copy."""
    source = _resolve_source_filter(source, "sort_nutrient_source_filter", _SOURCE_PICKER_FILTERS)
    with _db.get_db() as conn:
        target = _db.get_cached_food(conn, fdc_id)
        if not target:
            return RedirectResponse("/food/cache", status_code=303)
        results = _search_food_sources(conn, q.strip(), fdc_id, source=source) if q.strip() else []
    return templates.TemplateResponse(request, "food_fill_from.html", {
        "food": dict(target), "q": q.strip(), "results": results, "source": source,
        "source_filters": _SOURCE_PICKER_FILTERS, "source_labels": _SEARCH_SOURCE_LABELS,
        "omitted_sources": _omitted_source_labels(source, _SOURCE_PICKER_FILTERS),
    })


@app.post("/food/{fdc_id}/toggle-starter", response_class=RedirectResponse)
async def food_toggle_starter(fdc_id: int, next: str = Form("")):
    """Add or remove the "* " starter-data name prefix (see
    scripts/export_starter_data.py) on a food -- deliberately a plain rename
    (db.rename_cached_food), NOT a full update_cached_food_profile() edit,
    so marking a real USDA/OFF food as starter content doesn't also mark it
    user_drafted and block it from ever refreshing from USDA again.
    Curator-only: refused in the packaged program (see _is_curator())."""
    if not _is_curator():
        raise HTTPException(status_code=404, detail="Not found")
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        if cached is not None:
            name = cached["name"]
            new_name = name[1:].lstrip() if name.startswith("*") else f"* {name}"
            _db.rename_cached_food(conn, fdc_id, new_name)
    # The button lives on the Food Cache list; go back to the same row there.
    if next.startswith("/food/cache"):
        return RedirectResponse(next, status_code=303)
    return RedirectResponse(f"/food/{fdc_id}", status_code=303)


@app.get("/food/{fdc_id}/oxalate-link", response_class=HTMLResponse)
async def oxalate_link_get(request: Request, fdc_id: int, q: str | None = None):
    import oxalate as _ox
    with _db.get_db() as conn:
        food = _db.get_cached_food(conn, fdc_id)
        if food is None:
            raise HTTPException(status_code=404, detail="Food not found")
        link = _db.oxalate_link_get(conn, fdc_id)

    current_ox_row = None
    if link is not None and link["oxalate_food_id"]:
        with _ox.get_oxalate_db() as ox_conn:
            current_ox_row = _ox.get_by_id(ox_conn, link["oxalate_food_id"])

    query = q if q is not None else food["name"]
    candidates = []
    if query.strip():
        with _ox.get_oxalate_db() as ox_conn:
            candidates = [row for _score, row in _ox.search_similar(ox_conn, query, top_n=15)]

    return templates.TemplateResponse(request, "oxalate_link.html", {
        "food": food,
        "query": query,
        "candidates": candidates,
        "current_ox_row": current_ox_row,
        "current_confirmed": bool(link and link["user_confirmed"]),
        "current_no_match": bool(link and link["no_match"]),
        "format_oxalate": _ox.format_oxalate,
        "category_label": _ox.category_label,
    })


@app.post("/food/{fdc_id}/oxalate-link", response_class=RedirectResponse)
async def oxalate_link_post(
    fdc_id: int,
    choice: str = Form(...),
):
    with _db.get_db() as conn:
        if _db.get_cached_food(conn, fdc_id) is None:
            raise HTTPException(status_code=404, detail="Food not found")
        if choice == "no_match":
            _db.oxalate_link_save(conn, fdc_id, oxalate_food_id=None, no_match=True)
        else:
            _db.oxalate_link_save(conn, fdc_id, oxalate_food_id=int(choice), no_match=False)
    return RedirectResponse(f"/food/{fdc_id}", status_code=303)


def _food_available_sections(ctx: dict) -> list[str]:
    available = []
    if ctx.get("nutrient_sections"):
        available.append("nutrient_table")
    if ctx.get("gl_portion") is not None:
        available.append("glycemic_load")
    if ctx.get("protein"):
        available.append("protein_summary")
        available.append("protein_quality")
    if ctx.get("oxalate") or ctx.get("antinutrients"):
        available.append("antinutrients")
    complements = ctx.get("complements")
    if complements and not complements.get("no_data"):
        available.append("complements")
    return available


@app.get("/food/{fdc_id}/print", response_class=HTMLResponse)
async def food_print(
    request: Request,
    fdc_id: int,
    amount: float = Query(default=100.0, gt=0),
    portion_str: str = Query(default=""),
    sections: list[str] = Query(default=[]),
    sections_submitted: bool = Query(default=False),
    layout: str = Query(default=""),
    paper: str = Query(default=""),
    layout_submitted: bool = Query(default=False),
):
    ctx = _food_detail_context(fdc_id, amount, portion_str, [], [])
    if "error" in ctx:
        return templates.TemplateResponse(request, "search.html", {
            "results": [], "query": "", "error": ctx["error"],
        })

    # print.html renders GL from a {"total", "blockers"} dict, the same shape the
    # meal/day/recipe print pages pass; a single food's GL never has blockers,
    # since a missing GI simply means there is no GL to show at all.
    if ctx.get("gl_portion") is not None:
        ctx["gl"] = {"total": ctx["gl_portion"], "blockers": []}

    available = _food_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("food", available, sections, sections_submitted, prefs)
    layout_ctx = _print_sections.resolve_layout_context(layout, paper, layout_submitted, prefs)
    save_update = layout_ctx.pop("_save_update")
    if sections_submitted or save_update:
        _save_prefs_file({**_print_sections.save_sections("food", enabled, prefs), **save_update})

    subtitle_bits = [b for b in [ctx["food"].get("data_type"),
                                  f"{ctx['portion_label'] or (str(ctx['amount']) + ' g')}"] if b]

    return templates.TemplateResponse(request, "print.html", {
        "title":              ctx["food"]["name"],
        "subtitle":           " · ".join(subtitle_bits),
        "back_url":           f"/food/{fdc_id}",
        "back_label":         "Back to food",
        "fixed_params":       {"amount": amount, "portion_str": portion_str},
        "section_labels":     _print_sections.PRINT_SECTION_LABELS,
        "available_sections": available,
        "enabled":            enabled,
        **layout_ctx,
        **ctx,
    })


# ---------------------------------------------------------------------------
# Meal helpers
# ---------------------------------------------------------------------------

def _recipe_nutrients_per_serving(recipe_id: int, conn) -> dict:
    """Sum ingredient nutrients for one recipe, return per-serving totals. Handles nested recipes."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return {}
    servings = float(recipe["servings"] or 1)
    total = recipe_total_nutrients(recipe_id, conn)
    return {k: v / servings for k, v in total.items()} if servings else total


def _flatten_recipe_diaas_ingredients(recipe_id: int, conn, target_servings: float) -> list[dict]:
    """Build food-level dicts for a recipe's DIAAS pooling, treating any
    sub-recipe ingredient as one atomic food (see atomic_recipe_ingredients).
    target_servings: how many servings of this recipe to account for."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return []
    recipe_servings = float(recipe["servings"] or 1)
    return atomic_recipe_ingredients(recipe_id, conn, portion_factor=target_servings / recipe_servings)


def _build_diaas_display(diaas_result: dict | None) -> dict | None:
    """Build the full diaas_display dict from a meal_level_diaas result."""
    if not diaas_result or not diaas_result.get("diaas"):
        return None
    score = diaas_result["diaas"]
    total_p = diaas_result.get("total_protein_g", 0)
    if total_p <= 0:
        return None
    limiting_iaa_key = diaas_result.get("limiting_iaa")
    def _iaa_row(k, v):
        bar_pct = min(round(v / 1.5 * 100, 0), 100)
        is_lim = k == limiting_iaa_key
        if is_lim:
            color = "#ca8a04"   # deep yellow — limiting AA
        elif v >= 1.0:
            color = "#166534"   # dark green — met
        elif v >= 0.80:
            color = "#7f1d1d"   # deep dark red — near miss
        else:
            color = "#dc2626"   # medium red — gap
        return {"label": _usda.nutrient_label(k)[0], "ratio": round(v, 3),
                "met": v >= 1.0, "bar_pct": bar_pct, "bar_color": color,
                "is_limiting": is_lim}
    iaa_rows = sorted(
        [_iaa_row(k, v) for k, v in diaas_result.get("iaa_ratios", {}).items()],
        key=lambda r: r["label"],
    )
    eff_score = min(score, 1.0)
    ing_rows = []
    omitted_low_protein = False
    for ing in diaas_result.get("ingredients", []):
        p = ing.get("protein_g", 0.0)
        if p < 0.1:
            omitted_low_protein = True
            continue
        d = ing.get("digestibility", 1.0)
        has_aa = ing.get("has_aa_data", False)
        dig_p = p * d if has_aa else p
        src = ing.get("dig_source", "")
        src_tag = "user" if "user override" in src else ("~est" if "estimate" in src else "")
        ing_rows.append({
            "food_name":            ing.get("food_name", ""),
            "fdc_id":               ing.get("fdc_id"),
            "recipe_id":            ing.get("recipe_id"),
            "protein_g":            round(p, 1),
            "digestibility":        round(d, 2),
            "digestible_protein_g": round(dig_p, 1),
            "has_aa":               has_aa,
            "src_tag":              src_tag,
            "dcp_g":                round(p * eff_score, 1) if has_aa else None,
        })
    # Highest raw protein first. dcp_g is protein_g times one fixed meal-wide
    # score for every AA-having row, so sorting by protein already reproduces
    # DCP order there for free — and unlike dcp_g (None for no-AA-data foods),
    # protein_g is never missing, so a food that's a big protein contributor
    # but lacks AA data still surfaces near the top instead of at the bottom.
    ing_rows.sort(key=lambda r: r["protein_g"], reverse=True)
    aa_p = diaas_result.get("aa_protein_g") or total_p
    raw_dcp = diaas_result.get("digestible_complete_protein_g") or 0
    dcp_g = round(raw_dcp, 1)
    eff_pct = round(eff_score * 100, 0)
    aa_dig_p = diaas_result.get("aa_dig_protein_g")
    uncapped_dcp = aa_p * eff_score
    dcp_was_capped = aa_dig_p is not None and raw_dcp < uncapped_dcp - 0.05
    avg_digestibility = (aa_dig_p / aa_p) if (dcp_was_capped and aa_p > 0) else None
    protein_by_name = {
        ing.get("food_name", ""): ing.get("protein_g", 0.0)
        for ing in diaas_result.get("ingredients", [])
    }
    all_missing = diaas_result.get("missing_aa_names", [])
    missing_with_protein = [n for n in all_missing if protein_by_name.get(n, 0.0) >= 1.0]
    omitted_zero_protein_missing = len(missing_with_protein) < len(all_missing)
    return {
        "score":           round(score, 3),
        "total_protein_g": round(total_p, 1),
        "aa_protein_g":    round(aa_p, 1),
        "dcp_g":           dcp_g,
        "eff_pct":         eff_pct,
        "dcp_was_capped":  dcp_was_capped,
        "uncapped_dcp_g":  round(uncapped_dcp, 1),
        "avg_digestibility": round(avg_digestibility, 2) if avg_digestibility is not None else None,
        "limiting_label":  diaas_result.get("limiting_label"),
        "iaa_rows":        iaa_rows,
        "ing_rows":        ing_rows,
        "omitted_low_protein": omitted_low_protein,
        "missing":         missing_with_protein,
        "omitted_zero_protein_missing": omitted_zero_protein_missing,
        "has_complete":    diaas_result.get("has_complete_data", False),
        "phe_tyr_gap":     diaas_result.get("phe_tyr_gap", False),
    }


_REFERENCE_ADULT_PROTEIN_G = 56.0  # 0.8 g/kg × 70 kg WHO/FAO reference adult

def _protein_adequacy(nutrients: dict, diaas_dcp_g: float | None, rda: dict | None) -> dict:
    """Build protein adequacy dict. Uses DCP when available, else raw protein.
    Falls back to standard adult reference (56 g) when no profile is set."""
    if rda and rda.get("protein_g") and rda["protein_g"][0] > 0:
        target = rda["protein_g"][0]
        personal = True
    else:
        target = _REFERENCE_ADULT_PROTEIN_G
        personal = False
    # Both the value and its label key off the same test. Keying the value
    # off truthiness while the label used "is not None" meant a DCP of
    # exactly 0.0 — every contributing food lacking amino-acid data — showed
    # the raw protein figure under the "Digestible complete protein" label.
    intake = diaas_dcp_g if diaas_dcp_g is not None else nutrients.get("protein_g", 0.0)
    label = "Digestible complete protein" if diaas_dcp_g is not None else "Protein"
    pct = intake / target * 100.0
    return {"target": round(target, 1), "intake": round(intake, 1),
            "pct": round(pct, 0), "personal": personal, "label": label}


def _web_pantry_candidates() -> list[dict]:
    """Load pantry items as complement-suggestion candidates."""
    try:
        with _db.get_db() as conn:
            rows = _db.pantry_list(conn)
        candidates = []
        for row in rows:
            nutrients = None
            if row["fdc_id"] is not None:
                with _db.get_db() as conn:
                    cached = _db.get_cached_food(conn, row["fdc_id"])
                if cached and cached["nutrients_json"]:
                    nutrients = json.loads(cached["nutrients_json"])
            candidates.append({
                "name":      row["food_name"] or "",
                "fdc_id":    row["fdc_id"],
                "nutrients": nutrients,
                "diaas":     _usda.get_diaas(row["food_name"] or ""),
            })
        return candidates
    except Exception:
        return []


def _web_recipe_candidates(exclude_recipe_id: int | None = None) -> list[dict]:
    """Return analyzed recipes as complement-suggestion candidates.

    `exclude_recipe_id` leaves a recipe out of its own candidate list when
    suggesting complements for that same recipe.
    """
    try:
        with _db.get_db() as conn:
            rows = conn.execute(
                "SELECT id, name, servings, dcp_g, total_weight, total_weight_unit, nutrients_json"
                " FROM recipes WHERE nutrients_json IS NOT NULL"
            ).fetchall()
    except Exception:
        return []

    candidates: list[dict] = []
    for row in rows:
        if exclude_recipe_id is not None and row["id"] == exclude_recipe_id:
            continue
        try:
            nutrients = json.loads(row["nutrients_json"])
        except Exception:
            continue
        if not nutrients:
            continue

        servings = row["servings"] or 1
        try:
            total_weight = float(row["total_weight"]) if row["total_weight"] else None
        except Exception:
            total_weight = None
        serving_weight_g = (total_weight / servings) if total_weight else None

        diaas_val: float | None = None
        dcp_g = row["dcp_g"]
        if dcp_g and serving_weight_g and nutrients.get("protein_g", 0) > 0:
            protein_per_serving = nutrients["protein_g"] * serving_weight_g / 100
            if protein_per_serving > 0:
                diaas_val = min(1.0, dcp_g / protein_per_serving)

        candidates.append({
            "name": row["name"],
            "fdc_id": None,
            "recipe_id": row["id"],
            "nutrients": nutrients,
            "diaas": diaas_val,
            "serving_weight_g": serving_weight_g,
        })
    return candidates


_COMP_SORT_MODES = {"dcp", "digestible_protein", "gap_effect", "grams"}
_DIAAS_SORT_MODES = {"effect", "grams"}


def _complement_suggestions(
    aa_nutrients: dict,
    pooled_tid: float | None,
    context: str = "meal",
    exclude_recipe_id: int | None = None,
    ingredients: list[dict] | None = None,
    exclude_names: set[str] | None = None,
    comp_sort: str | None = None,
    diaas_sort: str | None = None,
    anchor_overrides: dict[str, float] | None = None,
) -> dict:
    """Build complement suggestion data. Returns no_data sentinel if AA data unavailable.

    context: "meal", "daily", "food", or "recipe" — controls the max serving cap
        for DIAAS-booster steps (120 g for meal/daily/food, 300 g for recipe).
    exclude_recipe_id: when context is "recipe", pass that recipe's own id so it
        never appears as a complement candidate for itself.

    pooled_tid: protein-weighted average TRUE digestibility across the base's
        ingredients — see diaas.pooled_tid() — passed through as the digestibility
        basis so gaps/DCP projections use the real baseline. Do NOT pass the
        meal's composite DIAAS here instead: DIAAS is the worst-case (limiting)
        AA ratio, and reapplying it as a flat per-AA
        multiplier manufactures gaps in amino acids that were never actually short
        — for a meal with one badly-imbalanced AA and otherwise-fine ones, this can
        make every candidate look unable to close the gap in any practical serving.
        Without pooled_tid, gaps/DCP projections default to digestibility=1.0, which
        overstates the DCP a suggested addition will actually achieve.

    ingredients: the base's real per-food breakdown (food_name/nutrients_100g/grams),
        on the SAME basis/scale as aa_nutrients, when the caller has one. Passed
        through to build_complement_display so DCP-achieved figures are computed by
        an exact diaas.meal_level_diaas recompute rather than approximated with a
        flat digestibility ratio. Must not be passed if its scale doesn't match
        aa_nutrients (e.g. per-serving aa_nutrients with whole-recipe ingredients) —
        that would silently produce a wrong "exact" number instead of a labeled
        estimate, so callers should only wire this through on a basis-matched path.
    """
    prefs = _load_prefs_file()
    diet_pref = prefs.get("diet_pref", "all")
    pantry = _web_pantry_candidates() + _web_recipe_candidates(exclude_recipe_id)
    cache_candidates = _complements.load_cache_candidates({c["name"].lower() for c in pantry})
    max_improver_grams = 300 if context == "recipe" else 120
    digestibility = min(pooled_tid, 1.0) if pooled_tid else 1.0
    comp_sort = comp_sort or _resolve_sort(None, "sort_complements", "dcp", _COMP_SORT_MODES)
    diaas_sort = diaas_sort or _resolve_sort(None, "sort_diaas_improvers", "effect", _DIAAS_SORT_MODES)
    return _complements.build_complement_display(
        aa_nutrients, pantry, diet_pref=diet_pref,
        digestibility=digestibility, max_improver_grams=max_improver_grams,
        ingredients=ingredients,
        cache_candidates=cache_candidates,
        exclude_names=exclude_names,
        comp_sort=comp_sort,
        diaas_sort=diaas_sort,
        anchor_overrides=anchor_overrides,
    )


def _recipe_gl_web(recipe_id: int, recipe_servings: float, servings: float) -> dict:
    """Glycemic load for a recipe portion. Returns {"total": float_or_None, "blockers": list}.

    Sub-recipe ingredients use the sub-recipe's own precomputed GL (gl_g) via
    compute_glycemic_load(), rather than always blocking on them."""
    with _db.get_db() as conn:
        ingredients = _db.recipe_get_ingredients(conn, recipe_id)
        line_items = [
            {
                "kind":      "recipe" if ing["ref_recipe_id"] else "food",
                "name":      ing["food_name"],
                "amount":    ing["amount"],
                "fdc_id":    ing["fdc_id"],
                "recipe_id": ing["ref_recipe_id"],
            }
            for ing in ingredients
        ]
        gl_total, blockers = compute_glycemic_load(line_items, conn)
    if blockers:
        return {"total": None, "blockers": blockers}
    gl_portion = round(gl_total / recipe_servings * servings, 1) if recipe_servings > 0 else round(gl_total, 1)
    return {"total": gl_portion, "blockers": []}


def _compute_gl(meal_id: int) -> tuple[float | None, list[str]]:
    """Glycemic load for a single meal. Returns (gl_total_or_None, blocker_names).

    Recipe items use the recipe's own precomputed GL (gl_g) via
    compute_glycemic_load(), rather than always blocking on them."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
        line_items = [
            {
                "kind":      "recipe" if item["item_type"] == "recipe" else "food",
                "name":      item["food_name"],
                "amount":    item["amount"],
                "fdc_id":    item["fdc_id"],
                "recipe_id": item["recipe_id"],
            }
            for item in items
        ]
        gl_total, blockers = compute_glycemic_load(line_items, conn)
    return (None if blockers else round(gl_total, 1), blockers)


def _recipe_aa_status(recipe_ids) -> dict[int, str]:
    """AA-column status per recipe id, for search-result rows.

    A recipe has no nutrients dict of its own to hand aa_indicator(), so the
    status is derived from its expanded ingredient totals. Recipe rows used to
    carry no "aa" key at all (or, on Food Search, a dcp_g stand-in that said
    nothing about AA data), leaving the column blank for recipes that do have
    amino acid data.
    """
    with _db.get_db() as conn:
        return {rid: recipe_aa_indicator(rid, conn) for rid in recipe_ids}


def _expand_recipe_ingredients(recipe_id: int, portion_factor: float, conn) -> list[dict]:
    """Recursively expand a recipe's ingredients for DIAAS, scaling by portion_factor.
    Thin positional-argument wrapper — the recursion itself lives in
    numa_app.services.recipe_nutrients."""
    return expand_recipe_ingredients(recipe_id, conn, portion_factor=portion_factor)


def _meal_aa_nutrients(meal_id: int) -> dict:
    """Return summed nutrients (scaled) from foods that have AA data, for complement suggestions.
    Expands recipe items recursively and applies complement-table AA fallback."""
    result: dict = {}
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
        for row in items:
            if row["item_type"] == "food" and row["fdc_id"]:
                cached = _db.get_cached_food(conn, row["fdc_id"])
                if not cached or not cached["nutrients_json"]:
                    continue
                nuts = best_aa_nutrients(json.loads(cached["nutrients_json"]), row["food_name"])
                if nuts:
                    scaled = _usda.scale_nutrients(nuts, float(row["amount"]))
                    for k, v in scaled.items():
                        result[k] = result.get(k, 0.0) + v
            elif row["item_type"] == "recipe" and row["recipe_id"]:
                recipe = _db.recipe_get(conn, row["recipe_id"])
                if not recipe:
                    continue
                recipe_servings = float(recipe["servings"] or 1)
                portion_factor = float(row["amount"]) / recipe_servings
                for ing in _expand_recipe_ingredients(row["recipe_id"], portion_factor, conn):
                    nuts = best_aa_nutrients(ing["nutrients_100g"], ing["food_name"])
                    if nuts:
                        scaled = _usda.scale_nutrients(nuts, ing["grams"])
                        for k, v in scaled.items():
                            result[k] = result.get(k, 0.0) + v
    return result


# ── Change impact ("what this change did") ───────────────────────────────
# After a food's data or an amount is corrected, the page shows which
# recipes and logged meals moved and by how much — the payoff of fixing data,
# made visible. Before/after totals are computed live; the summary rides to
# the next page under a one-time token (single-user app, so an in-process
# dict is enough; a stale token just shows nothing).
_IMPACT_KEYS = (("calories", "kcal", 0.5), ("protein_g", "g protein", 0.05),
                ("carbs_g", "g carbs", 0.05), ("fat_g", "g fat", 0.05))
_IMPACTS: dict[str, dict] = {}


def _impact_targets(fdc_ids) -> tuple[list[int], list[int]]:
    recipe_ids, meal_ids = set(), set()
    with _db.get_db() as conn:
        for fid in fdc_ids:
            recipe_ids.update(_db.recipes_using_food(conn, fid))
            meal_ids.update(_db.meals_using_food(conn, fid))
    return sorted(recipe_ids), sorted(meal_ids)


def _impact_snapshot(recipe_ids, meal_ids) -> dict:
    snap = {}
    with _db.get_db() as conn:
        for rid in recipe_ids:
            r = _db.recipe_get(conn, rid)
            if r:
                snap[("recipe", rid)] = {"label": r["name"],
                                         "values": _recipe_nutrients_per_serving(rid, conn)}
        meals = {mid: _db.meal_get(conn, mid) for mid in meal_ids}
    for mid, m in meals.items():
        if m:
            _items, totals, _d, _i = _meal_totals(mid)
            snap[("meal", mid)] = {"label": f"{m['meal_date']} {m['name']}", "values": totals}
    return snap


def _impact_store(title: str, before: dict, after: dict) -> str:
    """Diff two _impact_snapshot()s; keep the summary and return its token
    ("" when nothing moved)."""
    rows = {"recipe": [], "meal": []}
    for key, b in before.items():
        a = after.get(key)
        if not a:
            continue
        changes = []
        for nk, unit, eps in _IMPACT_KEYS:
            old, new = float(b["values"].get(nk) or 0), float(a["values"].get(nk) or 0)
            if abs(new - old) >= eps:
                changes.append({"unit": unit, "old": old, "new": new})
        if changes:
            kcal = next((c for c in changes if c["unit"] == "kcal"), None)
            rows[key[0]].append({"id": key[1], "label": b["label"], "changes": changes,
                                 "weight": abs(kcal["new"] - kcal["old"]) if kcal else 0})
    if not rows["recipe"] and not rows["meal"]:
        return ""
    for k in rows:
        rows[k].sort(key=lambda r: -r["weight"])
    import secrets
    token = secrets.token_urlsafe(8)
    if len(_IMPACTS) > 50:
        _IMPACTS.clear()
    _IMPACTS[token] = {"title": title, "recipes": rows["recipe"], "meals": rows["meal"]}
    return token


def _impact_pop(token: str) -> dict | None:
    return _IMPACTS.pop(token, None) if token else None


def _recalc_notes(meal_ids) -> list[dict]:
    """Why these meals' totals were last recalculated without the meal
    itself being edited (db.meal_recalc_log), newest first, for the small
    note on meal and Daily Summary pages."""
    with _db.get_db() as conn:
        rows = _db.meal_recalc_notes(conn, meal_ids)
    return [{"reason": r["reason"], "date": (r["logged_at"] or "")[:10]} for r in rows]


def _added_food_check(conn, fdc_id: int) -> str:
    """The `added_check` value to put on the redirect after adding a food to
    a meal or recipe: its id when the food has a data problem worth saying
    so right then (data_quality.food_issues — not mere estimates), else ""."""
    issues = _data_quality.issues_for_food(conn, fdc_id)
    return str(fdc_id) if any(i["severity"] == "problem" for i in issues) else ""


def _added_food_note(added_check: str) -> dict:
    """Template context for _food_quality_note.html after an add."""
    if not added_check.lstrip("-").isdigit():
        return {}
    fid = int(added_check)
    with _db.get_db() as conn:
        food = _db.get_cached_food(conn, fid)
        issues = _data_quality.issues_for_food(conn, fid) if food else []
    if not issues:
        return {}
    return {"quality_issues": issues, "quality_food": {"fdc_id": fid, "name": food["name"]}}


def _calorie_warnings(ingredients: list[dict]) -> dict | None:
    """The calorie-quality note above a meal's/recipe's/day's Nutritional
    Analysis table (_calorie_note.html), or None when every food's calories
    are sound. "items": foods whose calories are "missing" (no value — those
    grams add 0 kcal), "estimated" (filled from protein/carbs/fat, see
    energy_check.py) or "mismatch" (far from what the macros imply);
    "estimated_pct": share of the calorie total that is estimated — the
    trust figure the note leads with. `ingredients` are leaf foods as
    _meal_expand_for_diaas / expand_recipe_ingredients build them; repeats
    are merged first."""
    leaves = [i for i in _group_ingredients_by_food(ingredients) if i.get("fdc_id")]
    if not leaves:
        return None
    with _db.get_db() as conn:
        estimated = {i["fdc_id"]: _db.estimated_keys(conn, i["fdc_id"]) for i in leaves}
        ignores = _db.food_data_ignores(conn)
    out, total_kcal, est_kcal = [], 0.0, 0.0
    for ing in leaves:
        n = ing.get("nutrients_100g") or {}
        grams = float(ing.get("grams") or 0)
        kcal = float(n.get("calories") or 0) * grams / 100
        total_kcal += kcal
        if "macros" in ignores.get(ing["fdc_id"], set()):
            continue
        expected = _energy_check.atwater_estimate(n)
        kind = None
        if _energy_check.calories_missing(n):
            kind = "missing"
        elif "calories" in estimated.get(ing["fdc_id"], set()):
            kind = "estimated"
            est_kcal += kcal
        elif (_energy_check.calorie_mismatch(n) and expected is not None
              and abs(kcal - expected * grams / 100) >= _energy_check.NOTE_MIN_KCAL):
            kind = "mismatch"
        if kind:
            out.append({"fdc_id": ing["fdc_id"], "name": ing["food_name"], "kind": kind,
                        "grams": grams, "kcal": kcal,
                        "expected_kcal": expected * grams / 100 if expected is not None else None})
    if not out:
        return None
    out.sort(key=lambda w: ("missing", "mismatch", "estimated").index(w["kind"]))
    return {"items": out, "total_kcal": total_kcal,
            "estimated_pct": est_kcal / total_kcal * 100 if total_kcal else 0.0}


def _group_ingredients_by_food(ingredients: list[dict]) -> list[dict]:
    """Merge ingredient dicts that refer to the same food (same fdc_id, or
    same food_name when fdc_id is absent), summing their grams.

    Without this, a food logged/used more than once (e.g. the same fruit
    eaten twice in one meal, or appearing both standalone and inside a
    recipe) shows up as separate rows in Top Contributors and the
    Meal-Level Protein Analysis breakdown instead of one combined row."""
    grouped: dict[object, dict] = {}
    order: list[object] = []
    for ing in ingredients:
        key = ing.get("fdc_id") or ing["food_name"].lower()
        if key not in grouped:
            grouped[key] = dict(ing)
            order.append(key)
        else:
            grouped[key]["grams"] += ing["grams"]
    return [grouped[k] for k in order]


def _serving_weight_changed(logged: float | None, now: float | None) -> bool:
    """True when a logged recipe serving's gram weight and the recipe's
    current one are both known and differ by more than rounding noise."""
    if logged is None or now is None:
        return False
    return abs(now - logged) > max(0.5, 0.01 * logged)


def _annotate_recipe_amounts(items: list[dict], conn, *, id_key: str = "id") -> bool:
    """Give each recipe item in `items` what the shared recipe_amount() macro
    (templates/_recipe_amount.html) needs to show servings AND grams:
    serving_g (one serving's weight now, or None if it can't be worked out —
    see recipe_serving_grams()), grams (the logged amount's total weight, or
    None), and serving_changed ({"logged", "now"} when the serving weight has
    changed since the item was logged, else None).

    A meal stores recipe amounts in servings, so a later change to the
    recipe's servings count or total weight silently changes how much food a
    logged serving means. meal_items.serving_grams records the weight at log
    time; when it's missing (logged before this existed, or added by any path
    that doesn't set it) the current weight is recorded here, lazily, which
    is why this takes a writable connection. Returns True if any item is a
    recipe, so pages know to show the recipe-weight footnote."""
    any_recipe = False
    cache: dict[int, float | None] = {}
    for it in items:
        if it.get("item_type", "recipe" if it.get("recipe_id") else "food") != "recipe" or not it.get("recipe_id"):
            continue
        any_recipe = True
        rid = it["recipe_id"]
        if rid not in cache:
            cache[rid] = recipe_serving_grams(rid, conn) if _db.recipe_get(conn, rid) else None
        now = cache[rid]
        logged = it.get("serving_grams")
        if logged is None and now is not None and it.get(id_key):
            _db.meal_item_set_serving_grams(conn, it[id_key], now)
            logged = now
        amount = float(it.get("amount") or 0)
        it["serving_g"] = now
        it["grams"] = now * amount if now is not None else None
        it["serving_changed"] = (
            {"logged": logged, "now": now} if _serving_weight_changed(logged, now) else None
        )
    return any_recipe


def _annotate_food_amounts(items: list[dict], conn, *, unit_key: str = "unit") -> None:
    """Give each logged food in `items` (meal_items rows, which store the
    grams in amount and what was typed in unit — "1/3 c", "2 × large egg",
    or just "g" for entries made before meals kept it) what the shared
    _food_amount.html macro needs: typed_note (the typed amount when it was
    more than grams, else None), amount_display (re-parseable text for the
    Edit box) and generic_density (the "≈ generic" mark, see
    _mark_generic_density())."""
    for it in items:
        if it.get("recipe_id") or not it.get("fdc_id"):
            continue
        typed = it.get(unit_key)
        label = _ingredient_amount_display(conn, {"unit": typed, "amount": it.get("amount"),
                                                  "food_name": it.get("food_name") or "",
                                                  "fdc_id": it["fdc_id"]})
        it["typed_note"] = _typed_amount_note(label)
        cached = _db.get_cached_food(conn, it["fdc_id"])
        portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
        # A portion label ("2 × 1 large egg") doesn't parse back, so the Edit
        # box falls back to grams rather than offer text it would reject.
        reparses = _parse_portion_str(label, portions, it.get("food_name") or "")[0] is not None
        it["amount_display"] = label if reparses else f"{float(it.get('amount') or 0):.4g} g"
        it["generic_density"] = (_generic_density_kind(typed, portions, cached["name"])
                                 if cached and typed else None)


def _meal_expand_for_diaas(meal_id: int, conn) -> tuple[list, dict, list]:
    """Return (items_for_display, total_nutrients, diaas_ingredients) for one meal.

    Shared by _meal_totals (per-meal DIAAS) and _day_analysis (day-level pooled
    DIAAS across every meal on a date) — both need the same per-item nutrient
    scaling and recipe-ingredient expansion; only what they do with the result
    (compute DIAAS per meal vs. accumulate across meals first) differs."""
    raw_items = _db.meal_get_items(conn, meal_id)
    items = []
    ingredients = []
    total_nutrients: dict = {}

    for row in raw_items:
        if row["item_type"] == "food" and row["fdc_id"]:
            cached = _db.get_cached_food(conn, row["fdc_id"])
            nuts_100g = json.loads(cached["nutrients_json"]) if cached and cached["nutrients_json"] else {}
            portions = json.loads(cached["portions_json"]) if cached and cached["portions_json"] else []
            grams = float(row["amount"])
            scaled = _usda.scale_nutrients(nuts_100g, grams)
            for k, v in scaled.items():
                total_nutrients[k] = total_nutrients.get(k, 0.0) + v
            items.append({
                "id":        row["id"],
                "food_name": row["food_name"],
                "fdc_id":    row["fdc_id"],
                "recipe_id": None,
                "amount":    grams,
                "unit":      "g",
                "typed_unit": row["unit"],
                "notes":     row["notes"] or "",
                "has_nuts":  bool(nuts_100g),
                "portions":  portions,
            })
            if nuts_100g:
                ingredients.append({
                    "food_name":      row["food_name"],
                    "fdc_id":         row["fdc_id"],
                    "nutrients_100g": nuts_100g,
                    "grams":          grams,
                })

        elif row["item_type"] == "recipe" and row["recipe_id"]:
            servings_consumed = float(row["amount"])
            recipe = _db.recipe_get(conn, row["recipe_id"])
            total_servings = float(recipe["servings"] or 1) if recipe else 1.0
            portion_factor = servings_consumed / total_servings
            per_serving = _recipe_nutrients_per_serving(row["recipe_id"], conn)
            scaled = {k: v * servings_consumed for k, v in per_serving.items()}
            for k, v in scaled.items():
                total_nutrients[k] = total_nutrients.get(k, 0.0) + v
            # Expand recipe ingredients into DIAAS ingredient list (handles sub-recipes)
            ingredients.extend(_expand_recipe_ingredients(row["recipe_id"], portion_factor, conn))
            items.append({
                "id":             row["id"],
                "food_name":      row["food_name"],
                "fdc_id":         None,
                "recipe_id":      row["recipe_id"],
                "amount":         servings_consumed,
                "unit":           "serving" + ("s" if servings_consumed != 1 else ""),
                # "grams"/"serving_g"/"serving_changed" are filled in by
                # _annotate_recipe_amounts() below.
                "notes":          row["notes"] or "",
                "has_nuts":       bool(per_serving),
                "recipe_deleted": recipe is None,
                "item_type":      "recipe",
                "serving_grams":  row["serving_grams"],
            })

    _annotate_recipe_amounts(items, conn)
    _annotate_food_amounts(items, conn, unit_key="typed_unit")
    return items, total_nutrients, _group_ingredients_by_food(ingredients)


def _meal_totals(meal_id: int) -> tuple[list, dict, dict | None, list]:
    """Return (items_with_nutrients, total_nutrients, diaas_result, ingredients)."""
    with _db.get_db() as conn:
        items, total_nutrients, ingredients = _meal_expand_for_diaas(meal_id, conn)
        diaas_result = None
        if ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(ingredients, conn)
            except Exception:
                pass

    return items, total_nutrients, diaas_result, ingredients


# ---------------------------------------------------------------------------
# Meal routes
# ---------------------------------------------------------------------------

def _compute_and_store_meal_bcp(meal_id: int) -> float | None:
    """Compute DIAAS-based DCP and calories for a meal and persist them. Returns dcp_g or None.

    Falls back to summing recipe items' precomputed dcp_g when ingredient-level
    AA data is unavailable."""
    _, total_nutrients, diaas_result, _ = _meal_totals(meal_id)
    diaas = _build_diaas_display(diaas_result)
    bcp_g = diaas["dcp_g"] if diaas else None
    calories = total_nutrients.get("calories") if total_nutrients else None
    with _db.get_db() as conn:
        if bcp_g is None:
            bcp_g = recipe_dcp_fallback(meal_id, conn)
        _db.meal_set_bcp(conn, meal_id, bcp_g, calories, total_nutrients)
    return bcp_g


def _refresh_stale_meals() -> None:
    """Recompute and persist DCP/calories/nutrient snapshot for every meal in
    stale_meals — flagged when a food it logs (directly or inside a recipe)
    or a recipe it logs (directly or as a sub-recipe) changed — then refresh
    % goal for each affected date. Each meal's flag is cleared before it's
    recomputed, and a failure is logged to recompute_errors rather than
    raised, so one bad meal can't block every page load forever."""
    with _db.get_db() as conn:
        stale_ids = _db.stale_meal_ids(conn)
    if not stale_ids:
        return
    dates = set()
    for meal_id in stale_ids:
        with _db.get_db() as conn:
            _db.clear_stale_meal(conn, meal_id)
            meal = _db.meal_get(conn, meal_id)
        if meal is None:
            continue
        try:
            _compute_and_store_meal_bcp(meal_id)
        except Exception as exc:
            with _db.get_db() as conn:
                _db.log_recompute_error(conn, "meal", meal_id, f"Meal recompute after a food/recipe change failed: {exc}")
            continue
        dates.add(meal["meal_date"])
    for meal_date in dates:
        _refresh_day_pct_goal(meal_date)


def _refresh_day_pct_goal(meal_date: str) -> None:
    """Recompute day_pct_goal for every meal on meal_date from stored bcp_g,
    against the profile pinned to that date (not whatever is active now).

    Includes meals not yet marked complete — DCP is auto-saved as items are
    added, so an in-progress meal already contributes to the day total
    (matches the day-detail page's own pooled DIAAS analysis, and
    db.meal_dates_with_bcp's day_bcp aggregate used by the Daily Summary
    Recent Days table)."""
    with _db.get_db() as conn:
        date_rows = _db.meal_list_by_date(conn, meal_date)
        protein_target = _day_profile.protein_target_for_date(conn, meal_date, diet_pref=_current_diet_pref())
    vals = [r["bcp_g"] for r in date_rows if r["bcp_g"] is not None]
    if not vals or not protein_target:
        pct = None
    else:
        pct = round(sum(vals) / protein_target * 100, 1)
    for dr in date_rows:
        with _db.get_db() as conn:
            _db.meal_set_day_pct_goal(conn, dr["id"], pct)


def _meals_list_ctx(meals_rows, limit: int, total: int, before_date: str | None, sort: str = "date") -> dict:
    """Build template context for the meals list, including day DCP aggregates."""
    meals = [dict(m) for m in meals_rows]
    hidden = max(0, total - len(meals))

    # Extra user-chosen nutrient columns (stored in prefs.json). Drop
    # Calories — this list already shows it via its own fixed column below,
    # so picking it here too would just duplicate it (Recent Days, sharing
    # this same picker, still shows it if chosen — see MEALS_LIST_FIXED_KEYS).
    from numa_app.services.meal_list_columns import (
        saved_or_default as _saved_or_default_meal_nutrients, label_for as _meal_label_for, format_value as _meal_format_value,
        MEALS_LIST_FIXED_KEYS,
    )
    nutrient_keys = [k for k in _saved_or_default_meal_nutrients(_load_prefs_file())
                      if k not in MEALS_LIST_FIXED_KEYS]
    # "Raw protein" here (not just "Protein"), to distinguish it from the
    # digestibility-adjusted Meal/Day DCP columns shown alongside it — the
    # generic "Protein" label from label_for() is fine everywhere else.
    meal_nutrient_cols = [
        {"key": k, "label": "Raw protein (g)" if k == "protein_g" else _meal_label_for(k)}
        for k in nutrient_keys
    ]
    for m in meals:
        snapshot = json.loads(m["nutrients_snapshot_json"]) if m.get("nutrients_snapshot_json") else None
        m["nutrient_values"] = {
            k: (_meal_format_value(k, snapshot[k]) if snapshot and snapshot.get(k) is not None else None)
            for k in nutrient_keys
        }

    # Build day DCP totals from persisted bcp_g (any meal with a computed
    # value counts — DCP is auto-saved as items are added, regardless of
    # whether the meal has been marked complete). A day is flagged
    # provisional if any contributing meal is still incomplete, so the
    # template can mark the total as subject to change.
    dates_in_page = {m["meal_date"] for m in meals}
    day_bcp: dict[str, float | None] = {}
    day_provisional: dict[str, bool] = {}
    # Each date's % goal is scored against the profile pinned to *that* date,
    # not whatever profile is active now — dates in the same page can span a
    # profile switch.
    day_protein_target: dict[str, float | None] = {}
    day_profile_name: dict[str, str | None] = {}
    diet_pref = _current_diet_pref()
    for d in dates_in_page:
        with _db.get_db() as conn:
            date_rows = _db.meal_list_by_date(conn, d)
            day_protein_target[d] = _day_profile.protein_target_for_date(conn, d, diet_pref=diet_pref)
            dp_row = _db.day_profile_get(conn, d)
        day_profile_name[d] = dp_row["profile_name"] if dp_row else None
        contributing = [r for r in date_rows if r["bcp_g"] is not None]
        vals = [r["bcp_g"] for r in contributing]
        day_bcp[d] = round(sum(vals), 1) if vals else None
        day_provisional[d] = any(not r["complete"] for r in contributing)

    show_profile_col = len(_profile.list_profiles()) > 1
    show_pct_col = any(v is not None for v in day_protein_target.values())
    # Cosmetic header figure only ("goal = N g/day") — per-row math always
    # uses each date's own target above, not this.
    header_protein_target = _load_rda()
    header_protein_target = (
        header_protein_target["protein_g"][0]
        if header_protein_target and header_protein_target.get("protein_g") and header_protein_target["protein_g"][0] > 0
        else None
    )

    # Tag each meal with first-of-date flag so template can place Day DCP correctly
    seen_dates: set[str] = set()
    for m in meals:
        d = m["meal_date"]
        m["first_of_date"] = d not in seen_dates
        seen_dates.add(d)
        m["day_bcp"] = day_bcp.get(d)
        m["day_provisional"] = day_provisional.get(d, False)
        m["day_profile_name"] = day_profile_name.get(d)
        target = day_protein_target.get(d)
        if target and day_bcp.get(d) is not None:
            m["day_pct"] = round(day_bcp[d] / target * 100, 0)  # type: ignore[operator]
        else:
            m["day_pct"] = None

    return {
        "meals":          meals,
        "total":          total,
        "hidden":         hidden,
        "limit":          limit,
        "today":          datetime.date.today().isoformat(),
        "date_filter":    before_date or "",
        "sort":           sort,
        "protein_target": header_protein_target,
        "show_pct_col":   show_pct_col,
        "show_profile_col": show_profile_col,
        "meal_nutrient_cols": meal_nutrient_cols,
    }


_MEALS_SORT_KEYS = {"date", "name", "meal_bcp", "calories"}


@app.get("/meals", response_class=HTMLResponse)
async def meals_list(request: Request, limit: int = 9, date: str = "", sort: str | None = None):
    sort = _resolve_sort(sort, "sort_meals", "date", _MEALS_SORT_KEYS)
    before_date = date.strip() or None
    limit = max(1, limit)
    with _db.get_db() as conn:
        meals_rows = _db.meal_list_recent(conn, limit=limit, before_date=before_date, sort=sort)
        total = _db.meal_count_recent(conn, before_date=before_date)
    return templates.TemplateResponse(request, "meals.html",
                                      _meals_list_ctx(meals_rows, limit, total, before_date, sort))


@app.post("/meals/compute-bcp", response_class=RedirectResponse)
async def meals_compute_bcp(redirect_to: str = Form("/meals"), scope: str = Form("all")):
    """Recompute and persist DCP + calories for complete meals in the chosen scope
    (all meals and days / last 30 days / last 10 days)."""
    with _db.get_db() as conn:
        if scope == "30":
            since = (datetime.date.today() - datetime.timedelta(days=29)).isoformat()
            to_compute = _db.meal_list_complete_since(conn, since)
        elif scope == "10":
            since = (datetime.date.today() - datetime.timedelta(days=9)).isoformat()
            to_compute = _db.meal_list_complete_since(conn, since)
        else:
            to_compute = _db.meal_list_complete(conn)

    for meal in to_compute:
        _compute_and_store_meal_bcp(meal["id"])

    # Each affected date is scored against its own pinned profile, not
    # whatever profile is active now — a bulk recompute spanning many days
    # must not silently reattribute old days to today's profile.
    affected_dates = {meal["meal_date"] for meal in to_compute}
    for meal_date in affected_dates:
        _refresh_day_pct_goal(meal_date)

    return RedirectResponse(redirect_to, status_code=303)


@app.post("/meals/create", response_class=RedirectResponse)
async def meal_create(
    name: str = Form(""),
    meal_date: str = Form(""),
):
    name = name.strip() or "Meal"
    meal_date = meal_date.strip() or datetime.date.today().isoformat()
    with _db.get_db() as conn:
        meal_id = _db.meal_create(conn, name, meal_date)
        _day_profile.ensure_day_profile(conn, meal_date)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/refresh-aa", response_class=RedirectResponse)
async def meal_refresh_aa(meal_id: int):
    """Fetch AA nutrient data from USDA for all foods in this meal that lack
    it — or whose amino acids are only estimates (db.estimated_keys), which
    USDA's measured values replace. Otherwise fills blanks only."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
    filled, differs = 0, []
    for item in items:
        if item["item_type"] != "food" or not item["fdc_id"]:
            continue
        fdc_id = item["fdc_id"]
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if not cached or cached["user_drafted"]:
            continue
        data_type = cached["data_type"] or ""
        if data_type == "Branded":
            continue
        nutrients = json.loads(cached["nutrients_json"])
        with _db.get_db() as conn:
            estimated = _db.estimated_keys(conn, fdc_id)
        estimated_aa = {k for k in estimated if k.startswith("aa_")}
        if _usda.has_confirmed_aa_data(nutrients) and not estimated_aa:
            continue
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception:
            continue
        incoming = detail.get("nutrients", {}) or {}
        if not _usda.has_amino_acid_data(incoming):
            continue
        # Fill blanks only — never overwrite a value the food already has
        # (it may be the user's own edit). Foods where USDA's copy also
        # differs on existing values are listed for a per-value review.
        review = _incoming_review.nutrient_review(nutrients, incoming, _EDIT_NUTRIENT_GROUPS,
                                                  prefer_incoming=False, estimated=estimated_aa)
        rows = [f for g in review["groups"] for f in g["fields"]]
        # Measured amino acids replace estimated ones too (the review ticks them).
        fills = {f["key"]: f["incoming"] for f in rows
                 if f["status"] == "fill" or (f["status"] == "differs" and f["key"] in estimated_aa)}
        if any(f["status"] == "differs" and f["key"] not in estimated_aa for f in rows):
            differs.append(fdc_id)
        if fills:
            with _db.get_db() as conn:
                _db.merge_user_supplied_nutrients(conn, fdc_id, fills, overwrite=True, mark_edited=False)
                _db.update_estimated_keys(conn, fdc_id, remove=fills.keys())
                _recipe_dcp.cascade_food_change(fdc_id, conn)
            filled += 1
    url = f"/meal/{meal_id}?aa_refreshed={filled}"
    if differs:
        url += "&aa_differs=" + ",".join(str(i) for i in differs)
    return RedirectResponse(url + "#sec-protein-quality", status_code=303)


def _meal_add_food_local_results(q: str) -> list[dict]:
    """Local (recipe/cache/pantry) candidates for the meal add-food panel —
    the instant, no-network part. Shared by the initial synchronous render
    and the async search-api-results endpoint, which merges this with
    external results before sorting so a weak local match never outranks a
    much better external one just by rendering first."""
    # Preprocess query — strip meta words that shouldn't affect ranking
    _clean_words = [w for w in q.lower().split() if w not in _SEARCH_META_WORDS]
    clean_query = " ".join(_clean_words) if _clean_words else q

    search_results: list[dict] = []

    # Prepend matching recipes (local DB, instant)
    with _db.get_db() as conn:
        all_recipes   = _db.recipe_list(conn)
        cached_rows   = _db.search_cached_foods(conn, clean_query)
        pantry_ids    = _pantry_fdc_ids(conn)
    ql = q.lower()
    query_words = ql.split()
    matching_recipes = [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)]
    recipe_aa_status = _recipe_aa_status([r["id"] for r in matching_recipes])
    for r in matching_recipes:
        search_results.append({
            "_type":         "recipe",
            "recipe_id":     r["id"],
            "name":          r["name"],
            "servings":      float(r["servings"] or 1),
            "serving_size":  r["serving_size"],
            "total_weight":  r["total_weight"],
            "total_weight_unit": r["total_weight_unit"] or "g",
            "total_volume":  r["total_volume"],
            "total_volume_unit": r["total_volume_unit"] or "ml",
            "data_type":     "Recipe",
            "source":        "recipe",
            "aa":            recipe_aa_status[r["id"]],
        })

    # Cached foods only — fast, local DB. External USDA/OFF results are
    # fetched separately by the browser (GET /meal/{meal_id}/search-api-
    # results) so a repeat food already in the cache renders instantly
    # instead of waiting on 2-3 blocking USDA/OFF API round-trips.
    cache_fdc_ids = {row["fdc_id"] for row in cached_rows}
    with _db.get_db() as conn:
        annotations = _db.annotations_for_fdcids(conn, list(cache_fdc_ids))
        cached_nutrients: dict[int, str | None] = {}
        for fid in cache_fdc_ids:
            row = _db.get_cached_food(conn, fid)
            if row:
                cached_nutrients[fid] = row["nutrients_json"]

    def _aa_status(fdc_id: int, data_type: str) -> str:
        nuts_json = cached_nutrients.get(fdc_id)
        if nuts_json:
            return _usda.aa_indicator(json.loads(nuts_json))
        if data_type in ("Foundation", "SR Legacy"):
            return "~✓"
        return "✗"

    def _ann_gi(fdc_id: int) -> str:
        ann = annotations.get(fdc_id)
        if ann and ann["gi_estimate"] is not None:
            return str(int(round(ann["gi_estimate"])))
        return ""

    def _ann_gi_source(fdc_id: int) -> str:
        """Where a GI estimate came from, for the GI cell's tooltip — a rounded
        number in a narrow column says nothing about how trustworthy it is."""
        ann = annotations.get(fdc_id)
        if ann and ann["gi_estimate"] is not None and "gi_source" in ann.keys():
            return ann["gi_source"] or ""
        return ""

    def _ann_diaas(fdc_id: int) -> str:
        ann = annotations.get(fdc_id)
        if ann and ann["diaas_estimate"] is not None:
            return f"{ann['diaas_estimate']:.2f}"
        return ""

    for row in cached_rows:
        fid = row["fdc_id"]
        portions = json.loads(row["portions_json"] or "[]") or []
        dtype = row["data_type"] or ""
        search_results.append({
            "fdc_id":    fid,
            "name":      row["name"],
            "data_type": dtype,
            "brand":     row["brand"] or "",
            "source":    "pantry" if fid in pantry_ids else "cache",
            "off_code":  "",
            "portions":  portions,
            "aa":        _aa_status(fid, dtype),
            "gi":        _ann_gi(fid),
            "gi_source": _ann_gi_source(fid),
            "diaas":     _ann_diaas(fid),
        })

    # Static (bundled-dataset, no network) external sources are instant like
    # Pantry/Cache/Recipe, so they're merged in here rather than through the
    # async external-fetch path used by USDA/OFF/CNF.
    search_results.extend(_static_source_candidates(clean_query))

    return search_results


@app.get("/meal/{meal_id}", response_class=HTMLResponse)
async def meal_view(request: Request, meal_id: int, q: str = "", add_error: str = "", sort: str | None = None,
                     item_sort: str | None = None, source: list[str] | None = Query(default=None),
                     limit: int | None = None,
                     ignore_complements: list[str] = Query(default=[]),
                     unignore: list[str] = Query(default=[]),
                     comp_sort: str | None = None, diaas_sort: str | None = None,
                     anchor_name: list[str] = Query(default=[]),
                     anchor_grams: list[str] = Query(default=[]),
                     rank: str | None = None, top_n: str | None = None,
                     aa_refreshed: int | None = None, aa_differs: str = "", added_check: str = ""):
    sort = _resolve_sort(sort, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    item_sort = _resolve_sort(item_sort, "sort_meal_items", "alpha", {"alpha", "entry"})
    # "Refresh from USDA" result: foods it filled, and foods whose USDA copy
    # also differs on values they already have (left alone; review offered).
    aa_differ_foods: list[dict] = []
    for tok in aa_differs.split(","):
        try:
            did = int(tok)
        except ValueError:
            continue
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, did)
        if row:
            aa_differ_foods.append({"fdc_id": did, "name": row["name"]})
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    comp_sort = _resolve_sort(comp_sort, "sort_complements", "dcp", _COMP_SORT_MODES)
    diaas_sort = _resolve_sort(diaas_sort, "sort_diaas_improvers", "effect", _DIAAS_SORT_MODES)
    top_n = _resolve_contributor_top_n(top_n)
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
        if not meal:
            return RedirectResponse("/meals", status_code=303)
        sibling_meals = [
            dict(m) for m in _db.meal_list_by_date(conn, meal["meal_date"])
            if m["id"] != meal_id
        ]
    if not meal:
        return RedirectResponse("/meals", status_code=303)

    items, total_nutrients, diaas_result, meal_ingredients = _meal_totals(meal_id)
    items = _sort_meal_items_display(items, item_sort)

    contributor_options = _contributor_rank_options(total_nutrients)
    if not rank or rank not in {k for _, opts in contributor_options for k, _ in opts}:
        rank = _default_rank_key(contributor_options)
    with _db.get_db() as conn:
        contributor_result = _build_contributors(meal_ingredients, rank, top_n, conn)

    # Search results for add-food panel
    search_results = []
    if q:
        search_results = _sort_search_results(_meal_add_food_local_results(q), q, sort)
        search_results = _cap_results_preserving_local(_filter_search_results_by_source(search_results, source), limit)

    with _db.get_db() as conn:
        day_profile_obj = _day_profile.get_profile_for_date(conn, meal["meal_date"])
    rda = _load_rda(day_profile_obj)
    optimal = _load_optimal(day_profile_obj)
    max_limits = _load_max_limits(day_profile_obj)

    # Compute daily totals (this meal + siblings) for the day total % column
    daily_nutrients: dict | None = None
    if rda and total_nutrients:
        day_parts = [total_nutrients]
        for sib in sibling_meals:
            _, sib_nuts, _, _ = _meal_totals(sib["id"])
            if sib_nuts:
                day_parts.append(sib_nuts)
        if len(day_parts) > 1:
            daily_nutrients = {}
            for p in day_parts:
                for k, v in p.items():
                    daily_nutrients[k] = daily_nutrients.get(k, 0.0) + v
        else:
            daily_nutrients = total_nutrients

    diaas_display = _build_diaas_display(diaas_result)

    # Persist the calculated DCP and calories so they show up on Meals & Log.
    _compute_and_store_meal_bcp(meal_id)
    if meal["complete"]:
        _refresh_day_pct_goal(meal["meal_date"])

    aa_nutrients   = _meal_aa_nutrients(meal_id)
    gl_total, gl_blockers = _compute_gl(meal_id)

    item_antinutrients = []
    seen_names: set[str] = set()
    with _db.get_db() as conn:
        for item in items:
            food_name = item.get("food_name", "")
            if item.get("recipe_id"):
                for ing in _expand_recipe_ingredients(item["recipe_id"], 1.0, conn):
                    n = ing["food_name"]
                    if n not in seen_names:
                        seen_names.add(n)
                        flags = _usda.get_antinutrient_flags(n)
                        if flags:
                            item_antinutrients.append({"food_name": n, "flags": flags})
            elif item.get("fdc_id") and food_name and food_name not in seen_names:
                seen_names.add(food_name)
                flags = _usda.get_antinutrient_flags(food_name)
                if flags:
                    item_antinutrients.append({"food_name": food_name, "flags": flags})

    ox_items = []
    with _db.get_db() as conn:
        for it in items:
            if it.get("recipe_id"):
                portion_factor = float(it["amount"] or 1)
                recipe = _db.recipe_get(conn, it["recipe_id"])
                if recipe:
                    r_servings = float(recipe["servings"] or 1)
                    factor = portion_factor / r_servings
                else:
                    factor = portion_factor
                for ing in _expand_recipe_ingredients(it["recipe_id"], factor, conn):
                    if ing.get("fdc_id") and ing["fdc_id"] > 0:
                        ox_items.append({
                            "fdc_id":    ing["fdc_id"],
                            "food_name": ing["food_name"],
                            "amount_g":  ing["grams"],
                        })
            elif it.get("fdc_id"):
                ox_items.append({
                    "fdc_id":    it["fdc_id"],
                    "food_name": it["food_name"],
                    "amount_g":  it["amount"],
                })
    oxalate = _oxalate_for_items(ox_items)

    return templates.TemplateResponse(request, "meal.html", {
        **_added_food_note(added_check),
        "recalc_notes": _recalc_notes([meal_id]),
        "calorie_warnings": _calorie_warnings(meal_ingredients),
        "aa_refreshed":    aa_refreshed,
        "aa_differ_foods": aa_differ_foods,
        "meal":                dict(meal),
        "items":               items,
        "item_sort":           item_sort,
        "nutrient_sections":   _nutrient_sections(total_nutrients, rda, daily_nutrients,
                                                  optimal=optimal, max_limits=max_limits,
                                                  dcp_g=diaas_display["dcp_g"] if diaas_display else None,
                                                  dcp_missing=diaas_display["missing"] if diaas_display else None) if total_nutrients else [],
        "diaas":               diaas_display,
        "dcp_missing_names":   diaas_display["missing"] if diaas_display else [],
        "protein_adequacy":    _protein_adequacy(total_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":         _complement_suggestions(aa_nutrients, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="meal", ingredients=meal_ingredients, exclude_names=_effective_ignored(ignore_complements, unignore), comp_sort=comp_sort, diaas_sort=diaas_sort, anchor_overrides=_parse_anchor_overrides(anchor_name, anchor_grams)),
        "ignored_complements": sorted(_effective_ignored(ignore_complements, unignore)),
        "gl":                  {"total": gl_total, "blockers": gl_blockers},
        "item_antinutrients":  item_antinutrients,
        "oxalate":             oxalate,
        "q":                   q,
        "sort":                sort,
        "source":              source,
        "limit":               limit,
        "external_source_labels": _external_source_labels(source),
        "source_filters":      _SEARCH_SOURCE_FILTERS,
        "source_labels":       _SEARCH_SOURCE_LABELS,
        "omitted_sources":     _omitted_source_labels(source),
        "search_results":      search_results,
        "today":               datetime.date.today().isoformat(),
        "has_profile":         rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
        "has_day_pct":         daily_nutrients is not None,
        "sibling_meals":       sibling_meals,
        "add_error":           add_error,
        "contributor_options": contributor_options,
        "contributor_rank":    rank,
        "contributor_unit":    _usda.nutrient_label(rank)[1] if rank else "",
        "contributors":        contributor_result["items"],
        "contributor_total":   contributor_result["total"],
        "contributor_count":   contributor_result["count"],
        "contributor_top_n":         contributor_result["top_n"],
        "contributor_top_n_options": contributor_result["top_n_options"],
        "contributor_is_dcp":        contributor_result["is_dcp"],
    })


def _meal_print_context(meal_id: int) -> dict | None:
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
    if not meal:
        return None

    items, total_nutrients, diaas_result, meal_ingredients = _meal_totals(meal_id)
    items = _sort_meal_items_display(items)

    with _db.get_db() as conn:
        day_profile_obj = _day_profile.get_profile_for_date(conn, meal["meal_date"])
    rda = _load_rda(day_profile_obj)
    optimal = _load_optimal(day_profile_obj)
    max_limits = _load_max_limits(day_profile_obj)

    diaas_display = _build_diaas_display(diaas_result)
    aa_nutrients = _meal_aa_nutrients(meal_id)
    gl_total, gl_blockers = _compute_gl(meal_id)

    item_antinutrients = []
    seen_names: set[str] = set()
    with _db.get_db() as conn:
        for item in items:
            food_name = item.get("food_name", "")
            if item.get("recipe_id"):
                for ing in _expand_recipe_ingredients(item["recipe_id"], 1.0, conn):
                    n = ing["food_name"]
                    if n not in seen_names:
                        seen_names.add(n)
                        flags = _usda.get_antinutrient_flags(n)
                        if flags:
                            item_antinutrients.append({"food_name": n, "flags": flags})
            elif item.get("fdc_id") and food_name and food_name not in seen_names:
                seen_names.add(food_name)
                flags = _usda.get_antinutrient_flags(food_name)
                if flags:
                    item_antinutrients.append({"food_name": food_name, "flags": flags})

    ox_items = []
    with _db.get_db() as conn:
        for it in items:
            if it.get("recipe_id"):
                portion_factor = float(it["amount"] or 1)
                recipe = _db.recipe_get(conn, it["recipe_id"])
                if recipe:
                    r_servings = float(recipe["servings"] or 1)
                    factor = portion_factor / r_servings
                else:
                    factor = portion_factor
                for ing in _expand_recipe_ingredients(it["recipe_id"], factor, conn):
                    if ing.get("fdc_id") and ing["fdc_id"] > 0:
                        ox_items.append({
                            "fdc_id":    ing["fdc_id"],
                            "food_name": ing["food_name"],
                            "amount_g":  ing["grams"],
                        })
            elif it.get("fdc_id"):
                ox_items.append({
                    "fdc_id":    it["fdc_id"],
                    "food_name": it["food_name"],
                    "amount_g":  it["amount"],
                })
    oxalate = _oxalate_for_items(ox_items)

    return {
        "meal":               dict(meal),
        "meal_items":         items,
        "nutrient_sections":  _nutrient_sections(total_nutrients, rda, optimal=optimal, max_limits=max_limits,
                                                 dcp_g=diaas_display["dcp_g"] if diaas_display else None,
                                                 dcp_missing=diaas_display["missing"] if diaas_display else None) if total_nutrients else [],
        "diaas":              diaas_display,
        "dcp_missing_names":  diaas_display["missing"] if diaas_display else [],
        "protein_adequacy":   _protein_adequacy(total_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":        _complement_suggestions(aa_nutrients, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="meal", ingredients=meal_ingredients),
        "gl":                 {"total": gl_total, "blockers": gl_blockers},
        "ingredient_antinutrients": item_antinutrients,
        "oxalate_agg":        oxalate,
        "has_profile":        rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
    }


def _meal_available_sections(ctx: dict) -> list[str]:
    available = []
    if ctx.get("meal_items"):
        available.append("items")
    if ctx.get("nutrient_sections"):
        available.append("nutrient_table")
    if ctx.get("diaas"):
        available.append("protein_summary")
        available.append("protein_quality")
    gl = ctx.get("gl")
    if gl and gl.get("total") is not None:
        available.append("glycemic_load")
    if ctx.get("oxalate_agg") or ctx.get("ingredient_antinutrients"):
        available.append("antinutrients")
    complements = ctx.get("complements")
    if complements and not complements.get("no_data"):
        available.append("complements")
    return available


@app.get("/meal/{meal_id}/print", response_class=HTMLResponse)
async def meal_print(
    request: Request,
    meal_id: int,
    sections: list[str] = Query(default=[]),
    sections_submitted: bool = Query(default=False),
    layout: str = Query(default=""),
    paper: str = Query(default=""),
    layout_submitted: bool = Query(default=False),
):
    ctx = _meal_print_context(meal_id)
    if ctx is None:
        return RedirectResponse("/meals", status_code=303)

    available = _meal_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("meal", available, sections, sections_submitted, prefs)
    layout_ctx = _print_sections.resolve_layout_context(layout, paper, layout_submitted, prefs)
    save_update = layout_ctx.pop("_save_update")
    if sections_submitted or save_update:
        _save_prefs_file({**_print_sections.save_sections("meal", enabled, prefs), **save_update})

    return templates.TemplateResponse(request, "print.html", {
        "title":              ctx["meal"]["name"],
        "subtitle":           ctx["meal"]["meal_date"],
        "back_url":           f"/meal/{meal_id}",
        "back_label":         "Back to meal",
        "fixed_params":       {},
        "section_labels":     _print_sections.PRINT_SECTION_LABELS,
        "available_sections": available,
        "enabled":            enabled,
        "portion_label":      "this meal",
        **layout_ctx,
        **ctx,
    })


@app.get("/meal/{meal_id}/search-api-results", response_class=HTMLResponse)
async def meal_search_api_results(request: Request, meal_id: int, q: str = "", sort: str | None = None,
                                   source: list[str] | None = Query(default=None),
                                   limit: int | None = None):
    """Fetched by JS on the meal page after the initial (cache-only) render.
    Returns the FULL result set — local results merged with USDA/OFF and
    re-sorted together, not just the external rows appended below — so a
    weak local match never outranks a much better external one just because
    the local pass rendered first. The JS replaces the table body with this
    response rather than appending to it."""
    sort = _resolve_sort(sort, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    q = q.strip()
    results: list[dict] = []
    if q:
        _clean_words = [w for w in q.lower().split() if w not in _SEARCH_META_WORDS]
        clean_query = " ".join(_clean_words) if _clean_words else q
        _api_words = [w for w in clean_query.split() if w not in _SEARCH_PREP_WORDS]
        api_query = " ".join(_api_words) if _api_words else clean_query

        local = _meal_add_food_local_results(q)
        exclude_ids = {r["fdc_id"] for r in local if r.get("fdc_id")}
        external = _external_food_search_results(api_query, exclude_ids, q, sort, sources=source, limit=limit)
        results = _sort_search_results(local + external, q, sort)
        results = _cap_results_preserving_local(_filter_search_results_by_source(results, source), limit)

    return templates.TemplateResponse(request, "_add_food_api_rows.html", {
        "meal_id": meal_id,
        "results": results,
        "q":       q,
    })


@app.post("/meal/{meal_id}/confirm-aa", response_class=RedirectResponse)
async def meal_confirm_aa(
    meal_id: int,
    fdc_ids: list[int] = Form(...),
    q: str = Form(""),
    sort: str = Form(""),
    source: list[str] = Form([]),
    limit: int | None = Form(None),
):
    """Same as /food/confirm-aa, for the add-food search results on a meal's
    page — fetches and caches full USDA details for the selected foods so
    their '~✓' guess becomes a confirmed ✓ or ✗."""
    for fdc_id in fdc_ids:
        if fdc_id <= 0:
            continue
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached:
            continue
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception:
            continue
        with _db.get_db() as conn:
            _db.cache_food(
                conn, fdc_id=detail["fdcId"], name=detail["name"],
                data_type=detail.get("dataType", ""),
                brand=detail.get("brand"),
                serving_size=detail.get("servingSize"),
                serving_unit=detail.get("servingUnit"),
                nutrients=detail.get("nutrients", {}),
                portions=detail.get("portions", []),
            )
            _recipe_dcp.cascade_food_change(detail["fdcId"], conn)

    from urllib.parse import urlencode
    params: dict[str, str | list[str]] = {"q": q}
    if sort:
        params["sort"] = sort
    if source:
        params["source"] = source
    if limit:
        params["limit"] = str(limit)
    return RedirectResponse(f"/meal/{meal_id}?{urlencode(params, doseq=True)}", status_code=303)


@app.post("/meal/{meal_id}/add", response_class=RedirectResponse)
async def meal_add_food(
    meal_id: int,
    fdc_id: int = Form(...),
    food_name: str = Form(""),
    portion_str: str = Form("100 g"),
    off_code: str = Form(""),
    q: str = Form(""),
):
    from urllib.parse import quote, urlencode

    def _redirect(error: str | None = None, check: str = "") -> RedirectResponse:
        if error:
            params = {"add_error": error}
            if q:
                params["q"] = q
        else:
            # Explicit empty q= (not simply omitted) tells the persist-search
            # JS in base.html to forget the saved query instead of restoring
            # it from sessionStorage — otherwise the search panel would
            # reappear right after a successful add.
            params = {"q": ""}
            if check:
                params["added_check"] = check
        qs = f"?{urlencode(params)}"
        return RedirectResponse(f"/meal/{meal_id}{qs}", status_code=303)

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        try:
            detail = _fetch_uncached_food_detail(fdc_id, off_code)
            with _db.get_db() as conn:
                _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                               data_type=detail.get("dataType", ""),
                               brand=detail.get("brand"),
                               serving_size=detail.get("servingSize"),
                               serving_unit=detail.get("servingUnit"),
                               nutrients=detail.get("nutrients", {}),
                               portions=detail.get("portions", []))
                _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
            food_name = food_name or detail["name"]
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, fdc_id)
        except Exception as e:
            return _redirect(error=f'Could not fetch details for "{food_name or fdc_id}": {e}')

    name = food_name or (cached["name"] if cached else "Unknown food")
    portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
    raw = portion_str.strip() or "100 g"
    grams, label = _parse_portion_str(raw, portions, name)
    if not grams:
        return _redirect(error=label)
    # Store what was typed ("1/3 c", "2 × large egg") as the unit, the way a
    # recipe ingredient does, so a later portion correction can find it.
    with _db.get_db() as conn:
        _db.meal_add_food(conn, meal_id, fdc_id, name, grams, label)
        check = _added_food_check(conn, fdc_id)
    if _annotation_prompt_needed(fdc_id):
        # next= carries an explicit empty q= (not simply omitted) so that,
        # once the annotate flow redirects back to the meal page, the
        # persist-search JS in base.html forgets the saved query instead of
        # restoring the stale search-results panel.
        back = f"/meal/{meal_id}?q=" + (f"&added_check={check}" if check else "")
        return RedirectResponse(f"/food/annotate/{fdc_id}?next={quote(back)}", status_code=303)
    return _redirect(check=check)


@app.post("/meal/{meal_id}/add-recipe", response_class=RedirectResponse)
async def meal_add_recipe_item(
    meal_id: int,
    recipe_id: int = Form(...),
    recipe_name: str = Form(""),
    servings: float = Form(1.0),
    mode: str = Form("recipe"),
    amount_mode: str = Form("servings"),
    amount_value_weight: str = Form(""),
    amount_value_volume: str = Form(""),
):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)
    name = recipe_name or recipe["name"]

    # Convert weight/volume entry to an equivalent servings count
    try:
        r_servings = float(recipe["servings"] or 1)
        if amount_mode == "weight" and amount_value_weight.strip() and recipe["total_weight"]:
            servings = (float(amount_value_weight) / float(recipe["total_weight"])) * r_servings
        elif amount_mode == "volume" and amount_value_volume.strip() and recipe["total_volume"]:
            servings = (float(amount_value_volume) / float(recipe["total_volume"])) * r_servings
    except (ValueError, ZeroDivisionError):
        pass

    if mode == "ingredients":
        r_total_servings = float(recipe["servings"] or 1)
        scale = servings / r_total_servings
        # Recursively flatten to leaf foods (shared with the nutrient-total
        # code) rather than stopping one level deep: a direct ingredient that
        # is itself a sub-recipe used to get added as a single whole-recipe
        # meal item instead of being expanded further, so "individual
        # ingredients" for a recipe containing a sub-recipe silently added
        # that sub-recipe as a package alongside the real ingredients.
        with _db.get_db() as conn:
            leaves = expand_recipe_ingredients(recipe_id, conn, portion_factor=scale)
        with _db.get_db() as conn:
            for leaf in leaves:
                grams = leaf["grams"]
                _db.meal_add_food(conn, meal_id, leaf["fdc_id"],
                                  leaf["food_name"], grams, f"{grams:.4g} g")
    else:
        unit = f"{servings:g} serving" + ("s" if servings != 1 else "")
        with _db.get_db() as conn:
            _db.meal_add_recipe(conn, meal_id, recipe_id, name, servings, unit=unit)
    # Explicit empty q= tells the persist-search JS in base.html to forget
    # the saved query instead of restoring it from sessionStorage.
    return RedirectResponse(f"/meal/{meal_id}?q=", status_code=303)


@app.post("/meal/{meal_id}/remove/{item_id}", response_class=RedirectResponse)
async def meal_remove_item(meal_id: int, item_id: int):
    with _db.get_db() as conn:
        _db.meal_remove_item(conn, item_id, meal_id)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/rename", response_class=RedirectResponse)
async def meal_rename_post(meal_id: int, name: str = Form(...), meal_date: str = Form(...)):
    name = name.strip()
    meal_date = meal_date.strip()
    with _db.get_db() as conn:
        if name:
            _db.meal_rename(conn, meal_id, name)
        try:
            datetime.datetime.strptime(meal_date, "%Y-%m-%d")
            _db.meal_set_date(conn, meal_id, meal_date)
        except ValueError:
            pass
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/complete", response_class=RedirectResponse)
async def meal_toggle_complete(meal_id: int):
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
    if meal:
        with _db.get_db() as conn:
            _db.meal_set_complete(conn, meal_id, not bool(meal["complete"]))
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/delete", response_class=RedirectResponse)
async def meal_delete_post(meal_id: int):
    with _db.get_db() as conn:
        _db.meal_delete(conn, meal_id)
    return RedirectResponse("/meals", status_code=303)


@app.post("/meals/delete-day", response_class=RedirectResponse)
async def meals_delete_day_post(meal_date: str = Form(...), redirect_to: str = Form("/meals")):
    with _db.get_db() as conn:
        _db.meal_delete_by_date(conn, meal_date)
    return RedirectResponse(redirect_to, status_code=303)


@app.post("/meal/{meal_id}/update/{item_id}", response_class=RedirectResponse)
async def meal_update_item_post(
    meal_id: int,
    item_id: int,
    amount: str = Form(...),
    notes: str = Form(""),
    q: str = Form(""),
):
    from urllib.parse import urlencode

    def _redirect(error: str | None = None) -> RedirectResponse:
        if error:
            params = {"add_error": error}
            if q:
                params["q"] = q
        else:
            # Explicit empty q= tells the persist-search JS in base.html to
            # forget the saved query instead of restoring it — otherwise the
            # search panel reappears right after a successful edit.
            params = {"q": ""}
        qs = f"?{urlencode(params)}"
        return RedirectResponse(f"/meal/{meal_id}{qs}", status_code=303)

    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
    item = next((it for it in items if it["id"] == item_id), None)
    if not item:
        return _redirect()
    notes_val = notes.strip() or None
    if item["item_type"] == "recipe":
        try:
            srv = float(amount)
        except ValueError:
            return _redirect()
        if srv > 0:
            unit = f"{srv:g} serving" + ("s" if srv != 1 else "")
            with _db.get_db() as conn:
                _db.meal_update_item(conn, item_id, meal_id, srv, unit)
                # The amount was just typed against the recipe's serving as
                # it is now, so that's the serving weight to remember.
                _db.meal_item_set_serving_grams(conn, item_id, recipe_serving_grams(item["recipe_id"], conn))
    else:
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, item["fdc_id"]) if item["fdc_id"] else None
        portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
        grams, label = _parse_portion_str(amount.strip(), portions, item["food_name"])
        if grams is not None:
            with _db.get_db() as conn:
                _db.meal_replace_food(conn, item_id, meal_id, item["fdc_id"],
                                      item["food_name"], grams, label, notes_val)
        else:
            return _redirect(error=label)
    return _redirect()


@app.post("/meal/{meal_id}/item/{item_id}/serving-weight", response_class=RedirectResponse)
async def meal_item_serving_weight_post(meal_id: int, item_id: int, choice: str = Form(...)):
    """Resolve a logged recipe whose serving weight changed since it was
    logged. choice="keep": keep the grams originally eaten, by rescaling the
    servings count to the recipe's new serving. choice="accept": keep the
    servings count, i.e. accept the new, different amount of food."""
    with _db.get_db() as conn:
        item = next((it for it in _db.meal_get_items(conn, meal_id) if it["id"] == item_id), None)
        meal = _db.meal_get(conn, meal_id)
        if item is None or meal is None or item["item_type"] != "recipe":
            return RedirectResponse(f"/meal/{meal_id}?q=", status_code=303)
        now = recipe_serving_grams(item["recipe_id"], conn)
        logged = item["serving_grams"]
        if choice == "keep" and _serving_weight_changed(logged, now):
            srv = round(float(item["amount"]) * logged / now, 3)
            unit = f"{srv:g} serving" + ("s" if srv != 1 else "")
            _db.meal_update_item(conn, item_id, meal_id, srv, unit)
        _db.meal_item_set_serving_grams(conn, item_id, now)
    _compute_and_store_meal_bcp(meal_id)
    _refresh_day_pct_goal(meal["meal_date"])
    return RedirectResponse(f"/meal/{meal_id}?q=", status_code=303)


@app.post("/meal/{meal_id}/merge", response_class=RedirectResponse)
async def meal_merge_post(meal_id: int, request: Request):
    form = await request.form()
    new_name = (form.get("new_name") or "").strip()
    delete_originals = bool(form.get("delete_originals"))
    raw_ids = form.getlist("merge_ids")
    try:
        selected_ids = [int(x) for x in raw_ids]
    except (ValueError, TypeError):
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)
    if len(selected_ids) < 2:
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)

    with _db.get_db() as conn:
        meals_to_merge = [_db.meal_get(conn, mid) for mid in selected_ids]
    meals_to_merge = [m for m in meals_to_merge if m is not None]
    if len(meals_to_merge) < 2:
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)

    if not new_name:
        new_name = meals_to_merge[0]["name"]
    meal_date = meals_to_merge[0]["meal_date"]

    with _db.get_db() as conn:
        new_mid = _db.meal_create(conn, new_name, meal_date)
        _day_profile.ensure_day_profile(conn, meal_date)
        for m in meals_to_merge:
            _db.meal_copy_items(conn, m["id"], new_mid)

    if delete_originals:
        with _db.get_db() as conn:
            for m in meals_to_merge:
                _db.meal_delete(conn, m["id"])

    return RedirectResponse(f"/meal/{new_mid}", status_code=303)


@app.get("/meals/search", response_class=HTMLResponse)
async def meals_search(request: Request, q: str = ""):
    rows: list[dict] = []
    n_items = n_meals = n_dates = 0
    if q.strip():
        with _db.get_db() as conn:
            rows = [dict(r) for r in _db.search_meal_history(conn, q.strip())]
            recipe_ids = {r["recipe_id"] for r in rows if r["item_type"] == "recipe" and r["recipe_id"]}
            deleted_recipe_ids = {rid for rid in recipe_ids if _db.recipe_get(conn, rid) is None}
        for r in rows:
            if r["item_type"] == "recipe":
                r["recipe_deleted"] = r["recipe_id"] in deleted_recipe_ids
        with _db.get_db() as conn:
            _annotate_recipe_amounts(rows, conn, id_key="item_id")
            _annotate_food_amounts(rows, conn)
        n_items = len(rows)
        n_meals = len({r["meal_id"] for r in rows})
        n_dates = len({r["meal_date"] for r in rows})
    return templates.TemplateResponse(request, "meals_search.html", {
        "q":       q,
        "rows":    rows,
        "n_items": n_items,
        "n_meals": n_meals,
        "n_dates": n_dates,
    })


def _day_analysis(meal_date: str) -> tuple[list, dict, dict | None, list]:
    """Compute combined nutrients and DIAAS for all meals on a given date.

    Reuses _meal_expand_for_diaas (the same per-meal expansion _meal_totals
    uses) instead of re-walking each meal's items independently, so a fix to
    that expansion logic can't silently apply to per-meal pages but not to
    this day-level rollup (or vice versa)."""
    with _db.get_db() as conn:
        meals = [dict(m) for m in _db.meal_list_by_date(conn, meal_date)]
        combined_nutrients: dict = {}
        all_ingredients: list = []

        for meal in meals:
            _, nutrients, ingredients = _meal_expand_for_diaas(meal["id"], conn)
            for k, v in nutrients.items():
                combined_nutrients[k] = combined_nutrients.get(k, 0.0) + v
            all_ingredients.extend(ingredients)

        all_ingredients = _group_ingredients_by_food(all_ingredients)
        diaas_result = None
        if all_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(all_ingredients, conn)
            except Exception:
                pass

    return meals, combined_nutrients, diaas_result, all_ingredients


def _meal_day_context(meal_id: int) -> dict | None:
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
    if not meal:
        return None
    meal_date = meal["meal_date"]
    meals, combined_nutrients, diaas_result, day_ingredients = _day_analysis(meal_date)

    # Attach items list to each meal dict
    with _db.get_db() as conn:
        for m in meals:
            m_items = [dict(it) for it in _db.meal_get_items(conn, m["id"])]
            for it in m_items:
                if it["item_type"] == "recipe":
                    it["recipe_deleted"] = _db.recipe_get(conn, it["recipe_id"]) is None
            _annotate_recipe_amounts(m_items, conn)
            _annotate_food_amounts(m_items, conn)
            m["meal_items"] = _sort_meal_items_display(m_items)

    diaas_display = _build_diaas_display(diaas_result)

    # Pool AA nutrients across all meals on this date (for complement suggestions)
    aa_nutrients: dict = {}
    for m in meals:
        for k, v in _meal_aa_nutrients(m["id"]).items():
            aa_nutrients[k] = aa_nutrients.get(k, 0.0) + v

    # Pool GL across all meals on this date
    gl_total_sum = 0.0
    all_gl_blockers: list[str] = []
    any_gl_none = False
    for m in meals:
        gl_val, gl_blockers = _compute_gl(m["id"])
        if gl_val is None:
            any_gl_none = True
        else:
            gl_total_sum += gl_val
        all_gl_blockers.extend(gl_blockers)
    gl_total = None if any_gl_none else round(gl_total_sum, 1)

    with _db.get_db() as conn:
        day_profile_obj = _day_profile.get_profile_for_date(conn, meal_date)
        day_profile_row = _db.day_profile_get(conn, meal_date)
    rda = _load_rda(day_profile_obj)
    optimal = _load_optimal(day_profile_obj)
    max_limits = _load_max_limits(day_profile_obj)
    return {
        "meal_date":         meal_date,
        "meals":             meals,
        "from_meal_id":      meal_id,
        "nutrient_sections": _nutrient_sections(combined_nutrients, rda, combined_nutrients,
                                                optimal=optimal, max_limits=max_limits,
                                                dcp_g=diaas_display["dcp_g"] if diaas_display else None,
                                                dcp_missing=diaas_display["missing"] if diaas_display else None) if combined_nutrients else [],
        "diaas":             diaas_display,
        "dcp_missing_names": diaas_display["missing"] if diaas_display else [],
        "protein_adequacy":  _protein_adequacy(combined_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":       _complement_suggestions(aa_nutrients, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="daily", ingredients=day_ingredients),
        "gl":                {"total": gl_total, "blockers": all_gl_blockers},
        "has_profile":       rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
        "day_profile_name":  day_profile_row["profile_name"] if day_profile_row else None,
        "day_profile_overridden": bool(day_profile_row["overridden"]) if day_profile_row else False,
        "all_profile_names": _profile.list_profiles(),
    }


@app.get("/meal/{meal_id}/day", response_class=HTMLResponse)
async def meal_day_view(request: Request, meal_id: int):
    ctx = _meal_day_context(meal_id)
    if ctx is None:
        return RedirectResponse("/meals", status_code=303)
    return templates.TemplateResponse(request, "meal_day.html", ctx)


def _day_available_sections(ctx: dict) -> list[str]:
    available = []
    if ctx.get("meals"):
        available.append("meals_list")
    if ctx.get("nutrient_sections"):
        available.append("nutrient_table")
    if ctx.get("diaas"):
        available.append("protein_summary")
        available.append("protein_quality")
    gl = ctx.get("gl")
    if gl and gl.get("total") is not None:
        available.append("glycemic_load")
    complements = ctx.get("complements")
    if complements and not complements.get("no_data"):
        available.append("complements")
    return available


@app.get("/meal/{meal_id}/day/print", response_class=HTMLResponse)
async def meal_day_print(
    request: Request,
    meal_id: int,
    sections: list[str] = Query(default=[]),
    sections_submitted: bool = Query(default=False),
    layout: str = Query(default=""),
    paper: str = Query(default=""),
    layout_submitted: bool = Query(default=False),
):
    ctx = _meal_day_context(meal_id)
    if ctx is None:
        return RedirectResponse("/meals", status_code=303)

    available = _day_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("day", available, sections, sections_submitted, prefs)
    layout_ctx = _print_sections.resolve_layout_context(layout, paper, layout_submitted, prefs)
    save_update = layout_ctx.pop("_save_update")
    if sections_submitted or save_update:
        _save_prefs_file({**_print_sections.save_sections("day", enabled, prefs), **save_update})

    return templates.TemplateResponse(request, "print.html", {
        "title":              f"Daily Summary — {ctx['meal_date']}",
        "subtitle":           f"{ctx['meal_date']}" + (f" · profile: {ctx['day_profile_name']}" if ctx.get("day_profile_name") else ""),
        "back_url":           f"/meal/{meal_id}/day",
        "back_label":         "Back to day",
        "fixed_params":       {},
        "section_labels":     _print_sections.PRINT_SECTION_LABELS,
        "available_sections": available,
        "enabled":            enabled,
        "portion_label":      "full day",
        "gl_scope":           "day",
        "day_meals":          ctx["meals"],
        **layout_ctx,
        **ctx,
    })


@app.post("/meal/{meal_id}/day/profile", response_class=RedirectResponse)
async def meal_day_profile_override(meal_id: int, profile_name: str = Form(...)):
    """Reassign which profile this meal's date is scored against — for when
    illness/travel/a profile switch didn't line up with the calendar day."""
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
        if not meal:
            return RedirectResponse("/meals", status_code=303)
        meal_date = meal["meal_date"]
        _day_profile.set_day_profile_override(conn, meal_date, profile_name)
    _refresh_day_pct_goal(meal_date)
    return RedirectResponse(f"/meal/{meal_id}/day", status_code=303)


# ---------------------------------------------------------------------------
# Settings / profile routes
# ---------------------------------------------------------------------------

@app.get("/settings", response_class=HTMLResponse)
async def settings_get(request: Request, saved: str = "", recompute_retry: str = "", kept: int = 0,
                       gi_build_error: str = "", kept_recipes: int = 0, kept_edited: int = 0):
    profile = _profile.load_profile()
    diet_pref = _current_diet_pref()
    rda = _profile.compute_rda(profile, diet_pref=diet_pref) if profile else None
    rda_rows = []
    if rda:
        for key, (val, unit, rda_type) in rda.items():
            label, _ = _usda.nutrient_label(key)
            rda_rows.append({"label": label, "value": round(val, 1),
                              "unit": unit, "rda_type": rda_type})
    api_key = _usda.get_api_key()
    search_boost_page_size = _usda.get_search_boost_page_size()
    import oxalate as _ox
    oxalate_available = _ox.is_available()
    from numa_app.services import demo_data as _demo_data
    demo_data_loaded = _demo_data.is_loaded()
    with _db.get_db() as conn:
        diaas_overrides = [dict(r) for r in _diaas.diaas_override_list(conn)]
        recompute_errors = [dict(r) for r in _db.list_unresolved_recompute_errors(conn)]
        starter_status = _demo_data.starter_status(conn)
        starter_changes = _demo_data.pending_changes(conn, silent=_is_curator())
        starter_change_details = _demo_data.change_details(conn, starter_changes)

    nutrient_target_rows = []
    if profile:
        # Every nutrient listed here is settable, not just ones with an
        # established RDA/AI — amino acids, EPA/DHA, and phytonutrients have
        # no official DRI but are still valid Optimal/max-limit candidates.
        for group_name, keys in _NUTRIENT_TARGET_GROUPS:
            for key in keys:
                label, unit = _usda.nutrient_label(key)
                nutrient_target_rows.append({
                    "key":     key,
                    "label":   label,
                    "unit":    unit,
                    "optimal": profile.optimal_targets.get(key),
                    "limit":   profile.max_limits.get(key),
                })

    from numa_app.services.meal_list_columns import (
        AVAILABLE_NUTRIENTS, MAX_MEAL_LIST_NUTRIENTS, saved_or_default as _saved_or_default_meal_nutrients,
    )
    saved_meal_nutrients = _saved_or_default_meal_nutrients(_load_prefs_file())
    # Protein here is raw protein — DCP is never a picker choice, since both
    # lists already show it as fixed columns — so say so on the row itself.
    meal_list_nutrient_rows = [
        {
            "key": key, "label": "Protein (raw, not DCP)" if key == "protein_g" else label, "unit": unit,
            "position": (saved_meal_nutrients.index(key) + 1) if key in saved_meal_nutrients else None,
        }
        for key, label, unit in AVAILABLE_NUTRIENTS
    ]

    # A finished 2021-table build's outcome is shown once, then forgotten, so a
    # later visit to Settings doesn't keep announcing an old build.
    gi_build = _gi_table_build.build_status()
    if not gi_build["running"]:
        _gi_table_build.clear_status()

    return templates.TemplateResponse(request, "settings.html", {
        "data_check_reminder":  _data_check_reminder_prefs(),
        "profile":              profile,
        "rda_rows":             rda_rows,
        "activity_labels":      _profile.ACTIVITY_LABELS,
        "sex_values":           _profile.SEX_VALUES,
        "saved":                saved,
        "starter_foods_kept":   kept,
        "starter_recipes_kept": kept_recipes,
        "starter_edited_kept":  kept_edited,
        "diet_pref":            diet_pref,
        "diet_labels":          _DIET_LABELS,
        # An older saved "chromium-browser" shows as the one Chromium choice.
        "preferred_browser":    (_load_prefs_file().get("preferred_browser", "") or "").replace("chromium-browser", "chromium"),
        "browser_labels":       _BROWSER_LABELS,
        "api_key":              api_key,
        "search_boost_page_size": search_boost_page_size,
        "diaas_overrides":      diaas_overrides,
        "nutrient_target_rows": nutrient_target_rows,
        "diet_bioavailability_note": iron_zinc_bioavailability_note(diet_pref),
        "meal_list_nutrient_rows": meal_list_nutrient_rows,
        "meal_list_nutrients_max": MAX_MEAL_LIST_NUTRIENTS,
        "oxalate_available":    oxalate_available,
        "starter_data_loaded":  demo_data_loaded,
        "starter_food_count":   len(_demo_data.DEMO_FOODS),
        "starter_pantry_count": len(_demo_data.DEMO_PANTRY),
        "starter_recipe_count": len(_demo_data.DEMO_RECIPES),
        "starter_gi_count":     sum(1 for f in _demo_data.DEMO_FOODS if f.get("gi")),
        "starter_status":       starter_status,
        "starter_changes":      starter_changes,
        "starter_change_details": starter_change_details,
        "starter_new_food_ids": {f["fdc_id"] for f in starter_changes["new_foods"]},
        "recompute_errors":     recompute_errors,
        "recompute_retry":      recompute_retry,
        "gi_table":             _gi_lookup.active_table_info(),
        "gi_table_candidates":  _gi_lookup.local_table_candidates(),
        "gi_opt_out":           _gi_opt_out(),
        "gi_build":             gi_build,
        "gi_build_error":       gi_build_error,
    })


@app.post("/settings", response_class=RedirectResponse)
async def settings_post(
    age:            int   = Form(...),
    sex:            str   = Form(...),
    weight:         float = Form(...),
    weight_unit:    str   = Form("kg"),
    height_cm:      float = Form(0.0),
    height_ft:      int   = Form(0),
    height_in:      float = Form(0.0),
    height_unit:    str   = Form("cm"),
    activity_level: str   = Form(...),
    use_oxalate_data: str | None = Form(None),
    glucose_tolerance: str = Form(""),
):
    if height_unit == "imperial":
        height_cm_val = _profile.ftin_to_cm(height_ft, height_in)
    else:
        height_cm_val = height_cm

    weight_kg = _profile.lb_to_kg(weight) if weight_unit == "lb" else weight

    existing = _profile.load_profile()
    profile = _profile.UserProfile(
        age=age,
        sex=sex,
        weight_kg=round(weight_kg, 2),
        height_cm=round(height_cm_val, 1),
        activity_level=activity_level,
        weight_unit=weight_unit,
        height_unit=height_unit,
        use_oxalate_data=bool(use_oxalate_data),
        glucose_tolerance=glucose_tolerance if glucose_tolerance in ("normal", "impaired") else "",
        optimal_targets=dict(existing.optimal_targets) if existing else {},
        max_limits=dict(existing.max_limits) if existing else {},
    )
    _profile.save_profile(profile)
    return RedirectResponse("/settings?saved=profile", status_code=303)


@app.post("/settings/diet", response_class=RedirectResponse)
async def settings_diet_post(diet_pref: str = Form(...), next: str = Form(None)):
    if diet_pref in _VALID_DIET_PREFS:
        _save_prefs_file({"diet_pref": diet_pref})
    if next and next.startswith("/") and not next.startswith("//"):
        return RedirectResponse(next, status_code=303)
    return RedirectResponse("/settings?saved=diet", status_code=303)


@app.post("/update-notice/ack-banner", response_class=RedirectResponse)
async def update_notice_ack_banner(tag: str = Form(...)):
    """'Don't show this again for this version' on the home-page "update
    available" banner — dismisses only that exact release; a newer one
    still shows normally, same as the System Issues banner's 'Got it'."""
    _save_prefs_file({"update_notice_dismissed_tag": tag})
    return RedirectResponse("/", status_code=303)


@app.post("/check-for-updates", response_class=RedirectResponse)
async def check_for_updates_now():
    """Manually re-check GitHub for a new release right now — for anyone who
    dismissed a release and changed their mind (clears the dismissal) or
    doesn't want to wait for the periodic check's cache to refresh."""
    _update_check.clear_cache()
    _manual_update.clear_cache()
    _save_prefs_file({"update_notice_dismissed_tag": "", "manual_notice_dismissed_stamp": ""})
    return RedirectResponse("/", status_code=303)


def _data_check_reminder_prefs() -> dict:
    prefs = _load_prefs_file()
    try:
        weeks = max(0, int(prefs.get("data_check_reminder_weeks", 0)))
    except (TypeError, ValueError):
        weeks = 0
    return {"enabled": bool(prefs.get("data_check_reminder", True)), "weeks": weeks}


def _mark_starter_problems_seen(conn) -> None:
    """Record whatever the data checks find in starter foods and recipes as
    already seen, after starter data is loaded, restored or updated. Those
    come with the program (a spice with no amino-acid figures, a USDA record
    with no calories), not from anything the user did, so the Home page
    banner shouldn't greet a new user with them; Foods → 9 still lists them."""
    from numa_app.services import demo_data as _demo_data
    foods, recipes = _demo_data.starter_copies(conn)
    quality = _data_quality.scan(conn)
    keys = {k for k in quality["keys"]
            if k.split(":")[0] in ("food", "gap") and int(k.split(":")[1]) in foods}
    keys |= {f"stale:{s['where']}:{s['item_id']}" for s in quality["stale_amounts"]
             if s["where"] == "recipe" and s["owner_id"] in recipes}
    if keys:
        seen = set(_load_prefs_file().get("data_check_seen") or [])
        _save_prefs_file({"data_check_seen": sorted(seen | keys)})


def _data_check_reminder() -> dict | None:
    """The Home page's data-quality banner, or None. Issue-driven: shows
    only problems that weren't there when the user last opened Foods → 9
    (prefs data_check_seen, saved by that page), plus — if they asked for a
    routine — a nudge once data_check_reminder_weeks have passed with
    problems still open. Off entirely when the Settings toggle is off."""
    settings = _data_check_reminder_prefs()
    if not settings["enabled"]:
        return None
    with _db.get_db() as conn:
        keys = _data_quality.scan(conn)["keys"]
    if not keys:
        return None
    prefs = _load_prefs_file()
    seen = set(prefs.get("data_check_seen") or [])
    last = prefs.get("data_check_last_seen")
    new = keys - seen
    overdue = False
    if settings["weeks"] and last:
        try:
            age = (datetime.date.today() - datetime.date.fromisoformat(last)).days
            overdue = age >= settings["weeks"] * 7
        except ValueError:
            overdue = True
    if not new and not overdue:
        return None
    return {"new": len(new), "total": len(keys), "last_seen": last, "overdue": overdue and not new}


@app.post("/settings/data-check-reminder", response_class=RedirectResponse)
async def settings_data_check_reminder_post(enabled: list[str] = Form(default=[]), weeks: str = Form("0")):
    try:
        w = max(0, min(52, int(weeks or 0)))
    except ValueError:
        w = 0
    _save_prefs_file({"data_check_reminder": "1" in enabled, "data_check_reminder_weeks": w})
    return RedirectResponse("/settings?saved=data-check-reminder#data-check-reminder", status_code=303)


@app.post("/settings/browser", response_class=RedirectResponse)
async def settings_browser_post(preferred_browser: str = Form(""), next: str = Form(None)):
    if preferred_browser in _VALID_BROWSER_PREFS:
        _save_prefs_file({"preferred_browser": preferred_browser})
    if next and next.startswith("/") and not next.startswith("//"):
        return RedirectResponse(next, status_code=303)
    return RedirectResponse("/settings?saved=browser", status_code=303)


@app.post("/settings/api-key", response_class=RedirectResponse)
async def settings_api_key_post(api_key: str = Form("")):
    _usda.set_api_key(api_key.strip())
    return RedirectResponse("/settings?saved=api_key", status_code=303)


@app.post("/settings/search-boost", response_class=RedirectResponse)
async def settings_search_boost_post(search_boost_page_size: int = Form(...)):
    if search_boost_page_size >= 0:
        _usda.set_search_boost_page_size(search_boost_page_size)
        return RedirectResponse("/settings?saved=search_boost", status_code=303)
    return RedirectResponse("/settings", status_code=303)


@app.post("/settings/diaas-override", response_class=RedirectResponse)
async def settings_diaas_override_post(
    food_name:     str   = Form(...),
    digestibility: float = Form(...),
    notes:         str   = Form(""),
):
    food_name = food_name.strip()
    if food_name and 0.0 <= digestibility <= 1.0:
        with _db.get_db() as conn:
            _diaas.diaas_override_set(conn, food_name, digestibility, notes.strip() or None)
    return RedirectResponse("/settings?saved=diaas", status_code=303)


@app.post("/settings/diaas-override/delete", response_class=RedirectResponse)
async def settings_diaas_override_delete(request: Request, food_name: str = Form(...)):
    with _db.get_db() as conn:
        _diaas.diaas_override_delete(conn, food_name.strip())
    if _is_ajax_row_action(request):
        return JSONResponse({"ok": True})
    return RedirectResponse("/settings?saved=diaas", status_code=303)


@app.post("/settings/nutrient-target", response_class=RedirectResponse)
async def settings_nutrient_target_post(
    key:      str   = Form(...),
    optimal:  str   = Form(""),
    limit:    str   = Form(""),
):
    """Set or clear a Profile Optimal target and/or custom max limit for one nutrient.
    An empty field clears that setting; a numeric value sets it."""
    profile = _profile.load_profile()
    if profile is None:
        return RedirectResponse("/settings", status_code=303)

    valid_keys = {k for _g, keys in _NUTRIENT_TARGET_GROUPS for k in keys}
    if key in valid_keys:
        optimal = optimal.strip()
        if optimal:
            try:
                profile.optimal_targets[key] = float(optimal)
            except ValueError:
                pass
        else:
            profile.optimal_targets.pop(key, None)

        limit = limit.strip()
        if limit:
            try:
                profile.max_limits[key] = float(limit)
            except ValueError:
                pass
        else:
            profile.max_limits.pop(key, None)

        _profile.save_profile(profile)
    return RedirectResponse("/settings?saved=nutrient_target#nutrient-targets", status_code=303)


@app.post("/settings/nutrient-target/load-defaults", response_class=RedirectResponse)
async def settings_nutrient_target_load_defaults():
    """Apply profile.compute_optimal_defaults() to any nutrient the user
    hasn't already customized."""
    profile = _profile.load_profile()
    if profile is None:
        return RedirectResponse("/settings", status_code=303)

    defaults = _profile.compute_optimal_defaults(profile)
    for key, val in defaults.items():
        if key not in profile.optimal_targets:
            profile.optimal_targets[key] = val
    _profile.save_profile(profile)
    return RedirectResponse("/settings?saved=nutrient_target_defaults#nutrient-targets", status_code=303)


_GI_PDF_MAX_BYTES = 20 * 1024 * 1024   # each real supplemental table is ~1.6 MB


@app.post("/settings/gi-table/build", response_class=RedirectResponse)
async def settings_gi_table_build(files: list[UploadFile] = File(...)):
    """Build the user's own 2021 GI table from the two supplemental-table PDFs
    they uploaded. Parsing takes about a minute, so it runs on a background
    thread (gi_table_build.start_build) and Settings polls until it's done.
    The uploads go to a temporary folder the build removes when it finishes."""
    import tempfile
    pdfs = [f for f in files if f.filename]
    if len(pdfs) != 2:
        return RedirectResponse("/settings?gi_build_error=count#gi-table", status_code=303)
    tmp_dir = Path(tempfile.mkdtemp(prefix="numa-gi-"))
    paths: list[Path] = []
    for i, upload in enumerate(pdfs):
        data = await upload.read(_GI_PDF_MAX_BYTES + 1)
        if len(data) > _GI_PDF_MAX_BYTES:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return RedirectResponse("/settings?gi_build_error=size#gi-table", status_code=303)
        path = tmp_dir / f"table_{i}.pdf"
        path.write_bytes(data)
        paths.append(path)
    if not _gi_table_build.start_build(paths, _gi_lookup.user_table_path(), cleanup_dir=tmp_dir):
        shutil.rmtree(tmp_dir, ignore_errors=True)
    return RedirectResponse("/settings#gi-table", status_code=303)


@app.post("/settings/starter-data/load", response_class=RedirectResponse)
async def settings_demo_data_load():
    """Populate a fresh install with starter foods/pantry/recipes to explore
    the app with. See numa_app.services.demo_data for what's inserted and
    why — a marker file lets settings_demo_data_clear() undo exactly this."""
    from numa_app.services import demo_data as _demo_data
    with _db.get_db() as conn:
        _demo_data.load_demo_data(conn)
        _mark_starter_problems_seen(conn)
    return RedirectResponse("/settings?saved=starter_data_loaded", status_code=303)


@app.post("/settings/starter-data/clear", response_class=RedirectResponse)
async def settings_demo_data_clear():
    """Remove exactly the starter foods/pantry/recipes settings_demo_data_load() added.

    A starter food the user has since used in a meal, recipe, or their pantry is
    kept (see clear_demo_data) — the count comes back so the page can say so
    rather than leaving the food there unexplained."""
    from numa_app.services import demo_data as _demo_data
    with _db.get_db() as conn:
        result = _demo_data.clear_demo_data(conn)
    params = {"saved": "starter_data_cleared"}
    if result.get("foods_kept"):
        params["kept"] = result["foods_kept"]
    if result.get("recipes_kept"):
        params["kept_recipes"] = result["recipes_kept"]
    if result.get("edited_kept"):
        params["kept_edited"] = result["edited_kept"]
    return RedirectResponse(f"/settings?{urlencode(params)}", status_code=303)


@app.post("/settings/starter-data/restore", response_class=RedirectResponse)
async def settings_demo_data_restore(request: Request):
    """Selectively re-add starter foods/pantry items/recipes checked in the
    Settings restore list, skipping anything already present. See
    numa_app.services.demo_data.restore_selected() for the dependency rules
    (a checked pantry item or recipe also restores its underlying food)."""
    from numa_app.services import demo_data as _demo_data
    form = await request.form()
    food_fdc_ids = [int(v) for v in form.getlist("food_fdc_id")]
    pantry_names = form.getlist("pantry_name")
    recipe_names = form.getlist("recipe_name")
    with _db.get_db() as conn:
        _demo_data.restore_selected(conn, food_fdc_ids, pantry_names, recipe_names)
        _mark_starter_problems_seen(conn)
    return RedirectResponse("/settings?saved=starter_data_restored#starter-data", status_code=303)


@app.post("/settings/starter-data/improve", response_class=RedirectResponse)
async def settings_starter_data_improve(request: Request):
    """Replace the user's copies of the checked starter items with this
    version's improved ones, in place — see demo_data.apply_improvements()."""
    from numa_app.services import demo_data as _demo_data
    form = await request.form()
    food_fdc_ids = [int(v) for v in form.getlist("improve_fdc_id")]
    recipe_names = form.getlist("improve_recipe_name")
    with _db.get_db() as conn:
        _demo_data.apply_improvements(conn, food_fdc_ids, recipe_names)
        _mark_starter_problems_seen(conn)
    return RedirectResponse("/settings?saved=starter_data_improved#starter-data", status_code=303)


@app.post("/settings/starter-data/keep-mine", response_class=RedirectResponse)
async def settings_starter_data_keep_mine():
    """Decline every pending starter improvement; the user's copies stay as they are."""
    from numa_app.services import demo_data as _demo_data
    _demo_data.decline_improvements()
    return RedirectResponse("/settings?saved=starter_data_kept#starter-data", status_code=303)


@app.post("/starter-notice/ack", response_class=RedirectResponse)
async def starter_notice_ack():
    """'Got it' on the home page's new/improved starter items notice. The
    items themselves stay listed in Settings -> 9 until dealt with."""
    from numa_app.services import demo_data as _demo_data
    _demo_data.acknowledge_version_changes()
    return RedirectResponse("/", status_code=303)


@app.post("/settings/meal-nutrients", response_class=RedirectResponse)
async def settings_meal_nutrients_post(request: Request):
    """Save the ordered list of extra nutrient columns for the Meals & Log list."""
    from numa_app.services.meal_list_columns import AVAILABLE_NUTRIENTS, sanitize as _sanitize_meal_nutrients
    form = await request.form()
    positioned: list[tuple[int, str]] = []
    for key, _label, _unit in AVAILABLE_NUTRIENTS:
        raw = str(form.get(f"pos_{key}", "")).strip()
        if raw:
            try:
                positioned.append((int(raw), key))
            except ValueError:
                pass
    positioned.sort(key=lambda pair: pair[0])
    keys = _sanitize_meal_nutrients([key for _, key in positioned])
    _save_prefs_file({"meal_list_nutrients": keys})
    return RedirectResponse("/settings?saved=meal_nutrients#meal-list-nutrients", status_code=303)


@app.post("/settings/meal-nutrients/restore-defaults", response_class=RedirectResponse)
async def settings_meal_nutrients_restore_defaults():
    """Put the Meals & Log / Recent Days columns back to DEFAULT_MEAL_LIST_NUTRIENTS."""
    from numa_app.services.meal_list_columns import DEFAULT_MEAL_LIST_NUTRIENTS
    _save_prefs_file({"meal_list_nutrients": list(DEFAULT_MEAL_LIST_NUTRIENTS)})
    return RedirectResponse("/settings?saved=meal_nutrients_defaults#meal-list-nutrients", status_code=303)


@app.post("/settings/recompute-error/{error_id}/resolve", response_class=RedirectResponse)
async def settings_recompute_error_resolve(error_id: int):
    """Retry the failed recompute right now, and only mark the log entry
    resolved if the retry actually succeeds — clicking this never just hides
    the entry while the underlying stale/uncomputed recipe is still broken."""
    outcome = "not_found"
    with _db.get_db() as conn:
        error = _db.get_recompute_error(conn, error_id)
        if error:
            try:
                if error["entity_type"] == "recipe" and error["entity_id"] is not None:
                    _recipe_dcp.recompute_recipe_dcp(error["entity_id"], conn)
                elif error["entity_type"] == "meal" and error["entity_id"] is not None:
                    _compute_and_store_meal_bcp(error["entity_id"])
                _db.resolve_recompute_error(conn, error_id)
                outcome = "resolved"
            except Exception as exc:
                _db.update_recompute_error(conn, error_id, f"Retry failed again: {exc}")
                outcome = "still_failing"
    return RedirectResponse(f"/settings?recompute_retry={outcome}#system-issues", status_code=303)


@app.post("/recipes/compute-bcp", response_class=RedirectResponse)
async def recipes_compute_bcp(redirect_to: str = Form("/recipes")):
    """Recompute and persist DCP/serving for every recipe with resolvable data.

    Recipes missing amino acid data on a significant ingredient, or with 0
    servings, are left as NC — that reflects a real data gap, not a bug."""
    with _db.get_db() as conn:
        all_recipes = [dict(r) for r in _db.recipe_list_recent(conn, limit=10000)]
    for recipe in all_recipes:
        with _db.get_db() as conn:
            try:
                _recipe_dcp.recompute_recipe_dcp(recipe["id"], conn)
            except Exception:
                pass
    return RedirectResponse(redirect_to, status_code=303)


_RECIPE_SORT_KEYS = {
    "name":       lambda r: (r["name"] or "").lower(),
    "recent":     lambda r: r["last_accessed_at"] or r["created_at"] or "",
    "dcp":        lambda r: r["dcp_g"] if r["dcp_g"] is not None else -1.0,
    "id":         lambda r: r["id"],
}


@app.get("/recipes", response_class=HTMLResponse)
async def recipes_list(request: Request, q: str = "", sort: str | None = None,
                        show_archived: bool | None = None, archived: int = 0,
                        restored: int = 0, still_used: int = 0,
                        recipes_created: int = 0, recipes_reused: int = 0):
    sort = _resolve_sort(sort, "sort_recipes", "name", set(_RECIPE_SORT_KEYS))
    show_archived = _resolve_bool_pref(show_archived, "show_archived_recipes")
    with _db.get_db() as conn:
        total_count = _db.recipe_count(conn, include_archived=show_archived)
        all_recipes = [dict(r) for r in _db.recipe_list_recent(conn, limit=200, include_archived=show_archived)]
    if q:
        ql = q.lower()
        words = ql.split()
        all_recipes = [r for r in all_recipes if any(w in r["name"].lower() for w in words)]
    reverse = sort in ("recent", "dcp")
    all_recipes.sort(key=_RECIPE_SORT_KEYS[sort], reverse=reverse)
    return templates.TemplateResponse(request, "recipes.html", {
        "recipes": all_recipes,
        "total_count": total_count,
        "q": q,
        "sort": sort,
        "show_archived": show_archived,
        "archived": archived,
        "restored": restored,
        "still_used": still_used,
        "recipes_created": recipes_created,
        "recipes_reused": recipes_reused,
    })


@app.get("/recipes/broken-refs", response_class=HTMLResponse)
async def recipes_broken_refs(request: Request):
    with _db.get_db() as conn:
        broken = _db.list_all_broken_recipe_refs(conn)
    return templates.TemplateResponse(request, "recipe_broken_refs.html", {
        "meals":   broken["meals"],
        "recipes": broken["recipes"],
    })


@app.get("/recipe/import-csv", response_class=HTMLResponse)
async def recipe_import_csv_get(request: Request):
    return templates.TemplateResponse(request, "recipe_import_csv.html", {
        "recipes_text": "",
        "foods_text":   "",
        "review":       None,
    })


@app.post("/recipe/import-csv", response_class=HTMLResponse)
async def recipe_import_csv_post(request: Request,
                                  action: str = Form("preview"),
                                  recipes_text: str = Form(""),
                                  foods_text: str = Form(""),
                                  recipes_file: UploadFile | None = File(None),
                                  foods_file: UploadFile | None = File(None)):
    if recipes_file is not None and recipes_file.filename:
        recipes_text = (await recipes_file.read()).decode("utf-8-sig", errors="replace")
    if foods_file is not None and foods_file.filename:
        foods_text = (await foods_file.read()).decode("utf-8-sig", errors="replace")

    recipes, recipe_warnings = _recipe_csv.parse_recipes_csv(recipes_text)
    food_valid, food_warnings = _csv_import.parse_foods_csv(foods_text) if foods_text.strip() else ([], [])
    warnings = recipe_warnings + food_warnings

    if action == "confirm" and recipes:
        with _db.get_db() as conn:
            result = _recipe_csv.import_recipe_bundle(conn, recipes, food_valid)
        params = {
            "recipes_created": result["recipes_created"],
            "recipes_reused":  result["recipes_reused"],
        }
        return RedirectResponse(f"/recipes?{urlencode(params)}", status_code=303)

    with _db.get_db() as conn:
        existing_names = {r["name"].strip().lower() for r in _db.recipe_list(conn, include_archived=True)}
    review_rows = [{
        "name":            r["name"],
        "servings":        r["servings"],
        "ingredient_count": len(r["ingredients"]),
        "duplicate":       r["name"].strip().lower() in existing_names,
    } for r in recipes]
    return templates.TemplateResponse(request, "recipe_import_csv.html", {
        "recipes_text": recipes_text,
        "foods_text":   foods_text,
        "review":       review_rows,
        "warnings":     warnings,
    })


@app.get("/recipe/new", response_class=HTMLResponse)
async def recipe_new_get(request: Request):
    return templates.TemplateResponse(request, "recipe_new.html", {})


@app.post("/recipe/new", response_class=RedirectResponse)
async def recipe_new_post(
    name: str = Form(...),
    description: str = Form(""),
    servings: float = Form(4),
    total_weight: str = Form(""),
    total_weight_unit: str = Form("g"),
):
    name = name.strip()
    if not name:
        return RedirectResponse("/recipe/new", status_code=303)
    tw = float(total_weight) if total_weight.strip() else None
    with _db.get_db() as conn:
        rid = _db.recipe_create(
            conn, name=name, description=description.strip(),
            servings=servings, instructions="",
            total_weight=tw,
            total_weight_unit=total_weight_unit if tw else None,
        )
    return RedirectResponse(f"/recipe/{rid}/edit", status_code=303)


# Compare (foods + recipes, mixed)
# ---------------------------------------------------------------------------

_MAX_COMPARE_ITEMS = 8


def _parse_compare_items(items_str: str) -> list[tuple[str, int]]:
    """Parse the `items` query/form string ("f174,r12,f998") into
    [(kind, id), ...] pairs — "f" = food (fdc_id), "r" = recipe (recipe_id)."""
    items = []
    for tok in items_str.split(","):
        tok = tok.strip()
        if not tok:
            continue
        kind = "recipe" if tok[0] == "r" else "food"
        try:
            items.append((kind, int(tok[1:])))
        except ValueError:
            continue
    return items


def _compare_items_str(items: list[tuple[str, int]]) -> str:
    return ",".join(f"{'r' if kind == 'recipe' else 'f'}{id_}" for kind, id_ in items)


def _safe_return_to(return_to: str) -> str:
    """A Compare "return to" target is only ever a path inside numa —
    anything else (another site, a protocol-relative //host) is dropped."""
    return_to = (return_to or "").strip()
    if not return_to.startswith("/") or return_to.startswith("//") or "\\" in return_to:
        return ""
    return return_to


def _with_return(url: str, return_to: str) -> str:
    """Carry Compare's return_to through its own add/remove/save round-trips,
    so the "Back to ..." button survives every action on the page."""
    return_to = _safe_return_to(return_to)
    if not return_to:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}return_to={quote(return_to, safe='')}"


def _compare_return_label(return_to: str) -> str:
    """Button text for Compare's return button: names the custom profile
    being edited when that is where the user came from."""
    path = re.split(r"[?#]", return_to)[0]
    for pattern, verb in ((r"/food/custom-profiles/(-?\d+)/edit", "editing"),
                          (r"/food/(-?\d+)/fill-from", "filling in")):
        m = re.fullmatch(pattern, path)
        if m:
            with _db.get_db() as conn:
                row = _db.get_cached_food(conn, int(m.group(1)))
            if row:
                return f"Back to {verb} {row['name']}"
    return "Back to the page you came from"


def _load_compare_entry(conn, kind: str, id_: int) -> dict | None:
    """Load one comparison entry (food or recipe), normalized to a common,
    always-per-100g shape: {kind, id, name, data_type, nutrients,
    ingredients, diaas, cached, has_aa, weight_complete}. Every comparison
    on this page — ingredients, protein quality, nutrients — is judged per
    100g of the item, since a food's natural unit (grams) and a recipe's
    (servings) aren't otherwise a comparable amount to sit side by side.
    `ingredients` is a single self-referencing 100g row for a food (so the
    shared-ingredient table can include it too), or the recipe's own
    ingredients rescaled to add up to 100g of the finished dish.
    `weight_complete` is False when a recipe's ingredient weight (and so
    its 100g scaling) is only a lower-bound estimate — ingredients/nutrients
    are then left empty rather than scaled against an unreliable weight."""
    if kind == "food":
        cached = _db.get_cached_food(conn, id_)
        if cached:
            nutrients_100g = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
            name = cached["name"]
            data_type = cached["data_type"] or ""
        else:
            try:
                detail = _usda.get_food_detail(id_)
                nutrients_100g = detail.get("nutrients", {})
                name = detail["name"]
                data_type = detail.get("dataType", "")
            except Exception:
                nutrients_100g, name, data_type = {}, str(id_), ""
        diaas_display = None
        if nutrients_100g:
            try:
                diaas_result = _diaas.meal_level_diaas(
                    [{"food_name": name, "nutrients_100g": nutrients_100g, "grams": 100.0}], conn,
                )
            except Exception:
                diaas_result = None
            diaas_display = _build_diaas_display(diaas_result)
        return {
            "kind":            "food",
            "id":              id_,
            "name":            name,
            "data_type":       data_type,
            "nutrients":       nutrients_100g,
            "ingredients":     [{"food_name": name, "ref_recipe_id": None, "display": "100 g"}],
            "diaas":           diaas_display,
            "cached":          cached is not None,
            "has_aa":          _usda.has_confirmed_aa_data(nutrients_100g),
            "weight_complete": True,
        }

    recipe = _db.recipe_get(conn, id_)
    if not recipe:
        return None
    weight = _db.recipe_compute_weight(conn, id_)
    batch_grams, weight_complete = weight if weight else (0.0, False)
    scale = 100.0 / batch_grams if batch_grams else None

    nutrients: dict = {}
    ingredients: list[dict] = []
    diaas_display = None
    if scale:
        batch_nutrients = recipe_total_nutrients(id_, conn)
        nutrients = {k: v * scale for k, v in batch_nutrients.items()}
        for ing in _db.recipe_get_ingredients(conn, id_):
            scaled_amount = round(ing["amount"] * scale, 2)
            unit_word = "servings" if ing["ref_recipe_id"] else "g"
            if unit_word == "servings" and scaled_amount == 1:
                unit_word = "serving"
            ingredients.append({
                "food_name":     ing["food_name"],
                "ref_recipe_id": ing["ref_recipe_id"],
                "display":       f"{scaled_amount:g} {unit_word}",
            })
        diaas_ingredients = atomic_recipe_ingredients(id_, conn, portion_factor=scale)
        if diaas_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(diaas_ingredients, conn)
            except Exception:
                diaas_result = None
            diaas_display = _build_diaas_display(diaas_result)

    return {
        "kind":            "recipe",
        "id":              id_,
        "name":            recipe["name"],
        "data_type":       "Recipe",
        "nutrients":       nutrients,
        "ingredients":     ingredients,
        "diaas":           diaas_display,
        "cached":          True,
        "has_aa":          diaas_display is not None,
        "weight_complete": weight_complete,
    }


def _load_compare_entries(items: list[tuple[str, int]]) -> list[dict]:
    entries = []
    for kind, id_ in items:
        with _db.get_db() as conn:
            entry = _load_compare_entry(conn, kind, id_)
        if entry:
            entries.append(entry)
    return entries


def _build_protein_quality_rows(entries: list[dict]) -> list[dict]:
    """Build protein-quality comparison rows (DIAAS score, limiting amino acid,
    raw vs. digestible complete protein) — one row per metric, one cell per
    recipe. Highest value per numeric row is flagged for highlighting."""
    def _numeric_row(label, unit, getter):
        values = [e["diaas"].get(getter) if e["diaas"] else None for e in entries]
        numeric = [v for v in values if v is not None]
        max_val = max(numeric) if numeric else None
        cells = [
            {"value": v, "is_max": (v is not None and max_val is not None and v == max_val)}
            for v in values
        ]
        return {"label": label, "unit": unit, "cells": cells}

    for e in entries:
        if e["diaas"] and e["diaas"].get("eff_pct") is not None:
            e["diaas"]["eff_pct"] = int(e["diaas"]["eff_pct"])

    rows = [
        _numeric_row("Composite DIAAS score", "", "score"),
        _numeric_row("Raw protein", "g", "total_protein_g"),
        _numeric_row("Digestible complete protein (DCP)", "g", "dcp_g"),
        _numeric_row("DCP as % of raw protein", "%", "eff_pct"),
    ]
    limiting_cells = [
        {"value": e["diaas"].get("limiting_label") if e["diaas"] else None, "is_max": False}
        for e in entries
    ]
    rows.append({"label": "Limiting amino acid", "unit": "", "cells": limiting_cells})
    return rows if any(e["diaas"] for e in entries) else []


def _build_recipe_ingredient_rows(entries: list[dict]) -> list[dict]:
    """Union of ingredient names across the given entries into one row per
    distinct ingredient, one cell per entry holding its (already 100g-scaled)
    display amount, or None if that entry doesn't use it. Ingredients shared
    by 2+ entries are listed first — that's the interesting case for
    spotting why recipes differ — then entry-unique ingredients, both
    alphabetized."""
    rows_by_name: dict[str, dict] = {}
    for i, entry in enumerate(entries):
        for ing in entry["ingredients"]:
            row = rows_by_name.setdefault(ing["food_name"], {
                "name":      ing["food_name"],
                "is_recipe": bool(ing["ref_recipe_id"]),
                "cells":     [None] * len(entries),
            })
            row["cells"][i] = {"display": ing["display"]}
    rows = list(rows_by_name.values())
    for row in rows:
        row["shared_count"] = sum(1 for c in row["cells"] if c is not None)
    rows.sort(key=lambda r: (-r["shared_count"], r["name"].lower()))
    return rows


@app.get("/compare", response_class=HTMLResponse)
async def compare_get(
    request: Request,
    items: str = "",
    error: str = "",
    search: str = "",
    source: list[str] | None = Query(default=None),
    limit: int | None = None,
    return_to: str = "",
):
    source = _resolve_source_filter(source, "sort_food_search_source", _SEARCH_SOURCE_FILTERS)
    limit = _resolve_result_limit(limit)
    return_to = _safe_return_to(return_to)
    item_list = _parse_compare_items(items)
    entries = _load_compare_entries(item_list) if item_list else []
    compare_groups = _build_compare_groups(entries) if len(entries) >= 2 else []
    ingredient_rows = _build_recipe_ingredient_rows(entries) if len(entries) >= 2 else []
    protein_quality_rows = _build_protein_quality_rows(entries) if len(entries) >= 2 else []
    items_str = _compare_items_str(item_list)

    search_results: list[dict] = []
    search_error: str | None = None
    search = search.strip()
    if search:
        seen = {(kind, id_) for kind, id_ in item_list}
        search_results = _search_local_results(search)
        for r in search_results:
            key = ("recipe", r["recipe_id"]) if r.get("_type") == "recipe" else ("food", r.get("fdc_id"))
            seen.add(key)
        try:
            for food in _usda.search_foods(search, page_size=limit):
                fid = food.get("fdcId")
                if fid and ("food", fid) not in seen:
                    seen.add(("food", fid))
                    search_results.append({
                        "fdc_id":    fid,
                        "name":      food.get("description", ""),
                        "data_type": food.get("dataType", ""),
                        "brand":     food.get("brandOwner") or food.get("brandName") or "",
                        "source":    "usda",
                    })
        except Exception as exc:
            if not search_results:
                search_error = f"USDA API unavailable: {exc}"
        search_results = _sort_search_results(search_results, search, _resolve_sort(None, "sort_food_search", "relevance", _SEARCH_SORT_MODES))
        search_results = _cap_results_preserving_local(_filter_search_results_by_source(search_results, source), limit)

    with _db.get_db() as conn:
        saved_lists = _db.saved_mixed_comparison_list(conn)

    return templates.TemplateResponse(request, "compare.html", {
        "entries":              entries,
        "compare_groups":       compare_groups,
        "ingredient_rows":      ingredient_rows,
        "protein_quality_rows": protein_quality_rows,
        "items_str":            items_str,
        "error":                error,
        "search":               search,
        "search_results":       search_results,
        "search_error":         search_error,
        "saved_lists":          saved_lists,
        "source":               source,
        "limit":                limit,
        "source_filters":       _SEARCH_SOURCE_FILTERS,
        "source_labels":        _SEARCH_SOURCE_LABELS,
        "max_items":            _MAX_COMPARE_ITEMS,
        "return_to":            return_to,
        "return_label":         _compare_return_label(return_to) if return_to else "",
        "return_qs":            _with_return("", return_to),
    })


@app.get("/compare/export.csv")
async def compare_export_csv(items: str = ""):
    item_list = _parse_compare_items(items)
    entries = _load_compare_entries(item_list) if item_list else []
    compare_groups = _build_compare_groups(entries) if len(entries) >= 2 else []
    csv_text = _csv_export.compare_to_csv(entries, compare_groups)
    filename = f"numa_compare_{datetime.date.today().isoformat()}.csv"
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/compare/add", response_class=RedirectResponse)
async def compare_add(
    kind:    str = Form(...),
    item_id: int = Form(...),
    items:   str = Form(""),    return_to: str = Form(""),
):
    kind = "recipe" if kind == "recipe" else "food"
    item_list = _parse_compare_items(items)
    if len(item_list) >= _MAX_COMPARE_ITEMS:
        return RedirectResponse(
            _with_return(f"/compare?items={_compare_items_str(item_list)}"
                         f"&error=Maximum+{_MAX_COMPARE_ITEMS}+items+allowed", return_to),
            status_code=303,
        )
    if (kind, item_id) not in item_list:
        item_list.append((kind, item_id))
    return RedirectResponse(_with_return(f"/compare?items={_compare_items_str(item_list)}", return_to), status_code=303)


@app.post("/compare/add-multiple", response_class=RedirectResponse)
async def compare_add_multiple(request: Request, items: str = Form(""), return_to: str = Form("")):
    """Bulk-add checked foods/recipes to the comparison — used both by
    Compare's own "add via search" panel and by the compare checkboxes on
    Foods search, Food Cache, My Pantry, and the Recipes list (which post
    straight here to jump into a comparison without first landing on this
    page)."""
    form = await request.form()
    fdc_ids = form.getlist("fdc_id")
    recipe_ids = form.getlist("recipe_id")
    item_list = _parse_compare_items(items)
    added = skipped = 0
    for kind, id_strs in (("food", fdc_ids), ("recipe", recipe_ids)):
        for id_str in id_strs:
            try:
                id_ = int(id_str)
            except (ValueError, TypeError):
                continue
            if (kind, id_) in item_list:
                continue
            if len(item_list) >= _MAX_COMPARE_ITEMS:
                skipped += 1
                continue
            item_list.append((kind, id_))
            added += 1
    url = f"/compare?items={_compare_items_str(item_list)}"
    if skipped:
        url += f"&error=Added+{added}%2C+skipped+{skipped}+%E2%80%94+maximum+{_MAX_COMPARE_ITEMS}+items"
    return RedirectResponse(_with_return(url, return_to), status_code=303)


@app.post("/compare/remove", response_class=RedirectResponse)
async def compare_remove(
    remove_kind: str = Form(...),
    remove_id:   int = Form(...),
    items:       str = Form(""),    return_to: str = Form(""),
):
    remove_kind = "recipe" if remove_kind == "recipe" else "food"
    item_list = [it for it in _parse_compare_items(items) if it != (remove_kind, remove_id)]
    return RedirectResponse(_with_return(f"/compare?items={_compare_items_str(item_list)}", return_to), status_code=303)


@app.post("/compare/cache-food", response_class=RedirectResponse)
async def compare_cache_food(
    fdc_id: int = Form(...),
    items:  str = Form(""),    return_to: str = Form(""),
):
    with _db.get_db() as conn:
        already_cached = _db.get_cached_food(conn, fdc_id) is not None
    if not already_cached:
        try:
            detail = _usda.get_food_detail(fdc_id)
            with _db.get_db() as conn:
                _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                               data_type=detail.get("dataType", ""),
                               brand=detail.get("brand"),
                               serving_size=detail.get("servingSize"),
                               serving_unit=detail.get("servingUnit"),
                               nutrients=detail.get("nutrients", {}),
                               portions=detail.get("portions", []))
                _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
        except Exception:
            pass
    return RedirectResponse(_with_return(f"/compare?items={items}", return_to), status_code=303)


@app.post("/compare/save", response_class=RedirectResponse)
async def compare_save(
    name:  str = Form(""),
    items: str = Form(""),    return_to: str = Form(""),
):
    item_list = _parse_compare_items(items)
    if len(item_list) >= 2:
        with _db.get_db() as conn:
            _db.saved_mixed_comparison_save(
                conn, name.strip() or "Untitled",
                [{"kind": kind, "id": id_} for kind, id_ in item_list],
            )
    return RedirectResponse(_with_return(f"/compare?items={_compare_items_str(item_list)}", return_to), status_code=303)


@app.get("/compare/load/{cmp_id}", response_class=RedirectResponse)
async def compare_load(cmp_id: int, return_to: str = ""):
    with _db.get_db() as conn:
        row = _db.saved_mixed_comparison_get(conn, cmp_id)
    if not row:
        return RedirectResponse(_with_return("/compare", return_to), status_code=303)
    stored_items = json.loads(row["items"])
    items_str = ",".join(f"{'r' if it['kind'] == 'recipe' else 'f'}{it['id']}" for it in stored_items)
    return RedirectResponse(_with_return(f"/compare?items={items_str}", return_to), status_code=303)


@app.post("/compare/saved/rename", response_class=RedirectResponse)
async def compare_saved_rename(
    cmp_id: int = Form(...),
    name:   str = Form(""),
    items:  str = Form(""),    return_to: str = Form(""),
):
    new_name = name.strip() or "Untitled"
    with _db.get_db() as conn:
        _db.saved_mixed_comparison_rename(conn, cmp_id, new_name)
    url = f"/compare?items={items}" if items else "/compare"
    return RedirectResponse(_with_return(url, return_to), status_code=303)


@app.post("/compare/saved/delete", response_class=RedirectResponse)
async def compare_saved_delete(
    cmp_id: int = Form(...),
    items:  str = Form(""),    return_to: str = Form(""),
):
    with _db.get_db() as conn:
        _db.saved_mixed_comparison_delete(conn, cmp_id)
    items_str = items.strip()
    url = f"/compare?items={items_str}" if items_str else "/compare"
    return RedirectResponse(_with_return(url, return_to), status_code=303)


def _recipe_detail_context(recipe_id: int, servings: float | None,
                            ignore_complements: list[str], unignore: list[str],
                            comp_sort: str | None = None, diaas_sort: str | None = None,
                            rank: str | None = None, top_n: str | None = None,
                            anchor_name: list[str] | None = None,
                            anchor_grams: list[str] | None = None) -> dict | None:
    top_n = _resolve_contributor_top_n(top_n)
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return None
        _db.recipe_touch(conn, recipe_id)
        ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, recipe_id)]
        for _ing in ingredients:
            if not _ing["ref_recipe_id"] and _ing["amount"]:
                _ing["volume_display"] = _ingredient_volume_display(conn, _ing)
            if not _ing["ref_recipe_id"]:
                _ing["amount_display"] = _ingredient_amount_display(conn, _ing)
                _ing["typed_note"] = _typed_amount_note(_ing["amount_display"])
        _attach_ref_serving_sizes(conn, ingredients)
        _mark_generic_density(conn, ingredients)
        referencing_recipes = _db.recipe_referencing_subrecipe(conn, recipe_id)
        per_serving = _recipe_nutrients_per_serving(recipe_id, conn)
        recipe_servings = float(recipe["servings"] or 1)
        if servings is None:
            servings = 1.0

        diaas_ingredients = _flatten_recipe_diaas_ingredients(recipe_id, conn, servings)
        # Every leaf food, sub-recipes opened up — diaas_ingredients keeps a
        # sub-recipe atomic, which would hide its foods' calorie problems.
        calorie_leaves = expand_recipe_ingredients(recipe_id, conn,
                                                   portion_factor=servings / recipe_servings)

        diaas_result = None
        if diaas_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(diaas_ingredients, conn)
            except Exception:
                pass

        # Complement suggestions are sized against the recipe's own full total
        # (see comment below), so they need the ingredient list at that same
        # whole-recipe basis — not diaas_ingredients above, which is scaled to
        # the "servings to analyze" widget instead.
        full_diaas_ingredients = _flatten_recipe_diaas_ingredients(recipe_id, conn, recipe_servings)

    scaled = {k: v * servings for k, v in per_serving.items()}
    # Complement suggestions are always sized against the recipe's own full total,
    # independent of the "servings to analyze" widget above — the only way to act
    # on a suggestion is to add an ingredient to the whole recipe batch.
    recipe_total_nutrients = {k: v * recipe_servings for k, v in per_serving.items()}
    rda = _load_rda()
    optimal = _load_optimal()
    max_limits = _load_max_limits()
    diaas_display = _build_diaas_display(diaas_result)

    ingredient_antinutrients = []
    for ing in ingredients:
        flags = _usda.get_antinutrient_flags(ing["food_name"])
        if flags:
            ingredient_antinutrients.append({"food_name": ing["food_name"], "flags": flags})

    # Oxalate: build items list from direct-food ingredients (skip sub-recipes)
    ox_items = [
        {"fdc_id": ing["fdc_id"], "food_name": ing["food_name"],
         "amount_g": float(ing["amount"]) * servings}
        for ing in ingredients if ing.get("fdc_id") and not ing.get("ref_recipe_id")
    ]
    oxalate = _oxalate_for_items(ox_items)

    contributor_options = _contributor_rank_options(scaled)
    if not rank or rank not in {k for _, opts in contributor_options for k, _ in opts}:
        rank = _default_rank_key(contributor_options)
    with _db.get_db() as conn:
        contributor_result = _build_contributors(diaas_ingredients, rank, top_n, conn)

    return {
        "recipe":                   dict(recipe),
        "calorie_warnings":         _calorie_warnings(calorie_leaves),
        "ingredients":              ingredients,
        "servings":                 servings,
        "contributor_options":      contributor_options,
        "contributor_rank":         rank,
        "contributor_unit":         _usda.nutrient_label(rank)[1] if rank else "",
        "contributors":             contributor_result["items"],
        "contributor_total":        contributor_result["total"],
        "contributor_count":        contributor_result["count"],
        "contributor_top_n":        contributor_result["top_n"],
        "contributor_top_n_options": contributor_result["top_n_options"],
        "contributor_is_dcp":       contributor_result["is_dcp"],
        "nutrient_sections":        _nutrient_sections(scaled, rda, optimal=optimal, max_limits=max_limits,
                                                       dcp_g=diaas_display["dcp_g"] if diaas_display else None,
                                                       dcp_missing=diaas_display["missing"] if diaas_display else None) if scaled else [],
        "diaas":                    diaas_display,
        "dcp_missing_names":        diaas_display["missing"] if diaas_display else [],
        "protein_adequacy":         _protein_adequacy(scaled, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":              _complement_suggestions(recipe_total_nutrients, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="recipe", exclude_recipe_id=recipe_id, ingredients=full_diaas_ingredients, exclude_names=_effective_ignored(ignore_complements, unignore), comp_sort=comp_sort, diaas_sort=diaas_sort, anchor_overrides=_parse_anchor_overrides(anchor_name or [], anchor_grams or [])),
        "ignored_complements":      sorted(_effective_ignored(ignore_complements, unignore)),
        "gl":                       _recipe_gl_web(recipe_id, recipe_servings, servings),
        "has_profile":              rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
        "ingredient_antinutrients": ingredient_antinutrients,
        "oxalate":                  oxalate,
        "referencing_recipes":      referencing_recipes,
    }


@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe_detail(request: Request, recipe_id: int, servings: float | None = None,
                         ignore_complements: list[str] = Query(default=[]),
                         unignore: list[str] = Query(default=[]),
                         comp_sort: str | None = None, diaas_sort: str | None = None,
                         anchor_name: list[str] = Query(default=[]),
                         anchor_grams: list[str] = Query(default=[]),
                         rank: str | None = None, top_n: str | None = None):
    comp_sort = _resolve_sort(comp_sort, "sort_complements", "dcp", _COMP_SORT_MODES)
    diaas_sort = _resolve_sort(diaas_sort, "sort_diaas_improvers", "effect", _DIAAS_SORT_MODES)
    ctx = _recipe_detail_context(recipe_id, servings, ignore_complements, unignore,
                                  comp_sort=comp_sort, diaas_sort=diaas_sort, rank=rank, top_n=top_n,
                                  anchor_name=anchor_name, anchor_grams=anchor_grams)
    if ctx is None:
        return RedirectResponse("/recipes", status_code=303)
    with _db.get_db() as conn:
        ctx["translations"] = _db.recipe_translation_list(conn, recipe_id)
    return templates.TemplateResponse(request, "recipe_detail.html", ctx)


@app.get("/recipe/{recipe_id}/export.csv")
async def recipe_export_csv(recipe_id: int):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        recipes_text, foods_text = _recipe_csv.render_recipe_export(conn, [recipe_id])

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("recipes.csv", recipes_text)
        zf.writestr("foods.csv", foods_text)
    safe_name = re.sub(r"[^\w\s-]", "", recipe["name"]).strip()
    safe_name = re.sub(r"\s+", "_", safe_name)[:60] or "recipe"
    filename = f"{safe_name}_{datetime.date.today().isoformat()}.zip"
    return Response(
        content=buf.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def _recipe_available_sections(ctx: dict) -> list[str]:
    available = []
    if ctx.get("recipe", {}).get("introduction"):
        available.append("introduction")
    if ctx.get("ingredients"):
        available.append("ingredients")
    if ctx.get("recipe", {}).get("instructions"):
        available.append("procedure")
    if ctx.get("nutrient_sections"):
        available.append("nutrient_table")
    if ctx.get("diaas"):
        available.append("protein_summary")
        available.append("protein_quality")
    gl = ctx.get("gl")
    if gl and gl.get("total") is not None:
        available.append("glycemic_load")
    if ctx.get("oxalate") or ctx.get("ingredient_antinutrients"):
        available.append("antinutrients")
    complements = ctx.get("complements")
    if complements and not complements.get("no_data"):
        available.append("complements")
    if ctx.get("recipe", {}).get("notes"):
        available.append("notes")
    return available


@app.get("/recipe/{recipe_id}/print", response_class=HTMLResponse)
async def recipe_print(
    request: Request,
    recipe_id: int,
    servings: float | None = None,
    sections: list[str] = Query(default=[]),
    sections_submitted: bool = Query(default=False),
    layout: str = Query(default=""),
    paper: str = Query(default=""),
    layout_submitted: bool = Query(default=False),
):
    ctx = _recipe_detail_context(recipe_id, servings, [], [])
    if ctx is None:
        return RedirectResponse("/recipes", status_code=303)

    available = _recipe_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("recipe", available, sections, sections_submitted, prefs)
    layout_ctx = _print_sections.resolve_layout_context(layout, paper, layout_submitted, prefs)
    save_update = layout_ctx.pop("_save_update")
    if sections_submitted or save_update:
        _save_prefs_file({**_print_sections.save_sections("recipe", enabled, prefs), **save_update})

    return templates.TemplateResponse(request, "print.html", {
        "title":              ctx["recipe"]["name"],
        "subtitle":           f"#{recipe_id} / {ctx['servings']} serving{'s' if ctx['servings'] != 1 else ''} analyzed"
                              f"{' · ' + str(ctx['recipe']['servings']) + ' servings per recipe' if ctx['recipe'].get('servings') else ''}"
                              f"{' (1 serving = ' + ctx['recipe']['serving_size'] + ')' if ctx['recipe'].get('serving_size') else ''}",
        "back_url":           f"/recipe/{recipe_id}",
        "back_label":         "Back to recipe",
        "fixed_params":       {"servings": ctx["servings"]},
        "section_labels":     _print_sections.PRINT_SECTION_LABELS,
        "available_sections": available,
        "enabled":            enabled,
        "portion_label":      f"{ctx['servings']} serving{'s' if ctx['servings'] != 1 else ''}",
        "oxalate_agg":        ctx["oxalate"],
        **layout_ctx,
        **{k: v for k, v in ctx.items() if k != "oxalate"},
    })


# ---------------------------------------------------------------------------
# Recipe translation workflow (manual AI paste) — see
# numa_app/services/recipe_translate.py for the prompt-building and
# response-parsing logic. numa never calls a translation API itself: the user
# pastes the generated prompt into their own AI chat tool, translates it, and
# pastes the reply back for review before it's optionally saved.
# ---------------------------------------------------------------------------

def _recipe_ingredients_with_volume(conn, recipe_id: int) -> list[dict]:
    ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, recipe_id)]
    for ing in ingredients:
        if not ing["ref_recipe_id"] and ing["amount"]:
            ing["volume_display"] = _ingredient_volume_display(conn, ing)
    _attach_ref_serving_sizes(conn, ingredients)
    return ingredients


def _ingredient_volume_display(conn, ing: dict) -> str | None:
    """Scale from the food's own portion data (a known fact, possibly just
    user-edited) rather than a generic density-based guess, which is
    frequently wrong and can even contradict a portion the user just set.
    When the food has no portion data, prompts the user to add it instead of
    guessing. Returns None only when there's no linked food to even point at
    (a freeform-typed ingredient with no fdc_id)."""
    fdc_id = ing.get("fdc_id")
    if not fdc_id:
        return None
    cached = _db.get_cached_food(conn, fdc_id)
    portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
    return portion_amount_note(ing["amount"], portions, fdc_id)


def _attach_ref_serving_sizes(conn, ingredients: list[dict]) -> None:
    """For each ingredient that's a nested sub-recipe (ref_recipe_id set),
    attach that sub-recipe's own serving_size (e.g. "1 muffin") as
    ref_serving_size, so ingredient-list displays showing "N srv" can show
    what a serving of that sub-recipe actually is, right alongside it.

    Also attaches ref_grams — what those N servings weigh — so the same
    displays can say how much food "N srv" is. It stays None when the
    sub-recipe's serving weight can't be worked out (see
    recipe_serving_grams)."""
    ref_ids = {ing["ref_recipe_id"] for ing in ingredients if ing.get("ref_recipe_id")}
    sizes = {}
    serving_grams: dict[int, float | None] = {}
    for rid in ref_ids:
        sub = _db.recipe_get(conn, rid)
        if sub:
            sizes[rid] = sub["serving_size"]
            serving_grams[rid] = recipe_serving_grams(rid, conn)
    for ing in ingredients:
        if ing.get("ref_recipe_id"):
            ing["ref_serving_size"] = sizes.get(ing["ref_recipe_id"])
            per_serving_g = serving_grams.get(ing["ref_recipe_id"])
            ing["ref_grams"] = per_serving_g * float(ing["amount"]) if per_serving_g and ing["amount"] else None


def _ingredient_amount_display(conn, ing: dict) -> str:
    """The amount for this ingredient exactly as the user typed it ("1/2 t",
    "3 T", "90 g"), for pages that present a recipe to read or cook from.

    Those pages used to show the gram weight numa derived from that entry,
    which is nonsense for something measured in spoons — "3 g of vanilla
    extract" is not a thing anyone does. The gram weight is still what every
    calculation uses; it just isn't what gets printed.

    "p1" (shorthand for "this food's first saved portion") is the one entry
    that means nothing to a reader, so it resolves back to that portion's own
    description ("1 large egg"), or to grams if the portion is gone.
    """
    label = _ing_amount_display(ing["unit"], ing["amount"], ing["food_name"])
    if not re.fullmatch(r"(?:[\d.]+\s*(?:x|×)?\s*)?p\d+", label.strip(), re.IGNORECASE):
        return label
    cached = _db.get_cached_food(conn, ing["fdc_id"]) if ing.get("fdc_id") else None
    portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
    parsed = _parse_portion_input(label, portions, ing["food_name"])
    if parsed and parsed[1]:
        return parsed[1]
    return f"{float(ing['amount'] or 0):g} g"


_GRAMS_FRAGMENT_RE = re.compile(r"\(?\s*\d[\d.,/]*\s*(?:g|gr|grams?)\b\.?\s*\)?", re.IGNORECASE)


def _typed_amount_note(label: str | None) -> str | None:
    """What the user typed for an ingredient, minus any gram figure in it,
    for the recipe page's "<grams> g (<this>)" amount column: "14.7 gr (2 T)"
    -> "2 T", "1/3 c" -> "1/3 c". None when the entry was only grams ("33 g"),
    so the caller falls back to the portion-derived hint, which then adds
    something the gram figure doesn't."""
    if not label:
        return None
    rest = _GRAMS_FRAGMENT_RE.sub(" ", label)
    rest = re.sub(r"\(\s*\)", " ", rest)
    rest = " ".join(rest.split()).strip(" ,;()")
    return rest or None


def _mark_generic_density(conn, ingredients: list[dict]) -> None:
    """Set ing["generic_density"] ("typed" / "bracketed" / None) on each food
    ingredient whose grams came from the generic density table, for the
    "≈ generic" mark and footnote (_generic_density.html) — see
    portions.generic_density_kind()."""
    for ing in ingredients:
        if ing.get("ref_recipe_id") or not ing.get("fdc_id"):
            continue
        cached = _db.get_cached_food(conn, ing["fdc_id"])
        if cached is None:
            continue
        portions = json.loads(cached["portions_json"] or "[]") or []
        ing["generic_density"] = _generic_density_kind(ing.get("unit"), portions, cached["name"])


def _attach_ingredient_portions(conn, ingredients: list[dict]) -> None:
    """Attach each food ingredient's cached USDA portions (p1, p2, …) so the
    inline amount-edit popup can show them the same way the Add Ingredient
    search results do — without this, editing an amount gives no hint of
    what "p1" etc. actually mean for that specific food."""
    for ing in ingredients:
        if ing.get("ref_recipe_id") or not ing.get("fdc_id"):
            continue
        cached = _db.get_cached_food(conn, ing["fdc_id"])
        ing["portions"] = (json.loads(cached["portions_json"] or "[]") or []) if cached else []


def _original_recipe_fields(recipe: dict, target_language: str) -> dict:
    return {
        "name":         recipe.get("name") or "",
        "description":  recipe.get("description") or "",
        "introduction": recipe.get("introduction") or "",
        "instructions": recipe.get("instructions") or "",
        "notes":        recipe.get("notes") or "",
        "disclaimer":   _recipe_translate.DISCLAIMER_TEMPLATE.format(language=target_language),
    }


def _render_translated_recipe(ctx: dict, translated: dict) -> dict:
    """Overlay translated display strings onto a copy of a recipe detail ctx.
    Never touches amounts, servings, or any nutrient data."""
    new_ctx = dict(ctx)

    recipe = dict(ctx["recipe"])
    for key in ("name", "description", "introduction", "instructions", "notes"):
        if translated.get(key):
            recipe[key] = translated[key]
    new_ctx["recipe"] = recipe

    translated_ingredients = translated.get("ingredients") or []
    new_ingredients = []
    for ing, tr in zip(ctx["ingredients"], translated_ingredients):
        new_ing = dict(ing)
        if tr.get("food_name"):
            new_ing["food_name"] = tr["food_name"]
        if tr.get("notes"):
            new_ing["notes"] = tr["notes"]
        orig_vol = ing.get("volume_display")
        trans_vol = tr.get("volume_display")
        if trans_vol and orig_vol:
            new_ing["volume_display"] = f"{trans_vol} ({orig_vol})"
        elif trans_vol:
            new_ing["volume_display"] = trans_vol
        new_ingredients.append(new_ing)
    new_ctx["ingredients"] = new_ingredients

    new_ctx["disclaimer"] = translated.get("disclaimer")
    new_ctx["translated"] = True
    return new_ctx


@app.get("/recipe/{recipe_id}/translate", response_class=HTMLResponse)
async def recipe_translate_get(request: Request, recipe_id: int, language: str = ""):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        ingredients = _recipe_ingredients_with_volume(conn, recipe_id)
        translations = _db.recipe_translation_list(conn, recipe_id)

    language = language.strip()
    prompt = ""
    if language:
        original = _original_recipe_fields(dict(recipe), language)
        prompt = _recipe_translate.build_translate_prompt(original, ingredients, language)

    return templates.TemplateResponse(request, "recipe_translate.html", {
        "recipe":       dict(recipe),
        "language":     language,
        "prompt":       prompt,
        "translations": translations,
    })


@app.get("/recipe/{recipe_id}/translate/import", response_class=HTMLResponse)
async def recipe_translate_import_get(request: Request, recipe_id: int, language: str = ""):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
    return templates.TemplateResponse(request, "recipe_translate_import.html", {
        "recipe_id":     recipe_id,
        "language":      language,
        "response_text": "",
        "preview":       None,
    })


@app.post("/recipe/{recipe_id}/translate/import", response_class=HTMLResponse)
async def recipe_translate_import_post(
    request: Request,
    recipe_id: int,
    response_text: str = Form(...),
    language: str = Form(...),
    action: str = Form("preview"),
):
    ctx = _recipe_detail_context(recipe_id, None, [], [])
    if ctx is None:
        return RedirectResponse("/recipes", status_code=303)

    original = _original_recipe_fields(ctx["recipe"], language)
    parsed = _recipe_translate.parse_translation_response(response_text)
    clean, warnings, hard_fail = _recipe_translate.validate_translation(
        original, ctx["ingredients"], parsed
    )

    if hard_fail:
        return templates.TemplateResponse(request, "recipe_translate_import.html", {
            "recipe_id":     recipe_id,
            "language":      language,
            "response_text": response_text,
            "preview":       None,
            "hard_fail":     True,
            "warnings":      warnings,
        })

    if action == "save":
        with _db.get_db() as conn:
            translation_id = _db.recipe_translation_create(conn, recipe_id, language, clean)
        return RedirectResponse(
            f"/recipe/{recipe_id}/translation/{translation_id}/print", status_code=303
        )

    preview_ctx = _render_translated_recipe(ctx, clean)
    return templates.TemplateResponse(request, "recipe_translate_import.html", {
        "recipe_id":     recipe_id,
        "language":      language,
        "response_text": response_text,
        "preview":       preview_ctx,
        "hard_fail":     False,
        "warnings":      warnings,
    })


@app.get("/recipe/{recipe_id}/translation/{translation_id}/print", response_class=HTMLResponse)
async def recipe_translation_print(
    request: Request,
    recipe_id: int,
    translation_id: int,
    sections: list[str] = Query(default=[]),
    sections_submitted: bool = Query(default=False),
    layout: str = Query(default=""),
    paper: str = Query(default=""),
    layout_submitted: bool = Query(default=False),
):
    ctx = _recipe_detail_context(recipe_id, None, [], [])
    if ctx is None:
        return RedirectResponse("/recipes", status_code=303)

    with _db.get_db() as conn:
        row = _db.recipe_translation_get(conn, translation_id)
    if not row or row["recipe_id"] != recipe_id:
        return RedirectResponse(f"/recipe/{recipe_id}", status_code=303)

    translated = json.loads(row["data_json"])
    ctx = _render_translated_recipe(ctx, translated)

    available = _recipe_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("recipe", available, sections, sections_submitted, prefs)
    layout_ctx = _print_sections.resolve_layout_context(layout, paper, layout_submitted, prefs)
    save_update = layout_ctx.pop("_save_update")
    if sections_submitted or save_update:
        _save_prefs_file({**_print_sections.save_sections("recipe", enabled, prefs), **save_update})

    return templates.TemplateResponse(request, "print.html", {
        "title":              ctx["recipe"]["name"],
        "subtitle":           f"{row['language']} translation",
        "back_url":           f"/recipe/{recipe_id}",
        "back_label":         "Back to recipe",
        "fixed_params":       {},
        "section_labels":     _print_sections.PRINT_SECTION_LABELS,
        "available_sections": available,
        "enabled":            enabled,
        "portion_label":      f"{ctx['servings']} serving{'s' if ctx['servings'] != 1 else ''}",
        "oxalate_agg":        ctx["oxalate"],
        **layout_ctx,
        **{k: v for k, v in ctx.items() if k != "oxalate"},
    })


@app.post("/recipe/{recipe_id}/translation/{translation_id}/delete", response_class=RedirectResponse)
async def recipe_translation_delete(request: Request, recipe_id: int, translation_id: int):
    with _db.get_db() as conn:
        _db.recipe_translation_delete(conn, translation_id)
    if _is_ajax_row_action(request):
        return JSONResponse({"ok": True})
    return RedirectResponse(f"/recipe/{recipe_id}", status_code=303)


@app.get("/recipe/{recipe_id}/edit", response_class=HTMLResponse)
async def recipe_edit_get(request: Request, recipe_id: int, q: str = "", saved: str = "", error: str = "",
                           relinked: str = "", relinked_to: str = "", added_check: str = "",
                           source: list[str] | None = Query(default=None),
                           limit: int | None = None):
    # Keep the "Add Ingredient" panel open across a reload triggered from
    # inside it (Search, Reset all sources to ON, Refresh search) even when
    # the query box is empty — otherwise a source-filter change with no q
    # yet typed would collapse the panel the user was just using.
    show_add_section = bool(q) or "source" in request.query_params or "limit" in request.query_params
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        broken_refs = _db.find_broken_recipe_refs(conn, recipe["name"])
        _broken_groups: dict[str, dict] = {}
        for _row in broken_refs["meals"]:
            _g = _broken_groups.setdefault(_row["matched_name"], {"matched_name": _row["matched_name"], "meals": [], "recipes": []})
            _g["meals"].append(_row)
        for _row in broken_refs["recipes"]:
            _g = _broken_groups.setdefault(_row["matched_name"], {"matched_name": _row["matched_name"], "meals": [], "recipes": []})
            _g["recipes"].append(_row)
        broken_groups = sorted(_broken_groups.values(), key=lambda g: g["matched_name"])
        for _g in broken_groups:
            _g["candidates"] = _db.find_relink_candidates(conn, _g["matched_name"])
        all_recipes_for_relink = _db.recipe_list(conn) if broken_groups else []
        ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, recipe_id)]
        for _ing in ingredients:
            if not _ing["ref_recipe_id"]:
                _ing["amount_display"] = _ing_amount_display(_ing["unit"], _ing["amount"], _ing["food_name"])
        _attach_ref_serving_sizes(conn, ingredients)
        _attach_ingredient_portions(conn, ingredients)
        _mark_generic_density(conn, ingredients)

        # Running nutrition totals for edit-page live feedback — reuse the
        # same shared recipe-nutrient helpers the recipe detail page uses
        # (recipe_total_nutrients recurses into sub-recipe ingredients;
        # atomic_recipe_ingredients + meal_level_diaas treats each sub-recipe
        # as one already-computed food for DCP pooling), so a recipe that
        # uses another recipe as an ingredient shows the same totals here as
        # on its detail page — the previous hand-rolled loop here only
        # walked direct food ingredients and silently dropped every
        # sub-recipe ingredient's entire nutrient contribution.
        _ns_total = recipe_total_nutrients(recipe_id, conn)
        _ns_diaas_ings = atomic_recipe_ingredients(recipe_id, conn)
        _ns_dcp: float | None = None
        if _ns_diaas_ings:
            try:
                _ns_result = _diaas.meal_level_diaas(_ns_diaas_ings, conn)
                if _ns_result:
                    _ns_dcp = round(_ns_result.get("digestible_complete_protein_g") or 0, 1)
            except Exception:
                pass
        _ns_srv = float(recipe["servings"] or 1)
        nutrition_summary = {
            "calories":      round(_ns_total.get("calories", 0)),
            "protein_g":     round(_ns_total.get("protein_g", 0), 1),
            "dcp_g":         _ns_dcp,
            "cal_per_srv":   round(_ns_total.get("calories", 0) / _ns_srv),
            "prot_per_srv":  round(_ns_total.get("protein_g", 0) / _ns_srv, 1),
            "dcp_per_srv":   round(_ns_dcp / _ns_srv, 1) if _ns_dcp is not None else None,
            "servings":      _ns_srv,
            "has_data":      bool(_ns_total),
        }

    search_results = []
    if q:
        with _db.get_db() as conn:
            all_recipes = _db.recipe_list(conn)
            cached = _db.search_cached_foods(conn, q)
            pantry_ids = _pantry_fdc_ids(conn)
        ql = q.lower()
        query_words = ql.split()
        matching_recipes = [
            r for r in all_recipes
            if r["id"] != recipe_id and any(w in r["name"].lower() for w in query_words)
        ]
        recipe_aa_status = _recipe_aa_status([r["id"] for r in matching_recipes])
        for r in matching_recipes:
            search_results.append({
                "_type":     "recipe",
                "recipe_id": r["id"],
                "name":      r["name"],
                "servings":  float(r["servings"] or 1),
                "serving_size": r["serving_size"],
                "data_type": "Recipe",
                "source":    "recipe",
                "aa":        recipe_aa_status[r["id"]],
            })
        seen: set[int] = set()
        for row in cached:
            seen.add(row["fdc_id"])
            portions = json.loads(row["portions_json"] or "[]") or []
            nutrients = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
            search_results.append({
                "fdc_id":    row["fdc_id"],
                "name":      row["name"],
                "data_type": row["data_type"],
                "brand":     row["brand"] or "",
                "source":    "pantry" if row["fdc_id"] in pantry_ids else "cache",
                "portions":  portions,
                "aa":        _usda.aa_indicator(nutrients),
            })
        try:
            for food in _usda.search_foods(q, page_size=limit):
                fid = food.get("fdcId")
                if fid and fid not in seen:
                    seen.add(fid)
                    dtype = food.get("dataType", "")
                    search_results.append({
                        "fdc_id":    fid,
                        "name":      food.get("description", ""),
                        "data_type": dtype,
                        "brand":     food.get("brandOwner") or food.get("brandName") or "",
                        "source":    "usda",
                        "portions":  [],
                        "aa":        "~✓" if dtype in ("Foundation", "SR Legacy") else "✗",
                    })
        except Exception:
            pass
        search_results = _sort_search_results(search_results, q, _resolve_sort(None, "sort_food_search", "relevance", _SEARCH_SORT_MODES))
        search_results = _cap_results_preserving_local(_filter_search_results_by_source(search_results, source), limit)

    return templates.TemplateResponse(request, "recipe_edit.html", {
        **_added_food_note(added_check),
        "recipe":             dict(recipe),
        "ingredients":        ingredients,
        "q":                  q,
        "show_add_section":   show_add_section,
        "search_results":     search_results,
        "saved":              saved,
        "error":              error,
        "nutrition_summary":  nutrition_summary,
        "broken_groups":      broken_groups,
        "all_recipes_for_relink": all_recipes_for_relink,
        "relinked":           relinked,
        "relinked_to":        relinked_to,
        "source":             source,
        "limit":              limit,
        "source_filters":     _SEARCH_SOURCE_FILTERS,
        "source_labels":      _SEARCH_SOURCE_LABELS,
    })


@app.post("/recipe/{recipe_id}/relink", response_class=RedirectResponse)
async def recipe_relink_post(recipe_id: int, matched_name: str = Form(...), target_recipe_id: int = Form(...)):
    """recipe_id is only where to redirect back to (the edit page the user was
    on) — target_recipe_id (picked from the candidate/all-recipes dropdown,
    defaulting to recipe_id) is where the broken refs actually get relinked,
    since the user may be recreating a different recipe than the one they
    happen to be editing right now."""
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        target = _db.recipe_get(conn, target_recipe_id)
        if not recipe or not target:
            return RedirectResponse("/recipes", status_code=303)
        m, r = _db.relink_recipe_refs(conn, matched_name, target_recipe_id)
    params = urlencode({"relinked": f"{m},{r}", "relinked_to": target["name"]})
    return RedirectResponse(f"/recipe/{recipe_id}/edit?{params}", status_code=303)


@app.post("/recipe/{recipe_id}/edit", response_class=RedirectResponse)
async def recipe_edit_post(
    recipe_id: int,
    name: str = Form(...),
    description: str = Form(""),
    servings: float = Form(1),
    total_weight: str = Form(""),
    total_weight_unit: str = Form("g"),
    total_volume: str = Form(""),
    total_volume_unit: str = Form("ml"),
    serving_size: str = Form(""),
    introduction: str = Form(""),
    instructions: str = Form(""),
    notes: str = Form(""),
    complete: str = Form(""),
):
    tw = float(total_weight) if total_weight.strip() else None
    tv = float(total_volume) if total_volume.strip() else None
    if tv is not None:
        tv *= _PORTION_VOL_TO_ML.get(total_volume_unit.lower(), 1.0)
    with _db.get_db() as conn:
        _db.recipe_update(
            conn, recipe_id,
            name=name.strip(), description=description.strip(),
            servings=max(1.0, servings), instructions=instructions.strip(),
            total_weight=tw, total_weight_unit=total_weight_unit if tw else None,
            total_volume=tv, total_volume_unit="ml" if tv else None,
            complete=bool(complete),
            introduction=introduction.strip() or None,
            notes=notes.strip() or None,
            serving_size=serving_size.strip() or None,
        )
        _recipe_dcp.recompute_recipe_dcp(recipe_id, conn)
    return RedirectResponse(f"/recipe/{recipe_id}/edit?saved=1", status_code=303)


@app.post("/recipe/{recipe_id}/delete", response_class=RedirectResponse)
async def recipe_delete_post(request: Request, recipe_id: int):
    with _db.get_db() as conn:
        _db.recipe_delete(conn, recipe_id)
    if _is_ajax_row_action(request):
        return JSONResponse({"ok": True})
    return RedirectResponse("/recipes", status_code=303)


@app.post("/recipe/{recipe_id}/archive", response_class=RedirectResponse)
async def recipe_archive(request: Request, recipe_id: int):
    """Archive or restore a recipe — flips whichever state it's currently in."""
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            if _is_ajax_row_action(request):
                return JSONResponse({"ok": False})
            return RedirectResponse("/recipes", status_code=303)
        newly_archived = not recipe["archived"]
        still_used = 0
        if newly_archived:
            referencing = _db.recipe_referencing_subrecipe(conn, recipe_id)
            refs = _db.recipe_references(conn, recipe_id)
            still_used = int(bool(referencing or refs["meals"]))
        _db.set_recipe_archived(conn, recipe_id, newly_archived)
    if _is_ajax_row_action(request):
        return JSONResponse({"ok": True, "archived": newly_archived, "still_used": bool(still_used)})
    flag = "archived=1" if newly_archived else "restored=1"
    suffix = f"&still_used={still_used}" if newly_archived and still_used else ""
    return RedirectResponse(f"/recipes?{flag}{suffix}", status_code=303)


@app.post("/recipe/{recipe_id}/copy", response_class=RedirectResponse)
async def recipe_copy_post(recipe_id: int):
    with _db.get_db() as conn:
        src = _db.recipe_get(conn, recipe_id)
        if not src:
            return RedirectResponse("/recipes", status_code=303)
        new_id = _db.recipe_create(
            conn,
            name=f"Copy of {src['name']}",
            description=src["description"] or "",
            servings=src["servings"],
            instructions=src["instructions"] or "",
            total_weight=src["total_weight"],
            total_weight_unit=src["total_weight_unit"],
            introduction=src["introduction"],
            notes=src["notes"],
        )
        for ing in _db.recipe_get_ingredients(conn, recipe_id):
            _db.recipe_add_ingredient(
                conn, new_id, ing["fdc_id"], ing["food_name"],
                ing["amount"], ing["unit"], ing["notes"],
                ref_recipe_id=ing["ref_recipe_id"],
                ref_recipe_deleted=bool(ing["ref_recipe_deleted"]),
            )
        _recipe_dcp.recompute_recipe_dcp(new_id, conn)
    return RedirectResponse(f"/recipe/{new_id}/edit", status_code=303)


@app.post("/recipe/{recipe_id}/confirm-aa", response_class=RedirectResponse)
async def recipe_confirm_aa(
    recipe_id: int,
    fdc_ids: list[int] = Form(...),
    q: str = Form(""),
    source: list[str] = Form([]),
    limit: int | None = Form(None),
):
    """Same as /food/confirm-aa, for the ingredient-search results on a
    recipe's edit page — fetches and caches full USDA details for the
    selected foods so their '~✓' guess becomes a confirmed ✓ or ✗."""
    for fdc_id in fdc_ids:
        if fdc_id <= 0:
            continue
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached:
            continue
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception:
            continue
        with _db.get_db() as conn:
            _db.cache_food(
                conn, fdc_id=detail["fdcId"], name=detail["name"],
                data_type=detail.get("dataType", ""),
                brand=detail.get("brand"),
                serving_size=detail.get("servingSize"),
                serving_unit=detail.get("servingUnit"),
                nutrients=detail.get("nutrients", {}),
                portions=detail.get("portions", []),
            )
            _recipe_dcp.cascade_food_change(detail["fdcId"], conn)

    from urllib.parse import urlencode
    params: dict[str, str | list[str]] = {"q": q}
    if source:
        params["source"] = source
    if limit:
        params["limit"] = str(limit)
    return RedirectResponse(f"/recipe/{recipe_id}/edit?{urlencode(params, doseq=True)}", status_code=303)


@app.post("/recipe/{recipe_id}/ingredient/add", response_class=RedirectResponse)
async def recipe_ingredient_add(
    recipe_id: int,
    fdc_id: int = Form(...),
    food_name: str = Form(""),
    portion_str: str = Form("100 g"),
    notes: str = Form(""),
    q: str = Form(""),
):
    from urllib.parse import urlencode

    def _redirect(error: str | None = None) -> RedirectResponse:
        params = {}
        if q:
            params["q"] = q
        if error:
            params["error"] = error
        qs = f"?{urlencode(params)}" if params else ""
        return RedirectResponse(f"/recipe/{recipe_id}/edit{qs}", status_code=303)

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        try:
            detail = _usda.get_food_detail(fdc_id)
            with _db.get_db() as conn:
                _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                               data_type=detail.get("dataType", ""),
                               brand=detail.get("brand"),
                               serving_size=detail.get("servingSize"),
                               serving_unit=detail.get("servingUnit"),
                               nutrients=detail.get("nutrients", {}),
                               portions=detail.get("portions", []))
                _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
            food_name = food_name or detail["name"]
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, fdc_id)
        except Exception:
            return _redirect()

    name = food_name or (cached["name"] if cached else "Unknown food")
    portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
    grams, msg = _parse_portion_str(portion_str.strip() or "100 g", portions, name)
    if grams is None:
        return _redirect(error=msg)
    with _db.get_db() as conn:
        _db.recipe_add_ingredient(conn, recipe_id, fdc_id, name, grams, msg,
                                   notes.strip() or None)
        _recipe_dcp.recompute_recipe_dcp(recipe_id, conn)
        check = _added_food_check(conn, fdc_id)
    # Successful add: explicit empty q= (not simply omitted) tells the
    # persist-search JS in base.html to forget the saved query instead of
    # restoring it from sessionStorage — otherwise the search panel would
    # reappear right after the add.
    return RedirectResponse(f"/recipe/{recipe_id}/edit?q=" + (f"&added_check={check}" if check else ""),
                            status_code=303)


@app.post("/recipe/{recipe_id}/ingredient/add-recipe", response_class=RedirectResponse)
async def recipe_ingredient_add_recipe(
    recipe_id: int,
    ref_recipe_id: int = Form(...),
    recipe_name: str = Form(""),
    servings: float = Form(1.0),
    notes: str = Form(""),
    q: str = Form(""),
):
    from urllib.parse import urlencode

    def _redirect(error: str | None = None) -> RedirectResponse:
        params = {}
        if q:
            params["q"] = q
        if error:
            params["error"] = error
        qs = f"?{urlencode(params)}" if params else ""
        return RedirectResponse(f"/recipe/{recipe_id}/edit{qs}", status_code=303)

    if ref_recipe_id == recipe_id or servings <= 0:
        return _redirect(error="Invalid recipe ingredient.")
    with _db.get_db() as conn:
        sub = _db.recipe_get(conn, ref_recipe_id)
        if not sub:
            return _redirect(error="Recipe not found.")
        name = recipe_name or sub["name"]
        unit = f"{servings:g} serving" + ("s" if servings != 1 else "")
        _db.recipe_add_ingredient(conn, recipe_id, 0, name, servings, unit,
                                   notes.strip() or None, ref_recipe_id=ref_recipe_id)
        _db.recipe_auto_weight(conn, recipe_id)
        _recipe_dcp.recompute_recipe_dcp(recipe_id, conn)
    return RedirectResponse(f"/recipe/{recipe_id}/edit?q=", status_code=303)


@app.post("/recipe/{recipe_id}/ingredient/{ing_id}/remove", response_class=RedirectResponse)
async def recipe_ingredient_remove(recipe_id: int, ing_id: int):
    with _db.get_db() as conn:
        _db.recipe_remove_ingredient(conn, ing_id)
        _recipe_dcp.recompute_recipe_dcp(recipe_id, conn)
    return RedirectResponse(f"/recipe/{recipe_id}/edit", status_code=303)


@app.post("/recipe/{recipe_id}/ingredient/{ing_id}/edit", response_class=RedirectResponse)
async def recipe_ingredient_edit(
    recipe_id: int,
    ing_id: int,
    portion_str: str = Form(...),
    food_name: str = Form(...),
    notes: str = Form(""),
    q: str = Form(""),
):
    from urllib.parse import urlencode

    def _redirect(error: str | None = None) -> RedirectResponse:
        if error:
            params = {"error": error}
            if q:
                params["q"] = q
        else:
            # Explicit empty q= tells the persist-search JS in base.html to
            # forget the saved query instead of restoring it.
            params = {"q": ""}
        qs = f"?{urlencode(params)}"
        return RedirectResponse(f"/recipe/{recipe_id}/edit{qs}", status_code=303)

    with _db.get_db() as conn:
        ings = _db.recipe_get_ingredients(conn, recipe_id)
        ing = next((i for i in ings if i["id"] == ing_id), None)
        cached = (_db.get_cached_food(conn, ing["fdc_id"])
                  if ing and ing["fdc_id"] and not ing["ref_recipe_id"] else None)

    if ing and ing["ref_recipe_id"]:
        # Sub-recipe ingredients are measured in servings, not grams/portions.
        try:
            grams, label = float(portion_str.strip()), portion_str.strip()
        except ValueError:
            return _redirect(error="Enter a number of servings.")
    else:
        portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
        grams, label = _parse_portion_str(portion_str.strip(), portions, food_name.strip())
        if grams is None:
            return _redirect(error=label)
    with _db.get_db() as conn:
        _db.recipe_update_ingredient(conn, ing_id, grams, label,
                                      food_name.strip(), notes.strip() or None)
        _recipe_dcp.recompute_recipe_dcp(recipe_id, conn)
    return _redirect()


@app.post("/recipe/{recipe_id}/ingredient/{ing_id}/move", response_class=RedirectResponse)
async def recipe_ingredient_move(recipe_id: int, ing_id: int, direction: str = Form(...), next: str = Form("edit")):
    with _db.get_db() as conn:
        ings = _db.recipe_get_ingredients(conn, recipe_id)
        ids = [i["id"] for i in ings]
        dest = f"/recipe/{recipe_id}" if next == "detail" else f"/recipe/{recipe_id}/edit"
        if ing_id not in ids:
            return RedirectResponse(dest, status_code=303)
        idx = ids.index(ing_id)
        if direction == "up" and idx > 0:
            ids[idx], ids[idx - 1] = ids[idx - 1], ids[idx]
        elif direction == "down" and idx < len(ids) - 1:
            ids[idx], ids[idx + 1] = ids[idx + 1], ids[idx]
        _db.recipe_reorder_ingredients(conn, ids)
    return RedirectResponse(dest + "#sec-ingredients", status_code=303)


@app.post("/recipe/{recipe_id}/instructions", response_class=RedirectResponse)
async def recipe_instructions_post(recipe_id: int, instructions: str = Form("")):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        _db.recipe_update(
            conn, recipe_id,
            name=recipe["name"], description=recipe["description"] or "",
            servings=recipe["servings"], instructions=instructions.strip(),
            total_weight=recipe["total_weight"],
            total_weight_unit=recipe["total_weight_unit"],
            total_volume=recipe["total_volume"],
            total_volume_unit=recipe["total_volume_unit"],
            complete=bool(recipe["complete"]),
            introduction=recipe["introduction"],
            notes=recipe["notes"],
            serving_size=recipe["serving_size"],
        )
    return RedirectResponse(f"/recipe/{recipe_id}#sec-procedure", status_code=303)


@app.get("/summary/trend", response_class=HTMLResponse)
async def summary_trend(request: Request, days: int = Query(7)):
    """Nutrient averages across the last N days vs. RDA — surfaces chronic
    shortfalls (B12, iron, iodine, vitamin D, ...) a single day's snapshot
    can't."""
    if days not in (7, 14, 30):
        days = 7

    end = datetime.date.today()
    start = end - datetime.timedelta(days=days - 1)

    with _db.get_db() as conn:
        meals = _db.meal_list_by_date_range(conn, start.isoformat(), end.isoformat())
        daily_totals: dict[str, dict[str, float]] = {}
        day_dcp: dict[str, float] = {}
        for meal in meals:
            _, nutrients, _ingredients = _meal_expand_for_diaas(meal["id"], conn)
            if nutrients:
                day = daily_totals.setdefault(meal["meal_date"], {})
                for key, val in nutrients.items():
                    day[key] = day.get(key, 0.0) + val
            if meal["bcp_g"] is not None:
                day_dcp[meal["meal_date"]] = day_dcp.get(meal["meal_date"], 0.0) + meal["bcp_g"]

    avg_nutrients, num_days = average_from_daily_totals(daily_totals)

    # Average daily GL across the window. Weekly averages are the figure worth
    # acting on -- any single day's GL swings with what happened to be eaten --
    # but a day with incomplete GI coverage has no GL at all, so the count of
    # days that actually contributed is disclosed rather than hidden inside
    # the average.
    with _db.get_db() as conn:
        gl_by_date = day_gl_totals(conn, sorted(daily_totals))
    avg_gl, avg_gl_days = average_day_gl(gl_by_date)
    gl_unknown_dates = sorted(d for d, v in gl_by_date.items() if v is None)

    # RDA targets reflect the profile pinned to the *end* of the window
    # (today, for the common "last N days" case). If any logged day used a
    # different profile at the time, disclose it rather than silently
    # blending profiles into one average.
    with _db.get_db() as conn:
        end_profile_obj = _day_profile.get_profile_for_date(conn, end.isoformat())
        end_profile_row = _db.day_profile_get(conn, end.isoformat())
        differing_dates = sorted(
            d for d in daily_totals
            if (_db.day_profile_get(conn, d) or {"profile_name": None})["profile_name"]
            != (end_profile_row["profile_name"] if end_profile_row else None)
        )
    rda = _load_rda(end_profile_obj)
    optimal = _load_optimal(end_profile_obj)
    max_limits = _load_max_limits(end_profile_obj)

    # Lead with DCP, not raw protein — raw protein overstates what the body
    # can actually use, and that gap is exactly what this view exists to
    # catch over a chronic window, not just a single day.
    protein_target = rda["protein_g"][0] if rda and rda.get("protein_g") and rda["protein_g"][0] > 0 else None
    avg_dcp = round(sum(day_dcp.values()) / len(day_dcp), 1) if day_dcp else None
    avg_dcp_pct = round(avg_dcp / protein_target * 100, 0) if avg_dcp is not None and protein_target else None

    return templates.TemplateResponse(request, "trend.html", {
        "days":              days,
        "start":             start.isoformat(),
        "end":               end.isoformat(),
        "num_days":          num_days,
        "nutrient_sections": _nutrient_sections(avg_nutrients, rda, avg_nutrients,
                                                optimal=optimal, max_limits=max_limits,
                                                dcp_g=avg_dcp) if num_days else [],
        "dcp_missing_names": [],
        "has_profile":       rda is not None,
        "has_optimal":       bool(optimal),
        "has_ul":             bool(max_limits),
        "diet_notes":        _diet_aware_daily_notes(avg_nutrients, rda) if num_days else {},
        "end_profile_name":  end_profile_row["profile_name"] if end_profile_row else None,
        "differing_profile_dates": differing_dates,
        "avg_dcp":           avg_dcp,
        "avg_dcp_pct":       avg_dcp_pct,
        "avg_dcp_days":      len(day_dcp),
        "protein_target":    protein_target,
        "avg_gl":            avg_gl,
        "avg_gl_days":       avg_gl_days,
        "gl_by_date":        gl_by_date,
        "gl_unknown_dates":  gl_unknown_dates,
    })


def _nutrient_plot_params(conn, nutrients: list[str], days_back: str | None, anchor_date: str | None,
                           rolling: bool = False):
    """Shared by the plot page and its image endpoint: validate the chosen
    nutrient keys (capped to the plotting palette's 8 colors) and resolve
    which logged dates fall in range. days_back blank/absent/<=0 means "all
    logged days"; otherwise it's the N days ending at anchor_date (default:
    the most recent logged day). days_back arrives as a string (not int)
    because the "blank = all days" form field submits "" when empty, which
    FastAPI's query validation rejects outright for an int-typed param.
    rolling=True ("always end on the last complete day") overrides
    anchor_date with the most recent date where every meal is marked
    complete (falling back to yesterday if there's no such date yet, e.g. a
    brand-new install) and, in "all logged days" mode, drops any dates after
    it — so a saved Home page plot keeps sliding forward as days are
    completed instead of freezing at whatever date it was turned on. This can
    land on today, once today's meals are all marked complete — "complete"
    was never about the calendar date, just the meals' own complete flag."""
    valid_keys = {key for key, _label, _unit in _usda.NUTRIENT_MAP.values()} | {_DCP_PLOT_KEY, _GL_PLOT_KEY}
    chosen = [k for k in nutrients if k in valid_keys][:MAX_PLOT_NUTRIENTS]

    all_dates = sorted(r["meal_date"] for r in _db.meal_dates_with_bcp(conn, limit=1_000_000))

    if rolling:
        anchor_date = (_db.last_complete_meal_date(conn)
                       or (datetime.date.today() - datetime.timedelta(days=1)).isoformat())

    try:
        days_back_n = int(days_back) if days_back else None
    except ValueError:
        days_back_n = None

    if days_back_n and days_back_n > 0:
        anchor = anchor_date or (all_dates[-1] if all_dates else datetime.date.today().isoformat())
        anchor_d = datetime.date.fromisoformat(anchor)
        start_d = anchor_d - datetime.timedelta(days=days_back_n - 1)
        dates = [d for d in all_dates if start_d.isoformat() <= d <= anchor_d.isoformat()]
    else:
        anchor = anchor_date or (all_dates[-1] if all_dates else "")
        dates = all_dates
        if rolling:
            dates = [d for d in dates if d <= anchor]

    return chosen, dates, anchor


def _plot_variance(values: list[float]) -> float:
    vals = [v for v in values if not math.isnan(v)]
    if len(vals) < 2:
        return 0.0
    m = sum(vals) / len(vals)
    return sum((v - m) ** 2 for v in vals) / len(vals)


def _plot_stdev(values: list[float]) -> float:
    return math.sqrt(_plot_variance(values))


def _default_plot_scale_factor(series: list[dict]) -> float:
    """Auto scale factor: the most-variable series' standard deviation
    divided by the least-variable series'. Dividing the more-variable
    series' values by this factor brings its spread down to roughly match
    the smallest, so neither a small-scale nutrient (e.g. Protein) nor a
    large-scale one (e.g. Carbohydrate) flattens into a barely-visible line
    next to the other. This is the Nutrient Plot page's "Scale factor"
    field default — the user can type their own instead."""
    if len(series) < 2:
        return 1.0
    stds = [_plot_stdev(s["y"]) for s in series]
    positive = [v for v in stds if v > 0]
    if len(positive) < 2:
        return 1.0
    return round(max(positive) / min(positive), 1)


def _fmt_plot_factor(factor: float) -> str:
    return str(int(factor)) if factor == int(factor) else f"{factor:g}"


def _parse_plot_factor(raw: str | None) -> float | None:
    if not raw:
        return None
    try:
        v = float(raw)
    except ValueError:
        return None
    return v if v > 0 else None


def _apply_plot_scale_factor(series: list[dict], factor: float) -> list[dict]:
    """Step 1. Divide every series except the least-variable one (the
    reference — left at its natural scale) by `factor`, noting it in that
    series' own legend label. See _default_plot_scale_factor for the auto
    default. A single shared factor can't perfectly equalize more than two
    series at once — see _default_individual_factors (step 2) for the
    per-nutrient top-up this sets up for."""
    if len(series) < 2 or not factor or factor == 1:
        return series
    stds = [_plot_stdev(s["y"]) for s in series]
    reference_i = stds.index(min(stds))
    scaled = []
    for i, s in enumerate(series):
        if i == reference_i:
            scaled.append(s)
        else:
            new_s = {**s, "y": [v / factor for v in s["y"]],
                      "label": f"{s['label']} ÷{_fmt_plot_factor(factor)}", "scaled": True}
            if s.get("goal") is not None:
                new_s["goal"] = s["goal"] / factor
            if s.get("limit") is not None:
                new_s["limit"] = s["limit"] / factor
            scaled.append(new_s)
    return scaled


def _default_individual_factors(series: list[dict]) -> dict[str, float]:
    """Step 2, run after step 1's global factor is already applied. A
    single shared factor can still leave one nutrient nearly flat if its
    own variance is far below the plot's most-variable nutrient — dividing
    two things down to roughly the same level doesn't help a third that's
    smaller than both. Set a variance floor at 25% of the largest variance
    among the (already step-1-scaled) series; any series still under it
    gets its own individual multiplier on top, to bring its variance up to
    that floor. Returns {nutrient_key: multiplier} — 1.0 where no boost is
    needed. This is each nutrient's own "factor_<key>" field default on the
    Nutrient Plot page; the user can type their own instead."""
    variances = {s["key"]: _plot_variance(s["y"]) for s in series}
    max_var = max(variances.values()) if variances else 0.0
    floor = 0.25 * max_var
    factors = {}
    for key, v in variances.items():
        factors[key] = round(math.sqrt(floor / v), 1) if 0 < v < floor else 1.0
    return factors


def _apply_individual_factors(series: list[dict], factors: dict[str, float]) -> list[dict]:
    """Step 2's application: multiply each series by its own factor (see
    _default_individual_factors) on top of whatever step 1 already did to
    it. A multiplier > 1 boosts an otherwise-flat nutrient's visible
    variability; noted in its legend label alongside any step-1 note."""
    out = []
    for s in series:
        k = factors.get(s["key"], 1.0)
        if not k or k == 1.0:
            out.append(s)
        else:
            new_s = {**s, "y": [v * k for v in s["y"]],
                      "label": f"{s['label']} ×{_fmt_plot_factor(k)}", "scaled": True}
            if s.get("goal") is not None:
                new_s["goal"] = s["goal"] * k
            if s.get("limit") is not None:
                new_s["limit"] = s["limit"] * k
            out.append(new_s)
    return out


def _nutrient_plot_factor_params(query_params, chosen: list[str]) -> dict[str, str]:
    """Raw (unparsed) factor_<key> query values actually present, keyed by
    nutrient key — used both to resolve step 2's effective per-nutrient
    factors and to prefill the plot page's per-nutrient input fields."""
    return {k: query_params.get(f"factor_{k}", "") for k in chosen}


def _resolve_highlight(chosen: list[str], highlight: str | None) -> str | None:
    """Which chosen nutrient draws highlighted (fixed red and solid in
    color mode; the one solid line, everything else dashed, in grayscale
    mode). Defaults to Day DCP when it's among the chosen nutrients;
    otherwise no forced highlight — every series just auto-cycles."""
    if highlight and highlight in chosen:
        return highlight
    return _DCP_PLOT_KEY if _DCP_PLOT_KEY in chosen else None


def _nutrient_plot_raw_series(conn, chosen: list[str], dates: list[str],
                               highlight_key: str | None) -> list[dict]:
    from numa_app.services.meal_list_columns import day_nutrient_values

    plain_keys = [k for k in chosen if k not in (_DCP_PLOT_KEY, _GL_PLOT_KEY)]
    day_values = {d: day_nutrient_values(conn, d, plain_keys) for d in dates} if plain_keys else {}
    dcp_by_date: dict[str, float | None] = {}
    if _DCP_PLOT_KEY in chosen:
        dcp_by_date = {r["meal_date"]: r["day_bcp"] for r in _db.meal_dates_with_bcp(conn, limit=1_000_000)}
    gl_by_date: dict[str, float | None] = day_gl_totals(conn, dates) if _GL_PLOT_KEY in chosen else {}

    series = []
    for key in chosen:
        y = []
        for d in dates:
            if key == _DCP_PLOT_KEY:
                v = dcp_by_date.get(d)
            elif key == _GL_PLOT_KEY:
                v = gl_by_date.get(d)
            else:
                v = day_values[d][key]
            y.append(float(v) if v is not None else float("nan"))
        s = {"key": key, "x": dates, "y": y, "label": _plot_label_for(key)}
        if key == highlight_key:
            s["color"] = _HIGHLIGHT_COLOR
            s["highlight"] = True
        series.append(s)
    return series


_NUTRIENT_PLOT_GOAL_SUBTITLE = "(Dashed lines indicate profile goal levels)"
_NUTRIENT_PLOT_LIMIT_SUBTITLE = "(Dotted lines indicate maximum limit levels)"
_NUTRIENT_PLOT_GOAL_AND_LIMIT_SUBTITLE = (
    "(Dashed lines indicate profile goal levels; dotted lines indicate maximum limit levels)"
)


def _plot_legend_pos(value: str | None) -> str:
    """Sanitize the Nutrient Plot legend-placement param to one of
    plotting.LEGEND_POSITIONS. Anything unrecognized (including a hand-edited
    or stale querystring) falls back to "auto", which lets plotting.py pick
    top while the legend fits one row and bottom once it would wrap."""
    from numa_app.services.plotting import LEGEND_POSITIONS
    cleaned = (value or "auto").strip().lower()
    return cleaned if cleaned in LEGEND_POSITIONS else "auto"


def _nutrient_plot_goal(profile, diet_pref: str, key: str) -> float | None:
    """The single reference value a Nutrient Plot dashed goal line marks for
    one chosen nutrient key, from the currently-active profile (a flat
    reference line isn't meaningfully "per logged day", so this doesn't use
    day_profile's per-date pinned profile the way DCP scoring does). Prefers
    a user-configured Optimal target (profile.compute_optimal) over the
    built-in RDA/AI/limit (profile.compute_rda) when both exist — Optimal is
    the value the user deliberately chose to aim for instead. Returns None
    when no profile is set or the nutrient has neither."""
    if profile is None or key == _GL_PLOT_KEY:
        return None
    if key == _DCP_PLOT_KEY:
        rda = _profile.compute_rda(profile, diet_pref=diet_pref)
        entry = rda.get("protein_g")
        return entry[0] if entry else None
    optimal = _profile.compute_optimal(profile).get(key)
    if optimal:
        return optimal[0]
    rda_entry = _profile.compute_rda(profile, diet_pref=diet_pref).get(key)
    return rda_entry[0] if rda_entry else None


def _nutrient_plot_add_goals(series: list[dict], profile, diet_pref: str) -> list[dict]:
    """Attach each series' flat goal value (see _nutrient_plot_goal) under
    its "goal" key. plotting.line_plot_image draws the dashed reference
    line in whatever color that series' data line ends up in (explicit or
    auto-assigned), so the two always match without this needing to know
    the plot's color-assignment order itself."""
    return [({**s, "goal": goal} if (goal := _nutrient_plot_goal(profile, diet_pref, s["key"])) is not None else s)
            for s in series]


def _nutrient_plot_limit(profile, key: str) -> float | None:
    """The max-limit reference value a Nutrient Plot dotted line marks for
    one chosen nutrient key — profile.get_max_limits() (built-in Tolerable
    Upper Intake Levels merged with the user's own configured caps). None
    for the DCP pseudo-key and for any nutrient with no established/
    user-set limit."""
    if profile is None or key in (_DCP_PLOT_KEY, _GL_PLOT_KEY):
        return None
    return _profile.get_max_limits(profile).get(key)


def _nutrient_plot_add_limits(series: list[dict], profile) -> list[dict]:
    """Attach each series' flat max-limit value (see _nutrient_plot_limit)
    under its "limit" key, drawn as a dotted reference line — distinct from
    the dashed "goal" line so a nutrient with both stays readable as two
    different kinds of reference."""
    return [({**s, "limit": limit} if (limit := _nutrient_plot_limit(profile, s["key"])) is not None else s)
            for s in series]


DEFAULT_SMOOTHING_DAYS = 3


def _parse_smoothing_window(raw: str | None) -> int:
    """Smoothing window in days. Missing/blank/invalid falls back to the
    3-day default (the plot page always pre-fills the field with a concrete
    number, so blank only really happens on a bare first visit); 0 or 1
    means no smoothing — the original, unsmoothed data."""
    if raw is None:
        return DEFAULT_SMOOTHING_DAYS
    try:
        n = int(raw)
    except ValueError:
        return DEFAULT_SMOOTHING_DAYS
    return max(n, 0)


def _apply_smoothing(series: list[dict], window: int) -> list[dict]:
    """Trailing moving average over the points that HAVE data: each point
    becomes the average of itself and the (window - 1) data points before
    it, however far back they are, as if the missing days (nan) weren't
    there (owner's choice, 2026-10-04: a gap shouldn't shrink the average).
    Fewer at the very start of the series. A missing point stays missing.
    window <= 1 returns the series unchanged. Runs before the scale factor
    steps, so scaling is calibrated to what's actually displayed."""
    if window <= 1:
        return series
    smoothed = []
    for s in series:
        y = s["y"]
        new_y, seen = [], []
        for v in y:
            if math.isnan(v):
                new_y.append(float("nan"))
                continue
            seen.append(v)
            chunk = seen[-window:]
            new_y.append(sum(chunk) / len(chunk))
        smoothed.append({**s, "y": new_y})
    return smoothed


_GENERIC_PLOT_YLABEL = "Value (see legend for units)"


def _nutrient_plot_ylabel(chosen: list[str], series: list[dict]) -> str:
    # A single shared unit is only a meaningful axis label if nothing was
    # rescaled — a rescaled series is no longer in that unit, even though
    # every chosen nutrient nominally shares it (e.g. Fiber (g) plotted
    # alongside a much larger Total Fat (g) that got divided down).
    if any(s.get("scaled") for s in series):
        return _GENERIC_PLOT_YLABEL
    units = {unit for key, _label, unit in _usda.NUTRIENT_MAP.values() if key in chosen}
    if _DCP_PLOT_KEY in chosen:
        units.add("g")
    if _GL_PLOT_KEY in chosen:
        units.add("")   # unitless — forces the generic label unless GL is alone
    return units.pop() if len(units) == 1 and units != {""} else _GENERIC_PLOT_YLABEL


def _nutrient_plot_default_title(dates: list[str]) -> str:
    return f"Key nutrients consumed, {dates[0]} to {dates[-1]}" if dates else "Key nutrients consumed"


_AUTO_PLOT_TITLE_RE = re.compile(r"^Key nutrients consumed(, \d{4}-\d{2}-\d{2} to \d{4}-\d{2}-\d{2})?$")


def _user_plot_title(title: str | None) -> str | None:
    """A title the user actually typed, as distinct from a `title=` param
    that merely looks like NuMa's own auto-generated one (with some date
    range baked in) — e.g. one echoed back by a stale bookmark, an old saved
    Home-page link, or a resubmitted form. Treating any auto-shaped title as
    "none" here means the date range in it always tracks the plot's current
    range instead of freezing at whatever range was in effect when that
    exact title text first got captured somewhere (a bookmark, a saved
    querystring, ...)."""
    stripped = title.strip() if title else ""
    if not stripped or _AUTO_PLOT_TITLE_RE.match(stripped):
        return None
    return stripped


def _smoothing_lead_dates(conn, first_date: str, window: int, skip: set[str]) -> list[str]:
    """Up to (window - 1) logged dates before the plot's first date (minus
    `skip`): read for the trailing average of the first points plotted,
    never drawn."""
    if window <= 1 or not first_date:
        return []
    earlier = sorted(r["meal_date"] for r in _db.meal_dates_with_bcp(conn, limit=1_000_000)
                     if r["meal_date"] < first_date and r["meal_date"] not in skip)
    return earlier[-(window - 1):]


def _plot_days(conn, dates: list[str], rolling: bool) -> tuple[list[str], list[str], int]:
    """(data_dates, axis_dates, skipped_incomplete) for a plot of the logged
    `dates`. In "always end on the last complete day" mode, a day with a meal
    not marked complete is left out like a day with nothing logged, so a
    partly logged day can't drag the line down; otherwise incomplete days
    are plotted at what's logged (owner's choice, 2026-10-04, "for now").
    The axis runs over every calendar day from the first data day to the
    last, so each missing day shows as a break in the line."""
    skip = _db.meal_dates_with_incomplete(conn) if rolling else set()
    data_dates = [d for d in dates if d not in skip]
    if not data_dates:
        return [], [], len(dates)
    first = datetime.date.fromisoformat(data_dates[0])
    last = datetime.date.fromisoformat(data_dates[-1])
    axis = [(first + datetime.timedelta(days=i)).isoformat() for i in range((last - first).days + 1)]
    return data_dates, axis, len(dates) - len(data_dates)


def _smoothing_info(window: int, lead: list[str], data_dates: list[str], axis: list[str],
                    skipped_incomplete: int = 0) -> dict:
    """What the notes under a plot say (_smoothing_note.html): the window,
    how many earlier logged days were borrowed (lead_days, from lead_from),
    how many of the first plotted points still average over fewer days
    because that many earlier days don't exist (short), how many calendar
    days in the plotted span have no data (gap_days, breaks in the line)
    and how many logged days were left out for a meal not marked complete
    (skipped_incomplete)."""
    short = max(0, window - 1 - len(lead)) if window > 1 else 0
    return {"window": window, "lead_days": len(lead), "lead_from": lead[0] if lead else None,
            "short": min(short, len(data_dates)), "plotted_days": len(data_dates),
            "gap_days": len(axis) - len(data_dates), "skipped_incomplete": skipped_incomplete}


def _smoothed_plot_series(conn, chosen: list[str], dates: list[str], highlight_key: str | None,
                          window: int, rolling: bool = False) -> tuple[list[dict], dict]:
    """The plot's series over a calendar-day axis, missing days as nan (a
    break in the line), smoothed with a trailing average over the days that
    have data (_apply_smoothing), reaching back into the logged days BEFORE
    the plot's first date so the first points are averaged over as many
    days as the rest (when that many exist). Returns (series, _smoothing_info)."""
    data_dates, axis, skipped = _plot_days(conn, dates, rolling)
    if not data_dates:
        return [], _smoothing_info(window, [], [], [], skipped)
    skip = _db.meal_dates_with_incomplete(conn) if rolling else set()
    lead = _smoothing_lead_dates(conn, data_dates[0], window, skip)
    series = _apply_smoothing(_nutrient_plot_raw_series(conn, chosen, lead + data_dates, highlight_key), window)
    out = []
    for s in series:
        by_date = dict(zip(lead + data_dates, s["y"]))
        out.append({**s, "x": axis, "y": [by_date.get(d, float("nan")) for d in axis]})
    return out, _smoothing_info(window, lead, data_dates, axis, skipped)


def _nutrient_plot_qs(chosen: list[str], days_back: str | None, anchor: str | None,
                       scale_factor: str | None, title: str | None,
                       highlight: str | None, grayscale: bool, smoothing: int,
                       nutrient_factors: dict[str, str] | None = None,
                       rolling: bool = False, legend: str = "auto") -> str:
    from urllib.parse import urlencode
    params = [("nutrients", k) for k in chosen]
    if days_back:
        params.append(("days_back", days_back))
        if anchor and not rolling:
            params.append(("anchor_date", anchor))
    if rolling:
        params.append(("rolling", "1"))
    if scale_factor:
        params.append(("scale_factor", scale_factor))
    if title:
        params.append(("title", title))
    if highlight:
        params.append(("highlight", highlight))
    if grayscale:
        params.append(("grayscale", "1"))
    # Omitted entirely while the legend placement is left on "auto", so a
    # home_nutrient_plot_qs saved before this option existed still matches
    # the qs recomputed for the same view (is_home_plot compares the two
    # with ==, and an unconditional param would make every saved plot read
    # as "not the Home page one" the first time it was reloaded).
    if legend in ("top", "bottom"):
        params.append(("legend", legend))
    params.append(("smoothing", str(smoothing)))
    for key, val in (nutrient_factors or {}).items():
        if val:
            params.append((f"factor_{key}", val))
    return urlencode(params)


@app.get("/summary/nutrient-plot", response_class=HTMLResponse)
async def nutrient_plot_page(
    request: Request,
    nutrients: list[str] = Query([]),
    days_back: str | None = Query(None),
    anchor_date: str | None = Query(None),
    scale_factor: str | None = Query(None),
    title: str | None = Query(None),
    highlight: str | None = Query(None),
    grayscale: bool = Query(False),
    legend: str = Query("auto"),
    smoothing: str | None = Query(None),
    rolling: bool = Query(False),
    submitted: bool = Query(False),
):
    """Line plot of one or more Daily Summary nutrients over a chosen set of
    days — reuses the same per-day nutrient totals as the Recent Days table
    and the extra-column picker (numa_app.services.meal_list_columns).

    A genuinely fresh landing here (no `submitted` marker — see the form's
    hidden field) with nothing picked yet redirects to whatever's currently
    saved as the Home page plot, if any, instead of always rendering blank.
    Otherwise the page looked "unset" on every visit even with a Home page
    plot active, which also hid the "Show on Home page" toggle entirely
    (it only renders once something's actually plotted) while still
    showing the "a different plot is on the Home page" warning -- true of
    literally every fresh visit, not just an actual mismatch. A real
    "submitted this form with everything unchecked" request is left alone,
    since that's a deliberate empty view, not a fresh landing."""
    if not submitted and not nutrients:
        prefs = _load_prefs_file()
        if prefs.get("home_nutrient_plot_enabled") and prefs.get("home_nutrient_plot_qs"):
            return RedirectResponse(f"/summary/nutrient-plot?{prefs['home_nutrient_plot_qs']}", status_code=303)

    from numa_app.services.meal_list_columns import plot_nutrient_choices

    smoothing_n = _parse_smoothing_window(smoothing)

    with _db.get_db() as conn:
        chosen, dates, anchor = _nutrient_plot_params(conn, nutrients, days_back, anchor_date, rolling=rolling)
        has_plot = bool(chosen) and bool(dates)
        highlight_key = _resolve_highlight(chosen, highlight) if has_plot else None
        raw_series, smoothing_info = (_smoothed_plot_series(conn, chosen, dates, highlight_key, smoothing_n,
                                                            rolling=rolling)
                                      if has_plot else ([], _smoothing_info(smoothing_n, [], [], [])))
        # Every day in range left out (all have an incomplete meal, in
        # "always end on the last complete day" mode): keep the page's plot
        # controls, so that mode can be switched off, and say why instead of
        # drawing an empty plot.
        plot_empty = has_plot and not raw_series

    # scale_factor (step 1) is a "blank means auto" field, same convention
    # as Days back above it: the input's own value stays empty unless the
    # user actually typed an override, so the field re-syncs to a freshly
    # computed default (e.g. after changing which nutrients/days are
    # plotted) instead of echoing back a stale number forever. The
    # placeholder shows what "blank" currently resolves to. Step 2's
    # per-nutrient factor_<key> fields follow the identical convention.
    user_factor = _parse_plot_factor(scale_factor)
    default_factor = _default_plot_scale_factor(raw_series) if raw_series else None
    effective_factor = user_factor or default_factor or 1.0
    factor_str = _fmt_plot_factor(effective_factor)
    step1_series = _apply_plot_scale_factor(raw_series, effective_factor) if raw_series else []

    raw_factor_params = _nutrient_plot_factor_params(request.query_params, chosen)
    auto_individual = _default_individual_factors(step1_series) if step1_series else {}
    effective_individual = {
        k: (_parse_plot_factor(raw_factor_params.get(k)) or auto_individual.get(k, 1.0))
        for k in chosen
    }
    individual_factor_strs = {k: _fmt_plot_factor(v) for k, v in effective_individual.items()}

    # "blank means auto" convention, same as scale_factor above: only persist
    # a title in the qs when the user actually typed one, so an auto-generated
    # title (which embeds the date range) keeps recomputing itself — with the
    # current dates — on every reload instead of freezing at whatever range
    # was in effect the first time the qs was saved (e.g. when "Roll to last
    # complete day" was turned on).
    user_title = _user_plot_title(title)
    effective_title = user_title or _nutrient_plot_default_title(dates)

    # Same "blank means auto" convention applied to what gets persisted: only
    # bake a scale factor into qs when the user actually set one, so an
    # auto-computed default (which drifts as new meals get logged) can't
    # desync qs from a previously-saved home_nutrient_plot_qs and make the
    # "Show on Home page" checkbox read as unchecked even though the plot is
    # still showing there.
    legend_pos = _plot_legend_pos(legend)
    qs_scale_factor = scale_factor if user_factor else None
    qs_individual_factors = {k: v for k, v in raw_factor_params.items() if _parse_plot_factor(v)}

    qs = (_nutrient_plot_qs(chosen, days_back, anchor, qs_scale_factor, user_title,
                             highlight_key, grayscale, smoothing_n, qs_individual_factors,
                             rolling=rolling, legend=legend_pos)
          if has_plot else "")

    available = [(_DCP_PLOT_KEY, _DCP_PLOT_LABEL), (_GL_PLOT_KEY, _GL_PLOT_LABEL)] + plot_nutrient_choices()
    available_dicts = [{"key": k, "label": lbl} for k, lbl in available]
    # Split into 2 columns for the checklist (was 3 — narrowed so the
    # checklist box leaves enough width for the Days back/Highlight/Plot
    # options to sit beside it instead of wrapping below it), filled
    # top-to-bottom left-to-right (item 1..k in column 1, k+1..2k in column
    # 2, ...) rather than round-robin, so each column reads as a contiguous
    # chunk of the list.
    _col_size = -(-len(available_dicts) // 2)  # ceil
    available_nutrient_columns = [available_dicts[i:i + _col_size] for i in range(0, len(available_dicts), _col_size)]
    nutrient_factor_rows = [{
        "key":         k,
        "label":       _plot_label_for(k),
        "value":       raw_factor_params.get(k, ""),
        "placeholder": _fmt_plot_factor(auto_individual.get(k, 1.0)),
    } for k in chosen]

    prefs = _load_prefs_file()
    home_plot_enabled = bool(prefs.get("home_nutrient_plot_enabled"))
    is_home_plot = bool(has_plot and home_plot_enabled and prefs.get("home_nutrient_plot_qs") == qs)
    # True when some (possibly different, e.g. stale from before a qs-format
    # change, or just a different nutrient/range selection) plot is enabled
    # on the Home page but doesn't match what's on screen right now — the
    # "Show on Home page" checkbox can only reflect an exact match (checking
    # it always saves *this* view, so it must stay unchecked rather than lie
    # about a different one being shown), which would otherwise leave no way
    # to turn the Home page plot off from here at all.
    home_plot_enabled_elsewhere = home_plot_enabled and not is_home_plot

    return templates.TemplateResponse(request, "nutrient_plot.html", {
        "available_nutrients": available_dicts,
        "available_nutrient_columns": available_nutrient_columns,
        "chosen":     chosen,
        "days_back":  days_back or "",
        "anchor_date": anchor,
        "dates":      dates,
        "plot_first": raw_series[0]["x"][0] if raw_series else "",
        "plot_last":  raw_series[0]["x"][-1] if raw_series else "",
        "has_plot":   has_plot,
        "plot_empty": plot_empty,
        "qs":         qs,
        "is_home_plot": is_home_plot,
        "max_nutrients": MAX_PLOT_NUTRIENTS,
        "scale_factor": scale_factor if user_factor else "",
        "scale_factor_placeholder": _fmt_plot_factor(default_factor) if default_factor else "auto",
        "nutrient_factor_rows": nutrient_factor_rows,
        "title":      user_title or "",
        "title_placeholder": effective_title,
        "highlight":  highlight_key,
        "grayscale":  grayscale,
        "legend_pos": legend_pos,
        "smoothing":  smoothing_n,
        "smoothing_info": smoothing_info,
        "rolling":    rolling,
        "home_plot_enabled_elsewhere": home_plot_enabled_elsewhere,
    })


@app.post("/summary/nutrient-plot/home-pref")
async def nutrient_plot_home_pref(qs: str = Form(default=""), enabled: str | None = Form(None),
                                   rolling: str | None = Form(None)):
    """"Show this plot on the Home page" toggle on the Nutrient Plot page —
    stores the full plot querystring in prefs.json so index() can reuse it
    (server-rendered; the home page has no client JS state of its own to
    read a browser-stored preference from). The "always end on the last
    complete day" checkbox sits alongside it: checking it strips any frozen
    anchor_date from the stored querystring and adds rolling=1, so every
    future render (including the Home page's) recomputes the end date as
    the most recent day whose meals are all marked complete (see
    _nutrient_plot_params/_db.last_complete_meal_date) instead of replaying
    whatever date was current when this was saved. When that checkbox is NOT
    checked, anchor_date must be left alone
    — stripping it unconditionally used to silently drop a deliberately-set
    fixed "Ending on" date, making the plot fall back to the most-recent-
    logged-day default (which drifts forward on its own too) even though
    rolling was off, and then making this same checkbox read as unchecked on
    the very next reload since the freshly recomputed qs re-embeds that
    resolved date explicitly while the saved one omitted it."""
    from urllib.parse import parse_qsl, urlencode
    if rolling:
        params = [(k, v) for k, v in parse_qsl(qs) if k not in ("anchor_date", "rolling")]
        # Match _nutrient_plot_qs()'s canonical ordering (rolling sits right
        # after days_back/anchor_date, before scale_factor/title/highlight/...)
        # so the saved qs string is byte-for-byte identical to the qs the next
        # page render recomputes — is_home_plot compares them with `==`, and
        # appending rolling at the end instead used to desync the two the
        # moment any later param (highlight, smoothing, ...) was present,
        # making "Show on Home page" read as unchecked right after saving it.
        insert_at = next((i + 1 for i, (k, _) in enumerate(params) if k == "days_back"), len(params))
        params.insert(insert_at, ("rolling", "1"))
    else:
        params = [(k, v) for k, v in parse_qsl(qs) if k != "rolling"]
    final_qs = urlencode(params)
    if enabled:
        _save_prefs_file({"home_nutrient_plot_qs": final_qs, "home_nutrient_plot_enabled": True})
    else:
        _save_prefs_file({"home_nutrient_plot_enabled": False})
    return RedirectResponse(f"/summary/nutrient-plot?{final_qs}", status_code=303)


@app.get("/summary/nutrient-plot/image")
async def nutrient_plot_image(
    request: Request,
    nutrients: list[str] = Query([]),
    days_back: str | None = Query(None),
    anchor_date: str | None = Query(None),
    scale_factor: str | None = Query(None),
    title: str | None = Query(None),
    highlight: str | None = Query(None),
    grayscale: bool = Query(False),
    legend: str = Query("auto"),
    smoothing: str | None = Query(None),
    fmt: str = Query("png"),
    download: bool = Query(False),
    rolling: bool = Query(False),
):
    from numa_app.services.plotting import line_plot_image

    image_format = "svg" if fmt == "svg" else "png"

    with _db.get_db() as conn:
        chosen, dates, _anchor = _nutrient_plot_params(conn, nutrients, days_back, anchor_date, rolling=rolling)
        if not chosen or not dates:
            raise HTTPException(status_code=404, detail="No nutrients or days selected")
        highlight_key = _resolve_highlight(chosen, highlight)
        raw_series, _info = _smoothed_plot_series(conn, chosen, dates, highlight_key,
                                                  _parse_smoothing_window(smoothing), rolling=rolling)
        if not raw_series:
            raise HTTPException(status_code=404, detail="No days with data in range")

    profile = _profile.load_profile()
    raw_series = _nutrient_plot_add_goals(raw_series, profile, _current_diet_pref())
    raw_series = _nutrient_plot_add_limits(raw_series, profile)

    factor = _parse_plot_factor(scale_factor) or _default_plot_scale_factor(raw_series)
    step1_series = _apply_plot_scale_factor(raw_series, factor)

    raw_factor_params = _nutrient_plot_factor_params(request.query_params, chosen)
    auto_individual = _default_individual_factors(step1_series)
    effective_individual = {
        k: (_parse_plot_factor(raw_factor_params.get(k)) or auto_individual.get(k, 1.0))
        for k in chosen
    }
    series = _apply_individual_factors(step1_series, effective_individual)

    plot_title = _user_plot_title(title) or _nutrient_plot_default_title(dates)
    plot_ylabel = _nutrient_plot_ylabel(chosen, series)
    has_goal = any(s.get("goal") is not None for s in series)
    has_limit = any(s.get("limit") is not None for s in series)
    if has_goal and has_limit:
        plot_subtitle = _NUTRIENT_PLOT_GOAL_AND_LIMIT_SUBTITLE
    elif has_goal:
        plot_subtitle = _NUTRIENT_PLOT_GOAL_SUBTITLE
    elif has_limit:
        plot_subtitle = _NUTRIENT_PLOT_LIMIT_SUBTITLE
    else:
        plot_subtitle = ""

    image_bytes = line_plot_image(series, xlabel="Date", ylabel=plot_ylabel,
                                   title=plot_title, subtitle=plot_subtitle,
                                   image_format=image_format, grayscale=grayscale,
                                   hide_y_values=(plot_ylabel == _GENERIC_PLOT_YLABEL),
                                   legend_pos=_plot_legend_pos(legend))
    media_type = "image/svg+xml" if image_format == "svg" else "image/png"
    headers = ({"Content-Disposition": f'attachment; filename="numa-nutrient-plot.{image_format}"'}
               if download else {})
    return Response(content=image_bytes, media_type=media_type, headers=headers)


@app.get("/summary/nutrient-plot/print", response_class=HTMLResponse)
async def nutrient_plot_print(
    request: Request,
    nutrients: list[str] = Query([]),
    days_back: str | None = Query(None),
    anchor_date: str | None = Query(None),
    scale_factor: str | None = Query(None),
    title: str | None = Query(None),
    highlight: str | None = Query(None),
    grayscale: bool = Query(False),
    legend: str = Query("auto"),
    smoothing: str | None = Query(None),
    rolling: bool = Query(False),
):
    with _db.get_db() as conn:
        chosen, dates, anchor = _nutrient_plot_params(conn, nutrients, days_back, anchor_date, rolling=rolling)
    if not chosen or not dates:
        return RedirectResponse("/summary/nutrient-plot", status_code=303)

    highlight_key = _resolve_highlight(chosen, highlight)
    raw_factor_params = _nutrient_plot_factor_params(request.query_params, chosen)
    user_title = _user_plot_title(title)
    effective_title = user_title or _nutrient_plot_default_title(dates)
    # Only persist a user-typed title into qs (same "blank means auto"
    # convention as the main nutrient-plot page) so following the "Back to
    # plot" link doesn't freeze the auto title at today's date range.
    qs = _nutrient_plot_qs(chosen, days_back, anchor, scale_factor, user_title,
                            highlight_key, grayscale, _parse_smoothing_window(smoothing), raw_factor_params,
                            rolling=rolling, legend=_plot_legend_pos(legend))

    return templates.TemplateResponse(request, "nutrient_plot_print.html", {
        "labels":     [_plot_label_for(k) for k in chosen],
        "start_date": dates[0],
        "end_date":   dates[-1],
        "title":      effective_title,
        "qs":         qs,
    })


def _build_day_rows(rows, conn) -> tuple[list[dict], list[dict], list[dict]]:
    """Recent-days sidebar rows: % goal read from the stored day_pct_goal
    (already scored against whichever profile was pinned to that date), plus
    that date's profile name and its own goal in grams — never a single
    page-wide profile/target, since different days can be pinned to
    different profiles with different targets. Also attaches the user's
    chosen extra nutrient columns (shared with Meals & Log), aggregated per
    day rather than per meal, plus the mandatory Protein column every Recent
    Days row always shows first. Every nutrient column (mandatory or picked)
    also gets a "% Goal" figure the same way — that date's own pinned
    profile's RDA/target/limit for that nutrient — stored per-row in
    pct_goal_map, keyed by nutrient key."""
    from numa_app.services.meal_list_columns import (
        saved_or_default as _saved_or_default_meal_nutrients, label_for as _meal_label_for, day_nutrient_values,
        day_nutrient_raw_totals, MANDATORY_DAY_COLUMNS, MANDATORY_DAY_KEYS,
    )
    show_profile = len(_profile.list_profiles()) > 1
    # Drop Protein if the user separately picked it as a Meals & Log column
    # (that picker still allows it) — Recent Days already shows it via its
    # own fixed column below, so it would otherwise appear twice. Calories/
    # Carbs/Fiber are no longer mandatory here, so they pass through
    # normally if picked (same as any other nutrient).
    nutrient_keys = [k for k in _saved_or_default_meal_nutrients(_load_prefs_file())
                     if k not in MANDATORY_DAY_KEYS]
    all_keys = MANDATORY_DAY_KEYS + nutrient_keys
    diet_pref = _current_diet_pref()
    day_complete_map = _db.day_completion_map(conn)
    day_rows = []
    for r in rows:
        d = r["meal_date"]
        bcp = r["day_bcp"]
        profile_name = None
        if show_profile:
            dp = _db.day_profile_get(conn, d)
            profile_name = dp["profile_name"] if dp else None
        # Computed once per day and reused for both the Protein goal below
        # and every other nutrient column's % Goal — each day can be pinned
        # to a different profile, so this can't be hoisted out of the loop.
        day_profile_obj = _day_profile.get_profile_for_date(conn, d)
        rda = _profile.compute_rda(day_profile_obj, diet_pref=diet_pref) if day_profile_obj else None
        goal = rda.get("protein_g", (None,))[0] if rda else None
        raw_totals = day_nutrient_raw_totals(conn, d, all_keys) if rda else {}
        pct_goal_map = {}
        for key in all_keys:
            if not rda or key not in rda or key not in raw_totals:
                continue
            rda_val, rda_unit, rda_type = rda[key]
            if not rda_val or rda_val <= 0:
                continue
            pct = round(raw_totals[key] / rda_val * 100)
            pct_goal_map[key] = {
                "pct":  pct,
                "goal": f"{rda_val:.1f} {rda_unit}",
                "css":  _rda_css(pct, rda_type),
            }
        day_rows.append({
            "meal_date":      d,
            "day_bcp":        round(bcp, 1) if bcp is not None else None,
            "goal":           round(goal, 0) if goal else None,
            "pct_goal":       r["day_pct_goal"],
            "profile_name":   profile_name,
            "day_complete":   day_complete_map.get(d, False),
            "mandatory_values": day_nutrient_values(conn, d, MANDATORY_DAY_KEYS),
            "nutrient_values": day_nutrient_values(conn, d, nutrient_keys),
            "pct_goal_map":   pct_goal_map,
        })
    mandatory_day_cols = [{"key": k, "label": lbl, "title": tip} for k, lbl, tip in MANDATORY_DAY_COLUMNS]
    return day_rows, [{"key": k, "label": _meal_label_for(k)} for k in nutrient_keys], mandatory_day_cols


@app.get("/summary", response_class=HTMLResponse)
async def summary_index(request: Request):
    """Summary landing: recent-days table + date picker."""
    with _db.get_db() as conn:
        rows = _db.meal_dates_with_bcp(conn, limit=30)
        day_rows, day_nutrient_cols, mandatory_day_cols = _build_day_rows(rows, conn)

    return templates.TemplateResponse(request, "summary.html", {
        "day_rows":       day_rows,
        "day_nutrient_cols": day_nutrient_cols,
        "mandatory_day_cols": mandatory_day_cols,
        "show_profile_col": len(_profile.list_profiles()) > 1,
        "today":          datetime.date.today().isoformat(),
        "date_detail":    None,
    })


@app.get("/summary/{meal_date}", response_class=HTMLResponse)
async def summary_date(request: Request, meal_date: str):
    """Full-day nutrient + DIAAS analysis for a specific date."""
    meals, combined_nutrients, diaas_result, day_ingredients = _day_analysis(meal_date)
    if not meals:
        return RedirectResponse("/summary", status_code=303)

    with _db.get_db() as conn:
        for m in meals:
            m_items = [dict(it) for it in _db.meal_get_items(conn, m["id"])]
            for it in m_items:
                if it["item_type"] == "recipe":
                    it["recipe_deleted"] = _db.recipe_get(conn, it["recipe_id"]) is None
            _annotate_recipe_amounts(m_items, conn)
            _annotate_food_amounts(m_items, conn)
            m["meal_items"] = _sort_meal_items_display(m_items)

    diaas_display = _build_diaas_display(diaas_result)

    if diaas_display and diaas_display.get("dcp_g") is not None:
        with _db.get_db() as conn:
            _db.day_bcp_cache_set(conn, meal_date, diaas_display["dcp_g"])

    aa_nutrients: dict = {}
    for m in meals:
        for k, v in _meal_aa_nutrients(m["id"]).items():
            aa_nutrients[k] = aa_nutrients.get(k, 0.0) + v

    gl_total_sum = 0.0
    all_gl_blockers: list[str] = []
    any_gl_none = False
    for m in meals:
        gl_val, gl_blockers = _compute_gl(m["id"])
        if gl_val is None:
            any_gl_none = True
        else:
            gl_total_sum += gl_val
        all_gl_blockers.extend(gl_blockers)
    gl_total = None if any_gl_none else round(gl_total_sum, 1)

    with _db.get_db() as conn:
        day_profile_obj = _day_profile.get_profile_for_date(conn, meal_date)
        day_profile_row = _db.day_profile_get(conn, meal_date)
    rda = _load_rda(day_profile_obj)
    optimal = _load_optimal(day_profile_obj)
    max_limits = _load_max_limits(day_profile_obj)

    # Recent days for sidebar
    with _db.get_db() as conn:
        rows = _db.meal_dates_with_bcp(conn, limit=14)
        day_rows, day_nutrient_cols, mandatory_day_cols = _build_day_rows(rows, conn)

    return templates.TemplateResponse(request, "summary.html", {
        "calorie_warnings":  _calorie_warnings(day_ingredients),
        "recalc_notes":      _recalc_notes([m["id"] for m in meals]),
        "day_rows":          day_rows,
        "mandatory_day_cols": mandatory_day_cols,
        "day_nutrient_cols": day_nutrient_cols,
        "show_profile_col":  len(_profile.list_profiles()) > 1,
        "today":             datetime.date.today().isoformat(),
        "date_detail":       meal_date,
        "meals":             meals,
        "nutrient_sections": _nutrient_sections(combined_nutrients, rda, combined_nutrients,
                                                optimal=optimal, max_limits=max_limits,
                                                dcp_g=diaas_display["dcp_g"] if diaas_display else None,
                                                dcp_missing=diaas_display["missing"] if diaas_display else None) if combined_nutrients else [],
        "diaas":             diaas_display,
        "dcp_missing_names": diaas_display["missing"] if diaas_display else [],
        "protein_adequacy":  _protein_adequacy(combined_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":       _complement_suggestions(aa_nutrients, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="daily", ingredients=day_ingredients),
        "gl":                {"total": gl_total, "blockers": all_gl_blockers},
        "has_profile":       rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
        "day_profile_name":       day_profile_row["profile_name"] if day_profile_row else None,
        "day_profile_overridden": bool(day_profile_row["overridden"]) if day_profile_row else False,
        "all_profile_names":      _profile.list_profiles(),
        "diet_notes":        _diet_aware_daily_notes(combined_nutrients, rda) if combined_nutrients else {},
    })


@app.post("/summary/{meal_date}/profile", response_class=RedirectResponse)
async def summary_date_profile_override(meal_date: str, profile_name: str = Form(...)):
    """Reassign which profile meal_date is scored against."""
    with _db.get_db() as conn:
        _day_profile.set_day_profile_override(conn, meal_date, profile_name)
    _refresh_day_pct_goal(meal_date)
    return RedirectResponse(f"/summary/{meal_date}", status_code=303)


def _parse_id_list_tokens(raw: str) -> list[int]:
    """Parse a comma/space-separated list of IDs, with "N-M" range tokens
    expanded — shared by the meal-IDs and recipe-IDs selection boxes on the
    Food Use analysis pages."""
    ids: list[int] = []
    for token in re.split(r"[\s,]+", raw.strip()):
        if not token:
            continue
        m = re.fullmatch(r"(\d+)-(\d+)", token)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if lo > hi:
                lo, hi = hi, lo
            ids.extend(range(lo, hi + 1))
            continue
        try:
            ids.append(int(token))
        except ValueError:
            pass
    return ids


def _parse_date_range_lines(raw: str) -> list[tuple[str, str]]:
    """Parse "YYYY-MM-DD:YYYY-MM-DD" lines (one per line) into (start, end)
    tuples, swapping a reversed pair — shared by the Food Use analysis pages."""
    ranges: list[tuple[str, str]] = []
    for line in raw.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        start, end = line.split(":", 1)
        start, end = start.strip(), end.strip()
        if start and end:
            if start > end:
                start, end = end, start
            ranges.append((start, end))
    return ranges


def _item_code(e: dict) -> str:
    """A Food Use row's display code (U171477, R21, ...), "" if it has none."""
    classified = _classify_food_id(e["fdc_id"], e["recipe_id"] if e["kind"] == "recipe" else None)
    return classified[0] if classified else ""


def _resolve_meals_for_food_use(
    conn, mode: str, ranges_raw: str, meal_ids: str
) -> tuple[dict[int, dict], list[tuple[str, str]], list[int]]:
    """Resolve the mode="range"/"ids" selection on Food Use in Meals into the
    actual set of meals — shared by the analysis page itself and the
    substitution action, so a substitution always applies to exactly the
    meals currently on screen."""
    ranges = _parse_date_range_lines(ranges_raw) if mode == "range" else []
    requested_ids = _parse_id_list_tokens(meal_ids) if mode != "range" else []

    meals_by_id: dict[int, dict] = {}
    missing_ids: list[int] = []
    for start, end in ranges:
        for row in _db.meal_list_by_date_range(conn, start, end):
            meals_by_id[row["id"]] = dict(row)
    if requested_ids:
        found = _db.meal_list_by_ids(conn, requested_ids)
        found_ids = {row["id"] for row in found}
        missing_ids = [i for i in requested_ids if i not in found_ids]
        for row in found:
            meals_by_id[row["id"]] = dict(row)
    return meals_by_id, ranges, missing_ids


@app.get("/analysis/food-use", response_class=HTMLResponse)
async def analysis_food_use(
    request: Request,
    mode: str = Query(default="range"),
    ranges_raw: str | None = Query(default=None),
    meal_ids: str = Query(default=""),
    protein_only: bool = Query(default=False),
    sort: str = Query(default="frequency"),
    substituted: int = Query(default=0),
    error: str = Query(default=""),
    sub_kind: str = Query(default=""),
    sub_id: int | None = Query(default=None),
):
    """Food use in meals: frequency-of-use table across a chosen set of meals.

    mode selects EITHER date range(s) ("range") OR meal IDs ("ids") — never both.

    sub_kind/sub_id pre-fill the "Replace this" side of the substitute form —
    used to deep-link here from a delete-blocked message (Food Cache, Custom
    Food Profiles) with the blocking food already selected as the thing to
    replace, scoped to exactly the meals that were blocking the deletion.
    """
    if ranges_raw is None:
        today = datetime.date.today()
        ranges_raw = f"{today - datetime.timedelta(days=30)}:{today}"

    with _db.get_db() as conn:
        meals_by_id, ranges, missing_ids = _resolve_meals_for_food_use(conn, mode, ranges_raw, meal_ids)
    requested_ids = _parse_id_list_tokens(meal_ids) if mode != "range" else []

    agg: dict[tuple, dict] = {}
    with _db.get_db() as conn:
        for meal_id, meal in meals_by_id.items():
            items = _db.meal_expand_food_items(conn, meal_id)
            seen: set = set()
            for fdc_id, name, kind, has_protein, deleted, recipe_id in items:
                if fdc_id is not None:
                    key = (fdc_id, kind)
                elif recipe_id is not None:
                    key = (kind, recipe_id)
                else:
                    key = (kind, name)
                if key in seen:
                    continue
                seen.add(key)
                entry = agg.setdefault(key, {
                    "name": name, "fdc_id": fdc_id, "kind": kind, "has_protein": has_protein,
                    "deleted": deleted, "recipe_id": recipe_id, "meal_ids": set(), "days": set(),
                })
                entry["meal_ids"].add(meal_id)
                entry["days"].add(meal["meal_date"])

    rows_all = list(agg.values())
    if protein_only:
        rows_all = [r for r in rows_all if r["has_protein"]]

    sort_keys = {
        "frequency": lambda e: (-len(e["days"]), -len(e["meal_ids"]), e["name"].lower()),
        "food":      lambda e: (e["name"].lower(),),
        "id":        lambda e: _code_sort_key(_item_code(e)),
    }
    rows_sorted = sorted(rows_all, key=sort_keys.get(sort, sort_keys["frequency"]))
    total_days = len({m["meal_date"] for m in meals_by_id.values()})
    result_rows = [{
        "fdc_id":    r["fdc_id"],
        "code":      _item_code(r),
        "name":      r["name"],
        "kind":      r["kind"],
        "deleted":   r["deleted"],
        "recipe_id": r["recipe_id"],
        "days":      len(r["days"]),
        "meals":     len(r["meal_ids"]),
        "pct":       round(len(r["days"]) / total_days * 100, 0) if total_days else 0,
        "meal_ids":  sorted(r["meal_ids"]),
    } for r in rows_sorted]

    return templates.TemplateResponse(request, "analysis_food_use.html", {
        "mode":          mode,
        "ranges":        ranges,
        "ranges_raw":    ranges_raw,
        "meal_ids_raw":  meal_ids,
        "protein_only":  protein_only,
        "sort":          sort,
        "missing_ids":   missing_ids,
        "rows":          result_rows,
        "total_meals":   len(meals_by_id),
        "total_days":    total_days,
        "submitted":     bool(ranges or requested_ids),
        "substituted":   substituted,
        "error":         error,
        "sub_kind":      sub_kind,
        "sub_id":        sub_id,
    })


@app.post("/analysis/food-use/substitute", response_class=RedirectResponse)
async def analysis_food_use_substitute(
    mode: str = Form(...),
    ranges_raw: str = Form(""),
    meal_ids: str = Form(""),
    protein_only: bool = Form(False),
    sort: str = Form("frequency"),
    old_code: str = Form(...),
    new_code: str = Form(...),
):
    """Replace every direct occurrence of (old_kind, old_id) with (new_kind,
    new_id) across the meals currently selected on the Food Use in Meals page
    — the same date range(s)/meal-IDs selection already on screen, so a
    substitution always matches exactly what the user was just looking at."""
    from urllib.parse import urlencode

    def _back(error: str | None = None, n: int = 0) -> RedirectResponse:
        params = {"mode": mode, "protein_only": protein_only, "sort": sort}
        if mode == "range":
            params["ranges_raw"] = ranges_raw
        else:
            params["meal_ids"] = meal_ids
        if error:
            params["error"] = error
        elif n:
            params["substituted"] = n
        return RedirectResponse(f"/analysis/food-use?{urlencode(params)}", status_code=303)

    try:
        old_kind, old_id = _parse_code(old_code)
        new_kind, new_id = _parse_code(new_code)
    except ValueError as exc:
        return _back(error=str(exc))
    if old_kind == new_kind and old_id == new_id:
        return _back(error="Old and new selections are the same item.")
    try:
        with _db.get_db() as conn:
            meals_by_id, _, _ = _resolve_meals_for_food_use(conn, mode, ranges_raw, meal_ids)
            n = _db.substitute_item_in_meals(conn, list(meals_by_id), old_kind, old_id, new_kind, new_id)
    except ValueError as exc:
        return _back(error=str(exc))
    return _back(n=n)


def _parse_food_use_recipes_selection(
    conn, mode: str, ranges_raw: str, recipe_ids: str
) -> tuple[dict[int, dict], list[tuple[str, str]], list[int]]:
    """Resolve Food Use in Recipes' mode="all"/"range"/"ids" selection into
    the actual set of (container) recipes — shared by the analysis page and
    the substitution action."""
    if mode == "all":
        recipes_by_id = {row["id"]: dict(row) for row in _db.recipe_list(conn)}
        return recipes_by_id, [], []

    ranges = _parse_date_range_lines(ranges_raw) if mode == "range" else []
    requested_ids = _parse_id_list_tokens(recipe_ids) if mode == "ids" else []

    recipes_by_id: dict[int, dict] = {}
    missing_ids: list[int] = []
    for start, end in ranges:
        for row in _db.recipe_list_by_created_range(conn, start, end):
            recipes_by_id[row["id"]] = dict(row)
    if requested_ids:
        found = _db.recipe_list_by_ids(conn, requested_ids)
        found_ids = {row["id"] for row in found}
        missing_ids = [i for i in requested_ids if i not in found_ids]
        for row in found:
            recipes_by_id[row["id"]] = dict(row)
    return recipes_by_id, ranges, missing_ids


@app.get("/analysis/food-use-recipes", response_class=HTMLResponse)
async def analysis_food_use_recipes(
    request: Request,
    mode: str = Query(default="all"),
    ranges_raw: str = Query(default=""),
    recipe_ids: str = Query(default=""),
    protein_only: bool = Query(default=False),
    sort: str = Query(default="frequency"),
    substituted: int = Query(default=0),
    error: str = Query(default=""),
    sub_kind: str = Query(default=""),
    sub_id: int | None = Query(default=None),
):
    """Food use in recipes: frequency-of-use table across a chosen set of
    (container) recipes — how many of them use a given food or sub-recipe as
    an ingredient, directly or nested. mode selects ALL recipes ("all",
    default), a date range by when the recipe was created ("range"), or
    specific recipe IDs ("ids").

    sub_kind/sub_id pre-fill the "Replace this" side of the substitute form —
    used to deep-link here from a delete-blocked message (Food Cache, Custom
    Food Profiles) with the blocking food already selected as the thing to
    replace, scoped to exactly the recipes that were blocking the deletion.
    """
    with _db.get_db() as conn:
        recipes_by_id, ranges, missing_ids = _parse_food_use_recipes_selection(conn, mode, ranges_raw, recipe_ids)
    requested_ids = _parse_id_list_tokens(recipe_ids) if mode == "ids" else []

    agg: dict[tuple, dict] = {}
    with _db.get_db() as conn:
        for recipe_id in recipes_by_id:
            items = _db.recipe_expand_ingredient_use(conn, recipe_id)
            seen: set = set()
            for fdc_id, name, kind, has_protein, ref_recipe_id in items:
                if fdc_id is not None:
                    key = (fdc_id, "food")
                elif ref_recipe_id is not None:
                    key = ("recipe", ref_recipe_id)
                else:
                    key = (kind, name)
                if key in seen:
                    continue
                seen.add(key)
                entry = agg.setdefault(key, {
                    "name": name, "fdc_id": fdc_id, "kind": kind, "has_protein": has_protein,
                    "recipe_id": ref_recipe_id, "container_ids": set(),
                })
                entry["container_ids"].add(recipe_id)

    rows_all = list(agg.values())
    if protein_only:
        rows_all = [r for r in rows_all if r["has_protein"]]

    sort_keys = {
        "frequency": lambda e: (-len(e["container_ids"]), e["name"].lower()),
        "food":      lambda e: (e["name"].lower(),),
        "id":        lambda e: _code_sort_key(_item_code(e)),
    }
    rows_sorted = sorted(rows_all, key=sort_keys.get(sort, sort_keys["frequency"]))
    total_recipes = len(recipes_by_id)
    result_rows = [{
        "fdc_id":      r["fdc_id"],
        "code":        _item_code(r),
        "name":        r["name"],
        "kind":        r["kind"],
        "recipe_id":   r["recipe_id"],
        "count":       len(r["container_ids"]),
        "pct":         round(len(r["container_ids"]) / total_recipes * 100, 0) if total_recipes else 0,
        "recipe_ids":  sorted(r["container_ids"]),
    } for r in rows_sorted]

    return templates.TemplateResponse(request, "analysis_food_use_recipes.html", {
        "mode":           mode,
        "ranges":         ranges,
        "ranges_raw":     ranges_raw,
        "recipe_ids_raw": recipe_ids,
        "protein_only":   protein_only,
        "sort":           sort,
        "missing_ids":    missing_ids,
        "rows":           result_rows,
        "total_recipes":  total_recipes,
        "submitted":      mode == "all" or bool(ranges or requested_ids),
        "substituted":    substituted,
        "error":          error,
        "sub_kind":       sub_kind,
        "sub_id":         sub_id,
    })


@app.post("/analysis/food-use-recipes/substitute", response_class=RedirectResponse)
async def analysis_food_use_recipes_substitute(
    mode: str = Form(...),
    ranges_raw: str = Form(""),
    recipe_ids: str = Form(""),
    protein_only: bool = Form(False),
    sort: str = Form("frequency"),
    old_code: str = Form(...),
    new_code: str = Form(...),
):
    """Replace every ingredient occurrence of (old_kind, old_id) with
    (new_kind, new_id) across the recipes currently selected on the Food Use
    in Recipes page, then recompute DCP for every recipe actually changed
    (recompute_recipe_dcp cascades up to any ancestor recipe on its own)."""
    from urllib.parse import urlencode

    def _back(error: str | None = None, n: int = 0) -> RedirectResponse:
        params = {"mode": mode, "protein_only": protein_only, "sort": sort}
        if mode == "range":
            params["ranges_raw"] = ranges_raw
        elif mode == "ids":
            params["recipe_ids"] = recipe_ids
        if error:
            params["error"] = error
        elif n:
            params["substituted"] = n
        return RedirectResponse(f"/analysis/food-use-recipes?{urlencode(params)}", status_code=303)

    try:
        old_kind, old_id = _parse_code(old_code)
        new_kind, new_id = _parse_code(new_code)
    except ValueError as exc:
        return _back(error=str(exc))
    if old_kind == new_kind and old_id == new_id:
        return _back(error="Old and new selections are the same item.")
    try:
        with _db.get_db() as conn:
            recipes_by_id, _, _ = _parse_food_use_recipes_selection(conn, mode, ranges_raw, recipe_ids)
            affected_ids = _db.substitute_item_in_recipes(
                conn, list(recipes_by_id), old_kind, old_id, new_kind, new_id
            )
            for recipe_id in affected_ids:
                _recipe_dcp.recompute_recipe_dcp(recipe_id, conn)
    except ValueError as exc:
        return _back(error=str(exc))
    return _back(n=len(affected_ids))


@app.get("/manual", response_class=HTMLResponse)
async def manual(request: Request):
    from numa_app.services.manual_build import rebuild_manual_if_stale
    # Rebuild only ever applies to the baked-in copy (it has a .md source
    # beside it); a downloaded manual is html-only and must never be rebuilt.
    rebuild_manual_if_stale()
    active = _manual_update.get_active_manual(_MANUAL)
    if not active["path"].exists():
        return HTMLResponse("<p>User manual not found. Run <code>make manual</code> to generate it.</p>", status_code=404)
    return HTMLResponse(active["path"].read_text(encoding="utf-8"))


@app.get("/disclaimer", response_class=HTMLResponse)
async def disclaimer(request: Request):
    if not _DISCLAIMER_MD.exists():
        return HTMLResponse("<p>Disclaimer not found.</p>", status_code=404)
    body = _md.markdown(_DISCLAIMER_MD.read_text(encoding="utf-8"), extensions=["footnotes"])
    return templates.TemplateResponse(request, "disclaimer.html", {"body": body})
