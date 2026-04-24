"""
foods.py — Foods menu: food search, portion analysis, unit conversion, and cached-food viewer.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/foods.py — Foods menu"
"""
import json
from rich.table import Table

from .. import state
import db as _db
import usda as _usda
from ..services.portions import _pick_portion, _parse_portion_input
from ..services.search import _search_and_pick_food, _suggest_foundation_search
from ..ui.common import _id_cell, ID_KEY, _safe_call, _show_menu, _prompt_with_options, dot_cell, table_title, table_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_bioavailability, _print_complement_suggestions, _print_nutrient_table, _print_protein_completeness
from ..services.reports import _offer_export
from .pantry import _do_pantry_menu
from .recipes import _do_recipe_list, _get_recipe_total_nutrients, _pick_recipe_portion
from .drafted_foods import _do_edit_cached_food, _do_drafted_foods_menu

def _menu_foods() -> bool:
    """Foods submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Foods — Search & Analyze", [
            ("1", "Search food databases (USDA + Open Food Facts)"),
            ("2", "Analyze a food portion  (USDA + Open Food Facts)"),
            ("3", "Analyze a saved recipe portion"),
            ("4", "Convert a portion <==> weight  (volume/weight conversion, no analysis)"),
            ("5", "View cached / saved foods"),
            ("6", "My pantry  (protein sources on hand)"),
            ("7", "Drafted food profiles  (custom nutrient profiles)"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[dim]Cancelled.[/dim]")
            return True

        if choice == "1":
            _safe_call(_do_food_search)
        elif choice == "2":
            _safe_call(_do_analyze_food_portion)
        elif choice == "3":
            _safe_call(_do_analyze_recipe_portion)
        elif choice == "4":
            _safe_call(_do_convert_portion)
        elif choice == "5":
            _safe_call(_do_list_cached_foods)
        elif choice == "6":
            _safe_call(_do_pantry_menu)
        elif choice == "7":
            _safe_call(_do_drafted_foods_menu)
        elif choice == "m":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_food_search() -> None:
    try:
        query = _prompt("Search food or recipe", free_text=True).strip()
    except Cancelled:
        return
    if not query or query.lower() in ("b", "m", "q"):
        return
    ql = query.lower()
    with _db.get_db() as conn:
        all_recipes = _db.recipe_list(conn)
    query_words = ql.split()
    matching_recipes = sorted(
        [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)],
        key=lambda r: (-sum(1 for w in query_words if w in r["name"].lower()), r["name"].lower()),
    )
    food = _search_and_pick_food(initial_query=query, prepend_recipes=matching_recipes or None)
    if food is None:
        return
    _print_nutrient_table(food["nutrients"], title=food["name"], per_label="per 100g")
    has_aa = _print_protein_completeness(food["nutrients"], food_name=food["name"])
    aa_food = food  # tracks whichever food has AA data for all subsequent steps
    if not has_aa:
        alt = _suggest_foundation_search(food)
        if alt:
            _print_nutrient_table(alt["nutrients"], title=alt["name"], per_label="per 100g")
            has_aa = _print_protein_completeness(alt["nutrients"], food_name=alt["name"])
            aa_food = alt
    _print_bioavailability(aa_food["name"], aa_food["nutrients"])
    _aa_diaas = _usda.get_diaas(aa_food["name"]) or 1.0
    if has_aa and _usda.get_aa_gaps(aa_food["nutrients"], digestibility=_aa_diaas):
        _print_complement_suggestions(aa_food["nutrients"], context="food",
                                      offer_if_covered=False,
                                      base_food_name=aa_food["name"])

    try:
        ans = _prompt("Analyze a portion of this food?  [dim](y/N)[/dim]",
                      choices=["y", "n"], default="n")
    except Cancelled:
        return
    if ans != "y":
        return

    result = _pick_portion(aa_food)
    if result is None:
        return
    grams, label, scaled = result
    _print_nutrient_table(scaled, title=aa_food["name"], per_label=label)
    has_aa = _print_protein_completeness(scaled, food_name=aa_food["name"])
    _print_bioavailability(aa_food["name"], scaled)
    if has_aa and _usda.get_aa_gaps(scaled, digestibility=_aa_diaas):
        _print_complement_suggestions(scaled, context="food", offer_if_covered=False,
                                      base_food_name=aa_food["name"])


def _do_analyze_food_portion() -> None:
    food = _search_and_pick_food()
    if food is None:
        return
    result = _pick_portion(food)
    if result is None:
        return
    grams, label, scaled = result
    _print_nutrient_table(scaled, title=food["name"], per_label=label)
    has_aa = _print_protein_completeness(scaled, food_name=food["name"])
    # export_name / export_sections track what to offer for export at the end
    export_name = f"{food['name']} — {label}"
    export_sections: list[dict] = [
        {"type": "nutrient_table", "title": food["name"],
         "nutrients": scaled, "per_label": label},
        {"type": "protein_completeness", "nutrients": scaled},
        {"type": "bioavailability", "food_name": food["name"], "nutrients": scaled},
    ]
    if not has_aa:
        alt = _suggest_foundation_search(food)
        if alt:
            alt_result = _pick_portion(alt)
            if alt_result:
                alt_grams, alt_label, alt_scaled = alt_result
                _print_nutrient_table(alt_scaled, title=alt["name"],
                                      per_label=alt_label)
                has_aa = _print_protein_completeness(alt_scaled, food_name=alt["name"])
                _print_bioavailability(alt["name"], alt_scaled)
                export_name = f"{alt['name']} — {alt_label}"
                export_sections = [
                    {"type": "nutrient_table", "title": alt["name"],
                     "nutrients": alt_scaled, "per_label": alt_label},
                    {"type": "protein_completeness", "nutrients": alt_scaled},
                    {"type": "bioavailability", "food_name": alt["name"],
                     "nutrients": alt_scaled},
                ]
                _alt_diaas = _usda.get_diaas(alt["name"]) or 1.0
                if has_aa and _usda.get_aa_gaps(alt_scaled, digestibility=_alt_diaas):
                    _print_complement_suggestions(alt_scaled, context="food",
                                                  offer_if_covered=False,
                                                  base_food_name=alt["name"])
    else:
        _print_bioavailability(food["name"], scaled)
        _food_diaas = _usda.get_diaas(food["name"]) or 1.0
        if _usda.get_aa_gaps(scaled, digestibility=_food_diaas):
            _print_complement_suggestions(scaled, context="food", offer_if_covered=False,
                                          base_food_name=food["name"])
    _offer_export(export_name, export_sections)


def _do_convert_portion() -> None:
    """Convert a volume or weight to grams (or vice-versa) without nutritional analysis."""
    food = _search_and_pick_food()
    if food is None:
        return

    portions = food.get("portions", [])
    food_name = food.get("name", "")
    density = _usda.get_density_g_per_ml(food_name, portions)

    state.console.print(f"\n  Food: [bold]{food_name}[/bold]")
    if density is not None:
        state.console.print(f"  [dim]Weight: {density:.3f} g/ml[/dim]")
    state.console.print(f"  Enter an amount: 150 (g/gr), 3 oz, 0.5 lb, 1/4 c (cup), 2 T (tbsp), 1 t (tsp)")

    while True:
        try:
            raw = _prompt("Amount  (b=back, m=main, q=quit)").strip()
        except Cancelled:
            return
        if raw.lower() in ("b", ""):
            return
        if raw.lower() == "m":
            raise ReturnToMain()
        if raw.lower() == "q":
            raise SystemExit(0)

        result = _parse_portion_input(raw, portions, food_name)

        if result is None:
            state.console.print(f"[{state.T['warning']}]Not recognised. Try: 150, 65 gr, 3 oz, 1/4 cup, 2 T, 1 t, or p1.[/{state.T['warning']}]")
            continue
        if isinstance(result, str):
            state.console.print(f"[{state.T['warning']}]{result}[/{state.T['warning']}]")
            continue

        grams, label = result
        state.console.print(f"\n  [bold]{label}[/bold]  =  [bold]{grams:.1f} g[/bold]\n")


def _do_analyze_recipe_portion() -> None:
    _do_recipe_list()
    try:
        raw = _prompt("Recipe ID  (Enter/b=back, m=main, q=quit)").strip()
    except Cancelled:
        return
    if not raw or raw.lower() in ("b", "back"):
        return
    if raw.lower() == "m":
        raise ReturnToMain()
    if raw.lower() == "q":
        raise SystemExit(0)
    try:
        rid = int(raw)
    except ValueError:
        state.console.print(f"[{state.T['warning']}]Invalid recipe ID.[/{state.T['warning']}]")
        return

    recipe, ingredients, combined = _get_recipe_total_nutrients(rid)
    if recipe is None:
        state.console.print(f"[{state.T['warning']}]Recipe {rid} not found.[/{state.T['warning']}]")
        return
    if not combined:
        state.console.print(f"[{state.T['warning']}]Recipe has no analyzable ingredients yet.[/{state.T['warning']}]")
        return

    portion = _pick_recipe_portion(recipe)
    if portion is None:
        return
    servings, label = portion
    total_servings = recipe["servings"] or 1
    factor = servings / total_servings
    scaled = {k: v * factor for k, v in combined.items()}

    title = recipe["name"]
    _print_nutrient_table(scaled, title=title, per_label=label)
    has_aa = _print_protein_completeness(scaled)
    if has_aa and _usda.get_aa_gaps(scaled):
        _print_complement_suggestions(scaled, context="recipe", offer_if_covered=True)

    _offer_export(f"{title} — {label}", [
        {"type": "ingredient_list", "title": "Ingredients",
         "items": [{"food_name": i["food_name"], "amount": i["amount"], "unit": i["unit"]} for i in ingredients]},
        {"type": "nutrient_table", "title": title, "nutrients": scaled, "per_label": label},
        {"type": "protein_completeness", "nutrients": scaled},
    ])


# ---------------------------------------------------------------------------
# Cached food viewer / editor
# ---------------------------------------------------------------------------

def _do_list_cached_foods() -> None:
    filter_text: str | None = None
    while True:
        with _db.get_db() as conn:
            all_foods = _db.list_cached_foods(conn)
        if not all_foods:
            state.console.print("[dim]No foods cached yet.[/dim]")
            return

        if filter_text:
            fl = filter_text.lower()
            foods = [f for f in all_foods if fl in f["name"].lower()
                     or (f["brand"] and fl in f["brand"].lower())]
        else:
            foods = list(all_foods)

        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",     justify="right", min_width=3)
        tbl.add_column("Name",  min_width=40)
        tbl.add_column("Type",  min_width=14)
        tbl.add_column("Brand", min_width=20)
        for i, f in enumerate(foods, 1):
            tbl.add_row(str(i), f["name"], f["data_type"] or "", f["brand"] or "")

        if filter_text:
            table_title("Cached Foods",
                        f"[dim]{len(foods)} match for '[bold]{filter_text}[/bold]' "
                        f"({len(all_foods)} total) — enter / to clear filter[/dim]")
        else:
            table_title("Cached Foods",
                        f"[dim]{len(all_foods)} foods — enter /text to filter by name[/dim]")

        state.console.print(tbl)
        table_footer("  [dim]To refresh a corrupt or outdated entry: delete it here, "
                     "then re-search — it will be re-fetched automatically.[/dim]")

        try:
            raw = _prompt("Pick number  (/filter, Enter/b=back, m=main, q=quit)").strip()
        except Cancelled:
            return

        raw_lower = raw.lower()
        if not raw or raw_lower == "b":
            return
        if raw_lower == "m":
            raise ReturnToMain()
        if raw_lower == "q":
            raise SystemExit(0)
        if raw.startswith("/"):
            filter_text = raw[1:].strip() or None
            continue

        try:
            idx = int(raw) - 1
            if idx < 0 or idx >= len(foods):
                raise ValueError
        except ValueError:
            state.console.print(f"[{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
            continue

        row = foods[idx]
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, row["fdc_id"])
        if not cached:
            state.console.print(f"[{state.T['error']}]Food not found in cache.[/{state.T['error']}]")
            continue

        food = {
            "fdcId":            cached["fdc_id"],
            "name":             cached["name"],
            "dataType":         cached["data_type"],
            "brand":            cached["brand"],
            "servingSize":      cached["serving_size"],
            "servingUnit":      cached["serving_unit"],
            "householdServing": None,
            "nutrients":        json.loads(cached["nutrients_json"]),
            "portions":         json.loads(cached["portions_json"]),
        }

        try:
            action = _prompt_with_options(
                "Cached food action",
                [
                    ("1", "View nutrients"),
                    ("2", "Analyze portion"),
                    ("3", "Edit nutrients"),
                    ("d", "Delete from cache"),
                ],
                default="1",
            )
        except Cancelled:
            continue

        if action == "3":
            _do_edit_cached_food(row["fdc_id"], cached)
        elif action == "d":
            try:
                confirm = _prompt(
                    f"Delete [bold]{row['name']}[/bold] from cache?  "
                    f"[dim]Recipes using it will need to re-fetch on next analysis.  (y/N)[/dim]",
                    default="n",
                ).strip().lower()
            except Cancelled:
                continue
            if confirm == "y":
                with _db.get_db() as conn:
                    deleted = _db.delete_cached_food(conn, row["fdc_id"])
                if deleted:
                    state.console.print(
                        f"  [{state.T['success']}]✓[/{state.T['success']}]  Deleted '{row['name']}' from cache."
                    )
                else:
                    state.console.print(f"  [{state.T['warning']}]Not found — may have already been removed.[/{state.T['warning']}]")
        elif action == "2":
            result = _pick_portion(food)
            if result is None:
                continue
            grams, label, scaled = result
            _print_nutrient_table(scaled, title=food["name"], per_label=label)
            _print_protein_completeness(scaled, food_name=food["name"])
        else:
            _print_nutrient_table(food["nutrients"], title=food["name"], per_label="per 100g")
            _print_protein_completeness(food["nutrients"], food_name=food["name"])


