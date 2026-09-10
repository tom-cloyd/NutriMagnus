# NutriMagnus testing elevation — status and next steps

Started 2026-08-28 in a Cowork session (with the VSCodium Claude extension
handling the doc updates). This file is the handoff point for picking the
work back up. Test suite is at 805 tests as of the last manual update
(user-manual.md Part 2E, "Extensive code testing") — 731 as of 2026-08-28,
+69 from unrelated feature/bugfix work through 2026-09-09, +5 from item #2's
remainder (below), completed 2026-09-09.

## Where this came from

The manual (Part 2E) originally described two test tiers: "behavioral" route
tests (`tests/test_web.py`) and "computational validation" tests (known
inputs → known-correct numbers, e.g. `tests/test_diaas.py`). The question was
whether testing could be elevated above those two tiers. Six candidate tiers
were identified:

1. Scenario/journey tests — long, stateful tests chaining many real actions
   in one session (search → cache → recipe → meal → log across days → trend
   → substitute an ingredient → confirm downstream updates).
2. Property-based/invariant tests (Hypothesis) — generate many
   random-but-plausible inputs and check a math rule holds for all of them,
   not just hand-picked examples.
3. Cross-source data plausibility tests — guard against a data source's
   parsing going wrong or drifting.
4. Browser-level E2E tests (Playwright) — narrow coverage of the JS-driven
   async handoff routes (`search-api-results` and similar), where current
   tests only confirm the HTML contains the right `fetch()` call, not that
   it runs.
5. Mutation testing — checks whether the test suite would actually notice a
   deliberately broken change.
6. CI gate — nothing ran the suite automatically on push before this.

Agreed sequence: 6 → 2 → 1, hold 3/4/5 until those land.

## Done (2026-08-28)

- **#6 — CI gate.** `.github/workflows/tests.yml` added (separate from the
  manual-trigger `release.yml`), runs `pytest -q` on every push and PR.
  Placed and committed.
- **#2, partial — property/invariant tests.** Two new files, both written
  against the real code and verified passing (200+ generated examples each,
  repeated runs, zero failures) in a reconstructed scratch copy before
  delivery:
  - `tests/test_estimate_aa_properties.py` (3 tests) — the AA-estimation
    scaling math in `numa_app/services/aa_estimate.py`'s `estimate_aa()`:
    scaled AA/protein ratios always equal the source's ratios, the scale
    factor is always `target_protein / source_protein`, non-AA fields are
    never touched. Hypothesis found a real edge case on the first draft
    (a technically-positive-but-tiny generated fraction rounding away to
    0.0 under the function's 4-decimal rounding, silently defeating the
    "≥5 AAs present" check) — fixed by snapping near-zero fractions to
    exactly zero in the test strategy.
  - `tests/test_diaas_properties.py` (5 tests) — `diaas.py`'s
    `meal_level_diaas()` and `get_digestibility()`: total protein is an
    exact accounting identity, DIAAS is never negative (it is NOT capped at
    1.0 — that's intentional, per the function's own docstring), digestible
    complete protein never exceeds the digestible-protein ceiling,
    digestibility coefficients always fall in (0, 1], and a single-ingredient
    case matches an independently-computed expected ratio.
- **#3, part of it — the AA-estimation route, end to end.** Two tests
  appended to `tests/test_web.py`:
  `test_copy_aa_estimates_amino_acids_for_source_with_no_native_aa_data` and
  `test_copy_aa_shows_error_flag_when_source_has_no_aa_data`, exercising
  `/food/custom-profiles/{fdc_id}/copy-aa` — the only route by which a
  CoFID/CIQUAL food (see below) ever gets usable AA data. Verified against
  the real `web/backend.py`, real templates, real DB layer.
- `requirements.txt` — added `hypothesis==6.165.10`.
- `user-manual.md` Part 2E — updated by the VSCodium extension to describe
  the new property-based tier and current test count (731). Spot-checked
  this session: accurate, doesn't overstate coverage.

## Done (2026-09-09)

- **#2, the harder half — property tests against the suggestion-ranking
  engine.** `usda_nutrients.py` read in full around `get_aa_gaps()` (line
  143), `_score_one_complement()` (line 635, the shared gap-closing solver
  both single-food tiers and the two-food "pairs" cascade delegate to), and
  `suggest_complements()` (line 731). New file
  `tests/test_complements_properties.py` (5 tests), verified against the
  real code in this environment (not a reconstructed scratch copy — a real
  full run was possible this time): 200-1800 examples per test across
  several stress runs (10x-30x normal `max_examples`) before settling, zero
  unexplained failures.
  - `test_adequate_food_has_no_gaps` / `test_zeroed_aa_always_appears_as_the_worst_gap`
    — baseline sanity checks on `get_aa_gaps()`.
  - `test_gap_closing_is_monotonic_in_grams_added` — the "Monotonicity"
    invariant, scoped to the actual AA-ratio math `_score_one_complement`
    solves (not "pooled DIAAS," which is a different, DIAAS-improver-tier
    calculation — see below for why that stayed out of scope).
  - `test_suggested_grams_actually_closes_the_gap` — "Suggestion
    self-consistency," checked directly against `_score_one_complement`'s
    solved gram amount; a `>= 15g` filter excludes suggestions small enough
    for integer-gram display rounding to reopen the gap by itself (found by
    500 manual trials before writing the filter — a real, accepted
    display-rounding tradeoff, not a bug).
  - `test_pairs_cascade_closes_all_gaps_and_ranking_is_consistent` —
    "Ranking stability," built from a deterministic two-candidate scenario
    (candidate A closes the primary gap but zeroes out a second AA,
    diluting it into a new gap; candidate B closes that second gap without
    reopening the first) with Hypothesis varying the underlying quantities.
    Checks both that the real `suggest_complements()` pairs tier reports
    the constructed pair as `gaps_closed: True`, and that its sort order
    (`gaps_closed and total_grams <= 50` ranks first) holds over whatever
    the real call returns. A 10x-`max_examples` stress run caught one real
    gap in the test's own preconditions — a large-quantity A+B combination
    that correctly solved but was then, correctly, excluded by
    `_build_pairs()`'s own `total_grams > 600` cap, which the test hadn't
    accounted for; fixed by adding that same cap to the test's `assume()`
    filter, not by narrowing the generated ranges.

  **Scope note, disclosed rather than silently narrowed:** the original plan
  also named `complements.py`'s `two_step_combo()` / `build_complement_display()`.
  Those stayed out of scope — both are display/formatting wrappers that call
  `exact_dcp()`, which opens a real DB connection (`diaas.meal_level_diaas`
  via `db.get_db()`), so they aren't pure functions a Hypothesis property test
  can exercise without a database fixture. The actual suggestion *math* those
  two wrap is exactly `get_aa_gaps()` / `_score_one_complement()` /
  `suggest_complements()` in `usda_nutrients.py`, which is what's now covered.
  If `complements.py`'s own DB-dependent glue ever needs property coverage,
  that's a distinct, not-yet-scoped follow-up (would need a temp DB fixture,
  same pattern `tests/conftest.py` already uses for the behavioral suite).

## Not done — pick up here

### 1. #3, the rest: cross-source data plausibility

**Correction to the original framing, worth re-reading before starting:**
of the six data sources, only **USDA** (`usda_api.py`), **CNF**
(`cnf_api.py`), and **Open Food Facts** (`openfoodfacts.py`) are live APIs —
those are the ones where "the API changed its response shape out from under
us" is a real risk worth fixture-testing. **AFCD, CoFID, and CIQUAL are
static local JSON files already bundled in the repo**
(`afcd_data.json`, `cofid_data.json`, `ciqual_data.json`, 1.5-2MB each) —
their lookup modules (`afcd_lookup.py`, `ciqual_lookup.py`,
`cofid_lookup.py`) are ~2KB each, consistent with a simple local-JSON
lookup, not a full API client. So the risk profile for those three is
different: not runtime drift, but "does our parser still read the bundled
JSON correctly," which only matters when that JSON gets refreshed. Worth
confirming this by actually reading the three lookup files (not yet done)
before designing tests around it.

Two parts, per the original plan:
- **Source-fidelity fixtures (USDA, CNF, OFF only, given the correction
  above).** Record a handful of real (not mocked) responses per source as
  fixtures under `tests/fixtures/<source>/`, replay them through each
  source's own parser, assert: no negative values, essential-AA total never
  exceeds `protein_g`, and `usda.has_amino_acid_data()` still returns `True`
  on known-good USDA/CNF sample foods (OFF rarely has AA data, so that
  assertion doesn't apply there). **Needs your real USDA API key** (lives in
  your environment, not Claude's) and ideally a live network connection from
  wherever the recording script runs — plan to do this via the VSCodium
  extension or your own terminal, not Cowork.
- **Estimation-path coverage (CoFID, CIQUAL, most OFF)** — this part is
  actually already covered by the `/copy-aa` route tests added above, since
  those are exactly the sources with no native AA data. Nothing further
  needed here unless new gaps turn up.

### 2. Lower priority, unchanged from the original plan

- **#4 — narrow Playwright E2E** for the JS-driven async handoff routes
  (`search-api-results` and similar). Playwright itself is already present
  in `.venv` as of 2026-09-09, but only as an incidental dependency of some
  other tool — nothing in this project actually invokes it yet.
- **#5 — mutation testing** to check whether the suite actually catches
  deliberate breaks.

Both still queued behind #1 (cross-source fixtures) per the original
sequencing — no new information changes that ordering. (#2's harder half is
done, above — the remaining hold-out was #1 and #2/#3's Playwright/mutation
tail, not #2 itself.)

~~Run the real, full suite once~~ — done, repeatedly: `pytest -q` has been
run clean, locally, in every session since 2026-08-28, and `tests.yml` has
been running it on every push/PR the whole time. No longer worth listing as
a distinct step.

## Quick-start for next session

1. Re-read this file (the "Done (2026-09-09)" section above, specifically —
   #2 is now fully closed, both halves).
2. Confirm CI is green on the latest push (GitHub Actions tab).
3. Open `afcd_lookup.py`, `ciqual_lookup.py`, `cofid_lookup.py` to confirm
   the "static JSON, not live API" correction above before touching #1
   (cross-source fixtures) — not yet done as of 2026-09-09.
4. Item #1's fixture-recording step needs your real USDA API key and a live
   network connection — plan to do that part via your own terminal or the
   VSCodium extension, not a sandboxed session.
