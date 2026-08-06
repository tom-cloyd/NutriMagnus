# NutriMagnus User Manual

*Updated 2026-08-06:0734* / Reading time: 2 hours, 22 minutes

**NutriMagnus ("NuMa")** is an open-source computer program which provides nutritional information essential to making good food choices. [NuMa](#gloss-numa) gives a thorough analysis of the nutritional aspects of a user's food choices, with particular emphasis on protein because this is a problem for those eating primarily a plant-based diet, for older people, and for the chronically-ill.

**Eating is fundamentally about survival- all life's first priority, for we must constantly support and replace the cells in our body.** Most of the cells in our body persist for a shorter period than we do. During their lifespan they do their work using materials available to them in their immediate environment. Eventually they must be replaced by new cells, constructed again from such available materials.

**Cellular support and replacement depends upon our accessing essential materials, through eating.** While significant essential materials may already exist in the local environment of a cell, the rest have to come from elsewhere, and ultimately that means from outside our bodies. For this reason we must eat.

**Eating usually involves making choices, and good choice requires good information.** The three major problems impeding good food choice are a) lack of awareness of the choices available, and b) lack of information about the nutritional character of those choices, and c) lack of information as to what constitutes a good choice. All of these problems are addressed by the general domain of nutrition science. [NuMa](#gloss-numa) takes up these problems, in detail.

**Both the program and its accompanying *User Manual* are an ongoing project.** They are modified frequently. Both are already quite sophisticated, but new versions will be made available quickly for those already using the program. However, the manual has not yet received a careful editorial review; it is an advanced first draft.

**User feedback is highly valued, so please give us yours!** What many software users don't realize is that with programs in active development ANY feedback is appreciated and most likely useful. User experience with the program is a critical measure of program success or failure. So, please email all problems, thoughts, and ideas to [tomcloydmsma@gmail.com](mailto:tomcloydmsma@gmail.com). Put `NutriMagnus` or `NuMa` in the subject line, please!

**How to come up with feedback:** First, ANY thoughts you wish to share are welcome. We know what is useful to us, but can't react at all if you don't share. If in doubt, just do it! We'll be grateful. Of particular interest to us are these topics:

1. Inconveniences: you notice that something seems a bit difficult to do, or you see a simpler or quicker way to do it.
2. Missing or incomplete information: Sometimes updates and changes do not go out to every part of the program as they should, and you see a gap in the information provided.
3. Outright nonsense: you look at program output and think "that can't be right" or maybe you just feel doubtful about it.

User-derived issues get immediate priority in the program-development process!

---

## How to read this Manual

NuMa runs as a web app, opened in your ordinary browser — there is nothing to install and no command line involved.

- Read **Part 1** (Introduction) and **Part 2** (Core nutrition concepts) for the ideas behind the program.
- Read **Part 3** (Reading Your Results) whenever you want to know what a column or table means.
- Read **Part 4** (Shared Operations) for behaviors that show up in more than one place in the app, explained once.
- Read **Part 5 — Using the Web App** for how to actually operate NuMa.
- Parts 6 to 9 apply to everyone.

## To get a quick start:

### A. Start with what's easiest

This is a complex, powerful analytical program. A careful Internet search reveals that it is unique in its power and depth. It can be successfully approached by moving slowly and thoughtfully, with real benefit obtained from using some of its easiest and simplest features. 

Start with what is easiest to understand: analysis of single foods and simple recipes. Use the manual to learn more. Do not expect to learn it all in a few sessions. [Contact us](#feedback) quickly rather than slowly if you start to get overwhelmed — one of our goals is to minimize the risk of that happening!

### B. Use a kitchen scale to determine food quantities, if at all possible

You will have to tell the program WHAT you are eating and HOW MUCH. The absolute best way to do this is to give it a weight. Sometimes you can just give it a "portion" or a volume measure instead, and the program will figure out the weight for you from that so it can keep going. Remember that approximations are better than nothing.

Without the program you're flying blind. With it, even if you only use volume measures, there will be some errors of measurement, but you're still much better informed about what's happening than before. In some cases, though, a volume measure just doesn't work well. If that happens to you, [get in touch](#feedback) and we'll figure it out together. All in all, it's by far best to have and use a kitchen scale. I have had a small Oxo scale for years. It's excellent. There are others you can consider as well, but I do suggest that you get one.

### A. Download and install the program

Under development.

[//]: # "develop section"

### B. Go to Settings and do this:

a. Go to Settings and set up your personal profile, if you want the program to immediately apply to you. 
b. Set up your Pantry foods as available primary protein sources: Go to Appendix C below and review the listed foods. Some you will likely have. The others you should consider buying if you're serious about making plant protein sources your sole or primary protein concern.

### C. Skim Part 1, A and F, just to know they exist.

While looking at section A, make a few notes about what you'd like to try first.

Seriously consider what is suggested in section F - looking at the workflows can quickly show you major program features.

### D. Consider investing some time with Part 2

This program necessarily uses some specialized vocabulary. You have two options:

1. Learn the basics before diving into the program's functions and output.
2. Dive in first, and use the "Learn more..." links you'll see to immediately jump to the relevant manual section, so you can understand whatever's in front of you right when you need to.

---

## Part 1 — Introduction to NutriMagnus, a tool for intelligent eating: what you can do with this tool and why it matters

---

### A. What a user can do with NutriMagnus — brief overview

The five items in the top navigation bar correspond to the five major things you can do with the program:

- **Foods** — Search the [USDA](#gloss-usda) and Open Food Facts[^3] databases; analyze the nutrients in a specific portion of any food or recipe; compare up to eight foods side-by-side; manage your personal [Food Cache](#gloss-food-cache), Pantry, and custom food profiles; annotate foods with glycemic index and [DIAAS](#gloss-diaas) estimates.
- **Recipes** — Create and save recipes with ingredients and instructions; browse, copy, and delete saved recipes; develop a recipe iteratively with nutritional feedback after each ingredient change; analyze a recipe portion for full nutrient data, protein quality, and complement suggestions.
- **Meals & Log** — Record what you eat by date; add foods and recipes to meals; analyze individual meals or the combined total for a full day; search your entire meal history for any food.
- **Analysis** — A growing set of preset analyses. **Daily summary - [DCP](#gloss-dcp) and goals**: combined nutrient totals for today or any past date, compared against personalized [RDA](#gloss-rda) targets, plus a list of recent days with meals. **Food use in meals**: rank which foods were used across a chosen set of date ranges and/or meals, with a frequency histogram.
- **Settings** — Set your color theme, personal profile (age, sex, weight, height, activity level), dietary preferences, editor command, and advanced options including your personal [USDA](#gloss-usda) [API key](#food-data) (a free code from USDA's website that raises how many food searches you can do) and protein digestibility overrides.

**Detailed how-to guides for each menu area follow later in this manual.** If you prefer to learn by example before reading explanations, skip ahead to [Sample Workflows](#sample-workflows) at the end of this introduction — it points you to a set of annotated walkthroughs.

### B. NutriMagnus addresses two serious problems

Thoughtful diet management requires trustworthy, specific data that is only to be found in research report summaries. Both access and use of this data requires use of computers. 

Managing specific dietary problems presents even greater challenges. One such specific problem is management of protein intake in vegetarian and vegan diets, especially when a person is no longer young. NuMa is particularly suitable for management of this problem, but can address others as well, focusing on oxalate consumption, need for vitamins and or minerals, phytonutrient tracking, and more. 

**Diet matters.** It is now well established that the crucial factors affecting physical and mental health are diet, sleep, exercise, social engagement, stress management, and avoidance of injurious and risky substances. Their relationships are complex and interacting. Relative to diet, research supports an emphasis on a "plant-predominant eating pattern". [^1] The fortunate thing about diet is that is something we act on immediately and effectively - but only if we have the information needed to make good choices.

**Plant-based diets are preferable.** There are multiple good reasons to focus on eating foods derived from plants rather than animals. Plant-based proteins are far less ecologically damaging to produce than animal protein and also much less likely to acquire agricultural chemical accumulations, which are then ingested along with the nutrients they contain. They also do not involve the industrialized abuse of vast numbers of animals who live only long enough to produce edible protein and then are treated like a mere object to be processed as we might a fallen tree. 

Plant proteins are usually more affordable and easier to ship and store for long periods. Most of the world, and most humanity throughout human history, eats and has eaten a plant-predominant diet, so this is simply not a novel idea.

**Plant-based proteins require special management.** But almost all plant proteins come to us with a built-in problem: incomplete amino acid composition. When you read on your jar of peanut butter (an excellent protein source) that 2 tablespoons contain 7 grams of protein (a bit more than that in a large egg), what it doesn't tell you is that only a bit less than 4 grams is actually digestible by human bodies, and of that only a little over 2 grams is [complete protein](#gloss-complete-protein) - the kind found in an egg or a piece of chicken meat, and the kind we need.

There are 9 protein building blocks (amino acids) that human bodies cannot make and must therefore ingest. Additionally, they must be ingested in specific proportions. When a food, or meal, or diet lacks or is insufficient in one or more of these "essential" amino acids this has a limiting effect on the utilization of the other 8. This is the "incomplete protein" problem that almost all plant proteins present.

Consider someone building a brick wall, where the plan calls for a fixed ratio of bricks to bags of cement — say, 50 bricks per bag. If they have 500 bricks but only 6 bags of cement, they can only build as much wall as 6 bags of cement allows; the other 200 bricks sit unused no matter how many more of them they buy. Buying more bricks doesn't help, because bricks were never what was running short *relative to the fixed ratio the plan calls for*.

This is the essential amino acid problem inherent in plant-based diets. The human body needs each of the nine essential amino acids in a fixed proportion to the total protein eaten — much like the bricks-to-cement ratio above. When a food, meal, or diet is short on one amino acid relative to that required ratio, the shortfall — not the total protein eaten — sets a ceiling on how much of that protein the body can actually use; the rest is broken down and discarded, like the unused bricks. (This required ratio is the [FAO 2013 Reference Standard](#fao) — see [Appendix B](#appendix-b) for the full technical explanation.)

While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24-hour period if the amino acid limitation problem is to be avoided. So, one way or another, one needs to tend to the issue of what is missing and where to find replacements to add it to one's diet in time.

**NuMa handles gracefully the tricky problem of managing plant-based proteins.** Few people know which foods have missing essential amino acids ([EAAs](#gloss-eaa)) or which have the needed excess [EAAs](#gloss-eaa) which would make them a good complement to eat with other foods lacking enough of those [EAAS](#gloss-eaa) in the same 24-hour period.

Beyond the problem of ingesting the right mix of amino acids, there are two other related dietary protein problems to be addressed:

* Protein in a food, however balanced or not, does no good if our bodies do not access it. Different protein sources in plant-based diets are metabolized in differing degrees of efficiency. This is the **[bioavailable protein](#gloss-bioavailable-protein)** problem.

* Age, sex, and activity level differences in protein needs do exist and they are not minor. Older people, active people, and those with chronic diseases, for example, require substantially more protein than do younger healthy people, for several reasons. Almost all common discussions of dietary protein fail to address this problem, and in any case a mere discussion doesn't tell one what to eat and how much.

### C. This protein-management problem is critical for older people and the chronically ill, and especially so for women

In very brief summary, as we age, we tend to lose muscle mass, utilize dietary protein less efficiently, and simply eat less. These factors compound to create a perfect storm of vulnerability to general ill-health and the often dire consequences of falls. And these issues affect women more than men. Put simply - getting enough of the right sort of protein matters far more than most people realize. A good diet is utterly necessary, but not by itself sufficient. It must be complemented with adequate resistance exercise.

There is very little discussion of the problem in the mass media. So, it is up to use as individuals to self-educate and then make carefully considered decisions about our diet. But this is almost impossible to do without serious technical help, as the nutritional factors involved go well beyond simple arithmetic or the naively simple view offered to us by the first major statements about plant protein complementarity in the very early '70s.

### D. NutriMagnus is the missing helper

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

Nutrition analysis programs, both paid and free open source, already exist but none that I've seen focus on the problems faced by vegetarian and vegan folks. And none have the rich features and readily modifiable design that I want. The NuMa program addresses both problems in detail. It also suggests complementary foods that can be combined with a food or recipe or meal to create [complete proteins](#gloss-complete-protein) in one's diet.

NuMa has been under intense development and is still being developed. Over time, new users will expertience unanticipated needs and the program can be further developed to meet them. This is one reason why [reporting problems](#feedback) is so important - feedback drives program development.

Very recently, a Windows version of the program has been developed. It will soon be available for download and user trials. 


### E. Why you can trust NutriMagnus (NuMa)

**[NuMa](#gloss-numa) draws on multiple data sources, and tells you which ones it is using.** Nutrient data comes primarily from [USDA](#gloss-usda) FoodData Central[^2] — one of the most comprehensive public nutrition databases in the world — with branded and international foods supplemented by Open Food Facts.[^3] Beyond those external sources, [NuMa](#gloss-numa) also draws on data you have built up yourself: foods saved to your [Pantry](#pantry), and [recipes you have analyzed](#recipes-menu-web). For protein complement suggestions specifically, a built-in list of 25 common protein sources[^10] fills in as a fallback when your own data doesn't cover a gap. Glycemic index estimates can likewise be filled in automatically from a small published reference table (see [Glycemic Index](#gi)), rather than typed in from scratch. Wherever the program makes a suggestion, it shows you which sources it consulted.

**[NuMa](#gloss-numa) has an extensive formal code test process.** As of this writing (2026-08-04), there are 470 formal tests that the program must pass after every significant change. The vast majority of these are "behavioral" tests which verify that pages, forms, and workflows all still work as they should. A smaller number are "computational validation tests" in which real-world data is fed into the program to make sure that the output matches known correct numbers.

**Appendix K has a fully worked out validation example.** You can do this yourself, if you like. Data are brought in from outside the program and run through the official correct computation process. Full source references are given. You can run the same computation in [NuMa](#gloss-numa) and compare the result.

**Problems may appear anyway.** As professional programmers will tell you, all programs have bugs. This is more likely for new ones than for those which have been around for years. This is why you should report any result you are getting which doesn't make sense to you. There is a small chance you've found a "bug", but a greater chance that the program simply needs to explain itself to you more clearly. Either problem will be fixed ASAP, and all such fixes benefit everyone who uses the program.

**How to report suspected errors or problems with the program:** see [Getting more help](#feedback) in Part 7.

---

### F. Sample Workflows [sample-workflows]

**If you'd prefer to learn by example before reading explanations,** fully worked, step-by-step walkthroughs are provided later in this manual — see [Sample Workflows](#sample-workflows-web) in Part 5. You don't need to read Part 2 or Part 3 first.

---

## Part 2 — Core nutrition concepts

### A. Essential Amino Acids [aa]

Amino acids are the building blocks of protein. Nine of them are "essential", for our bodies cannot make them, so they must come from food every day:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and Phenylalanine respectively. NuMa evaluates [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr) as combined pairs when scoring protein quality, following [FAO](#gloss-fao) 2013 guidelines.

See [Protein Completeness](#complete) and [Amino Acid Gaps](#gap) for how completeness is scored and what a gap means.


### B. Protein Complement Suggestions [comp]

When amino acid gaps are detected, NuMa suggests foods that can improve the protein quality of the base food or meal. Two separate tiers are shown, and they use different methods:

#### TIER 1 — GAP CLOSERS

These foods can mathematically close a specific amino acid gap with a practical amount (up to 500 g). A gap closer has a high enough ratio of the [limiting amino acid](#gloss-limiting-amino-acid) to protein that adding it to the base food brings that amino acid's score to 1.0 (the [FAO](#gloss-fao) reference floor).

Each suggestion shows:
  - Grams to add
  - Which gaps it closes, with scores before and after
  - Digestible protein added
  - Total bioavailable [complete protein](#gloss-complete-protein) — the base food protein plus the complement protein, multiplied by the combined (pooled) [DIAAS](#gloss-diaas) of the pair. This is higher than just adding each food's individually-digestible protein, because the complement's amino acids improve the usability of the base food's protein too.

#### RANKING

Options are ranked by the smallest practical amount needed, with one refinement: an option that fully completes the amino acid profile is moved to the front — but only if its serving size is 50 g or less. An option requiring 90 g to achieve completeness will not outrank a 7 g option that merely closes the primary gap. This prevents a food with a barely-adequate amino acid ratio (just above the [FAO](#gloss-fao) reference) from dominating the list simply because adding large quantities of it eventually fixes every gap.

#### TIER 2 — DIAAS-BOOSTING OPTIONS

Sometimes the digestibility of the base food is low enough that no practical amount of any single food can "close the gap" mathematically. This happens when the food's raw amino acid ratios are already near the [FAO](#gloss-fao) reference — the gaps are digestibility-driven rather than composition-driven. Adding even a very good complement raises the pool's digestible amino acids but can't fully overcome the base food's own digestibility penalty via the gap-closer formula.

For those situations, [DIAAS](#gloss-diaas)-boosting options are shown instead. These foods raise the combined meal [DIAAS](#gloss-diaas) score toward 0.90 by contributing digestible amino acids that pool with the base food's amino acids. The calculation uses each food's own true [ileal digestibility](#gloss-ileal-digestibility) (not just the [DIAAS](#gloss-diaas) score), so a high-digestibility food like soy protein isolate (95%) contributes disproportionately more digestible amino acids than its raw content alone would suggest.

Each [DIAAS](#gloss-diaas)-boosting suggestion shows a progression of serving sizes — 15 g, 30 g, 60 g, and up to 120 g (roughly 1/2 cup) for meal, food, and daily-summary analyses. Each step shows the meal [DIAAS](#gloss-diaas) before and after adding that amount, so you can choose a realistic portion rather than being given a single impractically large target. Recipe analysis uses larger steps (up to 300 g) because recipe quantities serve multiple people.

#### TIER 3 — TWO-FOOD COMBINATIONS

When a single food can close the primary gap but in doing so dilutes another borderline amino acid, a two-food combination is offered. The logic follows a gap-cascade:

  Food A closes the primary (most-limiting) gap. It may open a smaller secondary gap by diluting a borderline amino acid that was already close to the threshold.

  Food B is chosen specifically to close whatever gap Food A left behind, without opening further gaps.

Together the pair clears all amino acid gaps. The output shows the individual gram amounts for each food, the cumulative amino acid effects, and whether the combination achieves "closes all gaps" status.

Three combinations are shown initially. The app offers to show more if available.

Combinations are ranked by total weight (lighter is ranked first), with combinations that close all gaps ranked above those that do not.

#### WHICH TIER IS RIGHT FOR YOU?

If single-food gap closers (Tier 1) are available, they are the most targeted choice: they fix a specific deficiency with a single food.

If single-food options open a secondary gap, Tier 3 two-food combinations show how to close everything in one practical step.

If only [DIAAS](#gloss-diaas)-boosting options are shown (Tier 2), the underlying problem is that the base food is not highly digestible. Adding a well-digested, amino-acid-rich food improves the overall protein quality of the meal even without closing any single gap definitively. This is nutritionally meaningful — a meal [DIAAS](#gloss-diaas) of 0.90 means 90% of the protein is both complete and digestible.

You do not need to eat [complement foods](#gloss-complement-food) at the same meal — meeting daily totals is sufficient for healthy adults. See also [DIAAS](#diaas) and [limiting amino acid](#gap) for background.

Data sources, checked in this order: your [pantry](#pantry) (Foods → [My Pantry](#gloss-my-pantry)) and any [recipes you have analyzed](#recipes-menu-web); then your broader food cache (any food you've ever looked up, matched by name against the built-in reference list below); then that built-in list itself[^10], filtered by your dietary preferences (see [dietary preferences](#diet)). The suggestion header tells you exactly which sources were considered for that run. See [amino acid estimates in suggestions](#comp-estimate) for what it means when a suggestion is tagged "(estimated)" or "(generic estimate)".

Don't want a particular suggestion? See [ignoring a complement suggestion](#ignore-complement) in Part 4.


### C. Amino acid estimates in complement suggestions [comp-estimate]

A [complement suggestion](#comp) needs amino acid data for the suggested food to compute how much of it closes a gap. Most of the time that comes from the food's own real, measured data. When it doesn't, NuMa falls back to the same built-in reference table of 25 common protein sources[^10] used to fill gaps in [Protein Complement Suggestions](#comp) (soy protein isolate, nutritional yeast, oats, and the like) rather than leaving you with no suggestion at all. Two tags tell you when that fallback happened:

  "(estimated)" — the suggested food is a real item from your pantry, recipes, or food cache, but it has no amino acid panel of its own. NuMa matched its name against the built-in reference table and scaled that table's amino acid profile to this food's own protein content.

  "(generic estimate)" — no real food matched at all. The whole suggestion is the reference table entry itself, not any specific product you have.

Either way, this estimate is computed fresh every time the suggestion is shown — it is never saved to the food's own record, so there is nothing to undo. This is not the same as the "estimate amino acids from another food" tool described under [Estimating amino acids by copying from another food](#custom-foods). That tool lets you search all your saved foods and pick whichever one you judge to be the best match yourself, and it saves your choice permanently to that food's own record. The built-in table used for the "(estimated)" / "(generic estimate)" tags, by contrast, is a fixed, much shorter list matched purely by keyword — it can't use your own judgment about which food is the closer match, so the two methods can disagree.

For a food you rely on often, running the "estimate amino acids from another food" tool on it yourself is worth doing: it is more accurate (your judgment beats a keyword match against 25 entries), it only has to be done once, and it turns the food into a normal pantry/cache candidate for every suggestion afterward — no more tags.


### D. Two-step combinations [comb]

After the gap-closer and [DIAAS](#gloss-diaas)-boosting sections, NuMa offers to show two-step combinations. Each combination pairs one of the top gap-closers (Step 1) with the best [DIAAS](#gloss-diaas)-booster for the resulting protein pool (Step 2).

Why two steps? A gap-closer fixes amino acid balance but may not raise digestibility. A [DIAAS](#gloss-diaas)-booster raises digestibility but cannot close a specific amino acid gap on its own. Together they address both problems: Step 1 corrects the [limiting amino acid](#gloss-limiting-amino-acid); Step 2 raises the overall [DIAAS](#gloss-diaas) of the now-balanced pool, increasing digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp)) further.

Each combination shows:
  - Step 1: the gap-closer, its serving size, and the [DCP](#gloss-dcp) gain from the base
  - Step 2: the smallest practical serving of the best booster for that pool, and the further [DCP](#gloss-dcp) gain
  - Net [DCP](#gloss-dcp) gain from base to end of Step 2

If no [DIAAS](#gloss-diaas)-booster can improve on the post-Step-1 pool (because the gap-closer already raised the pool's digestibility above what any available booster can match), the program says so rather than showing a misleading suggestion.

See also [complement suggestions](#comp) for the full complement suggestion system.


### E. Protein Completeness [complete]

A protein is "complete" when it supplies all nine essential amino acids at or above the [FAO](#gloss-fao) 2013 reference amounts, adjusted for digestibility. Essential amino acids cannot be made by the body — they must come from food.

Most animal proteins are complete. Most plant proteins are not, but combining plant foods across a day can produce a complete profile — see [Protein Complement Suggestions](#comp).

The score shown in completeness tables is the ratio of each amino acid to the [FAO](#gloss-fao) reference level. A score of **1.0 or above** for all nine means the protein is complete. The most-[limiting amino acid](#gloss-limiting-amino-acid) (the one with the lowest score) is identified as the bottleneck.


### F. Digestible Complete Protein (DCP) [dcp]

[DCP](#gloss-dcp) — digestible [complete protein](#gloss-complete-protein) — is the grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (supply all essential amino acids at or above reference levels).

It is more meaningful than raw grams of protein because it accounts for:

- **Digestibility:** how much protein is actually absorbed (from [DIAAS](#gloss-diaas))
- **Completeness:** whether the amino acid profile meets all requirements

A food with 30 g of protein but a [DIAAS](#gloss-diaas) of 0.70 and several amino acid gaps contributes less usable protein than those numbers suggest. [DCP](#gloss-dcp) captures that.

[DCP](#gloss-dcp) is also called "bioavailable complete protein" or "usable protein" in nutrition literature — these terms mean the same thing. NuMa uses [DCP](#gloss-dcp) throughout.

NuMa shows [DCP](#gloss-dcp) in the bioavailability section of food and recipe analysis. See also [DIAAS](#diaas) and [Protein Completeness](#complete).


### G. DIAAS — Digestible Indispensable Amino Acid Score [diaas]

[DIAAS](#gloss-diaas) measures how well your body can actually use the protein in a food. A score of **1.0** means the protein fully meets the [FAO 2013 amino acid reference standard](#fao) after accounting for digestibility. Scores above 1.0 are excellent; below 1.0 means one or more amino acids fall short.

Animal proteins typically score 1.0 or above. Most plant proteins score below 1.0, though some (pea protein, soy) come close. Digestibility matters because some protein in food is never absorbed — it passes through unchanged or is broken down by gut bacteria rather than used by your body.

A note on terminology: the [FAO](#gloss-fao) uses the term "indispensable amino acids" (IAA) where this manual uses "essential amino acids" ([EAA](#gloss-eaa)) — both refer to the same nine amino acids. The "I" in [DIAAS](#gloss-diaas) stands for "Indispensable."

NuMa uses [DIAAS](#gloss-diaas) to calculate digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp)), which is a better indicator of actual protein quality than raw grams. See [Digestible Complete Protein (DCP)](#dcp).

#### Estimating DIAAS by hand for a packaged food [diaas-estimate-table]

Branded/packaged products often have no amino acid data at all, so NuMa can't compute [DIAAS](#gloss-diaas) automatically — you record a point estimate instead via the [DIAAS](#gloss-diaas) estimate [Food Annotation](#gloss-food-annotation) (Foods → Annotate a food — see [Getting missing amino acid data](#custom-foods)). [DIAAS](#gloss-diaas) is mostly a property of the *protein source*, not the specific product, so the same point estimate is reusable across many products built from that ingredient. This table of published point estimates by dominant protein source is a starting reference, not a substitute for a real measured value if one is available:

    Protein source        DIAAS       Limiting AA                Note
    --------------------  ----------  -------------------------  ------------------------------
    Whole wheat            0.45       Lysine                     Range 0.40-0.57 across studies
    Soy (isolate/tofu)     0.90-1.00  Methionine+cystine (mild)  Near-complete
    Pea protein            0.82-0.90  Methionine+cystine         Complements wheat well
    Oats (dehulled)        0.77       Lysine                     Better than most cereals
    Sunflower seed          ~0.60     Lysine                     Usually a minor contributor

For a product where one ingredient supplies essentially all the protein (e.g. a wheat cracker where the oil contributes negligible protein), use that ingredient's row directly. For a product with two meaningful protein sources (e.g. a wheat+pea cracker), weight the estimate by each ingredient's share of total protein grams — the same complementary-protein logic used elsewhere in NuMa's [meal-level DIAAS](#dcp) pooling. Document your reasoning (source ingredient, any blending math) in the food's Confidence Note or notes field so it can be reviewed or revised later.


### H. Limiting-Amino-Acid Scoring [aa-scoring]

Protein quality analysis involves two separate adjustments. The Protein Digestibility table shows the result after the first adjustment only. The phrase "before limiting-amino-acid scoring" on that table means the second adjustment has not yet been applied.

#### Step 1 — Digestibility adjustment (shown in the table)

    Digestible protein (g) = food protein (g) × digestibility coefficient

This accounts for how much protein actually reaches your bloodstream. A food with 20 g of protein and a digestibility of 0.85 delivers 17 g of digestible protein. This is what the "Digestible prot" column shows.

#### Step 2 — Limiting-amino-acid scoring (the DIAAS step)

    Digestible complete protein (g) = digestible protein (g) × min(DIAAS, 1.0)

Even if all the protein is absorbed, it cannot all be incorporated into tissue unless every essential amino acid is present in sufficient proportion. The amino acid in shortest supply — the [limiting amino acid](#gloss-limiting-amino-acid) — sets a ceiling. [DIAAS](#gloss-diaas) is the ratio of that [limiting amino acid](#gloss-limiting-amino-acid) to the [FAO](#gloss-fao) reference level. If [DIAAS](#gloss-diaas) is 0.80, only 80% of the digestible protein can be fully used; the rest is broken down and excreted.

The "Total digestible protein" line below the table is the sum after step 1 only. The [DCP](#gloss-dcp) figure reported in the meal summary is the result after both steps.

Note: [DIAAS](#gloss-diaas) itself is not capped — a high-quality food can score above 1.0, meaning it has surplus amino acids relative to the reference. The min([DIAAS](#gloss-diaas), 1.0) applies only when computing [DCP](#gloss-dcp), because having excess amino acids does not allow you to absorb more total protein than you consumed.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [limiting amino acid](#gap), [DCP cap](#dcp-cap).


### I. Why DCP Is Sometimes Capped Below the DIAAS Projection [dcp-cap]

The short version: the [DIAAS](#gloss-diaas) formula can project a Digestible [Complete Protein](#gloss-complete-protein) value that is mathematically higher than the protein your body actually absorbed. When that happens, NuMa caps [DCP](#gloss-dcp) at the absorbed-protein ceiling, because you cannot use more protein than you took in.

#### Why this happens

*The next few paragraphs walk through the underlying math. If you'd rather skip the algebra, jump ahead to "In plain words" below, or straight to the worked example.*

[DIAAS](#gloss-diaas) is defined by the [FAO](#gloss-fao) as:

    DIAAS = (digestible supply of the limiting amino acid)
            divided by
            (FAO reference density for that amino acid × raw protein)

The numerator uses digestibility-corrected amino acids. The denominator uses raw (pre-digestion) protein. This is intentional in the [FAO](#gloss-fao) standard. [DCP](#gloss-dcp) is then:

    DCP = raw protein × DIAAS

Substituting the [DIAAS](#gloss-diaas) definition, this simplifies to:

    DCP = digestible limiting-AA supply / FAO reference density for that AA

**In plain words:** [DCP](#gloss-dcp) answers "How many grams of a reference-quality protein would supply the same amount of limiting amino acid as this meal provides?"

For a single food, [DIAAS](#gloss-diaas) never exceeds that food's own digestibility, so [DCP](#gloss-dcp) cannot exceed absorbed protein. In a mixed meal, however, the [limiting amino acid](#gloss-limiting-amino-acid) may be concentrated in a high-digestibility ingredient while the bulk of the protein mass comes from lower-digestibility ingredients. The [DIAAS](#gloss-diaas) score then reflects the high-digestibility source, but average protein absorption reflects the lower-digestibility majority. [DIAAS](#gloss-diaas) ends up higher than the weighted-average digestibility, and the [DCP](#gloss-dcp) formula overshoots absorbed protein. This is a known mathematical artifact of applying [FAO](#gloss-fao) [DIAAS](#gloss-diaas) to mixed meals.

#### A worked example

Suppose a breakfast has two protein sources:

    Food                   Raw protein   Digestibility   Absorbed protein
    -------------------    -----------   -------------   ----------------
    Soy protein isolate    10 g          0.95            9.5 g
    Oatmeal                30 g          0.82            24.6 g
    -------------------    -----------   -------------   ----------------
    Total                  40 g          avg 0.854       34.1 g

Soy isolate is lysine-rich. Because lysine is the usual [limiting amino acid](#gloss-limiting-amino-acid) in grain-heavy meals, it strongly influences the [DIAAS](#gloss-diaas) score. Suppose the pooled lysine supply (after digestibility correction) yields:

    DIAAS = 0.91

Raw-formula [DCP](#gloss-dcp):

    DCP = 40 g × 0.91 = 36.4 g

But total absorbed protein is only 34.1 g. The cap is applied:

    DCP = min(36.4 g, 34.1 g) = 34.1 g

Why did [DIAAS](#gloss-diaas) exceed average digestibility? The soy isolate (dig 0.95) provides most of the lysine, so the lysine ratio in the [DIAAS](#gloss-diaas) calculation reflects its high digestibility. The larger oatmeal portion (dig 0.82) dominates the absorbed-protein total and pulls the weighted average down to 0.854. [DIAAS](#gloss-diaas) (0.91) ended up above that average, causing the overshoot.

#### What the cap means in practice

A capped [DCP](#gloss-dcp) is actually good news about amino acid quality. It means your [limiting amino acid](#gloss-limiting-amino-acid) is present in such good supply (relative to raw protein) that the formula projects more [complete protein](#gloss-complete-protein) than you could possibly absorb. The practical reading: all of your absorbed protein is functioning as [complete protein](#gloss-complete-protein). You are not losing protein to an amino acid shortfall.

Compare this to an uncapped [DCP](#gloss-dcp) that is well below absorbed protein: the gap between them represents protein you absorbed but cannot fully use for tissue synthesis because the [limiting amino acid](#gloss-limiting-amino-acid) ran out first. That is the more common and more concerning situation.

The average digestibility shown in the cap note is the weighted average of per-ingredient [digestibility coefficients](#gloss-digestibility-coefficient), weighted by protein content. Each coefficient comes from the curated lookup table or category estimate described in [meal protein digestibility](#meal-diaas).

This cap note appears on the meal, full-day, recipe, and daily-summary DIAAS sections.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [amino acid scoring](#aa-scoring).


### J. FAO 2013 Reference Standard [fao]

The [FAO](#gloss-fao) (Food and Agriculture Organization of the United Nations) published a reference amino acid scoring pattern in 2013 that defines the minimum amounts of each essential amino acid per gram of protein needed to meet adult human requirements. This is a ratio, not an absolute quantity — the requirement scales with how much protein you eat, so a small meal and a large meal must both hit the same per-gram proportions. See [Appendix B](#appendix-b) for the full worked explanation of why this ratio, not total protein, determines what your body can use.

NuMa uses this pattern as the benchmark for all protein quality scoring: completeness, gaps, and complement calculations. A score of **1.0** for an amino acid means the food exactly meets the [FAO](#gloss-fao) reference for that amino acid; above 1.0 exceeds it; below 1.0 falls short.

The [FAO](#gloss-fao) 2013 pattern replaced an older 1991 standard and is the current international reference for protein quality assessment.


### K. Amino Acid Gaps [gap]

An amino acid gap means one or more essential amino acids are below the [FAO](#gloss-fao) 2013 reference level after digestibility adjustment. The gap is expressed as a score: 0.70 means the food supplies 70% of what is needed for that amino acid.

Gaps are sorted from most-limiting to least:

    Score     Status                                    Complement suggestion?
    --------  ----------------------------------------  ----------------------
    >= 1.0    Meets FAO reference -- complete           No
    0.95-0.99 Near-adequate -- practical gap too small  No (NuMa floor)
    0.70-0.94 Gap present                               Yes
    < 0.70    Significant gap -- high priority          Yes

NuMa generates complement suggestions only for scores below 0.95, not below the [FAO](#gloss-fao) floor of 1.0. A gap of 0.98 would suggest "add 1 g" -- not useful. The 0.95 floor filters those out.

- **Methionine** is the most commonly [limiting amino acid](#gloss-limiting-amino-acid) in plant-based diets.
- **Lysine** is the most commonly limiting in grain-heavy diets.

See [Protein Complement Suggestions](#comp) for how NuMa suggests foods to close gaps.


### L. Antinutrients [antinutrients]

Most people have never encountered this term, yet [antinutrients](#gloss-antinutrient) are present in virtually every plant food. Understanding them is especially important for anyone eating a plant-predominant diet, because the same foods that supply the most fiber, minerals, and [phytonutrients](#gloss-phytonutrients) are often the ones that contain the highest [antinutrient](#gloss-antinutrient) loads.

#### What is an antinutrient?

The word sounds alarming, but it simply means a naturally occurring compound in a food that partially blocks the absorption or use of a nutrient your body would otherwise receive. The effect is not binary — it is a matter of degree, and it can usually be reduced or eliminated by how you prepare the food.

Plants produce these compounds as a natural defense: against insects, fungi, and animals that would eat them. They are not contaminants or the result of farming practices. They are intrinsic to the plant's biology.

#### The main antinutrients that appear in NutriMagnus output

**Phytates** (phytic acid). Found in legumes, whole grains, nuts, and seeds. Phytate binds tightly to minerals — especially iron, zinc, calcium, and magnesium — forming a complex the body cannot easily absorb. A meal of lentils or whole-wheat bread may contain all the iron the label shows, but much of it may pass through unabsorbed if phytate is high. The effect depends on the rest of the meal: vitamin C consumed at the same meal significantly counteracts phytate's effect on iron. Preparation methods that consistently reduce phytate: soaking legumes or grains overnight before cooking; sprouting; fermentation (sourdough bread reduces phytate by 50-90%; tempeh and other fermented soy products have low phytate).

**[Oxalates](#gloss-oxalate)**. Found at high levels in spinach, Swiss chard, beet greens, rhubarb, and almonds; at moderate levels in many other plant foods. [Oxalates](#gloss-oxalate) bind calcium in the gut, meaning the calcium shown on a food label for spinach is largely unavailable — absorption rates can be as low as 5%, versus 30% for dairy calcium. For most people this is simply a reason not to rely on spinach as a calcium source, not a reason to avoid it. For people prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly. See [oxalate data](#oxalate) for the detailed data NuMa tracks on this.

**Lectins** and **trypsin inhibitors**. Found in raw legumes (beans, lentils, chickpeas, soybeans). Lectins interfere with the gut lining; trypsin inhibitors block a key digestive enzyme. Raw kidney beans contain enough lectin to cause acute food poisoning. Cooking completely solves the problem: full boiling for at least 10 minutes destroys both lectins and trypsin inhibitors. Canned beans are already safe. Tofu and tempeh are also safe because both involve prolonged heat treatment or fermentation. This is the one [antinutrient](#gloss-antinutrient) on this list that is not just about partial reduction — with raw legumes, proper cooking is required.

**Bound niacin** (in corn). Untreated corn contains niacin in a chemically bound form the human body cannot absorb. Populations who ate corn as a dietary staple without treatment historically developed pellagra (severe niacin deficiency). The traditional solution — practiced for thousands of years by Mesoamerican cultures and still used today — is nixtamalization: soaking dried corn in an alkaline lime solution. This releases the niacin and makes it fully bioavailable. Tortillas, masa, hominy, and grits made from nixtamalized corn are fine. Plain cornmeal (not nixtamalized) retains the problem.

#### How these appear in NutriMagnus output

When you view a food with known [antinutrient](#gloss-antinutrient) concerns, a note appears in the Bioavailability section of the analysis. The note names the compound, describes the specific problem, and lists the preparation method(s) that reduce it.

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

These notes appear only for foods where NuMa has a curated flag — the list is not exhaustive, and absence of a note does not mean a food is free of [antinutrients](#gloss-antinutrient).

#### What these notes do not mean

They are not a reason to avoid these foods. Legumes, whole grains, nuts, and leafy greens are among the most nutritious foods available. The minerals and protein they supply — even after [antinutrient](#gloss-antinutrient) reduction — are substantial, and their other benefits (fiber, [phytonutrients](#gloss-phytonutrients), cost, sustainability) are undiminished. The notes exist so you can make informed preparation choices and avoid assuming that every labeled nutrient is fully absorbed.

The practical message is: soak legumes, prefer sourdough or sprouted grains when possible, cook beans fully, pair iron-rich plant foods with vitamin C, and do not rely on spinach as your primary calcium source.


### M. Oxalate Data [oxalate]

[Oxalates](#gloss-oxalate) are one of the [antinutrients](#gloss-antinutrient) discussed in [antinutrients](#antinutrients). The section here covers the detailed data NuMa tracks and how to use it. For general background on what [oxalates](#gloss-oxalate) are and how they compare to other [antinutrients](#gloss-antinutrient), read [antinutrients](#antinutrients) first.

[Oxalates](#gloss-oxalate) (oxalic acid) bind calcium in the gut, reducing its absorption from high-[oxalate](#gloss-oxalate) foods. They are found at very high levels in spinach, Swiss chard, beet greens, and rhubarb, and at notable levels in almonds and some other nuts. For most people the main consequence is that these foods are poor calcium sources despite their labels. For anyone prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly.

NuMa includes the Harvard T.H. Chan School of Public Health [oxalate](#gloss-oxalate) table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine. This data is optional and disabled by default.

**To enable it:** Settings → Your Profile → check "Look up oxalate content for foods," then Save profile.

Once enabled, viewing a food or analyzing a recipe automatically looks it up in the Harvard table by name and links the best match — no confirmation prompt. That link is saved the first time and reused after, so the lookup only runs once per food.

#### Important limitations

- [Oxalate](#gloss-oxalate) values in the Harvard table are reported per serving, not per 100 g. For foods measured in ounces (fish, nuts, meat), NuMa automatically converts to per-100g. For foods measured in cups, pieces, or tablespoons, only the per-serving value is available. Volumetric servings cannot be converted to per-100g without knowing the food's density — that conversion must be done manually if needed.

- For recipe analysis, NuMa sums [oxalate](#gloss-oxalate) only for ingredients where a per-100g value is available. Volumetric-only items are excluded from the total and noted as such.

- [Oxalate](#gloss-oxalate) content varies with preparation method (cooking reduces [oxalate](#gloss-oxalate) in spinach, for example) and growing conditions. All values should be treated as estimates.

- Matching by food name is approximate. "Spinach, raw" in the Harvard table maps reasonably to [USDA](#gloss-usda) spinach entries, but processed or branded foods may not match well. Always verify the match makes culinary sense before confirming it.

For background on [oxalates](#gloss-oxalate) and kidney health, see the Harvard Health references in the source data (Settings -> [Oxalate](#gloss-oxalate) data for data provenance).


### N. Glycemic Index [gi]

The glycemic index ([GI](#gloss-gi)) measures how quickly a carbohydrate-containing food raises blood glucose compared to pure glucose ([GI](#gloss-gi) = 100). Low-[GI](#gloss-gi) foods (55 or below) produce a slower, more gradual rise; high-[GI](#gloss-gi) foods (70 and above) cause a faster spike.

[GI](#gloss-gi) is shown in the nutrient summary when data is available. It is most useful for comparing foods within the same category — for example, choosing between types of bread or rice. Keep in mind that [GI](#gloss-gi) describes a food eaten alone; combining foods in a meal (especially adding fat, protein, or fiber) physiologically blunts the blood glucose response to the carbohydrates present, by slowing gastric emptying and glucose absorption. However, this effect is not fully captured by glycemic load ([GL](#gloss-gl)) — see [Glycemic Load](#gl) for why.

NuMa displays [GI](#gloss-gi) for reference only and does not use it in protein quality calculations.

**Where [GI](#gloss-gi) values come from.** Neither [USDA](#gloss-usda) nor Open Food Facts[^3] tracks [GI](#gloss-gi), so NuMa can't look it up automatically the way it does for calories or protein — you (or NuMa, on your behalf) have to supply it. To save you the work for common foods, NuMa can automatically fill in [GI](#gloss-gi) values for about 60 everyday items, using a published reference table[^8]. If your food cache doesn't have these values yet, NuMa will ask whether you'd like it to fill them in for you. For anything else, just add [GI](#gloss-gi) values as you go: the first time you add a new food to your Pantry or a meal, NuMa will offer to prompt you for its [GI](#gloss-gi) value right there, so your data builds up naturally through normal use.


### O. Glycemic Load [gl]

Glycemic load ([GL](#gloss-gl)) improves on the glycemic index by accounting for both the quality and the quantity of carbohydrate in a serving. The formula is:

```
GL = (GI × grams of available carbohydrate) / 100
```

For a meal combining multiple foods, the total [GL](#gloss-gl) is the sum of the [GL](#gloss-gl) calculated separately for each component:

```
Meal GL = GL(food 1) + GL(food 2) + GL(food 3) + ...
```

Adding more carbohydrate-containing foods will always increase the meal total. The reason combining foods physiologically blunts the blood glucose response — as noted in the [GI](#gloss-gi) section — is not reflected in this calculation. Protein, fat, and fiber slow gastric emptying and glucose absorption, reducing the actual blood glucose rise; but because [GL](#gloss-gl) is calculated from fixed [GI](#gloss-gi) values measured for each food in isolation, it has no way to represent that interaction. [GL](#gloss-gl) is therefore a reliable tool for comparing meals of broadly similar macronutrient composition, but becomes less accurate when meals differ significantly in their fat or protein content.

A food can have a high [GI](#gloss-gi) but a low [GL](#gloss-gl) if the serving contains little actual carbohydrate — watermelon is the classic example. Conversely, a moderate-[GI](#gloss-gi) food eaten in a large portion can produce a high [GL](#gloss-gl). For this reason [GL](#gloss-gl) is generally a better guide to real-world blood glucose impact than [GI](#gloss-gi) alone.

**[GL](#gloss-gl) is interpreted on a per-meal or per-food basis:**

| [GL](#gloss-gl) Range | Classification |
|---|---|
| 10 or below | Low |
| 11–19 | Medium |
| 20 or above | High |

NuMa displays [GL](#gloss-gl) in the nutrient summary alongside [GI](#gloss-gi) when carbohydrate data is available. Like [GI](#gloss-gi), it is shown for reference and does not affect protein quality calculations.

For a discussion of how [GL](#gloss-gl) compares to other approaches for evaluating the blood glucose impact of different meal choices — particularly relevant for people managing diabetes — see [Appendix D: GL and Blood Glucose Comparison](#appendix-d).


### P. Recommended Dietary Allowances [rda]

[RDA](#gloss-rda) values in NuMa come from the Dietary Reference Intakes ([DRI](#gloss-dri)) published by the U.S. National Academies of Sciences. They represent the average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group.

When you set a user profile (Settings → User profile), NuMa uses your age, sex, weight, height, and activity level to estimate personalized targets. The calorie estimate uses the Mifflin-St Jeor equation with an activity multiplier. The protein target uses 0.8 g per kg body weight as a baseline minimum.

The comparison table ("Daily Intake vs. Recommended Values") shows how your logged meals for today compare to your targets.

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

Nutrients without an established Dietary Reference Intake ([phytonutrients](#gloss-phytonutrients), amino acids) are shown without a Target or % of [RDA](#gloss-rda) -- those rows show only the Intake amount.

See [daily nutrient goals](#goals) for a full explanation of how each goal is calculated.


### Q. Daily Nutrient Goals [goals]

NuMa calculates personalized daily nutrient goals from your user profile (Settings → User profile). Each goal is one of three types:

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

#### Omega-3 ALA (minimum)
    1600 mg/day men, 1100 mg/day women — Adequate Intake for alpha-linolenic
    acid (ALA), the plant-sourced omega-3. See [Omega-3 Fatty Acids](#omega3)
    for why this is the only omega-3 with an official goal in NuMa.

#### Minerals and vitamins
    All use age- and sex-specific values from the Dietary Reference
    Intakes published by the U.S. National Academies of Sciences.
    Values vary by age group and sex; the most common adjustments are
    calcium (increases after age 50-70), iron (higher for premenopausal
    women), vitamin D (increases at age 70), and B6 (increases after 50).

Nutrients without established [DRIs](#gloss-dri) ([phytonutrients](#gloss-phytonutrients), amino acids) have no goal shown. The "% today" column and "Daily goal" column are blank for those rows.

See [RDA](#rda) for a general overview of where these values come from. If the standard RDA isn't the number you actually want to hit for a given nutrient, see [Profile Optimal Targets](#optimal). If you want to be warned as you approach a personal daily cap, see [Maximum Nutrient Limits](#maxlimits). A single day's numbers are only a snapshot -- see [Multiday Nutrient Trend](#trend) for how to spot a shortfall that persists across many days.


### R. Multiday Nutrient Trend [trend]

Every other RDA comparison in NuMa -- food, recipe, meal, daily summary -- looks at a single day. That's the right window for "did today's meals cover me," but it's the wrong window for a nutrient that's chronically a little short: one low day is unremarkable, but the same shortfall repeated for two weeks straight is exactly the kind of pattern a single-day view can never show you, because you'd have to remember and compare each day yourself.

**Access it via the "Multiday nutrient trend" button on the Daily Summary page.** Choose a window -- last 7, 14, or 30 days -- and NuMa averages your total intake for every tracked nutrient across the days in that window that actually had a meal logged, then compares that average against your RDA (and Profile Optimal / max limits, if configured) using the exact same table, color coding, and diet-aware notes as the daily comparison.

**Only logged days count.** If you ask for a 30-day trend but only logged meals on 12 of those days, the average is computed over those 12 days -- unlogged days are treated as "no data," not as a zero-intake day. Diluting the average with days you simply didn't track would understate your real intake and could hide the exact shortfall this view exists to surface. The screen tells you how many logged days went into the average (e.g. "Averaging over 12 logged day(s) out of the last 30").

This is the same B12/iron/zinc-aware analysis described in [Diet-Aware Bioavailability and Deficiency Notes](#diet-bioavailability) -- a trend view is often where a B12 or iron pattern actually becomes visible, since a single low day rarely triggers concern on its own.

**Multi-day protein complementarity.** Below the nutrient comparison, the trend view also pools every amino-acid-containing food logged across the window's days and runs the same [complement suggestion](#comp) analysis normally shown for a single day -- but framed for forward planning ("Add to upcoming meals" rather than "Add to your day"), since the gap it found accumulated across several days, not one meal you can still fix. A gap that only shows up when pooled across the whole window -- rather than in any single day's suggestions -- is exactly the kind of small, persistent shortfall this view is meant to catch.


### S. Nutrient Plot [nutrient-plot]

A line chart of one or more nutrients across your logged days, day on the x-axis — useful for spotting a trend visually rather than reading a column of numbers.

**Access it from Analysis → Daily Summary → "Nutrient plot".** Check up to 8 nutrients from the full nutrient list (any nutrient NuMa tracks, not just the ones you've chosen as Meals & Log columns, plus Day DCP itself) — Day DCP, Protein, Calories, Carbs, and Fiber are listed first, matching Recent Days' mandatory columns; the checkbox list scrolls vertically below them. Then choose which days to include:

    (blank days-back)         Every logged day, oldest to newest.
    Days back + Ending on     The N days ending on the date you pick
                              (defaults to your most recent logged day).

Only days that actually have a logged meal appear on the chart — a gap in your logging shows as a gap in the line, not a drop to zero.

**Date labels thin out automatically on a long chart.** Every plotted day still gets a data point, but once there are more than 18 of them, showing every single date's label would crowd them into an unreadable jumble, so only every 2nd, 3rd, etc. date is labeled (always skipping at least one), spaced out enough to stay legible.

If you pick nutrients with different units (e.g. Protein in g alongside Sodium in mg), they still plot together on one y-axis. In that case the y-axis shows no title or numbers at all — once nutrients are on different scales, no single number on a shared axis means the same thing for every line, so printing one would just be misleading. The gridlines are still there for a rough sense of relative up-and-down movement; each line's real values live in its own legend entry instead. Plotting a single nutrient, or several that share a unit and didn't need any scaling, still shows a normal, meaningful numbered axis.

**Scaling happens in two steps, both of which you can override.**

*Step 1 — Scale factor.* If one nutrient's numbers dwarf another's (e.g. Calories next to Protein, or Calcium next to Protein), the smaller one would flatten into a barely-visible wiggle along the bottom. NuMa automatically divides every plotted nutrient except the least up-and-down one by a computed **Scale factor** — a number based on how much each nutrient's values swing over the plotted days — which brings a dominant nutrient's swings down to roughly match the smallest one's. The **Scale factor** field shows this computed value as a placeholder (grayed, e.g. "3.5") and is left blank by default, meaning "use that computed value." Type your own number and click Plot to override it.

*Step 2 — Per-nutrient factors.* A single shared Scale factor can't perfectly equalize more than two nutrients at once — with three or more plotted, one can still end up nearly flat even after step 1. NuMa checks each nutrient again after step 1 and sets a floor at 25% of the most up-and-down nutrient's swing; anything still below that floor gets its own individual multiplier (shown as "×2.4" etc. in its legend entry) to bring it back up to a visibly readable wiggle. Each chosen nutrient gets its own **Per-nutrient factors** field, prefilled the same "blank = use the computed value" way as Scale factor — type a number to override just that one nutrient.

**Highlight nutrient.** Pick which one nutrient always draws solid and (in color mode) red, so the figure you're usually comparing everything else against stands out at a glance — defaults to Day DCP whenever it's one of the chosen nutrients.

**Black & white (printer-friendly).** Check this to preview the chart the way it'll look on a printer that can't print color: every line drawn in black, with the highlighted nutrient solid and every other nutrient in its own dash pattern (dashed, dotted, dash-dot, etc.) instead of a color, so lines stay distinguishable without color at all. The on-screen chart updates the instant you check or uncheck the box — no need to click Plot — so you can compare both looks side by side before deciding.

**Smoothing.** Day-to-day values can be noisy enough to obscure the underlying trend. The **Smoothing (days)** field averages each point with its preceding days — a trailing moving average — to smooth that out; it defaults to 3 days. Set it to 0 to turn smoothing off and see the original, unsmoothed data. A smoothed nutrient's own scaling (steps 1 and 2 above) is calculated from the smoothed data, since that's what's actually on the chart.

**Plot title.** Defaults to "Key nutrients, {start date} to {end date}" for whatever range is currently plotted, shown right on the chart itself. Edit the **Plot title** field and click Plot to use your own instead.

**The legend sits below the chart**, wrapped horizontally rather than stacked in a tall column, so it never overlaps a data line and stays compact and print-friendly.

**Print or save it.** "Print / Save as PDF" opens a stripped-down, print-friendly page with the chart and your browser's print dialog. "Download PNG" and "Download SVG" save the chart as an image file — see [Plot File Formats](#plot-file-formats) for which one to pick.


#### Plot File Formats — PNG vs. SVG [plot-file-formats]

Both "Download PNG" and "Download SVG" save the same chart as an image file you can keep, email, or paste into a document — they just store it differently.

**PNG** is a normal photo-style image, a fixed grid of pixels. It opens everywhere without a second thought, and is the safer default if you're not sure what a document or website will accept.

**SVG** stores the chart as the shapes and lines that drew it, not pixels — so it stays perfectly crisp at any size, whether you zoom way in on screen or print it on a large sheet of paper. PNG images can look blurry or blocky if enlarged; an SVG never will. The trade-off is that a few older programs don't open SVG files directly (most current web browsers, word processors, and image editors do).

**Rule of thumb:** downloading to look at, email, or drop into a typical document — PNG. Need to print it large, or want it to stay sharp if someone else resizes it — SVG.


### T. Per-Day Profile Tracking [day-profile]

Your profile isn't fixed forever -- weight, activity level, or even which named profile is active can change over time (illness, travel, a deliberate weight change). But your logged meals stay put. If a past day's DCP and RDA comparisons always used *today's* profile, an old day could silently get re-scored against numbers that weren't true of you back then.

**Each logged day is pinned to whichever profile was active the first time a meal was saved for that date.** That pin is a full snapshot -- your age, weight, activity level, and targets as they were that day -- not just a name. So if you later edit that profile's numbers (or switch which profile is active), days already logged keep comparing against the numbers that were true when you logged them. Only a day that has never had a meal saved for it — or one you explicitly reassign — will pick up a different profile.

**Where you see it.** If you maintain more than one named profile, a **Profile** column/line appears next to each day: on the Meals & Log list, the Recent Days list, and the Daily Summary / full-day view. With only one profile configured, this column is hidden since there's nothing to distinguish.

**Changing a day's profile.** Sometimes the automatic pin doesn't match reality -- illness or travel rarely starts exactly at midnight. Open that day's summary and use the **Change** control next to "Profile:" (on the day's Summary or Full Day page) to pick a different saved profile. The day is marked "(manually set)" afterward and its DCP/RDA numbers recompute immediately against the new pin.

**Multiday trend.** The [Multiday Nutrient Trend](#trend) view spans many days at once, so it scores against the profile pinned to the *most recent* day in the window (today, for the usual "last N days"). If any day inside the window was pinned to a different profile, a note discloses which dates and profile differed, rather than silently blending two profiles' targets into one average.

**Existing data.** If you're upgrading from a version of NuMa that didn't have this feature, every day you'd already logged gets pinned to whichever profile is active the first time you open NuMa after upgrading -- you don't need to open or edit anything for this to happen.


### U. Omega-3 Fatty Acids [omega3]

NuMa tracks four omega fatty acids: ALA, EPA, and DHA (all omega-3), and linoleic acid (omega-6). Only one of these four -- ALA -- has an official Adequate Intake, so it's the only one that appears as a Daily Goal: 1600 mg/day for men, 1100 mg/day for women.

**Why not a goal for EPA and DHA directly?** No U.S. Dietary Reference Intake exists for EPA or DHA intake on their own -- the official guidance covers only total ALA. This matters because ALA is not itself the fatty acid your body mostly uses; it has to be converted into EPA and then DHA, and that conversion is inefficient -- commonly cited at only around 5-10% for EPA, and considerably less for DHA. Two people can hit the same ALA target and land in very different places on EPA/DHA status depending on the rest of their diet, genetics, and sex (conversion tends to be somewhat more efficient in women).

**Why this matters especially for plant-based eaters.** Direct dietary EPA and DHA come almost entirely from fish, algae, and other seafood. If ALA (from flax, chia, walnuts, hemp, canola and soy oils) is your only omega-3 source, meeting the ALA goal is necessary but may not be sufficient -- your actual EPA/DHA status depends on that inefficient conversion step. Common ways to address this without animal fish: algae-oil supplements (a direct EPA/DHA source independent of the ALA conversion pathway), or simply logging ALA-rich foods generously since the target itself already assumes real-world conversion losses are ahead of it.

**Setting your own EPA+DHA target.** Because there's no official DRI to compute automatically, NuMa can't put a Daily Goal on the EPA or DHA rows the way it does for ALA. If you want to track against a target anyway -- clinical guidance in the 250-500 mg/day combined EPA+DHA range is common -- set one yourself as a [Profile Optimal target](#optimal) for the EPA and/or DHA rows in Settings → Nutrient targets.

Linoleic acid (omega-6) is tracked for completeness but has no established goal or known deficiency risk in a typical diet -- most diets, plant-based or not, comfortably exceed the AI for it.


### V. Profile Optimal Targets [optimal]

The standard RDA is a population-wide minimum or average -- it is not always the number that matters most for you. The clearest example is Vitamin D: the RDA is 15-20 mcg/day, but many clinicians recommend a substantially higher daily intake for older adults specifically. Rather than change what "RDA" means, NuMa lets you set your own **Optimal target** for any nutrient, on top of the standard RDA, and tracks both side by side.

Configure Optimal targets in **Settings → 7. Nutrient Targets**. Pick a nutrient, enter your target amount in that nutrient's usual unit, and save. Leave the field blank and save again to clear it. This works for any nutrient NuMa tracks -- not just ones with a standard RDA. Amino acids, EPA/DHA, and [phytonutrients](#gloss-phytonutrients) have no official [DRI](#gloss-dri) but are still valid Optimal target or [max limit](#maxlimits) candidates; amino acids in particular are more accurately evaluated by the app's [DIAAS](#diaas)-based protein quality scoring (which accounts for total protein intake), so a flat daily gram target here is a coarser measure than that -- useful mainly if you want a simple standalone tripwire for one specific amino acid.

**Loading recommended targets.** Typing values in from scratch is a lot to ask, so the Nutrient targets screen offers a **"load recommended optimal targets"** button that fills in a small curated set of commonly-cited targets -- currently Vitamin D and combined EPA+DHA (split evenly) -- for any of those nutrients you haven't already customized yourself. These are general population guidance, not personalized medical advice, and every value it loads can still be reviewed and adjusted individually afterward. See [Omega-3 Fatty Acids](#omega3) for why EPA/DHA specifically has no official DRI to compute automatically.

Once you have at least one Optimal target set, every nutrient analysis table (food, recipe, meal, and daily summary) gains a second "Profile Optimal" set of columns next to the standard "Profile RDA" columns -- the same meal %, day total %, and goal columns you already know, computed against your custom target instead of the RDA. Nutrients you have not customized show a dash ("–") in these columns rather than falling back to the RDA value, so it stays obvious which nutrients you've actually personalized.

Optimal targets are per-nutrient, not per-day -- there is no single "optimal profile" to pick, only individual overrides you add nutrient by nutrient. Color coding matches the RDA columns: green at or above target, yellow approaching it, red well short (or, for capped nutrients like sodium, red once over).


### W. Maximum Nutrient Limits [maxlimits]

Separate from the built-in Tolerable Upper Intake Level that already caps sodium in the standard RDA calculation, NuMa tracks two more tiers of daily maximum:

- **Built-in safe upper limits.** A handful of nutrients carry a real risk of harm from chronic excess, most often from supplementing rather than food alone: iron, zinc, vitamin A, vitamin B6, iodine, and selenium. NuMa applies the standard adult Tolerable Upper Intake Level for these automatically -- no setup required. You'll see them listed as "Built-in safe upper limits" on the Daily Nutrient Targets screen (**Settings → View goals**).
- **Your own custom max limits.** On top of (or instead of) the built-in defaults, you can set your own personal daily maximum for any nutrient -- useful if your situation calls for a stricter cap than the general guideline, or a cap on a nutrient that has no standard upper limit at all. A custom limit you set always takes precedence over the built-in default for that nutrient.

Configure your own max limits in the same place as Optimal targets: **Settings → 7. Nutrient Targets**.

Once a max limit is active for a nutrient -- whether it's a built-in default or one you set yourself -- NuMa watches your logged intake for the day. When today's total for that nutrient reaches 90% of the limit, the nutrient's row is highlighted yellow; at or over 100% of the limit, it turns red. This check applies to your **day total**, not to any single meal or food in isolation -- a max limit is a daily budget, and a single meal being close to it isn't itself meaningful without knowing the rest of the day.

The max-limit warning is independent of the Optimal target feature -- you can set one, the other, both, or neither for any given nutrient.


### X. Diet-Aware Bioavailability and Deficiency Notes [diet-bioavailability]

Your [dietary preference](#diet) setting (Settings → Dietary preferences) is used for more than filtering protein complement suggestions -- it also shapes two parts of your daily RDA comparison, because a vegetarian or plant-based diet changes not just *what* nutrients you're likely getting, but how much of certain ones your body can actually use.

**Iron and zinc targets are raised on vegetarian and plant-based settings.** Absorbable iron comes in two forms: heme iron (from meat, fish, and poultry, absorbed efficiently) and non-heme iron (from plants, absorbed far less efficiently, and further blocked by phytate in legumes and grains -- see [Antinutrients](#antinutrients)). Zinc absorption is reduced by the same phytate. Rather than silently under-representing this, NuMa raises the iron RDA by 1.8x[^4][^5] and the zinc RDA by 1.5x[^4][^6] when your dietary preference is set to Vegetarian or Plant-based only -- figures drawn from the Institute of Medicine's Dietary Reference Intake report and the NIH Office of Dietary Supplements' fact sheets for these two minerals. This appears as a normal, higher Daily Goal on the RDA comparison and Daily Nutrient Targets screens, with an explanatory note alongside it. Setting your preference back to "All animal foods" returns both targets to their standard values.

**A B12 warning appears for the Plant-based only setting when intake is low.** Vitamin B12 is almost exclusively animal-sourced[^7] -- unlike most nutrient shortfalls, a persistently low B12 reading on a fully plant-based diet isn't something more food logging or dietary variety fixes; it typically means a B12 supplement or B12-fortified food is needed.[^7] NuMa shows this warning only when your dietary preference is Plant-based only *and* today's B12 intake is under 50% of the RDA -- vegetarians (who still eat dairy and eggs) aren't flagged, since those foods are a legitimate B12 source and an occasional low day isn't a structural gap the way it is for a fully plant-based diet. The 50% figure is NuMa's own conservative trigger for surfacing the warning, not a clinical diagnostic threshold -- an actual B12 deficiency is properly diagnosed by a blood test (serum B12, methylmalonic acid, or homocysteine), not by a single day's logged intake.

Both of these are general population guidance based on your stated preference, not personalized medical advice -- if you have a diagnosed deficiency or absorption condition, follow your clinician's specific recommendations instead.

### Y. How NutriMagnus scores meal and recipe protein quality [protein-scoring]

(This section explains the meal-level method. For background on single-food [DIAAS](#gloss-diaas) and how amino acid ratios work, see [Appendix B](#appendix-b).)

Single-food analysis and meal-level analysis use different methods. For a single food, NuMa computes a [DIAAS](#gloss-diaas) score directly from that food's amino acid profile and digestibility. For a recipe or logged meal, it uses the [FAO](#gloss-fao)'s endorsed method for mixed-food meals: it pools the digestible amino acids across all ingredients before scoring. The two approaches answer different questions and will give different results.

#### Why meals need their own calculation

A food that is short in one amino acid can be rescued by a companion food that supplies it generously — but only if you account for both foods together. A calculation that scores each food separately and then averages the scores misses this complementarity. The pooled method captures it correctly: amino acids from every ingredient in the meal are counted together before any ratio is computed.

#### The method, step by step

NuMa applies this procedure for each of the nine essential amino acids. For the paired amino acids [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr), both members of the pair are combined before scoring, following [FAO](#gloss-fao) practice.

**For each ingredient in the meal:**

Step 1. Determine the amino acid content in grams for the actual portion eaten. [USDA](#gloss-usda) data is per 100 g; NuMa scales to the weight you entered.

Step 2. Multiply each amino acid amount by the food's true [ileal digestibility](#gloss-ileal-digestibility) coefficient — a number between 0 and 1 representing the fraction that actually reaches your bloodstream. The result is the digestible grams of that amino acid from this ingredient.

    Digestible AA (g) = raw AA in portion (g) × digestibility coefficient

[Digestibility coefficients](#gloss-digestibility-coefficient) come from published literature and are looked up automatically. Eggs and dairy sit near 1.0; whole legumes are typically in the 0.79–0.85 range; most grains and seeds fall between 0.79 and 0.88.

**Then, across all ingredients:**

Step 3. Sum the digestible grams of each essential amino acid across every ingredient. This gives nine pooled totals — one per essential amino acid.

Step 4. For each amino acid, compute the ratio of the pooled digestible total to the [FAO](#gloss-fao) reference requirement for the total protein in the meal:

    Ratio = pooled digestible AA (g) ÷ (FAO reference value × total meal protein in g)

A ratio of 1.0 means the meal exactly meets the [FAO](#gloss-fao) target for that amino acid. A ratio of 0.80 means it supplies 80% of the target — a 20% shortfall.

Step 5. The lowest ratio across all nine essential amino acids is the meal's [DIAAS](#gloss-diaas) score. The amino acid with that lowest ratio is the [limiting amino acid](#gloss-limiting-amino-acid).

#### From DIAAS to digestible complete protein

    Digestible complete protein (g) = total meal protein (g) × min(DIAAS, 1.0)

If a meal contains 40 g of total protein and a [DIAAS](#gloss-diaas) of 0.82, NuMa reports 32.8 g of digestible [complete protein](#gloss-complete-protein). The remaining 7.2 g cannot be efficiently incorporated into tissue — the [limiting amino acid](#gloss-limiting-amino-acid) is exhausted before the rest of the protein can be used.

#### A worked example — two ingredients, two amino acids

To keep the arithmetic readable, only lysine and [Met+Cys](#gloss-met-cys) are shown. The full calculation runs the same steps for all nine essential amino acids.

**The meal:**

    150 g cooked lentils:    13.5 g protein    lysine 0.94 g    Met+Cys 0.25 g    digestibility 0.83
     50 g pumpkin seeds:     12.3 g protein    lysine 0.49 g    Met+Cys 0.42 g    digestibility 0.85

Lentils are rich in lysine but short in [Met+Cys](#gloss-met-cys). Pumpkin seeds supply more [Met+Cys](#gloss-met-cys). Together they cover each other's gap.

**Steps 1–2 — digestible [AA](#gloss-aa) per ingredient:**

    Lentils:        digestible lysine   = 0.94 × 0.83 = 0.780 g
                    digestible Met+Cys  = 0.25 × 0.83 = 0.208 g

    Pumpkin seeds:  digestible lysine   = 0.49 × 0.85 = 0.417 g
                    digestible Met+Cys  = 0.42 × 0.85 = 0.357 g

**Step 3 — pool across ingredients:**

    Pooled lysine   = 0.780 + 0.417 = 1.197 g
    Pooled Met+Cys  = 0.208 + 0.357 = 0.565 g

**Step 4 — compute ratios (total meal protein = 13.5 + 12.3 = 25.8 g):**

The [FAO](#gloss-fao) reference values are 48 mg of lysine and 23 mg of [Met+Cys](#gloss-met-cys) per gram of protein.

    FAO target for lysine   = 48 ÷ 1000 × 25.8 = 1.238 g
    FAO target for Met+Cys  = 23 ÷ 1000 × 25.8 = 0.593 g

    Ratio for lysine   = 1.197 ÷ 1.238 = 0.97
    Ratio for Met+Cys  = 0.565 ÷ 0.593 = 0.95

**Step 5 — [DIAAS](#gloss-diaas) = lowest ratio:**

    DIAAS = 0.95    (Met+Cys is the limiting amino acid)

**Digestible [complete protein](#gloss-complete-protein):**

    25.8 g × 0.95 = 24.5 g digestible complete protein

Neither food alone would produce this result — lentils score poorly on [Met+Cys](#gloss-met-cys) when analyzed individually, but pumpkin seeds supply enough to bring the combined score to 0.95.

#### A note about missing amino acid data

Not every food in the [USDA](#gloss-usda) database has a complete amino acid profile. When an ingredient is missing that data, NuMa runs the meal-level [DIAAS](#gloss-diaas) calculation using only the ingredients for which data exists, and flags the result as an estimate. The digestible [complete protein](#gloss-complete-protein) figure is then computed against only the protein that comes from those data-complete ingredients — so the result remains meaningful rather than artificially inflated.

##### Filling missing AA profiles at analysis time

When a meal contains ingredients without amino acid data, NuMa tells you how many are affected and distinguishes two situations:

- **Inside a recipe**: the ingredient is part of a recipe you logged as a meal item. Fix these by opening the recipe's ingredient editor and replacing or re-fetching the ingredient there.
- **Standalone meal ingredients**: foods you logged directly to the meal (not inside a recipe). These can be replaced on the spot: NuMa asks whether you want to search for a substitute.

If you say yes, for each affected ingredient the program opens a focused search of [USDA](#gloss-usda) SR Legacy and Foundation foods — the datasets most likely to include full amino acid profiles. The **[AA](#gloss-aa)** column in the results (✓ or ✗) shows at a glance which options have the data you need. Choosing a replacement updates that ingredient for the current analysis. Press Enter to skip an ingredient and leave it excluded from the calculation.

##### Why the first analysis of a meal can be slow

When you analyze a meal for the first time, you may see a "Fetching amino acid data…" message with a brief wait — sometimes several seconds. This is normal. NuMa is going online to download complete amino acid information for each food in the meal that doesn't already have it saved locally. Once downloaded, the data is stored on your computer, so the next time you analyze the same meal it will be fast.

---

## Part 3 — Reading Your Results

This part explains what the columns, tables, and analysis screens mean.

### A. Getting help [help]

Throughout this manual, **Learn more** links appear next to section headings and analysis output. Click any link to jump to the relevant explanation, or use this manual's own search box.

The sections linked from analysis output are:

- [Amino acid estimates in complement suggestions](#comp-estimate) — what "(estimated)" and "(generic estimate)" tags mean
- [Food Cache](#food-cache-web) — fetching missing amino acid data with Claude AI
- [Amino acid scoring](#aa-scoring) — limiting-amino-acid [DIAAS](#gloss-diaas) scoring method
- [Antinutrients](#antinutrients) — what [antinutrients](#gloss-antinutrient) are and how they appear in output
- [Archiving](#archive) — hiding foods, pantry entries, and recipes from everyday use without losing them
- [Bioavailability](#bioavailability) — [DIAAS](#gloss-diaas) bioavailability table columns
- [Complement suggestions](#comp) — protein [complement food](#gloss-complement-food) suggestions
- [Daily nutrient goals](#goals) — how daily nutrient goals are calculated
- [DCP cap](#dcp-cap) — why [DCP](#gloss-dcp) is sometimes capped below the [DIAAS](#gloss-diaas) projection
- [DIAAS](#diaas) — digestible indispensable amino acid score
- [Diet-aware bioavailability and deficiency notes](#diet-bioavailability) — how dietary preference raises iron/zinc targets and flags low B12
- [Dietary preferences](#diet) — dietary preferences setting
- [Digestibility overrides](#dcp-overrides) — protein digestibility overrides table
- [Digestible complete protein](#dcp) — [DCP](#gloss-dcp) concept and formula
- [Drafted food profiles](#drafted-foods) — drafted food profiles list columns
- [Essential amino acids](#aa) — [EAA](#gloss-eaa) reference and the nine indispensable amino acids
- [FAO reference values](#fao) — [FAO](#gloss-fao) 2013 amino acid reference requirement
- [Food annotation](#annotate) — annotate food picker table columns
- [Food Cache](#cached) — [Food Cache](#gloss-food-cache) column guide
- [Food comparison](#food-comparison) — food comparison table columns
- [Food import](#food-import) — foods to import review table columns
- [Food search](#food-search) — [USDA](#gloss-usda) food search results columns
- [Food use in meals](#fooduse) — food use in meals analysis table and histogram columns
- [Glossary](#glossary) — abbreviations and key terms
- [Glycemic index](#gi) — glycemic index background
- [Glycemic load](#gl) — glycemic load concept and formula
- [Glycemic output](#glycemic) — glycemic load output columns
- [IAA ratios](#iaa-ratios) — meal amino acid ratios table columns
- [Limiting amino acid](#gap) — amino acid gaps and how they are scored
- [Maximum nutrient limits](#maxlimits) — custom per-day nutrient caps and the near-limit warning
- [Meal history](#meal-history) — meal history search result tables
- [Meal items](#meal-detail) — meal items table columns
- [Meal protein digestibility](#meal-diaas) — meal protein digestibility analysis columns
- [Meals list](#meals-list) — Meals & Log list columns
- [Meals & Log columns](#meal-columns) — choosing extra nutrient columns for the Meals & Log list
- [Missing amino acid profiles](#missing-aa) — missing amino acid profile warnings
- [My Pantry](#pantry) — [My Pantry](#gloss-my-pantry) table columns
- [N-Day nutrient trend](#trend) — averaging intake across logged days to catch chronic shortfalls
- [Nutrient analysis](#nutrients) — nutrient analysis table columns and groups
- [Nutrient plot](#nutrient-plot) — line chart of chosen nutrients across logged days (web)
- [Omega-3 fatty acids](#omega3) — ALA, EPA, DHA, and why only ALA has a Daily Goal
- [Oxalate data](#oxalate) — [oxalate](#gloss-oxalate) data source, enabling, matching, and limitations
- [Per-day profile tracking](#day-profile) — how a logged day stays pinned to the profile active when it was saved, and how to change it
- [Plot File Formats](#plot-file-formats) — PNG vs. SVG, and which to pick when downloading a chart
- [Profile Optimal targets](#optimal) — custom per-nutrient targets above the standard RDA
- [Protein completeness](#complete) — what makes a protein "complete"
- [Protein quality](#protein-quality) — single-food amino acid ratios table columns
- [RDA](#rda) — daily intake vs. recommended values table
- [Recipe ingredients](#recipe-ingredients) — recipe ingredient list columns
- [Recipes list](#recipes) — recipes list table columns


### B. Reading the output

#### Food Cache — Column Guide [cached]

The Food Cache list shows every food you have stored locally, sortable by Name, Type, DIAAS, or GI estimate. Columns:

    AA      Amino acid data status.
              ✓  Amino acid data is present in your cache for this food.
              ✗  No amino acid data — common for branded and packaged foods.

    GI      Your saved glycemic index estimate for this food, if any.
            GI reflects how quickly a food raises blood glucose (scale 0-100).
            Type ?gi for a full explanation.

    DIAAS   Your saved DIAAS estimate for this food, if any.
            DIAAS (Digestible Indispensable Amino Acid Score) rates protein
            quality: 1.00 = complete, lower = a limiting amino acid is present.
            Type ?diaas for details. Shown with a star when it's your own
            saved estimate rather than the built-in reference-table value.

    C       Confidence / source note indicator.
              ✓  A source or confidence note is saved for this food.
              —  No note.

    N       Curator notes indicator.
              ✓  Curator notes are saved for this food (typically added by the
                 Claude data-fetch workflow).
              —  No curator notes.

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
              User Drafted   — Created or edited by hand in NuMa.

    BRAND   Brand owner, for Branded and OFF foods.

See [Food Cache](#food-cache-web) in Part 5 for the available actions on each row (Portions, Refresh, Archive/Restore, Delete, Prune unused foods) and how to fetch missing amino acid data with Claude AI.


#### Archiving [archive]

Archiving lets you keep a food, pantry entry, or recipe without losing it, while hiding it from everyday use: default list views, food search results, and protein complement suggestions. It's meant for things you're not currently using but don't want to delete -- a seasonal ingredient, an old recipe you might revisit, a pantry item you've used up.

Archiving is reversible with the same action, one entry (or a batch) at a time:

**Command line:**

    Food Cache   x# (or x#,# for multiple rows) archives or restores a food,
                 based on whichever state it's currently in. s toggles
                 whether archived foods are shown in the list at all.
    My Pantry    x, then the row ID, archives or restores that pantry entry.
                 s toggles visibility the same way.
    Recipes      y{id} archives or restores a recipe (in Browse). s toggles
                 visibility.

**Web app:** an **Archive/Restore** button on each row in the Food Cache, My Pantry, and Recipes pages does the same thing; a **Show archived** checkbox on each of those pages toggles whether archived entries are shown at all.

What archiving does NOT do:

    - It never deletes anything. An archived food/pantry entry/recipe still
      exists and can be restored at any time with the same command.
    - It never breaks existing references. A recipe that uses an archived
      food as an ingredient still analyzes correctly; a meal that logged an
      archived recipe still shows correctly. Archiving only affects whether
      something shows up by default and whether it's offered for new use.
    - Archived foods are protected from u (prune unused foods) in the Food
      Cache -- archiving is meant to preserve data, so an archived-but-
      unreferenced food is never swept up by pruning.

If you try to archive a food or recipe that's still actively referenced elsewhere (a pantry entry, a recipe ingredient, a logged meal), NuMa warns you first but lets you proceed -- the references keep working either way.

This setting (which entries are archived, and whether each list shows them) is saved and persists across sessions.


#### Nutrient Analysis Table [nutrients]

Shows the nutritional content of a food, recipe, or meal portion, grouped by category (Macronutrients, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients)).

Columns:

    Nutrient     Name of the nutrient.
    Amount       Value for the portion you entered.
    Unit         kcal for calories; g for macronutrients (protein, fat,
                 carbs, fiber, omega fatty acids); mg or mcg for minerals
                 and vitamins.

When analyzing a meal within a full-day context, three additional columns appear:

    meal %       This meal's contribution to your daily goal, in percent.
    day total %  All meals logged today as a percentage of your daily goal.
    Daily goal   Your personalized nutrient target for the day.

#### Color coding (meal % and day total % columns)
    Green    At or above the daily minimum, or within the upper limit for
             capped nutrients (sodium).
    Yellow   Getting close but not there yet.
    Red      Significantly short of the minimum, or over the limit.

If you have configured a Profile Optimal target for any nutrient (Settings → Nutrient targets), the table gains a second set of the same columns under a "Profile Optimal" heading, alongside the standard "Profile RDA" columns. Nutrients you have not customized show a dash ("–") in the Optimal columns. See [Profile Optimal Targets](#optimal) for details.

If you have configured a custom max limit for a nutrient, its row is highlighted (yellow, then red) once today's total is within 10% of that limit. See [Maximum Nutrient Limits](#maxlimits) for details.

[Phytonutrients](#gloss-phytonutrients) (carotenoids, choline, isoflavones, etc.) appear only when [USDA](#gloss-usda) data for that food includes those values -- many foods have none. Amino acids are not in this table; see the Protein Quality section below it.

See [daily nutrient goals](#goals) to see how your daily goals are calculated. See [RDA](#rda) to see the Daily Intake vs. Recommended Values table.


#### Protein Quality Table [protein-quality]

Shows how a food's amino acid profile compares to the [FAO](#gloss-fao) 2013 reference pattern. Appears below the nutrient table when amino acid data is available.

The header line tells you whether the protein is Complete (all nine essential amino acids at or above the [FAO](#gloss-fao) reference) or Incomplete (at least one is limiting), and which amino acid is most limiting.

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

Color: Green = at or above 1.0 (after adjustment if Adj. is present). Yellow = below 1.0.

See [DIAAS](#diaas) for the [DIAAS](#gloss-diaas) concept. See [limiting amino acid](#gap) to understand what "limiting" means. See [FAO reference values](#fao) for the [FAO](#gloss-fao) reference values used for each amino acid.


#### Meal Protein Digestibility Analysis [meal-diaas]

Step 1 of the meal [DIAAS](#gloss-diaas) calculation. Shows how much protein from each ingredient actually reaches your bloodstream -- before the [limiting amino acid](#gloss-limiting-amino-acid) penalty is applied.

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
    ↑ user  You set a custom value (Settings -> Advanced ->
            Digestibility overrides). Type ?dcp-overrides.

Ingredients contributing less than 1 g of protein are omitted from this table as negligible; the totals row sums only the ingredients shown.

Note: the "Total digestible protein" here is step 1 of a two-step method. Step 2 (the [DIAAS](#gloss-diaas) limiting-amino-acid penalty) reduces it further. See [amino acid scoring](#aa-scoring) for the full step-by-step method. See [DIAAS](#diaas) for background on [DIAAS](#gloss-diaas) and true [ileal digestibility](#gloss-ileal-digestibility).


#### Meal Amino Acid Ratios Table [iaa-ratios]

Step 2 of the meal [DIAAS](#gloss-diaas) calculation. Shows the pooled amino acid supply across the whole meal, expressed as a ratio vs. the [FAO](#gloss-fao) 2013 reference.

Columns:

    Amino Acid   Essential amino acid (FAO pair notation for Met+Cys and
                 Phe+Tyr).
    Ratio        Pooled digestible grams of this AA from all ingredients,
                 divided by (FAO reference value x total meal protein).
                 1.0 = exactly meets the reference. Below 1.0 = shortfall.
                 Above 1.0 = surplus.
    Bar          Visual indicator; each block = 0.10, capped at 2.0.

The amino acid with the lowest ratio is the [limiting amino acid](#gloss-limiting-amino-acid), marked "LIMITING". The meal [DIAAS](#gloss-diaas) score equals that lowest ratio (capped at 1.0).

#### Color coding
    Green    1.0 or above.
    Yellow   0.80-0.99.
    Red      Below 0.80.

The panel below this table shows the final Digestible [Complete Protein](#gloss-complete-protein) figure: total meal protein x the [DIAAS](#gloss-diaas) score.

See [DIAAS](#diaas) for the [DIAAS](#gloss-diaas) concept. See [amino acid scoring](#aa-scoring) for the step-by-step two-stage calculation method. See [digestible complete protein](#dcp) for Digestible [Complete Protein](#gloss-complete-protein).


#### Bioavailability Table [bioavailability]

This section appears in two forms depending on context.

#### SINGLE FOOD (labeled BIOAVAILABILITY)

Shown when viewing a food with a saved [DIAAS](#gloss-diaas) estimate. Displays:

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

A summary panel below the table shows total digestible protein and the [pooled DIAAS](#gloss-pooled-diaas) score for one recipe serving.

See [DIAAS](#diaas) for [DIAAS](#gloss-diaas) background. See [digestible complete protein](#dcp) for Digestible [Complete Protein](#gloss-complete-protein). See [complement suggestions](#comp) for [complement food](#gloss-complement-food) suggestions.


#### Meals and Log List [meals-list]

The main Meals & Log screen lists your recent meals, 15 at a time, sorted by date (most recent first) by default. Change the sort order — Date, Name, Meal DCP, or Calories — via the sort dropdown; your choice is remembered as the default the next time you open Meals & Log.

Columns:

    Date            Date of the meal (YYYY-MM-DD).
    Complete        Checkmark when you have marked the meal finished
                    (a Mark complete / Mark incomplete button on the meal page).
    Meal            Name you gave the meal (e.g. Breakfast, Lunch).
    Items           Number of foods and recipes logged in this meal.
    Meal DCP        Bioavailable complete protein for this meal alone (g).
    Day DCP         Sum of DCP for every meal on this date with a computed
                    value — including meals not yet marked complete, since
                    DCP is auto-saved as you add items. If any contributing
                    meal isn't marked complete, the total is flagged with
                    an asterisk (*) as provisional, since it may still
                    change. Shown on the topmost row for each date only.
    % profile goal  Day DCP as a percentage of your daily protein target.
                    Also flagged with * when provisional. Shown on the
                    topmost row for each date only.
    Calories        Calories for this meal alone.

You can add up to 6 more nutrient columns of your own choosing — see
[Meals & Log columns](#meal-columns).

[DCP](#gloss-dcp) and Calories values start as -- and are computed on demand.
Opening and analyzing a meal also saves its DCP and calories automatically.

    --    Not yet computed. Use the "Calculate DCP and calories for" dropdown
          and Calculate button to compute for all complete meals, the last 30
          days, or the last 10 days (results are saved permanently).
    n/a   Computed but no amino acid data (DCP) or nutrient data (calories)
          was available.

% profile goal requires a user profile (Settings -> User profile). Blank if no profile is set.

Click a meal to view or edit it, or delete it from there. **Search meal history** searches past meals by name or date; the sort dropdown changes list order; pagination controls move between older and newer pages.

See [digestible complete protein](#dcp) for a full explanation of digestible [complete protein](#gloss-complete-protein). See [daily nutrient goals](#goals) to see how your daily protein target is calculated.


#### Meals & Log Columns [meal-columns]

The Meals & Log list always shows Calories, plus up to 6 more nutrients you
choose yourself — e.g. Sodium, Fiber, Vitamin D, or any amino acid.

To choose them: Settings -> section 8 "Meals & Log columns". Pick each nutrient's position (1 =
leftmost); leave a nutrient's position blank to hide it. This choice is saved
automatically.

Values for these columns come from the same computed snapshot as [DCP](#gloss-dcp)
and Calories, so they show -- until computed and n/a if the ingredient data
doesn't cover that nutrient. Use the Calculate button on the Meals & Log screen
(or analyze a meal) to compute them.

The same chosen columns also appear on the Daily Summary's Recent Days table
(Analysis -> Daily Summary), aggregated per day instead of per meal -- so a
day's Sodium column, for example, is the sum of every meal logged that day.

On both lists (web), a column with a unit stacks it onto its own line below
the nutrient's name (e.g. "Vitamin D" over "(mcg)"), matching the built-in
Meal DCP / Day DCP / % goal columns -- so each column takes up roughly half
the width it otherwise would.

**Recent Days also always shows four columns right after Day DCP, regardless
of what you've chosen above:** Protein (the raw, un-adjusted total -- Day DCP
is the digestibility-adjusted figure), Calories, Carbs (carbohydrates --
sugars and starches), and Fiber. These aren't part of your 6-column choice
and can't be turned off; if you'd separately picked one of them as a Meals &
Log column, it's simply not duplicated on Recent Days.

Recent Days' column headers stack a nutrient's unit onto its own line below
the name (e.g. "Vitamin D" over "(mcg)") instead of running both on one
line, so each column takes up roughly half the width it otherwise would --
letting more columns fit on screen at once.


#### Meal Items Table [meal-detail]

Shows the foods and recipes logged in a single meal.

Columns:

    ID        Item ID. Use this number with options 2 (Edit) and 3 (Remove)
              in the meal action loop.
    Amount    Portion recorded: grams for foods, or serving count for
              recipes. Volume unit labels are shown where applicable.
    Food /    Name of the food or recipe. Food items show the USDA FDC ID
    Recipe    before the name. Recipe items show "(recipe)" after the name.

To add, edit, or remove items, use options 1, 2, and 3 in the meal action loop, opened with v{id} from the meal list.


#### Food Use in Meals — Column Guide [fooduse]

Analysis -> Food use in meals tabulates which foods appear across a set of
meals you choose. You pick one selection method — one or more date ranges,
or a list of specific meal IDs (not both in the same run) — then choose
whether to include all foods or only protein-containing foods
(more than 0 g of protein per 100 g).

Columns:

    ID          USDA FDC ID for foods. Blank for recipe rows.
    Food        Food or recipe name. Recipe rows are shown in bold.
    Kind        "recipe" for recipe rows, blank for individual foods.
    Days used   Number of distinct calendar days on which this food or
                recipe appeared, within the meals you selected.
    Meals       Number of selected meals containing this food or recipe.

Rows are ranked most- to least-used by Days used (ties broken by Meals, then
name), with a bar showing relative frequency.

Recipe items are counted twice: once as the recipe itself, and again as each
of its ingredients (recursively expanded through any nested recipes), so both
the dish and its components show up in the ranking.

Recipe rows always show the recipe's *current* name and are grouped by its
stable ID — if you rename a recipe after logging it in meals, this analysis
still finds and merges every occurrence under the new name rather than
splitting them across old and new names or dropping them.


#### Glycemic Load Output [glycemic]

Shows the estimated glycemic load ([GL](#gloss-gl)) for a meal or recipe.

The number displayed is the total [GL](#gloss-gl). Color coding:

    Green   10 or below (low glycemic impact).
    Yellow  11-19 (medium).
    Red     20 or above (high).

When the output reads "Not available -- GI annotation missing for: ...", one or more foods lack a [GI](#gloss-gi) value. [GL](#gloss-gl) cannot be computed without [GI](#gloss-gi) data for every single ingredient — one missing value blocks the whole total. To fix this, annotate the listed foods via Foods → Annotate, or edit the food directly from the Food Cache.

[GL](#gloss-gl) = ([GI](#gloss-gi) x grams of available carbohydrate) / 100 per ingredient, summed across all ingredients in the meal.

[GL](#gloss-gl) is shown for reference only and does not affect protein quality scores. See [glycemic load](#gl) for a full explanation of glycemic load and its limitations. See [glycemic index](#gi) for background on the glycemic index.


#### Meal History Tables [meal-history]

These tables appear when you search your meal history with s from the Meals & Log list. Results can be shown as Flat (every occurrence), Summary (totals per food), or Both.

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

Note: only foods and recipes logged directly as meal items appear here. Ingredients inside a logged recipe are not individually searchable.


#### Missing Amino Acid Profiles [missing-aa]

When a meal contains ingredients without amino acid data, NuMa cannot include them in the [pooled DIAAS](#gloss-pooled-diaas) calculation. This section lists the affected ingredients and describes your options.

NuMa distinguishes two cases:

Standalone meal ingredients: foods logged directly in the meal.

    These can often be replaced on the spot. NuMa can search for
    a USDA Foundation or SR Legacy substitute with amino acid data.

Inside a recipe: ingredients that are part of a recipe you logged.

    These must be fixed by editing that recipe (Recipes -> browse -> edit)
    and replacing the problematic ingredient there.

It's safe to ignore when the affected food contributes negligible protein (garnish, spice, a small amount of fruit). It matters more when the food is a significant protein source in your meal. Foods contributing less than 1 g of protein are treated as negligible and left off this list entirely (a footnote tells you when items were omitted this way).

The [DIAAS](#gloss-diaas) calculation runs on whichever ingredients do have [AA](#gloss-aa) data. The result is flagged as an estimate, and the [DCP](#gloss-dcp) figure reflects only the protein from data-complete ingredients.

See [meal protein digestibility](#meal-diaas) to see the digestibility table. See [DIAAS](#diaas) for [DIAAS](#gloss-diaas) background.


#### Recipes List Table [recipes]

Shows all your saved recipes. Sorted by Last accessed by default; use the sort dropdown (not available while a search filter is active) to switch to Name or DCP/serving instead. Your choice is remembered as the default the next time you browse recipes.

Columns:

    ID          Recipe ID. Use with commands: a{id} analyze, v{id}
                view/edit, d{id} delete, c{id} copy, y{id} archive/restore.
    Name        Recipe name.
    Servings    Number of servings. 0 means the recipe is analyzed by
                total weight or volume rather than a serving count.
    DCP/srv     Digestible complete protein per serving (g). Recomputed and
                saved automatically whenever the recipe or its ingredients
                change — no separate analysis step is needed. Shown as
                NC (not computed) if servings is 0, no ingredient has a
                known weight, or an ingredient with 1 g or more of protein
                has no amino acid data. Minor contributors missing amino
                acid data (under 1 g of protein — spices, oil, salt, a
                trace of chocolate) don't block the calculation — only
                significant ones do, since an approximate DCP is never
                saved as if it were exact. The 1 g floor is absolute: it
                doesn't matter what fraction of the recipe's total protein
                that 1 g represents. In the web app, the "Compute DCP for
                all complete recipes" button on the Recipes page recomputes every
                recipe at once.
    Complete    Checkmark if you have marked the recipe finished.
    Created     Date the recipe was first saved.
    ARCH        Shown only when archived recipes are visible (s toggle) —
                dot marks a recipe as archived. See [archiving](#archive).

Commands: a{id}=analyze  v{id}=view/edit  d{id}=delete  c{id}=copy  y{id}=archive/restore  x=new recipe  /text=filter by name  r=clear filter  o=sort  s=show/hide archived  n/p=next/prev page

See [digestible complete protein](#dcp) for a full explanation of digestible [complete protein](#gloss-complete-protein).


#### Recipe Ingredient List [recipe-ingredients]

Shows the current ingredients in a recipe during create, develop, or edit. Refreshes after each change so you can see the current state.

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

Nested recipes (ID = recipe) have their nutrients scaled automatically from their recorded serving count and total weight.


#### USDA Food Search Results [food-search]

Listed after a food search. Combines matches from [USDA](#gloss-usda) FoodData Central, Open Food Facts[^3], and your local [Food Cache](#gloss-food-cache).

Columns:

    AA      Amino acid data status.
              checkmark    Confirmed in your local cache.
              ~checkmark   Likely available (Foundation/SR Legacy not yet
                           fetched); confirmed on selection.
              X            No amino acid data.

    Search results carry only a food's name and type — USDA's search results
    don't include nutrient values up front, so "~checkmark" is a guess, not a
    fact. Opening a food's page (or adding it to a meal/recipe) fetches and
    caches its full details, which is when "~checkmark" turns into a confirmed
    checkmark or X. On the web app, you can also check a batch of "~checkmark"
    results directly from the search list: tick their checkboxes (or the
    header checkbox to select all of them) and click "Fetch full details for
    selected" — this avoids looking up every uncached result on every single
    search, which would use up more of your daily USDA search allowance than
    necessary.
    GI      Your saved glycemic index estimate, if any. See [Glycemic Index](#gi).
    DIAAS   Your saved DIAAS estimate, if any. See [DIAAS](#diaas).
    CONF.   Checkmark if a confidence/source note is saved. View it from
            the Food Cache.
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

    Source  Where the match came from:
              Pantry     Already in your Pantry.
              Cache      In your Food Cache, but not the Pantry.
              Recipe     One of your saved recipes.
              USDA       Not yet cached — from FoodData Central.
              OFF        Not yet cached — from Open Food Facts.

To select: click the result. If the food is not yet in your cache, NuMa fetches and saves it automatically.

**Sort order.** Results can be ordered two ways — a dropdown above the results table lets you switch, and your choice is remembered as the default for next time:

    Best match to name (default)   See "Ordering food search results" in
                                    Part 4 for how this ranking works.
    Pantry, Cache, then Other       Groups results strictly by where they
                                    came from (Pantry, then Cache, then
                                    Recipe, then USDA/OFF) regardless of
                                    match quality; within each group, the
                                    same relevance ranking applies.

See [Ordering food search results](#search-ranking) in Part 4 for the full explanation.

**Source filter.** A second dropdown next to the results table — separate from sort order — narrows the list to just one source: All sources, Pantry, Food Cache, Recipes, USDA FoodData Central, or Open Food Facts. Each option is labeled with the short badge used elsewhere plus its full name (e.g. "USDA — USDA FoodData Central"). Your choice is sticky across every search box that has this filter, the same way the sort-order choice is. Every search results table that follows this reference — the standalone Foods → Search page, My Pantry's "Add a food" search, the Meals & Log "Add Food or Recipe" panel, and a recipe's ingredient search — has this filter.

See [Food Cache](#cached) for the [Food Cache](#gloss-food-cache) column guide. See [Food Cache](#food-cache-web) to learn how to get missing amino acid data via Claude AI.


#### Food Comparison Table [food-comparison]

Shows up to eight foods or recipe portions side-by-side, with all nutrient groups in one table. All values are per the portion you entered for each food, not per 100 g.

The foods and portions you chose are listed above the table as Food 1, Food 2, etc.

Nutrient groups: Macronutrients, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients), Amino Acids. Groups appear only when at least one food has data for that category.

    Green   The highest value in that row across all foods.
    --      No data for this nutrient in this food.

Rows where every food shows -- are hidden automatically.

To run a comparison: Foods -> Compare foods side-by-side. You can save the food list under a name for quick reuse in future sessions. Previously saved lists are offered at the start of the comparison flow.


#### Annotate Food Picker Table [annotate]

Appears when you choose Foods -> Annotate a food. Pick a food from your cache to annotate.

Columns:

    #       Row number. Type the number to select that food.
    Name    Food name.
    Type    USDA data category or OFF. Type ?food-search for type meanings.

Type /text to filter by food name (e.g. /tofu shows only tofu entries). Type / alone to clear the filter.

After selecting a food, you can add or update:

    GI      Glycemic index (0-100). Type ?gi.
    DIAAS   Your protein quality estimate (0.00-1.50). Useful for packaged
            foods that lack amino acid data in USDA. Type ?diaas.
    Prep    A short preparation note (e.g. "boiled 20 min", "raw").

Annotations appear wherever that food is used: [Food Cache](#gloss-food-cache) list, food and recipe analysis, and meal analysis.


#### Foods to Import Review Table [food-import]

Appears when you click Review on the Import Claude response page, to import the data Claude gave you. Shows a preview so you can review before confirming the write.

Columns:

    Name        Food name from the Claude response.
    FDC ID      USDA FDC ID if one was provided.
    Calories    Calorie value from the response (per 100 g).
    Protein     Protein value (g per 100 g).
    AA count    How many of the 11 tracked amino acids were found
                (e.g. 9/11 means 9 out of 11 were present).

Review each row for plausibility. If a value looks wrong, press n to cancel, correct the response file (named claude_response.txt, saved in your home folder), and re-run r.

After confirming, each food is written to your cache. Foods that gain amino acid data change from X to checkmark in the [AA](#gloss-aa) column of the [Food Cache](#gloss-food-cache). Any notes Claude added are saved as curator notes (view with c# in the [Food Cache](#gloss-food-cache)).

For the full import workflow, see [Food Cache](#food-cache-web).


#### Drafted Food Profiles List [drafted-foods]

Shows the custom food profiles you have created by hand -- products from a label, research table entries, or supplements not in [USDA](#gloss-usda) or Open Food Facts[^3].

Columns:

    #       Row number. Use to select a profile for viewing or editing.
    Name    Food name as you entered it.
    Note    Your optional source or description note.

Drafted foods are stored in your [Food Cache](#gloss-food-cache) and appear in all food searches alongside [USDA](#gloss-usda) and Open Food Facts[^3] entries. In ID columns throughout the program, drafted foods are shown as "usr".

To edit nutrient data: Foods -> [Food Cache](#gloss-food-cache), find the food, and use e#. Editing is done in the [Food Cache](#gloss-food-cache), not in this list.

To create a new custom profile: Foods -> Drafted Food Profiles -> Create. See [Food Cache](#food-cache-web) for an alternative way to get missing data (e.g. amino acid data from Claude AI for foods not in [USDA](#gloss-usda)).

**Estimating amino acids by copying from another food.** Whenever you're prompted for a food's amino acid profile (creating a drafted profile, copying a cached food, or editing any food's data), a third option lets you search for and pick a similar food that already has amino acid data, instead of typing values in or pasting from literature. The picked food's amino acids are **scaled to match this food's own protein content** (not copied raw) — a food with less protein than the source gets proportionally less amino acid content, and vice versa — the same scaling already used by hand in this app's built-in curated foods (e.g. amino acids scaled between fresh and dried okara). A note documenting the source food and scale factor is suggested automatically for the Note field. On the web app, the same picker appears as an "Estimate amino acids from another food" panel on the custom-profile edit page ([Custom Food Profiles](#custom-foods)); editing any food's data this way marks it user-drafted, same as any other edit.


#### My Pantry Table [pantry]

Shows the protein sources you have flagged as currently on hand. The Pantry drives the complement advisor -- when NuMa suggests foods to fill an amino acid gap, it checks your pantry first and shows matching foods in a "From your pantry" tier.

Columns:

    ID      USDA FDC ID, OFF, or usr -- for name-only entries.
    AA      Amino acid data status.
              checkmark  AA data in your cache. This food can be used in
                         complement suggestions.
              X          No AA data. Click Edit to add it.
              --         Name-only entry: no USDA link, no nutrient data.
                         Use Link a food to attach real data.
    Food    Food name.
    Notes   Your optional note for this pantry entry.
    Type, GI est., DIAAS   Same as the matching columns in the
            [Food Cache](#cached) list — see the DIAAS entry there for
            how the saved-estimate-vs-reference-table value is chosen.
    ARCH    Shown only when archived entries are visible (the show-archived
            toggle) — a dot marks an entry as archived. See [archiving](#archive).

Only pantry foods with [AA](#gloss-aa) data (checkmark) appear in complement suggestions. Name-only entries (--) and those without [AA](#gloss-aa) data (X) may still appear if their name matches a built-in complement table entry. Archived pantry entries never appear in complement suggestions.

Actions: **Add a food** (USDA search or name-only — the search results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns), **Remove**, **Archive/Restore** (see [archiving](#archive)), and an **Edit** button on each row that jumps straight to that food's Food Cache entry for editing. A name-only entry (no USDA link) shows a **Link a food** button instead — search and pick a match to attach real nutrient data to that same pantry row, rather than adding a duplicate.

See [complement suggestions](#comp) for how complement suggestions use your pantry.


#### Protein Digestibility Overrides [dcp-overrides]

Shows your custom true [ileal digestibility](#gloss-ileal-digestibility) coefficients. These values override the defaults NuMa uses in meal-level [DIAAS](#gloss-diaas) calculations.

Columns:

    Food name       Name of the food this override applies to (matched
                    case-insensitively against meal ingredients).
    Digestibility   Your custom coefficient (0.00-1.00). The fraction of
                    protein absorbed by the small intestine.
    Notes           Your source note (e.g. "Smith 2020 Table 3").

When an override is active for a meal ingredient, the Digestibility column in the Meal Protein Digestibility table shows the value with a "↑ user" marker next to it, distinguishing it from estimated or literature defaults.

Use overrides when you have found a published measured value for a food you eat regularly and it differs meaningfully from NuMa's default. Values should come from primary literature ([ileal digestibility](#gloss-ileal-digestibility) studies), not from product labels or general nutrition sources.

Commands:

    a   Add or update an override (enter food name, then coefficient).
    d   Delete an override.

See [meal protein digestibility](#meal-diaas) to see where this value appears in the analysis output. See [DIAAS](#diaas) for background on true [ileal digestibility](#gloss-ileal-digestibility).

---

## Part 4 — Shared Operations

Several operations show up in more than one place in the app — the same mechanism behind a search box on three different pages, say. This Part collects those, so they're documented once instead of several times, with a link back here from every place they apply.

### A. Setting up your computed daily nutrient targets [daily-nutrient-targets]

This is a table of your personalized nutrient targets, computed from your profile: calories, protein, carbohydrates, fiber, every tracked mineral, and every tracked vitamin — each labeled with its goal type (minimum, target, or upper limit). See [daily nutrient goals](#goals) for the formulas behind these numbers, and [RDA](#rda) for where the underlying reference values come from.

This appears as its own read-only Settings panel and updates automatically whenever **Your Profile**, just above it, changes. It requires an active profile — if the table looks empty or the numbers seem off, check that your profile (age, sex, weight, height, activity level) is filled in first.

**Archiving vs. deleting** is documented once, in Part 3's [Archiving](#archive) reference, so it isn't repeated here.

**Every percentage shown elsewhere carries its goal type too, not just this table.** A percent-of-target is meaningless on its own — 120% is good news for a minimum (protein: you've cleared the bar) and bad news for a limit (sodium: you're over the cap). Wherever a nutrient's percentage appears — on a food, meal, recipe, daily summary, or trend page — it's followed by a small `min`, `max`, or `target` tag (hover it for the full explanation), so you never have to come back to this table to know which direction is good.

### B. Dietary Preferences (Settings → 4) [diet]

This setting controls which protein sources appear in complement suggestions and food search results throughout the program. Change it under **Settings → Dietary preferences**.

| Option | Setting | Includes |
|---|---|---|
| 1 | All animal foods | meat, fish, dairy, and eggs |
| 2 | Vegetarian | dairy and eggs only (no meat or fish) |
| 3 | Plant-based only | plant sources only |

The setting is saved between sessions and applies to both the interactive complement display and any exported reports.

**A quick-switch control sits right above every Protein Complement Suggestions list** — a dropdown pre-set to your current preference, plus a "Change settings" link straight to this section. Picking a different option in the dropdown saves it immediately and reloads the suggestions for the new preference, without leaving the page you're on — useful when you want to see, say, what a plant-only complement would look like without permanently changing your setting (just switch it back the same way afterward).

**Important — this setting also filters food search results, not just complement suggestions.** If your preference is set to "plant-based only" or "vegetarian", foods outside that category will not appear anywhere in NuMa — not in food searches, not in search results within recipes or meals, and not in any lookup by name or [FDC ID](#gloss-fdc-id). If you search for a food and get no results, check whether your dietary preference setting is silently excluding it. To look up any food regardless of category, temporarily switch to "All animal foods" under Settings, do your search, then switch back.

### C. Ordering food search results [search-ranking]

When you search for a food — whether from the Food Search page, the Meals & Log "Add Food or Recipe" panel, or a recipe's ingredient search — NuMa has to decide what order to show the matches in. That's a harder problem than it sounds, because "best match" usually means several different things at once: does the name contain your search words? All of them, or just some? And does it matter which words a near-miss is missing?

**The short version:** results are ranked first by how many of your search words appear in the name — an item matching every word you typed always outranks one matching only some of them, which always outranks one matching none. Only once that's settled does it matter whether the food happens to be sitting in your Pantry, your Food Cache, one of your Recipes, or hasn't been fetched yet at all — a genuinely better text match always wins over a weaker one, regardless of where it came from. Earlier versions of NuMa got this backwards for cache and pantry items: being already-on-hand could outrank an actual match to what you typed, which meant an unrelated pantry item could occasionally show up ahead of the food you were actually looking for.

**Word order matters, too.** If you type more than one search word, NuMa treats the order you typed them in as a signal of what matters most to you. Suppose you search `milk dry instant` because there are two kinds of dry milk — instant and non-instant — and you specifically want the instant kind, but you've put "dry" before "instant" because that's the more important distinguishing word to you. If nothing in your data matches all three words, NuMa prefers a match on `milk` + `dry` over a match on `milk` + `instant`, precisely because you typed "dry" first. In effect, the words you type earlier act as your stated priorities — a partial match that preserves your earlier words beats one that preserves only a later one, even when both partial matches contain the same number of words.

This means you can deliberately front-load your most important search word when you know a food name might be ambiguous or your data might be incomplete — put the word you care most about disambiguating on first, and let NuMa's ranking favor it if a perfect match isn't available.

*(For technically skilled users: the exact algorithm — including how word order is encoded as a simple bitmask comparison — is documented in `README-numa-documentation.md`, under "Searching for a food.")*

**When several results tie on text relevance, USDA data quality breaks the tie before name length does.** A dozen near-identical branded listings (say, a dozen "INSTANT NONFAT DRY MILK" products) can match your search words exactly as well as the one or two Foundation/SR Legacy foods actually named that — and branded names are often shorter, which used to let them win the final tiebreak even though they're the ones least likely to carry real amino acid data. Ties are now broken by data quality first (Foundation/SR Legacy, then Survey/Experimental, then Branded/Open Food Facts) and only fall back to shorter-name-wins after that, so the reference food most likely to actually answer your question surfaces before its branded look-alikes.

**Your own data is always checked first.** Before NuMa ever reaches out to USDA or Open Food Facts, it checks your local Food Cache and Pantry — a match there appears instantly, with no network round-trip. USDA and Open Food Facts results are still fetched right behind it (not only when the local check comes up empty), so a food newer than your cache, or one you've never looked up before, still turns up — it just takes a moment longer to appear, and once it does, the whole list is re-ranked together rather than just tacked on below the instant results — so a strong external match still lands above a weak local one, even though the local one rendered first. A 12- or 13-digit barcode (UPC-A or EAN-13) skips general search entirely and goes straight to a direct Open Food Facts lookup by that exact code.

**Search result depth.** Plain, unprocessed foods (the ones most likely to carry full amino acid data) can get buried under branded or prepared-dish matches for the same word — USDA's own relevance ranking can push something like "Potatoes, flesh and skin, raw" 15–20 results deep for a plain "potato" search, or return two dozen canned/branded products before a plain cooked bean shows up for "pinto beans." To counter this, NuMa runs a second search pass restricted to Foundation Foods and SR Legacy (USDA's most complete, least processed data), so those results aren't lost in the noise. How many results that second pass fetches is configurable (Settings → Advanced settings → Search result depth) — the default of 25 is enough for the vast majority of searches; set it higher if you still don't see the food you expect, or to 0 to remove the cap entirely (every matching result USDA returns, in one page — a higher number means a slightly slower search).

### D. Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it [recipe-dcp-cascade]

A recipe can be used as an ingredient inside another recipe — a lentil sauce that shows up in three different dinners, say. Editing and saving that base recipe recalculates its own digestible complete protein ([DCP](#gloss-dcp)) automatically. If it's also used as a sub-recipe ingredient elsewhere, saving it recalculates DCP for every recipe that depends on it too — directly, or through another sub-recipe in between — so a foundational recipe's protein score is never left stale in anything built on top of it. You never need to manually recompute a dependent recipe just because you changed the recipe it's built from.

A bulk "recompute DCP for all recipes" option still exists on the Recipes list — worth running after a bulk import, or if you suspect stale numbers predating this cascading recalculation.

### E. Entering custom foods and dietary supplements [custom-foods]

#### Custom (drafted) food profiles

When a food isn't in USDA or Open Food Facts[^3] — or the entry you found is incomplete — create a custom profile from an existing food as a starting point, or from scratch, via Foods → Custom food profiles → Create.

Whichever interface you use, the same fields apply:

- **Name** — what to call this food in searches and meal logs.
- **Supplement mode** (see below) or a normal serving size and unit.
- **Basic macros** — calories, protein, total fat, carbohydrates, fiber, sugars, saturated fat, mono/poly fats, sodium. Always required.
- **Minerals, vitamins, amino acids, and [phytonutrients](#gloss-phytonutrients)** — all optional. For vitamins A, D, and E you can type the amount in IU (e.g. `400 IU`) and NuMa converts it automatically; amino acids can be entered one-by-one or pasted in as a block from a research table (g per 100 g protein — converted automatically).
- **Note** — document your source or any caveats about the data.

Once saved, the food appears in every search and can be used in meals and recipes exactly like any other food. Edit or delete it from the same place you created it, at any time.

#### Dietary supplements — tablets, capsules, softgels

Supplement labels give amounts per tablet, not per 100 g. NuMa handles this with **supplement mode**: create a custom food profile as above, set the serving size to **1** with a unit of `tablet`, `capsule`, `softgel`, or similar, then enter the nutrient amounts exactly as printed on the label. Logging "1 [unit]" in a meal then adds exactly those label amounts to your totals — no weighing involved, and no conversion math on your part.

**Tip:** try a barcode search first (the 12- or 13-digit number on the label, entered at any search prompt). Many supplement products are already in Open Food Facts[^3] with complete data, saving you the manual entry.

To convert an existing custom food to supplement mode, edit it and change the serving size to **1** with a unit of `tablet`, `capsule`, or similar, same as creating one from scratch.


### F. Deleting a recipe that's used elsewhere [delete-recipe-elsewhere]

If another recipe uses the one you're deleting as a sub-recipe (an ingredient that is itself a recipe), NuMa warns you before deleting. If you delete it anyway:

1. That ingredient line is not removed. It stays in place, but is now flagged "recipe (deleted)" wherever it appears — in ingredient lists, meal history, and Food Use in Meals. This is expected, not a bug: NuMa can't know whether you meant to also cascade-delete every recipe that depended on it, so it leaves the reference intact and visible instead.
2. If you later create a new recipe whose name shares at least one word with the deleted recipe's name (for example, re-creating "Beef Stew" as "Chicken Stew," or under the exact same name as before), NuMa offers to relink those broken references to your new recipe — the offer appears as a banner on the new recipe's edit page.
3. If more than one deleted recipe matches by name, you're offered each one separately, and only the ones you confirm get relinked. Declining leaves the old references flagged as before.
4. To see every currently-broken reference in your data, regardless of what you're about to create, use the "Broken recipe references" button on the Recipes list.

### G. Ignoring a complement suggestion [ignore-complement]

Every [complement suggestion](#comp) — a Tier 1 gap closer, a Tier 2 [DIAAS](#gloss-diaas)-boosting option, or a food inside a Tier 3 two-food combination — carries an "Ignore this suggestion in recalculation" checkbox. Check one or more, then click **Recalculate complements** (it activates as soon as anything is checked) to reload the page with those foods excluded from every tier — pantry, general, two-food combinations, and DIAAS boosters all rebuild around the remaining candidates. Use this when a suggested food genuinely isn't an option for you (out of stock, disliked, already ruled out for some other reason) and you'd rather see the next-best alternative than one you can't act on.

Ignoring more foods on a later recalculation adds to the list rather than replacing it. A collapsible "Ignoring N suggestions — manage" panel lists every currently-ignored food alphabetically, each with its own "Remove ignore" checkbox to restore just that one; a "Clear all" link removes the whole list at once.

The ignored list is not saved anywhere — it resets the moment you navigate away, or reload the page without it. Available on the Food detail, Meal, and Recipe pages.

---

## Part 5 — Using the Web App

This is the program most user needs. NuMa's web app runs in your ordinary browser — there is nothing to install and no command line involved.

### A. Opening NutriMagnus

Launch NuMa the way it was set up on your computer — a desktop icon, an Applications-menu entry, or a shortcut someone set up for you. It opens automatically in your browser, normally at an address like `http://127.0.0.1:8000` — this just means "this computer, talking to itself," not an address on the internet, so don't worry if the exact numbers you see differ. If the page doesn't load right away, wait a few seconds and reload — the program is still starting up.

### B. Finding your way around

Every page has the same navigation bar across the top: **NuMa** (takes you home), **Foods**, **Recipes**, **Meals & Log**, **Analysis**, **Settings**, and **Manual** (this document). **Foods** and **Analysis** open as drop-down menus with several choices each; the others go straight to their page.

If you'd rather use the keyboard, each nav item has a shortcut — hold **Alt+Shift** and press the item's first letter (`F` for Foods, `R` for Recipes, `M` for Meals & Log, `N` for Analysis, `S` for Settings, `A` for Manual), using the underlined letter shown in each menu item and Settings section heading (e.g. `Alt+Shift+3` jumps to Dietary Preferences within Settings). For a dropdown menu item (Foods, Analysis), the shortcut also moves keyboard focus straight to the first item in the menu that opens — from there, ArrowUp/ArrowDown moves between items, Enter or Space picks one, and Escape closes the menu, all without touching the mouse. This is a browser-side feature — it is unrelated to, and does not affect, anything stored in your NuMa data. Turn it on or off in **Settings → Keyboard Shortcuts**; the setting is stored in your browser (not synced across devices) and takes effect immediately, with no page reload needed.

Most detail pages (a food, a recipe, a meal) show a collapsible outline down the side — click a heading there to jump straight to that section. Forms that have unsaved changes mark their Save button so you can tell at a glance whether you've edited something, and the browser will warn you before you navigate away from an unsaved form.

#### Search boxes remember your last search [search-memory]

On a meal's "Add Food or Recipe" search, a recipe's "Add Ingredient" search, and the Foods: Search page, if you follow a link away to look something up elsewhere and then come straight back to that exact page, your last search and its results are restored automatically — you don't have to retype it. This only applies to a plain link back to the page (the browser's own Back button already preserves it); it's scoped per page, so it never leaks a search from one meal into another.

There's no time limit on this — it holds for as long as your browser tab stays open, not just for a moment after you step away. Clicking **Reset search** (shown next to the search box whenever a search is active) or closing the browser tab clears it back to the page's clean, empty-search state.

The main navigation bar goes further than any one page: clicking **Recipes**, **Meals & Log**, **Settings**, or **Manual** returns you to the exact page you were last on in that section — e.g. the specific recipe you were editing, search and all — instead of always landing on its list page. When that memory is what brought you back, the page's breadcrumb is highlighted, with a one-click "All recipes" / "All meals" link in case you actually wanted the plain list. **Foods** is a drop-down of separate destinations (Search, Compare, Pantry, and more), so it works a little differently: a small "↩" quick-return link appears next to it whenever there's a food you've viewed, showing that food's name, so you can jump back to it in one click after wandering off elsewhere. Following a breadcrumb link (e.g. **Recipes** at the top of a recipe page) back to the list always starts fresh, clearing any remembered search or position.

### C. Sample Workflows [sample-workflows-web]

**Use this as a tutorial!** With NuMa open in your browser, work through these step by step, paying close attention to what appears on your screen. Each workflow is self-contained — you don't need to read Part 2 (nutrition concepts) or Part 3 (reference) first; terms are briefly explained in place.

**Workflows 1–3 are a single connected thread, not a tour of every menu.** They follow one feature end to end — protein complementarity — because it's NuMa's most distinctive capability. Right after them, a short "a few more things worth trying" section highlights a few other Foods and Recipes features these three don't touch, and Workflow 4 does the same connected-thread treatment for Meals & Log paired with Analysis.

---

#### Workflow 1 — Looking up a single food and finding its protein gaps

**What this shows:** how to search for a food, read its nutrient profile, and get automatic protein complement suggestions drawn from the built-in protein source list.

**Step 1 — Open the Foods menu.** Click **Foods** in the top navigation bar. A dropdown appears with nine numbered items.

**Step 2 — Search for a food.** Click **2. Analyze a food portion**. A search box appears. Type `brown rice cooked` and click **Search**. NuMa queries [USDA](#gloss-usda) FoodData Central and returns a ranked list of matches. Click the Foundation Foods entry — Foundation Foods have the most complete amino acid data.

**Step 3 — Choose a portion.** The food detail page opens. Near the top you will see a portion input field. Type `1 cup` (or select it from the named portions dropdown if it appears) and click **Recalculate nutrients**.

**Step 4 — Read the nutrient table.** The page now shows the full nutrient profile scaled to your chosen portion. Click the **Nutritional Analysis** section header to expand it — you will see macronutrients, minerals, vitamins, and amino acids.

**Step 5 — Read the protein quality section.** Click **Protein Quality** to expand it. NuMa shows a per-amino-acid score table. Brown rice is low in lysine — its lysine score will be well below 1.0 (the [FAO](#gloss-fao) reference floor). This is the [limiting amino acid](#gloss-limiting-amino-acid).

**Step 6 — Read the complement suggestions.** Click **Protein Complement Suggestions** to expand it. Because a gap exists, NuMa lists the amino acid(s) you're short on under **Gaps**, then shows foods that can close them under a **Suggestions** heading (or **Other options** if pantry items also qualified — see Step 5 of Workflow 2). Suggestions are ranked by smallest amount needed. You might see, for example, that adding 45 g of lentils would close the lysine gap and bring the combined protein to a complete profile.

**What you learned:** NuMa can tell you BOTH what is in a food AND what is missing — and exactly what to add to fix it.

---

#### Workflow 2 — Analyzing a meal with pantry items as complement candidates

**What this shows:** how recording your own protein sources in the Pantry makes complement suggestions personal and practical, drawing on foods you actually have.

**Before you start, set up your profile.** Click **Settings**, fill in your age, sex, weight, height, and activity level, and save. This is what lets NuMa compare your protein intake against a target built for you, rather than a generic default — you'll see it reflected in the % goal figures later in this workflow and in Workflow 4.

**Step 1 — Add a food to your Pantry.** Click **Foods** in the navigation bar, then click **7. My Pantry**. On the Pantry page, type `hemp seeds` into the search box under "Add a pantry item — search for full amino acid data" and click **Search**. A results table appears — click **Add to pantry** next to the best match. (The separate "Quick add by name only" box further down the page skips the search and saves just the name, with no nutrient data — use it only when you can't find a match.)

**Step 2 — Create a meal.** Click **Meals & Log** in the navigation bar. Click **New Meal**, give it a name (e.g., "Lunch today"), and a date. The meal page opens with a search box. Type `brown rice cooked`, click **Search**, then click the matching food and enter `1 cup` as the portion. Repeat with `black beans cooked` at `½ cup`. Both foods now appear in the meal's item list.

**Step 3 — View the meal's nutrition analysis.** Scroll down on the meal page. The **Nutritional Analysis**, **Meal-Level Protein Analysis**, and **Protein Complement Suggestions** sections are collapsed by default — click each header to expand it. NuMa aggregates the nutrients across both foods and shows a combined profile.

**Step 4 — Read the protein analysis section.** Rice and beans together improve each other's amino acid profile significantly — this is protein complementarity in action. The combined score will be higher than either food alone.

**Step 5 — Read the complement suggestions.** Because you now have a pantry item, the suggestions are organized into two headings: **From your pantry & recipes** (hemp seeds will appear here if it qualifies as a gap-closer for this meal) and **Other options** (the same built-in list from Workflow 1). Suggestions drawn from your pantry reflect a food you actually have, not just a theoretical option.

**What you learned:** Building even a small pantry of protein sources you keep on hand transforms complement suggestions from generic advice into a practical shopping and cooking guide.

---

#### Workflow 3 — Using an analyzed recipe as a complement candidate

**What this shows:** how recipes you have analyzed become available as complement options for other foods and meals, so NuMa can suggest "add 250 g of your lentil soup" rather than just "add lentils."

**Step 1 — Create and analyze a recipe.** Click **Recipes** in the navigation bar, then click **New recipe**. Give it a name such as "Lentil soup" and fill in the servings count. On the recipe edit page, add ingredients one at a time — for example, lentils (200 g), onion (80 g), garlic (10 g), and vegetable broth (500 g). Save the recipe details, then add each ingredient via the ingredient search box. The recipe detail page shows its Nutritional Analysis and [Complete Protein](#gloss-complete-protein) Analysis, computed automatically. Expand those sections to see the full protein profile and [DCP](#gloss-dcp).

**Step 2 — Look up a food with protein gaps.** Click **Foods** in the navigation bar, then click **2. Analyze a food portion**. Search for `corn tortilla`. Click the result, then enter `46 g` (about 2 tortillas) in the portion field and click **Recalculate nutrients**. Expand **Protein Quality** — corn is low in lysine and tryptophan.

**Step 3 — Read the complement suggestions.** Expand **Protein Complement Suggestions**. Under **From your pantry & recipes**, your lentil soup recipe appears as a candidate, tagged `(#id, Recipe)` next to its name so you can tell it apart from a plain food. NuMa shows how many grams of the recipe would close the gaps in the corn tortillas — for example, "Serve alongside: 180 g."

**Step 4 — Note what changes as you build up data.** The more recipes you analyze and the more pantry items you add, the more the complement suggestions reflect your actual kitchen — each qualifying recipe or pantry item appears as its own candidate card under **From your pantry & recipes**.

**What you learned:** NuMa's suggestions become progressively more useful as you add your own data. The built-in list ensures you always get suggestions even on day one; your pantry and recipes make those suggestions yours.

---

#### A few more things worth trying

Workflows 1–3 follow one thread — protein complementarity — since it's NuMa's most distinctive feature. A few other things worth a look, once you've got the basics down:

**Foods → Compare.** Add up to eight foods side by side in one table (checkboxes in the search results, a gram amount for each) — a quick way to answer "which of these is actually better for me" instead of flipping between separate detail pages. A comparison can be saved under a name and reopened later.

**Foods → Custom food profiles.** Enter a homemade dish, a supplement, or a product NuMa's databases don't have (or have incompletely) — either from scratch, or by copying an existing cached food as a starting draft and editing its nutrients from there.

**Recipes: use one recipe inside another.** A recipe can be added as an ingredient of another recipe — a lentil sauce used inside three different dinners, say. Editing and saving the base recipe keeps every recipe built on it up to date automatically — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 4.

**Recipes → Archive/Restore.** Hide a recipe (or a food, or a pantry entry) you're not using right now without deleting it — see [Archiving](#archive) in Part 3.

---

#### Workflow 4 — Logging several days, then spotting a pattern in Analysis

**What this shows:** how Analysis turns a handful of logged days into something a single meal — or even a single day — can't show you: a full day's combined nutrition, and a pattern across many days.

**Step 1 — Log a couple more days.** Click **Meals & Log → New Meal** and create two or three more meals across two or three different dates — reuse foods from Workflows 1–3 if you'd like to keep it quick (`brown rice cooked`, `black beans cooked`, `corn tortilla`).

**Step 2 — Analyze a full day.** Open any one of the meals on a date where you logged more than one — a button reading **Analyze full day (N meals)** appears near the top of the page whenever that's the case. Click it. NuMa pools every meal logged that date into one combined analysis — total nutrients, pooled protein quality, and complement suggestions across everything you ate that day, rather than meal by meal.

**Step 3 — Check the Daily Summary.** Click **Analysis → 1. Daily summary**. The Recent Days table lists every date you've logged: Day DCP, then Protein, Calories, Carbs, and Fiber (built in for every day, right after Day DCP), then your goal in grams and % of it. Click any date to reopen that day's full analysis.

**Step 4 — Catch a chronic pattern with Multiday Nutrient Trend.** From the Daily Summary page, click **Multiday nutrient trend** and choose a 7, 14, or 30-day window. NuMa averages your intake over that window and compares it to your RDA targets — surfacing a nutrient that's persistently a little low, the kind of gap a single good or bad day would hide.

**Step 5 — See the shape of it with Nutrient Plot.** Click **Nutrient plot** instead. Check Day DCP and Protein (or any other nutrient you're curious about), then click **Plot**. NuMa draws a line chart across your logged days — sometimes a shape on a chart makes a pattern obvious in a way a table of numbers doesn't.

**What you learned:** Analyzing a full day rolls up everything you ate; Daily Summary tracks that day by day; Multiday Trend and Nutrient Plot turn many days into a pattern you can act on — two different views (numbers-against-target, and shape-over-time) of the same underlying data.

---

### D. Using the Foods menu

#### Search (Foods → Search)

Type any part of a food name, an [FDC ID](#gloss-fdc-id) number, or a 12/13-digit barcode (UPC-A or EAN-13) — see [Your own data is always checked first](#search-ranking) in Part 4 for how results are sourced and ordered. Click a result to open its full [Nutritional Analysis](#nutrients), [Protein Quality](#protein-quality), and complement-suggestion page.

#### Analyze a food portion / Analyze a saved recipe portion

Shortcuts into Search that take you straight to entering an amount once you've picked a food or recipe, rather than seeing the per-100g view first.

#### Convert

A pure unit-conversion tool — search for a food, then type any amount (`3 oz`, `1/4 cup`, `150 g`) to see its gram/mL equivalent and the closest named portion size. No nutrient analysis is shown here; use Search for that.

#### Compare

Add up to eight foods (checkboxes in the search results) and set a gram amount for each to see them side by side in one nutrient table. Comparisons can be saved under a name and reopened later, renamed, or deleted.

#### Food Cache [food-cache-web]

Every food NuMa has ever fetched from USDA or Open Food Facts[^3] lives here — see the [Food Cache column guide](#cached) in Part 3 for what each column means. Per-food actions: **Portions** (add or edit named portion sizes), **Refresh** (re-fetch nutrient data from USDA while keeping your portions and notes), **Archive/Restore** ([hide without deleting](#archive)), and **Delete**. **Prune unused foods** removes cache entries no pantry entry, recipe, or meal is currently using.

**Fetching missing amino acid data with Claude AI.** Some foods — especially branded or prepared items — arrive without amino acid data. Check the boxes next to the foods you want (or click "Select all missing AA data" to grab every food currently missing it), then click **Fetch missing data from Claude AI**. This builds a ready-to-send prompt and shows it on its own page with a **Copy prompt to clipboard** button. From there:

1. Go to [claude.ai](https://claude.ai) — open a **new chat** (not an existing one) — paste the prompt, and send.
2. When Claude finishes, copy its entire reply (all of it, including every ` ```json ` block — if Claude splits its answer across multiple messages, copy each one and paste them together).
3. Back in NuMa, click **Import Claude response** (also reachable directly from the Food Cache page), paste the reply into the box, and click **Review**.
4. NuMa shows you a table of what it understood from the reply — name, FDC ID, calories, protein, and how many of the 11 tracked amino acids were found — plus any warnings about data it couldn't use. Check it over, then click **Import** to save it to your cache.

#### My Pantry

Foods you keep on hand — see [My Pantry](#pantry) in Part 3 for the column guide. Pantry foods are checked first for complement suggestions and search results. Add a food with full nutrient data via search, or use **Quick add by name only** for something you haven't looked up yet (link it to real data later with **Link a food**).

#### Custom food profiles

Create a food NuMa doesn't already have — a homemade dish, a supplement, or a product with an incomplete database entry. Either start from scratch, or **copy a cached food as a draft** and edit its nutrients from there. See [Entering custom foods and dietary supplements](#custom-foods) below.

#### Annotate

A list of cached foods where you can enter a glycemic index estimate, a [DIAAS](#gloss-diaas) estimate, prep-context notes, or check "don't ask again" for a specific nutrient. NuMa also opens this automatically as a follow-up prompt right after certain actions when data is missing — you can skip it for now or skip it permanently for that food.

### E. Opening a food's detail page

A food's page shows, in order: **Protein Summary** (DCP), **Nutritional Analysis** (type any amount, or pick a named portion, then click **Recalculate**), **Protein Quality** ([DIAAS](#diaas) and the per-amino-acid table), **Anti-nutrients**, **Complement Suggestions** (pantry foods first, then general suggestions, then two-food pairs and combos — each can be [ignored and recalculated](#ignore-complement)), and an **Add to Pantry** form at the bottom. If the food has no amino acid data, you'll see a suggestion to search for a Foundation or SR Legacy equivalent instead — those datasets are the ones most likely to have complete amino acid profiles.

### F. Using the Recipes menu [recipes-menu-web]

The **Recipes** page lists every recipe, with filter/sort options and a **Show archived** checkbox. Row actions: **Edit**, **Copy**, **Archive/Restore**, **Delete**. **Recompute DCP for all recipes** refreshes every recipe's protein score at once, and **Broken recipe references** finds any recipe whose sub-recipe ingredient was since deleted — see [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) in Part 4.

Editing a recipe's ingredients or servings recalculates its own [DCP](#gloss-dcp) automatically, and cascades to every recipe that depends on it too — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 4. You don't need **Recompute DCP for all recipes** just because you changed one recipe; it's there for after a bulk import, or if you suspect stale numbers from before this cascading recalculation existed.

- **New recipe** — a short form (name, description, servings, total yield) that drops you straight into editing.
- **Edit** — a details form plus an ingredients table. Add an ingredient by searching — the results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns and the "Fetch full details for selected" AA-confirmation button — then typing a portion (`150 g`, `1/2 cup`, or a saved preset like `p1`); reorder ingredients with the up/down controls, or edit or remove one inline. A **Running totals** card at the side updates live as you add ingredients, showing calories, protein, and DCP for the whole recipe and per serving.
- **Detail** — mirrors a food's detail page (Protein Summary, Ingredients, Procedure, Nutritional Analysis, [Complete Protein Analysis](#meal-diaas) with per-ingredient digestibility, Missing AA Profiles, Complement Suggestions — [ignorable and recalculable](#ignore-complement) here too, [Glycemic Load](#glycemic), Anti-nutrients), plus a servings field to re-analyze at a different batch size. **Print/save recipe** opens a stripped-down, print-friendly version in a new tab.

### G. Using the Meals & Log menu

The **Meals & Log** page has a **New Meal** form at the top (name + date), filters for date and sort order, a **Search meal history** link for full-text search across everything you've ever logged, and a batch button to calculate DCP and calories for all meals, or just the last 10 or 30 days. The list itself shows each meal's completeness, item count, Meal DCP, Day DCP (combined across all meals on that date), % of your daily goal, and calories.

Open a meal to add foods or recipes (search box at top — for a recipe you can log the whole thing or just individual ingredients), edit or remove items inline, mark the meal complete/incomplete, rename it or change its date, or merge it with other meals logged the same day. Below the item list: [Nutritional Analysis](#nutrients), [Meal-Level Protein Analysis](#meal-diaas) (with a **Refresh from USDA** button if amino acid data needs updating), Missing AA Profiles, Complement Suggestions ([ignorable and recalculable](#ignore-complement)), [Glycemic Load](#glycemic), and Anti-nutrients.

If more than one meal is logged on the same date, **Analyze full day** rolls all of them into one combined analysis — total nutrients, pooled protein quality, and complement suggestions across everything you ate that day.

### H. Using the Analysis menu

- **Daily summary** — a table of recent days with Day DCP and % of goal; pick a date to see that day's full analysis (same sections as the full-day meal view). From here, follow the **Multiday nutrient trend** link to see 7/14/30-day averages — useful for catching a chronic shortfall that a single good or bad day would hide.
- **Food use in meals** — see how often you've eaten a given food or recipe. Choose either a date range or a specific list of meal IDs, optionally limit results to protein-containing foods, and get a sortable table with a visual frequency bar.

### I. Using the Settings menu

Settings is organized into collapsible sections: **Your Profile** (age, sex, weight, height, activity level — this drives all your daily nutrient targets — plus a checkbox enabling [oxalate](#oxalate) lookup), **Computed Daily Targets** (see [Part 4](#daily-nutrient-targets)), **Dietary Preferences** (affects complement suggestions, [B12/iron/zinc guidance](#diet-bioavailability), and — see [Dietary Preferences](#diet) — every search and lookup in the program), **Keyboard Shortcuts**, **USDA API Key** (lets you use your own free personal code from USDA's website instead of the one NuMa shares with every user by default, so your searches are less likely to get temporarily blocked when many people are using NuMa at once — see [Food data](#food-data) for how to get one; also has the [search result depth](#search-ranking) setting), **Protein Digestibility Overrides** (custom digestibility numbers for specific foods), **Nutrient Targets** (optional per-nutrient Optimal targets and Max limits, with a one-click button to load recommended defaults), and **Sample Data** — see below.

#### Sample Data [demo-data]

A one-click way to populate the app with example content: real USDA foods (with full amino-acid data), a few of them in your pantry, and two recipes picked to show protein complementarity actually working — "Black Beans & Rice" and "Lentils & Oats Bowl," each combining a legume and a grain so the amino acids each is short on are covered by the other. Useful for exploring what the app does before you've built up your own data, or for trying it out on a fresh install.

Loading sample data never touches anything already in your cache, pantry, or recipes — it's tracked separately so **Clear sample data** (which appears once it's loaded) removes exactly what was added, nothing else. Loading again while it's already loaded is a no-op.

#### Computed Daily Targets

This section of Settings shows your personalized nutrient targets. See [Your computed daily nutrient targets](#daily-nutrient-targets) in Part 4 for what it contains and how it's kept current.

### J. Entering custom foods and dietary supplements

Go to **Foods → Custom food profiles → Create**. See [Entering custom foods and dietary supplements](#custom-foods) in Part 4 for the fields, the supplement/tablet mechanism, and the barcode-first tip — they work identically here.

### K. A note on amino acid data

New foods are cached automatically the first time they turn up in a search, comparison, or pantry lookup — no separate import step needed. If a food is still missing amino acid data, you'll see a **Refresh** button (Food Cache) or a **Refresh from USDA** link (a meal's Protein Analysis section) to re-fetch it, and wherever data is missing you'll usually see a suggestion to search for a Foundation or SR Legacy equivalent instead. You can also enter GI or DIAAS estimates yourself via **Foods → Annotate**.

---

## Part 6 — Essential resources

---

### A. Food data — where it comes from and how it is stored [food-data]

**Two large online tables** are NuMa's primary sources of food information:

- **[USDA](#gloss-usda) FoodData Central** — the U.S. government's nutrition database, covering hundreds of thousands of whole foods, ingredients, and branded products. This is NuMa's primary source. ([FoodData Central FAQ](https://fdc.nal.usda.gov/faq/))
- **Open Food Facts** — a community-maintained database of packaged and processed food products, especially useful for branded items not found in the [USDA](#gloss-usda) table. ([Open Food Facts](https://world.openfoodfacts.org/discover))

**[USDA](#gloss-usda) API key.** NuMa accesses FoodData Central through [USDA](#gloss-usda)'s public API. Without a personal key it falls back to a shared demonstration key (DEMO_KEY) that has a tight rate limit — heavy use by any user can exhaust it and cause searches to fail temporarily. Getting your own key is free and takes about a minute:

1. Go to https://fdc.nal.usda.gov/api-key-signup and enter your name and email.
2. [USDA](#gloss-usda) emails you a key immediately.
3. Enter it in NuMa under **Settings → Advanced settings → [USDA](#gloss-usda) API key**. Type **s** at that prompt to display your current key if you need to retrieve it.

Your key is stored on your computer only. Once set, all food searches use your personal key with a much higher rate limit.

**Search result depth** (Settings → Advanced settings) — see [Search result depth](#search-ranking) in Part 4 for what this controls and why.

Every food in these online tables has a unique ID number — think of it as a product code that identifies that one food and nothing else.

**Your [Food Cache](#gloss-food-cache)** is a table stored on your own computer. When you search for a food, NuMa checks your [Food Cache](#gloss-food-cache) first and shows any matches in a fast **[Food cache](#gloss-food-cache)** table before going online. Any food you have looked up before will be there and can be selected instantly, without a network call. If the food is not yet in your cache, the program searches both online tables and shows you a combined list of matches. When you select a food from that list, NuMa saves a copy of its nutrient data in your [Food Cache](#gloss-food-cache) automatically. Over time, most of the foods you normally eat will be in your [Food Cache](#gloss-food-cache) for quick retrieval.

**Edit protection.** Any food you edit manually — through Foods → 6. [Food Cache](#gloss-food-cache) — is marked as user-modified. NuMa will never silently overwrite a user-modified food with a fresh copy from [USDA](#gloss-usda), even if you search for that food again later. Your edits, custom amino acid values, and notes are permanent unless you change or delete them yourself.

**Omega fatty acid tracking.** NuMa tracks four individual omega fatty acids — ALA (plant-based omega-3, found in flaxseed, walnuts, chia), EPA and DHA (marine omega-3, found in fish and seafood), and linoleic acid (the main omega-6, found in vegetable oils and nuts). These appear in the nutrient table whenever [USDA](#gloss-usda) data is available. Foods already in your cache that predate this feature are updated automatically the first time you access them — no action needed on your part.

Food enters your [Food Cache](#gloss-food-cache) in four ways:

1. **From [USDA](#gloss-usda)** — you search, find a match, and select it. It is instantly saved into your [Food Cache](#gloss-food-cache).
2. **From Open Food Facts[^3]** — same process; the food is saved the moment you pick it.
3. **By barcode** — at any food search prompt, type the 12-digit UPC-A or 13-digit EAN barcode printed on the product (digits only; spaces and hyphens are ignored). NuMa looks the product up on Open Food Facts by barcode, shows you the product name and brand, and asks whether to use it. This is the fastest way to add packaged foods and dietary supplements — many have an Open Food Facts entry but no [USDA](#gloss-usda) record.
4. **By hand** — you create a custom food profile yourself, entering nutrient values from a product label or research source. These entries go straight into your [Food Cache](#gloss-food-cache) without coming from any online source.

In every case, NuMa saves the food's original ID number alongside its data. That ID is the key that allows everything else in the program to refer back to a specific food unambiguously.

**[Food Annotations](#gloss-food-annotation)** are a second table on your computer. They hold extra information you choose to add about a specific food — information that does not exist in either online table:

- **Glycemic index ([GI](#gloss-gi))** — how quickly a food raises blood sugar (scale 0–100). Neither [USDA](#gloss-usda) nor Open Food Facts[^3] provides [GI](#gloss-gi) values, so if you have a figure from a research table or a product source, you can record it here.
- **[DIAAS](#gloss-diaas) estimate** — a protein quality score (scale 0–1.5). NuMa can calculate this automatically for whole foods that have complete amino acid data. For packaged foods where that data is absent, you can record a known [DIAAS](#gloss-diaas) figure here instead — see [Estimating DIAAS by hand for a packaged food](#diaas-estimate-table) for a quick-reference table by protein source.
- **A preparation note** — a short reminder such as "boiled 20 minutes" or "soaked overnight."

Each annotation is linked to one specific food in your [Food Cache](#gloss-food-cache) by that food's ID number. This means two things: you can only annotate a food that is already in your cache, and if you ever remove a food from your cache, its annotation is removed with it automatically.

**Your Recipes** are stored in their own table on your computer. Each recipe holds a list of ingredients, and each ingredient is linked to a specific entry in your [Food Cache](#gloss-food-cache) — by that food's ID. NuMa handles this link automatically: when you add an ingredient to a recipe, it searches your cache and the online tables exactly as it would for any other food search, and caches the result if it isn't stored yet.

A recipe can also include another recipe as one of its ingredients, allowing you to build complex dishes from simpler prepared components. When you log a meal, you can add a portion of a recipe — or a portion of a recipe-within-a-recipe — exactly as you would add a single food.

**[My Pantry](#gloss-my-pantry)** is a short personal list of protein sources you currently have on hand — tofu, lentils, Greek yogurt, and so on. It is a separate table used for one specific purpose: when NuMa suggests foods to fill a protein gap in your diet, it checks your pantry first and moves those foods to the top of the suggestion list. This way the program recommends things you can actually use right now, rather than foods you would need to go and buy.

**How these lists relate — and where to edit.**

Your [Food Cache](#gloss-food-cache), your Pantry, and your Custom Food Profiles (called "Drafted Food Profiles" in the program) are three different windows onto the same underlying data — not three separate stores.

Every food's nutrient data lives in exactly one place: the [Food Cache](#gloss-food-cache). The Drafted Food Profiles list is simply a filtered view of your [Food Cache](#gloss-food-cache) showing only the foods you created or edited by hand. The Pantry is a short list of names that each point back to an entry in the [Food Cache](#gloss-food-cache) (when a [USDA](#gloss-usda) link exists).

This means: if you edit a food's nutrients in the [Food Cache](#gloss-food-cache), that change is immediately reflected everywhere — in Drafted Food Profiles, in any recipe using that food, in pantry-based analyses, and in annotations. There is no syncing, no duplication, and no risk of one list getting out of step with another.

**To edit nutrient data for any food, always go to Foods → 6. [Food Cache](#gloss-food-cache).** The Pantry and Drafted Food Profiles menus remind you of this and offer a shortcut key to jump there directly. Annotations ([GI](#gloss-gi), [DIAAS](#gloss-diaas) estimates) work the same way: annotate a food once in the [Food Cache](#gloss-food-cache) and the annotation appears everywhere that food is used.

### B. Glossary [glossary]

Abbreviations and key terms used in NuMa output and this manual.

---

**AA**{: #gloss-aa}  —  Amino acid. The molecular building blocks of all proteins. See [essential amino acids](#aa).

**AI**  —  Adequate Intake. A nutrient reference value used when a full RDA cannot be established; considered sufficient for most healthy people. Used for fiber in NuMa. See [RDA](#rda).

**Antinutrient**{: #gloss-antinutrient}  —  A naturally occurring plant compound that partially blocks the absorption or use of a nutrient. Common examples: phytates (reduce mineral absorption), oxalates (reduce calcium absorption), lectins (interfere with digestion in raw legumes), bound niacin in corn. All can be reduced by appropriate preparation. See [antinutrients](#antinutrients).

**Bioavailable protein**{: #gloss-bioavailable-protein}  —  Protein the body can actually absorb and use, accounting for both digestibility and amino acid completeness. More meaningful than the raw protein figure on a nutrition label.

**CGM**{: #gloss-cgm}  —  Continuous Glucose Monitoring. A wearable device that measures blood glucose every few minutes. Discussed in [Appendix D](#appendix-d) as the most accurate way to track individual glycemic response.

**CLI**{: #gloss-cli}  —  Command-Line Interface. A text-based program operated by typing commands and reading text output. NuMa originally had a CLI alongside the web app; it was retired in August 2026 in favor of focusing entirely on the web app. Mentioned here because older Appendix A changelog entries refer to it.

**Complete protein**{: #gloss-complete-protein}  —  A protein source that supplies all nine essential amino acids at or above FAO reference levels after digestibility adjustment. See [protein completeness](#complete).

**Complement food**{: #gloss-complement-food}  —  A food added to a meal specifically to supply the amino acids that other ingredients are short in. See [complement suggestions](#comp).

**DCP**{: #gloss-dcp}  —  Digestible Complete Protein. Grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (all essential amino acids present at adequate levels). See [digestible complete protein](#dcp).

**DIAAS**{: #gloss-diaas}  —  Digestible Indispensable Amino Acid Score. A score from 0 to 1.5+ measuring how much of a food's protein the body can actually use, accounting for digestibility and amino acid completeness. 1.0 = meets the FAO reference exactly; above 1.0 = excellent; below 1.0 = one or more amino acids are limiting. See [DIAAS](#diaas).

**Digestibility coefficient**{: #gloss-digestibility-coefficient}  —  A number between 0 and 1 representing the fraction of a nutrient that reaches the bloodstream after digestion. NuMa uses true ileal digestibility values from published literature. Eggs and dairy sit near 1.0; whole legumes are typically 0.79–0.85.

**DRI**{: #gloss-dri}  —  Dietary Reference Intakes. The system of nutritional reference values published by the U.S. National Academies of Sciences[^9]; the source for RDAs, AIs, and upper intake levels used in NuMa.

**EAA**{: #gloss-eaa}  —  Essential Amino Acid. One of nine amino acids the human body cannot make and must get from food every day: Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine. See [essential amino acids](#aa).

**FAO**{: #gloss-fao}  —  Food and Agriculture Organization of the United Nations. The body that published the 2013 amino acid reference standard used for all protein quality scoring in NuMa. See [FAO reference values](#fao).

**FDC**{: #gloss-fdc}  —  FoodData Central. The USDA's online nutrition database and NuMa's primary food data source. Each food has a unique numeric FDC ID. Website: https://fdc.nal.usda.gov/

**FDC ID**{: #gloss-fdc-id}  —  The unique numeric identifier assigned to each food entry in USDA FoodData Central. You can enter an FDC ID directly at any "Search food or recipe" prompt instead of typing a name.

**Food Cache**{: #gloss-food-cache}  —  Your local database of previously retrieved foods. Searching the cache is instant (no network required); foods are added automatically when you select them from USDA or Open Food Facts[^3] results.

**Food Annotation**{: #gloss-food-annotation}  —  Extra information you attach to a cached food: glycemic index, a DIAAS estimate, or a preparation note. Stored locally; not part of any online database.

**GI**{: #gloss-gi}  —  Glycemic Index. A scale from 0 to 100 measuring how quickly a food raises blood glucose relative to pure glucose (100). See [glycemic index](#gi).

**GL**{: #gloss-gl}  —  Glycemic Load. A measure of glycemic impact that combines GI with the actual amount of carbohydrate in a serving. More useful than GI alone for real-world meal comparisons. See [glycemic load](#gl).

**GUI**{: #gloss-gui}  —  Graphical User Interface. A visual, point-and-click interface — this is what NuMa's web app provides (see Part 5, "Using the Web App").

**Ileal digestibility**{: #gloss-ileal-digestibility}  —  The fraction of an amino acid absorbed by the end of the small intestine (ileum). DIAAS uses true ileal digestibility, which is more accurate than fecal digestibility for measuring protein available to the body.

**Limiting amino acid**{: #gloss-limiting-amino-acid}  —  The essential amino acid in shortest supply relative to the FAO reference, which caps how much of a food's protein can be incorporated into tissue. The overall DIAAS score equals the ratio for the limiting amino acid. See [limiting amino acid](#gap).

**Met+Cys**{: #gloss-met-cys}  —  Methionine + Cystine. These two amino acids are scored as a combined pair in DIAAS calculations, following FAO 2013 guidelines, because the body can convert Methionine into Cystine.

**My Pantry**{: #gloss-my-pantry}  —  A personal list of protein sources you currently have on hand. NuMa checks this list first when suggesting complement foods, so suggestions reflect what you can actually use.

**NuMa**{: #gloss-numa}  —  NutriMagnus. The abbreviated name used throughout this manual.

**OFF**{: #gloss-off}  —  Open Food Facts. A community-maintained database of packaged and branded food products; NuMa's secondary data source. Website: https://world.openfoodfacts.org/

**Oxalate**{: #gloss-oxalate}  —  A naturally occurring compound (oxalic acid / oxalate ion) found in many plant foods, especially spinach, beets, nuts, and chocolate. At high dietary levels it can promote calcium-oxalate kidney stones in susceptible individuals. NuMa can optionally display oxalate content using the Harvard T.H. Chan School of Public Health reference table. Enable it under Settings → Oxalate data. See [oxalate data](#oxalate).

**Phe+Tyr**{: #gloss-phe-tyr}  —  Phenylalanine + Tyrosine. Scored as a combined pair in DIAAS calculations because the body can convert Phenylalanine into Tyrosine.

**Phytonutrients**{: #gloss-phytonutrients}  —  Plant-derived bioactive compounds tracked by NuMa where USDA data exists: beta-carotene, alpha-carotene, lycopene, lutein/zeaxanthin, choline, beta-sitosterol, and isoflavones.

**Pooled DIAAS**{: #gloss-pooled-diaas}  —  The meal-level protein quality score computed by summing digestible amino acids across all ingredients before scoring. This captures how foods complement each other in a way that single-food DIAAS cannot. See the section "How NuMa scores meal and recipe protein quality."

**RDA**{: #gloss-rda}  —  Recommended Dietary Allowance. The average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group. See [RDA](#rda).

**SPI**{: #gloss-spi}  —  Soy Protein Isolate. A concentrated plant protein (95%+ protein by weight) with high digestibility (0.95); frequently cited in complement suggestions. See [Appendix I](#comp-appendix).

**TID**{: #gloss-tid}  —  True Ileal Digestibility. NuMa's abbreviation for [ileal digestibility](#gloss-ileal-digestibility), used as a column heading in per-ingredient digestibility breakdowns.

**USDA**{: #gloss-usda}  —  United States Department of Agriculture. The U.S. government body that publishes FoodData Central, NuMa's primary food data source.

**usr**{: #gloss-usr}  —  User-drafted. Appears in ingredient ID columns to indicate a food whose nutrient profile you created or edited by hand, rather than one retrieved from USDA or Open Food Facts[^3].

### C. Internet resources

Examine.com. (n.d.). Examine—Independent analysis of nutrition and supplement research. Retrieved August 2, 2026, from https://examine.com

> Independent, citation-linked summaries of supplement and nutrient research—a good sanity check when a nutrient shows up as low or high in your analysis and you want to know what the science actually says about it. It offers nutrition data, recommendations, safety recommendations, and much, much more.

Food and Agriculture Organization of the United Nations. (2013). Dietary protein quality evaluation in human nutrition: Report of an FAO expert consultation. Retrieved August 2, 2026, from https://www.fao.org/3/i3124e/i3124e.pdf

> The original FAO report defining Digestible Indispensable Amino Acid Score (DIAAS) methodology; the primary source behind NuMa's protein-quality calculations.

Linus Pauling Institute. (n.d.). Micronutrient Information Center. Oregon State University. Retrieved August 2, 2026, from https://lpi.oregonstate.edu/mic

> Deep-dive, peer-reviewed summaries of individual vitamins, minerals, and phytonutrients—deficiency symptoms, toxicity thresholds, and disease-prevention evidence that goes well beyond what a nutrient table can show.

National Institutes of Health Office of Dietary Supplements. (n.d.). Office of Dietary Supplements—Nutrient Recommendations and Databases. Retrieved August 2, 2026, from https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

> This extraordinary resource is the fundamental data source for nutrition data used by NutriMagnus.

Open Food Facts. (n.d.). Open Food Facts—World food products database. Retrieved August 2, 2026, from https://world.openfoodfacts.org

> The crowd-sourced packaged-food database NuMa already queries for barcode lookups; browsing it directly lets you see ingredient lists, Nutri-Score, and photos that NuMa doesn't surface.

University of Sydney. (n.d.). Glycemic Index Database. Retrieved August 2, 2026, from https://glycemicindex.com

> The original research database behind glycemic index and glycemic load values; useful for looking up GI numbers for foods not yet annotated in NuMa.


## Part 7 — Troubleshooting and feedback — reporting problems and offering ideas {: #feedback}

If something seems broken or confusing, there's a good chance the answer is already below. The topics are grouped by how the problem *feels* rather than which menu it's in, since that's usually how you'll remember it later — and a few topics are listed in more than one group, since the same problem can feel different ways depending on what you were expecting. There aren't so many that you can't just skim the headings if nothing matches at first.

### A. Operating the program

#### The program crashes unexpectedly [ts-crash]

If NuMa crashes or freezes, nothing you'd already saved is lost — every action (adding a food, saving a recipe, logging a meal) is written to your data immediately, not held until some later "save" step. It's safe to just restart the program and pick up where you left off.

If a page seems frozen or won't load, try refreshing it first. If that doesn't help, the program running in the background may need restarting — close and relaunch it the way you normally start NuMa.

Either way, [let us know](#feedback) — see "How to contact help" below. This is beta software; a crash almost always means we found a real bug worth fixing, not something you did wrong.

#### You know what you want to do but can't see how to do it [ts-findit]

Click any **Learn more** link near a section heading or analysis output — see [Getting help](#help) for the full list of what each one covers.
- Either version: this manual's own search — if you're reading it in the web app, use the sidebar search box; if you're skimming the plain text version, search for a word describing what you're trying to do rather than a menu name.

If you still can't find it, [tell us what you were trying to do](#feedback) in plain language, not what menu item you were looking for. That phrasing is exactly what we need to know whether the feature exists, is named confusingly, or genuinely isn't built yet.

### B. I don't understand...

#### A recipe's "Complete" checkbox doesn't match its protein-completeness score [ts-complete-confusion]

A recipe's **Complete** checkbox and its amino-acid completeness score are two unrelated ideas that happen to share the word "complete." **Complete** (the checkbox, see the [Recipes list](#recipes) column guide) is a personal flag you toggle yourself — "I'm done editing this recipe" — it has nothing to do with protein quality. Whether a food or recipe's amino acid profile is **complete** (clears every essential amino acid floor) is a separate calculation shown in its DCP and DIAAS analysis. A recipe can be marked Complete and still have an incomplete amino acid profile, or the reverse.

#### I set a recipe's servings to 0 and now everything looks different [ts-servings-zero]

Setting a recipe's **Servings** field to 0 is a deliberate mode switch, not an error: it tells NuMa you want to analyze the recipe by total weight or volume instead of by serving count — useful for something you haven't decided how to portion yet (a big batch of granola, say). Every "per serving" figure becomes "per 100 g" or "per 100 ml" instead, and DCP shows as **NC** (not computed) since there's no serving size to divide by. Set Servings back to any number greater than 0 to return to normal per-serving analysis.

*See also:* [DCP is capped or jumped in a way that doesn't add up](#ts-dcp-cap), [A food or recipe shows an "insufficient amino acid data" warning](#ts-missing-aa), [Oxalate or glycemic index data isn't showing](#ts-oxalate-gi).

### C. I'm confused — something unexpected happened

#### USDA searches got slow, or started failing [ts-usda-slow]

Without a personal [USDA API key](#food-data), NuMa shares a demonstration key (`DEMO_KEY`) with every other NuMa user, and its rate limit is tight enough that heavy use by anyone can exhaust it, causing searches to fail temporarily for everyone. A free personal key removes this ceiling and takes about a minute to get — see [Food data — where it comes from and how it is stored](#food-data) for the sign-up steps and where to enter it (Settings, either version).

#### A deleted recipe shows up as "(deleted)" somewhere [ts-deleted-recipe]

This is expected, not a bug: deleting a recipe that's used as an ingredient in another recipe doesn't remove that ingredient line — it stays in place, flagged "recipe (deleted)" wherever it appears (ingredient lists, meal history, Food Use in Meals). If you later create a new recipe with a similar or identical name, NuMa offers to relink the old references to it automatically. See [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) for the full behavior and how to browse every currently-broken reference.

*See also:* [I searched for a food I know exists and got nothing](#ts-search-empty), [The food I wanted wasn't at the top of the search results](#ts-search-order), [A meal's DCP isn't showing](#ts-meal-dcp), [A past day's numbers changed after I updated my profile](#ts-day-profile).

### D. I expected to see something, and it's not there

#### A food or recipe shows an "insufficient amino acid data" warning [ts-missing-aa]

Some foods — especially branded or prepared products — simply don't have amino acid data published anywhere NuMa can look it up automatically. This isn't a bug; it's a genuine data gap. Two ways to close it: search for a USDA Foundation or SR Legacy equivalent (plain/raw foods are far more likely to have full amino acid data than branded ones), or fetch the missing values yourself via Claude AI — see [Missing amino acid profiles](#missing-aa) and [Food Cache](#food-cache-web).

*See also:* [No brand or equivalent of a food has amino acid data anywhere in USDA](#ts-no-aa-anywhere), for the harder case where neither fix above applies.

#### No brand or equivalent of a food has amino acid data anywhere in USDA [ts-no-aa-anywhere]

This is a step beyond [an "insufficient amino acid data" warning](#ts-missing-aa): you've checked, and no brand, no store variant, and no generic USDA entry for this food carries amino acid data — the whole category is a gap, not just the specific product. "Search for a Foundation/SR Legacy equivalent" doesn't help here because there's no equivalent food with the data you need.

The fix is to stop looking for an equivalent *food* and look instead for an equivalent *ingredient* — something with measured amino acid data whose composition dominates the protein in the food you're trying to estimate. Flour-based baked goods, for instance, get essentially all their protein from the flour; a legume-based product gets essentially all of its protein from that legume. [Estimating amino acids by copying from another food](#drafted-foods) is the tool that turns an ingredient like this into an estimate for your actual food — it scales the ingredient's amino acid values to match your food's own measured protein content automatically, rather than you doing that arithmetic by hand.

If more than one ingredient contributes meaningfully to the protein (a flour blend, for example), blend their profiles first, by mass fraction, before treating the result as a single stand-in. The copy-from-another-food picker copies from one source food at a time, so build the blend as its own drafted food first — call it a **proxy food**: a temporary, scratch entry that exists only to hold the numbers you'll scale from, not something you'd search for or log a meal against. (If only one ingredient dominates, it's still worth entering as its own proxy food rather than typing numbers straight into the real food — see why below.)

Once you have a proxy food — blended or not — holding the numbers you need, there are two different ways to turn it into a usable estimate for your actual food. Pick whichever fits how you'll use that food going forward:

**Option 1 — create a new, clearly-labeled draft (the general-purpose default).** Foods → Custom Food Profiles → **Copy a cached food as a draft**, pick the real food you're missing AA data for (it copies that food's full nutrient snapshot — protein included — into a brand-new, independent entry), rename the copy something unambiguous like "Graham Cracker, generic (estimated AA)," then run the AA-copying picker on *that* draft, scaling from your proxy food. Because the original cached food is never touched, USDA can still refresh its full nutrient profile and portions automatically if that entry ever changes. The tradeoff: this new draft doesn't retroactively reach meals or recipes that already reference the *original* food — those keep pointing at the un-estimated entry until you go swap the reference over by hand.

**Option 2 — edit the original food's AA fields directly (a deliberate exception).** If you know you'll always be logging this exact product, editing its AA data in place is often more practical: every past and future meal or recipe that already references it picks up the estimate immediately, with nothing to swap. The cost is real, though — editing *any* of a food's data marks the entire record user-modified, not just the amino acid fields, so NuMa will never again silently refresh its full nutrient profile, portions, or anything else on it from USDA; you're taking permanent manual ownership of that specific record. That's an easy trade when the food is unlikely to gain real measured data any other way — a specific branded product like Nabisco Honey Maid Grahams already has its macronutrients measured and isn't about to grow USDA amino acid data on its own, so there's little future refresh being given up.

**Worked example: graham crackers, no AA data on any brand, made from a 2:1 white-to-whole-wheat flour blend. Nabisco Honey Maid Grahams specifically are already logged in past meals.**

Steps 1–3 build the proxy food and are the same regardless of which option you pick. Steps 4 onward differ — jump to whichever option fits your situation.

Step 1 — pull measured amino acid data for both flours (USDA Foundation/SR Legacy entries):

    Amino acid       White flour, per 100g    Whole wheat flour, per 100g
                      (protein 10.3 g)         (protein 13.21 g)
    Histidine         230 mg                    357 mg
    Isoleucine        357 mg                    443 mg
    Leucine           710 mg                    898 mg
    Lysine            228 mg                    359 mg
    Methionine        183 mg                    228 mg
    Phenylalanine     520 mg                    682 mg
    Threonine         281 mg                    367 mg
    Tryptophan        127 mg                    174 mg
    Valine            415 mg                    564 mg

Step 2 — blend (average) the two flours 2:1 by mass (2 parts white, 1 part whole wheat) to get the amino acid pattern of the flour actually used, per 100g of blend:

    Amino acid       Blend, per 100g flour mix (protein 11.27 g)
    Histidine         272 mg
    Isoleucine        386 mg
    Leucine           773 mg
    Lysine            272 mg
    Methionine        198 mg
    Phenylalanine     574 mg
    Threonine         310 mg
    Tryptophan        143 mg
    Valine            465 mg

Step 3 — enter this blend as its own proxy food (Foods → Drafted Food Profiles → Create; web: Custom Food Profiles), named something like "Wheat flour blend, 2:1 white:whole wheat (proxy)," with the protein and amino acid values from Step 2 typed in directly.

**Continuing with option 1 (new labeled draft).** Use this branch if you haven't already logged the Nabisco Honey Maid Grahams entry anywhere, or you'd simply rather leave it untouched:

Step 4 — Foods → Custom Food Profiles → **Copy a cached food as a draft**, and pick the Nabisco Honey Maid Grahams entry. This copies its full nutrient snapshot — including its measured protein content, 6.8 g/100g — into a brand-new, independent entry. The original cached food is untouched.

Step 5 — rename the new draft something unambiguous, like "Graham Cracker, generic (estimated AA)."

Step 6 — on that new draft, use the "estimate amino acids from another food" picker and choose the proxy food from Step 3 as the source. NuMa scales the proxy's amino acid values to match the draft's own protein content automatically — factor 6.8 ÷ 11.27 ≈ 0.60 — giving:

    Amino acid       Estimated, graham crackers, per 100g (protein 6.8 g)
    Histidine         164 mg
    Isoleucine        233 mg
    Leucine           466 mg
    Lysine            164 mg
    Methionine        119 mg
    Phenylalanine     346 mg
    Threonine         187 mg
    Tryptophan        86 mg
    Valine            280 mg

Step 7 — document the derivation in the draft's Note field (the picker suggests one automatically). From now on, use this draft — not the original Nabisco entry — when logging graham crackers in meals or recipes.

**Continuing with option 2 (edit the original in place) — Nabisco Honey Maid Grahams is already logged in past meals, so this is the better fit here:**

Step 4 — on the real Nabisco Honey Maid Grahams cached entry, use the "estimate amino acids from another food" picker and choose the proxy food from Step 3 as the source. The Grahams have their own measured protein content (6.8 g/100g) even though they lack amino acid data, so NuMa scales the proxy's amino acid values to match it automatically — factor 6.8 ÷ 11.27 ≈ 0.60 — giving the same result table as above.

Step 5 — document the derivation in the food's Note field (the picker suggests one automatically). Every meal and recipe already referencing this entry — past and future — picks up the estimate immediately; there's nothing else to update.

**Either way:** these amino acid figures are an approximation, not a certified lab value — they assume the crackers' protein comes entirely from the flour blend (true enough for a plain graham cracker; less true for a chocolate-coated one, where dairy protein in the coating would shift the pattern).

Once you've applied the estimate to every food that needed it, the proxy food from Step 3 has done its job — it exists only to hold numbers for the picker to scale from, not to be searched for or logged against. Delete it to keep it out of future search results, unless you expect to reuse it again soon (for another graham-cracker product, say) — in which case there's no harm leaving it in place until you're done with it.

#### I searched for a food I know exists and got nothing [ts-search-empty]

Try different search terms. "beans cooked" and "beans canned" may seem to be the same thing but they are not. The latter is a subgroup of the former. Playing with search terms can yield seriously variable results.

Check your **Dietary Preference** setting (Settings). If it's set to "Plant-based only" or "Vegetarian," foods outside that category are filtered out of *every* search, comparison, and lookup in NuMa — not just from complement suggestions — so a food you know is in USDA's database can still return zero results. Temporarily switch to "All animal foods," search, then switch back.

#### The food I wanted wasn't at the top of the search results [ts-search-order]

This is usually not a bug — it's the order you typed your search words in. NuMa ranks results first by how many of your search words a name contains, but when there's a tie, it treats the *order* you typed your words in as a signal of priority: matching your earlier words outranks matching your later ones. So searching `milk dry instant` will favor a "milk dry ..." match over a "milk instant ..." match whenever only one of those two words is present in a given result, simply because "dry" was typed before "instant."

If that's not the priority you meant, reorder your search words so the one you care most about comes first — put the word that most distinguishes what you want right after the main food name. See [Ordering food search results](#search-ranking) in Part 4 for the full explanation of how results are ranked.

#### A meal's DCP isn't showing [ts-meal-dcp]

DCP now computes and saves automatically every time you add, edit, or remove an item — there's no "mark complete" step required for it to appear, and an in-progress meal already contributes to that day's total. (Marking a meal **Complete** still matters for a different reason: a day containing an unmarked meal is flagged "provisional" in Daily Summary, since its total could still change.)

If DCP is still showing as missing, the real cause is the same as [an "insufficient amino acid data" warning](#ts-missing-aa): none of the meal's food items — and for recipe items, the recipe itself — have amino acid data available yet. Add AA data to at least one ingredient (or analyze the recipe), and DCP fills in immediately without needing to reopen or reanalyze the meal.

#### Oxalate or glycemic index data isn't showing for a food [ts-oxalate-gi]

Both are opt-in and off by default — this is a configuration gap, not a bug. [Oxalate data](#oxalate) needs its Settings toggle switched on (one account-wide switch, either version). [Glycemic index](#gi) needs either the built-in reference-table seed or your own annotation on that specific food; NuMa will offer to prompt you for it the first time you add a new food to your Pantry or a meal.

*See also:* [A recipe's "Complete" checkbox doesn't match its protein-completeness score](#ts-complete-confusion).

### E. The numbers don't make sense

#### DCP is capped, or jumped in a way that doesn't add up [ts-dcp-cap]

This is the single most common "the math looks wrong" report, and it's almost always correct behavior: DIAAS itself is not capped (a high-quality food can score above 1.0), but Digestible Complete Protein (DCP) can never exceed the protein you actually absorbed, so NuMa caps it there when the two disagree. A capped DCP is genuinely good news — it means your limiting amino acid is in strong enough supply that none of your absorbed protein is going to waste. See [Why DCP Is Sometimes Capped Below the DIAAS Projection](#dcp-cap) for the full explanation with a worked example.

#### A past day's numbers changed after I updated my profile [ts-day-profile]

This shouldn't happen, and if it does, it's worth [reporting](#feedback) — but first check whether it's actually the documented, intentional behavior: each logged day stays pinned to whichever profile was active *when you logged it*, not whatever profile is active today, specifically so that switching profiles (illness, travel, a deliberate weight change) doesn't silently rescore your history. If the automatic pin doesn't match reality — illness or travel rarely starts exactly at midnight — you can manually reassign which profile a specific day is compared against. See [Per-day profile tracking](#day-profile) for how.

*See also:* [A deleted recipe shows up as "(deleted)" somewhere](#ts-deleted-recipe).

### F. A food's portion or serving-size data looks wrong

This is a different kind of problem than the others on this page: it isn't NuMa misbehaving, it's a gap or error in the underlying USDA data NuMa displays. USDA publishes nutrient values reliably, but the *portion* records attached to a food — "1 large," "1 cup, sliced," and so on — are contributed unevenly and sometimes inaccurately. NuMa shows you exactly what USDA supplies; when that's missing or wrong, the fix is to teach NuMa the correct value yourself, once, and it's remembered for every future use of that food.

#### A food has no "per piece" or "per egg" portion — only grams [ts-no-piece-portion]

Some foods that obviously come in natural units — a whole egg, a piece of fruit, a slice of bread — still have no USDA-supplied portion for that unit, only the generic per-100-g figures. This happens because USDA's portion records are contributed per food entry, not derived automatically from the food's description, so some entries simply never got one. It's not something NuMa can infer on its own — "1 egg" isn't a fixed weight (USDA's own size grades range from about 38 g for "Small" to 63 g for "Jumbo").

Two fixes: weigh the item once on a kitchen scale and enter that weight directly (`56g`, for instance), or teach NuMa the unit permanently via the food's [Food Cache](#food-cache-web) entry, **Portions** action. Either way, every later analysis, recipe, and meal entry for that food can then use the unit directly (`1 egg`, `2 slices`) instead of a gram weight.

#### A food has a weight portion but no cup/tablespoon equivalent [ts-no-volume-portion]

NuMa converts a volume measure (cup, tablespoon, teaspoon) to grams using a *density* estimate for that food — mass per milliliter. USDA doesn't publish density directly; NuMa derives it only where a matching weight-and-volume portion pair exists in the food's own USDA record, plus a small built-in table for common dried herbs and spices (see [Portion Input Formats](#portion-formats)). Outside those cases, entering a volume measure will prompt you to weigh the amount and enter the grams yourself — this is expected, not a bug, since guessing a density would silently produce wrong nutrient totals.

If you'll be entering this food by volume repeatedly, teach NuMa the conversion once: weigh a level cup (or tablespoon) of it, then use the same Portions editor as above — the [Food Cache](#food-cache-web) entry's **Portions** action. From then on, cup and tablespoon amounts for that food convert automatically.

#### A food's portion or volume conversion looks flatly wrong [ts-bad-portion-data]

Occasionally a USDA record's portion weight is simply implausible for what it describes — a "1 large" egg listed at a weight that doesn't match a scale, or a "1 cup" measure clearly sized for a different preparation than the one you have. This is a data-entry error on USDA's side, inherited as-is; NuMa doesn't second-guess or adjust USDA's published portion weights, since there'd be no reliable way to tell a genuine correction from a wrong override.

If a portion weight doesn't match what you measure: weigh your actual amount and enter the gram figure directly for that one use, and — if you'll use this food again — replace the bad portion with a corrected one via the same Portions editor (the [Food Cache](#food-cache-web) entry's **Portions** action). Custom portions you add there are yours — they aren't overwritten by a later **Refresh** of the food's nutrient data. If you're confident the USDA source itself is wrong (not just unusual), [let us know](#feedback) — it's worth tracking so other users hit it less often, even though NuMa can't correct USDA's database directly.

*See also:* [Enter food portions as weights, not volume measures, whenever possible](#portion-formats).

### G. Getting more help

This is extremely easy, and we want you to do it. When you're having a problem the cause is NOT necessarily you! Regardless of the nature of your problem, contacting us gives us essential information needed to make things better for you and also for every other user. We very much want to hear from you if you have a problem.

1. Text Tom at 435-272-3332. Plainly state that you are having a problem with the program. A brief statement of the problem is all I need. With your phone number I can call you back and get complete details of what I need to know to resolve your problem. I will generally call you back immediately. If you prefer a different time, let me know.

2. For non-urgent problems - which generally are improvements you'd like to see - you can also email me. Provide screenshots, if you think that would help. ALWAYS TEXT ME IF YOU SEND AN EMAIL, as I do not check my email daily, and yours easily can get lost in the 100s I get every day.

---

## Part 8 — Possible Additional Features

Ideas below are listed in their current likely probability of being implemented.

---

### Suggested optimum nutrition profiles

For various major age groups, we can offer research supported optimums for critical nutrients. The user can choose to adopt them or use the as the basis for setting their own optimums, or ignore then altogether.

### Research-supported maximum nutrient level suggestions

For a limited number of nutrients, maximum levels of consumption have been established, the exceeding of which puts the individuals at risk in various wasy. We can identify these nutrients, levels, and risks, with full sourcing to back up claims made.

### Source citations for major assertions in the manual

This is basic. Claims must be backed up, and source citations are how it's done. Numa is designed around nutrition research findings. To move quickly, these findings have not been referenced in the manual. They will be as soon as possible, which is to say as soon as the program is reliably working for a number of serious users.

### D. Plots of individual nutrients consumed daily in relation to RDAs, user-established optimums, and maximum levels.

This is easily achieved once we have dealt with the fundamental data problem better - getting optimums and maximums specified for a user. 

### E. Development of glycemic data lookup tables

Such data is of interest to anyone wanting to better manage their blood sugar levels, including folks with any degree of metabolic syndrome, pre-diabetes, or outright diabetes. At present, no active use of such data exists in the program, but provision of such use is in place.

### F. What else? Well, know this...

#### Your ideas shape what gets built next {: #feature-ideas}

NuMa is an evolving tool, still actively being built out. This part exists to invite you into that process: if there's something NuMa doesn't do yet that would make it more useful to you, we want to hear about it.

No idea is too small, too ambitious, or too specific to your own situation. A feature that seems minor to you may turn out to matter to a lot of other users too — and one that seems highly personal often points to a real gap in the program. Several of NuMa's existing features started out as exactly this: one user's request.

#### How to contribute an idea

Use the same channel as [reporting a problem](#feedback):

1. **Text Tom at 435-272-3332** with a brief description of what you'd like NuMa to do, and why it would help you. He will generally call you back to get the full picture.
2. **Or email**, especially for a longer or more detailed idea — a screenshot or example is welcome if it helps explain what you have in mind. If you email, also send a text, since email isn't checked daily and a good idea shouldn't get lost in it.

There's no such thing as a request that's not worth mentioning. If you're not sure whether NuMa can already do what you want, ask anyway — the answer might be a feature you hadn't found yet, or it might be a real gap worth filling.


## Part 9 — Appendices

---

### A. Recent program updates log

[//]: # "Aside from being an update log for the user to ac cess, this section is also used by create_release.py at git push time to produce a release note. It only looks for today's date heading (#### Month Day). Once a release is cut, the matched text is copied into the GitHub release body permanently — nothing re-reads the manual afterward. So date whose release has already happened is safe to prune anytime; it can't retroactively change a past release's notes."
[//]: # "If there is no entry for the date of the push to main, create_release.py falls back to the generic "Automated build from main." message instead of real notes."

#### August 6

**FIX: THE "ESTIMATE AMINO ACIDS FROM ANOTHER FOOD" TOOL IS NOW EASY TO FIND**

When a food's detail page shows "No amino acid data for this food," it now also offers a link to estimate that food's amino acid profile from a similar food that already has one — previously this tool was reachable only from Custom Profiles, so it was effectively invisible for any food you hadn't already turned into a custom draft.

```
web/templates/food_detail.html
Added a link to /food/custom-profiles/{fdc_id}/edit next to the existing
Foundation Foods suggestion, in both places the "no AA data" banner
appears. No backend change was needed — the edit and copy-aa routes
(web/backend.py) were never actually gated on food.user_drafted; only
the "Edit nutrients" button's template condition was.
```

**NEW: PRINTABLE RECIPE, MEAL, AND DAILY SUMMARY ANALYSES, WITH A CHOICE OF WHAT TO INCLUDE**

Recipes, meals, and the full-day summary can now be printed / saved as PDF the same way food pages can — with checkboxes for exactly which sections to include. Recipes add Ingredients and Procedure to the checklist; meals add the food/recipe list; the day view adds a per-meal breakdown. Anti-nutrients isn't offered on the day view since that rollup isn't computed at that level.

```
web/backend.py, web/templates/print.html, numa_app/services/print_sections.py
Extends the food-print machinery from earlier today. _recipe_detail_context(),
_meal_print_context(), and _meal_day_context() factor out (or duplicate,
for meal, to avoid touching the larger meal_view route) each page's existing
data computation for reuse by new GET /recipe/{id}/print, /meal/{id}/print,
and /meal/{id}/day/print routes. print.html gained render blocks for the
diaas/protein_adequacy shape recipe/meal/day use (distinct from food's
protein/DIAAS shape), the oxalate_agg/ingredient_antinutrients aggregate
anti-nutrient shape, glycemic load, and the ingredients/procedure/items/
meals_list page-specific sections. The old dedicated recipe_print.html
(ingredients + procedure only, no nutrient data) is retired in favor of
this shared template. Section selection is remembered separately per page
type (food/recipe/meal/day) in prefs.json.
```

**NEW: PRINTABLE FOOD NUTRITIONAL ANALYSIS, WITH A CHOICE OF WHAT TO INCLUDE**

A food's detail page now has a "Print / Save as PDF" link. The print view lets you check off exactly which parts you want — nutrient table, protein summary, protein quality (AA/DIAAS), anti-nutrients, complement suggestions — so you only print what's useful, not the whole page. Your choice is remembered next time you print a food.

```
web/backend.py, web/templates/print.html, web/templates/food_detail.html,
numa_app/services/print_sections.py
New GET /food/{fdc_id}/print route, reusing the same data-computation the
food detail page already does (factored out into _food_detail_context()).
Section availability is computed per request (e.g. a food with no oxalate
data won't offer the anti-nutrients checkbox). Selection is carried via
query params and persisted per page-type in prefs.json under
"print_sections", the same file used for Meals list column choices. This
is a first instance of a page type, later extended to recipe/meal/day
printouts the same day (see entry above); nutrient_plot_print.html (chart
print) is unchanged.
```

**FIX: FOOD NAMES ON THE PANTRY PAGE ARE NOW CLICKABLE**

Food names in My Pantry now link to the food's detail page, matching how the Food Cache list already worked.

```
web/templates/pantry.html
Wrapped item.food_name in an <a href="/food/{fdc_id}"> link when item.fdc_id
is set, mirroring the pattern already used in food_cache.html.
```

#### August 5

**MANUAL: RECENT PROGRAM UPDATES LOG MOVED TO APPENDIX A, EVERY APPENDIX RELETTERED**

This changelog is now Appendix A (first) instead of Appendix K (last) — quicker to find. Every other appendix shifted down one letter to make room.

```
user-manual.md, scripts/create_release.py, README-numa-documentation.md
Moved Appendix K (this changelog) to Appendix A since it's checked far more often
than the others. Old A→B, B→C, ... J→K; Appendix L (footnotes) unchanged, already
last. Updated every "Appendix X" cross-reference and lettered anchor (#appendix-a
etc.) throughout the manual and README, and the hardcoded heading string in
scripts/create_release.py that pulls today's release notes. Entries inside this
changelog that mention "Appendix K" by name (e.g. the Aug 4 CLI-removal entry
below) were left as-is — historical record of what was true when written.
```

**MANUAL: EVERY CHANGELOG ENTRY FROM JULY 31 ON IS NOW A TERSE SUMMARY, WITH TECHNICAL DETAIL TUCKED IN A CODE BLOCK BELOW IT**

From July 31 onward, each entry here is now a bold title, a short plain-language line or two about what you can now do, and (if useful) full technical detail tucked into a block underneath, out of the way for anyone skimming.

```
user-manual.md
Reformatted all 24 entries from Aug 5 back through Jul 31 (Jul 30 and
earlier left in the old single-line format, per instruction — only the
recent entries are read often enough to be worth the rewrite). Summaries
now lead with the user-facing capability/result rather than the bug or
prior state that motivated the change, per explicit direction: what you
can now do matters more than what was wrong before.
```

#### August 4

**NEW: SAMPLE DATA — ONE-CLICK EXAMPLE FOODS, PANTRY, AND RECIPES FOR A FRESH INSTALL**

A brand-new install can now load one-click sample data — foods, a pantry, and two recipes — so you can see NuMa's protein-complementarity feature working right away instead of building everything up by hand. Find it at Settings → 9. Sample Data; "Clear sample data" removes exactly what was added and nothing else. [learn more...](#demo-data)

```
Settings → 9. Sample Data
Adds 9 real USDA foods (full amino-acid panels, not placeholders), 6 of them to
the pantry, and two recipes — "Black Beans & Rice" and "Lentils & Oats Bowl" —
chosen and gram-verified against NuMa's own DIAAS math to show a real
complementarity improvement (0.617/0.899 → 0.948 combined for beans-and-rice;
0.780/0.828 → 0.992 for lentils-and-oats). Never touches anything already in
your cache/pantry/recipes; added items are tracked separately so clearing
removes only those, and loading twice is a no-op.
```

**RELEASE PIPELINE NOW PACKAGES THE WEB APP INSTEAD OF THE REMOVED CLI, AND RUNS TESTS FIRST**

Releases are now built straight from the web app, not the retired CLI, and only ship after the full test suite passes — so a broken build can no longer become a public release.

```
nutrimagnus.spec, Makefile, scripts/create_release.py, .forgejo/workflows/release.yml
The Linux build was still packaging the CLI binary from the deleted numa.py,
failing every push to main. Repointed PyInstaller at web/launcher.py, bundling
web/templates, web/static, the manual source/output, and oxalate.db. Fixed a
latent bug: the release-notes generator was matching the wrong Appendix K
heading text and silently falling back to a generic message on every past
release. Windows packaging still targets the old CLI entry point — a known,
separately-tracked gap.
```

**REMOVED THE INTERACTIVE TERMINAL CLI**

The old terminal-based interface is gone. NuMa is web-only now — nothing changes for you if you were already using the web app.

```
numa.py, numa_app/ui, numa_app/workflows, numa_app/state.py, numa_app/config,
manual.py, and CLI-only services (annotations.py, oxalate_link.py, reports.py)
Owner never used the CLI and expected no other users to either. Shared
utilities (classify_food_id, rebuild_manual_if_stale) relocated out of the
CLI-only ui/ package into services/. ~144 CLI-only tests removed along with
the NumaTestRunner harness; deleted tests-prev/ (stale untracked duplicate).
requirements.txt now lists the actual web dependencies. Test count: 606 → 462.
```

**MANUAL, CLAUDE.md, AND README FULLY SWEPT FOR CLI-ERA CONTENT AFTER THE CLI REMOVAL**

The manual, README, and project instructions were combed through and rewritten to describe the web app only — no more leftover CLI-era instructions to trip you up.

```
Manual, CLAUDE.md, README-numa-documentation.md
Deleted the manual's ~1040-line "Using the Command Line" Part wholesale,
renumbered following Parts down by one; rescued two pieces of real content
that applied to the web app too (Dietary Preferences → Part 4.B; web-keyboard-
shortcuts detail → Part 5). Collapsed ~80 scattered CLI/web comparison asides
to the web half. Fixed a broken #outputSamples link and retargeted every
#fetch link at #food-cache-web. Removed CLAUDE.md's CLI-only sections
(Navigation Contract, ? Help System, Theme/Styling, Circular Import Pattern).
README's Architecture section (~250 lines on deleted CLI files) replaced with
an accurate module-split summary. Historical sections (this changelog,
README's "Bugs found..."/"Implementation Phases") deliberately left
describing CLI-era mechanics as history.
```

**MANUAL: SECOND PART 4 SWEEP, COVERING EVERYTHING SHIPPED SINCE THE AUG 2 SWEEP**

The manual's shared-operations section (Part 4) got a follow-up pass, closing a few explanation gaps left by features shipped in the last couple of days.

```
Manual
Follow-up to the Aug 2 sweep, covering Aug 3–4, establishing this as a
recurring weekly (Saturday) check. Fixed: (1) the web-only "Source" filter
dropdown had no canonical explanation — added to Food Search Results in
Part 3, linked from all four usage sites; (2) the Meal add-food page's
pointer to that section was stale; (3) the Aug 3 search-tiebreak fix was
only in this changelog, not the manual body — added to Ordering food search
results in Part 4; (4) the CLI's Pantry-menu command table in Part 6 had
drifted out of sync with Part 3's fuller one — replaced with a pointer to
the single authoritative list.
```

**MANUAL: THE NEW IGNORE/RECALCULATE COMPLEMENT FEATURE IS NOW DOCUMENTED ONCE, IN PART 4, INSTEAD OF PER-PAGE**

The "ignore a complement suggestion" feature (see below) is now explained in one place in the manual instead of being repeated three times.

```
Manual (Part 3.B, Part 4, Part 5)
The ignore/recalculate mechanic applies identically on three web pages (Food
detail, Meal, Recipe); consolidated into one new Part 4 entry, "Ignoring a
complement suggestion," cross-linked from the Protein Complement Suggestions
concept section and each page's feature list — same pattern already used for
search ranking and recipe DCP cascading.
```

**NEW: PROTEIN COMPLEMENT SUGGESTIONS CAN BE IGNORED, RESTORED, AND RECALCULATED**

Every suggested complement food on a Food detail, Meal, or Recipe page now has an "Ignore this suggestion" checkbox — check one or more, click "Recalculate complements," and the suggestions rebuild around what's left. Useful when a suggestion isn't actually available or appealing. A "Clear all" link restores everything; the ignored list resets on a plain page reload.

```
Food detail, Meal, Recipe (web)
Checking a box and clicking "Recalculate complements" reloads the page with
those foods excluded from every tier — pantry, general, two-food
combinations, DIAAS boosters, two-step combos. Ignoring more foods later in
the same session adds to the list rather than replacing it. A collapsible
"Ignoring N suggestions — manage" panel lists every currently-ignored food
alphabetically with its own "Remove ignore" checkbox. Nothing is persisted.
```

**NEW: FOOD SEARCH CAN NOW BE FILTERED TO A SINGLE DATA SOURCE**

Every food-search box in the app now has a "Source" dropdown — All sources, Pantry, Food Cache, Recipes, USDA, or Open Food Facts — so you can narrow a crowded results list to just what's in your own pantry, say. The choice is sticky across every search box, same as "Sort by."

```
Foods → Search / Analyze a Food Portion / Convert / Compare; My Pantry;
Meals & Log: Add Food or Recipe; Recipes → Edit (add ingredient) (web)
Options labeled with the source abbreviation plus full name (e.g. "USDA —
USDA FoodData Central"). Built to help track down a suspected remaining
search-ranking oddity by isolating results to one source at a time.
```

**NEW MANUAL SECTION: WHAT TO DO WHEN NO BRAND OR EQUIVALENT OF A FOOD HAS AMINO ACID DATA ANYWHERE IN USDA**

New troubleshooting guidance for when no version of a food anywhere in USDA has ever had its amino acids measured: build a "proxy food" from an ingredient that supplies essentially all the target food's protein, then either save it as a labeled draft or edit the original food's AA fields directly. Includes a full worked example. [learn more...](#ts-no-aa-anywhere)

```
Manual — Part 8 troubleshooting entry
Two ways to apply a proxy: copy the real food as a new labeled draft
(general-purpose default — leaves the original refreshable from USDA,
doesn't retroactively reach meals/recipes already logged) or edit the
original food's AA fields directly (for a specific product you'll always
log — reaches existing logs immediately, freezes that record against future
USDA refreshes). Worked example: graham crackers, no AA data on any brand,
estimated from a 2:1 white:whole-wheat flour blend, applied in-place since
the branded product was already logged.
```

**NEW: EDIT A PANTRY FOOD'S DATA DIRECTLY FROM THE PANTRY LIST**

Each pantry row now has a direct "Edit" shortcut into that food's Food Cache edit screen — no more leaving My Pantry, opening the Food Cache, and finding the food again by name. Not available for name-only pantry entries until you link a food first.

```
My Pantry (CLI + web)
CLI's new e<row> command (e.g. e3), or an Edit button on each web row,
rather than a second separate edit implementation. Deleting a food from
Pantry or the Food Cache was already possible in both interfaces and is
unchanged.
```

#### August 3

**MEALS & LOG: ADD FOOD OR RECIPE SEARCH CAN NOW CONFIRM "~✓" FOODS' AMINO ACID DATA TOO**

In Meals & Log's add-food search, you can now tick one or more "~✓" (likely, unconfirmed) foods and click "Fetch full details for selected" to resolve the guess into a real ✓ or ✗ before adding it to the meal.

```
Meals & Log: Add Food or Recipe (web)
Same gap as the Recipes → Edit fix below, same fix.
```

**RECIPES: ADD-INGREDIENT SEARCH CAN NOW CONFIRM "~✓" FOODS' AMINO ACID DATA, AND A STRAY CONFUSING NOTE IS GONE**

The Recipes → Edit ingredient search now also lets you tick "~✓" foods and confirm their amino-acid data before adding — every other search list in the app already had this. Also removed a stray, confusing instruction that appeared above every ingredient search regardless of context.

```
Recipes → Edit (web)
"Fetch full details for selected" resolves a "~✓" (likely, unconfirmed)
badge into a real ✓ or ✗. Removed leftover sentence ("Add a replacement
below, then remove the original ingredient above.") that described a
workflow this search box was never actually limited to.
```

**FIX: TERSE BRANDED PRODUCT NAMES WERE BURYING THE FOUNDATION/SR LEGACY FOOD THAT ACTUALLY HAS AMINO ACID DATA**

Food search now favors the USDA reference foods that actually have amino-acid data over near-duplicate branded listings with terser names, when many results tie on word match.

```
Foods → Search (CLI + web)
The final tiebreaker — shorter name wins — favored terse branded duplicates
over the longer, more descriptive Foundation/SR Legacy foods, even though
those are the ones with real AA data. Ties now break by USDA data quality
first (Foundation/SR Legacy, then Survey/Experimental, then Branded/Open
Food Facts) before name length. Repro: "milk nonfat dry instant" buried both
matching SR Legacy foods behind 13 branded duplicates.
```

#### August 2

**FIX: LOCAL AND EXTERNAL SEARCH RESULTS NOW GET RE-RANKED TOGETHER, NOT JUST STACKED**

Search results from your own pantry/cache/recipes and from USDA/Open Food Facts are now sorted together as one list, so a weak local match can no longer sit above a much better external match just because it loaded first.

```
Foods → Search / Analyze a Food Portion; Meals & Log: Add Food or Recipe (web)
These pages render local results instantly then fetch external results in
the background; external results were only ever appended below, never
re-sorted with the local set. The background fetch now returns the complete
merged, re-sorted list and the page replaces the table instead of appending.
Repro: "peanut butter old" with "Best match to name" put a barely-matching
pantry oatmeal ahead of the actual peanut butter result.
```

**MANUAL: VERIFIED EVERY PART 4 TOPIC IS CROSS-LINKED FROM BOTH PART 5 AND PART 6, AND FIXED A REMAINING GLYCEMIC LOAD GAP**

A documentation-only pass confirming every shared-operations topic is reachable from both the web app and command-line sections, plus a genuine fix: Glycemic Load's "needs GI data on every item" rule now has the incoming links it was missing.

```
Manual
Audited every anchor from the Part 4 consolidation to confirm both Part 5
and Part 6 link to it somewhere natural. Found one real gap: Glycemic
Load's rule was mentioned by name four times with no links to the
explanation; fixed.
```

**MANUAL: PART 4 EXPANDED — A FULL SWEEP FOR DUPLICATE AND ASYMMETRIC WEB/CLI EXPLANATIONS**

A systematic pass found the same mechanism explained twice (once per interface) in eight places, plus several facts documented for only one interface despite applying to both — all consolidated into one explanation each.

```
Manual
Consolidated into Part 4 or the existing Part 3 reference section, kept
interface-specific mechanics (menu numbers, buttons, keystrokes) alongside:
recipe DCP cascading recalculation, custom food/supplement profiles, the
Computed Daily Targets table, archiving semantics, local-cache-first search
priority and search-result-depth, broken-recipe-reference relinking.
Glycemic Load and Dietary Preferences reference sections gained the other
interface's missing instructions in place rather than duplicating.
```

**NEW TROUBLESHOOTING TOPIC: SEARCH RESULT ORDER CAN DEPEND ON WORD ORDER**

New troubleshooting entry explaining why the order you type search words in can affect which result comes out on top. [learn more...](#ts-search-order)

```
Manual
Covers the word-order-as-priority behavior introduced by the same-day
search ranking fix below.
```

**NEW PART 4: SHARED OPERATIONS**

Behavior that's genuinely identical across the web app and command line now has its own section instead of being explained twice or bolted onto one interface.

```
Manual
Using the Web App, Using the Command Line, Essential resources,
Troubleshooting and feedback, Possible Additional Features, and Appendices
all shift down one number (now Parts 5–10). Food Search Results reference
in Part 3 links here instead of duplicating.
```

**TROUBLESHOOTING: "A MEAL'S DCP ISN'T SHOWING" CORRECTED — DCP NO LONGER REQUIRES MARKING A MEAL COMPLETE**

Fixed outdated troubleshooting advice — a meal's DCP has not required marking the meal Complete to compute for some time now. The entry now explains the real cause when DCP is missing (no amino acid data yet on any item). [learn more...](#ts-meal-dcp)

```
Manual
Also clarifies what marking a meal Complete actually still affects — the
"provisional" flag on a day's total in Daily Summary, not whether DCP
itself appears.
```

**FOOD SEARCH RESULTS NOW RANK BY HOW MANY QUERY WORDS MATCH — AND WHICH ONES — BEFORE CONSIDERING SOURCE**

Search results across Foods, Meals & Log, and Recipes now rank primarily by how well your search words match a food's name, before considering whether it's from your pantry or an external source — so a genuinely better match no longer loses to something merely already in your own data. [learn more...](#food-search)

```
Foods: Search / Meals & Log: Add Food or Recipe / Recipes: Add Ingredient (CLI + web)
CLI previously had no text-relevance ranking for cached/pantry results
(pantry-first, then alphabetical); web's default view checked source before
match quality. Now both rank first by how many query words a name contains,
then by which words matched (earlier query words weigh more), then source
breaks any remaining tie. Web's "Pantry, Cache, then Other" option is
unchanged for strict source-first ordering; "Best match to name" (new
default) uses the corrected ranking.
```

**TROUBLESHOOTING AND FEEDBACK PROMOTED TO ITS OWN PART**

Troubleshooting help is now its own top-level manual Part instead of buried inside a resources section, matching how often you actually need it.

```
Manual
Was a subsection of Part 6 (Essential resources); now Part 7 in its own
right, with subheadings moved up a level. Parts 8 (Possible Additional
Features) and 9 (Appendices) shifted accordingly. #feedback anchor and all
?ts-... in-app help topics unchanged.
```

**MEAL ITEMS NOW LIST ALPHABETICALLY BY DEFAULT, WITH AN OPTION TO SWITCH BACK TO ENTRY ORDER**

A meal's food/recipe list now sorts alphabetically by default, making a meal with many items easier to scan. Switch back to the order you added things with the "o" CLI command or the web "Sort by" dropdown — the choice is remembered and shared between both.

```
Meals & Log (CLI + web)
Applies to the meal detail view and the per-meal breakdown on the Full Day
and Daily Summary web pages.
```

**USER BIBLIOGRAPHY: NEW "INTERNET RESOURCES" SECTION IN PART 6**

New annotated bibliography of external nutrition resources worth knowing about, alongside what NuMa itself provides.

```
Manual
Covers Examine.com, the FAO's DIAAS reference report, the Linus Pauling
Institute's Micronutrient Information Center, the NIH Office of Dietary
Supplements, Open Food Facts, and the University of Sydney's Glycemic
Index Database — each in APA format with a brief annotation, alphabetized
by author/organization.
```

**USER MANUAL BUILD SCRIPT NOW AUTO-COMPUTES WORD COUNT AND READING TIME**

The manual's "Reading time" figure at the top is no longer stale hand-typed guesswork — it's computed automatically on every build.

```
scripts/build_manual.py
Counts words in the source on every build, derives reading time at 225
words/minute, rewrites just that portion of the header line. The "Updated"
timestamp is still bumped by hand, per the version-stamp convention.
```

**PERFORMANCE: FOOD SEARCH AND ANALYZE-A-FOOD-PORTION PAGES NOW LOAD INSTANTLY; USDA/OPEN FOOD FACTS RESULTS ARRIVE A MOMENT LATER**

These two pages no longer wait on 2-3 external network calls before showing anything — they render instantly from your local cache/pantry/recipes, then fill in USDA/Open Food Facts results a moment later.

```
Foods → Search / Analyze a Food Portion (web)
Same background-fetch pattern already used by the meal add-food panel.
Fixed a real gap along the way: Food Search's synchronous search never
actually queried Open Food Facts (only USDA); the new background fetch
genuinely covers both. Yesterday's barcode-search addition is unaffected
(a direct lookup, not a broad search, so it still resolves immediately).
```

#### August 1

**MANUAL: THE "RATIO, NOT ABSOLUTE AMOUNT" IDEA BEHIND THE FAO REFERENCE STANDARD IS NOW EXPLAINED WHERE READERS FIRST MEET IT, AND LINKED EVERYWHERE ELSE IT'S USED**

The core idea that makes protein complementarity work — each essential amino acid is needed in a fixed ratio to total protein eaten, not some absolute daily amount — is now explained right in the introduction, with links out to it from everywhere the app cites an FAO reference figure.

```
Manual (Part 1 intro) + every screen citing an FAO amino acid reference (CLI + web)
Previously stated precisely only in Appendix A (now B), disconnected from
the plain-language brick-wall analogy in the intro. Intro analogy now
states the ratio explicitly and links to both the FAO 2013 Reference
Standard section and the full derivation. Every place the CLI or web app
shows an "FAO reference" figure — amino-acid-ratio tables, protein-quality
and complement-suggestion sections, "no suggestions needed" message — now
links to this explanation (?fao on the command line).
```

**NEW TROUBLESHOOTING CATEGORY: PORTION AND SERVING-SIZE DATA PROBLEMS**

New troubleshooting category for when a food's portion data is missing or wrong (e.g. an egg with only a 100 g figure, no "1 egg" option) — these are USDA data gaps, not NuMa bugs, and now have a documented home with fixes. [learn more...](#feedback)

```
Manual
Covers three forms: no per-piece/per-unit portion at all, a weight portion
with no cup/tablespoon equivalent (density unknown), and a portion/volume
conversion that's simply wrong in USDA's own record. Fix in each case:
weigh it yourself, or add/correct a custom portion via the Food Cache
Portions editor (persists across a later Refresh).
```

#### July 31

**NEW TROUBLESHOOTING SECTION: 13 REAL PROBLEMS, GROUPED BY HOW THEY FEEL RATHER THAN WHICH MENU THEY'RE IN**

Troubleshooting now covers 13 real problems, grouped by how they feel rather than which menu they're in — covering things easy to mistake for a bug (a dietary preference silently filtering search results, a meal's DCP capped below the DIAAS projection, a deleted recipe's ghost reference, and more). [learn more...](#feedback)

```
Manual
Filled in three previously-empty stub headings plus ten more topics
gathered from behavior already explained elsewhere but easy to mistake for
a bug. Grouped into five sections — Operating the program; I don't
understand...; I'm confused; I expected to see something and it's not
there; The numbers don't make sense — with cross-listing where a problem
could reasonably be searched for either way. Every topic is a working
?ts-... in-app help lookup.
```

**MANUAL: FULL PASS FOR NON-TECHNICAL READABILITY — JARGON, BROKEN SENTENCES, A WRONG MENU NUMBER, AND CLI-ONLY FEATURES NOW LABELED AS SUCH**

A full readability pass through the manual removed unexplained jargon, fixed broken sentences, corrected a wrong menu number, and labeled CLI-only features as CLI-only.

```
Manual
~2 dozen passages fixed: unexplained developer jargon (API keys, internal
names, min()/algebra notation, code-style comparisons like protein_g > 0)
rewritten in plain language or moved into "(For technically skilled
users: ...)" asides; several broken/garbled sentences (including the
manual's own DIAAS definition, a stray typo); empty TID glossary entry
filled in; wrong CLI menu number for Custom/Drafted Food Profiles
corrected ("Foods → 7" → "Foods → 8"); Claude AI amino-acid-fetch workflow
and Oxalate on/off switch labeled CLI-only, since the web app doesn't have
them yet — Oxalate section now also states that toggling it currently
requires the CLI (a real feature gap, not just documentation).
```

#### July 30

* MANUAL TABLE OF CONTENTS: SEARCH BOX NO LONGER SCROLLS OUT OF VIEW WHILE STEPPING THROUGH MULTIPLE HITS -  Manual (web page) - Jumping between search matches used to scroll the whole sidebar, including the search box and its Prev/Next buttons, out of view — you had to scroll back up to search-box and click the next-hit marker. Only the "Contents" list itself now scrolls to follow your position; the title and search box stay fixed in place above it.

#### July 29

* COMPLEMENT SUGGESTIONS NOW USE YOUR OWN FOOD DATA WHEN AVAILABLE, AND FLAG IT WHEN THEY DON'T -  Protein Complement Suggestions (CLI + web) search now checks your pantry, your recipes, and your broader food cache (any food you've ever looked up) for a real match before falling back to the built-in reference table, and any suggestion sized from that fallback is now clearly tagged "(estimated)" (a real food of yours, scaled from the reference table) or "(generic estimate)" (no real match at all — the reference food itself). A footer note explains what the tags mean and points to the more accurate, permanent alternative: the "estimate amino acids from another food" tool. [learn more...](#comp-estimate)

#### July 28

* WEB APP & CLI VERSION SAMPLE WORKFLOWS: NEW WORKFLOW 4 (MEALS & ANALYSIS), PLUS A LIGHTER "MORE THINGS WORTH TRYING" SECTION -  Manual - The three existing web workflows are now explicitly framed as one connected thread (protein complementarity), not a tour of every menu. Right after them: a short, non-step-by-step section highlighting Foods → Compare, Custom food profiles, sub-recipe nesting, and Archive/Restore; then a full new Workflow 4 covering full-day analysis, Daily Summary, Multiday Nutrient Trend, and Nutrient Plot. Workflow 2 now also points new users to Settings → Your Profile before starting. [learn more...](#sample-workflows-web)
* NUTRIENT PLOT: NEW LINE-SMOOTHING OPTION -  Analysis > Daily Summary > Nutrient plot (web) - A new **Smoothing (days)** field applies a trailing moving average to each plotted nutrient, defaulting to 3 days, to see the underlying trend through day-to-day noise. Set it to 0 to go back to the original, unsmoothed data. [learn more...](#nutrient-plot)
* NUTRIENT PLOT: CHOOSE WHICH NUTRIENT IS HIGHLIGHTED (DEFAULT: DAY DCP) -  Analysis > Daily Summary > Nutrient plot (web) - The "always red and solid" line was previously always Day DCP. A new **Highlight nutrient** dropdown lets you pick any currently-plotted nutrient instead — still defaults to Day DCP whenever it's one of your chosen nutrients. [learn more...](#nutrient-plot)
* NUTRIENT PLOT: BLACK & WHITE PREVIEW FOR NON-COLOR PRINTERS -  Analysis > Daily Summary > Nutrient plot (web) - A new "Black & white (printer-friendly)" checkbox renders every line in black, using a distinct dash pattern per nutrient instead of color (the highlighted nutrient stays solid). Works on-screen so you can preview it before printing, not just when printing. [learn more...](#nutrient-plot)
* NEW MANUAL SECTION: PNG VS. SVG, AND WHICH TO PICK -  Manual - Added a plain-language explanation of the Nutrient Plot's two download formats, linked from a new "Which format should I pick?" line next to the Download buttons. [learn more...](#plot-file-formats)
* NUTRIENT PLOT: SCALING NOW USES VARIANCE, NOT A FIXED ÷100, AND YOU CAN OVERRIDE IT -  Analysis > Daily Summary > Nutrient plot (web) - The previous fixed "divide by 100" rule could overshoot, turning the nutrient it was meant to rescue into the flat one instead (reported: Protein + Carbohydrates). Scaling now computes a factor from the ratio of the most-variable to least-variable plotted nutrient's standard deviation, which brings a dominant line down to roughly match the smallest without over- or under-correcting. A new **Scale factor** field on the plot page shows this computed value and lets you type your own instead. [learn more...](#nutrient-plot)

#### July 27

* NUTRIENT PLOT NOW AUTO-SCALES A DOMINANT NUTRIENT SO IT DOESN'T DROWN OUT A SMALLER ONE -  Analysis > Daily Summary > Nutrient plot (web) - Plotting Calories next to Protein (or Calcium next to Protein) used to flatten the smaller line to a barely-visible wiggle at the bottom. Any nutrient whose average is 5.5x or more the smallest plotted nutrient's average is now divided by 100 before plotting, noted right in its legend entry (e.g. "Calories (kcal) ÷100"). [learn more...](#nutrient-plot)
* RECENT DAYS NOW ALWAYS SHOWS PROTEIN, CALORIES, CARBS, AND FIBER -  Analysis > Daily Summary: Recent Days (CLI + web) - Four columns now always appear right after Day DCP: Protein (the raw, un-adjusted total — Day DCP is the digestibility-adjusted figure), Calories, Carbs (carbohydrates — sugars and starches), and Fiber. These are separate from your 6-column choice and can't be turned off; if you'd already picked one of them as an extra column, it's simply not shown twice. [learn more...](#meal-columns)
* NUTRIENT PLOT'S PICKER NOW LEADS WITH PROTEIN/CALORIES/CARBS/FIBER, INCLUDES CALORIES, AND SCROLLS VERTICALLY -  Analysis > Daily Summary > Nutrient plot (web) - The nutrient checklist now lists Protein, Calories, Carbohydrates (Sugars, starches), and Fiber first, matching Recent Days' mandatory columns — Calories wasn't previously plottable at all. The list is now a compact scrolling vertical column instead of a wide multi-per-row grid. [learn more...](#nutrient-plot)
* NEW: LINE PLOT ANY NUTRIENT ACROSS YOUR LOGGED DAYS -  Analysis > Daily Summary > Nutrient plot (web) - Pick up to 8 nutrients and a range of days (all logged days, or N days back from a chosen date), and NuMa draws a line chart with day on the x-axis. Missing days show as a gap in the line rather than a drop to zero. Printable via a stripped-down print page, and downloadable as a PNG. [learn more...](#nutrient-plot)
* MEAL IDS COLUMN IS WIDER SO ROWS AREN'T AS TALL -  Analysis > Food Use in Meals (web) - The Meal IDs column at the right of the results table is now about four times wider, so a food used across many meals lists its meal numbers with far less line-wrapping. [learn more...](#fooduse)
* CLICKING A MEAL ID FROM FOOD USE IN MEALS NOW GIVES YOU A WAY BACK -  Analysis > Food Use in Meals (web) - Clicking one of the meal numbers in the Meal IDs column now shows a "↩ Back to analysis" pill next to the breadcrumb on the meal page you land on, returning you to the exact search results you came from — matching how the main-nav breadcrumb already flags a memory-driven landing. [learn more...](#fooduse)
* A MEAL'S PAGE NOW SHOWS ITS ID NUMBER -  Meals & Log (web) - A meal's page title now shows its ID number in parentheses next to the date, so you can confirm you landed on the meal you meant to — useful right after following a Meal IDs link from Food Use in Meals.

#### July 26

* SEARCH RESULTS NOW RANK YOUR OWN RECIPES BELOW PANTRY AND CACHE FOODS, BUT STILL ABOVE USDA/OPEN FOOD FACTS -  Foods: Search / Meals & Log / Recipes: Add Ingredient (web) - Both sort modes previously treated Pantry, Cache, and your own Recipes as one tied-for-first group ahead of USDA/OFF results. Recipes now form their own middle tier — behind Pantry/Cache, still ahead of external results — so a recipe with a similar name no longer outranks an exact match already sitting in your Cache. [learn more...](#food-search)
* PRINTED RECIPE PAGES NOW SHOW THE RECIPE'S ID AND PROTEIN SCORE -  Recipes: Print/save recipe (web) - The print-friendly recipe page's header now lists the recipe's ID number and DCP in grams alongside servings and total yield, matching the detail you'd see on screen. [learn more...](#recipes-menu-web)

#### July 25

* RECIPE INGREDIENT SEARCH SHOWS AMINO ACID STATUS ON THE WEB, MATCHING THE TERMINAL APP -  Recipes: Add Ingredient (web) - The search results table for adding a recipe ingredient now shows the AA column already used everywhere else, so you can spot amino-acid data availability before adding a food. [learn more...](#food-search)
* FOODS SEARCH RESULTS PERSIST WHEN YOU STEP AWAY AND COME BACK -  Foods: Search (web) - Like the meal and recipe "add" searches already did, leaving to check something else and returning to Foods: Search now restores your last query and results instead of starting over. [learn more...](#search-memory)
* MAIN NAVIGATION REMEMBERS WHERE YOU WERE, PER SECTION -  Recipes / Meals & Log / Settings / Manual (web) - Clicking one of these in the top navigation now returns you to the exact page you were last on in that section — e.g. the specific recipe you were editing — instead of always jumping to its list page. When that memory is what brought you back, the page's breadcrumb is highlighted with a one-click "All recipes"/"All meals" link back to the plain list. [learn more...](#search-memory)
* A QUICK-RETURN LINK APPEARS NEXT TO FOODS WHEN THERE'S SOMEWHERE TO GO BACK TO -  Foods (web) - Foods is a drop-down of separate destinations, so it doesn't jump back the same way — instead, a small "↩" link appears next to it whenever you've viewed a food, showing that food's name, so you can return to it in one click after wandering off to Recipes or Meals & Log. [learn more...](#search-memory)
* AMOUNT FIELDS NOW SAY DIRECTLY THAT A PLAIN NUMBER MEANS GRAMS -  Foods / Recipes / Meals & Log (CLI + web) - Every place you type a portion amount now states, right there, that entering just a number with no unit is read as grams — previously this was true but unstated. [learn more...](#portion-formats)
* A RECIPE'S PROTEIN SCORE NOW UPDATES ITS PARENT RECIPES TOO -  Recipes - Changing a recipe that's used as an ingredient inside other recipes now recalculates DCP for those parent recipes as well, not just the one you edited directly — so a nested recipe's protein score is never left stale in whatever uses it. [learn more...](#recipes-menu-web)
* SUB-RECIPE INGREDIENTS ARE SCORED AS A WHOLE, NOT BROKEN BACK INTO THEIR RAW INGREDIENTS -  Recipes - When a recipe is used as an ingredient in another recipe, its protein-quality (DIAAS/DCP) contribution is now based on its own already-computed nutrient profile as a single item, instead of being decomposed back into its raw ingredients — so a sub-recipe deliberately built to complement its own limiting amino acid (e.g. a nut butter blended with a seed) gets credit for that pairing instead of it being hidden.
* MANUAL'S TABLE OF CONTENTS: CLICKING A COLLAPSED SECTION'S TITLE ALSO OPENS IT -  Manual (web) - Clicking a collapsed section's heading text in the sidebar contents now expands it in addition to taking you there, so it never looks "stuck" shut.

#### July 24

* WEB APP'S DIGESTIBLE COMPLETE PROTEIN EXPLANATION NOW MATCHES THE CLI WHEN IT'S CAPPED -  Meals & Log / Full Day / Recipes / Daily Summary (web) - When DCP is capped at your absorbed-protein ceiling, the web app now shows the same "capped" breakdown the terminal app already showed, instead of a plain raw-protein-times-DIAAS equation that no longer added up. A new "Learn more" link takes you straight to the explanation below. [learn more...](#dcp-cap)
* MANUAL'S TABLE OF CONTENTS NOW HIGHLIGHTS WHERE YOU ARE -  Manual (web) - The sidebar contents list now highlights the section you're currently reading as you scroll, and automatically expands a collapsed section if that's where you land, so you can always see the larger context of what's on screen.

#### July 23

* LOGGED DAYS KEEP THE USER PROFILE ACTIVE AT THE TIME THEY WERE LOGGED -  Analysis > Daily Summary - Each logged day now remains compared against whichever profile was active when you logged it, not whatever profile is active today — switching profiles for illness, travel, or a weight change no longer silently rescores your past days. You can also manually reassign which profile a specific day is compared against. [learn more...](#day-profile)
* RECENT DAYS SHOW YOUR DAILY DCP GOAL AND YOUR CHOSEN NUTRIENT COLUMNS -  Analysis > Daily Summary: Recent Days - Each day now shows its own protein (DCP) goal in grams, not just a percentage, and shows the same extra nutrient columns you chose for the Meals & Log list. [learn more...](#meal-columns)
* CHOOSE HOW MANY MEALS TO SHOW; CLEARER MEALS & LOG COLUMNS -  Meals & Log - Choose exactly how many meals to show via a number box, in place of the old "show all"/"show recent 9" toggle; Calories now appears before the DCP columns; column headers are stacked to fit more on screen; the "Search meal history" link now explains what it searches. [learn more...](#meals-list)
* MULTIDAY NUTRIENT TREND NOW LEADS WITH YOUR DCP AVERAGE -  Analysis > Multiday Nutrient Trend - This average-over-time view now leads with your average Digestible Complete Protein (DCP) instead of raw protein, since raw protein alone overstates what your body can actually use. [learn more...](#trend)
* SEARCH BOXES REMEMBER YOUR LAST SEARCH -  Meals & Log: Add Food or Recipe search / Recipes: Add Ingredient search (web) - If you follow a link away to look something up and come straight back, your last search and its results are restored automatically; a new "Reset search" button clears it back to the page's default.
* CONFIRM AMINO ACID DATA FOR SEARCH RESULTS ON DEMAND -  Foods: Search (web) - You can select foods showing the uncertain "~✓" amino-acid badge and click "Fetch full details for selected" to confirm, on demand, whether they truly have amino acid data. [learn more...](#food-search)
* ESTIMATE AMINO ACIDS BY COPYING FROM ANOTHER FOOD -  Foods: Drafted Food Profiles / Food Cache edit (CLI); Custom Food Profiles edit (web) - When entering a food's amino acid data, you can now search for and pick a similar food to copy amino acids from instead of typing them in by hand — values are scaled automatically to match the food's own protein content, and a note documenting the source is suggested for you. [learn more...](#drafted-foods)
* SEARCH RESULTS FOR RAW/WHOLE FOODS NO LONGER GET BURIED BEHIND BRANDED PRODUCTS -  Foods: Search / Meals & Log: Add Food or Recipe / Recipes: Add Ingredient (CLI + web) - USDA's own search ranking can bury a plain food like "Potatoes, flesh and skin, raw" — the version most likely to carry amino acid data — under branded and prepared-dish matches for the same word; the app now searches deeper to find them, and how deep is configurable in Settings > Advanced settings (0 = no limit). [learn more...](#food-data)
* CLICKING "MEALS" OR "RECIPES" IN THE BREADCRUMB NOW STARTS A FRESH SEARCH -  Meals & Log / Recipes: Edit (web) - Following the breadcrumb back to the list now clears your remembered search, so you land on a clean page; using the top "Meals & Log" menu link still brings your search back whenever you return to it. [learn more...](#search-memory)
* DAILY SUMMARY'S CHOSEN NUTRIENT COLUMNS NOW SHOW DATA FOR EVERY DAY -  Analysis > Daily Summary: Recent Days (CLI + web) - Fixed a bug where your chosen extra nutrient columns only had data for the couple of days you'd most recently opened; all logged days now show their numbers. [learn more...](#meal-columns)

#### July 22

* CHOOSE YOUR OWN EXTRA NUTRIENT COLUMNS FOR MEALS & LOG -  Meals & Log - You can now choose up to 6 extra nutrient columns, and their order, to show on the Meals & Log list, in both the terminal app and the web app. [learn more...](#meal-columns)
* SEE EACH FOOD OR RECIPE'S ID AND DATA SOURCE AT A GLANCE -  Foods / Recipes / Meals & Log - Every food and recipe name shown anywhere in the program now displays its ID number and data source (USDA, Open Food Facts, user-drafted, or recipe) right underneath it, so you can always trace what you're looking at back to its source.
* RECIPE PROTEIN COMPLETENESS RECALCULATES AUTOMATICALLY -  Recipes - A recipe's protein completeness (DCP) is now recalculated automatically whenever you change its ingredients or servings, instead of only when you explicitly ask for it.
* MANUAL NOW SPLIT INTO WEB APP AND COMMAND LINE PARTS -  Manual - The manual is now split into separate Web App and Command Line parts, so web users (most users) no longer have to read past command-line-only instructions. [learn more...](#how-to-read-this-manual)

#### July 20

* ARCHIVE FOODS, PANTRY ENTRIES, AND RECIPES YOU'RE NOT USING -  Foods / My Pantry / Recipes - You can now archive (reserve) a food, pantry entry, or recipe to hide it from search, complement suggestions, and everyday lists without deleting it or breaking anything that still references it — one click in the web app (Archive/Restore button, plus a Show Archived checkbox), or one command in the terminal app. [learn more...](#archive)

#### July 19

* IRON, ZINC, AND B12 GUIDANCE ADAPTS TO YOUR DIETARY PREFERENCE -  Analysis / Settings - If your dietary preference is set to vegetarian or plant-based, your iron and zinc daily targets are now automatically raised to reflect their lower absorption from plant foods, with an explanatory note; a warning also appears if your logged vitamin B12 intake is critically low on a plant-only diet. [learn more...](#diet-bioavailability)
* TRACK NUTRIENT TRENDS OVER 7, 14, OR 30 DAYS -  Analysis > Multiday Nutrient Trend - New view: average your nutrient intake over the last 7, 14, or 30 days against your targets, to catch a chronic shortfall that a single day's numbers would hide. [learn more...](#trend)
* IODINE AND SELENIUM NOW TRACKED ALONGSIDE YOUR OTHER MINERALS -  Settings > Nutrient Targets - Iodine and selenium are now tracked alongside your other minerals throughout the program.
* LOAD RECOMMENDED NUTRIENT TARGETS WITH ONE CLICK; SAFETY LIMITS APPLY AUTOMATICALLY -  Settings > Nutrient Targets - A new "load recommended optimal targets" action fills in sensible defaults (e.g. Vitamin D, EPA+DHA) for any nutrient you haven't already customized; built-in safe upper limits (iron, zinc, vitamin A, B6, iodine, selenium) now apply automatically even where you haven't set a personal max. [learn more...](#optimal)
* MY PANTRY NOW MATCHES FOOD CACHE COLUMNS; LINK A NAME-ONLY ENTRY TO REAL DATA -  My Pantry / Food Cache (web) - My Pantry now shows Type, AA, GI, and DIAAS columns matching the Food Cache; a new "Link a food" action lets you attach a name-only pantry entry to a searched food instead of creating a duplicate. [learn more...](#pantry)

#### July 16

* ANALYZING A MEAL NOW AUTO-SAVES ITS DCP AND CALORIES; ONE CALCULATE COMMAND FOR ALL/30/10 DAYS -  Meals & Log - Analyzing a meal now automatically saves its computed DCP and calories instead of only displaying them; a single Calculate command replaces the old p-command, letting you compute DCP and calories for all meals, the last 30 days, or the last 10 days at once. [learn more...](#meals-list)

#### July 15

* SET A PERSONAL TARGET ABOVE THE RDA, PLUS A DAILY SAFETY CAP, FOR ANY NUTRIENT -  Settings > Nutrient Targets - You can now set a personal target above the standard RDA for any nutrient (e.g. more vitamin D than the population minimum) and/or a personal daily safety cap — tracked alongside RDA everywhere nutrients are shown, with a warning color when your intake is near or over your cap. [learn more...](#optimal)
* UNSAVED FORM CHANGES NOW WARN YOU BEFORE YOU NAVIGATE AWAY -  Web app - Any editable form now warns you if you try to navigate away with unsaved changes, and shows a colored Save button when something's been edited.
* NEW DIAAS-BY-PROTEIN-SOURCE QUICK-REFERENCE TABLE IN THE MANUAL -  Manual - Added a DIAAS-by-protein-source quick-reference table for hand-estimating a packaged food's protein quality when it has no amino acid data. [learn more...](#diaas-estimate-table)
* FIND AND RELINK BROKEN RECIPE REFERENCES -  Recipes - A recipe ingredient that points to a food or recipe no longer in your cache (a "broken reference") can now be found and relinked, from a new Broken Recipe References list.
* FOOD USE IN MEALS NOW GROUPS CORRECTLY BY RECIPE, EVEN AFTER A RENAME -  Analysis > Food Use in Meals - Frequency-of-use history now groups correctly by recipe, so renaming a recipe no longer splits its history into two separate entries. [learn more...](#fooduse)
* VOLUME AMOUNTS FOR DRIED HERBS AND SPICES NO LONGER REJECTED -  Foods - Entering a volume amount (e.g. teaspoons) for dried herbs and spices like red pepper flakes is no longer rejected for lack of density data.
* QUICK DIETARY-PREFERENCE SWITCH NEXT TO EVERY COMPLEMENT SUGGESTIONS LIST -  Foods / Recipes / Meals / Analysis - A dropdown showing your current dietary preference, plus a "Change settings" link, now sits above every Protein Complement Suggestions list — change it on the spot without navigating to Settings and back. [learn more...](#diet)
* EVERY PERCENT-OF-TARGET NOW SHOWS WHETHER THE TARGET IS A MINIMUM, MAXIMUM, OR TARGET -  Foods / Recipes / Meals / Analysis - Every displayed nutrient percentage (protein, RDA, optimal goal) is now tagged `min`, `max`, or `target` inline, so a 120% reading is never ambiguous between "well past the minimum" and "over the safety cap." Previously this distinction was shown only on the Settings > Computed Daily Targets table. [learn more...](#daily-nutrient-targets)

---

### B. Raw protein, protein quality, and protein digestibility [appendix-b]

[//]: # "develop"

#### The core problems with protein

When you eat protein, not all of it is equally useful to your body. The usefulness depends on three things: **how much** protein you eat, and **how well-matched** its amino acid composition is to human physiological needs, and **how digestible** it is. 

#### The Nine Essential Amino Acids and their required relationship

Your body requires twenty amino acids to build proteins. Eleven of these it can synthesize from other raw materials. The remaining nine — the essential amino acids ([EAAs](#gloss-eaa)) — must come from food. 

These nine must all be present simultaneously for protein synthesis to proceed. They must also be present in the right amount. If any one of them is insufficiently supplied, then to the degree that its amount is short the other cannot be used. The surplus of the other eight cannot be stored and is instead broken down for energy — a functional waste.

In summary, the *pattern* of [EAAs](#gloss-eaa) in a food matters, not just the total protein quantity.

#### The required EAA pattern, established by the FAO

The Food and Agriculture Organization ([FAO](#gloss-fao)) of the United Nations leads international efforts to defeat hunger, achieve food security for all, and make sure that people have regular access to enough high-quality food to lead active, healthy lives.

Research has established human requirements for each [EAA](#gloss-eaa) independently, through controlled human trials. For each amino acid separately, researchers determined how much a healthy adult needs per day to maintain physiological function. From these studies came absolute daily requirement figures for each of the nine [EAAs](#gloss-eaa), expressed in milligrams per kilogram of body weight per day.

Separately, research has established how much total protein a healthy adult needs per day. By dividing each [EAA](#gloss-eaa)'s daily requirement by the total daily protein requirement, researchers produced a normalized figure: how many milligrams of each [EAA](#gloss-eaa) a person needs per gram of protein consumed. These normalized figures are the **[FAO](#gloss-fao) reference values**.

From the reference values for each amino acid which were determined *independently* come the ratios between [EAAs](#gloss-eaa). The reference values' relationship are a byproduct of the separately established requirements — not the starting point.

#### The FAO reference values tell you about the quality of protein in a food

The reference values allow a simple and powerful question to be asked about any food protein source:

> If I eat enough of this food to meet my total daily protein needs, will each essential amino acid also arrive in sufficient quantity?

If the answer is yes for all nine [EAAs](#gloss-eaa), the protein is high quality — no bottleneck will limit your body's ability to use it. If the answer is no for even one [EAA](#gloss-eaa), that amino acid becomes your limiting factor.

#### How the Ratio Is Calculated in NuMa

For each essential amino acid, the ratio shown in [NuMa](#gloss-numa)'s output is computed in two steps:

**Step 1 — convert [AA](#gloss-aa) amount to mg per gram of total protein:**

    (AA content in g per 100g food ÷ protein content in g per 100g food) × 1000

This expresses how many milligrams of that amino acid are present for every gram of total protein the food contains.

**Step 2 — divide by the [FAO](#gloss-fao) reference value:**

    mg AA per g protein ÷ FAO reference value (mg/g protein)

A ratio of 1.0 means the food hits the reference exactly. A ratio of 2.14 means it delivers more than twice the required amount. A ratio of 0.80 means it delivers only 80% of what is needed.

**Concrete example — cocoa ([USDA](#gloss-usda) #169594):**

    Cocoa Protein total:      19.6 g per 100g food
    Tryptophan AA in cocoa:   0.293 g per 100g food

    Step 1:  (0.293 / 19.6) × 1000  =  14.9 mg tryptophan per g protein
    Step 2:  14.9 / 7               =  2.14

The [FAO](#gloss-fao) reference value for tryptophan is 7 mg/g protein. Cocoa's protein delivers 14.9 mg/g — 2.14 times what is required.

Think for a moment: what if cocoa contained none of the needed [EAAs](#gloss-eaa)? Then the protein it contained would be unusable, if it were your only protein source. It could only be broken down for energy - the fate of all unusable protein. And what if it contained all the needed [EAAs](#gloss-eaa), in the right amount - except one was totally missing? That one would make all the other unusable.

#### Why Total Protein Is the Denominator

A reasonable question is why the ratio uses total protein (including non-essential amino acids) as its denominator rather than comparing [EAA](#gloss-eaa) amounts in absolute terms.

Total protein is a normalizing device — **a common scale that makes the quality metric meaningful across foods with very different protein concentrations and very different serving sizes.**

The practical interpretation is direct: **if a food's protein clears all nine floors, eating enough of that food to meet your daily protein target will automatically also deliver your daily [EAA](#gloss-eaa) requirements.** No separate [EAA](#gloss-eaa) accounting is needed. A food that fails even one floor means you would reach your protein target before accumulating enough of that [EAA](#gloss-eaa) — the protein source is insufficient on its own.

The non-essential amino acids that make up the rest of the protein are biologically irrelevant to this specific calculation. They appear in the denominator only because total protein is the natural unit for expressing protein intake. They are not required to "activate" the [EAAs](#gloss-eaa) — they are simply passengers.

#### What "Complete" Actually Means

"Complete" does not mean the amino acid ratios are all close to 1.0, or close to each other. It means **every one of the nine ratios is at or above 1.0** — each amino acid clears its own independent floor.

The nine [FAO](#gloss-fao) reference values were determined in separate human trials, one amino acid at a time. They are not ratios between amino acids; they are nine independent thresholds. Having tryptophan at 2.14× its floor while [Met+Cys](#gloss-met-cys) sits at 1.02× its floor creates no imbalance — the tryptophan surplus cannot compensate for a deficit in another amino acid, but it does not create one either.

A food can therefore have wildly varying ratios across its amino acids and still be complete. Cocoa's protein ranges from 1.02 to 2.25 across the nine amino acids — a factor of more than two between the lowest and highest — and is still complete because nothing falls below 1.0.

The floor analogy: imagine a building with nine rooms, each with its own minimum ceiling height requirement. A room that comfortably exceeds its requirement does not help or hurt any other room. Every room must pass independently.

#### The Limiting Amino Acid — A Practical Analogy

When any one [EAA](#gloss-eaa) ratio falls below 1.0, that amino acid is "limiting" — it acts as a bottleneck that caps how much protein your body can fully incorporate into tissue.

A concrete analogy: you are mixing mortar to build a small wall. You have plenty of dry mix but run out of water before you have mixed enough for the full job. Without water, the remaining dry mix is unusable — you can build only 90 bricks worth of wall instead of 150. The water is your [limiting amino acid](#gloss-limiting-amino-acid). The unused dry mix is the protein your body cannot build into tissue, and instead breaks down and excretes.

Complementary proteins work by pooling the [limiting amino acids](#gloss-limiting-amino-acid) from multiple foods — a grain that is low in lysine paired with a legume that is rich in lysine can together clear all nine floors even though neither does so alone.

#### The DIAAS Score

The Digestible Indispensable Amino Acid Score ([DIAAS](#gloss-diaas)) measures how much of a food's protein your body can actually use. For each [EAA](#gloss-eaa), it calculates:

> (mg of that [EAA](#gloss-eaa) actually absorbed per gram of food protein) ÷ ([FAO](#gloss-fao) reference value for that [EAA](#gloss-eaa))

The word "actually absorbed" is critical. Not all amino acids in a food survive digestion intact and cross into the bloodstream. [DIAAS](#gloss-diaas) uses [ileal digestibility](#gloss-ileal-digestibility) — the fraction of each amino acid absorbed by the end of the small intestine — to correct for this. The result is a score based on what your body actually receives, not merely what was in the food.

A ratio of 1.0 means the food **delivers** exactly the required amount of that [EAA](#gloss-eaa) (per gram of protein eaten). A ratio below 1.0 means a shortfall — that [EAA](#gloss-eaa) is limiting. A ratio above 1.0 means a surplus above the floor. **The overall [DIAAS](#gloss-diaas) score for the food is set by whichever [EAA](#gloss-eaa) has the lowest ratio — the weakest link.**

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

Every ratio exceeds 1.0. This means that if you eat enough chia seed to meet your total daily protein requirement, every one of the nine [EAAs](#gloss-eaa) will arrive in at least the required amount. No bottleneck. No [limiting amino acid](#gloss-limiting-amino-acid). The protein is complete and efficiently usable.

Lysine at 1.30 is the weakest link — your slimmest margin. It would be the first amino acid to fall below the floor if you ate progressively less chia. But at 1.30, it still clears the threshold comfortably.

Importantly, these ratios do *not* mean that 100 grams of chia seed provides all the [EAAs](#gloss-eaa) you need for a day. Chia seed contains roughly 17 grams of protein per 100 grams. If your daily protein target is 80 grams, 100 grams of chia gets you only about 21% of the way there. The quality score tells you that every gram of protein chia delivers is efficiently usable — but you still need to eat enough of it to accumulate your daily protein target.

Think of it like fuel efficiency: a car that gets 50 miles per gallon is efficient, but knowing that tells you nothing about whether one gallon is enough to reach your destination. Quality and quantity are separate questions answered separately.

#### Summary

| Concept | What it answers |
|---|---|
| [FAO](#gloss-fao) reference values | How many mg of each [EAA](#gloss-eaa) a human needs per gram of protein consumed |
| [DIAAS](#gloss-diaas) ratio for one [EAA](#gloss-eaa) | Does this food deliver enough of that [EAA](#gloss-eaa), accounting for digestibility? |
| Overall [DIAAS](#gloss-diaas) score | What is the weakest link — the most limiting [EAA](#gloss-eaa) in this food? |
| Ratio > 1.0 for all [EAAs](#gloss-eaa) | [Complete protein](#gloss-complete-protein): no bottleneck, full usability of what you eat |
| Daily protein target | Separate calculation: how many grams of protein do you need total? |

The [DIAAS](#gloss-diaas) table characterizes the quality of each gram. Hitting your daily protein target is about counting how many grams you eat.

### C. Plant protein sources in your pantry [appendix-c]

("pantry" here has two meanings: your actual pantry, and the pantry database that is in numa (see the Foods dropdown menu), which is a list of foods in your actual pantry.)

This appendix profiles the plant protein sources currently kept in a typical [NuMa](#gloss-numa) pantry, including nutritional yeast, which is not a plant but is grouped here because it fills the same dietary role. For each source: what form it takes, where it comes from, its essential amino acid ([EAA](#gloss-eaa)) strengths and weaknesses relative to the [FAO](#gloss-fao) reference values described in [Appendix B](#appendix-b), and its typical role in cooking.

The [EAA](#gloss-eaa) notes below describe general tendencies for each food, not a substitute for running the food itself through [NuMa](#gloss-numa). Growing conditions, processing, and the specific [USDA](#gloss-usda) or Open Food Facts[^3] record behind a given entry all shift the exact numbers — use [NuMa](#gloss-numa)'s own amino acid ratio and [DIAAS](#gloss-diaas) output for precise figures. Sourcing and cost information for these foods is addressed separately, not here.

BEFORE GOING ANY FURTHER: You should know that the two most useful foods below (aside from staples like whole wheat flour) are nutritional yeast and hulled hemp seed. Both are incredibly nutritious and useful. Nutritional yeast adds umami to any food, and hulled hemp seed is invaluable when eating legumes.

#### Seeds

**Chia seeds**

- *Form:* tiny oval seeds, black or mottled grey-brown, about 1mm long.
- *Source:* *Salvia hispanica*, a flowering mint-family plant native to Mexico and Guatemala.
- *[EAA](#gloss-eaa) profile:* unusually complete for a plant seed — as worked through in Appendix B, chia clears all nine [EAA](#gloss-eaa) floors, with lysine as its narrowest margin (~1.3× the reference). One of the few standalone-complete plant proteins in this pantry.
- *Culinary role:* primarily a functional/textural addition rather than a bulk protein source — a gelling agent for puddings, an egg replacer in baking (roughly 1 Tbsp ground chia + 3 Tbsp water per egg), and a smoothie thickener.
- *Also worth knowing:* must be ground or soaked until gelled — the intact seed coat lets whole chia pass through largely undigested.

**Ground flax seeds**

- *Form:* fine golden-brown to reddish-brown meal (pre-milled — whole flaxseed is a hard, shiny, oval seed instead).
- *Source:* *Linum usitatissimum*.
- *[EAA](#gloss-eaa) profile:* good, though a step below chia; lysine is typically its narrowest margin. A useful contributor, especially alongside grains.
- *Culinary role:* the same functional role as chia — egg replacer, binder, and fiber/omega-3 booster in baked goods and oatmeal; a meaningful protein contributor only at larger doses.
- *Also worth knowing:* ground flax oxidizes faster than whole flaxseed — keep it refrigerated or frozen, and use it within a few months of grinding.

**Hulled hemp seeds**

- *Form:* small, soft, pale green-to-tan kernels (already shelled).
- *Source:* *Cannabis sativa* (non-psychoactive hemp variety).
- *[EAA](#gloss-eaa) profile:* one of the better-balanced plant proteins here — good in the sulfur amino acids (methionine + cysteine), a category where legumes are typically weak, with lysine as its more [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* a standalone protein/texture addition to smoothies, granola, salads, and oatmeal; its nutty flavor and sulfur-amino-acid strength make it a good complement to legume-heavy meals.
- *Also worth knowing:* eaten raw with no preparation needed — it digests readily as sold.

**Sunflower seed kernels**

- *Form:* small, flattish oval kernels, off-white to pale grey with a green tinge.
- *Source:* *Helianthus annuus*.
- *[EAA](#gloss-eaa) profile:* moderate protein source; methionine is relatively strong while lysine is the more [limiting amino acid](#gloss-limiting-amino-acid) — roughly the mirror image of many legumes, which makes it a reasonable grain/legume complement.
- *Culinary role:* snack, salad topping, and seed butter; a minor protein contributor at typical serving sizes.
- *Also worth knowing:* high fat content gives raw kernels a short shelf life — refrigerate or freeze to prevent rancidity.

#### Grains & Pseudocereals

**Buckwheat, whole grain**

- *Form:* small, hard, three-cornered (pyramid-shaped) brown-green groats.
- *Source:* *Fagopyrum esculentum* — a pseudocereal, not a true grass/cereal despite the name; botanically closer to rhubarb and sorrel.
- *[EAA](#gloss-eaa) profile:* unusually well-balanced for a grain-like food — notably better in lysine than true cereals (wheat, corn, rice), the classic cereal weak point; more often limiting in leucine or the sulfur amino acids instead.
- *Culinary role:* a base ingredient (groats, kasha, buckwheat flour, soba noodles) rather than an addition; naturally gluten-free, which makes it a useful wheat substitute in a plant-based, protein-conscious diet.
- *Also worth knowing:* the hull surrounding the raw groat is inedible and is always removed before sale.

**Oats, whole grain, rolled**

- *Form:* flattened, cream-colored flakes (steamed and rolled whole groats).
- *Source:* *Avena sativa*.
- *[EAA](#gloss-eaa) profile:* among the stronger true cereals for protein quality — higher lysine than wheat or corn, though lysine is typically still the [limiting amino acid](#gloss-limiting-amino-acid); a solid moderate-quality grain protein overall.
- *Culinary role:* a base ingredient — porridge, baked goods, granola — that can carry a meaningful share of daily protein at typical serving sizes, unlike most seeds or nuts used as garnish.
- *Also worth knowing:* often processed in facilities shared with wheat — check labeling if strict gluten-free status matters.

**Cornmeal, whole-grain, yellow**

- *Form:* coarse-to-medium granular yellow meal (ground dried corn kernels, germ and bran retained).
- *Source:* *Zea mays*.
- *[EAA](#gloss-eaa) profile:* the classic maize deficiency pattern — low in both lysine and tryptophan; one of the more amino-acid-limited grains in this pantry, and a strong candidate for legume pairing (the traditional corn-and-beans combination).
- *Culinary role:* a base ingredient — cornbread, polenta, breading — rather than a minor addition.
- *Also worth knowing:* whole-grain (not degermed) cornmeal is more nutrient-dense but has a shorter shelf life than degermed cornmeal, due to the retained germ oil.

**Whole wheat flour, unenriched**

- *Form:* fine tan-brown powder (whole grain milled, bran and germ retained).
- *Source:* *Triticum aestivum*.
- *[EAA](#gloss-eaa) profile:* lysine is severely limiting — wheat protein (gluten) is notably poor in lysine, the sharpest deficiency among the grains in this pantry; threonine is often a secondary [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* a base ingredient for baked goods, and a major contributor to daily protein for anyone eating bread-based meals regularly — its lysine gap matters more in practice than seeds used only as garnish.
- *Also worth knowing:* "unenriched" means it lacks the iron/B-vitamin fortification added to most commercial white flour — a micronutrient note, not an amino acid one.

#### Tree Nuts & Peanuts

**Almond flour**

- *Form:* fine off-white powder (blanched almonds, ground).
- *Source:* *Prunus dulcis*.
- *[EAA](#gloss-eaa) profile:* relatively low overall protein density among nuts; lysine is the more [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* a base flour substitute in gluten-free/low-carb baking rather than a protein-boosting addition — its protein contribution is secondary to its role as a wheat-flour replacement.
- *Also worth knowing:* high fat content means a shorter shelf life than wheat flour — refrigerate or freeze.

**Cashew nuts**

- *Form:* kidney-shaped, ivory-white nuts.
- *Source:* *Anacardium occidentale* (the seed attached to the cashew apple).
- *[EAA](#gloss-eaa) profile:* comparatively favorable lysine for a tree nut, but generally low in the sulfur amino acids (methionine, cysteine) — a common tree-nut weakness.
- *Culinary role:* snack, cashew cream/cheese base, stir-fry addition; a significant contributor when used as a cream or sauce base in quantity, minor as a garnish.
- *Also worth knowing:* raw cashews are commonly soaked before blending into cream or cheese to soften texture — this is purely textural, not required for digestibility.

**Pecans**

- *Form:* smooth, elongated, ridged, brown-shelled halves.
- *Source:* *Carya illinoinensis*.
- *[EAA](#gloss-eaa) profile:* low overall protein density; lysine and the sulfur amino acids are both comparatively limited — pecans are more valuable here for fat and mineral content than as a protein source.
- *Culinary role:* garnish or mix-in (baked goods, salads); a minor protein contributor at typical serving sizes.
- *Also worth knowing:* high polyunsaturated fat content makes pecans prone to rancidity — store refrigerated or frozen.

**Walnuts, English**

- *Form:* wrinkled, brain-like lobed, brown-shelled halves.
- *Source:* *Juglans regia*.
- *[EAA](#gloss-eaa) profile:* a similar pattern to pecans — lysine limiting, modest sulfur amino acid content — notable mainly for omega-3 (ALA) content rather than protein quality.
- *Culinary role:* garnish or mix-in; a minor protein contributor.
- *Also worth knowing:* also prone to rancidity — refrigerate or freeze for storage.

**Brazil nuts**

- *Form:* large, dense, hard, off-white kernels with a rough triangular cross-section.
- *Source:* *Bertholletia excelsa*, native to the Amazon rainforest.
- *[EAA](#gloss-eaa) profile:* the exception among tree nuts — unusually rich in the sulfur amino acids (methionine and cysteine), the opposite weakness pattern from most nuts; lysine remains their more [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* snack, or a minor addition to trail mixes and baked goods — valuable precisely because it complements legume-heavy meals that tend to be sulfur-amino-acid-poor.
- *Also worth knowing:* the most concentrated food source of selenium known — a commonly cited ceiling is 1-2 nuts a day; eating many daily risks selenium toxicity, a separate issue from protein content worth tracking alongside it.

**Peanuts**

- *Form:* oblong, tan-shelled kernels (botanically a legume, not a true nut).
- *Source:* *Arachis hypogaea*.
- *[EAA](#gloss-eaa) profile:* better lysine than true tree nuts, consistent with its legume biology, but methionine and cysteine are its more [limiting amino acids](#gloss-limiting-amino-acid) — the classic legume weak point.
- *Culinary role:* snack, peanut butter, sauces; a substantial protein contributor at typical serving sizes, comparable to some legumes.
- *Also worth knowing:* raw peanuts are susceptible to aflatoxin-producing mold in storage — buy from a source with good turnover and store cool and dry. This is a food-safety note, not an amino acid one.

#### Soy-Based Foods

**Tofu, firm**

- *Form:* a solid, off-white curd block, custard-to-firm texture depending on how it was pressed.
- *Source:* coagulated soy milk (*Glycine max*), pressed to remove whey.
- *[EAA](#gloss-eaa) profile:* among the most complete plant proteins available — soy protein clears nearly every [EAA](#gloss-eaa) floor, with methionine/cysteine typically its only mildly [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* a primary protein ingredient — it stands in for meat or eggs across a wide range of dishes rather than functioning as a minor addition.
- *Also worth knowing:* pressing firmness determines water content and therefore protein density per gram — firm and extra-firm tofu concentrate protein relative to soft or silken tofu.

**Pure okara flour**

- *Form:* a fine, pale tan powder — dried and milled okara, the fibrous pulp left over from making soy milk and tofu.
- *Source:* a byproduct of soy milk production, from *Glycine max*.
- *[EAA](#gloss-eaa) profile:* a similar amino acid pattern to whole soy (methionine/cysteine mildly limiting), but the retained fiber and cell-wall material reduce digestibility relative to tofu or soy protein isolate — expect a lower [DIAAS](#gloss-diaas) despite a similar raw amino acid pattern.
- *Culinary role:* a flour substitute or booster in baked goods, veggie burgers, and pancakes — a byproduct-recycling ingredient rather than a dedicated protein powder.
- *Also worth knowing:* the reduced digestibility, not reduced amino acid content, is the thing to watch — check [NuMa](#gloss-numa)'s digestibility-adjusted ([DIAAS](#gloss-diaas)) figures rather than raw [AA](#gloss-aa) ratios for this one.

**Soy protein isolate**

- *Form:* a fine, white-to-off-white powder with minimal flavor.
- *Source:* soy protein extracted and concentrated to 90%+ protein by weight, with fiber, carbohydrate, and fat removed.
- *[EAA](#gloss-eaa) profile:* one of the highest-quality plant proteins available, with high digestibility (~0.95, as noted under "SPI" in the Glossary) — it clears essentially every [EAA](#gloss-eaa) floor, with methionine/cysteine still its narrowest margin.
- *Culinary role:* a concentrated protein-boosting addition — smoothies, baked goods, meat analogs — rarely eaten as a standalone dish, but very effective at raising a meal's complete-protein grams without much bulk or flavor change.
- *Also worth knowing:* as a concentrate rather than a whole food, it also strips out the fiber, [phytonutrients](#gloss-phytonutrients), and micronutrients present in whole soy — best treated as a protein-density tool, not a whole-food replacement for tofu or edamame.

#### Other Protein Concentrates

**Unsweetened pea protein powder**

- *Form:* a fine, off-white to pale yellow powder.
- *Source:* yellow split peas (*Pisum sativum*), protein-extracted and concentrated.
- *[EAA](#gloss-eaa) profile:* notably good lysine content — peas are a classic lysine-rich legume — but methionine/cysteine are clearly limiting, the reason pea protein is so often blended commercially with rice protein, which has the opposite pattern.
- *Culinary role:* a concentrated protein-boosting addition, the same role as soy protein isolate — smoothies, baking, general protein boosting — and it is a particularly effective complement to a grain-based meal (cereal, rice, wheat) that is itself lysine-poor but has adequate sulfur amino acids.
- *Also worth knowing:* the single best complement in this pantry for grain-heavy meals (bread, oats, cornbread), specifically because its strength (lysine) matches their specific weakness.

**Vital wheat gluten**

- *Form:* a fine, tan powder — nearly pure wheat protein with the starch washed out.
- *Source:* wheat flour (*Triticum aestivum*), processed to isolate the gluten protein fraction.
- *[EAA](#gloss-eaa) profile:* the most lysine-poor protein in this entire pantry — gluten is almost devoid of lysine, and concentrating the protein by removing the starch does not fix this; it simply delivers more of the same imbalanced amino acid pattern per gram.
- *Culinary role:* as much a structural/textural ingredient (seitan base, bread dough strengthener) as a protein source — it is often eaten as a primary "meat analog" ingredient (seitan) despite its poor amino acid balance, so it especially needs deliberate complementing with a lysine-rich food (legumes, pea protein) in the same meal or day.
- *Also worth knowing:* because seitan dishes are sometimes treated as a standalone "meat" replacement, this is the food in the pantry most likely to create an unnoticed lysine gap if eaten alone in quantity.

#### Nutritional Yeast

**Nutritional yeast flakes**

- *Form:* yellow flakes of deactivated, dried yeast. Flakes are less dense than powder, so measure by weight rather than volume when precision matters — a point already flagged in this pantry's notes for this item.
- *Source:* *Saccharomyces cerevisiae*, grown on a sugar-based medium, then deactivated (killed) and dried. Deactivation means it will not leaven anything or grow in the gut, unlike active baker's or brewer's yeast.
- *[EAA](#gloss-eaa) profile:* a good-quality, fairly [complete protein](#gloss-complete-protein) for a non-legume source, generally decent across the [EAAs](#gloss-eaa); the sulfur amino acids (methionine especially) tend to be its relative weak point, similar to soy and legumes generally.
- *Culinary role:* usually an addition rather than a primary ingredient — its concentrated umami (glutamate-driven) flavor makes it a savory, cheese-like flavoring for popcorn, pasta, sauces, and roasted vegetables, and it thickens liquids when whisked into a roux-based sauce (as in "nooch" cheese sauce). It can also become a primary ingredient in dishes built around it, such as cashew-and-nutritional-yeast "yeast cheese," where it supplies both flavor and a meaningful protein contribution.
- *Also worth knowing:* most commercial brands are fortified with B12 (and sometimes other B vitamins) — worth checking the label, since this is often the primary reason vegans include it in their diet, independent of its protein content.

### D. Glycemic load (GL) and Blood Glucose Comparison [appendix-d]

Glycemic load is a useful approximation, but no single formula-derived figure reliably predicts an individual's blood glucose response to a mixed meal. Three reasons account for this:

- The fat and protein suppression effect varies by person, by degree of insulin resistance, and by the specific foods involved.
- [GI](#gloss-gi) values were measured in healthy subjects and may not translate directly to someone with diabetes or insulin resistance.
- Individual glucose responses to identical meals vary substantially, even in the same person on different days.

[GL](#gloss-gl) is therefore most reliable when comparing meals of broadly similar composition — two different grain-based breakfasts, for example. When meals differ significantly in fat or protein content, the calculated [GL](#gloss-gl) will understate the difference in actual glycemic impact.

#### Continuous Glucose Monitoring

The practical gold standard today is continuous glucose monitoring ([CGM](#gloss-cgm)) — devices such as the Dexterity G7 or Libre 3 that measure interstitial glucose every few minutes. A person with diabetes can eat a meal, watch their glucose curve in the accompanying app, and directly compare their own real response across different meal choices over time. No formula approaches this for accuracy in individual prediction.

#### Predictive Apps

Some applications (January AI, Levels) go a step further, using machine learning models trained on large [CGM](#gloss-cgm) datasets to predict glucose response to a described meal before it is eaten — effectively personalising the [GI](#gloss-gi) and [GL](#gloss-gl) concepts. These predictions are probabilistic rather than exact, but they represent the closest available alternative to direct measurement.

#### Clinical Practice Without CGM

For clinical guidance without [CGM](#gloss-cgm), dietitians working with people with diabetes typically use carbohydrate counting combined with qualitative judgment about fat and protein content, rather than relying on [GL](#gloss-gl) as a single summary figure. [GL](#gloss-gl) remains a reasonable guide for comparing meals similar in structure, but should not be the deciding number when fat and protein differ significantly between the options being considered.

### E. FAO 2013 Amino Acid Reference Values

Under development.

[//]: # "develop section"

### F. Full Nutrient Key

Under development.

[//]: # "develop section"

### G. Protein ingestion timing

Under development.

[//]: # "develop section"

Resources:

* https://runningmagazine.ca/health-nutrition/could-you-be-timing-your-protein-all-wrong/

### H. Meal timing

Under development.

[//]: # "develop section"

Resources:

* https://www.theguardian.com/commentisfree/2026/may/05/game-changer-good-health-scientists-we-are-when-we-eat - article by expert

### I. Why some foods appear only in DIAAS-boosting suggestions [comp-appendix]

This appendix explains why certain nutritionally excellent protein sources — soy protein isolate, nutritional yeast, pea protein — sometimes appear only in the [DIAAS](#gloss-diaas)-boosting tier and not as gap closers, even though they are well-known complements to legumes.

DIGESTIBILITY-DRIVEN GAPS

When a legume such as pinto beans has a low [DIAAS](#gloss-diaas) (e.g., 0.73), that low score is often not caused by a weak amino acid profile. Pinto beans' raw [Met+Cys](#gloss-met-cys) ratio is approximately 22 mg/g protein — right at the [FAO](#gloss-fao) reference of 22. The gap emerges only because its true [ileal digestibility](#gloss-ileal-digestibility) is 0.80: the body absorbs only 80% of the protein, which pulls every amino acid's effective contribution below the reference threshold.

The gap-closer formula accounts for this by raising the target threshold:

    Adjusted target = FAO reference ÷ base digestibility
                     = 22 mg/g ÷ 0.73 = 30.1 mg/g

A gap closer must have an amino acid/protein ratio above 30.1 mg/g to mathematically close the [Met+Cys](#gloss-met-cys) gap. Most plant proteins are excluded:

    Soy protein isolate  Met+Cys  =  23.0 mg/g  (below 30.1) → excluded
    Nutritional yeast    Met+Cys  =  21.2 mg/g  (below 30.1) → excluded
    Sesame seeds         Met+Cys  =  49.7 mg/g  (above 30.1) → qualifies

This is mathematically correct: because pinto beans absorb poorly, you need a complement with a disproportionately high amino acid ratio to overcome the digestibility deficit in the gap-closer framework. Sesame qualifies; [SPI](#gloss-spi) and nutritional yeast do not.

WHY [DIAAS](#gloss-diaas)-BOOSTING STILL WORKS FOR [SPI](#gloss-spi)

The [DIAAS](#gloss-diaas)-boosting formula takes a different view. Instead of asking "can this food close the gap for pinto beans alone?", it asks: "what happens when I pool the digestible amino acids from pinto beans and SPI together?"

    Pooled digestible Met+Cys = (pinto's Met+Cys × 0.80)
                              + (SPI's Met+Cys per 100g × grams of SPI added ÷ 100 × 0.95)

    Pooled protein total = pinto's raw protein
                          + (SPI's raw protein per 100g × grams of SPI added ÷ 100)

Because [SPI](#gloss-spi) has a much higher digestibility (0.95 vs. 0.80), its amino acids contribute more efficiently per gram than pinto's own amino acids do. At approximately 25-35 g of [SPI](#gloss-spi) added to 100 g of pinto beans, the pooled meal [DIAAS](#gloss-diaas) reaches 0.90 — a meaningful improvement from 0.73.

The reason [SPI](#gloss-spi) still can't be a gap closer is that its raw [Met+Cys](#gloss-met-cys) ratio (23 mg/g) is below the inflated 30.1 mg/g threshold the gap-closer formula requires. But in the [pooled DIAAS](#gloss-pooled-diaas) calculation, where each food's digestibility applies only to its own amino acids, [SPI](#gloss-spi)'s superior digestibility (0.95 vs. pinto's 0.80) is sufficient to lift the combined score above the target.

PRACTICAL INTERPRETATION

From a dietary standpoint both tiers are useful, but they mean different things:

Gap closers (sesame, Brazil nuts, hemp seeds): these close the specific amino acid deficiency. After adding them, the combined protein is mathematically complete per the gap-closer model. Required amounts are often small (8-30 g).

[DIAAS](#gloss-diaas) boosters (soy protein isolate, nutritional yeast, egg, whey): these are high-quality proteins with excellent digestibility. They raise the effective quality of the whole meal by contributing highly digestible amino acids. A meal [DIAAS](#gloss-diaas) of 0.90 means 90% of the meal's protein is both complete and bioavailable — a strong nutritional outcome even if the precise gap-closer criterion isn't met.

In practice, combining a gap closer (e.g., sesame tahini) with a [DIAAS](#gloss-diaas) booster (e.g., a small serving of Greek yogurt or egg) gives both a complete amino acid profile and high overall digestibility — the best outcome for protein quality from a high-legume meal.

THE REFERENCE VALUES

NuMa uses two slightly different reference sets:

Gap-closer tier (an older reference table): [Met+Cys](#gloss-met-cys) = 22 mg/g, Lysine = 45 mg/g, Leucine = 59 mg/g

[DIAAS](#gloss-diaas)-booster tier ([FAO](#gloss-fao) 2013, Table 6 — the current authoritative reference): [Met+Cys](#gloss-met-cys) = 23 mg/g, Lysine = 48 mg/g, Leucine = 61 mg/g

The small differences (1-3 mg/g) reflect different published [FAO](#gloss-fao) tables used for these two tiers. Both are within normal rounding variance across [FAO](#gloss-fao) publications. The gap-closer tier's values are the older set; the [DIAAS](#gloss-diaas)-booster tier uses the authoritative [FAO](#gloss-fao) 2013 adult reference pattern.

(For technically skilled users: in NuMa's source code these two tables are `usda_api.AA_REFERENCE_MG_PER_G_PROTEIN` and `diaas.FAO_REFERENCE`, respectively.)

### J. Portion Input Formats [portion-formats]

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

NuMa converts volume to grams via the food's recorded density. If density is unknown for a food, it asks you to supply the weight manually. Common dried herbs and spices (pepper flakes, cinnamon, cumin, oregano, garlic powder, and dozens more) have built-in density estimates, since these are almost always measured by the teaspoon or tablespoon rather than weighed — including a generic fallback for any USDA "Spices, ..." entry not individually itemized.

    c  cup  cups                cups  (1 c = 236.6 ml)
    T  tbsp  tablespoon  tablespoons    tablespoons  (1 T = 14.8 ml)
    t  tsp  teaspoon  teaspoons     teaspoons  (1 t = 4.9 ml)
    ml  milliliter  milliliters  cc   milliliters
    floz                         fluid ounces  (1 floz = 29.6 ml)
    l  liter  liters             liters  (1 l = 1000 ml)

Note: T (uppercase) means tablespoon; t (lowercase) means teaspoon. These two are case-sensitive. All other units are case-insensitive.

PIECE / COUNT UNITS

    pc  pcs  piece  pieces  each  ea  count  ct  item  items

Piece entries record a count but no gram weight. The program will ask you to confirm or supply a weight if it needs one for nutrient scaling. Unlike weight and volume units, piece units require a space: "2 pc", not "2pc".

[USDA](#gloss-usda) STANDARD PORTIONS

Many [USDA](#gloss-usda) foods include pre-defined portion sizes (e.g. "1 medium egg", "1 cup sliced"). These are listed at the portion prompt and can be selected by number:

    p1         select USDA portion #1
    p2         select USDA portion #2
    1.5 p1     one-and-a-half times USDA portion #1

OMITTING THE SPACE

For all weight and volume units, the space between the number and unit is optional. These pairs are identical:

    2 T    =   2T
    0.25 c =   0.25c
    150 g  =   150g
    3 oz   =   3oz
    1/4 c  =   1/4c

(Piece units — pc, each, etc. — always require a space.)

VOLUME WITH EXPLICIT WEIGHT

When you know both the volume measure and the exact gram weight, you can supply both on one line. NuMa records the weight and labels the entry with the volume for readability:

    2 T 30g         →  30 g  (labeled "30 g (2 T)")
    1/4 c 60 g      →  60 g  (labeled "60 g (1/4 c)")

BARE NUMBER

A bare number with no unit is assumed to be grams; each amount field's example text says so directly.

### K. Worked validation example — meal-level DIAAS for pinto beans + quinoa [appendix-k]

This appendix lets you verify [NuMa](#gloss-numa)'s protein quality calculation independently. Every step is shown explicitly so you can reproduce it in a spreadsheet or calculator, then compare your result with what [NuMa](#gloss-numa) produces when you enter these two foods as a meal.

#### The two foods

| Food | [FDC ID](#gloss-fdc-id) | Data type | [USDA](#gloss-usda) source |
|------|--------|-----------|-------------|
| Beans, pinto, mature seeds, cooked, boiled, with salt | 173796 | SR Legacy | https://fdc.nal.usda.gov/food-details/173796/nutrients |
| Quinoa, cooked | 168917 | SR Legacy | https://fdc.nal.usda.gov/food-details/168917/nutrients |

All nutrient values below are drawn directly from those pages as of June 2026. The demo uses **100 g of each food** — round numbers that make the arithmetic easy to follow.

---

#### Step 1 — Individual nutrient profiles (per 100 g, from USDA)

**Table I-1. Macronutrients and key micronutrients**

| Nutrient | Unit | Pinto beans ([FDC](#gloss-fdc) 173796) | Quinoa ([FDC](#gloss-fdc) 168917) |
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

Amounts are in grams. Note that [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr) are scored as *pairs* in the [DIAAS](#gloss-diaas) methodology (see Step 3).

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

Raw amino acid values from [USDA](#gloss-usda) are not all absorbed. The [DIAAS](#gloss-diaas) methodology requires multiplying each food's IAA amounts by that food's *true [ileal digestibility](#gloss-ileal-digestibility) coefficient* — a value between 0 and 1 representing the fraction of each IAA that actually reaches the bloodstream.

[NuMa](#gloss-numa)'s digestibility values come from the [FAO](#gloss-fao) 2013 report and published literature. For these two foods:

| Food | [Digestibility coefficient](#gloss-digestibility-coefficient) | Source |
|------|:------------------------:|--------|
| Pinto beans | **0.80** | [FAO](#gloss-fao) Food and Nutrition Paper 92 (2013) |
| Quinoa | **0.85** | Mathai et al. (2017), *British Journal of Nutrition* |

To apply: multiply each food's IAA total by its coefficient. For example, for pinto beans' leucine: 0.664 × 0.80 = 0.531 g digestible leucine.

**Table I-5. Digestible IAA amounts per food (g)**

| Amino acid | Pinto × 0.80 | Quinoa × 0.85 | Pooled digestible |
|------------|-------------:|--------------:|------------------:|
| Histidine | 0.232 × 0.80 = **0.18560** | 0.127 × 0.85 = **0.10795** | **0.29355** |
| Isoleucine | 0.368 × 0.80 = **0.29440** | 0.157 × 0.85 = **0.13345** | **0.42785** |
| Leucine | 0.664 × 0.80 = **0.53120** | 0.261 × 0.85 = **0.22185** | **0.75305** |
| Lysine | 0.571 × 0.80 = **0.45680** | 0.239 × 0.85 = **0.20315** | **0.65995** |
| [Met+Cys](#gloss-met-cys) | 0.216 × 0.80 = **0.17280** | 0.159 × 0.85 = **0.13515** | **0.30795** |
| [Phe+Tyr](#gloss-phe-tyr) | 0.684 × 0.80 = **0.54720** | 0.268 × 0.85 = **0.22780** | **0.77500** |
| Threonine | 0.350 × 0.80 = **0.28000** | 0.131 × 0.85 = **0.11135** | **0.39135** |
| Tryptophan | 0.098 × 0.80 = **0.07840** | 0.052 × 0.85 = **0.04420** | **0.12260** |
| Valine | 0.435 × 0.80 = **0.34800** | 0.185 × 0.85 = **0.15725** | **0.50525** |

---

#### Step 4 — The FAO reference amounts for this meal

The [DIAAS](#gloss-diaas) method scores each pooled digestible IAA against how much of that IAA a *reference protein* of equal weight would provide. The reference values, from [FAO](#gloss-fao) Food and Nutrition Paper 92 (2013), Table 6, are expressed in **mg of IAA per gram of total protein** for older children, adolescents, and adults.

The full table is in Appendix E of this manual. The relevant values are:

| IAA | [FAO](#gloss-fao) reference (mg/g protein) |
|-----|-----------------------------:|
| Histidine | 16.0 |
| Isoleucine | 30.0 |
| Leucine | 61.0 |
| Lysine | 48.0 |
| [Met+Cys](#gloss-met-cys) | 23.0 |
| [Phe+Tyr](#gloss-phe-tyr) | 41.0 |
| Threonine | 25.0 |
| Tryptophan | 6.6 |
| Valine | 40.0 |

The meal contains **13.41 g total protein** (9.01 + 4.40). To find how many grams of each IAA the reference protein provides for this amount of protein, multiply:

    Reference amount (g) = FAO value (mg/g) × 13.41 (g protein) ÷ 1000

**Table I-6. [FAO](#gloss-fao) reference IAA amounts for 13.41 g protein**

| IAA | [FAO](#gloss-fao) (mg/g) | Calculation | Reference (g) |
|-----|----------:|-------------|-------------:|
| Histidine | 16.0 | 16.0 × 13.41 ÷ 1000 | 0.21456 |
| Isoleucine | 30.0 | 30.0 × 13.41 ÷ 1000 | 0.40230 |
| Leucine | 61.0 | 61.0 × 13.41 ÷ 1000 | 0.81801 |
| Lysine | 48.0 | 48.0 × 13.41 ÷ 1000 | 0.64368 |
| [Met+Cys](#gloss-met-cys) | 23.0 | 23.0 × 13.41 ÷ 1000 | 0.30843 |
| [Phe+Tyr](#gloss-phe-tyr) | 41.0 | 41.0 × 13.41 ÷ 1000 | 0.54981 |
| Threonine | 25.0 | 25.0 × 13.41 ÷ 1000 | 0.33525 |
| Tryptophan | 6.6 | 6.6 × 13.41 ÷ 1000 | 0.08851 |
| Valine | 40.0 | 40.0 × 13.41 ÷ 1000 | 0.53640 |

---

#### Step 5 — IAA ratios and the composite DIAAS score

For each IAA, divide the pooled digestible amount (from Table I-5) by the reference amount (from Table I-6). The result is a ratio: a value ≥ 1.0 means the meal meets or exceeds the reference for that IAA; below 1.0 means it falls short.

    Ratio = pooled digestible IAA (g) ÷ FAO reference IAA (g)

**Table I-7. IAA ratios vs. [FAO](#gloss-fao) reference**

| IAA | Pooled dig. (g) | Reference (g) | Ratio | Meets reference? |
|-----|----------------:|--------------:|------:|:----------------:|
| Histidine | 0.29355 | 0.21456 | 1.368 | Yes |
| Isoleucine | 0.42785 | 0.40230 | 1.063 | Yes |
| **Leucine** | **0.75305** | **0.81801** | **0.921** | **No — limiting** |
| Lysine | 0.65995 | 0.64368 | 1.025 | Yes |
| [Met+Cys](#gloss-met-cys) | 0.30795 | 0.30843 | 0.998 | Marginal (99.8%) |
| [Phe+Tyr](#gloss-phe-tyr) | 0.77500 | 0.54981 | 1.410 | Yes |
| Threonine | 0.39135 | 0.33525 | 1.167 | Yes |
| Tryptophan | 0.12260 | 0.08851 | 1.385 | Yes |
| Valine | 0.50525 | 0.53640 | 0.942 | No |

The **composite [DIAAS](#gloss-diaas) score is the lowest ratio** — the *limiting* amino acid determines the ceiling for all the others, because when one IAA runs out, the others cannot be used for protein synthesis.

    Composite DIAAS = the lowest ratio above = 0.921   (limited by Leucine)

A [DIAAS](#gloss-diaas) of 0.921 means this meal delivers about 92% of the protein quality of a reference protein. It also means the **digestible [complete protein](#gloss-complete-protein)** for this 200 g meal is:

    DCP = 13.41 g × 0.921 = 12.35 g

(If the DIAAS score were above 1.0, it would be capped at 1.0 for this calculation, since a food's digestible complete protein can never exceed its total protein.)

---

#### Step 6 — Interpreting the result

A composite [DIAAS](#gloss-diaas) ≥ 1.0 means the meal's protein is fully complete relative to the [FAO](#gloss-fao) reference. Values below 1.0 indicate partial completeness — the lower the value, the more the [limiting amino acid](#gloss-limiting-amino-acid) constrains usable protein.

For this meal:

- **Leucine** is the limiting IAA at 0.921. This is not surprising: leucine is the most abundant IAA in animal proteins, but plant proteins generally provide less of it relative to total protein.
- **Valine** is also below reference at 0.942. The combination of one legume and one pseudo-cereal improves but does not fully resolve either gap.
- **Lysine**, which is the classic weak point of grains, is met here (1.025) — the pinto beans contribute the lysine that quinoa alone would not cover.
- **[Met+Cys](#gloss-met-cys)** is nearly exactly met at 0.998 — essentially at the reference.

The [DCP](#gloss-dcp) of 12.35 g from 13.41 g of raw protein means that roughly 1.06 g of protein per meal is rendered non-contributory by the leucine shortfall. In practical terms, this is a high-quality plant-protein meal — [DIAAS](#gloss-diaas) above 0.9 is considered "good quality" by the [FAO](#gloss-fao).

---

#### Step 7 — Reproduce this in NuMa and compare

To run the same analysis in [NuMa](#gloss-numa):

1. From the main menu, select **Meals & Log**.
2. Create a new meal and add two foods:
   - Search for **pinto beans cooked** → select [FDC](#gloss-fdc) 173796
     ("Beans, pinto, mature seeds, cooked, boiled, with salt")
   - Enter a portion of **100 g**
   - Add a second food: search for **quinoa cooked** → select [FDC](#gloss-fdc) 168917
     ("Quinoa, cooked")
   - Enter a portion of **100 g**
3. Save the meal, then open it and select **View nutrition analysis**.
4. In the analysis screen, scroll to the **Protein quality** section.

[NuMa](#gloss-numa) will display:
- Total protein
- Composite [DIAAS](#gloss-diaas) score
- Digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp))
- A per-IAA ratio table identifying the [limiting amino acid](#gloss-limiting-amino-acid)

Compare the values [NuMa](#gloss-numa) shows with those in Table I-7 above. They should match to at least three significant figures. If they do not, please report the discrepancy at the project issue tracker.

---

### L. Notes

[^1]: Lippman, D., Stump, M., Veazey, E., Guimarães, S. T., Rosenfeld, R., Kelly, J. H., Ornish, D., & Katz, D. L. (2024). Foundations of Lifestyle Medicine and its Evolution. *Mayo Clinic Proceedings: Innovations, Quality & Outcomes, 8(1)*, 97–111. https://doi.org/10.1016/j.mayocpiqo.2023.11.004

[^2]: U.S. Department of Agriculture, Agricultural Research Service. (2019). *FoodData Central*. https://fdc.nal.usda.gov/

[^3]: Open Food Facts contributors. (2012). *Open Food Facts*. https://world.openfoodfacts.org/

[^4]: Institute of Medicine (US) Panel on Micronutrients. (2001). *Dietary Reference Intakes for Vitamin A, Vitamin K, Arsenic, Boron, Chromium, Copper, Iodine, Iron, Manganese, Molybdenum, Nickel, Silicon, Vanadium, and Zinc*. National Academies Press. https://doi.org/10.17226/10026 — the underlying Dietary Reference Intake report establishing that non-heme iron and phytate-inhibited zinc from plant foods are absorbed less efficiently than from mixed/omnivorous diets; the basis for the NIH fact-sheet figures below.

[^5]: National Institutes of Health, Office of Dietary Supplements. *Iron: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/ — states that because vegetarian diets contain no heme iron and their non-heme iron is less bioavailable, "the RDA for vegetarians is 1.8 times higher than for people who eat meat."

[^6]: National Institutes of Health, Office of Dietary Supplements. *Zinc: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/ — states that "the zinc requirements for vegetarians may be as much as 50% higher than for those who eat meat" because of the reduced bioavailability of zinc from plant-based diets.

[^7]: National Institutes of Health, Office of Dietary Supplements. *Vitamin B12: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/ — vitamin B12 occurs naturally only in animal foods. See also Melina, V., Craig, W., & Levin, S. (2016). Position of the Academy of Nutrition and Dietetics: Vegetarian Diets. *Journal of the Academy of Nutrition and Dietetics, 116*(12), 1970–1980. https://doi.org/10.1016/j.jand.2016.09.025 — recommends that vegans obtain vitamin B12 routinely from fortified foods or a supplement, since no reliable unfortified plant source exists. Neither source specifies a "50% of RDA" cutoff for a single day's intake; that trigger is NuMa's own design choice (see main text).

[^8]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2008," *Diabetes Care* 31(12):2281–3. This is a Creative Commons–licensed table, and NuMa uses it to fill in glycemic index values for common foods automatically. (For technically skilled users: this is done by a helper program, `import_gi_seed.py`, included in NuMa's program folder. It only fills in a value when a food's name matches the table exactly; anything less certain is left for you to confirm by hand.)

[^9]: US National Institutes of Health. (2026, July 31). Office of Dietary Supplements—Nutrient Recommendations and Databases. https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

[^10]: NuMa's own curated table of amino-acid profiles for common protein-complement foods — beans, grains, seeds, and a few animal foods included for comparison (`_COMPLEMENT_TABLE` in `usda_nutrients.py`). 23 of the 25 entries cite a specific [USDA](#gloss-usda) FoodData Central SR Legacy record by FDC ID, sourced the same way as the rest of NuMa's nutrient data[^2]; the remaining two (nutritional yeast, pea protein powder) use published amino-acid-composition literature values because no matching USDA record exists for those specific products. NuMa always checks your own food cache for a real match to each entry's food name before falling back to these built-in figures — see [amino acid estimates in complement suggestions](#comp-estimate).

