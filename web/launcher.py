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
import socket
import threading
import time
import webbrowser

if not _FROZEN:
    sys.path.insert(0, str(_PROJECT_ROOT))

import uvicorn

_WEB_DIR = _PROJECT_ROOT if _FROZEN else Path(__file__).parent


def _open_after(url: str, delay: float = 1.2) -> None:
    time.sleep(delay)
    webbrowser.open(url)


def main() -> None:
    parser = argparse.ArgumentParser(description="numa web app launcher")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (dev mode)")
    args = parser.parse_args()

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
                import subprocess
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
