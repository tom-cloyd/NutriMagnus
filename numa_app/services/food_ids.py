"""
food_ids.py — food/recipe ID classification shared by export.py and the web app.
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


def classify_food_id(fdc_id: int | None, recipe_id: int | None = None) -> tuple[str, str] | None:
    """Return (id_str, source_label) for a food/recipe reference, or None if nothing to show.

    recipe_id takes priority (a recipe used as a meal item or nested ingredient
    has no fdc_id of its own). source_label is one of "Recipe", "USDA", one of
    _SYNTHETIC_ID_RANGES' labels ("OFF", "CNF", "CoFID", ...), or "User-drafted".
    """
    if recipe_id is not None:
        return str(recipe_id), "Recipe"
    if fdc_id is None:
        return None
    if fdc_id > 0:
        return str(fdc_id), "USDA"
    for _key, start, end, label in _SYNTHETIC_ID_RANGES:
        if start <= fdc_id <= end:
            return str(fdc_id), label
    return str(fdc_id), "User-drafted"
