"""
prefs.py — dietary preference load/save and first-run animal-foods prompt.
Docs: README-numa-documentation.md, Project Structure
"""
import json
import pathlib

from .. import state
from ..ui.prompts import Cancelled, _prompt

_PREFS_FILE = pathlib.Path.home() / ".local" / "share" / "numa" / "prefs.json"


_VALID_DIET_PREFS = {"all", "vegetarian", "plant_only"}
_DIET_LABELS = {
    "all":        "all animal foods included",
    "vegetarian": "vegetarian (dairy + eggs)",
    "plant_only": "plant-based only",
}


def _load_prefs() -> None:
    if _PREFS_FILE.exists():
        try:
            data = json.loads(_PREFS_FILE.read_text())
            if not isinstance(data, dict):
                return
            needs_migration_save = False
            # New format: "diet_pref" string key
            if "diet_pref" in data:
                pref = data["diet_pref"]
                if pref in _VALID_DIET_PREFS:
                    state.set_diet_pref(pref)
            elif "include_animal_foods" in data:
                # Migrate legacy bool: True → "all", False → "plant_only"
                state.set_diet_pref("all" if data["include_animal_foods"] else "plant_only")
                needs_migration_save = True
            else:
                needs_migration_save = False
            setattr(state, "_editor_command", str(data.get("editor_command", "") or "").strip())
            setattr(state, "_display_program_settings", bool(data.get("display_program_settings", False)))
            if needs_migration_save:
                _save_prefs()  # all state now loaded — safe to write new format
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

    data.pop("include_animal_foods", None)  # remove legacy key
    data["diet_pref"] = state._diet_pref
    data["editor_command"] = str(getattr(state, "_editor_command", "") or "").strip()
    data["display_program_settings"] = bool(getattr(state, "_display_program_settings", False))

    if not data["editor_command"]:
        data.pop("editor_command", None)

    _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _PREFS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def _ask_animal_foods_pref() -> None:
    """First-run prompt: ask which dietary preference to apply to suggestions."""
    state.console.print(
        f"\n  [{state.T['hi']}]One quick question before we begin[/{state.T['hi']}]\n"
        f"\n  Which foods should protein complement suggestions include?\n"
        f"\n  [{state.T['accent']}]1[/{state.T['accent']}] — All animal foods  [dim](meat, fish, dairy, eggs)[/dim]"
        f"\n  [{state.T['accent']}]2[/{state.T['accent']}] — Vegetarian  [dim](dairy + eggs only)[/dim]"
        f"\n  [{state.T['accent']}]3[/{state.T['accent']}] — Plant-based only\n"
        f"\n  [dim]This can be changed later under Settings → Dietary preferences.[/dim]"
    )
    try:
        ans = _prompt("Choice  [dim](1/2/3)[/dim]", default="1").strip()
    except Cancelled:
        ans = "1"
    pref = {"1": "all", "2": "vegetarian", "3": "plant_only"}.get(ans, "all")
    state.set_diet_pref(pref)
    _save_prefs()
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {_DIET_LABELS[pref]}.")
