"""
prefs.py — dietary preference load/save and first-run animal-foods prompt.
Docs: README-numa-documentation.md, Project Structure
"""
import json
import pathlib

from .. import state
from ..ui.prompts import Cancelled, _prompt

_PREFS_FILE = pathlib.Path.home() / ".local" / "share" / "numa" / "prefs.json"


def _load_prefs() -> None:
    if _PREFS_FILE.exists():
        try:
            data = json.loads(_PREFS_FILE.read_text())
            if not isinstance(data, dict):
                return
            state.set_include_animal_foods(bool(data.get("include_animal_foods", True)))
            setattr(state, "_editor_command", str(data.get("editor_command", "") or "").strip())
            setattr(state, "_display_program_settings", bool(data.get("display_program_settings", False)))
        except (json.JSONDecodeError, OSError):
            pass


def _save_prefs() -> None:
    data: dict = {}
    if _PREFS_FILE.exists():
        try:
            loaded = json.loads(_PREFS_FILE.read_text())
            if isinstance(loaded, dict):
                data = loaded
        except (json.JSONDecodeError, OSError):
            data = {}

    data["include_animal_foods"] = state._include_animal_foods
    data["editor_command"] = str(getattr(state, "_editor_command", "") or "").strip()
    data["display_program_settings"] = bool(getattr(state, "_display_program_settings", False))

    if not data["editor_command"]:
        data.pop("editor_command", None)

    _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _PREFS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def _ask_animal_foods_pref() -> None:
    """First-run prompt: ask whether to include animal foods in suggestions."""
    state.console.print(
        f"\n  [{state.T['hi']}]One quick question before we begin[/{state.T['hi']}]\n"
        f"\n  Should protein complement suggestions include animal-based foods"
        f"\n  (eggs, cheese, fish, chicken, whey protein)?\n"
        f"\n  [{state.T['accent']}]y[/{state.T['accent']}] — Yes, include animal foods"
        f"  [{state.T['accent']}]n[/{state.T['accent']}] — No, plant-based only\n"
        f"\n  [dim]This can be changed later under Settings → Dietary preferences.[/dim]"
    )
    try:
        ans = _prompt("Include animal foods?  [dim](Y/n)[/dim]", default="y").strip().lower()
    except Cancelled:
        ans = "y"
    state.set_include_animal_foods(ans != "n")
    _save_prefs()
    label = "animal foods included" if state._include_animal_foods else "plant-based only"
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {label}.")
