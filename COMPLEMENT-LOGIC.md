# How numa chooses complement foods

*Plain-English description of the complement-suggestion logic. Written 2026-09-24,
reflecting the digestibility-basis fix made the same day. Companion document:
`COMPLEMENT-WORKED-EXAMPLE.md`, which works one case through with a calculator.*

*Code, if you want to follow along: the scoring and selection live in
`usda_nutrients.py` (`get_aa_gaps`, `_score_one_complement`, `suggest_complements`),
the display assembly in `numa_app/services/complements.py`.*

---

## 1. The yardstick: what "a gap" means

Every food's protein is judged by **amino acid concentration per gram of protein**,
not per gram of food. A food with very little protein isn't penalised for that here —
only for the *balance* of the protein it does have.

For each of the 9 essential amino acids there is an FAO 2013 reference figure, in
milligrams per gram of protein:

| Amino acid | Reference (mg/g protein) |
|---|---|
| Tryptophan | 6.6 |
| Threonine | 25 |
| Isoleucine | 30 |
| Leucine | 61 |
| Lysine | 48 |
| Methionine **+ cystine** | 23 |
| Phenylalanine **+ tyrosine** | 41 |
| Valine | 40 |
| Histidine | 16 |

For each amino acid:

> **score = (mg of that AA per g of the food's protein ÷ its reference) × digestibility**

- A score of 1.0 means the food exactly meets the reference. Above 1.0 is surplus.
- Methionine is always scored as **Met + Cys summed**; phenylalanine as **Phe + Tyr
  summed**. That is the FAO convention — the body can make cystine from methionine and
  tyrosine from phenylalanine, so they're treated as pairs. Cystine and tyrosine are
  never scored on their own; they exist only as helpers to those two.
- `digestibility` is the base item's **true ileal digestibility** — the fraction of its
  protein actually absorbed. It comes from the same curated table the meal-level DIAAS
  calculation uses (cooked lentils: 0.83). It is emphatically **not** the food's DIAAS
  score, which is a different quantity; see section 9.

**An amino acid counts as "a gap" when its score falls below 0.95.** Not 1.0 — that
0.05 margin exists so a score of 0.994 doesn't generate an absurd "add 1 g of lentils"
suggestion. Gaps are then sorted lowest-score-first, and the lowest of them is the
**primary gap**, which is the classic "limiting amino acid".

If nothing scores below 0.95, there are no suggestions at all. The screen says so and
stops.

## 2. The candidate pool: what foods numa is allowed to suggest

Three sources, in priority order:

1. **Your pantry** (and, in recipe and meal contexts, your recipes) — real foods with
   real cached nutrient data.
2. **Your wider food cache.** For each name in an internal curated table of ~25 common
   protein foods (lentils, tempeh, pumpkin seeds, nutritional yeast, whey, egg…), numa
   searches your own cache for a real food matching that name. If it finds one, your
   real food is used in place of the generic reference profile.
3. **The curated table itself** — generic literature profiles from USDA Foundation /
   SR Legacy data, used only when neither of the above supplied something for that slot.

Before any scoring happens, these filters apply:

- Your **diet preference** (plant-only / vegetarian / all) drops animal entries.
- Anything you've flagged **"ignore"** in the UI is dropped.
- Anything already offered from the pantry tier isn't repeated in the general tier,
  including when the same underlying cached food appears under two display names.

A candidate that has real macronutrients but **no amino acid panel of its own** is not
thrown away. Its AA profile is borrowed from whichever curated entry its name matches
and rescaled to its own protein content. Those suggestions are labelled "estimated" in
the display. This is separate from — and never overwrites — the "estimate amino acids
from another food" tool, which lets you choose the source food yourself and saves the
result permanently.

## 3. The core calculation: how many grams?

For one candidate food against one target amino acid, numa solves a single equation.
In words: *how much of this food must I add so the combined pool's score for that
amino acid lands exactly on 1.0?*

Let:

| Symbol | Meaning |
|---|---|
| **P** | base protein, g |
| **A** | base amount of the target amino acid, g (pair-summed) |
| **q** | candidate protein per gram of candidate (its protein per 100 g ÷ 100) |
| **a** | candidate target AA per gram of candidate (pair-summed, ÷ 100) |
| **R** | reference mg ÷ 1000 ÷ digestibility — the required grams of that AA per gram of protein |

Then:

> ### X = (R·P − A) ÷ (a − R·q)

The **numerator** is how short you are, in absolute grams of that amino acid.

The **denominator** is the crux. It's how much *surplus* of that amino acid each gram
of the candidate brings, **net of the extra protein that same gram adds to the pool**.
Every gram of a candidate does two things at once: it contributes the amino acid, and
it raises the protein total against which the amino acid is measured. If
`a ≤ R·q` — the candidate's own AA-to-protein ratio doesn't beat the reference — the
denominator is zero or negative and **no amount of that food will ever close the gap.**

That is why piling on more of a lysine-poor food never fixes a lysine gap. It's not a
quirk of the program; it's arithmetic. Nutritional yeast against a methionine gap is
the standard example: it's protein-dense and strong in most amino acids, but its
Met+Cys ratio sits just below the reference, so its denominator comes out negative and
it is correctly refused.

Note the **÷ digestibility** inside R. A poorly-digested base needs proportionally
*more* raw amino acid in the pool so that the absorbed share still hits the reference.

Each candidate is tried against the primary gap first, then the second-worst, and so
on. The first amino acid it can actually close is the one it's credited with.

## 4. What gets rejected

A solved amount is discarded if any of these hold:

- **X ≤ 0** — there's nothing left to close for that amino acid.
- **X > 300 g** — mathematically valid but not a serving any human eats. This is what
  stops "392 g of protein powder" appearing. Candidates whose ratio only marginally
  beats the reference race toward the formula's asymptote and land here.
- After adding X, the **target amino acid is still gapped** — a belt-and-braces
  recheck of the fully recomputed pool.
- The addition would **lower the pool's total digestible protein**: the projected
  pooled DIAAS of base + complement comes out below the base's own digestibility.
  (Applied only when real digestibility data exists; skipped when digestibility is the
  1.0 default used for whole-meal and whole-day contexts.)

That last projection is computed properly: base amino acids weighted by the base's
digestibility, complement amino acids weighted by the **complement's own true ileal
digestibility**, then the minimum ratio across all amino acids. Same method the
meal-level DIAAS engine uses. **This is the part that was wrong until 2026-09-24** —
see section 9.

## 5. Ranking of gap-closers

Internally, sorted by:

1. Does it close the **primary** (most limiting) amino acid? — yes first.
2. **Number of gaps closed**, most first.
3. **Smallest serving in grams.**

So "fixes the limiting amino acid" beats "tidies up three minor ones", and among equals
the smaller serving wins. The web display then re-sorts this list according to your
chosen sort mode (greatest resulting digestible complete protein by default; also most
digestible protein added, biggest gap effect, or smallest serving), and always promotes
a suggestion that completes the whole profile to the top of its tier.

## 6. The second tier: DIAAS improvers

Any candidate that can't close *any* gap by the formula above gets a second hearing
under a different question: **"can practical servings of this still raise the pooled
DIAAS meaningfully?"**

This one is brute force, not algebra. Pooled DIAAS is evaluated at fixed step sizes —
15/30/60/120 g in food, meal and daily contexts, 30/60/100/150/200/300 g for recipes —
keeping the steps that improve on the base without regressing. If the best step doesn't
beat the base by **at least 0.03 DIAAS**, the candidate is dropped entirely. If the base
already scores **0.90 or better**, nothing is offered at all: it's considered good
enough to leave alone.

This tier exists precisely for foods the analytical formula can't pick but which still
help. Ranked by best resulting DIAAS, then smallest serving.

## 7. Pairs (the "gap cascade")

Sometimes food A closes the limiting gap, but the protein it brings **opens a new gap**
elsewhere — you've fixed methionine and broken lysine. The pairs logic exists for
exactly that case:

- Take every candidate A that closes the primary gap **and opens a new one**. (If A
  alone completes the profile it's skipped here — it's already a strong single
  suggestion and pairing adds nothing.)
- Recompute the pool after adding A; find its new worst gap.
- Try every other candidate B against that new gap. **B is accepted only if it closes
  everything remaining and opens nothing new.**
- Reject the pair if A + B together exceed 600 g.

Each unordered pair is tested once. Sorted by total grams, with a jump to the top for
pairs that close everything in 50 g or less combined.

## 8. The two-step combo

This is the one shown most prominently in the web display.

**Step 1** is the chosen gap-closer. The pool that results from adding it is then run
through the *entire* suggestion machinery again from scratch, and **Step 2** is the
best DIAAS-improver for that new pool — offered only if it beats the Step-1 pool's own
digestibility.

Where a real ingredient breakdown exists (a recipe, a logged meal), the resulting
digestible-protein figure is not interpolated: the actual meal-level DIAAS engine is
re-run over the real ingredients plus the hypothetical addition. Where no breakdown
exists — a single food — a linear approximation is used instead, which is exact enough
because a single food's digestibility is a flat figure rather than a pooled one.

## 9. The digestibility-basis fix (2026-09-24)

Worth recording, because it silently distorted results and because the distinction it
turns on is easy to lose.

**Two different numbers were being conflated:**

- **True ileal digestibility (TID)** — the fraction of a food's protein actually
  absorbed. Sesame seeds: **0.84**. An ordinary, unremarkable figure.
- **DIAAS score** — digestibility *multiplied by* the food's own limiting amino acid
  ratio. Sesame seeds: **0.44**, because sesame is severely lysine-poor.

The reduction guard in section 4 weighted the **base** by TID but the **complement** by
its **DIAAS score**. Using DIAAS as if it were a digestibility double-counts the
complement's own limiting-AA shortfall — and it's the wrong shortfall, because what
matters when you combine two foods is whether the *pool* is balanced, not whether each
food was balanced on its own. That is the entire point of complementary proteins.

The effect was systematic and one-directional: **plant complements were suppressed.**
Low-DIAAS plant foods were penalised twice and failed the guard; animal foods, where
DIAAS ≈ TID ≈ 1, sailed through unaffected. So a lentil base was offered egg, cheddar,
salmon, chicken and whey, while sesame, sunflower, oats and pumpkin seeds — all of
which close the gap in a perfectly reasonable serving — were pushed down into the
DIAAS-improver tier.

numa then contradicted itself one tier down, because the improver tier has always used
TID correctly. The same food, against the same base, was simultaneously *"would reduce
your digestible protein, suppress it"* and *"30 g raises your DIAAS from 0.66 to 0.96,
recommend it."*

**The fix:** weight the complement by its true ileal digestibility, looked up the same
way the base's is, in both the single-food and the pair paths. Both tiers now agree.
Regression tests pin the new behaviour in
`tests/test_usda.py::TestComplementCandidateDigestibilityBasis`.

`COMPLEMENT-WORKED-EXAMPLE.md` shows the before/after numbers for a lentil base.

## 10. Two smaller things worth knowing

- **0.95 versus 1.0.** A gap is considered closed at 0.95, but a profile is only
  formally "complete" at 1.0. There is therefore a narrow band where numa can truthfully
  report no remaining gaps while the profile isn't technically complete. Intentional,
  but it reads like a bug when you check it by hand, so: it isn't one.
- **The curated Oats entry has no tyrosine value.** Its Phe+Tyr score is therefore
  computed from phenylalanine alone and is understated. It still clears 0.95 comfortably,
  so nothing breaks today, but a more accurate tyrosine figure would raise it.

## 11. Checking it yourself

`scripts/complement_worksheet.py` prints every intermediate number for any base food —
the per-amino-acid scores, the gap list, the target, and the solved grams for every
candidate — alongside what the program actually returns, so the two can be compared
line by line. It is read-only and never touches the database.

```bash
python3 scripts/complement_worksheet.py "lentil"             # first cache match
python3 scripts/complement_worksheet.py --curated "Lentils"  # the built-in reference entry
python3 scripts/complement_worksheet.py "lentil" 0.90        # force a digestibility
```
