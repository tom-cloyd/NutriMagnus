"""
launcher.py — Start the numa web app and open it in its own browser window
(Chromium-family app mode) or, failing that, a browser tab.

Usage:
    python web/launcher.py           # default port 8000
    python web/launcher.py --port 8080
    python web/launcher.py --no-browser
"""
import sys
from pathlib import Path

_FROZEN = getattr(sys, "frozen", False)

# Inject the project venv's site-packages if we're not already running inside it.
# Checking sys.prefix (not sys.executable) handles venvs that symlink the system Python.
# Site-packages location differs by platform: Lib/site-packages on Windows, lib/pythonX.Y/site-packages on Linux/Mac.
# None of this applies to a frozen build — everything is already bundled, no venv involved.
if _FROZEN:
    _PROJECT_ROOT = Path(sys._MEIPASS)
else:
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent
    _VENV = _PROJECT_ROOT / ".venv"
    if _VENV.exists() and not Path(sys.prefix).resolve().samefile(_VENV.resolve()):
        _py = f"python{sys.version_info.major}.{sys.version_info.minor}"
        _site = _VENV / ("Lib/site-packages" if sys.platform == "win32" else f"lib/{_py}/site-packages")
        if _site.exists() and str(_site) not in sys.path:
            sys.path.insert(0, str(_site))

import argparse
import json
import os
import shutil
import socket
import subprocess
import threading
import time
import webbrowser

# Ordered by rough popularity — used only as the fallback order when a
# dialog tool isn't available to ask the user directly (see _open_after).
_BROWSER_PROCESSES = (
    "firefox", "google-chrome", "chrome", "chromium", "chromium-browser",
    "brave", "brave-browser", "vivaldi", "opera", "microsoft-edge", "epiphany",
)

_BROWSER_DISPLAY_NAMES = {
    "firefox": "Firefox", "google-chrome": "Google Chrome", "chrome": "Chrome",
    "chromium": "Chromium", "chromium-browser": "Chromium",
    "brave": "Brave", "brave-browser": "Brave", "vivaldi": "Vivaldi",
    "opera": "Opera", "microsoft-edge": "Microsoft Edge", "epiphany": "GNOME Web",
}

# A browser name that may not itself be a launchable program — tried in
# order, first one that resolves wins. Distros install Chromium under more
# than one binary name, so the single "Chromium" Settings choice works
# whichever exists. And a running Chrome *or* Chromium shows up to pgrep as
# "chrome" (the internal binary name, e.g. the Chromium snap's
# /snap/chromium/.../chrome), but nothing called "chrome" is on $PATH —
# without these alternates the launch failed and quietly fell back to the
# OS default browser (seen 2026-11-06: Chromium running, Firefox opened).
_BROWSER_ALTERNATES = {
    "chromium": ("chromium", "chromium-browser"),
    "chromium-browser": ("chromium-browser", "chromium"),
    "google-chrome": ("google-chrome", "google-chrome-stable"),
    "chrome": ("chrome", "google-chrome", "google-chrome-stable",
               "chromium", "chromium-browser"),
    "brave": ("brave", "brave-browser"),
    "brave-browser": ("brave-browser", "brave"),
    "microsoft-edge": ("microsoft-edge", "microsoft-edge-stable"),
}

# Chromium-family browsers can open a page as its own app window
# (--app=URL): no tabs, no address bar, its own taskbar entry. Firefox
# dropped its equivalent, so with the "own window" setting on, the launcher
# reaches for one of these, and falls back to a normal tab if none is
# installed. _APP_WINDOW_ORDER is the order tried when no browser is chosen
# in Settings and none of these is already running.
_APP_WINDOW_BROWSERS = frozenset({
    "google-chrome", "chrome", "chromium", "chromium-browser",
    "brave", "brave-browser", "vivaldi", "microsoft-edge",
})
_APP_WINDOW_ORDER = ("chromium", "google-chrome", "brave", "microsoft-edge", "vivaldi")

# Where these browsers live on Windows and macOS, which rarely put them on
# $PATH. Tried only after the $PATH lookup fails.
def _platform_browser_paths(name: str) -> list[str]:
    if sys.platform == "win32":
        pf = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        pf86 = os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")
        local = os.environ.get("LOCALAPPDATA", "")
        rel = {
            "google-chrome": [r"Google\Chrome\Application\chrome.exe"],
            "chrome": [r"Google\Chrome\Application\chrome.exe"],
            "chromium": [r"Chromium\Application\chrome.exe"],
            "brave": [r"BraveSoftware\Brave-Browser\Application\brave.exe"],
            "brave-browser": [r"BraveSoftware\Brave-Browser\Application\brave.exe"],
            "microsoft-edge": [r"Microsoft\Edge\Application\msedge.exe"],
            "vivaldi": [r"Vivaldi\Application\vivaldi.exe"],
        }.get(name, [])
        return [str(Path(base) / r) for r in rel for base in (pf, pf86, local) if base]
    if sys.platform == "darwin":
        app = {
            "google-chrome": "Google Chrome", "chrome": "Google Chrome",
            "chromium": "Chromium", "brave": "Brave Browser",
            "brave-browser": "Brave Browser", "microsoft-edge": "Microsoft Edge",
            "vivaldi": "Vivaldi", "firefox": "Firefox",
        }.get(name)
        if app:
            return [f"/Applications/{app}.app/Contents/MacOS/{app}",
                    str(Path.home() / f"Applications/{app}.app/Contents/MacOS/{app}")]
    return []

# A desktop-entry / application-launcher shortcut typically runs with a
# minimal $PATH that omits directories a browser can actually live in —
# notably /snap/bin (e.g. Brave on Ubuntu) and the Flatpak export dirs.
# Searched only as a fallback after the process's own inherited $PATH.
_EXTRA_BIN_DIRS = (
    "/snap/bin",
    "/var/lib/flatpak/exports/bin",
    str(Path.home() / ".local/share/flatpak/exports/bin"),
    "/usr/local/bin",
    "/usr/bin",
)


def _resolve_executable(name: str) -> str | None:
    """Absolute path for `name`, checked against $PATH plus _EXTRA_BIN_DIRS.

    Returns an absolute path (not just the bare name) specifically so a
    later subprocess.Popen([path, url]) doesn't have to re-resolve the name
    against the calling process's own possibly-restricted $PATH.
    """
    found = shutil.which(name)
    if found:
        return found
    search_path = os.pathsep.join([os.environ.get("PATH", ""), *_EXTRA_BIN_DIRS])
    return shutil.which(name, path=search_path)


def _resolve_browser(name: str) -> str | None:
    """Absolute path for browser `name`, trying its _BROWSER_ALTERNATES too."""
    found = next(
        (path for alt in _BROWSER_ALTERNATES.get(name, (name,))
         if (path := _resolve_executable(alt))),
        None,
    )
    if found:
        return found
    return next((p for p in _platform_browser_paths(name) if os.path.isfile(p)), None)


def _detect_running_browsers() -> list[str]:
    """One launchable process name per actual running browser (Linux only).

    Several process names in _BROWSER_PROCESSES can belong to the same
    real browser — e.g. Brave's child/renderer processes show up under
    "brave" even when the main process (or the only name actually
    resolvable, such as the "brave" snap wrapper vs. a non-executable
    "brave-browser" comm) differs — so results are collapsed to one entry
    per display name, preferring whichever matching process name actually
    resolves to a real executable.
    """
    if sys.platform != "linux":
        return []
    running = [
        name for name in _BROWSER_PROCESSES
        if subprocess.run(["pgrep", "-x", name], capture_output=True).returncode == 0
    ]
    by_label: dict[str, list[str]] = {}
    for name in running:
        by_label.setdefault(_BROWSER_DISPLAY_NAMES.get(name, name), []).append(name)
    return [
        next((n for n in names if _resolve_browser(n)), names[0])
        for names in by_label.values()
    ]


def _prompt_browser_choice(running: list[str]) -> str | None:
    """Ask the user, via a native desktop dialog, which running browser to use.

    Returns None (never raises) if no dialog tool is on PATH, the user cancels,
    or the dialog times out — callers should fall back to a silent default
    in that case rather than block indefinitely.
    """
    labels = [_BROWSER_DISPLAY_NAMES.get(b, b) for b in running]
    text = "Multiple browsers are running — open numa in:"

    if shutil.which("zenity"):
        cmd = ["zenity", "--list", "--radiolist", "--title=numa", f"--text={text}",
               "--column=", "--column=Browser", "--hide-header"]
        for i, label in enumerate(labels):
            cmd += ["TRUE" if i == 0 else "FALSE", label]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return None
        choice = result.stdout.strip()
        if result.returncode == 0 and choice in labels:
            return running[labels.index(choice)]
        return None

    if shutil.which("kdialog"):
        cmd = ["kdialog", "--title", "numa", "--radiolist", text]
        for i, (binary, label) in enumerate(zip(running, labels)):
            cmd += [binary, label, "on" if i == 0 else "off"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return None
        choice = result.stdout.strip()
        if result.returncode == 0 and choice in running:
            return choice
        return None

    return None


def _read_prefs() -> dict:
    """prefs.json, the file the Settings page saves to ({} if missing/bad).

    Read directly from the JSON file (mirroring backend.py's _load_prefs_file)
    rather than importing backend.py, so the launcher never pulls in FastAPI/DB
    startup cost just to check a setting.
    """
    import platform_utils as _platform_utils
    prefs_file = _platform_utils.get_data_dir() / "prefs.json"
    if prefs_file.exists():
        try:
            data = json.loads(prefs_file.read_text())
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _preferred_browser_pref() -> str:
    """The "preferred_browser" value from prefs.json, set on the Settings page."""
    return _read_prefs().get("preferred_browser", "") or ""


def _app_window_pref() -> bool:
    """Settings' "open in its own window" choice — on unless turned off."""
    return _read_prefs().get("app_window", True) is not False


def _app_window_browser(preferred: str) -> str | None:
    """Path of a browser that can open NuMa as its own window, or None.

    A browser chosen in Settings is used only if it can (choosing Firefox
    means a normal Firefox tab). With none chosen, a running Chromium-family
    browser wins, then any installed one in _APP_WINDOW_ORDER — no "which
    browser?" dialog, since the window doesn't sit among anyone's tabs.
    """
    if preferred:
        return _resolve_browser(preferred) if preferred in _APP_WINDOW_BROWSERS else None
    running = [b for b in _detect_running_browsers() if b in _APP_WINDOW_BROWSERS]
    return next(
        (path for name in (*running, *_APP_WINDOW_ORDER) if (path := _resolve_browser(name))),
        None,
    )

if not _FROZEN:
    sys.path.insert(0, str(_PROJECT_ROOT))

import uvicorn

_WEB_DIR = _PROJECT_ROOT if _FROZEN else Path(__file__).parent


def _app_window_path() -> str:
    """The path NuMa's own window opens at — backend.py redirects it to Home.

    Chromium names an --app window after its address's host and path
    (http://127.0.0.1:8000/nutrimagnus → "chrome-127.0.0.1__nutrimagnus-Default";
    the port plays no part), and that name is what a Linux desktop matches
    to a menu entry for the window's icon. A path of NuMa's own makes the
    name distinctive, and a different one for source keeps the two installs
    apart, each under its own menu entry.
    """
    return "/nutrimagnus" if _FROZEN else "/nutrimagnus-source"


def _app_window_id(browser_path: str, url: str) -> str:
    """The name the browser gives NuMa's window (Linux app_id / WM_CLASS)."""
    from urllib.parse import urlsplit
    base = os.path.basename(browser_path).lower()
    prefix = next((p for key, p in (("brave", "brave"), ("edge", "msedge"),
                                    ("vivaldi", "vivaldi")) if key in base), "chrome")
    parts = urlsplit(url)
    return f"{prefix}-{parts.hostname}_{(parts.path or '/').replace('/', '_')}-Default"


def _app_window_profile(browser_path: str) -> Path:
    """A browser profile used only by NuMa's own window.

    Its own profile makes the browser start a separate process for NuMa.
    KDE groups windows into applications by process, so in the shared one
    (with an ordinary browser window open, OneTab's say) Alt+Tab filed
    NuMa's window under the browser and showed no NuMa icon (2026-11-17).
    It also keeps the main profile's extensions out of NuMa's window: their
    shortcuts (OneTab's Alt+Shift+1 and 2) reach the browser before the page
    sees the key. A snap browser may only write inside ~/snap/<name>/, so
    its profile goes there. cmgr's launcher does the same, for the same reason.
    """
    name = os.path.basename(browser_path)
    snap_home = Path.home() / "snap" / name
    if browser_path.startswith("/snap/") and snap_home.is_dir():
        return snap_home / "common" / "numa-profile"
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
        return base / "NutriMagnus" / "browser-profile"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "NutriMagnus" / "browser-profile"
    config = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return config / "numa" / "browser-profile"


def _ensure_linux_window_entry(window_id: str) -> None:
    """Give NuMa's window its icon on a Linux desktop, whichever the desktop.

    KDE, GNOME and the rest pick a window's taskbar icon from the
    applications-menu entry whose file name or StartupWMClass= matches the
    window's name; with none, it gets a generic icon. So unless a menu entry
    already claims the name (install-linux.sh's and deploy/'s do, for
    Chrome and Chromium), write a hidden one named after it. Never raises:
    a missing icon is not worth failing a launch over.
    """
    if sys.platform != "linux":
        return
    try:
        data_home = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
        apps = data_home / "applications"
        entry = apps / f"{window_id}.desktop"
        claim = f"StartupWMClass={window_id}"
        for f in apps.glob("*.desktop") if apps.is_dir() else ():
            if f != entry and claim in f.read_text(errors="ignore").splitlines():
                return
        # The bundled icon of a packaged build lives in a temporary folder
        # that's gone when it exits, so keep a copy of it.
        icon = data_home / "icons" / "nutrimagnus-window.png"
        src = (_WEB_DIR / "static" / "icon-256.png").read_bytes()
        if not icon.exists() or icon.read_bytes() != src:
            icon.parent.mkdir(parents=True, exist_ok=True)
            icon.write_bytes(src)
        exec_cmd = (f'"{sys.executable}"' if _FROZEN
                    else f'"{sys.executable}" "{Path(__file__).resolve()}"')
        text = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            f"Name={'NutriMagnus' if _FROZEN else 'NuMa (source)'}\n"
            f"Exec={exec_cmd}\n"
            f"Icon={icon}\n"
            "NoDisplay=true\n"
            f"{claim}\n"
            "Comment=Matches NuMa's window to its icon; written by NuMa's launcher\n"
        )
        if not entry.exists() or entry.read_text(errors="ignore") != text:
            apps.mkdir(parents=True, exist_ok=True)
            entry.write_text(text)
    except OSError:
        pass


def _pick_and_open_browser(url: str) -> None:
    """Open `url` in the preferred/detected/chosen browser, or the OS default.

    With "own window" on (the default) and a Chromium-family browser
    available, it opens as an app window — see _app_window_browser().
    Otherwise, as a normal tab. Order: an explicit Settings preference wins
    outright; otherwise, with
    zero or one browser running, use that (or the OS default if none);
    with more than one, ask via _prompt_browser_choice(), falling back to
    the first-detected one if that returns nothing (no dialog tool, user
    cancelled, or it timed out).
    """
    binary = _preferred_browser_pref()
    if _app_window_pref():
        app = _app_window_browser(binary)
        if app:
            from urllib.parse import urlsplit
            app_url = f"{urlsplit(url).scheme}://{urlsplit(url).netloc}{_app_window_path()}"
            _ensure_linux_window_entry(_app_window_id(app, app_url))
            try:
                profile = _app_window_profile(app)
                profile.mkdir(parents=True, exist_ok=True)
                subprocess.Popen(
                    [app, f"--app={app_url}", f"--user-data-dir={profile}",
                     "--no-first-run", "--no-default-browser-check"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                return
            except OSError:
                pass  # fall through to a normal tab
    if not binary:
        running = _detect_running_browsers()
        if len(running) > 1:
            binary = _prompt_browser_choice(running) or running[0]
        elif running:
            binary = running[0]
    if binary:
        target = _resolve_browser(binary) or binary
        try:
            subprocess.Popen(
                [target, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return
        except OSError:
            pass  # fall through to the OS-default lookup below
    webbrowser.open(url)


def _open_after(url: str, delay: float = 1.2) -> None:
    time.sleep(delay)
    _pick_and_open_browser(url)


# Served on the real port while the app itself is still importing and
# starting, so the browser tab can open at once and say so, instead of the
# user staring at nothing for the seconds a cold start takes (longer on a
# slow machine). It reloads itself every second; the first reload after the
# real server takes over the socket gets the real page, at the same URL.
_LOADING_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="1">
<title>Loading NutriMagnus…</title>
<style>
  body { font-family: system-ui, sans-serif; background: #fff; color: #222;
         display: flex; align-items: center; justify-content: center;
         height: 90vh; margin: 0; }
  @media (prefers-color-scheme: dark) { body { background: #1e1e1e; color: #ddd; } }
  p { font-size: 1.5rem; }
</style></head>
<body><p>Loading NutriMagnus…</p></body></html>
""".encode("utf-8")

# Swapped in if the app fails to start, so the tab says so instead of
# reloading into the browser's own "unable to connect" page.
_FAILED_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>NutriMagnus did not start</title>
<style>body { font-family: system-ui, sans-serif; max-width: 40rem; margin: 3rem auto; padding: 0 1rem; }</style>
</head><body><h1>NutriMagnus did not start</h1>
<p>Something went wrong while NutriMagnus was starting. Close this tab and try
starting it again. If it happens again, the error message from the window or
log file NutriMagnus was started from shows what went wrong.</p></body></html>
""".encode("utf-8")


class _LoadingServer:
    """Answer every request on `sock` with _LOADING_PAGE until stop().

    The listening socket itself is NOT closed on stop: it is handed to
    uvicorn, so no connection made in between is refused — it just waits in
    the listen backlog until the real server accepts it.
    """

    def __init__(self, sock: socket.socket) -> None:
        self._sock = sock
        self.page = _LOADING_PAGE
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def start(self) -> None:
        self._sock.settimeout(0.1)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join()
        self._sock.settimeout(None)

    def _serve(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _addr = self._sock.accept()
            except (socket.timeout, OSError):
                continue
            try:
                conn.settimeout(2)
                data = b""
                while b"\r\n\r\n" not in data and len(data) < 65536:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                conn.sendall(
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: text/html; charset=utf-8\r\n"
                    b"Cache-Control: no-store\r\n"
                    b"Connection: close\r\n"
                    b"Content-Length: " + str(len(self.page)).encode() + b"\r\n\r\n"
                    + self.page
                )
            except OSError:
                pass
            finally:
                conn.close()


def _bind_socket(host: str, port: int) -> socket.socket:
    """A listening socket on host:port, set up the way uvicorn binds its own."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sys.platform != "win32":
        # Same as uvicorn: on Windows SO_REUSEADDR would let a second
        # process bind a port that's already in use.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(2048)
    sock.set_inheritable(True)
    return sock


def main() -> None:
    parser = argparse.ArgumentParser(description="numa web app launcher")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (dev mode)")
    parser.add_argument(
        "--open-browser", metavar="URL",
        help="Just open the preferred/detected browser at URL and exit — "
             "used by launch-web.sh once it has confirmed the server is up, "
             "instead of a separate script hardcoding one browser.",
    )
    args = parser.parse_args()

    if args.open_browser:
        _pick_and_open_browser(args.open_browser)
        return

    url = f"http://{args.host}:{args.port}"

    # Check if port is already in use and offer to kill the occupant
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex((args.host, args.port)) == 0:
            print(f"Port {args.port} is already in use.")
            if sys.stdin.isatty():
                ans = input("Kill the existing process and restart? [y/N] ").strip().lower()
            else:
                # Non-interactive (launched from CLI) — kill automatically
                ans = "y"
            if ans == "y":
                if sys.platform == "win32":
                    # Find and kill the PID holding the port via netstat
                    out = subprocess.run(
                        ["netstat", "-ano"], capture_output=True, text=True
                    ).stdout
                    for line in out.splitlines():
                        if f":{args.port} " in line and "LISTENING" in line:
                            pid = line.split()[-1]
                            subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True)
                            break
                else:
                    subprocess.run(["fuser", "-k", f"{args.port}/tcp"], capture_output=True)
                time.sleep(0.5)
                print("Old process terminated.")
            else:
                print("Aborted. Stop the existing server first, then re-run launcher.py.")
                sys.exit(1)

    print(f"Starting numa at {url}")

    if args.reload:
        # Dev mode: uvicorn's reloader runs the app in a child process and
        # can't take over a socket bound here, so no loading page.
        if not args.no_browser:
            threading.Thread(target=_open_after, args=(url,), daemon=True).start()
        uvicorn.run("backend:app", host=args.host, port=args.port, reload=True, app_dir=str(_WEB_DIR))
        return

    # Bind the port and show the loading page first, then do the slow part
    # (importing the app) while the browser tab is already open. Also means
    # launch-web.sh's wait-for-the-port loop opens the browser at once.
    sock = _bind_socket(args.host, args.port)
    loading = _LoadingServer(sock)
    loading.start()
    if not args.no_browser:
        threading.Thread(target=_open_after, args=(url, 0), daemon=True).start()

    if str(_WEB_DIR) not in sys.path:
        sys.path.insert(0, str(_WEB_DIR))
    try:
        import backend
    except Exception:
        # Leave the failure page up long enough for the tab's next reload
        # to show it, then exit with the real traceback.
        loading.page = _FAILED_PAGE
        time.sleep(5)
        raise
    server = uvicorn.Server(uvicorn.Config(backend.app, host=args.host, port=args.port))
    backend.app.state.server = server     # lets Ctrl+Q (/quit) stop it cleanly
    backend.start_browser_watch()         # and Firefox quitting, which keeps Ctrl+Q
    loading.stop()
    server.run(sockets=[sock])


if __name__ == "__main__":
    main()
