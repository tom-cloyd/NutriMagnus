#!/usr/bin/env python3
"""
publish_manual.py — publish the current User Manual on its own, without a
program release: rebuilds user-manual.html, writes a signed manifest, and
uploads all three files to the rolling "manual-latest" GitHub release, which
running copies of NuMa check separately from program updates (see
numa_app/services/manual_update.py).

Usage (repo root):
    python scripts/publish_manual.py --dry-run   # build + sign into a temp dir, upload nothing
    python scripts/publish_manual.py             # build + sign + upload

Requires: `cryptography`; and for a real upload, GITHUB_TOKEN with repo write
scope. The Ed25519 private key is read from $NUMA_MANUAL_SIGNING_KEY or
~/.config/numa-signing/manual_signing_key.pem — keep it OUT of the repo and
back it up: if it's lost, manual updates stop verifying until a new program
release ships a replacement public key.

The rolling release is created as a PRERELEASE on purpose: GitHub's
"releases/latest" (which the program-update check and install-linux.sh use)
skips prereleases, so this never displaces the real latest program release.

manifest "requires_program" is the version.py VERSION this manual was written
against; older programs show a "describes newer features" warning.

Docs: README-numa-documentation.md (Web app section — Manual updates).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import pathlib
import sys
import tempfile
import urllib.error
import urllib.request

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from numa_app.services import manual_update as mu  # noqa: E402

API_BASE = f"https://api.github.com/repos/{mu._GITHUB_OWNER}/{mu._GITHUB_REPO}"
UPLOADS_BASE = f"https://uploads.github.com/repos/{mu._GITHUB_OWNER}/{mu._GITHUB_REPO}"
KEY_PATH = pathlib.Path(os.environ.get("NUMA_MANUAL_SIGNING_KEY")
                        or pathlib.Path.home() / ".config" / "numa-signing" / "manual_signing_key.pem")


def build_bundle(out_dir: pathlib.Path) -> dict:
    """Rebuild the manual, then write html + signed manifest into out_dir.
    Returns the manifest."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_manual", REPO_ROOT / "scripts" / "build_manual.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()

    from cryptography.hazmat.primitives import serialization
    import version as _v

    html = (REPO_ROOT / "user-manual.html").read_bytes()
    stamp = mu.stamp_of_html(html.decode("utf-8"))
    if not stamp:
        sys.exit("ERROR: couldn't find the 'Updated YYYY-MM-DD:HHMM' stamp in user-manual.html.")
    manifest = {
        "format": 1,
        "manual_stamp": stamp,
        "sha256": hashlib.sha256(html).hexdigest(),
        "size": len(html),
        "requires_program": _v.VERSION,
    }
    manifest_bytes = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8")
    if not KEY_PATH.exists():
        sys.exit(f"ERROR: signing key not found at {KEY_PATH}")
    key = serialization.load_pem_private_key(KEY_PATH.read_bytes(), password=None)
    sig = base64.b64encode(key.sign(manifest_bytes))

    (out_dir / mu.HTML_ASSET).write_bytes(html)
    (out_dir / mu.MANIFEST_ASSET).write_bytes(manifest_bytes)
    (out_dir / mu.SIGNATURE_ASSET).write_bytes(sig)
    if not mu.verify_bundle(manifest_bytes, sig, html):
        sys.exit("ERROR: freshly signed bundle does not verify against the public key baked into "
                 "manual_update.py — the signing key and _PUBLIC_KEY_B64 don't match.")
    return manifest


def _api(url: str, token: str, *, method: str = "GET", body: bytes | None = None,
         content_type: str = "application/json") -> dict | list | None:
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": content_type,
        "User-Agent": "NutriMagnus-publish-manual",
    })
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else None


def upload(out_dir: pathlib.Path, manifest: dict, token: str) -> None:
    try:
        release = _api(f"{API_BASE}/releases/tags/{mu.MANUAL_TAG}", token)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        target = os.environ.get("NUMA_MANUAL_TARGET_BRANCH", "main")
        release = _api(f"{API_BASE}/releases", token, method="POST", body=json.dumps({
            "tag_name": mu.MANUAL_TAG, "target_commitish": target, "name": "User Manual (rolling)",
            "body": "Rolling release holding the newest published User Manual. Checked by NutriMagnus "
                    "separately from program releases; not a program release.",
            "prerelease": True,
        }).encode())
    existing = {a["name"]: a["id"] for a in release.get("assets", [])}
    for name, ctype in ((mu.HTML_ASSET, "text/html"), (mu.MANIFEST_ASSET, "application/json"),
                        (mu.SIGNATURE_ASSET, "text/plain")):
        if name in existing:
            _api(f"{API_BASE}/releases/assets/{existing[name]}", token, method="DELETE")
        _api(f"{UPLOADS_BASE}/releases/{release['id']}/assets?name={name}", token, method="POST",
             body=(out_dir / name).read_bytes(), content_type=ctype)
        print(f"  uploaded {name}")
    _api(f"{API_BASE}/releases/{release['id']}", token, method="PATCH", body=json.dumps({
        "prerelease": True, "name": f"User Manual (rolling) — {manifest['manual_stamp']}"}).encode())


def main() -> int:
    dry = "--dry-run" in sys.argv
    if dry:
        out = pathlib.Path(tempfile.mkdtemp(prefix="numa-manual-publish-"))
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("ERROR: GITHUB_TOKEN not set.")
        out = pathlib.Path(tempfile.mkdtemp(prefix="numa-manual-publish-"))
    manifest = build_bundle(out)
    print(f"Manual {manifest['manual_stamp']} (describes program {manifest['requires_program']}) "
          f"built and signed in {out}")
    if dry:
        print("Dry run: nothing uploaded.")
        return 0
    upload(out, manifest, token)
    print(f"Published to {mu.RELEASE_PAGE_URL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
