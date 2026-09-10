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


# ---------------------------------------------------------------------------
# Print layout (full/half sheet) and paper size (Letter/A4) — global across
# all print pages (food/recipe/meal/day), unlike section choices which are
# per page type. These drive print.html's compact CSS and its @page size,
# so the browser's own print preview shows correct page breaks.
# ---------------------------------------------------------------------------

PRINT_LAYOUTS: dict[str, str] = {
    "full": "Full sheet",
    "half": "Half sheet",
}

PRINT_PAPERS: dict[str, str] = {
    "letter": "US Letter",
    "a4":     "A4",
}

# (layout, paper) -> CSS @page size value
PRINT_PAGE_SIZES: dict[tuple[str, str], str] = {
    ("full", "letter"): "8.5in 11in",
    ("full", "a4"):     "210mm 297mm",
    ("half", "letter"): "5.5in 8.5in",   # Half Letter / Statement
    ("half", "a4"):     "148mm 210mm",   # A5
}

# Print margin, in the same unit family as that paper's PRINT_PAGE_SIZES entry.
PRINT_PAGE_MARGINS: dict[str, str] = {
    "letter": "0.5in",
    "a4":     "12mm",
}


def resolve_layout(requested: str, submitted: bool, prefs: dict) -> str:
    if submitted and requested in PRINT_LAYOUTS:
        return requested
    saved = prefs.get("print_layout")
    return saved if saved in PRINT_LAYOUTS else "full"


def resolve_paper(requested: str, submitted: bool, prefs: dict) -> str:
    if submitted and requested in PRINT_PAPERS:
        return requested
    saved = prefs.get("print_paper")
    return saved if saved in PRINT_PAPERS else "letter"


def save_layout_prefs(layout: str, paper: str) -> dict:
    """Return the {"print_layout": ..., "print_paper": ...} update to pass to
    _save_prefs_file."""
    return {"print_layout": layout, "print_paper": paper}


def resolve_layout_context(layout: str, paper: str, layout_submitted: bool, prefs: dict) -> dict:
    """One-stop resolution for a print.html route: figures out the effective
    layout/paper (query params win when submitted, else saved prefs, else
    full/letter) and returns everything the template needs plus the prefs
    update to save (empty dict if nothing changed)."""
    layout = resolve_layout(layout, layout_submitted, prefs)
    paper = resolve_paper(paper, layout_submitted, prefs)
    return {
        "layout":           layout,
        "paper":            paper,
        "print_layouts":    PRINT_LAYOUTS,
        "print_papers":     PRINT_PAPERS,
        "page_css_size":    PRINT_PAGE_SIZES.get((layout, paper)),
        "page_css_margin":  PRINT_PAGE_MARGINS.get(paper, "0.5in"),
        "_save_update":     save_layout_prefs(layout, paper) if layout_submitted else {},
    }
