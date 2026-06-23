"""
meals.py — Meals & Log menu: log, view/edit, analyze, merge, and delete meals.
Docs: README-numa-documentation.md, Menu Structure: "3. Meals & Log"
"""
import json
import re
from datetime import date, datetime

import diaas as _diaas

from rich.table import Table

import db as _db
import profile as _profile
import usda as _usda
from .. import state
from ..services.portions import _normalize_unit_display, _pick_portion
from ..services.search import _refresh_cache_if_missing_aa, _search_and_pick_food, _simplify_food_query
from ..services.reports import _offer_export
from ..ui.common import _prompt_with_options, _safe_call, _show_menu, dot_cell, table_title, section_title, help_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_date, _ask_int, _prompt
from ..ui.render import _print_complement_suggestions, _print_meal_diaas, _print_nutrient_table, _print_protein_adequacy
from .recipes import _do_recipe_list, _format_recipe_portion_label, _parse_serving_amount

def _fix_meal_aa_profiles(meal_id: int, missing_names: list[str], protein_by_name: dict[str, float] | None = None) -> bool:
    """
    For each meal food item lacking AA data, offer a search-and-replace flow.
    The search results show Type (SR Legacy / Foundation / Branded) so the user
    can pick an entry that is likely to have AA profile data.
    Returns True if any items were replaced.
    """
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)

    pbn = protein_by_name or {}
    missing_lower = {n.lower() for n in missing_names}
    all_affected = [it for it in items
                    if it["item_type"] == "food" and it["food_name"].lower() in missing_lower]
    affected = [it for it in all_affected if pbn.get(it["food_name"], 0.0) >= 0.1] if pbn else all_affected
    if not affected:
        return False

    section_title("Missing Amino Acid Profiles")

    # Identify which recipes contain the missing ingredients (with protein only)
    recipe_missing_lower = missing_lower - {a["food_name"].lower() for a in all_affected}
    recipe_aa_gaps: dict[str, list[str]] = {}
    if recipe_missing_lower:
        for rit in (it for it in items if it["item_type"] == "recipe"):
            with _db.get_db() as conn:
                recipe = _db.recipe_get(conn, rit["recipe_id"])
                ings   = _db.recipe_get_ingredients(conn, rit["recipe_id"])
            if not recipe or not ings:
                continue
            missing_in = [ing["food_name"] for ing in ings
                          if ing["food_name"].lower() in recipe_missing_lower
                          and (not pbn or pbn.get(ing["food_name"], 0.0) >= 0.1)]
            if missing_in:
                recipe_aa_gaps[recipe["name"]] = missing_in

    recipe_missing = sum(len(v) for v in recipe_aa_gaps.values())
    if recipe_missing > 0:
        n_recipes = len(recipe_aa_gaps)
        recipe_word = "recipe" if n_recipes == 1 else "recipes"
        detail_lines = "\n".join(
            f"    · [{state.T['hi']}]{rname}[/{state.T['hi']}]  —  " + ", ".join(ing_names)
            for rname, ing_names in recipe_aa_gaps.items()
        )
        state.console.print(
            f"  [{state.T['warning']}]⚠  {recipe_missing} ingredient(s) inside "
            f"{n_recipes} {recipe_word} have no AA profile — edit those {recipe_word} to fix:[/{state.T['warning']}]\n"
            + detail_lines,
            highlight=False,
        )
    standalone_names = "\n".join(f"    · {it['food_name']}" for it in affected)
    state.console.print(
        f"  [grey62]Standalone meal ingredients missing AA data:[/grey62]\n"
        + standalone_names,
        highlight=False,
    )
    help_footer("missing-aa")
    try:
        go = _prompt(
            f"Fetch missing AA profiles for these {len(affected)} ingredient(s)?",
            choices=["y", "n", "b"], default="n",
        )
    except Cancelled:
        raise
    if go == "b":
        raise Cancelled
    if go != "y":
        return False

    state.console.print(
        f"\n  [grey62]For each ingredient, you can search for a replacement with AA data.\n"
        f"  In the search results, [bold]SR Legacy[/bold] or [bold]Foundation[/bold] entries"
        f" typically include full amino acid profiles — check the AA column.\n"
        f"  Press Enter to skip an ingredient.[/grey62]"
    )

    replaced_any = False
    for item in affected:
        state.console.print(f"\n  [grey62]Next food missing AA data:[/grey62]"
                      f"  [{state.T['accent']}]{item['food_name']}[/{state.T['accent']}]"
                      f"  [grey62]({_normalize_unit_display(item['unit'])})[/grey62]")
        suggested = _simplify_food_query(item["food_name"].split(",")[0].strip())
        state.console.print(f"  [grey62]Searching SR Legacy + Foundation for: '{suggested}'[/grey62]")
        food = _search_and_pick_food(
            data_types=["Foundation", "SR Legacy"],
            initial_query=suggested,
            show_aa_status=True,
            allow_research=False,
        )
        if food is None:
            state.console.print("  [grey62]Skipped.[/grey62]")
            continue

        has_aa = _usda.has_amino_acid_data(food["nutrients"])
        if not has_aa:
            state.console.print(
                f"  [{state.T['warning']}]⚠  This food also has no AA profile "
                f"(Type: {food.get('dataType', '?')}). Replace anyway?[/{state.T['warning']}]"
            )
            try:
                confirm = _prompt("Replace anyway?  [grey62](n = skip to next food)[/grey62]", choices=["y", "n"], default="n")
            except Cancelled:
                confirm = "n"
            if confirm != "y":
                continue

        grams, label = None, None
        if item["amount"] and item["amount"] > 0 and item["unit"] and item["unit"] != "—":
            state.console.print(f"  [grey62]Original amount: [bold]{_normalize_unit_display(item['unit'])}[/bold]"
                          f"  ({item['amount']:.0f} g)[/grey62]")
            try:
                keep = _prompt("Keep this amount for the replacement?  [grey62](Y/n)[/grey62]",
                               choices=["y", "n"], default="y")
            except Cancelled:
                keep = "y"
            if keep != "n":
                grams = item["amount"]
                label = item["unit"]
        if grams is None:
            result = _pick_portion(food)
            if result is None:
                state.console.print("  [grey62]Skipped.[/grey62]")
                continue
            grams, label, _ = result

        with _db.get_db() as conn:
            _db.meal_remove_item(conn, item["id"], meal_id)
            _db.meal_add_food(conn, meal_id, food["fdcId"], food["name"], grams, label, item["notes"] or None)

        aa_tag = (f"[{state.T['success']}]✓ has AA data[/{state.T['success']}]" if has_aa
                  else f"[{state.T['warning']}]⚠ no AA data[/{state.T['warning']}]")
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Replaced with: {food['name']}  {label}  {aa_tag}")
        replaced_any = True

    if replaced_any:
        state.console.print(
            f"\n  [{state.T['success']}]✓[/{state.T['success']}]  [grey62]Ingredients updated."
            f" Re-analyze this meal to see the updated DIAAS results.[/grey62]"
        )
    return replaced_any

def _is_date_str(s: str) -> bool:
    """Return True if s matches YYYY-MM-DD."""
    return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', s))


def _resolve_meal(raw_id: str):
    """Parse integer meal ID from raw_id; return DB row or None."""
    try:
        mid = int(raw_id)
    except ValueError:
        return None
    with _db.get_db() as conn:
        return _db.meal_get(conn, mid)


_MEALS_PAGE = 15


def _compute_meal_bcp(meal_id: int) -> float | None:
    """Return digestible complete protein (g) for a meal, or None if unavailable."""
    ing_list = _compute_meal_ingredient_list(meal_id)
    if not ing_list:
        return None
    with _db.get_db() as conn:
        result = _diaas.meal_level_diaas(ing_list, conn)
    return result.get("digestible_complete_protein_g")


def _print_meal_protein_summary(meal_id: int) -> None:
    """Print a one-line raw protein / DCP summary for use during meal editing."""
    nutrients = _compute_meal_nutrients(meal_id)
    if nutrients is None:
        return
    raw_prot = nutrients.get("protein_g", 0.0)
    dcp = _compute_meal_bcp(meal_id)
    dcp_str = f"{dcp:.1f} g" if dcp is not None else "[grey62]— (AA data missing)[/grey62]"
    state.console.print(
        f"  [grey62]Protein:[/grey62]  raw {raw_prot:.1f} g  "
        f"[grey62]·[/grey62]  complete (DCP) {dcp_str}"
    )


def _menu_meals() -> bool:
    """Meals & Log inline list. Returns True to go back, False to quit."""
    offset = 0
    before_date: str | None = None

    while True:
        with _db.get_db() as conn:
            meals = _db.meal_list_recent(
                conn, limit=_MEALS_PAGE + 1, offset=offset, before_date=before_date
            )
            total_count = _db.meal_count_recent(conn, before_date=before_date)
        has_more = len(meals) > _MEALS_PAGE
        page = meals[:_MEALS_PAGE]

        # Compute day BCP totals from whatever is stored in DB for each date in view.
        dates_in_page = {m["meal_date"] for m in page}
        day_bcp: dict[str, float | None] = {}
        for _d in dates_in_page:
            with _db.get_db() as conn:
                date_rows = _db.meal_list_by_date(conn, _d)
            day_vals = [
                r["bcp_g"] for r in date_rows
                if r["complete"] and r["bcp_g"] is not None
            ]
            day_bcp[_d] = sum(day_vals) if day_vals else None

        # Load profile protein target once per render — used in title and p handler.
        _profile_obj = _profile.load_profile()
        protein_target: float | None = None
        if _profile_obj:
            _t = _profile.compute_rda(_profile_obj).get("protein_g", (0.0,))[0]
            protein_target = _t if _t > 0 else None

        title = "Meals & Log"
        if before_date:
            title += f"  [grey62]— from {before_date}[/grey62]"
        if protein_target:
            title += f"  [grey62]— daily BCP goal = {protein_target:.0f} grams[/grey62]"
        section_title(title)

        _W_NAME = 24
        if page:
            tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
            tbl.add_column("ID",       justify="right",  min_width=4)
            tbl.add_column("Date",     min_width=10)
            tbl.add_column("Complete", justify="center", min_width=8)
            tbl.add_column("Meal",     min_width=_W_NAME, max_width=_W_NAME, no_wrap=True)
            tbl.add_column("Items",    justify="right",  min_width=5)
            tbl.add_column("Meal BCP",     justify="right",  min_width=8)
            tbl.add_column("Day BCP",      justify="right",  min_width=7)
            tbl.add_column("% profile goal", justify="left",  min_width=13)
            s = state.T["success"]
            dates_seen: set[str] = set()
            for m in page:
                done_cell = (f"[{s}]✓[/{s}]" if m["complete"] else "[grey62]·[/grey62]")
                bcp_g = m["bcp_g"]
                if bcp_g is not None:
                    meal_bcp_cell = f"[{s}]{bcp_g:.1f} g[/{s}]"
                elif m["bcp_computed_at"] is not None:
                    meal_bcp_cell = "[grey62]n/a[/grey62]"
                else:
                    meal_bcp_cell = "[grey62]—[/grey62]"
                d = m["meal_date"]
                if d not in dates_seen:
                    dv = day_bcp.get(d)
                    day_bcp_cell = (f"[{s}]{dv:.1f} g[/{s}]" if dv is not None
                                    else "[grey62]—[/grey62]")
                    pct = m["day_pct_goal"]
                    # Leading plain-text spaces position the value so its right edge
                    # falls under the 'e' in "profile" (col header = 14 chars; field = 9).
                    if pct is None:
                        goal_cell = " " * 8 + "[grey62]—[/grey62]"
                    else:
                        pct_color = (s if pct >= 100 else
                                     state.T["warning"] if pct >= 70 else
                                     state.T["error"])
                        val_str = f"{pct:.0f}%"
                        goal_cell = " " * (9 - len(val_str)) + f"[{pct_color}]{val_str}[/{pct_color}]"
                    dates_seen.add(d)
                else:
                    day_bcp_cell = ""
                    goal_cell = ""
                tbl.add_row(
                    str(m["id"]),
                    m["meal_date"],
                    done_cell,
                    dot_cell(m["name"], _W_NAME),
                    str(m["item_count"]),
                    meal_bcp_cell,
                    day_bcp_cell,
                    goal_cell,
                )
            state.console.print(tbl)
            state.console.print(
                "  [grey62]BCP = bioavailable (digestible) complete protein"
                "  ·  values are saved; press p to (re)compute[/grey62]",
                highlight=False,
            )
            help_footer("meals-list")
        elif offset == 0 and before_date is None:
            state.console.print("  [grey62]No meals logged yet.[/grey62]")
        else:
            state.console.print(
                "  [grey62]No" + (" more" if offset > 0 else "")
                + " meals" + (f" before {before_date}" if before_date else "") + ".[/grey62]"
            )

        if page:
            more_count = total_count - offset - len(page)
            state.console.print(
                f"  [grey62]({len(page)} shown — {more_count} more to show)[/grey62]",
                highlight=False,
            )
        state.console.print()
        state.console.print(f"  [{state.T['accent']}]Commands:[/{state.T['accent']}]", highlight=False)
        state.console.print("  [grey62]  n ············  New meal (prompts for date and name)[/grey62]", highlight=False)
        if page:
            state.console.print("  [grey62]  v{id} / e{id}  View or edit a meal  (e.g. v3 or e3)[/grey62]", highlight=False)
            state.console.print("  [grey62]  a{id} ········  Analyze a meal or the full day  (e.g. a3)[/grey62]", highlight=False)
            state.console.print("  [grey62]  d{id} ········  Delete meal(s)  (e.g. d3  or  d3 5 7  or  d3-7)[/grey62]", highlight=False)
        state.console.print("  [grey62]  s ············  Search all meals for a food  (e.g. s, then food name at prompt)[/grey62]", highlight=False)
        if page and any(m["complete"] for m in page):
            state.console.print("  [grey62]  p ············  Compute BCP for all complete meals shown[/grey62]", highlight=False)
        if has_more:
            state.console.print("  [grey62]  mr ···········  Show next 15 older meals[/grey62]", highlight=False)
        state.console.print("  [grey62]  d{YYYY-MM-DD}   Jump to meals on or before a date  (e.g. d2025-03-15)[/grey62]", highlight=False)
        state.console.print("  [grey62]  b / m / q ····  Back · Main menu · Quit[/grey62]", highlight=False)

        try:
            raw = _prompt("Command").strip()
        except Cancelled:
            state.console.print("[grey62]Cancelled.[/grey62]")
            return True

        rl = raw.lower()
        if rl in ("b", ""):
            return True
        if rl == "m":
            raise ReturnToMain()
        if rl == "q":
            raise SystemExit(0)
        if rl == "n":
            _safe_call(_do_new_meal, before_date or date.today().isoformat())
            continue
        if rl == "s":
            _safe_call(_do_meal_food_search)
            continue
        if rl == "p":
            complete_page = [m for m in page if m["complete"]]
            if not complete_page:
                state.console.print("  [grey62]No complete meals shown.[/grey62]")
                continue
            # Also compute BCP for any other complete meals on the same dates,
            # so that Day BCP reflects the full day even for off-page meals.
            to_compute: list = list(complete_page)
            seen_ids = {m["id"] for m in complete_page}
            for _d in dates_in_page:
                with _db.get_db() as conn:
                    for dm in _db.meal_list_by_date(conn, _d):
                        if dm["complete"] and dm["id"] not in seen_ids:
                            to_compute.append(dm)
                            seen_ids.add(dm["id"])
            with state.console.status("[bold]Computing BCP…[/bold]", spinner="dots"):
                for m in to_compute:
                    bcp = _compute_meal_bcp(m["id"])
                    with _db.get_db() as conn:
                        _db.meal_set_bcp(conn, m["id"], bcp)
            # Compute day totals and % of profile protein goal, then persist.
            for _d in dates_in_page:
                with _db.get_db() as conn:
                    date_meals = _db.meal_list_by_date(conn, _d)
                day_vals = [
                    dm["bcp_g"] for dm in date_meals
                    if dm["complete"] and dm["bcp_g"] is not None
                ]
                day_total = sum(day_vals) if day_vals else None
                pct = (day_total / protein_target * 100.0
                       if day_total is not None and protein_target else None)
                for dm in date_meals:
                    if dm["complete"]:
                        with _db.get_db() as conn:
                            _db.meal_set_day_pct_goal(conn, dm["id"], pct)
            continue
        if rl == "mr" and has_more:
            offset += _MEALS_PAGE
            continue
        if len(rl) >= 2 and rl[0] in ("v", "e", "a"):
            meal = _resolve_meal(raw[1:])
            if meal is None:
                state.console.print(f"[{state.T['warning']}]Unknown meal ID — use v{{id}}, e{{id}}, or a{{id}} (e.g. v42).[/{state.T['warning']}]")
                continue
            if rl[0] in ("v", "e"):
                _safe_call(_open_meal_view, meal["id"])
            else:
                _safe_call(_open_meal_analyze, meal["id"])
            continue
        if len(rl) >= 2 and rl[0] == "d":
            suffix = raw[1:].strip()
            if _is_date_str(suffix):
                before_date = suffix
                offset = 0
                continue
            id_tokens = suffix.split()
            ids: list[int] = []
            valid = True
            for tok in id_tokens:
                if "-" in tok:
                    parts = tok.split("-", 1)
                    try:
                        lo, hi = int(parts[0]), int(parts[1])
                        if lo > hi:
                            valid = False
                            break
                        ids.extend(range(lo, hi + 1))
                    except ValueError:
                        valid = False
                        break
                else:
                    try:
                        ids.append(int(tok))
                    except ValueError:
                        valid = False
                        break
            if not valid or not ids:
                state.console.print(f"[{state.T['warning']}]Enter d{{id}} to delete (e.g. d42  or  d3 5 7  or  d3-7) or d{{YYYY-MM-DD}} to jump.[/{state.T['warning']}]")
                continue
            if len(ids) == 1:
                meal = _resolve_meal(str(ids[0]))
                if meal is None:
                    state.console.print(f"[{state.T['warning']}]Meal {ids[0]} not found.[/{state.T['warning']}]")
                    continue
                _safe_call(_do_meal_delete_by_id, meal["id"])
            else:
                _safe_call(_do_meal_delete_multiple, ids)
            continue
        state.console.print(f"[{state.T['warning']}]Unknown command.[/{state.T['warning']}]")


def _meal_add_items(meal_id: int) -> None:
    """Interactive loop to add food or recipe items to an existing meal.
    A single search finds both saved recipes (shown first as R#) and USDA/OFF foods."""
    with _db.get_db() as conn:
        meal_row = _db.meal_get(conn, meal_id)
    meal_name = meal_row["name"] if meal_row else ""
    _print_meal_items(meal_id, meal_name)
    _print_meal_protein_summary(meal_id)
    state.console.print(f"\n  Add new items  [grey62](Enter/b=back, m=main, q=quit)[/grey62]", highlight=False)
    while True:
        state.console.print()
        try:
            query = _prompt("Search food or recipe  [grey62](name · FDC ID · barcode · b/d=back, m=main, q=quit)[/grey62]", free_text=True).strip()
        except Cancelled:
            break
        ql = query.lower()
        if not query or ql in ("b", "d"):
            break
        if ql == "m":
            raise ReturnToMain()
        if ql == "q":
            raise SystemExit(0)

        # Find matching recipes instantly from local DB, ranked by word-hit count
        with _db.get_db() as conn:
            all_recipes = _db.recipe_list(conn)
        query_words = ql.split()
        matching_recipes = sorted(
            [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)],
            key=lambda r: (-sum(1 for w in query_words if w in r["name"].lower()), r["name"].lower()),
        )

        result = _search_and_pick_food(
            initial_query=query,
            prepend_recipes=matching_recipes or None,
            allow_research=False,
        )
        if result is None:
            continue

        if result.get("_type") == "recipe":
            rid              = result["id"]
            rname            = result["name"]
            r_total_weight = result.get("total_weight") or None
            if not r_total_weight:
                with _db.get_db() as conn:
                    r_total_weight = _db.recipe_auto_weight(conn, rid)
            r_total_servings = result["servings"] or 1
            srv_hint = "[grey62](servings e.g. 1, 1/2, 1.5  ·  or weight e.g. 290 g · b=back, m=main, q=quit)[/grey62]"
            servings = None
            portion_label = None
            while True:
                try:
                    raw_srv = _prompt(f"Recipe portion  {srv_hint}", default="1").strip()
                except Cancelled:
                    break
                lowered = raw_srv.lower()
                if not raw_srv or lowered in ("b", "back"):
                    break
                if lowered == "m":
                    raise ReturnToMain()
                if lowered == "q":
                    raise SystemExit(0)
                # Gram-weight entry: input ends with 'g'
                if raw_srv.rstrip().lower().endswith("g"):
                    gram_str = raw_srv.rstrip()[:-1].strip()
                    try:
                        grams = float(gram_str)
                    except ValueError:
                        grams = None
                    if grams is None or grams <= 0:
                        state.console.print(f"[{state.T['warning']}]Enter a positive weight (e.g. 290 g).[/{state.T['warning']}]")
                        continue
                    total_wt = r_total_weight
                    if not total_wt or total_wt <= 0:
                        # Recipe has no stored total weight — ask inline
                        state.console.print(f"  [grey62]Recipe '{rname}' has no total weight on record.[/grey62]")
                        try:
                            raw_tw = _prompt(
                                "Total weight of the full recipe  [grey62](e.g. 800 g — b=skip)[/grey62]",
                                free_text=True,
                            ).strip()
                        except Cancelled:
                            continue
                        if not raw_tw or raw_tw.lower() in ("b", "back"):
                            continue
                        tw_str = raw_tw.rstrip().rstrip("g").strip()
                        try:
                            total_wt = float(tw_str)
                        except ValueError:
                            total_wt = None
                        if not total_wt or total_wt <= 0:
                            state.console.print(f"[{state.T['warning']}]Enter a positive number (e.g. 800 g).[/{state.T['warning']}]")
                            continue
                    servings = grams / total_wt * r_total_servings
                    portion_label = f"{grams:g} g"
                    break
                # Servings entry
                servings = _parse_serving_amount(raw_srv)
                if servings is None or servings <= 0:
                    state.console.print(f"[{state.T['warning']}]Enter servings (e.g. 1, 1/2, 1.5) or a weight (e.g. 290 g).[/{state.T['warning']}]")
                    continue
                portion_label = _format_recipe_portion_label(servings)
                break
            if not servings or servings <= 0:
                continue
            with _db.get_db() as conn:
                _db.meal_add_recipe(conn, meal_id, rid, rname, servings, unit=portion_label)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {rname}  {portion_label}")
            _print_meal_items(meal_id, meal_name)
            _print_meal_protein_summary(meal_id)

        else:
            food = result
            portion = _pick_portion(food)
            if portion is None:
                continue
            grams, label, _ = portion
            try:
                notes = _prompt("Note for this item  [grey62](optional, Enter to skip)[/grey62]", default="", free_text=True).strip() or None
            except Cancelled:
                notes = None
            with _db.get_db() as conn:
                _db.meal_add_food(conn, meal_id, food["fdcId"], food["name"], grams, label, notes)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Added: {food['name']}  {label}")
            _print_meal_items(meal_id, meal_name)
            _print_meal_protein_summary(meal_id)


def _do_new_meal(default_date: str | None = None) -> None:
    """Create a new meal, then drop into the meal action loop."""
    try:
        meal_date = _ask_date("Date", default=default_date or date.today().isoformat())
    except Cancelled:
        return
    if meal_date is None:
        return
    try:
        name = _prompt("Meal name", default="Meal").strip() or "Meal"
    except Cancelled:
        return
    with _db.get_db() as conn:
        meal_id = _db.meal_create(conn, name, meal_date)
    state.console.print(
        f"[{state.T['success']}]✓[/{state.T['success']}] Meal "
        f"[{state.T['hi']}]{name}[/{state.T['hi']}] on {meal_date} created (ID {meal_id})."
    )
    _meal_action_loop(meal_id, name, meal_date)


def _open_meal_view(meal_id: int) -> None:
    with _db.get_db() as conn:
        m = _db.meal_get(conn, meal_id)
    if m is None:
        state.console.print(f"[{state.T['warning']}]Meal {meal_id} not found.[/{state.T['warning']}]")
        return
    _meal_action_loop(m["id"], m["name"], m["meal_date"])


def _open_meal_analyze(meal_id: int) -> None:
    with _db.get_db() as conn:
        m = _db.meal_get(conn, meal_id)
    if m is None:
        state.console.print(f"[{state.T['warning']}]Meal {meal_id} not found.[/{state.T['warning']}]")
        return
    meal_date = m["meal_date"]
    with _db.get_db() as conn:
        meals = _db.meal_list_by_date(conn, meal_date)
    if len(meals) > 1:
        try:
            scope = _prompt(
                f"Analyze just [{state.T['hi']}]{m['name']}[/{state.T['hi']}]"
                f" or all {len(meals)} meals on {meal_date}?",
                choices=["1", "2"], default="1",
            )
        except Cancelled:
            return
        if scope == "2":
            _analyze_day(meals, meal_date)
            return
    _analyze_meal_inline(m["id"], m["name"], meal_date)


def _do_meal_delete_by_id(meal_id: int) -> None:
    with _db.get_db() as conn:
        m = _db.meal_get(conn, meal_id)
    if m is None:
        state.console.print(f"[{state.T['warning']}]Meal {meal_id} not found.[/{state.T['warning']}]")
        return
    try:
        confirm = _prompt(
            f"Delete [{state.T['hi']}]{m['name']}[/{state.T['hi']}] ({m['meal_date']})?",
            choices=["y", "n"], default="n",
        )
    except Cancelled:
        return
    if confirm == "y":
        with _db.get_db() as conn:
            _db.meal_delete(conn, meal_id)
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Deleted.")
    else:
        state.console.print("[grey62]Cancelled.[/grey62]")


def _do_meal_delete_multiple(meal_ids: list[int]) -> None:
    meals = []
    for mid in meal_ids:
        with _db.get_db() as conn:
            m = _db.meal_get(conn, mid)
        if m is None:
            state.console.print(f"[{state.T['warning']}]Meal {mid} not found — skipping.[/{state.T['warning']}]")
        else:
            meals.append(m)
    if not meals:
        return
    state.console.print(f"  [grey62]About to delete {len(meals)} meal(s):[/grey62]")
    for m in meals:
        state.console.print(f"    [grey62]· {m['id']}  {m['meal_date']}  {m['name']}[/grey62]", highlight=False)
    try:
        confirm = _prompt(
            f"Delete {len(meals)} meal(s)?",
            choices=["y", "n"], default="n",
        )
    except Cancelled:
        return
    if confirm == "y":
        for m in meals:
            with _db.get_db() as conn:
                _db.meal_delete(conn, m["id"])
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Deleted {len(meals)} meal(s).")
    else:
        state.console.print("[grey62]Cancelled.[/grey62]")


def _print_meal_items(meal_id: int, meal_name: str) -> list:
    """Print items for a meal and return the list of items."""
    with _db.get_db() as conn:
        meal_row = _db.meal_get(conn, meal_id)
        items    = _db.meal_get_items(conn, meal_id)
    date_prefix = f"{meal_row['meal_date']}  ·  " if meal_row else ""
    section_title(f"{date_prefix}{meal_name}  [grey62](ID {meal_id})[/grey62]")
    if not items:
        state.console.print("    [grey62]No items logged.[/grey62]")
    else:
        _MITEM_W = 38
        tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None,
                    padding=(0, 1), pad_edge=False)
        tbl.add_column("ID", justify="right", min_width=4)
        tbl.add_column("Amount", min_width=10)
        tbl.add_column("Food / Recipe", min_width=_MITEM_W, max_width=_MITEM_W, no_wrap=True)
        for it in items:
            if it["item_type"] == "recipe":
                unit = it["unit"] or ""
                amount_label = unit if unit and unit != "servings" else _format_recipe_portion_label(float(it["amount"]))
                fname = it["food_name"][:_MITEM_W - 1]
                fdots = "·" * (_MITEM_W - len(fname) - 1)
                name_cell = f"{fname} [grey62]{fdots}[/grey62]"
            else:
                unit = it["unit"] or "g"
                if unit == "g":
                    amount_label = f"{it['amount']:g} g"
                else:
                    amount_label = _normalize_unit_display(unit)
                fdc_str = str(it['fdc_id'])
                visible_len = len(fdc_str) + 2 + len(it['food_name'])
                fdots = "·" * max(0, _MITEM_W - visible_len - 1)
                name_cell = f"[grey62]{fdc_str}[/grey62]  {it['food_name']} [grey62]{fdots}[/grey62]"
            tbl.add_row(str(it["id"]), amount_label, name_cell)
        state.console.print(tbl)
        help_footer("meal-detail")
    return list(items)


def _recipe_total_nutrients(recipe_id: int) -> dict[str, float]:
    """Return summed raw nutrients for all ingredients in a recipe, handling nested recipes."""
    with _db.get_db() as conn:
        ings = _db.recipe_get_ingredients(conn, recipe_id)
    total: dict[str, float] = {}
    for ing in ings:
        if ing["ref_recipe_id"]:
            with _db.get_db() as conn:
                sub = _db.recipe_get(conn, ing["ref_recipe_id"])
            sub_servings = sub["servings"] if sub and sub["servings"] and sub["servings"] > 0 else 1
            sub_total = _recipe_total_nutrients(ing["ref_recipe_id"])
            portion = ing["amount"] / sub_servings
            total = _usda.sum_nutrients(total, {k: v * portion for k, v in sub_total.items()})
        else:
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, ing["fdc_id"])
            if cached:
                scaled = _usda.scale_nutrients(
                    json.loads(cached["nutrients_json"]), ing["amount"], base_size=100.0
                )
                total = _usda.sum_nutrients(total, scaled)
    return total


def _compute_meal_nutrients(meal_id: int) -> dict[str, float] | None:
    """Return combined nutrients for all items in a meal, or None if no data."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
    combined: dict[str, float] = {}
    for item in items:
        if item["item_type"] == "food":
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, item["fdc_id"])
            if cached:
                scaled = _usda.scale_nutrients(
                    json.loads(cached["nutrients_json"]), item["amount"], base_size=100.0
                )
                combined = _usda.sum_nutrients(combined, scaled)
        elif item["item_type"] == "recipe":
            with _db.get_db() as conn:
                recipe = _db.recipe_get(conn, item["recipe_id"])
            if recipe:
                recipe_total = _recipe_total_nutrients(item["recipe_id"])
                portion = item["amount"] / recipe["servings"] if recipe["servings"] and recipe["servings"] > 0 else item["amount"]
                scaled_recipe = {k: v * portion for k, v in recipe_total.items()}
                combined = _usda.sum_nutrients(combined, scaled_recipe)
    return combined if combined else None


def _compute_meal_ingredient_list(meal_id: int, force_refresh: bool = False) -> list[dict]:
    """
    Return per-ingredient data for a meal, suitable for meal-level DIAAS calculation.

    Each returned dict has:
        "food_name":      str
        "nutrients_100g": dict[str, float]   — USDA nutrients per 100g
        "grams":          float              — actual grams consumed

    Recipe items are expanded into their constituent ingredients (scaled by serving portion).
    By default uses cache-only (no API calls). Pass force_refresh=True to fetch AA data
    from USDA for any foods that are missing it.
    """
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)

    def _best_nutrients(fdc_id: int, food_name: str) -> dict[str, float] | None:
        """Return the best available nutrient dict for a food, with AA data if possible."""
        if force_refresh:
            refreshed = _refresh_cache_if_missing_aa(fdc_id)
        else:
            refreshed = None
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached is None:
            return None
        nutrients = refreshed if refreshed is not None else json.loads(cached["nutrients_json"])
        # If still missing AA data, try merging from the complement table
        if not _usda.has_amino_acid_data(nutrients):
            complement = _usda.get_complement_nutrients(food_name)
            if complement and _usda.has_amino_acid_data(complement):
                # Scale complement table AAs to match actual protein content
                actual_protein = nutrients.get("protein_g", 0)
                ref_protein = complement.get("protein_g", 0)
                if ref_protein > 0 and actual_protein > 0:
                    scale = actual_protein / ref_protein
                    merged = dict(nutrients)
                    for k, v in complement.items():
                        if k.startswith("aa_") and k not in merged:
                            merged[k] = v * scale
                    return merged
        return nutrients

    def _expand_ings(recipe_id: int, portion: float) -> list[dict]:
        with _db.get_db() as conn:
            ings = _db.recipe_get_ingredients(conn, recipe_id)
        out: list[dict] = []
        for ing in ings:
            if ing["ref_recipe_id"]:
                with _db.get_db() as conn:
                    sub = _db.recipe_get(conn, ing["ref_recipe_id"])
                sub_servings = sub["servings"] if sub and sub["servings"] and sub["servings"] > 0 else 1
                sub_portion = ing["amount"] / sub_servings * portion
                out.extend(_expand_ings(ing["ref_recipe_id"], sub_portion))
            else:
                nutrients = _best_nutrients(ing["fdc_id"], ing["food_name"])
                if nutrients is not None:
                    out.append({
                        "food_name":      ing["food_name"],
                        "fdc_id":         ing["fdc_id"],
                        "nutrients_100g": nutrients,
                        "grams":          ing["amount"] * portion,
                    })
        return out

    result: list[dict] = []
    for item in items:
        if item["item_type"] == "food":
            nutrients = _best_nutrients(item["fdc_id"], item["food_name"])
            if nutrients is not None:
                result.append({
                    "food_name":      item["food_name"],
                    "fdc_id":         item["fdc_id"],
                    "nutrients_100g": nutrients,
                    "grams":          item["amount"],
                })
        elif item["item_type"] == "recipe":
            with _db.get_db() as conn:
                recipe = _db.recipe_get(conn, item["recipe_id"])
            if recipe:
                portion = item["amount"] / recipe["servings"] if recipe["servings"] and recipe["servings"] > 0 else item["amount"]
                result.extend(_expand_ings(item["recipe_id"], portion))
    return result


def _compute_meal_gl(meal_id: int) -> tuple[float, list[str]]:
    """Compute glycemic load for a meal. Returns (gl_total, blockers).
    blockers is empty if GL is fully computable; non-empty means incomplete GI data."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)

    food_ids = [it["fdc_id"] for it in items if it["item_type"] == "food" and it["fdc_id"]]
    with _db.get_db() as conn:
        ann_map = _db.annotations_for_fdcids(conn, food_ids) if food_ids else {}

    blockers: list[str] = []
    gl_total = 0.0

    for item in items:
        if item["item_type"] == "recipe":
            with _db.get_db() as conn:
                recipe = _db.recipe_get(conn, item["recipe_id"])
            if recipe is None or recipe["gl_g"] is None:
                name = recipe["name"] if recipe else f"recipe #{item['recipe_id']}"
                blockers.append(f"{name} (no GL — analyze it first)")
            else:
                servings = recipe["servings"] or 1
                gl_total += recipe["gl_g"] * (item["amount"] / servings)
            continue

        ann = ann_map.get(item["fdc_id"])
        if ann is None or ann["gi_estimate"] is None:
            blockers.append(item["food_name"])
            continue

        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, item["fdc_id"])
        if cached is None:
            blockers.append(item["food_name"])
            continue

        carbs_g = json.loads(cached["nutrients_json"]).get("carbs_g", 0.0) * item["amount"] / 100.0
        gl_total += ann["gi_estimate"] * carbs_g / 100.0

    return (gl_total, blockers)


def _analyze_meal_inline(meal_id: int, meal_name: str, meal_date: str) -> None:
    """Analyze a single meal: nutrients, DIAAS, protein adequacy, complement suggestions."""
    _print_meal_items(meal_id, meal_name)
    nutrients = _compute_meal_nutrients(meal_id)
    if nutrients is None:
        state.console.print("[grey62]No nutrient data found for this meal. "
                      "Ensure all ingredients are in the cache.[/grey62]")
        return

    # Compute today's running total and RDA for the % today column
    profile = _profile.load_profile()
    daily_nutrients: dict[str, float] | None = None
    rda = None
    with _db.get_db() as conn:
        today_meals = _db.meal_list_by_date(conn, meal_date)
    if profile:
        daily_parts = [n for m in today_meals if (n := _compute_meal_nutrients(m["id"]))]
        if daily_parts:
            daily_nutrients = _usda.sum_nutrients(*daily_parts)
        rda = _profile.compute_rda(profile)

    _print_nutrient_table(nutrients, title=f"Nutrient analysis for {meal_name}",
                          daily_nutrients=daily_nutrients, rda=rda)

    ing_list = _compute_meal_ingredient_list(meal_id)
    missing_aa, _dcp_g = _print_meal_diaas(ing_list, profile=profile)
    if missing_aa:
        pbn = {
            ing["food_name"]: ing["nutrients_100g"].get("protein_g", 0.0) * ing["grams"] / 100.0
            for ing in ing_list
        }
        _fix_meal_aa_profiles(meal_id, missing_aa, protein_by_name=pbn)

    # Meal-level complement suggestions and glycemic load
    aa_nutrients = _usda.sum_nutrients(*[
        _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
        for ing in ing_list
        if _usda.has_amino_acid_data(ing["nutrients_100g"])
    ]) if ing_list else {}
    if aa_nutrients:
        _print_complement_suggestions(aa_nutrients, context="meal", offer_if_covered=True)

    gl_total, gl_blockers = _compute_meal_gl(meal_id)
    section_title("Glycemic load")
    if gl_blockers:
        state.console.print(
            f"  [{state.T['warning']}]Not available — GI annotation missing for:[/{state.T['warning']}]"
        )
        for name in gl_blockers:
            state.console.print(f"    [grey62]• {name}[/grey62]")
        state.console.print(
            "  [grey62]Annotate foods under Foods → View / edit / delete cached foods → pick food → Annotate.[/grey62]"
        )
    else:
        color = (state.T["success"] if gl_total <= 10
                 else state.T["warning"] if gl_total <= 19
                 else state.T["error"])
        state.console.print(
            f"  [{color}]{gl_total:.1f}[/{color}]  [grey62]this meal[/grey62]",
            highlight=False,
        )
    help_footer("glycemic")

    # Day-level analysis (only when there are multiple meals today)
    if len(today_meals) > 1:
        all_day_ings: list[dict] = []
        for m in today_meals:
            all_day_ings.extend(_compute_meal_ingredient_list(m["id"]))
        _print_meal_diaas(all_day_ings, profile=profile, title="Day-Level Complete Protein Analysis")
        day_aa_nutrients = _usda.sum_nutrients(*[
            _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
            for ing in all_day_ings
            if _usda.has_amino_acid_data(ing["nutrients_100g"])
        ]) if all_day_ings else {}
        if day_aa_nutrients:
            _print_complement_suggestions(day_aa_nutrients, context="daily", basis_label="all meals today", silent_if_complete=True)

        gl_total_day = 0.0
        gl_blockers_day: list[str] = []
        for m in today_meals:
            gl, bl = _compute_meal_gl(m["id"])
            if not bl:
                gl_total_day += gl
            gl_blockers_day.extend(bl)
        section_title("Glycemic load — all meals today")
        if gl_blockers_day:
            state.console.print(
                f"  [{state.T['warning']}]Not available — GI annotation missing for:[/{state.T['warning']}]"
            )
            seen: set[str] = set()
            for name in gl_blockers_day:
                if name not in seen:
                    state.console.print(f"    [grey62]• {name}[/grey62]")
                    seen.add(name)
            state.console.print(
                "  [grey62]Annotate foods under Foods → View / edit / delete cached foods → pick food → Annotate.[/grey62]"
            )
        else:
            color = (state.T["success"] if gl_total_day <= 10
                     else state.T["warning"] if gl_total_day <= 19
                     else state.T["error"])
            state.console.print(
                f"  [{color}]{gl_total_day:.1f}[/{color}]  [grey62]all meals — {meal_date}[/grey62]",
                highlight=False,
            )
        help_footer("glycemic")

    # AA data source note + optional USDA refresh (always offered)
    if ing_list:
        note = "AA data: local cache"
        if missing_aa:
            note += f"  ({len(missing_aa)} food(s) missing AA data)"
        state.console.print(f"\n  [grey62]{note}[/grey62]")
        try:
            fetch_ans = _prompt(
                "Refresh AA data from USDA?",
                choices=["y", "n"], default="n",
            )
        except Cancelled:
            fetch_ans = "n"
        if fetch_ans == "y":
            name_to_fdc: dict[str, int] = {
                ing["food_name"]: ing["fdc_id"] for ing in ing_list if "fdc_id" in ing
            }
            targets = set(missing_aa) if missing_aa else set(name_to_fdc)
            with state.console.status("[bold]Fetching AA data from USDA…[/bold]", spinner="dots"):
                for food_name, fdc_id in name_to_fdc.items():
                    if food_name in targets:
                        _refresh_cache_if_missing_aa(fdc_id)
            state.console.print(
                "  [grey62]AA data updated in cache — re-run analysis to see the full picture.[/grey62]"
            )


def _meal_action_loop(meal_id: int, meal_name: str, meal_date: str) -> bool:
    """
    Interactive design/edit loop for a single meal: add · edit · remove · analyze · manage.
    Returns True to go back to a meal-picker list, False to return to caller.
    """
    _print_meal_items(meal_id, meal_name)
    while True:
        with _db.get_db() as conn:
            meal_row = _db.meal_get(conn, meal_id)
            if meal_row is None:
                return False
            is_complete = bool(meal_row["complete"])
            siblings = [m for m in _db.meal_list_by_date(conn, meal_date) if m["id"] != meal_id]

        menu_items = [
            ("1", "Add items"),
            ("2", "Edit an item"),
            ("3", "Remove an item"),
            ("4", "Analyze this meal"),
            ("5", "Delete this meal"),
            ("6", "Mark complete" if not is_complete else "Mark incomplete"),
            ("7", "Edit meal name or date"),
        ]
        if siblings:
            menu_items.append(("8", "Merge with meal(s) on same date"))
        menu_items += [
            ("b", "Back to previous menu"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ]
        status_label = "[green]✓ complete[/green]" if is_complete else "[grey62][?] incomplete[/grey62]"
        _show_menu(f"Actions — {meal_name}  {status_label}", menu_items)
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return True

        if choice == "1":
            _meal_add_items(meal_id)
            _print_meal_items(meal_id, meal_name)

        elif choice == "2":
            items = _print_meal_items(meal_id, meal_name)
            if not items:
                continue
            try:
                raw_iid = _prompt("Item ID to edit").strip()
            except Cancelled:
                continue
            if not raw_iid or raw_iid.lower() == "b":
                continue
            if raw_iid.lower() == "m":
                raise ReturnToMain()
            if raw_iid.lower() == "q":
                raise SystemExit(0)
            iid = None
            try:
                iid = int(raw_iid)
            except ValueError:
                pass
            item = next((it for it in items if it["id"] == iid), None)
            if item is None:
                state.console.print(f"[{state.T['warning']}]Invalid item ID.[/{state.T['warning']}]")
                continue
            if item["item_type"] == "recipe":
                try:
                    raw_sv = _prompt("Recipe portion in servings", default=str(item["amount"])).strip()
                except Cancelled:
                    continue
                try:
                    servings = _parse_serving_amount(raw_sv)
                    if servings is None or servings <= 0:
                        raise ValueError
                except ValueError:
                    state.console.print(f"[{state.T['warning']}]Enter a number.[/{state.T['warning']}]")
                    continue
                with _db.get_db() as conn:
                    _db.meal_update_item(conn, iid, meal_id, servings, item["unit"])
                state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Updated to {_format_recipe_portion_label(servings)}.")
            else:
                cur_fdc_id = item["fdc_id"]
                cur_name   = item["food_name"]
                cur_amount = item["amount"]
                cur_unit   = item["unit"]
                cur_notes  = item["notes"] or ""
                changed    = False
                while True:
                    amt_display = (f"{_normalize_unit_display(cur_unit)}  ({cur_amount:.0f} g)"
                                   if cur_amount and cur_amount > 0 and cur_unit and cur_unit != "—"
                                   else "—")
                    notes_display = f"  [grey62]Note: {cur_notes}[/grey62]" if cur_notes else ""
                    state.console.print(f"\n  [grey62]Editing:[/grey62] [bold]{cur_name}[/bold]  {amt_display}{notes_display}")
                    state.console.print(f"  [{state.T['accent']}]f.[/{state.T['accent']}] Change food (search by new name)")
                    state.console.print(f"  [{state.T['accent']}]a.[/{state.T['accent']}] Change amount")
                    state.console.print(f"  [{state.T['accent']}]n.[/{state.T['accent']}] Edit note")
                    state.console.print(f"  [grey62]d / done  — save and exit[/grey62]")
                    try:
                        sub = _prompt("Choice").strip().lower()
                    except Cancelled:
                        break
                    if sub in ("b", "d", "done", ""):
                        break
                    if sub == "q":
                        raise SystemExit(0)
                    if sub == "n":
                        try:
                            new_notes = _prompt("Note  [grey62](Enter to clear)[/grey62]", default=cur_notes, free_text=True).strip()
                        except Cancelled:
                            continue
                        cur_notes = new_notes
                        changed = True
                    elif sub == "f":
                        try:
                            query = _prompt("Search for food").strip()
                        except Cancelled:
                            continue
                        if not query:
                            continue
                        new_food = _search_and_pick_food(initial_query=query)
                        if new_food is None:
                            state.console.print(f"  [{state.T['warning']}]Food not changed "
                                          f"(selection cancelled or fetch failed).[/{state.T['warning']}]")
                            continue
                        cur_fdc_id = new_food["fdcId"]
                        cur_name   = new_food["name"]
                        changed = True
                        state.console.print(f"  [grey62]Food set to: {cur_name}[/grey62]")
                    elif sub == "a":
                        with _db.get_db() as conn:
                            cached = _db.get_cached_food(conn, cur_fdc_id)
                        if cached is None:
                            state.console.print(f"[{state.T['warning']}]Food not in cache yet; add it first.[/{state.T['warning']}]")
                            continue
                        food_dict = {
                            "fdcId":       cached["fdc_id"],
                            "name":        cached["name"],
                            "dataType":    cached["data_type"],
                            "brand":       cached["brand"],
                            "servingSize": cached["serving_size"],
                            "servingUnit": cached["serving_unit"],
                            "nutrients":   json.loads(cached["nutrients_json"]),
                            "portions":    json.loads(cached["portions_json"]) if cached["portions_json"] else [],
                        }
                        result = _pick_portion(food_dict)
                        if result is None:
                            continue
                        cur_amount, cur_unit, _ = result
                        changed = True
                if changed:
                    with _db.get_db() as conn:
                        _db.meal_replace_food(conn, iid, meal_id, cur_fdc_id,
                                              cur_name, cur_amount, cur_unit,
                                              cur_notes or None)
                    state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Saved: {cur_name}  "
                                  f"{_normalize_unit_display(cur_unit)}")
            _print_meal_items(meal_id, meal_name)

        elif choice == "3":
            items = _print_meal_items(meal_id, meal_name)
            if not items:
                continue
            try:
                raw_iid = _prompt("Item ID to remove").strip()
            except Cancelled:
                continue
            if not raw_iid or raw_iid.lower() == "b":
                continue
            if raw_iid.lower() == "m":
                raise ReturnToMain()
            if raw_iid.lower() == "q":
                raise SystemExit(0)
            iid = None
            try:
                iid = int(raw_iid)
            except ValueError:
                pass
            if iid is None or not any(it["id"] == iid for it in items):
                state.console.print(f"[{state.T['warning']}]Invalid item ID.[/{state.T['warning']}]")
                continue
            with _db.get_db() as conn:
                removed = _db.meal_remove_item(conn, iid, meal_id)
            if removed:
                state.console.print(f"[{state.T['success']}]Item removed.[/{state.T['success']}]")
                _print_meal_items(meal_id, meal_name)
            else:
                state.console.print(f"[{state.T['warning']}]Could not remove item.[/{state.T['warning']}]")

        elif choice == "4":
            _analyze_meal_inline(meal_id, meal_name, meal_date)

        elif choice == "5":
            try:
                confirm = _prompt(f"Delete '{meal_name}'?  [grey62](y/n)[/grey62]", choices=["y", "n"], default="n")
            except Cancelled:
                continue
            if confirm != "y":
                continue
            with _db.get_db() as conn:
                _db.meal_delete(conn, meal_id)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Deleted: {meal_name}")
            return False

        elif choice == "6":
            new_complete = not is_complete
            with _db.get_db() as conn:
                _db.meal_set_complete(conn, meal_id, new_complete)
            label = "complete" if new_complete else "incomplete"
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Marked {label}.")

        elif choice == "7":
            # --- name ---
            try:
                new_name = _prompt("Meal name  [grey62](b=back, m=main, q=quit)[/grey62]", default=meal_name, prefill=True, free_text=True, two_line=True).strip()
            except Cancelled:
                continue
            if not new_name or new_name.lower() == "b":
                continue
            if new_name.lower() == "m":
                raise ReturnToMain()
            if new_name.lower() == "q":
                raise SystemExit(0)
            # --- date ---
            new_date: str | None = None
            while True:
                try:
                    raw_date = _prompt("Meal date  [grey62](YYYY-MM-DD, b=cancel, m=main, q=quit)[/grey62]", default=meal_date, prefill=True, two_line=True).strip()
                except Cancelled:
                    raw_date = "b"
                if not raw_date or raw_date.lower() == "b":
                    new_date = None
                    break
                if raw_date.lower() == "m":
                    raise ReturnToMain()
                if raw_date.lower() == "q":
                    raise SystemExit(0)
                try:
                    datetime.strptime(raw_date, "%Y-%m-%d")
                    new_date = raw_date
                    break
                except ValueError:
                    state.console.print(f"  [{state.T['warning']}]Use YYYY-MM-DD format (e.g. 2026-01-15).[/{state.T['warning']}]")
            if new_date is None:
                continue
            with _db.get_db() as conn:
                if new_name != meal_name:
                    _db.meal_rename(conn, meal_id, new_name)
                if new_date != meal_date:
                    _db.meal_set_date(conn, meal_id, new_date)
            meal_name = new_name
            meal_date = new_date
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {meal_name} [grey62]{meal_date}[/grey62]")

        elif choice == "8" and siblings:
            with _db.get_db() as conn:
                all_on_date = _db.meal_list_by_date(conn, meal_date)
            ids_str = "  ".join(f"{m['id']}={m['name']}" for m in all_on_date)
            state.console.print(f"  [grey62]Meals on {meal_date}: {ids_str}[/grey62]")
            try:
                raw_ids = _prompt(
                    "Meal IDs to merge  [grey62](space-separated, or 'all', b=back, m=main)[/grey62]",
                    default="all",
                ).strip().lower()
            except Cancelled:
                continue
            if raw_ids in ("b", ""):
                continue
            if raw_ids == "m":
                raise ReturnToMain()
            if raw_ids == "q":
                raise SystemExit(0)
            if raw_ids == "all":
                selected = list(all_on_date)
            else:
                selected_ids = []
                valid = True
                for tok in raw_ids.split():
                    try:
                        selected_ids.append(int(tok))
                    except ValueError:
                        state.console.print(f"[{state.T['warning']}]Invalid ID: {tok}[/{state.T['warning']}]")
                        valid = False
                        break
                if not valid:
                    continue
                selected = [m for m in all_on_date if m["id"] in selected_ids]
                missing = set(selected_ids) - {m["id"] for m in selected}
                if missing:
                    state.console.print(f"[{state.T['warning']}]IDs not found: {' '.join(str(x) for x in missing)}[/{state.T['warning']}]")
                    continue
                if len(selected) < 2:
                    state.console.print(f"[{state.T['warning']}]Select at least 2 meals to merge.[/{state.T['warning']}]")
                    continue
            default_name = selected[0]["name"]
            try:
                new_name = _prompt("Name for merged meal  [grey62](b=back, m=main, q=quit)[/grey62]", default=default_name, prefill=True, two_line=True).strip()
            except Cancelled:
                continue
            if not new_name or new_name.lower() == "b":
                continue
            if new_name.lower() == "m":
                raise ReturnToMain()
            if new_name.lower() == "q":
                raise SystemExit(0)
            new_name = new_name or default_name
            with _db.get_db() as conn:
                new_mid = _db.meal_create(conn, new_name, meal_date)
                total_items = sum(_db.meal_copy_items(conn, m["id"], new_mid) for m in selected)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Created '{new_name}' "
                          f"(ID {new_mid}) with {total_items} item(s).")
            try:
                del_orig = _prompt("Delete original meals?  [grey62](y/n)[/grey62]", choices=["y", "n"], default="y")
            except Cancelled:
                del_orig = "n"
            if del_orig == "y":
                with _db.get_db() as conn:
                    for m in selected:
                        _db.meal_delete(conn, m["id"])
                state.console.print(f"  [grey62]Deleted {len(selected)} original meal(s).[/grey62]")
            if del_orig == "y" and any(m["id"] == meal_id for m in selected):
                return False
            _print_meal_items(new_mid, new_name)

        elif choice in ("b", ""):
            return True
        elif choice == "m":
            raise ReturnToMain()
        elif choice == "q":
            raise SystemExit(0)
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _analyze_day(meals: list, meal_date: str) -> None:
    """Analyze and display combined nutrients for all meals on a given date."""
    combined: dict[str, float] = {}
    all_ings: list[dict] = []
    state.console.print()
    for m in meals:
        n = _compute_meal_nutrients(m["id"])
        if n:
            combined = _usda.sum_nutrients(combined, n)
        all_ings.extend(_compute_meal_ingredient_list(m["id"]))
    if not combined:
        state.console.print("[grey62]No nutrient data found.[/grey62]")
        return
    title = f"All meals — {meal_date}"
    _print_nutrient_table(combined, title=f"Nutrient analysis for {title}")
    profile = _profile.load_profile()
    _missing_aa, _dcp_g = _print_meal_diaas(all_ings, profile=profile)
    aa_nutrients = _usda.sum_nutrients(*[
        _usda.scale_nutrients(ing["nutrients_100g"], ing["grams"], base_size=100.0)
        for ing in all_ings
        if _usda.has_amino_acid_data(ing["nutrients_100g"])
    ]) if all_ings else {}
    if aa_nutrients:
        _print_complement_suggestions(aa_nutrients, context="meal", offer_if_covered=True)
    gl_total_day = 0.0
    gl_blockers_day: list[str] = []
    for m in meals:
        gl, bl = _compute_meal_gl(m["id"])
        if not bl:
            gl_total_day += gl
        gl_blockers_day.extend(bl)
    section_title("Glycemic load")
    if gl_blockers_day:
        state.console.print(
            f"  [{state.T['warning']}]Not available — GI annotation missing for:[/{state.T['warning']}]"
        )
        seen: set[str] = set()
        for name in gl_blockers_day:
            if name not in seen:
                state.console.print(f"    [grey62]• {name}[/grey62]")
                seen.add(name)
        state.console.print(
            "  [grey62]Annotate foods under Foods → View / edit / delete cached foods → pick food → Annotate.[/grey62]"
        )
    else:
        color = (state.T["success"] if gl_total_day <= 10
                 else state.T["warning"] if gl_total_day <= 19
                 else state.T["error"])
        state.console.print(
            f"  [{color}]{gl_total_day:.1f}[/{color}]  [grey62]all meals — {meal_date}[/grey62]",
            highlight=False,
        )
    help_footer("glycemic")
    state.console.print("\n  [grey62]AA data: local cache[/grey62]")
    _offer_export(title, [
        {"type": "nutrient_table", "title": title, "nutrients": combined},
        {"type": "protein_completeness", "nutrients": combined},
    ])


# ---------------------------------------------------------------------------
# Meal history food search
# ---------------------------------------------------------------------------

def _print_meal_history_flat(rows: list, query: str) -> None:
    _W_MEAL = 18
    _W_FOOD = 32
    _W_NOTE = 16
    table_title("MEAL HISTORY — OCCURRENCES", f"[grey62]search: '{query}'[/grey62]")
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Date",    min_width=10, no_wrap=True)
    tbl.add_column("Meal",    min_width=_W_MEAL, max_width=_W_MEAL, no_wrap=True)
    tbl.add_column("Food / Recipe", min_width=_W_FOOD, max_width=_W_FOOD, no_wrap=True)
    tbl.add_column("Portion", min_width=12, justify="right")
    tbl.add_column("Notes",   min_width=_W_NOTE, max_width=_W_NOTE, no_wrap=True)
    for r in rows:
        is_recipe = r["item_type"] == "recipe"
        portion   = r["unit"] if r["unit"] else (f"{r['amount']:.0f} g" if r["amount"] else "[grey62]—[/grey62]")
        notes     = r["notes"] or ""
        name_cell = (f"{r['food_name']} [grey62](recipe)[/grey62]" if is_recipe else r["food_name"])
        tbl.add_row(r["meal_date"], r["meal_name"], name_cell, portion, notes)
    state.console.print(tbl)
    help_footer("meal-history")


def _print_meal_history_summary(rows: list) -> None:
    from collections import defaultdict
    groups: dict[str, list] = defaultdict(list)
    for r in rows:
        groups[r["food_name"]].append(r)

    table_title("MEAL HISTORY — SUMMARY")
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("Food / Recipe", min_width=34, max_width=34, no_wrap=True)
    tbl.add_column("Times", min_width=5,  justify="right")
    tbl.add_column("Total", min_width=10, justify="right")
    tbl.add_column("First", min_width=10)
    tbl.add_column("Last",  min_width=10)

    sorted_groups = sorted(
        groups.items(),
        key=lambda kv: max(r["meal_date"] for r in kv[1]),
        reverse=True,
    )
    s = state.T["success"]
    for food_name, items in sorted_groups:
        is_recipe  = items[0]["item_type"] == "recipe"
        dates      = sorted(r["meal_date"] for r in items)
        if is_recipe:
            total_str  = "[grey62]—[/grey62]"
            name_cell  = f"{food_name} [grey62](recipe)[/grey62]"
        else:
            total_g   = sum(r["amount"] for r in items if r["amount"])
            total_str = f"[{s}]{total_g:.0f} g[/{s}]" if total_g else "[grey62]—[/grey62]"
            name_cell = food_name
        tbl.add_row(name_cell, str(len(items)), total_str, dates[0], dates[-1])
    state.console.print(tbl)
    help_footer("meal-history")


def _do_meal_food_search() -> None:
    """Search all logged meal items for a food by name (and fdc_id cross-reference)."""
    try:
        query = _prompt("Search food in meal history", free_text=True).strip()
    except Cancelled:
        return
    if not query or query.lower() == "b":
        return
    if query.lower() == "m":
        raise ReturnToMain()
    if query.lower() == "q":
        raise SystemExit(0)

    with _db.get_db() as conn:
        rows = _db.search_meal_history(conn, query)

    if not rows:
        state.console.print(
            f"[{state.T['warning']}]No meal items match '{query}'.[/{state.T['warning']}]\n"
            f"[grey62]Note: ingredients inside logged recipes are not searched — only foods and recipes logged directly.[/grey62]"
        )
        return

    n_items = len(rows)
    n_meals = len({r["meal_id"] for r in rows})
    n_dates = len({r["meal_date"] for r in rows})
    state.console.print(
        f"\n  [grey62]Found [bold]{n_items}[/bold] occurrence{'s' if n_items != 1 else ''} "
        f"across [bold]{n_meals}[/bold] meal{'s' if n_meals != 1 else ''} "
        f"on [bold]{n_dates}[/bold] date{'s' if n_dates != 1 else ''}.[/grey62]"
        f"\n  [grey62]Ingredients inside logged recipes are not included.[/grey62]\n"
    )

    try:
        view = _prompt_with_options(
            "View as",
            [("1", "Flat list  (every occurrence)"),
             ("2", "Summary  (totals per food name)"),
             ("3", "Both")],
            default="3",
        )
    except Cancelled:
        return
    if not view or view == "b":
        return
    if view == "m":
        raise ReturnToMain()
    if view == "q":
        raise SystemExit(0)

    if view in ("1", "3"):
        _print_meal_history_flat(rows, query)
    if view in ("2", "3"):
        _print_meal_history_summary(rows)
