"""
search_ranking.py — shared food-search relevance ranking (CLI + web).
Docs: README-numa-documentation.md

Ranks a candidate name against a multi-word query so that:
  1. More matching query words always outranks fewer (all terms > all-but-one > ...).
  2. Within an equal match count, matching the EARLIER query words outranks
     matching later ones — so "milk dry instant" ranks "milk dry" hits ahead
     of "milk instant" hits, since "instant" (the last word) is the one
     missing in the stronger result.
  3. Source (pantry/cache/recipe/external) breaks remaining ties — a real
     match always beats a weak or coincidental one, regardless of where it
     lives.
  4. Among external (USDA/OFF) results tied on all of the above, USDA data
     quality breaks the tie: Foundation/SR Legacy (far more likely to carry
     real amino acid data) beats Survey/Experimental, which beats Branded/
     Open Food Facts. Without this, a wall of near-identical branded product
     names (all short, all matching every query word) can bury the one
     Foundation/SR Legacy food that actually has the data being searched
     for, since a bare text/length tiebreak has no way to prefer it.
"""
SOURCE_RANK = {"pantry": 0, "cache": 1, "recipe": 2, "usda": 3, "off": 3}

DATA_TYPE_RANK = {
    "Foundation": 0, "SR Legacy": 0,
    "Survey (FNDDS)": 1, "Experimental": 1,
    "Branded": 2, "Open Food Facts": 2, "OFF": 2,
}


def _query_words(query: str) -> list[str]:
    return query.lower().split()


def _match_count_and_mask(name_lower: str, words: list[str]) -> tuple[int, int]:
    """Bit i (from the left, MSB = first query word) is set if words[i] is
    present in name_lower. Comparing masks as integers naturally prefers
    matches on earlier words when the match count is tied."""
    count = 0
    mask = 0
    n = len(words)
    for i, w in enumerate(words):
        if w in name_lower:
            count += 1
            mask |= 1 << (n - 1 - i)
    return count, mask


def relevance_key(name: str, query: str, source: str = "", data_type: str = "") -> tuple:
    """Sort key for a single candidate — lower sorts first."""
    nl = (name or "").lower().strip()
    ql = (query or "").lower().strip()
    words = _query_words(ql)
    count, mask = _match_count_and_mask(nl, words)
    return (
        -count,
        -mask,
        SOURCE_RANK.get(source, 9),
        DATA_TYPE_RANK.get(data_type, 1),
        0 if nl == ql else 1,
        0 if nl.startswith(ql) else 1,
        len(nl),
        nl,
    )
