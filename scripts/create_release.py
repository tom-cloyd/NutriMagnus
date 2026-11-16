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

Release notes (the GitHub release page) are just the SUMMARY paragraph of the
Version overview in user-manual.md's "What's new" section (#updates-log),
the part between the "<!-- Insert new updates below here -->" marker and the
next "#### Release ... summary" heading, followed by one line pointing to
the full list in the manual (since 2026-11-15; before that the whole stretch,
overview and every numbered bullet, was published). No SUMMARY there: the
release stops with an error instead of publishing an empty page.

On success, that running heading is renamed in place to "#### Release <tag>
summary", so the summary already written for the pending work simply becomes
that release's summary; the entries below it are never moved or rewritten,
and older, already-released entries stay untouched (summary-heading scheme
adopted 2026-09-23, replacing a "#### Release <tag> boundary" heading that
was inserted *below* the entries and carried no summary of its own).

"(dated details below)" is appended to the renamed heading only when dated
entry sections actually follow it, since a release whose entries have already
been pruned has no details left to point at.

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
# Written fresh by _write_starter_manifest() on every run, then uploaded, so
# the home page of an older install can preview this release's starter
# changes (numa_app/services/update_check.py fetches it by this name).
STARTER_MANIFEST_PATH = REPO_ROOT / "dist" / "starter_manifest.json"
VERSION_FILE = REPO_ROOT / "version.py"
MANUAL_FILE = REPO_ROOT / "user-manual.md"
# The dated, detailed entries (moved out of the manual 2026-11-14). A release
# adds a separator heading under its marker; nothing else here reads it.
DETAILS_FILE = REPO_ROOT / "docs" / "updates-log-details.md"
CHANGELOG_HEADING = "## What's new {: #updates-log}"
INSERT_MARKER = "<!-- Insert new updates below here -->"
_SUMMARY_RE = re.compile(r'^#### Release .+ summary\b.*$')
# The heading in the manual reads "#### Next release summary to this point
# (dated details below)". Only its stable opening words are matched, so
# re-wording the tail (or dropping the parenthetical) can't silently orphan it
# here -- a mismatch would make a release quietly treat the whole log as
# pending, which is a bad failure to have hinge on heading prose.
_NEXT_SUMMARY_RE = re.compile(r'^#### Next release summary\b.*$')
# Dated entry sections: "#### Sep 22 updates", "##### September 21 program updates".
_DATED_SECTION_RE = re.compile(r'^#{4,5} .+ updates\s*$')
_DETAILS_SUFFIX = " (dated details below)"
_RELEASE_VERSION_RE = re.compile(r'^(RELEASE_VERSION = ")(.*?)(-(?:rc|beta|alpha)\.)(\d+)("\s*)$', re.M)

# (asset name, file path, content type) — every release asset besides the notes.
_ASSETS = [
    ("nutrimagnus", BINARY_PATH, "application/octet-stream"),
    ("nutrimagnus.png", REPO_ROOT / "web" / "static" / "icon-256.png", "image/png"),
    ("install-linux.sh", REPO_ROOT / "scripts" / "install-linux.sh", "text/x-sh"),
    ("starter_manifest.json", STARTER_MANIFEST_PATH, "application/json"),
]


def _write_starter_manifest() -> None:
    """Summarize the starter set being released (one content hash per item;
    see demo_data.starter_manifest()) into STARTER_MANIFEST_PATH."""
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from numa_app.services import demo_data
    STARTER_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    STARTER_MANIFEST_PATH.write_text(json.dumps(demo_data.starter_manifest(), indent=2) + "\n")


def _version() -> str:
    sys.path.insert(0, str(REPO_ROOT))
    import version as _v
    return _v.VERSION


def _tag_for(version_str: str) -> str:
    # version.py uses "YYYY-MM-DD:HHMM" — ":" isn't a legal git ref character.
    return "v" + version_str.replace(":", "-")


def _pending_range(lines: list[str]) -> tuple[int | None, int | None]:
    """Find the marker line and the end of the "pending" (not yet in a
    release) stretch right after it: the index of the next release-summary
    heading, or the next "## "/"### " heading if no release summary exists
    yet (e.g. before the first-ever release cut), or end-of-file otherwise."""
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
        if _SUMMARY_RE.match(stripped) or stripped.startswith(("## ", "### ")):
            return marker_idx, i
    if marker_idx is None:
        return None, None
    return marker_idx, len(lines)


FULL_LIST_LINE = "See full list of changes in the User Manual's 'What's New' section"
_SUMMARY_LABEL_RE = re.compile(r"^SUMMARY:\s*")


def _release_summary() -> str | None:
    """The SUMMARY paragraph of the Version overview in the manual's
    unreleased What's new section, without its label; None if there isn't
    one. Also accepts the older one-line overview, where SUMMARY and DETAILS
    shared a line."""
    if not MANUAL_FILE.exists():
        return None
    lines = MANUAL_FILE.read_text().splitlines()
    marker_idx, end_idx = _pending_range(lines)
    if marker_idx is None:
        return None
    for line in lines[marker_idx + 1:end_idx]:
        text = re.sub(r"^Version overview:\s*", "", line.strip())
        if _SUMMARY_LABEL_RE.match(text):
            text = _SUMMARY_LABEL_RE.sub("", text).split("DETAILS:", 1)[0].strip()
            return text or None
    return None


def _release_notes() -> str | None:
    """The GitHub release page text: just the SUMMARY, then a pointer to the
    full list in the manual (decided 2026-11-15: the whole overview and every
    numbered bullet was more than anyone deciding whether to update reads).
    None when the manual has no SUMMARY, so main() can refuse to publish."""
    summary = _release_summary()
    if not summary:
        return None
    return f"{summary}\n\n{FULL_LIST_LINE}"


def _roll_release_summary(tag: str) -> bool:
    """Rename the running "#### Next release summary to this point" heading
    to "#### Release <tag> summary", so the summary already written for the
    pending entries becomes this release's summary in place -- the entries
    below it are never rewritten or relocated. If no running heading exists
    (nobody started one since the last release), the same heading is inserted
    directly under the marker instead, which lands it in the same position."""
    if not MANUAL_FILE.exists():
        return False
    lines = MANUAL_FILE.read_text().splitlines(keepends=True)
    bare = [l.rstrip("\n") for l in lines]
    marker_idx, end_idx = _pending_range(bare)
    if marker_idx is None:
        return False
    has_details = any(_DATED_SECTION_RE.match(l.strip()) for l in bare[marker_idx + 1:end_idx])
    heading = f"#### Release {tag} summary{_DETAILS_SUFFIX if has_details else ''}\n"
    for i in range(marker_idx + 1, end_idx):
        if _NEXT_SUMMARY_RE.match(bare[i].strip()):
            lines[i] = heading
            break
    else:
        lines[marker_idx + 1:marker_idx + 1] = ["\n", heading]
    MANUAL_FILE.write_text("".join(lines))
    _mark_release_in_details(tag)
    return True


def _mark_release_in_details(tag: str) -> None:
    """Put a "## Release <tag>" heading under docs/updates-log-details.md's
    marker, so the dated entries written since the last release sit under
    the release that shipped them."""
    if not DETAILS_FILE.exists():
        return
    text = DETAILS_FILE.read_text()
    if INSERT_MARKER not in text:
        return
    heading = f"## Release {tag} — dated entries released in it"
    DETAILS_FILE.write_text(text.replace(INSERT_MARKER, f"{INSERT_MARKER}\n\n{heading}", 1))


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


def _manual_links_ok() -> bool:
    """Rebuild user-manual.html and run the link-integrity tests against it.

    A release ships the manual, so a broken #anchor link (or a template link
    to a route that doesn't exist) stops the release instead of shipping. The
    release workflow also runs the full suite first; this covers a manual
    run of this script.
    """
    import subprocess
    root = pathlib.Path(__file__).resolve().parent.parent
    build = subprocess.run([sys.executable, str(root / "scripts" / "build_manual.py")], cwd=root)
    if build.returncode != 0:
        print("ERROR: scripts/build_manual.py failed — fix the manual, then try again.", file=sys.stderr)
        return False
    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_link_integrity.py"], cwd=root)
    if tests.returncode != 0:
        print("ERROR: the manual has broken links (see the test output above) — "
              "fix them, then run this script again. Nothing was released.", file=sys.stderr)
        return False
    return True


def main() -> int:
    import os
    token = "".join((os.environ.get("GITHUB_TOKEN") or "").split())   # stray \r/\n/spaces from a paste
    if not token:
        print("ERROR: GITHUB_TOKEN is not set.", file=sys.stderr)
        return 1
    if not _manual_links_ok():
        return 1
    _write_starter_manifest()
    for name, path, _ in _ASSETS:
        if not path.exists():
            print(f"ERROR: {path} not found (needed for asset {name!r}) — build it first.", file=sys.stderr)
            return 1

    version_str = _version()
    tag = _tag_for(version_str)
    body = _release_notes()
    if not body:
        print("ERROR: no SUMMARY in the manual's What's new section. Copy version.py's "
              "NEW_VERSION_NOTE into it as the Version overview (docs/claude/changelog.md), "
              "then try again.", file=sys.stderr)
        return 1
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

    if _roll_release_summary(tag):
        print(f"Rolled the manual's Recent program updates log summary heading to {tag}.")
    else:
        print("WARNING: could not find the changelog marker in user-manual.md — summary heading not rolled.",
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
