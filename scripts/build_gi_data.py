#!/usr/bin/env python3
"""
build_gi_data.py — regenerate gi_data.json from the Atkinson et al. 2021
"International tables of glycemic index and glycemic load values" online
supplemental tables (see user-manual.md footnote 8).

The supplement ships as two PDFs, split by METHODOLOGY QUALITY — not by
subject population, which is the trap when coming from the 2008 edition:

  Supplemental Table 1 — studies consistent with ISO 26642:2010 (food
                         numbers 1-2091)
  Supplemental Table 2 — method deviations from that standard, or values
                         showing wide variability (SEM>10 for low GI values,
                         SEM>15 for medium/high) (food numbers 2092-4018)

Table 2's deviations are things like fewer than 10 subjects, an available
carbohydrate portion other than 25/50 g, or an unrepeated reference food, so
most of its rows were still measured in normal-glucose-tolerance subjects.
Population therefore comes from each row's own "Subjects (type & number)"
cell, and ISO compliance is carried separately as `iso`. Deriving population
from which PDF a row came from — the way the 2008 A1/A2 split worked — would
mislabel roughly 1,250 normal-tolerance rows as impaired.

Fetch both PDFs from the publisher's "Supplementary data" link on the article
page (https://doi.org/10.1093/ajcn/nqab233) for provenance; like CoFID/AFCD/
CIQUAL this is a static download a developer grabs by hand, not a live API.

Licence, and why this is a script rather than shipped data: the 2021 article is
published under the Elsevier user licence, which expressly permits "access,
download, copy, translate, text and data mine" for non-commercial purposes but
forbids redistribution. So each user mines their own copy under their own access
rights, and NuMa ships this parser plus the Creative Commons 2008 table as its
bundled baseline. The output, gi_data_local.json, is gitignored and is not
bundled into packaged builds. Do not commit it or ship it.

Usage:
    python scripts/build_gi_data.py path/to/supp_table_1.pdf path/to/supp_table_2.pdf

Legacy tier: rows from the 2008 edition are NOT re-parsed from their own PDFs
(see scripts/build_gi_data_2008.py, kept only for that eventuality). They are
carried forward out of the bundled gi_data.json, and every 2008 row whose
name does not match a 2021 row is appended tagged `edition: 2008`. That is a
deliberate OVER-INCLUSION rule: 2021 rewrote many food descriptions and the
per-edition `ref` numbers cannot join the two, so no name match can tell a
genuinely-dropped food from a reworded one. A false "only in 2008" costs a
few near-duplicate Annotate matches; dropping a real food costs coverage numa
already ships. 2008 rows carry `year: null` — that extraction never captured
a year of test, and the edition year is not a measurement date.

Expect 4017 entries from 4018 printed food numbers. Number 4012 is printed
against the "Tamales" category heading in Supplemental Table 2 rather than
against a food, so it has no GI value of its own and is reported as a skip on
every run; that one is the source's quirk, not a parse failure. Two further
rows carry a misprinted number (2211 appears as "2111", 3536 as "2536"), which
is why printed numbers are not unique and are not treated as a key.

Extraction approach: `pdftotext -bbox-layout`, not `-layout`. Fixed-width text
cannot be parsed reliably here because a food's name wraps onto lines BOTH
ABOVE AND BELOW the line carrying its food number (the number is vertically
centred in its row), so no line-ordering rule recovers the name. Word
coordinates make row extent exact instead:

  * The food-number column is a narrow left column of its own, so every row
    is anchored by a number at a known y.
  * A row's vertical band runs to the midpoints between its number and the
    numbers above and below it.
  * Within a band, the name is the contiguous run of name-column lines whose
    inter-line gaps are at most _INTRA_ROW_GAP and which includes the line
    nearest the number. Category headers ("BAKERY PRODUCTS", "Cakes") and the
    standardized-portion notes beneath them share the name column's exact left
    margin, so indentation cannot separate them — but they sit ~14pt from
    their neighbours where wrapped name lines sit ~5-11pt apart, and no food
    number falls inside their run.

That removes the 2008 parser's "short, no digits or commas => header"
heuristic, and with it that edition's known-imperfect category tagging.

Serve size / available carbohydrate / the table's own GL are deliberately NOT
captured. numa computes GL live from a food's own cached carbohydrate content
and the amount consumed (numa_app.services.glycemic_load.compute_glycemic_load);
the published GL is explicitly a nominal figure derived from a standardized
per-category carbohydrate portion and described in the source as "intended as
a guide only", so the live calculation is strictly better for a specific
cached food.

Docs: README-numa-documentation.md, Architecture: "gi_lookup.py — glycemic index table lookup"
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

# Written beside the module, NOT over the bundled table. The 2021 edition's
# licence permits text and data mining but forbids redistribution, so the result
# must stay local to whoever built it: gi_data_local.json is gitignored and is
# not in nutrimagnus.spec's datas. gi_lookup.py prefers it when present.
OUTPUT = Path(__file__).parent.parent / "gi_data_local.json"
BASELINE = Path(__file__).parent.parent / "gi_data.json"

# Words on the same printed line can differ slightly in baseline (superscripts),
# and wrapped name lines sit closer together than separate table blocks do.
_SAME_LINE_TOL = 2.5
_INTRA_ROW_GAP = 12.5
# How far a food number's baseline may sit outside its name block's y-range.
_NUMBER_TOL = 7.0

_WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>'
)
_NUMBER_RE = re.compile(r'^\d{1,4}$')
_YEAR_RE = re.compile(r'\b((?:19|20)\d{2})\s*\*?')
_GI_SEM_RE = re.compile(r'(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)')
_SUBJ_RE = re.compile(
    r'\b(Normal|Type 1(?: diabetes)?|Type 2(?: diabetes)?|T1DM|T2DM|IGT|GDM'
    r'|Gestational(?: diabetes)?|Impaired\w*|Mixed|NS)\b[,\s]*(\d+)?'
)
# Shortest normalized name allowed to match a 2021 name by containment; below
# this a fragment like "peas" would swallow unrelated entries.
_MIN_CONTAINMENT_LEN = 12
# Similarity at which a reworded 2008 name counts as the same food as a 2021 one.
_MATCH_RATIO = 0.85
# Sanity bound on a GI read from its column; the highest real value here is 132.
_MAX_GI = 200.0
_PORTION_NOTE_RE = re.compile(r'available carbohydrate portion', re.I)
# Running citation / page furniture that sits in the name column's x-range and
# would otherwise be read as a category header.
_JUNK_RE = re.compile(
    r'Online Supplemental Material|Brand-Miller|Atkinson FS'
    r'|International tables of glycemic|^Supplemental Table \d|^\d{1,3}$'
)
_MAJOR_CAT_RE = re.compile(r'^[A-Z][A-Z &,\'\-/()0-9]{2,}$')
# Words unique to the column-header block, used to find where table content
# starts. Everyday words the header also uses ("food", "of", "and") are left
# out deliberately: they occur throughout the food names too, and including
# them pushed the detected header bottom to the foot of the page.
_HEADER_WORDS = {
    "GI2", "SEM", "Subjects", "Timepoints", "portion3", "production",
    "collection", "method4", "number)", "(Glu", "100)", "portion)", "test1",
    "(Test", "(min)", "Ref.", "Item", "Avail",
}
# How far above or below the "Food Number and Item" line the header's own
# wrapped heading lines reach.
_HEADER_BLOCK_SPAN = 30.0

_IMPAIRED_SUBJECTS = {
    "type 1", "type 1 diabetes", "type 2", "type 2 diabetes", "t1dm", "t2dm",
    "igt", "gdm", "gestational", "gestational diabetes", "impaired",
    "impaired glucose tolerance", "mixed",
}


class _Line:
    """One printed line's worth of words, with its x positions kept so any
    column's cell can be sliced back out of it."""

    def __init__(self, y: float):
        self.y = y
        self.words: list[tuple[float, str]] = []

    def text(self, x_lo: float = 0.0, x_hi: float = 1e9) -> str:
        parts = [w for x, w in sorted(self.words) if x_lo <= x < x_hi]
        return " ".join(parts).strip()


def _page_words(page_xml: str) -> list[tuple[float, float, str]]:
    words = []
    for x0, y0, _x1, _y1, text in _WORD_RE.findall(page_xml):
        text = (text.replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&quot;", '"')
                    .replace("&apos;", "'"))
        if text.strip():
            words.append((float(x0), float(y0), text.strip()))
    return words


def _group_lines(words: list[tuple[float, float, str]]) -> list[_Line]:
    lines: list[_Line] = []
    for x, y, text in sorted(words, key=lambda w: (w[1], w[0])):
        if lines and abs(y - lines[-1].y) <= _SAME_LINE_TOL:
            lines[-1].words.append((x, text))
        else:
            line = _Line(y)
            line.words.append((x, text))
            lines.append(line)
    return lines


def _page_geometry(lines: list[_Line]) -> dict[str, float] | None:
    """Per-page x windows for each column numa reads, plus the header bottom.

    Every cell is read from its own column window rather than by position in a
    reconstructed line, because a row's wrapped lines interleave fragments of
    several columns: a timepoints cell spilling "270,300" onto its own line
    sits earlier in the text than the row's real GI value, and a regex over
    the joined tail picks up whichever number comes first.

    Both tables print this header block on every data page but with different
    column sets (Table 2 adds "Rep ref food") and slightly different offsets,
    so the windows are recomputed per page rather than assumed.
    """
    # Anchor words are taken only from the header block, located by the line
    # carrying "Food Number and Item". Scanning the whole page picks up body
    # text that happens to reuse a heading word — the standardized-portion note
    # ends "...to determine the nominal GL for each item in this category.",
    # whose bare "GL" sits left of the real GL column and inverts its window.
    item_y = next((l.y for l in lines
                   for _x, w in l.words if w == "Item"), None)
    if item_y is None:
        return None

    header_bottom = 0.0
    cols: dict[str, float] = {}
    anchors = {
        "country": ("Country", "production"),
        "year": ("Year", "test1"),
        "gi": ("GI2", "SEM", "(Glu", "100)"),
        "gl": ("GL",),
        "subjects": ("Subjects", "number)"),
        "avail": ("Avail", "carb", "(Test", "portion)"),
        "ref": ("Ref.",),
    }
    for line in lines:
        if abs(line.y - item_y) > _HEADER_BLOCK_SPAN:
            continue
        for x, word in line.words:
            if word in _HEADER_WORDS:
                header_bottom = max(header_bottom, line.y)
            if x <= 100:
                continue
            for key, words in anchors.items():
                if word in words:
                    cols[key] = min(cols.get(key, x), x)
    if "country" not in cols:
        return None

    geom = {"header_bottom": header_bottom, "name_end": cols["country"] - 4.0}
    # Each window runs from its own header anchor to the next column's, with a
    # small left margin because a cell is centred under its heading.
    order = ["country", "year", "gi", "gl", "subjects", "avail"]
    for i, key in enumerate(order):
        if key not in cols:
            continue
        nxt = next((cols[k] for k in order[i + 1:] if k in cols), None)
        geom[f"{key}_x0"] = cols[key] - 8.0
        end = (nxt - 8.0) if nxt else cols[key] + 60.0
        # A column set that came out inverted would silently read an empty
        # cell, so fall back to a nominal width instead.
        geom[f"{key}_end"] = end if end > cols[key] else cols[key] + 60.0
    geom["ref_x0"] = cols.get("ref", 1e8) - 10.0
    return geom


def _name_column_x0(starts: list[float]) -> float:
    """Boundary between the food-number column and the name column.

    Measured once per PDF, not per page: the margin is constant within a table
    (~76pt in Supplemental Table 1, ~62pt in Table 2) but a single page is too
    small a sample, because on a page whose rows all fit one line the name is
    never a line's leftmost word and its column all but vanishes. Line-start
    x values fall into two clusters — numbers and names — and the boundary is
    the midpoint between them, which both tolerates the offset difference and
    leaves no room for a number to be read as name text.
    """
    clusters: dict[float, int] = {}
    for x in starts:
        key = next((k for k in clusters if abs(k - x) < 3), x)
        clusters[key] = clusters.get(key, 0) + 1
    ranked = sorted(clusters.items(), key=lambda kv: -kv[1])[:2]
    if len(ranked) < 2:
        return (ranked[0][0] - 3.0) if ranked else 62.0
    lo, hi = sorted(k for k, _n in ranked)
    return (lo + hi) / 2


def _parse_pdf(path: Path, iso: bool) -> tuple[list[dict], list[str]]:
    xml = subprocess.run(
        ["pdftotext", "-bbox-layout", str(path), "-"],
        capture_output=True, text=True, check=True,
    ).stdout

    items: list[dict] = []
    warnings: list[str] = []
    major: str | None = None
    minor: str | None = None

    # Pass 1: page geometry, and the line-start positions the name column's
    # left edge is measured from across the whole document.
    pages: list[tuple[int, list[_Line], dict[str, float]]] = []
    starts: list[float] = []
    for page_no, page_xml in enumerate(re.split(r"<page ", xml)[1:], start=1):
        lines = _group_lines(_page_words(page_xml))
        geom = _page_geometry(lines)
        if geom is None:
            continue                      # cover page / footnotes page
        pages.append((page_no, lines, geom))
        for line in lines:
            if line.y <= geom["header_bottom"] + 1:
                continue
            xs = [x for x, _w in sorted(line.words) if x < geom["country_x0"]]
            if xs:
                starts.append(xs[0])
    name_x0 = _name_column_x0(starts)

    for page_no, lines, geom in pages:
        name_end = geom["name_end"]
        header_bottom = geom["header_bottom"]

        body = [l for l in lines if l.y > header_bottom + 1]

        # Every row is anchored by its food number, alone in a narrow column
        # left of the names.
        candidates: list[tuple[float, int, float]] = []
        for line in body:
            for x, word in line.words:
                if x < name_x0 and _NUMBER_RE.match(word):
                    candidates.append((line.y, int(word), x))
        numbers = _food_numbers(candidates)
        if not numbers:
            continue

        # A row's band reaches to the midpoints with the rows either side.
        bands: list[tuple[float, float, float, int]] = []
        for i, (y, num) in enumerate(numbers):
            top = header_bottom if i == 0 else (numbers[i - 1][0] + y) / 2
            bottom = 1e9 if i == len(numbers) - 1 else (numbers[i + 1][0] + y) / 2
            bands.append((top, bottom, y, num))

        for top, bottom, num_y, num in bands:
            in_band = [l for l in body if top < l.y <= bottom]
            # The line carrying the food number usually has NO name text of its
            # own (the name wraps above and below it) but holds every other
            # cell, so the tail must be read from the whole band, while only
            # name-bearing lines take part in working out where the name runs.
            named = [l for l in in_band if l.text(name_x0, name_end)
                     and not _JUNK_RE.search(l.text(name_x0, name_end))]
            name_lines, header_lines = _split_name_and_headers(named, num_y)
            for text in (l.text(name_x0, name_end) for l in header_lines):
                if _PORTION_NOTE_RE.search(text):
                    continue
                if _MAJOR_CAT_RE.match(text):
                    major, minor = text, None
                else:
                    minor = text

            # Category headers and the standardized-portion notes beneath them
            # run clear across the table, so their text also sits in the
            # country column and in the tail; drop those lines entirely before
            # reading any cell from the band.
            data_lines = [l for l in in_band if l not in header_lines]
            name = " ".join(l.text(name_x0, name_end) for l in name_lines).strip()

            def cell(key: str) -> str:
                x0, x1 = geom.get(f"{key}_x0"), geom.get(f"{key}_end")
                if x0 is None:
                    return ""
                return " ".join(l.text(x0, x1) for l in data_lines).strip()
            item = _build_item(
                food_number=num, name=name, category=major, subcategory=minor,
                iso=iso, country=cell("country"), year=cell("year"),
                gi=cell("gi"), subjects=cell("subjects"),
                ref=" ".join(l.text(geom["ref_x0"]) for l in data_lines).strip(),
            )
            if item["gi_glucose"] is None:
                warnings.append(f"p{page_no} #{num}: no GI value ({name[:50]!r})")
                continue
            if len(name) < 3:
                warnings.append(f"p{page_no} #{num}: no name (GI {item['gi_glucose']})")
                continue
            items.append(item)

    return items, warnings


def _split_name_and_headers(in_band: list[_Line], num_y: float
                            ) -> tuple[list[_Line], list[_Line]]:
    """Separate a band's wrapped name lines from category/note lines above it.

    The name is the contiguous run of lines around the food number: wrapped
    name lines sit within _INTRA_ROW_GAP of each other, while a category
    header or portion note is separated by a visibly larger gap and never has
    a food number inside its own run.
    """
    if not in_band:
        return [], []
    anchor = min(range(len(in_band)), key=lambda i: abs(in_band[i].y - num_y))
    lo = anchor
    while lo > 0 and in_band[lo].y - in_band[lo - 1].y <= _INTRA_ROW_GAP:
        lo -= 1
    hi = anchor
    while hi + 1 < len(in_band) and in_band[hi + 1].y - in_band[hi].y <= _INTRA_ROW_GAP:
        hi += 1
    # The number must sit within (or just outside) the accepted run, or the
    # anchor line is really a header and this row's name is elsewhere.
    if not (in_band[lo].y - _NUMBER_TOL <= num_y <= in_band[hi].y + _NUMBER_TOL):
        return [], list(in_band)
    return in_band[lo:hi + 1], in_band[:lo] + in_band[hi + 1:]


def _food_numbers(candidates: list[tuple[float, int, float]]
                  ) -> list[tuple[float, int]]:
    """Food numbers on a page, from integer words in the left margin.

    A stray integer can land there when a value or footnote marker overflows
    leftward out of its own cell. Requiring the x to match the food-number
    column proper — the x shared by the page's other numbers — rejects those.

    Deliberately NOT also requiring the numbers to ascend: two rows in
    Supplemental Table 2 carry a misprinted number in the published PDF (2211
    appears as "2111" and 3536 as "2536"), and an ascending check throws those
    otherwise-intact rows away. The number is only a label here — nothing
    looks a food up by it — so a wrong one costs nothing, while losing the row
    costs its GI value.
    """
    if not candidates:
        return []
    xs = [x for _y, _n, x in candidates]
    modal_x = max(set(xs), key=lambda v: sum(1 for x in xs if abs(x - v) < 3))
    return sorted((y, n) for y, n, x in candidates if abs(x - modal_x) < 3)


def _build_item(*, food_number: int, name: str, category: str | None,
                subcategory: str | None, iso: bool, country: str,
                year: str, gi: str, subjects: str, ref: str) -> dict:
    gi_value, sem = _parse_gi(gi)
    ym = _YEAR_RE.search(year)
    sm = _SUBJ_RE.search(subjects)
    subj_type = sm.group(1) if sm else None
    item = {
        "food_number": food_number,
        "name": re.sub(r"\s+", " ", name).strip(),
        "gi_glucose": gi_value,
        "sem": sem,
        "year": int(ym.group(1)) if ym else None,
        "country": _clean_country(country),
        "subjects_type": subj_type,
        "subjects_n": int(sm.group(2)) if sm and sm.group(2) else None,
        "category": category,
        "subcategory": subcategory,
        "iso": iso,
        "edition": 2021,
        "ref": re.sub(r"\s+", " ", ref).strip(),
    }
    item["population"] = _classify_population(subj_type, iso)
    return item


def _classify_population(subj_type: str | None, iso: bool) -> str:
    """Map a row's own Subjects cell to numa's normal/impaired/unknown.

    Table 1's explanatory note requires "reported normal glucose tolerance"
    of every row it contains, so an unreadable cell there is still normal.
    Table 2 mixes populations, so an unreadable cell there really is unknown.
    """
    if subj_type:
        key = subj_type.strip().lower()
        if key in _IMPAIRED_SUBJECTS:
            return "impaired"
        if key == "normal":
            return "normal"
    return "normal" if iso else "unknown"


def _parse_gi(gi: str) -> tuple[float | None, float | None]:
    """GI on the glucose-referenced scale, plus its SEM where published.

    `gi` is already narrowed to that column, so the only ambiguity left is
    whether a SEM was reported at all: Supplemental Table 1 always reports one,
    Table 2 has several hundred rows carrying a bare GI.
    """
    m = _GI_SEM_RE.search(gi)
    if m:
        return float(m.group(1)), float(m.group(2))
    bare = re.search(r'(?<![\d.])(\d{1,3}(?:\.\d)?)(?![\d.])', gi)
    if bare:
        value = float(bare.group(1))
        # Published GI values do exceed 100 — sucrose reaches 132 in one study
        # here — so the bound is only a sanity check on a misread cell, not a
        # cap on what the table is allowed to say.
        if 0 <= value <= _MAX_GI:
            return value, None
    return None, None


def _clean_country(country: str | None) -> str | None:
    """Country of food production, read from that column's own x window.

    Taken positionally rather than as "the text before the year", because a
    band's wrapped lines put other columns' fragments first.
    """
    if not country:
        return None
    text = re.sub(r'\s+', ' ', country).strip(' ,;')
    if not text or text.replace(".", "").isdigit() or _YEAR_RE.fullmatch(text):
        return None
    return text


def _merge_key(name: str) -> str:
    """Normalized name used to decide whether a 2008 row survives into 2021.

    Parenthetical brand/manufacturer text is dropped: 2021 frequently rewrote
    it while describing the same food.
    """
    bare = re.sub(r'\([^)]*\)', ' ', name).lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]+', ' ', bare)).strip()


# Form words a 2008 name can start with when its category prefix went missing.
_GENERIC_START_RE = re.compile(
    r'^(Type NS|White|Brown|New|Instant|Boiled|Raw|Cooked|Plain|Regular'
    r'|Wholemeal|Whole wheat|Canned|Dried|Fresh|Mixed)\b', re.I
)


def _repair_legacy_name(name: str, category: str | None) -> str:
    """Put a 2008 row's category back on the front of a fragmentary name.

    The 2008 parser guessed at category headers with a text heuristic its own
    docstring called imperfect, and where it guessed wrong a food kept only the
    tail of its description — "Type NS (India)" under the category "Millet",
    or "New (Canada)" under "Potatoes". Alone in the Annotate picker those say
    nothing and invite a mis-pick, so the category goes back on the front.
    A category that is itself wreckage from that same heuristic (it starts with
    a bracket) is left off rather than compounding the mess.
    """
    if not category or category.startswith("("):
        return name
    if not (len(name) < 20 or _GENERIC_START_RE.match(name)):
        return name
    if category.lower() in name.lower():
        return name
    return f"{category}, {name}"


def _superseded(key: str, keys_2021: set[str], tokens_2021: dict[str, set[str]]
                ) -> bool:
    """Whether a 2008 row's name is the same food as some 2021 row's.

    Exact normalized equality catches only about a quarter of the overlap: 2021
    reworded most descriptions, moving the brand out of the parenthesis, adding
    the cooking method, or leading with the food rather than the form ("Bread,
    flax, made from flax meal & wheat flour" became "Flax bread made from flax
    meal wheat flour"). So containment and a similarity threshold are used too.

    Over-inclusion applies to genuine uncertainty, not to matches that can be
    detected — a 2008 row kept beside the 2021 row describing the same study is
    a duplicate in the Annotate picker, one of them missing a year of test.
    """
    if key in keys_2021:
        return True
    if len(key) >= _MIN_CONTAINMENT_LEN:
        for other in keys_2021:
            if key in other or other in key:
                return True
    words = set(key.split())
    if not words:
        return False
    for other, other_words in tokens_2021.items():
        shared = len(words & other_words)
        if shared < 2 or shared / max(len(words), len(other_words)) < 0.5:
            continue                # too little in common to be worth scoring
        if difflib.SequenceMatcher(None, key, other).ratio() >= _MATCH_RATIO:
            return True
    return False


def _legacy_rows(existing: dict, keys_2021: set[str]) -> list[dict]:
    """2008 rows describing a food no 2021 row covers, in the new row shape."""
    tokens_2021 = {k: set(k.split()) for k in keys_2021}
    out: list[dict] = []
    for pool, rows in existing.items():
        for row in rows:
            if row.get("edition") == 2021:
                continue            # re-run over an already-migrated file
            key = _merge_key(row["name"])
            if not key or _superseded(key, keys_2021, tokens_2021):
                continue
            out.append({
                "food_number": None,
                "name": _repair_legacy_name(row["name"], row.get("category")),
                "gi_glucose": row["gi_glucose"],
                "sem": None,
                "year": None,       # the 2008 extraction never captured one
                "country": None,
                "subjects_type": None,
                "subjects_n": None,
                "category": row.get("category"),
                "subcategory": None,
                "iso": None,        # predates the ISO-compliance split
                "edition": 2008,
                "ref": row.get("ref", ""),
                "population": row.get("population", pool),
            })
    return out


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    table1, warn1 = _parse_pdf(Path(sys.argv[1]), iso=True)
    table2, warn2 = _parse_pdf(Path(sys.argv[2]), iso=False)
    rows = table1 + table2
    keys_2021 = {_merge_key(r["name"]) for r in rows}

    legacy: list[dict] = []
    if BASELINE.exists():
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        legacy = _legacy_rows(baseline, keys_2021)
        rows += legacy

    pools: dict[str, list[dict]] = {"normal": [], "impaired": [], "unknown": []}
    for row in rows:
        pools[row["population"]].append(row)

    OUTPUT.write_text(json.dumps(pools, indent=2), encoding="utf-8")

    print(f"Wrote {OUTPUT}")
    print("  This file is yours alone: gitignored, never bundled, do not "
          "redistribute it.")
    print(f"  2021 Supplemental Table 1 (ISO-consistent):    {len(table1)} entries")
    print(f"  2021 Supplemental Table 2 (method deviations): {len(table2)} entries")
    print(f"  2008 rows carried forward as legacy tier:      {len(legacy)}")
    for pool, items in pools.items():
        dated = sum(1 for i in items if i["year"])
        print(f"  {pool}: {len(items)} entries ({dated} with a year of test)")
    for w in warn1 + warn2:
        print(f"  SKIPPED {w}")


if __name__ == "__main__":
    main()
