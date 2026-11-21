# Data shapes: database rows and the nutrients dict

Moved from `CLAUDE.md` (2026-11-12) so it loads only when a task needs it; `CLAUDE.md` points here. Read when code reads DB rows or nutrient values.

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
`id, name, description, servings, serving_size, dcp_g, dcp_computed_at, created_at, complete, on_hand, last_accessed_at, total_weight, total_weight_unit, total_volume, total_volume_unit`
(`recipe_list` also returns `archived`, `notes`, `is_drink`; `recipe_list_recent` returns `archived`, `is_drink`; `recipe_get` is `SELECT *` and also returns `instructions`, `introduction`, `notes`, `archived`)

`serving_size` is a free-text human description of what one serving actually is (e.g. `"1 muffin"`), set on the Edit Recipe page — independent of `total_weight`/`servings`, which give the gram weight of that same serving. Shown wherever a recipe's serving count is displayed, via the `_serving_note.html` macro.

`recipe_get_ingredients()` rows:
`id, recipe_id, fdc_id, food_name, amount, unit, notes, ref_recipe_id`

`meal_get_items()` rows:
`id, meal_id, item_type ('food'|'recipe'), fdc_id, recipe_id, food_name, amount, unit, notes, serving_grams`
(`serving_grams` = grams per recipe serving when logged; see `_annotate_recipe_amounts()` in web/backend.py)

`pantry_list()` rows:
`id, food_name, fdc_id, notes`

`get_cached_food()` rows:
`fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json, user_drafted, notes`
(`SELECT *`, so every `foods` column. `notes` are the source's (overwritten by a Refresh), except on a custom food, where they are the user's; `user_notes` are the user's own notes on any other food, written only by `food_set_user_notes()`.)

## Nutrients Dict

All nutrient values are **per 100 g**. The dict is stored as JSON in `foods.nutrients_json` and passed around as `dict[str, float]`.

Valid keys (from `usda_api.NUTRIENT_MAP`):

```
# Macros
calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g,
saturated_fat_g, mono_fat_g, poly_fat_g

# Water (g) — total moisture; drinks/food split is derived, see water.py
water_g

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
