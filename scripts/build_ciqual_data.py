#!/usr/bin/env python3
"""
build_ciqual_data.py — regenerate ciqual_data.json from the published French
CIQUAL 2020 food composition table (English-language XLS export).

CIQUAL is a static download, not a live API — this script is the one-time
ingest step, run by a developer, not by numa at runtime (see
ciqual_lookup.py's module docstring for the static-vs-live source distinction).

Usage:
    pip install xlrd       # not a runtime dependency — only this script needs it
    python scripts/build_ciqual_data.py path/to/Ciqual2020_ENG_2020_07_07.xls

Source spreadsheet: ANSES, "Table de composition nutritionnelle des aliments
Ciqual 2020" (English-language version), published via data.gouv.fr:
https://www.data.gouv.fr/fr/datasets/table-de-composition-nutritionnelle-des-aliments-ciqual/
Not redistributed here — download it yourself and pass the path in. Use the
English-language XLS (English column headers), not the French one — both
carry the same data.

CIQUAL's file is the legacy .xls format (not .xlsx), hence xlrd rather than
openpyxl. No amino-acid data — CIQUAL's public dataset has none (unlike
Canadian Nutrient File or AFCD). Cells use French locale formatting: a comma
decimal separator ("9,15") and "-" for not-analyzed/missing, both handled
below. Retinol and beta-carotene are reported separately, with no combined
RAE-style vitamin A figure — retinol alone is used for vitamin_a_mcg (the
same approximation used for Canadian Nutrient File).
"""
import json
import sys
from pathlib import Path

try:
    import xlrd
except ImportError:
    print("This script needs xlrd: pip install xlrd (not a runtime dependency)")
    sys.exit(1)

OUTPUT = Path(__file__).parent.parent / "ciqual_data.json"

# {column label -> (our_key, multiplier)}. Multiplier converts CIQUAL's unit
# to ours — mostly 1.0; the fatty-acid columns are g/100g, ours want mg for
# the omega-3/6 keys.
_COLUMN_MAP: dict[str, tuple[str, float]] = {
    "Protein (g/100g)":                                    ("protein_g",        1.0),
    "Fat (g/100g)":                                         ("fat_g",            1.0),
    "Carbohydrate (g/100g)":                                 ("carbs_g",          1.0),
    "Fibres (g/100g)":                                       ("fiber_g",          1.0),
    "Sugars (g/100g)":                                       ("sugar_g",          1.0),
    "FA saturated (g/100g)":                                 ("saturated_fat_g",  1.0),
    "FA mono (g/100g)":                                      ("mono_fat_g",       1.0),
    "FA poly (g/100g)":                                      ("poly_fat_g",       1.0),
    "FA 18:3 c9,c12,c15 (n-3) (g/100g)":                     ("omega3_ala_mg",    1000.0),
    "FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)":          ("omega3_epa_mg",    1000.0),
    "FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)":      ("omega3_dha_mg",    1000.0),
    "FA 18:2 9c,12c (n-6) (g/100g)":                         ("omega6_la_mg",     1000.0),
    "Calcium (mg/100g)":                                     ("calcium_mg",       1.0),
    "Iron (mg/100g)":                                        ("iron_mg",          1.0),
    "Iodine (µg/100g)":                                      ("iodine_mcg",       1.0),
    "Magnesium (mg/100g)":                                   ("magnesium_mg",     1.0),
    "Phosphorus (mg/100g)":                                  ("phosphorus_mg",    1.0),
    "Potassium (mg/100g)":                                   ("potassium_mg",     1.0),
    "Selenium (µg/100g)":                                    ("selenium_mcg",     1.0),
    "Sodium (mg/100g)":                                      ("sodium_mg",        1.0),
    "Zinc (mg/100g)":                                        ("zinc_mg",          1.0),
    # Retinol only — CIQUAL has no combined RAE-style vitamin A figure.
    "Retinol (µg/100g)":                                     ("vitamin_a_mcg",    1.0),
    "Beta-carotene (µg/100g)":                                ("beta_carotene_mcg", 1.0),
    "Vitamin C (mg/100g)":                                    ("vitamin_c_mg",     1.0),
    "Vitamin D (µg/100g)":                                    ("vitamin_d_mcg",    1.0),
    "Vitamin E (mg/100g)":                                    ("vitamin_e_mg",     1.0),
    "Vitamin K1 (µg/100g)":                                   ("vitamin_k_mcg",    1.0),  # K1 only, not K1+K2
    "Vitamin B1 or Thiamin (mg/100g)":                        ("thiamin_mg",       1.0),
    "Vitamin B2 or Riboflavin (mg/100g)":                     ("riboflavin_mg",    1.0),
    "Vitamin B3 or Niacin (mg/100g)":                         ("niacin_mg",        1.0),
    "Vitamin B6 (mg/100g)":                                   ("b6_mg",            1.0),
    "Vitamin B9 or Folate (µg/100g)":                         ("folate_mcg",       1.0),
    "Vitamin B12 (µg/100g)":                                  ("b12_mcg",          1.0),
}
_ENERGY_KCAL_COLUMN = "Energy, Regulation EU No 1169/2011 (kcal/100g)"
_NAME_COLUMN = "alim_nom_eng"
_CODE_COLUMN = "alim_code"


def _to_float(raw) -> float | None:
    if raw is None or raw == "" or raw == "-":
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    try:
        return float(str(raw).strip().replace(",", "."))
    except ValueError:
        return None  # "traces" or another non-numeric annotation


def main(xls_path: str) -> None:
    wb = xlrd.open_workbook(xls_path)
    ws = wb.sheet_by_name("compo")
    header = ws.row_values(0)
    col_index = {label: i for i, label in enumerate(header) if label in _COLUMN_MAP}
    name_i = header.index(_NAME_COLUMN)
    code_i = header.index(_CODE_COLUMN)
    energy_i = header.index(_ENERGY_KCAL_COLUMN)

    records = []
    for r in range(1, ws.nrows):
        row = ws.row_values(r)
        code = row[code_i]
        if not code:
            continue
        nutrients: dict[str, float] = {}
        cal = _to_float(row[energy_i])
        if cal is not None:
            nutrients["calories"] = cal
        for label, i in col_index.items():
            our_key, multiplier = _COLUMN_MAP[label]
            val = _to_float(row[i])
            if val is not None:
                nutrients[our_key] = val * multiplier
        records.append({"food_code": int(code), "name": row[name_i], "nutrients": nutrients})

    records.sort(key=lambda r: r["food_code"])
    OUTPUT.write_text(json.dumps(records, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(records)} foods to {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
