"""
test_food_id_tags.py — the rule that wherever a template shows a food's or
recipe's name, its code (U171477, R21 ...) shows with it: food_id_tag(),
food_id_short() or food_code() in the same table row / list item /
paragraph / heading (or right after a heading).

A static scan of web/templates, so a new page can't quietly break the rule.
Names that genuinely have no code are listed in EXEMPT, each with why.
"""
import pathlib
import re

TEMPLATES = pathlib.Path(__file__).resolve().parent.parent / "web" / "templates"

NAME = re.compile(r"\{\{ *([a-z_]+)\.(food_name|name)( *\|[^}]*)? *\}\}")
ID_HELPER = re.compile(r"food_id_tag|food_id_short|food_code|\.code\b")
OPEN = re.compile(r"<tr|<li|<p\b|<h[1-6]|<option")
CLOSE = re.compile(r"</tr>|</li>|</p>|</h[1-6]>|</option>")
# Variables holding something other than a food or recipe (meal, section,
# saved comparison, profile, nutrient group ...).
NOT_FOOD_VARS = {"section", "group", "s", "nm", "col", "sec", "t", "g", "source", "m", "meal", "sib"}

# (template, text on the line) -> reason it has no code.
EXEMPT = {
    ("_protein_per_meal.html", "{{ r.name }}"): "a meal's name, not a food's",
    ("food_cache_import_csv.html", "{{ f.name }}"): "import preview: not in the database yet, so no code",
    ("recipe_import_csv.html", "{{ r.name }}"): "import preview: not in the database yet, so no code",
    ("settings.html", "{{ ov.food_name }}"): "DIAAS overrides are keyed by food name, with no food ID stored",
}


def _violations() -> list[str]:
    found = []
    for path in sorted(TEMPLATES.glob("*.html")):
        lines = path.read_text().split("\n")
        for i, line in enumerate(lines):
            for m in NAME.finditer(line):
                if m.group(1) in NOT_FOOD_VARS:
                    continue
                # Page titles, breadcrumbs and the sidebar title repeat the
                # page heading, which carries the code; attributes aren't shown.
                if re.search(r"<title|block title|breadcrumb|sb-page-title|placeholder|confirm\(", line):
                    continue
                if re.search(r'(value|title|aria-label|alt)="[^"]*' + re.escape(m.group(0)), line):
                    continue
                if "urlencode" in line[m.start():m.end() + 15]:
                    continue
                if any(path.name == f and snippet in line for f, snippet in EXEMPT):
                    continue
                start = max([j for j in range(i, -1, -1) if OPEN.search(lines[j])] or [i])
                ends = [j for j in range(i, len(lines)) if CLOSE.search(lines[j])]
                end = (ends[0] if ends else i) + 1
                if not ID_HELPER.search("\n".join(lines[start:end + 1])):
                    found.append(f"{path.name}:{i + 1}: {line.strip()[:120]}")
    return found


def test_every_food_or_recipe_name_shows_its_code():
    assert _violations() == [], (
        "A food or recipe name with no code beside it. Add {{ food_id_tag(fdc_id, recipe_id) }} "
        "after the name (or a Code column with food_id_short), or, if it truly has no code, "
        "add it to EXEMPT with the reason:\n" + "\n".join(_violations()))
