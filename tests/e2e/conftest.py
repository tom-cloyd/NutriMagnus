"""
tests/e2e/conftest.py — fixtures for Playwright browser-level E2E tests.

These run against a REAL server in a separate subprocess, not FastAPI's
TestClient (which is in-process and can't drive real browser JS). Test
isolation therefore can't use tests/conftest.py's monkeypatch-based
approach (it never reaches a separate process) — instead the `live_server`
fixture points the subprocess at temp data/config dirs via the NUMA_DATA_DIR
/ NUMA_CONFIG_DIR env-var override added to platform_utils.py, and external
API calls are stubbed out in _run_isolated_server.py so a search never needs
network access or a real API key.

Docs: TESTING-ROADMAP.md, item #4.
"""
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_RUNNER = Path(__file__).parent / "_run_isolated_server.py"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_until_up(url: str, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"live_server did not come up at {url} within {timeout}s")


@pytest.fixture(scope="session")
def live_server(tmp_path_factory):
    """Session-scoped: one isolated server subprocess for the whole E2E run.

    A seeded-once fresh install (numa's demo data auto-seeds on first
    startup — see demo_data.seed_if_fresh_install()) gives every test a
    known, stable set of local foods (e.g. "Chickpeas") to search for.
    """
    data_dir = tmp_path_factory.mktemp("numa_e2e_data")
    config_dir = tmp_path_factory.mktemp("numa_e2e_config")
    host, port = "127.0.0.1", _free_port()
    base_url = f"http://{host}:{port}"

    env = {
        **os.environ,
        "NUMA_DATA_DIR": str(data_dir),
        "NUMA_CONFIG_DIR": str(config_dir),
    }
    proc = subprocess.Popen(
        [sys.executable, str(_RUNNER), host, str(port)],
        cwd=str(_PROJECT_ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_until_up(base_url + "/")
        yield base_url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        yield b
        b.close()


@pytest.fixture
def page(browser):
    pg = browser.new_page()
    yield pg
    pg.close()
