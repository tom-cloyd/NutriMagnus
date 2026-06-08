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
_PREFS_FILE = Path.home() / ".local" / "share" / "numa" / "prefs.json"

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
    ("Amino Acids", [
        "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
        "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
        "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g",
    ]),
]


def _nutrient_sections(nutrients: dict, rda: dict | None = None) -> list[dict]:
    sections = []
    for group_name, keys in _NUTRIENT_GROUPS:
        rows = []
        for key in keys:
            val = nutrients.get(key)
            if not val:
                continue
            label, unit = _usda.nutrient_label(key)
            pct = rda_type = rda_css = None
            if rda and key in rda:
                rda_val, _rda_unit, rda_type = rda[key]
                if rda_val and rda_val > 0:
                    pct = round(val / rda_val * 100, 0)
                    if rda_type == "limit":
                        rda_css = "rda-over" if pct > 100 else "rda-met"
                    else:
                        rda_css = "rda-met" if pct >= 100 else ("rda-near" if pct >= 75 else "rda-low")
            rows.append({
                "label":    label,
                "value":    round(val, 3),
                "unit":     unit,
                "pct":      pct,
                "rda_type": rda_type,
                "rda_css":  rda_css,
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
    return templates.TemplateResponse(request, "home.html", {})


async def _search_logic(request: Request, query: str, template: str, extra_ctx: dict | None = None):
    """Shared search logic for food search and analyze-portion pages."""
    query = query.strip()
    results = []
    error = None

    if query:
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, query)
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
    factor = servings  # per_serving already divides by recipe_servings
    scaled = {k: v * factor for k, v in per_serving.items()}
    rda = _load_rda()

    return templates.TemplateResponse(request, "food_analyze_recipe_portion.html", {
        "recipes":          recipes,
        "selected_recipe":  dict(recipe),
        "servings_input":   servings,
        "analysis": {
            "recipe_name":      recipe["name"],
            "servings_analyzed": servings,
        },
        "nutrient_sections":  _nutrient_sections(scaled, rda),
        "protein":            _protein_section(recipe["name"], per_serving),
        "has_profile":        rda is not None,
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
    """Sum ingredient nutrients for one recipe, return per-serving totals."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return {}
    servings = float(recipe["servings"] or 1)
    total: dict = {}
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if not ing["fdc_id"]:
            continue  # sub-recipe or missing food — skip for now
        cached = _db.get_cached_food(conn, ing["fdc_id"])
        if not cached or not cached["nutrients_json"]:
            continue
        nuts_100g = json.loads(cached["nutrients_json"])
        scaled = _usda.scale_nutrients(nuts_100g, float(ing["amount"]))
        for k, v in scaled.items():
            total[k] = total.get(k, 0.0) + v
    return {k: v / servings for k, v in total.items()} if servings else total


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
                # Expand recipe ingredients into DIAAS ingredient list
                for ing in _db.recipe_get_ingredients(conn, row["recipe_id"]):
                    if not ing["fdc_id"]:
                        continue
                    cached = _db.get_cached_food(conn, ing["fdc_id"])
                    if not cached or not cached["nutrients_json"]:
                        continue
                    nuts_100g = json.loads(cached["nutrients_json"])
                    if nuts_100g:
                        ingredients.append({
                            "food_name":      ing["food_name"],
                            "fdc_id":         ing["fdc_id"],
                            "nutrients_100g": nuts_100g,
                            "grams":          float(ing["amount"]) * portion_factor,
                        })
                items.append({
                    "id":        row["id"],
                    "food_name": row["food_name"],
                    "fdc_id":    None,
                    "recipe_id": row["recipe_id"],
                    "amount":    servings_consumed,
                    "unit":      "serving" + ("s" if servings_consumed != 1 else ""),
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

@app.get("/meals", response_class=HTMLResponse)
async def meals_list(request: Request, show_all: bool = False):
    limit = 1000 if show_all else 9
    with _db.get_db() as conn:
        meals = _db.meal_list_recent(conn, limit=limit)
        total = _db.meal_count_recent(conn)
    hidden = max(0, total - len(meals))
    return templates.TemplateResponse(request, "meals.html", {
        "meals":    meals,
        "total":    total,
        "hidden":   hidden,
        "show_all": show_all,
        "today":    datetime.date.today().isoformat(),
    })


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


@app.get("/meal/{meal_id}", response_class=HTMLResponse)
async def meal_view(request: Request, meal_id: int, q: str = ""):
    with _db.get_db() as conn:
        meal = _db.meal_get(conn, meal_id)
    if not meal:
        return RedirectResponse("/meals", status_code=303)

    items, total_nutrients, diaas_result = _meal_totals(meal_id)

    # Search results for add-food panel
    search_results = []
    if q:
        with _db.get_db() as conn:
            cached = _db.search_cached_foods(conn, q)
        seen: set[int] = set()
        for row in cached:
            seen.add(row["fdc_id"])
            search_results.append({"fdc_id": row["fdc_id"], "name": row["name"],
                                    "data_type": row["data_type"], "source": "cache"})
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

    # Prepare DIAAS display
    diaas_display = None
    if diaas_result and diaas_result.get("total_protein_g", 0) > 0:
        iaa_rows = [
            {"label": _usda.nutrient_label(k)[0], "ratio": round(v, 3), "met": v >= 1.0}
            for k, v in sorted(diaas_result.get("iaa_ratios", {}).items(), key=lambda x: x[1])
        ]
        diaas_display = {
            "score":           diaas_result.get("diaas"),
            "total_protein_g": round(diaas_result.get("total_protein_g", 0), 1),
            "dcp_g":           round(diaas_result.get("digestible_complete_protein_g") or 0, 1),
            "limiting_label":  diaas_result.get("limiting_label"),
            "iaa_rows":        iaa_rows,
            "missing":         diaas_result.get("missing_aa_names", []),
            "has_complete":    diaas_result.get("has_complete_data", False),
        }

    rda = _load_rda()
    return templates.TemplateResponse(request, "meal.html", {
        "meal":              dict(meal),
        "items":             items,
        "nutrient_sections": _nutrient_sections(total_nutrients, rda) if total_nutrients else [],
        "diaas":             diaas_display,
        "q":                 q,
        "search_results":    search_results,
        "today":             datetime.date.today().isoformat(),
        "has_profile":       rda is not None,
    })


@app.post("/meal/{meal_id}/add", response_class=RedirectResponse)
async def meal_add_food(
    meal_id: int,
    fdc_id: int = Form(...),
    food_name: str = Form(""),
    amount: float = Form(100.0),
):
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
        _db.meal_add_food(conn, meal_id, fdc_id, name, amount, "g")
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


@app.post("/meal/{meal_id}/remove/{item_id}", response_class=RedirectResponse)
async def meal_remove_item(meal_id: int, item_id: int):
    with _db.get_db() as conn:
        _db.meal_remove_item(conn, item_id, meal_id)
    return RedirectResponse(f"/meal/{meal_id}", status_code=303)


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
async def recipes(request: Request):
    return templates.TemplateResponse(request, "recipes.html", {})


@app.get("/summary", response_class=HTMLResponse)
async def summary(request: Request):
    return templates.TemplateResponse(request, "summary.html", {})


@app.get("/manual", response_class=HTMLResponse)
async def manual(request: Request):
    text = _MANUAL.read_text(encoding="utf-8") if _MANUAL.exists() else "*(manual not found)*"
    body = _md.markdown(text, extensions=["toc", "fenced_code", "tables"])
    return templates.TemplateResponse(request, "manual.html", {"body": body})
