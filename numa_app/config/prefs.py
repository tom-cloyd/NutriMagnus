"""
prefs.py — dietary preference load/save and first-run animal-foods prompt.
Docs: README-numa-documentation.md, Project Structure
"""
import json
import pathlib

import platform_utils as _platform_utils
from .. import state
from ..ui.prompts import Cancelled, _prompt

_PREFS_FILE = _platform_utils.get_data_dir() / "prefs.json"


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
            if data.get("sort_recipes") in ("recent", "name", "dcp"):
                state.app_ctx.sort_prefs["recipes"] = data["sort_recipes"]
            if data.get("sort_food_cache") in ("name", "type", "diaas", "gi"):
                state.app_ctx.sort_prefs["food_cache"] = data["sort_food_cache"]
            if data.get("sort_meals") in ("date", "name", "meal_bcp", "calories"):
                state.app_ctx.sort_prefs["meals"] = data["sort_meals"]
            if isinstance(data.get("show_archived_food_cache"), bool):
                state.app_ctx.list_filters["food_cache"] = data["show_archived_food_cache"]
            if isinstance(data.get("show_archived_pantry"), bool):
                state.app_ctx.list_filters["pantry"] = data["show_archived_pantry"]
            if isinstance(data.get("show_archived_recipes"), bool):
                state.app_ctx.list_filters["recipes"] = data["show_archived_recipes"]
            state.sync_globals()
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
    data["sort_recipes"] = state.app_ctx.sort_prefs.get("recipes", "recent")
    data["sort_food_cache"] = state.app_ctx.sort_prefs.get("food_cache", "name")
    data["sort_meals"] = state.app_ctx.sort_prefs.get("meals", "date")
    data["show_archived_food_cache"] = state.app_ctx.list_filters.get("food_cache", False)
    data["show_archived_pantry"] = state.app_ctx.list_filters.get("pantry", False)
    data["show_archived_recipes"] = state.app_ctx.list_filters.get("recipes", False)

    if not data["editor_command"]:
        data.pop("editor_command", None)

    _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _PREFS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def set_sort_pref(list_name: str, value: str) -> None:
    """Update the remembered sort choice for a list view ('recipes', 'food_cache',
    'meals') and persist it immediately so it's the default on next launch."""
    state.set_sort_pref(list_name, value)
    _save_prefs()


def set_list_filter(list_name: str, value: bool) -> None:
    """Update the remembered 'show archived' toggle for a list view ('recipes',
    'food_cache', 'pantry') and persist it immediately."""
    state.set_list_filter(list_name, value)
    _save_prefs()


def _ask_animal_foods_pref() -> None:
    """First-run prompt: ask which dietary preference to apply to suggestions."""
    state.console.print(
        f"\n  [{state.T['hi']}]One quick question before we begin[/{state.T['hi']}]\n"
        f"\n  Which foods should protein complement suggestions include?\n"
        f"\n  [{state.T['accent']}]1[/{state.T['accent']}] — All animal foods  [grey62](meat, fish, dairy, eggs)[/grey62]"
        f"\n  [{state.T['accent']}]2[/{state.T['accent']}] — Vegetarian  [grey62](dairy + eggs only)[/grey62]"
        f"\n  [{state.T['accent']}]3[/{state.T['accent']}] — Plant-based only\n"
        f"\n  [grey62]This can be changed later under Settings → Dietary preferences.[/grey62]"
    )
    try:
        ans = _prompt("Choice  [grey62](1/2/3)[/grey62]", default="1").strip()
    except Cancelled:
        ans = "1"
    pref = {"1": "all", "2": "vegetarian", "3": "plant_only"}.get(ans, "all")
    state.set_diet_pref(pref)
    _save_prefs()
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {_DIET_LABELS[pref]}.")
