"""
main.py — top-level orchestration: initialize_app(), print_startup_banner(), _run_menu(), run_app().
Docs: README-numa-documentation.md, Architecture: "numa_app/main.py — startup and top-level menu"
"""
import socket
import subprocess
import sys
import webbrowser
from pathlib import Path

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
from .workflows.analysis import _menu_analysis

_PROJECT_ROOT = Path(__file__).parent.parent
_WEB_URL = "http://127.0.0.1:8000"
_web_proc: "subprocess.Popen[bytes] | None" = None
_manual_opened = False


def _web_is_running() -> bool:
    if _web_proc is not None and _web_proc.poll() is None:
        return True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", 8000)) == 0


_WEB_LOG = _PROJECT_ROOT / "web-server.log"


def _launch_web() -> None:
    global _web_proc
    if _web_is_running():
        state.console.print(f"[{state.T['warning']}]Restarting web server…[/{state.T['warning']}]")
        if _web_proc is not None:
            _web_proc.terminate()
            _web_proc.wait()
        else:
            # fuser is Linux-only; on Windows we skip the kill (rare edge case)
            if sys.platform != "win32":
                subprocess.run(["fuser", "-k", "8000/tcp"], capture_output=True)
        import time
        time.sleep(0.8)
    log_fh = open(_WEB_LOG, "w")
    _web_proc = subprocess.Popen(
        [sys.executable, str(_PROJECT_ROOT / "web" / "launcher.py"), "--no-browser"],
        stdin=subprocess.DEVNULL,
        stdout=log_fh,
        stderr=log_fh,
    )
    import time
    time.sleep(1.5)
    if _web_proc.poll() is not None:
        log_fh.flush()
        log = _WEB_LOG.read_text().strip()
        state.console.print(f"[{state.T['error']}]✗  Web server failed to start.[/{state.T['error']}]")
        if log:
            state.console.print(f"[{state.T['error']}]{log}[/{state.T['error']}]")
        state.console.print(f"[grey62]Full log: {_WEB_LOG}[/grey62]")
        return
    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Web version ready at {_WEB_URL}")
    opened = webbrowser.open_new_tab(_WEB_URL)
    if not opened:
        state.console.print(f"[grey62]  Could not open browser automatically — navigate to {_WEB_URL} manually.[/grey62]")
    else:
        state.console.print(f"[grey62]  Tab opening in Firefox. If it doesn't appear, check other workspaces or navigate to {_WEB_URL}.[/grey62]")


def rebuild_manual_if_stale() -> None:
    """Silently regenerate user-manual.html if the markdown source is newer."""
    md   = _PROJECT_ROOT / "user-manual.md"
    html = _PROJECT_ROOT / "user-manual.html"
    if not md.exists():
        return
    if html.exists() and html.stat().st_mtime >= md.stat().st_mtime:
        return
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "build_manual", _PROJECT_ROOT / "scripts" / "build_manual.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
    except Exception:
        pass


def _open_manual() -> None:
    global _manual_opened
    rebuild_manual_if_stale()
    manual = _PROJECT_ROOT / "user-manual.html"
    if not manual.exists():
        state.console.print(f"[{state.T['error']}]User manual not found: {manual}[/{state.T['error']}]")
        return
    webbrowser.open(manual.as_uri())
    _manual_opened = True
    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] User Manual opened in your default browser.")


_load_theme()

_first_menu_visit = True


def _run_menu() -> None:
    """Top-level menu loop."""
    global _first_menu_visit
    while True:
        diet_label = _DIET_LABELS.get(state._diet_pref, state._diet_pref)
        state.console.print()
        _W = min(100, state.console.width)
        state.console.print(f"[{state.T['accent']}]NutriMagnus Menu[/{state.T['accent']}]")
        state.console.print(Rule(), width=_W)
        state.console.print(f"  [{state.T['accent']}]1.[/{state.T['accent']}] [bold]Foods[/bold]")
        state.console.print("     [grey62]search · analyze · compare · annotate · pantry · cache · custom profiles[/grey62]")
        state.console.print(f"  [{state.T['accent']}]2.[/{state.T['accent']}] [bold]Recipes[/bold]")
        state.console.print("     [grey62]create · browse/manage · develop (add/remove ingredients with nutritional feedback)[/grey62]")
        state.console.print(f"  [{state.T['accent']}]3.[/{state.T['accent']}] [bold]Meals & Log[/bold]")
        state.console.print("     [grey62]log meal · view/edit by date · analyze · delete[/grey62]")
        state.console.print(f"  [{state.T['accent']}]4.[/{state.T['accent']}] [bold]Analysis[/bold]")
        state.console.print("     [grey62]daily summary · food use in meals[/grey62]")
        state.console.print(f"  [grey62]5.[/grey62] [bold]Settings[/bold]  [grey62](theme · user profile · dietary preferences · API key · DB path)[/grey62]")
        if _web_is_running():
            state.console.print(f"  [{state.T['success']}]w.[/{state.T['success']}] Web version  [grey62](running at {_WEB_URL} — opens new tab)[/grey62]")
        else:
            state.console.print("  [grey62]w.[/grey62] Launch web version")
        state.console.print("  [grey62]m.[/grey62] Open User Manual in browser")
        state.console.print("  [grey62]q.[/grey62] Quit")
        state.console.print()
        state.console.print("  [grey62]Ctrl+C at any prompt — cancel and go back up menu tree[/grey62]")
        if _first_menu_visit:
            state.console.print()
            state.console.print("  [grey62]Type [bold]?[/bold] or [bold]?help[/bold] at any prompt to list built-in help topics.[/grey62]")
            state.console.print("  [grey62]Wherever it is relevant, a tip appears below the output — e.g.[/grey62]")
            state.console.print("  [grey62]  \"At any prompt, type ?diaas or ?dcp for help with these topics.\"[/grey62]")
            state.console.print("  [grey62]Type that ?topic at the next prompt to read the explanation inline.[/grey62]")
            _first_menu_visit = False
        else:
            state.console.print("  [grey62]?help at any prompt  — show available help topics[/grey62]")
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
                if not _menu_analysis():
                    break
            elif choice == "5":
                if not _menu_settings():
                    break
            elif choice == "w":
                _launch_web()
            elif choice == "m":
                _open_manual()
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
    state.console.print('[bold green]NutriMagnus[/bold green] [grey62]("nutrition wizard")[/grey62]')
    from version import VERSION
    state.console.print(f"Nutritional Analysis for individuals and families - version {VERSION}", highlight=False)
    if p:
        profile_label = (
            f"[bold]{p.name}[/bold] — "
            f"age {p.age}, {p.sex},"
            f" {_profile.format_weight(p.weight_kg, p.weight_unit)},"
            f" {_profile.format_height(p.height_cm, p.height_unit)},"
            f" {_profile.ACTIVITY_LABELS.get(p.activity_level, p.activity_level)}"
        )
    else:
        profile_label = "not set -- configure under Settings -> Manage profiles"

    state.console.print()
    state.console.print(f"[grey62]Color theme: {state._current_theme_name}  ({source}) -- change via Settings[/grey62]")
    state.console.print(f"[grey62]Dietary preferences: {diet_label} -- change via Settings[/grey62]")
    state.console.print(f"[grey62]Active profile: {profile_label}[/grey62]", highlight=False)


def run_app(*, theme: str | None = None, api_key: str | None = None) -> None:
    if not initialize_app(theme=theme, api_key=api_key):
        return
    if getattr(state, "_display_program_settings", False):
        print_startup_banner()
    try:
        _run_menu()
    except SystemExit:
        pass
    state.console.print()
    state.console.print("[grey62]NutriMagnus ending…[/grey62]")
    if _web_is_running():
        state.console.print("[grey62]Web version runs until its tab is closed.[/grey62]")
    if _manual_opened:
        state.console.print("[grey62]User Manual remains in browser window until its tab is closed.[/grey62]")
    state.console.print("\n[bold]Happy eating![/bold]\n")
