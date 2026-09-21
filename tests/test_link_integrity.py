"""
Regression test for the weekly sweep's "stale internal links" item
(README-numa-documentation.md, Maintenance section) — the app-screens half
of it, added 2026-09-13 after that check turned out to have only ever
covered the manual's own links, never links from app templates to real
routes or manual anchors. A broken href here 404s for a real user with no
error anywhere in the normal test suite, since nothing exercises the link
itself, just the pages at both ends of it.

This caught a genuine dead link, present since the oxalate-reporting
feature's original commit: food_detail.html linked to
"/food/{fdc_id}/oxalate-link", a route that was never built (the
oxalate_link_save() function it would have called has no caller anywhere
in web/backend.py).

Docs: README-numa-documentation.md (Maintenance: Weekly sweep, item 8).
"""
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_TEMPLATES_DIR = _ROOT / "web" / "templates"

# href prefixes that aren't app routes and shouldn't be checked against them.
_EXEMPT_PREFIXES = ("http://", "https://", "mailto:", "#", "{{")


def _registered_routes() -> tuple[set[str], set[str]]:
    """Returns (exact/parametrized route patterns, static-mount prefixes)
    -- kept separate because a mount is a prefix match (anything under
    /static/...) while a route is a full-path match (a bare "/" route must
    NOT prefix-match every other path, the way a naive shared check would)."""
    text = (_ROOT / "web" / "backend.py").read_text(encoding="utf-8")
    routes = set(re.findall(r'@app\.(?:get|post)\("([^"]+)"', text))
    mounts = set(re.findall(r'app\.mount\("([^"]+)"', text))
    return routes, mounts


def _manual_anchors() -> set[str]:
    """Every real anchor id in the *built* manual -- covers both explicit
    {: #foo} tags and headings auto-slugged by the toc extension, which an
    {: #foo}-only check would falsely flag as missing."""
    html_path = _ROOT / "user-manual.html"
    assert html_path.exists(), "run scripts/build_manual.py before this test"
    return set(re.findall(r'id="([A-Za-z0-9\-_]+)"', html_path.read_text(encoding="utf-8")))


def _route_matches(path: str, routes: set[str], mounts: set[str]) -> bool:
    norm = re.sub(r"\{\{[^}]+\}\}", "{x}", path)
    if any(norm.startswith(mount.rstrip("/") + "/") or norm == mount for mount in mounts):
        return True
    for route in routes:
        pattern = re.fullmatch(re.sub(r"\{[^/}]+\}", "[^/]+", route), norm)
        if pattern:
            return True
    return False


def test_app_template_links_resolve_to_real_routes_and_manual_anchors():
    routes, mounts = _registered_routes()
    manual_anchors = _manual_anchors()

    broken: list[str] = []
    for template in _TEMPLATES_DIR.rglob("*.html"):
        text = template.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r'href="([^"]+)"', text):
            if not href.startswith("/") or href.startswith(_EXEMPT_PREFIXES):
                continue
            path, _, frag = href.partition("#")
            path = path.split("?", 1)[0]
            if path in ("/manual", "/user-manual"):
                if frag and frag not in manual_anchors:
                    broken.append(f"{template.relative_to(_ROOT)}: {href} (no such manual anchor)")
                continue
            if not _route_matches(path, routes, mounts):
                broken.append(f"{template.relative_to(_ROOT)}: {href} (no matching route)")

    assert not broken, "Dead links found in app templates:\n" + "\n".join(broken)


def test_manual_internal_links_resolve_to_real_anchors():
    """The manual-links half of item 8 — previously a manual-only weekly-sweep
    check (README-numa-documentation.md), so a broken #anchor reference inside
    user-manual.md itself could go unnoticed for weeks; caught one, #web-shortcuts,
    on the 2026-09-20 sweep (two changelog entries referenced it, but the actual
    keyboard-shortcuts passage in Part 1 Section B had never carried that id)."""
    manual_anchors = _manual_anchors()
    md_text = (_ROOT / "user-manual.md").read_text(encoding="utf-8")
    refs = set(re.findall(r"\]\(#([A-Za-z0-9_\-]+)\)", md_text))
    missing = sorted(refs - manual_anchors)
    assert not missing, "user-manual.md links to nonexistent anchors:\n" + "\n".join(missing)
