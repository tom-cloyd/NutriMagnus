"""
usda_nutrients.py — nutrient math, protein analysis, complement suggestions,
DIAAS scoring, anti-nutrient flags, and density lookup for numa.

Called via usda.py which re-exports everything as usda.<name>.
Docs: README-numa-documentation.md, Architecture: "usda_nutrients.py — nutrient math and data tables"
"""
import re

from usda_api import NUTRIENT_MAP, ESSENTIAL_AMINO_ACIDS, AA_REFERENCE_MG_PER_G_PROTEIN

# Type alias for all per-100g nutrient dicts throughout the codebase.
Nutrients = dict[str, float]

# FAO 2013 specifies Met+Cys and Phe+Tyr as combined pairs.  The reference
# values in AA_REFERENCE_MG_PER_G_PROTEIN are for the combined pair, so we
# must sum both members before scoring against the reference.
_AA_PAIRS: dict[str, str] = {
    "aa_methionine_g":    "aa_cystine_g",   # Met+Cys combined reference = 22 mg/g
    "aa_phenylalanine_g": "aa_tyrosine_g",  # Phe+Tyr combined reference = 38 mg/g
}

# AAs scoring above this threshold are considered adequate; gaps below it are
# too small to generate practical complement suggestions (e.g. score=0.994 → 1g).
_MIN_GAP_SCORE: float = 0.95


def scale_nutrients(nutrients: Nutrients, amount: float,
                    base_size: float = 100.0) -> Nutrients:
    """
    Scale a nutrient dict from base_size grams to amount grams.
    USDA data is always per 100g unless a serving size is specified.
    Pass base_size=serving_size if you want to scale from per-serving data.
    """
    ratio = amount / base_size
    return {k: v * ratio for k, v in nutrients.items()}


def sum_nutrients(*nutrient_dicts: Nutrients) -> Nutrients:
    """Add together multiple nutrient dicts."""
    total: dict[str, float] = {}
    for nd in nutrient_dicts:
        for key, val in nd.items():
            total[key] = total.get(key, 0.0) + val
    return total


def has_amino_acid_data(nutrients: Nutrients) -> bool:
    """Return True if the nutrients dict contains sufficient amino acid data."""
    if nutrients.get("protein_g", 0) <= 0:
        return True   # no protein — AA data irrelevant
    aa_present = [k for k in ESSENTIAL_AMINO_ACIDS if nutrients.get(k, 0) > 0]
    return len(aa_present) >= 5


def protein_completeness(nutrients: Nutrients, digestibility: float = 1.0) -> dict:
    """
    Assess protein completeness based on essential amino acid profile.

    digestibility: overall protein digestibility factor (e.g. DIAAS score).
        Applied to scores before determining complete/limiting_aa so the
        classification reflects bioavailable amino acids, not just raw content.
        Scores in the returned dict are always raw (pre-digestibility) for display.

    Returns a dict with:
        has_data     bool — True if amino acid data is present
        complete     bool — True if all digestibility-adjusted AA scores ≥ 1.0
        limiting_aa  str | None — name of the most limiting (digestibility-adjusted) AA
        scores       dict — AA key → raw score vs. reference (1.0 = meets reference)
    """
    protein_g = nutrients.get("protein_g", 0)
    if protein_g <= 0:
        return {"has_data": False, "complete": False, "limiting_aa": None, "scores": {}}

    aa_present = [k for k in ESSENTIAL_AMINO_ACIDS if nutrients.get(k, 0) > 0]
    if len(aa_present) < 5:   # not enough AA data with non-zero values
        return {"has_data": False, "complete": False, "limiting_aa": None, "scores": {}}

    scores = {}
    for aa_key in ESSENTIAL_AMINO_ACIDS:
        if aa_key not in nutrients:
            continue
        # Combine paired AAs per FAO 2013 (Met+Cys, Phe+Tyr) before scoring.
        aa_val = nutrients[aa_key]
        if aa_key in _AA_PAIRS:
            aa_val = aa_val + nutrients.get(_AA_PAIRS[aa_key], 0.0)
        aa_mg_per_g_protein = (aa_val / protein_g) * 1000
        ref = AA_REFERENCE_MG_PER_G_PROTEIN.get(aa_key, 1)
        scores[aa_key] = aa_mg_per_g_protein / ref

    if not scores:
        return {"has_data": False, "complete": False, "limiting_aa": None, "scores": {}}

    # Apply digestibility for completeness determination; keep raw scores for display.
    adj = {k: v * digestibility for k, v in scores.items()}
    limiting = min(adj, key=lambda k: adj[k])
    complete = all(v >= 1.0 for v in adj.values())

    return {
        "has_data":    True,
        "complete":    complete,
        "limiting_aa": limiting,
        "scores":      scores,
    }


def nutrient_label(key: str) -> tuple[str, str]:
    """Return (display_name, unit) for a nutrient key, or (key, '') if unknown."""
    for nid, (k, label, unit) in NUTRIENT_MAP.items():
        if k == key:
            return label, unit
    return key, ""


def get_aa_gaps(nutrients: Nutrients, digestibility: float = 1.0) -> list[tuple[str, float, float]]:
    """
    Return (aa_key, score, deficit_g) for each essential AA below score 1.0
    after applying digestibility, sorted by score ascending (most limiting first).
    deficit_g is the additional grams of that AA (raw) needed to reach score 1.0.
    Returns [] if protein data is missing or insufficient.
    """
    protein_g = nutrients.get("protein_g", 0)
    if protein_g <= 0:
        return []
    gaps = []
    for aa_key in ESSENTIAL_AMINO_ACIDS:
        if aa_key not in nutrients:
            continue
        ref = AA_REFERENCE_MG_PER_G_PROTEIN[aa_key]
        aa_val = nutrients[aa_key]
        if aa_key in _AA_PAIRS:
            aa_val = aa_val + nutrients.get(_AA_PAIRS[aa_key], 0.0)
        aa_mg_per_g = (aa_val / protein_g) * 1000
        score = (aa_mg_per_g / ref) * digestibility
        if score < _MIN_GAP_SCORE:
            # Target raw AA needed so that digestible amount meets reference.
            target_g = ref * protein_g / 1000 / digestibility
            deficit_g = target_g - aa_val
            gaps.append((aa_key, score, deficit_g))
    return sorted(gaps, key=lambda x: x[1])


# ---------------------------------------------------------------------------
# Curated complement table — per-100g nutrient profiles for common plant
# protein sources.  Used when a pantry food has no USDA cache entry, and as
# the general-suggestion fallback when pantry coverage is insufficient.
# Values from USDA FDC Foundation / SR Legacy datasets.
# ---------------------------------------------------------------------------

_COMPLEMENT_TABLE: list[dict] = [
    # ---- Plant sources ----
    {
        "name": "Lentils, cooked",
        "animal": False,
        "diaas": 0.75,
        "nutrients": {
            # Source: USDA SR Legacy FDC 172421
            "protein_g":        9.02,
            "aa_tryptophan_g":  0.077, "aa_threonine_g":   0.355,
            "aa_isoleucine_g":  0.374, "aa_leucine_g":     0.636,
            "aa_lysine_g":      0.624, "aa_methionine_g":  0.077, "aa_cystine_g": 0.089,
            "aa_phenylalanine_g": 0.450, "aa_valine_g":    0.432,
            "aa_histidine_g":   0.254,
        },
    },
    {
        "name": "Chickpeas, cooked",
        "animal": False,
        "diaas": 0.83,
        "nutrients": {
            # Source: USDA SR Legacy FDC 173756
            "protein_g":        8.86,
            "aa_tryptophan_g":  0.079, "aa_threonine_g":   0.337,
            "aa_isoleucine_g":  0.383, "aa_leucine_g":     0.623,
            "aa_lysine_g":      0.519, "aa_methionine_g":  0.086, "aa_cystine_g": 0.107,
            "aa_phenylalanine_g": 0.471, "aa_valine_g":    0.377,
            "aa_histidine_g":   0.239,
        },
    },
    {
        "name": "Black beans, cooked",
        "animal": False,
        "diaas": 0.75,
        "nutrients": {
            # Source: USDA SR Legacy FDC 175236
            "protein_g":        8.86,
            "aa_tryptophan_g":  0.099, "aa_threonine_g":   0.355,
            "aa_isoleucine_g":  0.376, "aa_leucine_g":     0.677,
            "aa_lysine_g":      0.535, "aa_methionine_g":  0.117, "aa_cystine_g": 0.111,
            "aa_phenylalanine_g": 0.473, "aa_valine_g":    0.452,
            "aa_histidine_g":   0.264,
        },
    },
    {
        "name": "Kidney beans, cooked",
        "animal": False,
        "diaas": 0.75,
        "nutrients": {
            # Source: USDA SR Legacy FDC 175200 (pinto used as proxy; kidney similar)
            "protein_g":        8.67,
            "aa_tryptophan_g":  0.096, "aa_threonine_g":   0.366,
            "aa_isoleucine_g":  0.406, "aa_leucine_g":     0.700,
            "aa_lysine_g":      0.598, "aa_methionine_g":  0.111, "aa_cystine_g": 0.107,
            "aa_phenylalanine_g": 0.490, "aa_valine_g":    0.467,
            "aa_histidine_g":   0.276,
        },
    },
    {
        "name": "Tofu, firm",
        "animal": False,
        "diaas": 0.84,
        "nutrients": {
            # Source: USDA SR Legacy FDC 172479
            "protein_g":        8.08,
            "aa_tryptophan_g":  0.121, "aa_threonine_g":   0.321,
            "aa_isoleucine_g":  0.434, "aa_leucine_g":     0.652,
            "aa_lysine_g":      0.550, "aa_methionine_g":  0.103, "aa_cystine_g": 0.079,
            "aa_phenylalanine_g": 0.393, "aa_valine_g":    0.407,
            "aa_histidine_g":   0.231,
        },
    },
    {
        "name": "Tempeh",
        "animal": False,
        "diaas": 0.87,
        "nutrients": {
            # Source: USDA SR Legacy FDC 168190
            "protein_g":        20.29,
            "aa_tryptophan_g":  0.287, "aa_threonine_g":   0.861,
            "aa_isoleucine_g":  1.013, "aa_leucine_g":     1.545,
            "aa_lysine_g":      1.171, "aa_methionine_g":  0.274, "aa_cystine_g": 0.222,
            "aa_phenylalanine_g": 1.052, "aa_valine_g":    1.073,
            "aa_histidine_g":   0.582,
        },
    },
    {
        "name": "Edamame, cooked",
        "animal": False,
        "diaas": 0.84,
        "nutrients": {
            # Source: USDA SR Legacy FDC 168411
            "protein_g":        11.91,
            "aa_tryptophan_g":  0.156, "aa_threonine_g":   0.477,
            "aa_isoleucine_g":  0.534, "aa_leucine_g":     0.911,
            "aa_lysine_g":      0.782, "aa_methionine_g":  0.135, "aa_cystine_g": 0.163,
            "aa_phenylalanine_g": 0.580, "aa_valine_g":    0.559,
            "aa_histidine_g":   0.321,
        },
    },
    {
        "name": "Peas, green, cooked",
        "animal": False,
        "diaas": 0.79,
        "nutrients": {
            # Source: USDA SR Legacy FDC 170420
            "protein_g":        5.36,
            "aa_tryptophan_g":  0.050, "aa_threonine_g":   0.213,
            "aa_isoleucine_g":  0.238, "aa_leucine_g":     0.370,
            "aa_lysine_g":      0.305, "aa_methionine_g":  0.082, "aa_cystine_g": 0.037,
            "aa_phenylalanine_g": 0.253, "aa_valine_g":    0.264,
            "aa_histidine_g":   0.117,
        },
    },
    {
        "name": "Quinoa, cooked",
        "animal": False,
        "diaas": 0.85,
        "nutrients": {
            # Source: USDA SR Legacy FDC 168917
            "protein_g":        4.40,
            "aa_tryptophan_g":  0.052, "aa_threonine_g":   0.121,
            "aa_isoleucine_g":  0.152, "aa_leucine_g":     0.257,
            "aa_lysine_g":      0.233, "aa_methionine_g":  0.086, "aa_cystine_g": 0.049,
            "aa_phenylalanine_g": 0.180, "aa_valine_g":    0.175,
            "aa_histidine_g":   0.113,
        },
    },
    {
        "name": "Amaranth, cooked",
        "animal": False,
        "diaas": 0.76,
        "nutrients": {
            # Source: USDA SR Legacy FDC 170285
            "protein_g":        3.80,
            "aa_tryptophan_g":  0.056, "aa_threonine_g":   0.104,
            "aa_isoleucine_g":  0.131, "aa_leucine_g":     0.237,
            "aa_lysine_g":      0.213, "aa_methionine_g":  0.060, "aa_cystine_g": 0.039,
            "aa_phenylalanine_g": 0.148, "aa_valine_g":    0.163,
            "aa_histidine_g":   0.097,
        },
    },
    {
        "name": "Hemp seeds",
        "animal": False,
        "diaas": 0.63,
        "nutrients": {
            # Source: USDA SR Legacy FDC 170148 — hulled (shelled) hemp seeds
            "protein_g":        31.56,
            "aa_tryptophan_g":  0.490, "aa_threonine_g":   1.190,
            "aa_isoleucine_g":  1.430, "aa_leucine_g":     2.160,
            "aa_lysine_g":      0.960, "aa_methionine_g":  0.960, "aa_cystine_g": 0.480,
            "aa_phenylalanine_g": 1.440, "aa_valine_g":    1.780,
            "aa_histidine_g":   0.870,
        },
    },
    {
        "name": "Sesame seeds",
        "animal": False,
        # DIAAS ~0.44: lysine is limiting (34 mg/g vs 45 mg/g reference); digestibility ~0.91
        # Source: USDA SR Legacy FDC 12023 — Seeds, sesame seeds, whole, dried
        "diaas": 0.44,
        "nutrients": {
            "protein_g":        17.73,
            "aa_tryptophan_g":  0.330, "aa_threonine_g":   0.736,
            "aa_isoleucine_g":  0.762, "aa_leucine_g":     1.299,
            "aa_lysine_g":      0.570, "aa_methionine_g":  0.586, "aa_cystine_g": 0.295,
            "aa_phenylalanine_g": 0.940, "aa_valine_g":    0.982,
            "aa_histidine_g":   0.482,
        },
    },
    {
        "name": "Brazil nuts",
        "animal": False,
        # DIAAS ~0.54: lysine is limiting (34 mg/g vs 45 mg/g reference); digestibility ~0.87
        # Met+Cys/protein ratio ~94 mg/g — highest of any common food.
        # Source: USDA SR Legacy FDC 12078 — Nuts, brazilnuts, dried, unblanched
        "diaas": 0.54,
        "nutrients": {
            "protein_g":        14.32,
            "aa_tryptophan_g":  0.141, "aa_threonine_g":   0.362,
            "aa_isoleucine_g":  0.516, "aa_leucine_g":     1.155,
            "aa_lysine_g":      0.492, "aa_methionine_g":  1.008, "aa_cystine_g": 0.342,
            "aa_phenylalanine_g": 0.630, "aa_valine_g":    0.756,
            "aa_histidine_g":   0.386,
        },
    },
    {
        "name": "Pumpkin seeds",
        "animal": False,
        "diaas": 0.64,
        "nutrients": {
            # Source: USDA SR Legacy FDC 12014 — Seeds, pumpkin and squash seed kernels, roasted
            "protein_g":        24.54,
            "aa_tryptophan_g":  0.330, "aa_threonine_g":   0.801,
            "aa_isoleucine_g":  1.239, "aa_leucine_g":     2.408,
            "aa_lysine_g":      0.979, "aa_methionine_g":  0.528, "aa_cystine_g": 0.305,
            "aa_phenylalanine_g": 1.558, "aa_valine_g":    1.539,
            "aa_histidine_g":   0.745,
        },
    },
    {
        "name": "Sunflower seeds",
        "animal": False,
        "diaas": 0.53,
        "nutrients": {
            # Source: USDA SR Legacy FDC 12036 — Seeds, sunflower seed kernels, dried
            "protein_g":        19.33,
            "aa_tryptophan_g":  0.294, "aa_threonine_g":   0.892,
            "aa_isoleucine_g":  0.883, "aa_leucine_g":     1.434,
            "aa_lysine_g":      0.728, "aa_methionine_g":  0.430, "aa_cystine_g": 0.327,
            "aa_phenylalanine_g": 0.988, "aa_valine_g":    1.022,
            "aa_histidine_g":   0.510,
        },
    },
    {
        "name": "Oats",
        "animal": False,
        "diaas": 0.57,
        "nutrients": {
            # Source: USDA SR Legacy FDC 173904 — Cereals, oats, regular and quick, not fortified, dry
            "protein_g":        13.15,
            "aa_tryptophan_g":  0.182, "aa_threonine_g":   0.382,
            "aa_isoleucine_g":  0.503, "aa_leucine_g":     0.980,
            "aa_lysine_g":      0.637, "aa_methionine_g":  0.207, "aa_cystine_g": 0.321,
            "aa_phenylalanine_g": 0.665, "aa_valine_g":    0.688,
            "aa_histidine_g":   0.275,
        },
    },
    {
        "name": "Nutritional yeast",
        "animal": False,
        "diaas": 0.72,
        "nutrients": {
            # Cystine estimate from amino acid composition studies (DIAAS data sparse)
            "protein_g":        52.00,
            "aa_tryptophan_g":  0.660, "aa_threonine_g":   2.460,
            "aa_isoleucine_g":  2.520, "aa_leucine_g":     3.600,
            "aa_lysine_g":      3.110, "aa_methionine_g":  0.860, "aa_cystine_g": 0.240,
            "aa_phenylalanine_g": 2.000, "aa_valine_g":    2.770,
            "aa_histidine_g":   1.180,
        },
    },
    {
        "name": "Soy protein isolate",
        "animal": False,
        "diaas": 0.97,
        "nutrients": {
            # Source: USDA SR Legacy FDC 174276 — Soy protein isolate
            "protein_g":        86.04,
            "aa_tryptophan_g":  1.143, "aa_threonine_g":   3.579,
            "aa_isoleucine_g":  4.382, "aa_leucine_g":     7.133,
            "aa_lysine_g":      5.379, "aa_methionine_g":  1.145, "aa_cystine_g": 0.833,
            "aa_phenylalanine_g": 4.870, "aa_valine_g":    4.487,
            "aa_histidine_g":   2.425,
        },
    },
    {
        "name": "Pea protein powder",
        "animal": False,
        "diaas": 0.82,
        "nutrients": {
            # Cystine estimate for commercial pea protein isolate (~80% protein)
            "protein_g":        80.00,
            "aa_tryptophan_g":  0.730, "aa_threonine_g":   2.700,
            "aa_isoleucine_g":  3.440, "aa_leucine_g":     5.950,
            "aa_lysine_g":      5.360, "aa_methionine_g":  0.930, "aa_cystine_g": 0.600,
            "aa_phenylalanine_g": 3.760, "aa_valine_g":    3.630,
            "aa_histidine_g":   1.550,
        },
    },
    # ---- Animal sources ----
    # dairy_egg=True: allowed for vegetarians. meat/fish entries have animal=True only.
    {
        "name": "Egg, whole, cooked",
        "animal": True,
        "dairy_egg": True,
        "diaas": 1.13,
        "nutrients": {
            # Source: USDA SR Legacy FDC 173424
            "protein_g":        12.56,
            "aa_tryptophan_g":  0.153, "aa_threonine_g":   0.556,
            "aa_isoleucine_g":  0.671, "aa_leucine_g":     1.086,
            "aa_lysine_g":      0.904, "aa_methionine_g":  0.392, "aa_cystine_g": 0.292,
            "aa_phenylalanine_g": 0.668, "aa_valine_g":    0.858,
            "aa_histidine_g":   0.298,
        },
    },
    {
        "name": "Cheese, cheddar",
        "animal": True,
        "dairy_egg": True,
        "diaas": 1.08,
        "nutrients": {
            # Source: USDA SR Legacy FDC 171241
            "protein_g":        24.90,
            "aa_tryptophan_g":  0.320, "aa_threonine_g":   0.880,
            "aa_isoleucine_g":  1.220, "aa_leucine_g":     2.380,
            "aa_lysine_g":      1.850, "aa_methionine_g":  0.650, "aa_cystine_g": 0.096,
            "aa_phenylalanine_g": 1.280, "aa_valine_g":    1.600,
            "aa_histidine_g":   0.720,
        },
    },
    {
        "name": "Greek yogurt, plain",
        "animal": True,
        "dairy_egg": True,
        "diaas": 1.14,
        "nutrients": {
            # Source: USDA SR Legacy FDC 170903
            "protein_g":        9.95,
            "aa_tryptophan_g":  0.049, "aa_threonine_g":   0.338,
            "aa_isoleucine_g":  0.456, "aa_leucine_g":     0.785,
            "aa_lysine_g":      0.699, "aa_methionine_g":  0.253, "aa_cystine_g": 0.028,
            "aa_phenylalanine_g": 0.408, "aa_valine_g":    0.560,
            "aa_histidine_g":   0.230,
        },
    },
    {
        "name": "Whey protein powder",
        "animal": True,
        "dairy_egg": True,
        "diaas": 1.09,
        "nutrients": {
            # Source: USDA SR Legacy FDC 173218 (whey protein concentrate, ~78g protein)
            "protein_g":        78.00,
            "aa_tryptophan_g":  1.680, "aa_threonine_g":   5.800,
            "aa_isoleucine_g":  5.900, "aa_leucine_g":    10.100,
            "aa_lysine_g":      8.900, "aa_methionine_g":  2.250, "aa_cystine_g": 1.670,
            "aa_phenylalanine_g": 3.100, "aa_valine_g":    5.300,
            "aa_histidine_g":   1.700,
        },
    },
    {
        "name": "Chicken breast, cooked",
        "animal": True,
        "diaas": 1.08,
        "nutrients": {
            # Source: USDA SR Legacy FDC 171477
            "protein_g":        31.02,
            "aa_tryptophan_g":  0.365, "aa_threonine_g":   1.326,
            "aa_isoleucine_g":  1.452, "aa_leucine_g":     2.476,
            "aa_lysine_g":      2.778, "aa_methionine_g":  0.740, "aa_cystine_g": 0.322,
            "aa_phenylalanine_g": 1.277, "aa_valine_g":    1.566,
            "aa_histidine_g":   0.942,
        },
    },
    {
        "name": "Salmon, cooked",
        "animal": True,
        "diaas": 1.00,
        "nutrients": {
            # Source: USDA SR Legacy FDC 175168
            "protein_g":        25.44,
            "aa_tryptophan_g":  0.285, "aa_threonine_g":   1.115,
            "aa_isoleucine_g":  1.159, "aa_leucine_g":     2.054,
            "aa_lysine_g":      2.338, "aa_methionine_g":  0.800, "aa_cystine_g": 0.300,
            "aa_phenylalanine_g": 0.990, "aa_valine_g":    1.312,
            "aa_histidine_g":   0.757,
        },
    },
]

# Index for fast keyword lookup of complement table entries
_COMPLEMENT_INDEX: dict[str, dict] = {c["name"].lower(): c for c in _COMPLEMENT_TABLE}


def _find_complement_by_name(food_name: str) -> dict | None:
    """Match a food name against the complement table by keyword, return entry or None."""
    name_lower = food_name.lower()
    # Exact match first
    if name_lower in _COMPLEMENT_INDEX:
        return _COMPLEMENT_INDEX[name_lower]
    # Keyword substring match
    for entry_name, entry in _COMPLEMENT_INDEX.items():
        # Use first word of entry name as a keyword
        primary_kw = entry_name.split(",")[0].strip()
        if primary_kw in name_lower or name_lower in primary_kw:
            return entry
    return None


def get_complement_nutrients(food_name: str) -> Nutrients | None:
    """
    Return the nutrient profile from the complement table for a food name,
    or None if not found. Used as a fallback when USDA cache lacks AA data.
    """
    entry = _find_complement_by_name(food_name)
    return entry["nutrients"] if entry else None


def suggest_complements(
    base_nutrients: Nutrients,
    pantry_candidates: list[dict],
    diet_pref: str = "all",
    base_digestibility: float = 1.0,
    base_food_name: str | None = None,
) -> dict[str, list[dict]]:
    """
    Suggest complement foods to close essential amino acid gaps.

    pantry_candidates: list of dicts, each with:
        "name": str
        "nutrients": dict | None   (per-100g; None if not in USDA cache)
        "diaas": float | None
    diet_pref: "all" includes all sources; "vegetarian" allows dairy/eggs but not
        meat/fish; "plant_only" excludes all animal-sourced entries.
    base_food_name: used to look up true ileal digestibility for DIAAS-improver
        calculations; falls back to base_digestibility if None.

    Returns {"pantry": [...], "general": [...], "diaas_improvers": [...]}
    Gap-closer dicts contain:
        name, grams, new_scores, new_complete, gaps_closed,
        remaining_gaps, protein_added, digestible_protein_added, diaas
    DIAAS-improver dicts contain:
        name, grams, current_diaas, new_diaas,
        protein_added, digestible_protein_added, diaas
    """
    gaps = get_aa_gaps(base_nutrients, digestibility=base_digestibility)
    if not gaps:
        return {"pantry": [], "general": [], "diaas_improvers": []}

    primary_aa, _primary_score, primary_deficit_g = gaps[0]

    # True ileal digestibility for the base food (separate from DIAAS score).
    # Used only for the DIAAS-improver tier which mirrors diaas.meal_level_diaas().
    from diaas import FAO_REFERENCE as _FAO_REF, _IAA_PAIRS as _DIAAS_PAIRS
    from diaas import get_digestibility as _get_dig
    if base_food_name:
        base_tid, _ = _get_dig(base_food_name)
    else:
        base_tid = base_digestibility  # DIAAS used as TID proxy when name unavailable

    def _score_candidate(nutrients_100g: dict, diaas: float | None,
                         target_aa: str) -> dict | None:
        """
        Compute suggestion metrics for one candidate targeting a specific AA gap.
        Returns None if the candidate cannot improve that gap.

        Solving for grams X that brings target AA score to exactly 1.0:
            (base_aa + alpha*X) / (base_protein + beta*X) = R
        where alpha = cand_aa/100, beta = cand_protein/100, R = reference ratio.
        Rearranging: X = (R*base_protein - base_aa) / (alpha - R*beta)
        This is valid only when alpha > R*beta (candidate AA/protein > reference).
        """
        # Use combined AA values for paired AAs (Met+Cys, Phe+Tyr) per FAO 2013.
        if target_aa in _AA_PAIRS:
            pair_key = _AA_PAIRS[target_aa]
            alpha = (nutrients_100g.get(target_aa, 0.0) + nutrients_100g.get(pair_key, 0.0)) / 100.0
        else:
            alpha = nutrients_100g.get(target_aa, 0.0) / 100.0   # g AA per g food
        beta = nutrients_100g.get("protein_g", 0.0) / 100.0  # g protein per g food
        # Use digestibility-adjusted reference so that the sizing is consistent
        # with get_aa_gaps(), which uses the same adjustment to detect gaps.
        # Without this, a food whose raw ratio meets the reference but whose
        # digestibility-adjusted score is below 1.0 would compute grams ≈ 0
        # and no complement would qualify.
        R = AA_REFERENCE_MG_PER_G_PROTEIN[target_aa] / 1000.0 / max(base_digestibility, 0.01)
        denom = alpha - R * beta
        if denom <= 0:
            # Candidate's AA/protein ratio is below the (digestibility-adjusted)
            # reference — adding it won't close the gap (may worsen it).
            return None
        if target_aa in _AA_PAIRS:
            base_aa = base_nutrients.get(target_aa, 0.0) + base_nutrients.get(_AA_PAIRS[target_aa], 0.0)
        else:
            base_aa = base_nutrients.get(target_aa, 0.0)
        base_protein = base_nutrients.get("protein_g", 0.0)
        grams = (R * base_protein - base_aa) / denom
        # Cap at 500g: excludes mathematically valid but wholly impractical suggestions.
        if grams <= 0 or grams > 500:
            return None
        added = scale_nutrients(nutrients_100g, grams)
        combined = sum_nutrients(base_nutrients, added)
        new_pc = protein_completeness(combined, digestibility=base_digestibility)
        new_gaps = get_aa_gaps(combined, digestibility=base_digestibility)
        gaps_closed = len(gaps) - len(new_gaps)
        # Require that the targeted AA gap is actually closed.
        # We allow suggestions where a different gap opens, since the user can
        # layer complements — but the targeted AA must improve.
        target_still_gapped = any(aa == target_aa for aa, _, _ in new_gaps)
        if target_still_gapped:
            return None
        # Detect when this complement closes the target gap but opens a gap in
        # a different AA that was not previously limiting (e.g. Brazil nuts
        # close Met+Cys but dilute lysine enough to open a new gap there).
        original_gap_set = {aa for aa, _, _ in gaps}
        new_gap_set = {aa for aa, _, _ in new_gaps}
        opens_new_gap = bool(new_gap_set - original_gap_set)
        closes_primary = (target_aa == gaps[0][0])
        protein_added = nutrients_100g.get("protein_g", 0) * grams / 100
        dig_added = protein_added * (diaas if diaas is not None else 1.0)
        return {
            "grams":                    round(grams),
            "new_scores":               new_pc.get("scores", {}),
            "new_complete":             new_pc.get("complete", False),
            "gaps_closed":              gaps_closed,
            "opens_new_gap":            opens_new_gap,
            "closes_primary":           closes_primary,
            "remaining_gaps":           len(new_gaps),
            "protein_added":            protein_added,
            "digestible_protein_added": dig_added,
            "diaas":                    diaas,
        }

    def _diaas_improver_score(
        comp_nutrients: dict,
        comp_name: str,
        comp_diaas_val: float | None,
        target: float = 0.90,
    ) -> dict | None:
        """
        Find the smallest practical serving of comp that meaningfully improves the
        combined pooled DIAAS (base + complement), using numerical search.

        Uses pooled DIAAS methodology (consistent with diaas.meal_level_diaas):
          pooled_dig_aa_k = base_aa_k * base_tid + comp_aa_k/100 * X * d_comp
          ratio_k(X) = pooled_dig_aa_k / (FAO_ref_k/1000 * (base_protein + comp_protein/100 * X))
          DIAAS(X) = min_k(ratio_k(X))

        The analytical formula can only solve for AAs where the complement's
        digestibility-weighted AA/protein ratio exceeds the target threshold.  Foods
        like nutritional yeast are strong in most AAs but weak in Met+Cys — they
        can still meaningfully raise DIAAS even though they can't analytically close
        every gap.  The numerical approach handles that correctly.

        Returns None if improvement < 0.05 DIAAS points or best X > 300g.
        """
        base_protein = base_nutrients.get("protein_g", 0.0)
        comp_protein = comp_nutrients.get("protein_g", 0.0)
        if base_protein <= 0 or comp_protein <= 0:
            return None

        d_comp, _ = _get_dig(comp_name)
        P = base_protein
        Q = comp_protein / 100.0  # raw protein per gram of complement

        def _pooled_diaas(X: float) -> float:
            new_protein = P + Q * X
            ratios: dict[str, float] = {}
            for aa_key, ref_mg_per_g in _FAO_REF.items():
                secondary = _DIAAS_PAIRS.get(aa_key)
                base_aa = base_nutrients.get(aa_key, 0.0)
                if secondary:
                    base_aa += base_nutrients.get(secondary, 0.0)
                comp_aa = comp_nutrients.get(aa_key, 0.0)
                if secondary:
                    comp_aa += comp_nutrients.get(secondary, 0.0)
                if base_aa <= 0 and comp_aa <= 0:
                    continue
                pooled = base_aa * base_tid + comp_aa / 100.0 * X * d_comp
                ref_g = ref_mg_per_g / 1000.0 * new_protein
                if ref_g > 0:
                    ratios[aa_key] = pooled / ref_g
            return min(ratios.values()) if ratios else 0.0

        current_diaas_val = _pooled_diaas(0.0)
        if current_diaas_val >= target:
            return None  # base already meets target

        # Collect analytical candidate X values for AAs where denom > 0.
        candidate_X: list[float] = []
        for aa_key, ref_mg_per_g in _FAO_REF.items():
            secondary = _DIAAS_PAIRS.get(aa_key)
            base_aa = base_nutrients.get(aa_key, 0.0)
            if secondary:
                base_aa += base_nutrients.get(secondary, 0.0)
            if base_aa <= 0:
                continue
            comp_aa = comp_nutrients.get(aa_key, 0.0)
            if secondary:
                comp_aa += comp_nutrients.get(secondary, 0.0)
            A_k = base_aa * base_tid
            C_k = comp_aa / 100.0 * d_comp
            R_t_k = target * ref_mg_per_g / 1000.0
            ref_g = ref_mg_per_g / 1000.0 * P
            if ref_g <= 0 or A_k / ref_g >= target:
                continue  # already meets target for this AA
            denom = C_k - R_t_k * Q
            if denom > 0:
                grams_k = (R_t_k * P - A_k) / denom
                if 1.0 <= grams_k <= 300.0:
                    candidate_X.append(grams_k)
        # Always probe a range of practical amounts — catches foods where the
        # DIAAS peak is not aligned with any single analytical crossing point.
        candidate_X.extend([10, 20, 30, 50, 75, 100, 150, 200, 250, 300])

        # Find the X that maximises pooled DIAAS.
        best_X = 0.0
        best_diaas = current_diaas_val
        for X in candidate_X:
            d = _pooled_diaas(X)
            if d > best_diaas:
                best_diaas = d
                best_X = X

        if best_X <= 0 or best_diaas < current_diaas_val + 0.05:
            return None  # no meaningful improvement at any practical amount

        # If target is reachable, find the minimum X that crosses it (binary search).
        if best_diaas >= target:
            lo, hi = 1.0, best_X
            for _ in range(20):
                mid = (lo + hi) / 2.0
                if _pooled_diaas(mid) >= target:
                    hi = mid
                else:
                    lo = mid
            best_X = hi

        if best_X > 300:
            return None  # impractical even if mathematically valid

        protein_added = Q * best_X
        dig_added = protein_added * (comp_diaas_val if comp_diaas_val is not None else d_comp)
        return {
            "grams":                    round(best_X),
            "current_diaas":            round(current_diaas_val, 2),
            "new_diaas":                round(min(best_diaas, target + 0.01), 2),
            "protein_added":            protein_added,
            "digestible_protein_added": dig_added,
            "diaas":                    comp_diaas_val,
        }

    def _build_suggestions(candidates: list[dict]) -> tuple[list[dict], list[dict]]:
        gap_closers: list[dict] = []
        diaas_improvers: list[dict] = []
        seen_names: set[str] = set()
        for cand in candidates:
            name = cand["name"]
            if name in seen_names:
                continue
            cand_nutrients = cand.get("nutrients")
            cand_diaas = cand.get("diaas") or get_diaas(name)
            # If no nutrients from cache, try the complement table
            if cand_nutrients is None:
                entry = _find_complement_by_name(name)
                if entry:
                    cand_nutrients = entry["nutrients"]
                    cand_diaas = cand_diaas or entry["diaas"]
            if cand_nutrients is None:
                continue
            # Try gap-closer first (targeted AA-ratio formula)
            metrics = None
            for target_aa, _score, _deficit in gaps:
                metrics = _score_candidate(cand_nutrients, cand_diaas, target_aa)
                if metrics is not None:
                    break
            if metrics is not None:
                seen_names.add(name)
                gap_closers.append({"name": name, **metrics})
            else:
                # Try DIAAS-improver (pooled DIAAS formula with per-food digestibilities)
                imp = _diaas_improver_score(cand_nutrients, name, cand_diaas)
                if imp is not None:
                    seen_names.add(name)
                    diaas_improvers.append({"name": name, **imp})
        # Sort gap-closers: primary-gap first, then most gaps closed, then smallest grams.
        gap_closers.sort(key=lambda r: (not r.get("closes_primary"), -r["gaps_closed"], r["grams"]))
        # Sort DIAAS-improvers: best resulting DIAAS first, then smallest grams.
        diaas_improvers.sort(key=lambda r: (-r["new_diaas"], r["grams"]))
        return gap_closers, diaas_improvers

    pantry_gap_closers, pantry_diaas_improvers = _build_suggestions(pantry_candidates)

    # General suggestions from the curated table, filtered by dietary preference.
    pantry_names_lower = {c["name"].lower() for c in pantry_candidates}

    def _diet_allows(c: dict) -> bool:
        if not c.get("animal", False):
            return True
        if diet_pref == "all":
            return True
        if diet_pref == "vegetarian":
            return bool(c.get("dairy_egg", False))
        return False  # plant_only

    general_candidates = [
        {"name": c["name"], "nutrients": c["nutrients"], "diaas": c["diaas"]}
        for c in _COMPLEMENT_TABLE
        if c["name"].lower() not in pantry_names_lower
        and _diet_allows(c)
    ]
    general_gap_closers, general_diaas_improvers = _build_suggestions(general_candidates)

    # Merge DIAAS-improvers from both sources, excluding names already in gap-closer lists.
    gap_closer_names = {s["name"].lower() for s in pantry_gap_closers + general_gap_closers}
    all_diaas_improvers = [
        s for s in pantry_diaas_improvers + general_diaas_improvers
        if s["name"].lower() not in gap_closer_names
    ]
    all_diaas_improvers.sort(key=lambda r: (-r["new_diaas"], r["grams"]))

    return {
        "pantry": pantry_gap_closers,
        "general": general_gap_closers,
        "diaas_improvers": all_diaas_improvers,
    }


# ---------------------------------------------------------------------------
# DIAAS (Digestible Indispensable Amino Acid Score) lookup
# ---------------------------------------------------------------------------
# Values from FAO 2013 and peer-reviewed digestion studies.
# Each entry: (keywords_any_match, score).  First matching entry wins.
# Keywords are matched against the lowercased food name.
# More specific entries must come before more general ones.

_DIAAS_TABLE: list[tuple[tuple[str, ...], float]] = [
    # Animal proteins — high digestibility
    (("whey",),                                     1.09),
    (("egg",),                                      1.13),
    (("milk", "dairy", "yogurt", "kefir"),          1.14),
    (("cheese", "casein"),                          1.08),
    (("beef", "bison", "venison"),                  1.00),
    (("chicken", "turkey", "poultry"),              1.08),
    (("pork", "ham", "bacon"),                      0.99),
    (("salmon", "tuna", "cod", "tilapia", "shrimp",
      "fish", "seafood", "clam", "oyster"),         1.00),
    # Collagen/gelatin — near-zero DIAAS: tryptophan is essentially absent
    (("collagen", "gelatin"),                        0.04),
    # Soy — best plant source
    (("soy protein isolate",),                      0.97),
    (("soy protein concentrate",),                  0.92),
    (("tofu", "tempeh", "edamame", "miso",
      "soybeans", "soya"),                          0.84),
    # Other legumes
    (("pea protein",),                              0.82),
    (("quinoa",),                                   0.85),
    (("chickpea", "garbanzo"),                      0.83),
    (("lentil",),                                   0.75),
    (("black bean", "beans, black"),                0.75),
    (("kidney bean", "beans, kidney"),              0.75),
    (("navy bean", "haricot", "beans, navy"),       0.75),
    (("pinto bean", "beans, pinto"),                0.73),
    (("lima bean", "beans, lima"),                  0.72),
    (("mung bean", "beans, mung"),                  0.73),
    (("bean",),                                     0.75),   # generic legume fallback
    (("peas", "split pea"),                         0.79),
    # Yeast — direct DIAAS data is sparse; estimate from PDCAAS literature
    (("nutritional yeast",),                        0.72),
    # Cocoa / cacao — estimate from AA profile and plant protein digestibility
    (("cocoa", "cacao", "chocolate"),               0.78),
    # Spirulina / chlorella — high protein density but limited digestibility
    (("spirulina", "chlorella"),                    0.67),
    # Mushrooms — modest protein, digestibility varies by species
    (("mushroom",),                                 0.60),
    # Nuts and seeds
    (("hemp seed", "hemp protein", "hemp milk"),     0.63),
    (("flax seed", "flaxseed", "linseed"),          0.52),
    (("peanut",),                                   0.52),
    (("almond",),                                   0.40),
    (("sunflower seed",),                           0.53),
    (("pumpkin seed", "pepita"),                    0.64),
    (("chia seed",),                                0.56),
    (("sesame", "tahini"),                          0.42),
    (("walnut", "pecan", "cashew", "pistachio",
      "hazelnut", "macadamia"),                     0.50),
    # Grains
    (("rice protein",),                             0.59),
    (("okara",),                                    0.75),  # soy byproduct; must precede generic "flour" catch-all
    (("lentil pasta", "lentil noodle"),             0.75),  # must precede generic pasta catch-all
    (("chickpea pasta", "chickpea noodle"),         0.83),  # must precede generic pasta catch-all
    (("vital wheat gluten",),                        0.67),  # AA-computed (lysine-limited); SID 0.86 per FAO FNP 92
    (("seitan", "wheat protein", "gluten"),          0.46),
    (("brown rice", "whole grain rice"),            0.59),
    (("white rice",),                               0.62),
    (("oat",),                                      0.57),
    (("wheat", "bread", "pasta", "flour", "noodle",
      "tortilla", "cracker", "cereal"),             0.46),
    (("corn", "maize", "polenta", "grits"),         0.45),
    (("barley",),                                   0.53),
    (("rye",),                                      0.49),
    (("buckwheat",),                                0.75),
    (("amaranth",),                                 0.76),
    (("millet",),                                   0.54),
    # Vegetables with notable protein
    (("potato",),                                   0.71),
    (("broccoli",),                                 0.73),
    (("spinach",),                                  0.52),
    (("pea",),                                      0.79),
]


def get_diaas(food_name: str) -> float | None:
    """
    Return the DIAAS score for a food by keyword matching, or None if unknown.
    Scores > 1.0 are capped at 1.0 (excess doesn't add benefit beyond completeness).
    """
    name = food_name.lower()
    for keywords, score in _DIAAS_TABLE:
        if any(kw in name for kw in keywords):
            return min(score, 1.0)
    return None


# ---------------------------------------------------------------------------
# Anti-nutrient flags
# ---------------------------------------------------------------------------
# Each entry: (keywords_any_match, flag_text, suppressed_if_any_of).
# suppressed_if contains keywords that, if present in the food name, cancel the flag
# (e.g., "cooked" cancels trypsin inhibitor / lectin flags).

# Each entry: keywords, suppress_if, problem, group, cause, solution_label, solution.
# Entries sharing the same `group` are consolidated into one displayed note.
# solution_label / solution may be None for issues with no actionable remedy.
_ANTINUTRIENT_TABLE: list[dict] = [
    {
        "keywords":       ("bean", "lentil", "chickpea", "garbanzo", "pea", "peanut",
                           "soybeans", "edamame", "tofu", "tempeh"),
        "suppress_if":    (),
        "problem":        "Mineral absorption problem",
        "group":          "phytate",
        "cause":          "phytates are present",
        "solution_label": "Best reduction",
        "solution":       "soak or sprout before cooking",
    },
    {
        "keywords":       ("bean", "lentil", "chickpea", "garbanzo", "soybeans"),
        "suppress_if":    ("cooked", "boiled", "baked", "roasted", "tofu", "tempeh", "canned"),
        "problem":        "Digestibility problem",
        "group":          "lectin",
        "cause":          "lectins & trypsin inhibitors",
        "solution_label": "Required",
        "solution":       "fully cook (boil) to inactivate",
    },
    {
        "keywords":       ("oat", "wheat", "bran", "whole grain", "rye", "barley"),
        "suppress_if":    (),
        "problem":        "Mineral absorption problem",
        "group":          "phytate",
        "cause":          "phytates are present",
        "solution_label": "Best reduction",
        "solution":       "fermentation (sourdough) or soaking",
    },
    {
        "keywords":       ("spinach", "swiss chard", "beet green"),
        "suppress_if":    (),
        "problem":        "Mineral absorption problem",
        "group":          "oxalate",
        "cause":          "high oxalate reduces calcium uptake from this food specifically",
        "solution_label": None,
        "solution":       None,
    },
    {
        "keywords":       ("almond",),
        "suppress_if":    (),
        "problem":        "Mineral absorption problem",
        "group":          "oxalate_phytate",
        "cause":          "oxalate & phytate present",
        "solution_label": "Reduces both",
        "solution":       "roasting or soaking",
    },
    {
        "keywords":       ("nut", "seed", "sesame", "sunflower", "pumpkin"),
        "suppress_if":    ("peanut",),
        "problem":        "Mineral absorption problem",
        "group":          "phytate",
        "cause":          "phytates are present",
        "solution_label": "Moderate reduction",
        "solution":       "roasting",
    },
    {
        "keywords":       ("corn", "maize"),
        "suppress_if":    ("tortilla", "masa", "hominy"),
        "problem":        "Vitamin bioavailability problem",
        "group":          "niacin",
        "cause":          "niacin is bound — not usable unless nixtamalized",
        "solution_label": "Nixtamalized forms are fine",
        "solution":       "tortilla, masa, hominy",
    },
]


def get_antinutrient_flags(food_name: str) -> list[dict]:
    """
    Return consolidated anti-nutrient flags for a food.

    Each flag dict: {"problem": str, "cause": str,
                     "solutions": [(label, description), ...]}
    Entries sharing the same group are merged into one flag.
    """
    name = food_name.lower()

    _KW_PATTERNS: dict[str, str] = {
        "pea": r"pea(?!nut)",
    }

    def _matches(keywords: tuple) -> bool:
        return any(re.search(_KW_PATTERNS.get(kw, re.escape(kw)), name) for kw in keywords)

    groups: dict[str, dict] = {}
    for entry in _ANTINUTRIENT_TABLE:
        if not _matches(entry["keywords"]):
            continue
        if entry["suppress_if"] and _matches(entry["suppress_if"]):
            continue
        g = entry["group"]
        if g not in groups:
            groups[g] = {
                "problem":   entry["problem"],
                "cause":     entry["cause"],
                "solutions": [],
            }
        if entry["solution"]:
            groups[g]["solutions"].append((entry["solution_label"], entry["solution"]))

    return list(groups.values())


# ---------------------------------------------------------------------------
# Volume-to-mass density lookup
# ---------------------------------------------------------------------------
# Each entry: (keyword_tuple, grams_per_ml).  First match wins.
# More specific entries must come before more general ones.

_DENSITY_TABLE: list[tuple[tuple[str, ...], float]] = [
    # Specific products first
    (("nutritional yeast",),                                    0.61),
    (("peanut butter", "almond butter", "tahini"),              1.07),
    (("maple syrup",),                                          1.32),
    (("honey",),                                                1.42),
    (("olive oil", "coconut oil", "vegetable oil", "canola oil",
      "avocado oil", "sesame oil"),                             0.92),
    # Powders / flours
    (("cocoa powder",),                                         0.47),
    (("protein powder", "whey powder"),                         0.50),
    (("baking powder", "baking soda"),                          0.90),
    (("powdered sugar", "confectioner",),                       0.56),
    (("brown sugar",),                                          0.93),
    (("sugar",),                                                0.85),
    (("salt, ", "table salt", "sea salt", "kosher salt"),       1.22),
    (("all-purpose flour", "white flour"),                      0.53),
    (("whole wheat flour",),                                    0.52),
    (("vital wheat gluten",),                                   0.51),  # 121 g/cup
    (("flour",),                                                0.53),
    (("cocoa",),                                                0.47),
    # Grains / seeds
    (("rolled oat", "old-fashioned oat", "quick oat"),          0.36),
    (("oat",),                                                  0.36),
    (("quinoa",),                                               0.71),
    (("brown rice", "wild rice"),                               0.85),
    (("white rice",),                                           0.88),
    (("rice",),                                                 0.86),
    (("chia seed",),                                            0.77),
    (("flax seed", "flaxseed"),                                 0.67),
    (("hemp seed",),                                            0.57),
    (("sesame seed",),                                          0.60),
    (("sunflower seed",),                                       0.56),
    (("pumpkin seed", "pepita"),                                0.46),
    (("poppy seed",),                                           0.56),
    # Nuts (whole/chopped)
    (("almond", "walnut", "pecan", "cashew",
      "pistachio", "hazelnut", "macadamia"),                    0.60),
    (("peanut",),                                               0.60),
    # Legumes (cooked) — USDA descriptions use "Beans, [type], mature seeds, cooked" format;
    # cooked beans absorb water and are less dense than dry (~0.72 g/ml vs 0.77 dry).
    (("beans, pinto", "beans, black", "beans, kidney", "beans, navy",
      "beans, great", "beans, garbanzo", "beans, small", "beans, large",
      "lentils, mature", "chickpeas, mature"),                  0.72),
    # Legumes (dried)
    (("lentil",),                                               0.77),
    (("chickpea", "garbanzo"),                                  0.81),
    (("black bean", "kidney bean", "navy bean",
      "pinto bean", "bean"),                                    0.77),
    # Liquids
    (("oil",),                                                  0.92),
    (("milk", "cream", "buttermilk", "kefir"),                  1.03),
    (("juice",),                                                1.04),
    (("broth", "stock"),                                        1.00),
    (("vinegar",),                                              1.01),
    (("water",),                                                1.00),
]


def get_density_g_per_ml(food_name: str, portions: list[dict]) -> float | None:
    """
    Estimate g/ml density for a food.

    1. Static keyword table first — curated values are more reliable than
       branded USDA serving-size data.
    2. Falls back to USDA portion data if a cup/tablespoon entry is present
       and yields a plausible density (0.3–1.6 g/ml).
    3. Returns None if density cannot be determined.
    """
    # Static table first
    name = food_name.lower()
    for keywords, density in _DENSITY_TABLE:
        if any(kw in name for kw in keywords):
            return density

    # Fall back to USDA portions
    _VOL_ANCHORS = [
        ("cup",        236.6),
        ("tablespoon",  14.8),
        ("tbsp",        14.8),
        ("tbs",         14.8),
        ("teaspoon",     4.9),
        ("tsp",          4.9),
        ("fl oz",       29.6),
    ]
    # Case-sensitive abbreviations expanded before lowercasing (T=tablespoon, t=teaspoon, c=cup)
    _ABBREV = [
        (r"\bT\b", "tablespoon"),
        (r"\bt\b", "teaspoon"),
        (r"\bc\b", "cup"),
    ]
    for p in (portions or []):
        raw = p["description"]
        for pat, word in _ABBREV:
            raw = re.sub(pat, word, raw)
        desc = raw.lower()
        gw = p.get("gram_weight", 0)
        if gw <= 0:
            continue
        # Parse leading number so "2 tablespoons" uses 2×14.8 ml, not 1×14.8 ml
        m = re.match(r'^(\d+)/(\d+)', desc.strip())
        if m:
            count = int(m.group(1)) / int(m.group(2))
        else:
            m2 = re.match(r'^(\d+(?:\.\d+)?)', desc.strip())
            count = float(m2.group(1)) if m2 else 1.0
        for vol_word, ml_val in _VOL_ANCHORS:
            if vol_word in desc:
                density = gw / (count * ml_val)
                if 0.15 <= density <= 1.6:
                    return density

    return None
