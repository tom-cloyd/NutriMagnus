"""Tests for web/launcher.py's startup loading page."""
import importlib.util
import pathlib
import socket
import urllib.request

_spec = importlib.util.spec_from_file_location(
    "numa_launcher", pathlib.Path(__file__).parent.parent / "web" / "launcher.py")
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)


def _get(port: int) -> str:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/meals", timeout=5) as resp:
        return resp.read().decode()


def test_loading_page_served_then_socket_handed_on() -> None:
    """The loading page answers at once on the real port; after stop() the
    same listening socket still accepts connections (for uvicorn)."""
    sock = launcher._bind_socket("127.0.0.1", 0)
    port = sock.getsockname()[1]
    loading = launcher._LoadingServer(sock)
    loading.start()
    try:
        page = _get(port)
        assert "Loading NutriMagnus" in page
        assert 'http-equiv="refresh"' in page
        loading.page = launcher._FAILED_PAGE
        assert "did not start" in _get(port)
    finally:
        loading.stop()
    client = socket.create_connection(("127.0.0.1", port), timeout=2)
    conn, _ = sock.accept()
    conn.close()
    client.close()
    sock.close()


def test_running_chromium_snap_opens_chromium_not_os_default(monkeypatch) -> None:
    """A running Chrome/Chromium shows to pgrep as "chrome", a name nothing on
    $PATH answers to; it must still launch the real browser instead of
    falling back to webbrowser.open (the OS default — Firefox, 2026-11-06)."""
    on_path = {"chromium": "/snap/bin/chromium", "firefox": "/usr/bin/firefox"}
    monkeypatch.setattr(launcher, "_resolve_executable", on_path.get)
    monkeypatch.setattr(launcher, "_preferred_browser_pref", lambda: "")
    monkeypatch.setattr(launcher, "_detect_running_browsers", lambda: ["chrome"])
    launched = []
    monkeypatch.setattr(launcher.subprocess, "Popen",
                        lambda cmd, **kw: launched.append(cmd))
    monkeypatch.setattr(launcher.webbrowser, "open",
                        lambda url: launched.append(["default", url]))
    launcher._pick_and_open_browser("http://127.0.0.1:8000")
    assert launched == [["/snap/bin/chromium", "http://127.0.0.1:8000"]]
