# NutriMagnus User Manual
*Version 2026-04-28:0720*

---

## Special Note

NutriMagnus displays a help footer at the bottom of tables and analysis
output whenever additional context is available. It looks like this:

> At any prompt, type `?diaas` or `?dcp` for help with these columns.

Type the indicated command at the next prompt and the relevant section of
this manual will be displayed inline. You can also type `?help` at any
prompt to see the full list of available topics.

---

## Using the ? Help System [help]

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

Type ?help at any time to show this list again.

---

## Essential Amino Acids [aa]

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

---

## Protein Complement Suggestions [comp]

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

---

## Protein Completeness [complete]

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

---

## Digestible Complete Protein (DCP) [dcp]

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

---

## DIAAS — Digestible Indispensable Amino Acid Score [diaas]

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

---

## Dietary Preferences [diet]

This setting controls which protein sources appear in complement suggestions.
Change it under **Settings → Dietary preferences** (option 3 in the Settings menu).

| Option | Setting | Includes |
|---|---|---|
| 1 | All animal foods | meat, fish, dairy, and eggs |
| 2 | Vegetarian | dairy and eggs only (no meat or fish) |
| 3 | Plant-based only | plant sources only |

The setting is saved between sessions and applies to both the interactive
complement display and any exported reports.

---

## FAO 2013 Reference Standard [fao]

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

---

## Amino Acid Gaps [gap]

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

---

## Glycemic Index [gi]

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

---

## Glycemic Load [gl]

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

---

## Recommended Dietary Allowances [rda]

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

---

## Appendix A: GL and Blood Glucose Comparison

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