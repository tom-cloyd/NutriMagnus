"""
search.py — food lookup flow: _search_and_pick_food(), result ranking, and cache integration.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/search.py — food lookup flow"
"""
import json
import re
import textwrap
import threading

from rich.table import Table

import db as _db
import usda as _usda
import openfoodfacts as _off
from .. import state
from ..ui.common import _id_cell, ID_KEY, table_title, help_footer
from ..ui.prompts import Cancelled, ReturnToMain, _prompt


def _ask_yes_no_quit(prompt_text: str, *, default: str = "y") -> str:
    while True:
        try:
            ans = _prompt(prompt_text, default=default).strip().lower()
        except Cancelled:
            return "n"
        if ans in ("", "y", "yes"):
            return "y"
        if ans in ("n", "no"):
            return "n"
        if ans == "q":
            return "q"
        state.console.print(f"[{state.T['warning']}]Please enter y, n, or q.[/{state.T['warning']}]")

_BRAND_ADJECTIVES = {
    # Brand qualifiers
    "organic", "pure", "natural", "premium", "select", "extra", "virgin",
    # Processing descriptors
    "ground", "milled", "cold", "pressed", "roasted", "toasted",
    "unrefined", "refined", "dried", "dry", "dehydrated",
    # Form descriptors (these cause poor SR Legacy matches)
    "flakes", "flake", "powder", "granules", "granulated", "seeds", "seed",
    "whole", "fresh", "raw",
    # Taste/seasoning
    "unsweetened", "sweetened", "salted", "unsalted", "plain",
}

# Preparation/state words that users naturally add to queries but that USDA omits
# from food names (e.g. "peeled orange" → USDA has "Oranges, raw, navels", not
# "orange, peeled"). Stripping these from the API query gets better recall; the
# full user query is still used for local ranking.
_PREP_WORDS = {
    "peeled", "unpeeled", "sliced", "diced", "chopped", "minced", "grated",
    "shredded", "mashed", "pureed", "juiced", "squeezed", "seeded", "pitted",
    "skinless", "boneless", "trimmed", "halved", "quartered", "cubed",
    "cooked", "boiled", "steamed", "baked", "fried", "grilled", "sauteed",
    "blanched", "poached", "braised", "stewed", "microwaved",
    "frozen", "canned", "pickled", "smoked", "cured", "fermented",
    "fresh", "raw", "dried", "dehydrated", "reconstituted",
    "plain", "unseasoned", "seasoned", "marinated",
}

# Words users type as source hints (e.g. "almonds usda") that must be stripped
# before any API or cache query — "usda" appears in every SR Legacy food name
# ("Includes foods for USDA's Food Distribution Program") and would otherwise
# match thousands of irrelevant foods.
_META_WORDS = {"usda", "off", "openfoodfacts"}


def _ensure_api_key() -> bool:
    """Return True if an API key is configured, prompting the user if not."""
    if _usda.get_api_key():
        return True
    state.console.print(f"\n[{state.T['warning']}]No USDA API key configured.[/{state.T['warning']}]")
    state.console.print("  Get a free key at: https://fdc.nal.usda.gov/api-key-signup.html")
    state.console.print("  (A DEMO_KEY works for ~30 requests/hour but is rate-limited.)")
    state.console.print()
    state.console.print(f"  [{state.T['accent']}]1.[/{state.T['accent']}] Enter my API key now")
    state.console.print(f"  [{state.T['accent']}]2.[/{state.T['accent']}] Use DEMO_KEY for now (rate-limited)")
    state.console.print(f"  [dim]b.[/dim] Cancel")
    state.console.print()
    try:
        choice = _prompt("Choice").strip()
    except Cancelled:
        return False
    if choice == "1":
        try:
            key = _prompt("API key").strip()
        except Cancelled:
            return False
        if key:
            _usda.set_api_key(key)
            state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] API key saved.")
            return True
        return False
    elif choice == "2":
        state.console.print("[dim]Using DEMO_KEY.[/dim]")
        return True
    return False

def _simplify_food_query(name: str) -> str:
    """Strip brand-specific adjectives to get a cleaner generic search term."""
    words = name.lower().split()
    # Drop leading adjectives, keep the first noun-like word and anything after
    kept = [w for w in words if w not in _BRAND_ADJECTIVES]
    return " ".join(kept) if kept else name

def _search_cached_foods_by_name(query: str) -> list[dict]:
    with _db.get_db() as conn:
        rows = _db.search_cached_foods(conn, query)
    return [{
        "fdcId":         row["fdc_id"],
        "description":   row["name"],
        "dataType":      row["data_type"],
        "brandOwner":    row["brand"],
        "_from_cache":   True,
        "_portions_json": row["portions_json"],
    } for row in rows]


def _refresh_cache_if_missing_aa(fdc_id: int) -> dict | None:
    """
    If a cached food lacks amino acid data and is SR Legacy or Foundation,
    re-fetch it from the USDA API and update the cache.
    Returns the updated nutrients dict on success, None if not applicable or failed.
    Branded foods are skipped — they genuinely lack AA data in USDA.
    """
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if cached is None:
        return None
    if cached["user_drafted"]:
        return None  # never overwrite user-edited nutrient profiles
    nutrients = json.loads(cached["nutrients_json"])
    data_type = cached["data_type"] or ""
    if data_type == "Branded":
        return None  # branded foods won't have AA data regardless
    # Re-fetch if AA data is missing, OR if protein is 0 in an SR Legacy/Foundation food
    # (protein=0 in a curated food almost always means a corrupted/incomplete cache entry,
    # because has_amino_acid_data() short-circuits to True for protein=0 and would otherwise
    # silently suppress the refresh).
    protein_zero_suspect = (
        nutrients.get("protein_g", 0) == 0
        and data_type in ("SR Legacy", "Foundation")
    )
    if _usda.has_amino_acid_data(nutrients) and not protein_zero_suspect:
        return None  # already has AA data, nothing to do
    # Re-fetch full detail from API
    try:
        detail = _usda.get_food_detail(fdc_id)
    except _usda.USDAError:
        return None
    if not _usda.has_amino_acid_data(detail["nutrients"]):
        return None  # API also lacks AA data — nothing gained
    with _db.get_db() as conn:
        _db.cache_food(
            conn,
            detail["fdcId"], detail["name"], detail["dataType"], detail["brand"],
            detail["servingSize"], detail["servingUnit"], detail["nutrients"],
            detail.get("portions"),
        )
    return detail["nutrients"]


def _suggest_foundation_search(food: dict) -> dict | None:
    """
    When a food has no amino acid data, offer to search Foundation Foods for an
    equivalent that does. Returns an alternative food dict if the user picks one.
    Foundation Foods are USDA's curated dataset with the most complete nutrient
    profiles, including amino acids.
    """
    # Simplify the food name: take words before the first comma
    suggested = food.get("name", "").split(",")[0].strip().lower()
    state.console.print(
        "\n[dim]Foundation Foods is USDA's most complete dataset and usually "
        "includes amino acid data. (Open Food Facts products are excluded here "
        "as they do not contain amino acid profiles.)[/dim]"
    )
    try:
        go = _prompt(
            f"Search Foundation Foods for '{suggested}'?",
            choices=["y", "n"], default="y",
        )
    except Cancelled:
        return None
    if go != "y":
        return None
    return _search_and_pick_food(data_types=["Foundation"], initial_query=suggested)

def _fetch_food_from_result(result: dict) -> dict | None:
    """Fetch full food detail for a search result item (cache → OFF → USDA).

    Used when re-picking from a previously displayed result list without re-running
    the search. Returns a food dict suitable for _pick_portion, or None on failure.
    The name-mismatch guard that exists in the main pick loop is intentionally omitted
    here — the caller already showed the user the food name before they picked it.
    """
    fdc_id = result.get("fdcId")
    if fdc_id is None:
        return None

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if cached:
        nutrients = json.loads(cached["nutrients_json"])
        pj = cached["portions_json"]
        if nutrients and pj is not None and pj != "null":
            return {
                "fdcId":            cached["fdc_id"],
                "name":             cached["name"],
                "dataType":         cached["data_type"],
                "brand":            cached["brand"],
                "servingSize":      cached["serving_size"],
                "servingUnit":      cached["serving_unit"],
                "householdServing": None,
                "nutrients":        nutrients,
                "portions":         json.loads(pj),
            }

    if result.get("_from_off"):
        detail = _off.get_food_detail(result)
        with _db.get_db() as conn:
            _db.cache_food(
                conn,
                detail["fdcId"], detail["name"], detail["dataType"], detail["brand"],
                detail["servingSize"], detail["servingUnit"], detail["nutrients"],
                detail.get("portions"),
            )
        return detail

    state.console.print("[dim]Fetching details...[/dim]")
    try:
        detail = _usda.get_food_detail(fdc_id)
    except _usda.USDAError as e:
        state.console.print(f"[{state.T['error']}]API error: {e}[/{state.T['error']}]")
        return None
    except (TimeoutError, OSError) as e:
        state.console.print(f"[{state.T['error']}]Network error: {e}[/{state.T['error']}]")
        return None
    with _db.get_db() as conn:
        _db.cache_food(
            conn,
            detail["fdcId"], detail["name"], detail["dataType"], detail["brand"],
            detail["servingSize"], detail["servingUnit"], detail["nutrients"],
            detail.get("portions"),
        )
    return detail


def _search_and_pick_food(
    data_types: list[str] | None = None,
    initial_query: str | None = None,
    show_aa_status: bool = True,
    allow_research: bool = True,
    prepend_recipes: list[dict] | None = None,
    result_out: list | None = None,
) -> dict | None:
    """
    Interactive food search: prompts for a query, shows results, user picks one.
    Returns the full food detail dict (from USDA/OFF or cache), or None if cancelled.
    data_types restricts the USDA dataset search (default: Foundation, SR Legacy, Branded).
    Open Food Facts is included automatically in unrestricted (default) searches.
    initial_query pre-fills the search term without prompting.
    show_aa_status: add an AA column — always True by default.
    allow_research: when False, backing out of the pick list skips the current flow
        instead of returning to a new search prompt.
    result_out: if provided, populated (in-place) with the displayed food result list
        after each search so callers can offer re-picks without re-running the search.
    """
    if not _ensure_api_key():
        return None

    query: str | None = initial_query
    full_search: bool = False  # set True only when user types 'a ' prefix
    while True:
        if query is None:
            try:
                raw = _prompt("Search food  (prefix 'a ' for full USDA search)").strip()
            except Cancelled:
                return None
            q_lower = raw.lower()
            if q_lower == "q":
                raise SystemExit(0)
            if q_lower == "b" or not raw:
                return None
            if raw[:2].lower() == "a ":
                full_search = True
                query = raw[2:].strip()
                if not query:
                    query = None
                    continue
            else:
                full_search = False
                query = raw

        results = []
        # Include Open Food Facts only in unrestricted (default) searches.
        # AA-fix searches pass data_types=["Foundation", "SR Legacy"] and should
        # not include OFF products, which never have amino acid data.
        include_off = (data_types is None)

        # Strip source-hint meta words (e.g. "usda", "off") before any search.
        # "usda" appears in every SR Legacy food name and would match thousands of
        # irrelevant foods if passed to the API or cache query.
        _clean_words = [w for w in query.lower().split() if w not in _META_WORDS]
        clean_query = " ".join(_clean_words) if _clean_words else query

        state.console.print("[dim]Searching local cache...[/dim]")
        cache_results = _search_cached_foods_by_name(clean_query)
        cache_fdcids = {r.get("fdcId") for r in cache_results if r.get("fdcId")}

        # Strip prep words for the API query so "peeled orange" finds "Oranges, raw, navels".
        _api_words = [w for w in clean_query.split() if w not in _PREP_WORDS]
        api_query = " ".join(_api_words) if _api_words else clean_query

        if not full_search and cache_results:
            # Only foods with complete cached data (nutrients + portions) are usable
            # for immediate pick; incomplete entries still count for deduplication.
            # When data_types is restricted (e.g. Foundation only), also filter by type
            # so we don't offer off-type cached foods in the quick-pick.
            _complete_cache = [
                r for r in cache_results
                if (r.get("_portions_json") is not None and r.get("_portions_json") != "null")
                and (data_types is None or r.get("dataType") in data_types)
            ]

            _bg_results: list[dict] = []
            _bg_exc: list[Exception] = []
            _bg_done = threading.Event()

            def _bg_search() -> None:
                try:
                    found = _usda.search_foods(api_query, data_types=data_types)
                    if data_types is None:
                        generic = _usda.search_foods(
                            api_query, data_types=["Foundation", "SR Legacy"], page_size=8
                        )
                        generic_ids = {x["fdcId"] for x in generic}
                        found = generic + [x for x in found if x["fdcId"] not in generic_ids]
                    if include_off:
                        try:
                            off_found = _off.search_foods(api_query, page_size=6)
                        except Exception:
                            off_found = []
                        existing = {x.get("description", "").lower() for x in found}
                        for item in off_found:
                            if item["description"].lower() not in existing:
                                found.append(item)
                    _bg_results.extend(found)
                except Exception as exc:
                    _bg_exc.append(exc)
                finally:
                    _bg_done.set()

            threading.Thread(target=_bg_search, daemon=True).start()

            if _complete_cache:
                state.console.print()
                state.console.print(f"  [{state.T['hi']}]In your food cache:[/{state.T['hi']}]")
                for _ci, _cr in enumerate(_complete_cache, 1):
                    _cbrand = _cr.get("brandOwner") or ""
                    _cbrand_str = f"  [dim]{_cbrand}[/dim]" if _cbrand else ""
                    state.console.print(
                        f"    [{state.T['accent']}]{_ci}.[/{state.T['accent']}]"
                        f" {_cr['description']}{_cbrand_str}"
                        f"  [dim]{_cr.get('dataType', '')}[/dim]",
                        highlight=False,
                    )
                state.console.print()

                try:
                    cache_raw = _prompt(
                        "Pick # for cached food, or press Enter for full USDA results"
                    ).strip()
                except Cancelled:
                    return None

                if cache_raw.lower() == "q":
                    raise SystemExit(0)
                if cache_raw.lower() == "m":
                    raise ReturnToMain()
                if cache_raw.lower() == "b":
                    if allow_research:
                        query = None
                        continue
                    return None

                if cache_raw.isdigit():
                    _cidx = int(cache_raw) - 1
                    if 0 <= _cidx < len(_complete_cache):
                        _cfdc_id = _complete_cache[_cidx]["fdcId"]
                        with _db.get_db() as conn:
                            _cc = _db.get_cached_food(conn, _cfdc_id)
                        if _cc:
                            _cn = json.loads(_cc["nutrients_json"])
                            _cpj = _cc["portions_json"]
                            if _cn and _cpj is not None and _cpj != "null":
                                return {
                                    "fdcId":            _cc["fdc_id"],
                                    "name":             _cc["name"],
                                    "dataType":         _cc["data_type"],
                                    "brand":            _cc["brand"],
                                    "servingSize":      _cc["serving_size"],
                                    "servingUnit":      _cc["serving_unit"],
                                    "householdServing": None,
                                    "nutrients":        _cn,
                                    "portions":         json.loads(_cc["portions_json"]),
                                }

            # Wait for background search (may already be done)
            if not _bg_done.is_set():
                if data_types == ["Foundation"]:
                    _lbl = "Foundation Foods"
                elif data_types == ["Foundation", "SR Legacy"]:
                    _lbl = "SR Legacy + Foundation Foods"
                elif include_off:
                    _lbl = "USDA + Open Food Facts"
                else:
                    _lbl = "USDA"
                state.console.print(f"[dim]Searching {_lbl}...[/dim]")
                _bg_done.wait()

            if _bg_exc and not _bg_results:
                _be = _bg_exc[0]
                if isinstance(_be, _usda.USDAError):
                    state.console.print(
                        f"[{state.T['warning']}]{_be} — showing cached results only.[/{state.T['warning']}]"
                    )
                    results = [{**r, "_from_cache": True} for r in cache_results]
                else:
                    state.console.print(
                        f"[{state.T['error']}]{_be}[/{state.T['error']}]\n"
                        f"[dim]No results available. Try a different search term or check your connection.[/dim]"
                    )
                    if allow_research:
                        query = None
                        continue
                    return None
            else:
                tagged_cache = [{**r, "_from_cache": True} for r in cache_results]
                results = tagged_cache + [
                    r for r in _bg_results if r.get("fdcId") not in cache_fdcids
                ]
        else:
            # No cache hits (or explicit full search): run API search synchronously.
            if data_types == ["Foundation"]:
                label = "Foundation Foods"
            elif data_types == ["Foundation", "SR Legacy"]:
                label = "SR Legacy + Foundation Foods"
            elif include_off:
                label = "USDA + Open Food Facts"
            else:
                label = "USDA"
            state.console.print(f"[dim]Searching {label}...[/dim]")
            state.console.print()
            try:
                api_results = _usda.search_foods(api_query, data_types=data_types)
                # For default (unrestricted) searches the USDA API ranks by its own relevance
                # score, which buries Foundation/SR Legacy under many branded results.
                # Fetch them explicitly and prepend so they always appear.
                if data_types is None:
                    generic = _usda.search_foods(
                        api_query, data_types=["Foundation", "SR Legacy"], page_size=8
                    )
                    generic_ids = {r["fdcId"] for r in generic}
                    api_results = generic + [r for r in api_results if r["fdcId"] not in generic_ids]
            except _usda.USDAError as e:
                if cache_results:
                    state.console.print(
                        f"[{state.T['warning']}]{e} — showing cached results only.[/{state.T['warning']}]"
                    )
                    api_results = []
                else:
                    state.console.print(
                        f"[{state.T['error']}]{e}[/{state.T['error']}]\n"
                        f"[dim]No cached results for this query. Try a different search term or check your connection.[/dim]"
                    )
                    if allow_research:
                        query = None
                        continue
                    return None
            if include_off:
                try:
                    off_results = _off.search_foods(api_query, page_size=6)
                except Exception:
                    off_results = []
                    state.console.print("[dim]Open Food Facts unavailable; skipping.[/dim]")
                existing_names = {r.get("description", "").lower() for r in api_results}
                for r in off_results:
                    if r["description"].lower() not in existing_names:
                        api_results.append(r)

            # Merge: tag cache hits, then append remote items not already cached.
            tagged_cache = [{**r, "_from_cache": True} for r in cache_results]
            results = tagged_cache + [
                r for r in api_results if r.get("fdcId") not in cache_fdcids
            ]

        if not results:
            state.console.print(f"[{state.T['warning']}]No results found.[/{state.T['warning']}]")
            if allow_research:
                query = None
                continue
            return None

        # Deduplicate by (normalized description, brand) — keep first occurrence
        def _norm(s: str) -> str:
            return " ".join(re.sub(r'[^a-z0-9]', ' ', s.lower()).split())

        seen: set[tuple[str, str]] = set()
        deduped: list[dict] = []
        for food in results:
            brand = food.get("brandOwner") or food.get("brandName") or ""
            key = (_norm(food.get("description", "")), _norm(brand))
            if key not in seen:
                seen.add(key)
                deduped.append(food)

        # Bulk-fetch annotations for all candidates (single query, used for sort + display).
        with _db.get_db() as _ann_conn:
            _annotations = _db.annotations_for_fdcids(
                _ann_conn, [f["fdcId"] for f in deduped if isinstance(f.get("fdcId"), int)]
            )
        for food in deduped:
            food["_annotation"] = _annotations.get(food.get("fdcId"))

        # Sort: cache hits always first; within cache, annotated before unannotated;
        # then by data quality tier and word relevance.
        # Tier order: Foundation (1) → SR Legacy (2) → Open Food Facts (3) → Branded (4)
        def _norm(s: str) -> str:  # re-define to keep local scope clean
            return " ".join(re.sub(r'[^a-z0-9]', ' ', s.lower()).split())

        query_words = set(_norm(query).split())

        def _word_score(food: dict) -> int:
            desc_words = set(_norm(food.get("description", "")).split())
            # One-directional: query word must be a prefix/substring of a description word,
            # not the reverse — prevents "peel" in "peeled" causing false matches.
            return sum(
                1 for qw in query_words
                if any(qw in dw for dw in desc_words)
            )

        def _data_tier(food: dict) -> int:
            dtype = food.get("dataType", "")
            if dtype == "Foundation":
                return 1
            if dtype == "SR Legacy":
                return 2
            if food.get("_from_off") or dtype == "Open Food Facts":
                return 3
            return 4  # Branded or unknown

        def _ann_has_data(food: dict) -> bool:
            ann = food.get("_annotation")
            return ann is not None and (
                ann["gi_estimate"] is not None or ann["diaas_estimate"] is not None
            )

        # Detect a brand-specific query: any brand word (≥4 chars) appears in the query.
        query_lower = query.lower()
        brand_in_query = any(
            word in query_lower
            for food in deduped
            for word in _norm(food.get("brandOwner") or food.get("brandName") or "").split()
            if len(word) >= 4
        )

        if brand_in_query:
            results = sorted(deduped, key=lambda f: (
                not f.get("_from_cache"),
                not _ann_has_data(f),
                -_word_score(f),
                _data_tier(f),
            ))
        else:
            results = sorted(deduped, key=lambda f: (
                not f.get("_from_cache"),
                not _ann_has_data(f),
                _data_tier(f),
                -_word_score(f),
            ))

        if result_out is not None:
            result_out[:] = results

        recipe_rows = prepend_recipes or []

        _SRCH_W = 36
        _BRAND_W = 24
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",       justify="right", min_width=3)
        tbl.add_column("Type",    min_width=12)
        tbl.add_column("ID",      justify="right", min_width=7)
        tbl.add_column("Food / Recipe", min_width=_SRCH_W, max_width=_SRCH_W, no_wrap=True)
        tbl.add_column("Brand",   min_width=_BRAND_W, max_width=_BRAND_W, no_wrap=True)
        tbl.add_column("Ann",     min_width=5)
        if show_aa_status:
            tbl.add_column("AA data", min_width=8)

        def _srch_cell(text: str) -> str:
            """Word-wrap to _SRCH_W; dot-pad the last line only."""
            words = text.split()
            if not words:
                return ""
            lines: list[str] = []
            current = ""
            for word in words:
                candidate = f"{current} {word}" if current else word
                if len(candidate) <= _SRCH_W - 1:
                    current = candidate
                else:
                    if current:
                        lines.append(current)
                    current = word[: _SRCH_W - 1]
            if current:
                lines.append(current)
            last = lines[-1]
            pad = _SRCH_W - len(last) - 1
            if pad > 0:
                lines[-1] = f"{last} [dim]{'·' * pad}[/dim]"
            return "\n".join(lines)

        def _brand_cell(brand: str) -> str:
            if not brand:
                return f"[dim]{'·' * _BRAND_W}[/dim]"
            t = brand[: _BRAND_W - 1]
            pad = _BRAND_W - len(t) - 1
            return f"{t} [dim]{'·' * pad}[/dim]" if pad > 0 else t

        def _type_cell(food: dict) -> str:
            dtype = food.get("dataType", "")
            if food.get("_from_cache"):
                return f"[{state.T['success']}]★[/{state.T['success']}] {dtype}"
            return dtype

        def _ann_cell(food: dict) -> str:
            ann = food.get("_annotation")
            has_gi    = ann is not None and ann["gi_estimate"]    is not None
            has_diaas = ann is not None and ann["diaas_estimate"] is not None
            s = state.T["success"]
            if has_gi and has_diaas:
                return f"[{s}]GI DI[/{s}]"
            if has_gi:
                return f"[{s}]GI[/{s}][dim] ··[/dim]"
            if has_diaas:
                return f"[dim]·· [/dim][{s}]DI[/{s}]"
            return "[dim]·····[/dim]"

        # Recipe rows at top (R1, R2, …)
        for i, r in enumerate(recipe_rows, 1):
            aa_cell = (f"[{state.T['success']}]✓[/{state.T['success']}]"
                       if r["dcp_g"] is not None
                       else "[dim]—[/dim]")
            row = [f"R{i}", "Recipe", "", _srch_cell(r["name"]), _brand_cell(""), "[dim]——[/dim]"]
            if show_aa_status:
                row.append(aa_cell)
            tbl.add_row(*row)

        branded_count = 0
        for i, food in enumerate(results, 1):
            brand = food.get("brandOwner") or food.get("brandName") or ""
            dtype = food.get("dataType", "")
            if brand or dtype in ("Branded", "Open Food Facts"):
                branded_count += 1
            if show_aa_status:
                if food.get("_from_off"):
                    # OFF never has AA data
                    aa_cell = f"[{state.T['error']}]✗[/{state.T['error']}]"
                elif food.get("_alias_has_aa"):
                    # Alias: AA data verified in USDA — but check local cache to decide ✓ vs ~✓
                    with _db.get_db() as _ac:
                        _alias_cached = _db.get_cached_food(_ac, food["fdcId"])
                    if (_alias_cached is not None
                            and _usda.has_amino_acid_data(json.loads(_alias_cached["nutrients_json"]))):
                        aa_cell = f"[{state.T['success']}]✓[/{state.T['success']}]"
                    else:
                        aa_cell = f"[{state.T['success']}]~✓[/{state.T['success']}]"
                else:
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, food["fdcId"])
                    if cached is not None:
                        if _usda.has_amino_acid_data(json.loads(cached["nutrients_json"])):
                            aa_cell = f"[{state.T['success']}]✓[/{state.T['success']}]"
                        else:
                            aa_cell = f"[{state.T['error']}]✗[/{state.T['error']}]"
                    elif dtype in ("Foundation", "SR Legacy"):
                        # Not yet fetched, but these datasets almost always include AA data
                        aa_cell = f"[{state.T['success']}]~✓[/{state.T['success']}]"
                    else:
                        # Branded / unknown: virtually never have AA data in USDA
                        aa_cell = f"[{state.T['error']}]✗[/{state.T['error']}]"
                tbl.add_row(str(i), _type_cell(food), _id_cell(food['fdcId']), _srch_cell(food.get('description', '')), _brand_cell(brand), _ann_cell(food), aa_cell)
            else:
                tbl.add_row(str(i), _type_cell(food), _id_cell(food['fdcId']), _srch_cell(food.get('description', '')), _brand_cell(brand), _ann_cell(food))
        if show_aa_status:
            likely_count = 0
            for food in results:
                if food.get('_alias_has_aa'):
                    with _db.get_db() as _lc:
                        _lcached = _db.get_cached_food(_lc, food["fdcId"])
                    if (_lcached is not None
                            and _usda.has_amino_acid_data(json.loads(_lcached["nutrients_json"]))):
                        likely_count += 1  # confirmed ✓
                    else:
                        likely_count += 1  # ~✓ — counts as a good candidate
                    continue
                fdtype = food.get("dataType", "")
                with _db.get_db() as conn:
                    cached = _db.get_cached_food(conn, food['fdcId'])
                if cached is not None and _usda.has_amino_acid_data(json.loads(cached['nutrients_json'])):
                    likely_count += 1
                elif cached is None and fdtype in ("Foundation", "SR Legacy"):
                    likely_count += 1
        table_title("FOOD SEARCH RESULTS")
        state.console.print(tbl)
        state.console.print()
        state.console.print(f"  {ID_KEY}")
        _cached_count = sum(1 for f in results if f.get("_from_cache"))
        if _cached_count:
            state.console.print(
                f"  [dim][{state.T['success']}]★[/{state.T['success']}] in Type column = already in your local cache (instant — no network fetch)[/dim]",
                highlight=False,
            )
        state.console.print(
            f"  [dim]Ann (Annotations): [{state.T['success']}]GI[/{state.T['success']}] glycemic index · "
            f"[{state.T['success']}]DI[/{state.T['success']}] DIAAS — your saved estimates[/dim]",
            highlight=False,
        )
        if show_aa_status:
            state.console.print()
            state.console.print(
                f"  [dim]AA data column key:[/dim]\n"
                f"    [{state.T['success']}]✓[/{state.T['success']}]  [dim]confirmed — amino acid data in local cache[/dim]\n"
                f"    [{state.T['success']}]~✓[/{state.T['success']}] [dim]likely — not fetched yet; pick the number to fetch and confirm[/dim]\n"
                f"    [{state.T['error']}]✗[/{state.T['error']}]  [dim]none — branded/packaged food; USDA rarely includes AA data for these[/dim]",
                highlight=False,
            )
            if likely_count > 0:
                state.console.print(
                    f"  [dim]  → [bold]~✓[/bold] items are not yet in your cache. "
                    f"Enter the item number to fetch and cache it.[/dim]",
                    highlight=False,
                )
            if likely_count == 0:
                state.console.print(
                    f"  [{state.T['warning']}]No options with amino acid data found.[/{state.T['warning']}] "
                    "[dim]Try searching for a generic equivalent — add 'raw', 'cooked', or 'usda' to your query.[/dim]",
                    highlight=False,
                )

        _W = min(98, state.console.width - 2)
        if branded_count == 0 and data_types != ["Foundation"]:
            _msg = textwrap.fill(
                f"No branded or Open Food Facts products found for \"{query}\" — "
                f"showing generic/legacy equivalents.",
                width=_W, initial_indent="  ", subsequent_indent="  ",
            )
            state.console.print(
                f"[{state.T['warning']}]{_msg}[/{state.T['warning']}]",
                highlight=False,
            )
        elif branded_count >= len(results) // 2:
            _msg = textwrap.fill(
                "Tip: most results are branded products. For home-cooked or "
                "generic foods, try adding 'cooked', 'raw', or 'usda' to your search "
                "(e.g. 'pinto beans cooked').",
                width=_W, initial_indent="  ", subsequent_indent="  ",
            )
            state.console.print(f"[dim]{_msg}[/dim]", highlight=False)

        help_footer()

        pick_hint = ("  R#/# or id:FDCID, Enter/b=back, m=main, q=quit"
                     if recipe_rows else
                     "  Pick number, id:FDCID, or Enter/b=back, m=main, q=quit")

        # Inner loop: re-prompt on bad pick without re-running the search.
        while True:
            try:
                raw = _prompt(pick_hint).strip()
            except Cancelled:
                return None
            if raw.lower() == "m":
                raise ReturnToMain()
            if raw.lower() == "q":
                raise SystemExit(0)
            if not raw or raw.lower() == "b":
                if allow_research:
                    query = None
                    break  # → outer loop re-prompts for query
                return None

            # Recipe pick: R1, R2, …
            rl = raw.lower()
            if rl.startswith("r") and rl[1:].isdigit():
                ridx = int(rl[1:]) - 1
                if 0 <= ridx < len(recipe_rows):
                    r = recipe_rows[ridx]
                    return {
                        "_type":        "recipe",
                        "id":           r["id"],
                        "name":         r["name"],
                        "servings":     r["servings"],
                        "dcp_g":        r["dcp_g"],
                        "total_weight": r["total_weight"] if r["total_weight"] else None,
                    }
                state.console.print(f"  [{state.T['warning']}]Invalid recipe selection.[/{state.T['warning']}]")
                continue

            # Direct FDC ID lookup: id:171545 (USDA only)
            selected_result: dict | None = None
            selected_name: str | None = None
            if raw.lower().startswith("id:"):
                try:
                    fdc_id = int(raw[3:].strip())
                except ValueError:
                    state.console.print(f"  [{state.T['warning']}]Invalid FDC ID.[/{state.T['warning']}]")
                    continue
            else:
                try:
                    idx = int(raw) - 1
                    if idx < 0 or idx >= len(results):
                        raise ValueError
                except ValueError:
                    state.console.print(f"  [{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
                    continue
                selected_result = results[idx]
                fdc_id = selected_result["fdcId"]
                selected_name = selected_result.get("description", "")

            # Try cache first
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, fdc_id)
            if cached:
                nutrients = json.loads(cached["nutrients_json"])
                pj = cached["portions_json"]
                if nutrients and pj is not None and pj != "null":
                    return {
                        "fdcId":            cached["fdc_id"],
                        "name":             cached["name"],
                        "dataType":         cached["data_type"],
                        "brand":            cached["brand"],
                        "servingSize":      cached["serving_size"],
                        "servingUnit":      cached["serving_unit"],
                        "householdServing": None,
                        "nutrients":        nutrients,
                        "portions":         json.loads(cached["portions_json"]),
                    }

            # Open Food Facts: nutrients are already in the search result — no second call needed
            if selected_result and selected_result.get("_from_off"):
                detail = _off.get_food_detail(selected_result)
                with _db.get_db() as conn:
                    _db.cache_food(
                        conn,
                        detail["fdcId"], detail["name"], detail["dataType"], detail["brand"],
                        detail["servingSize"], detail["servingUnit"], detail["nutrients"],
                        detail.get("portions"),
                    )
                return detail

            # USDA: fetch full detail from API
            state.console.print("[dim]Fetching details...[/dim]")
            try:
                detail = _usda.get_food_detail(fdc_id)
            except _usda.USDAError as e:
                state.console.print(
                    f"[{state.T['error']}]API error: {e}[/{state.T['error']}]\n"
                    f"[dim]  (The USDA search index sometimes lists FDC IDs that no longer exist.\n"
                    f"   Try a different result, or use id:FDCID with a known-good ID.)[/dim]"
                )
                continue
            except (TimeoutError, OSError) as e:
                state.console.print(
                    f"[{state.T['error']}]Network error fetching food details: {e}[/{state.T['error']}]\n"
                    f"[dim]  Check your connection and try again.[/dim]"
                )
                continue

            # Verify the returned food matches what was selected (USDA search IDs can be wrong)
            if selected_name:
                def _name_words(s: str) -> set[str]:
                    return {w for w in re.sub(r'[^a-z0-9]', ' ', s.lower()).split() if len(w) > 2}
                sel_words = _name_words(selected_name)
                got_words = _name_words(detail["name"])
                overlap = len(sel_words & got_words) / max(len(sel_words), 1)
                if overlap < 0.4:
                    state.console.print(
                        f"\n  [{state.T['warning']}]⚠  USDA returned a different food than selected:[/{state.T['warning']}]\n"
                        f"  Selected:  {selected_name}\n"
                        f"  Returned:  {detail['name']}\n"
                        f"  [dim]This is a known USDA API issue. Try searching again or use id:FDCID.[/dim]"
                    )
                    confirm = _ask_yes_no_quit("Use it anyway?  [dim](y=yes · n=no · q=quit)[/dim]", default="n")
                    if confirm == "q":
                        raise SystemExit(0)
                    if confirm != "y":
                        query = None
                        break  # → outer loop re-prompts for query

            # Cache it
            with _db.get_db() as conn:
                _db.cache_food(
                    conn,
                    detail["fdcId"], detail["name"], detail["dataType"], detail["brand"],
                    detail["servingSize"], detail["servingUnit"], detail["nutrients"],
                    detail.get("portions"),
                )

            return detail
