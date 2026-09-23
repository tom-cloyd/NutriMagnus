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
updates log") section: everything between the "<!-- Insert new updates below
here -->" marker and the next "#### Release ... boundary" heading (or the end
of the appendix, if no release has ever been cut) — falling back to a generic
message if that stretch is empty. On success, a new "#### Release <tag>
boundary" heading is inserted right there, directly below those entries, so
they read as belonging to this release without moving or rewriting them;
older, already-released entries below are untouched (decided 2026-09-21,
replacing an earlier "#### Next release" heading scheme this same script had
drifted out of sync with).

This is also the one place RELEASE_VERSION's -rc.N/-beta.N/-alpha.N counter
in version.py advances (decided 2026-09-21) — scripts/bump_version.py only
touches the VERSION timestamp now, so the counter means "how many releases",
not "how many dev sessions".

Requires GITHUB_TOKEN in the environment (inside GitHub Actions this is the
automatic per-run token, granted `contents: write` by the workflow; for
manual/local use, a personal access token with repo write scope).
"""
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
GITHUB_OWNER = "tom-cloyd"
GITHUB_REPO = "NutriMagnus"
API_BASE = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
UPLOADS_BASE = f"https://uploads.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
BINARY_PATH = REPO_ROOT / "dist" / "nutrimagnus"
VERSION_FILE = REPO_ROOT / "version.py"
MANUAL_FILE = REPO_ROOT / "user-manual.md"
CHANGELOG_HEADING = "### A. Recent program updates log"
INSERT_MARKER = "<!-- Insert new updates below here -->"
_BOUNDARY_RE = re.compile(r'^#### Release .* boundary\s*$')
_RELEASE_VERSION_RE = re.compile(r'^(RELEASE_VERSION = ")(.*?)(-(?:rc|beta|alpha)\.)(\d+)("\s*)$', re.M)

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


def _pending_range(lines: list[str]) -> tuple[int | None, int | None]:
    """Find the marker line and the end of the "pending" (not yet in a
    release) stretch right after it: the index of the next release-boundary
    heading, or the next "### " appendix heading if no boundary exists yet
    (e.g. before the first-ever release cut), or end-of-file otherwise."""
    marker_idx = None
    in_appendix = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == CHANGELOG_HEADING:
            in_appendix = True
            continue
        if not in_appendix:
            continue
        if marker_idx is None:
            if stripped == INSERT_MARKER:
                marker_idx = i
            continue
        if _BOUNDARY_RE.match(stripped) or stripped.startswith("### "):
            return marker_idx, i
    if marker_idx is None:
        return None, None
    return marker_idx, len(lines)


def _release_notes() -> str:
    if not MANUAL_FILE.exists():
        return "Automated build from main."
    lines = MANUAL_FILE.read_text().splitlines()
    marker_idx, end_idx = _pending_range(lines)
    if marker_idx is None:
        return "Automated build from main."
    body = "\n".join(lines[marker_idx + 1:end_idx]).strip()
    return body or "Automated build from main."


def _roll_release_boundary(tag: str) -> bool:
    """Insert a new "#### Release <tag> boundary" heading directly below the
    pending entries under the marker -- the entries themselves are never
    rewritten or relocated, they just end up sitting above the new heading,
    which is what marks them as belonging to this release."""
    if not MANUAL_FILE.exists():
        return False
    text = MANUAL_FILE.read_text()
    lines = text.splitlines(keepends=True)
    marker_idx, end_idx = _pending_range([l.rstrip("\n") for l in lines])
    if marker_idx is None:
        return False
    insertion = [f"#### Release {tag} boundary\n", "\n"]
    new_lines = lines[:end_idx] + insertion + lines[end_idx:]
    MANUAL_FILE.write_text("".join(new_lines))
    return True


def _bump_release_version() -> str | None:
    """Increment RELEASE_VERSION's -rc.N/-beta.N/-alpha.N counter in
    version.py. Returns the new RELEASE_VERSION string, or None if the line
    has no such suffix to bump (e.g. it's already a plain final release like
    1.0.0 -- edit version.py by hand for that case)."""
    if not VERSION_FILE.exists():
        return None
    text = VERSION_FILE.read_text()

    def _incr(m: re.Match) -> str:
        return f"{m.group(1)}{m.group(2)}{m.group(3)}{int(m.group(4)) + 1}{m.group(5)}"

    new_text = _RELEASE_VERSION_RE.sub(_incr, text, count=1)
    if new_text == text:
        return None
    VERSION_FILE.write_text(new_text)
    return re.search(r'RELEASE_VERSION = "([^"]*)"', new_text).group(1)


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
    body = _release_notes()
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

    if _roll_release_boundary(tag):
        print(f"Rolled the manual's Recent program updates log boundary to {tag}.")
    else:
        print("WARNING: could not find the changelog marker in user-manual.md — boundary not rolled.",
              file=sys.stderr)

    new_release_version = _bump_release_version()
    if new_release_version:
        print(f"Bumped RELEASE_VERSION to {new_release_version}.")
    else:
        print("NOTE: RELEASE_VERSION has no -rc./-beta./-alpha.N suffix to bump "
              "(e.g. it may already be a plain final release) -- edit version.py by hand if needed.")

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
