#!/usr/bin/env python3
"""
build_gi_data.py — regenerate gi_data.json from the Foster-Powell/Holt/
Brand-Miller online-only appendix PDFs (see user-manual.md footnote 8).

The appendix ships as two PDFs, one per subject population:
  Table A1 — GI/GL values measured in subjects with normal glucose tolerance
  Table A2 — GI/GL values measured in subjects with impaired glucose
             tolerance, small subject numbers, or wide value variability

Both are a static download (PMC gates the page behind bot detection, so a
developer has to fetch them manually — see user-manual.md footnote 8) rather
than a live API, same category as CoFID/AFCD/CIQUAL. This script is the
one-time ingest step; gi_lookup.py reads its output at runtime.

Usage:
    python scripts/build_gi_data.py path/to/dc08-1239_1.pdf path/to/dc08-1239_2.pdf

Extraction approach: `pdftotext -layout` preserves the table's column
alignment as fixed-width text, but the exact column offsets drift slightly
page to page (pdftotext re-flows spacing per page), so column boundaries are
recomputed from each page's own repeated header line rather than assumed
constant across the whole document. Only the food name, the GI value on the
glucose-referenced scale (GI Glucose=100 — the scale the rest of numa uses;
NOT the GI Bread=100 column also printed), population, and the source
reference number are kept. Serve size / available carbohydrate / GL are
deliberately NOT captured: numa already computes GL live from a food's own
cached carbohydrate content and the amount consumed
(numa_app.services.glycemic_load.compute_glycemic_load), which is more
accurate for a specific cached food than rescaling the study's own tested
product's serving-specific GL would be.

A stray wrapped line of a food's name (continuing onto a second physical
line) is distinguished from a section header (e.g. "Cakes", "BAKERY
PRODUCTS") heuristically: short, no digits/commas/parens => header. This is
inherently imperfect — some section/category labels come through wrong for
a handful of entries — but it only affects the informational category tag,
never the food name or GI value.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "gi_data.json"

_FOOTER_RE = re.compile(r'^Atkinson FS|^Care 2008|^glucose tolerance: 2008$|^Table A\d\.')
_PAGENUM_RE = re.compile(r'^\s*\d+\s*$')
_SUBHEADER_RES = [
    re.compile(r'^\s*\(Glucose'),
    re.compile(r'^\s*= 100\)'),
    re.compile(r'^\s*g\s+g/serve\s*$'),
]
_FOOTNOTES_START_RE = re.compile(r'^Footnotes for Table')
_BARE_SERVING_RE = re.compile(r'^\d+\s?(g|mL|ml|portion)\b', re.I)


def _page_bounds(header_line: str) -> dict[str, int]:
    gi1 = header_line.find("GI2")
    gi2 = header_line.find("GI2", gi1 + 1)
    return {
        "name_end": gi1,
        "gi_glucose_end": gi2,
        "refperiod_end": header_line.find("Reference food"),
        "ref_end": header_line.find("Serve"),
    }


def _looks_like_header(stripped: str) -> bool:
    if not stripped or len(stripped) > 45:
        return False
    if re.search(r'[(),0-9]', stripped):
        return False
    return len(stripped.split()) <= 6


def _parse_pdf(path: Path, population: str) -> list[dict]:
    text = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    lines = [l.rstrip("\n") for l in text.splitlines()]

    items: list[dict] = []
    current: dict | None = None
    category: str | None = None
    bounds: dict[str, int] | None = None
    stopped = False

    for line in lines:
        if stopped or not line.strip():
            continue
        if line.startswith("Food Number and Item"):
            bounds = _page_bounds(line)
            current = None
            continue
        if _FOOTNOTES_START_RE.search(line):
            stopped = True
            current = None
            continue
        if _FOOTER_RE.search(line) or _PAGENUM_RE.match(line) \
           or any(r.match(line) for r in _SUBHEADER_RES):
            continue
        if bounds is None:
            continue

        num_field = line[:bounds["name_end"]]
        m = re.match(r'^\s*(\d+)\s', num_field)
        is_new_row = m and len(num_field.strip().split()[0]) == len(m.group(1))

        if is_new_row:
            name = num_field[m.end(1):].strip()
            if name.lower().startswith("mean of"):
                current = None
                continue
            gi_field = line[bounds["name_end"]:bounds["gi_glucose_end"]]
            gm = re.search(r'([\d.]+)', gi_field)
            gi_glucose = float(gm.group(1)) if gm else None
            ref = line[bounds["refperiod_end"]:bounds["ref_end"]].strip()
            item = {
                "name": name,
                "gi_glucose": gi_glucose,
                "category": category,
                "ref": ref,
                "population": population,
            }
            items.append(item)
            current = item
        else:
            stripped = line.strip()
            if not stripped or stripped.lower().startswith("mean of"):
                current = None
                continue
            if _looks_like_header(stripped):
                category = stripped
                current = None
            elif current is not None:
                current["name"] += " " + stripped
            else:
                category = stripped

    clean = [it for it in items if it["gi_glucose"] is not None and len(it["name"]) >= 3]
    for it in clean:
        if it["category"] and _BARE_SERVING_RE.match(it["name"]):
            it["name"] = f'{it["category"]}, {it["name"]}'
    return clean


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    normal = _parse_pdf(Path(sys.argv[1]), "normal")
    impaired = _parse_pdf(Path(sys.argv[2]), "impaired")

    OUTPUT.write_text(
        json.dumps({"normal": normal, "impaired": impaired}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}: {len(normal)} normal-tolerance + {len(impaired)} "
          f"impaired-tolerance entries")


if __name__ == "__main__":
    main()
