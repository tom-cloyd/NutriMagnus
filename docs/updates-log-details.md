# NutriMagnus — program updates log, dated details

The detailed, dated record of every user-facing change: what changed, and (in the hidden Scope blocks) the menu path, files touched and technical detail. Moved here from the User Manual's Part 11 on 2026-11-14, when the manual was reorganized: the manual now keeps only the one-line release summaries, in its **What's new** section (`#updates-log`), which is what users and the GitHub release page see.

How entries are written, numbered and rolled into a release: `docs/claude/changelog.md`.

Newest first. Entries made after a release are at the top, above the first "Released in" heading.

<!-- Insert new updates below here -->

#### November 21 updates

**PROGRAM: EDIT OR UNDO RIGHT AFTER ADDING TO A MEAL; EDIT AND REMOVE IN EVERY ITEMS VIEW**

Right after you add something to a meal, the green **Added …** line has **Edit** and **Undo** buttons, to change its amount or take it straight back out; a recipe added as individual ingredients is changed (a new total, scaled to keep its proportions) or undone all together. The **Foods** and **Foods & recipes** views of a meal's Items now have **Edit** and **✕** too, not only **As logged**. [learn more...](#meal-undo-add)

<!--
```
Scope: meal page. db.py: meal_add_food() and meal_add_recipe() return the new meal_items id. web/backend.py: /meal/{id}/add and /add-recipe put added_ids (comma-separated; every leaf row for mode=ingredients) in the redirect, the annotate detour's next= included; new POST /meal/{id}/remove-items (item_ids, name, q) removes several items, meal-scoped so ids from another meal are ignored, and redirects with removed=name when anything went; new POST /meal/{id}/scale-items (item_ids, amount, name, recipe_id) sets a new total for several food items, scaling each by one factor (amount: a weight via _parse_portion_str with no portions, else with recipe_id servings/volume via parse_recipe_amount × recipe_serving_grams), units rewritten as "N g", notes kept, meal-scoped; meal page context gains items_by_id. numa_app/services/meal_item_views.py: foods_view rows gain item_ids (logged items holding the food itself: on its own or from_recipe), item_grams and whole_recipes (recipes logged whole containing it); whole_view's gathered rows gain item_ids. meal.html: the As logged Edit pop-up moved into a top-level edit_popup(item, label) macro, with scale_popup() and remove_ids_button() beside it; #just-added is now a div (a form inside the old <p> closed it early) with Edit (edit_popup for one id still in the meal, scale_popup for several) and Undo; #just-removed line; Edit and ✕ columns in the Foods / Foods & recipes tables (Foods: a food only inside whole recipes shows "in a recipe"; one in both removes only the logged part, saying so in the title), scroll-restore regex covers remove-items. Tests: test_meal_item_views.py (7).
```
-->

#### November 20 updates

**PROGRAM: WHAT-IF: RECIPES FINDS RECIPES BY NAME, AND LISTS THEIR INGREDIENTS TO PICK FROM**

What-if: Recipes can now choose its recipes **By name**: type words, and the recipes whose names hold all of them are listed as you type. For **Remove** and **Change amount**, clicking the food/recipe box lists every food and sub-recipe in the chosen recipes, most used first, so you pick what to change from what's actually there instead of typing a name blind. Add and Replace still search all your foods and recipes. [learn more...](#whatif-recipes)

<!--
```
Scope: Analysis → What-if: Recipes. web/backend.py: _recipes_named() (list-filter rules, a typed R-code, empty selects nothing); _parse_food_use_recipes_selection gains mode="name" + recipe_name (Food Use in Recipes doesn't offer it yet); _whatif_recipes_compute/_whatif_args carry recipe_name, so CSV export, Apply for real and saved scenarios keep the selection; new GET /analysis/whatif-recipes/name-matches (count + first 40) and /analysis/whatif-recipes/ingredients (db.recipe_expand_ingredient_use over the selection, every depth, deleted sub-recipes skipped; counts per selected recipe; q = list filter or a code). Templates: analysis_whatif_recipes.html (By name radio, box, live preview; help text), _whatif_changes.html script(ingredient_source=...): the item picker reads the step-1 selection from the form and opens on focus/click for remove/scale; the Meals page passes none and is unchanged. Tests: test_web.py (4), tests/e2e/test_whatif_recipe_picks_e2e.py.
```
-->

**PROGRAM: RECIPES YOU'VE MADE CAN GO IN MY PANTRY**

A batch you've made, such as a loaf of bread, is now food on hand: put it in My Pantry with **Add to pantry** on My Pantry's search results (the search now finds your recipes too), the **In My Pantry** box on the recipe's page, or the Recipes list's new **Pantry** column. It's listed under **Recipes on hand** on My Pantry, with **Remove from pantry** for when the batch is used up. Protein complement suggestions offer the recipes in your pantry under **From your pantry** (renamed from "From your pantry & recipes"); your other recipes now appear under **Other options**, as things you could make, and archived recipes aren't suggested. [learn more...](#pantry-recipes)

<!--
```
Scope: db.py (recipes.on_hand column; set_recipe_on_hand(), recipes_on_hand(); recipe_list/recipe_list_recent select on_hand), usda_nutrients.py (suggest_complements recipe_candidates → general tier, name/diet/ignore filtered), numa_app/services/complements.py (build_complement_display and two_step_combo pass recipe_candidates through), web/backend.py (_web_complement_pools splits recipes by on_hand, archived recipes dropped from _web_recipe_candidates; POST /recipe/{id}/on-hand; /pantry passes recipes_on_hand; _screen_pantry finds recipes unless linking a name-only entry; recipe search rows carry on_hand), templates: _row_toggles.html (pantry_box), recipes.html (Pantry column), recipe_detail.html (In My Pantry box), pantry.html (Recipes on hand), _pantry_search_rows.html (recipe rows), complement headings in meal, meal_day, food_detail, recipe_detail, food_analyze_recipe_portion, print. Before this every analyzed recipe counted as on hand. Tests: test_complements.py TestRecipeCandidates, test_web.py (three new; pantry search test now expects recipes).
```
-->

#### November 19 updates

**PROGRAM: "COMPARE CHECKED FOODS WITH THIS ONE" TURNS BLUE WHEN READY; COMPARE KEEPS YOUR TICKS**

On **Fill in nutrients from another food** and a custom food's **Edit values** page, the **Compare checked foods with this one** button now starts grey and turns blue once one food is ticked (the page's own food is the other), like the Compare buttons on searches and lists, which turn blue at two. Before, it stayed a blue outline whatever was ticked. And every Compare button (these two, and Compare nutrition of selected on searches and lists) now keeps your ticks after comparing: coming back (its **← Back** button), the foods you ticked are still ticked, so you can untick or add one and compare again; before, comparing cleared them. **Clear all picks** unticks them all. [learn more...](#compare-picks)

<!--
```
Scope: web/templates/base.html (Compare picks script: a group's `min`, 1 for the custom-profile compare forms, ; picks are no longer cleared when Compare opens, for any Compare button: the SENT/clearSent step is gone), food_fill_from.html and food_custom_edit.html (button starts btn-outline-secondary), tests/e2e/test_compare_picks_e2e.py.
```
-->

**PROGRAM: YOUR OWN NOTES ON ANY FOOD; PANTRY NOTES CAN BE CHANGED**

Every food's page now has a **Notes** section with **Add your own notes on this food**: type, **Save notes**; clear the box and save to remove them. They're kept apart from the notes a food came with (now shown as **From the food's source**), so **Refresh from USDA** never overwrites them, and they show in the Food Cache's **Notes ▸** and on the printout. A custom food's box edits its existing notes (the same as on Edit values). Merging duplicate foods keeps both foods' notes. On the Pantry list, each entry's note is now editable in place (click it, or **add a note**); before, it could only be typed when the food was first added. [learn more...](#food-notes)

<!--
```
Scope: db.py (foods.user_notes column; food_set_user_notes(), custom food → notes; pantry_set_notes(); merge_food_into() appends the dropped food's user_notes; list_cached_foods selects user_notes), web/backend.py (POST /food/{id}/my-notes, POST /pantry/{id}/notes; food ctx user_notes/custom; Food Cache rows user_notes; print "notes" section counts user_notes), web/templates/food_detail.html (Notes section always shown, sidebar entry too), food_cache.html, pantry.html, print.html, tests/test_web.py, docs/claude/data-shapes.md.
```
-->

**PROGRAM: FOOD CACHE AND PANTRY CAN LIST THE FOODS YOU EAT MOST FIRST**

The Food Cache's and My Pantry's **Sort by** menus gain **Most meals, last 90 days**, the same order as Foods → 9's lists: foods in the most meals over the last 90 days first (on their own or inside a recipe), then the rest by name. While it's chosen, **Used in** adds "N in last 90 days". It is the default sort; a sort you'd already chosen is kept, and **Name** is still there for alphabetical. [learn more...](#food-cache-web)

<!--
```
Scope: web/backend.py (_FOOD_CACHE_SORT_KEYS["meals90"], so also _PANTRY_SORT_KEYS and the Archived page's menu; meals90 field in _food_cache_rows and pantry_get via data_quality.meals_eaten_counts; default sort "meals90" for sort_food_cache / sort_pantry), web/templates/food_cache.html and pantry.html (option, count line), tests/test_data_quality.py.
```
-->

**PROGRAM: FOODS → 9 LISTS START WITH THE FOODS YOU EAT MOST**

On Foods → 9 (Check database), every list of foods (missing nutrient data, named dry but mostly water, food data problems, no amino acid data, no portion weights, no GI, generic density, amounts that no longer match, old USDA copies) now starts with the foods that were in the most meals over the last 90 days, on their own or inside a recipe, and shows that count beside each name ("· 12 meals"). Ties keep the list's previous order. A new **Order every list of foods** menu at the top switches all of them to alphabetical, and is remembered. *Foods: days eaten* keeps its own ranking by days eaten unless alphabetical is chosen; *Broken references* is unchanged. [learn more...](#checking-your-data)

<!--
```
Scope: numa_app/services/data_quality.py (MEALS_EATEN_DAYS, meals_eaten_counts(), order_by_meals()), web/backend.py (food_cache_db_check_get: order param, pref data_check_order, lists re-sorted), web/templates/food_cache_db_check.html (order select, _m90 macro beside each food; "most-used first" dropped from three intros; de_no_gi sorted only in meals order), tests/test_data_quality.py, tests/test_web.py.
```
-->

**PROGRAM: CTRL+CLICK ON CONTENTS AND MANUAL LINKS EXPLAINS THE BROWSER TAB TOO**

In NuMa's own window, a Ctrl/Shift+click or middle-click on a link to a part of the same page, such as an entry in a meal's, day's or recipe's **Contents** sidebar, now shows the "Opening in a browser tab" explanation before the tab (a second copy of the page) opens; before, it opened unannounced. Likewise, a Ctrl/Shift+click or middle-click on a link in the User Manual (its contents, or a link in its text) now shows the same "Opening in a browser tab" explanation as one on a NuMa page; before, the tab opened without it. A link to a manual section opens the tab at that section, shown under NuMa's menu like the manual itself. "Don't show this again" covers both. [learn more...](#two-windows)

<!--
```
Scope: web/templates/base.html (notice's show() split out; onHashClick, a bubble-phase listener for same-page #links, skipped when a page handler already preventDefault()ed or the link has data-bs-toggle; window.numaNewTabNotice(href) for the manual frame), web/templates/manual_frame.html (capture click/auxclick listener on the frame's document hands modified clicks to it, /manual/page#x mapped to /manual#x; the plain-click redirect skips modified clicks).
```
-->

#### November 18 updates

**PROGRAM: A MEAL'S ITEMS CAN BE VIEWED AS FOODS, OR WITH EACH RECIPE KEPT WHOLE**

On a meal's page, Items has a **View** menu beside **Sort by**. **As logged** is the list as before. **Foods** lists every food eaten, with recipes (and recipes inside them) broken down and a food reached more than once shown as one row, with where it came from. **Foods & recipes** keeps each recipe whole, gathering a recipe you added as individual ingredients back into one row. The choice is remembered; only As logged has Edit and remove. [learn more...](#meal-items-view)

<!--
```
Scope: meal page. numa_app/services/meal_item_views.py (new: foods_view() via expand_recipe_ingredients, whole_view() via items' from_recipe, sort_rows()), web/backend.py (meal_view: item_view param, pref view_meal_items, item_view_rows), web/templates/meal.html (View select; read-only table for the two new views; footnotes only in As logged), tests/test_meal_item_views.py (new), README (tree entry, test table, count).
```
-->

**PROGRAM: ARCHIVED FOODS AND RECIPES PAGE FINDS THEIR MISSING NUTRIENT DATA**

The new **Archived foods & recipes** page (Foods → 10, key `0` in the Foods menu; also Recipes → 3) lists only what you've archived: foods with the Food Cache's columns, and recipes, whose **Other nutrients** column checks every ingredient food. Incomplete items used in logged meals come first, with a count at the top, because those meals still count in your long-run nutrient averages while Foods → 9's checks skip archived foods. Restore works in place. The Food Cache's **Sort by** gains **Incomplete first**. [learn more...](#archived-web)

<!--
```
Scope: Foods → 10, Recipes → 3. web/backend.py (_food_cache_rows() factored out of food_cache_get and reused by the refresh-error render, which had lacked "use" and would have failed on the Used in column; "problems" sort key; _archived_recipe_rows() via db.recipe_expand_ingredient_use(), flagging gap foods, uncached foods and deleted sub-recipes; GET /food/archived, pref sort_food_archived), web/templates/food_cache.html (archived_only mode: page_url, summary alert, no toolbar; "Archived only" button on the Food Cache), _archived_recipes.html (new), base.html (menu items; digit picker maps 0 to the tenth item; command palette shows 0), tests/test_web.py, tests/test_manual_menu_coverage.py.
```
-->

**PROGRAM: FOOD CACHE AND PANTRY SHOW WHETHER A FOOD'S OTHER NUTRIENTS ARE COMPLETE**

The Food Cache and My Pantry lists have an **Other nutrients** column after DIAAS. It reads "complete" when a food has its macronutrients, water, minerals, vitamins and the amino acids its DCP is worked out from (or each missing group is marked "not needed"), and "incomplete" otherwise. Pointing at "incomplete" lists what's missing, and clicking it opens the food. To make room, the Used in counts and the longer button labels ("Add to pantry", "Copy as draft") take two lines. [learn more...](#cached)

<!--
```
Scope: numa_app/services/data_completeness.py (OTHER_NUTRIENT_GROUPS = macros, water, minerals, vitamins, aa; OTHER_NUTRIENT_LABELS; other_nutrient_gaps(), water only while track_water), web/backend.py (_other_nutrients(): None for a supplement or unlinked pantry entry; food_cache_get and pantry_get add other_missing, honoring food_data_ignores), db.py (search_cached_foods selects is_supplement), web/templates/_other_nutrients.html (new: header and cell macros), food_cache.html, pantry.html (column; Used in and button labels stacked with <br>; notes row colspan 12), web/static/style.css (.actions-stack), tests/test_web.py. Omega and phyto are left out, as in DEFAULT_CHECKED.
```
-->

**PROGRAM: MEAL PAGE SAYS WHAT ONE SERVING OF A RECIPE WEIGHS**

When you add a recipe to a meal, the hint under its Amount box now gives one serving's weight ("4 total · 1 serving = 24 g"), with the serving description in front when the recipe has one ("1 serving = 1 muffin, 85 g"). Before, a recipe with no serving description gave only the number of servings it makes. [learn more...](#portions-vs-servings)

<!--
```
Scope: web/backend.py (_recipe_search_rows adds serving_grams from recipe_serving_grams() for every recipe search row; _screen_recipe's own serving_grams loop dropped as redundant), web/templates/_add_food_row.html (recipe Amount hint built like _recipe_search_rows.html's, no longer via _serving_note), _recipe_search_rows.html (weight shown with %g, so "24 g" not "24.0 g"), tests/test_web.py.
```
-->

#### November 17 updates

**PROGRAM: FOOD USE PAGES ALWAYS SAY WHETHER A REPLACE WORKED**

On Food Use in Meals and Food Use in Recipes, a replace (or, on the meals page, a remove or add) now always reports its outcome in a colored box the page opens at. Green names both items and how many meals or recipes changed. Red says nothing changed and why: a code no food or recipe has, or an item that isn't in the selected meals or recipes. After a red box, the codes you typed are still in their boxes to correct. [learn more...](#fooduse-substitute)

<!--
```
Scope: web/backend.py (analysis_food_use_substitute: checks the replacement exists and that the old item is logged directly in a selected meal, via meals_with_direct_item, before writing; zero hits is now an error naming the item, where it used to redirect with no count and so no message; success adds done=<sentence> via _food_use_label / _meal_count_text; _food_use_back lands on #substitute-panel and on error carries action/old_code/new_code/amount back; analysis_food_use_recipes_substitute likewise, zero affected recipes is an error; both GET routes take done/old_code/new_code), web/templates/_replace_picker.html (outcome macro; fields takes old_text/new_text), analysis_food_use.html (action radio and amount refilled), analysis_food_use_recipes.html (panel now opens on error or success too; it opened only for sub_id, so its error was hidden in a closed panel), tests/test_web.py.
```
-->

**PROGRAM: FOOD CACHE KEEPS FETCH TICKS AND DELETE WARNINGS WHEN YOU CLICK BACK**

On the Food Cache, the boxes you tick in the Fetch column, and any "Deletion not possible" warning under a food, are still there when you go to another page (to look at the meal using that food, say) and click back. Coming back with a keyboard shortcut (a menu shortcut or the command palette) starts the page fresh. Each warning is checked again on return, so it lists what uses the food now, and disappears once nothing does. [learn more...](#cached)

<!--
```
Scope: web/templates/food_cache.html (numa_fetch_picks and numa_delete_blocked in sessionStorage, per tab; Select all missing AA / Clear selection save too; restored on load and on pageshow from the back/forward cache), web/templates/base.html (showBlocked fires numa:row-blocked on the row and is exposed as window.numaShowRowBlocked), web/backend.py (new read-only GET /food/cache/{fdc_id}/delete-blocked returning {blocked_html} or null; _food_delete_blocked_html shared with the delete route), tests/test_web.py. Compare ticks already persisted (base.html compare picks); Fetch ticks, the first column and easily mistaken for Compare, did not. Ticks on foods a filter hides are kept and only visible ticks are sent. Keyboard vs mouse: base.html's head script flags, in sessionStorage numa_nav_by_key, a click on a #main-navbar or #palette link whose event.detail is 0 (Enter, or the shortcut code's element.click(); a mouse click is always 1 or more), and exposes it on the next page as window.numaArrivedByKey; food_cache.html then drops both keys before restoring.
```
-->

**PROGRAM: NUMA'S WINDOW GETS ITS ICON BACK IN ALT+TAB**

NuMa's own window now runs as its own browser process, with a browser profile of its own, so KDE shows it in Alt+Tab with NuMa's icon even while an ordinary Chromium window is open. Your browser's extensions no longer run in NuMa's window either. [learn more...](#browser-to-launch)

<!--
```
Scope: web/launcher.py (_app_window_profile; _pick_and_open_browser adds --user-data-dir=<profile> --no-first-run --no-default-browser-check to the --app launch), tests/test_launcher.py. KDE groups windows into applications by process: an --app window in the main profile's process, alongside an ordinary browser window (OneTab's tab, opened at Chromium startup), was filed under Chromium and showed no NuMa icon, although its app_id still matched chrome-127.0.0.1__nutrimagnus-source-Default.desktop. Same fix as cmgr's launcher (_profile_dir). Profile: ~/snap/<browser>/common/numa-profile for a snap browser (it may only write inside ~/snap/<name>/), else $XDG_CONFIG_HOME/numa/browser-profile, %LOCALAPPDATA%\NutriMagnus\browser-profile, ~/Library/Application Support/NutriMagnus/browser-profile. localStorage (manual bookmarks, Keyboard Shortcuts on/off, Nutrient Plot's last settings, Food use's meal column) is per profile, so it starts empty in the new one.
```
-->

**PROGRAM: OPEN A RECIPE OR MEAL BY TYPING ITS ID**

On the Recipes list, Meals & Log and Search meal history, press Alt+Shift+G, type a row's ID (21 for R21) and press Enter: that recipe or meal opens. A box at the bottom of the window shows what the digits typed so far match; Backspace removes a digit, Esc cancels. (First built as hold Alt+Shift, type the digits, let go; changed the same day because a browser extension's own Alt+Shift+1 and Alt+Shift+2 shortcuts, OneTab's, reach the browser before the page sees them.) [learn more...](#go-to-id)

<!--
```
Scope: web/templates/base.html (Alt+Shift keydown handler + "Go to a row by its ID" block), web/static/style.css (#go-id-box), recipes.html, meals.html, meals_search.html (data-go-id / data-go-label on each row's main link), tests/e2e/test_go_to_id_e2e.py. With any [data-go-id] on the page, Alt+Shift+G turns go-to-ID mode on; while on, a capture-phase window keydown listener swallows every key (so a focused search box never gets them): digits (Digit/Numpad) append to a buffer, Backspace trims it, Enter clicks the first [data-go-id="<Number(buffer)>"] or shows "No ID N in this list" for 2.5 s, Esc or any other key cancels. Window blur cancels. Settings' Alt+Shift+digit section shortcuts are untouched.
```
-->

**MANUAL: USING NUMA WITHOUT A MOUSE**

[Tips for new users](#new-user-tips) now points out that NuMa can be run entirely from the keyboard, for speed or for anyone who finds a mouse or touchpad hard to use, starting from `Alt+Shift+K`, the panel that lists every page and shortcut.

**PROGRAM: A RELOADED PAGE KEEPS YOUR PLACE EVEN WHEN ONLINE RESULTS ARRIVE LATE**

When a page reloads after you change something below its search results (on a meal, say), it reliably comes back to where you were. Before, if the online results arrived while the page was still gliding back into place, it could end up back at the top.

<!--

```
Scope: web/templates/base.html, the after-submit scroll restore. It used window.scrollTo(0, y), which Bootstrap's scroll-behavior: smooth animates; the online-rows swap (data-search-results fetch) records the scroll position and puts it back after replacing the rows, so landing mid-animation it read the half-way position (often 0) and its own scrollTo cancelled the restore. The restore now jumps with behavior: 'instant'. Found as an intermittent failure (about 1 in 7 on a fresh server) of tests/e2e/test_search_lands_on_results_e2e.py::test_meal_search_puts_panel_at_top_and_adding_keeps_your_place; 0 in 16 after.
```

-->

**PROGRAM: ALT+SHIFT+K LISTS EVERY PAGE AND SHORTCUT (COMMAND PALETTE)**

**Alt+Shift+K** (or the **⌘ Alt+Shift+K** button at the right of the menu bar, or `Ctrl+K`) opens a panel listing every menu page and every shortcut the current page has, each with the keys that reach it. Type to narrow it, or to search foods, recipes or meals for the typed text; ↑↓ and Enter choose; it can also quit NuMa. Settings' Keyboard Shortcuts section moves from `Alt+Shift+K` to `Alt+Shift+E`. [learn more...](#command-palette)

<!--

```
Scope: web/templates/base.html: navbar #palette-btn (data-ak="k"), #palette modal, palette script (pages read from the navbar so it can't drift from the menus; page entries from every [data-ak] outside the navbar, data-ak-label when the text won't do); the Alt+Shift handler refactored into akRun(key) / window.numaAkRun, which the palette runs; Ctrl+Q's handler exposed as window.numaQuit; Ctrl+K alias; footer hint names K. web/static/style.css: palette rules. settings.html: section 12 K -> E. meal.html, compare.html: data-ak-label on the Items targets. Same design as cmgr's palette (cmgr README, "Keyboard shortcuts and the command palette"). Tests: tests/e2e/test_command_palette_e2e.py (6); test_web settings-letters and Items tests updated.
```

-->

**PROGRAM: WHAT-IF REMOVES A RECIPE LOGGED AS INGREDIENTS, EVEN AFTER YOU CHANGED IT**

When a recipe is added to a meal as individual ingredients, each of those foods now remembers the recipe it came from, and the meal page shows *part of* and the recipe's name beside it. **What-if: meals** (Analysis → 4) uses that link to **Remove** or **Change amount** of the recipe, so it still works after you altered the recipe for that meal: an ingredient left out, an amount changed, or a food swapped. Foods you added yourself stay. Recipes logged this way before today are still found by matching their ingredients, as before. Where a change can't reach such foods, it now names the meals so you can fix them by hand: a **Replace** of the recipe (Replace needs the recipe itself in the meal), and a recipe used as a sub-recipe inside one logged as individual ingredients. The Apply confirmation page shows the same notes. [learn more...](#whatif-ingredients)

<!--

```
Scope: db.py: meal_items.from_recipe_id (ALTER TABLE migration); meal_add_food(from_recipe_id=); meal_copy_items copies it. web/backend.py meal_add_recipe_item() tags rows in "ingredients" mode; _meal_expand_for_diaas() adds `from_recipe` to food items; meal.html shows "part of" in Notes. whatif._apply_logged_ingredient_removals(): tagged rows first, _logged_ingredient_sets() on untagged rows only. _logged_set() and _containers(); replace and sub-recipe-inside-ingredients cases reported as not_replaced_meal_ids / inside_ingredients, rendered by _whatif_changes.html ingredient_notes() on analysis_whatif.html and analysis_whatif_apply.html (plan changes carry `rep`); loose-meal note moved there and reworded. Tests (test_whatif.py TestRecipeLoggedAsIngredients): test_logging_as_ingredients_tags_each_row, test_tagged_set_altered_for_the_meal_is_still_removed, test_rows_tagged_with_another_recipe_are_not_matched_by_contents, test_replace_names_meals_holding_the_recipe_as_ingredients, test_sub_recipe_inside_a_recipe_logged_as_ingredients_is_named.
```

-->

**PROGRAM: ASK CLAUDE AI FROM A FOOD'S EDIT PAGE; THE STEPS FOR FILLING MISSING DATA**

A food's **Edit** page now ends with an **Ask Claude AI for help** box. Choose one nutrient group or the whole profile, and either only the values the food is missing or every value (to replace doubtful figures), and NuMa writes the prompt to paste into Claude. The *No amino acid data* box on a food's page now lists its three fixes in order: search for a better record, estimate from a similar food, then **Write a prompt for Claude AI**. The manual's new Workflow 12 explains the order. [learn more...](#fix-food-data)

<!--

```
Scope: web/backend.py food_cache_claude_fetch(): new `replace` (ask for every key in the chosen groups, filled or not; all groups not marked not needed when none chosen) and `back` (local "Back to the food" link) form fields; "" group values (the Edit page's "whole profile") are dropped, as are unknown groups. claude_fetch.build_prompt(replace=) uses _INTRO_REPLACE. data_completeness.group_keys(). claude-import GET/POST take `replace`, which pre-ticks the review's overwrite box. _ask_ai_context() feeds food_custom_edit.html's new #sec-ask-ai details (last of the three solution boxes, with a sidebar entry and an intro line linking /manual#fix-food-data). food_detail.html's no-AA alert is a numbered list ending in a POST to claude-fetch with group=aa. Manual: Workflow 12 {#fix-food-data}, #edit-ask-ai paragraph, #fetch, #ts-missing-aa, #key-sources step 5 and Workflow 10 step 4 point to it. Tests: test_edit_page_ask_ai_box_comes_last_and_writes_prompts, test_food_page_no_aa_box_lists_claude_last, test_claude_import_replace_starts_with_replace_ticked, test_build_prompt_replace_asks_to_check_every_key_listed.
```

-->

#### November 16 updates

**PROGRAM: EDIT RECIPE'S SEARCH RESULTS SHOW DCP AND DESCRIPTION**

**Edit Recipe**'s **Add Ingredient** search results have two new columns right after **Code**: **DCP/srv (g)** (a recipe's digestible complete protein per serving, as on the Recipes list) and **Description** (a recipe's description). Foods show a dash in both, since search results don't carry them.

<!--

```
Scope: web/backend.py _recipe_search_rows() adds description and dcp_g (both already in db.recipe_list()). _recipe_search_rows.html: two <td>s (.col-dcp, .col-desc) after .col-id; every colspan 7 -> 9. recipe_edit.html: two <th>s and colgroup cols 4.5rem / 12rem; style.css .add-food-table-wide width 60.736 -> 77.236rem (comment updated), .col-dcp right-aligned and excluded from the left-align rule, .col-desc wraps. Test: test_recipe_edit_search_rows_show_recipe_dcp_and_description.
```

-->

**PROGRAM: EDIT RECIPE GETS A CONTENTS LIST AND AN INLINE CLEAR SEARCH**

**Edit Recipe** now has a **Contents** list down the left side, like a recipe's own page: Recipe details (with Introduction, Instructions, Notes and documentation, and Running totals under it), Add Ingredient and Ingredients. A click jumps there and opens the section if it was collapsed, and the list highlights the part you're looking at. **Clear search** now sits right after **Search**, always there, instead of below the filters only after a search. [learn more...](#search-keeps-results)

<!--

```
Scope: Recipes → Edit (web/templates/recipe_edit.html). analysis-page layout + analysis-sidebar (#recipe-edit-toc); new ids sec-details (the Recipe details <details>) and sec-instructions (wrapper). Script: a click opens every <details> up from the target; highlight = lowest target whose top is above a third of the window (by position, since Running totals sits beside the right-hand boxes), the window's bottom at the page's end, and a clicked entry stays lit while on screen until wheel/touch/key. Clear search: the old bottom <a data-reset-search> (shown only with q) replaced by a <button data-reset-search> in the input group; group max-width 28rem -> 42rem so the box isn't squeezed. Also this day, layout only: Introduction/Instructions/Notes textareas rows 5 -> 3; Recipes list title row centered (style.css: a heading in a .d-flex.align-items-center row drops its top margin, the row gets it as padding; .section-heading excepted); the Learn more link moved after + New recipe; the empty-Ingredients hint says Add Ingredient is above.
```

-->

**PROGRAM: RECIPES FILTER MATCHES EVERY WORD**

The **Recipes** list's filter box now keeps only recipes whose names hold every word you type, as the other list filters do, so `coffee 2` finds Coffee 2 instead of every recipe with "coffee" or a "2" in its name.

<!--

```
Scope: Recipes list (GET /recipes). web/backend.py recipes_list called _list_filter(q, any_word=True), keeping the any-word test it had before _list_filter existed; it now uses the all-words default like every other list filter, and the any_word parameter is removed (no other caller). Test: test_recipes_filter_needs_every_word.
```

-->

#### November 15 updates

**PROGRAM: SEE WHAT AN INGREDIENT CHANGE DOES TO A RECIPE**

On a recipe's Edit page, each time you add, remove or change the amount of an ingredient, NuMa offers a short report on how the change moved the recipe's nutrients per serving. Pick the nutrient groups, **All nutrients**, or **All nutrients that changed by 5% or more**. A report covers every change since the last one, so remove-then-add shows a whole swap. Reports go into `recipe-edit-effects-data.md`, which a **Show ingredient change(s) file content** button displays. Food and recipe names on the Edit page now open in a panel over it, so a look-up no longer leaves the page. [learn more...](#recipe-edit-effects)

<!--

```
Scope: Recipes → Edit. New numa_app/services/recipe_edit_effects.py (sessions in memory, per recipe: baseline snapshot taken before the first change since the last report; changes listed; offer shown once; selection remembered; file overwritten by a new session's first report, appended after). web/backend.py: recipe_edit_get starts a session unless the Referer is this Edit page, passes effects_* context; before_change/after_change in ingredient add, add-recipe, remove and edit (amount changes only); new POST /recipe/{id}/edit-effects/report and GET /recipe/{id}/edit-effects (Markdown → HTML, tables extension). recipe_edit.html: offer card (fixed, bottom right), Show button + panel, details <dialog> with an iframe for /food/N and /recipe/N links in Ingredients and the search results (capture-phase click, so base.html's leave guard isn't triggered). base.html adds .numa-embedded on <html> when framed; style.css hides the navbar there. File: project root from source, platform_utils.get_data_dir() when frozen; .gitignore'd; tests/conftest.py autouse fixture redirects it. Snapshot: recipe_total_nutrients / servings, recipe_dcp_per_serving, gl_for_leaves over expand_recipe_ingredients(portion_factor=1/servings). Groups: _shown_groups(_NUTRIENT_GROUPS) plus "Other". tests/test_recipe_edit_effects.py (8 tests).
```

-->

**PROGRAM: USDA API KEY CHECKED BEFORE IT IS SAVED**

Settings → 6 now checks a USDA API key with USDA when you save it. A key USDA rejects isn't saved, so a mistyped key can't make every USDA search fail; **Test key** checks the saved key again, and the card shows when it was last checked and the result. [learn more...](#usda-api-key)

<!--

```
Scope: Settings → 6. usda_api.py (check_api_key, record_api_key_check, get_api_key_check, clean_api_key; _get takes an api_key override; USDAError carries .status), usda.py re-exports, web/backend.py (POST /settings/api-key checks first; new POST /settings/api-key/test; settings_get passes api_key_check), web/templates/settings.html (card id usda-api-key, opens on these results), tests/test_web.py (3 tests).
Idea from cmgr's Google Contacts setup, which ticks "connected" only after a real request works and records the last successful check. Check = foods/search query "apple" pageSize 1 with the candidate key; 401/403 → rejected (not saved); any other failure → unreachable (saved, flagged). Verdict + time stored in config.json "api_key_check", dropped when the key changes or is cleared.
```

-->

**PROGRAM: RETURN FROM THE MANUAL IN ONE STEP**

The yellow bar above the manual now has two buttons: **↩ Return to …** (Alt+Shift+U) goes straight back to the NuMa page you opened the manual from, however many jumps you've made inside it, and **← Back one step** (Alt+←) retraces those jumps one at a time. The manual remembers where you were reading, so **Manual** in the menu reopens it there. [learn more...](#manual-back)

<!--

```
Scope: Manual. web/templates/manual_frame.html (two-row bar; return target from document.referrer, kept in sessionStorage numa_manual_return; page name from a path→label table), user-manual.md (#manual-back, #manual-menu, #how-to-read, keyboard shortcuts list), tests/test_web.py, tests/e2e/test_manual_return_e2e.py (new).
Modeled on cmgr's manual_frame.html (which uses Alt+Shift+R; R is Recipes in NuMa, so U). The reading place was already saved by build_manual.py's LAST_SECTION_KEY.
```

-->

#### November 14 updates

**MANUAL: USER MANUAL REORGANIZED**

The manual is now arranged for someone learning NuMa: Quick start, an Overview with a primer on the ideas NuMa uses, eleven Workflow examples (starting with taking stock of your own food), a Menu by menu reference with each page's tables and columns under its menu item, Skills used everywhere, Help and troubleshooting, The science behind NuMa, and Your data. [learn more...](#how-to-read)

Parts 4–8 were then tightened (about 124,000 words down to 99,000, sections carrying a review marker left as written), and the workflows were checked against the running program, which corrected four labels.

<!--

```
Scope: user-manual.md (whole file), docs/updates-log-details.md (new), scripts/create_release.py, scripts/build_ai_manual.py, scripts/search_terms_review.py, tests/test_manual_abbreviations.py, tests/test_manual_menu_coverage.py (new), tests/test_create_release_notes.py (new), docs/claude/changelog.md, CLAUDE.md, README-numa-documentation.md, numa-manual-plan.md.
Plan: numa-manual-plan.md. Sections were moved whole by a script, so every {: #id} anchor kept its target (115 manual_link anchors from the app, ~2,100 internal links). Old Part 5 column guides now sit under their Part 4 menu item; old Part 4 concepts and the conceptual appendices form Part 7 in five chapters; old Parts 6/8 became Parts 5/6; old Part 7 resources split between Part 8 and the Appendices. "in Part N" qualifiers after links were removed rather than renumbered. Part 11's dated entries moved here; the manual keeps the release summaries under "## What's new {: #updates-log}" (create_release.py CHANGELOG_HEADING updated; a release now also adds a "## Release <tag>" heading here). Dropped: old 1H/1I/2F/3J pointer sections, Part 9's done list, the manual-source-editing section (moved to the README), code-level asides in footnotes [^8] and [^10]. New test: every base.html nav destination maps to an anchor in Part 4.
```

-->

**PROGRAM: MEAL PAGE STAYS PUT WHEN YOU REMOVE AN ITEM**

Removing an item from a meal's Items list now leaves the page where it was, instead of jumping to the top and back. A search you had going in Add Food or Recipe stays as it was too.

<!--

```
Scope: Meals → a meal → Items → ✕ (web/backend.py meal_remove_item; web/templates/meal.html; web/templates/base.html).
Three causes. (1) The remove route redirected to a bare /meal/{id}, dropping q; base.html's persist-search script then location.replace()d with ?q= put back, a second load that started at the top after the first had already used up the saved scroll offset. The remove form now posts q and the route keeps it, like update does. (2) After the scroll restore, the search box's native autofocus, base.html's Search-button focus (when q is set) and meal.html's first-result focus all scrolled the page. The restore script now focuses the search box itself with preventScroll (a focused element makes the browser skip autofocus) and sets window.numaMealScrollRestored; the first-result focus honors it; the Search-button focus always uses preventScroll. (3) When the online results replaced the search table, the code put back the old absolute scrollY, undoing the browser's scroll anchoring, so a taller result set pushed Items down. If the viewport is wholly below the Add Food section, the scroll now moves by the section's change in height.
```

-->

**PROGRAM: EXCLUDING WORDS IN FILTER BOXES**

Put `!` before a word in a box that filters a list and NuMa leaves out the items whose names have that word, as it already did in search boxes: `beans !kidney` on the Recipes list, the Food Cache, Annotate, My Pantry's filter, Food Use in Recipes or in Meals, the "Replace it with" box, or Search meal history. A filter of only `!` words, such as `!kidney`, keeps everything else. [learn more...](#search-exclude)

<!--

```
Scope: web/backend.py (_list_filter(), _filtered_cached_foods(); recipes_list, food_cache_get,
food_cache_export_csv, food_annotate_list, pantry filter, food_custom_profiles_get copy_q,
food-use name filters, replacement-search, meals_search).
Each list filter splits off "!" words with search_ranking.split_excluded_words() and drops
names holding one via has_excluded_word(). The remaining words keep each box's own matching
(Recipes: any word; the others: every word). Food Cache / Annotate search the remaining
words through db.search_cached_foods(), or list everything when none remain. Manual: Part 6 C
"Leaving words out" renamed "Excluding words".
```

-->

#### November 13 updates

**PROGRAM: MARK A MEAL COMPLETE FROM THE MEALS & LOG LIST**

The **Complete** column on the **Meals & Log** list is now a checkbox instead of a checkmark. Tick or untick it to mark that meal complete or not; it saves at once, the same as the meal page's **Mark complete** button, and the list refreshes so the Day DCP and % goal figures drop or gain their `*` (provisional) mark. [learn more...](#meals-list)

<!--
```
Scope: web/backend.py (POST /meal/{id}/set-complete: sets from the `complete` field, JSON under X-Numa-Ajax, else back to `next`; the meal page's /meal/{id}/complete still toggles); web/templates/_row_toggles.html (meal_complete_box; box() gains reload= -> data-reload); web/templates/base.html (js-row-toggle reloads on success when data-reload); web/templates/meals.html; tests/test_web.py::test_meals_list_complete_box_saves_in_place.
```
-->

**PROGRAM: A SKIP BUTTON BESIDE EACH ESTIMATE ON THE ANNOTATE PAGE**

Each estimate the Annotate page is asking for now has a **Skip** button right beside its **Asking for this one** badge, so you no longer scroll to the foot of the form to skip. When both GI and DIAAS are asked for, the GI field's **Skip** leaves GI blank and moves you down to the DIAAS box; otherwise **Skip** works like **Skip for now**. [learn more...](#annotate)

<!--
```
Scope: web/templates/food_annotate.html (#gi-skip-btn, #diaas-skip-btn; toDiaas() shared with the "DIAAS needed" jump); tests/test_web.py::test_annotation_page_has_a_skip_beside_each_prompt; tests/e2e/test_annotate_skip_e2e.py. GI's Skip is a <button> only while DIAAS is also in `missing`; otherwise both are links to `next`, same as #annotate-back-btn. The leave guard still warns if a typed value would be lost.
```
-->

#### November 12 updates

**PROGRAM: SEARCH AGAIN WITH YOUR WORDS REVERSED**

After a food search that includes USDA, the end of the results offers the same words in reverse order (`small red beans` for `beans red small`), in a box you can edit. USDA strongly favors names holding your words in the order typed, and branded products are named like ordinary English, so the reversed search often finds many more. Add its results below yours, or replace yours with them. [learn more...](#search-word-order)

<!--

```
Scope: web/backend.py (_run_food_search also=, _reverse_offer_query, _drop_excluded,
_also, the screen builders and the three *-api-results routes),
web/templates/_reverse_offer.html, every search-results row partial, base.html
(offer script; a block holding only the offer stays visible), search.html, meal.html,
food_analyze_portion.html (pass <box>_also on).
Measured 2026-11-12 against live USDA: of the six orders of "beans red small" five gave
the same 19 results; "small red beans" gave 26, 13 of them new. Same pattern for
"bread wheat whole" / "whole wheat bread". Offered rather than automatic: one more
USDA request per search. The offer's inputs use form="numa-no-form" so they belong to
no form (Compare's results sit inside a POST form the unsaved-changes guard watches).
```

-->

**PROGRAM: HOW TO WRITE A SEARCH, UNDER EVERY SEARCH BOX**

Every food and recipe search box now has the same short hint under it: put your most important word first, put `!` before a word to leave it out, and type a code or barcode to go straight to one item. A **Learn more** link opens the full explanation. [learn more...](#search-ranking)

<!--

```
Scope: web/templates/_search_hint.html (now the one hint), the seven pages that had
their own "most important word first" line (search, analyze-portion, compare,
convert, pantry, recipe_edit, meal), web/static/style.css (comment only).
The meal panel renders the hint in the old tip's slot beside the search box
(class add-food-tip) instead of a second line below. The two source-picker pages
(food_custom_edit, food_fill_from) gain the word-order tip, which they never had.
```

-->

**PROGRAM: COOKED FOODS SEARCH NO LONGER MISSES CANNED ONES**

A search such as `beans red cooked` now also finds canned beans and other online products whose names don't say "cooked". Names that do say "cooked" still rank first. [learn more...](#search-prep-words)

<!--

```
Scope: web/backend.py (_search_api_query, _run_food_search).
usda_api.search_foods keeps only names containing every word sent, so sending
"cooked" dropped every canned product. Prep-state words (_SEARCH_PREP_WORDS) were
already left out of the online query by the meal panel (clean_query=True); now every
search screen leaves them out. Ranking still uses the whole query. The prep-word check
is now case-insensitive.
```

-->

**PROGRAM: SEARCH SAYS HOW MANY RESULTS ITS ! WORDS HID**

When `!` words leave results out of a food search, the list ends with a line such as "6 matches hidden by `!kidney`", so a source showing nothing isn't mistaken for one that found nothing. [learn more...](#search-exclude)

<!--

```
Scope: web/backend.py (_SearchResults, _run_food_search), web/templates/_excluded_note.html,
every search-results row partial, base.html, search.html, food_analyze_portion.html.
Reported for "beans red cooked !kidney": every cooked red bean USDA has is a kidney
bean, so no USDA rows remained and nothing said why. _run_food_search returns a list
subclass carrying hidden_by_exclusion (dropped rows the Source filter would have shown)
and excluded. The note row is classed search-group-divider with no data-row-key, so row
counters skip it (search.html and food_analyze_portion.html now count
tr:not(.search-group-divider), which also stops section dividers counting as results),
and base.html keeps a block holding only that note visible.
```

-->

**PROGRAM: LEAVE WORDS OUT OF A SEARCH WITH !**

Type `!` in front of a word in any food or recipe search box to drop every result whose name has that word: `beans red !kidney cooked` finds cooked red beans, but not kidney beans. [learn more...](#search-exclude)

<!--

```
Scope: numa_app/services/search_ranking.py (split_excluded_words, has_excluded_word),
web/backend.py (_run_food_search), numa_app/services/search_suggest.py.
_run_food_search() strips "!word" terms first, so local matching, ranking and the
online queries see only the remaining words; rows whose name has an excluded word
(matched like word_in_name) are dropped before sorting and capping. A query of only
"!" words returns no rows. Did-you-mean suggestions ignore "!" words. List-filter boxes
(Recipes list, Food Cache, ...) don't parse "!" yet.
```

-->

**PROGRAM: COMPARE PICKS KEPT ACROSS SEARCHES AND LISTS**

Tick foods in one search, search for something else and tick more, even go to Recipes, My Pantry or Food Cache and tick there: every **Compare nutrition of selected** button now compares everything you have picked, not just the ticks on the page in front of you. A note under each Compare button lists your picks, with an ✕ to drop one. A custom profile's Edit page and **Fill in nutrients from another food** keep their own picks the same way. [learn more...](#compare-picks)

<!--

```
Scope: web/templates/base.html (one script for every Compare column),
compare.html, food_cache.html and pantry.html (their own button-color
scripts removed: base.html now colors the button by the number of picks).
Picks live in sessionStorage (numa_compare_picks; per food for the
"Compare checked foods with this one" forms), are re-ticked on load and
after the online rows arrive, and go in as hidden fields on submit,
off_code included; cleared when /compare next loads. Previously a new
search reloaded the page and dropped every tick (only Compare's own
search carried ticks over, via then_search). Browser test
tests/e2e/test_compare_picks_e2e.py.
```

-->

**PROGRAM: ARROW KEYS MOVE THROUGH SEARCH RESULTS**

In every search list (Recipes, Foods search, a meal's or recipe's add search, My Pantry and the rest), the `↓` and `↑` keys now move the red outline from one result to the next, and `Enter` opens it. Come back with `Alt+←` or Back and the outline is on that same result again. [learn more...](#search-keys)

<!--

```
Scope: web/templates/base.html (one script, every [data-search-output]).
Arrow keys move focus to the same kind of element in the next/previous
result row (tbody tr / .list-group-item): an amount text box to the next
amount box, else the row's link; rows without one (dividers) are skipped;
number boxes, selects and textareas keep their own arrows. focusin on a
result saves the row (data-row-key, else its link's href, else its index)
in sessionStorage per page address; pageshow after Back (bfcache or
back_forward navigation) focuses it again, and again once the online
results replace the rows (numa:search-rows). Browser test
tests/e2e/test_search_arrow_keys_e2e.py.
```

-->

**PROGRAM: PRINT PAGES AND OTHER NUMA LINKS STAY IN NUMA'S WINDOW**

The Print / Save buttons for recipes, recipe translations, meals, days and the Nutrient Plot now open their print page in NuMa's own window, with a **Back** button to return. So do the Food Search link on the What-if pages, the Annotate page's "give me a prompt asking Claude AI" link (which now has a link back to Annotate), and the names of suggested foods and recipes in complement suggestions. Links to outside websites, such as claude.ai and GitHub, still open in your browser. [learn more...](#two-windows)

<!--

```
Scope: removed target="_blank" from every link/form to a NuMa page:
recipe_detail.html (print, translation print), recipe_translate.html,
meal.html, meal_day.html, nutrient_plot.html (print pages, each with its
own Back), analysis_food_use(_recipes).html (Food Search), food_annotate.html
gi-claude-form (claude_fetch.html gi_only now links back to Annotate),
backend._item_link. From NuMa's app window a new tab/window goes to the
system default browser, unannounced. Test test_numa_links_stay_in_numas_window
scans templates for any <a>/<form> to "/..." with _blank. The Ctrl/middle-
click new-tab notice (base.html) is deliberate and unchanged.
```

-->

**PROGRAM: COMPLETE AND DRINK BOXES IN THE ADD-INGREDIENT, MEAL AND PANTRY SEARCHES**

When you search to add an ingredient to a recipe, a food or recipe to a meal, or a food to My Pantry, each result now has small **Complete** and **Drink** boxes under its name (recipes get both, your own foods get Drink). Ticking one saves at once and leaves your search as it was. [learn more...](#water)

<!--

```
Scope: _recipe_search_rows.html (Edit Recipe), _add_food_row.html (meal),
_pantry_search_rows.html, via the new _row_toggles.labeled(food) macro
(box() gained an optional visible label). style.css .row-toggles.
base.html: js-row-toggle forms are no longer dirty-tracked: the checkbox's
inline onchange submits before the change event reaches the form's
tracker, so the tracker marked an already-saved form dirty and the page
warned "leave site?" (also affected the Recipes list / Foods search boxes).
```

-->

**PROGRAM: MARK DRINKS AND COMPLETE RECIPES FROM FOODS SEARCH RESULTS**

Foods search results now have the same checkboxes as the Recipes list: a recipe row has **Complete** and **Drink**, and a food of your own (Pantry or Cache) has **Drink**. Ticking or unticking one saves at once, and the results stay where they are. [learn more...](#food-search)

<!--

```
Scope: Foods -> Search (web/templates/_search_result_row.html, search.html,
_search_api_rows.html; dividers colspan 12 -> 14). New shared macro
_row_toggles.html (also used by recipes.html). base.html js-row-toggle is
now a delegated document submit listener (search rows arrive by fetch) that
fills `next` with the current URL for the no-fetch fallback. /food/{id}/drink
answers X-Numa-Ajax with JSON. Search rows carry is_drink (cached foods:
the foods SELECTs in db.search_cached_foods and the code/barcode lookups
now read is_drink) and complete (recipes). Uncached USDA/OFF rows: a dash.
```

-->

**PROGRAM: MARK RECIPES COMPLETE OR AS DRINKS FROM THE RECIPES LIST**

Every row of the Recipes list, including a filtered list, now has a **Complete** checkbox and a **Drink** checkbox. Each shows the recipe's current setting, and ticking or unticking it saves at once, without leaving the list. [learn more...](#recipes)

<!--

```
Scope: Recipes (web/templates/recipes.html); web/backend.py new POST
/recipe/{id}/complete (db.set_recipe_complete), /recipe/{id}/drink now
answers an X-Numa-Ajax request with JSON; base.html js-row-toggle forms
(handleRowForm fetch, falls back to a full submit that returns to the
same filtered list via `next`). db.recipe_list / recipe_list_recent now
return is_drink. The Drink column follows track_water(), like the recipe
page's own drink toggle; changing it recomputes DCP/nutrients as before.
```

-->

**PROGRAM: MANUAL SEARCH RESULTS OPEN THE RIGHT SECTION, HIGHLIGHTED**

In the manual's search, pressing Tab after the checkboxes now lands on the first result, with a clear outline, and Enter opens that section with your search words highlighted. The section you picked is shown at the top of the screen, so the "you are here" bar and the sidebar name it. [learn more...](#search-howto)

<!--

```
Scope: scripts/build_manual.py (regenerates user-manual.html).
Firefox makes any scrolling box a Tab stop, so Tab landed on the
#search-results <ul> itself; Enter there did nothing (no section opened,
nothing highlighted), and one more Tab reached result 1. Fix: tabindex=-1
on the list. The list's overflow also clipped the default focus ring, so
result 1 looked unfocused even in Chromium: :focus-visible now draws inside
the link. openResult() centred the first match, leaving the picked
heading mid-screen and the breadcrumb/scroll-spy naming the section above;
scrollToMark(0, true) now keeps the heading at the top when the match is
within 70% of a screen below it. The scroll-spy's 100px reading line was
above where a jump parks a heading whose breadcrumb wraps (its own
scroll-margin-top), so the section above stayed "current"; the line is
now max(100, that heading's margin + 4). Search jumps are instant, not
smooth (a long smooth glide in Chromium was still under way after 1.3 s).
```

-->

**PROGRAM: MEAL ITEMS SHOW THE TIME THEY WERE ENTERED**

Each food or recipe you add to a meal now records the time of day you entered it (hours and minutes, from your computer's clock), and the meal's Items list shows it in a new **Time** column. Items logged before this change show a dash. [learn more...](#meal-detail)

<!--

```
Scope: db.py (meal_items.added_time TEXT column + migration; _now_hhmm();
meal_add_food/meal_add_recipe stamp it, meal_copy_items stamps copies with
the copy time); web/backend.py _meal_expand_for_diaas carries added_time
into the item dicts; web/templates/meal.html Items table gets a Time column
(serving-changed warning row colspan 4 -> 6). Every add path (search add,
add recipe / as ingredients, bulk add to selected meals, What-if apply,
copy meal) goes through those db functions. Editing an item keeps its time.
NuMa's server runs on the user's machine, so the server clock is theirs.
```

-->

#### November 11 updates

**PROGRAM: DELETE A FOOD FROM ITS OWN PAGE**

A food's page now has a **Delete this food** button, so you no longer have to find the food in a list to delete it. As everywhere else, a food still used by a recipe, meal or your pantry can't be deleted, and the page tells you what is using it. [learn more...](#delete-food)

<!--

```
Scope: web/templates/food_detail.html (second button row, with Annotate and Copy);
web/backend.py food_cache_delete() takes return_to="food-page" and redirects to
/food/cache?deleted=<name> (food_cache_get gains `deleted`, food_cache.html shows
"Deleted <name>."). Refusal for a referenced food is the route's existing
redirect to the Food Cache list with the blocked explanation. Reported for UD12,
deletable only from the far-right column of its Food Search row.
```

-->

**PROGRAM: PLURAL SEARCH WORDS MATCH SINGULAR NAMES**

A plural word in a search now also matches its singular form in a food or recipe name (and "berry" now finds "berries"), so "green onions" ranks "Green onion, (scallion) ..." as matching both of your words. [learn more...](#search-ranking)

<!--

```
Scope: numa_app/services/search_ranking.py word_in_name() also tries singular
stems (_word_forms: -ies→y, -es, -s; stems of 3+ chars), which feeds relevance
ranking, recipe name matching and the full-local-match check in
_cap_results_preserving_local(). The cached-food SQL search already did this
(db._singular_variant); the ranking did not, so for "green onions" recipe R51
"Hummus, green pea" and cached U2727585 "Green onion ..." both scored one word
and the recipe won the source tiebreak.
```

-->

**PROGRAM: PARTIAL MATCHES NO LONGER CROWD THE TOP OF A SEARCH**

When one of your own foods or recipes matches every word you search for, it now comes first, followed by the online foods that also match every word. Your items that match only some of the words come after those, under a "Partial matches from your recipes, pantry, and food cache" heading. They are still listed. [learn more...](#search-ranking)

<!--

```
Scope: every food/recipe search screen (meal add-food panel, Foods → Search, recipe
ingredient search, Compare, Convert, Pantry, source pickers). web/backend.py
_cap_results_preserving_local() takes the query; when a local row matches every query
word (search_ranking.word_in_name), only those rows lead, then the capped external
block, then the remaining (partial) local rows — never dropped. With no full local
match the old local-first grouping is unchanged (the "vitamins daily" case). The 11
row templates gained a third divider. Reported: "jam cherry black" on a meal page put
four recipes matching only "black" (recipes match on any word) above USDA's Black
Cherry Jam foods, even though the cached Black Cherry Jam matched all three words.
```

-->

**PROGRAM: PROBLEMS BY FOOD**

You can now see everything wrong with a food in one place, with a fix button for each item, a box to borrow values from another food you name, and, where it applies, a button to mark an item not needed. The new **Problems by food** page (top of Foods → 9) has one entry per food, covering every check that page makes. Each food's own page shows the same list as **Everything to check on this food**. [learn more...](#problems-by-food)

<!--
```
Scope: numa_app/services/data_quality.py (problems_by_food(), SEVERITY_ORDER),
web/backend.py (/food/cache/problems, _food_problems(), _fixed_food(); data-fix takes
`next`; the food page uses food_problems in place of quality_issues),
templates food_cache_problems.html, _food_problem_items.html, _food_problems_box.html,
food_detail.html, food_cache_db_check.html; style.css; tests/test_data_quality.py.
problems_by_food() runs the existing checks (food_issues, completeness gaps, in-use
AA/portions/GI lists, generic density, stale amounts, wet/dry, duplicate groups, old
USDA copies, bad_json) and regroups them by fdc_id. Nothing is computed twice: the
same functions feed Foods -> 9. Whole-DB run is ~70 ms on 284 foods, so the food page
calls it and filters. A food's AA gap is told once (as the in-use item, with its fill
link) when both apply. Missing-group checks follow Foods -> 9's saved group picker.
Items carry `ignores` (data-ignore groups incl. calories_ok, portions, and "gi" ->
food_annotations.gi_no_prompt, newly accepted by POST /food/{id}/data-ignore; or a
duplicate group's dismiss key, POST /food/cache/duplicates/dismiss now takes `next`).
```
-->

#### November 10 updates

**PROGRAM: INSTALLED NUMA SAYS WHEN IT NEEDS RESTARTING**

After **Update Now**, every page of an installed NuMa now shows a yellow bar saying the new version is installed but the old one is still running, until you quit NuMa (Ctrl+Q) and start it again. Before, only the green message on the Home page said so, once. [learn more...](#ts-crash)

<!--
```
Scope: web/backend.py (_exe_identity, _STARTED_EXE, _restart_needed for frozen
installs), web/templates/base.html (banner wording when frozen), tests/test_web.py.
Cause found 2026-11-10: the owner's old install (Sep 27 build) kept running after
Update Now and failed on Analysis pages reading recipes.gl_g, which the new version
had just dropped from the shared database. A packaged install now remembers its
program file's inode/size/mtime at start; Update Now's os.replace changes them, so
the restart bar (and the 503 restart page on a crash) apply as they do from source.
```
-->

**PROGRAM: ERRORS ARE WRITTEN TO A LOG FILE**

When a page fails with "Internal Server Error", NuMa now writes what went wrong, with the technical detail, to `numa-errors.log` in its data folder, so there's something to send when you report a problem. [learn more...](#error-log)

<!--
```
Scope: web/backend.py (_error_log_path, _get_error_logger, _log_error in
_restart_needed_middleware), tests/conftest.py (tests write the log, and read
downloaded manuals, in tmp_path, never the real data folder), tests/test_web.py.
RotatingFileHandler, 1 MB, one backup; logs method, path, VERSION and the traceback.
```
-->


## Release v2026-11-10-2201 — dated entries released in it

#### November 10 updates

**PROGRAM: NEW STARTER FOODS AND RECIPES**

Five starter foods are new: dark seedless raisins, ground flax seeds, soy protein isolate powder, deglet noor dates and Chinese five spice powder. So are three starter recipes: walnut milk, a Mexican coffee made with it, and a black bean and quinoa meal without hemp. The starter granulated sugar, almonds and graham crackers are improved. After updating, NuMa lists what's new and improved in Settings → 11, where you choose what to take. [learn more...](#starter-data)

<!--
```
Scope: numa_app/services/starter_data.json (scripts/export_starter_data.py from the
curator DB): 49 -> 54 foods (five spice auto-included as an ingredient of a starred
recipe), 8 -> 11 recipes; portions changed on sugar, almonds, graham crackers,
nutrients on sugar. Three data problems the shipped-clean test caught were fixed in the
curator DB first: raisins' amino acids and five spice's vitamins marked not needed,
Walnut milk's vanilla amount updated.
```
-->

**MANUAL: MONTHLY FULL MANUAL AUDIT**

The whole manual was read against the program as it is today. The install and start-up steps now describe NuMa's own window, not a browser tab. Sections on colors, columns, buttons and settings that had drifted from the screens now match them, and a few things that no longer exist are gone. The message after an in-place update now says to close NuMa's window (or tab). [learn more...](#periodic-review)

<!--
```
Scope: user-manual.md throughout; web/templates/home.html (updated-message wording) +
tests/test_web.py. Also this session: mutation testing of recipe_nutrients.py (README
log; 13 tests in tests/test_water.py TestCookedWaterEdges, no code change).
Notable manual fixes: own-window wording in Part 1 A (Windows/Linux run, quit,
update steps), Part 1 "What kind of program", Part 3 intro and A, How to read; GI
table built in Settings 7 (was "item 11"); Part 2 nav description, duplicated Food
use bullet, GI "fills in automatically" contradiction, test count; Daily Summary
column order; Foods 9 check list (no GI, days eaten, wet/dry); Meals list columns;
food page section order; two-food combinations "up to six" (was three + show more);
"Use the full ... g this time"; antinutrient notes in Anti-nutrients section (no
Bioavailability section any more: Part 5 single-food block rewritten to Protein
Summary); color legend orange/blue swapped in Part 5 color-coding and Part 4 V
(rda-near is blue, rda-low orange); nutrient table columns (Minimum/Target/Maximum,
no "Daily goal"); DCP column on meal+recipe pages; ratio-bar legend colors; Day DCP
is the pooled day figure (sum only as fallback); Calculate dropdown "All meals and
days"; What-if GL is recalculated (was "isn't yet"); search results columns (Notes,
Food, Delete; no CONF.); pantry Archived badge (no ARCH column); digestibility tags
~est/user; servings-0 mode removed (forms require >= 1); profile switch default in
Part 8 E; oxalate/GI troubleshooting; stale "see the Aug 11 / Sep 19 entries" links;
contact email given in Part 8 G and Part 9; new glossary entry AI (artificial
intelligence), 11 Claude links moved to it from gloss-ai (Adequate Intake); search
terms on 6 sections; "weight loss" added to the calorie target's terms.
```
-->

**MANUAL: WEEKLY SWEEP**

This log now keeps the last two weeks of entries. The food-data section now gives CIQUAL's current size (about 3,500 foods). Searching the manual for *exit*, *shut down* or *missing recipe* now finds the right sections. On a food's Portions page, a row's **Save** button no longer grows when it lights up, so the Description box beside it stays the same size as you type. [learn more...](#food-data)

<!--
```
Scope: user-manual.md Part 11 (Oct 14-26 entries pruned), Part 7 A (CIQUAL ~3,200 ->
~3,500: the 2025 edition has 3,484), search terms on Part 3 B (#web-shortcuts) and
Part 8 C (#ts-deleted-recipe); README.md feature list (What-if applies any change;
"Runs like a desktop program"); README-numa-documentation.md monthly check (Project
Structure: 16 templates, browser_quit.py, vitamin_k_repair.py, launch-web.sh,
nutrimagnus.spec, workflows added, recipes.html / whatif_apply descriptions fixed;
schema columns incl. dead recipes.gl_g / saved_analysis_*; .venv is Python 3.14 locally
vs 3.12 in CI; CIQUAL 2025 count; test counts).
Fixes found by running the browser tests (Playwright's browser had to be reinstalled
after its update): the Portions page's Save button (.btn-dirty: bold + 2px border)
widened ~4 px when lit, squeezing the Description box - new .btn-steady (style.css:
hidden bold copy of the label via ::after content: attr(data-label), 1 px extra padding
standing in for the border); the manual-bookmark tests now open /manual/page (the
manual moved into a frame); test_complements_properties' pair-cascade test now sizes
A and B at their own digestibility, as suggest_complements() has since October (a
saved Hypothesis example had been failing on every run). New browser test for the
Ctrl+click notice.
```
-->

**PROGRAM: CTRL+CLICK EXPLAINS ITS BROWSER TAB FIRST**

In NuMa's own window, Ctrl+click, Shift+click or middle-click on a NuMa link opens that page in an ordinary browser tab, which is useful for two pages side by side but surprising the first time. NuMa's window now says so before the tab opens, and how to get back, until you tick "Don't show this again" (or untick it in Settings → 13). [learn more...](#two-windows)

<!--
```
Scope: web/templates/base.html, web/backend.py, web/templates/settings.html,
tests/test_web.py; manual Part 3 B "Working in two windows" (#two-windows).

The app window is recognised by window.name: /nutrimagnus(-source) now redirects
to /?numa_window=1, and base.html sets window.name = "numa-app-window" and strips
the parameter. window.name survives the window's same-origin navigations and is
not copied to tabs opened from it, so ordinary tabs never show the notice. A
capture-phase click/auxclick listener catches modified or middle clicks on
same-origin links (not target=_blank, download, # or javascript:), shows a
<dialog>, and on "Open it" calls window.open(url, "_blank") with opener nulled.
Pref: prefs.json new_tab_notice (default on); POST /prefs/new-tab-notice turns it
off; Settings -> 13's form sets it (shares the app_window_shown flag). Also: the
leave guard's unsaved-changes prompt no longer fires on a Ctrl/Shift/Cmd- or
middle-click, since that opens another tab and leaves the edits in place.
```
-->

**PROGRAM: A RECIPE IN USE CAN BE ARCHIVED, NOT DELETED**

A recipe that's logged in a meal or used inside another recipe can no longer be deleted. Clicking Delete says where it's used and offers to archive it instead, which hides it from lists and searches while everything using it keeps working. A recipe nothing uses deletes as before. [learn more...](#delete-recipe-elsewhere)

<!--

```
Scope: web/backend.py recipe_delete_post (refuses when recipe_referencing_subrecipe
or recipe_meal_use finds a use; ajax → blocked_html row note, else
recipe_delete_blocked.html), _recipe_delete_warning (None for a used recipe, so
no confirm), new _recipe_delete_blocked.html / recipe_delete_blocked.html,
recipes.html / recipe_detail.html (onsubmit only when there's a warning).
db.recipe_delete itself is unchanged (still flags sub-recipe lines) for
older data and tests that simulate it.
```

-->

**PROGRAM: FOODS → 9 LISTS MEALS AND RECIPES NAMING A DELETED RECIPE**

The meals and recipes that still name a deleted recipe, formerly behind a button on the Recipes list, are now in Foods → 9, Check database integrity and completeness, with how to reconnect each one. [learn more...](#relink-recipe)

<!--

```
Scope: db.check_db_integrity gains deleted_subrecipe_refs (recipe_ingredients
with ref_recipe_deleted = 1; not auto-repaired, so excluded from "repairable");
meal items pointing at a deleted recipe were already in orphaned_meal_items and
now carry a relink hint. food_cache_db_check.html new #deleted-recipes section.
/recipes/broken-refs now redirects to /food/cache/db-check#integrity;
recipe_broken_refs.html and the Recipes-list button removed. These also now
count toward the Home page's data-check reminder.
```

-->

**PROGRAM: THE MANUAL OPENS IN NUMA'S OWN WINDOW**

The manual now opens in NuMa's window, under NuMa's menu, instead of in a separate browser tab. A yellow bar above it explains how to get back: its **← Back** button, or **Alt+←** (with **Alt+→** to go forward again). [learn more...](#manual-back)

<!--

```
Scope: web/backend.py (/manual now renders manual_frame.html; the manual's own
HTML moved to /manual/page), web/templates/manual_frame.html (new), base.html
(footer block; Manual nav link no longer target=_blank), home.html,
_search_hint.html, _manual_link(). The manual is framed rather than restyled:
its sidebar, scroll-spy and search are all keyed to the whole viewport. The
frame page forwards a /manual#anchor to the iframe, sends manual links to NuMa
pages to the whole window, and passes Ctrl/Alt keystrokes typed in the manual
to the outer page so Ctrl+Q and the Alt+Shift menu shortcuts still work.
```

-->

**PROGRAM: A WEIGHT WITH A NOTE IN BRACKETS KEEPS THE NOTE**

You can type an amount as a weight with a note in brackets, such as `134.1 g (2/3 c)` or `50 g (1 slice)`: the weight is what counts, and the note is kept and shown as you typed it. That's the same form NuMa shows a weighed volume in, so an amount's Edit box can now be saved unchanged without losing its volume. Anything else after a weight (`134.1 g 2/3 c`) is refused with a message saying to put it in brackets. Amounts now have their own section in the manual, covering every form NuMa accepts, how each is read, and what's refused. [learn more...](#weight-and-volume)

<!--

```
Scope: web/backend.py _parse_portion_str_raw(); tests/test_web.py
TestParsePortionStrWeightWithNote; user-manual.md Part 6 K (new, "Entering
amounts in meals and recipes", #amount-formats), Part 6 J, Part 10.

Root cause: the weight-unit branch returned "<number> <unit>" as soon as it
saw a weight unit, ignoring every token after it. So "134.1 g (2/3 c)" was
stored as "134.1 g" (volume lost), and "134.1 g banana" was accepted. Since
"2/3 c 134.1 g" and Keep as entered both store "<weight> (<volume>)",
re-saving such an amount unchanged from its Edit box silently lost the
volume label (grams were always right).

Now: "<weight> (<note>)" (bare number = grams) returns the weight, label
"<weight label> (<note>)" with the note verbatim (whitespace collapsed);
unbracketed text after a weight returns an error naming it.
"2/3 c (134.1 g)" stays refused (older NuMa's own density-estimate form,
which data_quality treats as "bracketed", not user-weighed). Checked
against every stored meal/recipe unit in the live DB: no stored label's
parse result changes.

Manual: Appendix E "Portion Input Formats" (stale: said an unknown-density
volume asks for a weight) and Part 6 J's Amounts table merged into the new
Part 6 K (anchor renamed #portion-formats -> #amount-formats: a portion
is a food's named measure with its weight, an amount is anything typed;
the pN subsection is #portion-shortcuts), keeping #portions-vs-servings;
CSV section K -> L; Appendix F -> E (two "Appendix F" references updated).
J's table row "2 (for a recipe) = servings" and refusal "2 cups with no
density" were wrong and are gone.
```

-->

#### November 9 updates

**PROGRAM: CTRL+Q QUITS NUMA**

Press **Ctrl+Q** on any NuMa page to stop NuMa and close its window (it asks first if the page has unsaved changes). In Firefox, Ctrl+Q quits Firefox, and NuMa now stops along with it. [learn more...](#quit-numa)

<!--

```
Scope: numa_app/services/browser_quit.py (new), web/backend.py (POST /quit,
_stop_numa, Firefox-watch middleware, start_browser_watch), web/launcher.py,
web/templates/base.html (Ctrl+Q handler; numaDirtyGuard.anyDirty and
numaLeaveGuard.anyDirty for its unsaved-changes check), settings.html section 12,
tests/test_browser_quit.py, tests/test_web.py.
Modelled on cmgr's Ctrl+Q. /quit answers, then a thread waits 0.5 s, asks KWin (qdbus
loadScript) to close the window whose resourceClass ends "__nutrimagnus[-source]-Default",
and sets the launcher's uvicorn server.should_exit (app.state.server), with os._exit 5 s
later as a backstop; in --reload mode it SIGTERMs the reloader parent instead.
Firefox reserves Ctrl+Q (never dispatched to content), so FirefoxWatch: a middleware
records whether the latest HTML GET came from a Firefox UA; a daemon thread checks every
2 s for a Firefox main process (/proc cmdline basename firefox/firefox-bin/..., not
-contentproc; tasklist on Windows; pgrep elsewhere) and stops NuMa after 2 consecutive
misses following a sighting. Not started under tests. Tab close alone doesn't trigger it.
```

-->

**PROGRAM: NUMA OPENS IN ITS OWN WINDOW**

Starting NuMa now opens it in a window of its own, with no tabs and no address bar and its own taskbar entry showing NuMa's icon, like a desktop program. It needs Chrome, Chromium, Brave, Edge or Vivaldi installed (running or not). If none is installed, or you've chosen Firefox, it opens in a normal tab as before. Turn it off in **Settings → 13. Browser to Launch**. [learn more...](#browser-to-launch)

<!--

```
Scope: web/launcher.py, web/backend.py (/settings/browser, settings context), settings.html section 13.
Chromium-family "app mode": the launcher runs <browser> --app=URL. New prefs.json key
app_window (default true). _app_window_browser(): a Settings-chosen browser is used only
if Chromium-family; with "Ask each time", a running Chromium-family browser wins, then
any installed one (chromium, google-chrome, brave, microsoft-edge, vivaldi), and no
which-browser dialog. Falls back to the old normal-tab path. Also: brave/brave-browser
and microsoft-edge(-stable) alternates, and known install paths on Windows/macOS where
these browsers are rarely on PATH. The form's hidden app_window_shown field tells an
unticked checkbox from an absent one.
Window icon: the window opens at /nutrimagnus (release) or /nutrimagnus-source (source),
which backend.py redirects to /. Chromium names an --app window from host + path (not
port): chrome-127.0.0.1__nutrimagnus-Default. Linux desktops match that name to a menu
entry's file name or StartupWMClass= for the taskbar icon, so install-linux.sh's and
deploy/nutrimagnus-web.desktop's entries carry StartupWMClass; for any window name no
entry claims (Brave, Edge...), the launcher writes a hidden matching .desktop in
~/.local/share/applications (icon copied to ~/.local/share/icons/nutrimagnus-window.png,
since a packaged build's bundle folder is temporary). Windows takes the taskbar icon
from the page icon: new /favicon.ico route plus <link rel="icon"> in base.html.
Verified on KDE Plasma Wayland with snap Chromium; Windows not yet checked.
```

-->

**PROGRAM: WHAT-IF CAN APPLY ANY CHANGE FOR REAL**

**Apply these changes for real…** now works for Remove, Add and Change amount as well as Replace, on What-if: Meals and What-if: Recipes. On meals, an addition goes into a new meal called "Added by what-if" on each day, and Change amount also finds a recipe logged as individual ingredients. On recipes, the confirmation page says how many logged meals will change with them and lists recipes whose stored total weight or water once cooked to check afterwards. [learn more...](#whatif-apply)

<!--

```
Scope: Analysis -> What-if: meals / recipes -> Apply for real.
whatif.py: real_substitution_problems(edits, page, conn) allows all four ops on both pages (replace basis rule unchanged; scale must be > 0); refuses an item changed twice, a replacement that another edit changes, and (with conn) an added/replacement recipe containing an item another edit changes. Scale of a recipe logged as ingredients: _apply_logged_ingredient_removals now also handles scale via _Ctx.row_scale (meal_breakdown multiplies those rows).
db.py: amount_text(), scale_item_in_meals(), scale_meal_item(), remove_item_from_recipes(), scale_item_in_recipes().
backend: _whatif_apply_plan() adds new_meal_days (meals add), recipe-add loop refusal, "weighted" (recipes with total_weight / cooked water among those changed other than by a food-for-food replace), meals_affected (meals logging changed recipes or ancestors). POST applies in order remove, scale, replace, add; meals add -> one "Added by what-if" meal per day (WHATIF_ADDED_MEAL_NAME); recipes add -> recipe_add_ingredient, amount per serving x servings when per=serving. _whatif_page_extras hides Apply when ?applied= is present.
Tests: test_whatif.py apply tests.
```

-->

**PROGRAM: WHAT-IF: MEALS CAN APPLY A REMOVE FOR REAL**

**Apply these changes for real…** now also appears when a what-if on meals removes foods or recipes, not only when it replaces them. The confirmation page lists each meal that will change; a recipe logged as individual ingredients has just the matched foods deleted. [learn more...](#whatif-apply)

<!--

```
Scope: Analysis -> What-if: meals -> Apply for real. whatif.real_substitution_problems(edits, page): remove allowed on the meals page (not recipes); refusal text says "changed more than once" / "removes or replaces". Edit report "ingredient_rows" (meal id -> meal item ids) from _logged_ingredient_sets. backend _whatif_apply_plan(): a remove's meals = meals_with_direct_item | ingredient_rows meals; POST /analysis/whatif/apply does removes first (meal_remove_item per matched row + mark_meal_stale; db.remove_item_from_meals for direct rows), then replaces, one transaction. Button/heading/confirm wording "changes" instead of "replacements". Tests: test_whatif.py apply tests.
```

-->

**PROGRAM: WHAT-IF REMOVES A RECIPE LOGGED AS INDIVIDUAL INGREDIENTS**

Removing a recipe in What-if: Meals now also takes it out of meals where you added it as individual ingredients: the foods matching its ingredients and amounts go together, and other copies of the same foods stay. When a meal looks like it holds the recipe's ingredients but their amounts no longer match the recipe, the page names that meal instead of saying only "not found". [learn more...](#whatif-ingredients)

<!--

```
Scope: Analysis -> What-if: meals. numa_app/services/whatif.py: _logged_ingredient_sets() matches the recipe's expand_recipe_ingredients() leaves (one batch) to meal food rows with the same fdc_id at one common scale (anchor = largest leaf, tolerance 0.5%, newest rows first, repeated for several sets); _apply_logged_ingredient_removals() runs per meal before the "after" breakdown and puts matched row ids in _Ctx.skip_rows, which meal_breakdown() skips. Recipes with < 2 leaves never match. No match but >= 60% (min 2) of the recipe's distinct foods present -> edit report "loose_meal_ids". Edit report gains "as_ingredients". Template: analysis_whatif.html change list. Remove only. Tests: tests/test_whatif.py::TestRecipeLoggedAsIngredients.
```

-->

**PROGRAM: NUTRIENT PLOT SAYS HOW MANY DAYS IT'S SMOOTHED OVER**

The small line of text under the Nutrient Plot's title now ends with "Data smoothed over 3 days." (using the number in **Smoothing (days)**), and appears on its own when the plot has no goal or limit lines. With smoothing off it's left out. [learn more...](#nutrient-plot)

<!--

```
Scope: Daily Summary -> Nutrient Plot image (and the Home page plot, same image route). web/backend.py: _nutrient_plot_add_smoothing_note() appends the note inside the subtitle's parentheses in nutrient_plot_image; window <= 1 adds nothing. Test: test_nutrient_plot_subtitle_smoothing_note.
```

-->

**PROGRAM: WATER IN A RECIPE COUNTS AS FOOD UNLESS THE RECIPE IS A DRINK**

All the water in a recipe now counts as water from food, even from ingredients that are drinks on their own, such as the tap water in a bread dough; tick **This recipe is a drink** to count it all as drinks. A recipe with drink ingredients says so in a blue note on its page. Meals using such recipes were recalculated once. Every food and recipe in a meal's items, a recipe's ingredients, a day's list of meals and *Analyze a saved recipe portion* now shows its grams of water beside its name, "(72% water, 98 g)". [learn more...](#water-in-recipes)

<!--

```
Scope: recipe_nutrients.expand_recipe_ingredients tags each leaf with the recipe's
(or an enclosing recipe's) drink flag only, no longer `_drink or is_drink(food)`;
leaves carry food_is_drink for drink_ingredient_water(), which feeds the recipe page's
#drink-water-note. Meal-level foods keep their own flag (_meal_expand_for_diaas,
whatif). db.init_db: new one_time_steps table; step 'recipe-drink-water' marks stale
every meal logging a recipe that uses a drink food (at any depth) and logs the reason
in meal_recalc_log. _mark_water now also sets water_amount_g (food: water x grams;
recipe: per-serving water x servings) and is called on the day page's meal items and
Analyze a saved recipe portion too; _water_mark.html renders "(N% water, G g)",
"(N% water)" or "(G g water)".
```

-->

**PROGRAM: WATER AFTER COOKING FOR RECIPES**

A recipe's page now has a **Water after cooking** box: give the water the finished dish holds per 100 g (a number, or a food's code to copy its figure) and it replaces the water the raw ingredients add up to, in every meal, day and recipe that uses it. Weigh the batch after cooking and NuMa offers an estimate from the weight it lost. A recipe in a meal or another recipe now shows its water percentage beside its name, as foods do. [learn more...](#cooked-water)

<!--

```
Scope: Recipe page (Water after cooking box, POST /recipe/{id}/cooked-water); new
column recipes.cooked_water_per_100g (db.set_recipe_cooked_water). Applied in
recipe_nutrients.expand_recipe_ingredients via apply_cooked_water(): needs the stated
total_weight (cooked batch weight, not the raw ingredient sum); every leaf's water is
scaled by target/raw so per-food breakdowns still add up, and retagged as food water
unless the recipe or an enclosing one is a drink (so tap water baked into bread stops
counting as drinks). No leaf with a water value -> the whole amount goes on the
heaviest leaf. An outer recipe's own value supersedes its sub-recipes'. Setting it
recomputes the recipe and marks meals using it stale. _mark_water now tags recipe rows
(meal items, sub-recipe ingredients) via recipe_water_per_100g(). Recipe copy carries
the value. Not in recipe CSV export (is_drink isn't either). Prompted by R79 (bread:
4 c water, 2,328 g raw, 2,094 g baked -> 50.7 g/100 g counted vs ~39.6 actual).
```

-->

#### November 7 updates

**PROGRAM: ARCHIVE A RECIPE FROM ITS OWN PAGE**

A recipe's page now has an **Archive recipe** button between **Copy recipe** and **Delete recipe**, so you can hide a recipe without going back to the Recipes list. Once archived, the page shows an "Archived" badge by the title and the button reads **Restore recipe**. [learn more...](#archive)

<!--

```
Scope: web/templates/recipe_detail.html, web/backend.py (recipe_detail
takes archived/restored/still_used flags for its notice;
_recipe_delete_warning archive_here=True on the recipe page),
tests/test_web.py.
Posts to the existing /recipe/{id}/archive toggle with next=/recipe/{id};
the Delete confirm now points at the Archive button next to it.
```

-->

#### November 6 updates

**PROGRAM: NUMA OPENS IN A RUNNING CHROME OR CHROMIUM**

If Chrome or Chromium is the browser you have open when you start NuMa, NuMa now opens its tab there. Before, it gave up on Chrome or Chromium and opened your system's default browser (Firefox, say) instead. [learn more...](#browser-to-launch)

<!--

```
Scope: web/launcher.py (_BROWSER_ALTERNATES, new _resolve_browser()),
tests/test_launcher.py.
A running Chrome or Chromium shows to pgrep -x as "chrome", its internal
binary name (the Chromium snap runs /snap/chromium/.../chrome), but no
"chrome" is on $PATH, so Popen raised OSError and _pick_and_open_browser
fell through to webbrowser.open, the xdg default (Firefox). "chrome" now
tries google-chrome, google-chrome-stable, chromium, chromium-browser;
"google-chrome" also tries google-chrome-stable. _resolve_browser() is used
both to pick the launchable name in detection and to launch.
```

-->

**PROGRAM: NUTRIENT PLOT GOAL LINES NO LONGER HIDE EACH OTHER**

When two nutrients' goal lines (or limit lines) land at the same height on the Nutrient Plot, they're now drawn as one line whose dashes alternate between the two nutrients' colors, so both show. Before, the later line covered the earlier one and a goal seemed to be missing. [learn more...](#nutrient-plot)

<!--

```
Scope: numa_app/services/plotting.py (_draw_reference_lines(),
_REF_PATTERNS, REF_LINE_MERGE_FRACTION), tests/test_web.py.
Seen with Day DCP + Calories: the auto scale factor 28.5 put Calories'
2424 kcal goal at 85.05, on the DCP goal of 85.1, so 5 goals drew as 4.
Reference lines are now collected during the series loop and drawn after
it; same-kind lines within 1% of the y-range are grouped and each drawn
with the same dash period times n, offset by its index, at the group's
mean height.
```

-->

#### November 5 updates

**PROGRAM: PORTIONS PAGE RELOADS AFTER A SAVE**

After you add, edit, reorder or remove a portion, the Portions page now reloads normally, still showing what you just did, instead of giving a "Method Not Allowed" error. Removing a portion now also says "Portion removed." [learn more...](#food-cache-web)

<!--

```
Scope: web/backend.py (food_cache_portions_add/edit/delete/move now
POST-redirect-GET via _portions_redirect(); outcome as done=/error= keys
looked up in _PORTION_DONE / _PORTION_ERRORS by food_cache_portions_get),
tests/test_web.py.
Each POST used to render the page in place, leaving the browser on
/food/cache/{id}/portions/edit (etc.), a POST-only URL, so a reload or a
revisit answered 405. test_nav_memory_skips_post_rendered_pages now uses
/food/cache/claude-fetch as its POST-rendered example.
```

-->

**PROGRAM: SORT BY USE, AND A SORT MENU FOR THE PANTRY**

Food Cache's **Sort by** menu has a new **Used in** choice that puts the foods most recipes and meals use at the top. The Pantry list now has the same **Used in** column and its own **Sort by** menu: Name, Code, Type, DIAAS, GI estimate, Used in, or date Added. NuMa remembers the Pantry choice the way it remembers Food Cache's. [learn more...](#pantry)

<!--

```
Scope: web/backend.py (_FOOD_CACHE_SORT_KEYS["used"], new _PANTRY_SORT_KEYS
built from it plus "added"; pantry_get takes sort, pref "sort_pantry", adds
"use" from data_quality.usage_counts), web/templates/food_cache.html (option),
web/templates/pantry.html (Sort by select, Used in column), tests/test_web.py.
Pantry was previously always in name order (db.pantry_list ORDER BY food_name);
that stays the default. A name-only pantry entry counts as not used and has
an empty code.
```

-->

**PROGRAM: FOOD CACHE SHOWS WHERE EACH FOOD IS USED**

The Food Cache list has a new **Used in** column giving, for each food, how many recipes and logged meals use it, such as "2 recipes, 5 meals", or "not used". [learn more...](#cached)

<!--

```
Scope: web/backend.py (food_cache_get adds "use" from
data_quality.usage_counts), web/templates/food_cache.html (Used in column;
notes-row colspan 10 -> 11), tests/test_web.py.
Counts are distinct recipes with the food as a direct ingredient and
distinct meals with it as a food item; the same counts Duplicate Foods
shows. One extra pass of three GROUP BY queries per page load.
```

-->

**PROGRAM: DELETE BUTTON ON DUPLICATE FOODS**

Each copy listed on Duplicate Foods (Foods → 9 → Find duplicate foods) now has a **Delete** button, so you can remove a copy you don't want without merging anything. It's greyed out on a copy that a recipe, meal or pantry entry still uses; keep another copy for those instead. [learn more...](#duplicate-foods)

<!--

```
Scope: web/templates/food_duplicates.html, web/backend.py (food_cache_delete
return_to, food_cache_duplicates deleted flag), tests/test_web.py.
The button posts to the existing /food/cache/delete with
return_to=/food/cache/duplicates (the only accepted value), which redirects
back with ?deleted=1. Shown enabled only when f.use.total is 0, since that
route refuses to delete a referenced food anyway.
```

-->

#### November 3 updates

**PROGRAM: BARCODE SEARCH ON EVERY FOOD SEARCH BOX**

Typing a product's 12- or 13-digit barcode now finds it from any food search box: a meal's Add Food or Recipe, a recipe's Add Ingredient, the Pantry, Compare, Convert, and the copy-from searches on a food's page. Every one of those boxes also tells you, directly underneath, that it takes a name, an FDC ID or a barcode. [learn more...](#search-ranking)

<!--

```
Scope: web/backend.py (_barcode_digits, _barcode_search_results, _run_food_search,
_search_logic); web/templates/_search_hint.html (new macro) used by search.html,
food_analyze_portion.html, meal.html, recipe_edit.html, pantry.html, compare.html,
food_convert.html, food_fill_from.html, food_custom_edit.html (both pickers);
search-box tooltips mention barcodes. Barcode lookup used to live only in
_search_logic (Food Search, Analyze a Food Portion); every other box runs
_run_food_search, which had code/FDC ID lookup but treated a barcode as a name.
The lookup is now one helper both call. In _run_food_search a barcode never
falls through to a name search: the instant local pass (external=False)
checks only the cache, and the online pass also asks Open Food Facts and caches
the product. So on those pages an uncached barcode needs an online source
ticked (no online pass runs otherwise); Food Search still always looks it up.
The meal-history "Meals that contain" filter is not a food search and is unchanged.
```

-->

#### October 30 updates

**PROGRAM: MISSING PACKAGES INSTALLED AT LAUNCH**

Starting NuMa from source with `web/launch-web.sh` now installs anything in `requirements.txt` that this computer's `.venv` lacks, so a checkout synced to another laptop starts without a package error. If the install fails, you get a desktop notice and NuMa starts anyway.

<!--

```
Scope: web/launch-web.sh. Runs .venv/bin/pip install -q --disable-pip-version-check -r
requirements.txt, by full path, after the old server has stopped and just before
launcher.py starts, so packages never change underneath a running server. About 1 second
when nothing is missing. The if-wrapper keeps set -e from silently ending the launch on a
pip failure (offline, say). pip output goes to web-server.log, and the server now appends
to that log instead of truncating it, so pip errors survive. Installs the test/dev
packages in requirements.txt too; playwright's browsers are not installed by this.
```

-->

**PROGRAM: UPDATE ALL IMPROVED STARTER ITEMS AT ONCE**

**Update all N items to the new version**, under "Improved in this version of NuMa" in Settings → 11, brings every improved starter food and recipe you have up to date in one step, with no need to check them one by one. It asks you to confirm first, since updating replaces any changes you made to those copies. [learn more...](#starter-data)

<!--

```
Scope: Settings -> 11. Starter Data. web/templates/settings.html, web/backend.py.
New POST /settings/starter-data/improve-all takes its list from
demo_data.pending_changes() rather than the form, then calls the same
apply_improvements() as the checked-items route. Covers recipes as well as
foods, matching the list it sits under and "Keep all my copies as they are".
```

-->

**PROGRAM: A SEARCH NOW TAKES YOU TO ITS RESULTS**

After you run a search, its section ("Add Ingredient", "Add Food or Recipe") or, on a page without one, the search form itself comes to the top of the window, with the cursor on the first result: its amount box if it has one, otherwise its name. This works on every page with a search. Very short pages can only scroll as far as their end. [learn more...](#search-web)

<!--

```
Scope: web/templates/base.html (scroll-memory script: submit of a form[data-search-form]
with text in its box stores numa_ui_search_run instead of the submit-scroll offset; on
load + one tick, opens the enclosing <details>, focuses firstSearchResult() and scrolls
the section/form to the top, then the focused result into view if it fell below the
window; scrolls are behavior:'instant' because Bootstrap's smooth scrolling let the
second call cut the first short). numa:search-rows refocuses the first row after online
results replace the rows, unless the cursor has moved; search.html, food_analyze_portion.html
and meal.html now dispatch that event too. data-search-form on each page's main search
form (plus meals.html's history search and Custom Foods' copy search, whose results table
gained data-search-output). Other submits, and an empty box, keep the old scroll behavior.
Tests: tests/e2e/test_search_lands_on_results_e2e.py, test_every_main_search_box_lands_on_its_results.
```

-->

#### October 29 updates

**PROGRAM: ALT+SHIFT+I CLEARS THE OLD SEARCH RESULTS**

Pressing Alt+Shift+I to jump to a search box now also clears the previous search's results (and any "No results" or "Did you mean" line), so the page is ready for your next search. [learn more...](#web-shortcuts)

<!--

```
Scope: web/templates/base.html (Alt+Shift+I branch adds .numa-search-cleared to every
[data-search-output], .search-no-results, .search-suggestions); web/static/style.css
(.numa-search-cleared = display:none !important, so a late online-results fetch setting
inline display can't re-show them). data-search-output marks each page's results region:
_search_results_block.html attrs() (fill-from, compare, convert, pantry, recipe edit),
search.html, food_analyze_portion.html, meal.html, oxalate_link.html; filter-list pages
(food_cache, recipes, meals_search, food_annotate) only when a query is active, so an
unfiltered list is never hidden. Test: test_search_results_marked_for_alt_shift_i_clear.
```

-->

**MANUAL: MOVING FOODS AND RECIPES WITH CSV FILES**

You can now read, step by step, how to export foods and recipes to CSV files and import them on another NuMa install, including what each import does with foods and recipes you already have, and what is left behind. The Help links on both Import CSV pages now open it. [learn more...](#csv-transfer)

<!--

```
Scope: user-manual.md Part 6 K (new, #csv-transfer / #csv-foods / #csv-recipes); Part 2A links;
Backing up your data and the Part 9 CSV entry now link to it; help-link targets in
web/templates/food_cache_import_csv.html (was #food-import) and recipe_import_csv.html (was #recipes).
Facts checked against csv_export.py, csv_import.py (import_foods always creates new user_drafted
foods; resolve_or_import_foods reuses by case-insensitive name), recipe_csv.py (RECIPE_COLUMNS has
no introduction/serving_size; existing recipe names reused untouched; DCP recomputed for new ones).
```

-->


## Release v2026-10-28-1228 — dated entries released in it

#### October 28 updates

**MANUAL: WEEKLY SWEEP**

The section on food search results no longer says recipes always come first (since October 26 the best match comes first), and now says that online searches run side by side and are reused for ten minutes. Five sections gained search words, among them **Annotate a Food**. [learn more...](#food-search)

<!--
```
Scope: weekly sweep, 2026-10-28 (items 1-10, plus the weekly mutation churn
check). Clean: CLAUDE.md layout (1), NuMa capitalization (2), Bootstrap 5.3.8
still current (3), public README.md (6), glossary (9; no new terms).
(4) Log pruned to Oct 14 onward (Oct 13 and older, incl. the v2026-10-09-1637
summary, removed). (5) USDA Food Search Results: "recipes always come first"
replaced (contradicted the Oct 26 ranking change); Oct 27 parallel search /
10-minute reuse written into the body. (7) New tests:
test_remembered_live_search_expires, test_every_plot_line_gets_its_own_marker_shape,
tests/e2e/test_nutrient_plot_e2e.py (instant legend change -> address bar,
both image URLs, Home page). (8) Internal links pass; external: no new URLs;
non-200s all 403/429 bot-blocks except ciqual.anses.fr 503 (twice; likely
temporary) and eatrightpro.org's known SSO redirect loop [^64].
(10) Search terms added: Nutrient Plot, Meal Items Table, USDA Food Search
Results, weight-portion troubleshooting; new line for Annotate a Food.
Mutation churn: aa_estimate.py (7 survivors in scaled_aa, 6 real, closed),
recipe_nutrients.py (2 real gaps in the drink/supplement tagging, closed),
usda_nutrients.py (1 real gap: get_density_g_per_ml never passed last_resort
in a test; closed).
```
-->

**MANUAL: TESTING AND REVIEW DESCRIBED AS THEY STAND TODAY**

The part of the manual that explains why you can trust NuMa now gives the current size of the test suite and the kinds of tests in it, and has a new section on the regular weekly, monthly, quarterly and yearly reviews that keep the manual and the food data up to date. [learn more...](#data-testing-validation)

<!--
```
Scope: Part 2E. "Extensive code testing" replaced by "Automated code testing"
(2,398 tests, the five kinds, mutation testing on eight modules) and a new
"Periodic review" subsection summarizing the README's Maintenance cadences.
```
-->

**PROGRAM: HOME PAGE PLOT FOLLOWS CHANGES MADE ON THE NUTRIENT PLOT PAGE**

While a plot is shown on the Home page, whatever you change on the Nutrient Plot page now shows up on the Home page too, without ticking **Show on Home page** again. [learn more...](#nutrient-plot)

<!--
```
Scope: Analysis -> Daily summary -> Nutrient Plot; web/backend.py
(nutrient_plot_page), web/templates/nutrient_plot.html. Previously the Home
page kept the qs saved at tick time, and any later edit just raised "A
different plot configuration is currently shown on the Home page". Now a
render with has_plot and home_nutrient_plot_enabled saves its qs as
home_nutrient_plot_qs when they differ. The instant (no-reload) Black & white /
Legend placement changes also replaceState the address bar, update the hidden
home-pref qs, and POST it to /summary/nutrient-plot/home-pref while the toggle
is checked. test_nutrient_plot_stale_home_qs_offers_remove_button replaced by
test_nutrient_plot_home_page_copy_follows_changes.
```
-->

**PROGRAM: NUTRIENT PLOT LEGEND CAN SIT IN A COLUMN RIGHT OF THE PLOT**

**Legend placement** on the Nutrient Plot now has a fourth choice, **Right of the plot, in a column**: the names stack one per row beside the plot, long ones wrapped, and the plot keeps its full size. **Auto** now puts the legend there, instead of below the plot, once it won't fit on one row above. On a narrow screen the legend moves below the plot instead, so nothing shrinks to unreadable. [learn more...](#nutrient-plot)

<!--
```
Scope: Analysis -> Daily summary -> Nutrient Plot, Home page plot;
numa_app/services/plotting.py, web/templates/nutrient_plot.html,
web/templates/home.html, web/backend.py (_nutrient_plot_qs keeps any non-auto
legend value). plotting: LEGEND_POSITIONS gains "right"; ncol=1 legend anchored
upper-left at (1.02, 1.0), labelspacing 1.0; _wrap_legend_label wraps at 28 chars
with NBSPs gluing "(...)" groups and the ÷/× scale suffix so neither splits.
bbox_inches="tight" grows the image by the column width, which roughly matches
the width a 6-entry below-plot legend already forced. Responsive: the img sits in
a <picture>; the (min-width: 992px) <source> carries the qs as-is, the fallback
<img> swaps legend=right for legend=bottom (template replace; the page's live
legend-change JS maps right->bottom for that target only). Print view and
downloads use the qs unchanged.

Follow-up same day: auto now resolves to "right" (was "bottom") past one row;
the narrow fallback is a narrow=1 image param (line_plot_image(narrow=True)
turns right -> bottom) instead of a template legend=right string swap, since
auto has no legend param to swap.
```
-->

**PROGRAM: EACH NUTRIENT PLOT LINE HAS ITS OWN POINT SHAPE**

Every line on the Nutrient Plot now marks its points with its own shape (solid circle, square, rectangle, asterisk, #, and more after those), and the legend shows that shape on each line's sample, so a line can be matched to its name by shape as well as color. [learn more...](#nutrient-plot)

<!--
```
Scope: Analysis -> Daily summary -> Nutrient Plot (also the Home page plot image);
numa_app/services/plotting.py. New MARKERS list (marker, size, fillable), cycled
by series index in both color and grayscale modes; the rectangle is a custom
vertex path. Hollow (partial-GL) points now redraw the series' own shape with a
white face; the stroke-only asterisk and "#" can't be hollowed, so they get an
open ring instead. Previously every series used the same 3pt "o".
```
-->

#### October 27 updates

**PROGRAM: FASTER ONLINE FOOD SEARCHES, NO MORE FREEZING WHILE THEY RUN**

Online search results (USDA, Open Food Facts, Canadian Nutrient File) now arrive in about the time the slowest of the three takes, instead of all three added together. While they load you can keep using NuMa: other pages and buttons answer right away. Run the same search again within ten minutes, for example when the meal page reloads after **Add to meal**, and the online results come back instantly. [learn more...](#food-search)

<!--

```
Scope: every food search with online sources (Meal add-food panel, Foods ->
Search, Pantry, recipe ingredients, Compare, analyze-portion); web/backend.py,
platform_utils.py, usda_api.py, profile.py, tests/conftest.py, tests/test_web.py.

Root cause (owner report: ~2 s before anything happened on a new search, ~5 s
after Add to meal): every route was `async def` but did blocking work
(urllib, SQLite), so it ran ON uvicorn's single event loop. The online
search (/…/search-api-results) asked USDA (two requests), OFF and CNF one
after another, ~0.8-1 s each, and the server answered nothing else until it
finished. Add to meal then redirected back with the search kept, which ran
the whole online search a second time (no result caching).

Fixes: (1) 187 routes with no `await` are now plain `def`, so FastAPI runs
them on its thread pool; the 21 that await something stay async.
Measured on an isolated server: the meal page now returns in 0.1 s while an
online search is in flight (was: the full length of that search).
(2) _live_source_rows(): the selected _LIVE_SOURCES run in parallel threads,
and USDA's general + Foundation/SR Legacy boost requests do too. OFF's
same-name dedupe against USDA rows moved out of _fetch_off_candidates into
_drop_repeated_names(), applied at merge, unchanged in effect. (3) Raw
source rows cached 10 min (max 50 searches) keyed by query (case/space-
folded), selected sources, limit and the USDA boost size; a search where any
source failed is not cached. Cached/AA/GI marks are still computed fresh
from the DB on each call. (4) Thread safety now that requests overlap:
_save_prefs_file holds a lock around its read-modify-write, and prefs.json,
config.json and profile saves go through platform_utils.write_text_atomic
(temp file + os.replace), so a reader never sees a half-written file. The
stale-meals middleware stays async, so it still runs one request at a time.
New tests: sources asked at once, repeat answered from memory, failure not
remembered, 40 threads saving prefs lose nothing (fails without the lock).
```

-->

---
