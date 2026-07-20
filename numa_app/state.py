"""
state.py — shared mutable application state: AppContext dataclass, theme dict, and dietary preference flag.
Docs: README-numa-documentation.md, Architecture: "numa_app/state.py — shared state"
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from rich.console import Console

import platform_utils as _platform_utils
_config_dir = _platform_utils.get_config_dir()


THEMES: dict[str, dict[str, str]] = {
    "dark": {
        "accent": "bold cyan",
        "accent_plain": "cyan",
        "success": "green",
        "warning": "bold yellow",
        "error": "bold red",
        "danger": "bold red",
        "choice": "bold green",
        "default_hint": "bold blue",
        "hi": "bold white",
    },
    "light": {
        "accent": "bold blue",
        "accent_plain": "blue",
        "success": "dark_green",
        "warning": "bold dark_orange",
        "error": "bold red",
        "danger": "bold red",
        "choice": "bold dark_green",
        "default_hint": "bold navy_blue",
        "hi": "bold black",
    },
    "neutral": {
        "accent": "bold",
        "accent_plain": "bold",
        "success": "bold",
        "warning": "bold",
        "error": "bold",
        "danger": "bold underline",
        "choice": "bold",
        "default_hint": "bold",
        "hi": "bold",
    },
}


@dataclass
class AppContext:
    console: Console = field(default_factory=Console)
    theme_name: str = "dark"
    theme: dict[str, str] = field(default_factory=lambda: THEMES["dark"].copy())
    diet_pref: str = "all"  # "all" | "vegetarian" | "plant_only"
    sort_prefs: dict = field(default_factory=lambda: {
        "recipes": "recent", "food_cache": "name", "meals": "date",
    })
    theme_file: Path = field(default_factory=lambda: _platform_utils.get_config_dir() / "theme")
    prefs_file: Path = field(default_factory=lambda: _platform_utils.get_config_dir() / "prefs.json")


app_ctx = AppContext()

# Aliases used throughout the split modules.
console = app_ctx.console
T = app_ctx.theme
_current_theme_name = app_ctx.theme_name
_diet_pref = app_ctx.diet_pref


def sync_globals() -> None:
    global console, T, _current_theme_name, _diet_pref
    console = app_ctx.console
    T = app_ctx.theme
    _current_theme_name = app_ctx.theme_name
    _diet_pref = app_ctx.diet_pref


def set_theme(name: str, theme: dict[str, str]) -> None:
    app_ctx.theme_name = name
    app_ctx.theme = theme
    sync_globals()


def set_diet_pref(value: str) -> None:
    app_ctx.diet_pref = value
    sync_globals()


def get_sort_pref(list_name: str, default: str) -> str:
    return app_ctx.sort_prefs.get(list_name, default)


def set_sort_pref(list_name: str, value: str) -> None:
    app_ctx.sort_prefs[list_name] = value
    sync_globals()


sync_globals()
