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

_WEB_DIR  = Path(__file__).parent
_MANUAL   = _WEB_DIR.parent / "user-manual.md"

app = FastAPI(title="numa")
app.mount("/static", StaticFiles(directory=_WEB_DIR / "static"), name="static")
templates = Jinja2Templates(directory=_WEB_DIR / "templates")

# Custom Jinja2 filters for height display
templates.env.filters["ftin_ft"] = lambda cm: _profile.cm_to_ftin(cm)[0]
templates.env.filters["ftin_in"] = lambda cm: round(_profile.cm_to_ftin(cm)[1], 1)

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
    return templates.TemplateResponse(
        request, "search.html", {"results": [], "query": ""}
    )


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form("")):
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

    return templates.TemplateResponse(request, "search.html", {
        "results": results,
        "query":   query,
        "error":   error,
    })


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
async def settings_get(request: Request, saved: bool = False):
    profile = _profile.load_profile()
    rda = _profile.compute_rda(profile) if profile else None
    rda_rows = []
    if rda:
        for key, (val, unit, rda_type) in rda.items():
            label, _ = _usda.nutrient_label(key)
            rda_rows.append({"label": label, "value": round(val, 1),
                              "unit": unit, "rda_type": rda_type})
    return templates.TemplateResponse(request, "settings.html", {
        "profile":           profile,
        "rda_rows":          rda_rows,
        "activity_labels":   _profile.ACTIVITY_LABELS,
        "sex_values":        _profile.SEX_VALUES,
        "saved":             saved,
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
    return RedirectResponse("/settings?saved=1", status_code=303)


@app.get("/manual", response_class=HTMLResponse)
async def manual(request: Request):
    text = _MANUAL.read_text(encoding="utf-8") if _MANUAL.exists() else "*(manual not found)*"
    body = _md.markdown(text, extensions=["toc", "fenced_code", "tables"])
    return templates.TemplateResponse(request, "manual.html", {"body": body})
