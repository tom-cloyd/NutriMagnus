"""
diaas.py — Meal-level DIAAS (Digestible Indispensable Amino Acid Score) calculation.

Methodology: FAO (2013). Dietary protein quality evaluation in human nutrition.
FAO Food and Nutrition Paper 92.

The meal-level calculation applies a true ileal digestibility coefficient to each
ingredient's amino acid amounts, pools the digestible IAAs across all ingredients,
then computes a single composite DIAAS score from the pooled totals vs. the FAO adult
reference pattern.  This captures amino acid complementarity — a lysine-rich food
rescues a lysine-deficient one — which individual per-food DIAAS cannot.

Lookup order for digestibility coefficients:
  1. User override stored in the diaas_overrides table (exact food name, case-insensitive)
  2. Curated table: literature-sourced values for ~30 specific foods/categories
  3. Category default: broad averages for food type (legume, seed, grain, etc.)
  4. Overall default: 0.82 (conservative plant-protein average)
Docs: README-numa-documentation.md, Architecture: "diaas.py — Meal-level DIAAS calculation"
"""

from __future__ import annotations

import sqlite3

# ---------------------------------------------------------------------------
# FAO 2013 adult reference pattern  (mg of IAA per g of total protein)
# Source: FAO Food and Nutrition Paper 92 (2013), Table 6.
# Met+Cys and Phe+Tyr are combined pairs per DIAAS methodology.
# ---------------------------------------------------------------------------

FAO_REFERENCE: dict[str, float] = {
    "aa_histidine_g":       16.0,
    "aa_isoleucine_g":      30.0,
    "aa_leucine_g":         61.0,
    "aa_lysine_g":          48.0,
    "aa_methionine_g":      23.0,   # Met+Cys combined (see _IAA_PAIRS)
    "aa_phenylalanine_g":   41.0,   # Phe+Tyr combined (see _IAA_PAIRS)
    "aa_threonine_g":       25.0,
    "aa_tryptophan_g":       6.6,
    "aa_valine_g":          40.0,
}

# For paired IAAs, the secondary key's value is added to the primary before scoring.
# aa_tyrosine_g may be absent from older cached foods (added to NUTRIENT_MAP later);
# the code handles missing values by adding 0, and sets a gap flag in results.
_IAA_PAIRS: dict[str, str | None] = {
    "aa_histidine_g":       None,
    "aa_isoleucine_g":      None,
    "aa_leucine_g":         None,
    "aa_lysine_g":          None,
    "aa_methionine_g":      "aa_cystine_g",       # Met+Cys
    "aa_phenylalanine_g":   "aa_tyrosine_g",      # Phe+Tyr
    "aa_threonine_g":       None,
    "aa_tryptophan_g":      None,
    "aa_valine_g":          None,
}

# Human-readable labels for IAA keys
IAA_LABELS: dict[str, str] = {
    "aa_histidine_g":       "Histidine",
    "aa_isoleucine_g":      "Isoleucine",
    "aa_leucine_g":         "Leucine",
    "aa_lysine_g":          "Lysine",
    "aa_methionine_g":      "Met+Cys",
    "aa_phenylalanine_g":   "Phe+Tyr",
    "aa_threonine_g":       "Threonine",
    "aa_tryptophan_g":      "Tryptophan",
    "aa_valine_g":          "Valine",
}

# ---------------------------------------------------------------------------
# Curated digestibility table
# Each entry: (keywords_any_match, digestibility, citation).
# True ileal digestibility coefficient applied to all IAAs from the food.
# More specific entries must appear before broader ones.
# Sources: FAO FNP 92 (2013); Mathai et al. 2017 Br J Nutr; Gorissen et al. 2018 Amino Acids
# ---------------------------------------------------------------------------

_DIGESTIBILITY_TABLE: list[tuple[tuple[str, ...], float, str]] = [
    # Isolated / concentrated plant proteins
    (("soy protein isolate", "soy isolate"),          0.95, "Mathai et al. 2017, Br J Nutr"),
    (("soy protein concentrate",),                    0.92, "Mathai et al. 2017, Br J Nutr"),
    (("pea protein isolate",),                        0.94, "Mathai et al. 2017, Br J Nutr"),
    (("pea protein",),                                0.92, "Mathai et al. 2017, Br J Nutr"),
    (("rice protein",),                               0.87, "Gorissen et al. 2018, Amino Acids"),
    (("vital wheat gluten", "wheat protein", "seitan"), 0.86, "FAO FNP 92 (2013)"),
    (("hemp protein",),                               0.87, "Gorissen et al. 2018, Amino Acids"),
    # Soy whole foods
    (("soy milk", "soymilk"),                         0.92, "estimate — whole soy food"),
    (("tofu", "bean curd"),                           0.88, "estimate — whole soy food"),
    (("tempeh",),                                     0.89, "estimate — fermented soy"),
    (("edamame",),                                    0.84, "estimate — whole soybean"),
    (("miso",),                                       0.85, "estimate — fermented soy"),
    (("soybeans", "soya bean"),                       0.84, "estimate — whole soybean"),
    # Okara (soy fiber/protein byproduct)
    (("okara",),                                      0.80, "Li et al. 2012, Food Rev Int"),
    # Nutritional yeast
    (("nutritional yeast",),                          0.90, "estimate (Saccharomyces cerevisiae)"),
    # Animal proteins
    (("egg white",),                                  0.98, "FAO FNP 92 (2013)"),
    (("egg",),                                        0.98, "FAO FNP 92 (2013)"),
    (("whey",),                                       1.00, "FAO FNP 92 (2013)"),
    (("casein",),                                     0.99, "FAO FNP 92 (2013)"),
    (("milk", "dairy", "yogurt", "kefir"),            1.00, "FAO FNP 92 (2013)"),
    (("cheese",),                                     0.98, "FAO FNP 92 (2013)"),
    (("beef", "bison", "venison", "chicken", "turkey",
      "pork", "ham", "salmon", "tuna", "cod",
      "tilapia", "shrimp", "fish", "seafood"),        0.96, "FAO FNP 92 (2013)"),
    # Legumes (cooked)
    (("chickpea", "garbanzo"),                        0.82, "FAO FNP 92 (2013)"),
    (("lentil",),                                     0.83, "FAO FNP 92 (2013)"),
    (("split pea",),                                  0.85, "FAO FNP 92 (2013)"),
    (("black bean", "kidney bean", "navy bean",
      "pinto bean", "lima bean", "adzuki",
      "cannellini", "fava bean", "mung bean"),        0.80, "FAO FNP 92 (2013)"),
    (("peas", "green pea"),                           0.79, "FAO FNP 92 (2013)"),
    (("bean",),                                       0.80, "FAO FNP 92 (2013) — generic legume"),
    # Seeds
    (("flax seed", "flaxseed", "ground flax"),        0.85, "Gorissen et al. 2018, Amino Acids"),
    (("hemp seed",),                                  0.87, "Gorissen et al. 2018, Amino Acids"),
    (("chia seed",),                                  0.82, "estimate — seed category"),
    (("pumpkin seed", "pepita"),                      0.85, "estimate (Nwachukwu et al. 2022)"),
    (("sunflower seed",),                             0.84, "estimate — seed category"),
    (("sesame", "tahini"),                            0.84, "estimate — seed category"),
    # Nuts
    (("peanut butter powder", "pb powder", "pbp"),    0.87, "FAO FNP 92 (2013) — peanut"),
    (("peanut",),                                     0.87, "FAO FNP 92 (2013)"),
    (("walnut", "pecan", "almond", "cashew",
      "pistachio", "hazelnut", "macadamia"),          0.78, "estimate — tree nut category"),
    # Grains
    (("quinoa",),                                     0.85, "Mathai et al. 2017, Br J Nutr"),
    (("amaranth",),                                   0.78, "estimate — pseudocereal"),
    (("buckwheat",),                                  0.79, "estimate — pseudocereal"),
    (("oat", "oatmeal"),                              0.82, "estimate — cereal grain"),
    (("brown rice", "whole grain rice", "wild rice"), 0.82, "estimate — whole grain"),
    (("white rice",),                                 0.88, "estimate — refined grain"),
    (("wheat", "bread", "pasta", "flour", "noodle",
      "tortilla", "cracker"),                         0.84, "estimate — refined grain"),
    (("corn", "maize", "polenta", "grits"),           0.80, "estimate — cereal grain"),
    (("millet",),                                     0.79, "estimate — cereal grain"),
    (("barley",),                                     0.81, "estimate — cereal grain"),
    (("rye",),                                        0.80, "estimate — cereal grain"),
    # Vegetables (when contributing notable protein)
    (("potato",),                                     0.88, "estimate — tuber"),
    (("broccoli",),                                   0.78, "estimate — vegetable"),
    (("spinach",),                                    0.75, "estimate — leafy vegetable"),
]

# Category fallback defaults when no specific match is found.
# Each entry: (keywords_any, digestibility, category_label)
_CATEGORY_DEFAULTS: list[tuple[tuple[str, ...], float, str]] = [
    (("isolate", "concentrate", "protein powder"),  0.92, "isolated/concentrated plant protein"),
    (("legume", "bean", "lentil", "pea",
      "chickpea", "soy"),                           0.80, "legume"),
    (("seed",),                                     0.82, "seed"),
    (("nut",),                                      0.78, "nut"),
    (("grain", "rice", "wheat", "oat", "corn",
      "flour", "bread", "cereal"),                  0.82, "grain/cereal"),
    (("animal", "meat", "fish", "poultry",
      "dairy", "egg", "beef", "chicken",
      "turkey", "pork", "salmon"),                  0.96, "animal protein"),
]

# Conservative overall default — used only when nothing else matches.
_OVERALL_DEFAULT = 0.82


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_digestibility(
    food_name: str,
    conn: sqlite3.Connection | None = None,
) -> tuple[float, str]:
    """
    Return (digestibility, source_description) for a food name.

    source_description is one of:
      "user override"
      "curated (citation)"
      "category estimate (label)"
      "default estimate"
    """
    # 1. User override
    if conn is not None:
        row = diaas_override_get(conn, food_name)
        if row is not None:
            return float(row["digestibility"]), "user override"

    name_lower = food_name.lower()

    # 2. Curated table
    for keywords, dig, citation in _DIGESTIBILITY_TABLE:
        if any(kw in name_lower for kw in keywords):
            return dig, f"curated ({citation})"

    # 3. Category default
    for keywords, dig, label in _CATEGORY_DEFAULTS:
        if any(kw in name_lower for kw in keywords):
            return dig, f"category estimate ({label})"

    # 4. Overall default
    return _OVERALL_DEFAULT, "default estimate (0.82 — conservative plant protein average)"


def meal_level_diaas(
    ingredients: list[dict],
    conn: sqlite3.Connection | None = None,
) -> dict:
    """
    Compute meal-level DIAAS for a list of ingredients.

    Each ingredient dict must have:
        "food_name":      str
        "nutrients_100g": dict[str, float]  — USDA nutrient dict per 100g
        "grams":          float             — actual weight consumed

    Returns a dict with:
        "diaas":                        float | None   — composite score (may exceed 1.0; not capped)
        "total_protein_g":              float
        "digestible_complete_protein_g":float | None   — aa_protein_g × min(diaas, 1.0)
        "limiting_iaa":                 str | None     — IAA key of limiting amino acid
        "limiting_label":               str | None     — human-readable name of limiting IAA
        "iaa_ratios":                   dict[str, float]   — IAA key → ratio vs. FAO reference
        "phe_tyr_gap":                  bool  — True if tyrosine absent (Phe+Tyr underestimated)
        "ingredients":                  list[dict]  — per-ingredient breakdown
        "has_complete_data":            bool  — False if any ingredient is missing AA data
        "missing_aa_names":             list[str]   — food names without amino acid data
        "estimate_sources":             list[str]   — food names using category/default digestibility
    """
    total_protein_g = 0.0
    aa_protein_g = 0.0   # protein only from foods that have AA data (used for reference denominator)
    pooled: dict[str, float] = {k: 0.0 for k in FAO_REFERENCE}
    pooled_counts: dict[str, int] = {k: 0 for k in FAO_REFERENCE}
    ingredient_results: list[dict] = []
    missing_aa_names: list[str] = []
    estimate_sources: list[str] = []
    any_aa_data = False

    for ing in ingredients:
        food_name = ing["food_name"]
        nuts = ing["nutrients_100g"]
        grams = ing["grams"]
        scale = grams / 100.0

        protein_g = nuts.get("protein_g", 0.0) * scale
        total_protein_g += protein_g

        dig, dig_source = get_digestibility(food_name, conn)
        if "estimate" in dig_source or "default" in dig_source:
            estimate_sources.append(food_name)

        has_aa = any(nuts.get(k, 0) > 0 for k in FAO_REFERENCE)
        if not has_aa:
            missing_aa_names.append(food_name)
            ingredient_results.append({
                "food_name":     food_name,
                "fdc_id":        ing.get("fdc_id"),
                "grams":         grams,
                "protein_g":     protein_g,
                "digestibility": dig,
                "dig_source":    dig_source,
                "has_aa_data":   False,
            })
            continue

        any_aa_data = True
        aa_protein_g += protein_g
        ing_iaa: dict[str, float] = {}

        for aa_key, secondary in _IAA_PAIRS.items():
            raw_g = nuts.get(aa_key, 0.0) * scale
            if secondary:
                raw_g += nuts.get(secondary, 0.0) * scale
            dig_g = raw_g * dig
            ing_iaa[aa_key] = dig_g
            if raw_g > 0:
                pooled[aa_key] += dig_g
                pooled_counts[aa_key] += 1

        ingredient_results.append({
            "food_name":       food_name,
            "fdc_id":          ing.get("fdc_id"),
            "grams":           grams,
            "protein_g":       protein_g,
            "digestibility":   dig,
            "dig_source":      dig_source,
            "has_aa_data":     True,
            "digestible_iaa":  ing_iaa,
        })

    if total_protein_g <= 0 or not any_aa_data:
        return {
            "diaas": None,
            "total_protein_g": total_protein_g,
            "digestible_complete_protein_g": None,
            "limiting_iaa": None,
            "limiting_label": None,
            "iaa_ratios": {},
            "phe_tyr_gap": False,
            "ingredients": ingredient_results,
            "has_complete_data": False,
            "missing_aa_names": missing_aa_names,
            "estimate_sources": estimate_sources,
        }

    # Detect Phe+Tyr gap: if no ingredient had tyrosine data, Phe+Tyr is underestimated.
    phe_tyr_gap = not any(
        ing.get("nutrients_100g", {}).get("aa_tyrosine_g", 0) > 0
        for ing in ingredients
    )

    # Compute composite IAA ratios vs. FAO reference.
    # Use aa_protein_g (protein from foods with AA data) as the denominator — foods
    # without AA data are excluded from the numerator, so including their protein in
    # the reference would artificially deflate all ratios.
    iaa_ratios: dict[str, float] = {}
    ref_basis = aa_protein_g if aa_protein_g > 0 else total_protein_g
    for aa_key, ref_mg_per_g in FAO_REFERENCE.items():
        if pooled_counts[aa_key] == 0:
            continue  # no ingredient had data for this IAA — omit from scoring
        ref_g = ref_mg_per_g / 1000.0 * ref_basis
        iaa_ratios[aa_key] = pooled[aa_key] / ref_g if ref_g > 0 else 0.0

    if not iaa_ratios:
        return {
            "diaas": None,
            "total_protein_g": total_protein_g,
            "digestible_complete_protein_g": None,
            "limiting_iaa": None,
            "limiting_label": None,
            "iaa_ratios": {},
            "phe_tyr_gap": phe_tyr_gap,
            "ingredients": ingredient_results,
            "has_complete_data": False,
            "missing_aa_names": missing_aa_names,
            "estimate_sources": estimate_sources,
        }

    limiting_iaa = min(iaa_ratios, key=lambda k: iaa_ratios[k])
    composite_diaas = iaa_ratios[limiting_iaa]
    dcp = ref_basis * min(composite_diaas, 1.0)

    return {
        "diaas": composite_diaas,
        "total_protein_g": total_protein_g,
        "aa_protein_g": aa_protein_g,
        "digestible_complete_protein_g": dcp,
        "limiting_iaa": limiting_iaa,
        "limiting_label": IAA_LABELS.get(limiting_iaa),
        "iaa_ratios": iaa_ratios,
        "phe_tyr_gap": phe_tyr_gap,
        "ingredients": ingredient_results,
        "has_complete_data": not missing_aa_names,
        "missing_aa_names": missing_aa_names,
        "estimate_sources": estimate_sources,
    }


# ---------------------------------------------------------------------------
# DB functions for user overrides  (table created by db.init_db)
# ---------------------------------------------------------------------------

def diaas_override_get(
    conn: sqlite3.Connection, food_name: str
) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM diaas_overrides WHERE lower(food_name) = lower(?)",
        (food_name,),
    ).fetchone()


def diaas_override_set(
    conn: sqlite3.Connection,
    food_name: str,
    digestibility: float,
    notes: str | None = None,
) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO diaas_overrides (food_name, digestibility, notes)
           VALUES (?, ?, ?)""",
        (food_name, max(0.0, min(1.0, digestibility)), notes or None),
    )


def diaas_override_delete(
    conn: sqlite3.Connection, food_name: str
) -> bool:
    cur = conn.execute(
        "DELETE FROM diaas_overrides WHERE lower(food_name) = lower(?)",
        (food_name,),
    )
    return cur.rowcount > 0


def diaas_override_list(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM diaas_overrides ORDER BY food_name"
    ).fetchall()
