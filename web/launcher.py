"""
launcher.py — Start the numa web app and open a browser tab.

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

# A Settings choice that distros install under more than one binary name —
# tried in order, so the single "Chromium" choice works whichever one exists.
_BROWSER_ALTERNATES = {
    "chromium": ("chromium", "chromium-browser"),
    "chromium-browser": ("chromium-browser", "chromium"),
}

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
        next((n for n in names if _resolve_executable(n)), names[0])
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


def _preferred_browser_pref() -> str:
    """The "preferred_browser" value from prefs.json, set on the Settings page.

    Read directly from the JSON file (mirroring backend.py's _load_prefs_file)
    rather than importing backend.py, so the launcher never pulls in FastAPI/DB
    startup cost just to check one setting.
    """
    import platform_utils as _platform_utils
    prefs_file = _platform_utils.get_data_dir() / "prefs.json"
    if prefs_file.exists():
        try:
            data = json.loads(prefs_file.read_text())
            if isinstance(data, dict):
                return data.get("preferred_browser", "") or ""
        except (json.JSONDecodeError, OSError):
            pass
    return ""

if not _FROZEN:
    sys.path.insert(0, str(_PROJECT_ROOT))

import uvicorn

_WEB_DIR = _PROJECT_ROOT if _FROZEN else Path(__file__).parent


def _pick_and_open_browser(url: str) -> None:
    """Open `url` in the preferred/detected/chosen browser, or the OS default.

    Order: an explicit Settings preference wins outright; otherwise, with
    zero or one browser running, use that (or the OS default if none);
    with more than one, ask via _prompt_browser_choice(), falling back to
    the first-detected one if that returns nothing (no dialog tool, user
    cancelled, or it timed out).
    """
    binary = _preferred_browser_pref()
    if not binary:
        running = _detect_running_browsers()
        if len(running) > 1:
            binary = _prompt_browser_choice(running) or running[0]
        elif running:
            binary = running[0]
    if binary:
        target = next(
            (path for name in _BROWSER_ALTERNATES.get(binary, (binary,))
             if (path := _resolve_executable(name))),
            binary,
        )
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
    loading.stop()
    server.run(sockets=[sock])


if __name__ == "__main__":
    main()
