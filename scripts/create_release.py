#!/usr/bin/env python3
"""
create_release.py — create a GitHub release for the current version and
upload the freshly built Linux binary, its icon, and the one-file installer
(scripts/install-linux.sh) as release assets. Run from the repo root after
`pyinstaller nutrimagnus.spec` (packages web/launcher.py) has produced
dist/nutrimagnus. Used by .github/workflows/release.yml on manual dispatch;
safe to run manually too.

install-linux.sh fetches its assets from releases/latest/download/<name>, so
the exact names below (nutrimagnus, nutrimagnus.png) must stay in sync with
that script.

Release notes are pulled from user-manual.md's Appendix A ("Recent program
updates log") section matching today's date (#### Month Day), falling back
to a generic message if that section doesn't exist yet (e.g. no manual
changes were logged today).

Requires GITHUB_TOKEN in the environment (inside GitHub Actions this is the
automatic per-run token, granted `contents: write` by the workflow; for
manual/local use, a personal access token with repo write scope).
"""
import datetime
import json
import pathlib
import sys
import urllib.error
import urllib.request

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
GITHUB_OWNER = "tom-cloyd"
GITHUB_REPO = "NutriMagnus"
API_BASE = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
UPLOADS_BASE = f"https://uploads.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
BINARY_PATH = REPO_ROOT / "dist" / "nutrimagnus"
MANUAL_FILE = REPO_ROOT / "user-manual.md"
CHANGELOG_HEADING = "### A. Recent program updates log"

# (asset name, file path, content type) — every release asset besides the notes.
_ASSETS = [
    ("nutrimagnus", BINARY_PATH, "application/octet-stream"),
    ("nutrimagnus.png", REPO_ROOT / "web" / "static" / "icon-256.png", "image/png"),
    ("install-linux.sh", REPO_ROOT / "scripts" / "install-linux.sh", "text/x-sh"),
]


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
        if stripped == CHANGELOG_HEADING:
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


def _api_request(url: str, token: str, *, method: str = "GET",
                  data: bytes | None = None, content_type: str | None = None) -> dict:
    req = urllib.request.Request(url, method=method, data=data)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if content_type:
        req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    import os
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN is not set.", file=sys.stderr)
        return 1
    for name, path, _ in _ASSETS:
        if not path.exists():
            print(f"ERROR: {path} not found (needed for asset {name!r}) — build it first.", file=sys.stderr)
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
        release = _api_request(f"{API_BASE}/releases", token, method="POST",
                                data=payload, content_type="application/json")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        if e.code == 422 and "already_exists" in detail:
            print(f"Release {tag} already exists — nothing to do (version.py wasn't bumped since last release).")
            return 0
        print(f"ERROR creating release: {e.code} {detail}", file=sys.stderr)
        return 1

    release_id = release["id"]
    print(f"Created release {tag} (id {release_id}).")

    # GitHub's asset-upload endpoint takes the raw file bytes as the body
    # (not multipart/form-data like Gitea/Codeberg) with the filename as a
    # query parameter, and lives on a separate uploads.github.com host.
    for name, path, content_type in _ASSETS:
        try:
            _api_request(
                f"{UPLOADS_BASE}/releases/{release_id}/assets?name={name}",
                token, method="POST",
                data=path.read_bytes(), content_type=content_type,
            )
        except urllib.error.HTTPError as e:
            print(f"ERROR uploading asset {name!r}: {e.code} {e.read().decode(errors='replace')}", file=sys.stderr)
            return 1
        print(f"Uploaded {name} to release {tag}.")
    print(f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/tag/{tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
