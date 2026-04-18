import json
import re
import textwrap
from fractions import Fraction
from datetime import datetime, timezone

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..services.portions import _normalize_unit_display, _parse_portion_input, _pick_portion, _UNIT_TO_GRAMS, _VOLUME_TO_ML
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food
from ..services.reports import _offer_export
from ..ui.common import _id_cell, ID_KEY, _open_in_editor, _safe_call, _show_menu
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_complement_suggestions, _print_nutrient_table, _print_protein_completeness, _print_recipe_bioavailability

def _parse_measure(raw: str) -> tuple[float | None, str | None]:
    """Parse 'NUMBER UNIT' input, e.g. '4 cups' → (4.0, 'cups'), '' → (None, None)."""
    raw = raw.strip()
    if not raw:
        return None, None
    parts = raw.split(None, 1)
    try:
        val = float(parts[0])
    except ValueError:
        return None, None
    unit = parts[1].strip() if len(parts) > 1 else None
    return val, unit


_RECIPE_PAGE = 20


def _show_recipe_page(recipes: list, offset: int) -> None:
    page = recipes[offset : offset + _RECIPE_PAGE]
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID",       justify="right", min_width=4)
    tbl.add_column("Name",     min_width=30)
    tbl.add_column("Servings", justify="right", min_width=8)
    tbl.add_column("DCP/srv",  justify="right", min_width=9)
    tbl.add_column("Created",  min_width=12)
    for r in page:
        dcp_str = f"{r['dcp_g'] / r['servings']:.1f}g" if r["dcp_g"] is not None and r["servings"] > 0 else "[dim]—[/dim]"
        tbl.add_row(str(r["id"]), r["name"], str(r["servings"]), dcp_str, r["created_at"])
    state.console.print(tbl)
    if len(recipes) > _RECIPE_PAGE:
        state.console.print(f"  [dim]Showing {offset + 1}–{offset + len(page)} of {len(recipes)}[/dim]")


def _pick_recipe() -> dict | None:
    """
    Search recipes by name fragment (or list all), show paginated results,
    and return the selected recipe dict. Returns None if cancelled or not found.
    """
    with _db.get_db() as conn:
        all_recipes = _db.recipe_list(conn)
    if not all_recipes:
        state.console.print("[dim]No recipes saved yet.[/dim]")
        return None

    try:
        query = _prompt("Search recipes  [dim](Enter to list all, b=back, m=main, q=quit)[/dim]", default="", free_text=True).strip()
    except Cancelled:
        return None
    lowered = query.lower()
    if lowered == "q":
        raise SystemExit(0)
    if lowered == "m":
        raise ReturnToMain()
    if lowered == "b":
        return None

    if query:
        recipes = [r for r in all_recipes if lowered in r["name"].lower()]
        if not recipes:
            state.console.print(f"[{state.T['warning']}]No recipes matching '{query}'.[/{state.T['warning']}]")
            return None
    else:
        recipes = all_recipes

    offset = 0
    while True:
        _show_recipe_page(recipes, offset)
        has_more = offset + _RECIPE_PAGE < len(recipes)
        hints = ["id=pick"]
        if has_more:
            hints.append("more=next")
        if offset > 0:
            hints.append("prev=back")
        hints.append("b=cancel")
        try:
            raw = _prompt(f"Recipe ID  [dim]({', '.join(hints)})[/dim]").strip().lower()
        except Cancelled:
            return None
        if raw in ("b", ""):
            return None
        if raw == "m":
            raise ReturnToMain()
        if raw == "q":
            raise SystemExit(0)
        if raw == "more" and has_more:
            offset += _RECIPE_PAGE
            continue
        if raw == "prev" and offset > 0:
            offset = max(0, offset - _RECIPE_PAGE)
            continue
        try:
            rid = int(raw)
        except ValueError:
            state.console.print(f"[{state.T['warning']}]Enter a recipe ID from the list.[/{state.T['warning']}]")
            continue
        with _db.get_db() as conn:
            recipe = _db.recipe_get(conn, rid)
        if recipe is None:
            state.console.print(f"[{state.T['warning']}]Recipe not found.[/{state.T['warning']}]")
            continue
        return recipe


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
        if ing["ref_recipe_id"]:
            sub_dcp = _compute_recipe_dcp(ing["ref_recipe_id"])
            if sub_dcp is not None:
                with _db.get_db() as conn:
                    sub_recipe = _db.recipe_get(conn, ing["ref_recipe_id"])
                if sub_recipe and sub_recipe["servings"] > 0:
                    has_protein = True
                    total_digestible += sub_dcp * (ing["amount"] / sub_recipe["servings"])
            continue
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
    return total_digestible


def _augment_aa_from_curated(
    nutrients: dict[str, float],
    stats: list[dict],
) -> tuple[dict[str, float], bool]:
    """
    Return (augmented_nutrients, was_augmented).

    For each ingredient in stats that lacks USDA AA data (has_aa=False), look up
    its amino acid profile in the curated complement table and add scaled AA amounts.
    Preserves any existing USDA AA values — only adds for ingredients without them.
    Used to get reliable gap scores when the USDA cache has no AA records for
    branded products.
    """
    augmented = dict(nutrients)
    was_augmented = False
    for s in stats:
        if s.get("has_aa"):
            continue
        curated = _usda.get_complement_nutrients(s["name"])
        if not curated or curated.get("protein_g", 0) <= 0:
            continue
        scale = s["protein_g"] / curated["protein_g"]
        for aa_key in _usda.ESSENTIAL_AMINO_ACIDS:
            if aa_key in curated:
                augmented[aa_key] = augmented.get(aa_key, 0.0) + curated[aa_key] * scale
                was_augmented = True
    return augmented, was_augmented


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
            if ing["ref_recipe_id"]:
                _, _, sub_nutrients = _get_recipe_total_nutrients(ing["ref_recipe_id"])
                with _db.get_db() as conn:
                    sub_recipe = _db.recipe_get(conn, ing["ref_recipe_id"])
                if sub_recipe and sub_recipe["servings"] > 0:
                    scale = ing["amount"] / sub_recipe["servings"]
                    scaled = {k: v * scale for k, v in sub_nutrients.items()}
                    combined = _usda.sum_nutrients(combined, scaled)
            else:
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
                "Recipe portion in servings  [dim](examples: 1, 1/2, 1.5 · Enter/b=back, m=main, q=quit)[/dim]",
                default="1",
            ).strip()
        except Cancelled:
            return None
        lowered = raw.lower()
        if not lowered or lowered in ("b", "back"):
            return None
        if lowered == "m":
            raise ReturnToMain()
        if lowered == "q":
            raise SystemExit(0)
        servings = _parse_serving_amount(raw)
        if servings is None or servings <= 0:
            state.console.print(f"[{state.T['warning']}]Enter a positive number of servings.[/{state.T['warning']}]")
            continue
        return servings, _format_recipe_portion_label(servings)

def _do_recipe_display() -> None:
    """Show the full text of a recipe (name, description, volume/weight,
    ingredients, procedure) without running nutritional analysis."""
    recipe = _pick_recipe()
    if recipe is None:
        return
    with _db.get_db() as conn:
        ingredients = _db.recipe_get_ingredients(conn, recipe["id"])

    complete_tag = f"[green]✓ complete[/green]" if recipe["complete"] else "[dim]incomplete[/dim]"
    state.console.print(
        f"\n  [{state.T['accent']}]{recipe['name']}[/{state.T['accent']}]  "
        f"[dim]{recipe['servings']} serving(s)[/dim]  {complete_tag}"
    )
    if recipe["description"]:
        state.console.print(f"  {recipe['description']}")

    def _fmt(val, unit):
        return f"{val:g} {unit}" if unit else f"{val:g}" if val is not None else None

    vol = _fmt(recipe["total_volume"], recipe["total_volume_unit"])
    wt  = _fmt(recipe["total_weight"],  recipe["total_weight_unit"])
    parts = []
    if recipe["serving_size"]:
        parts.append(f"Serving size: {recipe['serving_size']}")
    if vol:
        parts.append(f"Volume: {vol}")
    if wt:
        parts.append(f"Weight: {wt}")
    if parts:
        state.console.print(f"  [dim]{' · '.join(parts)}[/dim]")

    if ingredients:
        state.console.print(f"\n  [{state.T['accent']}]Ingredients:[/{state.T['accent']}]  {ID_KEY}")
        for ing in ingredients:
            note_tag = f"  [dim]({ing['notes']})[/dim]" if ing["notes"] else ""
            if ing["ref_recipe_id"]:
                id_part = "[dim]recipe[/dim]"
            else:
                id_part = _id_cell(ing["fdc_id"])
            state.console.print(
                f"  • {_normalize_unit_display(ing['unit'])}  {id_part}  {ing['food_name']}{note_tag}"
            )
    else:
        state.console.print("\n  [dim]No ingredients yet.[/dim]")

    state.console.print(f"\n  [{state.T['accent']}]Procedure:[/{state.T['accent']}]")
    if recipe["instructions"] and recipe["instructions"].strip():
        width = max(40, state.console.width - 1)
        for line in recipe["instructions"].splitlines():
            state.console.print(
                textwrap.fill(line, width=width,
                              initial_indent="  ", subsequent_indent="  "),
                markup=False, highlight=False,
            )
    else:
        state.console.print("  [dim](none given)[/dim]")

    state.console.rule()


def _do_copy_recipe() -> None:
    """Pick a recipe and save an exact copy under a new name."""
    recipe = _pick_recipe()
    if recipe is None:
        return

    try:
        new_name = _prompt("New recipe name", default=f"Copy of {recipe['name']}").strip()
    except Cancelled:
        return
    if not new_name or new_name.lower() == "b":
        return

    with _db.get_db() as conn:
        ingredients = _db.recipe_get_ingredients(conn, recipe["id"])
        new_id = _db.recipe_create(
            conn,
            new_name,
            recipe["description"],
            recipe["servings"],
            recipe["instructions"],
            recipe["total_volume"],
            recipe["total_volume_unit"],
            recipe["total_weight"],
            recipe["total_weight_unit"],
        )
        for ing in ingredients:
            _db.recipe_add_ingredient(
                conn, new_id,
                ing["fdc_id"], ing["food_name"],
                ing["amount"], ing["unit"],
                ing["notes"],
            )

    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Copied to: [bold]{new_name}[/bold]  "
        f"(ID {new_id})  with {len(ingredients)} ingredient(s)"
    )


def _menu_recipes() -> bool:
    """Recipes submenu. Returns True to go back, False to quit."""
    from .recipe_edit import _do_recipe_edit        # lazy — avoids circular import
    from .recipe_analysis import _do_recipe_view    # lazy — avoids circular import
    while True:
        _show_menu("Recipes", [
            ("1", "Create new recipe"),
            ("2", "List recipes"),
            ("3", "View recipe"),
            ("4", "Edit recipe"),
            ("5", "Analyze recipe"),
            ("6", "Delete recipe"),
            ("7", "Copy a recipe"),
            ("m", "Return to main menu"),
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
            _safe_call(_do_recipe_display)
        elif choice == "4":
            _safe_call(_do_recipe_edit)
        elif choice == "5":
            _safe_call(_do_recipe_view)
        elif choice == "6":
            _safe_call(_do_recipe_delete)
        elif choice == "7":
            _safe_call(_do_copy_recipe)
        elif choice in ("m", "b"):
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_recipe_create() -> None:
    try:
        name = _prompt("Recipe name", free_text=True).strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return

    # Collect each header field individually — Cancelled at any point uses the
    # field's default so the recipe is always saved with whatever was entered.
    try:
        description = _prompt("Description (optional)", default="", free_text=True).strip()
    except Cancelled:
        description = ""

    try:
        raw_servings = _prompt("Number of servings  [dim](0 = analyze by weight/volume)[/dim]", default="0", free_text=True).strip()
        servings = int(raw_servings) if raw_servings.isdigit() else 0
    except Cancelled:
        servings = 0

    try:
        serving_size = _prompt("Serving size  [dim](e.g. 1 cup, 1 slice — Enter to skip)[/dim]", default="", free_text=True).strip() or None
    except Cancelled:
        serving_size = None

    try:
        raw_vol = _prompt(
            "Total volume  [dim](e.g. 4 cups, 500 ml — Enter to skip)[/dim]",
            default="", free_text=True,
        ).strip()
        total_volume, total_volume_unit = _parse_measure(raw_vol)
    except Cancelled:
        total_volume, total_volume_unit = None, None

    try:
        raw_wt = _prompt(
            "Total weight  [dim](e.g. 800 g, 1.5 lb — Enter to skip)[/dim]",
            default="", free_text=True,
        ).strip()
        total_weight, total_weight_unit = _parse_measure(raw_wt)
    except Cancelled:
        total_weight, total_weight_unit = None, None

    try:
        raw_complete = _prompt("Mark as complete?", choices=["y", "n"], default="n")
        complete = raw_complete.lower() == "y"
    except Cancelled:
        complete = False

    with _db.get_db() as conn:
        recipe_id = _db.recipe_create(
            conn, name, description, servings, "",
            total_volume, total_volume_unit, total_weight, total_weight_unit,
            serving_size, complete,
        )

    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Recipe [{state.T['hi']}]{name}[/{state.T['hi']}] "
                  f"created (ID {recipe_id}).  Now add ingredients.")

    # Add ingredients loop
    while True:
        state.console.print()
        try:
            query = _prompt("Search food or recipe  [dim](Enter/b=done adding)[/dim]", free_text=True).strip()
        except Cancelled:
            break
        ql = query.lower()
        if not query or ql == "b":
            break
        if ql == "m":
            raise ReturnToMain()
        if ql == "q":
            raise SystemExit(0)

        with _db.get_db() as conn:
            all_recipes = _db.recipe_list(conn)
        query_words = ql.split()
        matching_recipes = [
            r for r in all_recipes
            if r["id"] != recipe_id and any(w in r["name"].lower() for w in query_words)
        ]
        food = _search_and_pick_food(
            initial_query=query,
            prepend_recipes=matching_recipes or None,
        )
        if food is None:
            continue

        if food.get("_type") == "recipe":
            sub_rid  = food["id"]
            sub_name = food["name"]
            try:
                raw_srv = _prompt(
                    "Servings of this recipe  [dim](e.g. 1, 0.5, 2 — b=back)[/dim]",
                    default="1",
                ).strip()
            except Cancelled:
                continue
            if not raw_srv or raw_srv.lower() == "b":
                continue
            servings = _parse_serving_amount(raw_srv)
            if servings is None or servings <= 0:
                state.console.print(f"[{state.T['warning']}]Enter a positive number.[/{state.T['warning']}]")
                continue
            try:
                notes = _prompt("Note  [dim](optional, Enter to skip)[/dim]", default="", free_text=True).strip() or None
            except Cancelled:
                notes = None
            with _db.get_db() as conn:
                _db.recipe_add_ingredient(conn, recipe_id, 0, sub_name, servings, "servings", notes, ref_recipe_id=sub_rid)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added recipe: {sub_name}  {_format_recipe_portion_label(servings)}")
        else:
            result = _pick_portion(food)
            if result is None:
                continue
            grams, label, _ = result
            try:
                notes = _prompt("Note for this ingredient  [dim](optional, Enter to skip)[/dim]", default="", free_text=True).strip() or None
            except Cancelled:
                notes = None
            with _db.get_db() as conn:
                _db.recipe_add_ingredient(conn, recipe_id, food["fdcId"],
                                          food["name"], grams, label, notes)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")

        try:
            cont = _prompt("Add another ingredient?", choices=["y", "n", "q"], default="y")
        except Cancelled:
            break
        if cont.lower() == "q":
            raise SystemExit(0)
        if cont.lower() != "y":
            break

    state.console.print(
        f"\n  [{state.T['accent']}]Procedure[/{state.T['accent']}]"
        "  [dim]— an editor will open. Save and close it to continue.[/dim]"
    )
    state.console.print("  [dim]Press Enter to open the editor, or b to skip.[/dim]")
    try:
        go = _prompt("").strip().lower()
        instructions = "" if go == "b" else _open_in_editor("").strip()
    except Cancelled:
        instructions = ""

    if instructions:
        with _db.get_db() as conn:
            conn.execute("UPDATE recipes SET instructions = ? WHERE id = ?", (instructions, recipe_id))

    state.console.print(f"[{state.T['success']}]Recipe saved.[/{state.T['success']}]")


def _do_recipe_list() -> None:
    with _db.get_db() as conn:
        all_recipes = _db.recipe_list(conn)
    if not all_recipes:
        state.console.print("[dim]No recipes saved yet.[/dim]")
        return

    try:
        query = _prompt("Search  [dim](Enter to list all, b=back)[/dim]", default="", free_text=True).strip()
    except Cancelled:
        return
    lowered = query.lower()
    if lowered == "q":
        raise SystemExit(0)
    if lowered == "m":
        raise ReturnToMain()
    if lowered == "b":
        return

    if query:
        recipes = [r for r in all_recipes if lowered in r["name"].lower()]
        if not recipes:
            state.console.print(f"[{state.T['warning']}]No recipes matching '{query}'.[/{state.T['warning']}]")
            return
    else:
        recipes = all_recipes

    offset = 0
    while True:
        _show_recipe_page(recipes, offset)
        has_more = offset + _RECIPE_PAGE < len(recipes)
        if not has_more and offset == 0:
            return
        hints = []
        if has_more:
            hints.append("more=next")
        if offset > 0:
            hints.append("prev=back")
        hints.append("b=done")
        try:
            raw = _prompt(f"  [dim]({', '.join(hints)})[/dim]").strip().lower()
        except Cancelled:
            return
        if raw in ("b", "", "q", "m"):
            if raw == "q":
                raise SystemExit(0)
            if raw == "m":
                raise ReturnToMain()
            return
        if raw == "more" and has_more:
            offset += _RECIPE_PAGE
        elif raw == "prev" and offset > 0:
            offset = max(0, offset - _RECIPE_PAGE)


def _do_recipe_delete() -> None:
    recipe = _pick_recipe()
    if recipe is None:
        return
    rid = recipe["id"]
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
