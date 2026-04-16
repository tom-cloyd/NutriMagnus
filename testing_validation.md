---
tags:
---

## (From Claude)
 
Tests and validation are orthogonal concerns. "Tests verify that code does what "you told it to do" — validation verifies that what you told it to do is *correct*."  

(Strict quotes from here on:)

Here's how I'd think about the validation problem in layers:

### Layer 1: Data Integrity (Your Foundation)

Before trusting any calculation, you need to trust the underlying nutritional data. The most direct approach is spot-checking your database values against authoritative primary sources:

- **USDA FoodData Central** (fdc.nal.usda.gov) — the canonical source for most nutrient values, queryable directly
- **FAO INFOODS** — the gold standard for amino acid composition data, especially relevant for DIAAS work
- **Published digestibility coefficients** — for DIAAS, these come from specific FAO 2013 report tables, and you should verify your ileal digestibility values match those tables exactly

Pick 8–10 foods that span your typical use cases and manually verify every amino acid value against these primary sources. Discrepancies here undermine everything downstream.

### Layer 2: Algorithm Verification Against Known-Answer Tests

The FAO 2013 report (*Dietary Protein Quality Evaluation in Human Nutrition*, FAO Food and Nutrition Paper 92) contains worked examples with known correct outputs. These are the ideal test cases — the authors of the methodology calculated them, so they constitute ground truth. Running numa against those inputs and comparing outputs is the most rigorous validation possible for DIAAS logic specifically.

For PDCAAS or general amino acid scoring, similar worked examples exist in older FAO/WHO literature.

### Layer 3: Cross-Tool Replication

Cronometer is the most practical cross-validation tool for this purpose. It has detailed amino acid data and shares data lineage with USDA sources. The workflow would be:

1. Define a specific meal with exact gram quantities in both numa and Cronometer
2. Compare raw nutrient totals first (before any scoring) — if these diverge, you have a data problem
3. Then compare scored outputs if Cronometer supports the metric you're computing

Cronometer doesn't do DIAAS scoring natively, so this works best for verifying the nutrient accumulation layer rather than the scoring layer. For scoring, the FAO worked examples are stronger.

### Layer 4: Manual End-to-End Calculations

You already identified this — and for DIAAS specifically, you have the background to do it. I'd recommend:

- Choose 2–3 meals of increasing complexity (single food → two foods → a realistic mixed meal)
- Work through the full calculation manually: per-food amino acid content → sum to meal level → identify reference protein → compute DIAAS per amino acid → identify limiting AA → score
- Compare every intermediate value, not just the final score

Intermediate value comparison is critical. A correct final score can be produced by two compensating errors. Matching at every step gives much stronger confidence.

### Layer 5: Regression Locking

Once you've validated specific inputs → outputs through the above methods, encode those as **golden file tests** — tests that don't just assert behavior but assert specific numeric outputs against human-verified expected values. These are more fragile than behavioral tests but far more valuable for catching silent drift in calculations.

### Practical Order of Operations

Given where you are, I'd suggest:

1. **Data spot-check first** — this is highest leverage and takes an afternoon
2. **FAO worked examples** — encode these as new test cases with known-correct expected values
3. **Cronometer cross-check** on nutrient totals for a few representative meals
4. **Manual end-to-end** on one simple and one complex meal
5. **Regression lock** the validated cases

The manual calculation work will also likely surface edge cases (zero values, trace amounts, missing data handling) that your test suite may not be covering yet.

## Menu tree smoke test

[x] = passed

```
Main Menu  ("Nutrimagnus Menu")
├── 1. Foods
│   ├── 1. Search food databases (USDA + Open Food Facts)
│   │       Search by name → results from USDA and Open Food Facts merged →
│   │       select food → display full nutrient breakdown (per 100g) + protein
│   │       completeness assessment. Optionally proceed to portion analysis.
│   ├── 2. Analyze a food portion  (USDA + Open Food Facts)
│   │       Search → select → enter portion size → display scaled nutrients
│   ├── 3. Analyze a saved recipe portion         ← added
│   │       List saved recipes → select by ID → enter portion (number of servings
│   │       or fraction) → display scaled nutrient totals + protein completeness
│   ├── 4. Convert a portion <==> weight
│   │       Search → select → enter volume or weight → display gram equivalent
│   │       (no nutritional analysis; useful for recipe measurement conversion)
│   ├── 5. View cached / saved foods
│   │       List all foods previously fetched and stored locally
│   ├── 6. My pantry  (protein sources on hand)
│   │       Manage a persistent list of protein foods currently in stock.
│   │       Add via USDA search (links full amino acid data) or by name only.
│   │       Remove entries by pantry ID. Stored in the local database.
│   └── 7. User-drafted food profiles  (custom nutrient profiles)
│           Create, edit, and delete hand-crafted nutrient profiles for foods
│           lacking adequate official data. Profiles live in the local food
│           cache and behave like any other food (portions, recipes, meals).
│           See "User-drafted food profiles" under Usage Guide.
│
├── 2. Recipes
│   ├── 1. [x] Create new recipe
│   │       Name → description → servings → total volume (optional) →
│   │       total weight (optional) → procedure (editor, optional) →
│   │       add ingredients (search + portion) → saved to local database
│   ├── 2. [x] List recipes
│   ├── 3. [x] View recipe
│   │       Lists recipes → user picks by ID → displays name, description,
│   │       servings, volume/weight (if set), ingredients with amounts and
│   │       notes, and procedure text. Returns to the Recipes menu automatically
│   │       (no keypress needed). No nutritional analysis.
│   ├── 4. [x] Edit recipe
│   │       Edit name/description/servings/total volume/total weight/procedure,
│   │       or add/edit/remove/reorder ingredients. Each ingredient has an
│   │       optional Note field. The ingredient table shows a Note column when
│   │       any notes are present. DCP is recomputed and saved on any ingredient
│   │       change. Any changes made before pressing b/q/Ctrl+C are always saved.
│   ├── 5. [x] Analyze recipe
│   │       Shows name, description, ingredient list with amounts (and notes if
│   │       any are set), then procedure — all before any DCP prompts so the
│   │       recipe is fully visible when making decisions about missing data.
│   │       Then: total nutrients + per-serving nutrients + digestible complete
│   │       protein (DCP, saved to DB) + optional bioavailability breakdown +
│   │       protein completeness. If any ingredient lacks weight or DIAAS data,
│   │       a numbered Options menu prompts to provide values, calculate anyway
│   │       (approximate, not saved), or skip. b/q always available.
│   └── 6. [x] Delete recipe
│
├── 3. Meals & Log
│   ├── 1. Log a meal  (add to today's or create new)
│   │       If meals already exist today, shows a numbered list and lets you
│   │       add items to one of them. Choose n=new to create a fresh meal
│   │       (date defaults to today; enter a different date to log retroactively).
│   │       Each food item prompts for an optional Note (e.g., brand, preparation).
│   │       Saved to local database with date.
│   ├── 2. View / edit a meal
│   │       Paginated list of recent meals (9 per page, most recent first).
│   │       Pick by meal ID; page forward/back with more/prev; or jump to a
│   │       specific date. The selected meal's items are shown, then an action
│   │       menu offers:
│   │         1. Add items — unified search: type any name and matching saved
│   │                recipes appear first (R1, R2 …) above USDA/OFF food results.
│   │                Pick R# to add a recipe by servings; pick # to add a food
│   │                by portion.
│   │         2. Edit an item — change food, amount, or note for a food item;
│   │                or change servings for a recipe item.
│   │         3. Delete an item — remove one item from the meal.
│   │         4. Delete this meal — confirm, then remove the whole meal.
│   │         5. Merge with meal(s) on same date — appears only when other meals
│   │                exist on the same date. Choose which IDs to merge (or 'all'),
│   │                name the new combined meal, and optionally delete the originals.
│   ├── 3. Analyze a meal
│   │       Select a meal from the paginated list. If multiple meals share the
│   │       same date, choose whether to analyze just that meal or all meals on
│   │       the date together → combined nutrient totals + meal-level DIAAS
│   │       analysis (digestibility-corrected, pooled across all ingredients)
│   │       + protein completeness + complement suggestions
│   └── 4. Delete a meal
│           Select from the paginated list; confirm before deleting.
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
    ├── 1. Color theme  (dark / light / neutral / auto)
    ├── 2. User profile  (age, sex, weight, height, activity level)
    ├── 3. Dietary preferences  (animal foods included / plant-based only)
    ├── 4. Editor command  (for opening export files)
    ├── 5. Display program settings at launch  (yes / no)
    └── 6. Advanced settings
        ├── 1. Protein digestibility overrides  (for meal-level DIAAS calculation)
        ├── 2. USDA API key
        └── 3. Storage location  (display only)
```