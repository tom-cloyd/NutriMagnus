"""Every navigation-bar destination has a section in the User Manual's
Part 4 ("Menu by menu"), the manual's functional reference.

Docs: user-manual.md, Part 4 — Menu by menu (#part-3-using-numa);
numa-manual-plan.md section 6 step 6.

A new menu item fails here until it's added to NAV_ANCHORS below and
given a section in Part 4.
"""
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

# nav href in web/templates/base.html -> the manual anchor documenting it
NAV_ANCHORS = {
    "/": "home-page-tour",
    "/food/search": "search-web",
    "/food/analyze-portion": "analyze-portion",
    "/food/analyze-recipe-portion": "analyze-portion",
    "/food/convert": "convert",
    "/food/cache": "food-cache-web",
    "/pantry": "pantry-web",
    "/food/custom-profiles": "custom-foods",
    "/food/annotate": "annotate-web",
    "/food/cache/db-check": "checking-your-data",
    "/recipes": "recipes-menu-web",
    "/recipe/import-csv": "recipe-import-web",
    "/compare": "compare-web",
    "/meals": "meals-menu-web",
    "/summary": "daily-summary",
    "/analysis/food-use": "fooduse",
    "/analysis/food-use-recipes": "fooduse-recipes",
    "/analysis/whatif": "whatif",
    "/analysis/whatif-recipes": "whatif-recipes",
    "/settings": "settings",
    "/manual": "manual-menu",
}
# links in base.html that aren't menu items
_NOT_MENU = {"/disclaimer", "/favicon.ico"}


def _nav_hrefs() -> set[str]:
    html = (_ROOT / "web" / "templates" / "base.html").read_text(encoding="utf-8")
    hrefs = set(re.findall(r'href="(/[^"#?]*)"', html))
    return {h for h in hrefs if not h.startswith("/static/") and h not in _NOT_MENU}


def _part4_anchors() -> set[str]:
    md = (_ROOT / "user-manual.md").read_text(encoding="utf-8")
    start = md.index("## Part 4 — Menu by menu")
    end = md.index("\n## Part 5", start)
    return set(re.findall(r"\{:\s*#([A-Za-z0-9_-]+)\}", md[start:end]))


def test_every_nav_link_is_mapped():
    unmapped = sorted(_nav_hrefs() - NAV_ANCHORS.keys())
    assert not unmapped, ("menu items with no manual section listed in NAV_ANCHORS "
                          "(document them in Part 4, then add them): " + ", ".join(unmapped))


def test_every_menu_item_has_a_part4_section():
    anchors = _part4_anchors()
    missing = sorted(f"{href} -> #{a}" for href, a in NAV_ANCHORS.items() if a not in anchors)
    assert not missing, "menu items whose manual section isn't in Part 4: " + ", ".join(missing)
