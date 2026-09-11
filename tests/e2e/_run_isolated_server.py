"""
_run_isolated_server.py — launches numa's FastAPI app for Playwright E2E
tests, isolated from live external APIs and from the real DB/config dirs.

Not a general-purpose launcher (see web/launcher.py for that) — this is
test-only plumbing, invoked as a subprocess by tests/e2e/conftest.py's
`live_server` fixture:
  - NUMA_DATA_DIR / NUMA_CONFIG_DIR (set by the fixture) redirect db.py's
    and profile.py's paths via platform_utils.py's env-var override — see
    that module for how.
  - usda.search_foods / openfoodfacts.search_foods / cnf_api.search_foods
    are stubbed to return [] before backend.py's module-level
    `_LIVE_SOURCES` list is built, so a search never makes a real network
    call or needs a real API key. web/backend.py's `_fetch_*_candidates`
    functions look these up as module attributes at call time (not a
    captured reference), so patching the attribute here is enough even
    though backend.py does its own `import usda as _usda` etc.

Usage: python _run_isolated_server.py <host> <port>
"""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

import cnf_api
import openfoodfacts
import usda


def _stub_search(*_args, **_kwargs):
    return []


usda.search_foods = _stub_search
openfoodfacts.search_foods = _stub_search
cnf_api.search_foods = _stub_search

import uvicorn

if __name__ == "__main__":
    host, port = sys.argv[1], int(sys.argv[2])
    uvicorn.run("backend:app", host=host, port=port, app_dir=str(_PROJECT_ROOT / "web"))
