#!/usr/bin/env python3
"""
smoke_test_upgrade.py — before a release, check that the freshly built binary
starts cleanly on databases made by EARLIER code, i.e. that its startup
migrations upgrade an existing user's numa.db without crashing or losing rows.

The release checklist's fresh-install smoke test never exercises this: a fresh
install has no old schema to migrate. Scenarios run, each in its own throwaway
HOME / data / config dirs (nothing real is ever opened for writing):

  fresh-install     no database at all: the binary creates one and loads the
                    starter data, as for a new user. Also fails if the Home
                    page then shows the DATA CHECK banner — starter data must
                    never greet a new user with "data problems".
  previous-release  a numa.db created and starter-seeded by the source of the
                    newest v* git tag (the release users are on now)
  --db PATH ...     a COPY of each given database (default: your live
                    ~/.local/share/numa/numa.db). Old backups such as
                    numa.db.before-* make good extra cases — real data at an
                    older schema.

For each: row counts of the main tables before, start dist/nutrimagnus on it,
wait for the real app (not the launcher's loading page), GET a set of pages
plus one food/recipe/meal detail page, then compare row counts after. Any
non-200 page, "Traceback"/"Internal Server Error" text, startup failure, or
lost rows fails the run.

Run from the repo root, after `make build` (or pass --build):
    .venv/bin/python3 scripts/smoke_test_upgrade.py
    .venv/bin/python3 scripts/smoke_test_upgrade.py --build --db ~/.local/share/numa/numa.db.before-origins-20260929-210237
Docs: README-numa-documentation.md, Maintenance: "Database-upgrade smoke test before a release"
"""
import argparse
import os
import pathlib
import socket
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BINARY = REPO_ROOT / "dist" / "nutrimagnus"
LIVE_DB = pathlib.Path.home() / ".local" / "share" / "numa" / "numa.db"
TABLES = ("foods", "recipes", "recipe_ingredients", "meals", "meal_items", "pantry")
PAGES = (
    "/", "/meals", "/recipes", "/pantry", "/food/cache", "/food/cache/db-check",
    "/summary/trend", "/analysis/food-use", "/analysis/food-use-recipes",
    "/compare", "/settings",
)
BAD_TEXT = ("Traceback", "Internal Server Error", "NutriMagnus did not start")
STARTUP_TIMEOUT = 90


def _copy_db(src: pathlib.Path, dst: pathlib.Path) -> None:
    """Consistent copy via SQLite's backup API — safe even if the app is
    running on src; src is opened read-only (this is a test script, not app
    code, so it doesn't go through db.get_db())."""
    with sqlite3.connect(f"file:{src}?mode=ro", uri=True) as s, sqlite3.connect(dst) as d:
        s.backup(d)


def _row_counts(db: pathlib.Path) -> dict[str, int]:
    if not db.exists():
        return {}
    with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as conn:
        present = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        return {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in TABLES if t in present}


def _first_ids(db: pathlib.Path) -> list[str]:
    """One food, recipe and meal detail page to fetch, if the DB has any."""
    paths = []
    if not db.exists():
        return paths
    with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as conn:
        for sql, fmt in (
            ("SELECT fdc_id FROM foods ORDER BY fdc_id DESC LIMIT 1", "/food/{}"),
            ("SELECT id FROM recipes ORDER BY id LIMIT 1", "/recipe/{}"),
            ("SELECT id FROM meals ORDER BY id DESC LIMIT 1", "/meal/{}"),
        ):
            try:
                row = conn.execute(sql).fetchone()
            except sqlite3.Error:
                row = None
            if row:
                paths.append(fmt.format(row[0]))
    return paths


def _isolated_env(root: pathlib.Path) -> dict[str, str]:
    env = dict(os.environ)
    env.update(
        HOME=str(root / "home"),
        NUMA_DATA_DIR=str(root / "data"),
        NUMA_CONFIG_DIR=str(root / "config"),
    )
    for key in ("home", "data", "config"):
        (root / key).mkdir(parents=True, exist_ok=True)
    return env


def _make_previous_release_db(root: pathlib.Path) -> tuple[pathlib.Path, str]:
    """Create + starter-seed a numa.db with the newest v* tag's own source."""
    tag = subprocess.run(
        ["git", "tag", "--sort=-creatordate", "--list", "v*"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()[0]
    src = root / "src"
    src.mkdir(parents=True)
    archive = root / "src.tar"
    subprocess.run(["git", "archive", "-o", str(archive), tag], cwd=REPO_ROOT, check=True)
    with tarfile.open(archive) as tf:
        tf.extractall(src, filter="data")
    code = (
        "import db; db.init_db()\n"
        "from numa_app.services import demo_data\n"
        "with db.get_db() as conn: print(demo_data.seed_if_fresh_install(conn))\n"
    )
    subprocess.run([sys.executable, "-c", code], cwd=src, env=_isolated_env(root), check=True,
                   capture_output=True, text=True)
    return root / "data" / "numa.db", tag


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _get(url: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def run_scenario(name: str, root: pathlib.Path, db: pathlib.Path, *, fresh: bool = False) -> list[str]:
    """Start the binary on root's data dir (db already in place, unless
    fresh); return failures."""
    failures: list[str] = []
    before = _row_counts(db)
    detail_pages = _first_ids(db)
    port = _free_port()
    base = f"http://127.0.0.1:{port}"
    log = open(root / "server.log", "w")
    proc = subprocess.Popen([str(BINARY), "--no-browser", "--port", str(port)],
                            env=_isolated_env(root), stdout=log, stderr=subprocess.STDOUT)
    try:
        deadline = time.time() + STARTUP_TIMEOUT
        ready = False
        while time.time() < deadline and proc.poll() is None:
            try:
                status, body = _get(base + "/settings")
                if "did not start" in body:
                    break
                if status == 200 and "Loading NutriMagnus" not in body:
                    ready = True
                    break
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                pass
            time.sleep(1)
        if not ready:
            failures.append(f"app never became ready (see {root / 'server.log'})")
            return failures
        for path in PAGES + tuple(detail_pages):
            status, body = _get(base + path)
            bad = next((t for t in BAD_TEXT if t in body), None)
            if status != 200 or bad:
                failures.append(f"GET {path} -> {status}" + (f" ({bad!r} in page)" if bad else ""))
            if fresh and path == "/" and "DATA CHECK:" in body:
                failures.append("Home page shows the DATA CHECK banner on a fresh install — "
                                "the starter data has problems (see Foods → 9 in a fresh install)")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        log.close()
    after = _row_counts(db)
    if fresh and not after.get("foods"):
        failures.append("fresh install: no starter foods were loaded")
    for table, n in before.items():
        if after.get(table, 0) < n:
            failures.append(f"{table}: {n} rows before, {after.get(table, 0)} after")
    log_text = (root / "server.log").read_text(errors="replace")
    if "Traceback" in log_text:
        failures.append(f"Traceback in server log ({root / 'server.log'})")
    print(f"  rows before: {before}")
    print(f"  rows after:  {after}")
    print(f"  pages: {len(PAGES) + len(detail_pages)} fetched")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--build", action="store_true", help="run `make build` first")
    parser.add_argument("--db", action="append", type=pathlib.Path,
                        help=f"database to test a copy of (repeatable; default {LIVE_DB})")
    parser.add_argument("--keep", action="store_true", help="keep the temp dirs for inspection")
    args = parser.parse_args()

    if args.build:
        subprocess.run(["make", "build"], cwd=REPO_ROOT, check=True)
    if not BINARY.exists():
        print(f"ERROR: {BINARY} not found — run `make build` or pass --build.")
        return 2

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="numa-upgrade-smoke-"))
    any_failed = False
    scenarios: list[tuple[str, pathlib.Path, pathlib.Path]] = []

    fresh_root = tmp / "fresh-install"
    _isolated_env(fresh_root)
    scenarios.append(("fresh-install", fresh_root, fresh_root / "data" / "numa.db"))

    prev_root = tmp / "previous-release"
    prev_db, tag = _make_previous_release_db(prev_root)
    scenarios.append((f"previous-release ({tag})", prev_root, prev_db))

    for i, src in enumerate(args.db or [LIVE_DB]):
        src = src.expanduser()
        if not src.exists():
            print(f"SKIP: {src} does not exist")
            continue
        root = tmp / f"copy-{i}"
        _isolated_env(root)
        dst = root / "data" / "numa.db"
        _copy_db(src, dst)
        scenarios.append((f"copy of {src}", root, dst))

    for name, root, db in scenarios:
        print(f"== {name}")
        failures = run_scenario(name, root, db, fresh=(name == "fresh-install"))
        if failures:
            any_failed = True
            for f in failures:
                print(f"  FAIL: {f}")
        else:
            print("  OK")

    if args.keep or any_failed:
        print(f"\nTemp dirs kept at {tmp}")
    else:
        import shutil
        shutil.rmtree(tmp)
    print("\nRESULT:", "FAILED" if any_failed else "all scenarios passed")
    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())
