"""
food_ids.py — food/recipe ID classification used by the web app.
Docs: README-numa-documentation.md, Project Structure
"""

# Synthetic negative fdc_id ranges, one per external data source that doesn't
# use USDA's own positive FDC IDs. User-drafted foods live in (-1_000_000_000, 0)
# — see db.next_user_drafted_fdc_id() — so every reserved range here starts at
# or below -1_000_000_000 to avoid colliding with it. See user-manual.md
# Part 9, "Additional food nutrition database access", for the roadmap that
# introduced these one at a time (OFF/CNF live-API sources; CoFID/AFCD/CIQUAL
# static bundled-dataset sources).
#
# (key, range_start, range_end, label) — range is inclusive on both ends.
_SYNTHETIC_ID_RANGES: list[tuple[str, int, int, str]] = [
    ("off",   -3_000_000_000, -2_000_000_000, "OFF"),
    ("cnf",   -4_000_000_000, -3_000_000_000, "CNF"),
    ("cofid",  -5_000_000_000, -4_000_000_000, "CoFID"),
    ("afcd",   -6_000_000_000, -5_000_000_000, "AFCD"),
    ("ciqual", -7_000_000_000, -6_000_000_000, "CIQUAL"),
]


# Display-code prefix -> what it means, for footnotes/keys explaining codes.
CODE_PREFIXES: list[tuple[str, str]] = [
    ("U",      "USDA FoodData Central food"),
    ("UD",     "user-drafted food (one you entered yourself)"),
    ("R",      "recipe"),
    ("OFF",    "Open Food Facts product"),
    ("CNF",    "Canadian Nutrient File food"),
    ("CoFID",  "UK CoFID food"),
    ("AFCD",   "Australian AFCD food"),
    ("CIQUAL", "French CIQUAL food"),
]


def classify_food_id(fdc_id: int | None, recipe_id: int | None = None) -> tuple[str, str] | None:
    """Return (code, source_label) for a food/recipe reference, or None if nothing to show.

    code is the one short display code every food and recipe gets, in a
    single prefix+number pattern (see CODE_PREFIXES): U171477 (USDA), UD4
    (user-drafted), R21 (recipe), OFF3 / CNF1 / CoFID2 / AFCD1 / CIQUAL5
    (outside sources), and U171477.1 for an older version of a food kept at
    a Refresh (db.create_food_version). The stored ids behind them stay as
    they are; only the display changes:

    - user-drafted fdc_ids are -1, -2, -3, ... (db.next_user_drafted_fdc_id()),
      so UD<n> is n = -fdc_id;
    - outside-source fdc_ids are huge synthetic negatives (_SYNTHETIC_ID_RANGES)
      with no meaning to a reader, so they get a short per-source number from
      db.food_codes instead — or the bare prefix if the food was never cached.

    recipe_id takes priority (a recipe used as a meal item or nested ingredient
    has no fdc_id of its own). source_label is one of "Recipe", "USDA", one of
    _SYNTHETIC_ID_RANGES' labels ("OFF", "CNF", "CoFID", ...), or "User-drafted".
    """
    if recipe_id is not None:
        return f"R{recipe_id}", "Recipe"
    if fdc_id is None:
        return None
    if fdc_id > 0:
        return f"U{fdc_id}", "USDA"
    import db as _db
    if _db.is_version_id(fdc_id):
        # An older version kept at a Refresh (db.create_food_version):
        # its food's code plus ".n".
        info = _db.food_version_info(fdc_id)
        parent = classify_food_id(info["parent_fdc_id"]) if info else None
        return (f"{parent[0]}.{info['num']}" if parent else "V"), "Older version"
    for _key, start, end, label in _SYNTHETIC_ID_RANGES:
        if start <= fdc_id <= end:
            num = _db.food_code_num(fdc_id)
            return (f"{label}{num}" if num is not None else label), label
    return f"UD{-fdc_id}", "User-drafted"


def _split_version(code: str) -> tuple[str, int | None]:
    """"U171477.2" -> ("U171477", 2); a code with no ".n" -> (code, None)."""
    base, dot, ver = code.rpartition(".")
    if dot and base and ver.isdigit():
        return base, int(ver)
    return code, None


def code_source_name(code: str) -> str:
    """The plain-language meaning of a display code's prefix ("U171477" ->
    "USDA FoodData Central food"), for a hover title; "" if unrecognised."""
    code, ver = _split_version(code)
    if ver is not None:
        meaning = code_source_name(code)
        return f"older version of a {meaning}" if meaning else ""
    for prefix, meaning in sorted(CODE_PREFIXES, key=lambda p: -len(p[0])):
        rest = code[len(prefix):]
        if code.startswith(prefix) and (rest == "" or rest.isdigit()):
            return meaning
    return ""


def code_sort_key(code: str | None) -> tuple[int, int, int, str]:
    """Sort key for display codes: grouped by prefix in CODE_PREFIXES order,
    then numerically (so R9 sorts before R10), a food's older versions
    right after it. Blank codes sort last."""
    if not code:
        return (len(CODE_PREFIXES) + 1, 0, 0, "")
    base, ver = _split_version(code)
    for i, (prefix, _m) in sorted(enumerate(CODE_PREFIXES), key=lambda e: -len(e[1][0])):
        rest = base[len(prefix):]
        if base.startswith(prefix) and (rest == "" or rest.isdigit()):
            return (i, int(rest) if rest else 0, ver or 0, code)
    return (len(CODE_PREFIXES), 0, 0, code)


def parse_code(code: str) -> tuple[str, int]:
    """Turn a typed display code into ("food", fdc_id) or ("recipe", recipe_id).
    Case-insensitive, surrounding spaces ignored: "u171477", " R21", "OFF3".
    Raises ValueError with a user-readable message for anything else, or for
    an outside-source code no food has."""
    text = (code or "").strip()
    base, ver = _split_version(text)
    if ver is not None:
        kind, parent = parse_code(base)
        import db as _db
        vid = _db.food_version_id(parent, ver) if kind == "food" else None
        if vid is None:
            raise ValueError(f"{base} has no older version .{ver}.")
        return "food", vid
    upper = text.upper()
    for prefix, _m in sorted(CODE_PREFIXES, key=lambda p: -len(p[0])):
        rest = upper[len(prefix):]
        if upper.startswith(prefix.upper()) and rest.isdigit():
            n = int(rest)
            if prefix == "U":
                return "food", n
            if prefix == "UD":
                return "food", -n
            if prefix == "R":
                return "recipe", n
            import db as _db
            fdc_id = _db.food_code_fdc_id(prefix, n)
            if fdc_id is None:
                raise ValueError(f"No food has the code {prefix}{n}.")
            return "food", fdc_id
    raise ValueError(f'"{text}" is not a food or recipe code (examples: U171477, UD4, R21, OFF3, U171477.1).')
