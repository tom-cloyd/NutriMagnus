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
        target = _resolve_executable(binary) or binary
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

    if not args.no_browser:
        t = threading.Thread(target=_open_after, args=(url,), daemon=True)
        t.start()

    uvicorn.run(
        "backend:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        app_dir=str(_WEB_DIR),
    )


if __name__ == "__main__":
    main()
