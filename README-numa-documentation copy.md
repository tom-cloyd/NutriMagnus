# numa — Nutritional Analysis Program

A command-line nutritional analysis tool written in Python. Analyzes individual food portions, recipes, and complete meals using data from the USDA FoodData Central database.

UPDATED: 2026-04-04
---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Program](#running-the-program)
- [Menu Structure](#menu-structure)
- [Usage Guide](#usage-guide)
- [Architecture](#architecture)
- [Data Storage](#data-storage)
- [Test Suite](#test-suite)
- [Implementation Phases](#implementation-phases)

---

## Overview

numa was designed from a preliminary specification (see `2025-02-26-python-nutritional analysis program.md`) that called for:

- Calculation of bio-available complete protein combinations for one or more foods
- Nutritional analysis of individual foods, recipes, and meals
- Saving meals by date and saving recipes

The program uses the **USDA FoodData Central** API as its nutrition data source — a free, comprehensive database covering 300,000+ foods with full macro and micronutrient profiles, including amino acid data for protein completeness analysis.

The CLI interface follows the same interaction pattern as `cmgr.py` (the contact manager in the sibling `../cmgr/` directory): hierarchical menus, Ctrl+C to cancel and go back, color themes, and a consistent prompt style throughout.

---

## Project Structure

```
numa/
  numa.py                        — CLI entry point; all menus and user interaction
  db.py                          — SQLite database: schema, queries, context manager
  usda.py                        — USDA FoodData Central API client; nutrient math
  diaas.py                       — Meal-level DIAAS calculation and digestibility data
  export.py                      — Report export (txt, md, html)
  requirements.txt               — Python dependencies
  pytest.ini                     — Test runner configuration
  README-numa-documentation.md   — This file
  tests/
    __init__.py
    conftest.py                  — Shared fixtures (temp DB, CLI runner, sample data)
    test_db.py                   — Database layer tests
    test_usda.py                 — USDA module / pure-function tests
    test_diaas.py                — DIAAS module tests
    test_cli.py                  — End-to-end CLI tests (API mocked)
  .venv/                         — Python virtual environment (not committed)
```

---

## Setup

### 1. Virtual environment

The `.venv` directory is already created and populated. It uses Python 3.13 from the local miniconda installation, matching the `cmgr` project convention.

To recreate it from scratch:

```bash
cd numa
/home/tomc/miniconda3/bin/python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install pytest   # for running tests
```

Dependencies (`requirements.txt`):

| Package    | Purpose                                    |
|------------|--------------------------------------------|
| `typer`    | CLI argument parsing, `--help`, `--api-key` |
| `rich`     | Console output, tables, color themes       |
| `requests` | Available for future use (currently unused; HTTP uses stdlib `urllib`) |

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
inside the program (**Settings → USDA API key**).

---

## Running the Program

```bash
cd numa
./numa.py
```

The program launches directly into the interactive menu. No subcommands are required for normal use.

**Command-line options** (for scripting / setup only):

```
./numa.py --api-key KEY     Set USDA API key and exit
./numa.py --theme THEME     Set color theme: dark, light, neutral, auto
./numa.py --help            Show options
```

**Navigation conventions** (consistent with cmgr):

| Key      | Action                              |
|----------|-------------------------------------|
| `1`–`9`  | Select numbered menu item           |
| `b`      | Go back to the parent menu (works at every prompt) |
| `q`      | Quit the program entirely (works at every prompt)  |
| `s`      | Open Settings (from main menu)      |
| Ctrl+C   | Cancel current prompt, go back      |
| Escape   | Same as Ctrl+C                      |

`b` and `q` are accepted at every prompt throughout the program — menus, food
search results, ID entry, portion size entry, and ingredient/item loops. You
are never required to complete a flow before being able to leave it.

---

## Menu Structure

```
Main Menu
├── 1. Foods
│   ├── 1. Search USDA database
│   │       Search by name → view results table → select food → display full
│   │       nutrient breakdown (per 100g) + protein completeness assessment
│   ├── 2. Analyze a food portion
│   │       Search → select → enter portion size → display scaled nutrients
│   ├── 3. Convert a portion <==> weight
│   │       Search → select → enter volume or weight → display gram equivalent
│   │       (no nutritional analysis; useful for recipe measurement conversion)
│   ├── 4. View cached / saved foods
│   │       List all foods previously fetched and stored locally
│   └── 5. My pantry  (protein sources on hand)
│           Manage a persistent list of protein foods currently in stock.
│           Add via USDA search (links full amino acid data) or by name only.
│           Remove entries by pantry ID. Stored in the local database.
│
├── 2. Recipes
│   ├── 1. Create new recipe
│   │       Name → description → servings → add ingredients (search + portion)
│   │       → saved to local database
│   ├── 2. List recipes
│   ├── 3. View / analyze recipe
│   │       Shows ingredient list + total nutrients for whole recipe + per-serving
│   │       nutrients + digestible complete protein (DCP, saved to DB) + optional
│   │       bioavailability breakdown (DIAAS per ingredient) + protein completeness.
│   │       If any ingredient lacks weight or DIAAS data, prompts to provide values
│   │       or calculate anyway (result flagged approximate and not saved).
│   ├── 4. Edit recipe
│   │       Edit name/description/servings/instructions, or add/edit/remove/reorder
│   │       ingredients. DCP is recomputed and saved on any ingredient change.
│   └── 5. Delete recipe
│
├── 3. Meals & Log
│   ├── 1. Log a new meal
│   │       Date (default today) → meal name → add foods and/or recipes by portion
│   │       → saved to local database with date
│   ├── 2. View/edit meals for a date
│   ├── 3. Analyze a logged meal
│   │       Single meal or all meals for a day → combined nutrient totals
│   │       + meal-level DIAAS analysis (digestibility-corrected, pooled across
│   │       all ingredients) + protein completeness + complement suggestions
│   └── 4. Delete a meal
│
├── 4. Daily Summary
│   ├── 1. Today's summary
│   │       Sums all meals logged today → full nutrient breakdown
│   │       + meal-level DIAAS analysis + protein completeness + complement suggestions
│   ├── 2. Summary for a specific date
│   └── 3. Recent days (list dates that have meals)
│
└── s. Settings
    ├── 1. USDA API key
    ├── 2. Color theme  (dark / light / neutral / auto)
    ├── 3. Database path (display only)
    └── 4. Protein digestibility overrides  (for meal-level DIAAS calculation)
```

---

## Usage Guide

### Searching for a food

Select **Foods → Search USDA database**, enter a search term (e.g., "chicken breast"), and pick from the results table. The program fetches the full nutrient profile and caches it locally so subsequent lookups of the same food are instant.

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

Select **Foods → Analyze a food portion**. After picking a food, enter your portion size. Accepted formats:

| Input | Example | Notes |
|---|---|---|
| Plain number | `150` | Treated as grams |
| Fraction | `1/4` | Treated as grams |
| Mixed number | `1 1/2` | Treated as grams |
| Weight with unit | `3 oz`, `0.5 lb` | Converted to grams |
| Volume | `1/4 cup`, `2 tbsp` | Converted via food density |
| USDA portion shortcut | `p1`, `p2` | Uses gram weight shown in the portions list |
| Portion multiple | `1.5 p1` | 1.5 × the gram weight of portion 1 |

Volume inputs (`cup`, `tbsp`, `tsp`, `ml`) are converted to grams using the food's density. Density is derived from the USDA portions data when available (e.g., if USDA lists "1 cup = 240 g", that is used directly). For foods without a cup/tablespoon portion entry, a built-in density table covers common whole foods. If density cannot be determined, the program will say so and ask for grams instead.

Nutrients are scaled proportionally from the 100g USDA reference values.

### Protein completeness

Wherever protein is analyzed (food, recipe, or meal), numa automatically checks whether the protein is "complete" — meaning it contains all nine essential amino acids at or above the FAO/WHO reference levels. This requires that the USDA entry for the food includes amino acid data (most whole foods in the Foundation and SR Legacy datasets do).

The output shows:
- Complete / Incomplete designation
- The most limiting amino acid (if incomplete)
- A score bar for each essential amino acid vs. the reference level

#### No amino acid data?

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

DIAAS scores are not available from any API — they come from controlled digestion studies conducted in laboratory settings. numa uses a static lookup table of ~50 common food categories, built from FAO 2013 reference values and peer-reviewed studies (principally Mathai et al. 2017, *Br J Nutr*; Gorissen et al. 2018, *Amino Acids*). The lookup uses keyword matching on the food name (case-insensitive, longest match wins).

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

#### Digestibility data — three-tier lookup

For each food, the digestibility coefficient is resolved in order:

1. **User override** — an exact food-name entry you set in Settings → Protein digestibility overrides. Takes precedence over everything else.
2. **Curated table** (~50 entries in `diaas.py`) — literature-sourced values for specific foods and categories, with citations. Covers all common plant proteins.
3. **Category default** — broad averages when no specific match is found (isolated plant protein: 0.92, legume: 0.80, seed: 0.82, nut: 0.78, grain/cereal: 0.82, animal: 0.96). The source description shows `~est` in the output.
4. **Overall default: 0.82** — if nothing matches, a conservative plant-protein average is used.

The source of each digestibility value is shown in the ingredient table. Estimated values are also listed in a footnote.

#### Protein digestibility overrides

Settings → **Protein digestibility overrides** lets you set a specific digestibility coefficient for any food you have found a primary-literature value for. This is a power-user feature — the curated table covers most common plant proteins and the category defaults are defensible estimates. Overrides are stored in the `diaas_overrides` table and survive across sessions. The interface shows you what value numa would use without the override before asking for your input.

### Protein complement suggestions

Wherever protein is analyzed, numa checks for essential amino acid gaps and — if any exist — offers to show complement suggestions:

```
Show protein complement suggestions?  (y/N)
```

Press `y` to see the suggestions. The flow is:

1. **Pantry suggestions** — foods from your My Pantry list that can close the gap, shown first, ranked by gaps closed then by smallest required amount (up to 3 per page).
2. After the pantry section, you are asked: `Look elsewhere for more options?  (y/N)` — if yes, the general list is shown.
3. **General suggestions** — foods from a curated built-in table of common plant protein sources, shown up to 5 at a time.

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
- **Digestible protein added** and updated **total bioavailable complete protein**

**Why score 1.0?** The score is a ratio against the FAO 2013 reference pattern (mg of amino acid per g of protein that humans require). A score of 1.0 means the combined profile exactly meets requirements — it is the floor, not an aspirational target. Suggesting a complement that only reaches 0.85 would mean the gap remains open.

The advisor is triggered automatically at the end of food search, portion analysis, recipe view, meal analysis, and daily summary — wherever amino acid data is present. If the food has no amino acid data, the offer is skipped silently.

The pantry is the key input: populate **Foods → My pantry** with the protein sources you keep on hand and the advisor will always prioritize those over generic suggestions.

### Building a recipe

Select **Recipes → Create new recipe**. After entering the recipe name and serving count, you add ingredients one at a time via the food search flow. Each ingredient is stored with its weight. When you later view the recipe, numa calculates total nutrients and per-serving nutrients by summing all ingredients scaled to their specified amounts.

### Logging a meal

Select **Meals & Log → Log a new meal**. Enter a date (defaults to today) and a name (e.g., "Breakfast"). Then add food items (searched from USDA/cache) or saved recipes by number of servings. The meal is timestamped and stored.

### Daily summary

Select **Daily Summary → Today's summary** to see the combined nutrition for all meals logged today. Use **Summary for a specific date** to look back at any past day.

---

## Architecture

### `numa.py` — CLI and menus

Entry point via `typer`. When invoked without a subcommand, `main()` initializes the database and launches `_run_menu()`.

The menu system follows a strict pattern:
- `_show_menu(title, items)` renders a title, horizontal rule, and numbered/lettered items
- Each submenu is a function returning `bool` — `True` means "go back", `False` means "quit"
- The parent menu checks the return value: `if not _menu_foo(): break`
- `_prompt()` is a raw tty reader that converts Ctrl+C and Escape into a `Cancelled` exception
- `_safe_call(fn, *args)` wraps every action call to catch `Cancelled` and return to the menu

The `_search_and_pick_food()` helper handles the full food lookup flow: prompt → call USDA search → display table → user picks → check local cache → fetch detail if not cached → return food dict. It is reused everywhere a food needs to be selected (analyze, recipe ingredient, meal item).

`_compute_meal_nutrients(meal_id)` is the core aggregation function. It fetches all items for a meal, scales each food's nutrients from the 100g base to the logged portion size, and sums them. For recipe items, it first aggregates the recipe's ingredients, then scales by the requested number of servings.

`_compute_meal_ingredient_list(meal_id)` returns per-ingredient data in the form needed by `diaas.meal_level_diaas()`: a list of `{food_name, nutrients_100g, grams}` dicts. Recipe items are expanded into their constituent ingredients, each scaled by the requested serving portion. Used by meal analysis and daily summary to supply the DIAAS calculation.

`_print_meal_diaas(ingredient_list)` renders the full meal-level DIAAS output: per-ingredient digestibility table, IAA composite ratio table with bar chart, composite DIAAS, digestible complete protein, and caveats for missing data or estimated digestibility values.

**Recipe DCP functions:**

`_compute_recipe_dcp(rid)` silently computes digestible complete protein (grams, whole recipe) for a given recipe ID. Used by `_do_recipe_edit` to recompute and save DCP whenever ingredients change. Returns `None` if amino acid data is unavailable.

`_resolve_recipe_dcp_data(ingredients, ingredient_stats, combined)` is called from `_do_recipe_view` before displaying tables. It detects three data gaps — ingredients with unknown weight, ingredients with no DIAAS entry, and recipes with no amino acid profile — then presents the user with options: provide the missing data now, calculate anyway (result flagged approximate and not saved), or skip DCP entirely. Returns `None` on skip; otherwise returns `(updated_stats, updated_combined, approximate, notes)`.

`_print_recipe_bioavailability(ingredient_stats, analysis_nutrients)` renders the per-ingredient DIAAS table (ingredient, protein, DIAAS, digestible protein), total digestible protein, effective DIAAS, and digestible complete protein with the limiting amino acid score applied.

### `db.py` — SQLite database

All persistence goes through a `get_db()` context manager that commits on clean exit and rolls back on exception. The database path is `~/.local/share/numa/numa.db`.

**Schema:**

| Table                | Purpose                                              |
|----------------------|------------------------------------------------------|
| `foods`              | Local cache of USDA food entries (nutrients as JSON) |
| `recipes`            | Recipe metadata (name, servings, description, `dcp_g`) |
| `recipe_ingredients` | One row per ingredient; foreign key to `recipes`     |
| `meals`              | Meal log entries with date                           |
| `meal_items`         | Foods or recipes added to a meal; foreign key to `meals` |
| `pantry`             | User's protein-source inventory (food name, optional fdc_id, notes) |
| `diaas_overrides`    | User-set true ileal digestibility coefficients, keyed by food name |

`recipes.dcp_g` stores the digestible complete protein (grams, whole recipe) computed at last view. It is `NULL` when the recipe has never been viewed, when the calculation was approximate (user-provided data), or when amino acid data was unavailable. The recipe list shows DCP per serving when this value is present.

All nutrient data is stored as a JSON blob in `foods.nutrients_json`, keyed by the same field names used throughout (`calories`, `protein_g`, `carbs_g`, etc.). This avoids schema migrations when nutrient tracking is expanded.

### `usda.py` — USDA API client and nutrient math

**API:** USDA FoodData Central REST API (`https://api.nal.usda.gov/fdc/v1`). Uses stdlib `urllib` — no `requests` dependency at runtime.

`NUTRIENT_MAP` is a dict mapping USDA nutrient IDs (integers) to `(our_key, display_label, unit)` tuples. It covers 45 nutrients: macros, minerals, vitamins, 7 phytonutrients/bioactive compounds, and 11 amino acids (including tyrosine, added to support Phe+Tyr combined scoring in meal-level DIAAS).

**Key functions:**

| Function | Purpose |
|---|---|
| `search_foods(query)` | Search USDA; returns list of result dicts |
| `get_food_detail(fdc_id)` | Fetch full nutrient profile for one food |
| `scale_nutrients(nutrients, amount, base_size=100)` | Scale a nutrient dict from base_size to amount |
| `sum_nutrients(*dicts)` | Add any number of nutrient dicts together |
| `protein_completeness(nutrients)` | Assess essential amino acid completeness vs. FAO/WHO reference. Requires 5+ AAs with **non-zero** values; zero-keyed AA entries (common in branded USDA foods) are ignored. |
| `get_aa_gaps(nutrients)` | Return `(aa_key, score, deficit_g)` for each essential AA below 1.0, sorted most-limiting first |
| `suggest_complements(base_nutrients, pantry_candidates)` | Compute minimum-gram complement suggestions from pantry and curated table; returns `{"pantry": [...], "general": [...]}` |
| `nutrient_label(key)` | Reverse-lookup display name and unit for any nutrient key |
| `get_diaas(food_name)` | Return DIAAS protein digestibility score for a food (keyword lookup) |
| `get_antinutrient_flags(food_name)` | Return consolidated anti-nutrient flags as a list of `{"problem": str, "cause": str, "solutions": [(label, description), ...]}` dicts. Entries sharing the same group (e.g. legume phytate + seed phytate on the same food) are merged into one flag with multiple solutions. |
| `get_density_g_per_ml(food_name, portions)` | Estimate g/ml density for volume-to-weight conversion. Static table takes priority over USDA portion data. |

`_parse_food()` normalizes USDA API responses — the API returns nutrients in three different formats depending on the endpoint (`nutrientId`, `nutrient.id`, or `number`), and `_parse_food` handles all three.

**Protein completeness method:** The FAO 2013 dietary protein quality evaluation reference pattern (mg of each essential amino acid per gram of protein) is used. A food scores each essential amino acid by dividing its actual mg/g-protein content by the reference value. A score ≥ 1.0 on all nine essential amino acids means complete protein. The most limiting amino acid is the one with the lowest score.

**DIAAS lookup (`get_diaas`):** A static ordered table of ~50 food categories maps keyword patterns to DIAAS scores from FAO 2013 and peer-reviewed digestion studies. Used for single-food bioavailability display (recipe ingredient table, food analysis). Scores above 1.0 are capped at 1.0. More specific entries (e.g., "soy protein isolate") are listed before general ones (e.g., any soy keyword) — first match wins. Note: this is distinct from the digestibility coefficients in `diaas.py`, which are used for meal-level pooled calculation.

**Anti-nutrient flags:** A static table maps food keywords to advisory messages (phytate, oxalate, lectins, trypsin inhibitors, bound niacin). Flags can be suppressed by cooking-state keywords — e.g., "cooked"/"boiled" suppresses lectin and trypsin inhibitor warnings for beans, since these compounds are fully inactivated by cooking.

**Density lookup:** `get_density_g_per_ml` first checks the food's USDA portion list for any cup or tablespoon entry and derives density from it. If none is found, it falls back to a static keyword table covering ~50 food categories. Returns `None` if density cannot be determined.

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

---

## Data Storage

| Location | Contents |
|---|---|
| `~/.local/share/numa/numa.db` | SQLite database (foods cache, recipes, meals) |
| `~/.config/numa/config.json` | API key |
| `~/.config/numa/theme` | Saved color theme preference |

---

## Test Suite

**276 tests** covering the database layer, USDA pure functions, DIAAS calculation, user profile/RDA computation, and the full CLI.

```bash
cd numa
.venv/bin/pytest          # run all tests
.venv/bin/pytest -v       # verbose output
.venv/bin/pytest tests/test_usda.py   # one file only
```

### Test files

| File | What it tests |
|---|---|
| `tests/conftest.py` | Shared fixtures — see below |
| `tests/test_db.py` | Schema creation, all CRUD helpers, cascade deletes, rollback on exception |
| `tests/test_usda.py` | `scale_nutrients`, `sum_nutrients`, `_parse_food` (all three nutrient ID formats), `protein_completeness`, `nutrient_label`, `get_diaas`, `get_antinutrient_flags` |
| `tests/test_diaas.py` | `get_digestibility` (curated, category, default, user override), `meal_level_diaas` (edge cases, complementarity, Met+Cys pairing, scaling, gap flags), CRUD for `diaas_overrides` |
| `tests/test_profile.py` | `load_profile`, `save_profile`, `bmr`, `compute_rda` (sex/age/activity variants) |
| `tests/test_cli.py` | All five menus end-to-end via `CliRunner`; USDA API mocked; profile settings and RDA comparison |

### Key fixtures (`tests/conftest.py`)

| Fixture | Scope | Purpose |
|---|---|---|
| `use_test_db` | autouse | Redirects `db._DB_PATH` to a per-test temp file; every test gets a fresh isolated database automatically |
| `db_conn` | function | Raw `sqlite3.Connection` to the temp DB for direct assertion queries |
| `runner` | function | `typer.testing.CliRunner(env={"COLUMNS": "200"})` — wide terminal prevents table truncation |
| `cached_food` | function | Pre-inserts the sample chicken breast food into the DB cache; use in any test that needs a food without an API call |

### Mocking strategy

USDA API calls are mocked at the `usda.search_foods` and `usda.get_food_detail` level using `monkeypatch`. The `_mock_api()` helper in `test_cli.py` patches both functions to return constant sample data (chicken breast, 100g, with full amino acid profile) and patches `usda.get_api_key` to return a dummy key, bypassing the API key prompt entirely.

No tests touch the network. No tests touch the real database.

---

## Implementation Phases

The original design specified three phases. Phase 1 is complete.

### Phase 1 — Coding of core features: Complete ✓ | Testing and validation: in progress

- USDA FoodData Central API integration
- Food search, portion analysis, local food cache
- Recipe builder (create, view, analyze, delete)
- Meal log with date (log, view, analyze, delete)
- Daily nutrition summary
- Protein completeness analysis via amino acid profile
- Full test suite (130 tests)

### Phase 2 — In progress

**Item 1: Expanded nutrient tracking — Coded | Validation in progress**

- Seven additional phytonutrients and bioactive compounds tracked from the USDA database: carotenoids (beta-carotene, alpha-carotene, lycopene, lutein+zeaxanthin), choline, beta-sitosterol, and isoflavones.
- Protein bioavailability assessment using DIAAS: a keyword lookup table covering 50+ foods shows the digestibility-adjusted protein figure alongside raw protein grams.
- Anti-nutrient advisories: flags foods with phytate, oxalate, lectins, trypsin inhibitors, or bound niacin, with practical notes on how cooking reduces their effect. Flags are suppressed automatically when the food name indicates it has already been cooked or processed.
- Volume-to-weight conversion: portion sizes can now be entered as volumes (e.g., `1/8 cup`, `2 tbsp`). Density is derived from the static keyword table first; USDA portion data is used as a fallback. Fraction and mixed-number input (e.g., `1/4`, `1 1/2`) also supported.
- **Digestible complete protein (DCP) per recipe**: recipe view computes and saves DCP (grams per serving) to the database. The value reflects DIAAS-adjusted protein × the limiting amino acid score, giving a single number for how much complete, digestible protein the recipe delivers. Displayed in the recipe list as "DCP/srv". Recomputed automatically when any ingredient is added, edited, or removed. If an ingredient lacks weight or DIAAS data, the user is prompted to supply the missing information or to calculate anyway (approximate results are flagged and not saved to the database).

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
- `suggest_complements()` in `usda.py` uses the primary-gap algebraic solve: given the base protein and the candidate's AA/protein ratio, it computes the exact gram weight that closes the most limiting gap, then re-scores all nine essential AAs at that combined weight. Candidates whose AA/protein ratio is already below the reference (i.e., adding them makes the gap worse) are silently excluded.
- Pantry foods with no USDA cache entry fall back to the built-in curated table by keyword match, so name-only pantry entries still participate.
- The advisor is called automatically at the end of: food search, portion analysis, recipe analysis, meal analysis, and daily summary — wherever amino acid data is present.

**Item 4: Meal-level DIAAS analysis — Coded ✓**

- Meal analysis and daily summary now compute a composite meal-level DIAAS score using the FAO 2013 pooled-IAA methodology (see `diaas.py`).
- A true ileal digestibility coefficient is applied per ingredient before pooling, capturing amino acid complementarity across the whole meal.
- Digestibility coefficients sourced from a three-tier lookup: ~50-entry curated literature table → category defaults → 0.82 overall default. User overrides stored in the `diaas_overrides` DB table take precedence over all.
- Output: per-ingredient digestibility table, per-IAA composite ratio table with bar indicators, composite DIAAS, and digestible complete protein in grams.
- Tyrosine (USDA nutrient 1218) added to `NUTRIENT_MAP` so future food fetches include it for proper Phe+Tyr combined scoring.
- Settings menu extended with **Protein digestibility overrides** for power users who have primary-literature values for specific foods.
- 55 new tests in `tests/test_diaas.py` covering all lookup tiers, DB CRUD, calculation correctness, complementarity, and edge cases. Total test count: 224.

**Item 5: User profile and personalized RDA comparison — Coded ✓**

- A user profile (age, sex, weight in kg, height in cm, activity level) is set under **Settings → User profile** and persisted to `~/.config/numa/profile.json`.
- Calorie target is computed via the Mifflin-St Jeor equation × an activity multiplier. Protein target scales with body weight and activity level (0.8–1.2 g/kg).
- All other targets follow NIH/Institute of Medicine Dietary Reference Intakes: sex-specific values for iron, calcium, potassium, choline, and B vitamins; age-adjusted values for calcium (women 51+, men 70+), vitamin D (70+), fiber (50+), and vitamin B6 (51+).
- After any **Daily Summary**, if a profile is set, numa offers "Compare to your personalized RDA targets?". The comparison table shows each tracked nutrient's intake, target, percentage of RDA, a color-coded bar (green/yellow/red), and a plain-language status note. Sodium uses the limit direction (green if under, red if over); all other nutrients use the minimum direction.
- If no profile is set, a tip to configure one is shown instead. 28 new tests in `tests/test_profile.py`; 8 new CLI tests in `tests/test_cli.py`. Total test count: 276.

**Remaining Phase 2 items — Planned**

- Nutrient trend analysis over time (charts or tables)
- Meal planning and dietary pattern analysis

### Phase 3 — Planned

- Barcode scanning for packaged foods
- Integration with smart kitchen devices
- API for third-party app integration
- Machine learning components for dietary recommendations

---

## Appendix A — Phase 2 Expanded Nutrient Tracking: Research Notes

### Phytonutrients
Bioavailability — Protein
**What USDA FDC already has** (just not tracked yet — easy wins):

| Nutrient | USDA ID |
|---|---|
| Beta-carotene | 1107 |
| Alpha-carotene | 1108 |
| Lycopene | 1122 |
| Lutein + zeaxanthin | 1123 |
| Choline | 1180 |
| Isoflavones (total) | 1340 |
| Beta-sitosterol (phytosterol) | 1285 |

These can be added to `NUTRIENT_MAP` in `usda.py` with no other changes — USDA already returns them, we just discard them.

**What USDA FDC does NOT have well:**
- Polyphenols (flavonoids, resveratrol, quercetin, etc.)
- Glucosinolates (broccoli, kale, Brussels sprouts)
- Most individual flavonoid subclasses

For those, the only serious free database is **Phenol-Explorer** (phenol-explorer.eu), which has a REST API. It covers ~500 foods and ~900 polyphenols. It would require a second API integration and a separate cache table — doable but a significant addition.

---

### Bioavailability — Protein

**The current implementation** uses a PDCAAS-style approach: compare the food's AA profile against the WHO/FAO reference pattern. This is correct as far as it goes, but it ignores **digestibility** — how much protein actually gets absorbed.

The modern standard is **DIAAS** (Digestible Indispensable Amino Acid Score), which corrects for ileal digestibility per amino acid. This matters a lot for plant foods:

| Source | DIAAS |
|---|---|
| Whey / egg | 1.09 / 1.13 |
| Soy protein isolate | 0.90–1.00 |
| Pea protein | 0.82 |
| Chickpeas | 0.83 |
| Lentils | 0.75 |
| Black beans | 0.75 |
| Brown rice | 0.59 |
| Wheat (whole) | 0.46 |

DIAAS values are **not in any API** — they come from controlled digestion studies. The practical implementation is a static lookup table keyed by food name or category.

**Anti-nutrients** compound the problem further:

| Anti-nutrient | Effect | Reduced by |
|---|---|---|
| Phytate | Binds iron, zinc, calcium | Soaking, fermenting, sprouting |
| Oxalate | Binds calcium | Cooking (partial) |
| Tannins | Inhibit iron absorption | Not pairing with tea/coffee |
| Trypsin inhibitors | Reduce protein digestion | Cooking (fully inactivated) |
| Lectins | Reduce protein digestion | Cooking (fully inactivated) |

USDA doesn't track anti-nutrients at all. This would also require a static lookup.

---

### What is feasible to implement

**High value, low effort:**
- Add the USDA phytonutrient IDs listed above to `NUTRIENT_MAP` — a 10-minute change that immediately enriches every food already in the cache

**Medium effort, high value for the project's stated goals:**
- A static DIAAS table for ~50 common plant foods, used to display an "adjusted protein" figure alongside raw protein grams
- A static anti-nutrient flag table (e.g., "high phytate — consider soaking") shown when a food is added to a meal

**Significant effort:**
- Phenol-Explorer API integration for polyphenols
- Cooking/processing adjustments to bioavailability (requires a rules engine per food category)

---

The most impactful first step for this project's plant-protein focus is (1) add the easy USDA phytonutrients, then (2) implement a DIAAS lookup table with adjusted protein display. That directly addresses the core problem stated in the project description — something no standard nutrition app does.
