"""
common.py — menu rendering, safe dispatch, and table formatting helpers (dot_cell, section_title, etc.).
Docs: README-numa-documentation.md, Architecture: "numa_app/ui/common.py — menu rendering and safe dispatch"
"""
import os
import shutil
import subprocess
import tempfile
from typing import Any, Callable

from rich.rule import Rule

from .. import state
from .prompts import Cancelled

# Threshold separating Open Food Facts synthetic IDs from user-drafted negatives.
# OFF IDs are derived from barcodes via _OFF_ID_BASE = -2_000_000_000.
_OFF_ID_THRESHOLD = -1_000_000_000

# One-line key shown near any table or list that displays food IDs.
ID_KEY = "[grey62](ID key: number = USDA FDC · OFF = Open Food Facts · usr = user-drafted)[/grey62]"


def dot_cell(text: str, width: int, *, bold: bool = False) -> str:
    """Truncate *text* to *width* chars and pad the remainder with dim dot leaders.
    Pass bold=True for search/pick-list results, so the name stands out from the leaders."""
    t = text[:width - 1]
    if bold:
        t = f"[bold]{t}[/bold]"
    return f"{t} [grey62]{'·' * (width - len(text[:width - 1]) - 1)}[/grey62]"


def table_title(title: str, subtitle: str = "") -> None:
    """Blank line + indented hi-colour title for a table within an analysis section.
    Pass *subtitle* as a pre-formatted Rich markup string when a colour legend or
    extra context belongs on the same line as the title."""
    sub = f"  {subtitle}" if subtitle else ""
    state.console.print()
    state.console.print(f"  [{state.T['hi']}]{title}[/{state.T['hi']}]{sub}", highlight=False)


def section_title(title: str, subtitle: str = "") -> None:
    """Blank line + full-width accent title + rule — for top-level output sections.
    *subtitle* is plain text; it is wrapped in dim automatically."""
    sub = f"  [grey62]{subtitle}[/grey62]" if subtitle else ""
    _W = min(100, state.console.width)
    state.console.print()
    state.console.print(f"[{state.T['accent']}]{title}[/{state.T['accent']}]{sub}", highlight=False)
    state.console.print(Rule(), width=_W)


def table_footer(*lines: str) -> None:
    """Blank line then each line printed as-is — for key legends, totals, and notes.
    Callers supply their own Rich markup (dim, colour, etc.)."""
    state.console.print()
    for line in lines:
        state.console.print(line, highlight=False)


def help_footer(*topics: str) -> None:
    """Remind the user about ?help topics.

    With no args: prints the generic '?help' hint.
    With topic names: prints 'At any prompt, type ?foo or ?bar for help with these topics.'
    """
    if topics:
        topic_str = " or ".join(f"?{t}" for t in topics)
        msg = f"At any prompt, type {topic_str} for help with these topics."
    else:
        msg = "At any prompt, type ?help to see a list of available help topics."
    state.console.print(
        f"\n  [{state.T['warning']}]{msg}[/{state.T['warning']}]\n",
        highlight=False,
    )


def _id_cell(fdc_id: int | None) -> str:
    """Return a dimmed display string for a food's database ID column.

    Positive integers are USDA FDC IDs shown as-is.
    Values ≤ -1_000_000_000 are Open Food Facts synthetic IDs → 'OFF'.
    Small negatives are user-drafted food IDs → 'usr'.
    None → empty string.
    """
    if fdc_id is None:
        return ""
    if fdc_id > 0:
        return f"[grey62]{fdc_id}[/grey62]"
    if fdc_id <= _OFF_ID_THRESHOLD:
        return "[grey62]OFF[/grey62]"
    return "[grey62]usr[/grey62]"


def classify_food_id(fdc_id: int | None, recipe_id: int | None = None) -> tuple[str, str] | None:
    """Return (id_str, source_label) for a food/recipe reference, or None if nothing to show.

    recipe_id takes priority (a recipe used as a meal item or nested ingredient
    has no fdc_id of its own). source_label is one of "Recipe", "USDA", "OFF",
    "User-drafted".
    """
    if recipe_id is not None:
        return str(recipe_id), "Recipe"
    if fdc_id is None:
        return None
    if fdc_id > 0:
        return str(fdc_id), "USDA"
    if fdc_id <= _OFF_ID_THRESHOLD:
        return str(fdc_id), "OFF"
    return str(fdc_id), "User-drafted"


def food_id_tag(fdc_id: int | None, recipe_id: int | None = None, *, inline: bool = False) -> str:
    """Return '(#id, SOURCE)' Rich markup to identify a displayed food/recipe name.

    By default this starts with a newline + indent, so simple concatenation
    (f"{name}{food_id_tag(...)}") places the tag on its own line directly under
    the name. Pass inline=True at the few call sites that join several
    name+tag pairs into one running line (e.g. "Added: A, B, C") where a
    forced line break would break the list.

    Empty string if there's nothing to identify (fdc_id and recipe_id both None).
    """
    classified = classify_food_id(fdc_id, recipe_id)
    if classified is None:
        return ""
    id_str, source = classified
    tag = f"[grey62](#{id_str}, {source})[/grey62]"
    return f" {tag}" if inline else f"\n    {tag}"


def _show_menu(title: str, items: list[tuple[str, str]]) -> None:
    """Render a numbered/lettered menu with a title."""
    _W = min(100, state.console.width)
    state.console.print(f"\n[{state.T['accent']}]{title}[/{state.T['accent']}]")
    state.console.print(Rule(), width=_W)
    for key, label in items:
        if key.isdigit():
            state.console.print(f"  [{state.T['accent']}]{key}.[/{state.T['accent']}] {label}", highlight=False)
        else:
            state.console.print(f"  [grey62]{key}.[/grey62] {label}", highlight=False)
    state.console.print()
    state.console.print("  [grey62]?help at any prompt — show available help topics[/grey62]")
    state.console.print()


def _safe_call(fn: Callable[..., Any], *args: Any) -> None:
    """Call fn(*args), silencing Cancelled (prints 'Cancelled.').
    SystemExit(0) and ReturnToMain propagate — never swallow them here."""
    try:
        fn(*args)
    except SystemExit as e:
        if e.code == 0:
            raise
    except Cancelled:
        state.console.print("[grey62]Cancelled.[/grey62]")

def _open_in_editor(text: str = "") -> str:
    """
    Open `text` in the user's configured editor and return the edited result.
    Editor is resolved in order: state._editor_command → $VISUAL → $EDITOR → nano → vi.
    Returns the original text unchanged if the editor cannot be launched.
    """
    cmd = str(getattr(state, "_editor_command", "") or "").strip()
    if not cmd:
        cmd = os.environ.get("VISUAL") or os.environ.get("EDITOR") or ""
    if not cmd:
        # last-resort fallbacks
        for fallback in ("nano", "vi"):
            if shutil.which(fallback) is not None:
                cmd = fallback
                break
    if not cmd:
        state.console.print(
            f"  [{state.T['warning']}]No editor found. Set one under Settings → Editor command.[/{state.T['warning']}]"
        )
        return text

    suffix = ".txt"
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as tf:
            tf.write(text)
            tf_path = tf.name
        # Split to handle commands like "code --wait"
        cmd_parts = cmd.split() + [tf_path]
        _hint_map = {
            "micro": "Ctrl+S = save  ·  Ctrl+Q = quit",
            "nano":  "Ctrl+O = save  ·  Ctrl+X = quit",
            "vim":   ":wq = save and quit  ·  :q! = quit without saving",
            "vi":    ":wq = save and quit  ·  :q! = quit without saving",
            "nvim":  ":wq = save and quit",
            "helix": "Ctrl+S = save  ·  :q = quit",
            "hx":    "Ctrl+S = save  ·  :q = quit",
        }
        _ename = os.path.basename(cmd_parts[0]).lower()
        _hint = next((v for k, v in _hint_map.items() if k in _ename), None)
        if _hint:
            state.console.print(f"  [grey62]({_hint})[/grey62]")
        subprocess.run(cmd_parts, check=False)
        with open(tf_path, encoding="utf-8") as f:
            result = f.read()
    except Exception as exc:
        state.console.print(
            f"  [{state.T['warning']}]Editor error: {exc}[/{state.T['warning']}]"
        )
        return text
    finally:
        try:
            os.unlink(tf_path)
        except OSError:
            pass
    return result


def _prompt_with_options(
    prompt_label: str,
    options: list[tuple[str, str]],
    *,
    default: str = "",
) -> str:
    """Show explicit option lines above a prompt, then collect a choice."""
    state.console.print()
    state.console.print("  Options:")
    for key, desc in options:
        state.console.print(f"    {key:<5} {desc}", highlight=False)
    state.console.print()
    from .prompts import _prompt
    return _prompt(prompt_label, default=default).strip().lower()
