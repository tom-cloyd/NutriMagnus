# NutriMagnus User Manual

*Updated 2026-04-29:1040*

[TOC]

## The problem that NutriMagnus (NM) addresses

Nutrition analysis programs, both paid and free open source, already exist but none that I've seen focus on the problems faced by vegetarian and vegan folks. And none have the readily modifiable design that I have wanted. So, with the development of NutriMagnus, both problems are addressed.

Plant-based proteins are far less ecologically damaging to produce than animal protein, and also much less likely to acquire agricultural chemical accumulations, which are then ingested along with the nutrients they contain. They also do not involve the industrialized abuse of vast numbers of animals who live only long enough to produce edible protein and then are treated like a mere object to be processed as we might a fallen tree. 

But, almost all plant proteins come to us with a built-in problem: inadequate protein analysis. 

There are 9 protein building blocks (amino acids) which human bodies cannot make and must therefore ingest. Additionally, they must be ingested in specific proportions. When a food, or meal, or diet lacks or is insufficient in one or more of these "essential" amino acids this has a limiting effect on the utilization of the other 8. This is the "incomplete protein" problem which almost all plant proteins present.

Consider someone building a brick wall. Suppose they order a bag of cement and 500 bricks. It is likely that they will run out of cement before they run out of bricks. This is the limitation problem that is inherent in plant-based diets. While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24-hour period, if the amino acid limitation problem is to be avoided. So, one way or another one needs to tend to the issue of what is missing and where are you to find it so you can add it to your diet in time.

The simple fact is that few people know which food have missing essential amino acids (EEAs), now which have the needed excess EAAs which would make them a good complement to eat in the same 24-hour period.

There are two other related dietary protein problems to be addressed:

* Protein in a food, however balanced or not, does no good if our bodies do not access it. Different protein sources in plant-based diets are metabolized in differing degrees of efficiency. This is **bioavailable protein** problem.

* Age, sex, and activity level differences in protein needs do exist and they are not minor. Older people and active people, for example, require substantially more protein than do younger people, for several reasons. Almost all common discussions of dietary protein fais to address this problem, and in any case a mere discussion doesn't tell one what to eat and how much.

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

## What a user can do with NutriMagnus - brief overview

(To be developed)

For more detailed information on what can be done with the program, look at 

## Understanding your food data

NutriMagnus gets food information from two large, well-maintained online databases:

- **USDA FoodData Central** — the U.S. government's nutrition database, covering hundreds of thousands of whole foods, ingredients, and branded products. This is NutriMagnus's primary source. (Visit [FoodData Central FAQ](https://fdc.nal.usda.gov/faq/) to learn more.)
- **Open Food Facts** — a community-maintained database of packaged and processed food products, useful for branded items not found in the USDA database. (Visit [Open Food Facts - Discover](https://world.openfoodfacts.org/discover) to learn more.)

When you search for and select a food, NutriMagnus saves a copy of that food's nutrient numbers on your computer. Future lookups are faster, and already-looked-up foods are available even without an internet connection. Think of this as your **personal food library** that grows as you use the program.

### Things you can add or change yourself

Three features let you build on the food library with your own information:

**My Pantry** keeps a short list of foods you currently have on hand — particularly protein sources. When NutriMagnus suggests foods to fill protein gaps in your diet, it checks your pantry first and puts those suggestions at the top of the list.

**Custom food profiles** let you enter nutrient information by hand — for a food not found in either database, or to enter values from a product label you trust. Custom profiles appear in search results alongside regular foods.

**Food annotations** let you attach a glycemic index (GI) estimate or a protein quality (DIAAS) estimate to any food already in the library, when you have that information from another source. The food's nutrient numbers stay unchanged; you are simply adding extra detail that NutriMagnus can then use in its calculations.

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

- **Richer nutrient information**: In addition to the standard macronutrients and micronutrients, NM tracks several plant bioactive compounds (carotenoids, choline, isoflavones, and others) where USDA data is available. Foods that contain substances known to reduce nutrient absorption are flagged with practical notes on how cooking or preparation reduces their effect.

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

## Output samples

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
     log meal · view/edit by date · analyze · delete
  4. Daily Summary
     today · by date · recent days
  5. Settings  (theme · user profile · dietary preferences · API key · DB path)
  q. Quit

  Ctrl+C at any prompt — cancel and go back

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

* **Enter food portions:** if at all possible, enter weights, not volume measures. A cup of flour can vary greatly depending upon how much air is stirred into it. A cup of spinach is even harder to pin down. Even nuts can be a problem. But weights are far less likely to vary, and so are much more reliable.

## The NutriMagnus help system

NutriMagnus displays a help footer at the bottom of tables and analysis
output whenever additional context is available. It looks like this:

> At any prompt, type `?diaas` or `?dcp` for help with these columns.

Type the indicated command at the next prompt and the relevant section of
this manual will be displayed inline. You can also type `?help` at any
prompt to see the full list of available topics.


### Using the "?{topic}" Help System [help]

At any prompt in NutriMagnus, type `?` followed by a topic name to display an
explanation. Wherever help is available, a line at the bottom of the table or
output lists the relevant topic names — for example, "Type `?diaas` or `?dcp`
for help with these columns." Type the corresponding `?topic` at the next
prompt to display the explanation.

Available topics:

  ?aa       Essential amino acids
  ?comp     Protein complement food suggestions
  ?complete What makes a protein "complete"
  ?dcp      Digestible Complete Protein
  ?diaas    Digestible Indispensable Amino Acid Score
  ?diet     Dietary preferences setting
  ?fao      FAO 2013 amino acid reference standard
  ?gap      Amino acid gaps and how they are scored
  ?gi       Glycemic index
  ?gl       Glycemic load
  ?rda      Recommended Dietary Allowances

Aliases also work: ?suggest, ?dietary, ?completeness, ?digestible, etc.

**Type ?help at any time to show this list again.**


### Essential Amino Acids [aa]

Amino acids are the building blocks of protein. Nine of them are "essential", for
our bodies cannot make them, so they must come from food every day:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine,
> Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and
Phenylalanine respectively. NutriMagnus evaluates Met+Cys and Phe+Tyr as
combined pairs when scoring protein quality, following FAO 2013 guidelines.

See [Protein Completeness](#protein-completeness-complete) and
[Amino Acid Gaps](#amino-acid-gaps-gap) for how completeness is scored and
what a gap means.


### Protein Complement Suggestions [comp]

When amino acid gaps are detected, NutriMagnus suggests foods that would
close those gaps with the smallest practical addition.

Suggestions come from two sources:

1. **Your pantry** — foods you have added under Foods → My pantry. These are always shown first.
2. **A built-in table** of about 30 common protein sources, filtered by your dietary preferences (see [Dietary Preferences](#dietary-preferences-diet)).

For each suggestion NutriMagnus shows:

- How many grams to add
- Which gaps it closes
- How much digestible protein it adds to the total

The calculation is based on FAO 2013 amino acid reference ratios. You do
not need to eat complement foods at the same meal — meeting daily totals
is sufficient for adults in normal health.


### Protein Completeness [complete]

A protein is "complete" when it supplies all nine essential amino acids at or
above the FAO 2013 reference amounts, adjusted for digestibility. Essential
amino acids cannot be made by the body — they must come from food.

Most animal proteins are complete. Most plant proteins are not, but combining
plant foods across a day can produce a complete profile — see
[Protein Complement Suggestions](#protein-complement-suggestions-comp).

The score shown in completeness tables is the ratio of each amino acid to the
FAO reference level. A score of **1.0 or above** for all nine means the protein
is complete. The most-limiting amino acid (the one with the lowest score) is
identified as the bottleneck.


### Digestible Complete Protein (DCP) [dcp]

DCP — digestible complete protein — is the grams of protein in a food or
meal that are both digestible (absorbed by the body) and complete (supply
all essential amino acids at or above reference levels).

It is more meaningful than raw grams of protein because it accounts for:

- **Digestibility:** how much protein is actually absorbed (from DIAAS)
- **Completeness:** whether the amino acid profile meets all requirements

A food with 30 g of protein but a DIAAS of 0.70 and several amino acid gaps
contributes less usable protein than those numbers suggest. DCP captures that.

NutriMagnus shows DCP in the bioavailability section of food and recipe
analysis. See also [DIAAS](#diaas--digestible-indispensable-amino-acid-score-diaas)
and [Protein Completeness](#protein-completeness-complete).


### DIAAS — Digestible Indispensable Amino Acid Score [diaas]

DIAAS measures how well your body can actually use the protein in a food.
A score of **1.0** means the protein fully meets the FAO 2013 amino acid
reference standard after accounting for digestibility. Scores above 1.0
are excellent; below 1.0 means one or more amino acids fall short.

Animal proteins typically score 1.0 or above. Most plant proteins score
below 1.0, though some (pea protein, soy) come close. Digestibility matters
because some protein in food is never absorbed — it passes through unchanged
or is broken down by gut bacteria rather than used by your body.

NutriMagnus uses DIAAS to calculate digestible complete protein (DCP), which
is a better indicator of actual protein quality than raw grams. See
[Digestible Complete Protein (DCP)](#digestible-complete-protein-dcp-dcp).


### Dietary Preferences [diet]

This setting controls which protein sources appear in complement suggestions.
Change it under **Settings → Dietary preferences** (option 3 in the Settings menu).

| Option | Setting | Includes |
|---|---|---|
| 1 | All animal foods | meat, fish, dairy, and eggs |
| 2 | Vegetarian | dairy and eggs only (no meat or fish) |
| 3 | Plant-based only | plant sources only |

The setting is saved between sessions and applies to both the interactive
complement display and any exported reports.


### FAO 2013 Reference Standard [fao]

The FAO (Food and Agriculture Organization of the United Nations) published
a reference amino acid scoring pattern in 2013 that defines the minimum
amounts of each essential amino acid per gram of protein needed to meet adult
human requirements.

NutriMagnus uses this pattern as the benchmark for all protein quality
scoring: completeness, gaps, and complement calculations. A score of **1.0**
for an amino acid means the food exactly meets the FAO reference for that
amino acid; above 1.0 exceeds it; below 1.0 falls short.

The FAO 2013 pattern replaced an older 1991 standard and is the current
international reference for protein quality assessment.


### Amino Acid Gaps [gap]

An amino acid gap means one or more essential amino acids are below the FAO
2013 reference level after digestibility adjustment. The gap is expressed as
a score: 0.70 means the food supplies 70% of what is needed for that amino
acid.

Gaps are sorted from most-limiting to least. A small gap (score 0.90–0.95)
is near-adequate and may not be worth correcting on its own. A large gap
(below 0.70) in a food that forms a major part of your diet is worth
addressing with a complement food.

- **Methionine** is the most commonly limiting amino acid in plant-based diets.
- **Lysine** is the most commonly limiting in grain-heavy diets.

See [Protein Complement Suggestions](#protein-complement-suggestions-comp) for
how NutriMagnus suggests foods to close gaps.


### Glycemic Index [gi]

The glycemic index (GI) measures how quickly a carbohydrate-containing food
raises blood glucose compared to pure glucose (GI = 100). Low-GI foods (55
or below) produce a slower, more gradual rise; high-GI foods (70 and above)
cause a faster spike.

GI is shown in the nutrient summary when data is available. It is most useful
for comparing foods within the same category — for example, choosing between
types of bread or rice. Keep in mind that GI describes a food eaten alone;
combining foods in a meal (especially adding fat, protein, or fiber)
physiologically blunts the blood glucose response to the carbohydrates present,
by slowing gastric emptying and glucose absorption. However, this effect is
not fully captured by glycemic load (GL) — see
[Glycemic Load](#glycemic-load-gl) for why.

NutriMagnus displays GI for reference only and does not use it in protein
quality calculations.


### Glycemic Load [gl]

Glycemic load (GL) improves on the glycemic index by accounting for both the
quality and the quantity of carbohydrate in a serving. The formula is:

```
GL = (GI × grams of available carbohydrate) / 100
```

For a meal combining multiple foods, the total GL is the sum of the GL
calculated separately for each component:

```
Meal GL = GL(food 1) + GL(food 2) + GL(food 3) + ...
```

Adding more carbohydrate-containing foods will always increase the meal total.
The reason combining foods physiologically blunts the blood glucose response —
as noted in the GI section — is not reflected in this calculation. Protein,
fat, and fiber slow gastric emptying and glucose absorption, reducing the
actual blood glucose rise; but because GL is calculated from fixed GI values
measured for each food in isolation, it has no way to represent that
interaction. GL is therefore a reliable tool for comparing meals of broadly
similar macronutrient composition, but becomes less accurate when meals differ
significantly in their fat or protein content.

A food can have a high GI but a low GL if the serving contains little actual
carbohydrate — watermelon is the classic example. Conversely, a moderate-GI
food eaten in a large portion can produce a high GL. For this reason GL is
generally a better guide to real-world blood glucose impact than GI alone.

**GL is interpreted on a per-meal or per-food basis:**

| GL Range | Classification |
|---|---|
| 10 or below | Low |
| 11–19 | Medium |
| 20 or above | High |

NutriMagnus displays GL in the nutrient summary alongside GI when carbohydrate
data is available. Like GI, it is shown for reference and does not affect
protein quality calculations.

For a discussion of how GL compares to other approaches for evaluating the
blood glucose impact of different meal choices — particularly relevant for
people managing diabetes — see [Appendix A: GL and Blood Glucose Comparison](#appendix-a-gl-and-blood-glucose-comparison).


### Recommended Dietary Allowances [rda]

RDA values in NutriMagnus come from the Dietary Reference Intakes (DRI)
published by the U.S. National Academies of Sciences. They represent the
average daily intake sufficient to meet the needs of most healthy adults
in a given age and sex group.

When you set a user profile (**Settings → User profile**), NutriMagnus uses
your age, sex, weight, height, and activity level to estimate personalized
targets. The calorie estimate uses the Mifflin-St Jeor equation with an
activity multiplier. The protein target uses 0.8 g per kg body weight as
a baseline minimum.

RDA values appear in the comparison table shown after nutrient analysis.


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

To research.

Resources:

* https://runningmagazine.ca/health-nutrition/could-you-be-timing-your-protein-all-wrong/

## Appendix D: Meal timing

To research.

Resources:

* https://www.theguardian.com/commentisfree/2026/may/05/game-changer-good-health-scientists-we-are-when-we-eat - article by expert