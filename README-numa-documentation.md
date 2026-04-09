# numa — Nutritional Analysis Program

A command-line nutritional analysis tool written in Python. Analyzes individual food portions, recipes, and complete meals using data from the USDA FoodData Central database. The program presents itself to users as **Nutrimagnus**.

UPDATED: 2026-04-08 - 17:19 PM Pacific Time
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
  numa.py                          — thin CLI entry point (argparse); delegates to numa_app.main
  db.py                            — SQLite database: schema, queries, context manager
  usda.py                          — USDA FoodData Central API client; nutrient math
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
    state.py                       — AppContext; theme/dietary state; set_theme(), set_include_animal_foods()
    config/
      __init__.py
      prefs.py                     — dietary preferences load/save; first-run animal-foods prompt
      theme.py                     — theme load/save/detect; _change_theme()
    ui/
      __init__.py
      common.py                    — _show_menu(), _safe_call()
      prompts.py                   — _prompt(), Cancelled, _ask_float(), _ask_int(), _ask_date()
      render.py                    — _print_nutrient_table(), _print_protein_completeness(),
                                     _print_bioavailability(), _print_complement_suggestions()
    services/
      __init__.py
      portions.py                  — _pick_portion(), _parse_portion_input()
      reports.py                   — export rendering support
      search.py                    — _search_and_pick_food(), _suggest_foundation_search()
    workflows/
      __init__.py
      foods.py                     — Foods menu and all food-analysis handlers
      pantry.py                    — My Pantry menu
      meals.py                     — Meals & Log menu
      recipes.py                   — Recipes menu
      settings.py                  — Settings menu; user profile; DIAAS overrides; RDA comparison
      summary.py                   — Daily Summary menu
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
inside the program (**Settings → USDA API key**).

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

**Navigation conventions** (consistent with cmgr):

| Key      | Action                              |
|----------|-------------------------------------|
| `1`–`9`  | Select numbered menu item           |
| `b`      | Go back to the parent menu (works at every prompt) |
| `q`      | Quit the program entirely (works at every prompt)  |
| `d`      | Open Dietary preferences (from main menu)          |
| `s`      | Open Settings (from main menu)      |
| Ctrl+C   | Cancel current prompt, go back      |
| Escape   | Same as Ctrl+C                      |

`b` and `q` are accepted at every prompt throughout the program — menus, food
search results, ID entry, portion size entry, and ingredient/item loops. You
are never required to complete a flow before being able to leave it.

**First run:** On first launch, if no dietary preferences file exists, the program asks whether protein complement suggestions should include animal-based foods (eggs, cheese, fish, chicken, whey). The answer is saved to `~/.config/numa/prefs.json` and can be changed at any time via `d` or **Settings → Dietary preferences**.

---

## Menu Structure

```
Main Menu  ("Nutrimagnus Menu")
├── 1. Foods
│   ├── 1. Search food databases (USDA and others)
│   │       Search by name → view results table → select food → display full
│   │       nutrient breakdown (per 100g) + protein completeness assessment.
│   │       Optionally proceed directly to portion analysis from the same flow.
│   ├── 2. Analyze a USDA food portion
│   │       Search → select → enter portion size → display scaled nutrients
│   ├── 3. Analyze a saved recipe portion         ← added
│   │       List saved recipes → select by ID → enter portion (number of servings
│   │       or fraction) → display scaled nutrient totals + protein completeness
│   ├── 4. Convert a portion <==> weight
│   │       Search → select → enter volume or weight → display gram equivalent
│   │       (no nutritional analysis; useful for recipe measurement conversion)
│   ├── 5. View cached / saved foods
│   │       List all foods previously fetched and stored locally
│   └── 6. My pantry  (protein sources on hand)
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
├── d. Dietary preferences         ← top-level shortcut
│       Toggle whether complement suggestions include animal-based foods.
│       Saved immediately; also accessible under Settings → Dietary preferences.
│
└── s. Settings
    ├── 1. USDA API key
    ├── 2. Color theme  (dark / light / neutral / auto)
    ├── 3. Database path (display only)
    ├── 4. Protein digestibility overrides  (for meal-level DIAAS calculation)
    ├── 5. Dietary preferences  (animal foods included / plant-based only)
    └── 6. User profile  (age, sex, weight, height, activity level)
```

---

## Usage Guide

### Searching for a food

Select **Foods → Search food databases**, enter a search term (e.g., "chicken breast"), and pick from the results table. The program fetches the full nutrient profile and caches it locally so subsequent lookups of the same food are instant.

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
| Plain number | `150` | Treated as grams |
| Fraction | `1/4` | Treated as grams |
| Mixed number | `1 1/2` | Treated as grams |
| Weight with unit | `3 oz`, `0.5 lb` | Converted to grams |
| Volume | `1/4 cup`, `2 tbsp` | Converted via food density |
| USDA portion shortcut | `p1`, `p2` | Uses gram weight shown in the portions list |
| Portion multiple | `1.5 p1` | 1.5 × the gram weight of portion 1 |

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

### Dietary preferences

The `d` key at the main menu (or Settings → Dietary preferences) toggles whether protein complement suggestions include animal-based foods (eggs, cheese, fish, chicken, whey protein). The setting is saved immediately to `~/.config/numa/prefs.json` and applied to both pantry and general suggestions.

### Building a recipe

Select **Recipes → Create new recipe**. After entering the recipe name and serving count, you add ingredients one at a time via the food search flow. Each ingredient is stored with its weight. When you later view the recipe, numa calculates total nutrients and per-serving nutrients by summing all ingredients scaled to their specified amounts.

### Logging a meal

Select **Meals & Log → Log a new meal**. Enter a date (defaults to today) and a name (e.g., "Breakfast"). Then add food items (searched from USDA/cache) or saved recipes by number of servings. The meal is timestamped and stored.

### Daily summary

Select **Daily Summary → Today's summary** to see the combined nutrition for all meals logged today. Use **Summary for a specific date** to look back at any past day.

---

## Architecture

### Overview — the refactor

The original monolithic `numa.py` was split into a `numa_app/` package (see `README-refactor.md`). The split is organized by responsibility:

- **`numa.py`** — five lines: parse args with `argparse`, call `run_app()`. Uses stdlib only; no `typer`.
- **`numa_app/main.py`** — top-level orchestration: `initialize_app()`, `print_startup_banner()`, `_run_menu()`, `run_app()`.
- **`numa_app/state.py`** — shared mutable state: `AppContext` dataclass holding the `Console`, current theme, and dietary preference flag. Module-level aliases (`console`, `T`, `_current_theme_name`, `_include_animal_foods`) are kept for convenience; `sync_globals()` refreshes them when state changes.
- **`numa_app/config/`** — persistence for theme and dietary preferences.
- **`numa_app/ui/`** — all terminal I/O primitives and rendering.
- **`numa_app/services/`** — stateless helpers for food search, portion parsing, and report export.
- **`numa_app/workflows/`** — one file per top-level menu area; each contains the menu loop and the handlers for every item in that section.

The support modules (`db.py`, `usda.py`, `diaas.py`, `export.py`, `profile.py`) were copied intact and are imported by the workflow modules as needed.

### `numa_app/main.py` — startup and top-level menu

`initialize_app()` handles `--api-key` and `--theme` command-line flags (both exit after acting), calls `db.init_db()`, loads dietary preferences, and on first run triggers the animal-foods preference prompt.

`print_startup_banner()` renders the double green rule, program name ("Nutrimagnus"), profile summary, and theme/dietary status before the menu appears.

`_run_menu()` is the top-level loop. It renders the main menu inline (not via `_show_menu()`), dispatches to workflow submenus by return value — `True` means go back, `False` means quit — and handles the `d` shortcut for dietary preferences.

### `numa_app/state.py` — shared state

`AppContext` is the single source of truth. `set_theme(name, theme_dict)` and `set_include_animal_foods(value)` are the only mutation points; both call `sync_globals()` to keep the module-level aliases in sync with the dataclass. All workflow modules import `state` and reference `state.T`, `state.console`, `state._include_animal_foods` directly.

### `numa_app/ui/prompts.py` — input primitives

`_prompt(prompt_text, *, default, choices, prefill)` is the core input function. It has two paths:

- **Non-tty** (e.g., piped input, test runner): delegates to `rich.prompt.Prompt.ask()`.
- **Interactive tty**: reads raw characters via `termios`/`tty`. Ctrl+C and `\x04` (EOF) raise `Cancelled`. Escape is detected by checking for trailing bytes within 50 ms; a bare Escape with no following bytes raises `Cancelled`. Backspace/delete are handled by popping from the buffer and overwriting the terminal.

`prefill=True` uses `readline.set_pre_input_hook` to pre-populate the input line with the default value, allowing the user to edit it in-place (e.g., for recipe name edits). This path requires an interactive tty and a non-empty default.

`Cancelled` is a plain exception class raised at any prompt when the user cancels. It propagates up to `_safe_call()` or the enclosing workflow, which prints `[dim]Cancelled.[/dim]` and returns the menu to the previous level.

`_ask_float()`, `_ask_int()`, `_ask_date()` are thin wrappers that append `(b=back, q=quit)` to the prompt text and handle the `b` (return `None`) and `q` (`SystemExit(0)`) shortcuts.

### `numa_app/ui/common.py` — menu rendering and safe dispatch

`_show_menu(title, items)` renders a title, horizontal rule, and numbered/lettered items. Numeric keys are styled with the accent color; non-numeric keys (b, q, etc.) use dim.

`_safe_call(fn, *args)` wraps every action call to catch `Cancelled` (prints "Cancelled.") and re-raises `SystemExit(0)` cleanly. Used throughout workflow modules to dispatch individual menu actions without the caller needing try/except.

### `numa_app/ui/render.py` — output rendering

`_print_nutrient_table(nutrients, title, per_label)` renders a Rich table of nutrients grouped into Macronutrients, Minerals, Vitamins, and Phytonutrients. Only groups with at least one present key are shown.

`_print_protein_completeness(nutrients)` checks all nine essential amino acids against the FAO reference. Returns `True` if amino acid data was present, `False` if not. Requires 5+ AAs with non-zero values — zero-keyed entries (common in branded USDA foods) are treated as absent.

`_print_bioavailability(food_name, nutrients)` calls `usda.get_diaas()` and `usda.get_antinutrient_flags()` and renders the bioavailability block (DIAAS bar, digestible protein, anti-nutrient notes).

`_print_complement_suggestions(nutrients, context, offer_if_covered, base_food_name)` renders the pantry-then-general complement suggestion flow. `offer_if_covered=False` suppresses the offer when the food already meets the reference (used for single-food display). `offer_if_covered=True` always shows (used after recipe analysis).

### `numa_app/services/search.py` — food lookup flow

`_search_and_pick_food()` handles the full food lookup: prompt → USDA search → display results table → user picks → check local cache → fetch detail if not cached → return food dict. Reused by every workflow that needs a food selected.

`_suggest_foundation_search(food)` is called when the selected food has no amino acid data. It offers to re-search Foundation Foods using a pre-filled keyword (first token of the food name), shows results, and returns the user's pick or `None`.

### `numa_app/services/portions.py` — portion parsing

`_parse_portion_input(raw, portions, food_name)` parses a portion string and returns `(grams, label)`. Accepted formats: plain number (grams), fractions (`1/4`), mixed numbers (`1 1/2`), weight with unit (`3 oz`, `0.5 lb`), volume (`1/4 cup`, `2 tbsp`, `1 tsp`, `ml`), USDA portion shortcuts (`p1`, `p2`), and portion multiples (`1.5 p1`). Returns `None` on unrecognised input, a string error message when the format is recognised but density is unavailable.

`_pick_portion(food)` renders the USDA portions list for the food, then loops on `_parse_portion_input` until the user enters a valid amount or cancels.

### `numa_app/workflows/settings.py` — settings menu, profile, and RDA

`_menu_settings()` renders the six-item settings menu. Each item status is shown inline (key status, current theme, current dietary setting, current profile summary).

`_do_user_profile()` collects age, sex, weight (accepts kg or lb), height (accepts cm or feet+inches), and activity level. Existing values are shown and kept on empty input. On save, prints the computed calorie and protein targets.

`_print_rda_comparison(nutrients, profile)` renders a table comparing daily nutrient totals against personalized RDA targets. For each nutrient it shows intake, target, percentage of RDA, a color-coded bar (green/yellow/red), and a status note. Sodium uses the limit direction (green if under); all others use the minimum direction.

`_do_dietary_prefs()` toggles the animal-foods preference, saves to `prefs.json`, and updates `state._include_animal_foods` immediately.

`_do_diaas_overrides()` manages the `diaas_overrides` table: list, add/update, delete. Shows the current numa-calculated value before prompting for the override.

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

### `profile.py` — User profile and RDA

`UserProfile` dataclass: `age`, `sex` ("male"/"female"/"other"), `weight_kg`, `height_cm`, `activity_level`, `weight_unit` ("kg"/"lb"), `height_unit` ("cm"/"imperial"). The unit fields control display formatting only; internal calculations always use kg and cm.

`parse_weight(raw)` and `parse_height(raw)` accept free-form strings ("80 kg", "176 lbs", "178 cm", "5'10\"") and return `(value_in_base_unit, detected_unit)`.

`compute_rda(profile)` returns a dict mapping nutrient keys to `(rda_value, unit, rda_type)` tuples where `rda_type` is `"target"` or `"limit"`. Calorie target uses Mifflin-St Jeor × activity multiplier. Protein scales with weight and activity (0.8–1.2 g/kg). All other targets follow NIH/IOM Dietary Reference Intakes with sex-specific and age-adjusted values.

Profile is saved to and loaded from `~/.config/numa/profile.json`.

---

## Data Storage

| Location | Contents |
|---|---|
| `~/.local/share/numa/numa.db` | SQLite database (foods cache, recipes, meals, pantry, DIAAS overrides) |
| `~/.config/numa/config.json` | USDA API key |
| `~/.config/numa/theme` | Saved color theme preference |
| `~/.config/numa/prefs.json` | Dietary preferences (include_animal_foods flag) |
| `~/.config/numa/profile.json` | User profile (age, sex, weight, height, activity level) |

---

## Test Suite

The test suite has been rebuilt for the refactored `numa_app/` package structure. **316 tests**, all passing.

Run with: `pytest` (uses `pytest.ini` which sets `testpaths = tests` and `pythonpath = .`).

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

**Remaining Phase 2 items — Planned**

- Development of a slightly modified version that will run on Windows operating systems. (The developmental version is Linux-only.)
- Nutrient trend analysis over time (charts or tables)
- Meal planning and dietary pattern analysis
- Transition from a command line interface to graphic user interface.

### Phase 3 — Planned

- Barcode scanning for packaged foods
- Integration with smart kitchen devices
- API for third-party app integration
- Machine learning components for dietary recommendations
