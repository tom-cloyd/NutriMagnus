"""
common.py — menu rendering, safe dispatch, and table formatting helpers (dot_cell, section_title, etc.).
Docs: README-numa-documentation.md, Architecture: "numa_app/ui/common.py — menu rendering and safe dispatch"
"""
import os
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
ID_KEY = "[dim](ID key: number = USDA FDC · OFF = Open Food Facts · usr = user-drafted)[/dim]"


def dot_cell(text: str, width: int) -> str:
    """Truncate *text* to *width* chars and pad the remainder with dim dot leaders."""
    t = text[:width - 1]
    return f"{t} [dim]{'·' * (width - len(t) - 1)}[/dim]"


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
    sub = f"  [dim]{subtitle}[/dim]" if subtitle else ""
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


def help_footer(*anchors: str) -> None:
    """Warning-coloured one-liner listing lookupable help topics for the preceding output block.
    anchors: short manual anchor names (e.g. 'diaas', 'complete', 'fao').
    User types ?anchor at any prompt to display that section of the user manual."""
    topics = "  ".join(f"?{a}" for a in anchors)
    state.console.print(
        f"\n  [{state.T['warning']}]Help: {topics}[/{state.T['warning']}]",
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
        return f"[dim]{fdc_id}[/dim]"
    if fdc_id <= _OFF_ID_THRESHOLD:
        return "[dim]OFF[/dim]"
    return "[dim]usr[/dim]"


def _show_menu(title: str, items: list[tuple[str, str]]) -> None:
    """Render a numbered/lettered menu with a title."""
    _W = min(100, state.console.width)
    state.console.print(f"\n[{state.T['accent']}]{title}[/{state.T['accent']}]")
    state.console.print(Rule(), width=_W)
    for key, label in items:
        if key.isdigit():
            state.console.print(f"  [{state.T['accent']}]{key}.[/{state.T['accent']}] {label}", highlight=False)
        else:
            state.console.print(f"  [dim]{key}.[/dim] {label}", highlight=False)
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
        state.console.print("[dim]Cancelled.[/dim]")

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
            if subprocess.run(["which", fallback], capture_output=True).returncode == 0:
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
