"""
launcher.py — Start the numa web app and open a browser tab.

Usage:
    python web/launcher.py           # default port 8000
    python web/launcher.py --port 8080
    python web/launcher.py --no-browser
"""
import argparse
import signal
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn

_WEB_DIR = Path(__file__).parent


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
            ans = input("Kill the existing process and restart? [y/N] ").strip().lower()
            if ans == "y":
                import subprocess
                result = subprocess.run(
                    ["fuser", "-k", f"{args.port}/tcp"], capture_output=True
                )
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
