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
from ..services.search import _search_and_pick_food, _suggest_foundation_search, _fetch_food_from_result
from ..ui.common import _id_cell, ID_KEY, _safe_call, _show_menu, _prompt_with_options, dot_cell, table_title, table_footer, help_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_bioavailability, _print_complement_suggestions, _print_nutrient_table, _print_protein_completeness
from ..services.annotations import annotate_food_interactive
from ..services.reports import _offer_export
from .pantry import _do_pantry_menu
from .recipes import _do_recipe_list, _get_recipe_total_nutrients, _pick_recipe_portion
from .drafted_foods import _do_edit_cached_food, _do_drafted_foods_menu

def _menu_foods() -> bool:
    """Foods submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Foods — Search, Analyze & Manage", [
            ("1", "Search food databases  (USDA + Open Food Facts)"),
            ("2", "Analyze a food portion"),
            ("3", "Analyze a saved recipe portion"),
            ("4", "Convert a portion <==> weight  (volume/weight, no analysis)"),
            ("5", "Compare foods  (side-by-side nutrient table, up to 4)"),
            ("6", "Food Cache  (view, edit, delete foods you have looked up)"),
            ("7", "My pantry  (foods you have on hand)"),
            ("8", "Custom food profiles  (create and edit your own food data)"),
            ("9", "Annotate a food  (add your GI / DIAAS estimates)"),
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
        query = _prompt("Search food or recipe  [dim](name or FDC ID · b=back)[/dim]", free_text=True).strip()
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
    _print_bioavailability(food["name"], food["nutrients"])
    aa_food = food  # tracks whichever food has AA data for all subsequent steps
    if not has_aa:
        alt = _suggest_foundation_search(food)
        if alt:
            _print_nutrient_table(alt["nutrients"], title=alt["name"], per_label="per 100g")
            has_aa = _print_protein_completeness(alt["nutrients"], food_name=alt["name"])
            _print_bioavailability(alt["name"], alt["nutrients"])
            aa_food = alt
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
    state.console.print(f"  Enter an amount, for example: 150 (g/gr), 3 oz, 0.5 lb, 1/4 c (cup), 2 T (tbsp), 1 t (tsp)")

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
    """Render side-by-side nutrient table for 2–4 foods."""
    N = len(entries)
    _NUT_W = 26

    from ..ui.common import section_title, table_footer
    section_title("FOOD COMPARISON", f"{N} foods · per portion selected")
    for i, e in enumerate(entries, 1):
        state.console.print(f"  [{state.T['accent']}]{i}.[/{state.T['accent']}] {e['label']}", highlight=False)

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
                    cells.append("[dim]—[/dim]")
                elif v == max_val:
                    cells.append(f"[{state.T['success']}]{v:.2f}[/{state.T['success']}]")
                else:
                    cells.append(f"{v:.2f}")
            tbl.add_row(nut_cell, *cells)

    state.console.print()
    state.console.print(tbl)
    table_footer(
        f"  [{state.T['success']}]Highlighted[/{state.T['success']}]"
        f" [dim]= highest in row   —  = no data for this food[/dim]"
    )


def _do_compare_foods() -> None:
    """Collect up to 4 foods or recipe portions and display a side-by-side nutrient table."""
    MAX = 4
    entries: list[dict] = []  # {"name": str, "label": str, "nutrients": dict[str, float]}
    last_results: list[dict] = []  # food result dicts from the most recent search

    while len(entries) < MAX:
        n = len(entries)
        state.console.print()
        if n == 0:
            state.console.print(
                f"  [{state.T['hi']}]Food Comparison — select up to {MAX} foods[/{state.T['hi']}]"
            )
        else:
            names = "  ·  ".join(e["name"] for e in entries)
            state.console.print(f"  [dim]Added: {names}[/dim]")

        if n >= 1 and last_results:
            hint = "  [dim](# to re-pick from last results · new query to search again · Enter to compare)[/dim]"
        elif n >= 2:
            hint = "  [dim](Enter to compare)[/dim]"
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

        # Re-pick by number from the last search results (no new API call)
        if last_results and raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(last_results):
                food: dict | None = _fetch_food_from_result(last_results[idx])
                if food is None:
                    state.console.print(f"[{state.T['warning']}]Could not load that food.[/{state.T['warning']}]")
                    continue
            else:
                state.console.print(
                    f"[{state.T['warning']}]Number out of range — "
                    f"last search had {len(last_results)} results.[/{state.T['warning']}]"
                )
                continue
        else:
            # New search — result_out keeps the displayed list for future re-picks
            with _db.get_db() as conn:
                all_recipes = _db.recipe_list(conn)
            words = rl.split()
            matching = sorted(
                [r for r in all_recipes if any(w in r["name"].lower() for w in words)],
                key=lambda r: (-sum(1 for w in words if w in r["name"].lower()), r["name"].lower()),
            )
            food = _search_and_pick_food(
                initial_query=raw, prepend_recipes=matching or None, result_out=last_results
            )
            if food is None:
                continue

        if food.get("_type") == "recipe":
            from .recipes import _get_recipe_total_nutrients, _pick_recipe_portion
            recipe, _, combined = _get_recipe_total_nutrients(food["id"])
            if recipe is None or not combined:
                state.console.print(
                    f"[{state.T['warning']}]Recipe has no analyzable ingredients.[/{state.T['warning']}]"
                )
                continue
            portion = _pick_recipe_portion(recipe)
            if portion is None:
                continue
            servings, label = portion
            factor = servings / (recipe["servings"] or 1)
            scaled = {k: v * factor for k, v in combined.items()}
            entries.append({"name": food["name"], "label": f"{food['name']} ({label})", "nutrients": scaled})
        else:
            result = _pick_portion(food)
            if result is None:
                continue
            grams, label, scaled = result
            entries.append({"name": food["name"], "label": f"{food['name']} ({label})", "nutrients": scaled})

    if len(entries) < 2:
        if entries:
            state.console.print(
                f"[{state.T['warning']}]Add at least 2 foods to compare.[/{state.T['warning']}]"
            )
        return

    _print_food_comparison(entries)


# ---------------------------------------------------------------------------
# Cached food viewer / editor
# ---------------------------------------------------------------------------

def _do_annotate_food() -> None:
    """Foods menu entry: pick a cached food and open the annotation editor."""
    filter_text: str | None = None
    while True:
        with _db.get_db() as conn:
            all_foods = _db.list_cached_foods(conn)
        if not all_foods:
            state.console.print("[dim]No foods cached yet — search for a food first.[/dim]")
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
            tbl.add_row(str(i), f["name"], f["data_type"] or "")

        from ..ui.common import table_title, table_footer
        title_note = (
            f"[dim]{len(foods)} match · /text to filter[/dim]"
            if filter_text else
            f"[dim]{len(all_foods)} foods · /text to filter[/dim]"
        )
        table_title("ANNOTATE CACHED FOOD", title_note)
        state.console.print(tbl)
        table_footer(
            "  [dim]Type column: Foundation · SR Legacy · Survey (FNDDS) · Branded = USDA FoodData Central datasets  ·  OFF = Open Food Facts[/dim]",
        )

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

        fdc_ids = [f["fdc_id"] for f in foods]
        with _db.get_db() as conn:
            ann_map = _db.annotations_for_fdcids(conn, fdc_ids)

        s, e = state.T["success"], state.T["error"]

        _NAME_W  = 55
        _BRAND_W = 20
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
        tbl.add_column("#",      justify="right", min_width=3)
        tbl.add_column("AA",     min_width=3, justify="center")
        tbl.add_column("GI",     min_width=4, justify="right")
        tbl.add_column("DIAAS",  min_width=5, justify="right")
        tbl.add_column("CONF.",  min_width=5, justify="center")
        tbl.add_column("ID#",    justify="right", min_width=7)
        tbl.add_column("Name",   min_width=_NAME_W)
        tbl.add_column("Type",   min_width=14)
        tbl.add_column("Brand",  min_width=_BRAND_W)
        for i, f in enumerate(foods, 1):
            nutrients = json.loads(f["nutrients_json"])
            aa_cell = (f"[{s}]✓[/{s}]" if _usda.has_amino_acid_data(nutrients)
                       else f"[{e}]✗[/{e}]")
            ann = ann_map.get(f["fdc_id"])
            gi_cell = (f"[{s}]{ann['gi_estimate']:.0f}[/{s}]"
                       if ann and ann["gi_estimate"] is not None else "[dim]——[/dim]")
            diaas_cell = (f"[{s}]{ann['diaas_estimate']:.2f}[/{s}]"
                          if ann and ann["diaas_estimate"] is not None else "[dim]——[/dim]")
            conf_cell = "y" if f["notes"] else ""
            tbl.add_row(str(i), aa_cell, gi_cell, diaas_cell, conf_cell,
                        _id_cell(f["fdc_id"]),
                        dot_cell(f["name"], _NAME_W), f["data_type"] or "",
                        dot_cell(f["brand"], _BRAND_W) if f["brand"] else "")

        if filter_text:
            table_title("CACHED FOODS",
                        f"[dim]{len(foods)} match for '[bold]{filter_text}[/bold]' "
                        f"({len(all_foods)} total) — enter / to clear filter[/dim]")
        else:
            table_title("CACHED FOODS",
                        f"[dim]{len(all_foods)} foods — enter /text to filter by name[/dim]")

        state.console.print(tbl)
        help_footer("cached")

        try:
            raw = _prompt("(Enter # to see options, d#[,#…] to delete, /[food name] to filter, b=back, m=main, q=quit)").strip()
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

        # Delete command: d1  d1,3  d1 3 5  (space or comma separators)
        if raw_lower.startswith("d") and len(raw_lower) > 1:
            rest = raw_lower[1:].replace(",", " ")
            try:
                indices = [int(p) - 1 for p in rest.split()]
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
                               f"[dim]Recipes using it will need to re-fetch.  (y/N)[/dim]")
            else:
                preview = "\n".join(f"  · {f['name']}" for f in to_delete[:5])
                if len(to_delete) > 5:
                    preview += f"\n  · … and {len(to_delete) - 5} more"
                confirm_msg = (f"Delete {len(to_delete)} foods from cache?  [dim](y/N)[/dim]\n"
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

        has_note = bool(cached["notes"])
        options = [
            ("1", "View nutrients"),
            ("2", "Analyze portion"),
            ("3", "Edit nutrients"),
            ("4", "Annotate  (GI / DIAAS estimates)"),
        ]
        if has_note:
            options.append(("5", "View confidence note"))
        options.append(("d", "Delete from cache"))

        try:
            action = _prompt_with_options("Cached food action", options, default="1")
        except Cancelled:
            continue

        if action == "5" and has_note:
            state.console.print()
            state.console.print(
                f"[{state.T['hi']}]Confidence / source note for {cached['name']}:[/{state.T['hi']}]"
            )
            state.console.print(cached["notes"])
            state.console.print()
            continue
        elif action == "4":
            annotate_food_interactive(row["fdc_id"], cached["name"])
            continue
        elif action == "3":
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


