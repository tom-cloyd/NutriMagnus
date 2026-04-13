import json
from rich.table import Table

from .. import state
import db as _db
import usda as _usda
from ..services.portions import _pick_portion, _parse_portion_input
from ..services.search import _search_and_pick_food, _suggest_foundation_search
from ..ui.common import _safe_call, _show_menu
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_bioavailability, _print_complement_suggestions, _print_nutrient_table, _print_protein_completeness
from ..services.reports import _offer_export
from .pantry import _do_pantry_menu, _do_list_cached_foods
from .recipes import _do_recipe_list, _get_recipe_total_nutrients, _pick_recipe_portion

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


# ---------------------------------------------------------------------------
# Drafted food profiles
# ---------------------------------------------------------------------------

# Ordered list of (nutrient_key, display_label, unit) for user prompting.
# Split into two groups: basic macros (always prompted) and optional extras.
_DRAFT_MACROS = [
    ("calories",         "Calories",           "kcal"),
    ("protein_g",        "Protein",            "g"),
    ("fat_g",            "Total fat",          "g"),
    ("carb_g",           "Carbohydrates",      "g"),
    ("fiber_g",          "Fiber",              "g"),
    ("sugar_g",          "Sugars",             "g"),
    ("saturated_fat_g",  "Saturated fat",      "g"),
    ("sodium_mg",        "Sodium",             "mg"),
    ("calcium_mg",       "Calcium",            "mg"),
    ("iron_mg",          "Iron",               "mg"),
]

_DRAFT_AMINO_ACIDS = [
    ("aa_tryptophan_g",   "Tryptophan",    "g"),
    ("aa_threonine_g",    "Threonine",     "g"),
    ("aa_isoleucine_g",   "Isoleucine",    "g"),
    ("aa_leucine_g",      "Leucine",       "g"),
    ("aa_lysine_g",       "Lysine",        "g"),
    ("aa_methionine_g",   "Methionine",    "g"),
    ("aa_cystine_g",      "Cystine",       "g"),
    ("aa_phenylalanine_g","Phenylalanine", "g"),
    ("aa_tyrosine_g",     "Tyrosine",      "g"),
    ("aa_valine_g",       "Valine",        "g"),
    ("aa_histidine_g",    "Histidine",     "g"),
]

# Maps every name/abbreviation a literature source might use to the program's
# internal nutrient key.  Keys are lowercase; matching is case-insensitive.
_AA_NAME_LOOKUP: dict[str, str] = {
    # Tryptophan
    "tryptophan": "aa_tryptophan_g",  "trp": "aa_tryptophan_g",  "w": "aa_tryptophan_g",
    # Threonine
    "threonine":  "aa_threonine_g",   "thr": "aa_threonine_g",   "t": "aa_threonine_g",
    # Isoleucine
    "isoleucine": "aa_isoleucine_g",  "ile": "aa_isoleucine_g",  "i": "aa_isoleucine_g",
    # Leucine
    "leucine":    "aa_leucine_g",     "leu": "aa_leucine_g",     "l": "aa_leucine_g",
    # Lysine
    "lysine":     "aa_lysine_g",      "lys": "aa_lysine_g",      "k": "aa_lysine_g",
    # Methionine
    "methionine": "aa_methionine_g",  "met": "aa_methionine_g",  "m": "aa_methionine_g",
    # Cystine — accept cysteine too (they differ by one hydrogen; literature uses both)
    "cystine":    "aa_cystine_g",     "cysteine": "aa_cystine_g",
    "cys":        "aa_cystine_g",     "c": "aa_cystine_g",
    # Phenylalanine
    "phenylalanine": "aa_phenylalanine_g", "phe": "aa_phenylalanine_g", "f": "aa_phenylalanine_g",
    # Tyrosine
    "tyrosine":   "aa_tyrosine_g",    "tyr": "aa_tyrosine_g",    "y": "aa_tyrosine_g",
    # Valine
    "valine":     "aa_valine_g",      "val": "aa_valine_g",      "v": "aa_valine_g",
    # Histidine
    "histidine":  "aa_histidine_g",   "his": "aa_histidine_g",   "h": "aa_histidine_g",
}

# Non-essential AAs we recognize by name but do not store.
_AA_NON_ESSENTIAL: set[str] = {
    "arginine", "arg", "r",
    "alanine", "ala", "a",
    "aspartate", "aspartic", "aspartic acid", "asparagine", "asp", "asn", "d", "n",
    "glutamate", "glutamic", "glutamic acid", "glutamine", "glu", "gln", "e", "q",
    "glycine", "gly", "g",
    "proline", "pro", "p",
    "serine", "ser", "s",
    "hydroxyproline", "hyp",
    "selenocysteine", "sec", "u",
}


def _bulk_import_aa(protein_g: float | None) -> dict:
    """
    Accept amino acid values entered as 'name: value' pairs, one per prompt.
    If protein_g is provided, treats input as g per 100g protein and converts
    to g per 100g food.  If protein_g is None or 0, treats input as g per 100g
    food directly.  Returns a dict of {aa_key: value_per_100g_food}.
    """
    from_protein = (protein_g is not None and protein_g > 0)

    state.console.print(
        f"\n  [{state.T['accent']}]— Bulk amino acid import —[/{state.T['accent']}]"
    )
    if from_protein:
        state.console.print(
            f"  [dim]Input unit: [bold]g per 100g protein[/bold]  "
            f"(protein content: {protein_g:.2g} g/100g food)\n"
            f"  Values will be converted automatically: "
            f"aa_food = aa_protein × {protein_g:.2g} / 100[/dim]\n"
            f"  [dim]Accepted names: full name, 3-letter code, or 1-letter code "
            f"(e.g. tryptophan, trp, W)[/dim]\n"
            f"  [dim]Enter one amino acid per line as   name: value   "
            f"— press Enter on a blank line when done.[/dim]"
        )
    else:
        state.console.print(
            f"  [dim]Input unit: [bold]g per 100g food[/bold]\n"
            f"  Accepted names: full name, 3-letter code, or 1-letter code "
            f"(e.g. tryptophan, trp, W)\n"
            f"  Enter one amino acid per line as   name: value   "
            f"— press Enter on a blank line when done.[/dim]"
        )

    raw_entries: list[tuple[str, float]] = []   # (raw_name, raw_value)

    while True:
        try:
            line = _prompt("  AA").strip()
        except Cancelled:
            break
        if not line or line.lower() == "b":
            break
        if line.lower() == "q":
            raise SystemExit(0)

        # Accept "name: value", "name = value", or "name value"
        import re as _re
        m = _re.match(r"^([a-zA-Z][\w\s-]*)[\s:=]+([0-9.]+)\s*$", line)
        if not m:
            state.console.print(
                f"    [{state.T['warning']}]Format not recognised — "
                f"enter as  name: value  (e.g. lysine: 4.8)[/{state.T['warning']}]"
            )
            continue
        name_raw = m.group(1).strip()
        try:
            value = float(m.group(2))
        except ValueError:
            state.console.print(f"    [{state.T['warning']}]Value must be a number.[/{state.T['warning']}]")
            continue
        raw_entries.append((name_raw, value))

    if not raw_entries:
        return {}

    # Classify each entry
    stored:       list[tuple[str, str, float, float]] = []  # (raw_name, key, raw_val, stored_val)
    non_essential: list[tuple[str, float]] = []             # (raw_name, raw_val)
    unrecognized:  list[tuple[str, float]] = []             # (raw_name, raw_val)

    for name_raw, value in raw_entries:
        key_lookup = name_raw.lower().strip()
        if key_lookup in _AA_NAME_LOOKUP:
            aa_key = _AA_NAME_LOOKUP[key_lookup]
            stored_val = value * protein_g / 100.0 if from_protein else value
            stored.append((name_raw, aa_key, value, stored_val))
        elif key_lookup in _AA_NON_ESSENTIAL:
            non_essential.append((name_raw, value))
        else:
            unrecognized.append((name_raw, value))

    # Summary display
    state.console.print()
    if stored:
        state.console.print(f"  [{state.T['success']}]Recognized and stored:[/{state.T['success']}]")
        label_map = {key: label for key, label, _ in _DRAFT_AMINO_ACIDS}
        for name_raw, aa_key, raw_val, stored_val in stored:
            label = label_map.get(aa_key, aa_key)
            if from_protein:
                state.console.print(
                    f"    [{state.T['hi']}]{label:<16}[/{state.T['hi']}]"
                    f"  {raw_val:.4g} g/100g protein  →  {stored_val:.5g} g/100g food  "
                    f"[{state.T['success']}]✓[/{state.T['success']}]"
                )
            else:
                state.console.print(
                    f"    [{state.T['hi']}]{label:<16}[/{state.T['hi']}]"
                    f"  {stored_val:.5g} g/100g food  [{state.T['success']}]✓[/{state.T['success']}]"
                )
    if non_essential:
        state.console.print(f"  [dim]Not stored (non-essential, not tracked by this program):[/dim]")
        for name_raw, val in non_essential:
            state.console.print(f"    [dim]{name_raw}: {val:.4g}[/dim]")
    if unrecognized:
        state.console.print(f"  [{state.T['warning']}]Unrecognized names — not stored:[/{state.T['warning']}]")
        for name_raw, val in unrecognized:
            state.console.print(
                f"    [{state.T['warning']}]{name_raw}: {val:.4g}[/{state.T['warning']}]  "
                f"[dim](check spelling; accepted: full name, 3-letter, or 1-letter code)[/dim]"
            )

    return {aa_key: stored_val for _, aa_key, _, stored_val in stored}


def _list_drafted_foods() -> list:
    """Print a table of all user-drafted foods and return the rows."""
    with _db.get_db() as conn:
        rows = _db.list_user_drafted_foods(conn)
    if not rows:
        state.console.print("[dim]No drafted food profiles yet.[/dim]")
        return []
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("ID",   justify="right", min_width=5)
    tbl.add_column("Name", min_width=36)
    tbl.add_column("Note", min_width=24)
    for r in rows:
        tbl.add_row(str(r["fdc_id"]), r["name"], r["notes"] or "")
    state.console.print(tbl)
    return list(rows)


def _prompt_nutrients(existing: dict | None = None) -> dict:
    """
    Interactively prompt for nutrient values (per 100 g).
    existing: pre-fill from this dict if provided (e.g. loaded from USDA cache).
    Returns a nutrients dict.
    """
    state.console.print(
        f"\n  [dim]Enter nutrient values per [bold]100 g[/bold]. "
        f"Press Enter to keep the current value, or enter a number to override.[/dim]"
    )
    nutrients: dict = {}

    state.console.print(f"\n  [{state.T['accent']}]— Basic nutrients —[/{state.T['accent']}]")
    for key, label, unit in _DRAFT_MACROS:
        current = existing.get(key) if existing else None
        default_str = f"{current:.4g}" if current is not None else None
        while True:
            try:
                raw = _prompt(
                    f"  {label} ({unit}/100g)",
                    default=default_str if default_str else ""
                ).strip()
            except Cancelled:
                raw = ""
            if raw.lower() == "q":
                raise SystemExit(0)
            if not raw:
                if current is not None:
                    nutrients[key] = current
                break
            try:
                nutrients[key] = float(raw)
                break
            except ValueError:
                state.console.print(f"    [{state.T['warning']}]Enter a number (or press Enter to skip).[/{state.T['warning']}]")

    # Amino acids are optional — offer three choices
    state.console.print()
    state.console.print(
        f"  [{state.T['accent']}]Amino acid profile[/{state.T['accent']}]"
        f"  [dim](enables protein completeness analysis)[/dim]"
    )
    state.console.print("  [dim]1[/dim]  Enter values one-by-one (g per 100g food)")
    state.console.print("  [dim]2[/dim]  Bulk import from literature (g per 100g protein — auto-converted)")
    state.console.print("  [dim]n[/dim]  Skip")

    while True:
        try:
            aa_choice = _prompt("  Choice", choices=["1", "2", "n"], default="n").strip().lower()
        except Cancelled:
            aa_choice = "n"
        if aa_choice in ("1", "2", "n"):
            break

    if aa_choice == "1":
        state.console.print(f"\n  [{state.T['accent']}]— Amino acids (g per 100g food) —[/{state.T['accent']}]")
        state.console.print("  [dim]All are optional. Press Enter to skip any.[/dim]")
        for key, label, unit in _DRAFT_AMINO_ACIDS:
            current = existing.get(key) if existing else None
            default_str = f"{current:.5g}" if current is not None else None
            while True:
                try:
                    raw = _prompt(
                        f"  {label}",
                        default=default_str if default_str else ""
                    ).strip()
                except Cancelled:
                    raw = ""
                if raw.lower() == "q":
                    raise SystemExit(0)
                if not raw:
                    if current is not None:
                        nutrients[key] = current
                    break
                try:
                    nutrients[key] = float(raw)
                    break
                except ValueError:
                    state.console.print(f"    [{state.T['warning']}]Enter a number (or press Enter to skip).[/{state.T['warning']}]")

    elif aa_choice == "2":
        protein_g = nutrients.get("protein_g")
        bulk_result = _bulk_import_aa(protein_g)
        nutrients.update(bulk_result)

    return nutrients


def _do_drafted_foods_menu() -> None:
    while True:
        _show_menu("Drafted Food Profiles", [
            ("1", "List drafted profiles"),
            ("2", "Create new drafted profile"),
            ("3", "Edit a drafted profile"),
            ("4", "Delete a drafted profile"),
            ("b", "Back to Foods menu"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return

        if choice == "1":
            _list_drafted_foods()

        elif choice == "2":
            _do_create_drafted_food()

        elif choice == "3":
            rows = _list_drafted_foods()
            if not rows:
                continue
            fdc_id = _ask_int("Profile ID to edit")
            if fdc_id is None:
                continue
            row = next((r for r in rows if r["fdc_id"] == fdc_id), None)
            if row is None:
                state.console.print(f"[{state.T['warning']}]ID {fdc_id} not found.[/{state.T['warning']}]")
                continue
            _do_edit_drafted_food(fdc_id, row)

        elif choice == "4":
            rows = _list_drafted_foods()
            if not rows:
                continue
            fdc_id = _ask_int("Profile ID to delete")
            if fdc_id is None:
                continue
            row = next((r for r in rows if r["fdc_id"] == fdc_id), None)
            if row is None:
                state.console.print(f"[{state.T['warning']}]ID {fdc_id} not found.[/{state.T['warning']}]")
                continue
            try:
                confirm = _prompt(
                    f"Delete [{state.T['hi']}]{row['name']}[/{state.T['hi']}]?",
                    choices=["y", "n"], default="n"
                )
            except Cancelled:
                continue
            if confirm.lower() == "y":
                with _db.get_db() as conn:
                    conn.execute("DELETE FROM foods WHERE fdc_id = ? AND user_drafted = 1", (fdc_id,))
                state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Deleted.")

        elif choice == "b":
            return
        elif choice == "m":
            raise ReturnToMain()
        elif choice == "q":
            raise SystemExit(0)
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_create_drafted_food() -> None:
    state.console.print(
        f"\n  [{state.T['hi']}]Create a drafted food profile[/{state.T['hi']}]\n"
        f"  [dim]Drafted profiles let you build a best-guess nutrient profile for foods\n"
        f"  lacking complete official data. All values are per 100 g.[/dim]\n"
    )
    try:
        start = _prompt(
            "Start from a USDA food (pre-fill values) or from scratch?",
            choices=["u", "s"], default="s"
        ).strip().lower()
    except Cancelled:
        return

    existing_nutrients: dict = {}
    default_name = ""
    default_serving_size: float | None = None
    default_serving_unit: str | None = None

    if start == "u":
        food = _search_and_pick_food()
        if food is None:
            return
        existing_nutrients = dict(food.get("nutrients") or {})
        default_name = food.get("name", "")
        default_serving_size = food.get("servingSize")
        default_serving_unit = food.get("servingUnit")
        state.console.print(
            f"\n  [dim]Loaded: [bold]{default_name}[/bold] — "
            f"you can override any value below.[/dim]"
        )

    # Name
    try:
        name = _prompt("Food name", default=default_name).strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return

    # Serving size (optional metadata — not used in nutrient calculations)
    try:
        srv_raw = _prompt(
            "Serving size  [dim](e.g. 30, or Enter to skip)[/dim]",
            default=f"{default_serving_size:.0f}" if default_serving_size else ""
        ).strip()
    except Cancelled:
        srv_raw = ""
    serving_size: float | None = None
    if srv_raw:
        try:
            serving_size = float(srv_raw)
        except ValueError:
            pass

    try:
        serving_unit = _prompt(
            "Serving unit  [dim](e.g. g, oz, cup — or Enter to skip)[/dim]",
            default=default_serving_unit or ""
        ).strip() or None
    except Cancelled:
        serving_unit = None

    # Nutrients
    nutrients = _prompt_nutrients(existing_nutrients if existing_nutrients else None)

    # Note
    try:
        notes = _prompt(
            "Note  [dim](document your sources/assumptions — optional)[/dim]",
            default=""
        ).strip() or None
    except Cancelled:
        notes = None

    # Assign a negative fdc_id and save
    with _db.get_db() as conn:
        fdc_id = _db.next_user_drafted_fdc_id(conn)
        _db.cache_food(
            conn, fdc_id, name, "User Drafted",
            brand=None,
            serving_size=serving_size,
            serving_unit=serving_unit,
            nutrients=nutrients,
            portions=[],
            user_drafted=True,
            notes=notes,
        )

    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Drafted profile saved: "
        f"[bold]{name}[/bold]  (ID {fdc_id})"
    )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label="per 100g")


def _do_edit_drafted_food(fdc_id: int, row) -> None:
    state.console.print(
        f"\n  [{state.T['hi']}]Editing:[/{state.T['hi']}] [bold]{row['name']}[/bold]  (ID {fdc_id})\n"
        f"  [dim]Press Enter to keep the current value for each field.[/dim]\n"
    )

    # Load existing nutrients
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    existing_nutrients: dict = {}
    if cached and cached["nutrients_json"]:
        existing_nutrients = json.loads(cached["nutrients_json"])

    # Name
    try:
        name = _prompt("Food name", default=row["name"]).strip()
    except Cancelled:
        return
    if not name:
        name = row["name"]

    # Serving size
    current_srv = cached["serving_size"] if cached else None
    current_unit = cached["serving_unit"] if cached else None
    try:
        srv_raw = _prompt(
            "Serving size  [dim](Enter to keep)[/dim]",
            default=f"{current_srv:.0f}" if current_srv else ""
        ).strip()
    except Cancelled:
        srv_raw = ""
    serving_size: float | None = current_srv
    if srv_raw:
        try:
            serving_size = float(srv_raw)
        except ValueError:
            pass

    try:
        serving_unit = _prompt(
            "Serving unit  [dim](Enter to keep)[/dim]",
            default=current_unit or ""
        ).strip() or current_unit
    except Cancelled:
        serving_unit = current_unit

    # Nutrients
    nutrients = _prompt_nutrients(existing_nutrients)

    # Note
    try:
        notes = _prompt(
            "Note  [dim](Enter to keep, '-' to clear)[/dim]",
            default=row["notes"] or ""
        ).strip()
    except Cancelled:
        notes = row["notes"] or ""
    if notes == "-":
        notes = ""

    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id, name, nutrients,
            data_type="User Drafted",
            serving_size=serving_size,
            serving_unit=serving_unit,
            notes=notes or None,
            user_drafted=True,
        )

    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Profile updated: [bold]{name}[/bold]"
    )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label="per 100g")
