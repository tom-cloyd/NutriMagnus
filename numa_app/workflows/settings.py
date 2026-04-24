"""
settings.py — Settings menu: color theme, user profile, dietary preferences, DIAAS overrides, API key.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/settings.py — settings menu, profile, and RDA"
"""
import pathlib

from rich.table import Table

import db as _db
import diaas as _diaas
import profile as _profile
import usda as _usda
from .. import state
from ..config import prefs as prefs_config
from ..config.prefs import _save_prefs, _DIET_LABELS
from ..config import theme as theme_config
from ..config.theme import _change_theme
from ..ui.common import _safe_call, _show_menu, table_title, table_footer
from ..ui.prompts import Cancelled, ReturnToMain, _prompt

def _do_diaas_overrides() -> None:
    """Manage per-food protein digestibility overrides for DIAAS calculation."""
    table_title("Protein Digestibility Overrides")
    state.console.print(
        "  [dim]Set a specific true ileal digestibility coefficient (0.0–1.0) for a food,\n"
        "  overriding the curated or estimated value numa uses in meal-level DIAAS\n"
        "  calculations. Values should come from published nutrition studies.[/dim]",
        highlight=False,
    )
    while True:
        with _db.get_db() as conn:
            rows = _diaas.diaas_override_list(conn)

        if rows:
            _OV_W = 38
            tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl.add_column("Food name",      min_width=_OV_W, max_width=_OV_W, no_wrap=True)
            tbl.add_column("Digestibility",  justify="right", min_width=14)
            tbl.add_column("Notes",          min_width=20)
            for r in rows:
                fname = r["food_name"][:_OV_W - 1]
                fdots = "·" * (_OV_W - len(fname) - 1)
                tbl.add_row(
                    f"{fname} [dim]{fdots}[/dim]",
                    f"{r['digestibility']:.2f}",
                    r["notes"] or "",
                )
            state.console.print(tbl, highlight=False)
        else:
            state.console.print("  [dim](No overrides set.)[/dim]")

        state.console.print(
            f"\n  [{state.T['accent']}]a.[/{state.T['accent']}] Add / update override"
            f"  [{state.T['accent']}]d.[/{state.T['accent']}] Delete override"
            f"  [dim]b.[/dim] Back"
            f"  [dim]m.[/dim] Return to main menu"
        )
        try:
            act = _prompt("Action").strip().lower()
        except Cancelled:
            return

        if act == "a":
            try:
                food_name = _prompt("Food name (exact, case-insensitive)").strip()
            except Cancelled:
                continue
            if not food_name:
                continue
            # Show what numa would use without an override
            dig, src = _diaas.get_digestibility(food_name)
            state.console.print(f"  [dim]Current value: {dig:.2f}  ({src})[/dim]")
            try:
                raw = _prompt("Digestibility (0.00–1.00)").strip()
            except Cancelled:
                continue
            try:
                val = float(raw)
                if not 0.0 <= val <= 1.0:
                    raise ValueError
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Enter a number between 0.00 and 1.00.[/{state.T['warning']}]")
                continue
            try:
                notes = _prompt("Notes / source  (Enter to skip)", default="").strip()
            except Cancelled:
                notes = ""
            with _db.get_db() as conn:
                _diaas.diaas_override_set(conn, food_name, val, notes or None)
            state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Override saved for '{food_name}'.")

        elif act == "d":
            try:
                food_name = _prompt("Food name to remove").strip()
            except Cancelled:
                continue
            if not food_name:
                continue
            with _db.get_db() as conn:
                removed = _diaas.diaas_override_delete(conn, food_name)
            if removed:
                state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Removed override for '{food_name}'.")
            else:
                state.console.print(f"[{state.T['warning']}]No override found for '{food_name}'.[/{state.T['warning']}]")

        elif act in ("b", ""):
            return
        elif act == "m":
            raise ReturnToMain()
        else:
            state.console.print(f"[{state.T['warning']}]Enter a, d, b, or m.[/{state.T['warning']}]")


def _do_user_profile() -> None:
    """Interactive flow to set or update the user profile."""
    current = _profile.load_profile()
    _act_keys = list(_profile.ACTIVITY_LEVELS.keys())

    if current:
        w_str = _profile.format_weight(current.weight_kg, current.weight_unit)
        h_str = _profile.format_height(current.height_cm, current.height_unit)
        state.console.print(
            f"\n  [{state.T['hi']}]Current profile:[/{state.T['hi']}]"
            f"  Age {current.age}  ·  {current.sex}"
            f"  ·  {w_str}  ·  {h_str}"
            f"  ·  {_profile.ACTIVITY_LABELS.get(current.activity_level, current.activity_level)}"
            f"\n  [dim]Press Enter at any prompt to keep the current value.[/dim]",
            highlight=False,
        )
    else:
        state.console.print(f"\n  [dim]No profile set. Enter your details to get personalized RDA targets.[/dim]")

    state.console.print()
    try:
        # Age
        while True:
            default_age = str(current.age) if current else ""
            raw = _prompt("Age (years)", default=default_age).strip()
            if not raw and current:
                age = current.age
                break
            try:
                age = int(raw)
                if 1 <= age <= 120:
                    break
            except ValueError:
                pass
            state.console.print(f"[{state.T['warning']}]Enter a whole number (e.g. 35).[/{state.T['warning']}]")

        # Sex
        state.console.print(
            f"  [{state.T['accent']}]m[/{state.T['accent']}] Male  "
            f"[{state.T['accent']}]f[/{state.T['accent']}] Female  "
            f"[{state.T['accent']}]o[/{state.T['accent']}] Other / prefer not to say"
        )
        _sex_map = {"m": "male", "f": "female", "o": "other",
                    "male": "male", "female": "female", "other": "other"}
        while True:
            default_sex = current.sex[0] if current else ""
            raw = _prompt("Sex  [dim](m / f / o)[/dim]", default=default_sex).strip().lower()
            if not raw and current:
                sex = current.sex
                break
            sex = _sex_map.get(raw)
            if sex:
                break
            state.console.print(f"[{state.T['warning']}]Enter m, f, or o.[/{state.T['warning']}]")

        # Weight — accepts kg or lb
        weight_unit = current.weight_unit if current else "kg"
        if current:
            default_w = _profile.format_weight(current.weight_kg, current.weight_unit)
        else:
            default_w = ""
        while True:
            raw = _prompt(
                "Weight  [dim](kg or lb, e.g. 80 kg  or  176 lbs)[/dim]",
                default=default_w,
            ).strip()
            if not raw and current:
                weight_kg = current.weight_kg
                break
            kg_val, detected_unit = _profile.parse_weight(raw)
            if kg_val is not None and 20.0 <= kg_val <= 500.0:
                weight_kg = kg_val
                weight_unit = detected_unit
                break
            state.console.print(
                f"[{state.T['warning']}]Enter weight with unit, e.g.  80 kg  or  176 lbs[/{state.T['warning']}]"
            )

        # Height — accepts cm or feet+inches
        height_unit = current.height_unit if current else "cm"
        if current:
            default_h = _profile.format_height(current.height_cm, current.height_unit)
        else:
            default_h = ""
        while True:
            raw = _prompt(
                "Height  [dim](cm or ft+in, e.g. 178 cm  or  5'10\")[/dim]",
                default=default_h,
            ).strip()
            if not raw and current:
                height_cm = current.height_cm
                break
            cm_val, detected_unit = _profile.parse_height(raw)
            if cm_val is not None and 50.0 <= cm_val <= 280.0:
                height_cm = cm_val
                height_unit = detected_unit
                break
            state.console.print(
                f"[{state.T['warning']}]Enter height as cm (e.g. 178) or feet+inches (e.g. 5'10\")[/{state.T['warning']}]"
            )

        # Activity level
        state.console.print()
        for i, (key, label) in enumerate(_profile.ACTIVITY_LABELS.items(), 1):
            state.console.print(f"  [{state.T['accent']}]{i}[/{state.T['accent']}]  {label}")
        while True:
            default_act = str(_act_keys.index(current.activity_level) + 1) if current else ""
            raw = _prompt(f"Activity level  [dim](1–{len(_act_keys)})[/dim]",
                          default=default_act).strip()
            if not raw and current:
                activity_level = current.activity_level
                break
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(_act_keys):
                    activity_level = _act_keys[idx]
                    break
            except ValueError:
                pass
            state.console.print(f"[{state.T['warning']}]Enter a number 1–{len(_act_keys)}.[/{state.T['warning']}]")

    except Cancelled:
        state.console.print("[dim]Cancelled — profile unchanged.[/dim]")
        return

    new_profile = _profile.UserProfile(
        age=age, sex=sex, weight_kg=weight_kg,
        height_cm=height_cm, activity_level=activity_level,
        weight_unit=weight_unit, height_unit=height_unit,
    )
    _profile.save_profile(new_profile)
    rda = _profile.compute_rda(new_profile)
    cal = int(rda["calories"][0])
    prot = rda["protein_g"][0]
    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}] Profile saved."
        f"  Estimated calorie target: [{state.T['hi']}]{cal} kcal[/{state.T['hi']}]"
        f"  ·  Protein minimum: [{state.T['hi']}]{prot} g[/{state.T['hi']}]",
        highlight=False,
    )


def _do_dietary_prefs() -> None:
    """Set the dietary preference for protein complement suggestions."""
    current_label = _DIET_LABELS.get(state._diet_pref, state._diet_pref)
    state.console.print(f"\n  Current setting: [bold]{current_label}[/bold]")
    state.console.print(
        f"\n  [{state.T['accent']}]1[/{state.T['accent']}] — All animal foods  [dim](meat, fish, dairy, eggs)[/dim]"
        f"\n  [{state.T['accent']}]2[/{state.T['accent']}] — Vegetarian  [dim](dairy + eggs only)[/dim]"
        f"\n  [{state.T['accent']}]3[/{state.T['accent']}] — Plant-based only"
        f"\n  [dim]Enter — keep current[/dim]"
    )
    try:
        ans = _prompt("Change to?  [dim](1 / 2 / 3 / Enter)[/dim]", default="").strip()
    except Cancelled:
        return
    pref = {"1": "all", "2": "vegetarian", "3": "plant_only"}.get(ans)
    if pref is None:
        return
    state.set_diet_pref(pref)
    _save_prefs()
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {_DIET_LABELS[pref]}.")




def _get_editor_command() -> str:
    return str(getattr(state, "_editor_command", "") or "").strip() or "system default"


def _do_editor_command() -> None:
    current = str(getattr(state, "_editor_command", "") or "").strip()
    state.console.print(
        f"\n  [dim]The editor command is used when editing long text fields.\n"
        f"  If unset, the system default ($VISUAL / $EDITOR) is used.\n"
        f"  Use '-' to clear back to system default.[/dim]\n"
    )
    try:
        new_val = _prompt(
            "Editor command  [dim](e.g. nano, vim, code --wait — Enter to keep, '-' to clear)[/dim]",
            default=current
        ).strip()
    except Cancelled:
        return
    if new_val == "-":
        new_val = ""
    setattr(state, "_editor_command", new_val)
    _save_prefs()
    label = new_val if new_val else "system default"
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Editor command saved: {label}.")


def _do_launch_display_setting() -> None:
    current = "y" if bool(getattr(state, "_display_program_settings", False)) else "n"
    try:
        raw = _prompt("Display program settings at program launch?  [dim](y|n)[/dim]", default=current).strip().lower()
    except Cancelled:
        return
    if raw not in ("", "y", "n"):
        state.console.print(f"[{state.T['warning']}]Please enter y or n.[/{state.T['warning']}]")
        return
    setattr(state, "_display_program_settings", raw == "y")
    _save_prefs()
    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Launch display setting saved.")

def _menu_advanced_settings() -> None:
    while True:
        key_status = "set" if _usda.get_api_key() else "[bold yellow]not set[/bold yellow]"
        _show_menu("Advanced settings", [
            ("1", "Protein digestibility overrides  (for DIAAS calculation)"),
            ("2", f"USDA API key  ({key_status})"),
            ("3", f"Storage location: {_db.get_db_path()}"),
            ("b", "Back to previous menu"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return
        if choice == "1":
            _safe_call(_do_diaas_overrides)
        elif choice == "2":
            _safe_call(_do_set_api_key)
        elif choice == "3":
            state.console.print(f"  Storage location: {_db.get_db_path()}", highlight=False)
        elif choice == "b":
            return
        elif choice == "m":
            raise ReturnToMain()
        elif choice == "q":
            raise SystemExit(0)
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")

def _menu_settings() -> bool:
    """Settings submenu. Returns True to go back, False to quit."""
    while True:
        diet_status = _DIET_LABELS.get(state._diet_pref, state._diet_pref)
        p = _profile.load_profile()
        if p:
            profile_status = (
                f"age {p.age}, {p.sex},"
                f" {_profile.format_weight(p.weight_kg, p.weight_unit)},"
                f" {_profile.format_height(p.height_cm, p.height_unit)}"
            )
        else:
            profile_status = "[bold yellow]not set[/bold yellow]"
        editor_status = _get_editor_command()
        launch_status = "yes" if bool(getattr(state, "_display_program_settings", False)) else "no"

        _show_menu("Settings", [
            ("1", f"Color theme  (current setting: {state._current_theme_name})"),
            ("2", f"User profile  (current setting: {profile_status})"),
            ("3", f"Dietary preferences  (current setting: {diet_status})"),
            ("4", f"Editor command  (current setting: {editor_status})"),
            ("5", f"Display program settings at launch  (current setting: {launch_status})"),
            ("6", "Advanced settings  [dim](API key, storage, protein overrides)[/dim]"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[dim]Cancelled.[/dim]")
            return True

        if choice == "1":
            _safe_call(_change_theme)
        elif choice == "2":
            _safe_call(_do_user_profile)
        elif choice == "3":
            _safe_call(_do_dietary_prefs)
        elif choice == "4":
            _safe_call(_do_editor_command)
        elif choice == "5":
            _safe_call(_do_launch_display_setting)
        elif choice == "6":
            _safe_call(_menu_advanced_settings)
        elif choice == "m":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")

def _do_set_api_key() -> None:
    current = _usda.get_api_key()
    if current:
        state.console.print(f"  Current key: [dim]{current[:8]}...{current[-4:]}[/dim]")
    try:
        key = _prompt("New API key (Enter to keep current)", default="").strip()
    except Cancelled:
        return
    if key:
        _usda.set_api_key(key)
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] API key saved.")
    else:
        state.console.print("[dim]Unchanged.[/dim]")
