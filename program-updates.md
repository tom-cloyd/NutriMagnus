## July 23

* LOGGED DAYS KEEP THE USER PROFILE IN FORCE WHEN THEY WERE LOGGED -  Analysis > Daily Summary - Each logged day now remains compared against whichever profile was active when you logged it, not whatever profile is active today — switching profiles for illness, travel, or a weight change no longer silently rescores your past days. You can also manually reassign which profile a specific day is compared against. [learn more...](user-manual.md#day-profile)
* RECENT DAYS SHOW YOUR DAILY DCP GOAL AND YOUR CHOSEN NUTRIENT COLUMNS -  Analysis > Daily Summary: Recent Days - Each day now shows its own protein (DCP) goal in grams, not just a percentage, and shows the same extra nutrient columns you chose for the Meals & Log list. [learn more...](user-manual.md#meal-columns)
* CHOOSE HOW MANY MEALS TO SHOW; CLEARER MEALS & LOG COLUMNS -  Meals & Log - Choose exactly how many meals to show via a number box, in place of the old "show all"/"show recent 9" toggle; Calories now appears before the DCP columns; column headers are stacked to fit more on screen; the "Search meal history" link now explains what it searches. [learn more...](user-manual.md#meals-list)
* MULTIDAY NUTRIENT TREND NOW LEADS WITH YOUR DCP AVERAGE -  Analysis > Multiday Nutrient Trend - This average-over-time view now leads with your average Digestible Complete Protein (DCP) instead of raw protein, since raw protein alone overstates what your body can actually use. [learn more...](user-manual.md#trend)
* SEARCH BOXES REMEMBER YOUR LAST SEARCH -  Meals & Log: Add Food or Recipe search / Recipes: Add Ingredient search (web) - If you follow a link away to look something up and come straight back, your last search and its results are restored automatically; a new "Reset search" button clears it back to the page's default.
* CONFIRM AMINO ACID DATA FOR SEARCH RESULTS ON DEMAND -  Foods: Search (web) - You can select foods showing the uncertain "~✓" amino-acid badge and click "Fetch full details for selected" to confirm, on demand, whether they truly have amino acid data. [learn more...](user-manual.md#food-search)
* ESTIMATE AMINO ACIDS BY COPYING FROM ANOTHER FOOD -  Foods: Drafted Food Profiles / Food Cache edit (CLI); Custom Food Profiles edit (web) - When entering a food's amino acid data, you can now search for and pick a similar food to copy amino acids from instead of typing them in by hand — values are scaled automatically to match the food's own protein content, and a note documenting the source is suggested for you. [learn more...](user-manual.md#drafted-foods)
* SEARCH RESULTS FOR RAW/WHOLE FOODS NO LONGER GET BURIED BEHIND BRANDED PRODUCTS -  Foods: Search / Meals & Log: Add Food or Recipe / Recipes: Add Ingredient (CLI + web) - USDA's own search ranking can bury a plain food like "Potatoes, flesh and skin, raw" — the version most likely to carry amino acid data — under branded and prepared-dish matches for the same word; the app now searches deeper to find them, and how deep is configurable in Settings > Advanced settings (0 = no limit). [learn more...](user-manual.md#food-data)
* ADDING A FOOD OR RECIPE TO A MEAL NO LONGER RE-SHOWS YOUR OLD SEARCH RESULTS -  Meals & Log: Add Food or Recipe (web) - Fixed a bug where, right after a successful add, the page would flip back to the search results you'd already acted on, inviting an accidental duplicate add.
* CLICKING "MEALS" OR "RECIPES" IN THE BREADCRUMB NOW STARTS A FRESH SEARCH -  Meals & Log / Recipes: Edit (web) - Following the breadcrumb back to the list now clears your remembered search, so you land on a clean page; using the top "Meals & Log" menu link still brings your search back if you only stepped away briefly.
* DAILY SUMMARY'S CHOSEN NUTRIENT COLUMNS NOW SHOW DATA FOR EVERY DAY -  Analysis > Daily Summary: Recent Days (CLI + web) - Fixed a bug where your chosen extra nutrient columns only had data for the couple of days you'd most recently opened; all logged days now show their numbers.
* DAY DCP AND % GOAL NOW COUNT AN IN-PROGRESS MEAL -  Analysis > Daily Summary: Recent Days (web) - Fixed a bug where a day's total DCP and % of goal only counted meals you'd explicitly marked complete, even though the number had already been computed — now matches how the CLI and the day-detail page already worked.

## July 22 x

* Meals & Log - You can now choose up to 6 extra nutrient columns, and their order, to show on the Meals & Log list, in both the terminal app and the web app.
* Foods / Recipes / Meals & Log - Every food and recipe name shown anywhere in the program now displays its ID number and data source (USDA, Open Food Facts, user-drafted, or recipe) right underneath it, so you can always trace what you're looking at back to its source.
* Recipes - A recipe's protein completeness (DCP) is now recalculated automatically whenever you change its ingredients or servings, instead of only when you explicitly ask for it.
* Manual - The manual is now split into separate Web App and Command Line parts, so web users (most users) no longer have to read past command-line-only instructions.

## July 20 x

* Foods / My Pantry / Recipes - You can now archive (reserve) a food, pantry entry, or recipe to hide it from search, complement suggestions, and everyday lists without deleting it or breaking anything that still references it — one click in the web app (Archive/Restore button, plus a Show Archived checkbox), or one command in the terminal app.

## July 19

* Analysis / Settings - If your dietary preference is set to vegetarian or plant-based, your iron and zinc daily targets are now automatically raised to reflect their lower absorption from plant foods, with an explanatory note; a warning also appears if your logged vitamin B12 intake is critically low on a plant-only diet.
* Analysis > Multiday Nutrient Trend - New view: average your nutrient intake over the last 7, 14, or 30 days against your targets, to catch a chronic shortfall that a single day's numbers would hide.
* Settings > Nutrient Targets - Iodine and selenium are now tracked alongside your other minerals throughout the program.
* Settings > Nutrient Targets - A new "load recommended optimal targets" action fills in sensible defaults (e.g. Vitamin D, EPA+DHA) for any nutrient you haven't already customized; built-in safe upper limits (iron, zinc, vitamin A, B6, iodine, selenium) now apply automatically even where you haven't set a personal max.
* Foods: food detail page (web) - Fixed a bug where collapsing a section (like Protein Summary) on one food's page would also hide that same section on every other food you looked at afterward.
* My Pantry / Food Cache (web) - My Pantry now shows Type, AA, GI, and DIAAS columns matching the Food Cache; a new "Link a food" action lets you attach a name-only pantry entry to a searched food instead of creating a duplicate.
* Meals & Log - A day's total DCP and % of goal now include any meal with a computed value, not just meals marked complete, so an in-progress meal is no longer silently left out of its own day's total.
* Web app - Fixed a startup timing issue where a slow-starting web server could open your browser before it was actually ready to respond.

## July 16

* Meals & Log - Analyzing a meal now automatically saves its computed DCP and calories instead of only displaying them; a single Calculate command replaces the old p-command, letting you compute DCP and calories for all meals, the last 30 days, or the last 10 days at once.

## July 15

* Settings > Nutrient Targets - You can now set a personal target above the standard RDA for any nutrient (e.g. more vitamin D than the population minimum) and/or a personal daily safety cap — tracked alongside RDA everywhere nutrients are shown, with a warning color when your intake is near or over your cap.
* Web app - Any editable form now warns you if you try to navigate away with unsaved changes, and shows a colored Save button when something's been edited.
* Manual - Added a DIAAS-by-protein-source quick-reference table for hand-estimating a packaged food's protein quality when it has no amino acid data.
* Recipes - A recipe ingredient that points to a food or recipe no longer in your cache (a "broken reference") can now be found and relinked, from a new Broken Recipe References list.
* Recipes (web) - The recipe edit page now shows the ingredient search and running nutrition totals side by side, with an ID number and brand shown in ingredient search results.
* Analysis > Food Use in Meals - Frequency-of-use history now groups correctly by recipe, so renaming a recipe no longer splits its history into two separate entries.
* Foods - Entering a volume amount (e.g. teaspoons) for dried herbs and spices like red pepper flakes is no longer rejected for lack of density data.
