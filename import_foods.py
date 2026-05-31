"""
import_foods.py — import manually-compiled food records into the numa food cache.

Usage:
    1. Add entries to _FOODS below (each with fdc_id, name, data_type, notes, nutrients).
    2. Run:  python import_foods.py
    3. Foods appear immediately in numa's local cache search.

Safe to re-run: cache_food() uses INSERT OR REPLACE, so existing entries are
updated in place if the fdc_id already exists.

Nutrient rules (all values per 100 g):
  - Amino acids in grams (not mg, not per-gram-protein).
  - aa_methionine_g and aa_cystine_g are always separate keys.
  - aa_phenylalanine_g and aa_tyrosine_g are always separate keys.
  - Omit unknown values entirely (never zero-fill unknowns).
  - True zeros (e.g. b12_mcg in plant foods) may be included explicitly.

Extra keys not in _VALID_KEYS (e.g. selenium_mcg, sdg_lignan_mg) are stripped
automatically — put them in the notes string instead.

data_type conventions:
  "SR Legacy"    — data sourced from USDA SR Legacy records
  "Foundation"   — data sourced from USDA Foundation records
  "Branded"      — USDA Branded Foods entry (brand-dependent; flag in notes)
  "User Drafted" — fully user-estimated, no USDA anchor
"""
import sys
import pathlib

# Make sure we can import numa's db module from this directory.
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import db as _db

# ---------------------------------------------------------------------------
# Valid nutrient keys accepted by numa's nutrient dict.
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Foods to import.  Add new entries here each time you run the script.
# Previously imported entries can be left in place (INSERT OR REPLACE is safe).
# Each entry: fdc_id, name, data_type, notes, nutrients dict.
# ---------------------------------------------------------------------------
_FOODS = [
    {
        "fdc_id":    2261420,
        "name":      "Almond Flour",
        "data_type": "SR Legacy",
        "notes":     "Source: USDA SR Legacy FDC 170567 (whole almonds, measured). "
                     "Almond flour is ground almonds; per-100g composition near-identical. "
                     "High confidence for macros/minerals/amino acids. "
                     "Blanched flour slightly lower in fiber and calcium vs. whole.",
        "nutrients": {
            "calories": 579, "protein_g": 21.2, "carbs_g": 21.6, "fat_g": 49.9,
            "fiber_g": 12.5, "sugar_g": 4.4, "saturated_fat_g": 3.8,
            "mono_fat_g": 31.6, "poly_fat_g": 12.3,
            "calcium_mg": 269, "iron_mg": 3.7, "magnesium_mg": 270,
            "phosphorus_mg": 481, "potassium_mg": 733, "sodium_mg": 1, "zinc_mg": 3.1,
            "vitamin_c_mg": 0, "vitamin_e_mg": 25.6, "vitamin_k_mcg": 0,
            "thiamin_mg": 0.21, "riboflavin_mg": 1.14, "niacin_mg": 3.6,
            "b6_mg": 0.14, "folate_mcg": 44, "b12_mcg": 0,
            "beta_carotene_mcg": 1, "lutein_zeaxanthin_mcg": 1,
            "choline_mg": 52.1, "beta_sitosterol_mg": 132,
            "aa_tryptophan_g": 0.214, "aa_threonine_g": 0.611,
            "aa_isoleucine_g": 0.751, "aa_leucine_g": 1.488,
            "aa_lysine_g": 0.580, "aa_methionine_g": 0.157, "aa_cystine_g": 0.215,
            "aa_phenylalanine_g": 1.132, "aa_tyrosine_g": 0.452,
            "aa_valine_g": 0.855, "aa_histidine_g": 0.539,
        },
    },
    {
        "fdc_id":    790085,
        "name":      "Whole Wheat Flour, unenriched",
        "data_type": "SR Legacy",
        "notes":     "Source: USDA SR Legacy FDC 168893 (wheat flour, whole-grain, measured). "
                     "High confidence; all values measured. Dry flour, 100g basis. "
                     "Iron 3.6 mg is native grain (unenriched). No vitamin A/C/D/B12.",
        "nutrients": {
            "calories": 340, "protein_g": 13.2, "carbs_g": 72.0, "fat_g": 2.5,
            "fiber_g": 10.7, "sugar_g": 0.41, "saturated_fat_g": 0.43,
            "mono_fat_g": 0.28, "poly_fat_g": 1.17,
            "calcium_mg": 34, "iron_mg": 3.6, "magnesium_mg": 137,
            "phosphorus_mg": 357, "potassium_mg": 363, "sodium_mg": 2, "zinc_mg": 2.6,
            "vitamin_c_mg": 0, "vitamin_e_mg": 0.71, "vitamin_k_mcg": 1.9,
            "thiamin_mg": 0.50, "riboflavin_mg": 0.17, "niacin_mg": 4.96,
            "b6_mg": 0.41, "folate_mcg": 44, "b12_mcg": 0,
            "beta_carotene_mcg": 5, "lutein_zeaxanthin_mcg": 220, "choline_mg": 31.2,
            "aa_tryptophan_g": 0.174, "aa_threonine_g": 0.367,
            "aa_isoleucine_g": 0.443, "aa_leucine_g": 0.898,
            "aa_lysine_g": 0.359, "aa_methionine_g": 0.228, "aa_cystine_g": 0.275,
            "aa_phenylalanine_g": 0.682, "aa_tyrosine_g": 0.275,
            "aa_valine_g": 0.564, "aa_histidine_g": 0.357,
        },
    },
    {
        "fdc_id":    1868897,
        "name":      "Ground Flax Seeds",
        "data_type": "SR Legacy",
        "notes":     "Source: USDA SR Legacy FDC 169414 (flaxseed, measured). "
                     "Grinding does not alter per-100g composition vs. whole seed. "
                     "High confidence for macros/minerals/amino acids. "
                     "sdg_lignan_mg ~845 (midpoint of literature 600-1090 mg/100g range, "
                     "Corsato Alvarenga et al. 2014) — stored in notes only, not nutrient dict.",
        "nutrients": {
            "calories": 534, "protein_g": 18.3, "carbs_g": 28.9, "fat_g": 42.2,
            "fiber_g": 27.3, "sugar_g": 1.55, "saturated_fat_g": 3.66,
            "mono_fat_g": 7.53, "poly_fat_g": 28.73,
            "calcium_mg": 255, "iron_mg": 5.7, "magnesium_mg": 392,
            "phosphorus_mg": 642, "potassium_mg": 813, "sodium_mg": 30, "zinc_mg": 4.3,
            "vitamin_c_mg": 0.6, "vitamin_e_mg": 0.31, "vitamin_k_mcg": 4.3,
            "thiamin_mg": 1.64, "riboflavin_mg": 0.16, "niacin_mg": 3.08,
            "b6_mg": 0.47, "folate_mcg": 87, "b12_mcg": 0,
            "beta_carotene_mcg": 0, "lutein_zeaxanthin_mcg": 651,
            "choline_mg": 78.7, "beta_sitosterol_mg": 92,
            "aa_tryptophan_g": 0.297, "aa_threonine_g": 0.766,
            "aa_isoleucine_g": 0.896, "aa_leucine_g": 1.235,
            "aa_lysine_g": 0.862, "aa_methionine_g": 0.370, "aa_cystine_g": 0.340,
            "aa_phenylalanine_g": 0.957, "aa_tyrosine_g": 0.493,
            "aa_valine_g": 1.072, "aa_histidine_g": 0.472,
        },
    },
    {
        "fdc_id":    2676401,
        "name":      "Nutritional Yeast Flakes (fortified)",
        "data_type": "SR Legacy",
        "notes":     "Source: USDA branded nutritional yeast records (Bragg/Now Foods) + "
                     "S. cerevisiae SR data + peer-reviewed amino acid analysis. "
                     "Moderate confidence. B-vitamin values REFLECT FORTIFICATION — "
                     "non-fortified product would have much lower B1/B2/B3/B6/folate and ~0 B12. "
                     "Mineral data partial; phosphorus/magnesium/zinc/calcium are typical "
                     "S. cerevisiae estimates. Brand variability is large — verify against label.",
        "nutrients": {
            "calories": 400, "protein_g": 50.0, "carbs_g": 30.0, "fat_g": 2.8,
            "fiber_g": 20.0, "sugar_g": 0, "saturated_fat_g": 0,
            "calcium_mg": 50, "iron_mg": 10, "magnesium_mg": 195,
            "phosphorus_mg": 1300, "potassium_mg": 2100, "sodium_mg": 30, "zinc_mg": 8,
            "thiamin_mg": 62, "riboflavin_mg": 63, "niacin_mg": 350,
            "b6_mg": 72, "folate_mcg": 3600, "b12_mcg": 151,
            "aa_tryptophan_g": 0.55, "aa_threonine_g": 2.3,
            "aa_isoleucine_g": 2.0, "aa_leucine_g": 3.3,
            "aa_lysine_g": 3.5, "aa_methionine_g": 0.7, "aa_cystine_g": 0.5,
            "aa_phenylalanine_g": 1.9, "aa_tyrosine_g": 1.1,
            "aa_valine_g": 2.5, "aa_histidine_g": 1.0,
        },
    },
    {
        "fdc_id":    2346396,
        "name":      "Oats, whole grain, rolled, old fashioned (dry)",
        "data_type": "Foundation",
        "notes":     "Source: USDA Foundation FDC 2346396 (dry macros/minerals, measured); "
                     "amino acids/fat fractions from USDA SR Legacy FDC 169705. "
                     "High confidence dry values. "
                     "Cooked-in-water (FDC 173905): ~68 kcal/100g, ~2.56g protein — "
                     "roughly 5.6x caloric dilution. Use dry basis for analysis.",
        "nutrients": {
            "calories": 382, "protein_g": 13.5, "carbs_g": 68.7, "fat_g": 5.9,
            "fiber_g": 10.1, "sugar_g": 1.0, "saturated_fat_g": 1.05,
            "mono_fat_g": 1.98, "poly_fat_g": 2.30,
            "calcium_mg": 45.5, "iron_mg": 4.3, "magnesium_mg": 126,
            "phosphorus_mg": 387, "potassium_mg": 350, "sodium_mg": 0.7, "zinc_mg": 2.7,
            "thiamin_mg": 0.41, "riboflavin_mg": 0.14, "niacin_mg": 0.99,
            "b6_mg": 0.14, "folate_mcg": 32, "b12_mcg": 0,
            "aa_tryptophan_g": 0.234, "aa_threonine_g": 0.575,
            "aa_isoleucine_g": 0.694, "aa_leucine_g": 1.284,
            "aa_lysine_g": 0.701, "aa_methionine_g": 0.312, "aa_cystine_g": 0.408,
            "aa_phenylalanine_g": 0.895, "aa_tyrosine_g": 0.573,
            "aa_valine_g": 0.937, "aa_histidine_g": 0.405,
        },
    },
    {
        "fdc_id":    2396330,
        "name":      "Pure Okara Flour (dried)",
        "data_type": "SR Legacy",
        "notes":     "Source: literature (Mateos-Aparicio et al. 2010; Santos et al. 2019; Li et al.); "
                     "amino acids scaled from USDA wet-okara FDC 172452 to dry basis. "
                     "Moderate confidence; brand- and drying-method-dependent. "
                     "USDA wet okara (FDC 172452) is ~82% moisture, 76 kcal/3.5g protein per 100g; "
                     "dry okara flour here: ~25% protein, ~50% dietary fiber, ~10% fat. "
                     "isoflavones_mg ~100 is a representative total-isoflavone estimate "
                     "(varies strongly with drying temperature).",
        "nutrients": {
            "calories": 400, "protein_g": 25.0, "carbs_g": 53.0, "fat_g": 10.0,
            "fiber_g": 50.0,
            "calcium_mg": 126, "iron_mg": 4.45, "magnesium_mg": 100,
            "phosphorus_mg": 313, "potassium_mg": 286, "zinc_mg": 3.14,
            "isoflavones_mg": 100,
            "aa_tryptophan_g": 0.36, "aa_threonine_g": 0.94,
            "aa_isoleucine_g": 1.14, "aa_leucine_g": 1.74,
            "aa_lysine_g": 1.52, "aa_methionine_g": 0.29, "aa_cystine_g": 0.31,
            "aa_phenylalanine_g": 1.12, "aa_tyrosine_g": 0.77,
            "aa_valine_g": 1.16, "aa_histidine_g": 0.66,
        },
    },
    {
        "fdc_id":    2543837,
        "name":      "Raw Brazil Nuts",
        "data_type": "SR Legacy",
        "notes":     "Source: USDA SR Legacy FDC 170569 (brazil nuts, dried unblanched, measured). "
                     "High confidence; full measured profile. "
                     "selenium_mcg ~1917/100g (3485% DV) — not stored in nutrient dict "
                     "(no selenium key in schema) but noted here. One nut can exceed adult RDA. "
                     "Methionine unusually high at 1.135g/100g — consistent with selenomethionine content.",
        "nutrients": {
            "calories": 659, "protein_g": 14.3, "carbs_g": 11.7, "fat_g": 67.1,
            "fiber_g": 7.5, "sugar_g": 2.3, "saturated_fat_g": 16.13,
            "mono_fat_g": 24.55, "poly_fat_g": 24.40,
            "calcium_mg": 160, "iron_mg": 2.4, "magnesium_mg": 376,
            "phosphorus_mg": 725, "potassium_mg": 659, "sodium_mg": 3, "zinc_mg": 4.1,
            "vitamin_c_mg": 0.7, "vitamin_e_mg": 5.7,
            "thiamin_mg": 0.62, "riboflavin_mg": 0.04, "niacin_mg": 0.30,
            "b6_mg": 0.10, "folate_mcg": 22, "b12_mcg": 0,
            "choline_mg": 28.8, "beta_sitosterol_mg": 64,
            "aa_tryptophan_g": 0.135, "aa_threonine_g": 0.370,
            "aa_isoleucine_g": 0.524, "aa_leucine_g": 1.207,
            "aa_lysine_g": 0.492, "aa_methionine_g": 1.135, "aa_cystine_g": 0.310,
            "aa_phenylalanine_g": 0.645, "aa_tyrosine_g": 0.420,
            "aa_valine_g": 0.770, "aa_histidine_g": 0.386,
        },
    },
    {
        "fdc_id":    2515381,
        "name":      "Sunflower Seed Kernels, raw",
        "data_type": "SR Legacy",
        "notes":     "Source: USDA SR Legacy FDC 170562 (sunflower seed kernels, dried, measured). "
                     "High confidence; full measured profile. "
                     "beta_sitosterol_mg 534 represents TOTAL phytosterols from the SR record "
                     "(beta-sitosterol fraction not separately resolved). "
                     "Notably high vitamin E (35.17 mg) and folate (227 mcg).",
        "nutrients": {
            "calories": 584, "protein_g": 20.8, "carbs_g": 20.0, "fat_g": 51.5,
            "fiber_g": 8.6, "sugar_g": 2.62, "saturated_fat_g": 4.46,
            "mono_fat_g": 18.53, "poly_fat_g": 23.14,
            "calcium_mg": 78, "iron_mg": 5.25, "magnesium_mg": 325,
            "phosphorus_mg": 660, "potassium_mg": 645, "sodium_mg": 9, "zinc_mg": 5.0,
            "vitamin_c_mg": 1.4, "vitamin_e_mg": 35.17, "vitamin_k_mcg": 0,
            "thiamin_mg": 1.48, "riboflavin_mg": 0.355, "niacin_mg": 8.335,
            "b6_mg": 1.345, "folate_mcg": 227, "b12_mcg": 0,
            "beta_carotene_mcg": 30, "choline_mg": 55.1, "beta_sitosterol_mg": 534,
            "aa_tryptophan_g": 0.348, "aa_threonine_g": 0.928,
            "aa_isoleucine_g": 1.139, "aa_leucine_g": 1.659,
            "aa_lysine_g": 0.937, "aa_methionine_g": 0.494, "aa_cystine_g": 0.451,
            "aa_phenylalanine_g": 1.169, "aa_tyrosine_g": 0.666,
            "aa_valine_g": 1.315, "aa_histidine_g": 0.632,
        },
    },
    {
        "fdc_id":    2477360,
        "name":      "Unsweetened Pea Protein Powder (isolate)",
        "data_type": "SR Legacy",
        "notes":     "Source: macros from typical pea protein isolate labels; "
                     "amino acids from Gorissen et al. Amino Acids 2018;50(12):1685-1695 (UPLC-MS/MS). "
                     "Moderate confidence; brand-dependent. Methionine is the limiting AA. "
                     "Mineral data is brand-dependent; sodium and iron are representative label values.",
        "nutrients": {
            "calories": 400, "protein_g": 80.0, "carbs_g": 7.0, "fat_g": 7.0,
            "fiber_g": 3.0, "sugar_g": 0,
            "sodium_mg": 1200, "iron_mg": 9,
            "aa_tryptophan_g": 0.94, "aa_threonine_g": 2.5,
            "aa_isoleucine_g": 2.3, "aa_leucine_g": 5.7,
            "aa_lysine_g": 4.7, "aa_methionine_g": 0.3, "aa_cystine_g": 0.2,
            "aa_phenylalanine_g": 3.7, "aa_tyrosine_g": 2.6,
            "aa_valine_g": 2.7, "aa_histidine_g": 1.6,
        },
    },
]


def main() -> None:
    if not _FOODS:
        print("No foods in _FOODS list — nothing to import.")
        return
    print(f"Importing {len(_FOODS)} food(s) into numa cache at {_db.get_db_path()}\n")
    with _db.get_db() as conn:
        for food in _FOODS:
            nutrients = {k: v for k, v in food["nutrients"].items() if k in _VALID_KEYS}
            stripped = set(food["nutrients"]) - _VALID_KEYS
            _db.cache_food(
                conn,
                fdc_id=food["fdc_id"],
                name=food["name"],
                data_type=food["data_type"],
                brand=None,
                serving_size=None,
                serving_unit=None,
                nutrients=nutrients,
                portions=None,
                notes=food.get("notes"),
            )
            aa_count = sum(1 for k in nutrients if k.startswith("aa_"))
            suffix = f"  [stripped: {', '.join(sorted(stripped))}]" if stripped else ""
            print(f"  ✓  {food['name']} (FDC {food['fdc_id']})  — {aa_count} AAs{suffix}")
    print("\nDone. Foods are now in the cache and will appear in local search results.")


if __name__ == "__main__":
    main()
