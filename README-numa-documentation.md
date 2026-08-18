# NutriMagnus — Nutritional Analysis Program documentation

A nutritional analysis web app written in Python (FastAPI). Analyzes individual food portions, recipes, and complete meals using data from the USDA FoodData Central database. The program presents itself to users as **NutriMagnus ("nutrition wizard")**.

UPDATED: 2026-08-07:0744

Note: this was previously a dual CLI+web project. The interactive terminal CLI was removed 2026-08-04 — the owner never used it and expected no other users to either. This document has been updated for the web-only codebase. The "Bugs found during test restoration" and "Implementation Phases" sections near the end are left as historical development records and still describe CLI-era files/mechanics from when they happened — not current instructions.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Program](#running-the-program)
- [Architecture](#architecture)
- [Web Interface](#web-interface)
- [Data Storage](#data-storage)
- [Test Suite](#test-suite)
- [Maintenance](#maintenance)
- [Implementation Phases](#implementation-phases)

---

## Overview

NutriMagnus was designed from a preliminary specification (see `2025-02-26-python-nutritional analysis program.md`) that called for:

- Calculation of bio-available complete protein combinations for one or more foods
- Nutritional analysis of individual foods, recipes, and meals
- Saving meals by date and saving recipes

The program uses two nutrition data sources:

- **USDA FoodData Central** — free, comprehensive, 300,000+ foods with full macro/micronutrient profiles including amino acid data for protein completeness analysis.
- **Open Food Facts** — free, open-source (CC BY-SA 4.0), community-maintained, millions of branded/packaged products globally. No API key required. Does not include amino acid data.

---

## Project Structure

Note: the CLI was removed 2026-08-04. `numa_app/` used to also contain `main.py`, `state.py`, `config/`, `ui/`, and `workflows/` (all CLI-only) plus CLI-only `services/annotations.py`, `oxalate_link.py`, and `reports.py` — all deleted. `manual.py` (the CLI's `?keyword` help lookup) was also deleted; the small bit of it the web app needs (`rebuild_manual_if_stale()`) now lives in `numa_app/services/manual_build.py`.

```
numa/
  db.py                            — SQLite database: schema, queries, context manager
  usda.py                          — backwards-compatible re-export shim; import this
  usda_api.py                      — USDA FoodData Central HTTP client; API key; search; detail fetch
  usda_nutrients.py                — nutrient math; AA analysis; DIAAS lookup; complement table; density
  openfoodfacts.py                 — Open Food Facts API client; merged into food search results
  diaas.py                         — Meal-level DIAAS calculation and digestibility data
  export.py                        — Report export (txt, md, html)
  profile.py                       — User profile dataclass, RDA computation, unit parsing
  platform_utils.py                — Cross-platform data-dir path resolution
  version.py                       — Single-source-of-truth VERSION stamp
  requirements.txt                 — Python dependencies (fastapi, uvicorn, Jinja2, Markdown, python-multipart;
                                     pytest/httpx for test/dev)
  import_foods.py, import_json_folder.py, import_gi_seed.py
                                    — standalone maintenance scripts, independent of the web app
                                     (numa_gen_prompt.py, numa_import_claude.py also exist locally
                                     as personal, gitignored scratch tools — not part of the repo)
  build_oxalate_db.py              — one-time script: builds oxalate.db from oxalate_source_data.py
  README-numa-documentation.md     — This file
  scripts/
    setup_venv.sh                  — Create and populate .venv
    build_manual.py                — Regenerates user-manual.html from user-manual.md
  numa_app/
    __init__.py
    services/
      aa_estimate.py                — estimate a food's AA profile by scaling another food's AA
                                      values to its own protein content: estimate_aa(), source_note()
      claude_fetch.py                — Claude AI amino-acid-fetch prompt building and response import
      complements.py                — shared complement-suggestion display math: aa_effects(),
                                      two_step_combo(), build_complement_display()
      day_profile.py                 — per-day profile pinning: get_profile_for_date(), ensure_day_profile()
      diet_aware.py                  — B12/iron/zinc bioavailability notes based on dietary preference
      food_ids.py                    — classify_food_id() — food/recipe ID → (id_str, source_label)
      food_import.py                 — shared food-cache import logic (used by import_foods.py etc.)
      glycemic_load.py               — shared glycemic load aggregation: compute_glycemic_load()
      manual_build.py                — rebuild_manual_if_stale(), used by the web app's /manual route
      meal_bcp.py                    — shared meal-DCP fallback: recipe_dcp_fallback()
      meal_list_columns.py           — shared Meals & Log custom-column logic
      nutrient_trend.py              — multiday nutrient trend averaging
      plotting.py                    — nutrient trend line-chart rendering
      portions.py                    — _parse_portion_input() — portion-string parsing
      rda_status.py                  — shared RDA/limit percent-of-target classification: rda_status()
      recipe_dcp.py                  — shared auto-recompute of a recipe's per-serving DCP: recompute_recipe_dcp()
      recipe_nutrients.py            — shared recursive recipe-ingredient expansion:
                                      expand_recipe_ingredients(), recipe_total_nutrients(), best_aa_nutrients()
      search.py                      — _refresh_cache_if_missing_aa(), used by recipe_nutrients.py
      search_ranking.py              — shared food-search relevance ranking: relevance_key()
  user-manual.md                   — Essential instructions, tips, and reference material for
                                     users; plain-text sections keyed by {: #anchor} for inline display
  oxalate.py                       — Read-only access to oxalate.db: get_oxalate_db(), search_similar(),
                                     get_by_id(), format_oxalate(), category_label()
  oxalate_source_data.py           — Harvard T.H. Chan School of Public Health oxalate table compiled
                                     as Python dicts (433 foods, Nov 2023); SOURCE_URL, SOURCE_DATE
  build_oxalate_db.py              — One-time script: reads oxalate_source_data.py and creates oxalate.db
                                     Run: python build_oxalate_db.py
  oxalate.db                       — Static SQLite reference database (tables: oxalate_foods, source_info)
                                     Committed to repo; rebuilt by build_oxalate_db.py
  web/                             — Local web interface (FastAPI + Jinja2)
    backend.py                     — All routes, helpers, and template context builders
    static/
      style.css                    — Site-wide custom CSS (Bootstrap 5 base)
    templates/
      base.html                    — Shared layout: navbar, Bootstrap CDN links, keyboard-shortcut JS
      home.html                    — Landing page (rendered from home.md)
      search.html                  — Food search results (USDA + cache)
      food_detail.html             — Single food nutrient breakdown with RDA % and protein quality
      food_analyze_portion.html    — Select food + enter grams → nutrient table
      food_analyze_recipe_portion.html — Select saved recipe + servings → nutrient table
      food_convert.html            — Portion ↔ weight conversion (density lookup)
      food_compare.html            — Side-by-side nutrient comparison (up to 6 foods, save/load)
      food_cache.html              — Browse/search cached foods; delete from cache
      food_custom_profiles.html    — List user-drafted food profiles; create/delete
      food_annotate.html           — Browse foods for GI/DIAAS annotation; edit annotation form
      pantry.html                  — My Pantry: add/remove foods on hand
      meals.html                   — Meal list with Complete column, date filter, search link
      meal.html                    — Meal view/edit: items, inline edit, add food/recipe, manage actions
      meal_day.html                — Full-day combined nutrient + DIAAS analysis across all meals on a date
      meals_search.html            — Search all meal history; flat occurrences + summary-by-food tables
      recipes.html                 — Recipes placeholder (stub)
      summary.html                 — Daily summary placeholder (stub)
      settings.html                — User profile, dietary preferences, USDA API key, DIAAS overrides
      manual.html                  — Rendered user-manual.md
  .venv/                           — Python virtual environment (not committed)
```

---

## Setup

### 1. Virtual environment

The `.venv` directory is already created and populated. It uses Python 3.13 from the local miniconda installation, matching the `cmgr` project convention.

To recreate it from scratch using the setup script:

```bash
cd numa
./scripts/setup_venv.sh
```

Or manually:

```bash
cd numa
/home/tomc/miniconda3/bin/python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Dependencies (`requirements.txt`):

| Package           | Purpose                                    |
|-------------------|---------------------------------------------|
| `fastapi`         | Web app framework                          |
| `uvicorn`         | ASGI server                                |
| `Jinja2`          | Template rendering                         |
| `Markdown`        | Renders the manual and other markdown text |
| `python-multipart`| Form-data parsing (FastAPI dependency)     |
| `pytest`, `httpx` | Test suite / test client (test/dev only)   |

> **Note:** `requests` is not a dependency; HTTP uses stdlib `urllib`.

### 2. USDA API key

Food searches require a free API key from the USDA FoodData Central service.

#### Getting a key

1. Go to **https://fdc.nal.usda.gov/api-key-signup.html**
2. Enter your name and email address — no payment or account creation required.
3. The key is emailed to you immediately (check spam if it doesn't arrive within a minute or two).

The key is free and gives you **1,000 requests per hour**, which is more than enough for normal use. There is no paid tier — this is the standard limit for all registered keys.

> **Note:** The USDA API has a built-in `DEMO_KEY` that works without registration, but it is limited to roughly 30 requests per hour and will rate-limit quickly during a normal session. Always use a registered key for real use.

#### Setting the key

Set it from **Settings → Advanced settings → USDA API key** in the web app. It's saved to `~/.config/numa/config.json` and used automatically on all subsequent runs.

---

## Running the Program

```bash
python web/launcher.py
```

This starts uvicorn and opens a browser tab at `http://127.0.0.1:8000`. Useful flags: `--port N`, `--no-browser`, `--reload` (dev auto-restart). Alternatively, from the `web/` directory: `uvicorn backend:app --reload`.

For first-run setup, see the [NutriMagnus User Manual](user-manual.html).

---

## Menu Structure

numa has five top-level nav areas: **Foods**, **Recipes**, **Meals & Log**, **Analysis**, and **Settings**. Analysis is a growing collection of preset analyses — currently **Daily summary - DCP and goals** (the original per-day nutrient/RDA workflow) and **Food use in meals** (frequency of food use across a chosen set of date ranges and/or meal IDs). For a complete description of every page and workflow, see the [NutriMagnus User Manual](user-manual.html).

---

## Usage Guide

### The local food cache

For user-facing documentation of the food cache — what gets stored, the quick-pick flow, and how to view or delete entries — see the [User Manual](user-manual.html).

**Overwrite protection for edited foods:** Once you edit a food's nutrients through Food Cache (or create a food manually), it is marked `user_drafted = True`. Any subsequent USDA fetch for the same food — triggered by selecting it from a search results table — will not overwrite a user-drafted entry. Your manual edits, AA patches, and custom notes are permanent unless you explicitly edit or delete them.

**Automatic omega fatty acid backfill:** When a cached USDA food is selected and its stored nutrients are missing all four omega keys (`omega3_ala_mg`, `omega3_epa_mg`, `omega3_dha_mg`, `omega6_la_mg`), the program silently fetches and merges just those nutrients from the USDA API and updates the cache entry. This happens transparently on first use; subsequent accesses use the updated cache. User-drafted foods are never touched by this backfill.

---

### Food annotations (GI and DIAAS estimates)

The `food_annotations` table stores user-supplied estimates attached to individual cached foods by `fdc_id` (fields: `gi_estimate`, `diaas_estimate`, `prep_context`, `gi_no_prompt`, `diaas_no_prompt`). See the [User Manual](user-manual.html) for the annotation workflow.

**Prompt on first add:** `web/backend.py:_gi_prompt_needed()` fires the first time a food is added to the Pantry (single-add path) or to a meal, if that food has no `gi_estimate` on file and `gi_no_prompt` isn't set. `/pantry/add` and `/meal/{id}/add` redirect to `/food/annotate/{fdc_id}?next=...` when a prompt is warranted; the annotate page offers "Skip for now" (no DB write, redirects to `next`) vs. "Skip forever for this food" (POSTs to `/food/annotate/{fdc_id}/skip-forever`, which sets `gi_no_prompt=1` via `upsert_food_annotation` without touching other fields). `diaas_no_prompt` exists in the schema but is not currently wired into any add flow.

**Seeding GI values in bulk:** `import_gi_seed.py` (repo root) writes `gi_estimate` for cached foods whose name exactly matches an entry in a small hardcoded table sourced from Foster-Powell/Holt/Brand-Miller (2008) *Diabetes Care* 31(12):2281-3 (CC-licensed, ~60 common foods). Ambiguous/fuzzy matches are printed for manual review rather than written automatically — see the script's docstring. Run with `--apply` to write; without it, it's a dry run.

**Visibility columns:** The **Ann** column in search result tables (`GI`, `DI`, or `GI DI` in green) and the `AA`/`GI`/`DIAAS` columns in the cached food list are driven by joins against `food_annotations` keyed on `fdc_id`.

---

### Data model: cache, drafted foods, and pantry

These three lists are related but distinct. Understanding the relationship prevents confusion when editing or annotating a food.

**One source of truth — the `foods` table (the cache).**

Every food — USDA, Open Food Facts, or user-created — is a row in the `foods` SQLite table, uniquely identified by `fdc_id`. That row holds the name, serving metadata, `nutrients_json`, and a `user_drafted` flag.

| View | What it shows | Underlying table |
|------|--------------|-----------------|
| Food Cache (Foods → 6) | All rows in `foods` | `foods` |
| Drafted Food Profiles (Foods → 8) | Rows where `user_drafted = 1` | `foods` (filtered) |
| My Pantry (Foods → 7) | Pantry entries, each optionally FK'd to `foods` | `pantry` |

**Food Cache vs Drafted Food Profiles:** The "Drafted Food Profiles" list is a filtered view of the same `foods` table — `WHERE user_drafted = 1`. A food becomes `user_drafted = True` when you create it manually or when you edit its nutrients through Food Cache. Editing a food in Food Cache immediately affects what Drafted Food Profiles shows, and vice versa, because they are the same row.

`user_drafted = True` also activates overwrite protection: all code paths that write a fresh USDA fetch result to the cache check this flag first and skip the write if it is set. This means manual AA patches, serving-size corrections, and other edits survive repeated searches for the same food.

**Pantry:** The `pantry` table has its own `id` (autoincrement), a `food_name` text field, and a nullable `fdc_id` FK pointing into `foods`. A pantry entry can exist without a cache entry (name-only). When `fdc_id` is set, all nutrient calculations use the live `foods` row — so editing that food in Food Cache instantly updates any pantry-based analysis. However, the pantry stores its own `food_name` string; renaming a cached food does not update the pantry display name.

**Annotations:** The `food_annotations` table is keyed by `fdc_id` and foreign-keyed to `foods` (`ON DELETE CASCADE`). Annotations are visible everywhere that food appears — search results, cache list, analyses — because they are always looked up by `fdc_id`.

**Editing rule:** All nutrient editing goes through **Food Cache** (Foods → 6). Both the Drafted Food Profiles menu and the Pantry menu redirect there for edits and display a notice to that effect. This keeps a single edit path regardless of how you reached the food.

---

### Drafted food profiles (user-modified nutrients)

Drafted profiles let you store custom nutrient values for any food. They are saved into the food cache with a small negative `fdc_id` (−1, −2, −3…), displayed as `usr` in tables, and flagged `user_drafted = True` so USDA re-fetches never overwrite them. They appear at the top of search results and are usable anywhere a regular cached food is. See the [User Manual](user-manual.html) for the creation workflow.

#### Supplement / unit-based mode

Vitamins, minerals, and other supplement tablets are sold in per-tablet amounts, not per-100g amounts. Supplement mode solves this: by treating 1 tablet as equivalent to 100g internally, the stored per-100g values exactly equal the per-tablet label values. No weighing is required.

**Creating a supplement:** When you answer yes to "Is this a supplement?", the program asks for the unit name (default: `tablet`; other common values: `capsule`, `softgel`, `pill`, `scoop`). Serving size and unit are set automatically (`1 tablet`). Enter nutrient values exactly as printed on the label — e.g., if the label says "Vitamin B12: 5000 mcg per tablet", enter `5000` at the Vitamin B12 prompt. When you later log "1 tablet" in a meal, those exact amounts are added to your nutrient totals.

**Editing an old entry to convert it to supplement mode:** Open the entry via **Drafted food profiles → 3. Edit**. If the entry is user-drafted and not already in supplement mode, the program asks "Is this a supplement?" at the start of the edit session. Answer yes and confirm the unit name — the gram_weight=100 portion is added automatically, preserving any nutrient values you already entered.

**IU input for vitamins A, D, and E:**
Many US supplement labels express these vitamins in International Units. At those prompts, enter the number followed by `IU` (e.g. `400 IU` or `5000iu`). The program converts automatically:
- Vitamin A: 1 IU = 0.3 mcg RAE
- Vitamin D: 1 IU = 0.025 mcg
- Vitamin E (natural d-alpha-tocopherol): 1 IU = 0.67 mg

The conversion math is shown on screen so you can verify it against the label.

---

### Searching for a food

See the [User Manual](user-manual.html) for usage documentation on food search, barcode scanning, and the food cache quick-pick.

**Result ordering.** See `numa_app/services/search_ranking.py`. `relevance_key(name, query, source, data_type)` returns a sort tuple, lower sorts first:

```python
(-count, -mask, SOURCE_RANK.get(source, 9), DATA_TYPE_RANK.get(data_type, 1), exact, prefix, len(name), name)
```

- `count` — how many query words appear in the candidate's name (substring, case-insensitive). This is the dominant term: an all-words match always outranks an all-but-one match, which always outranks an all-but-two match, and so on.
- `mask` — a bitmask, one bit per query word, MSB = the *first* word typed. Within an equal `count`, comparing masks as integers means matching earlier query words outranks matching later ones: for the query `milk dry instant` (bit weights 4/2/1), a name matching `milk`+`dry` scores `110₂ = 6`, one matching `milk`+`instant` scores `101₂ = 5` — so the "dry" hit wins even though both matched exactly 2 of 3 words, because the user typed "dry" before "instant". This is a compact way to encode "word order signals priority" without hand-written tiering logic.
- `SOURCE_RANK` (`pantry`→0, `cache`→1, `recipe`→2, `usda`/`off`→3) — the *only* place source enters the comparison, and only once `count` and `mask` are already tied. This is what fixes the previous behavior where a weak or coincidental pantry/cache match could outrank a much better USDA/OFF result simply by virtue of already being in the user's own data.
- `DATA_TYPE_RANK` (`Foundation`/`SR Legacy`→0, `Survey (FNDDS)`/`Experimental`→1, `Branded`/`Open Food Facts`→2) — breaks ties among results that are otherwise identical on text relevance and source. Without this, a wall of near-identical branded product names (e.g. a dozen listings all named "INSTANT NONFAT DRY MILK") can bury the one Foundation/SR Legacy food that actually carries amino acid data, since the remaining tiebreakers (below) have no way to prefer it — a longer, more descriptive USDA reference name loses to a terse branded one on `len(name)` alone. This restores the property the original "search deeper into Foundation/SR Legacy" boost pass (see `get_search_boost_page_size()`) was designed to provide by list position, before `relevance_key` started re-sorting its output.
- `exact`, `prefix`, `len(name)`, `name` — final tiebreakers: exact string match, then prefix match, then shorter name, then alphabetical.

The web app additionally offers a "Pantry, Cache, then Other" sort mode (`_sort_search_results()` in `web/backend.py`) that sorts by `SOURCE_RANK` *before* `relevance_key`, for users who deliberately want their own library first regardless of match quality. "Best match to name" (the default) uses `relevance_key` as shown above, with source only as the final tiebreaker.

The results table always includes an **AA data** column (✓ confirmed / ~✓ likely / ✗ none) and an **Ann** column showing which foods have GI and/or DIAAS estimates saved (`GI`, `DI`, or `GI DI` in green; `·····` if none). Use these columns to pick the option with the richest existing data before committing to a fetch.

After viewing the full nutrient breakdown, the program now offers to immediately proceed to portion analysis for the same food — saving you from navigating back to "Analyze a food portion".

#### Too many branded results?

The USDA database contains many packaged/branded food entries. A simple search like "pinto beans" will often return 25 branded products (canned goods, mixes, etc.) rather than the plain cooked food you want.

For home-cooked or generic foods, add descriptive terms to narrow the results:

| Instead of… | Try… |
|---|---|
| `pinto beans` | `pinto beans cooked` |
| `chicken` | `chicken breast cooked` |
| `rice` | `brown rice cooked usda` |
| `oats` | `oats rolled raw usda` |

Adding **`cooked`** or **`raw`** targets the USDA Foundation Foods and SR Legacy datasets, which cover whole foods with full nutrient profiles (including amino acid data for protein completeness). Adding **`usda`** further filters toward those non-branded entries.

The program will display a tip automatically when most of your search results are branded products.

### Analyzing a portion

See [Appendix J of the User Manual](user-manual.html#portion-formats) for the full list of accepted portion formats.

**Pieces vs. weight (implementation note):** A bare number (e.g. `2`) is treated as pieces/count — no gram weight is recorded and the ingredient's nutritional contribution is zero in recipe/meal totals. To store a gram weight, the user must always include a unit. This distinction is enforced in `_parse_portion_input()` in `numa_app/services/portions.py`.

Nutrient values are stored per 100 g in the cache; all displayed values are scaled proportionally from that reference.

### Analyzing a recipe portion

See the [User Manual](user-manual.html) for usage documentation. Internally, the recipe's stored total-weight/total-volume fields plus the per-ingredient gram amounts are summed and scaled by the requested serving fraction.

### Protein completeness

Wherever protein is analyzed (food, recipe, or meal), numa checks whether all nine essential amino acids meet FAO/WHO reference levels. See the [User Manual](user-manual.html) for output interpretation; see [Appendix B of the User Manual](user-manual.html#appendix-b) for the theory behind FAO reference values and DIAAS.

#### No amino acid data — building a user-drafted profile from literature

When no database (USDA or Open Food Facts) provides amino acid data for a food, you can build a hand-crafted nutrient profile from a literature search and store it in the local cache via **Foods → 7. User-drafted food profiles → 2. Create new user-drafted profile**.

**Workflow:**

1. Choose to start from a USDA food (pre-fills all available nutrients — you override only the AA fields) or from scratch.
2. Enter the food name. Answer "no" to the supplement question (this is a whole food).
3. Enter the serving size and unit.
4. Step through macros, then optionally minerals, then optionally vitamins.
5. Choose how to enter the amino acid profile:
   - **1 — one-by-one (g per 100g food):** step through each essential amino acid individually; all are optional.
   - **2 — bulk import (g per 100g protein):** paste or type a list of `name: value` pairs (e.g. `lysine: 4.8`); values are automatically converted to g per 100g food using the protein content you entered in step 3. Accepts full names, 3-letter codes (e.g. `lys`), and 1-letter codes (e.g. `K`). Non-essential amino acids are silently discarded; unrecognized names are flagged. A summary shows stored values with the conversion math.
   - **n — skip:** no amino acid data will be stored.
6. Enter a **Note** documenting your source (e.g., *"AA profile from Sarwar et al. 1985, J. Food Sci. 50(2)"*). This is the field for source attribution.
7. The profile is saved with a negative fdc_id and `data_type = "User Drafted"`. It is immediately available as a food in all search, meal, and recipe flows.

User-drafted profiles can be edited at any time (**User-drafted food profiles → 3. Edit**) and are listed with their notes in the user-drafted profiles table so the source is always visible. Deleting a user-drafted profile removes it from the cache permanently.

**Copying a cached food as a draft — Foods → 7. User-drafted food profiles → 5. Copy a cached food as draft**

This option copies any food already in the local cache — whether a USDA food, an Open Food Facts product, or an existing user-drafted profile — into a new editable draft. The workflow:

1. Search the cache by name and pick the food to copy by ID.
2. Confirm or edit the name (defaults to "Copy of …"), serving size, and serving unit.
3. Step through all nutrient values pre-filled from the original — change only what you want.
4. Edit or keep the note field, then save.

The copy is saved as a fresh user-drafted entry with a new negative ID, completely independent of the original. Any subsequent edits to either the original or the copy do not affect the other. This is useful for modeling variations of a food (different cooking method, fortification, preparation) while retaining the original cached entry unchanged.

**Note field:** Every food in the cache has a `notes TEXT` column. For user-drafted profiles this is the right place to record citation, confidence level, or any caveat about the data.

#### No amino acid data — USDA suggestion

Some USDA entries — particularly SR Legacy and Branded foods — omit amino acid data. If the selected food has none, numa will display:

```
(No amino acid data available for protein completeness analysis.)
```

and immediately offer to search **Foundation Foods** for an equivalent entry. Foundation Foods is USDA's most curated dataset and almost always includes a full amino acid profile. The search is pre-filled with the first keyword(s) of the original food name (e.g., "beans, pinto, mature seeds, cooked, boiled, with salt" becomes "beans"). You can accept the suggestion, refine the query if needed, and pick from the Foundation results without leaving the current flow.

#### No amino acid data — the Claude fetch workflow

When no Foundation Foods substitute is available, numa provides a two-step workflow, backed by `numa_app/services/claude_fetch.py`, to retrieve amino acid (and other nutrient) data from Claude AI (claude.ai) and import it directly into the cache.

**Access** — Food Cache: check the boxes next to foods showing the uncertain/missing AA badge (or "Select all missing AA data"), then click **Fetch missing data from Claude AI**.

**Step 1 — prompt generation (`claude_fetch.build_prompt()`).**

Builds a prompt from the selected foods and shows it on its own page with a **Copy prompt to clipboard** button. The prompt instructs Claude to return one fenced JSON block per food containing:

- **Metadata keys**: `name`, `fdc_id`, `fdc_type`, `source`, `confidence_note`
- **Nutrient keys**: all recognized fields (macros, minerals, vitamins, phytonutrients, and all 11 amino acids), per 100 g edible portion

Key rules embedded in the prompt: amino acid values must be in grams per 100 g food (not per g protein, not mg); `aa_methionine_g`/`aa_cystine_g` and `aa_phenylalanine_g`/`aa_tyrosine_g` must always be separate keys; unknown values must be omitted entirely (never zero-filled); true zeros may be included explicitly; source hierarchy is USDA FDC → SR Legacy → peer-reviewed literature → estimate.

The page instructs the user to open a **new** claude.ai chat, paste the prompt and send, then copy Claude's entire reply back into NuMa's **Import Claude response** page.

**Step 2 — response import (`claude_fetch.parse_response()` / `validate_all()`).**

`parse_response()` extracts fenced (` ```json ``` `) and bare JSON objects from the pasted reply. Any non-JSON text trailing the last JSON block is collected as **curator text** — Claude's methodological caveats, confidence statements, and batch-level notes.

Each block is validated by `validate_block()`: it must have `name` (string), `fdc_id` (integer or integer-string), and a valid `fdc_type`; unrecognized nutrient keys are stripped silently; blocks that fail validation are reported and skipped.

Passing blocks are shown in a review table — name, FDC ID, calories, protein, and AA count out of 11 — before the user clicks **Import**. On confirmation, each food is written via `_db.cache_food()` (through `claude_fetch.import_foods()`) with:
- `notes` — formatted from `source` and `confidence_note`
- `curator_notes` — the batch-level curator text
- `user_drafted` **not set** — entries remain overwritable by subsequent USDA re-fetches (omega backfill, incomplete-cache detection)

Import doesn't require the foods to be pre-existing cache entries — `validate_block()` only needs `name` and `fdc_id`, so a hand-pasted response (skipping Step 1 entirely) can introduce a brand-new food, e.g. a packaged product keyed by its UPC.

**Per-serving input (`numa_app/services/food_import.py`).** Nutrient values normally must already be per-100g. As an alternative, a block may give `serving_size_g` + `nutrition_per_serving` (same key names as the flat shape); `validate_block()` runs these through `food_import.convert_per_serving()` (scales by `100 / serving_size_g`) before merging into `nutrients`, and appends the conversion factor to the food's notes. `food_import.VALID_NUTRIENT_KEYS` (derived from `usda_api.NUTRIENT_MAP`, so it can't drift from the nutrients numa actually understands) and `food_import.validate_and_strip()` are the single shared implementation of key validation/stripping — `claude_fetch.py`, `import_foods.py`, and `import_json_folder.py` all import from this module rather than keeping their own copies.

#### No amino acid data — `import_foods.py` (scripted alternative)

For stable, literature-sourced food records that need to survive repeated numa updates, `import_foods.py` is a standalone Python script that bypasses the interactive workflow. Food dicts are hardcoded in its `_FOODS` list (one per food, with the same nutrient key conventions as the Claude prompt template — including the `serving_size_g`/`nutrition_per_serving` alternate shape). Running the script imports all entries via `cache_food(..., user_drafted=True)`.

The `user_drafted=True` flag is the critical difference from the Claude import path: it prevents USDA re-fetches from overwriting the imported data. Without it, the omega backfill or incomplete-cache detection paths in `_fetch_food_from_result` can silently replace a manually curated entry with raw USDA data (which for Branded foods typically lacks amino acids). Re-running the script is always safe — `cache_food()` uses `INSERT OR REPLACE`, so existing entries are updated in place.

The script does not include portion data; `portions_json` is stored as an empty array `[]` via `json.dumps(portions or [])`.

#### `import_json_folder.py` — one-file-per-food drop folder

A third, lower-ceremony import path for a single food: save one JSON file per food into `food_imports/` (created on first run; gitignored) using the same block shape as a Claude-response entry (`name`, `fdc_id`, `fdc_type`, optional `source`/`confidence_note`, plus either flat per-100g nutrient keys or `serving_size_g`/`nutrition_per_serving`). Running `python import_json_folder.py` validates every file via the same `food_import.validate_and_strip()`/`convert_per_serving()` functions, prints a one-line summary per food, asks a single `y/N` confirmation, writes all of them via `cache_food(..., user_drafted=True)` in one `with _db.get_db()` block, then moves each processed file into `food_imports/imported/` — re-running is still safe (`INSERT OR REPLACE`) even if a file were left in place or reintroduced.

### Protein digestibility — DIAAS

Wherever a food is analyzed (search, portion analysis, recipe, or meal), numa automatically displays a **Bioavailability** section if it has data for that food. This section reports two things: the DIAAS score and any anti-nutrient advisories (see next section).

For background on the DIAAS scoring methodology and score interpretation, see [Appendix B of the User Manual](user-manual.html#appendix-b).

#### What numa displays

When a DIAAS score is known for the selected food, the **Bioavailability** section shows:

```
  Bioavailability
  Protein digestibility (DIAAS): 0.75  ███████████████░░░░░
  Digestible protein: 11.3g  (raw: 15.0g)
  Note: Mineral absorption problem — phytates are present
      * Best reduction: soak or sprout before cooking
      * Moderate reduction: roasting
```

The bar and color indicate digestibility quality — green (≥ 0.90), yellow (≥ 0.70), red (< 0.70). The **Digestible protein** figure is simply `raw protein × DIAAS score` and represents what the body can realistically use.

**Anti-nutrient notes** appear below the DIAAS line when relevant. Each note names the problem category (e.g. *Mineral absorption problem*, *Digestibility problem*, *Vitamin bioavailability problem*), states the specific cause, and lists solutions as bullet points ordered by effectiveness. If a food matches multiple rules with the same underlying issue (e.g. a USDA food named "Beans, snap, seeds, mature" matching both the legume and nut/seed phytate rules), they are consolidated into a single note with all solutions listed.

If the food is not in the DIAAS lookup table, this line is omitted silently — it does not mean the food has poor digestibility, only that no lookup entry exists for it.

#### How DIAAS values are sourced

DIAAS scores are not available from any API — they come from controlled digestion studies conducted in laboratory settings. numa uses a static lookup table of ~60 common food categories, built from FAO 2013 reference values and peer-reviewed studies (principally Mathai et al. 2017, *Br J Nutr*; Gorissen et al. 2018, *Amino Acids*). The lookup uses keyword matching on the food name (case-insensitive, first match wins). More specific entries appear before general ones in the table so that, e.g., "chickpea pasta" resolves to the chickpea score (0.83) rather than the generic pasta/wheat score (0.46).

**Notable entries:** Collagen and gelatin are scored at 0.04 — effectively zero — because tryptophan is essentially absent from these proteins. Without this entry, collagen powder added to a recipe would be silently treated as fully digestible, substantially inflating the displayed digestible protein figure.

**Lookup is not cached.** The keyword scan takes microseconds and is repeated on each analysis. USDA nutrient data (macros, minerals, vitamins, amino acids) is cached in the `foods` table after first fetch and never re-fetched unless you delete the cache entry. DIAAS scores, by contrast, are derived from the food name at runtime and are not written back to the database.

**Per-food DIAAS via annotations.** If you have a primary-literature DIAAS value for a specific food, you can save it via **Foods → Annotate a cached food** or the inline prompt during analysis. A saved annotation in `food_annotations.diaas_estimate` takes priority over the keyword table for that food. This is the only path to storing a DIAAS value per-food in the database.

This same saved-value-takes-priority rule applies to the DIAAS column shown in the web app's Food Cache and My Pantry list views (`food_cache.html`, `pantry.html`): a saved annotation is marked with ★, otherwise the list falls back to the keyword-table value when the food has amino acid data.

### Meal-level DIAAS analysis

Analyzing a meal or daily summary now shows a deeper **Meal-level DIAAS Analysis** section, computed by `diaas.py`, that goes beyond the per-food scores described above.

For the rationale behind meal-level pooling, see the [User Manual](user-manual.html).

#### The calculation

For each ingredient:

1. Look up the food's true ileal digestibility coefficient (0–1) — not the same as DIAAS. This is the fraction of each amino acid that is actually absorbed in the small intestine.
2. Multiply each essential amino acid (IAA) amount by that digestibility factor to get **digestible IAA grams**.

Then across all ingredients:

3. Pool the digestible IAA grams for each of the nine essential amino acids.
4. Divide each pooled total by the FAO 2013 adult reference (mg/g protein) applied to the meal's total protein.
5. The composite DIAAS is the ratio of the most limiting IAA. **Digestible complete protein** = protein from AA-analyzed ingredients × min(composite DIAAS, 1.0), **capped** at the digestibility-weighted absorbed protein from those same ingredients (`aa_dig_protein_g` in `diaas.py`) — the raw multiplication can otherwise project more complete protein than was physically absorbed, when the limiting amino acid is concentrated in a higher-digestibility ingredient than the meal's average. See [DCP cap](user-manual.html#dcp-cap) for the full worked example.

This is the methodology from FAO Food and Nutrition Paper 92 (2013).

For an annotated example of the meal-level DIAAS output table, see the [User Manual](user-manual.html). Note: if tyrosine data is absent (not tracked before April 2026; re-fetch the food to get it), the Phe+Tyr row is flagged as a gap.

#### Filling missing AA profiles at analysis time

When a meal has ingredients without AA data, the analysis reports how many are affected and distinguishes two categories:

- **Inside a recipe** — the ingredient is part of a recipe logged as a meal item. To fix these, edit the recipe directly (Recipes → browse → edit ingredients) and replace or re-fetch the ingredient there.
- **Standalone meal ingredients** — foods logged directly to the meal (not inside a recipe). These can be replaced interactively: the program offers a `y/n` prompt asking whether to search for a substitute.

If you answer `y`, for each affected standalone ingredient the program runs a focused search of USDA **SR Legacy** and **Foundation** foods — the datasets most likely to include full amino acid profiles. The **AA** column in the results table (✓/✗) shows at a glance which candidates have AA data. Picking a replacement updates that ingredient in the meal for the current analysis session. Press Enter to skip an ingredient and leave it excluded from IAA pooling.

Ingredients contributing less than 1 g of protein are treated as negligible and left off all of these missing-AA lists and digestibility tables — a footnote notes when items were omitted this way. This keeps garnishes, spices, and trace amounts (e.g. a square of dark chocolate) from cluttering warnings that matter only for real protein sources.

#### Why the "Fetching amino acid data…" spinner can be slow

When meal analysis begins, `_compute_meal_ingredient_list()` (`meals.py:610`) loops over every food in the meal and calls `_best_nutrients()` for each one. Inside `_best_nutrients()`, `_refresh_cache_if_missing_aa()` checks whether the cached food has amino acid data. If it does not — and the food is Foundation or SR Legacy (i.e. USDA *should* have AA data) — it makes a synchronous USDA API call to re-fetch the full nutrient profile and update the cache.

The result is one sequential HTTP round-trip per ingredient that lacks cached AA data. For a meal with six foods where four were cached without AA data (common for foods first added via a quick text search), that is four back-to-back network requests, each potentially taking 1–3 seconds. After the first analysis the AA data is stored in the local cache, so subsequent analyses of the same meal are fast. The spinner is a one-time fetch-and-cache cost per food.

#### Digestibility data — three-tier lookup

For each food, the digestibility coefficient is resolved in order:

1. **User override** — an exact food-name entry you set in Settings → Advanced settings → Protein digestibility overrides. Takes precedence over everything else.
2. **Curated table** (~50 entries in `diaas.py`) — literature-sourced values for specific foods and categories, with citations. Covers all common plant proteins.
3. **Category default** — broad averages when no specific match is found (isolated plant protein: 0.92, legume: 0.80, seed: 0.82, nut: 0.78, grain/cereal: 0.82, animal: 0.96). The source description shows `~est` in the output.
4. **Overall default: 0.82** — if nothing matches, a conservative plant-protein average is used.

The source of each digestibility value is shown in the ingredient table. Estimated values are also listed in a footnote.

#### Protein digestibility overrides

**Settings → Advanced settings → Protein digestibility overrides** lets you set a specific digestibility coefficient for any food you have found a primary-literature value for. This is a power-user feature — the curated table covers most common plant proteins and the category defaults are defensible estimates. Overrides are stored in the `diaas_overrides` table and survive across sessions. The interface shows you what value numa would use without the override before asking for your input.

### Protein complement suggestions

Wherever protein is analyzed, numa checks for essential amino acid gaps and offers complement suggestions. See the [User Manual](user-manual.html) for the user-facing workflow.

**Suggestion sources — three tiers (in order):**
1. **Pantry** — foods from My Pantry that close the gap; ranked by gaps closed then smallest required amount (up to 3 per page).
2. **General table** — a curated built-in table of common plant protein sources (protein + nine EAAs only; not usable in search/recipes).
3. The user can page through both lists interactively.

**Scoring formula for total DCP:** `(base_protein + complement_protein) × min(1.0, base_digestibility × new_pool_raw_min)`, where `new_pool_raw_min` is the minimum raw AA score (vs. FAO reference) across all essential amino acids in the combined pool. For DIAAS-improver suggestions: `(base_protein + raw) × min(1.0, new_diaas)` — sourced directly from `suggest_complements()` in `usda_nutrients.py`.

A complement that closes the primary gap but dilutes a different amino acid will show a lower total DCP — the pooled DIAAS drops because the new limiting AA is weaker than the base alone. A qualifying complement must bring the most limiting AA to exactly 1.0 (the FAO floor) in a practical serving (≤ 500 g).

### Dietary preferences

**Settings → Dietary preferences** controls which protein sources appear in complement suggestions. See the [User Manual](user-manual.html) for the three options. The setting is saved to `~/.config/numa/prefs.json` (key: `diet_pref`) and applied to both interactive complement suggestions and exported reports.

### Building a recipe

See the [User Manual](user-manual.html) for the recipe creation and editing workflow.

### Copying a recipe

See the [User Manual](user-manual.html). DCP is not copied — it is recalculated the first time you analyze the new recipe.

### Logging a meal

See the [User Manual](user-manual.html) for the meal logging workflow.

### Saved nutrition reports

Reports are auto-saved to `~/.numa/reports/` after every analysis. Additional user-exported copies (md/txt/html) go to `~/.numa/user-requested-nutrition-reports/`. See the [User Manual](user-manual.html) for the full workflow.

**Diet preference in exports:** Exported reports filter complement suggestion sections by the active dietary preference. Implemented by passing `diet_pref=state._diet_pref` to `export.build_report()` from `reports._offer_export()`. The `build_report(title, sections, fmt, diet_pref="all")` signature accepts the preference and overrides the static `complement_suggestions` renderer for that call.

### Daily summary

See the [User Manual](user-manual.html) for usage.

---

## Architecture

### Overview — module split

`usda.py` is a thin re-export shim. All code that does `import usda as _usda` continues to work unchanged. The actual implementation lives in two files that can each be read and edited independently:

- **`usda_api.py`** — HTTP client: API key management, `search_foods()`, `get_food_detail()`, `_parse_food()`, and the `NUTRIENT_MAP` / `ESSENTIAL_AMINO_ACIDS` / `AA_REFERENCE_MG_PER_G_PROTEIN` constants.
- **`usda_nutrients.py`** — all nutrient math: `scale_nutrients()`, `sum_nutrients()`, `has_amino_acid_data()`, `protein_completeness()`, `get_aa_gaps()`, `suggest_complements()`, `get_diaas()`, `get_antinutrient_flags()`, `get_density_g_per_ml()`, and the embedded DIAAS, anti-nutrient, and complement data tables.

The support modules (`db.py`, `usda.py`, `diaas.py`, `export.py`, `profile.py`) live at the project root and are imported by `numa_app/services/*` and `web/backend.py` as needed.

### `openfoodfacts.py` — Open Food Facts API client

`search_foods(query, page_size=8)` — searches the OFF REST API (no key required). Returns result dicts in the same format as `usda.search_foods()`, tagged with `_from_off=True` and `_off_data` (the full product record). Fails silently on network errors so a slow or unavailable OFF server never breaks USDA searches.

`get_food_detail(off_result)` — builds a full nutrient dict from the already-present `_off_data` in the search result. No second HTTP call needed.

`off_id(barcode)` — converts an EAN/UPC barcode string to a deterministic negative integer fdc_id in the range −2,000,000,000 to −3,000,000,000. This keeps OFF IDs well separated from USDA IDs (positive) and user-drafted IDs (−1, −2, −3, …).

OFF nutrient keys (`energy-kcal_100g`, `proteins_100g`, etc.) are mapped to the program's internal keys. Mineral values (sodium, calcium, iron, etc.) are converted from grams (OFF convention) to milligrams (program convention) by multiplying by 1000. Amino acid data is not available from OFF.

### `numa_app/services/portions.py` — portion parsing

`_parse_portion_input(raw, portions, food_name)` parses a portion string and returns `(grams, label)`. Accepted formats:

- **Bare number** (e.g. `2`) → pieces/count: returns `(0.0, "2 pc")`. No gram weight.
- **Piece unit** (`pc`, `pcs`, `piece`, `pieces`, `each`, `ea`, `count`, `ct`, `item`, `items`) → same as bare number.
- **Weight** (`150 g`, `3 oz`, `0.5 lb`, fractions, mixed numbers) → grams.
- **Volume** (`1/4 cup`, `2 tbsp`, `1 tsp`, `ml`) → grams via food density.
- **USDA portion shortcut** (`p1`, `p2`) → gram weight from USDA portions list.
- **Portion multiple** (`1.5 p1`) → multiple of a USDA portion.

Returns `None` on unrecognized input; `(None, vol_display)` when volume is recognized but density is unavailable (caller then prompts for grams). `_PIECE_UNITS` is a frozenset of the recognized piece-unit words. `volume_hint()` and `amount_note()` (also in this file) render a cups/tbsp/tsp approximation for a gram amount, used by complement suggestions and elsewhere. `web/backend.py` builds its own portion-picker UI around `_parse_portion_input()` directly; the interactive CLI equivalent (`_pick_portion()`) was removed with the CLI.

**`numa_app/services/aa_estimate.py` — AA copy/estimate:** manually typing or pasting a food's amino acid profile is slow, and copying another food's raw AA grams verbatim silently misestimates whenever the two foods' protein density differs (a food with 2× the protein would otherwise look 2× more complete than it really is). `estimate_aa(target_nutrients, source_nutrients) -> (updated, factor, error)` scales every `usda.ALL_AMINO_ACIDS` key present in `source_nutrients` by `target_protein_g / source_protein_g` before writing it onto a copy of `target_nutrients`; returns an `error` string instead if the source lacks amino acid data (`usda.has_amino_acid_data()`) or either food has no usable `protein_g`. `source_note(name, fdc_id, factor)` renders the "AA data estimated by scaling from X (#id), factor N.NNx, DATE" string used to auto-suggest a Note. `usda.ALL_AMINO_ACIDS` (in `usda_api.py`, re-exported via `usda.py`) is `ESSENTIAL_AMINO_ACIDS` plus `aa_cystine_g`/`aa_tyrosine_g` — the full trackable AA set, as distinct from the 9-key essential set used for completeness scoring. Entry point: an inline picker on `food_custom_edit.html` (search your Food Cache, "Use as source" button) posting to `POST /food/custom-profiles/{fdc_id}/copy-aa` (`web/backend.py`), which fetches-and-caches the source if it isn't cached yet, applies `estimate_aa()`, and redirects back with an `aa_applied` status flag.

### `db.py` — SQLite database

All persistence goes through a `get_db()` context manager that commits on clean exit and rolls back on exception. The database path is `~/.local/share/numa/numa.db`.

**Schema migrations run automatically at startup**: `web/backend.py`'s FastAPI `lifespan` handler (`_lifespan()`, wraps `app = FastAPI(..., lifespan=_lifespan)`) calls `_db.init_db()` on web server startup, so the app is self-sufficient against a brand-new or un-migrated database (see `tests/test_web.py::test_web_app_self_migrates_without_cli`, a regression test from when a second process used to be relied on for this). `init_db()` is idempotent (every migration step is a guarded `ALTER TABLE ... ADD COLUMN` or `CREATE TABLE IF NOT EXISTS`), so it's always safe and cheap to call.

**Schema:**

| Table                | Purpose                                              |
|----------------------|------------------------------------------------------|
| `foods`              | Local cache of USDA food entries (nutrients as JSON) |
| `recipes`            | Recipe metadata (name, servings, description, total volume, total weight, `dcp_g`, `last_accessed_at`) |
| `recipe_ingredients` | One row per ingredient; foreign key to `recipes`     |
| `meals`              | Meal log entries with date                           |
| `meal_items`         | Foods or recipes added to a meal; foreign key to `meals` |
| `pantry`             | User's protein-source inventory (food name, optional fdc_id, notes) |
| `food_annotations`   | Per-food user-supplied estimates (GI, DIAAS, prep context), keyed by fdc_id; also stores `gi_no_prompt` / `diaas_no_prompt` suppression flags |
| `diaas_overrides`    | User-set true ileal digestibility coefficients, keyed by food name (used by meal-level DIAAS in `diaas.py`; distinct from per-food annotations above) |

`recipes.total_volume` / `recipes.total_volume_unit` and `recipes.total_weight` / `recipes.total_weight_unit` store the user-entered batch size (e.g. 4.0 / "cups", 800.0 / "g"). Both pairs are nullable — either or both may be omitted. Added via `ALTER TABLE` migration so existing databases are upgraded automatically on first run.

`recipes.dcp_g` stores the digestible complete protein **per serving**, kept in sync automatically: `numa_app/services/recipe_dcp.py`'s `recompute_recipe_dcp()` recomputes and persists it after any recipe or ingredient edit (`web/backend.py` recipe/ingredient POST routes), and `db.py`'s mutating recipe functions (`recipe_update`, `recipe_add/update/remove_ingredient`) clear it to `NULL` as a fallback in case some caller doesn't. It is `NULL` (shown as `NC` — not computed) when servings is 0, no ingredient has weight, or a *significant* protein-contributing ingredient (≥1 g protein) is missing amino acid data; a best-guess/approximate value is never persisted. Minor protein contributors missing amino acid data (<1 g protein — spices, oil, salt, a trace of chocolate) are excluded from the calculation rather than blocking it, regardless of how large a share of the recipe's (possibly small) total protein that 1 g represents — the gram floor is absolute, not relative to the recipe. The web app's "Compute DCP for all complete recipes" button (`/recipes/compute-bcp`) also calls this same function across every recipe, regardless of its `complete` flag.

**Food edits cascade the same way.** `recipe_dcp.py`'s `cascade_food_change(fdc_id, conn)` recomputes DCP for every recipe that uses a given food directly (via `db.recipes_containing_food()`), then cascades up through ancestors exactly as an in-recipe edit does. It's called after every write to `foods.nutrients_json` — the USDA "refresh" route, the custom-profile edit route, the AA-import ("estimate it from a similar food") route, and the various `cache_food()` re-cache call sites reachable from search/pantry/recipe/meal food-add flows (skipped only at the couple of call sites where the `fdc_id` is guaranteed brand-new, e.g. custom-profile create/copy, since nothing can reference it yet). Each affected recipe is recomputed independently — one failure doesn't block the rest of the cascade, or the food save that triggered it — it's logged to `recompute_errors` instead (see below) so it isn't silently lost.

**`recompute_errors` table** (`db.py`) records any cascade step that raises rather than letting a bare `except Exception: pass` swallow it. Columns: `entity_type`, `entity_id`, `message`, `occurred_at`, `resolved_at` (NULL = unresolved), `banner_ack_at` (NULL = not yet dismissed from the home-page banner). `db.log_recompute_error()` writes an entry; `list_unresolved_recompute_errors()` backs the Settings > System Issues list; `list_unacked_recompute_errors()` backs the home-page banner, silenced without resolving via `ack_recompute_errors_banner()` ("Got it, don't remind me again" — a fresh failure after that reappears in the banner). This is deliberately *not* used for expected non-computability (0 servings, missing AA data on a significant ingredient) — those already surface as `NC` in the UI and aren't errors.

The Settings-page action is **Retry**, not a plain dismiss: `web/backend.py`'s `settings_recompute_error_resolve()` looks up the entry via `db.get_recompute_error()`, calls `recipe_dcp.recompute_recipe_dcp()` for that entry's recipe, and only calls `resolve_recompute_error()` if that succeeds. A retry that raises again calls `db.update_recompute_error()` to refresh that same row's `message`/`occurred_at` (and re-arm the banner by clearing `banner_ack_at`) rather than resolving it or inserting a duplicate row — an entry can never disappear from the list while its underlying recipe is still broken, and retrying repeatedly doesn't pile up multiple rows for the same recipe. Re-editing the recipe directly (which triggers the same `recompute_recipe_dcp()` call through the normal recipe-edit path) has the same clearing effect the next time that recipe's cascade succeeds, without needing to click Retry at all.

`recipes.last_accessed_at` stores the ISO 8601 UTC timestamp of the last time the recipe was opened via any workflow action (view/edit/develop/analyze/copy). It is `NULL` for recipes that have never been accessed. Added via `ALTER TABLE` migration. Used by `recipe_list_recent()` to order the Browse view; falls back to `created_at` for recipes with no access timestamp.

**Key db functions:**

| Function | Purpose |
|---|---|
| `recipe_list(conn)` | All recipes ordered by name; includes `complete`, `last_accessed_at`, `total_weight`, `total_weight_unit` columns |
| `recipe_list_recent(conn, limit=20)` | Recipes ordered by `COALESCE(last_accessed_at, created_at) DESC` — powers the Browse recent view |
| `recipe_touch(conn, recipe_id)` | Sets `last_accessed_at = datetime('now')` for a recipe — called whenever a recipe is opened |
| `meal_add_recipe(conn, meal_id, recipe_id, recipe_name, servings, unit="servings")` | `unit` parameter now configurable (was hardcoded to "servings") |

All nutrient data is stored as a JSON blob in `foods.nutrients_json`, keyed by the same field names used throughout (`calories`, `protein_g`, `carbs_g`, etc.). This avoids schema migrations when nutrient tracking is expanded.

**Archiving (`archived` column):** `foods`, `pantry`, and `recipes` each carry an `archived INTEGER NOT NULL DEFAULT 0` column (added via the same `ALTER TABLE ... ADD COLUMN` migration idiom as the rest of the schema — see `init_db()`). Archiving is the "reserve area" mechanism: it lets a user hide a row from default use without deleting it or risking foreign-key integrity, which ruled out the alternative of a literal second database file (recipes reference `fdc_id`, meals reference `recipe_id`, etc. — a second DB would require cross-database copies or ATTACHed joins to keep those relationships intact).

- `list_cached_foods`, `search_cached_foods`, `pantry_list`, `recipe_list`, `recipe_list_recent` all take `include_archived: bool = False` — the default excludes archived rows, so every existing caller (including all of `web/backend.py`) got this filtering automatically without change.
- Single-row lookups (`get_cached_food`, `expand_recipe_ingredients` in `recipe_nutrients.py`) are never filtered — an archived food/recipe still resolves correctly wherever it's already referenced (an existing recipe ingredient, a logged meal item).
- `set_food_archived` / `set_pantry_archived` / `set_recipe_archived` flip the flag; callers reuse the current-state check as a toggle, so one route handles both archive and restore.
- `food_references(conn, fdc_id)` / `recipe_references(conn, recipe_id)` return reference counts (pantry/recipes/meals) so the UI can warn — but not block — before archiving something still in active use.
- `list_unused_cached_foods` / `prune_unused_cached_foods` always exclude archived rows: archiving is meant to protect data from being lost, so an archived-but-unreferenced food is never swept up by `u` (prune unused).
- Per-list "show archived" visibility is a session/persisted preference, not a query default — `numa_app/state.py`'s `AppContext.list_filters` dict (`get_list_filter`/`set_list_filter`) mirrors the existing `sort_prefs` pattern exactly, and `numa_app/config/prefs.py` persists it (`show_archived_food_cache`/`show_archived_pantry`/`show_archived_recipes` keys in `prefs.json`) the same way sort choices are persisted. Any future per-list view-state toggle should follow this same two-layer (state.py get/set + config/prefs.py persisted wrapper) pattern.
- `web/backend.py`'s `/food/cache`, `/pantry`, and `/recipes` GET routes accept a `show_archived` query param resolved via `_resolve_bool_pref()` (mirrors `_resolve_sort()`), and each has a `POST .../{{id}}/archive` route that flips the flag and redirects with `?archived=1`/`?restored=1` (plus `&still_used=1` when the item was still referenced) for a flash-banner message. The web flow archives immediately (one click, no JS-driven confirm dialog) and surfaces the "still referenced" warning as a post-action flash message instead of a pre-action prompt — a warn-but-never-block policy, matching the app's plain-HTML-forms architecture (no fetch/AJAX anywhere in `web/`).

### `usda_api.py` — USDA HTTP client (~290 lines)

**API:** USDA FoodData Central REST API (`https://api.nal.usda.gov/fdc/v1`). Uses stdlib `urllib` — no `requests` dependency at runtime.

`NUTRIENT_MAP` is a dict mapping USDA nutrient IDs (integers) to `(our_key, display_label, unit)` tuples. It covers 45 nutrients: macros, minerals, vitamins, 7 phytonutrients/bioactive compounds, and 11 amino acids (including tyrosine, added to support Phe+Tyr combined scoring in meal-level DIAAS). Also defines `ESSENTIAL_AMINO_ACIDS` (list of 9 internal keys) and `AA_REFERENCE_MG_PER_G_PROTEIN` (FAO 2013 reference pattern).

**Key functions:**

| Function | Purpose |
|---|---|
| `get_api_key()` / `set_api_key(key)` | Read/write API key from `~/.config/numa/config.json` |
| `search_foods(query, page_size=15, data_types=None)` | Search USDA; returns list of result dicts |
| `get_food_detail(fdc_id)` | Fetch full nutrient profile for one food |
| `get_search_boost_page_size()` / `set_search_boost_page_size(n)` | Read/write the result cap (default 25) for the Foundation/SR Legacy-only "boost" search — see below |

`_parse_food()` normalizes USDA API responses — the API returns nutrients in three different formats depending on the endpoint (`nutrientId`, `nutrient.id`, or `number`), and `_parse_food` handles all three.

`search_foods(query, page_size, data_types)`: `page_size=0` means no cap — it requests `_USDA_MAX_PAGE_SIZE` (200, USDA's own per-request ceiling) and returns every filtered match, skipping the normal `[:page_size]` truncation. For any unrestricted (`data_types=None`) search, USDA's own relevance ranking can bury plain/raw foods — the ones most likely to carry amino-acid data — well below branded or prepared-dish matches (e.g. "Potatoes, flesh and skin, raw" ranks ~20th for the query "potato", behind "Bread, potato" and several potato-chip variants). Every caller that does an unrestricted search (the Foods search page, the meal add-food panel, and a recipe's ingredient search) works around this with a second, explicit `data_types=["Foundation", "SR Legacy"]` pass merged in ahead of the general results; that pass's `page_size` is `get_search_boost_page_size()`, user-configurable via the Settings page's USDA API Key panel, `0` meaning no cap.

`_SEARCH_ALIASES` is a small static list of foods that the USDA search index fails to surface reliably (e.g., flaxseed, chia, hemp seed, oats). These are injected into every search result that matches the alias keywords.

### `usda_nutrients.py` — nutrient math and data tables (~890 lines)

Imports `NUTRIENT_MAP`, `ESSENTIAL_AMINO_ACIDS`, and `AA_REFERENCE_MG_PER_G_PROTEIN` from `usda_api`. The bulk of this file is three large static data tables (DIAAS, anti-nutrient, complement) with the functions that query them.

**Key functions:**

| Function | Purpose |
|---|---|
| `scale_nutrients(nutrients, amount, base_size=100)` | Scale a nutrient dict from base_size to amount |
| `sum_nutrients(*dicts)` | Add any number of nutrient dicts together |
| `protein_completeness(nutrients)` | Assess essential amino acid completeness vs. FAO/WHO reference. Requires 5+ AAs with **non-zero** values; zero-keyed AA entries (common in branded USDA foods) are ignored. |
| `get_aa_gaps(nutrients, digestibility=1.0)` | Return `(aa_key, score, deficit_g)` for each essential AA with digestibility-adjusted score below 0.95, sorted most-limiting first. The 0.95 threshold filters out near-adequate AAs (e.g. score 0.994) that would otherwise generate impractically small complement amounts. |
| `suggest_complements(base_nutrients, pantry_candidates, diet_pref="all", cache_candidates=None, exclude_names=None)` | Compute minimum-gram complement suggestions from pantry, the broader food cache, and the curated table; returns `{"pantry": [...], "general": [...]}`. `diet_pref` controls which curated-table entries are eligible: `"all"` includes everything, `"vegetarian"` includes only plant and dairy/egg entries (those flagged `dairy_egg=True` in `_COMPLEMENT_TABLE`), `"plant_only"` excludes all animal entries. The curated table holds protein + nine essential AAs per 100g for ~30 common protein sources; used only for complement scoring and AA gap augmentation — not for general food search. Any real candidate (pantry, recipe, or `cache_candidates` — real foods matched by name to a curated entry, built by callers via `complement_table_names()` + `db.search_cached_foods()`) that has real macros but no amino acid panel of its own is auto-estimated by scaling the matching curated entry's AA profile to its own protein content, rather than being silently dropped; result dicts carry `"estimated": True` when this happened. The `general` tier prefers a `cache_candidates` match's real data/fdc_id over the curated entry's own generic profile when one is found. `exclude_names` (case-insensitive) omits given suggestion names entirely from every tier — pantry, general, pairs, and diaas_improvers all derive from the same two filtered candidate pools — used by the web app's per-suggestion "ignore" checkboxes on `/food/{id}`, `/meal/{id}`, `/recipe/{id}`; threaded through `numa_app/services/complements.py::build_complement_display()`. Each route takes two repeated query params: `ignore_complements` (every currently-ignored name — both hidden inputs carrying forward prior ignores and any newly checked suggestion-card boxes) and `unignore` (names checked in the "manage ignored foods" panel to restore); `backend.py::_effective_ignored()` computes the final exclude set as `ignore_complements - unignore` before passing it to `exclude_names`, and re-renders the same effective set into the next page's hidden inputs so ignores accumulate across repeated recalculations instead of being overwritten. See `numa_app/services/complements.py::load_cache_candidates()` and the manual's "Amino acid estimates in complement suggestions" section for the user-facing side of this. |
| `nutrient_label(key)` | Reverse-lookup display name and unit for any nutrient key |
| `get_diaas(food_name)` | Return DIAAS protein digestibility score for a food (keyword lookup) |
| `get_antinutrient_flags(food_name)` | Return consolidated anti-nutrient flags as a list of `{"problem": str, "cause": str, "solutions": [(label, description), ...]}` dicts. Entries sharing the same group are merged into one flag with multiple solutions. |
| `get_density_g_per_ml(food_name, portions)` | Estimate g/ml density for volume-to-weight conversion. Static table takes priority over USDA portion data. |

**Protein completeness method:** The FAO 2013 dietary protein quality evaluation reference pattern (mg of each essential amino acid per gram of protein) is used. Met+Cys and Phe+Tyr are evaluated as combined pairs per FAO 2013, with reference values of 22 and 38 mg/g protein respectively. A protein digestibility factor (DIAAS) is applied to scores before the complete/incomplete determination so the classification reflects bioavailable amino acids. A food is complete when all digestibility-adjusted AA scores ≥ 1.0; the most limiting AA is the one with the lowest adjusted score. Raw (pre-digestibility) scores are shown in the display table.

**DIAAS lookup (`get_diaas`):** A static ordered table of ~60 food categories maps keyword patterns to DIAAS scores from FAO 2013 and peer-reviewed digestion studies. Used for single-food bioavailability display. Scores above 1.0 are capped at 1.0. More specific entries are listed before general ones — first match wins. If no entry matches, returns `None` and the caller treats the food as fully digestible (1.0). Results are **not** written back to the database; the scan is repeated on each analysis (microsecond cost). Distinct from the digestibility coefficients in `diaas.py`, which are used for meal-level pooled calculation. Notable: collagen/gelatin is scored 0.04 (near-zero tryptophan) — without this entry these proteins would be silently over-credited.

**Anti-nutrient flags:** A static table maps food keywords to advisory messages (phytate, oxalate, lectins, trypsin inhibitors, bound niacin). Flags can be suppressed by cooking-state keywords — e.g., "cooked"/"boiled" suppresses lectin and trypsin inhibitor warnings for beans.

**Density lookup:** `get_density_g_per_ml` first checks the food's USDA portion list for any cup or tablespoon entry and derives density from it. If none is found, it falls back to a static keyword table covering ~50 food categories. Returns `None` if density cannot be determined.

### `usda.py` — backwards-compatible shim (29 lines)

Re-exports all public names from `usda_api` and `usda_nutrients` so that every `import usda as _usda` call in the codebase continues to work unchanged. Edit `usda_api.py` or `usda_nutrients.py` directly; `usda.py` itself never needs to change.

### `diaas.py` — Meal-level DIAAS calculation

Implements the FAO 2013 meal-level DIAAS methodology: apply a true ileal digestibility coefficient per ingredient, pool the resulting digestible IAA grams across all ingredients, then score the pool against the FAO adult reference pattern.

**Constants:**

| Name | Purpose |
|---|---|
| `FAO_REFERENCE` | FAO 2013 adult reference pattern — mg of each IAA per g of total protein |
| `IAA_LABELS` | Human-readable names for the nine IAA keys |

**Digestibility data — three tiers:**

| Name | Entries | Source |
|---|---|---|
| `_DIGESTIBILITY_TABLE` | ~50 specific foods | FAO FNP 92 (2013); Mathai et al. 2017; Gorissen et al. 2018; other literature |
| `_CATEGORY_DEFAULTS` | 6 broad categories | Literature averages |
| `_OVERALL_DEFAULT` | 0.82 | Conservative plant-protein average |

The Met+Cys and Phe+Tyr IAA pairs are handled via `_IAA_PAIRS`: the secondary key's value (cystine for Met+Cys; tyrosine for Phe+Tyr) is added to the primary before scoring. If tyrosine is absent from a food's USDA record, the `phe_tyr_gap` flag is set in results.

**Key functions:**

| Function | Purpose |
|---|---|
| `get_digestibility(food_name, conn)` | Three-tier lookup: user override → curated → category → default. Returns `(digestibility, source_description)`. |
| `meal_level_diaas(ingredients, conn)` | Pool digestibility-corrected IAAs across all ingredients; compute composite DIAAS, limiting IAA, and digestible complete protein. Returns a detailed result dict. |
| `diaas_override_set/get/list/delete` | CRUD for the `diaas_overrides` table. |

### `profile.py` — User profile and RDA

`UserProfile` dataclass: `age`, `sex` ("male"/"female"/"other"), `weight_kg`, `height_cm`, `activity_level`, `weight_unit` ("kg"/"lb"), `height_unit` ("cm"/"imperial"). The unit fields control display formatting only; internal calculations always use kg and cm.

`parse_weight(raw)` and `parse_height(raw)` accept free-form strings ("80 kg", "176 lbs", "178 cm", "5'10\"") and return `(value_in_base_unit, detected_unit)`.

`compute_rda(profile)` returns a dict mapping nutrient keys to `(rda_value, unit, rda_type)` tuples where `rda_type` is `"target"` (recommended intake, e.g. calories), `"minimum"` (RDA or Adequate Intake — most nutrients), or `"limit"` (Tolerable Upper Intake Level, e.g. sodium). Calorie target uses Mifflin-St Jeor × activity multiplier. Protein scales with weight and activity (0.8–1.2 g/kg). All other targets follow NIH/IOM Dietary Reference Intakes with sex-specific and age-adjusted values.

Profile is saved to and loaded from `~/.config/numa/profile.json`.

The `use_oxalate_data: bool = False` field enables Harvard oxalate data lookup (see below). It is opt-in and defaults to False for all new and existing profiles.

**Profile Optimal targets and custom max limits** (`optimal_targets: dict`, `max_limits: dict` fields, both `nutrient_key -> float`, native unit): user-configured overrides layered on top of the standard RDA. `compute_optimal(profile)` returns only the nutrients present in `optimal_targets`, in the same `(value, unit, "target")` shape as `compute_rda` — absent nutrients are simply not in the dict, so callers can distinguish "not customized" from "customized to zero". `get_max_limits(profile)` returns a copy of `max_limits`. Both are edited via Settings → 7. Nutrient Targets and persist through the same `save_profile`/`load_profile` JSON round-trip as the rest of the profile — `load_profile()` explicitly reconstructs `UserProfile` field-by-field, so any new dataclass field must be added there too or it will silently fail to reload despite being written correctly by `save_profile`.

`numa_app/services/rda_status.py`'s `limit_warning(day_total, limit)` returns `True` once a day's total reaches 90% of a configured max limit (or exceeds it) — independent of `rda_status`'s built-in `"limit"` tier for nutrients like sodium that already have a Tolerable Upper Intake Level baked into `compute_rda`. `_nutrient_sections` (in `web/backend.py`) accepts optional `optimal`/`max_limits` dicts: when `optimal` is non-empty, a second "Profile Optimal" triplet of columns (meal %, day total %, goal) is added next to the RDA triplet, with nutrients lacking a configured optimal shown as a dash rather than falling back to RDA; when a nutrient's day total triggers `limit_warning`, its row is colored warning/error.

**`numa_app/services/day_profile.py` — per-day profile pinning:** since a user can maintain several named profiles and switch the active one over time (illness, travel, weight change), any RDA/DCP comparison for a *specific logged date* must never resolve the profile via a bare `profile.load_profile()` — that always returns whichever profile is active *right now*, which is wrong for a past date. This module is the required entry point for any date-scoped profile lookup:

- `get_profile_for_date(conn, meal_date)` — returns the `UserProfile` pinned to `meal_date`, pinning it first (to the currently-active profile) if it has none yet.
- `ensure_day_profile(conn, meal_date)` — pins `meal_date` if unpinned; no-op otherwise. Called once from every `db.meal_create(...)` call site (`web/backend.py`) so a day is pinned the first time a meal is saved for it.
- `backfill_missing_day_profiles(conn)` — pins every currently-logged date that predates this feature (or was otherwise never pinned) to today's active profile. Called once at startup (`web/backend.py`'s FastAPI lifespan handler) so existing data doesn't require the user to touch a day for it to get a profile.
- `set_day_profile_override(conn, meal_date, profile_name)` — manually reassigns `meal_date` to a specific saved profile (for when illness/travel didn't line up with the calendar day) and flags the day `overridden`.
- `protein_target_for_date(conn, meal_date, diet_pref)` — the daily protein RDA target from the date's pinned profile; used wherever `day_pct_goal` (Meals & Log's "% profile goal" column) is recomputed.

The pin is a **full numeric snapshot** (`json.dumps(dataclasses.asdict(profile))`), not just a name reference — editing a profile's numbers later does not retroactively change a day already pinned to it. Schema: `day_profile(meal_date PRIMARY KEY, profile_name, profile_json, pinned_at, overridden)` in `db.py`, alongside `day_bcp_cache`.

---

## Oxalate Data

### Architecture: two-database design

Oxalate reference data is kept separate from the user's `numa.db` because it is static, read-only, and belongs to a third party (Harvard T.H. Chan School of Public Health).

```
oxalate_source_data.py   — 433 foods as Python dicts; the authoritative source
build_oxalate_db.py      — reads source_data, writes oxalate.db (run once)
oxalate.db               — read-only SQLite file committed to the repo
oxalate.py               — context manager + search/fetch helpers
numa.db (oxalate_links)  — user-specific table: which food maps to which oxalate record
```

### Data source

Harvard T.H. Chan School of Public Health, Oxalate Table (November 2023) Credit: Dr. John Knight, University of Alabama School of Medicine URL: https://hsph.harvard.edu/wp-content/uploads/2024/07/OXALATE-TABLE-1.xlsx Retrieved: 2026-06-22

### oxalate.db schema

```sql
CREATE TABLE oxalate_foods (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    food_group              TEXT NOT NULL,
    food_name               TEXT NOT NULL,
    serving_size            TEXT,
    oxalate_mg_per_serving  REAL,
    oxalate_mg_per_100g     REAL,    -- NULL when serving is volumetric (cup, piece, etc.)
    category                TEXT,    -- "very high" | "high" | "moderate" | "low" | "negligible"
    directly_measured       INTEGER DEFAULT 0,
    source_note             TEXT
);
CREATE TABLE source_info (key TEXT PRIMARY KEY, value TEXT);
```

Per-100g values are computed during build for oz-based servings (1 oz = 28.3495 g). Volumetric servings (cups, tablespoons, pieces) cannot be converted without density data; those rows have `oxalate_mg_per_100g = NULL`.

Category thresholds (per 100g when available, per serving otherwise):

- very high: ≥ 300 mg/100g  (or ≥ 100 mg/serving)
- high:      ≥ 100 mg/100g  (or ≥  26 mg/serving)
- moderate:  ≥  25 mg/100g  (or ≥  10 mg/serving)
- low:       ≥   5 mg/100g  (or ≥   2 mg/serving)
- negligible: < 5 mg/100g

### numa.db: oxalate_links table

User-confirmed links between cached foods and oxalate records:

```sql
CREATE TABLE IF NOT EXISTS oxalate_links (
    fdc_id          INTEGER PRIMARY KEY REFERENCES foods(fdc_id) ON DELETE CASCADE,
    oxalate_food_id INTEGER,      -- oxalate.db row id; NULL when no_match=1
    user_confirmed  INTEGER DEFAULT 0,
    confirmed_at    TEXT,
    no_match        INTEGER DEFAULT 0   -- 1 = user confirmed no record applies
);
```

### oxalate.py

- `get_oxalate_db()` — context manager returning a read-only sqlite3.Connection
- `is_available()` — returns True if oxalate.db exists (safe to call at startup)
- `search_similar(conn, food_name, top_n=5)` — difflib.SequenceMatcher ranking against a broad candidate pool
- `get_by_id(conn, id)` — fetch one row
- `format_oxalate(row)` — compact display string, e.g. "72.0 mg / 1 oz  [high]"

### Rebuilding oxalate.db

```bash
python build_oxalate_db.py
```

The script deletes and recreates `oxalate.db` from scratch. Run this after editing `oxalate_source_data.py`. The generated file is committed to git so end users never need to run the script.

---

## Web Interface

A local FastAPI web app. All routes are in `web/backend.py`; templates live in `web/templates/`. See Running the Program for how to launch it.

### Starting the web app

```bash
cd web
uvicorn backend:app --reload      # development (auto-reloads on save)
uvicorn backend:app               # production-style (no reload)
```

The app is then available at `http://127.0.0.1:8000`.

### `web/backend.py` — routes and helpers

All FastAPI routes and backend helpers are in this single file. Key patterns:

- **`_nutrient_sections(nutrients, rda)`** — converts a nutrients dict into a list of grouped display rows, each with RDA % and CSS class for colour-coding. Used by food detail, meal analysis, and day analysis.
- **`_protein_section(food_name, nutrients)`** — builds the protein quality block (DIAAS score, amino acid ratio table) for a single food. Returns `None` if the food has no protein or AA data.
- **`_meal_totals(meal_id)`** — returns `(items_with_nutrients, total_nutrients_dict, diaas_result)` for a meal. Expands recipe ingredients for DIAAS. Item dicts include `id`, `food_name`, `fdc_id`, `recipe_id`, `amount`, `unit`, `notes`, `has_nuts`.
- **`_day_analysis(meal_date)`** — aggregates nutrients and ingredients across all meals on a given date; returns `(meals_list, combined_nutrients, diaas_result)`.
- **`_recipe_nutrients_per_serving(recipe_id, conn)`** — sums ingredient nutrients for one recipe, divides by serving count.
- **`_load_rda()`** — loads the user profile and returns computed RDA dict, or `None` if no profile exists.

### Route reference

#### Foods

| Method | Path | Description |
|---|---|---|
| GET | `/food/search` | Food search form |
| POST | `/food/search` | Food search results (USDA + cache + recipes) |
| POST | `/search` | Legacy alias for POST `/food/search` |
| GET | `/food/analyze-portion` | Portion analysis form |
| POST | `/food/analyze-portion` | Portion analysis results |
| GET | `/food/analyze-recipe-portion` | Recipe portion analysis form |
| POST | `/food/analyze-recipe-portion` | Recipe portion analysis results |
| GET | `/food/convert` | Portion conversion search |
| GET | `/food/convert/{fdc_id}` | Portion conversion detail for a specific food |
| GET | `/food/compare` | Food comparison table (query params: `ids=`, `amounts=`, `search=`) |
| POST | `/food/compare/add` | Add a food to the comparison |
| POST | `/food/compare/remove` | Remove a food from the comparison |
| POST | `/food/compare/amounts` | Update gram amounts for compared foods |
| POST | `/food/compare/save` | Save the current comparison list |
| GET | `/food/compare/load/{cmp_id}` | Load a saved comparison |
| POST | `/food/compare/saved/delete` | Delete a saved comparison |
| GET | `/food/cache` | Browse/search cached foods |
| POST | `/food/cache/delete` | Remove a food from the cache |
| GET | `/food/cache/prune` | Preview foods unused by pantry/recipes/meals before pruning |
| POST | `/food/cache/prune` | Delete all foods unused by pantry/recipes/meals (user-drafted foods protected) |
| GET | `/food/custom-profiles` | List user-drafted food profiles |
| POST | `/food/custom-profiles/create` | Create a new drafted profile |
| POST | `/food/custom-profiles/delete/{fdc_id}` | Delete a drafted profile |
| GET | `/food/annotate` | Browse foods for annotation |
| GET | `/food/annotate/{fdc_id}` | Edit annotation form |
| POST | `/food/annotate/{fdc_id}` | Save annotation |
| GET | `/food/{fdc_id}` | Food detail with nutrient table and protein quality (registered last among `/food/*`) |

#### Pantry

| Method | Path | Description |
|---|---|---|
| GET | `/pantry` | Pantry list |
| POST | `/pantry/add` | Add a food to pantry |
| POST | `/pantry/remove/{pantry_id}` | Remove a food from pantry |

#### Meals

| Method | Path | Description |
|---|---|---|
| GET | `/meals` | Meal list (query params: `show_all=`, `date=YYYY-MM-DD`) |
| POST | `/meals/create` | Create a new meal |
| GET | `/meals/search` | Search meal history by food name (query param: `q=`) |
| GET | `/meal/{meal_id}` | Meal view/edit (query param: `q=` for food search) |
| POST | `/meal/{meal_id}/add` | Add a food to a meal |
| POST | `/meal/{meal_id}/add-recipe` | Add a recipe to a meal |
| POST | `/meal/{meal_id}/remove/{item_id}` | Remove an item from a meal |
| POST | `/meal/{meal_id}/rename` | Rename a meal |
| POST | `/meal/{meal_id}/complete` | Toggle meal complete/incomplete |
| POST | `/meal/{meal_id}/delete` | Delete a meal |
| POST | `/meal/{meal_id}/update/{item_id}` | Edit an item's amount and notes |
| POST | `/meal/{meal_id}/merge` | Merge selected meals on the same date into one |
| GET | `/meal/{meal_id}/day` | Full-day analysis for all meals on the same date as this meal |

#### Settings, Recipes, Summary

| Method | Path | Description |
|---|---|---|
| GET | `/settings` | Settings page (profile, diet, API key, DIAAS overrides, RDA table) |
| POST | `/settings` | Save user profile |
| POST | `/settings/diet` | Save dietary preference |
| POST | `/settings/api-key` | Save USDA API key |
| POST | `/settings/diaas-override` | Add/update a DIAAS digestibility override |
| POST | `/settings/diaas-override/delete` | Delete a DIAAS override |
| GET | `/recipes` | Recipes stub page (not yet implemented) |
| GET | `/summary` | Daily summary stub page (not yet implemented) |
| GET | `/manual` | Rendered user-manual.md |
| GET | `/` | Home page |

### Template reference

#### `base.html`

Shared layout wrapper. Includes Bootstrap 5 CDN, `/static/style.css`, the top navbar with dropdown menus, a footer, and the keyboard-shortcut JS. All other templates extend this.

The navbar marks the active section by comparing `request.url.path` to each nav link's prefix. Foods and Analysis (Daily summary, Food use in meals) are dropdowns; Recipes, Meals, Settings, and Manual are top-level links.

**Unsaved-changes warning.** A third inline script in `base.html` generically tracks every `form[method="post"]` containing at least one non-hidden editable field: it snapshots the form's serialized state (`FormData` → `URLSearchParams`) on load, re-checks on `input`/`change`, and toggles a `.form-dirty` class on the form plus `.btn-dirty` on its submit button (CSS in `web/static/style.css`) and a JS-injected `.unsaved-badge` ("Unsaved changes") span. A `beforeunload` listener warns if any tracked form is still dirty. Forms with no editable fields (delete/move/mark-complete one-click actions) and GET forms (search/filter) are excluded automatically by the selector, so no per-template opt-out markup is needed.

**Search-state restore.** A fourth inline script opts a page into remembering its last search across a brief trip to another page (via a plain link — the browser's own Back button already preserves URL state, so this only fills the gap for forward navigation). A page marks its search `<form>` with the bare `data-persist-search` attribute (currently `meal.html`'s "Add Food or Recipe" search and `recipe_edit.html`'s "Add Ingredient" search). On every load of a marked page the script: saves the current `?q=` to `sessionStorage` under `numa_search_q:<pathname>` if present and non-empty; clears it if `q` is present but explicitly empty (a deliberate cleared search must not be overridden); and if `q` is absent entirely, redirects once to re-add the last saved `q` (restoring results) when a saved value exists. Any element marked `data-reset-search` (rendered only when a search is active, e.g. a "Clear search" link) clears the saved value and reloads the bare path — the page's clean default state. Purely client-side; no server route or session state involved.

**Select-all-sources.** A fifth inline script gives every Source filter row (`_source_filter_select.html`) a "Select all sources" button (`data-select-all-sources`), which re-checks every checkbox inside its enclosing `role="group"` container without touching search text, sort, or the result-limit input — unlike "Clear search", which resets all of those. Delegated on `document`, so it works on every page that includes the Source filter row, including ones with no `data-persist-search` form.

#### `home.html`

Renders the content of `home.md` (project root) as HTML. The markdown file is rendered once at startup and cached in `web/home_body.cache`; the cache is invalidated if `home.md` is newer.

#### `search.html`

Food search results. Shows a results table with food name, data type, brand, and source badge (`pantry` / `cache` / `recipe` / `usda` / `off`). Each row links to `/food/{fdc_id}`. Used for both the Foods → Search page and as a reusable search partial.

**Ranking.** Results can be ordered two ways, chosen via a dropdown and persisted per-user in `prefs.json` (key `sort_food_search`, default `"relevance"`; shared with the meal add-food panel in `meal.html`): `"relevance"` ranks purely by name-match quality (`_search_relevance_key()` in `web/backend.py` — exact match, then prefix match, then fraction of query words matched, then shortest name, then alphabetical), ignoring source; `"grouped"` sorts by source category first (`_SEARCH_CATEGORY_RANK`: pantry → recipe → cache → USDA/OFF), using the same relevance key as a tiebreaker within each group. Both modes are applied via the shared `_sort_search_results()` helper. A cached food is tagged `"pantry"` instead of `"cache"` when its `fdc_id` is present in the Pantry table (`_pantry_fdc_ids()`).

**Batch AA confirmation.** A live (uncached) USDA search result's `aa` field is the coarse guess `"~✓"` for Foundation/SR Legacy types — `search_foods()`'s API response carries no nutrient data at all, so completeness genuinely can't be known without a detail fetch, and fetching every uncached result on every search would cost one USDA API call each. Instead, `search.html` renders a checkbox per `"~✓"` row (plus a select-all checkbox in the header) inside a `<form action="/food/confirm-aa">`; a "Fetch full details for selected" submit button (disabled until at least one box is checked, via inline JS) posts the chosen `fdc_id`s. `POST /food/confirm-aa` (`web/backend.py`) fetches and caches each one not already cached (same `get_food_detail()` + `cache_food()` pattern as `meal_add_food`), then redirects back to `/food/search?query=...&sort=...` — where those foods now resolve to a confirmed `"✓"` or `"✗"` via the normal cached-food path in `_search_logic()`.

#### `food_detail.html`

Displays full nutrient data for one food, scaled to the requested gram amount (`?amount=N`). Shows:

- Food name, data type, brand, serving size
- Portion picker (USDA named portions, if any)
- Nutrient table grouped by Macronutrients, Omega Fatty Acids, Minerals, Vitamins, Phytonutrients, Amino Acids — each row with value, unit, and RDA % (colour-coded if profile exists)
- Protein quality section (DIAAS score + AA ratio table) if amino acid data is present
- Antinutrient flags if applicable

#### `food_analyze_portion.html`

Two-phase page: search form → results table → pick a food → enter gram amount → full nutrient table. Reuses the same search logic as `search.html`.

#### `food_analyze_recipe_portion.html`

Dropdown of all saved recipes + servings input → scaled nutrient table. Shows protein quality section if recipe has AA data.

#### `food_convert.html`

Portion ↔ weight conversion. Phase 1: search for a food. Phase 2: shows the food's USDA named portions, gram weights, and the computed density (g/mL) for volume conversion. Highlights the closest USDA portion to an entered gram amount.

#### `food_compare.html`

Side-by-side nutrient comparison. Up to 6 foods; amounts are independently adjustable in grams. Highest value per nutrient row is highlighted. Saved comparison lists can be named, saved, loaded, and deleted. Food search is inline on the same page.

#### `food_cache.html`

Browsable/searchable table of all cached foods. Columns: FDC ID, name, data type, brand, AA data flag, GI annotation, DIAAS, notes. The DIAAS column shows your saved annotation (marked ★) when one exists, otherwise the keyword-matched reference-table value (see "Per-food DIAAS via annotations" above) for foods with amino acid data — blank otherwise. Each row links to `/food/{fdc_id}` and `/food/annotate/{fdc_id}`. Supports deletion.

#### `food_custom_profiles.html`

Lists all user-drafted food profiles (data type = "User Drafted"). Provides a create-by-name form and per-row delete. Creating a profile immediately redirects to `/food/{fdc_id}` for nutrient editing.

#### `food_annotate.html`

Two-mode template. In list mode: browsable/searchable table of cached foods showing existing GI and DIAAS annotations. In edit mode (`editing=True`): form for entering GI estimate (0–100), DIAAS digestibility (0–1), and prep context note, with "no prompt" checkboxes to suppress future annotation prompts.

#### `pantry.html`

Table of pantry items. Columns match `food_cache.html`: food name, FDC ID link (if available), data type, AA data flag, GI annotation, DIAAS (same saved-annotation-or-reference-table logic, ★ marks a saved value), notes, added date. Add-by-name form at top. Per-row remove button.

#### `meals.html`

Meal list with:
- New Meal form (name + date)
- Date filter form (`?date=YYYY-MM-DD`) + "Search meal history" link
- Table columns: Meal name (links to `/meal/{id}`), Date, Done (✓ / ·), Items count
- Show-all / show-recent-9 toggle when more than 9 meals exist

#### `meal.html`

Full meal view and edit page. Sections (all collapsible with `<details>`):

- **Header**: meal name, complete/incomplete badge, date
- **Management bar**: Mark complete/incomplete toggle, Analyze full day button (shown when other meals exist on the same date), Rename (inline collapsible form), Delete (with JS confirmation)
- **Add Food or Recipe**: food search form + results table; foods add by gram weight, recipes add by serving count
- **Items**: table with food name link, amount, notes, per-item Edit (inline collapsible form for amount + notes) and Remove buttons
- **Merge meals**: shown when other meals exist on the same date; checkboxes to select which meals to merge, name input, delete-originals option
- **Protein Quality (DIAAS)**: meal-level DIAAS score, total protein, digestible complete protein, limiting amino acid, per-AA ratio table. When DCP is capped (see [DCP cap](user-manual.html#dcp-cap)), the derivation line shows the uncapped projection and the capped result instead of a plain `raw protein × DIAAS` equation (`dcp_was_capped`, via `_build_diaas_display()` in `web/backend.py`).
- **Total Nutrients**: grouped nutrient table with RDA % colour-coded by target type

#### `meal_day.html`

Full-day analysis for all meals on a single date. Reached via the "Analyze full day" button on `meal.html`. Shows:

- List of all meals on the date (with links back to each meal)
- Combined DIAAS (pooled across all meals)
- Combined nutrient table with RDA % (using full-day totals as the denominator)

#### `meals_search.html`

Meal history search. Query param `q=` searches food names across all logged meal items (recipes are matched by name; ingredients inside recipes are not searched). Shows:

- **All Occurrences** table: date, meal (link), food name, portion, notes
- **Summary by Food** table: unique food names with times used, total grams consumed, first/last date seen

#### `recipes.html`

Placeholder stub. Recipes are not yet implemented in the web interface.

#### `summary.html`

Placeholder stub. Daily summary is not yet implemented in the web interface.

#### `settings.html`

Three forms on one page:

- **User profile**: age, sex, weight (kg or lb), height (cm or ft+in), activity level → computes and displays the RDA table
- **Dietary preferences**: radio buttons (all animal foods / vegetarian / plant-based only)
- **USDA API key**: text input with show/hide toggle
- **DIAAS digestibility overrides**: table of existing overrides with delete buttons; add-new form (food name, digestibility 0–1, optional notes)

#### `manual.html`

Renders `user-manual.md` as HTML using the Python `markdown` library with `toc`, `fenced_code`, and `tables` extensions. Provides a scrollable, linked view of the full user manual.

---

## Data Storage

| Location | Contents |
|---|---|
| `~/.local/share/numa/numa.db` | SQLite database (foods cache, recipes, meals, pantry, DIAAS overrides) |
| `~/.config/numa/config.json` | USDA API key, search result depth (`search_boost_page_size`) |
| `~/.config/numa/theme` | Saved color theme preference |
| `~/.local/share/numa/prefs.json` | Dietary preferences (`diet_pref`), editor command, and remembered list-sort choices (`sort_recipes`, `sort_food_cache`, `sort_meals`) |
| `~/.config/numa/profile.json` | User profile (age, sex, weight, height, activity level) |
| `~/.numa/reports/` | Auto-saved nutrition reports (Markdown) — one file per analysis |
| `~/.numa/user-requested-nutrition-reports/` | User-exported reports (txt, md, or html) |

---

## Test Suite

**462 tests**, all passing (as of the CLI removal, 2026-08-04 — `test_cli.py` and its ~144 CLI-only tests were deleted along with the CLI).

Run with: `pytest` (uses `pytest.ini` which sets `testpaths = tests` and `pythonpath = .`).

> **Note:** `pytest` and `httpx` are dev/test-only dependencies, listed in `requirements.txt` alongside the runtime ones. `httpx` is needed for `tests/test_web.py` (FastAPI's `TestClient` requires it).

| File | What it tests |
|---|---|
| `tests/conftest.py` | Shared fixtures and sample data constants |
| `tests/test_db.py` | Schema creation, all CRUD helpers, cascade deletes, rollback on exception |
| `tests/test_usda.py` | `scale_nutrients`, `sum_nutrients`, `_parse_food`, `protein_completeness`, `nutrient_label`, `get_diaas`, `get_antinutrient_flags`, `suggest_complements`, `get_density_g_per_ml` |
| `tests/test_diaas.py` | `get_digestibility` (all tiers), `meal_level_diaas` (edge cases, complementarity, pairing, gap flags), DIAAS override CRUD |
| `tests/test_profile.py` | `load_profile`, `save_profile`, `bmr`, `compute_rda` (sex/age/activity variants), `compute_optimal`, `get_max_limits`, unit conversion helpers |
| `tests/test_web.py` | FastAPI `TestClient` tests: every parameter-free page render, food search/detail, and all mutating POST workflows — pantry, meals (create/add/complete/delete/rename/merge/refresh-aa/add-recipe), recipes (new/edit/delete/copy/ingredient add-edit-move), custom profiles, settings (profile/DIAAS-override), food-cache delete/prune, annotate, and compare (add/add-multiple/remove/amounts/save/load/rename/delete) |
| `tests/test_complements.py` | `numa_app/services/complements.py`: `aa_effects()` digestibility rescaling, `two_step_combo()`, `build_complement_display()` gap detection |
| `tests/test_recipe_nutrients.py` | `numa_app/services/recipe_nutrients.py`: nested sub-recipe expansion/flattening, linear portion scaling, `best_aa_nutrients()` complement fallback |
| `tests/test_glycemic_load.py` | `numa_app/services/glycemic_load.py`: food/recipe line items, recipe GL rollup via `gl_g`, partial totals alongside blockers |
| `tests/test_meal_bcp.py` | `numa_app/services/meal_bcp.py`: `recipe_dcp_fallback()` sums precomputed recipe `dcp_g` when ingredient-level AA data is unavailable |
| `tests/test_rda_status.py` | `numa_app/services/rda_status.py`: `rda_status()` tier boundaries for minimum/target and limit-type nutrients; `limit_warning()` 90%/100% thresholds |
| `tests/test_food_import.py` | `numa_app/services/food_import.py`: `VALID_NUTRIENT_KEYS` completeness, `convert_per_serving()` scaling/validation, `validate_and_strip()` key/type filtering |

### Test infrastructure

**Autouse fixtures** keep each test hermetic:

| Fixture | Effect |
|---|---|
| `use_test_db` | Redirects `_db._DB_PATH` to a per-test temp file; schema initialized fresh |
| `use_test_profile` | Redirects `profile._PROFILE_FILE` to a per-test temp path |
| `no_off` | Stubs `openfoodfacts.search_foods` to return `[]`; prevents network hits and stops OFF results from affecting search ordering or output in any test |

`tests/test_web.py` additionally has its own `use_test_web_prefs` fixture (redirects `web/backend.py`'s own `_PREFS_FILE` constant) and a `client` fixture (FastAPI `TestClient`).

---

## Maintenance

### Weekly sweep (Saturdays)

A recurring maintenance pass, scoped to what changed since the last sweep — not a full re-audit each time. **Run the items in this order** — it's not arbitrary: pruning has to happen before the items that scan the changelog (so they're not reading entries about to be deleted), and the link check has to happen last (so it catches anything the manual-editing items introduce).

1. **CLAUDE.md drift** — the package-layout listing near the top of `CLAUDE.md` is hand-maintained; check it against what's actually in `numa_app/` and the repo root, since new modules added during the week won't show up unless someone remembers to add them. Fast and independent — do it first for an easy win.
2. **Vendored dependency check** — `web/static/vendor/bootstrap/` (CSS + JS, currently 5.3.8) is vendored locally rather than loaded from a CDN, so the app works offline. Low urgency since this is a locally-run app with no untrusted remote input reaching it, but worth a quick check for newer Bootstrap releases/patches at this cadence rather than a separate one. Also fast and independent.
3. **Changelog pruning** — the "Recent program updates log" lives in `user-manual.md` Appendix A (moved here from Appendix K on 2026-08-05 since it's checked far more often than the other appendices). Keep roughly the **last 2 weeks** of entries. Older entries are safe to delete: `create_release.py` copies same-day entries into the release notes at push time and never re-reads the file afterward, so a pruned old entry can't retroactively change a past release's notes (stated in the manual's own `[//]: #` comment above the log). Do this **before** items 4-6 below — they all scan "the last two weeks" of this same log, so pruning first means less to read and no risk of auditing an entry that's about to be deleted anyway.
4. **Manual consolidation** — the same mechanism explained more than once (once per page/interface) that should live once in Part 4 — Shared Operations (or an existing Part 3 reference section) of `user-manual.md`, cross-linked from every place it applies; a feature documented for only one interface/page despite applying to more than one; two command/column lists for the same menu that have drifted out of sync (fix by pointing the thinner one at the canonical list, not updating both); a real behavior change that only exists in the changelog and was never written into the manual body; an Appendix A entry that contradicts a later entry (e.g. a feature marked "not built yet" when a subsequent same-day or later entry announces it shipped). Also worth a dedicated pass: leftover CLI-era content (typed single-letter commands like `a{id}=analyze`, `Type ?keyword` help references) that survived past the 2026-08-04 CLI removal — grep `user-manual.md` for `Type ?`, `^Commands:`, and `Command line:` as a quick way to surface it; the first full sweep (2026-08-17) found a meaningful amount still there, so don't assume one pass caught it all.
5. **README.md accuracy** — repo-root `README.md` (the public-facing overview: disclaimer, who it's for, key features list, download section) checked against current app behavior — a feature listed there that changed or was removed, or a new user-facing feature that should be added to the "Key features" list. Distinct from this file (`README-numa-documentation.md`), which is the internal architecture doc and still has a CLI-era cleanup pass pending.
6. **Test coverage gaps** — cross-check the week's changelog entries against `tests/` to catch a shipped behavior change that never got a test.
7. **Stale internal links** — every `#anchor` reference in `user-manual.md` checked against actual anchor definitions (`[name]` tags / heading IDs); also worth a pass over external URLs (footnotes, source citations) for rot. A quick way to check: extract every `](#anchor)` reference and every `{: #anchor}` definition and diff them (a Python one-liner with two `re.findall` calls does it); for external URLs, `curl -s -o /dev/null -w "%{http_code}"` with a browser-like `-A` user agent and `-L` to follow redirects, but treat a 403/429 as inconclusive (bot-blocking, not necessarily rot) and only trust a 404/redirect-to-an-error-page as real rot. Do this **last** — item 4 (manual consolidation) is the item most likely to add new `[text](#anchor)` links, so checking beforehand just means checking again afterward anyway.

Items 4-6 all scan the same two-week changelog window for gaps, just against three different targets (manual body, README, test suite) — do a single read-through of the changelog and produce three gap-lists from it, rather than re-reading the same entries three separate times (the first full sweep, 2026-08-17, ran two separate audits that each re-read the same window from scratch).

After a sweep: log the result as a new `user-manual.md` Appendix A entry (or a suitable per-item entry if the fixes span categories), and bump the manual's own timestamp header. Pure doc/config consolidation does not require a `version.py` bump (no application behavior changed) — but a real bug fix found via item 6 (missing test written, bug fixed) does.

---

## Implementation Phases

The original design specified three phases. Phase 1 is complete.

### Phase 1 — Complete ✓

- USDA FoodData Central API integration
- Food search, portion analysis, local food cache
- Recipe builder (create, view, analyze, delete)
- Meal log with date (log, view, analyze, delete)
- Daily nutrition summary
- Protein completeness analysis via amino acid profile
- Full test suite

### Phase 2 — Planned

- Development of a slightly modified version that will run on Windows operating systems. (The developmental version is Linux-only.)
- Nutrient trend analysis over time (charts or tables)
- Meal planning and dietary pattern analysis

### Phase 3 — Planned

- Replacement of external editor with internal one - v. `2026-04-13-numa-system-editor-versus-python-replacement` for details
- ?-Integration with smart kitchen devices
- ?-API for third-party app integration
- Machine learning components for dietary recommendations


## Appendix — Understanding Protein Quality

For a full explanation of the FAO reference values, EAA ratios, what "complete" protein means, and how the DIAAS score is calculated with worked examples, see **[Appendix B of the NutriMagnus User Manual](user-manual.html#appendix-b)**.
