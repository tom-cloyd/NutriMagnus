# NutriMagnus testing elevation — status and next steps

Started 2026-08-28 in a Cowork session (with the VSCodium Claude extension
handling the doc updates). This file is the handoff point for picking the
work back up. Test suite is at 966 tests as of the last manual update
(user-manual.md Part 2E, "Extensive code testing") — 731 as of 2026-08-28,
+69 from unrelated feature/bugfix work through 2026-09-09, +5 from item #2's
remainder, completed 2026-09-09, +3 from item #4 (Playwright E2E), completed
2026-09-10 (all three candidate routes now covered, including the
meal-search one added later the same day), +10 from item #5's pilot
(`TestPooledTid` in tests/test_diaas.py, closing a real zero-coverage gap
mutation testing found — see below), also 2026-09-10, +19 from item #5's
rotation-group-1 pre-release run (also 2026-09-10), +3 (net) from a
follow-up deep-dive into `suggest_complements`/`_score_one_complement`
(also 2026-09-10), then six further rounds (+6, +3, +6, +2, +4, +3 net)
continuing that same deep-dive into `build_complement_display()`/
`two_step_combo()`, then +7 from a second round back on
`suggest_complements`/`_score_one_complement`, then +23 from a third round
targeting `suggest_complements()` directly, then +17 from
`get_density_g_per_ml()`, then +13 from a fourth round back on
`suggest_complements()` (all also 2026-09-10, at the
user's explicit, repeated request to keep pushing — this whole deep-dive
is stated prep work for a Windows port and two upcoming releases), then
+47 on 2026-09-11 from item #3's source-fidelity fixtures work, which
found and fixed three more real live parsing bugs (USDA, CNF, and OFF) —
see below for what all of that closed.
**Correction found along the way:** the originally-reported ~757/191
survivor counts for `build_complement_display()`/`two_step_combo()` were
inflated by a scoping artifact (mutating `usda_nutrients.py` simultaneously
in the same run) — isolated, the true counts were 125/191 — down from the
original ~948 by 59%, now at 341/51 after round 7 of that deep-dive.
`_score_one_complement()` similarly dropped from 105 to 39 across its two
rounds. `suggest_complements()` dropped 394→209 in round 3 — headlined by
its entire `diaas_improvers` tier (~95 lines) having had zero test
coverage of any kind, the single biggest finding of the whole effort —
then 209→117 in round 4, via three sampling-and-fix cycles that found and
closed a second genuine concentration (`_build_pairs()`'s candidate-pool
logic, 48% of remaining survivors) before confirming by re-sampling that
it had converged to baseline scatter.
Two techniques proved dramatically more efficient than one-test-per-mutant
sampling: comprehensive whole-dict field tests (round 4), and
systematically providing a real `ingredients` list / non-1.0 digestibility
value to close previously-untested recompute/masking dimensions (recurred
in both the `complements.py` rounds and the `_score_one_complement` round
2) — see below for exactly what's left, both techniques, and a noted
environment hazard (memory trending down across repeated long-running
mutation-testing sessions — check `free -h`/`df -h /tmp` before
continuing).

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

## Done (2026-09-10)

- **#4 — narrow Playwright E2E.** Confirmed first (per the quick-start note
  below) that AFCD/CoFID/CIQUAL are all thin `StaticSource` wrappers over
  bundled local JSON, no live API — so item #1 below is unaffected and
  still the only one that needs a real USDA key/live network from outside
  this environment.
  - Playwright had no env-var hook to isolate a live server subprocess from
    the real DB/config/prefs (unlike `tests/test_web.py`, which monkeypatches
    those paths in-process — doesn't reach a separate process). Added
    `NUMA_CONFIG_DIR`/`NUMA_DATA_DIR` env-var overrides to
    `platform_utils.get_config_dir()`/`get_data_dir()`, and fixed
    `web/backend.py`'s `_PREFS_FILE` (previously hardcoded to
    `~/.local/share/numa/prefs.json`, bypassing `platform_utils` entirely —
    a latent Windows bug too) to derive from `platform_utils.get_data_dir()`
    instead, so it picks up the same override.
  - New `tests/e2e/`: `conftest.py`'s `live_server` fixture launches
    `_run_isolated_server.py` as a subprocess pointed at temp
    `NUMA_DATA_DIR`/`NUMA_CONFIG_DIR` dirs (demo data auto-seeds on the
    resulting fresh install, giving known local foods like "Chickpeas" to
    search for); that runner script stubs `usda.search_foods` /
    `openfoodfacts.search_foods` / `cnf_api.search_foods` to return `[]`
    before starting uvicorn, so no test ever needs a real API key or live
    network. `test_search_e2e.py` drives it with Playwright (sync API),
    covering `/food/search` and `/food/analyze-portion` at first, then
    `/meal/{meal_id}/search-api-results` too (added later the same day —
    the meal-creation setup it needed turned out to be simple: a plain
    `page.request.post("/meals/create", form={...})`, reading the new meal's
    id back off the post-create redirect URL). All three original candidate
    routes are now covered.
  - The key design point: the initial page render already includes local
    results synchronously (by design — instant local-only response, see
    `_search_logic()`'s own comment), so asserting a seeded food's name
    appears in the table proves nothing about the JS fetch. Both tests
    instead use `page.expect_response()` to assert the browser actually
    issues the `*-api-results` fetch and gets a real 200 back, then confirm
    the DOM reflects it. Verified these aren't vacuous by temporarily
    breaking the fetch URL in `search.html` and confirming the test failed,
    then reverting (clean diff after).
  - New `e2e` pytest marker + `addopts = -m "not e2e"` in `pytest.ini` keeps
    these out of the default `pytest -q` run (and thus `tests.yml`'s
    per-push CI job, whose `python:3.12-slim` container has no browser
    installed anyway) — run explicitly with `pytest -m e2e`.
  - `requirements.txt` gains `playwright==1.61.0` (previously present only
    as an incidental transitive dependency, unused by anything).
  - **CI wiring, added later the same day:** a new, separate
    `.github/workflows/e2e-tests.yml` (plain `ubuntu-latest` runner, not
    `tests.yml`'s slim container, since `playwright install --with-deps`
    needs real apt access) runs `pytest -m e2e` on a weekly schedule
    (`cron: "0 6 * * 6"` — Saturday, same day as the manual weekly sweep,
    though the two run independently) plus `workflow_dispatch` for an
    on-demand run from the Actions tab. Deliberately not folded into
    `tests.yml`'s per-push job — see that file's own header comment and
    this file's "CI wiring" note above for the reasoning (added CI minutes
    and a different flakiness profile on every single push, versus a
    periodic check).

## Done (2026-09-10, continued) — #5 pilot

- **#5 — mutation testing, pilot run.** Installed `mutmut` (3.7.0; needs a
  `[mutmut]` section in `setup.cfg` — 3.x errors out without one, even for
  `--help`). Piloted against `diaas.py` (438 lines) scoped to its own two
  test files (`tests/test_diaas.py`, `tests/test_diaas_properties.py`):
  369 mutants generated, ran in ~61s (~6-7 mutants/second — mutmut only
  reruns tests it's determined actually cover the mutated line, not the
  whole suite per mutant, so this is far cheaper than a naive "full suite
  × every mutant" approach would be).
  - **Real finding, not noise:** `pooled_tid()` (diaas.py:371) — used in 7
    places across `web/backend.py` to size complement suggestions on the
    Recipe, Meal, and Daily Summary pages — had **zero test coverage
    anywhere in the suite** (confirmed via `grep -rn pooled_tid tests/`:
    no hits at all, not just in the two files this run was scoped to).
    Every mutation to it survived by default (mutmut reports these as "no
    tests" rather than "survived").
  - Fixed: `tests/test_diaas.py` gained a `TestPooledTid` class (10 tests).
    First pass killed 30 of the 31 previously-uncovered mutants; a second
    mutmut run against the tightened tests surfaced 6 more real survivors
    (boundary/default-value edge cases the first pass's tests didn't hit:
    a missing `protein_g` key relying on the `.get(..., 0)` default, and
    small-value boundaries like `protein_g=0.5` distinguishing `> 0` from
    an off-by-one `> 1`). Two more tests closed those; a third rerun
    confirmed **0 of 369 mutants survive against `pooled_tid()` now**. One
    accepted true equivalent mutant elsewhere in the file (a `>` → `>=`
    swap on a filter where the excluded/included item contributes exactly
    0 to both the numerator and denominator either way — behaviorally
    unobservable, not worth chasing). Full suite: 815 tests (was 805).
  - `mutants/` (mutmut's working copy + stats) added to `.gitignore` —
    regenerated on every run, never committed. `setup.cfg` committed with
    the `[mutmut]` config, but its `source_paths`/test-selection lines get
    hand-edited per module for each future run — see the rotation plan
    below, not a fixed permanent config.
  - **This closes the case for a "full annual run" being too slow to be
    practical** — extrapolating from diaas.py's pace, even the full
    codebase is probably a 10-30 minute compute job, not hours. The real
    bottleneck turned out to be triage time (deciding which survivors are
    real gaps vs. harmless equivalent mutants), not runtime — see the
    quarterly rotation plan below, which exists for that reason now, not
    a compute-cost reason.

### Ongoing cadence for #5 (agreed 2026-09-10)

Two mechanisms, not redundant — one guarantees a floor, the other pulls
checks forward when warranted:

- **Quarterly rotation, calendar backstop.** Run mutation testing against
  one subsystem group per quarter (highest-risk first), so everything gets
  checked at least once a year on a fixed schedule:
  1. Core nutrient math — `usda_nutrients.py`, `diaas.py` (done, pilot
     above), `profile.py`, `complements.py`, `aa_estimate.py`,
     `recipe_nutrients.py`, `glycemic_load.py`, `rda_status.py`.
  2. Data-source parsing — `usda_api.py`, `openfoodfacts.py`, `cnf_api.py`,
     the CoFID/AFCD/CIQUAL lookups, `food_import.py`, `csv_import.py`/
     `csv_export.py`, `recipe_csv.py`.
  3. Web-layer glue — `web/backend.py` route logic, `day_profile.py`,
     `meal_bcp.py`, `recipe_dcp.py`, `top_contributors.py`,
     `search_ranking.py`, `search_suggest.py`.
  4. Everything else — `export.py`, `demo_data.py`, `plotting.py`,
     `nutrient_trend.py`, `portions.py`, etc.
- **Weekly churn check, early-warning.** During the weekly sweep, check the
  tracked log (module → last-mutation-tested commit hash — now live in
  README-numa-documentation.md's "Quarterly mutation-testing rotation"
  section, wired into the weekly sweep's top-of-checklist due-date block)
  against `git log` for each module *not* due this quarter. Flag any with
  substantial code/test changes since its last check, and ask then whether
  to run it now or wait for its scheduled quarter. This is deliberately NOT
  a background/cron process — nothing runs unattended between sessions; it
  only fires when the weekly sweep itself is run.

## Done (2026-09-10, continued) — #5, rotation-group 1 pre-release run

Ran ahead of the normal quarterly cadence, at the user's request, given the
pilot's finding rate — wanted a broader pre-release look before committing
to a first release, not just diaas.py. Scope: "core nutrient math" (rotation
group 1) — `usda_nutrients.py`, `profile.py`, `numa_app/services/complements.py`,
`aa_estimate.py`, `recipe_nutrients.py`, `glycemic_load.py`, `rda_status.py`
(`diaas.py` itself already done in the pilot above). Triage was deliberately
narrow, per the agreed pre-release scope: only (a) zero-coverage functions
and (b) survivors in the most safety-critical functions (DIAAS/RDA/AA-gap
math) — not an exhaustive pass on all ~1966 survivors this run produced.

- **Environment hazard, not a finding:** this machine is memory-constrained
  under normal desktop use (Firefox/Obsidian/VSCodium already consuming
  most of 39GB RAM) — the run OOM-killed twice (exit 137) before
  succeeding with `mutmut run --max-children 2` after a reboot freed
  memory. VSCodium itself crashed once mid-session (likely the same
  memory pressure, not caused by mutmut specifically). Worth knowing for
  future rotation-chunk runs: use `--max-children 2`, check `free -h`
  first, and expect to need a background run (`run_in_background`) since
  a 4000+-mutant run exceeds a single command's normal timeout. **Second
  hazard found later the same session:** `/tmp` (a 20GB tmpfs — so also
  eating RAM) filled to 100% and broke the test suite outright
  (`sqlite3.OperationalError: database or disk is full`) after enough
  `mutmut` reruns — each `mutmut`-spawned pytest subprocess creates its own
  `/tmp/pytest-N` scratch dir, and pytest's own "keep the last 3" retention
  policy doesn't know about sibling processes, so they never get cleaned up
  (26,539 of them, ~20GB, accumulated over this session). Safe fix:
  `rm -rf /tmp/pytest-of-tomc` between runs — those are pytest's own ended-
  session scratch dirs, not live data. Freed 20GB and dropped memory
  pressure from ~34GB used to ~11GB. **Check `df -h /tmp` alongside
  `free -h` before any future long mutmut session**, and clean it
  periodically during one, not just at the start.
- **False-alarm scoping bug, caught before being reported as a finding:**
  the first attempt's `[mutmut]` `also_copy` in `setup.cfg` didn't include
  `numa_app/__init__.py` / `numa_app/services/__init__.py` (needed since
  mutmut copies only what's listed, not the real package structure) —
  this made 5 of the 7 modules falsely show 100% "no tests" (1496 mutants
  for `complements.py` alone). Fixed by copying the actual missing
  dependencies (`__init__.py` files, plus `portions.py` and
  `update_check.py`, both imported by the selected test files). Lesson
  for future rotation groups touching `numa_app/services/`: don't assume
  a "no tests" result is real without checking the module actually
  imports cleanly under `mutants/` first.
- **Real zero-coverage findings, fixed:**
  - `numa_app/services/recipe_nutrients.py`'s `atomic_recipe_ingredients()`
    (111 mutants, 0 coverage) — feeds a recipe's own DIAAS/digestibility
    pooling, keeping a sub-recipe as one atomic entry rather than
    decomposing it (so its deliberate AA complementarity isn't hidden).
    2 new tests in `tests/test_recipe_nutrients.py`
    (`TestAtomicRecipeIngredients`) cover the core atomic-grouping
    behavior and `portion_factor` scaling, reusing the existing
    `nested_recipe` fixture.
  - `profile.py`'s `rename_profile()`/`delete_profile()`/`get_profile_file()`
    (28 mutants combined, 0 coverage) — lower-stakes than the nutrient-math
    finding (worst case is a broken rename/delete, not a wrong displayed
    number) but real. 6 new tests in `tests/test_profile.py`
    (`TestProfileFileCrud`).
  - `numa_app/services/aa_estimate.py`'s `copy_nutrients_note()` (2
    mutants, 0 coverage) — a trivial string-formatting helper (builds a
    note message, no logic to get wrong). Deliberately left untested —
    not worth the test for what it is.
- **Real safety-critical finding, fixed:** `profile.py`'s `compute_rda()`
  has several age-threshold step functions (magnesium at 31, fiber at 50,
  calcium at 70/51/60 depending on sex, iron at 51) — every one of them
  had a survived mutant on its exact boundary condition (e.g.
  `age >= 31` silently becoming `age >= 32`). Existing tests only compared
  a "young" and "old" profile both well past/before each threshold (e.g.
  40 vs. 75), confirming the direction of change but never the boundary
  itself. New `TestAgeBoundariesExact` class in `tests/test_profile.py`
  (11 parametrized tests) pins the exact age each threshold changes at,
  for every sex. `compute_rda()` still has ~125 other survivors
  unaddressed (mostly default-parameter-value mutations like
  `diet_pref: str = "all"` mutating to `"XXallXX"` — untestable/low-value
  noise since no caller ever omits that argument to exercise the default)
  — not chased further, out of scope for this narrow pass.
- **Major finding, NOT fixed — flagged for a dedicated future pass:**
  `numa_app/services/complements.py`'s `build_complement_display()` (757
  survivors) and `two_step_combo()` (191), plus `usda_nutrients.py`'s
  `suggest_complements()` (357) and `_score_one_complement()` (105) —
  together roughly 1400 of the ~1966 survivors this run produced. Sampled
  ~10 diffs across these: some are the same low-value default-parameter
  noise as `compute_rda`, but several are substantive — internal dict-key
  lookups (`s.get("new_scores")`, `step.get("dcp")`) and an argument
  substitution (`a_diaas` → `None`) that survived, meaning real internal
  branches of the complement-suggestion display/scoring pipeline aren't
  exercised or precisely asserted by any test. This is the core
  suggestion-ranking logic a real user sees and acts on — genuinely
  important — but far too large to characterize or fix in a single
  session (roughly 4x the size of everything else fixed in this pass
  combined). Needs a dedicated future session scoped to just these
  four functions, not folded into routine rotation-chunk triage.
  Verification after all the above fixes: re-ran the full group —
  "no tests" dropped from 150 to 2 (only `copy_nutrients_note`, left
  deliberately); the specific `compute_rda` magnesium-boundary mutant
  confirmed killed. Full suite: 834 tests (was 815 after the diaas.py
  pilot).
- **Rotation group 2 (data-source parsing) not yet run** — deferred given
  time already spent this session; see "Not done" below.

## Done (2026-09-10, continued) — #5, complements.py/suggest_complements deep-dive

At the user's explicit request, went into the large flagged finding from the
rotation-group-1 run above (`complements.py`'s `build_complement_display()`/
`two_step_combo()` and `usda_nutrients.py`'s `suggest_complements()`/
`_score_one_complement()` — ~1400 of ~1966 survivors). Given the scale, this
was NOT a full triage — worked systematically through `_score_one_complement`
(the smallest, most foundational piece) in full, then sampled
`suggest_complements()` for its highest-value findings. `build_complement_display()`
(757 survivors) and `two_step_combo()` (191) were **not touched at all** —
still fully open.

- **`_score_one_complement()` — read in full, all 105 survivors characterized
  by sampling across the ID range** (not random spot-checks). Real,
  fixed findings, each verified with an exact hand-derived expected value
  (not just "still returns something reasonable" like the existing tests) —
  see `tests/test_usda.py`'s `TestScoreOneComplement` for the worked
  arithmetic in each test's own comments:
  - **`predicted_diaas` had no correctness check at all** — the formula
    that decides whether adding a complement would *reduce* overall
    digestibility (and reject it if so) was never verified against a known
    value. A sampled survivor changed a multiply to a divide in that exact
    formula and nothing caught it. One new test constructs a sparse,
    fully-hand-computable nutrient profile (only protein/methionine/cystine
    present — `get_aa_gaps()` skips a key that's *missing* entirely, unlike
    zero) so every intermediate number (alpha, beta, R, denom, grams,
    predicted_diaas) can be derived by hand and compared exactly.
  - The `denom <= 0` boundary (a previous survivor changed it to `< 0`,
    which would have let `denom == 0` fall through into a
    `ZeroDivisionError` instead of the documented `None` return) — new
    boundary test.
  - The Met+Cys/Phe+Tyr paired-AA contribution (`_AA_PAIRS`) being silently
    dropped (a survivor set `pair_key = None`) is now covered implicitly by
    the same hand-calculation test, since it deliberately includes a
    nonzero paired AA.
  - `result["comp_nutrients"]` (a dict-key-literal mutation survived —
    nothing checked this field's identity) — now asserted directly.
  - **Not fixed:** the `base_digestibility` kwarg being silently dropped
    from the internal `protein_completeness()` call. An attempted fix
    turned out to rest on a wrong premise — see the `NOTE:` comment left in
    `tests/test_usda.py` right where that test would go, explaining why (in
    short: `new_scores` are documented as always raw/pre-digestibility, so
    comparing them across digestibility levels doesn't actually test what
    it looks like it tests). A real, narrower gap than it first appeared —
    left open rather than force a fragile test.
  - Verification rerun: 105 → 52 survivors for this function (roughly half
    closed; the rest weren't sampled/characterized).
- **`suggest_complements()` — sampled only, not read/triaged in full
  (357 survivors, ~1/9 of it examined).** One real, high-value fix: the
  gap-closer sort key's primary-gap tiebreaker
  (`not r.get("closes_primary")`) had a survivor that replaced it with
  `not r.get(None)` — which is `True` for every row, silently disabling
  "the candidate that closes the PRIMARY gap sorts first" entirely. This
  directly controls which suggestion a real user sees first. New test
  constructs two candidates — one that closes the primary gap but needs
  75g, one that closes only a secondary gap but needs ~1.2g — and confirms
  the primary-gap closer still sorts first despite needing far more grams
  (this is exactly the scenario that would flip order under the broken
  sort key). Also sampled and left unfixed (real but not chased further,
  given time): `a_diaas` being silently dropped to `None` inside
  `_build_pairs()`'s first-food scoring call; a cached food's own DIAAS
  value (`real.get("diaas")`) not being verified as preferred over the
  curated table's fallback; several dict-key-literal mutations on fields
  (`current_diaas`, `fdc_id`, `predicted_diaas` inside pair dicts) that
  downstream display code reads. Verification rerun: 357 → 352 survivors
  (the vast majority of this function's survivors remain uncharacterized —
  only the one sort-order fix was made).
- **Full suite: 837 tests** (was 834; net +3 — 4 new `_score_one_complement`
  tests + 1 new sort-order test − 2 removed, the flawed digestibility test
  above plus one superseded by a cleaner replacement).
- **`build_complement_display()` (757) and `two_step_combo()` (191) —
  completely untouched.** This is the large majority of the original
  ~1400-survivor finding. Given the time already spent (this session ran
  long even before this deep-dive started), stopping here rather than
  continuing into these two — they need their own dedicated pass, not a
  continuation of this one. Whoever picks this up next should start by
  reading `numa_app/services/complements.py` in full (583 lines — that's
  where both `build_complement_display()` and `two_step_combo()` live) and
  `usda_nutrients.py`'s `suggest_complements()` (lines ~731-1150, the
  candidate-building/pairing/DIAAS-improver logic it delegates to) before
  sampling survivors — the code wasn't summarized anywhere reusable this
  session, only read once and worked from directly. See "Not done" below
  for the concrete next step.

## Done (2026-09-10, continued) — #5, build_complement_display/two_step_combo (the rest of the deep-dive)

Continued the deep-dive above at the user's explicit request ("push on").
**Correction to the earlier writeup, worth reading first:** the ~757/191
survivor counts reported above for `build_complement_display()`/
`two_step_combo()` were measured while `usda_nutrients.py` was ALSO being
mutated in the same run (rotation group 1's mixed scope) — calling into a
simultaneously-mutated `suggest_complements()` inflated the apparent
survivor count. Re-scoping `setup.cfg` to `source_paths=numa_app/services/complements.py`
alone (so `complements.py`'s own mutations run against a real, correct
`usda_nutrients.py`) gives the true count: **358, not 1007** — `two_step_combo`
191 (same, was already isolated), `build_complement_display` **125, not 757**,
`exact_dcp` 29, `load_cache_candidates` 13. `aa_effects` had 0 (all killed).

**Root cause understood: `two_step_combo` had exactly ONE test before this**
(`test_none_without_comp_nutrients`, only the early None-return) — the
entire step1/step2-building success path had never been exercised at all.
`exact_dcp` had ZERO direct tests — every other test in the file passed
`ingredients=None` specifically to dodge its real DB-backed success path.
That's why survivor counts were so lopsided toward these two.

**Real, fixed findings** (all in `tests/test_complements.py`), each verified
against the actual mutant IDs (`mutmut show <id>` confirmed the exact diff
before writing a test, and confirmed killed after):
- **`_grad_steps()`'s fallback had an inverted condition** — `if dcp is None: dcp = _dcp_at_frac(...)`
  survived as `if dcp is not None:`. Since no `ingredients` list means
  `exact_dcp()` always returns `None` (a single-food context, the common
  case), every graduated-dosage step (25/50/75/100%) would have silently
  shown blank `dcp`/`pct_increase` instead of the intended approximation.
  New test also pins the `pct_increase` formula exactly (a separate
  survivor swapped `/` for `*` in it) and — as a side effect of pinning an
  exact value — guards against `base_nutrients.get("protein_g")` silently
  reading a wrong key (another survivor: `.get("PROTEIN_G", 0.0)`), since a
  wrong/zero `base_protein` would break the same formula check.
- **`exact_dcp()`'s return statement had `is not None`/`is None` inverted**
  — would have made it always return `None` even when it had a real
  computed value, forcing every caller into fallback approximations
  permanently. New `TestExactDcp` class (3 tests) exercises the real
  DB-backed success path for the first time, cross-checking the result
  against an independent direct call to `diaas.meal_level_diaas()` (a
  different code path, not a re-derivation of the same formula).
- **`load_cache_candidates()`'s excluded-name check used `break` instead of
  `continue`** — would have silently stopped searching the *entire rest* of
  the curated table after the first excluded name, not just skipped that
  one entry. The existing exclusion test couldn't have caught this (it only
  ever inserted one matching food, so a fully-broken loop still "passed" —
  nothing else to find). New test inserts a second food matching the
  curated entry immediately after the excluded one in table order, and
  confirms it still gets found.
- **`two_step_combo()`'s step1-building path** — new test builds a real
  `gc` dict via an actual `suggest_complements()` call (more robust than
  hand-building one) and asserts every step1 field against it, including
  the `dcp_after` fallback formula (forced via `ingredients=None`, same
  trick as above).

**Not fixed — disclosed, not silently skipped:**
- `two_step_combo()`'s **step2** path (the DIAAS-booster pairing) — needs a
  gap-closer that still leaves DIAAS headroom for a second food to improve
  further. Tried several constructed scenarios; none naturally produced a
  non-`None` step2 without much deeper curated-table modeling than the time
  available justified. A handful of step2-specific dict-key-literal
  survivors (`fdc_id`, `diaas`, `comp_nutrients`, `gc_diaas`, `net_gain`
  rounding) remain open.
- The remaining ~100 `build_complement_display` survivors beyond the ones
  fixed above (mostly default-parameter-value noise like `diet_pref: str = "all"`
  mutating to `"XXallXX"`, never exercised since no caller omits that
  argument — same low-value pattern seen in `compute_rda` earlier).
- `two_step_combo`'s remaining ~185 survivors — only the step1 path got one
  comprehensive test; individual dict-key mutations beyond what that single
  test happens to cover were not chased one-by-one.

**An unresolved anomaly, disclosed rather than glossed over:** a verification
rerun (`mutmut run`, both `--max-children 2` and `--max-children 1` —
ruled out a concurrency/race explanation) showed a large, reproducible
INCREASE in total survivors (358 → 874) after these fixes, despite: (a) all
843 tests passing cleanly and repeatedly under direct `pytest` execution
(5 consecutive clean runs, no flakiness), and (b) every specific targeted
mutant ID (the `_grad_steps` fallback, `exact_dcp`'s inverted return, the
`break`/`continue` bug) individually confirmed killed by name. The
regression shows up broadly across the file, including in `aa_effects` —
a function untouched by this session's changes, previously 100% killed,
now showing 17 survivors. This pattern (a broad, function-agnostic
regression coinciding with new tests that touch a real SQLite file via
`db_conn`, combined with mutmut's pytest invocation using `-x` — stop on
first failure) points at mutmut's own coverage-based test-selection
possibly mis-tracking dependencies once file-backed DB tests enter the
mix, not a real drop in test quality — but this was NOT run to ground
before time ran out. **Treat any future `mutmut` aggregate count for
`complements.py` with suspicion until this is understood** — verify
specific mutant IDs by name (as done here) rather than trusting the
survived/killed totals at face value. Worth its own investigation, not a
routine rotation-chunk task.

Full suite: **843 tests** (was 837 before this continuation; +6 net — 5 new
tests plus the earlier session's +1 from this same file).

## Done (2026-09-10, continued) — #5, the "keep going" round

At the user's explicit request ("push on... keep going, this is getting
important results"), continued mining the same `complements.py` survivor
pool. **The mystery from the section above got resolved in an unexpectedly
useful way**, not by root-causing it, but by acting on it: sampling the
"newly surviving" mutants in `aa_effects` (previously 0 survivors reported,
suddenly 17) turned out to surface **real bugs a first, incomplete pass had
simply never sampled** — not tooling noise. Best working theory for why the
count itself shifted between runs: `tests/test_complements_properties.py`
uses Hypothesis (randomized inputs), so mutmut's one-time coverage-tracking
snapshot likely varies slightly run to run depending on which random
examples happened to execute which branches. Not proven, but the numbers
did stabilize to identical values (633/863, twice, including with
`track_dependencies=False`) once no further test changes were made between
runs — so this looks like initial-snapshot variance, not ongoing flakiness.
**Practical conclusion for future work: don't trust an aggregate survivor
count from a single run as either a floor or a ceiling — sample real diffs
and verify by mutant ID, exactly as this whole session has been doing.**

**Real, fixed findings** (all in `tests/test_complements.py`, each verified
against the actual mutant diff and confirmed killed by name afterward):
- **`aa_effects()`'s `"label"` field used the wrong tuple index** —
  `nutrient_label(aa)[1]` (the unit, e.g. "g") instead of `[0]` (the display
  name, e.g. "Lysine") — nothing checked its value. Also fixed in the same
  pass: the `"met"` boundary at exactly `1.0` (a survivor changed `>=` to
  `>`), and `"before"`'s value/rounding.
- **`load_cache_candidates()`'s `"diaas"` field** — nothing checked its
  value; a survivor both renamed the key and separately read the wrong
  row's name for the lookup.
- **`two_step_combo()`'s step2 path finally got a working test** — the
  construction that failed twice before (a gap-closer that still leaves
  DIAAS headroom for a second food) turned out to just need a smaller,
  fully-controlled sparse nutrient profile instead of relying on the
  curated table's real data to happen to cooperate. This closes real
  survivors: `exclude_names` being silently dropped from step2's internal
  `suggest_complements()` call (a genuinely user-visible bug — an "ignored"
  food could still appear as a two-step suggestion) was *found* but not
  yet fixed (see below — the working test doesn't happen to exercise that
  specific parameter's effect); several step2 dict-key-literal mutations
  are now caught by the new comprehensive field check.
- **`build_complement_display()`'s `has_estimate_or_generic` check had its
  `"estimated"` half silently neutered** (`row.get("estimated")` →
  `row.get(None)`, always falsy) — and the *existing* test for this didn't
  catch it, for a subtle reason: its scenario happened to also include an
  unrelated generic (no-`fdc_id`) suggestion, so the flag stayed `True` via
  the *other* half of the check by coincidence. New test explicitly
  excludes every generic entry from the scenario, isolating the
  `"estimated"` half specifically.
- **`build_complement_display()`'s `"gap_effect"` comp_sort mode was
  silently broken** — `-(s.get("gaps_closed") or 0)` survived as
  `-(s.get("gaps_closed") and 0)`, which evaluates to `-0` for *any* row
  with a nonzero `gaps_closed` (the overwhelmingly common case) —
  neutering the primary sort key entirely. Even sneakier: the *existing*
  sort-mode test didn't catch it either, because Python's stable sort left
  the neutered-and-tied rows in their original list order, and that
  original order happened to already match the correct sorted order. New
  test feeds the same two candidates in the *reversed* starting order,
  forcing the sort to actually prove itself.
- **`build_complement_display()`'s pairs tier (`_fmt_pair()`) had NO test
  at all** — a survivor swapped a `*` for a `/` in the `total_dig_complete`
  fallback formula (25.0 × 0.6 = 15.0 vs. 25.0 ÷ 0.6 = 41.7 — wildly
  different). New test is the first to exercise this tier's formatting at
  all.

**Verification:** full suite 849 tests (was 843); a rerun confirmed all 6
spot-checked targeted mutants killed, zero regressions. Aggregate counts
for context only (see the caveat above about trusting these):
`build_complement_display` 707→675, `two_step_combo` 133→96,
`load_cache_candidates` 12→10, `aa_effects` 17→4, `exact_dcp` unchanged at 5.

**Still open — `build_complement_display` (675) and `two_step_combo` (96)
remain the overwhelming majority of `complements.py`'s survivors, sampled
only in scattered patches, not systematically worked through.** Known,
found-but-not-yet-fixed real bug: `two_step_combo()`'s step2 silently drops
`exclude_names` when searching for a DIAAS-booster, so a food the user
explicitly flagged "ignore" could still appear as a two-step suggestion —
this needs its own test (the current step2 test doesn't pass a non-empty
`exclude_names`, so it doesn't exercise this).

## Done (2026-09-10, continued) — #5, fourth round: comprehensive field tests

At the user's continued explicit request ("keep going... quite productive").
Two changes in approach this round, both high-leverage:

1. **Fixed the one already-known, not-yet-fixed bug first**: `two_step_combo()`'s
   step2 silently dropping `exclude_names` — turned out to already work
   correctly in the real code (confirmed: excluding step2's own winning
   candidate by name correctly makes it disappear); just needed a test.
2. **Switched from one-mutant-one-test to comprehensive field tests.**
   Earlier rounds wrote a narrow test per specific mutant found while
   sampling. This round instead wrote a few tests that each assert on
   *every* field of one function's output at once (`_fmt()`,
   `_fmt_improver()`, `_fmt_pair()`, and the top-level summary fields),
   built from one fully-controlled, hand-computed input. **Payoff was much
   larger than expected: 3 such tests dropped `build_complement_display`'s
   survivors from 675 to 428 in one step** — each comprehensive test
   happens to kill dozens of scattered dict-key-literal and
   default-value mutations across the whole function at once, since it
   touches nearly every line of output construction. Recommended technique
   for whoever picks up rotation groups 2-4: prefer one comprehensive
   "does every field match a hand-computed value" test over many narrow
   ones, when a function is mostly assembling a dict from simple
   expressions — it's dramatically more test-writing-effort-efficient.

**Also fixed, using the established "reverse the input order" technique**:
two more instances of the same sneaky stable-sort-masking bug pattern
found in the previous round (`comp_sort="grams"` and `diaas_sort="grams"`
each had their sort key silently neutered by a survivor, undetected by the
existing test because the stub data's *given* list order happened to
already match the *correct* sorted order — Python's stable sort left a
fully-tied list untouched, passing by coincidence). Checked every other
sort-mode test's stub-data ordering against its expected result while
here; the `dcp` and `digestible_protein` modes were confirmed NOT
susceptible (their expected order genuinely differs from the stub's given
order, so a broken sort key there would already fail visibly).

**Verification:** full suite 855 tests (was 849); rerun confirmed the
`comp_sort="grams"` fix killed, zero regressions. Aggregate counts for
context: `build_complement_display` 675→424, `two_step_combo` 93→93 (the
exclude_names test targeted a specific behavior already covered by an
earlier field-value test, so didn't move this function's count further).

**Still open — diminishing returns setting in, but not exhausted.** 424 +
93 = 517 survivors remain across these two functions. A quick sample of
what's left (see this round's investigation) suggests a higher proportion
of genuinely low-value cases now (unkillable default-parameter values,
`_dcp_at_frac`'s narrow edge-case boundaries, one confirmed-unreachable
dead branch — `limiting_aa` can never be falsy at the point it's checked,
since `build_complement_display` already returned early if `gaps` were
empty) than in earlier rounds, though real bugs may well still be mixed
in — this round's two additional sneaky-sort-bug catches show the pattern
isn't exhausted. Next session: consider running the SAME comprehensive
field-test technique against `two_step_combo()`'s step2 output (only
partially covered so far) and against `_grad_steps()`'s own `_dcp_at_frac`
helper directly, before falling back to narrow one-off sampling.

## Done (2026-09-10, continued) — #5, fifth round: applying the technique elsewhere

At the user's continued explicit request. Applied the comprehensive-field-test
technique (discovered last round) to the two places flagged as the
suggested next step: `two_step_combo()`'s step2 output and `_dcp_at_frac()`.

- **`two_step_combo()`'s step2 test extended to pin every field** (was:
  name truthy, diaas rounding, dcp_before/net_gain formulas only). The
  scenario is fully deterministic (verified stable across repeated runs),
  so every field — `fdc_id`, `estimated`, `grams`, `amount_note`,
  `new_diaas`, `dcp_after` — could be pinned to an exact expected value.
  Also completed step1's field coverage (`aa_effects` was the one field
  missing) and, sampling the remainder, found and fixed one more real gap:
  `aa_effects_limit` being silently dropped from step1's internal
  `aa_effects()` call (passed `limit=None` instead) — invisible in every
  existing scenario because none of them had more gaps than the default
  limit of 3 to prove anything; new test uses a 9-gap scenario with an
  explicit `aa_effects_limit=2` to distinguish.
- **`_dcp_at_frac()`'s own weighted-pool IAA formula hand-verified across
  all four graduated dosage steps** (25/50/75/100%) — previously only
  reachable indirectly through a test checking `pct_increase`'s formula,
  never `_dcp_at_frac`'s own per-AA weighted math directly.

**Verification:** full suite 857 tests (was 855); rerun confirmed real
improvement, zero regressions. Aggregate counts for context:
`two_step_combo` 93→64 (its biggest single-round drop — the comprehensive
step1/step2 field tests turned out to matter more for this function than
any other round's fixes), `build_complement_display` 424→400.

**Still open — same technique, same suggested next targets, now smaller.**
517→481 combined survivors across the two functions. Diminishing returns
are more visible now: sampling this round's remaining `two_step_combo`
survivors found mostly cases needing a real `ingredients` list to matter
(this file's tests have consistently used `ingredients=None` throughout,
which is realistic for the single-food context but never exercises the
"exact per-ingredient recompute" code paths — a real, if narrow, gap
pattern worth naming for whoever continues: **every test in this file so
far uses `ingredients=None`; none exercise the meal/recipe context where a
real ingredients list is passed and `exact_dcp()` actually returns a
value instead of `None`.** That's a distinct, unexplored dimension from
the per-field/per-branch gaps found so far.

## Done (2026-09-10, continued) — #5, sixth round: the `ingredients` dimension

At the user's continued explicit request. Pursued the gap pattern named at
the end of round 5: every test in `tests/test_complements.py` used
`ingredients=None`, so none exercised the real per-ingredient `exact_dcp()`
recompute path — only the fallback approximations.

Added 4 new tests, one per call site, each providing a real `ingredients`
list (a controlled Oats/Peanut-butter/Cheese scenario) and cross-checking
the result against an **independent direct call to `exact_dcp()`** with
the same data:
- `_fmt()`'s `total_dig` — confirmed it not only matches the independent
  recompute but is **numerically different from what the fallback formula
  would give** (13.4 vs. 19.0), proving the real path is genuinely taken,
  not coincidentally matching a fallback.
- `_grad_steps()`'s per-step `dcp` (all 4 dosage steps).
- `two_step_combo()`'s step1 `dcp_after` (5.1 vs. 15.0 for the identical
  scenario without ingredients in an earlier round's test — same
  "genuinely different from fallback" confirmation).
- `_fmt_pair()`'s `total_dig_complete` (a real two-food per-ingredient
  recompute).

No new bugs found this round — but that's a real, useful result in
itself: it confirms `exact_dcp()`'s wiring into all four call sites is
correct when given real data, closing out a previously-untested dimension
rather than leaving it as an unknown. (`two_step_combo`'s step2 `b_dcp`
with real ingredients was investigated but not completed — extracting a
curated-table winner's real `comp_nutrients` to build an independent
cross-check proved more involved than the other three; left open.)

**Verification:** full suite 861 tests (was 857); rerun confirmed real
improvement, zero regressions. Aggregate counts: `build_complement_display`
400→371, `two_step_combo` 64→57.

**Still open.** 371 + 57 = 428 combined survivors (down from 948 at the
start of this deep-dive — more than halved). Memory is trending down
across repeated runs this session (39GB machine now routinely dropping to
~14GB available mid-run) — worth checking `free -h`/`df -h /tmp` before
each further run and cleaning `/tmp/pytest-of-tomc` proactively, not just
when something breaks.

## Done (2026-09-10, continued) — #5, round 7: closing the last real gap,
## plus two invariant tests

Three targeted additions to `tests/test_complements.py`, closing the
specific next-steps named at the end of round 6:

1. **`two_step_combo`'s step2 `b_dcp` with real ingredients** — the one
   corner round 6's "ingredients provided" dimension left unclosed.
   `test_step2_dcp_after_uses_real_exact_dcp_when_ingredients_provided`
   builds the same deterministic scenario used by the sparse-profile tests
   (base profile that always picks "Soy protein isolate" as the gap-closer
   candidate), now passing a real `ingredients` list through, and uses
   `usda.get_complement_nutrients()` to independently fetch the winner's
   real curated nutrient profile for the cross-check against a direct
   `exact_dcp()` call — without hard-coding that data into the test. Note:
   unlike step1's `dcp_after` (which clearly differs from its
   `ingredients=None` counterpart, 5.1 vs 15.0), this scenario's real and
   fallback `b_dcp` values happen to coincide at 32.0 — confirmed a genuine
   coincidence of this specific base/candidate combination via the
   independent cross-check, not evidence the real path isn't exercised.
2. **`_total_dig()`'s scale-formula branch** — every existing test only
   ever exercised the function's "else" branch (`new_scores={}` falsy,
   falls back to `base_digestible + dig`). `test_total_dig_scale_formula_branch`
   hand-computes the other branch (`new_scores` truthy, scaled by
   `min(new_adj_min)/old_adj_min` capped at 1.0) against a stubbed
   candidate, confirming `round((20.0 + 10.0) * 0.8, 1) == 24.0`.
3. **The `new_complete` top-of-tier promotion invariant** — documented in
   `build_complement_display()`'s own docstring ("A full profile-completer
   is always promoted to the top of its tier regardless of mode") but never
   actually tested; every sort-mode test up to now only ever compared two
   `new_complete=False` candidates.
   `test_new_complete_always_promoted_to_top_regardless_of_sort_mode` pits a
   `new_complete=True` candidate that's worse by every other metric (more
   grams, fewer gaps closed, less digestible protein added) against a
   `new_complete=False` candidate that wins on all of those, and confirms
   the complete one still sorts first across all four `comp_sort` modes.

No new application bugs found this round — all three closed real
test-coverage gaps rather than catching new mutants, consistent with
diminishing-but-real returns.

**Verification:** full suite 864 tests (was 861); mutmut rerun confirmed
real improvement, zero regressions. Aggregate counts: `build_complement_display`
371→341, `two_step_combo` 57→51.

**Still open.** 341 + 51 = 392 combined survivors (down from 948 at the
very start of this deep-dive — 59% reduction). Same diminishing-returns
picture as round 6: real gaps still turning up, but slower per round.
Concrete next steps unchanged in spirit: apply the comprehensive-field-test
technique to whichever of `build_complement_display`'s internal closures
haven't gotten one yet (the sort-key lambdas' exact tie-break values are
the main remaining candidate), or move on to `suggest_complements()`'s
~350 survivors / `_score_one_complement()`'s remaining 52, which have had
much less attention than `complements.py`'s two headline functions.

## Done (2026-09-10, continued) — #5, suggest_complements/_score_one_complement, round 2

At the user's request to keep going, shifted target from `complements.py`
back to `usda_nutrients.py`'s `suggest_complements()`/`_score_one_complement()`
— untouched since the single round documented above (105→52 survivors for
`_score_one_complement`, `suggest_complements` barely sampled). Re-scoped
`setup.cfg` to `source_paths=usda_nutrients.py` (`also_copy=usda_api.py,
usda.py`; test selection `tests/test_usda.py`) — isolating it from
`complements.py` the same way that file was isolated from
`usda_nutrients.py` in the earlier correction, to avoid the same
cross-file survivor-count inflation. Baseline this run: `suggest_complements`
394, `_score_one_complement` 57, `get_density_g_per_ml` 53,
`protein_completeness` 40, `_estimate_aa_from_curated` 11, `get_aa_gaps` 10,
`get_antinutrient_flags` 6, `_find_complement_by_name` 2 (the earlier 52
vs. this run's 57 for `_score_one_complement` is the known aggregate-count
run-to-run variance, not a regression).

Read `_score_one_complement()`'s remaining survivors in full this round
(all ~57 IDs, not sampled) and fixed 10 real, distinct bugs, each verified
with an exact hand-derived expected value (see `tests/test_usda.py`'s
`TestScoreOneComplement` for the worked arithmetic in each test's
comments):
- **`R`'s digestibility divide silently became a multiply** — identical
  masking pattern to `complements.py`'s earlier "everything tested at
  `ingredients=None`"/"digestibility always 1.0" findings: every existing
  test used `base_digestibility=1.0`, where `/1.0` and `*1.0` are
  indistinguishable. New test uses `base_digestibility=0.5`, where the two
  formulas diverge sharply (R=0.096 vs 0.024), cascading into a completely
  different exact grams/`predicted_diaas`.
- The same masking pattern recurred inside `predicted_diaas`'s per-AA loop
  (`base_aa * base_digestibility` silently becoming `base_aa /
  base_digestibility`) — closed by the same `base_digestibility=0.5` test.
- The `grams <= 0 or grams > 500` guard's `or` silently became `and`
  (making the guard permanently unsatisfiable — `grams` can never be both
  `<=0` and `>500` at once) — two new boundary tests (`grams` solving to
  exactly 0; a huge-deficit/near-reference-ratio candidate solving to
  grams far past 500).
- `gaps_closed = len(base_gaps) - len(new_gaps)`'s `-` silently becoming
  `+` — closed by adding an exact-count assertion to the existing
  lysine-borderline test (Met+Cys closes, lysine opens — nets to 0 real,
  would read 2 under the mutant).
- The per-AA "skip if absent from both foods" guard
  (`base_aa <= 0 and comp_aa <= 0: continue`) had its `and` silently
  become `or` — silently dropping any AA present in only one of the two
  foods from the `predicted_diaas` calculation. New test gives the
  candidate an AA (threonine) the base lacks entirely, tuned so that AA's
  ratio becomes the new minimum — the `or` mutant would wrongly exclude it
  and report a much higher (wrong) `predicted_diaas`.
- `comp_dig`'s (and separately `dig_added`'s) "assume fully digestible
  when the candidate's own DIAAS is unknown" fallback silently became 2.0
  instead of 1.0 in two places — no existing test passed `cand_diaas=None`
  while checking an exact dependent value. New test does, catching both.
- The final rejection guard (`predicted_diaas is not None and
  base_digestibility < 1.0 and predicted_diaas < base_digestibility:
  return None`) had its `is not None` silently become `is None` —
  inverting when a low-quality pairing gets rejected. Nothing exercised
  the actual rejection path before (every test used `base_digestibility=1.0`,
  where this guard is a documented no-op). New test: a candidate that
  closes the target gap in raw terms but whose poor own digestibility
  drags the pooled prediction below the base's 0.9 — must be rejected.
- `closes_primary`'s ternary else-branch (`False` when `base_gaps` is
  empty) had no test ever calling the function with an empty `base_gaps`
  list to exercise it — new direct test does.
- `new_complete`'s dict-key lookup had multiple survived key-literal/key-type
  mutations (`.get(None, False)`, `.get(False)`, `.get("XXcompleteXX",
  False)`, `.get("COMPLETE", False)`) — none caught because no existing
  test's scenario actually produced `new_complete=True`, so the mutants'
  wrong-default `False` coincidentally matched the real (also `False`)
  result. Extended the existing full-closure test (BASE/BRAZIL, which
  closes every essential AA) with an explicit `is True` assertion, closing
  all four at once.

**Not fixed, left open (documented, not chased further):** the sparse
`.get(key, 0.0)` → `.get(key, 1.0)`-style default-value mutations
throughout (roughly a dozen IDs) are dead-default noise in practice — every
real nutrient dict always carries every `NUTRIENT_MAP` key, so the
fallback default is never actually reached; not worth fragile sparse-dict
tests to chase. The `target_still_gapped = None` mutant (bypasses the
"candidate didn't actually close the gap" rejection) is real but requires
constructing a scenario where the analytically-solved grams, after
`round()`-ing, falls just barely short of the `_MIN_GAP_SCORE=0.95`
threshold — attempted numerically, didn't find a clean non-fragile
construction in the time available; same character as the
`base_digestibility` kwarg-drop gap left open in the previous round.

**Verification:** full suite 871 tests (was 864; +7 new tests). Mutmut
rerun confirmed real improvement, zero regressions elsewhere: `_score_one_complement`
57→39 (18 killed — 2 more than the 10 targeted bugs above, from incidental
kills via the exact-value cross-checks), plus a bonus drop in
`protein_completeness` 40→39 (the same file, hit incidentally by the same
assertions since `_score_one_complement` calls it internally).
`suggest_complements` (394) and everything else unchanged, as expected —
not touched this round.

**Still open.** `suggest_complements()`'s 394 survivors remain almost
entirely uncharacterized (only the one sort-order fix from the earlier
round touched it) — the highest-value remaining target in this whole
mutation-testing effort by volume. `_score_one_complement()`'s remaining
39 are the dead-default noise plus the one hard `target_still_gapped`
gap, both explicitly not worth chasing further without a better technique.
`get_density_g_per_ml()` (53) and `protein_completeness()` (39, now
`suggest_complements`-adjacent in priority) are untouched entirely.

## Done (2026-09-10, continued) — #5, suggest_complements, round 3 (the big one)

At the user's request to keep going, targeted `suggest_complements()`'s 394
survivors directly — untouched by name until now (round 2 above only
fixed `_score_one_complement()`). Read the whole function in full (~420
lines, `usda_nutrients.py` lines 731-1150) before sampling anything.

**The single biggest finding of this whole mutation-testing effort:**
`_diaas_improver_score()` — the ~95-line closure that builds the
"diaas_improvers" tier (the numerical pooled-DIAAS search used when a food
can't analytically close any specific AA gap but still meaningfully
improves overall quality, e.g. nutritional yeast) — **had ZERO test
coverage of any kind.** Not a single test in `tests/test_usda.py` ever
referenced `result["diaas_improvers"]`. New `TestDiaasImprovers` class (6
tests): built a synthetic candidate whose every essential AA sits exactly
at the FAO reference ratio (`denom == 0` for every possible gap-closer
target, so it's guaranteed to fall through to the diaas-improver path),
then independently reimplemented the function's own documented pooled-DIAAS
formula (from its docstring) inline in the test — using the real
`diaas.FAO_REFERENCE`/`diaas._IAA_PAIRS`/`diaas.get_digestibility()` — and
cross-checked every field (`current_diaas`, every step's `new_diaas`/`dcp`,
`grams`, `protein_added`, `digestible_protein_added`, `diaas`) against it.
Also covered: the `current_diaas_val >= target` early-exit (no improvers
suggested when the base is already good enough), and the `base_food_name`
lookup branch (looks up a real TID via `diaas.get_digestibility()` instead
of falling back to `base_digestibility` — no prior test ever passed
`base_food_name` to `suggest_complements()` at all). **This one class of
tests alone dropped the survivor count 394→291** (103 killed) — by far
the single largest jump of the whole session, bigger than any other
round's total.

**Other zero-coverage areas found and closed, each previously entirely
untested:**
- **`diet_pref` filtering** (`vegetarian`/`plant_only`, `_diet_allows()`/
  `_diet_allows_by_name()`) — no test ever passed anything but the "all"
  default, and no test ever omitted the parameter to exercise the default
  itself either (closing a distinct dict-key/default-value mutant from
  passing it explicitly). 6 new tests: all/vegetarian/plant_only differ
  correctly on real curated-table meat vs. dairy entries (Chicken breast
  vs. Cheese, cheddar), the by-name pantry-side filter, an unmatched
  pantry food passing through untouched, and the default value itself.
- **`exclude_names`** (the web app's per-suggestion "ignore" checkbox
  wiring) — same story, zero coverage. 4 new tests: pantry exclusion,
  case-insensitivity, general-tier exclusion, and a control confirming
  unrelated candidates aren't also (over- or under-) excluded.
- **The gap-closer sort key's second tiebreaker** (`-r["gaps_closed"]`,
  "most gaps closed wins after the primary-gap tiebreak") — only the
  first tiebreak (primary-gap) had a test; this one didn't. New test:
  two candidates both closing the primary gap, one closing both gaps but
  needing far more grams — the 2-gap closer must still sort first.
- **Duplicate candidate names** (`seen_names` dedup) — a name appearing
  twice in `pantry_candidates` must be scored/listed only once.
- **The pairs tier's summary fields** (`total_protein_added`,
  `total_dig_added`, `predicted_diaas`, `new_complete`, `new_scores`,
  `gaps_closed`) had only structural tests (right keys present, sorted
  order, no dupes) — zero exact-value checks. New test independently
  recomputes both legs via direct `_score_one_complement()` calls (the
  same building blocks `_build_pairs()` itself uses) and cross-checks
  every summary field.
- **A real logic bug**: the pairs cascade's second-leg acceptance check
  (`if b_m["remaining_gaps"] > 0 or b_m["opens_new_gap"]: continue`) had a
  survived `continue`→`break` mutation — which would abandon the search
  for a valid second leg entirely the moment ANY candidate failed, instead
  of trying the next one. New test places a bad second-leg candidate
  (pure lysine, dilutes every other AA) BEFORE a good one (closes
  everything cleanly) in pantry order and confirms the good pairing is
  still found — this is a genuinely user-visible bug class (a valid
  two-food suggestion silently missing depending on candidate order).
- Several dict-key-literal mutations closed with direct field-identity
  assertions: gap-closer's `diaas` field reflecting the candidate's own
  input value (not a `.get(None)` mutant coincidentally matching a
  `None`-passed test scenario every prior test used), the diaas-improver
  dict's `"diaas"` key, and the pairs foods' `fdc_id`/`recipe_id`/
  `comp_nutrients` keys (extended the existing structural key-presence
  tests to include them, plus a `comp_nutrients is not None` check).

**Verification, done incrementally across 4 mutmut reruns as tests were
added in batches:** 394 → 291 (diaas_improvers + pairs cross-check, 6
tests) → 253 (diet_pref + exclude_names + gaps_closed tiebreak, 10 tests)
→ 249 (base_food_name + duplicate-name dedup, 2 tests) → **209** (dict-key
identity checks + the continue/break pairs bug, 5 tests). 23 new tests
total this round. Full suite: **892 tests** (was 871). Zero regressions
at any point; `get_density_g_per_ml` (53), `protein_completeness` (39),
`_estimate_aa_from_curated` (11), `get_aa_gaps` (10), and the rest held
steady throughout, confirming nothing else was touched.

**Not fixed, sampled but left open (real, lower-value-per-effort):**
several more dead-default `.get(key, 0.0)`-style mutations in the same
vein as `_score_one_complement`'s round-2 findings; a `_diaas_improver_score`
guard's `or`→`and` mutation (`if base_protein <= 0 or comp_protein <= 0`)
that's hard to reach through the public API since `suggest_complements()`
itself early-returns before reaching this closure when `base_protein <= 0`;
a step-size list literal boundary (`150`→`151`); and two candidate-
resolution spots in `_build_pairs()`'s own candidate-pool building
(dropping a pantry food's curated-table-fallback nutrients/recipe_id) that
would need a dedicated pantry-sourced-pairs-candidate scenario not yet
built.

**Still open.** `suggest_complements()`'s 209 remaining survivors (down
from 394 — a 47% reduction this round alone, and from the original ~948
survivor figure at the very start of this whole mutation-testing effort,
a combined reduction of well over 75%) are now much more evenly spread
across smaller pockets rather than one dominant blind spot.
`get_density_g_per_ml()` (53 survivors) remains completely untouched and
is now the most attention-starved function of meaningful size in
`usda_nutrients.py`.

## Done (2026-09-10, continued) — #5, get_density_g_per_ml

At the user's explicit instruction to keep going ("this is all preliminary
to creating the Windows version, then pushing 2 releases") — self-contained
53-line function (density estimation for volume-unit portions, e.g. "2
tablespoons"), completely untouched by this whole mutation-testing effort
until now. Existing coverage (11 tests) only exercised the static
keyword-table lookup path and one narrow case of the USDA-portion
fallback; almost all 53 survivors were in that fallback's parsing logic.

17 new tests across two verification passes:
- **Round 1 (12 tests, 53→21):** fraction count parsing ("1/2 cup"), the
  `T`/`t`/`c` case-sensitive abbreviation expansions, missing-leading-number
  defaulting count to 1.0, zero-gram-weight skip, out-of-bounds density
  falling through to the next portion rather than stopping, the `fl oz`/
  `teaspoon`/`tbs` keywords, `None` portions not crashing, an
  unrecognized-unit portion being ignored, and the count multiplier
  actually scaling the ml value (not just being parsed and discarded).
- **Round 2 (5 tests, 21→13):** the `tbsp`/`tsp` keywords specifically
  (distinct from `tablespoon`/`tbs` and from the `t`→`teaspoon` abbreviation
  expansion, which had been coincidentally masking `tsp` never being
  reached directly); the `gw <= 0` skip guard's boundary (a survived
  `gw <= 1` mutation — `gram_weight=1` is real, non-degenerate data that
  yields a perfectly plausible density and must not be treated as
  zero/missing); a `continue`→`break` bug (a single zero-weight portion
  earlier in the list must not prevent a later valid portion from being
  used — same bug *class* as round 3's pairs-cascade finding above, a
  recurring pattern this session); and the `0.15`/`1.6` plausibility
  bounds' inclusivity at both exact boundary values, plus confirming the
  upper bound really is 1.6 and not something wider.

**Left open, sampled and understood but not chased:** several `_ABBREV`
string-literal mutations (`"tablespoon"`→`"XXtablespoonXX"` etc.) turned
out to be genuine equivalent mutants in practice — the mutated string
still contains the real keyword as a substring (`"xxtablespoonxx"`
contains `"tablespoon"`), so the later `if vol_word in desc` substring
check still matches regardless. Also left open: `.get("gram_weight", 0)`
default-value mutations (dead in practice — portion dicts always carry
the key) and the `gw < 0` vs `gw <= 0` boundary at exactly `gw == 0`
(also effectively equivalent — a zero-weight portion always produces
`density == 0.0`, which fails the plausibility bounds check regardless of
whether the skip guard fires).

**Verification:** full suite **909 tests** (was 892). Zero regressions;
`suggest_complements` (209), `_score_one_complement` (39),
`protein_completeness` (39), and the rest held steady throughout,
confirming nothing else was touched. `get_density_g_per_ml`: 53→13 (40
killed, 75% reduction — the best per-test yield of any function tackled
this session, reflecting how much of it had literally never been
exercised before).

**Still open.** `get_density_g_per_ml()`'s remaining 13 are mostly the
equivalent-mutant/dead-default classes described above — not worth
chasing further without a different technique.
`suggest_complements()`'s 209 survivors (round 3 above) remain the
largest pool in the file, now spread across smaller pockets.

## Done (2026-09-10, continued) — #5, suggest_complements, round 4 (the
## _build_pairs concentration — a worked example of "how do we know when
## to stop")

At the user's request to keep going, but with a real, well-posed
question attached: *"we can afford it, and not doing it leaves things
unknown — but I don't have the experience to judge whether to continue."*
Rather than guess, this round answered that with evidence: three
sampling-and-fix cycles, each checking whether the remaining survivor
pool was genuinely scattered (safe to stop) or hiding another
concentration (worth another pass) — the same question round 3 above
first raised when it found `diaas_improvers`.

**Pass 1 (reconnaissance, no fixes).** Sampled a spread of 21 of the 209
remaining survivors. Result: 9 of 21 (43%) clustered in one specific
region — `_build_pairs()`'s own candidate-pool construction
(`all_candidates_ordered`) and its A/B leg field-resolution logic.
Extrapolated and confirmed by ID range: **101 of 209 (48%)** of all
survivors sat in that one code region. This is a genuine second
concentration, on par with `diaas_improvers` by raw count — exactly the
kind of thing that wouldn't have been visible without sampling.

**Pass 2 (fix + verify).** 9 new tests targeting that region, in
`tests/test_usda.py`'s `TestComplementPairs` and `TestDiaasImprovers`
classes:
- **`_pooled_diaas()`'s paired-AA accumulation** (`comp_aa += ...`) had a
  survived `+=`→`-=` mutation — every existing `diaas_improvers` test
  used a candidate with cystine/tyrosine zeroed out, masking it entirely.
  New test splits the same total Met+Cys ratio across both keys instead
  of putting it all on methionine and confirms the result is identical
  either way (proving addition, not subtraction, is really happening).
- **`max_improver_grams` silently dropped** from the internal
  `_diaas_improver_score()` call — always fell back to that function's
  own default (300) regardless of the caller's actual value. Real,
  user-visible: the docstring promises 120 for meal/food/daily contexts
  vs. 300 for recipe contexts.
- **A pantry candidate's own `diaas` silently discarded** on the
  curated-table-fallback path, in two places with two different broken
  forms (`cand_d = None` outright, and `cand_d = cand_d and entry["diaas"]`
  — an inverted `and`/`or` that replaces a real value with the curated
  table's generic one instead of preserving it).
- **`recipe_id`/`fdc_id`/`serving_weight_g`/`diaas` dict-key-literal
  mutations** on both pair legs — `_build_pairs()` re-extracts these
  fields from its own separate candidate-pool dict, a genuinely distinct
  code path from `_build_suggestions()`'s identically-named extraction
  (already covered elsewhere), with its own separate survived mutations.
  Closed for leg A specifically (a Brazil-nuts-profile clone guaranteed
  to land in the A position) since the existing pairs tests' controlled
  candidates only ever landed as leg B.
- **`diet_pref`'s default-value comparison** — round 3's earlier fix for
  this used an *empty* pantry, so the `if diet_pref != "all":` filtering
  branch was never actually exercised (filtering nothing is a no-op
  regardless of the mutant). Fixed with a non-empty pantry candidate.

Verification: 209 → 141 (68 killed — far more than the ~10 explicitly
targeted, from broad knock-on kills via the cross-check-style
assertions).

**Pass 3 (re-sample, confirm or find more).** Re-sampled the same
`_build_pairs` region: concentration dropped 48% → **38%** (53 of 141).
Still elevated, so sampled again rather than assuming it was done.
Found two more real, distinct bugs:
- **`continue`→`break`** in the `general_candidates` construction loop's
  cache-exclusion check — since it iterates the ~25-entry curated table
  in a *fixed order*, breaking on the first excluded cache-matched entry
  would silently drop every curated suggestion that comes after it too.
  A genuinely serious, user-visible bug: excluding any one cache-matched
  food could have wiped out most of the "general" suggestions tier
  entirely. New test excludes a cache match for "Lentils, cooked" (first
  in the table) and confirms entries near the end of the table
  ("Chickpeas, cooked", "Salmon, cooked") still appear.
- **`b_dig`'s "assume fully digestible when diaas is unknown" fallback**
  silently became 2.0 instead of 1.0 for leg B specifically (leg A's
  identical fallback was already covered) — no existing pairs test ever
  had a leg B candidate whose true `diaas` resolved to `None` (every
  curated-table candidate carries a real value).

2 more tests. Verification: 141 → **117** (24 killed). Re-sampled a third
time: concentration in the same region down to **27%** (32 of 120 before
this last fix) — converging toward the region's actual share of the
function's total line count, i.e. genuinely resolved to baseline scatter
rather than a hidden concentration. The remaining handful of real bugs
found in this last sample (a step-acceptance `and`→`or`, a `continue`→
`break` on `total_grams > 600` requiring two near-500g-cap candidates to
construct) are real but meaningfully harder to construct without
fragility, and were left open rather than forced.

**Verification, full round:** full suite **919 tests** (was 892). Zero
regressions across all three verification passes. `_score_one_complement`
(39), `get_density_g_per_ml` (13), `protein_completeness` (39), and the
rest held steady, confirming nothing else was touched — plus a bonus:
`_find_complement_by_name`'s 2 survivors were incidentally killed too
(the excluded-cache-candidate test exercises it directly).

**The answer to the user's original question, made concrete:** two full
sampling passes each found a genuine, sizeable concentration (48%, then
38%) that would NOT have been visible without actually sampling —
confirming the worry that "stopping early leaves real unknowns" was
well-founded, not just cautious instinct. The third pass found the
concentration had converged to baseline (27%, trending toward the
region's proportional share) — confirming the *opposite* worry, that
there's always "just one more" finding, is not automatically true either.
Mutation testing is not a "finish once" task (see the existing quarterly
rotation cadence in README-numa-documentation.md's Maintenance section)
— but *this specific thread*, on *this specific function*, has now been
checked by actual evidence rather than a guess, twice, and both times the
concentration was real, found, and fixed. A reasonable stopping point for
this thread specifically.

**Still open.** `suggest_complements()`: 117 survivors remaining (down
from 394 at the start of round 3, a 70% reduction; down from ~948 at the
very start of this whole mutation-testing deep-dive — combined with every
other function touched this session, well over 85% down session-wide).
Scattered across small pockets with no further concentration detected by
sampling. `_score_one_complement()` (39) and `get_density_g_per_ml` (13)
similarly scattered/low-value. No further mutation-testing rounds
recommended for this thread without a new technique or a fresh target
(rotation group 2 — the untouched data-source-parsing files — is the
next natural candidate, per the existing rotation plan below, whenever
this work resumes).

## Done (2026-09-11) — #3, cross-source data plausibility: source-fidelity
## fixtures, and three real live parsing bugs they surfaced immediately

Picked up right where the 2026-09-10 handoff left off: the user ran
`scripts/record_source_fixtures.py` themselves (real USDA key + live
network, exactly as documented) and handed the resulting fixture files
back. Before writing the planned sanity test, actually looked at what got
recorded — and found the fixture-recording step itself had already done
its job better than expected, surfacing three real, live, previously-
unknown parsing bugs on the very first run:

- **USDA: some Branded records return foodNutrients items with no
  identifiable nutrient id at all.** `get_food_detail()`'s full-format
  endpoint normally returns items shaped `{"nutrient": {"id": ...}, ...}`;
  for several private-label Branded records (confirmed live: all three
  recorded USDA queries — "chicken breast", "lentils", "salmon" —
  happened to match exactly this kind), the full-format endpoint instead
  returns `{"type": "FoodNutrient", "id": <opaque row id>, "amount": ...}`
  — no `nutrient.id`/`nutrientId` the existing parser could use. Real
  nutrient data existed (protein, fat, etc. all present with real values)
  but silently became an empty `nutrients: {}`. The `format=abridged`
  variant of the *same* endpoint, for the *same* fdcId, does carry a
  `number` field the parser already knows how to read (`NUTRIENT_NUMBER_MAP`)
  — so `usda_api.get_food_detail()` now retries with `format=abridged` and
  merges in its nutrients whenever the primary parse comes back empty
  despite real `foodNutrients` rows being present, while still using the
  full-format response for everything else (portions, brand — abridged
  lacks `foodPortions` entirely). 3 new tests,
  `TestGetFoodDetailAbridgedFallback` in `tests/test_usda.py`.
- **CNF: nutrient resolution was completely broken — every single CNF
  food lookup, unconditionally, returned zero nutrients.** `get_food_detail()`
  read `entry.get("nutrient_symbol")` off each `/nutrientamount/` response
  item, but the live endpoint's items only ever carry a numeric
  `nutrient_name_id`, never a `nutrient_symbol` field — confirmed this was
  true for every one of the 104 nutrient rows checked, not an edge case.
  The existing test suite never caught this because its mocked
  `_http_get` response used the *documented-but-wrong* `nutrient_symbol`
  shape, matching the code instead of the real API. The actual id→symbol
  mapping lives in a separate, small (~150-row), static reference table
  at `/nutrientname/?type=json` — `cnf_api.py` now fetches and caches that
  once per process (`_nutrient_symbols()`, mirroring the existing
  `_food_list_cache` pattern) and joins through it. This is the most
  severe of the three findings: it means CNF-sourced foods have likely
  been silently contributing zero nutrition data throughout, for as long
  as this bug existed — worth being aware of if anyone's nutrient records
  for CNF-matched foods look suspiciously sparse. 3 new tests in
  `tests/test_cnf.py` (`test_resolves_via_nutrient_name_id_not_a_symbol_field`,
  a fetched-once check, an unmapped-id-ignored check), plus the existing
  `TestGetFoodDetail`/`TestGetFoodDetailById` tests' mocks corrected to
  the real two-endpoint shape (they'd been passing against the same wrong
  assumption the production code made).
- **Open Food Facts: a straightforward key-name typo.** `carbohydrates_100g`
  was mapped to `"carb_g"` instead of the canonical `"carbs_g"` used
  everywhere else in the app (`usda_api.NUTRIENT_MAP`, `cnf_api.py`,
  CLAUDE.md's documented Nutrients Dict) — every OFF-sourced food's carb
  value has been silently unreadable by the rest of the app (RDA
  comparisons, nutrient displays, etc. would show it as missing/zero).
  One-line fix in `openfoodfacts.py`. `openfoodfacts.py` had zero unit
  test coverage of any kind before this — new `tests/test_openfoodfacts.py`
  (4 tests) pins every mapped key to its canonical name specifically so a
  typo like this fails immediately next time, plus basic parse/error-path
  coverage.

All fixtures re-recorded after each fix to confirm live: USDA fixtures
now carry real nutrient data (10 keys each, previously 0); CNF fixtures
now carry a full panel including amino acids (39-44 keys each, previously
0); OFF fixtures show `carbs_g` correctly. (One OFF query, "oat milk",
hit a persistent rate-limit during re-recording — its one previously-
recorded `carb_g` field was corrected by hand instead, since the fix's
correctness was already independently confirmed twice on other OFF
foods in the same run.)

**Then, the originally-planned test:** `tests/test_source_fixtures.py` (37
tests via `pytest.mark.parametrize` over every fixture file) — no negative
nutrient values, a non-empty parsed `nutrients` dict, `protein_g` present,
essential-AA total never exceeding `protein_g` (USDA+CNF), and
`has_amino_acid_data()` returning `True` on **CNF** samples specifically
(not USDA — live confirmation this run: USDA's default search includes
Branded products, whose nutrition labels never carry amino acids, and
generic-named branded items often outrank the true Foundation entry for a
query like "chicken breast"; asserting AA-data-required there would fail
on legitimate expected results, not catch a real bug).

**Verification:** full suite **966 tests** (was 919). Zero regressions.
This closes item #3's "source-fidelity fixtures" half entirely — the
one-time setup, the recording, and the sanity test are all done and
wired together. Re-running this quarterly (per README-numa-documentation.md's
"Quarterly source-fixture refresh" section) is now just: you re-run
`scripts/record_source_fixtures.py`, then `pytest` — if a source has
changed shape again, `test_source_fixtures.py` is what will now catch it,
the same way today's manual read of the fixture files caught these three
by hand.

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
  above) — DONE 2026-09-11**, including `tests/test_source_fixtures.py`,
  and three real live parsing bugs it surfaced and fixed on the very
  first real run (one of them — CNF nutrient resolution being completely
  broken, 100% of lookups — the most severe finding of this whole effort).
  See "Done (2026-09-11) — #3" above for the full writeup. Nothing further
  planned here beyond the normal quarterly re-run cadence.
- **Estimation-path coverage (CoFID, CIQUAL, most OFF)** — this part is
  actually already covered by the `/copy-aa` route tests added above, since
  those are exactly the sources with no native AA data. Nothing further
  needed here unless new gaps turn up.

### 2. Lower priority, unchanged from the original plan

- **#4 — narrow Playwright E2E, fully done 2026-09-10, CI wiring also done
  2026-09-10** — all three original candidate routes covered: `/food/search`,
  `/food/analyze-portion`, and `/meal/{meal_id}/search-api-results`.
  Deliberately not wired into `tests.yml`'s per-push job (would add real
  minutes to every push and a different flakiness profile to a currently
  100%-reliable fast check) — instead a new, separate
  `.github/workflows/e2e-tests.yml` runs `pytest -m e2e` on a weekly
  schedule (Saturdays 06:00 UTC, same day as the manual weekly sweep, though
  independent of it) plus on-demand via `workflow_dispatch` ("Run workflow"
  in the Actions tab). **#4 is now fully closed, nothing further planned.**
- **#5 — mutation testing.** Pilot (`diaas.py`), rotation group 1 (core
  nutrient math), and a six-round deep-dive into group 1's biggest
  finding all done 2026-09-10 — see above for the full writeup. Real gaps
  found and fixed: `pooled_tid()`, `atomic_recipe_ingredients()`,
  `compute_rda()`'s age boundaries, `rename_profile()`/`delete_profile()`/
  `get_profile_file()`, `_score_one_complement()`'s `predicted_diaas`
  formula and `denom==0` boundary, `suggest_complements()`'s primary-gap
  sort order, `_grad_steps()`'s inverted fallback condition, `exact_dcp()`'s
  inverted return, `load_cache_candidates()`'s `break`/`continue` bug and
  `"diaas"` field, `aa_effects()`'s `"label"`/`"met"`/`"before"` fields,
  `two_step_combo()`'s step1, step2, `exclude_names` handling, AND
  `aa_effects_limit` passthrough, `_dcp_at_frac()`'s weighted-pool formula,
  `has_estimate_or_generic`'s neutered `"estimated"` check, the
  `"gap_effect"` AND `"grams"`/`"diaas_sort=grams"` sort modes' silently
  broken sort keys (three separate instances of the same stable-sort-
  masking bug pattern), and the pairs tier's `total_dig_complete`
  multiply/divide bug. Cadence agreed and wired into
  README-numa-documentation.md's Maintenance section (weekly churn-check
  block + rotation log). The earlier "mutmut aggregate-count anomaly" is
  now understood well enough to act on (see above) — not fully root-caused,
  but resolved practically: sample and verify by mutant ID, don't trust
  the aggregate total from a single run. **Two techniques discovered,
  both dramatically more efficient than one-test-per-mutant sampling:**
  (1, round 4) a comprehensive "every field of one function's output,
  hand-computed" test — first use dropped `build_complement_display` from
  675 to 428 in one step; reused against `two_step_combo`'s step1/step2/
  `_dcp_at_frac` in round 5, its single biggest-drop round (93→64). (2,
  round 6) systematically providing a real `ingredients` list to close the
  previously-untested per-ingredient `exact_dcp()` recompute path — every
  test through round 5 used `ingredients=None`; 4 new tests (one per call
  site: `_fmt`, `_grad_steps`, `two_step_combo` step1, `_fmt_pair`) each
  cross-checked against an independent direct `exact_dcp()` call,
  confirming correct wiring (no new bugs found, but a real dimension
  closed rather than left unknown). `two_step_combo`'s step2 `b_dcp` with
  real ingredients remains unexplored — extracting a curated-table
  winner's real `comp_nutrients` for an independent cross-check proved
  more involved than the other three call sites. **Still open, in
  priority order:**
  1. `build_complement_display()` (341 survivors) and `two_step_combo()`
     (51) remain the overwhelming majority of `complements.py`'s
     survivors — sampled across seven rounds now (down from the original
     ~948, a 59% reduction), still not systematically worked through start
     to finish, and diminishing returns are visibly setting in — though
     real bugs are still turning up most rounds, so not exhausted. Round
     7 closed both concrete next steps named after round 6: (a)
     `two_step_combo`'s step2 `b_dcp` with real ingredients; (b) the
     comprehensive-field-test technique applied to `_total_dig()`'s scale
     branch and the `new_complete` top-of-tier promotion invariant. The
     sort-key lambdas' exact tie-break values are the main remaining
     candidate for that technique.
  2. `suggest_complements()` closed heavily across rounds 3-4 above:
     394→209→117 (70% total reduction), headlined by two genuine
     concentrations found by actually sampling rather than guessing — the
     entire zero-coverage `diaas_improvers` tier (round 3) and
     `_build_pairs()`'s candidate-pool/leg-resolution logic (round 4,
     found via 48%→38%→27% concentration sampling across three cycles).
     Real bugs fixed along the way: `diet_pref`/`exclude_names` filtering,
     two `continue`→`break` logic bugs (one in the pairs cascade, one in
     `general_candidates` construction that could've silently hidden most
     of the "general" suggestions tier), several dict-key-identity checks,
     and a `+=`→`-=` paired-AA bug in the pooled-DIAAS formula. Its
     remaining 117 are now confirmed (by re-sampling) to be genuine
     scattered/low-value noise — no further concentration detected.
     `_score_one_complement()` closed further in round 2
     (57→39, 10 more real bugs fixed); its remaining 39 are dead-default
     `.get()` noise plus two known-unresolved gaps (the
     `base_digestibility` kwarg silently not reaching the internal
     `protein_completeness()` call, and the `target_still_gapped = None`
     mutant needing a fragile rounding-boundary construction — see the
     `NOTE:` comment in `tests/test_usda.py`).
     `get_density_g_per_ml()` closed 53→13 (75% reduction — the best
     per-test yield of any function this session), the entire USDA-portion
     parsing fallback having previously been almost completely untested.
     Its remaining 13 are equivalent-mutant/dead-default classes, not
     worth chasing further. **This whole `usda_nutrients.py`/`complements.py`
     thread is now at a reasonable stopping point** — not because it's
     "finished" (it never fully is; see the quarterly rotation cadence
     below) but because two independent sampling passes confirmed no
     further concentrated blind spot remains undetected.
  3. Rotation group 2 (data-source parsing: `usda_api.py`,
     `openfoodfacts.py`, `cnf_api.py`, the CoFID/AFCD/CIQUAL lookups,
     `food_import.py`, `csv_import.py`/`csv_export.py`, `recipe_csv.py`)
     — not yet run at all.
  4. Rotation groups 3-4 (web-layer glue, everything else) — normal
     quarterly pace, no pre-release urgency.

The original "#5 queued behind #1" sequencing no longer holds — #5's pilot
ran ahead of #1 on 2026-09-10, once it became clear #5 had no dependency on
#1 and #1 was blocked on your key/network anyway. Both are now independent,
parallel open items: #1 waiting on you, #5 waiting on the next rotation
chunk (either can be picked up first). (#2 and #4 are both fully done,
above.)

~~Run the real, full suite once~~ — done, repeatedly: `pytest -q` has been
run clean, locally, in every session since 2026-08-28, and `tests.yml` has
been running it on every push/PR the whole time. No longer worth listing as
a distinct step.

## Handoff notes for the next mutation-testing round (target: 2026-12-05)

Written 2026-09-10 at the end of a very long single-session deep-dive, for
whoever (or whichever Claude session) picks this back up in ~3 months. The
session that wrote this closed rotation group 1 (core nutrient math) far
more deeply than a normal quarterly pass — don't expect future rounds to
run this long; this was unusually thorough because the user kept saying
"keep going" and it kept finding real things. Next time, a normal-scope
quarterly pass is fine.

**What's done, what's not:**
- Rotation group 1 (`diaas.py`, `usda_nutrients.py`, `profile.py`,
  `numa_app/services/complements.py`, `aa_estimate.py`,
  `recipe_nutrients.py`, `glycemic_load.py`, `rda_status.py`) — deeply
  worked. See README-numa-documentation.md's rotation-log table for a
  one-line summary per module, and the many "Done (2026-09-10, continued)"
  sections above for the full detail. `glycemic_load.py` and
  `rda_status.py` were only screened (zero-coverage + safety-critical
  triage), not fully characterized — if group 1 comes up for its next
  quarterly check, those two are the least-explored and worth a proper
  look before re-treading the heavily-worked functions above them.
- **Rotation group 2 (data-source parsing) has never been run at all** —
  `usda_api.py`, `openfoodfacts.py`, `cnf_api.py`, the CoFID/AFCD/CIQUAL
  lookups, `food_import.py`, `csv_import.py`/`csv_export.py`,
  `recipe_csv.py`. This is the natural next target when this cadence comes
  up — either because it's genuinely due (calendar floor) or because the
  weekly churn check flags real changes there. Start here rather than
  re-visiting group 1 unless the weekly churn check specifically flags a
  group-1 module.
- Rotation groups 3-4 (web-layer glue, everything else) — untouched,
  normal quarterly pace, no urgency.

**Practical lessons, so the next round doesn't re-learn them the hard
way:**
- **Scope `setup.cfg`'s `[mutmut]` section to ONE source file at a time**,
  not a whole rotation group at once. Mutating multiple files in the same
  run inflates apparent survivor counts for any function that calls into
  another mutated file (confirmed twice this session — `complements.py`'s
  true counts were 4-6x lower once isolated from `usda_nutrients.py`).
  `also_copy` needs the *unmutated* real versions of anything the target
  file (or its test selection's `conftest.py`) imports — for anything
  under `numa_app/services/`, that means both `__init__.py` files at
  minimum, plus whatever sibling modules it actually imports. A "no
  tests" result on 5 of 7 modules in one run turned out to be exactly
  this bug, not a real finding — always sanity-check a too-good/too-bad
  "no tests" result against whether the module even imports cleanly
  inside `mutants/` before reporting it.
- **Memory and `/tmp` hygiene, every time, not just once:** this machine
  runs tight under normal desktop load. Always `--max-children 2`. Check
  `free -h` before starting and `df -h /tmp` periodically during a long
  session — pytest subprocesses spawned by `mutmut` each get their own
  `/tmp/pytest-N` scratch dir that never gets cleaned up across siblings,
  and `/tmp` is a RAM-backed tmpfs, so it silently eats memory *and* can
  fill disk outright (`sqlite3.OperationalError: database or disk is
  full` happened once this session). Fix: `rm -rf /tmp/pytest-of-tomc`
  before/during any long run — always safe, those are ended-session
  scratch dirs. A `mutmut run` on a real-sized file (1000-1500 mutants)
  takes several minutes — always run it with `run_in_background`, never
  foreground.
- **`mutmut`'s results database lives inside `mutants/`** — deleting that
  directory (the standard cleanup step after each run) also deletes the
  ability to `mutmut show <id>` or re-query `mutmut results` for anything
  from that run. If you want to sample survivor diffs, do it *before*
  cleaning up, or budget time to `mutmut run` again first.
- **The sampling-for-concentration technique** (new this session, proved
  itself twice — see round 4/5 above for `_build_pairs`): don't assume a
  large survivor count is "just scattered noise." Sample a spread of
  ~20 survivor IDs (evenly across the full ID range, not just the first
  20), read each `mutmut show <id>` diff, and check whether they cluster
  in one code region. If a meaningful fraction (40%+) cluster together,
  that's very likely a real, previously-unexercised chunk of the function
  (a whole closure, a whole code path) — worth a dedicated pass, not just
  one-off fixes. After fixing, re-sample rather than assuming it's done;
  this session needed three rounds (48%→38%→27%) before the concentration
  was confirmed resolved to baseline scatter. Don't stop after one
  fix-and-hope pass on a large survivor count without at least one
  reconnaissance sample first.
- **Two other techniques worth reusing**, both discovered this session and
  dramatically more efficient than one-test-per-mutant sampling:
  1. **Comprehensive whole-dict field tests** — one test that asserts on
     *every* field of a function's output at once, from one fully
     hand-computed input, kills dozens of scattered dict-key-literal and
     default-value mutations in a single pass (first use dropped one
     function's survivor count by 40% in one step).
  2. **Defeat "tested only at the default" masking** — when a function
     takes a parameter like `digestibility=1.0` or `ingredients=None` and
     every existing test either omits it or passes the default, any bug
     in the code path that only matters at a *non-default* value is
     invisible. This pattern recurred at least four separate times this
     session (digestibility divide/multiply bugs, an `ingredients`-list
     recompute path, `cand_diaas=None` fallback defaults) — when a
     function has an optional parameter with a "usually 1.0/None/all"
     default, deliberately write at least one test that supplies a real,
     non-default value and checks an exact dependent result.
- **Independently reimplementing a documented formula** is the right
  technique for testing a closure with no direct entry point (like
  `_diaas_improver_score()`, only reachable through
  `suggest_complements()`'s output) — read the function's own docstring
  formula, reimplement it standalone in the test using the same real
  constants/lookups the function itself uses, and cross-check every
  output field against it. Caught the single biggest finding of the
  whole session this way (an entire ~95-line closure with zero coverage).
- **A category of mutant isn't worth chasing**: dead-default `.get(key,
  X)` mutations where the key is always present in real data (common
  when a dict is built by the app itself, not user input), and string-
  literal mutations on lookup keywords that happen to still match as a
  substring after mutation (`"tablespoon"` still matches inside
  `"XXtablespoonXX"`). Both showed up repeatedly this session; don't
  spend time constructing sparse-dict tests to chase them.

## Quick-start for next session

1. Re-read this file (the "Done (2026-09-10)" section above, specifically —
   #4 is now fully closed, including CI wiring; #2 was already fully closed
   as of 2026-09-09).
2. Confirm CI is green on the latest push (GitHub Actions tab) — both
   `tests.yml` (every push) and, once it's had a chance to run on its
   Saturday schedule or been triggered manually, `e2e-tests.yml`.
3. **Done 2026-09-11** — item #3's fixture-recording step (needed your real
   USDA API key + live network) ran, and `tests/test_source_fixtures.py`
   is written and passing. See "Done (2026-09-11) — #3" above — this also
   found and fixed three real live parsing bugs (USDA Branded-record
   nutrients, CNF nutrient resolution being completely broken, an OFF
   key-name typo), not just closed the checklist item.
4. #3 and #4 both have nothing left. #5 remains open, not urgent — see the
   "Handoff notes for the next mutation-testing round" section above
   (target ~2026-12-05; next real step there is **rotation group 2**,
   data-source parsing, never run). No blocking open item remains before
   moving to the Windows port, which is where this session is headed next.
5. On memory: this machine runs tight on RAM under normal desktop load
   (Firefox/Obsidian/VSCodium). A `mutmut run` across a rotation group hit
   OOM twice before succeeding with `--max-children 2` after a reboot —
   check `free -h` first, use `--max-children 2`, and expect to need
   `run_in_background` (a multi-thousand-mutant run exceeds a normal
   command timeout). Also check `df -h /tmp` and `rm -rf /tmp/pytest-of-tomc`
   — see the handoff section above for why.
6. `[mutmut]` in `setup.cfg` currently points at `usda_nutrients.py` alone
   (this session's last-used scope) — edit it to point at whichever
   module(s) run next. **Scope to one source file at a time**, not a whole
   rotation group at once (cross-file mutation inflates apparent survivor
   counts — confirmed twice this session). If touching anything under
   `numa_app/services/`, make sure `also_copy` includes both `__init__.py`
   files plus any sibling module it imports — see the "false-alarm
   scoping bug" note above for exactly what tripped this up last time.
