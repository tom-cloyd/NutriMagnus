# NutriMagnus — Nutritional Analysis Program documentation

A command-line nutritional analysis tool written in Python. Analyzes individual food portions, recipes, and complete meals using data from the USDA FoodData Central database. The program presents itself to users as **NutriMagnus ("nutrition wizard")**.

UPDATED: 2026-06-21:0034
---

## Table of Contents

- [Preliminary](#preliminary)
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Program](#running-the-program)
- [Menu Structure](#menu-structure)
- [Usage Guide](#usage-guide)
  - [The local food cache](#the-local-food-cache)
  - [Food annotations (GI and DIAAS estimates)](#food-annotations-gi-and-diaas-estimates)
  - [Drafted food profiles](#drafted-food-profiles-user-modified-nutrients)
  - [Searching for a food](#searching-for-a-food)
- [Architecture](#architecture)
- [Web Interface](#web-interface)
- [Data Storage](#data-storage)
- [Test Suite](#test-suite)
- [Implementation Phases](#implementation-phases)
- [Appendix — Understanding Protein Quality: The FAO Reference Values and DIAAS](#appendix---understanding-protein-quality-the-fao-reference-values-and-diaas)

---

## Preliminary

* **To launch the CLI version**
  * Linux: `numa`  (symlink at `~/.local/bin/numa` → `numa.py` is on PATH)
  * Windows: `python numa.py`

* **To launch the web version**
  * From the `web/` directory:
  * Linux / Windows: `uvicorn backend:app --reload`
  * Then open `http://localhost:8000` in a browser.
  * Use `uvicorn backend:app` (no `--reload`) for a stable session without auto-restart.

---

## Overview

NutriMagnus was designed from a preliminary specification (see `2025-02-26-python-nutritional analysis program.md`) that called for:

- Calculation of bio-available complete protein combinations for one or more foods
- Nutritional analysis of individual foods, recipes, and meals
- Saving meals by date and saving recipes

The program uses two nutrition data sources:

- **USDA FoodData Central** — free, comprehensive, 300,000+ foods with full macro/micronutrient profiles including amino acid data for protein completeness analysis.
- **Open Food Facts** — free, open-source (CC BY-SA 4.0), community-maintained, millions of branded/packaged products globally. No API key required. Does not include amino acid data.

The CLI interface follows the same interaction pattern as `cmgr.py` (the contact manager in the sibling `../cmgr/` directory): hierarchical menus, Ctrl+C to cancel and go back, color themes, and a consistent prompt style throughout.

---

## Project Structure

```
numa/
  numa.py                          — thin CLI entry point (argparse); delegates to numa_app.main
  db.py                            — SQLite database: schema, queries, context manager
  usda.py                          — backwards-compatible re-export shim (29 lines); import this
  usda_api.py                      — USDA FoodData Central HTTP client; API key; search; detail fetch
  usda_nutrients.py                — nutrient math; AA analysis; DIAAS lookup; complement table; density
  openfoodfacts.py                 — Open Food Facts API client; merged into food search results
  diaas.py                         — Meal-level DIAAS calculation and digestibility data
  export.py                        — Report export (txt, md, html)
  profile.py                       — User profile dataclass, RDA computation, unit parsing
  requirements.txt                 — Python dependencies (rich only)
  README-numa-documentation.md     — This file
  README-Nutrimagnus-status-report.md  — Draft public status report
  README-refactor.md               — Notes on the offline-friendly refactor
  scripts/
    setup_venv.sh                  — Create and populate .venv
    run_numa.sh                    — Quick run without manually activating venv
  numa_app/                        — Main application package (product of the refactor)
    __init__.py
    __main__.py
    main.py                        — run_app(), initialize_app(), print_startup_banner(), _run_menu()
    state.py                       — AppContext; theme/dietary state; set_theme(), set_diet_pref()
    config/
      __init__.py
      prefs.py                     — dietary preferences load/save; first-run diet-pref prompt; _DIET_LABELS
      theme.py                     — theme load/save/detect; _change_theme()
    ui/
      __init__.py
      common.py                    — _show_menu(), _safe_call(), dot_cell(), table_title(), section_title(), table_footer()
      prompts.py                   — _prompt(), Cancelled, _ask_float(), _ask_int(), _ask_date()
      render.py                    — _print_nutrient_table(), _print_protein_completeness(),
                                     _print_bioavailability(), _print_complement_suggestions()
    services/
      __init__.py
      annotations.py               — annotate_food_interactive(), maybe_prompt_gi/diaas(); food annotation UI
      portions.py                  — _pick_portion(), _parse_portion_input()
      reports.py                   — export rendering support
      search.py                    — _search_and_pick_food(), _suggest_foundation_search()
    workflows/
      __init__.py
      foods.py                     — Foods menu; search, portion analysis, convert, cached-food viewer
      drafted_foods.py             — Edit any cached food; drafted-profile CRUD; bulk AA import
      pantry.py                    — My Pantry menu
      meals.py                     — Meals & Log menu
      recipes.py                   — Recipes menu dispatch; shared helpers; create/browse/develop/delete
      recipe_analysis.py           — Analyze recipe workflow (_do_recipe_view, _resolve_recipe_dcp_data)
      recipe_edit.py               — Edit recipe workflow (_do_recipe_edit)
      settings.py                  — Settings menu; user profile; DIAAS overrides; RDA comparison
      summary.py                   — Daily Summary menu
  manual.py                        — User manual parser; ?keyword help lookup; show(), lookup(),
                                     available(); _ALIASES for topic shortcuts
  user-manual.md                   — Essential instructions, tips, and reference material for
                                     users; plain-text sections keyed by [anchor] for inline display
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

| Package | Purpose                                    |
|---------|--------------------------------------------|
| `rich`  | Console output, tables, color themes       |

> **Note:** `typer` was removed in the refactor — the CLI now uses stdlib `argparse`. `requests` is not a dependency; HTTP uses stdlib `urllib`.

### 2. USDA API key

Food searches require a free API key from the USDA FoodData Central service.

#### Getting a key

1. Go to **https://fdc.nal.usda.gov/api-key-signup.html**
2. Enter your name and email address — no payment or account creation required.
3. The key is emailed to you immediately (check spam if it doesn't arrive within a minute or two).

The key is free and gives you **1,000 requests per hour**, which is more than
enough for normal use. There is no paid tier — this is the standard limit for
all registered keys.

> **Note:** The USDA API has a built-in `DEMO_KEY` that works without registration,
> but it is limited to roughly 30 requests per hour and will rate-limit quickly
> during a normal session. Always use a registered key for real use.

#### Setting the key

Run this once after you receive the key:

```bash
./numa.py --api-key YOUR_KEY_HERE
```

The key is saved to `~/.config/numa/config.json` and used automatically on all
subsequent runs. It can also be changed at any time via the **Settings** menu
inside the program (**Settings → Advanced settings → USDA API key**).

---

## Running the Program

```bash
cd numa
./numa.py
```

Or, without manually activating the venv:

```bash
./scripts/run_numa.sh
```

The program launches into a startup banner (showing profile, theme, and dietary-preference status) and then the interactive menu. No subcommands are required for normal use.

**Command-line options** (for scripting / setup only):

```
./numa.py --api-key KEY     Set USDA API key and exit
./numa.py --theme THEME     Set color theme: dark, light, neutral, auto
./numa.py --help            Show options
```

**Menu navigation conventions** (consistent with cmgr):

| Key      | Action                              |
|----------|-------------------------------------|
| `1`–`9`  | Select numbered menu item           |
| `b`      | Go back to the parent menu (works at every prompt) |
| `m`      | Jump directly to the main menu (works at every prompt) |
| `q`      | Quit the program entirely (works at every prompt)  |
| Ctrl+C   | Cancel current prompt, go back      |
| Escape   | Same as Ctrl+C                      |
| ↑ / ↓    | Cycle through input history at any free-text prompt |

`b`, `m`, and `q` are accepted at every prompt throughout the program — menus, food
search results, ID entry, portion size entry, and ingredient/item loops. You
are never required to complete a flow before being able to leave it.

**First run:** On first launch, if no dietary preferences file have been saved yet, the program asks which foods protein complement suggestions should include: all animal foods, vegetarian (dairy + eggs only), or plant-based only. The answer is saved to `~/.config/numa/prefs.json` as the `diet_pref` key and can be changed at any time via **Settings → Dietary preferences**. Existing installs that have the legacy `include_animal_foods` boolean are migrated automatically on the next launch.

---

## Menu Structure

numa has five top-level menu areas. The main menu is a simple numbered list; each choice opens a submenu with its own set of commands. The sections below describe each menu in detail.

```
NutriMagnus Menu
  1. Foods          — search, analyze, compare, cache, pantry, custom profiles
  2. Recipes        — create, browse, edit, analyze, copy, develop
  3. Meals & Log    — log meals, view history, analyze, merge
  4. Daily Summary  — nutrient totals for today or any date
  5. Settings       — theme, profile, preferences, API key, advanced
```

At every prompt in the program, `b` goes back to the previous menu, `m` jumps directly to the main menu, and `q` quits. Ctrl+C at any prompt is equivalent to `b`.

---

### Foods Menu

**Title:** Foods — Search, Analyze & Manage

The Foods menu is the primary interface for finding food data, exploring nutrients, and managing the local food cache. It has nine items.

**1. Search food databases (USDA + Open Food Facts / display or output data)**

Search by name or FDC ID. The program checks the local cache first and shows any matches in a fast **Food cache** table before going online. If the food is not cached, it queries USDA FoodData Central and Open Food Facts simultaneously and presents a merged results list. Selecting a food displays its full nutrient breakdown (per 100 g) including protein completeness assessment. The user may then proceed to portion analysis. See [Searching for a food](#searching-for-a-food) and [Protein completeness](#protein-completeness) in the Usage Guide.

**`dout` — bulk data output command.** Typing `dout <id> [id …]` at the search prompt (e.g. `dout 2346396 2477360`) fetches complete nutrient data for one or more FDC IDs and writes it to `numa.data` in the user's home directory (`~/numa.data`, i.e. `/home/<user>/numa.data`). The output is a JSON array; each entry contains `fdc_id`, `name`, `data_type`, `source` (`"cache"` or `"USDA"`), `nutrients_per_100g`, and `portions`. The cache is checked first; any food not found locally is fetched from USDA and then stored in the cache. The terminal confirms the full file path on completion. Intended for validation and hand calculations outside the interactive workflow. Implemented in `_do_dout()` in `foods.py`.

**2. Analyze a food portion**

Same search flow as item 1, but proceeds directly to portion sizing after food selection. The user enters an amount (e.g. `150 g`, `3 oz`, `1 cup`) and the program displays scaled nutrient totals, protein completeness, bioavailability (if DIAAS data is available), and complement suggestions. See [Analyzing a portion](#analyzing-a-portion).

**3. Analyze a saved recipe portion**

Lists saved recipes and allows the user to select one by ID. After choosing a portion size (number of servings or a fraction), the program displays scaled nutrient totals and protein completeness for that portion. Equivalent to running the recipe analysis workflow without entering the full Recipes menu. See [Analyzing a recipe portion](#analyzing-a-recipe-portion).

**4. Convert a portion ⟺ weight (volume/weight, no analysis)**

Search for a food, then enter either a volume (e.g. `1 cup`) or a weight (e.g. `200 g`). The program returns the equivalent in the other unit using USDA portion data or estimated density. No nutritional analysis is performed; this is a measurement conversion tool for recipe development.

**5. Compare foods (side-by-side nutrient table, up to 8)**

Select two to eight foods (by search or cache pick, each with its own portion choice) and view them in a side-by-side nutrient table. The header lists each food's name and FDC ID. Columns cover all nutrient groups; rows with no data in any column are suppressed. Useful for choosing between protein sources, evaluating substitutions, or comparing branded variants.

**6. Food Cache (view, edit, delete foods you have looked up)**

Lists every food stored in the local cache with columns for AA status (✓/✗), GI annotation, DIAAS annotation, confidence note indicator (C), curator notes indicator (N), FDC ID, name, data type, and brand. Supports name/brand filtering with `/text`. Commands below the table act on individual rows by number:

| Command | Action |
|---------|--------|
| `v#` | View nutrient profile (per 100 g) |
| `n#` | View nutrients + protein completeness + all notes |
| `c#` | View confidence/source note only |
| `a#` | Analyze a portion |
| `e#` | Edit food data (name, serving, nutrients, note, GI/DIAAS annotation) |
| `d#` / `d#,#` | Delete one or more entries |
| `i#` / `i#,#` / `i` | Generate a Claude AI prompt for selected or all ✗ foods |
| `r` | Import a saved Claude response (`~/claude_response.txt`) |
| `l` | Re-display the full table |
| `/text` | Filter list by name or brand |

Editing any food marks it `user_drafted=True`, protecting it from future USDA re-fetches. For the Claude fetch workflow (`i` / `r`), see [No amino acid data — the Claude fetch workflow](#no-amino-acid-data--the-claude-fetch-workflow).

**7. My Pantry (foods you have on hand)**

A persistent list of protein foods currently in stock. Pantry foods appear at the top of complement suggestions — the program recommends what you can actually use, not just what is theoretically ideal. Each entry can be linked to a USDA food (bringing full amino acid data) or stored by name only. The AA column shows ✓ (data in cache), ✗ (USDA-linked but no AA data), or — (name-only entry). See [Protein complement suggestions](#protein-complement-suggestions).

**8. Custom food profiles (create and edit your own food data)**

Opens the **Drafted Food Profiles** submenu with five items:

| Item | Action |
|------|--------|
| 1. List | Show all user-drafted profiles |
| 2. Create | Build a new profile from scratch or pre-filled from a USDA food |
| 3. Edit | Edit name, serving, nutrients, or note for an existing draft |
| 4. Delete | Remove a drafted profile |
| 5. Copy | Clone any cached food (USDA, OFF, or existing draft) as a new editable draft |

Create supports a **supplement/unit-based mode** for tablets, capsules, softgels, and scoops — enter per-label amounts directly without converting to grams. Nutrient entry covers macros, minerals, vitamins (IU auto-converted for A, D, E), amino acids (one-by-one or bulk import from g/100 g protein), and phytonutrients. See [Drafted food profiles](#drafted-food-profiles-user-modified-nutrients).

**9. Annotate a food (add your GI / DIAAS estimates)**

Pick any cached food and attach your own estimates for glycemic index (0–100) and/or DIAAS (0.0–1.5), plus an optional preparation-context note ("cooked", "raw", etc.). Each value can be skipped (ask again next time) or suppressed (never prompt again for this food). Suppression can be re-enabled, and all annotations for a food can be cleared, from this same flow. Annotations are also accessible from within the Food Cache (`e#`). See [Food annotations (GI and DIAAS estimates)](#food-annotations-gi-and-diaas-estimates).

---

### Recipes Menu

**Title:** Recipes

The Recipes menu covers the full lifecycle of a recipe: creation, browsing, editing, copying, analysis, iterative development, and saved portion analysis.

**1. Create new recipe**

A sequential wizard: name → description → servings → serving size (optional) → total volume (optional) → total weight (optional) → complete? → add ingredients (search + portion, looped) → procedure (opens a text editor, optional) → save. Each ingredient is linked to a cached food by FDC ID; the program searches and caches automatically if the food is not yet stored. Digestible complete protein (DCP) is computed and saved on first ingredient addition and recomputed on any subsequent change.

**2. Browse / view, edit, copy, delete recipes**

Displays the 20 most recently accessed recipes with total recipe count. Commands are typed as a letter followed immediately by the recipe's DB ID (e.g. `v3`, `x14`):

| Command | Action |
|---------|--------|
| `v<id>` | View/edit — displays name, description, servings, volume/weight, ingredients with amounts and notes, and procedure text (no nutritional analysis), then prompts `e=edit  b/Enter=done`. Pressing `e` opens the full edit flow: step through metadata (name/description/servings/serving size/complete flag), manage ingredients (add/edit/remove/reorder), then optionally edit procedure. All changes are saved even if you exit early with b/q/Ctrl+C. DCP is recomputed on any ingredient change. |
| `a<id>` | Analyze — full nutritional analysis (see below). |
| `x<id>` | Develop — launch the iterative Develop workflow (item 3) on this recipe. |
| `c<id>` | Copy — prompts for a name (default: "Copy of …"), saves an exact duplicate with all ingredients, description, servings, volume/weight, and procedure. |
| `d<id>` | Delete — confirm, then permanently remove. |
| `s` | Search — filter recipes by one or more words (results ranked by number of matching words, capped at 20). |
| `r` | Recent — return to the "20 most recently accessed" view after a search. |

Accessing a recipe via any action stamps its `last_accessed_at` timestamp, keeping the recent list current.

**Recipe analysis** (used by `a<id>` in Browse and by Develop):

Shows name, description, ingredient list with amounts and notes, and procedure before any calculation, so the recipe is fully visible when making decisions about missing data. Then: total nutrients + DCP (saved to DB) + optional bioavailability breakdown + protein completeness + complement suggestions.

- If servings > 0: per-serving nutrients; DCP is per-serving.
- If servings = 0: whole-recipe totals + per-100 g (if total weight recorded) + per-100 ml and per-cup (if total volume recorded).
- If any ingredient lacks amino acid data or weight, a numbered Options menu offers: provide the missing values, calculate anyway (approximate, not saved), or skip.

Non-protein ingredients (spices, oil, salt) can safely be skipped in the missing-data warning list.

**3. Develop a recipe (add/remove ingredients with nutritional feedback)**

A focused loop for iterative ingredient development. Pick a recipe, then loop:

| Command | Action |
|---------|--------|
| `a` | Add ingredient — food search → portion → optional note → added to recipe; then optionally run full analysis on the updated recipe. |
| `r` | Remove ingredient — pick by number from the displayed list → removed; then optionally run full analysis. |
| `d` | Done — exit the loop. |

After the loop: optional access to the Procedure editor. DCP is recomputed and saved on exit if any ingredients changed. Also accessible from Browse via `x<id>`.

**4. Analyze a recipe portion (saves analysis with date)**

Runs the full nutritional analysis for a chosen recipe and automatically saves a plain-text snapshot of the report to the database with an ISO timestamp. On subsequent calls for the same recipe, the user is prompted:

- `s` — Show the saved analysis (printed to the terminal; date shown).
- `r` — Redo the analysis (overwrites the saved snapshot).
- `b` — Cancel.

The `a<id>` command in Browse also runs the full analysis but does **not** save a snapshot. Item 4 is the intended path when you want a persistent record of where a recipe stands at a point in time.

Storage: `recipes.saved_analysis_at` (ISO UTC timestamp) and `recipes.saved_analysis_text` (plain text string).

---

### Meals & Log Menu

**Title:** Meals & Log

Displays up to 15 recent meals, most-recent first, as an inline numbered list with date, name, item count, and completion status. Commands are entered at the prompt:

| Command | Action |
|---------|--------|
| `n` | New meal — prompts for date (default today) and name, then opens the meal action loop. |
| `v<id>` | View / edit meal — shows items, then the **meal action menu** (see below). |
| `a<id>` | Analyze meal — full nutrient table + meal-level DIAAS (pooled, digestibility-corrected) + protein completeness + complement suggestions + glycemic load. If multiple meals share the date, choose single or combined. |
| `d<id>` | Delete meal — confirm before removing. |
| `s` | Search food across entire meal history. |
| `mr` | Show next 15 meals (older). |
| `d<YYYY-MM-DD>` | Jump to meals on or before the given date. |

**Meal action menu** (opened by `v<id>`):

| Item | Action |
|------|--------|
| 1. Add items | Unified search — recipes first, then USDA/OFF foods; add by portion or servings. |
| 2. Edit an item | Change food, amount, or note for a logged item. |
| 3. Delete an item | Remove one item from the meal. |
| 4. Analyze this meal | Same analysis as `a<id>` from the list. |
| 5. Delete this meal | Confirm, then remove the whole meal. |
| 6. Mark complete / incomplete | Toggle the meal's completion status. |
| 7. Rename this meal | Edit the meal name. |
| 8. Merge with meal(s) on same date | Combine multiple meals logged on the same date (shown only when applicable). |

See [Logging a meal](#logging-a-meal) and [Meal-level DIAAS analysis](#meal-level-diaas-analysis) in the Usage Guide.

---

### Daily Summary Menu

**Title:** Daily Nutrition Summary

Aggregates all meals logged on a given date and presents a single combined nutrient breakdown, meal-level DIAAS analysis, protein completeness assessment, and complement suggestions.

| Item | Action |
|------|--------|
| 1. Today's summary | Sums all meals logged today. |
| 2. Summary for a specific date | Prompts for a date (YYYY-MM-DD) and sums all meals on that date. |
| 3. Recent days | Lists dates that have logged meals, most recent first. Select a date to view its summary. |

See [Daily summary](#daily-summary) in the Usage Guide.

---

### Settings Menu

**Title:** Settings

Configuration for appearance, user profile, dietary preferences, and program behaviour. Current values are displayed inline in each menu item.

| Item | Action |
|------|--------|
| 1. Color theme | Switch between dark, light, neutral, and auto themes. Auto follows the terminal's background. Change takes effect immediately. |
| 2. User profile | Set age, sex, weight, height, and activity level. Used to compute Recommended Daily Allowances (RDAs) shown in nutrient tables and the daily summary. |
| 3. View daily nutrient targets | Display the current RDA/goal table based on the stored user profile. |
| 4. Dietary preferences | Choose which protein sources appear in complement suggestions: all animal foods, vegetarian (dairy + eggs), or plant-based only. Saved immediately to `~/.config/numa/prefs.json`. |
| 5. Editor command | Set the command used to open the procedure editor (e.g. `nano`, `vim`, `code --wait`). Leave blank to use the `$VISUAL`/`$EDITOR` environment variable. Enter `-` to clear back to system default. |
| 6. Display program settings at launch | Toggle whether the startup banner shows theme, profile, and dietary preference. |
| 7. Advanced settings | Opens the Advanced Settings submenu (see below). |

**Advanced Settings submenu:**

| Item | Action |
|------|--------|
| 1. Protein digestibility overrides | Add, edit, or remove per-food true ileal digestibility coefficients used by the meal-level DIAAS calculation. Overrides take precedence over the curated table and category defaults in `diaas.py`. |
| 2. USDA API key | Enter or update the key used for all USDA FoodData Central API calls. Required for food search and detail fetch; the program will not search USDA without it. |
| 3. Storage location | Display the path of the SQLite database file. Read-only. |

See [Dietary preferences](#dietary-preferences) and [Protein digestibility — DIAAS](#protein-digestibility--diaas) in the Usage Guide.

---

## Usage Guide

### The local food cache

NutriMagnus does not store full nutrient profiles for every food in a built-in database. Instead it fetches them on demand from USDA FoodData Central (or Open Food Facts) and saves each result to a **local food cache** — a SQLite table on your machine. Once a food is cached, it is available instantly on every subsequent search and analysis, with no network access required.

**When a food enters the cache:**
A food is cached the moment you **pick it** from a search results table — not during the search itself. Browsing results does not cache anything; selecting a result triggers the fetch-and-cache step. If you pick a food that is already cached, the stored copy is returned immediately and no network call is made.

**Cache quick-pick:**
Before showing API search results, the program checks your cache for name matches and offers them in a fast "Food cache" table. This lets you reuse a cached food without waiting for a network search. Foods in the cache that lack USDA portion data are included in this table; selecting one triggers a background USDA refetch to complete the entry.

**Overwrite protection for edited foods:**
Once you edit a food's nutrients through Food Cache (or create a food manually), it is marked `user_drafted = True`. Any subsequent USDA fetch for the same food — triggered by selecting it from a search results table — will not overwrite a user-drafted entry. Your manual edits, AA patches, and custom notes are permanent unless you explicitly edit or delete them.

**What is stored:**
Name, data type, brand (if any), serving size and unit, the full nutrient profile (macros, minerals, vitamins, amino acids, omega fatty acids), and USDA portion data (e.g. "1 cup, chopped"). All nutrient values are per 100 g.

**Automatic omega fatty acid backfill:**
When a cached USDA food is selected and its stored nutrients are missing all four omega keys (`omega3_ala_mg`, `omega3_epa_mg`, `omega3_dha_mg`, `omega6_la_mg`), the program silently fetches and merges just those nutrients from the USDA API and updates the cache entry. This happens transparently on first use; subsequent accesses use the updated cache. User-drafted foods are never touched by this backfill.

**Viewing and managing the cache:**
Starting with the main menu, select **Foods → Food cache** to list every cached food with filter-by-name suppor/act. From there you can view its full nutrient profile, analyze a portion, or delete the entry. Deleting forces a fresh fetch the next time you search for that food — useful if the cached data looks corrupt or outdated.

---

### Food annotations (GI and DIAAS estimates)

The `food_annotations` table stores user-supplied estimates attached to individual cached foods by `fdc_id`. These fill gaps where official data is absent — particularly glycemic index (not available in any free API) and DIAAS for foods without amino acid data.

**What can be annotated:**

| Field | Scale | Notes |
|---|---|---|
| `gi_estimate` | 0–100 | Glycemic index (glucose = 100). Low < 55, medium 55–69, high ≥ 70. |
| `diaas_estimate` | 0.0–1.5 | Protein digestibility. 1.0 = fully digestible. |
| `prep_context` | text | Free-form context: "cooked", "raw", "soaked then boiled", etc. |

**How to annotate a food:**

- **Foods → 8. Annotate a cached food** — filterable list of all cached foods → pick one → annotation editor.
- **Foods → 5 → pick food → 4. Annotate** — same editor, reached from the cached food viewer.

Inside the editor you can set or update each field, re-enable prompts (if you had previously chosen "never ask"), or clear all annotations for that food.

**Prompt behavior:**
When a GI or DIAAS value is needed during analysis and none is on file, the program prompts inline. At that prompt:

| Input | Effect |
|---|---|
| A number | Value saved and used immediately |
| Enter or `s` | Skip — value not saved; will ask again next time |
| `x` | Never ask again for this food — prompt suppressed permanently |
| `b` | Cancel the current action |

The `gi_no_prompt` and `diaas_no_prompt` flags stored in `food_annotations` control this suppression. Clearing annotations (via the editor) also resets these flags.

**Visibility in search results:**
The **Ann** column in search result tables shows `GI`, `DI`, or `GI DI` (green) when estimates exist, helping you choose a cached food over an equivalent unannotated result from a remote source.

**Visibility in the cached food list:**
**Foods → 5. View cached / saved foods** shows `AA`, `GI`, and `DIAAS` columns so the state of each food is visible at a glance without opening it.

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

**Food Cache vs Drafted Food Profiles:**
The "Drafted Food Profiles" list is a filtered view of the same `foods` table — `WHERE user_drafted = 1`. A food becomes `user_drafted = True` when you create it manually or when you edit its nutrients through Food Cache. Editing a food in Food Cache immediately affects what Drafted Food Profiles shows, and vice versa, because they are the same row.

`user_drafted = True` also activates overwrite protection: all code paths that write a fresh USDA fetch result to the cache check this flag first and skip the write if it is set. This means manual AA patches, serving-size corrections, and other edits survive repeated searches for the same food.

**Pantry:**
The `pantry` table has its own `id` (autoincrement), a `food_name` text field, and a nullable `fdc_id` FK pointing into `foods`. A pantry entry can exist without a cache entry (name-only). When `fdc_id` is set, all nutrient calculations use the live `foods` row — so editing that food in Food Cache instantly updates any pantry-based analysis. However, the pantry stores its own `food_name` string; renaming a cached food does not update the pantry display name.

**Annotations:**
The `food_annotations` table is keyed by `fdc_id` and foreign-keyed to `foods` (`ON DELETE CASCADE`). Annotations are visible everywhere that food appears — search results, cache list, analyses — because they are always looked up by `fdc_id`.

**Editing rule:**
All nutrient editing goes through **Food Cache** (Foods → 6). Both the Drafted Food Profiles menu and the Pantry menu redirect there for edits and display a notice to that effect. This keeps a single edit path regardless of how you reached the food.

---

### Drafted food profiles (user-modified nutrients)

When a food lacks complete official data — or when you want to model a modified version (different cooking method, fortification, substitution) — you can build a **drafted food profile** with your own nutrient values.

**Foods → Drafted food profiles → Create new drafted profile**

The creation flow:
1. Choose to **start from a USDA food** (searches the database and pre-fills all nutrient values, which you then override) or **start from scratch**.
2. Enter a name.
3. **Supplement check** — the program asks "Is this a supplement?" (tablet, capsule, softgel, etc.). If yes, enter the unit name; the entry is stored in supplement mode (see below). If no, enter the serving size and unit normally.
4. Enter nutrient values — the prompt walks through five sections:
   - **Basic macros** (always prompted): calories, protein, fat, carbs, fiber, sugars, saturated fat, mono/poly fats, sodium.
   - **Minerals** (optional, default y if existing data): calcium, iron, magnesium, phosphorus, potassium, zinc.
   - **Vitamins** (optional): A, C, D, E, K, B1 (thiamin), B2 (riboflavin), B3 (niacin), B6, B9 (folate), B12. Vitamins A, D, and E can be entered in IU — the program converts to mcg/mg automatically and shows the math.
   - **Amino acids** (optional): one-by-one (g per 100g food), bulk import from literature (g per 100g protein — auto-converted), or skip.
   - **Phytonutrients** (optional): beta-carotene, alpha-carotene, lycopene, lutein+zeaxanthin, choline, beta-sitosterol, isoflavones.
5. Enter an optional note to document your sources and assumptions.

Drafted profiles are saved into the food cache with a small negative ID (−1, −2, −3…) displayed as `usr`. They appear at the top of search results (as cached foods always do), are labeled **User Drafted** in the Type column, and can be used anywhere a regular cached food can — portion analysis, recipes, meal logging, complement suggestions. They can be edited or deleted from the same **Drafted food profiles** menu.

#### Supplement / unit-based mode

Vitamins, minerals, and other supplement tablets are sold in per-tablet amounts, not per-100g amounts. Supplement mode solves this: by treating 1 tablet as equivalent to 100g internally, the stored per-100g values exactly equal the per-tablet label values. No weighing is required.

**Creating a supplement:**
When you answer yes to "Is this a supplement?", the program asks for the unit name (default: `tablet`; other common values: `capsule`, `softgel`, `pill`, `scoop`). Serving size and unit are set automatically (`1 tablet`). Enter nutrient values exactly as printed on the label — e.g., if the label says "Vitamin B12: 5000 mcg per tablet", enter `5000` at the Vitamin B12 prompt. When you later log "1 tablet" in a meal, those exact amounts are added to your nutrient totals.

**Editing an old entry to convert it to supplement mode:**
Open the entry via **Drafted food profiles → 3. Edit**. If the entry is user-drafted and not already in supplement mode, the program asks "Is this a supplement?" at the start of the edit session. Answer yes and confirm the unit name — the gram_weight=100 portion is added automatically, preserving any nutrient values you already entered.

**IU input for vitamins A, D, and E:**
Many US supplement labels express these vitamins in International Units. At those prompts, enter the number followed by `IU` (e.g. `400 IU` or `5000iu`). The program converts automatically:
- Vitamin A: 1 IU = 0.3 mcg RAE
- Vitamin D: 1 IU = 0.025 mcg
- Vitamin E (natural d-alpha-tocopherol): 1 IU = 0.67 mg

The conversion math is shown on screen so you can verify it against the label.

---

### Searching for a food

Select **Foods → Search food databases**, enter a search term (e.g., "chicken breast"), and pick from the results table. The program fetches the full nutrient profile and caches it locally so subsequent lookups of the same food are instant.

**Barcode search:** At any food search prompt, enter a 12-digit UPC-A or 13-digit EAN barcode (digits only, spaces or hyphens ignored). The program looks the product up on Open Food Facts by barcode, shows the product name and brand, and asks whether to use it. If found, the product is cached and its nutrient data returned exactly as for a name search. Barcode search is the recommended method for dietary supplement labels, which often have an OFF entry while lacking any USDA record.

Every search queries the **local food cache first**, then USDA FoodData Central (and Open Food Facts for unrestricted searches). All results are merged into a single table so you always see every available option in one view.

**Result ordering** — results are ranked in this order:

1. **Local cache** — foods you have already fetched always appear first
2. **Annotated cache hits** — within cached foods, those with GI or DIAAS estimates on file sort above unannotated ones
3. **USDA Foundation Foods and SR Legacy** — whole-food entries with the most complete nutrient profiles
4. **Open Food Facts** — community-sourced packaged foods
5. **Branded (USDA)** — commercial products

If the search string contains a brand name (any brand word of four or more characters that appears in a result's brand field), the ranking switches to relevance order (most query-word matches first) so the specific product you named surfaces at the top; cache and annotation status still apply as tiebreakers.

The results table always includes an **AA data** column (✓ confirmed / ~✓ likely / ✗ none) and an **Ann** column showing which foods have GI and/or DIAAS estimates saved (`GI`, `DI`, or `GI DI` in green; `·····` if none). Use these columns to pick the option with the richest existing data before committing to a fetch.

After viewing the full nutrient breakdown, the program now offers to immediately proceed to portion analysis for the same food — saving you from navigating back to "Analyze a food portion".

#### Too many branded results?

The USDA database contains many packaged/branded food entries. A
simple search like "pinto beans" will often return 25 branded products (canned
goods, mixes, etc.) rather than the plain cooked food you want.

For home-cooked or generic foods, add descriptive terms to narrow the results:

| Instead of… | Try… |
|---|---|
| `pinto beans` | `pinto beans cooked` |
| `chicken` | `chicken breast cooked` |
| `rice` | `brown rice cooked usda` |
| `oats` | `oats rolled raw usda` |

Adding **`cooked`** or **`raw`** targets the USDA Foundation Foods and SR Legacy
datasets, which cover whole foods with full nutrient profiles (including amino
acid data for protein completeness). Adding **`usda`** further filters toward
those non-branded entries.

The program will display a tip automatically when most of your search results
are branded products.

### Analyzing a portion

Select **Foods → Analyze a USDA food portion**. After picking a food, enter your portion size. Accepted formats:

| Input | Example | Notes |
|---|---|---|
| Plain number | `2` | Pieces / count (no gram weight) |
| Piece unit | `2 pc`, `3 each` | Pieces / count — same as bare number |
| Weight | `150 g`, `65 gr` | Grams |
| Fraction weight | `1/4 g` | Treated as grams |
| Mixed number weight | `1 1/2 oz` | Treated as weight with unit |
| Weight with unit | `3 oz`, `0.5 lb` | Converted to grams |
| Volume | `1/4 cup`, `2 tbsp` | Converted via food density |
| USDA portion shortcut | `p1`, `p2` | Uses gram weight shown in the portions list |
| Portion multiple | `1.5 p1` | 1.5 × the gram weight of portion 1 |

> **Pieces vs. weight:** A bare number (e.g. `2`) means 2 pieces/count — no gram weight is recorded and the ingredient's nutritional contribution is zero in the totals. To record a gram weight, always include a unit: `150 g`, `3 oz`, `1/4 cup`. Accepted piece-unit words: `pc`, `pcs`, `piece`, `pieces`, `each`, `ea`, `count`, `ct`, `item`, `items`.

Volume inputs (`cup`, `tbsp`, `tsp`, `ml`) are converted to grams using the food's density. Density is derived from the USDA portions data when available (e.g., if USDA lists "1 cup = 240 g", that is used directly). For foods without a cup/tablespoon portion entry, a built-in density table covers common whole foods. If density cannot be determined, the program will say so and ask for grams instead.

Nutrients are scaled proportionally from the 100g USDA reference values.

### Analyzing a recipe portion

Select **Foods → Analyze a saved recipe portion**. The program lists saved recipes; enter the recipe ID, then specify how many servings (whole number, fraction, or decimal — e.g., `2`, `0.5`, `1.5`). The recipe's total nutrients are scaled to that portion and displayed with full protein completeness analysis.

### Protein completeness

Wherever protein is analyzed (food, recipe, or meal), numa automatically checks whether the protein is "complete" — meaning it contains all nine essential amino acids at or above the FAO/WHO reference levels. This requires that the USDA entry for the food includes amino acid data (most whole foods in the Foundation and SR Legacy datasets do).

The output shows:
- Complete / Incomplete designation
- The most limiting amino acid (if incomplete)
- A score bar for each essential amino acid vs. the reference level

> For a deeper explanation of what the FAO reference values are, where they come from, and how to interpret ratios above 1.0, see the [Appendix — Understanding Protein Quality](#appendix---understanding-protein-quality-the-fao-reference-values-and-diaas).

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

Some USDA entries — particularly SR Legacy and Branded foods — omit amino acid
data. If the selected food has none, numa will display:

```
(No amino acid data available for protein completeness analysis.)
```

and immediately offer to search **Foundation Foods** for an equivalent entry.
Foundation Foods is USDA's most curated dataset and almost always includes a
full amino acid profile. The search is pre-filled with the first keyword(s) of
the original food name (e.g., "beans, pinto, mature seeds, cooked, boiled, with
salt" becomes "beans"). You can accept the suggestion, refine the query if
needed, and pick from the Foundation results without leaving the current flow.

#### No amino acid data — the Claude fetch workflow

When no Foundation Foods substitute is available, numa provides a two-step interactive workflow to retrieve amino acid (and other nutrient) data from Claude AI (claude.ai) and import it directly into the cache.

**Access** — **Foods → 5. View cached / saved foods**, commands printed below the table:

| Command | Action |
|---------|--------|
| `i#` / `i#,#` | Generate prompt for specific row(s) — e.g. `i3`, `i1,4,7` |
| `i` alone | Generate prompt for every ✗ food in the current list (with confirmation) |
| `r` | Read and import `~/claude_response.txt` |

**Step 1 — prompt generation (`_do_claude_fetch` in `foods.py`).**

Builds the food list from the selected rows (or all ✗ foods if no row numbers are given) and writes `~/claude_prompt.txt` using `_CLAUDE_PROMPT_TEMPLATE`. The template instructs Claude to return one fenced JSON block per food containing:

- **Metadata keys**: `name`, `fdc_id`, `fdc_type`, `source`, `confidence_note`
- **Nutrient keys**: all recognized fields (macros, minerals, vitamins, phytonutrients, and all 11 amino acids), per 100 g edible portion

Key rules embedded in the template: amino acid values must be in grams per 100 g food (not per g protein, not mg); `aa_methionine_g`/`aa_cystine_g` and `aa_phenylalanine_g`/`aa_tyrosine_g` must always be separate keys; unknown values must be omitted entirely (never zero-filled); true zeros may be included explicitly; source hierarchy is USDA FDC → SR Legacy → peer-reviewed literature → estimate.

After writing the file, the function prints a four-step instruction block: open the file, copy its entire contents, paste into a **new** claude.ai chat, and — critically — copy only Claude's reply text (not the full conversation) before saving as `~/claude_response.txt`.

**Step 2 — response import (`_do_claude_import` in `foods.py`).**

Reads `~/claude_response.txt` and passes it to `_claude_parse_response()`, which extracts fenced (` ```json ``` `) and bare JSON objects. Any non-JSON text trailing the last JSON block is collected as **curator text** — Claude's methodological caveats, confidence statements, and batch-level notes.

Each block is validated by `_claude_validate_block()`: it must have `name` (string), `fdc_id` (integer or integer-string), and a valid `fdc_type`; unrecognized nutrient keys are stripped silently; blocks that fail validation are reported and skipped.

Passing blocks are shown in a review table — name, FDC ID, calories, protein, and AA count out of 11 — before the user confirms. On confirmation, each food is written via `_db.cache_food()` with:
- `notes` — formatted from `source` and `confidence_note`
- `curator_notes` — the batch-level curator text (shown in the N column; readable with `n#`)
- `user_drafted` **not set** — entries remain overwritable by subsequent USDA re-fetches (omega backfill, incomplete-cache detection)

#### No amino acid data — `import_foods.py` (scripted alternative)

For stable, literature-sourced food records that need to survive repeated numa updates, `import_foods.py` is a standalone Python script that bypasses the interactive workflow. Food dicts are hardcoded in its `_FOODS` list (one per food, with the same nutrient key conventions as the Claude prompt template). Running the script imports all entries via `cache_food(..., user_drafted=True)`.

The `user_drafted=True` flag is the critical difference from the Claude import path: it prevents USDA re-fetches from overwriting the imported data. Without it, the omega backfill or incomplete-cache detection paths in `_fetch_food_from_result` can silently replace a manually curated entry with raw USDA data (which for Branded foods typically lacks amino acids). Re-running the script is always safe — `cache_food()` uses `INSERT OR REPLACE`, so existing entries are updated in place.

The script does not include portion data; `portions_json` is stored as an empty array `[]` via `json.dumps(portions or [])`.

### Protein digestibility — DIAAS

Wherever a food is analyzed (search, portion analysis, recipe, or meal), numa automatically displays a **Bioavailability** section if it has data for that food. This section reports two things: the DIAAS score and any anti-nutrient advisories (see next section).

#### What DIAAS is

**DIAAS** (Digestible Indispensable Amino Acid Score) is the current international standard (FAO, 2013) for measuring protein quality. It answers a different question than the amino acid completeness check above: not *are all the amino acids present*, but *how much of the protein does the body actually absorb and use?*

The score runs from 0 to 1.0 (values above 1.0 are capped at 1.0):

| Score | Meaning |
|---|---|
| 1.0 | Fully digestible — essentially all protein is usable |
| 0.75–0.99 | Good digestibility — modest losses |
| 0.50–0.74 | Moderate digestibility — significant losses |
| < 0.50 | Poor digestibility — most protein is not absorbed |

This matters most for plant-based diets. While raw protein figures often look similar across food sources, the body's actual access to that protein varies considerably:

| Food | DIAAS | Raw protein × DIAAS = usable |
|---|---|---|
| Egg / whey protein | 1.0 | 20 g × 1.0 = 20 g |
| Soy protein isolate | 0.97 | 20 g × 0.97 = 19.4 g |
| Chickpeas | 0.83 | 20 g × 0.83 = 16.6 g |
| Lentils | 0.75 | 20 g × 0.75 = 15.0 g |
| Brown rice | 0.59 | 20 g × 0.59 = 11.8 g |
| Wheat (whole) | 0.46 | 20 g × 0.46 = 9.2 g |

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

### Meal-level DIAAS analysis

Analyzing a meal or daily summary now shows a deeper **Meal-level DIAAS Analysis** section, computed by `diaas.py`, that goes beyond the per-food scores described above.

#### Why meal-level matters

When you eat multiple protein sources together, their amino acid profiles combine. A food with too little lysine paired with a food rich in lysine produces a meal whose composite lysine level is higher than either food alone. The per-food DIAAS approach misses this entirely. The meal-level calculation captures it.

#### The calculation

For each ingredient:

1. Look up the food's true ileal digestibility coefficient (0–1) — not the same as DIAAS. This is the fraction of each amino acid that is actually absorbed in the small intestine.
2. Multiply each essential amino acid (IAA) amount by that digestibility factor to get **digestible IAA grams**.

Then across all ingredients:

3. Pool the digestible IAA grams for each of the nine essential amino acids.
4. Divide each pooled total by the FAO 2013 adult reference (mg/g protein) applied to the meal's total protein.
5. The composite DIAAS is the ratio of the most limiting IAA. **Digestible complete protein** = total protein × min(composite DIAAS, 1.0).

This is the methodology from FAO Food and Nutrition Paper 92 (2013).

#### The output

```
  Meal-level DIAAS Analysis  (digestibility-corrected, pooled across ingredients)
  ──────────────────────────────────────────────────────────────────────────────

  Ingredient               Protein  Digestibility  Digestible prot
  Soy protein isolate       14.4g    0.95              13.7g
  Pea protein powder         8.0g    0.92               7.4g
  Ground flax seed           0.9g    0.85               0.8g

  Amino acid ratios vs. FAO adult reference  (≥1.0 = meets reference)
  Histidine      1.341  █████████████
  Isoleucine     1.362  █████████████
  Leucine        1.119  ███████████
  Lysine         1.130  ███████████
  Met+Cys        0.841  ████████     ← LIMITING
  Phe+Tyr        1.117  ███████████
  Threonine      1.292  ████████████
  Tryptophan     1.704  █████████████████
  Valine         1.084  ██████████

  Composite DIAAS: 0.841  (utilization efficiency: 84%)
  Digestible complete protein: 19.4g  from 23.1g total
```

The ingredient table shows the digestibility coefficient used for each food and flags estimated values with `~est`. The IAA table shows each amino acid's composite ratio; the limiting one is marked. Met+Cys and Phe+Tyr are combined pairs per the FAO methodology.

If any ingredient lacks amino acid data in the USDA cache, it is excluded from IAA pooling and listed in a note. If tyrosine data is absent (it was not tracked before April 2026; re-fetch foods to get it), the Phe+Tyr row is flagged as a gap.

#### Filling missing AA profiles at analysis time

When a meal has ingredients without AA data, the analysis reports how many are affected and distinguishes two categories:

- **Inside a recipe** — the ingredient is part of a recipe logged as a meal item. To fix these, edit the recipe directly (Recipes → browse → edit ingredients) and replace or re-fetch the ingredient there.
- **Standalone meal ingredients** — foods logged directly to the meal (not inside a recipe). These can be replaced interactively: the program offers a `y/n` prompt asking whether to search for a substitute.

If you answer `y`, for each affected standalone ingredient the program runs a focused search of USDA **SR Legacy** and **Foundation** foods — the datasets most likely to include full amino acid profiles. The **AA** column in the results table (✓/✗) shows at a glance which candidates have AA data. Picking a replacement updates that ingredient in the meal for the current analysis session. Press Enter to skip an ingredient and leave it excluded from IAA pooling.

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

Wherever protein is analyzed, numa checks for essential amino acid gaps and — if any exist — offers to show complement suggestions:

```
Show protein complement suggestions?  (y/N)
```

Press `y` to see the suggestions. The flow is:

1. **Pantry suggestions** — foods from your My Pantry list that can close the gap, shown first, ranked by gaps closed then by smallest required amount (up to 3 per page).
2. After the pantry section, you are asked: `Look elsewhere for more options?  (y/N)` — if yes, the general list is shown.
3. **General suggestions** — foods from a curated built-in table of common plant protein sources, shown up to 5 at a time. These entries contain only protein and the nine essential amino acids (no full nutrient profile) and are used exclusively for complement scoring — they do not appear in food search results and cannot be added as recipe ingredients.

If no general options qualify, numa explains why:

```
  No other qualifying options found in the database.
  A qualifying complement must have a high enough Methionine / protein ratio
  to close the gap to the FAO reference level (score 1.0) in a practical serving (≤ 500g).
  Score 1.0 means the combined profile meets human requirements — not that it exceeds them.
  Foods that bring the score only partway toward 1.0 are not listed because the gap would remain.
```

Each suggestion shows:

```
  Option 1  Brown rice, cooked  DIAAS 0.59
    Pair with: 185g  (≈ ¾ cup)
    Effect: Lysine: 0.54→1.00 · Threonine: 0.81→0.92
    Adds: 7.2g digestible protein  (from 12.2g raw)
    Total bioavailable complete protein now = 19.4g
```

- **Name** and DIAAS digestibility score
- **Grams to add** — the minimum amount that brings the most limiting amino acid to exactly 1.0 (the FAO reference requirement level)
- **Effect** — before → after scores for the top-gap amino acids (green = meets reference, yellow = improved but still below)
- **Digestible protein added** — the complement's raw protein × its own DIAAS score.
- **Total digestible complete protein** — computed as `(base_protein + complement_protein) × min(1.0, base_digestibility × new_pool_raw_min)`, where `new_pool_raw_min` is the minimum raw AA score (vs. FAO reference) across all essential amino acids in the combined pool, and `base_digestibility` is the base meal/recipe's DIAAS. This reflects the pooled-DIAAS approach used by `diaas.py`: all ingredients contribute their amino acids to a single pool, and the pool's limiting AA determines how much of the total protein counts as "complete."

  A complement that fixes the primary gap but dilutes a different amino acid will show a modest total — the pooled DIAAS drops because the new limiting AA is weaker than what the base alone achieved. This is correct and expected: a low-quality complement (e.g. DIAAS 0.45) may add only a small net DCP gain even though it technically closes the target gap.

  For DIAAS-improver suggestions the formula is different: `(base_protein + raw) × min(1.0, new_diaas)` where `new_diaas` is supplied directly from the pooled re-calculation in `suggest_complements`.

**Why score 1.0?** The score is a ratio against the FAO 2013 reference pattern (mg of amino acid per g of protein that humans require). A score of 1.0 means the combined profile exactly meets requirements — it is the floor, not an aspirational target. Suggesting a complement that only reaches 0.85 would mean the gap remains open.

The advisor is triggered automatically at the end of food search, portion analysis, recipe view, meal analysis, and daily summary — wherever amino acid data is present. If the food has no amino acid data, the offer is skipped silently.

The pantry is the key input: populate **Foods → My pantry** with the protein sources you keep on hand and the advisor will always prioritize those over generic suggestions.

### Dietary preferences

**Settings → Dietary preferences** controls which protein sources appear in complement suggestions. There are three options:

| Option | Value | What is included |
|--------|-------|-----------------|
| 1 | `all` | All animal foods — meat, fish, dairy, eggs, whey |
| 2 | `vegetarian` | Dairy + eggs only (no meat or fish) |
| 3 | `plant_only` | Plant-based sources only |

The setting is saved immediately to `~/.config/numa/prefs.json` (key: `diet_pref`) and applied to both interactive complement suggestions and exported reports.

### Building a recipe

Select **Recipes → Create new recipe**. The create flow prompts for:

1. **Name** — required.
2. **Description** — optional free text.
3. **Number of servings** — defaults to 0. A value of 0 means the recipe has no fixed serving count; analysis will be presented as whole-recipe totals plus per-100g and/or per-100ml breakdowns (depending on whether total weight or volume was recorded). A positive integer enables per-serving analysis.
4. **Total volume** — optional; enter as `NUMBER UNIT`, e.g. `4 cups` or `500 ml`. Press Enter to skip.
5. **Total weight** — optional; enter as `NUMBER UNIT`, e.g. `800 g` or `1.5 lb`. Press Enter to skip.
6. **Procedure** — opens the configured text editor; press Enter to open, `b` to skip.

After the header fields, the ingredient-entry loop begins. Cancelling at any prompt during header entry (Ctrl+C, `b`, `q`) still saves the recipe with whatever was entered up to that point — no data is lost.

Each ingredient is stored with its weight (or piece count). When you analyze the recipe, numa calculates total nutrients and per-serving nutrients by summing all ingredients scaled to their specified gram amounts; piece-count ingredients contribute zero to nutrient totals.

Total volume and total weight can be edited at any time via **Recipes → Edit recipe** (they appear after name/description/servings in the metadata step, current values shown as blue defaults). Any field changes made before pressing `b`, `q`, or Ctrl+C during editing are always saved before exiting.

### Copying a recipe

Select **Recipes → Copy a recipe**. The program lists saved recipes; pick one by ID, then enter a name for the copy (press Enter to accept the default "Copy of …"). The copy is saved immediately with all ingredients, description, servings, total volume, total weight, and procedure text identical to the original. The copy is fully independent — editing or deleting either does not affect the other. DCP is not copied; it is recalculated the first time you analyze the new recipe.

### Logging a meal

Select **Meals & Log → Log a meal**. If meals already exist today, you can add items to one of them instead of creating a new one. For a new meal, enter a date (defaults to today) and a name. Then add items using the unified search: type any name and matching saved recipes appear at the top of results (labelled R1, R2 …) above USDA/OFF food results. Pick R# to add a recipe by servings; pick a number to add a food item by portion. Each food item has an optional Note field (e.g., brand, preparation). The meal is timestamped and stored.

### Saved nutrition reports

After any analysis that produces a report (food search, portion analysis, recipe analysis, meal analysis, daily summary), numa automatically saves a Markdown report to `~/.numa/reports/`. The filename encodes the food or recipe name and a timestamp (e.g. `chicken_breast_cooked_20260418_1045.md`).

**After auto-saving, the full file path is printed in the terminal**, for example:

```
  Report auto-saved → /home/you/.numa/reports/chicken_breast_cooked_20260418_1045.md
```

If a previous report exists for the same subject, numa lists it before saving and offers to view it instead of creating a new one. At that prompt you can:

- Enter a number to view that existing report in the terminal.
- Enter `new` to proceed with saving a fresh report.
- Press Enter to skip without saving.

After auto-saving, numa optionally exports an additional copy in your choice of format:

| Format | Saved to |
|---|---|
| Markdown (md) | `~/.numa/user-requested-nutrition-reports/` |
| Plain text (txt) | `~/.numa/user-requested-nutrition-reports/` |
| HTML | `~/.numa/user-requested-nutrition-reports/` |

You can accept the default filename (shown in the prompt) or enter your own. **The full path of any user-exported file is also printed in the terminal after saving.** Press Enter to skip the extra export.

Exported reports respect the active **dietary preferences** setting: complement suggestion sections in the exported file show only the same sources (all / vegetarian / plant-only) that the interactive display would show. This is implemented by passing `diet_pref=state._diet_pref` to `export.build_report()` from `reports._offer_export()`. The `build_report(title, sections, fmt, diet_pref="all")` signature accepts the preference and overrides the static `complement_suggestions` renderer for that call.

### Daily summary

Select **Daily Summary → Today's summary** to see the combined nutrition for all meals logged today. Use **Summary for a specific date** to look back at any past day.

---

## Architecture

### Overview — the refactor

The original monolithic `numa.py` was split into a `numa_app/` package (see `README-refactor.md`). The split is organized by responsibility:

- **`numa.py`** — five lines: parse args with `argparse`, call `run_app()`. Uses stdlib only; no `typer`.
- **`numa_app/main.py`** — top-level orchestration: `initialize_app()`, `print_startup_banner()`, `_run_menu()`, `run_app()`.
- **`numa_app/state.py`** — shared mutable state: `AppContext` dataclass holding the `Console`, current theme, and dietary preference. Module-level aliases (`console`, `T`, `_current_theme_name`, `_diet_pref`) are kept for convenience; `sync_globals()` refreshes them when state changes.
- **`numa_app/config/`** — persistence for theme and dietary preferences.
- **`numa_app/ui/`** — all terminal I/O primitives and rendering.
- **`numa_app/services/`** — stateless helpers for food search, portion parsing, and report export.
- **`numa_app/workflows/`** — one file per top-level menu area; each contains the menu loop and the handlers for every item in that section.

The support modules (`db.py`, `usda.py`, `diaas.py`, `export.py`, `profile.py`) live at the project root and are imported by the workflow modules as needed.

`usda.py` is a thin re-export shim (29 lines). All code that does `import usda as _usda` continues to work unchanged. The actual implementation lives in two files that can each be read and edited independently:

- **`usda_api.py`** (~290 lines) — HTTP client: API key management, `search_foods()`, `get_food_detail()`, `_parse_food()`, and the `NUTRIENT_MAP` / `ESSENTIAL_AMINO_ACIDS` / `AA_REFERENCE_MG_PER_G_PROTEIN` constants.
- **`usda_nutrients.py`** (~890 lines) — all nutrient math: `scale_nutrients()`, `sum_nutrients()`, `has_amino_acid_data()`, `protein_completeness()`, `get_aa_gaps()`, `suggest_complements()`, `get_diaas()`, `get_antinutrient_flags()`, `get_density_g_per_ml()`, and the embedded DIAAS, anti-nutrient, and complement data tables.

Similarly, the three largest workflow files were split to keep each under 600 lines:

- **`recipes.py`** — menu dispatch + shared helpers + create/list/display/delete (~440 lines). Uses lazy imports of `recipe_edit` and `recipe_analysis` inside `_menu_recipes()` to avoid circular dependencies.
- **`recipe_analysis.py`** — the "Analyze recipe" workflow: `_resolve_recipe_dcp_data()` and `_do_recipe_view()` (~575 lines).
- **`recipe_edit.py`** — the "Edit recipe" workflow: `_do_recipe_edit()` (~355 lines).
- **`foods.py`** — Foods menu + search/analyze/convert/cached-food viewer (~365 lines).
- **`drafted_foods.py`** — `_do_edit_cached_food()`, `_prompt_nutrients()`, `_bulk_import_aa()`, and drafted-profile management (`_do_drafted_foods_menu`, `_do_create_drafted_food`) — no separate edit entry point; editing goes through Food Cache.

### `numa_app/main.py` — startup and top-level menu

`initialize_app()` handles `--api-key` and `--theme` command-line flags (both exit after acting), calls `db.init_db()`, loads dietary preferences, and on first run triggers the animal-foods preference prompt.

`print_startup_banner()` renders the double green rule, then two lines: `NutriMagnus ("nutrition wizard")` in bold green, and `Nutritional Analysis for individuals and families`. Then profile summary and theme/dietary status.

`_run_menu()` is the top-level loop. It renders the main menu inline (not via `_show_menu()`), dispatches to workflow submenus by return value — `True` means go back, `False` means quit. It catches `ReturnToMain` exceptions, which any nested prompt can raise when the user types `m` to jump directly back here from anywhere in the menu tree.

### `numa_app/state.py` — shared state

`AppContext` is the single source of truth. `set_theme(name, theme_dict)` and `set_diet_pref(value)` are the only mutation points; both call `sync_globals()` to keep the module-level aliases in sync with the dataclass. All workflow modules import `state` and reference `state.T`, `state.console`, `state._diet_pref` directly. `_diet_pref` is a string: `"all"` | `"vegetarian"` | `"plant_only"`.

### `numa_app/ui/prompts.py` — input primitives

`_prompt(prompt_text, *, default, choices, prefill)` is the core input function. It has two paths:

- **Non-tty** (e.g., piped input, test runner): delegates to `rich.prompt.Prompt.ask()`.
- **Interactive tty, free_text**: uses `readline`-backed `input()`. Default values are displayed before the colon as `(Press enter to keep VALUE)` with the value in the theme's blue (`default_hint` style); nothing is pre-filled after the colon. Pressing Enter on a blank line returns the stored default.
- **Interactive tty, choices**: single-keypress mode via `termios`/`tty`. Only a character in the `choices` list is accepted; all other keystrokes are silently ignored. Pressing Enter on no input returns the default. This prevents accidentally submitting multi-character garbage (e.g., typing a food name at a `y/n/q` prompt).
- **Interactive tty, no choices, not free_text**: accumulation mode — characters are buffered and echoed until Enter; backspace/delete work. Up/down arrow keys navigate a persistent input history (up to 1000 entries, stored in `~/.numa_history`, loaded at startup). Pressing up saves the current partial buffer (`hist_saved`) and replaces it with the previous history entry; pressing down restores toward the current input. Consecutive duplicates are suppressed. Empty entries are not recorded.

Ctrl+C and `\x04` (EOF) raise `Cancelled` in all tty paths. Escape is detected by checking for trailing bytes within 50 ms; a bare Escape raises `Cancelled`.

`prefill=True` uses `readline.set_pre_input_hook` to pre-populate the input line with the default value, allowing the user to edit it in-place (e.g., for recipe name edits). This path requires an interactive tty and a non-empty default.

`Cancelled` is a plain exception class raised at any prompt when the user cancels. It propagates up to `_safe_call()` or the enclosing workflow, which prints `[dim]Cancelled.[/dim]` and returns the menu to the previous level.

`ReturnToMain` is a plain exception class raised when the user types `m` at any prompt that offers `m=main`. It propagates freely through `_safe_call()` (which does not catch it) and through all workflow loops up to `_run_menu()`, which catches it and resumes the main menu loop. Every inline prompt that offers `b=back` also offers `m=main`.

`_ask_float()`, `_ask_int()`, `_ask_date()` are thin wrappers that append `(b=back, m=main, q=quit)` to the prompt text and handle the `b` (return `None`), `m` (raise `ReturnToMain`), and `q` (`SystemExit(0)`) shortcuts.

### `manual.py` — inline help lookup

Parses `user-manual.md` on first use and caches sections keyed by anchor. Sections are headed `## Title [anchor]`; the anchor is the bracketed token, lower-cased.

`show(ref)` resolves aliases via `_ALIASES`, looks up the section, and renders it as a Rich `Panel` using the app's console. Returns `True` if found, `False` (with a list of available topics) if not. Called from `_prompt()` whenever the user types a `?`-prefixed command at any prompt.

`lookup(ref)` returns `(title, body)` or `None` — use this when the caller wants to handle display itself.

`available()` returns all defined anchor names sorted — used to build the "Available topics" fallback message.

`_ALIASES` maps common alternate spellings and synonyms to canonical anchors (e.g. `"suggest"` → `"comp"`, `"?"` → `"help"`).

#### Adding a new help topic

1. Add a section to `user-manual.md` with an anchored heading:
   ```
   ## My New Topic [mytopic]

   Plain text body. No Markdown tables or markup — Rich renders this as-is inside a Panel.
   ```
   The anchor must be unique and lower-case.

2. If alternate spellings should resolve to the same section, add them to `_ALIASES` in `manual.py`:
   ```python
   "my-topic": "mytopic",
   ```

3. Surface the topic from the relevant output block using `help_footer()` in `ui/common.py`:
   ```python
   from ..ui.common import help_footer
   help_footer("mytopic")            # single topic
   help_footer("mytopic", "diaas")   # multiple — joined with "or"
   ```
   This prints: `At any prompt, type ?mytopic or ?diaas for help with these columns.`

4. Add the new topic to the topic list in the `## Using the ? Help System [help]` section of `user-manual.md`.

**Format rules for manual sections:** plain text only — no Markdown tables, no bold/italic (Rich won't interpret them). `---` separator lines are stripped from section bodies automatically. Indented blocks are preserved as-is.

### `numa_app/ui/common.py` — menu rendering and safe dispatch

`_show_menu(title, items)` renders a title, horizontal rule, and numbered/lettered items. Numeric keys are styled with the accent color; non-numeric keys (b, q, etc.) use dim.

`_safe_call(fn, *args)` wraps every action call to catch `Cancelled` (prints "Cancelled.") and re-raises `SystemExit(0)` cleanly. Used throughout workflow modules to dispatch individual menu actions without the caller needing try/except.

**Table rendering helpers** (used throughout workflows and render.py):

| Function | Purpose |
|---|---|
| `dot_cell(text, width)` | Truncate text to `width` chars and pad remainder with dim dot leaders (`·`). Standardizes column appearance across all tables. |
| `table_title(title, subtitle)` | Blank line + indented hi-colour title for a table within an analysis section. `subtitle` is a pre-formatted Rich markup string for color legends or context. |
| `section_title(title, subtitle)` | Blank line + full-width accent title + rule — for top-level output sections. `subtitle` is plain text (auto-wrapped in dim). |
| `table_footer(*lines)` | Blank line then each line printed as-is — for key legends, totals, and notes below a table. |
| `help_footer(*anchors)` | One-liner beneath a table listing `?topic` commands the user can type. Joins multiple anchors with "or". No-ops if called with no arguments. |

### `numa_app/ui/render.py` — output rendering

All functions now use `section_title()`, `table_title()`, `table_footer()`, and `dot_cell()` from `ui.common` for consistent heading and table-column formatting throughout all output contexts (food, recipe, meal, daily summary).

`_print_nutrient_table(nutrients, title, per_label)` renders a Rich table of nutrients grouped into Macronutrients, Minerals, Vitamins, and Phytonutrients. Only groups with at least one present key are shown. Nutrient name column uses dot leaders via `dot_cell()`.

`_print_protein_completeness(nutrients)` checks all nine essential amino acids against the FAO reference. Returns `True` if amino acid data was present, `False` if not. Requires 5+ AAs with non-zero values — zero-keyed entries (common in branded USDA foods) are treated as absent.

`_print_bioavailability(food_name, nutrients)` calls `usda.get_diaas()` and `usda.get_antinutrient_flags()` and renders the bioavailability block (DIAAS bar, digestible protein, anti-nutrient notes).

`_print_complement_suggestions(nutrients, context, offer_if_covered, base_food_name)` renders the pantry-then-general complement suggestion flow. `offer_if_covered=False` suppresses the offer when the food already meets the reference (used for single-food display). `offer_if_covered=True` always shows (used after recipe analysis).

`_print_rda_comparison(nutrients, profile)` renders a table comparing daily nutrient totals against personalized RDA targets. For each nutrient it shows intake, target, percentage of RDA, a color-coded bar (green/yellow/red), and a status note. Sodium uses the limit direction (green if under); all others use the minimum direction. Nutrient name column uses `dot_cell()` for fixed-width alignment.

### `numa_app/services/search.py` — food lookup flow

`_search_and_pick_food()` handles the full food lookup: prompt → search local cache and USDA (and Open Food Facts for unrestricted searches) → merge results cache-first → remove duplicates and rank → display results table → user picks → fetch detail if not cached → cache and return food dict. Reused by every workflow that needs food selected. Both cache-return paths include an omega fatty acid backfill check: if the selected food is a non-user-drafted USDA food missing all four omega keys, the program silently fetches and merges them before returning.

The local cache is **always** searched first. The USDA (and OFF) search always runs alongside it — both sources are queried on every search regardless of cache hits. Remote-only items (not already in the cache) are appended without duplicates (matched by `fdc_id`).

**Result ranking** is performed after deduplication via two paths:

- **Brand query detected** — if any brand word (≥ 4 chars) from any result's `brandOwner` / `brandName` field appears in the query string, results are sorted by `_word_score` (descending): the count of query words that appear in the food's description. This surfaces the specific branded product the user named.
- **Generic query** — otherwise, results are sorted by `(_source_tier(f), -_word_score(f))`. `_source_tier` returns `0` for cached items, `1` for Foundation/SR Legacy, `2` for Open Food Facts, and `3` for Branded/unknown. Within each tier, higher word-score items rank first.

An **AA data** column is always shown in the results table using the following symbols:

| Symbol | Meaning |
|--------|---------|
| ✓ | Confirmed — food is cached and has amino acid values |
| ✗ | None — food is cached with no AA data, or is a branded/OFF product (these sources never include AA data) |
| ~✓ | Likely — food is not yet cached but is Foundation or SR Legacy type, which almost always carry full AA profiles |

A multi-line key below the table explains these symbols. If the USDA API fails but cache results exist, the function continues with cached items only and shows a warning.

When `data_types` is restricted to `["Foundation", "SR Legacy"]` (AA-fix flows), Open Food Facts is excluded automatically, since OFF products never contain amino acid data.

When a recipe is selected from the results, the returned dict now includes `total_weight` (from `recipes.total_weight`), enabling recipe-portion analysis to display per-100g breakdowns when total weight is recorded.

Network errors (`TimeoutError`, `OSError`) when fetching food detail are now caught and displayed as a user-friendly message rather than crashing the flow.

`_suggest_foundation_search(food)` is called when the selected food has no amino acid data. It offers to re-search Foundation Foods using a pre-filled keyword (first token of the food name), shows results, and returns the user's pick or `None`. The help text notes that Open Food Facts results are excluded from this flow.

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

Returns `None` on unrecognized input; `(None, vol_display)` when volume is recognized but density is unavailable (caller then prompts for grams). `_PIECE_UNITS` is a frozenset of the recognized piece-unit words.

`_pick_portion(food)` renders the USDA portions list for the food, then loops on `_parse_portion_input` until the user enters a valid amount or cancels. The hint text explains that a bare number means pieces/count and a unit is required for weight or volume.

### `numa_app/workflows/recipes.py` — recipe CRUD and shared helpers

Contains the menu dispatch (`_menu_recipes`), all shared helper functions used by the split-out modules, and the create/browse/develop/display/delete/copy handlers.

**Menu dispatch** (`_menu_recipes`): three items — Create / Browse / Develop. Uses lazy imports of `recipe_edit` and `recipe_analysis` inside action handlers to avoid circular dependencies.

**Key workflow handlers:**

| Function | Purpose |
|---|---|
| `_do_recipe_browse()` | Browse workflow: shows 20 most-recently-accessed recipes; supports inline `v/x/a/d/c<id>` actions, `s`=search, `r`=recent. Each action stamps `last_accessed_at` via `recipe_touch()`. |
| `_do_recipe_develop(recipe=None)` | Develop workflow: iterative add/remove ingredients with optional nutritional analysis after each change; prompts for procedure on exit; recomputes and saves DCP if ingredients changed. Accepts optional pre-selected recipe (used by Browse `x<id>`). |
| `_do_recipe_display(recipe=None)` | Text view: name, ingredients, procedure; ends with `e=edit  b/Enter=done` prompt — pressing `e` chains directly into `_do_recipe_edit`. Accepts optional pre-selected recipe. |
| `_do_recipe_delete(recipe=None)` | Delete with confirmation. Accepts optional pre-selected recipe. |
| `_do_copy_recipe(recipe=None)` | Copy recipe under a new name. Accepts optional pre-selected recipe. |

Key shared helpers imported by `recipe_analysis.py` and `recipe_edit.py`:

| Function | Purpose |
|---|---|
| `_pick_recipe()` | Search/list recipes, return selected recipe dict |
| `_compute_recipe_dcp(rid)` | Compute digestible complete protein (g) for a whole recipe from cached ingredient data |
| `_augment_aa_from_curated(nutrients, stats)` | Add AA data from the curated complement table for ingredients that lack USDA AA profiles |
| `_parse_serving_amount(raw)` | Parse a serving count string (int, fraction, decimal) |
| `_format_recipe_portion_label(servings)` | Format a portion label ("1 serving", "2 servings", etc.) |
| `_get_recipe_total_nutrients(recipe_id)` | Return `(recipe, ingredients, combined_nutrients)` — used by the Foods workflow to analyze a recipe portion |
| `_pick_recipe_portion(recipe)` | Prompt for number of servings; return `(servings, label)` |

### `numa_app/workflows/recipe_analysis.py` — analyze recipe workflow (~575 lines)

Contains `_resolve_recipe_dcp_data()` and `_do_recipe_view()` (menu option 5 "Analyze recipe").

`_resolve_recipe_dcp_data(recipe_id, ingredients, ingredient_stats, combined)` detects missing data that blocks or degrades DCP calculation (unknown ingredient weights, missing DIAAS scores, missing AA data). It prompts the user to provide data, calculate with assumptions, or skip. Returns `(updated_stats, updated_combined, approximate, notes)`, `None` to skip DCP entirely, or `"rerun"` if ingredients were replaced and analysis should restart.

`_do_recipe_view()` is the full nutrition analysis workflow: builds combined nutrient totals, calls `_resolve_recipe_dcp_data`, applies DIAAS-weighted DCP calculation, displays per-serving and whole-recipe nutrient tables, recipe bioavailability table, protein completeness, and complement suggestions. Supports live replacement of ingredients with missing AA data during the session.

Also contains `_recipe_weight_to_g()` and `_recipe_vol_to_ml()` — unit converters for recipe total volume/weight metadata.

### `numa_app/workflows/recipe_edit.py` — edit recipe workflow (~355 lines)

Contains `_do_recipe_edit()` (menu option 4 "Edit recipe"). Supports back-navigation through metadata fields (name → description → servings → total volume → total weight → procedure), ingredient-level editing (amount, unit, food name, notes), ingredient replacement via USDA search, reordering, and deletion. Recomputes DCP after any ingredient change.

### `numa_app/workflows/foods.py` — Foods menu (~365 lines)

Contains the Foods menu dispatch and the search/analyze/convert/cached-food-viewer handlers. Imports `_do_edit_cached_food` and `_do_drafted_foods_menu` from `drafted_foods.py`.

### `numa_app/workflows/drafted_foods.py` — cache editing and drafted profiles (~620 lines)

`_do_edit_cached_food(fdc_id, cached)` edits any cached food (USDA, OFF, or user-drafted): name, serving metadata, all nutrients (pre-filled from existing values), and a note. After saving, marks the entry `user_drafted=True` so automatic AA re-fetches will not overwrite the changes. Preserves original USDA portion data. Auto-detects supplement mode (single portion with `gram_weight=100`); for user-drafted foods not yet in supplement mode, asks at the start of the edit session whether to convert.

`_prompt_nutrients(existing, unit_label)` interactively prompts for all nutrient values per 100g (or per tablet/capsule/etc. when `unit_label` is set). Walks through five optional sections: basic macros (always), minerals, vitamins, amino acids (three modes: one-by-one, bulk import, or skip), and phytonutrients. For vitamins A, D, and E, IU input is accepted and auto-converted to the program's native mcg/mg units. In supplement mode, the intro explains the label-entry convention so naive users are not confused by the "per 100g" framing.

`_bulk_import_aa(protein_g)` accepts amino acid values as `name: value` pairs (full name, 3-letter, or 1-letter codes). If `protein_g` is provided, converts from g/100g-protein to g/100g-food automatically. Classifies each entry as stored, non-essential (skipped with note), or unrecognized (warning).

`_do_drafted_foods_menu()` / `_do_create_drafted_food()` — drafted-profile management. The menu offers five options: List, Create, Edit, Delete, and Copy. Create supports starting from a USDA food (pre-fills all values) or from scratch, and includes a supplement/unit-based mode question. Edit calls `_do_edit_cached_food()` directly, which handles supplement detection and the conversion question. Drafted profiles are saved with small negative `fdc_id` values (−1, −2, …) and `user_drafted=True`.

### `numa_app/workflows/settings.py` — settings menu, profile, and RDA

`_menu_settings()` renders the six-item settings menu: Color theme, User profile, Dietary preferences, Editor command, Display program settings at launch, and Advanced settings. Each item shows its current status inline. Item 6 opens `_menu_advanced_settings()`, which holds USDA API key, Protein digestibility overrides, and Storage location (display only).

`_get_editor_command()` / `_do_editor_command()` — let the user set a preferred editor command (e.g. `nano`, `vim`, `code --wait`). Blank means use `$VISUAL`/`$EDITOR`. Enter `-` to clear back to system default.

`_do_launch_display_setting()` — toggles whether the startup banner (profile, theme, dietary status) is shown on launch. Default is off (`n`). Setting is stored in `prefs.json`; `run_app()` checks it before calling `print_startup_banner()`.

`_do_user_profile()` collects age, sex, weight (accepts kg or lb), height (accepts cm or feet+inches), and activity level. Existing values are shown and kept on empty input. On save, prints the computed calorie and protein targets.

`_do_dietary_prefs()` presents a three-option menu (all animal foods / vegetarian / plant-based only), saves the chosen value to `prefs.json`, and updates `state._diet_pref` immediately. Label strings for all three values are defined in `_DIET_LABELS` (in `prefs.py`) and imported by both `settings.py` and `main.py`.

`_do_diaas_overrides()` manages the `diaas_overrides` table: list, add/update, delete. Shows the current numa-calculated value before prompting for the override. Uses `table_title()` and `dot_cell()` from `ui.common` for consistent table styling.

### `db.py` — SQLite database

All persistence goes through a `get_db()` context manager that commits on clean exit and rolls back on exception. The database path is `~/.local/share/numa/numa.db`.

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

`recipes.dcp_g` stores the digestible complete protein (grams, whole recipe) computed at last view. It is `NULL` when the recipe has never been viewed, when the calculation was approximate (user-provided data), or when amino acid data was unavailable. The recipe list shows DCP per serving when this value is present.

`recipes.last_accessed_at` stores the ISO 8601 UTC timestamp of the last time the recipe was opened via any workflow action (view/edit/develop/analyze/copy). It is `NULL` for recipes that have never been accessed. Added via `ALTER TABLE` migration. Used by `recipe_list_recent()` to order the Browse view; falls back to `created_at` for recipes with no access timestamp.

**Key db functions:**

| Function | Purpose |
|---|---|
| `recipe_list(conn)` | All recipes ordered by name; includes `complete`, `last_accessed_at`, `total_weight`, `total_weight_unit` columns |
| `recipe_list_recent(conn, limit=20)` | Recipes ordered by `COALESCE(last_accessed_at, created_at) DESC` — powers the Browse recent view |
| `recipe_touch(conn, recipe_id)` | Sets `last_accessed_at = datetime('now')` for a recipe — called whenever a recipe is opened |
| `meal_add_recipe(conn, meal_id, recipe_id, recipe_name, servings, unit="servings")` | `unit` parameter now configurable (was hardcoded to "servings") |

All nutrient data is stored as a JSON blob in `foods.nutrients_json`, keyed by the same field names used throughout (`calories`, `protein_g`, `carbs_g`, etc.). This avoids schema migrations when nutrient tracking is expanded.

### `usda_api.py` — USDA HTTP client (~290 lines)

**API:** USDA FoodData Central REST API (`https://api.nal.usda.gov/fdc/v1`). Uses stdlib `urllib` — no `requests` dependency at runtime.

`NUTRIENT_MAP` is a dict mapping USDA nutrient IDs (integers) to `(our_key, display_label, unit)` tuples. It covers 45 nutrients: macros, minerals, vitamins, 7 phytonutrients/bioactive compounds, and 11 amino acids (including tyrosine, added to support Phe+Tyr combined scoring in meal-level DIAAS). Also defines `ESSENTIAL_AMINO_ACIDS` (list of 9 internal keys) and `AA_REFERENCE_MG_PER_G_PROTEIN` (FAO 2013 reference pattern).

**Key functions:**

| Function | Purpose |
|---|---|
| `get_api_key()` / `set_api_key(key)` | Read/write API key from `~/.config/numa/config.json` |
| `search_foods(query)` | Search USDA; returns list of result dicts |
| `get_food_detail(fdc_id)` | Fetch full nutrient profile for one food |

`_parse_food()` normalizes USDA API responses — the API returns nutrients in three different formats depending on the endpoint (`nutrientId`, `nutrient.id`, or `number`), and `_parse_food` handles all three.

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
| `suggest_complements(base_nutrients, pantry_candidates, diet_pref="all")` | Compute minimum-gram complement suggestions from pantry and curated table; returns `{"pantry": [...], "general": [...]}`. `diet_pref` controls which curated-table entries are eligible: `"all"` includes everything, `"vegetarian"` includes only plant and dairy/egg entries (those flagged `dairy_egg=True` in `_COMPLEMENT_TABLE`), `"plant_only"` excludes all animal entries. The curated table holds protein + nine essential AAs per 100g for ~30 common protein sources; used only for complement scoring and AA gap augmentation — not for general food search. |
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

---

## Web Interface

A local FastAPI web app that exposes the same data and analysis as the CLI. All routes are in `web/backend.py`; templates live in `web/templates/`. The app is launched separately from the CLI (see Running the Program). It shares the same SQLite database and config files as the CLI.

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

The navbar marks the active section by comparing `request.url.path` to each nav link's prefix. Foods items are in a dropdown; Recipes, Meals, Daily Summary, Settings, and Manual are top-level links.

#### `home.html`

Renders the content of `home.md` (project root) as HTML. The markdown file is rendered once at startup and cached in `web/home_body.cache`; the cache is invalidated if `home.md` is newer.

#### `search.html`

Food search results. Shows a results table with food name, data type, brand, and source badge (cache / usda / local). Each row links to `/food/{fdc_id}`. Used for both the Foods → Search page and as a reusable search partial.

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

Browsable/searchable table of all cached foods. Columns: FDC ID, name, data type, brand, AA data flag, GI annotation, DIAAS annotation, notes. Each row links to `/food/{fdc_id}` and `/food/annotate/{fdc_id}`. Supports deletion.

#### `food_custom_profiles.html`

Lists all user-drafted food profiles (data type = "User Drafted"). Provides a create-by-name form and per-row delete. Creating a profile immediately redirects to `/food/{fdc_id}` for nutrient editing.

#### `food_annotate.html`

Two-mode template. In list mode: browsable/searchable table of cached foods showing existing GI and DIAAS annotations. In edit mode (`editing=True`): form for entering GI estimate (0–100), DIAAS digestibility (0–1), and prep context note, with "no prompt" checkboxes to suppress future annotation prompts.

#### `pantry.html`

Table of pantry items with food name, FDC ID link (if available), and notes. Add-by-name form at top. Per-row remove button.

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
- **Protein Quality (DIAAS)**: meal-level DIAAS score, total protein, digestible complete protein, limiting amino acid, per-AA ratio table
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
| `~/.config/numa/config.json` | USDA API key |
| `~/.config/numa/theme` | Saved color theme preference |
| `~/.config/numa/prefs.json` | Dietary preferences (`diet_pref`: `"all"` / `"vegetarian"` / `"plant_only"`) |
| `~/.config/numa/profile.json` | User profile (age, sex, weight, height, activity level) |
| `~/.numa/reports/` | Auto-saved nutrition reports (Markdown) — one file per analysis |
| `~/.numa/user-requested-nutrition-reports/` | User-exported reports (txt, md, or html) |

---

## Test Suite

The test suite has been rebuilt for the refactored `numa_app/` package structure. **316 tests**, all passing.

Run with: `pytest` (uses `pytest.ini` which sets `testpaths = tests` and `pythonpath = .`).

> **Note:** `pytest` is not in `requirements.txt` (which lists only runtime dependencies). Install it separately: `pip install pytest`.

| File | What it tests |
|---|---|
| `tests/conftest.py` | Shared fixtures, sample data constants, and `NumaTestRunner` |
| `tests/test_db.py` | Schema creation, all CRUD helpers, cascade deletes, rollback on exception |
| `tests/test_usda.py` | `scale_nutrients`, `sum_nutrients`, `_parse_food`, `protein_completeness`, `nutrient_label`, `get_diaas`, `get_antinutrient_flags`, `suggest_complements`, `get_density_g_per_ml` |
| `tests/test_diaas.py` | `get_digestibility` (all tiers), `meal_level_diaas` (edge cases, complementarity, pairing, gap flags), DIAAS override CRUD |
| `tests/test_profile.py` | `load_profile`, `save_profile`, `bmr`, `compute_rda` (sex/age/activity variants), unit conversion helpers |
| `tests/test_cli.py` | All menus end-to-end; USDA API mocked; dietary prefs toggle; Foods item 3 (recipe portion analysis); profile settings and RDA comparison |

### Test infrastructure

**`NumaTestRunner`** (in `conftest.py`) replaces the old `typer.testing.CliRunner`. It calls `run_app()` directly, replacing `sys.stdin` with `io.StringIO(input)` and redirecting the rich `Console` to a buffer. When `sys.stdin` is not a tty, `_prompt()` falls back to `rich.prompt.Prompt.ask()`, which calls `input()` — reading from the injected `StringIO`. This captures all interactive I/O without requiring a real terminal.

**Autouse fixtures** keep each test hermetic:

| Fixture | Effect |
|---|---|
| `use_test_db` | Redirects `_db._DB_PATH` to a per-test temp file; schema initialized fresh |
| `use_test_profile` | Redirects `profile._PROFILE_FILE` to a per-test temp path |
| `use_test_prefs` | Pre-populates a temp prefs file and patches both `prefs._PREFS_FILE` and `main._PREFS_FILE` so the first-run animal foods prompt is never shown |
| `no_export` | Stubs `_offer_export` to a no-op; tests don't write real files and don't need extra input lines to decline the export prompt |
| `no_off` | Stubs `openfoodfacts.search_foods` to return `[]`; prevents network hits and stops OFF results from affecting search ordering or output in any test |

### Bugs found during test restoration

Five missing imports were discovered in the production code (all `NameError` crashes on real user actions):

- `numa_app/workflows/foods.py` — `_offer_export` not imported (crashes Foods → Analyze USDA portion)
- `numa_app/workflows/foods.py` — `_do_list_cached_foods` not imported (crashes Foods → View cached)
- `numa_app/workflows/foods.py` — `_do_recipe_list`, `_get_recipe_total_nutrients`, `_pick_recipe_portion` not imported (crashes Foods → Analyze recipe portion)
- `numa_app/workflows/settings.py` — `_change_theme` not imported (crashes Settings → Color theme)
- `numa_app/workflows/settings.py` — `_save_prefs` not imported (crashes Settings → Dietary preferences and main menu `d`)

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

### Phase 2 — In progress

**Item 1: Expanded nutrient tracking — Coded | Validation in progress**

- Seven additional phytonutrients and bioactive compounds tracked from the USDA database: carotenoids (beta-carotene, alpha-carotene, lycopene, lutein+zeaxanthin), choline, beta-sitosterol, and isoflavones.
- Protein bioavailability assessment using DIAAS: a keyword lookup table covering 50+ foods shows the digestibility-adjusted protein figure alongside raw protein grams.
- Anti-nutrient advisories: flags foods with phytate, oxalate, lectins, trypsin inhibitors, or bound niacin, with practical notes on how cooking reduces their effect. Flags are suppressed automatically when the food name indicates it has already been cooked or processed.
- Volume-to-weight conversion: portion sizes can now be entered as volumes (e.g., `1/8 cup`, `2 tbsp`). Density is derived from the static keyword table first; USDA portion data is used as a fallback. Fraction and mixed-number input (e.g., `1/4`, `1 1/2`) also supported.
- **Digestible complete protein (DCP) per recipe**: recipe view computes and saves DCP (grams per serving) to the database. The value is the sum of each ingredient's protein × its DIAAS score — the DIAAS score already encodes both digestibility and amino acid quality, so no further limiting-score factor is applied. This gives a single number for how much protein the recipe realistically delivers. Displayed in the recipe list as "DCP/srv". Recomputed automatically when any ingredient is added, edited, or removed. If an ingredient lacks weight or DIAAS data, the user is prompted to supply the missing information or to calculate anyway (approximate results are flagged and not saved to the database).

**Item 2: Pantry — Coded ✓**

- A persistent "My Pantry" list tracks protein sources currently on hand.
- Foods can be added via USDA search (linking the full amino acid profile) or by name only for a quick entry.
- The pantry list is stored in the local SQLite database (`pantry` table: food name, optional fdc_id, notes, date added).
- Accessible from **Foods → My pantry**.

**Item 3: Protein complementarity advisor — Coded ✓**

- After any protein analysis — individual food, recipe, meal, or daily summary — numa offers to show protein complement suggestions.
- The advisor identifies which essential amino acids are still below the FAO/WHO reference score (the "gaps"), then calculates the minimum grams of a complement food needed to bring the most limiting amino acid to exactly 1.0.
- Suggestions are split into two lists: **Pantry** foods first (from the user's My Pantry list), then **General** suggestions from a curated built-in table of common plant protein sources. This means pantry items are always prioritized; the curated fallback covers users who haven't set up a pantry yet.
- For each suggestion the output shows: the food name, DIAAS score, how many grams to add, and a before→after score for the top-gap amino acids.
- `suggest_complements()` in `usda.py` uses the primary-gap algebraic solve: given the base protein and the candidate's AA/protein ratio, it computes the exact gram weight that closes the most limiting gap (working throughout in digestibility-adjusted space), then re-scores all nine essential AAs at that combined weight. Candidates whose AA/protein ratio is below the digestibility-adjusted reference are silently excluded (adding them would worsen the gap).
- Met+Cys and Phe+Tyr are treated as combined pairs throughout gap detection and suggestion scoring, consistent with FAO 2013.
- Suggestions are ranked: primary-gap closers first, then by number of gaps closed, then by smallest gram amount.
- Complements that close one gap while opening a new one (e.g. Brazil nuts close Met+Cys but dilute lysine) are included with an "opens new gap" warning so users can layer complements if needed.
- Only AAs with digestibility-adjusted score below 0.95 are treated as gaps. Near-adequate AAs (score 0.95–1.0) are excluded to avoid impractically small suggestions (e.g. 1g nutritional yeast to close a 0.6% isoleucine shortfall).
- Pantry foods with no USDA cache entry fall back to the built-in curated table by keyword match, so name-only pantry entries still participate.
- The advisor is called automatically at the end of: food search, portion analysis, recipe analysis, meal analysis, and daily summary — wherever amino acid data is present.

**Item 4: Meal-level DIAAS analysis — Coded ✓**

- Meal analysis and daily summary now compute a composite meal-level DIAAS score using the FAO 2013 pooled-IAA methodology (see `diaas.py`).
- A true ileal digestibility coefficient is applied per ingredient before pooling, capturing amino acid complementarity across the whole meal.
- Digestibility coefficients sourced from a three-tier lookup: ~50-entry curated literature table → category defaults → 0.82 overall default. User overrides stored in the `diaas_overrides` DB table take precedence over all.
- Output: per-ingredient digestibility table, per-IAA composite ratio table with bar indicators, composite DIAAS, and digestible complete protein in grams.
- Tyrosine (USDA nutrient 1218) added to `NUTRIENT_MAP` so future food fetches include it for proper Phe+Tyr combined scoring.
- Settings menu extended with **Protein digestibility overrides** for power users who have primary-literature values for specific foods.
- 55 new tests in `tests/test_diaas.py` covering all lookup tiers, DB CRUD, calculation correctness, complementarity, and edge cases.

**Item 5: User profile and personalized RDA comparison — Coded ✓**

- A user profile (age, sex, weight in kg, height in cm, activity level) is set under **Settings → User profile** (item 2) and persisted to `~/.config/numa/profile.json`.
- Calorie target is computed via the Mifflin-St Jeor equation × an activity multiplier. Protein target scales with body weight and activity level (0.8–1.2 g/kg).
- All other targets follow NIH/Institute of Medicine Dietary Reference Intakes: sex-specific values for iron, calcium, potassium, choline, and B vitamins; age-adjusted values for calcium (women 51+, men 70+), vitamin D (70+), fiber (50+), and vitamin B6 (51+).
- After any **Daily Summary**, if a profile is set, numa offers "Compare to your personalized RDA targets?". The comparison table shows each tracked nutrient's intake, target, percentage of RDA, a color-coded bar (green/yellow/red), and a plain-language status note. Sodium uses the limit direction (green if under, red if over); all other nutrients use the minimum direction.
- If no profile is set, a tip to configure one is shown instead. 28 new tests in `tests/test_profile.py`; 8 new CLI tests in `tests/test_cli.py`.

**Item 6: Refactor to numa_app/ package — Coded ✓**

- The monolithic `numa.py` was split into a `numa_app/` package to reduce per-file size and make individual feature areas easier to work on in isolation (particularly in offline LLM editing sessions).
- `numa.py` is now a five-line thin entry point using stdlib `argparse`; `typer` is no longer a dependency.
- All menu logic, rendering, services, and workflow code lives under `numa_app/` (see Project Structure above).
- Smoke checks passed: imports resolve, `python -m compileall` clean, `--help` works.
- The test suite has been rebuilt for the refactored structure (316 tests, all passing). The rebuild also uncovered five missing imports in `foods.py` and `settings.py` that would have caused `NameError` crashes on real user actions.

**Item 7: Dietary preferences — Coded ✓**

- First-run prompt asks whether complement suggestions should include animal-based foods (eggs, cheese, fish, chicken, whey).
- Preference saved to `~/.config/numa/prefs.json` and applied to all complement suggestion flows.
- Accessible at the main menu via `d`, and also under Settings → Dietary preferences.

**Item 8: Analyze a saved recipe portion (Foods menu) — Coded ✓**

- New entry in the Foods menu (item 3): select a saved recipe by ID, specify a number of servings (decimal or fraction), and view scaled nutrient totals with full protein completeness analysis.
- Uses the same nutrient scaling and rendering pipeline as other analysis flows.

**Item 9: Notes on meal/recipe ingredients — Coded ✓**  *(2026-04-11)*

- Every ingredient in a recipe and every food item in a meal now has an optional **Note** field (the `notes TEXT` column was already in the DB schema; the UI prompts were missing).
- Recipes: note is prompted after portion selection when adding an ingredient (both create and edit flows). When editing an existing ingredient, the current note is pre-filled; enter `-` to clear. The ingredient table in the edit view shows a **Note** column when any notes are present.
- Meals: note is prompted after portion selection when adding a food item. The food item edit loop (`f`/`a`/`n`) now has an `n` option for editing the note in-place.
- Pantry already had note support.

**Item 10: User-drafted food nutritional profiles — Coded ✓**  *(2026-04-11)*

- New Foods submenu item 7: **User-drafted food profiles** — create, edit, list, and delete hand-crafted nutrient profiles for foods lacking adequate official data.
- Create flow: start from a USDA food (pre-fills existing data) or from scratch. Prompts for name, serving size, all macros, then offers a three-way amino acid choice: one-by-one in g/100g food, bulk import in g/100g protein (auto-converted), or skip. Requires a Note for source documentation.
- Profiles are stored in the `foods` table with `user_drafted = 1` and a negative fdc_id (range −1 to −2,000,000,000, distinct from Open Food Facts ids). They behave like any other cached food in all analysis flows.
- Edit flow walks through the same prompts with current values pre-filled.
- Primary use case: constructing best-guess AA profiles from literature searches for specialty foods not in any public database.

**Item 11: Open Food Facts integration — Coded ✓**  *(2026-04-11)*

- New module `openfoodfacts.py` implements the OFF REST API (no key required, CC BY-SA 4.0 data).
- Results from USDA and OFF are merged in all unrestricted food searches. OFF items are labeled "Open Food Facts" in the Type column; they show `✗` in the AA data column immediately (no cache lookup needed).
- OFF items are excluded from AA-fix searches (Foundation Foods replacement flow) since OFF never contains amino acid data.
- OFF nutrient data is in the search result already — no second HTTP call when the user selects an OFF item. The item is cached to the local DB under `data_type = "Open Food Facts"`.
- OFF product fdc_ids are deterministic negative integers (range −2,000,000,000 to −3,000,000,000) derived from the product barcode.
- Foods menu labels and search status text updated throughout to name both databases.

**Item 12: Bug fixes and UX corrections — Coded ✓**  *(2026-04-11)*

- **Settings → Editor command** (`_do_editor_command`, `_get_editor_command`): both functions were referenced in the menu but never written. Now implemented.
- **"Display settings at launch" setting**: was stored and displayed but never checked. `run_app()` now wraps `print_startup_banner()` in `if getattr(state, "_display_program_settings", False)`. Default is off.
- **Recipe view**: ingredient list with amounts (and per-ingredient notes) now appears before the DCP options menu, so the recipe is fully visible when the user must make decisions about missing data. Label "Instructions" renamed to "Procedure".
- **DCP options menu**: converted from ad-hoc letter choices (`f`, `c`, `s`, `p`) to the standard numbered menu format with `b` and `q` options. Invalid input now shows a warning and re-prompts.
- **API key corruption on paste**: `_prompt()` now skips non-printable characters (e.g., the `\x16` Ctrl+V byte injected by some terminals when pasting). `set_api_key()` also strips non-printable characters as a safety net.
- **`sqlite3.Row` vs dict**: `.get("notes")` calls on `sqlite3.Row` objects (which don't support `.get()`) replaced with direct key access throughout `meals.py` and `recipes.py`.

**Item 13: Bulk literature amino acid import — Coded ✓**  *(2026-04-11)*

- The amino acid prompt in user-drafted food profiles now offers three choices instead of y/n: one-by-one (g/100g food), bulk import (g/100g protein), or skip.
- Bulk import (`_bulk_import_aa` in `foods.py`) reads `name: value` pairs (one per line; also accepts `name = value` or `name value`). Accepted name forms: full name, 3-letter code, 1-letter code.
- If protein content was entered in the same session, values are automatically converted: `aa_food = aa_protein × protein_g / 100`. The summary display shows the conversion for each amino acid.
- Non-essential amino acids (alanine, arginine, glycine, etc.) are silently discarded with a note. Unrecognized names are flagged in yellow. Essential amino acids (the nine stored by the program) are shown in green with a ✓.
- Designed for entering FAO/WHO/literature amino acid composition tables that report values in g per 100g protein — the most common format in peer-reviewed nutrition literature.

**Item 14: UX fixes and recipe volume/weight — Coded ✓**  *(2026-04-13)*

- **Startup banner**: First line is now `NutriMagnus ("nutrition wizard")` (bold green); second line is `Nutritional Analysis for individuals and families`. Previously a single combined line.
- **Default-value prompt display**: All prompts with a default now show `(Press enter to keep VALUE)` before the colon, with the value rendered in the theme's blue (`default_hint` style). Nothing is pre-filled after the colon; pressing Enter on a blank input returns the stored default.
- **Choices prompt — single keypress only**: When `choices` is provided (e.g. `y/n/q`), the prompt now accepts only valid single keystrokes. Any character not in the choices list is silently ignored, preventing multi-character input like a food name from being misread as a menu selection.
- **Recipe create — procedure editor gate**: Opening the text editor now requires the user to press Enter first (or `b` to skip), consistent with the recipe-edit flow. Previously the editor launched immediately after printing the message.
- **Recipe search in meal add**: The "add items to meal" search now tokenizes the query and matches a recipe if **any** word appears in its name. Previously the entire query string had to be a substring of the name, making multi-word searches like `coffee Mexican Tom` fail to find `Mexican coffee`.
- **Recipe total volume and weight**: New optional fields `total_volume`, `total_volume_unit`, `total_weight`, `total_weight_unit` added to the `recipes` table (auto-migrated). Both fields are prompted during recipe create (after servings, before the procedure editor) and recipe edit (after name/description/servings). Input format: `NUMBER UNIT` (e.g. `4 cups`, `800 g`). Either or both may be skipped (Enter on blank). `_parse_measure()` helper handles parsing.

**Item 15: Recipe UX improvements and piece-count portions — Coded ✓** *(2026-04-13)*

- **Recipes menu restructured (1→6 items)**: item 3 is now a plain text view (new `_do_recipe_display`); item 4 is Edit (unchanged); item 5 is Analyze (was item 3 "View / analyze"); item 6 is Delete (was item 5).
- **Recipe view (item 3)**: lists recipes → user picks by ID → displays full recipe text (name, description, servings, volume/weight, ingredients with notes, procedure) and returns to the menu automatically. No nutritional analysis.
- **Ingredients menu `b` key**: `b` and `d` both proceed to the Procedure editor. `m` and `q` remain the escape hatches that skip Procedure (menu labels updated to note this). Previously `b` exited the edit entirely, bypassing Procedure.
- **Recipe always-save on exit**: header fields in create (`_do_recipe_create`) each have their own `try/except Cancelled` so Ctrl+C at any prompt after the name still creates the record. In edit (`_do_recipe_edit`), `b`, `q`, and Ctrl+C in the meta loop now break to the save block instead of returning early — any fields already changed are written to the DB before exit. `q` specifically was saving nothing; it now saves then raises `SystemExit`.
- **Servings default changed to 0** (was 1) in the recipe creation flow.
- **Blank line added** before "Current recipe ingredients" heading in the ingredient-edit loop.
- **Piece/count portion input**: a bare number (e.g. `2`) now means pieces/count, not grams — `grams = 0.0`, label `"2 pc"`. Explicit piece-unit words also accepted: `pc`, `pcs`, `piece`, `pieces`, `each`, `ea`, `count`, `ct`, `item`, `items`. Nutritional contribution of piece-count ingredients is zero in totals. Prompt hint and error message updated to explain the distinction. `_PIECE_UNITS` frozenset added to `portions.py`.

**Item 16: Recipe analysis servings=0, DCP UX fixes, and display polish — Coded ✓** *(2026-04-13)*

- **Servings=0 analysis**: when a recipe has no serving count, `_do_recipe_view` now shows: (1) whole-recipe nutrient totals, (2) per-100g table if total weight was recorded, (3) per-100ml and per-1-cup tables if total volume was recorded. The complement-suggestions basis menu is skipped; the analysis nutrients are used directly with a label reflecting what they represent (whole recipe / per 100 g / per 100 ml). DCP is not saved to the DB when servings=0. Export labels updated to say "whole recipe (no serving count)" instead of "whole recipe, 0 servings".
- **Servings prompt clarified**: both the create and edit prompts now read `Number of servings  (0 = analyze by weight/volume)`.
- **DCP missing-data Options menu loops**: the options menu (provide data / calculate anyway / skip) is now shown inside a `while True` so pressing `b` during "Provide missing data" re-displays the menu rather than exiting the analysis.
- **DCP warning note**: a dim note is printed after the missing-ingredient list reminding the user that non-protein ingredients (spices, oil, salt) can safely be ignored in the warning.
- **Report file path color**: path strings in the auto-save and previous-reports display are now rendered in `thistle1` (light lavender) instead of `dim`, which was unreadable on dark terminal backgrounds.

**Item 18: Omega fatty acid tracking and automatic backfill — Coded ✓**  *(2026-05-31)*

- Four individual omega fatty acid keys added to `NUTRIENT_MAP`: `omega3_ala_mg` (ALA, plant-based; USDA ID 1404), `omega3_epa_mg` (EPA, marine; 1278), `omega3_dha_mg` (DHA, marine; 1272), `omega6_la_mg` (linoleic acid; 1269). USDA reports these in grams; `_parse_food` multiplies by 1000 on fetch to store and display in mg.
- All four appear in the Macronutrients group of the nutrient display table, after polyunsaturated fat, whenever data is present.
- Added to `_DRAFT_MACROS` so custom food entry prompts them after poly fat.
- **Automatic backfill**: both cache-return paths in `search.py` (`_fetch_food_from_result` and the main pick loop) check whether the selected USDA food is missing all four omega keys. If so, a silent USDA fetch is made, only the omega values are merged into `nutrients_json` via `db.update_food_nutrients_partial()`, and the updated nutrients are returned. Happens once per food; subsequent accesses use the cached data. User-drafted foods are never touched.

**Item 17: Supplement mode, full nutrient coverage, and barcode search — Coded ✓**  *(2026-05-31)*

- **Supplement / unit-based mode** added to both Create and Edit flows in Drafted Food Profiles. Treating 1 tablet = 100g internally means stored per-100g values equal per-tablet label values exactly — no weighing required. Supplement entries store a single portion `{"description": "1 tablet", "gram_weight": 100.0}` so "1 tablet" in a meal contributes those exact amounts.
- **Edit flow supplement detection**: `_do_edit_cached_food` auto-detects supplement mode (single portion with `gram_weight=100`). For user-drafted foods not yet in supplement mode, it asks at the start of the session whether to convert; existing nutrient values are preserved as-is and the gram_weight=100 portion is added.
- **Supplement intro text**: When entering nutrient values in supplement mode, a clear explanation is shown: values should be entered as on the label; no weighing needed; logging "1 tablet" in a meal contributes exactly those amounts.
- **Full vitamin and mineral coverage**: `_prompt_nutrients` now walks through all 11 vitamins (A, C, D, E, K, B1, B2, B3, B6, B9, B12), 6 minerals (Ca, Fe, Mg, P, K, Zn), and 7 phytonutrients as optional sections. Previously only macros, sodium, Ca, and Fe were prompted.
- **IU auto-conversion**: at vitamins A, D, and E prompts, input ending in `IU` is auto-converted (A: ×0.3 mcg RAE; D: ×0.025 mcg; E: ×0.67 mg). The conversion math is printed for verification.
- **Edit option in Drafted Food Profiles menu**: option 3 is now Edit (was absent; editing previously required navigating to Food Cache). Delete moved to 4, Copy to 5.
- **Barcode search**: at any food search prompt, a 12-digit UPC-A or 13-digit EAN barcode (digits only) triggers an Open Food Facts barcode lookup. The product name and brand are shown and the user confirms before caching. Recommended for supplement labels which rarely have USDA records.
- **Food Cache C/N indicator columns**: replaced the wide "Confidence Note" text column with two single-character indicator columns — `C` (source/confidence note present) and `N` (curator notes present). Commands updated: `v#` shows nutrients only, `c#` shows confidence note only, `n#` shows nutrients + protein completeness + both notes (combined view).

**Remaining Phase 2 items — Planned**

- Development of a slightly modified version that will run on Windows operating systems. (The developmental version is Linux-only.)
- Nutrient trend analysis over time (charts or tables)
- Meal planning and dietary pattern analysis
- Transition from a menu-driven interface to graphic user interface.

### Phase 3 — Planned

- Replacement of external editor with internal one - v. `2026-04-13-numa-system-editor-versus-python-replacement` for details
- ?-Integration with smart kitchen devices
- ?-API for third-party app integration
- Machine learning components for dietary recommendations


## Appendix - Understanding Protein Quality: The FAO Reference Values and DIAAS

### The Core Question

When you eat protein, not all of it is equally useful to your body. The usefulness depends on two things: **how much** protein you eat, and **how well-matched** its amino acid composition is to human physiological needs. The FAO reference values and the DIAAS score exist to answer that second question — protein quality — independently of the first.

### The Nine Essential Amino Acids

Your body requires twenty amino acids to build proteins. Eleven of these it can synthesize from other raw materials. The remaining nine — the essential amino acids (EAAs) — must come from food. These nine must all be present simultaneously for protein synthesis to proceed; if any one runs short, it acts as a bottleneck and limits how much protein your body can actually build from what you've eaten. The surplus of the other eight cannot be stored and is instead broken down for energy — a functional waste.

This means that the *pattern* of EAAs in a food matters, not just the total protein quantity.

### Where the FAO Reference Values Come From

Researchers established human requirements for each EAA independently, through controlled human trials. For each amino acid separately, they asked: how much of this amino acid does a healthy adult need per day to maintain physiological function? These studies produced absolute daily requirement figures for each of the nine EAAs, expressed in milligrams per kilogram of body weight per day.

Separately, research has established how much total protein a healthy adult needs per day. By dividing each EAA's daily requirement by the total daily protein requirement, researchers produced a normalized figure: how many milligrams of each EAA a person needs per gram of protein consumed. These normalized figures are the FAO reference values.

The key point is that the reference values for each amino acid were determined *independently*, not in relation to each other. The ratios between EAAs that fall out of the reference values are a byproduct of separately established requirements — not the starting point.

### What the FAO Reference Values Actually Ask

The reference values allow a simple and powerful question to be asked about any food protein:

> If I eat enough of this food to meet my total daily protein needs, will each essential amino acid also arrive in sufficient quantity?

If the answer is yes for all nine EAAs, the protein is high quality — no bottleneck will limit your body's ability to use it. If the answer is no for even one EAA, that amino acid becomes your limiting factor.

### How the Ratio Is Calculated in numa

For each essential amino acid, the ratio shown in numa's output is computed in two steps:

**Step 1 — convert to mg per gram of protein:**

    (AA content in g per 100g food ÷ protein content in g per 100g food) × 1000

This expresses how many milligrams of that amino acid are present for every gram of total protein the food contains.

**Step 2 — divide by the FAO reference value:**

    mg AA per g protein ÷ FAO reference value (mg/g protein)

A ratio of 1.0 means the food hits the reference exactly. A ratio of 2.14 means it delivers more than twice the required amount. A ratio of 0.80 means it delivers only 80% of what is needed.

**Concrete example — cocoa (USDA #169594):**

    Protein:      19.6 g per 100g food
    Tryptophan:    0.293 g per 100g food

    Step 1:  (0.293 / 19.6) × 1000  =  14.9 mg tryptophan per g protein
    Step 2:  14.9 / 7               =  2.14

The FAO reference for tryptophan is 7 mg/g protein. Cocoa's protein delivers 14.9 mg/g — 2.14 times the floor.

### Why Total Protein Is the Denominator

A reasonable question is why the ratio uses total protein (including non-essential amino acids) as its denominator rather than comparing EAA amounts in absolute terms.

Total protein is a normalizing device — a common scale that makes the quality metric meaningful across foods with very different protein concentrations and very different serving sizes.

The practical interpretation is direct: **if a food's protein clears all nine floors, eating enough of that food to meet your daily protein target will automatically also deliver your daily EAA requirements.** No separate EAA accounting is needed. A food that fails even one floor means you would reach your protein target before accumulating enough of that EAA — the protein source is insufficient on its own.

The non-essential amino acids that make up the rest of the protein are biologically irrelevant to this specific calculation. They appear in the denominator only because total protein is the natural unit for expressing protein intake. They are not required to "activate" the EAAs — they are simply passengers.

### What "Complete" Actually Means

"Complete" does not mean the amino acid ratios are all close to 1.0, or close to each other. It means **every one of the nine ratios is at or above 1.0** — each amino acid clears its own independent floor.

The nine FAO reference values were determined in separate human trials, one amino acid at a time. They are not ratios between amino acids; they are nine independent thresholds. Having tryptophan at 2.14× its floor while Met+Cys sits at 1.02× its floor creates no imbalance — the tryptophan surplus cannot compensate for a deficit in another amino acid, but it does not create one either.

A food can therefore have wildly varying ratios across its amino acids and still be complete. Cocoa's protein ranges from 1.02 to 2.25 across the nine amino acids — a factor of more than two between the lowest and highest — and is still complete because nothing falls below 1.0.

The floor analogy: imagine a building with nine rooms, each with its own minimum ceiling height requirement. A room that comfortably exceeds its requirement does not help or hurt any other room. Every room must pass independently.

### The Limiting Amino Acid — A Practical Analogy

When any one EAA ratio falls below 1.0, that amino acid is "limiting" — it acts as a bottleneck that caps how much protein your body can fully incorporate into tissue.

A concrete analogy: you are mixing mortar to build a small wall. You have plenty of dry mix but run out of water before you have mixed enough for the full job. Without water, the remaining dry mix is unusable — you can build only 90 bricks worth of wall instead of 150. The water is your limiting amino acid. The unused dry mix is the protein your body cannot build into tissue, and instead breaks down and excretes.

Complementary proteins work by pooling the limiting amino acids from multiple foods — a grain that is low in lysine paired with a legume that is rich in lysine can together clear all nine floors even though neither does so alone.

### The DIAAS Score

The Digestible Indispensable Amino Acid Score (DIAAS) puts this question into numerical form. For each EAA, it calculates:

> (mg of that EAA actually absorbed per gram of food protein) ÷ (FAO reference value for that EAA)

The word "actually absorbed" is critical. Not all amino acids in a food survive digestion intact and cross into the bloodstream. DIAAS uses ileal digestibility — the fraction of each amino acid absorbed by the end of the small intestine — to correct for this. The result is a score based on what your body actually receives, not merely what was in the food.

A ratio of 1.0 means the food delivers exactly the required amount of that EAA (per gram of protein eaten). A ratio below 1.0 means a shortfall — that EAA is limiting. A ratio above 1.0 means a surplus above the floor. The overall DIAAS score for the food is set by whichever EAA has the lowest ratio — the weakest link.

### A Concrete Example: Chia Seed

Consider a protein quality analysis of chia seed that produces output like this:

```
 Amino Acid      Ratio vs. FAO
 Tryptophan               3.77
 Threonine                1.86
 Isoleucine               1.61
 Leucine                  1.40
 Lysine                   1.30
 Methionine               1.62
 Phenylalanine            1.62
 Valine                   1.47
 Histidine                2.14
```

Every ratio exceeds 1.0. This means that if you eat enough chia seed to meet your total daily protein requirement, every one of the nine EAAs will arrive in at least the required amount. No bottleneck. No limiting amino acid. The protein is complete and efficiently usable.

Lysine at 1.30 is the weakest link — your slimmest margin. It would be the first amino acid to fall below the floor if you ate progressively less chia. But at 1.30, it still clears the threshold comfortably.

Importantly, these ratios do *not* mean that 100 grams of chia seed provides all the EAAs you need for a day. Chia seed contains roughly 17 grams of protein per 100 grams. If your daily protein target is 80 grams, 100 grams of chia gets you only about 21% of the way there. The quality score tells you that every gram of protein chia delivers is efficiently usable — but you still need to eat enough of it to accumulate your daily protein target.

Think of it like fuel efficiency: a car that gets 50 miles per gallon is efficient, but knowing that tells you nothing about whether one gallon is enough to reach your destination. Quality and quantity are separate questions, to be answered separately.

### Summary

| Concept | What it answers |
|---|---|
| FAO reference values | How many mg of each EAA a human needs per gram of protein consumed |
| DIAAS ratio for one EAA | Does this food deliver enough of that EAA, accounting for digestibility? |
| Overall DIAAS score | What is the weakest link — the most limiting EAA in this food? |
| Ratio > 1.0 for all EAAs | Complete protein: no bottleneck, full usability of what you eat |
| Daily protein target | Separate calculation: how many grams of protein do you need total? |

The DIAAS table characterizes the quality of each gram. Hitting your daily protein target is about counting how many grams you eat.