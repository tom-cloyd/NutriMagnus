"""
food_ids.py — food/recipe ID classification shared by export.py and the web app.
Docs: README-numa-documentation.md, Project Structure
"""

# Threshold separating Open Food Facts synthetic IDs from user-drafted negatives.
# OFF IDs are derived from barcodes via _OFF_ID_BASE = -2_000_000_000.
_OFF_ID_THRESHOLD = -1_000_000_000


def classify_food_id(fdc_id: int | None, recipe_id: int | None = None) -> tuple[str, str] | None:
    """Return (id_str, source_label) for a food/recipe reference, or None if nothing to show.

    recipe_id takes priority (a recipe used as a meal item or nested ingredient
    has no fdc_id of its own). source_label is one of "Recipe", "USDA", "OFF",
    "User-drafted".
    """
    if recipe_id is not None:
        return str(recipe_id), "Recipe"
    if fdc_id is None:
        return None
    if fdc_id > 0:
        return str(fdc_id), "USDA"
    if fdc_id <= _OFF_ID_THRESHOLD:
        return str(fdc_id), "OFF"
    return str(fdc_id), "User-drafted"
