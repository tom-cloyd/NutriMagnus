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

# Nutrient groupings for the multi-food compare feature (CLI foods.py + web
# backend.py) — kept here as the single source of truth so the two UIs can't
# silently drift apart on which nutrients are grouped together.
COMPARE_GROUPS: list[tuple[str, list[str]]] = [
    ("Macronutrients", [
        "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
        "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    ]),
    ("Minerals", [
        "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
        "potassium_mg", "sodium_mg", "zinc_mg",
    ]),
    ("Vitamins", [
        "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
        "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
        "b6_mg", "folate_mcg", "b12_mcg",
    ]),
    ("Phytonutrients", [
        "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
        "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg", "isoflavones_mg",
    ]),
    ("Amino Acids", [
        "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
        "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
        "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g",
    ]),
]

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
        "fdc_id": 172421,
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
        "fdc_id": 173756,
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
        "fdc_id": 175236,
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
        "fdc_id": 175200,
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
        "fdc_id": 172479,
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
        "fdc_id": 168190,
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
        "fdc_id": 168411,
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
        "fdc_id": 170420,
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
        "fdc_id": 168917,
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
        "fdc_id": 170285,
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
        "fdc_id": 170148,
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
        "fdc_id": 12023,
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
        "fdc_id": 12078,
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
        "fdc_id": 12014,
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
        "fdc_id": 12036,
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
        "fdc_id": 173904,
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
        "fdc_id": None,
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
        "fdc_id": 174276,
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
        "fdc_id": None,
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
        "fdc_id": 173424,
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
        "fdc_id": 171241,
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
        "fdc_id": 170903,
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
        "fdc_id": 173218,
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
        "fdc_id": 171477,
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
        "fdc_id": 175168,
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


def complement_table_names() -> list[str]:
    """Names of all foods in the internal curated complement table.

    Used by callers (CLI render.py, web backend.py) to search the user's own
    food cache for a real match to each curated entry before falling back to
    the entry's generic literature profile — see suggest_complements()'s
    cache_candidates parameter.
    """
    return [c["name"] for c in _COMPLEMENT_TABLE]


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


def _estimate_aa_from_curated(nutrients: Nutrients, food_name: str) -> Nutrients | None:
    """Merge in amino acid data from the curated complement table, scaled to
    `nutrients`' own protein content. Returns None if `nutrients` already has
    real AA data, no curated entry matches `food_name`, or either side has no
    usable protein figure to scale by.

    This is the "auto-estimate" fallback used by suggest_complements() for a
    real cached/pantry food that lacks its own amino acid panel — distinct
    from the user-driven "estimate amino acids from another food" tool, which
    lets the user pick any food (not just this ~20-entry table) as the source
    and persists the result. This one is recomputed fresh each call and never
    saved, so it can't accidentally preempt that more accurate, user-chosen
    estimate.
    """
    if has_amino_acid_data(nutrients):
        return None
    entry = _find_complement_by_name(food_name)
    if not entry:
        return None
    ref_protein = entry["nutrients"].get("protein_g", 0)
    actual_protein = nutrients.get("protein_g", 0)
    if ref_protein <= 0 or actual_protein <= 0:
        return None
    scale = actual_protein / ref_protein
    merged = dict(nutrients)
    for k, v in entry["nutrients"].items():
        if k.startswith("aa_"):
            merged[k] = v * scale
    return merged


def get_complement_nutrients(food_name: str) -> Nutrients | None:
    """
    Return the nutrient profile from the complement table for a food name,
    or None if not found. Used as a fallback when USDA cache lacks AA data.
    """
    entry = _find_complement_by_name(food_name)
    return entry["nutrients"] if entry else None


def _score_one_complement(
    base_nutrients: Nutrients,
    base_gaps: list,
    base_digestibility: float,
    cand_nutrients: Nutrients,
    cand_diaas: float | None,
    target_aa: str,
) -> dict | None:
    """
    Compute suggestion metrics for one candidate food targeting a specific AA gap
    in base_nutrients.  Returns None if the candidate cannot close that gap.

    Solves for grams X: (base_aa + alpha*X) / (base_protein + beta*X) = R
    where alpha = cand_aa/100, beta = cand_protein/100, R = digestibility-adjusted
    reference ratio.  Valid only when alpha > R*beta (candidate AA/protein ratio
    exceeds the reference).

    Extracted from the _score_candidate closure inside suggest_complements so that
    _build_pairs can re-use the same formula with a different base (post-first-food).
    """
    if target_aa in _AA_PAIRS:
        pair_key = _AA_PAIRS[target_aa]
        alpha = (cand_nutrients.get(target_aa, 0.0) + cand_nutrients.get(pair_key, 0.0)) / 100.0
    else:
        alpha = cand_nutrients.get(target_aa, 0.0) / 100.0
    beta = cand_nutrients.get("protein_g", 0.0) / 100.0
    R = AA_REFERENCE_MG_PER_G_PROTEIN[target_aa] / 1000.0 / max(base_digestibility, 0.01)
    denom = alpha - R * beta
    if denom <= 0:
        return None
    if target_aa in _AA_PAIRS:
        base_aa = base_nutrients.get(target_aa, 0.0) + base_nutrients.get(_AA_PAIRS[target_aa], 0.0)
    else:
        base_aa = base_nutrients.get(target_aa, 0.0)
    base_protein = base_nutrients.get("protein_g", 0.0)
    grams = (R * base_protein - base_aa) / denom
    if grams <= 0 or grams > 500:
        return None
    added = scale_nutrients(cand_nutrients, grams)
    combined = sum_nutrients(base_nutrients, added)
    new_pc = protein_completeness(combined, digestibility=base_digestibility)
    new_gaps = get_aa_gaps(combined, digestibility=base_digestibility)
    gaps_closed = len(base_gaps) - len(new_gaps)
    target_still_gapped = any(aa == target_aa for aa, _, _ in new_gaps)
    if target_still_gapped:
        return None
    original_gap_set = {aa for aa, _, _ in base_gaps}
    new_gap_set = {aa for aa, _, _ in new_gaps}
    opens_new_gap = bool(new_gap_set - original_gap_set)
    closes_primary = (target_aa == base_gaps[0][0]) if base_gaps else False
    protein_added = cand_nutrients.get("protein_g", 0) * grams / 100
    dig_added = protein_added * (cand_diaas if cand_diaas is not None else 1.0)
    # Predicted DIAAS for the combined pool using per-source digestibility.
    # base_nutrients scaled by base_digestibility; complement scaled by its own DIAAS.
    # This is more accurate than applying base_digestibility uniformly to the combined
    # raw pool, which overestimates DCP when adding a high-DIAAS complement.
    comp_dig = cand_diaas if cand_diaas is not None else 1.0
    total_raw_protein = combined.get("protein_g", 0)
    predicted_diaas: float | None = None
    if total_raw_protein > 0:
        dig_scores: dict[str, float] = {}
        for aa_key in ESSENTIAL_AMINO_ACIDS:
            pair_key = _AA_PAIRS.get(aa_key)
            base_aa = base_nutrients.get(aa_key, 0.0)
            comp_aa = cand_nutrients.get(aa_key, 0.0) * grams / 100
            if pair_key:
                base_aa += base_nutrients.get(pair_key, 0.0)
                comp_aa += cand_nutrients.get(pair_key, 0.0) * grams / 100
            if base_aa <= 0 and comp_aa <= 0:
                continue
            ref_g = AA_REFERENCE_MG_PER_G_PROTEIN[aa_key] / 1000.0 * total_raw_protein
            if ref_g > 0:
                dig_scores[aa_key] = (base_aa * base_digestibility + comp_aa * comp_dig) / ref_g
        if dig_scores:
            predicted_diaas = min(dig_scores.values())
    # Reject if adding this complement would reduce total DCP (pooled DIAAS
    # below the base meal's digestibility).  Only meaningful when we have real
    # digestibility data; skip when base_digestibility is the 1.0 default.
    if predicted_diaas is not None and base_digestibility < 1.0 and predicted_diaas < base_digestibility:
        return None
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
        "diaas":                    cand_diaas,
        "predicted_diaas":          predicted_diaas,
        "comp_nutrients":           cand_nutrients,
    }


def suggest_complements(
    base_nutrients: Nutrients,
    pantry_candidates: list[dict],
    diet_pref: str = "all",
    base_digestibility: float = 1.0,
    base_food_name: str | None = None,
    max_improver_grams: float = 300,
    cache_candidates: list[dict] | None = None,
) -> dict[str, list[dict]]:
    """
    Suggest complement foods to close essential amino acid gaps.

    pantry_candidates: list of dicts, each with:
        "name": str
        "nutrients": dict | None   (per-100g; None if not in USDA cache)
        "diaas": float | None
    cache_candidates: real foods from the user's broader food cache (not just
        pantry) that match a curated-table entry by name — same dict shape as
        pantry_candidates. When one is found for a given curated entry, it's
        used in place of that entry's generic profile in the "general" tier
        (see complement_table_names() for the names to search the cache for).
    diet_pref: "all" includes all sources; "vegetarian" allows dairy/eggs but not
        meat/fish; "plant_only" excludes all animal-sourced entries.
    base_food_name: used to look up true ileal digestibility for DIAAS-improver
        calculations; falls back to base_digestibility if None.

    Any candidate (pantry or general) that has real nutrient data but lacks its
    own amino acid panel is auto-estimated via the curated table (scaled to its
    own protein content) rather than dropped — see _estimate_aa_from_curated().
    Result dicts carry "estimated": True when this happened.

    Returns {"pantry": [...], "general": [...], "diaas_improvers": [...]}
    Gap-closer dicts contain:
        name, grams, new_scores, new_complete, gaps_closed, estimated,
        remaining_gaps, protein_added, digestible_protein_added, diaas
    DIAAS-improver dicts contain:
        name, steps (list of {grams, new_diaas}), grams (largest step),
        current_diaas, new_diaas (at largest step), estimated,
        protein_added, digestible_protein_added, diaas
    """
    gaps = get_aa_gaps(base_nutrients, digestibility=base_digestibility)
    if not gaps:
        return {"pantry": [], "general": [], "pairs": [], "diaas_improvers": []}

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
        """Delegate to the module-level helper using this closure's base context."""
        return _score_one_complement(
            base_nutrients, gaps, base_digestibility,
            nutrients_100g, diaas, target_aa,
        )

    def _diaas_improver_score(
        comp_nutrients: dict,
        comp_name: str,
        comp_diaas_val: float | None,
        target: float = 0.90,
        max_grams: float = 300,
    ) -> dict | None:
        """
        Find a stepped progression of practical servings of comp that improve the
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

        max_grams: cap on the largest step shown; use 120 for meal/food/daily
            contexts, 300 for recipe contexts.

        Returns None if no step within max_grams achieves ≥ 0.03 DIAAS improvement.
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

        # Standard step sizes; trim to max_grams cap.
        if max_grams <= 120:
            all_steps = [15, 30, 60, 120]
        else:
            all_steps = [30, 60, 100, 150, 200, 300]
        step_sizes = [s for s in all_steps if s <= max_grams]

        # Evaluate pooled DIAAS at each step.
        steps: list[dict] = []
        prev_diaas = current_diaas_val
        for X in step_sizes:
            d = _pooled_diaas(X)
            if d > current_diaas_val + 0.005 and d > prev_diaas - 0.005:
                dcp = round((P + Q * X) * min(1.0, d), 1)
                steps.append({"grams": X, "new_diaas": round(d, 2), "dcp": dcp})
                prev_diaas = d

        if not steps:
            return None
        best_diaas = steps[-1]["new_diaas"]
        if best_diaas < current_diaas_val + 0.03:
            return None  # no meaningful improvement within the cap

        best_X = steps[-1]["grams"]
        protein_added = Q * best_X
        dig_added = protein_added * (comp_diaas_val if comp_diaas_val is not None else d_comp)
        return {
            "steps":                    steps,
            "grams":                    best_X,   # largest step (for ranking)
            "current_diaas":            round(current_diaas_val, 2),
            "new_diaas":                round(best_diaas, 2),
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
            fdc_id = cand.get("fdc_id")
            recipe_id = cand.get("recipe_id")
            serving_weight_g = cand.get("serving_weight_g")
            if name in seen_names:
                continue
            cand_nutrients = cand.get("nutrients")
            cand_diaas = cand.get("diaas") or get_diaas(name)
            estimated = False
            # If no nutrients from cache, try the complement table
            if cand_nutrients is None:
                entry = _find_complement_by_name(name)
                if entry:
                    cand_nutrients = entry["nutrients"]
                    cand_diaas = cand_diaas or entry["diaas"]
            elif not has_amino_acid_data(cand_nutrients):
                # Real food, real macros, but no AA panel of its own — auto-estimate
                # from the curated table rather than silently dropping it.
                merged = _estimate_aa_from_curated(cand_nutrients, name)
                if merged is not None:
                    cand_nutrients = merged
                    cand_diaas = cand_diaas or get_diaas(name)
                    estimated = True
            if cand_nutrients is None:
                continue
            # Try gap-closer first (targeted AA-ratio formula)
            metrics = None
            for target_aa, _score, _deficit in gaps:
                metrics = _score_candidate(cand_nutrients, cand_diaas, target_aa)
                if metrics is not None:
                    break
            extra = {"recipe_id": recipe_id, "serving_weight_g": serving_weight_g, "estimated": estimated}
            if metrics is not None:
                seen_names.add(name)
                gap_closers.append({"name": name, "fdc_id": fdc_id, **extra, **metrics})
            else:
                # Try DIAAS-improver (pooled DIAAS formula with per-food digestibilities)
                imp = _diaas_improver_score(cand_nutrients, name, cand_diaas,
                                           max_grams=max_improver_grams)
                if imp is not None:
                    seen_names.add(name)
                    diaas_improvers.append({"name": name, "fdc_id": fdc_id, **extra, **imp})
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

    # Index cache_candidates (real foods matching a curated entry by name) so the
    # general tier prefers real cached data over the entry's generic profile.
    cache_by_curated_key: dict[str, dict] = {}
    for cc in (cache_candidates or []):
        entry = _find_complement_by_name(cc["name"])
        if entry and entry["name"].lower() not in cache_by_curated_key:
            cache_by_curated_key[entry["name"].lower()] = cc

    general_candidates = []
    for c in _COMPLEMENT_TABLE:
        if c["name"].lower() in pantry_names_lower or not _diet_allows(c):
            continue
        real = cache_by_curated_key.get(c["name"].lower())
        if real is not None:
            general_candidates.append({
                "name": real["name"], "fdc_id": real.get("fdc_id"),
                "nutrients": real.get("nutrients"), "diaas": real.get("diaas") or c["diaas"],
            })
        else:
            general_candidates.append(
                {"name": c["name"], "fdc_id": c.get("fdc_id"), "nutrients": c["nutrients"], "diaas": c["diaas"]}
            )
    general_gap_closers, general_diaas_improvers = _build_suggestions(general_candidates)

    # Merge DIAAS-improvers from both sources, excluding names already in gap-closer lists.
    gap_closer_names = {s["name"].lower() for s in pantry_gap_closers + general_gap_closers}
    all_diaas_improvers = [
        s for s in pantry_diaas_improvers + general_diaas_improvers
        if s["name"].lower() not in gap_closer_names
    ]
    all_diaas_improvers.sort(key=lambda r: (-r["new_diaas"], r["grams"]))

    # --- Gap-cascade pairs ---------------------------------------------------
    # All candidates (pantry first for preference, then general) deduplicated by name.
    all_candidate_names: set[str] = set()
    all_candidates_ordered: list[dict] = []
    for c in pantry_candidates:
        if c["name"] not in all_candidate_names:
            # Resolve nutrients + diaas the same way _build_suggestions does.
            cand_n = c.get("nutrients")
            cand_d = c.get("diaas") or get_diaas(c["name"])
            if cand_n is None:
                entry = _find_complement_by_name(c["name"])
                if entry:
                    cand_n = entry["nutrients"]
                    cand_d = cand_d or entry["diaas"]
            if cand_n is not None:
                all_candidate_names.add(c["name"])
                all_candidates_ordered.append({
                    "name": c["name"], "fdc_id": c.get("fdc_id"),
                    "recipe_id": c.get("recipe_id"),
                    "serving_weight_g": c.get("serving_weight_g"),
                    "nutrients": cand_n, "diaas": cand_d,
                })
    for c in general_candidates:
        if c["name"] not in all_candidate_names and c.get("nutrients"):
            all_candidate_names.add(c["name"])
            all_candidates_ordered.append(c)

    def _build_pairs() -> list[dict]:
        """
        Gap-cascade pairs: food A closes the primary gap but opens a new one;
        food B closes what A left behind.  Both foods together achieve a complete
        amino acid profile.  Each unique unordered pair (A, B) is tested once.
        """
        pairs: list[dict] = []
        seen_pair_keys: set[frozenset] = set()

        for cand_a in all_candidates_ordered:
            a_name = cand_a["name"]
            a_nutrients = cand_a["nutrients"]
            a_diaas = cand_a["diaas"]
            a_fdc_id = cand_a.get("fdc_id")
            a_recipe_id = cand_a.get("recipe_id")
            a_serving_wt = cand_a.get("serving_weight_g")

            # Score A against the original primary gap.
            primary_aa = gaps[0][0]
            a_m = _score_one_complement(
                base_nutrients, gaps, base_digestibility,
                a_nutrients, a_diaas, primary_aa,
            )
            if a_m is None:
                continue
            # Skip A if it alone achieves completeness — it's already a strong
            # single-food suggestion and pairing adds no value.
            if not a_m["opens_new_gap"]:
                continue

            combined_after_a: Nutrients = sum_nutrients(
                base_nutrients, scale_nutrients(a_nutrients, a_m["grams"])
            )
            gaps_after_a: list = get_aa_gaps(combined_after_a, digestibility=base_digestibility)
            if not gaps_after_a:
                continue

            for cand_b in all_candidates_ordered:
                b_name = cand_b["name"]
                if b_name == a_name:
                    continue
                pair_key: frozenset = frozenset([a_name, b_name])
                if pair_key in seen_pair_keys:
                    continue
                seen_pair_keys.add(pair_key)

                b_nutrients = cand_b["nutrients"]
                b_diaas = cand_b["diaas"]
                b_fdc_id = cand_b.get("fdc_id")
                b_recipe_id = cand_b.get("recipe_id")
                b_serving_wt = cand_b.get("serving_weight_g")

                b_target_aa = gaps_after_a[0][0]
                b_m = _score_one_complement(
                    combined_after_a, gaps_after_a, base_digestibility,
                    b_nutrients, b_diaas, b_target_aa,
                )
                if b_m is None:
                    continue
                # Only accept B if it closes all remaining gaps without opening new ones.
                if b_m["remaining_gaps"] > 0 or b_m["opens_new_gap"]:
                    continue

                total_grams = a_m["grams"] + b_m["grams"]
                if total_grams > 600:
                    continue

                a_prot = a_nutrients.get("protein_g", 0) * a_m["grams"] / 100
                b_prot = b_nutrients.get("protein_g", 0) * b_m["grams"] / 100
                a_dig  = a_prot * (a_diaas if a_diaas is not None else 1.0)
                b_dig  = b_prot * (b_diaas if b_diaas is not None else 1.0)

                pairs.append({
                    "foods": [
                        {"name": a_name, "fdc_id": a_fdc_id, "recipe_id": a_recipe_id,
                         "serving_weight_g": a_serving_wt, "diaas": a_diaas,
                         "grams": a_m["grams"],
                         "protein_added": round(a_prot, 1),
                         "dig_added":     round(a_dig,  1)},
                        {"name": b_name, "fdc_id": b_fdc_id, "recipe_id": b_recipe_id,
                         "serving_weight_g": b_serving_wt, "diaas": b_diaas,
                         "grams": b_m["grams"],
                         "protein_added": round(b_prot, 1),
                         "dig_added":     round(b_dig,  1)},
                    ],
                    "total_grams":         total_grams,
                    # gaps_closed: all AAs at score ≥ 0.95 (the gap threshold).
                    # Stronger than new_complete (which requires ≥ 1.0) but the
                    # practically meaningful result for multi-food combinations.
                    "gaps_closed":         b_m["remaining_gaps"] == 0,
                    "new_complete":        b_m["new_complete"],
                    "new_scores":          b_m["new_scores"],
                    "predicted_diaas":     b_m.get("predicted_diaas"),
                    "total_protein_added": round(a_prot + b_prot, 1),
                    "total_dig_added":     round(a_dig  + b_dig,  1),
                })

        # Sort: smallest total grams first; gap-closure bonus only when ≤50 g total.
        pairs.sort(key=lambda p: (
            0.0 if (p["gaps_closed"] and p["total_grams"] <= 50) else 1.0,
            p["total_grams"],
        ))
        return pairs

    complement_pairs = _build_pairs()

    return {
        "pantry":          pantry_gap_closers,
        "general":         general_gap_closers,
        "pairs":           complement_pairs,
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
    (("butter",),                                              0.91),
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
    # Dried fruits
    (("raisin",),                                                  0.63),  # 149 g/cup; King Arthur Baking weight chart
    (("dried cranberr", "craisin"),                                0.48),  # 114 g/cup; King Arthur Baking weight chart
    (("dried apricot",),                                           0.54),  # 128 g/cup diced; King Arthur Baking weight chart
    (("date",),                                                    0.74),  # 175 g/cup whole pitted; Sweet2Eat baking reference
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
    # Dried herbs & spices — specific ones first (flaked/leafy herbs are much
    # lighter per volume than ground powders or seeds; values from common
    # spoon-for-spoon weight references, e.g. King Arthur / USDA SR).
    (("pepper flakes", "crushed red pepper", "chili flakes"),   0.35),
    (("black pepper", "white pepper", "peppercorn"),            0.44),
    (("pepper, red or cayenne", "cayenne"),                     0.45),
    (("cinnamon",),                                             0.51),
    (("cumin",),                                                0.48),
    (("paprika",),                                              0.45),
    (("garlic powder",),                                        0.45),
    (("onion powder",),                                         0.45),
    (("ginger, ground", "ground ginger"),                       0.43),
    (("nutmeg",),                                                0.48),
    (("allspice",),                                             0.44),
    (("turmeric",),                                             0.44),
    (("chili powder",),                                         0.45),
    (("curry powder",),                                         0.40),
    (("cloves",),                                                0.51),
    (("coriander",),                                            0.45),
    (("oregano",),                                              0.18),
    (("basil",),                                                0.13),
    (("thyme",),                                                0.28),
    (("rosemary",),                                             0.20),
    (("spices, sage",),                                         0.28),
    (("dill weed",),                                            0.18),
    (("parsley",),                                              0.15),
    (("bay leaf", "bay leaves"),                                0.15),
    (("marjoram",),                                             0.16),
    (("tarragon",),                                             0.18),
    (("poultry seasoning", "italian seasoning", "seasoning"),   0.35),
    # Generic fallback for any other dried spice — USDA names these foods
    # "Spices, <name>", so this catches ones not itemized above. Approximate;
    # kept last so any more specific match above always wins.
    (("spices,", "spices ("),                                   0.40),
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
