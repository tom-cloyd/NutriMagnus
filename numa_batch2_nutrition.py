"""
numa_batch2_nutrition.py
========================
Complete nutritional data (per 100 g edible portion) for 10 foods,
formatted for direct import into numa.py.

Amino acid rules (always):
  - All values in grams per 100 g FOOD (not mg, not per g protein)
  - methionine and cystine are SEPARATE keys
  - phenylalanine and tyrosine are SEPARATE keys
  - Missing values are OMITTED (never zero-filled)

Source hierarchy used:
  1. USDA FoodData Central (the exact FDC ID supplied, where data are present)
  2. USDA SR Legacy parent food (when the supplied FDC entry is sparse)
  3. Peer-reviewed literature (cited inline), with explicit flag
  
Scaling notes:
  - Chia amino acids: SR Legacy FDC 170554 is per 28 g → multiplied ×3.5714
  - Peanut butter amino acids: SR Legacy FDC 172470 is per 32 g → multiplied ×3.125
  - Dark chocolate amino acids/minerals: FDC 170273 is per 28 g → multiplied ×3.5714
  - Pumpkin seed amino acids: SR Legacy FDC 170556 is per 28 g → multiplied ×3.5714
  - Whole wheat bread: FDC 172688 is per 64 g (2 slices) → multiplied ×1.5625
  - Refried beans: FDC 174296 is per 242 g (1 cup) → multiplied ×0.4132
"""

# ──────────────────────────────────────────────────────────────
# 1. WHOLE WHEAT BREAD  FDC 1918726 (Branded)
# ──────────────────────────────────────────────────────────────
whole_wheat_bread = {
    "name": "100% Whole Wheat Bread",
    "fdc_id": 1918726,
    "fdc_type": "Branded",
    "source": (
        "Macros/minerals/vitamins: USDA SR Legacy FDC 172688 "
        "'Bread, whole-wheat, commercially prepared' (measured, per 64g scaled to 100g). "
        "Branded FDC 1918726 not directly retrievable; SR Legacy used as closest proxy. "
        "Amino acids: USDA SR Legacy FDC 172688 (no amino acid data present in this record; "
        "estimated from whole-wheat flour amino acid profile FDC 168893, protein-scaled to "
        "bread protein content of ~12.5 g/100g — moderate confidence)."
    ),
    "confidence_note": (
        "Macros and minerals HIGH confidence from SR Legacy measured record. "
        "Sodium ~455 mg/100g is characteristic of commercially prepared whole wheat bread "
        "(high — relevant for clinical sodium tracking). Amino acids are ESTIMATES scaled "
        "from whole-wheat flour protein profile; bread protein is diluted by ~39% moisture "
        "and minor ingredients (yeast, oil, sugar, salt). Verify against the specific brand "
        "label (FDC 1918726) for exact values. No vitamin A/D/B12. Fiber ~5.9 g/100g is "
        "lower than flour due to water content and processing."
    ),
    "calories": 252,
    "protein_g": 12.5,
    "carbs_g": 42.7,
    "fat_g": 3.4,
    "fiber_g": 5.9,
    "sugar_g": 4.4,
    "saturated_fat_g": 0.72,
    "mono_fat_g": 0.62,
    "poly_fat_g": 1.59,
    "calcium_mg": 161,
    "iron_mg": 2.5,
    "magnesium_mg": 75,
    "phosphorus_mg": 212,
    "potassium_mg": 254,
    "sodium_mg": 455,
    "zinc_mg": 1.72,
    "vitamin_c_mg": 0,
    "vitamin_d_mcg": 0,
    "vitamin_e_mg": 2.66,
    "vitamin_k_mcg": 7.8,
    "thiamin_mg": 0.39,
    "riboflavin_mg": 0.17,
    "niacin_mg": 4.38,
    "b6_mg": 0.22,
    "folate_mcg": 42,
    "b12_mcg": 0,
    "beta_carotene_mcg": 2,
    "lutein_zeaxanthin_mcg": 87,
    "choline_mg": 27.2,
    # Amino acids estimated from WW flour profile (FDC 168893), protein-scaled to 12.5g/100g bread
    "aa_tryptophan_g": 0.165,
    "aa_threonine_g": 0.347,
    "aa_isoleucine_g": 0.419,
    "aa_leucine_g": 0.849,
    "aa_lysine_g": 0.340,
    "aa_methionine_g": 0.216,
    "aa_cystine_g": 0.260,
    "aa_phenylalanine_g": 0.645,
    "aa_tyrosine_g": 0.260,
    "aa_valine_g": 0.533,
    "aa_histidine_g": 0.338,
}

# ──────────────────────────────────────────────────────────────
# 2. CHIA SEEDS, DRY, RAW  FDC 2710819 (Foundation)
# ──────────────────────────────────────────────────────────────
chia_seeds = {
    "name": "Chia Seeds, dry, raw",
    "fdc_id": 2710819,
    "fdc_type": "Foundation",
    "source": (
        "FDC 2710819 (Foundation): macros, select minerals (Ca 595 mg, Fe 6 mg, "
        "Mg 326 mg, P 691 mg, K 642 mg, Zn 5.6 mg), thiamin 0.50 mg, niacin 8.7 mg, "
        "B6 0.20 mg measured. Fat fractions, vitamins, folate, amino acids from "
        "USDA SR Legacy FDC 170554 'Seeds, chia seeds, dried' (measured), scaled from "
        "28g servings. Fat fraction (ALA 18.1 g, LA 5.9 g) cross-validated with "
        "Melo Ferreira et al. Molecules 2023 (doi:10.3390/molecules28020723)."
    ),
    "confidence_note": (
        "Foundation FDC 2710819 is unusually sparse — it publishes only macros and "
        "select minerals, with all fat fractions, vitamins, and amino acids missing. "
        "SR Legacy 170554 (the established chia seed record) is used for those fields. "
        "Macros show a small discrepancy: FDC 2710819 reports 517 kcal/17g protein/32.9g fat "
        "vs SR Legacy 486 kcal/16.5g protein/30.7g fat — the Foundation values (higher) are "
        "used for macro/mineral block as they are the supplied FDC ID. Amino acids from SR "
        "Legacy 170554, moderate-to-high confidence (complete essential AA profile measured). "
        "Chia is the richest plant source of ALA omega-3 (~17–18 g/100g in SR record). "
        "No sugar (confirmed 0 in SR Legacy). Notable: calcium 595 mg/100g — higher than dairy milk."
    ),
    "calories": 517,
    "protein_g": 17.0,
    "carbs_g": 38.3,
    "fat_g": 32.9,
    "fiber_g": 34.4,   # from SR Legacy 170554 (Foundation entry omits fiber)
    "sugar_g": 0,
    "saturated_fat_g": 3.33,   # SR Legacy 170554 scaled
    "mono_fat_g": 2.34,
    "poly_fat_g": 23.93,
    "calcium_mg": 595,
    "iron_mg": 6.0,
    "magnesium_mg": 326,
    "phosphorus_mg": 691,
    "potassium_mg": 642,
    "sodium_mg": 16,
    "zinc_mg": 5.6,
    "vitamin_a_mcg": 0,
    "vitamin_c_mg": 1.6,    # SR Legacy 170554
    "vitamin_e_mg": 0.50,   # SR Legacy 170554
    "thiamin_mg": 0.50,
    "riboflavin_mg": 0.18,  # SR Legacy per 28g ×3.571
    "niacin_mg": 8.7,
    "b6_mg": 0.20,
    "folate_mcg": 49,       # SR Legacy 170554 (13.9 mcg per 28g × 3.571)
    "b12_mcg": 0,
    # Amino acids: SR Legacy 170554 per 28g, ×3.5714
    "aa_tryptophan_g": 0.443,   # 124 mg/28g
    "aa_threonine_g": 0.718,    # 201 mg/28g
    "aa_isoleucine_g": 0.811,   # 227 mg/28g
    "aa_leucine_g": 1.389,      # 389 mg/28g
    "aa_lysine_g": 0.982,       # 275 mg/28g
    "aa_methionine_g": 0.596,   # 167 mg/28g
    "aa_cystine_g": 0.414,      # 116 mg/28g
    "aa_phenylalanine_g": 1.032, # 289 mg/28g
    "aa_tyrosine_g": 0.571,     # 160 mg/28g
    "aa_valine_g": 0.964,       # 270 mg/28g
    "aa_histidine_g": 0.539,    # 151 mg/28g
}

# ──────────────────────────────────────────────────────────────
# 3. DARK CHOCOLATE CHIPS  FDC 2577544 (Branded)
# ──────────────────────────────────────────────────────────────
dark_chocolate_chips = {
    "name": "Dark Chocolate Chips",
    "fdc_id": 2577544,
    "fdc_type": "Branded",
    "source": (
        "Macros/minerals/fat fractions/theobromine: USDA SR Legacy FDC 170273 "
        "'Chocolate, dark, 70-85% cacao solids' (measured, per 28g scaled to 100g). "
        "Branded FDC 2577544 not directly retrievable; SR Legacy used as closest proxy. "
        "Amino acids: not present in FDC 170273; estimated from cocoa powder SR Legacy "
        "FDC 169593 protein-scaled to 7.79g protein/100g (low confidence — flag for DIAAS use). "
        "Theobromine confirmed 813 mg/100g from SR Legacy."
    ),
    "confidence_note": (
        "Macros/minerals HIGH confidence from SR Legacy FDC 170273 (70-85% cacao). "
        "Branded chip product (FDC 2577544) may differ in exact cacao %, sugar, and "
        "emulsifier content — verify the product label. Theobromine 813 mg/100g is "
        "a notable constituent (clinically relevant: ~1.5g from 185g/6.5oz). "
        "Iron is exceptionally high at 12.0 mg/100g — one of the richest food sources. "
        "Beta-sitosterol: 86 mg/100g from SR Legacy phytosterol data. "
        "Amino acids are LOW CONFIDENCE — omit or flag for DIAAS calculations "
        "until a measured amino acid profile for the specific product is obtained. "
        "B12 in chocolate derives from traces in milk solids; dark chocolate is generally "
        "very low but SR Legacy reports a trace (0.29 mcg/100g)."
    ),
    "calories": 607,
    "protein_g": 7.79,
    "carbs_g": 46.36,
    "fat_g": 43.06,
    "fiber_g": 11.00,
    "sugar_g": 24.23,
    "saturated_fat_g": 24.49,
    "mono_fat_g": 12.78,
    "poly_fat_g": 1.28,
    "calcium_mg": 73,
    "iron_mg": 12.0,
    "magnesium_mg": 228,
    "phosphorus_mg": 308,
    "potassium_mg": 715,
    "sodium_mg": 20,
    "zinc_mg": 3.31,
    "vitamin_a_mcg": 2,
    "vitamin_e_mg": 0.59,
    "vitamin_k_mcg": 7.3,
    "thiamin_mg": 0.034,
    "riboflavin_mg": 0.078,
    "niacin_mg": 1.05,
    "b6_mg": 0.038,
    "b12_mcg": 0.29,
    "beta_carotene_mcg": 19,
    "alpha_carotene_mcg": 7,
    "lutein_zeaxanthin_mcg": 28,
    "beta_sitosterol_mg": 86,
    "theobromine_mg": 813,   # extra key — important constituent of dark chocolate
    # Amino acids: estimated from cocoa powder (FDC 169593) protein-scaled; LOW CONFIDENCE
    # Omitted per rule #4 (genuinely uncertain for this branded chip product)
    # Use only after obtaining measured data from the specific product
}

# ──────────────────────────────────────────────────────────────
# 4. NUTRITIONAL YEAST  FDC 2411476 (Branded)
# ──────────────────────────────────────────────────────────────
nutritional_yeast_2 = {
    "name": "Nutritional Yeast Flakes (FDC 2411476)",
    "fdc_id": 2411476,
    "fdc_type": "Branded",
    "source": (
        "FDC 2411476 not directly retrievable; values compiled from USDA-derived mirrors "
        "for Bragg/Bob's Red Mill-type nutritional yeast, cross-checked against prior "
        "batch entry (FDC 2676401). Amino acids from S. cerevisiae profile, USDA SR Legacy "
        "active dry yeast (FDC 172169), protein-scaled to ~50g protein/100g. "
        "B12 value assumes fortified product — verify label."
    ),
    "confidence_note": (
        "MODERATE CONFIDENCE — same organism (S. cerevisiae), different branded product "
        "from FDC 2676401 (batch 1). Key question: FORTIFIED OR NOT? If non-fortified, "
        "set B12 ≈ 0, and reduce B1/B2/B3/B6/folate to native yeast levels (~10-15% of "
        "fortified values). Protein per 100g typically 45–55g for most commercial products. "
        "This entry is functionally identical to the prior batch entry (FDC 2676401) "
        "at this level of resolution — distinguish only after pulling the specific product "
        "label. Mineral values (Mg, P, K) are estimated from S. cerevisiae composition; "
        "brand variability is high."
    ),
    "calories": 400,
    "protein_g": 50.0,
    "carbs_g": 30.0,
    "fat_g": 2.8,
    "fiber_g": 20.0,
    "sugar_g": 0,
    "calcium_mg": 50,
    "iron_mg": 10,
    "magnesium_mg": 195,
    "phosphorus_mg": 1300,
    "potassium_mg": 2100,
    "sodium_mg": 30,
    "zinc_mg": 8,
    "thiamin_mg": 62,
    "riboflavin_mg": 63,
    "niacin_mg": 350,
    "b6_mg": 72,
    "folate_mcg": 3600,
    "b12_mcg": 151,          # if fortified; 0 if unfortified — verify label
    "aa_tryptophan_g": 0.55,
    "aa_threonine_g": 2.30,
    "aa_isoleucine_g": 2.00,
    "aa_leucine_g": 3.30,
    "aa_lysine_g": 3.50,
    "aa_methionine_g": 0.70,
    "aa_cystine_g": 0.50,
    "aa_phenylalanine_g": 1.90,
    "aa_tyrosine_g": 1.10,
    "aa_valine_g": 2.50,
    "aa_histidine_g": 1.00,
}

# ──────────────────────────────────────────────────────────────
# 5. OLD FASHIONED PEANUT BUTTER  FDC 2436177 (Branded)
# ──────────────────────────────────────────────────────────────
peanut_butter_old_fashioned = {
    "name": "Old Fashioned Peanut Butter",
    "fdc_id": 2436177,
    "fdc_type": "Branded",
    "source": (
        "Macros/minerals/vitamins/fat fractions/amino acids: USDA SR Legacy FDC 172470 "
        "'Peanut butter, smooth style, without salt' (measured, per 32g scaled to 100g). "
        "Old-fashioned/natural PB is peanuts ± salt; SR Legacy unsalted smooth is the "
        "correct amino acid proxy. Sodium adjusted below: if product is salted, "
        "add ~150-200 mg/100g; unsalted version shown. "
        "Beta-sitosterol from Kritchevsky & Chen 2005 (peanuts); choline from SR Legacy."
    ),
    "confidence_note": (
        "HIGH confidence for amino acids, fat fractions, and most micronutrients — "
        "all from full SR Legacy measured record. Branded FDC 2436177 was not directly "
        "retrievable. Old-fashioned PB = peanuts (and often salt); minimal processing "
        "means the SR Legacy unsalted PB profile is an excellent proxy. If the product "
        "IS salted, sodium increases to ~140-200 mg/100g (verify label). "
        "Note: peanuts are the primary phytosterol food — beta-sitosterol ~127 mg/100g "
        "per Kritchevsky & Chen 2005. Peanut butter is lysine-limited relative to leucine."
    ),
    "calories": 598,
    "protein_g": 22.2,
    "carbs_g": 22.2,
    "fat_g": 51.4,
    "fiber_g": 5.0,
    "sugar_g": 10.6,
    "saturated_fat_g": 10.3,
    "mono_fat_g": 25.9,
    "poly_fat_g": 12.5,
    "calcium_mg": 49,
    "iron_mg": 1.75,
    "magnesium_mg": 168,
    "phosphorus_mg": 335,
    "potassium_mg": 558,
    "sodium_mg": 17,     # unsalted; salted version ~150-200 mg/100g
    "zinc_mg": 2.5,
    "vitamin_c_mg": 0,
    "vitamin_d_mcg": 0,
    "vitamin_e_mg": 9.1,
    "vitamin_k_mcg": 0.3,
    "thiamin_mg": 0.16,
    "riboflavin_mg": 0.19,
    "niacin_mg": 13.1,
    "b6_mg": 0.44,
    "folate_mcg": 87,
    "b12_mcg": 0,
    "lycopene_mcg": 0,
    "lutein_zeaxanthin_mcg": 0,
    "choline_mg": 63.1,
    "beta_sitosterol_mg": 127,
    # Amino acids: SR Legacy FDC 172470, per 32g × 3.125
    "aa_tryptophan_g": 0.231,    # 74 mg/32g
    "aa_threonine_g": 0.525,     # 168 mg/32g
    "aa_isoleucine_g": 0.616,    # 197 mg/32g
    "aa_leucine_g": 1.547,       # 495 mg/32g
    "aa_lysine_g": 0.681,        # 218 mg/32g
    "aa_methionine_g": 0.266,    # 85 mg/32g
    "aa_cystine_g": 0.228,       # 73 mg/32g
    "aa_phenylalanine_g": 1.203, # 385 mg/32g
    "aa_tyrosine_g": 0.828,      # 265 mg/32g
    "aa_valine_g": 0.781,        # 250 mg/32g
    "aa_histidine_g": 0.556,     # 178 mg/32g
}

# ──────────────────────────────────────────────────────────────
# 6. PEA PROTEIN POWDER  FDC 2608970 (Branded)
# ──────────────────────────────────────────────────────────────
pea_protein_powder_2 = {
    "name": "Pea Protein Powder (FDC 2608970)",
    "fdc_id": 2608970,
    "fdc_type": "Branded",
    "source": (
        "Macros: typical pea protein isolate label (75-85% protein, ~7% each fat/carb). "
        "Amino acids: Gorissen SHM et al., Amino Acids 2018;50(12):1685-1695 "
        "(UPLC-MS/MS analysis of commercial pea protein isolate, per 100g). "
        "Functionally identical methodology to prior batch FDC 2477360."
    ),
    "confidence_note": (
        "MODERATE CONFIDENCE — different branded product from FDC 2477360 (batch 1). "
        "At this resolution both pea protein entries are functionally indistinguishable "
        "without the specific product label. Amino acid profile from Gorissen et al. 2018 "
        "is a well-validated peer-reviewed source for commercial pea protein isolate. "
        "Methionine (0.3 g/100g) is the limiting amino acid; leucine is high (5.7 g/100g). "
        "Sodium varies widely by brand (800-1600 mg/100g typical). "
        "Distinguish from FDC 2477360 by pulling specific product label; update sodium "
        "and protein% accordingly, then re-scale amino acids proportionally."
    ),
    "calories": 400,
    "protein_g": 80.0,
    "carbs_g": 7.0,
    "fat_g": 7.0,
    "fiber_g": 3.0,
    "sugar_g": 0,
    "sodium_mg": 1200,
    "iron_mg": 9,
    "aa_tryptophan_g": 0.94,
    "aa_threonine_g": 2.50,
    "aa_isoleucine_g": 2.30,
    "aa_leucine_g": 5.70,
    "aa_lysine_g": 4.70,
    "aa_methionine_g": 0.30,
    "aa_cystine_g": 0.20,
    "aa_phenylalanine_g": 3.70,
    "aa_tyrosine_g": 2.60,
    "aa_valine_g": 2.70,
    "aa_histidine_g": 1.60,
}

# ──────────────────────────────────────────────────────────────
# 7. PEANUT BUTTER POWDER  FDC 2063659 (Branded)
# ──────────────────────────────────────────────────────────────
peanut_butter_powder = {
    "name": "Peanut Butter Powder",
    "fdc_id": 2063659,
    "fdc_type": "Branded",
    "source": (
        "Macros: representative PB powder label (PB2/Bell Plantation-type product: "
        "~45g protein, ~33g carbs, ~13g fat per 100g). "
        "Amino acids: USDA SR Legacy FDC 172430 'Peanuts, all types, raw' (measured), "
        "protein-scaled from 25.8g peanut protein to 45g PB powder protein (scale factor 1.744). "
        "Minerals: estimated from peanut composition, scaled to powder concentration factor (~1.8× "
        "vs whole peanuts reflecting fat removal and concentration of non-fat components)."
    ),
    "confidence_note": (
        "MODERATE CONFIDENCE. Peanut butter powder is defatted peanut flour — the fat "
        "content is reduced from ~50g (PB) to ~13g/100g (powder) by pressing/centrifugation. "
        "Protein is concentrated to ~45g/100g. Amino acid profile tracks whole peanut "
        "composition closely (fat removal does not alter AA ratios); values protein-scaled "
        "from SR Legacy raw peanut record. Sodium varies by brand (often 240-350 mg/100g). "
        "Verify the specific branded product (FDC 2063659) label for exact macros; re-scale "
        "amino acids if protein differs from 45g/100g. Minerals are estimates — use with caution."
    ),
    "calories": 371,
    "protein_g": 45.0,
    "carbs_g": 33.0,
    "fat_g": 13.0,
    "fiber_g": 6.0,
    "sugar_g": 9.0,
    "saturated_fat_g": 2.0,
    "sodium_mg": 280,
    "calcium_mg": 80,
    "iron_mg": 3.0,
    "magnesium_mg": 230,
    "phosphorus_mg": 590,
    "potassium_mg": 900,
    "zinc_mg": 4.5,
    "niacin_mg": 22.0,
    "folate_mcg": 150,
    "choline_mg": 95,
    # Amino acids: peanut SR Legacy 172430, protein-scaled from 25.8→45g (×1.744)
    "aa_tryptophan_g": 0.494,
    "aa_threonine_g": 1.133,
    "aa_isoleucine_g": 1.376,
    "aa_leucine_g": 2.716,
    "aa_lysine_g": 1.438,
    "aa_methionine_g": 0.518,
    "aa_cystine_g": 0.476,
    "aa_phenylalanine_g": 2.189,
    "aa_tyrosine_g": 1.541,
    "aa_valine_g": 1.748,
    "aa_histidine_g": 1.022,
}

# ──────────────────────────────────────────────────────────────
# 8. REFRIED BEANS, CANNED, VEGETARIAN  FDC 174296 (SR Legacy)
# ──────────────────────────────────────────────────────────────
refried_beans = {
    "name": "Refried Beans, canned, vegetarian",
    "fdc_id": 174296,
    "fdc_type": "SR Legacy",
    "source": (
        "Macros/minerals/fat fractions: USDA SR Legacy FDC 174296 (measured), "
        "per 242g (1 cup) scaled to 100g (×0.4132). "
        "Amino acids: USDA SR Legacy FDC 175194 'Beans, pinto, canned, solids and liquids' "
        "protein-scaled to 5.3g protein/100g refried beans — moderate confidence. "
        "Sodium: FDC 174296 reports 1040 mg per 242g = 430 mg/100g."
    ),
    "confidence_note": (
        "Macros, minerals, and fat fractions are HIGH confidence (fully measured SR Legacy). "
        "This is a vegetarian product — no lard. Sodium 430 mg/100g is HIGH "
        "(canned beans; ~180% more than home-cooked). Amino acids are ESTIMATED from "
        "pinto bean composition protein-scaled to the refried beans protein content "
        "(5.3g/100g); moderate confidence. Folate data not present in FDC 174296 SR Legacy "
        "record — pinto beans are a major folate source (~150 µg/100g raw beans) but "
        "canning and water content dilute this substantially; omitted rather than estimated. "
        "Isoflavones not reported (pinto beans have trace/negligible isoflavones vs soy)."
    ),
    "calories": 83,
    "protein_g": 5.3,
    "carbs_g": 13.5,
    "fat_g": 0.87,
    "fiber_g": 4.7,
    "sugar_g": 0.58,
    "saturated_fat_g": 0.14,
    "mono_fat_g": 0.21,
    "poly_fat_g": 0.47,
    "calcium_mg": 35,
    "iron_mg": 1.70,
    "magnesium_mg": 38,
    "phosphorus_mg": 114,
    "potassium_mg": 344,
    "sodium_mg": 430,
    "zinc_mg": 0.74,
    "vitamin_e_mg": 0.09,
    "thiamin_mg": 0.041,
    "riboflavin_mg": 0.017,
    "niacin_mg": 0.37,
    "b6_mg": 0.107,
    # Amino acids: estimated from pinto bean SR Legacy, protein-scaled to 5.3g/100g
    "aa_tryptophan_g": 0.059,
    "aa_threonine_g": 0.222,
    "aa_isoleucine_g": 0.243,
    "aa_leucine_g": 0.403,
    "aa_lysine_g": 0.348,
    "aa_methionine_g": 0.065,
    "aa_cystine_g": 0.055,
    "aa_phenylalanine_g": 0.273,
    "aa_tyrosine_g": 0.163,
    "aa_valine_g": 0.261,
    "aa_histidine_g": 0.149,
}

# ──────────────────────────────────────────────────────────────
# 9. PUMPKIN SEEDS (PEPITAS), RAW  FDC 2515380 (Foundation)
# ──────────────────────────────────────────────────────────────
pumpkin_seeds = {
    "name": "Pumpkin Seeds (Pepitas), raw",
    "fdc_id": 2515380,
    "fdc_type": "Foundation",
    "source": (
        "FDC 2515380 (Foundation): macros (555 kcal, 29.9g protein, 40g fat, 18.7g carbs, "
        "5.1g fiber), and minerals (Ca 37.4, Fe 8.4, Mg 499.7, P 1150, K 691.2, Zn 6.3 mg, "
        "Se 20.5 mcg) — measured. Fat fractions, vitamins, amino acids from "
        "USDA SR Legacy FDC 170556 'Seeds, pumpkin and squash seed kernels, dried' "
        "(measured, per 28g scaled to 100g × 3.5714). "
        "Beta-sitosterol from Piironen et al. 2000 (pumpkin seed phytosterol data)."
    ),
    "confidence_note": (
        "Foundation FDC 2515380 has good macro/mineral data but is missing all fat fractions, "
        "vitamins, and amino acids — supplemented from SR Legacy FDC 170556 (raw dried pepita "
        "kernels; essentially same food). Mineral values from FDC 2515380 are the primary "
        "source (Foundation measured data); they differ slightly from SR Legacy "
        "(e.g., Mg 500 mg in Foundation vs 598 mg in SR Legacy — use Foundation values). "
        "Amino acids from SR Legacy HIGH confidence (full measured profile). "
        "Pumpkin seeds are exceptional: magnesium 500 mg/100g, zinc 6.3 mg/100g, "
        "phosphorus 1150 mg/100g, iron 8.4 mg/100g — among the highest of any common food. "
        "Arginine is very high (5.4 g/100g) — relevant for DIAAS/clinical protein quality. "
        "Beta-sitosterol ~117 mg/100g per Piironen et al. 2000."
    ),
    "calories": 555,
    "protein_g": 29.9,
    "carbs_g": 18.7,
    "fat_g": 40.0,
    "fiber_g": 5.1,
    "sugar_g": 1.4,
    "saturated_fat_g": 8.9,     # SR Legacy 170556 per 28g (2.5g) ×3.571
    "mono_fat_g": 16.5,         # 4.613g/28g ×3.571
    "poly_fat_g": 21.3,         # 5.957g/28g ×3.571
    "calcium_mg": 37.4,
    "iron_mg": 8.4,
    "magnesium_mg": 500,
    "phosphorus_mg": 1150,
    "potassium_mg": 691,
    "sodium_mg": 7,
    "zinc_mg": 6.3,
    "vitamin_a_mcg": 1.0,       # SR Legacy per 28g (0.28 mcg) ×3.571
    "vitamin_c_mg": 1.9,        # SR Legacy (0.54 mg/28g) ×3.571
    "vitamin_d_mcg": 0,
    "vitamin_e_mg": 2.2,        # SR Legacy (0.62 mg/28g) ×3.571
    "vitamin_k_mcg": 7.5,       # SR Legacy (2.1 mcg/28g) ×3.571
    "thiamin_mg": 0.29,         # SR Legacy (0.08 mg/28g) ×3.571
    "riboflavin_mg": 0.14,      # SR Legacy (0.04 mg/28g) ×3.571
    "niacin_mg": 5.0,           # SR Legacy (1.4 mg/28g) ×3.571
    "b6_mg": 0.14,              # SR Legacy (0.04 mg/28g) ×3.571
    "folate_mcg": 59,           # SR Legacy (16.5 mcg/28g) ×3.571
    "b12_mcg": 0,
    "beta_carotene_mcg": 9.3,   # SR Legacy (2.6 mcg/28g) ×3.571
    "lutein_zeaxanthin_mcg": 75, # SR Legacy (21 mcg/28g) ×3.571
    "choline_mg": 63.9,         # SR Legacy (17.9 mg/28g) ×3.571
    "beta_sitosterol_mg": 117,  # Piironen et al. 2000, estimated
    # Amino acids: SR Legacy FDC 170556 per 28g × 3.5714
    "aa_tryptophan_g": 0.586,   # 164 mg/28g
    "aa_threonine_g": 1.011,    # 283 mg/28g
    "aa_isoleucine_g": 1.300,   # 364 mg/28g
    "aa_leucine_g": 2.454,      # 687 mg/28g
    "aa_lysine_g": 1.254,       # 351 mg/28g
    "aa_methionine_g": 0.611,   # 171 mg/28g
    "aa_cystine_g": 0.336,      # 94 mg/28g
    "aa_phenylalanine_g": 1.757, # 492 mg/28g
    "aa_tyrosine_g": 1.107,     # 310 mg/28g
    "aa_valine_g": 1.600,       # 448 mg/28g
    "aa_histidine_g": 0.793,    # 222 mg/28g
}

# ──────────────────────────────────────────────────────────────
# 10. WHOLE WHEAT PASTA  FDC 1865558 (Branded)
# ──────────────────────────────────────────────────────────────
whole_wheat_pasta = {
    "name": "Whole Wheat Pasta (dry)",
    "fdc_id": 1865558,
    "fdc_type": "Branded",
    "source": (
        "Macros/minerals/vitamins: USDA SR Legacy FDC 168930 "
        "'Pasta, whole-wheat, dry' (measured). "
        "Branded FDC 1865558 not directly retrievable; SR Legacy used as closest proxy. "
        "Amino acids: USDA SR Legacy FDC 168930 (full measured amino acid profile). "
        "Reported on DRY basis — cooking approximately doubles water weight, "
        "diluting all values by ~50-55% (see cooked note below)."
    ),
    "confidence_note": (
        "HIGH confidence for macros/minerals/amino acids from full SR Legacy measured record "
        "FDC 168930. Branded product FDC 1865558 likely matches this profile closely "
        "(whole wheat pasta is a commodity with consistent composition). "
        "VALUES ARE FOR DRY PASTA — multiply by ~0.44 to approximate per-100g-cooked values "
        "(cooked whole wheat pasta: ~124 kcal, ~5.3g protein, ~25g carbs per 100g cooked). "
        "Notable: whole wheat pasta retains more fiber (6.3g/100g dry) and protein (14.6g) "
        "than refined pasta. Amino acid profile is wheat-based — lysine is the limiting AA "
        "(classic for wheat proteins; 0.35g/100g dry pasta)."
    ),
    "calories": 348,
    "protein_g": 14.6,
    "carbs_g": 75.0,
    "fat_g": 1.7,
    "fiber_g": 6.3,
    "sugar_g": 0,
    "saturated_fat_g": 0.32,
    "mono_fat_g": 0.22,
    "poly_fat_g": 0.72,
    "calcium_mg": 35,
    "iron_mg": 3.63,
    "magnesium_mg": 143,
    "phosphorus_mg": 268,
    "potassium_mg": 277,
    "sodium_mg": 8,
    "zinc_mg": 2.57,
    "vitamin_c_mg": 0,
    "vitamin_d_mcg": 0,
    "vitamin_e_mg": 0.83,
    "vitamin_k_mcg": 0.9,
    "thiamin_mg": 0.34,
    "riboflavin_mg": 0.11,
    "niacin_mg": 5.14,
    "b6_mg": 0.26,
    "folate_mcg": 29,
    "b12_mcg": 0,
    "lutein_zeaxanthin_mcg": 185,
    "choline_mg": 36.9,
    # Amino acids from SR Legacy FDC 168930 (measured, per 100g dry pasta)
    "aa_tryptophan_g": 0.195,
    "aa_threonine_g": 0.443,
    "aa_isoleucine_g": 0.576,
    "aa_leucine_g": 1.024,
    "aa_lysine_g": 0.350,
    "aa_methionine_g": 0.220,
    "aa_cystine_g": 0.304,
    "aa_phenylalanine_g": 0.740,
    "aa_tyrosine_g": 0.362,
    "aa_valine_g": 0.617,
    "aa_histidine_g": 0.342,
}


# ──────────────────────────────────────────────────────────────
# MASTER LIST — import this into numa.py
# ──────────────────────────────────────────────────────────────
BATCH2_FOODS = [
    whole_wheat_bread,
    chia_seeds,
    dark_chocolate_chips,
    nutritional_yeast_2,
    peanut_butter_old_fashioned,
    pea_protein_powder_2,
    peanut_butter_powder,
    refried_beans,
    pumpkin_seeds,
    whole_wheat_pasta,
]


_META_KEYS = {"name", "fdc_id", "fdc_type", "source", "confidence_note"}

_VALID_KEYS = {
    "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
    "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
    "potassium_mg", "sodium_mg", "zinc_mg",
    "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
    "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
    "b6_mg", "folate_mcg", "b12_mcg",
    "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
    "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg", "isoflavones_mg",
    "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
    "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
    "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g",
}

if __name__ == "__main__":
    import sys
    import pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import db as _db

    print(f"Importing {len(BATCH2_FOODS)} food(s) into numa cache at {_db.get_db_path()}\n")
    with _db.get_db() as conn:
        for food in BATCH2_FOODS:
            nutrients = {k: v for k, v in food.items() if k in _VALID_KEYS}
            stripped = set(food) - _VALID_KEYS - _META_KEYS
            notes_parts = []
            if food.get("source"):
                notes_parts.append(food["source"])
            if food.get("confidence_note"):
                notes_parts.append(food["confidence_note"])
            _db.cache_food(
                conn,
                fdc_id=food["fdc_id"],
                name=food["name"],
                data_type=food.get("fdc_type", "SR Legacy"),
                brand=None,
                serving_size=None,
                serving_unit=None,
                nutrients=nutrients,
                portions=None,
                notes=" | ".join(notes_parts) or None,
            )
            aa_count = sum(1 for k in nutrients if k.startswith("aa_"))
            suffix = f"  [stripped: {', '.join(sorted(stripped))}]" if stripped else ""
            print(f"  ✓  {food['name']} (FDC {food['fdc_id']})  — {aa_count} AAs{suffix}")
    print("\nDone. Foods are now in the cache and will appear in local search results.")