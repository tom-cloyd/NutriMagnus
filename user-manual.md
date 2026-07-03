# NutriMagnus User Manual

*Updated 2026-06-30:0930* / Reading 1 hour, 57 minutes

<!--  the following preface is (26-06-28) what appears on the WEB version home page, accessed in home.md. -->

## Preface

**NutriMagnus ("NuMa")** is an open-source program which provides specifics about essential nutritional qualities of food. Good food choices require this information. NuMa gives a very thorough analysis of nutrition, focusing particularly on protein because this is a problem for those eating primarily a plant-based diet.

**Eating is about persistence, and our connectedness makes both possible.** Modern science grew from careful observation, and this has led to the indisputable conclusion that all life exists in relation to other life and to the material universe. This connectedness allows us to persist for a time, because by ourselves we are not sufficient. We NEED what is outside us.

A key quality of the known world is change - impermanence, and this is especially true of life forms. We are constantly dying and being reborn, on many levels. As individuals, while we exist, most of the cells in our body persist for a shorter span than we do. During their lifespan they do their work using available materials. Eventually they must be replaced by new cells constructed again from available materials. 

From where do these materials come? Some are immediately available in the local environment of a cell, but the rest have to come from elsewhere, and ultimately that means from outside our bodies. For this reason we must eat.

Eating almost always involves making choices, and choice requires information. The two major problems with food choice are a) awareness of the choices to be made, and b) information about the options available for our choosing. Both of these problems are addressed in the general domain of nutrition science. NuMa takes up both problems, in detail.

**Both program and accompanying User Manual are ongoing projects.** They are modified frequently. Both are already quite sophisticated, but new versions will be made available quickly for those already using the program. However, the manual has not yet received a careful editorial review; it is an advanced first draft.

**User feedback is highly valued.** What many software users don't realize is that with programs in active development ANY feedback is appreciated and likely to be useful. User experience with the program is the best measure of program success or failure. So, please email all problems, thoughts, and ideas to [tomcloydmsma@gmail.com](mailto:tomcloydmsma@gmail.com). Put `NutriMagnus` in the subject line, please!

---

## Part 1 — Introduction to NutriMagnus, a tool for intelligent eating

---

### What a user can do with NutriMagnus — brief overview

The five items in the top navigation bar correspond to the five major things you can do with the program:

- **Foods** — Search the USDA and Open Food Facts databases; analyze the nutrients in a specific portion of any food or recipe; compare up to eight foods side-by-side; manage your personal Food Cache, Pantry, and custom food profiles; annotate foods with glycemic index and DIAAS estimates.
- **Recipes** — Create and save recipes with ingredients and instructions; browse, copy, and delete saved recipes; develop a recipe iteratively with nutritional feedback after each ingredient change; analyze a recipe portion for full nutrient data, protein quality, and complement suggestions.
- **Meals & Log** — Record what you eat by date; add foods and recipes to meals; analyze individual meals or the combined total for a full day; search your entire meal history for any food.
- **Daily Summary** — View combined nutrient totals for today or any past date; compare your intake against personalized RDA targets; list recent days with meals.
- **Settings** — Set your color theme, personal profile (age, sex, weight, height, activity level), dietary preferences, editor command, and advanced options including your USDA API key and protein digestibility overrides.

**Detailed how-to guides for each menu area follow later in this manual.** For output samples and screenshots, see the [Output samples](#outputSamples) section. If you prefer to learn by example before reading explanations, skip ahead to [Sample Workflows](#sample-workflows) at the end of this introduction — three annotated walkthroughs show the program in action from start to finish.

### NutriMagnus addresses a very specific problem

**Diet matters.** It is now well established that the crucial factors affecting physical and mental health are diet, sleep, exercise, social engagement, stress management, and avoidance of injurious and risky substances. Their relationships are complex and interacting. Relative to diet, research supports an emphasis on a "plant-predominant eating pattern". [^1] The fortunate thing about diet is that is something we act on immediately and effectively - but only if we have the information needed to make good choices.

**Plant-based diets are preferable.** There are multiple good reasons to focus on eating foods derived from plants rather than animals. Plant-based proteins are far less ecologically damaging to produce than animal protein and also much less likely to acquire agricultural chemical accumulations, which are then ingested along with the nutrients they contain. They also do not involve the industrialized abuse of vast numbers of animals who live only long enough to produce edible protein and then are treated like a mere object to be processed as we might a fallen tree. 

Plant proteins are usually more affordable and easier to ship and store for long periods. Most of the world, and most of humanity throughout human history, eats and has eaten a plant-predominant diet, so this is simply not a novel idea.

**Plant-based proteins require special management.** But almost all plant proteins come to us with a built-in problem: incomplete amino acid composition. When you read on your jar of peanut butter (an excellent protein source) that 2 tablespoons contain 7 grams of protein (a bit more than that in a large egg), what it doesn't tell you is that only a bit less than 4 grams is actually digestible by human bodies, and of that only a little over 2 grams is complete protein - the kind found in an egg or a piece of chicken meat, and the kind we need.

There are 9 protein building blocks (amino acids) that human bodies cannot make and must therefore ingest. Additionally, they must be ingested in specific proportions. When a food, or meal, or diet lacks or is insufficient in one or more of these "essential" amino acids this has a limiting effect on the utilization of the other 8. This is the "incomplete protein" problem that almost all plant proteins present.

Consider someone building a brick wall. Suppose they order a bag of cement and 500 bricks. It is likely that they will run out of cement before they run out of bricks. This is the limitation problem that is inherent in plant-based diets. While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24-hour period if the amino acid limitation problem is to be avoided. So, one way or another, one needs to tend to the issue of what is missing and where to find replacements to add it to one's diet in time.

**NutriMagnus handles gracefully the tricky problem of managing plant-based proteins.** Few people know which foods have missing essential amino acids (EAAs) or which have the needed excess EAAs which would make them a good complement to eat with other foods lacking enough of those EAAS in the same 24-hour period.

Beyond the problem of ingesting the right mix of amino acids, there are two other related dietary protein problems to be addressed:

* Protein in a food, however balanced or not, does no good if our bodies do not access it. Different protein sources in plant-based diets are metabolized in differing degrees of efficiency. This is the **bioavailable protein** problem.

* Age, sex, and activity level differences in protein needs do exist and they are not minor. Older people, active people, and those with chronic diseases, for example, require substantially more protein than do younger healthy people, for several reasons. Almost all common discussions of dietary protein fail to address this problem, and in any case a mere discussion doesn't tell one what to eat and how much.

### This protein-management problem is critical for older people and the chronically ill, and especially so for women

In very brief summary, as we age, we tend to lose muscle mass, utilize dietary protein less efficiently, and simply eat less. These factors compound to create a perfect storm of vulnerability to general ill-health and the often dire consequences of falls. And these issues affect women more than men. Put simply - getting enough of the right sort of protein matters far more than most people realize. A good diet is utterly necessary, but not by itself sufficient. It must be complemented with adequate resistance exercise.

There is very little discussion of the problem in the mass media. So, it is up to use as individuals to self-educate and then make carefully considered decisions about our diet. But this is almost impossible to do without serious technical help, as the nutritional factors involved go well beyond simple arithmetic or the naively simple view offered to us by the first major statements about plant protein complementarity in the very early '70s.

### NutriMagnus is the missing helper

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

Nutrition analysis programs, both paid and free open source, already exist but none that I've seen focus on the problems faced by vegetarian and vegan folks. And none have the rich features and readily modifiable design that I want. The NutriMagnus program addresses both problems in detail. It also suggests complementary foods that can be combined with a food or recipe or meal to create complete proteins in one's diet.

NutriMagnus has been under intense development and is still being developed. Over time, new users will expertience unanticipated needs and the program can be further developed to meet them. This is one reason why [reporting problems](#feedback) is so important - feedback drives program development.

Very recently, a Windows version of the program has been developed. It will soon be available for download and user trials. 

### Why you can trust NutriMagnus (NuMa)

**NuMa draws on multiple data sources, and tells you which ones it used.** Nutrient data comes primarily from USDA FoodData Central[^2] — one of the most comprehensive public nutrition databases in the world — with branded and international foods supplemented by Open Food Facts.[^3] Beyond those external sources, NuMa also draws on data you have built up yourself: foods saved to your Pantry, and recipes you have analyzed. For protein complement suggestions specifically, a built-in list of about 30 common protein sources fills in as a fallback when your own data doesn't cover a gap. Wherever the program makes a suggestion, it shows you which sources it consulted.

**NuMa has an extensive formal code test process.** As of this writing (2026-06-23), there are 359 formal tests that the program must pass after every significant change. The vast majority of these are "behavioral" tests which verify that menus, prompts, and control flow all still work as they should. A very small number are "computational validation tests" in which real-world data is fed into the program to make sure that the output matches known correct numbers.

**Appendix I has a fully worked out validation example.** You can do this yourself, if you like. Data are brought in from outside the program and run through the official correct computation process. Full source references are given. You can run the same computation in NuMa and compare the result.

**Problems may appear anyway.** As professional programmers will tell you, all programs have bugs. This is more likely for new ones than for those which have been around for years. This is why you should report any result you are getting which doesn't make sense to you. There is a small chance you've found a "bug", but a greater chance that the program simply needs to explain itself to you more clearly. Either problem will be fixed ASAP, and all fixes benefit everyone who uses the program.

**How to report suspected errors or problem with the program:** (to be developed)

---

### Sample Workflows {#sample-workflows}

**Three examples showing NutriMagnus in action, end to end.** Each workflow is self-contained. You do not need to read Part 2 (nutrition concepts) or Part 3 (reference) first — terms are briefly explained in place. The three examples are chosen to show progressively richer use of the program's data sources.

**Use this as a tutorial!** With NuMa open in your browser, work through any of the following workflows step by step, paying close attention to the step instructions and what appears on your screen. You will become familiar with the program quickly doing this.

**How to navigate:** NuMa has a navigation bar at the top of every page. **Foods** opens a dropdown menu with nine options. **Recipes**, **Meals & Log**, **Daily Summary**, and **Settings** are single-click links. Clicking the NutriMagnus logo at the far left always returns you to the home page.

---

#### Workflow 1 — Looking up a single food and finding its protein gaps

**What this shows:** how to search for a food, read its nutrient profile, and get automatic protein complement suggestions drawn from the built-in protein source list.

**Step 1 — Open the Foods menu.** Click **Foods** in the top navigation bar. A dropdown appears with nine numbered items.

**Step 2 — Search for a food.** Click **2. Analyze a food portion**. A search box appears. Type `brown rice cooked` and click **Search**. NuMa queries USDA FoodData Central and returns a ranked list of matches. Click the Foundation Foods entry — Foundation Foods have the most complete amino acid data.

**Step 3 — Choose a portion.** The food detail page opens. Near the top you will see a portion input field. Type `1 cup` (or select it from the named portions dropdown if it appears) and click **Recalculate nutrients**.

**Step 4 — Read the nutrient table.** The page now shows the full nutrient profile scaled to your chosen portion. Click the **Nutritional Analysis** section header to expand it — you will see macronutrients, minerals, vitamins, and amino acids.

**Step 5 — Read the protein quality section.** Click **Protein Quality** to expand it. NuMa shows a per-amino-acid score table. Brown rice is low in lysine — its lysine score will be well below 1.0 (the FAO reference floor). This is the limiting amino acid.

**Step 6 — Read the complement suggestions.** Click **Complement Suggestions** to expand it. Because a gap exists, NuMa shows foods that can close it. The header line tells you what was considered — for example:

    Considered: built-in list of ~30 common protein sources.

(If you have pantry items or analyzed recipes, they appear here too.) The suggestions are ranked by smallest amount needed. You might see, for example, that adding 45 g of lentils would close the lysine gap and bring the combined protein to a complete profile.

**What you learned:** NuMa can tell you not just what is in a food but what is missing — and exactly what to add to fix it.

---

#### Workflow 2 — Analyzing a meal with pantry items as complement candidates

**What this shows:** how recording your own protein sources in the Pantry makes complement suggestions personal and practical, drawing on foods you actually have.

**Step 1 — Add a food to your Pantry.** Click **Foods** in the navigation bar, then click **7. My Pantry**. On the Pantry page, type `hemp seeds` in the Food name field and click **Add to pantry**. NuMa searches for the food and saves it. This takes about thirty seconds.

**Step 2 — Create a meal.** Click **Meals & Log** in the navigation bar. Click **New meal** and give it a name (e.g., "Lunch today"). The meal page opens with a search box. Type `brown rice cooked`, click **Search**, then click the matching food and enter `1 cup` as the portion. Repeat with `black beans cooked` at `½ cup`. Both foods now appear in the meal's item list.

**Step 3 — View the meal's nutrition analysis.** Scroll down on the meal page. The **Nutritional Analysis**, **Protein Analysis (DIAAS)**, and **Complement Suggestions** sections are collapsed by default — click each header to expand it. NuMa aggregates the nutrients across both foods and shows a combined profile.

**Step 4 — Read the protein analysis section.** Rice and beans together improve each other's amino acid profile significantly — this is protein complementarity in action. The combined score will be higher than either food alone.

**Step 5 — Read the complement suggestions.** The header now reads something like:

    Considered: 1 pantry item, built-in list of ~30 common protein sources.

Hemp seeds — your pantry item — will appear in the suggestions if they qualify as a gap closer for this particular meal. Because the suggestion is drawn from your pantry, it reflects a food you actually have, not just a theoretical option.

**What you learned:** Building even a small pantry of protein sources you keep on hand transforms complement suggestions from generic advice into a practical shopping and cooking guide.

---

#### Workflow 3 — Using an analyzed recipe as a complement candidate

**What this shows:** how recipes you have analyzed become available as complement options for other foods and meals, so NuMa can suggest "add a serving of your lentil soup" rather than just "add lentils."

**Step 1 — Create and analyze a recipe.** Click **Recipes** in the navigation bar, then click **New recipe**. Give it a name such as "Lentil soup" and fill in the servings count. On the recipe edit page, add ingredients one at a time — for example, lentils (200 g), onion (80 g), garlic (10 g), and vegetable broth (500 g). Click **Save**. The recipe detail page opens; its **Nutritional Analysis** and **Complete Protein Analysis** sections are computed automatically. Click those section headers to expand them and see the full protein profile and DCP.

**Step 2 — Look up a food with protein gaps.** Click **Foods** in the navigation bar, then click **2. Analyze a food portion**. Search for `corn tortilla`. Click the result, then enter `46 g` (about 2 tortillas) in the portion field and click **Recalculate nutrients**. Expand **Protein Quality** — corn is low in lysine and tryptophan.

**Step 3 — Read the complement suggestions.** Expand the **Complement Suggestions** section. The header now reads something like:

    Considered: 1 analyzed recipe, built-in list of ~30 common protein sources.

Your lentil soup recipe appears as a candidate. NuMa shows how many grams of the recipe (and approximately how many servings) would close the gaps in the corn tortillas. The suggestion might read: "Add to food above: 180 g  (0.9 servings)."

**Step 4 — Note what changes as you build up data.** The more recipes you analyze and the more pantry items you add, the more the complement suggestions reflect your actual kitchen. A fully populated pantry and recipe collection will produce a header like:

    Considered: 6 pantry items, 4 analyzed recipes, built-in list of ~30 common protein sources.

**What you learned:** NuMa's suggestions become progressively more useful as you add your own data. The built-in list ensures you always get suggestions even on day one; your pantry and recipes make those suggestions yours.

---

## Part 2 — Core nutrition concepts

### Essential Amino Acids [aa]

Amino acids are the building blocks of protein. Nine of them are "essential", for our bodies cannot make them, so they must come from food every day:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and Phenylalanine respectively. NutriMagnus evaluates Met+Cys and Phe+Tyr as combined pairs when scoring protein quality, following FAO 2013 guidelines.

See [Protein Completeness](#complete) and [Amino Acid Gaps](#gap) for how completeness is scored and what a gap means.


### Protein Complement Suggestions [comp]

When amino acid gaps are detected, NutriMagnus suggests foods that can improve the protein quality of the base food or meal. Two separate tiers are shown, and they use different methods:

#### TIER 1 — GAP CLOSERS

These foods can mathematically close a specific amino acid gap with a practical amount (up to 500 g). A gap closer has a high enough ratio of the limiting amino acid to protein that adding it to the base food brings that amino acid's score to 1.0 (the FAO reference floor).

Each suggestion shows:
  - Grams to add
  - Which gaps it closes, with scores before and after
  - Digestible protein added
  - Total bioavailable complete protein — the base food protein plus the complement protein, multiplied by the combined (pooled) DIAAS of the pair. This is higher than just adding each food's individually-digestible protein, because the complement's amino acids improve the usability of the base food's protein too.

#### RANKING

Options are ranked by the smallest practical amount needed, with one refinement: an option that fully completes the amino acid profile is moved to the front — but only if its serving size is 50 g or less. An option requiring 90 g to achieve completeness will not outrank a 7 g option that merely closes the primary gap. This prevents a food with a barely-adequate amino acid ratio (just above the FAO reference) from dominating the list simply because adding large quantities of it eventually fixes every gap.

#### TIER 2 — DIAAS-BOOSTING OPTIONS

Sometimes the digestibility of the base food is low enough that no practical amount of any single food can "close the gap" mathematically. This happens when the food's raw amino acid ratios are already near the FAO reference — the gaps are digestibility-driven rather than composition-driven. Adding even a very good complement raises the pool's digestible amino acids but can't fully overcome the base food's own digestibility penalty via the gap-closer formula.

For those situations, DIAAS-boosting options are shown instead. These foods raise the combined meal DIAAS score toward 0.90 by contributing digestible amino acids that pool with the base food's amino acids. The calculation uses each food's own true ileal digestibility (not just the DIAAS score), so a high-digestibility food like soy protein isolate (95%) contributes disproportionately more digestible amino acids than its raw content alone would suggest.

Each DIAAS-boosting suggestion shows a progression of serving sizes — 15 g, 30 g, 60 g, and up to 120 g (roughly 1/2 cup) for meal, food, and daily-summary analyses. Each step shows the meal DIAAS before and after adding that amount, so you can choose a realistic portion rather than being given a single impractically large target. Recipe analysis uses larger steps (up to 300 g) because recipe quantities serve multiple people.

#### TIER 3 — TWO-FOOD COMBINATIONS

When a single food can close the primary gap but in doing so dilutes another borderline amino acid, a two-food combination is offered. The logic follows a gap-cascade:

  Food A closes the primary (most-limiting) gap. It may open a smaller secondary gap by diluting a borderline amino acid that was already close to the threshold.

  Food B is chosen specifically to close whatever gap Food A left behind, without opening further gaps.

Together the pair clears all amino acid gaps. Both the CLI and web output show the individual gram amounts for each food, the cumulative amino acid effects, and whether the combination achieves "closes all gaps" status.

Three combinations are shown initially. The app offers to show more if available.

Combinations are ranked by total weight (lighter is ranked first), with combinations that close all gaps ranked above those that do not.

#### WHICH TIER IS RIGHT FOR YOU?

If single-food gap closers (Tier 1) are available, they are the most targeted choice: they fix a specific deficiency with a single food.

If single-food options open a secondary gap, Tier 3 two-food combinations show how to close everything in one practical step.

If only DIAAS-boosting options are shown (Tier 2), the underlying problem is that the base food is not highly digestible. Adding a well-digested, amino-acid-rich food improves the overall protein quality of the meal even without closing any single gap definitively. This is nutritionally meaningful — a meal DIAAS of 0.90 means 90% of the protein is both complete and digestible.

You do not need to eat complement foods at the same meal — meeting daily totals is sufficient for healthy adults. See also [DIAAS](#diaas) and [limiting amino acid](#gap) for background.

Data sources: your pantry (Foods → My Pantry) and any recipes you have analyzed are checked first; a built-in list of about 30 common protein sources is also always consulted as a fallback, filtered by your dietary preferences (see [dietary preferences](#diet)). The suggestion header tells you exactly which sources were considered for that run.


### Two-step combinations [comb]

After the gap-closer and DIAAS-boosting sections, NutriMagnus offers to show two-step combinations. Each combination pairs one of the top gap-closers (Step 1) with the best DIAAS-booster for the resulting protein pool (Step 2).

Why two steps? A gap-closer fixes amino acid balance but may not raise digestibility. A DIAAS-booster raises digestibility but cannot close a specific amino acid gap on its own. Together they address both problems: Step 1 corrects the limiting amino acid; Step 2 raises the overall DIAAS of the now-balanced pool, increasing digestible complete protein (DCP) further.

Each combination shows:
  - Step 1: the gap-closer, its serving size, and the DCP gain from the base
  - Step 2: the smallest practical serving of the best booster for that pool, and the further DCP gain
  - Net DCP gain from base to end of Step 2

If no DIAAS-booster can improve on the post-Step-1 pool (because the gap-closer already raised the pool's digestibility above what any available booster can match), the program says so rather than showing a misleading suggestion.

See also [complement suggestions](#comp) for the full complement suggestion system.


### Protein Completeness [complete]

A protein is "complete" when it supplies all nine essential amino acids at or above the FAO 2013 reference amounts, adjusted for digestibility. Essential amino acids cannot be made by the body — they must come from food.

Most animal proteins are complete. Most plant proteins are not, but combining plant foods across a day can produce a complete profile — see [Protein Complement Suggestions](#comp).

The score shown in completeness tables is the ratio of each amino acid to the FAO reference level. A score of **1.0 or above** for all nine means the protein is complete. The most-limiting amino acid (the one with the lowest score) is identified as the bottleneck.


### Digestible Complete Protein (DCP) [dcp]

DCP — digestible complete protein — is the grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (supply all essential amino acids at or above reference levels).

It is more meaningful than raw grams of protein because it accounts for:

- **Digestibility:** how much protein is actually absorbed (from DIAAS)
- **Completeness:** whether the amino acid profile meets all requirements

A food with 30 g of protein but a DIAAS of 0.70 and several amino acid gaps contributes less usable protein than those numbers suggest. DCP captures that.

DCP is also called "bioavailable complete protein" or "usable protein" in nutrition literature — these terms mean the same thing. NutriMagnus uses DCP throughout.

NutriMagnus shows DCP in the bioavailability section of food and recipe analysis. See also [DIAAS](#diaas) and [Protein Completeness](#complete).


### DIAAS — Digestible Indispensable Amino Acid Score [diaas]

DIAAS measures how well your body can actually use the protein in a food. A score of **1.0** means the protein fully meets the FAO 2013 amino acid reference standard after accounting for digestibility. Scores above 1.0 are excellent; below 1.0 means one or more amino acids fall short.

Animal proteins typically score 1.0 or above. Most plant proteins score below 1.0, though some (pea protein, soy) come close. Digestibility matters because some protein in food is never absorbed — it passes through unchanged or is broken down by gut bacteria rather than used by your body.

A note on terminology: the FAO uses the term "indispensable amino acids" (IAA) where this manual uses "essential amino acids" (EAA) — both refer to the same nine amino acids. The "I" in DIAAS stands for "Indispensable."

NutriMagnus uses DIAAS to calculate digestible complete protein (DCP), which is a better indicator of actual protein quality than raw grams. See [Digestible Complete Protein (DCP)](#dcp).


### Limiting-Amino-Acid Scoring [aa-scoring]

Protein quality analysis involves two separate adjustments. The Protein Digestibility table shows the result after the first adjustment only. The phrase "before limiting-amino-acid scoring" on that table means the second adjustment has not yet been applied.

#### Step 1 — Digestibility adjustment (shown in the table)

    Digestible protein (g) = food protein (g) × digestibility coefficient

This accounts for how much protein actually reaches your bloodstream. A food with 20 g of protein and a digestibility of 0.85 delivers 17 g of digestible protein. This is what the "Digestible prot" column shows.

#### Step 2 — Limiting-amino-acid scoring (the DIAAS step)

    Digestible complete protein (g) = digestible protein (g) × min(DIAAS, 1.0)

Even if all the protein is absorbed, it cannot all be incorporated into tissue unless every essential amino acid is present in sufficient proportion. The amino acid in shortest supply — the limiting amino acid — sets a ceiling. DIAAS is the ratio of that limiting amino acid to the FAO reference level. If DIAAS is 0.80, only 80% of the digestible protein can be fully used; the rest is broken down and excreted.

The "Total digestible protein" line below the table is the sum after step 1 only. The DCP figure reported in the meal summary is the result after both steps.

Note: DIAAS itself is not capped — a high-quality food can score above 1.0, meaning it has surplus amino acids relative to the reference. The min(DIAAS, 1.0) applies only when computing DCP, because having excess amino acids does not allow you to absorb more total protein than you consumed.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [limiting amino acid](#gap), [DCP cap](#dcp-cap).


### Why DCP Is Sometimes Capped Below the DIAAS Projection [dcp-cap]

The short version: the DIAAS formula can project a Digestible Complete Protein value that
is mathematically higher than the protein your body actually absorbed. When that happens,
NutriMagnus caps DCP at the absorbed-protein ceiling, because you cannot use more protein
than you took in.

#### Why this happens

DIAAS is defined by the FAO as:

    DIAAS = (digestible supply of the limiting amino acid)
            divided by
            (FAO reference density for that amino acid × raw protein)

The numerator uses digestibility-corrected amino acids. The denominator uses raw (pre-
digestion) protein. This is intentional in the FAO standard. DCP is then:

    DCP = raw protein × DIAAS

Substituting the DIAAS definition, this simplifies to:

    DCP = digestible limiting-AA supply / FAO reference density for that AA

In plain words, DCP answers: "How many grams of a reference-quality protein would supply
the same amount of limiting amino acid as this meal provides?"

For a single food, DIAAS never exceeds that food's own digestibility, so DCP cannot exceed
absorbed protein. In a mixed meal, however, the limiting amino acid may be concentrated in
a high-digestibility ingredient while the bulk of the protein mass comes from lower-
digestibility ingredients. The DIAAS score then reflects the high-digestibility source,
but average protein absorption reflects the lower-digestibility majority. DIAAS ends up
higher than the weighted-average digestibility, and the DCP formula overshoots absorbed
protein. This is a known mathematical artifact of applying FAO DIAAS to mixed meals.

#### A worked example

Suppose a breakfast has two protein sources:

    Food                   Raw protein   Digestibility   Absorbed protein
    -------------------    -----------   -------------   ----------------
    Soy protein isolate    10 g          0.95            9.5 g
    Oatmeal                30 g          0.82            24.6 g
    -------------------    -----------   -------------   ----------------
    Total                  40 g          avg 0.854       34.1 g

Soy isolate is lysine-rich. Because lysine is the usual limiting amino acid in grain-heavy
meals, it strongly influences the DIAAS score. Suppose the pooled lysine supply (after
digestibility correction) yields:

    DIAAS = 0.91

Raw-formula DCP:

    DCP = 40 g × 0.91 = 36.4 g

But total absorbed protein is only 34.1 g. The cap is applied:

    DCP = min(36.4 g, 34.1 g) = 34.1 g

Why did DIAAS exceed average digestibility? The soy isolate (dig 0.95) provides most of
the lysine, so the lysine ratio in the DIAAS calculation reflects its high digestibility.
The larger oatmeal portion (dig 0.82) dominates the absorbed-protein total and pulls the
weighted average down to 0.854. DIAAS (0.91) ended up above that average, causing the
overshoot.

#### What the cap means in practice

A capped DCP is actually good news about amino acid quality. It means your limiting amino
acid is present in such good supply (relative to raw protein) that the formula projects
more complete protein than you could possibly absorb. The practical reading: all of your
absorbed protein is functioning as complete protein. You are not losing protein to an
amino acid shortfall.

Compare this to an uncapped DCP that is well below absorbed protein: the gap between them
represents protein you absorbed but cannot fully use for tissue synthesis because the
limiting amino acid ran out first. That is the more common and more concerning situation.

The average digestibility shown in the cap note is the weighted average of per-ingredient
digestibility coefficients, weighted by protein content. Each coefficient comes from the
curated lookup table or category estimate described in [meal protein digestibility](#meal-diaas).

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [amino acid scoring](#aa-scoring).


### FAO 2013 Reference Standard [fao]

The FAO (Food and Agriculture Organization of the United Nations) published a reference amino acid scoring pattern in 2013 that defines the minimum amounts of each essential amino acid per gram of protein needed to meet adult human requirements.

NutriMagnus uses this pattern as the benchmark for all protein quality scoring: completeness, gaps, and complement calculations. A score of **1.0** for an amino acid means the food exactly meets the FAO reference for that amino acid; above 1.0 exceeds it; below 1.0 falls short.

The FAO 2013 pattern replaced an older 1991 standard and is the current international reference for protein quality assessment.


### Amino Acid Gaps [gap]

An amino acid gap means one or more essential amino acids are below the FAO 2013 reference level after digestibility adjustment. The gap is expressed as a score: 0.70 means the food supplies 70% of what is needed for that amino acid.

Gaps are sorted from most-limiting to least:

    Score     Status                                    Complement suggestion?
    --------  ----------------------------------------  ----------------------
    >= 1.0    Meets FAO reference -- complete           No
    0.95-0.99 Near-adequate -- practical gap too small  No (NutriMagnus floor)
    0.70-0.94 Gap present                               Yes
    < 0.70    Significant gap -- high priority          Yes

NutriMagnus generates complement suggestions only for scores below 0.95, not below the FAO floor of 1.0. A gap of 0.98 would suggest "add 1 g" -- not useful. The 0.95 floor filters those out.

- **Methionine** is the most commonly limiting amino acid in plant-based diets.
- **Lysine** is the most commonly limiting in grain-heavy diets.

See [Protein Complement Suggestions](#comp) for how NutriMagnus suggests foods to close gaps.


### Antinutrients [antinutrients]

Most people have never encountered this term, yet antinutrients are present in virtually every plant food. Understanding them is especially important for anyone eating a plant-predominant diet, because the same foods that supply the most fiber, minerals, and phytonutrients are often the ones that contain the highest antinutrient loads.

#### What is an antinutrient?

The word sounds alarming, but it simply means a naturally occurring compound in a food that partially blocks the absorption or use of a nutrient your body would otherwise receive. The effect is not binary — it is a matter of degree, and it can usually be reduced or eliminated by how you prepare the food.

Plants produce these compounds as a natural defense: against insects, fungi, and animals that would eat them. They are not contaminants or the result of farming practices. They are intrinsic to the plant's biology.

#### The main antinutrients that appear in NutriMagnus output

**Phytates** (phytic acid). Found in legumes, whole grains, nuts, and seeds. Phytate binds tightly to minerals — especially iron, zinc, calcium, and magnesium — forming a complex the body cannot easily absorb. A meal of lentils or whole-wheat bread may contain all the iron the label shows, but much of it may pass through unabsorbed if phytate is high. The effect depends on the rest of the meal: vitamin C consumed at the same meal significantly counteracts phytate's effect on iron. Preparation methods that consistently reduce phytate: soaking legumes or grains overnight before cooking; sprouting; fermentation (sourdough bread reduces phytate by 50-90%; tempeh and other fermented soy products have low phytate).

**Oxalates**. Found at high levels in spinach, Swiss chard, beet greens, rhubarb, and almonds; at moderate levels in many other plant foods. Oxalates bind calcium in the gut, meaning the calcium shown on a food label for spinach is largely unavailable — absorption rates can be as low as 5%, versus 30% for dairy calcium. For most people this is simply a reason not to rely on spinach as a calcium source, not a reason to avoid it. For people prone to calcium-oxalate kidney stones, total dietary oxalate matters more directly. See [oxalate data](#oxalate) for the detailed data NutriMagnus tracks on this.

**Lectins** and **trypsin inhibitors**. Found in raw legumes (beans, lentils, chickpeas, soybeans). Lectins interfere with the gut lining; trypsin inhibitors block a key digestive enzyme. Raw kidney beans contain enough lectin to cause acute food poisoning. Cooking completely solves the problem: full boiling for at least 10 minutes destroys both lectins and trypsin inhibitors. Canned beans are already safe. Tofu and tempeh are also safe because both involve prolonged heat treatment or fermentation. This is the one antinutrient on this list that is not just about partial reduction — with raw legumes, proper cooking is required.

**Bound niacin** (in corn). Untreated corn contains niacin in a chemically bound form the human body cannot absorb. Populations who ate corn as a dietary staple without treatment historically developed pellagra (severe niacin deficiency). The traditional solution — practiced for thousands of years by Mesoamerican cultures and still used today — is nixtamalization: soaking dried corn in an alkaline lime solution. This releases the niacin and makes it fully bioavailable. Tortillas, masa, hominy, and grits made from nixtamalized corn are fine. Plain cornmeal (not nixtamalized) retains the problem.

#### How these appear in NutriMagnus output

When you view a food with known antinutrient concerns, a note appears in the Bioavailability section of the analysis. The note names the compound, describes the specific problem, and lists the preparation method(s) that reduce it.

#### Examples of what you may see

    Mineral absorption problem — phytates are present
    Best reduction: soak or sprout before cooking

    Mineral absorption problem — high oxalate reduces calcium uptake from this food specifically

    Mineral absorption problem — oxalate & phytate present
    Reduces both: roasting or soaking

    Digestibility problem — lectins & trypsin inhibitors
    Required: fully cook (boil) to inactivate

    Vitamin bioavailability problem — niacin is bound, not usable unless nixtamalized
    Nixtamalized forms are fine: tortilla, masa, hominy

These notes appear only for foods where NutriMagnus has a curated flag — the list is not exhaustive, and absence of a note does not mean a food is free of antinutrients.

#### What these notes do not mean

They are not a reason to avoid these foods. Legumes, whole grains, nuts, and leafy greens are among the most nutritious foods available. The minerals and protein they supply — even after antinutrient reduction — are substantial, and their other benefits (fiber, phytonutrients, cost, sustainability) are undiminished. The notes exist so you can make informed preparation choices and avoid assuming that every labeled nutrient is fully absorbed.

The practical message is: soak legumes, prefer sourdough or sprouted grains when possible, cook beans fully, pair iron-rich plant foods with vitamin C, and do not rely on spinach as your primary calcium source.


### Oxalate Data [oxalate]

Oxalates are one of the antinutrients discussed in [antinutrients](#antinutrients). The section here covers the detailed data NutriMagnus tracks and how to use it. For general background on what oxalates are and how they compare to other antinutrients, read [antinutrients](#antinutrients) first.

Oxalates (oxalic acid) bind calcium in the gut, reducing its absorption from high-oxalate foods. They are found at very high levels in spinach, Swiss chard, beet greens, and rhubarb, and at notable levels in almonds and some other nuts. For most people the main consequence is that these foods are poor calcium sources despite their labels. For anyone prone to calcium-oxalate kidney stones, total dietary oxalate matters more directly.

NutriMagnus includes the Harvard T.H. Chan School of Public Health oxalate table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine. This data is optional and disabled by default.

To enable it: Settings -> Oxalate data (option 5) -> y.

Once enabled, after you view a food (Foods -> Search and view) or analyze a recipe, NutriMagnus will look up the food in the Harvard table. Three outcomes are possible:

1. The food has already been linked to an oxalate record — the value is displayed immediately. No prompt appears.

2. The food is new — NutriMagnus searches for similar names and presents up to five candidates ranked by name similarity. You choose a number, n (none apply), or s (skip for now). If you choose a match, you confirm it with y. That link is saved and will never prompt again.

3. If you previously confirmed no match (n), the food is silently skipped.

#### Important limitations

- Oxalate values in the Harvard table are reported per serving, not per 100 g. For foods measured in ounces (fish, nuts, meat), NutriMagnus automatically converts to per-100g. For foods measured in cups, pieces, or tablespoons, only the per-serving value is available. Volumetric servings cannot be converted to per-100g without knowing the food's density — that conversion must be done manually if needed.

- For recipe analysis, NutriMagnus sums oxalate only for ingredients where a per-100g value is available. Volumetric-only items are excluded from the total and noted as such.

- Oxalate content varies with preparation method (cooking reduces oxalate in spinach, for example) and growing conditions. All values should be treated as estimates.

- Matching by food name is approximate. "Spinach, raw" in the Harvard table maps reasonably to USDA spinach entries, but processed or branded foods may not match well. Always verify the match makes culinary sense before confirming it.

For background on oxalates and kidney health, see the Harvard Health references in the source data (Settings -> Oxalate data for data provenance).


### Glycemic Index [gi]

The glycemic index (GI) measures how quickly a carbohydrate-containing food raises blood glucose compared to pure glucose (GI = 100). Low-GI foods (55 or below) produce a slower, more gradual rise; high-GI foods (70 and above) cause a faster spike.

GI is shown in the nutrient summary when data is available. It is most useful for comparing foods within the same category — for example, choosing between types of bread or rice. Keep in mind that GI describes a food eaten alone; combining foods in a meal (especially adding fat, protein, or fiber) physiologically blunts the blood glucose response to the carbohydrates present, by slowing gastric emptying and glucose absorption. However, this effect is not fully captured by glycemic load (GL) — see [Glycemic Load](#gl) for why.

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

For a discussion of how GL compares to other approaches for evaluating the blood glucose impact of different meal choices — particularly relevant for people managing diabetes — see [Appendix B: GL and Blood Glucose Comparison](#appendix-b).


### Recommended Dietary Allowances [rda]

RDA values in NutriMagnus come from the Dietary Reference Intakes (DRI) published by the U.S. National Academies of Sciences. They represent the average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group.

When you set a user profile (Settings → User profile), NutriMagnus uses your age, sex, weight, height, and activity level to estimate personalized targets. The calorie estimate uses the Mifflin-St Jeor equation with an activity multiplier. The protein target uses 0.8 g per kg body weight as a baseline minimum.

The comparison table ("Daily Intake vs. Recommended Values") shows how your
logged meals for today compare to your targets.

Columns:
    Nutrient    Name of the nutrient.
    Intake      How much you consumed today from all logged meals.
    Target      Your personalized daily goal for this nutrient.
    % of RDA    Intake / Target x 100. Color coded:
                  Green   At or above the minimum (or within the limit for
                          capped nutrients like sodium).
                  Yellow  Getting close but not yet there.
                  Red     Significantly short, or over the limit.
    Status      A color bar showing the same information visually.

Nutrients without an established Dietary Reference Intake (phytonutrients,
amino acids) are shown without a Target or % of RDA -- those rows show
only the Intake amount.

See [daily nutrient goals](#goals) for a full explanation of how each goal is calculated.


### Daily Nutrient Goals [goals]

NutriMagnus calculates personalized daily nutrient goals from your user profile (Settings → User profile). Each goal is one of three types:

    Minimum  — RDA or Adequate Intake (AI): the daily amount needed to
               meet the requirements of most healthy adults.
    Target   — an estimated ideal intake (currently applies to calories).
    Limit    — Tolerable Upper Intake Level: the maximum safe daily
               amount (currently applies to sodium only).

#### HOW EACH GOAL IS CALCULATED

#### Calories (target)
    Mifflin-St Jeor equation for Basal Metabolic Rate, multiplied by an
    activity factor based on your activity level setting:

        Sedentary (desk job, little exercise)           x 1.2
        Lightly active (light exercise 1-3 days/week)   x 1.375
        Moderately active (3-5 days/week)               x 1.55
        Active (hard exercise 6-7 days/week)            x 1.725
        Very active (physical job or twice-daily)       x 1.9

#### Protein (minimum)
    Scaled to body weight and activity level:

        Sedentary or lightly active   0.8 g per kg body weight
        Moderately active             1.0 g per kg body weight
        Active or very active         1.2 g per kg body weight

#### Carbohydrates (minimum)
    130 g/day — the brain's minimum glucose requirement (fixed for all).

#### Fiber (minimum)
    Age- and sex-dependent Adequate Intake:

        Men under 50: 38 g/day     Men 50+: 30 g/day
        Women under 50: 25 g/day   Women 50+: 21 g/day

#### Sodium (limit)
    2300 mg/day — standard Tolerable Upper Intake Level (fixed for all).

#### Minerals and vitamins
    All use age- and sex-specific values from the Dietary Reference
    Intakes published by the U.S. National Academies of Sciences.
    Values vary by age group and sex; the most common adjustments are
    calcium (increases after age 50-70), iron (higher for premenopausal
    women), vitamin D (increases at age 70), and B6 (increases after 50).

Nutrients without established DRIs (phytonutrients, amino acids) have no
goal shown. The "% today" column and "Daily goal" column are blank for
those rows.

See [RDA](#rda) for a general overview of where these values come from.

## Part 3 — Using NutriMagnus
### Installation

#### Windows

Note: the Windows version is coming soon. When available, installation will be as follows:

1. Go to https://codeberg.org/Tom_Cloyd/NutriMagnus/releases/latest
2. Click **nutrimagnus.exe** to download it
3. Double-click the downloaded file to launch the program

No installation steps are required — the program runs directly from the downloaded file. If Windows displays a security warning ("Windows protected your PC"), click **More info** then **Run anyway**. This warning appears because the program is not yet signed with a commercial certificate; it is safe to proceed.

#### Linux

1. Go to https://codeberg.org/Tom_Cloyd/NutriMagnus/releases/latest
2. Click **nutrimagnus** to download it
3. Open a terminal and navigate to your Downloads folder:

        cd ~/Downloads

4. Make the file runnable (one-time step):

        chmod +x nutrimagnus

5. Launch the program:

        ./nutrimagnus

---

### Getting help [help]

Throughout this manual, **Learn more** links appear next to section headings and analysis output. Click any link to jump to the relevant explanation.

The sections linked from analysis output are:

- [Essential amino acids](#aa) — EAA reference and the nine indispensable amino acids
- [Amino acid scoring](#aa-scoring) — limiting-amino-acid DIAAS scoring method
- [Food annotation](#annotate) — annotate food picker table columns
- [Antinutrients](#antinutrients) — what antinutrients are and how they appear in output
- [Bioavailability](#bioavailability) — DIAAS bioavailability table columns
- [Food Cache](#cached) — Food Cache column guide
- [Complement suggestions](#comp) — protein complement food suggestions
- [Protein completeness](#complete) — what makes a protein "complete"
- [Digestible complete protein](#dcp) — DCP concept and formula
- [DCP cap](#dcp-cap) — why DCP is sometimes capped below the DIAAS projection
- [Digestibility overrides](#dcp-overrides) — protein digestibility overrides table
- [DIAAS](#diaas) — digestible indispensable amino acid score
- [Dietary preferences](#diet) — dietary preferences setting
- [Drafted food profiles](#drafted-foods) — drafted food profiles list columns
- [FAO reference values](#fao) — FAO 2013 amino acid reference requirement
- [Amino acid fetch workflow](#fetch) — fetching missing data with Claude AI
- [Food comparison](#food-comparison) — food comparison table columns
- [Food import](#food-import) — foods to import review table columns
- [Food search](#food-search) — USDA food search results columns
- [Limiting amino acid](#gap) — amino acid gaps and how they are scored
- [Glycemic index](#gi) — glycemic index background
- [Glycemic load](#gl) — glycemic load concept and formula
- [Glossary](#glossary) — abbreviations and key terms
- [Glycemic output](#glycemic) — glycemic load output columns
- [Daily nutrient goals](#goals) — how daily nutrient goals are calculated
- [IAA ratios](#iaa-ratios) — meal amino acid ratios table columns
- [Meal items](#meal-detail) — meal items table columns
- [Meal protein digestibility](#meal-diaas) — meal protein digestibility analysis columns
- [Meal history](#meal-history) — meal history search result tables
- [Meals list](#meals-list) — Meals & Log list columns
- [Missing amino acid profiles](#missing-aa) — missing amino acid profile warnings
- [Nutrient analysis](#nutrients) — nutrient analysis table columns and groups
- [Oxalate data](#oxalate) — oxalate data source, enabling, matching, and limitations
- [My Pantry](#pantry) — My Pantry table columns
- [Protein quality](#protein-quality) — single-food amino acid ratios table columns
- [RDA](#rda) — daily intake vs. recommended values table
- [Recipe ingredients](#recipe-ingredients) — recipe ingredient list columns
- [Recipes list](#recipes) — recipes list table columns


### Reading the output

#### Food Cache — Column Guide [cached]

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

See [amino acid fetch workflow](#fetch) for step-by-step instructions on the i/r fetch workflow.


#### Nutrient Analysis Table [nutrients]

Shows the nutritional content of a food, recipe, or meal portion, grouped
by category (Macronutrients, Minerals, Vitamins, Phytonutrients).

Columns:
    Nutrient     Name of the nutrient.
    Amount       Value for the portion you entered.
    Unit         kcal for calories; g for macronutrients (protein, fat,
                 carbs, fiber, omega fatty acids); mg or mcg for minerals
                 and vitamins.

When analyzing a meal within a full-day context, three additional columns
appear:

    meal %       This meal's contribution to your daily goal, in percent.
    day total %  All meals logged today as a percentage of your daily goal.
    Daily goal   Your personalized nutrient target for the day.

#### Color coding (meal % and day total % columns)
    Green    At or above the daily minimum, or within the upper limit for
             capped nutrients (sodium).
    Yellow   Getting close but not there yet.
    Red      Significantly short of the minimum, or over the limit.

Phytonutrients (carotenoids, choline, isoflavones, etc.) appear only when
USDA data for that food includes those values -- many foods have none.
Amino acids are not in this table; see the Protein Quality section below it.

See [daily nutrient goals](#goals) to see how your daily goals are calculated.
See [RDA](#rda) to see the Daily Intake vs. Recommended Values table.


#### Protein Quality Table [protein-quality]

Shows how a food's amino acid profile compares to the FAO 2013 reference
pattern. Appears below the nutrient table when amino acid data is available.

The header line tells you whether the protein is Complete (all nine
essential amino acids at or above the FAO reference) or Incomplete (at
least one is limiting), and which amino acid is most limiting.

Columns:
    Amino Acid   Name, using FAO pair notation where applicable
                 (Met+Cys, Phe+Tyr).
    Raw ratio    Milligrams of this amino acid per gram of protein, divided
                 by the FAO reference value. 1.0 = exactly meets the
                 reference. Below 1.0 = limiting. Above 1.0 = surplus.
    Adj.         Raw ratio multiplied by the food's DIAAS digestibility
                 coefficient. Appears only when a DIAAS value is saved.
                 The bar chart and completeness classification use this
                 adjusted value when it is available.
    Bar          Visual indicator: each full block represents 0.10, capped
                 at 2.0 (20 blocks).

Color: Green = at or above 1.0 (after adjustment if Adj. is present).
Yellow = below 1.0.

See [DIAAS](#diaas) for the DIAAS concept. See [limiting amino acid](#gap) to understand what "limiting"
means. See [FAO reference values](#fao) for the FAO reference values used for each amino acid.


#### Meal Protein Digestibility Analysis [meal-diaas]

Step 1 of the meal DIAAS calculation. Shows how much protein from each
ingredient actually reaches your bloodstream -- before the limiting amino
acid penalty is applied.

Columns:
    ID              USDA FDC ID, OFF, or usr. Type ?glossary for ID types.
    Food            Ingredient name.
    Food tot. gr.   Total grams of this ingredient in the meal (across all
                    items that reference it).
    Protein         Raw (crude) protein from this ingredient, in grams.
    Digestibility   True ileal digestibility coefficient (0.00-1.00): the
                    fraction of protein absorbed by the small intestine.
    Digestible prot Protein x Digestibility. What your body absorbs from
                    this ingredient, before the amino acid step.
    AA              Amino acid data: checkmark = present, X = not available.
                    Ingredients without AA data are excluded from DIAAS.

#### Color coding for Digestibility
    Green   0.90 or above (high: eggs, dairy, soy isolate, fish).
    Yellow  0.80-0.89 (moderate: most whole legumes, whole grains).
    Red     Below 0.80 (lower: some seeds, raw legumes, high-fiber foods).

#### Suffixes in the Digestibility column
    ~est    Estimated from food category average; no measured value for
            this specific food.
    up-arrow user    You set a custom value (Settings -> Advanced ->
            Digestibility overrides). Type ?dcp-overrides.

The totals row sums ingredient weight, crude protein, and digestible
protein across all ingredients.

Note: the "Total digestible protein" here is step 1 of a two-step method.
Step 2 (the DIAAS limiting-amino-acid penalty) reduces it further.
See [amino acid scoring](#aa-scoring) for the full step-by-step method.
See [DIAAS](#diaas) for background on DIAAS and true ileal digestibility.


#### Meal Amino Acid Ratios Table [iaa-ratios]

Step 2 of the meal DIAAS calculation. Shows the pooled amino acid supply
across the whole meal, expressed as a ratio vs. the FAO 2013 reference.

Columns:
    Amino Acid   Essential amino acid (FAO pair notation for Met+Cys and
                 Phe+Tyr).
    Ratio        Pooled digestible grams of this AA from all ingredients,
                 divided by (FAO reference value x total meal protein).
                 1.0 = exactly meets the reference. Below 1.0 = shortfall.
                 Above 1.0 = surplus.
    Bar          Visual indicator; each block = 0.10, capped at 2.0.

The amino acid with the lowest ratio is the limiting amino acid, marked
"LIMITING". The meal DIAAS score equals that lowest ratio (capped at 1.0).

#### Color coding
    Green    1.0 or above.
    Yellow   0.80-0.99.
    Red      Below 0.80.

The panel below this table shows the final Digestible Complete Protein
figure: total meal protein x the DIAAS score.

See [DIAAS](#diaas) for the DIAAS concept. See [amino acid scoring](#aa-scoring) for the step-by-step
two-stage calculation method. See [digestible complete protein](#dcp) for Digestible Complete Protein.


#### Bioavailability Table [bioavailability]

This section appears in two forms depending on context.

#### SINGLE FOOD (labeled BIOAVAILABILITY)

Shown when viewing a food with a saved DIAAS estimate. Displays:
    - Protein digestibility score (literature DIAAS, 0.00-1.50 scale).
    - A bar proportional to the score.
    - Digestible protein in grams from this portion.
    - Digestible complete protein (when amino acid data is also present).
    - Antinutrient notes when applicable (phytates, oxalates, lectins,
      bound niacin). Each note names the compound, describes the specific
      problem, and lists preparation steps that reduce the effect.
      Type ?antinutrients for a full explanation of what these notes mean.

#### RECIPE PER SERVING (labeled BIOAVAILABILITY -- PER SERVING)

Per-ingredient table in recipe analysis. Columns:
    ID              FDC ID, OFF, or usr.
    Ingredient      Name.
    Serving         Grams of this ingredient in one recipe serving.
    Crude protein   Raw protein from this ingredient (g per serving).
    Digestibility   True ileal digestibility coefficient (0.00-1.00).
    Limiting IAA    Most-limiting amino acid for this ingredient, or
                    "-- (complete)" if none.
    Digestible      Crude protein x Digestibility (g).

Color for Digestibility: Green 0.90+, Yellow 0.70-0.89, Red below 0.70.

A summary panel below the table shows total digestible protein and the
pooled DIAAS score for one recipe serving.

See [DIAAS](#diaas) for DIAAS background. See [digestible complete protein](#dcp) for Digestible Complete
Protein. See [complement suggestions](#comp) for complement food suggestions.


#### Meals and Log List [meals-list]

The main Meals & Log screen lists your recent meals, 15 at a time.

Columns:
    ID              Meal ID. Use with commands: v3 view, a3 analyze,
                    d3 delete.
    Date            Date of the meal (YYYY-MM-DD).
    Complete        Checkmark when you have marked the meal finished
                    (option 6 in the meal action loop).
    Meal            Name you gave the meal (e.g. Breakfast, Lunch).
    Items           Number of foods and recipes logged in this meal.
    Meal BCP        Bioavailable complete protein for this meal alone (g).
    Day BCP         Sum of BCP for all complete meals on this date. Shown
                    on the topmost row for each date only.
    % profile goal  Day BCP as a percentage of your daily protein target.
                    Shown on the topmost row for each date only.

BCP values start as -- and are computed on demand.

    --    BCP not yet computed. Press p to compute for all complete meals
          currently shown (results are saved permanently).
    n/a   BCP was computed but no amino acid data was available for any
          ingredient.

% profile goal requires a user profile (Settings -> User profile). Blank
if no profile is set.

Commands: n=new  v{id}=view/edit  a{id}=analyze  d{id}=delete
  s=search history  p=compute BCP  mr=next 15 older  ml=15 newer
  d{YYYY-MM-DD}=jump to date

See [digestible complete protein](#dcp) for a full explanation of digestible complete protein.
See [daily nutrient goals](#goals) to see how your daily protein target is calculated.


#### Meal Items Table [meal-detail]

Shows the foods and recipes logged in a single meal.

Columns:
    ID        Item ID. Use this number with options 2 (Edit) and 3 (Remove)
              in the meal action loop.
    Amount    Portion recorded: grams for foods, or serving count for
              recipes. Volume unit labels are shown where applicable.
    Food /    Name of the food or recipe. Food items show the USDA FDC ID
    Recipe    before the name. Recipe items show "(recipe)" after the name.

To add, edit, or remove items, use options 1, 2, and 3 in the meal
action loop, opened with v{id} from the meal list.


#### Glycemic Load Output [glycemic]

Shows the estimated glycemic load (GL) for a meal or recipe.

The number displayed is the total GL. Color coding:
    Green   10 or below (low glycemic impact).
    Yellow  11-19 (medium).
    Red     20 or above (high).

When the output reads "Not available -- GI annotation missing for: ...",
one or more foods lack a GI value. GL cannot be computed without GI data
for every ingredient. To fix this, annotate the listed foods:
  Foods -> 9 Annotate a food, or Food Cache e# to edit.

GL = (GI x grams of available carbohydrate) / 100 per ingredient,
summed across all ingredients in the meal.

GL is shown for reference only and does not affect protein quality scores.
See [glycemic load](#gl) for a full explanation of glycemic load and its limitations.
See [glycemic index](#gi) for background on the glycemic index.


#### Meal History Tables [meal-history]

These tables appear when you search your meal history with s from the
Meals & Log list. Results can be shown as Flat (every occurrence),
Summary (totals per food), or Both.

#### MEAL HISTORY -- OCCURRENCES
Every time a food or recipe appeared in any logged meal.

    Date        Date of the meal.
    Meal        Name of the meal.
    Food/Recipe Name of the food or recipe. Recipe items show "(recipe)".
    Portion     Amount logged: grams for foods, serving count for recipes.
    Notes       Your note for that item, if any.

#### MEAL HISTORY -- SUMMARY
Totals per food across all matching meals.

    Food/Recipe Name of the food or recipe.
    Times       Number of times this food has been logged.
    Total       Total grams logged (-- for recipes, which are measured in
                servings rather than grams).
    First       Date of the earliest logged occurrence.
    Last        Date of the most recent logged occurrence.

Note: only foods and recipes logged directly as meal items appear here.
Ingredients inside a logged recipe are not individually searchable.


#### Missing Amino Acid Profiles [missing-aa]

When a meal contains ingredients without amino acid data, NutriMagnus
cannot include them in the pooled DIAAS calculation. This section lists
the affected ingredients and describes your options.

NutriMagnus distinguishes two cases:

Standalone meal ingredients: foods logged directly in the meal.
    These can often be replaced on the spot. NutriMagnus can search for
    a USDA Foundation or SR Legacy substitute with amino acid data.

Inside a recipe: ingredients that are part of a recipe you logged.
    These must be fixed by editing that recipe (Recipes -> browse -> edit)
    and replacing the problematic ingredient there.

Safe to ignore when the affected food contributes negligible protein
(garnish, spice, small amount of fruit).
Matters when the food is a significant protein source in your meal.

The DIAAS calculation runs on whichever ingredients do have AA data.
The result is flagged as an estimate, and the DCP figure reflects only
the protein from data-complete ingredients.

See [meal protein digestibility](#meal-diaas) to see the digestibility table. See [DIAAS](#diaas) for DIAAS
background.


#### Recipes List Table [recipes]

Shows all your saved recipes. Displayed when you open Recipes -> Browse
or Recipes -> Search, and after any recipe action.

Columns:
    ID          Recipe ID. Use with commands: a{id} analyze, v{id}
                view/edit, d{id} delete, c{id} copy.
    Name        Recipe name.
    Servings    Number of servings. 0 means the recipe is analyzed by
                total weight or volume rather than a serving count.
    DCP/srv     Digestible complete protein per serving (g). Requires at
                least one full analysis run (a{id}). Shown as -- if not
                yet computed or if no AA data was available.
    Complete    Checkmark if you have marked the recipe finished.
    Created     Date the recipe was first saved.

Commands: a{id}=analyze  v{id}=view/edit  d{id}=delete  c{id}=copy
  x=new recipe  /text=filter by name  r=clear filter
  n/p=next/prev page

See [digestible complete protein](#dcp) for a full explanation of digestible complete protein.


#### Recipe Ingredient List [recipe-ingredients]

Shows the current ingredients in a recipe during create, develop, or edit.
Refreshes after each change so you can see the current state.

Columns:
    #       Row number. Use with Remove (option 3) and Reorder (option 4)
            in the ingredient edit menu.
    Amount  Portion entered: e.g. "175g", "1 T", "2 servings".
    ID      Database identifier for this ingredient.
              A number = USDA FDC ID.
              OFF      = Open Food Facts.
              usr      = User-drafted custom food.
              recipe   = This ingredient is itself a saved recipe (nested).
    Food    Ingredient name.

Nested recipes (ID = recipe) have their nutrients scaled automatically
from their recorded serving count and total weight.


#### USDA Food Search Results [food-search]

Listed after a food search. Combines matches from USDA FoodData Central,
Open Food Facts, and your local Food Cache.

Columns:
    AA      Amino acid data status.
              checkmark    Confirmed in your local cache.
              ~checkmark   Likely available (Foundation/SR Legacy not yet
                           fetched); confirmed on selection.
              X            No amino acid data.
    GI      Your saved glycemic index estimate, if any. Type ?gi.
    DIAAS   Your saved DIAAS estimate, if any. Type ?diaas.
    CONF.   Checkmark if a confidence/source note is saved. View with c#
            in the Food Cache.
    ID#     USDA FDC ID, OFF (Open Food Facts), or usr (user-drafted).
    Name    Food name.
    Type    USDA data category or OFF.
              Foundation     Highest accuracy; most likely to have AA data.
              SR Legacy      Standard Reference; also likely to have AA data.
              Survey (FNDDS) Foods as eaten; AA data less common.
              Branded        Manufacturer data; AA data rare.
              OFF            Open Food Facts (community data).
              star in Type   Already in your local cache (instant, no
                             network call needed).
    Brand   Brand name for Branded and OFF entries.

To select: type the row number. If the food is not yet in your cache,
NutriMagnus fetches and saves it automatically.

See [Food Cache](#cached) for the Food Cache column guide.
See [amino acid fetch workflow](#fetch) to learn how to get missing amino acid data via Claude AI.


#### Food Comparison Table [food-comparison]

Shows up to eight foods or recipe portions side-by-side, with all nutrient
groups in one table. All values are per the portion you entered for each
food, not per 100 g.

The foods and portions you chose are listed above the table as Food 1,
Food 2, etc.

Nutrient groups: Macronutrients, Minerals, Vitamins, Phytonutrients,
Amino Acids. Groups appear only when at least one food has data for that
category.

    Green   The highest value in that row across all foods.
    --      No data for this nutrient in this food.

Rows where every food shows -- are hidden automatically.

To run a comparison: Foods -> Compare foods side-by-side.
You can save the food list under a name for quick reuse in future sessions.
Previously saved lists are offered at the start of the comparison flow.


#### Annotate Food Picker Table [annotate]

Appears when you choose Foods -> Annotate a food. Pick a food from your
cache to annotate.

Columns:
    #       Row number. Type the number to select that food.
    Name    Food name.
    Type    USDA data category or OFF. Type ?food-search for type meanings.

Type /text to filter by food name (e.g. /tofu shows only tofu entries).
Type / alone to clear the filter.

After selecting a food, you can add or update:
    GI      Glycemic index (0-100). Type ?gi.
    DIAAS   Your protein quality estimate (0.00-1.50). Useful for packaged
            foods that lack amino acid data in USDA. Type ?diaas.
    Prep    A short preparation note (e.g. "boiled 20 min", "raw").

Annotations appear wherever that food is used: Food Cache list, food and
recipe analysis, and meal analysis.


#### Foods to Import Review Table [food-import]

Appears when you run r (Read Claude response) from the Food Cache to
import data from ~/claude_response.txt. Shows a preview so you can
review before confirming the write.

Columns:
    Name        Food name from the Claude response.
    FDC ID      USDA FDC ID if one was provided.
    Calories    Calorie value from the response (per 100 g).
    Protein     Protein value (g per 100 g).
    AA count    How many of the 11 tracked amino acids were found
                (e.g. 9/11 means 9 out of 11 were present).

Review each row for plausibility. If a value looks wrong, press n to
cancel, correct ~/claude_response.txt, and re-run r.

After confirming, each food is written to your cache. Foods that gain
amino acid data change from X to checkmark in the AA column of the
Food Cache. Any notes Claude added are saved as curator notes (view
with c# in the Food Cache).

For the full import workflow, see [amino acid fetch workflow](#fetch).


#### Drafted Food Profiles List [drafted-foods]

Shows the custom food profiles you have created by hand -- products from
a label, research table entries, or supplements not in USDA or Open Food
Facts.

Columns:
    #       Row number. Use to select a profile for viewing or editing.
    Name    Food name as you entered it.
    Note    Your optional source or description note.

Drafted foods are stored in your Food Cache and appear in all food
searches alongside USDA and Open Food Facts entries. In ID columns
throughout the program, drafted foods are shown as "usr".

To edit nutrient data: Foods -> Food Cache, find the food, and use e#.
Editing is done in the Food Cache, not in this list.

To create a new custom profile: Foods -> Drafted Food Profiles -> Create.
See [amino acid fetch workflow](#fetch) for an alternative way to get missing data (e.g. amino acid
data from Claude AI for foods not in USDA).


#### My Pantry Table [pantry]

Shows the protein sources you have flagged as currently on hand. The
Pantry drives the complement advisor -- when NutriMagnus suggests foods
to fill an amino acid gap, it checks your pantry first and shows matching
foods in a "From your pantry" tier.

Columns:
    #       Row number.
    ID      USDA FDC ID, OFF, or usr. -- for name-only entries.
    AA      Amino acid data status.
              checkmark  AA data in your cache. This food can be used in
                         complement suggestions.
              X          No AA data. Add data via the Food Cache (option c).
              --         Name-only entry: no USDA link, no nutrient data.
                         Search for this food via Foods to add it properly.
    Food    Food name.
    Notes   Your optional note for this pantry entry.

Only pantry foods with AA data (checkmark) appear in complement
suggestions. Name-only entries (--) and those without AA data (X)
may still appear if their name matches a built-in complement table entry.

Commands:
    a   Add a food (USDA search or name-only).
    r   Remove a food from the pantry.
    c   Open the Food Cache to edit nutrients for a pantry food.

See [complement suggestions](#comp) for how complement suggestions use your pantry.


#### Protein Digestibility Overrides [dcp-overrides]

Shows your custom true ileal digestibility coefficients. These values
override the defaults NutriMagnus uses in meal-level DIAAS calculations.

Columns:
    Food name       Name of the food this override applies to (matched
                    case-insensitively against meal ingredients).
    Digestibility   Your custom coefficient (0.00-1.00). The fraction of
                    protein absorbed by the small intestine.
    Notes           Your source note (e.g. "Smith 2020 Table 3").

When an override is active for a meal ingredient, the Digestibility column
in the Meal Protein Digestibility table shows the value with an
"up-arrow user" suffix, distinguishing it from estimated or literature
defaults.

Use overrides when you have found a published measured value for a food
you eat regularly and it differs meaningfully from NutriMagnus's default.
Values should come from primary literature (ileal digestibility studies),
not from product labels or general nutrition sources.

Commands:
    a   Add or update an override (enter food name, then coefficient).
    d   Delete an override.

See [meal protein digestibility](#meal-diaas) to see where this value appears in the analysis output.
See [DIAAS](#diaas) for background on true ileal digestibility.

---

### Menu navigation

These conventions apply at every prompt throughout the program — menus, search results, ID entry, portion sizing, and ingredient loops. You are never required to finish a flow before you can leave it.

| Key | Action |
|-----|--------|
| `1`–`9` | Select a numbered menu item |
| `b` | Go back to the parent menu |
| `m` | Jump directly to the main menu |
| `q` | Quit the program |
| Ctrl+C | Cancel the current prompt (same as `b`) |
| Escape | Same as Ctrl+C |
| ↑ / ↓ | Cycle through input history at any free-text prompt |

`b`, `m`, and `q` are accepted at every prompt. Ctrl+C and Escape are caught silently and treated as "back" — they never crash or exit the program unexpectedly.

---

### *Output samples { #outputSamples}

(Incomplete and outdated; to be updated very soon...)

#### Launching the program from the command line => main menu displayed

![program launch - main menu](26-04-08-status-main-menu.png)

The main menu is simple. There are 5 main functions, each numbered. There are also several support functions, one of which simply ends the program. Below, I have selected function 2. I want to make sure the recipe I want to enter is not already partially entered.

```
────────────────────────────────────────────────────────────────────────────────────────────────────
────────────────────────────────────────────────────────────────────────────────────────────────────
NutriMagnus ("nutrition wizard")
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
  4. Analyze a recipe portion  (saves analysis with date)
  m. Return to main menu
  q. Quit

Choice: 2

```

#### Entering a recipe

**Main menu** function 2 brings up the **Recipes** menu, and again I enter 2, to get a list of the recipes NuMa knows about.

Notice the options available in the **Recipes** menu: One can start a recipe and return to it later to edit it or even delete it. One can also copy it to have multiple versions. Item 3 on the menu is particularly interesting: One can develop a recipe, using nutritional feedback to make ingredient choices that achieve nutritional goals.

Now, looking at the displayed list of recipes, I see that the one I want to enter is already there, so I enter `v 5` (it could also have been `v5`) to look at recipe 5, which is then immediately displayed.

```
Recipes
────────────────────────────────────────────────────────────────────────────────────────────────────
  1. Create new recipe
  2. Browse / view, edit, copy, delete recipes
  3. Develop a recipe  (add/remove ingredients with nutritional feedback)
  4. Analyze a recipe portion  (saves analysis with date)
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

  See the [Getting help](#help) section for a list of available topics.

  Actions: v=view/edit  x=develop  a=analyze  d=delete  c=copy  ·  s=search  b=done
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

  See the [Getting help](#help) section for a list of available topics.

  Actions: v=view/edit  x=develop  a=analyze  d=delete  c=copy  ·  s=search  b=done
  (Enter action + ID, e.g. v3 or x 14)
: v5

```

The recipe is incomplete, and now I can work to complete it. Entering `v5` opens the recipe view, which shows the full text (name, ingredients, procedure) and ends with `e=edit  b/Enter=done`. Pressing `e` at that prompt opens the edit flow.

In the output you will see a program 'bug' - The **Procedure** is not wrapped around to match the length of the other lines, and the line beneath it should be truncated. This is now fixed, but I leave the problem for you to see because the program is still at the beta stage, and such bugs are to be expected - especially in output formatting (which is a concern secondary to output content) is still being tuned up.

(Additional output samples are coming...)

### *Usage tips

(under development)

* **Input history:** At any free-text prompt (food or recipe name, search term, amount, note, etc.) you can press the **up arrow** to recall what you typed previously. Press up again to go further back, and **down arrow** to move forward again. If you started typing before pressing up, your partial input is saved and restored when you press down back to the current position. History persists across sessions (saved to `~/.numa_history`), holds up to 1000 entries, and skips consecutive duplicates.

* **Enter food portions:** if at all possible, enter weights, not volume measures. A cup of flour can vary greatly depending upon how much air is stirred into it. A cup of spinach is even harder to pin down. Even nuts can be a problem. But weights are far less likely to vary, and so are much more reliable.

* **Exporting results:** at the end of most analysis screens (food portion, recipe analysis, meal analysis) you are offered the option to save the output as a plain-text (`.txt`), Markdown (`.md`), or HTML (`.html`) file. The file is saved to a folder of your choice. This is the easiest way to keep a record of an analysis or share it with someone else.

### Using the Foods menu

The Foods menu (main menu option **1**) has nine sub-options. Most start with a food search — type any part of a food name, an FDC ID number, or a 12-digit barcode.

#### Search food databases (Foods → 1)

Searches USDA FoodData Central and Open Food Facts. Your local Food Cache is checked first; any cached match appears instantly at the top of the results list with no network call. Select a food to see its complete nutrient table (per 100 g), protein completeness analysis, and DIAAS bioavailability data. If amino acid gaps are present, complement suggestions are shown automatically.

After the per-100g display, you are asked whether to analyze a specific portion. Answer **y** to open the portion picker.

#### Analyze a food portion (Foods → 2)

Works like Foods → 1 but goes directly to portion analysis after you select a food — no separate confirmation is needed. After you choose a serving size, NutriMagnus shows the full nutrient table scaled to that portion, together with protein completeness, bioavailability data, and complement suggestions if any amino acids fall short.

Saved recipes are included in the search results. When you pick a recipe, you enter a number of servings instead of a weight, and the recipe's nutrients are scaled accordingly.

A brief note at the end of a recipe analysis explains that the per-ingredient TID (digestibility) breakdown is available under Recipes → Browse — this shortcut shows combined totals only.

At the end of every analysis, you are offered the option to export the results as a text, Markdown, or HTML file.

#### Analyze a saved recipe portion (Foods → 3)

A shortcut for quick recipe analysis. Shows the list of your saved recipes; enter a recipe ID and a number of servings. The output is the scaled nutrient table for that portion, protein completeness, and complement suggestions — without the per-ingredient detail of the full recipe analysis in the Recipes menu.

#### Convert a portion ↔ weight (Foods → 4)

Converts any volume or weight measure to grams without running a full nutritional analysis. Useful when a recipe or label gives you a volume and you need the weight to log it accurately.

Search for a food, then type an amount. A few examples:

    150        →  grams
    3 oz       →  ounces
    1/4 c      →  cups
    2 T        →  tablespoons

The space between number and unit is always optional: `2T`, `0.25c`, `150g`, and `3oz` work exactly like their spaced equivalents. For the full list of recognized units and input formats, see [Appendix F](#portion-formats).

NutriMagnus looks up the food's density and returns the gram equivalent. If no density data is available for that food and measure, it asks you to weigh your portion and enter the result manually.

You can convert multiple amounts for the same food in a row — the prompt repeats until you press Enter or `b`.

#### Compare foods side-by-side (Foods → 5)

Select up to eight foods (or recipe portions) and NutriMagnus displays them in a single side-by-side table. All nutrient groups are shown — macronutrients, minerals, vitamins, phytonutrients, and amino acids — with the highest value in each row highlighted in green.

**Adding foods to the comparison:**

1. At each "Food N — search" prompt, type a food name, FDC ID, or barcode as usual.
2. After selecting a food, choose a portion. That portion's nutrients appear as one column in the table.
3. Once you have added at least two foods, press Enter (or `b`) to display the table. You can add up to eight.

**Re-picking without a new search:** after the first food is added, if the next food you want was already in the last search results, just type its row number — no second network call is made.

**Saved comparison lists:** after the table is shown, you can save the food list under a name. Saved lists appear at the start of the next comparison session so you can reload them without re-searching. Useful for groups you compare regularly (e.g. different protein powder brands, or candidate legumes for a new recipe).

#### Food Cache (Foods → 6)

Described in detail under [Food data — where it comes from and how it is stored](#food-data) and the [Food Cache](#cached) help topic. This is the primary place to view, edit, and delete stored foods, and to run the Claude AI amino acid fetch workflow (`i` / `r` commands).

##### Fetching Missing Nutritional Data from Claude [fetch]

Some foods in your cache are missing amino acid data (shown as ✗ in the AA
column). You can fill this gap using Claude at claude.ai — no paid subscription
required. The workflow has four steps.

#### Step 1 — Generate the prompt

    In the Food Cache list, type i followed by the row numbers of the foods
    you want data for:

        i30          (one food — row 30)
        i30,67       (two foods — rows 30 and 67)
        i            (all foods in the current list that show ✗)

    NutriMagnus writes a prompt to ~/claude_prompt.txt and tells you its
    full path. (`~` in that file pathname indicates that the file belong
    in the root of your computer's user account file system.)

#### Step 2 — Send the prompt to Claude

    IMPORTANT: Start a brand-new chat at claude.ai for each request.
    Do NOT reuse a previous chat window. This ensures the copy step
    below captures only Claude's one response, nothing else.

    Open ~/claude_prompt.txt (any text editor) and copy its entire contents.
    Go to claude.ai in your browser (a free account is sufficient).
    Open a new chat, paste the text, and press Enter or click Send.

#### Step 3 — Save Claude's response

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

#### Step 4 — Import the data

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

For full context and annotated examples, see 'Getting missing amino acid data'
in the user manual (HTML version: #food-cache-fetch-workflow).

#### My Pantry (Foods → 7)

Described under [Food data — where it comes from and how it is stored](#food-data). Commands inside the Pantry menu:

| Key | Action |
|---|---|
| `a` | Add a food to your pantry (search USDA or enter name only) |
| `r` | Remove a food from your pantry |
| `c` | Jump to the Food Cache to edit nutrients for a pantry food |

#### Custom food profiles (Foods → 8)

Described under [Entering custom foods and dietary supplements](#custom-foods).

#### Annotate a food (Foods → 9)

Opens your Food Cache list and lets you pick a food to annotate. Annotations add information that the USDA database does not include:

- **Glycemic index (GI)** — how quickly the food raises blood sugar (scale 0–100).
- **DIAAS estimate** — a protein quality score for packaged foods that lack amino acid data in USDA.
- **Preparation note** — a short reminder such as "boiled 20 min" or "soaked overnight".

Type `/text` at the list prompt to filter by food name before picking. Once saved, annotations appear in the nutrient table and analysis output wherever that food is used.

---

### Using the Recipes menu

The Recipes menu (main menu option **2**) manages everything related to recipes — creating them, editing them, analyzing their nutritional content, and developing them iteratively with nutritional feedback.

#### Create a new recipe (Recipes → 1)

You are prompted for the recipe header, then its ingredients, and finally its procedure (cooking instructions).

**Header prompts:**

| Prompt | Notes |
|---|---|
| Name | Required. Appears in all search results and meal logs. |
| Description | Optional. A one-line note about the dish. |
| Number of servings | Enter **0** to analyze the recipe by total weight or volume rather than by serving count. |
| Serving size | Optional label, e.g. "1 cup" or "1 slice". |
| Total volume | Optional, e.g. `4 cups` or `500 ml`. Used to compute per-100ml figures when servings = 0. |
| Total weight | Optional, e.g. `800 g` or `1.5 lb`. Used to compute per-100g figures when servings = 0. |
| Mark as complete? | Whether the ingredient list is finished. Shown in the recipe list table. |

**Ingredient loop:** after the header is saved, you enter ingredients one by one. At each "Search food or recipe" prompt, type a food name, FDC ID, or barcode. Other saved recipes are also searchable and can be nested as ingredients — NutriMagnus scales their nutrients automatically from their serving counts.

For each ingredient:
1. Choose a portion (weight, volume, or a USDA standard portion listed for that food — see [Appendix F](#portion-formats) for all accepted formats).
2. Add an optional note (e.g. "drained", "cooked", "raw"). Press Enter to skip.

The current ingredient list is printed after each addition. When you are done, press Enter or `b`.

**Procedure:** a text editor opens for cooking instructions. Press `b` to skip and save immediately. The editor used is set under Settings → 5 (Editor command); if not set, the system default (`$VISUAL` / `$EDITOR`) is used.

#### Browse, view, edit, copy, and delete recipes (Recipes → 2)

Displays all your recipes sorted by most recently accessed. The table shows:

| Column | Meaning |
|---|---|
| ID | Recipe number — use this in commands |
| Name | Recipe name |
| Servings | Number of servings (0 = analyze by weight/volume) |
| DCP/srv | Digestible complete protein per serving (requires at least one analysis) |
| Complete | ✓ if the recipe is marked finished |
| Created | Date first saved |

**Commands** — type the action letter immediately followed by the recipe ID (e.g. `v3`, `a 14`):

| Command | Action |
|---|---|
| `v{id}` | View the recipe text (name, ingredients, procedure) and optionally open the edit flow |
| `a{id}` | Run the full nutrition analysis (nutrient table, DCP, TID breakdown, complements, glycemic load) |
| `d{id}` | Delete the recipe after confirmation |
| `c{id}` | Copy the recipe — you are asked for a new name |
| `x` | Create a new recipe (same as Recipes → 1) |
| `/text` | Filter all your recipes to those whose names contain `text` — e.g. `/soup` searches every saved recipe and shows only matches. Type `/` alone to clear the filter. |
| `r` | Return to the most-recently-accessed view (clears any active filter) |
| `n` / `p` | Next / previous page when there are more than 20 recipes |
| `b` / Enter | Done — back to the Recipes menu |

**Viewing and editing a recipe (`v{id}`):** the full recipe text is shown — name, description, volume/weight, ingredients with amounts and ID numbers, and the procedure. At the end, type `e` to open the edit flow or `b` / Enter to return to the browse list.

The edit flow lets you update any header field (name, description, servings, serving size, volume, weight, complete flag) and manage the ingredient list: add, edit, remove, or reorder ingredients. The ingredient list menu also offers:

| Key | Action |
|---|---|
| `a` | Run a full nutrition analysis on the recipe as currently saved |
| `x` | Export the recipe — see below |

When done with the ingredient list, you can proceed to edit the procedure in the text editor or press `b` to skip.

#### Exporting a recipe

Press `x` at the ingredient list menu to export the current recipe to a file. NutriMagnus asks whether to include a per-serving nutrition summary, then immediately saves a Markdown file and shows you exactly where it went:

```
Report saved → /home/yourname/.numa/reports/My_Recipe_2026-06-21.md
```

You are then offered the option to save an additional copy in plain text (`.txt`), Markdown (`.md`), or HTML (`.html`).

**What the file contains:**

- Recipe name, description, and serving count
- Ingredients list with amounts and any notes you have added
- Procedure (if entered)
- Optionally: a per-serving nutrition table (macronutrients + digestible complete protein)

**Example output** (Markdown format, single serving, nutrition included):

```markdown
# Oatmeal high protein, seeds, okara
*no protein powder, tasty*
**Servings:** 1  *(2.5 c per serving)*

## Ingredients

- 243.7 gr (1 cup)  Soy milk, sweetened, plain, refrigerated
  *(homemade is presumed; commercial is fine)*
- 30 g (1 7/8 T)  Old Fashioned Peanut Butter
  *(can substitute peanuts)*
- 10 g (1 T)  Ground Flax Seeds
- 10 g (1 1/6 T)  Seeds, hemp seed, hulled
- 10 g  Nutritional Yeast Flakes
- 55 g (10 1/3 T)  Oats, whole grain, rolled, old fashioned (dry)
- 35 g (4 T + 1 2/5 t)  Organic Pure Okara Flour
- 12 g (1 T)  Chia Seeds, dry, raw  *(ground)*
- 20 g (2 T + 1 3/8 t)  Apricots, dried, sulfured, uncooked
  *(approx. weight of 3)*
- 25 g (2 T)  Plums, dried (prunes), uncooked
  *(approx. weight of 4)*
- 33 g (13 1/5 T)  Cranberries, dried, sweetened
  *(approx. weight of 1/4 c)*

## Procedure

1. To saucepan add soy milk, peanut butter, hemp seed, flax seed,
   nutritional yeast. Do not turn on heat yet.
2. Add chopped fruit.
3. Measure out oats, okara, chia. Set aside.
4. Heat liquid on med. high heat, wiping bottom of pan at all times
   with rubber scrapper.
5. When bubbling strongly, stir in well the oats mixture.
   Cover and remove from heat.
6. May be eaten immediately, or allowed to cook with residual heat
   for up to 10 minutes.

## Nutrition — whole recipe

| Nutrient                    | Amount  | Unit |
|:----------------------------|--------:|:-----|
| Calories                    |  920.18 | kcal |
| Protein                     |   43.50 | g    |
| Carbohydrate                |  123.96 | g    |
| Total Fat                   |   39.84 | g    |
| Fiber                       |   24.55 | g    |
| Sugars                      |    3.21 | g    |
| Saturated Fat               |    4.99 | g    |
| Monounsaturated Fat         |    9.81 | g    |
| Polyunsaturated Fat         |   15.12 | g    |
| Digestible complete protein |   41.4  | g    |
```

**Where files are saved:**

All auto-saved reports go to `~/.numa/reports/`. If you export an additional copy (txt/md/html), it goes to `~/.numa/user-requested-nutrition-reports/`. NutriMagnus always prints the full file path so you know exactly where to find it.

The DCP figure in the nutrition summary comes from the most recent analysis run (`a` key or Recipes → 4). If you have never analyzed the recipe, that row shows "not computed — run analysis first."

#### Develop a recipe (Recipes → 3)

Use this when you want to refine a recipe's ingredient list with nutritional feedback at each step. After each ingredient is added or removed, NutriMagnus asks whether you want a fresh analysis — answer **y** and the full nutrient table and DCP calculation appear immediately so you can make informed ingredient decisions.

Add ingredients the same way as in Create (food name, FDC ID, barcode, or another recipe). Remove an ingredient by typing its row number. When you are satisfied with the ingredient list, press `d` to proceed to the procedure editor.

#### Analyze a recipe portion (Recipes → 4)

Select a recipe, then enter a number of servings. NutriMagnus shows a full nutritional analysis:

- Total recipe nutrients and per-serving nutrients (or per-100g / per-cup when servings = 0)
- Digestible complete protein (DCP) per serving, saved to the recipe for the recipe list
- Protein completeness table and per-ingredient digestibility breakdown (TID table)
- Complement suggestions if amino acid gaps are present
- Glycemic load (if GI annotations are set for all ingredients)

**Saved analysis:** after the analysis runs, a plain-text snapshot is saved to the recipe. The next time you select the same recipe here, you are offered the choice to view the saved snapshot (`s`) or re-run a fresh analysis (`r`).

**Handling missing data:** if some ingredients are missing amino acid data or have no recorded weight (volume-only entries), an options menu appears:

| Option | Action |
|---|---|
| Fix | Replace affected ingredients by searching USDA Foundation Foods — results show an AA column (✓ / ✗) so you can pick an entry with complete data |
| Provide missing data | Enter gram weights for volume-only ingredients on the spot |
| Calculate anyway | Run the analysis with the available data; the DCP result is flagged as approximate |
| Skip DCP | Proceed with the nutrient analysis only, without a DCP figure |

#### Search recipes (Recipes → 5)

Filters your recipe list as you type. Each character you enter narrows the list to recipes whose names contain the text typed so far. To pick a recipe from the filtered list, type `/1`, `/2`, and so on (using the row number shown in the filtered view). After picking, choose an action: `v` view, `a` analyze, `d` delete, `c` copy.

---

### Using the Meals & Log menu

The Meals & Log screen (main menu option **3**) is where you record what you eat each day. It shows a list of your recent meals — 15 at a time — with these columns:

| Column | Meaning |
|---|---|
| ID | Meal ID used in commands below |
| Date | Date of the meal |
| Complete | ✓ when you have marked the meal finished |
| Meal | Meal name |
| Items | Number of logged food/recipe items |
| Meal BCP | Bioavailable (digestible) complete protein for this meal (g) |
| Day BCP | Sum of BCP across all complete meals on the same date (shown on topmost row for each date) |
| % profile goal | Day BCP as a percentage of your daily protein target from your user profile (shown on topmost row for each date) |

BCP values start as `—` and are computed on demand with the `p` command (see below). Once computed they are saved permanently and shown every time you open the list. If you have a user profile set, the screen title shows your daily BCP protein goal in grams.

#### Commands on the meal list

| Command | Action |
|---|---|
| `n` | Create a new meal (prompts for date and name) |
| `v{id}` | Open a meal to view, add to, or edit (e.g. `v5`) |
| `a{id}` | Analyze a meal, or optionally all meals on the same date |
| `d{id}` | Delete one meal (e.g. `d5`) |
| `d{id} {id} {id}` | Delete multiple meals by space-separated IDs (e.g. `d3 5 7`) |
| `d{id}-{id}` | Delete a range of meal IDs (e.g. `d3-7`) |
| `s` | Search your entire meal history for a food by name |
| `p` | Compute BCP for all complete meals currently shown (and any other complete meals on the same dates, so Day BCP reflects the full day). Results are saved to the database and can be recomputed at any time by pressing `p` again. |
| `mr` | Load the next 15 older meals |
| `d{YYYY-MM-DD}` | Jump to meals on or before a specific date (e.g. `d2025-06-01`) |
| `b` / Enter | Back to main menu |

#### Creating a meal

Type `n`. You are asked for:

1. **Date** — defaults to today. Press Enter to accept, or type a date in `YYYY-MM-DD` format.
2. **Meal name** — e.g. "Breakfast", "Lunch", "Evening smoothie". Defaults to "Meal".

After the meal is created you are taken immediately into the meal action loop (below) where you can start adding items.

#### The meal action loop

Opening a meal with `v{id}` (or just after creating one) shows the current items and this menu:

| Option | Action |
|---|---|
| **1** | Add items |
| **2** | Edit an item |
| **3** | Remove an item |
| **4** | Analyze this meal |
| **5** | Delete this meal |
| **6** | Mark complete / Mark incomplete |
| **7** | Rename this meal |
| **8** | Merge with meal(s) on the same date *(shown only when other meals exist on that date)* |
| `b` | Back to the meal list |

#### Adding items to a meal

Choose **1**. At the "Search food or recipe" prompt, type a food name, FDC ID, or barcode. Saved recipes are included in the results automatically.

**Adding a food:** after picking the food, choose a portion (weight, volume, or a USDA standard portion — see [Appendix F](#portion-formats) for all accepted formats). You are then offered an optional note field — a short label like "with skin" or "boiled". Press Enter to skip.

**Adding a recipe:** enter the number of servings you are logging (e.g. `1`, `0.5`, `1 1/2`). You can also enter a gram weight followed by `g` (e.g. `290 g`) — NutriMagnus calculates the equivalent serving count from the recipe's recorded total weight. If the recipe has no total weight on record, you are asked to supply it.

The updated item list is shown after each addition. Add as many items as needed; press Enter or `b` to finish.

#### Editing and removing meal items

**Edit (option 2):** the item list is displayed and you enter the item ID you want to change. For food items:

| Sub-option | Action |
|---|---|
| `f` | Change the food (search for a different food by name) |
| `a` | Change the amount (re-enter the portion) |
| `n` | Edit the note |
| `d` / Enter | Save changes and return |

For recipe items, you can update the number of servings.

**Remove (option 3):** enter the item ID to remove it immediately.

#### Analyzing a meal

Choose **4** from the meal action loop, or type `a{id}` from the main meal list. If there are multiple meals on the same date, you are asked whether to analyze just the selected meal or combine all meals from that date.

The analysis shows:

- Full nutrient table. If you have a user profile set, a "% of today's total" column shows how this meal contributes to your daily intake.
- Meal-level pooled DIAAS and digestible complete protein (see [How NutriMagnus scores meal and recipe protein quality](#protein-scoring) for the method).
- Complement suggestions if amino acid gaps are present.
- Glycemic load for the meal (if GI annotations are set for all foods).

**Missing amino acid data:** if the meal includes foods without amino acid profiles that appear to be meaningful protein sources, NutriMagnus tells you how many are affected and which are inside logged recipes (fix those by editing the recipe) versus standalone meal items (those can be replaced on the spot via a focused Foundation Foods search). You can also skip the fix entirely — the analysis still runs using whichever foods do have AA data.

**Refreshing AA data:** at the end of the analysis you are offered the option to go online and fetch the latest amino acid data from USDA for any foods that were missing it. The data is saved to your cache, and the next analysis of the same meal will be faster and more complete.

#### Marking a meal complete

Choose **6** (Mark complete). This puts a ✓ in the Complete column on the meal list as a personal flag that you have finished logging this meal. It can be toggled at any time. Meals must be marked complete before BCP is computed for them — the `p` command on the meal list skips incomplete meals.

#### Merging meals

If you logged the same eating occasion as two or more separate meals and want to consolidate them, open any of them and choose **8**. You are shown all meals on the same date. Enter specific IDs (space-separated) or type `all` to merge everything on that date. After the merged meal is created, you are asked whether to delete the originals.

#### Searching meal history

Type `s` from the meal list. Enter a food name (partial matches work). Results can be viewed as:

| View | Shows |
|---|---|
| Flat list | Every logged occurrence — date, meal name, food name, portion, note |
| Summary | Totals per food name — number of times logged, total grams, first and last date |
| Both | Flat list followed by summary |

Note: this search finds foods and recipes logged directly as meal items. Ingredients inside a logged recipe are not included in the search.

---

### Using the Daily Summary menu

The Daily Summary menu (main menu option **4**) aggregates all meals on a given day into one nutrient report.

| Option | Action |
|---|---|
| **1** | Today's summary |
| **2** | Summary for a specific date — enter `YYYY-MM-DD` at the prompt |
| **3** | List the 30 most recent dates that have meals logged |

The summary shows, in order:

- Combined nutrient table for all meals on the date
- Pooled meal-level DIAAS and digestible complete protein (spanning all meals on the day)
- Protein adequacy assessment if a user profile is set
- Complement suggestions for any amino acid gaps in the day's total protein

**RDA comparison:** if a user profile is set (Settings → 2), you are asked at the end whether to compare your intake against your personalized daily targets. Answer **y** for a color-coded breakdown: green = at or above the goal, yellow = close, red = significantly short or over the limit. This comparison uses the same targets shown under Settings → 3 (View daily nutrient targets).

If no profile is set, the nutrient totals still appear — you just won't see personalized targets. A brief tip at the bottom suggests setting up a profile.

---

### Using the Settings menu

The Settings menu (main menu option **5**) has eight options. The current value of each setting is shown next to its menu item.

#### Color theme (Settings → 1)

Switches the display between available color themes (dark, light, etc.). The new theme takes effect immediately and is saved for future sessions. You can also change the theme from the command line with `/config` (see [help topics](#help) for the full list of slash commands).

#### User profile (Settings → 2)

Enter your personal details so NutriMagnus can compute daily calorie and nutrient targets specific to you:

| Prompt | Format |
|---|---|
| Age | Whole years, e.g. `65` |
| Sex | `m` (male), `f` (female), or `o` (other / prefer not to say) |
| Weight | With unit — e.g. `80 kg` or `176 lbs` |
| Height | As cm (`178 cm`) or feet-and-inches (`5'10"`) |
| Activity level | 1 = sedentary through 5 = very active (a numbered list is shown) |

Press Enter at any prompt to keep the current value. After saving, NutriMagnus immediately shows your estimated calorie target and minimum protein requirement.

Your profile drives the personalized columns and comparisons that appear in meal, recipe, and daily-summary analyses. See [daily nutrient goals](#goals) for the exact formulas used. See [RDA](#rda) for background on where the reference values come from.

#### View daily nutrient targets (Settings → 3)

Displays the full table of personalized nutrient targets derived from your profile — calories, protein, carbohydrates, fiber, all minerals, and all vitamins. Each entry shows the goal type (minimum, target, or upper limit) and the computed value. Requires a profile to be set (Settings → 2).

#### Dietary Preferences (Settings → 4) [diet]

This setting controls which protein sources appear in complement suggestions and food search results throughout the program.
Change it under **Settings → Dietary preferences** (option 4 in the Settings menu).

| Option | Setting | Includes |
|---|---|---|
| 1 | All animal foods | meat, fish, dairy, and eggs |
| 2 | Vegetarian | dairy and eggs only (no meat or fish) |
| 3 | Plant-based only | plant sources only |

The setting is saved between sessions and applies to both the interactive complement display and any exported reports.

**Important — this setting also filters food search results.** If your preference is set to "plant-based only" or "vegetarian", foods outside that category will not appear anywhere in NutriMagnus — not in food searches, not in search results within recipes or meals, and not in any lookup by name or FDC ID. If you search for a food and get no results, check whether your dietary preference setting is silently excluding it. To look up any food regardless of category, temporarily switch to "All animal foods" under Settings, do your search, then switch back.

#### Oxalate data (Settings → 5)

Enables or disables Harvard oxalate data lookup for individual foods and recipes. Disabled by default. When enabled, NutriMagnus checks the Harvard T.H. Chan School of Public Health oxalate table (433 foods) whenever you view a food or analyze a recipe. See [oxalate data](#oxalate) for a full explanation of the matching process, limitations, and data source.

Requires an active user profile. The toggle shows "on" or "off" next to the menu item, and notes if oxalate.db is not found (run `python build_oxalate_db.py` from the application directory if so).

#### Editor command (Settings → 6)

Sets the text editor that opens when you edit the Procedure field of a recipe (in Create, Develop, or Browse → edit). If not set, NutriMagnus uses the system default — the program named in your `$VISUAL` or `$EDITOR` environment variable.

Enter any command your shell can run, for example `nano`, `vim`, or `code --wait` (VS Code in wait mode). To clear back to the system default, type `-`.

#### Display settings at program launch (Settings → 7)

When enabled, NutriMagnus prints the current color theme, dietary preference, and user profile at the top of the screen each time it starts. This provides a quick confirmation of your active configuration without having to open Settings. Turn it off if you find it clutters the opening screen.

#### Advanced settings (Settings → 8)

Contains three sub-options.

**1 — Protein digestibility overrides:** lets you set a custom true ileal digestibility coefficient (a number from 0.00 to 1.00) for any specific food, overriding the default value NutriMagnus uses in meal-level DIAAS calculations. This is for cases where you have found a published study with a measured value for a food you eat regularly.

Enter the food name exactly as it appears in your cache (the match is case-insensitive). NutriMagnus shows you the value it would use without an override. Enter your coefficient and an optional source note. Existing overrides are listed in a table; use `d` to delete one.

**2 — USDA API key:** enter your personal FoodData Central API key. Type `s` to display the currently stored key. A personal key gives you a much higher search rate limit than the shared DEMO_KEY fallback. Getting a free key takes about a minute — instructions are in the [Food data](#food-data) section.

**3 — Storage location:** displays the full path to your NutriMagnus database file (`numa.db`). This is read-only; the path is set automatically when the program first runs and cannot be changed here.

---

### Getting missing amino acid data into your cache

Many foods in the USDA database — particularly branded products and older SR Legacy entries — have complete macronutrient data but no amino acid values. NutriMagnus marks these with ✗ in the AA column of the Food Cache list. Without amino acid data, protein completeness scores and the meal-level DIAAS calculation cannot include that food. There are two ways to fill the gap.

---

#### Method 1 — Ask Claude AI (the interactive workflow)

This is the built-in route, available directly inside NutriMagnus. It takes about two minutes per batch of foods and requires only a free claude.ai account. For a compact in-program reminder of these steps, see [amino acid fetch workflow](#fetch) from the Food Cache screen.

**Where to find it:** Foods → 5. View cached / saved foods. The `i` and `r` commands appear in the option list below the food table.

**Step 1 — Generate the prompt.**

From the Food Cache list, type `i` followed immediately by the row number(s) you want data for:

    i30           one food (row 30)
    i30,67        two foods (rows 30 and 67)
    i             every food in the current list that shows ✗

NutriMagnus builds a detailed data-request prompt and saves it to:

    ~/claude_prompt.txt

(The `~` means your home folder — the same folder that contains Documents, Desktop, etc.) The program prints the file's full path and shows you the next steps.

**Step 2 — Send the prompt to Claude AI.**

Open `~/claude_prompt.txt` in any text editor and copy its entire contents. Then:

1. Go to **claude.ai** in your browser. A free account is sufficient.
2. Open a **brand-new chat** — do not reuse a previous chat window.
3. Paste the text you copied and press Enter or click Send.
4. Wait for Claude to finish. It will return one structured data block per food.

**Step 3 — Save Claude's reply.**

Copy only Claude's reply — not your original prompt, not the whole page.

The safest way:
- Click at the very beginning of Claude's reply text.
- Scroll to the absolute end of that reply.
- Shift-click to select everything Claude wrote.
- Copy (Ctrl+C or Cmd+C).

Do not use the copy button at the bottom of the chat window — that captures the entire conversation history, not just Claude's answer.

Open a plain-text editor (Notepad, gedit, TextEdit, nano, etc.), paste, and save the file as:

    ~/claude_response.txt

Overwrite any previous version of that file completely.

**Step 4 — Import the data.**

Return to NutriMagnus, go to Foods → 5. View cached / saved foods, and type `r`.

NutriMagnus reads the file, validates each food record, and shows you a review table — food name, calories, protein, and how many of the 11 amino acids were found. You confirm before anything is written. After a successful import the food's AA column changes from ✗ to ✓.

Any explanatory notes or caveats that Claude added after the data are saved automatically as curator notes, visible with `n#` in the cache list.

**Re-running is safe.** You can run this workflow again at any time to update a food's data or add notes you missed. The import overwrites the existing entry.

---

#### Method 2 — The `import_foods.py` script (for permanent, curated records)

If you have sourced nutrient data directly from published literature — amino acid assay papers, authoritative food composition tables, or similar — and you want those figures to stay in your cache permanently, use `import_foods.py` instead of the Claude workflow.

This is a Python script in the NutriMagnus project folder. You add food records directly to its `_FOODS` list (each record is a Python dict with the food's name, FDC ID, data type, and nutrient values), then run:

    python import_foods.py

All records in the list are written into your cache immediately. The script marks each imported food as user-protected, so NutriMagnus will never silently overwrite the data with a fresh copy from USDA — even if you search for that food again later. Re-running the script is always safe: existing entries are updated in place, not duplicated.

Use the Claude workflow for exploratory or one-off data gathering where interactive review is helpful. Use `import_foods.py` for stable, permanently-needed records that you have verified from primary sources.

---

### Entering custom foods and dietary supplements [custom-foods]

#### Custom (drafted) food profiles

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

#### Dietary supplements — tablets, capsules, softgels

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

### How NutriMagnus scores meal and recipe protein quality [protein-scoring]

(This section explains the meal-level method. For background on single-food DIAAS and how amino acid ratios work, see [Appendix A](#appendix-a).)

Single-food analysis and meal-level analysis use different methods. For a single food, NutriMagnus computes a DIAAS score directly from that food's amino acid profile and digestibility. For a recipe or logged meal, it uses the FAO's endorsed method for mixed-food meals: it pools the digestible amino acids across all ingredients before scoring. The two approaches answer different questions and will give different results.

#### Why meals need their own calculation

A food that is short in one amino acid can be rescued by a companion food that supplies it generously — but only if you account for both foods together. A calculation that scores each food separately and then averages the scores misses this complementarity. The pooled method captures it correctly: amino acids from every ingredient in the meal are counted together before any ratio is computed.

#### The method, step by step

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

#### From DIAAS to digestible complete protein

    Digestible complete protein (g) = total meal protein (g) × min(DIAAS, 1.0)

If a meal contains 40 g of total protein and a DIAAS of 0.82, NutriMagnus reports 32.8 g of digestible complete protein. The remaining 7.2 g cannot be efficiently incorporated into tissue — the limiting amino acid is exhausted before the rest of the protein can be used.

#### A worked example — two ingredients, two amino acids

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

#### A note about missing amino acid data

Not every food in the USDA database has a complete amino acid profile. When an ingredient is missing that data, NutriMagnus runs the meal-level DIAAS calculation using only the ingredients for which data exists, and flags the result as an estimate. The digestible complete protein figure is then computed against only the protein that comes from those data-complete ingredients — so the result remains meaningful rather than artificially inflated.

##### Filling missing AA profiles at analysis time

When a meal contains ingredients without amino acid data, NutriMagnus tells you how many are affected and distinguishes two situations:

- **Inside a recipe**: the ingredient is part of a recipe you logged as a meal item. Fix these by editing the recipe directly (Recipes → browse → edit ingredients) and replacing or re-fetching the ingredient there.
- **Standalone meal ingredients**: foods you logged directly to the meal (not inside a recipe). These can be replaced on the spot: NutriMagnus asks whether you want to search for a substitute.

If you say yes, for each affected ingredient the program opens a focused search of USDA SR Legacy and Foundation foods — the datasets most likely to include full amino acid profiles. The **AA** column in the results (✓ or ✗) shows at a glance which options have the data you need. Choosing a replacement updates that ingredient for the current analysis. Press Enter to skip an ingredient and leave it excluded from the calculation.

##### Why the first analysis of a meal can be slow

When you analyze a meal for the first time, you may see a "Fetching amino acid data…" message with a brief wait — sometimes several seconds. This is normal. NutriMagnus is going online to download complete amino acid information for each food in the meal that doesn't already have it saved locally. Once downloaded, the data is stored on your computer, so the next time you analyze the same meal it will be fast.

---

### *Troubleshooting and feedback — reporting problems and offering ideas {: #feedback}

(Under development)

#### The program crashes unexpectedly


#### You don't understand how to respond to a prompt


#### You know what you want to do but can't see how to do it


#### How to contact help

Do not be reluctant in any way to do this. When you're having a problem the cause most like is NOT you! So, contacting us gives us essential information needed to make things better for you and also for every other user. We very much want to hear from you if you have a problem.

1. Text Tom at 435-272-3332. Plainly state that you are having a problem with the program. A brief statement of the problem is all I need. With your phone number I can call you back and get complete details of what I need to know to resolve your problem. I will generally call you back immediately. If a better time is available, let me know.

2. For non-urgent problems - which generally are improvements you'd like to see - you can also email me. Provide screenshots, if you think that would help. ALWAYS TEXT ME IF YOU SEND AN EMAIL, as I do not check my email daily, and yours easily can get lost in the 100s I get every day.

---

## Part 4 — Essential resources

---

### Food data — where it comes from and how it is stored [food-data]

**Two large online tables** are NutriMagnus's primary sources of food information:

- **USDA FoodData Central** — the U.S. government's nutrition database, covering hundreds of thousands of whole foods, ingredients, and branded products. This is NutriMagnus's primary source. ([FoodData Central FAQ](https://fdc.nal.usda.gov/faq/))
- **Open Food Facts** — a community-maintained database of packaged and processed food products, especially useful for branded items not found in the USDA table. ([Open Food Facts](https://world.openfoodfacts.org/discover))

**USDA API key.** NutriMagnus accesses FoodData Central through USDA's public API. Without a personal key it falls back to a shared demonstration key (DEMO_KEY) that has a tight rate limit — heavy use by any user can exhaust it and cause searches to fail temporarily. Getting your own key is free and takes about a minute:

1. Go to https://fdc.nal.usda.gov/api-key-signup and enter your name and email.
2. USDA emails you a key immediately.
3. Enter it in NutriMagnus under **Settings → Advanced settings → USDA API key**. Type **s** at that prompt to display your current key if you need to retrieve it.

Your key is stored on your computer only. Once set, all food searches use your personal key with a much higher rate limit.

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

### Glossary [glossary]

Abbreviations and key terms used in NutriMagnus output and this manual.

---

**AA**  —  Amino acid. The molecular building blocks of all proteins. See [essential amino acids](#aa).

**AI**  —  Adequate Intake.

**Antinutrient**  —  A naturally occurring plant compound that partially blocks the absorption or use of a nutrient. Common examples: phytates (reduce mineral absorption), oxalates (reduce calcium absorption), lectins (interfere with digestion in raw legumes), bound niacin in corn. All can be reduced by appropriate preparation. See [antinutrients](#antinutrients). A nutrient reference value used when a full RDA cannot be established; considered sufficient for most healthy people. Used for fiber in NutriMagnus. See [RDA](#rda).

**Bioavailable protein**  —  Protein the body can actually absorb and use, accounting for both digestibility and amino acid completeness. More meaningful than the raw protein figure on a nutrition label.

**CGM**  —  Continuous Glucose Monitoring. A wearable device that measures blood glucose every few minutes. Discussed in [Appendix B](#appendix-b) as the most accurate way to track individual glycemic response.

**CLI**  —  Command-Line Interface. A text-based program you operate by typing commands and reading text output. NutriMagnus currently runs as a CLI; a graphical interface (GUI) is planned for a future phase.

**Complete protein**  —  A protein source that supplies all nine essential amino acids at or above FAO reference levels after digestibility adjustment. See [protein completeness](#complete).

**Complement food**  —  A food added to a meal specifically to supply the amino acids that other ingredients are short in. See [complement suggestions](#comp).

**DCP**  —  Digestible Complete Protein. Grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (all essential amino acids present at adequate levels). See [digestible complete protein](#dcp).

**DIAAS**  —  Digestible Indispensable Amino Acid Score. A score from 0 to 1.5+ measuring how much of a food's protein the body can actually use, accounting for digestibility and amino acid completeness. 1.0 = meets the FAO reference exactly; above 1.0 = excellent; below 1.0 = one or more amino acids are limiting. See [DIAAS](#diaas).

**Digestibility coefficient**  —  A number between 0 and 1 representing the fraction of a nutrient that reaches the bloodstream after digestion. NutriMagnus uses true ileal digestibility values from published literature. Eggs and dairy sit near 1.0; whole legumes are typically 0.79–0.85.

**DRI**  —  Dietary Reference Intakes. The system of nutritional reference values published by the U.S. National Academies of Sciences; the source for RDAs, AIs, and upper intake levels used in NutriMagnus.

**EAA**  —  Essential Amino Acid. One of nine amino acids the human body cannot make and must get from food every day: Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine. See [essential amino acids](#aa).

**FAO**  —  Food and Agriculture Organization of the United Nations. The body that published the 2013 amino acid reference standard used for all protein quality scoring in NutriMagnus. See [FAO reference values](#fao).

**FDC**  —  FoodData Central. The USDA's online nutrition database and NutriMagnus's primary food data source. Each food has a unique numeric FDC ID. Website: https://fdc.nal.usda.gov/

**FDC ID**  —  The unique numeric identifier assigned to each food entry in USDA FoodData Central. You can enter an FDC ID directly at any "Search food or recipe" prompt instead of typing a name.

**Food Cache**  —  Your local database of previously retrieved foods. Searching the cache is instant (no network required); foods are added automatically when you select them from USDA or Open Food Facts results.

**Food Annotation**  —  Extra information you attach to a cached food: glycemic index, a DIAAS estimate, or a preparation note. Stored locally; not part of any online database.

**GI**  —  Glycemic Index. A scale from 0 to 100 measuring how quickly a food raises blood glucose relative to pure glucose (100). See [glycemic index](#gi).

**GL**  —  Glycemic Load. A measure of glycemic impact that combines GI with the actual amount of carbohydrate in a serving. More useful than GI alone for real-world meal comparisons. See [glycemic load](#gl).

**GUI**  —  Graphical User Interface. A visual, point-and-click interface. Planned for a future phase of NutriMagnus; the CLI will remain available.

**Ileal digestibility**  —  The fraction of an amino acid absorbed by the end of the small intestine (ileum). DIAAS uses true ileal digestibility, which is more accurate than fecal digestibility for measuring protein available to the body.

**Limiting amino acid**  —  The essential amino acid in shortest supply relative to the FAO reference, which caps how much of a food's protein can be incorporated into tissue. The overall DIAAS score equals the ratio for the limiting amino acid. See [limiting amino acid](#gap).

**Met+Cys**  —  Methionine + Cystine. These two amino acids are scored as a combined pair in DIAAS calculations, following FAO 2013 guidelines, because the body can convert Methionine into Cystine.

**My Pantry**  —  A personal list of protein sources you currently have on hand. NutriMagnus checks this list first when suggesting complement foods, so suggestions reflect what you can actually use.

**NuMa**  —  NutriMagnus. The abbreviated name used throughout this manual.

**OFF**  —  Open Food Facts. A community-maintained database of packaged and branded food products; NutriMagnus's secondary data source. Website: https://world.openfoodfacts.org/

**Oxalate**  —  A naturally occurring compound (oxalic acid / oxalate ion) found in many plant foods, especially spinach, beets, nuts, and chocolate. At high dietary levels it can promote calcium-oxalate kidney stones in susceptible individuals. NutriMagnus can optionally display oxalate content using the Harvard T.H. Chan School of Public Health reference table. Enable it under Settings → Oxalate data. See [oxalate data](#oxalate).

**Phe+Tyr**  —  Phenylalanine + Tyrosine. Scored as a combined pair in DIAAS calculations because the body can convert Phenylalanine into Tyrosine.

**Phytonutrients**  —  Plant-derived bioactive compounds tracked by NutriMagnus where USDA data exists: beta-carotene, alpha-carotene, lycopene, lutein/zeaxanthin, choline, beta-sitosterol, and isoflavones.

**Pooled DIAAS**  —  The meal-level protein quality score computed by summing digestible amino acids across all ingredients before scoring. This captures how foods complement each other in a way that single-food DIAAS cannot. See the section "How NutriMagnus scores meal and recipe protein quality."

**RDA**  —  Recommended Dietary Allowance. The average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group. See [RDA](#rda).

**SPI**  —  Soy Protein Isolate. A concentrated plant protein (95%+ protein by weight) with high digestibility (0.95); frequently cited in complement suggestions. See [Appendix E](#comp-appendix).

**TID** —  

**USDA**  —  United States Department of Agriculture. The U.S. government body that publishes FoodData Central, NutriMagnus's primary food data source.

**usr**  —  User-drafted. Appears in ingredient ID columns to indicate a food whose nutrient profile you created or edited by hand, rather than one retrieved from USDA or Open Food Facts.

### Internet resources

Under development.

---

## Part 5 — Appendices

---

### Appendix A: Raw protein, protein quality, and protein digestibility [appendix-a]

#### The core problems with protein

When you eat protein, not all of it is equally useful to your body. The usefulness depends on three things: **how much** protein you eat, and **how well-matched** its amino acid composition is to human physiological needs, and **how digestible** it is. 

#### The Nine Essential Amino Acids and their required relationship

Your body requires twenty amino acids to build proteins. Eleven of these it can synthesize from other raw materials. The remaining nine — the essential amino acids (EAAs) — must come from food. 

These nine must all be present simultaneously for protein synthesis to proceed. They must also be present in the right amount. If any one of them is insufficiently supplied, then to the degree that its amount is short the other cannot be used. The surplus of the other eight cannot be stored and is instead broken down for energy — a functional waste.

In summary, the *pattern* of EAAs in a food matters, not just the total protein quantity.

#### The required EAA pattern, established by the FAO

The Food and Agriculture Organization (FAO) of the United Nations leads international efforts to defeat hunger, achieve food security for all, and make sure that people have regular access to enough high-quality food to lead active, healthy lives.

Research has established human requirements for each EAA independently, through controlled human trials. For each amino acid separately, researchers determined how much a healthy adult needs per day to maintain physiological function. From these studies came absolute daily requirement figures for each of the nine EAAs, expressed in milligrams per kilogram of body weight per day.

Separately, research has established how much total protein a healthy adult needs per day. By dividing each EAA's daily requirement by the total daily protein requirement, researchers produced a normalized figure: how many milligrams of each EAA a person needs per gram of protein consumed. These normalized figures are the **FAO reference values**.

From the reference values for each amino acid which were determined *independently* come the ratios between EAAs. The reference values' relationship are a byproduct of the separately established requirements — not the starting point.

#### The FAO reference values tell you about the quality of protein in a food

The reference values allow a simple and powerful question to be asked about any food protein source:

> If I eat enough of this food to meet my total daily protein needs, will each essential amino acid also arrive in sufficient quantity?

If the answer is yes for all nine EAAs, the protein is high quality — no bottleneck will limit your body's ability to use it. If the answer is no for even one EAA, that amino acid becomes your limiting factor.

#### How the Ratio Is Calculated in NuMa

For each essential amino acid, the ratio shown in NuMa's output is computed in two steps:

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

#### Why Total Protein Is the Denominator

A reasonable question is why the ratio uses total protein (including non-essential amino acids) as its denominator rather than comparing EAA amounts in absolute terms.

Total protein is a normalizing device — **a common scale that makes the quality metric meaningful across foods with very different protein concentrations and very different serving sizes.**

The practical interpretation is direct: **if a food's protein clears all nine floors, eating enough of that food to meet your daily protein target will automatically also deliver your daily EAA requirements.** No separate EAA accounting is needed. A food that fails even one floor means you would reach your protein target before accumulating enough of that EAA — the protein source is insufficient on its own.

The non-essential amino acids that make up the rest of the protein are biologically irrelevant to this specific calculation. They appear in the denominator only because total protein is the natural unit for expressing protein intake. They are not required to "activate" the EAAs — they are simply passengers.

#### What "Complete" Actually Means

"Complete" does not mean the amino acid ratios are all close to 1.0, or close to each other. It means **every one of the nine ratios is at or above 1.0** — each amino acid clears its own independent floor.

The nine FAO reference values were determined in separate human trials, one amino acid at a time. They are not ratios between amino acids; they are nine independent thresholds. Having tryptophan at 2.14× its floor while Met+Cys sits at 1.02× its floor creates no imbalance — the tryptophan surplus cannot compensate for a deficit in another amino acid, but it does not create one either.

A food can therefore have wildly varying ratios across its amino acids and still be complete. Cocoa's protein ranges from 1.02 to 2.25 across the nine amino acids — a factor of more than two between the lowest and highest — and is still complete because nothing falls below 1.0.

The floor analogy: imagine a building with nine rooms, each with its own minimum ceiling height requirement. A room that comfortably exceeds its requirement does not help or hurt any other room. Every room must pass independently.

#### The Limiting Amino Acid — A Practical Analogy

When any one EAA ratio falls below 1.0, that amino acid is "limiting" — it acts as a bottleneck that caps how much protein your body can fully incorporate into tissue.

A concrete analogy: you are mixing mortar to build a small wall. You have plenty of dry mix but run out of water before you have mixed enough for the full job. Without water, the remaining dry mix is unusable — you can build only 90 bricks worth of wall instead of 150. The water is your limiting amino acid. The unused dry mix is the protein your body cannot build into tissue, and instead breaks down and excretes.

Complementary proteins work by pooling the limiting amino acids from multiple foods — a grain that is low in lysine paired with a legume that is rich in lysine can together clear all nine floors even though neither does so alone.

#### The DIAAS Score

The Digestible Indispensable Amino Acid Score (DIAAS) assesses the degree to which a food protein can actually be accessed puts this question into by our body. For each EAA, it calculates:

> (mg of that EAA actually absorbed per gram of food protein) ÷ (FAO reference value for that EAA)

The word "actually absorbed" is critical. Not all amino acids in a food survive digestion intact and cross into the bloodstream. DIAAS uses ileal digestibility — the fraction of each amino acid absorbed by the end of the small intestine — to correct for this. The result is a score based on what your body actually receives, not merely what was in the food.

A ratio of 1.0 means the food **delivers** exactly the required amount of that EAA (per gram of protein eaten). A ratio below 1.0 means a shortfall — that EAA is limiting. A ratio above 1.0 means a surplus above the floor. **The overall DIAAS score for the food is set by whichever EAA has the lowest ratio — the weakest link.**

#### A Concrete Example: Chia Seed

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

#### Summary

| Concept | What it answers |
|---|---|
| FAO reference values | How many mg of each EAA a human needs per gram of protein consumed |
| DIAAS ratio for one EAA | Does this food deliver enough of that EAA, accounting for digestibility? |
| Overall DIAAS score | What is the weakest link — the most limiting EAA in this food? |
| Ratio > 1.0 for all EAAs | Complete protein: no bottleneck, full usability of what you eat |
| Daily protein target | Separate calculation: how many grams of protein do you need total? |

The DIAAS table characterizes the quality of each gram. Hitting your daily protein target is about counting how many grams you eat.

### Appendix B: Glycemic load (GL) and Blood Glucose Comparison [appendix-b]

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

#### Continuous Glucose Monitoring

The practical gold standard today is continuous glucose monitoring (CGM) —
devices such as the Dexterity G7 or Libre 3 that measure interstitial glucose
every few minutes. A person with diabetes can eat a meal, watch their glucose
curve in the accompanying app, and directly compare their own real response
across different meal choices over time. No formula approaches this for
accuracy in individual prediction.

#### Predictive Apps

Some applications (January AI, Levels) go a step further, using machine
learning models trained on large CGM datasets to predict glucose response to a
described meal before it is eaten — effectively personalising the GI and GL
concepts. These predictions are probabilistic rather than exact, but they
represent the closest available alternative to direct measurement.

#### Clinical Practice Without CGM

For clinical guidance without CGM, dietitians working with people with
diabetes typically use carbohydrate counting combined with qualitative
judgment about fat and protein content, rather than relying on GL as a
single summary figure. GL remains a reasonable guide for comparing meals
similar in structure, but should not be the deciding number when fat and
protein differ significantly between the options being considered.

### Appendix C: FAO 2013 Amino Acid Reference Values

Under development.

### Appendix D: Full Nutrient Key

Under development.

### Appendix E: Protein ingestion timing

To be researched.

Resources:

* https://runningmagazine.ca/health-nutrition/could-you-be-timing-your-protein-all-wrong/

### Appendix F: Meal timing

To be researched.

Resources:

* https://www.theguardian.com/commentisfree/2026/may/05/game-changer-good-health-scientists-we-are-when-we-eat - article by expert

### Appendix G: Why some foods appear only in DIAAS-boosting suggestions [comp-appendix]

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

### Appendix H: Portion Input Formats [portion-formats]

Every prompt that asks for a portion amount — in Foods, Recipes, Meals, and the Convert tool — accepts the same input formats.

NUMBERS

Plain decimals, fractions, and mixed numbers are all accepted:

    150        plain number
    0.5        decimal
    1/4        fraction
    1 1/2      mixed number (whole + fraction, separated by a space)

WEIGHT UNITS

    g  gr  gram  grams          grams  (1 g = 1 g)
    oz  ounce  ounces           ounces  (1 oz = 28.35 g)
    lb  lbs  pound  pounds      pounds  (1 lb = 453.6 g)
    kg  kilogram  kilograms     kilograms  (1 kg = 1000 g)

VOLUME UNITS

NutriMagnus converts volume to grams via the food's recorded density.
If density is unknown for a food, it asks you to supply the weight manually.

    c  cup  cups                cups  (1 c = 236.6 ml)
    T  tbsp  tablespoon  tablespoons    tablespoons  (1 T = 14.8 ml)
    t  tsp  teaspoon  teaspoons     teaspoons  (1 t = 4.9 ml)
    ml  milliliter  milliliters  cc   milliliters
    floz                         fluid ounces  (1 floz = 29.6 ml)
    l  liter  liters             liters  (1 l = 1000 ml)

Note: T (uppercase) means tablespoon; t (lowercase) means teaspoon.
These two are case-sensitive. All other units are case-insensitive.

PIECE / COUNT UNITS

    pc  pcs  piece  pieces  each  ea  count  ct  item  items

Piece entries record a count but no gram weight. The program will ask
you to confirm or supply a weight if it needs one for nutrient scaling.
Unlike weight and volume units, piece units require a space: "2 pc",
not "2pc".

USDA STANDARD PORTIONS

Many USDA foods include pre-defined portion sizes (e.g. "1 medium egg",
"1 cup sliced"). These are listed at the portion prompt and can be
selected by number:

    p1         select USDA portion #1
    p2         select USDA portion #2
    1.5 p1     one-and-a-half times USDA portion #1

OMITTING THE SPACE

For all weight and volume units, the space between the number and unit
is optional. These pairs are identical:

    2 T    =   2T
    0.25 c =   0.25c
    150 g  =   150g
    3 oz   =   3oz
    1/4 c  =   1/4c

(Piece units — pc, each, etc. — always require a space.)

VOLUME WITH EXPLICIT WEIGHT

When you know both the volume measure and the exact gram weight, you can
supply both on one line. NutriMagnus records the weight and labels the
entry with the volume for readability:

    2 T 30g         →  30 g  (labeled "30 g (2 T)")
    1/4 c 60 g      →  60 g  (labeled "60 g (1/4 c)")

BARE NUMBER

A bare number with no unit is assumed to be grams, but NutriMagnus
always asks for confirmation before storing it.

### Appendix I: Worked validation example — meal-level DIAAS for pinto beans + quinoa [appendix-i]

This appendix lets you verify NuMa's protein quality calculation independently. Every step is shown explicitly so you can reproduce it in a spreadsheet or calculator, then compare your result with what NuMa produces when you enter these two foods as a meal.

#### The two foods

| Food | FDC ID | Data type | USDA source |
|------|--------|-----------|-------------|
| Beans, pinto, mature seeds, cooked, boiled, with salt | 173796 | SR Legacy | https://fdc.nal.usda.gov/food-details/173796/nutrients |
| Quinoa, cooked | 168917 | SR Legacy | https://fdc.nal.usda.gov/food-details/168917/nutrients |

All nutrient values below are drawn directly from those pages as of June 2026. The demo uses **100 g of each food** — round numbers that make the arithmetic easy to follow.

---

#### Step 1 — Individual nutrient profiles (per 100 g, from USDA)

**Table I-1. Macronutrients and key micronutrients**

| Nutrient | Unit | Pinto beans (FDC 173796) | Quinoa (FDC 168917) |
|----------|------|------------------------:|--------------------:|
| Calories | kcal | 143.0 | 120.0 |
| Protein | g | 9.01 | 4.40 |
| Carbohydrate | g | 26.22 | 21.30 |
| Total fat | g | 0.65 | 1.92 |
| Fiber | g | 9.00 | 2.80 |
| Saturated fat | g | 0.109 | 0.231 |
| Monounsaturated fat | g | 0.106 | 0.528 |
| Polyunsaturated fat | g | 0.188 | 1.078 |
| Calcium | mg | 46.0 | 17.0 |
| Iron | mg | 2.09 | 1.49 |
| Magnesium | mg | 50.0 | 64.0 |
| Phosphorus | mg | 147.0 | 152.0 |
| Potassium | mg | 436.0 | 172.0 |
| Sodium | mg | 238.0 | 7.0 |
| Zinc | mg | 0.98 | 1.09 |
| Vitamin C | mg | 0.8 | 0.0 |
| Thiamin (B1) | mg | 0.193 | 0.107 |
| Riboflavin (B2) | mg | 0.062 | 0.110 |
| Niacin (B3) | mg | 0.318 | 0.412 |
| Vitamin B6 | mg | 0.229 | 0.123 |
| Folate | mcg | 172.0 | 42.0 |
| Vitamin E | mg | 0.94 | 0.63 |
| Vitamin K | mcg | 3.5 | 0.0 |
| Choline | mg | — | 23.0 |

**Table I-2. Indispensable amino acids (IAAs) per 100 g**

Amounts are in grams. Note that Met+Cys and Phe+Tyr are scored as *pairs* in the DIAAS methodology (see Step 3).

| Amino acid | Pinto beans | Quinoa |
|------------|------------:|-------:|
| Histidine | 0.232 | 0.127 |
| Isoleucine | 0.368 | 0.157 |
| Leucine | 0.664 | 0.261 |
| Lysine | 0.571 | 0.239 |
| Methionine | 0.126 | 0.096 |
| Cystine (pairs with Met) | 0.090 | 0.063 |
| Phenylalanine | 0.450 | 0.185 |
| Tyrosine (pairs with Phe) | 0.234 | 0.083 |
| Threonine | 0.350 | 0.131 |
| Tryptophan | 0.098 | 0.052 |
| Valine | 0.435 | 0.185 |

---

#### Step 2 — Pooled nutrients for the meal (100 g pinto + 100 g quinoa = 200 g total)

To pool, simply add the values from the two 100 g servings. The totals below represent the entire 200 g meal.

**Table I-3. Pooled macros and key micronutrients (200 g meal)**

| Nutrient | Pinto 100 g | Quinoa 100 g | Meal total |
|----------|------------:|-------------:|-----------:|
| Calories (kcal) | 143.0 | 120.0 | 263.0 |
| Protein (g) | 9.01 | 4.40 | **13.41** |
| Carbohydrate (g) | 26.22 | 21.30 | 47.52 |
| Total fat (g) | 0.65 | 1.92 | 2.57 |
| Fiber (g) | 9.00 | 2.80 | 11.80 |
| Calcium (mg) | 46.0 | 17.0 | 63.0 |
| Iron (mg) | 2.09 | 1.49 | 3.58 |
| Magnesium (mg) | 50.0 | 64.0 | 114.0 |
| Potassium (mg) | 436.0 | 172.0 | 608.0 |
| Folate (mcg) | 172.0 | 42.0 | 214.0 |

**Table I-4. Pooled IAA totals for the meal (g)**

| Amino acid | Pinto 100 g | Quinoa 100 g | Meal total |
|------------|------------:|-------------:|-----------:|
| Histidine | 0.232 | 0.127 | 0.359 |
| Isoleucine | 0.368 | 0.157 | 0.525 |
| Leucine | 0.664 | 0.261 | 0.925 |
| Lysine | 0.571 | 0.239 | 0.810 |
| Met + Cys | 0.126 + 0.090 = 0.216 | 0.096 + 0.063 = 0.159 | **0.375** |
| Phe + Tyr | 0.450 + 0.234 = 0.684 | 0.185 + 0.083 = 0.268 | **0.952** |
| Threonine | 0.350 | 0.131 | 0.481 |
| Tryptophan | 0.098 | 0.052 | 0.150 |
| Valine | 0.435 | 0.185 | 0.620 |

---

#### Step 3 — Applying digestibility to get digestible IAA amounts

Raw amino acid values from USDA are not all absorbed. The DIAAS methodology requires multiplying each food's IAA amounts by that food's *true ileal digestibility coefficient* — a value between 0 and 1 representing the fraction of each IAA that actually reaches the bloodstream.

NuMa's digestibility values come from the FAO 2013 report and published literature. For these two foods:

| Food | Digestibility coefficient | Source |
|------|:------------------------:|--------|
| Pinto beans | **0.80** | FAO Food and Nutrition Paper 92 (2013) |
| Quinoa | **0.85** | Mathai et al. (2017), *British Journal of Nutrition* |

To apply: multiply each food's IAA total by its coefficient. For example, for pinto beans' leucine: 0.664 × 0.80 = 0.531 g digestible leucine.

**Table I-5. Digestible IAA amounts per food (g)**

| Amino acid | Pinto × 0.80 | Quinoa × 0.85 | Pooled digestible |
|------------|-------------:|--------------:|------------------:|
| Histidine | 0.232 × 0.80 = **0.18560** | 0.127 × 0.85 = **0.10795** | **0.29355** |
| Isoleucine | 0.368 × 0.80 = **0.29440** | 0.157 × 0.85 = **0.13345** | **0.42785** |
| Leucine | 0.664 × 0.80 = **0.53120** | 0.261 × 0.85 = **0.22185** | **0.75305** |
| Lysine | 0.571 × 0.80 = **0.45680** | 0.239 × 0.85 = **0.20315** | **0.65995** |
| Met+Cys | 0.216 × 0.80 = **0.17280** | 0.159 × 0.85 = **0.13515** | **0.30795** |
| Phe+Tyr | 0.684 × 0.80 = **0.54720** | 0.268 × 0.85 = **0.22780** | **0.77500** |
| Threonine | 0.350 × 0.80 = **0.28000** | 0.131 × 0.85 = **0.11135** | **0.39135** |
| Tryptophan | 0.098 × 0.80 = **0.07840** | 0.052 × 0.85 = **0.04420** | **0.12260** |
| Valine | 0.435 × 0.80 = **0.34800** | 0.185 × 0.85 = **0.15725** | **0.50525** |

---

#### Step 4 — The FAO reference amounts for this meal

The DIAAS method scores each pooled digestible IAA against how much of that IAA a *reference protein* of equal weight would provide. The reference values, from FAO Food and Nutrition Paper 92 (2013), Table 6, are expressed in **mg of IAA per gram of total protein** for older children, adolescents, and adults.

The full table is in Appendix C of this manual. The relevant values are:

| IAA | FAO reference (mg/g protein) |
|-----|-----------------------------:|
| Histidine | 16.0 |
| Isoleucine | 30.0 |
| Leucine | 61.0 |
| Lysine | 48.0 |
| Met+Cys | 23.0 |
| Phe+Tyr | 41.0 |
| Threonine | 25.0 |
| Tryptophan | 6.6 |
| Valine | 40.0 |

The meal contains **13.41 g total protein** (9.01 + 4.40). To find how many grams of each IAA the reference protein provides for this amount of protein, multiply:

    Reference amount (g) = FAO value (mg/g) × 13.41 (g protein) ÷ 1000

**Table I-6. FAO reference IAA amounts for 13.41 g protein**

| IAA | FAO (mg/g) | Calculation | Reference (g) |
|-----|----------:|-------------|-------------:|
| Histidine | 16.0 | 16.0 × 13.41 ÷ 1000 | 0.21456 |
| Isoleucine | 30.0 | 30.0 × 13.41 ÷ 1000 | 0.40230 |
| Leucine | 61.0 | 61.0 × 13.41 ÷ 1000 | 0.81801 |
| Lysine | 48.0 | 48.0 × 13.41 ÷ 1000 | 0.64368 |
| Met+Cys | 23.0 | 23.0 × 13.41 ÷ 1000 | 0.30843 |
| Phe+Tyr | 41.0 | 41.0 × 13.41 ÷ 1000 | 0.54981 |
| Threonine | 25.0 | 25.0 × 13.41 ÷ 1000 | 0.33525 |
| Tryptophan | 6.6 | 6.6 × 13.41 ÷ 1000 | 0.08851 |
| Valine | 40.0 | 40.0 × 13.41 ÷ 1000 | 0.53640 |

---

#### Step 5 — IAA ratios and the composite DIAAS score

For each IAA, divide the pooled digestible amount (from Table I-5) by the reference amount (from Table I-6). The result is a ratio: a value ≥ 1.0 means the meal meets or exceeds the reference for that IAA; below 1.0 means it falls short.

    Ratio = pooled digestible IAA (g) ÷ FAO reference IAA (g)

**Table I-7. IAA ratios vs. FAO reference**

| IAA | Pooled dig. (g) | Reference (g) | Ratio | Meets reference? |
|-----|----------------:|--------------:|------:|:----------------:|
| Histidine | 0.29355 | 0.21456 | 1.368 | Yes |
| Isoleucine | 0.42785 | 0.40230 | 1.063 | Yes |
| **Leucine** | **0.75305** | **0.81801** | **0.921** | **No — limiting** |
| Lysine | 0.65995 | 0.64368 | 1.025 | Yes |
| Met+Cys | 0.30795 | 0.30843 | 0.998 | Marginal (99.8%) |
| Phe+Tyr | 0.77500 | 0.54981 | 1.410 | Yes |
| Threonine | 0.39135 | 0.33525 | 1.167 | Yes |
| Tryptophan | 0.12260 | 0.08851 | 1.385 | Yes |
| Valine | 0.50525 | 0.53640 | 0.942 | No |

The **composite DIAAS score is the lowest ratio** — the *limiting* amino acid determines the ceiling for all the others, because when one IAA runs out, the others cannot be used for protein synthesis.

    Composite DIAAS = min(all ratios) = 0.921   (limited by Leucine)

A DIAAS of 0.921 means this meal delivers about 92% of the protein quality of a reference protein. It also means the **digestible complete protein** for this 200 g meal is:

    DCP = 13.41 g × min(0.921, 1.0) = 12.35 g

---

#### Step 6 — Interpreting the result

A composite DIAAS ≥ 1.0 means the meal's protein is fully complete relative to the FAO reference. Values below 1.0 indicate partial completeness — the lower the value, the more the limiting amino acid constrains usable protein.

For this meal:

- **Leucine** is the limiting IAA at 0.921. This is not surprising: leucine is the most abundant IAA in animal proteins, but plant proteins generally provide less of it relative to total protein.
- **Valine** is also below reference at 0.942. The combination of one legume and one pseudo-cereal improves but does not fully resolve either gap.
- **Lysine**, which is the classic weak point of grains, is met here (1.025) — the pinto beans contribute the lysine that quinoa alone would not cover.
- **Met+Cys** is nearly exactly met at 0.998 — essentially at the reference.

The DCP of 12.35 g from 13.41 g of raw protein means that roughly 1.06 g of protein per meal is rendered non-contributory by the leucine shortfall. In practical terms, this is a high-quality plant-protein meal — DIAAS above 0.9 is considered "good quality" by the FAO.

---

#### Step 7 — Reproduce this in NuMa and compare

To run the same analysis in NuMa:

1. From the main menu, select **Meals & Log**.
2. Create a new meal and add two foods:
   - Search for **pinto beans cooked** → select FDC 173796
     ("Beans, pinto, mature seeds, cooked, boiled, with salt")
   - Enter a portion of **100 g**
   - Add a second food: search for **quinoa cooked** → select FDC 168917
     ("Quinoa, cooked")
   - Enter a portion of **100 g**
3. Save the meal, then open it and select **View nutrition analysis**.
4. In the analysis screen, scroll to the **Protein quality** section.

NuMa will display:
- Total protein
- Composite DIAAS score
- Digestible complete protein (DCP)
- A per-IAA ratio table identifying the limiting amino acid

Compare the values NuMa shows with those in Table I-7 above. They should match to at least three significant figures. If they do not, please report the discrepancy at the project issue tracker.

---

### Notes

[^1]: Lippman, D., Stump, M., Veazey, E., Guimarães, S. T., Rosenfeld, R., Kelly, J. H., Ornish, D., & Katz, D. L. (2024). Foundations of Lifestyle Medicine and its Evolution. *Mayo Clinic Proceedings: Innovations, Quality & Outcomes, 8(1)*, 97–111. https://doi.org/10.1016/j.mayocpiqo.2023.11.004

[^2]: U.S. Department of Agriculture, Agricultural Research Service. (2019). *FoodData Central*. https://fdc.nal.usda.gov/

[^3]: Open Food Facts contributors. (2012). *Open Food Facts*. https://world.openfoodfacts.org/
