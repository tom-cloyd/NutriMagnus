"""print_sections.py — shared vocabulary and prefs-aware resolution for the
"what to include" checkboxes on printable nutritional analyses.

Docs: README-numa-documentation.md, Print / export
"""

# Every section key any printable page can offer, in display/print order.
# Individual pages only expose the subset they actually have data for.
# nutrient_table/protein_summary/protein_quality/antinutrients/complements
# are shared across page types (food/recipe/meal/day) though the underlying
# data shape differs — print.html has a distinct render block per shape.
# The rest are specific to one or two page types.
PRINT_SECTION_LABELS: dict[str, str] = {
    "items":           "Foods & recipes in this meal",
    "meals_list":      "Meals breakdown",
    "introduction":     "Introduction",
    "ingredients":      "Ingredients",
    "procedure":        "Procedure",
    "nutrient_table":   "Nutrient table",
    "protein_summary":  "Protein summary (DCP)",
    "protein_quality":  "Protein quality (AA / DIAAS)",
    "glycemic_load":    "Glycemic load",
    "antinutrients":    "Anti-nutrients",
    "complements":      "Complement suggestions",
}


def resolve_sections(
    page_type: str,
    available: list[str],
    requested: list[str] | None,
    submitted: bool,
    prefs: dict,
) -> list[str]:
    """Pick which sections to render, in PRINT_SECTION_LABELS order.

    `requested` is whatever the print form actually submitted (an empty list
    means the user unchecked everything) — only trusted when `submitted` is
    True, since an empty checkbox list is otherwise indistinguishable from "no
    form submitted yet" (e.g. a direct link). Falls back to this page type's
    saved pref, then to all available sections.
    """
    available_set = set(available)
    if submitted:
        chosen = {k for k in (requested or []) if k in available_set}
    else:
        saved = prefs.get("print_sections", {}).get(page_type)
        chosen = {k for k in saved if k in available_set} if saved is not None else available_set
    return [k for k in PRINT_SECTION_LABELS if k in chosen]


def save_sections(page_type: str, chosen: list[str], prefs: dict) -> dict:
    """Return the {"print_sections": {...}} update to pass to _save_prefs_file."""
    by_page = dict(prefs.get("print_sections", {}))
    by_page[page_type] = chosen
    return {"print_sections": by_page}
