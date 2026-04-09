import json
import re

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..ui.prompts import Cancelled, _prompt

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
    nutrients = json.loads(cached["nutrients_json"])
    if _usda.has_amino_acid_data(nutrients):
        return None  # already has AA data, nothing to do
    data_type = cached["data_type"] or ""
    if data_type == "Branded":
        return None  # branded foods won't have AA data regardless
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
        "includes amino acid data.[/dim]"
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
    show_aa_status: bool = False,
    allow_research: bool = True,
) -> dict | None:
    """
    Interactive food search: prompts for a query, shows results, user picks one.
    Returns the full food detail dict (from USDA or cache), or None if cancelled.
    data_types restricts the USDA dataset search (default: Foundation, SR Legacy, Branded).
    initial_query pre-fills the search term without prompting.
    show_aa_status: add an AA column by checking the local cache (no extra API calls).
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

        if data_types == ["Foundation"]:
            label = "Foundation Foods"
        elif data_types == ["Foundation", "SR Legacy"]:
            label = "SR Legacy + Foundation Foods"
        else:
            label = "USDA"
        state.console.print(f"[dim]Searching {label}...[/dim]")
        try:
            results = _usda.search_foods(query, data_types=data_types)
        except _usda.USDAError as e:
            state.console.print(f"[{state.T['error']}]API error: {e}[/{state.T['error']}]")
            return None

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

        # Re-rank: more query-word matches in description → higher
        query_words = set(_norm(query).split())
        def _score(food: dict) -> int:
            desc_words = set(_norm(food.get("description", "")).split())
            return len(query_words & desc_words)
        results = sorted(deduped, key=_score, reverse=True)

        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",       justify="right", min_width=3)
        tbl.add_column("Type",    min_width=12)
        tbl.add_column("Food",    min_width=40)
        tbl.add_column("Brand",   min_width=20)
        if show_aa_status:
            tbl.add_column("AA data", min_width=8)
        branded_count = 0
        for i, food in enumerate(results, 1):
            brand = food.get("brandOwner") or food.get("brandName") or ""
            dtype = food.get("dataType", "")
            if brand or dtype == "Branded":
                branded_count += 1
            if show_aa_status:
                if food.get("_alias_has_aa"):
                    aa_cell = f"[{state.T['success']}]✓[/{state.T['success']}]"
                else:
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, food["fdcId"])
                    if cached is None:
                        aa_cell = "[dim]?[/dim]"
                    elif _usda.has_amino_acid_data(json.loads(cached["nutrients_json"])):
                        aa_cell = f"[{state.T['success']}]✓[/{state.T['success']}]"
                    else:
                        aa_cell = f"[{state.T['error']}]✗[/{state.T['error']}]"
                tbl.add_row(str(i), dtype, food.get("description", ""), brand, aa_cell)
            else:
                tbl.add_row(str(i), dtype, food.get("description", ""), brand)
        if show_aa_status:
            confirmed_count = 0
            for food in results:
                if food.get('_alias_has_aa'):
                    confirmed_count += 1
                    continue
                with _db.get_db() as conn:
                    cached = _db.get_cached_food(conn, food['fdcId'])
                if cached is not None and _usda.has_amino_acid_data(json.loads(cached['nutrients_json'])):
                    confirmed_count += 1
            state.console.print("[dim]  AA data: ✓ confirmed  ✗ none  ? not yet fetched (SR Legacy usually has it)[/dim]")
        state.console.print(tbl)
        if show_aa_status and confirmed_count == 0:
            state.console.print("[dim]No options with confirmed amino acid data were found. You can try a '?' entry or press Enter/b to skip.[/dim]")

        if branded_count == 0 and data_types != ["Foundation"]:
            state.console.print(
                f"[{state.T['warning']}]No branded products found for \"{query}\" — "
                f"showing generic/legacy equivalents.[/{state.T['warning']}]"
            )
        elif branded_count >= len(results) // 2:
            state.console.print(
                "[dim]Tip: most results are branded products. For home-cooked or "
                "generic foods, try adding 'cooked', 'raw', or 'usda' to your search "
                "(e.g. 'pinto beans cooked').[/dim]"
            )

        try:
            raw = _prompt("Pick number, id:FDCID, or Enter/b=back, q=quit").strip()
        except Cancelled:
            return None
        if raw.lower() == "q":
            raise SystemExit(0)
        if not raw or raw.lower() == "b":
            if allow_research:
                query = None
                continue
            return None

        # Direct FDC ID lookup: id:171545
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
            fdc_id = results[idx]["fdcId"]
            selected_name = results[idx].get("description", "")

        # Try cache first
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached:
            nutrients = json.loads(cached["nutrients_json"])
            # portions_json is 'null' (or SQL NULL) when portions have never been fetched.
            # '[]' means fetched and confirmed none; '[...]' means fetched and has portions.
            # Only serve from cache when both nutrients and portions data are present.
            pj = cached["portions_json"]
            if nutrients and pj is not None and pj != "null":
                return {
                    "fdcId":          cached["fdc_id"],
                    "name":           cached["name"],
                    "dataType":       cached["data_type"],
                    "brand":          cached["brand"],
                    "servingSize":    cached["serving_size"],
                    "servingUnit":    cached["serving_unit"],
                    "householdServing": None,
                    "nutrients":      nutrients,
                    "portions":       json.loads(cached["portions_json"]),
                }

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
                try:
                    confirm = _prompt("Use it anyway?", choices=["y", "n"], default="n")
                except Cancelled:
                    confirm = "n"
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
