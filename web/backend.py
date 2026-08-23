"""
backend.py — FastAPI web interface for numa nutritional analysis.
Docs: README-numa-documentation.md, Architecture: "web/ — Local web app"
"""
import datetime
import io
import json
import math
import re
import sys
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlencode

if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(Path(__file__).parent.parent))

import markdown as _md
from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import afcd_lookup as _afcd
import ciqual_lookup as _ciqual
import cnf_api as _cnf
import cofid_lookup as _cofid
import db as _db
import diaas as _diaas
import openfoodfacts as _off
import profile as _profile
import usda as _usda
from numa_app.services import claude_fetch as _claude_fetch
from numa_app.services import complements as _complements
from numa_app.services import csv_export as _csv_export
from numa_app.services import csv_import as _csv_import
from numa_app.services import recipe_csv as _recipe_csv
from numa_app.services import day_profile as _day_profile
from numa_app.services import aa_estimate as _aa_estimate
from numa_app.services.glycemic_load import compute_glycemic_load
from numa_app.services.meal_bcp import recipe_dcp_fallback
from numa_app.services.nutrient_trend import average_from_daily_totals
from numa_app.services.portions import _ing_amount_display, volume_hint
from numa_app.services.portions import _UNIT_TO_GRAMS as _PORTION_UNIT_TO_G
from version import VERSION
from numa_app.services.portions import _VOLUME_TO_ML as _PORTION_VOL_TO_ML
from numa_app.services.rda_status import rda_status, limit_warning
from numa_app.services.diet_aware import b12_deficiency_note, iron_zinc_bioavailability_note
from numa_app.services.recipe_nutrients import (
    atomic_recipe_ingredients, best_aa_nutrients, expand_recipe_ingredients, recipe_total_nutrients,
)
from numa_app.services.top_contributors import rank_contributors, rank_contributors_by_dcp
from numa_app.services import recipe_dcp as _recipe_dcp
from numa_app.services import search_ranking as _search_ranking
from numa_app.services import print_sections as _print_sections

# In a PyInstaller onefile build, backend.py is bundled as a flattened
# top-level module — there's no separate web/ subdirectory nested under a
# project root, both collapse to sys._MEIPASS. Source (non-frozen) layout
# still has web/backend.py one level below the real project root.
_WEB_DIR     = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
_PROJECT_ROOT = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else _WEB_DIR.parent
_MANUAL     = _PROJECT_ROOT / "user-manual.html"
_HOME_MD    = _PROJECT_ROOT / "home.md"
_PREFS_FILE = Path.home() / ".local" / "share" / "numa" / "prefs.json"

_HOME_CACHE = _WEB_DIR / "home_body.cache"

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
    if not _HOME_MD.exists():
        return ""
    if _HOME_CACHE.exists() and _HOME_CACHE.stat().st_mtime >= _HOME_MD.stat().st_mtime:
        return _HOME_CACHE.read_text(encoding="utf-8")
    html = _md.markdown(_HOME_MD.read_text(encoding="utf-8"), extensions=["footnotes"])
    _HOME_CACHE.write_text(html, encoding="utf-8")
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

# Compare Foods (/food/compare) can't hold a recipe as a comparison entry —
# entries are per-100g food nutrient data keyed by fdc_id, which recipes
# don't have. Recipe-to-recipe comparison lives at /recipe/compare instead,
# so "Recipes" is left out of this page's source filter.
_FOOD_COMPARE_SOURCE_FILTERS = [s for s in _SEARCH_SOURCE_FILTERS if s != "recipe"]


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

# The "highlighted" nutrient (user-selectable, defaults to Day DCP if
# chosen) always draws in this fixed red and solid, so the one figure
# everything else is usually compared against stands out — regardless of
# which nutrient that is this time. In grayscale mode it's still the one
# solid line; everything else switches to a dash pattern instead of color.
_HIGHLIGHT_COLOR = "#e34948"


def _plot_label_for(key: str) -> str:
    if key == _DCP_PLOT_KEY:
        return _DCP_PLOT_LABEL
    from numa_app.services.meal_list_columns import label_for as _nutrient_label_for
    return _nutrient_label_for(key)


def _sort_search_results(results: list[dict], query: str, mode: str) -> list[dict]:
    """Order search results by match quality: how many query words a name
    contains (all > all-but-one > ...), with ties broken first by which
    specific words matched (earlier query words outrank later ones — see
    numa_app.services.search_ranking) and only then by source category
    (pantry/cache/recipe/external). "Pantry, Cache, then Other" mode instead
    sorts strictly by source category first, for users who want their own
    data ahead of everything else regardless of match quality."""
    if mode == "grouped":
        return sorted(
            results,
            key=lambda r: (_SEARCH_CATEGORY_RANK.get(r["source"], 9),
                            _search_ranking.relevance_key(r["name"], query, data_type=r.get("data_type", ""))),
        )
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
            return "✓" if _usda.has_amino_acid_data(json.loads(nuts_json)) else "✗"
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
            "diaas":     _ann_diaas(fid),
        })
    return _sort_search_results(results, q, sort)


def _pantry_fdc_ids(conn) -> set[int]:
    return {r["fdc_id"] for r in _db.pantry_list(conn) if r["fdc_id"]}


def _current_diet_pref() -> str:
    """Return the saved dietary preference, validated, defaulting to 'all'."""
    pref = _load_prefs_file().get("diet_pref", "all")
    return pref if pref in _VALID_DIET_PREFS else "all"

@asynccontextmanager
async def _lifespan(app: FastAPI):
    # Apply schema/migrations on web server startup, since the web app owns
    # the database and nothing else initializes it first.
    _db.init_db()
    with _db.get_db() as conn:
        from numa_app.services import demo_data as _demo_data
        _demo_data.seed_if_fresh_install(conn)
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
    yield

app = FastAPI(title="numa", lifespan=_lifespan)
app.mount("/static", StaticFiles(directory=_WEB_DIR / "static"), name="static")
templates = Jinja2Templates(directory=_WEB_DIR / "templates")

# Custom Jinja2 filters
templates.env.filters["ftin_ft"]  = lambda cm: _profile.cm_to_ftin(cm)[0]
templates.env.filters["ftin_in"]  = lambda cm: round(_profile.cm_to_ftin(cm)[1], 1)
templates.env.filters["fromjson"] = json.loads

def _manual_link(anchor: str, text: str = "Learn more") -> str:
    """Render an inline link to a user-manual section, opened in a new tab."""
    from markupsafe import Markup, escape
    return Markup(
        f'<a class="manual-link" href="/manual#{escape(anchor)}" target="_blank" rel="noopener">{escape(text)} &rarr;</a>'
    )

templates.env.globals["manual_link"] = _manual_link
templates.env.globals["is_local_source"] = _is_local_source

def _food_id_tag(fdc_id: int | None, recipe_id: int | None = None) -> str:
    """Render the '(#id, SOURCE)' annotation shown on its own line under a food/recipe name."""
    from markupsafe import Markup, escape
    from numa_app.services.food_ids import classify_food_id
    classified = classify_food_id(fdc_id, recipe_id)
    if classified is None:
        return ""
    id_str, source = classified
    return Markup(f'<span class="food-id-tag">(#{escape(id_str)}, {escape(source)})</span>')

templates.env.globals["food_id_tag"] = _food_id_tag
templates.env.globals["diet_labels"] = _DIET_LABELS
templates.env.globals["current_diet_pref"] = _current_diet_pref

# ---------------------------------------------------------------------------
# Nutrient display groups (ordered for presentation)
# ---------------------------------------------------------------------------

_NUTRIENT_GROUPS: list[tuple[str, list[str]]] = [
    ("Macronutrients", [
        "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
        "saturated_fat_g", "mono_fat_g", "poly_fat_g",
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


def _nutrient_sections(nutrients: dict, rda: dict | None = None,
                       daily_nutrients: dict | None = None,
                       optimal: dict | None = None,
                       max_limits: dict | None = None) -> list[dict]:
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
            day_pct = day_rda_css = None
            if rda and key in rda:
                rda_val, _rda_unit, rda_type = rda[key]
                if rda_val and rda_val > 0:
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


def _oxalate_info(fdc_id: int | None, food_name: str) -> dict | None:
    """Return oxalate data for one food, auto-linking on first call if not yet linked.

    Returns None when oxalate.db is unavailable, fdc_id is invalid/negative, or no
    good match was found.  Returned dict keys:
        mg_per_100g (float|None), mg_per_serving (float|None), serving_size (str|None),
        category (str), ref_name (str), confirmed (bool)
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
    missing: list[str] = []

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
            rows.append({
                "name":      name,
                "amount_g":  round(amount_g, 1),
                "mg":        round(mg, 1),
                "category":  info["category"],
                "confirmed": info["confirmed"],
            })
        elif info["mg_per_serving"] is not None:
            serving_g = _serving_str_to_grams(info["serving_size"] or "")
            if serving_g and serving_g > 0 and _serving_is_weight(info["serving_size"] or ""):
                # Weight-based serving → derive mg/100g and compute exact portion mg
                mg_per_100g = info["mg_per_serving"] / serving_g * 100.0
                mg = mg_per_100g * amount_g / 100.0
                total_mg += mg
                rows.append({
                    "name":      name,
                    "amount_g":  round(amount_g, 1),
                    "mg":        round(mg, 1),
                    "category":  info["category"],
                    "confirmed": info["confirmed"],
                })
            else:
                # Volume-based serving — density unknown, category only
                qualitative.append({
                    "name":      name,
                    "category":  info["category"],
                    "confirmed": info["confirmed"],
                })
        else:
            missing.append(name)

    if not rows and not qualitative:
        return None
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
    diaas = _usda.get_diaas(food_name)
    digestibility = diaas if diaas is not None else 1.0
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
    protein_digestible = round(protein_raw * digestibility, 1) if diaas is not None else None
    limiting_score = min(pc["scores"].values()) if pc["scores"] else None
    dcp_g = None
    if protein_digestible is not None and limiting_score is not None:
        dcp_g = round(protein_digestible * min(1.0, limiting_score), 1)
    return {
        "diaas":              diaas,
        "diaas_pct":          min(100, round(diaas * 100)) if diaas is not None else None,
        "diaas_level":        ("good" if diaas >= 0.90 else ("ok" if diaas >= 0.70 else "low")) if diaas is not None else None,
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


def _food_complement_section(food_name: str, nutrients: dict, exclude_names: set[str] | None = None,
                              comp_sort: str | None = None, diaas_sort: str | None = None) -> dict:
    """Complement suggestions for a single food, using its own DIAAS as digestibility."""
    if not _usda.has_amino_acid_data(nutrients) or nutrients.get("protein_g", 0) <= 0:
        return {"no_data": True}
    diaas = _usda.get_diaas(food_name)
    digestibility = diaas if diaas is not None else 1.0
    prefs = _load_prefs_file()
    diet_pref = prefs.get("diet_pref", "all")
    pantry = _web_pantry_candidates() + _web_recipe_candidates()
    cache_candidates = _complements.load_cache_candidates({c["name"].lower() for c in pantry})
    comp_sort = comp_sort or _resolve_sort(None, "sort_complements", "effect", _COMPLEMENT_SORT_MODES)
    diaas_sort = diaas_sort or _resolve_sort(None, "sort_diaas_improvers", "effect", _COMPLEMENT_SORT_MODES)
    return _complements.build_complement_display(
        nutrients, pantry, diet_pref=diet_pref,
        digestibility=digestibility, base_food_name=food_name,
        max_improver_grams=120, cache_candidates=cache_candidates,
        exclude_names=exclude_names,
        comp_sort=comp_sort,
        diaas_sort=diaas_sort,
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
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
    return templates.TemplateResponse(
        request, "home.html", {
            "home_body": _render_home_md(), "version": VERSION,
            "diet_label": diet_label, "profile_label": profile_label,
            "unacked_errors": unacked_errors,
        }
    )


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
        pantry_ids = _pantry_fdc_ids(conn)
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
            "source":    "pantry" if row["fdc_id"] in pantry_ids else "cache",
            "aa":        "✓" if _usda.has_amino_acid_data(nutrients) else "✗",
            "gi":        round(ann["gi_estimate"]) if ann and ann["gi_estimate"] is not None else None,
            "diaas":     round(ann["diaas_estimate"], 2) if ann and ann["diaas_estimate"] is not None else None,
            "has_notes": bool(row["notes"]),
        })
    matching_recipes = [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)]
    for r in matching_recipes:
        results.append({
            "_type":     "recipe",
            "recipe_id": r["id"],
            "name":      r["name"],
            "data_type": "Recipe",
            "brand":     "",
            "source":    "recipe",
            "aa":        "✓" if r["dcp_g"] is not None else "—",
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
                "aa":        "✓" if _usda.has_amino_acid_data(nutrients) else "✗",
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
                    "aa":        "✓" if _usda.has_amino_acid_data(detail.get("nutrients", {})) else "✗",
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
        },
        "ingredients":        display_ingredients,
        "nutrient_sections":  _nutrient_sections(scaled, rda, optimal=optimal, max_limits=max_limits),
        "diaas_display":      diaas_display,
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
        portions = [{"description": "1 serving", "gram_weight": round(total_weight / servings, 1)}]

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
    """Build comparison group rows from a list of {name, amount, nutrients} dicts."""
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


def _load_compare_entries(ids: list[int], amounts: list[float]) -> list[dict]:
    """Load food data for comparison, scaling nutrients to given gram amounts."""
    entries = []
    for fdc_id, amount in zip(ids, amounts):
        nutrients: dict = {}
        name = str(fdc_id)
        data_type = ""
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached:
            nutrients_100g = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
            name = cached["name"]
            data_type = cached["data_type"] or ""
        else:
            try:
                detail = _usda.get_food_detail(fdc_id)
                nutrients_100g = detail.get("nutrients", {})
                name = detail["name"]
                data_type = detail.get("dataType", "")
            except Exception:
                nutrients_100g = {}
        nutrients = _usda.scale_nutrients(nutrients_100g, amount) if amount != 100.0 else nutrients_100g
        entries.append({
            "fdc_id":    fdc_id,
            "name":      name,
            "data_type": data_type,
            "amount":    amount,
            "nutrients": nutrients,
            "cached":    cached is not None,
            "has_aa":    _usda.has_amino_acid_data(nutrients_100g),
        })
    return entries


def _parse_ids_amounts(ids_str: str, amounts_str: str) -> tuple[list[int], list[float]]:
    ids = [int(x) for x in ids_str.split(",") if x.strip()] if ids_str.strip() else []
    raw_amounts = [x.strip() for x in amounts_str.split(",") if x.strip()] if amounts_str.strip() else []
    amounts = []
    for i, fid in enumerate(ids):
        try:
            amounts.append(float(raw_amounts[i]) if i < len(raw_amounts) else 100.0)
        except (ValueError, IndexError):
            amounts.append(100.0)
    return ids, amounts


@app.get("/food/compare", response_class=HTMLResponse)
async def food_compare_get(
    request: Request,
    ids: str = "",
    amounts: str = "",
    error: str = "",
    search: str = "",
    source: list[str] | None = Query(default=None),
    limit: int | None = None,
):
    source = _resolve_source_filter(source, "sort_food_search_source", _FOOD_COMPARE_SOURCE_FILTERS)
    limit = _resolve_result_limit(limit)
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    entries = _load_compare_entries(id_list, amount_list) if id_list else []
    compare_groups = _build_compare_groups(entries) if len(entries) >= 2 else []
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)

    search_results: list[dict] = []
    search_error: str | None = None
    search = search.strip()
    if search:
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, search)
            pantry_ids = _pantry_fdc_ids(conn)
        seen: set[int] = set(id_list)  # exclude already-added foods
        for row in cached:
            if row["fdc_id"] not in seen:
                seen.add(row["fdc_id"])
                search_results.append({
                    "fdc_id":    row["fdc_id"],
                    "name":      row["name"],
                    "data_type": row["data_type"],
                    "brand":     row["brand"] or "",
                    "source":    "pantry" if row["fdc_id"] in pantry_ids else "cache",
                })
        try:
            for food in _usda.search_foods(search, page_size=limit):
                fid = food.get("fdcId")
                if fid and fid not in seen:
                    seen.add(fid)
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
        saved_lists = _db.saved_comparison_list(conn)

    return templates.TemplateResponse(request, "food_compare.html", {
        "entries":        entries,
        "compare_groups": compare_groups,
        "ids_str":        ids_str,
        "amounts_str":    amounts_str,
        "error":          error,
        "search":         search,
        "search_results": search_results,
        "search_error":   search_error,
        "saved_lists":    saved_lists,
        "source":         source,
        "limit":          limit,
        "source_filters": _FOOD_COMPARE_SOURCE_FILTERS,
        "source_labels":  _SEARCH_SOURCE_LABELS,
    })


@app.get("/food/compare/export.csv")
async def food_compare_export_csv(ids: str = "", amounts: str = ""):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    entries = _load_compare_entries(id_list, amount_list) if id_list else []
    compare_groups = _build_compare_groups(entries) if len(entries) >= 2 else []
    csv_text = _csv_export.compare_to_csv(entries, compare_groups)
    filename = f"numa_food_compare_{datetime.date.today().isoformat()}.csv"
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/food/compare/add", response_class=RedirectResponse)
async def food_compare_add(
    fdc_id: int = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)
    if len(id_list) >= 8:
        return RedirectResponse(
            f"/food/compare?ids={ids_str}&amounts={amounts_str}&error=Maximum+8+foods+allowed",
            status_code=303,
        )
    if fdc_id not in id_list:
        id_list.append(fdc_id)
        amount_list.append(100.0)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)
    return RedirectResponse(
        f"/food/compare?ids={ids_str}&amounts={amounts_str}",
        status_code=303,
    )


@app.post("/food/compare/add-multiple", response_class=RedirectResponse)
async def food_compare_add_multiple(request: Request, ids: str = Form(""), amounts: str = Form("")):
    """Bulk-add checked foods to the comparison — used both by Compare Foods'
    own "add via search" panel and by the compare checkboxes on Foods search,
    Food Cache, and My Pantry (which post straight here to jump into a
    comparison without first landing on this page)."""
    form = await request.form()
    fdc_ids = form.getlist("fdc_id")
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    added = skipped = 0
    for fdc_id_str in fdc_ids:
        try:
            fdc_id = int(fdc_id_str)
        except (ValueError, TypeError):
            continue
        if fdc_id in id_list:
            continue
        if len(id_list) >= 8:
            skipped += 1
            continue
        id_list.append(fdc_id)
        amount_list.append(100.0)
        added += 1
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)
    url = f"/food/compare?ids={ids_str}&amounts={amounts_str}"
    if skipped:
        url += f"&error=Added+{added}%2C+skipped+{skipped}+%E2%80%94+maximum+8+foods"
    return RedirectResponse(url, status_code=303)


@app.post("/food/compare/remove", response_class=RedirectResponse)
async def food_compare_remove(
    remove_id: int = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    paired = [(i, a) for i, a in zip(id_list, amount_list) if i != remove_id]
    new_ids = [str(p[0]) for p in paired]
    new_amounts = [str(p[1]) for p in paired]
    return RedirectResponse(
        f"/food/compare?ids={','.join(new_ids)}&amounts={','.join(new_amounts)}",
        status_code=303,
    )


@app.post("/food/compare/cache-food", response_class=RedirectResponse)
async def food_compare_cache_food(
    fdc_id: int = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
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
    return RedirectResponse(f"/food/compare?ids={ids}&amounts={amounts}", status_code=303)


@app.post("/food/compare/amounts", response_class=RedirectResponse)
async def food_compare_amounts(request: Request, ids: str = Form("")):
    form = await request.form()
    id_list = [int(x) for x in ids.split(",") if x.strip()] if ids.strip() else []
    new_amounts = []
    for fid in id_list:
        try:
            val = float(form.get(f"amounts_{fid}", 100.0))
            new_amounts.append(max(1.0, val))
        except (ValueError, TypeError):
            new_amounts.append(100.0)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in new_amounts)
    return RedirectResponse(f"/food/compare?ids={ids_str}&amounts={amounts_str}", status_code=303)


@app.post("/food/compare/save", response_class=RedirectResponse)
async def food_compare_save(
    name: str = Form(""),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    if len(id_list) >= 2:
        with _db.get_db() as conn:
            _db.saved_comparison_save(conn, name.strip() or "Untitled", id_list, amount_list)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)
    return RedirectResponse(f"/food/compare?ids={ids_str}&amounts={amounts_str}", status_code=303)


@app.get("/food/compare/load/{cmp_id}", response_class=RedirectResponse)
async def food_compare_load(cmp_id: int):
    with _db.get_db() as conn:
        row = _db.saved_comparison_get(conn, cmp_id)
    if not row:
        return RedirectResponse("/food/compare", status_code=303)
    ids_str = ",".join(str(i) for i in json.loads(row["fdc_ids"]))
    amounts_str = ",".join(str(a) for a in json.loads(row["amounts"]))
    return RedirectResponse(f"/food/compare?ids={ids_str}&amounts={amounts_str}", status_code=303)


@app.post("/food/compare/saved/rename", response_class=RedirectResponse)
async def food_compare_saved_rename(
    cmp_id: int = Form(...),
    name: str = Form(""),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    new_name = name.strip() or "Untitled"
    with _db.get_db() as conn:
        _db.saved_comparison_rename(conn, cmp_id, new_name)
    url = f"/food/compare?ids={ids}&amounts={amounts}" if ids else "/food/compare"
    return RedirectResponse(url, status_code=303)


@app.post("/food/compare/saved/delete", response_class=RedirectResponse)
async def food_compare_saved_delete(
    cmp_id: int = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    with _db.get_db() as conn:
        _db.saved_comparison_delete(conn, cmp_id)
    ids_str = ids.strip()
    amounts_str = amounts.strip()
    url = f"/food/compare?ids={ids_str}&amounts={amounts_str}" if ids_str else "/food/compare"
    return RedirectResponse(url, status_code=303)


_FOOD_CACHE_SORT_KEYS = {
    "name":  lambda f: (f["name"] or "").lower(),
    "type":  lambda f: ((f["data_type"] or "").lower(), (f["name"] or "").lower()),
    "diaas": lambda f: (f["diaas"] is None, -(f["diaas"] or 0), (f["name"] or "").lower()),
    "gi":    lambda f: (f["gi"] is None, -(f["gi"] or 0), (f["name"] or "").lower()),
}


@app.get("/food/cache", response_class=HTMLResponse)
async def food_cache_get(request: Request, q: str = "", pruned: int = 0, sort: str | None = None,
                          show_archived: bool | None = None, archived: int = 0, restored: int = 0,
                          still_used: int = 0, imported: int = 0, delete_blocked: int = 0,
                          blocked_pantry: str = "", blocked_recipes: str = "", blocked_meals: str = ""):
    sort = _resolve_sort(sort, "sort_food_cache", "name", set(_FOOD_CACHE_SORT_KEYS))
    show_archived = _resolve_bool_pref(show_archived, "show_archived_food_cache")
    with _db.get_db() as conn:
        if q.strip():
            rows = _db.search_cached_foods(conn, q.strip(), include_archived=show_archived)
        else:
            rows = _db.list_cached_foods(conn, include_archived=show_archived)
        fdc_ids = [r["fdc_id"] for r in rows]
        annotations = _db.annotations_for_fdcids(conn, fdc_ids) if fdc_ids else {}

    foods = []
    for row in rows:
        ann = annotations.get(row["fdc_id"])
        nuts = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
        has_aa = _usda.has_amino_acid_data(nuts)
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
            "diaas":          diaas,
            "diaas_saved":    diaas_saved is not None,
            "notes":          row["notes"] or "",
            "curator_notes":  row["curator_notes"] or "" if "curator_notes" in row.keys() else "",
            "archived":       bool(row["archived"]),
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
        "delete_blocked": delete_blocked,
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
async def food_cache_delete(fdc_id: int = Form(...), q: str = Form(""),
                             sort: str = Form(""), show_archived: int = Form(0)):
    """Delete a cached food — refused if a pantry entry, recipe, or meal still
    references it, since that would silently orphan the reference (it would
    keep pointing at an fdc_id with no data behind it, breaking that food's
    page). Use Archive instead to hide a still-referenced food."""
    params = {"q": q, "sort": sort, "show_archived": show_archived}
    with _db.get_db() as conn:
        refs = _db.food_references(conn, fdc_id)
        if refs["pantry"] or refs["recipes"] or refs["meals"]:
            params["delete_blocked"] = 1
            if refs["pantry"]:
                params["blocked_pantry"] = ",".join(str(i) for i in refs["pantry"])
            if refs["recipes"]:
                params["blocked_recipes"] = ",".join(str(i) for i in refs["recipes"])
            if refs["meals"]:
                params["blocked_meals"] = ",".join(str(i) for i in refs["meals"])
            return RedirectResponse(f"/food/cache?{urlencode(params)}", status_code=303)
        _db.delete_cached_food(conn, fdc_id)
    return RedirectResponse(f"/food/cache?{urlencode(params)}", status_code=303)


# ---------------------------------------------------------------------------
# Claude AI amino-acid/nutrient fetch workflow — see numa_app/services/
# claude_fetch.py for the prompt-building and response-parsing logic.
# ---------------------------------------------------------------------------

@app.post("/food/cache/claude-fetch", response_class=HTMLResponse)
async def food_cache_claude_fetch(request: Request, fdc_id: list[int] = Form(default=[])):
    with _db.get_db() as conn:
        selected = []
        for fid in fdc_id:
            cached = _db.get_cached_food(conn, fid)
            if cached:
                selected.append((fid, cached["name"]))
    prompt = _claude_fetch.build_prompt(selected) if selected else ""
    return templates.TemplateResponse(request, "claude_fetch.html", {
        "prompt":   prompt,
        "selected": selected,
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
                                         action: str = Form("preview")):
    raw_blocks, curator_text, parse_warnings = _claude_fetch.parse_response(response_text)
    valid, validate_warnings = _claude_fetch.validate_all(raw_blocks)
    warnings = parse_warnings + validate_warnings

    if action == "confirm" and valid:
        with _db.get_db() as conn:
            _claude_fetch.import_foods(conn, valid, curator_text)
        return RedirectResponse("/food/cache?imported=" + str(len(valid)), status_code=303)

    review_rows = []
    for f in valid:
        n = f["nutrients"]
        aa_n = sum(1 for k in _claude_fetch.AA_KEYS if k in n)
        review_rows.append({
            "name":      f["name"],
            "fdc_id":    f["fdc_id"],
            "calories":  int(n.get("calories", 0)),
            "protein_g": round(n.get("protein_g", 0), 1),
            "aa_count":  aa_n,
        })
    return templates.TemplateResponse(request, "claude_import.html", {
        "response_text": response_text,
        "review":        review_rows,
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
async def food_cache_archive(fdc_id: int, q: str = Form(""), sort: str = Form(""),
                              show_archived: int = Form(0)):
    """Archive or restore a cached food — flips whichever state it's currently in."""
    params = {"q": q, "sort": sort, "show_archived": show_archived}
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        if not cached:
            return RedirectResponse(f"/food/cache?{urlencode(params)}", status_code=303)
        newly_archived = not cached["archived"]
        still_used = 0
        if newly_archived:
            refs = _db.food_references(conn, fdc_id)
            still_used = int(bool(refs["pantry"] or refs["recipes"] or refs["meals"]))
        _db.set_food_archived(conn, fdc_id, newly_archived)
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
async def food_cache_db_check_get(request: Request, repaired: int = 0):
    """Scan for referential-integrity problems (see db.check_db_integrity)."""
    with _db.get_db() as conn:
        issues = _db.check_db_integrity(conn)
    total = sum(len(v) for v in issues.values())
    return templates.TemplateResponse(request, "food_cache_db_check.html", {
        "issues": issues,
        "total": total,
        "repairable": total - len(issues["bad_json"]),
        "repaired": repaired,
    })


@app.post("/food/cache/db-check/repair", response_class=RedirectResponse)
async def food_cache_db_check_repair(category: str = Form(default="")):
    """category: one of db.REPAIRABLE_ISSUE_CATEGORIES to fix just that kind
    of problem, or "" (the "Remove all" button) to fix every repairable kind
    at once."""
    categories = {category} if category else None
    with _db.get_db() as conn:
        counts = _db.repair_db_integrity(conn, categories=categories)
    return RedirectResponse(f"/food/cache/db-check?repaired={sum(counts.values())}", status_code=303)


@app.get("/food/cache/{fdc_id}/portions", response_class=HTMLResponse)
async def food_cache_portions_get(request: Request, fdc_id: int):
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
                "has_aa":        _usda.has_amino_acid_data(nuts),
                "gi":            ann["gi_estimate"] if ann else None,
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
            has_aa = _usda.has_amino_acid_data(nuts)
            ann = annotations.get(r["fdc_id"])
            diaas_saved = ann["diaas_estimate"] if ann else None
            diaas = diaas_saved if diaas_saved is not None else (_usda.get_diaas(r["food_name"]) if has_aa else None)
            item.update({
                "data_type":   cached["data_type"] if cached else "",
                "has_aa":      has_aa,
                "gi":          ann["gi_estimate"] if ann else None,
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
                "aa":        "✓" if _usda.has_amino_acid_data(nuts) else "✗",
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
):
    food_name = food_name.strip()
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
    if fdc_id_int is not None and _gi_prompt_needed(fdc_id_int):
        from urllib.parse import quote
        return RedirectResponse(
            f"/food/annotate/{fdc_id_int}?next={quote('/pantry?' + result_flag)}", status_code=303
        )
    return RedirectResponse(f"/pantry?{result_flag}", status_code=303)


@app.post("/pantry/remove/{pantry_id}", response_class=RedirectResponse)
async def pantry_remove(pantry_id: int):
    with _db.get_db() as conn:
        _db.pantry_remove(conn, pantry_id)
    return RedirectResponse("/pantry", status_code=303)


@app.post("/pantry/{pantry_id}/archive", response_class=RedirectResponse)
async def pantry_archive(pantry_id: int):
    """Archive or restore a pantry entry — flips whichever state it's currently in."""
    with _db.get_db() as conn:
        row = _db.pantry_get(conn, pantry_id)
        if not row:
            return RedirectResponse("/pantry", status_code=303)
        newly_archived = not row["archived"]
        _db.set_pantry_archived(conn, pantry_id, newly_archived)
    flag = "archived=1" if newly_archived else "restored=1"
    return RedirectResponse(f"/pantry?{flag}", status_code=303)


@app.get("/food/custom-profiles", response_class=HTMLResponse)
async def food_custom_profiles_get(request: Request, copy_q: str = Query(default=""),
                                    delete_blocked: int = 0):
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
            return RedirectResponse("/food/custom-profiles?delete_blocked=1", status_code=303)
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
            r["has_aa"] = _usda.has_amino_acid_data(n)
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
        "nutrient_source_q": nutrient_source_q.strip(),
        "nutrient_source_results": nutrient_source_results,
        "nutrients_applied": nutrients_applied,
        "nutrient_source": nutrient_source,
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
        source = _db.get_cached_food(conn, source_fdc_id)

    if not source:
        try:
            detail = _fetch_uncached_food_detail(source_fdc_id, off_code)
        except Exception:
            return RedirectResponse(
                f"/food/custom-profiles/{fdc_id}/edit?aa_applied=source_fetch_failed", status_code=303
            )
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
            source = _db.get_cached_food(conn, source_fdc_id)

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


@app.post("/food/custom-profiles/{fdc_id}/copy-nutrients", response_class=RedirectResponse)
async def food_custom_profiles_copy_nutrients(fdc_id: int, source_fdc_id: int = Form(...), off_code: str = Form("")):
    """Overwrite this food's entire nutrient profile with a raw (unscaled) copy
    of a source food's per-100g values — a quick way to seed a blank draft
    before hand-editing. Independent of copy-aa: either can overwrite the
    other's fields, since this replaces the whole nutrients dict wholesale."""
    with _db.get_db() as conn:
        target = _db.get_cached_food(conn, fdc_id)
        if not target:
            return RedirectResponse("/food/custom-profiles", status_code=303)
        source = _db.get_cached_food(conn, source_fdc_id)

    if not source:
        try:
            detail = _fetch_uncached_food_detail(source_fdc_id, off_code)
        except Exception:
            return RedirectResponse(
                f"/food/custom-profiles/{fdc_id}/edit?nutrients_applied=source_fetch_failed", status_code=303
            )
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
            source = _db.get_cached_food(conn, source_fdc_id)

    source_nutrients = json.loads(source["nutrients_json"]) if source["nutrients_json"] else {}
    if not source_nutrients:
        return RedirectResponse(
            f"/food/custom-profiles/{fdc_id}/edit?nutrients_applied=error", status_code=303
        )

    portions_json = target["portions_json"]
    portions: list[dict] = json.loads(portions_json) if portions_json and portions_json != "null" else []
    note = _aa_estimate.copy_nutrients_note(source["name"], source_fdc_id)
    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id, target["name"], dict(source_nutrients),
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


@app.post("/food/custom-profiles/copy/{fdc_id}", response_class=RedirectResponse)
async def food_custom_profiles_copy(fdc_id: int):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        if not cached:
            return RedirectResponse("/food/custom-profiles", status_code=303)
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
    return RedirectResponse(f"/food/custom-profiles/{new_id}/edit", status_code=303)


def _gi_prompt_needed(fdc_id: int) -> bool:
    """True if this food has no GI estimate and prompts for it aren't suppressed."""
    with _db.get_db() as conn:
        ann = _db.get_food_annotation(conn, fdc_id)
    if ann is None:
        return True
    return ann["gi_estimate"] is None and not ann["gi_no_prompt"]


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
    return templates.TemplateResponse(request, "food_annotate.html", {
        "editing":   True,
        "fdc_id":    fdc_id,
        "food_name": food_name,
        "annotation": dict(ann) if ann else None,
        "saved":     bool(saved),
        "next":      next,
    })


@app.post("/food/annotate/{fdc_id}", response_class=RedirectResponse)
async def food_annotate_edit_post(
    fdc_id: int,
    gi_estimate:     str = Form(""),
    diaas_estimate:  str = Form(""),
    prep_context:    str = Form(""),
    gi_no_prompt:    str = Form(""),
    diaas_no_prompt: str = Form(""),
    next:            str = Form(""),
):
    gi   = float(gi_estimate)    if gi_estimate.strip()    else None
    dias = float(diaas_estimate) if diaas_estimate.strip() else None
    prep = prep_context.strip() or None
    with _db.get_db() as conn:
        _db.set_food_annotation(
            conn, fdc_id,
            gi_estimate=gi,
            gi_no_prompt=bool(gi_no_prompt),
            diaas_estimate=dias,
            diaas_no_prompt=bool(diaas_no_prompt),
            prep_context=prep,
        )
    if next:
        return RedirectResponse(next, status_code=303)
    return RedirectResponse(f"/food/annotate/{fdc_id}?saved=1", status_code=303)


@app.post("/food/annotate/{fdc_id}/skip-forever", response_class=RedirectResponse)
async def food_annotate_skip_forever(fdc_id: int, next: str = Form("")):
    """Suppress future GI prompts for this food without touching any other annotation field."""
    with _db.get_db() as conn:
        _db.upsert_food_annotation(conn, fdc_id, gi_no_prompt=1)
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

    oxalate = _oxalate_info(food["fdc_id"], food["name"])
    oxalate_mg_portion: float | None = None
    if oxalate and amount and oxalate.get("mg_per_100g") is not None:
        oxalate_mg_portion = round(oxalate["mg_per_100g"] * amount / 100.0, 1)

    return {
        "food":               food,
        "amount":             amount,
        "portion_str":        portion_str.strip(),
        "portion_label":      portion_label,
        "portion_error":      portion_error,
        "portion_density_hint": portion_density_hint,
        "portions":           portions,
        "nutrient_sections":  _nutrient_sections(display_nutrients, rda_scaled or rda,
                                                 optimal=optimal_scaled or optimal, max_limits=max_limits),
        "protein":            _protein_section(food["name"], display_nutrients),
        "complements":        _food_complement_section(food["name"], display_nutrients, exclude_names=_effective_ignored(ignore_complements, unignore), comp_sort=comp_sort, diaas_sort=diaas_sort),
        "ignored_complements": sorted(_effective_ignored(ignore_complements, unignore)),
        "antinutrients":      antinutrient_flags,
        "has_profile":        rda is not None,
        "has_optimal":        bool(optimal),
        "has_ul":             bool(max_limits),
        "suggest_foundation": suggest_foundation,
        "oxalate":            oxalate,
        "oxalate_mg_portion": oxalate_mg_portion,
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
):
    comp_sort = _resolve_sort(comp_sort, "sort_complements", "effect", _COMPLEMENT_SORT_MODES)
    diaas_sort = _resolve_sort(diaas_sort, "sort_diaas_improvers", "effect", _COMPLEMENT_SORT_MODES)
    ctx = _food_detail_context(fdc_id, amount, portion_str, ignore_complements, unignore,
                                comp_sort=comp_sort, diaas_sort=diaas_sort)
    if "error" in ctx:
        return templates.TemplateResponse(request, "search.html", {
            "results": [], "query": "", "error": ctx["error"],
        })
    return templates.TemplateResponse(request, "food_detail.html", ctx)


def _food_available_sections(ctx: dict) -> list[str]:
    available = []
    if ctx.get("nutrient_sections"):
        available.append("nutrient_table")
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
):
    ctx = _food_detail_context(fdc_id, amount, portion_str, [], [])
    if "error" in ctx:
        return templates.TemplateResponse(request, "search.html", {
            "results": [], "query": "", "error": ctx["error"],
        })

    available = _food_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("food", available, sections, sections_submitted, prefs)
    if sections_submitted:
        _save_prefs_file(_print_sections.save_sections("food", enabled, prefs))

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
    intake = diaas_dcp_g if diaas_dcp_g else nutrients.get("protein_g", 0.0)
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


_COMPLEMENT_SORT_MODES = {"effect", "grams"}


def _complement_suggestions(
    aa_nutrients: dict,
    pooled_tid: float | None,
    context: str = "meal",
    exclude_recipe_id: int | None = None,
    ingredients: list[dict] | None = None,
    exclude_names: set[str] | None = None,
    comp_sort: str | None = None,
    diaas_sort: str | None = None,
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
    comp_sort = comp_sort or _resolve_sort(None, "sort_complements", "effect", _COMPLEMENT_SORT_MODES)
    diaas_sort = diaas_sort or _resolve_sort(None, "sort_diaas_improvers", "effect", _COMPLEMENT_SORT_MODES)
    return _complements.build_complement_display(
        aa_nutrients, pantry, diet_pref=diet_pref,
        digestibility=digestibility, max_improver_grams=max_improver_grams,
        ingredients=ingredients,
        cache_candidates=cache_candidates,
        exclude_names=exclude_names,
        comp_sort=comp_sort,
        diaas_sort=diaas_sort,
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
                "notes":          row["notes"] or "",
                "has_nuts":       bool(per_serving),
                "recipe_deleted": recipe is None,
            })

    return items, total_nutrients, ingredients


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

    # Extra user-chosen nutrient columns (stored in prefs.json).
    from numa_app.services.meal_list_columns import (
        sanitize as _sanitize_meal_nutrients, label_for as _meal_label_for, format_value as _meal_format_value,
    )
    nutrient_keys = _sanitize_meal_nutrients(_load_prefs_file().get("meal_list_nutrients", []))
    meal_nutrient_cols = [{"key": k, "label": _meal_label_for(k)} for k in nutrient_keys]
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
    """Fetch AA nutrient data from USDA for all foods in this meal that lack it."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
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
        if _usda.has_amino_acid_data(nutrients):
            continue
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception:
            continue
        if not _usda.has_amino_acid_data(detail.get("nutrients", {})):
            continue
        with _db.get_db() as conn:
            _db.cache_food(conn, detail["fdcId"], detail["name"], detail["dataType"],
                           detail.get("brand"), detail.get("servingSize"),
                           detail.get("servingUnit"), detail.get("nutrients", {}),
                           detail.get("portions"))
            _recipe_dcp.cascade_food_change(detail["fdcId"], conn)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


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
    for r in matching_recipes:
        search_results.append({
            "_type":         "recipe",
            "recipe_id":     r["id"],
            "name":          r["name"],
            "servings":      float(r["servings"] or 1),
            "total_weight":  r["total_weight"],
            "total_weight_unit": r["total_weight_unit"] or "g",
            "total_volume":  r["total_volume"],
            "total_volume_unit": r["total_volume_unit"] or "ml",
            "data_type":     "Recipe",
            "source":        "recipe",
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
            return "✓" if _usda.has_amino_acid_data(json.loads(nuts_json)) else "✗"
        if data_type in ("Foundation", "SR Legacy"):
            return "~✓"
        return "✗"

    def _ann_gi(fdc_id: int) -> str:
        ann = annotations.get(fdc_id)
        if ann and ann["gi_estimate"] is not None:
            return str(int(round(ann["gi_estimate"])))
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
                     rank: str | None = None, top_n: str | None = None):
    sort = _resolve_sort(sort, "sort_food_search", "relevance", _SEARCH_SORT_MODES)
    item_sort = _resolve_sort(item_sort, "sort_meal_items", "alpha", {"alpha", "entry"})
    source = _resolve_source_filter(source, "sort_food_search_source")
    limit = _resolve_result_limit(limit)
    comp_sort = _resolve_sort(comp_sort, "sort_complements", "effect", _COMPLEMENT_SORT_MODES)
    diaas_sort = _resolve_sort(diaas_sort, "sort_diaas_improvers", "effect", _COMPLEMENT_SORT_MODES)
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
        "meal":                dict(meal),
        "items":               items,
        "item_sort":           item_sort,
        "nutrient_sections":   _nutrient_sections(total_nutrients, rda, daily_nutrients,
                                                  optimal=optimal, max_limits=max_limits) if total_nutrients else [],
        "diaas":               diaas_display,
        "protein_adequacy":    _protein_adequacy(total_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":         _complement_suggestions(aa_nutrients, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="meal", ingredients=meal_ingredients, exclude_names=_effective_ignored(ignore_complements, unignore), comp_sort=comp_sort, diaas_sort=diaas_sort),
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
        "nutrient_sections":  _nutrient_sections(total_nutrients, rda, optimal=optimal, max_limits=max_limits) if total_nutrients else [],
        "diaas":              diaas_display,
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
):
    ctx = _meal_print_context(meal_id)
    if ctx is None:
        return RedirectResponse("/meals", status_code=303)

    available = _meal_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("meal", available, sections, sections_submitted, prefs)
    if sections_submitted:
        _save_prefs_file(_print_sections.save_sections("meal", enabled, prefs))

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

    def _redirect(error: str | None = None) -> RedirectResponse:
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
    grams, error_msg = _parse_portion_str(raw, portions, name)
    if not grams:
        return _redirect(error=error_msg)
    with _db.get_db() as conn:
        _db.meal_add_food(conn, meal_id, fdc_id, name, grams, "g")
    if _gi_prompt_needed(fdc_id):
        # next= carries an explicit empty q= (not simply omitted) so that,
        # once the annotate flow redirects back to the meal page, the
        # persist-search JS in base.html forgets the saved query instead of
        # restoring the stale search-results panel.
        return RedirectResponse(
            f"/food/annotate/{fdc_id}?next={quote(f'/meal/{meal_id}?q=')}", status_code=303
        )
    return _redirect()


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
        with _db.get_db() as conn:
            ings = _db.recipe_get_ingredients(conn, recipe_id)
        with _db.get_db() as conn:
            for ing in ings:
                if ing["ref_recipe_deleted"]:
                    continue
                if ing["ref_recipe_id"]:
                    scaled_srv = (ing["amount"] or 1) * scale
                    sub_unit = f"{scaled_srv:g} serving" + ("s" if scaled_srv != 1 else "")
                    _db.meal_add_recipe(conn, meal_id, ing["ref_recipe_id"],
                                        ing["food_name"], scaled_srv, unit=sub_unit)
                else:
                    scaled_g = (ing["amount"] or 0) * scale
                    _db.meal_add_food(conn, meal_id, ing["fdc_id"],
                                      ing["food_name"], scaled_g, f"{scaled_g:.4g} g")
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
    else:
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, item["fdc_id"]) if item["fdc_id"] else None
        portions = (json.loads(cached["portions_json"] or "[]") or []) if cached else []
        grams, error_msg = _parse_portion_str(amount.strip(), portions, item["food_name"])
        if grams is not None:
            with _db.get_db() as conn:
                _db.meal_replace_food(conn, item_id, meal_id, item["fdc_id"],
                                      item["food_name"], grams, "g", notes_val)
        else:
            return _redirect(error=error_msg)
    return _redirect()


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
                                                optimal=optimal, max_limits=max_limits) if combined_nutrients else [],
        "diaas":             diaas_display,
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
):
    ctx = _meal_day_context(meal_id)
    if ctx is None:
        return RedirectResponse("/meals", status_code=303)

    available = _day_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("day", available, sections, sections_submitted, prefs)
    if sections_submitted:
        _save_prefs_file(_print_sections.save_sections("day", enabled, prefs))

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
        "day_meals":          ctx["meals"],
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
async def settings_get(request: Request, saved: str = "", recompute_retry: str = ""):
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

    from numa_app.services.meal_list_columns import AVAILABLE_NUTRIENTS, MAX_MEAL_LIST_NUTRIENTS
    saved_meal_nutrients = _load_prefs_file().get("meal_list_nutrients", [])
    meal_list_nutrient_rows = [
        {
            "key": key, "label": label, "unit": unit,
            "position": (saved_meal_nutrients.index(key) + 1) if key in saved_meal_nutrients else None,
        }
        for key, label, unit in AVAILABLE_NUTRIENTS
    ]

    return templates.TemplateResponse(request, "settings.html", {
        "profile":              profile,
        "rda_rows":             rda_rows,
        "activity_labels":      _profile.ACTIVITY_LABELS,
        "sex_values":           _profile.SEX_VALUES,
        "saved":                saved,
        "diet_pref":            diet_pref,
        "diet_labels":          _DIET_LABELS,
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
        "starter_status":       starter_status,
        "recompute_errors":     recompute_errors,
        "recompute_retry":      recompute_retry,
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
async def settings_diaas_override_delete(food_name: str = Form(...)):
    with _db.get_db() as conn:
        _diaas.diaas_override_delete(conn, food_name.strip())
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
    return RedirectResponse("/settings?saved=nutrient_target", status_code=303)


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
    return RedirectResponse("/settings?saved=nutrient_target_defaults", status_code=303)


@app.post("/settings/starter-data/load", response_class=RedirectResponse)
async def settings_demo_data_load():
    """Populate a fresh install with starter foods/pantry/recipes to explore
    the app with. See numa_app.services.demo_data for what's inserted and
    why — a marker file lets settings_demo_data_clear() undo exactly this."""
    from numa_app.services import demo_data as _demo_data
    with _db.get_db() as conn:
        _demo_data.load_demo_data(conn)
    return RedirectResponse("/settings?saved=starter_data_loaded", status_code=303)


@app.post("/settings/starter-data/clear", response_class=RedirectResponse)
async def settings_demo_data_clear():
    """Remove exactly the starter foods/pantry/recipes settings_demo_data_load() added."""
    from numa_app.services import demo_data as _demo_data
    with _db.get_db() as conn:
        _demo_data.clear_demo_data(conn)
    return RedirectResponse("/settings?saved=starter_data_cleared", status_code=303)


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
    return RedirectResponse("/settings?saved=starter_data_restored#starter-data", status_code=303)


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
}


@app.get("/recipes", response_class=HTMLResponse)
async def recipes_list(request: Request, q: str = "", sort: str | None = None,
                        show_archived: bool | None = None, archived: int = 0,
                        restored: int = 0, still_used: int = 0,
                        recipes_created: int = 0, recipes_reused: int = 0):
    sort = _resolve_sort(sort, "sort_recipes", "recent", set(_RECIPE_SORT_KEYS))
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


# Recipe comparison
# ---------------------------------------------------------------------------

_MAX_COMPARE_RECIPES = 6


def _parse_recipe_compare_ids(ids_str: str) -> list[int]:
    return [int(x) for x in ids_str.split(",") if x.strip()] if ids_str.strip() else []


def _load_recipe_compare_entries(conn, recipe_ids: list[int], unit: str) -> list[dict]:
    """Load recipe data for comparison. unit='serving' scales nutrients to one
    serving of each recipe — the fair basis for comparing recipes with
    different batch sizes; unit='batch' uses the whole recipe as authored."""
    entries = []
    for rid in recipe_ids:
        recipe = _db.recipe_get(conn, rid)
        if not recipe:
            continue
        servings = float(recipe["servings"] or 1)
        per_serving = _recipe_nutrients_per_serving(rid, conn)
        nutrients = per_serving if unit == "serving" else {k: v * servings for k, v in per_serving.items()}
        ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, rid)]

        target_servings = 1.0 if unit == "serving" else servings
        diaas_display = None
        diaas_ingredients = _flatten_recipe_diaas_ingredients(rid, conn, target_servings)
        if diaas_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(diaas_ingredients, conn)
            except Exception:
                diaas_result = None
            diaas_display = _build_diaas_display(diaas_result)

        entries.append({
            "id":          rid,
            "name":        recipe["name"],
            "servings":    servings,
            "nutrients":   nutrients,
            "ingredients": ingredients,
            "diaas":       diaas_display,
        })
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


_GRAM_NUM_RE = re.compile(r'(\d+(?:\.\d+)?)(\s*gr?\b)')


def _round_grams_in_label(label: str) -> str:
    """Round any gram figure in a display label to a whole number — fractional
    grams aren't meaningful at cooking precision, and this table is a quick
    side-by-side scan, not a place for hundredths-of-a-gram accuracy."""
    return _GRAM_NUM_RE.sub(lambda m: f"{round(float(m.group(1)))}{m.group(2)}", label)


def _build_recipe_ingredient_rows(entries: list[dict]) -> list[dict]:
    """Union of ingredient names across the given recipe entries into one row
    per distinct ingredient, one cell per recipe holding its amount/unit (or
    None if that recipe doesn't use it). Ingredients shared by 2+ recipes are
    listed first — that's the interesting case for spotting why recipes
    differ — then recipe-unique ingredients, both alphabetized."""
    rows_by_name: dict[str, dict] = {}
    for i, entry in enumerate(entries):
        for ing in entry["ingredients"]:
            row = rows_by_name.setdefault(ing["food_name"], {
                "name":      ing["food_name"],
                "is_recipe": bool(ing["ref_recipe_id"]),
                "cells":     [None] * len(entries),
            })
            display = _ing_amount_display(ing["unit"], ing["amount"], ing["food_name"])
            row["cells"][i] = {"display": _round_grams_in_label(display)}
    rows = list(rows_by_name.values())
    for row in rows:
        row["shared_count"] = sum(1 for c in row["cells"] if c is not None)
    rows.sort(key=lambda r: (-r["shared_count"], r["name"].lower()))
    return rows


@app.get("/recipe/compare", response_class=HTMLResponse)
async def recipe_compare_get(
    request: Request,
    ids:     str = "",
    search:  str = "",
    unit:    str = "serving",
    error:   str = "",
):
    unit = unit if unit in ("serving", "batch") else "serving"
    id_list = _parse_recipe_compare_ids(ids)
    search = search.strip()
    search_results: list[dict] = []
    with _db.get_db() as conn:
        entries = _load_recipe_compare_entries(conn, id_list, unit)
        if search:
            words = search.lower().split()
            seen = set(id_list)
            for r in _db.recipe_list_recent(conn, limit=200):
                if r["id"] in seen:
                    continue
                if any(w in r["name"].lower() for w in words):
                    search_results.append(dict(r))

    ingredient_rows = _build_recipe_ingredient_rows(entries) if len(entries) >= 2 else []
    compare_groups = _build_compare_groups(entries) if len(entries) >= 2 else []
    protein_quality_rows = _build_protein_quality_rows(entries) if len(entries) >= 2 else []
    ids_str = ",".join(str(e["id"]) for e in entries)

    return templates.TemplateResponse(request, "recipe_compare.html", {
        "entries":              entries,
        "ingredient_rows":      ingredient_rows,
        "compare_groups":       compare_groups,
        "protein_quality_rows": protein_quality_rows,
        "ids_str":              ids_str,
        "search":               search,
        "search_results":       search_results,
        "unit":                 unit,
        "error":                error,
        "max_recipes":          _MAX_COMPARE_RECIPES,
    })


@app.post("/recipe/compare/add", response_class=RedirectResponse)
async def recipe_compare_add(
    recipe_id: int = Form(...),
    ids:       str = Form(""),
    unit:      str = Form("serving"),
):
    id_list = _parse_recipe_compare_ids(ids)
    if len(id_list) >= _MAX_COMPARE_RECIPES:
        ids_str = ",".join(str(i) for i in id_list)
        return RedirectResponse(
            f"/recipe/compare?ids={ids_str}&unit={unit}"
            f"&error=Maximum+{_MAX_COMPARE_RECIPES}+recipes+allowed",
            status_code=303,
        )
    if recipe_id not in id_list:
        id_list.append(recipe_id)
    ids_str = ",".join(str(i) for i in id_list)
    return RedirectResponse(f"/recipe/compare?ids={ids_str}&unit={unit}", status_code=303)


@app.post("/recipe/compare/add-multiple", response_class=RedirectResponse)
async def recipe_compare_add_multiple(request: Request, ids: str = Form(""), unit: str = Form("serving")):
    """Bulk-add checked recipes to the comparison — used both by Compare
    Recipes' own "add via search" panel and by the compare checkboxes on
    Foods search and the Recipes list (which post straight here)."""
    form = await request.form()
    recipe_id_strs = form.getlist("recipe_id")
    id_list = _parse_recipe_compare_ids(ids)
    added = skipped = 0
    for rid_str in recipe_id_strs:
        try:
            rid = int(rid_str)
        except (ValueError, TypeError):
            continue
        if rid in id_list:
            continue
        if len(id_list) >= _MAX_COMPARE_RECIPES:
            skipped += 1
            continue
        id_list.append(rid)
        added += 1
    ids_str = ",".join(str(i) for i in id_list)
    url = f"/recipe/compare?ids={ids_str}&unit={unit}"
    if skipped:
        url += f"&error=Added+{added}%2C+skipped+{skipped}+%E2%80%94+maximum+{_MAX_COMPARE_RECIPES}+recipes"
    return RedirectResponse(url, status_code=303)


@app.post("/recipe/compare/remove", response_class=RedirectResponse)
async def recipe_compare_remove(
    remove_id: int = Form(...),
    ids:       str = Form(""),
    unit:      str = Form("serving"),
):
    id_list = [i for i in _parse_recipe_compare_ids(ids) if i != remove_id]
    ids_str = ",".join(str(i) for i in id_list)
    return RedirectResponse(f"/recipe/compare?ids={ids_str}&unit={unit}", status_code=303)


def _recipe_detail_context(recipe_id: int, servings: float | None,
                            ignore_complements: list[str], unignore: list[str],
                            comp_sort: str | None = None, diaas_sort: str | None = None,
                            rank: str | None = None, top_n: str | None = None) -> dict | None:
    top_n = _resolve_contributor_top_n(top_n)
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return None
        _db.recipe_touch(conn, recipe_id)
        ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, recipe_id)]
        for _ing in ingredients:
            if not _ing["ref_recipe_id"] and _ing["amount"]:
                _ing["volume_display"] = volume_hint(_ing["amount"], _ing["food_name"])
        referencing_recipes = _db.recipe_referencing_subrecipe(conn, recipe_id)
        per_serving = _recipe_nutrients_per_serving(recipe_id, conn)
        recipe_servings = float(recipe["servings"] or 1)
        if servings is None:
            servings = 1.0

        diaas_ingredients = _flatten_recipe_diaas_ingredients(recipe_id, conn, servings)

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
        "nutrient_sections":        _nutrient_sections(scaled, rda, optimal=optimal, max_limits=max_limits) if scaled else [],
        "diaas":                    diaas_display,
        "protein_adequacy":         _protein_adequacy(scaled, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":              _complement_suggestions(recipe_total_nutrients, _diaas.pooled_tid(diaas_result) if diaas_result else None, context="recipe", exclude_recipe_id=recipe_id, ingredients=full_diaas_ingredients, exclude_names=_effective_ignored(ignore_complements, unignore), comp_sort=comp_sort, diaas_sort=diaas_sort),
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
                         rank: str | None = None, top_n: str | None = None):
    comp_sort = _resolve_sort(comp_sort, "sort_complements", "effect", _COMPLEMENT_SORT_MODES)
    diaas_sort = _resolve_sort(diaas_sort, "sort_diaas_improvers", "effect", _COMPLEMENT_SORT_MODES)
    ctx = _recipe_detail_context(recipe_id, servings, ignore_complements, unignore,
                                  comp_sort=comp_sort, diaas_sort=diaas_sort, rank=rank, top_n=top_n)
    if ctx is None:
        return RedirectResponse("/recipes", status_code=303)
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
    return available


@app.get("/recipe/{recipe_id}/print", response_class=HTMLResponse)
async def recipe_print(
    request: Request,
    recipe_id: int,
    servings: float | None = None,
    sections: list[str] = Query(default=[]),
    sections_submitted: bool = Query(default=False),
):
    ctx = _recipe_detail_context(recipe_id, servings, [], [])
    if ctx is None:
        return RedirectResponse("/recipes", status_code=303)

    available = _recipe_available_sections(ctx)
    prefs = _load_prefs_file()
    enabled = _print_sections.resolve_sections("recipe", available, sections, sections_submitted, prefs)
    if sections_submitted:
        _save_prefs_file(_print_sections.save_sections("recipe", enabled, prefs))

    return templates.TemplateResponse(request, "print.html", {
        "title":              ctx["recipe"]["name"],
        "subtitle":           f"{ctx['servings']} serving{'s' if ctx['servings'] != 1 else ''} analyzed"
                              f"{' · ' + str(ctx['recipe']['servings']) + ' servings per recipe' if ctx['recipe'].get('servings') else ''}",
        "back_url":           f"/recipe/{recipe_id}",
        "back_label":         "Back to recipe",
        "fixed_params":       {"servings": ctx["servings"]},
        "section_labels":     _print_sections.PRINT_SECTION_LABELS,
        "available_sections": available,
        "enabled":            enabled,
        "portion_label":      f"{ctx['servings']} serving{'s' if ctx['servings'] != 1 else ''}",
        "oxalate_agg":        ctx["oxalate"],
        **{k: v for k, v in ctx.items() if k != "oxalate"},
    })


@app.get("/recipe/{recipe_id}/edit", response_class=HTMLResponse)
async def recipe_edit_get(request: Request, recipe_id: int, q: str = "", saved: str = "", error: str = "",
                           relinked: str = "", source: list[str] | None = Query(default=None),
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
        ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, recipe_id)]
        for _ing in ingredients:
            if not _ing["ref_recipe_id"]:
                _ing["amount_display"] = _ing_amount_display(_ing["unit"], _ing["amount"], _ing["food_name"])

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
        for r in matching_recipes:
            search_results.append({
                "_type":     "recipe",
                "recipe_id": r["id"],
                "name":      r["name"],
                "servings":  float(r["servings"] or 1),
                "data_type": "Recipe",
                "source":    "recipe",
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
                "aa":        "✓" if _usda.has_amino_acid_data(nutrients) else "✗",
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
        "recipe":             dict(recipe),
        "ingredients":        ingredients,
        "q":                  q,
        "show_add_section":   show_add_section,
        "search_results":     search_results,
        "saved":              saved,
        "error":              error,
        "nutrition_summary":  nutrition_summary,
        "broken_groups":      broken_groups,
        "relinked":           relinked,
        "source":             source,
        "limit":              limit,
        "source_filters":     _SEARCH_SOURCE_FILTERS,
        "source_labels":      _SEARCH_SOURCE_LABELS,
    })


@app.post("/recipe/{recipe_id}/relink", response_class=RedirectResponse)
async def recipe_relink_post(recipe_id: int, matched_name: str = Form(...)):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        m, r = _db.relink_recipe_refs(conn, matched_name, recipe_id)
    return RedirectResponse(f"/recipe/{recipe_id}/edit?relinked={m},{r}", status_code=303)


@app.post("/recipe/{recipe_id}/edit", response_class=RedirectResponse)
async def recipe_edit_post(
    recipe_id: int,
    name: str = Form(...),
    description: str = Form(""),
    servings: float = Form(1),
    total_weight: str = Form(""),
    total_weight_unit: str = Form("g"),
    instructions: str = Form(""),
    complete: str = Form(""),
):
    tw = float(total_weight) if total_weight.strip() else None
    with _db.get_db() as conn:
        existing = _db.recipe_get(conn, recipe_id)
        _db.recipe_update(
            conn, recipe_id,
            name=name.strip(), description=description.strip(),
            servings=max(1.0, servings), instructions=instructions.strip(),
            total_weight=tw, total_weight_unit=total_weight_unit if tw else None,
            complete=bool(complete),
            introduction=existing["introduction"] if existing else None,
        )
        _recipe_dcp.recompute_recipe_dcp(recipe_id, conn)
    return RedirectResponse(f"/recipe/{recipe_id}/edit?saved=1", status_code=303)


@app.post("/recipe/{recipe_id}/delete", response_class=RedirectResponse)
async def recipe_delete_post(recipe_id: int):
    with _db.get_db() as conn:
        _db.recipe_delete(conn, recipe_id)
    return RedirectResponse("/recipes", status_code=303)


@app.post("/recipe/{recipe_id}/archive", response_class=RedirectResponse)
async def recipe_archive(recipe_id: int):
    """Archive or restore a recipe — flips whichever state it's currently in."""
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        newly_archived = not recipe["archived"]
        still_used = 0
        if newly_archived:
            referencing = _db.recipe_referencing_subrecipe(conn, recipe_id)
            refs = _db.recipe_references(conn, recipe_id)
            still_used = int(bool(referencing or refs["meals"]))
        _db.set_recipe_archived(conn, recipe_id, newly_archived)
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
    # Successful add: explicit empty q= (not simply omitted) tells the
    # persist-search JS in base.html to forget the saved query instead of
    # restoring it from sessionStorage — otherwise the search panel would
    # reappear right after the add.
    return RedirectResponse(f"/recipe/{recipe_id}/edit?q=", status_code=303)


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
            complete=bool(recipe["complete"]),
            introduction=recipe["introduction"],
        )
    return RedirectResponse(f"/recipe/{recipe_id}#sec-procedure", status_code=303)


@app.post("/recipe/{recipe_id}/introduction", response_class=RedirectResponse)
async def recipe_introduction_post(recipe_id: int, introduction: str = Form("")):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        _db.recipe_update(
            conn, recipe_id,
            name=recipe["name"], description=recipe["description"] or "",
            servings=recipe["servings"], instructions=recipe["instructions"] or "",
            total_weight=recipe["total_weight"],
            total_weight_unit=recipe["total_weight_unit"],
            complete=bool(recipe["complete"]),
            introduction=introduction.strip(),
        )
    return RedirectResponse(f"/recipe/{recipe_id}/edit#sec-introduction", status_code=303)


@app.get("/summary/trend", response_class=HTMLResponse)
async def summary_trend(request: Request, days: int = Query(7)):
    """Multiday average nutrient intake vs. RDA — surfaces chronic shortfalls
    (B12, iron, iodine, vitamin D, ...) a single day's snapshot can't."""
    if days not in (7, 14, 30):
        days = 7

    end = datetime.date.today()
    start = end - datetime.timedelta(days=days - 1)

    with _db.get_db() as conn:
        meals = _db.meal_list_by_date_range(conn, start.isoformat(), end.isoformat())
        daily_totals: dict[str, dict[str, float]] = {}
        all_ingredients: list = []
        day_dcp: dict[str, float] = {}
        for meal in meals:
            _, nutrients, ingredients = _meal_expand_for_diaas(meal["id"], conn)
            if nutrients:
                day = daily_totals.setdefault(meal["meal_date"], {})
                for key, val in nutrients.items():
                    day[key] = day.get(key, 0.0) + val
            all_ingredients.extend(ingredients)
            if meal["bcp_g"] is not None:
                day_dcp[meal["meal_date"]] = day_dcp.get(meal["meal_date"], 0.0) + meal["bcp_g"]

    avg_nutrients, num_days = average_from_daily_totals(daily_totals)

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

    # Pool amino acids across the whole window (not averaged — pooling totals
    # first and averaging per-day both produce identical gap ratios here,
    # since get_aa_gaps() only compares AA-to-protein ratios, so pooling is
    # simpler and avoids an extra averaging pass).
    aa_nutrients: dict = {}
    for ing in all_ingredients:
        if _usda.has_amino_acid_data(ing["nutrients_100g"]):
            scaled = _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
            for k, v in scaled.items():
                aa_nutrients[k] = aa_nutrients.get(k, 0.0) + v

    trend_pooled_tid: float | None = None
    if all_ingredients:
        with _db.get_db() as conn:
            trend_diaas_result = _diaas.meal_level_diaas(all_ingredients, conn)
        trend_pooled_tid = _diaas.pooled_tid(trend_diaas_result)

    return templates.TemplateResponse(request, "trend.html", {
        "days":              days,
        "start":             start.isoformat(),
        "end":               end.isoformat(),
        "num_days":          num_days,
        "nutrient_sections": _nutrient_sections(avg_nutrients, rda, avg_nutrients,
                                                optimal=optimal, max_limits=max_limits) if num_days else [],
        "has_profile":       rda is not None,
        "has_optimal":       bool(optimal),
        "has_ul":             bool(max_limits),
        "diet_notes":        _diet_aware_daily_notes(avg_nutrients, rda) if num_days else {},
        "complements":       _complement_suggestions(aa_nutrients, trend_pooled_tid, context="daily",
                                                      ingredients=all_ingredients) if aa_nutrients else None,
        "end_profile_name":  end_profile_row["profile_name"] if end_profile_row else None,
        "differing_profile_dates": differing_dates,
        "avg_dcp":           avg_dcp,
        "avg_dcp_pct":       avg_dcp_pct,
        "avg_dcp_days":      len(day_dcp),
        "protein_target":    protein_target,
    })


def _nutrient_plot_params(conn, nutrients: list[str], days_back: str | None, anchor_date: str | None):
    """Shared by the plot page and its image endpoint: validate the chosen
    nutrient keys (capped to the plotting palette's 8 colors) and resolve
    which logged dates fall in range. days_back blank/absent/<=0 means "all
    logged days"; otherwise it's the N days ending at anchor_date (default:
    the most recent logged day). days_back arrives as a string (not int)
    because the "blank = all days" form field submits "" when empty, which
    FastAPI's query validation rejects outright for an int-typed param."""
    valid_keys = {key for key, _label, _unit in _usda.NUTRIENT_MAP.values()} | {_DCP_PLOT_KEY}
    chosen = [k for k in nutrients if k in valid_keys][:MAX_PLOT_NUTRIENTS]

    all_dates = sorted(r["meal_date"] for r in _db.meal_dates_with_bcp(conn, limit=1_000_000))

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
            scaled.append({**s, "y": [v / factor for v in s["y"]],
                            "label": f"{s['label']} ÷{_fmt_plot_factor(factor)}", "scaled": True})
    return scaled


def _default_individual_factors(series: list[dict]) -> dict[str, float]:
    """Step 2, run after step 1's global factor is already applied. A
    single shared factor can still leave one nutrient nearly flat if its
    own variance is far below the chart's most-variable nutrient — dividing
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
            out.append({**s, "y": [v * k for v in s["y"]],
                         "label": f"{s['label']} ×{_fmt_plot_factor(k)}", "scaled": True})
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

    plain_keys = [k for k in chosen if k != _DCP_PLOT_KEY]
    day_values = {d: day_nutrient_values(conn, d, plain_keys) for d in dates} if plain_keys else {}
    dcp_by_date: dict[str, float | None] = {}
    if _DCP_PLOT_KEY in chosen:
        dcp_by_date = {r["meal_date"]: r["day_bcp"] for r in _db.meal_dates_with_bcp(conn, limit=1_000_000)}

    series = []
    for key in chosen:
        y = []
        for d in dates:
            v = dcp_by_date.get(d) if key == _DCP_PLOT_KEY else day_values[d][key]
            y.append(float(v) if v is not None else float("nan"))
        s = {"key": key, "x": dates, "y": y, "label": _plot_label_for(key)}
        if key == highlight_key:
            s["color"] = _HIGHLIGHT_COLOR
            s["highlight"] = True
        series.append(s)
    return series


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
    """Trailing moving average: each point becomes the average of itself
    and up to (window - 1) preceding points, using fewer at the very start
    of the series and skipping gap days (nan) rather than treating them as
    zero. window <= 1 returns the series unchanged. Runs before the scale
    factor steps, so scaling is calibrated to what's actually displayed."""
    if window <= 1:
        return series
    smoothed = []
    for s in series:
        y = s["y"]
        new_y = []
        for i in range(len(y)):
            chunk = [v for v in y[max(0, i - window + 1):i + 1] if not math.isnan(v)]
            new_y.append(sum(chunk) / len(chunk) if chunk else float("nan"))
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
    return units.pop() if len(units) == 1 else _GENERIC_PLOT_YLABEL


def _nutrient_plot_default_title(dates: list[str]) -> str:
    return f"Key nutrients, {dates[0]} to {dates[-1]}" if dates else "Key nutrients"


def _nutrient_plot_qs(chosen: list[str], days_back: str | None, anchor: str | None,
                       scale_factor: str | None, title: str | None,
                       highlight: str | None, grayscale: bool, smoothing: int,
                       nutrient_factors: dict[str, str] | None = None) -> str:
    from urllib.parse import urlencode
    params = [("nutrients", k) for k in chosen]
    if days_back:
        params.append(("days_back", days_back))
        if anchor:
            params.append(("anchor_date", anchor))
    if scale_factor:
        params.append(("scale_factor", scale_factor))
    if title:
        params.append(("title", title))
    if highlight:
        params.append(("highlight", highlight))
    if grayscale:
        params.append(("grayscale", "1"))
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
    smoothing: str | None = Query(None),
):
    """Line plot of one or more Daily Summary nutrients over a chosen set of
    days — reuses the same per-day nutrient totals as the Recent Days table
    and the extra-column picker (numa_app.services.meal_list_columns)."""
    from numa_app.services.meal_list_columns import plot_nutrient_choices

    smoothing_n = _parse_smoothing_window(smoothing)

    with _db.get_db() as conn:
        chosen, dates, anchor = _nutrient_plot_params(conn, nutrients, days_back, anchor_date)
        has_plot = bool(chosen) and bool(dates)
        highlight_key = _resolve_highlight(chosen, highlight) if has_plot else None
        raw_series = _nutrient_plot_raw_series(conn, chosen, dates, highlight_key) if has_plot else []

    raw_series = _apply_smoothing(raw_series, smoothing_n)

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

    effective_title = title.strip() if title and title.strip() else _nutrient_plot_default_title(dates)

    qs = (_nutrient_plot_qs(chosen, days_back, anchor, factor_str, effective_title,
                             highlight_key, grayscale, smoothing_n, individual_factor_strs)
          if has_plot else "")

    available = [(_DCP_PLOT_KEY, _DCP_PLOT_LABEL)] + plot_nutrient_choices()
    nutrient_factor_rows = [{
        "key":         k,
        "label":       _plot_label_for(k),
        "value":       raw_factor_params.get(k, ""),
        "placeholder": _fmt_plot_factor(auto_individual.get(k, 1.0)),
    } for k in chosen]

    return templates.TemplateResponse(request, "nutrient_plot.html", {
        "available_nutrients": [{"key": k, "label": lbl} for k, lbl in available],
        "chosen":     chosen,
        "days_back":  days_back or "",
        "anchor_date": anchor,
        "dates":      dates,
        "has_plot":   has_plot,
        "qs":         qs,
        "max_nutrients": MAX_PLOT_NUTRIENTS,
        "scale_factor": scale_factor if user_factor else "",
        "scale_factor_placeholder": _fmt_plot_factor(default_factor) if default_factor else "auto",
        "nutrient_factor_rows": nutrient_factor_rows,
        "title":      effective_title,
        "highlight":  highlight_key,
        "grayscale":  grayscale,
        "smoothing":  smoothing_n,
    })


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
    smoothing: str | None = Query(None),
    fmt: str = Query("png"),
    download: bool = Query(False),
):
    from numa_app.services.plotting import line_plot_image

    image_format = "svg" if fmt == "svg" else "png"

    with _db.get_db() as conn:
        chosen, dates, _anchor = _nutrient_plot_params(conn, nutrients, days_back, anchor_date)
        if not chosen or not dates:
            raise HTTPException(status_code=404, detail="No nutrients or days selected")
        highlight_key = _resolve_highlight(chosen, highlight)
        raw_series = _nutrient_plot_raw_series(conn, chosen, dates, highlight_key)

    raw_series = _apply_smoothing(raw_series, _parse_smoothing_window(smoothing))

    factor = _parse_plot_factor(scale_factor) or _default_plot_scale_factor(raw_series)
    step1_series = _apply_plot_scale_factor(raw_series, factor)

    raw_factor_params = _nutrient_plot_factor_params(request.query_params, chosen)
    auto_individual = _default_individual_factors(step1_series)
    effective_individual = {
        k: (_parse_plot_factor(raw_factor_params.get(k)) or auto_individual.get(k, 1.0))
        for k in chosen
    }
    series = _apply_individual_factors(step1_series, effective_individual)

    plot_title = title.strip() if title and title.strip() else _nutrient_plot_default_title(dates)
    plot_ylabel = _nutrient_plot_ylabel(chosen, series)

    image_bytes = line_plot_image(series, xlabel="Date", ylabel=plot_ylabel,
                                   title=plot_title, image_format=image_format, grayscale=grayscale,
                                   hide_y_values=(plot_ylabel == _GENERIC_PLOT_YLABEL))
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
    smoothing: str | None = Query(None),
):
    with _db.get_db() as conn:
        chosen, dates, anchor = _nutrient_plot_params(conn, nutrients, days_back, anchor_date)
    if not chosen or not dates:
        return RedirectResponse("/summary/nutrient-plot", status_code=303)

    highlight_key = _resolve_highlight(chosen, highlight)
    raw_factor_params = _nutrient_plot_factor_params(request.query_params, chosen)
    effective_title = title.strip() if title and title.strip() else _nutrient_plot_default_title(dates)
    qs = _nutrient_plot_qs(chosen, days_back, anchor, scale_factor, effective_title,
                            highlight_key, grayscale, _parse_smoothing_window(smoothing), raw_factor_params)

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
    day rather than per meal, plus the mandatory Protein/Calories/Carbs/Fiber
    columns every Recent Days row always shows."""
    from numa_app.services.meal_list_columns import (
        sanitize as _sanitize_meal_nutrients, label_for as _meal_label_for, day_nutrient_values,
        MANDATORY_DAY_COLUMNS, MANDATORY_DAY_KEYS,
    )
    show_profile = len(_profile.list_profiles()) > 1
    # Drop any mandatory key the user separately picked as a Meals & Log
    # column (that picker still allows it) — Recent Days already shows it,
    # via its own fixed column below, so it would otherwise appear twice.
    nutrient_keys = [k for k in _sanitize_meal_nutrients(_load_prefs_file().get("meal_list_nutrients", []))
                     if k not in MANDATORY_DAY_KEYS]
    day_rows = []
    for r in rows:
        d = r["meal_date"]
        bcp = r["day_bcp"]
        profile_name = None
        if show_profile:
            dp = _db.day_profile_get(conn, d)
            profile_name = dp["profile_name"] if dp else None
        goal = _day_profile.protein_target_for_date(conn, d, diet_pref=_current_diet_pref())
        day_rows.append({
            "meal_date":      d,
            "day_bcp":        round(bcp, 1) if bcp is not None else None,
            "goal":           round(goal, 0) if goal else None,
            "pct_goal":       r["day_pct_goal"],
            "profile_name":   profile_name,
            "mandatory_values": day_nutrient_values(conn, d, MANDATORY_DAY_KEYS),
            "nutrient_values": day_nutrient_values(conn, d, nutrient_keys),
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
        "day_rows":          day_rows,
        "mandatory_day_cols": mandatory_day_cols,
        "day_nutrient_cols": day_nutrient_cols,
        "show_profile_col":  len(_profile.list_profiles()) > 1,
        "today":             datetime.date.today().isoformat(),
        "date_detail":       meal_date,
        "meals":             meals,
        "nutrient_sections": _nutrient_sections(combined_nutrients, rda, combined_nutrients,
                                                optimal=optimal, max_limits=max_limits) if combined_nutrients else [],
        "diaas":             diaas_display,
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
):
    """Food use in meals: frequency-of-use table across a chosen set of meals.

    mode selects EITHER date range(s) ("range") OR meal IDs ("ids") — never both.
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
        "id":        lambda e: (e["fdc_id"] is None, e["fdc_id"] or 0),
    }
    rows_sorted = sorted(rows_all, key=sort_keys.get(sort, sort_keys["frequency"]))
    total_days = len({m["meal_date"] for m in meals_by_id.values()})
    result_rows = [{
        "fdc_id":    r["fdc_id"],
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
    })


@app.post("/analysis/food-use/substitute", response_class=RedirectResponse)
async def analysis_food_use_substitute(
    mode: str = Form(...),
    ranges_raw: str = Form(""),
    meal_ids: str = Form(""),
    protein_only: bool = Form(False),
    sort: str = Form("frequency"),
    old_kind: str = Form(...),
    old_id: int = Form(...),
    new_kind: str = Form(...),
    new_id: int = Form(...),
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
):
    """Food use in recipes: frequency-of-use table across a chosen set of
    (container) recipes — how many of them use a given food or sub-recipe as
    an ingredient, directly or nested. mode selects ALL recipes ("all",
    default), a date range by when the recipe was created ("range"), or
    specific recipe IDs ("ids")."""
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
        "id":        lambda e: (e["fdc_id"] is None, e["fdc_id"] or 0),
    }
    rows_sorted = sorted(rows_all, key=sort_keys.get(sort, sort_keys["frequency"]))
    total_recipes = len(recipes_by_id)
    result_rows = [{
        "fdc_id":      r["fdc_id"],
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
    })


@app.post("/analysis/food-use-recipes/substitute", response_class=RedirectResponse)
async def analysis_food_use_recipes_substitute(
    mode: str = Form(...),
    ranges_raw: str = Form(""),
    recipe_ids: str = Form(""),
    protein_only: bool = Form(False),
    sort: str = Form("frequency"),
    old_kind: str = Form(...),
    old_id: int = Form(...),
    new_kind: str = Form(...),
    new_id: int = Form(...),
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
    rebuild_manual_if_stale()
    if not _MANUAL.exists():
        return HTMLResponse("<p>User manual not found. Run <code>make manual</code> to generate it.</p>", status_code=404)
    return HTMLResponse(_MANUAL.read_text(encoding="utf-8"))
