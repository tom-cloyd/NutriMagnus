"""Stopping NuMa along with the browser it's shown in.

Two ways NuMa ends with its window:

* Ctrl+Q in a Chromium-family app window (or any browser that passes the key
  to the page): base.html posts /quit; the server closes NuMa's own window
  (close_app_window) and stops.
* Firefox keeps Ctrl+Q for itself and never shows that key to a page, so it
  quits Firefox instead. FirefoxWatch notices: when the most recent NuMa page
  was viewed in Firefox and Firefox is then no longer running, NuMa stops.
  Closing only NuMa's tab doesn't count; Firefox has to be gone.

Docs: user-manual.md, "Finding your way around" (#quit-numa).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from typing import Callable

_FIREFOX_NAMES = {"firefox", "firefox-bin", "firefox-esr", "firefox.real"}


def is_firefox_ua(user_agent: str) -> bool:
    """A Firefox user agent (not one of the browsers that also say Gecko)."""
    return "Firefox/" in user_agent and "Seamonkey" not in user_agent


def firefox_running() -> bool | None:
    """Whether a Firefox main process is running; None if it can't be told."""
    try:
        if sys.platform.startswith("linux"):
            for pid in os.listdir("/proc"):
                if not pid.isdigit():
                    continue
                try:
                    with open(f"/proc/{pid}/cmdline", "rb") as f:
                        args = f.read().split(b"\0")
                except OSError:
                    continue
                if (args and os.path.basename(args[0].decode(errors="replace")) in _FIREFOX_NAMES
                        and b"-contentproc" not in args):
                    return True
            return False
        if sys.platform == "win32":
            out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq firefox.exe", "/NH"],
                                 capture_output=True, text=True, timeout=10,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)).stdout
            return "firefox.exe" in out.lower()
        if shutil.which("pgrep"):
            return subprocess.run(["pgrep", "-x", "firefox"], capture_output=True,
                                  timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        pass
    return None


class FirefoxWatch:
    """Calls on_quit once Firefox has quit, if NuMa's last page was in Firefox.

    page_seen() is called for every page NuMa serves. Firefox counts as gone
    only after it was seen running while a Firefox page was the latest, and
    then missing on `misses` checks in a row (so a brief gap can't stop NuMa).
    """

    def __init__(self, on_quit: Callable[[], None], interval: float = 2.0, misses: int = 2,
                 running: Callable[[], bool | None] = firefox_running):
        self.on_quit, self.interval, self.misses, self.running = on_quit, interval, misses, running
        self.last_page_firefox = False
        self._seen_running = False
        self._missing = 0
        self._started = False

    def page_seen(self, user_agent: str) -> None:
        self.last_page_firefox = is_firefox_ua(user_agent)
        if not self.last_page_firefox:
            self._seen_running = False

    def check(self) -> bool:
        """One check; True when NuMa should stop now."""
        if not self.last_page_firefox:
            self._missing = 0
            return False
        state = self.running()
        if state is None:
            return False
        if state:
            self._seen_running, self._missing = True, 0
            return False
        if not self._seen_running:
            return False
        self._missing += 1
        return self._missing >= self.misses

    def start(self) -> None:
        if self._started:
            return
        self._started = True

        def _loop():
            while True:
                time.sleep(self.interval)
                if self.check():
                    self.on_quit()
                    return
        threading.Thread(target=_loop, daemon=True, name="numa-firefox-watch").start()


def close_app_window(path: str) -> None:
    """Ask KDE to close NuMa's own app window, opened at `path` (/nutrimagnus
    or /nutrimagnus-source; see launcher._window_path). A page can't reliably
    close a window it didn't open, so the server does it, with a KWin script
    over D-Bus. Does nothing off KDE or if anything fails; the page's "NuMa
    has stopped" note stays up instead."""
    qdbus = shutil.which("qdbus6") or shutil.which("qdbus")
    if not qdbus:
        return
    suffix = "_" + path.replace("/", "_") + "-Default"
    script = ("var ws = workspace.windowList();"
              "for (var i = 0; i < ws.length; i++)"
              f"  if (String(ws[i].resourceClass).endsWith({suffix!r})) ws[i].closeWindow();")
    name = f"numa-close-{os.getpid()}"
    fname = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(script)
            fname = f.name
        sid = subprocess.run([qdbus, "org.kde.KWin", "/Scripting", "org.kde.kwin.Scripting.loadScript",
                              fname, name], capture_output=True, text=True, timeout=5).stdout.strip()
        subprocess.run([qdbus, "org.kde.KWin", f"/Scripting/Script{sid}", "org.kde.kwin.Script.run"],
                       capture_output=True, timeout=5)
        time.sleep(0.5)
        subprocess.run([qdbus, "org.kde.KWin", "/Scripting", "org.kde.kwin.Scripting.unloadScript", name],
                       capture_output=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        pass
    finally:
        if fname:
            try:
                os.unlink(fname)
            except OSError:
                pass
