"""
update_check.py — check GitHub for a NuMa release newer than the one
running, for the "update available" banner on the home page.

Never raises and never blocks the app on a slow/offline network: any
failure (no connection, timeout, rate limit, malformed response) is treated
the same as "no update available." Results are cached in-process for
_CACHE_TTL_SECONDS so a burst of home-page views doesn't re-hit GitHub's API
each time.

Docs: README-numa-documentation.md (Web app section).
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

_GITHUB_OWNER = "tom-cloyd"
_GITHUB_REPO = "NutriMagnus"
_LATEST_RELEASE_URL = f"https://api.github.com/repos/{_GITHUB_OWNER}/{_GITHUB_REPO}/releases/latest"
_TIMEOUT_SECONDS = 2.0
_CACHE_TTL_SECONDS = 6 * 60 * 60  # 6 hours

_cache: dict | None = None
_cache_checked_at: float = 0.0
_cache_for_version: str | None = None


def _tag_for(version_str: str) -> str:
    # version.py uses "YYYY-MM-DD:HHMM" — ":" isn't a legal git ref character.
    # Matches scripts/create_release.py's _tag_for(), which is what actually
    # tags each GitHub release.
    return "v" + version_str.replace(":", "-")


def _fetch_latest_release() -> dict | None:
    """Raw GitHub API call. Returns None on any failure."""
    req = urllib.request.Request(
        _LATEST_RELEASE_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "NutriMagnus-update-check",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError):
        return None


def check_for_update(current_version: str) -> dict | None:
    """Return {'tag', 'url'} if a newer release than current_version is
    published on GitHub, else None.

    The fixed-width "YYYY-MM-DD:HHMM" stamp (tag-ified to
    "vYYYY-MM-DD-HHMM") sorts correctly as a plain string, so a direct
    string comparison is enough to tell "newer" — no version-parsing
    library needed.
    """
    global _cache, _cache_checked_at, _cache_for_version
    now = time.monotonic()
    if _cache_for_version == current_version and now - _cache_checked_at < _CACHE_TTL_SECONDS:
        return _cache

    data = _fetch_latest_release()
    result = None
    if data:
        latest_tag = data.get("tag_name", "")
        current_tag = _tag_for(current_version)
        if latest_tag and latest_tag > current_tag:
            result = {"tag": latest_tag, "url": data.get("html_url", "")}

    _cache = result
    _cache_checked_at = now
    _cache_for_version = current_version
    return result
