#!/usr/bin/env python3
"""
create_release.py — create a Codeberg release for the current version and
upload the freshly built Linux binary as its asset. Run from the repo root
after `pyinstaller --onefile --name nutrimagnus numa.py` has produced
dist/nutrimagnus. Used by .forgejo/workflows/release.yml on every push to
main; safe to run manually too.

Release notes are pulled from user-manual.md's Appendix K ("Recent program
updates log") section matching today's date (#### Month Day), falling back
to a generic message if that section doesn't exist yet (e.g. no manual
changes were logged today).

Requires CODEBERG_TOKEN in the environment (a Codeberg access token with
repo write scope).
"""
import datetime
import json
import pathlib
import sys
import urllib.error
import urllib.request

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
API_BASE = "https://codeberg.org/api/v1/repos/Tom_Cloyd/NutriMagnus"
BINARY_PATH = REPO_ROOT / "dist" / "nutrimagnus"
MANUAL_FILE = REPO_ROOT / "user-manual.md"
APPENDIX_K_HEADING = "### Appendix K: Recent program updates log"


def _version() -> str:
    sys.path.insert(0, str(REPO_ROOT))
    import version as _v
    return _v.VERSION


def _tag_for(version_str: str) -> str:
    # version.py uses "YYYY-MM-DD:HHMM" — ":" isn't a legal git ref character.
    return "v" + version_str.replace(":", "-")


def _release_notes_for_today() -> str:
    today_heading = "#### " + datetime.date.today().strftime("%B %-d")
    if not MANUAL_FILE.exists():
        return "Automated build from main."
    lines = MANUAL_FILE.read_text().splitlines()
    in_appendix = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == APPENDIX_K_HEADING:
            in_appendix = True
            continue
        if not in_appendix:
            continue
        if stripped == today_heading:
            body_lines = []
            for later in lines[i + 1:]:
                if later.startswith("#### ") or later.startswith("### "):
                    break
                body_lines.append(later)
            body = "\n".join(body_lines).strip()
            if body:
                return body
    return "Automated build from main."


def _api_request(path: str, token: str, *, method: str = "GET",
                  data: bytes | None = None, content_type: str | None = None) -> dict:
    req = urllib.request.Request(f"{API_BASE}{path}", method=method, data=data)
    req.add_header("Authorization", f"token {token}")
    if content_type:
        req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    import os
    token = os.environ.get("CODEBERG_TOKEN")
    if not token:
        print("ERROR: CODEBERG_TOKEN is not set.", file=sys.stderr)
        return 1
    if not BINARY_PATH.exists():
        print(f"ERROR: {BINARY_PATH} not found — build it first.", file=sys.stderr)
        return 1

    version_str = _version()
    tag = _tag_for(version_str)
    body = _release_notes_for_today()
    payload = json.dumps({
        "tag_name": tag,
        "name": f"NutriMagnus {tag}",
        "body": body,
        "draft": False,
        "prerelease": False,
    }).encode()

    try:
        release = _api_request("/releases", token, method="POST",
                                data=payload, content_type="application/json")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        if e.code == 409 or "already exist" in detail.lower():
            print(f"Release {tag} already exists — nothing to do (version.py wasn't bumped this push).")
            return 0
        print(f"ERROR creating release: {e.code} {detail}", file=sys.stderr)
        return 1

    release_id = release["id"]
    print(f"Created release {tag} (id {release_id}).")

    # Multipart upload for the binary asset — stdlib has no built-in
    # multipart/form-data encoder, so build the minimal body by hand.
    boundary = "----numa-release-boundary"
    binary_bytes = BINARY_PATH.read_bytes()
    body_parts = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="attachment"; filename="nutrimagnus"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + binary_bytes + f"\r\n--{boundary}--\r\n".encode()

    try:
        _api_request(
            f"/releases/{release_id}/assets", token, method="POST",
            data=body_parts, content_type=f"multipart/form-data; boundary={boundary}",
        )
    except urllib.error.HTTPError as e:
        print(f"ERROR uploading asset: {e.code} {e.read().decode(errors='replace')}", file=sys.stderr)
        return 1

    print(f"Uploaded nutrimagnus binary to release {tag}.")
    print(f"https://codeberg.org/Tom_Cloyd/NutriMagnus/releases/tag/{tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
