"""
record_source_fixtures.py — record real API responses from the three live
data sources (USDA FoodData Central, Open Food Facts, Canadian Nutrient
File) as JSON fixture files under tests/fixtures/.

Why: unlike AFCD/CoFID/CIQUAL (bundled static datasets, no network), these
three are live APIs that can change their response shape without warning.
Fixtures recorded here get replayed by a test that checks the values still
look sane (no negative numbers, essential-AA total never exceeds protein,
etc.) — see TESTING-ROADMAP.md item #1 for the full plan, and
README-numa-documentation.md's Maintenance section for how often to re-run
this (quarterly).

Requires your real USDA API key already configured (Settings -> API key in
the web app, which writes it to ~/.config/numa/config.json — the same file
usda.get_api_key() reads) and a live network connection. Safe to re-run any
time: it always overwrites the existing fixture files with fresh ones, three
well-known foods per source.

Usage:
    python scripts/record_source_fixtures.py
"""
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

import cnf_api
import openfoodfacts
import usda as _usda

_FIXTURES_DIR = _PROJECT_ROOT / "tests" / "fixtures"

# Three well-known foods per source, chosen for having solid amino-acid/
# nutrient coverage so a real parsing gap is more likely to surface.
_USDA_QUERIES = ["chicken breast", "lentils", "salmon"]
_OFF_QUERIES = ["peanut butter", "greek yogurt", "oat milk"]
_CNF_QUERIES = ["egg", "lentils", "tofu"]


def _slug(text: str) -> str:
    return text.lower().replace(" ", "_")


def _write(out_dir: Path, query: str, search_result: dict, detail: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {"query": query, "search_result": search_result, "detail": detail}
    path = out_dir / f"{_slug(query)}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"  wrote {path.relative_to(_PROJECT_ROOT)}")


def _record_usda() -> None:
    out_dir = _FIXTURES_DIR / "usda"
    for query in _USDA_QUERIES:
        results = _usda.search_foods(query, page_size=5)
        if not results:
            print(f"  USDA: no results for {query!r}, skipping")
            continue
        top = results[0]
        detail = _usda.get_food_detail(top["fdcId"])
        _write(out_dir, query, top, detail)


def _record_off() -> None:
    out_dir = _FIXTURES_DIR / "off"
    for query in _OFF_QUERIES:
        results = openfoodfacts.search_foods(query, page_size=5)
        if not results:
            print(f"  OFF: no results for {query!r}, skipping")
            continue
        top = results[0]
        detail = openfoodfacts.get_food_detail(top)
        _write(out_dir, query, top, detail)


def _record_cnf() -> None:
    out_dir = _FIXTURES_DIR / "cnf"
    for query in _CNF_QUERIES:
        results = cnf_api.search_foods(query, page_size=5)
        if not results:
            print(f"  CNF: no results for {query!r}, skipping")
            continue
        top = results[0]
        detail = cnf_api.get_food_detail(top)
        _write(out_dir, query, top, detail)


def main() -> None:
    if not _usda.get_api_key():
        print(
            "WARNING: no USDA API key configured (Settings -> API key in the "
            "web app) -- USDA calls will fall back to the shared DEMO_KEY, "
            "which is rate-limited and may fail.",
            file=sys.stderr,
        )
    print("Recording USDA fixtures...")
    _record_usda()
    print("Recording Open Food Facts fixtures...")
    _record_off()
    print("Recording CNF fixtures...")
    _record_cnf()
    print("Done.")


if __name__ == "__main__":
    main()
