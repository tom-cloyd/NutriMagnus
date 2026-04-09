import json
import pathlib

from rich.table import Table

import db as _db
import diaas as _diaas
import profile as _profile
import usda as _usda
from .. import state
from ..config import prefs as prefs_config
from ..config.prefs import _PREFS_FILE, _save_prefs
from ..config import theme as theme_config
from ..config.theme import _change_theme
from ..ui.common import _safe_call, _show_menu
from ..ui.prompts import Cancelled, _prompt

def _do_diaas_overrides() -> None:
    """Manage per-food protein digestibility overrides for DIAAS calculation."""
    state.console.print(
        f"\n  [{state.T['hi']}]Protein digestibility overrides[/{state.T['hi']}]"
        f"\n  [dim]These let you set a specific true ileal digestibility coefficient "
        f"(0.0–1.0) for a food,\n  overriding the curated or estimated value numa "
        f"uses in meal-level DIAAS calculations.\n  Values come from published "
        f"nutrition studies — see the calculation notes for sources.[/dim]",
        highlight=False,
    )
    while True:
        with _db.get_db() as conn:
            rows = _diaas.diaas_override_list(conn)

        if rows:
            tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl.add_column("Food name",      min_width=34)
            tbl.add_column("Digestibility",  justify="right", min_width=14)
            tbl.add_column("Notes",          min_width=20)
            for r in rows:
                tbl.add_row(
                    r["food_name"],
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
        )
        try:
            act = _prompt("Choice").strip().lower()
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
                notes = _prompt("Notes / source  [Enter=skip]", default="").strip()
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
        else:
            state.console.print(f"[{state.T['warning']}]Enter a, d, or b.[/{state.T['warning']}]")


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
            raw = _prompt("Sex  [m=male · f=female · o=other]", default=default_sex).strip().lower()
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


def _print_rda_comparison(nutrients: dict[str, float], profile: "_profile.UserProfile") -> None:
    """Print a table comparing daily nutrient totals against personalized RDA targets."""
    rda = _profile.compute_rda(profile)
    nutrient_label = _usda.nutrient_label  # (key) → (label, unit) | None

    state.console.print(f"\n[{state.T['accent']}]Daily Intake vs. Recommended Values[/{state.T['accent']}]")
    state.console.rule()
    state.console.print(
        f"  Profile: age {profile.age}  ·  {profile.sex}"
        f"  ·  {_profile.format_weight(profile.weight_kg, profile.weight_unit)}"
        f"  ·  {_profile.format_height(profile.height_cm, profile.height_unit)}"
        f"  ·  {_profile.ACTIVITY_LABELS.get(profile.activity_level, profile.activity_level)}\n",
        highlight=False,
    )

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Nutrient",  min_width=26)
    tbl.add_column("Intake",    justify="right", min_width=12)
    tbl.add_column("Target",    justify="right", min_width=12)
    tbl.add_column("% of RDA",  justify="right", min_width=10)
    tbl.add_column("Status",    min_width=28)

    BAR_WIDTH = 16

    for key, (rda_val, unit, rda_type) in rda.items():
        intake = nutrients.get(key, 0.0)
        label_info = nutrient_label(key)
        label = label_info[0] if label_info else key.replace("_", " ").title()

        if rda_val and rda_val > 0:
            pct = (intake / rda_val) * 100.0
        else:
            pct = 0.0

        # Format intake and target
        if unit in ("kcal", "g"):
            intake_str = f"{intake:.1f} {unit}"
            target_str = f"{rda_val:.1f} {unit}"
        else:
            intake_str = f"{intake:.1f} {unit}"
            target_str = f"{rda_val:.1f} {unit}"
        pct_str = f"{pct:.0f}%"

        # Status bar and color
        if rda_type == "limit":
            # For limits: green if under, yellow if near (80-100%), red if over
            if pct <= 80:
                bar_color = state.T["success"]
                status_note = "within limit"
            elif pct <= 100:
                bar_color = state.T["warning"]
                status_note = "approaching limit"
            else:
                bar_color = state.T["error"]
                status_note = f"over limit by {pct - 100:.0f}%"
            filled = min(int(BAR_WIDTH * min(pct, 200) / 200), BAR_WIDTH)
        else:
            # For minimums/targets: red < 70%, yellow 70-99%, green 100%+
            if pct >= 100:
                bar_color = state.T["success"]
                status_note = "met"
            elif pct >= 70:
                bar_color = state.T["warning"]
                status_note = f"{100 - pct:.0f}% short"
            else:
                bar_color = state.T["error"]
                status_note = f"{100 - pct:.0f}% short"
            filled = min(int(BAR_WIDTH * min(pct, 100) / 100), BAR_WIDTH)

        bar = f"[{bar_color}]{'█' * filled}[/{bar_color}]{'░' * (BAR_WIDTH - filled)}"
        status_cell = f"{bar}  [{bar_color}]{status_note}[/{bar_color}]"

        tbl.add_row(label, intake_str, target_str, pct_str, status_cell)

    state.console.print(tbl, highlight=False)
    state.console.print(
        "  [dim]Target = RDA or Adequate Intake  ·  Limit = Tolerable Upper Intake Level[/dim]\n"
    )



def _get_editor_command() -> str:
    editor_value = str(getattr(state, "_editor_command", "") or "").strip()
    if editor_value:
        return editor_value
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            editor_value = str(data.get("editor_command", "") or "").strip()
            if editor_value:
                setattr(state, "_editor_command", editor_value)
                return editor_value
    except Exception:
        pass
    return ""


def _save_editor_command(value: str) -> None:
    value = str(value or "").strip()
    setattr(state, "_editor_command", value)
    data: dict = {}
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                data = {}
    except Exception:
        data = {}
    if value:
        data["editor_command"] = value
    else:
        data.pop("editor_command", None)
    _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _PREFS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _do_editor_command() -> None:
    current = _get_editor_command()
    current_label = current if current else "system default"
    state.console.print(
        f"\n  Current editor: [{state.T['hi']}]{current_label}[/{state.T['hi']}]"
    )
    state.console.print(
        "  [dim]Examples: nano, vim, micro, code --wait[/dim]\n"
        "  [dim]Press Enter on a blank value to use the system default editor.[/dim]"
    )
    try:
        raw = _prompt("Editor command", default=current).strip()
    except Cancelled:
        return

    if raw == current:
        state.console.print("[dim]Unchanged.[/dim]")
        return

    _save_editor_command(raw)
    if raw:
        state.console.print(
            f"[{state.T['success']}]✓[/{state.T['success']}] Editor saved: {raw}"
        )
    else:
        state.console.print(
            f"[{state.T['success']}]✓[/{state.T['success']}] Editor cleared. System default will be used."
        )


def _do_dietary_prefs() -> None:
    """Toggle the include_animal_foods preference."""
    current = "animal foods included" if state._include_animal_foods else "plant-based only"
    state.console.print(f"\n  Current setting: [bold]{current}[/bold]")
    state.console.print(
        f"\n  [{state.T['accent']}]y[/{state.T['accent']}] — Include animal foods  "
        f"[{state.T['accent']}]n[/{state.T['accent']}] — Plant-based only  "
        f"[dim]Enter — keep current[/dim]"
    )
    try:
        ans = _prompt("Choice  [y=include animal foods · n=plant-based only · Enter=keep]", default="").strip().lower()
    except Cancelled:
        return
    if ans == "y":
        state.set_include_animal_foods(True)
    elif ans == "n":
        state.set_include_animal_foods(False)
    else:
        return
    _save_prefs()
    label = "animal foods included" if state._include_animal_foods else "plant-based only"
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {label}.")


def _menu_settings() -> bool:
    """Settings submenu. Returns True to go back, False to quit."""
    while True:
        key_status = "set" if _usda.get_api_key() else "[bold yellow]not set[/bold yellow]"
        diet_status = "animal foods included" if state._include_animal_foods else "plant-based only"
        p = _profile.load_profile()
        if p:
            profile_status = (
                f"age {p.age}, {p.sex},"
                f" {_profile.format_weight(p.weight_kg, p.weight_unit)},"
                f" {_profile.format_height(p.height_cm, p.height_unit)}"
            )
        else:
            profile_status = "[bold yellow]not set[/bold yellow]"
        editor_status = _get_editor_command() or "system default"
        _show_menu("Settings", [
            ("1", f"USDA API key  ({key_status})"),
            ("2", f"Color theme  (current setting: {state._current_theme_name})"),
            ("3", f"Database path: {_db.get_db_path()}"),
            ("4", "Protein digestibility overrides  (for DIAAS calculation)"),
            ("5", f"Dietary preferences  (current setting: {diet_status})"),
            ("6", f"User profile  (current setting: {profile_status})"),
            ("7", f"Editor command  (current setting: {editor_status})"),
            ("b", "Back to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[dim]Cancelled.[/dim]")
            return True

        if choice == "1":
            _safe_call(_do_set_api_key)
        elif choice == "2":
            _safe_call(_change_theme)
        elif choice == "3":
            state.console.print(f"  Database: {_db.get_db_path()}", highlight=False)
        elif choice == "4":
            _safe_call(_do_diaas_overrides)
        elif choice == "5":
            _safe_call(_do_dietary_prefs)
        elif choice == "6":
            _safe_call(_do_user_profile)
        elif choice == "7":
            _safe_call(_do_editor_command)
        elif choice == "b":
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
        key = _prompt("New API key  [Enter=keep current]", default="").strip()
    except Cancelled:
        return
    if key:
        _usda.set_api_key(key)
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] API key saved.")
    else:
        state.console.print("[dim]Unchanged.[/dim]")
