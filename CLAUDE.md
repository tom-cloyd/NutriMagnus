# NutriMagnus (numa) — AI Coding Guide

Nutritional analysis web app (FastAPI). USDA FoodData Central + Open Food Facts. Python 3.13.

Full architecture docs: `README-numa-documentation.md`

Note: this was previously a dual CLI+web project. The interactive terminal CLI was removed
2026-08-04 — the owner never used it and expected no other users to either. This file is
fully updated for the web-only codebase. `README-numa-documentation.md` may still have
CLI-era mechanics pending its own cleanup pass.

---

## Run / Test

```bash
python web/launcher.py           # launch the web app (opens a browser tab)
pytest                           # run full test suite
pytest tests/test_web.py -k foo  # run one test
```

---

## Package Layout

```
db.py                — all SQLite access (get_db context manager + query functions)
usda.py               — thin re-export shim; edit usda_api.py / usda_nutrients.py instead
usda_api.py           — USDA HTTP client, NUTRIENT_MAP, amino acid constants
usda_nutrients.py     — nutrient math, AA analysis, DIAAS, complement suggestions
diaas.py              — meal-level DIAAS pooled calculation
profile.py            — UserProfile dataclass, RDA computation
export.py             — report rendering (txt / md / html)
openfoodfacts.py      — Open Food Facts API client

numa_app/
  services/
    aa_estimate.py     — estimate a food's AA profile by scaling another food's
                         AA values to its own protein content: estimate_aa(), source_note()
    complements.py     — shared complement-suggestion math: aa_effects(),
                         two_step_combo(), build_complement_display()
    day_profile.py     — per-day profile pinning: get_profile_for_date(),
                         ensure_day_profile(), backfill_missing_day_profiles(),
                         set_day_profile_override(), protein_target_for_date() —
                         required entry point for any date-scoped profile lookup
    food_ids.py        — classify_food_id() — food/recipe ID → (id_str, source_label)
    glycemic_load.py    — shared GL aggregation: compute_glycemic_load()
    manual_build.py     — rebuild_manual_if_stale(), used by the /manual route
    meal_bcp.py         — shared meal-DCP fallback: recipe_dcp_fallback()
    portions.py         — _parse_portion_input() — portion-string parsing
    rda_status.py       — shared RDA/limit percent-of-target classification: rda_status()
    recipe_nutrients.py — shared recursive recipe-ingredient expansion:
                         expand_recipe_ingredients(), recipe_total_nutrients(), best_aa_nutrients()
    search.py           — _refresh_cache_if_missing_aa(), used by recipe_nutrients.py

web/
  backend.py           — the FastAPI app: all routes
  launcher.py          — starts uvicorn and opens a browser tab
  templates/           — Jinja2 templates
  static/              — CSS/static assets
```

---

## Database Pattern

```python
# ALWAYS use the context manager — it commits on clean exit, rolls back on exception
with _db.get_db() as conn:
    row = _db.recipe_get(conn, rid)

# NEVER hold a connection open across a slow operation (an external API call,
# a second network round-trip) — open it, do the DB work, close it
with _db.get_db() as conn:
    data = _db.some_query(conn)
# ... slow operation here ...
with _db.get_db() as conn:
    _db.some_write(conn, data)
```

`get_db()` sets `row_factory = sqlite3.Row` on the connection.

**Row column names** (key tables):

`recipe_list()` / `recipe_get()` rows:
`id, name, description, servings, dcp_g, dcp_computed_at, created_at, complete, last_accessed_at, total_weight, total_weight_unit`
(`recipe_get` also returns `total_volume`, `total_volume_unit`, `instructions`)

`recipe_get_ingredients()` rows:
`id, recipe_id, fdc_id, food_name, amount, unit, notes, ref_recipe_id`

`meal_get_items()` rows:
`id, meal_id, item_type ('food'|'recipe'), fdc_id, recipe_id, food_name, amount, unit, notes`

`pantry_list()` rows:
`id, food_name, fdc_id, notes`

`get_cached_food()` rows:
`fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json, user_drafted, notes`

---

## Nutrients Dict

All nutrient values are **per 100 g**. The dict is stored as JSON in `foods.nutrients_json` and passed around as `dict[str, float]`.

Valid keys (from `usda_api.NUTRIENT_MAP`):

```
# Macros
calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g,
saturated_fat_g, mono_fat_g, poly_fat_g

# Omega fatty acids (mg)
omega3_ala_mg, omega3_epa_mg, omega3_dha_mg, omega6_la_mg

# Minerals (mg, except iodine/selenium which are mcg)
calcium_mg, iron_mg, magnesium_mg, phosphorus_mg,
potassium_mg, sodium_mg, zinc_mg, iodine_mcg, selenium_mcg

# Vitamins
vitamin_a_mcg, vitamin_c_mg, vitamin_d_mcg, vitamin_e_mg,
vitamin_k_mcg, thiamin_mg, riboflavin_mg, niacin_mg,
b6_mg, folate_mcg, b12_mcg

# Phytonutrients
beta_carotene_mcg, alpha_carotene_mcg, lycopene_mcg,
lutein_zeaxanthin_mcg, choline_mg, beta_sitosterol_mg, isoflavones_mg

# Amino acids (g) — all prefixed aa_
aa_tryptophan_g, aa_threonine_g, aa_isoleucine_g, aa_leucine_g,
aa_lysine_g, aa_methionine_g, aa_cystine_g, aa_phenylalanine_g,
aa_tyrosine_g, aa_valine_g, aa_histidine_g
```

Essential AAs: all `aa_` keys except `aa_cystine_g` and `aa_tyrosine_g`.
`usda.has_amino_acid_data(nutrients)` → True if 5+ non-zero AA values present.

---

## Key Invariants

- **Never `import usda_api` or `import usda_nutrients` directly** — always `import usda as _usda`. `usda.py` is the stable public surface.
- **Never open the DB outside `get_db()`** — no raw `sqlite3.connect()` calls anywhere.
- **Add `Docs:` line** to any new module's docstring pointing to the relevant README section.
- **Bump `version.py`'s `VERSION` stamp before ending any session that changed application behavior** (bug fixes, features, refactors — not pure docs/comments). Get the current timestamp with `date "+%Y-%m-%d:%H%M"` and never guess it. If `user-manual.md` or `README-numa-documentation.md` were also edited, update their header stamps the same way (see each file's top few lines for the exact format).

---

## Test Conventions

- `_mock_api(monkeypatch)` (in `tests/conftest.py`) — stubs USDA API; use for any test that touches food search.
- Autouse fixtures handle DB, profile, and OFF stub — don't set these up manually.
- `tests/test_web.py` has its own `use_test_web_prefs` fixture and `client` (FastAPI `TestClient`) fixture.
