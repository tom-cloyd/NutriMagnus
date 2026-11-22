# NutriMagnus User Manual

*Updated 2026-11-22:1046* / Reading time: 7 hours, 58 minutes

*Last full audit: 2026-11-10* / [Disclaimer](/disclaimer)

<!-- WORK TO BE DONE: Denoted by `[//]: #...` at the beginning of a line -->

<!-- t:26-10-02:0741 Today I will start marking sections I have reviewed/edited with HTML comment of this sort. I have previously reviewed many sections, but not marked them, but I need to know which sections have not yet been reviewed so this is how I'll keep records. A section no so marked may be one of those previously reviewed, but it will take me a while to catch up with such sections, and I may not recall them all anyway. I may or may not append a comment to the basic flag comment, the first of which may be seen below. -->

<!-- t:26-11-15 -->

**NutriMagnus ("NuMa")** is a computer program with open source (publicly available) code which provides a thorough nutritional analysis of a user's food choices. NuMa has special resources for tracking and analysis of protein because this is a problem for those eating primarily a plant-based diet, for older people, and for the chronically-ill:

* **Vegetarians and vegans** must deal with protein that has digestibility issues and amino acid completeness problems. 
* **Older people** are impacted by multiple factors reducing the chances of their being well nourished, including a much-reduced ability to make use of protein. 
* The **chronically-ill**, as well as **older people**, also have typically reduced appetites. 

People in these groups rarely have an accurate sense of the nutritional adequacy of their diet. The information is obscure, technically dense, and when it's on commercial packaging is both inadequate and misleading.

**Eating usually involves making choices, and good choice requires good information.** The four major problems impeding good food choice are a) lack of awareness of the choices available, and b) lack of information about the nutritional character of those choices, and c) lack of information as to what constitutes a good choice, and d) lack of detailed information about one's current eating habits and their deficiencies and excesses, if any. All of these problems are addressed by NuMa, in detail. Using the program will be quited an education for almost all users.

**Eating is fundamentally about survival - the first priority for all life.** Most of the cells in our body persist for a shorter period than we do. During their lifespan they do their work using materials available to them in their immediate environment. Eventually they must be replaced by new cells, constructed again from such available materials.

**Essential materials needed for cellular support and replacement come from what we eat.** While significant essential materials may already exist in the local environment of a cell, ultimately all materials come from outside our bodies, through eating.

**Both the program and its accompanying *User Manual* are in continuing active development.** They are modified frequently. Both are already quite sophisticated, but new versions will be made available quickly for those already using the program. However, the manual is still receiving a careful editorial review of all its parts. It is an advanced first draft.

**User feedback is highly valued, so please give us yours!** With computer programs in active development ANY feedback is appreciated and most likely useful. User experience with the program is a critical measure of program success or failure. So, please email all problems, thoughts, and ideas to [tomcloydmsma@gmail.com](mailto:tomcloydmsma@gmail.com). Put `NutriMagnus` or `NuMa` in the subject line, please! For what's most useful to tell us, and the quickest ways to reach us, see [Getting more help](#quickhelp).

**Manual authors:** This manual was designed by Tom Cloyd but largely written by Claude AI, which does an excellent job of summarizing program code and research reports. Tom is reviewing the manual, critical sections first, and making editorial changes when needed. Overt errors in the manual have been extremely rare. A weekly, monthly, quarterly, and annual sweep (review) by Claude AI of the manual and of the program code as well, is also done - see ([what each one covers](#periodic-review)).

---

## How to read this manual {: #how-to-read}

<!-- t:26-11-15 -->

*Search terms: where to start, reading order, which part, overview of the manual.*

NuMa is a desktop program that runs on your own computer, normally in a window of its own. Once it's installed ([Quick start](#quick-start)), there's no command line involved.

This manual is long because NuMa does a lot, but you don't need to read most of it. The first three Parts are meant to be read, in order, in about an hour. Everything after them is reference: you look things up there, or follow a **Learn more** link on a NuMa page straight to the section you need.

| If you want to… | Read |
|---|---|
| Install NuMa and set it up | [Part 1 — Quick start](#quick-start) |
| Know what NuMa does, and the few ideas it's built on | [Part 2 — Overview](#overview) |
| Learn by doing, step by step | [Part 3 — Workflow examples](#sample-workflows-web) |
| Know what a menu item, page, table or column does | [Part 4 — Menu by menu](#part-3-using-numa) |
| Enter amounts, search, edit data, move data between computers | [Part 5 — Skills used everywhere](#skills) |
| Fix a problem, or ask for help | [Part 6 — Help and troubleshooting](#feedback) |
| Understand the nutrition science behind a number | [Part 7 — The science behind NuMa](#coreNutrition) |
| Know where your data comes from, where it's kept, and how to back it up | [Part 8 — Your data](#your-data) |
| Look up a word | [Glossary](#glossary) |
| See what changed in a new version | [What's new](#updates-log) |

**A good path for a new user:** Part 1, then Workflows 1 and 2 in Part 3, then use NuMa every day for a week. Skim Part 2 along the way. Part 7 can wait until a number on the screen makes you curious: technical terms on NuMa's pages link to their explanations.

**Getting back to NuMa.** **↩ Return to …** (Alt+Shift+U), in the yellow bar above this manual, goes straight back to the page you came from, and **Manual** in the menu later reopens the manual where you left off. **← Back one step** (Alt+←) retraces your jumps inside the manual instead. See [Getting back to where you were](#manual-back).

**Looking for something specific?** Type a word or two into the search box at the top of the sidebar. It works differently from a plain text search; see [Using this manual's search](#search-howto).

## Part 1 — Quick start {: #quick-start}

*(Reading time: 10 minutes)*

### A. Download and install the program

<!-- t:26-11-15 -->

*Search terms: installation, installer, setup, get the program, get NuMa.*

NuMa runs on Windows and Linux, which install differently: follow the steps for your system, then read [What kind of program this is](#install-webapp-note), which surprises nearly everyone.

#### Windows {: #install-windows}

*Search terms: Windows 10, Windows 11, SmartScreen, blocked download, virus warning, upgrade, upgrading, uninstall, Start menu.*

NuMa has no installer: it's one program file that you keep somewhere and run.

a. **Download it** from <https://github.com/tom-cloyd/NutriMagnus/releases/latest/download/nutrimagnus.exe>. This link always gives the newest version.

b. **Give it a permanent home.** In File Explorer, make a folder called **NutriMagnus** in **Documents** and move `nutrimagnus.exe` into it. Left in Downloads, it may get cleaned out.

c. **Get past Windows' two warnings.** Your browser will probably block the download. In **Edge**, click the **...** beside it, choose **Keep**, then **Show more** → **Keep anyway**; in **Chrome**, click the **^**, choose **Keep**, then **Keep anyway**. The first time you run it, a blue **"Windows protected your PC"** box appears: click **More info**, then **Run anyway**. It won't ask again for that copy.

   Both warnings mean "Windows doesn't know who published this", not "this file is dangerous": any program whose author hasn't paid for a signing certificate gets them. If your antivirus quarantines the file for the same reason, allow it.

d. **Run it.** Double-click `nutrimagnus.exe`. A black window full of text opens: that *is* NuMa running, so leave it open. A few seconds later NuMa's own window opens (using Edge, which every Windows computer has, or Chrome; see [Browser to Launch](#browser-to-launch)), and that's the one you use. The first start can take up to a minute while Windows scans the file. If nothing opens, go to **http://127.0.0.1:8000** in your browser.

e. **Make it easy to start.** Right-click `nutrimagnus.exe` and choose **Pin to Start**, or for a desktop icon, **Show more options** → **Send to** → **Desktop (create shortcut)**.

f. **Quit it properly.** Press **Ctrl+Q** on any NuMa page, or close both NuMa's window *and* the black window. Closing only NuMa's window leaves it running. [More about Ctrl+Q](#quit-numa)

g. **Updating it later.**{: #update-windows} A running program can't replace itself on Windows, so you swap the file yourself:

   1. **Download the new version.** When there is one, an **UPDATE AVAILABLE** message appears on NuMa's home page; click **Download NutriMagnus** (or use the link in step a). If the browser warns you, choose **Keep**, then **Keep anyway**, as in step c.
   2. **Quit NuMa** by closing its black window. The manual stays on screen, so you can keep following these steps.
   3. **Replace the old file.** Move the new `nutrimagnus.exe` from Downloads into your NutriMagnus folder (the UPDATE AVAILABLE message names the folder) and choose **Replace the file in the destination**. If Windows says the file is in use, NuMa is still running: go back to step 2.
   4. **Start NuMa again** as usual; your pin or shortcut still works. If the blue "Windows protected your PC" box appears, click **More info**, then **Run anyway**.
   5. **Press F5 in every window or tab that has this manual, or any other NuMa page, open.**

   **Don't skip step 5.** An open page doesn't update itself, and nothing on it says it's out of date: the manual would go on showing old instructions.

   Your data isn't inside the program file. It lives in your Windows account (`%LOCALAPPDATA%\numa` and `%APPDATA%\numa`), so updating loses nothing. To remove NuMa, delete `nutrimagnus.exe`, and those two `numa` folders too if you want your data gone.

#### Linux {: #install-linux}

*Search terms: installation, Debian, Mint, Fedora, upgrade, uninstall, app menu, AppImage.*

a. **Download** `install-linux.sh` from the latest release on the [NutriMagnus releases page](https://github.com/tom-cloyd/NutriMagnus/releases); it's the only file you need. NuMa is built and tested on Ubuntu 24.04 LTS and should work on most modern Linux systems. If it won't run on yours, see "For developers" in the project's `README.md` to run it from source.

b. **Install it** by running `bash install-linux.sh` in a terminal, in the folder you downloaded it to. It installs into your own account (`~/.local/bin`): no admin password, and nothing outside your account is touched.

c. **Find it in your applications menu,** where the installer adds it like any other program. If you don't know which desktop you have, it's almost certainly GNOME.

   - **GNOME (Ubuntu's default):** press the Super key (⊞) or click **Activities**, and type "NutriMagnus" or "NuMa".
   - **KDE Plasma:** open the application launcher (bottom left, or press Meta) and type the same.
   - **Others (XFCE, Cinnamon, MATE…):** look under Utilities or Science, or search for "NutriMagnus".

   Some desktops update their menu only at login, so if it's missing, log out and back in.

d. **Start it** by clicking its icon. It starts in the background and opens in its own window (or a browser tab; see [Browser to Launch](#browser-to-launch)). No terminal needed after installing.

**If the icon never appears,** even after logging back in, run `~/.local/bin/nutrimagnus` in a terminal, and [let us know](#feedback) so it can be fixed.

Your data lives in `~/.local/share/numa` and `~/.config/numa`, not in the program, so updating or reinstalling leaves it untouched ([Backing up your data](#backup)).

#### What kind of program this is {: #install-webapp-note}

*Search terms: offline, no internet, privacy, private, localhost, server, page won't load, site can't be reached, connection refused, hibernate.*

NuMa is a desktop program that runs quietly in the background and shows its screens through a web browser, in a window of its own or a tab. It looks like a website, but it's talking only to itself on your computer. It doesn't need the internet to run, and nothing you enter leaves your computer: it goes online only to look up a food in an online [database](#gloss-database), or to check for a new version. Two things follow:

   - **The window and the program are different things.** Closing NuMa's window doesn't stop NuMa. To get back, start NuMa as usual and a fresh window opens. To quit for real, press **Ctrl+Q** ([more](#quit-numa)).
   - **Sleep can disconnect the window.** If your computer sleeps while NuMa is open, the program may stop, and the page won't load when you come back. Nothing is broken and your data is safe: just start NuMa again.

### B. Setting NuMa up: first time, or after losing your data {: #first-setup}

*Search terms: first run, initial setup, setup checklist, configuration, getting started, reinstall, new computer.*

Follow these steps the first time you run NuMa, or after your computer was wiped or replaced without your NuMa data being saved.

**Lost your data? Check this first.** If you have a backup of NuMa's two data folders, restore it ([Backing up your data](#backup)) and skip the rest.

**Starter foods and recipes.** A new install isn't empty: your Food Cache and Recipes already hold some common foods, most with full amino acid data, and a few recipes showing protein complementing at work. Their names begin with an asterisk and a space (`* Quinoa, cooked`), so you can tell them from your own. Keep or remove them (Step 2).

#### Step 1 — Settings you must address before you start

*Search terms: required settings, personal details, vegan, configuration, blank percentages, empty targets.*

Go to **Settings**. Until these three are done, NuMa's results are blank or quietly misleading.

1. **Your Profile (section 1):** your age, sex, weight, height and activity level. Without them every "% of daily target" is blank. On the same form, also set:
    - **your glucose tolerance**: impaired if you have diabetes, prediabetes or insulin resistance, otherwise normal. It decides which [GI](#gloss-gi) values the lookup shows first, and the note shown beside a GI [measured in people with diabetes](#gi-impaired);
    - the **oxalate lookup** box, if oxalate matters to you (for kidney stones, say);
    - if you like, a **daily glycemic load target**, a ceiling for each day's [GL](#gloss-gl) ([more](#gl-target)).
2. **Dietary Preferences (section 3):** all foods, vegetarian, or plant-based only. This filters *every* search and suggestion, so a wrong setting hides foods you expect to see.
3. **[USDA](#gloss-usda) [API](#gloss-api) Key (section 6).** Most of NuMa's food data comes from the US government's FoodData Central, which asks every program using it for a **key**: a long code, like a password, free to anyone. Without your own, NuMa shares one key among all its users, and when that's overused your searches can fail for a while. Getting your own takes about a minute ([how](#food-data)).

Then glance at **Computed Daily Targets (section 2)** to check your targets look sensible.

#### Step 2 — Settings worth doing at some point

*Search terms: optional settings, preferences, configuration, default browser, recommended targets, supplements, routine.*

- **Nutrient Targets - Researched (section 5):** click **Load recommended Revised Optimal targets**, and add max limits for anything you need to keep low.
- **Glycemic Index Reference Table (section 7):** only if you'll track glycemic index (Step 4). Build the 2021 table ([how](#gi-editions)) before choosing glycemic index values, so they come from the better table.
- **Meals & Log columns (section 11):** which nutrient columns your meal lists show.
- **Starter Data (section 12):** keep the starter foods and recipes, or clear them.
- **Browser to Launch (section 13):** NuMa's own window (the default) or a browser tab, and which browser if you run several.
- **[Daily Starting Items](#daily-start) (section 10):** foods and recipes you have every day, such as a vitamin or a morning coffee, which NuMa then adds to each day's first meal for you. Each food must already be in NuMa, so this is easiest after Step 3.
- **Protein Digestibility Overrides (section 4):** nothing to do now; it's for later, if you find a better digestibility figure for a food.

#### Step 3 — Set up your pantry

*Search terms: staples, groceries, everyday foods, favorite foods, kitchen cupboard.*

Your pantry is the foods you keep at home and use often. It matters for two reasons. NuMa looks there first when it suggests a food to fill a protein gap, so its suggestions are things you have. And NuMa can only work with the data it has: foods from even the best databases often lack amino acid data, have patchy omega-3 data, and never have glycemic index values. The foods you eat most are the ones worth getting right.

**[Workflow 1 — Start with your own food](#wf-inventory)** walks you through it: list the foods you actually eat, find each one in NuMa, add it to your pantry, and fix the gaps that matter. Do it now if you can.

#### Step 4 — Glycemic index values for your core foods (optional)

*Search terms: blood glucose, diabetic, carbs, low GI, insulin.*

**Most people can skip this step.** It's for those who want to track glycemic index (GI), for example because of diabetes or prediabetes. If that's you, follow [Workflow 7 — Watching your blood sugar](#wf-blood-sugar) once your pantry is set up.

#### After an update: new starter items

*Search terms: upgrade, what's new, release notes.*

A new version sometimes adds starter foods or recipes, or improves ones you have. **NuMa tells you:** the **UPDATE AVAILABLE** message says what it will change, and a **NEW STARTER ITEMS** message on the home page says what it added or improved. Nothing in your data changes until you choose, in [Settings → 12. Starter Data](#starter-data).

### C. Where to go next {: #quick-start-next}

*Search terms: first steps, what now, next steps, getting started.*

With NuMa installed and set up, here's a good order for your first week:

1. **Take stock of your food, away from the computer.** [Workflow 1](#wf-inventory) starts with a pencil and your kitchen cupboards, then puts the foods you eat most into NuMa. It's the single most useful thing you can do, because every later result depends on it.
2. **Log a day of eating.** [Workflow 2](#wf-first-day) shows how. After Workflow 1 it's quick, since most of what you eat is already in NuMa.
3. **Use NuMa every day for a week.** The other workflows in [Part 3](#sample-workflows-web) show more of what it can do; try them as they become useful.
4. **Skim [Part 2](#overview)** for the handful of ideas behind what NuMa shows you.

### D. Tips for new users {: #new-user-tips}

*Search terms: getting started, beginner, how to learn, learning curve, practice, weigh, food scale, measuring, guess, help, support, stuck, mouse, touchpad, trackpad, accessibility, tremor, hand pain.*

- **Start with what's easiest.** NuMa is a powerful program, and unusually deep. Approach it slowly: single foods and simple recipes give real benefit early. Don't expect to learn it all in a few sessions, and [contact us](#feedback) early, not late, if it starts to feel overwhelming.
- **Use it every day for the first week.** Without daily use for about a week you won't get past the slow-fumbling stage. This is a Boeing 727, not a Piper Cub: learn the cockpit and you can be a world traveler. There are two things to learn: the ideas ([Part 7](#coreNutrition), or the short version in [Part 2](#ideas-primer)) and the menus ([Part 4](#part-3-using-numa)). The learning can be gradual; daily contact is what counts.
- **Look carefully at each screen.** NuMa's pages are rich in information. You needn't use it all at once, but watch for **Learn more** and **Why?** links: they open the part of this manual that explains what you're looking at.
- **You can leave the mouse alone.** NuMa can be used entirely from the keyboard, which is faster once learned, and a real help if a mouse or touchpad is awkward or tiring for you, for example because of a tremor or limited fine motor control. Press `Alt+Shift+K` on any page: a panel lists every page and everything the current page has a shortcut for, with the keys for each, so it's the one shortcut you need to remember. Type a few letters to narrow the list, then press Enter. Within a page, Tab moves from box to box and Enter saves or searches, and in search results ↑ and ↓ move from one result to the next. See [Finding your way around](#web-shortcuts).
- **Weigh your food if you can.** NuMa needs to know what you ate and how much, and a weight is by far the most accurate way to say how much. A cup or a named portion works too, and NuMa converts it, with some error; an estimate is still much better than nothing. Still, a kitchen scale is worth having. I have had a small Oxo scale for years, and it's excellent.
- **It gets faster.** NuMa remembers what you've typed and chosen, and your [Food Cache](#FoodCache) keeps every food you've used, so foods you've had before appear instantly, without going online.
- **Stuck?** Search this manual for a word or two, with **Only show things you can do** ticked, or look in [Part 6 — Help and troubleshooting](#feedback). If that doesn't solve it, [help is close at hand](#quickhelp).

## Part 2 — Overview: what NuMa does, and the ideas behind it {: #overview}

*(Reading time: 13 minutes)*


This Part says what NuMa does, explains briefly the handful of ideas behind everything it shows you, and shows how its pieces fit together. It's short on purpose: each idea links to its full explanation in [Part 7](#coreNutrition).

### A. What you can do with NuMa {: #what-numa-does}

*Search terms: features, what it does, capabilities, menus.*

The main menus in the top navigation bar correspond to the major things you can do with the program (**Compare** and **Manual** have their own items in the bar too):

- **Foods**
    - Search the [USDA](#gloss-usda) and Open Food Facts[^3] [databases](#gloss-database), the Canadian Nutrient File, and the UK, Australian and French food databases bundled with NuMa — see [Search](#search-web).
    - Analyze the nutrients in a specific portion of any food or recipe — see [Analyze a food portion](#analyze-portion).
    - Compare up to eight foods and recipes side-by-side — see [Compare](#compare-web).
    - Manage your personal [Food Cache](#gloss-food-cache), Pantry, and custom food profiles — see [Food Cache](#food-cache-web), [My Pantry](#pantry-web) and [Custom food profiles](#custom-foods).
    - Annotate foods with glycemic index and [DIAAS](#gloss-diaas) estimates — see [Annotate a Food](#annotate).
    - Export/import your Food Cache as [CSV](#gloss-csv), to move data to or from another NuMa install — see [Moving foods with CSV files](#csv-foods).
- **Recipes**
    - Create and save recipes with ingredients and instructions — see [Using the Recipes menu](#recipes-menu-web).
    - Browse, copy, and delete saved recipes — see [Recipes List Table](#recipes).
    - Export/import a recipe as a self-contained [CSV](#gloss-csv), bundling every sub-recipe and ingredient's data along with it — see [Moving recipes with CSV files](#csv-recipes).
    - Develop a recipe iteratively with nutritional feedback after each ingredient change — see the **Running totals** card in [Using the Recipes menu](#recipes-menu-web).
    - Analyze a recipe portion for full nutrient data, protein quality, and complement suggestions — see [Analyze a saved recipe portion](#analyze-portion).
- **Meals & Log**
    - Record what you eat by date — see [Using the Meals & Log menu](#meals-menu-web).
    - Add foods and recipes to meals — see [Meal Items Table](#meal-detail).
    - Analyze individual meals or the combined total for a full day, to monitor intake of any nutrient(s) of particular interest — see [Analyze full day](#full-day).
    - Search your entire meal history for any food — see [Meal History Tables](#meal-history).
- **Analysis** — a growing set of preset analyses
    - **Daily summary — [DCP](#gloss-dcp) and goals**: combined nutrient totals for today or any past date, compared against personalized [RDA](#gloss-rda) targets, plus a list of recent days with meals — see [Using the Analysis menu](#analysis-menu-web) and [Daily Nutrient Goals](#goals).
    - **Food use in meals**: rank everything you actually ate — foods, recipes, sub-recipes, and the foods inside recipes — across a chosen set of date ranges and/or meals, with a frequency histogram — see [Food Use in Meals](#fooduse).
    - **Food use in recipes**: the same ranking, but for which foods and recipes are used as ingredients across your recipe book — not a measure of what you eat — see [Food Use in Recipes](#fooduse-recipes).
    - Both Food Use pages can also bulk-substitute one food or recipe for another across the current selection — see [Substituting a Food or Recipe](#fooduse-substitute).
    - **What-if: meals**: see how your average daily nutrition over a set of days would change if you removed, added, replaced or cut down foods and recipes — without changing anything — see [What-if: Meals](#whatif).
    - **What-if: recipes**: the same for your recipes — how each one's nutrition per serving would change if you removed, added or replaced an ingredient — see [What-if: Recipes](#whatif-recipes).
- **Settings**
    - Your profile (age, sex, weight, height, activity level), which sets all your daily nutrient targets — see [Your Profile](#profile-setup).
    - Dietary preferences — see [Dietary Preferences](#diet).
    - Researched nutrient targets and maximum limits — see [Revised Optimal targets](#optimal) and [Maximum Nutrient Limits](#maxlimits).
    - Protein digestibility overrides — see [Protein Digestibility Overrides](#dcp-overrides).
    - Your personal [USDA](#gloss-usda) [API key](#food-data) (a free code from USDA's website that increases how many food searches you can do), the glycemic index table, glycemic load and water display, Meals & Log columns, starter data, keyboard shortcuts and more — see [Using the Settings menu](#settings).

Each menu is described in full in [Part 4 — Menu by menu](#part-3-using-numa). To learn by doing instead, go to [Part 3 — Workflow examples](#sample-workflows-web).

### B. The ideas NuMa uses, in brief {: #ideas-primer}

*Search terms: basics, concepts, nutrition basics, jargon, terminology, beginner.*

NuMa uses some specialized words. You don't need to master them before you start, but knowing roughly what each one means makes NuMa's pages much easier to read. Each heading links to the full explanation.

**Food data is per 100 grams, then scaled.** Every food's nutrients are stored per 100 g. NuMa multiplies them by the amount you say you ate, so the amount matters as much as the food. A kitchen scale makes the biggest single difference to accuracy (see [Entering amounts](#amount-formats)).

**Protein is made of amino acids, and nine are essential.** Your body builds its own protein from about twenty amino acids. Nine of them it can't make, so they must come from food: the [essential amino acids](#aa). How much of each a food has decides how useful its protein is.

**The amino acid in shortest supply sets the limit.** Your body needs the nine in roughly fixed proportions. If one is short, the body can use the others only up to the level that one allows, and the extra is wasted, like bricks left over when the cement runs out. The short one is the food's *limiting amino acid*, and how far short it falls is its [gap](#gap). Most plant proteins have at least one. The proportions themselves come from the [FAO 2013 reference standard](#fao).

**Not all protein gets digested.** Some protein passes through the body unused. [DIAAS](#diaas) (Digestible Indispensable Amino Acid Score) combines digestibility with the limiting amino acid into one number: 1.0 or more means the protein fully meets the standard; below 1.0 means it falls short.

**[DCP](#gloss-dcp) is the protein that counts.** [Digestible complete protein](#dcp) (DCP) is the grams of protein in a food, meal or day that your body can actually digest and use, after allowing for digestibility and the limiting amino acid. It is NuMa's main protein figure, and the one compared with your daily protein goal. It is usually lower than the protein figure on a label, sometimes much lower.

**Foods can make up for each other.** A food rich in the amino acid another lacks *complements* it: rice and beans is the classic pair. They don't have to be eaten together, only within about a day. When a food, recipe or meal has a gap, NuMa suggests [complements](#comp), from your own pantry first.

**Your targets are personal.** How much of each nutrient you need depends on your age, sex, weight, height and activity level, which you enter once in your profile. NuMa starts from the official [Recommended Dietary Allowances](#rda) (RDAs), and lets you add more recent [research-based targets](#optimal) and [upper limits](#maxlimits).

**Blood sugar: [GI](#gloss-gi) and [GL](#gloss-gl).** The [glycemic index](#gi) (GI) says how fast a carbohydrate food raises blood sugar; [glycemic load](#gl) (GL) combines that with how much carbohydrate you actually ate. NuMa uses only GI values you choose from published tables, never guesses. If blood sugar isn't a concern for you, you can turn all of this off.

**Some things in food get in the way.** [Antinutrients](#antinutrients) such as phytate reduce how much of some minerals you absorb, and [oxalate](#oxalate) matters to people prone to kidney stones. NuMa notes them where they matter.

**Water counts too.** NuMa can track the [water](#water) you get from drinks and from food, which matters especially for older people.

**Missing data is common, and NuMa tells you.** Many foods in public databases lack amino acid figures, portion weights or some nutrients. NuMa marks what is missing, labels anything it [estimates](#filling-gaps), and lists the gaps worth fixing in [Checking your data](#checking-your-data).

### C. How the pieces fit together {: #how-it-fits}

*Search terms: structure, how NuMa is organized, food cache vs pantry, data model, big picture.*

Everything in NuMa is built from foods. Here is how the parts connect:

<pre>
  Online food databases (USDA, Open Food Facts, and others)
        │  a search brings a food in
        ▼
  Food Cache ──────────► My Pantry
  (every food you've      (the foods you keep at home;
   looked up or made)      suggestions look here first)
        │
        ├──────────► Recipes (made of foods, and of other recipes)
        │                 │
        ▼                 ▼
  Meals (what you ate, by date) ──► Days ──► Analysis (across many days)
                                     ▲
  Settings: your profile ────────────┘ (sets your daily targets)
</pre>

- **[Food Cache](#food-cache-web):** your own copy of every food you've looked up, added or created. Once a food is here, NuMa doesn't need the internet to use it.
- **[My Pantry](#pantry-web):** the foods you actually keep at home. NuMa looks here first when it suggests a food to fill a gap.
- **[Custom food profiles](#custom-foods):** foods you enter yourself, such as a homemade item, a product with an incomplete entry, or a supplement tablet.
- **[Recipes](#recipes-menu-web):** made of foods and other recipes, analyzed per serving.
- **[Meals](#meals-menu-web):** what you ate, with amounts and a date. All the meals on one date make a **day**.
- **[Analysis](#analysis-menu-web):** looks across days: daily summaries, averages, plots, how often you eat each food, and "what if" changes.
- **[Settings](#settings):** your profile and preferences, which set your daily targets.

**Every analysis page looks alike.** A food, a recipe, a meal and a whole day all get the same kind of analysis: nutrients against your targets, protein quality, complement suggestions, glycemic load and more. Learn to read one and you can read them all; see [A food's page, and every analysis page](#analysis-pages).

### D. Why NuMa exists: the protein problem {: #why-numa}

Why NuMa was built, and the problem it is best at.

#### NutriMagnus addresses two serious problems

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

Thoughtful diet management requires trustworthy, specific data that is only to be found in research report summaries. Both access and use of this data requires use of computers. 

Managing specific dietary problems presents even greater challenges. One such specific problem is management of protein intake in vegetarian and vegan diets, especially when a person is no longer young. NuMa is particularly suitable for management of this problem, but can address others as well, focusing on oxalate consumption, need for vitamins and or minerals, phytonutrient tracking, and more. 

**Diet matters.** It is now well established that the crucial factors affecting physical and mental health are diet, sleep, exercise, social engagement, stress management, and avoidance of injurious and risky substances. Their relationships are complex and interacting. Relative to diet, research supports an emphasis on a "plant-predominant eating pattern". [^1] The fortunate thing about diet is that it is something we act on immediately and effectively - but only if we have the information needed to make good choices.

**Plant-based diets are preferable.** There are multiple good reasons to focus on eating foods derived from plants rather than animals. Plant-based proteins are far less ecologically damaging to produce than animal protein and also much less likely to acquire agricultural chemical accumulations, which are then ingested along with the nutrients they contain. They also do not involve the industrialized abuse of vast numbers of animals who live only long enough to produce edible protein and then are treated like a mere object to be processed as we might a fallen tree. 

Plant proteins are usually more affordable and easier to ship and store for long periods. Most of the world, and most humanity throughout human history, eats and has eaten a plant-predominant diet, so this is simply not a novel idea.

**Plant-based proteins require special management.** But almost all plant proteins come to us with a built-in problem: incomplete amino acid composition. When you read on your jar of peanut butter (an excellent protein source) that 2 tablespoons contain 7 grams of protein (a bit more than that in a large egg), what it doesn't tell you is that only a bit less than 4 grams is actually digestible by human bodies, and of that only a little over 2 grams is [complete protein](#gloss-complete-protein) - the kind found in an egg or a piece of chicken meat, and the kind we need.

There are 9 protein building blocks (amino acids) that human bodies cannot make and must therefore ingest. Additionally, they must be ingested in specific proportions. When a food, or meal, or diet lacks or is insufficient in one or more of these "essential" amino acids this has a limiting effect on the utilization of the other 8. This is the "incomplete protein" problem that almost all plant proteins present.

Consider someone building a brick wall, where the plan calls for a fixed ratio of bricks to bags of cement — say, 50 bricks per bag. If they have 500 bricks but only 6 bags of cement, they can only build as much wall as 6 bags of cement allows; the other 200 bricks sit unused no matter how many more of them they buy. Buying more bricks doesn't help, because bricks were never what was running short *relative to the fixed ratio the plan calls for*.

This is the essential amino acid problem inherent in plant-based diets. The human body needs each of the nine essential amino acids in a fixed proportion to the total protein eaten — much like the bricks-to-cement ratio above. When a food, meal, or diet is short on one amino acid relative to that required ratio, the shortfall — not the total protein eaten — sets a ceiling on how much of that protein the body can actually use; the rest is broken down and discarded, like the unused bricks. (This required ratio is the [FAO 2013 Reference Standard](#fao) — see [Raw protein, protein quality, and protein digestibility](#appendix-protein-quality) for the full technical explanation.)

While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24-hour period if the amino acid limitation problem is to be avoided. So, one way or another, one needs to tend to the issue of what is missing and where to find replacements to add it to one's diet in time.

**NuMa handles gracefully the tricky problem of managing plant-based proteins.** Few people know which foods have missing essential amino acids ([EAAs](#gloss-eaa)) or which have the needed excess [EAAs](#gloss-eaa) which would make them a good complement to eat with other foods lacking enough of those [EAAs](#gloss-eaa) in the same 24-hour period.

Beyond the problem of ingesting the right mix of amino acids, there are two other related dietary protein problems to be addressed:

* Protein in a food, however balanced or not, does no good if our bodies do not access it. Different protein sources in plant-based diets are metabolized in differing degrees of efficiency. This is the **[bioavailable protein](#gloss-bioavailable-protein)** problem.

* Age, sex, and activity level differences in protein needs do exist and they are not minor. Older people, active people, and those with chronic diseases, for example, require substantially more protein than do younger healthy people, for several reasons. Almost all common discussions of dietary protein fail to address this problem, and in any case a mere discussion doesn't tell one what to eat and how much.

#### This protein-management problem is critical for older people and the chronically ill, and especially so for women <!-- tc:rev26-09-16 -->

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

In very brief summary, as we age, we tend to lose muscle mass, utilize dietary protein less efficiently, and simply eat less. These factors compound to create a perfect storm of vulnerability to general ill-health and the often dire consequences of falls. And these issues affect women more than men. Put simply - getting enough of the right sort of protein matters far more than most people realize. A good diet is utterly necessary, but not by itself sufficient. It must be complemented with adequate resistance exercise.

There is very little discussion of the problem in the mass media. So, it is up to us as individuals to self-educate and then make carefully considered decisions about our diet. But this is almost impossible to do without serious technical help, as the nutritional factors involved go well beyond simple arithmetic or the naively simple view offered to us by the first major statements about plant protein complementarity in the very early '70s.

#### NutriMagnus is the missing helper

*Search terms: plant-based, why NuMa, purpose, other nutrition apps, Cronometer, MyFitnessPal.*

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

Nutrition analysis programs, both paid and free open source, already exist but none that we've seen focus on the problems faced by vegetarian and vegan folks. And none have the rich features and readily modifiable design that we want. The NuMa program addresses both problems in detail. It also suggests complementary foods that can be combined with a food or recipe or meal to create [complete proteins](#gloss-complete-protein) in one's diet.

NuMa has been under intense development and is still being developed. Over time, new users will experience unanticipated needs and the program can be further developed to meet them. This is one reason why [reporting problems](#feedback) is so important - feedback drives program development.

### E. Why you can trust the numbers {: #trust-short}

*Search terms: accuracy, trustworthy, where the numbers come from.*

- **The data comes from reliable public sources,** mainly the US government's FoodData Central, plus national food databases from Canada, the UK, Australia and France, and Open Food Facts for packaged foods. NuMa shows which source each food came from.
- **The calculations follow published methods,** chiefly the [FAO](#gloss-fao)'s for protein quality, and a [worked example](#appendix-diaas-validation) lets you check one by hand.
- **The program is tested automatically,** by more than 2,000 tests run every time it changes, and reviewed on a regular schedule.
- **Gaps and estimates are labeled,** never hidden.
- **Bugs still happen.** If a number looks wrong to you, [tell us](#feedback).

The full account is in [Data, testing, and validation](#data-testing-validation).

## Part 3 — Workflow examples {: #sample-workflows-web}

*(Reading time: 21 minutes)*


<span id="sample-workflows"></span>

*Search terms: walkthrough, learn by doing, how do I start, practice.*

**Use this Part as a tutorial.** Each workflow is a short, real task, done step by step. Work through it with NuMa open, and look carefully at what appears on your screen. You don't need to read Part 4 or Part 7 first; terms are explained briefly where they come up, and each workflow ends with links to the sections it used.

Workflows 1 and 2 are the place to start, in that order. The rest can be done in any order, whenever they become useful to you.

1. [Start with your own food](#wf-inventory): take stock of what you eat, then put it into NuMa.
2. [Log your first day](#wf-first-day)
3. [Build a recipe](#wf-recipe)
4. [Close a meal's protein gap from your pantry](#wf-pantry-gap)
5. [A food NuMa doesn't know, or a supplement](#wf-unknown-food)
6. [A week in review](#wf-week)
7. [Watching your blood sugar](#wf-blood-sugar)
8. ["What if I stopped eating this?"](#wf-whatif)
9. [Comparing foods while you shop](#wf-compare)
10. [Cleaning up your data, monthly](#wf-cleanup)
11. [A kidney-stone concern: oxalate](#wf-oxalate)
12. [A food is missing nutrient data, or its figures look wrong](#fix-food-data): search, borrow, then ask [AI](#gloss-artificial-intelligence).

At the end, [A few more things worth trying](#wf-more) lists some features the workflows don't reach.

---

### Workflow 1 — Start with your own food {: #wf-inventory}

*Search terms: fridge, staples, list of foods, set up pantry, first workflow, groceries.*

**What this does:** gets the foods you actually eat into NuMa, with good data, before you log a single meal. It's worth doing first for three reasons. You need these foods in NuMa anyway, to log what you eat. NuMa's suggestions for filling a protein gap come from your pantry first, so they become practical: foods you already have. And it keeps your attention on your food, which is the point of all this.

**Part one: away from the computer (about 30 minutes).**

**Step 1 — Take stock.** With paper and pencil, go through your pantry, cupboards, refrigerator and freezer. Write down every food you eat at least once a week or so: grains, beans, nuts and seeds, bread, vegetables, fruit, dairy or its replacements, eggs, tofu, meat or fish, oils, spreads, and anything you drink besides water. Skip things you use only by the pinch, such as spices.

**Step 2 — Add how you usually eat them.** Beside each food, note the form you eat it in (cooked or raw, dry or canned) and, roughly, how much at a time: "oats, dry, ½ cup", "black beans, canned, drained". The form matters: cooked rice and dry rice are very different per 100 g (see [Practical compromises](#dry-weight-compromise)).

**Step 3 — Mark the most important.** Star the foods you eat most often, and the ones that supply most of your protein. Those are the ones to get right first.

**Step 4 — Look for gaps.** Glance through [Plant protein sources in your pantry](#appendix-plant-proteins). You may find good protein foods you'd like to add to your list.

**Part two: in NuMa (about an hour, and it can be spread over several sessions).** Start with your starred foods.

**Step 5 — Check the starter foods first.** NuMa comes with a set of starter foods whose data has already been checked; their names begin with `* `. Go to **Foods → 5. Food Cache**, type `*` in the filter box, and click **Filter this list**. For each food on your list that's there, click **Add to pantry**.

**Step 6 — Find the rest.** Go to **Foods → 6. My Pantry**. Type a food's name into the search box (`black beans canned`, say) and click **Search**. In the results, prefer a plain, unbranded entry with a ✓ in the **AA** (amino acid) column: only foods with amino acid data can be used to judge protein quality and suggest complements. Click **Add to pantry**. The results stay on screen, so you can add another from the same list.

- **A packaged food?** Type the 12- or 13-digit barcode number from the package instead of the name.
- **Can't find it?** Open **Can't find it? Save just the name for now** under the search box. That saves the name only; link it to real data later with **Link a food**.
- **Taken to an Annotate page?** After you add a food, NuMa may open its Annotate page to ask for its glycemic index (GI) or [DIAAS](#gloss-diaas). Unless you track blood sugar ([Workflow 7](#wf-blood-sugar)), click **Skip for now**: you go back to your search results.

**Step 7 — Look at one of your foods.** Click a food's name in your pantry list to open its page. Type the amount you usually eat (`1 cup`, `150 g`) into the amount box and click **Recalculate nutrients**. Then open these sections by clicking their headings:

- **Protein Summary:** the food's protein, and its **DCP** (digestible complete protein), the part of that protein your body can actually use. For most plant foods DCP is noticeably lower.
- **Protein Quality:** a score for each essential amino acid. A score below 1.0 marks a shortfall; the lowest is the food's *limiting amino acid*. Brown rice, for example, is short of lysine.
- **Protein Complement Suggestions:** if the food has a gap, foods that would close it, and how much of each. Suggestions from your own pantry come first, under **From your pantry**.

**Step 8 — Check for missing data.** Go to **Foods → 9. Check database**. It lists foods with problems, such as no calorie value or no amino acid data. Fix your starred foods first. **Problems by food** at the top of the page lists each food's problems together, with a button for each fix. Don't try to fix everything now; [Workflow 10](#wf-cleanup) covers this properly.

**What you now have:** your everyday foods in NuMa, with the most important checked. Logging meals is now mostly a matter of picking from foods you've already found, and complement suggestions will name foods in your own kitchen.

*Sections used:* [My Pantry](#pantry-web) · [Food Cache](#food-cache-web) · [A food's page](#food-page) · [Protein Quality](#protein-quality) · [Protein Complement Suggestions](#comp) · [Checking your data](#checking-your-data)

---

### Workflow 2 — Log your first day {: #wf-first-day}

*Search terms: log a meal, food diary, record what I ate, first meal, daily log.*

**What this does:** records one day's eating and shows you what it added up to.

**Before you start:** your profile should be filled in (**Settings → 1. Your Profile**: age, sex, weight, height, activity level). Without it, NuMa can't compare what you ate with what you need.

**Step 1 — Create a meal.** Click **Meals & Log**. In the **New Meal** form at the top, give the meal a name ("Breakfast") and today's date, and create it. The meal's page opens, with a search box. If it's the day's first meal and you have [daily starting items](#daily-start), they're already in it.

**Step 2 — Add what you ate.** Type a food's name and click **Search**. Foods from your pantry and Food Cache come first, so after Workflow 1 most of what you want is near the top. In the result's amount box, type how much you ate (`1 cup`, `40 g`, `2 slices`, `p1` for the food's first saved portion) and add it. Repeat for each food. You can add a recipe the same way. If NuMa opens a food's Annotate page to ask for its glycemic index, click **Skip for now** to get back to the meal.

- If you drank something, tick its **Drink** box, so NuMa counts its water as a drink.
- A typing mistake is easy to fix: click **Edit** or **Undo** on the green **Added …** line straight away, edit the amount inline, or remove the item with ✕.

**Step 3 — Mark it complete.** When the meal holds everything you ate, click **Mark complete**. An incomplete meal still counts; marking it tells NuMa (and you, later) that the day's totals are final.

**Step 4 — Read the meal's analysis.** Scroll down. **Nutritional Analysis** compares each nutrient with your daily targets, with colors showing how close you are. **Meal-Level Protein Analysis** pools the protein from all the foods: foods often complement each other, so the meal's protein quality can be better than any one food's.

**Step 5 — Log the rest of the day.** Create a meal for each eating occasion. Once a date has more than one meal, an **Analyze full day** button appears on each of them. Click it to see the whole day pooled: total nutrients against your targets, the day's [DCP](#gloss-dcp) (digestible complete protein) against your protein goal, and suggestions for anything still short.

**What you now have:** a complete day, and a first honest look at it. Most people find at least one surprise.

*Sections used:* [The Meals & Log menu](#meals-menu-web) · [Meal Items Table](#meal-detail) · [Entering amounts](#amount-formats) · [Nutrient Analysis Table](#nutrients) · [Color coding](#color-coding) · [Analyze full day](#full-day)

---

### Workflow 3 — Build a recipe {: #wf-recipe}

*Search terms: create recipe, recipe nutrition, recipe as complement, cooking.*

**What this does:** enters a dish you make often, so you can log it in one step and see its nutrition per serving. A recipe also becomes a candidate for complement suggestions, so NuMa can say "add 180 g of your lentil soup" rather than just "add lentils".

**Step 1 — Create it.** Click **Recipes**, then **New recipe**. Give it a name ("Lentil soup"), the number of servings it makes, and, if you know it, its total yield (the weight of the finished dish).

**Step 2 — Add the ingredients.** On the recipe's edit page, search for each ingredient and give its amount, exactly as you'd put it in the pot: lentils (200 g, dry), onion (80 g), garlic (10 g), vegetable broth (500 g). A **Running totals** card at the side updates as you go, with calories, protein and [DCP](#gloss-dcp) for the whole recipe and per serving. A recipe can also be an ingredient of another recipe.

**Step 3 — Save, and read the analysis.** Click **Save recipe details**. The recipe's page shows the same sections as a food's page, per serving: nutrients, protein quality with each ingredient's contribution, complement suggestions and glycemic load.

**Step 4 — See it used as a complement.** Open a food that's short of lysine, such as corn tortillas (**Foods → 2. Analyze a food portion**, then `46 g`, about two tortillas). Open **Protein Complement Suggestions**. Your lentil soup appears as a candidate, with its recipe code (R followed by a number) and how much of it would close the gap: under **Other options**, as something you could make. Once you've made a batch, tick **In My Pantry** on the recipe's page and it moves up to **From your pantry**, as something you have ([Recipes in your pantry](#pantry-recipes)).

**Step 5 — Log it.** In a meal, search for the recipe by name and enter the number of servings you ate.

**What you now have:** a dish you can log in seconds, analyzed per serving, and available to NuMa's suggestions. When you change the recipe later, every meal and recipe that uses it is updated.

*Sections used:* [The Recipes menu](#recipes-menu-web) · [Recipe Ingredient List](#recipe-ingredients) · [Recipe servings and grams](#recipe-servings-grams) · [Changing a recipe](#recipe-dcp-cascade)

---

### Workflow 4 — Close a meal's protein gap from your pantry {: #wf-pantry-gap}

*Search terms: complementary protein, missing amino acid, what to add, incomplete protein.*

**What this does:** shows how complement suggestions turn a meal's protein shortfall into a practical choice from your own kitchen.

**Step 1 — Make a meal with a gap.** Create a meal (**Meals & Log → New Meal**) and add `brown rice cooked`, 1 cup.

**Step 2 — Read its protein analysis.** Open **Meal-Level Protein Analysis**. Rice on its own is short of lysine, so its [DCP](#gloss-dcp) (digestible complete protein) is well below its raw protein.

**Step 3 — Read the suggestions.** Open **Protein Complement Suggestions**. NuMa names the amino acid(s) you're short of under **Gaps**, then foods that would close them. Foods and recipes from your pantry come first, under **From your pantry**; your other recipes and the built-in list follow under **Other options**. Each says how much would be needed.

**Step 4 — Add one, and look again.** Add a suggested food to the meal (black beans, ½ cup, say). The meal's DCP rises, often by more than the beans' own protein would suggest, because each food now supplies what the other lacks.

**Step 5 — Remember the day.** Complements don't have to be in the same meal. If the gap remains at the end of the day, **Analyze full day** shows it, with suggestions for the whole day.

**What you now have:** a meal that uses its protein fully, and a feel for how complementing works. Suggestions for foods you'd never eat? Tick **Ignore this suggestion in recalculation** beside each, then click **Recalculate complements**.

*Sections used:* [Protein Complement Suggestions](#comp) · [Meal Protein Digestibility Analysis](#meal-diaas) · [Ignoring a complement suggestion](#ignore-complement) · [Amino Acid Gaps](#gap)

---

### Workflow 5 — A food NuMa doesn't know, or a supplement {: #wf-unknown-food}

*Search terms: UPC, product not found, nutrition label, vitamin tablet, multivitamin, pill.*

**What this does:** gets a food into NuMa when a name search doesn't find it, and enters a dietary supplement so its nutrients count.

**A packaged food: try the barcode.** In any search box, type the 12- or 13-digit number under the package's barcode. NuMa looks it up in Open Food Facts, a large, volunteer-built database of packaged foods. Check the result against the label: volunteer data is usually right but not always.

**Still not found: make a custom food.**

1. Go to **Foods → 7. Custom food profiles** and click **Create**. If a similar food exists, use **Copy a cached food as a draft** instead, and change only what differs.
2. Enter the name, then the nutrients from the label. Labels give amounts per serving; enter the serving size and NuMa converts, or work per 100 g. Fill in calories, protein, carbohydrate, fat and fiber at least.
3. Note where the figures came from in **Note**, and save. The food now works like any other.

**A supplement tablet.**

1. Create a custom food as above, with serving size **1** and unit `tablet` (or `capsule`, `softgel`, `gummy`, `scoop`).
2. Enter each nutrient exactly as printed on the label, such as `25 mcg` or `400 IU` ([IU](#gloss-iu): International Units). Save. NuMa adds a "1 tablet" portion and marks the food as a supplement.
3. Log it in a meal as `1 tablet`. Its nutrients count toward your day's totals and upper limits, and nutrient tables show how much came *from supplements*, which matters most for vitamin B12 on a plant-based diet.

**What you now have:** a food or supplement that NuMa counts properly. Try the barcode first: many supplements are in Open Food Facts already.

*Sections used:* [USDA Food Search Results](#food-search) · [Custom food profiles](#custom-foods) · [Dietary supplements](#supplements) · [Data entry](#data-entry)

---

### Workflow 6 — A week in review {: #wf-week}

*Search terms: trends, weekly review, logging days, progress, history.*

**What this does:** turns a week of logged days into patterns that no single day can show.

**Step 1 — Log a week.** Use Workflow 2 each day. Mark each meal complete when it's done.

**Step 2 — Open the Daily Summary.** Click **Analysis → 1. Daily summary**. The **Recent Days** table lists every date you've logged: whether the day is complete, protein and its percentage of your goal, the day's [DCP](#gloss-dcp) and its percentage, and the day's glycemic load if you track it. Click a date to reopen that day's full analysis.

**Step 3 — Look at averages.** Click **Nutrient averages over a period** and choose a 7-, 14- or 30-day window. NuMa averages your intake and compares it with your targets. This is where a nutrient that's a little low every day shows up, the kind of gap one good or bad day hides.

**Step 4 — See the shape.** Click **Nutrient plot**, tick Day DCP and Protein (or any nutrient you're curious about), and click **Plot**. A line across your days, with your target drawn in, often makes a pattern obvious at a glance.

**Step 5 — See what you eat most.** **Analysis → 2. Food use in meals** ranks the foods you actually ate over a date range. The foods at the top are the ones whose data most deserves to be right.

**What you now have:** a picture of your eating over time, and of the one or two nutrients worth working on.

*Sections used:* [The Analysis menu](#analysis-menu-web) · [Nutrient Averages Across Days](#trend) · [Nutrient Plot](#nutrient-plot) · [Food Use in Meals](#fooduse)

---

### Workflow 7 — Watching your blood sugar {: #wf-blood-sugar}

*Search terms: blood glucose, low GI, diabetic, pre-diabetes, glucose monitor.*

**What this does:** sets NuMa up to track glycemic load, the measure of how much a meal is likely to raise your blood sugar, and finds lower-glycemic swaps. Skip it if blood sugar isn't a concern for you.

**Step 1 — Settings.** In **Settings → 1. Your Profile**, set **your glucose tolerance** (impaired if you have diabetes, prediabetes or insulin resistance) and, if you like, a **daily glycemic load target**; **Help me choose a target** suggests one. If you can, also build the 2021 glycemic index table in **Settings → 7**; it takes a few minutes and gives better values.

**Step 2 — Give GI values to your carbohydrate foods.** NuMa never guesses a food's glycemic index (GI); you choose each one from published tables. You only need them for the carbohydrate foods you eat most: grains, bread, rice, pasta, oats, potatoes, beans and lentils, fruit, sweeteners. For each, go to **Foods → 8. Annotate**, click **Edit**, and use **Look up a GI value from the published reference table**. Prefer the same food prepared the same way, tested in people like you. If nothing matches, leave it blank.

**Step 3 — Read a meal's glycemic load.** Open a meal. Its **Glycemic Load** section gives the meal's total, rated low, medium or high, and an estimated GI for the meal as a whole. Under the title, the day's glycemic load so far is shown against your target.

**Step 4 — Find swaps.** In **Top Contributors**, rank by glycemic load. For a medium or high meal, NuMa suggests lower-GI foods from your Food Cache with similar carbohydrate, and what each would do to the meal's load.

**What you now have:** glycemic load on every meal and day, checked against your target. Published GI values are averages; your own response can differ, and a glucose meter or monitor is the final word.

*Sections used:* [Glycemic Index](#gi) · [Choosing a GI value](#choosing-gi-values) · [Daily glycemic load target](#gl-target) · [Glycemic Load Output](#glycemic) · [Lower-glycemic swaps](#gl-swaps)

---

### Workflow 8 — "What if I stopped eating this?" {: #wf-whatif}

*Search terms: try a change, hypothetical, swap everywhere, simulate, experiment.*

**What this does:** shows how your nutrition would change if you dropped, added or swapped a food, without changing anything you've logged. Then, if you like the result, makes the change.

**Step 1 — Choose the days.** Go to **Analysis → 4. What-if: meals**. Type a date range, one per line, such as `2026-09-01:2026-09-30`.

**Step 2 — Describe the change.** In the first change row, choose **Remove**, **Add**, **Replace** or **Change amount**, and pick the food: type part of its name and choose it from the list. Add more rows with **Add another change**; they all apply together.

**Step 3 — See the effect.** Click **Show the effect**. NuMa shows your average daily nutrition over those days, before and after, nutrient by nutrient. Switch between averaging over every logged day and only the days the food was eaten, to see both the effect on your diet overall and on the days it mattered.

**Step 4 — Apply it, if you want to.** A what-if changes nothing unless you click **Apply**. To change future eating, just eat differently. To correct the record, for example because you've been logging the wrong food all along, **Analysis → 2. Food use in meals** has a **Substitute a food or recipe** panel that replaces one food with another throughout the meals you select.

**What you now have:** an answer to "what difference would it make?" before you change your eating. **What-if: recipes** does the same for your recipes.

*Sections used:* [What-if: Meals](#whatif) · [What-if: Recipes](#whatif-recipes) · [Saving and applying a what-if](#whatif-apply) · [Replace a food everywhere](#fooduse-substitute)

---

### Workflow 9 — Comparing foods while you shop {: #wf-compare}

*Search terms: comparison, which is better, versus, vs, grocery.*

**What this does:** puts several foods side by side, so you can see which is the better buy for you.

**Step 1 — Gather the foods.** Click **Compare**. Search for the first food, tick it, then search for the next. Whatever you ticked is kept as you search again, up to eight foods or recipes. You can also tick foods in your pantry, the Food Cache or the Recipes list and bring them in with **Add selected to comparison**.

**Step 2 — Read the tables.** By default everything is compared per 100 g, which shows how concentrated each food is. Set an amount for each item to compare realistic servings instead. The tables cover ingredients, protein quality, glycemic values and all nutrients.

**Step 3 — Save it.** Give the comparison a name under **Save this list** to reopen it later, for example while deciding between two brands of tofu.

**What you now have:** a clear answer to "which of these is better for me?", based on your own targets.

*Sections used:* [Compare](#compare-web) · [Comparison Tables](#comparison)

---

### Workflow 10 — Cleaning up your data, monthly {: #wf-cleanup}

*Search terms: data quality, fix data, maintenance, check data, errors.*

**What this does:** finds and fixes the data problems that matter most, in about half an hour a month. NuMa's results are only as good as the food data under them.

**Step 1 — Start where it matters.** Go to **Foods → 9. Check database** and click **Problems by food**. Sort by **most used**: a problem in a food you eat daily matters far more than one in a food you used once.

**Step 2 — Fix the real problems.** Each problem has a button for the fix NuMa can offer, such as filling in calories from protein, carbohydrate and fat, or converting a value entered in the wrong unit. For a missing nutrient group, **Borrow values from** copies figures from a similar food you choose.

**Step 3 — Dismiss what doesn't matter.** Basil doesn't need macronutrients; a supplement doesn't need amino acids. Mark such gaps **not needed** and NuMa stops listing them.

**Step 4 — Fill amino acid gaps.** Foods with no amino acid data can't be scored for protein quality. Look for a plain, unbranded equivalent in a search (look for the ✓ in the [AA](#gloss-aa) column), or ask Claude AI for the figures: **Fetch missing data from Claude AI** builds the request for you, and you paste the answer back. [Workflow 12](#fix-food-data) gives the order to try these in.

**Step 5 — See what changed.** After a fix, NuMa lists every recipe and meal whose figures moved. Past days are recalculated too, and say so.

**What you now have:** more accurate results everywhere, starting with the foods you eat most. The Home page tells you when new problems turn up.

*Sections used:* [Checking your data](#checking-your-data) · [Problems by food](#problems-by-food) · [Seeing what a fix changed](#data-effects) · [Fetching missing data with Claude AI](#fetch)

---

### Workflow 11 — A kidney-stone concern: oxalate {: #wf-oxalate}

*Search terms: low oxalate diet, kidney stone, stones, calcium oxalate.*

**What this does:** shows how much oxalate your usual foods contain, for anyone advised to limit it.

**Step 1 — Turn it on.** In **Settings → 1. Your Profile**, tick **Look up oxalate content for foods**, and save.

**Step 2 — Look at your foods.** Open a food's page. NuMa looks the food up by name in the Harvard oxalate table and links the best match, showing its oxalate for the table's serving and a category from very low to very high. The match is automatic, so check it: if it's marked **auto-matched — correct if wrong** and the food isn't right, click that link and choose the right entry, or say the food isn't in the table.

**Step 3 — Look at your meals and days.** Meal, recipe and day pages total the oxalate from matched foods. Foods the table measures only by volume (a cup, a piece) can't be scaled, so they're left out of the total and noted. A day's total can be compared with the 40–50 mg a day often suggested for people who form calcium-oxalate stones; your doctor's advice comes first.

**What you now have:** oxalate figures for your usual foods and days. Spinach, rhubarb, beet greens and almonds are the usual surprises.

*Sections used:* [Oxalate Data](#oxalate) · [Correcting a wrong match](#oxalate-link-correction) · [Antinutrients](#antinutrients)

---

### Workflow 12 — A food is missing nutrient data, or its figures look wrong {: #fix-food-data}

*Search terms: no amino acid data, missing data, missing nutrients, incomplete food, fill gaps, AI help, ask AI, ask Claude, chatbot, ChatGPT, prompt, doubtful values, bad data, wrong numbers, borrow values.*

**What this does:** gets better figures for a food whose data is incomplete (the common case is "No amino acid data for this food") or looks wrong. There are three ways, and the order matters: each is less certain than the one before it.

**Step 1 — Look for a better-documented record of the same food.** [USDA](#gloss-usda)'s Foundation and [SR](#gloss-sr) Legacy records are the most complete there are; branded records list only what's on the label. Search for the food's plain name ("chocolate, dark" rather than a brand) and look for a ✓ in the [AA](#gloss-aa) column, or for whichever nutrients you need. The search also covers the Canadian, UK, Australian and French national food tables. If you find a good match, use it in your meals and recipes instead, or copy its values into your food (Step 2's first box does that).

**Step 2 — Borrow values from a similar food.** If no record of the same food has the figures, a close relative often does: another dark chocolate, another bean. Open the food's **Edit** page (Foods → 7. Custom food profiles → **Edit**, or the links in the warning on the food's own page). Its first two boxes do this:

- **Copy nutrient values from another food** copies the figures you tick, exactly as the other food has them.
- **Estimate amino acids from another food** copies only amino acids, scaled to your food's own protein. A food with twice the protein gets twice the amino acids.

Copied values are marked *estimated* on the food's page.

**Step 3 — Ask Claude [AI](#gloss-artificial-intelligence).** When neither search turns up anything usable, use the Edit page's third box, **Ask Claude AI for help**. (Claude is the AI chatbot at [claude.ai](https://claude.ai), made by Anthropic.)

1. Under **Ask for**, choose **the whole nutrient profile** or one nutrient group (only amino acids, say).
2. Choose **Only the values it's missing** (it keeps every figure the food already has) or **Every value, to replace doubtful figures** (for figures you don't trust).
3. Click **Write the prompt for Claude AI**. NuMa writes the request (a "prompt") for you; click **Copy prompt to clipboard**.
4. Open a new chat at claude.ai, paste the prompt and send it. Claude answers in a form NuMa can read.
5. Copy Claude's whole answer, go to **Import Claude response**, paste it and click **Review**. Check the figures and the sources Claude names, then click **Import**. Nothing is saved before this.

The food's own page offers a shortcut for amino acids: the *No amino acid data* warning ends with **Write a prompt for Claude AI**. Step 3 comes last because AI figures need the most checking. Claude can be wrong, so look at the sources it cites.

**What you now have:** a food with the best figures available, and a note of where each came from. If even Claude finds nothing, the honest answer is that nobody has measured it; mark the gap **not needed** so NuMa stops asking ([how](#key-sources)).

*Sections used:* [When a food has no data for a nutrient](#key-sources) · [Custom food profiles](#drafted-foods) · [Fetching missing data with Claude AI](#fetch) · [Missing amino acid profiles](#missing-aa)

---

### A few more things worth trying {: #wf-more}

*Search terms: more features, what else, tips.*

A few other things worth a look, once you've got the basics down:

- **Convert (Foods → 4).** How many grams is a cup of this food, or a tablespoon? Convert answers without the rest of the analysis. See [Convert](#convert).
- **Recipes inside recipes.** A recipe can be an ingredient of another: a lentil sauce used in three different dinners, say. Change the sauce and every dish using it is updated. See [Changing a recipe](#recipe-dcp-cascade).
- **Archive instead of delete.** Hide a recipe, food or pantry entry you're not using right now, without losing it. See [Archiving](#archive).
- **Print or save a page.** A recipe's, food's, meal's or day's page has a printable version, with a half-sheet layout for recipe cards. See [The Recipes menu](#recipes-menu-web).
- **Two pages at once.** Ctrl+click a link to open it in a browser tab beside NuMa's window. See [Working in two windows](#two-windows).
- **Protein per meal.** Each meal's page says whether it carries the amount of protein research links with keeping muscle, worked out for your weight and age. See [Protein per meal](#protein-per-meal) and [When to eat protein](#protein-timing).
- **Move foods and recipes to another computer** as CSV files. See [Moving foods and recipes with CSV files](#csv-transfer).

## Part 4 — Menu by menu {: #part-3-using-numa}

*(Reading time: 2 hours, 20 minutes)*



NuMa shows its screens through a browser, normally in a window of its own (see [Browser to Launch](#browser-to-launch)). That makes NuMa easier to develop, and gives you an interface that already feels partly familiar.

This Part follows the navigation bar from left to right: one chapter per menu, and under it one section per menu item, saying what it's for, what's on the page, and what you can do there. One chapter is not a menu: [A food's page, and every analysis page](#analysis-pages) covers the analysis that food, recipe, meal and day pages all share. Operations that work the same way on many pages, such as entering amounts and searching, are in [Part 5](#skills).

### A. Opening NutriMagnus

*Search terms: start the program, open NuMa, page won't load.*

Start NuMa the way it was set up on your computer: a desktop icon, an applications-menu entry, or a shortcut. It opens by itself, normally in a window of its own with no address bar or tabs (see [Browser to Launch](#browser-to-launch)), otherwise in a browser tab at an address like `http://127.0.0.1:8000`. That address just means "this computer, talking to itself", not a site on the internet; the numbers may differ. While NuMa starts you see a short "starting" page, which turns into the home page by itself.

#### What you see on the home page {: #home-page-tour}

*Search terms: start page, dashboard.*

The home page starts with a short reminder that NuMa is not medical advice, then the **Welcome to NutriMagnus** heading, a one-line description, and these status lines:

- **Dietary preferences:** your current setting (e.g. "All animal foods"), with a link to change it in Settings.
- **Active profile:** a one-line summary (age, sex, weight, height, activity level), or "not set" with a link to set one up.
- **Current manual version / Current program version date:** the date of the manual and of the program you're running, both as `yyyy-mm-dd:hhmm`, then a **see what changed** link into [What's new](#updates-log), whose newest release summary starts with a short *Version overview*. After it, when no update is showing, **Check for updates now** checks GitHub at once instead of waiting for the regular check. It also undoes an earlier "don't show this again" on an update banner, in case you change your mind.

Banners can appear above the heading when they apply:

- **Your profile isn't set yet**, until you save a profile. It links to Settings and to the [setup steps](#first-setup), and has a **Don't remind me about this again** box.
- **NEW STARTER ITEMS**, the first time a new version runs, if it added or improved [starter foods or recipes](#starter-data).
- A [database](#gloss-database)-integrity warning, an "update installed" confirmation after Update Now, or an update-failed message.
- **UPDATE AVAILABLE**, when a newer release is on GitHub. On the packaged Linux install it has an **Update Now** button that installs the update in place; elsewhere (Windows, or Linux run from source) a **Download NutriMagnus** button fetches the new installer. It says what the update would add to or improve in your [starter foods and recipes](#starter-data), and has a **Don't show this again for this version** box. While it shows, the separate **New user manual available** banner is left out, since the new program brings its own manual.

The bottom of the page gives the release and build numbers, e.g. *NutriMagnus 0.1.0-rc.26 (build 2026-10-17:0722)*.

**When does NuMa check for a new release?** Each time the home page loads, whether at launch, on reload or on coming back to it. The answer is kept for a few hours, so going back and forth doesn't contact GitHub every time. Once a newer version exists, **UPDATE AVAILABLE** shows on every page load until you install it or tick "Don't show this again for this version". A later release always shows, whatever you dismissed before.

### B. Finding your way around {: #web-shortcuts}

*Search terms: hotkeys, menu bar, exit, close the program, shut down, command palette, list of commands, cheat sheet, Ctrl+K, open by ID, open by number, recipe code, meal number, go to ID.*

Every page has the same navigation bar across the top: **NuMa** (home), **Foods**, **Recipes**, **Compare**, **Meals & Log**, **Analysis**, **Settings** and **Manual** (this document). **Foods**, **Recipes** and **Analysis** open drop-down menus; the others go straight to their page.

**Keyboard shortcuts.** Hold **Alt+Shift** and press the underlined letter of a menu item: `F` Foods, `R` Recipes, `C` Compare, `M` Meals & Log, `N` Analysis, `S` Settings, `A` Manual. Settings sections have them too: `Alt+Shift+3` jumps to section 3, Dietary Preferences; section 10, Daily Starting Items, is `Alt+Shift+0`; sections 11 to 16 use a letter of their name (`L` Meals & Log columns, `T` Starter Data, `B` Browser to Launch, `D` Data Quality Reminder, `E` Keyboard Shortcuts, `Y` System Issues). With a menu open, pressing an item's number opens it; in the Foods menu, item 10 (Archived foods & recipes) is `0`. They work in any desktop browser.

<span id="command-palette"></span>
**Can't remember a shortcut? Press `Alt+Shift+K`.** It opens the *command palette*: a panel listing every page in the menus, plus anything the page you're on has a shortcut for (its search box, its Items section, Settings' sections), each followed by the keys that reach it, such as *Foods: Food Cache (Alt+Shift+F, then 5)*. So the only shortcut you need to remember is `K`. The **⌘ Alt+Shift+K** button at the right end of the menu bar opens it too.

- Start typing to narrow the list: *cache* leaves Food Cache; *water* leaves Settings' Water Tracking.
- Whatever you type can also be searched for: the bottom of the list offers *Search foods for …*, *Search recipes for …* and *Meals that contain …*.
- ↑ and ↓ move the highlight, Enter opens it, Escape closes the panel. Clicking an entry works too.
- Choosing something you could have done with a shortcut does exactly what that shortcut does, on the page you were on.
- **Quit NuMa** is in the list as well, which is handy in Firefox, where `Ctrl+Q` quits Firefox instead (see below).

Used to other programs? `Ctrl+K` opens the same panel.

- On a drop-down menu the shortcut also puts you on its first item: ↑ and ↓ move, Enter or Space picks, Escape closes.
- `Alt+Shift+I`, on any page with a search box, puts the cursor in it with the text selected, ready for a new search, and clears the old results (opening the box's section first if it's closed).
- `Alt+Shift+U`, in the manual, returns to the NuMa page you opened it from (see [Getting back to where you were](#manual-back)).
- `Alt+Shift+U`, on a meal, a recipe or a food page, does what clicking **Nutritional Analysis** in the page's Contents sidebar does: it takes you to that section (on a food page, opening it first if it's collapsed). Pages with no Nutritional Analysis entry in their sidebar don't use it.
- `Alt+Shift+Y`, on a page with an Items section (a meal, Compare, Analyze a recipe portion, or a recipe's Edit page, where it's Ingredients), moves to that section.

<span id="go-to-id"></span>
**Opening a recipe or meal by its ID.** On the **Recipes** list, **Meals & Log** and **Search meal history**, every row has an [ID](#gloss-id): the Code column on Recipes (**[R21](#gloss-code)**; type just `21`), the ID column on the meal lists. Press **Alt+Shift+G** (for "go") and let go, type the ID's digits, and press **Enter**: that recipe or meal opens, just as if you'd clicked its name. While you type, a box at the bottom of the window shows the ID so far and the row it matches, so you can see you've got the right one before pressing Enter. **Backspace** removes the last digit, and **Esc** (or any other key) cancels. If no row on the page has that ID, the box says so and nothing opens (only rows shown in the list count; a meal further back, or an archived recipe while archived ones are hidden, needs the list to show it first).

Turn shortcuts on or off in **Settings → Keyboard Shortcuts** (`Alt+Shift+E` there). The setting is kept in your browser and takes effect at once. With shortcuts off, the menu bar's button reads **⌘ Commands** and still opens the command palette, as does `Ctrl+K`; the palette then lists pages without their keys.

<span id="quit-numa"></span>
**To quit NuMa, press `Ctrl+Q`** on any NuMa page. NuMa stops and its window closes; if the page has unsaved changes, it asks first. This works whether or not the Alt+Shift shortcuts are on.

- **In Firefox,** `Ctrl+Q` quits Firefox itself, all its windows, and NuMa notices within a few seconds and stops too. Firefox doesn't ask about unsaved changes on a NuMa page, so save first. This only stops NuMa if the last NuMa page you used was in Firefox and Firefox has quit completely; closing just NuMa's tab leaves NuMa running.
- **In NuMa's own window** (Chrome, Chromium, Brave, Edge or Vivaldi) on the KDE desktop, NuMa closes the window itself. Elsewhere the browser may not allow that; the page then says "NuMa has stopped", and you close it.
- **On a Mac,** use `Ctrl+Q`, not `Cmd+Q`, which quits the browser.

<span id="search-keys"></span>
**Moving through search results from the keyboard.** After a search, the first result is outlined in red (on a meal's or recipe's add search, its amount box). `↓` and `↑` move the outline; `Enter` opens that result. When you come back (`Alt+←` or Back), the outline is where you left it. This works in every search list.

**Outlines and unsaved changes.** Long pages (a food, a recipe, Edit Recipe, a meal) have an outline down the side: click a heading to jump to it. A form with unsaved changes lights up its Save button (solid blue, red border) with "Unsaved changes" beside it, and the browser warns you before you leave. The big edit forms (Edit Recipe, a meal, Edit Custom Profile, Annotate a Food) go further, as their "Data-entered safety" note says: follow a link elsewhere in NuMa with unsaved edits and NuMa offers to save them, leave without saving, or stay. On Edit Custom Profile, Edit Recipe and a meal page, running or re-sorting a search saves your edits first, and a note above the results offers to undo that. Closing or refreshing the tab is the one case NuMa can't catch; only the browser's own warning appears, so save first.

#### Search boxes remember your last search {: #search-memory}

*Search terms: search history, previous search, restore search.*

On a meal's "Add Food or Recipe" search, a recipe's "Add Ingredient" search and Foods → Search, if you follow a link away and then come back to the same page, your last search and its results are restored. This works for a plain link back (the browser's Back button keeps them anyway) and is kept per page, so one meal's search never appears on another's.

**Adding from the results keeps them.**{: #search-keeps-results} When you add a result to a meal, a recipe or your pantry, the same search results stay on screen, with a green **Added …** line naming what you just added, so you can go straight on and add another from the same list. On a meal, that line has **Edit** and **Undo** buttons ([Fix or undo an addition](#meal-undo-add)). They change only when you run a new search, or click **Clear search**.

This lasts as long as the browser tab stays open. **Clear search** (beside the search box while a search is showing), or closing the tab, clears it.

**Menus remember where you were.** Clicking **Recipes**, **Meals & Log**, **Compare**, **Settings** or **Manual** from another section takes you back to the page you were last on there, such as the recipe you were editing or the items lined up on Compare. Clicking it while you're already in that section goes to its main list. When the memory took you back, the breadcrumb is highlighted, with an "All recipes" / "All meals" link if you wanted the list. **Foods** and **Analysis** are drop-downs, so instead a small "↩" link beside them names the last page you used there, and returns you to it in one click. Following a breadcrumb back to a list (e.g. **Recipes** at the top of a recipe) always starts fresh.

**Long pages come back the way you left them.** The Daily Summary, a meal, a recipe and a food's page remember how far down you'd scrolled and which sections were open, for as long as the tab stays open. Two exceptions: inline **Edit** panels never reopen by themselves (closing one is how you discard what you typed), and a link to a particular spot on a page (ending in `#something`) still goes to that spot.

#### Working in two windows {: #two-windows}

*Search terms: new tab, second window, side by side, ctrl click, middle click, browser tab, print page, opens in Chromium, default browser.*

NuMa's own window has no tabs, but you can still have two NuMa pages open, say a recipe beside the Food Cache. **Hold `Ctrl` and click a NuMa link** (or middle-click it, or `Shift`+click it). That page opens in an ordinary browser tab, and NuMa's window stays as it was. This works in the User Manual too: Ctrl+click a section in its contents, or a link in its text, and that section opens in a tab. On a page with a **Contents** sidebar (a meal, a day, a recipe), Ctrl+clicking an entry opens a second copy of the same page in a tab, at that part.

Otherwise every NuMa link and button, **Print / Save** included, opens in NuMa's own window, and the new page has a **Back** button or link (or press `Alt+←`). Only links to outside websites, such as claude.ai or GitHub, open in your browser.

- **Both show the same data.** Whatever you save in one is saved for both, but a page already on screen doesn't change by itself: reload it to see what you changed in the other one.
- **To get back,** switch to the NuMa window with `Alt+Tab` or its taskbar button. The browser tab stays open until you close it.
- **Closing the tab doesn't stop NuMa.** Quit NuMa from its own window, with `Ctrl+Q` (see [quitting NuMa](#quit-numa)).

The first time, NuMa explains what's about to happen: **Open it** goes ahead, **Cancel** stays put, and **Don't show this again** skips the explanation from then on. To bring it back, tick **In NuMa's own window, explain before a Ctrl+click opens a page in a browser tab** in **Settings → 13, Browser to Launch**.

If NuMa runs in a normal browser tab (Firefox, or with **Open NuMa in its own window** off), Ctrl+click just opens another tab, as usual.

### C. The Foods menu {: #foods-menu-web}

#### Search (Foods → Search) {: #search-web}

*Search terms: food search, find a food, look up food.*

Searches your own foods and recipes and the online and bundled food databases at once. Type part of a food's name, an [FDC ID](#gloss-fdc-id), a 12- or 13-digit barcode ([UPC](#gloss-upc)-A or [EAN](#gloss-ean)-13), or a food's or recipe's [code](#search-by-code). Put `!` before a word to leave it out: `beans red !kidney cooked` skips kidney beans ([Excluding words](#search-exclude)). How results are found and ordered is in [Setting up a search](#search-ranking).

After a search, the cursor lands on the first result, so Enter opens it (on a meal or recipe, it lands in that result's amount box). Click a result to open its page, with its [Nutritional Analysis](#nutrients), [Protein Quality](#protein-quality) and complement suggestions. The results table, its sort order and its Source checkboxes are described next.

##### Search results, column by column {: #food-search}

*Search terms: results columns, AA checkmark, slow search, speed, beverage, finished recipe, lost ticks, checked foods disappear, multiple searches, basket.*

The list after a food search: your own pantry, Food Cache and recipes first, then [USDA](#gloss-usda) FoodData Central, Open Food Facts[^3] and the other sources.

Columns:

<pre>
    AA      Amino acid data status.
              checkmark    Confirmed in your local cache.
              ~checkmark   Likely available (Foundation/SR Legacy not yet
                           fetched); confirmed on selection.
              X            No amino acid data.

    Search results carry only a food's name and type — USDA's search results
    don't include nutrient values up front, so "~checkmark" is a guess, not a
    fact. Opening a food's page (or adding it to a meal/recipe) fetches and
    caches its full details, which is when "~checkmark" turns into a confirmed
    checkmark or X. You can also check a batch of "~checkmark"
    results directly from the search list: tick their checkboxes (or the
    header checkbox to select all of them) and click "Fetch full details for
    selected" — this avoids looking up every uncached result on every single
    search, which would use up more of your daily USDA search allowance than
    necessary.
    A recipe in the results shows an <a href="#gloss-aa">AA</a> status too,
    worked out from its ingredients rather than from a nutrient record of its
    own: a checkmark
    when they add up to a full amino acid profile, an X when they do not,
    and a warning sign for a recipe with no usable ingredient data at all.

    GI      Your saved glycemic index estimate, if any. See <a href="#gi">Glycemic Index</a>.
            The figure is a link: click it to edit that value, or click the
            dash to add one. See <a href="#annotate">Annotate a Food</a>.
    DIAAS   Your saved DIAAS estimate, if any. See <a href="#diaas">DIAAS</a>.
            Also clickable, the same way.
    Notes   "y" if the food has a saved note. View it from the Food
            Cache.
    Code    The food's code: U (USDA), UD (user-drafted), R (recipe),
            OFF (Open Food Facts) ... — see <a href="#gloss-code">Code</a>.
    Food    Food or recipe name.
    Type    USDA data category or OFF.
              Foundation     Highest accuracy; most likely to have AA data.
              SR Legacy      Standard Reference; also likely to have AA data.
              Survey (FNDDS) Foods as eaten; AA data less common.
              Branded        Manufacturer data; AA data rare.
              OFF            Open Food Facts (community data).
              star in Type   Already in your local cache (instant, no
                             network call needed).
    Brand   Brand name for Branded and OFF entries.

    Source  Where the match came from:
              Pantry     Already in your Pantry.
              Cache      In your Food Cache, but not the Pantry.
              Recipe     One of your saved recipes.
              USDA       Not yet cached — from FoodData Central.
              OFF        Not yet cached — from Open Food Facts.

    Complete  Recipes only: ticked if you have marked the recipe
              finished. Tick or untick it here; it's saved at once.
              (Foods are never "complete".)
    Drink     Recipes and your own foods (Pantry, Cache): ticked if it
              is a drink, so its water counts as water from drinks (see
              <a href="#water">Water</a>). Tick or untick it here; it's
              saved at once. A USDA or OFF result not saved yet shows a
              dash: open it first. USDA beverages are ticked for you when
              saved. Not shown when water tracking is off.

    Delete  On a recipe row, <b>Delete</b> (asks first; refused for a recipe
            still in use); on a pantry row, <b>Remove from pantry</b>.
</pre>

Click a result to open it. A food not yet in your Food Cache is fetched and saved automatically.

**Compare selected.**{: #compare-checkboxes} Each row has a **Compare** checkbox. Tick any mix of foods and recipes and click **Compare nutrition of selected (up to 8)** to open [Comparison](#comparison) with them already added. The same checkbox and button are on [Food Cache](#food-cache-web), [My Pantry](#pantry) and the [Recipes list](#recipes-menu-web).

**Picking from several searches.**{: #compare-picks} Ticks in a **Compare** column are kept when you search again or go to another list, so you can gather items from many searches: tick two kinds of salmon, search for lentils and tick one, tick a recipe on the Recipes list, then click any **Compare nutrition of selected** button, and all four go in. This works across Foods → Search, [My Pantry](#pantry), the [Recipes list](#recipes-menu-web), [Food Cache](#food-cache-web) and [Compare](#comparison)'s own search. A note under each Compare button lists your picks, with **✕** to drop one and **Clear all picks**; a picked item shows ticked whenever it appears in a later search. Only the first 8 are used (the note warns you in red if you pick more). Picks are kept after Compare opens too, so you can come back (**← Back**), untick or add some, and compare again; **Clear all picks** starts afresh. They last only while the browser tab is open.

**Sort order.** A drop-down above the results offers two orders, and remembers your choice:

<pre>
    Best match to name (default)   See <a href="#search-ranking">Setting up a Food or Recipe search</a>
                                    for how this ranking works.
    Recipes, Pantry, Cache,         Same match-quality ranking, but when two
      then Other                    or more results are tied on how well they
                                    matched your search, your own Recipe,
                                    then Pantry, then Cache entries sort
                                    ahead of USDA/OFF/other external results
                                    within that tie. It never lets a weaker
                                    match from your own data outrank a
                                    stronger external match.
</pre>

Either way, your own matches come first, above a divider, with online results below, so a food or recipe you already have is never buried. Among your own matches the best match comes first; a recipe goes ahead of a food only when both match equally well.

**Source filter.** Checkboxes beside every food search box choose which sources to search: Pantry, Food Cache, Recipes, [USDA](#gloss-usda) FoodData Central, Open Food Facts, the Canadian Nutrient File, CoFID (UK), AFCD (Australia) and CIQUAL (France). Ticking or unticking one re-runs the search; unticking all of them counts as ticking all; **Select all sources** ticks every box. **What are these sources? →** explains each ([Food data](#food-data)). Your choice is kept for every search box with this filter: Foods → Search, Analyze a food portion, Convert, Compare, My Pantry, a meal's "Add Food or Recipe", a recipe's ingredient search, and the "copy from another food" searches on Edit Custom Profile.

**"Did you mean" suggestions.**{: #search-suggestions} A search with no results offers likely corrections: "brocoli" suggests **broccoli**. Click one to search again with it, or press Esc to keep what you typed. Suggestions come from your own foods, pantry and recipes, then the names in the bundled CoFID/[AFCD](#gloss-afcd)/CIQUAL [databases](#gloss-database), so they work offline but can't guess a brand name NuMa has never seen. The filter boxes on [Food Cache](#food-cache-web), [Annotate](#annotate), [Recipes](#recipes-menu-web), [Search meal history](#meal-history) and Custom food profiles' "Copy a cached food as a draft" search offer them too.

**Omitted-source warning.** Because your Source choice is kept everywhere, a box unticked once stays unticked, and a missing food can look like a search bug. So on Foods → Search and a meal's "Add Food or Recipe", a small red note beside **Sort by** names any unticked source: **Omitted from search: RECIPE**, for example.

**Online search in progress…** shows in red while USDA, Open Food Facts or the Canadian Nutrient File (the three live [databases](#gloss-database)) is being searched; hover over it to see which. They're searched at the same time, and you can keep using NuMa meanwhile. Online results are kept for ten minutes, so the same search again (when a meal page reloads after **Add to meal**, say) is instant. CoFID, AFCD and [CIQUAL](#gloss-ciqual) are bundled with NuMa, so their results appear at once, with your own.

**Result limit.** **Show up to ___ search results**, beside the Source filter, sets how many results each source returns (default 25, up to 500). Your choice is remembered.


#### Analyze a food portion / Analyze a saved recipe portion {: #analyze-portion}

*Search terms: portion analysis, analyze an amount, how much protein in.*

Like Search, but once you pick a food (or, with item 3, a saved recipe) you go straight to entering an amount, instead of seeing the per-100 g view first.

#### Convert {: #convert}

*Search terms: unit conversion, convert units, grams to cups, ounces to grams, measurement conversion.*

Converts amounts for one food, with no nutrient analysis. Search for the food, then type an amount (`3 oz`, `1/4 cup`, `150 g`) to see it in grams or mL, and the nearest named portion.

#### Food Cache {: #food-cache-web}

*Search terms: cached foods, saved foods, food list, stored foods, my foods, most eaten, frequent foods.*

Every food NuMa has fetched from [USDA](#gloss-usda), Open Food Facts[^3] or another source, plus every food you've created, is kept here: your own copy, usable offline. The columns are explained in the [Food Cache column guide](#cached) below.

- **Find a food.** **Filter this list** narrows your cached foods (a misspelling offers a ["Did you mean"](#search-suggestions) correction). **Search online** runs the same words through [Foods → Search](#food-search); after filtering, **Not here? Search online** beside the count does the same.
- **Sort by** **Most meals, last 90 days** (the foods you actually eat first: the meals each was in over the last 90 days, on its own or in a recipe, shown under **Used in**), Name, Code, Type, [DIAAS](#gloss-diaas), [GI](#gloss-gi) estimate, **Used in** (most-used first) or **Incomplete first**. NuMa remembers your choice.
- **Add to pantry** adds the food to your [Pantry](#pantry) and keeps your place; a food already there shows **In pantry**, which opens the Pantry.
- **Portions** adds or edits named portion sizes.
- **Refresh** fetches USDA's current copy, and lets you [choose which changed values to take](#review-incoming).
- **Archive/Restore** hides a food without deleting it ([Archiving](#archive)).
- **Delete** is refused while a pantry entry, recipe or meal uses the food. The refusal links every one by number ("pantry: 34 | recipe: 12 | meal: 9, 72"), so you can remove or replace it, or archive the food instead. The refusal stays under the food's row when you leave the Food Cache and come back (to open that meal, say), brought up to date: once nothing uses the food, it's gone. A keyboard shortcut back clears it, as it does the Fetch ticks.
- **Prune unused foods** removes foods nothing uses, with a box per food (ticked) so you can keep some.
- **Compare** checkboxes send foods to [Comparison](#comparison) ([Compare selected](#compare-checkboxes)).
- **Fetch missing data from Claude AI** and **Import Claude response**: below. Your **Fetch** ticks are kept when you leave the Food Cache and click your way back, for as long as that browser tab stays open. Coming back with a keyboard shortcut (a menu shortcut, or the [command palette](#command-palette)) starts the page fresh.

**Fetching missing data with Claude [AI](#gloss-artificial-intelligence).**{: #fetch} Some foods, especially branded or prepared ones, arrive without amino acid data, and a few without even calories or protein. Claude can usually find the figures. Tick the foods you want (**Select all missing [AA](#gloss-aa) data** ticks every food missing amino acids) and click **Fetch missing data from Claude AI**. You can also start from the [missing nutrient data check](#data-completeness), from the *No amino acid data* warning on a food's page (**Write a prompt for Claude AI**), or from the **Ask Claude AI for help** box on a food's [Edit page](#edit-ask-ai), which also asks for one group or the whole profile, and can ask for every value rather than only the missing ones. In what order to try Claude and the other ways of filling gaps: [Workflow 12](#fix-food-data). NuMa builds a request (a "prompt") and shows it with a **Copy prompt to clipboard** button.

The prompt asks only for the values each food is missing. Groups you've marked "not needed" are named as not needed, and a food with nothing missing is left out (the page says which).

**Asking for GI and DIAAS too.**{: #fetch-gi-diaas} Tick **Also ask for each food's glycemic index (GI) and DIAAS** at the top of the prompt page, and the prompt also asks for those, for foods that don't have them (skipping any whose Annotate page says to stop asking). Importing saves them to the food's [annotation](#annotate), as if typed on **Foods → Annotate**, with Claude's cited source beside the GI. Like nutrients, they only fill blanks unless you tick **Also replace the values these foods already have**.

From there:

1. Go to [claude.ai](https://claude.ai) — open a **new chat** (not an existing one) — paste the prompt, and send.
2. **Check the reply for gaps.** Claude's first answer often sticks to USDA data. If many values are missing or "unknown", ask in the same chat: *"Please do a literature review for the missing values and give me all the food blocks again, complete and in the same format."* That usually finds more, from published studies and other countries' databases.
3. Copy Claude's latest complete reply with the **Copy** button under it, including every fenced `json` block (if the answer is split over several messages, copy each and paste them together). Selecting the text by hand usually works too.
4. Back in NuMa, click **Import Claude response** (also on the Food Cache page), paste the reply, and click **Review**.
5. NuMa shows what it understood ([the review table](#food-import)), with warnings about anything it couldn't use. Check it, then click **Import**.

**Importing only fills gaps.** For a food already in your cache, importing adds only the missing values; its existing values, name, portions and notes stay. Where Claude gives a different value for something the food already has, the review table says so, and **Also replace the values these foods already have** takes Claude's value instead. Leave it unticked unless you mean it.

##### Food Cache — Column Guide {: #cached}

*Search terms: Food Cache columns, column meanings, food list columns, usage count, where used.*

Columns:

<pre>
    Fetch    Checkbox to select this food for "Fetch missing data from Claude
             AI" — see <a href="#fetch">Fetching missing data with Claude AI</a>. That button is only
             colored (actionable) when at least one food in the current list
             is missing amino acid data.

    Compare  Checkbox to add this food to Comparison — see <a href="#compare-checkboxes">Compare selected</a>.
             Ticks are kept when you search again or go to another list —
             see <a href="#compare-picks">Picking from several searches</a>.
             That button is only colored once 2 or more items are picked.

    Code     The food's code (see <a href="#gloss-code">Code</a>).
             U171477 = USDA FoodData Central food (number = its FDC ID).
             UD4     = user-drafted food (one you entered yourself).
             OFF3    = Open Food Facts (community-contributed data); CNF,
                       CoFID, AFCD and CIQUAL foods follow the same pattern.

    Name     Food name as stored in your cache, linked to its detail page. The
             brand (for Branded/OFF foods) appears in small text underneath.

    Type     Data source within USDA FoodData Central, or the external database it came from.
               Foundation     — USDA-analyzed reference foods; highest accuracy.
               SR Legacy      — Standard Reference database (pre-2019).
               Survey (FNDDS) — Foods as eaten, used in national dietary surveys.
               Branded        — Manufacturer-submitted data for packaged products.
               OFF            — Open Food Facts (community-contributed).
               CNF            — Canadian Nutrient File (Health Canada).
               CoFID          — UK Composition of Foods Integrated Dataset.
               AFCD           — Australian Food Composition Database (FSANZ).
               CIQUAL         — French CIQUAL database (ANSES).
               User Drafted   — A custom food: one you created in NuMa.
             A food you have changed yourself — its nutrients, its portions,
             or by giving it a GI or DIAAS value — keeps its origin and adds
             "· user-edited", e.g. "SR Legacy · user-edited".

    AA       Amino acid data status.
               ✓  Amino acid data is present in your cache for this food.
               —  No amino acid data — common for branded and packaged foods.

    GI est.  Your saved glycemic index estimate for this food, if any.
             GI reflects how quickly a food raises blood glucose (scale 0-100).
             See <a href="#gi">Glycemic Index</a> for a full explanation.

    DIAAS    Your saved DIAAS estimate for this food, if any.
             DIAAS (Digestible Indispensable Amino Acid Score) rates protein
             quality: 1.00 = complete, lower = a limiting amino acid is present.
             See <a href="#diaas">DIAAS</a> for details. Shown with a star when it's your
             own saved estimate rather than the built-in reference-table value.

    Other    "complete" when the food has macronutrients, water, minerals,
    nutrients vitamins and amino acids (which its DCP is worked out from),
             or each missing group is marked "not needed" for it; otherwise
             "incomplete", linked to the food's page. Point at "incomplete"
             to see what's missing. Omega fatty acids and phytonutrients
             aren't checked (most foods never had them measured), nor is a
             supplement (shows --). Water counts only while NuMa tracks it
             (Settings).

    Used in  How many recipes and logged meals use this food directly, e.g.
             "2 recipes, 5 meals" ("not used" if none). A recipe counts once
             however many times the food appears in it; a food reached only
             through a sub-recipe counts for that sub-recipe, not the recipe
             using it. Pantry entries aren't counted here.

    Notes    A "Notes ▸" link expands to show your own notes on the food
             (see Your notes on a food), any notes that came with it, and
             curator notes (typically added by the Claude data-fetch
             workflow) — blank if there are none.

    Actions  Portions, Refresh, Archive/Restore, and Delete for that row —
             see <a href="#food-cache-web">Food Cache</a>.
</pre>


##### Archiving {: #archive}

*Search terms: hide food, unarchive, hidden items.*

Archiving hides a food, pantry entry or recipe from everyday use (lists, food searches and complement suggestions) without deleting it: a seasonal ingredient, an old recipe you might make again, a pantry item you've used up.

**Archive/Restore** on each row of Food Cache, My Pantry and Recipes switches an entry between the two (a recipe's own page has **Archive recipe** / **Restore recipe** too). **Show archived …** / **Hide archived …** on each of those pages shows or hides archived entries; the button is filled in while they're showing, and each page remembers your choice.

What archiving does NOT do:

    - It never deletes anything. An archived food/pantry entry/recipe still
      exists and can be restored at any time with the same button.
    - It never breaks existing references. A recipe that uses an archived
      food as an ingredient still analyzes correctly; a meal that logged an
      archived recipe still shows correctly. Archiving only affects whether
      something shows up by default and whether it's offered for new use.
    - Archived foods are protected from "Prune unused foods" in the Food
      Cache -- archiving is meant to preserve data, so an archived-but-
      unreferenced food is never swept up by pruning.

Archiving something still in use (in a pantry entry, a recipe or a logged meal) gets a warning, but is allowed: those uses keep working.


##### Foods to Import Review Table {: #food-import}

*Search terms: Claude import, import preview.*

Shown when you click **Review** on the Import Claude response page: a preview of what importing will do, before anything is saved.

Columns:

    Name        Food name from the Claude response.
    Code        The food's code, if it is already in your cache.
    Cal         Calorie value from the response (per 100 g).
    Protein (g) Protein value (g per 100 g).
    AAs         How many of the 11 tracked amino acids were found
                (e.g. 9/11 means 9 out of 11 were present).
    GI, DIAAS   Values from the reply, when you asked for them.
    What importing does
                New food, or which missing values will be filled in.

Check each row. If a value looks wrong, don't import: edit the pasted text (or paste a corrected reply) and click **Review** again. Otherwise click **Import … into cache**.

Foods that gain amino acid data change from — to ✓ in the Food Cache's [AA](#gloss-aa) column. Notes Claude added are saved as curator notes, under the food's "Notes ▸" link.


#### My Pantry {: #pantry-web}

*Search terms: foods on hand, staples, groceries, leftovers, batch cooking, meal prep, made ahead.*

The foods you keep at home. NuMa looks here first for [complement suggestions](#comp) and lists pantry foods first in searches. The list's columns are explained under [My Pantry Table](#pantry) below.

- **Add a food** with the search box at the top, which looks for *new* foods: pick a result and click **Add to pantry**. Your pantry and Food Cache matches show at once; online results follow a few seconds later, as on [Foods → Search](#food-search). Only adding a search result brings in the food's nutrient data.
- **Can't find it? Save just the name for now**, under the search box, saves a name only ([why](#pantry-name-only)); attach real data later with **Link a food**.
- **Filter my pantry list**, just above the search box, narrows the list you already have to items whose name or notes contain every word you type.
- **Remove from pantry** appears on a search result that's already in your pantry, and **Remove** on each row of the list.
- **Edit** on a row opens that food's Food Cache entry; **Archive/Restore** hides an entry without deleting it ([Archiving](#archive)).
- **Compare** checkboxes, on the list and on search results, send foods to [Comparison](#comparison) ([Picking from several searches](#compare-picks)). A name-only entry can't be compared.

**Recipes in your pantry.**{: #pantry-recipes} A batch you've made, such as a loaf of bread or a pot of soup, is food on hand too. Put a recipe in your pantry with **Add to pantry** on a search result here (the search finds your recipes as well as foods), the **In My Pantry** box on the recipe's page, or the **Pantry** column of the [Recipes list](#recipes-menu-web). It's listed under **Recipes on hand** on this page, and complement suggestions offer it under **From your pantry**. Your other recipes are still suggested, under **Other options**, as things you could make. When the batch is used up, click **Remove from pantry** or untick the box; the recipe itself is kept. An archived recipe isn't suggested.

##### My Pantry Table {: #pantry}

*Search terms: staples, groceries, kitchen cupboard, pantry columns.*

The foods you've marked as on hand. When NuMa suggests a food to fill an amino acid gap, it looks here first, and lists matches under "From your pantry". Recipes you've made are listed separately, under Recipes on hand ([Recipes in your pantry](#pantry-recipes)).

**Sort by**, above the list, orders it by **Most meals, last 90 days** (as in the Food Cache: the foods you actually eat first, with the count under Used in), Name, Code, Type, [DIAAS](#gloss-diaas), [GI](#gloss-gi) estimate, Used in (most-used first) or date Added, and remembers your choice. Columns:

<pre>
    Compare Tick to compare pantry foods side by side. Ticks are kept when
            you search again or go to another list (see Picking from
            several searches).
    Food    Food name.
    Code    The food's code (U171477, UD4, OFF3 ...); -- for name-only entries.
    AA      Amino acid data status.
              checkmark  AA data in your cache. This food can be used in
                         complement suggestions.
              X          No AA data. Click Edit to add it.
              --         Name-only entry: no USDA link, no nutrient data.
                         Use Link a food to attach real data.
    Notes   Your optional note for this pantry entry. Click it (or "add a
            note") to change it, then Save note.
    Added   When you added it.
    Type, GI est., DIAAS, Other nutrients, Used in   Same as the matching columns in the
            <a href="#cached">Food Cache</a> list — see the DIAAS entry there for
            how the saved-estimate-vs-reference-table value is chosen.
    An archived entry, shown when archived entries are visible, has an
    "Archived" badge after its name. See <a href="#archive">archiving</a>.
</pre>

Only pantry foods with [AA](#gloss-aa) data (✓) are used in complement suggestions, plus name-only and no-AA entries whose name matches NuMa's built-in complement table. Archived entries are never used.

**Why save just a name?**{: #pantry-name-only} It's a placeholder for a food you have when a search finds no good match, you're offline, or you'd rather choose the match later. It has no nutrient data, so it can't be analyzed or compared, and it isn't added to your [Food Cache](#gloss-food-cache) (its [AA](#gloss-aa) column shows "--"). **Link a food** later attaches a real match to the same row, without retyping, and caches it.


#### Custom food profiles {: #custom-foods}

*Search terms: homemade food, own food, create food, label data.*

Foods you enter yourself: a homemade dish, a supplement, or a product whose database entry is missing or incomplete. Start from scratch with **Create**, or use **Copy a cached food as a draft** and change only what differs. The copy searches have the usual [Source filter](#food-search) and reach your cache, [USDA](#gloss-usda) and Open Food Facts; a misspelling offers a ["Did you mean"](#search-suggestions) correction.

##### Creating a custom food profile

*Search terms: create food, homemade, nutrition label.*

Go to **Foods → Custom food profiles → Create** (or copy a cached food as a draft). The fields:

- **Name** — what to call this food in searches and meal logs.
- **Supplement mode** (see below) or a normal serving size and unit.
- **Basic macros** — calories, protein, total fat, carbohydrates, fiber, sugars, saturated fat, mono/poly fats, sodium. Fill these in first: calorie totals and protein quality depend on them.
- **Minerals, vitamins, amino acids, and [phytonutrients](#gloss-phytonutrients)** — all optional. Each box takes a plain number in the unit shown beside it, or a number with a unit that NuMa converts: `400 IU` ([IU](#gloss-iu)) for vitamins A, D and E, `12 mg`, `2.4 µg`, `1046 kJ` for calories. Amino acids can be typed one by one, or pasted as a table into **Paste an amino acid table** (g or mg per 100 g of food, g per 100 g of protein, or mg per g of protein — choose which, and NuMa converts). See [Data entry](#data-entry) for every form NuMa accepts.
- **Note** — document your source or any caveats about the data.

Once saved, the food appears in every search and works in meals and recipes like any other. Edit or delete it from the same page at any time.

**Portions (`p1`, `p2`, …).** The custom-profile form has no portions editor. A copied food keeps the original's portions ("1 cup", "1 slice"). To add, remove or change one, use the **Portions** action on the food's [Food Cache](#food-cache-web) entry, as for any food ([how](#ts-no-piece-portion)).

##### Dietary supplements — tablets, capsules, softgels {: #supplements}
<span id="supplement-mode"></span>
*Search terms: supplement, vitamin tablet, B12 tablet, capsule, softgel, from supplements, supplement mode.*

Supplement labels give amounts per tablet, not per 100 g. NuMa handles this with **supplement mode**: create a custom food profile as above, set the serving size to **1** with a unit of `tablet`, `capsule`, `softgel`, `pill`, `gummy`, `scoop` or similar, then enter the nutrient amounts exactly as printed on the label (`400 IU` — [IU](#gloss-iu) — and `25 mcg` both work). When you save, NuMa adds a "1 tablet" portion to the food and says so. Logging `1 tablet` in a meal then adds exactly those label amounts to your totals, and `2 tablets` twice them — no weighing involved, and no conversion math on your part.

**Tip:** try a barcode search first (the 12- or 13-digit number on the label, entered at any search prompt). Many supplement products are already in Open Food Facts[^3] with complete data, saving you the manual entry.

To convert an existing custom food to supplement mode, edit it and change the serving size to **1** with a unit of `tablet`, `capsule`, or similar, same as creating one from scratch.

**A supplement isn't treated as a food.** Saving in supplement mode also ticks **This is a supplement** on the food's page; you can tick or untick it there for any food. While it's ticked:

- **No food checks.** NuMa doesn't ask a supplement for calories, protein, amino acids, a [GI](#gloss-gi), [DIAAS](#gloss-diaas), portions or water. It never appears in Food data problems, the missing-data lists, a meal's calorie note or Top Contributors' no-data list, so there's nothing to mark "not needed".
- **Its nutrients count in full.** Every nutrient on its label counts toward your meal and day totals and your daily targets, and toward upper limits. High-dose vitamin D, zinc or iron tablets can take a day over its upper limit, and NuMa says so as for any food.
- **It weighs nothing.** A tablet adds nothing to a recipe's weight or its per-100 g figures, and stays out of glycemic load.
- **It reads per tablet.** The food's page shows its values for **1 tablet**, and adding it to a meal starts at `1 tablet`. A number on its own counts tablets: `2` means 2 tablets, not 2 grams. Meal, day and summary pages list it the same way — **2 capsules**, **0.5 tablet** — never in grams: inside NuMa one tablet is stored as "100 g" so the label's per-tablet figures can be used as they are, but that number isn't a weight, and a supplement counts as 0 g in every weight total.

**From supplements.** In every nutrient table for a meal, a day, the Daily Summary, a recipe and the nutrient averages, a nutrient that came partly or wholly from supplements shows how much, under its amount: *12 mcg from supplements*, or *all from supplements*. On a plant-based diet that matters most for B12: 250% of the target, all from a tablet, is a different picture from 250% from food.

**A supplement found by barcode** in Open Food Facts usually gives its figures per 100 g of tablets, not per tablet. Ticking **This is a supplement** on it still skips the food checks, but to log it by the tablet, copy it to a custom food and enter the label's per-tablet amounts; the food's page says so.


##### Custom Food Profiles List {: #drafted-foods}

*Search terms: custom foods list, my custom foods.*

The custom foods you've created: from a label, a research table, or a supplement.

Columns:

    Name    Food name as you entered it.
    Code    The food's code — UD followed by a number (UD4).
    Type    Where it came from ("User Drafted", or the source of a
            food you copied and edited).

Custom foods live in your [Food Cache](#gloss-food-cache) and appear in every food search. NuMa calls them "user-drafted", and their [codes](#gloss-code) start with UD (older versions showed "usr"; see [usr](#gloss-usr)).

To change a custom food's nutrients, open it from the Food Cache or this list and click **Edit nutrients**. You edit the food itself, not a copy.

**Comparing search results before you copy.** On the edit page, results of both searches ("Copy nutrient values from another food" and "Estimate amino acids from another food") have **Compare** checkboxes. Tick the ones to weigh up, from as many searches as you like (up to 7), and click **Compare checked foods with this one**. These ticks belong to this profile only. The button turns blue once one food is ticked. [Compare](#comparison) opens with your profile first and the ticked foods beside it, per 100 g; **← Back to editing …** returns you, with your ticks still in place, so you can untick one and compare again. **Clear all picks**, in the note under the button, unticks them all. Unsaved edits are saved first, as with a search, and the Undo offer waits for you when you come back.

**Estimating amino acids from another food.** Wherever NuMa asks for a food's amino acids (creating or copying a custom food, or editing any food's data), you can pick a similar food that has amino acid data instead of typing values. Its amino acids are **scaled to this food's protein content**, not copied as they are: a food with half the protein gets half the amino acids. A note naming the source food and the scale factor is offered for the Note field. On the custom-profile edit page this is the "Estimate amino acids from another food" panel. Editing any food this way marks it user-drafted, like any other edit.

**Asking Claude AI for help.**{: #edit-ask-ai} The edit page's third box, **Ask Claude AI for help**, is the last resort, for when neither search finds a usable food. Choose the whole nutrient profile or one nutrient group, and whether to ask only for the values the food is missing or for every value (to replace figures you doubt), then click **Write the prompt for Claude AI**. NuMa writes the prompt; you paste it into Claude and import its answer, reviewing it first. With **Every value**, the import page starts with **Also replace the values these foods already have** ticked. The steps are in [Workflow 12](#fix-food-data); how the prompt and import work, in [Fetching missing data with Claude AI](#fetch).

**A shortcut from search results:** every food row in [Food Search](#food-search), Food Cache and the Pantry's search has a **Copy as custom-food draft** button. It copies the food as an editable draft and opens its edit page, with the amino-acid source search ready.


#### Annotate {: #annotate-web}

*Search terms: GI estimate, DIAAS estimate, annotation, food notes.*

A list of your cached foods, where you record a glycemic index (GI) or [DIAAS](#gloss-diaas) estimate and a preparation note, or tell NuMa to stop asking for one. NuMa also opens a food's Annotate page by itself after you add a food that's missing them; **Skip for now** puts it off. The filter box offers ["Did you mean"](#search-suggestions) corrections.

##### The Annotate page, field by field {: #annotate}

*Search terms: add a glycemic index, enter protein quality, cooking note.*

Your own [GI](#gi) and [DIAAS](#gloss-diaas) estimates for a food, plus a short preparation note. Four ways in, all to the same page:

- **Foods -> Annotate a Food**, then filter by name and click **Edit** on the food you want.
- **The food's page**, or its [Edit Custom Profile](#drafted-foods) page: **Add or edit [GI](#gloss-gi) / DIAAS estimates** (you come back there when you save).
- **The GI or [DIAAS](#gloss-diaas) figure in a search result**, which is a link: click the value (or the dash) to edit it.
- **The prompt after adding a food** that's missing an estimate.

The list shows each food's Name, Type, **GI est.** and **DIAAS est.**, with a dash where there's none.

What you can set:

<pre>
    GI estimate      Glycemic index (0-100). See <a href="#gi">Glycemic Index</a>.
    GI source        Where the GI value came from. Filled in for you when
                     you pick a value from the lookup; type your own for a
                     value from anywhere else.
    DIAAS estimate   Your protein quality estimate (0.00-2.00). Useful for
                     packaged foods that lack amino acid data in USDA. See
                     <a href="#diaas">DIAAS</a>.
    DIAAS source     Where the DIAAS value came from.
    Prep context     A short preparation note (e.g. "boiled 20 min", "raw").
</pre>

**Note where each value came from.** A source is kept only with its value: clear the value and the source goes too. Both appear on the food's page after "Value taken from". Typing a different number over a value picked from the GI lookup clears the lookup's citation, since it no longer describes your number; a source you typed stays.

**Raw or cooked: pick the GI for the form you eat.** Cooking, baking and grinding change GI a lot: raw wheat flour in water tests around 20, bread made from it 70–90, and the lookup lists both. A yellow warning under the GI box says so; when the food's name says raw, dry, uncooked or flour, it adds that a raw-form GI makes the meals you cook from it look better than they are, so use the GI of what you make, or leave it blank. Recipes flag such ingredients too (*Ingredients that may not be eaten as listed*, under [Glycemic Index](#gi)).

**Looking up a GI value.** Open **Look up a GI value from the published reference table** and search by name. Click a result to take its value: the GI box fills in and **Save annotation** lights up (nothing is stored until you click it). How to choose between results is in [Choosing a GI value](#choosing-gi-values). If nothing is found, the page suggests what to try: plainer words, another name, a similar food, or glycemicindex.com.

**There's no lookup for DIAAS**, since few foods have published values. A note under the box explains how to estimate one from the food's main protein source, with [the DIAAS estimate table](#diaas-estimate-table).

**The two "don't prompt me again" boxes** are only for leaving a value blank on purpose. Saving an estimate already stops NuMa asking for it.

**If you don't record GI values at all**, say so once: tick **I do not record glycemic index data** at the foot of **Settings → Glycemic Index Reference Table**. NuMa then stops asking for GI values, the per-food GI box disappears, the GI field folds away on this page, and the notices about which GI table is in use stop. Nothing recorded is deleted: saved GI values are still shown and used for [glycemic load](#gl), and unticking it restores everything. DIAAS prompts continue, since that's a separate question.

**Saving settles the food.** Change anything on the page and **Save annotation** lights up (solid blue, red border). Saving tells NuMa you've dealt with this food: it stops asking when you add the food to a meal or the pantry, even if you left an estimate blank on purpose. **Skip for now** saves nothing, so NuMa asks again next time.

**When only one estimate is still wanted**, the page says which. The form always shows both fields, badged **Asking for this one** and **Settled — not being asked about**. The cursor starts in the GI box when GI is missing; when only DIAAS is, **DIAAS needed, click to go there** jumps down to it. Each estimate being asked for has a **Skip** button beside it: with both asked for, the GI **Skip** leaves GI blank and moves you to DIAAS; otherwise **Skip** works like **Skip for now**.

Your estimates are used wherever the food is: the Food Cache list, and food, recipe and meal analysis.


#### Checking your data {: #checking-your-data}

*Search terms: data checks, data quality, problems in data, find errors, since last time.*

Every result NuMa gives you is only as good as the food data underneath it. A food with no calorie value quietly adds nothing to every calorie total it's part of; a wrong cup weight is worse still: NuMa works out the food's density from it, and uses that density for *every* volume measure of the food — tablespoons, teaspoons, fluid ounces, any fraction or multiple of a cup — so every such amount you enter for that food, in any recipe or meal, comes out wrong. (Correcting the cup weight fixes amounts entered afterwards; those already entered are listed under [Amounts that no longer match](#stale-amounts).) NuMa checks your data in three places:

- **When data comes in.** Each food is checked the moment it's saved, by whatever route — a [USDA](#gloss-usda) fetch, Open Food Facts, a [CSV](#gloss-csv) or Claude [AI](#gloss-artificial-intelligence) import, or your own typing. Missing calories are filled in as an estimate, and right after you add a food with a problem to a meal or recipe, a note on that page says what's wrong with it.
- **Where you use data.** Food, meal, recipe and daily-summary pages flag what affects the figures you're looking at.
- **In one place, on demand.** **Foods → 9 (Database Integrity and Data Completeness Check)** lists every problem across all your data, grouped by kind of problem; its **Problems by food** button lists the same findings grouped by food (see [Problems by food](#problems-by-food) below). Its lists of foods start with the foods you eat most: those in the most meals over the last 90 days (on their own or in a recipe), with the count beside each name, so fixing the top of a list improves the most of your figures. **Order every list of foods**, at the top of the page, switches every list to alphabetical order and back, and NuMa remembers your choice. *Foods: days eaten* keeps its own ranking, by days eaten in the span you pick there, unless you choose alphabetical. The Home page tells you when new problems turn up (see [the reminder](#data-check-reminder) below).

##### Every check, and what to do about it {: #data-checks-list}

*Search terms: all checks, data check list, fix data.*

| Check | What it catches | Where you see it | What to do |
|---|---|---|---|
| [Broken references](#db-check) | A pantry entry, recipe ingredient or logged meal item pointing at a food or recipe that no longer exists; unreadable stored data | Foods → 9; a Home page banner | Use the fix button for each kind; read its note first, since each has a different effect |
| [Missing nutrient data](#data-completeness) | A food with no values at all for a whole nutrient group (macronutrients, minerals, vitamins, amino acids; omega fats and phytonutrients if you ask) | Foods → 9; the food's own page | Refresh it, ask Claude AI for just the gaps, or mark the gap "not needed" (a spice doesn't need macronutrients) |
| [Calories missing or not adding up](#calorie-checks) | No calorie value; calories far from what the food's protein, carbs and fat imply; calories estimated | Foods → 9; the food's page; a **Calories** note on meal, recipe and summary pages | Refresh from [USDA](#gloss-usda), fill in from another food, or edit the value; alcohol, sugar alcohols and very high fiber can explain a real gap |
| Impossible values | Negative values; more than 100 g of one nutrient per 100 g; protein, carbs and fat adding up to more than 100 g; more sugars than carbohydrate; more of the three fat types than total fat | Foods → 9; the food's page; right after adding it | Correct the value on the food; such data usually came wrong from its source |
| [Amounts that no longer match](#stale-amounts) | A recipe amount typed as a volume or portion ("1/3 c", "p1") whose stored grams differ from what it works out to today | Foods → 9 | Check the food's portions, then update the amounts there in one click |
| [Amounts converted with a generic density](#generic-density) | A volume amount ("2 T") for a food with no cup or spoon weight of its own, converted with a [generic](#gloss-generic) density for that kind of food | Recipe and meal pages ("≈ generic" mark), Foods → 9 | Measure the food's cup or spoon weight and add it on its Portions page, then correct the amounts |
| [Old USDA copies](#old-copies) | USDA foods not refreshed in over a year | Foods → 9 | **Refresh from USDA** shows what changed and lets you choose |
| [Missing amino acid data](#missing-aa) | Foods with protein but no amino acid figures, left out of protein quality ([DCP](#gloss-dcp), [DIAAS](#gloss-diaas)) | Foods → 9 (foods you use, most eaten first); meal, recipe and food pages; the [AA](#gloss-aa) column in search results, Food Cache and Pantry | Find a Foundation or [SR](#gloss-sr) Legacy version, refresh from USDA, or estimate from a similar food; or tick "not needed" |
| [Missing GI values](#missing-gi) | A food you use with carbohydrate (5 g or more per 100 g) but no [GI](#gloss-gi), so [glycemic load](#gl) is incomplete wherever it appears and it can't be suggested as a [lower-GI swap](#gl-swaps) | Foods → 9 (foods you use, most eaten first); any incomplete [GL](#gloss-gl) figure; Top Contributors ranked by glycemic load | Look one up on the food's Annotate page; or tick "not needed" (the same as "don't prompt me") |
| [Missing portion weights](#ts-no-volume-portion) | A food with no cup, spoon or piece weight, so a volume or count can't become grams | Foods → 9 (foods you use, most eaten first); recipe pages ("No portion/weight data exists"); when you type an amount | Add the weight once on the food's Portions page; or tick "not needed" if you always weigh it |
| [Duplicate foods](#duplicate-foods) | Two or more foods with the same name, so a fix to one doesn't reach what uses the other | Foods → 9 → **Find duplicate foods** (on request) | Compare them, keep one (the rest are replaced by it everywhere), or mark "not duplicates" |
| [Recipe weight unknown](#recipe-servings-grams) | A logged recipe whose serving weight can't be worked out; a recipe whose serving size changed after you logged it | Meal pages | Enter the recipe's total weight; review the meal as the page suggests |
| [Deleted sub-recipes](#ts-deleted-recipe) | A recipe ingredient or meal item pointing at a recipe that was deleted | Foods → 9; Edit Recipe (offers to relink) | Relink it or remove it |
| [Failed recalculations](#system-issues-howto) | A recipe or meal whose automatic recalculation broke after a change | Settings → 16; a red alert at the top of every page | **Retry** |
| [Import checks](#fetch) | Claude AI replies, [CSV](#gloss-csv) files and recipe imports: missing names, non-numbers, unknown nutrients; imports fill only empty values | The import page's "Notes from validation" | Fix the source and import again |
| [Estimates](#filling-gaps) | Where NuMa used an estimate (calories, amino acids, protein digestibility) instead of measured data | Labeled where the figure appears | Replace with real data where you can |

**Right after you add a food.** If a food you've just added to a meal or recipe has a problem from the table (not merely an estimate), the page says so at once, with a link to the food. That's the easiest moment to fix it.

**The Home page reminder.**{: #data-check-reminder} When new problems have turned up since you last opened Foods → 9, the Home page says how many, with a link. Opening Foods → 9 clears it until more new ones appear. Problems in NuMa's starter foods and recipes never set it off (they're still listed). **Settings → 14 (Data Quality Reminder)** turns it off, or asks for a reminder every so many weeks regardless. A monthly look is a good habit if you log most days.

**New since your last check.**{: #new-problems} The reminder's **Review them** link opens Foods → 9 at a box listing just the new problems, one per line: the food (or meal or recipe item), what's wrong, and a link to its place in the full lists below. Look here first: a cluster of new problems usually has one cause, such as a food you just added, a Refresh from USDA, or a recipe or portion you edited. The box stays as you work, even if you leave the page and come back; each problem you fix is crossed out and marked **fixed ✓**. Click **Done with these** to clear the box. Problems still open stay in their lists, and only problems that are newer still will bring the box back.

##### Problems by food {: #problems-by-food}

*Search terms: everything wrong with a food, all problems for one food, fix a food, food checklist, ignore a problem, dismiss, borrow, copy values.*

Foods → 9 lists by kind of problem, so a food with three things wrong turns up in three places on that page. **Problems by food** (the button at the top of Foods → 9) turns it around: one entry per food, with everything NuMa found on it and a button for each fix, so you can put a food right in one visit. Each item is tagged:

- **Problem**: gives wrong figures now (no calories, impossible values, a nutrient group with no data, amounts that no longer match, a wet food picked for a dry one).
- **Suggestion**: leaves a result incomplete or approximate (no amino acid data, no [GI](#gloss-gi), no portion weights, a [generic](#gloss-generic) density, a possible duplicate).
- **Note**: for information (calories estimated, a [USDA](#gloss-usda) copy over a year old).

**Borrowing values from another food.** A food with missing or wrong values has a **Borrow values from** box, filled in with its own name. Change it to the food to borrow from (*onions, raw* for a green onion) and click **Find it**. That opens [Fill in nutrients from another food](#review-incoming) with that search, where you compare and tick which values to copy, some or all, before anything is written.

Only foods with at least one problem are listed until you tick **Also list foods with only suggestions or notes**. Sort them by most problems, most used, or name. Anything you've marked "not needed" isn't listed, and most items carry buttons after **or stop flagging it:** to mark them so right there: a missing nutrient group (one button per group), **Macronutrients not needed** for a food with no calories (a spice, yeast; it also stops the calorie checks), **These calories are right**, **Amino acids not needed**, **Portions not needed** (you always weigh it), **GI not needed**, and **Not duplicates**. To undo one, use the food's own page (a nutrient group, under "Marked not needed for this food"; calories, with **Check them again**) or the matching list on Foods → 9 with its "also list … marked not needed" box ticked. Missing nutrient data covers the groups ticked under **Groups to check** on Foods → 9. Each item's **all foods** link opens the full list for that kind of problem on Foods → 9, where it can be marked "not needed".

The same list shows on each food's own page, as **Everything to check on this food**: open when the food has a problem, folded when there are only suggestions or notes. A one-click fix made there brings you back to the food.

##### Seeing what a fix changed {: #data-effects}

*Search terms: effect of a fix, what changed.*

Fixing data changes results, sometimes a lot: filling in a missing calorie value for almonds once took a day's total from 1,527 to 1,955 kcal. NuMa shows the effect three ways:

- **"What this change did."** After you refresh a food from [USDA](#gloss-usda), fill it in from another food, save a custom food, import Claude [AI](#gloss-artificial-intelligence)'s data, merge duplicates or update amounts on Foods → 9, the page lists each recipe (per serving) and logged meal whose calories, protein, carbohydrate or fat moved, before and after.
- **How much of a calorie total is measured.** The **Calories** note on a meal, recipe or daily summary starts with the share of calories from measured values, and names any food with no calorie value (its grams count as zero).
- **Past days change too, and say so.** A meal's totals come from its foods' data, so correcting a food updates every past day that used it. That makes your history more accurate, but a past day can then differ from what you saw at the time, so meal and Daily Summary pages say when and why they were recalculated ("Totals recalculated: 2026-10-03 (Nuts, almonds: its data changed)").

**Amounts that no longer match.**{: #stale-amounts} A volume or portion you type is turned into grams once, when you enter it ([why](#food-edit-consequences)). If the food's portions change later, or NuMa's conversion does, those grams stay. Foods → 9 lists each recipe and meal amount that would come out differently if typed today, with the grams stored and the grams it would be "Now", and a **portions** link for each food. Check the food's portions first: if a portion weight is wrong (a "tsp" that's really half a teaspoon), fix it on its Portions page and "Now" follows. Then tick amounts and choose:

- **Update the ticked amounts to their "Now" grams** — the amount you entered stays; its grams change. Updating a logged meal changes that past day's totals.
- **Keep the ticked amounts as entered** — the stored grams are right (you weighed it, say). NuMa rewrites the amount with your weight first, "8 c (2309 gr)" becoming "2309.2 g (8 c)", so it's never listed again.

Amounts typed with a weight ("42 g", "2 T 15 g") are never listed. A volume followed by a weight in brackets, like "1/3 c (42 gr)", is: older versions of NuMa added that weight themselves, but you may have weighed it, so check before updating. Updating drops the bracketed figure.

A food's **Portions page** shows the same list for that food after you add, change or remove a portion. There, recipe amounts start ticked; meals and bracketed weights start unticked. After reordering portions, amounts typed as `p1`, `p2`… point at a different portion, so re-enter those instead of updating them.

**Amounts converted with a generic density.**{: #generic-density} A volume ("1/3 c", "2 T") for a food with no cup or spoon weight of its own is converted with a [generic](#gloss-generic) density for that kind of food (protein powders, flours, seeds…). It's a reasonable guess, but a guess, so recipe, Edit Recipe and meal pages mark it **≈ generic\***. Click the mark to open the food's Portions page, weigh a level cup or spoonful, and add it; the mark goes, and the affected amounts appear under [Amounts that no longer match](#stale-amounts) to correct. Foods → 9 lists such foods, most eaten first. A bracketed weight ("2 T (14.7 gr)") counts too, since older versions wrote their generic conversion that way; a weight you typed ("15 g") never does.

**Foods you use with no amino acid data, or no portion weights.** Two folded lists on Foods → 9, showing only foods used in a recipe, meal or your pantry, most eaten first. In the amino acid list, **find amino acid data** searches for a similar food to copy amino acids from (scaled to this food's protein). Tick **not needed** for a food that doesn't matter (a sprinkle of cheese; a food you always weigh). Each list's Save button is at the bottom; a note above turns red and counts your changes once you tick something, and NuMa asks before you leave unsaved. Neither list raises the Home page reminder: these are improvements, not errors.

**Foods you use with no GI.**{: #missing-gi} A third folded list: foods you use with 5 g or more carbohydrate per 100 g and no [GI](#gloss-gi), most eaten first. Each leaves [glycemic load](#gl) incomplete wherever it appears, and can't be offered as a [lower-GI swap](#gl-swaps), so this list is also how to get better swap suggestions. **look up a GI** opens the food's Annotate page with the lookup ([how](#gi-source-para)); saving brings you back. Ticking **not needed** is the same as **don't prompt me** on the Annotate page: the food stops being listed, and a glycemic load that includes it says "marked don't prompt me". **Also list foods for which the GI is marked "not needed"** adds every food so marked, used or not (with "has GI" where one exists); untick **not needed** on any and save, and NuMa asks for its GI again. **Hide foods for which the GI is marked "not needed"** switches back, and NuMa remembers your choice. Save works as in the lists above.

**Foods: days eaten.**{: #days-eaten} A folded list for finding the gaps that matter most. Choose **Days to cover** and the date to go **back from** (default: 30 days to today), and click **Show foods eaten in these days**. Three tables follow, most days first:

- **All foods eaten** — each food, and on how many of those days, whether logged alone or inside a recipe. "(4 in a recipe)" means on 4 days it came only from a recipe.
- **Eaten with no GI** — foods with no [GI](#gloss-gi) that left a day's [glycemic load](#gl) incomplete, ranked by how many days. Work from this one if the [Nutrient Plot](#nutrient-plot) shows few [GL](#gloss-gl) points. A food eaten only by the pinch isn't listed (too little carbohydrate to count); one marked "don't prompt me" stays, since it still leaves days incomplete. Hidden if GI is turned off in Settings.
- **Eaten with no carbohydrate value** — foods with no carbohydrate figure at all, so they add nothing to carbohydrate or glycemic load. A supplement belongs here only until you mark its macronutrients "not needed" ([Missing nutrient data](#data-completeness)).

**Duplicate foods.**{: #duplicate-foods} Two copies of one food split your data: correct one, and whatever uses the other doesn't see it. **Find duplicate foods** on Foods → 9 lists foods whose names match once capitals, punctuation, a "\* " starter prefix, "Copy of" and "([FDC](#gloss-fdc) …)" are ignored (merely similar names aren't matched). Each group shows every copy's type, number of nutrient values, your edits and where it's used. **Compare nutrition** shows them side by side; **Keep this one** keeps the better copy (usually the fuller or the corrected one).

If the other copies have values the kept one lacks or differs on, or extra portions, the button reads **Keep this one, reviewing the others' values first**, and you choose, value by value (yours marked "(yours)"), before anything is deleted. NuMa preselects the sensible choice: blanks are filled, and your own edit on another copy wins unless the kept value is also yours. A copied value counts as your edit, so a later [Refresh from USDA](#review-incoming) asks before replacing it. Missing portions are ticked to be added.

Every recipe, meal and pantry entry using the other copies then switches to the kept one, keeping its own name and amount, and the others are deleted; "what this change did" shows how totals moved. Two pantry entries become one. If the foods really differ (raw and cooked), click **Not duplicates**; **Show groups marked "not duplicates"** brings them back. An unused copy has a **Delete** button (greyed out on a copy in use). A "\* " food is [starter data](#starter-data): keeping your own copy deletes the starter one.

**Foods in your pantry more than once** is the last list. Adding a food already in your pantry reuses the existing entry (restoring it if archived), and NuMa merges older doubles when it starts. Any left over are listed with **Merge into one**, which keeps the oldest entry and combines the notes.

**Old USDA copies.**{: #old-copies} USDA revises its records from time to time. Foods → 9 lists USDA foods you haven't fetched or refreshed in over a year. That isn't a problem in itself; **Refresh from USDA** on the food's page shows whether anything changed and lets you choose what to take.

**Vitamin K from USDA, corrected.**{: #vitamin-k-fix} Until 14 October 2026, NuMa took a USDA food's vitamin K from the wrong USDA figure (menaquinone-4, a form of K2 found mostly in meat and eggs) instead of phylloquinone (K1), the form in leafy greens and the one the daily goal is based on. So USDA foods saved before then show little or no vitamin K; raw spinach showed none. For those, the Home page shows a **VITAMIN K** note, and Foods → 9 has **Correct vitamin K for N USDA foods from USDA**. It fetches only each food's vitamin K, 20 at a time, and replaces or removes the old value; nothing else changes, a value you entered yourself is kept, and meals and recipes update to match. A food USDA has no record of (one you drafted under a USDA-style number, say) is left alone and named; one that couldn't be reached stays listed, so click again to retry. Foods from the other databases were never affected.


##### Integrity, missing data and calorie checks, in detail {: #foods9-detail}

*Search terms: database integrity, missing nutrients, orphaned records.*

**Broken references.**{: #db-check} The first check on Foods → 9 finds pantry entries, recipe ingredients and meal items that point at a food or recipe no longer in your [database](#gloss-database), left over from older versions or a hand-edited database file. (Opening such a food fails, because NuMa tries to fetch it again from USDA.) Problems are grouped by kind, most with their own fix button and a note on what it does, since the effects differ:

- **Pantry entries** — removing one only takes it off your pantry list.
- **Recipe ingredients** — removing one deletes that line; the recipe recalculates without it.
- **Logged meal items** — removing one deletes it from that day's meal, and the day recalculates as if it had never been logged. A deleted *recipe* can be [relinked](#relink-recipe) instead.
- **Sub-recipe references** — nothing is deleted; the ingredient is labeled "recipe (deleted)", as everywhere else.
- **Recipe ingredients naming a deleted recipe** — the line keeps the name but adds nothing to the totals. Not fixed automatically: [relink](#relink-recipe) it, or remove or replace the line.
- **Unreadable nutrient/portion data** — never repaired automatically; each food gets **Refresh** (fetch again from USDA) and **Delete**, so you decide.

**Missing nutrient data.**{: #data-completeness} This list shows foods with *no* values at all for a nutrient group: Macronutrients, Omega Fatty Acids, Minerals, Vitamins, Phytonutrients (the blocks of a Nutritional Analysis table) or Amino Acids. Macronutrients count as missing if any of calories, protein, carbohydrate or fat is absent; amino acids only for a food with protein. A group with *some* values is normal and isn't listed. **Groups to check** chooses which groups to look at; Omega Fatty Acids and Phytonutrients start unticked, since most food records were never measured for them.

**Not needed.** Not every gap matters: basil doesn't need macronutrients. Tick **not needed** under such a gap and click **Save "not needed" and "has none" choices**. NuMa stops listing and warning about it, and tells Claude [AI](#gloss-artificial-intelligence) it isn't needed in any prompt. **Mark column not needed** under a column's heading marks the whole column (click again, **Unmark column**, to clear). **Refresh list** checks every food again (asking first if you have unsaved choices). To undo one, open the food's page, where each group marked not needed has an **Undo** button, or tick **Also list foods whose only gaps are marked "not needed"**, untick it and save.

**When a food has none.**{: #data-completeness-has-none} Some gaps aren't missing data: meat has no phytonutrients, a vitamin pill no macronutrients, sugar no omega fats. Tick **has none (0)** and save; after you confirm, NuMa records 0 for that group's missing values (keeping any it has) and updates meals and recipes using the food, which then counts as 0 everywhere instead of being skipped. **Mark column has none** ticks a whole column. Amino acids have no such box, since a food with protein has amino acids. Use **has none** only when you know; otherwise **not needed** keeps the value honestly blank. To change a recorded 0, edit the food. For one nutrient rather than a group, see the no-data list under [Top Contributors](#contrib-no-data-answers).

**Asking Claude.** To fill real gaps, tick **ask AI** under each gap (or **all** under a column) and click **Build a Claude AI prompt for the gaps checked "ask AI"** ([how it works](#fetch)). A food's own page offers the same: a missing-macronutrients warning has **Ask Claude AI for the missing data** and **Macronutrients not needed for this food**, and other missing groups are named below it (with **Amino acids not needed for this food** when amino acids are missing).

**Calorie checks.**{: #calorie-checks} Protein and carbohydrate supply about 4 kcal per gram and fat about 9, so a food's protein, carbs and fat imply roughly what its calories should be. NuMa uses that two ways:

- **Missing calories are filled in** from protein, carbs and fat, and marked as an *estimate*, whenever a food has those three but no calories, however it arrived. A real figure from the source later replaces it; changing protein, carbs or fat updates it. A food missing one of the three can't be estimated until it gets it.
- **Calories that don't add up are flagged**, never changed, when they're more than about a quarter away from the estimate. The gap can be real (alcohol, sugar alcohols and very high fiber carry energy the 4-4-9 rule misses), but usually the data is wrong. If you know they're right, **These calories are right — stop flagging them** (on the food's page or in **Food data problems**) stops the check; **Check them again** restarts it.

**Turning the calorie check off for a food.**{: #calorie-check-off} For a supplement or a spice used by the pinch, calories don't matter. Open the food (click its name in a **Calories** note) and use the button it shows:

- **Macronutrients not needed for this food — stop flagging**, for a food with *no* calorie value (or no protein, carbs or fat): NuMa stops checking its calories, and it no longer counts toward "no calorie value" warnings. The one for supplements.
- **These calories are right — stop flagging them**, for calories NuMa doubts but you know are correct.

Each can be undone on the same page (**Undo**, or **Check them again**). Estimated calories need nothing turned off; that line is information, not a warning.

**Food data problems**, on Foods → 9, lists every food with either calorie problem or an [impossible value](#data-checks-list), and, for information, every food with estimated calories. Foods whose macronutrients are marked "not needed" aren't checked. Meals, recipes and daily summaries including such a food show a **Calories** note above their Nutritional Analysis table: the share of calories from measured values, then the foods concerned.

**Fixing a food data problem.**{: #data-problem-fixes} Each problem in the **Food data problems** list comes with whatever fix NuMa can offer, as a button under it. A button changes only the value it names, and only when you click it:

- **No calorie value** → **Fill in calories from protein, carbs and fat**, marked as an estimate.
- **Calories don't match protein, carbs and fat** → when the figures point to a likely cause, NuMa names it and offers that fix first:
    - about 4.2 times too high: *looks like kilojoules entered as calories*, → **Convert from kilojoules**;
    - right for one serving rather than 100 g: *looks like the calories for one serving*, → **Convert to per 100 g**.

    Otherwise, or as well, **Use the estimate**, which takes the 4-4-9 figure (marked as an estimate), and **These calories are right — stop flagging them**.
- **More than 100 g of one nutrient per 100 g** → **Divide by 1,000**, when that gives a sensible figure: usually milligrams entered as grams.
- **More sugars than carbohydrate** → **Set sugars to the carbohydrate figure** (sugars are part of carbohydrate).
- **More of the three fat types than total fat** → **Set total fat to the sum of its types**.
- **A negative value** → **Remove the negative value**.
- **Protein, carbs and fat adding up to over 100 g** → no button: NuMa can't tell which of the three is wrong.

Under each food's name are the ways to fix it by hand: **Refresh from USDA** (USDA foods), **Fill in from another food** (already searching for its name), and **Edit values** (your own custom foods).

**Every fix is recorded** on the food's page, under **Corrected on Foods → 9**: which value, from what, to what, why, and when. On a USDA or other outside food a corrected value counts as yours, so a later **Refresh from USDA** shows the source's figure beside it, unticked, instead of quietly restoring it. Recipes and meals using the food are recalculated at once.

#### Archived foods & recipes (Foods → 10) {: #archived-web}

*Search terms: archive, hidden foods, retired recipes, restore, unarchive, old foods.*

**Archiving** a food or recipe hides it from search, suggestions and the default lists without deleting it. That's useful for something you no longer eat. But every meal you already logged with it still counts in your daily totals and in your long-run nutrient averages. If an archived food is missing data (no vitamin values, say), those past days come out too low for those nutrients, and nothing reminds you, because Foods → 9's completeness checks look only at foods in current use.

**Foods → 10** (also **Recipes → 3**) lists only what you've archived, in two tables:

- **Archived foods**, with the same columns as the [Food Cache](#food-cache-web), including **Other nutrients** (*complete* or *incomplete*; point at *incomplete* to see what's missing) and **Used in** (how many recipes and logged meals use the food).
- **Archived recipes.** A recipe has no nutrient data of its own; its figures come from its ingredients. So its **Other nutrients** column checks every ingredient food, including those inside sub-recipes. Click *incomplete* to see which ingredients have gaps and what each is missing. An ingredient food that is no longer in the Food Cache, or a sub-recipe that was deleted, counts as a gap too, since it adds nothing to the recipe. **Used in** gives the number of logged meals (and the most recent date) and how many other recipes use it as a sub-recipe.

A summary line at the top counts the incomplete items and how many of them are in logged meals: those are the ones affecting your averages. By default both tables sort **incomplete first**, with the most-used first within each group (**Sort by** changes it; **Incomplete first** is on the Food Cache's list too). The filter box narrows both tables by name or code.

**Fixing a gap.** Tick foods in the first column and click **Fetch missing data from Claude AI**, as on the Food Cache (see [Fetching missing data](#fetch)), or open a food and refresh or edit it. For a recipe, fix its ingredient foods; the recipe and the meals using it are recalculated. If a group truly doesn't apply to a food, mark it *not needed* on the food's page, and the food then counts as complete. **Restore** returns an item to normal use (click again to re-archive it); neither changes any logged meal.

### D. A food's page, and every analysis page {: #analysis-pages}

*Search terms: results page, reading results, what the sections mean, output.*

A food's page, a recipe's page, a meal's page and a whole day's page all show the same kind of analysis, in collapsible sections. This chapter describes a food's own page first, then each analysis section and table in turn. Click a section's heading on the page to open it; the outline down the side of a long page jumps straight to each one.

The sections, roughly in the order a meal's page shows them:

- [Nutritional Analysis](#nutrients): every nutrient, against your daily targets, [color-coded](#color-coding).
- [Top Contributors](#top-contributors): which foods supply most of a nutrient, with [lower-glycemic swaps](#gl-swaps).
- Protein: the [Protein Quality](#protein-quality) table for a single food, or [Meal Protein Digestibility Analysis](#meal-diaas) and the [Amino Acid Ratios](#iaa-ratios) table for a recipe, meal or day.
- [Missing Amino Acid Profiles](#missing-aa): foods whose missing data weakens the protein figures.
- Complement suggestions: foods that would close a protein gap; see [Protein Complement Suggestions](#comp) for how they're chosen, and [Ignoring a complement suggestion](#ignore-complement).
- [Glycemic Load](#glycemic), with the [estimated GI](#mixture-gi) of a meal or recipe.
- Antinutrients: notes on phytate, oxalate and others where they matter; see [Antinutrients](#antinutrients).

#### A food's page {: #food-page}

*Search terms: food page, food details, nutrition facts, food analysis, my notes, personal notes, comments.*

A food's page shows, from the top:

- **Copy as new draft**, under the title: copies the food as a [custom food](#custom-foods) to edit.
- **Rename this food** ([below](#rename-food)).
- **Your changes to this food's original values**, a folded list, once you've changed a [USDA](#gloss-usda) or other outside food's data.
- **Notes**: your own notes on the food, any notes that came with it, and the preparation note from its Annotate page ([below](#food-notes)).
- Its [GI](#gloss-gi), if recorded, and [glycemic load](#glycemic), per 100 g and for the amount shown.
- **Protein Summary**, with its [DCP](#gloss-dcp).
- **Nutritional Analysis**: type an amount or pick a named portion, then click **Recalculate nutrients**.
- **Protein Quality**: [DIAAS](#diaas) and the table for each amino acid.
- **Anti-nutrients.**
- **Protein Complement Suggestions**: pantry foods first, then general suggestions, two-food combinations, DIAAS-boosting options and two-step combinations, each of which [can be ignored](#ignore-complement).
- **Add to Pantry**, at the bottom.

A food with no amino acid data suggests searching for a Foundation or [SR](#gloss-sr) Legacy version, the USDA datasets most likely to have it.

**Your notes on a food.**{: #food-notes} Any food can carry notes of your own: how it tastes, which brand you buy, how you cook it. On the food's page, under **Notes**, click **Add your own notes on this food**, type, and click **Save notes**. To change them later, edit the box and save again; to remove them, clear the box and save. Your notes show on the food's page, under **Notes ▸** in the [Food Cache](#cached), and on its printout.

- **They're kept when you refresh.** A food from USDA or another source may come with notes of its own, shown under **From the food's source**. **Refresh from USDA** replaces those, but never touches yours.
- **For a [custom food](#custom-foods),** the box holds the same notes as its **Edit values** page, since a food you made has no notes but yours.
- **Merging duplicates** ([Duplicate foods](#duplicate-foods)) keeps the notes of both foods.
- **A pantry entry has its own note,** separate from these: see [My Pantry](#pantry).

**Renaming a food.**{: #rename-food} **Rename this food**, under the name, works for any food, USDA ones included. Type the new name and click **Save the new name**; every recipe, meal and pantry line using the food shows it. A USDA food stays linked, so **Refresh from USDA** still works, and shows USDA's name beside yours, unticked, instead of putting it back.

#### Nutrient Analysis Table {: #nutrients}

*Search terms: nutrient table, nutrition facts, nutrients list.*

Shows the nutritional content of a food, recipe, or meal portion, grouped by category (Macronutrients, Water, Omega Fatty Acids, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients)).

Columns:

    Nutrient     Name of the nutrient.
    Amount       Value for the portion you entered.
    Unit         kcal for calories; g for macronutrients (protein, fat,
                 carbs, fiber, omega fatty acids); mg or mcg for minerals
                 and vitamins.

**Every nutrient NuMa tracks gets a row, and "0" and "no data" differ.** **0** means the source measured it and found none (for a recipe or meal: every ingredient reporting it has none). **no data** means it was never measured, so the amount is unknown, not zero. A meal or recipe shows a figure once any ingredient has one, so a total can be too low when others have no data; [Missing nutrient data](#data-completeness) lists the foods with whole groups missing. Small amounts keep their decimals (0.3 mg, 0.04 mcg) instead of rounding to a misleading 0.

With a profile set, the goal columns appear (**Minimum**, **Target**, **Maximum** — see [RDA](#rda) for what each means), and on a meal two percentage columns:

    meal %       This meal's contribution to your daily goal, in percent.
    day total %  All meals logged that day as a percentage of your daily goal.

#### Color coding (meal % and day total % columns) {: #color-coding}
    Green    Met — at or above a minimum, or within the comfortable range
             around a target (e.g. calories), or safely under a limit.
    Blue     Near — approaching a minimum from below, or drifting toward
             the edge of a target's comfortable range, or nearing a limit.
    Orange   Below minimum — well short of a floor-type nutrient (protein,
             most vitamins/minerals), where more is always fine.
    Red      Over the limit — past a Tolerable Upper Intake Level, or, for
             a target-type nutrient like calories, significantly over 100%.

A legend of the four colors appears under every table that uses them.

If you've set a [Revised Optimal target](#optimal) for a nutrient (Settings → 5), a higher goal based on recent research, the table adds **Revised Optimal goal** and matching percentage columns (**% of Revised Optimal**, or **Rev. Opt. meal %** and **Rev. Opt. day %** on a meal), with a dash for nutrients without one.

A nutrient with a custom [max limit](#maxlimits) is highlighted (orange, then red) once the day's total is within 10% of it.

[Phytonutrients](#gloss-phytonutrients) (carotenoids, choline, isoflavones…) appear only when the food's data includes them, which many don't. Amino acids are in the protein sections, not this table. How your goals are worked out: [Daily Nutrient Goals](#goals) and [RDA](#rda).


#### Top Contributors Table {: #top-contributors}

*Search terms: which foods supply, biggest sources, main sources, ranking foods.*

On meal and recipe pages, just above the Nutrient Analysis Table. Pick a nutrient under **Rank by** to see which foods supply most of it.

Columns:

<pre>
    Food / Recipe   Name of the contributing food, linked to its detail page.
                    On a meal's table, the header instead says "Food or
                    ingredient" — any recipe used in that meal is broken
                    into its individual foods for this table, so no row
                    ever names a whole recipe. (A recipe's own Top
                    Contributors table can legitimately show a sub-recipe
                    by name, so it keeps the "Food / Recipe" header.)
    Amount          This food's contribution, in the selected nutrient's unit.
    % of total      This food's share of the summed contribution across every
                    food in the meal or recipe (not a percent of any daily
                    target — see <a href="#nutrients">Nutrient Analysis Table</a> for that).
</pre>

**Show** limits the list to the top 5, 10 (the default), 15, 20 or 30, or all, offering only choices that would shorten it. The **Total, all contributors** row always counts every food.

**Recipes kept whole.**{: #contrib-by-item} On a meal with a recipe in it, a second table, **By meal item, recipes kept whole**, ranks the items as you logged them, each recipe as one row (the first table is then headed **By food, recipes split into their foods**). One answers "was it the dal or the tofu?", the other "was it the lentils or the spinach?". For **Protein**, a recipe's figure is its own [DCP](#gloss-dcp), its foods pooled as if it were the whole meal, so it can score more than its foods added up. For **Glycemic load**, it's the sum of its foods' (those with a [GI](#gloss-gi)).

A food that appears more than once in a meal (twice on its own, or also inside a recipe) is one row, with the amounts added. The same goes for a whole day.

**Ranking by Protein** uses each food's own [DCP](#gloss-dcp) (digestible complete protein), worked out as if that food were eaten alone, not raw protein grams. Because foods complement each other, the meal's real DCP (in Protein Summary) is usually higher than this table's total. Foods without amino acid data can't be scored and are left out.


**Ranking by Glycemic load (GI × carbs)** (under Macronutrients) ranks foods by [glycemic load](#gl): GI × carbohydrate grams ÷ 100, for the amount used, with each food's [GI](#gloss-gi) and grams. GL adds up, so the rows total the meal's or recipe's [GL](#gloss-gl). Foods inside sub-recipes are listed separately, since GI belongs to a food. Foods with carbohydrate but no GI are named underneath, each linked to its Annotate page to [look one up](#gi-source-para), with how much of the carbohydrate the ranking covers. **Which foods drive it, and lower-GI swaps to try**, under a Glycemic Load figure, opens this view.

**Foods with no data for the nutrient** can't be ranked and add nothing to the total. **Show the N foods with no data for …**, under the table, lists them, heaviest first, so you can see what the total may be missing. A stored 0 counts as data. For Protein (DCP), it lists foods with protein but no amino acid data; glycemic load already names its foods without GI. On a recipe, the list goes down to foods inside sub-recipes.

**Getting the missing data.**{: #contrib-find-data} **Find this data** (for DCP, **Find amino acid data**) beside a food opens **Fill in nutrients from another food**, already searching for the food's name in [USDA](#gloss-usda), the other databases and your Food Cache; pick a match and copy the values it lacks ([how](#review-incoming)). A custom food opens on its Edit page, which has the same search. **where to find it** opens the nutrient's entry in the [Full Nutrient Key](#nutrient-key), which says which sources to try ([the general order](#key-sources)).

**When the data doesn't exist, or doesn't matter.**{: #contrib-no-data-answers} Each food in the list also has two one-click answers. Both apply to the food everywhere, and bring you back:

- **Has none — record 0**, for a food that truly has none: no vitamin B12, [EPA](#gloss-epa) or [DHA](#gloss-dha) in a plant food, no lycopene in meat, no vitamin C in an oil. NuMa stores 0, the food leaves the list, and meals and recipes update. For Protein (DCP) it reads **Has no protein — record 0** and appears only for a food with no protein figure (a food with protein has amino acids: use **Find amino acid data**, which copies a similar food's, scaled, as an estimate). Use it only when you know: a wrong 0 makes the total too low without saying so. To change a 0, edit the food.
- **Not needed for this food** (for DCP, **Amino acids not needed**), for a gap too small to matter: the iodine in a pinch of spice, the water in a spoonful of oil. The value stays blank, but the food stops being listed and the nutrient is left out of [Claude AI prompts](#fetch). It covers that one nutrient only (a spice's missing iron still shows); a whole group marked not needed on Foods → 9 counts too.

Foods marked not needed move to a line under the table, each with **undo**; the food's page lists them under "No data, marked not needed for this food".

**Which to use:** calories never need either, since NuMa estimates them once protein, carbs and fat are known ([why](#calorie-checks)). Macronutrients, EPA/DHA, B12, vitamin D and carotenoids are often truly 0, so **Has none** fits when you know. Minerals, most vitamins, choline, beta-sitosterol and water rarely are: prefer **Find this data**, or **Not needed** for small amounts. Never record 0 water except for an oil, sugar or salt.

#### Lower-glycemic swaps {: #gl-swaps}

*Search terms: lower GI swaps, swap foods, alternatives, blood sugar swaps.*

When a meal's or recipe's [glycemic load](#gl) is Medium or High and you rank Top Contributors by glycemic load, NuMa suggests swaps for the one or two biggest contributors: foods in your Food Cache that

- have a [GI](#gloss-gi) at least 5 points lower (published values vary by a few points, so less isn't a real improvement);
- have similar carbohydrate per 100 g (within half again either way), so the same weight changes the *kind* of carbohydrate, not the amount;
- cut the [GL](#gloss-gl) by at least 0.5 for the amount used.

Foods sharing a word with the original come first (brown rice for white rice), then the biggest cut, each with its GI and the GL it would have at the same weight.

Whether barley belongs in your risotto is your call, so each suggestion has **see the full effect in What-if**, which opens [What-if](#whatif) with that replacement filled in, for this meal or recipe (on a meal, also **last 30 days**). There you see every nutrient before and after, and nothing changes unless you apply it ([Glycemic load in a what-if](#whatif-gl)).

Suggestions come only from foods with a [GI](#gloss-gi). A line under them says how many that is, and how many foods you use lack one, with a link to [that list](#missing-gi).

#### Protein Quality Table {: #protein-quality}

*Search terms: amino acid scores, essential amino acid table, protein score.*

How a food's amino acids compare with the [FAO](#gloss-fao) 2013 reference pattern. Shown below the nutrient table when the food has amino acid data.

Above the table:

  - **Digestibility** — the share of this food's protein your body absorbs (0.79 = 79%).
  - **DIAAS** — the lowest score in the table's "After digestion" column. 1.0 or more means every amino acid meets the reference per gram of protein eaten.
  - **Digestible protein** and **digestible complete protein** ([DCP](#gloss-dcp)), with what limits the DCP.
  - Whether the protein is Complete (every amino acid at or above the reference after digestion) or Incomplete, and which amino acid is most limiting.

Columns:

    Amino Acid       Name, using FAO pair notation where applicable
                     (Met+Cys, Phe+Tyr).
    In the food      Milligrams of this amino acid per gram of the food's
                     protein, divided by the FAO reference value. 1.0 =
                     exactly meets the reference.
    After digestion  The same, multiplied by the food's digestibility --
                     what you actually absorb per gram eaten. This is the
                     DIAAS way of scoring.
    Status           Met (1.0 or more after digestion) or Short. Whether
                     the protein counts as complete follows this column.

A food can meet every amino acid on paper and still be incomplete. Buckwheat's amino acids are all in proportion, but only 79% of its protein is absorbed, so per gram eaten, leucine and lysine fall short; a note under the table explains this. All the absorbed protein still counts as digestible complete protein: what limits the food is digestibility, not one amino acid.

Background: [DIAAS](#diaas), [limiting amino acids](#gap), [the FAO reference values](#fao).


#### Meal Protein Digestibility Analysis {: #meal-diaas}

*Search terms: digestibility table, per ingredient protein, absorbed protein.*

Step 1 of the meal [DIAAS](#gloss-diaas) calculation: how much protein from each ingredient is absorbed, before the [limiting amino acid](#gloss-limiting-amino-acid) is taken into account. Sorted by raw protein, highest first.

On meal and recipe pages the table also has a [DCP](#gloss-dcp) column. That's each food's raw protein times one score shared by the whole meal or recipe, not the food's own protein quality (for that, see [Top Contributors](#top-contributors)). So two foods with equal protein show the same DCP, whatever their amino acids.

A food logged more than once in a meal is one row, with the amounts added.

Columns:

<pre>
    Food            Ingredient name.
    Protein (g)     Raw (crude) protein from this ingredient, in grams.
    Digestibility   True ileal digestibility coefficient (0.00-1.00): the
                    fraction of protein absorbed by the small intestine. A
                    small "~est" or "user" tag next to the number (see below)
                    marks where the coefficient came from.
    Digestible (g)  Protein x Digestibility. What your body absorbs from
                    this ingredient, before the amino acid step.
    AA data         Amino acid data: checkmark = present, — = not available.
                    Ingredients without AA data are excluded from DIAAS.
    DCP (g)         Digestible complete protein from this ingredient — see
                    the note below the table for how this is calculated.
</pre>

#### Suffixes in the Digestibility column

*Search terms: suffix, estimated digestibility.*

<pre>
    ~est    Estimated from food category average; no measured value for
            this specific food.
    user    You set a custom value (Settings → 4. Protein Digestibility
            Overrides — see <a href="#dcp-overrides">Digestibility overrides</a>).
</pre>

Ingredients contributing less than 1 g of protein are omitted from this table as negligible; the totals row sums only the ingredients shown.

The "Total digestible protein" here is step 1; step 2, the limiting amino acid, reduces it further. The full method: [Limiting-amino-acid scoring](#aa-scoring); background: [DIAAS](#diaas) and [ileal digestibility](#gloss-ileal-digestibility).


#### Meal Amino Acid Ratios Table {: #iaa-ratios}

*Search terms: pooled ratios, meal amino acids.*

Step 2 of the meal [DIAAS](#gloss-diaas) calculation: the whole meal's pooled amino acids, each as a ratio to the [FAO](#gloss-fao) 2013 reference.

Columns:

    Amino Acid   Essential amino acid (FAO pair notation for Met+Cys and
                 Phe+Tyr).
    Ratio        Pooled digestible grams of this AA from all ingredients,
                 divided by (FAO reference value x total meal protein).
                 1.0 = exactly meets the reference. Below 1.0 = shortfall.
                 Above 1.0 = surplus.
    Status       Met (ratio 1.0 or above) or Gap.
    (bar)        Visual indicator, colored as below.

The amino acid with the lowest ratio is the [limiting amino acid](#gloss-limiting-amino-acid), marked "← limiting". The meal [DIAAS](#gloss-diaas) score equals that lowest ratio (capped at 1.0).

#### Color coding in the ratios table
    Green      1.0 or above (met).
    Dark red   0.80-0.99 (near).
    Red        Below 0.80 (gap).
    Gold       The limiting amino acid.

The panel below this table shows the final Digestible [Complete Protein](#gloss-complete-protein) figure: total meal protein x the [DIAAS](#gloss-diaas) score.

Background: [DIAAS](#diaas), [Limiting-amino-acid scoring](#aa-scoring), [Digestible Complete Protein](#dcp).


#### Bioavailability Table {: #bioavailability}

*Search terms: absorption, digestible protein.*

It takes two forms:

#### Single food (Protein Summary)

A food's page gives these under **Protein Summary**, at the top: its [DCP](#gloss-dcp) for the amount shown, whether it's complete (or which amino acid limits it), and how it was worked out (raw protein × digestibility = digestible protein → DCP). Without amino acid data, it says quality can't be analyzed. Details are in the [Protein Quality Table](#protein-quality); antinutrient notes are in **Anti-nutrients** ([Antinutrients](#antinutrients)).

#### Recipe per serving

A recipe's page uses the meal's per-ingredient table ([Meal Protein Digestibility Analysis](#meal-diaas)), for one serving, with total digestible protein and the [pooled DIAAS](#gloss-pooled-diaas) below it.


#### Glycemic Load Output {: #glycemic}

*Search terms: GL bands, GL figure.*

The estimated glycemic load ([GL](#gloss-gl)) of a food portion, meal, recipe or whole day.

The figure is rated against one of two scales. A food portion, meal or recipe uses the per-serving scale:

    Low       10 or below (low glycemic impact).
    Medium    11-19.
    High      20 or above.

A whole day (Daily Summary, the day's page, the day printout) uses the daily scale, since a day's total is several meals':

    Low       below 80.
    Moderate  80-120.
    High      above 120.

The daily bands are a convention, not a validated clinical target, and a day's GL rises with how much you eat; NuMa says so under the figure. More in [Glycemic Load](#gl).

**Where you see it:** a food's page, per 100 g and for the amount shown; a recipe's, per serving (or the servings you ask for); a meal's, for the meal; a day's, for the day.

**The day so far.** Under a meal's title, a line gives the day's GL up to and including this meal ("Glycemic load for 2026-10-13 up to and including this meal (2 of 3 meals): 30.6"), counting meals in the order you created them; a day's page gives the day so far. With a daily target set, it shows your share of it. "≥" means some foods lack a [GI](#gloss-gi), so the true figure is higher.

To hide glycemic load everywhere, untick **Show glycemic load** in Settings → 8. A recipe's GL is worked out fresh from its ingredients (and recipes inside it), so it follows any change at once.

**"at least 14.2 — incomplete, missing GI data"** means some foods have carbohydrate but no GI, so the figure counts only the rest, and the true one is higher. A line says how much carbohydrate it covers ("GL covers 72% of the carbohydrate here (28 of 39 g)"), and the foods left out are listed, with the reason:

- **no GI recorded yet** — with an **add a GI** link to that food's Annotate page.
- **no GI (marked "don't prompt me")** — you told NuMa not to ask, or turned GI off. It still can't be counted; **add one anyway** if you change your mind.
- **this food has no nutrient data** — NuMa can't tell how much carbohydrate it has.

A band (Low, Medium, High) is shown only for a complete figure, or for an incomplete one that's already High. If no food with carbohydrate has a GI, the output reads **Not available** and lists them.

**Foods with almost no carbohydrate don't need a GI.** Under 1 g of carbohydrate in the amount used (meat, eggs, oil, a pinch of spice) counts as zero, since its GL could be at most 1, so the salt doesn't make a recipe incomplete. [DCP](#gloss-dcp) has the same rule for under 1 g of protein.

[GL](#gloss-gl) = ([GI](#gloss-gi) x grams of available carbohydrate) / 100 per ingredient, summed across all ingredients in the meal.

**Which carbohydrate counts.** GI is measured on *available* carbohydrate, the part digested into glucose, so fiber is left out. [USDA](#gloss-usda), the Canadian database, Open Food Facts and your own foods (mostly from US labels) include fiber in carbohydrate, so NuMa subtracts it; the UK, Australian and French databases already leave it out. For beans with 60 g carbohydrate and 34 g fiber per 100 g, that's 26 g available. (A European Open Food Facts product already excludes fiber, which the label doesn't reveal, so NuMa's figure runs low for it by its fiber.)

Below the [GL](#gloss-gl) figure, a meal, recipe or day also gets an [estimated GI](#mixture-gi).

GL doesn't affect protein scores. Background: [Glycemic Load](#gl), [Glycemic Index](#gi).


#### Estimated GI of a meal or recipe {: #mixture-gi}

*Search terms: meal GI, recipe GI, mixed meal GI.*

A meal, recipe or whole day gets an estimated [GI](#gloss-gi), shown under the [GL](#gloss-gl): each food's GI, weighted by how much carbohydrate it brings:

    GI = sum of (food's GI x its carbohydrate) / total carbohydrate

So 40 g carbohydrate from sugar (GI 65) and 15 g from milk (GI 39) comes out at about 58. It's GL worked backward: 100 × GL ÷ carbohydrate. A single food's page shows the food's own GI.

The usual GI scale applies: Low 55 or under, Medium 56–69, High 70 or more. Within 5 of a boundary it says so ("Medium, close to Low"); the estimate can't tell 54 from 57.

**It's an estimate from the foods, not a measured blood-sugar response.** It's the standard method, and studies disagree on how well it works: one found table GI values predicted responses to mixed breakfasts[^91], another found no connection for meals differing a lot in fat and energy[^92], and a third found the calculation 22–50% higher than the measured GI[^94]. Fat, protein and fiber slow carbohydrate absorption, which the calculation can't see ([why](#gl)).

The estimate comes with these conditions:

- **Only foods with a GI count.** Otherwise the estimate describes the rest and says so ("GI of the 72% of carbohydrate with a GI value"). Unlike GL, it isn't a lower limit: the missing foods could move it either way.
- **Not given under 10 g of carbohydrate.** GI is measured with 25 or 50 g; with much less, one person's response to the same food varies a lot (about twice as much at 5 g as at 20 g in one study[^95]). So coffee with a teaspoon of sugar and some milk (about 5.5 g) gets a GL (about 3) but no GI, with the reason.
- **Ingredients that may not be eaten as listed.** A recipe ingredient whose name says raw, dry, uncooked or flour is flagged if its GI counts, since cooking, baking and grinding change GI (flour, water and yeast don't have the GI of bread). If its GI is for the form you eat, or it really is eaten that way (raw fruit in a smoothie), click **These ingredients are eaten as listed — stop flagging them** on the recipe's page (**Flag uncooked ingredients again** undoes it). This covers the recipe's own ingredients, not those of recipes inside it. A meal or day containing the recipe names the flagged ingredient, with a link. Name matching is rough: dried fruit is left out, and a dry food whose name doesn't say so isn't caught.
- **Values measured in people with diabetes** are named, as for GL ([GI populations](#gi-populations)).

A day's estimated GI is what research calls a *dietary GI*.


#### Missing Amino Acid Profiles {: #missing-aa}

*Search terms: missing amino acids, no AA data, excluded ingredients.*

*One of NuMa's data checks — see [Checking your data](#checking-your-data) for the rest.*

Ingredients without amino acid data can't be included in the [pooled DIAAS](#gloss-pooled-diaas), so this section lists them, separately for foods logged directly and foods inside a recipe.

    The meal's Refresh from USDA button fetches amino acid data for
    these where USDA has it. Otherwise, replace the food with a USDA
    Foundation or SR Legacy equivalent that has amino acid data.

    These must be fixed by editing that recipe (Recipes → the recipe →
    Edit) and replacing the problematic ingredient there.

It matters when the food is a real protein source, not when it's a garnish or spice. Foods with under 1 g of protein aren't listed (a footnote says when any were left off).

**Turning this check off for a food.**{: #missing-aa-off} For a food whose protein doesn't matter (a supplement, a seasoning blend), click **Amino acids not needed for this food — stop listing it** beside it here. For a food under 1 g of protein, which isn't listed, use its **not needed** box on Foods → 9 or the button on its own page. All three set the same mark, everywhere the food is used, inside recipes too: it leaves Foods → 9's no-amino-acid list and Claude AI prompts, and a line under this list counts the foods hidden. The food is still left out of DIAAS; the mark stops the warning, it doesn't supply data. Undo it on the food's page (**Undo** beside *Amino Acids*).

DIAAS is worked out from the ingredients that have [AA](#gloss-aa) data, flagged as an estimate, and the [DCP](#gloss-dcp) counts only their protein. See also [Meal Protein Digestibility Analysis](#meal-diaas).


#### Ignoring a complement suggestion {: #ignore-complement}

*Search terms: ignore suggestion, hide suggestion, exclude food.*

Every [complement suggestion](#comp) (a gap closer, a [DIAAS](#gloss-diaas)-boosting option, or a food in a two-food combination) has an **Ignore this suggestion in recalculation** box. Tick one or more and click **Recalculate complements**: the page reloads with those foods left out, and every tier is rebuilt from what's left. Use it for a food you can't or won't eat, to see the next best.

Ignoring more later adds to the list. **Ignoring N suggestions — manage** lists the ignored foods, each with **Remove ignore**; **Clear all** removes them all.

The list isn't saved: it resets when you leave or reload the page. Available on food, meal and recipe pages.


### E. The Recipes menu {: #recipes-menu-web}

*Search terms: recipe list, edit recipe, copy recipe, archive recipe.*

The **Recipes** page lists every recipe; its columns are explained in the [Recipes List Table](#recipes) below. Each row has **Edit**, **Copy**, **Archive/Restore** and **Delete**, and a **Compare** checkbox ([Compare selected](#compare-checkboxes)). A recipe used in a meal or another recipe can't be deleted, only archived ([why](#delete-recipe-elsewhere)).

Changing a recipe's ingredients or servings recalculates its [DCP](#gloss-dcp), and that of every recipe using it ([how](#recipe-dcp-cascade)). **Recompute [DCP](#gloss-dcp) for all recipes** is only needed after a bulk import, or if you suspect old figures.

- **New recipe** — a short form (name, description, servings, total yield) that opens the recipe for editing.
- **Edit** — the recipe's details, with one **Save recipe details** button, and its ingredients. Details include an **Introduction** (where the recipe came from, why you like it, serving notes) and, below Instructions, **Notes and documentation** (sources, substitutions tried, changes for next time), which print at the bottom of the recipe's analysis and go into its [CSV](#gloss-csv) export and [AI](#gloss-artificial-intelligence) translation. Add an ingredient by searching (the [usual results table](#food-search)) and typing an amount (`150 g`, `1/2 cup`, `p1`). NuMa saves it as grams at that moment, so later changes to the food's portions don't alter it ([why](#food-edit-consequences)). Reorder ingredients with the arrows, or edit or remove one in place. A **Running totals** card shows calories, protein and DCP for the whole recipe and per serving as you go.
- **Detail** — like a food's page: Introduction, Protein Summary, Ingredients, Instructions, Nutritional Analysis, [Complete Protein Analysis](#meal-diaas) per ingredient, Missing [AA](#gloss-aa) Profiles, Complement Suggestions, [Glycemic Load](#glycemic) and Anti-nutrients, with a servings box to analyze a different batch size.
- **Print/save recipe** opens a print-friendly version (**Back to recipe** returns). Tick what to include (Introduction is one choice), and choose **Print layout** (Full sheet, or Half sheet, which is more compact) and **Paper size** (US Letter or A4, for your browser's Print / Save as [PDF](#gloss-pdf)); both choices are remembered. Food, meal and day pages have the same printable version.

#### Recipes List Table {: #recipes}

*Search terms: recipe list, recipes table, recipe columns, beverage, finished recipe.*

All your recipes, sorted by Last accessed unless you choose Name or [DCP](#gloss-dcp)/serving (not while filtering); your choice is remembered.

Columns:

    Compare     Tick to compare recipes side by side (see Compare selected).
                Ticks are kept when you search again or go to another list
                (see Picking from several searches).
    Code        The recipe's code (R21). Press Alt+Shift+G, type 21, and
                press Enter to open it (see Opening a recipe or meal by its ID).
    Name        Recipe name; click it to open the recipe.
    Description Short recipe description, if any.
    Servings    Number of servings (1 or more; fractions allowed).
    DCP/srv     Digestible complete protein per serving (g). Recomputed and
                saved automatically whenever the recipe or its ingredients
                change — no separate analysis step is needed. Shown as
                NC (not computed) if no ingredient has a
                known weight, or an ingredient with 1 g or more of protein
                has no amino acid data. Minor contributors missing amino
                acid data (under 1 g of protein — spices, oil, salt, a
                trace of chocolate) don't block the calculation — only
                significant ones do, since an approximate DCP is never
                saved as if it were exact. The 1 g floor is absolute: it
                doesn't matter what fraction of the recipe's total protein
                that 1 g represents. The "Recompute DCP for all recipes"
                button above the table recomputes every recipe at once.
    Complete    Ticked if you have marked the recipe finished. Tick or
                untick it right here; it's saved at once.
    Pantry      Ticked if a batch is made and on hand: the recipe is in
                My Pantry, and complement suggestions offer it as something
                you have (see Recipes in your pantry). Tick or untick it
                right here; it's saved at once.
    Drink       Ticked if the recipe is a drink: its water counts as
                water from drinks in your totals (see Water). Tick or
                untick it right here; it's saved at once, and the recipes
                and meals that use it are updated. Not shown when water
                tracking is turned off in Settings.
    Created     Date the recipe was first saved.

A filter box narrows the list by name (a misspelling offers a ["Did you mean"](#search-suggestions) correction). **Show archived recipes** shows archived ones, greyed, with an "Archived" badge ([Archiving](#archive)). Meals and recipes still naming a deleted recipe are listed on [Foods → 9](#db-check).



#### Recipe Ingredient List {: #recipe-ingredients}
A recipe's ingredients, on its page and on Edit Recipe.

Columns:

    #       Row number. On Edit Recipe, each row also has up/down, Edit
            and Remove controls.
    Amount  Portion entered: e.g. "175 g", "14.7 g (2 T)", "2 servings".
    Food    Ingredient name, followed by its code (U171477, UD4, R21 for
            an ingredient that is itself a saved recipe, and so on —
            see code in the Glossary).
    Notes   Your note for that ingredient, if any.

A recipe used as an ingredient (code starting with R) is scaled from its servings and total weight. Its amount is always a number of servings, never `pN` ([why](#portions-vs-servings)).

**Unsaved details and adding an ingredient.** The details fields save separately from the ingredients. If you've changed one without saving and then add an ingredient, NuMa warns you: **Continue** saves the details and adds the ingredient; **Cancel** lets you finish the details first.

**Adding a recipe as an ingredient, by servings or grams.**{: #subrecipe-amount} A recipe in the ingredient search can be added like a food: type servings, or switch the box beside the amount to **grams**, and NuMa converts using the recipe's serving weight ("1 serving = 1 cup, 240 g"). Grams are offered only when NuMa knows that weight (a total weight was entered, or every ingredient has a weight). It's saved as servings either way.


#### Seeing what an ingredient change does {: #recipe-edit-effects}

*Search terms: ingredient change effect, swap an ingredient, substitute ingredient, recipe development, before and after, nutrient change report, recipe-edit-effects-data.md.*

While you work on a recipe, NuMa can tell you how a change moved its nutrients. Nothing happens unless you ask.

1. Open the recipe's **Edit** page (or start a new recipe).
2. Add an ingredient, remove one, or change an ingredient's amount with its **Edit** button.
3. A small box appears in the bottom right corner, naming the change and asking **Report the effect on nutrients?** The answer is **No** unless you say otherwise: press **Esc**, click **No (Esc)**, or just carry on, and the box goes away. Esc also closes the box at any later step.
4. Click **Yes…** and tick the groups of nutrients you want: the same groups as in a food's, meal's or recipe's nutrient table (Macronutrients, Minerals, Vitamins and so on). Or tick one of the two "all" choices: **All nutrients**, or **All nutrients that changed by 5% or more**, which leaves out everything that barely moved. Then click **Write report**.

Each report numbers the changes it covers and shows a table for each group, per serving: **Before** (the recipe before change 1), then the recipe after each change (**After 1**, **After 2** and so on, or just **After** for a single change), then **Change** and **Change %**, the whole effect from Before to the last After. A **?** means a figure can't be worked out at that point. Protein (DCP) is always listed under Protein, even when it can't be worked out at all. Protein (DCP), the protein your body can actually use, follows Protein, and glycemic load (how much a serving is likely to raise blood sugar) ends the Macronutrients table when you track it.

**A report covers every change since the last one.** To swap one ingredient for another, remove the old one (answer **No**), then add the new one and answer **Yes**: the report compares the recipe with how it was before the removal, so it shows the whole swap. The first report of a session covers everything since you opened the Edit page.

**Your choice of nutrients is remembered** and ticked for you at the next offer, until you change it or the session ends.

**Reading the reports.** Once a report is written, the corner box says so: **Show the report** opens it right away. After the first report, a **Show ingredient change(s) file content** button sits above **Add Ingredient** for as long as the page is open. It shows every report from this session, newest last; the button, now **Hide ingredient change(s) file content**, moves below the last report.

**The file.** Reports go into a file named `recipe-edit-effects-data.md`, so you can read them after you close the page. Run from the program's own folder, NuMa keeps the file there. The downloadable NuMa keeps it in its data folder, beside its database; the Show button gives the full location. The file holds one session: the first report of the next session replaces it.

**What counts as a session.** A session starts each time you open the Edit page from another page (the recipe's own page, the Recipes list, a new recipe and so on). Adding, removing, searching and saving the recipe's details all happen on the Edit page itself, so they keep the same session.

**Looking up a food without leaving.** On the Edit page, clicking a food's or a recipe's name in **Ingredients** or in the search results opens its full page in a panel over the Edit page. Close the panel (**Close**, or the Esc key) and you are back exactly where you were, with any search results, unsaved details and an open report box still there. **Open as its own page** leaves the Edit page for that page instead.

#### Deleting a recipe that's used elsewhere {: #delete-recipe-elsewhere}

*Search terms: remove recipe, recipe in use, can't delete, broken recipe references, relink, reconnect.*

A recipe logged in a meal, or used inside another recipe, can't be deleted. **Delete** (on the list or the recipe's page) says how many meals it's in, between which dates, and which recipes use it, and offers **Archive** instead: the recipe leaves lists and searches but keeps working where it's used, and can be restored any time. A recipe nothing uses is deleted after you confirm. Removing it from every meal and recipe makes it deletable.

<span id="relink-recipe"></span>**Meals and recipes that still name a deleted recipe.** Older versions allowed deleting a recipe in use. Such a line shows the name flagged "recipe (deleted)" and counts no nutrients; [Foods → 9](#db-check) lists them. To reconnect them, create a recipe with the same name, or sharing at least two words with it ("Chicken Noodle Stew" for "Beef Noodle Stew"): its edit page offers to relink those lines to it, or to another recipe you pick, one deleted recipe at a time.

#### Import CSV (Recipes → 2) {: #recipe-import-web}

*Search terms: import recipe, recipe file, share recipe, recipe from another computer.*

Brings in a recipe exported from this or another NuMa install, with every ingredient's data and any recipes inside it. See [Moving recipes with CSV files](#csv-recipes).

### F. Compare {: #compare-web}

*Search terms: compare foods, comparison, which is better.*

Puts up to eight foods and recipes side by side. Pick them with checkboxes in search results here or on other pages ([Picking from several searches](#compare-picks)), set an amount for each if you like, and save the comparison under a name to reopen, rename or delete later. The page is described in [Comparison Tables](#comparison).

#### Comparison Tables {: #comparison}

*Search terms: versus, vs, difference between foods.*

Up to eight foods and recipes, in up to four tables: ingredients, protein quality, glycemic values and nutrients. Everything is per 100 g of each item unless you set amounts, since a food's grams and a recipe's servings can't otherwise be compared. **Clear the list and start over**, beside Search, empties the list (saved lists are untouched). A **Contents** list down the side jumps to each part.

**Gathering items from several searches.**{: #comparison-gather} Search, tick, then search for the next item: what you ticked is added before the new search runs (**Add selected to comparison** adds without searching). Items ticked on other pages and not yet compared are listed under that button and go in with it. Everything added is listed under the search, each with **Remove**.

**Setting an amount for each item.**{: #comparison-amounts} Each item has an **Amount** box: grams for a food, servings for a recipe. A recipe with a known serving weight also offers **servings / g** and shows "1 serving = … g" (with its serving description, such as "1 muffin (85 g)", which also appears in the nutrient table); its column then reads "100 g (0.97 servings)", say. A food with portions offers **g / portion**, reading "2 × 1 slice (56 g)". Click **Show comparison at the amounts set above** (or press Enter); the blue Show button is always the one matching what you've asked for. **Compare amounts** then switches to **The amount I set for each item**. A blank box means 100 g of a food or 1 serving of a recipe. Amounts stay as you add or remove items, are saved with the list, and are kept if you switch back to per 100 g.

**Comparing recipes as written.**{: #comparison-basis} Per 100 g shows how concentrated each item is, but can mislead: add a little salsa to a recipe and the other ingredients seem to shrink, each now a smaller share of 100 g. With a recipe in the comparison, **Compare amounts** offers two more views (besides [your own amounts](#comparison-amounts)):

- **Per serving of each recipe, as written** — one serving of each recipe: its own ingredient amounts divided by its servings, and the nutrients of that serving.
- **Each whole recipe, as written** — every ingredient exactly as entered in the recipe, with the measure you typed (⅓ c, 2 T) beside its grams, and the whole recipe's nutrients.

Each recipe's column heading says which amount it shows ("1 serving (140 g)"). A plain food stays per 100 g. NuMa remembers your choice. These views aren't scaled by weight, so "(estimate)" doesn't apply to them.

**How a recipe's 100 g figure is worked out.**{: #comparison-estimate} A food's per-100 g figures come from its data. For a recipe, NuMa scales its total nutrients (and each ingredient's amount) by 100 ÷ the recipe's weight, the same weight a meal uses:

- **Its own total weight**, if entered: the finished dish, allowing for cooking losses. A stew cooked down from 1,300 g of ingredients to 1,000 g is compared per 100 g of the 1,000 g, so its ingredients add up to more than 100 g in the ingredient table.
- **Otherwise, its ingredients added up**: each food's grams, plus each sub-recipe's weight per serving × servings used (worked out the same way, however deep).

(Before October 18, 2026, Compare always added up the ingredients, so recipes with a stated weight could differ slightly from a meal.)

If a recipe has no total weight and an ingredient's weight is unknown (a blank amount, a deleted sub-recipe, a sub-recipe without servings), that ingredient is left out of the sum. The weight is then too small, so the per-100 g figures run *high*, and the recipe's name is marked "(estimate)" everywhere in the tables.

The **ingredient table** has a row per ingredient (with its code) and a column per item: how much goes into 100 g of the finished item ("--" if unused or unknown). A food is its own single ingredient, "100 g". Ingredients shared by two or more items come first, highlighted: usually the interesting question is how recipes differ. A sub-recipe shows its servings, not its own ingredients.

The **protein-quality table** appears when at least one item has enough amino acid data: [DIAAS](#gloss-diaas), raw protein, [DCP](#gloss-dcp), DCP as % of raw protein, and the limiting amino acid, per 100 g, the highest per row highlighted.

The **glycemic table**{: #compare-gl} appears when an item has a [GI](#gloss-gi) or [GL](#gloss-gl): each food's GI (a recipe shows —) and each item's [glycemic load](#gl) per 100 g, counting foods with a GI. The **lowest** is highlighted. A figure missing some GI reads "≥" with its carbohydrate coverage, and isn't highlighted. **†** marks a GI [measured in people with diabetes](#gi-impaired). For a real portion, see the meal or recipe page.

The **nutrient table**{: #compare-nutrients} covers every nutrient a food's analysis shows, plus amino acids, per 100 g, the highest per row in green, sortable by ticked nutrients. A nutrient no item has data for gets no row, and a yellow box above names those left out. The item list above shows an **[AA](#gloss-aa)** column (✓ or ✗).

**Print comparison table** prints just the table; **Download [CSV](#gloss-csv)** gives a spreadsheet file, a row per nutrient and a column per item.

**Saving a comparison list.**{: #comparison-saved-lists} **Save this list**, at the bottom, names and stores the current items. **Use a saved list**, at the top (even on an empty page), reloads, renames or deletes saved lists.


### G. The Meals & Log menu {: #meals-menu-web}

*Search terms: food log, food diary, logging meals, meal list, journal.*

The **Meals & Log** page:

- **New Meal** (name and date) creates a meal and opens it.
- The [list of meals](#meals-list): completeness, items, Meal DCP, Day DCP (all meals that date), % of your daily goal, calories, [glycemic load](#glycemic) if you track it, and any nutrient columns chosen in [Settings → 11](#meal-columns). Filters set the date and sort order.
- **Search meal history** finds every meal that contains, or doesn't contain, a food or recipe, by name or [ID](#gloss-id) ([Meal History Tables](#meal-history)).
- **Calculate** works out DCP and calories for all meals, or the last 10 or 30 days.

**A meal's page.** Add foods or recipes with the search box at the top (a recipe can be logged whole or as its separate ingredients). Edit or remove items in place; a food's amount is saved as grams when you enter it, so later changes to its portions don't alter it ([why](#food-edit-consequences)). You can mark the meal complete or incomplete, rename it, change its date, or merge it with other meals that day. Below the items come the [analysis sections](#analysis-pages): [Nutritional Analysis](#nutrients), [Meal-Level Protein Analysis](#meal-diaas) (with **Refresh from [USDA](#gloss-usda)** if amino acid data needs updating), Missing [AA](#gloss-aa) Profiles, Complement Suggestions, [Glycemic Load](#glycemic) and Anti-nutrients.

<span id="full-day"></span>**Analyze full day**, on any meal when its date has more than one, pools all that day's meals into one analysis, with the same sections as a meal's page. It's also the page the Daily Summary opens for a date (only the breadcrumb differs). The line under the title sums up the day's protein: number of meals, the day's [DCP](#gloss-dcp), its share of your DCP goal, and its share of the day's raw protein. A meal's page has the same line for the meal, so you can see how much of the day's goal it covers.

#### Meals and Log List {: #meals-list}

*Search terms: meals list, meal list columns, sort meals.*

Your recent meals, newest first, 9 at a time unless you change **Number shown**. **Show meals on or before** sets a cutoff date. Sort by Date, Name, Meal [DCP](#gloss-dcp), Calories or Glycemic load ([GL](#gloss-gl)); your choice is remembered.

Columns:

    ID              The meal's number. Press Alt+Shift+G, type it, and press
                    Enter to open the meal (see Opening a recipe or meal by its ID).
    Meal            Name you gave the meal (e.g. Breakfast, Lunch).
    Date            Date of the meal (YYYY-MM-DD).
    Complete        A checkbox, ticked when the meal is finished. Tick or
                    untick it right here to change it; it saves at once and
                    the list refreshes, so Day DCP's * updates. (Same flag as
                    the meal page's Mark complete / Mark incomplete button.)
    Items           Number of foods and recipes logged in this meal.
    Meal DCP        Digestible complete protein for this meal alone (g).
    Day DCP         The day's DCP, pooled across all its meals (as on the
                    day's own page) — or, until that has been worked out,
                    the sum of the meals' DCP figures. Includes meals not yet
                    marked complete, since DCP is auto-saved as you add items. If any contributing
                    meal isn't marked complete, the total is flagged with
                    an asterisk (*) as provisional, since it may still
                    change. Shown on the topmost row for each date only.
    % of goal (min) Day DCP as a percentage of that date's protein target.
                    Also flagged with * when provisional. Shown on the
                    topmost row for each date only.
    Calories        Calories for this meal alone, with its share of the
                    day's calorie goal in parentheses underneath.
    GL              Glycemic load of the whole meal, with its band (Low,
                    Medium, High, on the per-serving scale) underneath.
                    "≥ 9.1" over "49% with GI" means some foods in the
                    meal have carbohydrate but no GI value, so the true
                    figure is higher; the % is the share of the meal's
                    carbohydrate that does have one. "no GI" means none of
                    them has one. Hidden if you've turned GI off in Settings.
    Profile         Which profile the day is pinned to — shown only if you
                    have more than one (see Per-Day Profile Tracking).

Up to 6 nutrient columns of your own can be added ([Meals & Log columns](#meal-columns)). Under each meal's figure, "(23%)" is its share of the day's goal for that nutrient; figures aren't colored, since one meal is only part of a day. A nutrient with no daily goal (sugar) shows the figure alone. Under each date, a **current profile** switch scores the day against your profile as it is now ([Per-Day Profile Tracking](#day-profile)).

[DCP](#gloss-dcp) and Calories show -- until worked out; opening a meal saves them. % of goal needs a profile (Settings → 1).

    --    Not yet computed. Use the "Calculate DCP and calories for" dropdown
          and Calculate button to compute for all meals and days, the last 30
          days, or the last 10 days (results are saved permanently).
    n/a   Computed but no amino acid data (DCP) or nutrient data (calories)
          was available.

GL is worked out fresh each time, so it's never out of date. Sorting by GL puts the highest first (an incomplete figure sorts by its counted part; meals with none come last). See [Glycemic Load Output](#glycemic).

Click a meal to open, edit or delete it.



#### Meals & Log Columns {: #meal-columns}

*Search terms: meal columns, choose columns, nutrient columns.*

Besides its fixed columns, the Meals & Log list shows nutrients you choose, such as sodium, fiber, vitamin D or an amino acid.

Choose them in **Settings → 11. Meals & Log columns**: give each nutrient a position (1 = leftmost), leave others blank, and click **Save Meals & Log columns**. Until you choose, they're Protein, Calories, Carbohydrate, Fiber and Sugars; **Restore default columns** puts those back.

Protein here is raw protein; [DCP](#gloss-dcp) always has fixed columns of its own.

These values are saved along with DCP and calories, so they show -- until worked out (**Calculate**, or open the meal), and n/a if the ingredients have no data for that nutrient.

The same columns appear on the Daily Summary's Recent Days table, added up per day. Recent Days always shows raw Protein first (Day DCP is the digestibility-adjusted figure); it isn't one of your choices and can't be turned off, and isn't repeated if you also chose Protein.


#### Meal Items Table {: #meal-detail}

*Search terms: foods in a meal, edit meal, comment, memo, timestamp, clock, when eaten, view, ingredients, break down, recipes whole, mistake, wrong amount, take back.*

Shows the foods and recipes logged in a single meal.

Columns:

    Time      Time of day (HH:MM, from your computer's clock) the item
              was entered into the meal. Items logged before NuMa began
              recording this show a dash.
    Food /    Name of the food or recipe, linked to its own analysis page.
    Recipe    Each shows its source-database ID tag; a deleted-but-still-
              referenced recipe is flagged "(recipe deleted)".
    Amount    Portion recorded: grams for foods, or serving count for
              recipes. Volume unit labels are shown where applicable.
    Notes     Any note saved with this item, if present.

**Edit** on a row changes the amount and notes in a pop-up (click **Save changes**); **✕** removes the item at once. Add items with the "Add Food or Recipe" search above.

<span id="meal-undo-add"></span>
**Fix or undo an addition.** Right after you add something, the green **Added …** line above the search results has **Edit** and **Undo** buttons. **Edit** changes the amount (and notes) of what you just added; for a recipe added as individual ingredients, it sets their total amount and scales each one to match. **Undo** takes the addition back out of the meal, all of it, and a green line says what was removed.

<span id="meal-items-view"></span>
**View.** The **View** menu beside **Sort by** shows the same meal three ways. NuMa remembers your choice.

- **As logged** (the usual): each item as you entered it. A recipe you added whole is one row. A recipe you added as individual ingredients is one row per food, each marked "part of" the recipe.
- **Foods**: every food you ate. Recipes are broken down into their foods, including any recipe used inside another. A food that turns up in more than one place is one row with its total amount, and **From** says where it came from: a recipe's name, or "logged on its own". A food inside a recipe that has no nutrient data isn't listed. **✕** removes what you logged of the food yourself: on its own, or as one of a recipe's individual ingredients. A food inside a recipe you added whole can't be removed here (its row says "in a recipe"): remove the recipe, or change it. When a food is in both places, **Edit** and **✕** change only the part you logged yourself. **Edit** on a food you logged more than once sets their total amount.
- **Foods & recipes**: each recipe kept whole. The ingredients of a recipe you added as individual ingredients are gathered back into one row for the recipe, with their total weight in grams. That weight reflects any changes you made to those ingredients for this meal. **Edit** and **✕** work on every row. On a gathered recipe, **Edit** sets the total amount of its ingredients (a weight, or servings such as `2 srv`) and scales each one to match, keeping their proportions; **✕** removes them all.

<span id="meal-note"></span>
**Meal note.** The box beside the Protein Summary card holds a note about the meal: when you ate it, how you felt, what you'd change. **Save meal note** keeps it; save an empty box to remove it. Merged meals keep all their notes, each under its meal's name.


#### Meal History Tables {: #meal-history}

*Search terms: past meals, search history, exclude, absent, never eaten.*

Type a name or [ID](#gloss-id) in **Search meal history** on the Meals & Log list (a [code](#search-by-code) such as **U171477** or **[R21](#gloss-code)**, or an [FDC ID](#gloss-fdc-id)); results open on their own page. With **Meals that contain** (the usual), you get the two tables below. With **Meals that don't contain**, one table, *Meals without ...*, lists every meal it isn't in, with number, date, name and item count.

##### Meal history: occurrences
Each time the food or recipe was logged, linked to its meal.

    ID          The meal's number.
    Date        Date of the meal.
    Meal        Name of the meal.
    Food/Recipe Name of the food or recipe. Recipe items show "(recipe)".
    Portion     Amount logged: grams for foods, serving count for recipes.
    Notes       Your note for that item, if any.

##### Meal history: summary
Per food: times used, total grams, first and last dates.

    Food/Recipe Name of the food or recipe.
    Times       Number of times this food has been logged.
    Total       Total grams logged (-- for recipes, which are measured in
                servings rather than grams).
    First       Date of the earliest logged occurrence.
    Last        Date of the most recent logged occurrence.

Only items logged directly are searched, not ingredients inside a logged recipe, so a meal with a recipe made from the food counts as not containing it.


### H. The Analysis menu {: #analysis-menu-web}

*Search terms: reports, trends.*

- **Daily summary** — your recent days at a glance, each day's full analysis, and averages, totals and plots across days ([below](#daily-summary)).
- **Food use in meals** — how often you've eaten each food or recipe, counting foods inside recipes too ([Food Use in Meals](#fooduse)).
- **Food use in recipes** — how many of your recipes use each food or sub-recipe; not a measure of what you eat ([Food Use in Recipes](#fooduse-recipes)).

- **What-if: meals** — how dropping, adding, replacing or cutting down a food would change your daily nutrition over a set of days, without changing anything ([What-if: Meals](#whatif)).
- **What-if: recipes** — the same for recipes, per serving ([What-if: Recipes](#whatif-recipes)).

Both Food Use pages can also replace one food or recipe with another throughout what's selected ([Substitute](#fooduse-substitute)).

#### Daily summary (Analysis → 1) {: #daily-summary}

*Search terms: daily totals, day view, daily report, warning sign, weight changed, settle.*

Your recent days side by side, and the starting point for looking across several days:

- Buttons lead to [Nutrient averages over a period](#trend) (the last 7, 14 or 30 days, [any dates or chosen meals](#range-totals)), [Week-by-week averages](#summary-blocks) and the [Nutrient plot](#nutrient-plot), each described below.
- **Recent Days with Meals** lists each logged date: **Complete** (✓ when every meal that day is marked complete; click the dot to go to that day's meals), Protein and its percentage of your goal, Day [DCP](#gloss-dcp) and its percentage, the day's glycemic load if you track it, and any other nutrients you've chosen in [Settings → 11](#meal-columns). Click a date to open that day's full analysis: every meal pooled, with the same sections as a meal's page (see [Analyze full day](#full-day)). For a day older than the table reaches, open any of its meals in Meals & Log and click **Analyze full day** (shown when the day has more than one meal; with only one, that meal's page is the whole day).
- A yellow box above the table appears when a recipe's serving weight has changed since some meals logged it: it lists those meals, on any date, each with **Settle**, and the table marks their days with ⚠. What settling does: [Settling them all at once](#servings-yield-effects).

#### Nutrient Averages Over a Period {: #trend}

*Search terms: trends, several days, weekly average, chronic shortfall, multi-day.*

Every other comparison with your targets looks at one day. That shows whether today was enough, but not a nutrient that's a little short every day: one low day means little, two weeks of them is a pattern.

Click **Nutrient averages over a period** on the Daily Summary and choose the last 7, 14 or 30 days. NuMa averages each nutrient over the days in that window that have a meal logged, and compares the average with your targets in the same table as a single day, with the same colors and diet-aware notes.

**Only logged days count.** Days with nothing logged are left out, not counted as zero, which would understate your intake and hide the very shortfall this is for. The page says how many days were averaged ("Averaging over 12 logged day(s) out of the last 30").

The [B12, iron and zinc notes](#diet-bioavailability) apply here too, and this is often where such a pattern first shows.

**Averages for any dates, or a set of meals.**{: #range-totals} Below the 7/14/30-day buttons:

- **From / To** and **Average these dates** — any range of dates, not just the last 7, 14 or 30.
- **Meal IDs** and **Average these meals** — only the meals you list by number (shown on Meals & Log), separated by commas or spaces; `20-24` means meals 20 to 24. A number with no meal is named and skipped.

Either way the per-day average is what's compared with your goals; a **Total** column beside it gives the whole period's amount (useful for adding up a few meals as one, or a nutrient with weekly guidance), and total [DCP](#gloss-dcp) appears under the average. With meals chosen by number, the average covers only those meals, not the rest of those days; they're listed under **Meals included**.

**Week-by-week averages.**{: #summary-blocks} Shows the Recent Days table a block at a time: each row a run of days (7 by default), averaged per logged day, latest first. Choose **Days in each block**, **Number of blocks** and **Last day of the most recent block**, then **Show these blocks**. Columns are your Recent Days choices with their share of the goal, plus Day [DCP](#gloss-dcp) and Day [GL](#gloss-gl) if tracked; **All nutrients** opens every nutrient's average for that block. Comparing week with week shows whether a change is holding.

There are no complement suggestions here: complementing works within about a day, so a suggestion pooled over a week couldn't be acted on. Use a day's, meal's or recipe's [suggestions](#comp) instead.


#### Nutrient Plot {: #nutrient-plot}

*Search terms: graph, chart, nutrient over time, trend line, symbols, markers.*

A line plot of nutrients across your logged days.

Open it from **Analysis → Daily summary → Nutrient plot**. Tick up to 8 nutrients (any NuMa tracks, plus Day [DCP](#gloss-dcp); Protein, Calories, Carbs and Fiber come first; **Clear all nutrient checkmarks** starts afresh), then choose the days:

    (blank days-back)         Every logged day, oldest to newest.
    Days back + Ending on     The N days ending on the date you pick
                              (defaults to your most recent logged day).

**Each line has its own point shape** (circle, square, rectangle, asterisk, #, triangle, diamond, upside-down triangle), shown in the legend too, so lines can be told apart without color.

**Every logged day appears**, complete or not (unless you tick "Always end on last complete day"). A day with nothing logged is a **break in the line**, not a drop to zero, and a note counts them. A nutrient with no data in the range isn't drawn, and a yellow note names it. **Daily glycemic load**: a day where some carbohydrate food lacks a [GI](#gloss-gi) is drawn as a hollow point (a ring, for asterisk and # points) if foods with a GI cover at least 80% of its carbohydrate, since the real [GL](#gloss-gl) was at least that high, and left out below that; a note counts both.

**Goal and limit lines.** A nutrient with a goal gets a **dashed** line at it (your [Revised Optimal](#optimal) target, else its [RDA](#gloss-rda)/[AI](#gloss-ai)), and one with a limit a **dotted** line (the [Tolerable Upper Intake Level](#maxlimits), or your own cap), in its own color. Two lines at the same height share one line with alternating colors. A note under the title says which lines are shown.

**Always end on the last complete day.** Instead of a fixed end date, the plot always ends on the latest day whose meals are all complete, which suits a Home page plot. Earlier days with an incomplete meal are left out too, as breaks, so a partly logged day can't drag the line down; a note says how many. If every day has an incomplete meal, the page says there's nothing to draw.

**Date labels thin out** past 18 days, so they stay readable; every day still has a point.

**Mixed units.** Nutrients with different units (protein in g, sodium in mg) share one axis, which then has no numbers, since no single scale fits every line; the gridlines show relative movement, and each line's real values are in the legend. One nutrient, or several in one unit without scaling, gets a normal numbered axis.

**Scaling, in two steps, both adjustable.**

*Step 1 — Scale factor.* When one nutrient's numbers dwarf another's (calories beside protein), the smaller would flatten along the bottom. So NuMa divides every nutrient but the steadiest by a **Scale factor**, based on how much each swings, to bring their swings to a similar size. The box shows the computed value greyed; leave it blank to use it, or type your own and click Plot.

*Step 2 — Per-nutrient factors.* With three or more nutrients, one can still end up nearly flat, so any nutrient swinging less than a quarter as much as the liveliest gets its own multiplier ("×2.4" in the legend). Each has a **Per-nutrient factors** box, used the same way.

**Highlight nutrient** is drawn solid (and red, in color), so the figure you compare everything against stands out. It defaults to Day DCP when chosen.

**Black & white (printer-friendly)** draws every line in black, the highlighted one solid and the rest in dash patterns. The plot changes as soon as you tick it.

**Smoothing (days)** averages each point with the logged days before it (default 3; 0 turns it off), and the note under the title says so. Scaling is worked out from the smoothed data. Missing days are skipped, not counted as zero. The first points are smoothed like the rest, using days before the start date (read but not drawn); if there aren't enough earlier days, the first few points average fewer days and can swing more, and a note says how many.

**Plot title** defaults to "Key nutrients, {start date} to {end date}"; type your own and click Plot.

**Legend placement.** The legend never covers a line. Choose:

- **Auto (above, else right)** — the default: under the title while it fits on one row (up to four nutrients), otherwise in a column to the right.
- **Always above the plot** — the plot shrinks a little to make room.
- **Always below the plot.**
- **Right of the plot, in a column** — one name per row, the plot keeping its full size. In a window under 992 pixels wide it moves below the plot instead; print and downloads keep it at the right.

The plot changes at once, and the choice goes with it into print, downloads and the Home page copy.

**Print or save it.** **Print / Save as [PDF](#gloss-pdf)** opens a print-friendly page; **Download [PNG](#gloss-png)** and **Download [SVG](#gloss-svg)** save an image ([which to pick](#plot-file-formats)).

**Show this plot on the Home page**, beside Plot, puts this plot (a little smaller) near the top of the Home page, with an **Edit this plot** link. Only one plot at a time; while it's on, changes you make here appear there too. Untick it to remove it. Your plot settings are remembered between visits; **Reset to defaults** starts over.


##### Plot File Formats — PNG vs. SVG {: #plot-file-formats}

*Search terms: download plot, export plot.*

Both save the same plot as an image, stored differently.

**[PNG](#gloss-png)** is an ordinary picture made of pixels. It opens everywhere: the safe choice.

**[SVG](#gloss-svg)** stores the lines and shapes themselves, so it stays sharp at any size, where a PNG blurs when enlarged. A few older programs can't open it.

**Rule of thumb:** to view, email or put in a document, PNG; to print large or let others resize it, SVG.


#### Food Use in Meals — Column Guide {: #fooduse}

*Search terms: how often, most eaten foods, food usage.*

Everything you actually ate across the meals you choose: foods logged alone, recipes, the sub-recipes inside them, and every food inside a recipe. Choose one or more date ranges, or a list of meal numbers (not both), and all foods or only those with protein. To find one item in a long table, type part of its name (or its exact code) in **Show only foods and recipes whose name contains**{: #fooduse-name} and click **Analyze**; counts and percentages still cover the whole selection, and **Clear name filter** shows everything again.

Columns:

    Food        Food or recipe name. Recipe rows are shown in bold.
    Code        The item's code: U = USDA food, UD = user-drafted food,
                R = recipe, OFF/CNF/CoFID/AFCD/CIQUAL = a food from
                that database. A key sits under the table.
    Days used   Number of distinct calendar days on which this food or
                recipe appeared, within the meals you selected.
    Meals       Number of selected meals containing this food or recipe.
    Meal IDs /  The meals (or, switched, the dates) the item was eaten in.
    Dates eaten A "Last column shows" switch above the table picks which;
                each meal ID opens that meal, each date opens that day's
                Daily Summary. Your choice is remembered in this browser.

Rows are ranked by Days used (then Meals, then name), with a bar showing how often.

A logged recipe counts both as itself and as each of its ingredients, through any recipes inside it, so both the dish and its parts are ranked, and a food or sub-recipe you only eat inside recipes still counts as eaten.

Rows always show an item's current name, and gather every use under it, even meals logged before a rename.

The **Replace, remove or add a food or recipe in these meals** panel above the results makes a change across all the selected meals ([Substitute](#fooduse-substitute), [Removing or adding](#fooduse-remove-add)).


#### Food Use in Recipes — Column Guide {: #fooduse-recipes}
Which foods and recipes your recipes use as *ingredients*: your recipe book, not what you eat (a recipe you log but never use inside another won't appear; for eating, see [Food Use in Meals](#fooduse)). Choose all recipes (the default), recipes created in certain date ranges, or a list of recipe numbers, and optionally only foods with protein. **Show only foods and recipes whose name contains**{: #fooduse-recipes-name} works as on Food Use in Meals.

Columns:

    Food / Recipe       Food or sub-recipe name. Sub-recipe rows are shown
                        in bold.
    Code                The item's code (U, UD, R, OFF ... — see
                        Food Use in Meals above, or the key under the
                        table).
    Recipes used in     Number of selected (container) recipes whose
                        ingredient list contains this food or sub-recipe,
                        directly or nested inside another sub-recipe.

Rows are ranked most-used first, with a bar showing the share of selected recipes using each. A sub-recipe (a house dressing in several salads) gets its own row, and its ingredients are listed too.

The same **Substitute a food or recipe** panel works on the ingredients of the selected recipes ([Substitute](#fooduse-substitute)).


#### Replace a Food or Recipe Everywhere (Substitute) {: #fooduse-substitute}

*Search terms: replace food everywhere, swap food, bulk replace.*

Replaces one food or recipe with another everywhere it's used in the current selection (the dates or numbers you searched with), in one step. Both Food Use pages have it.

A refused deletion leads here too: when Food Cache or Custom Food Profiles won't delete a food because it's in use, the message's "swap it for a different food" link opens this with those meals or recipes selected and the food filled in; you just pick the replacement.

It's the tool for what looks like two foods but is really one (after re-adding a food from a search instead of using the cached copy, say), which you want under a single entry.

On either Food Use page, after you've searched:

1. Tick **Replace** (on Food Use in Meals, **Replace or remove**) beside the item to get rid of; only one at a time. The panel opens with "Replace this" filled in.
2. In **Replace it with**, type part of the replacement's name and pick it from the list (mouse, or arrows and **Enter**). The list covers your Food Cache and recipes. A line reads back what will replace what.
3. Click **Substitute everywhere in this selection** (on Food Use in Meals, **Replace everywhere in this selection**) and confirm.

The page then comes back to this panel with the outcome in a colored box at its top. Green names what was changed and where: "Replaced “Oats, rolled” (U173904) with “Barley, pearled” (U170284) in 3 meals." Red means nothing was changed, and says why: a code no food or recipe has, or an item that isn't in the selected meals or recipes. After a red box the codes you typed are still in their boxes, so you can correct a typo and try again.

A dash instead of a tick-box means the item can't be reached from this selection: on Food Use in Meals it was eaten only *inside* a recipe; on Food Use in Recipes it's only inside an unselected sub-recipe (select that too, or choose "All recipes"). A food not yet in NuMa won't be listed; add it through [Food Search](#food-search) first.

You can also type codes into the two code boxes:

    Replace this         The old item's code (U171477, UD4, R21, OFF3 ...).
    With this /
    Replacement (code)   The replacement's code.

The item you're replacing is marked "replacing this" when you arrive from a refused deletion. Codes are shown on [Food Search](#food-search) and the Recipes list.

A food can replace a recipe and vice versa. The amount recorded is kept as it is; only *what* it points to changes, so check the amount makes sense if the two are measured differently.

On **Food Use in Meals**, only items logged *directly* are replaced; a food inside a recipe belongs to the recipe. Such a row says **Eaten only inside**{: #fooduse-inside-recipes} (or **Also eaten inside**) and names the recipe; **replace it in that recipe** opens Food Use in Recipes ready to do it there. So a food still showing after a replace hasn't failed: it's in a recipe those meals use. On **Food Use in Recipes**, each changed recipe's [DCP](#gloss-dcp) is recalculated, and so is every recipe using it.

A recipe is never put inside itself; that case is skipped.

The change is saved as soon as you confirm, with no undo, so check first.

**Removing or adding a food in many meals.**{: #fooduse-remove-add} Food Use in Meals can also take an item out of every selected meal, or add one to each: say you stopped salting the breakfasts you'd copied for a week, or forgot the nutritional yeast in all of them. Select the meals (use **Meal IDs** if a date range catches too many), then:

- **Remove from every meal**: tick the item, then **Remove from every meal in this selection**. Lines logged directly go; one inside a recipe stays.
- **Add to every meal**: pick the item, give the **Amount in each meal** as on a meal page (a food: `30 g`, `1/3 c`; a recipe: `1 serving`, a weight or volume, a bare number meaning grams), and click **Add to every meal in this selection**. Each meal gets one new line, even if it already has the item.

**Only some of the days.**{: #fooduse-pick-dates} **pick dates**, beside a row's Days used, lists the dates the item was eaten, with their meals. Tick the dates you want (**tick all**, **untick all**); a replace, remove or add then reaches only those meals (an add goes in beside the item), and the panel says which. Untick all to use the whole selection again. Dates can be ticked in several rows.

Both save as soon as you confirm, with no undo. To see the nutritional effect first, try it in [What-if](#whatif).


#### What-if: Meals {: #whatif}

*Search terms: hypothetical, simulate, try a change, expanded recipe, recipe ingredients.*

Shows how your average daily nutrition over a set of days would change if you ate differently: dropped a food, added a supplement, swapped one food for another, or ate less of something. Nothing is changed.

1. **Which meals.** Dates, one per line: a range (`2026-09-01:2026-09-30`) or a single date. Or switch to **Meal IDs** to pick meals.
2. **What to change.** One change per row; **Add another change** adds rows, all applied together. Type part of a name and pick it from the list (or type its [code](#fooduse)).
3. **Which days to average over.** Every logged day in the selection, or only the days when something you're removing, replacing or changing was eaten. If 112 of your days are logged and the food was eaten on 47, the first shows the effect on your diet overall, the second what those 47 days would have looked like. **Add** rows don't narrow the days.
4. Click **Show the effect**. Switching the day choice afterward redraws at once.

A bold line above the results says which days are averaged and how many contained what you're changing.

The four actions:

    Remove          Takes the food or recipe out wherever it appears —
                    logged on a meal, or used inside a recipe (at any depth).
    Add             Adds an amount once on every day that has a meal logged
                    (days with nothing logged are left alone). A food takes
                    any amount the meal page accepts (1/3 c, 30 g, p1); a
                    recipe takes servings (1, 1 1/2) or grams (150 g).
    Replace         Swaps one item for another only where the old one was
                    eaten. Choose how much of the replacement: the same
                    weight, a multiple of the old weight (1.1 or 110% =
                    a tenth more), the same servings (recipe for recipe),
                    or a stated amount each time.
    Change amount   Multiplies the amount eaten everywhere it appears.
    (multiply)      Type the multiplier as a number or a percentage:
                    1.5 or 150% = half again as much; 0.5 or 50% = half.

<span id="whatif-ingredients"></span>**A recipe logged as individual ingredients.** When you add a recipe to a
meal as separate ingredients, the meal holds the foods, not the recipe. Each of those foods remembers which recipe it came from (the meal page shows *part of* and the recipe's name beside it), so **Remove** and **Change amount** still find it, and change those foods together; the change's line says so. That holds even after you changed them for that meal: an ingredient left out, an amount changed, or a food swapped for another. A food you added to the meal yourself is not part of the recipe and stays. Foods logged this way before 2026-11-17 don't carry that link; for them, NuMa looks for foods matching the recipe's ingredients at the same portion size. If those were changed, or the recipe has changed since, nothing matches and a note names the meal; change the foods one by one. This works for Remove and Change amount (including [applying for real](#whatif-apply)). Two things it can't do, and the change's line names the meals where they happen, so you can fix those by hand:

- **Replace** works only where the recipe itself was logged, not its separate foods. In those meals, remove the recipe's foods and add the replacement yourself.
- **A recipe used inside another recipe** (a sub-recipe) is found wherever the outer recipe was logged whole, but not where the outer recipe was logged as individual ingredients: those foods record the outer recipe, not which sub-recipe each came from. Change those foods in the meal yourself.

To swap foods: **Replace** puts the new food only where the old one was; a **Remove** row plus an **Add** row drops the old and adds the new on every logged day.

What you see:

- A line per change saying how many meals and days it was found in; a change that matched nothing is pointed out, so a typo doesn't go unnoticed.
- A table of calories, protein, Protein ([DCP](#gloss-dcp)), carbohydrate, sugars, fat and fiber per day: **Before (as logged)**, **After your changes**, **Change**. DCP is worked out per day as on the Daily Summary, with a note if some days lack the data.
- A table of every nutrient that changed (a link shows the rest): before, after, change, % of target before and after with its status (as on the [Daily Summary](#goals)), and how many days fell short of the target, or over a maximum, before and after. An average can look fine while several days fall short. Order by **Largest change first** or **Grouped like the daily summary**.
- **?** beside a nutrient: something you added has no value for it, so "after" may be too low.

Targets come from each day's pinned profile; days with nothing logged are left out, not counted as zero. Glycemic load is recalculated too ([Glycemic load in a what-if](#whatif-gl)).

**try removing**, on each row of [Food Use in Meals](#fooduse), opens this page with that item entered. The page's address holds the whole scenario, so you can bookmark it.


#### What-if: Recipes {: #whatif-recipes}

*Search terms: what-if recipes, recipe scenario, change ingredient, recipes by name, ingredient list.*

The recipe version of [What-if: Meals](#whatif): how each recipe's nutrition **per serving** would change if you removed, added, replaced or cut down an ingredient. Nothing is changed.

1. **Which recipes.** All recipes (the default), **By name**, recipes created on certain dates, or a list of recipe IDs. **By name** takes the recipes whose names hold every word you type (`chicken soup`); `!word` leaves out names with that word (`soup !lentil`). As you type, the matching recipes are listed under the box.
2. **What to change.** The same rows as What-if: Meals. Remove, Replace and Change amount reach the ingredient wherever it's used, sub-recipes included. For **Remove** and **Change amount**, click the food/recipe box: it lists every food and sub-recipe in the recipes chosen in step 1, most used first, with how many of them use each ("in 3 of 5"). Type to narrow the list, then pick one. For **Add** and **Replace**, the box searches all your foods and recipes, as on What-if: Meals. **Add** puts an amount into each recipe, for **each serving** or **the whole recipe**.
3. Click **Show the effect**.

Servings never change, so removing an ingredient makes each serving lighter: "if I left out the nutritional yeast, what would one serving give me?"

To swap at a different amount (pumpkin seeds for hemp seeds at 1.1 times the weight), use one **Replace** row with **A multiple of the old weight**, `1.1` (or `110%`).

To use more or less of an ingredient, use **Change amount (multiply: 1.5 or 150%)**: 1.5 or 150% for half again, 0.5 or 50% for half, wherever it's used. Remove plus Add does it with an exact amount ("10 g per serving"), but Add puts the ingredient into every selected recipe.

The results are a grid, a column per recipe: each cell the value per serving **after** your changes, in bold, with the change below (**Also show the before values** adds the old one). **Average change**, the first column, averages each recipe's percent change over every recipe reached; recipes that had none of the nutrient are left out of it ("over N" says when). Only changed nutrients are listed; a link shows the rest. Protein ([DCP](#gloss-dcp)) is worked out as on the recipe page; NC (not computed) means an ingredient with 1 g or more of protein lacks amino acid data.

Only recipes the change reaches are shown (with only Add rows, all selected ones), at most 8, the most-changed; the rest are named, so you can choose with **Recipe IDs** or **By name**.

Unselected recipes that use a changed recipe are listed under the grid, since they'd change too; **Show them too** adds them.

**try removing**, on [Food Use in Recipes](#fooduse-recipes), opens this page with that ingredient entered.


#### Glycemic load in a what-if {: #whatif-gl}

*Search terms: what-if GL, glycemic load before and after.*

Both what-if pages show [glycemic load](#gl) before and after, from the same changed foods.

- **What-if: Meals** adds a **Glycemic load** column to *Average per day*: the average day's [GL](#gloss-gl) over days with carbohydrate, with its band on the day scale (Low under 80, Moderate 80–120, High over 120) and, with a [daily target](#gl-target), how many days were over it, before and after.
- **What-if: Recipes** adds a **Glycemic load** row: GL per serving, with its band (Low 10 or below, Medium 11–19, High 20 or above), and "(was …)" when the band changed.

**Watch the coverage.** GL counts only foods with a [GI](#gloss-gi). Swap a food with one for a food without, and "after" drops because NuMa can't count the new food, not because it's better. So NuMa says how much carbohydrate each figure covers, before and after, and names the foods without GI, each linked to its Annotate page ([look one up](#gi-source-para)); on the Recipes page a cell reads **≥** with its coverage. Add the missing GI and run it again for a fair comparison.

A typical use: replace a high-GI staple you eat often (white rice) with a lower one (barley) at the same weight, and see your day's GL band change, along with fiber, protein and everything else.


#### Saving, downloading and applying a what-if {: #whatif-apply}

*Search terms: save scenario, apply changes, make it real, delete from meals.*

With results showing, a bar under the changes offers:

- **Save this scenario.** Name it; it appears under **Use a saved scenario** at the top of the page (meals and recipes have separate lists), to open, rename or delete. Opening brings back everything, dates exactly as typed.
- **Download CSV.** A [CSV](#gloss-csv) spreadsheet file of the changes and every nutrient; from What-if: Recipes, for *every* recipe reached, not just the 8 shown.
- **Apply these changes for real…** Changes your actual meals or recipes, so it's offered only when doing so gives exactly the result shown. Limits: a **Replace** must be food for food at the same weight, or recipe for recipe at the same servings; a **Change amount** of 0% is a removal (use Remove); nothing is changed twice, or replaced with or added as something another change changes. Otherwise the bar says why. After applying, the button is hidden, so nothing is added twice.

Clicking it first lists what will change, meal by meal or recipe by recipe; **Yes, make these changes** goes ahead. What each action does:

    Remove          Deletes the item from those meals, or the ingredient
                    from those recipes.
    Add             Meals: puts the item in a new meal called "Added by
                    what-if" on each day, so your own meals stay as you
                    logged them. Recipes: one more ingredient in each
                    selected recipe (per batch or per serving, as chosen).
    Replace         The same substitution as the Replace box on
                    Food Use in Meals and Food Use in Recipes.
    Change amount   Multiplies the amount. Afterwards it's shown in grams
                    (servings for a recipe), since "2 c" no longer
                    describes it.

For a recipe [logged as separate ingredients](#whatif-ingredients), exactly the matched foods are deleted or changed, and the page says how many.

It also says what stays as it is: on What-if: Meals, a food inside a recipe (changing the recipe would change every meal using it; use What-if: Recipes); on What-if: Recipes, a recipe with the item only in an unlisted sub-recipe. A recipe can't be added to itself or to a recipe it's in.

**Changing a recipe changes the meals that use it**, past days included, so What-if: Recipes says how many logged meals that is. It also lists recipes with a stored total weight or water once cooked, which applying doesn't change, so check them afterward. Each changed recipe's [DCP](#gloss-dcp) is worked out again.


### I. The Settings menu {: #settings}

*Search terms: preferences, options, configuration, setup.*

Settings has sixteen numbered sections, each opening and closing. The **Contents** sidebar on the left lists them all: click one to open it and go straight to it.

- **1. [Your Profile](#profile-setup)** — age, sex, weight, height, activity level (this drives all your daily nutrient targets), plus a checkbox enabling [oxalate](#oxalate) lookup, your [glucose tolerance](#gi-impaired) (the [GI](#gloss-gi) lookup default, and which advice [GI](#gloss-gi) notes give you), and an optional [daily glycemic load target](#gl-target).
- **2. Computed Daily Targets** — see [Computed Daily Targets (Settings → 2)](#daily-nutrient-targets).
- **3. Dietary Preferences** — affects complement suggestions, [B12/iron/zinc guidance](#diet-bioavailability), and (see [Dietary Preferences](#diet)) every search and lookup in the program.
- **4. Protein Digestibility Overrides** — custom digestibility numbers for specific foods.
- **5. Nutrient Targets - Researched** — optional per-nutrient [Revised Optimal (Recent Research)](#optimal) targets and [Max limits](#maxlimits), with a one-click button to load recommended defaults.
- **6. [USDA](#gloss-usda) [API](#gloss-api) Key** — lets you use your own free personal code from USDA's website instead of the one NuMa shares with every user by default, so your searches are less likely to get temporarily blocked when many people are using NuMa at once (NuMa checks a key with USDA before saving it; see [Food data](#usda-api-key) for how to get one); also has the [search result depth](#search-ranking) setting.
- **7. Glycemic Index Reference Table** — which [GI](#gloss-gi) table lookups search, and building the 2021 one (see [Upgrading to the 2021 tables](#gi-editions)).
- **8. Glycemic Load** — show or hide every [glycemic load](#gl) figure: on food, meal, recipe and day pages (with the [estimated GI](#mixture-gi)), the day's [GL](#gloss-gl) so far under a meal's and a day's title, the [GL](#gloss-gl) columns and sort on Meals & Log and Recent Days, the [GL](#gloss-gl) trend and plot series, Compare, What-if, Top Contributors' [GL](#gloss-gl) ranking and swaps, printouts, and your daily [GL](#gloss-gl) target in Settings → 1. On unless you turn it off. [GI](#gloss-gi) values are still shown and kept, and nothing is deleted: turning it back on brings everything back, including a daily target you'd set. This is separate from **I do not record glycemic index data** in Settings → 7, which only stops NuMa asking you for GI values.
- **9. Water Tracking** — show or hide everything about [water](#water): the drinks / food split, the drink tick-boxes, the water fill-in and the check for a wet food picked in place of a dry one. On unless you turn it off; turning it off deletes nothing. From age 65, a day's page also warns when its drinks fall below the minimum that ESPEN (the European Society for Clinical Nutrition and Metabolism) recommends for older people.
- **10. [Daily Starting Items](#daily-start)** — foods and recipes added to the first meal of each new day.
- **11. [Meals & Log columns](#meal-columns)** — which nutrient columns your meal lists show.
- **12. [Starter Data](#starter-data)** — curated foods and recipes to explore or build on.
- **13. Browser to Launch** — see below.
- **14. Data Quality Reminder** — the Home page note about new data problems (see [Checking your data](#data-check-reminder)).
- **15. Keyboard Shortcuts** — see [Finding your way around](#web-shortcuts).
- **16. System Issues** — see [below](#system-issues-howto).

#### Your Profile {: #profile-setup}

*Search terms: personal details, body measurements.*

Age, sex, weight, height and activity level. All your targets come from these: [RDAs](#rda), [Daily Nutrient Goals](#goals), and any [Revised Optimal targets](#optimal) and [Maximum Nutrient Limits](#maxlimits). The same form has the [oxalate](#oxalate) lookup box (off unless you tick it), your [glucose tolerance](#gi-impaired) and an optional [daily glycemic load target](#gl-target).

Without a profile NuMa still works, but every "% of daily target" is blank. Fill it in whenever you're ready: days that follow your current profile (the usual case, see [Per-Day Profile Tracking](#day-profile)) are re-scored at once.

#### Per-Day Profile Tracking {: #day-profile}

*Search terms: profile changes, past days, history, rescoring, pinned profile.*

Your profile changes over time (weight, activity, which profile is active), but logged meals don't. If past days were always scored against today's profile, an old day could be judged by numbers that weren't true of you then. So each day can keep its own profile.

**A new day follows your current profile.** A day starts with its **current profile** switch ticked, so its goals follow your profile. NuMa also keeps a full copy of the profile as it was that day. Untick the switch and the day goes back to that copy and stays there, whatever you change later.

**Today, even when unticked**, is re-pinned whenever you save your profile or a researched target, since it's still in progress, unless you set today's profile by hand with **Change**.

**Applying a change to earlier days.** After you save your profile, **Also score every logged day from [date] to today against this profile** appears: pick a date and click **Apply profile to those days**. Days you set by hand are skipped; NuMa says how many it switched.

**The "current profile" switch** is beside "Profile:" on a day's Summary and Full Day pages (**Score this day against my current profile**), and under each date on Meals & Log (**current profile**). Ticked, the day follows your profile; unticked, it returns to the copy it was pinned to, which NuMa keeps meanwhile.

**Where you see it.** With more than one named profile, a **Profile** column or line appears beside each day on Meals & Log, Recent Days and the day's pages.

**Changing a day's profile.** Illness or travel rarely starts at midnight. **Change**, beside "Profile:" on the day's page, picks another saved profile; the day is marked "(manually set)" and re-scored at once.

**Averages across days** ([Nutrient Averages Across Days](#trend)) are scored against the most recent day's profile, with a note naming any days in the window that had a different one.

**Days logged before this feature existed** were pinned to the profile active when you first ran the new version.


#### Computed Daily Targets (Settings → 2) {: #daily-nutrient-targets}

*Search terms: daily targets, goals table.*

A read-only table of your targets, worked out from your profile: calories, protein, carbohydrate, fiber and every tracked mineral and vitamin, each labeled minimum, target or upper limit. It updates when your profile changes; if it looks empty or wrong, check your profile. The formulas are in [Daily Nutrient Goals](#goals), the reference values in [RDA](#rda).

**Every percentage carries its goal type.** 120% is good for a minimum (protein) and bad for a limit (sodium), so wherever a percentage appears it's followed by a small `min`, `max` or `target` tag (hover for more).

#### Dietary Preferences (Settings → 3) {: #diet}

*Search terms: diet preference, vegan, filter foods.*

Which foods NuMa offers: in complement suggestions, and in every food search.

| Option | Setting | Includes |
|---|---|---|
| 1 | All animal foods | meat, fish, dairy, and eggs |
| 2 | Vegetarian | dairy and eggs only (no meat or fish) |
| 3 | Plant-based only | plant sources only |

It's kept between sessions, and applies to exported reports too.

**A quick switch above every Protein Complement Suggestions list** changes it at once and reloads the suggestions, so you can see what a plant-only complement would look like and switch back; **Change settings** opens this section.

**It also filters food searches.** With "plant-based only" or "vegetarian", other foods appear nowhere in NuMa, not even by [FDC ID](#gloss-fdc-id). If a search finds nothing, check this setting; to look something up anyway, switch to "All animal foods" for the search, then back.

#### Protein Digestibility Overrides {: #dcp-overrides}

*Search terms: digestibility override, custom digestibility.*

Your own true [ileal digestibility](#gloss-ileal-digestibility) figures for particular foods, used instead of NuMa's defaults in meal [DIAAS](#gloss-diaas) calculations.

Columns:

    Food name       Name of the food this override applies to (matched
                    case-insensitively against meal ingredients).
    Digestibility   Your custom coefficient (0.00-1.00). The fraction of
                    protein absorbed by the small intestine.
    Notes           Your source note (e.g. "Smith 2020 Table 3").

An ingredient using one shows a small "user" marker in the Digestibility column.

Use one when you've found a published, measured value for a food you eat often that differs clearly from NuMa's. It should come from digestibility studies, not labels or general nutrition sources.

In **Settings → 4**, enter the food's exact name, a figure from 0.00 to 1.00 and an optional source note, then Save. The same name again replaces it; ✕ deletes it. See also [Meal Protein Digestibility Analysis](#meal-diaas) and [DIAAS](#diaas).

---

#### Browser to Launch

*Search terms: default browser, which browser opens, desktop app, standalone window, app mode, no tabs, address bar.*

NuMa normally opens in **its own window**: no tabs, no address bar, its own icon in the taskbar and Alt+Tab, like a desktop program. This needs Chrome, Chromium, Brave, Microsoft Edge or Vivaldi installed (you needn't use it otherwise, or have it running); Firefox and GNOME Web can't do it. To use a normal browser tab instead, untick **Open NuMa in its own window**; it takes effect next time NuMa starts.

NuMa's own window runs separately from your everyday browser, even when it's the same browser. That keeps it a program of its own in Alt+Tab and the taskbar, with its own icon, rather than one more browser window. It also has its own browser settings, kept apart from your browser's, so your browser's add-ons (extensions) don't run in it and can't take over NuMa's keyboard shortcuts. A page you open from it with Ctrl+click opens in a browser window that belongs to NuMa's window, not in your everyday browser.

In a normal tab (own window off, Firefox or GNOME Web chosen, or none of those browsers installed), NuMa asks which browser to use if several are running. Choosing a **Browser to Launch** skips the question; "Ask each time" is the default. With its own window on and "Ask each time", NuMa uses a suitable browser that's running, or any installed one.

The last box brings back the Ctrl+click explanation from [Working in two windows](#two-windows).

#### Starter Data {: #starter-data}

*Search terms: sample data, demo data, example recipes, preloaded.*

A small set of checked foods and recipes, loaded automatically on a new install so your Food Cache and Recipes aren't empty. Many foods have full amino acid data, some a glycemic index value (only ones NuMa may share), and several recipes show protein complementing at work. Some foods (salt, vanilla, cinnamon) are there only because a starter recipe uses them; **View all starter data** shows which recipes use each. Their names start with `* `. Your pantry starts empty: only you know what you keep ([Set up your pantry](#first-setup)). This section is for putting the starter data back after clearing it, or loading it into an older install: **Load starter data** restores it all, **Restore individual starter items** chosen ones.

Loading never touches what you already have (a food you have is skipped), and **Clear starter data** removes only what loading added.

**Clear keeps whatever you've made your own:** anything you've renamed (including removing the `*`), edited, re-portioned or given a [GI](#gloss-gi) or [DIAAS](#gloss-diaas) value, and anything in use in a meal, one of your recipes or your pantry. Settings says how many were kept, and why.

**When a new version changes the starter set,** NuMa tells you what's different:

   - **New items** are marked **(new in this version)** in **Restore individual starter items**, which opens by itself, with a short description of each. Tick and click **Restore selected**. Something you deleted on purpose is never shown as new.
   - **Improved items** you already have are listed under **Improved in this version of NuMa**, each showing exactly what updating would change in *your* copy (your own edits marked **your edit**). **Update the checked items to the new version** replaces your copy, *your changes included*, so leave edited ones unticked; **Update all N items to the new version** takes them all, after a confirmation. Anything using an updated item keeps working and is recalculated. **Keep all my copies as they are** stops the offer.

These lists stay until you act on them, and a skipped version's changes are included in the next.

#### System Issues {: #system-issues-howto}

*Search terms: stale scores, outdated DCP, recalculate, out of date, refresh totals.*

*One of NuMa's data checks — see [Checking your data](#checking-your-data) for the rest.*

NuMa saves each recipe's [DCP](#gloss-dcp), and each meal's DCP, calories and totals, for its lists. Whenever a food or recipe changes, it recalculates every recipe depending on it, up the chain, and every meal using them, by itself ([what changes](#editing-consequences)).

**System Issues lists the times that recalculation itself failed** because of a software error, which would otherwise leave a stale figure with no sign of trouble. It's not for "NC" (not computed), which just means DCP can't be worked out yet because a significant ingredient lacks amino acid data.

**You can't miss one:** a red alert at the top of every page links here. **Got it. Don't remind me again.** hides it until another failure; the failure stays listed until fixed.

Each entry shows when, which recipe or meal, and the error. **Retry** recalculates at once:

- If it works, the entry clears.
- If it fails again, the entry stays with the new error. A repeat failure usually means a bug: please [report it](#feedback).

Opening and saving the recipe does the same as Retry.

The Home page also shows a banner for each new entry, with its own **Got it** box.

**Updates.** The Home page checks GitHub for a newer release and shows **UPDATE AVAILABLE** if there is one, with a **Don't show this again for this version** box. The check takes a second or two and fails quietly offline ([details](#home-page-tour)).

**Update Now**, on the packaged Linux install, downloads and installs the new version in place, leaving your data untouched; close and restart NuMa when it says so (the running version keeps working until then). On Windows, or running from source, there's a **Download NutriMagnus** button or a GitHub link instead.

#### Daily Starting Items {: #daily-start}

*Search terms: every day, routine, supplements, vitamins, automatic, default foods, template.*

Some things you have every day: a vitamin pill, a morning coffee, the same breakfast cereal. **Settings → 10. Daily Starting Items** saves you adding them by hand each day. List them once, and whenever you create a meal on a date that has no meals yet, NuMa adds them to that meal for you.

**Setting them up.** Each row takes a **code** and an **amount**:

- The [code](#gloss-code) is the one in the **Code** column of the Food Cache, My Pantry or the Recipes list: [U171477](#gloss-code) for a [USDA](#gloss-usda) food, [UD4](#gloss-code) for one you entered yourself, [R21](#gloss-code) for a recipe. Capital letters don't matter.
- The amount is written the way you'd write it on a meal: `1 cup`, `40 g` or `p1` (the food's first saved portion) for a food; `1 serving`, `2 srv` or `200 g` for a recipe. Left empty, it means 100 g of a food or 1 serving of a recipe.
- A food must already be in your Food Cache. If it isn't, search for it and add it to a meal or your pantry once, and it will be.

**Finding a code without leaving Settings.** Above the table, **Find a code** has a search box with **Search foods** (your Food Cache; Enter does the same) and **Search recipes** buttons. Type part of a name (every word must be in it, and `!word` leaves out names with that word) and click one: the matches are listed with their codes, a food with its first few saved portions (`p1`, `p2` …) and a recipe with what one serving weighs. **Use** on a match puts its code in the first empty row and moves the cursor to that row's amount box. Nothing is saved until you click **Save daily starting items**.

Click **Save daily starting items**. The table then shows the name of each food or recipe beside its code, with the amount it works out to. There are always three empty rows at the bottom; to add more than three items, fill those in, save, and three more appear. To take an item off the list, tick its **Remove** box and save.

If a code or amount can't be used (a mistyped code, or an amount NuMa can't read, such as `3 flurbs`), **nothing is saved**: a red box says what's wrong with each row, and everything you typed is still there to correct.

**When they're added.** Only the *first* meal created on a date gets them: later meals that day get nothing extra, and meals you already have are never changed. This works for any date with no meals yet, including a past day you're filling in. Merging meals and What-if don't create new days this way, so they never add them.

**On the meal page**, a green line names what was added, with an **Undo** button that takes all of them back out at once (handy on a day you skipped them). You can also change or remove each one in the Items list, like anything else in the meal. If an item can no longer be added (its recipe was deleted, say), a red line names it, and the others are still added.

### J. The Manual {: #manual-menu}

*Search terms: help, documentation, user manual.*

**Manual** (Alt+Shift+A) opens this document, in the same window as the rest of NuMa, at the section you were last reading. The yellow bar above it has two ways out: **↩ Return to …** (Alt+Shift+U) goes straight back to the NuMa page you came from, and **← Back one step** (Alt+←) undoes your last jump inside the manual (see [Getting back to where you were](#manual-back)). The sidebar has a search box, the table of contents and your bookmarks. Small **Learn more** links on NuMa's pages open the relevant section directly.

#### Using this manual's search {: #search-howto}

*Search terms: manual search, how to search, find in manual.*

The search box is at the top of the sidebar.

**It finds sections containing all your words**, anywhere and in any order. `portion size` finds sections with both words, not necessarily together. A phrase that never appears word for word (`edit portion`) still works, as long as each word appears. If a search finds nothing, drop a word: start with the noun you care about (`portion`), and add a second only if the list is too long.

**The best match comes first:** a section ranks higher when your words are in its heading, make up more of a short section, or are rarer (in `replace food`, "replace" counts for more than "food").

**Double quotes find an exact phrase:** `"iron and zinc targets"` finds that exact wording, for finding a sentence you remember. It's more likely to find nothing; then drop the quotes.

**Results are sections.** Click one (or press **Enter** for the top one) to open it with every match highlighted; **Enter** / **Shift+Enter** (or ▲ / ▼) then step through the highlights in that section.

**Sections also answer to everyday words they don't use.**{: #search-terms} Some carry a hidden list of other words people search with (*seniors* for a section that says "65 and over"). Nothing on the page is highlighted then; the count under the box says **this section is listed under that search**.

**Only show things you can do** keeps only sections with instructions (add, edit, change, remove…), for when you want to do something rather than understand it. It's a rule of thumb that can miss a section, so if the list comes up empty, untick it.

**Match case** and **Whole words only** help with short terms that are also parts of words: "AI" (artificial intelligence) normally matches *main*, *detail*, *said*. **Match case** matches only capital "AI"; adding **Whole words only** also skips it inside capitalized words. **Whole words only** alone helps with [GI](#gloss-gi) and [AA](#gloss-aa). Both apply to exact phrases and to highlights.

**No matches** shows a yellow box naming your search, suggesting you untick a box if one is ticked.

#### Finding your way around the table of contents {: #toc-howto}

*Search terms: outline, navigation, open all, close all, go back, return, back button, previous page, forward.*

The table of contents opens one level at a time, so even the biggest Parts are easy to get into.

- **Click ▸** beside a title to show the next level (each still closed).
- **Double-click the ▸ arrow** to open everything below that title at once, at every depth.
- **Click the ▾ arrow** of an open title to close it again; double-clicking ▾ closes it along with everything below it.
- **Click a title itself** (not the arrow) to jump to that part of the manual.
- **Expand all** and **Collapse all**, beside the "Contents" heading, open or close everything; **Collapse all** leaves just the main titles.

<span id="manual-back"></span>**Getting back to where you were.** The manual opens in NuMa's window, under NuMa's menu. The yellow bar above the manual has two buttons, for two different needs:

- **↩ Return to …** (or **Alt+Shift+U**) takes you straight back to the NuMa page you opened the manual from, in one step, however many places you've jumped to inside the manual. The button names that page: *Return to the meal*, *Return to Recipes*, and so on. The manual remembers the section you were reading, so the next time you choose **Manual** from the menu it opens right there. (A **Learn more** link opens the section it points to instead.)
- **← Back one step** (or **Alt+←**) undoes your last jump inside the manual: following a link, a search result, a contents entry or a bookmark. Press it again for the jump before that. Once there are no jumps left, it takes you back to the page you came from. **Alt+→** goes forward again.

Use **Back one step** to retrace your path through the manual, and **Return** when you're done reading and want to get back to work.

As you read, the list opens just far enough to show where you are, with the current section highlighted.

A "How to use this list" box at the end of the list can be hidden with **Got it — hide this**, and brought back with the link beside "Contents".

#### Bookmarking sections of this manual {: #bookmarks-howto}

*Search terms: save place, favorites.*

Bookmark any section to come back to it. The buttons are in the sidebar, between the search box and "Contents".

- **Bookmark this section** bookmarks the one you're reading (named last in the bar at the top); in a bookmarked section it reads **Remove this bookmark**.
- **Bookmarks (N) ▾** lists them in manual order, with where each sits; click one to go there.
- **×** removes one; **Clear all bookmarks** removes all, after asking.
- In the table of contents, **★** marks a bookmarked section, **☆** a title with a bookmark inside it.

Bookmarks are kept by your browser on this computer, and survive manual updates; one whose section was removed is marked so you can clear it.

## Part 5 — Skills used everywhere {: #skills}

*(Reading time: 27 minutes)*



Things that work the same way on many pages, explained once here and linked from each page that uses them.

### A. Entering amounts in meals and recipes {: #amount-formats}

*Search terms: portion formats, how to type an amount, quantity, measurements, units, ounces, cups, tablespoons, teaspoons, fractions, weighed, grams and cups together.*

Every box that asks how much of a food or recipe (a meal's **Amount**, a recipe ingredient, **Convert**, Compare, What-if, **Add to every meal**) reads amounts the same way.

**What NuMa does with what you type.** It works out one number, grams for a food or servings for a recipe, which every total and check uses. It also keeps your text, lightly tidied ("2T" becomes "2 T", "2 T 15 g" becomes "15 g (2 T)"), and shows it wherever the amount appears; an **Edit** box shows that text, and saving it unchanged changes nothing. If NuMa can't read something, it refuses the whole amount and says why, never using part of it.

#### At a glance {: #amounts-at-a-glance}

| You type | NuMa reads it as | Shown as |
|---|---|---|
| `150` or `150 g` | 150 g (a number on its own is grams) | 150 g |
| `150g`, `3oz`, `2T` | the same as with a space | 150 g, 3 oz, 2 T |
| `3 oz`, `0.5 lb`, `1 kg` | converted to grams | as typed |
| `1/4 cup`, `1 1/2 c`, `2 T`, `1 tsp`, `100 ml`, `1 fl oz` | converted to grams with the food's own cup or spoon weight, or a [generic density](#gloss-generic-density) (marked **≈ generic**) | as typed |
| `½ cup`, `1½ c`, `¾ tsp` | the same as `1/2 cup`, `1 1/2 c`, `3/4 tsp` | |
| `1,000 g`, `12,5 g` | 1000 g; 12.5 g (a decimal comma is read as a point) | |
| `2 tbsp.`, `3 oz.`, `2 tbs`, `1 fl. oz` | trailing periods and common spellings are understood | |
| `2/3 c 134.1 g`, `2 T 15`, `1 c 2 oz` | a measure you weighed: the weight counts, the volume is kept as a label | 134.1 g (2/3 c) |
| `134.1 g (2/3 c)`, `50 g (1 slice)` | a weight with a note in brackets: the weight counts, the note is kept as typed | as typed |
| `p1`, `2 p1`, `1.5 p2` | the food's 1st portion, twice its 1st, one and a half times its 2nd | 1 large egg, 2 × 1 large egg |
| `1 large egg`, `2 eggs`, `3 slices`, `2 tablets` | a count of one of the food's own portions, matched by name | 2 × 1 large egg |
| `1 serving`, `1 1/8 srv` (a recipe) | servings of the recipe | 1.125 servings |
| `200 g`, `200`, `3/4 c` (a recipe) | turned into servings through the recipe's serving weight or volume — see [Recipes](#portions-vs-servings) | servings |

#### Numbers

Plain numbers, decimals, fractions and mixed numbers all work, as do the fraction characters ½ ¼ ¾ ⅓ ⅔ ⅛ and the rest:

    150        plain number
    0.5        decimal
    1/4        fraction
    1 1/2      mixed number (whole number, a space, then a fraction)
    1½         the same as 1 1/2

A number on its own is grams, for a recipe too, except for a [supplement](#supplements) stored per tablet, where `2` is two tablets.

#### Weights

    g  gr  gram  grams          grams
    oz  ounce  ounces           ounces     (1 oz = 28.35 g)
    lb  lbs  pound  pounds      pounds     (1 lb = 453.6 g)
    kg  kilogram  kilograms     kilograms  (1 kg = 1000 g)

A weight is the most accurate entry: used exactly as typed, never marked as an estimate, and never changed by later edits to the food's portions.

#### Volumes (cups and spoons)

    c  cup  cups                       cups          (1 c = 236.6 ml)
    T  tbsp  tablespoon  tablespoons   tablespoons   (1 T = 14.8 ml)
    t  tsp  teaspoon  teaspoons        teaspoons     (1 t = 4.9 ml)
    ml  milliliter  milliliters  cc    milliliters
    floz  fl oz                        fluid ounces  (1 floz = 29.6 ml)
    l  liter  liters                   liters        (1 l = 1000 ml)

`T` (capital) is a tablespoon and `t` (small) is a teaspoon. Those two are the only units where capitals matter.

A volume has no weight, so NuMa converts it to grams using, in order:

1. **The food's own cup or spoon portion**, including one you added: a fact about that food, so the one to trust.
2. **A [generic](#gloss-generic) density for that kind of food** (flours, protein powders, seeds, dried herbs and spices…).
3. **0.45 g per milliliter**, typical of a ground spice, when nothing better is known. A volume is never refused, since spices are often only measured by the spoon.

The second and third are guesses, marked **≈ [generic](#gloss-generic)** ([why](#generic-density)). For a teaspoon of spice it hardly matters; for a cup of flour it can be well off. Weigh a cup or spoonful once and add it as a portion (Food Cache → **Portions**): later volumes come out right, and earlier ones appear under [Amounts that no longer match](#stale-amounts) to correct.

#### A weight and a volume together {: #weight-and-volume}

When you've weighed something you also measured (2/3 cup of flour that weighed 134.1 g), record both in one box. The weight counts; the volume is kept beside it. Two ways to type it:

- **Volume, then weight:** `2/3 c 134.1 g` (or `2/3 c 134.1`), shown and stored as `134.1 g (2/3 c)`.
- **Weight, then a note in brackets:** `134.1 g (2/3 c)`, the form NuMa shows. The note is kept as typed and not checked, so it can be anything: `50 g (1 slice)`, `120 g (1 cup, packed)`.

Two near-misses are refused rather than guessed at:

- `134.1 g 2/3 c`, without brackets: NuMa can't tell a note from a typo, so asks for brackets.
- `2/3 c (134.1 g)`, weight in brackets: older versions wrote their own estimates that way, so it doesn't count as weighed. Type `2/3 c 134.1 g`.

An amount with its own weight is never marked **≈ [generic](#gloss-generic)** or listed under [Amounts that no longer match](#stale-amounts). (A weight in the amount and the volume in the item's **Notes** works too, but is no longer needed.)

#### A food's own portions: `pN` and counting by name {: #portion-shortcuts}

Many foods have named portions, from [USDA](#gloss-usda) or added by you: "1 large egg", "1 cup, sliced", "1 tablet". Every amount box lists them, each with its shortcut:

    p1         the food's 1st portion
    2 p1       twice its 1st portion (also 2p1)
    1.5 p2     one and a half times its 2nd portion

You can also type the description (`1 large egg`), a count (`3 large eggs`), or just its main word (`2 eggs`) when only one portion has it. NuMa shows `2 × 1 large egg`.

**`p1`, `p2`, … mean the food's 1st, 2nd… portion in its list, never a portion's name.** A custom portion *named* `p1` that's fourth in the list is `p4`. Check the list before typing; adding, removing or reordering portions renumbers them ([details](#ts-portion-numbering)).

There's no general count unit (`2 pc`, `2 pieces`), since NuMa can't know what a piece weighs. Give the food a portion for one ("1 slice", 28 g) and count it by name.

#### Recipes: servings instead of `pN` {: #portions-vs-servings}

*Search terms: recipe servings, servings not pN, sub-recipe amount.*

Recipes have no `p1`, `p2`… list, and don't need one: `pN` saves weighing a food, but a recipe is already measured in **servings**, so `1 serving` (or `1 srv`) says it directly.

**A recipe's amount can also be a weight or volume**, on a meal page and for a sub-recipe on Edit Recipe: servings (`1.125 srv`, `1 1/8 servings`), a weight (`200 g`, `8 oz`, or `200`), or a volume (`3/4 c`, `250 ml`). NuMa turns a weight into servings by the serving weight, and a volume by the recipe's **Total yield volume** or, failing that, a **Serving description** that's a measure (`2/3 cup`: so `3/4 c` is 1.125 servings). The hint under the box says which this recipe can take; if it can't convert, it says why and adds nothing. Servings are what's recorded and shown (`1.5 servings`).

A recipe's serving weight comes from **Number of servings** and **Total yield weight** on Edit Recipe: 21 servings from 1,942.5 g makes 92.5 g per serving, wherever the recipe is used.

(On Convert only, `p1` for a recipe means its one serving.)

**Serving description**, beside Number of servings, gives the serving a real-world name: 1 muffin, 1 slice. It's a label, except that a measure (`2/3 cup`) lets a meal convert volumes, as above. It appears as "(1 serving = 1 muffin)" wherever the recipe's servings are shown. When you add the recipe to a meal, the hint under the Amount box also gives one serving's weight, if it's known ("1 serving = 1 muffin, 85 g"), or the weight alone if there is no description ("1 serving = 24 g").

**Where you see the weight.** Servings are shown with grams, "2 servings (500 g)", on screen and in print, from the Total yield weight or else the ingredients added up, but only if every ingredient has a weight (a partial sum would mislead).

See also [Recipe Ingredient List](#recipe-ingredients).

#### Refused, with the reason

*Search terms: error, rejected, invalid amount, not accepted, won't save.*

Nothing is added or changed, your text stays in the box, and the message says what couldn't be read:

- `2 bananas` for a food with no portion called banana — the message lists the food's portions (`p1 = 1 medium banana`…) so you can pick one.
- `2 eggs` when the food has both "1 large egg" and "1 small egg" — NuMa won't guess; type `2 large eggs` or `2 p1`.
- `2 pc`, `3 pieces` — there's no general count unit; see above.
- `2 T 15 bananas` — whatever follows a volume must be a weight.
- `134.1 g 2/3 c`, `134.1 g banana` — whatever follows a weight must be a note in brackets: `134.1 g (2/3 c)`.
- `2/3 c (134.1 g)` — type it as `2/3 c 134.1 g` (see [A weight and a volume together](#weight-and-volume)).
- `p7` for a food with only three portions — "No preset p7 for this food."
- `200` for a recipe whose serving weight NuMa doesn't know — give it a Total yield weight, or type servings.

#### Practical compromises: dry pasta, weighed dry {: #dry-weight-compromise}

*Search terms: uncooked, cooked weight, dried, water weight, noodles, spaghetti, grains, rice, oats, beans, lentils, workaround.*

Sometimes the "right" food profile is hard to use, and a compromise works as well. Cooked-pasta profiles are scarce, and cooked weight depends on shape and cooking time; dry pasta profiles are everywhere, and dry pasta is easy to weigh.

**Weigh the pasta dry and use a dry pasta profile.** It's as accurate as a cooked profile with a cooked weight, usually more.

**The weight and the profile must match.** Cooking adds water, not calories or protein: 100 g dry becomes about 230 g cooked. Per 100 g, [USDA](#gloss-usda) lists dry enriched pasta at 371 calories and 13.0 g protein, cooked at 158 and 5.8. A cooked weight with a dry profile counts more than twice what you ate. If you forgot to weigh it dry, cooked weight × 0.43 is close, though less exact.

**Protein quality is the same either way**: [DIAAS](#gloss-diaas) is per gram of protein, so water doesn't change it. (A little of some B vitamins goes into the cooking water.)

The same goes for rice, oats, dried beans and lentils. Putting "dry" or "cooked" in the food's name ([Renaming a food](#rename-food)) helps later.

### B. Data entry: what you can type, and data errors to catch {: #data-entry}

*Search terms: typing values, input rules, form errors.*

*Every data check NuMa runs afterwards: [Checking your data](#checking-your-data).*

**NuMa reads what it can, tells you when it converted something, and refuses, by name, anything it can't read.** Nothing is silently dropped; if a form can't be saved, what you typed stays, with a list of what to fix.

#### Amounts — in meals, recipes, a food's page, Convert and Compare

See [Entering amounts in meals and recipes](#amount-formats).

#### Nutrient values — custom food profiles, and Settings → 5. Nutrient Targets - Researched

| You type | NuMa reads it as |
|---|---|
| `18` | 18 in the box's own unit (shown beside it) |
| `18 mg`, `0.018 g` (in an mg box) | 18 mg — converted, and named in a note |
| `2.4 µg`, `2.4 ug`, `2.4 mcg` | micrograms, however written |
| `400 IU` ([IU](#gloss-iu)) vitamin D | 10 mcg; `5000 IU` vitamin A = 1500 mcg RAE (retinol activity equivalents); `30 IU` vitamin E = 20.1 mg |
| `1046 kJ` calories | 250 kcal |
| `1,200`, `2½`, `12,5` | 1200, 2.5, 12.5 |
| `trace` | 0, noted |
| `-`, `n/a`, `—`, blank | left empty |

**Refused, with the reason:**

- `400 IU` in any box but vitamins A, D and E — IU means something different for each vitamin, so NuMa only converts the three it can.
- `10%` — a percent of daily value can't be turned into an amount reliably; enter the amount from the label.
- `<0.5` — a limit, not an amount; enter `0` or a figure.
- `-3` — negative.
- `3 cups` or `250 g` in a calories box — not a unit for that box.

**A pasted amino acid table** (Edit Custom Profile → **Paste an amino acid table**): one amino acid per line, name then figure (`Lysine 5.2`, `Leucine: 7.9`, or two spreadsheet columns). Choose the unit; per-protein figures use the Protein box, so fill that first. Untracked amino acids (arginine, alanine…) are skipped and named; an unknown name, a line without a number, or a repeat is refused.

#### Data errors NuMa can't catch for you

*Search terms: common errors, per serving vs per 100 g.*

Some mistakes give a perfectly readable number, so no form can refuse them. Watch for:

- **Per-serving figures in per-100 g boxes.** "Protein 6 g per 30 g serving" is 20 g per 100 g; typing 6 makes the food a third as nutritious. (In [supplement mode](#custom-foods) you do type per tablet.)
- **The wrong unit.** Sodium "0.4" as mg when the label says 0.4 g is a thousandfold error. Type the unit (`0.4 g`) and NuMa converts.
- **A slipped decimal point.** `100` for `10.0`. Foods → 9 catches impossible values, not merely unlikely ones.
- **A wrong portion weight.** A "cup" that's really half a cup makes every `1 c` wrong; fixing it lists affected amounts under [Amounts that no longer match](#stale-amounts).
- **The wrong food.** An ingredient line keeps its name even if linked to a different food ([details](#food-edit-consequences)).

After you save a food, its page shows any problem NuMa can see; [Checking your data](#checking-your-data) lists every check.

### C. Setting up a Food or Recipe search {: #search-ranking}

*Search terms: search order, search ranking, search by code, result order, best match, partial word, exclude, not, leave out, without, hidden matches, cooked, canned, preparation words, word order, reverse, search again, branded products.*

**Searching by code.**{: #search-by-code} Every food and recipe search box also takes a [code](#gloss-code): **[R21](#gloss-code)** for a recipe, **U171477**, **[UD4](#gloss-code)** or **[OFF3](#gloss-code)** for a food, **U171477.1** for an older version of one (any case). The search then shows just that item, at once and offline, whatever the Source boxes say, even if archived. A plain number works when it's the [FDC ID](#gloss-fdc-id) of a food in your Food Cache. A code or number NuMa has nothing for is searched as ordinary text, so an FDC ID you haven't used still finds the food online. A hint under each search box sums up word order, `!` and codes, linking to [Word order matters, too](#search-word-first).

Boxes that *filter a list* take a code too (the Recipes list, Food Cache, Annotate, **Filter my pantry list**, the Food Use filters and "Replace it with" box, and [Search meal history](#meal-history), where a code lists every meal with that item): a code narrows to that one item; anything else filters by name, and `!` words [leave names out](#search-exclude).

The rest of this section is about the order results come in.

**The short version:** results are ranked first by how many of your words appear in the name: all of them beats some, which beats none. A word counts only where a word in the name starts with it: "orange" matches "Oranges", "onions" matches "Green onion", "berry" matches "Berries" (singular and plural find each other), but "raw" in "st**raw**berry" doesn't count, nor "sauce" in "applesauce". Your own matches come before online ones, under "From your recipes, pantry, and food cache", in best-match order (a recipe goes ahead of a food only when both match equally well). When one of your items matches every word, your items matching only some move below the online results, under "Partial matches from your recipes, pantry, and food cache".

**Word order matters, too.**{: #search-word-first} NuMa takes the words you type first as the ones that matter most. Search `milk dry instant` and, if nothing matches all three, a match on `milk` + `dry` beats one on `milk` + `instant`, because you typed "dry" first. So put your most important word first when a name might be ambiguous.

**Excluding words.**{: #search-exclude} Put `!` before a word to drop every result whose name has it: `beans red !kidney cooked` finds cooked red beans that aren't kidney beans; `beans !kidney !pinto` drops both. An excluded word matches the way a searched one does, doesn't affect ranking, and isn't sent online. A search of only `!` words shows nothing; a list filter of only `!` words (`!kidney`) keeps everything else. When `!` words hide results, a line says how many ("6 matches hidden by `!kidney`"), so a source showing nothing isn't mistaken for one that found nothing. (In [USDA](#gloss-usda) every cooked red bean is a kidney bean, so `beans red cooked !kidney` shows no USDA rows.) It works in every food and recipe search box and every list filter.

**Trying the words in another order.**{: #search-word-order} [USDA](#gloss-usda)'s search strongly favors names holding your words *in the order sent*. Branded products are named as people talk ("small red beans"), the reverse of most-important-first, so `beans red small` misses many that `small red beans` finds. So after a search including USDA, the end of the results offers your words reversed, in a box you can edit. **Add its results below these** (the default, offered when the first search found something in USDA) adds what the second search found, under *Also found by searching ...*; **Replace these results with its results** searches for it instead. Your `!` words apply to both. NuMa doesn't run it by itself, since it's another request to USDA.

**Preparation words.**{: #search-prep-words} Words like *cooked*, *raw*, *boiled*, *canned*, *frozen*, *dried*, *chopped* count toward ranking, but aren't sent to USDA, Open Food Facts or the Canadian Nutrient File, which keep only names holding every word: a can of beans is cooked, but its name says "canned" or nothing, so "cooked" would leave it out.

**Ties go to the better data.** When results match equally well, Foundation and [SR](#gloss-sr) Legacy foods come first, then Survey/Experimental, then Branded and Open Food Facts, and only then shorter names. So a reference food likely to have amino acid data comes before a dozen branded look-alikes.

**Your own data is always checked first.** Matches in your Food Cache and Pantry appear at once; online results follow a moment later, and the whole list is then ranked together, so a better online match can move ahead of a weaker one of yours. A 12- or 13-digit barcode ([UPC](#gloss-upc)-A or [EAN](#gloss-ean)-13) goes straight to an Open Food Facts lookup.

**Search result depth.** Plain foods, the likeliest to have amino acid data, can be buried under branded and prepared ones: USDA can rank "Potatoes, flesh and skin, raw" 15–20 deep for "potato". So NuMa runs a second search of Foundation and SR Legacy foods only. **Settings → 6 → Search result depth** sets how many it fetches: 25 by default; more if you still miss a food; 0 for no limit (slower).

### D. Data editing: what changes when editing recipes, meals, or the food cache {: #editing-consequences}

*Search terms: editing consequences, recalculation.*

*How NuMa shows you the effect of a change, including on past days: [Seeing what a fix changed](#data-effects). Every data check: [Checking your data](#checking-your-data).*

**Changes to nutrient data carry through everywhere; amounts you've already typed don't change.** Edit a food's nutrients, or a recipe's ingredients or servings, and everything built on it (other recipes, meals, past days, lists, summaries, averages, plots) is updated by itself. An amount already entered was saved as grams, so a later portion edit leaves it alone; Foods → 9 lists the ones worth a second look.

| You change… | Recipes that use it | Meals that log it, past days included | More |
|---|---|---|---|
| **A food's nutrients** — editing them, copying from another food, estimating amino acids, refreshing from [USDA](#gloss-usda), importing Claude's answer, merging duplicates | Recalculated at once, and every recipe built on those too | Recalculated by the next page you open | [Editing or changing a food](#food-edit-consequences) |
| **A food's portions** (`p1`, a cup weight) | No change — amounts keep the grams they were entered with | No change, for the same reason | [Amounts that no longer match](#stale-amounts) |
| **A food's [GI](#gloss-gi)** (Foods → Annotate) | Recipe glycemic load follows at once — it's worked out fresh each time it's shown | Same, for meals and days | [Glycemic Load Output](#glycemic) |
| **A food's name** | The new name replaces the old one on every ingredient line that uses the food; nutrients unaffected | Same, and in your pantry | [Editing or changing a food](#food-edit-consequences) |
| **Deleting a food** | Refused while any recipe, meal or pantry entry uses it | Refused | [Editing or changing a food](#food-edit-consequences) |
| **A recipe's ingredients or amounts** | That recipe recalculated, and every recipe built on it | Recalculated by the next page you open | [Changing a recipe…](#recipe-dcp-cascade) |
| **A recipe's Number of servings** | Per-serving figures change, and cascade as above | A meal logs servings, so "1 serving" now means the new serving; the meal page flags the item and asks whether to keep the grams you ate | [What changes in servings or yield weight affect](#servings-yield-effects) |
| **A recipe's Total yield weight** | No nutrient change (except water, if the recipe has a cooked water figure); only what a serving weighs | No nutrient change until you choose; the meal page flags the item and asks whether to keep the grams | [What changes in servings or yield weight affect](#servings-yield-effects) |
| **A recipe's name** | The new name replaces the old one everywhere | Same | [Editing or changing a food](#food-edit-consequences) |
| **Deleting a recipe** | Refused while any recipe or meal uses it; Archive instead | Refused | [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) |
| **Substituting** one food or recipe for another everywhere | Ingredients switched and recalculated, cascading up; amounts kept as typed | Items switched; amounts kept as typed | [Replace a Food or Recipe Everywhere](#fooduse-substitute) |
| **A what-if** | Nothing, unless you click Apply | Nothing, unless you click Apply | [Saving, downloading and applying a what-if](#whatif-apply) |
| **Your profile** (weight, targets) | — | Past days keep the profile they were pinned to | [Per-Day Profile Tracking](#day-profile) |

A meal's or recipe's page always works its figures out fresh. What's described below is how NuMa keeps the figures it *saves* for lists up to date: each recipe's [DCP](#gloss-dcp) per serving, and each meal's DCP, calories and nutrient totals, used by Meals & Log, Recent Days, averages and the Nutrient Plot. For where NuMa fills in *missing* data, see [Where NuMa fills gaps](#filling-gaps).

#### Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it {: #recipe-dcp-cascade}

*Search terms: nested recipe, recalculate parent recipe, update dependent recipes.*

A recipe can be an ingredient of other recipes (a lentil sauce in three dinners). Saving it recalculates its [DCP](#gloss-dcp) and that of every recipe built on it, directly or through others, so nothing built on it goes stale.

**Meals follow too:** every meal logging it, or a recipe built on it, is recalculated by the next page you open.

**Recompute DCP for all recipes**, on the Recipes list, is for after a bulk import.

#### How a meal records a recipe: servings, with grams when they're known {: #recipe-servings-grams}

*Search terms: recipe servings, grams per serving, serving weight.*

A meal records *servings* of a recipe, not grams, because a serving is always defined but a recipe's weight often isn't: cooking adds or removes water, and some ingredients have no weight ("4 t cumin, weight not known").

Wherever meal items are listed, a recipe shows its servings and, when known, grams: **1 serving (295 g)**. One serving's weight comes from:

1. the recipe's **Total weight**, if entered: the most reliable, since you weigh the finished dish;
2. otherwise its ingredients added up, if *every* one has a weight.

Otherwise it reads **1 serving (weight unknown)**. The nutrients are still right, since they're worked out per serving. Enter the Total weight to see grams.

**If a recipe's serving size changes after you've logged it, NuMa asks what you meant.** Change 8 servings to 4 and each serving is twice the food, so a meal's "1 serving" would count double. NuMa remembers what a serving weighed when logged; if that changes, the meal page shows a yellow note with two buttons:

- **Keep the 295 g I logged** — adjusts the servings (to 0.5 here) so the meal holds what you ate. Usually right when the number of servings changed; after a corrected Total yield weight it depends on how you entered the amount (see [below](#servings-yield-effects)).
- **Use the new serving size** — keeps "1 serving", for when the old size was wrong.

Day pages and Meal History Search flag the item too. Differences under 1% are ignored; it only works when both weights are known. Typing a new amount for the item also settles it.


#### What changes in Number of servings or Total yield weight affect {: #servings-yield-effects}

*Search terms: cooked weight, raw weight, batch weight, portion size, yield, recipe weight correction.*

On Edit Recipe, **Number of servings** and **Total yield weight** together say what one serving is: how many portions the finished dish is divided into, and what the whole dish weighs. One serving weighs the total divided by the number of servings (1,200 g in 4 servings: 300 g each). The two fields affect different things.

**Changing Number of servings changes the nutrients in a serving.** The recipe's nutrients are its ingredients' total divided by the number of servings, so going from 8 servings to 4 puts twice the nutrients (and twice the weight) in each serving. That reaches:

- **The recipe itself:** every per-serving figure on its page (nutrients, calories, [DCP](#gloss-dcp)).
- **Recipes that use it as an ingredient:** they record it in servings, so their nutrients change too, and so on up the chain.
- **Meals that logged it:** a meal records servings, so its "1 serving" now holds the new amount, and the meal's nutrients change. Each such meal page shows a yellow note asking whether to keep the grams you logged instead ([How a meal records a recipe](#recipe-servings-grams)).

**Changing Total yield weight changes only what a serving weighs, not its nutrients.** The ingredients and the number of servings are the same, so the nutrients in a serving are the same. Correcting a raw weight to the cooked weight (often about half, as water cooks off) means each serving is the same food in less weight. What changes:

- **The grams shown beside servings** everywhere: "1 serving (148 g)" instead of "(296 g)".
- **Turning a weight into servings from now on:** typing `200 g` of the recipe on a meal or Edit Recipe now means more servings, since each serving weighs less.
- **Water,** but only if the recipe page has a cooked water figure (g per 100 g of the finished dish): NuMa multiplies that by the total weight, so the water in a serving changes with it.
- **The weight of recipes that use it,** when their own weight is worked out from their ingredients. Their nutrients don't change.

**Meals you already logged keep their nutrients, until you choose.** A meal records servings, not grams, so a new weight alone changes nothing in it. But the serving now weighs something different from when you logged it, so each meal page that has the recipe shows the yellow note with two choices. NuMa doesn't know how you entered each amount, so it's for you to say:

- **You logged it in servings** ("1 serving", one bowl of four): choose **Use the new serving size**. The servings, and the nutrients, stay as they are; only the grams shown change. This is right because the serving you ate was always that share of the dish.
- **You weighed it and typed grams** ("200 g"): choose **Keep the … g I logged**. NuMa turned your 200 g into servings using the old weight, which was wrong, so the meal holds too little (or too much) of the recipe. Keeping the grams works the servings out again with the corrected weight, and the meal's nutrients change to match: halving the yield weight doubles the servings in 200 g, and so the nutrients.

**Settling them all at once.** After a change to either field, the recipe's page and Edit Recipe show a yellow box saying how many meal items and recipe ingredients were entered at the old serving weight, with **Review them**. It opens a list of every one of them: each meal (date and name) and each recipe that uses this one as an ingredient, with what one serving weighed then and now, and two choices side by side, **Keep the grams** (the servings this works out to) or **Keep the servings**. Tick one in each row, or use **For every row** to tick the same everywhere, and click **Apply these choices** (there's one above the list and one below). Nothing is saved until you do: a row with neither ticked is left as it is and stays listed, and if you try to leave the page with choices ticked but not applied, NuMa asks first. The meals and recipes you settle are worked out again at once. The same list opens from **Settle every meal and recipe that uses it at once** in a meal page's yellow note.

**On Daily Summary**, a box above the table lists every meal, on any date, that holds a recipe whose serving weight has changed since it was logged, with a **Settle** button for its recipe, and a ⚠ beside each affected day in the table. The box goes once every such meal is settled.

Recipes used as ingredients are checked the same way: NuMa records what a serving weighed when you added the ingredient, or last changed its amount.

#### Editing or changing a food: nutrients, portions, amounts, name {: #food-edit-consequences}

*Search terms: edit food, rename food, change nutrients, food changes.*

**Editing a food's nutrients updates every recipe and meal that uses it**, however you edit them ([copying from another food](#drafted-foods), estimating amino acids, refreshing from [USDA](#gloss-usda), importing Claude [AI](#gloss-artificial-intelligence)'s answer): [DCP](#gloss-dcp) is recalculated for every recipe using it, and everything built on those, and every meal.

**Editing a food's portions changes nothing already entered.** Every amount becomes grams when you type it:

- **`p1`, `1.5 p1`** — that portion's weight *as it is now*; the line saves the portion's description ("1 cup, chopped"), not `p1`.
- **A volume** (`1/4 cup`) — converted by the food's density, the volume kept as a label ("52.3 gr (1/4 cup)"). Without a known density, NuMa asks for a weight.
- **A weight, like `3 oz`** — converted straight to grams.

What that means when you edit a portion afterwards:

- **Nutrient totals don't change.** Past recipe ingredients and logged meal items keep the grams they were entered with.
- **A recipe's ingredient label is a record**: change `p1` from "1 cup" to "1 large" and old lines still say "1 cup".
- **A meal item keeps what you typed too** ("41.8 g (1/3 c)"); items entered before October 5, 2026 kept only grams.
- **Editing an amount re-reads it** against today's portions.

If a portion's weight was wrong, fix the portion; Foods → 9 then lists the amounts that used it under [Amounts that no longer match](#stale-amounts).

**Renaming a food renames it everywhere**{: #food-rename}: every recipe line, meal item (past days too) and pantry entry, and the page says how many. Nutrients don't change, since they come from the food a line is *linked* to. One exception: NuMa estimates protein digestibility from the name ([how](#digestibility-by-name)), so dropping a telling word ("tofu", "lentil") can change DCP; a digestibility you set moves with the name. A name typed in an ingredient line's **Edit** pop-up is replaced too; that pop-up only changes the shown name, never the linked food. If a recipe's nutrients look wrong, check each line is linked to the food its name says; to relink, remove the line and add the right food.

**Deleting a food.**{: #delete-food} **Delete this food** is on the food's page (second row of buttons); Food Search, Food Cache and Foods → 9 have **Delete** on each row. **A food still used by a recipe, meal or your pantry can't be deleted**, so nothing is left pointing at nothing. Recipes work the same way ([details](#delete-recipe-elsewhere)).

#### Meals and days {: #meal-edit-consequences}

*Search terms: meal totals, day totals, recalculate meals.*

A meal's or day's page always works everything out fresh; the figures saved for lists are updated automatically after any edit. **Calculate**, on [Meals & Log](#meal-columns), is for after a bulk import or for meals saved before October 2026. A recalculation that fails is reported under [System Issues](#system-issues-howto).

### E. Where NuMa fills gaps: estimates and estimation {: #filling-gaps}

*Search terms: missing values, generic values, filling in.*

*To find the gaps themselves, see [Checking your data](#checking-your-data).*

Food data is never complete: many foods lack amino acid figures, and none records protein digestibility. Where a calculation needs a missing number, NuMa either estimates it from a small built-in list, or leaves the food out and says so. It never quietly saves a [generic](#gloss-generic) estimate into your data. Here is every place it estimates.

**Protein digestibility, for every food.**{: #digestibility-by-name} [DCP](#gloss-dcp) needs how much of each food's protein is absorbed, which databases don't record, so NuMa looks it up by name, in order:

1. your own figure, if you've entered one for that food ([Protein Digestibility Overrides](#dcp-overrides), Settings → 4);
2. a curated table of about 50 foods and food types, each with a published source;
3. a broad category estimate — isolated plant protein, legume, seed, nut, grain/cereal, or animal protein;
4. failing all of those, a default estimate of 0.82, a deliberately conservative figure for plant protein.

[Meal Protein Digestibility Analysis](#meal-diaas) marks which each food got: "~est" for a category or default estimate, "user" for your own. If you know a better figure for a food you eat often, add an override.

**Amino acids in complement suggestions.** A candidate food with no amino acid figures is matched by name against a built-in table of 25 protein sources (soy protein isolate, nutritional yeast, oats…), scaled to its protein, and tagged "(estimated)" or "([generic](#gloss-generic) estimate)" ([details](#comp-estimate)). It's never saved, and used *only* for suggestions, never in DCP.

**Amino acids you estimate yourself** with "estimate amino acids from another food" ([how](#drafted-foods)) *are* saved, with a note naming the source, and used everywhere like real data, since you chose the source. A [DIAAS estimate](#diaas-estimate-table) you record by hand is shown with the food but not used in DCP.

**Where NuMa leaves a food out.** A food with no amino acid figures, not covered above, is left out of DCP, which gets a footnote ("the true figure is at least this much"), and [Missing AA profiles](#missing-aa) lists it. A recipe ingredient under 1 g of protein (spice, oil, salt) is left out quietly; a bigger protein source without figures stops the recipe's DCP being saved, so it shows "NC" (not computed).

**Where NuMa shows "unknown".** A logged recipe's weight is shown only when it can be worked out ([details](#recipe-servings-grams)).

**Calories**, when a food has protein, carbohydrate and fat but none, are estimated (4, 4 and 9 kcal per gram), marked, and replaced by a real figure if one arrives; pages say what share of their calories is estimated ([Calorie checks](#calorie-checks)).

### F. Moving foods and recipes with CSV files {: #csv-transfer}

*Search terms: export, import, share recipes, share foods, spreadsheet, transfer, send to a friend, another computer.*

A [CSV](#gloss-csv) file (a plain spreadsheet file) carries foods, or a recipe, to another NuMa install: to share with a friend, or copy to a second computer. It isn't a backup: meals, pantry, profile and settings stay behind ([Backing up your data](#backup)).

#### Foods {: #csv-foods}

**To export,** click **Export [CSV](#gloss-csv)** on **Foods → Food Cache**. The file holds exactly the foods shown (filter first for some; **Show archived foods** to include those): one row per food, with its name, type, brand, serving size, notes, portions and every nutrient per 100 g.

**To import,** click **Import CSV**, pick the file and click **Review**. NuMa lists the foods it understood, and any rows skipped (no name, or no usable values). Then click **Import ... foods into cache**.

- **Every imported food is new**, with its own code; it never replaces one you have. A name you already have is marked **Possible duplicate**.
- **Imported foods are custom foods**, even ones from [USDA](#gloss-usda), so they can't be refreshed from USDA; search for a USDA food here instead to keep its link.
- **Only the food's data travels**: its [GI](#gloss-gi), [DIAAS](#gloss-diaas), oxalate match and drink or supplement setting stay behind.
- A food arriving with protein, carbs and fat but no calories has its calories [worked out](#calorie-checks) as usual.

#### Recipes {: #csv-recipes}

**To export,** click **Export [CSV](#gloss-csv)** on the recipe's page. You get a `.zip` holding `recipes.csv` (the recipe and every sub-recipe, at any depth) and `foods.csv` (every food in them), so the recipe arrives complete.

**To import,** unzip it, open **Recipes → Import CSV**, pick the two files, click **Review**, then **Import ... recipes**.

- **A recipe import reuses what you have.** A recipe with a name you already have is marked **Already have this** and left alone; an ingredient food with a matching name uses your food, even if the figures differ (capitals don't matter).
- **What travels:** name, description, servings, total weight, instructions, notes, and ingredients with amounts and notes. The introduction and serving description need re-entering.
- Each new recipe's [DCP](#gloss-dcp) is then worked out.

---

## Part 6 — Help and troubleshooting {: #feedback}

*(Reading time: 12 minutes)*



If something seems broken or confusing, the answer may well be below. Topics are grouped by how the problem *feels*, not by menu, and a few appear in more than one group. Skim the headings if nothing matches at first; if you're still stuck, [Getting more help](#quickhelp) says how to reach us.

### A. Getting help {: #help}

*Search terms: learn more links, support, where to find help.*

**On NuMa's pages**, **Learn more** links beside headings and results open the section of this manual that explains them. Technical terms link to the [Glossary](#glossary).

**In this manual**, the search box at the top of the sidebar finds sections by the words in them, and by everyday words they don't use; tick **Only show things you can do** when you want instructions ([how to search](#search-howto)). The table of contents lists everything, Part by Part.

**Still stuck?** The rest of this Part covers common problems. If none fits, [contact us](#quickhelp).

### B. Operating the program

#### The program crashes unexpectedly {: #ts-crash}

*Search terms: freeze, hang, not responding, internal server error, error log, restart after update.*

If NuMa crashes or freezes, nothing you saved is lost: every action is saved at once. Just restart it and carry on.

**A yellow "NuMa has been updated — please restart it" bar** means the program was updated while running (after **Update Now**), and some pages won't work until you quit NuMa (Ctrl+Q) and start it again. Running from source, the bar has **Restart NuMa now**, and the page reloads by itself where you were.

**Every error is written down.**{: #error-log} When a page fails with "Internal Server Error", NuMa records the details in `numa-errors.log` in its data folder (`%LOCALAPPDATA%\numa` on Windows, `~/.local/share/numa` on Linux). Send that file with a problem report. It stays small.

If a page seems frozen or won't load, refresh it; if that fails, restart NuMa.

Either way, [let us know](#quickhelp). This is beta software: a crash almost always means a real bug, not something you did.

#### You know what you want to do but can't see how to do it {: #ts-findit}

*Search terms: how do I, can't find feature, where is.*

Search this manual for a word describing what you're trying to do, not a menu name, with **Only show things you can do** ticked ([how](#search-howto)). If you still can't find it, [tell us](#quickhelp) in plain words what you were trying to do: that tells us whether the feature exists, is badly named, or isn't built yet.

### C. I don't understand...

#### A recipe's "Complete" checkbox doesn't match its protein-completeness score {: #ts-complete-confusion}

*Search terms: Complete checkbox, done editing.*

They're unrelated ideas sharing a word. The **Complete** checkbox ([Recipes list](#recipes)) is your own "I've finished this recipe" mark. A **complete** amino acid profile, every essential amino acid at or above its reference level, is part of the [DCP](#gloss-dcp) and [DIAAS](#gloss-diaas) analysis. A recipe can be one without the other.

*See also:* [DCP is capped or jumped in a way that doesn't add up](#ts-dcp-cap), [A food or recipe shows an "insufficient amino acid data" warning](#ts-missing-aa), [Oxalate or glycemic index data isn't showing](#ts-oxalate-gi).

### D. I'm confused — something unexpected happened

#### USDA searches got slow, or started failing {: #ts-usda-slow}

*Search terms: slow search, USDA failing.*

Without your own [USDA API key](#food-data), NuMa uses a shared demonstration key (`DEMO_KEY`), whose limit heavy use by anyone can exhaust, making searches fail for a while. A free personal key takes about a minute ([how](#food-data); enter it in Settings → 6).

#### A deleted recipe shows up as "(deleted)" somewhere {: #ts-deleted-recipe}

*Search terms: missing recipe, recipe gone, broken recipe link, reconnect.*

A recipe deleted by an older version, while still in use, leaves its lines flagged "recipe (deleted)", counting no nutrients. [Foods → 9](#db-check) lists them; create a recipe with the same or a similar name and NuMa offers to relink them ([details](#delete-recipe-elsewhere)).

*See also:* [I searched for a food I know exists and got nothing](#ts-search-empty), [The food I wanted wasn't at the top of the search results](#ts-search-order), [A meal's DCP isn't showing](#ts-meal-dcp), [A past day's numbers changed after I updated my profile](#ts-day-profile).

### E. I expected to see something, and it's not there

#### A food or recipe shows an "insufficient amino acid data" warning {: #ts-missing-aa}

*Search terms: no amino acids, AA missing, amino acid warning.*

Many foods, especially branded or prepared ones, have no published amino acid data. That's a data gap, not a bug. Search for a [USDA](#gloss-usda) Foundation or [SR](#gloss-sr) Legacy version (plain foods are far likelier to have it), then estimate the amino acids from a similar food, and last, ask Claude [AI](#gloss-artificial-intelligence) for the values. [Workflow 12](#fix-food-data) walks through all three. See also [Missing amino acid profiles](#missing-aa).

*See also:* [No brand or equivalent of a food has amino acid data anywhere in USDA](#ts-no-aa-anywhere), for the harder case where neither fix above applies.

#### No brand or equivalent of a food has amino acid data anywhere in USDA {: #ts-no-aa-anywhere}

*Search terms: no amino acid data anywhere, Claude AI, research amino acids.*

Here no brand and no generic [USDA](#gloss-usda) entry for the food has amino acid data, so there's no equivalent food to find.

Look instead for the *ingredient* that supplies most of the food's protein and has measured data: baked goods get their protein from the flour, a bean product from the bean. [Estimating amino acids from another food](#drafted-foods) turns that ingredient into an estimate for your food, scaled to the food's own protein.

If several ingredients supply the protein (a flour blend), blend their figures by weight first, and enter the blend as its own custom food: a **proxy food**, a scratch entry that only holds numbers to copy from. (Even for one ingredient, a proxy food is better than typing numbers into the real food; see below.)

Then choose one of two ways to apply it:

**Option 1 — a new, clearly labeled copy (the usual choice).** Copy the real food as a draft (**Copy a cached food as a draft**, or **Copy as custom-food draft** on a search result), name it plainly ("Graham Cracker, generic (estimated AA)"), and estimate its amino acids ([AA](#gloss-aa)) from the proxy food. The original stays untouched and refreshable from USDA, but meals and recipes already using the original keep using it until you switch them.

**Option 2 — estimate on the original food.** If you'll always log this exact product, estimating its amino acids in place means every past and future meal and recipe using it picks up the estimate at once. NuMa marks the food *user-edited*, remembers which values you changed, and keeps them through a **Refresh from USDA** unless you choose otherwise ([details](#review-incoming)); they're remembered as estimates, so real measured values can replace them later. It suits a branded product unlikely ever to gain amino acid data, such as Nabisco Honey Maid Grahams.

**Worked example: graham crackers, no AA data on any brand, made from a 2:1 white-to-whole-wheat flour blend. Nabisco Honey Maid Grahams specifically are already logged in past meals.**

Steps 1–3 build the proxy food; then follow one option.

Step 1 — the measured amino acid data for both flours (USDA Foundation/[SR](#gloss-sr) Legacy):

    Amino acid       White flour, per 100g    Whole wheat flour, per 100g
                      (protein 10.3 g)         (protein 13.21 g)
    Histidine         230 mg                    357 mg
    Isoleucine        357 mg                    443 mg
    Leucine           710 mg                    898 mg
    Lysine            228 mg                    359 mg
    Methionine        183 mg                    228 mg
    Phenylalanine     520 mg                    682 mg
    Threonine         281 mg                    367 mg
    Tryptophan        127 mg                    174 mg
    Valine            415 mg                    564 mg

Step 2 — blend them 2:1 by weight, per 100 g of blend:

    Amino acid       Blend, per 100g flour mix (protein 11.27 g)
    Histidine         272 mg
    Isoleucine        386 mg
    Leucine           773 mg
    Lysine            272 mg
    Methionine        198 mg
    Phenylalanine     574 mg
    Threonine         310 mg
    Tryptophan        143 mg
    Valine            465 mg

Step 3 — enter the blend as a proxy food (**Foods → Custom food profiles → Create**), named "Wheat flour blend, 2:1 white:whole wheat (proxy)", with Step 2's protein and amino acids.

**Option 1** (if the Grahams aren't logged anywhere yet, or you'd rather not change them):

Step 4 — **Copy a cached food as a draft** of the Nabisco Honey Maid Grahams entry; the copy has its measured protein, 6.8 g/100 g.

Step 5 — name the copy "Graham Cracker, generic (estimated AA)".

Step 6 — on the copy, use "estimate amino acids from another food" with the proxy food. NuMa scales by 6.8 ÷ 11.27 ≈ 0.60, giving:

    Amino acid       Estimated, graham crackers, per 100g (protein 6.8 g)
    Histidine         164 mg
    Isoleucine        233 mg
    Leucine           466 mg
    Lysine            164 mg
    Methionine        119 mg
    Phenylalanine     346 mg
    Threonine         187 mg
    Tryptophan        86 mg
    Valine            280 mg

Step 7 — keep the suggested note, and log graham crackers with this copy from now on.

**Option 2** (the better fit here, since the Grahams are already in past meals):

Step 4 — on the Grahams entry itself, use "estimate amino acids from another food" with the proxy food; the same 0.60 scaling gives the same table.

Step 5 — keep the suggested note. Every meal and recipe using the Grahams picks up the estimate at once.

**Either way**, it's an approximation that assumes all the protein comes from the flour: fair for a plain graham cracker, less so for a chocolate-coated one.

When you're done, delete the proxy food so it stays out of searches, unless you'll reuse it soon.

#### I searched for a food I know exists and got nothing {: #ts-search-empty}

*Search terms: nothing found, no results, search fails, can't find food.*

Try other words: "beans cooked" and "beans canned" find different things. Try your words in another order too ([why](#search-word-order)), or a [`!` word](#search-exclude) may be hiding it.

Check your **Dietary Preferences** (Settings → 3): "Plant-based only" or "Vegetarian" hides other foods from every search. Switch to "All animal foods" to search, then back. Also check that no Source box is unticked (a red **Omitted from search** note says so).

#### The food I wanted wasn't at the top of the search results {: #ts-search-order}

*Search terms: search order, wrong result first, word order.*

Usually it's word order: when results tie on how many of your words they contain, matching your earlier words wins, so `milk dry instant` favors "milk dry ..." over "milk instant ...". Put the word you care most about first ([how ranking works](#search-ranking)).

#### A meal's DCP isn't showing {: #ts-meal-dcp}

*Search terms: DCP missing, no DCP, meal DCP not showing.*

[DCP](#gloss-dcp) is worked out every time you add, edit or remove an item; you don't need to mark the meal complete. (Marking it **Complete** still matters: a day with an unmarked meal is flagged "provisional", since its total may change.)

If DCP is still missing, none of the meal's foods (or recipes) has amino acid data yet ([what to do](#ts-missing-aa)). Add it to one, and DCP appears.

#### Oxalate or glycemic index data isn't showing for a food {: #ts-oxalate-gi}

*Search terms: oxalate missing, GI missing, not showing.*

[Oxalate data](#oxalate) is off until you turn it on in Settings → 1. A [glycemic index](#gi) shows only once you've given the food one (from the reference table on its Annotate page, or typed); NuMa never fills one in itself.

*See also:* [A recipe's "Complete" checkbox doesn't match its protein-completeness score](#ts-complete-confusion).

### F. The numbers don't make sense

#### DCP is capped, or jumped in a way that doesn't add up {: #ts-dcp-cap}

*Search terms: DCP capped, numbers wrong, math wrong.*

This is the most common "the math looks wrong" report, and it's almost always right. [DIAAS](#gloss-diaas) isn't capped (it can exceed 1.0), but [DCP](#gloss-dcp) can never exceed the protein you absorbed, so it's capped there. A capped DCP is good news: none of your absorbed protein is wasted. [Full explanation, with an example](#dcp-cap).

#### A past day's numbers changed after I updated my profile {: #ts-day-profile}

*Search terms: past day changed, profile changed history.*

By default a day follows your current profile (its **current profile** switch is ticked), so saving a change re-scores it. To keep a past day as it was, untick its switch (on its Summary or Full Day page, or under its date on Meals & Log), or set its profile by hand with **Change** ([details](#day-profile)).

*See also:* [A deleted recipe shows up as "(deleted)" somewhere](#ts-deleted-recipe).

### G. A food's portion or serving-size data looks wrong

*Search terms: portion wrong, serving size wrong, bad portion data.*

Mostly this is a gap or error in the [USDA](#gloss-usda) data NuMa shows: USDA's nutrient values are reliable, but its portion records ("1 large", "1 cup, sliced") are uneven. The fix is to give NuMa the right value once; it's remembered. (The `pN` mix-up below is a NuMa rule, not a data problem.)

#### A food has no "per piece" or "per egg" portion — only grams {: #ts-no-piece-portion}

*Search terms: no portion, units missing.*

Some foods that come in natural units (an egg, a slice of bread) have no [USDA](#gloss-usda) portion for that unit, and NuMa can't guess one: USDA's egg sizes run from about 38 g (Small) to 63 g (Jumbo).

Weigh it and enter the grams, or add the portion once on its [Food Cache](#food-cache-web) entry's **Portions** page; then you can type `2 eggs` or `2 p1`.

#### A food has a weight portion but no cup/tablespoon equivalent {: #ts-no-volume-portion}

*Search terms: no cup measure, volume missing, seasoning.*

NuMa converts a volume to grams with the food's density, from a cup or spoon portion in its record (including one you added); failing that, a generic figure for that kind of food, or 0.45 g per mL ([details](#amount-formats)). Those guesses are marked **≈ [generic](#gloss-generic)** and listed on Foods → 9.

If you'll often measure this food by volume, weigh a level cup or tablespoon once and add it on the food's **Portions** page.

#### A food's portion or volume conversion looks flatly wrong {: #ts-bad-portion-data}

*Search terms: wrong portion weight, bad conversion.*

Sometimes a [USDA](#gloss-usda) portion weight is just wrong: a "1 large" egg that doesn't match the scale, a "1 cup" for a different preparation. NuMa shows USDA's figures as published.

Enter the grams you weighed, and replace the bad portion on the food's **Portions** page; your portions survive a **Refresh**. If you're sure USDA is wrong, [tell us](#quickhelp).

*See also:* [Enter amounts as weights, not volumes, whenever possible](#amount-formats).

#### A food's portion "pN" shortcut points to the wrong portion {: #ts-portion-numbering}

*Search terms: pN wrong, portion shortcut, p1 p2.*

`p1`, `p2`… mean the food's 1st, 2nd… portion *in list order*, never a portion's name. A portion you add, even one you call "p1", usually lands further down (`p3`, `p4`) after the food's existing portions, and typing `p1` then quietly uses a different portion.

Two ways to avoid this:

1. **Check the list beside the amount box**, which shows each portion's real shortcut (`p1 oz (14.2 g) · p2 1.75" square (3.0 g) · …`).
2. **Check again after editing portions**, which renumbers those after the change. (Amounts already entered are safe, saved as grams.)

*See also:* [A food's own portions](#portion-shortcuts). A copied custom food keeps the original's portions, so the same applies.

### H. Getting more help {: #quickhelp}

*Search terms: contact, support.*

This is extremely easy, and we want you to do it. When you're having a problem the cause is NOT necessarily you! Regardless of the nature of your problem, contacting us gives us essential information needed to make things better for you and also for every other user. We very much want to hear from you if you have a problem.

1. Text Tom at 435-272-3332. Plainly state that you are having a problem with the program. A brief statement of the problem is all I need. With your phone number I can call you back and get complete details of what I need to know to resolve your problem. I will generally call you back immediately. If you prefer a different time, let me know.

2. For non-urgent problems - which generally are improvements you'd like to see - you can also email me at [tomcloydmsma@gmail.com](mailto:tomcloydmsma@gmail.com). Provide screenshots, if you think that would help. ALWAYS TEXT ME IF YOU SEND AN EMAIL, as I do not check my email daily, and yours easily can get lost in the 100s I get every day.


**What to offer as "feedback":** First, ANY thoughts you wish to share are welcome. If in doubt, just do it! We'll be grateful. Of particular interest to us are these topics:

1. Inconveniences: you notice that something seems a bit difficult to do, or you see a simpler or quicker way to do it.
2. Missing or incomplete information: Sometimes updates and changes do not go out to every part of the program as they should, and you see a gap in the information provided.
3. Outright nonsense: you look at program output and think "that can't be right" or maybe you just feel doubtful about it.

User-derived issues get immediate priority in the program-development process!

---

## Part 7 — The science behind NuMa {: #coreNutrition}

*(Reading time: 2 hours, 34 minutes)*



### A. Protein {: #science-protein}

*Search terms: protein science, amino acids, protein quality, complete protein.*

Why protein quality matters, how NuMa measures it, and how it suggests complements. Start with the primer, which explains the whole subject in plain terms; the sections after it go into each idea in detail, and the chapter ends with a fully worked example you can check by hand.

#### Raw protein, protein quality, and protein digestibility {: #appendix-protein-quality}

##### The core problems with protein

*Search terms: protein quality basics.*

When you eat protein, not all of it is equally useful to your body. The usefulness depends on three things: **how much** protein you eat, and **how well-matched** its amino acid composition is to human physiological needs, and **how digestible** it is. 

##### The Nine Essential Amino Acids and their required relationship

Your body requires twenty amino acids to build proteins. Eleven of these it can synthesize from other raw materials. The remaining nine — the essential amino acids ([EAAs](#gloss-eaa)) — must come from food[^16].

These nine must all be present simultaneously for protein synthesis to proceed. They must also be present in the right amount. If any one of them is insufficiently supplied, then to the degree that its amount is short the other cannot be used. The surplus of the other eight cannot be stored and is instead broken down for energy — a functional waste[^110].

In summary, the *pattern* of [EAAs](#gloss-eaa) in a food matters, not just the total protein quantity.

##### The required EAA pattern, established by the FAO

*Search terms: FAO pattern, reference pattern.*

The Food and Agriculture Organization ([FAO](#gloss-fao)) of the United Nations leads international efforts to defeat hunger, achieve food security for all, and make sure that people have regular access to enough high-quality food to lead active, healthy lives.

Research has established human requirements for each [EAA](#gloss-eaa) independently, through controlled human trials. For each amino acid separately, researchers determined how much a healthy adult needs per day to maintain physiological function. From these studies came absolute daily requirement figures for each of the nine [EAAs](#gloss-eaa), expressed in milligrams per kilogram of body weight per day.

Separately, research has established how much total protein a healthy adult needs per day. By dividing each [EAA](#gloss-eaa)'s daily requirement by the total daily protein requirement, researchers produced a normalized figure: how many milligrams of each [EAA](#gloss-eaa) a person needs per gram of protein consumed. These normalized figures are the **[FAO](#gloss-fao) reference values**[^16].

From the reference values for each amino acid which were determined *independently* come the ratios between [EAAs](#gloss-eaa). The reference values' relationship are a byproduct of the separately established requirements — not the starting point.

##### The FAO reference values tell you about the quality of protein in a food

The reference values allow a simple and powerful question to be asked about any food protein source:

> If I eat enough of this food to meet my total daily protein needs, will each essential amino acid also arrive in sufficient quantity?

If the answer is yes for all nine [EAAs](#gloss-eaa), the protein is high quality — no bottleneck will limit your body's ability to use it. If the answer is no for even one [EAA](#gloss-eaa), that amino acid becomes your limiting factor.

##### How the Ratio Is Calculated in NuMa

For each essential amino acid, the ratio shown in [NuMa](#gloss-numa)'s output is computed in two steps:

**Step 1 — convert [AA](#gloss-aa) amount to mg per gram of total protein:**

    (AA content in g per 100g food ÷ protein content in g per 100g food) × 1000

This expresses how many milligrams of that amino acid are present for every gram of total protein the food contains.

**Step 2 — divide by the [FAO](#gloss-fao) reference value:**

    mg AA per g protein ÷ FAO reference value (mg/g protein)

A ratio of 1.0 means the food hits the reference exactly. A ratio of 2.14 means it delivers more than twice the required amount. A ratio of 0.80 means it delivers only 80% of what is needed.

**Concrete example — cocoa ([USDA](#gloss-usda) #169593, unsweetened dry powder):**

    Cocoa Protein total:      19.6 g per 100g food
    Tryptophan AA in cocoa:   0.293 g per 100g food

    Step 1:  (0.293 / 19.6) × 1000  =  14.9 mg tryptophan per g protein
    Step 2:  14.9 / 6.6             =  2.26

The [FAO](#gloss-fao) reference value for tryptophan is 6.6 mg/g protein (for anyone over 3 years old)[^16]. Cocoa's protein delivers 14.9 mg/g — 2.26 times what is required.

Think for a moment: what if cocoa contained none of the needed [EAAs](#gloss-eaa)? Then the protein it contained would be unusable, if it were your only protein source. It could only be broken down for energy - the fate of all unusable protein. And what if it contained all the needed [EAAs](#gloss-eaa), in the right amount - except one was totally missing? That one would make all the other unusable.

##### Why Total Protein Is the Denominator

A reasonable question is why the ratio uses total protein (including non-essential amino acids) as its denominator rather than comparing [EAA](#gloss-eaa) amounts in absolute terms.

Total protein is a normalizing device — **a common scale that makes the quality metric meaningful across foods with very different protein concentrations and very different serving sizes.**

The practical interpretation is direct: **if a food's protein clears all nine floors, eating enough of that food to meet your daily protein target will automatically also deliver your daily [EAA](#gloss-eaa) requirements.** No separate [EAA](#gloss-eaa) accounting is needed. A food that fails even one floor means you would reach your protein target before accumulating enough of that [EAA](#gloss-eaa) — the protein source is insufficient on its own.

The non-essential amino acids that make up the rest of the protein are biologically irrelevant to this specific calculation. They appear in the denominator only because total protein is the natural unit for expressing protein intake. They are not required to "activate" the [EAAs](#gloss-eaa) — they are simply passengers.

##### What "Complete" Actually Means

*Search terms: complete protein definition.*

"Complete" does not mean the amino acid ratios are all close to 1.0, or close to each other. It means **every one of the nine ratios is at or above 1.0** — each amino acid clears its own independent floor.

The nine [FAO](#gloss-fao) reference values were determined in separate human trials, one amino acid at a time. They are not ratios between amino acids; they are nine independent thresholds. Having tryptophan at 3.99× its floor while lysine sits at 1.22× its floor creates no imbalance — the tryptophan surplus cannot compensate for a deficit in another amino acid, but it does not create one either.

A food can therefore have wildly varying ratios across its amino acids and still be complete. Chia seed's protein ranges from 1.22 (lysine) to 3.99 (tryptophan) — a factor of more than three between the lowest and highest — and is still complete because nothing falls below 1.0. Cocoa shows the other side: its tryptophan is 2.26, yet it is *not* complete, because leucine (0.99) and [Met+Cys](#gloss-met-cys) (0.98) fall just short. One amino acid below the floor is enough, however small the shortfall.

The floor analogy: imagine a building with nine rooms, each with its own minimum ceiling height requirement. A room that comfortably exceeds its requirement does not help or hurt any other room. Every room must pass independently.

##### The Limiting Amino Acid — A Practical Analogy

When any one [EAA](#gloss-eaa) ratio falls below 1.0, that amino acid is "limiting" — it acts as a bottleneck that caps how much protein your body can fully incorporate into tissue.

A concrete analogy: you are mixing mortar to build a small wall. You have plenty of dry mix but run out of water before you have mixed enough for the full job. Without water, the remaining dry mix is unusable — you can build only 90 bricks worth of wall instead of 150. The water is your [limiting amino acid](#gloss-limiting-amino-acid). The unused dry mix is the protein your body cannot build into tissue, and instead breaks down and excretes.

Complementary proteins work by pooling the [limiting amino acids](#gloss-limiting-amino-acid) from multiple foods — a grain that is low in lysine paired with a legume that is rich in lysine can together clear all nine floors even though neither does so alone.

**The fate of unusable (not "complete") protein.** That unused portion isn't simply carried along or saved for later — your body has no way to bank amino acids the way it banks fat. Protein that can't be matched to the missing (limiting) amino acid is broken apart: the nitrogen-containing amino group is stripped off (deaminated) and converted to urea, which the kidneys excrete in urine; the leftover carbon skeleton is burned for energy or converted into glucose or fat, the same as it would be from a carbohydrate or fat source[^110]. So none of the calories are wasted — but as *protein*, it's gone. It cannot be retrieved later and built into muscle, enzymes, or any other tissue. This is exactly why pairing complementary foods matters: it lets more of what you eat cross the threshold and actually become usable protein, instead of being deaminated and excreted. Wherever NuMa shows digestible complete protein (DCP) alongside raw protein, the gap between the two is this same effect in numbers.
{: #unusable-protein-fate}

##### Digestion, Synthesis, and Catabolism — the Full Path {: #protein-fate-detail}

*Search terms: protein synthesis, protein breakdown.*

The paragraph above is the practical summary. Here is the fuller mechanism, for readers who want it.

Digestion itself doesn't distinguish complete from incomplete protein. Every protein you eat, regardless of amino acid profile, is broken down by digestive enzymes into free amino acids and small peptides, absorbed across the intestinal wall, and released into the bloodstream, joining the body's general pool of circulating amino acids. The "complete vs. incomplete" distinction only starts to matter at the *next* step.

Building new protein — muscle, enzymes, hormones, anything — requires all nine [EAAs](#gloss-eaa) to be present at once, in roughly the ratio the specific protein being built calls for. The body's protein-building machinery can't substitute one amino acid for another. If a meal's amino acid profile is short on one or more EAAs relative to what's needed, that shortfall — the [limiting amino acid](#gloss-limiting-amino-acid) — caps how much new protein can be built from that meal, no matter how abundant the other eight are.

The body has no storage depot for spare amino acids, the way it stores glucose as glycogen or extra energy as fat. Once the amount usable for building new protein is accounted for, whatever amino acids are left over get broken down for other uses (mostly in the liver, with the branched-chain amino acids handled largely in muscle instead). That breakdown happens in two parts: the nitrogen-containing amino group is stripped off and processed through the urea cycle for excretion in urine (some of it gets recycled into other, nonessential amino acids or into nucleotides and hormones instead); and the leftover carbon skeleton is used to make glucose, converted into ketone bodies, burned directly for energy, or stored as fat if there's a surplus[^110].

**Does this mean every meal needs to be a "complete" protein on its own?** No — and this is where the picture gets more reassuring. The classic reasoning here (Young & Pellett, 1994)[^14] is that the body turns over roughly 250–300 g of its own protein every day, far more than a typical meal provides, and the free amino acid pool released by that ongoing turnover can help fill in whatever a given meal's protein is short on. That's the biochemical basis for the now-standard advice that complementary foods (rice with beans, for instance) don't need to be eaten together at the same meal — pairing them anywhere across a varied day is enough. A 2024 controlled feeding study testing this directly[^15] — comparing meals built from complete, complementary, and single incomplete protein sources, all matched for total protein — found no significant difference in how much new muscle protein was built in the hours afterward, even though the amount of certain EAAs available in the bloodstream did differ between conditions. That suggests the real-world cost of an occasional single incomplete-protein meal may be smaller in practice than the classic model implies, though it's an area of active research rather than settled fact.

None of this changes what NuMa reports: it's still true that, gram for gram, a food or meal with a limiting amino acid yields less usable ([DCP](#gloss-dcp)) protein than its raw protein total. What the research adds is context on the time frame that matters — it's your protein pattern across the day, not any single meal in isolation, that determines how much of what you eat actually becomes usable protein.

##### The DIAAS Score

The Digestible Indispensable Amino Acid Score ([DIAAS](#gloss-diaas)) measures how much of a food's protein your body can actually use. For each [EAA](#gloss-eaa), it calculates:

> (mg of that [EAA](#gloss-eaa) actually absorbed per gram of food protein) ÷ ([FAO](#gloss-fao) reference value for that [EAA](#gloss-eaa))

The word "actually absorbed" is critical. Not all amino acids in a food survive digestion intact and cross into the bloodstream. [DIAAS](#gloss-diaas) uses [ileal digestibility](#gloss-ileal-digestibility) — the fraction of each amino acid absorbed by the end of the small intestine — to correct for this. The result is a score based on what your body actually receives, not merely what was in the food[^16].

A ratio of 1.0 means the food **delivers** exactly the required amount of that [EAA](#gloss-eaa) (per gram of protein eaten). A ratio below 1.0 means a shortfall — that [EAA](#gloss-eaa) is limiting. A ratio above 1.0 means a surplus above the floor. **The overall [DIAAS](#gloss-diaas) score for the food is set by whichever [EAA](#gloss-eaa) has the lowest ratio — the weakest link.**

##### A Concrete Example: Chia Seed

Consider chia seed ([USDA](#gloss-usda) #170554). Its amino acid ratios, before digestibility, are:

```
 Amino Acid      Ratio vs. FAO
 Tryptophan               3.99
 Threonine                1.71
 Isoleucine               1.61
 Leucine                  1.36
 Lysine                   1.22
 Met+Cys                  2.62
 Phe+Tyr                  2.33
 Valine                   1.44
 Histidine                2.01
```

Every ratio exceeds 1.0. This means that chia's protein contains every one of the nine [EAAs](#gloss-eaa) in at least the required proportion: no [limiting amino acid](#gloss-limiting-amino-acid) in the food itself. Its protein is complete.

Lysine at 1.22 is the weakest link — your slimmest margin, and the first to fall short once digestibility is counted. That is the next question, and a separate one: like most plant proteins, chia's is not fully digested, so its [DIAAS](#diaas), which counts what is absorbed, is lower than these ratios. A complete pattern does not by itself mean all of the protein is usable.

Importantly, these ratios do *not* mean that 100 grams of chia seed provides all the [EAAs](#gloss-eaa) you need for a day. Chia seed contains roughly 17 grams of protein per 100 grams. If your daily protein target is 80 grams, 100 grams of chia gets you only about 21% of the way there. The quality score tells you how well each gram of chia protein is matched to your needs — but you still need to eat enough of it to accumulate your daily protein target.

Think of it like fuel efficiency: a car that gets 50 miles per gallon is efficient, but knowing that tells you nothing about whether one gallon is enough to reach your destination. Quality and quantity are separate questions answered separately.

##### Summary

| Concept | What it answers |
|---|---|
| [FAO](#gloss-fao) reference values | How many mg of each [EAA](#gloss-eaa) a human needs per gram of protein consumed |
| [DIAAS](#gloss-diaas) ratio for one [EAA](#gloss-eaa) | Does this food deliver enough of that [EAA](#gloss-eaa), accounting for digestibility? |
| Overall [DIAAS](#gloss-diaas) score | What is the weakest link — the most limiting [EAA](#gloss-eaa) in this food? |
| Ratio > 1.0 for all [EAAs](#gloss-eaa) | [Complete protein](#gloss-complete-protein): no amino acid short in the food itself (how much is absorbed is the digestibility question) |
| Daily protein target | Separate calculation: how many grams of protein do you need total? |

The [DIAAS](#gloss-diaas) table characterizes the quality of each gram. Hitting your daily protein target is about counting how many grams you eat.

#### Essential Amino Acids {: #aa}

*Search terms: EAA, indispensable amino acids.*

Amino acids are the building blocks of protein. Nine of them are "essential", for our bodies cannot make them, so they must come from food every day[^60]:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and Phenylalanine respectively[^60]. Because of that, cystine in food spares some of the need for methionine, and tyrosine spares some of the need for phenylalanine. So the official scoring pattern judges each pair as one combined figure, and NuMa does the same: it evaluates [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr) as combined pairs when scoring protein quality, following [FAO](#gloss-fao) 2013 guidelines[^16].

See [Protein Completeness](#complete) and [Amino Acid Gaps](#gap) for how completeness is scored and what a gap means.


#### Protein Completeness {: #complete}

*Search terms: complete protein, incomplete protein, all essential amino acids, plant protein quality.*

A protein is "complete" when it supplies all nine essential amino acids at or above the [FAO](#gloss-fao) 2013 reference amounts, adjusted for digestibility[^16]. Essential amino acids cannot be made by the body — they must come from food.

Most animal proteins are complete. Most plant proteins are not, but combining plant foods across a day can produce a complete profile — see [Protein Complement Suggestions](#comp).

The score shown in completeness tables is the ratio of each amino acid to the [FAO](#gloss-fao) reference level. A score of **1.0 or above** for all nine means the protein is complete. The most-[limiting amino acid](#gloss-limiting-amino-acid) (the one with the lowest score) is identified as the bottleneck.


#### FAO 2013 Reference Standard {: #fao}

*Search terms: reference pattern, amino acid requirements, WHO.*

The [FAO](#gloss-fao) (Food and Agriculture Organization of the United Nations) published a reference amino acid scoring pattern in 2013 that defines the minimum amounts of each essential amino acid per gram of protein needed to meet adult human requirements. This is a ratio, not an absolute quantity — the requirement scales with how much protein you eat, so a small meal and a large meal must both hit the same per-gram proportions. See [Raw protein, protein quality, and protein digestibility](#appendix-protein-quality) for the full worked explanation of why this ratio, not total protein, determines what your body can use.

NuMa uses this pattern as the benchmark for all protein quality scoring: completeness, gaps, and complement calculations. A score of **1.0** for an amino acid means the food exactly meets the [FAO](#gloss-fao) reference for that amino acid; above 1.0 exceeds it; below 1.0 falls short.

The [FAO](#gloss-fao) 2013 pattern replaced an older 1991 standard and is the current international reference for protein quality assessment.

##### The reference values {: #fao-reference-values}
<span id="fao-values"></span>

*Search terms: mg per gram protein, amino acid table, requirements table.*

These are the nine numbers every protein-quality figure in NuMa is measured against — the 2013 report's scoring pattern for older children (over 3), adolescents and adults[^16]:

| Essential amino acid | mg per g of protein |
|---|---:|
| Histidine | 16 |
| Isoleucine | 30 |
| Leucine | 61 |
| Lysine | 48 |
| Sulfur amino acids ([Met+Cys](#gloss-met-cys)) | 23 |
| Aromatic amino acids ([Phe+Tyr](#gloss-phe-tyr)) | 41 |
| Threonine | 25 |
| Tryptophan | 6.6 |
| Valine | 40 |

**How to read it.** A protein meets the reference for leucine if each gram of it supplies at least 61 mg of leucine — after [digestibility](#gloss-tid) is taken into account. Divide what a food actually supplies by these figures and you get the score for each amino acid; the lowest score is the food's [DIAAS](#gloss-diaas), and that amino acid is its [limiting amino acid](#gloss-limiting-amino-acid). [Worked validation example — meal-level DIAAS for pinto beans + quinoa](#appendix-diaas-validation) works a real meal through every step.

**Why pairs.** Methionine and cysteine are scored together, as are phenylalanine and tyrosine, because the body makes cysteine from methionine and tyrosine from phenylalanine — what matters is the pair's total.

**One pattern, for everyone over 3.** The report also gives higher patterns for infants and for children from six months to three years, whose growth needs more of each amino acid per gram of protein. NuMa uses the over-3 pattern throughout; it isn't meant for planning a young child's diet.


#### DIAAS — Digestible Indispensable Amino Acid Score {: #diaas}

*Search terms: protein score, protein quality score, PDCAAS, digestibility score.*

[DIAAS](#gloss-diaas) measures how well your body can actually use the protein in a food. A score of **1.0** means the protein fully meets the [FAO 2013 amino acid reference standard](#fao) after accounting for digestibility[^16]. Scores above 1.0 are excellent; below 1.0 means one or more amino acids fall short.

Animal proteins typically score 1.0 or above. Most plant proteins score below 1.0, though some (pea protein, soy) come close. Digestibility matters because some protein in food is never absorbed — it passes through unchanged or is broken down by gut bacteria rather than used by your body.

A note on terminology: the [FAO](#gloss-fao) uses the term "indispensable amino acids" ([IAA](#gloss-iaa)) where this manual uses "essential amino acids" ([EAA](#gloss-eaa)) — both refer to the same nine amino acids. The "I" in [DIAAS](#gloss-diaas) stands for "Indispensable."

NuMa uses [DIAAS](#gloss-diaas) to calculate digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp)), which is a better indicator of actual protein quality than raw grams. See [Digestible Complete Protein (DCP)](#dcp).

##### Estimating DIAAS by hand for a packaged food {: #diaas-estimate-table}

*Search terms: packaged food DIAAS, branded food, estimate DIAAS, protein powder, product without amino acids.*

Branded/packaged products often have no amino acid data at all, so NuMa can't compute [DIAAS](#gloss-diaas) automatically — you record a point estimate instead via the [DIAAS](#gloss-diaas) estimate [Food Annotation](#gloss-food-annotation) (Foods → Annotate a food — see [Getting missing amino acid data](#custom-foods)). [DIAAS](#gloss-diaas) is mostly a property of the *protein source*, not the specific product, so the same point estimate is reusable across many products built from that ingredient. This table of published point estimates by dominant protein source is a starting reference, not a substitute for a real measured value if one is available:

    Protein source        DIAAS       Limiting AA                Note
    --------------------  ----------  -------------------------  ------------------------------
    Whole wheat            0.45       Lysine                     Range 0.40-0.57 across studies
    Soy (isolate/tofu)     0.90-1.00  Methionine+cystine (mild)  Near-complete
    Pea protein            0.82-0.90  Methionine+cystine         Complements wheat well
    Oats (dehulled)        0.77       Lysine                     Better than most cereals
    Sunflower seed          ~0.60     Lysine                     Usually a minor contributor

For a product where one ingredient supplies essentially all the protein (e.g. a wheat cracker where the oil contributes negligible protein), use that ingredient's row directly. For a product with two meaningful protein sources (e.g. a wheat+pea cracker), weight the estimate by each ingredient's share of total protein grams — the same complementary-protein logic used elsewhere in NuMa's [meal-level DIAAS](#dcp) pooling. Document your reasoning (source ingredient, any blending math) in the food's Confidence Note or notes field so it can be reviewed or revised later.


#### Limiting-Amino-Acid Scoring {: #aa-scoring}

*Search terms: limiting amino acid, two adjustments, two-stage calculation.*

Protein quality analysis involves two separate adjustments. The Protein Digestibility table shows the result after the first adjustment only. The phrase "before limiting-amino-acid scoring" on that table means the second adjustment has not yet been applied.

##### Step 1 — Digestibility adjustment (shown in the table)

    Digestible protein (g) = food protein (g) × digestibility coefficient

This accounts for how much protein actually reaches your bloodstream. A food with 20 g of protein and a digestibility of 0.85 delivers 17 g of digestible protein. This is what the "Digestible (g)" column in the [Meal Protein Digestibility Analysis](#meal-diaas) table shows.

##### Step 2 — Limiting-amino-acid scoring (the DIAAS step)

    Digestible complete protein (g) = digestible protein (g) × min(DIAAS, 1.0)

Even if all the protein is absorbed, it cannot all be incorporated into tissue unless every essential amino acid is present in sufficient proportion. The amino acid in shortest supply — the [limiting amino acid](#gloss-limiting-amino-acid) — sets a ceiling. [DIAAS](#gloss-diaas) is the ratio of that [limiting amino acid](#gloss-limiting-amino-acid) to the [FAO](#gloss-fao) reference level. If [DIAAS](#gloss-diaas) is 0.80, only 80% of the digestible protein can be fully used; the rest is broken down and converted to energy or excreted.

The "Total digestible protein" line below the table is the sum after step 1 only. The [DCP](#gloss-dcp) figure reported in the meal summary is the result after both steps.

Note: [DIAAS](#gloss-diaas) itself is not capped — a high-quality food can score above 1.0, meaning it has surplus amino acids relative to the reference. The min([DIAAS](#gloss-diaas), 1.0) applies only when computing [DCP](#gloss-dcp), because having excess amino acids does not allow you to absorb more total protein than you consumed.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [limiting amino acid](#gap), [DCP cap](#dcp-cap).


#### Digestible Complete Protein (DCP) {: #dcp}

*Search terms: effective protein, protein quality, bioavailable protein, digestible protein.*

[DCP](#gloss-dcp), digestible [complete protein](#gloss-complete-protein), is the grams of protein in a food or meal that are both digestible (absorbed) and complete (supplying every essential amino acid at or above reference levels). It allows for:

- **Digestibility:** how much protein is actually absorbed (from [DIAAS](#gloss-diaas))
- **Completeness:** whether the amino acid profile meets all requirements

So 30 g of protein with a [DIAAS](#gloss-diaas) of 0.70 and several gaps gives less usable protein than it seems; DCP shows how much. The literature also calls it "bioavailable complete protein" or "usable protein". See also [DIAAS](#diaas) and [Protein Completeness](#complete).

##### Protein per meal {: #protein-per-meal}
<span id="protein-distribution"></span><span id="protein-per-meal-amount"></span>
*Search terms: protein per meal, protein distribution, how much protein in one meal, leucine threshold, muscle protein synthesis, older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

For **when** to eat it — around exercise, before sleep, at breakfast — see [When to eat protein](#protein-timing).

The daily total matters most, but spread matters too: muscle is built in bursts after each meal, and a meal with little protein triggers only a small one. So it helps if most meals carry a worthwhile amount.

**The per-meal amount NuMa uses** comes from your profile ([Settings](#settings) → 1. Your Profile):

| You | Per meal | Leucine per meal | Source |
|---|---|---|---|
| Under 65 | 0.25–0.4 g per kg of body weight (for 70 kg: 17.5–28 g) | 0.7–3 g | lower end: International Society of Sports Nutrition[^65]; upper end: Schoenfeld & Aragon[^66] |
| 65 and over | 25–30 g | about 2.5–2.8 g | [PROT-AGE Study Group](#gloss-prot-age)[^67] |
| No profile set | 20–40 g | 0.7–3 g | International Society of Sports Nutrition[^65] |

Older bodies respond less to a small dose of protein (sometimes called *anabolic resistance*), which is why the 65-and-over figure is higher and isn't scaled down for lighter people.

**Where NuMa shows it.**

- **A meal's page**, under **Protein Summary**: the meal's protein and leucine, and whether it reaches the lower end of your per-meal amount.
- **A day's pages** (the day view and the Daily Summary for a date), under **Protein Quality — Full Day**: each meal's protein and leucine, and how many of the day's meals reached it.

**Why it uses DCP.** The studies used high-quality protein (dairy, egg, meat, soy), which is what [DCP](#gloss-dcp) measures, so a meal of 30 g raw protein with a low [DIAAS](#gloss-diaas) can fall short. Where DCP can't be worked out, NuMa uses raw protein and says so. Leucine, the amino acid most tied to switching on muscle building, is shown beside it (the raw amount).

**What it doesn't do.**

- **It never flags a meal as "too much".** The old idea that the body can use only 20–25 g at once has been overturned: a larger dose gives a larger, longer response[^68].
- **It doesn't check timing.** Sports guidance suggests such meals every 3–4 hours[^65], but NuMa records only when you entered an item, not when you ate, so it counts meals, not hours ([timing](#protein-timing)).
- **It doesn't replace your daily target** ([Daily Nutrient Goals](#goals)).

The figures come mostly from studies of healthy, often active, adults: a sensible guide for keeping or building muscle, especially when older, not a prescription. With kidney disease or another condition limiting protein, follow your clinician.


#### Why DCP Is Sometimes Capped Below the DIAAS Projection {: #dcp-cap}

*Search terms: DCP cap, absorbed protein limit, DCP lower than expected.*

The short version: the [DIAAS](#gloss-diaas) formula can project a Digestible [Complete Protein](#gloss-complete-protein) value that is mathematically higher than the protein your body actually absorbed. When that happens, NuMa caps [DCP](#gloss-dcp) at the absorbed-protein ceiling, because you cannot use more protein than you took in.

##### Why this happens

*The next few paragraphs walk through the underlying math. If you'd rather skip the algebra, jump ahead to "In plain words" below, or straight to the worked example.*

[DIAAS](#gloss-diaas) is defined by the [FAO](#gloss-fao) as:

    DIAAS = (digestible supply of the limiting amino acid)
            divided by
            (FAO reference density for that amino acid × raw protein)

The numerator uses digestibility-corrected amino acids. The denominator uses raw (pre-digestion) protein. This is intentional in the [FAO](#gloss-fao) standard. [DCP](#gloss-dcp) is then:

    DCP = raw protein × DIAAS

Substituting the [DIAAS](#gloss-diaas) definition, this simplifies to:

    DCP = digestible limiting-AA supply / FAO reference density for that AA

**In plain words:** [DCP](#gloss-dcp) answers "How many grams of a reference-quality protein would supply the same amount of limiting amino acid as this meal provides?"

For a single food, [DIAAS](#gloss-diaas) never exceeds that food's own digestibility, so [DCP](#gloss-dcp) cannot exceed absorbed protein. In a mixed meal, however, the [limiting amino acid](#gloss-limiting-amino-acid) may be concentrated in a high-digestibility ingredient while the bulk of the protein mass comes from lower-digestibility ingredients. The [DIAAS](#gloss-diaas) score then reflects the high-digestibility source, but average protein absorption reflects the lower-digestibility majority. [DIAAS](#gloss-diaas) ends up higher than the weighted-average digestibility, and the [DCP](#gloss-dcp) formula overshoots absorbed protein. This is a known mathematical artifact of applying [FAO](#gloss-fao) [DIAAS](#gloss-diaas) to mixed meals.

##### A worked example

Suppose a breakfast has two protein sources:

    Food                   Raw protein   Digestibility   Absorbed protein
    -------------------    -----------   -------------   ----------------
    Soy protein isolate    10 g          0.95            9.5 g
    Oatmeal                30 g          0.82            24.6 g
    -------------------    -----------   -------------   ----------------
    Total                  40 g          avg 0.854       34.1 g

Soy isolate is lysine-rich. Because lysine is the usual [limiting amino acid](#gloss-limiting-amino-acid) in grain-heavy meals, it strongly influences the [DIAAS](#gloss-diaas) score. Suppose the pooled lysine supply (after digestibility correction) yields:

    DIAAS = 0.91

Raw-formula [DCP](#gloss-dcp):

    DCP = 40 g × 0.91 = 36.4 g

But total absorbed protein is only 34.1 g. The cap is applied:

    DCP = min(36.4 g, 34.1 g) = 34.1 g

Why did [DIAAS](#gloss-diaas) exceed average digestibility? The soy isolate (dig 0.95) provides most of the lysine, so the lysine ratio in the [DIAAS](#gloss-diaas) calculation reflects its high digestibility. The larger oatmeal portion (dig 0.82) dominates the absorbed-protein total and pulls the weighted average down to 0.854. [DIAAS](#gloss-diaas) (0.91) ended up above that average, causing the overshoot.

##### What the cap means in practice

A capped [DCP](#gloss-dcp) is actually good news about amino acid quality. It means your [limiting amino acid](#gloss-limiting-amino-acid) is present in such good supply (relative to raw protein) that the formula projects more [complete protein](#gloss-complete-protein) than you could possibly absorb. The practical reading: all of your absorbed protein is functioning as [complete protein](#gloss-complete-protein). You are not losing protein to an amino acid shortfall.

Compare this to an uncapped [DCP](#gloss-dcp) that is well below absorbed protein: the gap between them represents protein you absorbed but cannot fully use for tissue synthesis because the [limiting amino acid](#gloss-limiting-amino-acid) ran out first. That is the more common and more concerning situation.

The average digestibility shown in the cap note is the weighted average of per-ingredient [digestibility coefficients](#gloss-digestibility-coefficient), weighted by protein content. Each coefficient comes from the curated lookup table or category estimate described in [meal protein digestibility](#meal-diaas).

This cap note appears on the meal, full-day, recipe, and daily-summary [DIAAS](#gloss-diaas) sections.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [amino acid scoring](#aa-scoring).


#### Amino Acid Gaps {: #gap}

*Search terms: shortfall, deficiency, low amino acid score.*

An amino acid gap means one or more essential amino acids are below the [FAO](#gloss-fao) 2013 reference level after digestibility adjustment. The gap is expressed as a score: 0.70 means the food supplies 70% of what is needed for that amino acid.

Each [complement suggestion](#comp) shows these scores as **Amino acid score, now → after** — for example "Lysine: 0.86→0.96" means lysine is at 86% of the reference now, and would be at 96% after adding the suggested amount. An "after" figure shown in green has reached 1.00, fully meeting the reference.

Gaps are sorted from most-limiting to least:

    Score     Status                                    Complement suggestion?
    --------  ----------------------------------------  ----------------------
    >= 1.0    Meets FAO reference -- complete           No
    0.95-0.99 Near-adequate -- practical gap too small  No (NuMa floor)
    0.70-0.94 Gap present                               Yes
    < 0.70    Significant gap -- high priority          Yes

NuMa generates complement suggestions only for scores below 0.95, not below the [FAO](#gloss-fao) floor of 1.0. A gap of 0.98 would suggest "add 1 g" -- not useful. The 0.95 floor filters those out.

- **Methionine** is the most commonly [limiting amino acid](#gloss-limiting-amino-acid) in plant-based diets.
- **Lysine** is the most commonly limiting in grain-heavy diets.

See [Protein Complement Suggestions](#comp) for how NuMa suggests foods to close gaps, and [When does NuMa suggest protein complements?](#comp-threshold) for how this per-amino-acid gap threshold relates to the meal-level composite [DIAAS](#gloss-diaas) score.


#### How NutriMagnus scores meal and recipe protein quality {: #protein-scoring}

*Search terms: meal protein quality, pooled DIAAS, recipe scoring.*

(This section explains the meal-level method. For background on single-food [DIAAS](#gloss-diaas) and how amino acid ratios work, see [Raw protein, protein quality, and protein digestibility](#appendix-protein-quality).)

A single food's [DIAAS](#gloss-diaas) comes straight from its amino acids and digestibility. A recipe or meal uses the [FAO](#gloss-fao)'s method for mixed meals: digestible amino acids are pooled across all ingredients before scoring. The two answer different questions.

##### Why meals need their own calculation

A food short in one amino acid can be rescued by another that has plenty, but only if both are counted together. Scoring each food and averaging misses that; pooling the amino acids first captures it.

##### The method, step by step

*Search terms: calculation, pooled amino acids.*

NuMa applies this procedure for each of the nine essential amino acids. For the paired amino acids [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr), both members of the pair are combined before scoring, following [FAO](#gloss-fao) practice.

**For each ingredient in the meal:**

Step 1. Determine the amino acid content in grams for the actual portion eaten. [USDA](#gloss-usda) data is per 100 g; NuMa scales to the weight you entered.

Step 2. Multiply each amino acid amount by the food's true [ileal digestibility](#gloss-ileal-digestibility) coefficient — a number between 0 and 1 representing the fraction that actually reaches your bloodstream. The result is the digestible grams of that amino acid from this ingredient.

    Digestible AA (g) = raw AA in portion (g) × digestibility coefficient

[Digestibility coefficients](#gloss-digestibility-coefficient) come from published literature and are looked up automatically. Eggs and dairy sit near 1.0; whole legumes are typically in the 0.79–0.85 range; most grains and seeds fall between 0.79 and 0.88.

**Then, across all ingredients:**

Step 3. Sum the digestible grams of each essential amino acid across every ingredient. This gives nine pooled totals — one per essential amino acid.

Step 4. For each amino acid, compute the ratio of the pooled digestible total to the [FAO](#gloss-fao) reference requirement for the total protein in the meal:

    Ratio = pooled digestible AA (g) ÷ (FAO reference value × total meal protein in g)

A ratio of 1.0 means the meal exactly meets the [FAO](#gloss-fao) target for that amino acid. A ratio of 0.80 means it supplies 80% of the target — a 20% shortfall.

Step 5. The lowest ratio across all nine essential amino acids is the meal's [DIAAS](#gloss-diaas) score. The amino acid with that lowest ratio is the [limiting amino acid](#gloss-limiting-amino-acid).

##### From DIAAS to digestible complete protein

*Search terms: DCP calculation, from DIAAS to DCP.*

    Digestible complete protein (g) = total meal protein (g) × min(DIAAS, 1.0)

A meal with 40 g of protein and a [DIAAS](#gloss-diaas) of 0.82 has 32.8 g of digestible [complete protein](#gloss-complete-protein); the other 7.2 g can't be used, because the [limiting amino acid](#gloss-limiting-amino-acid) runs out first.

##### A worked example — two ingredients, two amino acids

To keep the arithmetic readable, only lysine and [Met+Cys](#gloss-met-cys) are shown. The full calculation runs the same steps for all nine essential amino acids.

**The meal:**

    150 g cooked lentils:    13.5 g protein    lysine 0.94 g    Met+Cys 0.25 g    digestibility 0.83
     50 g pumpkin seeds:     12.3 g protein    lysine 0.49 g    Met+Cys 0.42 g    digestibility 0.85

Lentils are rich in lysine but short in [Met+Cys](#gloss-met-cys). Pumpkin seeds supply more [Met+Cys](#gloss-met-cys). Together they cover each other's gap.

**Steps 1–2 — digestible [AA](#gloss-aa) per ingredient:**

    Lentils:        digestible lysine   = 0.94 × 0.83 = 0.780 g
                    digestible Met+Cys  = 0.25 × 0.83 = 0.208 g

    Pumpkin seeds:  digestible lysine   = 0.49 × 0.85 = 0.417 g
                    digestible Met+Cys  = 0.42 × 0.85 = 0.357 g

**Step 3 — pool across ingredients:**

    Pooled lysine   = 0.780 + 0.417 = 1.197 g
    Pooled Met+Cys  = 0.208 + 0.357 = 0.565 g

**Step 4 — compute ratios (total meal protein = 13.5 + 12.3 = 25.8 g):**

The [FAO](#gloss-fao) reference values are 48 mg of lysine and 23 mg of [Met+Cys](#gloss-met-cys) per gram of protein.

    FAO target for lysine   = 48 ÷ 1000 × 25.8 = 1.238 g
    FAO target for Met+Cys  = 23 ÷ 1000 × 25.8 = 0.593 g

    Ratio for lysine   = 1.197 ÷ 1.238 = 0.97
    Ratio for Met+Cys  = 0.565 ÷ 0.593 = 0.95

**Step 5 — [DIAAS](#gloss-diaas) = lowest ratio:**

    DIAAS = 0.95    (Met+Cys is the limiting amino acid)

**Digestible [complete protein](#gloss-complete-protein):**

    25.8 g × 0.95 = 24.5 g digestible complete protein

Neither food alone would produce this result — lentils score poorly on [Met+Cys](#gloss-met-cys) when analyzed individually, but pumpkin seeds supply enough to bring the combined score to 0.95.

##### A note about missing amino acid data

*Search terms: missing amino acids, partial data.*

Ingredients without amino acid data are left out of the pooling; the result is flagged as an estimate, and [DCP](#gloss-dcp) counts only the protein from ingredients with data, so it isn't inflated.

###### Filling missing AA profiles at analysis time

NuMa says how many ingredients lack data, in two groups:

- **Inside a recipe:** fix it in the recipe, by replacing or refreshing the ingredient.
- **Logged directly:** the meal's **Refresh from [USDA](#gloss-usda)** fetches amino acids for those USDA has, filling only gaps ([details](#review-incoming)). Otherwise use a Foundation or [SR](#gloss-sr) Legacy equivalent, or [estimate from a similar food](#drafted-foods).

Until then such ingredients are left out and named. NuMa never goes online by itself during an analysis.

---

#### Protein Complement Suggestions {: #comp}

*Search terms: complements, protein combining, combine foods, pairing proteins, complementary proteins, protein pairing.*

When a food, recipe, meal or day has an amino acid gap, NuMa suggests foods that would improve its protein quality, in up to three tiers, each worked out differently.

##### WHEN DOES NUMA SUGGEST PROTEIN COMPLEMENTS? {: #comp-threshold}

*Search terms: when complements appear, no suggestions shown.*

A meal's [DIAAS](#gloss-diaas) is its lowest amino acid ratio, the [limiting amino acid](#gloss-limiting-amino-acid)'s[^16]. So when the meal's DIAAS is 0.95 or more, every amino acid is at 0.95 or more, and no suggestions appear.

Below 0.95 is the threshold because smaller gaps would take only a gram or two of food to close, not worth suggesting. A DIAAS of 0.95–0.99 is a small real shortfall, still a "good" protein by the [FAO](#gloss-fao)'s scale (0.75 to 0.99)[^16].

Below 0.95, NuMa suggests foods that supply the missing amino acid and raise the DIAAS toward or above 1.0.

To summarize:

    Meal DIAAS  What it means                                    Complement suggestions
    ----------  -----------------------------------------------  -----------------------
    >= 1.00     All amino acids meet or exceed the reference     None -- protein is fully complete
    0.95-0.99   Minor limiting amino acid; negligible gap        None -- gap too small to address
    < 0.95      Meaningful amino acid gap                        Yes -- foods shown that close the gap

See also [Amino Acid Gaps](#gap) for the same 0.95 threshold applied per amino acid rather than at the meal-composite level.

The amino acid completeness categories NuMa uses are derived from the work of the Food and Agriculture Organization of the United Nations.[^16]

##### TIER 1 — GAP CLOSERS

*Search terms: close a gap, fix amino acid shortfall, how much to add.*

Foods that can close a specific gap in a practical amount: rich enough in the limiting amino acid, relative to their protein, to bring its score to 1.0 (the [FAO](#gloss-fao) reference).

The amount counts each food at its own digestibility, so a well-digested food like soy protein isolate isn't undercounted in a less digestible meal. Gaps are tried most limiting first; the amount shown is for the first gap the food can close, and the suggestion says which if it isn't the main one.

**How much NuMa will suggest.** Each food has a most-per-meal amount, so you're never told to add four cups of nutritional yeast: your own saved limit; else three label servings (two for a recipe); else 15 g for seasonings and nutritional yeast, 40 g for protein powders, seeds and nuts, 60 g for cheese, 300 g for anything else. If closing the gap needs more, the suggestion shows the food at its limit, how much full closure would take, and how far the limit gets you. **Use the full … g this time** lifts the limit for this page; **Most I'd add to a meal** with **Save limit for this food** sets it for good (clear and save for the default). Booster steps stop at the same limit.

Each suggestion shows:
  - The food's or recipe's name, linked to its page (a [generic](#gloss-generic) estimate from the built-in list isn't linked)
  - Grams to add
  - Which gaps it closes, with scores before and after
  - Digestible protein added
  - Total bioavailable [complete protein](#gloss-complete-protein): the base and the added protein together, times their pooled [DIAAS](#gloss-diaas). It's more than the two foods' figures added, because the complement makes the base food's protein more usable too.
  - **% increase** over your current [DCP](#gloss-dcp) (named under the table). A food held to its limit says "per-meal limit" instead of "full".

##### RANKING

*Search terms: sort suggestions, best suggestion, order of suggestions.*

**Sort by** chooses how gap closers are ranked:

  - **Greatest [DCP](#gloss-dcp) achieved** (the default): the most total complete protein afterward, the same figure each option shows (for a meal, day or recipe, worked out from every ingredient; a note says how).
  - **Most digestible protein added**, however well it targets the gap.
  - **Greatest effect on amino acid gap**: most gaps closed, then the biggest rise in the limiting amino acid.
  - **Smallest addition (in grams).**

In every order, an option that completes the amino acid profile comes first. (Two-food combinations get a similar promotion, only up to 50 g.)

##### TIER 2 — DIAAS-BOOSTING OPTIONS

*Search terms: DIAAS booster, raise digestibility, improve protein quality.*

Sometimes no practical amount of one food can close the gap, because the base food's amino acids are already near the reference and the shortfall comes from its low digestibility.

Then NuMa shows [DIAAS](#gloss-diaas)-boosting options: foods whose digestible amino acids raise the pooled DIAAS toward 0.90. Each food's own [ileal digestibility](#gloss-ileal-digestibility) is used, so a well-digested food like soy protein isolate (95%[^86]) counts for more than its raw content suggests.

Each shows a range of amounts (15, 30, 60, up to 120 g, about ½ cup; up to 300 g for a recipe batch), with the DIAAS before and after each, so you can choose a realistic portion.

##### TIER 3 — TWO-FOOD COMBINATIONS

*Search terms: two foods, pair of foods, second gap.*

When one food closes the main gap but dilutes another borderline amino acid, a pair is offered:

  Food A closes the primary (most-limiting) gap. It may open a smaller secondary gap by diluting a borderline amino acid that was already close to the threshold.

  Food B is chosen specifically to close whatever gap Food A left behind, without opening further gaps.

Together they clear every gap. Each pair shows its two amounts, the combined effect, and whether it "closes all gaps". Up to six are shown, lightest first; one closing all gaps is moved up only if it weighs 50 g or less, so a heavy pairing doesn't win just because enough of it fixes everything.

##### WHICH TIER IS RIGHT FOR YOU?

*Search terms: which suggestion, choose a suggestion, tiers compared.*

Gap closers (Tier 1) are the most targeted: one food, one deficiency.

If they open a second gap, two-food combinations (Tier 3) close everything in one step.

If only [DIAAS](#gloss-diaas)-boosting options appear (Tier 2), the base food isn't very digestible. A well-digested, amino-acid-rich addition still helps: a meal DIAAS of 0.90 means 90% of its protein is complete and digestible.

[Complement foods](#gloss-complement-food) needn't be in the same meal: daily totals are enough for healthy adults[^14]<sup>,</sup>[^15].

##### RECIPE ANALYSIS: AMOUNTS ARE SIZED TO THE WHOLE BATCH {: #comp-recipe-scale}

*Search terms: recipe suggestions, amounts too large, scale suggestions.*

On a recipe's own page, every suggested amount is for the **whole batch**, all servings, because the only way to act on it is to add the ingredient to the whole recipe.

So a suggestion can look large (80 g or more of soy protein isolate for a 4-serving recipe): that's for the pot, not a serving. Each also shows the per-serving equivalent.

**Where candidates come from**, in order: your [pantry](#pantry), including the recipes in it ([Recipes in your pantry](#pantry-recipes)); then your other [recipes](#recipes-menu-web), your wider Food Cache (matched by name against the built-in list); then the built-in list itself[^10], filtered by your [dietary preferences](#diet). The header says which were used. Tags like "(estimated)" are explained in [Amino acid estimates in suggestions](#comp-estimate); to drop a suggestion, see [Ignoring a complement suggestion](#ignore-complement).


#### Amino acid estimates in complement suggestions {: #comp-estimate}

*Search terms: estimated amino acids, estimated tag.*

A [complement suggestion](#comp) needs amino acid data for the suggested food to compute how much of it closes a gap. Most of the time that comes from the food's own real, measured data. When it doesn't, NuMa falls back to its built-in reference table of 25 common protein sources[^10] (soy protein isolate, nutritional yeast, oats, and the like) — the same last-resort data source described above in [Protein Complement Suggestions](#comp) — rather than leaving you with no suggestion at all. Two tags tell you when that fallback happened:

  "(estimated)" — the suggested food is a real item from your pantry, recipes, or food cache, but it has no amino acid panel of its own. NuMa matched its name against the built-in reference table and scaled that table's amino acid profile to this food's own protein content.

  "([generic](#gloss-generic) estimate)" — no real food matched at all. The whole suggestion is the reference table entry itself, not any specific product you have.

Either way, this estimate is computed fresh every time the suggestion is shown — it is never saved to the food's own record, so there is nothing to undo. This is not the same as the "estimate amino acids from another food" tool described under [Estimating amino acids by copying from another food](#custom-foods). That tool lets you search all your saved foods and pick whichever one you judge to be the best match yourself, and it saves your choice permanently to that food's own record. The built-in table used for the "(estimated)" / "([generic](#gloss-generic) estimate)" tags, by contrast, is a fixed, much shorter list matched purely by keyword — it can't use your own judgment about which food is the closer match, so the two methods can disagree.

For a food you rely on often, running the "estimate amino acids from another food" tool on it yourself is worth doing: it is more accurate (your judgment beats a keyword match against 25 entries), it only has to be done once, and it turns the food into a normal pantry/cache candidate for every suggestion afterward — no more tags.


#### Two-step combinations {: #comb}

*Search terms: two foods, add two foods, second food.*

After the gap-closer and [DIAAS](#gloss-diaas)-boosting sections, NuMa offers to show two-step combinations. Each combination pairs one of the top gap-closers (Step 1) with the best [DIAAS](#gloss-diaas)-booster for the resulting protein pool (Step 2).

Why two steps? A gap-closer fixes amino acid balance but may not raise digestibility. A [DIAAS](#gloss-diaas)-booster raises digestibility but cannot close a specific amino acid gap on its own. Together they address both problems: Step 1 corrects the [limiting amino acid](#gloss-limiting-amino-acid); Step 2 raises the overall [DIAAS](#gloss-diaas) of the now-balanced pool, increasing digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp)) further.

Each combination shows:
  - Step 1: the gap-closer, its serving size, and the [DCP](#gloss-dcp) gain from the base
  - Step 2: the smallest practical serving of the best booster for that pool, and the further [DCP](#gloss-dcp) gain
  - Net [DCP](#gloss-dcp) gain from base to end of Step 2

If no [DIAAS](#gloss-diaas)-booster can improve on the post-Step-1 pool (because the gap-closer already raised the pool's digestibility above what any available booster can match), the program says so rather than showing a misleading suggestion.

See also [complement suggestions](#comp) for the full complement suggestion system.


#### Why some foods appear only in DIAAS-boosting suggestions {: #comp-appendix}

*Search terms: DIAAS boosting only, why not gap closer.*

This appendix explains why certain nutritionally excellent protein sources — soy protein isolate, nutritional yeast, pea protein — sometimes appear only in the [DIAAS](#gloss-diaas)-boosting tier and not as gap closers, even though they are well-known complements to legumes.

DIGESTIBILITY-DRIVEN GAPS

When a legume such as pinto beans has a low [DIAAS](#gloss-diaas) (e.g., 0.73), that low score is often not caused by a weak amino acid profile. Pinto beans' raw [Met+Cys](#gloss-met-cys) ratio is approximately 22 mg/g protein — right at the [FAO](#gloss-fao) reference of 22. The gap emerges only because its true [ileal digestibility](#gloss-ileal-digestibility) is 0.80: the body absorbs only 80% of the protein, which pulls every amino acid's effective contribution below the reference threshold.

The gap-closer formula accounts for this by raising the target threshold:

    Adjusted target = FAO reference ÷ base digestibility
                     = 22 mg/g ÷ 0.73 = 30.1 mg/g

A gap closer must have an amino acid/protein ratio above 30.1 mg/g to mathematically close the [Met+Cys](#gloss-met-cys) gap. Most plant proteins are excluded:

    Soy protein isolate  Met+Cys  =  23.0 mg/g  (below 30.1) → excluded
    Nutritional yeast    Met+Cys  =  21.2 mg/g  (below 30.1) → excluded
    Sesame seeds         Met+Cys  =  49.7 mg/g  (above 30.1) → qualifies

This is mathematically correct: because pinto beans absorb poorly, you need a complement with a disproportionately high amino acid ratio to overcome the digestibility deficit in the gap-closer framework. Sesame qualifies; [SPI](#gloss-spi) and nutritional yeast do not.

WHY [DIAAS](#gloss-diaas)-BOOSTING STILL WORKS FOR [SPI](#gloss-spi)

The [DIAAS](#gloss-diaas)-boosting formula takes a different view. Instead of asking "can this food close the gap for pinto beans alone?", it asks: "what happens when I pool the digestible amino acids from pinto beans and SPI together?"

    Pooled digestible Met+Cys = (pinto's Met+Cys × 0.80)
                              + (SPI's Met+Cys per 100g × grams of SPI added ÷ 100 × 0.95)

    Pooled protein total = pinto's raw protein
                          + (SPI's raw protein per 100g × grams of SPI added ÷ 100)

Because [SPI](#gloss-spi) has a much higher digestibility (0.95 vs. 0.80), its amino acids contribute more efficiently per gram than pinto's own amino acids do. At approximately 25-35 g of [SPI](#gloss-spi) added to 100 g of pinto beans, the pooled meal [DIAAS](#gloss-diaas) reaches 0.90 — a meaningful improvement from 0.73.

The reason [SPI](#gloss-spi) still can't be a gap closer is that its raw [Met+Cys](#gloss-met-cys) ratio (23 mg/g) is below the inflated 30.1 mg/g threshold the gap-closer formula requires. But in the [pooled DIAAS](#gloss-pooled-diaas) calculation, where each food's digestibility applies only to its own amino acids, [SPI](#gloss-spi)'s superior digestibility (0.95 vs. pinto's 0.80) is sufficient to lift the combined score above the target.

PRACTICAL INTERPRETATION

From a dietary standpoint both tiers are useful, but they mean different things:

Gap closers (sesame, Brazil nuts, hemp seeds): these close the specific amino acid deficiency. After adding them, the combined protein is mathematically complete per the gap-closer model. Required amounts are often small (8-30 g).

[DIAAS](#gloss-diaas) boosters (soy protein isolate, nutritional yeast, egg, whey): these are high-quality proteins with excellent digestibility. They raise the effective quality of the whole meal by contributing highly digestible amino acids. A meal [DIAAS](#gloss-diaas) of 0.90 means 90% of the meal's protein is both complete and bioavailable — a strong nutritional outcome even if the precise gap-closer criterion isn't met.

In practice, combining a gap closer (e.g., sesame tahini) with a [DIAAS](#gloss-diaas) booster (e.g., a small serving of Greek yogurt or egg) gives both a complete amino acid profile and high overall digestibility — the best outcome for protein quality from a high-legume meal.

THE REFERENCE VALUES

NuMa uses two slightly different reference sets:

Gap-closer tier (an older reference table): [Met+Cys](#gloss-met-cys) = 22 mg/g, Lysine = 45 mg/g, Leucine = 59 mg/g

[DIAAS](#gloss-diaas)-booster tier ([FAO](#gloss-fao) 2013, Table 6 — the current authoritative reference): [Met+Cys](#gloss-met-cys) = 23 mg/g, Lysine = 48 mg/g, Leucine = 61 mg/g

The small differences (1-3 mg/g) reflect different published [FAO](#gloss-fao) tables used for these two tiers. Both are within normal rounding variance across [FAO](#gloss-fao) publications. The gap-closer tier's values are the older set; the [DIAAS](#gloss-diaas)-booster tier uses the authoritative [FAO](#gloss-fao) 2013 adult reference pattern.

(For technically skilled users: in NuMa's source code these two tables are `usda_api.AA_REFERENCE_MG_PER_G_PROTEIN` and `diaas.FAO_REFERENCE`, respectively.)

#### When to eat protein {: #protein-timing}
<span id="when-to-eat-protein"></span><span id="protein-timing-exercise"></span><span id="nutrient-timing"></span>
*Search terms: protein timing, when to eat protein, protein before or after exercise, anabolic window, workout, resistance training, endurance, protein before bed, pre-sleep protein, breakfast protein, time of day, meal timing.*

What the research says about *when* to eat protein, as distinct from [how much per meal](#protein-per-meal). Most of it comes from studies of muscle building in healthy, often young and trained, adults; where a finding is narrower than that, it says so.

##### First: the daily total matters most

*Search terms: total protein, daily protein total.*

Before any question of timing, the biggest single factor is how much protein you eat over the day. The International Society of Sports Nutrition (ISSN) puts meeting the daily total — "preferably with evenly spaced protein feedings" — as the primary emphasis[^70]. When studies of protein "timing" are corrected for the fact that the timed group often simply ate more protein, most of the timing effect disappears[^71]. And extra protein stops adding muscle at around 1.6 g per kg of body weight a day in people doing resistance training[^72]. So: get the daily total right first; timing is the refinement.

##### Spread it across the day

The best-supported timing advice is to **spread protein fairly evenly over your meals**, rather than eating most of it at dinner. In a controlled study, the same daily protein eaten as about 30 g at each of three meals produced 25% more muscle protein synthesis over 24 hours than the typical pattern of little at breakfast and a lot at dinner[^73]. The [ISSN](#gloss-issn) suggests 20–40 g every 3–4 hours[^70]. This is what NuMa's [protein per meal](#protein-per-meal) check helps with: aim for most meals to reach your per-meal amount.

##### Around exercise

*Search terms: workout, gym, after exercise, resistance training.*

- **After resistance exercise** (weights, bodyweight strength work): protein "immediately to 2 hours" afterwards strongly stimulates muscle building[^70]. But the old idea of a narrow "anabolic window" — a 30–60-minute window you must not miss — hasn't held up: once total protein is matched, protein eaten within an hour of training shows no clear advantage over protein eaten at other times[^71]. In practice, having a protein-containing meal within a couple of hours either side of a session covers it.
- **Before exercise**: protein (or protein with carbohydrate) before *or* after training can both support strength gains[^70]; if you train soon after a meal that already contained protein, there's no need for more right after.
- **After endurance exercise** (running, cycling, swimming): the priorities shift. Carbohydrate to refill muscle glycogen comes first, especially if you'll train again within the day; adding protein to it helps repair. When recovery time is short, the [ISSN](#gloss-issn) suggests carbohydrate with 0.2–0.4 g protein per kg per hour[^70]. In trained endurance athletes after a long ride, about 30 g of protein (roughly 0.5 g/kg) gave the maximum muscle-protein response, and more didn't help[^74]. Protein did not, however, increase the building of new mitochondria (the muscle's energy machinery) beyond what carbohydrate alone did — that adaptation comes from the training itself.
- **Does the kind of exercise matter?** Yes, in what you pair protein with and why. After strength work, the goal is muscle building, and protein is the main lever. After long or hard endurance work, refuelling with carbohydrate matters most, with protein supporting repair. For mixed training, a meal with both covers both.

##### Before sleep

*Search terms: bedtime, sleep protein.*

A dose of slowly digested protein before sleep can keep muscle building going overnight. The [ISSN](#gloss-issn) cites about 30–40 g of casein (the main protein in milk; cottage cheese and Greek yogurt are rich in it)[^70]. In young men doing a 12-week resistance program, about 27.5 g of protein each night before sleep led to greater gains in muscle size and strength than a placebo[^75]. Most of this evidence is from young, training men; it's a reasonable option if your evening meal was light on protein, not a requirement.

##### Time of day: is breakfast special?

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

There's emerging evidence that protein early in the day may matter more for muscle than the same protein late in the day, linked to the muscle's own daily (circadian) clock. In mice, protein at the first meal of their active period built more muscle than protein at the last, an effect that vanished in mice with a disrupted muscle clock; and among 60 women aged 65 and over, those who ate a larger share of their protein at breakfast had better muscle function[^76]. The human part of that evidence is observational, so it shows association, not cause. But it points the same way as the distribution advice above: since breakfast is usually the lowest-protein meal, raising it is a good first step.

##### What NuMa shows, and doesn't

*Search terms: timing not tracked, clock time, limitations.*

The [protein per meal](#protein-per-meal) check shows which meals reached a worthwhile amount, the practical heart of the advice above. NuMa records when you entered each item, not when you ate or exercised, so it can't check timing around a workout or sleep; naming a meal for its role ("Post-workout", "Bedtime snack") makes it easy to spot.

These are guides for keeping and building muscle, not medical advice. If you have kidney disease or another condition that limits protein, follow your clinician's advice.

#### Worked validation example — meal-level DIAAS for pinto beans + quinoa {: #appendix-diaas-validation}

*Search terms: check the math, verify DIAAS, worked example.*

This appendix lets you verify [NuMa](#gloss-numa)'s protein quality calculation independently. Every step is shown explicitly so you can reproduce it in a spreadsheet or calculator, then compare your result with what [NuMa](#gloss-numa) produces when you enter these two foods as a meal.

##### The two foods

| Food | [FDC ID](#gloss-fdc-id) | Data type | [USDA](#gloss-usda) source |
|------|--------|-----------|-------------|
| Beans, pinto, mature seeds, cooked, boiled, with salt | 173796 | [SR](#gloss-sr) Legacy | https://fdc.nal.usda.gov/food-details/173796/nutrients |
| Quinoa, cooked | 168917 | SR Legacy | https://fdc.nal.usda.gov/food-details/168917/nutrients |

All nutrient values below are drawn directly from those pages as of June 2026. The demo uses **100 g of each food** — round numbers that make the arithmetic easy to follow.

---

##### Step 1 — Individual nutrient profiles (per 100 g, from USDA)

**Table I-1. Macronutrients and key micronutrients**

| Nutrient | Unit | Pinto beans ([FDC](#gloss-fdc) 173796) | Quinoa ([FDC](#gloss-fdc) 168917) |
|----------|------|------------------------:|--------------------:|
| Calories | kcal | 143.0 | 120.0 |
| Protein | g | 9.01 | 4.40 |
| Carbohydrate | g | 26.22 | 21.30 |
| Total fat | g | 0.65 | 1.92 |
| Fiber | g | 9.00 | 2.80 |
| Saturated fat | g | 0.109 | 0.231 |
| Monounsaturated fat | g | 0.106 | 0.528 |
| Polyunsaturated fat | g | 0.188 | 1.078 |
| Calcium | mg | 46.0 | 17.0 |
| Iron | mg | 2.09 | 1.49 |
| Magnesium | mg | 50.0 | 64.0 |
| Phosphorus | mg | 147.0 | 152.0 |
| Potassium | mg | 436.0 | 172.0 |
| Sodium | mg | 238.0 | 7.0 |
| Zinc | mg | 0.98 | 1.09 |
| Vitamin C | mg | 0.8 | 0.0 |
| Thiamin (B1) | mg | 0.193 | 0.107 |
| Riboflavin (B2) | mg | 0.062 | 0.110 |
| Niacin (B3) | mg | 0.318 | 0.412 |
| Vitamin B6 | mg | 0.229 | 0.123 |
| Folate | mcg | 172.0 | 42.0 |
| Vitamin E | mg | 0.94 | 0.63 |
| Vitamin K | mcg | 3.5 | 0.0 |
| Choline | mg | — | 23.0 |

**Table I-2. Indispensable amino acids (IAAs) per 100 g**

Amounts are in grams. Note that [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr) are scored as *pairs* in the [DIAAS](#gloss-diaas) methodology (see Step 3).

| Amino acid | Pinto beans | Quinoa |
|------------|------------:|-------:|
| Histidine | 0.232 | 0.127 |
| Isoleucine | 0.368 | 0.157 |
| Leucine | 0.664 | 0.261 |
| Lysine | 0.571 | 0.239 |
| Methionine | 0.126 | 0.096 |
| Cystine (pairs with Met) | 0.090 | 0.063 |
| Phenylalanine | 0.450 | 0.185 |
| Tyrosine (pairs with Phe) | 0.234 | 0.083 |
| Threonine | 0.350 | 0.131 |
| Tryptophan | 0.098 | 0.052 |
| Valine | 0.435 | 0.185 |

---

##### Step 2 — Pooled nutrients for the meal (100 g pinto + 100 g quinoa = 200 g total)

To pool, simply add the values from the two 100 g servings. The totals below represent the entire 200 g meal.

**Table I-3. Pooled macros and key micronutrients (200 g meal)**

| Nutrient | Pinto 100 g | Quinoa 100 g | Meal total |
|----------|------------:|-------------:|-----------:|
| Calories (kcal) | 143.0 | 120.0 | 263.0 |
| Protein (g) | 9.01 | 4.40 | **13.41** |
| Carbohydrate (g) | 26.22 | 21.30 | 47.52 |
| Total fat (g) | 0.65 | 1.92 | 2.57 |
| Fiber (g) | 9.00 | 2.80 | 11.80 |
| Calcium (mg) | 46.0 | 17.0 | 63.0 |
| Iron (mg) | 2.09 | 1.49 | 3.58 |
| Magnesium (mg) | 50.0 | 64.0 | 114.0 |
| Potassium (mg) | 436.0 | 172.0 | 608.0 |
| Folate (mcg) | 172.0 | 42.0 | 214.0 |

**Table I-4. Pooled [IAA](#gloss-iaa) totals for the meal (g)**

| Amino acid | Pinto 100 g | Quinoa 100 g | Meal total |
|------------|------------:|-------------:|-----------:|
| Histidine | 0.232 | 0.127 | 0.359 |
| Isoleucine | 0.368 | 0.157 | 0.525 |
| Leucine | 0.664 | 0.261 | 0.925 |
| Lysine | 0.571 | 0.239 | 0.810 |
| Met + Cys | 0.126 + 0.090 = 0.216 | 0.096 + 0.063 = 0.159 | **0.375** |
| Phe + Tyr | 0.450 + 0.234 = 0.684 | 0.185 + 0.083 = 0.268 | **0.952** |
| Threonine | 0.350 | 0.131 | 0.481 |
| Tryptophan | 0.098 | 0.052 | 0.150 |
| Valine | 0.435 | 0.185 | 0.620 |

---

##### Step 3 — Applying digestibility to get digestible IAA amounts

Raw amino acid values from [USDA](#gloss-usda) are not all absorbed. The [DIAAS](#gloss-diaas) methodology requires multiplying each food's [IAA](#gloss-iaa) amounts by that food's *true [ileal digestibility](#gloss-ileal-digestibility) coefficient* — a value between 0 and 1 representing the fraction of each IAA that actually reaches the bloodstream.

[NuMa](#gloss-numa)'s digestibility values come from the [FAO](#gloss-fao) 2013 report and published literature. For these two foods:

| Food | [Digestibility coefficient](#gloss-digestibility-coefficient) | Source |
|------|:------------------------:|--------|
| Pinto beans | **0.80** | [FAO](#gloss-fao) Food and Nutrition Paper 92 (2013) |
| Quinoa | **0.85** | Mathai et al. (2017), *British Journal of Nutrition* |

To apply: multiply each food's IAA total by its coefficient. For example, for pinto beans' leucine: 0.664 × 0.80 = 0.531 g digestible leucine.

**Table I-5. Digestible IAA amounts per food (g)**

| Amino acid | Pinto × 0.80 | Quinoa × 0.85 | Pooled digestible |
|------------|-------------:|--------------:|------------------:|
| Histidine | 0.232 × 0.80 = **0.18560** | 0.127 × 0.85 = **0.10795** | **0.29355** |
| Isoleucine | 0.368 × 0.80 = **0.29440** | 0.157 × 0.85 = **0.13345** | **0.42785** |
| Leucine | 0.664 × 0.80 = **0.53120** | 0.261 × 0.85 = **0.22185** | **0.75305** |
| Lysine | 0.571 × 0.80 = **0.45680** | 0.239 × 0.85 = **0.20315** | **0.65995** |
| [Met+Cys](#gloss-met-cys) | 0.216 × 0.80 = **0.17280** | 0.159 × 0.85 = **0.13515** | **0.30795** |
| [Phe+Tyr](#gloss-phe-tyr) | 0.684 × 0.80 = **0.54720** | 0.268 × 0.85 = **0.22780** | **0.77500** |
| Threonine | 0.350 × 0.80 = **0.28000** | 0.131 × 0.85 = **0.11135** | **0.39135** |
| Tryptophan | 0.098 × 0.80 = **0.07840** | 0.052 × 0.85 = **0.04420** | **0.12260** |
| Valine | 0.435 × 0.80 = **0.34800** | 0.185 × 0.85 = **0.15725** | **0.50525** |

---

##### Step 4 — The FAO reference amounts for this meal

The [DIAAS](#gloss-diaas) method scores each pooled digestible [IAA](#gloss-iaa) against how much of that IAA a *reference protein* of equal weight would provide. The reference values, from [FAO](#gloss-fao) Food and Nutrition Paper 92 (2013), Table 6, are expressed in **mg of IAA per gram of total protein** for older children, adolescents, and adults.

The full table, with how to read it, is in [The reference values](#fao-reference-values). The relevant values are:

| IAA | [FAO](#gloss-fao) reference (mg/g protein) |
|-----|-----------------------------:|
| Histidine | 16.0 |
| Isoleucine | 30.0 |
| Leucine | 61.0 |
| Lysine | 48.0 |
| [Met+Cys](#gloss-met-cys) | 23.0 |
| [Phe+Tyr](#gloss-phe-tyr) | 41.0 |
| Threonine | 25.0 |
| Tryptophan | 6.6 |
| Valine | 40.0 |

The meal contains **13.41 g total protein** (9.01 + 4.40). To find how many grams of each IAA the reference protein provides for this amount of protein, multiply:

    Reference amount (g) = FAO value (mg/g) × 13.41 (g protein) ÷ 1000

**Table I-6. [FAO](#gloss-fao) reference IAA amounts for 13.41 g protein**

| IAA | [FAO](#gloss-fao) (mg/g) | Calculation | Reference (g) |
|-----|----------:|-------------|-------------:|
| Histidine | 16.0 | 16.0 × 13.41 ÷ 1000 | 0.21456 |
| Isoleucine | 30.0 | 30.0 × 13.41 ÷ 1000 | 0.40230 |
| Leucine | 61.0 | 61.0 × 13.41 ÷ 1000 | 0.81801 |
| Lysine | 48.0 | 48.0 × 13.41 ÷ 1000 | 0.64368 |
| [Met+Cys](#gloss-met-cys) | 23.0 | 23.0 × 13.41 ÷ 1000 | 0.30843 |
| [Phe+Tyr](#gloss-phe-tyr) | 41.0 | 41.0 × 13.41 ÷ 1000 | 0.54981 |
| Threonine | 25.0 | 25.0 × 13.41 ÷ 1000 | 0.33525 |
| Tryptophan | 6.6 | 6.6 × 13.41 ÷ 1000 | 0.08851 |
| Valine | 40.0 | 40.0 × 13.41 ÷ 1000 | 0.53640 |

---

##### Step 5 — IAA ratios and the composite DIAAS score

For each [IAA](#gloss-iaa), divide the pooled digestible amount (from Table I-5) by the reference amount (from Table I-6). The result is a ratio: a value ≥ 1.0 means the meal meets or exceeds the reference for that IAA; below 1.0 means it falls short.

    Ratio = pooled digestible IAA (g) ÷ FAO reference IAA (g)

**Table I-7. IAA ratios vs. [FAO](#gloss-fao) reference**

| IAA | Pooled dig. (g) | Reference (g) | Ratio | Meets reference? |
|-----|----------------:|--------------:|------:|:----------------:|
| Histidine | 0.29355 | 0.21456 | 1.368 | Yes |
| Isoleucine | 0.42785 | 0.40230 | 1.064 | Yes |
| **Leucine** | **0.75305** | **0.81801** | **0.921** | **No — limiting** |
| Lysine | 0.65995 | 0.64368 | 1.025 | Yes |
| [Met+Cys](#gloss-met-cys) | 0.30795 | 0.30843 | 0.998 | Marginal (99.8%) |
| [Phe+Tyr](#gloss-phe-tyr) | 0.77500 | 0.54981 | 1.410 | Yes |
| Threonine | 0.39135 | 0.33525 | 1.167 | Yes |
| Tryptophan | 0.12260 | 0.08851 | 1.385 | Yes |
| Valine | 0.50525 | 0.53640 | 0.942 | No |

The **composite [DIAAS](#gloss-diaas) score is the lowest ratio** — the *limiting* amino acid determines the ceiling for all the others, because when one IAA runs out, the others cannot be used for protein synthesis.

    Composite DIAAS = the lowest ratio above = 0.921   (limited by Leucine)

A [DIAAS](#gloss-diaas) of 0.921 means this meal delivers about 92% of the protein quality of a reference protein.

**Digestible complete protein has a second ceiling beyond the DIAAS multiplication.** The naive calculation would be:

    13.41 g × 0.921 = 12.35 g

but this can overstate what the body actually absorbs. DIAAS is the *limiting-IAA* ratio, not an average — and here the limiting IAA (leucine) happens to be relatively better-supplied by quinoa, the more digestible of the two foods (0.85 vs. pinto beans' 0.80). Multiplying the *whole* protein pool by that single ratio can produce a [DCP](#gloss-dcp) higher than the protein that was ever actually digested. [NuMa](#gloss-numa) guards against this by also capping DCP at the meal's digestibility-weighted protein — the sum of each food's protein × its own digestibility coefficient:

    aa_dig_protein_g = (9.01 g × 0.80) + (4.40 g × 0.85) = 7.208 + 3.740 = 10.948 g

    DCP = min(13.41 g × 0.921, 10.948 g) = min(12.35 g, 10.948 g) = 10.948 g

(The DIAAS-based figure is also separately capped at 1.0 when DIAAS exceeds 1.0, since digestible complete protein can never exceed total protein either way.)

---

##### Step 6 — Interpreting the result

A composite [DIAAS](#gloss-diaas) ≥ 1.0 means the meal's protein is fully complete relative to the [FAO](#gloss-fao) reference. Values below 1.0 indicate partial completeness — the lower the value, the more the [limiting amino acid](#gloss-limiting-amino-acid) constrains usable protein.

For this meal:

- **Leucine** is the limiting [IAA](#gloss-iaa) at 0.921. This is not surprising: leucine is the most abundant IAA in animal proteins, but plant proteins generally provide less of it relative to total protein.
- **Valine** is also below reference at 0.942. The combination of one legume and one pseudo-cereal improves but does not fully resolve either gap.
- **Lysine**, which is the classic weak point of grains, is met here (1.025) — the pinto beans contribute the lysine that quinoa alone would not cover.
- **[Met+Cys](#gloss-met-cys)** is nearly exactly met at 0.998 — essentially at the reference.

The [DCP](#gloss-dcp) of 10.948 g from 13.41 g of raw protein means that roughly 2.46 g of protein per meal is rendered non-contributory — most of that from the digestibility gap between the two foods, with the leucine shortfall further capping the naive DIAAS-only estimate. In practical terms, this is still a high-quality plant-protein meal — [DIAAS](#gloss-diaas) above 0.9 is considered "good quality" by the [FAO](#gloss-fao).

---

##### Step 7 — Reproduce this in NuMa and compare

To run the same analysis in [NuMa](#gloss-numa):

1. From the main menu, select **Meals & Log**.
2. Create a new meal and add two foods:
   - Search for **pinto beans cooked** → select [FDC](#gloss-fdc) 173796 ("Beans, pinto, mature seeds, cooked, boiled, with salt")
   - Enter a portion of **100 g**
   - Add a second food: search for **quinoa cooked** → select [FDC](#gloss-fdc) 168917 ("Quinoa, cooked")
   - Enter a portion of **100 g**
3. Save the meal and open it. The meal page itself is the analysis screen.
4. Scroll to **Protein Summary** (total protein and DCP) and **Protein Analysis (DIAAS)** (composite score and per-[IAA](#gloss-iaa) ratios), or click those headings in the side outline.

[NuMa](#gloss-numa) will display:
- Total protein
- Composite [DIAAS](#gloss-diaas) score
- Digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp))
- A per-IAA ratio table identifying the [limiting amino acid](#gloss-limiting-amino-acid)

Compare the values [NuMa](#gloss-numa) shows with those in Table I-7 above. They should match to at least three significant figures. If they do not, please report the discrepancy at the project issue tracker.

---

##### Step 8 — Bonus: validating a protein-complement suggestion (quinoa + black beans)

The steps above validate [DIAAS](#gloss-diaas)/[DCP](#gloss-dcp) for a fixed, user-chosen pair of foods. This bonus section validates the *other* half of NuMa's protein-quality math — how it decides which complement food to suggest, and how much of it — using the same quinoa (FDC 168917) from Step 1 as the starting point. See [Protein Complement Suggestions](#comp) for the plain-language version of this logic.

**Quinoa alone has two amino acid gaps.** Using quinoa's own digestibility coefficient (0.85, Mathai et al. 2017 — same source as Step 3) and the Table I-2 amino acid values, quinoa's digestibility-adjusted scores are:

| [IAA](#gloss-iaa) | Adjusted score | Gap? (< 0.95) |
|-----|---------------:|:--------------:|
| Histidine | 1.533 | No |
| Isoleucine | 1.011 | No |
| **Leucine** | **0.827** | **Yes — primary (lowest)** |
| Lysine | 0.962 | No |
| [Met+Cys](#gloss-met-cys) | 1.335 | No |
| [Phe+Tyr](#gloss-phe-tyr) | 1.263 | No |
| Threonine | 1.012 | No |
| Tryptophan | 1.522 | No |
| **Valine** | **0.893** | **Yes — secondary** |

(These scores use quinoa's own [DIAAS](#gloss-diaas)-context digestibility, 0.85 — a single food is scored at its own digestibility, unlike the pinto+quinoa *meal* used in Steps 1–7, where digestibility is applied after pooling. See [Protein Completeness](#complete).)

**The candidate: Black beans, cooked** — one of the 25 entries in NuMa's curated complement table[^10] (not itself in the user's pantry or cache). Per 100 g: 8.86 g protein, 0.677 g leucine, 0.452 g valine, true ileal digestibility 0.80 ([FAO](#gloss-fao) Food and Nutrition Paper (FNP) 92, 2013 — distinct from its [DIAAS](#gloss-diaas) of 0.75; see Step 3 above for why these are different numbers).

**The gap-closer formula.** NuMa solves for the grams `X` of the candidate needed so the *combined* pool's target-[AA](#gloss-aa)-to-protein ratio reaches the [FAO](#gloss-fao) reference, using the base food's own digestibility as the conversion factor:

    alpha = candidate's target AA (g) per g of food       = 0.677 / 100   = 0.00677
    beta  = candidate's protein (g) per g of food          = 8.86  / 100   = 0.0886
    R     = FAO reference (g AA / g protein), inflated
            for the base food's digestibility                = (61.0 / 1000) / 0.85 = 0.071765
    X     = (R × base_protein − base_target_AA) / (alpha − R × beta)
          = (0.071765 × 4.40 − 0.261) / (0.00677 − 0.071765 × 0.0886)
          = 0.054765 / 0.0004119
          ≈ 132.96 g   →  NuMa displays **133 g** (rounded)

**Checking the result.** Adding 133 g of black beans to the 100 g of quinoa gives a combined pool of 16.18 g protein. Recomputing every IAA ratio against this new pool (same method as Table I-7) shows both original gaps closed (the scores below are *raw* — multiply by quinoa's 0.85 for the adjusted figure, e.g. leucine 1.176 × 0.85 = 1.00, valine 1.214 × 0.85 = 1.03) — and, as a side effect neither targeted directly, every other IAA stays comfortably clear too:

| IAA | New raw score (before digestibility) | Gap? |
|-----|--------------------:|:----:|
| Histidine | 1.846 | No |
| Isoleucine | 1.353 | No |
| **Leucine** | **1.176** | **No — closed** |
| Lysine | 1.224 | No |
| [Met+Cys](#gloss-met-cys) | 1.242 | No |
| [Phe+Tyr](#gloss-phe-tyr) | 1.352 | No |
| Threonine | 1.491 | No |
| Tryptophan | 1.720 | No |
| **Valine** | **1.214** | **No — closed** |

This confirms NuMa's Tier 1 result exactly: `gaps_closed: 2`, `new_complete: True`, `closes_primary: True` — a single food closed both gaps, so no Tier 3 two-food cascade ([Two-step combinations](#comb)) was needed here.

**"Total digestible complete protein" — a food page shows an approximation, not the exact pooled figure.** A single food's own page has no ingredient-by-ingredient breakdown to work from — unlike a meal or recipe, it is just one food plus a hypothetical complement — so NuMa falls back to a simpler scale-based estimate rather than the exact per-ingredient pooling used in Steps 1–7 above. The formula:

    new_adj_min = (lowest raw score in the combined pool, from the table above) × quinoa's own digestibility
                = 1.17647 × 0.85 = 1.00000
    old_adj_min = quinoa's own adjusted leucine score (its worst AA before adding anything)
                = 0.82657
    scale       = min(1.0, new_adj_min ÷ old_adj_min)
                = min(1.0, 1.00000 ÷ 0.82657) = min(1.0, 1.2098) = 1.0   (capped)
    Total digestible complete protein
                = (base protein + protein added) × scale
                = (4.40 g + 11.787 g) × 1.0 = 16.187 g  →  displayed as **16.2 g**

The scale factor is capped at 1.0 because a food can never be "more than 100% complete" for DCP purposes — once the combination's weakest amino acid clears the reference, NuMa credits the *entire* combined raw protein pool as digestible and complete. This is a looser approximation than the exact pooled calculation in Steps 1–7 (which applies each food's own digestibility to each amino acid individually, then takes the true minimum ratio) — NuMa's own documentation of this trade-off notes that it can differ from the exact figure by 15–20 g on a real meal. It is used here only because a plain food page has nothing more granular to pool from; meal, recipe, and daily-summary contexts (which do have a real ingredient list) use the exact method instead.

**Reproduce this in NuMa:** open a food page for quinoa, cooked ([FDC](#gloss-fdc) 168917), and look at its [Protein Complement Suggestions](#comp) section. Black beans, cooked should appear in the "General" tier at 133 g, showing "Leucine: 0.83→1.00" and "Valine: 0.89→1.03" under "Amino acid score, now → after", "Adds: 8.8 g digestible protein (from 11.8 g raw protein in this addition)", and "Total digestible complete protein: 16.2 g" — matching every figure derived above.

### B. Blood sugar: glycemic index and load {: #science-glycemic}

*Search terms: blood sugar, glucose, diabetes, carbohydrate quality.*

What glycemic index and glycemic load mean, where NuMa's values come from, how to choose one, and how the published figures compare with what a glucose meter would show you.

#### Glycemic Index {: #gi}

*Search terms: blood sugar, low GI, high GI, carbohydrate quality.*

<!-- t:26-10-10 -->

The glycemic index ([GI](#gloss-gi)) measures how quickly a carbohydrate-containing food raises blood glucose compared to pure glucose ([GI](#gloss-gi) = 100). Low-[GI](#gloss-gi) foods (55 or below) produce a slower, more gradual rise; high-[GI](#gloss-gi) foods (70 and above) cause a faster spike.

**Every [GI](#gloss-gi) figure NuMa shows is one you put there.** Nothing looks [GI](#gloss-gi) up automatically, because no nutrient [database](#gloss-database) NuMa draws on carries it — so a food shows a [GI](#gloss-gi) if, and only if, you supplied one, either by typing it in or by picking a row from the bundled reference table (see [Where GI values come from](#gi-source-para) below). Choosing which published value fits a food is a judgment call, and it stays yours; NuMa won't make it for you. Once saved, the value appears in the **GI** column wherever that food is listed — Food Cache, Pantry, food search, a meal's add-food panel — on the food's own page, and in any glycemic load NuMa computes from it.

**What it's good for.** [GI](#gloss-gi) is at its most reliable comparing like with like, where the two foods differ in one respect you're choosing between — this bread against that bread, parboiled rice against sticky rice. But it is genuinely useful across categories too, whenever two foods are candidates for the same job: bread and rice at breakfast really do behave differently, largely because of physical form, and [GI](#gloss-gi) is what tells you so. What *doesn't* survive the comparison is quantity. [GI](#gloss-gi) is measured on a fixed dose of available carbohydrate (usually 50 g) rather than on a serving of food, so two foods with the same [GI](#gloss-gi) can have very different effects at the amounts you'd actually eat. That's what the glycemic load number is for — see [Glycemic Load](#gl).

**What it doesn't capture.** [GI](#gloss-gi) describes a food eaten alone. Combining foods in a meal (especially adding fat, protein, or fiber) physiologically blunts the blood glucose response to the carbohydrates present, by slowing gastric emptying and glucose absorption. However, this effect is not fully captured by glycemic load ([GL](#gloss-gl)) either — see [Glycemic Load](#gl) for why.

NuMa displays [GI](#gloss-gi) for reference only and does not use it in protein quality calculations.

**Where [GI](#gloss-gi) values come from.**{: #gi-source-para} Neither [USDA](#gloss-usda) nor Open Food Facts[^3] tracks [GI](#gloss-gi), so NuMa can't look it up automatically the way it does for calories or protein — you have to supply it, but NuMa makes that easy. Every food's [Food Cache](#food-cache-web) → **Annotate** page has a **"Look up a GI value from the published reference table"** section: type the food's name (already pre-filled for you), pick which subject population you want — normal glucose tolerance, impaired glucose tolerance/diabetes, or both — and NuMa searches the full published reference table[^8] — about 2,500 foods as shipped, or over 4,000 if you [add the newer edition](#gi-editions) — and lists every plausible match, not just its single best guess. Click **Use this GI value** next to whichever one actually matches your food and its value fills the [GI](#gloss-gi) field; nothing is written until you save the annotation.

When you add a food to your Pantry or a meal and it has no [GI](#gloss-gi) or [DIAAS](#gloss-diaas) estimate yet, NuMa offers to take you to its Annotate page to add them — and keeps offering each time until you save that page once (leaving a value blank on purpose counts). Adding a food to a recipe doesn't prompt. That way your data builds up naturally through normal use, even without visiting Annotate directly.

##### Normal and impaired — which people a value was measured in {: #gi-populations}

Every search result is labeled with the subject group the value was actually measured in, taken from that row's own entry in the table[^8] rather than inferred from anything else:

* **Normal glucose tolerance** — ordinary healthy volunteers. This is the bulk of the table and the default assumption behind any [GI](#gloss-gi) figure you see quoted anywhere.

* **Impaired glucose tolerance** — people with type 1 or type 2 diabetes, gestational diabetes, or diagnosed impaired glucose tolerance ([what this covers, and how to use such a value](#gi-impaired)). Where the table gives the number of subjects, NuMa shows that too (`Type 2, n=9`), because a nine-person study and a thirty-person study do not deserve equal weight.

* **Subject group not stated** — the table didn't record who the value was measured in. These appear in *both* the normal and impaired lists rather than being hidden from both, since a value with an unrecorded population is still a real measurement; the label tells you to treat it cautiously.

Which of these to pick for your own foods is covered next.

##### Choosing a GI value — which result to use for a food {: #choosing-gi-values}
<span id="gi-value-choice"></span><span id="choosing-gi-value"></span><span id="which-gi-value"></span><span id="picking-a-gi-value"></span><span id="gi-population-choice"></span>
*Search terms: choosing GI values, GI value choice, which GI value to use, picking or selecting a GI, best GI result, normal or impaired glucose tolerance, GI for diabetes.*

A lookup on a food's Annotate page often lists several plausible results with different [GI](#gloss-gi) values. Which one you save matters more than anything else about your [GI](#gloss-gi) data: every [glycemic load](#gl) NuMa shows for that food, and for every meal and recipe that uses it, follows from it.

**First, pick the population that matches you.**

- **If you have normal glucose tolerance**, prefer a normal-tolerance result whenever one exists for your food. Use an impaired one when it's all there is, and treat it as a rough indication rather than a number to plan around — see [using such a value](#gi-impaired).
- **If you have diabetes, pre-diabetes or insulin resistance**, the impaired-tolerance values are the ones measured in people like you, and are worth preferring where they exist — best of all those whose subjects had your own type (type 1 or type 2).

Setting **Your glucose tolerance** under [Settings](#settings) → 1. Your Profile makes the lookup show your population's results first, and tailors the notes NuMa shows beside impaired-tolerance values.

**Then, among the results for your population, prefer in this order:**

1. **The same food, prepared the same way.** Boiled versus baked, whole grain versus flour, and cooking time all change [GI](#gloss-gi) a lot.
2. **Rows not flagged "non-ISO method"** — studies that followed the international measuring standard, [ISO](#gloss-iso) 26642 ([more](#gi-method-quality)).
3. **More recent studies, with more people tested and a smaller ± (standard error).** See [How to read a lookup result](#gi-result-row).

**When the table doesn't have your food.** Many everyday foods have no row of their own: search "peanut butter" and every row is a bar or biscuit that contains it. The lookup then says **No row in the table is "peanut butter" itself** above the results, so you know not to take one of them for the food. Below the results it lists **Possible stand-ins**: plain rows for each word of your search, such as "Peanuts". Use a stand-in only if your food is mostly that ingredient (whole peanuts for peanut butter, but not butter). A stand-in's saved source says it was used as a stand-in. When rows score equally, plain foods are listed before a named company's product. The search box starts with the food's full name, such as "Peanut butter, smooth style, with salt"; the lookup reads the part before the first comma as the food and the rest as its description, so you rarely need to shorten it yourself.
<span id="gi-stand-in"></span>

**If nothing is a genuine match, leave the value blank.** No value is better than a wrong one: a blank shows up honestly as a gap ("at least…", "covers N% of the carbohydrate"), while a wrong number looks exactly like a right one. The one exception is a food with very little carbohydrate, where any sensible value gives nearly the same result — see [Foods with no GI anywhere and little carbohydrate](#gi-low-carb).

See also the [GI](#gloss-gi) caveats in [Glycemic load (GL) and Blood Glucose Comparison](#appendix-gl-comparison).

##### Foods with no GI anywhere and little carbohydrate {: #gi-low-carb}
<span id="gi-no-value"></span><span id="gi-estimate-by-analogy"></span>
*Search terms: no GI found, GI not available, low-carb food GI, seeds and nuts GI, hemp seed GI, estimating a GI, GI by analogy.*

Some foods have no [GI](#gloss-gi) in any table, and probably never will: hulled hemp seed, many seeds and nuts, and other foods made up mostly of fat and protein. That's because of how [GI](#gloss-gi) is measured. Under the international standard ([ISO](#gloss-iso) 26642), the people being tested eat a portion containing 50 g of available carbohydrate (sometimes 25 g), and their blood-glucose rise is compared with their rise after the same amount of pure glucose. Hulled hemp seed has about 4.7 g of available carbohydrate per 100 g (8.7 g carbohydrate less 4 g fiber), so a 50 g test portion would mean eating more than a kilogram of it at one sitting. Nobody tests foods like that, so the tables leave them out.

**For these foods the GI hardly matters.** [GL](#gloss-gl) is [GI](#gloss-gi) × grams of available carbohydrate ÷ 100, and the carbohydrate is so small that the [GL](#gloss-gl) stays near zero whatever [GI](#gloss-gi) you use. Three tablespoons of hemp seed (30 g) has about 1.4 g of available carbohydrate: a [GL](#gloss-gl) of about 0.2 at a [GI](#gloss-gi) of 15, and still only 0.7 at a [GI](#gloss-gi) of 50. By comparison, a slice of white bread is around 10.

**But NuMa still needs a value.** A food counts as carbohydrate-free only below 1 g of available carbohydrate in the amount eaten (see [Glycemic Load Output](#glycemic)). A typical serving of a seed or nut is usually just over that, so without a [GI](#gloss-gi), every meal and recipe that uses it shows its [GL](#gloss-gl) as incomplete, even though the missing share is tiny. Ticking **Don't prompt me for a GI estimate for this food again** stops NuMa asking, but doesn't change this: the figure stays incomplete, with the food listed as "marked don't prompt me".

**What to do: save an estimate, and say it's one.** On the food's Annotate page:

1. **Choose a value by analogy.** Take the [GI](#gloss-gi) of tested foods that are made up the same way: mostly fat and protein, with some fiber and little sugar or starch. Search the lookup for such foods (other seeds, nuts) and use a typical value from among them. A food with essentially no starch, such as hemp seed, belongs at or below their usual range rather than above it. A low value in the teens is a reasonable working figure for hemp seed. Because of how little carbohydrate there is, being somewhat wrong costs almost nothing.
2. **Type it into the GI box.**
3. **Say where it came from** in **Where this GI value came from**, so it can't later be mistaken for a measured value, for example: *"Estimate by analogy with tested seeds and nuts; no measured GI exists for this food."*

The ready-made prompt asking Claude AI (under the lookup) can help with step 1, but check that its answer says plainly whether its figure was measured or inferred. For a food like this it will almost always be inferred.

**This is the exception to "no value is better than a wrong one".** For a food with real carbohydrate content, a guessed [GI](#gloss-gi) can move a meal's [GL](#gloss-gl) a long way, so leave it blank (see [Choosing a GI value](#choosing-gi-values)). For a food with very little carbohydrate, a labeled estimate gives a complete and practically correct [GL](#gloss-gl), while a blank gives an "incomplete" warning about almost nothing.

##### Daily glycemic load target {: #gl-target}

*Search terms: GL target, daily GL limit, glycemic load ceiling, blood sugar limit.*

An optional personal ceiling for a whole day's [GL](#gloss-gl), set under **Settings → 1. Your Profile** (**Daily glycemic load target**; leave it blank to turn it off). It's a *limit*, shown the way a nutrient's maximum is: under it is good. Not sure what number to use? **Help me choose a target**, right under the box, offers three starting points with their reasons — see [Choosing a daily glycemic load target](#gl-target-choose).

Where it shows, once set:

- **A day's pages** (the day view, the Daily Summary for a date, the day printout) — under the Glycemic Load figure: "Your daily target: 80 — 64%", or "— over it" in the over-limit color, or "close to it" from 80% up.
- **Recent Days** — the **Day GL** figure is colored against the target; hover for the percentage.
- **Nutrient averages over a period** — how many days in the window were over it.
- **[What-if: Meals](#whatif-gl)** — days over it *before and after* your changes. An average can sit comfortably under the target while several days are over it; this count shows those days, and whether a change fixes them.

**Days with missing GI values.** A day's [GL](#gloss-gl) counts only foods with a [GI](#gloss-gi), so it's a lower bound when some are missing. If that lower bound is already over the target, the day is over for certain and is shown so. If it's under, NuMa says it can't tell yet rather than calling it under — the missing foods could push it over.

Like the rest of your profile, the target is [pinned to each day](#day-profile) as it's logged, so changing it later doesn't rewrite how past days were scored.

##### Choosing a daily glycemic load target {: #gl-target-choose}

*Search terms: GL target, what number, recommended GL.*

**There is no official number.** No diabetes or nutrition guideline sets a daily [GL](#gloss-gl) target. The American Diabetes Association's Standards of Care set none, and the UK's NICE (National Institute for Health and Care Excellence) and Diabetes Canada recommend low-[GI](#gloss-gi) carbohydrate choices without giving a figure[^64]. The research shows a slope, not a line: across large long-term studies, the risk of type 2 diabetes rises steadily with daily [GL](#gloss-gl), with no level below which it stops mattering[^63]. So any target is a point you choose on that slope — lower is better, on average — and the useful question is which starting point suits you.

**Help me choose a target**, under the target box in [Settings](#settings) → 1. Your Profile, offers three. Click one to fill the box, then save.

1. **Scaled to your calorie target (recommended).** 80 × your daily calorie target ÷ 2,000 — for example, 96 for 2,400 kcal, 64 for 1,600. *Who it suits:* most people. It starts from the University of Sydney GI Foundation's description of a "moderate" [GL](#gloss-gl) diet, an average daily [GL](#gloss-gl) under 80 per 2,000 kcal[^61], and scales it to how much you actually eat, so a large or active person isn't held to a small person's number. NuMa takes your calorie target from your profile (see [Daily Nutrient Goals](#goals)). *Limits:* the Foundation states the figure without saying what study it comes from.
2. **The common convention: 80.** *Who it suits:* anyone who wants the figure most often quoted for a "low glycemic load day", the same for everyone. *Limits:* it's widely repeated — for example by the UK's advertising regulator — but nobody cites a study for it[^62], and it doesn't allow for body size or activity. For someone eating well over 2,000 kcal, option 1 is fairer.
3. **A step down from where you are.** Your own average daily [GL](#gloss-gl) over the last 30 days, minus 10–20% (NuMa fills in the middle of that range). *Who it suits:* someone who wants a gradual, achievable change rather than a jump to an outside number — and whose current average is already near or below the others, who'd learn nothing from them. *Limits:* it's not a published target; it rests only on the finding that lower is better on average[^63]. It needs at least 7 days in those 30 with a complete [GL](#gloss-gl) (every food with carbohydrate has a [GI](#gloss-gi)); fewer, and NuMa doesn't offer it, since the average would mean little.

**If you have diabetes, pre-diabetes or insulin resistance**, set the number with your doctor or dietitian. Any of the three can be a starting point for that conversation, but none is a treatment target, and your own glucose readings ([CGM](#gloss-cgm), if you use one) are the better guide — see [Glycemic load (GL) and Blood Glucose Comparison](#appendix-gl-comparison).

##### What "impaired glucose tolerance" means here, and using such a value {: #gi-impaired}

*Search terms: prediabetes.*

**It's NuMa's umbrella label, not one condition.** Strictly, IGT (impaired glucose tolerance) is a specific finding: blood glucose two hours after a standard glucose drink of 7.8–11.0 mmol/L (140–199 mg/dL) — higher than normal, below the diabetes threshold, one of the forms of "pre-diabetes". NuMa uses the phrase more broadly, for every value *not* measured in people with normal glucose tolerance. In the 2021 tables that means rows whose subjects had:

* **type 2 diabetes** — the large majority;
* **type 1 diabetes** — about one row in five;
* **gestational diabetes** (diabetes first appearing in pregnancy), **IGT** in the strict sense, or a **mixed** group — a handful each.

The lookup result shows which (`Type 2, n=9`), and so does "Value taken from" on the food's page once you've saved it. In the 2008 tables, the whole second list of values (measured in "subjects with impaired glucose tolerance or diabetes") gets this label; that edition doesn't break it down further.

**Why the group matters, and why it often matters less than you'd think.** A [GI](#gloss-gi) is a *ratio*: each subject's blood-glucose rise after the food, divided by the same subject's rise after pure glucose. Because each person is their own yardstick, much of the difference between people cancels out, and comparisons of the same foods in people with and without diabetes have generally found the average values broadly similar. But "broadly similar on average" isn't "the same": results vary more from person to person in people with diabetes, and in type 1 diabetes the result also depends on the insulin given with the test meal. The international standard for measuring [GI](#gloss-gi) ([ISO](#gloss-iso) 26642) calls for healthy subjects, so normal-tolerance values are the reference ones.

**If you do *not* have diabetes, pre-diabetes or insulin resistance**, and the only value for a food was measured in this group:

1. **Look for a normal-tolerance row first** — the same food, or a very close one. If there is one, use it instead.
2. **Otherwise, use the value as an approximation.** It's usually in the right range — good enough to tell a low-[GI](#gloss-gi) food from a high one — but don't read much into small differences. Two foods 5–10 points apart may not really differ for you.
3. **Prefer type 2 over type 1 rows**, and larger studies (higher *n*) over smaller ones, when you have a choice.
4. **When comparing two foods, try to use values from the same group** for both, so the comparison isn't skewed by the groups rather than the foods.

**If you do have diabetes, pre-diabetes or insulin resistance**, these are the values measured in people like you — prefer them, and the closer the match (type 2 rows if you have type 2), the better. Whatever group a value comes from, your own response is the final word: see [Continuous Glucose Monitoring](#appendix-gl-comparison).

**Where NuMa reminds you.** Once you've saved a value picked from an impaired-tolerance row, NuMa marks it wherever it matters: a note under the value on the Annotate page and the food's own page; a **†** beside its [GI](#gloss-gi) in Top Contributors ranked by glycemic load and in [lower-GI swap](#gl-swaps) suggestions; and, under a meal's, recipe's or day's Glycemic Load figure, a line naming each food whose [GI](#gloss-gi) came from such a row. What the note says depends on **Your glucose tolerance** under [Settings](#settings) → 1. Your Profile: set to impaired, it tells you the value fits you (best when the study's subjects had your own type); set to normal, it tells you to treat the value as an approximation and prefer a normal-tolerance one where the table has it; not set, it gives both readings and offers a link to set it. A value you typed by hand, or picked from a normal-tolerance or not-stated row, isn't marked.

By default the lookup searches both populations at once. If you'd rather it default to just one — say, you have diabetes and always want the impaired-tolerance values shown first — set **Your glucose tolerance** under [Settings](#settings). You can still switch populations for any individual lookup regardless of that default.

##### Method quality, and why some rows are flagged {: #gi-method-quality}

*Search terms: study quality, flagged rows.*

Subject group is one axis; how well the study was run is a separate one, and the table[^8] splits its rows on exactly that. There is an international standard for measuring [GI](#gloss-gi) — [ISO](#gloss-iso) (International Organization for Standardization) 26642:2010 — which sets out how much carbohydrate the test portion must contain, how many people must be tested, and when blood must be sampled.

* Rows from studies that **met** that standard carry no flag. They are the bulk of what you'll see, and they are the ones to trust.

* Rows from studies that **deviated** from it are marked **non-ISO method**. The deviation might be fewer than ten subjects, a test portion with an unusual amount of carbohydrate, an unrepeated reference food, or results whose [standard error](#gloss-standard-error) was wide enough that the average is shaky.

A **non-ISO method** flag is not a warning about the food — it's a warning about the *evidence*. Be especially wary when a flagged value looks extreme, since an implausibly low or high figure is exactly what a tiny or high-variance study tends to produce.

Note that the two things are genuinely independent: most non-ISO rows were still measured in normal-tolerance subjects, and an unflagged row can still have been measured in people with diabetes. That's why NuMa shows them as two separate pieces of information rather than rolling them into one tag.

##### How to read a lookup result {: #gi-result-row}

*Search terms: reading a GI row, test year.*

A search for "black beans" might return a row like this:

```
Beans, dried, boiled, type NS      GI 20 ±3    tested 1998 · non-ISO method    Impaired glucose tolerance (Type 2, n=8) · ref 76
```

Reading it left to right:

* **Beans, dried, boiled, type [NS](#gloss-ns)** — the food exactly as the study described it. **type NS** means "type not specified": the researchers didn't record which bean it was, so this row may or may not be about black beans at all. Names are often long, and deliberately so — the 2021 edition of the table[^8] describes cooking method, processing and brand where it knows them, which is usually what tells you whether a row is really your food.

* **[GI](#gloss-gi) 20 ±3** — the value itself, always on the glucose-referenced scale (glucose = 100), which is the scale NuMa uses everywhere. The **±3** is the study's own [standard error](#gloss-standard-error): how much the individual subjects' results scattered around that average. A small figure means the subjects broadly agreed; a large one (±15, say) means they didn't, and the average is correspondingly shaky. Some rows have no standard error published, in which case none is shown.

* **tested 1998** — the year the study was run, which is the most useful thing on the row after the value itself. A [GI](#gloss-gi) measured on a commercial product decades ago may no longer describe what's in the packet today, since recipes get reformulated. Hover over the date for the food's country of production and which published table the row came from. Rows carried over from the older 2008 edition of the tables say **2008 edition** instead, because that edition didn't record a year of test at all — see below.

* **non-ISO method** — present only when the study deviated from the international [GI](#gloss-gi) measurement standard, [ISO](#gloss-iso) 26642, as described under [non-ISO method values](#gi-method-quality). Most rows don't have it.

* **Impaired glucose tolerance (Type 2, n=8)** — the subject group and, where the table says, how many people were tested.

* **ref 76** — which study the value came from: entry 76 in the table's own reference list[^8]. A code beginning **UO** instead (UO4, UO5…) means "unpublished observations" — data the table's authors held but never published as a paper, so there is nothing to look up.

That row, in plain English: *someone fed unspecified boiled dried beans to eight people with type 2 diabetes in 1998, using a method that departed from the standard in some way, and the glucose-scale answer was 20, give or take 3.*

Nothing about a row obliges you to use it. When two or three plausible rows disagree, it's entirely reasonable to pick the one whose description best matches the food you actually eat, or to skip the lookup and type a value of your own. Where rows disagree, the date and the [standard error](#gloss-standard-error) are usually what settles it.

##### What NuMa keeps from a lookup {: #gi-what-is-stored}

*Search terms: GI source, saved GI, where a GI came from.*

Clicking **Use this GI value** copies the number into the food's [GI](#gloss-gi) field, and records the row it came from alongside it — one line naming the edition and published table, the entry's own food name, when and where it was tested, and who in, like this:

```
Atkinson 2021 international GI tables, Supplemental Table 2 (method deviations):
"Beans, dried, boiled, type NS" · tested 1998, Italy ·
Impaired glucose tolerance (Type 2, n=8) · ref 76
```

A value picked from a row carried over from the 2008 edition records that instead, and says plainly that no year of test exists for it:

```
Atkinson 2008 international GI tables (carried forward; year of test not
recorded): "Muesli, toasted" · Normal glucose tolerance · ref 42
```

That line appears under the [GI](#gloss-gi) box on the Annotate page, and on the food's own page underneath its name, so a value you saved months ago can still be traced back to the entry behind it. It is saved when you save the annotation, like everything else on that page.

Two things worth knowing about it. First, **typing over the number by hand clears it** — a figure you supplied yourself isn't the table's, so keeping the old citation next to it would be a lie. Type your own value and the food simply shows a [GI](#gloss-gi) with no source line; use **Prep context** if you want to say where your own figure came from. Second, clearing the [GI](#gloss-gi) field clears the source with it, since it describes nothing on its own.

Two things NuMa deliberately does not do with the table:

* **It never rescales.** The published table prints two [GI](#gloss-gi) columns — glucose = 100 and bread = 100 — and NuMa reads only the glucose-referenced one. The "ref Bread" in a row describes what that study fed as its comparison; the table's authors already converted the result onto the glucose scale. So a bread-referenced row's value needs no adjustment and is directly comparable to every other [GI](#gloss-gi) figure in NuMa.

* **It never imports glycemic load.** The table publishes a [GL](#gloss-gl) for each row, computed from the serving the study happened to test. NuMa ignores it and computes [GL](#gloss-gl) live from your food's own cached carbohydrate content and the amount you actually ate — which is more accurate for that specific food than rescaling somebody else's tested portion. See [Glycemic Load](#gl).

##### Upgrading to the 2021 tables {: #gi-editions}

*Search terms: upgrade GI table, Atkinson, newer GI data, build GI table.*

NuMa ships with the **2008** edition of the *International Tables of Glycemic Index and Glycemic Load Values*[^8a] — about 2,500 foods. A **2021** edition[^8] exists with over 4,000, and it carries information the 2008 one doesn't: the year each study was run, its [standard error](#gloss-standard-error), the country the food came from, how many people were tested, and whether the study met the international measurement standard.

NuMa can't ship that newer edition, for a straightforward reason. The 2008 edition is Creative Commons licensed, so it can be copied and distributed freely, which is why it's the one built in. The 2021 edition is published under a license that expressly **permits you to download it and extract data from it for your own non-commercial use**, but **forbids redistributing it**. So NuMa includes the tool that reads it, and you supply the document — which the license entitles you to do.

**What to do** — it's all in one place, **Settings → 7. Glycemic Index Reference Table**:

1. Open the 2021 article's page at the publisher[^8] (the section links straight to it), find its **Supplementary data** section, and download both PDFs there — Supplemental Table 1 and Supplemental Table 2. NuMa can't fetch them for you: the publisher's site turns away programs, and only a person can collect them.
2. Back in that Settings section, choose both files together (hold Ctrl, or Shift, to pick the second one). The order doesn't matter — NuMa reads which table is which from the PDFs themselves.
3. Click **Build my 2021 GI table**.

It takes about a minute. The section shows a "Building…" message and refreshes itself until it's done, then says how many foods it read. From then on the Annotate page's [GI](#gloss-gi) lookup searches the new table, straight away, with no restart. The PDFs aren't kept, only the table built from them. If you pick the wrong files — the same table twice, or some other document — NuMa says so and changes nothing, and if you already had a 2021 table it stays in use. To rebuild later (a fresh download, say), the same button is there, relabelled **Rebuild**.

That file is yours alone. It isn't shared, uploaded, or included in anything NuMa distributes, and it shouldn't be passed on to anyone else — the same license that lets you build it is what stops it being handed around.

**What you'll see afterwards.** Results gain a date and the other detail described in [How to read a lookup result](#gi-result-row). A few hundred foods that appear only in the 2008 edition are kept alongside the newer ones, labeled **2008 edition**, so nothing is lost in the upgrade. Those carry no year, standard error or country, because that edition never published them in a form NuMa captured.

One honest caveat about that set: the 2021 authors rewrote most food descriptions — moving brand names around, adding cooking detail — so deciding which 2008 foods 2021 *doesn't* already cover means comparing reworded descriptions, with no shared identifier to match them by. NuMa deliberately errs toward keeping a 2008 row when it can't tell. The cost is the occasional near-duplicate pair in your results, one of them without a date; the cost of the opposite choice would be silently losing foods. If you see such a pair, take the 2021 one.

##### Why these tables instead of the University of Sydney database {: #gi-why-foster-powell}

*Search terms: GI database, why not Sydney.*

Two candidate sources exist for bulk [GI](#gloss-gi) data, and they're related but not the same. Brand-Miller — a co-author of the published tables[^8] — also runs the University of Sydney's GI research group, and a great many entries in those tables came from the Sydney group's own lab testing, so there's real lineage and overlap between the two.

But they differ in ways that matter for a bulk local lookup table. The published tables are a fixed, peer-reviewed, citable snapshot: a static document that can be read into a file once and then work offline and identically every time — and in the 2008 edition's case, explicitly Creative Commons licensed, so NuMa can ship it outright. The Sydney [database](#gloss-database) (glycemicindex.com) is a live, continuously updated, searchable website — larger and more current, but a site to query rather than a table with a clear bulk-redistribution license; scraping it for a local table would be a licensing gray area at best.

That's why NuMa's built-in table comes from the published tables, and why glycemicindex.com is listed in [Internet resources](#internet-resources) as a manual look-up fallback rather than something NuMa imports from directly.

#### Glycemic Load {: #gl}

*Search terms: blood sugar, carbohydrate amount, carbs.*

Glycemic load ([GL](#gloss-gl)) improves on the glycemic index by accounting for both the quality and the quantity of carbohydrate in a serving[^69]. The formula is:

```
GL = (GI × grams of available carbohydrate) / 100
```

For a meal combining multiple foods, the total [GL](#gloss-gl) is the sum of the [GL](#gloss-gl) calculated separately for each component:

```
Meal GL = GL(food 1) + GL(food 2) + GL(food 3) + ...
```

So adding carbohydrate foods always raises a meal's total. What the calculation can't show is that eating foods together blunts the blood-sugar rise: protein, fat and fiber slow digestion and absorption. Gram for gram, protein lowers the rise about twice as much as fat[^89], and thick (viscous) fiber, as in oats and legumes, does it best[^90]. Because GL uses each food's GI measured alone, it's reliable for comparing meals of broadly similar make-up[^91], less so when fat or protein differ a lot[^92].

A high-GI food can have a low GL if a serving has little carbohydrate (watermelon is the classic case), and a moderate-GI food in a big portion a high one. So GL is generally the better guide to real-world effect.

**GL has two scales, and mixing them up is the commonest misreading.** A food, serving, meal or recipe portion uses the per-serving scale:

| Per-serving [GL](#gloss-gl) | Classification |
|---|---|
| 10 or below | Low |
| 11–19 | Medium |
| 20 or above | High |

A whole day, a much larger number, uses its own:

| Daily total [GL](#gloss-gl) | Classification |
|---|---|
| Below 80 | Low |
| 80–120 | Moderate |
| Above 120 | High |

**Treat the daily scale loosely.** The per-serving bands are published with the international GI tables and well established; the daily ones are a convention, defined inconsistently (the University of Sydney group calls under 80 per 2,000 kcal a *moderate* diet, not a low one). A day's GL also rises with how much you eat, so a large or active person runs higher without anything being wrong. NuMa shows the daily band for orientation, with that caveat.

NuMa shows GL for every food (per 100 g and for the portion shown: halve the portion and GL halves while GI stays put, which is the point of it), recipe (per serving), meal and day, marked incomplete when foods lack a GI ([details](#glycemic)). Recipes, meals and days also get an [estimated GI](#mixture-gi). GL doesn't affect protein scores.

**Averages beat single days.** One day's GL swings with what you happened to eat. [Nutrient averages over a period](#trend) gives the average over 7, 14 or 30 days (skipping incomplete days, and saying how many counted), and the [Nutrient Plot](#nutrient-plot) can plot **Daily glycemic load** to show patterns such as weekends or late evenings.

How GL compares with glucose monitors and prediction apps, especially for diabetes: [GL and blood glucose](#appendix-gl-comparison).


##### What you can do with GI and GL {: #gl-uses}

*Search terms: using GI, using GL, lower blood sugar, practical use.*

GI values are only worth entering if they help you choose. How NuMa puts them to work:

1. **Read a meal's or recipe's GL and band**, under **Glycemic Load** (per serving for a recipe); a day's is on its pages and in Recent Days' **Day GL**, on the day scale.
2. **See which foods drive it**: **Which foods drive it, and lower-GI swaps to try** ranks them ([Top Contributors](#top-contributors)). Usually one or two carry most of it.
3. **Change one.** In rough order of effect: a **smaller portion**; a **swap** to a similar lower-GI food (NuMa [suggests some](#gl-swaps)); or **pairing** it with fat, protein, fiber or acid (vinegar, lemon), which slows absorption[^89]<sup>,</sup>[^90]<sup>,</sup>[^93], though the GL number can't show it.
4. **Check the whole picture first:** each swap suggestion opens [What-if](#whatif-gl), showing GL and every other nutrient before and after.
5. **Compare candidates:** [Compare](#compare-gl) shows GI and GL per 100 g for up to 8 items.
6. **Set a [daily target](#gl-target)** if it helps.
7. **Watch the trend**, not the day ([averages](#trend), the plot).
8. **Keep the figures honest:** "at least" and "covers N% of the carbohydrate" mean some foods lack a GI; [Foods you use with no GI](#missing-gi) lists them. A value measured in people with diabetes is marked ([what that means](#gi-impaired)).

**A worked example.** Say a dinner is 200 g of cooked white rice with chicken and broccoli. Chicken and broccoli have almost no carbohydrate, so the rice is the whole story. Cooked white rice is about 28 g carbohydrate per 100 g ([USDA](#gloss-usda)), so 200 g is about 56 g. The bundled table's "Medium grain white rice, boiled 12 mins" has a [GI](#gloss-gi) of 75: [GL](#gloss-gl) = 75 × 56 ÷ 100 ≈ **42 — High** (20 or more).

Cooked pearled barley also has about 28 g carbohydrate per 100 g, and the table's "Barley, pearled, boiled 60 min" has a [GI](#gloss-gi) of 35. The same 200 g: 35 × 56 ÷ 100 ≈ **20** — less than half, on the High/Medium line. Same amount of food, same carbohydrate; only the kind of carbohydrate changed. (Halving the rice to 100 g instead would give about 21 — similar, but by eating less.)

To try it: give both foods a GI on their Annotate pages, rank the meal's Top Contributors by glycemic load, and follow the barley suggestion's **see the full effect in What-if**.

#### Glycemic load (GL) and Blood Glucose Comparison {: #appendix-gl-comparison}

*Search terms: GL accuracy, individual response.*

Glycemic load is a useful approximation, but no single formula-derived figure reliably predicts an individual's blood glucose response to a mixed meal. Three reasons account for this:

- The fat and protein suppression effect varies by person, by degree of insulin resistance, and by the specific foods involved[^89].
- Most published [GI](#gloss-gi) values were measured in subjects with normal glucose tolerance and may not translate directly to someone with diabetes or insulin resistance. NuMa's built-in reference table[^8] does include a separate set of values measured specifically in subjects with impaired glucose tolerance — see [Where GI values come from](#gi) — ([what that group covers](#gi-impaired)), but that set is smaller and doesn't exist for every food, so this caveat still applies whenever only a normal-tolerance value is available.
- Individual glucose responses to identical meals vary substantially between people[^112], and even in the same person on different days: in one study, a single person's measured GI for the same white bread varied more from one test to the next than people varied from each other[^113].

[GL](#gloss-gl) is therefore most reliable when comparing meals of broadly similar composition — two different grain-based breakfasts, for example. When meals differ significantly in fat or protein content, the calculated [GL](#gloss-gl) will understate the difference in actual glycemic impact.

##### Continuous Glucose Monitoring

*Search terms: continuous glucose monitor, glucose monitor.*

The practical gold standard today is continuous glucose monitoring ([CGM](#gloss-cgm)) — devices such as the Dexcom G7 or Libre 3 that measure interstitial glucose every few minutes. A person with diabetes can eat a meal, watch their glucose curve in the accompanying app, and directly compare their own real response across different meal choices over time. No formula approaches this for accuracy in individual prediction.

##### Predictive Apps

*Search terms: glucose prediction, personalized nutrition.*

Research has shown that a machine-learning model trained on [CGM](#gloss-cgm) data, together with blood tests, diet, activity and the gut microbiome, can predict an individual's glucose response to a meal before it is eaten, and that diets chosen from those predictions lowered post-meal glucose[^112]. Some commercial apps (January AI, for one) offer predictions of this kind — effectively personalizing the [GI](#gloss-gi) and [GL](#gloss-gl) concepts. These predictions are probabilistic rather than exact, but they represent the closest available alternative to direct measurement.

##### Clinical Practice Without CGM

*Search terms: carb counting, dietitian.*

For clinical guidance without [CGM](#gloss-cgm), dietitians working with people with diabetes typically use carbohydrate counting combined with qualitative judgment about fat and protein content, rather than relying on [GL](#gloss-gl) as a single summary figure. The American Diabetes Association's nutrition consensus report recommends carbohydrate counting for insulin dosing in type 1 diabetes, and says that for a meal with substantial fat or protein, insulin dosing shouldn't rest on carbohydrate counting alone[^114]. [GL](#gloss-gl) remains a reasonable guide for comparing meals similar in structure, but should not be the deciding number when fat and protein differ significantly between the options being considered.

### C. Daily targets {: #science-targets}

*Search terms: nutrient targets, requirements, how much do I need, goals, limits.*

Where your daily targets come from: the official Recommended Dietary Allowances, the age- and sex-adjusted goals NuMa builds from them, optional research-based targets, upper limits, and how a plant-based diet changes what you need.

#### Recommended Dietary Allowances {: #rda}

*Search terms: recommended daily allowance, daily requirements, adequate intake.*

[RDA](#gloss-rda) values in NuMa come from the Dietary Reference Intakes ([DRI](#gloss-dri)) published by the U.S. National Academies of Sciences, by way of the **NIH** (National Institutes of Health) **ODS** (Office of Dietary Supplements)[^9]. Here is the ODS's own definition, word for word:

> "Recommended Dietary Allowance (RDA): Average daily level of intake sufficient to meet the nutrient requirements of nearly all (97–98%) healthy individuals[^9]."

**So an RDA is not a bare minimum:** it covers nearly everyone in your age and sex group, with margin to spare. (The bare-minimum figure, meeting only the *average* person's need, is the EAR (Estimated Average Requirement), a population tool NuMa doesn't use.) Where NuMa calls an RDA a "minimum", it means "meet or exceed this", a direction, not a size; see [Daily Nutrient Goals](#goals) for minimum, target and limit.

Your profile (age, sex, weight, height, activity) sets your targets; [Daily Nutrient Goals](#goals) gives the age and sex bands for every mineral and vitamin. Calories use the Mifflin-St Jeor equation with an activity multiplier. Protein starts at 0.8 g per kg of body weight, rising to 1.0 g/kg at moderate activity and 1.2 g/kg for active and very active people. The 0.8 g/kg comes from the nitrogen-balance research behind the RDAs of the **IOM** (Institute of Medicine, now the National Academy of Medicine)[^60], and it carries an assumption that matters greatly to anyone eating mostly plants:

##### The protein target assumes high-quality protein {: #protein-rda-quality}

*Search terms: protein requirement, 0.8 g per kg, plant protein needs, vegans need more protein.*

The **IOM** (Institute of Medicine)[^60] set 0.8 g/kg for protein **"of mixed quality as typically consumed"**[^60]: the ordinary American diet studied, mostly animal protein, nearly all digestible and complete. It was never "any 0.8 g/kg of anything". The IOM notes needs may be higher on less digestible plant proteins, and the [FAO](#gloss-fao) and **WHO** (World Health Organization) recommend correcting for protein quality on mainly plant-based diets.

In other words, **the protein target is measured in reference-quality protein**, which is exactly what [Digestible Complete Protein](#dcp) measures. So the honest comparison, for everyone, is [DCP](#gloss-dcp) against the target, not raw grams.

For someone eating meat, eggs and dairy, it makes little difference: their pooled [DIAAS](#gloss-diaas) is near 1.0, so DCP and raw protein nearly match, which is why the assumption went unnoticed. On a mostly plant diet they separate, and raw grams flatter the result: a day can show 120% of the target in raw grams and under 90% in usable protein.

**So NuMa shows both:** the **Protein** row (raw intake) and, beneath it, the **(Digestible Complete Protein)** row (usable intake), against the same target. Together they show what your protein quality is costing you. The Protein Summary leads with DCP for the same reason.

**There's no separate protein target for vegetarians or vegans, on purpose.** NuMa raises iron and zinc targets for plant-based diets ([why](#diet-bioavailability)) because their absorption penalty is invisible in the data. Protein's isn't: it *is* the [DIAAS](#gloss-diaas), already measured from your foods and built into DCP, including for mixed diets ([how](#protein-scoring)). A higher target would count the penalty twice.

DCP can only count foods with amino acid data. When some lack it, the DCP row has an asterisk and names them, so you know it's an understatement ([filling the gaps](#aa-note-web)).

The nutrient comparison table, on food, recipe, meal and daily-summary pages, compares intake with targets.

Columns:

<pre>
    Nutrient              Name of the nutrient.
    Total                 How much this food/recipe/meal/day provides (or,
                           on a food page, how much the entered portion provides).
    Unit                  The nutrient's unit (g, mg, mcg).
    Minimum                The RDA/AI figure itself — the amount to meet or
                           exceed. Filled for almost every tracked nutrient;
                           shown only when you've set up a user profile.
    Target                 A two-sided ideal figure — aim close to this
                           amount, not just above or below it. Only Calories
                           uses this today; every other row leaves it blank.
    Maximum                That nutrient's own recommended not-to-exceed
                           amount — a different, more clinically conservative
                           figure than the UL column further right (see the
                           "max vs. UL" note below). Only Sodium uses this
                           today; every other row leaves it blank.
    % of daily target     Total / (Minimum, Target, or Maximum, whichever
                           applies) x 100, color-coded (see below) by how
                           close you are to (or over) it — shown only when
                           you've set up a user profile.
    Revised Optimal goal,
    % of Revised Optimal  A higher daily goal you set yourself, for a
    (Rev. Opt. meal %,     nutrient where more recent research recommends
     Rev. Opt. day %)      more than the RDA (Vitamin D is the usual
                           example). The % columns measure the same total
                           against that goal instead of the Minimum. These
                           columns appear only once you've set at least one
                           such goal in Settings → 5. Nutrient Targets - Researched; a dash
                           means none is set for that row (see <a href="#optimal">Revised
                           Optimal Targets</a>).
    UL                    Shown only where you're near or over a max limit —
                           see <a href="#maxlimits">Maximum Nutrient Limits</a>.
</pre>

**Reading the two protein rows.** **Protein** and the indented **(Digestible Complete Protein)** share a target and a % column; the wider the gap between their percentages, the more protein quality is costing you. An asterisk on DCP means some foods lacked amino acid data (named below the table), so the real figure is higher.

The DCP row leaves **day total %** blank: a day's DCP isn't the sum of its meals' (foods in different meals still complement each other), so NuMa won't show a misleading sum. A day's real DCP is on the [Daily summary](#daily-summary).

Each nutrient's [DRI](#gloss-dri) is one kind, so only one of Minimum, Target and Maximum is filled per row (the others show "—"). A footer under every table explains the four (Minimum, Target, Maximum, UL).

The four colors on % of target: **green**, met (at or above a Minimum, or near a Target); **blue**, near ("almost there", not a warning); **orange**, well below a minimum (a real shortfall); **red**, over a Maximum (only sodium has one now) or, for a Target like calories, well over 100%.

**Maximum and [UL](#gloss-ul) are different ceilings.** A Maximum (sodium) is a recommended not-to-exceed amount, more conservative; the **UL** column is the highest amount safe for nearly everyone. No nutrient has both. More in [Maximum Nutrient Limits](#maxlimits).

Nutrients without a Dietary Reference Intake ([phytonutrients](#gloss-phytonutrients), amino acids) show only the amount. How each goal is worked out: [Daily Nutrient Goals](#goals).


#### Daily Nutrient Goals {: #goals}

*Search terms: daily goals, targets.*

NuMa works out your daily goals from your profile (Settings → 1). Each goal is one of three types:

<pre>
    Minimum  — RDA or Adequate Intake (AI): the daily amount needed to
               meet the requirements of most healthy adults.
    Target   — an estimated ideal intake (currently applies to calories).
    Limit    — a maximum daily amount you don't want to exceed. Sodium has
               its own fixed 2300 mg/day limit (see the sodium note below).
               Twelve other nutrients get an automatic Tolerable Upper
               Intake Level as their default limit — see <a href="#maxlimits">Maximum Nutrient
               Limits</a> for the full list and for setting your
               own custom limit on any nutrient.
</pre>

##### HOW EACH GOAL IS CALCULATED

##### Calories (target)

*Search terms: energy, BMR, TDEE, metabolism, calorie needs, weight loss, losing weight.*

    Mifflin-St Jeor equation for Basal Metabolic Rate, multiplied by an
    activity factor based on your activity level setting:

        Sedentary (desk job, little exercise)           x 1.2
        Lightly active (light exercise 1-3 days/week)   x 1.375
        Moderately active (3-5 days/week)               x 1.55
        Active (hard exercise 6-7 days/week)            x 1.725
        Very active (physical job or twice-daily)       x 1.9

##### Protein (minimum)

*Search terms: protein goal, grams per kg, protein need.*

    Scaled to body weight and activity level:

        Sedentary or lightly active   0.8 g per kg body weight
        Moderately active             1.0 g per kg body weight
        Active or very active         1.2 g per kg body weight

##### Carbohydrates (minimum)

*Search terms: carbs minimum, carbohydrate need.*

    130 g/day — the brain's minimum glucose requirement (fixed for all).

##### Fiber (minimum)

*Search terms: fiber goal, fiber need.*

    Age- and sex-dependent Adequate Intake:

        Men under 50: 38 g/day     Men 50+: 30 g/day
        Women under 50: 25 g/day   Women 50+: 21 g/day

##### Sodium (limit)

*Search terms: salt.*

    2300 mg/day — standard Tolerable Upper Intake Level (fixed for all).

##### Omega-3 ALA (minimum)

*Search terms: omega-3 goal, alpha-linolenic acid, flax.*

<pre>
    1600 mg/day men, 1100 mg/day women — Adequate Intake for alpha-linolenic
    acid (<a href="#gloss-ala">ALA</a>), the plant-sourced omega-3. See <a href="#omega3">Omega-3 Fatty Acids</a>
    for why this is the only omega-3 with an official goal in NuMa.
</pre>

##### Omega-6 linoleic acid (minimum)
<pre>
    17 g/day men, 12 g/day women aged under 51; 14 g/day men, 11 g/day women
    at 51+ ("other": midpoint) — Adequate Intake for linoleic acid. Shown in mg
    like the other omega rows (17000 mg and so on).
</pre>

##### Minerals and vitamins — every age/sex band, in full

*Search terms: older people, seniors, elderly, over 65, aging, women, men, vitamin needs by age.*

Minerals and vitamins use age- and sex-specific values from the US National Academies' Dietary Reference Intakes[^9]. For sex "other", NuMa uses the midpoint of the male and female values, except for the rows marked \*, where the tables give nothing but male and female, so the female value is used.

| Nutrient | Men | Women | Other | Age band that changes it |
|---|---|---|---|---|
| Calcium | 1000 mg (1200 mg at 70+) | 1000 mg (1200 mg at 51+) | 1000 mg (1200 mg at 60+) | Yes — see per-column ages |
| Iron | 8 mg (all ages) | 18 mg under 51, 8 mg at 51+ | 13 mg under 51, 8 mg at 51+ | Yes, women/other only |
| Magnesium | 400 mg (420 mg at 31+) | 310 mg (320 mg at 31+) | 355 mg (370 mg at 31+) | Yes — see per-column ages |
| Potassium | 3400 mg | 2600 mg | 3000 mg | No |
| Zinc | 11 mg | 8 mg | 9.5 mg | No |
| Iodine | 150 mcg | 150 mcg | 150 mcg | No |
| Selenium | 55 mcg | 55 mcg | 55 mcg | No |
| Phosphorus | 700 mg | 700 mg | 700 mg | No |
| Vitamin A | 900 mcg | 700 mcg | 800 mcg | No |
| Vitamin C | 90 mg | 75 mg | 82.5 mg | No |
| Vitamin D | 15 mcg (20 mcg at 70+) | 15 mcg (20 mcg at 70+) | 15 mcg (20 mcg at 70+) | Yes, same for all sexes |
| Vitamin E | 15 mg | 15 mg | 15 mg | No |
| Vitamin K | 120 mcg | 90 mcg | 105 mcg | No |
| Thiamin (B1) | 1.2 mg | 1.1 mg | 1.1 mg\* | No |
| Riboflavin (B2) | 1.3 mg | 1.1 mg | 1.1 mg\* | No |
| Niacin (B3) | 16 mg | 14 mg | 14 mg\* | No |
| Vitamin B6 | 1.3 mg under 51, 1.7 mg at 51+ | 1.3 mg under 51, 1.5 mg at 51+ | 1.3 mg under 51, 1.5 mg at 51+\* | Yes, at 51+ only |
| Folate (B9) | 400 mcg | 400 mcg | 400 mcg | No |
| Vitamin B12 | 2.4 mcg | 2.4 mcg | 2.4 mcg | No |
| Choline | 550 mg | 425 mg | 487.5 mg | No |

Nutrients without [DRIs](#gloss-dri) ([phytonutrients](#gloss-phytonutrients), amino acids) have no goal.

See also: [RDA](#rda) for where the values come from, [Revised Optimal Targets](#optimal) for a different target, [Maximum Nutrient Limits](#maxlimits) for a cap, [Nutrient Averages Across Days](#trend) for shortfalls over time, and the [Full Nutrient Key](#nutrient-key) for each nutrient by name.


#### Profile Revised Optimal (Recent Research) Targets {: #optimal}

*Search terms: research targets, above RDA, revised targets.*

**Two different ideas.** The [RDA](#gloss-rda) already meets the needs of nearly all healthy people in your group[^9]. This section is a *second* tier: nutrients where recent research argues for a target *above* the RDA. NuMa calls it **Revised Optimal (Recent Research)**, never just "optimal", to keep the two apart.

Vitamin D shows how this tier changes. The RDA is 15–20 mcg a day. A 2011 Endocrine Society guideline recommended 37.5–50 mcg for adults at risk of deficiency[^12], and NuMa used 50 mcg. The Society's 2024 guideline replaced it: for healthy adults under 75 it advises *against* going above the reference intakes, suggesting more only from 75 (and for children, pregnancy and high-risk prediabetes)[^101]. NuMa follows the 2024 guideline. You can set your own **Revised Optimal target** for any nutrient, tracked beside the RDA.

Set them in **Settings → 5. Nutrient Targets - Researched**: pick a nutrient, enter the amount in its usual unit, save (blank and save to clear). Any nutrient works, including those without an official [DRI](#gloss-dri) (amino acids, [EPA](#gloss-epa)/DHA, [phytonutrients](#gloss-phytonutrients)). For amino acids, NuMa's [DIAAS](#diaas)-based protein scoring is the better measure; a flat gram target is only a simple tripwire.

**Loading recommended targets.** **Load recommended Revised Optimal targets** fills in a small set of commonly cited targets, for nutrients you haven't set yourself:

| Nutrient | Built-in Revised Optimal default | Source |
|---|---|---|
| Vitamin D | 23 mcg/day, **age 75 and older only** (no default under 75) | Endocrine Society 2024 guideline[^101]: the average daily dose in the trials behind its 75+ advice |
| Omega-3 EPA | 250 mg/day | [ADA](#gloss-ada)/Dietitians of Canada position paper[^13] (250 mg EPA + 250 mg DHA = ~500 mg combined) |
| Omega-3 [DHA](#gloss-dha) | 250 mg/day | Same source[^13] |

These are general guidance, not medical advice, and each can be changed. EPA/DHA has no official DRI ([why](#omega3)). **The vitamin D default (changed 14 October 2026):** under 75 there is none, so your target is the RDA; from 75 it's 23 mcg (about 900 [IU](#gloss-iu)), the average daily dose in the trials behind the 2024 guideline's advice, which names no best dose and prefers daily doses to occasional large ones[^101]. If you loaded targets before that date, your vitamin D target is still 50 mcg; change or clear it in Settings → 5. If pregnant or with high-risk prediabetes, ask your clinician.

Only these three have a default; magnesium, vitamin K2 and choline were considered and not added ([why](#expand-revised-optimal)).

With at least one set, every nutrient table adds Revised Optimal columns beside the RDA ones (goal, meal %, day %), with a dash for nutrients you haven't set, so it's clear which you've personalized.

They're set nutrient by nutrient. Each is a two-sided "target" ([colors](#color-coding)), like calories: green at 100–130%, blue at 70–99% or 131–150%, orange under 70%, red over 150%.


#### Maximum Nutrient Limits {: #maxlimits}

*Search terms: too much, toxicity, overdose.*

Three kinds of daily maximum:

- **Sodium's built-in limit**, part of the standard goals ([Daily Nutrient Goals](#goals)): 2,300 mg a day, the Chronic Disease Risk Reduction Intake. Not adjustable.
- **Built-in Tolerable Upper Intake Levels ([UL](#gloss-ul))** for twelve nutrients where chronic excess, usually from supplements, can harm, applied automatically by age and sex:

    | Nutrient | Adult UL | Age band |
    |---|---|---|
    | Calcium | 2500 mg (2000 mg at 51+) | Yes |
    | Phosphorus | 4000 mg (3000 mg at 70+) | Yes |
    | Iron | 45 mg | No |
    | Zinc | 40 mg | No |
    | Iodine | 1100 mcg | No |
    | Selenium | 400 mcg | No |
    | Vitamin A | 3000 mcg | No |
    | Vitamin C | 2000 mg | No |
    | Vitamin D | 100 mcg | No |
    | Vitamin E | 1000 mg | No |
    | Vitamin B6 | 100 mg | No |
    | Choline | 3500 mg | No |

    Source: [NIH](#gloss-nih) Office of Dietary Supplements / Institute of Medicine Dietary Reference Intake UL summary tables[^9]. Five other tracked nutrients (potassium, thiamin, riboflavin, vitamin B12, vitamin K) simply have no established UL — the [DRI](#gloss-dri) tables mark these "ND" (not determinable from available data), which is different from "no risk at any dose." Magnesium, niacin, and folate are deliberately left out even though the DRI table publishes ULs for them (350 mg, 35 mg, and 1000 mcg respectively): each of those figures applies only to *supplemental* or fortified-food forms, not to the nutrient as it naturally occurs in whole food — niacin's UL guards against a flushing reaction specific to synthetic nicotinic acid/nicotinamide, and folate's guards against synthetic folic acid, neither of which whole-food niacin or folate triggers. NuMa sums whole-food intake for all three, so applying their published ULs here would flag entirely ordinary diets as "over the limit" for a risk that doesn't actually apply to them. If you take a supplement containing any of the three, that supplemental amount is exactly what the real UL is meant to track — use a [custom max limit](#maxlimits) to watch it.
- **Your own max limits**, for any nutrient, stricter than the guideline or where there's none. Yours always take precedence. Set them in **Settings → 5. Nutrient Targets - Researched**.

**Where you see it.** Every nutrient table (and its printout) has a **UL** column, far right, with the limit that applies (yours, or the built-in one). Against a **day's total**, it turns amber with the row tinted at 90% of the limit, and red at 100% or more; a limit is a daily budget, so single meals aren't flagged. Without a day (a food's per-100 g view), it shows just the limit.

Limits and Revised Optimal targets are independent: set either, both or neither.


#### Diet-Aware Bioavailability and Deficiency Notes {: #diet-bioavailability}

*Search terms: vegan.*

Your [dietary preference](#diet) also adjusts your targets, because a vegetarian or plant-based diet changes how much of some nutrients you absorb.

**Iron and zinc targets are raised for vegetarian and plant-based settings.** Iron from plants (non-heme) is absorbed far less well than iron from meat and fish (heme), and phytate in legumes and grains blocks it further ([Antinutrients](#antinutrients)); phytate reduces zinc too. So NuMa raises the iron RDA 1.8 times[^4]<sup>,</sup>[^5] and zinc 1.5 times[^4]<sup>,</sup>[^6], following the Institute of Medicine and the [NIH](#gloss-nih) Office of Dietary Supplements, with a note beside the goal. "All animal foods" restores the standard values.

**A B12 warning, for Plant-based only, when intake is low.** B12 comes almost only from animal foods[^7], so a fully plant-based diet usually needs a supplement or fortified food[^7]. The warning appears when the day's B12 is under 50% of the RDA (NuMa's own trigger, not a diagnostic threshold; deficiency is diagnosed by blood test). Vegetarians aren't flagged, since dairy and eggs supply B12.

Both are general guidance; with a diagnosed deficiency or absorption problem, follow your clinician.

**The protein target is deliberately not raised.** Protein's quality penalty is already in [Digestible Complete Protein](#dcp), measured from your actual foods, including mixed diets, so raising the target would count it twice. Compare the [DCP](#gloss-dcp) row with your protein target; [The protein target assumes high-quality protein](#protein-rda-quality) explains why.

### D. Other nutrients and food factors {: #science-other}

*Search terms: omega-3, antinutrients, oxalate, water, hydration.*

Omega-3 fats, antinutrients, oxalate and water: four topics that matter to many people, each with its own data in NuMa.

#### Omega-3 Fatty Acids {: #omega3}

*Search terms: fish oil, algae oil.*

NuMa tracks four omega fatty acids: [ALA](#gloss-ala), EPA, and DHA (all omega-3), and linoleic acid (omega-6). Of the three omega-3s, only ALA has an official Adequate Intake, and it appears as a Daily Goal: 1600 mg/day for men, 1100 mg/day for women[^60].

**Why not a goal for [EPA](#gloss-epa) and DHA directly?** No U.S. Dietary Reference Intake exists for EPA or DHA intake on their own -- the official guidance covers only total ALA[^60]. This matters because ALA is not itself the fatty acid your body mostly uses; it has to be converted into EPA and then DHA, and that conversion is inefficient -- estimated at under 5-10% for EPA, and only 2-5% for DHA[^87]. Two people can hit the same ALA target and land in very different places on EPA/DHA status depending on the rest of their diet, genetics, and sex (conversion is more efficient in women, possibly because of an effect of estrogen[^88]).

**Why this matters especially for plant-based eaters.** Direct dietary EPA and [DHA](#gloss-dha) come almost entirely from fish, algae, and other seafood. If ALA (from flax, chia, walnuts, hemp, canola and soy oils) is your only omega-3 source, meeting the ALA goal is necessary but may not be sufficient -- your actual EPA/DHA status depends on that inefficient conversion step, which is why total omega-3 needs may be higher for vegetarians than for people who eat fish[^87]. Common ways to address this without animal fish: algae-oil supplements (a direct EPA/DHA source independent of the ALA conversion pathway), or simply logging ALA-rich foods generously since the target itself already assumes real-world conversion losses are ahead of it.

**Setting your own EPA+DHA target.** Because there's no official [DRI](#gloss-dri) to compute automatically, NuMa can't put a Daily Goal on the EPA or DHA rows the way it does for ALA. If you want to track against a target anyway -- clinical guidance in the 250-500 mg/day combined EPA+DHA range is common[^13] -- set one yourself as a [Revised Optimal target](#optimal) for the EPA and/or DHA rows in Settings → Nutrient targets.

Linoleic acid (omega-6) also has an official [AI](#gloss-ai), and it too appears as a Daily Goal: 17 g/day for men and 12 g/day for women aged 19-50, and 14 and 11 g/day from 51 on[^60]. Read it more loosely than most goals. That AI was set at the typical (median) U.S. intake rather than from a measured need, so about half of people fall a little short of it, and deficiency is essentially unknown in people eating ordinary diets[^60]. Falling short is worth a look only if you're well under it day after day.


#### Antinutrients {: #antinutrients}

*Search terms: phytates, oxalates, lectins, mineral absorption, anti-nutrients.*

[Antinutrients](#gloss-antinutrient) are in nearly every plant food, and matter especially on a plant-based diet: the foods richest in fiber, minerals and [phytonutrients](#gloss-phytonutrients) often carry the most.

##### What is an antinutrient?

*Search terms: definition, what antinutrients are, absorption blockers.*

A natural compound in a food that partly blocks absorption or use of a nutrient. It's a matter of degree, and preparation can usually reduce or remove it.

They are not contaminants or the result of farming practices; they are part of the plant's own biology. Some are defenses against insects and animals that would eat the plant, such as lectins and trypsin inhibitors[^107]. Others have different jobs: phytate is the main way seeds store phosphorus[^102].

##### The main antinutrients that appear in NutriMagnus output

*Search terms: trypsin inhibitor, tannin, goitrogen, oxalic acid.*

**Phytates** (phytic acid). Found in legumes, whole grains, nuts, and seeds. Phytate binds tightly to minerals — especially iron, zinc, calcium, and magnesium — forming a complex the body cannot easily absorb[^102]. A meal of lentils or whole-wheat bread may contain all the iron the label shows, but much of it may pass through unabsorbed if phytate is high. The effect depends on the rest of the meal: vitamin C eaten at the same meal counteracts phytate's effect on iron, and more vitamin C counteracts more of it[^103]. Preparation methods that reduce phytate: soaking legumes or grains overnight before cooking; sprouting; fermentation[^102]. In one study, sourdough fermentation cut the phytate in whole wheat bread by about 62%, against about 38% for ordinary yeast bread, and by about 90% when the bran was fermented first[^104]. Tempeh and other fermented soy products are low in phytate.

**[Oxalates](#gloss-oxalate)**. Found at high levels in spinach, Swiss chard, beet greens, rhubarb, and almonds; at moderate levels in many other plant foods. [Oxalates](#gloss-oxalate) bind calcium in the gut, meaning the calcium shown on a food label for spinach is largely unavailable — in a direct comparison, people absorbed about 5% of the calcium in spinach against about 28% of the calcium in milk[^105]. For most people this is simply a reason not to rely on spinach as a calcium source, not a reason to avoid it. For people prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly. See [oxalate data](#oxalate) for the detailed data NuMa tracks on this.

**Lectins** and **trypsin inhibitors**. Found in raw legumes (beans, lentils, chickpeas, soybeans). Lectins interfere with the gut lining; trypsin inhibitors block a key digestive enzyme. Raw kidney beans contain enough lectin to cause acute food poisoning: as few as four or five raw beans can cause symptoms. The US Food and Drug Administration advises soaking dried beans for at least 5 hours, pouring the water away, and boiling them in fresh water for at least 30 minutes, and warns that slow cookers don't get hot enough to destroy the lectin[^106]. Trypsin inhibitors are more resistant to heat; ordinary cooking removes most of their activity, though not necessarily all[^107]. Canned beans are already cooked. Tofu and tempeh are also safe because both involve prolonged heat treatment or fermentation. This is the one [antinutrient](#gloss-antinutrient) on this list that is not just about partial reduction — with raw legumes, proper cooking is required.

**Bound niacin** (in corn). Untreated corn contains niacin in a chemically bound form the human body cannot absorb. Populations who ate corn as a dietary staple without treatment historically developed pellagra (severe niacin deficiency), and outbreaks still occur where untreated maize is the staple food[^108]. The traditional solution — practiced for thousands of years by Mesoamerican cultures and still used today — is nixtamalization: soaking dried corn in an alkaline lime solution. This releases the bound niacin so the body can use it[^108]. Tortillas, masa, hominy, and grits made from nixtamalized corn are fine. Plain cornmeal (not nixtamalized) retains the problem.

##### How these appear in NutriMagnus output

A food with known concerns gets a note in its **Anti-nutrients** section (and in any meal, recipe or day including it), naming the compound, the problem, and the preparation that reduces it.

##### Examples of what you may see

*Search terms: cook beans, preparation methods.*

    Mineral absorption problem — phytates are present
    Best reduction: soak or sprout before cooking

    Mineral absorption problem — high oxalate reduces calcium uptake from this food specifically

    Mineral absorption problem — oxalate & phytate present
    Reduces both: roasting or soaking

    Food safety: cook dried beans fully — raw or dried, they carry lectins and trypsin inhibitors
    Required: soak at least 5 hours, pour the water away, and boil in fresh water for at least
    30 minutes — red kidney beans most of all; a slow cooker doesn't get hot enough

    Vitamin bioavailability problem — niacin is bound, not usable unless nixtamalized
    Nixtamalized forms are fine: tortilla, masa, hominy

Notes appear only for foods NuMa has flagged, so no note doesn't mean no antinutrients. NuMa matches whole words in the name (beans, lentils, oats, cornmeal…), skipping look-alikes (jelly beans, coffee beans, nutmeg, cornstarch, sweet corn). The dried-bean note is left off cooked or canned beans.

**Dried beans in a slow cooker.**{: #slow-cooker-beans} When a recipe uses dried beans and its instructions mention a slow cooker or Crock-Pot, the recipe page and printout show a red **food safety** warning: a slow cooker doesn't get hot enough to destroy the lectin. Boil the beans first, or use canned. NuMa only sees the words, so the warning appears even if your instructions already boil them first.

##### What these notes do not mean

*Search terms: should I avoid, safe to eat, healthy foods, reassurance.*

They're not a reason to avoid these foods. Legumes, whole grains, nuts and leafy greens are among the most nutritious there are, and still supply plenty after antinutrient losses. The notes are there for preparation choices, and so you don't assume every labeled nutrient is fully absorbed.

In practice: soak legumes, prefer sourdough or sprouted grains, cook beans fully, pair iron-rich plant foods with vitamin C, and don't rely on spinach for calcium.


#### Oxalate Data {: #oxalate}

*Search terms: low-oxalate diet, Harvard oxalate table.*

[Oxalates](#gloss-oxalate) are one of the [antinutrients](#antinutrients); this section covers the data NuMa keeps on them.

[Oxalates](#gloss-oxalate) (oxalic acid) bind calcium in the gut, reducing its absorption from high-[oxalate](#gloss-oxalate) foods. They are found at very high levels in spinach, Swiss chard, beet greens, and rhubarb, and at notable levels in almonds and some other nuts. For most people the main consequence is that these foods are poor calcium sources despite their labels. For anyone prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly.

NuMa includes the Harvard T.H. Chan School of Public Health [oxalate](#gloss-oxalate) table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine, whose laboratory measured many of its values[^11]. This data is optional and disabled by default.

**To enable it:** Settings → Your Profile → check "Look up oxalate content for foods," then Save profile.

Then viewing a food or recipe looks it up in the table by name and links the best match automatically, once per food.

##### Correcting a wrong match {: #oxalate-link-correction}

*Search terms: wrong oxalate match, fix oxalate match, correct oxalate.*

Name matching is sometimes wrong, so an unconfirmed match is marked "auto-matched — correct if wrong". Click it to search the same table, pick the right entry and save, or choose "This food is not in the oxalate reference table". Either way the food is marked confirmed, and the warning goes.

##### How to read a reference entry {: #oxalate-row}

*Search terms: oxalate table row, reading oxalate entry, oxalate serving.*

Each candidate on that page is one row of the Harvard table, printed like this:

```
Spinach, Raw — 316.2 mg  / 1 cup  [very high]
Vegetables · measured in this food
```

* **316.2 mg / 1 cup** — the [oxalate](#gloss-oxalate) content of the serving *the table chose*, which is rarely 100 g. When that serving is a weight (usually ounces), the row also carries **= x mg/100g**, and NuMa can then scale the figure to whatever amount you actually eat. When it's a cup, a piece or a tablespoon, there is no per-100 g figure and none can be derived without knowing the food's density — such a row is flagged on the page as "per-serving only", and NuMa leaves that food out of recipe [oxalate](#gloss-oxalate) totals rather than guessing.

* **[very high]** — the band NuMa uses to color the value. Thresholds are in the next section.

* **Vegetables** — the table's own food group (23 of them, from *Cold Cereal* to *Soups And Chowder*). It earns its place when two rows start the same way: "Bacon, Broiled, Pan-Fried, Or Roasted" sits under *Meat*, while "Bacon, Turkey, Microwaved" is under *Poultry*.

* **measured in this food** — whether this value was measured directly or estimated. See [Measured or estimated](#oxalate-measured).

Pick the row that best matches what you eat: same preparation (raw or boiled matters a lot), same form. A near name with the wrong preparation is worse than a different name with the right one.

##### What the categories mean {: #oxalate-categories}

*Search terms: oxalate bands, low oxalate, oxalate levels.*

NuMa puts every value in one of five bands, colored on the food's page. The cut-offs are NuMa's own (the table gives values only). With a per-100 g figure, the band comes from that:

| Category | Per 100 g |
|---|---|
| Very high | 300 mg or more |
| High | 100–299 mg |
| Moderate | 25–99 mg |
| Low | 5–24 mg |
| Negligible | under 5 mg |

Per-serving-only rows use lower cut-offs on that figure (100 mg or more very high, then 26, 10 and 2 mg); the two scales don't compare directly.

For scale: people with calcium-oxalate kidney stones are often advised to stay under 40–50 mg a day[^109] (some use 100 mg; follow your clinician), so one "very high" serving can exceed a day's allowance. For everyone else, read the bands as a guide to poor calcium sources, not a budget.

##### Measured or estimated {: #oxalate-measured}

The table marks values **measured directly** in the food (235 of 433); the rest were **estimated** from a similar food. NuMa shows which, on the match page and the food's page.

An estimate is still a reasoned value, but less certain; between two equally good rows, prefer the measured one.

##### What NuMa saves from a match {: #oxalate-what-is-stored}

*Search terms: confirmed match, oxalate choice saved.*

Saving a match records your choice, marked confirmed: the warning stops and NuMa never re-matches that food.

"This food is not in the oxalate reference table" is saved the same way, and the food then has no oxalate figure, better than a wrong one in every total.

These choices are yours, in your own [database](#gloss-database); the bundled table itself never changes.

##### Important limitations

*Search terms: oxalate limitations, accuracy.*

- Values are per serving. Weighed servings (ounces) are converted to per 100 g; cups, pieces and tablespoons can't be without the food's density, so such foods are left out of totals and noted.

- Oxalate varies with preparation (cooking reduces it in spinach) and growing conditions; treat all values as estimates.

- Name matching is approximate, especially for processed or branded foods; check a match makes culinary sense.

The table's source, the Harvard T.H. Chan School of Public Health, is named under every oxalate table NuMa shows.


#### Water: from drinks and from food {: #water}

*Search terms: fluids, hydration, beverages, dough, batter, grams of water, how much to drink.*

NuMa counts the water in everything you log, not just drinks: an apple is about 86% water, and milk, soup and cooked grains are mostly water too, so food supplies a real share. (To stop tracking water, turn it off in Settings → 9; nothing is deleted.)

**Where you see it.** Meal, recipe and day pages show **Water**, split into **Water from drinks** and **Water from food**. Items in meals, recipes and day lists show their water in gray beside the name: "(72% water, 98 g)" (a recipe's after cooking, if set). Both rows can also be Meals & Log and Recent Days columns, and plotted. Amounts are in grams; for water, 1 g is 1 mL.

**What counts as a drink.** You decide, with **This food is a drink** on a food's page, or **This recipe is a drink** on a recipe's (both also appear on search results, the Recipes list and Food use in meals). NuMa ticks it itself for a [USDA](#gloss-usda) food filed under beverages (tea, coffee, juice, soft drinks, water), but not for milk, soup or smoothies; tick those if you drink them. Changing it updates every meal and recipe using the food. Most branded drinks have no water value (US labels don't list it), so ticking the box estimates one, 100 g minus protein, carbs and fat, marked as an estimate; a measured value is never replaced.

**Inside a recipe, only the recipe decides.**{: #water-in-recipes} A recipe's water all counts as water from food, even from drink ingredients (the tap water in bread dough, the milk in pancake batter), since once mixed or baked in, it isn't something you drank; a blue note on the recipe names such ingredients. If you do drink the recipe (a smoothie, a broth), tick **This recipe is a drink** and all its water counts as drinks, including when it's used inside another recipe. (Before 9 November 2026 drink ingredients counted as drinks; affected meals were recalculated once, and say so.) For cooked dishes, see [water after cooking](#cooked-water).

**The daily goal.**{: #water-reference} The goal is the 2004 [Adequate Intake](#gloss-ai), from the US Institute of Medicine (IOM), for *total* water, drinks and food together: 3.7 liters a day for men, 2.7 for women. It's a guide, not a requirement: these are typical intakes of healthy Americans, not a measured need, and the IOM says less may carry no added risk. The European Food Safety Authority (EFSA) sets 2.5 and 2.0 liters[^84]. Choose under **Water goals from** in Settings → 1 (the IOM's by default); today follows the change at once, earlier days only if you [apply your profile to them](#day-profile). Needs rise with heat, exercise, body size and illness.

Going past a water goal gains nothing, so the percentage is colored below the goal but plain, not green, at or above it.

**A fluid limit from your clinician** (for heart failure or kidney disease) goes in as a [maximum limit](#maxlimits) in Settings → Nutrient Targets: on **Water from drinks** if it counts what you drink, as heart-failure limits usually do, or on **Water** if it counts everything. NuMa then stops nudging you to drink more: water goals lose their color, and the older-people warning and the notes below go.

**A weight-based figure, for comparison.**{: #water-weight} Neither the IOM nor EFSA scales by body weight. The common weight-based figure comes from NICE (National Institute for Health and Care Excellence, UK), for adults in hospital on a drip: 25–30 mL per kg a day, up to about 3 liters, using ideal body weight for people with obesity[^85]. A day's page shows yours under the Water rows, using your weight, or with a body mass index (BMI) of 30 or more an ideal weight from your height (the Devine formula). It's for patients lying in bed, not a goal for healthy people, and per-kilogram rules mislead at both ends: a body 50 kg heavier needs only about 0.7 liters more. At 60 kg it gives 1.5–1.8 liters, below both goals, and the note says so; your goal stays the one you chose.

**A goal for drinks, too:** the drinks part of the IOM figures, 3.0 liters for men and 2.2 for women (the rest comes from food)[^77], or with EFSA's figures 2.0 and 1.6 (80%)[^84]. From age 65, a day's page also warns when drinks fall below the minimum for older people, a floor, not a lower goal ([Water and older people](#water-older)).

**What counts as water.** Coffee, tea, beer and other dilute alcoholic drinks hydrate about as well as water (their diuretic effect is brief), and the IOM counts them. Milk and juice are 85–90% water and count in full. Food's share is shown beside **Water from food** ("23% of the total"): about a fifth on a typical diet, more with plenty of fruit, vegetables and soup.

**Protein and water.** Breaking down protein makes urea, which the kidneys clear in urine, so a high-protein diet needs more water. NuMa doesn't change the goal, but a day's page notes it when protein reaches 1.5 times your goal or more (a judgment, not a research figure). How much it adds: [Water and older people](#water-older).

**Gaps in the data.**{: #water-gaps} NuMa began recording water in October 2026, so foods saved earlier show "no data", making water totals too low. To fill them in:

- **All your USDA foods at once:** on Foods → 9, *Missing nutrient data*, click **Fill in water for N USDA foods from USDA**. It fetches only water, fills only blanks, and takes well under a minute for a few hundred foods; if it stops, click again to carry on. Foods USDA has no water for (usual for branded foods) are named; **Show these foods in the list below** turns on the Water column there, with **ask AI** and **not needed** boxes.
- **One food:** **Find this data** beside it under [Top Contributors](#top-contributors) (ranked by Water), or **Fill in nutrients from another food** on its page ([which source first](#key-sources)).
- **Any other food:** tick the **Water** group and ask Claude AI ([Checking your data](#checking-your-data)).

USDA, the Canadian Nutrient File and the UK, Australian and French databases report water (the French for most foods); most Open Food Facts products don't.

##### A wet food picked for a dry one {: #water-wet-dry}

*Search terms: wrong food record, dry vs wet, water percentage.*

Water also reveals the wrong record. The same food comes wet or dry, and the name may not say which: [USDA](#gloss-usda)'s okara is the wet pulp from soy milk, about 82% water, while okara *flour* is about 8% water with five times the protein and calories. Pick the wet one for a flour recipe and every value is several times too low.

So when a food's name (or the name you gave it) says dry (*flour*, *powder*, *dried*, *dehydrated*, *dry*) but its data is over 40% water, NuMa marks it with a yellow **"82% water — but named flour?"**, explains below the list, and lists it on Foods → 9 under **Named dry, but mostly water**. Dried fruit stays under the line (prunes are about 31% water), and "prepared with milk", "packed in oil" or "dry white wine" don't count. A food without a water value can't be checked.

##### Cooked dishes: water after cooking {: #cooked-water}

*Search terms: baking, baked, bread, moisture loss, evaporation, boiled down, reduced, simmered, yield.*

A recipe's water starts as its raw ingredients' water: the 4 cups in bread dough plus the little in the flour. Baking, simmering and roasting drive some off, so servings would count too much.

**Water after cooking**, on a recipe's page, takes the water the finished dish really holds, in g per 100 g: a number, or the code of a food to copy it from (a commercial version of the dish, say). That figure then replaces the ingredients' water everywhere the recipe counts, each serving getting its share. Cooking loses water, not protein or minerals, so nothing else changes. **Clear** goes back.

It needs the recipe's **total weight** (the cooked batch, on its Edit page); without one, the box says it isn't in use yet.

**No commercial version?** If you weighed the cooked batch, the box estimates it, assuming all weight lost was water (it nearly always is): 2,328 g of ingredients holding 1,062 g of water that bake to 2,094 g lost 234 g, leaving 828 g, 39.6 g per 100 g. **use this** saves it. It needs every ingredient's weight, and a batch lighter than its ingredients.

It counts as water from food, unless the recipe is marked as a drink.

##### Water and older people {: #water-older}

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

Older people don't need less water than younger adults, and need to take more care to get it. NuMa keeps the same Institute of Medicine (IOM) goals at every adult age, for three reasons:

- **Less water from food.** Older people eat less, so get less of the fifth or so of daily water food supplies[^77]; more must come from drinks.
- **Kidneys that save less water.** Ageing kidneys concentrate urine less, so the same waste takes more water. In healthy men without water for 12 hours, the oldest group's most concentrated urine was about a fifth weaker than the youngest's[^80], and dehydration becomes more common with age[^82].
- **More protein, more urea.** From 65, at least 1.0–1.2 g of protein per kg a day is advised, against 0.8 g for younger adults ([PROT-AGE](#gloss-prot-age)[^67]). Each gram leaves about 5.7 milliosmoles of urea to clear (its nitrogen, about 16% of its weight, ÷ 28)[^83]. Going from 60 to 100 g a day adds about 230 milliosmoles: at an older kidney's concentration, at least a quarter liter more urine a day.

And **thirst fades with age**: healthy men aged 67 to 75, kept without water for 24 hours, felt less thirsty and drank less afterward than young men[^81]. About one older adult in four living at home is mildly dehydrated[^79].

Hence a floor: ESPEN (the European Society for Clinical Nutrition and Metabolism) recommends offering older people **at least 1.6 liters of drinks a day for women and 2.0 for men**, unless a condition calls for otherwise[^78]. It's a minimum for the many who drink far too little, not a measure of need, so NuMa uses it as a warning from age 65, not as the goal. If a clinician gave you a fluid limit, follow it, and set it as a [maximum limit](#maxlimits).


### E. Food reference {: #science-food-reference}

*Search terms: food list, nutrient list, protein foods, plant proteins.*

Two reference lists: common plant protein sources, with notes on each, and every nutrient NuMa tracks, with where its data comes from.

#### Plant protein sources in your pantry {: #appendix-plant-proteins}

*Search terms: plant proteins, vegan protein, vegetarian protein.*

("pantry" here has two meanings: your actual pantry, and the pantry [database](#gloss-database) that is in NuMa (see the Foods dropdown menu), which is a list of foods in your actual pantry.)

This appendix profiles the plant protein sources currently kept in a typical [NuMa](#gloss-numa) pantry, including nutritional yeast, which is not a plant but is grouped here because it fills the same dietary role. For each source: what form it takes, where it comes from, its essential amino acid ([EAA](#gloss-eaa)) strengths and weaknesses relative to the [FAO](#gloss-fao) reference values described in [Raw protein, protein quality, and protein digestibility](#appendix-protein-quality), and its typical role in cooking.

The [EAA](#gloss-eaa) notes below describe general tendencies for each food, not a substitute for running the food itself through [NuMa](#gloss-numa). Growing conditions, processing, and the specific [USDA](#gloss-usda) or Open Food Facts[^3] record behind a given entry all shift the exact numbers — use [NuMa](#gloss-numa)'s own amino acid ratio and [DIAAS](#gloss-diaas) output for precise figures. Sourcing and cost information for these foods is addressed separately, not here.

*The figures quoted below (checked 14 October 2026) are each food's [USDA](#gloss-usda) record[^2], scored by NuMa against the [FAO](#gloss-fao) 2013 reference values[^16], before digestibility: 1.00 means exactly the reference amount. Where a claim isn't one NuMa can compute (storage, cooking, food safety), it's general food knowledge.*

BEFORE GOING ANY FURTHER: You should know that the two most useful foods below (aside from staples like whole wheat flour) are nutritional yeast and hulled hemp seed. Both are incredibly nutritious and useful. Nutritional yeast adds umami to any food, and hulled hemp seed is invaluable when eating legumes.

##### Seeds

**Chia seeds**

- *Form:* tiny oval seeds, black or mottled gray-brown, about 1mm long.
- *Source:* *Salvia hispanica*, a flowering mint-family plant native to Mexico and Guatemala.
- *[EAA](#gloss-eaa) profile:* unusually complete for a plant seed — as worked through in the [protein-quality primer](#appendix-protein-quality), chia clears all nine [EAA](#gloss-eaa) floors, with lysine as its narrowest margin (1.22× the reference). One of the few standalone-complete plant proteins in this pantry.
- *Culinary role:* primarily a functional/textural addition rather than a bulk protein source — a gelling agent for puddings, an egg replacer in baking (roughly 1 Tbsp ground chia + 3 Tbsp water per egg), and a smoothie thickener.
- *Also worth knowing:* usually eaten soaked until gelled, or ground.

**Ground flax seeds**

- *Form:* fine golden-brown to reddish-brown meal (pre-milled — whole flaxseed is a hard, shiny, oval seed instead).
- *Source:* *Linum usitatissimum*.
- *[EAA](#gloss-eaa) profile:* good, though a step below chia: it falls just short of complete — lysine 0.98 in [USDA](#gloss-usda)'s flaxseed record, methionine + cysteine 0.97 in its ground-flaxseed record. A useful contributor, especially alongside grains.
- *Culinary role:* the same functional role as chia — egg replacer, binder, and fiber/omega-3 booster in baked goods and oatmeal; a meaningful protein contributor only at larger doses.
- *Also worth knowing:* ground flax oxidizes faster than whole flaxseed — keep it refrigerated or frozen, and use it within a few months of grinding.

**Hulled hemp seeds**

- *Form:* small, soft, pale green-to-tan kernels (already shelled).
- *Source:* *Cannabis sativa* (non-psychoactive hemp variety).
- *[EAA](#gloss-eaa) profile:* a protein-dense seed (about 32 g per 100 g) — good in the sulfur amino acids (methionine + cysteine), a category where legumes are typically weak, with lysine as its [limiting amino acid](#gloss-limiting-amino-acid) (0.84).
- *Culinary role:* a standalone protein/texture addition to smoothies, granola, salads, and oatmeal; its nutty flavor and sulfur-amino-acid strength make it a good complement to legume-heavy meals.
- *Also worth knowing:* eaten raw with no preparation needed — it digests readily as sold.

**Sunflower seed kernels**

- *Form:* small, flattish oval kernels, off-white to pale gray with a green tinge.
- *Source:* *Helianthus annuus*.
- *[EAA](#gloss-eaa) profile:* moderate protein source; methionine is relatively strong while lysine is the [limiting amino acid](#gloss-limiting-amino-acid) (0.94) — roughly the mirror image of many legumes, which makes it a reasonable legume complement.
- *Culinary role:* snack, salad topping, and seed butter; a minor protein contributor at typical serving sizes.
- *Also worth knowing:* high fat content gives raw kernels a short shelf life — refrigerate or freeze to prevent rancidity.

##### Grains & Pseudocereals

**Buckwheat, whole grain**

- *Form:* small, hard, three-cornered (pyramid-shaped) brown-green groats.
- *Source:* *Fagopyrum esculentum* — a pseudocereal, not a true grass/cereal despite the name; botanically closer to rhubarb and sorrel.
- *[EAA](#gloss-eaa) profile:* unusually well-balanced for a grain-like food — notably better in lysine than true cereals (wheat, corn, rice), the classic cereal weak point; its narrowest margins are leucine (1.03) and lysine (1.06), and it clears every floor.
- *Culinary role:* a base ingredient (groats, kasha, buckwheat flour, soba noodles) rather than an addition; naturally gluten-free, which makes it a useful wheat substitute in a plant-based, protein-conscious diet.
- *Also worth knowing:* the hull surrounding the raw groat is inedible and is always removed before sale.

**Oats, whole grain, rolled**

- *Form:* flattened, cream-colored flakes (steamed and rolled whole groats).
- *Source:* *Avena sativa*.
- *[EAA](#gloss-eaa) profile:* among the stronger true cereals for protein quality — higher lysine than wheat or corn; lysine is still its narrowest margin, right at the floor (1.01). A solid moderate-quality grain protein overall.
- *Culinary role:* a base ingredient — porridge, baked goods, granola — that can carry a meaningful share of daily protein at typical serving sizes, unlike most seeds or nuts used as garnish.
- *Also worth knowing:* often processed in facilities shared with wheat — check labeling if strict gluten-free status matters.

**Cornmeal, whole-grain, yellow**

- *Form:* coarse-to-medium granular yellow meal (ground dried corn kernels, germ and bran retained).
- *Source:* *Zea mays*.
- *[EAA](#gloss-eaa) profile:* the classic maize deficiency pattern — lysine well short (0.58), and tryptophan only just above the floor (1.06); one of the more amino-acid-limited grains in this pantry, and a strong candidate for legume pairing (the traditional corn-and-beans combination).
- *Culinary role:* a base ingredient — cornbread, polenta, breading — rather than a minor addition.
- *Also worth knowing:* whole-grain (not degermed) cornmeal is more nutrient-dense but has a shorter shelf life than degermed cornmeal, due to the retained germ oil.

**Whole wheat flour, unenriched**

- *Form:* fine tan-brown powder (whole grain milled, bran and germ retained).
- *Source:* *Triticum aestivum*.
- *[EAA](#gloss-eaa) profile:* lysine is severely limiting (0.57) — wheat protein (gluten) is notably poor in lysine; with cornmeal's, the sharpest deficiency among the grains in this pantry. Every other amino acid clears its floor.
- *Culinary role:* a base ingredient for baked goods, and a major contributor to daily protein for anyone eating bread-based meals regularly — its lysine gap matters more in practice than seeds used only as garnish.
- *Also worth knowing:* "unenriched" means it lacks the iron/B-vitamin fortification added to most commercial white flour — a micronutrient note, not an amino acid one.

##### Tree Nuts & Peanuts

**Almond flour**

- *Form:* fine off-white powder (blanched almonds, ground).
- *Source:* *Prunus dulcis*.
- *[EAA](#gloss-eaa) profile:* the most protein-dense nut here (about 21 g per 100 g, almonds' own figure), but short in two amino acids: lysine (0.56) and methionine + cysteine (0.76).
- *Culinary role:* a base flour substitute in gluten-free/low-carb baking rather than a protein-boosting addition — its protein contribution is secondary to its role as a wheat-flour replacement.
- *Also worth knowing:* high fat content means a shorter shelf life than wheat flour — refrigerate or freeze.

**Cashew nuts**

- *Form:* kidney-shaped, ivory-white nuts.
- *Source:* *Anacardium occidentale* (the seed attached to the cashew apple).
- *[EAA](#gloss-eaa) profile:* the one complete tree nut here — favorable lysine for a nut, and its narrowest margin (1.06).
- *Culinary role:* snack, cashew cream/cheese base, stir-fry addition; a significant contributor when used as a cream or sauce base in quantity, minor as a garnish.
- *Also worth knowing:* raw cashews are commonly soaked before blending into cream or cheese to soften texture — this is purely textural, not required for digestibility.

**Pecans**

- *Form:* smooth, elongated, ridged, brown-shelled halves.
- *Source:* *Carya illinoinensis*.
- *[EAA](#gloss-eaa) profile:* low overall protein density (about 9 g per 100 g); lysine is well short (0.65) — pecans are more valuable here for fat and mineral content than as a protein source.
- *Culinary role:* garnish or mix-in (baked goods, salads); a minor protein contributor at typical serving sizes.
- *Also worth knowing:* high polyunsaturated fat content makes pecans prone to rancidity — store refrigerated or frozen.

**Walnuts, English**

- *Form:* wrinkled, brain-like lobed, brown-shelled halves.
- *Source:* *Juglans regia*.
- *[EAA](#gloss-eaa) profile:* a similar pattern to pecans — lysine limiting (0.58) — notable mainly for omega-3 ([ALA](#gloss-ala)) content rather than protein quality.
- *Culinary role:* garnish or mix-in; a minor protein contributor.
- *Also worth knowing:* also prone to rancidity — refrigerate or freeze for storage.

**Brazil nuts**

- *Form:* large, dense, hard, off-white kernels with a rough triangular cross-section.
- *Source:* *Bertholletia excelsa*, native to the Amazon rainforest.
- *[EAA](#gloss-eaa) profile:* the exception among tree nuts — unusually rich in the sulfur amino acids (methionine and cysteine), the opposite weakness pattern from most nuts; lysine remains their [limiting amino acid](#gloss-limiting-amino-acid) (0.71).
- *Culinary role:* snack, or a minor addition to trail mixes and baked goods — valuable precisely because it complements legume-heavy meals that tend to be sulfur-amino-acid-poor.
- *Also worth knowing:* extraordinarily rich in selenium — about 1,900 mcg per 100 g in [USDA](#gloss-usda)'s record, so a single 5 g nut holds nearly twice the 55 mcg daily [RDA](#gloss-rda), and four or five reach the 400 mcg upper limit NuMa uses[^9]. In one trial, two Brazil nuts a day raised selenium levels as well as a 100 mcg supplement[^111]. The amount varies a great deal with where the nuts grew. Eating many daily risks selenium toxicity, a separate issue from protein content worth tracking alongside it.

**Peanuts**

- *Form:* oblong, tan-shelled kernels (botanically a legume, not a true nut).
- *Source:* *Arachis hypogaea*.
- *[EAA](#gloss-eaa) profile:* despite being a legume, lysine is its [limiting amino acid](#gloss-limiting-amino-acid) (0.75), with valine and leucine only just above their floors; methionine + cysteine, the usual legume weak point, are not short.
- *Culinary role:* snack, peanut butter, sauces; a substantial protein contributor at typical serving sizes, comparable to some legumes.
- *Also worth knowing:* raw peanuts are susceptible to aflatoxin-producing mold in storage — buy from a source with good turnover and store cool and dry. This is a food-safety note, not an amino acid one.

##### Soy-Based Foods

**Tofu, firm**

- *Form:* a solid, off-white curd block, custard-to-firm texture depending on how it was pressed.
- *Source:* coagulated soy milk (*Glycine max*), pressed to remove whey.
- *[EAA](#gloss-eaa) profile:* soy protein clears nearly every [EAA](#gloss-eaa) floor, with methionine + cysteine its [limiting amino acids](#gloss-limiting-amino-acid). How short they fall depends on the record: [USDA](#gloss-usda)'s firm tofu puts them well short (0.67), mainly because it lists very little cysteine, while soy protein isolate clears the floor (1.07). Check your own tofu's figures in NuMa.
- *Culinary role:* a primary protein ingredient — it stands in for meat or eggs across a wide range of dishes rather than functioning as a minor addition.
- *Also worth knowing:* pressing firmness determines water content and therefore protein density per gram — firm and extra-firm tofu concentrate protein relative to soft or silken tofu.

**Pure okara flour**

- *Form:* a fine, pale tan powder — dried and milled okara, the fibrous pulp left over from making soy milk and tofu.
- *Source:* a byproduct of soy milk production, from *Glycine max*.
- *[EAA](#gloss-eaa) profile:* a similar amino acid pattern to whole soy (methionine/cysteine mildly limiting), but the retained fiber and cell-wall material reduce digestibility relative to tofu or soy protein isolate — expect a lower [DIAAS](#gloss-diaas) despite a similar raw amino acid pattern.
- *Culinary role:* a flour substitute or booster in baked goods, veggie burgers, and pancakes — a byproduct-recycling ingredient rather than a dedicated protein powder.
- *Also worth knowing:* the reduced digestibility, not reduced amino acid content, is the thing to watch — check [NuMa](#gloss-numa)'s digestibility-adjusted ([DIAAS](#gloss-diaas)) figures rather than raw [AA](#gloss-aa) ratios for this one.

**Soy protein isolate**

- *Form:* a fine, white-to-off-white powder with minimal flavor.
- *Source:* soy protein extracted and concentrated to 90%+ protein by weight, with fiber, carbohydrate, and fat removed.
- *[EAA](#gloss-eaa) profile:* one of the highest-quality plant proteins available, with high digestibility (~0.95, as noted under "[SPI](#gloss-spi)" in the Glossary) — it clears every [EAA](#gloss-eaa) floor, with methionine + cysteine still its narrowest margin (1.07).
- *Culinary role:* a concentrated protein-boosting addition — smoothies, baked goods, meat analogs — rarely eaten as a standalone dish, but very effective at raising a meal's complete-protein grams without much bulk or flavor change.
- *Also worth knowing:* as a concentrate rather than a whole food, it also strips out the fiber, [phytonutrients](#gloss-phytonutrients), and micronutrients present in whole soy — best treated as a protein-density tool, not a whole-food replacement for tofu or edamame.

##### Other Protein Concentrates

**Unsweetened pea protein powder**

- *Form:* a fine, off-white to pale yellow powder.
- *Source:* yellow split peas (*Pisum sativum*), protein-extracted and concentrated.
- *[EAA](#gloss-eaa) profile:* notably good lysine content — peas are a classic lysine-rich legume — but methionine + cysteine are limiting (0.88 in [USDA](#gloss-usda)'s split peas; a protein powder's own label or record may differ), the reason pea protein is so often blended commercially with rice protein, which has the opposite pattern.
- *Culinary role:* a concentrated protein-boosting addition, the same role as soy protein isolate — smoothies, baking, general protein boosting — and it is a particularly effective complement to a grain-based meal (cereal, rice, wheat) that is itself lysine-poor but has adequate sulfur amino acids.
- *Also worth knowing:* the single best complement in this pantry for grain-heavy meals (bread, oats, cornbread), specifically because its strength (lysine) matches their specific weakness.

**Vital wheat gluten**

- *Form:* a fine, tan powder — nearly pure wheat protein with the starch washed out.
- *Source:* wheat flour (*Triticum aestivum*), processed to isolate the gluten protein fraction.
- *[EAA](#gloss-eaa) profile:* the most lysine-poor protein in this pantry — gluten is very low in lysine, and concentrating the protein by removing the starch does not fix this; it simply delivers more of the same imbalanced amino acid pattern per gram. (USDA's vital wheat gluten record has no amino acid figures, so NuMa can't score it unless you add them.)
- *Culinary role:* as much a structural/textural ingredient (seitan base, bread dough strengthener) as a protein source — it is often eaten as a primary "meat analog" ingredient (seitan) despite its poor amino acid balance, so it especially needs deliberate complementing with a lysine-rich food (legumes, pea protein) in the same meal or day.
- *Also worth knowing:* because seitan dishes are sometimes treated as a standalone "meat" replacement, this is the food in the pantry most likely to create an unnoticed lysine gap if eaten alone in quantity.

##### Nutritional Yeast

**Nutritional yeast flakes**

- *Form:* yellow flakes of deactivated, dried yeast. Flakes are less dense than powder, so measure by weight rather than volume when precision matters — a point already flagged in this pantry's notes for this item.
- *Source:* *Saccharomyces cerevisiae*, grown on a sugar-based medium, then deactivated (killed) and dried. Deactivation means it will not leaven anything or grow in the gut, unlike active baker's or brewer's yeast.
- *[EAA](#gloss-eaa) profile:* a good-quality protein for a non-legume source, though not quite complete: in NuMa's built-in profile, methionine + cysteine (0.92) and phenylalanine + tyrosine (0.94) fall just short — the sulfur amino acids being its weak point, as for soy and legumes generally.
- *Culinary role:* usually an addition rather than a primary ingredient — its concentrated umami (glutamate-driven) flavor makes it a savory, cheese-like flavoring for popcorn, pasta, sauces, and roasted vegetables, and it thickens liquids when whisked into a roux-based sauce (as in "nooch" cheese sauce). It can also become a primary ingredient in dishes built around it, such as cashew-and-nutritional-yeast "yeast cheese," where it supplies both flavor and a meaningful protein contribution.
- *Also worth knowing:* most commercial brands are fortified with B12 (and sometimes other B vitamins) — worth checking the label, since this is often the primary reason vegans include it in their diet, independent of its protein content.

#### Full Nutrient Key {: #nutrient-key}

*Search terms: nutrient definitions, what each nutrient does, internal names, column names.*

All the nutrient groups from the Nutrient Analysis table are covered below. Each entry gives a plain-language description of one nutrient NuMa tracks, links to where it's discussed elsewhere in this manual, a link to a respected outside source for anyone who wants to go deeper than a nutrient table can show, and, under **Where to find it**, where to get a value a food is missing. Amino acids aren't repeated here — they already have their own extensive treatment; start at [Essential Amino Acids](#aa).

Each entry ends with the nutrient's **[data key](#gloss-data-key)**, the name NuMa uses for it internally. You never need it to use NuMa; it's there so a technically inclined reader can find the nutrient in the program's data files or code.

---

##### When a food has no data for a nutrient {: #key-sources}

*Search terms: where to find values, data sources, nutrient data, missing data.*

A food with no figure for a nutrient adds nothing to a meal's or recipe's total for it, so the total comes out too low. Under [Top Contributors](#top-contributors), the list of foods with no data shows which foods those are, with a **Find this data** button beside each; Foods → 9 lists every food you use that has [missing nutrient data](#data-completeness).

**Try these sources in this order.** Each nutrient's entry below says where it differs.

1. **The same food in [USDA](#gloss-usda)**, in a Foundation or [SR](#gloss-sr) Legacy record — the most complete records there are. Branded USDA records list only what's on the package label. *In NuMa:* **Find this data** (or **Fill in nutrients from another food** on the food's page) searches for the food's own name; pick a USDA match and copy the values it lacks. For a food that is already a USDA food, try **Refresh from USDA** on its page first: USDA sometimes adds values.
2. **Another national food database**: the Canadian Nutrient File (searched online), and the UK CoFID, Australian AFCD and French CIQUAL databases bundled with NuMa. *In NuMa:* the same search covers all four; their codes say which a result came from: CNF (Canadian Nutrient File), [CoFID](#gloss-cofid), [AFCD](#gloss-afcd) and [CIQUAL](#gloss-ciqual).
3. **The package label**, for a packaged food: calories, fat, saturated fat, carbohydrate, sugar, fiber, protein and sodium, and on US labels also calcium, iron, potassium and vitamin D. Open Food Facts holds many labels; the same search includes it (code [OFF](#gloss-off)). A label never lists water, amino acids, carotenoids or most vitamins.
4. **A close, similar food** — tomato purée for a tomato sauce, another bean for a bean. Same search; a value borrowed this way is marked *estimated* on the food's page. A homemade dish is usually better entered as a [recipe](#recipes-menu-web) of its ingredients, so its values come from them.
5. **Claude AI.** On the food's Edit page, use **Ask Claude AI for help** ([Workflow 12](#fix-food-data)), or on Foods → 9 tick the food's group in *Missing nutrient data* and [fetch the missing values from Claude](#fetch). Last, because the figures need checking: ask for the source and look at it. An import only fills blanks.
6. **Nobody has it.** Some nutrients are measured for few foods anywhere (several phytonutrients, below). Then the honest answer is that the total is a minimum. Marking the gap **not needed**, from the Top Contributors list ([how](#contrib-no-data-answers)) or for its whole group in Foods → 9's *Missing nutrient data* list, stops NuMa asking about it and leaves it out of Claude prompts. The total is still a minimum. If you know the food has none, **Has none — record 0** says so instead.

**Amino acids.**{: #key-sources-aa} The same order, with these differences. USDA SR Legacy has full amino acid profiles for thousands of foods, and the Canadian Nutrient File for many; the Australian database has them for about one food in eight; the UK and French databases have none, and labels never list them. When you copy amino acids from a similar food, NuMa scales them to this food's own protein rather than copying them raw (see [Fill in nutrients from another food](#review-incoming)). A food with very little protein can simply be marked **Amino acids not needed** (see [Missing Amino Acid Profiles](#missing-aa-off)).

---

##### Macronutrients

*Search terms: macros.*

**The indentation below shows the real parent/child relationship among these** — Calories, Protein, Carbohydrates, and Fat are the four independent top-level macronutrients (none is a subset of another); Carbohydrates and Fat each break down further into the sub-rows nested beneath them. NuMa's own nutrient tables (food, recipe, meal, and daily-summary pages, plus the printable report) show this same hierarchy visually too — Fiber, Sugar, and the three fat types are indented under their parent row, the way a Nutrition Facts label does (completed 2026-09-19).

###### Calories {: #key-calories}
The energy a food provides, from protein, carbohydrate, fat, and alcohol combined. NuMa estimates your personal daily calorie target using the Mifflin-St Jeor equation and your activity level — see [Daily Nutrient Goals](#goals) for the full calculation and the [RDA](#gloss-rda)/[DRI](#gloss-dri) framework it draws on[^9].

**Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; every food database and label has it. A food with protein, carbohydrate and fat but no calories doesn't need a source: NuMa works them out from those three and marks the figure *estimated* (see [food data problems](#calorie-checks)).

**[Data key](#gloss-data-key):** *calories*

###### Protein {: #key-protein}
Builds and repairs every cell in the body and is the nutrient NuMa focuses on most closely, since how much of it your body can actually *use* depends on both digestibility and amino acid completeness, not just the gram total on a label. See [Digestible Complete Protein](#dcp) and [Essential Amino Acids](#aa) for how NuMa scores protein quality beyond this raw figure, and [Recommended Dietary Allowances](#rda) for how your target is set. For more, see *Dietary Proteins* from MedlinePlus[^17].

**Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; every food database has it.

**[Data key](#gloss-data-key):** *protein_g*

###### Carbohydrates {: #key-carbs}
The body's primary energy source. **Fiber and Sugar below are subsets of this total, not additional to it** — Fiber + Sugar + Starch + a few minor carbohydrate types add up to the Carbohydrates figure, the same relationship a Nutrition Facts label shows by indenting "Dietary Fiber" and "Total Sugars" under "Total Carbohydrate." NuMa uses carbohydrate content, alongside a food's glycemic index, to compute [Glycemic Load](#gl). For more, see *Carbohydrates* from MedlinePlus[^18].

**Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; every food database has it. **Watch the definition:** USDA's and the Canadian figure include fiber, but the UK, Australian and French databases give *available* carbohydrate, with fiber left out, so their figure runs lower by the food's fiber. Copying one from those three, add the fiber back if you want it to match USDA's.

**[Data key](#gloss-data-key):** *carbs_g*

- **Fiber**{: #key-fiber} — The indigestible part of plant carbohydrate. NuMa's figure is [USDA](#gloss-usda)'s "total dietary fiber" — **soluble and insoluble combined**, not insoluble alone. The two behave differently: soluble fiber (oats, beans, apples, citrus) dissolves into a gel that slows digestion and is linked to lower cholesterol and better blood-sugar control; insoluble fiber (whole grains, vegetable skins, wheat bran) adds bulk and speeds transit, supporting digestive regularity. NuMa doesn't split the two because USDA FoodData Central only reports that breakdown for a small fraction of foods — reliably showing it would mean leaving it blank almost everywhere. Fiber is one of the few macronutrients using an Adequate Intake rather than a full [RDA](#gloss-rda) — see [Daily Nutrient Goals](#goals) for what that distinction means for your target. For more, see *Dietary Fiber* from MedlinePlus[^20].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed. The UK database has it for only about half its foods; the others for nearly all.
    - **[Data key](#gloss-data-key):** *fiber_g*
- **Sugar**{: #key-sugar} — Simple carbohydrate — both naturally occurring (fruit, dairy) and added (sweeteners) — that NuMa reports as one combined total. High-sugar foods tend to raise [Glycemic Load](#gl) sharply; see that section for how NuMa weighs sugar's blood-glucose impact against a food's fiber and overall carbohydrate. For more, see *Sweeteners – Sugars* from MedlinePlus[^21].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; nearly every database and label has it.
    - **[Data key](#gloss-data-key):** *sugar_g*
- *Starch is not tracked as its own row — USDA rarely reports it as a distinct value, so it stays folded into the Carbohydrates total along with everything else that isn't Fiber or Sugar.*

###### Fat {: #key-fat}
Total dietary fat. **Saturated, Monounsaturated, and Polyunsaturated fat below are subsets of this total, not additional to it** — the three add up to (approximately) the Fat figure. Fat itself sits at the same level as Protein and Carbohydrates above, not beneath them — it's a third independent macronutrient, not a subset of either. See [Omega-3 Fatty Acids](#omega3) for the specific unsaturated fatty acids NuMa tracks individually and gives their own goals. For more, see *Dietary fats explained* from MedlinePlus[^19].

**Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; every food database and label has it.

**[Data key](#gloss-data-key):** *fat_g*

- **Saturated fat**{: #key-saturated-fat} — The fat subtype most consistently linked to cardiovascular risk when eaten in excess; most dietary guidance favors keeping intake low and replacing it with unsaturated fat where possible. For more, see *Saturated Fat* from Examine.com[^22].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; labels give it too.
    - **[Data key](#gloss-data-key):** *saturated_fat_g*
- **Monounsaturated fat**{: #key-mono-fat} — Found mainly in olive oil, avocados, and many nuts; generally considered neutral-to-beneficial for cardiovascular health when it displaces saturated fat in the diet. For more, see *Dietary fats explained* from MedlinePlus[^19].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label; about three foods in four in the UK and French databases have it.
    - **[Data key](#gloss-data-key):** *mono_fat_g*
- **Polyunsaturated fat**{: #key-poly-fat} — Includes the omega-3 and omega-6 fatty acids NuMa tracks individually — see [Omega-3 Fatty Acids](#omega3) for [ALA](#gloss-ala), [EPA](#gloss-epa), [DHA](#gloss-dha), and linoleic acid specifically, and why ALA is the only one with an official intake goal. For more, see *Dietary fats explained* from MedlinePlus[^19].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label; about three foods in four in the UK and French databases have it.
    - **[Data key](#gloss-data-key):** *poly_fat_g*

---

##### Water

*Search terms: hydration, fluids, fluid intake.*

###### Water {: #key-water}
The water a food or drink contains, measured as its moisture. NuMa adds it up from everything you log, and splits a meal's or day's total into **Water from drinks** (from foods and recipes marked as a drink) and **Water from food** (everything else); the split isn't stored with a food, so a food's own figure is just its water. See [Water: from drinks and from food](#water) for the goals and what counts as water.

**Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, and almost always at step 1 or 2: [USDA](#gloss-usda), the Canadian Nutrient File and the UK and Australian databases have it for nearly every food, the French database for most. Labels never list it, so a packaged food needs a matching generic food (a jarred tomato sauce takes a USDA or [CIQUAL](#gloss-ciqual) tomato sauce's value). For all your USDA foods at once, Foods → 9 fills it in from USDA (see [Gaps in the data](#water-gaps)). Make sure the match is in the same state: a dry food (flour, powder, dried beans) has very little water, and the same food cooked or soaked a lot (see [A wet food picked for a dry one](#water-wet-dry)).

**[Data keys](#gloss-data-key):** *water_g*; the drinks/food split is *water_drinks_g* and *water_food_g*

---

##### Omega Fatty Acids

*Search terms: fish oil, essential fatty acids, PUFA.*

**Grouped below by fatty acid family (omega-3 vs. omega-6) — a real biochemical classification, but not a sum like Carbohydrates/Fat above:** there's no single "total omega-3" figure these three add up to; [ALA](#gloss-ala), [EPA](#gloss-epa), and [DHA](#gloss-dha) are each reported and goal-tracked independently. See [Omega-3 Fatty Acids](#omega3) for the full discussion, including why only ALA has an official intake goal and how the ALA→EPA→DHA conversion pathway works. External (covers this entire group): Linus Pauling Institute, *Essential Fatty Acids*[^23].

###### Omega-3

- **[ALA](#gloss-ala)**{: #key-ala} — Alpha-linolenic acid, the plant-based omega-3 (flaxseed, walnuts, chia, canola and soy oils). The only omega-3 with an official Adequate Intake, so it's the only one of the three with a Daily Goal.
    - **Where to find it:** [USDA](#gloss-usda) Foundation and [SR](#gloss-sr) Legacy records, the Canadian Nutrient File and the Australian database; the French database for about half its foods; not the UK database as bundled, and never a label. Then Claude (step 5 of the [six data sources](#key-sources) NuMa uses).
    - **[Data key](#gloss-data-key):** *omega3_ala_mg*
- **[EPA](#gloss-epa)**{: #key-epa} — Eicosapentaenoic acid. No U.S. [DRI](#gloss-dri) exists for EPA on its own; the body makes some from ALA, inefficiently, or gets it directly from fish, algae, and other seafood. Set your own [Revised Optimal target](#optimal) if you want to track it against a number.
    - **Where to find it:** USDA Foundation and SR Legacy records, the Canadian Nutrient File and the Australian database; the French database for about half its foods; not the UK database as bundled, and never a label. Then Claude (step 5 of the [six data sources](#key-sources) NuMa uses). A plant food missing EPA has essentially none: EPA comes from fish, seafood and algae.
    - **[Data key](#gloss-data-key):** *omega3_epa_mg*
- **[DHA](#gloss-dha)**{: #key-dha} — Docosahexaenoic acid, the omega-3 most concentrated in the brain and retina. Like EPA, it has no official DRI and can be tracked against a self-set [Revised Optimal target](#optimal) instead.
    - **Where to find it:** USDA Foundation and SR Legacy records, the Canadian Nutrient File and the Australian database; the French database for about half its foods; not the UK database as bundled, and never a label. Then Claude (step 5 of the [six data sources](#key-sources) NuMa uses). A plant food missing DHA has essentially none: DHA comes from fish, seafood and algae.
    - **[Data key](#gloss-data-key):** *omega3_dha_mg*

###### Omega-6

- **Linoleic acid (LA)**{: #key-la} — The essential omega-6 fatty acid. Has a Daily Goal, its Adequate Intake (17 g men, 12 g women under 51); that figure is the typical U.S. intake, and deficiency is essentially unknown on ordinary diets — see [Omega-3 Fatty Acids](#omega3).
    - **Where to find it:** [USDA](#gloss-usda) Foundation and [SR](#gloss-sr) Legacy records, the Canadian Nutrient File and the Australian database; the French database for about half its foods; not the UK database as bundled, and never a label. Then Claude (step 5 of the [six data sources](#key-sources) NuMa uses).
    - **[Data key](#gloss-data-key):** *omega6_la_mg*

---

##### Minerals

*Search terms: electrolytes, trace elements.*

**Grouped below by the standard nutrition-science split between macrominerals (needed in gram-per-day amounts) and trace minerals (needed in milligram or microgram amounts)** — a categorical family, like Omega-3 vs. Omega-6 above, not a sum relationship.

###### Macrominerals

- **Calcium**{: #key-calcium} — Builds and maintains bone, and supports nerve and muscle function. A major dietary source for many people (dairy, fortified plant milks, leafy greens) is undermined by [oxalates](#antinutrients) in some of those same leafy greens — spinach's labeled calcium is largely unabsorbed. For more, see *Calcium* from the Linus Pauling Institute[^24].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; US labels give it too.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: mainly a supplement risk, not a food risk — getting this much from food alone is difficult. [NIH](#gloss-nih) notes higher-dose calcium supplements are linked to a greater risk of kidney stones, and some research ties them to a higher risk of cardiovascular disease[^48].
    - **[Data key](#gloss-data-key):** *calcium_mg*
- **Magnesium**{: #key-magnesium} — Involved in hundreds of enzyme reactions, including energy production and muscle/nerve function. A candidate for a future [Revised Optimal](#optimal) target above the [RDA](#gloss-rda) — see [Expanding Revised Optimal (Recent Research) targets](#expand-revised-optimal) — though the evidence for a specific above-RDA number is less settled than for vitamin D. For more, see *Magnesium* from the Linus Pauling Institute[^25].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label.
    - **[Data key](#gloss-data-key):** *magnesium_mg*
- **Phosphorus**{: #key-phosphorus} — Works alongside calcium in bone structure and is also central to cellular energy (ATP). Deficiency is rare in any diet with adequate protein, since phosphorus is present in most protein-rich foods. For more, see *Phosphorus* from the Linus Pauling Institute[^26].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: NIH notes high intakes seldom cause problems in otherwise healthy people; the real concern is chronic kidney disease, where the kidneys can't clear excess phosphorus and it builds up in the blood, worsening bone and kidney health[^49].
    - **[Data key](#gloss-data-key):** *phosphorus_mg*
- **Potassium**{: #key-potassium} — Supports fluid balance, nerve signaling, and healthy blood pressure; typically under-consumed relative to its Adequate Intake in a typical Western diet. For more, see *Potassium* from the Linus Pauling Institute[^27].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; US labels give it too.
    - **[Data key](#gloss-data-key):** *potassium_mg*
- **Sodium**{: #key-sodium} — The one nutrient in NuMa's tables with its own Maximum column entry rather than a Minimum — see [Recommended Dietary Allowances](#rda) for the Maximum-vs-UL distinction and [Maximum Nutrient Limits](#maxlimits) for how NuMa flags approaching it. For more, see *Sodium* from the Linus Pauling Institute[^28].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; every database and label has it. A label that gives salt instead: sodium is salt ÷ 2.5 (1 g salt = 400 mg sodium).
    - **[Data key](#gloss-data-key):** *sodium_mg*

###### Trace Minerals

- **Iron**{: #key-iron} — Carries oxygen in red blood cells. Plant (non-heme) iron absorbs far less efficiently than animal (heme) iron and is further blocked by [phytates](#antinutrients) — NuMa raises the iron [RDA](#gloss-rda) target 1.8× on a Vegetarian or Plant-based dietary preference to reflect this; see [Diet-Aware Bioavailability Notes](#diet-bioavailability)[^4]<sup>,</sup>[^5]. For more, see *Iron* from the Linus Pauling Institute[^29].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; US labels give it too.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: acute overdose (often accidental, in children) can cause severe gastrointestinal damage and organ failure; chronically, people with hemochromatosis (an inherited iron-overload condition) should avoid iron and vitamin C supplements, since excess iron builds up and can damage the liver and heart[^50].
    - **[Data key](#gloss-data-key):** *iron_mg*
- **Zinc**{: #key-zinc} — Supports immune function and wound healing; absorption is reduced by the same [phytates](#antinutrients) that affect iron. NuMa raises the zinc RDA target 1.5× on a Vegetarian or Plant-based preference — see [Diet-Aware Bioavailability Notes](#diet-bioavailability)[^4]<sup>,</sup>[^6]. For more, see *Zinc* from the Linus Pauling Institute[^30].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label; the French database has it for about two foods in three.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: nausea, vomiting, and gastric distress in the short term. Sustained high doses interfere with copper absorption, which can itself cause neurological problems (loss of coordination, numbness, weakness) if it leads to copper deficiency[^51].
    - **[Data key](#gloss-data-key):** *zinc_mg*
- **Iodine**{: #key-iodine} — Required for thyroid hormone production. Iodized salt is the primary dietary source in most Western diets; those avoiding it (and not eating much seafood or dairy) are the main deficiency risk group. For more, see *Iodine* from the Linus Pauling Institute[^31].
    - **Where to find it:** Often missing. The Australian database has it for every food, the UK database for about half and the French for about a third; USDA records rarely have it and the Canadian file doesn't. Outside NuMa, the [USDA](#gloss-usda), FDA (Food and Drug Administration) and [NIH](#gloss-nih) *Database for the Iodine Content of Common Foods* covers US foods; take a value from it to Claude or a similar food. Then try the [six data sources](#key-sources) NuMa uses, in the order listed.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: ironically similar to deficiency — high intakes can trigger goiter and thyroid gland inflammation. Very large single doses (gram-range, essentially unreachable from food) can cause burning of the mouth and throat, fever, and vomiting[^52].
    - **[Data key](#gloss-data-key):** *iodine_mcg*
- **Selenium**{: #key-selenium} — An antioxidant-supporting trace mineral; Brazil nuts are an unusually concentrated source (a couple a day can exceed the daily target). For more, see *Selenium* from the Linus Pauling Institute[^32].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label; the UK database has it for about three foods in five, the French for about one in three.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: chronic over-intake causes selenosis — hair loss, brittle nails, a garlic odor on the breath, and nausea are the classic signs; very high intakes can affect the nervous system and, rarely, the heart[^53].
    - **[Data key](#gloss-data-key):** *selenium_mcg*

---

##### Vitamins

*Search terms: multivitamin, B vitamins.*

**Grouped below by the standard fat-soluble vs. water-soluble split** — fat-soluble vitamins are stored in body fat and can build up to toxic levels with excess supplementation; water-soluble vitamins are not stored the same way and excess is typically excreted in urine (vitamin B6 is a partial exception at very high supplemental doses). Again a categorical family, not a sum relationship.

###### Fat-Soluble

- **Vitamin A**{: #key-vitamin-a} — Supports vision, immune function, and cell growth. NuMa's figure is already expressed in mcg RAE (Retinol Activity Equivalents) — [USDA](#gloss-usda)'s own standardized unit that converts provitamin-A carotenoids (see Beta-carotene and Alpha-carotene under Phytonutrients below) into vitamin-A-equivalent amounts using their own conversion factors, not a simple sum. For more, see *Vitamin A* from the Linus Pauling Institute[^33].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, with a caution: the Canadian and French figures in NuMa count only retinol, the animal form, so for a plant food they understate it, often to zero. For a plant food prefer USDA, the UK or the Australian database.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9] (that UL applies to preformed vitamin A specifically, a narrower figure than the mcg RAE total NuMa tracks — see the note there; [NIH](#gloss-nih) notes there's no established UL for beta-carotene and other provitamin-A carotenoids).
    - Risk of excess: getting too much preformed vitamin A (usually from supplements, liver, or certain medicines, rarely from food alone) can cause headache, blurred vision, nausea, dizziness, and coordination problems; long-term excess is also linked to reduced bone strength and, in pregnancy, to birth defects[^54].
    - **[Data key](#gloss-data-key):** *vitamin_a_mcg*
- **Vitamin C**{: #key-vitamin-c} — An antioxidant vitamin also needed for collagen synthesis; notably, vitamin C consumed at the same meal significantly improves absorption of non-heme iron from plant foods — see [Antinutrients](#antinutrients). For more, see *Vitamin C* from the Linus Pauling Institute[^34].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; the French database has it for about half its foods.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: mostly mild — diarrhea, nausea, and stomach cramps at high intakes. In people with hemochromatosis (an iron-overload condition), high-dose vitamin C can worsen iron overload and tissue damage[^55].
    - **[Data key](#gloss-data-key):** *vitamin_c_mg*
- **Vitamin D**{: #key-vitamin-d} — Supports calcium absorption and bone health. NuMa's built-in [Revised Optimal](#optimal) default goes above the standard [RDA](#gloss-rda) based on Endocrine Society guidance[^12] — see that section for why. For more, see *Vitamin D* from the Linus Pauling Institute[^35].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; US labels give it too. Often missing for plant foods because there's almost none to measure; mushrooms grown under ultraviolet (UV) light are the exception, and a fortified food's label has it.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: essentially a supplement-only risk (sun exposure and food don't cause it). Excess vitamin D drives calcium too high in the blood (hypercalcemia) and urine, which in turn can cause nausea, weakness, and mineral deposits in soft tissue and blood vessels[^56].
    - **[Data key](#gloss-data-key):** *vitamin_d_mcg*
- **Vitamin E**{: #key-vitamin-e} — An antioxidant vitamin that protects cell membranes from oxidative damage; found concentrated in nuts, seeds, and vegetable oils. For more, see *Vitamin E* from the Linus Pauling Institute[^36].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; the French database rarely has it.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: a supplement-only risk — NIH notes no adverse effects from vitamin E in food, only from high-dose supplements. The main concern is bleeding risk, since high doses reduce the blood's ability to clot; this is especially relevant alongside blood-thinning medication like warfarin[^57].
    - **[Data key](#gloss-data-key):** *vitamin_e_mg*
- **Vitamin K**{: #key-vitamin-k} — Needed for blood clotting and bone metabolism. NuMa tracks vitamin K1 (from the RDA); vitamin K2, a distinct form with separate emerging research on cardiovascular and bone benefits, is not yet reflected in an official [DRI](#gloss-dri) — see [Expanding Revised Optimal (Recent Research) targets](#expand-revised-optimal) for that as a candidate future addition. For more, see *Vitamin K* from the Linus Pauling Institute[^37].
    - **Where to find it:** USDA [SR](#gloss-sr) Legacy and the Canadian Nutrient File; the French database for about a third of its foods; the UK database rarely and the Australian not at all. Then Claude (step 5 of the [six data sources](#key-sources) NuMa uses).
    - **[Data key](#gloss-data-key):** *vitamin_k_mcg*

###### Water-Soluble

- **Thiamin (B1)**{: #key-thiamin} — Needed for converting food into energy and for nerve function. Deficiency (beriberi) is rare in a varied diet but historically arose in populations relying heavily on unenriched white rice. For more, see *Thiamin* from the Linus Pauling Institute[^38].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label (except an enriched or fortified food's).
    - **[Data key](#gloss-data-key):** *thiamin_mg*
- **Riboflavin (B2)**{: #key-riboflavin} — Supports energy production and functions as an antioxidant; widely available in dairy, eggs, meat, and fortified grains, so deficiency is uncommon. For more, see *Riboflavin* from the Linus Pauling Institute[^39].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label (except an enriched or fortified food's).
    - **[Data key](#gloss-data-key):** *riboflavin_mg*
- **Niacin (B3)**{: #key-niacin} — Involved in energy metabolism and [DNA](#gloss-dna) repair. Corn-based diets can carry a deficiency risk (pellagra) unless the corn is nixtamalized — see **Bound niacin** under [Antinutrients](#antinutrients). For more, see *Niacin* from the Linus Pauling Institute[^40].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label (except an enriched or fortified food's).
    - **[Data key](#gloss-data-key):** *niacin_mg*
- **Vitamin B6**{: #key-b6} — Involved in amino acid metabolism and neurotransmitter synthesis. One of the few water-soluble vitamins where very high long-term supplemental doses (not food intake) carry a real toxicity risk (nerve damage). For more, see *Vitamin B6* from the Linus Pauling Institute[^41].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed, but not from a label.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: people almost never get too much B6 from food. Taking high-dose supplements for a year or longer can cause severe, sometimes irreversible nerve damage (loss of control of body movements), along with painful skin patches and extreme sun sensitivity[^58].
    - **[Data key](#gloss-data-key):** *b6_mg*
- **Folate**{: #key-folate} — Essential for cell division and DNA synthesis; especially critical before and during early pregnancy to prevent neural tube defects. For more, see *Folate* from the Linus Pauling Institute[^42].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed; the French database has it for about two foods in five.
    - **[Data key](#gloss-data-key):** *folate_mcg*
- **Vitamin B12**{: #key-b12} — Needed for nerve function and red blood cell formation. Almost exclusively animal-sourced[^7] — NuMa shows a specific low-intake warning on a Plant-based only dietary preference; see [Diet-Aware Bioavailability Notes](#diet-bioavailability). For more, see *Vitamin B12* from the Linus Pauling Institute[^43].
    - **Where to find it:** the [six data sources](#key-sources) NuMa uses, tried in the order listed. An unfortified plant food missing it has essentially none; a fortified one (plant milk, nutritional yeast, cereal) has it on its label.
    - **[Data key](#gloss-data-key):** *b12_mcg*

---

##### Phytonutrients

*Search terms: phytochemicals.*

**Grouped below into carotenoids (a defined chemical family) vs. everything else** — again categorical, not a sum. Phytonutrients have no established Dietary Reference Intake, so none of these show a "% of daily target" figure the way vitamins and minerals do — see [Recommended Dietary Allowances](#rda).

###### Carotenoids

- **Beta-carotene**{: #key-beta-carotene} — A provitamin-A carotenoid (orange/red pigment in carrots, sweet potatoes, squash); the body converts it to vitamin A, feeding into the Vitamin A (RAE) figure above via [USDA](#gloss-usda)'s own conversion factor rather than a simple sum.
    - **Where to find it:** USDA, the Australian database, the UK database (whose figure is total carotene) and the French database for about half its foods. Then Claude (step 5 of the [six data sources](#key-sources) NuMa uses). Foods that aren't orange, red or green have little.
    - **[Data key](#gloss-data-key):** *beta_carotene_mcg*
- **Alpha-carotene**{: #key-alpha-carotene} — A second provitamin-A carotenoid, generally present alongside beta-carotene in orange vegetables, converted to vitamin A less efficiently.
    - **Where to find it:** Mostly USDA Foundation and [SR](#gloss-sr) Legacy records; the Australian database for about two foods in three; not the other databases. Often measured nowhere: step 6 of the [six data sources](#key-sources) NuMa uses ("Nobody has it") is a fair answer.
    - **[Data key](#gloss-data-key):** *alpha_carotene_mcg*
- **Lycopene**{: #key-lycopene} — The red carotenoid in tomatoes and watermelon; unlike the two above, it has no vitamin A activity — it's tracked purely for its own antioxidant interest.
    - **Where to find it:** Almost only USDA Foundation and SR Legacy records. Only red foods (tomato, watermelon, pink grapefruit, guava) have much, so a missing value elsewhere is usually near zero; for a tomato product, a USDA tomato match is worth finding.
    - **[Data key](#gloss-data-key):** *lycopene_mcg*
- **Lutein + Zeaxanthin**{: #key-lutein} — Carotenoids concentrated in the retina, where they're associated with eye health; found in leafy greens, corn, and eggs. Also no vitamin A activity. External (covers all four carotenoids above): Linus Pauling Institute, *Carotenoids*[^45].
    - **Where to find it:** Almost only USDA Foundation and SR Legacy records. Often measured nowhere: step 6 of the [six data sources](#key-sources) NuMa uses ("Nobody has it") is a fair answer.
    - **[Data key](#gloss-data-key):** *lutein_zeaxanthin_mcg*

###### Other Phytonutrients

- **Choline**{: #key-choline} — Needed for cell membrane structure and neurotransmitter synthesis; a meaningful share of adults fall short of even its Adequate Intake — a candidate for a future [Revised Optimal](#optimal) target, see [Expanding Revised Optimal (Recent Research) targets](#expand-revised-optimal). For more, see *Choline* from the Linus Pauling Institute[^44].
    - **Where to find it:** [USDA](#gloss-usda) [SR](#gloss-sr) Legacy and Foundation records and the Canadian Nutrient File only; none of the other databases or labels. Then Claude (step 5 of the [six data sources](#key-sources) NuMa uses).
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: a fishy body odor is the classic tell (from a choline metabolite excreted in sweat and urine); [NIH](#gloss-nih) also lists low blood pressure, sweating, and liver damage at high intakes, with some research linking very high intakes to cardiovascular risk[^59].
    - **[Data key](#gloss-data-key):** *choline_mg*
- **Beta-sitosterol**{: #key-beta-sitosterol} — A plant sterol structurally similar to cholesterol; dietary intake is associated with modestly lower [LDL](#gloss-ldl) cholesterol. For more, see *Phytosterols* from the Linus Pauling Institute[^47].
    - **Where to find it:** USDA only, and for few foods (nuts, seeds, oils, legumes mainly). Usually measured nowhere: step 6 of the [six data sources](#key-sources) NuMa uses ("Nobody has it") is a fair answer.
    - **[Data key](#gloss-data-key):** *beta_sitosterol_mg*
- **Isoflavones**{: #key-isoflavones} — Plant compounds with mild estrogen-like activity, found mainly in soy; frequently discussed in the context of soy's role in a plant-based diet. For more, see *Soy Isoflavones* from the Linus Pauling Institute[^46].
    - **Where to find it:** USDA, for soy foods mainly; outside NuMa, USDA's separate *Database for the Isoflavone Content of Selected Foods* is the standard source, worth giving to Claude. A food without soy or other legumes has essentially none.
    - **[Data key](#gloss-data-key):** *isoflavones_mg*

---

## Part 8 — Your data {: #your-data}

*(Reading time: 15 minutes)*

Where NuMa's food data comes from, what NuMa keeps on your computer, how to back it up, and how NuMa's results are checked.

### A. Food data — where it comes from and how it is stored {: #food-data}

*Search terms: data sources, nutrition databases, API key sign-up, free USDA key.*

NuMa's food data comes from six large databases:

- **[USDA](#gloss-usda) FoodData Central** — the U.S. government's nutrition [database](#gloss-database), covering hundreds of thousands of whole foods, ingredients, and branded products. This is NuMa's primary source. ([FoodData Central FAQ](https://fdc.nal.usda.gov/faq/))
- **Open Food Facts** — a community-maintained [database](#gloss-database) of packaged and processed food products, especially useful for branded items not found in the [USDA](#gloss-usda) table. ([Open Food Facts](https://world.openfoodfacts.org/discover))
- **Canadian Nutrient File** — Health Canada's reference [database](#gloss-database), particularly good on amino acid coverage. ([Canadian Nutrient File](https://food-nutrition.canada.ca/cnf-fce/?lang=eng))
- **UK CoFID** — ~2,900 UK foods from Public Health England/[DHSC](#gloss-dhsc), bundled into NuMa directly rather than looked up live (it has no [API](#gloss-api) of its own). No amino acid data. ([CoFID](https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid))
- **Australian [AFCD](#gloss-afcd)** — ~1,600 Australian foods from [FSANZ](#gloss-fsanz), also bundled directly. Has real amino acid data, unlike CoFID. ([AFCD](https://www.foodstandards.gov.au/science-data/monitoringnutrients/afcd))
- **French [CIQUAL](#gloss-ciqual)** — ~3,500 French/European foods from [ANSES](#gloss-anses), also bundled directly. No amino acid data. ([CIQUAL](https://ciqual.anses.fr/))

<span id="usda-api-key"></span>**Your own [USDA](#gloss-usda) API key.** NuMa reaches FoodData Central through USDA's public API. Without your own key it uses a shared demonstration key (DEMO_KEY) whose tight limit anyone's heavy use can exhaust, making searches fail for a while. A key is free and takes a minute:

1. Go to https://fdc.nal.usda.gov/api-key-signup and enter your name and email.
2. [USDA](#gloss-usda) emails you a key immediately.
3. Enter it in **Settings → 6. [USDA](#gloss-usda) API Key** and click **Save key** (the box shows your saved key, so you can find it again there).

**NuMa checks the key with USDA when you save it.** If USDA accepts it, you'll see *API key saved, and USDA accepted it*. If USDA rejects it (usually a few characters missing from a copy and paste), the key is **not** saved, so your searches keep working with whatever you had before; copy the whole key from USDA's email and try again. If NuMa can't reach USDA at that moment (you're offline, say), it saves the key anyway and says it couldn't check it.

**Test key**, beside **Save key**, asks USDA again whether your saved key still works, and the line under the buttons shows when it was last checked and what USDA said. If USDA searches start failing with "API key rejected", click **Test key** first: if USDA rejects it, paste a fresh key, or click **Clear key** to go back to `DEMO_KEY`.

It's stored only on your computer, and gives a much higher limit. **Search result depth** is set on the same page ([what it does](#search-ranking)).

Every food in these databases has a unique [ID](#gloss-id) number, like a product code.

**Your [Food Cache](#gloss-food-cache)**{: #FoodCache}, on your own computer, keeps a copy of every food you pick from a search. Searches check it first, so foods you've used before appear at once, offline; over time most of what you eat will be there.

**Edit protection.** A food you change is marked user-edited (its type reads, say, "[SR](#gloss-sr) Legacy · user-edited"), and NuMa never silently replaces it with a fresh USDA copy. When you ask for fresh data with **Refresh**, you see it beside yours and choose value by value ([how](#review-incoming)).

NuMa tracks *which* values you changed, listed on the food's page under **Your changes to this food's original values**, each beside the original. The mark lasts while any change of yours remains, or a GI, DIAAS or preparation note of yours; change everything back and it goes. (A food edited before this tracking says so; one Refresh from USDA sorts it out.)

**Refreshing a food, or filling it in from another food.**{: #review-incoming} Both open the same review screen: each differing value, current beside incoming, and only ticked values are written.

- **Refresh** (Food Cache list, or **Refresh from USDA** on a USDA food's page) fetches USDA's current copy of the food.
- **Fill in nutrients from another food** (on a food's page; custom foods have it on their Edit page) searches for a similar food to take values from. **Compare** boxes on results let you weigh several first, each then with a **Fill in ... from ...** button. Your ticks are kept when you search again and when you come back from Compare; **Clear all picks** unticks them.

What's ticked for you:

- A value that **fills a blank** is always ticked.
- On a Refresh, a value that **differs** is ticked when the food's value is just USDA's older figure, and unticked when it's one you changed (marked **yours**), so yours is kept unless you choose otherwise.
- From another food, a value that differs from one the food already has is unticked.
- Matching values are only counted; a value USDA no longer lists is kept, and named.
- **Tick only blanks**, **Tick all** and **Tick none** change every tick at once.

A Refresh offers the name, brand and serving size the same way. Portions are never changed (logged `p1`s depend on them), though new USDA portions are offered as additions.

Filling in changes the food itself, so every meal and recipe using it updates, and it becomes user-edited. A note above **Write the ticked values** says how the user-edited mark will change.

**Keeping the old version for past meals.**{: #keep-version} A Refresh normally changes the food everywhere, past meals included. If the food itself changed (a reformulated product, revised USDA figures), tick **Keep this food's current values for meals logged before** and pick a date. The current values become an *older version* with its own [code](#gloss-code) (**U171477.1**, type "Branded · 2025-07-13"); earlier meals switch to it and keep their totals, while later meals and all recipes get the new values. The food's page lists its older versions; they stay out of searches. To merge one back, use **Substitute** on Food Use in Meals.

**Amino acids from another food are scaled, not copied**, to this food's protein (or to the source's protein if you tick that too); a food with no protein value needs one first. The notes record the source. Filling only some amino acids mixes two sources, and the screen says so.

**Estimates give way to measured values:** a later Refresh with USDA's measured figure ticks it, even on an edited food, and a meal's **Refresh from USDA** replaces estimated amino acids with measured ones automatically.

A meal page's **Refresh from USDA** handles all its foods at once without asking: it only fills blanks, then lists foods whose USDA copy differs elsewhere, linked to this review.

**Omega fats.** NuMa tracks [ALA](#gloss-ala) (plant omega-3: flaxseed, walnuts, chia), [EPA](#gloss-epa) and [DHA](#gloss-dha) (marine omega-3) and linoleic acid (the main omega-6), when the data has them.

Foods enter your Food Cache four ways:

1. **From [USDA](#gloss-usda)** or another database: pick a search result and it's saved.
2. **From Open Food Facts[^3]**, the same way.
3. **By barcode:** type the 12-digit [UPC](#gloss-upc)-A or 13-digit [EAN](#gloss-ean) number (spaces and hyphens are ignored) in any food search box, and NuMa looks it up on Open Food Facts; click the result. The fastest way to add packaged foods and supplements. An uncached product needs an online source ticked.
4. **By hand**, as a custom food.

Each keeps its original ID, which the rest of NuMa uses to refer to it.

A name-only pantry entry isn't cached until you **Link a food** ([why](#pantry-name-only)).

**[Food Annotations](#gloss-food-annotation)** hold what you add about a food that no database has:

- **Glycemic index ([GI](#gloss-gi))** (0–100), which neither USDA nor Open Food Facts provides.
- **A [DIAAS](#gloss-diaas) estimate** (0–2.0), for a food without amino acid data ([estimating one](#diaas-estimate-table)).
- **A preparation note** ("boiled 20 minutes").

Each belongs to one cached food, and goes if the food is deleted.

**Recipes** link each ingredient to a Food Cache food (or another recipe), caching a food as it's added.

**[My Pantry](#gloss-my-pantry)** is your list of foods on hand, which complement suggestions look at first.

**One food, one place.** The Food Cache, the Pantry and Custom Food Profiles aren't separate stores. Each food's data lives once, in the Food Cache; Custom Food Profiles lists the ones you made; Pantry entries point to cached foods. So a change to a food shows everywhere at once, with nothing to keep in step.

**Where it all lives.**{: #data-location} Foods, annotations, pantry, recipes and meals are tables in one database file, which sits with your page preferences and any large files you've built (the 2021 GI table) in NuMa's data folder; profiles and your USDA key are in a separate config folder:

- **Windows:** data in `%LOCALAPPDATA%\numa`, config in `%APPDATA%\numa`.
- **Linux:** data in `~/.local/share/numa`, config in `~/.config/numa` (hidden folders; press Ctrl+H in your file manager to see them).

Both folders are kept apart from the program itself, so updating NuMa never touches them. To back them up, restore them, or move your data to another computer, see [Backing up your data](#backup).

### B. A note on amino acid data {: #aa-note-web}

*Search terms: missing amino acids, AA data, refresh food, no amino acid data.*

Foods are cached automatically when you first pick them. A food missing amino acid data has **Refresh** (Food Cache) or **Refresh from [USDA](#gloss-usda)** (a meal's protein section), which [fill in only what's missing unless you choose otherwise](#review-incoming); where data is missing NuMa usually suggests a Foundation or [SR](#gloss-sr) Legacy equivalent. [GI](#gloss-gi) and [DIAAS](#gloss-diaas) estimates go in on **Foods → Annotate**.

---

### C. What's on your computer, and why {: #installed-files}

*Search terms: uninstall, uninstalling, file locations, where my data is stored, disk space.*

NuMa puts only a handful of files on your computer. The program itself is one file; everything else is either a menu shortcut or your own data.

**The program**

| File | What it's for |
|---|---|
| `nutrimagnus.exe` (Windows, in the folder you chose) or `~/.local/bin/nutrimagnus` (Linux) | The whole program, in one file. The built-in User Manual and NuMa's reference tables (oxalate, glycemic index, the UK, Australian and French food databases, starter foods and recipes) are packed inside it. |
| `~/.local/share/icons/nutrimagnus.png` (Linux) | NuMa's icon, for the applications menu. |
| `~/.local/share/applications/nutrimagnus.desktop` (Linux) | The applications-menu entry that starts NuMa. |

**Your data** — created the first time NuMa runs, and never touched by an update. On Windows these folders are `%LOCALAPPDATA%\numa` (data) and `%APPDATA%\numa` (settings); on Linux, `~/.local/share/numa` and `~/.config/numa`.

| File | What it's for |
|---|---|
| `numa.db` (data folder) | Everything you've entered: your Food Cache, pantry, recipes, logged meals, [GI](#gloss-gi) and [DIAAS](#gloss-diaas) notes, and the rest. The one file that matters most to back up. |
| `prefs.json` (data folder) | How you like the pages: sort orders, chosen columns, dismissed notices. |
| `demo_data.json`, `demo_data_seed_attempted`, `starter_versions.json` (data folder) | Small notes about the [starter foods and recipes](#starter-data): which were loaded, and which version of them you have. |
| `manual/` (data folder) | Only if you've clicked **Update manual now**: a newer User Manual than the one inside the program. |
| `numa-errors.log` (data folder) | Only once something has gone wrong: the details of each error, for [reporting a problem](#error-log). |
| `gi_data_local.json` (data folder) | Only if you've built it in Settings → 7: your own copy of the 2021 glycemic index tables. |
| `config.json` (settings folder) | Your [USDA](#gloss-usda) key, if you've entered one, and the search-depth setting. |
| `profiles/`, `active_profile.txt` (settings folder) | Your profiles (age, weight, activity level, targets) and which one is in use. |

To remove NuMa completely, delete the program file (and on Linux the icon and menu entry), then both folders above. To keep your data, keep the folders — see [Backing up your data](#backup).

### D. Backing up your data {: #backup}

*Search terms: migrate, migration, transfer, data loss, lost data, sync, safe copy.*

This section covers your data's location — where NuMa keeps it on your computer — and its storage, backing it up, restoring it, and moving your data to a new computer.

Everything you put into NuMa lives in two folders on your computer, kept apart from the program itself: your foods, pantry, recipes, logged meals, annotations, profile and settings, and your 2021 glycemic index table if you built one (in Settings, item 7).

   - **Windows:** `%LOCALAPPDATA%\numa` and `%APPDATA%\numa`. Type either one, exactly as written, into File Explorer's address bar and press Enter to open it.
   - **Linux:** `~/.local/share/numa` and `~/.config/numa`. These are hidden folders in your home folder; press Ctrl+H in your file manager to show them.

**To back up,** copy both folders somewhere safe — a memory stick, an external drive, or a cloud-synced folder. Do it when NuMa isn't in the middle of saving something; the simplest way is to do it before you start NuMa for the day. Repeat it now and then: a backup only holds what you'd entered when you made it.

**To restore, or to move your data to another computer** — a new computer, or one whose system was wiped — install NuMa ([Windows](#install-windows), [Linux](#install-linux)), but don't start it yet. Copy both backed-up `numa` folders into place, replacing any that exist, and then start NuMa. Everything comes back as it was.

A [CSV](#gloss-csv) export from the Food Cache or Recipes pages is *not* a full backup. It's for moving selected foods or recipes around, and leaves out your meals, pantry, profile and settings (see [Moving foods and recipes with CSV files](#csv-transfer)).

### E. Data, testing, and validation: Why you can trust NutriMagnus (NuMa) {: #data-testing-validation}

#### Reliable data sources

<!-- t:26-10-28 -->

*Search terms: where the numbers come from, trustworthy, accuracy, reliability.*

**[NuMa](#gloss-numa) draws on multiple data sources, and tells you which ones it is using.** Wherever the program makes a suggestion, it shows you which sources it consulted.

- **[USDA](#gloss-usda) FoodData Central**[^2] — the primary nutrient [database](#gloss-database), one of the most comprehensive public nutrition sources in the world. Used for most food searches.
- **Open Food Facts**[^3] — supplements [USDA](#gloss-usda) for branded and international foods, especially packaged products with a barcode.
- **Canadian Nutrient File** — Health Canada's reference [database](#gloss-database); particularly good amino acid coverage, which helps with [DIAAS](#gloss-diaas) calculations.
- **UK CoFID** (Composition of Foods Integrated Dataset) — ~2,900 UK foods from Public Health England/[DHSC](#gloss-dhsc); strong on macros, minerals, and vitamins, but has no amino acid data of its own.
- **Australian AFCD** (Australian Food Composition Database) — ~1,600 Australian foods from [FSANZ](#gloss-fsanz); also has real amino acid coverage, like Canadian Nutrient File.
- **French [CIQUAL](#gloss-ciqual)** — ~3,480 French/European foods from [ANSES](#gloss-anses) (2025 edition); like CoFID, no amino acid data. 

See [Food data — where it comes from and how it is stored](#food-data) for more on all six of NuMa's sources.

In addition, the following internal data sources are used:

- **Harvard T.H. Chan School of Public Health oxalate table**[^11] — a 433-food reference table used to fill in [oxalate](#gloss-oxalate) content when [Oxalate data](#oxalate) is switched on in Settings. (This is optional and is off by default.)
- **Atkinson/Brand-Miller international glycemic index tables**[^8] — a published reference table of about 2,500 foods, searchable from the Annotate page, so you can pick a published [Glycemic Index](#gi) value for a food rather than finding one and typing it in yourself. A newer edition of over 4,000 foods can be added to your own copy of NuMa in a few minutes — see [Upgrading to the 2021 tables](#gi-editions).
- **NuMa's own curated protein-complement table**[^10] — a built-in list of 25 common protein sources used as a fallback for amino-acid data in complement suggestions, when your own data doesn't cover a gap.
- **Your own data** — foods saved to your [Pantry](#pantry), and [recipes you have analyzed](#recipes-menu-web), are consulted ahead of every other source above.


#### Automated code testing  

<!-- t:26-10-28 -->

*Search terms: quality control, quality assurance, accuracy, reliability, code testing, program testing.*

**Every change to [NuMa](#gloss-numa) has to pass an automated test suite before it can ship.** As of November 2026 that suite holds about 2,500 tests, in about 85 files, covering everything from "does this page load" to "does this protein-quality calculation come out to exactly the right number." They run on every change, on my machine and again on GitHub, and a release can't be built at all unless every one passes.

**The tests come in several kinds:**

- **Exact-answer tests**, the great majority: a known input, and the one right result the program must produce from it.
- **Rule tests**, which don't stop at a few hand-picked examples: they generate hundreds of realistic random inputs and confirm a rule holds for every one, for example that the complete protein a meal provides never comes out higher than the digestible protein it contains.
- **Browser tests**, which open NuMa in a real browser window and click through it the way you would, checking what actually appears on screen. These run weekly.
- **Tests of this manual**: every link inside it has to lead somewhere, and every abbreviation has to be spelled out or linked to the [Glossary](#glossary) in each section where it appears, since you may arrive at any section directly.
- **Install and upgrade tests**, run on the finished program before each release: it's started once as a brand-new install and once on a copy of an existing user's data, and must open every main page without an error and without losing a single food, recipe or meal.

**The tests themselves get tested.** A technique called *mutation testing* plants a small deliberate mistake in the code (a plus swapped for a minus, say) and reruns the tests to see whether any of them notices. If none does, that's a blind spot: a piece of logic nothing is actually watching, which an "all tests passed" report can't reveal. So far this has been done for eight of NuMa's core calculation modules, the protein-quality, glycemic load and nutrient-target math among them, and it has found and closed well over a hundred such gaps, a handful of them real errors that hadn't shown up yet.

**The protein-complement suggestions and the Claude AI fetch and import workflow each have extensive tests of their own**, on top of the above. What each one does is explained in [Protein Complement Suggestions](#comp) through [Two-step combinations](#comb), and in [Fetching missing data with Claude AI](#fetch).

#### Periodic review {: #periodic-review}

<!-- t:26-10-28 -->

*Search terms: maintenance, upkeep, audit, schedule, checkups, manual review, database updates.*

**Automated tests catch a program doing the wrong thing. They can't catch a manual that has quietly fallen behind the program, or a food database that has published a newer edition.** That's the job of a scheduled review, done by hand (with Claude AI's help), on four timescales:

- **Weekly:** everything that changed that week. Does the manual describe each change correctly, and in the places a reader would look for it? Did each change get a test? Do the manual's links, Glossary and search words still fit? Any calculation module whose code changed substantially is flagged for another round of mutation testing.
- **Monthly:** the whole manual is read through against the program as it is now, not just the week's changes, along with the program's own technical documentation.
- **Quarterly:** the three online food sources ([USDA](#gloss-usda), Open Food Facts and the Canadian Nutrient File) checked for changes in how they send their data; the Glossary checked against the whole manual; and the next group of program modules put through mutation testing, so that every part of the program gets that check at least once a year.
- **Annually:** the bundled national food databases (UK, Australia, France) checked for newer editions. The first check, in September 2026, found one: the French database was upgraded to its 2025 edition, adding nearly 300 foods.

*(For technically skilled users: the file-by-file test breakdown, the tools used, the full review procedures, and the mutation-testing log with its results are in README-numa-documentation.md's Test Suite and Maintenance sections.)*

#### Validation you can replicate yourself
<!-- t:26-10-28 -->

*Search terms: check the math, verify, reproduce, proof.*

**A fully worked validation example is in [Worked validation example](#appendix-diaas-validation).** You can do this yourself, if you like. Data are brought in from outside the program and run through the official correct computation process. Full source references are given. You can run the same computation in [NuMa](#gloss-numa) and compare the result.

#### Reasonable expectations: bugs remain
<!-- t:26-10-28 -->

*Search terms: mistakes, wrong results, report a problem.*

**Problems may appear anyway.** As professional programmers will tell you, all programs have bugs. This is more likely for new ones than for those which have been around for years. This is why you should report any result you are getting which doesn't make sense to you. There is a small chance you've found a "bug", but a greater chance that the program simply needs to explain itself to you more clearly. Either problem will be fixed ASAP, and all such fixes benefit everyone who uses the program.

**How to report suspected errors or problems with the program:** see [Getting more help](#feedback).
<!-- t:26-10-28 -->

---

## Appendices {: #appendices}

The glossary, links to outside resources, and ideas for features not yet built.



### A. Glossary {: #glossary}

*Search terms: definitions, acronyms, jargon, what does it mean.*

Abbreviations and key terms used in NuMa output and this manual.

---

**AA**{: #gloss-aa}  —  Amino acid. The molecular building blocks of all proteins. See [essential amino acids](#aa).

**ADA**{: #gloss-ada}  —  American Dietetic Association, now the Academy of Nutrition and Dietetics. Co-author, with Dietitians of Canada, of the omega-3 position paper behind NuMa's suggested EPA/DHA targets. See [Omega-3 Fatty Acids](#omega3).

**AFCD**{: #gloss-afcd}  —  Australian Food Composition Database. ~1,600 Australian foods published by [FSANZ](#gloss-fsanz), one of the bundled datasets NuMa searches; it does carry amino acid data. See [Food data](#food-data).

**AI**{: #gloss-ai}  —  Adequate Intake. A nutrient reference value used when a full RDA cannot be established; considered sufficient for most healthy people. Used for fiber in NuMa. See [RDA](#rda).

**AI (artificial intelligence)**{: #gloss-artificial-intelligence}  —  A computer program that writes and answers in ordinary language. In this manual it means Claude, the AI chat assistant NuMa can prepare questions for, to fetch missing food data or translate a recipe; NuMa itself contains no AI. See [Fetching missing data with Claude AI](#fetch).

**ALA**{: #gloss-ala}  —  Alpha-Linolenic Acid. The plant-based omega-3 fatty acid — found in flaxseed, walnuts, and chia — that NuMa tracks alongside EPA and DHA. See [Omega-3 Fatty Acids](#omega3).

**ANSES**{: #gloss-anses}  —  Agence nationale de sécurité sanitaire de l'alimentation (French food safety agency). Publisher of the [CIQUAL](#gloss-ciqual) food composition table bundled with NuMa.

**Antinutrient**{: #gloss-antinutrient}  —  A naturally occurring plant compound that partially blocks the absorption or use of a nutrient. Common examples: phytates (reduce mineral absorption), oxalates (reduce calcium absorption), lectins (interfere with digestion in raw legumes), bound niacin in corn. All can be reduced by appropriate preparation. See [antinutrients](#antinutrients).

**API**{: #gloss-api}  —  Application Programming Interface. A doorway one program uses to fetch data directly from another over the internet, with nobody clicking anything. NuMa uses [USDA](#gloss-usda) FoodData Central's API to look up foods. See [Food data](#food-data).

**Bioavailable protein**{: #gloss-bioavailable-protein}  —  Protein the body can actually absorb and use, accounting for both digestibility and amino acid completeness. More meaningful than the raw protein figure on a nutrition label.

**CGM**{: #gloss-cgm}  —  Continuous Glucose Monitoring. A wearable device that measures blood glucose every few minutes. Discussed in [Glycemic load (GL) and Blood Glucose Comparison](#appendix-gl-comparison) as the most accurate way to track individual glycemic response.

**CIQUAL**{: #gloss-ciqual}  —  The French food composition table published by [ANSES](#gloss-anses); ~3,480 French and European foods bundled with NuMa. No amino acid data. See [Food data](#food-data).

**Code**{: #gloss-code}  —  The short identifier every food and recipe gets, in one pattern: a few letters saying what kind of item it is, then a number. **U** = USDA FoodData Central food (U171477 — the number is its [FDC ID](#gloss-fdc-id)); **UD** = user-drafted food, one you entered yourself (UD4); **R** = recipe (R21); **OFF**, **CNF**, **CoFID**, **AFCD**, **CIQUAL** = a food from one of the other food databases, numbered 1, 2, 3… in the order you added them (OFF3). A **.1**, **.2** … on the end is an older version of that food, kept for past meals at a Refresh (U171477.1 — see [Keeping the old version](#keep-version)). A food's code never changes, even when you rename or edit it; a small **edited** tag after a code (U175237 `edited`) means you've changed that food's data since it came from its source (it is *user-edited* — see [Custom Food Profiles](#drafted-foods)). The Substitute tool accepts codes typed in either upper or lower case, and so does every search box ([search by code](#search-by-code)). Shown in Code columns, or, where a table has no Code column, in parentheses under a food or recipe name — hover over it to see the kind spelled out. Every table with a Code column has a one-line key under it explaining the letters and the edited tag. See also [ID](#gloss-id).

**CoFID**{: #gloss-cofid}  —  Composition of Foods Integrated Dataset. The UK's national food composition table, ~2,900 foods, published by Public Health England/[DHSC](#gloss-dhsc) and bundled with NuMa. No amino acid data. See [Food data](#food-data).

**Complete protein**{: #gloss-complete-protein}  —  A protein source that supplies all nine essential amino acids at or above FAO reference levels after digestibility adjustment. See [protein completeness](#complete).

**Complement food**{: #gloss-complement-food}  —  A food added to a meal specifically to supply the amino acids that other ingredients are short in. See [complement suggestions](#comp).

**CSV**{: #gloss-csv}  —  Comma-Separated Values. A plain-text spreadsheet format — one line per row, commas between columns — that Excel, Google Sheets, and most spreadsheet programs can open directly. NuMa uses it for exporting and importing Food Cache and recipe data. See [Food Cache](#food-cache-web).

**Database**{: #gloss-database}  —  An organized collection of information, stored so a program can search it and pull out exactly the piece it needs. NuMa works with two kinds. The food databases it looks foods up in: online ones such as [USDA](#gloss-usda) FoodData Central and Open Food Facts, plus the bundled ones that ship with it ([CoFID](#gloss-cofid), [AFCD](#gloss-afcd), [CIQUAL](#gloss-ciqual)). And your own database — a single file on your computer holding your [Food Cache](#gloss-food-cache), pantry, recipes, logged meals and annotations. See [Food data](#food-data).

**Data key**{: #gloss-data-key}  —  The name NuMa uses internally for a nutrient, such as *protein_g* for protein or *iron_mg* for iron: the nutrient's name, then the unit its amounts are stored in (g, mg, mcg). It's how the nutrient is labeled in NuMa's stored data and program code, and it's the column heading you'll see when you export your Food Cache as a [CSV](#gloss-csv) file. You never need to type or know one to use NuMa. Each entry in the [Full Nutrient Key](#nutrient-key) ends with its nutrient's data key.

**DCP**{: #gloss-dcp}  —  Digestible Complete Protein. Grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (all essential amino acids present at adequate levels). See [digestible complete protein](#dcp).

**DHA**{: #gloss-dha}  —  Docosahexaenoic Acid. A marine omega-3 fatty acid — found in fish and seafood — that NuMa tracks alongside ALA and EPA. See [Omega-3 Fatty Acids](#omega3).

**DHSC**{: #gloss-dhsc}  —  Department of Health and Social Care, the UK government department that (with Public Health England) publishes [CoFID](#gloss-cofid), the UK food composition dataset bundled with NuMa.

**DIAAS**{: #gloss-diaas}  —  Digestible Indispensable Amino Acid Score. A score from 0 to 1.5+ measuring how much of a food's protein the body can actually use, accounting for digestibility and amino acid completeness. 1.0 = meets the FAO reference exactly; above 1.0 = excellent; below 1.0 = one or more amino acids are limiting. See [DIAAS](#diaas).

**Digestibility coefficient**{: #gloss-digestibility-coefficient}  —  A number between 0 and 1 representing the fraction of a nutrient that reaches the bloodstream after digestion. NuMa uses true ileal digestibility values from published literature. Eggs and dairy sit near 1.0; whole legumes are typically 0.79–0.85.

**DNA**{: #gloss-dna}  —  Deoxyribonucleic Acid. The molecule in every cell that carries its genetic instructions. Mentioned in the [Full Nutrient Key](#nutrient-key), where several B vitamins are needed to make and repair it.

**DRI**{: #gloss-dri}  —  Dietary Reference Intakes. The system of nutritional reference values published by the U.S. National Academies of Sciences[^9]; the source for RDAs, AIs, and upper intake levels used in NuMa.

**EAA**{: #gloss-eaa}  —  Essential Amino Acid. One of nine amino acids the human body cannot make and must get from food every day: Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine. See [essential amino acids](#aa).

**EAN**{: #gloss-ean}  —  European Article Number, the 13-digit barcode standard used outside North America. Typing one into food search goes straight to an Open Food Facts lookup. See [Setting up a Food or Recipe search](#search-ranking).

**EAR**{: #gloss-ear}  —  Estimated Average Requirement. The intake that meets the needs of the *average* person in a group, with no safety margin — a population-statistics figure, not a personal target. The [RDA](#gloss-rda) is set above it. NuMa does not use the EAR for anything. See [Recommended Dietary Allowances](#rda).

**EFSA**{: #gloss-efsa}  —  European Food Safety Authority. The European Union's food-science agency, whose dietary reference values are the European counterpart of the IOM's; NuMa offers its water goals (2.5 liters a day for men, 2.0 for women) as an alternative to the IOM's, under **Water goals from** in Settings → 1, Your Profile. See [The daily goal](#water-reference).

**EPA**{: #gloss-epa}  —  Eicosapentaenoic Acid. A marine omega-3 fatty acid — found in fish and seafood — that NuMa tracks alongside ALA and DHA. See [Omega-3 Fatty Acids](#omega3).

**FAO**{: #gloss-fao}  —  Food and Agriculture Organization of the United Nations. The body that published the 2013 amino acid reference standard used for all protein quality scoring in NuMa. See [FAO reference values](#fao).

**FDC**{: #gloss-fdc}  —  FoodData Central. The USDA's online nutrition [database](#gloss-database) and NuMa's primary food data source. Each food has a unique numeric FDC ID. Website: https://fdc.nal.usda.gov/

**FDC ID**{: #gloss-fdc-id}  —  The unique numeric identifier assigned to each food entry in USDA FoodData Central. You can enter an FDC ID directly at any "Search food or recipe" prompt instead of typing a name.

**Food Cache**{: #gloss-food-cache}  —  Your local [database](#gloss-database) of previously retrieved foods. Searching the cache is instant (no network required); foods are added automatically when you select them from USDA or Open Food Facts[^3] results.

**Food Annotation**{: #gloss-food-annotation}  —  Extra information you attach to a cached food: glycemic index, a DIAAS estimate, or a preparation note. Stored locally; not part of any online [database](#gloss-database).

**FSANZ**{: #gloss-fsanz}  —  Food Standards Australia New Zealand, the agency publishing the [AFCD](#gloss-afcd) food composition [database](#gloss-database) bundled with NuMa.

**Generic**{: #gloss-generic}  —  In NuMa, a figure that isn't the food's own: a typical value for that *kind* of food, taken from one of NuMa's small built-in tables and used where the food's own record lacks a number a calculation needs. It's a reasonable guess, but a guess, and NuMa labels it wherever it's shown. You'll meet it in two places. A volume amount ("2 T", "1/3 c") for a food with no cup or spoon weight of its own is converted to grams with a [generic density](#gloss-generic-density) and marked **≈ generic**; see [Amounts converted with a generic density](#generic-density), which also says how to replace the guess with the food's real weight. And a complement suggestion tagged "(generic estimate)" is an entry from NuMa's built-in table of common protein sources, not a food you have; see [Amino acid estimates in suggestions](#comp-estimate). Every place NuMa estimates is listed under [Where NuMa fills gaps](#filling-gaps).

**Generic density**{: #gloss-generic-density}  —  A typical weight-per-volume figure for a kind of food (flours, protein powders, seeds and so on) that NuMa uses to turn a cup or spoon amount into grams when the food has no cup or spoon portion of its own. A reasonable guess, but a guess: such amounts are marked **≈ [generic](#gloss-generic)**. See [Amounts converted with a generic density](#generic-density).

**GI**{: #gloss-gi}  —  Glycemic Index. A scale from 0 to 100 measuring how quickly a food raises blood glucose relative to pure glucose (100). See [glycemic index](#gi).

**GL**{: #gloss-gl}  —  Glycemic Load. A measure of glycemic impact that combines GI with the actual amount of carbohydrate in a serving. More useful than GI alone for real-world meal comparisons. See [glycemic load](#gl).

**GUI**{: #gloss-gui}  —  Graphical User Interface. A visual, point-and-click interface — this is what NuMa provides (see [Part 4 — Menu by menu](#part-3-using-numa)).

**IAA**{: #gloss-iaa}  —  Indispensable Amino Acid. The FAO's own term for what this manual calls [EAA](#gloss-eaa) (Essential Amino Acid) — both refer to the same nine amino acids. See [essential amino acids](#aa).

**ID**{: #gloss-id}  —  Identifier. A number that refers to exactly one thing — one food, recipe, or meal — and never changes, even when you rename that thing. NuMa shows IDs in list columns and page titles so you can tell two similarly-named items apart. Foods and recipes show theirs as a [code](#gloss-code) (U171477, UD4, R21, OFF3). See also [FDC ID](#gloss-fdc-id).

**Ileal digestibility**{: #gloss-ileal-digestibility}  —  The fraction of an amino acid absorbed by the end of the small intestine (ileum). DIAAS uses true ileal digestibility, which is more accurate than fecal digestibility for measuring protein available to the body.

**IOM**{: #gloss-iom}  —  Institute of Medicine. The US body whose 2005 report set the Dietary Reference Intakes NuMa uses, including the 0.8 g/kg protein figure; renamed the National Academy of Medicine in 2015. See [The protein target assumes high-quality protein](#protein-rda-quality).

**ISO**{: #gloss-iso}  —  International Organization for Standardization. The independent international body that publishes agreed standards for how things are measured, tested and made. In NuMa it matters for one standard, ISO 26642:2010, which sets out how a [GI](#gloss-gi) study must be run: how much carbohydrate the test portion contains, how many people are tested, and when blood is sampled. Rows in the GI reference tables from studies that deviated from it are flagged **non-ISO method** — a warning about the evidence, not the food. See [Method quality, and why some rows are flagged](#gi-method-quality).

**ISSN**{: #gloss-issn}  —  International Society of Sports Nutrition. A professional society of sports-nutrition researchers whose published position stands summarize the evidence on protein intake and timing for people who exercise. NuMa uses its per-meal protein and timing figures — see [Protein per meal](#protein-per-meal) and [When to eat protein](#protein-timing).

**IU**{: #gloss-iu}  —  International Units. A dosage measurement used for vitamins A, D, and E on supplement labels. On a [custom food profile](#custom-foods), you can type these vitamins' amounts directly in IU and NuMa converts them automatically.

**LDL**{: #gloss-ldl}  —  Low-Density Lipoprotein. The particle that carries cholesterol in the blood; high levels of this "LDL cholesterol" are linked to heart disease. Mentioned in the [Full Nutrient Key](#nutrient-key).

**Limiting amino acid**{: #gloss-limiting-amino-acid}  —  The essential amino acid in shortest supply relative to the FAO reference, which caps how much of a food's protein can be incorporated into tissue. The overall DIAAS score equals the ratio for the limiting amino acid. See [limiting amino acid](#gap).

**Met+Cys**{: #gloss-met-cys}  —  Methionine + Cystine. These two amino acids are scored as a combined pair in DIAAS calculations, following FAO 2013 guidelines, because the body can convert Methionine into Cystine.

**My Pantry**{: #gloss-my-pantry}  —  A personal list of protein sources you currently have on hand. NuMa checks this list first when suggesting complement foods, so suggestions reflect what you can actually use.

**NIH**{: #gloss-nih}  —  National Institutes of Health. The US government medical research agency; its Office of Dietary Supplements ([ODS](#gloss-ods)) publishes the nutrient fact sheets most of NuMa's [RDA](#gloss-rda) figures come from.

**NS**{: #gloss-ns}  —  Not specified. In glycemic index reference rows, marks a detail the original published study did not record — a bean variety, say. See [How to read a lookup result](#gi-result-row).

**NuMa**{: #gloss-numa}  —  NutriMagnus. The abbreviated name used throughout this manual.

**ODS**{: #gloss-ods}  —  Office of Dietary Supplements, part of the [NIH](#gloss-nih). The direct source for most [RDA](#gloss-rda) and Adequate Intake values in NuMa. See [Recommended Dietary Allowances](#rda).

**OFF**{: #gloss-off}  —  Open Food Facts. A community-maintained [database](#gloss-database) of packaged and branded food products; NuMa's secondary data source. Website: https://world.openfoodfacts.org/ 

**Oxalate**{: #gloss-oxalate}  —  A naturally occurring compound (oxalic acid / oxalate ion) found in many plant foods, especially spinach, beets, nuts, and chocolate. At high dietary levels it can promote calcium-oxalate kidney stones in susceptible individuals. NuMa can optionally display oxalate content using the Harvard T.H. Chan School of Public Health reference table. Enable it under Settings → Oxalate data. See [oxalate data](#oxalate).

**PDCAAS**{: #gloss-pdcaas}  —  Protein Digestibility-Corrected Amino Acid Score. The older protein-quality score (FAO/WHO, 1991) that [DIAAS](#gloss-diaas) replaced. It scales a food's most limiting amino acid by how well its protein *as a whole* is digested, measured over the whole gut, and cuts every score off at 1.0, so it can't tell a good protein from an excellent one. In 2013 the FAO recommended DIAAS instead, which measures how well *each* amino acid is digested by the end of the small intestine, and isn't cut off. NuMa uses DIAAS throughout; a PDCAAS figure in a food's notes came from that food's source, and doesn't convert one-to-one into a DIAAS. See [DIAAS](#diaas).

**PDF**{: #gloss-pdf}  —  Portable Document Format. A file that keeps its exact page layout wherever it is opened or printed. Every printable page in NuMa can be saved as one through your browser's own Print dialog.

**Phe+Tyr**{: #gloss-phe-tyr}  —  Phenylalanine + Tyrosine. Scored as a combined pair in DIAAS calculations because the body can convert Phenylalanine into Tyrosine.

**Phytonutrients**{: #gloss-phytonutrients}  —  Plant-derived bioactive compounds tracked by NuMa where USDA data exists: beta-carotene, alpha-carotene, lycopene, lutein/zeaxanthin, choline, beta-sitosterol, and isoflavones.

**PNG**{: #gloss-png}  —  Portable Network Graphics. An image file made of a fixed grid of dots, so it blurs if enlarged a lot. The friendlier of the two plot download formats — it opens anywhere. See [Plot File Formats](#plot-file-formats).

**Pooled DIAAS**{: #gloss-pooled-diaas}  —  The meal-level protein quality score computed by summing digestible amino acids across all ingredients before scoring. This captures how foods complement each other in a way that single-food DIAAS cannot. See the section [How NuMa scores meal and recipe protein quality](#protein-scoring).

**PROT-AGE**{: #gloss-prot-age}  —  The PROT-AGE Study Group: an international group of experts in geriatrics and nutrition whose 2013 position paper set out protein recommendations for people over 65 — at least 1.0–1.2 g per kg of body weight a day, and a higher amount per meal than younger adults need. NuMa uses its per-meal figure for profiles aged 65 and over. See [Protein per meal](#protein-per-meal).

**RDA**{: #gloss-rda}  —  Recommended Dietary Allowance. The average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group. See [RDA](#rda).

**Reference value**{: #gloss-reference-value}  —  Short for [FAO](#gloss-fao) reference value: how many mg of one specific essential amino acid a person needs per gram of dietary protein, established independently for each of the nine [EAAs](#gloss-eaa). Dividing a food's own mg-of-that-amino-acid-per-gram-of-protein by its reference value produces that amino acid's [DIAAS](#gloss-diaas)-basis score. See [FAO reference values](#fao).

**Standard error**{: #gloss-standard-error}  —  A measure of how much the individual people in a study disagreed with each other, reported alongside an average as "±3" or "±15". A small figure means their results clustered tightly around the average, so that average is a dependable estimate; a large one means they scattered widely, so the average is shaky and could easily have come out differently with a different handful of subjects. It is written **SEM** in the published glycemic index tables (standard error of the mean). See [How to read a lookup result](#gi-result-row).

**SR**{: #gloss-sr}  —  Standard Reference, as in "SR Legacy" — the [USDA](#gloss-usda)'s pre-2019 food composition [database](#gloss-database). Along with Foundation foods, it is the [USDA](#gloss-usda) data type most likely to carry a full amino acid profile. See [Food data](#food-data).

**Sub-recipe**{: #gloss-sub-recipe}  —  A saved recipe used as one ingredient of another recipe — a sauce inside a pasta dish, a spice blend inside a stew. Its amount is given in servings, not grams, and its nutrients are worked out from its own ingredients and folded into the parent, however many levels deep the nesting goes. See [Recipes: Servings Instead of `pN`](#portions-vs-servings) for how a serving's weight is derived.

**SPI**{: #gloss-spi}  —  Soy Protein Isolate. A concentrated plant protein (95%+ protein by weight) with high digestibility (0.95); frequently cited in complement suggestions. See [Why some foods appear only in DIAAS-boosting suggestions](#comp-appendix).

**SVG**{: #gloss-svg}  —  Scalable Vector Graphics. An image file stored as shapes rather than dots, so it stays perfectly sharp at any size. The better choice for printing a plot large. See [Plot File Formats](#plot-file-formats).

**TID**{: #gloss-tid}  —  True Ileal Digestibility. NuMa's abbreviation for [ileal digestibility](#gloss-ileal-digestibility), used as a column heading in per-ingredient digestibility breakdowns.

**UL**{: #gloss-ul}  —  Tolerable Upper Intake Level. The highest daily intake of a nutrient unlikely to cause harm — NuMa applies built-in ULs for twelve nutrients with a real risk of excess, shown as a column on every nutrient analysis table. See [Maximum Nutrient Limits](#maxlimits).

**UPC**{: #gloss-upc}  —  Universal Product Code, the 12-digit barcode standard used in North America. Typing one into food search goes straight to an Open Food Facts lookup. See [Setting up a Food or Recipe search](#search-ranking).

**USDA**{: #gloss-usda}  —  United States Department of Agriculture. The U.S. government body that publishes FoodData Central, NuMa's primary food data source.

**User-edited**{: #gloss-user-edited}  —  A food whose data you've changed since it came from its source — shown as an **edited** tag after its [code](#gloss-code), and in its type ("SR Legacy · user-edited"). NuMa remembers which values you changed, and a Refresh keeps them unless you choose otherwise. See [Food data](#food-data).

**usr**{: #gloss-usr}  —  User-drafted. Older name for what is now the **UD** prefix of a [code](#gloss-code) (UD4): a food whose nutrient profile you created or edited by hand, rather than one retrieved from USDA or Open Food Facts[^3] — this is what the [Custom Food Profiles](#drafted-foods) list shows.

**What-if**{: #gloss-what-if}  —  NuMa's Analysis pages for trying a change before making it: remove, add, replace or scale a food across a set of meals or recipes and see the nutrition before and after, with nothing saved unless you apply it. See [What-if: Meals](#whatif) and [What-if: Recipes](#whatif-recipes).

**WHO**{: #gloss-who}  —  World Health Organization. The United Nations health agency; co-publisher, with the [FAO](#gloss-fao), of the protein and amino acid requirement guidance NuMa's protein quality scoring follows.

### B. Internet resources {: #internet-resources}

*Search terms: websites, links, outside resources, reading list.*

Examine.com. (n.d.). Examine—Independent analysis of nutrition and supplement research. Retrieved August 2, 2026, from https://examine.com

> Independent, citation-linked summaries of supplement and nutrient research—a good sanity check when a nutrient shows up as low or high in your analysis and you want to know what the science actually says about it. It offers nutrition data, recommendations, safety recommendations, and much, much more.

Food and Agriculture Organization of the United Nations. (2013). Dietary protein quality evaluation in human nutrition: Report of an [FAO](#gloss-fao) expert consultation. Retrieved August 2, 2026, from https://www.fao.org/3/i3124e/i3124e.pdf

> The original FAO report defining Digestible Indispensable Amino Acid Score (DIAAS) methodology; the primary source behind NuMa's protein-quality calculations.

Linus Pauling Institute. (n.d.). Micronutrient Information Center. Oregon State University. Retrieved August 2, 2026, from https://lpi.oregonstate.edu/mic

> Deep-dive, peer-reviewed summaries of individual vitamins, minerals, and phytonutrients—deficiency symptoms, toxicity thresholds, and disease-prevention evidence that goes well beyond what a nutrient table can show.

National Institutes of Health Office of Dietary Supplements. (n.d.). Office of Dietary Supplements—Nutrient Recommendations and Databases. Retrieved August 2, 2026, from https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

> This extraordinary resource is the fundamental data source for nutrition data used by NutriMagnus.

Open Food Facts. (n.d.). Open Food Facts—World food products database. Retrieved August 2, 2026, from https://world.openfoodfacts.org

> The crowd-sourced packaged-food [database](#gloss-database) NuMa already queries for barcode lookups; browsing it directly lets you see ingredient lists, Nutri-Score, and photos that NuMa doesn't surface.

University of Sydney. (n.d.). Glycemic Index Database. Retrieved August 2, 2026, from https://glycemicindex.com

> The original research [database](#gloss-database) behind glycemic index and glycemic load values; useful for looking up [GI](#gloss-gi) numbers for foods not yet annotated in NuMa.

### C. Ideas for future features {: #future-features}


Ideas below are listed in their current likely probability of being implemented. User feedback has a major effect on these probabilities!

---

#### Expanding Revised Optimal (Recent Research) targets {: #expand-revised-optimal}

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

☑ **Age/sex-banded [RDA](#gloss-rda) (completed, existing feature)** and ☑ **research-backed maximum nutrient levels (completed 2026-08-11)** are both done — see [Daily Nutrient Goals](#goals) for the full RDA age/sex band table and [Maximum Nutrient Limits](#maxlimits) for all 12 built-in Tolerable Upper Intake Levels, each sourced to the [NIH](#gloss-nih) DRI tables[^9].

☒ **Assessed 2026-10-14, not added.** The [Revised Optimal (Recent Research)](#optimal) tier — the *above-RDA* targets, as distinct from the RDA itself — has built-in defaults for three nutrients: vitamin D[^12], [EPA](#gloss-epa) and [DHA](#gloss-dha)[^13]. Three more were candidates. The test for each was the one those three were held to: an expert body's statement or a research consensus, a specific number, and a citation able to stand next to the [DRI](#gloss-dri)-sourced RDA and [UL](#gloss-ul) figures. None of the three passed:

- **Magnesium — not added.** The best evidence for an intake above the RDA in older adults is for sleep: a 2021 meta-analysis pooled three small trials, 151 people in all, and judged the evidence low to very low in quality, "substandard for physicians to make well-informed recommendations"[^96]. Those trials compared magnesium with a placebo, not one intake with another, so there is no number above the RDA to defend.
- **Vitamin K2 — not added, and NuMa couldn't track it anyway.** A Cochrane review found a single small trial, too little to judge whether vitamin K prevents heart disease[^97]. A 2021 review found that the claim of a benefit unique to K2 "is not supported by the results of the limited number of intervention trials conducted to date"[^98]. And [USDA](#gloss-usda) reports only one form of K2 (menaquinone-4), not menaquinone-7, the form in natto and most K2 supplements, so a K2 target would have nothing reliable to measure against. The assessment also turned up a NuMa bug: vitamin K had been read from that menaquinone-4 figure rather than vitamin K1, now [corrected](#vitamin-k-fix).
- **Choline — not added.** The real problem is falling short of the existing [AI](#gloss-ai), not a missing target above it: only about 8% of US adults reach the AI[^99]. Observational studies link adequate choline with better thinking and memory in older people, but there are no intervention studies in older people[^100]. NuMa's choline goal is already the AI, so its shortfall already shows.

**One existing default changed.** The vitamin D default (50 mcg) came from the Endocrine Society's 2011 guideline[^12]. Its 2024 guideline, which replaces it, takes the opposite view for most adults: it suggests *against* vitamin D supplements above the [IOM](#gloss-iom)'s reference intakes for healthy adults under 75, and suggests more only for people 75 and older, pregnant people, children and adolescents, and adults at high risk of diabetes[^101]. NuMa now follows it (14 October 2026): no vitamin D default under 75, and 23 mcg from 75 — see [Revised Optimal targets](#optimal) for where that figure comes from. 

☒ **Suggested optimum nutrition profiles by age group — retired 2026-10-14.** The idea was a few pre-built bundles of Revised Optimal settings, one per life stage ("Adults 65+ bone health," "Endurance athlete"), to load all at once. It depended on the work above producing enough above-RDA targets to make a bundle different from the [RDA](#gloss-rda) itself, and it produced none. With vitamin D now above the RDA only from age 75, a bundle would differ from the RDA by EPA and DHA alone, and the age differences that matter are already built into the RDA's own age and sex bands. 

#### Source citations for major assertions in the manual {: #citations-progress}

This is basic. Claims must be backed up, and source citations are how it's done. NuMa is designed around nutrition research findings, and at first, to move quickly, many of them went unreferenced. That is now being worked through, area by area; this list tracks where things stand (last reviewed 2026-10-14).

**☑ Sourced** — each with footnotes giving the source and what it does and doesn't support: 

- Daily targets and upper limits ([RDA](#rda), [Maximum Nutrient Limits](#maxlimits)) — the [NIH](#gloss-nih) Dietary Reference Intake tables.
- [Revised Optimal](#optimal) defaults for vitamin D, [EPA](#gloss-epa) and [DHA](#gloss-dha).
- [Diet-aware notes](#diet-bioavailability) on iron, zinc and B12.
- The [FAO 2013 reference values](#fao-reference-values), and the definitions of [DIAAS](#diaas) and [complete protein](#complete) that rest on them.
- [Digestible complete protein](#dcp).
- The [glycemic index tables](#gi) and their subject populations, the [definition of glycemic load](#gl), and [choosing a daily GL target](#gl-target-choose).
- [Protein per meal](#protein-per-meal) and [when to eat protein](#protein-timing).
- [Essential amino acids](#aa) — the nine essential amino acids, and the Met+Cys and Phe+Tyr pairings.
- [Protein complement suggestions](#comp) — the "lowest ratio" definition, the FAO quality band, soy protein isolate's digestibility, and complements not needing to share a meal.
- [Omega-3 fatty acids](#omega3) — the Adequate Intakes, and how poorly [ALA](#gloss-ala) converts to [EPA](#gloss-epa) and [DHA](#gloss-dha).
- [Glycemic load](#gl) caveats — fat, protein, fiber and acid blunting the blood-glucose response of a mixed meal, and the evidence for and against predicting a meal's response from table values.
- [Antinutrients](#antinutrients) — phytate's mineral binding and its reduction by soaking, sprouting and sourdough; vitamin C against phytate; spinach's calcium; raw kidney beans and how long to boil them; trypsin inhibitors; bound niacin and nixtamalization (sourced 2026-10-14, and corrected where the sources disagreed: sourdough's reduction, the bean boiling time, and phytate not being a plant defense).
- [Oxalate data](#oxalate) — the Harvard table itself, and the 40–50 mg a day figure for people who form kidney stones (2026-10-14). The five oxalate bands are labeled as NuMa's own cut-offs.
- The [protein-quality primer](#appendix-protein-quality), [Plant protein sources](#appendix-plant-proteins) and [GL and blood glucose](#appendix-gl-comparison) sections — checked claim by claim 2026-10-14. The primer's cocoa example had used older reference values, which made cocoa look complete when it falls just short; its chia figures were out of date. The plant-protein section's amino acid notes for each food are now checked against that food's [USDA](#gloss-usda) record, which corrected almonds, cashews, pecans, walnuts, peanuts and tofu. The blood-glucose section's points on glucose-response variation, prediction apps and carbohydrate counting are sourced.

**☐ Still to source** — research claims stated without a reference: none known at the last review. New sections are checked as they're written.

**☐ NuMa's own choices, to be labeled as such** — these are design decisions, not research findings, so the fix is to say so plainly where they're described rather than to cite anything:

- The 0.95 "near-adequate" floor below which a complement is suggested ([Amino Acid Gaps](#gap)).
- The absorbed-protein ceiling on [DCP](#dcp-cap).
- The default digestibility used when a food has no measured value.
- The 1 g floors below which a food's missing amino acid data, or missing [GI](#gloss-gi), is ignored.

#### Antinutrient notes with amounts {: #antinutrient-amounts}

*Search terms: phytate amounts, quantified antinutrients, future feature.*

☐ **Proposed 2026-10-14, not started.** NuMa's [antinutrient](#antinutrients) notes say only *whether* a food carries phytate, oxalate or lectins, not how much. A pinch of sesame gets the same note as a bowl of lentils. Absorption researchers judge phytate's effect on zinc and iron by its ratio to the mineral in the same meal, so a quantified version would show, for a meal or recipe, whether that ratio is high enough to matter.

Why it waits: it needs phytate figures for each food, and [USDA](#gloss-usda) has none. They exist in published tables, but those would have to be found, checked against each other, matched to NuMa's foods, and licensed for use — a separate dataset, like the oxalate table. The thresholds that turn a ratio into "this matters" would also need their own sources. Until then, the notes stay qualitative, and the oxalate table remains the one antinutrient NuMa can quantify.

#### What else? Well, know this...

##### Your ideas shape what gets built next {: #feature-ideas}

*Search terms: feature request, suggestion, wish list.*

NuMa is an evolving tool, still actively being built out. This part exists to invite you into that process: if there's something NuMa doesn't do yet that would make it more useful to you, we want to hear about it.

No idea is too small, too ambitious, or too specific to your own situation. A feature that seems minor to you may turn out to matter to a lot of other users too — and one that seems highly personal often points to a real gap in the program. Several of NuMa's existing features started out as exactly this: one user's request.

##### How to contribute an idea

*Search terms: send idea, contact, suggest a feature.*

Use the same channel as [reporting a problem](#feedback):

1. **Text Tom at 435-272-3332** with a brief description of what you'd like NuMa to do, and why it would help you. He will generally call you back to get the full picture.
2. **Or email** [tomcloydmsma@gmail.com](mailto:tomcloydmsma@gmail.com), especially for a longer or more detailed idea — a screenshot or example is welcome if it helps explain what you have in mind. If you email, also send a text, since email isn't checked daily and a good idea shouldn't get lost in it.

There's no such thing as a request that's not worth mentioning. If you're not sure whether NuMa can already do what you want, ask anyway — the answer might be a feature you hadn't found yet, or it might be a real gap worth filling.

## What's new {: #updates-log}

<!-- Release summaries only. The dated, detailed entries (with their hidden Scope blocks) live in docs/updates-log-details.md since the 2026-11-14 reorganization. create_release.py still reads this section: only the Version overview's SUMMARY paragraph (between the marker below and the nearest "#### Release ... summary" heading) becomes that release's GitHub notes, followed by a pointer to this section, so keep the SUMMARY brief; and the running "#### Next release summary to this point" heading is renamed in place to "#### Release <tag> summary". Each user-facing change gets one numbered bullet under the running heading here, plus its dated entry in docs/updates-log-details.md. Rules: docs/claude/changelog.md. -->

*Search terms: release notes, new version, version history.*

What changed in each release of NuMa, newest first, one line per change. The newest release that hasn't shipped yet is at the top, under **Next release summary to this point**.

<!-- Insert new updates below here -->

#### Next release summary to this point

Version overview: 

SUMMARY: Each food's data problems, and their fixes, are now in one place; smarter searches; checkboxes for "complete" added to lists and searches, and for "drinks" in the Recipes list and in searches; Compare keeps your picks across searches; a shorter, reorganized manual with a Return button; recipe Edit can report what each ingredient change does to the recipe's nutrients; filling in a food's missing data has clear steps, ending with Claude AI; What-if removes a recipe logged as individual ingredients even after you changed it for that meal; Alt+Shift+K lists every page and shortcut; Alt+Shift+G, then a recipe's or meal's ID and Enter, opens it from its list; NuMa's window shows its icon in Alt+Tab again; the Food Cache keeps your Fetch ticks and delete warnings when you leave and click back; replacing a food across meals or recipes always says whether it worked; a new Archived page (Foods → 10) finds archived foods and recipes with missing nutrient data; a meal's Items can be viewed as logged, as foods (recipes broken down), or with each recipe kept whole; Ctrl+click on a Contents sidebar or in the manual explains the browser tab before it opens; Foods → 9's lists, the Food Cache and My Pantry can start with the foods you eat most; any food can carry your own notes, kept through a Refresh, and pantry notes can be changed; a recipe you have made can go in My Pantry, so protein complement suggestions treat it as on hand; What-if: Recipes finds recipes by name and lists their ingredients to pick from; an addition to a meal can be changed or undone straight away, and every Items view can edit and remove items; Alt+Shift+U goes to a page's Nutritional Analysis; Settings has a Contents sidebar, and a new Daily Starting Items section adds the foods and recipes you have every day to each day's first meal; the Home page's data-check link opens Foods → 9 on just the new problems; Edit Recipe explains what changing servings or yield weight affects, and a recipe whose serving weight changed can be settled in every meal and recipe at once, with Daily Summary flagging the meals affected.

DETAILS:

* New **Problems by food** page (Foods → 9), and an **Everything to check on this food** box on each food's page: all of a food's data problems in one place, with their fixes.
* Searches no longer put partial matches from your own data above full matches when you already have an item matching every word.
* Singular and plural search words match each other.
* A food can be deleted from its own page.
* Each meal item now records and shows the time of day it was entered.
* Recipes can be marked complete or as drinks, and foods as drinks, straight from the Recipes list and every search.
* Arrow keys move through search results, and Back returns to the one you opened.
* Print pages and other NuMa links stay in NuMa's own window.
* Quiet buttons are blue.
* The manual's search opens the section you picked, with your words highlighted.
* Compare ticks are kept as you search again or move between lists, so one comparison can gather foods from several searches.
* A `!` before a search word leaves out results with that word (`beans red !kidney cooked`), and the list says how many results it hid.
* A `!` word works in list filter boxes too (Recipes, Food Cache, My Pantry, Search meal history and the rest).
* A search for a cooked food no longer misses canned products online.
* A hint under every search box sums up how to write a search.
* NuMa offers to search USDA again with your words reversed, which finds many branded products.
* On the Annotate page, each estimate being asked for has its own **Skip** button beside it.
* The Meals & Log list's **Complete** column is a checkbox, so a meal can be marked complete without opening it.
* On a meal, the Add Food or Recipe header, search box and search hint line up along the top, and the hint's **Learn more** opens the manual at word order.
* Removing an item from a meal no longer makes the page jump around.
* The User Manual is reorganized and much shorter, with step-by-step workflows.
* A **Return** button above the manual (Alt+Shift+U) goes straight back to the page you came from, and **Manual** reopens it where you left off.
* Settings checks a USDA API key with USDA before saving it, with a **Test key** button.
* The Daily Summary page now says it covers several days and drops its date box and Today's summary button; a day opens from its date in the table.
* Daily Summary buttons now say what they show: **Nutrient averages over a period** (the last 7, 14 or 30 days, any dates, or chosen meals; this replaces the separate Nutrient totals button, which opened the same page) and **Week-by-week averages** (was Blocks of days).
* The date-range buttons read **Average these dates** and **Average these meals**, and each block's link is **All nutrients** (was Full nutrient totals).
* On a recipe's Edit page, adding, removing or changing the amount of an ingredient offers a short report on how the recipe's nutrients per serving moved since the last report (nutrient groups you pick, all nutrients, or only those that changed by 5% or more), shown by a button above Add Ingredient; food and recipe names there open in a panel over the page.
* The Recipes list's filter keeps only recipes whose names hold every word you type, like the other list filters.
* Edit Recipe has a Contents list down the side and a **Clear search** button after Search; its search results show each recipe's DCP per serving and description.
* A food's Edit page ends with an **Ask Claude AI for help** box, which writes a prompt for one nutrient group or the whole profile, for missing values only or for every value.
* The *No amino acid data* box on a food's page lists its three fixes in order, ending with **Write a prompt for Claude AI**, and the manual's new Workflow 12 gives the order to try them.
* A recipe added to a meal as individual ingredients marks each of those foods with the recipe, so **What-if: meals** can remove it or change its amount even after it was changed for that meal; where a change can't reach such foods, What-if and its Apply page name the meals to fix by hand.
* **Alt+Shift+K** (or Ctrl+K) opens a command palette: every menu page and this page's own shortcuts, each with its keys, filtered as you type, plus searches for the typed text and Quit. Settings' Keyboard Shortcuts section moves to **Alt+Shift+E**.
* A page that reloads after a change below its search results keeps your place even when the online results arrive late.
* On the Recipes list, Meals & Log and Search meal history, pressing Alt+Shift+G, typing a row's ID (21 for R21) and pressing Enter opens that recipe or meal; a box shows what the digits match.
* NuMa's own window now runs as a separate browser process with its own profile, so KDE shows it in Alt+Tab with its own icon even while an ordinary Chromium window is open, and your browser's extensions (and their keyboard shortcuts) no longer reach it.
* On the Food Cache, Fetch ticks and "Deletion not possible" warnings are kept when you leave the page and click your way back (a keyboard shortcut back starts it fresh); each warning is checked again, so it shows what uses the food now, and goes once nothing does.
* On both Food Use pages, a replace, remove or add always reports what happened, in a colored box the page opens at: what was changed and in how many meals or recipes, or that nothing was and why. After a mistake, the codes you typed are still there to correct.
* When you add a recipe to a meal, the hint under its Amount box says what one serving weighs ("1 serving = 24 g"), even with no serving description.
* The Food Cache and My Pantry lists have an Other nutrients column, complete or incomplete, covering macronutrients, water, minerals, vitamins and the amino acids DCP needs; the Used in counts and longer button labels there now take two lines.
* New **Archived foods & recipes** page (Foods → 10, key 0; also Recipes → 3) lists only archived items, foods with the Food Cache's columns and recipes judged by their ingredient foods, incomplete-and-used first, since meals logged with them still count in long-run averages but Foods → 9 skips them; **Incomplete first** is also a Food Cache sort.
* On a meal's page, Items has a **View** menu beside **Sort by**: **As logged** (the list as before), **Foods** (every food eaten, recipes and recipes inside them broken down, a food reached more than once shown as one row with where it came from) and **Foods & recipes** (each recipe kept whole, a recipe added as individual ingredients gathered back into one row); the choice is remembered.
* In NuMa's own window, a Ctrl+click or middle-click on a page's Contents sidebar entry (a link to part of the same page, which opens a second copy in a tab) now explains the tab before it opens, as does one on a link in the User Manual, its contents included, where the tab opens the manual at that section.
* On Foods → 9, every list of foods starts with the foods in the most meals over the last 90 days (on their own or in a recipe), with that count beside each name; an **Order every list of foods** menu at the top switches them all to alphabetical, and is remembered.
* The Food Cache's and My Pantry's **Sort by** menus gain **Most meals, last 90 days**, the same order, now their default (a sort already chosen is kept), with the 90-day count under Used in.
* Every food's page has a **Notes** section where you can add your own notes on the food (a custom food's box edits its existing notes); they are kept apart from the source's notes, so a Refresh from USDA never overwrites them, show in the Food Cache's Notes and on the printout, and merging duplicates keeps both foods' notes.
* A pantry entry's note can now be changed from the Pantry list.
* **Compare checked foods with this one** (Fill in nutrients from another food, a custom food's Edit values) turns blue once a food is ticked. Every Compare button keeps your ticks after comparing, so coming back finds them still ticked; Clear all picks clears them.
* A batch of a recipe you have made can now go in My Pantry: **Add to pantry** on My Pantry's search results (which now find your recipes too), the **In My Pantry** box on the recipe's page, or the Recipes list's new **Pantry** column. It is listed under **Recipes on hand** on My Pantry, with **Remove from pantry** for when the batch is used up.
* Protein complement suggestions now offer only the recipes in your pantry under **From your pantry** (renamed from From your pantry & recipes); your other recipes move to **Other options**, as things you could make, and archived recipes are no longer suggested.
* **What-if: Recipes** can choose its recipes **By name** (the recipes whose names hold every word typed, listed as you type), and for **Remove** and **Change amount** its food/recipe box lists every food and sub-recipe in the chosen recipes, most used first, to pick from; **Add** and **Replace** still search all your foods and recipes.
* Right after you add something to a meal, the green **Added …** line has **Edit** and **Undo** buttons: **Edit** changes its amount (for a recipe added as individual ingredients, their total, each scaled to keep their proportions), and **Undo** takes it back out, all of it, with a green line saying what was removed.
* A meal's **Foods** and **Foods & recipes** views of Items now have **Edit** and remove buttons too: in Foods & recipes they work on the row (a recipe logged as individual ingredients: a new total, a weight or servings, or all of them removed); in Foods they change what you logged of a food yourself, while a food inside a recipe logged whole says "in a recipe" and changes only with the recipe.
* **Alt+Shift+U** on a meal, a recipe or a food page clicks **Nutritional Analysis** in the Contents sidebar, going to that section (opening it first on a food page, if collapsed).
* Settings has a **Contents** sidebar listing its sections; clicking one opens it and goes to it.
* New **Settings → 10. Daily Starting Items** (Alt+Shift+0), after Water Tracking; the sections after it move down one, and Meals & Log columns, now 11, is Alt+Shift+L; Keyboard Shortcuts moves to 15, just before System Issues: foods and recipe portions, each given as a code and an amount, that NuMa adds to the first meal created on a date with no meals yet. Its **Find a code** box searches foods or recipes by name, and **Use** puts a match's code in the first empty row. The meal page names them, with an **Undo** for all of them, and names any that could no longer be added. A code or amount that can't be used refuses the save, with the reason and what was typed kept.
* When the Home page reports new data problems, **Review them** opens Foods → 9 at a **New since your last check** box listing just those problems, each with its food (or meal or recipe item), what's wrong and a link to its place in the lists; fixed ones are marked **fixed ✓**, and **Done with these** clears the box.
* Edit Recipe has a link under Number of servings and Total yield weight to a new manual section on what changing each affects: the number of servings changes the nutrients in a serving; the total yield weight changes only what a serving weighs (and water, if the recipe has a cooked water figure), with meals keeping their nutrients until you choose on each meal page.
* When a recipe's serving weight changes, its page and Edit Recipe show **Review them**: a list of every meal item and recipe ingredient entered at the old weight, each with **Keep the grams** or **Keep the servings** (or one choice for every row), applied at once. A meal page's yellow note links there. **Daily Summary** lists every affected meal, on any date, with **Settle**, and marks affected days with ⚠. Recipes used as ingredients now record their serving weight too, and saving a recipe records the old weight first on any use without one.

- **57.** MANUAL: Daily Summary's section now explains its box of meals logged at a recipe's old serving weight, and more everyday words (*leftovers*, *undo*, *my notes*, *error*) find the right sections in the manual's search. [learn more...](#daily-summary)
- **56.** When a recipe's serving weight changes, **Review them** on its page lists every meal and recipe that used the old weight, to keep the grams or the servings for each, all at once; Daily Summary lists every meal affected, with ⚠ beside its day. [learn more...](#servings-yield-effects)
- **55.** On Edit Recipe, a link under **Number of servings** and **Total yield weight** explains what changing each affects: servings change the nutrients in a serving; total weight changes only what a serving weighs, and your meals keep their nutrients until you choose. [learn more...](#servings-yield-effects)
- **54.** The Home page's **Review them** opens Foods → 9 at a list of just the new data problems, each linked to its food and its place in the full lists, kept until you click **Done with these**. [learn more...](#new-problems)
- **53.** Settings has a **Contents** sidebar listing all its sections, and a new section, **10. Daily Starting Items**: foods and recipes NuMa adds to the first meal of each new day, such as a daily vitamin, with a **Find a code** search for foods and recipes right there. The sections after it move down one; Meals & Log columns, now 11, is Alt+Shift+L; Keyboard Shortcuts moves to 15, just before System Issues. [learn more...](#daily-start)
- **52.** `Alt+Shift+U` on a meal, a recipe or a food page goes to its Nutritional Analysis section, as clicking that entry in the Contents sidebar does. [learn more...](#web-shortcuts)
- **51.** On a meal, the green **Added …** line has **Edit** and **Undo** buttons, to change or take back what you just added (a recipe added as individual ingredients, all together), and the **Foods** and **Foods & recipes** views of Items now have **Edit** and **✕** too, not only **As logged**. [learn more...](#meal-undo-add)
- **50.** What-if: Recipes can choose recipes **By name** (every word you type, listed as you type), and for **Remove** and **Change amount** its food/recipe box lists the ingredients of the chosen recipes to pick from, most used first ([What-if: Recipes](#whatif-recipes)).
- **49.** A recipe you've made can now go in My Pantry (**Add to pantry** on My Pantry's search, **In My Pantry** on the recipe's page, or the Recipes list's **Pantry** column), and complement suggestions offer it under **From your pantry**. Your other recipes are suggested under **Other options**, as things you could make. [learn more...](#pantry-recipes)
- **48.** On Fill in nutrients from another food and a custom food's Edit values page, **Compare checked foods with this one** turns blue once a food is ticked, as Compare buttons do elsewhere. Every Compare button now keeps your ticks after comparing, so coming back finds them still ticked; **Clear all picks** clears them. [learn more...](#compare-picks)
- **47.** Any food can now carry notes of your own: on its page, under **Notes**, click **Add your own notes on this food**. They're kept when you Refresh from USDA. A pantry entry's note can now be changed from the Pantry list. [learn more...](#food-notes)
- **46.** The Food Cache and My Pantry can be sorted by **Most meals, last 90 days**, the same order as Foods → 9's lists, and start that way unless you've already chosen another sort. [learn more...](#food-cache-web)
- **45.** On Foods → 9, every list of foods starts with the foods in the most meals over the last 90 days, with the count beside each name; **Order every list of foods** switches them to alphabetical. [learn more...](#checking-your-data)
- **44.** A Ctrl+click (or middle-click) on a page's Contents sidebar, or on the User Manual's contents or links, now shows the same "Opening in a browser tab" explanation as on NuMa's pages, and the tab opens the manual at that section. [learn more...](#two-windows)
- **43.** On a meal, a **View** menu beside Items' **Sort by** lists the meal three ways: **As logged**, **Foods** (recipes broken down into their foods) and **Foods & recipes** (each recipe kept whole, even one you added as individual ingredients). [learn more...](#meal-items-view)
- **42.** New **Archived foods & recipes** page (Foods → 10, or press `0` in the Foods menu; also Recipes → 3): lists only what you've archived, with the Food Cache's columns, and shows which archived foods and recipes are missing nutrient data. Meals logged with them still count in your long-run averages. [learn more...](#archived-web)
- **41.** The [Food Cache](#cached) and My Pantry lists have an **Other nutrients** column after DIAAS: "complete" when a food has its macronutrients, water, minerals, vitamins and the amino acids DCP needs, otherwise "incomplete", with what's missing shown when you point at it.
- **40.** When you add a recipe to a meal, the hint under its Amount box now says what one serving weighs ("1 serving = 24 g"), even when the recipe has no serving description. [learn more...](#portions-vs-servings)
- **39.** On both Food Use pages, a replace, remove or add now always says what happened, in a colored box the page opens at. It names what was changed and in how many meals or recipes, or says nothing was changed and why (a mistyped code used to change nothing and say nothing). After a mistake, the codes you typed are still there to correct. See [Replace a Food or Recipe Everywhere](#fooduse-substitute).
- **38.** On the [Food Cache](#cached), your **Fetch** ticks and any "Deletion not possible" warnings are still there when you leave the page and click your way back, so you can look at the meal that's using a food without losing your place. Coming back with a keyboard shortcut starts the page fresh.
- **37.** NuMa's own window shows NuMa's icon in Alt+Tab again, even while your everyday Chromium is open. The window now runs separately from your browser, with its own browser settings, so your browser's extensions no longer reach it. See [Browser to Launch](#browser-to-launch).
- **36.** On the **Recipes** list, **Meals & Log** and **Search meal history**, press **Alt+Shift+G**, type a row's ID (`21` for R21), and press **Enter**: that recipe or meal opens. See [Opening a recipe or meal by its ID](#go-to-id).
- **35.** MANUAL: [Tips for new users](#new-user-tips) now says NuMa can be used entirely from the keyboard, starting from `Alt+Shift+K`.
- **34.** A meal page that reloads after you change a setting on its search results keeps your place reliably: when the online results arrived at the wrong moment, it used to jump back to the top.
- **33.** **Alt+Shift+K** opens a *command palette*: every page in the menus, and whatever the page you're on has a shortcut for, each with its keys, narrowed as you type; it can also search foods, recipes and meals for what you typed, or quit NuMa. `Ctrl+K` opens it too. Settings' Keyboard Shortcuts section is now `Alt+Shift+E`. See [Finding your way around](#command-palette).
- **32.** What-if: Meals removes (or changes the amount of) a recipe logged as individual ingredients even after you changed it for that meal: each of those foods now remembers its recipe, shown as *part of* on the meal page. Where a change can't reach such foods (a Replace, or a sub-recipe inside a recipe logged that way), it names the meals. [learn more...](#whatif-ingredients)
- **31.** A food's **Edit** page ends with **Ask Claude AI for help** (one nutrient group or the whole profile; missing values only, or every value), and the *No amino acid data* box lists its fixes in order, ending with a Claude AI prompt. New [Workflow 12](#fix-food-data) gives the steps.
- **30.** **Edit Recipe**'s search results show each recipe's **DCP/srv** and **Description**, right after **Code**.
- **29.** **Edit Recipe** has a **Contents** list down the side that jumps to each part (opening it if collapsed), and a **Clear search** button right after **Search**.
- **28.** The **Recipes** list's filter now keeps only recipes whose names hold every word you type, like the other list filters: `coffee 2` finds Coffee 2, not every recipe with a 2 in its name.
- **27.** On a recipe's **Edit** page, each add, remove or amount change offers a short report on how it moved the recipe's nutrients per serving (groups you pick, all nutrients, or only those that changed by 5% or more); reports go into `recipe-edit-effects-data.md`, shown by a button above **Add Ingredient**. Food and recipe names there now open in a panel over the page. [learn more...](#recipe-edit-effects)
- **26.** In **Settings → 6**, NuMa now checks a USDA API key with USDA when you save it, and won't save one USDA rejects; **Test key** checks the saved key again, and the card shows when it was last checked.
- **25.** The yellow bar above the manual now has **↩ Return to …** (Alt+Shift+U), which goes straight back to the NuMa page you came from however many jumps you've made in the manual; **Manual** then reopens it where you left off. **← Back one step** (Alt+←) still retraces your jumps one at a time.
- **24.** MANUAL: The User Manual is reorganized and about a fifth shorter. New: an Overview with a short primer on the ideas NuMa uses, eleven step-by-step Workflow examples (starting with taking stock of your own food), and a Menu by menu Part with each page's tables and columns beside its menu item. The science moved to its own Part, the help and troubleshooting sections are together, and this What's new section now keeps one line per change.
- **23.** Removing an item from a meal no longer makes the page jump around: you stay where you were in the Items list, and a search you had going stays put.
- **22.** `!` before a word now works in the boxes that filter a list too (Recipes, Food Cache, My Pantry, Search meal history and the rest): `beans !kidney` keeps the beans that aren't kidney beans.
- **21.** On the **Meals & Log** list, the **Complete** column is now a checkbox: tick or untick it to mark a meal complete without opening it.
- **20.** On the Annotate page, each estimate NuMa is asking for has its own **Skip** button beside it; GI's moves you on to the DIAAS box when DIAAS is asked for too.
- **19.** After a food search that includes USDA, NuMa offers to search again with your words reversed (`small red beans` for `beans red small`), which finds many branded products; you can edit it, and add its results below yours or replace them.
- **18.** A hint under every food and recipe search box now sums up how to write a search: most important word first, `!` to leave a word out, and codes or barcodes, with a **Learn more** link.
- **17.** Searching for a cooked food online no longer leaves out canned products, whose names say "canned" rather than "cooked".
- **16.** When `!` words leave results out of a food search, the list ends with a line saying how many, such as "6 matches hidden by `!kidney`".
- **15.** Put `!` before a word in a food search to leave out results with it: `beans red !kidney cooked` finds cooked red beans but not kidney beans.
- **14.** Ticks in a **Compare** column are kept when you search again or go to another list, so one comparison can gather foods and recipes from several searches; a note under each Compare button lists them.
- **13.** In every search list, the `↓` and `↑` keys move the red outline from result to result, and coming back from a result you opened puts the outline on it again.
- **12.** Print / Save pages, Food Search from What-if, Annotate's Claude GI prompt and suggested foods' links now open in NuMa's own window, not in your default browser.
- **11.** The searches for adding an ingredient to a recipe, adding to a meal and adding to My Pantry show the same boxes, labeled under each result's name; ticking one no longer leaves a false "unsaved changes" warning.
- **10.** Foods search results have the same boxes: **Complete** and **Drink** on recipes, **Drink** on your own foods.
- **9.** The Recipes list has a **Drink** checkbox and a clickable **Complete** checkbox on every row (filtered lists too); ticking either saves at once.
- **8.** In the manual's search, Tab now goes straight to the first result in Firefox, Enter opens it with your words highlighted, and the section you picked stays at the top of the screen.
- **7.** Each item you add to a meal now records the time of day you entered it, shown in a new **Time** column of the meal's Items list.
- **6.** A food's own page now has a **Delete this food** button.
- **5.** Searches match singular and plural both ways ("onions" finds "Green onion", "berry" finds "Berries"), so that food is no longer outranked by a recipe that matches fewer of your words.
- **4.** In food and recipe searches, when one of your own foods or recipes matches every word you typed, your items that match only some of the words now come after the online results, under their own heading.
- **3.** **Problems by food** (a button at the top of Foods → 9) lists everything wrong with each food in one place, with its fixes, a "Borrow values from" search and "not needed" buttons; each food's page shows the same list.
- **2.** Errors are written to `numa-errors.log` in NuMa's data folder, so a failed page leaves a record to report.
- **1.** An installed NuMa now shows the yellow "please restart it" bar after **Update Now** until you quit and start it again.

#### Release v2026-11-10-2201 summary

Version overview: GI processing and GL (glycemic load) calculation and analysis fully implemented, including an estimated GI for meals and recipes. Water intake from drinks and food now fully tracked. Daily Summary can add up every nutrient for any date range or chosen meals, and show days in blocks. Vitamin K from USDA corrected: it had been read from the wrong USDA figure, so most foods showed little or none, and Foods 9 now fixes foods saved earlier in one click. Protein complement suggestions reworked to count each food at its own digestibility and stay within a sensible amount per meal, and meal and day pages now check each meal against the amount of protein per meal that research recommends for building and keeping muscle, based on your weight and age. Online food searches are faster, and the app no longer freezes while one runs. Cooked recipes can record the water they keep after cooking, so meals no longer count the water that baked or boiled off, and water in a recipe counts as a drink only when the recipe is one; every item in a meal or recipe shows its grams of water. NuMa now opens in its own window, like a desktop program, when Chrome, Chromium, Brave, Edge or Vivaldi is installed, with the manual inside it under the menu, and Ctrl+Q quits it; a Ctrl+click there first explains that the page will open in a browser tab. Many interface improvements and bug fixes.

- **29.** New starter foods and recipes: raisins, ground flax seeds, soy protein isolate powder, deglet noor dates and Chinese five spice powder, with three recipes (walnut milk, a Mexican coffee made with it, and a black bean and quinoa meal); granulated sugar, almonds and graham crackers improved.
- **28.** MANUAL: Monthly full read-through of the manual against the program: about 40 corrections, mostly to sections that still described NuMa in a browser tab or older screens; the post-update message now mentions NuMa's own window.
- **27.** MANUAL: Weekly sweep: updates log trimmed to the last two weeks, CIQUAL's food count corrected, a few search words added; a Portions page Save button no longer squeezes the Description box when it lights up.
- **26.** In NuMa's own window, a Ctrl+click (or middle-click) on a NuMa link now first explains that the page will open in a browser tab and how to get back, until you turn that off; the manual has a new "Working in two windows" section.
- **25.** A recipe used in a meal or another recipe can no longer be deleted; Delete offers to archive it instead.
- **24.** Meals and recipes that still name a deleted recipe are now listed in Foods → 9, with how to reconnect them, instead of behind a button on the Recipes list.
- **23.** The manual now opens in NuMa's own window under NuMa's menu, with a bar explaining how to get back (a Back button, or Alt+←).
- **22.** An amount typed as a weight with a note in brackets, such as `134.1 g (2/3 c)`, now keeps the note, and other text after a weight is refused instead of dropped; amounts now have their own manual section (Part 6 K).
- **21.** **Ctrl+Q** now quits NuMa and closes its window; in Firefox it quits Firefox and NuMa stops with it.
- **20.** NuMa now opens in its own window, with NuMa's icon and no tabs or address bar, when Chrome, Chromium, Brave, Edge or Vivaldi is installed; untick it in Settings → 13 for a normal tab.
- **19.** What-if can now apply every kind of change for real: Remove, Add and Change amount as well as Replace, on both the Meals and Recipes pages; the Recipes confirmation says how many logged meals will change and which recipes' stored weights to check.
- **18.** What-if: Meals can now apply a Remove for real, including a recipe logged as individual ingredients, after a confirmation page.
- **17.** What-if: Meals can now remove a recipe that was logged as individual ingredients, and says when a meal seems to hold one it couldn't match.
- **16.** The Nutrient Plot's note under its title now also says how many days the data is smoothed over.
- **15.** Water in a recipe now counts as water from food unless the recipe itself is marked as a drink (tap water in a bread dough is no longer counted as a drink), with a note on the recipe page; every item in a meal, recipe, day or portion analysis now shows its grams of water beside its name.
- **14.** A cooked recipe can now record the water it keeps after cooking, in g per 100 g (typed, copied from a food, or estimated from the weight it lost), and meals count that instead of the raw ingredients' water; recipes in a meal now show their water percentage too.
- **13.** A recipe's own page now has an Archive recipe button (Restore recipe once archived), between Copy recipe and Delete recipe.
- **12.** With Chrome or Chromium open, starting NuMa now opens it there instead of in your default browser.
- **11.** On the Nutrient Plot, two goal lines that land at the same height now both show, as one line in alternating colors.
- **10.** Reloading a food's Portions page after saving a change no longer shows "Method Not Allowed".
- **9.** Food Cache and Pantry can be sorted by how many recipes and meals use each food, and the Pantry now shows that count too; Pantry gets a Sort by menu.
- **8.** The Food Cache list now shows how many recipes and meals use each food.
- **7.** Duplicate Foods now has a Delete button on each copy that nothing uses.
- **6.** A barcode or FDC ID now works in every food search box, including on meal and recipe pages, and every search box says so underneath.
- **5.** Starting NuMa from source with web/launch-web.sh now installs any missing packages first.
- **4.** Settings → 11. Starter Data can now update every improved starter food and recipe with one button.
- **3.** After a search, its section comes to the top of the window and the cursor lands on the first result, on every page with a search.
- **2.** Alt+Shift+I now also clears the previous search's results when it puts the cursor in a search box.
- **1.** MANUAL: A new section explains how to move foods and recipes between NuMa installs with CSV files: exporting, importing, and what does and doesn't travel.

#### Release v2026-10-28-1228 summary

Version overview: GI processing and GL (glycemic load) calculation and analysis fully implemented, including an estimated GI for meals and recipes. Water intake from drinks and food now fully tracked. Daily Summary can add up every nutrient for any date range or chosen meals, and show days in blocks. Vitamin K from USDA corrected: it had been read from the wrong USDA figure, so most foods showed little or none, and Foods 9 now fixes foods saved earlier in one click. Protein complement suggestions reworked to count each food at its own digestibility and stay within a sensible amount per meal, and meal and day pages now check each meal against the amount of protein per meal that research recommends for building and keeping muscle, based on your weight and age. Online food searches are faster, and the app no longer freezes while one runs. Many interface improvements and bug fixes.

- **14.** MANUAL: Weekly sweep: the search results section now matches how results are ordered and says online results are reused for ten minutes; a few search words added.
- **13.** MANUAL: "Why you can trust NuMa" now describes the program's testing as it stands today, and the regular review schedule behind the manual and the food data.
- **12.** While a plot is on the Home page, any change made to it on the Nutrient Plot page now shows up on the Home page too.
- **11.** The Nutrient Plot's legend can now sit in a column to the right of the plot (Auto now puts it there when it won't fit on one row above), moving below the plot on a narrow screen.
- **10.** Each line on the Nutrient Plot now has its own point shape, shown in the legend too.
- **9.** Online food searches finish sooner, and NuMa no longer freezes while one runs: adding a food to a meal no longer waits on the same search all over again.
- **8.** The line under a day page's title, and now a meal page's too, gives the DCP as a share of your daily DCP goal first, then as a share of raw protein.
- **7.** Food searches rank better: a word inside another word ("raw" in "strawberry") no longer counts as a match, and recipes no longer jump ahead of foods that match your search better.
- **6.** Every Save button with unsaved changes in its form now lights up in solid blue with a red border, not just a faint outline.
- **5.** On the Annotate page, **Save annotation** lights up as soon as you change anything, including a "don't prompt me" box.
- **4.** Foods → 9's amino acid and portion lists get the same save reminder and leave-without-saving question as the GI list.
- **3.** Foods → 9's GI list now reminds you to save beside the **Also list...** button, and asks before you leave with unsaved "not needed" changes.
- **2.** Foods → 9's "Foods you use with no GI" list can now also show every food whose GI you've marked "not needed", so you can find and undo those choices.
- **1.** **Alt+Shift+Y** on a recipe's Edit page now jumps to its Ingredients section.

## Notes

[^1]: Lippman, D., Stump, M., Veazey, E., Guimarães, S. T., Rosenfeld, R., Kelly, J. H., Ornish, D., & Katz, D. L. (2024). Foundations of Lifestyle Medicine and its Evolution. *Mayo Clinic Proceedings: Innovations, Quality & Outcomes, 8(1)*, 97–111. https://doi.org/10.1016/j.mayocpiqo.2023.11.004

[^2]: U.S. Department of Agriculture, Agricultural Research Service. (2019). *FoodData Central*. https://fdc.nal.usda.gov/

[^3]: Open Food Facts contributors. (2012). *Open Food Facts*. https://world.openfoodfacts.org/

[^4]: Institute of Medicine (US) Panel on Micronutrients. (2001). *Dietary Reference Intakes for Vitamin A, Vitamin K, Arsenic, Boron, Chromium, Copper, Iodine, Iron, Manganese, Molybdenum, Nickel, Silicon, Vanadium, and Zinc*. National Academies Press. https://doi.org/10.17226/10026 — the underlying Dietary Reference Intake report establishing that non-heme iron and phytate-inhibited zinc from plant foods are absorbed less efficiently than from mixed/omnivorous diets; the basis for the NIH fact-sheet figures below.

[^5]: National Institutes of Health, Office of Dietary Supplements. *Iron: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/ — states that because vegetarian diets contain no heme iron and their non-heme iron is less bioavailable, "the RDA for vegetarians is 1.8 times higher than for people who eat meat."

[^6]: National Institutes of Health, Office of Dietary Supplements. *Zinc: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/ — states that "the zinc requirements for vegetarians may be as much as 50% higher than for those who eat meat" because of the reduced bioavailability of zinc from plant-based diets.

[^7]: National Institutes of Health, Office of Dietary Supplements. *Vitamin B12: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/ — vitamin B12 occurs naturally only in animal foods. See also Melina, V., Craig, W., & Levin, S. (2016). Position of the Academy of Nutrition and Dietetics: Vegetarian Diets. *Journal of the Academy of Nutrition and Dietetics, 116*(12), 1970–1980. https://doi.org/10.1016/j.jand.2016.09.025 — recommends that vegans obtain vitamin B12 routinely from fortified foods or a supplement, since no reliable unfortified plant source exists. Neither source specifies a "50% of RDA" cutoff for a single day's intake; that trigger is NuMa's own design choice (see main text).

[^8]: Atkinson, Brand-Miller, Foster-Powell, Buyken & Goletzke, "International tables of glycemic index and glycemic load values 2021: a systematic review," *The American Journal of Clinical Nutrition* 114(5):1625–1632 (doi:10.1093/ajcn/nqab233). The newer of the two editions involved. NuMa does not ship it — its license forbids that — but it can read it into your own copy in a few minutes; see [Upgrading to the 2021 tables](#gi-editions). The published table is actually two online supplemental tables, and the thing to understand about them is that they are split by **how well the study was run, not by who it was run on**: **Supplemental Table 1** holds values from studies whose method was consistent with ISO 26642:2010 (food numbers 1–2091), and **Supplemental Table 2** holds values from studies that deviated from that standard — fewer than ten subjects, an unusual carbohydrate portion, an unrepeated reference food — or whose results varied widely (2092–4018). Most of Table 2 was still measured in normal-glucose-tolerance subjects, so NuMa takes each row's subject group from that row's own "Subjects (type & number)" column and carries ISO compliance as a separate flag; see [Method quality](#gi-method-quality). This is a change from the 2008 edition, whose two appendix tables genuinely were split by population. Values are taken from the glucose-referenced GI column (GI, Glucose=100), matching the scale NuMa uses everywhere else. Glycemic load is not imported from the table at all: the published GL is a *nominal* figure computed from a standardized carbohydrate portion for the whole food category, and the source itself calls it "intended as a guide only", so NuMa computes GL live from a food's own cached carbohydrate content and the amount consumed instead (see [Glycemic Load](#gl)). Each row also publishes its **year of test** and country of food production, which NuMa shows in the lookup — see [How to read a lookup result](#gi-result-row). Licensing: published under the Elsevier user license, which expressly permits "access, download, copy, translate, text and data mine" for non-commercial purposes but forbids redistribution, reposting and adaptation. That is precisely why NuMa ships the parser and the Creative Commons 2008 edition[^8a] rather than this table: extracting the data for your own use is something the license allows *you* to do, and the resulting file stays on your machine. Copyright is held by the American Society for Nutrition; permission to distribute would have to come from them via the publisher. Every entry cites its source study by number, listed in the supplemental tables' own footnotes and reference list; a code beginning **UO** means "unpublished observations", for which there is no paper to trace.

[^8a]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2008," *Diabetes Care* 31(12):2281–3. **The edition built into NuMa**, and the one every install has. A Creative Commons–licensed table, which is exactly why it can ship with the program at all. If you add the 2021 edition[^8] yourself, NuMa keeps the few hundred of this edition's foods that 2021 does not appear to cover, labeled **2008 edition** in lookup results — see [Upgrading to the 2021 tables](#gi-editions). Those rows have no year of test, no standard error and no country, because this edition did not publish them in a form NuMa captured; "2008" on such a row is the edition it came from, never the year the food was tested.

[^8b]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2002," *The American Journal of Clinical Nutrition* 76(1):5–56. Deliberately **not** used. It is the direct predecessor of the 2008 table above, which revised and absorbed it, so adding it would mainly contribute duplicate food names carrying older values for the same studies — actively worse than not having them, since the lookup shows you every plausible match to choose between. Listed here only to record that it was considered and why it was rejected.

[^9]: US National Institutes of Health. (2026, July 31). Office of Dietary Supplements—Nutrient Recommendations and Databases. https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

[^10]: NuMa's own curated table of amino-acid profiles for common protein-complement foods — beans, grains, seeds, and a few animal foods included for comparison. 23 of the 25 entries cite a specific [USDA](#gloss-usda) FoodData Central SR Legacy record by FDC ID, sourced the same way as the rest of NuMa's nutrient data[^2]; the remaining two (nutritional yeast, pea protein powder) use published amino-acid-composition literature values because no matching USDA record exists for those specific products. NuMa always checks your own food cache for a real match to each entry's food name before falling back to these built-in figures — see [amino acid estimates in complement suggestions](#comp-estimate).

[^11]: Harvard T.H. Chan School of Public Health, Renal and Urology News Oxalate Table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine, "whose laboratory measured the oxalate content of many foods on this list"; the spreadsheet is marked "Posted Nov. 2023", and an asterisk marks a directly measured value. Retrieved for NuMa 22 June 2026. https://hsph.harvard.edu/wp-content/uploads/2024/07/OXALATE-TABLE-1.xlsx — NuMa matches foods to this table by name; see [Oxalate data](#oxalate) for enabling it, matching, and limitations.

[^12]: Holick, M. F., Binkley, N. C., Bischoff-Ferrari, H. A., Gordon, C. M., Hanley, D. A., Heaney, R. P., Murad, M. H., & Weaver, C. M. (2011). Evaluation, Treatment, and Prevention of Vitamin D Deficiency: an Endocrine Society Clinical Practice Guideline. *Journal of Clinical Endocrinology & Metabolism, 96*(7), 1911–1930. https://doi.org/10.1210/jc.2011-0385 — recommends adults at risk of deficiency take 1500–2000 IU/day (37.5–50 mcg) of vitamin D to reliably maintain a blood level above 30 ng/mL, well above the 15–20 mcg RDA. NuMa's built-in Revised Optimal default (50 mcg) sits at the top of that range.

[^13]: Kris-Etherton, P. M., Innis, S., American Dietetic Association, & Dietitians of Canada. (2007). Position of the American Dietetic Association and Dietitians of Canada: Dietary Fatty Acids. *Journal of the American Dietetic Association, 107*(9), 1599–1611. https://doi.org/10.1016/j.jada.2007.07.024 — summarizes multiple expert-body recommendations (including ISSFAL's) converging on roughly 500 mg/day combined EPA+DHA for general cardiovascular health in adults without existing heart disease, well above what a typical omega-3-ALA-only diet provides. NuMa's built-in Revised Optimal defaults (250 mg EPA + 250 mg DHA) split that combined figure evenly.

[^14]: Young, V. R., & Pellett, P. L. (1994). Plant proteins in relation to human protein and amino acid nutrition. *American Journal of Clinical Nutrition, 59*(5, Suppl.), 1203S–1212S. — the basis for the modern consensus that complementary protein sources don't need to be eaten at the same meal, since the body's own daily protein turnover (roughly 250–300 g) can supply amino acids the free pool is short on.

[^15]: Arentson-Lantz, E. J., Von Ruff, Z., Connolly, G., Albano, F., Kilroe, S. P., Wacher, A., Campbell, W. W., & Paddon-Jones, D. (2024). Meals containing equivalent total protein from foods providing complete, complementary, or incomplete essential amino acid profiles do not differentially affect 24-h skeletal muscle protein synthesis in healthy, middle-aged women. *The Journal of Nutrition*. Advance online publication. — a controlled feeding study finding no significant difference in acute or 24-hour muscle protein synthesis across complete, complementary, and single incomplete-protein meal conditions.

[^16]: FAO. (2013). *Dietary protein quality evaluation in human nutrition.* FAO Food and Nutrition Paper 92. Food and Agriculture Organization of the United Nations, Rome. *Available at:* https://www.researchgate.net/profile/Suzane-Leser/publication/259554481_The_2013_FAO_report_on_dietary_protein_quality_evaluation_in_human_nutrition_Recommendations_and_implications/links/5da88dfca6fdccdad54c5210/The-2013-FAO-report-on-dietary-protein-quality-evaluation-in-human-nutrition-Recommendations-and-implications.pdf

[^17]: MedlinePlus, National Library of Medicine. *Dietary Proteins*. https://medlineplus.gov/dietaryproteins.html

[^18]: MedlinePlus, National Library of Medicine. *Carbohydrates*. https://www.medlineplus.gov/carbohydrates.html

[^19]: MedlinePlus, National Library of Medicine. *Dietary fats explained*. https://medlineplus.gov/ency/patientinstructions/000104.htm

[^20]: MedlinePlus, National Library of Medicine. *Dietary Fiber*. https://medlineplus.gov/dietaryfiber.html

[^21]: MedlinePlus, National Library of Medicine. *Sweeteners – Sugars*. https://www.medlineplus.gov/ency/article/002444.htm

[^22]: Examine.com. *Saturated Fat*. https://examine.com/foods/saturated-fat/

[^23]: Linus Pauling Institute, Oregon State University. *Essential Fatty Acids*. https://lpi.oregonstate.edu/mic/other-nutrients/essential-fatty-acids

[^24]: Linus Pauling Institute, Oregon State University. *Calcium*. https://lpi.oregonstate.edu/mic/minerals/calcium

[^25]: Linus Pauling Institute, Oregon State University. *Magnesium*. https://lpi.oregonstate.edu/mic/minerals/magnesium

[^26]: Linus Pauling Institute, Oregon State University. *Phosphorus*. https://lpi.oregonstate.edu/mic/minerals/phosphorus

[^27]: Linus Pauling Institute, Oregon State University. *Potassium*. https://lpi.oregonstate.edu/mic/minerals/potassium

[^28]: Linus Pauling Institute, Oregon State University. *Sodium*. https://lpi.oregonstate.edu/mic/minerals/sodium

[^29]: Linus Pauling Institute, Oregon State University. *Iron*. https://lpi.oregonstate.edu/mic/minerals/iron

[^30]: Linus Pauling Institute, Oregon State University. *Zinc*. https://lpi.oregonstate.edu/mic/minerals/zinc

[^31]: Linus Pauling Institute, Oregon State University. *Iodine*. https://lpi.oregonstate.edu/mic/minerals/iodine

[^32]: Linus Pauling Institute, Oregon State University. *Selenium*. https://lpi.oregonstate.edu/mic/minerals/selenium

[^33]: Linus Pauling Institute, Oregon State University. *Vitamin A*. https://lpi.oregonstate.edu/mic/vitamins/vitamin-A

[^34]: Linus Pauling Institute, Oregon State University. *Vitamin C*. https://lpi.oregonstate.edu/mic/vitamins/vitamin-C

[^35]: Linus Pauling Institute, Oregon State University. *Vitamin D*. https://lpi.oregonstate.edu/mic/vitamins/vitamin-D

[^36]: Linus Pauling Institute, Oregon State University. *Vitamin E*. https://lpi.oregonstate.edu/mic/vitamins/vitamin-E

[^37]: Linus Pauling Institute, Oregon State University. *Vitamin K*. https://lpi.oregonstate.edu/mic/vitamins/vitamin-K

[^38]: Linus Pauling Institute, Oregon State University. *Thiamin*. https://lpi.oregonstate.edu/mic/vitamins/thiamin

[^39]: Linus Pauling Institute, Oregon State University. *Riboflavin*. https://lpi.oregonstate.edu/mic/vitamins/riboflavin

[^40]: Linus Pauling Institute, Oregon State University. *Niacin*. https://lpi.oregonstate.edu/mic/vitamins/niacin

[^41]: Linus Pauling Institute, Oregon State University. *Vitamin B6*. https://lpi.oregonstate.edu/mic/vitamins/vitamin-B6

[^42]: Linus Pauling Institute, Oregon State University. *Folate*. https://lpi.oregonstate.edu/mic/vitamins/folate

[^43]: Linus Pauling Institute, Oregon State University. *Vitamin B12*. https://lpi.oregonstate.edu/mic/vitamins/vitamin-B12

[^44]: Linus Pauling Institute, Oregon State University. *Choline*. https://lpi.oregonstate.edu/mic/other-nutrients/choline

[^45]: Linus Pauling Institute, Oregon State University. *Carotenoids*. https://lpi.oregonstate.edu/mic/dietary-factors/phytochemicals/carotenoids

[^46]: Linus Pauling Institute, Oregon State University. *Soy Isoflavones*. https://lpi.oregonstate.edu/mic/dietary-factors/phytochemicals/soy-isoflavones

[^47]: Linus Pauling Institute, Oregon State University. *Phytosterols*. https://lpi.oregonstate.edu/mic/dietary-factors/phytochemicals/phytosterols

[^48]: US National Institutes of Health, Office of Dietary Supplements. *Calcium – Consumer*. https://ods.od.nih.gov/factsheets/Calcium-Consumer/

[^49]: US National Institutes of Health, Office of Dietary Supplements. *Phosphorus – Consumer*. https://ods.od.nih.gov/factsheets/Phosphorus-Consumer/

[^50]: US National Institutes of Health, Office of Dietary Supplements. *Iron – Consumer*. https://ods.od.nih.gov/factsheets/Iron-Consumer/

[^51]: US National Institutes of Health, Office of Dietary Supplements. *Zinc – Consumer*. https://ods.od.nih.gov/factsheets/Zinc-Consumer/

[^52]: US National Institutes of Health, Office of Dietary Supplements. *Iodine – Consumer*. https://ods.od.nih.gov/factsheets/Iodine-Consumer/

[^53]: US National Institutes of Health, Office of Dietary Supplements. *Selenium – Consumer*. https://ods.od.nih.gov/factsheets/Selenium-Consumer/

[^54]: US National Institutes of Health, Office of Dietary Supplements. *Vitamin A and Carotenoids – Consumer*. https://ods.od.nih.gov/factsheets/VitaminA-Consumer/

[^55]: US National Institutes of Health, Office of Dietary Supplements. *Vitamin C – Consumer*. https://ods.od.nih.gov/factsheets/VitaminC-Consumer/

[^56]: US National Institutes of Health, Office of Dietary Supplements. *Vitamin D – Consumer*. https://ods.od.nih.gov/factsheets/VitaminD-Consumer/

[^57]: US National Institutes of Health, Office of Dietary Supplements. *Vitamin E – Consumer*. https://ods.od.nih.gov/factsheets/VitaminE-Consumer/

[^58]: US National Institutes of Health, Office of Dietary Supplements. *Vitamin B6 – Consumer*. https://ods.od.nih.gov/factsheets/VitaminB6-Consumer/

[^59]: US National Institutes of Health, Office of Dietary Supplements. *Choline – Consumer*. https://ods.od.nih.gov/factsheets/Choline-Consumer/

[^60]: Institute of Medicine (US), Food and Nutrition Board. *Dietary Reference Intakes for Energy, Carbohydrate, Fiber, Fat, Fatty Acids, Cholesterol, Protein, and Amino Acids*. National Academies Press, 2005. The protein RDA of 0.8 g/kg/day is specified for protein of mixed quality as typically consumed, and the report notes that requirements may differ for diets based on less-digestible plant protein sources. https://nap.nationalacademies.org/catalog/10490/

[^61]: Barclay, A. "How to enjoy a moderate glycemic load diet." *GI News*, Glycemic Index Foundation / University of Sydney, November 2021. https://glycemicindex.com/2021/11/how-to-enjoy-a-moderate-glycemic-load-diet/ — States that "an average daily GL of less than 80 g per 2000 calories ... is considered a moderate GL diet", alongside 130–230 g of available carbohydrate a day and an average [GI](#gloss-gi) under 45. This is the best-sourced daily figure available, and its "per 2,000 calories" wording is what lets NuMa scale it to a person's own calorie target. Even so, the article gives no study behind the 80; its own references concern fiber and blood lipids, not a [GL](#gloss-gl) cut-off.

[^62]: Advertising Standards Authority (UK). "Weight control: Glycaemic index (GI)." Advice Online, updated 25 November 2025. https://www.asa.org.uk/advice-online/weight-control-glycaemic-index-gi.html — Lists "Low GL for the day: 80 or less" and "High GL for the day: 120 or more" as the classifications advertisers should use. It attributes them to no source; they are the same widely repeated day bands NuMa uses (see [Glycemic Load](#gl)), which is why NuMa calls them a convention rather than a clinical target.

[^63]: Livesey, G., Taylor, R., Livesey, H. F. et al. "Dietary Glycemic Index and Load and the Risk of Type 2 Diabetes: A Systematic Review and Updated Meta-Analyses of Prospective Cohort Studies." *Nutrients* 11(6):1280, 2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6627334/ — Pooling long-term cohort studies, type 2 diabetes risk rose by 26% (risk ratio 1.26, 95% CI 1.15–1.37) for every additional 80 g/day of [GL](#gloss-gl) in a 2,000 kcal diet, across intakes from about 73 to 257 g/day. The relationship is continuous: the paper identifies no threshold below which risk stops falling and no "safe" level. It supports "lower is better, on average", not any particular target — and as observational evidence it shows association, not proof that lowering [GL](#gloss-gl) alone lowers risk.

[^64]: Academy of Nutrition and Dietetics. "A Primer on Glycemic Index." *Practice trends*, eatrightpro.org. https://eatrightpro.org/news-center/practice-trends/glycemic-index — Summarizes the guideline position: the American Diabetes Association's annual *Standards of Care in Diabetes* gives no specific recommendation on [GI](#gloss-gi) or [GL](#gloss-gl); the UK's National Institute for Health and Care Excellence (NICE) recommends that adults with type 2 diabetes choose high-fiber, low-[GI](#gloss-gi) carbohydrate sources; Diabetes Canada's Clinical Practice Guidelines advise choosing low-[GI](#gloss-gi) carbohydrates. None sets a numeric daily [GL](#gloss-gl) target.

[^65]: Jäger, R., Kerksick, C. M., Campbell, B. I. et al. "International Society of Sports Nutrition Position Stand: protein and exercise." *Journal of the International Society of Sports Nutrition* 14:20, 2017. https://doi.org/10.1186/s12970-017-0177-8 (free full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC5477153/) — Point 5: "General recommendations are 0.25 g of a high-quality protein per kg of body weight, or an absolute dose of 20–40 g." Point 6: "Acute protein doses should strive to contain 700–3000 mg of leucine." Point 7: doses "should ideally be evenly distributed, every 3–4 h, across the day." Point 2: 1.4–2.0 g/kg/day overall for most exercisers. Written for people who exercise; NuMa uses its per-dose figures as the lower end for everyone under 65, and its absolute 20–40 g when no profile is set.

[^66]: Schoenfeld, B. J. & Aragon, A. A. "How much protein can the body use in a single meal for muscle-building? Implications for daily protein distribution." *Journal of the International Society of Sports Nutrition* 15:10, 2018. https://doi.org/10.1186/s12970-018-0215-1 — Concludes that "to maximize anabolism one should consume protein at a target intake of 0.4 g/kg/meal across a minimum of four meals in order to reach a minimum of 1.6 g/kg/day", with 0.55 g/kg/meal at the upper end of daily intakes. A review aimed at people training for muscle growth; NuMa uses 0.4 g/kg as the upper end of its range, not a requirement.

[^67]: Bauer, J., Biolo, G., Cederholm, T. et al. "Evidence-based recommendations for optimal dietary protein intake in older people: a position paper from the PROT-AGE Study Group." *Journal of the American Medical Directors Association* 14(8):542–559, 2013. https://www.jamda.com/article/S1525-8610(13)00326-5/fulltext — Recommends at least 1.0–1.2 g/kg/day for people over 65, more with acute or chronic illness, and notes that the per-meal threshold for stimulating muscle protein synthesis is higher in older people than in young adults: 25–30 g of protein per meal, containing about 2.5–2.8 g of leucine. The group also says the evidence on per-meal amounts was not yet strong enough for firm recommendations — NuMa presents the figure as a guide accordingly.

[^68]: Trommelen, J., van Lieshout, G. A. A., Nyakayiru, J. et al. "The anabolic response to protein ingestion during recovery from exercise has no upper limit in magnitude and duration in vivo in humans." *Cell Reports Medicine* 4(12):101324, 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC10772463/ — In 36 healthy, recreationally active young men after whole-body resistance exercise, 100 g of milk protein produced a larger and longer (over 12 hours) anabolic response than 25 g; the authors conclude the response "is not restricted and has previously been underestimated". They caution it was a single session, in young men only, with one protein source — but it is why NuMa never treats a large meal as wasted protein.

[^69]: Salmerón, J., Manson, J. E., Stampfer, M. J. et al. "Dietary fiber, glycemic load, and risk of non-insulin-dependent diabetes mellitus in women." *JAMA* 277(6):472–477, 1997. — The Nurses' Health Study analysis that introduced glycemic load — a food's GI multiplied by its carbohydrate content — as a single measure of both the quality and the quantity of carbohydrate eaten. NuMa computes GL the same way, from each food's own carbohydrate and the amount eaten; the per-serving classification bands come with the international GI tables (footnote 8).

[^70]: Kerksick, C. M., Arent, S., Schoenfeld, B. J. et al. "International society of sports nutrition position stand: nutrient timing." *Journal of the International Society of Sports Nutrition* 14:33, 2017. https://pmc.ncbi.nlm.nih.gov/articles/PMC5596471/ — The position points used here: meeting the total daily protein intake, "preferably with evenly spaced protein feedings", should be "a primary area of emphasis" (point 6); a 20–40 g protein dose every three to four hours "appears to most favorably affect" muscle protein synthesis (point 11); "post-exercise ingestion (immediately to 2-h post) of high-quality protein sources stimulates robust increases" in it (point 9); pre- and/or post-exercise carbohydrate + protein or protein alone may support strength gains (point 8); about 30–40 g of casein before sleep "can acutely increase" overnight muscle protein synthesis (point 12); and, when glycogen must be restored quickly, carbohydrate at 0.8 g/kg/h with protein at 0.2–0.4 g/kg/h (point 3). A position stand from a sports-nutrition society — aimed at people who exercise.

[^71]: Schoenfeld, B. J., Aragon, A. A. & Krieger, J. W. "The effect of protein timing on muscle strength and hypertrophy: a meta-analysis." *Journal of the International Society of Sports Nutrition* 10:53, 2013. https://pmc.ncbi.nlm.nih.gov/articles/PMC3879660/ — Pooling 23 studies, protein taken within an hour of resistance exercise appeared to add muscle at first sight, but the effect "all but disappeared" once total protein intake was controlled for: the timed groups had simply eaten more protein. Total intake was the strongest predictor of muscle gain. It argues against a narrow post-exercise "window", not against eating protein after training.

[^72]: Morton, R. W., Murphy, K. T., McKellar, S. R. et al. "A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training-induced gains in muscle mass and strength in healthy adults." *British Journal of Sports Medicine* 52(6):376–384, 2018. https://pubmed.ncbi.nlm.nih.gov/28698222/ — Across 49 randomized trials (1,863 people), protein supplementation increased gains in strength and lean mass during resistance training of 6 weeks or more, but intakes beyond about 1.62 g/kg/day gave no further lean-mass gain. The benefit was smaller with increasing age.

[^73]: Mamerow, M. M., Mettler, J. A., English, K. L. et al. "Dietary protein distribution positively influences 24-h muscle protein synthesis in healthy adults." *Journal of Nutrition* 144(6):876–880, 2014. https://pmc.ncbi.nlm.nih.gov/articles/PMC4018950/ — In 8 healthy adults eating the same daily protein two ways, an even spread (about 31, 30 and 33 g at breakfast, lunch and dinner) gave 25% higher 24-hour muscle protein synthesis than a skewed one (about 11, 16 and 63 g), and the difference held after a week on each diet. A small study, but a direct test of distribution with total intake held equal.

[^74]: Churchward-Venne, T. A., Pinckaers, P. J. M., Smeets, J. S. J. et al. "Dose-response effects of dietary protein on muscle protein synthesis during recovery from endurance exercise in young men: a double-blind randomized trial." *American Journal of Clinical Nutrition* 112(2):303–317, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7398777/ — In 48 endurance-trained young men (cyclists and triathletes) after 90 minutes of cycling, with carbohydrate, "30 g of a high-quality protein (or a mean of ∼0.49 g protein/kg) is sufficient to maximize" myofibrillar protein synthesis; doses up to 45 g did not raise it further, and protein "did not result in greater" mitochondrial protein synthesis than carbohydrate alone.

[^75]: Snijders, T., Res, P. T., Smeets, J. S. J. et al. "Protein ingestion before sleep increases muscle mass and strength gains during prolonged resistance-type exercise training in healthy young men." *Journal of Nutrition* 145(6):1178–1184, 2015. — 44 young men on a 12-week resistance program took either a drink with 27.5 g protein (casein), 15 g carbohydrate and 0.1 g fat every night before sleep, or a non-caloric placebo; the protein group gained more muscle size and strength. Young, training men only.

[^76]: Aoyama, S., Kim, H.-K., Hirooka, R. et al. "Distribution of dietary protein intake in daily meals influences skeletal muscle hypertrophy via the muscle clock." *Cell Reports* 36(1):109336, 2021. — In mice, protein concentrated at the first meal of the active period produced more muscle growth than the same protein at the last meal, and the effect was absent in mice with mutations in muscle clock genes; branched-chain amino acids were involved. In a cross-sectional study of 60 healthy women aged 65 and over, a larger share of protein at breakfast was associated with better muscle function. The human data show association, not cause.

[^77]: Institute of Medicine (US), Panel on Dietary Reference Intakes for Electrolytes and Water. *Dietary Reference Intakes for Water, Potassium, Sodium, Chloride, and Sulfate*. National Academies Press, 2005. https://doi.org/10.17226/10925 — Sets the Adequate Intake for total water (3.7 L/day men, 2.7 L/day women, of which about 3.0 and 2.2 L from beverages) from median intakes in US survey data, with food supplying roughly 20% of the total. Counts caffeinated and alcoholic drinks toward total water.

[^78]: Volkert, D., Beck, A. M., Cederholm, T. et al. "ESPEN guideline on clinical nutrition and hydration in geriatrics." *Clinical Nutrition* 38(1):10–47, 2019. https://doi.org/10.1016/j.clnu.2018.05.024 — Recommends that older women be offered at least 1.6 L and older men at least 2.0 L of drinks a day, unless a clinical condition requires otherwise.

[^79]: Parkinson, E., Hooper, L., Fynn, J. et al. "Low-intake dehydration prevalence in non-hospitalised older adults: Systematic review and meta-analysis." *Clinical Nutrition* 42(8):1510–1520, 2023. https://doi.org/10.1016/j.clnu.2023.06.010 — Pooled prevalence of low-intake dehydration (serum osmolality above 300 mOsm/kg) of about 24% in older adults living outside hospital.

[^80]: Rowe, J. W., Shock, N. W., DeFronzo, R. A. "The influence of age on the renal response to water deprivation in man." *Nephron* 17(4):270–278, 1976. https://doi.org/10.1159/000180731 — After 12 hours without water, the maximum urine concentration healthy men reached fell with age, the oldest group's being roughly a fifth below the youngest's.

[^81]: Phillips, P. A., Rolls, B. J., Ledingham, J. G. G. et al. "Reduced thirst after water deprivation in healthy elderly men." *New England Journal of Medicine* 311(12):753–759, 1984. https://doi.org/10.1056/NEJM198409203111202 — After 24 hours without water, healthy men aged 67–75 reported less thirst and drank less than young men, and their plasma stayed more concentrated.

[^82]: Hooper, L., Bunn, D., Jimoh, F. O., Fairweather-Tait, S. J. "Water-loss dehydration and aging." *Mechanisms of Ageing and Development* 136–137:50–58, 2014. https://doi.org/10.1016/j.mad.2013.11.009 — Review: water-loss dehydration is common in older people, driven by reduced thirst and the kidney's reduced ability to concentrate urine, among other age-related changes.

[^83]: Ziegler, E. E., Fomon, S. J. "Potential renal solute load of infant formulas." *Journal of Nutrition* 119(12 Suppl):1785–1788, 1989. https://doi.org/10.1093/jn/119.12_suppl.1785 — The standard estimate of the load the kidneys must clear, in which protein contributes its nitrogen (mg) divided by 28 mOsm: about 5.7 mOsm per gram of protein. (The paper concerns infant formulas; the arithmetic is the same for any diet.)

[^84]: EFSA Panel on Dietetic Products, Nutrition, and Allergies. "Scientific Opinion on Dietary reference values for water." *EFSA Journal* 8(3):1459, 2010. https://doi.org/10.2903/j.efsa.2010.1459 — EFSA's Adequate Intakes for total water: 2.5 L a day for men, 2.0 L for women. EFSA publishes no drinks figure; NuMa's drinks goal under EFSA is 80% of the total (2.0 and 1.6 L), from EFSA's own assumption that food supplies about 20%.

[^85]: National Institute for Health and Care Excellence. *Intravenous fluid therapy in adults in hospital* (Clinical Guideline CG174), 2013, updated 2017. https://www.nice.org.uk/guidance/cg174 — routine maintenance starts at 25–30 mL/kg/day of water; for patients with obesity, the prescription is adjusted to ideal body weight, and patients rarely need more than 3 L a day in total.

[^86]: Mathai, J. K., Liu, Y. & Stein, H. H. "Values for digestible indispensable amino acid scores (DIAAS) for some dairy and plant proteins may better describe protein quality than values calculated using the concept for protein digestibility-corrected amino acid scores (PDCAAS)." *British Journal of Nutrition* 117(4):490–499, 2017. https://doi.org/10.1017/S0007114517000125 — Measured in growing pigs, the animal model used for regulatory DIAAS work. For soy protein isolate, the standardized ileal digestibility of crude protein was 94%, and of the indispensable amino acids 96% on average (Tables 4–5). NuMa's 0.95 sits between the two, and is the same coefficient its digestibility table uses for soy protein isolate.

[^87]: Davis, B. C. & Kris-Etherton, P. M. "Achieving optimal essential fatty acid status in vegetarians: current knowledge and practical implications." *American Journal of Clinical Nutrition* 78(3 Suppl):640S–646S, 2003. https://doi.org/10.1093/ajcn/78.3.640S — Reports that conversion of ALA to EPA is inefficient, under 5–10%, and to DHA 2–5%; that vegetarian and vegan diets supply little if any EPA and DHA; and that total omega-3 requirements may therefore be higher for vegetarians than for non-vegetarians, who get some EPA and DHA directly.

[^88]: Burdge, G. C. & Calder, P. C. "Conversion of α-linolenic acid to longer-chain polyunsaturated fatty acids in human adults." *Reproduction Nutrition Development* 45(5):581–597, 2005. https://doi.org/10.1051/rnd:2005047 — A review of stable-isotope tracer studies: in men, conversion of ALA to EPA happens but is limited, and further conversion to DHA is very low; in women the fractional conversion is greater, possibly because of a regulatory effect of estrogen, and less ALA is burned for energy. The authors conclude ALA is a limited source of the longer-chain omega-3s.

[^89]: Moghaddam, E., Vogt, J. A. & Wolever, T. M. S. "The effects of fat and protein on glycemic responses in nondiabetic humans vary with waist circumference, fasting plasma insulin, and dietary fiber intake." *Journal of Nutrition* 136(10):2506–2511, 2006. https://pubmed.ncbi.nlm.nih.gov/16988118/ — 20 nondiabetic adults drank 50 g glucose with 0–30 g each of added fat and protein, 18 times each. Both lowered the glucose response; gram for gram, protein lowered it about twice as much as fat. How strong the effect was varied from person to person (with waist size, fasting insulin and fiber intake). The authors note the findings came from drinks and may not carry over to solid meals.

[^90]: Jenkins, D. J. A., Wolever, T. M. S., Leeds, A. R. et al. "Dietary fibres, fibre analogues, and glucose tolerance: importance of viscosity." *British Medical Journal* 1(6124):1392–1394, 1978. https://pmc.ncbi.nlm.nih.gov/articles/PMC1604761/ — Adding fibers such as guar, pectin or wheat bran to a 50 g glucose drink lowered the blood glucose rise, and the more viscous the fiber, the bigger the effect; guar lost its effect once broken down into a non-viscous form. Small groups of 4–6 volunteers.

[^91]: Wolever, T. M. S., Yang, M., Zeng, X. Y., Atkinson, F. & Brand-Miller, J. C. "Food glycemic index, as given in glycemic index tables, is a significant determinant of glycemic responses elicited by composite breakfast meals." *American Journal of Clinical Nutrition* 83(6):1306–1312, 2006. — Testing typical mixed breakfasts in 26 healthy people in Sydney and Toronto, the GI values from published tables did predict the blood glucose response of the whole meal. This is the opposite of what the study in footnote 92 found; the authors argued that earlier negative findings like that one came from problems of method.

[^92]: Flint, A., Møller, B. K., Raben, A. et al. "The use of glycaemic index tables to predict glycaemic index of composite breakfast meals." *British Journal of Nutrition* 91(6):979–989, 2004. https://doi.org/10.1079/BJN20041124 — 28 healthy young men ate 13 breakfasts, each with 50 g available carbohydrate but very different in energy, fat and protein. The meal GI predicted from the tables showed no association with the GI actually measured, and the more energy and fat a meal held, the lower its measured GI.

[^93]: Östman, E., Granfeldt, Y., Persson, L. & Björck, I. "Vinegar supplementation lowers glucose and insulin responses and increases satiety after a bread meal in healthy subjects." *European Journal of Clinical Nutrition* 59(9):983–988, 2005. https://doi.org/10.1038/sj.ejcn.1602197 — In 12 healthy volunteers, white bread eaten with vinegar gave a lower blood glucose rise at 30 and 45 minutes, and a lower insulin response, than the same bread alone, more so at higher doses. Small, short-term, and about vinegar's acetic acid specifically; NuMa's mention of lemon rests on the same reasoning (acid) rather than its own study.

[^94]: Dodd, H., Williams, S., Brown, R. & Venn, B. "Calculating meal glycemic index by using measured and published food values compared with directly measured meal glycemic index." *American Journal of Clinical Nutrition* 94(4):992–996, 2011. — 30 healthy adults ate three meals of 50 g carbohydrate each. The meal GI calculated from the foods' GIs was 22–50% higher than the GI measured for the whole meal.

[^95]: Spolar, M., Gibbs, A. L., Wolever, T. M. S., Hitchner, E. V. & Heimowitz, C. "Equivalent glycemic load (EGL): a method for quantifying the glycemic responses elicited by low carbohydrate foods." *Nutrition & Metabolism* 3:33, 2006. https://doi.org/10.1186/1743-7075-3-33 — Repeating the same portion of white bread in the same people, the response varied by about 65% (coefficient of variation) with 5 g carbohydrate, against about 31% with 20 g. The authors also note that glycemic load can't be used directly for low-carbohydrate foods, and propose a measured alternative.

[^96]: Mah, J. & Pitre, T. "Oral magnesium supplementation for insomnia in older adults: a Systematic Review & Meta-Analysis." *BMC Complementary Medicine and Therapies* 21:125, 2021. https://doi.org/10.1186/s12906-021-03297-z — Three randomized trials, 151 older adults: sleep onset about 17 minutes faster with magnesium, total sleep time not significantly changed; evidence judged low to very low in quality. The trials compared magnesium with placebo, not intake levels with each other.

[^97]: Hartley, L., Clar, C., Ghannam, O., Flowers, N., Stranges, S. & Rees, K. "Vitamin K for the primary prevention of cardiovascular disease." *Cochrane Database of Systematic Reviews* 2015, Issue 9, Art. No. CD011148. https://doi.org/10.1002/14651858.CD011148.pub2 — Found one eligible trial (60 healthy adults, menaquinone for three months) that reported no cardiovascular events and no effect on blood pressure or lipids; concludes the evidence is too thin to judge.

[^98]: Shea, M. K., Berkner, K. L., Ferland, G., Fu, X., Holden, R. M. & Booth, S. L. "Perspective: Evidence before Enthusiasm—A Critical Review of the Potential Cardiovascular Benefits of Vitamin K." *Advances in Nutrition* 12(3):632–646, 2021. https://doi.org/10.1093/advances/nmab004 — Observational studies link menaquinone (K2), but not phylloquinone (K1), intake to less coronary calcification; the review finds that claim of a unique K2 benefit unsupported by the intervention trials to date.

[^99]: Wallace, T. C. & Fulgoni, V. L. "Usual Choline Intakes Are Associated with Egg and Protein Food Consumption in the United States." *Nutrients* 9(8):839, 2017. https://doi.org/10.3390/nu9080839 — NHANES 2009–2014: only about 8% of US adults met the Adequate Intake for choline; no subgroup exceeded the upper limit.

[^100]: Obeid, R. & Karlsson, T. "Choline – a scoping review for Nordic Nutrition Recommendations 2023." *Food & Nutrition Research* 67, 2023. https://doi.org/10.29219/fnr.v67.10359 — Observational studies suggest adequate choline may benefit cognitive function in older people; prospective data are lacking and no intervention studies in the elderly are available.

[^101]: Demay, M. B., Pittas, A. G., Bikle, D. D. et al. "Vitamin D for the Prevention of Disease: An Endocrine Society Clinical Practice Guideline." *Journal of Clinical Endocrinology & Metabolism* 109(8):1907–1947, 2024. https://doi.org/10.1210/clinem/dgae290 — Suggests against vitamin D supplements above the IOM reference intakes in healthy adults under 75; suggests empiric supplementation for children and adolescents, adults 75 and older, pregnancy, and high-risk prediabetes; advises against routine blood-level testing. Optimal doses "remain unclear"; in the trials behind the 75+ recommendation (mortality outcome) doses ran from 400 to 3333 IU (10–83 mcg) a day, weighted average about 900 IU (23 mcg), and daily lower doses are preferred over occasional high ones. Replaces the 2011 guideline cited in [^12].

[^102]: Schlemmer, U., Frølich, W., Prieto, R. M. & Grases, F. "Phytate in foods and significance for humans: Food sources, intake, processing, bioavailability, protective role and analysis." *Molecular Nutrition & Food Research* 53(S2):S330–S375, 2009. https://doi.org/10.1002/mnfr.200900099 — Review: phytate as the seed's phosphorus store, its binding of iron, zinc, calcium and magnesium, and its breakdown by soaking, germination and fermentation.

[^103]: Hallberg, L., Brune, M. & Rossander, L. "Iron absorption in man: ascorbic acid and dose-dependent inhibition by phytate." *American Journal of Clinical Nutrition* 49(1):140–144, 1989. https://doi.org/10.1093/ajcn/49.1.140 — Phytate inhibits non-heme iron absorption in proportion to the amount; added ascorbic acid counteracts the inhibition, more of it counteracting more.

[^104]: Lopez, H. W., Krespine, V., Guy, C., Messager, A., Demigné, C. & Rémésy, C. "Prolonged fermentation of whole wheat sourdough reduces phytate level and increases soluble magnesium." *Journal of Agricultural and Food Chemistry* 49(5):2657–2662, 2001. https://doi.org/10.1021/jf001255z — Sourdough fermentation reduced whole wheat bread's phytate by 62%, yeast fermentation by 38%; pre-fermenting the bran reached about 90%. Measured in bread, not in people's absorption.

[^105]: Heaney, R. P., Weaver, C. M. & Recker, R. R. "Calcium absorbability from spinach." *American Journal of Clinical Nutrition* 47(4):707–709, 1988. https://doi.org/10.1093/ajcn/47.4.707 — Thirteen adults, crossover design, labeled calcium: mean absorption 27.6% from milk, 5.1% from spinach.

[^106]: US Food and Drug Administration. "Phytohaemagglutinin (kidney bean lectin)." In *Bad Bug Book: Handbook of Foodborne Pathogenic Microorganisms and Natural Toxins*, 2nd ed., 2012. https://www.fda.gov/media/83271/download — As few as four or five raw kidney beans can cause symptoms; boiling for 10 minutes destroyed the toxin in one study, but the FDA advises at least 5 hours' soaking and at least 30 minutes' boiling, and warns against slow cookers, which often reach only 75 °C.

[^107]: Avilés-Gaxiola, S., Chuck-Hernández, C. & Serna Saldívar, S. O. "Inactivation Methods of Trypsin Inhibitor in Legumes: A Review." *Journal of Food Science* 83(1):17–29, 2018. https://pubmed.ncbi.nlm.nih.gov/29210451/ — Trypsin inhibitors as a defense compound and major antinutritional factor of legumes; heat is the usual means of inactivating them, with how complete it is depending on time, temperature and the form of the bean.

[^108]: World Health Organization. *Pellagra and its prevention and control in major emergencies.* WHO/NHD/00.10, 2000. https://www.who.int/publications/i/item/WHO-NHD-00.10 — Pellagra as a disease of diets based on maize not treated with alkali, with outbreaks among refugees and displaced people since 1988; alkali (lime) treatment makes maize's niacin available.

[^109]: University of Michigan Health, Department of Urology. *Low Oxalate Diet Guidelines* (patient handout). https://www.med.umich.edu/1libr/urology/LowOxalateDietGuidelines.pdf — For people with high urinary oxalate, limit oxalate to 40–50 mg a day, or less if a doctor advises. The Oxalosis & Hyperoxaluria Foundation gives a general target of under 100 mg a day (https://ohf.org/diet-nutrition/low-oxalate-diet/). There is no single agreed figure.

[^110]: Berg, J. M., Tymoczko, J. L., Gatto, G. J. Jr. & Stryer, L. *Biochemistry*, 8th ed. New York: W. H. Freeman, 2015. Chapter 23, "Protein Turnover and Amino Acid Catabolism." — Amino acids beyond what is needed for protein synthesis are not stored; their amino group is removed and becomes urea, and their carbon skeletons are converted to glucose, ketone bodies or fat, or burned for energy. A standard textbook account; any current biochemistry text says the same.

[^111]: Thomson, C. D., Chisholm, A., McLachlan, S. K. & Campbell, J. M. "Brazil nuts: an effective way to improve selenium status." *American Journal of Clinical Nutrition* 87(2):379–384, 2008. https://doi.org/10.1093/ajcn/87.2.379 — In a 12-week trial, two Brazil nuts a day raised plasma selenium and glutathione peroxidase activity as effectively as 100 mcg of selenium as selenomethionine.

[^112]: Zeevi, D., Korem, T., Zmora, N. et al. "Personalized Nutrition by Prediction of Glycemic Responses." *Cell* 163(5):1079–1094, 2015. https://doi.org/10.1016/j.cell.2015.11.001 — A week of continuous glucose monitoring in 800 people (46,898 meals): identical meals gave widely different responses between people; a machine-learning model using blood tests, diet, anthropometrics, activity and gut microbiota predicted individual responses, was validated in 100 more people, and diets chosen from it lowered post-meal glucose in a blinded randomized trial.

[^113]: Vega-López, S., Ausman, L. M., Griffith, J. L. & Lichtenstein, A. H. "Interindividual variability and intra-individual reproducibility of glycemic index values for commercial white bread." *Diabetes Care* 30(6):1412–1417, 2007. https://doi.org/10.2337/dc06-1598 — 23 healthy adults, white bread tested against glucose up to three times each: within-person variation (coefficient of variation 42.8%) exceeded between-person variation (17.8%); individual GI values ranged from 44 to 132 around a mean of 71.

[^114]: Evert, A. B., Dennison, M., Gardner, C. D. et al. "Nutrition Therapy for Adults With Diabetes or Prediabetes: A Consensus Report." *Diabetes Care* 42(5):731–754, 2019. https://doi.org/10.2337/dci19-0014 — American Diabetes Association: carbohydrate counting with intensive insulin therapy for type 1 diabetes; consistent carbohydrate timing and amount on fixed insulin doses; for mixed meals high in fat or protein, insulin dosing should not rely on carbohydrate counting alone.


---

## Disclaimer {: #disclaimer}

NuMa is a personal food-record and nutrient-calculation tool, not a source of medical or dietary advice, and it makes no claim about health or illness. Its figures are informed estimates pooled from third-party food [databases](#gloss-database) and checked routinely for internal correctness — they are not a substitute for a physician, registered dietitian, or product label. See the full [Disclaimer](/disclaimer) for details on data accuracy, review practices, and your own responsibility when using this program.

