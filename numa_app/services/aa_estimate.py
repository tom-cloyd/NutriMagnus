"""
aa_estimate.py — estimate a food's amino acid profile by copying another
food's AA values, scaled to match its own protein content (CLI + web).

Raw AA grams don't transfer directly between foods with different protein
density — a food with 2x the protein of its source would otherwise end up
looking 2x more complete than it really is. Scaling by the target/source
protein_g ratio keeps the estimate honest, matching the manual convention
already used in this app's curated foods (e.g. "amino acids scaled from
USDA wet-okara FDC 172452 to dry basis").
Docs: README-numa-documentation.md, Architecture: "numa_app/services/aa_estimate.py — AA copy/estimate"
"""
from datetime import date

import usda as _usda


def estimate_aa(target_nutrients: dict, source_nutrients: dict) -> tuple[dict | None, float | None, str | None]:
    """Scale source_nutrients' AA values onto target_nutrients' protein content.

    Returns (updated_nutrients, scale_factor, error). On failure the first two
    are None and error explains why (no AA data on source, or no protein_g on
    either food to scale by). On success, updated_nutrients is target_nutrients
    with every ALL_AMINO_ACIDS key present in source_nutrients overwritten.
    """
    if not _usda.has_amino_acid_data(source_nutrients):
        return None, None, "Source food has no amino acid data to copy."
    target_protein = target_nutrients.get("protein_g") or 0.0
    source_protein = source_nutrients.get("protein_g") or 0.0
    if target_protein <= 0:
        return None, None, "Target food has no protein_g value to scale against."
    if source_protein <= 0:
        return None, None, "Source food has no protein_g value to scale from."

    factor = target_protein / source_protein
    updated = dict(target_nutrients)
    for key in _usda.ALL_AMINO_ACIDS:
        if key in source_nutrients:
            updated[key] = round(source_nutrients[key] * factor, 4)
    return updated, factor, None


def source_note(source_name: str, source_fdc_id: "int | None", factor: float) -> str:
    """Free-text note documenting where an AA estimate came from, matching
    the manual "Source: ... scaled from ..." convention used elsewhere."""
    id_part = f" (#{source_fdc_id})" if source_fdc_id else ""
    return (
        f"AA data estimated by scaling from {source_name}{id_part}, "
        f"factor {factor:.2f}x, {date.today().isoformat()}"
    )
