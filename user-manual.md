# NutriMagnus User Manual

*Updated 2026-08-31:2157* / Reading time: 4 hours, 25 minutes

*Last full audit: 2026-08-30*

**NutriMagnus ("NuMa")** is an open-source computer program which provides a thorough nutritional analysis of a user's food choices. It is particularly focused on protein because this is a problem for those eating primarily a plant-based diet, for older people, and for the chronically-ill.

**Eating usually involves making choices, and good choice requires good information.** The three major problems impeding good food choice are a) lack of awareness of the choices available, and b) lack of information about the nutritional character of those choices, and c) lack of information as to what constitutes a good choice. All of these problems are addressed by NuMa, in detail.

**Eating is fundamentally about survival - the first priority for all life.** Most of the cells in our body persist for a shorter period than we do. During their lifespan they do their work using materials available to them in their immediate environment. Eventually they must be replaced by new cells, constructed again from such available materials.

**Essential materials needed for cellular support and replacement come from what we eat.** While significant essential materials may already exist in the local environment of a cell, ultimately all materials come from outside our bodies, through eating.

**Both the program and its accompanying *User Manual* are in continuing active development.** They are modified frequently. Both are already quite sophisticated, but new versions will be made available quickly for those already using the program. However, the manual has not yet received a careful editorial review of all its parts. It is an advanced first draft.

**User feedback is highly valued, so please give us yours!** With computer programs in active development ANY feedback is appreciated and most likely useful. User experience with the program is a critical measure of program success or failure. So, please email all problems, thoughts, and ideas to [tomcloydmsma@gmail.com](mailto:tomcloydmsma@gmail.com). Put `NutriMagnus` or `NuMa` in the subject line, please!

**How to come up with feedback:** First, ANY thoughts you wish to share are welcome. If in doubt, just do it! We'll be grateful. Of particular interest to us are these topics:

1. Inconveniences: you notice that something seems a bit difficult to do, or you see a simpler or quicker way to do it.
2. Missing or incomplete information: Sometimes updates and changes do not go out to every part of the program as they should, and you see a gap in the information provided.
3. Outright nonsense: you look at program output and think "that can't be right" or maybe you just feel doubtful about it.

User-derived issues get immediate priority in the program-development process!

---

## How to read this Manual

NuMa runs as a web app, opened in your ordinary browser — there is nothing to install and no command line involved.

- Read **Part 1** (To get a quick start) for a fast orientation before diving in.
- Read **Part 2** (Introduction) for the ideas behind the program.
- Read **Part 3 — Using the Web App** for how to actually operate NuMa.
- Read **Part 4** (Core nutrition concepts) for more of the ideas behind the program.
- Read **Part 5** (Reading Your Results) whenever you want to know what a column or table means.
- Read **Part 6** (Shared Operations) for behaviors that show up in more than one place in the app, explained once.
- Parts 7 to 10 apply to everyone.
- Trying to find something in this document itself, not in the app? See [Using this manual's search](#search-howto) — it works differently from a plain text search.

## Part 1 — To get a quick start
### A. Start with what's easiest

This is a complex and powerful analytical program. A careful Internet search reveals that it is unique in its power and depth. It can be successfully approached by moving slowly and thoughtfully, with real benefit obtained from using some of its easiest and simplest features. 

Start with what is easiest to understand: analysis of single foods and simple recipes. Use the manual to learn more. Do not expect to learn it all in a few sessions. [Contact us](#feedback) quickly rather than slowly if you start to get overwhelmed — one of our goals is to minimize the risk of that happening!

### B. Two major tips for new learners

**Slow down and look carefully at what you see on your screen.** What you see is the interface between you and the program. By design, it is rich in information. You don't need to understand or use all of it immediately, but notice that there are often links such as "Learn more ==>" or "Why?" encouraging you to link to a section of the manual that will tell you much more about something.

**Learning a powerful tool requires time and frequent contact.** You have two critical things to learn: basic concepts (covered in [Part 4](#coreNutrition)) and the interface itself, including the functions listed on the main menu items drop-down menus. **If you don't commit to daily use of the program, for about a week, you will not get past the slow-fumbling stage.** What you are dealing with is a Boeing 727, not a Piper Cub. Learn the cockpit and you can be a world traveler! (And that learning can come gradually, but daily exposure is the key.)

### C. Numa often learns from you as you use it

While we don't yet have on-board local AI to help you with NuMa and your food questions, we do have Numa remembering recent entries you've made to text input boxes, and a number of different options you've selected. 

One huge asset is the [Food cache](#FoodCache) database you'll set up. This serves as a memory of every food you've looked up or put into your Pantry. Saved is the food name, ID number, and nutrition data. 

### D. Stuck? 

It happens to us all! You can first look in this manual's [Part 8 — Troubleshooting and feedback — reporting problems and offering ideas](#feedback) to see if your problem has an identified fix.

If you're wondering how to do something, search the Manual for one or two key words. For an especially efficient search, click the "Only show things you can do" checkbox that is right below the Manual's search text input box.

Still stuck? You need help...and it's readily available. Learn more...[here](#quickhelp).

### E. Use a kitchen scale to determine food quantities, if at all possible

You will have to tell the program WHAT you are eating and HOW MUCH. The absolute best way to do this is to give it a weight. Sometimes you can just give it a "portion" or a volume measure instead, and the program will figure out the weight for you from that so it can keep going. Remember that approximations are better than nothing, so if you can do nothing else, try to give NuMa an approximate amount.

Without the program you're flying blind. With it, even if you only use volume measures, there will be some errors of measurement, but you're still much better informed about what's happening than before. In some cases, though, a volume measure just doesn't work well. If that happens to you, [get in touch](#feedback) and we'll figure it out together. All in all, it's by far best to have and use a kitchen scale. I have had a small Oxo scale for years. It's excellent. There are others you can consider as well, but I do suggest that you get one.

### F. Download and install the program

a. **Where to get it.** Go to the [NutriMagnus releases page](https://github.com/tom-cloyd/NutriMagnus/releases) on GitHub and download `install-linux.sh` from the latest release — that's the one file you need, not a menu of binaries to choose between. Built and tested on Ubuntu 24.04 LTS; it should run on most other modern Linux distros too, but only Ubuntu is verified. If it doesn't run on yours, see the "For developers" section of the project's `README.md` to run NuMa from source instead — no compiled binary required.

b. **Where it goes on your computer.** Run the installer once (`bash install-linux.sh` in a terminal, from wherever you downloaded it). It copies the program into a private per-user location (`~/.local/bin`) — nothing outside your own account is touched, and it never asks for an admin password.

c. **Getting it into your applications menu.** The same installer step adds NuMa to your normal applications menu with its own icon, exactly like any program you'd install from a software center. Concretely, it writes one file — `~/.local/share/applications/nutrimagnus.desktop` — which every major Linux desktop reads automatically. Where to find it depends on your desktop environment:

   - **GNOME (Ubuntu's default):** press the **Super key** (the ⊞ / Windows key) or click **Activities** in the top-left corner, then type "NutriMagnus" or "NuMa".
   - **KDE Plasma:** open the application launcher (bottom-left icon, or press the Meta key) and type the same.
   - **Other desktops (XFCE, Cinnamon, MATE, ...):** open the applications menu (usually a button in a corner or a taskbar icon) and either browse to Utilities/Science or type "NutriMagnus" into its search box.

   **If it doesn't show up:** this is a known rough edge — some desktops only refresh their menu/search index at login, so a program installed while you're already logged in can be invisible until you log out and back in (a full restart isn't needed, just a fresh login). If it's still missing after that, run it directly instead — see "If the icon never appears" under the next item.

d. **How to launch it.** From then on, launch NuMa like any other program — click its icon in the applications menu (see item c for where to find it). It starts quietly in the background and opens a browser tab pointed at the running app. No terminal, no typed commands, ever, after the one-time install.

**If the icon never appears,** even after logging out and back in, you can still run NuMa directly: open a terminal and run `~/.local/bin/nutrimagnus` — that's the actual program the icon would have pointed to, installed there regardless of whether the menu entry works. [Contact us](#feedback) too, so this can get fixed for good.

e. **What kind of program this is, and what that means for you.** NuMa is a "web app" — a small program that runs quietly in the background on your own computer and shows its screens in a browser tab, the same way a website does. Nothing goes out over the internet: it's talking only to itself, on your machine, not to any server anywhere else. Two things follow from this:

   - **The browser tab and the program are two different things.** Closing the browser tab does not close NuMa — the background program is still running. To get back to it, either click NuMa's icon again (it will open a fresh tab pointed at the still-running program) or open a new browser tab yourself and go to the same address the first tab had.
   - **Putting your computer to sleep can disconnect the tab.** If you sleep or hibernate your computer while NuMa is open, the background program may stop when the computer sleeps and needs restarting when it wakes — you'll typically see the browser tab fail to load or show a connection error. This is expected, not a sign anything is broken. Just click NuMa's icon again to relaunch it; your data is stored on disk and is unaffected.

**Starter foods and recipes.** The first time you launch a fresh install, your Food Cache and Recipes list already contain a small set of starter items — foods with verified USDA nutrient and amino-acid data, and a few recipes chosen to demonstrate real protein-complementarity gains. Their names begin with an asterisk (for example, `* Pinto-quinoa meal`) so you can always tell them apart from anything you've added yourself, and remove or keep them as you like — see the [Settings](#settings) starter-data toggle if you clear them and want them back.

### G. Set up your personal profile and initialize your My Pantry foods

a. Go to Settings and set up your personal profile, if you want the program to immediately apply to you. 

b. Set up your Pantry foods as available primary protein sources: Go to Appendix C below and review the listed foods. Some you will likely have. The others you should consider buying if you're serious about making plant protein sources your sole or primary protein concern.

### H. Skim Part 2, A and F, just to know they exist.

While looking at section A, make a few notes about what you'd like to try first.

Seriously consider what is suggested in section F - looking at the workflows can quickly show you major program features.

### I. Consider investing some time with Part 4

This program necessarily uses some specialized vocabulary. You have two options:

1. Learn the basics before diving into the program's functions and output.
2. Dive in first, and use the "Learn more..." links you'll see to immediately jump to the relevant manual section, so you can understand whatever's in front of you right when you need to.

---

## Part 2 — Introduction to NutriMagnus, a tool for intelligent eating: what you can do with this tool and why it matters
---

### A. What a user can do with NutriMagnus — brief overview

The five items in the top navigation bar correspond to the five major things you can do with the program:

- **Foods**
    - Search the [USDA](#gloss-usda) and Open Food Facts[^3] databases
    - Analyze the nutrients in a specific portion of any food or recipe
    - Compare up to eight foods side-by-side
    - Manage your personal [Food Cache](#gloss-food-cache), Pantry, and custom food profiles
    - Annotate foods with glycemic index and [DIAAS](#gloss-diaas) estimates
    - Export/import your Food Cache as CSV, to move data to or from another NuMa install
- **Recipes**
    - Create and save recipes with ingredients and instructions
    - Browse, copy, and delete saved recipes
    - Export/import a recipe as a self-contained CSV, bundling every sub-recipe and ingredient's data along with it
    - Develop a recipe iteratively with nutritional feedback after each ingredient change
    - Analyze a recipe portion for full nutrient data, protein quality, and complement suggestions
- **Meals & Log**
    - Record what you eat by date
    - Add foods and recipes to meals
    - Analyze individual meals or the combined total for a full day, to monitor intake of any nutrient(s) of particular interest
    - Search your entire meal history for any food
- **Analysis** — a growing set of preset analyses
    - **Daily summary — [DCP](#gloss-dcp) and goals**: combined nutrient totals for today or any past date, compared against personalized [RDA](#gloss-rda) targets, plus a list of recent days with meals
    - **Food use in meals**: rank which foods were used across a chosen set of date ranges and/or meals, with a frequency histogram
    - **Food use in recipes**: the same ranking, but for which foods and sub-recipes appear as ingredients across your recipes
    - Both Food Use pages can also bulk-substitute one food or recipe for another across the current selection — see [Substituting a Food or Recipe](#fooduse-substitute)
- **Settings**
    - Color theme
    - Personal profile (age, sex, weight, height, activity level)
    - Dietary preferences
    - Editor command
    - Advanced options: your personal [USDA](#gloss-usda) [API key](#food-data) (a free code from USDA's website that increases how many food searches you can do), and protein digestibility overrides

**Detailed how-to guides for each menu area follow later in this manual.** If you prefer to learn by example before reading explanations, skip ahead to [Sample Workflows](#sample-workflows) at the end of this introduction — it points you to a set of annotated walkthroughs.

### B. NutriMagnus addresses two serious problems

Thoughtful diet management requires trustworthy, specific data that is only to be found in research report summaries. Both access and use of this data requires use of computers. 

Managing specific dietary problems presents even greater challenges. One such specific problem is management of protein intake in vegetarian and vegan diets, especially when a person is no longer young. NuMa is particularly suitable for management of this problem, but can address others as well, focusing on oxalate consumption, need for vitamins and or minerals, phytonutrient tracking, and more. 

**Diet matters.** It is now well established that the crucial factors affecting physical and mental health are diet, sleep, exercise, social engagement, stress management, and avoidance of injurious and risky substances. Their relationships are complex and interacting. Relative to diet, research supports an emphasis on a "plant-predominant eating pattern". [^1] The fortunate thing about diet is that is something we act on immediately and effectively - but only if we have the information needed to make good choices.

**Plant-based diets are preferable.** There are multiple good reasons to focus on eating foods derived from plants rather than animals. Plant-based proteins are far less ecologically damaging to produce than animal protein and also much less likely to acquire agricultural chemical accumulations, which are then ingested along with the nutrients they contain. They also do not involve the industrialized abuse of vast numbers of animals who live only long enough to produce edible protein and then are treated like a mere object to be processed as we might a fallen tree. 

Plant proteins are usually more affordable and easier to ship and store for long periods. Most of the world, and most humanity throughout human history, eats and has eaten a plant-predominant diet, so this is simply not a novel idea.

**Plant-based proteins require special management.** But almost all plant proteins come to us with a built-in problem: incomplete amino acid composition. When you read on your jar of peanut butter (an excellent protein source) that 2 tablespoons contain 7 grams of protein (a bit more than that in a large egg), what it doesn't tell you is that only a bit less than 4 grams is actually digestible by human bodies, and of that only a little over 2 grams is [complete protein](#gloss-complete-protein) - the kind found in an egg or a piece of chicken meat, and the kind we need.

There are 9 protein building blocks (amino acids) that human bodies cannot make and must therefore ingest. Additionally, they must be ingested in specific proportions. When a food, or meal, or diet lacks or is insufficient in one or more of these "essential" amino acids this has a limiting effect on the utilization of the other 8. This is the "incomplete protein" problem that almost all plant proteins present.

Consider someone building a brick wall, where the plan calls for a fixed ratio of bricks to bags of cement — say, 50 bricks per bag. If they have 500 bricks but only 6 bags of cement, they can only build as much wall as 6 bags of cement allows; the other 200 bricks sit unused no matter how many more of them they buy. Buying more bricks doesn't help, because bricks were never what was running short *relative to the fixed ratio the plan calls for*.

This is the essential amino acid problem inherent in plant-based diets. The human body needs each of the nine essential amino acids in a fixed proportion to the total protein eaten — much like the bricks-to-cement ratio above. When a food, meal, or diet is short on one amino acid relative to that required ratio, the shortfall — not the total protein eaten — sets a ceiling on how much of that protein the body can actually use; the rest is broken down and discarded, like the unused bricks. (This required ratio is the [FAO 2013 Reference Standard](#fao) — see [Appendix B](#appendix-b) for the full technical explanation.)

While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24-hour period if the amino acid limitation problem is to be avoided. So, one way or another, one needs to tend to the issue of what is missing and where to find replacements to add it to one's diet in time.

**NuMa handles gracefully the tricky problem of managing plant-based proteins.** Few people know which foods have missing essential amino acids ([EAAs](#gloss-eaa)) or which have the needed excess [EAAs](#gloss-eaa) which would make them a good complement to eat with other foods lacking enough of those [EAAS](#gloss-eaa) in the same 24-hour period.

Beyond the problem of ingesting the right mix of amino acids, there are two other related dietary protein problems to be addressed:

* Protein in a food, however balanced or not, does no good if our bodies do not access it. Different protein sources in plant-based diets are metabolized in differing degrees of efficiency. This is the **[bioavailable protein](#gloss-bioavailable-protein)** problem.

* Age, sex, and activity level differences in protein needs do exist and they are not minor. Older people, active people, and those with chronic diseases, for example, require substantially more protein than do younger healthy people, for several reasons. Almost all common discussions of dietary protein fail to address this problem, and in any case a mere discussion doesn't tell one what to eat and how much.

### C. This protein-management problem is critical for older people and the chronically ill, and especially so for women

In very brief summary, as we age, we tend to lose muscle mass, utilize dietary protein less efficiently, and simply eat less. These factors compound to create a perfect storm of vulnerability to general ill-health and the often dire consequences of falls. And these issues affect women more than men. Put simply - getting enough of the right sort of protein matters far more than most people realize. A good diet is utterly necessary, but not by itself sufficient. It must be complemented with adequate resistance exercise.

There is very little discussion of the problem in the mass media. So, it is up to use as individuals to self-educate and then make carefully considered decisions about our diet. But this is almost impossible to do without serious technical help, as the nutritional factors involved go well beyond simple arithmetic or the naively simple view offered to us by the first major statements about plant protein complementarity in the very early '70s.

### D. NutriMagnus is the missing helper

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

Nutrition analysis programs, both paid and free open source, already exist but none that I've seen focus on the problems faced by vegetarian and vegan folks. And none have the rich features and readily modifiable design that I want. The NuMa program addresses both problems in detail. It also suggests complementary foods that can be combined with a food or recipe or meal to create [complete proteins](#gloss-complete-protein) in one's diet.

NuMa has been under intense development and is still being developed. Over time, new users will expertience unanticipated needs and the program can be further developed to meet them. This is one reason why [reporting problems](#feedback) is so important - feedback drives program development.

Very recently, a Windows version of the program has been developed. It will soon be available for download and user trials. 


### E. Data, testing, and validation: Why you can trust NutriMagnus (NuMa)

#### Reliable data sources

**[NuMa](#gloss-numa) draws on multiple data sources, and tells you which ones it is using.** Wherever the program makes a suggestion, it shows you which sources it consulted.

- **[USDA](#gloss-usda) FoodData Central**[^2] — the primary nutrient database, one of the most comprehensive public nutrition sources in the world. Used for most food searches.
- **Open Food Facts**[^3] — supplements USDA for branded and international foods, especially packaged products with a barcode.
- **Canadian Nutrient File** — Health Canada's reference database; particularly good amino acid coverage, which helps with DIAAS calculations.
- **UK CoFID** (Composition of Foods Integrated Dataset) — ~2,900 UK foods from Public Health England/DHSC; strong on macros, minerals, and vitamins, but has no amino acid data of its own.
- **Australian AFCD** (Australian Food Composition Database) — ~1,600 Australian foods from FSANZ; also has real amino acid coverage, like Canadian Nutrient File.
- **French CIQUAL** — ~3,200 French/European foods from ANSES; like CoFID, no amino acid data. 

See [Food data — where it comes from and how it is stored](#food-data) in Part 8 for more on all six of NuMa's sources.

In additions, the following internal data sources are used:

- **Harvard T.H. Chan School of Public Health oxalate table**[^11] — a 433-food reference table used to fill in [oxalate](#gloss-oxalate) content when [Oxalate data](#oxalate) is switched on in Settings. (This is optional and is off by default.)
- **Foster-Powell/Holt/Brand-Miller glycemic index table**[^8] — a published reference table used to fill in [Glycemic Index](#gi) estimates automatically, rather than requiring you to type them in from scratch.
- **NuMa's own curated protein-complement table**[^10] — a built-in list of 25 common protein sources used as a fallback for amino-acid data in complement suggestions, when your own data doesn't cover a gap.
- **Your own data** — foods saved to your [Pantry](#pantry), and [recipes you have analyzed](#recipes-menu-web), are consulted ahead of every other source above.


#### Extensive code testing

**[NuMa](#gloss-numa) has an extensive formal code test process.** As of this writing (2026-08-31), there are 753 formal tests that the program must pass after every significant change. The vast majority of these are "behavioral" tests which verify that pages, forms, and workflows all still work as they should. A smaller number are "computational validation tests" in which real-world data is fed into the program to make sure that the output matches known correct numbers. A third, newer tier is "property-based tests" — instead of checking a handful of hand-picked examples, these generate many random-but-plausible inputs (using the [Hypothesis](https://hypothesis.readthedocs.io/) library) and confirm that a mathematical rule holds for all of them, not just the cases someone thought to type in by hand. `tests/test_estimate_aa_properties.py` checks that the amino-acid-estimation scaling math preserves AA/protein ratios for any target/source pair, and `tests/test_diaas_properties.py` checks that [DIAAS](#gloss-diaas) scores and digestible-protein totals stay within their valid ranges for any ingredient list.

**The protein-complement suggestion engine has its own dedicated test coverage** — which foods are suggested to close an amino acid gap, how gap-cascade pairs are built, and how [DIAAS](#gloss-diaas)-boosting steps are ranked (`tests/test_complements.py` and the complement/pair tests in `tests/test_usda.py`, roughly 40 tests combined). The logic itself — what each suggestion tier does and how options are ranked — is explained in plain language in [Protein Complement Suggestions](#comp) through [Two-step combinations](#comb) in Part 4.

**The Claude AI fetch/import workflow also has its own dedicated test coverage** — prompt building, response parsing (fenced and bare JSON, malformed-JSON warnings), per-block validation, and the per-serving-to-per-100g label conversion arithmetic (`tests/test_claude_fetch.py`, 24 tests), plus the two web routes behind it (`tests/test_web.py`, 5 tests). See [Fetching missing amino acid data with Claude AI](#fetch) in Part 3.

#### Validation you can replicate yourself

**Appendix K has a fully worked out validation example.** You can do this yourself, if you like. Data are brought in from outside the program and run through the official correct computation process. Full source references are given. You can run the same computation in [NuMa](#gloss-numa) and compare the result.

#### Reasonable expectations: bugs remain

**Problems may appear anyway.** As professional programmers will tell you, all programs have bugs. This is more likely for new ones than for those which have been around for years. This is why you should report any result you are getting which doesn't make sense to you. There is a small chance you've found a "bug", but a greater chance that the program simply needs to explain itself to you more clearly. Either problem will be fixed ASAP, and all such fixes benefit everyone who uses the program.

**How to report suspected errors or problems with the program:** see [Getting more help](#feedback) in Part 8.

---

### F. Sample Workflows {: #sample-workflows}
**If you'd prefer to learn by example before reading explanations,** fully worked, step-by-step walkthroughs are provided later in this manual — see [Sample Workflows](#sample-workflows-web) in Part 3. You don't need to read Part 4 or Part 5 first.

---

## Part 3 — Using the Web App
NuMa's web app runs in your ordinary browser. This makes program development, which is ongoing, easier, and also provides the user with an interface they are already at least partly familiar with.

### A. Opening NutriMagnus

Launch NuMa the way it was set up on your computer — a desktop icon, an Applications-menu entry, or a shortcut someone set up for you. It opens automatically in your browser, normally at a browser address like `http://127.0.0.1:8000` — this just means "this computer, talking to itself," not an address on the internet, so don't worry if the exact numbers you see differ. If the page doesn't load right away, wait a few seconds and reload — the program is still starting up.

#### What you see on the home page {: #home-page-tour}

Right below the **Welcome to NutriMagnus** heading is a small block of status lines:

- **Dietary preferences** — your current setting (e.g. "All animal foods"), with a link straight to Settings to change it.
- **Active profile** — a one-line summary of your profile (age, sex, weight, height, activity level), or "not set" with a link to configure one if you haven't yet.
- **Current version date** — the exact build you're running, as `yyyy-mm-dd:hhmm`. Whenever `version.py`'s build note is set, it follows in parentheses as "(Version note: ...)" — a short plain-language description of what changed in that build.

Above all of that, a few one-time or conditional banners can appear when relevant: a database-integrity warning, an "update installed" confirmation right after using Update Now, an update-failed message, and an **UPDATE AVAILABLE** banner when a newer release exists on GitHub (with an **Update Now** button if you're running the packaged Linux install, otherwise a plain link to what's new). That banner repeats the build note as its own line, plus a note on how often you're being notified about new releases and a link to change that in **Settings → Update Notifications** (daily, weekly, or monthly — daily by default).

**When does NuMa actually check for a new release?** Every time the home page loads — at launch, on a manual reload, or by navigating back to it from anywhere else in the program — it asks whether a newer version exists. That check itself is cached for a few hours, so bouncing back to the home page repeatedly doesn't re-contact GitHub every time; it just reuses the last answer until the cache expires. Separately, even when a newer version genuinely is available, whether the **UPDATE AVAILABLE** banner is actually shown to you on a given visit is throttled again by your daily/weekly/monthly notification-frequency setting — so you won't see it more often than you asked to.

### B. Finding your way around

Every page has the same navigation bar across the top: **NuMa** (takes you home), **Foods**, **Recipes**, **Meals & Log**, **Analysis**, **Settings**, and **Manual** (this document). **Foods** and **Analysis** open as drop-down menus with several choices each; the others go straight to their page.

If you are using the Firefox browser and you'd rather use the keyboard, each nav item has a shortcut — hold **Alt+Shift** and press the item's first letter (`F` for Foods, `R` for Recipes, `M` for Meals & Log, `N` for Analysis, `S` for Settings, `A` for Manual), using the underlined letter shown in each menu item and Settings section heading (e.g. `Alt+Shift+3` jumps to Dietary Preferences within Settings). For a dropdown menu item (Foods, Analysis), the shortcut also moves keyboard focus straight to the first item in the menu that opens — from there, ArrowUp/ArrowDown moves between items, Enter or Space picks one, and Escape closes the menu, all without touching the mouse. This is a browser-side feature — it is unrelated to, and does not affect, anything stored in your NuMa data. Turn it on or off in **Settings → Keyboard Shortcuts**; the setting is stored in your browser (not synced across devices) and takes effect immediately, with no page reload needed.

Most detail pages (a food, a recipe, a meal) show a collapsible outline down the side — click a heading there to jump straight to that section. Forms that have unsaved changes mark their Save button so you can tell at a glance whether you've edited something, and the browser will warn you before you navigate away from an unsaved form.

#### Search boxes remember your last search {: #search-memory}
On a meal's "Add Food or Recipe" search, a recipe's "Add Ingredient" search, and the Foods: Search page, if you follow a link away to look something up elsewhere and then come straight back to that exact page, your last search and its results are restored automatically — you don't have to retype it. This only applies to a plain link back to the page (the browser's own Back button already preserves it); it's scoped per page, so it never leaks a search from one meal into another.

There's no time limit on this — it holds for as long as your browser tab stays open, not just for a moment after you step away. Clicking **Clear search** (shown next to the search box whenever a search is active) or closing the browser tab clears it back to the page's clean, empty-search state.

The main navigation bar goes further than any one page: clicking **Recipes**, **Meals & Log**, **Settings**, or **Manual** returns you to the exact page you were last on in that section — e.g. the specific recipe you were editing, search and all — instead of always landing on its list page. When that memory is what brought you back, the page's breadcrumb is highlighted, with a one-click "All recipes" / "All meals" link in case you actually wanted the plain list. **Foods** is a drop-down of separate destinations (Search, Compare, Pantry, and more), so it works a little differently: a small "↩" quick-return link appears next to it whenever there's a food you've viewed, showing that food's name, so you can jump back to it in one click after wandering off elsewhere. Following a breadcrumb link (e.g. **Recipes** at the top of a recipe page) back to the list always starts fresh, clearing any remembered search or position.

### C. Sample Workflows {: #sample-workflows-web}
**Use this as a tutorial!** With NuMa open in your browser, work through these step by step, paying close attention to what appears on your screen. Each workflow is self-contained — you don't need to read Part 4 (nutrition concepts) or Part 5 (reference) first; terms are briefly explained in place.

**Workflows 1–3 are a single connected thread, not a tour of every menu.** They follow one feature end to end — protein complementarity — because it's NuMa's most distinctive capability. Right after them, a short "a few more things worth trying" section highlights a few other Foods and Recipes features these three don't touch, and Workflow 4 does the same connected-thread treatment for Meals & Log paired with Analysis.

---

#### Workflow 1 — Looking up a single food and finding its protein gaps

**What this shows:** how to search for a food, read its nutrient profile, and get automatic protein complement suggestions drawn from the built-in protein source list.

**Step 1 — Open the Foods menu.** Click **Foods** in the top navigation bar. A dropdown appears with ten numbered items.

**Step 2 — Search for a food.** Click **2. Analyze a food portion**. A search box appears. Type `brown rice cooked` and click **Search**. NuMa queries [USDA](#gloss-usda) FoodData Central and returns a ranked list of matches. Click the Foundation Foods entry — Foundation Foods have the most complete amino acid data.

**Step 3 — Choose a portion.** The food detail page opens. Near the top you will see a portion input field. Type `1 cup` (or select it from the named portions dropdown if it appears) and click **Recalculate nutrients**.

**Step 4 — Read the nutrient table.** The page now shows the full nutrient profile scaled to your chosen portion. Click the **Nutritional Analysis** section header to expand it — you will see macronutrients, minerals, vitamins, and amino acids.

**Step 5 — Read the protein quality section.** Click **Protein Quality** to expand it. NuMa shows a per-amino-acid score table. Brown rice is low in lysine — its lysine score will be well below 1.0 (the [FAO](#gloss-fao) reference floor). This is the [limiting amino acid](#gloss-limiting-amino-acid).

**Step 6 — Read the complement suggestions.** Click **Protein Complement Suggestions** to expand it. Because a gap exists, NuMa lists the amino acid(s) you're short on under **Gaps**, then shows foods that can close them under a **Suggestions** heading (or **Other options** if pantry items also qualified — see Step 5 of Workflow 2). Suggestions are ranked by smallest amount needed. You might see, for example, that adding 45 g of lentils would close the lysine gap and bring the combined protein to a complete profile.

**What you learned:** NuMa can tell you BOTH what is in a food AND what is missing — and exactly what to add to fix it.

---

#### Workflow 2 — Analyzing a meal with pantry items as complement candidates

**What this shows:** how recording your own protein sources in the Pantry makes complement suggestions personal and practical, drawing on foods you actually have.

**Before you start, set up your profile.** Click **Settings**, fill in your age, sex, weight, height, and activity level, and save. This is what lets NuMa compare your protein intake against a target built for you, rather than a generic default — you'll see it reflected in the % goal figures later in this workflow and in Workflow 4.

**Step 1 — Add a food to your Pantry.** Click **Foods** in the navigation bar, then click **7. My Pantry**. On the Pantry page, type `hemp seeds` into the search box under "Add a pantry item — search for full amino acid data" and click **Search**. A results table appears — click **Add to pantry** next to the best match. (The separate "Quick add by name only" box further down the page skips the search and saves just the name, with no nutrient data — use it only when you can't find a match.)

**Step 2 — Create a meal.** Click **Meals & Log** in the navigation bar. Click **New Meal**, give it a name (e.g., "Lunch today"), and a date. The meal page opens with a search box. Type `brown rice cooked`, click **Search**, then click the matching food and enter `1 cup` as the portion. Repeat with `black beans cooked` at `½ cup`. Both foods now appear in the meal's item list.

**Step 3 — View the meal's nutrition analysis.** Scroll down on the meal page. The **Nutritional Analysis**, **Meal-Level Protein Analysis**, and **Protein Complement Suggestions** sections are collapsed by default — click each header to expand it. NuMa aggregates the nutrients across both foods and shows a combined profile.

**Step 4 — Read the protein analysis section.** Rice and beans together improve each other's amino acid profile significantly — this is protein complementarity in action. The combined score will be higher than either food alone.

**Step 5 — Read the complement suggestions.** Because you now have a pantry item, the suggestions are organized into two headings: **From your pantry & recipes** (hemp seeds will appear here if it qualifies as a gap-closer for this meal) and **Other options** (the same built-in list from Workflow 1). Suggestions drawn from your pantry reflect a food you actually have, not just a theoretical option.

**What you learned:** Building even a small pantry of protein sources you keep on hand transforms complement suggestions from generic advice into a practical shopping and cooking guide.

---

#### Workflow 3 — Using an analyzed recipe as a complement candidate

**What this shows:** how recipes you have analyzed become available as complement options for other foods and meals, so NuMa can suggest "add 250 g of your lentil soup" rather than just "add lentils."

**Step 1 — Create and analyze a recipe.** Click **Recipes** in the navigation bar, then click **New recipe**. Give it a name such as "Lentil soup" and fill in the servings count. On the recipe edit page, add ingredients one at a time — for example, lentils (200 g), onion (80 g), garlic (10 g), and vegetable broth (500 g). Save the recipe details, then add each ingredient via the ingredient search box. The recipe detail page shows its Nutritional Analysis and [Complete Protein](#gloss-complete-protein) Analysis, computed automatically. Expand those sections to see the full protein profile and [DCP](#gloss-dcp).

**Step 2 — Look up a food with protein gaps.** Click **Foods** in the navigation bar, then click **2. Analyze a food portion**. Search for `corn tortilla`. Click the result, then enter `46 g` (about 2 tortillas) in the portion field and click **Recalculate nutrients**. Expand **Protein Quality** — corn is low in lysine and tryptophan.

**Step 3 — Read the complement suggestions.** Expand **Protein Complement Suggestions**. Under **From your pantry & recipes**, your lentil soup recipe appears as a candidate, tagged `(#id, Recipe)` next to its name so you can tell it apart from a plain food. NuMa shows how many grams of the recipe would close the gaps in the corn tortillas — for example, "Serve alongside: 180 g."

**Step 4 — Note what changes as you build up data.** The more recipes you analyze and the more pantry items you add, the more the complement suggestions reflect your actual kitchen — each qualifying recipe or pantry item appears as its own candidate card under **From your pantry & recipes**.

**What you learned:** NuMa's suggestions become progressively more useful as you add your own data. The built-in list ensures you always get suggestions even on day one; your pantry and recipes make those suggestions yours.

---

#### A few more things worth trying

Workflows 1–3 follow one thread — protein complementarity — since it's NuMa's most distinctive feature. A few other things worth a look, once you've got the basics down:

**Foods → Compare.** Add up to eight foods side by side in one table (checkboxes in the search results, a gram amount for each) — a quick way to answer "which of these is actually better for me" instead of flipping between separate detail pages. A comparison can be saved under a name and reopened later.

**Foods → Custom food profiles.** Enter a homemade dish, a supplement, or a product NuMa's databases don't have (or have incompletely) — either from scratch, or by copying an existing cached food as a starting draft and editing its nutrients from there.

**Recipes: use one recipe inside another.** A recipe can be added as an ingredient of another recipe — a lentil sauce used inside three different dinners, say. Editing and saving the base recipe keeps every recipe built on it up to date automatically — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 6.

**Recipes → Archive/Restore.** Hide a recipe (or a food, or a pantry entry) you're not using right now without deleting it — see [Archiving](#archive) in Part 5.

---

#### Workflow 4 — Logging several days, then spotting a pattern in Analysis

**What this shows:** how Analysis turns a handful of logged days into something a single meal — or even a single day — can't show you: a full day's combined nutrition, and a pattern across many days.

**Step 1 — Log a couple more days.** Click **Meals & Log → New Meal** and create two or three more meals across two or three different dates — reuse foods from Workflows 1–3 if you'd like to keep it quick (`brown rice cooked`, `black beans cooked`, `corn tortilla`).

**Step 2 — Analyze a full day.** Open any one of the meals on a date where you logged more than one — a button reading **Analyze full day (N meals)** appears near the top of the page whenever that's the case. Click it. NuMa pools every meal logged that date into one combined analysis — total nutrients, pooled protein quality, and complement suggestions across everything you ate that day, rather than meal by meal.

**Step 3 — Check the Daily Summary.** Click **Analysis → 1. Daily summary**. The Recent Days table lists every date you've logged: Day DCP, then Protein, Calories, Carbs, and Fiber (built in for every day, right after Day DCP), then your goal in grams and % of it. Click any date to reopen that day's full analysis.

**Step 4 — Catch a chronic pattern with Multiday Nutrient Trend.** From the Daily Summary page, click **Multiday nutrient trend** and choose a 7, 14, or 30-day window. NuMa averages your intake over that window and compares it to your RDA targets — surfacing a nutrient that's persistently a little low, the kind of gap a single good or bad day would hide.

**Step 5 — See the shape of it with Nutrient Plot.** Click **Nutrient plot** instead. Check Day DCP and Protein (or any other nutrient you're curious about), then click **Plot**. NuMa draws a line chart across your logged days — sometimes a shape on a chart makes a pattern obvious in a way a table of numbers doesn't.

**What you learned:** Analyzing a full day rolls up everything you ate; Daily Summary tracks that day by day; Multiday Trend and Nutrient Plot turn many days into a pattern you can act on — two different views (numbers-against-target, and shape-over-time) of the same underlying data.

---

### D. Using the Foods menu

#### Search (Foods → Search)

Type any part of a food name, an [FDC ID](#gloss-fdc-id) number, or a 12/13-digit barcode (UPC-A or EAN-13) — see [Your own data is always checked first](#search-ranking) in Part 6 for how results are sourced and ordered. Next to the search box, a row of Source checkboxes (Pantry, Food Cache, Recipes, USDA, Open Food Facts) lets you narrow results to any combination of sources before or after you search — see [Source filter](#food-search) in Part 6 for details. Click a result to open its full [Nutritional Analysis](#nutrients), [Protein Quality](#protein-quality), and complement-suggestion page.

#### Analyze a food portion / Analyze a saved recipe portion

Shortcuts into Search that take you straight to entering an amount once you've picked a food or recipe, rather than seeing the per-100g view first.

#### Convert

A pure unit-conversion tool — search for a food (with the same [Source filter](#food-search) as every other search box), then type any amount (`3 oz`, `1/4 cup`, `150 g`) to see its gram/mL equivalent and the closest named portion size. No nutrient analysis is shown here; use Search for that.

#### Compare

Add up to eight foods (checkboxes in the search results, filterable by [Source](#food-search) the same as any other search) and set a gram amount for each to see them side by side in one nutrient table. Comparisons can be saved under a name and reopened later, renamed, or deleted.

#### Food Cache {: #food-cache-web}
Every food NuMa has ever fetched from USDA or Open Food Facts[^3] lives here — see the [Food Cache column guide](#cached) in Part 5 for what each column means. Per-food actions: **Portions** (add or edit named portion sizes), **Refresh** (re-fetch nutrient data from USDA while keeping your portions and notes), **Archive/Restore** ([hide without deleting](#archive)), and **Delete** — refused if a pantry entry, recipe, or meal still uses that food, since deleting it anyway would leave that entry pointing at nothing; the refusal names and links every blocking pantry entry, recipe, and meal by id (e.g. "pantry: 34 | recipe: 12 | meal: 9, 72") so you can go straight to the place to remove or replace it, or use Archive instead. **Prune unused foods** removes cache entries no pantry entry, recipe, or meal is currently using — with a checkbox per food (checked by default) so you can uncheck anything you'd rather keep before pruning. Each row also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) above — for jumping straight into [Compare Foods](#food-comparison) with the checked items.

**Check database integrity.**{: #db-check} Scans for pantry entries, recipe ingredients, or logged meal items that still point at a food or recipe no longer in the cache — leftover from before Delete started refusing to remove still-used foods, or from a manually edited database file. Opening a food page for one of these fails, since NuMa treats the missing food as never-cached and tries to re-fetch it from USDA by ID — which errors outright for an Open Food Facts food (its ID isn't a real USDA ID) and can return the wrong food for a reused-looking one. The check page lists every problem found, grouped into up to five kinds, **each with its own fix button and a plain-language note on what that fix actually does** — they're kept separate because the consequences are not equivalent:

- **Pantry entries** — low impact; removing one only takes it off your pantry list.
- **Recipe ingredients** — removing one deletes that ingredient line from its recipe; the recipe's nutrient totals recalculate without it.
- **Logged meal items** — removing one deletes that food/recipe from a day's logged meal history; that day's totals recalculate without it, same as if it had never been logged.
- **Sub-recipe references** — non-destructive; nothing is deleted, the ingredient is just flagged "recipe (deleted)" (the same label used everywhere else a referenced recipe is gone) instead of erroring.
- **Unreadable nutrient/portion data** — never auto-repaired; each food gets its own **Refresh** (re-fetch from USDA) and **Delete** buttons so you decide.

**Fetching missing amino acid data with Claude AI.**{: #fetch} Some foods — especially branded or prepared items — arrive without amino acid data. Check the boxes next to the foods you want (or click "Select all missing AA data" to grab every food currently missing it), then click **Fetch missing data from Claude AI**. This builds a ready-to-send prompt and shows it on its own page with a **Copy prompt to clipboard** button. From there:

1. Go to [claude.ai](https://claude.ai) — open a **new chat** (not an existing one) — paste the prompt, and send.
2. When Claude finishes, copy its entire reply (all of it, including every fenced `json` block — if Claude splits its answer across multiple messages, copy each one and paste them together).
3. Back in NuMa, click **Import Claude response** (also reachable directly from the Food Cache page), paste the reply into the box, and click **Review**.
4. NuMa shows you a table of what it understood from the reply — name, FDC ID, calories, protein, and how many of the 11 tracked amino acids were found — plus any warnings about data it couldn't use. Check it over, then click **Import** to save it to your cache.

#### My Pantry

Foods you keep on hand — see [My Pantry](#pantry) in Part 5 for the column guide. Pantry foods are checked first for complement suggestions and search results. Add a food with full nutrient data via search (with the same [Source filter](#food-search) as every other search box), or use **Quick add by name only** for something you haven't looked up yet (link it to real data later with **Link a food**). Only the search-and-select route caches the food — see [Only a search-and-select adds a food to your Food Cache](#pantry) in Part 5. Searching for a food already in your pantry shows a **Remove from pantry** button right on its search-results row, so you don't need to scroll down to find the matching row in the pantry list to take it out. Each pantry item with a linked food also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) above — for jumping straight into [Compare Foods](#food-comparison) with the checked items; a quick-add item with no linked data can't be compared.

#### Custom food profiles

Create a food NuMa doesn't already have — a homemade dish, a supplement, or a product with an incomplete database entry. Either start from scratch, or **copy a cached food as a draft** and edit its nutrients from there — both of the page's "copy from another food" searches have the same [Source filter](#food-search) too, and can now reach Open Food Facts as well as your cache and USDA. See [Entering custom foods and dietary supplements](#custom-foods) below.

#### Annotate

A list of cached foods where you can enter a glycemic index estimate, a [DIAAS](#gloss-diaas) estimate, prep-context notes, or check "don't ask again" for a specific nutrient. NuMa also opens this automatically as a follow-up prompt right after certain actions when data is missing — you can skip it for now or skip it permanently for that food.

### E. Opening a food's detail page

A food's page shows, in order: **Protein Summary** (DCP), **Nutritional Analysis** (type any amount, or pick a named portion, then click **Recalculate**), **Protein Quality** ([DIAAS](#diaas) and the per-amino-acid table), **Anti-nutrients**, **Complement Suggestions** (pantry foods first, then general suggestions, then two-food pairs and combos — each can be [ignored and recalculated](#ignore-complement)), and an **Add to Pantry** form at the bottom. If the food has no amino acid data, you'll see a suggestion to search for a Foundation or SR Legacy equivalent instead — those datasets are the ones most likely to have complete amino acid profiles.

### F. Using the Recipes menu {: #recipes-menu-web}
The **Recipes** page lists every recipe, with filter/sort options and a **Show archived** checkbox. Row actions: **Edit**, **Copy**, **Archive/Restore**, **Delete**. **Recompute DCP for all recipes** refreshes every recipe's protein score at once, and **Broken recipe references** finds any recipe whose sub-recipe ingredient was since deleted — see [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) in Part 6. Each row also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) in Part 5 — for jumping straight into [Compare Recipes](#recipe-comparison) with the checked recipes.

Editing a recipe's ingredients or servings recalculates its own [DCP](#gloss-dcp) automatically, and cascades to every recipe that depends on it too — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 6. You don't need **Recompute DCP for all recipes** just because you changed one recipe; it's there for after a bulk import, or if you suspect stale numbers from before this cascading recalculation existed.

- **New recipe** — a short form (name, description, servings, total yield) that drops you straight into editing.
- **Edit** — a details form plus an ingredients table. The details form includes an **Introduction** field, right after Ingredients, for background — where the recipe came from, why you like it, serving notes — anything that isn't the step-by-step procedure. Add an ingredient by searching — the results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns and the "Fetch full details for selected" AA-confirmation button — then typing a portion (`150 g`, `1/2 cup`, or a saved preset like `p1`); reorder ingredients with the up/down controls, or edit or remove one inline. A **Running totals** card at the side updates live as you add ingredients, showing calories, protein, and DCP for the whole recipe and per serving.
- **Detail** — mirrors a food's detail page (Introduction right after the title, Protein Summary, Ingredients, Procedure, Nutritional Analysis, [Complete Protein Analysis](#meal-diaas) with per-ingredient digestibility, Missing AA Profiles, Complement Suggestions — [ignorable and recalculable](#ignore-complement) here too, [Glycemic Load](#glycemic), Anti-nutrients), plus a servings field to re-analyze at a different batch size. **Print/save recipe** opens a stripped-down, print-friendly version in a new tab, with Introduction included as one of the "Include on this printout" checkboxes.

### G. Using the Meals & Log menu

The **Meals & Log** page has a **New Meal** form at the top (name + date), filters for date and sort order, a **Search meal history** link for full-text search across everything you've ever logged, and a batch button to calculate DCP and calories for all meals, or just the last 10 or 30 days. The list itself shows each meal's completeness, item count, Meal DCP, Day DCP (combined across all meals on that date), % of your daily goal, and calories.

Open a meal to add foods or recipes (search box at top — for a recipe you can log the whole thing or just individual ingredients), edit or remove items inline, mark the meal complete/incomplete, rename it or change its date, or merge it with other meals logged the same day. Below the item list: [Nutritional Analysis](#nutrients), [Meal-Level Protein Analysis](#meal-diaas) (with a **Refresh from USDA** button if amino acid data needs updating), Missing AA Profiles, Complement Suggestions ([ignorable and recalculable](#ignore-complement)), [Glycemic Load](#glycemic), and Anti-nutrients.

If more than one meal is logged on the same date, **Analyze full day** rolls all of them into one combined analysis — total nutrients, pooled protein quality, and complement suggestions across everything you ate that day.

### H. Using the Analysis menu

- **Daily summary** — a table of recent days with Day DCP and % of goal; pick a date to see that day's full analysis (same sections as the full-day meal view). From here, follow the **Multiday nutrient trend** link to see 7/14/30-day averages — useful for catching a chronic shortfall that a single good or bad day would hide.
- **Food use in meals** — see how often you've eaten a given food or recipe. Choose either a date range or a specific list of meal IDs, optionally limit results to protein-containing foods, and get a sortable table with a visual frequency bar.
- **Food use in recipes** — the same idea, but for your recipe book: see how many of your recipes use a given food or sub-recipe as an ingredient. Choose all recipes, a date-created range, or a specific list of recipe IDs.

Both Food Use pages have a **Substitute a food or recipe** panel for bulk-replacing one food or recipe with another across whatever's currently selected — see [Substituting a Food or Recipe](#fooduse-substitute).

### I. Using the Settings menu {: #settings}
Settings is organized into collapsible sections: **[Your Profile](#profile-setup)** (age, sex, weight, height, activity level — this drives all your daily nutrient targets — plus a checkbox enabling [oxalate](#oxalate) lookup), **Computed Daily Targets** (see [Part 6](#daily-nutrient-targets)), **Dietary Preferences** (affects complement suggestions, [B12/iron/zinc guidance](#diet-bioavailability), and — see [Dietary Preferences](#diet) — every search and lookup in the program), **Keyboard Shortcuts**, **USDA API Key** (lets you use your own free personal code from USDA's website instead of the one NuMa shares with every user by default, so your searches are less likely to get temporarily blocked when many people are using NuMa at once — see [Food data](#food-data) for how to get one; also has the [search result depth](#search-ranking) setting), **Protein Digestibility Overrides** (custom digestibility numbers for specific foods), **Nutrient Targets** (optional per-nutrient [Revised Optimal (Recent Research)](#optimal) targets and [Max limits](#maxlimits), with a one-click button to load recommended defaults), **Starter Data** — see below, and **System Issues** — see [below](#system-issues-howto).

#### Your Profile {: #profile-setup}
Age, sex, weight, height, and activity level. This is the one form that everything else in NuMa's nutrient-target system depends on: your [RDA](#rda) values (Part 5, Section P), the age/sex-adjusted [Daily Nutrient Goals](#goals) (Section Q), and — where you've set them — your [Revised Optimal targets](#optimal) and [Maximum Nutrient Limits](#maxlimits) all key off the age, sex, weight, height, and activity level you enter here. Also on this form: a checkbox enabling [oxalate](#oxalate) lookup, off by default.

Leave this form empty and NuMa still works — you can search, log, and analyze foods and recipes — but every nutrient table's "% of daily target" column is blank, since there's no profile to calculate a target from. Fill it in whenever you're ready; every already-logged meal is re-evaluated against your new targets immediately, nothing needs to be re-entered.

#### Starter Data {: #starter-data}
A small set of curated content — real USDA foods (with full amino-acid data), a few of them in your pantry, and two recipes picked to show protein complementarity actually working — "* Black Beans & Rice" and "* Lentils & Oats Bowl," each combining a legume and a grain so the amino acids each is short on are covered by the other. Their names all start with `* ` so you can always tell them apart from anything you've added yourself. A brand-new install loads this automatically the first time you launch it, so your Food Cache, Pantry, and Recipes aren't empty on day one — this section is for anyone who cleared it and wants it back, or an existing install that never had it.

Loading starter data never touches anything already in your cache, pantry, or recipes — it's tracked separately so **Clear starter data** (which appears once it's loaded) removes exactly what was added, nothing else. Loading again while it's already loaded is a no-op.

#### Computed Daily Targets

This section of Settings shows your personalized nutrient targets. See [Your computed daily nutrient targets](#daily-nutrient-targets) in Part 6 for what it contains and how it's kept current.

#### System Issues {: #system-issues-howto}
Every recipe caches its protein-quality score (DCP) so it doesn't have to be recalculated every time you view it. Whenever a food or recipe changes — editing a food's nutrients, bringing in amino acid data via "estimate it from a similar food," refreshing a food from USDA, editing a recipe's ingredients — NuMa automatically recalculates DCP for every recipe that depends on the thing that changed, including recipes-of-recipes, all the way up the chain. You never have to trigger this yourself.

**System Issues is where NuMa tells you when that automatic recalculation itself broke.** This is not the same as a recipe showing "NC" (not computed) — NC just means DCP genuinely can't be calculated yet (a significant ingredient is missing amino acid data, or the recipe has 0 servings), which is an expected, normal state and isn't logged here at all. System Issues is specifically for the rarer case where the recalculation *should* have run and produced a real answer, but something went wrong internally (a software error) — the kind of failure that would otherwise silently vanish and leave a recipe's protein score stale with no indication anything was ever wrong.

Each entry shows when it happened, which recipe it affects, and the error itself. Click **Retry** to have NuMa recompute that recipe's DCP again right now:

- If the retry succeeds, the entry clears — you'll see a confirmation, and the recipe's DCP is now current.
- If it fails again, the entry stays (with a fresh error message) and NuMa tells you so — Retry never just makes an entry disappear while the recipe underneath it is still broken. A repeat failure usually means a real bug that needs fixing in the code, not something you can resolve by clicking around; consider reporting it.

If you'd rather fix the underlying recipe yourself instead of using Retry, re-editing it (or opening it and saving again) triggers the same recalculation that Retry does, and clears the System Issues entry the next time it succeeds.

A one-time banner also appears on the home page whenever there's a System Issues entry you haven't seen yet, with a **Got it. Don't remind me again.** checkbox — checking it hides the banner (the entry still stays listed under Settings until it's actually resolved), and any *new* failure after that brings the banner back.

**The home page also checks GitHub for a newer NuMa release**, showing an **UPDATE AVAILABLE** banner with a link to what's new if one exists. This check is quick (a couple of seconds at most) and fails silently if you're offline or GitHub is unreachable — it never blocks the home page from loading. See [What you see on the home page](#home-page-tour) for exactly where the current build's version stamp and build note appear, how often the check itself runs, and how the **Settings → Update Notifications** frequency setting controls how often the banner is shown.

**If you installed NuMa via the Linux installer, the banner also has an Update Now button** that downloads and installs the new version for you — no terminal, no manual download. Click it, confirm, and NuMa fetches the latest release and swaps itself in place; your data is completely untouched (it lives in a separate location the update never touches). You'll see a message telling you to close the browser tab and relaunch NuMa once it's done — the version you're currently running keeps working right up until you do. If you're running NuMa from source instead (a developer checkout), the button doesn't appear — you'll see the plain "what's new on GitHub" link instead, since there's no packaged install for it to replace.

### J. Entering custom foods and dietary supplements

Go to **Foods → Custom food profiles → Create**. See [Entering custom foods and dietary supplements](#custom-foods) in Part 6 for the fields, the supplement/tablet mechanism, and the barcode-first tip — they work identically here.

### K. A note on amino acid data

New foods are cached automatically the first time they turn up in a search, comparison, or pantry lookup — no separate import step needed. If a food is still missing amino acid data, you'll see a **Refresh** button (Food Cache) or a **Refresh from USDA** link (a meal's Protein Analysis section) to re-fetch it, and wherever data is missing you'll usually see a suggestion to search for a Foundation or SR Legacy equivalent instead. You can also enter GI or DIAAS estimates yourself via **Foods → Annotate**.

---

## Part 4 — Core nutrition concepts {: #coreNutrition}
### A. Essential Amino Acids {: #aa}
Amino acids are the building blocks of protein. Nine of them are "essential", for our bodies cannot make them, so they must come from food every day:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and Phenylalanine respectively. NuMa evaluates [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr) as combined pairs when scoring protein quality, following [FAO](#gloss-fao) 2013 guidelines.

See [Protein Completeness](#complete) and [Amino Acid Gaps](#gap) for how completeness is scored and what a gap means.


### B. Protein Complement Suggestions {: #comp}
When amino acid gaps are detected, NuMa suggests foods that can improve the protein quality of the base food or meal. Two separate tiers are shown, and they use different methods:

#### TIER 1 — GAP CLOSERS

These foods can mathematically close a specific amino acid gap with a practical amount (up to 500 g). A gap closer has a high enough ratio of the [limiting amino acid](#gloss-limiting-amino-acid) to protein that adding it to the base food brings that amino acid's score to 1.0 (the [FAO](#gloss-fao) reference floor).

Each suggestion shows:
  - Grams to add
  - Which gaps it closes, with scores before and after
  - Digestible protein added
  - Total bioavailable [complete protein](#gloss-complete-protein) — the base food protein plus the complement protein, multiplied by the combined (pooled) [DIAAS](#gloss-diaas) of the pair. This is higher than just adding each food's individually-digestible protein, because the complement's amino acids improve the usability of the base food's protein too.

#### RANKING

Options are ranked by the smallest practical amount needed, with one refinement: an option that fully completes the amino acid profile is moved to the front — but only if its serving size is 50 g or less. An option requiring 90 g to achieve completeness will not outrank a 7 g option that merely closes the primary gap. This prevents a food with a barely-adequate amino acid ratio (just above the [FAO](#gloss-fao) reference) from dominating the list simply because adding large quantities of it eventually fixes every gap.

#### TIER 2 — DIAAS-BOOSTING OPTIONS

Sometimes the digestibility of the base food is low enough that no practical amount of any single food can "close the gap" mathematically. This happens when the food's raw amino acid ratios are already near the [FAO](#gloss-fao) reference — the gaps are digestibility-driven rather than composition-driven. Adding even a very good complement raises the pool's digestible amino acids but can't fully overcome the base food's own digestibility penalty via the gap-closer formula.

For those situations, [DIAAS](#gloss-diaas)-boosting options are shown instead. These foods raise the combined meal [DIAAS](#gloss-diaas) score toward 0.90 by contributing digestible amino acids that pool with the base food's amino acids. The calculation uses each food's own true [ileal digestibility](#gloss-ileal-digestibility) (not just the [DIAAS](#gloss-diaas) score), so a high-digestibility food like soy protein isolate (95%) contributes disproportionately more digestible amino acids than its raw content alone would suggest.

Each [DIAAS](#gloss-diaas)-boosting suggestion shows a progression of serving sizes — 15 g, 30 g, 60 g, and up to 120 g (roughly 1/2 cup) for meal, food, and daily-summary analyses. Each step shows the meal [DIAAS](#gloss-diaas) before and after adding that amount, so you can choose a realistic portion rather than being given a single impractically large target. Recipe analysis uses larger steps (up to 300 g) because recipe quantities serve multiple people.

#### TIER 3 — TWO-FOOD COMBINATIONS

When a single food can close the primary gap but in doing so dilutes another borderline amino acid, a two-food combination is offered. The logic follows a gap-cascade:

  Food A closes the primary (most-limiting) gap. It may open a smaller secondary gap by diluting a borderline amino acid that was already close to the threshold.

  Food B is chosen specifically to close whatever gap Food A left behind, without opening further gaps.

Together the pair clears all amino acid gaps. The output shows the individual gram amounts for each food, the cumulative amino acid effects, and whether the combination achieves "closes all gaps" status.

Three combinations are shown initially. The app offers to show more if available.

Combinations are ranked by total weight (lighter is ranked first), with combinations that close all gaps ranked above those that do not.

#### WHICH TIER IS RIGHT FOR YOU?

If single-food gap closers (Tier 1) are available, they are the most targeted choice: they fix a specific deficiency with a single food.

If single-food options open a secondary gap, Tier 3 two-food combinations show how to close everything in one practical step.

If only [DIAAS](#gloss-diaas)-boosting options are shown (Tier 2), the underlying problem is that the base food is not highly digestible. Adding a well-digested, amino-acid-rich food improves the overall protein quality of the meal even without closing any single gap definitively. This is nutritionally meaningful — a meal [DIAAS](#gloss-diaas) of 0.90 means 90% of the protein is both complete and digestible.

You do not need to eat [complement foods](#gloss-complement-food) at the same meal — meeting daily totals is sufficient for healthy adults. See also [DIAAS](#diaas) and [limiting amino acid](#gap) for background.

#### RECIPE ANALYSIS: AMOUNTS ARE SIZED TO THE WHOLE BATCH {: #comp-recipe-scale}

When you analyze a recipe (its own page, not a portion-analysis or meal/day view), every gram amount in this section — gap closers, [DIAAS](#gloss-diaas)-boosting steps, two-food combinations, two-step combinations — is calculated against the recipe's full total protein across **all of its servings**, not one serving. This is deliberate: the only way to act on a suggestion is to add an ingredient to the whole recipe batch, so the math solves for the whole batch's amino acid gap, not a single portion of it.

This is why a recipe suggestion can look large — for example, 80+ g of soy protein isolate to close a lysine gap in a 4-serving recipe. That is not a serving-size recommendation; it is how much to add to the pot so that every serving, once divided out, ends up amino-acid-complete. Each recipe suggestion also shows the per-serving equivalent alongside the whole-batch amount, so you can see what one serving actually gets.

Data sources, checked in this order: your [pantry](#pantry) (Foods → [My Pantry](#gloss-my-pantry)) and any [recipes you have analyzed](#recipes-menu-web); then your broader food cache (any food you've ever looked up, matched by name against the built-in reference list below); then that built-in list itself[^10], filtered by your dietary preferences (see [dietary preferences](#diet)). The suggestion header tells you exactly which sources were considered for that run. See [amino acid estimates in suggestions](#comp-estimate) for what it means when a suggestion is tagged "(estimated)" or "(generic estimate)".

Don't want a particular suggestion? See [ignoring a complement suggestion](#ignore-complement) in Part 6.


### C. Amino acid estimates in complement suggestions {: #comp-estimate}
A [complement suggestion](#comp) needs amino acid data for the suggested food to compute how much of it closes a gap. Most of the time that comes from the food's own real, measured data. When it doesn't, NuMa falls back to its built-in reference table of 25 common protein sources[^10] (soy protein isolate, nutritional yeast, oats, and the like) — the same last-resort data source described above in [Protein Complement Suggestions](#comp) — rather than leaving you with no suggestion at all. Two tags tell you when that fallback happened:

  "(estimated)" — the suggested food is a real item from your pantry, recipes, or food cache, but it has no amino acid panel of its own. NuMa matched its name against the built-in reference table and scaled that table's amino acid profile to this food's own protein content.

  "(generic estimate)" — no real food matched at all. The whole suggestion is the reference table entry itself, not any specific product you have.

Either way, this estimate is computed fresh every time the suggestion is shown — it is never saved to the food's own record, so there is nothing to undo. This is not the same as the "estimate amino acids from another food" tool described under [Estimating amino acids by copying from another food](#custom-foods). That tool lets you search all your saved foods and pick whichever one you judge to be the best match yourself, and it saves your choice permanently to that food's own record. The built-in table used for the "(estimated)" / "(generic estimate)" tags, by contrast, is a fixed, much shorter list matched purely by keyword — it can't use your own judgment about which food is the closer match, so the two methods can disagree.

For a food you rely on often, running the "estimate amino acids from another food" tool on it yourself is worth doing: it is more accurate (your judgment beats a keyword match against 25 entries), it only has to be done once, and it turns the food into a normal pantry/cache candidate for every suggestion afterward — no more tags.


### D. Two-step combinations {: #comb}
After the gap-closer and [DIAAS](#gloss-diaas)-boosting sections, NuMa offers to show two-step combinations. Each combination pairs one of the top gap-closers (Step 1) with the best [DIAAS](#gloss-diaas)-booster for the resulting protein pool (Step 2).

Why two steps? A gap-closer fixes amino acid balance but may not raise digestibility. A [DIAAS](#gloss-diaas)-booster raises digestibility but cannot close a specific amino acid gap on its own. Together they address both problems: Step 1 corrects the [limiting amino acid](#gloss-limiting-amino-acid); Step 2 raises the overall [DIAAS](#gloss-diaas) of the now-balanced pool, increasing digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp)) further.

Each combination shows:
  - Step 1: the gap-closer, its serving size, and the [DCP](#gloss-dcp) gain from the base
  - Step 2: the smallest practical serving of the best booster for that pool, and the further [DCP](#gloss-dcp) gain
  - Net [DCP](#gloss-dcp) gain from base to end of Step 2

If no [DIAAS](#gloss-diaas)-booster can improve on the post-Step-1 pool (because the gap-closer already raised the pool's digestibility above what any available booster can match), the program says so rather than showing a misleading suggestion.

See also [complement suggestions](#comp) for the full complement suggestion system.


### E. Protein Completeness {: #complete}
A protein is "complete" when it supplies all nine essential amino acids at or above the [FAO](#gloss-fao) 2013 reference amounts, adjusted for digestibility. Essential amino acids cannot be made by the body — they must come from food.

Most animal proteins are complete. Most plant proteins are not, but combining plant foods across a day can produce a complete profile — see [Protein Complement Suggestions](#comp).

The score shown in completeness tables is the ratio of each amino acid to the [FAO](#gloss-fao) reference level. A score of **1.0 or above** for all nine means the protein is complete. The most-[limiting amino acid](#gloss-limiting-amino-acid) (the one with the lowest score) is identified as the bottleneck.


### F. Digestible Complete Protein (DCP) {: #dcp}
[DCP](#gloss-dcp) — digestible [complete protein](#gloss-complete-protein) — is the grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (supply all essential amino acids at or above reference levels).

It is more meaningful than raw grams of protein because it accounts for:

- **Digestibility:** how much protein is actually absorbed (from [DIAAS](#gloss-diaas))
- **Completeness:** whether the amino acid profile meets all requirements

A food with 30 g of protein but a [DIAAS](#gloss-diaas) of 0.70 and several amino acid gaps contributes less usable protein than those numbers suggest. [DCP](#gloss-dcp) captures that.

[DCP](#gloss-dcp) is also called "bioavailable complete protein" or "usable protein" in nutrition literature — these terms mean the same thing. NuMa uses [DCP](#gloss-dcp) throughout.

NuMa shows [DCP](#gloss-dcp) in the bioavailability section of food and recipe analysis. See also [DIAAS](#diaas) and [Protein Completeness](#complete).


### G. DIAAS — Digestible Indispensable Amino Acid Score {: #diaas}
[DIAAS](#gloss-diaas) measures how well your body can actually use the protein in a food. A score of **1.0** means the protein fully meets the [FAO 2013 amino acid reference standard](#fao) after accounting for digestibility. Scores above 1.0 are excellent; below 1.0 means one or more amino acids fall short.

Animal proteins typically score 1.0 or above. Most plant proteins score below 1.0, though some (pea protein, soy) come close. Digestibility matters because some protein in food is never absorbed — it passes through unchanged or is broken down by gut bacteria rather than used by your body.

A note on terminology: the [FAO](#gloss-fao) uses the term "indispensable amino acids" (IAA) where this manual uses "essential amino acids" ([EAA](#gloss-eaa)) — both refer to the same nine amino acids. The "I" in [DIAAS](#gloss-diaas) stands for "Indispensable."

NuMa uses [DIAAS](#gloss-diaas) to calculate digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp)), which is a better indicator of actual protein quality than raw grams. See [Digestible Complete Protein (DCP)](#dcp).

#### Estimating DIAAS by hand for a packaged food {: #diaas-estimate-table}
Branded/packaged products often have no amino acid data at all, so NuMa can't compute [DIAAS](#gloss-diaas) automatically — you record a point estimate instead via the [DIAAS](#gloss-diaas) estimate [Food Annotation](#gloss-food-annotation) (Foods → Annotate a food — see [Getting missing amino acid data](#custom-foods)). [DIAAS](#gloss-diaas) is mostly a property of the *protein source*, not the specific product, so the same point estimate is reusable across many products built from that ingredient. This table of published point estimates by dominant protein source is a starting reference, not a substitute for a real measured value if one is available:

    Protein source        DIAAS       Limiting AA                Note
    --------------------  ----------  -------------------------  ------------------------------
    Whole wheat            0.45       Lysine                     Range 0.40-0.57 across studies
    Soy (isolate/tofu)     0.90-1.00  Methionine+cystine (mild)  Near-complete
    Pea protein            0.82-0.90  Methionine+cystine         Complements wheat well
    Oats (dehulled)        0.77       Lysine                     Better than most cereals
    Sunflower seed          ~0.60     Lysine                     Usually a minor contributor

For a product where one ingredient supplies essentially all the protein (e.g. a wheat cracker where the oil contributes negligible protein), use that ingredient's row directly. For a product with two meaningful protein sources (e.g. a wheat+pea cracker), weight the estimate by each ingredient's share of total protein grams — the same complementary-protein logic used elsewhere in NuMa's [meal-level DIAAS](#dcp) pooling. Document your reasoning (source ingredient, any blending math) in the food's Confidence Note or notes field so it can be reviewed or revised later.


### H. Limiting-Amino-Acid Scoring {: #aa-scoring}
Protein quality analysis involves two separate adjustments. The Protein Digestibility table shows the result after the first adjustment only. The phrase "before limiting-amino-acid scoring" on that table means the second adjustment has not yet been applied.

#### Step 1 — Digestibility adjustment (shown in the table)

    Digestible protein (g) = food protein (g) × digestibility coefficient

This accounts for how much protein actually reaches your bloodstream. A food with 20 g of protein and a digestibility of 0.85 delivers 17 g of digestible protein. This is what the "Digestible (g)" column in the [Meal Protein Digestibility Analysis](#meal-diaas) table shows.

#### Step 2 — Limiting-amino-acid scoring (the DIAAS step)

    Digestible complete protein (g) = digestible protein (g) × min(DIAAS, 1.0)

Even if all the protein is absorbed, it cannot all be incorporated into tissue unless every essential amino acid is present in sufficient proportion. The amino acid in shortest supply — the [limiting amino acid](#gloss-limiting-amino-acid) — sets a ceiling. [DIAAS](#gloss-diaas) is the ratio of that [limiting amino acid](#gloss-limiting-amino-acid) to the [FAO](#gloss-fao) reference level. If [DIAAS](#gloss-diaas) is 0.80, only 80% of the digestible protein can be fully used; the rest is broken down and excreted.

The "Total digestible protein" line below the table is the sum after step 1 only. The [DCP](#gloss-dcp) figure reported in the meal summary is the result after both steps.

Note: [DIAAS](#gloss-diaas) itself is not capped — a high-quality food can score above 1.0, meaning it has surplus amino acids relative to the reference. The min([DIAAS](#gloss-diaas), 1.0) applies only when computing [DCP](#gloss-dcp), because having excess amino acids does not allow you to absorb more total protein than you consumed.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [limiting amino acid](#gap), [DCP cap](#dcp-cap).


### I. Why DCP Is Sometimes Capped Below the DIAAS Projection {: #dcp-cap}
The short version: the [DIAAS](#gloss-diaas) formula can project a Digestible [Complete Protein](#gloss-complete-protein) value that is mathematically higher than the protein your body actually absorbed. When that happens, NuMa caps [DCP](#gloss-dcp) at the absorbed-protein ceiling, because you cannot use more protein than you took in.

#### Why this happens

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

#### A worked example

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

#### What the cap means in practice

A capped [DCP](#gloss-dcp) is actually good news about amino acid quality. It means your [limiting amino acid](#gloss-limiting-amino-acid) is present in such good supply (relative to raw protein) that the formula projects more [complete protein](#gloss-complete-protein) than you could possibly absorb. The practical reading: all of your absorbed protein is functioning as [complete protein](#gloss-complete-protein). You are not losing protein to an amino acid shortfall.

Compare this to an uncapped [DCP](#gloss-dcp) that is well below absorbed protein: the gap between them represents protein you absorbed but cannot fully use for tissue synthesis because the [limiting amino acid](#gloss-limiting-amino-acid) ran out first. That is the more common and more concerning situation.

The average digestibility shown in the cap note is the weighted average of per-ingredient [digestibility coefficients](#gloss-digestibility-coefficient), weighted by protein content. Each coefficient comes from the curated lookup table or category estimate described in [meal protein digestibility](#meal-diaas).

This cap note appears on the meal, full-day, recipe, and daily-summary DIAAS sections.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [amino acid scoring](#aa-scoring).


### J. FAO 2013 Reference Standard {: #fao}
The [FAO](#gloss-fao) (Food and Agriculture Organization of the United Nations) published a reference amino acid scoring pattern in 2013 that defines the minimum amounts of each essential amino acid per gram of protein needed to meet adult human requirements. This is a ratio, not an absolute quantity — the requirement scales with how much protein you eat, so a small meal and a large meal must both hit the same per-gram proportions. See [Appendix B](#appendix-b) for the full worked explanation of why this ratio, not total protein, determines what your body can use.

NuMa uses this pattern as the benchmark for all protein quality scoring: completeness, gaps, and complement calculations. A score of **1.0** for an amino acid means the food exactly meets the [FAO](#gloss-fao) reference for that amino acid; above 1.0 exceeds it; below 1.0 falls short.

The [FAO](#gloss-fao) 2013 pattern replaced an older 1991 standard and is the current international reference for protein quality assessment.


### K. Amino Acid Gaps {: #gap}
An amino acid gap means one or more essential amino acids are below the [FAO](#gloss-fao) 2013 reference level after digestibility adjustment. The gap is expressed as a score: 0.70 means the food supplies 70% of what is needed for that amino acid.

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

See [Protein Complement Suggestions](#comp) for how NuMa suggests foods to close gaps.


### L. Antinutrients {: #antinutrients}
Most people have never encountered this term, yet [antinutrients](#gloss-antinutrient) are present in virtually every plant food. Understanding them is especially important for anyone eating a plant-predominant diet, because the same foods that supply the most fiber, minerals, and [phytonutrients](#gloss-phytonutrients) are often the ones that contain the highest [antinutrient](#gloss-antinutrient) loads.

#### What is an antinutrient?

The word sounds alarming, but it simply means a naturally occurring compound in a food that partially blocks the absorption or use of a nutrient your body would otherwise receive. The effect is not binary — it is a matter of degree, and it can usually be reduced or eliminated by how you prepare the food.

Plants produce these compounds as a natural defense: against insects, fungi, and animals that would eat them. They are not contaminants or the result of farming practices. They are intrinsic to the plant's biology.

#### The main antinutrients that appear in NutriMagnus output

**Phytates** (phytic acid). Found in legumes, whole grains, nuts, and seeds. Phytate binds tightly to minerals — especially iron, zinc, calcium, and magnesium — forming a complex the body cannot easily absorb. A meal of lentils or whole-wheat bread may contain all the iron the label shows, but much of it may pass through unabsorbed if phytate is high. The effect depends on the rest of the meal: vitamin C consumed at the same meal significantly counteracts phytate's effect on iron. Preparation methods that consistently reduce phytate: soaking legumes or grains overnight before cooking; sprouting; fermentation (sourdough bread reduces phytate by 50-90%; tempeh and other fermented soy products have low phytate).

**[Oxalates](#gloss-oxalate)**. Found at high levels in spinach, Swiss chard, beet greens, rhubarb, and almonds; at moderate levels in many other plant foods. [Oxalates](#gloss-oxalate) bind calcium in the gut, meaning the calcium shown on a food label for spinach is largely unavailable — absorption rates can be as low as 5%, versus 30% for dairy calcium. For most people this is simply a reason not to rely on spinach as a calcium source, not a reason to avoid it. For people prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly. See [oxalate data](#oxalate) for the detailed data NuMa tracks on this.

**Lectins** and **trypsin inhibitors**. Found in raw legumes (beans, lentils, chickpeas, soybeans). Lectins interfere with the gut lining; trypsin inhibitors block a key digestive enzyme. Raw kidney beans contain enough lectin to cause acute food poisoning. Cooking completely solves the problem: full boiling for at least 10 minutes destroys both lectins and trypsin inhibitors. Canned beans are already safe. Tofu and tempeh are also safe because both involve prolonged heat treatment or fermentation. This is the one [antinutrient](#gloss-antinutrient) on this list that is not just about partial reduction — with raw legumes, proper cooking is required.

**Bound niacin** (in corn). Untreated corn contains niacin in a chemically bound form the human body cannot absorb. Populations who ate corn as a dietary staple without treatment historically developed pellagra (severe niacin deficiency). The traditional solution — practiced for thousands of years by Mesoamerican cultures and still used today — is nixtamalization: soaking dried corn in an alkaline lime solution. This releases the niacin and makes it fully bioavailable. Tortillas, masa, hominy, and grits made from nixtamalized corn are fine. Plain cornmeal (not nixtamalized) retains the problem.

#### How these appear in NutriMagnus output

When you view a food with known [antinutrient](#gloss-antinutrient) concerns, a note appears in the Bioavailability section of the analysis. The note names the compound, describes the specific problem, and lists the preparation method(s) that reduce it.

#### Examples of what you may see

    Mineral absorption problem — phytates are present
    Best reduction: soak or sprout before cooking

    Mineral absorption problem — high oxalate reduces calcium uptake from this food specifically

    Mineral absorption problem — oxalate & phytate present
    Reduces both: roasting or soaking

    Digestibility problem — lectins & trypsin inhibitors
    Required: fully cook (boil) to inactivate

    Vitamin bioavailability problem — niacin is bound, not usable unless nixtamalized
    Nixtamalized forms are fine: tortilla, masa, hominy

These notes appear only for foods where NuMa has a curated flag — the list is not exhaustive, and absence of a note does not mean a food is free of [antinutrients](#gloss-antinutrient).

#### What these notes do not mean

They are not a reason to avoid these foods. Legumes, whole grains, nuts, and leafy greens are among the most nutritious foods available. The minerals and protein they supply — even after [antinutrient](#gloss-antinutrient) reduction — are substantial, and their other benefits (fiber, [phytonutrients](#gloss-phytonutrients), cost, sustainability) are undiminished. The notes exist so you can make informed preparation choices and avoid assuming that every labeled nutrient is fully absorbed.

The practical message is: soak legumes, prefer sourdough or sprouted grains when possible, cook beans fully, pair iron-rich plant foods with vitamin C, and do not rely on spinach as your primary calcium source.


### M. Oxalate Data {: #oxalate}
[Oxalates](#gloss-oxalate) are one of the [antinutrients](#gloss-antinutrient) discussed in [antinutrients](#antinutrients). The section here covers the detailed data NuMa tracks and how to use it. For general background on what [oxalates](#gloss-oxalate) are and how they compare to other [antinutrients](#gloss-antinutrient), read [antinutrients](#antinutrients) first.

[Oxalates](#gloss-oxalate) (oxalic acid) bind calcium in the gut, reducing its absorption from high-[oxalate](#gloss-oxalate) foods. They are found at very high levels in spinach, Swiss chard, beet greens, and rhubarb, and at notable levels in almonds and some other nuts. For most people the main consequence is that these foods are poor calcium sources despite their labels. For anyone prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly.

NuMa includes the Harvard T.H. Chan School of Public Health [oxalate](#gloss-oxalate) table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine. This data is optional and disabled by default.

**To enable it:** Settings → Your Profile → check "Look up oxalate content for foods," then Save profile.

Once enabled, viewing a food or analyzing a recipe automatically looks it up in the Harvard table by name and links the best match — no confirmation prompt. That link is saved the first time and reused after, so the lookup only runs once per food.

#### Important limitations

- [Oxalate](#gloss-oxalate) values in the Harvard table are reported per serving, not per 100 g. For foods measured in ounces (fish, nuts, meat), NuMa automatically converts to per-100g. For foods measured in cups, pieces, or tablespoons, only the per-serving value is available. Volumetric servings cannot be converted to per-100g without knowing the food's density — that conversion must be done manually if needed.

- For recipe analysis, NuMa sums [oxalate](#gloss-oxalate) only for ingredients where a per-100g value is available. Volumetric-only items are excluded from the total and noted as such.

- [Oxalate](#gloss-oxalate) content varies with preparation method (cooking reduces [oxalate](#gloss-oxalate) in spinach, for example) and growing conditions. All values should be treated as estimates.

- Matching by food name is approximate. "Spinach, raw" in the Harvard table maps reasonably to [USDA](#gloss-usda) spinach entries, but processed or branded foods may not match well. Always verify the match makes culinary sense before confirming it.

For background on [oxalates](#gloss-oxalate) and kidney health, see the Harvard Health references in the source data (Settings -> [Oxalate](#gloss-oxalate) data for data provenance).


### N. Glycemic Index {: #gi}
The glycemic index ([GI](#gloss-gi)) measures how quickly a carbohydrate-containing food raises blood glucose compared to pure glucose ([GI](#gloss-gi) = 100). Low-[GI](#gloss-gi) foods (55 or below) produce a slower, more gradual rise; high-[GI](#gloss-gi) foods (70 and above) cause a faster spike.

[GI](#gloss-gi) is shown in the nutrient summary when data is available. It is most useful for comparing foods within the same category — for example, choosing between types of bread or rice. Keep in mind that [GI](#gloss-gi) describes a food eaten alone; combining foods in a meal (especially adding fat, protein, or fiber) physiologically blunts the blood glucose response to the carbohydrates present, by slowing gastric emptying and glucose absorption. However, this effect is not fully captured by glycemic load ([GL](#gloss-gl)) — see [Glycemic Load](#gl) for why.

NuMa displays [GI](#gloss-gi) for reference only and does not use it in protein quality calculations.

**Where [GI](#gloss-gi) values come from.** Neither [USDA](#gloss-usda) nor Open Food Facts[^3] tracks [GI](#gloss-gi), so NuMa can't look it up automatically the way it does for calories or protein — you (or NuMa, on your behalf) have to supply it. To save you the work for common foods, NuMa can automatically fill in [GI](#gloss-gi) values for about 60 everyday items, using a published reference table[^8]. If your food cache doesn't have these values yet, NuMa will ask whether you'd like it to fill them in for you. For anything else, just add [GI](#gloss-gi) values as you go: the first time you add a new food to your Pantry or a meal, NuMa will offer to prompt you for its [GI](#gloss-gi) value right there, so your data builds up naturally through normal use.


### O. Glycemic Load {: #gl}
Glycemic load ([GL](#gloss-gl)) improves on the glycemic index by accounting for both the quality and the quantity of carbohydrate in a serving. The formula is:

```
GL = (GI × grams of available carbohydrate) / 100
```

For a meal combining multiple foods, the total [GL](#gloss-gl) is the sum of the [GL](#gloss-gl) calculated separately for each component:

```
Meal GL = GL(food 1) + GL(food 2) + GL(food 3) + ...
```

Adding more carbohydrate-containing foods will always increase the meal total. The reason combining foods physiologically blunts the blood glucose response — as noted in the [GI](#gloss-gi) section — is not reflected in this calculation. Protein, fat, and fiber slow gastric emptying and glucose absorption, reducing the actual blood glucose rise; but because [GL](#gloss-gl) is calculated from fixed [GI](#gloss-gi) values measured for each food in isolation, it has no way to represent that interaction. [GL](#gloss-gl) is therefore a reliable tool for comparing meals of broadly similar macronutrient composition, but becomes less accurate when meals differ significantly in their fat or protein content.

A food can have a high [GI](#gloss-gi) but a low [GL](#gloss-gl) if the serving contains little actual carbohydrate — watermelon is the classic example. Conversely, a moderate-[GI](#gloss-gi) food eaten in a large portion can produce a high [GL](#gloss-gl). For this reason [GL](#gloss-gl) is generally a better guide to real-world blood glucose impact than [GI](#gloss-gi) alone.

**[GL](#gloss-gl) is interpreted on a per-meal or per-food basis:**

| [GL](#gloss-gl) Range | Classification |
|---|---|
| 10 or below | Low |
| 11–19 | Medium |
| 20 or above | High |

NuMa displays [GL](#gloss-gl) in the nutrient summary alongside [GI](#gloss-gi) when carbohydrate data is available. Like [GI](#gloss-gi), it is shown for reference and does not affect protein quality calculations.

For a discussion of how [GL](#gloss-gl) compares to other approaches for evaluating the blood glucose impact of different meal choices — particularly relevant for people managing diabetes — see [Appendix D: GL and Blood Glucose Comparison](#appendix-d).


### P. Recommended Dietary Allowances {: #rda}
[RDA](#gloss-rda) values in NuMa come from the Dietary Reference Intakes ([DRI](#gloss-dri)) published by the U.S. National Academies of Sciences, by way of the NIH Office of Dietary Supplements[^9]. Here is the ODS's own definition, word for word:

> "Recommended Dietary Allowance (RDA): Average daily level of intake sufficient to meet the nutrient requirements of nearly all (97–98%) healthy individuals[^9]."

**Read that carefully — an RDA is not a bare-survival minimum.** It's set high enough that following it meets the needs of nearly everyone in your age/sex group, with margin built in. (The government's actual bare-minimum figure, the amount that meets only the *average* person's need with no safety margin, is called the EAR — Estimated Average Requirement — and NuMa doesn't use it for anything, since it's a population-statistics tool, not a personal target.) NuMa still labels this tier "minimum" in a few places in the interface — meaning "meet or exceed this amount," a directional instruction, not a claim about how large the number itself is — see the color-coding note below and [Daily Nutrient Goals](#goals) for exactly what "minimum," "target," and "limit" each mean as goal types.

When you set a user profile (Settings → User profile), NuMa uses your age, sex, weight, height, and activity level to estimate personalized targets — see [Daily Nutrient Goals](#goals) just below for the age/sex bands behind every mineral and vitamin RDA, not just the two formula-based ones (calories, protein) described here. The calorie estimate uses the Mifflin-St Jeor equation with an activity multiplier. The protein target uses 0.8 g per kg body weight as a baseline minimum.

The nutrient comparison table (shown on food, recipe, meal, and daily-summary pages) shows your intake compared to your targets.

Columns:

    Nutrient              Name of the nutrient.
    Total                 How much this food/recipe/meal/day provides (or,
                           on a food page, how much the entered portion provides).
    Unit                  The nutrient's unit (g, mg, mcg).
    % of daily target     Total / RDA target x 100, color-coded green/yellow/red
                           by how close you are to (or over) that target —
                           shown only when you've set up a user profile.
    Revised Optimal goal,
    % of Revised Optimal  Same idea against your own custom Revised Optimal
                           target instead of the standard RDA — shown only for
                           nutrients where you've set one (see [Profile Optimal
                           Targets](#optimal)).
    UL                    Shown only where you're near or over a max limit —
                           see [Maximum Nutrient Limits](#maxlimits).

The color coding on % of daily target (and % of Revised Optimal) follows the same green/at-or-above, yellow/getting-close, red/short-or-over-limit logic throughout the app.

Nutrients without an established Dietary Reference Intake ([phytonutrients](#gloss-phytonutrients), amino acids) are shown without a % of [RDA](#gloss-rda) figure -- those rows show only the Total amount.

See [daily nutrient goals](#goals) for a full explanation of how each goal is calculated.


### Q. Daily Nutrient Goals {: #goals}
NuMa calculates personalized daily nutrient goals from your user profile (Settings → User profile). Each goal is one of three types:

    Minimum  — RDA or Adequate Intake (AI): the daily amount needed to
               meet the requirements of most healthy adults.
    Target   — an estimated ideal intake (currently applies to calories).
    Limit    — a maximum daily amount you don't want to exceed. Sodium has
               its own fixed 2300 mg/day limit (see the sodium note below).
               Twelve other nutrients get an automatic Tolerable Upper
               Intake Level as their default limit — see [Maximum Nutrient
               Limits](#maxlimits) for the full list and for setting your
               own custom limit on any nutrient.

#### HOW EACH GOAL IS CALCULATED

#### Calories (target)
    Mifflin-St Jeor equation for Basal Metabolic Rate, multiplied by an
    activity factor based on your activity level setting:

        Sedentary (desk job, little exercise)           x 1.2
        Lightly active (light exercise 1-3 days/week)   x 1.375
        Moderately active (3-5 days/week)               x 1.55
        Active (hard exercise 6-7 days/week)            x 1.725
        Very active (physical job or twice-daily)       x 1.9

#### Protein (minimum)
    Scaled to body weight and activity level:

        Sedentary or lightly active   0.8 g per kg body weight
        Moderately active             1.0 g per kg body weight
        Active or very active         1.2 g per kg body weight

#### Carbohydrates (minimum)
    130 g/day — the brain's minimum glucose requirement (fixed for all).

#### Fiber (minimum)
    Age- and sex-dependent Adequate Intake:

        Men under 50: 38 g/day     Men 50+: 30 g/day
        Women under 50: 25 g/day   Women 50+: 21 g/day

#### Sodium (limit)
    2300 mg/day — standard Tolerable Upper Intake Level (fixed for all).

#### Omega-3 ALA (minimum)
    1600 mg/day men, 1100 mg/day women — Adequate Intake for alpha-linolenic
    acid (ALA), the plant-sourced omega-3. See [Omega-3 Fatty Acids](#omega3)
    for why this is the only omega-3 with an official goal in NuMa.

#### Minerals and vitamins — every age/sex band, in full

All minerals and vitamins use age- and sex-specific values from the Dietary Reference Intakes published by the U.S. National Academies of Sciences[^9]. If your profile's sex is set to "other," NuMa uses the midpoint of the male and female values — except for the handful of nutrients marked below, where the underlying DRI tables don't publish a distinct value for anything other than male/female, so "other" uses the same value as female.

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

\* These four rows are the exception noted above: the DRI tables don't distinguish "other" from female here, so NuMa uses the female value rather than a male/female midpoint.

Nutrients without established [DRIs](#gloss-dri) ([phytonutrients](#gloss-phytonutrients), amino acids) have no goal shown. The "% today" column and "Daily goal" column are blank for those rows.

See [RDA](#rda) for a general overview of where these values come from. If the standard RDA isn't the number you actually want to hit for a given nutrient, see [Profile Optimal Targets](#optimal). If you want to be warned as you approach a personal daily cap, see [Maximum Nutrient Limits](#maxlimits). A single day's numbers are only a snapshot -- see [Multiday Nutrient Trend](#trend) for how to spot a shortfall that persists across many days.


### R. Multiday Nutrient Trend {: #trend}
Every other RDA comparison in NuMa -- food, recipe, meal, daily summary -- looks at a single day. That's the right window for "did today's meals cover me," but it's the wrong window for a nutrient that's chronically a little short: one low day is unremarkable, but the same shortfall repeated for two weeks straight is exactly the kind of pattern a single-day view can never show you, because you'd have to remember and compare each day yourself.

**Access it via the "Multiday nutrient trend" button on the Daily Summary page.** Choose a window -- last 7, 14, or 30 days -- and NuMa averages your total intake for every tracked nutrient across the days in that window that actually had a meal logged, then compares that average against your RDA (and Profile Optimal / max limits, if configured) using the exact same table, color coding, and diet-aware notes as the daily comparison.

**Only logged days count.** If you ask for a 30-day trend but only logged meals on 12 of those days, the average is computed over those 12 days -- unlogged days are treated as "no data," not as a zero-intake day. Diluting the average with days you simply didn't track would understate your real intake and could hide the exact shortfall this view exists to surface. The screen tells you how many logged days went into the average (e.g. "Averaging over 12 logged day(s) out of the last 30").

This is the same B12/iron/zinc-aware analysis described in [Diet-Aware Bioavailability and Deficiency Notes](#diet-bioavailability) -- a trend view is often where a B12 or iron pattern actually becomes visible, since a single low day rarely triggers concern on its own.

**Multi-day protein complementarity.** Below the nutrient comparison, the trend view also pools every amino-acid-containing food logged across the window's days and runs the same [complement suggestion](#comp) analysis normally shown for a single day -- but framed for forward planning ("Add to upcoming meals" rather than "Add to your day"), since the gap it found accumulated across several days, not one meal you can still fix. A gap that only shows up when pooled across the whole window -- rather than in any single day's suggestions -- is exactly the kind of small, persistent shortfall this view is meant to catch.


### S. Nutrient Plot {: #nutrient-plot}
A line chart of one or more nutrients across your logged days, day on the x-axis — useful for spotting a trend visually rather than reading a column of numbers.

**Access it from Analysis → Daily Summary → "Nutrient plot".** Check up to 8 nutrients from the full nutrient list (any nutrient NuMa tracks, not just the ones you've chosen as Meals & Log columns, plus Day DCP itself) — Day DCP, Protein, Calories, Carbs, and Fiber are listed first, matching Recent Days' mandatory columns; the checkbox list scrolls vertically below them. Then choose which days to include:

    (blank days-back)         Every logged day, oldest to newest.
    Days back + Ending on     The N days ending on the date you pick
                              (defaults to your most recent logged day).

Only days that actually have a logged meal appear on the chart — a gap in your logging shows as a gap in the line, not a drop to zero.

**Date labels thin out automatically on a long chart.** Every plotted day still gets a data point, but once there are more than 18 of them, showing every single date's label would crowd them into an unreadable jumble, so only every 2nd, 3rd, etc. date is labeled (always skipping at least one), spaced out enough to stay legible.

If you pick nutrients with different units (e.g. Protein in g alongside Sodium in mg), they still plot together on one y-axis. In that case the y-axis shows no title or numbers at all — once nutrients are on different scales, no single number on a shared axis means the same thing for every line, so printing one would just be misleading. The gridlines are still there for a rough sense of relative up-and-down movement; each line's real values live in its own legend entry instead. Plotting a single nutrient, or several that share a unit and didn't need any scaling, still shows a normal, meaningful numbered axis.

**Scaling happens in two steps, both of which you can override.**

*Step 1 — Scale factor.* If one nutrient's numbers dwarf another's (e.g. Calories next to Protein, or Calcium next to Protein), the smaller one would flatten into a barely-visible wiggle along the bottom. NuMa automatically divides every plotted nutrient except the least up-and-down one by a computed **Scale factor** — a number based on how much each nutrient's values swing over the plotted days — which brings a dominant nutrient's swings down to roughly match the smallest one's. The **Scale factor** field shows this computed value as a placeholder (grayed, e.g. "3.5") and is left blank by default, meaning "use that computed value." Type your own number and click Plot to override it.

*Step 2 — Per-nutrient factors.* A single shared Scale factor can't perfectly equalize more than two nutrients at once — with three or more plotted, one can still end up nearly flat even after step 1. NuMa checks each nutrient again after step 1 and sets a floor at 25% of the most up-and-down nutrient's swing; anything still below that floor gets its own individual multiplier (shown as "×2.4" etc. in its legend entry) to bring it back up to a visibly readable wiggle. Each chosen nutrient gets its own **Per-nutrient factors** field, prefilled the same "blank = use the computed value" way as Scale factor — type a number to override just that one nutrient.

**Highlight nutrient.** Pick which one nutrient always draws solid and (in color mode) red, so the figure you're usually comparing everything else against stands out at a glance — defaults to Day DCP whenever it's one of the chosen nutrients.

**Black & white (printer-friendly).** Check this to preview the chart the way it'll look on a printer that can't print color: every line drawn in black, with the highlighted nutrient solid and every other nutrient in its own dash pattern (dashed, dotted, dash-dot, etc.) instead of a color, so lines stay distinguishable without color at all. The on-screen chart updates the instant you check or uncheck the box — no need to click Plot — so you can compare both looks side by side before deciding.

**Smoothing.** Day-to-day values can be noisy enough to obscure the underlying trend. The **Smoothing (days)** field averages each point with its preceding days — a trailing moving average — to smooth that out; it defaults to 3 days. Set it to 0 to turn smoothing off and see the original, unsmoothed data. A smoothed nutrient's own scaling (steps 1 and 2 above) is calculated from the smoothed data, since that's what's actually on the chart.

**Plot title.** Defaults to "Key nutrients, {start date} to {end date}" for whatever range is currently plotted, shown right on the chart itself. Edit the **Plot title** field and click Plot to use your own instead.

**The legend sits below the chart**, wrapped horizontally rather than stacked in a tall column, so it never overlaps a data line and stays compact and print-friendly.

**Print or save it.** "Print / Save as PDF" opens a stripped-down, print-friendly page with the chart and your browser's print dialog. "Download PNG" and "Download SVG" save the chart as an image file — see [Plot File Formats](#plot-file-formats) for which one to pick.


#### Plot File Formats — PNG vs. SVG {: #plot-file-formats}
Both "Download PNG" and "Download SVG" save the same chart as an image file you can keep, email, or paste into a document — they just store it differently.

**PNG** is a normal photo-style image, a fixed grid of pixels. It opens everywhere without a second thought, and is the safer default if you're not sure what a document or website will accept.

**SVG** stores the chart as the shapes and lines that drew it, not pixels — so it stays perfectly crisp at any size, whether you zoom way in on screen or print it on a large sheet of paper. PNG images can look blurry or blocky if enlarged; an SVG never will. The trade-off is that a few older programs don't open SVG files directly (most current web browsers, word processors, and image editors do).

**Rule of thumb:** downloading to look at, email, or drop into a typical document — PNG. Need to print it large, or want it to stay sharp if someone else resizes it — SVG.


### T. Per-Day Profile Tracking {: #day-profile}
Your profile isn't fixed forever -- weight, activity level, or even which named profile is active can change over time (illness, travel, a deliberate weight change). But your logged meals stay put. If a past day's DCP and RDA comparisons always used *today's* profile, an old day could silently get re-scored against numbers that weren't true of you back then.

**Each logged day is pinned to whichever profile was active the first time a meal was saved for that date.** That pin is a full snapshot -- your age, weight, activity level, and targets as they were that day -- not just a name. So if you later edit that profile's numbers (or switch which profile is active), days already logged keep comparing against the numbers that were true when you logged them. Only a day that has never had a meal saved for it — or one you explicitly reassign — will pick up a different profile.

**Where you see it.** If you maintain more than one named profile, a **Profile** column/line appears next to each day: on the Meals & Log list, the Recent Days list, and the Daily Summary / full-day view. With only one profile configured, this column is hidden since there's nothing to distinguish.

**Changing a day's profile.** Sometimes the automatic pin doesn't match reality -- illness or travel rarely starts exactly at midnight. Open that day's summary and use the **Change** control next to "Profile:" (on the day's Summary or Full Day page) to pick a different saved profile. The day is marked "(manually set)" afterward and its DCP/RDA numbers recompute immediately against the new pin.

**Multiday trend.** The [Multiday Nutrient Trend](#trend) view spans many days at once, so it scores against the profile pinned to the *most recent* day in the window (today, for the usual "last N days"). If any day inside the window was pinned to a different profile, a note discloses which dates and profile differed, rather than silently blending two profiles' targets into one average.

**Existing data.** If you're upgrading from a version of NuMa that didn't have this feature, every day you'd already logged gets pinned to whichever profile is active the first time you open NuMa after upgrading -- you don't need to open or edit anything for this to happen.


### U. Omega-3 Fatty Acids {: #omega3}
NuMa tracks four omega fatty acids: ALA, EPA, and DHA (all omega-3), and linoleic acid (omega-6). Only one of these four -- ALA -- has an official Adequate Intake, so it's the only one that appears as a Daily Goal: 1600 mg/day for men, 1100 mg/day for women.

**Why not a goal for EPA and DHA directly?** No U.S. Dietary Reference Intake exists for EPA or DHA intake on their own -- the official guidance covers only total ALA. This matters because ALA is not itself the fatty acid your body mostly uses; it has to be converted into EPA and then DHA, and that conversion is inefficient -- commonly cited at only around 5-10% for EPA, and considerably less for DHA. Two people can hit the same ALA target and land in very different places on EPA/DHA status depending on the rest of their diet, genetics, and sex (conversion tends to be somewhat more efficient in women).

**Why this matters especially for plant-based eaters.** Direct dietary EPA and DHA come almost entirely from fish, algae, and other seafood. If ALA (from flax, chia, walnuts, hemp, canola and soy oils) is your only omega-3 source, meeting the ALA goal is necessary but may not be sufficient -- your actual EPA/DHA status depends on that inefficient conversion step. Common ways to address this without animal fish: algae-oil supplements (a direct EPA/DHA source independent of the ALA conversion pathway), or simply logging ALA-rich foods generously since the target itself already assumes real-world conversion losses are ahead of it.

**Setting your own EPA+DHA target.** Because there's no official DRI to compute automatically, NuMa can't put a Daily Goal on the EPA or DHA rows the way it does for ALA. If you want to track against a target anyway -- clinical guidance in the 250-500 mg/day combined EPA+DHA range is common -- set one yourself as a [Profile Optimal target](#optimal) for the EPA and/or DHA rows in Settings → Nutrient targets.

Linoleic acid (omega-6) is tracked for completeness but has no established goal or known deficiency risk in a typical diet -- most diets, plant-based or not, comfortably exceed the AI for it.


### V. Profile Revised Optimal (Recent Research) Targets {: #optimal}
**A word on terminology, since two different ideas both sound like "optimal":** the standard RDA (Part 5, Section P) is not a bare minimum — it's already defined to meet the needs of nearly all healthy people in your age/sex group[^9]. What's described in this section is a *different, second* tier: a small number of nutrients where specific, more recent research argues for a target meaningfully *above* even that generous RDA figure. To keep the two clearly apart, NuMa calls this second tier **Revised Optimal (Recent Research)** — never just "optimal" on its own — and the RDA is never relabeled to match it.

The clearest example is Vitamin D: the RDA is 15–20 mcg/day, but a 2011 Endocrine Society clinical practice guideline recommends 37.5–50 mcg/day for adults at risk of deficiency[^12]. Rather than change what "RDA" means, NuMa lets you set your own **Revised Optimal target** for any nutrient, on top of the standard RDA, and tracks both side by side.

Configure Revised Optimal targets in **Settings → 7. Nutrient Targets**. Pick a nutrient, enter your target amount in that nutrient's usual unit, and save. Leave the field blank and save again to clear it. This works for any nutrient NuMa tracks -- not just ones with a standard RDA. Amino acids, EPA/DHA, and [phytonutrients](#gloss-phytonutrients) have no official [DRI](#gloss-dri) but are still valid Revised Optimal target or [max limit](#maxlimits) candidates; amino acids in particular are more accurately evaluated by the app's [DIAAS](#diaas)-based protein quality scoring (which accounts for total protein intake), so a flat daily gram target here is a coarser measure than that -- useful mainly if you want a simple standalone tripwire for one specific amino acid.

**Loading recommended targets.** Typing values in from scratch is a lot to ask, so the Nutrient targets screen offers a **"load recommended Revised Optimal targets"** button that fills in a small curated set of commonly-cited targets for any of those nutrients you haven't already customized yourself:

| Nutrient | Built-in Revised Optimal default | Source |
|---|---|---|
| Vitamin D | 50 mcg/day | Endocrine Society clinical practice guideline[^12] |
| Omega-3 EPA | 250 mg/day | ADA/Dietitians of Canada position paper[^13] (250 mg EPA + 250 mg DHA = ~500 mg combined) |
| Omega-3 DHA | 250 mg/day | Same source[^13] |

These are general population guidance, not personalized medical advice, and every value it loads can still be reviewed and adjusted individually afterward. See [Omega-3 Fatty Acids](#omega3) for why EPA/DHA specifically has no official DRI to compute automatically. Only these three nutrients have a built-in default today — see [Expanding Revised Optimal (Recent Research) targets](#expand-revised-optimal) in Part 9 for the plan to add more, each with its own citation the same way.

Once you have at least one Revised Optimal target set, every nutrient analysis table (food, recipe, meal, and daily summary) gains a second "Revised Optimal" set of columns next to the standard "RDA" columns -- the same meal %, day total %, and goal columns you already know, computed against your custom target instead of the RDA. Nutrients you have not customized show a dash ("–") in these columns rather than falling back to the RDA value, so it stays obvious which nutrients you've actually personalized.

Revised Optimal targets are per-nutrient, not per-day -- there is no single "optimal profile" to pick, only individual overrides you add nutrient by nutrient. Color coding matches the RDA columns: green at or above target, yellow approaching it, red well short (or, for capped nutrients like sodium, red once over).


### W. Maximum Nutrient Limits {: #maxlimits}
NuMa tracks three tiers of daily maximum, from broadest to narrowest:

- **Sodium's built-in RDA-tier limit.** Sodium is the one nutrient with a "limit" type right in the standard [RDA](#rda) calculation itself (Part 5, Section Q) — 2300 mg/day, the Chronic Disease Risk Reduction Intake. This is separate from the tier below and isn't configurable.
- **Built-in Tolerable Upper Intake Levels (UL).** Twelve more nutrients carry a real risk of harm from chronic excess, most often from supplementing rather than food alone. NuMa applies the standard adult UL for these automatically — no setup required — using the same age/sex-band pattern as the RDA table:

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

    Source: NIH Office of Dietary Supplements / Institute of Medicine Dietary Reference Intake UL summary tables[^9]. Five other tracked nutrients (potassium, thiamin, riboflavin, vitamin B12, vitamin K) simply have no established UL — the DRI tables mark these "ND" (not determinable from available data), which is different from "no risk at any dose." Magnesium, niacin, and folate are deliberately left out even though the DRI table publishes ULs for them (350 mg, 35 mg, and 1000 mcg respectively): each of those figures applies only to *supplemental* or fortified-food forms, not to the nutrient as it naturally occurs in whole food — niacin's UL guards against a flushing reaction specific to synthetic nicotinic acid/nicotinamide, and folate's guards against synthetic folic acid, neither of which whole-food niacin or folate triggers. NuMa sums whole-food intake for all three, so applying their published ULs here would flag entirely ordinary diets as "over the limit" for a risk that doesn't actually apply to them. If you take a supplement containing any of the three, that supplemental amount is exactly what the real UL is meant to track — use a [custom max limit](#maxlimits) below to watch it.
- **Your own custom max limits.** On top of (or instead of) the built-in defaults, you can set your own personal daily maximum for any nutrient -- useful if your situation calls for a stricter cap than the general guideline, or a cap on a nutrient that has no standard upper limit at all. A custom limit you set always takes precedence over the built-in default for that nutrient.

Configure your own max limits in the same place as Revised Optimal targets: **Settings → 7. Nutrient Targets**.

**Where you see it.** Every nutrient analysis table (food, recipe, meal, daily summary, trend, and the print/PDF view) has a **UL** column, far right — whichever of the tiers above applies to that nutrient (your own custom limit if you've set one, otherwise the built-in UL), shown as a plain number when there's nothing to flag. Once a max limit is active for a nutrient — whether it's a built-in default or one you set yourself — NuMa watches your logged intake for the day: when today's total for that nutrient reaches 90% of the limit, the UL column shows a highlighted amber percentage and the whole row is tinted; at or over 100%, both turn red. This check applies to your **day total**, not to any single meal or food in isolation — a max limit is a daily budget, and a single meal being close to it isn't itself meaningful without knowing the rest of the day. On a page with no day-level context (a single food's per-100g view, for instance), the UL column still shows the numeric ceiling itself, just without a live percentage against it.

The max-limit warning is independent of the Revised Optimal target feature -- you can set one, the other, both, or neither for any given nutrient.


### X. Diet-Aware Bioavailability and Deficiency Notes {: #diet-bioavailability}
Your [dietary preference](#diet) setting (Settings → Dietary preferences) is used for more than filtering protein complement suggestions -- it also shapes two parts of your daily RDA comparison, because a vegetarian or plant-based diet changes not just *what* nutrients you're likely getting, but how much of certain ones your body can actually use.

**Iron and zinc targets are raised on vegetarian and plant-based settings.** Absorbable iron comes in two forms: heme iron (from meat, fish, and poultry, absorbed efficiently) and non-heme iron (from plants, absorbed far less efficiently, and further blocked by phytate in legumes and grains -- see [Antinutrients](#antinutrients)). Zinc absorption is reduced by the same phytate. Rather than silently under-representing this, NuMa raises the iron RDA by 1.8x[^4][^5] and the zinc RDA by 1.5x[^4][^6] when your dietary preference is set to Vegetarian or Plant-based only -- figures drawn from the Institute of Medicine's Dietary Reference Intake report and the NIH Office of Dietary Supplements' fact sheets for these two minerals. This appears as a normal, higher Daily Goal on the RDA comparison and Daily Nutrient Targets screens, with an explanatory note alongside it. Setting your preference back to "All animal foods" returns both targets to their standard values.

**A B12 warning appears for the Plant-based only setting when intake is low.** Vitamin B12 is almost exclusively animal-sourced[^7] -- unlike most nutrient shortfalls, a persistently low B12 reading on a fully plant-based diet isn't something more food logging or dietary variety fixes; it typically means a B12 supplement or B12-fortified food is needed.[^7] NuMa shows this warning only when your dietary preference is Plant-based only *and* today's B12 intake is under 50% of the RDA -- vegetarians (who still eat dairy and eggs) aren't flagged, since those foods are a legitimate B12 source and an occasional low day isn't a structural gap the way it is for a fully plant-based diet. The 50% figure is NuMa's own conservative trigger for surfacing the warning, not a clinical diagnostic threshold -- an actual B12 deficiency is properly diagnosed by a blood test (serum B12, methylmalonic acid, or homocysteine), not by a single day's logged intake.

Both of these are general population guidance based on your stated preference, not personalized medical advice -- if you have a diagnosed deficiency or absorption condition, follow your clinician's specific recommendations instead.

### Y. How NutriMagnus scores meal and recipe protein quality {: #protein-scoring}
(This section explains the meal-level method. For background on single-food [DIAAS](#gloss-diaas) and how amino acid ratios work, see [Appendix B](#appendix-b).)

Single-food analysis and meal-level analysis use different methods. For a single food, NuMa computes a [DIAAS](#gloss-diaas) score directly from that food's amino acid profile and digestibility. For a recipe or logged meal, it uses the [FAO](#gloss-fao)'s endorsed method for mixed-food meals: it pools the digestible amino acids across all ingredients before scoring. The two approaches answer different questions and will give different results.

#### Why meals need their own calculation

A food that is short in one amino acid can be rescued by a companion food that supplies it generously — but only if you account for both foods together. A calculation that scores each food separately and then averages the scores misses this complementarity. The pooled method captures it correctly: amino acids from every ingredient in the meal are counted together before any ratio is computed.

#### The method, step by step

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

#### From DIAAS to digestible complete protein

    Digestible complete protein (g) = total meal protein (g) × min(DIAAS, 1.0)

If a meal contains 40 g of total protein and a [DIAAS](#gloss-diaas) of 0.82, NuMa reports 32.8 g of digestible [complete protein](#gloss-complete-protein). The remaining 7.2 g cannot be efficiently incorporated into tissue — the [limiting amino acid](#gloss-limiting-amino-acid) is exhausted before the rest of the protein can be used.

#### A worked example — two ingredients, two amino acids

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

#### A note about missing amino acid data

Not every food in the [USDA](#gloss-usda) database has a complete amino acid profile. When an ingredient is missing that data, NuMa runs the meal-level [DIAAS](#gloss-diaas) calculation using only the ingredients for which data exists, and flags the result as an estimate. The digestible [complete protein](#gloss-complete-protein) figure is then computed against only the protein that comes from those data-complete ingredients — so the result remains meaningful rather than artificially inflated.

##### Filling missing AA profiles at analysis time

When a meal contains ingredients without amino acid data, NuMa tells you how many are affected and distinguishes two situations:

- **Inside a recipe**: the ingredient is part of a recipe you logged as a meal item. Fix these by opening the recipe's ingredient editor and replacing or re-fetching the ingredient there.
- **Standalone meal ingredients**: foods you logged directly to the meal (not inside a recipe). These can be replaced on the spot: NuMa asks whether you want to search for a substitute.

If you say yes, for each affected ingredient the program opens a focused search of [USDA](#gloss-usda) SR Legacy and Foundation foods — the datasets most likely to include full amino acid profiles. The **[AA](#gloss-aa)** column in the results (✓ or ✗) shows at a glance which options have the data you need. Choosing a replacement updates that ingredient for the current analysis. Press Enter to skip an ingredient and leave it excluded from the calculation.

##### Why the first analysis of a meal can be slow

When you analyze a meal for the first time, you may see a "Fetching amino acid data…" message with a brief wait — sometimes several seconds. This is normal. NuMa is going online to download complete amino acid information for each food in the meal that doesn't already have it saved locally. Once downloaded, the data is stored on your computer, so the next time you analyze the same meal it will be fast.

---

## Part 5 — Reading Your Results
This part explains what the columns, tables, and analysis screens mean.

### A. Getting help {: #help}
Throughout this manual, **Learn more** links appear next to section headings and analysis output. Click any link to jump to the relevant explanation, or use this manual's own search box.

The sections linked from analysis output are:

- [Amino acid estimates in complement suggestions](#comp-estimate) — what "(estimated)" and "(generic estimate)" tags mean
- [Food Cache](#food-cache-web) — fetching missing amino acid data with Claude AI
- [Amino acid scoring](#aa-scoring) — limiting-amino-acid [DIAAS](#gloss-diaas) scoring method
- [Antinutrients](#antinutrients) — what [antinutrients](#gloss-antinutrient) are and how they appear in output
- [Archiving](#archive) — hiding foods, pantry entries, and recipes from everyday use without losing them
- [Bioavailability](#bioavailability) — [DIAAS](#gloss-diaas) bioavailability table columns
- [Complement suggestions](#comp) — protein [complement food](#gloss-complement-food) suggestions
- [Daily nutrient goals](#goals) — how daily nutrient goals are calculated
- [DCP cap](#dcp-cap) — why [DCP](#gloss-dcp) is sometimes capped below the [DIAAS](#gloss-diaas) projection
- [DIAAS](#diaas) — digestible indispensable amino acid score
- [Diet-aware bioavailability and deficiency notes](#diet-bioavailability) — how dietary preference raises iron/zinc targets and flags low B12
- [Dietary preferences](#diet) — dietary preferences setting
- [Digestibility overrides](#dcp-overrides) — protein digestibility overrides table
- [Digestible complete protein](#dcp) — [DCP](#gloss-dcp) concept and formula
- [Drafted food profiles](#drafted-foods) — drafted food profiles list columns
- [Essential amino acids](#aa) — [EAA](#gloss-eaa) reference and the nine indispensable amino acids
- [FAO reference values](#fao) — [FAO](#gloss-fao) 2013 amino acid reference requirement
- [Food annotation](#annotate) — annotate food picker table columns
- [Food Cache](#cached) — [Food Cache](#gloss-food-cache) column guide
- [Food comparison](#food-comparison) — food comparison table columns
- [Food import](#food-import) — foods to import review table columns
- [Food search](#food-search) — [USDA](#gloss-usda) food search results columns
- [Food use in meals](#fooduse) — food use in meals analysis table and histogram columns
- [Food use in recipes](#fooduse-recipes) — food use in recipes analysis table
- [Substituting a food or recipe](#fooduse-substitute) — bulk-replace one food/recipe with another
- [Glossary](#glossary) — abbreviations and key terms
- [Glycemic index](#gi) — glycemic index background
- [Glycemic load](#gl) — glycemic load concept and formula
- [Glycemic output](#glycemic) — glycemic load output columns
- [IAA ratios](#iaa-ratios) — meal amino acid ratios table columns
- [Limiting amino acid](#gap) — amino acid gaps and how they are scored
- [Maximum nutrient limits](#maxlimits) — custom per-day nutrient caps and the near-limit warning
- [Meal history](#meal-history) — meal history search result tables
- [Meal items](#meal-detail) — meal items table columns
- [Meal protein digestibility](#meal-diaas) — meal protein digestibility analysis columns
- [Meals list](#meals-list) — Meals & Log list columns
- [Meals & Log columns](#meal-columns) — choosing extra nutrient columns for the Meals & Log list
- [Missing amino acid profiles](#missing-aa) — missing amino acid profile warnings
- [My Pantry](#pantry) — [My Pantry](#gloss-my-pantry) table columns
- [N-Day nutrient trend](#trend) — averaging intake across logged days to catch chronic shortfalls
- [Nutrient analysis](#nutrients) — nutrient analysis table columns and groups
- [Nutrient plot](#nutrient-plot) — line chart of chosen nutrients across logged days (web)
- [Omega-3 fatty acids](#omega3) — ALA, EPA, DHA, and why only ALA has a Daily Goal
- [Oxalate data](#oxalate) — [oxalate](#gloss-oxalate) data source, enabling, matching, and limitations
- [Per-day profile tracking](#day-profile) — how a logged day stays pinned to the profile active when it was saved, and how to change it
- [Plot File Formats](#plot-file-formats) — PNG vs. SVG, and which to pick when downloading a chart
- [Profile Optimal targets](#optimal) — custom per-nutrient targets above the standard RDA
- [Protein completeness](#complete) — what makes a protein "complete"
- [Protein quality](#protein-quality) — single-food amino acid ratios table columns
- [RDA](#rda) — daily intake vs. recommended values table
- [Recipe comparison](#recipe-comparison) — recipe comparison ingredient and nutrient tables
- [Recipe ingredients](#recipe-ingredients) — recipe ingredient list columns
- [Recipes list](#recipes) — recipes list table columns


### B. Reading the output

#### Food Cache — Column Guide {: #cached}
The Food Cache list shows every food you have stored locally, sortable by Name, Type, DIAAS, or GI estimate. Columns:

    Compare  Checkbox to add this food to Compare Foods — see Compare selected.

    ID       Database identifier.
             A plain number = USDA FoodData Central FDC ID.
             "OFF"          = Open Food Facts (community-contributed data).
             Other id styles (CNF, CoFID, AFCD, CIQUAL) show as their source's
             own row in the ID column when applicable.

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
               User Drafted   — Created or edited by hand in NuMa.

    AA       Amino acid data status.
               ✓  Amino acid data is present in your cache for this food.
               —  No amino acid data — common for branded and packaged foods.

    GI est.  Your saved glycemic index estimate for this food, if any.
             GI reflects how quickly a food raises blood glucose (scale 0-100).
             See [Glycemic Index](#gi) for a full explanation.

    DIAAS    Your saved DIAAS estimate for this food, if any.
             DIAAS (Digestible Indispensable Amino Acid Score) rates protein
             quality: 1.00 = complete, lower = a limiting amino acid is present.
             See [DIAAS](#diaas) for details. Shown with a star when it's your
             own saved estimate rather than the built-in reference-table value.

    Notes    A "Notes ▸" link expands to show any saved notes and curator
             notes (curator notes are typically added by the Claude data-fetch
             workflow) — blank if neither is present.

    Actions  Portions, Refresh, Archive/Restore, and Delete for that row —
             see [Food Cache](#food-cache-web) in Part 3.

See [Food Cache](#food-cache-web) in Part 3 for the available actions on each row (Portions, Refresh, Archive/Restore, Delete, Prune unused foods) and how to fetch missing amino acid data with Claude AI.


#### Archiving {: #archive}
Archiving lets you keep a food, pantry entry, or recipe without losing it, while hiding it from everyday use: default list views, food search results, and protein complement suggestions. It's meant for things you're not currently using but don't want to delete -- a seasonal ingredient, an old recipe you might revisit, a pantry item you've used up.

Archiving is reversible with the same action, one entry at a time: an **Archive/Restore** button on each row in the Food Cache, My Pantry, and Recipes pages toggles the state; a **Show archived** checkbox on each of those pages toggles whether archived entries are shown at all.

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

If you try to archive a food or recipe that's still actively referenced elsewhere (a pantry entry, a recipe ingredient, a logged meal), NuMa warns you first but lets you proceed -- the references keep working either way.

This setting (which entries are archived, and whether each list shows them) is saved and persists across sessions.


#### Nutrient Analysis Table {: #nutrients}
Shows the nutritional content of a food, recipe, or meal portion, grouped by category (Macronutrients, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients)).

Columns:

    Nutrient     Name of the nutrient.
    Amount       Value for the portion you entered.
    Unit         kcal for calories; g for macronutrients (protein, fat,
                 carbs, fiber, omega fatty acids); mg or mcg for minerals
                 and vitamins.

When analyzing a meal within a full-day context, three additional columns appear:

    meal %       This meal's contribution to your daily goal, in percent.
    day total %  All meals logged today as a percentage of your daily goal.
    Daily goal   Your personalized nutrient target for the day.

#### Color coding (meal % and day total % columns)
    Green    At or above the daily minimum, or within the upper limit for
             capped nutrients (sodium).
    Yellow   Getting close but not there yet.
    Red      Significantly short of the minimum, or over the limit.

If you have configured a Profile Optimal target for any nutrient (Settings → Nutrient targets), the table gains a second set of the same columns under a "Profile Optimal" heading, alongside the standard "Profile RDA" columns. Nutrients you have not customized show a dash ("–") in the Optimal columns. See [Profile Optimal Targets](#optimal) for details.

If you have configured a custom max limit for a nutrient, its row is highlighted (yellow, then red) once today's total is within 10% of that limit. See [Maximum Nutrient Limits](#maxlimits) for details.

[Phytonutrients](#gloss-phytonutrients) (carotenoids, choline, isoflavones, etc.) appear only when [USDA](#gloss-usda) data for that food includes those values -- many foods have none. Amino acids are not in this table; see the Protein Quality section below it.

See [daily nutrient goals](#goals) to see how your daily goals are calculated. See [RDA](#rda) to see the Daily Intake vs. Recommended Values table.


#### Top Contributors Table {: #top-contributors}
Shows on meal and recipe detail pages, just above the Nutrient Analysis Table. Pick any tracked nutrient from the **Rank by** dropdown and see which foods in that meal or recipe supply the most of it, ranked highest to lowest.

Columns:

    Food / Recipe   Name of the contributing food, linked to its detail page.
                    On a meal's table, the header just says "Food" — any
                    recipe used in that meal is broken into its individual
                    foods for this table, so no row ever names a whole
                    recipe. (A recipe's own Top Contributors table can
                    legitimately show a sub-recipe by name, so it keeps the
                    "Food / Recipe" header.)
    Amount          This food's contribution, in the selected nutrient's unit.
    % of total      This food's share of the summed contribution across every
                    food in the meal or recipe (not a percent of any daily
                    target — see [Nutrient Analysis Table](#nutrients) for that).

A **Show** control next to the picker limits the list to the top 5/10/15/20/30 foods, or all of them (defaults to 10); it only offers choices that would actually shorten the list, so a meal with 6 contributors just offers "5" or "All." A "Total, all contributors" row at the bottom of the table always reflects every contributor, even when the list above it is trimmed.

Ranking by **Protein** is special: instead of raw protein grams, it ranks each food by its own standalone [digestible complete protein](#dcp) ([DCP](#gloss-dcp)) — what that food alone would contribute after accounting for amino acid digestibility and completeness, using the same [DIAAS](#diaas) math as Protein Summary above it, applied to that one food in isolation. A note below the table explains this distinction and links back to Protein Summary. Because combining foods can raise a meal's *actual* DCP above what any single food scores alone — [protein complementarity](#comp) is the whole point of DIAAS — this table's total will typically be lower than, and should not be read as equal to, the real meal DCP shown in Protein Summary. Foods with no amino acid data on file don't score a DCP and are omitted from the ranking when Protein is selected.


#### Protein Quality Table {: #protein-quality}
Shows how a food's amino acid profile compares to the [FAO](#gloss-fao) 2013 reference pattern. Appears below the nutrient table when amino acid data is available.

The header line tells you whether the protein is Complete (all nine essential amino acids at or above the [FAO](#gloss-fao) reference) or Incomplete (at least one is limiting), and which amino acid is most limiting.

Columns:

    Amino Acid   Name, using FAO pair notation where applicable
                 (Met+Cys, Phe+Tyr).
    Raw ratio    Milligrams of this amino acid per gram of protein, divided
                 by the FAO reference value. 1.0 = exactly meets the
                 reference. Below 1.0 = limiting. Above 1.0 = surplus.
    Adj.         Raw ratio multiplied by the food's DIAAS digestibility
                 coefficient. Appears only when a DIAAS value is saved.
                 The bar chart and completeness classification use this
                 adjusted value when it is available.
    Bar          Visual indicator: each full block represents 0.10, capped
                 at 2.0 (20 blocks).

Color: Green = at or above 1.0 (after adjustment if Adj. is present). Yellow = below 1.0.

See [DIAAS](#diaas) for the [DIAAS](#gloss-diaas) concept. See [limiting amino acid](#gap) to understand what "limiting" means. See [FAO reference values](#fao) for the [FAO](#gloss-fao) reference values used for each amino acid.


#### Meal Protein Digestibility Analysis {: #meal-diaas}
Step 1 of the meal [DIAAS](#gloss-diaas) calculation. Shows how much protein from each ingredient actually reaches your bloodstream -- before the [limiting amino acid](#gloss-limiting-amino-acid) penalty is applied. Rows are sorted by raw protein, highest first, so the foods actually driving the meal's or recipe's numbers are at the top.

On food and recipe pages, this table also has a DCP column. That DCP is just each food's raw protein times one shared meal- or recipe-wide score, so it's not that food's own standalone protein quality — two foods can show the same DCP simply by contributing equal protein, even with very different amino acid profiles, and that shared multiplier is also why sorting by protein and by DCP land on the same order. See [Top Contributors](#top-contributors) for each food's own standalone quality instead.

Columns:

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

#### Suffixes in the Digestibility column
    ~est    Estimated from food category average; no measured value for
            this specific food.
    user    You set a custom value (Settings → 6. Protein Digestibility
            Overrides — see [Digestibility overrides](#dcp-overrides)).

Ingredients contributing less than 1 g of protein are omitted from this table as negligible; the totals row sums only the ingredients shown.

Note: the "Total digestible protein" here is step 1 of a two-step method. Step 2 (the [DIAAS](#gloss-diaas) limiting-amino-acid penalty) reduces it further. See [amino acid scoring](#aa-scoring) for the full step-by-step method. See [DIAAS](#diaas) for background on [DIAAS](#gloss-diaas) and true [ileal digestibility](#gloss-ileal-digestibility).


#### Meal Amino Acid Ratios Table {: #iaa-ratios}
Step 2 of the meal [DIAAS](#gloss-diaas) calculation. Shows the pooled amino acid supply across the whole meal, expressed as a ratio vs. the [FAO](#gloss-fao) 2013 reference.

Columns:

    Amino Acid   Essential amino acid (FAO pair notation for Met+Cys and
                 Phe+Tyr).
    Ratio        Pooled digestible grams of this AA from all ingredients,
                 divided by (FAO reference value x total meal protein).
                 1.0 = exactly meets the reference. Below 1.0 = shortfall.
                 Above 1.0 = surplus.
    Bar          Visual indicator; each block = 0.10, capped at 2.0.

The amino acid with the lowest ratio is the [limiting amino acid](#gloss-limiting-amino-acid), marked "LIMITING". The meal [DIAAS](#gloss-diaas) score equals that lowest ratio (capped at 1.0).

#### Color coding
    Green    1.0 or above.
    Yellow   0.80-0.99.
    Red      Below 0.80.

The panel below this table shows the final Digestible [Complete Protein](#gloss-complete-protein) figure: total meal protein x the [DIAAS](#gloss-diaas) score.

See [DIAAS](#diaas) for the [DIAAS](#gloss-diaas) concept. See [amino acid scoring](#aa-scoring) for the step-by-step two-stage calculation method. See [digestible complete protein](#dcp) for Digestible [Complete Protein](#gloss-complete-protein).


#### Bioavailability Table {: #bioavailability}
This section appears in two forms depending on context.

#### SINGLE FOOD (labeled BIOAVAILABILITY)

Shown when viewing a food with a saved [DIAAS](#gloss-diaas) estimate. Displays:

    - Protein digestibility score (literature DIAAS, 0.00-2.00 scale).
    - A bar proportional to the score.
    - Digestible protein in grams from this portion.
    - Digestible complete protein (when amino acid data is also present).
    - Antinutrient notes when applicable (phytates, oxalates, lectins,
      bound niacin). Each note names the compound, describes the specific
      problem, and lists preparation steps that reduce the effect.
      See [Antinutrients](#antinutrients) for a full explanation of what these notes mean.

#### RECIPE PER SERVING (labeled BIOAVAILABILITY -- PER SERVING)

Per-ingredient table in recipe analysis. Columns:

    ID              FDC ID, OFF, or usr.
    Ingredient      Name.
    Serving         Grams of this ingredient in one recipe serving.
    Crude protein   Raw protein from this ingredient (g per serving).
    Digestibility   True ileal digestibility coefficient (0.00-1.00).
    Limiting IAA    Most-limiting amino acid for this ingredient, or
                    "-- (complete)" if none.
    Digestible      Crude protein x Digestibility (g).

Color for Digestibility: Green 0.90+, Yellow 0.70-0.89, Red below 0.70.

A summary panel below the table shows total digestible protein and the [pooled DIAAS](#gloss-pooled-diaas) score for one recipe serving.

See [DIAAS](#diaas) for [DIAAS](#gloss-diaas) background. See [digestible complete protein](#dcp) for Digestible [Complete Protein](#gloss-complete-protein). See [complement suggestions](#comp) for [complement food](#gloss-complement-food) suggestions.


#### Meals and Log List {: #meals-list}
The main Meals & Log screen lists your recent meals, 9 at a time by default, sorted by date (most recent first). Change the sort order — Date, Name, Meal DCP, or Calories — via the sort dropdown; your choice is remembered as the default the next time you open Meals & Log. A **Number shown** field raises or lowers how many meals are listed, and a **Show meals on or before** date filter narrows the list to a cutoff date — both persist in the page's own controls, not as separate "older/newer" pagination links.

Columns:

    Date            Date of the meal (YYYY-MM-DD).
    Complete        Checkmark when you have marked the meal finished
                    (a Mark complete / Mark incomplete button on the meal page).
    Meal            Name you gave the meal (e.g. Breakfast, Lunch).
    Items           Number of foods and recipes logged in this meal.
    Meal DCP        Bioavailable complete protein for this meal alone (g).
    Day DCP         Sum of DCP for every meal on this date with a computed
                    value — including meals not yet marked complete, since
                    DCP is auto-saved as you add items. If any contributing
                    meal isn't marked complete, the total is flagged with
                    an asterisk (*) as provisional, since it may still
                    change. Shown on the topmost row for each date only.
    % profile goal  Day DCP as a percentage of your daily protein target.
                    Also flagged with * when provisional. Shown on the
                    topmost row for each date only.
    Calories        Calories for this meal alone.

You can add up to 6 more nutrient columns of your own choosing — see
[Meals & Log columns](#meal-columns).

[DCP](#gloss-dcp) and Calories values start as -- and are computed on demand.
Opening and analyzing a meal also saves its DCP and calories automatically.

    --    Not yet computed. Use the "Calculate DCP and calories for" dropdown
          and Calculate button to compute for all complete meals, the last 30
          days, or the last 10 days (results are saved permanently).
    n/a   Computed but no amino acid data (DCP) or nutrient data (calories)
          was available.

% profile goal requires a user profile (Settings -> User profile). Blank if no profile is set.

Click a meal to view or edit it, or delete it from there. **Search meal history** (a separate page, linked from Meals & Log) searches every logged food/recipe item by name only — no date filter, sort control, or pagination of its own. Results show a flat "All Occurrences" table (one row per time that food or recipe was logged, linked to its meal) and a "Summary by Food" table grouping those occurrences by name with times-used count, total grams, and first/last-seen dates. Ingredients inside a logged recipe aren't searched — only the recipe itself, by name.

See [digestible complete protein](#dcp) for a full explanation of digestible [complete protein](#gloss-complete-protein). See [daily nutrient goals](#goals) to see how your daily protein target is calculated.


#### Meals & Log Columns {: #meal-columns}
The Meals & Log list always shows Calories, plus up to 6 more nutrients you
choose yourself — e.g. Sodium, Fiber, Vitamin D, or any amino acid.

To choose them: Settings -> section 8 "Meals & Log columns". Pick each nutrient's position (1 =
leftmost); leave a nutrient's position blank to hide it. This choice is saved
automatically.

Values for these columns come from the same computed snapshot as [DCP](#gloss-dcp)
and Calories, so they show -- until computed and n/a if the ingredient data
doesn't cover that nutrient. Use the Calculate button on the Meals & Log screen
(or analyze a meal) to compute them.

The same chosen columns also appear on the Daily Summary's Recent Days table
(Analysis -> Daily Summary), aggregated per day instead of per meal -- so a
day's Sodium column, for example, is the sum of every meal logged that day.

On both lists (web), a column with a unit stacks it onto its own line below
the nutrient's name (e.g. "Vitamin D" over "(mcg)"), matching the built-in
Meal DCP / Day DCP / % goal columns -- so each column takes up roughly half
the width it otherwise would.

**Recent Days also always shows four columns right after Day DCP, regardless
of what you've chosen above:** Protein (the raw, un-adjusted total -- Day DCP
is the digestibility-adjusted figure), Calories, Carbs (carbohydrates --
sugars and starches), and Fiber. These aren't part of your 6-column choice
and can't be turned off; if you'd separately picked one of them as a Meals &
Log column, it's simply not duplicated on Recent Days.

Recent Days' column headers stack a nutrient's unit onto its own line below
the name (e.g. "Vitamin D" over "(mcg)") instead of running both on one
line, so each column takes up roughly half the width it otherwise would --
letting more columns fit on screen at once.


#### Meal Items Table {: #meal-detail}
Shows the foods and recipes logged in a single meal.

Columns:

    Food /    Name of the food or recipe, linked to its own analysis page.
    Recipe    Each shows its source-database ID tag; a deleted-but-still-
              referenced recipe is flagged "(recipe deleted)".
    Amount    Portion recorded: grams for foods, or serving count for
              recipes. Volume unit labels are shown where applicable.
    Notes     Any note saved with this item, if present.

An **Edit** button on each row opens a popup to change the amount/servings and notes without leaving the page; an **✕** button removes that item from the meal (both ask no separate confirmation — Edit requires clicking "Save changes", and Remove acts immediately). Use the "Add Food or Recipe" search above the table to add a new item.


#### Food Use in Meals — Column Guide {: #fooduse}
Analysis -> Food use in meals tabulates which foods appear across a set of
meals you choose. You pick one selection method — one or more date ranges,
or a list of specific meal IDs (not both in the same run) — then choose
whether to include all foods or only protein-containing foods
(more than 0 g of protein per 100 g).

Columns:

    ID          USDA FDC ID for foods. Blank for recipe rows.
    Food        Food or recipe name. Recipe rows are shown in bold.
    Kind        "recipe" for recipe rows, blank for individual foods.
    Days used   Number of distinct calendar days on which this food or
                recipe appeared, within the meals you selected.
    Meals       Number of selected meals containing this food or recipe.

Rows are ranked most- to least-used by Days used (ties broken by Meals, then
name), with a bar showing relative frequency.

Recipe items are counted twice: once as the recipe itself, and again as each
of its ingredients (recursively expanded through any nested recipes), so both
the dish and its components show up in the ranking.

Recipe rows always show the recipe's *current* name and are grouped by its
stable ID — if you rename a recipe after logging it in meals, this analysis
still finds and merges every occurrence under the new name rather than
splitting them across old and new names or dropping them. Food rows work the
same way: the name shown is always the food's current cached name, even for
a meal logged before you last renamed it.

An expandable **Substitute a food or recipe** panel above the results lets
you bulk-replace one food or recipe with another across the meals currently
selected — see [Substituting a Food or Recipe](#fooduse-substitute).


#### Food Use in Recipes — Column Guide {: #fooduse-recipes}
Analysis -> Food use in recipes tabulates which foods and sub-recipes appear
as *ingredients* across a set of recipes you choose — the recipe-book
equivalent of Food Use in Meals. Pick one selection method: all recipes
(the default), one or more date ranges by when the recipe was created, or a
list of specific recipe IDs, then optionally limit to protein-containing
foods.

Columns:

    ID                  USDA FDC ID for foods. Blank for sub-recipe rows.
    Food / Recipe       Food or sub-recipe name. Sub-recipe rows are shown
                        in bold.
    Kind                "recipe" for sub-recipe rows, blank for individual
                        foods.
    Recipes used in     Number of selected (container) recipes whose
                        ingredient list contains this food or sub-recipe,
                        directly or nested inside another sub-recipe.

Rows are ranked most- to least-used, with a bar showing what percentage of
the selected recipes use each item. A sub-recipe used as an ingredient (e.g.
a house dressing used in several salads) gets its own row — its own
ingredients are also listed individually, the same way a directly-added
recipe on Food Use in Meals shows up both as itself and as its expanded
ingredients.

This page has the same **Substitute a food or recipe** panel as Food Use in
Meals, scoped to ingredients of the recipes currently selected — see
[Substituting a Food or Recipe](#fooduse-substitute).


#### Substituting (Replacing) a Food or Recipe {: #fooduse-substitute}
Both Food Use in Meals and Food Use in Recipes have a **Substitute a food or
recipe** panel that bulk-replaces every occurrence of one food or recipe
with another, restricted to whatever's currently selected on that page (the
same date range(s) or ID list you searched with).

You can also reach this replacement tool directly from a blocked deletion:
if Food Cache or Custom Food Profiles refuses to delete a food because it's
still used in a recipe or a meal, the "swap it for a different food" link in
that message brings you here with those exact recipes/meals already
selected and the food already filled in as the one to replace — you only
need to supply the replacement's kind and ID.

This is the tool for the common situation where a rename — or re-adding a
food from a search instead of reusing what was already in your cache — has
left what looks like two different foods, when really it's one food you
just want to consolidate under a single, newer entry. Fill in:

    Replace this   The old item's kind (Food or Recipe) and ID number.
    With this      The replacement's kind and ID number.

The results table below the form shows what's *currently used* in this
selection, not a list of foods you could replace with — it's there so you
can confirm what you're about to change (the item you're replacing, if any,
is marked "replacing this" in that table). To find the ID of the
**replacement** item, look it up on [Food Search](#food-search) or the
Recipes list (both open in a new tab from links right above the form) —
each shows the ID in its results.

You can mix kinds — replace a food with a recipe or vice versa — since both
meal items and recipe ingredients can point at either one. The amount and
unit already recorded are kept as-is; only *what* the entry points to
changes, so double-check the replacement's portion makes sense afterward if
the two items aren't measured the same way.

On **Food Use in Meals**, substitution only reaches items added *directly*
to a meal — a food used inside a recipe is part of that recipe's own
ingredient list, not the meal's, so substitute it from **Food Use in
Recipes** instead, scoped to that recipe. On **Food Use in Recipes**,
substitution updates every selected recipe's ingredient list and recomputes
each changed recipe's DCP automatically — including cascading up to any
recipe that in turn uses one of them as a sub-recipe.

A recipe can never be substituted into referencing itself; that combination
is silently skipped rather than creating a broken self-reference.

This writes to the database immediately when you click through the
confirmation prompt — there's no automatic undo, so it's worth double-
checking the ID numbers first.


#### Glycemic Load Output {: #glycemic}
Shows the estimated glycemic load ([GL](#gloss-gl)) for a meal or recipe.

The number displayed is the total [GL](#gloss-gl). Color coding:

    Green   10 or below (low glycemic impact).
    Yellow  11-19 (medium).
    Red     20 or above (high).

When the output reads "Not available -- GI annotation missing for: ...", one or more foods lack a [GI](#gloss-gi) value. [GL](#gloss-gl) cannot be computed without [GI](#gloss-gi) data for every single ingredient — one missing value blocks the whole total. To fix this, annotate the listed foods via Foods → Annotate, or edit the food directly from the Food Cache.

[GL](#gloss-gl) = ([GI](#gloss-gi) x grams of available carbohydrate) / 100 per ingredient, summed across all ingredients in the meal.

[GL](#gloss-gl) is shown for reference only and does not affect protein quality scores. See [glycemic load](#gl) for a full explanation of glycemic load and its limitations. See [glycemic index](#gi) for background on the glycemic index.


#### Meal History Tables {: #meal-history}
These tables appear when you search your meal history with s from the Meals & Log list. Results can be shown as Flat (every occurrence), Summary (totals per food), or Both.

#### MEAL HISTORY -- OCCURRENCES
Every time a food or recipe appeared in any logged meal.

    Date        Date of the meal.
    Meal        Name of the meal.
    Food/Recipe Name of the food or recipe. Recipe items show "(recipe)".
    Portion     Amount logged: grams for foods, serving count for recipes.
    Notes       Your note for that item, if any.

#### MEAL HISTORY -- SUMMARY
Totals per food across all matching meals.

    Food/Recipe Name of the food or recipe.
    Times       Number of times this food has been logged.
    Total       Total grams logged (-- for recipes, which are measured in
                servings rather than grams).
    First       Date of the earliest logged occurrence.
    Last        Date of the most recent logged occurrence.

Note: only foods and recipes logged directly as meal items appear here. Ingredients inside a logged recipe are not individually searchable.


#### Missing Amino Acid Profiles {: #missing-aa}
When a meal contains ingredients without amino acid data, NuMa cannot include them in the [pooled DIAAS](#gloss-pooled-diaas) calculation. This section lists the affected ingredients and describes your options.

NuMa distinguishes two cases:

Standalone meal ingredients: foods logged directly in the meal.

    These can often be replaced on the spot. NuMa can search for
    a USDA Foundation or SR Legacy substitute with amino acid data.

Inside a recipe: ingredients that are part of a recipe you logged.

    These must be fixed by editing that recipe (Recipes -> browse -> edit)
    and replacing the problematic ingredient there.

It's safe to ignore when the affected food contributes negligible protein (garnish, spice, a small amount of fruit). It matters more when the food is a significant protein source in your meal. Foods contributing less than 1 g of protein are treated as negligible and left off this list entirely (a footnote tells you when items were omitted this way).

The [DIAAS](#gloss-diaas) calculation runs on whichever ingredients do have [AA](#gloss-aa) data. The result is flagged as an estimate, and the [DCP](#gloss-dcp) figure reflects only the protein from data-complete ingredients.

See [meal protein digestibility](#meal-diaas) to see the digestibility table. See [DIAAS](#diaas) for [DIAAS](#gloss-diaas) background.


#### Recipes List Table {: #recipes}
Shows all your saved recipes. Sorted by Last accessed by default; use the sort dropdown (not available while a search filter is active) to switch to Name or DCP/serving instead. Your choice is remembered as the default the next time you browse recipes.

Columns:

    ID          Recipe ID.
    Name        Recipe name; click it to open the recipe.
    Description Short recipe description, if any.
    Servings    Number of servings. 0 means the recipe is analyzed by
                total weight or volume rather than a serving count.
    DCP/srv     Digestible complete protein per serving (g). Recomputed and
                saved automatically whenever the recipe or its ingredients
                change — no separate analysis step is needed. Shown as
                NC (not computed) if servings is 0, no ingredient has a
                known weight, or an ingredient with 1 g or more of protein
                has no amino acid data. Minor contributors missing amino
                acid data (under 1 g of protein — spices, oil, salt, a
                trace of chocolate) don't block the calculation — only
                significant ones do, since an approximate DCP is never
                saved as if it were exact. The 1 g floor is absolute: it
                doesn't matter what fraction of the recipe's total protein
                that 1 g represents. The "Recompute DCP for all recipes"
                button above the table recomputes every recipe at once.
    Complete    Checkmark if you have marked the recipe finished.
    Created     Date the recipe was first saved.

Each row has **Edit**, **Copy**, **Archive/Restore**, and **Delete** buttons. A filter box narrows the list by name; a **Sort by** dropdown switches between Last accessed, Name, and DCP/serving; a **Show archived** checkbox reveals archived recipes (shown grayed out with an "Archived" badge — see [archiving](#archive)). A **Broken recipe references** link finds ingredients pointing at a food or recipe no longer in your cache.

See [digestible complete protein](#dcp) for a full explanation of digestible [complete protein](#gloss-complete-protein).


#### Recipe Comparison Tables {: #recipe-comparison}
Shows up to six recipes side-by-side in two tables: an ingredient table and a nutrient table.

The **ingredient table** has one row per distinct ingredient name across the recipes you're comparing, one column per recipe, showing that ingredient's amount in each recipe or "--" if it isn't used. Ingredients shared by two or more recipes are listed first (highlighted) — that's usually the interesting question when comparing recipes: which ingredients differ, and by how much. A sub-recipe used as an ingredient shows its serving count rather than being expanded into its own raw ingredients.

The **nutrient table** reuses the same layout as [food comparison](#food-comparison) — all nutrient groups, highest value per row highlighted, sortable by checked nutrients. A toggle switches the basis between **Per serving** (each recipe's nutrients divided by its own serving count — the fair way to compare recipes with different batch sizes) and **Whole recipe** (the full batch as authored).

To run a comparison: Recipes -> Compare recipes. Search adds from your own saved recipes only (recipe comparison doesn't reach out to USDA/OFF, since a recipe only exists in your database). As with [Compare Foods](#food-comparison), you can save the recipe list under a name for quick reuse in future sessions — previously saved lists are offered at the start of the comparison flow.


#### Recipe Ingredient List {: #recipe-ingredients}
Shows the current ingredients in a recipe during create, develop, or edit. Refreshes after each change so you can see the current state.

Columns:

    #       Row number. Use with Remove (option 3) and Reorder (option 4)
            in the ingredient edit menu.
    Amount  Portion entered: e.g. "175g", "1 T", "2 servings".
    ID      Database identifier for this ingredient.
              A number = USDA FDC ID.
              OFF      = Open Food Facts.
              usr      = User-drafted custom food.
              recipe   = This ingredient is itself a saved recipe (nested).
    Food    Ingredient name.

Nested recipes (ID = recipe) have their nutrients scaled automatically from their recorded serving count and total weight.

**Unsaved recipe-details edits and adding an ingredient.** The Recipe details fields (name, servings, instructions, etc.) at the top of the Edit Recipe page save separately from the ingredient list — clicking "Add to recipe" doesn't normally touch them. If you've changed one of those fields without clicking "Save recipe details" yet and then add an ingredient, a warning appears: adding the ingredient will save those pending changes for you rather than silently discard them. Choose Cancel to go back and finish editing those fields first, or Continue to save them and add the ingredient in one step.


#### USDA Food Search Results {: #food-search}
Listed after a food search. Combines matches from [USDA](#gloss-usda) FoodData Central, Open Food Facts[^3], and your local [Food Cache](#gloss-food-cache).

Columns:

    AA      Amino acid data status.
              checkmark    Confirmed in your local cache.
              ~checkmark   Likely available (Foundation/SR Legacy not yet
                           fetched); confirmed on selection.
              X            No amino acid data.

    Search results carry only a food's name and type — USDA's search results
    don't include nutrient values up front, so "~checkmark" is a guess, not a
    fact. Opening a food's page (or adding it to a meal/recipe) fetches and
    caches its full details, which is when "~checkmark" turns into a confirmed
    checkmark or X. On the web app, you can also check a batch of "~checkmark"
    results directly from the search list: tick their checkboxes (or the
    header checkbox to select all of them) and click "Fetch full details for
    selected" — this avoids looking up every uncached result on every single
    search, which would use up more of your daily USDA search allowance than
    necessary.
    GI      Your saved glycemic index estimate, if any. See [Glycemic Index](#gi).
    DIAAS   Your saved DIAAS estimate, if any. See [DIAAS](#diaas).
    CONF.   Checkmark if a confidence/source note is saved. View it from
            the Food Cache.
    ID#     USDA FDC ID, OFF (Open Food Facts), or usr (user-drafted).
    Name    Food name.
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

To select: click the result. If the food is not yet in your cache, NuMa fetches and saves it automatically.

**Compare selected.**{: #compare-checkboxes} Every row also has a checkbox in its own **Compare** column — check the foods and/or recipes you want, then click **Compare nutrition of selected foods (up to 8)** or **Compare nutrition of selected recipes (up to 6)** above the table to jump straight to [Compare Foods](#food-comparison) or [Compare Recipes](#recipe-comparison) with those items already added, no need to redo the search there. Foods and recipes use separate checkboxes and buttons since the two comparison pages can't mix them. The same checkbox-and-button pair appears on [Food Cache](#food-cache-web), [My Pantry](#pantry)'s pantry list, and the [Recipes list](#recipes-menu-web) — each jumps into the matching comparison page from wherever you're already looking at a food or recipe.

**Sort order.** Results can be ordered two ways — a dropdown above the results table lets you switch, and your choice is remembered as the default for next time:

    Best match to name (default)   See "Ordering food search results" in
                                    Part 6 for how this ranking works.
    Pantry, Cache, then Other       Same match-quality ranking, but when two
                                    or more results are tied on how well they
                                    matched your search, your own Pantry,
                                    then Cache, then Recipe entries sort
                                    ahead of USDA/OFF/other external results
                                    within that tie. It never lets a weaker
                                    match from your own data outrank a
                                    stronger external match.

Both modes group your own Pantry/Food Cache/Recipe matches under their own heading above a divider, with external results below — but that heading reflects where the top-ranked matches happen to sort, not a hard rule; a strong external match can still land ahead of a weak local one under either sort mode.

See [Ordering food search results](#search-ranking) in Part 6 for the full explanation.

**Source filter.** A row of checkboxes next to the search box itself — visible before you've even typed a query, not just after results come back — narrows the list to any combination of sources you check: Pantry, Food Cache, Recipes, USDA FoodData Central, Open Food Facts, Canadian Nutrient File, CoFID, AFCD, CIQUAL (USDA and Open Food Facts, the two most-used external sources, lead the external group). Check as many as you like; unchecking every box is treated the same as checking them all, since a filter that hides everything isn't useful. Each checkbox is labeled with the short badge used elsewhere plus its full name (e.g. "USDA — USDA FoodData Central") and re-runs the search the moment you check or uncheck it. A **Select all sources** button re-checks every box in one click. A **What are these sources? →** link next to the "Source" label jumps to [Food data — where it comes from and how it is stored](#food-data). Your choice is sticky across every search box that has this filter, the same way the sort-order choice is. It appears next to every food search in the app: the standalone Foods → Search page, Analyze a Food Portion, Convert a Portion, Compare Foods, My Pantry's "Add a food" search, the Meals & Log "Add Food or Recipe" panel, a recipe's ingredient search, and the two "copy from another food" searches on the Edit Custom Profile page.

**Omitted-source warning.** Because the Source filter is sticky, a box unchecked once (even by accident, or while narrowing down a different search) stays unchecked everywhere until you re-check it — silently, with no visual difference from a normal search. If that hides a food you expected to see, it can look exactly like a search or ranking bug rather than a filter setting. On the Foods search page and the Meals & Log "Add Food or Recipe" panel, whenever one or more sources are unchecked, a small red note appears next to the Sort by control — **Omitted from search: RECIPE**, for example — naming exactly which ones. Check the Source filter row below to bring them back.

While a live database (USDA, Open Food Facts, or Canadian Nutrient File) is being searched, a status line names exactly which ones it's contacting — just "Searching USDA FoodData Central…" if you've unchecked the other two, for instance. If you've unchecked all three, that line (and the network requests behind it) doesn't appear at all. CoFID, AFCD, and CIQUAL are different: each is a bundled dataset, not a live lookup, so their results appear instantly alongside your own Pantry/Cache/Recipe matches — checking or unchecking any of them never triggers a network wait.

**Result limit.** A "Show up to ___ search results" box next to the Source filter controls how many results are fetched and shown, per source (default 25, up to 500). Type a number and press Enter or click Search to apply it — like the Source filter, your choice is remembered as the default for next time.

See [Food Cache](#cached) for the [Food Cache](#gloss-food-cache) column guide. See [Food Cache](#food-cache-web) to learn how to get missing amino acid data via Claude AI.


#### Food Comparison Table {: #food-comparison}
Shows up to eight foods or recipe portions side-by-side, with all nutrient groups in one table. All values are per the portion you entered for each food, not per 100 g.

The foods and portions you chose are listed above the table as Food 1, Food 2, etc. — each row also shows an **AA** column indicating at a glance whether that food has amino acid data (✓) or not (✗).

Nutrient groups: Macronutrients, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients), Amino Acids. Groups appear only when at least one food has data for that category.

    Green   The highest value in that row across all foods.
    --      No data for this nutrient in this food.

Rows where every food shows -- are hidden automatically.

**Print comparison table** and **Download CSV** buttons appear above the table: Print opens your browser's print dialog with just the comparison table (no nav, search box, or other page chrome); the CSV download gives one row per nutrient and one column per food, ready to open in a spreadsheet.

To run a comparison: Foods -> Compare foods side-by-side. You can save the food list under a name for quick reuse in future sessions. Previously saved lists are offered at the start of the comparison flow.


#### Annotate Food Picker Table {: #annotate}
Appears when you choose Foods -> Annotate a food. Pick a food from your cache to annotate.

Columns:

    #       Row number. Type the number to select that food.
    Name    Food name.
    Type    USDA data category or OFF. See [Food Search](#food-search) for type meanings.

Type /text to filter by food name (e.g. /tofu shows only tofu entries). Type / alone to clear the filter.

After selecting a food, you can add or update:

    GI      Glycemic index (0-100). See [Glycemic Index](#gi).
    DIAAS   Your protein quality estimate (0.00-2.00). Useful for packaged
            foods that lack amino acid data in USDA. See [DIAAS](#diaas).
    Prep    A short preparation note (e.g. "boiled 20 min", "raw").

Annotations appear wherever that food is used: [Food Cache](#gloss-food-cache) list, food and recipe analysis, and meal analysis.


#### Foods to Import Review Table {: #food-import}
Appears when you click Review on the Import Claude response page, to import the data Claude gave you. Shows a preview so you can review before confirming the write.

Columns:

    Name        Food name from the Claude response.
    FDC ID      USDA FDC ID if one was provided.
    Calories    Calorie value from the response (per 100 g).
    Protein     Protein value (g per 100 g).
    AA count    How many of the 11 tracked amino acids were found
                (e.g. 9/11 means 9 out of 11 were present).

Review each row for plausibility. If a value looks wrong, don't click "Confirm and import" — go back to the Import Claude response page, edit the pasted text in the textarea (or paste in a corrected reply from Claude), and click **Review** again.

After confirming, each food is written to your cache. Foods that gain amino acid data change from — to ✓ in the [AA](#gloss-aa) column of the [Food Cache](#gloss-food-cache). Any notes Claude added are saved as curator notes — view them by clicking that food's "Notes ▸" link in the [Food Cache](#gloss-food-cache) list.

For the full import workflow, see [Food Cache](#food-cache-web).


#### Drafted Food Profiles List {: #drafted-foods}
Shows the custom food profiles you have created by hand -- products from a label, research table entries, or supplements not in [USDA](#gloss-usda) or Open Food Facts[^3].

Columns:

    #       Row number. Use to select a profile for viewing or editing.
    Name    Food name as you entered it.
    Note    Your optional source or description note.

Drafted foods are stored in your [Food Cache](#gloss-food-cache) and appear in all food searches alongside [USDA](#gloss-usda) and Open Food Facts[^3] entries. In ID columns throughout the program, drafted foods are shown as "usr".

To edit nutrient data: Foods -> [Food Cache](#gloss-food-cache), find the food, and use e#. Editing is done in the [Food Cache](#gloss-food-cache), not in this list.

To create a new custom profile: Foods -> Drafted Food Profiles -> Create. See [Food Cache](#food-cache-web) for an alternative way to get missing data (e.g. amino acid data from Claude AI for foods not in [USDA](#gloss-usda)).

**Estimating amino acids by copying from another food.** Whenever you're prompted for a food's amino acid profile (creating a drafted profile, copying a cached food, or editing any food's data), a third option lets you search for and pick a similar food that already has amino acid data, instead of typing values in or pasting from literature. The picked food's amino acids are **scaled to match this food's own protein content** (not copied raw) — a food with less protein than the source gets proportionally less amino acid content, and vice versa — the same scaling already used by hand in this app's built-in curated foods (e.g. amino acids scaled between fresh and dried okara). A note documenting the source food and scale factor is suggested automatically for the Note field. On the web app, the same picker appears as an "Estimate amino acids from another food" panel on the custom-profile edit page ([Custom Food Profiles](#custom-foods)); editing any food's data this way marks it user-drafted, same as any other edit.

On the web app, [Food Search](#food-search) has a shortcut into this workflow: any search result missing confirmed amino acid data shows a **Copy as draft to add AA data** link right in its row. Clicking it duplicates that food as an editable draft and takes you straight to its edit page, AA-source search box ready — skipping the separate trip through Custom Food Profiles' own "Copy a cached food as a draft" search.


#### My Pantry Table {: #pantry}
Shows the protein sources you have flagged as currently on hand. The Pantry drives the complement advisor -- when NuMa suggests foods to fill an amino acid gap, it checks your pantry first and shows matching foods in a "From your pantry" tier.

Columns:

    ID      USDA FDC ID, OFF, or usr -- for name-only entries.
    AA      Amino acid data status.
              checkmark  AA data in your cache. This food can be used in
                         complement suggestions.
              X          No AA data. Click Edit to add it.
              --         Name-only entry: no USDA link, no nutrient data.
                         Use Link a food to attach real data.
    Food    Food name.
    Notes   Your optional note for this pantry entry.
    Type, GI est., DIAAS   Same as the matching columns in the
            [Food Cache](#cached) list — see the DIAAS entry there for
            how the saved-estimate-vs-reference-table value is chosen.
    ARCH    Shown only when archived entries are visible (the show-archived
            toggle) — a dot marks an entry as archived. See [archiving](#archive).

Only pantry foods with [AA](#gloss-aa) data (checkmark) appear in complement suggestions. Name-only entries (--) and those without [AA](#gloss-aa) data (X) may still appear if their name matches a built-in complement table entry. Archived pantry entries never appear in complement suggestions.

Actions: **Add a food** (USDA search or name-only — the search results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns), **Remove**, **Archive/Restore** (see [archiving](#archive)), and an **Edit** button on each row that jumps straight to that food's Food Cache entry for editing. A name-only entry (no USDA link) shows a **Link a food** button instead — search and pick a match to attach real nutrient data to that same pantry row, rather than adding a duplicate.

**Only a search-and-select adds a food to your [Food Cache](#gloss-food-cache).** Picking a real match from **Add a food** caches it, the same as any other food search in NuMa — see [how foods enter your Food Cache](#food-data) in Part 8. Typing a **name-only** entry does not: nothing is written to the cache until you use **Link a food** to attach a real match, which is why a name-only row shows "--" in the [AA](#gloss-aa) column above instead of a checkmark or X.

See [complement suggestions](#comp) for how complement suggestions use your pantry.


#### Protein Digestibility Overrides {: #dcp-overrides}
Shows your custom true [ileal digestibility](#gloss-ileal-digestibility) coefficients. These values override the defaults NuMa uses in meal-level [DIAAS](#gloss-diaas) calculations.

Columns:

    Food name       Name of the food this override applies to (matched
                    case-insensitively against meal ingredients).
    Digestibility   Your custom coefficient (0.00-1.00). The fraction of
                    protein absorbed by the small intestine.
    Notes           Your source note (e.g. "Smith 2020 Table 3").

When an override is active for a meal ingredient, the Digestibility column in the Meal Protein Digestibility table shows the value with a "↑ user" marker next to it, distinguishing it from estimated or literature defaults.

Use overrides when you have found a published measured value for a food you eat regularly and it differs meaningfully from NuMa's default. Values should come from primary literature ([ileal digestibility](#gloss-ileal-digestibility) studies), not from product labels or general nutrition sources.

Set in **Settings → 6. Protein Digestibility Overrides**: enter a food name (matched exactly), a coefficient (0.00-1.00), and an optional source note, then Save. Entering the same food name again replaces its existing override. Each row in the table has a delete (✕) button.

See [meal protein digestibility](#meal-diaas) to see where this value appears in the analysis output. See [DIAAS](#diaas) for background on true [ileal digestibility](#gloss-ileal-digestibility).

---

## Part 6 — Shared Operations
Several operations show up in more than one place in the app — the same mechanism behind a search box on three different pages, say. This Part collects those, so they're documented once instead of several times, with a link back here from every place they apply.

### A. Setting up your computed daily nutrient targets {: #daily-nutrient-targets}
This is a table of your personalized nutrient targets, computed from your profile: calories, protein, carbohydrates, fiber, every tracked mineral, and every tracked vitamin — each labeled with its goal type (minimum, target, or upper limit). See [daily nutrient goals](#goals) for the formulas behind these numbers, and [RDA](#rda) for where the underlying reference values come from.

This appears as its own read-only Settings panel and updates automatically whenever **Your Profile**, just above it, changes. It requires an active profile — if the table looks empty or the numbers seem off, check that your profile (age, sex, weight, height, activity level) is filled in first.

**Archiving vs. deleting** is documented once, in Part 5's [Archiving](#archive) reference, so it isn't repeated here.

**Every percentage shown elsewhere carries its goal type too, not just this table.** A percent-of-target is meaningless on its own — 120% is good news for a minimum (protein: you've cleared the bar) and bad news for a limit (sodium: you're over the cap). Wherever a nutrient's percentage appears — on a food, meal, recipe, daily summary, or trend page — it's followed by a small `min`, `max`, or `target` tag (hover it for the full explanation), so you never have to come back to this table to know which direction is good.

### B. Dietary Preferences (Settings → 3) {: #diet}
This setting controls which protein sources appear in complement suggestions and food search results throughout the program. Change it under **Settings → Dietary preferences**.

| Option | Setting | Includes |
|---|---|---|
| 1 | All animal foods | meat, fish, dairy, and eggs |
| 2 | Vegetarian | dairy and eggs only (no meat or fish) |
| 3 | Plant-based only | plant sources only |

The setting is saved between sessions and applies to both the interactive complement display and any exported reports.

**A quick-switch control sits right above every Protein Complement Suggestions list** — a dropdown pre-set to your current preference, plus a "Change settings" link straight to this section. Picking a different option in the dropdown saves it immediately and reloads the suggestions for the new preference, without leaving the page you're on — useful when you want to see, say, what a plant-only complement would look like without permanently changing your setting (just switch it back the same way afterward).

**Important — this setting also filters food search results, not just complement suggestions.** If your preference is set to "plant-based only" or "vegetarian", foods outside that category will not appear anywhere in NuMa — not in food searches, not in search results within recipes or meals, and not in any lookup by name or [FDC ID](#gloss-fdc-id). If you search for a food and get no results, check whether your dietary preference setting is silently excluding it. To look up any food regardless of category, temporarily switch to "All animal foods" under Settings, do your search, then switch back.

### C. Ordering food search results {: #search-ranking}
When you search for a food — whether from the Food Search page, the Meals & Log "Add Food or Recipe" panel, or a recipe's ingredient search — NuMa has to decide what order to show the matches in. That's a harder problem than it sounds, because "best match" usually means several different things at once: does the name contain your search words? All of them, or just some? And does it matter which words a near-miss is missing?

**The short version:** results are ranked first by how many of your search words appear in the name — an item matching every word you typed always outranks one matching only some of them, which always outranks one matching none. Your own Pantry/Food Cache/Recipe matches only sort ahead of USDA/Open Food Facts/Canadian Nutrient File results when they're tied on that match quality — a genuinely better external match is never buried beneath a weak or coincidental match from your own data. The results table still shows your local matches under their own "From your pantry, food cache, and recipes" heading, with a divider before the external results below, but that's a display grouping over a single relevance-ranked list, not a hard "local always first" rule — the two groups can interleave if a later block of external results actually matches better. (An earlier version of NuMa let pantry/cache items always outrank everything else in the "Pantry, Cache, then Other" sort mode regardless of match quality, so an unrelated pantry item with only a coincidental word match could show up ahead of the food you actually typed. That mode now only breaks ties this way among equally-good matches — see below.)

**Word order matters, too.** If you type more than one search word, NuMa treats the order you typed them in as a signal of what matters most to you. Suppose you search `milk dry instant` because there are two kinds of dry milk — instant and non-instant — and you specifically want the instant kind, but you've put "dry" before "instant" because that's the more important distinguishing word to you. If nothing in your data matches all three words, NuMa prefers a match on `milk` + `dry` over a match on `milk` + `instant`, precisely because you typed "dry" first. In effect, the words you type earlier act as your stated priorities — a partial match that preserves your earlier words beats one that preserves only a later one, even when both partial matches contain the same number of words.

This means you can deliberately front-load your most important search word when you know a food name might be ambiguous or your data might be incomplete — put the word you care most about disambiguating on first, and let NuMa's ranking favor it if a perfect match isn't available.

*(For technically skilled users: the exact algorithm — including how word order is encoded as a simple bitmask comparison — is documented in `README-numa-documentation.md`, under "Searching for a food.")*

**When several results tie on text relevance, USDA data quality breaks the tie before name length does.** A dozen near-identical branded listings (say, a dozen "INSTANT NONFAT DRY MILK" products) can match your search words exactly as well as the one or two Foundation/SR Legacy foods actually named that — and branded names are often shorter, which used to let them win the final tiebreak even though they're the ones least likely to carry real amino acid data. Ties are now broken by data quality first (Foundation/SR Legacy, then Survey/Experimental, then Branded/Open Food Facts) and only fall back to shorter-name-wins after that, so the reference food most likely to actually answer your question surfaces before its branded look-alikes.

**Your own data is always checked first.** Before NuMa ever reaches out to USDA or Open Food Facts, it checks your local Food Cache and Pantry — a match there appears instantly, with no network round-trip. USDA and Open Food Facts results are still fetched right behind it (not only when the local check comes up empty), so a food newer than your cache, or one you've never looked up before, still turns up — it just takes a moment longer to appear. Once those external results arrive, the whole list (local and external together) is re-ranked by match quality as described above, so a stronger external match can end up ahead of a weaker local one rather than being stuck below it. A 12- or 13-digit barcode (UPC-A or EAN-13) skips general search entirely and goes straight to a direct Open Food Facts lookup by that exact code.

**Search result depth.** Plain, unprocessed foods (the ones most likely to carry full amino acid data) can get buried under branded or prepared-dish matches for the same word — USDA's own relevance ranking can push something like "Potatoes, flesh and skin, raw" 15–20 results deep for a plain "potato" search, or return two dozen canned/branded products before a plain cooked bean shows up for "pinto beans." To counter this, NuMa runs a second search pass restricted to Foundation Foods and SR Legacy (USDA's most complete, least processed data), so those results aren't lost in the noise. How many results that second pass fetches is configurable (Settings → 5. USDA API Key → Search result depth) — the default of 25 is enough for the vast majority of searches; set it higher if you still don't see the food you expect, or to 0 to remove the cap entirely (every matching result USDA returns, in one page — a higher number means a slightly slower search).

### D. Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it {: #recipe-dcp-cascade}
A recipe can be used as an ingredient inside another recipe — a lentil sauce that shows up in three different dinners, say. Editing and saving that base recipe recalculates its own digestible complete protein ([DCP](#gloss-dcp)) automatically. If it's also used as a sub-recipe ingredient elsewhere, saving it recalculates DCP for every recipe that depends on it too — directly, or through another sub-recipe in between — so a foundational recipe's protein score is never left stale in anything built on top of it. You never need to manually recompute a dependent recipe just because you changed the recipe it's built from.

A bulk "recompute DCP for all recipes" option still exists on the Recipes list — worth running after a bulk import, or if you suspect stale numbers predating this cascading recalculation.

### E. Entering custom foods and dietary supplements {: #custom-foods}
#### Custom (drafted) food profiles

When a food isn't in USDA or Open Food Facts[^3] — or the entry you found is incomplete — create a custom profile from an existing food as a starting point, or from scratch, via Foods → Custom food profiles → Create.

Whichever interface you use, the same fields apply:

- **Name** — what to call this food in searches and meal logs.
- **Supplement mode** (see below) or a normal serving size and unit.
- **Basic macros** — calories, protein, total fat, carbohydrates, fiber, sugars, saturated fat, mono/poly fats, sodium. Always required.
- **Minerals, vitamins, amino acids, and [phytonutrients](#gloss-phytonutrients)** — all optional. For vitamins A, D, and E you can type the amount in IU (e.g. `400 IU`) and NuMa converts it automatically; amino acids can be entered one-by-one or pasted in as a block from a research table (g per 100 g protein — converted automatically).
- **Note** — document your source or any caveats about the data.

Once saved, the food appears in every search and can be used in meals and recipes exactly like any other food. Edit or delete it from the same place you created it, at any time.

#### Dietary supplements — tablets, capsules, softgels

Supplement labels give amounts per tablet, not per 100 g. NuMa handles this with **supplement mode**: create a custom food profile as above, set the serving size to **1** with a unit of `tablet`, `capsule`, `softgel`, or similar, then enter the nutrient amounts exactly as printed on the label. Logging "1 [unit]" in a meal then adds exactly those label amounts to your totals — no weighing involved, and no conversion math on your part.

**Tip:** try a barcode search first (the 12- or 13-digit number on the label, entered at any search prompt). Many supplement products are already in Open Food Facts[^3] with complete data, saving you the manual entry.

To convert an existing custom food to supplement mode, edit it and change the serving size to **1** with a unit of `tablet`, `capsule`, or similar, same as creating one from scratch.


### F. Deleting a recipe that's used elsewhere {: #delete-recipe-elsewhere}
If another recipe uses the one you're deleting as a sub-recipe (an ingredient that is itself a recipe), NuMa warns you before deleting. If you delete it anyway:

1. That ingredient line is not removed. It stays in place, but is now flagged "recipe (deleted)" wherever it appears — in ingredient lists, meal history, and Food Use in Meals. This is expected, not a bug: NuMa can't know whether you meant to also cascade-delete every recipe that depended on it, so it leaves the reference intact and visible instead.
2. If you later create a new recipe whose name shares at least one word with the deleted recipe's name (for example, re-creating "Beef Stew" as "Chicken Stew," or under the exact same name as before), NuMa offers to relink those broken references to your new recipe — the offer appears as a banner on the new recipe's edit page.
3. If more than one deleted recipe matches by name, you're offered each one separately, and only the ones you confirm get relinked. Declining leaves the old references flagged as before.
4. To see every currently-broken reference in your data, regardless of what you're about to create, use the "Broken recipe references" button on the Recipes list.

### G. Ignoring a complement suggestion {: #ignore-complement}
Every [complement suggestion](#comp) — a Tier 1 gap closer, a Tier 2 [DIAAS](#gloss-diaas)-boosting option, or a food inside a Tier 3 two-food combination — carries an "Ignore this suggestion in recalculation" checkbox. Check one or more, then click **Recalculate complements** (it activates as soon as anything is checked) to reload the page with those foods excluded from every tier — pantry, general, two-food combinations, and DIAAS boosters all rebuild around the remaining candidates. Use this when a suggested food genuinely isn't an option for you (out of stock, disliked, already ruled out for some other reason) and you'd rather see the next-best alternative than one you can't act on.

Ignoring more foods on a later recalculation adds to the list rather than replacing it. A collapsible "Ignoring N suggestions — manage" panel lists every currently-ignored food alphabetically, each with its own "Remove ignore" checkbox to restore just that one; a "Clear all" link removes the whole list at once.

The ignored list is not saved anywhere — it resets the moment you navigate away, or reload the page without it. Available on the Food detail, Meal, and Recipe pages.

---

## Part 7 — Essential resources
---

### A. Food data — where it comes from and how it is stored {: #food-data}
**Six large tables** are NuMa's primary sources of food information:

- **[USDA](#gloss-usda) FoodData Central** — the U.S. government's nutrition database, covering hundreds of thousands of whole foods, ingredients, and branded products. This is NuMa's primary source. ([FoodData Central FAQ](https://fdc.nal.usda.gov/faq/))
- **Open Food Facts** — a community-maintained database of packaged and processed food products, especially useful for branded items not found in the [USDA](#gloss-usda) table. ([Open Food Facts](https://world.openfoodfacts.org/discover))
- **Canadian Nutrient File** — Health Canada's reference database, particularly good on amino acid coverage. ([Canadian Nutrient File](https://food-nutrition.canada.ca/cnf-fce/?lang=eng))
- **UK CoFID** — ~2,900 UK foods from Public Health England/DHSC, bundled into NuMa directly rather than looked up live (it has no API of its own). No amino acid data. ([CoFID](https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid))
- **Australian AFCD** — ~1,600 Australian foods from FSANZ, also bundled directly. Has real amino acid data, unlike CoFID. ([AFCD](https://www.foodstandards.gov.au/science-data/monitoringnutrients/afcd))
- **French CIQUAL** — ~3,200 French/European foods from ANSES, also bundled directly. No amino acid data. ([CIQUAL](https://ciqual.anses.fr/))

**[USDA](#gloss-usda) API key.** NuMa accesses FoodData Central through [USDA](#gloss-usda)'s public API. Without a personal key it falls back to a shared demonstration key (DEMO_KEY) that has a tight rate limit — heavy use by any user can exhaust it and cause searches to fail temporarily. Getting your own key is free and takes about a minute:

1. Go to https://fdc.nal.usda.gov/api-key-signup and enter your name and email.
2. [USDA](#gloss-usda) emails you a key immediately.
3. Enter it in NuMa under **Settings → 5. USDA API Key**, and click **Save key**. The field shows your current key in plain text whenever one is already saved, so you can retrieve it there any time.

Your key is stored on your computer only. Once set, all food searches use your personal key with a much higher rate limit.

**Search result depth** (Settings → 5. USDA API Key) — see [Search result depth](#search-ranking) in Part 6 for what this controls and why.

Every food in these online tables has a unique ID number — think of it as a product code that identifies that one food and nothing else.

**Your [Food Cache](#gloss-food-cache)**{: #FoodCache} is a table stored on your own computer. When you search for a food, NuMa checks your [Food Cache](#gloss-food-cache) first and shows any matches in a fast **[Food cache](#gloss-food-cache)** table before going online. Any food you have looked up before will be there and can be selected instantly, without a network call. If the food is not yet in your cache, the program searches both online tables and shows you a combined list of matches. When you select a food from that list, NuMa saves a copy of its nutrient data in your [Food Cache](#gloss-food-cache) automatically. Over time, most of the foods you normally eat will be in your [Food Cache](#gloss-food-cache) for quick retrieval.

**Edit protection.** Any food you edit manually — through Foods → 6. [Food Cache](#gloss-food-cache) — is marked as user-modified. NuMa will never silently overwrite a user-modified food with a fresh copy from [USDA](#gloss-usda), even if you search for that food again later. Your edits, custom amino acid values, and notes are permanent unless you change or delete them yourself.

**Omega fatty acid tracking.** NuMa tracks four individual omega fatty acids — ALA (plant-based omega-3, found in flaxseed, walnuts, chia), EPA and DHA (marine omega-3, found in fish and seafood), and linoleic acid (the main omega-6, found in vegetable oils and nuts). These appear in the nutrient table whenever [USDA](#gloss-usda) data is available. Foods already in your cache that predate this feature are updated automatically the first time you access them — no action needed on your part.

Food enters your [Food Cache](#gloss-food-cache) in four ways:

1. **From [USDA](#gloss-usda)** — you search, find a match, and select it. It is instantly saved into your [Food Cache](#gloss-food-cache).
2. **From Open Food Facts[^3]** — same process; the food is saved the moment you pick it.
3. **By barcode** — in any food search box, type the 12-digit UPC-A or 13-digit EAN barcode printed on the product (spaces and hyphens are ignored). NuMa looks the product up on Open Food Facts by barcode and shows it as the one search result — typing the exact barcode is itself the confirmation, so there's no separate "use this?" step; click it like any other search result to add it. This is the fastest way to add packaged foods and dietary supplements — many have an Open Food Facts entry but no [USDA](#gloss-usda) record.
4. **By hand** — you create a custom food profile yourself, entering nutrient values from a product label or research source. These entries go straight into your [Food Cache](#gloss-food-cache) without coming from any online source.

In every case, NuMa saves the food's original ID number alongside its data. That ID is the key that allows everything else in the program to refer back to a specific food unambiguously.

**Adding to [My Pantry](#pantry) doesn't always mean caching.** Picking a real search result when you add a food to your pantry caches it exactly like ways 1–3 above — there's no separate pantry-specific mechanism. But Pantry's **Quick add by name only** option skips the cache entirely: it stores just a name, with no nutrient data, until you later use **Link a food** to attach a real match and cache it. See [My Pantry](#pantry) in Part 5 for the full picture, including how a name-only entry shows up in that table.

**[Food Annotations](#gloss-food-annotation)** are a second table on your computer. They hold extra information you choose to add about a specific food — information that does not exist in either online table:

- **Glycemic index ([GI](#gloss-gi))** — how quickly a food raises blood sugar (scale 0–100). Neither [USDA](#gloss-usda) nor Open Food Facts[^3] provides [GI](#gloss-gi) values, so if you have a figure from a research table or a product source, you can record it here.
- **[DIAAS](#gloss-diaas) estimate** — a protein quality score (scale 0–2.0). NuMa can calculate this automatically for whole foods that have complete amino acid data. For packaged foods where that data is absent, you can record a known [DIAAS](#gloss-diaas) figure here instead — see [Estimating DIAAS by hand for a packaged food](#diaas-estimate-table) for a quick-reference table by protein source.
- **A preparation note** — a short reminder such as "boiled 20 minutes" or "soaked overnight."

Each annotation is linked to one specific food in your [Food Cache](#gloss-food-cache) by that food's ID number. This means two things: you can only annotate a food that is already in your cache, and if you ever remove a food from your cache, its annotation is removed with it automatically.

**Your Recipes** are stored in their own table on your computer. Each recipe holds a list of ingredients, and each ingredient is linked to a specific entry in your [Food Cache](#gloss-food-cache) — by that food's ID. NuMa handles this link automatically: when you add an ingredient to a recipe, it searches your cache and the online tables exactly as it would for any other food search, and caches the result if it isn't stored yet.

A recipe can also include another recipe as one of its ingredients, allowing you to build complex dishes from simpler prepared components. When you log a meal, you can add a portion of a recipe — or a portion of a recipe-within-a-recipe — exactly as you would add a single food.

**[My Pantry](#gloss-my-pantry)** is a short personal list of protein sources you currently have on hand — tofu, lentils, Greek yogurt, and so on. It is a separate table used for one specific purpose: when NuMa suggests foods to fill a protein gap in your diet, it checks your pantry first and moves those foods to the top of the suggestion list. This way the program recommends things you can actually use right now, rather than foods you would need to go and buy.

**How these lists relate — and where to edit.**

Your [Food Cache](#gloss-food-cache), your Pantry, and your Custom Food Profiles (called "Drafted Food Profiles" in the program) are three different windows onto the same underlying data — not three separate stores.

Every food's nutrient data lives in exactly one place: the [Food Cache](#gloss-food-cache). The Drafted Food Profiles list is simply a filtered view of your [Food Cache](#gloss-food-cache) showing only the foods you created or edited by hand. The Pantry is a short list of names that each point back to an entry in the [Food Cache](#gloss-food-cache) (when a [USDA](#gloss-usda) link exists).

This means: if you edit a food's nutrients in the [Food Cache](#gloss-food-cache), that change is immediately reflected everywhere — in Drafted Food Profiles, in any recipe using that food, in pantry-based analyses, and in annotations. There is no syncing, no duplication, and no risk of one list getting out of step with another.

**To edit nutrient data for any food, always go to Foods → 6. [Food Cache](#gloss-food-cache).** The Pantry and Drafted Food Profiles menus remind you of this and offer a shortcut key to jump there directly. Annotations ([GI](#gloss-gi), [DIAAS](#gloss-diaas) estimates) work the same way: annotate a food once in the [Food Cache](#gloss-food-cache) and the annotation appears everywhere that food is used.

### B. Glossary {: #glossary}
Abbreviations and key terms used in NuMa output and this manual.

---

**AA**{: #gloss-aa}  —  Amino acid. The molecular building blocks of all proteins. See [essential amino acids](#aa).

**AI**  —  Adequate Intake. A nutrient reference value used when a full RDA cannot be established; considered sufficient for most healthy people. Used for fiber in NuMa. See [RDA](#rda).

**Antinutrient**{: #gloss-antinutrient}  —  A naturally occurring plant compound that partially blocks the absorption or use of a nutrient. Common examples: phytates (reduce mineral absorption), oxalates (reduce calcium absorption), lectins (interfere with digestion in raw legumes), bound niacin in corn. All can be reduced by appropriate preparation. See [antinutrients](#antinutrients).

**Bioavailable protein**{: #gloss-bioavailable-protein}  —  Protein the body can actually absorb and use, accounting for both digestibility and amino acid completeness. More meaningful than the raw protein figure on a nutrition label.

**CGM**{: #gloss-cgm}  —  Continuous Glucose Monitoring. A wearable device that measures blood glucose every few minutes. Discussed in [Appendix D](#appendix-d) as the most accurate way to track individual glycemic response.

**Complete protein**{: #gloss-complete-protein}  —  A protein source that supplies all nine essential amino acids at or above FAO reference levels after digestibility adjustment. See [protein completeness](#complete).

**Complement food**{: #gloss-complement-food}  —  A food added to a meal specifically to supply the amino acids that other ingredients are short in. See [complement suggestions](#comp).

**DCP**{: #gloss-dcp}  —  Digestible Complete Protein. Grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (all essential amino acids present at adequate levels). See [digestible complete protein](#dcp).

**DIAAS**{: #gloss-diaas}  —  Digestible Indispensable Amino Acid Score. A score from 0 to 1.5+ measuring how much of a food's protein the body can actually use, accounting for digestibility and amino acid completeness. 1.0 = meets the FAO reference exactly; above 1.0 = excellent; below 1.0 = one or more amino acids are limiting. See [DIAAS](#diaas).

**Digestibility coefficient**{: #gloss-digestibility-coefficient}  —  A number between 0 and 1 representing the fraction of a nutrient that reaches the bloodstream after digestion. NuMa uses true ileal digestibility values from published literature. Eggs and dairy sit near 1.0; whole legumes are typically 0.79–0.85.

**DRI**{: #gloss-dri}  —  Dietary Reference Intakes. The system of nutritional reference values published by the U.S. National Academies of Sciences[^9]; the source for RDAs, AIs, and upper intake levels used in NuMa.

**EAA**{: #gloss-eaa}  —  Essential Amino Acid. One of nine amino acids the human body cannot make and must get from food every day: Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine. See [essential amino acids](#aa).

**FAO**{: #gloss-fao}  —  Food and Agriculture Organization of the United Nations. The body that published the 2013 amino acid reference standard used for all protein quality scoring in NuMa. See [FAO reference values](#fao).

**FDC**{: #gloss-fdc}  —  FoodData Central. The USDA's online nutrition database and NuMa's primary food data source. Each food has a unique numeric FDC ID. Website: https://fdc.nal.usda.gov/

**FDC ID**{: #gloss-fdc-id}  —  The unique numeric identifier assigned to each food entry in USDA FoodData Central. You can enter an FDC ID directly at any "Search food or recipe" prompt instead of typing a name.

**Food Cache**{: #gloss-food-cache}  —  Your local database of previously retrieved foods. Searching the cache is instant (no network required); foods are added automatically when you select them from USDA or Open Food Facts[^3] results.

**Food Annotation**{: #gloss-food-annotation}  —  Extra information you attach to a cached food: glycemic index, a DIAAS estimate, or a preparation note. Stored locally; not part of any online database.

**GI**{: #gloss-gi}  —  Glycemic Index. A scale from 0 to 100 measuring how quickly a food raises blood glucose relative to pure glucose (100). See [glycemic index](#gi).

**GL**{: #gloss-gl}  —  Glycemic Load. A measure of glycemic impact that combines GI with the actual amount of carbohydrate in a serving. More useful than GI alone for real-world meal comparisons. See [glycemic load](#gl).

**GUI**{: #gloss-gui}  —  Graphical User Interface. A visual, point-and-click interface — this is what NuMa's web app provides (see Part 3, "Using the Web App").

**Ileal digestibility**{: #gloss-ileal-digestibility}  —  The fraction of an amino acid absorbed by the end of the small intestine (ileum). DIAAS uses true ileal digestibility, which is more accurate than fecal digestibility for measuring protein available to the body.

**Limiting amino acid**{: #gloss-limiting-amino-acid}  —  The essential amino acid in shortest supply relative to the FAO reference, which caps how much of a food's protein can be incorporated into tissue. The overall DIAAS score equals the ratio for the limiting amino acid. See [limiting amino acid](#gap).

**Met+Cys**{: #gloss-met-cys}  —  Methionine + Cystine. These two amino acids are scored as a combined pair in DIAAS calculations, following FAO 2013 guidelines, because the body can convert Methionine into Cystine.

**My Pantry**{: #gloss-my-pantry}  —  A personal list of protein sources you currently have on hand. NuMa checks this list first when suggesting complement foods, so suggestions reflect what you can actually use.

**NuMa**{: #gloss-numa}  —  NutriMagnus. The abbreviated name used throughout this manual.

**OFF**{: #gloss-off}  —  Open Food Facts. A community-maintained database of packaged and branded food products; NuMa's secondary data source. Website: https://world.openfoodfacts.org/

**Oxalate**{: #gloss-oxalate}  —  A naturally occurring compound (oxalic acid / oxalate ion) found in many plant foods, especially spinach, beets, nuts, and chocolate. At high dietary levels it can promote calcium-oxalate kidney stones in susceptible individuals. NuMa can optionally display oxalate content using the Harvard T.H. Chan School of Public Health reference table. Enable it under Settings → Oxalate data. See [oxalate data](#oxalate).

**Phe+Tyr**{: #gloss-phe-tyr}  —  Phenylalanine + Tyrosine. Scored as a combined pair in DIAAS calculations because the body can convert Phenylalanine into Tyrosine.

**Phytonutrients**{: #gloss-phytonutrients}  —  Plant-derived bioactive compounds tracked by NuMa where USDA data exists: beta-carotene, alpha-carotene, lycopene, lutein/zeaxanthin, choline, beta-sitosterol, and isoflavones.

**Pooled DIAAS**{: #gloss-pooled-diaas}  —  The meal-level protein quality score computed by summing digestible amino acids across all ingredients before scoring. This captures how foods complement each other in a way that single-food DIAAS cannot. See the section "How NuMa scores meal and recipe protein quality."

**RDA**{: #gloss-rda}  —  Recommended Dietary Allowance. The average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group. See [RDA](#rda).

**SPI**{: #gloss-spi}  —  Soy Protein Isolate. A concentrated plant protein (95%+ protein by weight) with high digestibility (0.95); frequently cited in complement suggestions. See [Appendix I](#comp-appendix).

**TID**{: #gloss-tid}  —  True Ileal Digestibility. NuMa's abbreviation for [ileal digestibility](#gloss-ileal-digestibility), used as a column heading in per-ingredient digestibility breakdowns.

**USDA**{: #gloss-usda}  —  United States Department of Agriculture. The U.S. government body that publishes FoodData Central, NuMa's primary food data source.

**usr**{: #gloss-usr}  —  User-drafted. Appears in ingredient ID columns to indicate a food whose nutrient profile you created or edited by hand, rather than one retrieved from USDA or Open Food Facts[^3].

### C. Internet resources

Examine.com. (n.d.). Examine—Independent analysis of nutrition and supplement research. Retrieved August 2, 2026, from https://examine.com

> Independent, citation-linked summaries of supplement and nutrient research—a good sanity check when a nutrient shows up as low or high in your analysis and you want to know what the science actually says about it. It offers nutrition data, recommendations, safety recommendations, and much, much more.

Food and Agriculture Organization of the United Nations. (2013). Dietary protein quality evaluation in human nutrition: Report of an FAO expert consultation. Retrieved August 2, 2026, from https://www.fao.org/3/i3124e/i3124e.pdf

> The original FAO report defining Digestible Indispensable Amino Acid Score (DIAAS) methodology; the primary source behind NuMa's protein-quality calculations.

Linus Pauling Institute. (n.d.). Micronutrient Information Center. Oregon State University. Retrieved August 2, 2026, from https://lpi.oregonstate.edu/mic

> Deep-dive, peer-reviewed summaries of individual vitamins, minerals, and phytonutrients—deficiency symptoms, toxicity thresholds, and disease-prevention evidence that goes well beyond what a nutrient table can show.

National Institutes of Health Office of Dietary Supplements. (n.d.). Office of Dietary Supplements—Nutrient Recommendations and Databases. Retrieved August 2, 2026, from https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

> This extraordinary resource is the fundamental data source for nutrition data used by NutriMagnus.

Open Food Facts. (n.d.). Open Food Facts—World food products database. Retrieved August 2, 2026, from https://world.openfoodfacts.org

> The crowd-sourced packaged-food database NuMa already queries for barcode lookups; browsing it directly lets you see ingredient lists, Nutri-Score, and photos that NuMa doesn't surface.

University of Sydney. (n.d.). Glycemic Index Database. Retrieved August 2, 2026, from https://glycemicindex.com

> The original research database behind glycemic index and glycemic load values; useful for looking up GI numbers for foods not yet annotated in NuMa.

### D. Using this manual's search {: #search-howto}
Use the sidebar search box near the top of the table of contents.

**It searches whole words, not phrases, and requires all of them.** Type `portion size` and NuMa looks for sections that contain *both* words somewhere — not necessarily next to each other, not in the order you typed them. This is different from typing a whole phrase and expecting an exact match: `edit portion` (as a phrase) will find nothing, because that exact wording never appears anywhere in the manual, even though the idea is covered extensively. If a search comes up empty, the fix is usually to drop a word, not add one — start with just the noun you care about (`portion`), see what comes back, then add a second word only if the list is too long to skim.

**Results are sections, not raw text.** Instead of jumping straight to every individual occurrence of your words scattered across the whole manual, search shows you a short list of section headings that contain all of them — click one (or press **Enter** to jump straight to the top match) to open it, and NuMa highlights every matching word within that section so you can see at a glance where they landed. **Enter**/**Shift+Enter** (or the &#x25B2;/&#x25BC; buttons) then step between highlighted words inside that one section, not across the whole document.

**The "Only show things you can do" checkbox** narrows the results further, to sections that contain some instruction — add, edit, change, remove, and similar words — rather than sections that merely *discuss* a topic. Turn it on when you're trying to do something rather than understand something: `portion size` with the box checked skips past conceptual explanations of what a portion is and goes straight to the section that tells you how to add or correct one. It's a heuristic, not a guarantee — a section phrased with an instruction word this checkbox doesn't happen to recognize can still be missed, and unchecking the box always shows you the same results or more, never fewer, so it's worth trying both if the checked list comes up empty.

## Part 8 — Troubleshooting and feedback — reporting problems and offering ideas {: #feedback}
If something seems broken or confusing, there's a good chance the answer is already below. The topics are grouped by how the problem *feels* rather than which menu it's in, since that's usually how you'll remember it later — and a few topics are listed in more than one group, since the same problem can feel different ways depending on what you were expecting. There aren't so many that you can't just skim the headings if nothing matches at first.

### A. Operating the program

#### The program crashes unexpectedly {: #ts-crash}
If NuMa crashes or freezes, nothing you'd already saved is lost — every action (adding a food, saving a recipe, logging a meal) is written to your data immediately, not held until some later "save" step. It's safe to just restart the program and pick up where you left off.

If a page seems frozen or won't load, try refreshing it first. If that doesn't help, the program running in the background may need restarting — close and relaunch it the way you normally start NuMa.

Either way, [let us know](#feedback) — see "How to contact help" below. This is beta software; a crash almost always means we found a real bug worth fixing, not something you did wrong.

#### You know what you want to do but can't see how to do it {: #ts-findit}
Click any **Learn more** link near a section heading or analysis output — see [Getting help](#help) for the full list of what each one covers.
- Either version: this manual's own search — if you're reading it in the web app, use the sidebar search box (see [Using this manual's search](#search-howto) for how to get good results from it, especially the "Only show things you can do" checkbox); if you're skimming the plain text version, search for a word describing what you're trying to do rather than a menu name.

If you still can't find it, [tell us what you were trying to do](#feedback) in plain language, not what menu item you were looking for. That phrasing is exactly what we need to know whether the feature exists, is named confusingly, or genuinely isn't built yet.

### B. I don't understand...

#### A recipe's "Complete" checkbox doesn't match its protein-completeness score {: #ts-complete-confusion}
A recipe's **Complete** checkbox and its amino-acid completeness score are two unrelated ideas that happen to share the word "complete." **Complete** (the checkbox, see the [Recipes list](#recipes) column guide) is a personal flag you toggle yourself — "I'm done editing this recipe" — it has nothing to do with protein quality. Whether a food or recipe's amino acid profile is **complete** (clears every essential amino acid floor) is a separate calculation shown in its DCP and DIAAS analysis. A recipe can be marked Complete and still have an incomplete amino acid profile, or the reverse.

#### I set a recipe's servings to 0 and now everything looks different {: #ts-servings-zero}
Setting a recipe's **Servings** field to 0 is a deliberate mode switch, not an error: it tells NuMa you want to analyze the recipe by total weight or volume instead of by serving count — useful for something you haven't decided how to portion yet (a big batch of granola, say). Every "per serving" figure becomes "per 100 g" or "per 100 ml" instead, and DCP shows as **NC** (not computed) since there's no serving size to divide by. Set Servings back to any number greater than 0 to return to normal per-serving analysis.

*See also:* [DCP is capped or jumped in a way that doesn't add up](#ts-dcp-cap), [A food or recipe shows an "insufficient amino acid data" warning](#ts-missing-aa), [Oxalate or glycemic index data isn't showing](#ts-oxalate-gi).

### C. I'm confused — something unexpected happened

#### USDA searches got slow, or started failing {: #ts-usda-slow}
Without a personal [USDA API key](#food-data), NuMa shares a demonstration key (`DEMO_KEY`) with every other NuMa user, and its rate limit is tight enough that heavy use by anyone can exhaust it, causing searches to fail temporarily for everyone. A free personal key removes this ceiling and takes about a minute to get — see [Food data — where it comes from and how it is stored](#food-data) for the sign-up steps and where to enter it (Settings, either version).

#### A deleted recipe shows up as "(deleted)" somewhere {: #ts-deleted-recipe}
This is expected, not a bug: deleting a recipe that's used as an ingredient in another recipe doesn't remove that ingredient line — it stays in place, flagged "recipe (deleted)" wherever it appears (ingredient lists, meal history, Food Use in Meals). If you later create a new recipe with a similar or identical name, NuMa offers to relink the old references to it automatically. See [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) for the full behavior and how to browse every currently-broken reference.

*See also:* [I searched for a food I know exists and got nothing](#ts-search-empty), [The food I wanted wasn't at the top of the search results](#ts-search-order), [A meal's DCP isn't showing](#ts-meal-dcp), [A past day's numbers changed after I updated my profile](#ts-day-profile).

### D. I expected to see something, and it's not there

#### A food or recipe shows an "insufficient amino acid data" warning {: #ts-missing-aa}
Some foods — especially branded or prepared products — simply don't have amino acid data published anywhere NuMa can look it up automatically. This isn't a bug; it's a genuine data gap. Two ways to close it: search for a USDA Foundation or SR Legacy equivalent (plain/raw foods are far more likely to have full amino acid data than branded ones), or fetch the missing values yourself via Claude AI — see [Missing amino acid profiles](#missing-aa) and [Food Cache](#food-cache-web).

*See also:* [No brand or equivalent of a food has amino acid data anywhere in USDA](#ts-no-aa-anywhere), for the harder case where neither fix above applies.

#### No brand or equivalent of a food has amino acid data anywhere in USDA {: #ts-no-aa-anywhere}
This is a step beyond [an "insufficient amino acid data" warning](#ts-missing-aa): you've checked, and no brand, no store variant, and no generic USDA entry for this food carries amino acid data — the whole category is a gap, not just the specific product. "Search for a Foundation/SR Legacy equivalent" doesn't help here because there's no equivalent food with the data you need.

The fix is to stop looking for an equivalent *food* and look instead for an equivalent *ingredient* — something with measured amino acid data whose composition dominates the protein in the food you're trying to estimate. Flour-based baked goods, for instance, get essentially all their protein from the flour; a legume-based product gets essentially all of its protein from that legume. [Estimating amino acids by copying from another food](#drafted-foods) is the tool that turns an ingredient like this into an estimate for your actual food — it scales the ingredient's amino acid values to match your food's own measured protein content automatically, rather than you doing that arithmetic by hand.

If more than one ingredient contributes meaningfully to the protein (a flour blend, for example), blend their profiles first, by mass fraction, before treating the result as a single stand-in. The copy-from-another-food picker copies from one source food at a time, so build the blend as its own drafted food first — call it a **proxy food**: a temporary, scratch entry that exists only to hold the numbers you'll scale from, not something you'd search for or log a meal against. (If only one ingredient dominates, it's still worth entering as its own proxy food rather than typing numbers straight into the real food — see why below.)

Once you have a proxy food — blended or not — holding the numbers you need, there are two different ways to turn it into a usable estimate for your actual food. Pick whichever fits how you'll use that food going forward:

**Option 1 — create a new, clearly-labeled draft (the general-purpose default).** Foods → Custom Food Profiles → **Copy a cached food as a draft**, pick the real food you're missing AA data for (it copies that food's full nutrient snapshot — protein included — into a brand-new, independent entry), rename the copy something unambiguous like "Graham Cracker, generic (estimated AA)," then run the AA-copying picker on *that* draft, scaling from your proxy food. Web app: [Food Search](#food-search)'s **Copy as draft to add AA data** link does the "copy as draft" half of this step in one click, right from the search results row. Because the original cached food is never touched, USDA can still refresh its full nutrient profile and portions automatically if that entry ever changes. The tradeoff: this new draft doesn't retroactively reach meals or recipes that already reference the *original* food — those keep pointing at the un-estimated entry until you go swap the reference over by hand.

**Option 2 — edit the original food's AA fields directly (a deliberate exception).** If you know you'll always be logging this exact product, editing its AA data in place is often more practical: every past and future meal or recipe that already references it picks up the estimate immediately, with nothing to swap. The cost is real, though — editing *any* of a food's data marks the entire record user-modified, not just the amino acid fields, so NuMa will never again silently refresh its full nutrient profile, portions, or anything else on it from USDA; you're taking permanent manual ownership of that specific record. That's an easy trade when the food is unlikely to gain real measured data any other way — a specific branded product like Nabisco Honey Maid Grahams already has its macronutrients measured and isn't about to grow USDA amino acid data on its own, so there's little future refresh being given up.

**Worked example: graham crackers, no AA data on any brand, made from a 2:1 white-to-whole-wheat flour blend. Nabisco Honey Maid Grahams specifically are already logged in past meals.**

Steps 1–3 build the proxy food and are the same regardless of which option you pick. Steps 4 onward differ — jump to whichever option fits your situation.

Step 1 — pull measured amino acid data for both flours (USDA Foundation/SR Legacy entries):

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

Step 2 — blend (average) the two flours 2:1 by mass (2 parts white, 1 part whole wheat) to get the amino acid pattern of the flour actually used, per 100g of blend:

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

Step 3 — enter this blend as its own proxy food (Foods → Drafted Food Profiles → Create; web: Custom Food Profiles), named something like "Wheat flour blend, 2:1 white:whole wheat (proxy)," with the protein and amino acid values from Step 2 typed in directly.

**Continuing with option 1 (new labeled draft).** Use this branch if you haven't already logged the Nabisco Honey Maid Grahams entry anywhere, or you'd simply rather leave it untouched:

Step 4 — Foods → Custom Food Profiles → **Copy a cached food as a draft**, and pick the Nabisco Honey Maid Grahams entry. This copies its full nutrient snapshot — including its measured protein content, 6.8 g/100g — into a brand-new, independent entry. The original cached food is untouched.

Step 5 — rename the new draft something unambiguous, like "Graham Cracker, generic (estimated AA)."

Step 6 — on that new draft, use the "estimate amino acids from another food" picker and choose the proxy food from Step 3 as the source. NuMa scales the proxy's amino acid values to match the draft's own protein content automatically — factor 6.8 ÷ 11.27 ≈ 0.60 — giving:

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

Step 7 — document the derivation in the draft's Note field (the picker suggests one automatically). From now on, use this draft — not the original Nabisco entry — when logging graham crackers in meals or recipes.

**Continuing with option 2 (edit the original in place) — Nabisco Honey Maid Grahams is already logged in past meals, so this is the better fit here:**

Step 4 — on the real Nabisco Honey Maid Grahams cached entry, use the "estimate amino acids from another food" picker and choose the proxy food from Step 3 as the source. The Grahams have their own measured protein content (6.8 g/100g) even though they lack amino acid data, so NuMa scales the proxy's amino acid values to match it automatically — factor 6.8 ÷ 11.27 ≈ 0.60 — giving the same result table as above.

Step 5 — document the derivation in the food's Note field (the picker suggests one automatically). Every meal and recipe already referencing this entry — past and future — picks up the estimate immediately; there's nothing else to update.

**Either way:** these amino acid figures are an approximation, not a certified lab value — they assume the crackers' protein comes entirely from the flour blend (true enough for a plain graham cracker; less true for a chocolate-coated one, where dairy protein in the coating would shift the pattern).

Once you've applied the estimate to every food that needed it, the proxy food from Step 3 has done its job — it exists only to hold numbers for the picker to scale from, not to be searched for or logged against. Delete it to keep it out of future search results, unless you expect to reuse it again soon (for another graham-cracker product, say) — in which case there's no harm leaving it in place until you're done with it.

#### I searched for a food I know exists and got nothing {: #ts-search-empty}
Try different search terms. "beans cooked" and "beans canned" may seem to be the same thing but they are not. The latter is a subgroup of the former. Playing with search terms can yield seriously variable results.

Check your **Dietary Preference** setting (Settings). If it's set to "Plant-based only" or "Vegetarian," foods outside that category are filtered out of *every* search, comparison, and lookup in NuMa — not just from complement suggestions — so a food you know is in USDA's database can still return zero results. Temporarily switch to "All animal foods," search, then switch back.

#### The food I wanted wasn't at the top of the search results {: #ts-search-order}
This is usually not a bug — it's the order you typed your search words in. NuMa ranks results first by how many of your search words a name contains, but when there's a tie, it treats the *order* you typed your words in as a signal of priority: matching your earlier words outranks matching your later ones. So searching `milk dry instant` will favor a "milk dry ..." match over a "milk instant ..." match whenever only one of those two words is present in a given result, simply because "dry" was typed before "instant."

If that's not the priority you meant, reorder your search words so the one you care most about comes first — put the word that most distinguishes what you want right after the main food name. See [Ordering food search results](#search-ranking) in Part 6 for the full explanation of how results are ranked.

#### A meal's DCP isn't showing {: #ts-meal-dcp}
DCP now computes and saves automatically every time you add, edit, or remove an item — there's no "mark complete" step required for it to appear, and an in-progress meal already contributes to that day's total. (Marking a meal **Complete** still matters for a different reason: a day containing an unmarked meal is flagged "provisional" in Daily Summary, since its total could still change.)

If DCP is still showing as missing, the real cause is the same as [an "insufficient amino acid data" warning](#ts-missing-aa): none of the meal's food items — and for recipe items, the recipe itself — have amino acid data available yet. Add AA data to at least one ingredient (or analyze the recipe), and DCP fills in immediately without needing to reopen or reanalyze the meal.

#### Oxalate or glycemic index data isn't showing for a food {: #ts-oxalate-gi}
Both are opt-in and off by default — this is a configuration gap, not a bug. [Oxalate data](#oxalate) needs its Settings toggle switched on (one account-wide switch, either version). [Glycemic index](#gi) needs either the built-in reference-table seed or your own annotation on that specific food; NuMa will offer to prompt you for it the first time you add a new food to your Pantry or a meal.

*See also:* [A recipe's "Complete" checkbox doesn't match its protein-completeness score](#ts-complete-confusion).

### E. The numbers don't make sense

#### DCP is capped, or jumped in a way that doesn't add up {: #ts-dcp-cap}
This is the single most common "the math looks wrong" report, and it's almost always correct behavior: DIAAS itself is not capped (a high-quality food can score above 1.0), but Digestible Complete Protein (DCP) can never exceed the protein you actually absorbed, so NuMa caps it there when the two disagree. A capped DCP is genuinely good news — it means your limiting amino acid is in strong enough supply that none of your absorbed protein is going to waste. See [Why DCP Is Sometimes Capped Below the DIAAS Projection](#dcp-cap) for the full explanation with a worked example.

#### A past day's numbers changed after I updated my profile {: #ts-day-profile}
This shouldn't happen, and if it does, it's worth [reporting](#feedback) — but first check whether it's actually the documented, intentional behavior: each logged day stays pinned to whichever profile was active *when you logged it*, not whatever profile is active today, specifically so that switching profiles (illness, travel, a deliberate weight change) doesn't silently rescore your history. If the automatic pin doesn't match reality — illness or travel rarely starts exactly at midnight — you can manually reassign which profile a specific day is compared against. See [Per-day profile tracking](#day-profile) for how.

*See also:* [A deleted recipe shows up as "(deleted)" somewhere](#ts-deleted-recipe).

### F. A food's portion or serving-size data looks wrong

Most of what's below isn't NuMa misbehaving, it's a gap or error in the underlying USDA data NuMa displays. USDA publishes nutrient values reliably, but the *portion* records attached to a food — "1 large," "1 cup, sliced," and so on — are contributed unevenly and sometimes inaccurately. NuMa shows you exactly what USDA supplies; when that's missing or wrong, the fix is to teach NuMa the correct value yourself, once, and it's remembered for every future use of that food. (One entry below — the `pN` shortcut mix-up — is a NuMa naming rule rather than a USDA data gap; it's grouped here because it's still fundamentally a portion-editing question.)

#### A food has no "per piece" or "per egg" portion — only grams {: #ts-no-piece-portion}
Some foods that obviously come in natural units — a whole egg, a piece of fruit, a slice of bread — still have no USDA-supplied portion for that unit, only the generic per-100-g figures. This happens because USDA's portion records are contributed per food entry, not derived automatically from the food's description, so some entries simply never got one. It's not something NuMa can infer on its own — "1 egg" isn't a fixed weight (USDA's own size grades range from about 38 g for "Small" to 63 g for "Jumbo").

Two fixes: weigh the item once on a kitchen scale and enter that weight directly (`56g`, for instance), or teach NuMa the unit permanently via the food's [Food Cache](#food-cache-web) entry, **Portions** action. Either way, every later analysis, recipe, and meal entry for that food can then use the unit directly (`1 egg`, `2 slices`) instead of a gram weight.

#### A food has a weight portion but no cup/tablespoon equivalent {: #ts-no-volume-portion}
NuMa converts a volume measure (cup, tablespoon, teaspoon) to grams using a *density* estimate for that food — mass per milliliter. USDA doesn't publish density directly; NuMa derives it only where a matching weight-and-volume portion pair exists in the food's own USDA record, plus a small built-in table for common dried herbs and spices (see [Portion Input Formats](#portion-formats)). Outside those cases, entering a volume measure will prompt you to weigh the amount and enter the grams yourself — this is expected, not a bug, since guessing a density would silently produce wrong nutrient totals.

If you'll be entering this food by volume repeatedly, teach NuMa the conversion once: weigh a level cup (or tablespoon) of it, then use the same Portions editor as above — the [Food Cache](#food-cache-web) entry's **Portions** action. From then on, cup and tablespoon amounts for that food convert automatically.

#### A food's portion or volume conversion looks flatly wrong {: #ts-bad-portion-data}
Occasionally a USDA record's portion weight is simply implausible for what it describes — a "1 large" egg listed at a weight that doesn't match a scale, or a "1 cup" measure clearly sized for a different preparation than the one you have. This is a data-entry error on USDA's side, inherited as-is; NuMa doesn't second-guess or adjust USDA's published portion weights, since there'd be no reliable way to tell a genuine correction from a wrong override.

If a portion weight doesn't match what you measure: weigh your actual amount and enter the gram figure directly for that one use, and — if you'll use this food again — replace the bad portion with a corrected one via the same Portions editor (the [Food Cache](#food-cache-web) entry's **Portions** action). Custom portions you add there are yours — they aren't overwritten by a later **Refresh** of the food's nutrient data. If you're confident the USDA source itself is wrong (not just unusual), [let us know](#feedback) — it's worth tracking so other users hit it less often, even though NuMa can't correct USDA's database directly.

*See also:* [Enter food portions as weights, not volume measures, whenever possible](#portion-formats).

#### A food's portion "pN" shortcut points to the wrong portion {: #ts-portion-numbering}
This is not a USDA data problem, it's a NuMa naming rule that's easy to misread: `p1`, `p2`, … always mean "the food's 1st stored portion, 2nd stored portion, …" in list order — never a portion's own description text. If you add a custom portion and type its own name in the **Description** field — say, you literally type `p1` as the description — that text has no bearing on its shortcut number. A food copied or imported from USDA usually already has a few built-in portions ("oz", "1 cup sliced," and so on) occupying the early slots, so your new one lands further down the list — often `p3` or `p4` — while `p1` still refers to whatever was already first. Typing `p1` in that situation silently applies the *wrong* portion's gram weight, with no error, since `p1` is still a valid shortcut — just not the one you meant.

Two ways to avoid this:

1. **Check the portion list shown right where you type the amount** — Foods, Recipes, and Meals all display the food's full portion set with its real shortcut number next to each entry (e.g. `p1 oz (14.2 g) · p2 1.75" square (3.0 g) · p3 …`) immediately above or below the amount field. Match against that list, not against a portion's name.
2. **Re-check after any portion edit.** Adding, removing, or reordering a food's portions renumbers every `pN` from that point on — a `p1` amount you entered correctly last week can silently mean something else today if you've since added or removed an earlier portion. If a `pN` amount doesn't come out the way you expect, re-open that food's [Manage Portions](#food-cache-web) page and count down the list before assuming something's broken.

*See also:* [USDA standard portions and the `pN` shortcut](#portion-formats).

### G. Getting more help{:#quickhelp}

This is extremely easy, and we want you to do it. When you're having a problem the cause is NOT necessarily you! Regardless of the nature of your problem, contacting us gives us essential information needed to make things better for you and also for every other user. We very much want to hear from you if you have a problem.

1. Text Tom at 435-272-3332. Plainly state that you are having a problem with the program. A brief statement of the problem is all I need. With your phone number I can call you back and get complete details of what I need to know to resolve your problem. I will generally call you back immediately. If you prefer a different time, let me know.

2. For non-urgent problems - which generally are improvements you'd like to see - you can also email me. Provide screenshots, if you think that would help. ALWAYS TEXT ME IF YOU SEND AN EMAIL, as I do not check my email daily, and yours easily can get lost in the 100s I get every day.

---

## Part 9 — Possible Additional Features
Ideas below are listed in their current likely probability of being implemented.

---

### ☑ CSV export and import for foods and recipes (completed 2026-08-11)

Foods and recipes can now both be exported to CSV and imported back in — on this or another NuMa install — via **Export CSV**/**Import CSV** buttons on the [Food Cache](#food-cache-web) list and on each [recipe](#recipes)'s page. A recipe's export is self-contained: it bundles every sub-recipe and food ingredient's full data along with it, so nothing has to already exist on the receiving end for the import to work, and anything that already matches by name is reused rather than duplicated. See the August 11 entries in [Recent program updates](#a-recent-program-updates-log) for full detail.

### Expanding Revised Optimal (Recent Research) targets {: #expand-revised-optimal}
☑ **Age/sex-banded RDA (completed, existing feature)** and ☑ **research-backed maximum nutrient levels (completed 2026-08-11)** are both done — see [Daily Nutrient Goals](#goals) for the full RDA age/sex band table and [Maximum Nutrient Limits](#maxlimits) for all 12 built-in Tolerable Upper Intake Levels, each sourced to the NIH DRI tables[^9].

☐ **What's still open:** the [Revised Optimal (Recent Research)](#optimal) tier — the *above-RDA* targets, as distinct from the RDA itself — only has built-in defaults for three nutrients today: vitamin D[^12] and EPA+DHA[^13]. Candidates for a future addition, each needing its own specific citation the way those two already have (not a bulk table import like the RDA/UL work, since there's no single unified source for "beyond-RDA" targets — see the tradeoff discussed when this feature was scoped):

- **Magnesium** — some research suggests intakes above the RDA support better sleep and muscle function in older adults, though evidence is mixed enough that a single number is harder to defend than vitamin D's.
- **Vitamin K2** (as distinct from K1, which the RDA already covers) — emerging research on cardiovascular and bone benefits, not yet reflected in an official DRI.
- **Choline** — a meaningful fraction of adults fall short of even the AI-level intake; whether a "revised optimal" above the AI is warranted (versus just meeting the existing RDA) needs its own look.

Each addition means the same three-part exercise done for vitamin D and EPA/DHA: find the specific research consensus (or best available expert-body statement), a real number, and a citation good enough to stand next to the DRI-sourced RDA/UL figures without embarrassment.

### Suggested optimum nutrition profiles by age group

A step beyond the per-nutrient targets above: a small number of pre-built *bundles* of Revised Optimal settings, one per major life stage (e.g. "Adults 65+ bone health," "Endurance athlete") that a user could load all at once instead of setting each nutrient individually. Lower priority than the per-nutrient expansion above, since it depends on that work existing first for enough nutrients to make a bundle meaningfully different from just the RDA.

### Source citations for major assertions in the manual

This is basic. Claims must be backed up, and source citations are how it's done. Numa is designed around nutrition research findings. To move quickly, these findings have not been referenced in the manual. They will be as soon as possible, which is to say as soon as the program is reliably working for a number of serious users.

### Plots of individual nutrients consumed daily in relation to RDAs, user-established optimums, and maximum levels.

This is easily achieved once we have dealt with the fundamental data problem better - getting optimums and maximums specified for a user. 

### Development of glycemic data lookup tables

Such data is of interest to anyone wanting to better manage their blood sugar levels, including folks with any degree of metabolic syndrome, pre-diabetes, or outright diabetes. At present, no active use of such data exists in the program, but provision of such use is in place.

### What else? Well, know this...

#### Your ideas shape what gets built next {: #feature-ideas}

NuMa is an evolving tool, still actively being built out. This part exists to invite you into that process: if there's something NuMa doesn't do yet that would make it more useful to you, we want to hear about it.

No idea is too small, too ambitious, or too specific to your own situation. A feature that seems minor to you may turn out to matter to a lot of other users too — and one that seems highly personal often points to a real gap in the program. Several of NuMa's existing features started out as exactly this: one user's request.

#### How to contribute an idea

Use the same channel as [reporting a problem](#feedback):

1. **Text Tom at 435-272-3332** with a brief description of what you'd like NuMa to do, and why it would help you. He will generally call you back to get the full picture.
2. **Or email**, especially for a longer or more detailed idea — a screenshot or example is welcome if it helps explain what you have in mind. If you email, also send a text, since email isn't checked daily and a good idea shouldn't get lost in it.

There's no such thing as a request that's not worth mentioning. If you're not sure whether NuMa can already do what you want, ask anyway — the answer might be a feature you hadn't found yet, or it might be a real gap worth filling.


## Part 10 — Appendices
---

### A. Recent program updates log

[//]: # "Aside from being an update log for the user to access, this section is also used by create_release.py at git push time to produce a release note. It only looks for today's date heading (#### Month Day program updates). Once a release is cut, the matched text is copied into the GitHub release body permanently — nothing re-reads the manual afterward. So date whose release has already happened is safe to prune anytime; it can't retroactively change a past release's notes."
[//]: # "If there is no entry for the date of the push to main, create_release.py falls back to the generic "Automated build from main." message instead of real notes."

Each entry below has a bold title and a plain-language description — anywhere from one sentence to a short paragraph — of what you can now do or what changed. Many entries also carry a fenced code block underneath, labeled "Scope:", with the technical detail (menu path, files touched, root cause) for anyone who wants it; skip it if you just want the plain-language summary above it.

#### August 31 program updates

**CHOOSE HOW OFTEN YOU'RE TOLD ABOUT NEW VERSIONS, AND ALWAYS SEE YOUR CURRENT ONE**

Settings now has an "Update Notifications" section where you can set how often the "new version available" banner shows up on the home page: daily (the default), weekly, or monthly. The banner's build note also names that setting directly, with a link to change it. Separately, the home page now always shows a line under the Welcome heading — "Current version date: yyyy-mm-dd:hhmm" — so you can check exactly what you're running, down to the minute, without scrolling to the page footer; whenever a build note is set it follows in parentheses as "(Version note: ...)" on that same line. The build note no longer gets its own standalone box further up the page. See [What you see on the home page](#home-page-tour) for the full rundown, including exactly when the update check itself runs.

```
Scope: web/backend.py (_current_update_notify_frequency(), _should_show_update_notice()
gating index()'s update_available via a saved prefs.json frequency + last-shown-date pair;
new POST /settings/update-notify-frequency route; version_date passed as the full
VERSION stamp). web/templates/settings.html (new "Update Notifications" section).
web/templates/home.html (frequency note added next to NEW VERSION NOTE in the banner;
the old standalone "NEW VERSION NOTE" box removed; the always-visible "Current version
date" line below Welcome now carries the build note in parentheses). tests/test_web.py
(updated accordingly). user-manual.md (new "What you see on the home page" tour, Part 3
Section A). README-numa-documentation.md (matching, fuller technical writeup).
```

**BUILD-NOTE LINE NOW LABELED "NEW VERSION NOTE:", AND ITS BROKEN RENAME FIXED**

The plain-language note about your current build now reads "NEW VERSION NOTE: ..." instead of repeating the version number a second time on that line (the number's already in the line above it, or the page-bottom small print). Separately, `version.py`'s note constant was renamed to `NEW_VERSION_NOTE`; the web app's own import of the old name was fixed to match (it briefly wouldn't start otherwise), and one of the two places that line is rendered had been missed in the wording update, leaving stale text visible in the UPDATE AVAILABLE banner specifically — that's fixed too.

```
Scope: version.py (VERSION_NOTE renamed to NEW_VERSION_NOTE), web/backend.py
(import and template-context key updated to match), web/templates/home.html
(both the update_available and standalone renderings of the note now read
"NEW VERSION NOTE: ..."). tests/test_web.py (updated to the new name and
an assertion added that was missing on the merged-into-banner case).
```

**FIX: "UPDATE AVAILABLE" BANNER STILL SHOWED RIGHT AFTER A SUCCESSFUL UPDATE**

After clicking Update Now, the just-updated confirmation and the "there's an update available" banner could both show at once — confusing, since one says you're done and the other says you're not. The running process doesn't reload its own version number until it's relaunched, so the availability check still (accurately, but unhelpfully) saw the old version and flagged the release you just installed as available. That check is now skipped for the one page load right after a successful update.

```
Scope: web/backend.py (index() skips the update_check call when the
updated query param is set). tests/test_web.py (1 new assertion).
```

**FIX: "UPDATE NOW" SUCCESS MESSAGE TOLD YOU TO QUIT AN APP WITH NO VISIBLE WINDOW TO QUIT**

After a successful in-place update, the message used to say "Quit and reopen NutriMagnus" — but the packaged install has no visible window or taskbar entry to quit from, only the browser tab. It now says "Close this browser tab, then relaunch NutriMagnus," which is both accurate (the background server process only picks up the new binary on relaunch, not just from closing the tab) and matches what a user actually sees on screen.

```
Scope: web/templates/home.html (UPDATED banner wording), user-manual.md
(matching wording in the Update Now description). tests/test_web.py (1
new assertion).
```

**FIX: THE CURRENT-BUILD VERSION NOTE WAS BURIED IN FINE PRINT AT THE PAGE BOTTOM**

The plain-language note describing what changed in your current build (`version.py`'s `VERSION_NOTE`) used to appear only in small grey text at the very bottom of the home page — easy to miss entirely. It now shows near the top of the page: when there's an update available, it appears as a second line inside that same UPDATE AVAILABLE box, right below the first line; otherwise it gets its own light box in that same spot. The bare version number stays in the small print at the page bottom either way, for reference.

```
Scope: web/templates/home.html (version_note now renders as a line inside
the update_available alert box when one is shown — not a separate box
below it — falling back to its own alert-secondary box only when there's
no update available, so it's never shown twice; the bare version number
stays in the page-bottom small print, unchanged). tests/test_web.py (2
new tests covering both placements and no duplication).
```

**NEW: ONE-CLICK "UPDATE NOW" BUTTON ON THE UPDATE-AVAILABLE BANNER**

If you're running the packaged Linux install, the home page's UPDATE AVAILABLE banner now has an **Update Now** button — no terminal, no manual download. It fetches the latest release and replaces the running program in place; your data lives elsewhere and is never touched. A message tells you when it's safe to quit and reopen NuMa to start using the new version — the copy you're currently running keeps working until you do. Running from source instead of the packaged install shows the plain "what's new on GitHub" link as before, since there's no packaged binary for the button to replace.

```
Scope: numa_app/services/self_update.py (new — perform_update() downloads
the latest release's binary/icon from GitHub and os.replace()s the running
PyInstaller-onefile binary in place, atomic on the same filesystem;
is_available() gates this to a packaged Linux install, checking
sys.frozen and sys.platform), web/backend.py (new POST /update-now route,
index() now reads back updated/update_error query params for the
success/failure flash), web/templates/home.html (Update Now button +
confirm() dialog, success/failure banners). tests/test_self_update.py (7
new tests), tests/test_web.py (2 new tests).
```

**NEW: HOME PAGE NOW CHECKS FOR A NEWER RELEASE, AND SHOWS A SHORT NOTE ABOUT WHAT CHANGED IN YOUR CURRENT VERSION**

The home page now checks GitHub for a newer NuMa release each time it loads (cached for a few hours so it isn't re-checked on every visit) and shows an **UPDATE AVAILABLE** banner with a link to what's new when one exists. The version line at the bottom of the home page also now carries a short plain-language note about what changed in that build (e.g. "minor problem fixes"), instead of just the bare timestamp. The check fails silently if you're offline or GitHub is unreachable — it never delays or blocks the home page from loading.

```
Scope: version.py (new VERSION_NOTE constant, hand-updated alongside
VERSION and the Appendix A entry it summarizes), numa_app/services/
update_check.py (new — check_for_update() against GitHub's latest-release
API, string-compares the "vYYYY-MM-DD-HHMM" tag format scripts/create_
release.py already uses, in-process cached for 6 hours, never raises),
web/backend.py (index() route calls it via run_in_threadpool so a slow/
offline check can't block the event loop), web/templates/home.html (new
banner + version-note display). tests/test_update_check.py (7 new tests),
tests/test_web.py (1 new test), tests/conftest.py (no_update_check autouse
fixture stubs the network call for every other test, same pattern as
no_off/no_cnf).
```

**MANUAL: "USING THE WEB APP" MOVED RIGHT AFTER THE INTRODUCTION, AND A STALE READING-TIME FIGURE FIXED**

Part 6 ("Using the Web App") now comes right after Part 2 (the introduction), as the new Part 3 — the practical how-to-operate-NuMa material now reads before the nutrition-concepts and reference parts, instead of after them. Parts 3–6 renumbered accordingly (old 3→4, 4→5, 5→6), and every cross-reference to a part number throughout the manual was updated to match. Separately, the manual's "Reading time" figure had been silently wrong for a while — undercounting by close to 20,000 words — because the script that computes it treated any three backtick characters anywhere in the text as a code-fence marker, so a single sentence in Part 3 that mentioned the triple-backtick JSON fence syntax by name was misread as the start of a code block, and everything up to the next real fence (thousands of words) got wrongly excluded from the count. Reading time is now the corrected ~4 hours 19 minutes, not the ~2 hours 56 minutes shown before.

```
Scope: user-manual.md (Parts 3-6 reordered/renumbered, all in-text "Part N"
cross-references updated via a mapping pass, one prose line reworded to
drop the raw backtick sequence that broke word counting), scripts/build_
manual.py (count_words()'s fenced-code-block regex now requires the ```
fence to be alone at the start of its own line, per CommonMark, instead of
matching any three backticks anywhere in the raw text).
```

#### August 30 program updates

**ANTI-NUTRIENT CATEGORY LIST NOW SORTED HIGH TO LOW, NO REPEATS**

On meal, recipe, and food pages, the "Categorical report only — no quantitative data available" oxalate list (foods with only a category, not an exact milligram figure) now sorts by severity, very high to negligible, and alphabetically by food name within each category, instead of appearing in whatever order the ingredients happened to be listed in. The same food appearing more than once in a meal or recipe (e.g. used in two sub-recipes) now shows up only once, since it's a category label, not a summed quantity.

```
Scope: web/backend.py's _oxalate_for_items(), used by the meal, recipe, and
food detail routes. Sorts the qualitative list against oxalate.py's existing
CATEGORY_ORDER tuple; deduplicates by fdc_id (falling back to a
case-insensitive name match for entries with no fdc_id) before sorting.
tests/test_web.py: 2 new regression tests.
```

**MAINTENANCE: CLI REFERENCES FULLY RETIRED, README ARCHITECTURE DOC BROUGHT CURRENT, DOZENS OF STALE MANUAL PASSAGES FIXED**

This week's sweep closed out the one-time CLI-mention cleanup (added 2026-08-25): every remaining reference to the retired terminal CLI — the glossary entry, a "view with c#" note, a file-based Claude-response-review workflow, and a CLI-style "options 1/2/3" description of editing a meal item — is gone, replaced with the actual web-app buttons and forms. `README-numa-documentation.md`'s Project Structure, route reference, and Test Suite sections (last checked "never") were brought fully current against the real codebase: the Recipes and Daily Summary pages were still documented as unimplemented stubs, dozens of routes and templates added since were missing, and the test count was stale — all now match. A full read-through of `user-manual.md` against actual app behavior turned up and fixed real drift: wrong Settings section numbers (Dietary Preferences was labeled section 4, actually 3; "Advanced settings" doesn't exist — the API key and search-depth settings live in section 5), a wrong Foods-menu item count (nine listed, ten exist), a wrong Meals & Log default page size (documented as 15, actually 9), a stale description of Search Meal History (claimed date filtering, sorting, and pagination it doesn't have), a wrong DIAAS annotation range (documented 0–1.5, actually 0–2.0), stale Food Cache and meal-Digestibility table column lists that no longer matched the real columns, an outdated "% of RDA" table description (the real column is "% of daily target," with color-coding built into that cell rather than a separate status column), an incomplete description of Sodium's daily limit (didn't mention the 12 other nutrients that get an automatic upper-limit-based cap), and a barcode-search description implying a confirm prompt that was removed when barcode search became direct-to-result. Item 6 (test coverage) found and closed one real gap: the August 27 fix stopping generic prep/state words (raw, cooked, etc.) from triggering a spurious food-search match had no regression test; two were added, both passing — no bug found in the fix itself. Changelog pruned back to the last two weeks. This is the first monthly deep check and first full manual audit — both headers now show 2026-08-30 as their last-run date.

```
Scope: CLAUDE.md, README-numa-documentation.md, user-manual.md (Parts 3,
5, 6, 7, and Appendix A), tests/test_db.py (2 new tests for
_OR_FALLBACK_STOPWORDS). No application code changed — this was a
documentation-accuracy sweep, not a behavior change.
```

#### August 27 program updates

**SUBSTITUTE PANEL NO LONGER LOOKS LIKE ITS USAGE TABLE IS A LIST OF REPLACEMENT CANDIDATES**

The Food Use in Meals / Food Use in Recipes substitute-a-food-or-recipe panel showed an unlabeled table of what's currently used in your selection, easy to mistake for a menu of foods you could pick as the replacement — including the very food you're trying to replace, sitting right there in the list. That table now says plainly it's a usage summary, not a replacement picker, marks the item you're replacing as "replacing this," and links straight to Food Search / Recipes (each opens in a new tab and shows IDs) for finding the replacement's ID. [learn more...](#fooduse-substitute)

```
Scope: web/templates/analysis_food_use.html and analysis_food_use_recipes.html
(panel intro text now explains the table's purpose and links to /food/search
and /recipes for ID lookup; each results row computes is_replace_target by
comparing sub_kind/sub_id against the row's kind/fdc_id/recipe_id and shows
a "replacing this" badge when it matches), user-manual.md (#fooduse-substitute
updated to match — no longer tells the reader to read the replacement's ID
off the results table).
```

**BLOCKED-DELETE MESSAGES NOW OFFER A ONE-CLICK BULK REPLACE, NOT JUST REMOVAL INSTRUCTIONS**

The delete-blocked message on Food Cache and Custom Food Profiles previously only explained how to remove the food from each blocking recipe/meal one at a time. It now also links each blocking recipe/meal group to the existing Food Use substitution tools, pre-selected to exactly those recipes/meals with this food already chosen as the one to replace — so swapping in a different food everywhere it's used, in one action, is one click away. [learn more...](#fooduse-substitute)

```
Scope: web/backend.py (food_cache_delete/food_custom_profiles_delete now
pass blocked_fdc_id through the redirect; analysis_food_use() and
analysis_food_use_recipes() gained optional sub_kind/sub_id query params
that pre-fill the substitute form's "Replace this" side and auto-expand
its <details>), web/templates/food_cache.html and food_custom_profiles.html
(delete-blocked alert links to /analysis/food-use-recipes?mode=ids&recipe_ids=...
and /analysis/food-use?mode=ids&meal_ids=... with sub_kind/sub_id set),
web/templates/analysis_food_use.html and analysis_food_use_recipes.html
(old_kind/old_id inputs take their default from sub_kind/sub_id).
```

**BLOCKED-DELETE MESSAGES (FOOD CACHE, CUSTOM FOOD PROFILES) NOW SPELL OUT HOW TO CLEAR EACH BLOCKER**

Trying to delete a food that's still used in a pantry entry, recipe, or logged meal used to just name the blocking item(s) (or, for Custom Food Profiles, not even that — see below) and say "remove/replace the food first," without saying how. Both pages now give a short numbered how-to per blocker type: which button to click on the Pantry page, which control to use on the recipe's edit page, which control to use on the meal page.

Custom Food Profiles' delete-blocked message previously didn't name the blocking item(s) at all, unlike Food Cache's — it now does too, with the same linked pantry/recipe/meal ids.

```
Scope: web/backend.py (food_custom_profiles_delete/food_custom_profiles_get
now carry blocked_pantry/blocked_recipes/blocked_meals through the redirect,
mirroring food_cache_delete()), web/templates/food_cache.html and
food_custom_profiles.html (delete-blocked alert now lists linked
pantry/recipe/meal ids plus a per-category how-to list instead of a
generic "remove/replace the food" line).
```

**RECIPE-RELINK SUGGESTIONS NO LONGER FIRE ON A SINGLE COINCIDENTAL WORD, AND YOU CAN NOW RELINK TO ANY RECIPE**

Editing a recipe used to offer to relink dangling "deleted recipe" references based on sharing just one word with the recipe's name — generic words like "protein" could trigger a nonsensical suggestion. It now requires sharing 2+ words (or an exact name match). The relink form also no longer assumes you meant the recipe you're currently editing — a dropdown lets you pick any suggested match or any recipe at all as the relink target. Separately, the opening page now shows an UPDATE banner if the database check (Food Cache > Database check) finds any referential-integrity problems, instead of requiring a visit to that page to notice.

```
Scope: db.py (find_broken_recipe_refs/find_relink_candidates now require
MIN_RELINK_SHARED_WORDS=2 shared words, or an exact case-insensitive name
match, via new _name_matches_for_relink() helper; new
find_relink_candidates() lists live recipes plausibly matching a deleted
recipe's name), web/backend.py (recipe_edit_get attaches candidates +
all_recipes_for_relink per broken group; recipe_relink_post takes a
target_recipe_id form field instead of always relinking to the recipe
being edited; index() runs check_db_integrity() and passes db_issue_count),
web/templates/recipe_edit.html (relink form now has a target-recipe
<select> with suggested/all-recipes optgroups), web/templates/home.html
(new UPDATE banner linking to /food/cache/db-check).
```

**FOOD SEARCH NO LONGER SURFACES (LET ALONE TOP-RANKS) FOODS MATCHING ONLY A GENERIC WORD**

Searching a multi-word query like "orange raw" could surface a user-drafted cached food like "Raw Brazil Nuts" — which shares nothing with "orange" — just because it contained the word "raw." Worse, under "Pantry, Cache, then Other" sort mode, that coincidental match could rank above every genuine "orange" result, since source category was compared before match quality. Generic prep/state words (raw, cooked, fresh, dried, frozen, canned, whole, ground, sliced, diced, chopped, boiled, roasted, baked, grilled, steamed, plain) can no longer trigger a match on their own. "Pantry, Cache, then Other" mode also now always ranks by how many query words matched first — pantry/cache only get listed ahead of other sources when they're tied on match quality, never when they matched fewer words.

```
Scope: db.py (search_cached_foods's user-drafted any-word fallback now
excludes a new _OR_FALLBACK_STOPWORDS set of generic prep/state words from
triggering a match by themselves), web/backend.py (_sort_search_results's
"grouped" mode now sorts by match count/word-mask from
numa_app.services.search_ranking.relevance_key first, with source category
only breaking ties between equally-good matches, instead of comparing
category before match quality at all).
```

#### August 26 program updates

**NEW: DELETE BUTTONS ON FOOD SEARCH RESULTS, AND A ONE-CLICK "UNSELECT ALL" FOR THE SOURCE FILTER**

Food Search rows now carry a Delete column: a pantry match gets "Remove from pantry," a food-cache match gets "Delete" (refused if something still references it, same as Food Cache's own Delete), and a recipe match gets "Delete" for the recipe — each asks for confirmation first. Separately, the Source filter row (already had "Select all sources") now also has an "Unselect all" button.

```
Scope: web/backend.py (_search_local_results()/_pantry_id_by_fdc() now attach
a pantry_id to pantry-sourced rows so the row can call the existing
/pantry/remove/{pantry_id} route), web/templates/_search_result_row.html
(new Delete column, reusing the existing /pantry/remove/{id},
/food/cache/delete, and /recipe/{id}/delete routes and their confirm()
patterns from pantry.html/food_cache.html/recipes.html), web/templates/
search.html and _search_api_rows.html (header cell and colspan bump),
web/templates/_source_filter_select.html + base.html (new
data-unselect-all-sources button, delegated click handler mirroring the
existing data-select-all-sources one).
```

#### August 25 program updates

**NEW: ADDING AN INGREDIENT NOW WARNS ABOUT AND AUTO-SAVES ANY UNSAVED RECIPE DETAILS**

On the Edit Recipe page, the Recipe details fields (name, servings, instructions, etc.) save separately from the ingredient list — editing one of those fields and then clicking "Add to recipe" without first clicking "Save recipe details" used to leave that edit sitting unsaved, easy to lose track of. Now, adding an ingredient while any recipe-detail field has an unsaved change shows a warning first; choosing to continue saves those pending changes automatically along with adding the ingredient. [learn more...](#recipe-ingredients)

```
Scope: web/templates/recipe_edit.html (recipe-details-form given an id;
new script tracks input/change events on it, intercepts submission of the
"add ingredient" and "add sub-recipe as ingredient" forms via a confirm()
warning, then POSTs the details form via fetch before letting the original
add-ingredient submit proceed). No backend route changes — this reuses the
existing /recipe/{id}/edit save endpoint and the existing
/recipe/{id}/ingredient/add(-recipe) endpoints, just sequenced from the
client side.
```

**NEW: COMPARE RECIPES CAN NOW SAVE AND RELOAD COMPARISON LISTS, LIKE COMPARE FOODS ALREADY COULD**

Compare Recipes had no way to save a set of recipes you'd compared before — every visit started from a blank list. It now works exactly like Compare Foods: a "Save this list" box at the bottom names and stores your current comparison, and a "Use a saved list" panel at the top of the page — including the very first, empty-list view — lets you reload, rename, or delete any saved comparison. [learn more...](#recipe-comparison)

```
Scope: db.py (new saved_recipe_comparisons table and
saved_recipe_comparison_save/list/get/rename/delete() functions, mirroring
the existing food-comparison saved_comparisons table), web/backend.py (new
/recipe/compare/save, /recipe/compare/load/{cmp_id},
/recipe/compare/saved/rename, /recipe/compare/saved/delete routes;
recipe_compare_get() now loads saved_lists), web/templates/recipe_compare.html
(new saved-lists panel and "Save this list" form, both copied from
food_compare.html's equivalent markup), tests/test_web.py (new
save/load/rename/delete regression test), user-manual.md (Recipe Comparison
Tables section).
```

**FIXED: A FAST CLICK ON A LOCAL FOOD SEARCH RESULT'S COMPARE CHECKBOX COULD GET SILENTLY DISCARDED, AND THE LOCAL-RESULTS SECTION NOW HAS ITS OWN HEADING**

Food Search renders your own pantry/cache/recipe matches instantly, then quietly replaces the whole results table a moment later once USDA/Open Food Facts respond, merging both sets together. Checking a compare checkbox on one of those instant local results *before* that replace finished got silently wiped out — the checkbox just looked broken, with no error or explanation. Checked boxes now carry across that replace. Separately, the local-results section at the top of the table now has its own "From your pantry, food cache, and recipes" heading, matching the "From USDA, Open Food Facts, and other external sources" heading the external section already had — the top section wasn't previously labeled at all.

```
Scope: web/templates/search.html (JS captures checked compare/confirm-aa
checkbox values before replacing #search-tbody's innerHTML, re-applies them
by value afterward; new local-results divider row), web/templates/_search_api_rows.html
(same new divider, kept in sync with search.html since both render the same
table body), tests/test_web.py (existing divider-ordering test extended to
also check the new local heading).
```

**NEW: "COPY AS DRAFT TO ADD AA DATA" SHORTCUT ON FOOD SEARCH RESULTS**

Any Food Search result missing confirmed amino acid data now shows a **Copy as draft to add AA data** link right in its row. Clicking it duplicates that food as an editable custom-profile draft and takes you straight to its edit page with the amino-acid-source search box ready — the one-click version of the "search, then go to Custom Food Profiles, then search again" path this previously required. [learn more...](#ts-no-aa-anywhere)

```
Scope: web/backend.py (new /food/custom-profiles/copy-from-search route,
shared _duplicate_food_as_draft() helper factored out of the existing
copy/{fdc_id} route), web/templates/_search_result_row.html (new per-row
form/button; confirm-aa-form restructured to a form= reference instead of
DOM nesting so each row can hold its own independent form),
web/templates/search.html (confirm-aa-form now closes before the results
table, select-all checkbox looked up by id instead of by form-descendant
query), tests/test_web.py (2 new tests, cached and uncached source),
user-manual.md (Drafted Food Profiles List and the "no AA data anywhere"
troubleshooting entry both mention the shortcut).
```

**SEARCH-RESULT CHECKBOXES ARE NOW COLOR-CODED WITH A LEGEND**

Food Search result rows can carry two different checkboxes — one to confirm amino acid data on an unconfirmed food, one to add the food to a comparison — and it wasn't obvious they were two separate controls when both appeared on the same row. The "confirm AA" checkbox is now orange and the "compare" checkbox is now purple, with a small legend above the results table explaining what each one does.

```
Scope: web/templates/_search_result_row.html (checkbox-confirm-aa /
checkbox-compare classes), web/templates/search.html (select-all checkbox
recolored, new legend above the results table), web/static/style.css
(accent-color rules + legend swatches).
```

**PROTEIN POWDERS NOW ACCEPT TABLESPOON/CUP AMOUNTS WHEN ADDED TO A RECIPE, AND THE EDIT-RECIPE PAGE NOW SHOWS THE RECIPE'S ID**

Adding an ingredient like "Soy protein isolate" to a recipe using a volume amount (e.g. `2 T`) was silently rejected with "no density data is available for this food" — the density lookup only recognized "protein powder" and "whey powder" by name, not "protein isolate" or "protein concentrate". Those are now recognized too. Separately, the Edit Recipe page now shows the recipe's ID number under its title, matching other pages that display it.

```
Scope: usda_nutrients.py (_DENSITY_TABLE gained "protein isolate" and
"protein concentrate" keywords alongside the existing "protein powder"/"whey
powder" entry), tests/test_usda.py (regression test), web/templates/recipe_edit.html
(recipe ID shown under the page title).
```

**RECIPE COMPLEMENT SUGGESTIONS NOW EXPLAIN THEIR WHOLE-BATCH SIZING AND SHOW A PER-SERVING AMOUNT**

Protein Complement Suggestions on a recipe's own page size every gram amount to the recipe's full total across all its servings, not one serving — that's intentional, since the only way to act on a suggestion is to add an ingredient to the whole batch. But a 4-serving recipe could show "add 83 g of soy protein isolate" with no indication that figure was for the whole pot, not one bowl. A note now appears at the top of the section for any recipe with more than one serving explaining this, with a link to further detail in the manual, and every gram amount throughout the section (gap closers, graduated steps, DIAAS boosters, two-food and two-step combinations) now also shows its per-serving equivalent in parentheses. [learn more...](#comp-recipe-scale)

```
Scope: user-manual.md (new "Recipe analysis: amounts are sized to the whole
batch" subsection under Protein Complement Suggestions, #comp-recipe-scale),
web/templates/recipe_detail.html (top-of-section note for multi-serving
recipes; new per_serving_note() macro applied to every grams display in the
complements section), tests/test_web.py (new regression test).
```

#### August 23 program updates

**NIACIN AND FOLATE NO LONGER FALSELY FLAG NORMAL DIETS AS OVER THE LIMIT**

The **UL** column on nutrient analysis tables no longer warns about niacin (B3) or folate (B9) from ordinary food intake. Their published upper limits only apply to synthetic/supplemental forms (fortified food or pills) — whole-food niacin and folate don't carry the same risk, the same reasoning already applied to magnesium. Every table with a UL column now also carries a "Special note re: UL scope" callout right in the table footer explaining this in plain language, rather than leaving it to a manual page few people open. If you take a supplement containing niacin, folate, or magnesium, set a [custom max limit](#maxlimits) to track that. [learn more...](#maxlimits)

```
Scope: profile.py (compute_upper_limits() no longer includes niacin_mg or
folate_mcg, doc comment explains why — mirrors the existing magnesium
exclusion), tests/test_profile.py (expected UL dict updated),
web/templates/_ul_column.html (note() macro gained an inline "Special note
re: UL scope" callout, shown on every nutrient table with a UL column —
food/recipe/meal/daily summary/trend/print), user-manual.md (Maximum
Nutrient Limits table and counts updated from 14 to 12 built-in ULs).
```

**MAINTENANCE: WEEKLY SWEEP — 3 TEST GAPS CLOSED, README FEATURE LIST CAUGHT UP, CHANGELOG PRUNED**

Item 1 (CLAUDE.md drift) and item 2 (vendored Bootstrap, still 5.3.8, current) found nothing to fix. Item 6 (test coverage) found three real gaps from the last few days of shipped changes and closed all of them: the Food Cache delete-refusal page rendering a food/pantry/recipe/meal blocker as an actual link, the My Pantry search results' "Remove from pantry" button, and Food Use in Meals/Recipes linking each row to its own analysis page — each now has a regression test. Item 5 (README.md) added three shipped features that were missing from the public "Key features" list: side-by-side comparison, food-use analysis, and the database integrity checker. Item 4 (manual consolidation) folded the delete-blocker and pantry-remove-button behavior into the manual body itself, and removed a stale internal editorial note that had outlived its purpose. Item 3 pruned the changelog back to roughly the last two weeks. Item 7 (link check) found nothing broken in-manual, but turned up something outside the manual's scope worth a look: `https://github.com/tom-cloyd/NutriMagnus` and its `/releases` page both return a genuine 404 right now, not a bot-block — worth confirming the repo's current visibility/location before the next release announcement, since `README.md`'s Download section and clone instructions point there.

```
Scope: tests/test_web.py (3 new/extended tests), README.md (Key features list),
user-manual.md (Food Cache and My Pantry sections in Part 3, stray editorial
note removed from Appendix A header, test-count sentence in Part 1).
```

#### August 22 program updates

**NEW: FOOD USE IN MEALS AND FOOD USE IN RECIPES NOW LINK EACH FOOD/RECIPE NAME TO ITS ANALYSIS PAGE**

The Food Use in Meals and Food Use in Recipes tables listed each food and recipe by name only, with no way to jump to that food's or recipe's own nutritional analysis page short of re-searching for it elsewhere. Every row's name is now a link — to `/food/{id}` for a food, `/recipe/{id}` for a recipe — except where there's genuinely nothing to link to (a deleted recipe, or a food added without a linked USDA/Open Food Facts/etc. id).

```
Scope: web/templates/analysis_food_use.html, web/templates/analysis_food_use_recipes.html.
Both already had fdc_id/recipe_id/kind (and, for Food Use in Meals, a deleted flag)
per row from web/backend.py's analysis_food_use / analysis_food_use_recipes routes;
this only changed the row-name markup, no backend/query changes.
```

#### August 21 program updates

**CLARIFY: "CAN'T DELETE THAT FOOD" NOW NAMES AND LINKS EVERY PANTRY ENTRY, RECIPE, AND MEAL BLOCKING IT**

Food Cache → Delete used to refuse with a generic "it's still used in a pantry entry, recipe, or logged meal" message, giving no way to find which ones without hunting through Pantry, Recipes, and Meals & Log by hand. It now lists every blocking pantry entry, recipe, and meal by id, each one linked straight to the place you'd remove or replace that food — e.g. "pantry: 34 | recipe: 12 | meal: 9, 72".

```
Scope: db.py (food_references — now returns id lists instead of counts;
still truthy/falsy the same way so existing callers were untouched), web/backend.py
(food_cache_delete passes the blocked ids through as blocked_pantry/blocked_recipes/
blocked_meals query params, food_cache_get parses them back into lists), web/templates/
food_cache.html (renders each id as a link: pantry ids to /pantry, recipe ids to
/recipe/{id}/edit, meal ids to /meal/{id}).
```

**NEW: REMOVE A FOOD FROM YOUR PANTRY DIRECTLY FROM SEARCH RESULTS**

Searching My Pantry for a food already in your pantry used to just label its search-results row "Already in pantry" with no action available — removing it meant scrolling down to find the matching row in the pantry list below. That row now has a **Remove from pantry** button instead, so you can add or remove a food from the same search results table.

```
Scope: web/backend.py (pantry_get), web/templates/pantry.html. Search results whose
source is "pantry" now carry the underlying pantry row's id (pantry_id_by_fdc, built
from the same items list used to render the pantry table below); the template swaps
the static "Already in pantry" label for a form posting to the existing
/pantry/remove/{pantry_id} route when that id is present.
```

#### August 20 program updates

**NEW: SEARCH NOW WARNS YOU WHEN A SOURCE IS UNCHECKED, AND USDA/OFF LEAD THE SOURCE FILTER**

An unchecked Source filter box (e.g. "Recipes") is sticky — it stays unchecked on every search box in the app until re-checked — which made a genuinely missing result (a recipe that should have matched, say) indistinguishable from a search or ranking bug, since nothing on the page said a source had been excluded. The Foods search page and the Meals & Log "Add Food or Recipe" panel now show a small red **Omitted from search: ...** note next to the Sort by control whenever one or more sources are unchecked, naming exactly which ones. Separately, the Source filter checkbox row itself now lists **USDA** and **Open Food Facts** — the two most-used external sources — ahead of the smaller regional datasets (CoFID, AFCD, CIQUAL) and Canadian Nutrient File, instead of alphabetically/arbitrarily mixed in among them.

**FIX: YOUR OWN PANTRY/CACHE/RECIPE MATCHES NOW ALWAYS SHOW FIRST, IN THEIR OWN SECTION**

The previous fix (below) stopped a food already in your cache from being dropped entirely, but it could still end up ranked far down the list — behind dozens of external USDA/Open Food Facts results that happened to word-match the search more closely — so finding it still meant scrolling. Every search results table in the app (Foods search, Food Cache, My Pantry, Meals & Log's Add Food or Recipe, a recipe's ingredient search, Compare Foods, Analyze a Food Portion, Convert a Portion) now always shows your Pantry/Food Cache/Recipe matches first, in their own group, with a labeled divider before the ranked USDA/Open Food Facts/CNF results below — regardless of which sort order is selected.

**FIX: A FOOD ALREADY IN YOUR CACHE OR PANTRY COULD VANISH FROM SEARCH RESULTS ENTIRELY**

Search results merge your own Pantry/Food Cache/Recipe matches with USDA/Open Food Facts/Canadian Nutrient File results, then trim to the "Show up to ___ results" limit (default 25). That trim didn't distinguish a free, already-known local match from an external one — so a food already in your cache could be crowded out and never shown at all, if enough external results happened to word-match the query more closely. Example: searching "vitamins daily" for a cached food named "Complete multivitamin" (no literal "daily" in the name) could bury it under dozens of branded products literally named "Daily Vitamins." Local matches are now always kept regardless of the limit — the limit only bounds how many external results fill the remaining slots. Affects every food search in the app.

**NEW: JUMP FROM ANY SEARCH RESULTS OR LIST STRAIGHT INTO COMPARE FOODS/RECIPES**

Foods search results, Food Cache, My Pantry, and the Recipes list all now have a **Compare** checkbox next to each row, plus a **Compare nutrition of selected** button above the list — check the items you want, click the button, and land on Compare Foods (or Compare Recipes) with those items already added, no need to redo the search there. On Foods search, where a result can be either a food or a recipe, foods and recipes get separate checkboxes and buttons since the two comparison pages can't mix them. [learn more...](#compare-checkboxes)

**CLARIFY: THE DCP LINE UNDER A FOOD/RECIPE/MEAL/DAY TITLE IS NOW VISUALLY DISTINCT, NOT JUST GRAY METADATA**

The digestible complete protein (DCP) summary line just under a food, recipe, meal, or day page's title — added August 17 — was styled identically to the brand/serving-size metadata right below it: small, gray, and easy to skim past entirely. It's now normal-sized black text with the key figure bolded and labeled "(DCP)" explicitly, so it reads as the headline stat it's meant to be rather than incidental page furniture. The data itself was always there and correct — this was a pure legibility fix.

**CLARIFY: COMPLEMENT SUGGESTIONS SPELL OUT WHOSE "RAW" PROTEIN IS BEING ADDED**

Every protein-complement suggestion's "Adds: X g digestible protein (from Y g raw)" line left "raw" ambiguous — raw protein in what, exactly? It now reads "from Y g raw protein in this addition" for a single suggestion, or "raw protein combined" for a two-food pairing — making clear it's the protein contributed by the suggested food(s) at that serving size, not the base food's own protein. Appears everywhere complement suggestions do: food, recipe, meal, daily-summary, and trend pages.

**CLARIFY: FOOD CACHE NOW EXPLAINS THE CLAUDE AI FETCH BUTTONS BEFORE YOU CLICK THEM**

The checkbox-and-button pair for fetching missing amino acid data via Claude AI used to appear on the Food Cache page with no explanation — just "Select all missing AA data" and "Fetch missing data from Claude AI" buttons with no context. A brief line above them now explains what checking a box and clicking Fetch actually does, with a **Learn more** link to the full walkthrough. [learn more...](#fetch)

**NEW: CHECK DATABASE INTEGRITY — FIND AND FIX BROKEN FOOD/RECIPE REFERENCES**

Foods → **Check database integrity** (also on the Food Cache page) scans for pantry entries, recipe ingredients, and logged meal items that still point at a food or recipe no longer in the cache — previously undetectable except by the food page failing to open ("USDA API 400: bad request" for an Open Food Facts food). Each kind of problem gets its own fix button with a plain-language note on what that fix actually changes (a pantry-entry removal is harmless; a recipe-ingredient or logged-meal-item removal recalculates that recipe's or day's totals without it) — they're deliberately not bundled into one "fix everything" button. Deleting a food from the cache also now refuses when a pantry entry, recipe, or meal still uses it, so this situation can no longer happen through normal use — Archive is offered instead. [learn more...](#db-check)

**FIX: "LEARN MORE" ON THE FETCH-FROM-CLAUDE-AI PAGE NOW JUMPS TO THE RIGHT SECTION**

The "Learn more" link on Food Cache → Fetch missing data from Claude AI pointed at a manual anchor that didn't exist, so it always landed on the manual's title page instead of the explanation. It now jumps straight to "Fetching missing amino acid data with Claude AI" in the Food Cache section. [learn more...](#fetch)

**NEW: PRUNE UNUSED FOODS LETS YOU UNCHECK ANY FOOD YOU WANT TO KEEP**

Foods → Food Cache → Prune Unused Foods now lists every unused food with a checkbox, checked by default. Uncheck any you'd rather keep before clicking "Prune checked foods" — previously the page always deleted every listed food with no way to exclude individual ones. Pruning still permanently deletes the food from the cache (a real database delete, not an archive) — Check all / Uncheck all buttons are provided for convenience.

**FIX: PLANT-BASED-ONLY PREFERENCE NOW APPLIES TO YOUR OWN PANTRY AND RECIPE COMPLEMENT SUGGESTIONS**

Setting Dietary Preference to "Plant based only" (or "Vegetarian") in Settings only ever filtered the built-in reference-table complement suggestions — an animal-sourced food sitting in My Pantry, or in one of your own analyzed recipes, could still turn up as a suggested complement (e.g. "Organic Eggs" suggested alongside peanut butter). Both preferences now also apply to your own pantry items and recipes. [learn more...](#comp)

**FIX: SETTINGS NO LONGER SHOWS A STALE "DIETARY PREFERENCE SAVED" MESSAGE**

The "✓ Dietary preference saved" confirmation on the Settings page used to stay on screen even after you changed the radio selection without clicking Save preference — making it look like the new, unsaved choice had already been saved. Changing the selection now clears that message until you actually save again.

#### August 18 program updates

**DIAAS-BOOSTING TABLES NOW EXPLAIN THEIR COLUMNS AND SHOW % INCREASE**

The "DIAAS-Boosting Options" tables on the meal, full-day, food, and recipe pages now label the DCP column "DCP achieved" (matching the Protein Complement Suggestions table) and add a "% increase" column, with a footer note spelling out what each column means. The graduated-addition tables on the meal and recipe pages gained the same footer note. [learn more...](#comp)

#### August 17 program updates

**MAINTENANCE: WEEKLY SWEEP — 10 NEW REGRESSION TESTS, VENDORED BOOTSTRAP CONFIRMED CURRENT, CHECKLIST TRIMMED**

The rest of this week's sweep: item 6 (test coverage) cross-checked two weeks of shipped changes against `tests/` and found 7 real gaps, most notably the Recipe Edit page's "Running totals" — the DCP-undercounting-for-sub-recipe-ingredients bug fixed August 15 had no regression test guarding it. All 7 got a test rather than being deferred to a future sweep: `test_recipe_edit_running_totals_include_subrecipe_ingredient` (the running-totals fix); four new tests in `tests/test_portions.py` for `_ing_amount_display()` (previously zero coverage despite fixing a real save-rejection bug); a numeric cross-check plus a "suppressed at zero" test for the unusable-protein line; a numeric cross-check for the DCP summary line under a food's title; a test for the "copy nutrient profile from another food" endpoint; a test that a nutrient's UL badge actually turns "near"/"over" as a day's total approaches or passes a personal max limit, not just that the column renders; and a test for the piece-based-food gram-display fix when a food page is opened via a recipe/meal ingredient link. Item 7: the vendored `web/static/vendor/bootstrap/` (5.3.8) is still the current upstream release — no update needed. The checklist itself dropped its "CLI/web parity" item (moot now that the CLI is gone) and gained explicit grep/curl recipes for items 1 and 2, plus a note to watch for changelog entries that contradict each other.

**MAINTENANCE: WEEKLY SWEEP — DOCS DE-DRIFTED, DEAD LINK FIXED, LEFTOVER CLI COMMANDS REMOVED**

This week's maintenance sweep (items 1-5 of the recurring Weekly sweep checklist) found and fixed real drift, not just tidying. `CLAUDE.md`'s package layout was missing 13 `numa_app/services/` modules added since the last sweep. The Canadian Nutrient File source link in [Food data](#food-data) pointed at a dead API path; it now points at the live CNF search page. `README.md`'s Key Features list gained three shipped features it was missing (nutrient trends/plotting, CSV export/import, archive). Several spots in the manual — the Recipes List Table, Protein Digestibility Overrides, and the Archiving section — still described typed single-letter commands (`a{id}=analyze`, `y{id}=archive/restore`, and so on) from the CLI that was removed 2026-08-04; these now describe the actual web-app buttons and forms instead. A handful of "Type ?keyword" CLI-help references throughout Part 5 were converted to real `[links](#anchor)`. Five real features that had only ever been described in this changelog — the Source filter's "Select all sources" button, the Recipe Introduction field, Compare Foods' AA column and Print/CSV buttons, the meal-specific Top Contributors header note, and the Protein Digestibility table's sort-by-protein/self-explanation — were folded into the manual body where a reader would actually look for them. The changelog itself was pruned back to roughly the last two weeks (entries before August 4 removed; already safe per the note above this log).

**CLARIFY: MANUAL LINKS NEXT TO ANOTHER MANUAL LINK NOW SIT IN THEIR OWN PARENTHESES**

A few section headings carry two "Learn more →"-style links side by side (e.g. "Protein Quality" followed by "About the FAO reference"). The first link's arrow used to sit right in front of the second link's text, reading as if it pointed there. Each now gets its own parentheses — `(Learn more →) (About the FAO reference →)` — so neither looks like it's pointing at the other. The gap inside those parentheses has also been tightened everywhere it's used, to a single space instead of the wide gap the link's own spacing left behind.

**NEW: "WHAT ARE THESE SOURCES?" LINK ON EVERY SEARCH'S SOURCE FILTER**

The Source filter (the row of PANTRY / CACHE / RECIPE / USDA / OFF / CNF / CoFID / AFCD / CIQUAL checkboxes shown on every search) now has a **What are these sources? →** link right next to the "Source" label, jumping straight to [Food data — where it comes from and how it is stored](#food-data) — those abbreviations meant nothing without it.

**FIX: MEAL PAGE'S MANAGEMENT BUTTONS NOW ALL THE SAME HEIGHT**

On a meal's page, the row of buttons above "Add Food or Recipe" (Mark complete, Analyze full day, Print / Save as PDF, Rename / change date, Delete meal) rendered at two different heights — a plain link-styled button stretched to fill the row while a button nested inside its own form didn't. All five now render at a consistent height, on this page and on a recipe's equivalent action row.

**CLARIFY: PROTEIN DIGESTIBILITY TABLE NOW EXPLAINS ITSELF AND SORTS BY RAW PROTEIN**

The "Meal foods: Digestibility" / "Ingredients: digestibility" table (in Meal-Level and Complete Protein Analysis, on food, recipe, meal, and daily-summary pages) used to list foods in whatever order they were added, with no explanation of what the table was for. It now opens with a plain-language description of what the table shows, and sorts by raw protein, highest first — the foods actually driving the meal's or recipe's numbers are now at the top. On the food and recipe pages, where the table has a DCP column, a note explains that DCP there is just each food's raw protein times one shared meal- or recipe-wide score, so it's not that food's own standalone quality — two foods can show the same DCP simply by contributing equal protein, even with very different amino acid profiles, and that shared multiplier is also why sorting by protein and by DCP land on the same order. [Top Contributors](#top-contributors) is where to look for each food's own standalone quality instead.

**CLARIFY: "RESET SEARCH" RENAMED "CLEAR SEARCH"**

The button that clears a search box and resets its Source and result-limit filters back to default is now labeled **Clear search** instead of the more ambiguous "Reset search" — same behavior, clearer name. Appears on Foods → Search, Meals & Log → Add Food or Recipe, and Recipes → Add Ingredient.

**NEW: "SELECT ALL SOURCES" BUTTON ON EVERY SOURCE FILTER**

Every search's Source filter (the row of USDA / Open Food Facts / Canadian Nutrient File / etc. checkboxes) now has a **Select all sources** button that re-checks every box in one click — handy after narrowing a search down and wanting all sources back without retyping your search or losing your other settings. [learn more...](#search-memory)

**NEW: SEE HOW MUCH PROTEIN IS LOST TO AN INCOMPLETE AMINO ACID PROFILE**

Every food, recipe, meal, and day page that shows digestible complete protein (DCP) now also states how much of that raw protein *can't* be built into tissue — in grams and percent — right below the existing DCP line, whenever that amount is greater than zero. [learn more...](#unusable-protein-fate)

**NEW: THE MAIN MENU BAR NOW STAYS PINNED TO THE TOP OF THE SCREEN**

The blue nav bar (Foods / Recipes / Meals & Log / Analysis / Settings / Manual) no longer scrolls away — it stays visible at the top no matter how far down a page you scroll, so a menu is always one click away.

#### August 16 program updates

**FIX: ESC AND CLICKING OUTSIDE NOW CLOSE POPUP "EDIT" FORMS WITHOUT SAVING**

The floating "Edit" popups on meal items, recipe ingredients, and "Rename / change date" had no way to back out of once opened — Esc did nothing, and clicking elsewhere on the page did nothing. Both now close the popup and discard whatever you'd typed, same as canceling any other dialog.

**CLARIFY: MEAL-PAGE TOP CONTRIBUTORS IS ALWAYS FOOD-LEVEL**

On a meal's Top Contributors table, the column header now just says "Food" (not "Food / Recipe"), with a note underneath: any recipe used in that meal is broken into its individual foods for this table, so no row ever names a whole recipe. (A recipe's *own* Top Contributors table can legitimately show a sub-recipe by name, so it keeps the "Food / Recipe" header.)

**NEW: RECIPE INTRODUCTION FIELD**

Recipes now have an **Introduction** field for background — where it came from, why you like it, serving notes — anything that isn't the step-by-step procedure. On the recipe edit page it sits right after Ingredients; on the recipe's own page and on the printed/PDF version it appears right after the title. It's one of the checkboxes on the "Include on this printout" picker, so it can be left off a printout like any other section.

**FIX: CHANGING "RANK BY" OR "SHOW" ON TOP CONTRIBUTORS NO LONGER JUMPS TO THE TOP OF THE PAGE**

Changing the nutrient or count in the Top Contributors section (Meal/Recipe pages) reloads the page and is meant to land you back at that section. It was instead landing at the very top of the page, because a search box or "Add Food or Recipe" field further up the page could grab focus (and the scroll position that comes with it) after the intended scroll had already happened. The page now re-asserts the scroll position after everything else on the page has finished loading, so it reliably wins.

**NEW: PRINT AND CSV EXPORT FOR THE FOOD COMPARISON TABLE**

The Compare Foods page's nutrient comparison table now has **Print comparison table** and **Download CSV** buttons. Print opens your browser's print dialog with just the comparison table (no nav, search box, or other page chrome); the CSV download gives one row per nutrient and one column per food, ready to open in a spreadsheet.

**NEW: AA COLUMN ON FOOD COMPARE PAGE**

The Compare Foods page's food list now has an **AA** column showing at a glance whether each food has amino acid data (✓) or not (✗), right after the food name.

---

### B. Raw protein, protein quality, and protein digestibility {: #appendix-b}
[//]: # "develop"

#### The core problems with protein

When you eat protein, not all of it is equally useful to your body. The usefulness depends on three things: **how much** protein you eat, and **how well-matched** its amino acid composition is to human physiological needs, and **how digestible** it is. 

#### The Nine Essential Amino Acids and their required relationship

Your body requires twenty amino acids to build proteins. Eleven of these it can synthesize from other raw materials. The remaining nine — the essential amino acids ([EAAs](#gloss-eaa)) — must come from food. 

These nine must all be present simultaneously for protein synthesis to proceed. They must also be present in the right amount. If any one of them is insufficiently supplied, then to the degree that its amount is short the other cannot be used. The surplus of the other eight cannot be stored and is instead broken down for energy — a functional waste.

In summary, the *pattern* of [EAAs](#gloss-eaa) in a food matters, not just the total protein quantity.

#### The required EAA pattern, established by the FAO

The Food and Agriculture Organization ([FAO](#gloss-fao)) of the United Nations leads international efforts to defeat hunger, achieve food security for all, and make sure that people have regular access to enough high-quality food to lead active, healthy lives.

Research has established human requirements for each [EAA](#gloss-eaa) independently, through controlled human trials. For each amino acid separately, researchers determined how much a healthy adult needs per day to maintain physiological function. From these studies came absolute daily requirement figures for each of the nine [EAAs](#gloss-eaa), expressed in milligrams per kilogram of body weight per day.

Separately, research has established how much total protein a healthy adult needs per day. By dividing each [EAA](#gloss-eaa)'s daily requirement by the total daily protein requirement, researchers produced a normalized figure: how many milligrams of each [EAA](#gloss-eaa) a person needs per gram of protein consumed. These normalized figures are the **[FAO](#gloss-fao) reference values**.

From the reference values for each amino acid which were determined *independently* come the ratios between [EAAs](#gloss-eaa). The reference values' relationship are a byproduct of the separately established requirements — not the starting point.

#### The FAO reference values tell you about the quality of protein in a food

The reference values allow a simple and powerful question to be asked about any food protein source:

> If I eat enough of this food to meet my total daily protein needs, will each essential amino acid also arrive in sufficient quantity?

If the answer is yes for all nine [EAAs](#gloss-eaa), the protein is high quality — no bottleneck will limit your body's ability to use it. If the answer is no for even one [EAA](#gloss-eaa), that amino acid becomes your limiting factor.

#### How the Ratio Is Calculated in NuMa

For each essential amino acid, the ratio shown in [NuMa](#gloss-numa)'s output is computed in two steps:

**Step 1 — convert [AA](#gloss-aa) amount to mg per gram of total protein:**

    (AA content in g per 100g food ÷ protein content in g per 100g food) × 1000

This expresses how many milligrams of that amino acid are present for every gram of total protein the food contains.

**Step 2 — divide by the [FAO](#gloss-fao) reference value:**

    mg AA per g protein ÷ FAO reference value (mg/g protein)

A ratio of 1.0 means the food hits the reference exactly. A ratio of 2.14 means it delivers more than twice the required amount. A ratio of 0.80 means it delivers only 80% of what is needed.

**Concrete example — cocoa ([USDA](#gloss-usda) #169594):**

    Cocoa Protein total:      19.6 g per 100g food
    Tryptophan AA in cocoa:   0.293 g per 100g food

    Step 1:  (0.293 / 19.6) × 1000  =  14.9 mg tryptophan per g protein
    Step 2:  14.9 / 7               =  2.14

The [FAO](#gloss-fao) reference value for tryptophan is 7 mg/g protein. Cocoa's protein delivers 14.9 mg/g — 2.14 times what is required.

Think for a moment: what if cocoa contained none of the needed [EAAs](#gloss-eaa)? Then the protein it contained would be unusable, if it were your only protein source. It could only be broken down for energy - the fate of all unusable protein. And what if it contained all the needed [EAAs](#gloss-eaa), in the right amount - except one was totally missing? That one would make all the other unusable.

#### Why Total Protein Is the Denominator

A reasonable question is why the ratio uses total protein (including non-essential amino acids) as its denominator rather than comparing [EAA](#gloss-eaa) amounts in absolute terms.

Total protein is a normalizing device — **a common scale that makes the quality metric meaningful across foods with very different protein concentrations and very different serving sizes.**

The practical interpretation is direct: **if a food's protein clears all nine floors, eating enough of that food to meet your daily protein target will automatically also deliver your daily [EAA](#gloss-eaa) requirements.** No separate [EAA](#gloss-eaa) accounting is needed. A food that fails even one floor means you would reach your protein target before accumulating enough of that [EAA](#gloss-eaa) — the protein source is insufficient on its own.

The non-essential amino acids that make up the rest of the protein are biologically irrelevant to this specific calculation. They appear in the denominator only because total protein is the natural unit for expressing protein intake. They are not required to "activate" the [EAAs](#gloss-eaa) — they are simply passengers.

#### What "Complete" Actually Means

"Complete" does not mean the amino acid ratios are all close to 1.0, or close to each other. It means **every one of the nine ratios is at or above 1.0** — each amino acid clears its own independent floor.

The nine [FAO](#gloss-fao) reference values were determined in separate human trials, one amino acid at a time. They are not ratios between amino acids; they are nine independent thresholds. Having tryptophan at 2.14× its floor while [Met+Cys](#gloss-met-cys) sits at 1.02× its floor creates no imbalance — the tryptophan surplus cannot compensate for a deficit in another amino acid, but it does not create one either.

A food can therefore have wildly varying ratios across its amino acids and still be complete. Cocoa's protein ranges from 1.02 to 2.25 across the nine amino acids — a factor of more than two between the lowest and highest — and is still complete because nothing falls below 1.0.

The floor analogy: imagine a building with nine rooms, each with its own minimum ceiling height requirement. A room that comfortably exceeds its requirement does not help or hurt any other room. Every room must pass independently.

#### The Limiting Amino Acid — A Practical Analogy

When any one [EAA](#gloss-eaa) ratio falls below 1.0, that amino acid is "limiting" — it acts as a bottleneck that caps how much protein your body can fully incorporate into tissue.

A concrete analogy: you are mixing mortar to build a small wall. You have plenty of dry mix but run out of water before you have mixed enough for the full job. Without water, the remaining dry mix is unusable — you can build only 90 bricks worth of wall instead of 150. The water is your [limiting amino acid](#gloss-limiting-amino-acid). The unused dry mix is the protein your body cannot build into tissue, and instead breaks down and excretes.

Complementary proteins work by pooling the [limiting amino acids](#gloss-limiting-amino-acid) from multiple foods — a grain that is low in lysine paired with a legume that is rich in lysine can together clear all nine floors even though neither does so alone.

**The fate of unusable (not "complete") protein.** That unused portion isn't simply carried along or saved for later — your body has no way to bank amino acids the way it banks fat. Protein that can't be matched to the missing (limiting) amino acid is broken apart: the nitrogen-containing amino group is stripped off (deaminated) and converted to urea, which the kidneys excrete in urine; the leftover carbon skeleton is burned for energy or converted into glucose or fat, the same as it would be from a carbohydrate or fat source. So none of the calories are wasted — but as *protein*, it's gone. It cannot be retrieved later and built into muscle, enzymes, or any other tissue. This is exactly why pairing complementary foods matters: it lets more of what you eat cross the threshold and actually become usable protein, instead of being deaminated and excreted. Wherever NuMa shows digestible complete protein (DCP) alongside raw protein, the gap between the two is this same effect in numbers.
{: #unusable-protein-fate}

#### Digestion, Synthesis, and Catabolism — the Full Path {: #protein-fate-detail}

The paragraph above is the practical summary. Here is the fuller mechanism, for readers who want it.

Digestion itself doesn't distinguish complete from incomplete protein. Every protein you eat, regardless of amino acid profile, is broken down by digestive enzymes into free amino acids and small peptides, absorbed across the intestinal wall, and released into the bloodstream, joining the body's general pool of circulating amino acids. The "complete vs. incomplete" distinction only starts to matter at the *next* step.

Building new protein — muscle, enzymes, hormones, anything — requires all nine [EAAs](#gloss-eaa) to be present at once, in roughly the ratio the specific protein being built calls for. The body's protein-building machinery can't substitute one amino acid for another. If a meal's amino acid profile is short on one or more EAAs relative to what's needed, that shortfall — the [limiting amino acid](#gloss-limiting-amino-acid) — caps how much new protein can be built from that meal, no matter how abundant the other eight are.

The body has no storage depot for spare amino acids, the way it stores glucose as glycogen or extra energy as fat. Once the amount usable for building new protein is accounted for, whatever amino acids are left over get broken down for other uses (mostly in the liver, with the branched-chain amino acids handled largely in muscle instead). That breakdown happens in two parts: the nitrogen-containing amino group is stripped off and processed through the urea cycle for excretion in urine (some of it gets recycled into other, nonessential amino acids or into nucleotides and hormones instead); and the leftover carbon skeleton is used to make glucose, converted into ketone bodies, burned directly for energy, or stored as fat if there's a surplus.

**Does this mean every meal needs to be a "complete" protein on its own?** No — and this is where the picture gets more reassuring. The classic reasoning here (Young & Pellett, 1994)[^14] is that the body turns over roughly 250–300 g of its own protein every day, far more than a typical meal provides, and the free amino acid pool released by that ongoing turnover can help fill in whatever a given meal's protein is short on. That's the biochemical basis for the now-standard advice that complementary foods (rice with beans, for instance) don't need to be eaten together at the same meal — pairing them anywhere across a varied day is enough. A 2024 controlled feeding study testing this directly[^15] — comparing meals built from complete, complementary, and single incomplete protein sources, all matched for total protein — found no significant difference in how much new muscle protein was built in the hours afterward, even though the amount of certain EAAs available in the bloodstream did differ between conditions. That suggests the real-world cost of an occasional single incomplete-protein meal may be smaller in practice than the classic model implies, though it's an area of active research rather than settled fact.

None of this changes what NuMa reports: it's still true that, gram for gram, a food or meal with a limiting amino acid yields less usable ([DCP](#gloss-dcp)) protein than its raw protein total. What the research adds is context on the time frame that matters — it's your protein pattern across the day, not any single meal in isolation, that determines how much of what you eat actually becomes usable protein.

#### The DIAAS Score

The Digestible Indispensable Amino Acid Score ([DIAAS](#gloss-diaas)) measures how much of a food's protein your body can actually use. For each [EAA](#gloss-eaa), it calculates:

> (mg of that [EAA](#gloss-eaa) actually absorbed per gram of food protein) ÷ ([FAO](#gloss-fao) reference value for that [EAA](#gloss-eaa))

The word "actually absorbed" is critical. Not all amino acids in a food survive digestion intact and cross into the bloodstream. [DIAAS](#gloss-diaas) uses [ileal digestibility](#gloss-ileal-digestibility) — the fraction of each amino acid absorbed by the end of the small intestine — to correct for this. The result is a score based on what your body actually receives, not merely what was in the food.

A ratio of 1.0 means the food **delivers** exactly the required amount of that [EAA](#gloss-eaa) (per gram of protein eaten). A ratio below 1.0 means a shortfall — that [EAA](#gloss-eaa) is limiting. A ratio above 1.0 means a surplus above the floor. **The overall [DIAAS](#gloss-diaas) score for the food is set by whichever [EAA](#gloss-eaa) has the lowest ratio — the weakest link.**

#### A Concrete Example: Chia Seed

Consider a protein quality analysis of chia seed that produces output like this:

```
 Amino Acid      Ratio vs. FAO
 Tryptophan               3.77
 Threonine                1.86
 Isoleucine               1.61
 Leucine                  1.40
 Lysine                   1.30
 Methionine               1.62
 Phenylalanine            1.62
 Valine                   1.47
 Histidine                2.14
```

Every ratio exceeds 1.0. This means that if you eat enough chia seed to meet your total daily protein requirement, every one of the nine [EAAs](#gloss-eaa) will arrive in at least the required amount. No bottleneck. No [limiting amino acid](#gloss-limiting-amino-acid). The protein is complete and efficiently usable.

Lysine at 1.30 is the weakest link — your slimmest margin. It would be the first amino acid to fall below the floor if you ate progressively less chia. But at 1.30, it still clears the threshold comfortably.

Importantly, these ratios do *not* mean that 100 grams of chia seed provides all the [EAAs](#gloss-eaa) you need for a day. Chia seed contains roughly 17 grams of protein per 100 grams. If your daily protein target is 80 grams, 100 grams of chia gets you only about 21% of the way there. The quality score tells you that every gram of protein chia delivers is efficiently usable — but you still need to eat enough of it to accumulate your daily protein target.

Think of it like fuel efficiency: a car that gets 50 miles per gallon is efficient, but knowing that tells you nothing about whether one gallon is enough to reach your destination. Quality and quantity are separate questions answered separately.

#### Summary

| Concept | What it answers |
|---|---|
| [FAO](#gloss-fao) reference values | How many mg of each [EAA](#gloss-eaa) a human needs per gram of protein consumed |
| [DIAAS](#gloss-diaas) ratio for one [EAA](#gloss-eaa) | Does this food deliver enough of that [EAA](#gloss-eaa), accounting for digestibility? |
| Overall [DIAAS](#gloss-diaas) score | What is the weakest link — the most limiting [EAA](#gloss-eaa) in this food? |
| Ratio > 1.0 for all [EAAs](#gloss-eaa) | [Complete protein](#gloss-complete-protein): no bottleneck, full usability of what you eat |
| Daily protein target | Separate calculation: how many grams of protein do you need total? |

The [DIAAS](#gloss-diaas) table characterizes the quality of each gram. Hitting your daily protein target is about counting how many grams you eat.

### C. Plant protein sources in your pantry {: #appendix-c}
("pantry" here has two meanings: your actual pantry, and the pantry database that is in numa (see the Foods dropdown menu), which is a list of foods in your actual pantry.)

This appendix profiles the plant protein sources currently kept in a typical [NuMa](#gloss-numa) pantry, including nutritional yeast, which is not a plant but is grouped here because it fills the same dietary role. For each source: what form it takes, where it comes from, its essential amino acid ([EAA](#gloss-eaa)) strengths and weaknesses relative to the [FAO](#gloss-fao) reference values described in [Appendix B](#appendix-b), and its typical role in cooking.

The [EAA](#gloss-eaa) notes below describe general tendencies for each food, not a substitute for running the food itself through [NuMa](#gloss-numa). Growing conditions, processing, and the specific [USDA](#gloss-usda) or Open Food Facts[^3] record behind a given entry all shift the exact numbers — use [NuMa](#gloss-numa)'s own amino acid ratio and [DIAAS](#gloss-diaas) output for precise figures. Sourcing and cost information for these foods is addressed separately, not here.

BEFORE GOING ANY FURTHER: You should know that the two most useful foods below (aside from staples like whole wheat flour) are nutritional yeast and hulled hemp seed. Both are incredibly nutritious and useful. Nutritional yeast adds umami to any food, and hulled hemp seed is invaluable when eating legumes.

#### Seeds

**Chia seeds**

- *Form:* tiny oval seeds, black or mottled grey-brown, about 1mm long.
- *Source:* *Salvia hispanica*, a flowering mint-family plant native to Mexico and Guatemala.
- *[EAA](#gloss-eaa) profile:* unusually complete for a plant seed — as worked through in Appendix B, chia clears all nine [EAA](#gloss-eaa) floors, with lysine as its narrowest margin (~1.3× the reference). One of the few standalone-complete plant proteins in this pantry.
- *Culinary role:* primarily a functional/textural addition rather than a bulk protein source — a gelling agent for puddings, an egg replacer in baking (roughly 1 Tbsp ground chia + 3 Tbsp water per egg), and a smoothie thickener.
- *Also worth knowing:* must be ground or soaked until gelled — the intact seed coat lets whole chia pass through largely undigested.

**Ground flax seeds**

- *Form:* fine golden-brown to reddish-brown meal (pre-milled — whole flaxseed is a hard, shiny, oval seed instead).
- *Source:* *Linum usitatissimum*.
- *[EAA](#gloss-eaa) profile:* good, though a step below chia; lysine is typically its narrowest margin. A useful contributor, especially alongside grains.
- *Culinary role:* the same functional role as chia — egg replacer, binder, and fiber/omega-3 booster in baked goods and oatmeal; a meaningful protein contributor only at larger doses.
- *Also worth knowing:* ground flax oxidizes faster than whole flaxseed — keep it refrigerated or frozen, and use it within a few months of grinding.

**Hulled hemp seeds**

- *Form:* small, soft, pale green-to-tan kernels (already shelled).
- *Source:* *Cannabis sativa* (non-psychoactive hemp variety).
- *[EAA](#gloss-eaa) profile:* one of the better-balanced plant proteins here — good in the sulfur amino acids (methionine + cysteine), a category where legumes are typically weak, with lysine as its more [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* a standalone protein/texture addition to smoothies, granola, salads, and oatmeal; its nutty flavor and sulfur-amino-acid strength make it a good complement to legume-heavy meals.
- *Also worth knowing:* eaten raw with no preparation needed — it digests readily as sold.

**Sunflower seed kernels**

- *Form:* small, flattish oval kernels, off-white to pale grey with a green tinge.
- *Source:* *Helianthus annuus*.
- *[EAA](#gloss-eaa) profile:* moderate protein source; methionine is relatively strong while lysine is the more [limiting amino acid](#gloss-limiting-amino-acid) — roughly the mirror image of many legumes, which makes it a reasonable grain/legume complement.
- *Culinary role:* snack, salad topping, and seed butter; a minor protein contributor at typical serving sizes.
- *Also worth knowing:* high fat content gives raw kernels a short shelf life — refrigerate or freeze to prevent rancidity.

#### Grains & Pseudocereals

**Buckwheat, whole grain**

- *Form:* small, hard, three-cornered (pyramid-shaped) brown-green groats.
- *Source:* *Fagopyrum esculentum* — a pseudocereal, not a true grass/cereal despite the name; botanically closer to rhubarb and sorrel.
- *[EAA](#gloss-eaa) profile:* unusually well-balanced for a grain-like food — notably better in lysine than true cereals (wheat, corn, rice), the classic cereal weak point; more often limiting in leucine or the sulfur amino acids instead.
- *Culinary role:* a base ingredient (groats, kasha, buckwheat flour, soba noodles) rather than an addition; naturally gluten-free, which makes it a useful wheat substitute in a plant-based, protein-conscious diet.
- *Also worth knowing:* the hull surrounding the raw groat is inedible and is always removed before sale.

**Oats, whole grain, rolled**

- *Form:* flattened, cream-colored flakes (steamed and rolled whole groats).
- *Source:* *Avena sativa*.
- *[EAA](#gloss-eaa) profile:* among the stronger true cereals for protein quality — higher lysine than wheat or corn, though lysine is typically still the [limiting amino acid](#gloss-limiting-amino-acid); a solid moderate-quality grain protein overall.
- *Culinary role:* a base ingredient — porridge, baked goods, granola — that can carry a meaningful share of daily protein at typical serving sizes, unlike most seeds or nuts used as garnish.
- *Also worth knowing:* often processed in facilities shared with wheat — check labeling if strict gluten-free status matters.

**Cornmeal, whole-grain, yellow**

- *Form:* coarse-to-medium granular yellow meal (ground dried corn kernels, germ and bran retained).
- *Source:* *Zea mays*.
- *[EAA](#gloss-eaa) profile:* the classic maize deficiency pattern — low in both lysine and tryptophan; one of the more amino-acid-limited grains in this pantry, and a strong candidate for legume pairing (the traditional corn-and-beans combination).
- *Culinary role:* a base ingredient — cornbread, polenta, breading — rather than a minor addition.
- *Also worth knowing:* whole-grain (not degermed) cornmeal is more nutrient-dense but has a shorter shelf life than degermed cornmeal, due to the retained germ oil.

**Whole wheat flour, unenriched**

- *Form:* fine tan-brown powder (whole grain milled, bran and germ retained).
- *Source:* *Triticum aestivum*.
- *[EAA](#gloss-eaa) profile:* lysine is severely limiting — wheat protein (gluten) is notably poor in lysine, the sharpest deficiency among the grains in this pantry; threonine is often a secondary [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* a base ingredient for baked goods, and a major contributor to daily protein for anyone eating bread-based meals regularly — its lysine gap matters more in practice than seeds used only as garnish.
- *Also worth knowing:* "unenriched" means it lacks the iron/B-vitamin fortification added to most commercial white flour — a micronutrient note, not an amino acid one.

#### Tree Nuts & Peanuts

**Almond flour**

- *Form:* fine off-white powder (blanched almonds, ground).
- *Source:* *Prunus dulcis*.
- *[EAA](#gloss-eaa) profile:* relatively low overall protein density among nuts; lysine is the more [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* a base flour substitute in gluten-free/low-carb baking rather than a protein-boosting addition — its protein contribution is secondary to its role as a wheat-flour replacement.
- *Also worth knowing:* high fat content means a shorter shelf life than wheat flour — refrigerate or freeze.

**Cashew nuts**

- *Form:* kidney-shaped, ivory-white nuts.
- *Source:* *Anacardium occidentale* (the seed attached to the cashew apple).
- *[EAA](#gloss-eaa) profile:* comparatively favorable lysine for a tree nut, but generally low in the sulfur amino acids (methionine, cysteine) — a common tree-nut weakness.
- *Culinary role:* snack, cashew cream/cheese base, stir-fry addition; a significant contributor when used as a cream or sauce base in quantity, minor as a garnish.
- *Also worth knowing:* raw cashews are commonly soaked before blending into cream or cheese to soften texture — this is purely textural, not required for digestibility.

**Pecans**

- *Form:* smooth, elongated, ridged, brown-shelled halves.
- *Source:* *Carya illinoinensis*.
- *[EAA](#gloss-eaa) profile:* low overall protein density; lysine and the sulfur amino acids are both comparatively limited — pecans are more valuable here for fat and mineral content than as a protein source.
- *Culinary role:* garnish or mix-in (baked goods, salads); a minor protein contributor at typical serving sizes.
- *Also worth knowing:* high polyunsaturated fat content makes pecans prone to rancidity — store refrigerated or frozen.

**Walnuts, English**

- *Form:* wrinkled, brain-like lobed, brown-shelled halves.
- *Source:* *Juglans regia*.
- *[EAA](#gloss-eaa) profile:* a similar pattern to pecans — lysine limiting, modest sulfur amino acid content — notable mainly for omega-3 (ALA) content rather than protein quality.
- *Culinary role:* garnish or mix-in; a minor protein contributor.
- *Also worth knowing:* also prone to rancidity — refrigerate or freeze for storage.

**Brazil nuts**

- *Form:* large, dense, hard, off-white kernels with a rough triangular cross-section.
- *Source:* *Bertholletia excelsa*, native to the Amazon rainforest.
- *[EAA](#gloss-eaa) profile:* the exception among tree nuts — unusually rich in the sulfur amino acids (methionine and cysteine), the opposite weakness pattern from most nuts; lysine remains their more [limiting amino acid](#gloss-limiting-amino-acid).
- *Culinary role:* snack, or a minor addition to trail mixes and baked goods — valuable precisely because it complements legume-heavy meals that tend to be sulfur-amino-acid-poor.
- *Also worth knowing:* the most concentrated food source of selenium known — a commonly cited ceiling is 1-2 nuts a day; eating many daily risks selenium toxicity, a separate issue from protein content worth tracking alongside it.

**Peanuts**

- *Form:* oblong, tan-shelled kernels (botanically a legume, not a true nut).
- *Source:* *Arachis hypogaea*.
- *[EAA](#gloss-eaa) profile:* better lysine than true tree nuts, consistent with its legume biology, but methionine and cysteine are its more [limiting amino acids](#gloss-limiting-amino-acid) — the classic legume weak point.
- *Culinary role:* snack, peanut butter, sauces; a substantial protein contributor at typical serving sizes, comparable to some legumes.
- *Also worth knowing:* raw peanuts are susceptible to aflatoxin-producing mold in storage — buy from a source with good turnover and store cool and dry. This is a food-safety note, not an amino acid one.

#### Soy-Based Foods

**Tofu, firm**

- *Form:* a solid, off-white curd block, custard-to-firm texture depending on how it was pressed.
- *Source:* coagulated soy milk (*Glycine max*), pressed to remove whey.
- *[EAA](#gloss-eaa) profile:* among the most complete plant proteins available — soy protein clears nearly every [EAA](#gloss-eaa) floor, with methionine/cysteine typically its only mildly [limiting amino acid](#gloss-limiting-amino-acid).
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
- *[EAA](#gloss-eaa) profile:* one of the highest-quality plant proteins available, with high digestibility (~0.95, as noted under "SPI" in the Glossary) — it clears essentially every [EAA](#gloss-eaa) floor, with methionine/cysteine still its narrowest margin.
- *Culinary role:* a concentrated protein-boosting addition — smoothies, baked goods, meat analogs — rarely eaten as a standalone dish, but very effective at raising a meal's complete-protein grams without much bulk or flavor change.
- *Also worth knowing:* as a concentrate rather than a whole food, it also strips out the fiber, [phytonutrients](#gloss-phytonutrients), and micronutrients present in whole soy — best treated as a protein-density tool, not a whole-food replacement for tofu or edamame.

#### Other Protein Concentrates

**Unsweetened pea protein powder**

- *Form:* a fine, off-white to pale yellow powder.
- *Source:* yellow split peas (*Pisum sativum*), protein-extracted and concentrated.
- *[EAA](#gloss-eaa) profile:* notably good lysine content — peas are a classic lysine-rich legume — but methionine/cysteine are clearly limiting, the reason pea protein is so often blended commercially with rice protein, which has the opposite pattern.
- *Culinary role:* a concentrated protein-boosting addition, the same role as soy protein isolate — smoothies, baking, general protein boosting — and it is a particularly effective complement to a grain-based meal (cereal, rice, wheat) that is itself lysine-poor but has adequate sulfur amino acids.
- *Also worth knowing:* the single best complement in this pantry for grain-heavy meals (bread, oats, cornbread), specifically because its strength (lysine) matches their specific weakness.

**Vital wheat gluten**

- *Form:* a fine, tan powder — nearly pure wheat protein with the starch washed out.
- *Source:* wheat flour (*Triticum aestivum*), processed to isolate the gluten protein fraction.
- *[EAA](#gloss-eaa) profile:* the most lysine-poor protein in this entire pantry — gluten is almost devoid of lysine, and concentrating the protein by removing the starch does not fix this; it simply delivers more of the same imbalanced amino acid pattern per gram.
- *Culinary role:* as much a structural/textural ingredient (seitan base, bread dough strengthener) as a protein source — it is often eaten as a primary "meat analog" ingredient (seitan) despite its poor amino acid balance, so it especially needs deliberate complementing with a lysine-rich food (legumes, pea protein) in the same meal or day.
- *Also worth knowing:* because seitan dishes are sometimes treated as a standalone "meat" replacement, this is the food in the pantry most likely to create an unnoticed lysine gap if eaten alone in quantity.

#### Nutritional Yeast

**Nutritional yeast flakes**

- *Form:* yellow flakes of deactivated, dried yeast. Flakes are less dense than powder, so measure by weight rather than volume when precision matters — a point already flagged in this pantry's notes for this item.
- *Source:* *Saccharomyces cerevisiae*, grown on a sugar-based medium, then deactivated (killed) and dried. Deactivation means it will not leaven anything or grow in the gut, unlike active baker's or brewer's yeast.
- *[EAA](#gloss-eaa) profile:* a good-quality, fairly [complete protein](#gloss-complete-protein) for a non-legume source, generally decent across the [EAAs](#gloss-eaa); the sulfur amino acids (methionine especially) tend to be its relative weak point, similar to soy and legumes generally.
- *Culinary role:* usually an addition rather than a primary ingredient — its concentrated umami (glutamate-driven) flavor makes it a savory, cheese-like flavoring for popcorn, pasta, sauces, and roasted vegetables, and it thickens liquids when whisked into a roux-based sauce (as in "nooch" cheese sauce). It can also become a primary ingredient in dishes built around it, such as cashew-and-nutritional-yeast "yeast cheese," where it supplies both flavor and a meaningful protein contribution.
- *Also worth knowing:* most commercial brands are fortified with B12 (and sometimes other B vitamins) — worth checking the label, since this is often the primary reason vegans include it in their diet, independent of its protein content.

### D. Glycemic load (GL) and Blood Glucose Comparison {: #appendix-d}
Glycemic load is a useful approximation, but no single formula-derived figure reliably predicts an individual's blood glucose response to a mixed meal. Three reasons account for this:

- The fat and protein suppression effect varies by person, by degree of insulin resistance, and by the specific foods involved.
- [GI](#gloss-gi) values were measured in healthy subjects and may not translate directly to someone with diabetes or insulin resistance.
- Individual glucose responses to identical meals vary substantially, even in the same person on different days.

[GL](#gloss-gl) is therefore most reliable when comparing meals of broadly similar composition — two different grain-based breakfasts, for example. When meals differ significantly in fat or protein content, the calculated [GL](#gloss-gl) will understate the difference in actual glycemic impact.

#### Continuous Glucose Monitoring

The practical gold standard today is continuous glucose monitoring ([CGM](#gloss-cgm)) — devices such as the Dexterity G7 or Libre 3 that measure interstitial glucose every few minutes. A person with diabetes can eat a meal, watch their glucose curve in the accompanying app, and directly compare their own real response across different meal choices over time. No formula approaches this for accuracy in individual prediction.

#### Predictive Apps

Some applications (January AI, Levels) go a step further, using machine learning models trained on large [CGM](#gloss-cgm) datasets to predict glucose response to a described meal before it is eaten — effectively personalising the [GI](#gloss-gi) and [GL](#gloss-gl) concepts. These predictions are probabilistic rather than exact, but they represent the closest available alternative to direct measurement.

#### Clinical Practice Without CGM

For clinical guidance without [CGM](#gloss-cgm), dietitians working with people with diabetes typically use carbohydrate counting combined with qualitative judgment about fat and protein content, rather than relying on [GL](#gloss-gl) as a single summary figure. [GL](#gloss-gl) remains a reasonable guide for comparing meals similar in structure, but should not be the deciding number when fat and protein differ significantly between the options being considered.

### E. FAO 2013 Amino Acid Reference Values

Under development.

[//]: # "develop section"

### F. Full Nutrient Key

Under development.

[//]: # "develop section"

### G. Protein ingestion timing

Under development.

[//]: # "develop section"

Resources:

* https://runningmagazine.ca/health-nutrition/could-you-be-timing-your-protein-all-wrong/

### H. Meal timing

Under development.

[//]: # "develop section"

Resources:

* https://www.theguardian.com/commentisfree/2026/may/05/game-changer-good-health-scientists-we-are-when-we-eat - article by expert

### I. Why some foods appear only in DIAAS-boosting suggestions {: #comp-appendix}
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

### J. Portion Input Formats {: #portion-formats}
Every prompt that asks for a portion amount — in Foods, Recipes, Meals, and the Convert tool — accepts the same input formats.

NUMBERS

Plain decimals, fractions, and mixed numbers are all accepted:

    150        plain number
    0.5        decimal
    1/4        fraction
    1 1/2      mixed number (whole + fraction, separated by a space)

WEIGHT UNITS

    g  gr  gram  grams          grams  (1 g = 1 g)
    oz  ounce  ounces           ounces  (1 oz = 28.35 g)
    lb  lbs  pound  pounds      pounds  (1 lb = 453.6 g)
    kg  kilogram  kilograms     kilograms  (1 kg = 1000 g)

VOLUME UNITS

NuMa converts volume to grams via the food's recorded density. If density is unknown for a food, it asks you to supply the weight manually. Common dried herbs and spices (pepper flakes, cinnamon, cumin, oregano, garlic powder, and dozens more) have built-in density estimates, since these are almost always measured by the teaspoon or tablespoon rather than weighed — including a generic fallback for any USDA "Spices, ..." entry not individually itemized.

    c  cup  cups                cups  (1 c = 236.6 ml)
    T  tbsp  tablespoon  tablespoons    tablespoons  (1 T = 14.8 ml)
    t  tsp  teaspoon  teaspoons     teaspoons  (1 t = 4.9 ml)
    ml  milliliter  milliliters  cc   milliliters
    floz                         fluid ounces  (1 floz = 29.6 ml)
    l  liter  liters             liters  (1 l = 1000 ml)

Note: T (uppercase) means tablespoon; t (lowercase) means teaspoon. These two are case-sensitive. All other units are case-insensitive.

PIECE / COUNT UNITS

    pc  pcs  piece  pieces  each  ea  count  ct  item  items

Piece entries record a count but no gram weight. The program will ask you to confirm or supply a weight if it needs one for nutrient scaling. Unlike weight and volume units, piece units require a space: "2 pc", not "2pc".

[USDA](#gloss-usda) STANDARD PORTIONS

Many [USDA](#gloss-usda) foods include pre-defined portion sizes (e.g. "1 medium egg", "1 cup sliced"). These are listed at the portion prompt and can be selected by number:

    p1         select USDA portion #1
    p2         select USDA portion #2
    1.5 p1     one-and-a-half times USDA portion #1

**`p1`, `p2`, … mean "the food's 1st portion, 2nd portion, …" — position in the list, never the portion's own text.** This trips people up specifically when you add a custom portion (via [Food Cache](#food-cache-web) → **Portions**) and happen to *name* it something like `p1`: that name has no effect on its shortcut number. If it's the fourth portion in the list, its shortcut is `p4`, no matter what you called it. Every screen where you type a `pN` shortcut — Foods, Recipes, Meals — also lists that food's full portion set with the real shortcut number next to each one; check that list before typing `pN`, don't guess from a portion's name. Adding, removing, or reordering portions on a food also renumbers every `pN` that follows the changed spot, so re-check the list after any portion edit, too — see [A food's portion "pN" shortcut points to the wrong portion](#ts-portion-numbering) if a `pN` amount doesn't come out the way you expected.

OMITTING THE SPACE

For all weight and volume units, the space between the number and unit is optional. These pairs are identical:

    2 T    =   2T
    0.25 c =   0.25c
    150 g  =   150g
    3 oz   =   3oz
    1/4 c  =   1/4c

(Piece units — pc, each, etc. — always require a space.)

VOLUME WITH EXPLICIT WEIGHT

When you know both the volume measure and the exact gram weight, you can supply both on one line. NuMa records the weight and labels the entry with the volume for readability:

    2 T 30g         →  30 g  (labeled "30 g (2 T)")
    1/4 c 60 g      →  60 g  (labeled "60 g (1/4 c)")

BARE NUMBER

A bare number with no unit is assumed to be grams; each amount field's example text says so directly.

### K. Worked validation example — meal-level DIAAS for pinto beans + quinoa {: #appendix-k}
This appendix lets you verify [NuMa](#gloss-numa)'s protein quality calculation independently. Every step is shown explicitly so you can reproduce it in a spreadsheet or calculator, then compare your result with what [NuMa](#gloss-numa) produces when you enter these two foods as a meal.

#### The two foods

| Food | [FDC ID](#gloss-fdc-id) | Data type | [USDA](#gloss-usda) source |
|------|--------|-----------|-------------|
| Beans, pinto, mature seeds, cooked, boiled, with salt | 173796 | SR Legacy | https://fdc.nal.usda.gov/food-details/173796/nutrients |
| Quinoa, cooked | 168917 | SR Legacy | https://fdc.nal.usda.gov/food-details/168917/nutrients |

All nutrient values below are drawn directly from those pages as of June 2026. The demo uses **100 g of each food** — round numbers that make the arithmetic easy to follow.

---

#### Step 1 — Individual nutrient profiles (per 100 g, from USDA)

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

#### Step 2 — Pooled nutrients for the meal (100 g pinto + 100 g quinoa = 200 g total)

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

**Table I-4. Pooled IAA totals for the meal (g)**

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

#### Step 3 — Applying digestibility to get digestible IAA amounts

Raw amino acid values from [USDA](#gloss-usda) are not all absorbed. The [DIAAS](#gloss-diaas) methodology requires multiplying each food's IAA amounts by that food's *true [ileal digestibility](#gloss-ileal-digestibility) coefficient* — a value between 0 and 1 representing the fraction of each IAA that actually reaches the bloodstream.

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

#### Step 4 — The FAO reference amounts for this meal

The [DIAAS](#gloss-diaas) method scores each pooled digestible IAA against how much of that IAA a *reference protein* of equal weight would provide. The reference values, from [FAO](#gloss-fao) Food and Nutrition Paper 92 (2013), Table 6, are expressed in **mg of IAA per gram of total protein** for older children, adolescents, and adults.

The full table is in Appendix E of this manual. The relevant values are:

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

#### Step 5 — IAA ratios and the composite DIAAS score

For each IAA, divide the pooled digestible amount (from Table I-5) by the reference amount (from Table I-6). The result is a ratio: a value ≥ 1.0 means the meal meets or exceeds the reference for that IAA; below 1.0 means it falls short.

    Ratio = pooled digestible IAA (g) ÷ FAO reference IAA (g)

**Table I-7. IAA ratios vs. [FAO](#gloss-fao) reference**

| IAA | Pooled dig. (g) | Reference (g) | Ratio | Meets reference? |
|-----|----------------:|--------------:|------:|:----------------:|
| Histidine | 0.29355 | 0.21456 | 1.368 | Yes |
| Isoleucine | 0.42785 | 0.40230 | 1.063 | Yes |
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

but this can overstate what the body actually absorbs. DIAAS is the *limiting-IAA* ratio, not an average — and here the limiting IAA (leucine) happens to be relatively better-supplied by quinoa, the more digestible of the two foods (0.85 vs. pinto beans' 0.80). Multiplying the *whole* protein pool by that single ratio can produce a DCP higher than the protein that was ever actually digested. [NuMa](#gloss-numa) guards against this by also capping DCP at the meal's digestibility-weighted protein — the sum of each food's protein × its own digestibility coefficient:

    aa_dig_protein_g = (9.01 g × 0.80) + (4.40 g × 0.85) = 7.208 + 3.740 = 10.948 g

    DCP = min(13.41 g × 0.921, 10.948 g) = min(12.35 g, 10.948 g) = 10.948 g

(The DIAAS-based figure is also separately capped at 1.0 when DIAAS exceeds 1.0, since digestible complete protein can never exceed total protein either way.)

---

#### Step 6 — Interpreting the result

A composite [DIAAS](#gloss-diaas) ≥ 1.0 means the meal's protein is fully complete relative to the [FAO](#gloss-fao) reference. Values below 1.0 indicate partial completeness — the lower the value, the more the [limiting amino acid](#gloss-limiting-amino-acid) constrains usable protein.

For this meal:

- **Leucine** is the limiting IAA at 0.921. This is not surprising: leucine is the most abundant IAA in animal proteins, but plant proteins generally provide less of it relative to total protein.
- **Valine** is also below reference at 0.942. The combination of one legume and one pseudo-cereal improves but does not fully resolve either gap.
- **Lysine**, which is the classic weak point of grains, is met here (1.025) — the pinto beans contribute the lysine that quinoa alone would not cover.
- **[Met+Cys](#gloss-met-cys)** is nearly exactly met at 0.998 — essentially at the reference.

The [DCP](#gloss-dcp) of 10.948 g from 13.41 g of raw protein means that roughly 2.46 g of protein per meal is rendered non-contributory — most of that from the digestibility gap between the two foods, with the leucine shortfall further capping the naive DIAAS-only estimate. In practical terms, this is still a high-quality plant-protein meal — [DIAAS](#gloss-diaas) above 0.9 is considered "good quality" by the [FAO](#gloss-fao).

---

#### Step 7 — Reproduce this in NuMa and compare

To run the same analysis in [NuMa](#gloss-numa):

1. From the main menu, select **Meals & Log**.
2. Create a new meal and add two foods:
   - Search for **pinto beans cooked** → select [FDC](#gloss-fdc) 173796
     ("Beans, pinto, mature seeds, cooked, boiled, with salt")
   - Enter a portion of **100 g**
   - Add a second food: search for **quinoa cooked** → select [FDC](#gloss-fdc) 168917
     ("Quinoa, cooked")
   - Enter a portion of **100 g**
3. Save the meal, then open it and select **View nutrition analysis**.
4. In the analysis screen, scroll to the **Protein quality** section.

[NuMa](#gloss-numa) will display:
- Total protein
- Composite [DIAAS](#gloss-diaas) score
- Digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp))
- A per-IAA ratio table identifying the [limiting amino acid](#gloss-limiting-amino-acid)

Compare the values [NuMa](#gloss-numa) shows with those in Table I-7 above. They should match to at least three significant figures. If they do not, please report the discrepancy at the project issue tracker.

---

#### Step 8 — Bonus: validating a protein-complement suggestion (quinoa + black beans)

The steps above validate [DIAAS](#gloss-diaas)/[DCP](#gloss-dcp) for a fixed, user-chosen pair of foods. This bonus section validates the *other* half of NuMa's protein-quality math — how it decides which complement food to suggest, and how much of it — using the same quinoa (FDC 168917) from Step 1 as the starting point. See [Protein Complement Suggestions](#comp) in Part 4.B for the plain-language version of this logic.

**Quinoa alone has two amino acid gaps.** Using quinoa's own digestibility coefficient (0.85, Mathai et al. 2017 — same source as Step 3) and the Table I-2 amino acid values, quinoa's digestibility-adjusted scores are:

| IAA | Adjusted score | Gap? (< 0.95) |
|-----|---------------:|:--------------:|
| Histidine | 1.533 | No |
| Isoleucine | 1.011 | No |
| **Leucine** | **0.827** | **Yes — primary (lowest)** |
| Lysine | 0.962 | No |
| [Met+Cys](#gloss-met-cys) | 1.336 | No |
| [Phe+Tyr](#gloss-phe-tyr) | 1.263 | No |
| Threonine | 1.012 | No |
| Tryptophan | 1.522 | No |
| **Valine** | **0.894** | **Yes — secondary** |

(These scores use quinoa's own [DIAAS](#gloss-diaas)-context digestibility, 0.85 — a single food is scored at its own digestibility, unlike the pinto+quinoa *meal* used in Steps 1–7, where digestibility is applied after pooling. See [Protein Completeness](#complete).)

**The candidate: Black beans, cooked** — one of the 25 entries in NuMa's curated complement table[^10] (not itself in the user's pantry or cache). Per 100 g: 8.86 g protein, 0.677 g leucine, 0.452 g valine, true ileal digestibility 0.80 (FAO FNP 92, 2013 — distinct from its [DIAAS](#gloss-diaas) of 0.75; see Step 3 above for why these are different numbers).

**The gap-closer formula.** NuMa solves for the grams `X` of the candidate needed so the *combined* pool's target-AA-to-protein ratio reaches the [FAO](#gloss-fao) reference, using the base food's own digestibility as the conversion factor:

    alpha = candidate's target AA (g) per g of food       = 0.677 / 100   = 0.00677
    beta  = candidate's protein (g) per g of food          = 8.86  / 100   = 0.0886
    R     = FAO reference (g AA / g protein), inflated
            for the base food's digestibility                = (61.0 / 1000) / 0.85 = 0.071765
    X     = (R × base_protein − base_target_AA) / (alpha − R × beta)
          = (0.071765 × 4.40 − 0.261) / (0.00677 − 0.071765 × 0.0886)
          = 0.054765 / 0.0004119
          ≈ 132.96 g   →  NuMa displays **133 g** (rounded)

**Checking the result.** Adding 133 g of black beans to the 100 g of quinoa gives a combined pool of 16.18 g protein. Recomputing every IAA ratio against this new pool (same method as Table I-7) shows both original gaps closed — and, as a side effect neither targeted directly, every other IAA stays comfortably clear too:

| IAA | New adjusted score | Gap? |
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

This confirms NuMa's Tier 1 result exactly: `gaps_closed: 2`, `new_complete: True`, `closes_primary: True` — a single food closed both gaps, so no Tier 3 two-food cascade (Part 4.D) was needed here.

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

The scale factor is capped at 1.0 because a food can never be "more than 100% complete" for DCP purposes — once the combination's weakest amino acid clears the reference, NuMa credits the *entire* combined raw protein pool as digestible and complete. This is a looser approximation than the exact pooled calculation in Steps 1–7 (which applies each food's own digestibility to each amino acid individually, then takes the true minimum ratio) — `numa_app/services/complements.py` documents this trade-off explicitly, noting it can differ from the exact figure by 15–20 g on a real meal. It is used here only because a plain food page has nothing more granular to pool from; meal, recipe, and daily-summary contexts (which do have a real ingredient list) use the exact method instead.

**Reproduce this in NuMa:** open a food page for quinoa, cooked ([FDC](#gloss-fdc) 168917), and look at its [Protein Complement Suggestions](#comp) section. Black beans, cooked should appear in the "General" tier at 133 g, showing "Leucine: 0.83→1.00" and "Valine: 0.89→1.03" under Effect, "Adds: 8.8 g digestible protein (from 11.8 g raw protein in this addition)", and "Total digestible complete protein: 16.2 g" — matching every figure derived above.

---


## Notes

[^1]: Lippman, D., Stump, M., Veazey, E., Guimarães, S. T., Rosenfeld, R., Kelly, J. H., Ornish, D., & Katz, D. L. (2024). Foundations of Lifestyle Medicine and its Evolution. *Mayo Clinic Proceedings: Innovations, Quality & Outcomes, 8(1)*, 97–111. https://doi.org/10.1016/j.mayocpiqo.2023.11.004

[^2]: U.S. Department of Agriculture, Agricultural Research Service. (2019). *FoodData Central*. https://fdc.nal.usda.gov/

[^3]: Open Food Facts contributors. (2012). *Open Food Facts*. https://world.openfoodfacts.org/

[^4]: Institute of Medicine (US) Panel on Micronutrients. (2001). *Dietary Reference Intakes for Vitamin A, Vitamin K, Arsenic, Boron, Chromium, Copper, Iodine, Iron, Manganese, Molybdenum, Nickel, Silicon, Vanadium, and Zinc*. National Academies Press. https://doi.org/10.17226/10026 — the underlying Dietary Reference Intake report establishing that non-heme iron and phytate-inhibited zinc from plant foods are absorbed less efficiently than from mixed/omnivorous diets; the basis for the NIH fact-sheet figures below.

[^5]: National Institutes of Health, Office of Dietary Supplements. *Iron: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/ — states that because vegetarian diets contain no heme iron and their non-heme iron is less bioavailable, "the RDA for vegetarians is 1.8 times higher than for people who eat meat."

[^6]: National Institutes of Health, Office of Dietary Supplements. *Zinc: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/ — states that "the zinc requirements for vegetarians may be as much as 50% higher than for those who eat meat" because of the reduced bioavailability of zinc from plant-based diets.

[^7]: National Institutes of Health, Office of Dietary Supplements. *Vitamin B12: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/ — vitamin B12 occurs naturally only in animal foods. See also Melina, V., Craig, W., & Levin, S. (2016). Position of the Academy of Nutrition and Dietetics: Vegetarian Diets. *Journal of the Academy of Nutrition and Dietetics, 116*(12), 1970–1980. https://doi.org/10.1016/j.jand.2016.09.025 — recommends that vegans obtain vitamin B12 routinely from fortified foods or a supplement, since no reliable unfortified plant source exists. Neither source specifies a "50% of RDA" cutoff for a single day's intake; that trigger is NuMa's own design choice (see main text).

[^8]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2008," *Diabetes Care* 31(12):2281–3. This is a Creative Commons–licensed table, and NuMa uses it to fill in glycemic index values for common foods automatically. (For technically skilled users: this is done by a helper program, `import_gi_seed.py`, included in NuMa's program folder. It only fills in a value when a food's name matches the table exactly; anything less certain is left for you to confirm by hand.)

[^9]: US National Institutes of Health. (2026, July 31). Office of Dietary Supplements—Nutrient Recommendations and Databases. https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

[^10]: NuMa's own curated table of amino-acid profiles for common protein-complement foods — beans, grains, seeds, and a few animal foods included for comparison (`_COMPLEMENT_TABLE` in `usda_nutrients.py`). 23 of the 25 entries cite a specific [USDA](#gloss-usda) FoodData Central SR Legacy record by FDC ID, sourced the same way as the rest of NuMa's nutrient data[^2]; the remaining two (nutritional yeast, pea protein powder) use published amino-acid-composition literature values because no matching USDA record exists for those specific products. NuMa always checks your own food cache for a real match to each entry's food name before falling back to these built-in figures — see [amino acid estimates in complement suggestions](#comp-estimate).

[^11]: Harvard T.H. Chan School of Public Health, Renal and Urology News Oxalate Table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine. https://hsph.harvard.edu/wp-content/uploads/2024/07/OXALATE-TABLE-1.xlsx — NuMa matches foods to this table by name; see [Oxalate data](#oxalate) for enabling it, matching, and limitations.

[^12]: Holick, M. F., Binkley, N. C., Bischoff-Ferrari, H. A., Gordon, C. M., Hanley, D. A., Heaney, R. P., Murad, M. H., & Weaver, C. M. (2011). Evaluation, Treatment, and Prevention of Vitamin D Deficiency: an Endocrine Society Clinical Practice Guideline. *Journal of Clinical Endocrinology & Metabolism, 96*(7), 1911–1930. https://doi.org/10.1210/jc.2011-0385 — recommends adults at risk of deficiency take 1500–2000 IU/day (37.5–50 mcg) of vitamin D to reliably maintain a blood level above 30 ng/mL, well above the 15–20 mcg RDA. NuMa's built-in Revised Optimal default (50 mcg) sits at the top of that range.

[^13]: Kris-Etherton, P. M., Innis, S., American Dietetic Association, & Dietitians of Canada. (2007). Position of the American Dietetic Association and Dietitians of Canada: Dietary Fatty Acids. *Journal of the American Dietetic Association, 107*(9), 1599–1611. https://doi.org/10.1016/j.jada.2007.07.024 — summarizes multiple expert-body recommendations (including ISSFAL's) converging on roughly 500 mg/day combined EPA+DHA for general cardiovascular health in adults without existing heart disease, well above what a typical omega-3-ALA-only diet provides. NuMa's built-in Revised Optimal defaults (250 mg EPA + 250 mg DHA) split that combined figure evenly.

[^14]: Young, V. R., & Pellett, P. L. (1994). Plant proteins in relation to human protein and amino acid nutrition. *American Journal of Clinical Nutrition, 59*(5, Suppl.), 1203S–1212S. — the basis for the modern consensus that complementary protein sources don't need to be eaten at the same meal, since the body's own daily protein turnover (roughly 250–300 g) can supply amino acids the free pool is short on.

[^15]: Arentson-Lantz, E. J., Von Ruff, Z., Connolly, G., Albano, F., Kilroe, S. P., Wacher, A., Campbell, W. W., & Paddon-Jones, D. (2024). Meals containing equivalent total protein from foods providing complete, complementary, or incomplete essential amino acid profiles do not differentially affect 24-h skeletal muscle protein synthesis in healthy, middle-aged women. *The Journal of Nutrition*. Advance online publication. — a controlled feeding study finding no significant difference in acute or 24-hour muscle protein synthesis across complete, complementary, and single incomplete-protein meal conditions.

