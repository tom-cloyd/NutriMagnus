import json

from .. import state
import db as _db
import usda as _usda
from ..services.portions import _pick_portion, _parse_portion_input
from ..services.search import _search_and_pick_food, _suggest_foundation_search
from ..ui.common import _safe_call, _show_menu
from ..ui.prompts import Cancelled, _prompt
from ..ui.render import _print_bioavailability, _print_complement_suggestions, _print_nutrient_table, _print_protein_completeness
from ..services.reports import _offer_export
from .pantry import _do_pantry_menu, _do_list_cached_foods
from .recipes import _do_recipe_list, _get_recipe_total_nutrients, _pick_recipe_portion

def _menu_foods() -> bool:
    """Foods submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Foods — Search & Analyze", [
            ("1", "Search food databases (USDA and others)"),
            ("2", "Analyze a USDA food portion"),
            ("3", "Analyze a saved recipe portion"),
            ("4", "Convert a portion <==> weight  (volume/weight conversion, no analysis)"),
            ("5", "View cached / saved foods"),
            ("6", "My pantry  (protein sources on hand)"),
            ("b", "Back to main menu"),
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
        elif choice == "b":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_food_search() -> None:
    food = _search_and_pick_food()
    if food is None:
        return
    _print_nutrient_table(food["nutrients"], title=food["name"], per_label="per 100g")
    has_aa = _print_protein_completeness(food["nutrients"])
    aa_food = food  # tracks whichever food has AA data for all subsequent steps
    if not has_aa:
        alt = _suggest_foundation_search(food)
        if alt:
            _print_nutrient_table(alt["nutrients"], title=alt["name"], per_label="per 100g")
            has_aa = _print_protein_completeness(alt["nutrients"])
            aa_food = alt
    _print_bioavailability(aa_food["name"], aa_food["nutrients"])
    if has_aa and _usda.get_aa_gaps(aa_food["nutrients"]):
        try:
            ans = _prompt("Show protein complement suggestions?  [dim](y/N)[/dim]",
                          default="n").strip().lower()
        except Cancelled:
            ans = "n"
        if ans == "y":
            _print_complement_suggestions(aa_food["nutrients"], context="food",
                                          offer_if_covered=False,
                                          base_food_name=aa_food["name"])

    try:
        ans = _prompt("Analyze a portion of this food?  [dim](y/N)[/dim]",
                      default="n").strip().lower()
    except Cancelled:
        return
    if ans != "y":
        return

    result = _pick_portion(aa_food)
    if result is None:
        return
    grams, label, scaled = result
    _print_nutrient_table(scaled, title=aa_food["name"], per_label=label)
    has_aa = _print_protein_completeness(scaled)
    _print_bioavailability(aa_food["name"], scaled)
    if has_aa and _usda.get_aa_gaps(scaled):
        try:
            ans = _prompt("Show protein complement suggestions?  [dim](y/N)[/dim]",
                          default="n").strip().lower()
        except Cancelled:
            ans = "n"
        if ans == "y":
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
    has_aa = _print_protein_completeness(scaled)
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
                has_aa = _print_protein_completeness(alt_scaled)
                _print_bioavailability(alt["name"], alt_scaled)
                export_name = f"{alt['name']} — {alt_label}"
                export_sections = [
                    {"type": "nutrient_table", "title": alt["name"],
                     "nutrients": alt_scaled, "per_label": alt_label},
                    {"type": "protein_completeness", "nutrients": alt_scaled},
                    {"type": "bioavailability", "food_name": alt["name"],
                     "nutrients": alt_scaled},
                ]
                if has_aa and _usda.get_aa_gaps(alt_scaled):
                    try:
                        ans = _prompt(
                            "Show protein complement suggestions?  [dim](y/N)[/dim]",
                            default="n").strip().lower()
                    except Cancelled:
                        ans = "n"
                    if ans == "y":
                        _print_complement_suggestions(alt_scaled, context="food",
                                                      offer_if_covered=False,
                                                      base_food_name=alt["name"])
    else:
        _print_bioavailability(food["name"], scaled)
        if _usda.get_aa_gaps(scaled):
            try:
                ans = _prompt("Show protein complement suggestions?  [dim](y/N)[/dim]",
                              default="n").strip().lower()
            except Cancelled:
                ans = "n"
            if ans == "y":
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
            raw = _prompt("Amount  (b=back, q=quit)").strip()
        except Cancelled:
            return
        if raw.lower() in ("b", ""):
            return
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
        raw = _prompt("Recipe ID  (Enter/b=back, q=quit)").strip()
    except Cancelled:
        return
    if not raw or raw.lower() in ("b", "back"):
        return
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
        try:
            ans = _prompt("Show protein complement suggestions?  [dim](y/N)[/dim]",
                          default="n").strip().lower()
        except Cancelled:
            ans = "n"
        if ans == "y":
            _print_complement_suggestions(scaled, context="recipe", offer_if_covered=True)

    _offer_export(f"{title} — {label}", [
        {"type": "ingredient_list", "title": "Ingredients",
         "items": [{"food_name": i["food_name"], "amount": i["amount"], "unit": i["unit"]} for i in ingredients]},
        {"type": "nutrient_table", "title": title, "nutrients": scaled, "per_label": label},
        {"type": "protein_completeness", "nutrients": scaled},
    ])
