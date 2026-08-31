"""
self_update.py — download the latest GitHub release's binary/icon and
replace the currently-running packaged install in place, for the home
page's "Update Now" button.

Only meaningful for a packaged (PyInstaller onefile) Linux install —
a source/dev checkout has nothing sensible to self-replace, and there's
no Windows build published from this same release flow yet. is_available()
gates both.

Replacing the binary while it's still running is safe on Linux: os.replace()
is atomic, and the OS keeps the current process's already-open executable
file alive under its old inode until the process exits, so this session
keeps running unaffected. The new file is picked up the next time
NutriMagnus is launched.

Docs: README-numa-documentation.md (Web app section).
"""
from __future__ import annotations

import os
import stat
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

_GITHUB_OWNER = "tom-cloyd"
_GITHUB_REPO = "NutriMagnus"
_LATEST_DOWNLOAD_BASE = f"https://github.com/{_GITHUB_OWNER}/{_GITHUB_REPO}/releases/latest/download"
_TIMEOUT_SECONDS = 30.0
_MIN_BINARY_BYTES = 5_000_000  # sanity floor — a truncated/error download won't be this big

_ICON_PATH = Path.home() / ".local" / "share" / "icons" / "nutrimagnus.png"


def is_available() -> bool:
    """True only for a packaged (PyInstaller onefile) Linux install — the
    one thing this can safely self-replace."""
    return bool(getattr(sys, "frozen", False)) and sys.platform.startswith("linux")


def _download(url: str, *, min_bytes: int = 0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "NutriMagnus-self-update"})
    with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
        if resp.status != 200:
            raise RuntimeError(f"unexpected status {resp.status} fetching {url}")
        data = resp.read()
    if len(data) < min_bytes:
        raise RuntimeError(f"downloaded file too small ({len(data)} bytes) — likely not the real binary")
    return data


def perform_update() -> dict:
    """Download and install the latest release in place of the running
    binary. Returns {'ok': True} on success or {'ok': False, 'error': str}
    on failure — never raises, so the caller can always show something
    sensible."""
    if not is_available():
        return {"ok": False, "error": "Self-update is only available for the packaged Linux install."}

    exe_path = Path(sys.executable).resolve()
    try:
        binary_data = _download(f"{_LATEST_DOWNLOAD_BASE}/nutrimagnus", min_bytes=_MIN_BINARY_BYTES)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, RuntimeError) as e:
        return {"ok": False, "error": f"Download failed: {e}"}

    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(dir=str(exe_path.parent), prefix=".nutrimagnus-update-")
        with os.fdopen(fd, "wb") as f:
            f.write(binary_data)
        os.chmod(tmp_path, os.stat(exe_path).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        os.replace(tmp_path, exe_path)  # atomic on the same filesystem
    except OSError as e:
        if tmp_path:
            Path(tmp_path).unlink(missing_ok=True)
        return {"ok": False, "error": f"Could not replace the installed binary: {e}"}

    # Icon refresh is best-effort — a failure here isn't reported as an
    # update failure, since the binary swap (the part that matters) already
    # succeeded.
    try:
        icon_data = _download(f"{_LATEST_DOWNLOAD_BASE}/nutrimagnus.png")
        _ICON_PATH.parent.mkdir(parents=True, exist_ok=True)
        _ICON_PATH.write_bytes(icon_data)
    except Exception:
        pass

    return {"ok": True}
