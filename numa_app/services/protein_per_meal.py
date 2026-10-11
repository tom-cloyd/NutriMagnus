"""
protein_per_meal.py — how much protein one meal "should" carry, and whether a
meal reached it: the per-meal amount research associates with fully
stimulating muscle protein synthesis, personalised from the profile.

Sources (user-manual.md #protein-per-meal, footnotes there):
- ISSN position stand (Jäger et al. 2017): 0.25 g/kg of high-quality protein
  per serving (20-40 g absolute), 700-3000 mg leucine, every 3-4 h.
- Schoenfeld & Aragon 2018: 0.4 g/kg per meal over at least four meals to
  reach 1.6 g/kg/day (0.55 g/kg at the upper end).
- PROT-AGE (Bauer et al. 2013): older people need more per meal — about
  25-30 g with about 2.5-2.8 g leucine.
- Trommelen et al. 2023: no upper limit to how much one meal can be used, so
  a large meal is never flagged as "too much".

The meal's protein is compared as digestible complete protein (DCP) when
NuMa can work it out — the studies used high-quality protein, which is what
DCP measures — and as raw protein otherwise, labelled so. Reads only.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/protein_per_meal.py"; user-manual.md #protein-per-meal
"""

OLDER_ADULT_AGE = 65                 # PROT-AGE's "older people"
ADULT_G_PER_KG = (0.25, 0.40)        # ISSN 2017 lower; Schoenfeld & Aragon 2018 upper
OLDER_G = (25.0, 30.0)               # PROT-AGE 2013
GENERAL_G = (20.0, 40.0)             # ISSN 2017 absolute dose, when no profile is set
ADULT_LEUCINE_G = (0.7, 3.0)         # ISSN 2017
OLDER_LEUCINE_G = (2.5, 2.8)         # PROT-AGE 2013


def per_meal_amount(profile) -> dict:
    """{"low_g", "high_g", "leucine_low_g", "leucine_high_g", "basis"} for one
    meal. basis: "older" (65+), "adult" (scaled to body weight) or "general"
    (no profile: the absolute 20-40 g dose)."""
    if profile is None or not getattr(profile, "weight_kg", None):
        low, high = GENERAL_G
        return {"low_g": low, "high_g": high, "leucine_low_g": ADULT_LEUCINE_G[0],
                "leucine_high_g": ADULT_LEUCINE_G[1], "basis": "general"}
    if profile.age >= OLDER_ADULT_AGE:
        low, high = OLDER_G
        return {"low_g": low, "high_g": high, "leucine_low_g": OLDER_LEUCINE_G[0],
                "leucine_high_g": OLDER_LEUCINE_G[1], "basis": "older"}
    w = profile.weight_kg
    return {"low_g": round(ADULT_G_PER_KG[0] * w, 1), "high_g": round(ADULT_G_PER_KG[1] * w, 1),
            "leucine_low_g": ADULT_LEUCINE_G[0], "leucine_high_g": ADULT_LEUCINE_G[1],
            "basis": "adult"}


def meal_check(dcp_g: float | None, protein_g: float, leucine_g: float | None, amount: dict) -> dict:
    """One meal against amount (per_meal_amount()). {"protein_g", "is_dcp",
    "reached", "leucine_g", "leucine_reached"}: reached means the meal's DCP
    (or raw protein when DCP can't be worked out) is at least the low end.
    leucine_reached is None when the meal's foods carry no leucine figure."""
    is_dcp = dcp_g is not None
    value = dcp_g if is_dcp else (protein_g or 0.0)
    return {"protein_g": round(value, 1), "is_dcp": is_dcp,
            "reached": value >= amount["low_g"],
            "leucine_g": round(leucine_g, 2) if leucine_g else None,
            "leucine_reached": (leucine_g >= amount["leucine_low_g"]) if leucine_g else None}
