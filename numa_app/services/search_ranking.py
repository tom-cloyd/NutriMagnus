"""
search_ranking.py — food-search relevance ranking, used by the web backend.
Docs: README-numa-documentation.md

Ranks a candidate name against a multi-word query so that:
  1. More matching query words always outranks fewer (all terms > all-but-one > ...).
  2. Within an equal match count, matching the EARLIER query words outranks
     matching later ones — so "milk dry instant" ranks "milk dry" hits ahead
     of "milk instant" hits, since "instant" (the last word) is the one
     missing in the stronger result.
  3. Source (recipe/pantry/cache/external) breaks remaining ties — a real
     match always beats a weak or coincidental one, regardless of where it
     lives.
  A query word counts as present only at the START of a word in the name
  ("raw" matches "Raw" and "rawhide", not "stRAWberry"; "orange" still
  matches "Oranges"), via word_in_name(). Before 2026-10-26 any substring
  counted, so a recipe named "...strawberry..." matched "orange raw" and,
  with recipes then forced to the top of the local block, outranked
  "Oranges, raw, Florida".
  4. Among external (USDA/OFF) results tied on all of the above, USDA data
     quality breaks the tie: Foundation/SR Legacy (far more likely to carry
     real amino acid data) beats Survey/Experimental, which beats Branded/
     Open Food Facts. Without this, a wall of near-identical branded product
     names (all short, all matching every query word) can bury the one
     Foundation/SR Legacy food that actually has the data being searched
     for, since a bare text/length tiebreak has no way to prefer it.
"""
import re

SOURCE_RANK = {"recipe": 0, "pantry": 1, "cache": 2, "usda": 3, "off": 3}

DATA_TYPE_RANK = {
    "Foundation": 0, "SR Legacy": 0,
    "Survey (FNDDS)": 1, "Experimental": 1,
    "Branded": 2, "Open Food Facts": 2, "OFF": 2,
}


def _query_words(query: str) -> list[str]:
    return query.lower().split()


def _word_forms(word: str) -> list[str]:
    """`word` plus its plausible singular forms ("onions" -> "onion",
    "tomatoes" -> "tomato", "berries" -> "berry"), each kept to 3+
    characters so a short word ("as") can't shrink into a one-letter
    prefix that matches nearly everything — and, for a word ending in a
    consonant + "y", its "-ies" plural ("berry" -> "berries"), the one
    plural a singular word isn't already a prefix of ("onion" already
    begins "onions")."""
    forms = [word]
    if len(word) >= 3 and word.endswith("y") and word[-2] not in "aeiou":
        forms.append(word[:-1] + "ies")
    for suffix, repl in (("ies", "y"), ("es", ""), ("s", "")):
        if word.endswith(suffix):
            stem = word[: -len(suffix)] + repl
            if len(stem) >= 3 and stem not in forms:
                forms.append(stem)
    return forms


def word_in_name(word: str, name_lower: str) -> bool:
    """True if `word` (lowercase), or a singular form of it, begins a word in
    `name_lower`: found with no letter or digit just before it. A prefix
    match, so plurals and longer forms still count ("orange" in "oranges"),
    and a plural query word finds the singular name ("onions" in "Green
    onion" — added 2026-11-11, when a recipe matching only "green" tied
    with, and so outranked, that food for "green onions"), but a fragment
    inside another word does not ("raw" in "strawberry", "sauce" in
    "applesauce")."""
    return any(re.search(r"(?<![a-z0-9])" + re.escape(f), name_lower) is not None
               for f in _word_forms(word))


def _match_count_and_mask(name_lower: str, words: list[str]) -> tuple[int, int]:
    """Bit i (from the left, MSB = first query word) is set if words[i] is
    present in name_lower. Comparing masks as integers naturally prefers
    matches on earlier words when the match count is tied."""
    count = 0
    mask = 0
    n = len(words)
    for i, w in enumerate(words):
        if word_in_name(w, name_lower):
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
