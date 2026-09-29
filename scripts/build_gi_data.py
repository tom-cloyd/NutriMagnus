#!/usr/bin/env python3
"""
build_gi_data.py — developer command-line wrapper around
numa_app/services/gi_table_build.py, which holds the actual parser (and its
documentation). Users do this from Settings -> Glycemic Index Reference Table
instead: upload the two PDFs, click Build.

Writes gi_data_local.json beside gi_lookup.py (the repo root) by default, or to
--output. That file is gitignored and never bundled: the 2021 tables' licence
forbids redistribution. Do not commit it or ship it.

Usage:
    python scripts/build_gi_data.py supp_table_1.pdf supp_table_2.pdf [--output PATH]

The two PDFs may be given in either order.
"""
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from numa_app.services import gi_table_build as _build  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pdfs", nargs=2, type=Path)
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "gi_data_local.json")
    args = parser.parse_args()
    try:
        r = _build.build_table(args.pdfs, args.output)
    except _build.BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {r['output']}")
    print("  This file is yours alone: gitignored, never bundled, do not "
          "redistribute it.")
    print(f"  2021 Supplemental Table 1 (ISO-consistent):    {r['table1']} entries")
    print(f"  2021 Supplemental Table 2 (method deviations): {r['table2']} entries")
    print(f"  2008 rows carried forward as legacy tier:      {r['legacy']}")
    for pool, n in r["pools"].items():
        print(f"  {pool}: {n} entries ({r['dated'][pool]} with a year of test)")
    for w in r["skipped"]:
        print(f"  SKIPPED {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
