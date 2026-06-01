# NutriMagnus User Manual

*Updated 2026-05-31*:2345

[TOC]

## The problem that NutriMagnus (NM) addresses

Nutrition analysis programs, both paid and free open source, already exist but none that I've seen focus on the problems faced by vegetarian and vegan folks. And none have the readily modifiable design that I have wanted. So, with the development of NutriMagnus, both problems are addressed.

Plant-based proteins are far less ecologically damaging to produce than animal protein, and also much less likely to acquire agricultural chemical accumulations, which are then ingested along with the nutrients they contain. They also do not involve the industrialized abuse of vast numbers of animals who live only long enough to produce edible protein and then are treated like a mere object to be processed as we might a fallen tree. 

But, almost all plant proteins come to us with a built-in problem: inadequate protein analysis. 

There are 9 protein building blocks (amino acids) which human bodies cannot make and must therefore ingest. Additionally, they must be ingested in specific proportions. When a food, or meal, or diet lacks or is insufficient in one or more of these "essential" amino acids this has a limiting effect on the utilization of the other 8. This is the "incomplete protein" problem which almost all plant proteins present.

Consider someone building a brick wall. Suppose they order a bag of cement and 500 bricks. It is likely that they will run out of cement before they run out of bricks. This is the limitation problem that is inherent in plant-based diets. While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24-hour period, if the amino acid limitation problem is to be avoided. So, one way or another one needs to tend to the issue of what is missing and where are you to find it so you can add it to your diet in time.

The simple fact is that few people know which food have missing essential amino acids (EEAs), nor which have the needed excess EAAs which would make them a good complement to eat in the same 24-hour period.

There are two other related dietary protein problems to be addressed:

* Protein in a food, however balanced or not, does no good if our bodies do not access it. Different protein sources in plant-based diets are metabolized in differing degrees of efficiency. This is **bioavailable protein** problem.

* Age, sex, and activity level differences in protein needs do exist and they are not minor. Older people and active people, for example, require substantially more protein than do younger people, for several reasons. Almost all common discussions of dietary protein fais to address this problem, and in any case a mere discussion doesn't tell one what to eat and how much.

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

## What a user can do with NutriMagnus - brief overview

(To be developed)

For more detailed information on what can be done with the program, look at the [Output samples](#outputSamples) section.


## Output samples { #outputSamples}

(Incomplete and under development...)

### Launching the program from the command line => main menu displayed

![program launch - main menu](26-04-08-status-main-menu.png)

The main menu is simple. There are 5 main functions, each numbered. There are also several support functions, one of which simply ends the program. Below, I have selected function 2. I want to make sure the recipe I want to enter is not already partially entered. 

```
────────────────────────────────────────────────────────────────────────────────────────────────────
────────────────────────────────────────────────────────────────────────────────────────────────────
NutriMagnus ("nourishment wizard")
Nutritional Analysis for individuals and families - version 2026-04-29 - 11:30 AM

Color theme: dark  (auto-detected) -- change via Settings
Dietary preferences: plant-based only -- change via Settings
User profile: age 80, male, 158.0 lb  (71.7 kg), 5'9"  (175.3 cm), Very active (6–7 days/week)

NutriMagnus Menu
────────────────────────────────────────────────────────────────────────────────────────────────────
  1. Foods
     search · analyze · compare · annotate · manage pantry · custom profiles
  2. Recipes
     create · browse/manage · develop (add/remove ingredients with nutritional feedback)
  3. Meals & Log
     Shows up to 15 recent meals. Commands: n=new · v{id}=view/edit · a{id}=analyze
     d{id}=delete · s=search history · mr=next 15 older · d{YYYY-MM-DD}=jump to date
  4. Daily Summary
     today · by date · recent days
  5. Settings  (theme · user profile · dietary preferences · API key · DB path)
  q. Quit

  Ctrl+C at any prompt — cancel and go back
  ↑ / ↓  at any text prompt — scroll through your input history

Choice: 2

Recipes
────────────────────────────────────────────────────────────────────────────────────────────────────
  1. Create new recipe
  2. Browse / view, edit, copy, delete recipes
  3. Develop a recipe  (add/remove ingredients with nutritional feedback)
  m. Return to main menu
  q. Quit

Choice: 2

```

### Entering a recipe

**Main menu** function 2 brings up the **Recipes** menu, and again I enter 2, to get a list of the recipes NM knows about. 

Notice the options available in the **Recipes** menu: One can start a recipe and return to it later to edit it or even delete it. One can also copy it to have multiple versions. Item 3 on the menu is particularly interesting: One can develop a recipe, using nutritional feedback to make ingredient choices that achieve nutritional goals.

Now, looking at the displayed list of recipes, I see that the one I want to enter is already there, so I enter `v 5` (it could also have been `v5`) to look at recipe 5, which is then immediately displayed.

```
Recipes
────────────────────────────────────────────────────────────────────────────────────────────────────
  1. Create new recipe
  2. Browse / view, edit, copy, delete recipes
  3. Develop a recipe  (add/remove ingredients with nutritional feedback)
  m. Return to main menu
  q. Quit

Choice: 2

  RECIPES  Most recently accessed  (12 total)
   ID  Name                                Servings    DCP/srv  Complete  Created      
    5  Marinara pasta sauce ·············         7       0.0g     —      2026-04-10   
   15  Smoothie core - developmental 3 ··         1          —     ✓      2026-04-27   
   13  Smoothie core - developmental 2 ··         1      33.7g     —      2026-04-18   
   10  Refried beans, Tom's ·············         0          —     ✓      2026-04-14   
   12  Coffee 2 ·························         1       2.3g     —      2026-04-17   
    3  Smoothie core - developmental ····         1      35.4g     —      2026-04-03   
   11  coffee 1 ·························         1       9.1g     —      2026-04-17   
   14  Smoothie core - minimal ··········         1       8.9g     —      2026-04-18   
    8  Garbanzo bean broccoli soup ······        10      22.6g     —      2026-04-13   
    7  Okara whole wheat pasta ··········         1          —     —      2026-04-11   
    6  Mexican coffee - Tom's ···········         7          —     —      2026-04-10   
    4  Walnut milk ······················         5          —     —      2026-04-09   

  At any prompt, type ?help to see a list of available help topics.

  Actions: v=view  e=edit  x=develop  a=analyze  d=delete  c=copy  ·  s=search  b=done
  (Enter action + ID, e.g. v3 or x 14)
: v5

  Marinara pasta sauce  7 serving(s)  incomplete
  Serving size: 2/3 c · Volume: 4.7 c

  Ingredients:  (ID key: number = USDA FDC · OFF = Open Food Facts · usr = user-drafted)
  • 2 T (27 gr)  748608  Oil, olive, extra virgin
  • 175 g (1 c + 1 1/2 T)  170000  Onions, raw

  Procedure:
  Saute onions until they start to brown. Add tomato sauce, herbs and spices and stir in well while
  heating. Chop garlic and add along with rest of ingredients. Bring to simmer and cook 15 minutes.
────────────────────────────────────────────────────────────────────────────────────────────────────

  RECIPES  Most recently accessed  (12 total)
   ID  Name                                Servings    DCP/srv  Complete  Created      
    5  Marinara pasta sauce ·············         7       0.0g     —      2026-04-10   
   15  Smoothie core - developmental 3 ··         1          —     ✓      2026-04-27   
   13  Smoothie core - developmental 2 ··         1      33.7g     —      2026-04-18   
   10  Refried beans, Tom's ·············         0          —     ✓      2026-04-14   
   12  Coffee 2 ·························         1       2.3g     —      2026-04-17   
    3  Smoothie core - developmental ····         1      35.4g     —      2026-04-03   
   11  coffee 1 ·························         1       9.1g     —      2026-04-17   
   14  Smoothie core - minimal ··········         1       8.9g     —      2026-04-18   
    8  Garbanzo bean broccoli soup ······        10      22.6g     —      2026-04-13   
    7  Okara whole wheat pasta ··········         1          —     —      2026-04-11   
    6  Mexican coffee - Tom's ···········         7          —     —      2026-04-10   
    4  Walnut milk ······················         5          —     —      2026-04-09   

  At any prompt, type ?help to see a list of available help topics.

  Actions: v=view  e=edit  x=develop  a=analyze  d=delete  c=copy  ·  s=search  b=done
  (Enter action + ID, e.g. v3 or x 14)
: e5

```

The recipe is incomplete, and now I can work to complete it, by entering `e5`

In the output you will see a program 'bug' - The **Procedure** is not wrapped around to match the length of the other lines, and the line beneath it should be truncated. This is now fixed, but I leave the problem for you to see because the program is still at the beta stage, and such bugs are to be expected - especially in output formatting (which is a concern secondary to output content) is still being tuned up.

(Additional output samples are coming...)

## Usage tips

(under development)

* **Input history:** At any free-text prompt (food or recipe name, search term, amount, note, etc.) you can press the **up arrow** to recall what you typed previously. Press up again to go further back, and **down arrow** to move forward again. If you started typing before pressing up, your partial input is saved and restored when you press down back to the current position. History holds the last 100 entries for the session and resets when you quit.

* **Enter food portions:** if at all possible, enter weights, not volume measures. A cup of flour can vary greatly depending upon how much air is stirred into it. A cup of spinach is even harder to pin down. Even nuts can be a problem. But weights are far less likely to vary, and so are much more reliable.

## Food data — where it comes from and how it is stored

**Two large online tables** are NutriMagnus's primary sources of food information:

- **USDA FoodData Central** — the U.S. government's nutrition database, covering hundreds of thousands of whole foods, ingredients, and branded products. This is NutriMagnus's primary source. ([FoodData Central FAQ](https://fdc.nal.usda.gov/faq/))
- **Open Food Facts** — a community-maintained database of packaged and processed food products, especially useful for branded items not found in the USDA table. ([Open Food Facts](https://world.openfoodfacts.org/discover))

Every food in these online tables has a unique ID number — think of it as a product code that identifies that one food and nothing else.

**Your Food Cache** is a table stored on your own computer. When you search for a food, NutriMagnus checks your Food Cache first and shows any matches in a fast **Food cache** table before going online. Any food you have looked up before will be there and can be selected instantly, without a network call. If the food is not yet in your cache, the program searches both online tables and shows you a combined list of matches. When you select a food from that list, NutriMagnus saves a copy of its nutrient data in your Food Cache automatically. Over time, most of the foods you normally eat will be in your Food Cache for quick retrieval.

**Edit protection.** Any food you edit manually — through Foods → 6. Food Cache — is marked as user-modified. NutriMagnus will never silently overwrite a user-modified food with a fresh copy from USDA, even if you search for that food again later. Your edits, custom amino acid values, and notes are permanent unless you change or delete them yourself.

**Omega fatty acid tracking.** NutriMagnus tracks four individual omega fatty acids — ALA (plant-based omega-3, found in flaxseed, walnuts, chia), EPA and DHA (marine omega-3, found in fish and seafood), and linoleic acid (the main omega-6, found in vegetable oils and nuts). These appear in the nutrient table whenever USDA data is available. Foods already in your cache that predate this feature are updated automatically the first time you access them — no action needed on your part.

Food enters your Food Cache in four ways:

1. **From USDA** — you search, find a match, and select it. It is instantly saved into your Food Cache.
2. **From Open Food Facts** — same process; the food is saved the moment you pick it.
3. **By barcode** — at any food search prompt, type the 12-digit UPC-A or 13-digit EAN barcode printed on the product (digits only; spaces and hyphens are ignored). NutriMagnus looks the product up on Open Food Facts by barcode, shows you the product name and brand, and asks whether to use it. This is the fastest way to add packaged foods and dietary supplements — many have an Open Food Facts entry but no USDA record.
4. **By hand** — you create a custom food profile yourself, entering nutrient values from a product label or research source. These entries go straight into your Food Cache without coming from any online source.

In every case, NutriMagnus saves the food's original ID number alongside its data. That ID is the key that allows everything else in the program to refer back to a specific food unambiguously.

**Food Annotations** are a second table on your computer. They hold extra information you choose to add about a specific food — information that does not exist in either online table:

- **Glycemic index (GI)** — how quickly a food raises blood sugar (scale 0–100). Neither USDA nor Open Food Facts provides GI values, so if you have a figure from a research table or a product source, you can record it here.
- **DIAAS estimate** — a protein quality score (scale 0–1.5). NutriMagnus can calculate this automatically for whole foods that have complete amino acid data. For packaged foods where that data is absent, you can record a known DIAAS figure here instead.
- **A preparation note** — a short reminder such as "boiled 20 minutes" or "soaked overnight."

Each annotation is linked to one specific food in your Food Cache by that food's ID number. This means two things: you can only annotate a food that is already in your cache, and if you ever remove a food from your cache, its annotation is removed with it automatically.

**Your Recipes** are stored in their own table on your computer. Each recipe holds a list of ingredients, and each ingredient is linked to a specific entry in your Food Cache — by that food's ID. NutriMagnus handles this link automatically: when you add an ingredient to a recipe, it searches your cache and the online tables exactly as it would for any other food search, and caches the result if it isn't stored yet.

A recipe can also include another recipe as one of its ingredients, allowing you to build complex dishes from simpler prepared components. When you log a meal, you can add a portion of a recipe — or a portion of a recipe-within-a-recipe — exactly as you would add a single food.

**My Pantry** is a short personal list of protein sources you currently have on hand — tofu, lentils, Greek yogurt, and so on. It is a separate table used for one specific purpose: when NutriMagnus suggests foods to fill a protein gap in your diet, it checks your pantry first and moves those foods to the top of the suggestion list. This way the program recommends things you can actually use right now, rather than foods you would need to go and buy.

**How these lists relate — and where to edit.**

Your Food Cache, your Pantry, and your Custom Food Profiles (called "Drafted Food Profiles" in the program) are three different windows onto the same underlying data — not three separate stores.

Every food's nutrient data lives in exactly one place: the Food Cache. The Drafted Food Profiles list is simply a filtered view of your Food Cache showing only the foods you created or edited by hand. The Pantry is a short list of names that each point back to an entry in the Food Cache (when a USDA link exists).

This means: if you edit a food's nutrients in the Food Cache, that change is immediately reflected everywhere — in Drafted Food Profiles, in any recipe using that food, in pantry-based analyses, and in annotations. There is no syncing, no duplication, and no risk of one list getting out of step with another.

**To edit nutrient data for any food, always go to Foods → 6. Food Cache.** The Pantry and Drafted Food Profiles menus remind you of this and offer a shortcut key to jump there directly. Annotations (GI, DIAAS estimates) work the same way: annotate a food once in the Food Cache and the annotation appears everywhere that food is used.

## Entering custom foods and dietary supplements

### Custom (drafted) food profiles

When you need a food that is not in USDA or Open Food Facts — or when the database entry is incomplete — you can create a custom profile via **Foods → 7. Drafted Food Profiles → 2. Create**. The entry wizard walks you through:

- **Name** — what to call this food in searches and meal logs.
- **Supplement mode** (see below) or normal serving size and unit.
- **Basic macros** — calories, protein, total fat, carbohydrates, fiber, sugars, saturated fat, mono/poly fats, sodium. These are always prompted.
- **Minerals** (optional) — calcium, iron, magnesium, phosphorus, potassium, zinc.
- **Vitamins** (optional) — A, C, D, E, K, B1 (thiamin), B2 (riboflavin), B3 (niacin), B6, B9 (folate), B12. You can type values in IU for vitamins A, D, and E (e.g. `400 IU`) and the program converts them automatically.
- **Amino acids** (optional) — enter one-by-one or paste in a block from a research table (g per 100g protein — converted automatically).
- **Phytonutrients** (optional) — beta-carotene, lycopene, lutein, choline, and others.
- **Note** — document your source or any caveats about the data.

Once saved, the profile appears in all food searches, and can be used in meals and recipes exactly like any other food.

You can list, edit, or delete custom profiles from **Foods → 7. Drafted Food Profiles** at any time.

### Dietary supplements — tablets, capsules, softgels

Vitamins, minerals, and other supplement tablets are sold in per-tablet amounts, not per-100g amounts. NutriMagnus handles this with **supplement mode**: the program stores the per-tablet values internally in a way that means logging "1 tablet" in a meal contributes exactly the amounts on the label — no weighing required.

**How to create a supplement entry:**

1. Go to **Foods → 7. Drafted Food Profiles → 2. Create**.
2. Enter the product name (e.g. "Vitamin D3 2000 IU" or "Garden of Life Vitamin B12").
3. When asked "Is this a supplement?" — answer **y**.
4. Enter the unit name. For most tablets, just press Enter to accept the default (`tablet`). Other accepted values: `capsule`, `softgel`, `pill`, `scoop`.
5. Enter the nutrient values from the label. Enter them exactly as printed — e.g., if the label says "Vitamin B12: 5000 mcg", enter `5000` at the Vitamin B12 prompt.
6. For vitamins A, D, and E, the prompt accepts IU directly (e.g. `2000 IU`). The conversion is shown on screen.

When you later log "1 tablet" in a meal, those exact amounts are added to your nutrient totals.

**Tip:** Try a barcode search first (type the 12-digit number on the label at any search prompt). Many supplement products are already in Open Food Facts with complete nutrient data and require no manual entry.

**Converting an old entry to supplement mode:**

If you created a supplement entry before this feature was added, open it via **Foods → 7. Drafted Food Profiles → 3. Edit**. At the start of the edit session, the program asks "Is this a supplement?" — answer yes, confirm the unit name, and the existing nutrient values are preserved. The supplement portion is added automatically so the entry works correctly going forward.

## How NutriMagnus scores meal and recipe protein quality

Single-food analysis and meal-level analysis use different methods. For a single food, NutriMagnus computes a DIAAS score directly from that food's amino acid profile and digestibility. For a recipe or logged meal, it uses the FAO's endorsed method for mixed-food meals: it pools the digestible amino acids across all ingredients before scoring. The two approaches answer different questions and will give different results.

This section explains the meal-level method. For background on single-food DIAAS and how amino acid ratios work, see Appendix A.

### Why meals need their own calculation

A food that is short in one amino acid can be rescued by a companion food that supplies it generously — but only if you account for both foods together. A calculation that scores each food separately and then averages the scores misses this complementarity. The pooled method captures it correctly: amino acids from every ingredient in the meal are counted together before any ratio is computed.

### The method, step by step

NutriMagnus applies this procedure for each of the nine essential amino acids. For the paired amino acids Met+Cys and Phe+Tyr, both members of the pair are combined before scoring, following FAO practice.

**For each ingredient in the meal:**

Step 1. Determine the amino acid content in grams for the actual portion eaten. USDA data is per 100 g; NutriMagnus scales to the weight you entered.

Step 2. Multiply each amino acid amount by the food's true ileal digestibility coefficient — a number between 0 and 1 representing the fraction that actually reaches your bloodstream. The result is the digestible grams of that amino acid from this ingredient.

    Digestible AA (g) = raw AA in portion (g) × digestibility coefficient

Digestibility coefficients come from published literature and are looked up automatically. Eggs and dairy sit near 1.0; whole legumes are typically in the 0.79–0.85 range; most grains and seeds fall between 0.79 and 0.88.

**Then, across all ingredients:**

Step 3. Sum the digestible grams of each essential amino acid across every ingredient. This gives nine pooled totals — one per essential amino acid.

Step 4. For each amino acid, compute the ratio of the pooled digestible total to the FAO reference requirement for the total protein in the meal:

    Ratio = pooled digestible AA (g) ÷ (FAO reference value × total meal protein in g)

A ratio of 1.0 means the meal exactly meets the FAO target for that amino acid. A ratio of 0.80 means it supplies 80% of the target — a 20% shortfall.

Step 5. The lowest ratio across all nine essential amino acids is the meal's DIAAS score. The amino acid with that lowest ratio is the limiting amino acid.

### From DIAAS to digestible complete protein

    Digestible complete protein (g) = total meal protein (g) × min(DIAAS, 1.0)

If a meal contains 40 g of total protein and a DIAAS of 0.82, NutriMagnus reports 32.8 g of digestible complete protein. The remaining 7.2 g cannot be efficiently incorporated into tissue — the limiting amino acid is exhausted before the rest of the protein can be used.

### A worked example — two ingredients, two amino acids

To keep the arithmetic readable, only lysine and Met+Cys are shown. The full calculation runs the same steps for all nine essential amino acids.

**The meal:**

    150 g cooked lentils:    13.5 g protein    lysine 0.94 g    Met+Cys 0.25 g    digestibility 0.83
     50 g pumpkin seeds:     12.3 g protein    lysine 0.49 g    Met+Cys 0.42 g    digestibility 0.85

Lentils are rich in lysine but short in Met+Cys. Pumpkin seeds supply more Met+Cys. Together they cover each other's gap.

**Steps 1–2 — digestible AA per ingredient:**

    Lentils:        digestible lysine   = 0.94 × 0.83 = 0.780 g
                    digestible Met+Cys  = 0.25 × 0.83 = 0.208 g

    Pumpkin seeds:  digestible lysine   = 0.49 × 0.85 = 0.417 g
                    digestible Met+Cys  = 0.42 × 0.85 = 0.357 g

**Step 3 — pool across ingredients:**

    Pooled lysine   = 0.780 + 0.417 = 1.197 g
    Pooled Met+Cys  = 0.208 + 0.357 = 0.565 g

**Step 4 — compute ratios (total meal protein = 13.5 + 12.3 = 25.8 g):**

The FAO reference values are 48 mg of lysine and 23 mg of Met+Cys per gram of protein.

    FAO target for lysine   = 48 ÷ 1000 × 25.8 = 1.238 g
    FAO target for Met+Cys  = 23 ÷ 1000 × 25.8 = 0.593 g

    Ratio for lysine   = 1.197 ÷ 1.238 = 0.97
    Ratio for Met+Cys  = 0.565 ÷ 0.593 = 0.95

**Step 5 — DIAAS = lowest ratio:**

    DIAAS = 0.95    (Met+Cys is the limiting amino acid)

**Digestible complete protein:**

    25.8 g × 0.95 = 24.5 g digestible complete protein

Neither food alone would produce this result — lentils score poorly on Met+Cys when analyzed individually, but pumpkin seeds supply enough to bring the combined score to 0.95.

### A note about missing amino acid data

Not every food in the USDA database has a complete amino acid profile. When an ingredient is missing that data, NutriMagnus runs the meal-level DIAAS calculation using only the ingredients for which data exists, and flags the result as an estimate. The digestible complete protein figure is then computed against only the protein that comes from those data-complete ingredients — so the result remains meaningful rather than artificially inflated.

#### Filling missing AA profiles at analysis time

When a meal contains ingredients without amino acid data, NutriMagnus tells you how many are affected and distinguishes two situations:

- **Inside a recipe**: the ingredient is part of a recipe you logged as a meal item. Fix these by editing the recipe directly (Recipes → browse → edit ingredients) and replacing or re-fetching the ingredient there.
- **Standalone meal ingredients**: foods you logged directly to the meal (not inside a recipe). These can be replaced on the spot: NutriMagnus asks whether you want to search for a substitute.

If you say yes, for each affected ingredient the program opens a focused search of USDA SR Legacy and Foundation foods — the datasets most likely to include full amino acid profiles. The **AA** column in the results (✓ or ✗) shows at a glance which options have the data you need. Choosing a replacement updates that ingredient for the current analysis. Press Enter to skip an ingredient and leave it excluded from the calculation.

---

## Incremental approach to developing NutriMagnus

NM is being developed using Claude Code AI, in the VSCodium programming editor, which allows for rapid progress and excellent human/AI pairing.

Development is focusing at present on coding and validating core features in a command line environment. Progress to a graphic user interface (GUI) is planned, but will not occur until core features are in place. Command and menu-driven operation of NM will always be available after the GUI is working.

## Developmental Plan - functions developed and planned

### Phase 1 — Functions completed ✓

- Search the USDA food database and view detailed nutrient information for any food
- Analyze the nutritional content of a specific portion of a food
- Build and save recipes; view and analyze their nutritional content
- Log meals by date; view what you ate and analyze its nutritional content
- Daily nutrition summary
- Protein completeness analysis: see whether a food, recipe, or meal provides all nine essential amino acids in adequate proportions
- **Automated test suite** *(development tool)*: a set of automated checks that verify every key function of the program still works correctly after any code change. Running the tests after a change immediately reveals what, if anything, has broken — catching errors before they can reach users.

### Phase 2 — Features coded and in use; two items still planned

**Available now:**

- **Richer nutrient information**: In addition to the standard macronutrients and micronutrients, NM tracks several plant bioactive compounds (carotenoids, choline, isoflavones, and others) where USDA data is available. Four individual omega fatty acids are tracked separately — ALA (plant omega-3), EPA and DHA (marine omega-3), and linoleic acid (omega-6) — so you can see not just total polyunsaturated fat but the specific forms your body uses differently. Foods that contain substances known to reduce nutrient absorption are flagged with practical notes on how cooking or preparation reduces their effect.

- **Protein quality score (DIAAS)**: For any food or recipe, NM shows not just how much protein is present but how much your body can realistically use — adjusted for both digestibility and amino acid completeness. This matters especially on a plant-based diet, where raw protein figures routinely overstate what the body actually absorbs.

- **Protein complement suggestions**: After analyzing any food, recipe, meal, or daily summary, NM can suggest specific foods — drawing from your personal pantry list first — that would fill in your amino acid gaps. It calculates the minimum amount needed to close the gap, so you know exactly what to add to your meal.

- **My Pantry**: Keep a personal list of protein sources you currently have on hand. The complement advisor draws from this list first when making suggestions.

- **Meal-level protein quality**: When you analyze a full meal, NM computes a composite protein quality score across all the meal's ingredients combined, capturing how different foods complement each other.

- **Personalized nutrition targets**: Enter your age, sex, weight, height, and activity level, and NM computes calorie, protein, and micronutrient targets calibrated to you. After viewing a daily summary, you can compare your intake against these personal targets, with color-coded results for each nutrient.

- **Dietary preferences**: Tell NM which protein sources to include in complement suggestions — all animal foods (meat, fish, dairy, eggs) may be included, vegetarian (dairy and eggs only, no meat or fish), or plant-based only. The setting is saved between sessions and applies to both the on-screen display and any exported reports.

- **Recipe portion analysis**: Analyze the nutrients in a specific portion of any saved recipe — for example, how much protein and calcium you get from one serving of your chickpea stew.

- **Flexible portion entry**: Portions can be entered by weight (grams, ounces, pounds), or by volume (cups, tablespoons, teaspoons) for foods where a density is known.

- **Built-in help system**: NM includes a plain-language user manual you can consult without leaving the program. After any analysis that uses specialized terms — protein completeness, DIAAS, amino acid gaps, and others — a brief line at the bottom of the output lists the topics available. Type `?topic` at the next prompt to read the explanation. For example, `?diaas` explains the protein digestibility score, `?fao` explains the international reference standard used for protein quality assessment, and `?help` lists everything available. The explanation appears on screen and the prompt returns immediately afterward.

**Still planned for Phase 2:**

- Development of a slightly modified version that will run on Windows operating systems. (The developmental version is Linux-only.)
- Nutrient trend charts or tables: see how your intake of key nutrients has varied over days or weeks
- Dietary pattern analysis
- Transition to a graphical user interface (GUI); menu-driven operation will remain available

### Phase 3 — Possible further development

- Machine learning components for dietary recommendations

## The NutriMagnus help system

NutriMagnus displays a help footer at the bottom of tables and analysis
output whenever additional context is available. It looks like this:

> At any prompt, type `?diaas` or `?dcp` for help with these columns.

Type the indicated command at the next prompt and the relevant section of
this manual will be displayed inline. You can also type `?help` at any
prompt to see the full list of available topics.


### Using the "?{topic}" Help System [help]

At any prompt in NutriMagnus, type `?` followed by a topic name to display an explanation. Wherever help is available, a line at the bottom of the table or output lists the relevant topic names — for example, "Type `?diaas` or `?dcp` for help with these columns." Type the corresponding `?topic` at the next prompt to display the explanation.

Available topics:

  ?aa        Essential amino acids
  ?cached    Food Cache column guide
  ?comp      Protein complement food suggestions
  ?complete  What makes a protein "complete"
  ?dcp       Digestible Complete Protein
  ?diaas     Digestible Indispensable Amino Acid Score
  ?diet      Dietary preferences setting
  ?fao       FAO 2013 amino acid reference standard
  ?gap       Amino acid gaps and how they are scored
  ?gi        Glycemic index
  ?gl        Glycemic load
  ?glossary  Abbreviations and key terms
  ?goals     How daily nutrient goals are calculated
  ?rda       Recommended Dietary Allowances

Aliases also work: ?suggest, ?dietary, ?completeness, ?digestible, etc.

**Type ?help at any time to show this list again.**


### Food Cache — Column Guide [cached]

The CACHED FOODS list shows every food you have stored locally. Columns:

    #       Row number. Use with a command letter to act on that food
            (see Commands below).

    AA      Amino acid data status.
              ✓  Amino acid data is present in your cache for this food.
              ✗  No amino acid data — common for branded and packaged foods.

    GI      Your saved glycemic index estimate for this food, if any.
            GI reflects how quickly a food raises blood glucose (scale 0-100).
            Add or update via e# (Edit food data). Type ?gi for a full explanation.

    DIAAS   Your saved DIAAS estimate for this food, if any.
            DIAAS (Digestible Indispensable Amino Acid Score) rates protein
            quality: 1.00 = complete, lower = a limiting amino acid is present.
            Add or update via e# (Edit food data). Type ?diaas for details.

    C       Confidence / source note indicator.
              ✓  A source or confidence note is saved for this food.
              —  No note.
            View the full note with c# (see Commands below).

    N       Curator notes indicator.
              ✓  Curator notes are saved for this food (typically added by the
                 Claude data-fetch workflow).
              —  No curator notes.
            View with n# (see Commands below).

    ID#     Database identifier.
            A plain number = USDA FoodData Central FDC ID.
            "OFF"          = Open Food Facts (community-contributed data).
            "usr"          = User-drafted (created or edited by hand).

    NAME    Food name as stored in your cache.

    TYPE    Data source within USDA FoodData Central, or OFF for Open Food Facts.
              Foundation     — USDA-analyzed reference foods; highest accuracy.
              SR Legacy      — Standard Reference database (pre-2019).
              Survey (FNDDS) — Foods as eaten, used in national dietary surveys.
              Branded        — Manufacturer-submitted data for packaged products.
              OFF            — Open Food Facts (community-contributed).
              User Drafted   — Created or edited by hand in NutriMagnus.

    BRAND   Brand owner, for Branded and OFF foods.

Commands (type the letter followed by the row number, e.g. v3, e12):

    v#      View nutrients for that food (per 100g).
    n#      Combined view — nutrients + protein completeness + all notes
            (confidence note and curator notes). Use this when you want to
            see everything about a food in one screen.
    c#      View the confidence/source note only.
    a#      Analyze a portion — choose serving size, then see scaled nutrients.
    e#      Edit food data — name, serving, nutrients, note, GI/DIAAS annotation.
    d#      Delete from cache (also d#,# or d# # # for multiple rows).
    i#      Fetch missing data from Claude — generates a prompt you paste into
            claude.ai (free). Also i#,# for multiple rows. Type i alone to
            select every food in the current list that is missing AA data (✗).
    r       Read Claude's response — import the data saved in ~/claude_response.txt.
    /text   Filter list by name or brand. Enter / alone to clear the filter.
    Enter   Re-display the full food list (clears any in-progress filter view).

To refresh a corrupt or outdated cache entry: delete it with d#,
then search for the food again — it will be re-fetched automatically.

Type ?fetch for step-by-step instructions on the i/r fetch workflow.


### Fetching Missing Nutritional Data from Claude [fetch]

Some foods in your cache are missing amino acid data (shown as ✗ in the AA
column). You can fill this gap using Claude at claude.ai — no paid subscription
required. The workflow has four steps.

Step 1 — Generate the prompt.

    In the Food Cache list, type i followed by the row numbers of the foods
    you want data for:

        i30          (one food — row 30)
        i30,67       (two foods — rows 30 and 67)
        i            (all foods in the current list that show ✗)

    NutriMagnus writes a prompt to ~/claude_prompt.txt and tells you its
    full path. (`~` in that file pathname indicates that the file belong
    in the root of your computer's user account file system.)

Step 2 — Send the prompt to Claude.

    IMPORTANT: Start a brand-new chat at claude.ai for each request.
    Do NOT reuse a previous chat window. This ensures the copy step
    below captures only Claude's one response, nothing else.

    Open ~/claude_prompt.txt (any text editor) and copy its entire contents.
    Go to claude.ai in your browser (a free account is sufficient).
    Open a new chat, paste the text, and press Enter or click Send.

Step 3 — Save Claude's response.

    When Claude finishes responding, copy ONLY Claude's reply — not the
    whole page, not your original prompt. The safest method:

        a. Click at the very beginning of Claude's response text.
        b. Scroll to the absolute end of that response.
        c. Shift-click at the end to select everything Claude wrote.
        d. Copy (Ctrl+C or Cmd+C).

    Avoid using the copy button at the bottom of the chat window — that
    button copies the entire conversation history, not just Claude's reply.

    Open a plain-text editor (TextEdit, gedit, Notepad, etc.), paste, and
    save the file as:

        ~/claude_response.txt

    NutriMagnus handles both fenced (```json ...) and bare JSON formats.
    Any explanatory notes Claude adds after the data are saved automatically
    as curator notes (viewable with n# in the cache list).

Step 4 — Import the data.

    Return to NutriMagnus, go to Foods → Food Cache, and type r.
    NutriMagnus reads ~/claude_response.txt, shows you a review table
    (food name, calories, protein, and how many of the 11 amino acids
    were found), and asks for confirmation before writing anything.

    After a successful import the cache list refreshes automatically.
    Foods that gained amino acid data will change from ✗ to ✓.
    Note: some foods (e.g. FNDDS survey records) structurally lack amino
    acid data in their source database — for those, ✗ is correct even
    after a successful import of macros and minerals.

Notes:
- Per-food source and confidence notes are saved in the Confidence Note
  field (view with c#). Curator notes that apply to the whole batch are
  saved with every food in that import (view with n#).
- You can re-run the workflow at any time to update a food's data or add
  curator notes that were missed; the import safely overwrites the entry.
- To add curator notes to foods imported in a previous session: paste
  both the original JSON response and the notes text into
  ~/claude_response.txt and run r again — it is safe to re-import.
- If ~/claude_response.txt already exists from a prior session, overwrite
  it completely before saving a new response.


### Essential Amino Acids [aa]

Amino acids are the building blocks of protein. Nine of them are "essential", for our bodies cannot make them, so they must come from food every day:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and Phenylalanine respectively. NutriMagnus evaluates Met+Cys and Phe+Tyr as combined pairs when scoring protein quality, following FAO 2013 guidelines.

See [Protein Completeness](#protein-completeness-complete) and [Amino Acid Gaps](#amino-acid-gaps-gap) for how completeness is scored and what a gap means.


### Protein Complement Suggestions [comp]

When amino acid gaps are detected, NutriMagnus suggests foods that can improve the protein quality of the base food or meal. Two separate tiers are shown, and they use different methods:

TIER 1 — GAP CLOSERS

These foods can mathematically close a specific amino acid gap with a practical amount (up to 500 g). A gap closer has a high enough ratio of the limiting amino acid to protein that adding it to the base food brings that amino acid's score to 1.0 (the FAO reference floor).

Each suggestion shows:
  - Grams to add
  - Which gaps it closes, with scores before and after
  - Digestible protein added
  - Total bioavailable complete protein — the base food protein plus the complement protein, multiplied by the combined (pooled) DIAAS of the pair. This is higher than just adding each food's individually-digestible protein, because the complement's amino acids improve the usability of the base food's protein too.

TIER 2 — DIAAS-BOOSTING OPTIONS

Sometimes the digestibility of the base food is low enough that no practical amount of any single food can "close the gap" mathematically. This happens when the food's raw amino acid ratios are already near the FAO reference — the gaps are digestibility-driven rather than composition-driven. Adding even a very good complement raises the pool's digestible amino acids but can't fully overcome the base food's own digestibility penalty via the gap-closer formula.

For those situations, DIAAS-boosting options are shown instead. These foods raise the combined meal DIAAS score toward 0.90 by contributing digestible amino acids that pool with the base food's amino acids. The calculation uses each food's own true ileal digestibility (not just the DIAAS score), so a high-digestibility food like soy protein isolate (95%) contributes disproportionately more digestible amino acids than its raw content alone would suggest.

Each DIAAS-boosting suggestion shows:
  - Grams to add
  - Meal DIAAS before and after adding that amount

WHICH TIER IS RIGHT FOR YOU?

If gap closers are available, they are the most targeted choice: they fix a specific deficiency and fully complete the amino acid profile.

If only DIAAS-boosting options are shown, the underlying problem is that the base food is not highly digestible. Adding a well-digested, amino-acid-rich food improves the overall protein quality of the meal even without closing any single gap definitively. This is nutritionally meaningful — a meal DIAAS of 0.90 means 90% of the protein is both complete and digestible.

You do not need to eat complement foods at the same meal — meeting daily totals is sufficient for healthy adults. See also ?diaas and ?gap for background.

Data sources: your pantry (Foods → My Pantry) is checked first; a built-in table of about 30 common protein sources is used otherwise, filtered by your dietary preferences (see ?diet).


### Protein Completeness [complete]

A protein is "complete" when it supplies all nine essential amino acids at or above the FAO 2013 reference amounts, adjusted for digestibility. Essential amino acids cannot be made by the body — they must come from food.

Most animal proteins are complete. Most plant proteins are not, but combining plant foods across a day can produce a complete profile — see [Protein Complement Suggestions](#protein-complement-suggestions-comp).

The score shown in completeness tables is the ratio of each amino acid to the FAO reference level. A score of **1.0 or above** for all nine means the protein is complete. The most-limiting amino acid (the one with the lowest score) is identified as the bottleneck.


### Digestible Complete Protein (DCP) [dcp]

DCP — digestible complete protein — is the grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (supply all essential amino acids at or above reference levels).

It is more meaningful than raw grams of protein because it accounts for:

- **Digestibility:** how much protein is actually absorbed (from DIAAS)
- **Completeness:** whether the amino acid profile meets all requirements

A food with 30 g of protein but a DIAAS of 0.70 and several amino acid gaps contributes less usable protein than those numbers suggest. DCP captures that.

NutriMagnus shows DCP in the bioavailability section of food and recipe analysis. See also [DIAAS](#diaas--digestible-indispensable-amino-acid-score-diaas) and [Protein Completeness](#protein-completeness-complete).


### DIAAS — Digestible Indispensable Amino Acid Score [diaas]

DIAAS measures how well your body can actually use the protein in a food. A score of **1.0** means the protein fully meets the FAO 2013 amino acid reference standard after accounting for digestibility. Scores above 1.0 are excellent; below 1.0 means one or more amino acids fall short.

Animal proteins typically score 1.0 or above. Most plant proteins score below 1.0, though some (pea protein, soy) come close. Digestibility matters because some protein in food is never absorbed — it passes through unchanged or is broken down by gut bacteria rather than used by your body.

NutriMagnus uses DIAAS to calculate digestible complete protein (DCP), which is a better indicator of actual protein quality than raw grams. See [Digestible Complete Protein (DCP)](#digestible-complete-protein-dcp-dcp).


### Dietary Preferences [diet]

This setting controls which protein sources appear in complement suggestions.
Change it under **Settings → Dietary preferences** (option 3 in the Settings menu).

| Option | Setting | Includes |
|---|---|---|
| 1 | All animal foods | meat, fish, dairy, and eggs |
| 2 | Vegetarian | dairy and eggs only (no meat or fish) |
| 3 | Plant-based only | plant sources only |

The setting is saved between sessions and applies to both the interactive complement display and any exported reports.


### FAO 2013 Reference Standard [fao]

The FAO (Food and Agriculture Organization of the United Nations) published a reference amino acid scoring pattern in 2013 that defines the minimum amounts of each essential amino acid per gram of protein needed to meet adult human requirements.

NutriMagnus uses this pattern as the benchmark for all protein quality scoring: completeness, gaps, and complement calculations. A score of **1.0** for an amino acid means the food exactly meets the FAO reference for that amino acid; above 1.0 exceeds it; below 1.0 falls short.

The FAO 2013 pattern replaced an older 1991 standard and is the current international reference for protein quality assessment.


### Amino Acid Gaps [gap]

An amino acid gap means one or more essential amino acids are below the FAO 2013 reference level after digestibility adjustment. The gap is expressed as a score: 0.70 means the food supplies 70% of what is needed for that amino acid.

Gaps are sorted from most-limiting to least. A small gap (score 0.90–0.95) is near-adequate and may not be worth correcting on its own. A large gap (below 0.70) in a food that forms a major part of your diet is worth addressing with a complement food.

- **Methionine** is the most commonly limiting amino acid in plant-based diets.
- **Lysine** is the most commonly limiting in grain-heavy diets.

See [Protein Complement Suggestions](#protein-complement-suggestions-comp) for how NutriMagnus suggests foods to close gaps.


### Glycemic Index [gi]

The glycemic index (GI) measures how quickly a carbohydrate-containing food raises blood glucose compared to pure glucose (GI = 100). Low-GI foods (55 or below) produce a slower, more gradual rise; high-GI foods (70 and above) cause a faster spike.

GI is shown in the nutrient summary when data is available. It is most useful for comparing foods within the same category — for example, choosing between types of bread or rice. Keep in mind that GI describes a food eaten alone; combining foods in a meal (especially adding fat, protein, or fiber) physiologically blunts the blood glucose response to the carbohydrates present, by slowing gastric emptying and glucose absorption. However, this effect is not fully captured by glycemic load (GL) — see [Glycemic Load](#glycemic-load-gl) for why.

NutriMagnus displays GI for reference only and does not use it in protein quality calculations.


### Glycemic Load [gl]

Glycemic load (GL) improves on the glycemic index by accounting for both the quality and the quantity of carbohydrate in a serving. The formula is:

```
GL = (GI × grams of available carbohydrate) / 100
```

For a meal combining multiple foods, the total GL is the sum of the GL calculated separately for each component:

```
Meal GL = GL(food 1) + GL(food 2) + GL(food 3) + ...
```

Adding more carbohydrate-containing foods will always increase the meal total. The reason combining foods physiologically blunts the blood glucose response — as noted in the GI section — is not reflected in this calculation. Protein, fat, and fiber slow gastric emptying and glucose absorption, reducing the actual blood glucose rise; but because GL is calculated from fixed GI values measured for each food in isolation, it has no way to represent that interaction. GL is therefore a reliable tool for comparing meals of broadly similar macronutrient composition, but becomes less accurate when meals differ significantly in their fat or protein content.

A food can have a high GI but a low GL if the serving contains little actual carbohydrate — watermelon is the classic example. Conversely, a moderate-GI food eaten in a large portion can produce a high GL. For this reason GL is generally a better guide to real-world blood glucose impact than GI alone.

**GL is interpreted on a per-meal or per-food basis:**

| GL Range | Classification |
|---|---|
| 10 or below | Low |
| 11–19 | Medium |
| 20 or above | High |

NutriMagnus displays GL in the nutrient summary alongside GI when carbohydrate data is available. Like GI, it is shown for reference and does not affect protein quality calculations.

For a discussion of how GL compares to other approaches for evaluating the blood glucose impact of different meal choices — particularly relevant for people managing diabetes — see [Appendix A: GL and Blood Glucose Comparison](#appendix-a-gl-and-blood-glucose-comparison).


### Recommended Dietary Allowances [rda]

RDA values in NutriMagnus come from the Dietary Reference Intakes (DRI) published by the U.S. National Academies of Sciences. They represent the average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group.

When you set a user profile (**Settings → User profile**), NutriMagnus uses your age, sex, weight, height, and activity level to estimate personalized targets. The calorie estimate uses the Mifflin-St Jeor equation with an activity multiplier. The protein target uses 0.8 g per kg body weight as a baseline minimum.

RDA values appear in the comparison table shown after nutrient analysis.


### Daily Nutrient Goals [goals]

NutriMagnus calculates personalized daily nutrient goals from your user profile (Settings → User profile). Each goal is one of three types:

    Minimum  — RDA or Adequate Intake (AI): the daily amount needed to
               meet the requirements of most healthy adults.
    Target   — an estimated ideal intake (currently applies to calories).
    Limit    — Tolerable Upper Intake Level: the maximum safe daily
               amount (currently applies to sodium only).

HOW EACH GOAL IS CALCULATED

Calories (target)
    Mifflin-St Jeor equation for Basal Metabolic Rate, multiplied by an
    activity factor based on your activity level setting:

        Sedentary (desk job, little exercise)           x 1.2
        Lightly active (light exercise 1-3 days/week)   x 1.375
        Moderately active (3-5 days/week)               x 1.55
        Active (hard exercise 6-7 days/week)            x 1.725
        Very active (physical job or twice-daily)       x 1.9

Protein (minimum)
    Scaled to body weight and activity level:

        Sedentary or lightly active   0.8 g per kg body weight
        Moderately active             1.0 g per kg body weight
        Active or very active         1.2 g per kg body weight

Carbohydrates (minimum)
    130 g/day — the brain's minimum glucose requirement (fixed for all).

Fiber (minimum)
    Age- and sex-dependent Adequate Intake:

        Men under 50: 38 g/day     Men 50+: 30 g/day
        Women under 50: 25 g/day   Women 50+: 21 g/day

Sodium (limit)
    2300 mg/day — standard Tolerable Upper Intake Level (fixed for all).

Minerals and vitamins
    All use age- and sex-specific values from the Dietary Reference
    Intakes published by the U.S. National Academies of Sciences.
    Values vary by age group and sex; the most common adjustments are
    calcium (increases after age 50-70), iron (higher for premenopausal
    women), vitamin D (increases at age 70), and B6 (increases after 50).

Nutrients without established DRIs (phytonutrients, amino acids) have no
goal shown. The "% today" column and "Daily goal" column are blank for
those rows.

Type ?rda for a general overview of where these values come from.


## Glossary [glossary]

Abbreviations and key terms used in NutriMagnus output and this manual.

---

**AA**  —  Amino acid. The molecular building blocks of all proteins. See ?aa.

**AI**  —  Adequate Intake. A nutrient reference value used when a full RDA cannot be established; considered sufficient for most healthy people. Used for fiber in NutriMagnus. See ?rda.

**Bioavailable protein**  —  Protein the body can actually absorb and use, accounting for both digestibility and amino acid completeness. More meaningful than the raw protein figure on a nutrition label.

**CGM**  —  Continuous Glucose Monitoring. A wearable device that measures blood glucose every few minutes. Discussed in Appendix B as the most accurate way to track individual glycemic response.

**CLI**  —  Command-Line Interface. A text-based program you operate by typing commands and reading text output. NutriMagnus currently runs as a CLI; a graphical interface (GUI) is planned for a future phase.

**Complete protein**  —  A protein source that supplies all nine essential amino acids at or above FAO reference levels after digestibility adjustment. See ?complete.

**Complement food**  —  A food added to a meal specifically to supply the amino acids that other ingredients are short in. See ?comp.

**DCP**  —  Digestible Complete Protein. Grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (all essential amino acids present at adequate levels). See ?dcp.

**DIAAS**  —  Digestible Indispensable Amino Acid Score. A score from 0 to 1.5+ measuring how much of a food's protein the body can actually use, accounting for digestibility and amino acid completeness. 1.0 = meets the FAO reference exactly; above 1.0 = excellent; below 1.0 = one or more amino acids are limiting. See ?diaas.

**Digestibility coefficient**  —  A number between 0 and 1 representing the fraction of a nutrient that reaches the bloodstream after digestion. NutriMagnus uses true ileal digestibility values from published literature. Eggs and dairy sit near 1.0; whole legumes are typically 0.79–0.85.

**DRI**  —  Dietary Reference Intakes. The system of nutritional reference values published by the U.S. National Academies of Sciences; the source for RDAs, AIs, and upper intake levels used in NutriMagnus.

**EAA**  —  Essential Amino Acid. One of nine amino acids the human body cannot make and must get from food every day: Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine. See ?aa.

**FAO**  —  Food and Agriculture Organization of the United Nations. The body that published the 2013 amino acid reference standard used for all protein quality scoring in NutriMagnus. See ?fao.

**FDC**  —  FoodData Central. The USDA's online nutrition database and NutriMagnus's primary food data source. Each food has a unique numeric FDC ID. Website: https://fdc.nal.usda.gov/

**FDC ID**  —  The unique numeric identifier assigned to each food entry in USDA FoodData Central. You can enter an FDC ID directly at any "Search food or recipe" prompt instead of typing a name.

**Food Cache**  —  Your local database of previously retrieved foods. Searching the cache is instant (no network required); foods are added automatically when you select them from USDA or Open Food Facts results.

**Food Annotation**  —  Extra information you attach to a cached food: glycemic index, a DIAAS estimate, or a preparation note. Stored locally; not part of any online database.

**GI**  —  Glycemic Index. A scale from 0 to 100 measuring how quickly a food raises blood glucose relative to pure glucose (100). See ?gi.

**GL**  —  Glycemic Load. A measure of glycemic impact that combines GI with the actual amount of carbohydrate in a serving. More useful than GI alone for real-world meal comparisons. See ?gl.

**GUI**  —  Graphical User Interface. A visual, point-and-click interface. Planned for a future phase of NutriMagnus; the CLI will remain available.

**Ileal digestibility**  —  The fraction of an amino acid absorbed by the end of the small intestine (ileum). DIAAS uses true ileal digestibility, which is more accurate than fecal digestibility for measuring protein available to the body.

**Limiting amino acid**  —  The essential amino acid in shortest supply relative to the FAO reference, which caps how much of a food's protein can be incorporated into tissue. The overall DIAAS score equals the ratio for the limiting amino acid. See ?gap.

**Met+Cys**  —  Methionine + Cystine. These two amino acids are scored as a combined pair in DIAAS calculations, following FAO 2013 guidelines, because the body can convert Methionine into Cystine.

**My Pantry**  —  A personal list of protein sources you currently have on hand. NutriMagnus checks this list first when suggesting complement foods, so suggestions reflect what you can actually use.

**NM**  —  NutriMagnus. The abbreviated name used throughout this manual.

**OFF**  —  Open Food Facts. A community-maintained database of packaged and branded food products; NutriMagnus's secondary data source. Website: https://world.openfoodfacts.org/

**Phe+Tyr**  —  Phenylalanine + Tyrosine. Scored as a combined pair in DIAAS calculations because the body can convert Phenylalanine into Tyrosine.

**Phytonutrients**  —  Plant-derived bioactive compounds tracked by NutriMagnus where USDA data exists: beta-carotene, alpha-carotene, lycopene, lutein/zeaxanthin, choline, beta-sitosterol, and isoflavones.

**Pooled DIAAS**  —  The meal-level protein quality score computed by summing digestible amino acids across all ingredients before scoring. This captures how foods complement each other in a way that single-food DIAAS cannot. See the section "How NutriMagnus scores meal and recipe protein quality."

**RDA**  —  Recommended Dietary Allowance. The average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group. See ?rda.

**SPI**  —  Soy Protein Isolate. A concentrated plant protein (95%+ protein by weight) with high digestibility (0.95); frequently cited in complement suggestions. See Appendix E.

**TID** —  

**USDA**  —  United States Department of Agriculture. The U.S. government body that publishes FoodData Central, NutriMagnus's primary food data source.

**usr**  —  User-drafted. Appears in ingredient ID columns to indicate a food whose nutrient profile you created or edited by hand, rather than one retrieved from USDA or Open Food Facts.


## Appendix A: Raw protein, protein quality, and protein digestibility

### The core problems with protein

When you eat protein, not all of it is equally useful to your body. The usefulness depends on three things: **how much** protein you eat, and **how well-matched** its amino acid composition is to human physiological needs, and **how digestible** it is. 

### The Nine Essential Amino Acids and their required relationship

Your body requires twenty amino acids to build proteins. Eleven of these it can synthesize from other raw materials. The remaining nine — the essential amino acids (EAAs) — must come from food. 

These nine must all be present simultaneously for protein synthesis to proceed. They must also be present in the right amount. If any one of them is insufficiently supplied, then to the degree that its amount is short the other cannot be used. The surplus of the other eight cannot be stored and is instead broken down for energy — a functional waste.

In summary, the *pattern* of EAAs in a food matters, not just the total protein quantity.

### The required EAA pattern, established by the FAO

The Food and Agriculture Organization (FAO) of the United Nations leads international efforts to defeat hunger, achieve food security for all, and make sure that people have regular access to enough high-quality food to lead active, healthy lives.

Research has established human requirements for each EAA independently, through controlled human trials. For each amino acid separately, researchers determined how much a healthy adult needs per day to maintain physiological function. From these studies came absolute daily requirement figures for each of the nine EAAs, expressed in milligrams per kilogram of body weight per day.

Separately, research has established how much total protein a healthy adult needs per day. By dividing each EAA's daily requirement by the total daily protein requirement, researchers produced a normalized figure: how many milligrams of each EAA a person needs per gram of protein consumed. These normalized figures are the **FAO reference values**.

From the reference values for each amino acid which were determined *independently* come the ratios between EAAs. The reference values' relationship are a byproduct of the separately established requirements — not the starting point.

### The FAO reference values tell you about the quality of protein in a food

The reference values allow a simple and powerful question to be asked about any food protein source:

> If I eat enough of this food to meet my total daily protein needs, will each essential amino acid also arrive in sufficient quantity?

If the answer is yes for all nine EAAs, the protein is high quality — no bottleneck will limit your body's ability to use it. If the answer is no for even one EAA, that amino acid becomes your limiting factor.

### How the Ratio Is Calculated in numa

For each essential amino acid, the ratio shown in numa's output is computed in two steps:

**Step 1 — convert AA amount to mg per gram of total protein:**

    (AA content in g per 100g food ÷ protein content in g per 100g food) × 1000

This expresses how many milligrams of that amino acid are present for every gram of total protein the food contains.

**Step 2 — divide by the FAO reference value:**

    mg AA per g protein ÷ FAO reference value (mg/g protein)

A ratio of 1.0 means the food hits the reference exactly. A ratio of 2.14 means it delivers more than twice the required amount. A ratio of 0.80 means it delivers only 80% of what is needed.

**Concrete example — cocoa (USDA #169594):**

    Cocoa Protein total:      19.6 g per 100g food
    Tryptophan AA in cocoa:   0.293 g per 100g food

    Step 1:  (0.293 / 19.6) × 1000  =  14.9 mg tryptophan per g protein
    Step 2:  14.9 / 7               =  2.14

The FAO reference value for tryptophan is 7 mg/g protein. Cocoa's protein delivers 14.9 mg/g — 2.14 times what is required.

Think for a moment: what if cocoa contained none of the needed EAAs? Then the protein it contained would be unusable, if it were your only protein source. It could only be broken down for energy - the fate of all unusable protein. And what if it contained all the needed EAAs, in the right amount - except one was totally missing? That one would make all the other unusable.

### Why Total Protein Is the Denominator

A reasonable question is why the ratio uses total protein (including non-essential amino acids) as its denominator rather than comparing EAA amounts in absolute terms.

Total protein is a normalizing device — **a common scale that makes the quality metric meaningful across foods with very different protein concentrations and very different serving sizes.**

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

The Digestible Indispensable Amino Acid Score (DIAAS) assesses the degree to which a food protein can actually be accessed puts this question into by our body. For each EAA, it calculates:

> (mg of that EAA actually absorbed per gram of food protein) ÷ (FAO reference value for that EAA)

The word "actually absorbed" is critical. Not all amino acids in a food survive digestion intact and cross into the bloodstream. DIAAS uses ileal digestibility — the fraction of each amino acid absorbed by the end of the small intestine — to correct for this. The result is a score based on what your body actually receives, not merely what was in the food.

A ratio of 1.0 means the food **delivers** exactly the required amount of that EAA (per gram of protein eaten). A ratio below 1.0 means a shortfall — that EAA is limiting. A ratio above 1.0 means a surplus above the floor. **The overall DIAAS score for the food is set by whichever EAA has the lowest ratio — the weakest link.**

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

Think of it like fuel efficiency: a car that gets 50 miles per gallon is efficient, but knowing that tells you nothing about whether one gallon is enough to reach your destination. Quality and quantity are separate questions answered separately.

### Summary

| Concept | What it answers |
|---|---|
| FAO reference values | How many mg of each EAA a human needs per gram of protein consumed |
| DIAAS ratio for one EAA | Does this food deliver enough of that EAA, accounting for digestibility? |
| Overall DIAAS score | What is the weakest link — the most limiting EAA in this food? |
| Ratio > 1.0 for all EAAs | Complete protein: no bottleneck, full usability of what you eat |
| Daily protein target | Separate calculation: how many grams of protein do you need total? |

The DIAAS table characterizes the quality of each gram. Hitting your daily protein target is about counting how many grams you eat.

## Appendix B: Glycemic load (GL) and Blood Glucose Comparison

Glycemic load is a useful approximation, but no single formula-derived figure
reliably predicts an individual's blood glucose response to a mixed meal. Three
reasons account for this:

- The fat and protein suppression effect varies by person, by degree of insulin resistance, and by the specific foods involved.
- GI values were measured in healthy subjects and may not translate directly to someone with diabetes or insulin resistance.
- Individual glucose responses to identical meals vary substantially, even in the same person on different days.

GL is therefore most reliable when comparing meals of broadly similar
composition — two different grain-based breakfasts, for example. When meals
differ significantly in fat or protein content, the calculated GL will
understate the difference in actual glycemic impact.

### Continuous Glucose Monitoring

The practical gold standard today is continuous glucose monitoring (CGM) —
devices such as the Dexterity G7 or Libre 3 that measure interstitial glucose
every few minutes. A person with diabetes can eat a meal, watch their glucose
curve in the accompanying app, and directly compare their own real response
across different meal choices over time. No formula approaches this for
accuracy in individual prediction.

### Predictive Apps

Some applications (January AI, Levels) go a step further, using machine
learning models trained on large CGM datasets to predict glucose response to a
described meal before it is eaten — effectively personalising the GI and GL
concepts. These predictions are probabilistic rather than exact, but they
represent the closest available alternative to direct measurement.

### Clinical Practice Without CGM

For clinical guidance without CGM, dietitians working with people with
diabetes typically use carbohydrate counting combined with qualitative
judgment about fat and protein content, rather than relying on GL as a
single summary figure. GL remains a reasonable guide for comparing meals
similar in structure, but should not be the deciding number when fat and
protein differ significantly between the options being considered.

## Appendix D: Protein ingestion timing

To be researched.

Resources:

* https://runningmagazine.ca/health-nutrition/could-you-be-timing-your-protein-all-wrong/

## Appendix D: Meal timing

To be researched.

Resources:

* https://www.theguardian.com/commentisfree/2026/may/05/game-changer-good-health-scientists-we-are-when-we-eat - article by expert

## Appendix E: Why some foods appear only in DIAAS-boosting suggestions [comp-appendix]

This appendix explains why certain nutritionally excellent protein sources —
soy protein isolate, nutritional yeast, pea protein — sometimes appear only
in the DIAAS-boosting tier and not as gap closers, even though they are
well-known complements to legumes.

DIGESTIBILITY-DRIVEN GAPS

When a legume such as pinto beans has a low DIAAS (e.g., 0.73), that low score
is often not caused by a weak amino acid profile. Pinto beans' raw Met+Cys
ratio is approximately 22 mg/g protein — right at the FAO reference of 22.
The gap emerges only because its true ileal digestibility is 0.80: the body
absorbs only 80% of the protein, which pulls every amino acid's effective
contribution below the reference threshold.

The gap-closer formula accounts for this by raising the target threshold:

    R = FAO_reference / base_digestibility
      = 22 mg/g / 0.73 = 30.1 mg/g (adjusted target)

A gap closer must have an amino acid/protein ratio above 30.1 mg/g to
mathematically close the Met+Cys gap. Most plant proteins are excluded:

    Soy protein isolate  Met+Cys  =  23.0 mg/g  (below 30.1) → excluded
    Nutritional yeast    Met+Cys  =  21.2 mg/g  (below 30.1) → excluded
    Sesame seeds         Met+Cys  =  49.7 mg/g  (above 30.1) → qualifies

This is mathematically correct: because pinto beans absorb poorly, you need
a complement with a disproportionately high amino acid ratio to overcome the
digestibility deficit in the gap-closer framework. Sesame qualifies; SPI and
nutritional yeast do not.

WHY DIAAS-BOOSTING STILL WORKS FOR SPI

The DIAAS-boosting formula takes a different view. Instead of asking "can this
food close the gap for pinto beans alone?", it asks: "what happens when I pool
the digestible amino acids from pinto beans and SPI together?"

    Pooled digestible Met+Cys = (pinto Met+Cys * 0.80) + (SPI Met+Cys/100 * X * 0.95)
    Denominator = pinto raw protein + SPI raw protein/100 * X

Because SPI has a much higher digestibility (0.95 vs. 0.80), its amino acids
contribute more efficiently per gram than pinto's own amino acids do. At
approximately 25-35 g of SPI added to 100 g of pinto beans, the pooled meal
DIAAS reaches 0.90 — a meaningful improvement from 0.73.

The reason SPI still can't be a gap closer is that its raw Met+Cys ratio
(23 mg/g) is below the inflated 30.1 mg/g threshold the gap-closer formula
requires. But in the pooled DIAAS calculation, where each food's digestibility
applies only to its own amino acids, SPI's superior digestibility (0.95 vs.
pinto's 0.80) is sufficient to lift the combined score above the target.

PRACTICAL INTERPRETATION

From a dietary standpoint both tiers are useful, but they mean different things:

Gap closers (sesame, Brazil nuts, hemp seeds):
  These close the specific amino acid deficiency. After adding them, the
  combined protein is mathematically complete per the gap-closer model.
  Required amounts are often small (8-30 g).

DIAAS boosters (soy protein isolate, nutritional yeast, egg, whey):
  These are high-quality proteins with excellent digestibility. They raise
  the effective quality of the whole meal by contributing highly digestible
  amino acids. A meal DIAAS of 0.90 means 90% of the meal's protein is both
  complete and bioavailable — a strong nutritional outcome even if the
  precise gap-closer criterion isn't met.

In practice, combining a gap closer (e.g., sesame tahini) with a DIAAS
booster (e.g., a small serving of Greek yogurt or egg) gives both a complete
amino acid profile and high overall digestibility — the best outcome for
protein quality from a high-legume meal.

THE REFERENCE VALUES

NutriMagnus uses two slightly different reference sets:

Gap-closer tier:  usda_api.AA_REFERENCE_MG_PER_G_PROTEIN
  Met+Cys = 22 mg/g, Lysine = 45 mg/g, Leucine = 59 mg/g

DIAAS-booster tier: diaas.FAO_REFERENCE (FAO 2013, Table 6)
  Met+Cys = 23 mg/g, Lysine = 48 mg/g, Leucine = 61 mg/g

The small differences (1-3 mg/g) reflect different published FAO tables used
at different points in the codebase. Both are within normal rounding variance
across FAO publications. The gap-closer tier's values are the older set;
the DIAAS-booster tier uses the authoritative FAO 2013 adult reference pattern.

