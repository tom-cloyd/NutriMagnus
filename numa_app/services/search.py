import json
import re

from rich.table import Table

import db as _db
import usda as _usda
import openfoodfacts as _off
from .. import state
from ..ui.common import _id_cell, ID_KEY
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
        "fdcId": row["fdc_id"],
        "description": row["name"],
        "dataType": row["data_type"],
        "brandOwner": row["brand"],
        "_from_cache": True,
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

def _search_and_pick_food(
    data_types: list[str] | None = None,
    initial_query: str | None = None,
    show_aa_status: bool = True,
    allow_research: bool = True,
    prepend_recipes: list[dict] | None = None,
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
    """
    if not _ensure_api_key():
        return None

    query: str | None = initial_query
    while True:
        if query is None:
            try:
                query = _prompt("Search food").strip()
            except Cancelled:
                return None
            q_lower = query.lower()
            if q_lower == "q":
                raise SystemExit(0)
            if q_lower == "b" or not query:
                return None

        results = []
        # Include Open Food Facts only in unrestricted (default) searches.
        # AA-fix searches pass data_types=["Foundation", "SR Legacy"] and should
        # not include OFF products, which never have amino acid data.
        include_off = (data_types is None)

        # Always search the local cache first, then merge with remote results.
        state.console.print("[dim]Searching local cache...[/dim]")
        cache_results = _search_cached_foods_by_name(query)
        cache_fdcids = {r.get("fdcId") for r in cache_results if r.get("fdcId")}

        # Strip prep words for the API query so "peeled orange" finds "Oranges, raw, navels".
        # The full user query is still used for local ranking.
        _api_words = [w for w in query.lower().split() if w not in _PREP_WORDS]
        api_query = " ".join(_api_words) if _api_words else query

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
        except _usda.USDAError as e:
            if cache_results:
                state.console.print(
                    f"[{state.T['warning']}]USDA API error ({e}); showing cached results only.[/{state.T['warning']}]"
                )
                api_results = []
            else:
                state.console.print(f"[{state.T['error']}]API error: {e}[/{state.T['error']}]")
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

        # Sort: tier-first unless the query names a specific brand.
        # Tier order: cache (0) → Foundation (1) → SR Legacy (2) → Open Food Facts (3) → Branded (4)
        # Within each tier, rank by number of query words matched in the description.
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

        def _source_tier(food: dict) -> int:
            if food.get("_from_cache"):
                return 0
            dtype = food.get("dataType", "")
            if dtype == "Foundation":
                return 1
            if dtype == "SR Legacy":
                return 2
            if food.get("_from_off") or dtype == "Open Food Facts":
                return 3
            return 4  # Branded or unknown

        # Detect a brand-specific query: any brand word (≥4 chars) appears in the query.
        query_lower = query.lower()
        brand_in_query = any(
            word in query_lower
            for food in deduped
            for word in _norm(food.get("brandOwner") or food.get("brandName") or "").split()
            if len(word) >= 4
        )

        results = sorted(deduped, key=lambda f: (-_word_score(f), _source_tier(f)))

        recipe_rows = prepend_recipes or []

        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",       justify="right", min_width=3)
        tbl.add_column("Type",    min_width=12)
        tbl.add_column("ID",      justify="right", min_width=7)
        tbl.add_column("Food / Recipe", min_width=32)
        tbl.add_column("Brand",   min_width=20)
        if show_aa_status:
            tbl.add_column("AA data", min_width=8)

        # Recipe rows at top (R1, R2, …)
        for i, r in enumerate(recipe_rows, 1):
            aa_cell = (f"[{state.T['success']}]✓[/{state.T['success']}]"
                       if r["dcp_g"] is not None
                       else "[dim]—[/dim]")
            row = [f"R{i}", "Recipe", "", r["name"], ""]
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
                tbl.add_row(str(i), dtype, _id_cell(food['fdcId']), food.get('description', ''), brand, aa_cell)
            else:
                tbl.add_row(str(i), dtype, _id_cell(food['fdcId']), food.get('description', ''), brand)
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
        state.console.print(tbl)
        state.console.print(f"  {ID_KEY}")
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

        if branded_count == 0 and data_types != ["Foundation"]:
            state.console.print(
                f"[{state.T['warning']}]No branded or Open Food Facts products found for \"{query}\" — "
                f"showing generic/legacy equivalents.[/{state.T['warning']}]"
            )
        elif branded_count >= len(results) // 2:
            state.console.print(
                "[dim]Tip: most results are branded products. For home-cooked or "
                "generic foods, try adding 'cooked', 'raw', or 'usda' to your search "
                "(e.g. 'pinto beans cooked').[/dim]"
            )

        pick_hint = ("R#/# or id:FDCID, Enter/b=back, m=main, q=quit"
                     if recipe_rows else
                     "Pick number, id:FDCID, or Enter/b=back, m=main, q=quit")
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
                continue
            return None

        # Recipe pick: R1, R2, …
        rl = raw.lower()
        if rl.startswith("r") and rl[1:].isdigit():
            ridx = int(rl[1:]) - 1
            if 0 <= ridx < len(recipe_rows):
                r = recipe_rows[ridx]
                return {
                    "_type":    "recipe",
                    "id":       r["id"],
                    "name":     r["name"],
                    "servings": r["servings"],
                    "dcp_g":    r["dcp_g"],
                }
            state.console.print(f"[{state.T['warning']}]Invalid recipe selection.[/{state.T['warning']}]")
            continue

        # Direct FDC ID lookup: id:171545 (USDA only)
        selected_result: dict | None = None
        selected_name: str | None = None
        if raw.lower().startswith("id:"):
            try:
                fdc_id = int(raw[3:].strip())
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Invalid FDC ID.[/{state.T['warning']}]")
                continue
        else:
            try:
                idx = int(raw) - 1
                if idx < 0 or idx >= len(results):
                    raise ValueError
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
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
                    continue

        # Cache it
        with _db.get_db() as conn:
            _db.cache_food(
                conn,
                detail["fdcId"], detail["name"], detail["dataType"], detail["brand"],
                detail["servingSize"], detail["servingUnit"], detail["nutrients"],
                detail.get("portions"),
            )

        return detail
