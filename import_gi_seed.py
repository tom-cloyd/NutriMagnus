"""
import_gi_seed.py — seed glycemic index (GI) estimates onto matching cached foods.

Source: Foster-Powell K, Holt SH, Brand-Miller JC. "International table of
glycemic index and glycemic load values: 2008." Diabetes Care 31(12):2281-3.
Table 1 (62 common foods), CC-licensed (cite, non-commercial, unaltered).
https://pmc.ncbi.nlm.nih.gov/articles/PMC2584181/

This is a small, high-confidence starter set covering common categories,
including plant proteins (legumes, soy). It is NOT the full ~2,480-item
appendix — that requires a manual browser download (PMC gates it behind a
bot-detection challenge) and isn't wired up here.

Usage:
    python import_gi_seed.py            # dry run: report matches only
    python import_gi_seed.py --apply    # write GI values for EXACT name matches

Matching is conservative on purpose: only an exact, case/punctuation-insensitive
name match against the food cache is written automatically. Anything else is
printed as a suggestion for you to confirm by hand via the Foods menu's
"Annotate food" action (or the web /food/annotate page) — food names in this
table are generic ("Lentils") while cache entries are specific USDA/OFF
records, so fuzzy auto-assignment risks attaching the wrong value.
"""
import re
import sys
import pathlib
import difflib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import db as _db

# name, GI (mean), source note suffix
_GI_SEED = [
    ("White wheat bread", 75, "bread"),
    ("Whole wheat bread", 74, "bread"),
    ("Specialty grain bread", 53, "bread"),
    ("Unleavened wheat bread", 70, "bread"),
    ("Wheat roti", 62, "bread"),
    ("Chapatti", 52, "bread"),
    ("Corn tortilla", 46, "bread"),
    ("Cornflakes", 81, "breakfast cereal"),
    ("Wheat flake biscuits", 69, "breakfast cereal"),
    ("Porridge, rolled oats", 55, "breakfast cereal"),
    ("Instant oat porridge", 79, "breakfast cereal"),
    ("Rice porridge/congee", 78, "breakfast cereal"),
    ("Millet porridge", 67, "breakfast cereal"),
    ("Muesli", 57, "breakfast cereal"),
    ("White rice, boiled", 73, "grain"),
    ("Brown rice, boiled", 68, "grain"),
    ("Barley", 28, "grain"),
    ("Spaghetti, white", 49, "pasta"),
    ("Spaghetti, whole meal", 48, "pasta"),
    ("Rice noodles", 53, "pasta"),
    ("Udon noodles", 55, "pasta"),
    ("Couscous", 65, "grain"),
    ("Apple, raw", 36, "fruit"),
    ("Orange, raw", 43, "fruit"),
    ("Banana, raw", 51, "fruit"),
    ("Pineapple, raw", 59, "fruit"),
    ("Mango, raw", 51, "fruit"),
    ("Watermelon, raw", 76, "fruit"),
    ("Dates, raw", 42, "fruit"),
    ("Peaches, canned", 43, "fruit"),
    ("Apple juice", 41, "beverage"),
    ("Orange juice", 50, "beverage"),
    ("Potato, boiled", 78, "vegetable"),
    ("Potato, instant mash", 87, "vegetable"),
    ("Potato, french fries", 63, "vegetable"),
    ("Carrots, boiled", 39, "vegetable"),
    ("Sweet potato, boiled", 63, "vegetable"),
    ("Pumpkin, boiled", 64, "vegetable"),
    ("Sweet corn", 52, "vegetable"),
    ("Plantain", 55, "vegetable"),
    ("Taro, boiled", 53, "vegetable"),
    ("Vegetable soup", 48, "vegetable"),
    ("Milk, full fat", 39, "dairy"),
    ("Milk, skim", 37, "dairy"),
    ("Ice cream", 51, "dairy"),
    ("Yogurt, fruit", 41, "dairy"),
    ("Soy milk", 34, "dairy alternative / plant protein"),
    ("Rice milk", 86, "dairy alternative"),
    ("Chickpeas", 28, "legume / plant protein"),
    ("Kidney beans", 24, "legume / plant protein"),
    ("Lentils", 32, "legume / plant protein"),
    ("Soya beans", 16, "legume / plant protein"),
    ("Chocolate", 40, "snack"),
    ("Popcorn", 65, "snack"),
    ("Potato crisps", 56, "snack"),
    ("Rice crackers", 87, "snack"),
    ("Soft drink/soda", 59, "beverage"),
    ("Strawberry jam/jelly", 49, "condiment"),
    ("Fructose", 15, "sugar"),
    ("Sucrose", 65, "sugar"),
    ("Glucose", 103, "sugar"),
    ("Honey", 61, "sugar"),
]

_SOURCE_NOTE = (
    "GI from Foster-Powell, Holt, Brand-Miller (2008), Diabetes Care 31(12):2281-3, "
    "Table 1 — international mean value for a generic food, not this specific product."
)


def _normalize(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", " ", name)
    return re.sub(r"\s+", " ", name).strip()


def main() -> None:
    apply = "--apply" in sys.argv

    with _db.get_db() as conn:
        cached = _db.list_cached_foods(conn)

    by_norm: dict[str, list] = {}
    for row in cached:
        by_norm.setdefault(_normalize(row["name"]), []).append(row)

    all_norms = list(by_norm.keys())

    exact_matches = []
    suggestions = []
    no_match = []

    for gi_name, gi_value, category in _GI_SEED:
        norm = _normalize(gi_name)
        rows = by_norm.get(norm)
        if rows and len(rows) == 1:
            exact_matches.append((gi_name, gi_value, category, rows[0]))
        elif rows:
            suggestions.append((gi_name, gi_value, category, rows))
        else:
            close = difflib.get_close_matches(norm, all_norms, n=3, cutoff=0.6)
            close_rows = [by_norm[c][0] for c in close]
            if close_rows:
                suggestions.append((gi_name, gi_value, category, close_rows))
            else:
                no_match.append((gi_name, gi_value, category))

    print(f"GI seed: {len(_GI_SEED)} entries from Foster-Powell/Holt/Brand-Miller 2008 Table 1\n")

    print(f"Exact name matches in cache: {len(exact_matches)}")
    for gi_name, gi_value, category, row in exact_matches:
        marker = "would set" if not apply else "set"
        print(f"  [{marker}] {row['name']} (FDC {row['fdc_id']})  GI={gi_value}  [{category}]")

    if suggestions:
        print(f"\nAmbiguous / fuzzy matches — review and annotate manually ({len(suggestions)}):")
        for gi_name, gi_value, category, rows in suggestions:
            names = ", ".join(f"{r['name']} (FDC {r['fdc_id']})" for r in rows[:5])
            print(f"  '{gi_name}' GI={gi_value}  ->  {names}")

    if no_match:
        print(f"\nNo cache match found ({len(no_match)}) — not in your pantry/cache yet:")
        for gi_name, gi_value, category in no_match:
            print(f"  '{gi_name}' GI={gi_value}  [{category}]")

    if not apply:
        print(f"\nDry run only. Re-run with --apply to write {len(exact_matches)} exact-match GI value(s).")
        return

    if not exact_matches:
        print("\nNothing to write.")
        return

    with _db.get_db() as conn:
        for gi_name, gi_value, category, row in exact_matches:
            _db.upsert_food_annotation(conn, row["fdc_id"], gi_estimate=float(gi_value))

    print(f"\nWrote GI values for {len(exact_matches)} food(s).")
    print(f"Note: {_SOURCE_NOTE}")


if __name__ == "__main__":
    main()
