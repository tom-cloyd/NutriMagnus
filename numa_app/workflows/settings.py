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
from ..ui.common import _safe_call, _show_menu, table_title, table_footer, help_footer, _prompt_with_options
from ..ui.prompts import Cancelled, ReturnToMain, _prompt, _ask_float
from ..ui.render import _print_rda_targets

# Nutrients offered for Profile Optimal / max-limit configuration in Settings —
# mirrors web/backend.py's _NUTRIENT_TARGET_GROUPS. Every nutrient here is
# settable, not just ones with an established RDA/AI (compute_rda's key set) —
# amino acids, EPA/DHA, and phytonutrients have no official DRI but are still
# valid Optimal target or max-limit candidates (see manual topic ?omega3 for
# why this matters for EPA/DHA specifically).
_NUTRIENT_TARGET_GROUPS: list[tuple[str, list[str]]] = [
    ("Macronutrients", ["calories", "protein_g", "carbs_g", "fiber_g", "sodium_mg",
                         "omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg"]),
    ("Minerals", ["calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
                  "potassium_mg", "zinc_mg", "iodine_mcg", "selenium_mcg"]),
    ("Vitamins", ["vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
                  "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
                  "b6_mg", "folate_mcg", "b12_mcg", "choline_mg"]),
    ("Phytonutrients", ["beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
                        "lutein_zeaxanthin_mcg", "beta_sitosterol_mg", "isoflavones_mg"]),
    ("Amino Acids", ["aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
                     "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
                     "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g"]),
]


def _do_diaas_overrides() -> None:
    """Manage per-food protein digestibility overrides for DIAAS calculation."""
    table_title("PROTEIN DIGESTIBILITY OVERRIDES")
    state.console.print(
        "  [grey62]Set a specific true ileal digestibility coefficient (0.0–1.0) for a food,\n"
        "  overriding the curated or estimated value numa uses in meal-level DIAAS\n"
        "  calculations. Values should come from published nutrition studies.[/grey62]",
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
                    f"{fname} [grey62]{fdots}[/grey62]",
                    f"{r['digestibility']:.2f}",
                    r["notes"] or "",
                )
            state.console.print(tbl, highlight=False)
            help_footer("dcp-overrides")
        else:
            state.console.print("  [grey62](No overrides set.)[/grey62]")

        state.console.print(
            f"\n  [{state.T['accent']}]a.[/{state.T['accent']}] Add / update override"
            f"  [{state.T['accent']}]d.[/{state.T['accent']}] Delete override"
            f"  [grey62]b.[/grey62] Back"
            f"  [grey62]m.[/grey62] Return to main menu"
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
            state.console.print(f"  [grey62]Current value: {dig:.2f}  ({src})[/grey62]")
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


def _do_user_profile(profile_name: str | None = None) -> None:
    """Interactive flow to create or edit a named profile.
    profile_name=None edits the active profile; pass a name to edit a specific one."""
    current = _profile.load_profile(profile_name)
    _act_keys = list(_profile.ACTIVITY_LEVELS.keys())

    if current:
        w_str = _profile.format_weight(current.weight_kg, current.weight_unit)
        h_str = _profile.format_height(current.height_cm, current.height_unit)
        state.console.print(
            f"\n  [{state.T['hi']}]Editing profile:[/{state.T['hi']}]  [bold]{current.name}[/bold]"
            f"  ·  Age {current.age}  ·  {current.sex}"
            f"  ·  {w_str}  ·  {h_str}"
            f"  ·  {_profile.ACTIVITY_LABELS.get(current.activity_level, current.activity_level)}"
            f"\n  [grey62]Press Enter at any prompt to keep the current value.[/grey62]",
            highlight=False,
        )
    else:
        state.console.print(f"\n  [grey62]Creating new profile. Enter your details to get personalized RDA targets.[/grey62]")

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
            raw = _prompt("Sex  [grey62](m / f / o)[/grey62]", default=default_sex).strip().lower()
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
                "Weight  [grey62](kg or lb, e.g. 80 kg  or  176 lbs)[/grey62]",
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
                "Height  [grey62](cm or ft+in, e.g. 178 cm  or  5'10\")[/grey62]",
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
            raw = _prompt(f"Activity level  [grey62](1–{len(_act_keys)})[/grey62]",
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
        state.console.print("[grey62]Cancelled — profile unchanged.[/grey62]")
        return

    saved_name = (current.name if current else None) or profile_name or _profile.get_active_profile_name()
    new_profile = _profile.UserProfile(
        age=age, sex=sex, weight_kg=weight_kg,
        height_cm=height_cm, activity_level=activity_level,
        weight_unit=weight_unit, height_unit=height_unit,
        name=saved_name,
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


def _profile_summary(p: "_profile.UserProfile") -> str:
    return (
        f"age {p.age}, {p.sex},"
        f" {_profile.format_weight(p.weight_kg, p.weight_unit)},"
        f" {_profile.format_height(p.height_cm, p.height_unit)},"
        f" {_profile.ACTIVITY_LABELS.get(p.activity_level, p.activity_level)}"
    )


def _do_manage_profiles() -> None:
    """Profile management: list, switch, create, edit, rename, delete."""
    _NW = 24
    while True:
        names = _profile.list_profiles()
        active = _profile.get_active_profile_name()

        table_title("PROFILES")
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",       justify="right", min_width=3)
        tbl.add_column("Active",  justify="center", min_width=6)
        tbl.add_column("Name",    min_width=_NW)
        tbl.add_column("Summary", min_width=40)

        profiles: list[tuple[str, "_profile.UserProfile | None"]] = []
        for nm in names:
            p = _profile.load_profile(nm)
            profiles.append((nm, p))
            mark = f"[{state.T['success']}]✓[/{state.T['success']}]" if nm == active else ""
            summary = _profile_summary(p) if p else "[grey62]unreadable[/grey62]"
            tbl.add_row(str(len(profiles)), mark, nm, summary)

        state.console.print(tbl)
        if not names:
            state.console.print("  [grey62]No profiles yet. Enter 'n' to create one.[/grey62]")

        state.console.print()
        state.console.print(f"  [{state.T['hi']}]Options:[/{state.T['hi']}]")
        state.console.print( "    [bold]s[/bold]#   Switch active profile         [grey62](e.g. s2)[/grey62]")
        state.console.print( "    [bold]n[/bold]    New profile")
        state.console.print( "    [bold]e[/bold]#   Edit profile                  [grey62](e.g. e1)[/grey62]")
        state.console.print( "    [bold]r[/bold]#   Rename profile                [grey62](e.g. r2)[/grey62]")
        state.console.print( "    [bold]d[/bold]#   Delete profile                [grey62](e.g. d3)[/grey62]")
        state.console.print( "    [grey62]Enter=refresh  b=back  m=main  q=quit[/grey62]")

        try:
            raw = _prompt("  Command", free_text=True).strip().lower()
        except Cancelled:
            return

        if not raw or raw == "l":
            continue
        if raw in ("b", "q", "m"):
            if raw == "m":
                raise ReturnToMain()
            if raw == "q":
                raise SystemExit(0)
            return

        cmd = raw[0]
        rest = raw[1:].strip()

        def _parse_idx(s: str) -> int | None:
            try:
                i = int(s) - 1
                return i if 0 <= i < len(profiles) else None
            except ValueError:
                return None

        if cmd == "s" and rest:
            idx = _parse_idx(rest)
            if idx is None:
                state.console.print(f"[{state.T['warning']}]Enter a list number after s (e.g. s2).[/{state.T['warning']}]")
                continue
            nm = profiles[idx][0]
            _profile.set_active_profile_name(nm)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Active profile set to [bold]{nm}[/bold].")

        elif cmd == "n":
            try:
                new_name = _prompt("  New profile name", free_text=True).strip()
            except Cancelled:
                continue
            if not new_name:
                continue
            if new_name in names:
                state.console.print(f"[{state.T['warning']}]A profile named '{new_name}' already exists.[/{state.T['warning']}]")
                continue
            # Build a blank profile with just the name pre-set, then open editor
            blank = _profile.UserProfile(
                age=30, sex="other", weight_kg=70.0, height_cm=170.0,
                activity_level="moderate", name=new_name,
            )
            _profile.save_profile(blank)
            _do_user_profile(new_name)
            if not names:  # first profile — make it active automatically
                _profile.set_active_profile_name(new_name)
            else:
                try:
                    ans = _prompt(
                        f"  Make [bold]{new_name}[/bold] the active profile?  [grey62](Y/n)[/grey62]",
                        default="y",
                    ).strip().lower()
                except Cancelled:
                    ans = "n"
                if ans != "n":
                    _profile.set_active_profile_name(new_name)

        elif cmd == "e" and rest:
            idx = _parse_idx(rest)
            if idx is None:
                state.console.print(f"[{state.T['warning']}]Enter a list number after e (e.g. e1).[/{state.T['warning']}]")
                continue
            _do_user_profile(profiles[idx][0])

        elif cmd == "r" and rest:
            idx = _parse_idx(rest)
            if idx is None:
                state.console.print(f"[{state.T['warning']}]Enter a list number after r (e.g. r1).[/{state.T['warning']}]")
                continue
            old_nm = profiles[idx][0]
            try:
                new_nm = _prompt(f"  Rename '{old_nm}' to", free_text=True).strip()
            except Cancelled:
                continue
            if not new_nm or new_nm == old_nm:
                continue
            if new_nm in names:
                state.console.print(f"[{state.T['warning']}]A profile named '{new_nm}' already exists.[/{state.T['warning']}]")
                continue
            if _profile.rename_profile(old_nm, new_nm):
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Renamed '{old_nm}' → '{new_nm}'.")
            else:
                state.console.print(f"[{state.T['error']}]Rename failed.[/{state.T['error']}]")

        elif cmd == "d" and rest:
            idx = _parse_idx(rest)
            if idx is None:
                state.console.print(f"[{state.T['warning']}]Enter a list number after d (e.g. d2).[/{state.T['warning']}]")
                continue
            nm = profiles[idx][0]
            if len(names) <= 1:
                state.console.print(f"[{state.T['warning']}]Cannot delete the only profile.[/{state.T['warning']}]")
                continue
            try:
                confirm = _prompt(
                    f"  Delete profile [bold]{nm}[/bold]? This cannot be undone.  [grey62](y/N)[/grey62]",
                    default="n",
                ).strip().lower()
            except Cancelled:
                continue
            if confirm != "y":
                continue
            _profile.delete_profile(nm)
            if active == nm:
                remaining = [n for n in names if n != nm]
                _profile.set_active_profile_name(remaining[0])
                state.console.print(
                    f"  [{state.T['success']}]✓[/{state.T['success']}]  Deleted '{nm}'."
                    f"  Active profile switched to [bold]{remaining[0]}[/bold]."
                )
            else:
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Deleted '{nm}'.")

        else:
            state.console.print(f"[{state.T['warning']}]Unrecognized command. Use s#, n, e#, r#, d#, or b.[/{state.T['warning']}]")


def _do_view_goals() -> None:
    """Display the user's personalized daily nutrient targets."""
    profile = _profile.load_profile()
    if not profile:
        state.console.print(
            "\n  [grey62]No profile set. Go to Settings → User profile to set your details.[/grey62]"
        )
        return
    _print_rda_targets(profile)


def _load_recommended_optimal_defaults(profile: "_profile.UserProfile") -> None:
    """Apply profile.compute_optimal_defaults() to any nutrient the user hasn't
    already customized, save, and report what changed."""
    defaults = _profile.compute_optimal_defaults(profile)
    applied: list[str] = []
    for key, val in defaults.items():
        if key in profile.optimal_targets:
            continue
        profile.optimal_targets[key] = val
        applied.append(key)

    if not applied:
        state.console.print(
            f"\n  [grey62]All recommended nutrients already have a custom Optimal target — nothing to load.[/grey62]"
        )
        return

    _profile.save_profile(profile)
    state.console.print(f"\n  [{state.T['success']}]✓ Loaded recommended optimal targets:[/{state.T['success']}]")
    for key in applied:
        label, unit = _usda.nutrient_label(key)
        state.console.print(f"    {label}: {defaults[key]:.1f} {unit}", highlight=False)
    state.console.print(
        "\n  [grey62]These are commonly-cited general guidance, not personalized medical advice —"
        " review and adjust any of them individually below.[/grey62]"
    )


def _do_nutrient_targets() -> None:
    """Manage per-nutrient Profile Optimal targets and custom max limits."""
    profile = _profile.load_profile()
    if not profile:
        state.console.print(
            "\n  [grey62]No profile set. Go to Settings → User profile to set your details.[/grey62]"
        )
        return

    groups = _NUTRIENT_TARGET_GROUPS

    while True:
        state.console.print()
        table_title("Nutrient targets",
                     "custom Profile Optimal targets and max limits, layered on top of your standard RDA")
        idx = 1
        numbered: dict[str, str] = {}
        for group_name, keys in groups:
            present = list(keys)
            if not present:
                continue
            state.console.print(f"\n  [{state.T['hi']}]{group_name}[/{state.T['hi']}]")
            for key in present:
                label, unit = _usda.nutrient_label(key)
                opt = profile.optimal_targets.get(key)
                lim = profile.max_limits.get(key)
                opt_str = f"{opt:.1f} {unit}" if opt is not None else "–"
                lim_str = f"{lim:.1f} {unit}" if lim is not None else "–"
                state.console.print(
                    f"    [{state.T['accent']}]{idx:>2}[/{state.T['accent']}]  {label:<24}"
                    f" optimal: {opt_str:<12} max limit: {lim_str}",
                    highlight=False,
                )
                numbered[str(idx)] = key
                idx += 1

        state.console.print()
        try:
            choice = _prompt(
                "Nutrient #  [grey62](Enter/b=back, l=load recommended optimal targets)[/grey62]",
                default="",
            ).strip()
        except Cancelled:
            return
        if not choice or choice.lower() in ("b", "m", "q"):
            return
        if choice.lower() == "l":
            _load_recommended_optimal_defaults(profile)
            continue
        key = numbered.get(choice)
        if key is None:
            state.console.print(f"[{state.T['warning']}]Unrecognized number.[/{state.T['warning']}]")
            continue

        label, unit = _usda.nutrient_label(key)
        try:
            field = _prompt_with_options(
                f"Set what for {label}?",
                [("1", f"Optimal target ({unit})"), ("2", f"Max limit ({unit})"),
                 ("3", "Clear optimal target"), ("4", "Clear max limit")],
                default="",
            )
        except Cancelled:
            continue

        if field == "1":
            val = _ask_float(f"Optimal daily target for {label}, in {unit}")
            if val is not None:
                profile.optimal_targets[key] = val
                _profile.save_profile(profile)
        elif field == "2":
            val = _ask_float(f"Max daily limit for {label}, in {unit}")
            if val is not None:
                profile.max_limits[key] = val
                _profile.save_profile(profile)
        elif field == "3":
            if profile.optimal_targets.pop(key, None) is not None:
                _profile.save_profile(profile)
        elif field == "4":
            if profile.max_limits.pop(key, None) is not None:
                _profile.save_profile(profile)


def _do_dietary_prefs() -> None:
    """Set the dietary preference for protein complement suggestions."""
    current_label = _DIET_LABELS.get(state._diet_pref, state._diet_pref)
    state.console.print(f"\n  Current setting: [bold]{current_label}[/bold]")
    state.console.print(
        f"\n  [{state.T['accent']}]1[/{state.T['accent']}] — All animal foods  [grey62](meat, fish, dairy, eggs)[/grey62]"
        f"\n  [{state.T['accent']}]2[/{state.T['accent']}] — Vegetarian  [grey62](dairy + eggs only)[/grey62]"
        f"\n  [{state.T['accent']}]3[/{state.T['accent']}] — Plant-based only"
        f"\n  [grey62]Enter — keep current[/grey62]"
    )
    try:
        ans = _prompt("Change to?  [grey62](1 / 2 / 3 / Enter)[/grey62]", default="").strip()
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
        f"\n  [grey62]The editor command is used when editing long text fields.\n"
        f"  If unset, the system default ($VISUAL / $EDITOR) is used.\n"
        f"  Use '-' to clear back to system default.[/grey62]\n"
    )
    try:
        new_val = _prompt(
            "Editor command  [grey62](e.g. nano, vim, code --wait — Enter to keep, '-' to clear)[/grey62]",
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


def _do_oxalate_data_setting() -> None:
    """Toggle Harvard oxalate data lookup on/off for the active profile."""
    import oxalate as _ox
    prof = _profile.load_profile()
    if not prof:
        state.console.print(
            "\n  [grey62]No active profile. Create a profile first (Settings → Manage profiles).[/grey62]"
        )
        return
    current = prof.use_oxalate_data
    status = "enabled" if current else "disabled"
    avail = _ox.is_available()
    avail_note = "" if avail else "  [bold yellow](oxalate.db not found — run build_oxalate_db.py)[/bold yellow]"
    state.console.print(
        f"\n  Current setting: [bold]{status}[/bold]{avail_note}\n"
        f"  [grey62]When enabled, numa will look up oxalate content for foods you view or\n"
        f"  use in recipes, using the Harvard School of Public Health oxalate table.\n"
        f"  You will be asked to confirm or reject each match the first time a food\n"
        f"  appears; confirmed links are saved and not repeated.[/grey62]",
        highlight=False,
    )
    try:
        raw = _prompt(
            f"{'Disable' if current else 'Enable'} oxalate data?  [grey62](y/n)[/grey62]",
            choices=["y", "n"],
            default="n",
        ).strip().lower()
    except Cancelled:
        return
    if raw != "y":
        return
    import dataclasses
    new_prof = dataclasses.replace(prof, use_oxalate_data=not current)
    _profile.save_profile(new_prof)
    new_status = "enabled" if new_prof.use_oxalate_data else "disabled"
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Oxalate data {new_status}.")


def _do_launch_display_setting() -> None:
    current = "y" if bool(getattr(state, "_display_program_settings", False)) else "n"
    try:
        raw = _prompt("Display program settings at program launch?  [grey62](y|n)[/grey62]", choices=["y", "n"], default=current)
    except Cancelled:
        return
    setattr(state, "_display_program_settings", raw == "y")
    _save_prefs()
    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Launch display setting saved.")

def _menu_advanced_settings() -> None:
    while True:
        _key = _usda.get_api_key()
        key_status = f"{_key[:8]}...{_key[-4:]}" if _key else "[bold yellow]not set[/bold yellow]"
        _show_menu("Advanced settings", [
            ("1", "Protein digestibility overrides  (for DIAAS calculation)"),
            ("2", f"USDA API key  ({key_status})  [grey62]· s = show full[/grey62]"),
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
                f"[bold]{p.name}[/bold] — "
                f"age {p.age}, {p.sex},"
                f" {_profile.format_weight(p.weight_kg, p.weight_unit)},"
                f" {_profile.format_height(p.height_cm, p.height_unit)}"
            )
            oxalate_status = "on" if p.use_oxalate_data else "off"
        else:
            profile_status = "[bold yellow]not set[/bold yellow]"
            oxalate_status = "off"
        editor_status = _get_editor_command()
        launch_status = "yes" if bool(getattr(state, "_display_program_settings", False)) else "no"

        _show_menu("Settings", [
            ("1", f"Color theme  (current setting: {state._current_theme_name})"),
            ("2", f"Manage profiles  (active: {profile_status})"),
            ("3", "View daily nutrient targets"),
            ("4", f"Dietary preferences  (current setting: {diet_status})"),
            ("5", f"Oxalate data  (Harvard reference table, current setting: {oxalate_status})"),
            ("6", f"Editor command  (current setting: {editor_status})"),
            ("7", f"Display program settings at launch  (current setting: {launch_status})"),
            ("8", "Advanced settings  [grey62](API key, storage, protein overrides)[/grey62]"),
            ("9", f"Nutrient targets  [grey62](Profile Optimal targets and custom max limits, {len(p.optimal_targets) + len(p.max_limits) if p else 0} set)[/grey62]"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[grey62]Cancelled.[/grey62]")
            return True

        if choice == "1":
            _safe_call(_change_theme)
        elif choice == "2":
            _safe_call(_do_manage_profiles)
        elif choice == "3":
            _safe_call(_do_view_goals)
        elif choice == "4":
            _safe_call(_do_dietary_prefs)
        elif choice == "5":
            _safe_call(_do_oxalate_data_setting)
        elif choice == "6":
            _safe_call(_do_editor_command)
        elif choice == "7":
            _safe_call(_do_launch_display_setting)
        elif choice == "8":
            _safe_call(_menu_advanced_settings)
        elif choice == "9":
            _safe_call(_do_nutrient_targets)
        elif choice == "m":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")

def _do_set_api_key() -> None:
    current = _usda.get_api_key()
    if current:
        state.console.print(f"  Current key: [grey62]{current[:8]}...{current[-4:]}[/grey62]")
    while True:
        try:
            key = _prompt("New API key  [grey62](Enter = keep · s = show full key)[/grey62]", default="").strip()
        except Cancelled:
            return
        if key.lower() == "s":
            if current:
                state.console.print(f"  Full key: [bold]{current}[/bold]")
            else:
                state.console.print("  [grey62](No API key set.)[/grey62]")
            continue
        if key:
            _usda.set_api_key(key)
            state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] API key saved.")
        else:
            state.console.print("[grey62]Unchanged.[/grey62]")
        return
