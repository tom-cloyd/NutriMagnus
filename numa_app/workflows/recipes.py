import json
import os
import re
import shutil
import shlex
import subprocess
import tempfile
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..config.prefs import _PREFS_FILE
from ..services.portions import _normalize_unit_display, _pick_portion
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food
from ..services.reports import _offer_export
from ..ui.common import _safe_call, _show_menu
from ..ui.prompts import Cancelled, _ask_int, _prompt
from ..ui.render import _print_complement_suggestions, _print_nutrient_table, _print_protein_completeness, _print_recipe_bioavailability

_RECIPE_LIST_PAGE_SIZE = 20




def _load_editor_command_from_prefs() -> str:
    """Return persisted editor command from prefs, if available."""
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            value = str(data.get("editor_command", "") or "").strip()
            return value
    except Exception:
        pass
    return ""


def _resolve_editor_command() -> tuple[str | None, str]:
    """Return (editor_command, source_label)."""
    editor_from_settings = str(getattr(state, "_editor_command", "") or "").strip()
    if not editor_from_settings:
        editor_from_settings = _load_editor_command_from_prefs()
        if editor_from_settings:
            setattr(state, "_editor_command", editor_from_settings)
    if editor_from_settings:
        return editor_from_settings, "Settings"

    visual = (os.environ.get("VISUAL") or "").strip()
    if visual:
        return visual, "VISUAL"

    editor = (os.environ.get("EDITOR") or "").strip()
    if editor:
        return editor, "EDITOR"

    for candidate in ("nano", "vim", "vi"):
        if shutil.which(candidate):
            return candidate, "system default"

    return None, "system default"



def _edit_text_in_system_editor(initial_text: str = "", label: str = "Procedure") -> str | None:
    """Edit multi-line text in the system editor.

    Returns the edited text, or None if the editor could not be opened.
    Leaving the editor without changes preserves the current text.
    """
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR") or "nano"
    suffix = f"_{label.lower().replace(' ', '_')}.txt"
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", suffix=suffix, delete=False) as tmp:
        path = tmp.name
        tmp.write(initial_text or "")
        tmp.flush()

    try:
        try:
            result = subprocess.run([editor, path], check=False)
        except FileNotFoundError:
            if editor != "vi":
                state.console.print(
                    f"[{state.T['warning']}]Editor '{editor}' not found; trying vi.[/{state.T['warning']}]"
                )
                result = subprocess.run(["vi", path], check=False)
            else:
                raise
        if result.returncode != 0:
            state.console.print(
                f"[{state.T['warning']}]Editor exited with status {result.returncode}. Keeping existing {label.lower()}.[/{state.T['warning']}]"
            )
            return initial_text
        return Path(path).read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        state.console.print(
            f"[{state.T['warning']}]No system editor is available. Keeping existing {label.lower()}.[/{state.T['warning']}]"
        )
        return None
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _edit_recipe_procedure(recipe_id: int, current_text: str = "") -> str:
    state.console.print(
        f"\n[{state.T['accent']}]Procedure[/{state.T['accent']}]  "
        "[dim](opens in system editor; save and quit editor to keep changes)[/dim]"
    )
    edited = _edit_text_in_system_editor(current_text or "", label="Procedure")
    if edited is None:
        return current_text or ""
    return edited
def _compute_recipe_dcp(rid: int) -> float | None:
    """
    Compute digestible complete protein (g, whole recipe) from cached ingredient data.
    Returns None if AA profile data is unavailable.
    """
    with _db.get_db() as conn:
        ingredients = _db.recipe_get_ingredients(conn, rid)

    combined: dict[str, float] = {}
    total_digestible = 0.0
    has_protein = False
    for ing in ingredients:
        _refresh_cache_if_missing_aa(ing["fdc_id"])
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, ing["fdc_id"])
        if not cached:
            continue
        scaled = _usda.scale_nutrients(
            json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
        )
        combined = _usda.sum_nutrients(combined, scaled)
        p = scaled.get("protein_g", 0.0)
        if p > 0:
            has_protein = True
            diaas = _usda.get_diaas(ing["food_name"])
            total_digestible += p * (diaas if diaas is not None else 1.0)

    if not has_protein:
        return None
    pc = _usda.protein_completeness(combined)
    if not pc.get("has_data") or not pc.get("scores"):
        return None
    limiting_score = min(pc["scores"].values())
    return total_digestible * min(1.0, limiting_score)



def _parse_serving_amount(raw: str) -> float | None:
    """Parse a recipe serving amount like 1, 0.5, 1/2, or 1 1/2."""
    raw = raw.strip().lower()
    if not raw or raw in {"b", "back"}:
        return None
    try:
        parts = raw.split()
        if len(parts) == 2 and "/" in parts[1]:
            return float(parts[0]) + float(Fraction(parts[1]))
        if "/" in raw:
            return float(Fraction(raw))
        return float(raw)
    except (ValueError, ZeroDivisionError):
        return None


def _format_recipe_portion_label(servings: float) -> str:
    if abs(servings - 1.0) < 1e-9:
        return "1 serving"
    if servings.is_integer():
        return f"{int(servings)} servings"
    return f"{servings:g} servings"


def _get_recipe_total_nutrients(recipe_id: int) -> tuple[object | None, list, dict[str, float]]:
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        ingredients = _db.recipe_get_ingredients(conn, recipe_id) if recipe else []

    combined: dict[str, float] = {}
    if recipe and ingredients:
        for ing in ingredients:
            _refresh_cache_if_missing_aa(ing["fdc_id"])
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, ing["fdc_id"])
            if cached:
                scaled = _usda.scale_nutrients(
                    json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
                )
                combined = _usda.sum_nutrients(combined, scaled)
    return recipe, ingredients, combined


def _pick_recipe_portion(recipe: object) -> tuple[float, str] | None:
    while True:
        try:
            raw = _prompt(
                "Recipe portion in servings  [dim](examples: 1, 1/2, 1.5 · Enter/b=back, q=quit)[/dim]",
                default="1",
            ).strip()
        except Cancelled:
            return None
        lowered = raw.lower()
        if not lowered or lowered in ("b", "back"):
            return None
        if lowered == "q":
            raise SystemExit(0)
        servings = _parse_serving_amount(raw)
        if servings is None or servings <= 0:
            state.console.print(f"[{state.T['warning']}]Enter a positive number of servings.[/{state.T['warning']}]")
            continue
        return servings, _format_recipe_portion_label(servings)

def _menu_recipes() -> bool:
    """Recipes submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Recipes", [
            ("1", "Create new recipe"),
            ("2", "List recipes"),
            ("3", "View / analyze recipe"),
            ("4", "Edit recipe"),
            ("5", "Delete recipe"),
            ("b", "Back to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[dim]Cancelled.[/dim]")
            return True

        if choice == "1":
            _safe_call(_do_recipe_create)
        elif choice == "2":
            _safe_call(_do_recipe_list)
        elif choice == "3":
            _safe_call(_do_recipe_view)
        elif choice == "4":
            _safe_call(_do_recipe_edit)
        elif choice == "5":
            _safe_call(_do_recipe_delete)
        elif choice == "b":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _edit_recipe_procedure_in_editor(initial_text: str = "") -> str | None:
    """Edit recipe procedure in the user's system editor.

    Returns edited text, or None if editor unavailable or failed.
    Caller should preserve existing text when None is returned.
    """
    editor, editor_source = _resolve_editor_command()

    if not editor:
        state.console.print(
            f"[{state.T['warning']}]No editor is available. Keeping existing procedure.[/{state.T['warning']}]"
        )
        return None

    if editor_source == "system default":
        state.console.print(
            "[dim]No editor has been specified. Using the system default editor.[/dim]"
        )

    suffix = ".md" if "\n" in (initial_text or "") else ".txt"
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=suffix,
            delete=False,
            encoding="utf-8",
        ) as tf:
            temp_path = tf.name
            tf.write(initial_text or "")

        try:
            cmd = shlex.split(editor)
        except ValueError as exc:
            state.console.print(
                f"[{state.T['warning']}]Invalid editor command: {exc}. Keeping existing procedure.[/{state.T['warning']}]"
            )
            return None

        if not cmd:
            state.console.print(
                f"[{state.T['warning']}]Editor command is empty. Keeping existing procedure.[/{state.T['warning']}]"
            )
            return None

        if not (os.path.isabs(cmd[0]) or shutil.which(cmd[0])):
            state.console.print(
                f"[{state.T['warning']}]Editor '{cmd[0]}' not found. Keeping existing procedure.[/{state.T['warning']}]"
            )
            return None

        state.console.print(
            '[dim]\"Procedure\" will open in your system editor.[/dim]'
        )
        state.console.print(
            '[dim]Choice  [Enter=open editor · b=back][/dim]'
        )

        try:
            nav = _prompt("Choice", default="").strip().lower()
        except Cancelled:
            state.console.print(
                f"[{state.T['warning']}]Editor launch cancelled. Keeping existing procedure.[/{state.T['warning']}]"
            )
            return None

        if nav == "b":
            state.console.print("[dim]Returned to previous field.[/dim]")
            return None

        result = subprocess.run(cmd + [temp_path], check=False)

        if result.returncode != 0:
            state.console.print(
                f"[{state.T['warning']}]Editor exited with status {result.returncode}. Keeping existing procedure.[/{state.T['warning']}]"
            )
            return None

        with open(temp_path, "r", encoding="utf-8") as fh:
            return fh.read().rstrip()

    except KeyboardInterrupt:
        state.console.print(
            f"[{state.T['warning']}]Editor cancelled. Keeping existing procedure.[/{state.T['warning']}]"
        )
        return None

    except Exception as exc:
        state.console.print(
            f"[{state.T['warning']}]Could not open editor: {exc}. Keeping existing procedure.[/{state.T['warning']}]"
        )
        return None

    finally:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass


def _do_recipe_create() -> None:
    try:
        name = _prompt("Recipe name").strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return

    try:
        description = _prompt("Description (optional)", default="").strip()
        raw_servings = _prompt("Number of servings", default="1").strip()
        servings = int(raw_servings) if raw_servings.isdigit() else 1
    except Cancelled:
        return

    with _db.get_db() as conn:
        recipe_id = _db.recipe_create(conn, name, description, servings, "")

    state.console.print(
        f"[{state.T['success']}]✓[/{state.T['success']}] Recipe [{state.T['hi']}]{name}[/{state.T['hi']}] "
        f"created (ID {recipe_id}).  Now add ingredients."
    )

    # Add ingredients first
    while True:
        state.console.print()
        food = _search_and_pick_food()
        if food is None:
            break
        result = _pick_portion(food)
        if result is None:
            break
        grams, label, _ = result
        with _db.get_db() as conn:
            _db.recipe_add_ingredient(conn, recipe_id, food["fdcId"], food["name"], grams, label)
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")
        try:
            cont = _prompt("Choice  [y=add another · n=continue · q=quit]", choices=["y", "n", "q"], default="y")
        except Cancelled:
            break
        if cont.lower() == "q":
            raise SystemExit(0)
        if cont.lower() != "y":
            break

    # Procedure comes after ingredients, using the system editor
    state.console.print()
    procedure = _edit_recipe_procedure_in_editor("")
    if procedure is not None:
        with _db.get_db() as conn:
            current = _db.recipe_get(conn, recipe_id)
            _db.recipe_update(
                conn,
                recipe_id,
                current["name"],
                current["description"] or "",
                current["servings"],
                procedure,
            )

    state.console.print(f"[{state.T['success']}]Recipe saved.[/{state.T['success']}]")


def _get_all_recipes() -> list:
    with _db.get_db() as conn:
        return _db.recipe_list(conn)


def _show_recipes_for_selection() -> list:
    recipes = _get_all_recipes()
    if not recipes:
        state.console.print("[dim]No recipes saved yet.[/dim]")
        return []
    _do_recipe_list(recipes=recipes)
    return recipes


def _do_recipe_list(recipes: list | None = None) -> None:
    if recipes is None:
        recipes = _get_all_recipes()
    if not recipes:
        state.console.print("[dim]No recipes saved yet.[/dim]")
        return

    page_size = _RECIPE_LIST_PAGE_SIZE
    total = len(recipes)
    start_idx = 0

    while start_idx < total:
        end_idx = min(start_idx + page_size, total)
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("ID", justify="right", min_width=4)
        tbl.add_column("Name", min_width=30)
        tbl.add_column("Servings", justify="right", min_width=8)
        tbl.add_column("DCP/srv", justify="right", min_width=9)
        tbl.add_column("Created", min_width=12)
        for r in recipes[start_idx:end_idx]:
            if r["dcp_g"] is not None and r["servings"] > 0:
                dcp_str = f"{r['dcp_g'] / r['servings']:.1f}g"
            else:
                dcp_str = "[dim]—[/dim]"
            tbl.add_row(str(r["id"]), r["name"], str(r["servings"]), dcp_str, r["created_at"])

        state.console.print()
        state.console.print(f"[dim]Recipes {start_idx + 1}-{end_idx} of {total}[/dim]")
        state.console.print(tbl)

        if end_idx >= total:
            return

        try:
            more = _prompt("Choice  [Enter=next · b=back · q=quit]", default="").strip().lower()
        except Cancelled:
            return
        if more == "q":
            raise SystemExit(0)
        if more == "b":
            return
        start_idx += page_size


def _resolve_recipe_dcp_data(
    recipe_id: int,
    ingredients: list,
    ingredient_stats: list[dict],
    combined: dict[str, float],
) -> tuple[list[dict], dict[str, float], bool, list[str]] | None:
    """
    Detect missing data that blocks or degrades DCP calculation.
    Prompts the user to provide data, calculate with assumptions, or skip.

    Returns (updated_stats, updated_combined, approximate, notes),
    None if the user chooses to skip DCP entirely,
    or the string "rerun" if ingredients were replaced and analysis should restart.
    """
    zero_weight = [ing for ing in ingredients if "(weight not known)" in (ing["unit"] or "")]
    no_diaas    = [s for s in ingredient_stats if s["diaas"] is None]
    no_aa_ings  = [s for s in ingredient_stats if not s.get("has_aa", True)]
    pc          = _usda.protein_completeness(combined)
    no_aa       = not pc.get("has_data")

    if not zero_weight and not no_diaas and not no_aa:
        return ingredient_stats, combined, False, []

    state.console.print(f"\n  [{state.T['warning']}]⚠  Missing data for digestible complete protein (DCP):[/{state.T['warning']}]")
    for ing in zero_weight:
        state.console.print(f"    • {ing['food_name']} — weight unknown ({_normalize_unit_display(ing['unit'])})")
    for s in no_diaas:
        state.console.print(f"    • {s['name']} — no digestibility (DIAAS) score in database")
    if no_aa:
        if no_aa_ings:
            for s in no_aa_ings:
                state.console.print(f"    • {s['name']} — no amino acid profile in USDA data")
        else:
            state.console.print("    • No amino acid profile available in USDA data for these ingredients.")

    option_actions: list[tuple[str, str]] = []
    if zero_weight or no_diaas:
        option_actions.append(("provide", "Provide missing data now"))
    if no_aa and no_aa_ings:
        option_actions.append(("fix", "Fix: replace affected ingredients via Foundation Foods search"))
    option_actions.append(("calculate", "Calculate anyway  (result flagged as approximate)"))
    option_actions.append(("skip", "Skip DCP calculation"))

    menu_options = [(str(i + 1), label) for i, (_, label) in enumerate(option_actions)]
    menu_options.extend([("b", "Back"), ("q", "Quit")])
    _show_menu("Options", menu_options)
    try:
        choice = _prompt("Choice").strip().lower()
    except Cancelled:
        choice = "b"

    if choice == "q":
        raise SystemExit(0)
    if choice == "b" or not choice:
        return None

    action_map = {str(i + 1): action for i, (action, _) in enumerate(option_actions)}
    action = action_map.get(choice)
    if action is None:
        state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")
        return None

    if action == "fix":
        # Replace each affected ingredient with a Foundation Foods version
        affected_names = {s["name"].lower() for s in no_aa_ings}
        with _db.get_db() as conn:
            all_ings = _db.recipe_get_ingredients(conn, recipe_id)
        replaced_any = False
        for ing in all_ings:
            if ing["food_name"].lower() not in affected_names:
                continue
            state.console.print(
                f"\n  Replacing: [{state.T['accent']}]{ing['food_name']}[/{state.T['accent']}]\n"
                "  [dim]Search for a Foundation Foods replacement:[/dim]"
            )
            food = _search_and_pick_food(data_types=["Foundation", "SR Legacy"], show_aa_status=True, allow_research=False)
            if food is None:
                state.console.print("  [dim]Skipped.[/dim]")
                continue
            result = _pick_portion(food)
            if result is None:
                state.console.print("  [dim]Skipped.[/dim]")
                continue
            grams, label, _ = result
            with _db.get_db() as conn:
                _db.recipe_remove_ingredient(conn, ing["id"])
                _db.recipe_add_ingredient(conn, recipe_id, food["fdcId"], food["name"], grams, label)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Replaced with: {food['name']}  {label}")
            replaced_any = True
        if replaced_any:
            return "rerun"  # type: ignore[return-value]
        return None

    approximate = False
    notes: list[str] = []

    if action == "provide":
        new_combined  = dict(combined)
        new_stats     = list(ingredient_stats)

        for ing in zero_weight:
            vol_display = _normalize_unit_display(ing["unit"]).replace(" (weight not known)", "")
            state.console.print(f"\n  [{state.T['accent']}]{ing['food_name']}[/{state.T['accent']}]"
                          f"  [dim]({vol_display})[/dim]")
            try:
                w_raw = _prompt("Weight in grams  [Enter=skip]").strip()
            except Cancelled:
                w_raw = ""
            if w_raw.lower() == "q":
                raise SystemExit(0)
            if w_raw and w_raw.lower() not in ("b", "s"):
                try:
                    grams = float(w_raw)
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, ing["fdc_id"])
                    if cached:
                        scaled = _usda.scale_nutrients(
                            json.loads(cached["nutrients_json"]), grams, base_size=100.0
                        )
                        new_combined = _usda.sum_nutrients(new_combined, scaled)
                        p = scaled.get("protein_g", 0.0)
                        if p > 0:
                            new_stats.append({
                                "name": ing["food_name"],
                                "protein_g": p,
                                "diaas": _usda.get_diaas(ing["food_name"]),
                            })
                    notes.append(f"{ing['food_name']}: {grams:.0f}g (user-provided, not saved)")
                    approximate = True  # user-supplied value, not from DB
                except ValueError:
                    approximate = True
                    notes.append(f"{ing['food_name']}: skipped (invalid weight)")
            else:
                approximate = True
                notes.append(f"{ing['food_name']}: excluded (weight not provided)")

        for s in no_diaas:
            state.console.print(
                f"\n  [{state.T['accent']}]{s['name']}[/{state.T['accent']}]  [dim]— DIAAS unknown[/dim]\n"
                "  [dim]Reference: eggs 0.99 · whey 0.97 · meat/fish 0.90–0.95 · soy 0.91 "
                "· legumes 0.64–0.75 · wheat 0.46[/dim]"
            )
            try:
                d_raw = _prompt("DIAAS value (0.0–1.0)  [Enter=skip; assume 1.0]").strip()
            except Cancelled:
                d_raw = ""
            if d_raw.lower() == "q":
                raise SystemExit(0)
            if d_raw and d_raw.lower() not in ("b", "s"):
                try:
                    diaas = max(0.0, min(1.0, float(d_raw)))
                    s["diaas"] = diaas
                    notes.append(f"{s['name']}: DIAAS {diaas:.2f} (user-provided)")
                    approximate = True
                except ValueError:
                    approximate = True
                    notes.append(f"{s['name']}: DIAAS assumed 1.0 (invalid input)")
            else:
                approximate = True
                notes.append(f"{s['name']}: DIAAS assumed 1.0")

        return new_stats, new_combined, approximate, notes

    else:  # "calculate" — calculate anyway
        approximate = True
        for ing in zero_weight:
            notes.append(f"{ing['food_name']}: excluded (weight not known)")
        for s in no_diaas:
            notes.append(f"{s['name']}: DIAAS assumed 1.0")
        if no_aa:
            notes.append("amino acid completeness: unknown — no AA data in USDA cache")
        return ingredient_stats, combined, True, notes


def _do_recipe_view() -> None:
    recipes = _show_recipes_for_selection()
    if not recipes:
        return
    rid = _ask_int("Recipe ID")
    if rid is None:
        return
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
        if recipe is None:
            state.console.print(f"[{state.T['warning']}]Recipe {rid} not found.[/{state.T['warning']}]")
            return
        ingredients = _db.recipe_get_ingredients(conn, rid)

    if not ingredients:
        state.console.print("[dim]This recipe has no ingredients.[/dim]")
        return

    while True:
        # Reload recipe + ingredients on rerun (ingredients may have been replaced)
        with _db.get_db() as conn:
            recipe     = _db.recipe_get(conn, rid)
            ingredients = _db.recipe_get_ingredients(conn, rid)

        state.console.print(f"\n[{state.T['accent']}]{recipe['name']}[/{state.T['accent']}]  "
                      f"[dim]{recipe['servings']} serving(s)[/dim]")
        if recipe["description"]:
            state.console.print(f"  {recipe['description']}")
        if recipe["instructions"]:
            state.console.print(f"\n[{state.T['accent']}]Procedure:[/{state.T['accent']}]")
            state.console.print(f"  {recipe['instructions']}")
        state.console.rule()

        # Build combined nutrients and per-ingredient protein+DIAAS (silent — before display)
        combined: dict[str, float] = {}
        ingredient_stats: list[dict] = []
        for ing in ingredients:
            _refresh_cache_if_missing_aa(ing["fdc_id"])
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, ing["fdc_id"])
            if cached:
                scaled = _usda.scale_nutrients(
                    json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
                )
                combined = _usda.sum_nutrients(combined, scaled)
                ing_protein = scaled.get("protein_g", 0.0)
                if ing_protein > 0:
                    ingredient_stats.append({
                        "name": ing["food_name"],
                        "protein_g": ing_protein,
                        "diaas": _usda.get_diaas(ing["food_name"]),
                        "has_aa": _usda.protein_completeness(scaled).get("has_data", False),
                    })

        # Resolve missing DCP data before displaying tables so totals reflect any user input
        dcp_skip = False
        dcp_approximate = False
        dcp_notes: list[str] = []
        if combined:
            resolved = _resolve_recipe_dcp_data(recipe["id"], ingredients, ingredient_stats, combined)
            if resolved == "rerun":
                continue
            if resolved is None:
                dcp_skip = True
            else:
                ingredient_stats, combined, dcp_approximate, dcp_notes = resolved
        break

    if combined:
        state.console.print()
        # Show ingredient list
        for ing in ingredients:
            state.console.print(f"  • {ing['food_name']}  {_normalize_unit_display(ing['unit'])}")
        state.console.print()
        _print_nutrient_table(combined, title="Total recipe",
                              per_label=f"whole recipe ({recipe['servings']} servings)")
        # Per-serving (skip when servings=1 — identical to total)
        if recipe["servings"] > 1:
            per_serving = {k: v / recipe["servings"] for k, v in combined.items()}
            _print_nutrient_table(per_serving, title="Per serving")
            analysis_nutrients = per_serving
        else:
            analysis_nutrients = combined

        # Compute DCP, save to DB, and always display it as a summary line
        now_utc = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()
        if dcp_skip:
            with _db.get_db() as conn:
                _db.recipe_set_dcp(conn, recipe["id"], None)
            state.console.print("\n  [dim]Digestible complete protein: skipped.[/dim]")
        else:
            total_protein = analysis_nutrients.get("protein_g", 0.0)
            pc_quick = _usda.protein_completeness(analysis_nutrients)
            if ingredient_stats and total_protein > 0 and pc_quick.get("has_data") and pc_quick.get("scores"):
                total_digestible = sum(
                    s["protein_g"] * (s["diaas"] if s["diaas"] is not None else 1.0)
                    for s in ingredient_stats
                )
                limiting_score = min(pc_quick["scores"].values())
                dcp = total_digestible * min(1.0, limiting_score)
                dcp_whole = dcp * recipe["servings"] if recipe["servings"] > 1 else dcp
                # Only save to DB if all data was authoritative (not approximate)
                save_ts = now_utc if not dcp_approximate else None
                was_missing = recipe["dcp_g"] is None
                with _db.get_db() as conn:
                    _db.recipe_set_dcp(conn, recipe["id"], None if dcp_approximate else dcp_whole, save_ts)
                color = state.T["success"] if limiting_score >= 1.0 else state.T["warning"]
                approx_tag = f"  [{state.T['warning']}]⚠ approximate[/{state.T['warning']}]" if dcp_approximate else ""
                if was_missing and not dcp_approximate:
                    state.console.print(
                        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  [dim]Recipe data now complete"
                        f" — DCP can be calculated.[/dim]"
                    )
                state.console.print(
                    f"\n  Digestible complete protein: [{color}]{dcp:.1f}g[/{color}]"
                    f"  [dim]per serving[/dim]{approx_tag}",
                    highlight=False,
                )
                if dcp_approximate:
                    if dcp_notes:
                        for note in dcp_notes:
                            state.console.print(f"    [dim]↳ {note}[/dim]")
                else:
                    state.console.print(
                        f"  [dim]↳ Saved to recipe · computed {now_utc}[/dim]",
                        highlight=False,
                    )
            else:
                with _db.get_db() as conn:
                    _db.recipe_set_dcp(conn, recipe["id"], None)
                state.console.print(
                    "\n  [dim]Digestible complete protein: not available "
                    "(no amino acid data for these ingredients)[/dim]"
                )
                if dcp_notes:
                    for note in dcp_notes:
                        state.console.print(f"    [dim]↳ {note}[/dim]")

        # Offer full protein analysis
        try:
            ans = _prompt("Choice  [y=show protein analysis · Enter=skip]", default="").strip().lower()
        except Cancelled:
            ans = "n"
        if ans == "y":
            has_aa = _print_protein_completeness(analysis_nutrients)
            if ingredient_stats:
                _print_recipe_bioavailability(ingredient_stats, analysis_nutrients)
            if has_aa and _usda.get_aa_gaps(analysis_nutrients):
                _print_complement_suggestions(analysis_nutrients, context="recipe",
                                              offer_if_covered=True)
        _offer_export(recipe["name"], [
            {"type": "ingredient_list", "title": "Ingredients",
             "items": [{"food_name": i["food_name"], "amount": i["amount"],
                        "unit": i["unit"]} for i in ingredients]},
            {"type": "nutrient_table", "title": "Total recipe", "nutrients": combined,
             "per_label": f"whole recipe, {recipe['servings']} servings"},
            {"type": "nutrient_table", "title": "Per serving", "nutrients": analysis_nutrients},
            {"type": "protein_completeness", "nutrients": analysis_nutrients},
        ])



def _print_recipe_edit_progress(current_step: int, values: dict[str, object]) -> None:
    """Show recipe edit steps, highlighting the current field."""
    steps = [
        ("Name", values.get("name", "")),
        ("Description", values.get("description", "")),
        ("Servings", values.get("servings", "")),
        ("Procedure", "system editor"),
        ("Ingredients", "list/menu"),
    ]
    state.console.print(f"[dim]Enter = keep current · b = back · Ctrl+C = cancel[/dim]")
    for idx, (label, value) in enumerate(steps):
        prefix = "→" if idx == current_step else " "
        style = state.T["accent"] if idx == current_step else "dim"
        if label == "Procedure":
            display = str(value)
        elif label == "Ingredients":
            display = str(value)
        else:
            display = str(value) if value not in (None, "") else "—"
        state.console.print(
            f" [{style}]{prefix} {idx + 1}. {label}[/{style}] [dim]({display})[/dim]",
            highlight=False,
        )
    state.console.print()

def _do_recipe_edit() -> None:
    recipes = _show_recipes_for_selection()
    if not recipes:
        return
    rid = _ask_int("Recipe ID to edit")
    if rid is None:
        return
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
    if recipe is None:
        state.console.print(f"[{state.T['warning']}]Recipe {rid} not found.[/{state.T['warning']}]")
        return

    with _db.get_db() as conn:
        initial_ingredient_count = len(_db.recipe_get_ingredients(conn, rid))

    state.console.print()
    state.console.print(f"[{state.T['accent']}]Editing: {recipe['name']}[/{state.T['accent']}]")
    state.console.print()

    values: dict[str, object] = {
        "name": recipe["name"],
        "description": recipe["description"] or "",
        "servings": recipe["servings"],
        "procedure": recipe["instructions"] or "",
        "ingredients_count": initial_ingredient_count,
    }

    changed = False
    ingredients_changed = False
    steps = ["name", "description", "servings", "procedure", "ingredients"]
    idx = 0

    def _save_recipe_details() -> None:
        with _db.get_db() as conn:
            _db.recipe_update(
                conn,
                rid,
                str(values["name"]),
                str(values["description"]),
                int(values["servings"]),
                str(values["procedure"]),
            )

    while idx < len(steps):
        step = steps[idx]
        _print_recipe_edit_progress(idx, {
            "name": values["name"],
            "description": values["description"],
            "servings": values["servings"],
            "procedure": values["procedure"],
            "ingredients": f"{values['ingredients_count']} item(s)",
        })

        try:
            if step == "name":
                raw = _prompt("Name", default=str(values["name"])).strip()
                if raw.lower() == "b":
                    if idx == 0:
                        state.console.print("[dim]Already at the first field.[/dim]")
                        continue
                    idx -= 1
                    continue
                if raw and raw != values["name"]:
                    values["name"] = raw
                    _save_recipe_details()
                    changed = True
                    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Name autosaved.")
                idx += 1
                continue

            if step == "description":
                raw = _prompt("Description", default=str(values["description"])).strip()
                if raw.lower() == "b":
                    idx -= 1
                    continue
                if raw != values["description"]:
                    values["description"] = raw
                    _save_recipe_details()
                    changed = True
                    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Description autosaved.")
                idx += 1
                continue

            if step == "servings":
                raw = _prompt("Servings", default=str(values["servings"])).strip()
                if raw.lower() == "b":
                    idx -= 1
                    continue
                if raw:
                    if raw.isdigit():
                        new_servings = int(raw)
                        if new_servings != values["servings"]:
                            values["servings"] = new_servings
                            _save_recipe_details()
                            changed = True
                            state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Servings autosaved.")
                    else:
                        state.console.print(f"[{state.T['warning']}]Enter a whole number for servings.[/{state.T['warning']}]")
                        continue
                idx += 1
                continue

            if step == "procedure":
                procedure = _edit_recipe_procedure_in_editor(str(values["procedure"]))
                if procedure is None:
                    try:
                        nav = _prompt('Choice  [Enter=continue · b=back to "Servings"]', default="").strip().lower()
                    except Cancelled:
                        return
                    if nav == "b":
                        idx -= 1
                    else:
                        idx += 1
                    continue
                if procedure != values["procedure"]:
                    values["procedure"] = procedure
                    _save_recipe_details()
                    changed = True
                    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Procedure autosaved.")
                idx += 1
                continue

            # step == "ingredients"
            while True:
                with _db.get_db() as conn:
                    ingredients = _db.recipe_get_ingredients(conn, rid)
                values["ingredients_count"] = len(ingredients)

                state.console.print()
                state.console.print(f"[{state.T['accent']}]Ingredients[/{state.T['accent']}]")
                if ingredients:
                    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
                    tbl.add_column("#", justify="right", min_width=3)
                    tbl.add_column("Amount", min_width=14)
                    tbl.add_column("Food", min_width=40)
                    for i, ing in enumerate(ingredients, 1):
                        tbl.add_row(str(i), _normalize_unit_display(ing["unit"]), ing["food_name"])
                    state.console.print(tbl)
                else:
                    state.console.print("[dim]No ingredients yet.[/dim]")

                _show_menu("Ingredients", [
                    ("1", "Add ingredient"),
                    ("2", "Edit ingredient"),
                    ("3", "Remove ingredient"),
                    ("4", "Reorder ingredients"),
                    ("b", "Back"),
                    ("q", "Quit"),
                ])
                try:
                    choice = _prompt("Choice").strip().lower()
                except Cancelled:
                    return

                if choice == "b":
                    idx -= 1
                    break
                if choice == "q":
                    raise SystemExit(0)
                elif choice == "1":
                    food = _search_and_pick_food()
                    if food is None:
                        continue
                    result = _pick_portion(food)
                    if result is None:
                        continue
                    grams, label, _ = result
                    with _db.get_db() as conn:
                        _db.recipe_add_ingredient(conn, rid, food["fdcId"], food["name"], grams, label)
                    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")
                    ingredients_changed = True
                    changed = True
                elif choice == "2":
                    if not ingredients:
                        state.console.print(f"[{state.T['warning']}]No ingredients to edit.[/{state.T['warning']}]")
                        continue
                    ing_idx = _ask_int("Ingredient # to edit")
                    if ing_idx is None or ing_idx < 1 or ing_idx > len(ingredients):
                        state.console.print(f"[{state.T['warning']}]Invalid number.[/{state.T['warning']}]")
                        continue
                    ing = ingredients[ing_idx - 1]
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, ing["fdc_id"])
                    if cached is None:
                        state.console.print(f"[{state.T['warning']}]Food details not in cache; remove and re-add this ingredient.[/{state.T['warning']}]")
                        continue
                    food = {
                        "fdcId": cached["fdc_id"],
                        "name": cached["name"],
                        "dataType": cached["data_type"],
                        "brand": cached["brand"],
                        "servingSize": cached["serving_size"],
                        "servingUnit": cached["serving_unit"],
                        "nutrients": json.loads(cached["nutrients_json"]),
                        "portions": json.loads(cached["portions_json"]) if cached["portions_json"] else [],
                    }
                    try:
                        food_name_new = _prompt("Name", default=ing["food_name"]).strip()
                    except Cancelled:
                        continue
                    if not food_name_new:
                        food_name_new = ing["food_name"]
                    result = _pick_portion(food)
                    if result is None:
                        continue
                    grams, label, _ = result
                    with _db.get_db() as conn:
                        _db.recipe_update_ingredient(conn, ing["id"], grams, label, food_name_new)
                    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Updated: {food_name_new}  {label}")
                    ingredients_changed = True
                    changed = True
                elif choice == "3":
                    if not ingredients:
                        state.console.print(f"[{state.T['warning']}]No ingredients to remove.[/{state.T['warning']}]")
                        continue
                    ing_idx = _ask_int("Ingredient # to remove")
                    if ing_idx is None or ing_idx < 1 or ing_idx > len(ingredients):
                        state.console.print(f"[{state.T['warning']}]Invalid number.[/{state.T['warning']}]")
                        continue
                    ing = ingredients[ing_idx - 1]
                    with _db.get_db() as conn:
                        _db.recipe_remove_ingredient(conn, ing["id"])
                    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Removed: {ing['food_name']}")
                    ingredients_changed = True
                    changed = True
                elif choice == "4":
                    if len(ingredients) < 2:
                        state.console.print(f"[{state.T['warning']}]Nothing to reorder.[/{state.T['warning']}]")
                        continue
                    state.console.print("[dim]Enter ingredient numbers in the new order, space- or comma-separated "
                                  f"(e.g. 3 1 2 4 for {len(ingredients)} ingredients):[/dim]")
                    try:
                        raw_order = _prompt("New order  [numbers only; b=back · q=quit]").strip()
                    except Cancelled:
                        continue
                    if not raw_order or raw_order.lower() in ("b", "q"):
                        if raw_order.lower() == "q":
                            raise SystemExit(0)
                        continue
                    tokens = re.split(r'[\s,]+', raw_order.strip())
                    try:
                        new_order = [int(t) for t in tokens if t]
                    except ValueError:
                        state.console.print(f"[{state.T['warning']}]Enter numbers only.[/{state.T['warning']}]")
                        continue
                    if sorted(new_order) != list(range(1, len(ingredients) + 1)):
                        state.console.print(f"[{state.T['warning']}]Must include each number 1–{len(ingredients)} exactly once.[/{state.T['warning']}]")
                        continue
                    reordered = [ingredients[i - 1] for i in new_order]
                    with _db.get_db() as conn:
                        conn.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (rid,))
                        for ing in reordered:
                            _db.recipe_add_ingredient(conn, rid, ing["fdc_id"], ing["food_name"], ing["amount"], ing["unit"])
                    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Ingredients reordered.")
                    ingredients_changed = True
                    changed = True
                else:
                    state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")
            if idx < 0:
                idx = 0
            if idx < len(steps) and steps[idx] == "procedure":
                continue
            idx += 1

        except Cancelled:
            return

    if changed or ingredients_changed:
        dcp = _compute_recipe_dcp(rid)
        ts = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat() if dcp is not None else None
        with _db.get_db() as conn:
            _db.recipe_set_dcp(conn, rid, dcp, ts)
        state.console.print(f"[{state.T['success']}]Recipe saved.[/{state.T['success']}]")
    else:
        state.console.print("[dim]No changes made.[/dim]")

def _do_recipe_delete() -> None:
    recipes = _show_recipes_for_selection()
    if not recipes:
        return
    rid = _ask_int("Recipe ID to delete")
    if rid is None:
        return
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, rid)
    if recipe is None:
        state.console.print(f"[{state.T['warning']}]Recipe {rid} not found.[/{state.T['warning']}]")
        return
    try:
        confirm = _prompt(
            f"Delete [{state.T['hi']}]{recipe['name']}[/{state.T['hi']}]?",
            choices=["y", "n"], default="n"
        )
    except Cancelled:
        return
    if confirm.lower() == "y":
        with _db.get_db() as conn:
            _db.recipe_delete(conn, rid)
        state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Deleted.")
    else:
        state.console.print("[dim]Cancelled.[/dim]")
