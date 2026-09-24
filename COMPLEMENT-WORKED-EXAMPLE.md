# Complement suggestions, worked through by hand

*One complete case, calculator-checkable at every step. Written 2026-09-24, after the
digestibility-basis fix. Companion document: `COMPLEMENT-LOGIC.md`, which explains the
reasoning these numbers implement.*

**The case:** 100 g of cooked lentils, using the built-in reference profile so the
numbers are reproducible on any machine.

Reproduce the whole thing with:

```bash
python3 scripts/complement_worksheet.py --curated "Lentils"
```

The worksheet prints four blocks. Blocks 1–3 are the arithmetic below, laid out so you
can redo any line with a calculator. Block 4 is what the program actually returns.
**Where blocks 3 and 4 disagree, something is being rejected by a rule rather than by
the arithmetic** — that comparison is the whole point of the tool, and it's how the
2026-09-24 bug was found.

---

## The inputs

Cooked lentils, per 100 g:

| | |
|---|---|
| Protein (P) | 9.02 g |
| Methionine | 0.077 g |
| Cystine | 0.089 g |
| Digestibility (d) | **0.83** — true ileal digestibility, FAO FNP 92 (2013) |

That 0.83 is the figure the app itself looks up. It is **not** lentils' DIAAS score of
0.75; those are different quantities and mixing them up is exactly what went wrong
before this fix. See `COMPLEMENT-LOGIC.md` §9.

---

## Step 1 — score each essential amino acid

Formula: **(AA grams ÷ P) × 1000 ÷ reference × d**

Methionine, worked out in full (remember Met and Cys are summed — 0.077 + 0.089 = 0.166):

> 0.166 ÷ 9.02 = 0.018404 g of Met+Cys per g of protein
> × 1000 = **18.40 mg per g of protein**
> ÷ 23 (the reference) = 0.8001
> × 0.83 (digestibility) = **0.664**

All nine:

| Amino acid | AA (g) | mg/g protein | Reference | Score | |
|---|---|---|---|---|---|
| Tryptophan | 0.0770 | 8.54 | 6.6 | 1.0735 | |
| Threonine | 0.3550 | 39.36 | 25 | 1.3067 | |
| Isoleucine | 0.3740 | 41.46 | 30 | 1.1472 | |
| Leucine | 0.6360 | 70.51 | 61 | 0.9594 | |
| Lysine | 0.6240 | 69.18 | 48 | 1.1962 | |
| **Methionine + cystine** | **0.1660** | **18.40** | **23** | **0.6641** | ← **GAP** |
| Phenylalanine + tyrosine | 0.4500 | 49.89 | 41 | 1.0100 | |
| Valine | 0.4320 | 47.89 | 40 | 0.9938 | |
| Histidine | 0.2540 | 28.16 | 16 | 1.4608 | |

One score falls below the 0.95 threshold. **Methionine+cystine is the limiting amino
acid**, at 0.66 — which is the textbook result for lentils, so the machinery is
behaving.

Note how close valine (0.9938) and leucine (0.9594) come to the threshold. Nudge the
digestibility down and they'd both become gaps too; at d = 0.75 all four are gaps.
This is worth knowing: **the gap list is sensitive to the digestibility figure**, and
that figure is a table lookup, sometimes a category estimate rather than a measured
value.

---

## Step 2 — the target for methionine

> R = reference ÷ 1000 ÷ d = 23 ÷ 1000 ÷ 0.83 = **0.027711** g of Met+Cys per g of protein
>
> Required in the pool: R × P = 0.027711 × 9.02 = **0.24995 g**
> Actually present: **0.16600 g**
> **Short by 0.08395 g**

The division by 0.83 is what makes this a *raw* target: you need 0.24995 g of raw
Met+Cys so that the 83% which is actually absorbed meets the reference.

---

## Step 3 — how many grams of each candidate

> **X = (R·P − A) ÷ (a − R·q)**
>
> where a = candidate Met+Cys per gram, q = candidate protein per gram

### Brazil nuts, in full

Brazil nuts, per 100 g: methionine 1.008 g, cystine 0.342 g, protein 14.32 g.

> a = (1.008 + 0.342) ÷ 100 = **0.013500**
> q = 14.32 ÷ 100 = **0.143200**
> R·q = 0.027711 × 0.143200 = **0.003968**
> denominator = 0.013500 − 0.003968 = **0.009532**
> **X = 0.08395 ÷ 0.009532 = 8.81 g**

The program returns **9 g**. ✅

### All candidates

| Candidate | a | q | R·q | a − R·q | X (g) | Verdict |
|---|---|---|---|---|---|---|
| Lentils, cooked | 0.001660 | 0.090200 | 0.002500 | −0.000840 | — | ratio too low |
| Chickpeas, cooked | 0.001930 | 0.088600 | 0.002455 | −0.000525 | — | ratio too low |
| Black beans, cooked | 0.002280 | 0.088600 | 0.002455 | −0.000175 | — | ratio too low |
| Kidney beans, cooked | 0.002180 | 0.086700 | 0.002403 | −0.000223 | — | ratio too low |
| Tofu, firm | 0.001820 | 0.080800 | 0.002239 | −0.000419 | — | ratio too low |
| Tempeh | 0.004960 | 0.202900 | 0.005623 | −0.000663 | — | ratio too low |
| Edamame, cooked | 0.002980 | 0.119100 | 0.003300 | −0.000320 | — | ratio too low |
| Peas, green, cooked | 0.001190 | 0.053600 | 0.001485 | −0.000295 | — | ratio too low |
| Quinoa, cooked | 0.001350 | 0.044000 | 0.001219 | 0.000131 | 642.21 | over 300 g |
| Amaranth, cooked | 0.000990 | 0.038000 | 0.001053 | −0.000063 | — | ratio too low |
| Hemp seeds | 0.014400 | 0.315600 | 0.008746 | 0.005654 | **14.85** | ok |
| Sesame seeds | 0.008810 | 0.177300 | 0.004913 | 0.003897 | **21.54** | ok |
| Brazil nuts | 0.013500 | 0.143200 | 0.003968 | 0.009532 | **8.81** | ok |
| Pumpkin seeds | 0.008330 | 0.245400 | 0.006800 | 0.001530 | **54.88** | ok |
| Sunflower seeds | 0.007570 | 0.193300 | 0.005357 | 0.002213 | **37.93** | ok |
| Oats | 0.005280 | 0.131500 | 0.003644 | 0.001636 | **51.31** | ok |
| Nutritional yeast | 0.011000 | 0.520000 | 0.014410 | −0.003410 | — | ratio too low |
| Soy protein isolate | 0.019780 | 0.860400 | 0.023842 | −0.004062 | — | ratio too low |
| Pea protein powder | 0.015300 | 0.800000 | 0.022169 | −0.006869 | — | ratio too low |
| Egg, whole, cooked | 0.006840 | 0.125600 | 0.003480 | 0.003360 | **24.99** | ok |
| Cheese, cheddar | 0.007460 | 0.249000 | 0.006900 | 0.000560 | **149.91** | ok |
| Greek yogurt, plain | 0.002810 | 0.099500 | 0.002757 | 0.000053 | 1590.87 | over 300 g |
| Whey protein powder | 0.039200 | 0.780000 | 0.021614 | 0.017586 | **4.77** | ok |
| Chicken breast, cooked | 0.010620 | 0.310200 | 0.008596 | 0.002024 | **41.48** | ok |
| Salmon, cooked | 0.011000 | 0.254400 | 0.007050 | 0.003950 | **21.25** | ok |

### Reading the rejections

**"Ratio too low" is not a near miss — it's a mathematical impossibility.** Nutritional
yeast is the clearest case: it's 52% protein and strong in most amino acids, but its
Met+Cys per gram (0.011000) is *less* than the methionine demand its own protein creates
(0.014410). The denominator is negative. Every gram you add makes the methionine score
slightly worse, not better. No serving size fixes it. Same story for all the legumes
(which share lentils' methionine weakness — this is why bean-on-bean doesn't
complement) and both isolated plant protein powders.

**Greek yogurt shows why the 300 g ceiling has to exist.** Its denominator is
0.000053 — positive, so the formula happily solves, but it solves to 1591 g of yogurt.
Quinoa likewise: 642 g. These are real solutions to the equation and complete nonsense
as advice. The ceiling catches them.

---

## Step 4 — what the program returns

```
  Brazil nuts                 9 g   closes_primary=True  gaps_closed=1 remaining=0
  Sesame seeds               22 g   closes_primary=True  gaps_closed=1 remaining=0
  Egg, whole, cooked         25 g   closes_primary=True  gaps_closed=1 remaining=0
  Sunflower seeds            38 g   closes_primary=True  gaps_closed=1 remaining=0
  Oats                       51 g   closes_primary=True  gaps_closed=1 remaining=0
  Cheese, cheddar           150 g   closes_primary=True  gaps_closed=1 remaining=0
  Whey protein powder         5 g   closes_primary=True  gaps_closed=0 remaining=1
  Hemp seeds                 15 g   closes_primary=True  gaps_closed=0 remaining=1
  Salmon, cooked             21 g   closes_primary=True  gaps_closed=0 remaining=1
  Chicken breast, cooked     41 g   closes_primary=True  gaps_closed=0 remaining=1
  Pumpkin seeds              55 g   closes_primary=True  gaps_closed=0 remaining=1
```

**Every solvable candidate from step 3 appears, at the gram amount step 3 predicted,**
rounded to whole grams: 8.81→9, 21.54→22, 24.99→25, 37.93→38, 51.31→51, 149.91→150,
4.77→5, 14.85→15, 21.25→21, 41.48→41, 54.88→55.

The `remaining=1` entries are interesting: whey, hemp, salmon, chicken and pumpkin seeds
all close methionine, but the protein they add dilutes the pool enough to push leucine
(which was sitting at 0.9594) below the 0.95 line. That's the "gap cascade" described in
`COMPLEMENT-LOGIC.md` §7, visible in miniature.

---

## The bug this comparison exposed

**Before the 2026-09-24 fix, step 4 was missing four foods that step 3 solved cleanly:**
sesame (21.5 g), sunflower (37.9 g), oats (51.3 g) and pumpkin seeds (54.9 g). All well
under the 300 g ceiling. All genuinely closing the gap. All silently absent.

They were being killed by the "don't reduce digestible protein" guard, which weighted
the **base** by its true ileal digestibility (0.83) but the **complement** by its
**DIAAS score** — a different quantity that already has the food's own limiting-amino-acid
shortfall baked into it. Counting that shortfall a second time made ordinary plant foods
look like they'd drag the pool down:

| Food | DIAAS score | True digestibility | Pooled result using DIAAS (wrong) | Using TID (right) | Verdict before → after |
|---|---|---|---|---|---|
| Sesame seeds | 0.44 | 0.84 | 0.749 | **0.974** | rejected → offered at 22 g |
| Sunflower seeds | 0.53 | 0.84 | 0.771 | **0.955** | rejected → offered at 38 g |
| Oats | 0.57 | 0.82 | 0.806 | **0.978** | rejected → offered at 51 g |
| Pumpkin seeds | 0.64 | 0.85 | 0.798 | **0.903** | rejected → offered at 55 g |
| Brazil nuts | 0.54 | 0.78 | 0.842 | 0.968 | offered either way |

(The guard compares against the base's own 0.83. Everything in the "wrong" column falls
below it; everything in the "right" column clears it.)

The distortion was **systematic and one-directional**. Animal foods have DIAAS ≈ TID ≈ 1,
so they were unaffected and sailed through — which is why the pre-fix suggestion list for
lentils was egg, cheddar, salmon, chicken and whey, with the plant options pushed down
into the second tier. For anyone eating a legume-based diet, the suggestions were being
quietly filtered toward animal foods by an arithmetic slip.

numa also contradicted itself. The DIAAS-improver tier has always used true digestibility
correctly, so it was simultaneously reporting *"sesame seeds, 30 g, DIAAS 0.66 → 0.96"*
for the very food the gap-closer tier had just rejected as harmful.

Both tiers now use true ileal digestibility, looked up the same way for base and
complement alike. Pinned by
`tests/test_usda.py::TestComplementCandidateDigestibilityBasis`.

---

## Checking a food of your own

```bash
python3 scripts/complement_worksheet.py "quinoa"
```

It resolves the name against your own food cache, looks up the digestibility the way the
app does, and prints all four blocks. Read-only; it never writes to the database.

What to look for, in order:

1. **Step 1** — does the gap list match what you'd expect for that food? A grain showing
   a lysine gap and a legume showing a methionine gap is the sanity check.
2. **Step 2** — is the digestibility figure a real measurement or a category estimate?
   The worksheet says which. A category estimate moves every score in step 1.
3. **Step 3 vs step 4** — any food that solves in step 3 but is absent from step 4 is
   being removed by a rule, not by the arithmetic. The rules that can do that are the
   300 g ceiling, the still-gapped recheck, and the digestible-protein guard
   (`COMPLEMENT-LOGIC.md` §4). If none of them obviously applies, that's worth a look.
