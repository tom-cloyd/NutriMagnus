# What-if analysis — implementation plan

Drafted 2026-10-04. Phases 1-3 built 2026-10-06; Phases 4-5 not started. Non-destructive "what if I removed / added /
replaced / scaled X" analysis across a chosen set of meals (by date ranges,
dates, or meal IDs) or a chosen set of recipes, showing nutrient profiles
before and after.

## Critique summary (why the plan looks the way it does)

- **Builds on Food Use.** Food use in meals / in recipes already turn a selection
  into a set of meals or recipes (`_resolve_meals_for_food_use`,
  `_parse_food_use_recipes_selection` in web/backend.py), already read typed codes
  (`parse_code`) and already have a substitute action. That substitute is
  destructive; what-if is the same idea with no writes. The Food Use tables
  already list every code with frequency, so they're the place to pick items
  ("Use in what-if" button per row).
- **Polyphenols aren't tracked.** `NUTRIENT_MAP` has isoflavones and carotenoids
  only. Adding polyphenol data is a separate project (the USDA flavonoid
  database is separate from FoodData Central).
- **Set of dates = one-day ranges.** Let a bare date line (`2026-09-03`) count as
  a one-day range in the existing ranges box. No new mode needed.
- **Operations need precise scope:** remove, add (amount + basis), replace
  (same grams / same servings / stated amount), scale. Remove and replace apply at
  every depth (a recipe nested in a recipe). "Add" applies only to days
  you logged, matching `average_from_daily_totals`, so "didn't log" never
  gets mixed up with "ate this".
- **Averages hide timing.** A supplement taken 3 days a week can average fine
  while 4 days a week fall short. Show days below target before and after (Phase 5).
- **Flag status changes both ways:** below target ↔ adequate ↔ over limit (adding
  supplements can push past an upper limit).
- **Targets come from each day's pinned profile** (`get_profile_for_date`), not today's.
- **Must never write.** Meals store nutrient snapshots (`meal_set_bcp`); recipe
  edits trigger DCP recompute. Test: DB file is byte-identical before and after a run.
- **No sixth copy of the expansion logic.** Pass edits into the existing expanders
  as an optional argument that changes nothing when absent.
- **Recipe layout:** one column per recipe, cells show "after (Δ)" with a toggle to show
  the before value; hide nutrients that didn't change; cap at 8 (matches Compare);
  per serving.

## Decisions (settled 2026-10-06)

- Remove/replace apply at every depth: yes
- "Add" basis is per logged day: yes (per meal / chosen days later — see Later)
- Recipe results per serving: yes
- Polyphenols out of scope for now — but they WILL be tracked soon, so nothing
  in what-if may hard-code the nutrient list (see Phase 1, "generic rows")
- A scenario is a list of edits: any mix of remove / add / replace / scale, so
  substitution can be done either as one replace (lands only where the old item
  was) or as remove + add (add lands on every logged day). Both are kept.

## Phase 1 — core service: `numa_app/services/whatif.py`

**Status: done 2026-10-06** (meals part; `evaluate_recipes` moves to Phase 3).
As built, differing from the draft below:
- Edit fields are `op, item, replacement, amount, unit ("g"|"servings"), basis
  ("grams"|"servings"|"stated")`. Amount text is parsed in web/backend.py
  (`_parse_whatif_amount`, using the meal page's `_parse_portion_str` for foods),
  so the service only sees numbers.
- The expansion hook is a `rewrite(kind, id, qty) -> [(kind, id, qty)]` callable
  on `expand_recipe_ingredients` / `recipe_total_nutrients`, not an `edits` list,
  so recipe_nutrients stays ignorant of what-if.
- `_meal_expand_for_diaas` was NOT moved: it also builds the meal page's display
  rows. The service has its own small `meal_nutrients()`; a test holds the two
  totals equal for every meal.
- Several scale edits on one item multiply; then the first remove/replace wins.

- `Edit(op: remove|add|replace|scale, target: (kind, id), new: (kind, id) | None,
  amount, unit, basis)`; a scenario is a list of edits. Amounts are parsed with the
  existing `_parse_portion_input` so that "2 oz" works.
- Optional `edits` argument on `recipe_nutrients.expand_recipe_ingredients` /
  `recipe_total_nutrients`, applied to each ingredient row at every level.
- Move the nutrient-summing core of `_meal_expand_for_diaas` into the service so
  it can take `edits`; the backend wrapper calls it.
- `evaluate_meals(meal_ids, edits)` → daily totals before and after, averages,
  per-day targets, status changes.
- `evaluate_recipes(recipe_ids, edits)` → per-serving before/after per recipe.
- Additions folded in 2026-10-06:
  - **Unknown, not zero:** an added/replacement item with no value for a
    nutrient (food: key absent; recipe: absent from a leaf that is >=10% of
    its weight) marks that nutrient's "after" as possibly understated.
  - **Generic rows:** result rows come from the display groups plus an
    "Other" group for any non-AA key present, so new nutrients (polyphenols)
    appear without what-if changes.
  - **Recipes added by grams or servings** (grams converted via
    recipe_serving_grams).
  - **Per-edit report:** how many meals/days each edit actually touched, so
    an edit that matched nothing is visible.
  - Replacement recipe that contains the replaced item is refused (would loop).
  - Read-only profile lookup (no day-profile pinning), so the no-write test holds.
- Tests: existing suite still green (no behavior change without edits); one test per
  operation, incl. nested removal and add-on-logged-days-only; byte-identical-DB check.

## Phase 2 — Analysis → What-if: meals

**Status: done 2026-10-06.** `/analysis/whatif`, `analysis_whatif.html`, Analysis
menu item 4, "try removing" link per row on Food use in meals (opens a remove
row; switch it to Replace on the page). Bare-date lines work on both Food Use
pages too. Up to 12 change rows. Manual: `#whatif`; Part 11 entry October 6.
Tests: tests/test_whatif.py (service) + 5 in tests/test_web.py.

- Inputs: Food Use's selection box (ranges, bare dates, or meal IDs) + an edit list
  (operation, code, amount, basis) with add/remove buttons per row.
- Settings live in the URL so a scenario can be bookmarked.
- Output: full nutrient table — before avg / after avg / Δ / Δ% / % target
  before → after, with status changes highlighted; sorted by largest change;
  unchanged rows hidden behind a toggle. Header line: days and meals covered,
  IDs not found.
- "Use in what-if" button on each Food use in meals row.
- Folded in 2026-10-06: calories + macros summary at the top; days target not
  met / days over max limit, before and after (moved up from Phase 5).

## Phase 3 — Analysis → What-if: recipes

**Status: done 2026-10-06.** `/analysis/whatif-recipes`, `evaluate_recipes()`.
As built: "add" goes into each batch (per serving = amount / servings);
columns = recipes a remove/replace/scale reached, top 8 by summed relative
change, the rest listed by name; DCP row under protein via the new pure
`recipe_dcp.recipe_dcp_per_serving()`; parents listed with a "Show them too"
link; cells show after + change, with a tick-box to show before. Change-row
editor shared in `_whatif_changes.html`.
Added later 2026-10-06 after review: Add per serving or per whole recipe
(`Edit.per`); Average change column (mean of per-recipe % change over all
reached recipes, recipes with a zero "before" left out); full-width layout.
Both pages: Replace basis "factor" (a multiple of the old weight, 1.1 or
110%); arrow keys in the name lists; clearer action labels.

**Next session (2026-10-07):** user to finish checking Phases 1-3, then Phase 4.

- Selection like Food use in recipes (all / created-date range / IDs); same edit list.
- Output: the after (Δ) grid, cap 8; option to also list parent recipes the
  change flows into.
- "Use in what-if" button on each Food use in recipes row.

## Phase 4 — bridges

- "Apply this for real": a scenario made only of replace edits hands off to the
  existing destructive substitute, with a confirmation step.
- Saved named scenarios (follow the `/compare/save` pattern).
- CSV export.

## Phase 5 — deeper analysis

- GL before and after (DCP done 2026-10-06 in the summary table: ~0.4 s for 118 days;
  fast enough that it did not need to be opt-in). 
- Speed check on a 90-day range; cache recipe totals for the length of one request.

## Later (agreed 2026-10-06, after the first working version)

- Limit an "add" to some days (weekdays, chosen dates) or per meal.
- Compare two scenarios side by side against the current data.

## Each phase ends with

`Docs:` line in new modules, README Architecture entry + Test Suite row,
manual section + Part 11 entry, then the `bump_version.py` run.

Recommended first chunk: Phases 1 + 2 together (answers the multivitamin question).
