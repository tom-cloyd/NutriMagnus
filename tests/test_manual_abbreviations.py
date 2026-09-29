"""
Regression test for the weekly sweep's "unexpanded abbreviations" item
(README-numa-documentation.md, Maintenance section), added 2026-09-27.

The manual is not read front to back. Every heading is a landing point --
the app's "learn more..." links, the table of contents, and the manual's own
search all drop a reader into the middle of it. So an abbreviation that was
spelled out three sections earlier is, for that reader, simply undefined.
The rule this test enforces:

    An abbreviation must, WITHIN THE SECTION WHERE IT APPEARS, either be
    expanded inline on first use or be linked to its glossary entry.

Expanded inline means the letters and the words appear together -- "IOM
(Institute of Medicine)" or "Institute of Medicine (IOM)" -- not merely the
full name somewhere in nearby prose, which leaves the reader to guess that
the two refer to the same thing (the distinction that prompted this test).

Sections are delimited by any Markdown heading, since any of them can be
landed on directly. The changelog (Appendix A) is excluded: its entries are
a dated historical record and are deliberately never rewritten.
"""
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_MANUAL = _ROOT / "user-manual.md"

# Self-evident in context, or not abbreviations NuMa should be teaching:
# file formats and units the reader either knows or never needs to act on,
# country codes, date-format placeholders, and desktop-environment names
# that only ever appear beside installation instructions.
_ALLOWED = {
    # Computing terms are NOT exempt. NuMa's readers are people managing
    # their own nutrition, not developers: CSV, PDF, API, PNG, SVG, ID and
    # the rest all get a Glossary entry and a link like any other
    # abbreviation (owner's call, 2026-09-27). "PC" stays only because it is
    # ordinary English for a computer, not a term anyone must look up.
    "PC",
    # Country / region codes used as plain adjectives ("UK foods").
    "US", "UK", "USA", "EU",
    # Date-format placeholders in examples.
    "YYYY", "MM", "DD", "HH",
    # Linux desktop environments. Exempt only because the passage naming
    # them says outright that they ARE Linux desktop environments, so a
    # Windows reader is not left baffled -- keep that framing if that
    # passage is ever rewritten.
    "GNOME", "KDE", "XFCE", "MATE", "LTS", "DEB", "RPM",
    # Project / file names, not abbreviations to expand.
    "NUMA", "README", "CLAUDE", "FAQ", "TODO",
    # Paper sizes and table/appendix designators from cited sources
    # ("Table A1", "US Letter or A4") -- labels, not abbreviations.
    "A1", "A2", "A3", "A4", "UO", "UO4", "UO5",
    # Vitamin and nutrient identifiers. "B12" is the vitamin's name, not a
    # contraction of anything longer.
    "B1", "B2", "B3", "B6", "B12", "D2", "D3", "K1", "K2",
    # Keyboard key names, always written beside "key" ("press the F5 key").
    "F5",
    # Everyday English abbreviations needing no gloss.
    "ASAP", "AKA", "ETC", "IE", "EG", "AM", "PM",
}

# ALL-CAPS English words that appear in bold labels and emphatic prose and
# are not abbreviations at all. Kept explicit rather than inferred, so a
# genuine new abbreviation can never be silently swallowed by a heuristic.
_NOT_ABBREVIATIONS = {
    "AND", "THE", "NOT", "ALL", "FOR", "YOU", "ANY", "HOW", "WHAT", "MUCH",
    "BOTH", "WHEN", "DOES", "WHICH", "RIGHT", "ARE", "SIZED", "TO", "WHOLE",
    "BATCH", "EACH", "GOAL", "SINGLE", "ALWAYS", "TEXT", "ME", "IF", "SEND",
    "AN", "EMAIL", "IS", "PER", "MEAL", "FOOD", "RECIPE", "TIER", "UPDATE",
    "NEW", "ONE", "TWO", "DRY", "MILK", "NONFAT", "WITH", "FROM", "THAT",
    "THIS", "YOUR", "OWN", "USE", "SEE", "ADD", "SET", "GET", "NO", "OK",
    "IN", "ON", "AT", "OF", "OR", "BY", "AS", "IT", "BE", "DO", "SO", "UP",
    "ITEMS",  # the home page's NEW STARTER ITEMS banner label
}


def _body_sections() -> list[tuple[str, str]]:
    """The manual's prose, split into (heading, text) sections.

    Code fences, <pre> blocks, indented code blocks, footnote definitions,
    HTML comments and the changelog are all dropped: none of them is prose a
    reader parses for meaning, and the changelog is a historical record we
    don't rewrite.

    Indented code blocks matter more than they look. A Markdown link written
    inside one does not render -- the reader sees the raw
    "[DIAAS](#gloss-diaas)" text. So these blocks must be excluded here, or
    the test demands links in exactly the places where a link is broken.
    (Learned the hard way on 2026-09-27: 28 such links were added before the
    built HTML was checked.) A 4-space-indented line is only code when it is
    not part of a list -- nested bullets are indented too, and those render
    normally -- so list markers and the lines continuing them are kept.
    """
    lines = _MANUAL.read_text(encoding="utf-8").split("\n")
    try:
        stop = next(i for i, l in enumerate(lines)
                    if "Insert new updates below here" in l)
    except StopIteration:            # marker gone -- check the whole file
        stop = len(lines)

    sections: list[tuple[str, list[str]]] = [("(front matter)", [])]
    in_pre = in_fence = in_comment = in_list_block = False
    for line in lines[:stop]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if "<pre>" in line:
            in_pre = True
        if "</pre>" in line:
            in_pre = False
            continue
        if "<!--" in line:
            in_comment = True
        if "-->" in line:
            in_comment = False
            continue
        if in_pre or in_fence or in_comment or line.startswith("[^"):
            continue
        if re.match(r"^(?: {4,}|\t)", line):
            stripped = line.strip()
            is_list = bool(re.match(r"^(?:[-*+]\s|\d+[.)]\s)", stripped))
            if is_list:
                in_list_block = True
            elif not in_list_block:
                continue            # indented code block -- not prose
            if not stripped:
                in_list_block = False
        elif line.strip():
            in_list_block = False
        if line.startswith("#"):
            sections.append((line.strip(), []))
            continue
        sections[-1][1].append(line)
    return [(h, "\n".join(body)) for h, body in sections]


# A few letter-pairs are not always the abbreviation the glossary defines.
# "AI" is Adequate Intake in the nutrition chapters but artificial
# intelligence in "Claude AI" -- a product name, where linking it to the
# nutrition entry is actively wrong (it briefly was, on 2026-09-27). Each
# entry maps a token to the contexts in which it is NOT the glossary's term;
# those occurrences are dropped before the section is checked.
_OTHER_SENSE = {
    "AI": re.compile(r"(?:Claude|local|on-board local|generative)\s+AI\b"),
}


def _is_handled(token: str, text: str) -> bool:
    """True if `text` either expands `token` inline or links it to the glossary."""
    patterns = (
        # IOM (Institute of Medicine) -- optionally bolded, linked or quoted.
        # The quote case covers codes shown as literal output: "NC" (not
        # computed).
        rf"""\b{token}\b[*"'\]]*\s*\(\s*[A-Za-z][A-Za-z.'-]*\s+[A-Za-z]""",
        # Institute of Medicine (IOM)
        rf"[A-Za-z]\s+\(\**{token}\**\)",
        # EAR -- Estimated Average Requirement
        rf"\b{token}\b\**\s*[-—]+\s*[A-Z][a-z]",
        # [IOM](#gloss-iom) / [EAAs](#gloss-eaa) -- linked by its own letters.
        rf"\[\**{token}s?\**\]\(#gloss-",
        # ...](#gloss-iom) -- linked under some other wording.
        rf"\]\(#gloss-{token.lower()}\)",
        # [FAO 2013 Reference Standard](#fao), [IAA ratios](#iaa-ratios) --
        # link text carrying the abbreviation, pointing at the section that
        # explains it. That serves the reader at least as well as a glossary
        # link, so it counts.
        rf"\[[^\]]*\b{token}\b[^\]]*\]\(#",
    )
    return any(re.search(p, text) for p in patterns)


def _offenders() -> list[str]:
    problems = []
    for heading, text in _body_sections():
        if heading.startswith("### B. Glossary"):
            continue             # the glossary defines them; that is its job
        for tok, pattern in _OTHER_SENSE.items():
            if tok in text:
                text = pattern.sub("", text)
        seen = set()
        # The trailing lookahead matters: a plain \b would let a 6-character
        # prefix of a longer all-caps word through ("AVAILA" from AVAILABLE).
        # "EPA+DHA" yields EPA and DHA, which is right -- it is two
        # abbreviations joined, not one ending in a plus. Underscore is
        # excluded too, so the literal DEMO_KEY is not read as "DEMO".
        for token in re.findall(r"\b[A-Z][A-Z0-9]{1,5}(?![A-Za-z0-9_])", text):
            if token in _ALLOWED or token in _NOT_ABBREVIATIONS or token in seen:
                continue
            seen.add(token)
            if not _is_handled(token, text):
                problems.append(f"{token}  in  {heading}")
    return problems


def test_manual_abbreviations_are_expanded_or_linked_in_their_own_section() -> None:
    offenders = _offenders()
    assert not offenders, (
        "Abbreviations used with no inline expansion and no glossary link in "
        "the section where they appear. A reader who lands on that section "
        "from a 'learn more...' link or the table of contents cannot resolve "
        "them. Expand on first use in the section -- IOM (Institute of "
        "Medicine) -- or link it: [IOM](#gloss-iom).\n  "
        + "\n  ".join(offenders)
    )
