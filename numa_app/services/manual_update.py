"""
manual_update.py — check for, download, and serve a newer User Manual than
the one baked into the running program, independent of program updates.

The manual is published as a rolling GitHub release (tag "manual-latest",
marked prerelease so it never becomes the program's "latest" release) holding
three assets: user-manual.html, manual-manifest.json, manual-manifest.sig.
The manifest carries the manual's stamp, the html's SHA-256 and size, and the
oldest program VERSION the manual describes; the .sig is a base64 Ed25519
signature over the manifest's exact bytes, made by scripts/publish_manual.py
with a private key that never leaves the publisher's machine. Only the public
key is baked in here (_PUBLIC_KEY_B64). Anything that fails verification —
bad signature, hash mismatch, malformed manifest, missing `cryptography`
package — is refused, never served. A downloaded manual is re-verified every
time it is served, so on-disk tampering is caught too, and is used only while
its stamp is newer than the baked-in one (so a program update never gets
stuck on an older downloaded copy, and a replayed old signed manual can't
downgrade you).

Like update_check.py, nothing here raises or blocks on a bad network.

Docs: README-numa-documentation.md (Web app section — Manual updates).
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

import platform_utils as _platform_utils

_GITHUB_OWNER = "tom-cloyd"
_GITHUB_REPO = "NutriMagnus"
MANUAL_TAG = "manual-latest"
_ASSET_BASE = f"https://github.com/{_GITHUB_OWNER}/{_GITHUB_REPO}/releases/download/{MANUAL_TAG}"
RELEASE_PAGE_URL = f"https://github.com/{_GITHUB_OWNER}/{_GITHUB_REPO}/releases/tag/{MANUAL_TAG}"
HTML_ASSET = "user-manual.html"
MANIFEST_ASSET = "manual-manifest.json"
SIGNATURE_ASSET = "manual-manifest.sig"

# Raw 32-byte Ed25519 public key, base64. The matching private key lives only
# on the publisher's machine (see scripts/publish_manual.py). Replacing it
# requires a program update — that's the point.
_PUBLIC_KEY_B64 = "vnZTDvqy28FKSEGOtyXeJQ17giB4rKJiH+bwF9fLLAM="

_TIMEOUT_SECONDS = 3.0
_DOWNLOAD_TIMEOUT_SECONDS = 30.0
_CACHE_TTL_SECONDS = 6 * 60 * 60
_MAX_HTML_BYTES = 20 * 1024 * 1024
_MAX_MANIFEST_BYTES = 16 * 1024

_STAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}:\d{4}$")
_HTML_STAMP_RE = re.compile(r"Updated (\d{4}-\d{2}-\d{2}:\d{4})")


def stamp_of_html(text: str) -> str | None:
    """The 'Updated YYYY-MM-DD:HHMM' stamp from a built manual's header."""
    m = _HTML_STAMP_RE.search(text)
    return m.group(1) if m else None


def installed_dir() -> Path:
    return _platform_utils.get_data_dir() / "manual"


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_bundle(manifest_bytes: bytes, signature_b64: bytes | str, html_bytes: bytes | None = None) -> dict | None:
    """Return the parsed manifest if its signature is valid (and, when
    html_bytes is given, the html matches the manifest's hash and size);
    otherwise None. Never raises."""
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        key = Ed25519PublicKey.from_public_bytes(base64.b64decode(_PUBLIC_KEY_B64))
        sig = base64.b64decode(signature_b64.strip() if isinstance(signature_b64, (bytes, str)) else b"", validate=True)
        try:
            key.verify(sig, manifest_bytes)
        except InvalidSignature:
            return None
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        if manifest.get("format") != 1 or not _STAMP_RE.match(str(manifest.get("manual_stamp", ""))):
            return None
        req = str(manifest.get("requires_program", ""))
        if not _STAMP_RE.match(req):
            return None
        if html_bytes is not None:
            if len(html_bytes) != manifest.get("size"):
                return None
            if hashlib.sha256(html_bytes).hexdigest() != manifest.get("sha256"):
                return None
            if stamp_of_html(html_bytes.decode("utf-8", errors="replace")) != manifest["manual_stamp"]:
                return None
        return manifest
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Which manual to serve
# ---------------------------------------------------------------------------

_installed_cache: tuple[tuple, dict | None] | None = None


def _load_installed() -> tuple[Path, dict] | None:
    """The downloaded manual and its verified manifest, or None if absent or
    it fails verification. Re-verified whenever the files change."""
    global _installed_cache
    d = installed_dir()
    html_p, man_p, sig_p = d / HTML_ASSET, d / MANIFEST_ASSET, d / SIGNATURE_ASSET
    try:
        sig_key = tuple((p.stat().st_mtime_ns, p.stat().st_size) for p in (html_p, man_p, sig_p))
    except OSError:
        return None
    if _installed_cache and _installed_cache[0] == (str(d),) + sig_key:
        m = _installed_cache[1]
        return (html_p, m) if m else None
    manifest = None
    try:
        manifest = verify_bundle(man_p.read_bytes(), sig_p.read_bytes(), html_p.read_bytes())
    except OSError:
        pass
    _installed_cache = ((str(d),) + sig_key, manifest)
    return (html_p, manifest) if manifest else None


def get_active_manual(baked_html: Path) -> dict:
    """Pick the manual to serve. Returns {'path', 'stamp', 'source'
    ('baked'|'downloaded'), 'requires_program'}. The downloaded copy wins only
    when it verifies and its stamp is newer than the baked-in one."""
    baked_stamp = None
    try:
        baked_stamp = stamp_of_html(baked_html.read_text(encoding="utf-8"))
    except OSError:
        pass
    inst = _load_installed()
    if inst and (baked_stamp is None or inst[1]["manual_stamp"] > baked_stamp):
        return {"path": inst[0], "stamp": inst[1]["manual_stamp"], "source": "downloaded",
                "requires_program": inst[1]["requires_program"]}
    return {"path": baked_html, "stamp": baked_stamp, "source": "baked", "requires_program": None}


# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------

def _fetch(name: str, max_bytes: int, timeout: float) -> bytes | None:
    req = urllib.request.Request(f"{_ASSET_BASE}/{name}", headers={"User-Agent": "NutriMagnus-manual-update"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read(max_bytes + 1)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError):
        return None
    return data if len(data) <= max_bytes else None


_cache: dict | None = None
_cache_checked_at: float = 0.0
_cache_for: tuple | None = None


def clear_cache() -> None:
    global _cache, _cache_checked_at, _cache_for
    _cache = None
    _cache_checked_at = 0.0
    _cache_for = None


def check_for_manual_update(current_stamp: str | None, program_version: str) -> dict | None:
    """Return {'stamp', 'requires_program', 'program_too_old', 'url'} if a
    newer, correctly signed manual is published, else None. Only the small
    signed manifest is fetched here; the html is fetched and verified by
    install_update()."""
    global _cache, _cache_checked_at, _cache_for
    now = time.monotonic()
    key = (current_stamp, program_version)
    if _cache_for == key and now - _cache_checked_at < _CACHE_TTL_SECONDS:
        return _cache
    result = None
    man = _fetch(MANIFEST_ASSET, _MAX_MANIFEST_BYTES, _TIMEOUT_SECONDS)
    sig = _fetch(SIGNATURE_ASSET, _MAX_MANIFEST_BYTES, _TIMEOUT_SECONDS) if man else None
    manifest = verify_bundle(man, sig) if man and sig else None
    if manifest and (current_stamp is None or manifest["manual_stamp"] > current_stamp):
        result = {
            "stamp": manifest["manual_stamp"],
            "requires_program": manifest["requires_program"],
            "program_too_old": program_version < manifest["requires_program"],
            "url": RELEASE_PAGE_URL,
        }
    _cache, _cache_checked_at, _cache_for = result, now, key
    return result


def install_update(current_stamp: str | None) -> dict:
    """Download, verify, and install the published manual. Returns
    {'ok': True, 'stamp': ...} or {'ok': False, 'error': plain-language
    reason}. Nothing is written unless everything verifies."""
    man = _fetch(MANIFEST_ASSET, _MAX_MANIFEST_BYTES, _DOWNLOAD_TIMEOUT_SECONDS)
    sig = _fetch(SIGNATURE_ASSET, _MAX_MANIFEST_BYTES, _DOWNLOAD_TIMEOUT_SECONDS)
    if not man or not sig:
        return {"ok": False, "error": "Couldn't reach GitHub — this is usually just your internet connection. Check that you're online and press Try again."}
    manifest = verify_bundle(man, sig)
    if not manifest:
        return {"ok": False, "error": "The new manual failed NutriMagnus's safety check, so it was NOT installed and your current manual is unchanged. Trying again won't help — please text Tom (see Getting more help) so this can be fixed."}
    if current_stamp is not None and manifest["manual_stamp"] <= current_stamp:
        return {"ok": False, "error": "You already have the newest manual, so there was nothing to install."}
    html = _fetch(HTML_ASSET, _MAX_HTML_BYTES, _DOWNLOAD_TIMEOUT_SECONDS)
    if not html:
        return {"ok": False, "error": "The manual file didn't finish downloading — this is usually a brief connection problem. Press Try again in a minute; if it keeps failing, text Tom (see Getting more help)."}
    if not verify_bundle(man, sig, html):
        return {"ok": False, "error": "The downloaded manual failed NutriMagnus's safety check, so it was NOT installed and your current manual is unchanged. Pressing Try again once is fine (a bad download can cause this); if it fails again, please text Tom (see Getting more help)."}
    try:
        d = installed_dir()
        d.mkdir(parents=True, exist_ok=True)
        # html first, manifest/sig last: a half-finished install fails
        # verification (mismatched hash) and is ignored, never served.
        for name, data in ((HTML_ASSET, html), (MANIFEST_ASSET, man), (SIGNATURE_ASSET, sig)):
            tmp = d / (name + ".tmp")
            tmp.write_bytes(data)
            tmp.replace(d / name)
    except OSError as exc:
        return {"ok": False, "error": f"Couldn't save the manual on this computer ({exc}). Press Try again; if it keeps failing, text Tom (see Getting more help)."}
    clear_cache()
    return {"ok": True, "stamp": manifest["manual_stamp"]}
