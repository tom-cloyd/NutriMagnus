"""
theme.py — color theme load/save/detect and the _change_theme() interactive flow.
Docs: README-numa-documentation.md, Project Structure
"""
import pathlib

from .. import state
from ..ui.prompts import _prompt

_THEME_FILE = pathlib.Path.home() / ".local" / "share" / "numa" / "theme"


def _detect_terminal_theme() -> str:
    import os as _os
    fgbg = _os.environ.get("COLORFGBG", "")
    if fgbg:
        try:
            return "light" if int(fgbg.split(";")[-1]) >= 8 else "dark"
        except ValueError:
            pass
    return "dark"


def _load_theme() -> None:
    if _THEME_FILE.exists():
        saved = _THEME_FILE.read_text().strip()
        if saved in state.THEMES:
            state.set_theme(saved, state.THEMES[saved])
            return
        if saved == "auto":
            detected = _detect_terminal_theme()
            state.set_theme(detected, state.THEMES[detected])
            return
    detected = _detect_terminal_theme()
    state.set_theme(detected, state.THEMES[detected])


def _save_theme(name: str) -> None:
    _THEME_FILE.parent.mkdir(parents=True, exist_ok=True)
    _THEME_FILE.write_text(name + "\n")


def _theme_source() -> str:
    if _THEME_FILE.exists():
        saved = _THEME_FILE.read_text().strip()
        if saved == "auto":
            return "auto-detected"
        if saved in state.THEMES:
            return "saved preference"
    return "auto-detected"


_load_theme()


def _change_theme() -> None:
    state.console.print(f"\n[{state.T['accent']}]Color theme[/{state.T['accent']}]  (current: {state._current_theme_name})")
    state.console.print(f"  [{state.T['accent']}]1.[/{state.T['accent']}] dark     — for dark terminal backgrounds")
    state.console.print(f"  [{state.T['accent']}]2.[/{state.T['accent']}] light    — for light terminal backgrounds")
    state.console.print(f"  [{state.T['accent']}]3.[/{state.T['accent']}] neutral  — bold/dim only, no color")
    state.console.print(f"  [{state.T['accent']}]4.[/{state.T['accent']}] auto     — detect each launch")
    state.console.print(f"  [{state.T['accent']}]Enter[/{state.T['accent']}] to keep current\n")
    choice = _prompt("Theme [1/2/3/4]", default="").strip()
    mapping = {"1": "dark", "2": "light", "3": "neutral", "4": "auto"}
    if choice in mapping:
        selected = mapping[choice]
        _save_theme(selected)
        actual = _detect_terminal_theme() if selected == "auto" else selected
        state.set_theme(actual, state.THEMES[actual])
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Theme set to [bold]{selected}[/bold].")
    else:
        state.console.print("[grey62]Theme unchanged.[/grey62]")
