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
    monkeypatch.setattr(launcher, "_app_window_pref", lambda: False)
    monkeypatch.setattr(launcher, "_detect_running_browsers", lambda: ["chrome"])
    launched = []
    monkeypatch.setattr(launcher.subprocess, "Popen",
                        lambda cmd, **kw: launched.append(cmd))
    monkeypatch.setattr(launcher.webbrowser, "open",
                        lambda url: launched.append(["default", url]))
    launcher._pick_and_open_browser("http://127.0.0.1:8000")
    assert launched == [["/snap/bin/chromium", "http://127.0.0.1:8000"]]


def _capture_launch(monkeypatch, *, preferred: str, running: list[str],
                    on_path: dict[str, str]) -> list:
    monkeypatch.setattr(launcher, "_resolve_executable", on_path.get)
    monkeypatch.setattr(launcher, "_platform_browser_paths", lambda name: [])
    monkeypatch.setattr(launcher, "_preferred_browser_pref", lambda: preferred)
    monkeypatch.setattr(launcher, "_app_window_pref", lambda: True)
    monkeypatch.setattr(launcher, "_detect_running_browsers", lambda: running)
    monkeypatch.setattr(launcher, "_prompt_browser_choice", lambda r: None)
    monkeypatch.setattr(launcher, "_ensure_linux_window_entry", lambda window_id: None)
    launched = []
    monkeypatch.setattr(launcher.subprocess, "Popen",
                        lambda cmd, **kw: launched.append(cmd))
    monkeypatch.setattr(launcher.webbrowser, "open",
                        lambda url: launched.append(["default", url]))
    launcher._pick_and_open_browser("http://127.0.0.1:8000")
    return launched


def test_own_window_uses_installed_chromium_even_if_only_firefox_runs(monkeypatch) -> None:
    launched = _capture_launch(
        monkeypatch, preferred="", running=["firefox"],
        on_path={"chromium": "/snap/bin/chromium", "firefox": "/usr/bin/firefox"})
    assert launched == [["/snap/bin/chromium", "--app=http://127.0.0.1:8000/nutrimagnus-source"]]


def test_own_window_prefers_running_chromium_family_browser(monkeypatch) -> None:
    launched = _capture_launch(
        monkeypatch, preferred="", running=["firefox", "brave"],
        on_path={"chromium": "/usr/bin/chromium", "brave": "/snap/bin/brave",
                 "firefox": "/usr/bin/firefox"})
    assert launched == [["/snap/bin/brave", "--app=http://127.0.0.1:8000/nutrimagnus-source"]]


def test_own_window_with_firefox_chosen_opens_normal_tab(monkeypatch) -> None:
    launched = _capture_launch(
        monkeypatch, preferred="firefox", running=[],
        on_path={"chromium": "/usr/bin/chromium", "firefox": "/usr/bin/firefox"})
    assert launched == [["/usr/bin/firefox", "http://127.0.0.1:8000"]]


def test_own_window_with_no_chromium_family_falls_back_to_tab(monkeypatch) -> None:
    launched = _capture_launch(
        monkeypatch, preferred="", running=["firefox"],
        on_path={"firefox": "/usr/bin/firefox"})
    assert launched == [["/usr/bin/firefox", "http://127.0.0.1:8000"]]


def test_app_window_pref_defaults_on(monkeypatch) -> None:
    monkeypatch.setattr(launcher, "_read_prefs", lambda: {})
    assert launcher._app_window_pref() is True
    monkeypatch.setattr(launcher, "_read_prefs", lambda: {"app_window": False})
    assert launcher._app_window_pref() is False


def test_window_id_follows_browser_and_path() -> None:
    url = "http://127.0.0.1:8000/nutrimagnus"
    assert launcher._app_window_id("/snap/bin/chromium", url) == "chrome-127.0.0.1__nutrimagnus-Default"
    assert launcher._app_window_id("/usr/bin/brave-browser", url) == "brave-127.0.0.1__nutrimagnus-Default"
    assert launcher._app_window_id("/usr/bin/microsoft-edge", url) == "msedge-127.0.0.1__nutrimagnus-Default"


def test_linux_window_entry_written_unless_already_claimed(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(launcher.sys, "platform", "linux")
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    wid = "brave-127.0.0.1__nutrimagnus-source-Default"
    launcher._ensure_linux_window_entry(wid)
    entry = (tmp_path / "applications" / f"{wid}.desktop").read_text()
    assert f"StartupWMClass={wid}" in entry and "NoDisplay=true" in entry
    icon = tmp_path / "icons" / "nutrimagnus-window.png"
    assert f"Icon={icon}" in entry and icon.read_bytes()[:4] == b"\x89PNG"

    # A menu entry that already claims the window's name: no hidden one.
    wid2 = "chrome-127.0.0.1__nutrimagnus-source-Default"
    (tmp_path / "applications" / "numa.desktop").write_text(
        f"[Desktop Entry]\nName=NuMa\nStartupWMClass={wid2}\n")
    launcher._ensure_linux_window_entry(wid2)
    assert not (tmp_path / "applications" / f"{wid2}.desktop").exists()
