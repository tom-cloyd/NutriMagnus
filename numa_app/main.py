"""
main.py — top-level orchestration: initialize_app(), print_startup_banner(), _run_menu(), run_app().
Docs: README-numa-documentation.md, Architecture: "numa_app/main.py — startup and top-level menu"
"""
import db as _db
import profile as _profile
import usda as _usda
from rich.rule import Rule
from . import state
from .config.prefs import _PREFS_FILE, _ask_animal_foods_pref, _load_prefs, _DIET_LABELS
from .config.theme import _detect_terminal_theme, _load_theme, _save_theme, _theme_source
from .ui.common import _safe_call
from .ui.prompts import Cancelled, ReturnToMain, _prompt, _load_input_history
from .workflows.foods import _menu_foods
from .workflows.meals import _menu_meals
from .workflows.settings import _menu_settings
from .workflows.recipes import _menu_recipes
from .workflows.summary import _menu_summary

_load_theme()


def _run_menu() -> None:
    """Top-level menu loop."""
    while True:
        diet_label = _DIET_LABELS.get(state._diet_pref, state._diet_pref)
        state.console.print()
        _W = min(100, state.console.width)
        state.console.print(f"[{state.T['accent']}]NutriMagnus Menu[/{state.T['accent']}]")
        state.console.print(Rule(), width=_W)
        state.console.print(f"  [{state.T['accent']}]1.[/{state.T['accent']}] [bold]Foods[/bold]")
        state.console.print("     [dim]search · analyze · compare · annotate · pantry · cache · custom profiles[/dim]")
        state.console.print(f"  [{state.T['accent']}]2.[/{state.T['accent']}] [bold]Recipes[/bold]")
        state.console.print("     [dim]create · browse/manage · develop (add/remove ingredients with nutritional feedback)[/dim]")
        state.console.print(f"  [{state.T['accent']}]3.[/{state.T['accent']}] [bold]Meals & Log[/bold]")
        state.console.print("     [dim]log meal · view/edit by date · analyze · delete[/dim]")
        state.console.print(f"  [{state.T['accent']}]4.[/{state.T['accent']}] [bold]Daily Summary[/bold]")
        state.console.print("     [dim]today · by date · recent days[/dim]")
        state.console.print(f"  [dim]5.[/dim] [bold]Settings[/bold]  [dim](theme · user profile · dietary preferences · API key · DB path)[/dim]")
        state.console.print("  [dim]q.[/dim] Quit")
        state.console.print()
        state.console.print("  [dim]Ctrl+C at any prompt — cancel and go back[/dim]")
        state.console.print()
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            break

        try:
            if choice == "1":
                if not _menu_foods():
                    break
            elif choice == "2":
                if not _menu_recipes():
                    break
            elif choice == "3":
                if not _menu_meals():
                    break
            elif choice == "4":
                if not _menu_summary():
                    break
            elif choice == "5":
                if not _menu_settings():
                    break
            elif choice == "q":
                break
            else:
                state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")
        except ReturnToMain:
            continue


def initialize_app(*, theme: str | None = None, api_key: str | None = None) -> bool:
    """Initialize config and handle optional startup actions.

    Returns True when the interactive menu should run, False when the caller should exit.
    """
    if api_key is not None:
        _usda.set_api_key(api_key)
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] API key saved.")
        return False

    if theme is not None:
        if theme not in (*state.THEMES, "auto"):
            state.console.print(
                f"[{state.T['error']}]Unknown theme '{theme}'. Choose: dark, light, neutral, auto[/{state.T['error']}]"
            )
            raise SystemExit(1)
        _save_theme(theme)
        actual = _detect_terminal_theme() if theme == "auto" else theme
        state.set_theme(actual, state.THEMES[actual])

    _db.init_db()
    _load_prefs()
    _load_input_history()
    if not _PREFS_FILE.exists() or "diet_pref" not in _PREFS_FILE.read_text():
        _ask_animal_foods_pref()
    return True


def print_startup_banner() -> None:
    source = _theme_source()
    diet_label = _DIET_LABELS.get(state._diet_pref, state._diet_pref)
    p = _profile.load_profile()

    _W = min(100, state.console.width)
    state.console.print()
    state.console.print(Rule(style="green"), width=_W)
    state.console.print(Rule(style="green"), width=_W)
    state.console.print('[bold green]NutriMagnus[/bold green] [dim]("nutrition wizard")[/dim]')
    from version import VERSION
    state.console.print(f"Nutritional Analysis for individuals and families - version {VERSION}", highlight=False)
    if p:
        profile_label = (
            f"age {p.age}, {p.sex},"
            f" {_profile.format_weight(p.weight_kg, p.weight_unit)},"
            f" {_profile.format_height(p.height_cm, p.height_unit)},"
            f" {_profile.ACTIVITY_LABELS.get(p.activity_level, p.activity_level)}"
        )
    else:
        profile_label = "not set -- configure under Settings -> User profile"

    state.console.print()
    state.console.print(f"[dim]Color theme: {state._current_theme_name}  ({source}) -- change via Settings[/dim]")
    state.console.print(f"[dim]Dietary preferences: {diet_label} -- change via Settings[/dim]")
    state.console.print(f"[dim]User profile: {profile_label}[/dim]", highlight=False)


def run_app(*, theme: str | None = None, api_key: str | None = None) -> None:
    if not initialize_app(theme=theme, api_key=api_key):
        return
    if getattr(state, "_display_program_settings", False):
        print_startup_banner()
    try:
        _run_menu()
    except SystemExit:
        pass
    state.console.print("\n[bold]Happy eating![/bold]\n")
