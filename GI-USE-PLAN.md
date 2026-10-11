# Putting GI to use — implementation plan

Drafted 2026-10-10. All four groups agreed 2026-10-10: docs,
features, nudges, population caveat. Ties into WHATIF-PLAN.md Phase 5 wherever
both need the same piece; those links are marked **[WI-5]**.

**Status marks:** ✅ done (date) · ◐ partly done · ☐ not started.
**Plan complete 2026-10-10:** all 11 items and all 6 order steps done. Added 2026-10-10 on request: `#gi-impaired` manual
section, linked from every impaired-tolerance mark.

What already exists (don't rebuild): `numa_app/services/glycemic_load.py`
(food/recipe/meal/day GL, gaps, `gl_band()` serving vs day scale, day totals
and averages); GL on food, meal, recipe, day and summary pages; the GL nutrient
plot (`_GL_PLOT_KEY`); manual sections `#gi`, `#gi-populations`, `#gl`,
`#glycemic`, Appendix C `#appendix-gl-comparison`. Every GI value is one the
user supplied (`food_annotations`), with its population and source row.

## A. Docs and guidance

1. ✅ (2026-10-10) **Manual: "What you can do with GI and GL"** (`#gl-uses`), a short practical
   section after `#gl`: what to look at first (a meal's GL and its band), what
   to change (portion, swap, pairing), what GL can't tell you (individual
   response; fat/protein/acid blunting, already explained in `#gl`), and pointers
   to every feature below. Written in the existing voice of `#gl`.
2. ✅ (2026-10-10) **Worked example** in that section: one plausible meal, its GL and band; swap
   white rice for barley; show the drop. Numbers come from the bundled 2008 table
   so any user can reproduce them. Then show the same thing done in what-if
   (Replace, same grams), so the example teaches the tool too. **[WI-5]**
   *Built as: 200 g white rice (GI 75) vs pearled barley (GI 35), both ~28 g
   carbs/100 g: GL ~42 High -> ~20; then the same in What-if. In `#gl-uses`.*
3. ✅ (2026-10-10) **One-line help under every GL band**: what the band means for that scope,
   plus the caveat already in `gl_band_caveat()` for day totals, plus a link to
   `#gl-uses`. One shared partial (`_gl_band_note.html`), used everywhere a band
   is shown — grep every call site (see the AA-checkmark lesson).
   *Built as: `gl_band_help(scope)` macro in `_gl_result.html` (not a separate
   partial), called from `gl_figure()`, the food page and the trend page; the
   per-page caveat copies it replaced were removed.*

## B. Features that use data already there

4. ✅ (2026-10-10) **GL Top Contributors.** Add GL to the "Top Contributors" nutrient choices on
   meal and recipe pages. `top_contributors.rank_contributors()` ranks by a
   per-100 g key; GL isn't one, so add `rank_contributors_by_gl()` next to the
   existing `rank_contributors_by_dcp()` (same pattern), using
   `glycemic_load.food_gl()` per ingredient. Foods with no GI show as gaps, not 0.
5. ✅ (2026-10-10) **Lower-GL swap suggestions.** On a meal or recipe with a Medium/High GL: for
   the top one or two GL contributors (from 4), suggest cached foods with a GI
   on record that are a plausible like-for-like (same food group / name-token
   overlap; carbohydrate ≥ half the original's) and a lower GI. Each suggestion
   shows the GL after the swap and opens **what-if** pre-filled with that
   Replace edit (same grams), so the user can see every other nutrient's change
   before committing. Nothing writes. **[WI-5]** — what-if already does the
   before/after; this is only a pre-filled link into it.
   *Built as: new `gl_swaps.py`; GI ≥ 5 lower, carbs/100 g within 1.5×, shared
   name words first; links for this meal, last 30 days, or this recipe. Notes
   under the swaps say they come only from foods with a GI, linking to 10.*
6. ✅ (2026-10-10) **GL in Compare.** Add GI (food) and GL per 100 g / per serving rows to
   /compare, gaps shown as —. Uses `food_gl()` / `recipe_gl()`.
   *Built as: a "Glycemic comparison" table, per 100 g only (Compare is per
   100 g throughout); lowest complete GL highlighted; "≥" + coverage. Not in
   the CSV export yet.*
7. ✅ (2026-10-10) **Optional daily GL target in the profile.** Off by default. When set,
   day pages and Recent Days show day GL against it the way nutrients show
   against RDA (`rda_status()` colours, as a *limit*). Pinned per day like other
   profile values (`get_profile_for_date`). Default suggestion when switched on:
   the "Low" day ceiling, 80, editable. Manual says plainly it is a personal
   budget, not a clinical target (reuse `gl_band_caveat()` text).
   *Built as: `UserProfile.gl_day_target` (Settings -> 1; blank = off; no default
   filled in — the placeholder suggests 80); `glycemic_load.gl_target_status()`;
   shown on day pages, Recent Days (colour), trend (days over), What-if (days
   over before/after). An incomplete day is "over" only when its lower bound
   already is. Also fixed: Settings save now keeps the active profile's name.*
8. ✅ (2026-10-10) **GL trend made visible.** Recent Days gets a Day GL column (picker option via
   `meal_list_columns.py`); Nutrient Plot already supports GL — point to it from
   `#gl-uses` and from the day page's GL line.
   *Built as: a fixed Day GL column (not a picker choice — the picker is shared
   with Meals & Log), hidden when GI is opted out; links to the plot.*

## C. Nudges toward filling the data in

9. ✅ (2026-10-10) **GL coverage line.** Wherever GL is shown with gaps: "GL covers 72% of this
   meal's carbohydrate; 2 foods have no GI — add one" with each food linked to
   its Annotate page's GI lookup. Coverage = carbs from foods with GI ÷ all carbs
   (foods under `NEGLIGIBLE_CARBS_G` excluded, GI "not wanted" excluded).
   Computed in `glycemic_load._result()` so every caller gets it.
   *Built as: `coverage_pct` in every GL result; shown on every incomplete GL
   figure, in what-if, and under GL Top Contributors.*
10. ✅ (2026-10-10) **Foods → 9: "Foods you eat most that have no GI".** Folded-up list like the
    missing-AA list: foods used in meals/recipes/pantry, carbohydrate above the
    negligible line, no GI and not marked "don't prompt me"; most-used first;
    each linked to Annotate. Not a Home-page reminder (improvement, not error).
    *Built as: `data_quality.missing_gi_in_use()`, carbs ≥ 5 g/100 g, `#missing-gi`;
    "not needed" sets `gi_no_prompt`; hidden when GI is opted out in Settings.*

## D. Population caveat

11. ✅ (2026-10-10) **Say who a GI was measured in.** Where a food's GI shows (food page,
    Annotate, GL Top Contributors, swap suggestions), mark values measured only in
    people with impaired glucose tolerance/diabetes: "measured in people with
    diabetes — may read differently for you". Population is already stored per
    row. A meal/recipe GL that leans on such values says so in its coverage
    line (9). Profile has no diabetes field, so the note is neutral, not
    personalised; adding one is out of scope unless asked.
    *Built as: `glycemic_load.gi_measured_impaired()` on the saved `gi_source`
    label; notes on food and Annotate pages and under every GL figure (naming
    the foods); † in GL Top Contributors and swap suggestions.*

## Ties to what-if Phase 5 [WI-5]

- ✅ (2026-10-10) **GL before and after** (Phase 5's first item) is the base for 2 and 5: build
  it first. Meals: day GL total before/after and average day GL; recipes: GL
  per serving before/after. Use `gl_for_items()` with the same `rewrite` hook the
  nutrient expanders take, so no new expansion path.
  *Built instead with `gl_for_leaves()` on what-if's own already-edited leaf
  foods — same "no new expansion path" goal, simpler.*
- ✅ (2026-10-10) **Days over target** (Phase 5's "averages hide timing" point): when a daily
  GL target (7) is set, what-if shows days othat list, not against a portion's name.ver it before and after, same as
  days below target for nutrients.
- ✅ (2026-10-10) **Coverage in what-if** (9): a scenario that swaps in a food with no GI must
  say GL coverage dropped, or the "after" GL looks better than it is.
- ✅ (2026-10-10) **Speed**: GL per day adds one pass; include it in Phase 5's 90-day speed check.
  *Measured on a copy of the real DB: 90 days, 87 meals — 0.74 s total, GL cell
  0.04 s. No per-request cache needed.*

## Suggested order

1. ✅ WI-5 GL before/after + coverage (9) in `glycemic_load` — the shared base.
2. ✅ GL Top Contributors (4), then swap suggestions (5) linking into what-if.
3. ✅ Population marks (11) and Foods → 9 list (10).
4. ✅ Compare rows (6), Recent Days column (8), band help partial (3).
5. ✅ Daily GL target (7) + days-over-target in what-if.
6. ✅ Manual `#gl-uses` + worked example (1, 2) — written 2026-10-10 ahead of
   step 5, since the band help links to it; step 5 added the daily GL target
   to it.

## Each step ends with

`Docs:` line in new modules, README Architecture entry + Test Suite row,
manual section + Part 11 entry, then the `bump_version.py` run.
