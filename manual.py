"""
manual.py — User manual parser and ?keyword help lookup.

user-manual.md format:
  ## [anchor] Section Title
  Body text (plain text, multiple lines).
  (next ## [anchor] line starts the next section)

Callers display results via show(); lookup() returns raw (title, body) if
the caller wants to handle display itself.
"""
from __future__ import annotations

import pathlib

_MANUAL_FILE = pathlib.Path(__file__).parent / "user-manual.md"
_sections: dict[str, tuple[str, str]] | None = None

# Common shortcuts → canonical anchor.
_ALIASES: dict[str, str] = {
    "?":                    "help",
    "amino-acid":           "aa",
    "amino-acids":          "aa",
    "essential-amino-acids": "aa",
    "amino-acid-gap":       "gap",
    "amino-acid-gaps":      "gap",
    "gaps":                 "gap",
    "suggest":              "comp",
    "complements":          "comp",
    "complement":           "comp",
    "dietary":              "diet",
    "diet-pref":            "diet",
    "dietary-pref":         "diet",
    "dietary-preferences":  "diet",
    "preferences":          "diet",
    "completeness":         "complete",
    "complete-protein":     "complete",
    "protein-completeness": "complete",
    "digestible":           "dcp",
    "digestible-protein":   "dcp",
    "goal":                 "goals",
    "daily-goals":          "goals",
    "nutrient-goals":       "goals",
    "targets":              "goals",
    "daily-targets":        "goals",
}


def _load() -> dict[str, tuple[str, str]]:
    global _sections
    if _sections is not None:
        return _sections
    _sections = {}
    if not _MANUAL_FILE.exists():
        return _sections

    current_anchor: str | None = None
    current_title = ""
    current_lines: list[str] = []

    def _flush() -> None:
        if current_anchor is not None:
            # Strip section-separator lines (---) that bleed into body from the raw file
            body = "\n".join(l for l in current_lines if l.rstrip() != "---").strip()
            _sections[current_anchor] = (current_title, body)

    all_lines = _MANUAL_FILE.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(all_lines):
        line = all_lines[i]
        stripped = line.rstrip()
        next_stripped = all_lines[i + 1].rstrip() if i + 1 < len(all_lines) else ""

        # Primary format: "Title [anchor]" followed immediately by 10+ dashes
        if (stripped.endswith("]") and "[" in stripped
                and len(next_stripped) >= 10 and all(c == "-" for c in next_stripped)):
            _flush()
            current_lines = []
            open_b = stripped.rfind("[")
            current_anchor = stripped[open_b + 1:-1].strip().lower()
            current_title = stripped[:open_b].strip() or current_anchor
            i += 2  # consume title line + underline
            continue

        # Legacy format: any markdown heading level — "## Title [anchor]" or "### Title [anchor]"
        stripped_hashes = stripped.lstrip("#")
        if (stripped_hashes.startswith(" ") and stripped_hashes != stripped
                and stripped.endswith("]") and "[" in stripped):
            _flush()
            current_lines = []
            text = stripped_hashes.strip()
            open_b = text.rfind("[")
            current_anchor = text[open_b + 1:-1].strip().lower()
            current_title = text[:open_b].strip() or current_anchor
        elif current_anchor is not None:
            current_lines.append(line)

        i += 1

    _flush()
    return _sections


def lookup(ref: str) -> tuple[str, str] | None:
    """Return (title, body) for the anchor (resolving aliases), or None."""
    key = ref.lower().strip().lstrip("?")
    key = _ALIASES.get(key, key)
    return _load().get(key)


def available() -> list[str]:
    """Return all anchor names defined in the manual (sorted, no aliases)."""
    return sorted(_load().keys())


def show(ref: str) -> bool:
    """
    Display the manual section for ref using the app's Rich console.
    Returns True if found, False if not.
    Must be called only after numa_app.state has been initialised.
    """
    from rich.panel import Panel
    from numa_app import state

    entry = lookup(ref)
    if entry is None:
        known = ", ".join(f"?{a}" for a in available())
        state.console.print(
            f"\n  [dim]No help entry for '[bold]{ref}[/bold]'.[/dim]"
            f"\n  [dim]Available topics: {known}[/dim]"
        )
        return False

    title, body = entry
    _W = min(100, state.console.width)
    state.console.print(
        Panel(
            body,
            title=f"[bold]{title}[/bold]",
            border_style=state.T["accent_plain"],
            padding=(1, 2),
            width=_W,
        )
    )
    return True
