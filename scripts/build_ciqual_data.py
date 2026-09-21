#!/usr/bin/env python3
"""
build_ciqual_data.py — regenerate ciqual_data.json from the published French
CIQUAL food composition table (English-language XLS export). Last run
against Ciqual 2025 (upgraded from the original Ciqual 2020 ingest,
2026-09-20 — see README-numa-documentation.md's annual static-dataset check).

CIQUAL is a static download, not a live API — this script is the one-time
ingest step, run by a developer, not by numa at runtime (see
ciqual_lookup.py's module docstring for the static-vs-live source distinction).

Usage:
    pip install xlrd       # not a runtime dependency — only this script needs it
    python scripts/build_ciqual_data.py "path/to/Table Ciqual 2025_ENG_2025_11_03.xls"

Source spreadsheet: ANSES, "Ciqual French food composition table" (English-
language version), published at https://ciqual.anses.fr/ (download page) and
mirrored on recherche.data.gouv.fr. Not redistributed here — download it
yourself and pass the path in. Use the English-language export (English
column headers), not the French one — both carry the same data. ANSES's
download page also offers a separate, smaller "table of average foods and
their contributors" spreadsheet — don't use that one; it's a different table
(average/composite foods mapped to their contributing ingredients, not the
full food-composition table this script parses).

CIQUAL's file is the legacy .xls format (not .xlsx — ANSES also publishes an
.xlsx export if that's ever preferable), hence xlrd rather than openpyxl. No
amino-acid data — CIQUAL's public dataset has none (unlike Canadian Nutrient
File or AFCD). Cells use French locale formatting: a comma decimal separator
("9,15") and "-" for not-analyzed/missing, both handled below. Retinol and
beta-carotene are reported separately, with no combined RAE-style vitamin A
figure used here — retinol alone is used for vitamin_a_mcg (the same
approximation used for Canadian Nutrient File); Ciqual 2025 does add a
"Vitamin A activity, retinol equivalent" column, but its header carries what
looks like a units typo (µg/100mg, inconsistent with every other per-100g
column) — deliberately not used until that's confirmed with ANSES, rather
than risk silently mis-scaling every food's vitamin A by 1000x.

The 2025 export's header row wraps each column label across several
embedded newlines (e.g. "Protein\\n(g\\n100g)" instead of 2020's single-line
"Protein (g/100g)") and renamed the data sheet from "compo" to
"food composition" (plus a second "INFOODS codes" sheet that isn't used
here). Column matching is done against a whitespace-normalized form of each
header (newlines and slashes both collapsed to plain spaces) specifically so
this keeps working across that kind of harmless reformatting in a future
edition without needing another manual fixup — see _normalize_header().
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

# {normalized column label -> (our_key, multiplier)}. Multiplier converts
# CIQUAL's unit to ours — mostly 1.0; the fatty-acid columns are g/100g,
# ours want mg for the omega-3/6 keys. Keys are matched against each header
# cell after _normalize_header() (newlines/slashes collapsed to spaces), so
# they're written here in that same normalized form.
_COLUMN_MAP: dict[str, tuple[str, float]] = {
    "Protein (g 100g)":                                    ("protein_g",        1.0),
    "Fat (g 100g)":                                         ("fat_g",            1.0),
    "Carbohydrate (g 100g)":                                 ("carbs_g",          1.0),
    "Fibres (g 100g)":                                       ("fiber_g",          1.0),
    "Sugars (g 100g)":                                       ("sugar_g",          1.0),
    "FA saturated (g 100g)":                                 ("saturated_fat_g",  1.0),
    "FA mono (g 100g)":                                      ("mono_fat_g",       1.0),
    "FA poly (g 100g)":                                      ("poly_fat_g",       1.0),
    "FA 18:3 c9,c12,c15 (n-3) (g 100g)":                     ("omega3_ala_mg",    1000.0),
    "FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g 100g)":          ("omega3_epa_mg",    1000.0),
    "FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g 100g)":      ("omega3_dha_mg",    1000.0),
    "FA 18:2 9c,12c (n-6) (g 100g)":                         ("omega6_la_mg",     1000.0),
    "Calcium (mg 100g)":                                     ("calcium_mg",       1.0),
    "Iron (mg 100g)":                                        ("iron_mg",          1.0),
    "Iodine (µg 100g)":                                      ("iodine_mcg",       1.0),
    "Magnesium (mg 100g)":                                   ("magnesium_mg",     1.0),
    "Phosphorus (mg 100g)":                                  ("phosphorus_mg",    1.0),
    "Potassium (mg 100g)":                                   ("potassium_mg",     1.0),
    "Selenium (µg 100g)":                                    ("selenium_mcg",     1.0),
    "Sodium (mg 100g)":                                      ("sodium_mg",        1.0),
    "Zinc (mg 100g)":                                        ("zinc_mg",          1.0),
    # Retinol only — CIQUAL has no combined RAE-style vitamin A figure in
    # use here (see the module docstring re: the 2025 RAE column's units).
    "Retinol (µg 100g)":                                     ("vitamin_a_mcg",    1.0),
    "Beta-carotene (µg 100g)":                                ("beta_carotene_mcg", 1.0),
    "Vitamin C (mg 100g)":                                    ("vitamin_c_mg",     1.0),
    "Vitamin D (µg 100g)":                                    ("vitamin_d_mcg",    1.0),
    "Vitamin E (mg 100g)":                                    ("vitamin_e_mg",     1.0),
    "Vitamin K1 (µg 100g)":                                   ("vitamin_k_mcg",    1.0),  # K1 only, not K1+K2
    "Vitamin B1 or Thiamin (mg 100g)":                        ("thiamin_mg",       1.0),
    "Vitamin B2 or Riboflavin (mg 100g)":                     ("riboflavin_mg",    1.0),
    "Vitamin B3 or Niacin (mg 100g)":                         ("niacin_mg",        1.0),
    "Vitamin B6 (mg 100g)":                                   ("b6_mg",            1.0),
    # "total folates" (not the DFE-adjusted variant Ciqual 2025 also added)
    # is the direct successor of 2020's single plain "Folate" column.
    "Vitamin B9 or total folates (µg 100g)":                  ("folate_mcg",       1.0),
    "Vitamin B12 (µg 100g)":                                  ("b12_mcg",          1.0),
}
_ENERGY_KCAL_COLUMN = "Energy, Regulation EU No 1169 2011 (kcal 100g)"
_NAME_COLUMN = "alim_nom_eng"
_CODE_COLUMN = "alim_code"
_SHEET_NAMES = ("food composition", "compo")  # 2025, then 2020 fallback


def _normalize_header(label) -> str:
    return " ".join(str(label).replace("/", " ").split())


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
    sheet_name = next((n for n in _SHEET_NAMES if n in wb.sheet_names()), None)
    if sheet_name is None:
        raise SystemExit(
            f"None of the expected sheet names {_SHEET_NAMES!r} found; "
            f"workbook has: {wb.sheet_names()!r}"
        )
    ws = wb.sheet_by_name(sheet_name)
    header = [_normalize_header(h) for h in ws.row_values(0)]
    col_index = {label: i for i, label in enumerate(header) if label in _COLUMN_MAP}
    missing = set(_COLUMN_MAP) - set(col_index)
    if missing:
        print(f"Warning: {len(missing)} expected column(s) not found in this "
              f"file's header row (skipped): {sorted(missing)}")
    name_i = header.index(_normalize_header(_NAME_COLUMN))
    code_i = header.index(_normalize_header(_CODE_COLUMN))
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
