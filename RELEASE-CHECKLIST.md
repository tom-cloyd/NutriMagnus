# NutriMagnus Linux Release — Sequenced Checklist

Generated 2026-08-07 from a review of recent Claude chat sessions plus a direct check
of the repo's current state (git remote, Makefile, scripts, manual). Work through
phases in order — later phases assume earlier ones are done.

Two corrections to keep in mind while reading old chat sessions:
- The program is **NutriMagnus** ("NuMa"), not NutraMagnus.
- It moved off Codeberg to **GitHub** on 2026-08-05 (Codeberg's ToS bans AI-majority-authored
  code — a real risk given the commit history). All release tooling now targets
  `github.com/tom-cloyd/NutriMagnus`. Older chat sessions that mention Codeberg,
  `.forgejo/workflows/`, or `program-updates.md` are superseded — treat them as history only.

---

## Phase 0 — Repo hygiene (5 min, do first)

- [x] Delete the stale `.forgejo/workflows/release.yml` — it's still tracked in git
      (`git ls-files .forgejo/`) even though the project no longer uses Codeberg Actions.
      Leaving it risks confusion about which workflow is authoritative.
- [x] `git status` — confirm a clean tree before starting (uncommitted files have
      silently accumulated between sessions before).

## Phase 1 — Content prerequisites (blocking, not yet done)

- [x] **Curate more starter data.** Done 2026-08-10 — starred 4 real recipes in the live
      app (`*Mexican coffee - Tom's`, `*Pinto-quinoa meal`, `*Marinara pasta sauce - quick,
      from cans`, `*Chickpea-quinoa meal`; note these were typed without the space after
      `*` — `export_starter_data.py`/`refresh_starter_data.py` were updated to accept
      `*Foo` as well as `* Foo`, normalizing to the canonical `"* "` form on export) and
      ran:
      ```bash
      python scripts/export_starter_data.py
      ```
      which auto-included their 22 non-starred ingredient foods. `starter_data.json` now
      has 23 foods, 0 pantry items, 4 recipes — replaces the old placeholder 9/6/2 set entirely
      (export is a full rebuild from whatever's currently starred, not additive). One data
      gap surfaced: `* Marinara pasta sauce - quick, from cans` uses two branded foods
      ("TOMATO SAUCE", "TOMATO PASTE") with no amino acid data, so that recipe's DCP
      legitimately computes as unavailable rather than guessed — not blocking,
      `tests/test_demo_data.py` was updated to expect this instead of assuming every demo
      recipe has a DCP.
- [x] **Appendix J / DIAAS golden-value regression test.** Done 2026-08-07 —
      `TestGoldenValuePintoQuinoaMeal` in `tests/test_diaas.py` runs the real pinto
      beans + quinoa meal (FDC 173796/168917) through `meal_level_diaas()` and checks
      every IAA ratio against Appendix K's Table I-7. Also caught and fixed a stale DCP
      figure in Appendix K itself (see today's manual changelog entry).

## Phase 2 — Build & local verification

- [x] **Refresh starter data against your current cache:**
      ```bash
      python scripts/refresh_starter_data.py
      ```
      Catches up any edits made to already-exported starter foods/recipes (corrected
      portion, tweaked instructions, renamed item, added ingredient) without needing to
      re-star anything. Matches by stable ID (fdc_id / source_recipe_id), not name, so a
      rename doesn't break the match. Never removes an entry — anything with no live
      match is left untouched. Complements (doesn't replace) Phase 1's
      `export_starter_data.py`, which picks up brand-new `"* "`-starred content; run
      that first if you starred anything new, then this to sync the rest.
      Done 2026-08-10 — ran right after the export, correctly reported 0 changes
      (nothing to sync yet).
- [x] `make build` — regenerates the manual HTML, then runs PyInstaller against
      `nutrimagnus.spec` (packages `web/launcher.py` only — the CLI was removed
      2026-08-04, so this is now web-only). Done 2026-08-10 — succeeded, `dist/nutrimagnus`
      built cleanly.
- [x] Run the full test suite from the venv and confirm it's green (CI does this too,
      but check locally first). Done 2026-08-10 — 533 passed.
- [x] Smoke-test `dist/nutrimagnus` locally:
      ```bash
      HOME=$(mktemp -d) ./dist/nutrimagnus
      ```
      Confirms a fresh install seeds starter data correctly and doesn't leak your
      personal DB (this exact check was already done once, 2026-08-05 — repeat after
      the Phase 1 data changes). Done 2026-08-10 in an isolated `$HOME` — fresh DB seeded
      23 foods / 4 recipes / 0 pantry items as expected, `GET /` and static assets returned
      200, no personal data touched, temp dir discarded after.

## Phase 3 — Cut the actual release (the real blocker)

Nothing has run this end-to-end yet — `user-manual.md` (Part 1, Section C) says so
explicitly: "Not yet verified against a real cut release."

- [ ] Set `GITHUB_TOKEN` (personal access token, repo write scope) in your environment.
- [ ] `make push-release` (= `git push origin main` + `make release-linux`, which builds
      and runs `scripts/create_release.py`). This tags from `version.py` (currently
      `2026-08-07:1142`), uploads three assets — `nutrimagnus`, `nutrimagnus.png`,
      `install-linux.sh` — and pulls release notes from `user-manual.md` Appendix A's
      entry for today's date.
- [ ] Alternatively, trigger `.github/workflows/release.yml` by hand from the GitHub
      Actions tab (`workflow_dispatch` — it will never fire on a plain push, by design).
- [ ] **On a genuinely clean machine/account** (not one with `~/.local/bin/nutrimagnus`
      already present from dev use), run:
      ```bash
      curl -fL https://github.com/tom-cloyd/NutriMagnus/releases/latest/download/install-linux.sh | bash
      ```
      Confirm: binary lands in `~/.local/bin`, icon in `~/.local/share/icons`, `.desktop`
      entry appears, and — the one thing no session confirms doing — actually find
      "NutriMagnus" in a real GNOME/KDE applications menu, not just check the files exist.
- [ ] Click-launch it from that menu entry and confirm it opens a browser tab cleanly.

## Phase 4 — Manual finalization

- [ ] Once Phase 3 succeeds, rewrite `user-manual.md` Part 1, Section C (lines ~53-76)
      from planning language into plain present-tense instructions — delete the italic
      "*being drafted ahead of...*" preamble and the "What still has to be built"
      engineering checklist (items 1-4 are done; item 5 is the Windows follow-on, moves
      to its own future task).
- [ ] Reconcile `README.md` (line ~41) — it currently reads as if a working Linux
      release already exists ("Download the latest release from the Releases page").
      Leave as-is if Phase 3 succeeds; otherwise soften until it's true.

## Phase 5 — Optional polish (non-blocking)

- [ ] Swap the placeholder icon (`web/static/icon-256.png`, a green "N" monogram) for
      real branding whenever ready — no code changes needed elsewhere, the installer
      just downloads whatever's at that release-asset name.
- [ ] CSV export/import for food/recipe data — logged in the manual's Part 9 as a
      future idea, not this release.

## Deferred, not part of this release

- Windows build/installer (Phase 4's item 5) — explicitly waits until Linux is proven
  end-to-end.
- The update-check-against-latest-release feature floated in earlier chats — never got
  built; not blocking.
