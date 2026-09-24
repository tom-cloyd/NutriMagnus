#!/usr/bin/env python3
"""complement_worksheet.py — print every intermediate number behind numa's
complement suggestions for one base food, so the result can be checked by hand.

Read-only: never writes to the database.

Usage:
    python3 complement_worksheet.py "lentils"            # base at digestibility 1.0
    python3 complement_worksheet.py "lentils" 0.75       # base at a given digestibility
    python3 complement_worksheet.py --curated "Oats"     # use the curated-table entry
"""
import json
import sys

sys.path.insert(0, ".")
import db as _db
import usda as _usda
from usda_api import AA_REFERENCE_MG_PER_G_PROTEIN as REF
from usda_nutrients import _AA_PAIRS, _COMPLEMENT_TABLE, _MIN_GAP_SCORE


def short(aa):
    return aa.replace("aa_", "").replace("_g", "")


def paired(n, aa):
    v = n.get(aa, 0.0)
    if aa in _AA_PAIRS:
        v += n.get(_AA_PAIRS[aa], 0.0)
    return v


def find_base(term, curated):
    if curated:
        for c in _COMPLEMENT_TABLE:
            if term.lower() in c["name"].lower():
                return c["name"], c["nutrients"]
        sys.exit(f"no curated entry matching {term!r}")
    with _db.get_db() as conn:
        rows = _db.search_cached_foods(conn, term)
    if not rows:
        sys.exit(f"nothing in the food cache matching {term!r}")
    r = rows[0]
    return r["name"], json.loads(r["nutrients_json"] or "{}")


def main():
    args = [a for a in sys.argv[1:] if a != "--curated"]
    curated = "--curated" in sys.argv
    if not args:
        sys.exit(__doc__)
    term = args[0]
    name, n = find_base(term, curated)
    if len(args) > 1:
        dig = float(args[1])
    else:
        import diaas as _diaas
        dig, dig_src = _diaas.get_digestibility(name)
        print(f"(digestibility looked up the same way the app does: {dig} — {dig_src})")
    P = n.get("protein_g", 0.0)
    print(f"BASE: {name}   (per 100 g)")
    print(f"  protein P = {P} g      digestibility d = {dig}")
    print()

    print("STEP 1 — score each essential amino acid")
    print(f"  score = (AA_g / P) * 1000 / ref * d          gap threshold = {_MIN_GAP_SCORE}")
    print(f"  {'amino acid':<16}{'AA g':>9}{'mg/g prot':>11}{'ref':>7}{'score':>9}   gap?")
    gaps = []
    for aa in REF:
        v = paired(n, aa)
        mg = (v / P) * 1000 if P else 0.0
        sc = mg / REF[aa] * dig
        flag = "<-- GAP" if sc < _MIN_GAP_SCORE else ""
        pair = "+cys" if aa == "aa_methionine_g" else ("+tyr" if aa == "aa_phenylalanine_g" else "")
        print(f"  {short(aa)+pair:<16}{v:>9.4f}{mg:>11.2f}{REF[aa]:>7}{sc:>9.4f}   {flag}")
        if sc < _MIN_GAP_SCORE:
            gaps.append((aa, sc))
    print()
    if not gaps:
        print("No gaps -> no complement suggestions at all.")
        return
    gaps.sort(key=lambda t: t[1])
    print(f"  gaps, worst first: {[(short(a), round(s, 4)) for a, s in gaps]}")
    primary = gaps[0][0]
    print(f"  PRIMARY (limiting) amino acid: {short(primary)}")
    print()

    A = paired(n, primary)
    R = REF[primary] / 1000.0 / max(dig, 0.01)
    print(f"STEP 2 — the target for {short(primary)}")
    print(f"  R    = ref/1000/d = {REF[primary]}/1000/{dig} = {R:.6f} g of AA per g of protein")
    print(f"  A    = base {short(primary)} = {A:.4f} g")
    print(f"  R*P  = {R:.6f} * {P} = {R * P:.5f} g needed")
    print(f"  short by {R * P - A:.5f} g")
    print()

    print("STEP 3 — grams X of each candidate:  X = (R*P - A) / (a - R*q)")
    print(f"  {'candidate':<24}{'a':>10}{'q':>10}{'R*q':>10}{'a-R*q':>10}{'X g':>9}   verdict")
    for c in _COMPLEMENT_TABLE:
        cn = c["nutrients"]
        a = paired(cn, primary) / 100.0
        q = cn.get("protein_g", 0.0) / 100.0
        den = a - R * q
        if den <= 0:
            print(f"  {c['name']:<24}{a:>10.6f}{q:>10.6f}{R * q:>10.6f}{den:>10.6f}{'-':>9}   ratio too low")
            continue
        X = (R * P - A) / den
        verdict = "ok" if 0 < X <= 300 else "over 300 g - rejected"
        print(f"  {c['name']:<24}{a:>10.6f}{q:>10.6f}{R * q:>10.6f}{den:>10.6f}{X:>9.2f}   {verdict}")
    print()

    print("STEP 4 — what the program actually returns (compare with step 3)")
    res = _usda.suggest_complements(n, [], diet_pref="all", base_digestibility=dig,
                                    base_food_name=name)
    for s in res["general"]:
        print(f"  {s['name']:<24}{s['grams']:>5} g   closes_primary={str(s['closes_primary']):<5}"
              f" gaps_closed={s['gaps_closed']} remaining={s['remaining_gaps']}")
    if res["diaas_improvers"]:
        print("  -- DIAAS improvers (could not close any gap) --")
        for s in res["diaas_improvers"]:
            print(f"  {s['name']:<24}{s['grams']:>5} g   DIAAS {s['current_diaas']} -> {s['new_diaas']}")


main()
