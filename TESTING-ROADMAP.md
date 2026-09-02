# NutriMagnus testing elevation — status and next steps

Started 2026-08-28 in a Cowork session (with the VSCodium Claude extension
handling the doc updates). This file is the handoff point for picking the
work back up. Test suite is at 731 tests as of the last manual update
(user-manual.md Part 2E, "Extensive code testing").

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

## Not done — pick up here

### 1. #2, the harder half: property tests against the suggestion-ranking engine

Not started. This is `numa_app/services/complements.py`
(`two_step_combo()`, `build_complement_display()`) and
`usda_nutrients.py`'s `get_aa_gaps()` (line ~143) and `suggest_complements()`
(line ~731, the biggest function in the codebase — not yet read in full).
This is deliberately the harder half: it needed more read-and-verify time
than was available in one sitting, and shipping unverified property tests
against logic this central would be worse than not shipping them.

Candidate invariants to test, once `suggest_complements()` is actually read:
- **Monotonicity**: increasing a suggested gap-closer's grams never
  decreases the resulting pooled DIAAS, up to full completion.
- **Suggestion self-consistency**: whatever grams `build_complement_display()`
  proposes to "close all gaps," feeding that amount back through
  `diaas.meal_level_diaas()` actually clears the FAO floor it claims to
  clear (this is the same idea as `complements.py`'s own `exact_dcp()`
  helper — may be able to reuse it directly in the test).
- Ranking stability: the promoted-to-top "full profile completer" rule
  (serving size ≤ 50g) behaves correctly across generated inputs, not just
  the hand-picked cases in `tests/test_complements.py`.

Start by reading `usda_nutrients.py` lines ~700-950 (`suggest_complements`
and whatever it calls) before writing anything.

### 2. #3, the rest: cross-source data plausibility

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

### 3. Run the real, full suite once

Nothing in this session ever ran your actual 712→731-test suite in full —
verification happened in a reconstructed scratch copy (the device shell was
down all of 2026-08-28). Now that `tests.yml` is pushed, the next push/PR
will run it for real in CI; also worth running `pytest -q` locally once just
to see a clean full pass with your own eyes.

### 4. Lower priority, unchanged from the original plan

- **#4 — narrow Playwright E2E** for the JS-driven async handoff routes
  (`search-api-results` and similar).
- **#5 — mutation testing** to check whether the suite actually catches
  deliberate breaks.

Both still queued behind #2 (remainder) and #3 (remainder) per the original
sequencing — no new information changes that ordering.

## Quick-start for tomorrow

1. Re-read this file.
2. Confirm CI is green on the latest push (GitHub Actions tab).
3. Open `usda_nutrients.py` around `suggest_complements()` (line ~731) —
   that's the reading needed before #2's remainder can be written.
4. Open `afcd_lookup.py`, `ciqual_lookup.py`, `cofid_lookup.py` to confirm
   the "static JSON, not live API" correction above before touching #3.
