#!/usr/bin/env python3
"""
numa.py — CLI entry point for the numa nutritional analysis program.

Parses --api-key / --theme command-line flags, then delegates to numa_app.main.run_app().
Docs: README-numa-documentation.md, Project Structure
"""

import argparse
import json
import pathlib
import sys

from numa_app.main import run_app
from version import VERSION  # noqa: F401  — single source of truth for app version


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="numa — nutritional analysis")
    parser.add_argument(
        "--theme",
        choices=["dark", "light", "neutral", "auto"],
        help="Set color theme: dark, light, neutral, auto",
    )
    parser.add_argument(
        "--api-key",
        help="Set USDA FoodData Central API key and exit",
    )
    parser.add_argument(
        "--export-json",
        metavar="FDC_ID",
        nargs="+",
        type=int,
        help="Export cached food data as JSON (one or more FDC IDs)",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write --export-json output to FILE instead of stdout",
    )
    return parser.parse_args()


def _maybe_rebuild_manual() -> None:
    """Silently regenerate user-manual.html if the markdown source is newer."""
    root = pathlib.Path(__file__).parent
    md   = root / "user-manual.md"
    html = root / "user-manual.html"
    if not md.exists():
        return
    if html.exists() and html.stat().st_mtime >= md.stat().st_mtime:
        return
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "build_manual", root / "scripts" / "build_manual.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
    except Exception:
        pass  # never block startup over a docs rebuild


def _run_export_json(fdc_ids: list[int], output: str | None) -> None:
    import db as _db

    results = []
    missing = []
    with _db.get_db() as conn:
        for fdc_id in fdc_ids:
            row = _db.get_cached_food(conn, fdc_id)
            if row is None:
                missing.append(fdc_id)
                continue
            results.append({
                "fdc_id":        row["fdc_id"],
                "name":          row["name"],
                "data_type":     row["data_type"],
                "brand":         row["brand"],
                "serving_size":  row["serving_size"],
                "serving_unit":  row["serving_unit"],
                "nutrients_per_100g": (
                    json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
                ),
            })

    if missing:
        print(f"Warning: FDC IDs not found in cache: {missing}", file=sys.stderr)

    payload = json.dumps(results, indent=2)
    if output:
        path = pathlib.Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
        print(f"Wrote {len(results)} food(s) to {path}", file=sys.stderr)
    else:
        print(payload)


if __name__ == "__main__":
    args = parse_args()
    if args.export_json:
        _run_export_json(args.export_json, args.output)
        sys.exit(0)
    _maybe_rebuild_manual()
    run_app(theme=args.theme, api_key=args.api_key)
    