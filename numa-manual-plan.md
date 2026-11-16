# NutriMagnus User Manual — Revision Plan

_Drafted 2026-11-14; decisions recorded the same day (section 8). Status 2026-11-14 (evening): all steps done; see section 9 for what was deliberately left as written._

## 1. What the manual is now

`user-manual.md` is 7,461 lines and about **135,000 words**, roughly 9 hours of reading. That is about 15 times the size of cmgr's manual. By Part:

| Part | Words | What it holds |
|---|---:|---|
| Preface: How to read | 170 | |
| 1. Quick start | 4,800 | install, backups, tips, first setup, "skim Part 2", "consider Part 4" |
| 2. Introduction | 3,300 | what NuMa does, the protein problem, trust/validation, a pointer to workflows |
| 3. Using NuMa | 12,600 | home page, navigation, **4 workflows**, menu by menu (short), settings |
| 4. Core nutrition concepts | **28,700** | 27 sections, A through AA |
| 5. Reading your results | **20,300** | getting help, then every table's column guide, What-if, history, search results |
| 6. Shared operations | 15,100 | targets, diet, search ranking, editing consequences, custom foods, data checks, amounts, CSV |
| 7. Essential resources | 7,800 | food data sources, glossary, internet links, how to use the manual |
| 8. Troubleshooting | 4,600 | by symptom |
| 9. Possible features | 2,200 | future ideas plus a list of features already done |
| 10. Appendices | 15,400 | protein-quality primer, plant proteins, GL vs CGM, DIAAS-only foods, worked validation, nutrient key |
| 11. Updates log | **12,800** | dated change entries, some with code identifiers |
| Notes (footnotes) | 6,400 | citations, some with script and file names |

## 2. The main problems

1. **Each feature is described in three places.** To learn the Meals page you read Part 3G (what the menu does, in brief), Part 5 (the Meals list, Meal columns, Meal items table, What-if, Meal history), and Part 6 (editing consequences, amounts, recipe servings). Part 3 is mostly links to Parts 5 and 6.
2. **Material that matters to users is buried in reference text.** Part 4 mixes nutrition science (essential amino acids, DIAAS, the FAO standard) with descriptions of NuMa features (Nutrient Plot, Per-day profile tracking, Daily Nutrient Goals, how complements are ranked). Its 27 lettered sections have no grouping: protein topics are spread over A–K and Y, and again in Appendices A, D and E.
3. **Workflows are hard to find, and there are few of them.** Part 2F is a one-line pointer to Part 3C, which has four workflows plus "a few more things worth trying".
4. **Duplicated sections.** "Entering custom foods and dietary supplements" is in both Part 3J and Part 6E. Settings is covered in Part 3I and again in Part 6A–B. "Getting help" is Part 5A, but troubleshooting is Part 8 and "using the manual" is Part 7D–F.
5. **Developer material in a user manual.** Part 11 (13k words) records changes at code level, some with identifiers such as `_meal_expand_for_diaas`. Some footnotes name scripts and JSON files. Part 9 lists features already finished. Part 6D has a section on editing `user-manual.md` itself.
6. **The quick start is too long.** At 4,800 words it is longer than most of cmgr's Parts, and two of its sections (H, I) only tell you to read other Parts.

## 3. Constraints on any reorganization

- **115 anchors are linked from inside the app** (`manual_link("…")` in the templates and backend), and the manual has **2,142 internal links** to its 375 anchors. Sections can move and be renamed freely, as long as their `{: #id}` anchors stay. `tests/test_link_integrity.py` already checks this, so every step can be verified.
- `*Search terms:*` lines (see `docs/claude/manual-search-terms.md`), the `<!-- t:YY-MM-DD -->` review markers, the reading-time stamps and `scripts/build_manual.py` all carry over unchanged.
- Some tests look for specific manual content (abbreviations, search terms, top contributors, GL swaps, AA estimates, packaging). Before moving their sections, check which text they look for.

## 4. Proposed outline

This follows the cmgr plan: concepts first, then a menu-by-menu reference, then workflows, with each behavior explained once and cross-linked. The difference from cmgr is the large science reference, which gets a Part of its own at the back, so the reading path through Parts 1–4 stays short.

**Preface: How to read this manual.** What NuMa is in three sentences, which Part to read for what, a reading-path table ("new user: 1 → 2 → 3, then use 4 as a reference"), and a pointer to the search how-to. This replaces Part 1 H–I.

**Part 1: Quick start** *(target about 2,000 words)*
- A. Install (Windows, Linux), what's on your computer, backups. Kept, but trimmed.
- B. First-time setup: the four steps from the current 1G.
- C. A ten-minute tour: look up one food, log one meal, see its protein score. One pass through the core loop, linking to the workflows.
- D. Tips: the current 1B–F reduced to a short list (estimates are fine at first, NuMa learns from you, help is nearby).

**Part 2: Overview: the ideas behind NuMa** *(target about 4,000 words)*
- A. What NuMa does and who it's for: the current 2A–D, condensed.
- B. **A short primer on the ideas used everywhere**, one or two paragraphs each, linking to Part 7 for depth: protein quantity vs. quality, essential amino acids and the limiting one, DIAAS and DCP, complements, daily targets (RDA, optimal, maximum), GI and GL, antinutrients and oxalate, water.
- C. How the pieces fit: foods → recipes → meals → days → analysis, the pantry and the food cache. A small diagram.
- D. Why you can trust the numbers: the current 2E, condensed. The full version moves to Part 8.

**Part 3: Workflow examples** *(new Part; each workflow ends with "what you now have" and links to the Part 4 sections it used)*. A candidate list; the current four are folded in:
1. **Is this food a good protein source?** Look up a food, read its protein quality, see its gaps and complement suggestions. *(current WF1)*
2. **Logging your first day.** Create meals, add foods by amount, mark them complete, read the full-day analysis.
3. **Building a recipe from scratch.** Ingredients, servings, per-serving DCP, then using it in a meal and as a complement. *(current WF3)*
4. **Closing a meal's protein gap from your pantry.** *(current WF2)*
5. **A packaged food NuMa doesn't know.** Barcode search, Open Food Facts, or a custom food profile; a supplement tablet.
6. **A week in review.** Several days logged, then Daily Summary, trends and the nutrient plot. *(current WF4)*
7. **Watching blood sugar.** Set a GL target, annotate GI for your core foods, find lower-glycemic swaps.
8. **"What if I stopped eating this?"** What-if on meals, then Substitute everywhere.
9. **Comparing foods while shopping.** Compare, saved comparisons.
10. **Monthly data clean-up.** Checking your data, Problems by food, seeing what a fix changed.
11. **A kidney-stone concern.** Oxalate data for your usual foods. *(optional)*

**Part 4: Menu by menu** *(the functional reference, the heart of the manual)*. One chapter per menu, in navigation-bar order: **Foods** (Search, Analyze portion, Analyze recipe portion, Convert, Food Cache, My Pantry, Custom food profiles, Annotate, Checking your data) · **Recipes** (list, import CSV) · **Compare** · **Meals & Log** · **Analysis** (Daily Summary, Food use in meals, Food use in recipes, What-if: Meals, What-if: Recipes) · **Settings** (each numbered setting) · **Manual**. Plus one chapter for **a food's detail page**, which most menus lead to.

Every menu item gets the same three sub-parts:
- *What it's for*: one or two sentences.
- *What you see*: the page's tables and columns. The Part 5 column guides move here, each to the page it describes.
- *What you can do*: the tasks, titled with verbs ("Archive a recipe", "Merge two meals"). The page-specific parts of Part 6 move here.

**Part 5: Skills used everywhere.** Only the operations that really apply on many pages: entering amounts (current 6K), what you can type and data errors to catch (6J), how searching works (6C, with `!` exclusions and "Did you mean"), what changes when you edit something (6D), where NuMa fills gaps with estimates (6H), moving data with CSV (6L), navigation and keyboard (3B, including two windows).

**Part 6: Help and troubleshooting.** Getting help (current 5A) and troubleshooting by symptom (current Part 8), together in one Part, ending with feedback.

**Part 7: The science behind NuMa** *(the reference; current Part 4 plus the conceptual appendices, grouped into chapters instead of 27 flat letters)*
- A. **Protein**: amino acids, completeness, DIAAS, limiting-AA scoring, the FAO standard, DCP and its cap, gaps, how meals are scored (4Y), complements and their tiers, protein per meal and timing (4Z), and from the appendices the primer (10A), DIAAS-only foods (10D) and the worked validation example (10E).
- B. **Blood sugar**: GI, GL, and GL vs. CGM (10C).
- C. **Targets**: RDAs, daily goals, optimal, maximum limits, diet-aware bioavailability, per-day profiles.
- D. **Other**: omega-3, antinutrients, oxalate, water.
- E. **Food reference**: plant protein sources (10B) and the full nutrient key (10G).

Feature descriptions now in Part 4 (Nutrient Plot, Nutrient Averages, Per-day Profile Tracking) move to Part 4 under Analysis or Settings, leaving a short "the science" paragraph behind where needed.

**Part 8: Your data.** Where food data comes from (7A), what's stored on your computer, backups and restore (from 1A), and validation in full (2E).

**Appendices**: A. Glossary · B. Internet resources · C. Using this manual (search, contents, bookmarks) · D. What's new (user-level only; see section 5) · E. Ideas for future features (open items only) · Notes · Disclaimer.

## 5. Simplification: what gets shorter

| Change | Words saved (approx.) |
|---|---:|
| Part 11 moves out of the manual. The user manual keeps a short "What's new" appendix of release summaries; the dated code-level entries go to `docs/` or the README. *(decision 1)* | 10,000–12,000 |
| Footnotes: technical asides (script names, JSON files, licence mechanics) move to the README; citations stay. | 1,500 |
| Part 9's "already implemented" list is deleted; "Editing the manual's source file" (6D) moves to the README. | 1,000 |
| Duplicates merged: custom foods/supplements (3J and 6E), settings (3I and 6A–B), help (5A and Part 8). | 1,500–2,500 |
| Part 3D–H's brief menu summaries are replaced by the full Part 4 chapters, not added on top of them. | 3,000–5,000 |
| Quick start trimmed from 4,800 to about 2,000 words. | 2,800 |
| Part-by-Part tightening as each chapter is reviewed (long sentences, repeated "see X in Part Y" chains). | 10–15% of what remains |

A realistic result is **about 95,000–105,000 words**. The bigger gain is the reading path: Preface plus Parts 1–3 come to about **12,000 words** (under an hour), and everything after that is reference you search for or follow a link into.

## 6. Order of work

Each step is a separate session and commit, with the full test suite passing at the end of each.

1. **Move, don't rewrite.** Reorder the existing sections into the new outline, anchors unchanged, with no prose edits except the Part and section letters and the "in Part N" phrases that the move makes wrong. A small script can find every "Part N" / "Part N, X" reference left over afterwards. Tests verify that no link broke.
2. **Take out the developer material**: Part 11, technical footnotes, Part 9's done list, the manual-editing section. Update CLAUDE.md step 3 and `docs/claude/changelog.md` for the new home of the log.
3. **Merge the duplicates** and fold Part 5's column guides into their Part 4 pages (this is the biggest editing step; one menu per session).
4. **Write the new pieces**: the Preface reading path, the Part 2 primer and diagram, the trimmed quick start, and the Part 3 workflows.
5. **Tighten, Part by Part**, using the `t:` review markers to track progress. Update the reading-time stamps and the header stamp, then run `scripts/build_manual.py`.
6. **Keep it in shape**: add a weekly-sweep item checking that every menu item in `base.html` has a Part 4 section (a test could do this, like cmgr's keyboard-drift test).

## 7. Writing conventions (same as cmgr)

Second person, present tense. On-screen labels in **bold**, exactly as shown. Task headings start with a verb. One task per section. Explain each behavior once and link to it everywhere else. American spelling. One line per paragraph (no hard wraps).

## 8. Decisions (2026-11-14)

1. **Part 11 log:** option (b). Release summaries stay in the manual as **What's new** (`#updates-log`); dated entries moved to `docs/updates-log-details.md`.
2. **Workflows:** the list stands, with one change: Workflow 1 starts away from the computer, taking stock of pantry and fridge to list commonly eaten foods, then puts those foods into NuMa (pantry, protein quality). That makes Workflow 2 (logging a day) easy, it's something every user needs to do anyway, and it puts attention on the food, which is the point. Workflow 5 keeps dietary supplements.
3. **Audience:** anyone. Most readers will be fairly intelligent, but a college education can't be assumed: plain words, technical terms explained where they first appear.
4. **"Supplements":** the reference material already in the manual (concepts, appendices, nutrient key, glossary), kept in Part 7 and the Appendices.
5. **Pace:** all at once.

## 9. What was done, and what's left

Done 2026-11-14:

- **Step 1.** Sections moved by script into the section 4 outline; every anchor kept. "in Part N" qualifiers after links removed rather than renumbered; the rest fixed by hand.
- **Step 2.** Part 11's dated entries moved to `docs/updates-log-details.md`; `create_release.py`, `build_ai_manual.py`, `search_terms_review.py`, the abbreviation test, `docs/claude/changelog.md`, CLAUDE.md and the README updated. A release now also adds a `## Release <tag>` heading to the details file. Code-level asides removed from footnotes [^8] and [^10]; Part 9's done list dropped; "Editing the manual's source file" moved to the README.
- **Step 3.** Duplicates merged: custom foods (old 3J/6E), Settings (old 3I/6A–B), help (old 5A + Part 8). Every Part 5 column guide moved under its Part 4 page. The Foods → 9 check details moved from the Food Cache section into Checking your data. New sections: Daily summary (Analysis → 1) and Import CSV (Recipes → 2).
- **Step 4.** Written: the Preface reading-path table, Part 1 C–D, Part 2 intro, primer (B), how the pieces fit (C, with a diagram), trust summary (E), all eleven workflows plus "A few more things", and chapter introductions in Parts 4, 7, 8 and the Appendices.
- **Step 6.** `tests/test_manual_menu_coverage.py`: every navigation-bar destination in `base.html` must map to an anchor inside Part 4.
- **Step 5, partly.** Part 1 trimmed: the GI step now points to Workflow 7, the dry-pasta note moved to Entering amounts; the front matter's feedback list moved to Getting more help.

Done later on 2026-11-14 (second session):

- **Workflows checked against the running program**, on an isolated test server (temporary data folders, online lookups stubbed): 54 of 61 labels matched; the rest appear only after a search or with data problems. Fixed: the meal protein heading (**Meal-Level Protein Analysis**), **Copy as new draft** on a food's page, **Copy a cached food as a draft**, and the Annotate page that can open after adding a food (Workflows 1 and 2 now say to click **Skip for now**).
- **Step 5, Parts 4–8.** Tightened paragraph by paragraph, keeping every fact: Part 4 41,400 → 28,100 words, Part 5 9,100 → 5,600, Part 6 5,300 → 2,800, Part 7 40,800 → 35,700, Part 8 4,700 → 3,400. Whole manual 124,400 → 98,700. Old menu summaries now introduce the column guides beside them instead of repeating them; stale "above/below" references fixed; the long link list in Getting help replaced by three short paragraphs; the protein-target argument now made once (RDA section) instead of twice; a developer aside on search ranking removed.
- **Corrections found along the way:** a Food Cache column linked to the wrong section; Settings had search terms meant for older people; the manual said NuMa doesn't record times, but meal items now record when they were entered (not when eaten).

Left as written, on purpose:

- **Sections carrying your `t:` review markers**: all of Part 1, Part 2's reviewed section, the Glycemic Index section, Part 8's backup, installed-files and validation sections, and "Getting more help". Part 1 therefore stays at about 3,400 words rather than the 2,000 targeted; trimming it further means rewording text you've reviewed, so that's your call.
- **Reference material**: the Full Nutrient Key, Plant protein sources, the protein-quality primer (checked claim by claim in October), the worked validation example, the Glossary and the Notes.
