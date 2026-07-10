"""
foods.py — Foods menu: food search, portion analysis, unit conversion, and cached-food viewer.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/foods.py — Foods menu"
"""
import json
import pathlib
import re
from rich.table import Table

from .. import state
import db as _db
import usda as _usda
from ..services.portions import _pick_portion, _parse_portion_input
from ..services.search import _search_and_pick_food, _suggest_foundation_search, _fetch_food_from_result, _parse_hash_pick
from ..ui.common import _id_cell, ID_KEY, _safe_call, _show_menu, _prompt_with_options, dot_cell, table_title, table_footer, help_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _ask_float, _prompt
from ..ui.render import _print_bioavailability, _print_complement_suggestions, _get_daily_context, _print_nutrient_table, _print_protein_completeness
from ..services.annotations import annotate_food_interactive
from ..services.reports import _offer_export
from .pantry import _do_pantry_menu
from .recipes import _do_recipe_list, _get_recipe_total_nutrients, _pick_recipe_portion
from .drafted_foods import _do_edit_cached_food, _do_drafted_foods_menu

def _menu_foods() -> bool:
    """Foods submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Foods — Search, Analyze & Manage", [
            ("1", "Search food databases  (USDA + Open Food Facts / display or output data)"),
            ("2", "Analyze a food portion"),
            ("3", "Analyze a saved recipe portion"),
            ("4", "Convert a portion <==> weight  (volume/weight, no analysis)"),
            ("5", "Compare foods  (side-by-side nutrient table, up to 8)"),
            ("6", "Food Cache  (foods you have looked up: view, manage, get additional information)"),
            ("7", "My pantry  (foods you have on hand)"),
            ("8", "Custom food profiles  (create and edit your own food data)"),
            ("9", "Annotate a food  (add your GI / DIAAS estimates)"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[grey62]Cancelled.[/grey62]")
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
            _safe_call(_do_compare_foods)
        elif choice == "6":
            _safe_call(_do_list_cached_foods)
        elif choice == "7":
            _safe_call(_do_pantry_menu)
        elif choice == "8":
            _safe_call(_do_drafted_foods_menu)
        elif choice == "9":
            _safe_call(_do_annotate_food)
        elif choice in ("m", "b"):
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_food_search() -> None:
    try:
        query = _prompt(
            "Search food or recipe  [grey62](name · FDC ID · barcode · Enter/b=back · dout <id…>=output data)[/grey62]",
            free_text=True,
        ).strip()
    except Cancelled:
        return
    if not query or query.lower() in ("b", "m", "q"):
        return

    ql = query.lower()
    if ql.startswith("dout"):
        _do_dout(query[4:].strip())
        return
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

    if food.get("_type") == "recipe":
        from .recipe_analysis import _do_recipe_view
        _do_recipe_view(food)
        return

    daily_nutrients, rda = _get_daily_context()
    _print_nutrient_table(food["nutrients"], title=food["name"], per_label="per 100g",
                          daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
    has_aa = _print_protein_completeness(food["nutrients"], food_name=food["name"])
    _print_bioavailability(food["name"], food["nutrients"])
    aa_food = food  # tracks whichever food has AA data for all subsequent steps
    if not has_aa:
        alt = _suggest_foundation_search(food)
        if alt:
            _print_nutrient_table(alt["nutrients"], title=alt["name"], per_label="per 100g",
                                  daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
            has_aa = _print_protein_completeness(alt["nutrients"], food_name=alt["name"])
            _print_bioavailability(alt["name"], alt["nutrients"])
            aa_food = alt
    _aa_diaas = _usda.get_diaas(aa_food["name"]) or 1.0
    if has_aa and _usda.get_aa_gaps(aa_food["nutrients"], digestibility=_aa_diaas):
        _print_complement_suggestions(aa_food["nutrients"], context="food",
                                      offer_if_covered=False,
                                      base_food_name=aa_food["name"])

    from ..services.oxalate_link import maybe_show_oxalate
    maybe_show_oxalate(food["fdcId"], food["name"])

    try:
        ans = _prompt("Analyze a portion of this food?  [grey62](y/N)[/grey62]",
                      choices=["y", "n"], default="n")
    except Cancelled:
        return
    if ans != "y":
        return

    result = _pick_portion(aa_food)
    if result is None:
        return
    grams, label, scaled = result
    _print_nutrient_table(scaled, title=aa_food["name"], per_label=label,
                          daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
    has_aa = _print_protein_completeness(scaled, food_name=aa_food["name"])
    _print_bioavailability(aa_food["name"], scaled)
    if has_aa and _usda.get_aa_gaps(scaled, digestibility=_aa_diaas):
        _print_complement_suggestions(scaled, context="food", offer_if_covered=False,
                                      base_food_name=aa_food["name"])


def _do_analyze_food_portion() -> None:
    try:
        query = _prompt(
            "Search food or recipe  [grey62](name · FDC ID · barcode · Enter/b=back)[/grey62]",
            free_text=True,
        ).strip()
    except Cancelled:
        return
    if not query or query.lower() in ("b", "m", "q"):
        return

    with _db.get_db() as conn:
        all_recipes = _db.recipe_list(conn)
    query_words = query.lower().split()
    matching_recipes = sorted(
        [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)],
        key=lambda r: (-sum(1 for w in query_words if w in r["name"].lower()), r["name"].lower()),
    )
    food = _search_and_pick_food(initial_query=query, prepend_recipes=matching_recipes or None)
    if food is None:
        return

    daily_nutrients, rda = _get_daily_context()

    if food.get("_type") == "recipe":
        from .recipes import _get_recipe_total_nutrients, _pick_recipe_portion
        recipe, _, combined = _get_recipe_total_nutrients(food["id"])
        if recipe is None or not combined:
            state.console.print(f"[{state.T['warning']}]Recipe has no analyzable ingredients.[/{state.T['warning']}]")
            return
        portion = _pick_recipe_portion(recipe)
        if portion is None:
            return
        servings, label = portion
        factor = servings / (recipe["servings"] or 1)
        scaled = {k: v * factor for k, v in combined.items()}
        food_name = food["name"]
        state.console.print(
            "  [grey62]Note: for per-ingredient digestibility breakdown (TID table), use Recipes → Browse / analyze recipe.[/grey62]",
            highlight=False,
        )
        _print_nutrient_table(scaled, title=food_name, per_label=label,
                              daily_nutrients=daily_nutrients, rda=rda)
        has_aa = _print_protein_completeness(scaled)
        if has_aa and _usda.get_aa_gaps(scaled):
            _print_complement_suggestions(scaled, context="recipe", offer_if_covered=True)
        elif not has_aa and scaled.get("protein_g", 0) > 0:
            state.console.print(
                f"\n  [{state.T['warning']}]⚑  Insufficient amino acid data.[/{state.T['warning']}]",
                highlight=False,
            )
        _offer_export(food_name, [
            {"type": "nutrient_table", "title": food_name, "nutrients": scaled, "per_label": label},
            {"type": "protein_completeness", "nutrients": scaled},
        ])
        return

    result = _pick_portion(food)
    if result is None:
        return
    grams, label, scaled = result
    _print_nutrient_table(scaled, title=food["name"], per_label=label,
                          daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
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
                                      per_label=alt_label,
                                      daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
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
        state.console.print(f"  [grey62]Weight: {density:.3f} g/ml[/grey62]")
    state.console.print(f"  Enter an amount, for example: 150 (g/gr), 3 oz, 0.5 lb, 1/4 c (cup), 2 T (tbsp), 1 t (tsp)")

    prompt_text = "Amount  (b=back, m=main, q=quit)"
    while True:
        try:
            raw = _prompt(prompt_text).strip()
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
        if grams is None:
            vol_display = label
            state.console.print(f"  [grey62]Weight per volume is unknown for this food. Weigh your portion to continue.[/grey62]")
            try:
                w_raw = _prompt(f"Weight of {vol_display} in grams  (e.g. 140 g · Enter=skip, b=back)", free_text=True).strip()
            except Cancelled:
                continue
            if not w_raw or w_raw.lower() in ("b", "back"):
                continue
            if w_raw.lower() == "m":
                raise ReturnToMain()
            if w_raw.lower() == "q":
                raise SystemExit(0)
            try:
                grams = float(re.sub(r'\s*(gr?a?m?s?)\s*$', '', w_raw, flags=re.IGNORECASE).strip())
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Enter a number (e.g. 140).[/{state.T['warning']}]")
                continue
            label = vol_display
        state.console.print(f"\n  [bold]{label}[/bold]  =  [bold]{grams:.1f} g[/bold]\n")
        prompt_text = "Another amount?  (Enter/b=done, m=main, q=quit)"


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
    daily_nutrients, rda = _get_daily_context()
    _print_nutrient_table(scaled, title=title, per_label=label,
                          daily_nutrients=daily_nutrients, rda=rda)
    has_aa = _print_protein_completeness(scaled)
    if has_aa and _usda.get_aa_gaps(scaled):
        _print_complement_suggestions(scaled, context="recipe", offer_if_covered=True)
    elif not has_aa and scaled.get("protein_g", 0) > 0:
        state.console.print(
            f"\n  [{state.T['warning']}]⚑  Insufficient amino acid data to assess protein completeness.[/{state.T['warning']}]",
            highlight=False,
        )
        state.console.print(
            "  [grey62]Recipe ingredients lack USDA amino acid records. If this recipe relies "
            "mainly on plant proteins, consider pairing with a complementary source "
            "(e.g. legumes + grains, or dairy / eggs / soy) to improve amino acid balance.[/grey62]",
            highlight=False,
        )

    _offer_export(f"{title} — {label}", [
        {"type": "ingredient_list", "title": "Ingredients",
         "items": [{"food_name": i["food_name"], "amount": i["amount"], "unit": i["unit"]} for i in ingredients]},
        {"type": "nutrient_table", "title": title, "nutrients": scaled, "per_label": label},
        {"type": "protein_completeness", "nutrients": scaled},
    ])


# ---------------------------------------------------------------------------
# Food comparison
# ---------------------------------------------------------------------------

_COMPARE_GROUPS: list[tuple[str, list[str]]] = [
    ("Macronutrients", [
        "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
        "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    ]),
    ("Minerals", [
        "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
        "potassium_mg", "sodium_mg", "zinc_mg",
    ]),
    ("Vitamins", [
        "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
        "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
        "b6_mg", "folate_mcg", "b12_mcg",
    ]),
    ("Phytonutrients", [
        "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
        "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg", "isoflavones_mg",
    ]),
    ("Amino Acids", [
        "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
        "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
        "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g",
    ]),
]


def _print_food_comparison(entries: list[dict]) -> None:
    """Render side-by-side nutrient table for 2–8 foods."""
    N = len(entries)
    _NUT_W = 26

    from ..ui.common import section_title, table_footer, _id_cell
    section_title("FOOD COMPARISON", f"{N} foods · per portion selected")
    for i, e in enumerate(entries, 1):
        id_str = _id_cell(e.get("fdc_id"))
        prefix = f"{id_str}  " if id_str else ""
        state.console.print(f"  [{state.T['accent']}]{i}.[/{state.T['accent']}] {prefix}{e['label']}", highlight=False)

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Nutrient", min_width=_NUT_W, max_width=_NUT_W, no_wrap=True)
    for i, e in enumerate(entries, 1):
        name = e["name"]
        short = (name[:11] + "…") if len(name) > 12 else name
        tbl.add_column(f"{i}. {short}", justify="right", min_width=9)

    for group_name, keys in _COMPARE_GROUPS:
        if not any(e["nutrients"].get(k, 0.0) > 0 for e in entries for k in keys):
            continue
        tbl.add_row(f"[{state.T['hi']}]{group_name}[/{state.T['hi']}]", *[""] * N)
        for key in keys:
            vals = [e["nutrients"].get(key, 0.0) for e in entries]
            if not any(v > 0 for v in vals):
                continue
            lbl, unit = _usda.nutrient_label(key)
            raw_cell = f"  {lbl} ({unit})"
            nut_cell = raw_cell if len(raw_cell) <= _NUT_W else raw_cell[:_NUT_W - 1] + "…"
            max_val = max(vals)
            cells = []
            for v in vals:
                if v <= 0:
                    cells.append("[grey62]—[/grey62]")
                elif v == max_val:
                    cells.append(f"[{state.T['success']}]{v:.2f}[/{state.T['success']}]")
                else:
                    cells.append(f"{v:.2f}")
            tbl.add_row(nut_cell, *cells)

    state.console.print()
    state.console.print(tbl)
    table_footer(
        f"  [{state.T['success']}]Highlighted[/{state.T['success']}]"
        f" [grey62]= highest in row   —  = no data for this food[/grey62]"
    )
    help_footer("food-comparison")


def _do_compare_foods() -> None:
    """Collect up to 8 foods or recipe portions and display a side-by-side nutrient table."""
    MAX = 8
    entries: list[dict] = []  # {"name": str, "label": str, "nutrients": dict[str, float], "fdc_id": int | None}
    last_results: list[dict] = []  # food result dicts from the most recent search

    # Offer saved lists before starting
    with _db.get_db() as conn:
        saved = _db.saved_comparison_list(conn)
    if saved:
        state.console.print()
        state.console.print(f"  [{state.T['hi']}]Saved comparisons ({len(saved)}):[/{state.T['hi']}]")
        for i, s in enumerate(saved, 1):
            import json as _json
            n_foods = len(_json.loads(s["fdc_ids"]))
            state.console.print(f"    [{state.T['accent']}]{i}.[/{state.T['accent']}]  {s['name']}  [grey62]({n_foods} foods · {s['created_at'][:10]})[/grey62]")
        state.console.print(f"  [grey62]Type a number to load a saved list, or press Enter to start fresh.[/grey62]")
        try:
            raw_s = _prompt("  Load saved list").strip()
        except Cancelled:
            raw_s = ""
        if raw_s.isdigit():
            idx = int(raw_s) - 1
            if 0 <= idx < len(saved):
                import json as _json
                fdc_ids = _json.loads(saved[idx]["fdc_ids"])
                state.console.print(f"  [{state.T['success']}]Loaded: {saved[idx]['name']}[/{state.T['success']}]")
                for fid in fdc_ids:
                    with _db.get_db() as conn:
                        cached = _db.get_cached_food(conn, fid)
                    if not cached:
                        state.console.print(f"  [{state.T['warning']}]Food {fid} no longer in cache — skipping.[/{state.T['warning']}]")
                        continue
                    import json as _json2
                    nuts_100g = _json2.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
                    portions = _json2.loads(cached["portions_json"]) if cached["portions_json"] else []
                    food_stub = {
                        "fdcId": fid, "name": cached["name"],
                        "dataType": cached["data_type"] or "",
                        "nutrients": nuts_100g, "portions": portions,
                    }
                    result = _pick_portion(food_stub)
                    if result is None:
                        continue
                    grams, label, scaled = result
                    entries.append({"name": cached["name"], "label": f"{cached['name']} ({label})", "nutrients": scaled, "fdc_id": fid})
            else:
                state.console.print(f"  [{state.T['warning']}]No saved list #{raw_s}.[/{state.T['warning']}]")

    def _add_food_to_entries(food: dict) -> bool:
        """Prompt for portion and append to entries. Returns True if added."""
        if food.get("_type") == "recipe":
            from .recipes import _get_recipe_total_nutrients, _pick_recipe_portion
            recipe, _, combined = _get_recipe_total_nutrients(food["id"])
            if recipe is None or not combined:
                state.console.print(
                    f"  [{state.T['warning']}]Recipe has no analyzable ingredients.[/{state.T['warning']}]"
                )
                return False
            portion = _pick_recipe_portion(recipe)
            if portion is None:
                return False
            servings, label = portion
            factor = servings / (recipe["servings"] or 1)
            scaled = {k: v * factor for k, v in combined.items()}
            entries.append({"name": food["name"], "label": f"{food['name']} ({label})", "nutrients": scaled, "fdc_id": None})
        else:
            result = _pick_portion(food)
            if result is None:
                return False
            grams, label, scaled = result
            entries.append({"name": food["name"], "label": f"{food['name']} ({label})", "nutrients": scaled, "fdc_id": food.get("fdcId")})
        return True

    while len(entries) < MAX:
        n = len(entries)
        state.console.print()
        if n == 0:
            state.console.print(
                f"  [{state.T['hi']}]Food Comparison — select up to {MAX} foods[/{state.T['hi']}]"
            )
        else:
            names = "  ·  ".join(e["name"] for e in entries)
            state.console.print(f"  [grey62]Added: {names}[/grey62]")

        remaining = MAX - n
        if n >= 1 and last_results:
            _repick_hint = f"#N · #N–M · #N,M,... · mixed (#4-7,9) (1–{len(last_results)})"
            hint = f"  [grey62](re-pick from last results: {_repick_hint} · new query to search again · Enter to compare)[/grey62]"
        elif n >= 2:
            hint = "  [grey62](Enter to compare)[/grey62]"
        else:
            hint = ""
        try:
            raw = _prompt(f"  Food {n + 1} — search{hint}", free_text=True).strip()
        except Cancelled:
            if n >= 2:
                break
            return

        rl = raw.lower()
        if not raw or rl == "b":
            if n >= 2:
                break
            return
        if rl == "m":
            raise ReturnToMain()
        if rl == "q":
            raise SystemExit(0)

        # Re-pick by number(s) from the last search results (no new API call)
        if last_results and (raw.isdigit() or raw.startswith("#")):
            pick_str = raw if raw.startswith("#") else f"#{raw}"
            indices = _parse_hash_pick(pick_str, len(last_results))
            if indices is None:
                state.console.print(
                    f"  [{state.T['warning']}]Use #N, #N–M, #N,M,... or mixed — numbers 1–{len(last_results)}[/{state.T['warning']}]"
                )
                continue
            for idx in indices:
                if len(entries) >= MAX:
                    state.console.print(f"  [grey62](Comparison limit of {MAX} reached — stopping here.)[/grey62]")
                    break
                food = _fetch_food_from_result(last_results[idx])
                if food is None:
                    state.console.print(f"  [{state.T['warning']}]Could not load #{idx + 1}.[/{state.T['warning']}]")
                    continue
                _add_food_to_entries(food)
        else:
            # New search — result_out keeps the displayed list for future re-picks
            with _db.get_db() as conn:
                all_recipes = _db.recipe_list(conn)
            words = rl.split()
            matching = sorted(
                [r for r in all_recipes if any(w in r["name"].lower() for w in words)],
                key=lambda r: (-sum(1 for w in words if w in r["name"].lower()), r["name"].lower()),
            )
            foods = _search_and_pick_food(
                initial_query=raw, prepend_recipes=matching or None,
                result_out=last_results, multi_select=True,
            )
            for food in (foods or []):
                if len(entries) >= MAX:
                    state.console.print(f"  [grey62](Comparison limit of {MAX} reached — stopping here.)[/grey62]")
                    break
                _add_food_to_entries(food)

    if len(entries) < 2:
        if entries:
            state.console.print(
                f"[{state.T['warning']}]Add at least 2 foods to compare.[/{state.T['warning']}]"
            )
        return

    _print_food_comparison(entries)

    # Offer to save the list
    food_entries = [e for e in entries if e.get("fdc_id")]
    if food_entries:
        try:
            save_name = _prompt(
                "Save this food list?  [grey62](Enter a name to save · Enter/b=skip)[/grey62]",
                free_text=True,
            ).strip()
        except Cancelled:
            save_name = ""
        if save_name and save_name.lower() not in ("b", "m", "q", "n", "no"):
            import json as _json
            fdc_ids = [e["fdc_id"] for e in food_entries]
            amounts = [100.0] * len(fdc_ids)
            with _db.get_db() as conn:
                _db.saved_comparison_save(conn, save_name, fdc_ids, amounts)
            state.console.print(f"  [{state.T['success']}]✓  Saved as '{save_name}'.[/{state.T['success']}]")


# ---------------------------------------------------------------------------
# Cached food viewer / editor
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Claude nutrition-data fetch / import
# ---------------------------------------------------------------------------

_CLAUDE_PROMPT_FILE   = pathlib.Path.home() / "claude_prompt.txt"
_CLAUDE_RESPONSE_FILE = pathlib.Path.home() / "claude_response.txt"
_DOUT_FILE            = pathlib.Path.home() / "numa.data"

_CLAUDE_META_KEYS = {"name", "fdc_id", "fdc_type", "source", "confidence_note"}

_CLAUDE_VALID_KEYS: set[str] = {
    "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
    "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
    "potassium_mg", "sodium_mg", "zinc_mg",
    "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
    "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
    "b6_mg", "folate_mcg", "b12_mcg",
    "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
    "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg", "isoflavones_mg",
    "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
    "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
    "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g",
}
_CLAUDE_AA_KEYS = {k for k in _CLAUDE_VALID_KEYS if k.startswith("aa_")}
_CLAUDE_VALID_FDC_TYPES = {
    "Foundation", "SR Legacy", "Branded", "Survey (FNDDS)", "User Drafted", "OFF",
}

_CLAUDE_PROMPT_TEMPLATE = """\
I need complete nutritional data for {n} food(s), formatted as JSON for direct import into a Python nutrition app.

Output ALL foods in a SINGLE reply — one fenced ```json ... ``` block per food, all in the same response. Do not split your answer across multiple messages. Each block must follow this exact structure — metadata keys first, then all available nutrient keys:

```json
{{
  "name": "Full food name",
  "fdc_id": 123456,
  "fdc_type": "SR Legacy",
  "source": "USDA FoodData Central FDC 123456 (measured values)",
  "confidence_note": "Brief note on data quality and any estimates made",
  "calories": 0,
  "protein_g": 0
}}
```

All nutrient values are per 100 g edible portion. Use exactly these key names (omit any key whose value is genuinely unknown — never substitute 0 for unknown):

    calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g,
    saturated_fat_g, mono_fat_g, poly_fat_g,
    calcium_mg, iron_mg, magnesium_mg, phosphorus_mg,
    potassium_mg, sodium_mg, zinc_mg,
    vitamin_a_mcg, vitamin_c_mg, vitamin_d_mcg, vitamin_e_mg,
    vitamin_k_mcg, thiamin_mg, riboflavin_mg, niacin_mg,
    b6_mg, folate_mcg, b12_mcg,
    beta_carotene_mcg, alpha_carotene_mcg, lycopene_mcg,
    lutein_zeaxanthin_mcg, choline_mg, beta_sitosterol_mg, isoflavones_mg,
    aa_tryptophan_g, aa_threonine_g, aa_isoleucine_g, aa_leucine_g,
    aa_lysine_g, aa_methionine_g, aa_cystine_g, aa_phenylalanine_g,
    aa_tyrosine_g, aa_valine_g, aa_histidine_g

Critical rules:
1. Amino acid values are per 100 g FOOD, in grams (not mg, not per g protein).
2. aa_methionine_g and aa_cystine_g are always separate keys — never combined.
3. aa_phenylalanine_g and aa_tyrosine_g are always separate keys — never combined.
4. Omit any key where the value is genuinely unknown; do not estimate 0.
5. For true zeros (e.g. vitamin B12 in plant foods), include the key explicitly with value 0.
6. Source hierarchy: prefer USDA FoodData Central (cite FDC ID), then USDA SR Legacy (cite FDC ID), then peer-reviewed literature (cite paper), then estimate (flag clearly in confidence_note). Note: direct access to the USDA database is not possible — use your training data, which mirrors these sources.
7. fdc_type must be exactly one of: "Foundation", "SR Legacy", "Branded", "Survey (FNDDS)", "User Drafted".
8. If scaling from a non-100 g reference portion, show the calculation in confidence_note.

Foods ({n} total — USDA FDC IDs provided where known):
{food_list}"""


def _claude_parse_response(text: str) -> tuple[list[dict], str | None]:
    """Parse Claude's response into (food_blocks, curator_text).

    Handles fenced ```json blocks and bare JSON objects. Any non-JSON text
    (curator notes, recommendations, caveats) is returned as curator_text.
    """
    blocks: list[dict] = []
    spans: list[tuple[int, int]] = []  # character spans of JSON content to strip

    # Primary: fenced ```json ... ``` blocks
    for m in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL):
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                blocks.append(obj)
                spans.append((m.start(), m.end()))
        except json.JSONDecodeError as exc:
            preview = m.group(1)[:60].replace("\n", " ")
            state.console.print(
                f"  [{state.T['warning']}]JSON parse error in fenced block: {preview!r} ({exc})[/{state.T['warning']}]"
            )

    if not blocks:
        # Fallback: bare JSON objects — brace-match to find each top-level { }
        state.console.print("  [grey62]No fenced JSON blocks found — scanning for bare JSON objects…[/grey62]")
        i = 0
        while i < len(text):
            if text[i] != "{":
                i += 1
                continue
            depth, in_str, esc, j = 0, False, False, i
            while j < len(text):
                ch = text[j]
                if esc:
                    esc = False
                elif ch == "\\" and in_str:
                    esc = True
                elif ch == '"':
                    in_str = not in_str
                elif not in_str:
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            try:
                                obj = json.loads(text[i : j + 1])
                                if isinstance(obj, dict) and "fdc_id" in obj:
                                    blocks.append(obj)
                                    spans.append((i, j + 1))
                            except json.JSONDecodeError:
                                pass
                            break
                j += 1
            i = j + 1

    # Extract non-JSON text (curator notes) by removing JSON spans
    curator_text: str | None = None
    if spans:
        remaining = text
        for start, end in sorted(spans, reverse=True):
            remaining = remaining[:start] + remaining[end:]
        lines = [ln for ln in remaining.split("\n") if ln.strip()]
        curator_text = "\n".join(lines).strip() or None

    return blocks, curator_text


def _claude_validate_block(block: dict, idx: int) -> dict | None:
    """Validate and clean one food block. Returns cleaned dict or None on fatal error."""
    name   = block.get("name")
    fdc_id = block.get("fdc_id")

    if not name:
        state.console.print(f"  [{state.T['warning']}]Block {idx}: missing 'name' — skipped.[/{state.T['warning']}]")
        return None

    if isinstance(fdc_id, str):
        try:
            fdc_id = int(fdc_id)
        except ValueError:
            fdc_id = None
    if not isinstance(fdc_id, int):
        state.console.print(
            f"  [{state.T['warning']}]Block {idx} ({name!r}): missing/invalid 'fdc_id' — skipped.[/{state.T['warning']}]"
        )
        return None

    fdc_type = block.get("fdc_type", "User Drafted")
    if fdc_type not in _CLAUDE_VALID_FDC_TYPES:
        state.console.print(
            f"  [{state.T['warning']}]Block {idx} ({name!r}): unknown fdc_type {fdc_type!r} — using 'User Drafted'.[/{state.T['warning']}]"
        )
        fdc_type = "User Drafted"

    nutrients: dict[str, float] = {}
    stripped: list[str] = []
    for k, v in block.items():
        if k in _CLAUDE_META_KEYS:
            continue
        if k in _CLAUDE_VALID_KEYS:
            if isinstance(v, (int, float)):
                nutrients[k] = float(v)
            else:
                state.console.print(
                    f"  [{state.T['warning']}]Block {idx} ({name!r}): {k!r} is non-numeric — skipped.[/{state.T['warning']}]"
                )
        else:
            stripped.append(k)

    if stripped:
        state.console.print(
            f"  [grey62]Block {idx} ({name!r}): stripped unrecognised keys: {', '.join(stripped)}[/grey62]"
        )

    return {
        "name":            name,
        "fdc_id":          fdc_id,
        "fdc_type":        fdc_type,
        "source":          block.get("source"),
        "confidence_note": block.get("confidence_note"),
        "nutrients":       nutrients,
    }


def _claude_build_notes(food: dict) -> str | None:
    parts = []
    if food.get("source"):
        parts.append(f"Source: {food['source']}")
    if food.get("confidence_note"):
        parts.append(f"Confidence: {food['confidence_note']}")
    return "  |  ".join(parts) if parts else None


def _do_dout(id_str: str) -> None:
    """Fetch complete nutrient data for one or more FDC IDs and write to ~/numa.data.

    Checks the local food cache first; falls back to the USDA API for missing items.
    Newly fetched foods are also written to the cache.
    """
    s, e, w = state.T["success"], state.T["error"], state.T["warning"]

    parts = id_str.split()
    fdc_ids: list[int] = []
    for p in parts:
        try:
            fdc_ids.append(int(p))
        except ValueError:
            state.console.print(f"  [{w}]Skipping non-integer token: {p!r}[/{w}]")

    if not fdc_ids:
        state.console.print(f"  [{w}]No valid FDC IDs found after 'dout'.[/{w}]")
        return

    results: list[dict] = []

    for fdc_id in fdc_ids:
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)

        if cached:
            source = "cache"
            nutrients = json.loads(cached["nutrients_json"])
            portions = json.loads(cached["portions_json"]) if cached["portions_json"] else []
            entry = {
                "fdc_id":            fdc_id,
                "name":              cached["name"],
                "data_type":         cached["data_type"] or "",
                "source":            source,
                "nutrients_per_100g": nutrients,
                "portions":          portions,
            }
        else:
            try:
                food = _usda.get_food_detail(fdc_id)
                source = "USDA"
                nutrients = food["nutrients"]
                portions  = food.get("portions") or []
                entry = {
                    "fdc_id":            fdc_id,
                    "name":              food["name"],
                    "data_type":         food.get("dataType") or "",
                    "source":            source,
                    "nutrients_per_100g": nutrients,
                    "portions":          portions,
                }
                with _db.get_db() as conn:
                    _db.cache_food(
                        conn,
                        fdc_id=fdc_id,
                        name=food["name"],
                        data_type=food.get("dataType") or "",
                        brand=food.get("brand"),
                        serving_size=food.get("servingSize"),
                        serving_unit=food.get("servingUnit"),
                        nutrients=nutrients,
                        portions=portions,
                    )
            except Exception as exc:
                state.console.print(f"  [{e}]ID {fdc_id}: fetch failed — {exc}[/{e}]")
                continue

        results.append(entry)
        name_preview = entry["name"][:45]
        state.console.print(
            f"  [{s}]ID {fdc_id}[/{s}] / {name_preview} / data from {source}"
        )

    if not results:
        state.console.print(f"  [{w}]No data retrieved.[/{w}]")
        return

    _DOUT_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    state.console.print()
    state.console.print(
        f"  [{s}]✓[/{s}]  {len(results)} food(s) written to your home directory:"
    )
    state.console.print(f"      [bold]{_DOUT_FILE}[/bold]")


def _do_claude_fetch(foods: list, rest: str) -> None:
    """Generate a Claude prompt for selected or AA-incomplete foods."""
    s, e, w = state.T["success"], state.T["error"], state.T["warning"]

    if rest:
        try:
            numbers = [int(p) for p in rest.replace(",", " ").split()]
            if not numbers:
                raise ValueError
        except ValueError:
            state.console.print(f"  [{w}]Use i# or i#,# — row numbers (e.g. i3  i1,4,7) or FDC IDs (e.g. i172430,170148)[/{w}]")
            return
        # If any number exceeds the list length, treat all as FDC IDs
        fdc_id_map = {f["fdc_id"]: f["name"] for f in foods}
        if any(n > len(foods) for n in numbers):
            missing = [n for n in numbers if n not in fdc_id_map]
            if missing:
                state.console.print(f"  [{w}]FDC IDs not found in current list: {missing}[/{w}]")
                return
            selected = [(n, fdc_id_map[n]) for n in numbers]
        else:
            indices = [n - 1 for n in numbers]
            out_of_range = [i + 1 for i in indices if i < 0 or i >= len(foods)]
            if out_of_range:
                state.console.print(f"  [{w}]Out of range: {out_of_range}[/{w}]")
                return
            selected = [(foods[i]["fdc_id"], foods[i]["name"]) for i in indices]
    else:
        # No numbers: find all foods in current view missing AA data and confirm
        candidates = [
            (f["fdc_id"], f["name"]) for f in foods
            if not _usda.has_amino_acid_data(json.loads(f["nutrients_json"]))
        ]
        if not candidates:
            state.console.print(f"  [{s}]All foods in the current list already have amino acid data.[/{s}]")
            return
        state.console.print(
            f"\n  {len(candidates)} food(s) in the current list are missing amino acid data:\n"
        )
        for fdc_id, name in candidates:
            tag = str(fdc_id) if fdc_id else "no FDC ID"
            state.console.print(f"    [{tag}]  {name}")
        state.console.print()
        state.console.print(
            "  [grey62]Tip: use /filter to narrow the list first, then type i to "
            "fetch only the foods you want.[/grey62]"
        )
        try:
            ans = _prompt("  Generate prompt for all of these?", choices=["y", "n"], default="n")
        except Cancelled:
            return
        if ans != "y":
            state.console.print("  [grey62]Cancelled — use i# or iFDCID,FDCID to select specific foods.[/grey62]")
            return
        selected = candidates

    lines = "\n".join(
        f"    {fdc_id}  {name}" if fdc_id else f"    (no FDC ID)  {name}"
        for fdc_id, name in selected
    )
    prompt = _CLAUDE_PROMPT_TEMPLATE.format(n=len(selected), food_list=lines)
    _CLAUDE_PROMPT_FILE.write_text(prompt, encoding="utf-8")

    state.console.print()
    state.console.print(f"  [{s}]✓[/{s}]  Prompt written to: [bold]{_CLAUDE_PROMPT_FILE}[/bold]")
    state.console.print()
    state.console.print("  Next steps:")
    state.console.print("    [bold]1.[/bold]  Open that file and copy its entire contents.")
    state.console.print("    [bold]2.[/bold]  Go to [bold]claude.ai[/bold] — open a [bold]new chat[/bold] (not an existing one),")
    state.console.print("           paste the prompt, and send.")
    state.console.print("    [bold]3.[/bold]  When Claude finishes, copy its reply.")
    state.console.print("           [grey62]All foods should appear in one response. If Claude splits across[/grey62]")
    state.console.print("           [grey62]multiple replies, copy each one and paste them together.[/grey62]")
    state.console.print("           Paste into a text editor and save as:")
    state.console.print(f"           [bold]{_CLAUDE_RESPONSE_FILE}[/bold]")
    state.console.print("    [bold]4.[/bold]  Return here and type [bold]r[/bold] to import the data.")
    state.console.print(f"  [grey62]Type ?fetch for full instructions.[/grey62]")
    state.console.print()


def _do_claude_import() -> None:
    """Import nutritional data from a saved Claude response file."""
    s, e, w = state.T["success"], state.T["error"], state.T["warning"]

    if not _CLAUDE_RESPONSE_FILE.exists():
        state.console.print(f"  [{w}]File not found: {_CLAUDE_RESPONSE_FILE}[/{w}]")
        state.console.print("  Save Claude’s response as that file, then type [bold]r[/bold] again.")
        return

    text = _CLAUDE_RESPONSE_FILE.read_text(encoding="utf-8")
    raw_blocks, curator_text = _claude_parse_response(text)

    if not raw_blocks:
        state.console.print(f"  [{e}]No JSON blocks found in the response file.[/{e}]")
        state.console.print("  Make sure the file was saved in full and contains ```json blocks.")
        return

    state.console.print(f"\n  Found {len(raw_blocks)} JSON block(s). Validating…")
    valid: list[dict] = []
    for i, block in enumerate(raw_blocks, 1):
        result = _claude_validate_block(block, i)
        if result:
            valid.append(result)

    if curator_text:
        state.console.print(
            f"\n  [{state.T['hi']}]Curator notes found[/{state.T['hi']}]"
            f" [grey62](will be stored with each imported food — view with n#)[/grey62]"
        )

    if not valid:
        state.console.print(f"  [{e}]No valid food records after validation.[/{e}]")
        return

    # Review table
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Name",   min_width=42)
    tbl.add_column("FDC ID", justify="right", min_width=9)
    tbl.add_column("Cal",    justify="right", min_width=5)
    tbl.add_column("Prot g", justify="right", min_width=6)
    tbl.add_column("AAs",    justify="right", min_width=5)
    for f in valid:
        n = f["nutrients"]
        aa_n = sum(1 for k in _CLAUDE_AA_KEYS if k in n)
        tbl.add_row(
            f["name"][:42],
            str(f["fdc_id"]),
            str(int(n.get("calories", 0))),
            f"{n.get('protein_g', 0):.1f}",
            f"{aa_n}/11",
        )
    from ..ui.common import table_title
    table_title("FOODS TO IMPORT", f"[grey62]{len(valid)} food(s) from Claude response[/grey62]")
    state.console.print(tbl)
    help_footer("food-import")
    state.console.print()

    try:
        ans = _prompt(f"  Import {len(valid)} food(s) into cache?", choices=["y", "n"], default="n")
    except Cancelled:
        return
    if ans != "y":
        state.console.print("  [grey62]Import cancelled.[/grey62]")
        return

    with _db.get_db() as conn:
        for f in valid:
            _db.cache_food(
                conn,
                fdc_id=f["fdc_id"],
                name=f["name"],
                data_type=f["fdc_type"],
                brand=None,
                serving_size=None,
                serving_unit=None,
                nutrients=f["nutrients"],
                notes=_claude_build_notes(f),
                curator_notes=curator_text,
            )

    state.console.print(
        f"  [{s}]✓[/{s}]  Imported {len(valid)} food(s). "
        "The cache list will refresh now."
    )


def _do_annotate_food() -> None:
    """Foods menu entry: pick a cached food and open the annotation editor."""
    filter_text: str | None = None
    while True:
        with _db.get_db() as conn:
            all_foods = _db.list_cached_foods(conn)
        if not all_foods:
            state.console.print("[grey62]No foods cached yet — search for a food first.[/grey62]")
            return

        foods = (
            [f for f in all_foods
             if filter_text and (filter_text.lower() in f["name"].lower()
                                 or (f["brand"] and filter_text.lower() in f["brand"].lower()))]
            if filter_text else list(all_foods)
        )

        from rich.table import Table
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",     justify="right", min_width=3)
        tbl.add_column("Name",  min_width=40)
        tbl.add_column("Type",  min_width=14)
        for i, f in enumerate(foods, 1):
            tbl.add_row(str(i), f"[bold]{f['name']}[/bold]", f["data_type"] or "")

        from ..ui.common import table_title, table_footer
        title_note = (
            f"[grey62]{len(foods)} match · /text to filter[/grey62]"
            if filter_text else
            f"[grey62]{len(all_foods)} foods · /text to filter[/grey62]"
        )
        table_title("ANNOTATE CACHED FOOD", title_note)
        state.console.print(tbl)
        table_footer(
            "  [grey62]Type column: Foundation · SR Legacy · Survey (FNDDS) · Branded = USDA FoodData Central datasets  ·  OFF = Open Food Facts[/grey62]",
        )
        help_footer("annotate")

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
        annotate_food_interactive(row["fdc_id"], row["name"])


def _do_edit_portions(fdc_id: int, food_name: str) -> None:
    """Interactively add or remove custom portions for a cached food."""
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        state.console.print(f"[{state.T['error']}]Food not found in cache.[/{state.T['error']}]")
        return

    portions = json.loads(cached["portions_json"] or "[]") or []

    while True:
        state.console.print(f"\n  [{state.T['hi']}]Portions — {food_name}[/{state.T['hi']}]")
        if portions:
            for i, p in enumerate(portions, 1):
                state.console.print(f"    [{state.T['accent']}]{i}[/{state.T['accent']}]  {p['description']}  [grey62]{p['gram_weight']:.4g}g[/grey62]")
        else:
            state.console.print("    [grey62]No portions defined.[/grey62]")

        try:
            choice = _prompt_with_options(
                "Edit portions",
                [
                    ("c", "Add cup weight — enables cup / tbsp / tsp measures"),
                    ("p", "Add piece weight — e.g. 1 slice, 1 clove, 1 tablet"),
                    ("x", "Add custom portion"),
                    ("r", "Remove a portion  (e.g. r2)"),
                    ("d", "Done"),
                ],
                default="d",
            )
        except Cancelled:
            return
        if choice == "d":
            return

        if choice == "c":
            g = _ask_float(f"Grams per 1 cup of {food_name}")
            if g and g > 0:
                portions.append({"description": "1 cup", "gram_weight": round(g, 1)})
                with _db.get_db() as conn:
                    _db.update_food_portions(conn, fdc_id, portions)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved.")

        elif choice == "p":
            try:
                unit = _prompt(
                    "Unit name (e.g. piece, slice, clove, tablet)",
                    default="piece", free_text=True,
                ).strip() or "piece"
            except Cancelled:
                continue
            g = _ask_float(f"Grams per 1 {unit} of {food_name}")
            if g and g > 0:
                portions.append({"description": f"1 {unit}", "gram_weight": round(g, 1)})
                with _db.get_db() as conn:
                    _db.update_food_portions(conn, fdc_id, portions)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved.")

        elif choice == "x":
            try:
                desc = _prompt("Portion description (e.g. '1 tbsp', '2 oz bar')", free_text=True).strip()
            except Cancelled:
                continue
            if not desc:
                continue
            g = _ask_float(f"Grams for '{desc}'")
            if g and g > 0:
                portions.append({"description": desc, "gram_weight": round(g, 1)})
                with _db.get_db() as conn:
                    _db.update_food_portions(conn, fdc_id, portions)
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved.")

        elif choice.startswith("r"):
            idx_str = choice[1:].strip()
            if not idx_str:
                try:
                    idx_str = _prompt("Remove portion number").strip()
                except Cancelled:
                    continue
            try:
                idx = int(idx_str) - 1
                if idx < 0 or idx >= len(portions):
                    raise ValueError
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Enter a valid portion number.[/{state.T['warning']}]")
                continue
            removed = portions.pop(idx)
            with _db.get_db() as conn:
                _db.update_food_portions(conn, fdc_id, portions)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Removed: {removed['description']}.")

        else:
            state.console.print(f"[{state.T['warning']}]Unrecognized — use c, p, x, r, or b.[/{state.T['warning']}]")


_NUTRIENT_GROUPS: list[tuple[str, list[str]]] = [
    ("Macros", [
        "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
        "saturated_fat_g", "mono_fat_g", "poly_fat_g",
        "omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg",
    ]),
    ("Minerals", [
        "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
        "potassium_mg", "sodium_mg", "zinc_mg",
    ]),
    ("Vitamins", [
        "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
        "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
        "b6_mg", "folate_mcg", "b12_mcg", "choline_mg",
    ]),
    ("Phytonutrients", [
        "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
        "lutein_zeaxanthin_mcg", "beta_sitosterol_mg", "isoflavones_mg",
    ]),
    ("Amino acids", [
        "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
        "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
        "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g",
    ]),
]


def _pick_nutrients_from_usda(
    usda_nutrients: dict,
    cached_nutrients: dict,
    nutrient_label: dict[str, tuple[str, str]],
    *,
    strategy: str | None = None,
) -> dict:
    """
    Interactive nutrient selection for the USDA refresh flow.
    Returns a merged nutrient dict (cached base + selected USDA values).
    nutrient_label maps key → (label, unit).
    strategy: pre-chosen 'a'/'g'/'i'/'n'; if None, prompts the user.
    """
    if strategy is None:
        try:
            ans = _prompt(
                "  Replace nutrients?  [grey62]a=all  g=by group  i=individual  n=keep cached[/grey62]",
                choices=["a", "g", "i", "n"], default="n",
            ).strip().lower()
        except Cancelled:
            return cached_nutrients
    else:
        ans = strategy

    if ans == "a":
        return {**cached_nutrients, **usda_nutrients}
    if ans == "n":
        return cached_nutrients

    result = dict(cached_nutrients)

    def _pick_individual(keys: list[str]) -> None:
        for key in keys:
            if key not in usda_nutrients:
                continue
            usda_val = usda_nutrients[key]
            cached_val = cached_nutrients.get(key)
            label, unit = nutrient_label.get(key, (key, ""))
            cached_str = f"{cached_val:g} {unit}" if cached_val is not None else "—"
            try:
                inc = _prompt(
                    f"    {label}: cached={cached_str}  USDA={usda_val:g} {unit}  use USDA?  [grey62](Y/n)[/grey62]",
                    default="y",
                ).strip().lower()
            except Cancelled:
                return
            if inc != "n":
                result[key] = usda_val

    if ans == "g":
        for group_name, keys in _NUTRIENT_GROUPS:
            usda_in_group = [k for k in keys if k in usda_nutrients]
            if not usda_in_group:
                continue
            state.console.print(f"  [bold]{group_name}[/bold]  [grey62]({len(usda_in_group)} nutrients from USDA)[/grey62]")
            try:
                g_ans = _prompt(
                    f"    Replace {group_name}?  [grey62]a=all  i=individual  n=skip[/grey62]",
                    choices=["a", "i", "n"], default="n",
                ).strip().lower()
            except Cancelled:
                return result
            if g_ans == "a":
                for key in usda_in_group:
                    result[key] = usda_nutrients[key]
            elif g_ans == "i":
                _pick_individual(usda_in_group)
    else:  # i
        for _, keys in _NUTRIENT_GROUPS:
            _pick_individual(keys)

    return result


def _do_refresh_usda_nutrients(fdc_id: int, cached) -> None:
    """Re-fetch nutrient data from USDA for a cached food, with per-field preserve/replace choice."""
    if fdc_id < 0:
        state.console.print(
            f"[{state.T['warning']}]This is an Open Food Facts entry — USDA refresh not available.[/{state.T['warning']}]"
        )
        return
    cached_name = cached["name"]
    try:
        strategy = _prompt(
            f"Refresh [bold]{cached_name}[/bold] nutrients from USDA — how?  "
            "[grey62]a=replace all  g=by group  i=individual  n=cancel[/grey62]",
            choices=["a", "g", "i", "n"], default="n",
        ).strip().lower()
    except Cancelled:
        return
    if strategy == "n":
        return

    with state.console.status("[bold]Fetching from USDA…[/bold]", spinner="dots"):
        food = _usda.get_food_detail(fdc_id)
    if not food or not food.get("nutrients"):
        state.console.print(
            f"[{state.T['error']}]USDA returned no data for FDC {fdc_id}.[/{state.T['error']}]"
        )
        return

    existing_portions = json.loads(cached["portions_json"] or "[]") or []
    usda_portions = food.get("portions") or []

    # --- name ---
    usda_name = food.get("name") or cached_name
    if usda_name and usda_name != cached_name:
        state.console.print(
            f"  [grey62]Cached name:[/grey62]  {cached_name}\n"
            f"  [grey62]USDA name:  [/grey62]  {usda_name}"
        )
        try:
            ans = _prompt("  Use USDA name?  [grey62](y/N)[/grey62]", default="n").strip().lower()
        except Cancelled:
            return
        food_name = usda_name if ans == "y" else cached_name
    else:
        food_name = cached_name

    # --- portions ---
    if usda_portions:
        usda_desc = ", ".join(f"{p['description']} ({p['gram_weight']:g} g)" for p in usda_portions)
        if existing_portions:
            state.console.print("  [grey62]Cached portions:[/grey62]")
            for p in existing_portions:
                state.console.print(f"    {p['description']} ({p['gram_weight']:g} g)")
            state.console.print("  [grey62]USDA portions:[/grey62]")
            for i, p in enumerate(usda_portions, 1):
                state.console.print(f"    {i}. {p['description']} ({p['gram_weight']:g} g)")
            try:
                ans = _prompt(
                    "  Replace cached portions?  [grey62]a=all  i=individual  n=keep cached[/grey62]",
                    choices=["a", "i", "n"], default="n",
                ).strip().lower()
            except Cancelled:
                return
            if ans == "a":
                portions = usda_portions
            elif ans == "i":
                portions = []
                for p in usda_portions:
                    try:
                        inc = _prompt(
                            f"  Include '{p['description']}' ({p['gram_weight']:g} g)?  [grey62](Y/n)[/grey62]",
                            default="y",
                        ).strip().lower()
                    except Cancelled:
                        return
                    if inc != "n":
                        portions.append(p)
                if not portions:
                    portions = existing_portions
            else:
                portions = existing_portions
        else:
            state.console.print(f"  [grey62]USDA portions:[/grey62]  {usda_desc}")
            try:
                ans = _prompt("  Store USDA portions?  [grey62](Y/n)[/grey62]", default="y").strip().lower()
            except Cancelled:
                return
            portions = usda_portions if ans != "n" else []
    else:
        portions = existing_portions

    # --- nutrients ---
    from usda_api import NUTRIENT_MAP as _NM
    nutrient_label = {key: (label, unit) for _, (key, label, unit) in _NM.items()}
    cached_nutrients = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
    nutrients = _pick_nutrients_from_usda(food["nutrients"], cached_nutrients, nutrient_label, strategy=strategy)

    # --- notes ---
    cached_notes = cached["notes"] or ""
    if cached_notes:
        try:
            ans = _prompt("  Keep existing notes?  [grey62](Y/n)[/grey62]", default="y").strip().lower()
        except Cancelled:
            return
        notes = cached_notes if ans != "n" else ""
    else:
        notes = ""

    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id,
            name=food_name,
            nutrients=nutrients,
            data_type=food.get("dataType") or cached["data_type"],
            brand=cached["brand"],
            serving_size=food.get("servingSize") or cached["serving_size"],
            serving_unit=food.get("servingUnit") or cached["serving_unit"],
            portions=portions,
            notes=notes,
            user_drafted=False,
        )
    state.console.print(
        f"  [{state.T['success']}]✓[/{state.T['success']}]  Nutrients refreshed from USDA for [bold]{food_name}[/bold]."
    )


def _do_list_cached_foods() -> None:
    filter_text: str | None = None
    show_table = True
    _pending_refresh: tuple | None = None  # (fdc_id, cached_row) — set before redraw so table shows first
    daily_nutrients, rda = _get_daily_context()
    while True:
        with _db.get_db() as conn:
            all_foods = _db.list_cached_foods(conn)
        if not all_foods:
            state.console.print("[grey62]No foods cached yet.[/grey62]")
            return

        if filter_text:
            fl = filter_text.lower()
            foods = [f for f in all_foods if fl in f["name"].lower()
                     or (f["brand"] and fl in f["brand"].lower())]
        else:
            foods = list(all_foods)

        s, e = state.T["success"], state.T["error"]

        if show_table:
            fdc_ids = [f["fdc_id"] for f in foods]
            with _db.get_db() as conn:
                ann_map = _db.annotations_for_fdcids(conn, fdc_ids)

            _NAME_W  = 42
            _BRAND_W = 14
            tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl.add_column("#",     justify="right", min_width=3)
            tbl.add_column("AA",    min_width=3, justify="center")
            tbl.add_column("GI",    min_width=3, justify="right")
            tbl.add_column("DIAAS", min_width=5, justify="right")
            tbl.add_column("ID#",   justify="right", min_width=7)
            tbl.add_column("NAME",  min_width=_NAME_W)
            tbl.add_column("TYPE",  min_width=4)
            tbl.add_column("BRAND", min_width=_BRAND_W)
            tbl.add_column("C",     min_width=3, justify="center")
            tbl.add_column("N",     min_width=3, justify="center")
            for i, f in enumerate(foods, 1):
                nutrients = json.loads(f["nutrients_json"])
                aa_cell = (f"[{s}]✓[/{s}]" if _usda.has_amino_acid_data(nutrients)
                           else f"[{e}]✗[/{e}]")
                ann = ann_map.get(f["fdc_id"])
                gi_cell = (f"[{s}]{ann['gi_estimate']:.0f}[/{s}]"
                           if ann and ann["gi_estimate"] is not None else "—")
                diaas_cell = (f"[{s}]{ann['diaas_estimate']:.2f}[/{s}]"
                              if ann and ann["diaas_estimate"] is not None else "—")
                c_cell = f"[{s}]✓[/{s}]" if f["notes"] else "—"
                n_cell = f"[{s}]✓[/{s}]" if f["curator_notes"] else "—"
                tbl.add_row(str(i), aa_cell, gi_cell, diaas_cell,
                            _id_cell(f["fdc_id"]),
                            dot_cell(f["name"], _NAME_W, bold=True), f["data_type"] or "",
                            dot_cell(f["brand"] or "", _BRAND_W),
                            c_cell, n_cell)

            if filter_text:
                table_title("CACHED FOODS",
                            f"[grey62]{len(foods)} match for '[bold]{filter_text}[/bold]' "
                            f"({len(all_foods)} total) — enter / to clear filter[/grey62]")
            else:
                table_title("CACHED FOODS",
                            f"[grey62]{len(all_foods)} foods — enter /text to filter by name[/grey62]")

            state.console.print(tbl)
            table_footer(
                f"  [grey62]C = source/confidence note  ·  N = curator notes  ·  {ID_KEY}[/grey62]"
            )
            help_footer("food-cache")

            state.console.print()
            state.console.print(f"  [{state.T['hi']}]Options:[/{state.T['hi']}]")
            state.console.print( "    [bold]v[/bold]    View nutrients only          [grey62](e.g. v3)[/grey62]")
            state.console.print( "    [bold]n[/bold]    View nutrients + all notes   [grey62](e.g. n3 — nutrients, source, curator)[/grey62]")
            state.console.print( "    [bold]c[/bold]    Confidence/source note only  [grey62](e.g. c3)[/grey62]")
            state.console.print( "    [bold]a[/bold]    Analyze portion              [grey62](e.g. a3)[/grey62]")
            state.console.print( "    [bold]e[/bold]    Edit food data               [grey62](e.g. e3)[/grey62]")
            state.console.print( "    [bold]f[/bold]    Refresh nutrients from USDA  [grey62](e.g. f3 — re-fetch nutrients, keeps your portions/notes)[/grey62]")
            state.console.print( "    [bold]p[/bold]    Edit portions                [grey62](e.g. p3 — add cup/piece/custom weights)[/grey62]")
            state.console.print( "    [bold]d[/bold]    Delete from cache            [grey62](e.g. d3  d1,4,7)[/grey62]", highlight=False)
            state.console.print( "    [bold]i[/bold]    Fetch data from Claude       [grey62](i alone = list foods missing AA data · i3  i1,4,7  iFDCID,FDCID · ?fetch)[/grey62]", highlight=False)
            state.console.print( "    [bold]r[/bold]    Read Claude response         [grey62](import ~/claude_response.txt)[/grey62]")
            state.console.print( "    [bold]l[/bold]    List  [grey62](re-display this table)[/grey62]")
            state.console.print( "    / to filter  ·  Enter=re-list  ·  b=back  m=main  q=quit", highlight=False)
            show_table = False
            if _pending_refresh:
                fdc_id_pend, cached_pend = _pending_refresh
                _pending_refresh = None
                _do_refresh_usda_nutrients(fdc_id_pend, cached_pend)
                show_table = True
                continue
        else:
            if filter_text:
                state.console.print(
                    f"\n  [grey62]Cache — {len(foods)} of {len(all_foods)} foods"
                    f" · filter: '{filter_text}'"
                    f" · v# c# n# a# e# f# p# d# i# r · l=list · /filter · b=back[/grey62]"
                )
            else:
                state.console.print(
                    f"\n  [grey62]Cache — {len(all_foods)} foods"
                    f" · v# c# n# a# e# f# p# d# i# r · l=list · /filter · b=back[/grey62]"
                )

        try:
            raw = _prompt("  Command", free_text=True).strip()
        except Cancelled:
            return

        raw_lower = raw.lower()
        if raw_lower == "b":
            return
        if not raw:
            show_table = True
            continue
        if raw_lower == "m":
            raise ReturnToMain()
        if raw_lower == "q":
            raise SystemExit(0)
        if raw_lower == "l":
            show_table = True
            continue
        if raw.startswith("/"):
            filter_text = raw[1:].strip() or None
            show_table = True
            continue

        cmd  = raw_lower[0] if raw_lower else ""
        rest = raw[1:].strip()

        if cmd == "d" and rest:
            nums = rest.replace(",", " ")
            try:
                indices = [int(p) - 1 for p in nums.split()]
                if not indices:
                    raise ValueError
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Use d# or d#,# (e.g. d3  d1,4,7).[/{state.T['warning']}]")
                continue
            out_of_range = [i + 1 for i in indices if i < 0 or i >= len(foods)]
            if out_of_range:
                state.console.print(f"[{state.T['warning']}]Out of range: {out_of_range}[/{state.T['warning']}]")
                continue
            to_delete = [foods[i] for i in indices]
            if len(to_delete) == 1:
                confirm_msg = (f"Delete [bold]{to_delete[0]['name']}[/bold] from cache?  "
                               f"[grey62]Recipes using it will need to re-fetch.  (y/N)[/grey62]")
            else:
                preview = "\n".join(f"  · {f['name']}" for f in to_delete[:5])
                if len(to_delete) > 5:
                    preview += f"\n  · … and {len(to_delete) - 5} more"
                confirm_msg = (f"Delete {len(to_delete)} foods from cache?  [grey62](y/N)[/grey62]\n"
                               + preview)
            try:
                confirm = _prompt(confirm_msg, default="n").strip().lower()
            except Cancelled:
                continue
            if confirm == "y":
                with _db.get_db() as conn:
                    n_deleted = sum(1 for f in to_delete if _db.delete_cached_food(conn, f["fdc_id"]))
                if n_deleted == len(to_delete):
                    state.console.print(
                        f"  [{state.T['success']}]✓[/{state.T['success']}]  "
                        f"Deleted {n_deleted} food{'s' if n_deleted != 1 else ''} from cache."
                    )
                else:
                    state.console.print(
                        f"  [{state.T['warning']}]Deleted {n_deleted} of {len(to_delete)} "
                        f"(some may have already been removed).[/{state.T['warning']}]"
                    )
                show_table = True
            continue

        if cmd == "i":
            _do_claude_fetch(foods, rest)
            continue

        if cmd == "r":
            _do_claude_import()
            show_table = True
            continue

        if cmd == "f" and rest:
            try:
                idx = int(rest) - 1
                if idx < 0 or idx >= len(foods):
                    raise ValueError
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Enter a list number after f (e.g. f3).[/{state.T['warning']}]")
                continue
            row = foods[idx]
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, row["fdc_id"])
            if cached:
                _pending_refresh = (row["fdc_id"], cached)
                show_table = True
            continue

        if cmd == "p" and rest:
            try:
                idx = int(rest) - 1
                if idx < 0 or idx >= len(foods):
                    raise ValueError
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Enter a list number after p (e.g. p3).[/{state.T['warning']}]")
                continue
            row = foods[idx]
            _do_edit_portions(row["fdc_id"], row["name"])
            continue

        if cmd in ("v", "c", "a", "e", "n") and rest:
            try:
                idx = int(rest) - 1
                if idx < 0 or idx >= len(foods):
                    raise ValueError
            except ValueError:
                state.console.print(f"[{state.T['warning']}]Enter a list number after the command (e.g. v3, a5).[/{state.T['warning']}]")
                continue
            row = foods[idx]
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, row["fdc_id"])
            if not cached:
                state.console.print(f"[{state.T['error']}]Food not found in cache.[/{state.T['error']}]")
                continue

            if cmd == "c":
                if cached["notes"]:
                    state.console.print()
                    state.console.print(
                        f"  [{state.T['hi']}]Confidence / source note — {cached['name']}:[/{state.T['hi']}]"
                    )
                    state.console.print(f"  {cached['notes']}")
                    state.console.print()
                else:
                    state.console.print("  [grey62]No confidence note for this food.[/grey62]")
                show_table = True
                continue

            if cmd == "n":
                nutrients = json.loads(cached["nutrients_json"])
                _print_nutrient_table(nutrients, title=cached["name"], per_label="per 100g",
                                      daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
                _print_protein_completeness(nutrients, food_name=cached["name"])
                state.console.print()
                if cached["notes"]:
                    state.console.print(
                        f"  [{state.T['hi']}]Source / confidence note:[/{state.T['hi']}]"
                    )
                    state.console.print(f"  {cached['notes']}")
                    state.console.print()
                else:
                    state.console.print("  [grey62]No source/confidence note for this food.[/grey62]")
                cn = cached["curator_notes"] if "curator_notes" in cached.keys() else None
                if cn:
                    state.console.print(
                        f"  [{state.T['hi']}]Curator notes:[/{state.T['hi']}]"
                    )
                    state.console.print()
                    for line in cn.splitlines():
                        state.console.print(f"  {line}")
                    state.console.print()
                else:
                    state.console.print("  [grey62]No curator notes for this food.[/grey62]")
                show_table = True
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
                "portions":         json.loads(cached["portions_json"]) if cached["portions_json"] and cached["portions_json"] != "null" else [],
            }

            if cmd == "v":
                _print_nutrient_table(food["nutrients"], title=food["name"], per_label="per 100g",
                                      daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
                _print_protein_completeness(food["nutrients"], food_name=food["name"])
                show_table = True
            elif cmd == "a":
                result = _pick_portion(food)
                if result is None:
                    continue
                grams, label, scaled = result
                _print_nutrient_table(scaled, title=food["name"], per_label=label,
                                      daily_nutrients=daily_nutrients, rda=rda, show_meal_pct=False)
                _print_protein_completeness(scaled, food_name=food["name"])
                show_table = True
            elif cmd == "e":
                _do_edit_cached_food(row["fdc_id"], cached)
                try:
                    annotate_food_interactive(row["fdc_id"], cached["name"])
                except Cancelled:
                    pass
                show_table = True
            continue

        state.console.print(f"[{state.T['warning']}]Unrecognized command. Use v#, c#, n#, a#, e#, f#, p#, d#, i#, r, or l — or / to filter.[/{state.T['warning']}]")


