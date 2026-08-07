"""
diet_aware.py — diet-preference-aware analysis notes, used by the web backend
(web/backend.py) in the daily summary / RDA comparison views.

The stored diet_pref preference was previously consulted only to filter
protein complement suggestions; the iron/zinc RDA bump itself lives in
profile.compute_rda's diet_pref parameter — this module covers the
analysis-layer warnings that sit alongside that, which have no natural home
in profile.py since they produce user-facing text rather than numbers.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/diet_aware.py — diet-preference-aware analysis notes"
"""


def b12_deficiency_note(diet_pref: str, b12_pct_of_rda: float) -> str | None:
    """Return a warning note when a plant-based diet's logged B12 intake looks
    critically low, or None if not applicable.

    Vitamin B12 is almost entirely animal-sourced, so unlike most nutrients a
    persistently low reading on a plant-only diet points to a specific,
    well-known fix (a supplement or fortified food) rather than "eat more of
    the foods you're already eating." Scoped to plant_only only — vegetarians
    still have dairy and eggs as a B12 source, so an ordinary low-B12 day for
    that group is more likely just an off day, not a structural diet gap.

    The 50% cutoff is this app's own conservative warning trigger, not a
    cited clinical threshold — actual B12 deficiency is diagnosed by blood
    test, not logged dietary intake. See user-manual.md Notes [^7] for the
    (real, cited) claims this note does make: B12 is animal-only, and vegans
    should get it from fortified food or a supplement.
    """
    if diet_pref != "plant_only":
        return None
    if b12_pct_of_rda >= 50:
        return None
    return (
        "Vitamin B12 is almost entirely animal-sourced. On a plant-based diet, "
        "consistently low B12 usually means a supplement or fortified food is "
        "needed — diet alone rarely closes this gap."
    )


def iron_zinc_bioavailability_note(diet_pref: str) -> str | None:
    """Return an explanatory note when the iron/zinc RDA has been bumped for
    reduced dietary bioavailability, or None if diet_pref is "all".

    Pairs with profile.compute_rda's diet_pref parameter, which is what
    actually raises the targets — this just explains why to the user, since
    an RDA that silently changed from what they remember is confusing without it.
    """
    if diet_pref not in ("vegetarian", "plant_only"):
        return None
    return (
        "Iron and zinc targets are raised above the standard RDA on this diet "
        "setting: without heme iron (meat/fish/poultry), and with phytate in "
        "legumes and grains reducing zinc absorption, vegetarian and "
        "plant-based diets need more of both to absorb the same effective "
        "amount."
    )
