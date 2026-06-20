"""
backend.py — FastAPI web interface for numa nutritional analysis.
Docs: README-numa-documentation.md, Architecture: "web/ — Local web app"
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import markdown as _md
from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import db as _db
import diaas as _diaas
import profile as _profile
import usda as _usda

_WEB_DIR    = Path(__file__).parent
_MANUAL     = _WEB_DIR.parent / "user-manual.md"
_HOME_MD    = _WEB_DIR.parent / "home.md"
_PREFS_FILE = Path.home() / ".local" / "share" / "numa" / "prefs.json"

_HOME_CACHE = _WEB_DIR / "home_body.cache"

def _render_home_md() -> str:
    if not _HOME_MD.exists():
        return ""
    if _HOME_CACHE.exists() and _HOME_CACHE.stat().st_mtime >= _HOME_MD.stat().st_mtime:
        return _HOME_CACHE.read_text(encoding="utf-8")
    html = _md.markdown(_HOME_MD.read_text(encoding="utf-8"), extensions=["footnotes"])
    _HOME_CACHE.write_text(html, encoding="utf-8")
    return html

_HOME_BODY = _render_home_md()

_DIET_LABELS = {
    "all":        "All animal foods (meat, fish, dairy, eggs)",
    "vegetarian": "Vegetarian (dairy + eggs only)",
    "plant_only": "Plant-based only",
}
_VALID_DIET_PREFS = {"all", "vegetarian", "plant_only"}


def _load_prefs_file() -> dict:
    if _PREFS_FILE.exists():
        try:
            data = json.loads(_PREFS_FILE.read_text())
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_prefs_file(updates: dict) -> None:
    data = _load_prefs_file()
    data.update(updates)
    _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    _PREFS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

app = FastAPI(title="numa")
app.mount("/static", StaticFiles(directory=_WEB_DIR / "static"), name="static")
templates = Jinja2Templates(directory=_WEB_DIR / "templates")

# Custom Jinja2 filters
templates.env.filters["ftin_ft"]  = lambda cm: _profile.cm_to_ftin(cm)[0]
templates.env.filters["ftin_in"]  = lambda cm: round(_profile.cm_to_ftin(cm)[1], 1)
templates.env.filters["fromjson"] = json.loads

# ---------------------------------------------------------------------------
# Nutrient display groups (ordered for presentation)
# ---------------------------------------------------------------------------

_NUTRIENT_GROUPS: list[tuple[str, list[str]]] = [
    ("Macronutrients", [
        "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
        "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    ]),
    ("Omega Fatty Acids", [
        "omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg",
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
]


def _rda_css(pct: float, rda_type: str) -> str:
    if rda_type == "limit":
        return "rda-over" if pct > 100 else "rda-met"
    return "rda-met" if pct >= 100 else ("rda-near" if pct >= 75 else "rda-low")


def _nutrient_sections(nutrients: dict, rda: dict | None = None,
                       daily_nutrients: dict | None = None) -> list[dict]:
    sections = []
    for group_name, keys in _NUTRIENT_GROUPS:
        rows = []
        for key in keys:
            val = nutrients.get(key)
            if not val:
                continue
            label, unit = _usda.nutrient_label(key)
            pct = rda_type = rda_css_val = None
            day_pct = day_rda_css = None
            if rda and key in rda:
                rda_val, _rda_unit, rda_type = rda[key]
                if rda_val and rda_val > 0:
                    pct = round(val / rda_val * 100, 0)
                    rda_css_val = _rda_css(pct, rda_type)
                    if daily_nutrients is not None:
                        day_pct = round(daily_nutrients.get(key, 0.0) / rda_val * 100, 0)
                        day_rda_css = _rda_css(day_pct, rda_type)
            rows.append({
                "label":       label,
                "value":       round(val, 3),
                "unit":        unit,
                "pct":         pct,
                "rda_type":    rda_type,
                "rda_css":     rda_css_val,
                "day_pct":     day_pct,
                "day_rda_css": day_rda_css,
            })
        if rows:
            sections.append({"name": group_name, "rows": rows})
    return sections


def _load_rda() -> dict | None:
    """Load the user profile and return computed RDA dict, or None if no profile set."""
    profile = _profile.load_profile()
    if profile is None:
        return None
    return _profile.compute_rda(profile)


def _protein_section(food_name: str, nutrients: dict) -> dict | None:
    if nutrients.get("protein_g", 0) <= 0:
        return None
    if not _usda.has_amino_acid_data(nutrients):
        return None
    diaas = _usda.get_diaas(food_name)
    digestibility = diaas if diaas is not None else 1.0
    pc = _usda.protein_completeness(nutrients, digestibility)
    if not pc["has_data"]:
        return None
    limiting_label = _usda.nutrient_label(pc["limiting_aa"])[0] if pc["limiting_aa"] else None
    aa_rows = [
        {
            "label": _usda.nutrient_label(k)[0],
            "score": round(v, 3),
            "met": v >= 1.0,
        }
        for k, v in sorted(pc["scores"].items(), key=lambda x: x[1])
    ]
    return {
        "diaas":         diaas,
        "complete":      pc["complete"],
        "limiting_aa":   limiting_label,
        "aa_rows":       aa_rows,
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "home.html", {"home_body": _HOME_BODY})


async def _search_logic(request: Request, query: str, template: str, extra_ctx: dict | None = None):
    """Shared search logic for food search and analyze-portion pages."""
    query = query.strip()
    results = []
    error = None

    if query:
        ql = query.lower()
        query_words = ql.split()
        with _db.get_db() as conn:
            all_recipes = _db.recipe_list(conn)
            cached = _db.search_cached_foods(conn, query)
        matching_recipes = sorted(
            [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)],
            key=lambda r: (-sum(1 for w in query_words if w in r["name"].lower()), r["name"].lower()),
        )
        for r in matching_recipes:
            results.append({
                "_type":     "recipe",
                "recipe_id": r["id"],
                "name":      r["name"],
                "data_type": "Recipe",
                "brand":     "",
                "source":    "local",
            })
        seen_ids: set[int] = set()
        for row in cached:
            seen_ids.add(row["fdc_id"])
            results.append({
                "fdc_id":    row["fdc_id"],
                "name":      row["name"],
                "data_type": row["data_type"],
                "brand":     row["brand"] or "",
                "source":    "cache",
            })
        try:
            for food in _usda.search_foods(query):
                fid = food.get("fdcId")
                if fid and fid not in seen_ids:
                    seen_ids.add(fid)
                    results.append({
                        "fdc_id":    fid,
                        "name":      food.get("description", ""),
                        "data_type": food.get("dataType", ""),
                        "brand":     food.get("brandOwner") or food.get("brandName") or "",
                        "source":    "usda",
                    })
        except Exception as exc:
            if not results:
                error = f"USDA API unavailable: {exc}"

    ctx = {"results": results, "query": query, "error": error}
    if extra_ctx:
        ctx.update(extra_ctx)
    return templates.TemplateResponse(request, template, ctx)


@app.get("/food/search", response_class=HTMLResponse)
async def food_search_get(request: Request):
    return templates.TemplateResponse(request, "search.html", {"results": [], "query": ""})


@app.post("/food/search", response_class=HTMLResponse)
async def food_search_post(request: Request, query: str = Form("")):
    return await _search_logic(request, query, "search.html")


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form("")):
    """Legacy alias — same as POST /food/search."""
    return await _search_logic(request, query, "search.html")


# ---------------------------------------------------------------------------
# Food sub-pages: analyze portion, analyze recipe portion, convert, compare,
#                 cache, pantry, custom profiles, annotate
# NOTE: /food/{fdc_id} is registered AFTER all literal /food/* paths so that
#       Starlette matches specific paths first (first-match routing).
# ---------------------------------------------------------------------------

@app.get("/food/analyze-portion", response_class=HTMLResponse)
async def food_analyze_portion_get(request: Request):
    return templates.TemplateResponse(request, "food_analyze_portion.html",
                                      {"results": [], "query": ""})


@app.post("/food/analyze-portion", response_class=HTMLResponse)
async def food_analyze_portion_post(request: Request, query: str = Form("")):
    return await _search_logic(request, query, "food_analyze_portion.html")


@app.get("/food/analyze-recipe-portion", response_class=HTMLResponse)
async def food_analyze_recipe_portion_get(request: Request):
    with _db.get_db() as conn:
        recipes = [dict(r) for r in _db.recipe_list(conn)]
    return templates.TemplateResponse(request, "food_analyze_recipe_portion.html", {
        "recipes": recipes,
    })


@app.post("/food/analyze-recipe-portion", response_class=HTMLResponse)
async def food_analyze_recipe_portion_post(
    request: Request,
    recipe_id: int = Form(...),
    servings: float = Form(1.0),
):
    with _db.get_db() as conn:
        recipes = [dict(r) for r in _db.recipe_list(conn)]
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return templates.TemplateResponse(request, "food_analyze_recipe_portion.html", {
                "recipes": recipes,
                "error": f"Recipe {recipe_id} not found.",
            })
        per_serving = _recipe_nutrients_per_serving(recipe_id, conn)
        recipe_servings = float(recipe["servings"] or 1)

        all_ings = _db.recipe_get_ingredients(conn, recipe_id)
        display_ingredients = []
        diaas_ingredients = []
        for ing in all_ings:
            if ing["ref_recipe_id"]:
                n = ing["amount"]
                amt_str = f"{n:g} serving{'s' if n != 1 else ''}"
            else:
                amt_str = ing["unit"] or f"{ing['amount']:g} g"
            display_ingredients.append({
                "food_name":  ing["food_name"],
                "amount_str": amt_str,
                "notes":      ing["notes"] or "",
            })
            if not ing["fdc_id"]:
                continue
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                continue
            diaas_ingredients.append({
                "food_name":      ing["food_name"],
                "nutrients_100g": json.loads(cached["nutrients_json"]),
                "grams":          float(ing["amount"]) / recipe_servings * servings,
                "fdc_id":         ing["fdc_id"],
            })

        diaas_result = None
        if diaas_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(diaas_ingredients, conn)
            except Exception:
                pass

    factor = servings  # per_serving already divides by recipe_servings
    scaled = {k: v * factor for k, v in per_serving.items()}
    rda = _load_rda()
    diaas_display = _build_diaas_display(diaas_result)

    return templates.TemplateResponse(request, "food_analyze_recipe_portion.html", {
        "recipes":            recipes,
        "selected_recipe":    dict(recipe),
        "servings_input":     servings,
        "analysis": {
            "recipe_name":       recipe["name"],
            "servings_analyzed": servings,
        },
        "ingredients":        display_ingredients,
        "nutrient_sections":  _nutrient_sections(scaled, rda),
        "diaas_display":      diaas_display,
        "has_profile":        rda is not None,
        "protein_adequacy":   _protein_adequacy(scaled, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":        _complement_suggestions(scaled, diaas_display["score"] if diaas_display else None),
        "gl":                 _recipe_gl_web(recipe_id, recipe_servings, servings),
    })


@app.get("/food/convert", response_class=HTMLResponse)
async def food_convert_get(request: Request, q: str = ""):
    search_results = []
    search_error = None
    if q:
        q = q.strip()
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, q)
        seen: set[int] = set()
        for row in cached:
            seen.add(row["fdc_id"])
            search_results.append({
                "fdc_id":    row["fdc_id"],
                "name":      row["name"],
                "data_type": row["data_type"],
                "brand":     row["brand"] or "",
                "source":    "cache",
            })
        try:
            for food in _usda.search_foods(q):
                fid = food.get("fdcId")
                if fid and fid not in seen:
                    seen.add(fid)
                    search_results.append({
                        "fdc_id":    fid,
                        "name":      food.get("description", ""),
                        "data_type": food.get("dataType", ""),
                        "brand":     food.get("brandOwner") or food.get("brandName") or "",
                        "source":    "usda",
                    })
        except Exception as exc:
            if not search_results:
                search_error = f"USDA API unavailable: {exc}"
    return templates.TemplateResponse(request, "food_convert.html", {
        "query":          q,
        "search_results": search_results,
        "search_error":   search_error,
    })


@app.get("/food/convert/{fdc_id}", response_class=HTMLResponse)
async def food_convert_detail(
    request: Request,
    fdc_id: int,
    amount: float = Query(default=None),
):
    food_data: dict = {}
    portions: list = []
    nutrients: dict = {}

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)

    if cached:
        nutrients = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
        portions = json.loads(cached["portions_json"]) if cached["portions_json"] else []
        food_data = {"fdc_id": cached["fdc_id"], "name": cached["name"], "brand": cached["brand"] or ""}
    else:
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception as exc:
            return templates.TemplateResponse(request, "food_convert.html", {
                "search_error": f"Could not load food {fdc_id}: {exc}",
            })
        nutrients = detail.get("nutrients", {})
        portions = detail.get("portions", [])
        food_data = {"fdc_id": fdc_id, "name": detail["name"], "brand": detail.get("brand") or ""}
        with _db.get_db() as conn:
            _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                           data_type=detail.get("dataType", ""), brand=detail.get("brand"),
                           serving_size=detail.get("servingSize"),
                           serving_unit=detail.get("servingUnit"),
                           nutrients=nutrients, portions=portions)

    density = _usda.get_density_g_per_ml(food_data["name"], portions)

    closest_portion = None
    if amount and portions:
        best = min(portions, key=lambda p: abs(float(p.get("gram_weight", 0)) - amount))
        closest_portion = best

    return templates.TemplateResponse(request, "food_convert.html", {
        "food":            food_data,
        "portions":        portions,
        "density":         density,
        "amount":          amount,
        "closest_portion": closest_portion,
    })


# ---------------------------------------------------------------------------
# Compare helpers
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
    ("Amino Acids", [
        "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
        "aa_lysine_g", "aa_methionine_g", "aa_phenylalanine_g",
        "aa_valine_g", "aa_histidine_g",
    ]),
]


def _build_compare_groups(entries: list[dict]) -> list[dict]:
    """Build comparison group rows from a list of {name, amount, nutrients} dicts."""
    groups = []
    for group_name, keys in _COMPARE_GROUPS:
        rows = []
        for key in keys:
            label, unit = _usda.nutrient_label(key)
            values = [round(e["nutrients"].get(key) or 0, 3) for e in entries]
            max_val = max(values) if any(v > 0 for v in values) else None
            cells = [
                {"value": v if v > 0 else None, "is_max": (max_val is not None and v == max_val and v > 0)}
                for v in values
            ]
            if any(c["value"] is not None for c in cells):
                rows.append({"label": label, "unit": unit, "cells": cells})
        if rows:
            groups.append({"name": group_name, "rows": rows})
    return groups


def _load_compare_entries(ids: list[int], amounts: list[float]) -> list[dict]:
    """Load food data for comparison, scaling nutrients to given gram amounts."""
    entries = []
    for fdc_id, amount in zip(ids, amounts):
        nutrients: dict = {}
        name = str(fdc_id)
        data_type = ""
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if cached:
            nutrients_100g = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
            name = cached["name"]
            data_type = cached["data_type"] or ""
        else:
            try:
                detail = _usda.get_food_detail(fdc_id)
                nutrients_100g = detail.get("nutrients", {})
                name = detail["name"]
                data_type = detail.get("dataType", "")
                with _db.get_db() as conn:
                    _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                                   data_type=detail.get("dataType", ""),
                                   brand=detail.get("brand"),
                                   serving_size=detail.get("servingSize"),
                                   serving_unit=detail.get("servingUnit"),
                                   nutrients=nutrients_100g,
                                   portions=detail.get("portions", []))
            except Exception:
                nutrients_100g = {}
        nutrients = _usda.scale_nutrients(nutrients_100g, amount) if amount != 100.0 else nutrients_100g
        entries.append({
            "fdc_id":    fdc_id,
            "name":      name,
            "data_type": data_type,
            "amount":    amount,
            "nutrients": nutrients,
        })
    return entries


def _parse_ids_amounts(ids_str: str, amounts_str: str) -> tuple[list[int], list[float]]:
    ids = [int(x) for x in ids_str.split(",") if x.strip()] if ids_str.strip() else []
    raw_amounts = [x.strip() for x in amounts_str.split(",") if x.strip()] if amounts_str.strip() else []
    amounts = []
    for i, fid in enumerate(ids):
        try:
            amounts.append(float(raw_amounts[i]) if i < len(raw_amounts) else 100.0)
        except (ValueError, IndexError):
            amounts.append(100.0)
    return ids, amounts


@app.get("/food/compare", response_class=HTMLResponse)
async def food_compare_get(
    request: Request,
    ids: str = "",
    amounts: str = "",
    error: str = "",
    search: str = "",
):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    entries = _load_compare_entries(id_list, amount_list) if id_list else []
    compare_groups = _build_compare_groups(entries) if len(entries) >= 2 else []
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)

    search_results: list[dict] = []
    search_error: str | None = None
    search = search.strip()
    if search:
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, search)
        seen: set[int] = set(id_list)  # exclude already-added foods
        for row in cached:
            if row["fdc_id"] not in seen:
                seen.add(row["fdc_id"])
                search_results.append({
                    "fdc_id":    row["fdc_id"],
                    "name":      row["name"],
                    "data_type": row["data_type"],
                    "brand":     row["brand"] or "",
                    "source":    "cache",
                })
        try:
            for food in _usda.search_foods(search):
                fid = food.get("fdcId")
                if fid and fid not in seen:
                    seen.add(fid)
                    search_results.append({
                        "fdc_id":    fid,
                        "name":      food.get("description", ""),
                        "data_type": food.get("dataType", ""),
                        "brand":     food.get("brandOwner") or food.get("brandName") or "",
                        "source":    "usda",
                    })
        except Exception as exc:
            if not search_results:
                search_error = f"USDA API unavailable: {exc}"

    with _db.get_db() as conn:
        saved_lists = _db.saved_comparison_list(conn)

    return templates.TemplateResponse(request, "food_compare.html", {
        "entries":        entries,
        "compare_groups": compare_groups,
        "ids_str":        ids_str,
        "amounts_str":    amounts_str,
        "error":          error,
        "search":         search,
        "search_results": search_results,
        "search_error":   search_error,
        "saved_lists":    saved_lists,
    })


@app.post("/food/compare/add", response_class=RedirectResponse)
async def food_compare_add(
    fdc_id: int = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)
    if len(id_list) >= 6:
        return RedirectResponse(
            f"/food/compare?ids={ids_str}&amounts={amounts_str}&error=Maximum+6+foods+allowed",
            status_code=303,
        )
    if fdc_id not in id_list:
        id_list.append(fdc_id)
        amount_list.append(100.0)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)
    return RedirectResponse(
        f"/food/compare?ids={ids_str}&amounts={amounts_str}",
        status_code=303,
    )


@app.post("/food/compare/remove", response_class=RedirectResponse)
async def food_compare_remove(
    remove_id: int = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    paired = [(i, a) for i, a in zip(id_list, amount_list) if i != remove_id]
    new_ids = [str(p[0]) for p in paired]
    new_amounts = [str(p[1]) for p in paired]
    return RedirectResponse(
        f"/food/compare?ids={','.join(new_ids)}&amounts={','.join(new_amounts)}",
        status_code=303,
    )


@app.post("/food/compare/amounts", response_class=RedirectResponse)
async def food_compare_amounts(request: Request, ids: str = Form("")):
    form = await request.form()
    id_list = [int(x) for x in ids.split(",") if x.strip()] if ids.strip() else []
    new_amounts = []
    for fid in id_list:
        try:
            val = float(form.get(f"amounts_{fid}", 100.0))
            new_amounts.append(max(1.0, val))
        except (ValueError, TypeError):
            new_amounts.append(100.0)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in new_amounts)
    return RedirectResponse(f"/food/compare?ids={ids_str}&amounts={amounts_str}", status_code=303)


@app.post("/food/compare/save", response_class=RedirectResponse)
async def food_compare_save(
    name: str = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    id_list, amount_list = _parse_ids_amounts(ids, amounts)
    if len(id_list) >= 2:
        with _db.get_db() as conn:
            _db.saved_comparison_save(conn, name.strip() or "Untitled", id_list, amount_list)
    ids_str = ",".join(str(i) for i in id_list)
    amounts_str = ",".join(str(a) for a in amount_list)
    return RedirectResponse(f"/food/compare?ids={ids_str}&amounts={amounts_str}", status_code=303)


@app.get("/food/compare/load/{cmp_id}", response_class=RedirectResponse)
async def food_compare_load(cmp_id: int):
    with _db.get_db() as conn:
        row = _db.saved_comparison_get(conn, cmp_id)
    if not row:
        return RedirectResponse("/food/compare", status_code=303)
    ids_str = ",".join(str(i) for i in json.loads(row["fdc_ids"]))
    amounts_str = ",".join(str(a) for a in json.loads(row["amounts"]))
    return RedirectResponse(f"/food/compare?ids={ids_str}&amounts={amounts_str}", status_code=303)


@app.post("/food/compare/saved/delete", response_class=RedirectResponse)
async def food_compare_saved_delete(
    cmp_id: int = Form(...),
    ids: str = Form(""),
    amounts: str = Form(""),
):
    with _db.get_db() as conn:
        _db.saved_comparison_delete(conn, cmp_id)
    ids_str = ids.strip()
    amounts_str = amounts.strip()
    url = f"/food/compare?ids={ids_str}&amounts={amounts_str}" if ids_str else "/food/compare"
    return RedirectResponse(url, status_code=303)


@app.get("/food/cache", response_class=HTMLResponse)
async def food_cache_get(request: Request, q: str = ""):
    with _db.get_db() as conn:
        if q.strip():
            rows = _db.search_cached_foods(conn, q.strip())
        else:
            rows = _db.list_cached_foods(conn)
        fdc_ids = [r["fdc_id"] for r in rows]
        annotations = _db.annotations_for_fdcids(conn, fdc_ids) if fdc_ids else {}

    foods = []
    for row in rows:
        ann = annotations.get(row["fdc_id"])
        nuts = json.loads(row["nutrients_json"]) if row["nutrients_json"] else {}
        foods.append({
            "fdc_id":    row["fdc_id"],
            "name":      row["name"],
            "data_type": row["data_type"] or "",
            "brand":     row["brand"] or "",
            "has_aa":    _usda.has_amino_acid_data(nuts),
            "gi":        ann["gi_estimate"] if ann else None,
            "diaas":     ann["diaas_estimate"] if ann else None,
            "notes":     row["notes"] or "",
        })
    return templates.TemplateResponse(request, "food_cache.html", {
        "foods": foods,
        "q":     q,
    })


@app.post("/food/cache/delete", response_class=RedirectResponse)
async def food_cache_delete(fdc_id: int = Form(...)):
    with _db.get_db() as conn:
        _db.delete_cached_food(conn, fdc_id)
    return RedirectResponse("/food/cache", status_code=303)


@app.get("/pantry", response_class=HTMLResponse)
async def pantry_get(request: Request):
    with _db.get_db() as conn:
        items = [dict(r) for r in _db.pantry_list(conn)]
    return templates.TemplateResponse(request, "pantry.html", {"items": items})


@app.post("/pantry/add", response_class=RedirectResponse)
async def pantry_add(
    food_name: str = Form(...),
    notes: str = Form(""),
):
    food_name = food_name.strip()
    notes = notes.strip() or None
    if food_name:
        with _db.get_db() as conn:
            _db.pantry_add(conn, food_name, notes=notes)
    return RedirectResponse("/pantry", status_code=303)


@app.post("/pantry/remove/{pantry_id}", response_class=RedirectResponse)
async def pantry_remove(pantry_id: int):
    with _db.get_db() as conn:
        _db.pantry_remove(conn, pantry_id)
    return RedirectResponse("/pantry", status_code=303)


@app.get("/food/custom-profiles", response_class=HTMLResponse)
async def food_custom_profiles_get(request: Request):
    with _db.get_db() as conn:
        rows = _db.list_user_drafted_foods(conn)
    foods = [dict(r) for r in rows]
    return templates.TemplateResponse(request, "food_custom_profiles.html", {"foods": foods})


@app.post("/food/custom-profiles/create", response_class=RedirectResponse)
async def food_custom_profiles_create(name: str = Form(...)):
    name = name.strip()
    if not name:
        return RedirectResponse("/food/custom-profiles", status_code=303)
    with _db.get_db() as conn:
        fdc_id = _db.next_user_drafted_fdc_id(conn)
        _db.cache_food(
            conn,
            fdc_id=fdc_id,
            name=name,
            data_type="User Drafted",
            brand=None,
            serving_size=None,
            serving_unit=None,
            nutrients={},
            portions=[],
            user_drafted=True,
        )
    return RedirectResponse(f"/food/{fdc_id}", status_code=303)


@app.post("/food/custom-profiles/delete/{fdc_id}", response_class=RedirectResponse)
async def food_custom_profiles_delete(fdc_id: int):
    with _db.get_db() as conn:
        _db.delete_cached_food(conn, fdc_id)
    return RedirectResponse("/food/custom-profiles", status_code=303)


@app.get("/food/annotate", response_class=HTMLResponse)
async def food_annotate_list(request: Request, q: str = ""):
    with _db.get_db() as conn:
        if q.strip():
            rows = _db.search_cached_foods(conn, q.strip())
        else:
            rows = _db.list_cached_foods(conn)
        fdc_ids = [r["fdc_id"] for r in rows]
        annotations = _db.annotations_for_fdcids(conn, fdc_ids) if fdc_ids else {}

    foods = []
    for row in rows:
        ann = annotations.get(row["fdc_id"])
        foods.append({
            "fdc_id":    row["fdc_id"],
            "name":      row["name"],
            "data_type": row["data_type"] or "",
            "gi":        ann["gi_estimate"] if ann else None,
            "diaas":     ann["diaas_estimate"] if ann else None,
        })
    return templates.TemplateResponse(request, "food_annotate.html", {
        "editing": False,
        "foods":   foods,
        "q":       q,
    })


@app.get("/food/annotate/{fdc_id}", response_class=HTMLResponse)
async def food_annotate_edit_get(request: Request, fdc_id: int, saved: str = ""):
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
        ann = _db.get_food_annotation(conn, fdc_id)
    food_name = cached["name"] if cached else f"Food {fdc_id}"
    return templates.TemplateResponse(request, "food_annotate.html", {
        "editing":   True,
        "fdc_id":    fdc_id,
        "food_name": food_name,
        "annotation": dict(ann) if ann else None,
        "saved":     bool(saved),
    })


@app.post("/food/annotate/{fdc_id}", response_class=RedirectResponse)
async def food_annotate_edit_post(
    fdc_id: int,
    gi_estimate:    str = Form(""),
    diaas_estimate: str = Form(""),
    prep_context:   str = Form(""),
    gi_no_prompt:   str = Form(""),
    diaas_no_prompt: str = Form(""),
):
    gi   = float(gi_estimate)   if gi_estimate.strip()   else None
    dias = float(diaas_estimate) if diaas_estimate.strip() else None
    prep = prep_context.strip() or None
    with _db.get_db() as conn:
        _db.upsert_food_annotation(
            conn, fdc_id,
            gi_estimate=gi,
            gi_no_prompt=bool(gi_no_prompt),
            diaas_estimate=dias,
            diaas_no_prompt=bool(diaas_no_prompt),
            prep_context=prep,
        )
    return RedirectResponse(f"/food/annotate/{fdc_id}?saved=1", status_code=303)


# /food/{fdc_id} must be registered LAST among /food/* routes so literal paths win.
@app.get("/food/{fdc_id}", response_class=HTMLResponse)
async def food_detail(
    request: Request,
    fdc_id: int,
    amount: float = Query(default=100.0, gt=0),
):
    nutrients: dict = {}
    portions: list = []
    food: dict = {}

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)

    if cached:
        nutrients = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
        portions = json.loads(cached["portions_json"]) if cached["portions_json"] else []
        food = {
            "fdc_id":       cached["fdc_id"],
            "name":         cached["name"],
            "data_type":    cached["data_type"],
            "brand":        cached["brand"] or "",
            "serving_size": cached["serving_size"],
            "serving_unit": cached["serving_unit"] or "",
        }
    else:
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception as exc:
            return templates.TemplateResponse(request, "search.html", {
                "results": [],
                "query":   "",
                "error":   f"Could not load food {fdc_id}: {exc}",
            })
        nutrients = detail.get("nutrients", {})
        portions = detail.get("portions", [])
        food = {
            "fdc_id":       detail["fdcId"],
            "name":         detail["name"],
            "data_type":    detail.get("dataType", ""),
            "brand":        detail.get("brand") or "",
            "serving_size": detail.get("servingSize"),
            "serving_unit": detail.get("servingUnit") or "",
        }
        with _db.get_db() as conn:
            _db.cache_food(
                conn,
                fdc_id=detail["fdcId"],
                name=detail["name"],
                data_type=detail.get("dataType", ""),
                brand=detail.get("brand"),
                serving_size=detail.get("servingSize"),
                serving_unit=detail.get("servingUnit"),
                nutrients=nutrients,
                portions=portions,
            )

    # Scale nutrient display values; protein analysis uses per-100g ratios so stays unscaled
    display_nutrients = _usda.scale_nutrients(nutrients, amount) if amount != 100.0 else nutrients
    rda = _load_rda()
    # For RDA % on food detail, scale the RDA targets by the same portion factor
    rda_scaled: dict | None = None
    if rda and amount != 100.0:
        rda_scaled = {k: (v * (amount / 100.0), u, t) for k, (v, u, t) in rda.items()}
    antinutrient_flags = _usda.get_antinutrient_flags(food["name"])

    return templates.TemplateResponse(request, "food_detail.html", {
        "food":               food,
        "amount":             amount,
        "portions":           portions,
        "nutrient_sections":  _nutrient_sections(display_nutrients, rda_scaled or rda),
        "protein":            _protein_section(food["name"], nutrients),
        "antinutrients":      antinutrient_flags,
        "has_profile":        rda is not None,
    })


# ---------------------------------------------------------------------------
# Meal helpers
# ---------------------------------------------------------------------------

def _recipe_nutrients_per_serving(recipe_id: int, conn) -> dict:
    """Sum ingredient nutrients for one recipe, return per-serving totals. Handles nested recipes."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return {}
    servings = float(recipe["servings"] or 1)
    total: dict = {}
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_id"]:
            # Sub-recipe: get its per-serving nutrients and scale by servings consumed
            sub_per_serving = _recipe_nutrients_per_serving(ing["ref_recipe_id"], conn)
            amount = float(ing["amount"])
            for k, v in sub_per_serving.items():
                total[k] = total.get(k, 0.0) + v * amount
        elif ing["fdc_id"]:
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                continue
            nuts_100g = json.loads(cached["nutrients_json"])
            scaled = _usda.scale_nutrients(nuts_100g, float(ing["amount"]))
            for k, v in scaled.items():
                total[k] = total.get(k, 0.0) + v
    return {k: v / servings for k, v in total.items()} if servings else total


def _build_diaas_display(diaas_result: dict | None) -> dict | None:
    """Build the full diaas_display dict from a meal_level_diaas result."""
    if not diaas_result or not diaas_result.get("diaas"):
        return None
    score = diaas_result["diaas"]
    total_p = diaas_result.get("total_protein_g", 0)
    if total_p <= 0:
        return None
    limiting_iaa_key = diaas_result.get("limiting_iaa")
    def _iaa_row(k, v):
        bar_pct = min(round(v / 1.5 * 100, 0), 100)
        is_lim = k == limiting_iaa_key
        if is_lim:
            color = "#ca8a04"   # deep yellow — limiting AA
        elif v >= 1.0:
            color = "#166534"   # dark green — met
        elif v >= 0.80:
            color = "#7f1d1d"   # deep dark red — near miss
        else:
            color = "#dc2626"   # medium red — gap
        return {"label": _usda.nutrient_label(k)[0], "ratio": round(v, 3),
                "met": v >= 1.0, "bar_pct": bar_pct, "bar_color": color,
                "is_limiting": is_lim}
    iaa_rows = sorted(
        [_iaa_row(k, v) for k, v in diaas_result.get("iaa_ratios", {}).items()],
        key=lambda r: r["label"],
    )
    ing_rows = []
    for ing in diaas_result.get("ingredients", []):
        d = ing.get("digestibility", 1.0)
        p = ing.get("protein_g", 0.0)
        dig_p = p * d if ing.get("has_aa_data") else p
        src = ing.get("dig_source", "")
        src_tag = "user" if "user override" in src else ("~est" if "estimate" in src else "")
        ing_rows.append({
            "food_name":            ing.get("food_name", ""),
            "fdc_id":               ing.get("fdc_id"),
            "protein_g":            round(p, 1),
            "digestibility":        round(d, 2),
            "digestible_protein_g": round(dig_p, 1),
            "has_aa":               ing.get("has_aa_data", False),
            "src_tag":              src_tag,
        })
    aa_p = diaas_result.get("aa_protein_g") or total_p
    dcp_g = round(diaas_result.get("digestible_complete_protein_g") or 0, 1)
    eff_pct = round(min(score, 1.0) * 100, 0)
    return {
        "score":           round(score, 3),
        "total_protein_g": round(total_p, 1),
        "aa_protein_g":    round(aa_p, 1),
        "dcp_g":           dcp_g,
        "eff_pct":         eff_pct,
        "limiting_label":  diaas_result.get("limiting_label"),
        "iaa_rows":        iaa_rows,
        "ing_rows":        ing_rows,
        "missing":         diaas_result.get("missing_aa_names", []),
        "has_complete":    diaas_result.get("has_complete_data", False),
        "phe_tyr_gap":     diaas_result.get("phe_tyr_gap", False),
    }


_REFERENCE_ADULT_PROTEIN_G = 56.0  # 0.8 g/kg × 70 kg WHO/FAO reference adult

def _protein_adequacy(nutrients: dict, diaas_dcp_g: float | None, rda: dict | None) -> dict:
    """Build protein adequacy dict. Uses DCP when available, else raw protein.
    Falls back to standard adult reference (56 g) when no profile is set."""
    if rda and rda.get("protein_g") and rda["protein_g"][0] > 0:
        target = rda["protein_g"][0]
        personal = True
    else:
        target = _REFERENCE_ADULT_PROTEIN_G
        personal = False
    intake = diaas_dcp_g if diaas_dcp_g else nutrients.get("protein_g", 0.0)
    pct = intake / target * 100.0
    return {"target": round(target, 1), "intake": round(intake, 1),
            "pct": round(pct, 0), "personal": personal}


def _web_pantry_candidates() -> list[dict]:
    """Load pantry items as complement-suggestion candidates."""
    try:
        with _db.get_db() as conn:
            rows = _db.pantry_list(conn)
        candidates = []
        for row in rows:
            nutrients = None
            if row["fdc_id"] is not None:
                with _db.get_db() as conn:
                    cached = _db.get_cached_food(conn, row["fdc_id"])
                if cached and cached["nutrients_json"]:
                    nutrients = json.loads(cached["nutrients_json"])
            candidates.append({
                "name":      row["food_name"] or "",
                "nutrients": nutrients,
                "diaas":     _usda.get_diaas(row["food_name"] or ""),
            })
        return candidates
    except Exception:
        return []


_AA_LOW_IN: dict[str, str] = {
    "aa_methionine_g":    "grains (rice, wheat, quinoa) and most legumes",
    "aa_lysine_g":        "grains (rice, wheat, corn, oats)",
    "aa_threonine_g":     "wheat and refined grains",
    "aa_leucine_g":       "most plant foods other than soy",
    "aa_isoleucine_g":    "legumes and most plant foods",
    "aa_valine_g":        "most plant foods",
    "aa_tryptophan_g":    "untreated corn-based foods",
    "aa_histidine_g":     "most plant foods",
    "aa_phenylalanine_g": "most plant foods",
}

def _complement_suggestions(aa_nutrients: dict, diaas_score: float | None) -> dict:
    """Build complement suggestion data. Returns no_data sentinel if AA data unavailable."""
    if not aa_nutrients or aa_nutrients.get("protein_g", 0) <= 0:
        return {"no_data": True}
    # Use digestibility=1.0 for gap analysis, matching CLI meal context behaviour.
    # The meal DIAAS is a pooled value and must not be re-applied as a per-food multiplier.
    try:
        gaps = _usda.get_aa_gaps(aa_nutrients, digestibility=1.0)
    except Exception:
        return {"no_data": True}
    if not gaps:
        return {"no_gaps": True}
    prefs = _load_prefs_file()
    diet_pref = prefs.get("diet_pref", "all")
    pantry = _web_pantry_candidates()
    try:
        suggestions = _usda.suggest_complements(
            aa_nutrients, pantry, diet_pref=diet_pref,
            base_digestibility=1.0,
        )
    except Exception:
        return {"no_data": True}

    base_protein = aa_nutrients.get("protein_g", 0.0)
    base_digestible = base_protein  # digestibility=1.0 for meal context

    def _aa_effects(s: dict) -> list[dict]:
        effects = []
        for aa, orig_score, _ in gaps[:3]:
            new_raw = s.get("new_scores", {}).get(aa)
            new_score = new_raw if new_raw is not None else orig_score
            effects.append({
                "label":  _usda.nutrient_label(aa)[0],
                "before": round(orig_score, 2),
                "after":  round(new_score, 2),
                "met":    new_score >= 1.0,
            })
        return effects

    def _total_dig(s: dict) -> float:
        raw = float(s.get("protein_added") or 0)
        dig = float(s.get("digestible_protein_added") or 0)
        new_scores = s.get("new_scores", {})
        if new_scores and gaps:
            old_raw_min = gaps[0][1]  # already at digestibility=1.0
            new_raw_min = min(new_scores.values())
            scale = (new_raw_min / old_raw_min) if old_raw_min > 0 else 1.0
            return round((base_protein + raw) * min(1.0, scale), 1)
        return round(base_digestible + dig, 1)

    def _fmt(s: dict) -> dict:
        raw = float(s.get("protein_added") or 0)
        dig = float(s.get("digestible_protein_added") or 0)
        return {
            "name":              s.get("name", ""),
            "grams":             s.get("grams"),
            "fdc_id":            s.get("fdc_id"),
            "diaas":             round(s["diaas"], 2) if s.get("diaas") else None,
            "new_complete":      s.get("new_complete", False),
            "dig_protein_added": round(dig, 1),
            "protein_added":     round(raw, 1),
            "opens_new_gap":     s.get("opens_new_gap", False),
            "aa_effects":        _aa_effects(s),
            "total_dig":         _total_dig(s),
        }

    def _fmt_improver(s: dict) -> dict:
        raw = float(s.get("protein_added") or 0)
        dig = float(s.get("digestible_protein_added") or 0)
        new_diaas = s.get("new_diaas") or 0.0
        total_dig = round((base_protein + raw) * min(1.0, new_diaas), 1) if new_diaas else round(base_digestible + dig, 1)
        return {
            "name":              s.get("name", ""),
            "grams":             s.get("grams"),
            "fdc_id":            s.get("fdc_id"),
            "diaas":             round(s["diaas"], 2) if s.get("diaas") else None,
            "current_diaas":     s.get("current_diaas"),
            "new_diaas":         s.get("new_diaas"),
            "dig_protein_added": round(dig, 1),
            "protein_added":     round(raw, 1),
            "total_dig":         total_dig,
        }

    sort_key = lambda s: (0 if s.get("new_complete") else 1, float(s.get("grams") or 999))
    pantry_suggs    = sorted(suggestions.get("pantry",          []), key=sort_key)[:3]
    general_suggs   = sorted(suggestions.get("general",         []), key=sort_key)[:6]
    diaas_improvers = suggestions.get("diaas_improvers", [])[:5]

    gap_rows = [{"label": _usda.nutrient_label(k)[0], "score": round(v, 3)} for k, v, _ in gaps[:4]]
    limiting_aa = gaps[0][0] if gaps else None
    limiting_label = _usda.nutrient_label(limiting_aa)[0] if limiting_aa else "this amino acid"
    low_in = _AA_LOW_IN.get(limiting_aa or "", "many plant foods")
    n_shown = len(pantry_suggs) + len(general_suggs)
    exhausted_prefix = "All options that qualify are shown above — no others meet the criteria." \
        if n_shown > 0 else "No qualifying options found in the database."

    return {
        "no_gaps":           False,
        "gaps":              gap_rows,
        "ranking_note":      "Ranked by the smallest practical amount needed to close the main amino acid gap.",
        "pantry_empty":      not pantry,
        "pantry_no_qualify": bool(pantry) and not pantry_suggs,
        "pantry":            [_fmt(s) for s in pantry_suggs],
        "general":           [_fmt(s) for s in general_suggs],
        "diaas_improvers":   [_fmt_improver(s) for s in diaas_improvers],
        "have_gap_closers":  bool(pantry_suggs or general_suggs),
        "exhausted_msg":     (
            f"{exhausted_prefix} A qualifying complement must have a {limiting_label}/protein ratio "
            f"above the FAO reference to close the gap to score 1.0 in a practical serving (≤ 500 g). "
            f"Score 1.0 = meets human requirements (the floor, not an aspirational target). "
            f"Foods that don't qualify for a {limiting_label} gap: {low_in}. "
            f"Their ratio falls below the reference — adding them dilutes the score further."
        ),
    }


def _recipe_gl_web(recipe_id: int, recipe_servings: float, servings: float) -> dict:
    """Glycemic load for a recipe portion. Returns {"total": float_or_None, "blockers": list}."""
    with _db.get_db() as conn:
        ingredients = _db.recipe_get_ingredients(conn, recipe_id)
        food_ids = [i["fdc_id"] for i in ingredients if i["fdc_id"] and not i["ref_recipe_id"]]
        ann_map = _db.annotations_for_fdcids(conn, food_ids) if food_ids else {}
        blockers: list[str] = []
        gl_total = 0.0
        for ing in ingredients:
            if ing["ref_recipe_id"]:
                blockers.append(f"{ing['food_name']} (sub-recipe)")
                continue
            ann = ann_map.get(ing["fdc_id"])
            if ann is None or ann["gi_estimate"] is None:
                blockers.append(ing["food_name"])
                continue
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                blockers.append(ing["food_name"])
                continue
            carbs_g = (json.loads(cached["nutrients_json"]).get("carbs_g", 0.0)
                       * float(ing["amount"]) / 100.0)
            gl_total += ann["gi_estimate"] * carbs_g / 100.0
    if blockers:
        return {"total": None, "blockers": blockers}
    gl_portion = round(gl_total / recipe_servings * servings, 1) if recipe_servings > 0 else round(gl_total, 1)
    return {"total": gl_portion, "blockers": []}


def _compute_gl(meal_id: int) -> tuple[float | None, list[str]]:
    """Glycemic load for a single meal. Returns (gl_total_or_None, blocker_names)."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
        food_ids = [it["fdc_id"] for it in items if it["item_type"] == "food" and it["fdc_id"]]
        ann_map = _db.annotations_for_fdcids(conn, food_ids) if food_ids else {}
        blockers: list[str] = []
        gl_total = 0.0
        for item in items:
            if item["item_type"] == "recipe":
                blockers.append(f"{item['food_name']} (recipe — no GL data)")
                continue
            ann = ann_map.get(item["fdc_id"])
            if ann is None or ann["gi_estimate"] is None:
                blockers.append(item["food_name"])
                continue
            cached = _db.get_cached_food(conn, item["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                blockers.append(item["food_name"])
                continue
            carbs_g = (json.loads(cached["nutrients_json"]).get("carbs_g", 0.0)
                       * float(item["amount"]) / 100.0)
            gl_total += ann["gi_estimate"] * carbs_g / 100.0
    return (None if blockers else round(gl_total, 1), blockers)


def _best_aa_nutrients(nuts: dict, food_name: str) -> dict | None:
    """Return nuts enhanced with complement-table AA data if cached AA data is missing.
    Mirrors the CLI's _best_nutrients fallback logic."""
    if _usda.has_amino_acid_data(nuts):
        return nuts
    complement = _usda.get_complement_nutrients(food_name)
    if complement and _usda.has_amino_acid_data(complement):
        actual_protein = nuts.get("protein_g", 0)
        ref_protein = complement.get("protein_g", 0)
        if ref_protein > 0 and actual_protein > 0:
            scale = actual_protein / ref_protein
            merged = dict(nuts)
            for k, v in complement.items():
                if k.startswith("aa_") and k not in merged:
                    merged[k] = v * scale
            return merged
    return None


def _meal_aa_nutrients(meal_id: int) -> dict:
    """Return summed nutrients (scaled) from foods that have AA data, for complement suggestions.
    Expands recipe items recursively and applies complement-table AA fallback, matching the CLI."""
    result: dict = {}
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
        for row in items:
            if row["item_type"] == "food" and row["fdc_id"]:
                cached = _db.get_cached_food(conn, row["fdc_id"])
                if not cached or not cached["nutrients_json"]:
                    continue
                nuts = _best_aa_nutrients(json.loads(cached["nutrients_json"]), row["food_name"])
                if nuts:
                    scaled = _usda.scale_nutrients(nuts, float(row["amount"]))
                    for k, v in scaled.items():
                        result[k] = result.get(k, 0.0) + v
            elif row["item_type"] == "recipe" and row["recipe_id"]:
                recipe = _db.recipe_get(conn, row["recipe_id"])
                if not recipe:
                    continue
                recipe_servings = float(recipe["servings"] or 1)
                portion_factor = float(row["amount"]) / recipe_servings
                for ing in _expand_recipe_ingredients(row["recipe_id"], portion_factor, conn):
                    nuts = _best_aa_nutrients(ing["nutrients_100g"], ing["food_name"])
                    if nuts:
                        scaled = _usda.scale_nutrients(nuts, ing["grams"])
                        for k, v in scaled.items():
                            result[k] = result.get(k, 0.0) + v
    return result


def _expand_recipe_ingredients(recipe_id: int, portion_factor: float, conn) -> list[dict]:
    """Recursively expand a recipe's ingredients for DIAAS, scaling by portion_factor."""
    result = []
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_id"]:
            sub = _db.recipe_get(conn, ing["ref_recipe_id"])
            sub_servings = float(sub["servings"] or 1) if sub else 1.0
            sub_factor = float(ing["amount"]) / sub_servings * portion_factor
            result.extend(_expand_recipe_ingredients(ing["ref_recipe_id"], sub_factor, conn))
        elif ing["fdc_id"]:
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                continue
            nuts_100g = json.loads(cached["nutrients_json"])
            if nuts_100g:
                result.append({
                    "food_name":      ing["food_name"],
                    "fdc_id":         ing["fdc_id"],
                    "nutrients_100g": nuts_100g,
                    "grams":          float(ing["amount"]) * portion_factor,
                })
    return result


def _meal_totals(meal_id: int) -> tuple[list, dict, dict | None]:
    """Return (items_with_nutrients, total_nutrients, diaas_result)."""
    with _db.get_db() as conn:
        raw_items = _db.meal_get_items(conn, meal_id)
        items = []
        ingredients = []
        total_nutrients: dict = {}

        for row in raw_items:
            if row["item_type"] == "food" and row["fdc_id"]:
                cached = _db.get_cached_food(conn, row["fdc_id"])
                nuts_100g = json.loads(cached["nutrients_json"]) if cached and cached["nutrients_json"] else {}
                grams = float(row["amount"])
                scaled = _usda.scale_nutrients(nuts_100g, grams)
                item_label = f"{row['food_name']} ({grams:g} g)"
                for k, v in scaled.items():
                    total_nutrients[k] = total_nutrients.get(k, 0.0) + v
                items.append({
                    "id":        row["id"],
                    "food_name": row["food_name"],
                    "fdc_id":    row["fdc_id"],
                    "recipe_id": None,
                    "amount":    grams,
                    "unit":      "g",
                    "notes":     row["notes"] or "",
                    "has_nuts":  bool(nuts_100g),
                })
                if nuts_100g:
                    ingredients.append({
                        "food_name":      row["food_name"],
                        "fdc_id":         row["fdc_id"],
                        "nutrients_100g": nuts_100g,
                        "grams":          grams,
                    })

            elif row["item_type"] == "recipe" and row["recipe_id"]:
                servings_consumed = float(row["amount"])
                recipe = _db.recipe_get(conn, row["recipe_id"])
                total_servings = float(recipe["servings"] or 1) if recipe else 1.0
                portion_factor = servings_consumed / total_servings
                per_serving = _recipe_nutrients_per_serving(row["recipe_id"], conn)
                scaled = {k: v * servings_consumed for k, v in per_serving.items()}
                for k, v in scaled.items():
                    total_nutrients[k] = total_nutrients.get(k, 0.0) + v
                # Expand recipe ingredients into DIAAS ingredient list (handles sub-recipes)
                ingredients.extend(_expand_recipe_ingredients(row["recipe_id"], portion_factor, conn))
                items.append({
                    "id":        row["id"],
                    "food_name": row["food_name"],
                    "fdc_id":    None,
                    "recipe_id": row["recipe_id"],
                    "amount":    servings_consumed,
                    "unit":      "serving" + ("s" if servings_consumed != 1 else ""),
                    "notes":     row["notes"] or "",
                    "has_nuts":  bool(per_serving),
                })

        diaas_result = None
        if ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(ingredients, conn)
            except Exception:
                pass

    return items, total_nutrients, diaas_result


# ---------------------------------------------------------------------------
# Meal routes
# ---------------------------------------------------------------------------

def _compute_and_store_meal_bcp(meal_id: int) -> float | None:
    """Compute DIAAS-based BCP for a meal and persist it. Returns dcp_g or None."""
    _, _, diaas_result = _meal_totals(meal_id)
    diaas = _build_diaas_display(diaas_result)
    bcp_g = diaas["dcp_g"] if diaas else None
    with _db.get_db() as conn:
        _db.meal_set_bcp(conn, meal_id, bcp_g)
    return bcp_g


def _meals_list_ctx(meals_rows, show_all: bool, total: int, before_date: str | None) -> dict:
    """Build template context for the meals list, including day BCP aggregates."""
    meals = [dict(m) for m in meals_rows]
    hidden = max(0, total - len(meals))

    # Build day BCP totals from persisted bcp_g (complete meals only)
    dates_in_page = {m["meal_date"] for m in meals}
    day_bcp: dict[str, float | None] = {}
    for d in dates_in_page:
        with _db.get_db() as conn:
            date_rows = _db.meal_list_by_date(conn, d)
        vals = [r["bcp_g"] for r in date_rows if r["complete"] and r["bcp_g"] is not None]
        day_bcp[d] = round(sum(vals), 1) if vals else None

    # Profile protein target for % goal column
    rda = _load_rda()
    protein_target: float | None = None
    if rda and rda.get("protein_g") and rda["protein_g"][0] > 0:
        protein_target = rda["protein_g"][0]

    # Tag each meal with first-of-date flag so template can place Day BCP correctly
    seen_dates: set[str] = set()
    for m in meals:
        d = m["meal_date"]
        m["first_of_date"] = d not in seen_dates
        seen_dates.add(d)
        m["day_bcp"] = day_bcp.get(d)
        if protein_target and day_bcp.get(d) is not None:
            m["day_pct"] = round(day_bcp[d] / protein_target * 100, 0)  # type: ignore[operator]
        else:
            m["day_pct"] = None

    return {
        "meals":          meals,
        "total":          total,
        "hidden":         hidden,
        "show_all":       show_all,
        "today":          datetime.date.today().isoformat(),
        "date_filter":    before_date or "",
        "protein_target": protein_target,
    }


@app.get("/meals", response_class=HTMLResponse)
async def meals_list(request: Request, show_all: bool = False, date: str = ""):
    before_date = date.strip() or None
    limit = 1000 if show_all else 9
    with _db.get_db() as conn:
        meals_rows = _db.meal_list_recent(conn, limit=limit, before_date=before_date)
        total = _db.meal_count_recent(conn, before_date=before_date)
    return templates.TemplateResponse(request, "meals.html",
                                      _meals_list_ctx(meals_rows, show_all, total, before_date))


@app.post("/meals/compute-bcp", response_class=RedirectResponse)
async def meals_compute_bcp(redirect_to: str = Form("/meals")):
    """Recompute and persist BCP for all complete meals that lack a stored value."""
    with _db.get_db() as conn:
        all_meals = _db.meal_list_recent(conn, limit=10000)
    rda = _load_rda()
    protein_target: float | None = None
    if rda and rda.get("protein_g") and rda["protein_g"][0] > 0:
        protein_target = rda["protein_g"][0]

    for meal in all_meals:
        if not meal["complete"]:
            continue
        _compute_and_store_meal_bcp(meal["id"])

    # Now persist day_pct_goal for every complete meal
    if protein_target:
        with _db.get_db() as conn:
            all_meals2 = _db.meal_list_recent(conn, limit=10000)
        dates_seen: set[str] = set()
        for meal in all_meals2:
            if not meal["complete"] or meal["meal_date"] in dates_seen:
                continue
            dates_seen.add(meal["meal_date"])
            with _db.get_db() as conn:
                date_rows = _db.meal_list_by_date(conn, meal["meal_date"])
            vals = [r["bcp_g"] for r in date_rows if r["complete"] and r["bcp_g"] is not None]
            if not vals:
                continue
            day_bcp_g = sum(vals)
            pct = round(day_bcp_g / protein_target * 100, 1)
            for dr in date_rows:
                if dr["complete"]:
                    with _db.get_db() as conn:
                        _db.meal_set_day_pct_goal(conn, dr["id"], pct)

    return RedirectResponse(redirect_to, status_code=303)


@app.post("/meals/create", response_class=RedirectResponse)
async def meal_create(
    name: str = Form(""),
    meal_date: str = Form(""),
):
    name = name.strip() or "Meal"
    meal_date = meal_date.strip() or datetime.date.today().isoformat()
    with _db.get_db() as conn:
        meal_id = _db.meal_create(conn, name, meal_date)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/refresh-aa", response_class=RedirectResponse)
async def meal_refresh_aa(meal_id: int):
    """Fetch AA nutrient data from USDA for all foods in this meal that lack it."""
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
    for item in items:
        if item["item_type"] != "food" or not item["fdc_id"]:
            continue
        fdc_id = item["fdc_id"]
        with _db.get_db() as conn:
            cached = _db.get_cached_food(conn, fdc_id)
        if not cached or cached["user_drafted"]:
            continue
        data_type = cached["data_type"] or ""
        if data_type == "Branded":
            continue
        nutrients = json.loads(cached["nutrients_json"])
        if _usda.has_amino_acid_data(nutrients):
            continue
        try:
            detail = _usda.get_food_detail(fdc_id)
        except Exception:
            continue
        if not _usda.has_amino_acid_data(detail.get("nutrients", {})):
            continue
        with _db.get_db() as conn:
            _db.cache_food(conn, detail["fdcId"], detail["name"], detail["dataType"],
                           detail.get("brand"), detail.get("servingSize"),
                           detail.get("servingUnit"), detail.get("nutrients", {}),
                           detail.get("portions"))
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.get("/meal/{meal_id}", response_class=HTMLResponse)
async def meal_view(request: Request, meal_id: int, q: str = ""):
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
        if not meal:
            return RedirectResponse("/meals", status_code=303)
        sibling_meals = [
            dict(m) for m in _db.meal_list_by_date(conn, meal["meal_date"])
            if m["id"] != meal_id
        ]
    if not meal:
        return RedirectResponse("/meals", status_code=303)

    items, total_nutrients, diaas_result = _meal_totals(meal_id)

    # Search results for add-food panel
    search_results = []
    if q:
        # Prepend matching recipes (local DB, instant)
        with _db.get_db() as conn:
            all_recipes = _db.recipe_list(conn)
            cached = _db.search_cached_foods(conn, q)
        ql = q.lower()
        query_words = ql.split()
        matching_recipes = sorted(
            [r for r in all_recipes if any(w in r["name"].lower() for w in query_words)],
            key=lambda r: (-sum(1 for w in query_words if w in r["name"].lower()), r["name"].lower()),
        )
        for r in matching_recipes:
            search_results.append({
                "_type":    "recipe",
                "recipe_id": r["id"],
                "name":     r["name"],
                "servings": float(r["servings"] or 1),
                "data_type": "Recipe",
                "source":   "local",
            })
        seen: set[int] = set()
        for row in cached:
            seen.add(row["fdc_id"])
            portions = json.loads(row["portions_json"]) if row["portions_json"] else []
            search_results.append({"fdc_id": row["fdc_id"], "name": row["name"],
                                    "data_type": row["data_type"], "source": "cache",
                                    "portions": portions})
        try:
            for food in _usda.search_foods(q):
                fid = food.get("fdcId")
                if fid and fid not in seen:
                    seen.add(fid)
                    search_results.append({"fdc_id": fid,
                                           "name": food.get("description", ""),
                                           "data_type": food.get("dataType", ""),
                                           "source": "usda"})
        except Exception:
            pass

    rda = _load_rda()

    # Compute daily totals (this meal + siblings) for the day total % column
    daily_nutrients: dict | None = None
    if rda and total_nutrients:
        day_parts = [total_nutrients]
        for sib in sibling_meals:
            _, sib_nuts, _ = _meal_totals(sib["id"])
            if sib_nuts:
                day_parts.append(sib_nuts)
        if len(day_parts) > 1:
            daily_nutrients = {}
            for p in day_parts:
                for k, v in p.items():
                    daily_nutrients[k] = daily_nutrients.get(k, 0.0) + v
        else:
            daily_nutrients = total_nutrients

    diaas_display = _build_diaas_display(diaas_result)
    aa_nutrients   = _meal_aa_nutrients(meal_id)
    gl_total, gl_blockers = _compute_gl(meal_id)
    return templates.TemplateResponse(request, "meal.html", {
        "meal":                dict(meal),
        "items":               items,
        "nutrient_sections":   _nutrient_sections(total_nutrients, rda, daily_nutrients) if total_nutrients else [],
        "diaas":               diaas_display,
        "protein_adequacy":    _protein_adequacy(total_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":         _complement_suggestions(aa_nutrients, diaas_display["score"] if diaas_display else None),
        "gl":                  {"total": gl_total, "blockers": gl_blockers},
        "q":                   q,
        "search_results":      search_results,
        "today":               datetime.date.today().isoformat(),
        "has_profile":         rda is not None,
        "has_day_pct":         daily_nutrients is not None,
        "sibling_meals":       sibling_meals,
    })


_UNIT_TO_GRAMS: dict[str, float] = {
    "g": 1.0, "oz": 28.3495, "lb": 453.592, "kg": 1000.0,
}


@app.post("/meal/{meal_id}/add", response_class=RedirectResponse)
async def meal_add_food(
    meal_id: int,
    fdc_id: int = Form(...),
    food_name: str = Form(""),
    amount: float = Form(100.0),
    unit: str = Form("g"),
):
    grams = round(amount * _UNIT_TO_GRAMS.get(unit, 1.0), 2)
    # Ensure food is cached before adding to meal
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        try:
            detail = _usda.get_food_detail(fdc_id)
            with _db.get_db() as conn:
                _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                               data_type=detail.get("dataType", ""),
                               brand=detail.get("brand"),
                               serving_size=detail.get("servingSize"),
                               serving_unit=detail.get("servingUnit"),
                               nutrients=detail.get("nutrients", {}),
                               portions=detail.get("portions", []))
            food_name = food_name or detail["name"]
        except Exception:
            return RedirectResponse(f"/meal/{meal_id}", status_code=303)

    name = food_name or (cached["name"] if cached else "Unknown food")
    with _db.get_db() as conn:
        _db.meal_add_food(conn, meal_id, fdc_id, name, grams, "g")
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/add-recipe", response_class=RedirectResponse)
async def meal_add_recipe_item(
    meal_id: int,
    recipe_id: int = Form(...),
    recipe_name: str = Form(""),
    servings: float = Form(1.0),
):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)
    name = recipe_name or recipe["name"]
    unit = f"{servings:g} serving" + ("s" if servings != 1 else "")
    with _db.get_db() as conn:
        _db.meal_add_recipe(conn, meal_id, recipe_id, name, servings, unit=unit)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/remove/{item_id}", response_class=RedirectResponse)
async def meal_remove_item(meal_id: int, item_id: int):
    with _db.get_db() as conn:
        _db.meal_remove_item(conn, item_id, meal_id)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/rename", response_class=RedirectResponse)
async def meal_rename_post(meal_id: int, name: str = Form(...), meal_date: str = Form(...)):
    name = name.strip()
    meal_date = meal_date.strip()
    with _db.get_db() as conn:
        if name:
            _db.meal_rename(conn, meal_id, name)
        try:
            datetime.datetime.strptime(meal_date, "%Y-%m-%d")
            _db.meal_set_date(conn, meal_id, meal_date)
        except ValueError:
            pass
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/complete", response_class=RedirectResponse)
async def meal_toggle_complete(meal_id: int):
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
    if meal:
        with _db.get_db() as conn:
            _db.meal_set_complete(conn, meal_id, not bool(meal["complete"]))
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/delete", response_class=RedirectResponse)
async def meal_delete_post(meal_id: int):
    with _db.get_db() as conn:
        _db.meal_delete(conn, meal_id)
    return RedirectResponse("/meals", status_code=303)


@app.post("/meal/{meal_id}/update/{item_id}", response_class=RedirectResponse)
async def meal_update_item_post(
    meal_id: int,
    item_id: int,
    amount: float = Form(...),
    notes: str = Form(""),
):
    with _db.get_db() as conn:
        items = _db.meal_get_items(conn, meal_id)
    item = next((it for it in items if it["id"] == item_id), None)
    if item and amount > 0:
        notes_val = notes.strip() or None
        with _db.get_db() as conn:
            if item["item_type"] == "recipe":
                unit = f"{amount:g} serving" + ("s" if amount != 1 else "")
                _db.meal_update_item(conn, item_id, meal_id, amount, unit)
            else:
                _db.meal_replace_food(conn, item_id, meal_id, item["fdc_id"],
                                      item["food_name"], amount, "g", notes_val)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/merge", response_class=RedirectResponse)
async def meal_merge_post(meal_id: int, request: Request):
    form = await request.form()
    new_name = (form.get("new_name") or "").strip()
    delete_originals = bool(form.get("delete_originals"))
    raw_ids = form.getlist("merge_ids")
    try:
        selected_ids = [int(x) for x in raw_ids]
    except (ValueError, TypeError):
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)
    if len(selected_ids) < 2:
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)

    with _db.get_db() as conn:
        meals_to_merge = [_db.meal_get(conn, mid) for mid in selected_ids]
    meals_to_merge = [m for m in meals_to_merge if m is not None]
    if len(meals_to_merge) < 2:
        return RedirectResponse(f"/meal/{meal_id}", status_code=303)

    if not new_name:
        new_name = meals_to_merge[0]["name"]
    meal_date = meals_to_merge[0]["meal_date"]

    with _db.get_db() as conn:
        new_mid = _db.meal_create(conn, new_name, meal_date)
        for m in meals_to_merge:
            _db.meal_copy_items(conn, m["id"], new_mid)

    if delete_originals:
        with _db.get_db() as conn:
            for m in meals_to_merge:
                _db.meal_delete(conn, m["id"])

    return RedirectResponse(f"/meal/{new_mid}", status_code=303)


@app.get("/meals/search", response_class=HTMLResponse)
async def meals_search(request: Request, q: str = ""):
    rows: list[dict] = []
    n_items = n_meals = n_dates = 0
    if q.strip():
        with _db.get_db() as conn:
            rows = [dict(r) for r in _db.search_meal_history(conn, q.strip())]
        n_items = len(rows)
        n_meals = len({r["meal_id"] for r in rows})
        n_dates = len({r["meal_date"] for r in rows})
    return templates.TemplateResponse(request, "meals_search.html", {
        "q":       q,
        "rows":    rows,
        "n_items": n_items,
        "n_meals": n_meals,
        "n_dates": n_dates,
    })


def _day_analysis(meal_date: str) -> tuple[list, dict, dict | None]:
    """Compute combined nutrients and DIAAS for all meals on a given date."""
    with _db.get_db() as conn:
        meals = [dict(m) for m in _db.meal_list_by_date(conn, meal_date)]
        combined_nutrients: dict = {}
        all_ingredients: list = []

        for meal in meals:
            raw_items = _db.meal_get_items(conn, meal["id"])
            for row in raw_items:
                if row["item_type"] == "food" and row["fdc_id"]:
                    cached = _db.get_cached_food(conn, row["fdc_id"])
                    if not cached or not cached["nutrients_json"]:
                        continue
                    nuts_100g = json.loads(cached["nutrients_json"])
                    grams = float(row["amount"])
                    scaled = _usda.scale_nutrients(nuts_100g, grams)
                    for k, v in scaled.items():
                        combined_nutrients[k] = combined_nutrients.get(k, 0.0) + v
                    if nuts_100g:
                        all_ingredients.append({
                            "food_name":      row["food_name"],
                            "fdc_id":         row["fdc_id"],
                            "nutrients_100g": nuts_100g,
                            "grams":          grams,
                        })
                elif row["item_type"] == "recipe" and row["recipe_id"]:
                    recipe = _db.recipe_get(conn, row["recipe_id"])
                    if not recipe:
                        continue
                    total_servings = float(recipe["servings"] or 1)
                    servings_consumed = float(row["amount"])
                    portion_factor = servings_consumed / total_servings
                    per_serving = _recipe_nutrients_per_serving(row["recipe_id"], conn)
                    scaled = {k: v * servings_consumed for k, v in per_serving.items()}
                    for k, v in scaled.items():
                        combined_nutrients[k] = combined_nutrients.get(k, 0.0) + v
                    all_ingredients.extend(
                        _expand_recipe_ingredients(row["recipe_id"], portion_factor, conn)
                    )

        diaas_result = None
        if all_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(all_ingredients, conn)
            except Exception:
                pass

    return meals, combined_nutrients, diaas_result


@app.get("/meal/{meal_id}/day", response_class=HTMLResponse)
async def meal_day_view(request: Request, meal_id: int):
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
    if not meal:
        return RedirectResponse("/meals", status_code=303)
    meal_date = meal["meal_date"]
    meals, combined_nutrients, diaas_result = _day_analysis(meal_date)

    # Attach items list to each meal dict
    with _db.get_db() as conn:
        for m in meals:
            m["meal_items"] = [dict(it) for it in _db.meal_get_items(conn, m["id"])]

    diaas_display = _build_diaas_display(diaas_result)

    # Pool AA nutrients across all meals on this date (for complement suggestions)
    aa_nutrients: dict = {}
    for m in meals:
        for k, v in _meal_aa_nutrients(m["id"]).items():
            aa_nutrients[k] = aa_nutrients.get(k, 0.0) + v

    # Pool GL across all meals on this date
    gl_total_sum = 0.0
    all_gl_blockers: list[str] = []
    any_gl_none = False
    for m in meals:
        gl_val, gl_blockers = _compute_gl(m["id"])
        if gl_val is None:
            any_gl_none = True
        else:
            gl_total_sum += gl_val
        all_gl_blockers.extend(gl_blockers)
    gl_total = None if any_gl_none else round(gl_total_sum, 1)

    rda = _load_rda()
    return templates.TemplateResponse(request, "meal_day.html", {
        "meal_date":         meal_date,
        "meals":             meals,
        "from_meal_id":      meal_id,
        "nutrient_sections": _nutrient_sections(combined_nutrients, rda) if combined_nutrients else [],
        "diaas":             diaas_display,
        "protein_adequacy":  _protein_adequacy(combined_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":       _complement_suggestions(aa_nutrients, diaas_display["score"] if diaas_display else None),
        "gl":                {"total": gl_total, "blockers": all_gl_blockers},
        "has_profile":       rda is not None,
    })


# ---------------------------------------------------------------------------
# Settings / profile routes
# ---------------------------------------------------------------------------

@app.get("/settings", response_class=HTMLResponse)
async def settings_get(request: Request, saved: str = ""):
    profile = _profile.load_profile()
    rda = _profile.compute_rda(profile) if profile else None
    rda_rows = []
    if rda:
        for key, (val, unit, rda_type) in rda.items():
            label, _ = _usda.nutrient_label(key)
            rda_rows.append({"label": label, "value": round(val, 1),
                              "unit": unit, "rda_type": rda_type})
    prefs = _load_prefs_file()
    diet_pref = prefs.get("diet_pref", "all")
    if diet_pref not in _VALID_DIET_PREFS:
        diet_pref = "all"
    api_key = _usda.get_api_key()
    with _db.get_db() as conn:
        diaas_overrides = [dict(r) for r in _diaas.diaas_override_list(conn)]
    return templates.TemplateResponse(request, "settings.html", {
        "profile":          profile,
        "rda_rows":         rda_rows,
        "activity_labels":  _profile.ACTIVITY_LABELS,
        "sex_values":       _profile.SEX_VALUES,
        "saved":            saved,
        "diet_pref":        diet_pref,
        "diet_labels":      _DIET_LABELS,
        "api_key":          api_key,
        "diaas_overrides":  diaas_overrides,
    })


@app.post("/settings", response_class=RedirectResponse)
async def settings_post(
    age:            int   = Form(...),
    sex:            str   = Form(...),
    weight:         float = Form(...),
    weight_unit:    str   = Form("kg"),
    height_cm:      float = Form(0.0),
    height_ft:      int   = Form(0),
    height_in:      float = Form(0.0),
    height_unit:    str   = Form("cm"),
    activity_level: str   = Form(...),
):
    if height_unit == "imperial":
        height_cm_val = _profile.ftin_to_cm(height_ft, height_in)
    else:
        height_cm_val = height_cm

    weight_kg = _profile.lb_to_kg(weight) if weight_unit == "lb" else weight

    profile = _profile.UserProfile(
        age=age,
        sex=sex,
        weight_kg=round(weight_kg, 2),
        height_cm=round(height_cm_val, 1),
        activity_level=activity_level,
        weight_unit=weight_unit,
        height_unit=height_unit,
    )
    _profile.save_profile(profile)
    return RedirectResponse("/settings?saved=profile", status_code=303)


@app.post("/settings/diet", response_class=RedirectResponse)
async def settings_diet_post(diet_pref: str = Form(...)):
    if diet_pref in _VALID_DIET_PREFS:
        _save_prefs_file({"diet_pref": diet_pref})
    return RedirectResponse("/settings?saved=diet", status_code=303)


@app.post("/settings/api-key", response_class=RedirectResponse)
async def settings_api_key_post(api_key: str = Form("")):
    _usda.set_api_key(api_key.strip())
    return RedirectResponse("/settings?saved=api_key", status_code=303)


@app.post("/settings/diaas-override", response_class=RedirectResponse)
async def settings_diaas_override_post(
    food_name:     str   = Form(...),
    digestibility: float = Form(...),
    notes:         str   = Form(""),
):
    food_name = food_name.strip()
    if food_name and 0.0 <= digestibility <= 1.0:
        with _db.get_db() as conn:
            _diaas.diaas_override_set(conn, food_name, digestibility, notes.strip() or None)
    return RedirectResponse("/settings?saved=diaas", status_code=303)


@app.post("/settings/diaas-override/delete", response_class=RedirectResponse)
async def settings_diaas_override_delete(food_name: str = Form(...)):
    with _db.get_db() as conn:
        _diaas.diaas_override_delete(conn, food_name.strip())
    return RedirectResponse("/settings?saved=diaas", status_code=303)


@app.get("/recipes", response_class=HTMLResponse)
async def recipes_list(request: Request, q: str = ""):
    with _db.get_db() as conn:
        all_recipes = [dict(r) for r in _db.recipe_list(conn)]
    if q:
        ql = q.lower()
        words = ql.split()
        all_recipes = [r for r in all_recipes if any(w in r["name"].lower() for w in words)]
    return templates.TemplateResponse(request, "recipes.html", {
        "recipes": all_recipes,
        "q": q,
    })


@app.get("/recipe/new", response_class=HTMLResponse)
async def recipe_new_get(request: Request):
    return templates.TemplateResponse(request, "recipe_new.html", {})


@app.post("/recipe/new", response_class=RedirectResponse)
async def recipe_new_post(
    name: str = Form(...),
    description: str = Form(""),
    servings: int = Form(4),
    total_weight: str = Form(""),
    total_weight_unit: str = Form("g"),
):
    name = name.strip()
    if not name:
        return RedirectResponse("/recipe/new", status_code=303)
    tw = float(total_weight) if total_weight.strip() else None
    with _db.get_db() as conn:
        rid = _db.recipe_create(
            conn, name=name, description=description.strip(),
            servings=servings, instructions="",
            total_weight=tw,
            total_weight_unit=total_weight_unit if tw else None,
        )
    return RedirectResponse(f"/recipe/{rid}/edit", status_code=303)


@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe_detail(request: Request, recipe_id: int, servings: float = 1.0):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        _db.recipe_touch(conn, recipe_id)
        ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, recipe_id)]
        per_serving = _recipe_nutrients_per_serving(recipe_id, conn)
        recipe_servings = float(recipe["servings"] or 1)

        diaas_ingredients = []
        for ing in ingredients:
            if not ing["fdc_id"] or ing["ref_recipe_id"]:
                continue
            cached = _db.get_cached_food(conn, ing["fdc_id"])
            if not cached or not cached["nutrients_json"]:
                continue
            diaas_ingredients.append({
                "food_name":      ing["food_name"],
                "nutrients_100g": json.loads(cached["nutrients_json"]),
                "grams":          float(ing["amount"]) / recipe_servings * servings,
                "fdc_id":         ing["fdc_id"],
            })

        diaas_result = None
        if diaas_ingredients:
            try:
                diaas_result = _diaas.meal_level_diaas(diaas_ingredients, conn)
            except Exception:
                pass

    scaled = {k: v * servings for k, v in per_serving.items()}
    rda = _load_rda()
    diaas_display = _build_diaas_display(diaas_result)
    return templates.TemplateResponse(request, "recipe_detail.html", {
        "recipe":            dict(recipe),
        "ingredients":       ingredients,
        "servings":          servings,
        "nutrient_sections": _nutrient_sections(scaled, rda) if scaled else [],
        "diaas":             diaas_display,
        "protein_adequacy":  _protein_adequacy(scaled, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":       _complement_suggestions(scaled, diaas_display["score"] if diaas_display else None),
        "gl":                _recipe_gl_web(recipe_id, recipe_servings, servings),
        "has_profile":       rda is not None,
    })


@app.get("/recipe/{recipe_id}/edit", response_class=HTMLResponse)
async def recipe_edit_get(request: Request, recipe_id: int, q: str = "", saved: str = ""):
    with _db.get_db() as conn:
        recipe = _db.recipe_get(conn, recipe_id)
        if not recipe:
            return RedirectResponse("/recipes", status_code=303)
        ingredients = [dict(i) for i in _db.recipe_get_ingredients(conn, recipe_id)]

    search_results = []
    if q:
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, q)
        seen: set[int] = set()
        for row in cached:
            seen.add(row["fdc_id"])
            portions = json.loads(row["portions_json"]) if row["portions_json"] else []
            search_results.append({
                "fdc_id":    row["fdc_id"],
                "name":      row["name"],
                "data_type": row["data_type"],
                "source":    "cache",
                "portions":  portions,
            })
        try:
            for food in _usda.search_foods(q):
                fid = food.get("fdcId")
                if fid and fid not in seen:
                    seen.add(fid)
                    search_results.append({
                        "fdc_id":    fid,
                        "name":      food.get("description", ""),
                        "data_type": food.get("dataType", ""),
                        "source":    "usda",
                        "portions":  [],
                    })
        except Exception:
            pass

    return templates.TemplateResponse(request, "recipe_edit.html", {
        "recipe":         dict(recipe),
        "ingredients":    ingredients,
        "q":              q,
        "search_results": search_results,
        "saved":          saved,
    })


@app.post("/recipe/{recipe_id}/edit", response_class=RedirectResponse)
async def recipe_edit_post(
    recipe_id: int,
    name: str = Form(...),
    description: str = Form(""),
    servings: int = Form(1),
    total_weight: str = Form(""),
    total_weight_unit: str = Form("g"),
    instructions: str = Form(""),
    complete: str = Form(""),
):
    tw = float(total_weight) if total_weight.strip() else None
    with _db.get_db() as conn:
        _db.recipe_update(
            conn, recipe_id,
            name=name.strip(), description=description.strip(),
            servings=max(1, servings), instructions=instructions.strip(),
            total_weight=tw, total_weight_unit=total_weight_unit if tw else None,
            complete=bool(complete),
        )
    return RedirectResponse(f"/recipe/{recipe_id}/edit?saved=1", status_code=303)


@app.post("/recipe/{recipe_id}/delete", response_class=RedirectResponse)
async def recipe_delete_post(recipe_id: int):
    with _db.get_db() as conn:
        _db.recipe_delete(conn, recipe_id)
    return RedirectResponse("/recipes", status_code=303)


@app.post("/recipe/{recipe_id}/copy", response_class=RedirectResponse)
async def recipe_copy_post(recipe_id: int):
    with _db.get_db() as conn:
        src = _db.recipe_get(conn, recipe_id)
        if not src:
            return RedirectResponse("/recipes", status_code=303)
        new_id = _db.recipe_create(
            conn,
            name=f"Copy of {src['name']}",
            description=src["description"] or "",
            servings=src["servings"],
            instructions=src["instructions"] or "",
            total_weight=src["total_weight"],
            total_weight_unit=src["total_weight_unit"],
        )
        for ing in _db.recipe_get_ingredients(conn, recipe_id):
            _db.recipe_add_ingredient(
                conn, new_id, ing["fdc_id"], ing["food_name"],
                ing["amount"], ing["unit"], ing["notes"],
                ref_recipe_id=ing["ref_recipe_id"],
            )
    return RedirectResponse(f"/recipe/{new_id}/edit", status_code=303)


@app.post("/recipe/{recipe_id}/ingredient/add", response_class=RedirectResponse)
async def recipe_ingredient_add(
    recipe_id: int,
    fdc_id: int = Form(...),
    food_name: str = Form(""),
    amount: float = Form(100.0),
    unit: str = Form("g"),
    notes: str = Form(""),
):
    grams = round(amount * _UNIT_TO_GRAMS.get(unit, 1.0), 2)
    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, fdc_id)
    if not cached:
        try:
            detail = _usda.get_food_detail(fdc_id)
            with _db.get_db() as conn:
                _db.cache_food(conn, fdc_id=detail["fdcId"], name=detail["name"],
                               data_type=detail.get("dataType", ""),
                               brand=detail.get("brand"),
                               serving_size=detail.get("servingSize"),
                               serving_unit=detail.get("servingUnit"),
                               nutrients=detail.get("nutrients", {}),
                               portions=detail.get("portions", []))
            food_name = food_name or detail["name"]
        except Exception:
            return RedirectResponse(f"/recipe/{recipe_id}/edit", status_code=303)

    name = food_name or (cached["name"] if cached else "Unknown food")
    with _db.get_db() as conn:
        _db.recipe_add_ingredient(conn, recipe_id, fdc_id, name, grams, "g",
                                   notes.strip() or None)
    return RedirectResponse(f"/recipe/{recipe_id}/edit", status_code=303)


@app.post("/recipe/{recipe_id}/ingredient/{ing_id}/remove", response_class=RedirectResponse)
async def recipe_ingredient_remove(recipe_id: int, ing_id: int):
    with _db.get_db() as conn:
        _db.recipe_remove_ingredient(conn, ing_id)
    return RedirectResponse(f"/recipe/{recipe_id}/edit", status_code=303)


@app.post("/recipe/{recipe_id}/ingredient/{ing_id}/edit", response_class=RedirectResponse)
async def recipe_ingredient_edit(
    recipe_id: int,
    ing_id: int,
    amount: float = Form(...),
    unit: str = Form("g"),
    food_name: str = Form(...),
    notes: str = Form(""),
):
    grams = round(amount * _UNIT_TO_GRAMS.get(unit, 1.0), 2)
    with _db.get_db() as conn:
        _db.recipe_update_ingredient(conn, ing_id, grams, "g",
                                      food_name.strip(), notes.strip() or None)
    return RedirectResponse(f"/recipe/{recipe_id}/edit", status_code=303)


@app.get("/summary", response_class=HTMLResponse)
async def summary_index(request: Request):
    """Summary landing: recent-days table + date picker."""
    with _db.get_db() as conn:
        rows = _db.meal_dates_with_bcp(conn, limit=30)

    rda = _load_rda()
    protein_target: float | None = None
    if rda and rda.get("protein_g") and rda["protein_g"][0] > 0:
        protein_target = rda["protein_g"][0]

    day_rows = []
    for r in rows:
        bcp = r["day_bcp"]
        pct = round(bcp / protein_target * 100, 0) if (bcp is not None and protein_target) else None
        day_rows.append({
            "meal_date":     r["meal_date"],
            "day_bcp":       round(bcp, 1) if bcp is not None else None,
            "pct_goal":      pct,
            "complete_count": r["complete_count"],
        })

    return templates.TemplateResponse(request, "summary.html", {
        "day_rows":       day_rows,
        "protein_target": protein_target,
        "today":          datetime.date.today().isoformat(),
        "date_detail":    None,
    })


@app.get("/summary/{meal_date}", response_class=HTMLResponse)
async def summary_date(request: Request, meal_date: str):
    """Full-day nutrient + DIAAS analysis for a specific date."""
    meals, combined_nutrients, diaas_result = _day_analysis(meal_date)
    if not meals:
        return RedirectResponse("/summary", status_code=303)

    with _db.get_db() as conn:
        for m in meals:
            m["meal_items"] = [dict(it) for it in _db.meal_get_items(conn, m["id"])]

    diaas_display = _build_diaas_display(diaas_result)

    aa_nutrients: dict = {}
    for m in meals:
        for k, v in _meal_aa_nutrients(m["id"]).items():
            aa_nutrients[k] = aa_nutrients.get(k, 0.0) + v

    gl_total_sum = 0.0
    all_gl_blockers: list[str] = []
    any_gl_none = False
    for m in meals:
        gl_val, gl_blockers = _compute_gl(m["id"])
        if gl_val is None:
            any_gl_none = True
        else:
            gl_total_sum += gl_val
        all_gl_blockers.extend(gl_blockers)
    gl_total = None if any_gl_none else round(gl_total_sum, 1)

    rda = _load_rda()

    # Recent days for sidebar
    with _db.get_db() as conn:
        rows = _db.meal_dates_with_bcp(conn, limit=14)
    protein_target: float | None = None
    if rda and rda.get("protein_g") and rda["protein_g"][0] > 0:
        protein_target = rda["protein_g"][0]
    day_rows = []
    for r in rows:
        bcp = r["day_bcp"]
        pct = round(bcp / protein_target * 100, 0) if (bcp is not None and protein_target) else None
        day_rows.append({
            "meal_date":      r["meal_date"],
            "day_bcp":        round(bcp, 1) if bcp is not None else None,
            "pct_goal":       pct,
            "complete_count": r["complete_count"],
        })

    return templates.TemplateResponse(request, "summary.html", {
        "day_rows":          day_rows,
        "protein_target":    protein_target,
        "today":             datetime.date.today().isoformat(),
        "date_detail":       meal_date,
        "meals":             meals,
        "nutrient_sections": _nutrient_sections(combined_nutrients, rda) if combined_nutrients else [],
        "diaas":             diaas_display,
        "protein_adequacy":  _protein_adequacy(combined_nutrients, diaas_display["dcp_g"] if diaas_display else None, rda),
        "complements":       _complement_suggestions(aa_nutrients, diaas_display["score"] if diaas_display else None),
        "gl":                {"total": gl_total, "blockers": all_gl_blockers},
        "has_profile":       rda is not None,
    })


@app.get("/manual", response_class=HTMLResponse)
async def manual(request: Request):
    text = _MANUAL.read_text(encoding="utf-8") if _MANUAL.exists() else "*(manual not found)*"
    body = _md.markdown(text, extensions=["toc", "fenced_code", "tables"])
    return templates.TemplateResponse(request, "manual.html", {"body": body})
