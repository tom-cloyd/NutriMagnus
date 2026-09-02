"""
search_suggest.py — "did you mean" suggestions for a food/recipe search that
returned no results.

A lightweight, dependency-free fuzzy match (stdlib difflib) against every
food/recipe name this install already knows — cached foods, pantry, recipes
— plus the food names bundled with the CoFID/AFCD/CIQUAL static datasets
(numa_app.services.static_source_lookup). No network call, so it works
offline and costs nothing to try on every empty search.

This can't suggest a branded product (e.g. a cracker brand) that's never
been searched/cached on this install and isn't in the three bundled
national food-composition tables (which list generic ingredients, not
brands) — there's no bundled catalog of every branded product name to check
against. In that case suggest() just returns [], same as "nothing close
enough found".

Docs: README-numa-documentation.md, Architecture: "search_suggest.py — did-you-mean search suggestions"
"""
from __future__ import annotations

import difflib
import functools
import re
import sqlite3

import afcd_lookup as _afcd
import ciqual_lookup as _ciqual
import cofid_lookup as _cofid
import db as _db

_TOKEN_RE = re.compile(r"[a-z']+")
_MIN_TOKEN_LEN = 4
# The local corpus (foods/pantry/recipes you've actually searched or added
# before) is small and low-noise, so a looser cutoff there still gives good
# matches; the bundled static datasets are ~7,600 generic food names — a
# stricter cutoff keeps that larger, noisier corpus from surfacing
# unrelated words that merely share a lot of characters.
_LOCAL_CUTOFF = 0.65
_STATIC_CUTOFF = 0.72


def _tokenize_names(names) -> set[str]:
    tokens = set()
    for name in names:
        if not name:
            continue
        for tok in _TOKEN_RE.findall(name.lower()):
            if len(tok) >= _MIN_TOKEN_LEN:
                tokens.add(tok)
    return tokens


@functools.lru_cache(maxsize=1)
def _static_tokens() -> frozenset[str]:
    """Tokens from the three bundled national food-composition datasets —
    built once per process, since those files never change at runtime."""
    names: list[str] = []
    for mod in (_afcd, _cofid, _ciqual):
        names.extend(mod.all_names())
    return frozenset(_tokenize_names(names))


def _local_tokens(conn: sqlite3.Connection) -> set[str]:
    names: list[str] = []
    names.extend(r["name"] for r in _db.list_cached_foods(conn))
    names.extend(r["food_name"] for r in _db.pantry_list(conn))
    names.extend(r["name"] for r in _db.recipe_list(conn))
    return _tokenize_names(names)


def suggest(conn: sqlite3.Connection, query: str, limit: int = 3) -> list[str]:
    """Return up to `limit` corrected versions of `query`, each with exactly
    one word swapped for its closest known match. [] if the query is blank,
    every word is already a known token, or nothing was close enough.

    A word this install has actually seen before (cached foods, pantry,
    recipes) is preferred over one only present in the bundled national
    food-composition name lists — a name you've searched before is more
    likely what you meant, and re-searching it is guaranteed to find
    something, whereas a bundled-dataset word is merely a real word."""
    query = (query or "").strip()
    if not query:
        return []
    local_corpus = _local_tokens(conn)
    static_corpus = _static_tokens()
    words = query.split()
    variants: list[str] = []
    seen: set[str] = {query.lower()}
    for i, w in enumerate(words):
        lw = w.lower()
        if len(lw) < _MIN_TOKEN_LEN or lw in local_corpus or lw in static_corpus:
            continue
        candidates = difflib.get_close_matches(lw, local_corpus, n=limit, cutoff=_LOCAL_CUTOFF)
        if len(candidates) < limit:
            for extra in difflib.get_close_matches(lw, static_corpus, n=limit, cutoff=_STATIC_CUTOFF):
                if extra not in candidates:
                    candidates.append(extra)
                if len(candidates) >= limit:
                    break
        for close in candidates:
            new_words = list(words)
            new_words[i] = close
            variant = " ".join(new_words)
            if variant.lower() not in seen:
                seen.add(variant.lower())
                variants.append(variant)
    return variants[:limit]
