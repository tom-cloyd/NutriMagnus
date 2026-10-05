# NutriMagnus User Manual

*Updated 2026-10-05:0704* / Reading time: 7 hours, 17 minutes

*Last full audit: 2026-09-13* / [Disclaimer](/disclaimer)

<!-- t:26-10-02:0741 Today I will start marking sections I have reviewed/edited with HTML comment of this sort. I have previously reviewed many sections, but not marked them, but I need to know which sections have not yet been reviewed so this is how I'll keep records. A section no so marked may be one of those previously reviewed, but it will take me a while to catch up with such sections, and I may not recall them all anyway. I may or may not append a comment to the basic flag comment, the first of which may be seen below. -->

<!-- t:26-10-02 -->

**NutriMagnus ("NuMa")** is a computer program with publicly available code which provides a thorough nutritional analysis of a user's food choices. NuMa has special resources for tracking and analysis of protein because this is a problem for those eating primarily a plant-based diet, for older people, and for the chronically-ill:

* **Vegetarians and vegans** must deal with protein that has digestibility issues and amino acid completeness problems. 
* **Older people** are impacted by multiple factors reducing the chances of their being well nourished, including a much-reduced ability to make use of protein. 
* The **chronically-ill**, as well as **older people**, also have typically reduced appetites. 

People in these groups rarely have an accurate sense of the nutritional adequacy of their diet. The information is obscure, technically dense, and when it's on commercial packaging is both inadequate and misleading.

**Eating usually involves making choices, and good choice requires good information.** The three major problems impeding good food choice are a) lack of awareness of the choices available, and b) lack of information about the nutritional character of those choices, and c) lack of information as to what constitutes a good choice. All of these problems are addressed by NuMa, in detail.

**Eating is fundamentally about survival - the first priority for all life.** Most of the cells in our body persist for a shorter period than we do. During their lifespan they do their work using materials available to them in their immediate environment. Eventually they must be replaced by new cells, constructed again from such available materials.

**Essential materials needed for cellular support and replacement come from what we eat.** While significant essential materials may already exist in the local environment of a cell, ultimately all materials come from outside our bodies, through eating.

**Both the program and its accompanying *User Manual* are in continuing active development.** They are modified frequently. Both are already quite sophisticated, but new versions will be made available quickly for those already using the program. However, the manual has not yet received a careful editorial review of all its parts. It is an advanced first draft.

**User feedback is highly valued, so please give us yours!** With computer programs in active development ANY feedback is appreciated and most likely useful. User experience with the program is a critical measure of program success or failure. So, please email all problems, thoughts, and ideas to [tomcloydmsma@gmail.com](mailto:tomcloydmsma@gmail.com). Put `NutriMagnus` or `NuMa` in the subject line, please!

**What to offer as "feedback":** First, ANY thoughts you wish to share are welcome. If in doubt, just do it! We'll be grateful. Of particular interest to us are these topics:

1. Inconveniences: you notice that something seems a bit difficult to do, or you see a simpler or quicker way to do it.
2. Missing or incomplete information: Sometimes updates and changes do not go out to every part of the program as they should, and you see a gap in the information provided.
3. Outright nonsense: you look at program output and think "that can't be right" or maybe you just feel doubtful about it.

User-derived issues get immediate priority in the program-development process!

---

## How to read this Manual <!-- t:26-10-02 -->

NuMa runs as a web app, opened in your ordinary browser — there is nothing to install and no command line involved.

- Read **Part 1** (To get a quick start) for a fast orientation before diving in.
- Read **Part 2** (Introduction) for the ideas behind the program.
- Read **Part 3 — Using the Web App** for how to actually operate NuMa.
- Read **Part 4** (Core nutrition concepts) for more of the ideas behind the program.
- Read **Part 5** (Reading Your Results) whenever you want to know what a column or table means.
- Read **Part 6** (Shared Operations) for behaviors that show up in more than one place in the app, explained once.
- Parts 7 to 10 apply to everyone.
- Trying to find something in this document itself, not in the app? See [Using this manual's search](#search-howto) — it works differently from a plain text search.

## Part 1 — To get a quick start <!-- t:26-10-04 -->

*(Reading time: 16 minutes)*

### A. Download and install the program <!-- t:26-10-03 -->

NuMa runs on Windows and on Linux. Find your own system below and ignore the other — the two are installed quite differently. Whichever you're on, read [What kind of program this is](#install-webapp-note) at the end; it explains something about NuMa that surprises nearly everyone at first.

#### Windows {: #install-windows}

NuMa has no installer. It's a single program file that you keep wherever you like and just run.

a. **Download it.** Click this link: <https://github.com/tom-cloyd/NutriMagnus/releases/latest/download/nutrimagnus.exe>. It always gives you the newest version.

b. **Put it somewhere permanent.** In File Explorer, make a new folder in **Documents** called **NutriMagnus**, and move `nutrimagnus.exe` into it from your Downloads folder. Leave it in Downloads and it may get cleaned out later.

c. **Get past Windows' two warnings.** Your browser will probably block the download: in **Edge**, click the **...** beside it and choose **Keep**, then **Show more** → **Keep anyway**; in **Chrome**, click the **^** beside it and choose **Keep**, then **Keep anyway**. Then, the first time you run the program, a blue box says **"Windows protected your PC"** — click **More info**, then **Run anyway**. Once you allow it, it won't ask again about that copy of the program.

   Both warnings mean "Windows doesn't recognize who published this," not "this file is dangerous." Unsigned programs — which means anything whose author hasn't paid a certificate authority an annual fee — always get them. Your antivirus may quarantine the file for the same reason; if it does, allow it through.

d. **Run it.** Double-click `nutrimagnus.exe`. A black window full of text opens — that *is* NuMa running, so leave it alone. A few seconds later your browser opens a tab with NuMa in it, and that tab is what you use. (The first launch can take up to a minute while Windows scans the file.) If no tab opens, go to **http://127.0.0.1:8000** yourself.

e. **Make it easy to start next time.** Right-click `nutrimagnus.exe` and choose **Pin to Start**. For a desktop icon instead: right-click → **Show more options** → **Send to** → **Desktop (create shortcut)**.

f. **Quit it properly.** Close the browser tab *and* the black window. Closing only the tab leaves NuMa running in the background.

g. **Updating it later.**{: #update-windows} Windows won't let a running program replace itself, so updating NuMa means swapping the program file yourself. There are five steps:

   1. **Download the new version.** When one is available, an **UPDATE AVAILABLE** message appears at the top of NuMa's home page. Click its **Download NutriMagnus** button. (If you dismissed that message, or don't want to wait for it, the link in item 'a' above always downloads the newest version.) The new `nutrimagnus.exe` goes to your **Downloads** folder. If your browser warns you about it, choose **Keep**, then **Keep anyway**, as in item c.
   2. **Quit NuMa.** Close NuMa's black window; that's what actually stops the program. You can leave this manual open in its tab, so you can keep following these steps.
   3. **Replace the old program file.** In File Explorer, move the new `nutrimagnus.exe` from Downloads into your NutriMagnus folder. The UPDATE AVAILABLE message shows you exactly which folder that is. When Windows asks, choose **Replace the file in the destination**. If Windows instead says the file is in use, NuMa is still running: go back to step 2.
   4. **Start NuMa again** the way you usually do. Your Start-menu pin or desktop shortcut still works. If the blue "Windows protected your PC" box appears, which a new version can trigger, click **More info**, then **Run anyway**.
   5. **Refresh every browser tab that has this User Manual open: click in the tab and press the F5 key.** Do this for each one.

   **Don't skip step 5.** An open manual tab does *not* update itself. Until you refresh it, it keeps showing the *old* manual: old instructions, and a Recent program updates log without the changes you just installed. Nothing on the page tells you it's out of date. The same goes for any other NuMa tab you left open, so press F5 in those too.

   Nothing you've entered is lost: your data lives in your Windows user account area (`%LOCALAPPDATA%\numa` and `%APPDATA%\numa`), not inside the program file. That's also why deleting `nutrimagnus.exe` is all it takes to remove NuMa — delete those two `numa` folders as well if you want your data gone too.

#### Linux {: #install-linux}

a. **Where to get it.** Go to the [NutriMagnus releases page](https://github.com/tom-cloyd/NutriMagnus/releases) and download `install-linux.sh` from the latest release — the only file you need. Built and tested on Ubuntu 24.04 LTS; should work on most other modern Linux distros too, but only Ubuntu is verified. If it doesn't run on yours, see "For developers" in the project's `README.md` to run NuMa from source instead.

b. **Where it goes on your computer.** Run the installer once (`bash install-linux.sh`, from a terminal in the folder you downloaded it to). It installs to a private per-user location (`~/.local/bin`) — nothing outside your account is touched, and no admin password is needed.

c. **Getting it into your applications menu.** The installer also adds NuMa to your applications menu, like any program from a software center — it writes `~/.local/share/applications/nutrimagnus.desktop`, which every major Linux desktop reads automatically:

   The names below are Linux *desktop environments* — the part of Linux that draws your menus and windows. If you don't know which one you have, it is almost certainly GNOME.

   - **GNOME (Ubuntu's default):** press the Super key (⊞) or click **Activities**, then type "NutriMagnus" or "NuMa".
   - **KDE Plasma:** open the application launcher (bottom-left icon, or press Meta) and type the same.
   - **Other desktops (XFCE, Cinnamon, MATE, ...):** open the applications menu and browse to Utilities/Science, or search "NutriMagnus".

   **If it doesn't show up:** some desktops only refresh their menu index at login, so a program installed while you're already logged in can be invisible until you log out and back in. Still missing after that? See "If the icon never appears" below.

d. **How to launch it.** From then on, click NuMa's icon like any other program (see item c). It starts quietly in the background and opens a browser tab — no terminal, no typed commands, ever again.

**If the icon never appears,** even after logging back in, you can still run NuMa directly: open a terminal and run `~/.local/bin/nutrimagnus` — the same program the icon would have pointed to. [Contact us](#feedback) too, so this can get fixed for good.

#### What kind of program this is {: #install-webapp-note}

NuMa is a "web app" — it runs quietly in the background and shows its screens in a browser tab, like a website, but it's talking only to itself on your machine. It doesn't need the internet to run at all, and nothing you enter leaves your computer; NuMa reaches out only when you look up a food in an online [database](#gloss-database), or when it checks whether a newer version has been released. Two things follow from all this:

   - **The browser tab and the program are different things.** Closing the tab doesn't close NuMa — it's still running. To get back, start NuMa again the way you normally do (which opens a fresh tab) or open a new tab yourself to the same address.
   - **Sleep can disconnect the tab.** If your computer sleeps or hibernates while NuMa is open, the background program may stop and need restarting when it wakes — you'll typically see the tab fail to load. This is expected, not a sign anything's broken. Start NuMa again to relaunch it; your data is on disk and unaffected.

#### Backing up your data {: #backup}

Everything you put into NuMa lives in two folders on your computer, kept apart from the program itself: your foods, pantry, recipes, logged meals, annotations, profile and settings, and your 2021 glycemic index table if you built one (do this in Settings, item 11).

   - **Windows:** `%LOCALAPPDATA%\numa` and `%APPDATA%\numa`. Type either one, exactly as written, into File Explorer's address bar and press Enter to open it.
   - **Linux:** `~/.local/share/numa` and `~/.config/numa`. These are hidden folders in your home folder; press Ctrl+H in your file manager to show them.

**To back up,** copy both folders somewhere safe — a memory stick, an external drive, or a cloud-synced folder. Do it when NuMa isn't in the middle of saving something; the simplest way is to do it before you start NuMa for the day. Repeat it now and then: a backup only holds what you'd entered when you made it.

**To restore** — on a new computer, or after your system was wiped — install NuMa as described above, but don't start it yet. Copy both backed-up `numa` folders into place, replacing any that exist, and then start NuMa. Everything comes back as it was.

A [CSV](#gloss-csv) export from the Food Cache or Recipes pages is *not* a full backup. It's for moving selected foods or recipes around, and leaves out your meals, pantry, profile and settings.

### B. Start with what's easiest <!-- t:26-10-03 -->

This is a complex and powerful analytical program. A careful Internet search reveals that it is unique in its power and depth. It can be successfully approached by moving slowly and thoughtfully, with real benefit obtained early from using some of its easiest and simplest features. 

Start with what is easiest to understand: analysis of single foods and simple recipes. Use the manual to learn more. Do not expect to learn it all in a few sessions. [Contact us](#feedback) quickly rather than slowly if you start to get overwhelmed — one of our goals is to minimize the risk of that happening!

### C. Simple tips for new learners <!-- t:26-10-03 -->

**Slow down and look carefully at what you see on your screen.** What you see is the interface between you and the program. By design, it is rich in information. You don't need to understand or use all of it immediately, but notice that there are often links such as "Learn more ==>" or "Why?" encouraging you to link to a section of the manual that will tell you much more about something. We've worked very hard on the Manual, with the hope that it will both help you and educate you.

**Plan frequent program usage in the beginning.** Learning a powerful tool requires time and frequent contact. You have two critical things to learn: basic concepts (covered in [Part 4](#coreNutrition)) and the interface itself, including the functions listed on the main menu items' drop-down menus (see [Finding your way around](#web-shortcuts) in Part 3, and [Using the Foods menu](#foods-menu-web) and the sections after it for each menu in turn). **If you don't commit to daily use of the program, for about a week, you will not get past the slow-fumbling stage.** What you are dealing with is a Boeing 727, not a Piper Cub. Learn the cockpit and you can be a world traveler! (And that learning can come gradually, but daily exposure is the key.)

### D. NuMa often learns from YOU as you use it <!-- t:26-10-03 -->

While we don't yet have on-board local [AI](#gloss-ai) to help you with NuMa and your food questions, we do have NuMa remembering recent entries you've made to text input boxes, and a number of different options you've selected. Rather quickly, this will make use of the program easier and quicker.

One huge asset is the [Food cache](#FoodCache) [database](#gloss-database) you'll set up. This serves as a memory of every food you've looked up or put into your Pantry. Saved is the food name, [ID](#gloss-id) number, and nutrition data. Data retrievals from the online [databases](#gloss-database) take time; retrievals from you personal Food cache are essentially instant.

### E. Stuck? You have help nearby, and an on-call expert to assist you. <!-- t:26-10-03 -->

It happens to us all! You can first look in this manual's [Part 8 — Troubleshooting and feedback — reporting problems and offering ideas](#feedback) to see if your problem has an identified fix.

If you're wondering how to do something, search the Manual for one or two key words. For an especially efficient search, click the "Only show things you can do" checkbox that is right below the Manual's search text input box.

Still stuck? You need help...and it's readily available. Learn more...[here](#quickhelp).

### F. You can start food inputs with estimates, in many cases, but... <!-- t:26-10-03 -->

Use a kitchen scale to determine food quantities, if at all possible. It's easier than you may think, and much more accurate.

Regardless of how you eat, you will have to tell the program WHAT you are eating and HOW MUCH. The absolute best way to do this is to give it a weight. Sometimes you can just give it a "portion" or a volume measure instead, and the program will figure out the weight for you from that so it can keep going. However, remember that approximations are better than nothing, so if you can do nothing else, try to give NuMa an approximate amount.

Without the program you're flying blind. With it, even if you only use volume measures, there will be some errors of measurement, but you're still much better informed about what's happening than before. In some cases, though, a volume measure just doesn't work well. If that happens to you, [get in touch](#feedback) and we'll figure it out together. All in all, it's by far best to have and use a kitchen scale. I have had a small Oxo scale for years. It's excellent. There are others you can consider as well, but I do suggest that you get one.

### G. Setting NuMa up: first time, or after losing your data <!-- t:26-10-03 --> {: #first-setup}

Use this list the first time you run NuMa. Use it again if your computer was wiped or replaced and your NuMa data wasn't saved.

**Lost your data? Check this first.** If you have a backup of NuMa's two data folders, restore it — see [Backing up your data](#backup). Everything comes back, and you can skip the rest of this list. Only without a backup do you need the steps below.

**Starter foods and recipes.** A fresh install doesn't start empty. Your Food Cache and Recipes list already hold a small set of starter items: common foods, most with full amino acid data, and a few recipes showing protein complementing at work. Their names begin with an asterisk and a space (for example, `* Quinoa, cooked`), so you can always tell them apart from anything you've added yourself. Keep them or remove them as you like — see Step 2.

#### Step 1 — Settings you must address before you start

Go to **Settings**. Until these three are done, NuMa's results are either blank or quietly misleading.

1. **Your Profile (section 1).** Enter your age, sex, weight, height and activity level. Without them, every "% of daily target" column is blank. On the same form, also set:
    - the **Glycemic index lookup default** — choose impaired glucose tolerance if you have diabetes, pre-diabetes or insulin resistance; otherwise leave it searching both;
    - the **oxalate lookup** checkbox, if oxalates matter to you (for kidney stones, say).
2. **Dietary Preferences (section 3).** Choose all foods, vegetarian, or plant-based only. This filters *every* search and suggestion in NuMa, so a wrong setting hides foods you'd expect to see.
3. **[USDA](#gloss-usda) [API](#gloss-api) Key (section 5).** NuMa gets most of its food data from the US government's FoodData Central website. That site asks every program that uses it to identify itself with a **key**: a long code, like a password, that USDA gives out free to anyone who asks. Until you enter your own, NuMa uses one shared key for all its users, and when that shared key gets overused your food searches can fail for a while. Getting your own takes about a minute and costs nothing — see [how to get a USDA key](#food-data).

Then open **Computed Daily Targets (section 2)** and glance at the targets calculated for you, to check they look sensible.

#### Step 2 — Settings worth doing at some point

- **Glycemic Index Reference Table (section 11)** — only if you plan to track glycemic index (see Step 4): build the 2021 table ([how](#gi-editions)). Do this before Step 4 below, so your values come from the better table.
- **Nutrient Targets (section 7):** click **Load recommended Revised Optimal targets**, and add Max limits for anything you need to keep low.
- **Starter Data (section 9):** decide whether to keep the starter foods and recipes, or clear them.
- **Browser to Launch (section 10):** pick a browser, if you run more than one and don't want to be asked which each time.
- **Meals & Log columns (section 8):** choose which nutrient columns your meal lists show.
- **Protein Digestibility Overrides (section 6):** nothing to do now. It's for later, if you find a better digestibility figure for a particular food.

#### Step 3 — Set up your pantry

Your pantry is the list of protein foods you actually keep at home. NuMa looks there first when it suggests foods to fill a protein gap, so a good pantry makes those suggestions practical ones.

1. Look through [Appendix B](#appendix-plant-proteins) and note the foods there that you have, or would buy.
2. **Check the starter foods first.** Some of the foods you want are probably already in your Food Cache as starter foods — the ones whose names begin with `* `. They come with their nutrient data already checked, so using them saves real time. Go to **Foods → Food Cache**, type `*` in the filter box to list them, and add the ones you want to your pantry from there.
3. For anything not among them, go to **Foods → My Pantry** and add it **by search**, picking a result from the list. Only a search-and-select brings in the food's nutrient data, including its amino acids.
4. Prefer results with a ✓ in the **[AA](#gloss-aa)** (amino acid) column. Only foods with amino acid data can be used in protein suggestions, and plain, unbranded [USDA](#gloss-usda) entries are the likeliest to have it.
5. Can't find a food right away? Open **Can't find it? Save just the name for now** under the search box to save just its name, and link it to real data later with **Link a food**.

#### Step 4 — Glycemic index values for your core foods (optional)

**Most people can skip this step.** It's only for those who want to track glycemic index (GI) — for example, because of diabetes or pre-diabetes, or to manage blood sugar swings. If that isn't you, you're done.

NuMa never fills in GI values by itself; each one is a choice you make from the reference table. You don't need GI for everything, only for the **carbohydrate foods you eat most often**: grains, bread, rice, pasta, oats and breakfast cereals; potatoes and other starchy vegetables; beans and lentils; fruit; sweeteners. Skip foods with little carbohydrate (oils, most nuts, tofu, meat, fish, eggs, cheese) — a GI number means little for them.

For each food, go to **Foods → Annotate**, click **Edit**, and use **Look up a GI value from the published reference table**. When choosing between results, prefer, in this order:

1. **The same food, prepared the same way.** Boiled versus baked, whole grain versus flour, and cooking time all change GI a lot.
2. **The population that matches you** — normal or impaired glucose tolerance.
3. **Rows not flagged as "non-ISO method"** — that is, studies that didn't follow the international measuring standard, [ISO](#gloss-iso) (International Organization for Standardization) 26642 ([more](#gi-method-quality)).
4. **More recent studies, with more people tested and a smaller ± (standard error).**

If nothing is a genuine match, leave the value blank. No value is better than a wrong one. See [How to read a lookup result](#gi-result-row) for what each part of a result means.

Adding a food to your pantry or a meal also offers to ask you for its GI, so if you're tracking GI, say yes there too.

#### After an update: new starter items

From time to time, a new version of NuMa adds starter foods or recipes, or improves ones you already have. **NuMa tells you.** The **UPDATE AVAILABLE** message says what an update will change in them before you install it, and the first time the new version runs, a **NEW STARTER ITEMS** message on the home page says what it added or improved. Nothing in your data changes on its own; you choose, in [Settings → 9. Starter Data](#starter-data).

### H. Skim Part 2, A and F, just to know they exist. <!-- t:26-10-03 -->

While looking at section A, make a few notes about what you'd like to try first.

Seriously consider what is suggested in section F - looking at the workflows can quickly show you major program features.

### I. Consider investing some time with Part 4 <!-- t:26-10-03 -->

This program necessarily uses some specialized vocabulary. You have two options:

1. Learn the basics before diving into the program's functions and output.
2. Dive in first, and use the "Learn more..." links you'll see to immediately jump to the relevant manual section, so you can understand whatever's in front of you right when you need to.

---

## Part 2 — Introduction to NutriMagnus, a tool for intelligent eating: what you can do with this tool and why it matters

*(Reading time: 11 minutes)*

---

### A. What a user can do with NutriMagnus — brief overview

The five items in the top navigation bar correspond to the five major things you can do with the program:

- **Foods**
    - Search the [USDA](#gloss-usda) and Open Food Facts[^3] [databases](#gloss-database)
    - Analyze the nutrients in a specific portion of any food or recipe
    - Compare up to eight foods side-by-side
    - Manage your personal [Food Cache](#gloss-food-cache), Pantry, and custom food profiles
    - Annotate foods with glycemic index and [DIAAS](#gloss-diaas) estimates
    - Export/import your Food Cache as [CSV](#gloss-csv), to move data to or from another NuMa install
- **Recipes**
    - Create and save recipes with ingredients and instructions
    - Browse, copy, and delete saved recipes
    - Export/import a recipe as a self-contained [CSV](#gloss-csv), bundling every sub-recipe and ingredient's data along with it
    - Develop a recipe iteratively with nutritional feedback after each ingredient change
    - Analyze a recipe portion for full nutrient data, protein quality, and complement suggestions
- **Meals & Log**
    - Record what you eat by date
    - Add foods and recipes to meals
    - Analyze individual meals or the combined total for a full day, to monitor intake of any nutrient(s) of particular interest
    - Search your entire meal history for any food
- **Analysis** — a growing set of preset analyses
    - **Daily summary — [DCP](#gloss-dcp) and goals**: combined nutrient totals for today or any past date, compared against personalized [RDA](#gloss-rda) targets, plus a list of recent days with meals
    - **Food use in meals**: rank everything you actually ate — foods, recipes, sub-recipes, and the foods inside recipes — across a chosen set of date ranges and/or meals, with a frequency histogram
    - **Food use in recipes**: the same ranking, but for which foods and recipes are used as ingredients across your recipe book — not a measure of what you eat
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

This is the essential amino acid problem inherent in plant-based diets. The human body needs each of the nine essential amino acids in a fixed proportion to the total protein eaten — much like the bricks-to-cement ratio above. When a food, meal, or diet is short on one amino acid relative to that required ratio, the shortfall — not the total protein eaten — sets a ceiling on how much of that protein the body can actually use; the rest is broken down and discarded, like the unused bricks. (This required ratio is the [FAO 2013 Reference Standard](#fao) — see [Appendix A](#appendix-protein-quality) for the full technical explanation.)

While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24-hour period if the amino acid limitation problem is to be avoided. So, one way or another, one needs to tend to the issue of what is missing and where to find replacements to add it to one's diet in time.

**NuMa handles gracefully the tricky problem of managing plant-based proteins.** Few people know which foods have missing essential amino acids ([EAAs](#gloss-eaa)) or which have the needed excess [EAAs](#gloss-eaa) which would make them a good complement to eat with other foods lacking enough of those [EAAS](#gloss-eaa) in the same 24-hour period.

Beyond the problem of ingesting the right mix of amino acids, there are two other related dietary protein problems to be addressed:

* Protein in a food, however balanced or not, does no good if our bodies do not access it. Different protein sources in plant-based diets are metabolized in differing degrees of efficiency. This is the **[bioavailable protein](#gloss-bioavailable-protein)** problem.

* Age, sex, and activity level differences in protein needs do exist and they are not minor. Older people, active people, and those with chronic diseases, for example, require substantially more protein than do younger healthy people, for several reasons. Almost all common discussions of dietary protein fail to address this problem, and in any case a mere discussion doesn't tell one what to eat and how much.

### C. This protein-management problem is critical for older people and the chronically ill, and especially so for women <!-- tc:rev26-09-16 -->

In very brief summary, as we age, we tend to lose muscle mass, utilize dietary protein less efficiently, and simply eat less. These factors compound to create a perfect storm of vulnerability to general ill-health and the often dire consequences of falls. And these issues affect women more than men. Put simply - getting enough of the right sort of protein matters far more than most people realize. A good diet is utterly necessary, but not by itself sufficient. It must be complemented with adequate resistance exercise.

There is very little discussion of the problem in the mass media. So, it is up to use as individuals to self-educate and then make carefully considered decisions about our diet. But this is almost impossible to do without serious technical help, as the nutritional factors involved go well beyond simple arithmetic or the naively simple view offered to us by the first major statements about plant protein complementarity in the very early '70s.

### D. NutriMagnus is the missing helper

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

Nutrition analysis programs, both paid and free open source, already exist but none that we've seen focus on the problems faced by vegetarian and vegan folks. And none have the rich features and readily modifiable design that we want. The NuMa program addresses both problems in detail. It also suggests complementary foods that can be combined with a food or recipe or meal to create [complete proteins](#gloss-complete-protein) in one's diet.

NuMa has been under intense development and is still being developed. Over time, new users will experience unanticipated needs and the program can be further developed to meet them. This is one reason why [reporting problems](#feedback) is so important - feedback drives program development.

### E. Data, testing, and validation: Why you can trust NutriMagnus (NuMa) {: #data-testing-validation}

#### Reliable data sources

**[NuMa](#gloss-numa) draws on multiple data sources, and tells you which ones it is using.** Wherever the program makes a suggestion, it shows you which sources it consulted.

- **[USDA](#gloss-usda) FoodData Central**[^2] — the primary nutrient [database](#gloss-database), one of the most comprehensive public nutrition sources in the world. Used for most food searches.
- **Open Food Facts**[^3] — supplements [USDA](#gloss-usda) for branded and international foods, especially packaged products with a barcode.
- **Canadian Nutrient File** — Health Canada's reference [database](#gloss-database); particularly good amino acid coverage, which helps with [DIAAS](#gloss-diaas) calculations.
- **UK CoFID** (Composition of Foods Integrated Dataset) — ~2,900 UK foods from Public Health England/[DHSC](#gloss-dhsc); strong on macros, minerals, and vitamins, but has no amino acid data of its own.
- **Australian AFCD** (Australian Food Composition Database) — ~1,600 Australian foods from [FSANZ](#gloss-fsanz); also has real amino acid coverage, like Canadian Nutrient File.
- **French [CIQUAL](#gloss-ciqual)** — ~3,480 French/European foods from [ANSES](#gloss-anses) (2025 edition); like CoFID, no amino acid data. 

See [Food data — where it comes from and how it is stored](#food-data) in Part 8 for more on all six of NuMa's sources.

In addition, the following internal data sources are used:

- **Harvard T.H. Chan School of Public Health oxalate table**[^11] — a 433-food reference table used to fill in [oxalate](#gloss-oxalate) content when [Oxalate data](#oxalate) is switched on in Settings. (This is optional and is off by default.)
- **Atkinson/Brand-Miller international glycemic index tables**[^8] — a published reference table of about 2,500 foods, used to fill in [Glycemic Index](#gi) estimates automatically, rather than requiring you to type them in from scratch. A newer edition of over 4,000 foods can be added to your own copy of NuMa in a few minutes — see [Upgrading to the 2021 tables](#gi-editions).
- **NuMa's own curated protein-complement table**[^10] — a built-in list of 25 common protein sources used as a fallback for amino-acid data in complement suggestions, when your own data doesn't cover a gap.
- **Your own data** — foods saved to your [Pantry](#pantry), and [recipes you have analyzed](#recipes-menu-web), are consulted ahead of every other source above.


#### Extensive code testing

**[NuMa](#gloss-numa) has an extensive, fully automated test process.** As of this writing (2026-09-30), there are 1,311 automated checks the program must pass after every single change before it ships — everything from "does this page load" to "does this specific nutrition calculation come out to exactly the right number." Some of these don't just check a handful of hand-picked examples: they generate hundreds of realistic, random inputs and confirm a mathematical rule holds true for every one of them, and a newer, smaller set actually drives the app in a real browser window, end to end, rather than only checking the code in theory.

**NuMa is also periodically checked with a technique called mutation testing** — a way of testing the tests themselves. It works by deliberately planting a small, wrong change somewhere in the code (say, swapping a plus for a minus) and rerunning the test suite to see whether anything notices. If nothing does, that's a real, measurable blind spot — a piece of logic nothing is actually watching, something an ordinary "all tests passed" report can't reveal on its own. This has already found and closed several genuine gaps in NuMa's most complex code, the protein-quality math in particular, including places where a test was checking the right general idea but not the exact number, and places where one path through the code was covered while a nearby one wasn't covered at all.

**The protein-complement suggestion engine and the Claude AI fetch/import workflow each have their own extensive, dedicated test coverage**, on top of everything above. What each of those actually does is explained in plain language in [Protein Complement Suggestions](#comp) through [Two-step combinations](#comb), and in [Fetching missing data with Claude AI](#fetch).

*(For technically skilled users: the full file-by-file test breakdown, the specific tools used, and mutation-testing methodology/results are documented in README-numa-documentation.md's Test Suite and Maintenance sections.)*

#### Validation you can replicate yourself

**Appendix F has a fully worked out validation example.** You can do this yourself, if you like. Data are brought in from outside the program and run through the official correct computation process. Full source references are given. You can run the same computation in [NuMa](#gloss-numa) and compare the result.

#### Reasonable expectations: bugs remain

**Problems may appear anyway.** As professional programmers will tell you, all programs have bugs. This is more likely for new ones than for those which have been around for years. This is why you should report any result you are getting which doesn't make sense to you. There is a small chance you've found a "bug", but a greater chance that the program simply needs to explain itself to you more clearly. Either problem will be fixed ASAP, and all such fixes benefit everyone who uses the program.

**How to report suspected errors or problems with the program:** see [Getting more help](#feedback) in Part 8.

---

### F. Sample Workflows {: #sample-workflows}
**If you'd prefer to learn by example before reading explanations,** fully worked, step-by-step walkthroughs are provided later in this manual — see [Sample Workflows](#sample-workflows-web) in Part 3. You don't need to read Part 4 or Part 5 first.

---

## Part 3 — Using the Web App

*(Reading time: 39 minutes)*

NuMa's web app runs in your ordinary browser. This makes program development, which is ongoing, easier, and also provides the user with an interface they are already at least partly familiar with.

### A. Opening NutriMagnus

Launch NuMa the way it was set up on your computer — a desktop icon, an Applications-menu entry, or a shortcut someone set up for you. It opens automatically in your browser, normally at a browser address like `http://127.0.0.1:8000` — this just means "this computer, talking to itself," not an address on the internet, so don't worry if the exact numbers you see differ. If the page doesn't load right away, wait a few seconds and reload — the program is still starting up.

#### What you see on the home page {: #home-page-tour}

Right below the **Welcome to NutriMagnus** heading is a small block of status lines:

- **Dietary preferences** — your current setting (e.g. "All animal foods"), with a link straight to Settings to change it.
- **Active profile** — a one-line summary of your profile (age, sex, weight, height, activity level), or "not set" with a link to configure one if you haven't yet.
- **Current version date** — the exact build you're running, as `yyyy-mm-dd:hhmm`, alongside a human-facing release version (e.g. `0.1.0-rc.1`). Whenever `version.py`'s build note is set, it follows in parentheses as "(Version note: ...)" — a short plain-language description of what changed in that build. Right after it, a **Check for updates now** link re-checks GitHub immediately instead of waiting for the periodic check — useful right after dismissing an UPDATE AVAILABLE banner if you change your mind, since it also undoes that dismissal. It only appears when no update is currently showing.

Above all of that, a few one-time or conditional banners can appear when relevant: a **NEW TO NUMA?** message linking to the [setup checklist](#first-setup) until your profile is saved, a **NEW STARTER ITEMS** message the first time a new version runs, if it added or improved starter foods or recipes (see [Starter Data](#starter-data)), a [database](#gloss-database)-integrity warning, an "update installed" confirmation right after using Update Now, an update-failed message, and an **UPDATE AVAILABLE** banner when a newer release exists on GitHub. If you're running the packaged Linux install, this shows an **Update Now** button that installs the update in place; otherwise (Windows, or a non-packaged Linux checkout) it shows a **Download NutriMagnus** button that goes straight to the new installer file. That banner repeats the build note as its own line, says what the update would add to or improve in the [starter foods and recipes](#starter-data) you have, and has a **Don't show this again for this version** checkbox — same idea as the System Issues banner's "Got it" checkbox below.

**When does NuMa actually check for a new release?** Every time the home page loads — at launch, on a manual reload, or by navigating back to it from anywhere else in the program — it asks whether a newer version exists. That check itself is cached for a few hours, so bouncing back to the home page repeatedly doesn't re-contact GitHub every time; it just reuses the last answer until the cache expires. Once a newer version is available, the **UPDATE AVAILABLE** banner shows on every single page load — it never disappears on its own — until you either install the update or check the "Don't show this again for this version" box; a later, different release always shows regardless of what you've dismissed.

### B. Finding your way around {: #web-shortcuts}

Every page has the same navigation bar across the top: **NuMa** (takes you home), **Foods**, **Recipes**, **Meals & Log**, **Analysis**, **Settings**, and **Manual** (this document). **Foods** and **Analysis** open as drop-down menus with several choices each; the others go straight to their page.

If you'd rather use the keyboard, each nav item has a shortcut — hold **Alt+Shift** and press the item's first letter (`F` for Foods, `R` for Recipes, `C` for Compare, `M` for Meals & Log, `N` for Analysis, `S` for Settings, `A` for Manual), using the underlined letter shown in each menu item and Settings section heading (e.g. `Alt+Shift+3` jumps to Dietary Preferences within Settings; section 10, Browser to Launch, is `Alt+Shift+0`; sections 11 and 13 use their first letter, `G` and `D`; and section 12, System Issues, is `Alt+Shift+Y`, since `S` already belongs to Settings). This works the same way in any desktop browser (Firefox, Chrome, Brave, Edge, and the rest) — it's NuMa's own page script listening for the key combination, not a browser-specific feature, so it isn't limited to whichever browser you happen to be using. For a dropdown menu item (Foods, Analysis), the shortcut also moves keyboard focus straight to the first item in the menu that opens — from there, ArrowUp/ArrowDown moves between items, Enter or Space picks one, and Escape closes the menu, all without touching the mouse. It's unrelated to, and does not affect, anything stored in your NuMa data. Turn it on or off in **Settings → Keyboard Shortcuts**; the setting is stored in your browser (not synced across devices) and takes effect immediately, with no page reload needed.

Most detail pages (a food, a recipe, a meal) show a collapsible outline down the side — click a heading there to jump straight to that section. Forms that have unsaved changes mark their Save button so you can tell at a glance whether you've edited something, and the browser will warn you before you navigate away from an unsaved form. On the pages with a substantial edit form — Edit Recipe, a meal, Edit Custom Profile, Annotate a Food — NuMa goes further, with the "Data-entered safety" note at the top of each: click a link elsewhere in NuMa with unsaved edits and NuMa offers to save them for you first, or to leave without saving, or to stay and keep editing. On Edit Custom Profile, Edit Recipe and a meal page, running a search (or re-sorting its results) while you have unsaved edits saves them for you first, and a note at the top of the results offers to undo that save. (Closing or refreshing the browser tab is the one case NuMa can't step into — only your browser's own "leave this page?" warning appears there, so save first if you're closing the tab.)

#### Search boxes remember your last search {: #search-memory}
On a meal's "Add Food or Recipe" search, a recipe's "Add Ingredient" search, and the Foods: Search page, if you follow a link away to look something up elsewhere and then come straight back to that exact page, your last search and its results are restored automatically — you don't have to retype it. This only applies to a plain link back to the page (the browser's own Back button already preserves it); it's scoped per page, so it never leaks a search from one meal into another.

There's no time limit on this — it holds for as long as your browser tab stays open, not just for a moment after you step away. Clicking **Clear search** (shown next to the search box whenever a search is active) or closing the browser tab clears it back to the page's clean, empty-search state.

The main navigation bar goes further than any one page: clicking **Recipes**, **Meals & Log**, **Compare**, **Settings**, or **Manual** returns you to the exact page you were last on in that section — e.g. the specific recipe you were editing, or the exact set of items you had lined up on Compare — instead of always landing on its list/default page. That only happens when you arrive from a *different* section: click **Meals & Log** (or press `Alt+Shift+M`) while you're already working on a meal, and you go to the Meals & Log list itself. When that memory is what brought you back, the page's breadcrumb is highlighted, with a one-click "All recipes" / "All meals" link in case you actually wanted the plain list. **Foods** and **Analysis** are drop-downs of separate destinations (Search, Pantry, Daily summary, and more), so they work a little differently: a small "↩" quick-return link appears next to the drop-down whenever there's a page you've viewed in it, showing that page's name, so you can jump back to it in one click after wandering off elsewhere — the drop-down itself always opens normally. Following a breadcrumb link (e.g. **Recipes** at the top of a recipe page) back to the list always starts fresh, clearing any remembered search or position.

**Long pages also come back the way you left them.** On the Daily Summary, a meal, a recipe, and a food's own page, NuMa remembers how far down you had scrolled and which collapsible sections you had open, and puts both back when you return to that page. Like the search memory above, this lasts as long as the browser tab stays open. Two things are deliberately left out of it: inline **Edit** panels never reopen by themselves, since closing one is how you discard what you typed in it, and a link that points at a specific spot on a page (any link ending in `#something`) still takes you to that spot rather than to where you last were.

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

**Step 1 — Add a food to your Pantry.** Click **Foods** in the navigation bar, then click **7. My Pantry**. On the Pantry page, type `hemp seeds` into the search box under "Add a pantry item — search for full amino acid data" and click **Search**. A results table appears — click **Add to pantry** next to the best match. (The **Can't find it? Save just the name for now** link just under the search box skips the search and saves just the name, with no nutrient data — use it only when you can't find a match.)

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

**Foods → Custom food profiles.** Enter a homemade dish, a supplement, or a product NuMa's [databases](#gloss-database) don't have (or have incompletely) — either from scratch, or by copying an existing cached food as a starting draft and editing its nutrients from there.

**Recipes: use one recipe inside another.** A recipe can be added as an ingredient of another recipe — a lentil sauce used inside three different dinners, say. Editing and saving the base recipe keeps every recipe built on it up to date automatically — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 6.

**Recipes → Archive/Restore.** Hide a recipe (or a food, or a pantry entry) you're not using right now without deleting it — see [Archiving](#archive) in Part 5.

---

#### Workflow 4 — Logging several days, then spotting a pattern in Analysis

**What this shows:** how Analysis turns a handful of logged days into something a single meal — or even a single day — can't show you: a full day's combined nutrition, and a pattern across many days.

**Step 1 — Log a couple more days.** Click **Meals & Log → New Meal** and create two or three more meals across two or three different dates — reuse foods from Workflows 1–3 if you'd like to keep it quick (`brown rice cooked`, `black beans cooked`, `corn tortilla`).

**Step 2 — Analyze a full day.** Open any one of the meals on a date where you logged more than one — a button reading **Analyze full day (N meals)** appears near the top of the page whenever that's the case. Click it. NuMa pools every meal logged that date into one combined analysis — total nutrients, pooled protein quality, and complement suggestions across everything you ate that day, rather than meal by meal.

**Step 3 — Check the Daily Summary.** Click **Analysis → 1. Daily summary**. The Recent Days table lists every date you've logged: Protein first, then Day [DCP](#gloss-dcp), then % goal and Goal, then any other nutrients you've picked in Settings. Click any date to reopen that day's full analysis.

**Step 4 — Catch a chronic pattern with Nutrient Averages Across Days.** From the Daily Summary page, click **Nutrient averages across days** and choose a 7, 14, or 30-day window. NuMa averages your intake over that window and compares it to your [RDA](#gloss-rda) targets — surfacing a nutrient that's persistently a little low, the kind of gap a single good or bad day would hide.

**Step 5 — See the shape of it with Nutrient Plot.** Click **Nutrient plot** instead. Check Day DCP and Protein (or any other nutrient you're curious about), then click **Plot**. NuMa draws a line plot across your logged days — sometimes a shape on a plot makes a pattern obvious in a way a table of numbers doesn't.

**What you learned:** Analyzing a full day rolls up everything you ate; Daily Summary tracks that day by day; Nutrient Averages Across Days and Nutrient Plot turn many days into a pattern you can act on — two different views (numbers-against-target, and shape-over-time) of the same underlying data.

---

### D. Using the Foods menu {: #foods-menu-web}

#### Search (Foods → Search)

Type any part of a food name, an [FDC ID](#gloss-fdc-id) number, or a 12/13-digit barcode ([UPC](#gloss-upc)-A or [EAN](#gloss-ean)-13) — see [Your own data is always checked first](#search-ranking) in Part 6 for how results are sourced and ordered. Next to the search box, a row of Source checkboxes (Pantry, Food Cache, Recipes, [USDA](#gloss-usda), Open Food Facts) lets you narrow results to any combination of sources before or after you search — see [Source filter](#food-search) in Part 6 for details. Click a result to open its full [Nutritional Analysis](#nutrients), [Protein Quality](#protein-quality), and complement-suggestion page.

#### Analyze a food portion / Analyze a saved recipe portion

Shortcuts into Search that take you straight to entering an amount once you've picked a food or recipe, rather than seeing the per-100g view first.

#### Convert

A pure unit-conversion tool — search for a food (with the same [Source filter](#food-search) as every other search box), then type any amount (`3 oz`, `1/4 cup`, `150 g`) to see its gram/mL equivalent and the closest named portion size. No nutrient analysis is shown here; use Search for that.

#### Compare

Add up to eight foods (checkboxes in the search results, filterable by [Source](#food-search) the same as any other search) and set a gram amount for each to see them side by side in one nutrient table. Comparisons can be saved under a name and reopened later, renamed, or deleted.

#### Food Cache {: #food-cache-web}
Every food NuMa has ever fetched from [USDA](#gloss-usda) or Open Food Facts[^3] lives here — see the [Food Cache column guide](#cached) in Part 5 for what each column means. A **Sort by** dropdown orders the list by Name, [ID](#gloss-id), Type, [DIAAS](#gloss-diaas), or [GI](#gloss-gi) estimate. A misspelled filter offers a ["Did you mean"](#search-suggestions) correction, same as any other search box. Per-food actions: **Add to pantry** (adds the food to your [Pantry](#pantry) and returns you to the same row; a food already there shows **In pantry** instead, which opens the Pantry), **Portions** (add or edit named portion sizes), **Refresh** (fetch USDA's current copy of the food and [choose which changed values to take](#review-incoming)), **Archive/Restore** ([hide without deleting](#archive)), and **Delete** — refused if a pantry entry, recipe, or meal still uses that food, since deleting it anyway would leave that entry pointing at nothing; the refusal names and links every blocking pantry entry, recipe, and meal by id (e.g. "pantry: 34 | recipe: 12 | meal: 9, 72") so you can go straight to the place to remove or replace it, or use Archive instead. **Prune unused foods** removes cache entries no pantry entry, recipe, or meal is currently using — with a checkbox per food (checked by default) so you can uncheck anything you'd rather keep before pruning. Each row also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) above — for jumping straight into [Comparison](#comparison) with the checked items.

**Check [database](#gloss-database) integrity.**{: #db-check} *(This page — Foods → 9 — now runs five checks: broken references, below; [missing nutrient data](#data-completeness); [food data problems](#calorie-checks); [amounts that no longer match](#stale-amounts); and [old USDA copies](#old-copies). [Checking your data](#checking-your-data) lists every data check NuMa makes.)* The first scans for pantry entries, recipe ingredients, or logged meal items that still point at a food or recipe no longer in the cache — leftover from before Delete started refusing to remove still-used foods, or from a manually edited [database](#gloss-database) file. Opening a food page for one of these fails, since NuMa treats the missing food as never-cached and tries to re-fetch it from USDA by [ID](#gloss-id) — which errors outright for an Open Food Facts food (its ID isn't a real USDA ID) and can return the wrong food for a reused-looking one. The check page lists every problem found, grouped into up to five kinds, **each with its own fix button and a plain-language note on what that fix actually does** — they're kept separate because the consequences are not equivalent:

- **Pantry entries** — low impact; removing one only takes it off your pantry list.
- **Recipe ingredients** — removing one deletes that ingredient line from its recipe; the recipe's nutrient totals recalculate without it.
- **Logged meal items** — removing one deletes that food/recipe from a day's logged meal history; that day's totals recalculate without it, same as if it had never been logged.
- **Sub-recipe references** — non-destructive; nothing is deleted, the ingredient is just flagged "recipe (deleted)" (the same label used everywhere else a referenced recipe is gone) instead of erroring.
- **Unreadable nutrient/portion data** — never auto-repaired; each food gets its own **Refresh** (re-fetch from USDA) and **Delete** buttons so you decide.

**Check for missing nutrient data.**{: #data-completeness} The same page (Foods → 9) has a section, **Missing nutrient data**, listing every cached food that has *no* values at all for one of six nutrient groups — the five blocks of a Nutritional Analysis table (Macronutrients, Omega Fatty Acids, Minerals, Vitamins, Phytonutrients) plus Amino Acids. Macronutrients count as missing if even one of calories, protein, carbohydrate, or fat is absent; amino acids only for a food that has protein. A group with *some* values is normal for real data and isn't listed.

Not every gap matters. Basil doesn't need macronutrients — too little goes into a recipe to count. For a gap like that, check **not needed** under it and click **Save "not needed" choices**: NuMa stops listing it for that food, stops warning about it on the food's own page, and leaves it out of any Claude AI prompt (which tells Claude it's not needed). To undo one, tick **Also list foods whose only gaps are marked "not needed"**, uncheck the box, and save again. **Groups to check** narrows the list to the groups you care about. Omega Fatty Acids and Phytonutrients start out unchecked: most ordinary food records were never measured for them, so checking them lists nearly every food. Tick them if you want them anyway. NuMa remembers both settings.

To fill real gaps, check **ask AI** under each gap you want help with — one food, a few, or a whole group at once with the **all** link under that column's heading — and click **Build a Claude AI prompt for the gaps checked "ask AI"**. The prompt covers only the gaps you checked. See [Fetching missing data with Claude AI](#fetch) below. A food's own page offers the same thing: if it's missing core macronutrients you'll see a warning with **Ask Claude AI for the missing data** and **Macronutrients not needed for this food** buttons, and any other missing group is named in a short line under it.

**Calorie checks.**{: #calorie-checks} Calories are the one figure NuMa can check against the rest of a food's data: protein and carbohydrate supply about 4 kcal per gram and fat about 9, so a food's protein, carbs and fat imply roughly what its calories should be. NuMa uses that in two ways.

- **Missing calories are filled in.** When a food arrives — from USDA, Open Food Facts, a [CSV](#gloss-csv) file, Claude AI, or typed in by you — with protein, carbs and fat but no calories, NuMa works the calories out from those three and marks the figure as an *estimate*. If the food's source later supplies a real figure (a Refresh from USDA, say), that replaces it. If you change the food's protein, carbs or fat, the estimate follows. A food missing even one of the three can't be estimated; it stays missing.
- **Calories that don't add up are flagged.** A stored figure far from what the food's own protein, carbs and fat imply (more than about a quarter off) is flagged, never changed. Sometimes the gap is real: alcohol, sugar alcohols and very high fiber all carry energy that the 4-4-9 rule doesn't model. Otherwise it usually means the food's data is wrong. When you know a food's calories are right, the **These calories are right — stop flagging them** button on its page turns this check off for that food (**Check them again** turns it back on).

The same page (Foods → 9) has a section, **Food data problems**, listing every food in either situation (along with any food holding an [impossible value](#data-checks-list)), plus every food whose calories are estimated, for information. Foods whose macronutrients you've marked "not needed" (a supplement, a spice) aren't checked for calories. A meal, recipe or daily summary that includes such a food shows a short **Calories** note above its Nutritional Analysis table: it leads with how much of the calorie total comes from measured values, then names each food, so you know when the total is approximate or too low. See [Checking your data](#checking-your-data) for every other check. To fix a food, open it and use **Refresh from USDA** (for a USDA food), **Fill in nutrients from another food**, or edit its values directly.

**Fetching missing data with Claude [AI](#gloss-ai).**{: #fetch} Some foods — especially branded or prepared items — arrive without amino acid data, and a few arrive missing even calories or protein. Check the boxes next to the foods you want (or click "Select all missing [AA](#gloss-aa) data" to grab every food currently missing it), then click **Fetch missing data from Claude AI**. (You can also start from the [missing nutrient data check](#data-completeness), or from the warning on a food's own page.) This builds a ready-to-send prompt and shows it on its own page with a **Copy prompt to clipboard** button.

The prompt asks only for what each food is missing — the specific values, food by food — and says nothing about groups you've marked "not needed" except that they're not needed. A food with nothing missing is left out (the page tells you which). From there:

1. Go to [claude.ai](https://claude.ai) — open a **new chat** (not an existing one) — paste the prompt, and send.
2. When Claude finishes, copy its entire reply (all of it, including every fenced `json` block — if Claude splits its answer across multiple messages, copy each one and paste them together).
3. Back in NuMa, click **Import Claude response** (also reachable directly from the Food Cache page), paste the reply into the box, and click **Review**.
4. NuMa shows you a table of what it understood from the reply — name, [FDC](#gloss-fdc) ID, calories, protein, how many of the 11 tracked amino acids were found, and what importing will do — plus any warnings about data it couldn't use. Check it over, then click **Import** to save it to your cache.

**Importing only fills gaps.** For a food already in your cache, importing adds the values it was missing and nothing else — every value it already has stays, and so do its name, portions, and notes. If Claude's reply includes a different value for something the food already has, the review table names it, and a checkbox, **Also replace the values these foods already have**, lets you take Claude's value instead. Leave it unchecked unless you mean it.

#### My Pantry

Foods you keep on hand — see [My Pantry](#pantry) in Part 5 for the column guide. Pantry foods are checked first for complement suggestions and search results. Add a food with full nutrient data via search (with the same [Source filter](#food-search) as every other search box), or use **Can't find it? Save just the name for now** for something you haven't looked up yet (link it to real data later with **Link a food**). Only the search-and-select route caches the food — see [Only a search-and-select adds a food to your Food Cache](#pantry) in Part 5. Searching for a food already in your pantry shows a **Remove from pantry** button right on its search-results row, so you don't need to scroll down to find the matching row in the pantry list to take it out. Each pantry item with a linked food also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) above — for jumping straight into [Comparison](#comparison) with the checked items; a quick-add item with no linked data can't be compared.

#### Custom food profiles

Create a food NuMa doesn't already have — a homemade dish, a supplement, or a product with an incomplete [database](#gloss-database) entry. Either start from scratch, or **copy a cached food as a draft** and edit its nutrients from there — both of the page's "copy from another food" searches have the same [Source filter](#food-search) too, and can now reach Open Food Facts as well as your cache and [USDA](#gloss-usda). A misspelled "copy a cached food as a draft" search also offers a ["Did you mean"](#search-suggestions) correction. See [Entering custom foods and dietary supplements](#custom-foods) below.

#### Annotate

A list of cached foods where you can enter a glycemic index estimate, a [DIAAS](#gloss-diaas) estimate, prep-context notes, or check "don't ask again" for a specific nutrient. NuMa also opens this automatically as a follow-up prompt right after certain actions when data is missing — you can skip it for now or skip it permanently for that food. The filter box offers a ["Did you mean"](#search-suggestions) correction on a misspelled name, same as any other search box.

### E. Opening a food's detail page

A food's page shows, in order: **Protein Summary** ([DCP](#gloss-dcp)), **Nutritional Analysis** (type any amount, or pick a named portion, then click **Recalculate**), **Protein Quality** ([DIAAS](#diaas) and the per-amino-acid table), **Anti-nutrients**, **Complement Suggestions** (pantry foods first, then general suggestions, then two-food pairs and combos — each can be [ignored and recalculated](#ignore-complement)), and an **Add to Pantry** form at the bottom. If the food has no amino acid data, you'll see a suggestion to search for a Foundation or [SR](#gloss-sr) Legacy equivalent instead — those datasets are the ones most likely to have complete amino acid profiles.

Right below the title, every food's page also has a **Copy as custom-food draft** button — no detour through Food Search or Custom Food Profiles needed to start editing a copy of what you're already looking at. See [Entering custom foods and dietary supplements](#custom-foods) for what to do with the copy.

### F. Using the Recipes menu {: #recipes-menu-web}
The **Recipes** page lists every recipe, with filter/sort options and a **Show archived recipes** / **Hide archived recipes** button. A misspelled filter offers a ["Did you mean"](#search-suggestions) correction, same as any other search box. Row actions: **Edit**, **Copy**, **Archive/Restore**, **Delete**. **Recompute [DCP](#gloss-dcp) for all recipes** refreshes every recipe's protein score at once, and **Broken recipe references** finds any recipe whose sub-recipe ingredient was since deleted — see [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) in Part 6. Each row also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) in Part 5 — for jumping straight into [Comparison](#comparison) with the checked recipes.

Editing a recipe's ingredients or servings recalculates its own [DCP](#gloss-dcp) automatically, and cascades to every recipe that depends on it too — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 6. You don't need **Recompute DCP for all recipes** just because you changed one recipe; it's there for after a bulk import, or if you suspect stale numbers from before this cascading recalculation existed.

- **New recipe** — a short form (name, description, servings, total yield) that drops you straight into editing.
- **Edit** — a details form plus an ingredients table, with a single **Save recipe details** button (on the "Recipe details" heading row) that saves every field in that form at once. The details form includes an **Introduction** field for background — where the recipe came from, why you like it, serving notes — anything that isn't the step-by-step instructions — and, below Instructions, a **Notes and documentation** field for anything you want on record: sources you consulted, substitutions you have tried, changes to make next time. Notes print at the very bottom of the recipe's nutritional analysis, go into the recipe [CSV](#gloss-csv) export, and are included in the [AI](#gloss-ai) translation. Add an ingredient by searching — the results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns and the "Fetch full details for selected" [AA](#gloss-aa)-confirmation button — then typing a portion (`150 g`, `1/2 cup`, or a saved preset like `p1`) — NuMa saves it as grams at that moment, so later changes to the food's portions don't alter it (see [Editing or changing a food](#food-edit-consequences)); reorder ingredients with the up/down controls, or edit or remove one inline. A **Running totals** card at the side updates live as you add ingredients, showing calories, protein, and DCP for the whole recipe and per serving.
- **Detail** — mirrors a food's detail page (Introduction right after the title, Protein Summary, Ingredients, Instructions, Nutritional Analysis, [Complete Protein Analysis](#meal-diaas) with per-ingredient digestibility, Missing AA Profiles, Complement Suggestions — [ignorable and recalculable](#ignore-complement) here too, [Glycemic Load](#glycemic), Anti-nutrients), plus a servings field to re-analyze at a different batch size. **Print/save recipe** opens a stripped-down, print-friendly version in a new tab, with Introduction included as one of the "Include on this printout" checkboxes. Above those checkboxes, a **Print layout** choice (Full sheet or Half sheet — Half sheet shrinks the title and tightens line spacing throughout, including the Ingredients list) and a **Paper size** choice (US Letter or A4, which sets the exact page dimensions your browser's Print/Save-as-[PDF](#gloss-pdf) preview paginates against) are both remembered for next time. This printable page — and the same layout/paper choices — is also available from a food's, a meal's, and a day's own detail page, not just a recipe's.

### G. Using the Meals & Log menu

The **Meals & Log** page has a **New Meal** form at the top (name + date), filters for date and sort order, a **Search meal history** link for full-text search across everything you've ever logged (a misspelled search there also offers a ["Did you mean"](#search-suggestions) correction), and a batch button to calculate DCP and calories for all meals, or just the last 10 or 30 days. The list itself shows each meal's completeness, item count, Meal DCP, Day DCP (combined across all meals on that date), % of your daily goal, and calories.

Open a meal to add foods or recipes (search box at top — for a recipe you can log the whole thing or just individual ingredients), edit or remove items inline (a food's amount is saved as grams the moment you enter it, so later changes to that food's portions don't alter it — see [Editing or changing a food](#food-edit-consequences)), mark the meal complete/incomplete, rename it or change its date, or merge it with other meals logged the same day. Below the item list: [Nutritional Analysis](#nutrients), [Meal-Level Protein Analysis](#meal-diaas) (with a **Refresh from [USDA](#gloss-usda)** button if amino acid data needs updating), Missing [AA](#gloss-aa) Profiles, Complement Suggestions ([ignorable and recalculable](#ignore-complement)), [Glycemic Load](#glycemic), and Anti-nutrients.

If more than one meal is logged on the same date, **Analyze full day** rolls all of them into one combined analysis — total nutrients, pooled protein quality, and complement suggestions across everything you ate that day.

### H. Using the Analysis menu {: #analysis-menu-web}

- **Daily summary** — a table of recent days with Day [DCP](#gloss-dcp) and % of goal; pick a date to see that day's full analysis (same sections as the full-day meal view). From here, follow the **Nutrient averages across days** link to see 7/14/30-day averages — useful for catching a chronic shortfall that a single good or bad day would hide.
- **Food use in meals** — see how often you've eaten a given food or recipe. Everything you actually ate is counted: foods logged on their own, recipes, the sub-recipes inside them, and foods you only eat inside recipes. Choose either a date range or a specific list of meal IDs, optionally limit results to protein-containing foods, and get a sortable table with a visual frequency bar.
- **Food use in recipes** — the same idea, but for your recipe book: see how many of your recipes use a given food or sub-recipe as an ingredient. This doesn't measure what you eat: a recipe you log in meals but never use inside another recipe won't appear. Choose all recipes, a date-created range, or a specific list of recipe IDs.

Both Food Use pages have a **Substitute a food or recipe** panel for bulk-replacing one food or recipe with another across whatever's currently selected — see [Substituting a Food or Recipe](#fooduse-substitute).

### I. Using the Settings menu {: #settings}
Settings is organized into thirteen numbered, collapsible sections:

- **1. [Your Profile](#profile-setup)** — age, sex, weight, height, activity level (this drives all your daily nutrient targets), plus a checkbox enabling [oxalate](#oxalate) lookup and the [glycemic index lookup default](#gi).
- **2. Computed Daily Targets** — see [Part 6](#daily-nutrient-targets).
- **3. Dietary Preferences** — affects complement suggestions, [B12/iron/zinc guidance](#diet-bioavailability), and (see [Dietary Preferences](#diet)) every search and lookup in the program.
- **4. Keyboard Shortcuts** — see [Finding your way around](#web-shortcuts).
- **5. [USDA](#gloss-usda) [API](#gloss-api) Key** — lets you use your own free personal code from USDA's website instead of the one NuMa shares with every user by default, so your searches are less likely to get temporarily blocked when many people are using NuMa at once (see [Food data](#food-data) for how to get one); also has the [search result depth](#search-ranking) setting.
- **6. Protein Digestibility Overrides** — custom digestibility numbers for specific foods.
- **7. Nutrient Targets** — optional per-nutrient [Revised Optimal (Recent Research)](#optimal) targets and [Max limits](#maxlimits), with a one-click button to load recommended defaults.
- **8. [Meals & Log columns](#meal-columns)** — which nutrient columns your meal lists show.
- **9. [Starter Data](#starter-data)** — curated foods and recipes to explore or build on.
- **10. Browser to Launch** — see below.
- **11. Glycemic Index Reference Table** — which [GI](#gloss-gi) table lookups search, and building the 2021 one (see [Upgrading to the 2021 tables](#gi-editions)).
- **12. System Issues** — see [below](#system-issues-howto).
- **13. Data Quality Reminder** — the Home page note about new data problems (see [Checking your data](#data-check-reminder)).

#### Your Profile {: #profile-setup}
Age, sex, weight, height, and activity level. This is the one form that everything else in NuMa's nutrient-target system depends on: your [RDA](#rda) values (Part 5, Section P), the age/sex-adjusted [Daily Nutrient Goals](#goals) (Section Q), and — where you've set them — your [Revised Optimal targets](#optimal) and [Maximum Nutrient Limits](#maxlimits) all key off the age, sex, weight, height, and activity level you enter here. Also on this form: a checkbox enabling [oxalate](#oxalate) lookup, off by default.

Leave this form empty and NuMa still works — you can search, log, and analyze foods and recipes — but every nutrient table's "% of daily target" column is blank, since there's no profile to calculate a target from. Fill it in whenever you're ready; every already-logged meal is re-evaluated against your new targets immediately, nothing needs to be re-entered.

#### Browser to Launch

Starting NuMa opens a browser tab automatically. If you have more than one browser running at the time (Firefox, Chrome, Chromium, Brave, Vivaldi, Opera, Edge, or GNOME Web), NuMa normally asks which one to use via a small dialog. Setting a **Browser to Launch** here skips that dialog and always uses the one you pick — leave it on "Ask each time" (the default) if you're fine being asked, or don't run more than one browser at once.

#### Starter Data {: #starter-data}

This is a small set of curated content: foods, and recipes made from them. The foods come from [USDA](#gloss-usda) and NuMa's other sources, and a few are custom foods; many carry full amino acid data, and a food may come with a glycemic index value already filled in (only ever one NuMa is permitted to share). Several of the recipes show protein complementing at work, pairing foods so that the amino acids each is short on are covered by the other. Many of the starter foods are there only because a starter recipe uses them: a recipe can't be loaded without its ingredients, which is why everyday items like salt, vanilla and cinnamon are in the set. **Settings → 9. Starter Data → View all starter data** shows, beside each food, which starter recipes use it. Their names all start with `* ` so you can always tell them apart from anything you've added yourself. A brand-new install loads this automatically the first time you launch it, so your Food Cache and Recipes aren't empty on day one — this section is for anyone who cleared it and wants it back, or an existing install that never had it. Clearing it is never permanent: **Load starter data** reappears here to put it all back, and **Restore individual starter items** brings back just the ones you pick. Your pantry starts empty: it's the list of foods *you* keep at home, so only you can fill it (see [Set up your pantry](#first-setup)).

Loading starter data never touches anything already in your cache, pantry, or recipes: a starter food you already have is simply skipped. It's tracked separately, so **Clear starter data** (which appears once it's loaded) removes only what was added, and nothing else. Loading again while it's already loaded does nothing.

**Clear keeps whatever you've made your own.** A starter food or recipe you've renamed (including taking the `*` off its name), edited, re-portioned, or given a glycemic index or [DIAAS](#gloss-diaas) value is yours from then on, and Clear leaves it alone. So does anything you're still using: a starter recipe you've logged in a meal or used inside one of your own recipes, and a starter food that a meal, one of your recipes, or your pantry still uses. After clearing, Settings says how many items were kept, and why.

**When a new version changes the starter set.** NuMa remembers which starter foods and recipes the version you ran before came with, so after an update it can tell you exactly what's different:

   - **New items** are marked **(new in this version)** in the **Restore individual starter items** list, which opens by itself when there are any, with a short description: a food's type, calories and protein per 100 g, and whether it has amino acid figures; a recipe's ingredients. Check the ones you want and click **Restore selected**. Something you deleted on purpose is never presented as new; only items the new version actually added are.
   - **Improved items** — starter foods or recipes you already have, which the new version has corrected or improved — are listed under **Improved in this version of NuMa**. Under each one, NuMa shows exactly what updating would change in *your* copy: for a food, each value side by side (yours now, the new version), with any value you edited yourself marked **your edit**, and portions that would be added or removed; for a recipe, changed servings, name, description or instructions, and ingredients added, removed or with a new amount. Check the ones you want and click **Update the checked items to the new version**. Updating replaces your copy with the new one, *including any changes you made to it yourself*, so leave unchecked anything you've edited and want to keep. Meals, recipes and pantry entries that use an updated item keep working, and their figures are recalculated. **Keep all my copies as they are** stops NuMa offering the improved versions.

These lists stay until you act on them, even after you dismiss the home-page message about them. If you skip a version, nothing is lost: the next version's lists include the skipped one's changes.

#### Computed Daily Targets

This section of Settings shows your personalized nutrient targets. See [Your computed daily nutrient targets](#daily-nutrient-targets) in Part 6 for what it contains and how it's kept current.

#### System Issues {: #system-issues-howto}
*One of NuMa's data checks — see [Checking your data](#checking-your-data) for the rest.*

Every recipe caches its protein-quality score (DCP) so it doesn't have to be recalculated every time you view it, and every meal saves its DCP, calories and nutrient totals for the list views. Whenever a food or recipe changes — editing a food's nutrients, bringing in amino acid data via "estimate it from a similar food," refreshing a food from [USDA](#gloss-usda), editing a recipe's ingredients — NuMa automatically recalculates DCP for every recipe that depends on the thing that changed, including recipes-of-recipes, all the way up the chain, and then every meal that logs any of them. You never have to trigger this yourself — see [Editing your data, and what changes as a result](#editing-consequences).

**System Issues is where NuMa tells you when that automatic recalculation itself broke.** This is not the same as a recipe showing "NC" (not computed) — NC just means DCP genuinely can't be calculated yet (a significant ingredient is missing amino acid data, or the recipe has 0 servings), which is an expected, normal state and isn't logged here at all. System Issues is specifically for the rarer case where the recalculation *should* have run and produced a real answer, but something went wrong internally (a software error) — the kind of failure that would otherwise silently vanish and leave a recipe's protein score stale with no indication anything was ever wrong.

Each entry shows when it happened, which recipe or meal it affects, and the error itself. Click **Retry** to have NuMa recompute it again right now:

- If the retry succeeds, the entry clears — you'll see a confirmation, and the recipe's DCP is now current.
- If it fails again, the entry stays (with a fresh error message) and NuMa tells you so — Retry never just makes an entry disappear while the recipe underneath it is still broken. A repeat failure usually means a real bug that needs fixing in the code, not something you can resolve by clicking around; consider reporting it.

If you'd rather fix the underlying recipe yourself instead of using Retry, re-editing it (or opening it and saving again) triggers the same recalculation that Retry does, and clears the System Issues entry the next time it succeeds.

A one-time banner also appears on the home page whenever there's a System Issues entry you haven't seen yet, with a **Got it. Don't remind me again.** checkbox — checking it hides the banner (the entry still stays listed under Settings until it's actually resolved), and any *new* failure after that brings the banner back.

**The home page also checks GitHub for a newer NuMa release**, showing an **UPDATE AVAILABLE** banner with a link to what's new if one exists, and its own **Don't show this again for this version** checkbox — same idea as the System Issues checkbox just above. This check is quick (a couple of seconds at most) and fails silently if you're offline or GitHub is unreachable — it never blocks the home page from loading. See [What you see on the home page](#home-page-tour) for exactly where the current build's version stamp and build note appear and how often the check itself runs.

**If you installed NuMa via the Linux installer, the banner also has an Update Now button** that downloads and installs the new version for you — no terminal, no manual download. Click it, confirm, and NuMa fetches the latest release and swaps itself in place; your data is completely untouched (it lives in a separate location the update never touches). You'll see a message telling you to close the browser tab and relaunch NuMa once it's done — the version you're currently running keeps working right up until you do. If you're running NuMa from source instead (a developer checkout), the button doesn't appear — you'll see the plain "what's new on GitHub" link instead, since there's no packaged install for it to replace.

### J. Entering custom foods and dietary supplements

Go to **Foods → Custom food profiles → Create**. See [Entering custom foods and dietary supplements](#custom-foods) in Part 6 for the fields, the supplement/tablet mechanism, and the barcode-first tip — they work identically here.

### K. A note on amino acid data {: #aa-note-web}

New foods are cached automatically the first time they turn up in a search, comparison, or pantry lookup — no separate import step needed. If a food is still missing amino acid data, you'll see a **Refresh** button (Food Cache) or a **Refresh from [USDA](#gloss-usda)** link (a meal's Protein Analysis section) to fetch it — both only [fill in what's missing unless you choose otherwise](#review-incoming) — and wherever data is missing you'll usually see a suggestion to search for a Foundation or [SR](#gloss-sr) Legacy equivalent instead. You can also enter [GI](#gloss-gi) or [DIAAS](#gloss-diaas) estimates yourself via **Foods → Annotate**.

---

## Part 4 — Core nutrition concepts {: #coreNutrition}

*(Reading time: 1 hour, 21 minutes)*

### A. Essential Amino Acids {: #aa}
Amino acids are the building blocks of protein. Nine of them are "essential", for our bodies cannot make them, so they must come from food every day:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and Phenylalanine respectively. NuMa evaluates [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr) as combined pairs when scoring protein quality, following [FAO](#gloss-fao) 2013 guidelines.

See [Protein Completeness](#complete) and [Amino Acid Gaps](#gap) for how completeness is scored and what a gap means.


### B. Protein Complement Suggestions {: #comp}
When amino acid gaps are detected, NuMa suggests foods that can improve the protein quality of the base food or meal. Two separate tiers are shown, and they use different methods:

#### WHEN DOES NUMA SUGGEST PROTEIN COMPLEMENTS? {: #comp-threshold}

The composite [DIAAS](#gloss-diaas) for a meal is defined as the lowest of the nine individual amino acid ratios — the ratio for the [limiting amino acid](#gloss-limiting-amino-acid). This means the meal [DIAAS](#gloss-diaas) and the complement-suggestion threshold are directly connected: if the meal [DIAAS](#gloss-diaas) is 0.95 or above, every single amino acid in the meal is also scoring 0.95 or above, and no suggestions will appear.

NuMa uses **0.95** as its threshold because gaps smaller than that are nutritionally trivial to close — the math works out to needing only a gram or two of additional food, which is not a practical suggestion worth presenting. A meal [DIAAS](#gloss-diaas) of 0.95–0.99 means the [limiting amino acid](#gloss-limiting-amino-acid) is present but slightly below the [FAO](#gloss-fao) ideal; the deficit is real but small, and the protein is considered of good quality for a varied diet.<sup>[FAO 2013]</sup>

Below 0.95, a meaningful gap exists, and NuMa will show complement suggestions — foods that supply the missing amino acid and, when added to the meal, raise the composite [DIAAS](#gloss-diaas) toward or above 1.0.

To summarize:

    Meal DIAAS  What it means                                    Complement suggestions
    ----------  -----------------------------------------------  -----------------------
    >= 1.00     All amino acids meet or exceed the reference     None -- protein is fully complete
    0.95-0.99   Minor limiting amino acid; negligible gap        None -- gap too small to address
    < 0.95      Meaningful amino acid gap                        Yes -- foods shown that close the gap

See also [Amino Acid Gaps](#gap) for the same 0.95 threshold applied per amino acid rather than at the meal-composite level.

The amino acid completeness categories NuMa uses are derived from the work of the Food and Agriculture Organization of the United Nations.[^16]

#### TIER 1 — GAP CLOSERS

These foods can mathematically close a specific amino acid gap with a practical amount (up to 300 g). A gap closer has a high enough ratio of the [limiting amino acid](#gloss-limiting-amino-acid) to protein that adding it to the base food brings that amino acid's score to 1.0 (the [FAO](#gloss-fao) reference floor).

Each suggestion shows:
  - Grams to add
  - Which gaps it closes, with scores before and after
  - Digestible protein added
  - Total bioavailable [complete protein](#gloss-complete-protein) — the base food protein plus the complement protein, multiplied by the combined (pooled) [DIAAS](#gloss-diaas) of the pair. This is higher than just adding each food's individually-digestible protein, because the complement's amino acids improve the usability of the base food's protein too.

#### RANKING

A **Sort by** dropdown above the list lets you pick how Tier 1 options are ranked:

  - **Greatest [DCP](#gloss-dcp) achieved** (the default) — the option that leaves the most total bioavailable complete protein after adding it.
  - **Most digestible protein added** — the option contributing the most digestible protein on its own, regardless of how well it targets the limiting amino acid.
  - **Greatest effect on amino acid gap** — the option closing the most amino acid gaps, then (as a tiebreaker) improving the limiting amino acid's score the most.
  - **Smallest addition (in grams)** — the option needing the fewest grams.

In every mode, one refinement applies: an option that fully completes the amino acid profile is always moved to the front of its tier, regardless of how many grams it takes. (Tier 3 two-food combinations, described below, apply a similar promotion but only when the combined serving is 50 g or less — see that section.)

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

Combinations are ranked by total weight (lighter is ranked first). A combination that closes all gaps is promoted to the front, but only when its combined weight is 50 g or less — a combination needing 90 g to close everything won't outrank a 30 g combination that only partially closes the gaps, which prevents a barely-adequate pairing from dominating the list just because enough of it eventually fixes everything.

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

A note on terminology: the [FAO](#gloss-fao) uses the term "indispensable amino acids" ([IAA](#gloss-iaa)) where this manual uses "essential amino acids" ([EAA](#gloss-eaa)) — both refer to the same nine amino acids. The "I" in [DIAAS](#gloss-diaas) stands for "Indispensable."

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

Even if all the protein is absorbed, it cannot all be incorporated into tissue unless every essential amino acid is present in sufficient proportion. The amino acid in shortest supply — the [limiting amino acid](#gloss-limiting-amino-acid) — sets a ceiling. [DIAAS](#gloss-diaas) is the ratio of that [limiting amino acid](#gloss-limiting-amino-acid) to the [FAO](#gloss-fao) reference level. If [DIAAS](#gloss-diaas) is 0.80, only 80% of the digestible protein can be fully used; the rest is broken down and converted to energy or excreted.

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

This cap note appears on the meal, full-day, recipe, and daily-summary [DIAAS](#gloss-diaas) sections.

See also [DIAAS](#diaas), [digestible complete protein](#dcp), [amino acid scoring](#aa-scoring).


### J. FAO 2013 Reference Standard {: #fao}
The [FAO](#gloss-fao) (Food and Agriculture Organization of the United Nations) published a reference amino acid scoring pattern in 2013 that defines the minimum amounts of each essential amino acid per gram of protein needed to meet adult human requirements. This is a ratio, not an absolute quantity — the requirement scales with how much protein you eat, so a small meal and a large meal must both hit the same per-gram proportions. See [Appendix A](#appendix-protein-quality) for the full worked explanation of why this ratio, not total protein, determines what your body can use.

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

See [Protein Complement Suggestions](#comp) for how NuMa suggests foods to close gaps, and [When does NuMa suggest protein complements?](#comp-threshold) for how this per-amino-acid gap threshold relates to the meal-level composite [DIAAS](#gloss-diaas) score.


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

#### Correcting a wrong match {: #oxalate-link-correction}

Since the match is automatic and name-based, it's sometimes wrong. A food's page marks an unconfirmed automatic match with "auto-matched — correct if wrong"; click that link to open a search page over the same Harvard reference table. Search for the right entry, select it, and save — or, if the food genuinely isn't in the Harvard table at all, choose "This food is not in the oxalate reference table" instead, which stops NuMa from re-matching it on future lookups. Either choice marks the food as user-confirmed, so the "auto-matched" warning won't reappear for it.

#### How to read a reference entry {: #oxalate-row}

Each candidate on that page is one row of the Harvard table, printed like this:

```
Spinach, Raw — 316.2 mg  / 1 cup  [very high]
Vegetables · measured in this food
```

* **316.2 mg / 1 cup** — the [oxalate](#gloss-oxalate) content of the serving *the table chose*, which is rarely 100 g. When that serving is a weight (usually ounces), the row also carries **= x mg/100g**, and NuMa can then scale the figure to whatever amount you actually eat. When it's a cup, a piece or a tablespoon, there is no per-100 g figure and none can be derived without knowing the food's density — such a row is flagged on the page as "per-serving only", and NuMa leaves that food out of recipe [oxalate](#gloss-oxalate) totals rather than guessing.

* **[very high]** — the band NuMa uses to colour the value. Thresholds are in the next section.

* **Vegetables** — the table's own food group (23 of them, from *Cold Cereal* to *Soups And Chowder*). It earns its place when two rows start the same way: "Bacon, Broiled, Pan-Fried, Or Roasted" sits under *Meat*, while "Bacon, Turkey, Microwaved" is under *Poultry*.

* **measured in this food** — whether this value was measured directly or estimated. See [Measured or estimated](#oxalate-measured).

Pick the row whose description best matches the food you actually eat — same preparation (raw vs boiled matters a great deal for [oxalate](#gloss-oxalate)), same form, same sort of product. A near-miss on the name with the wrong preparation is a worse match than a slightly different name with the right one.

#### What the categories mean {: #oxalate-categories}

NuMa bands every value into one of five categories, and colours it accordingly on a food's page. Where a per-100 g figure exists, the band comes from that:

| Category | Per 100 g |
|---|---|
| Very high | 300 mg or more |
| High | 100–299 mg |
| Moderate | 25–99 mg |
| Low | 5–24 mg |
| Negligible | under 5 mg |

Rows that have only a per-serving figure are banded on that figure instead, using a lower set of cut-offs — 100 mg or more for very high, then 26, 10 and 2 mg. The two scales aren't interchangeable, which is worth remembering when comparing a volumetric row against a weighed one.

For scale: anyone managing calcium-[oxalate](#gloss-oxalate) kidney stones is typically advised to stay under 40–50 mg of total [oxalate](#gloss-oxalate) a day, so a single "very high" serving can exceed a day's allowance on its own. For everyone else the categories are best read as a guide to which foods are poor calcium sources rather than as a budget.

#### Measured or estimated {: #oxalate-measured}

The Harvard table marks some values with an asterisk to say they were **measured directly** in that food; the rest were **estimated** from measurements of a similar food. NuMa shows which is which on both the match page and the food's own page (235 of the 433 entries are direct measurements).

An estimated value is still worth having — it's a reasoned inference by the people who compiled the table, not a guess — but it carries more uncertainty than a measured one. When two candidate rows fit your food about equally well, the directly-measured one is the better pick.

#### What NuMa saves from a match {: #oxalate-what-is-stored}

Saving on the match page records your choice of reference entry against that food, marked as confirmed by you. Two consequences: the "auto-matched" warning stops appearing, and NuMa never re-runs name-matching for that food, so your choice can't be silently replaced later.

Choosing "This food is not in the oxalate reference table" is saved the same way, and means the food contributes no [oxalate](#gloss-oxalate) figure at all — which is the honest outcome when nothing in the table matches, and better than carrying a wrong number into every recipe total the food appears in.

Note that this is *your* map from food to reference row, stored in your own [database](#gloss-database). The Harvard table itself is a bundled read-only file that NuMa never writes to, so nothing you do here changes the reference data — only which row your food points at.

#### Important limitations

- [Oxalate](#gloss-oxalate) values in the Harvard table are reported per serving, not per 100 g. For foods measured in ounces (fish, nuts, meat), NuMa automatically converts to per-100g. For foods measured in cups, pieces, or tablespoons, only the per-serving value is available. Volumetric servings cannot be converted to per-100g without knowing the food's density — that conversion must be done manually if needed.

- For recipe analysis, NuMa sums [oxalate](#gloss-oxalate) only for ingredients where a per-100g value is available. Volumetric-only items are excluded from the total and noted as such.

- [Oxalate](#gloss-oxalate) content varies with preparation method (cooking reduces [oxalate](#gloss-oxalate) in spinach, for example) and growing conditions. All values should be treated as estimates.

- Matching by food name is approximate. "Spinach, raw" in the Harvard table maps reasonably to [USDA](#gloss-usda) spinach entries, but processed or branded foods may not match well. Always verify the match makes culinary sense before confirming it.

For background on [oxalates](#gloss-oxalate) and kidney health, see the Harvard Health references in the source data (Settings -> [Oxalate](#gloss-oxalate) data for data provenance).


### N. Glycemic Index {: #gi}
The glycemic index ([GI](#gloss-gi)) measures how quickly a carbohydrate-containing food raises blood glucose compared to pure glucose ([GI](#gloss-gi) = 100). Low-[GI](#gloss-gi) foods (55 or below) produce a slower, more gradual rise; high-[GI](#gloss-gi) foods (70 and above) cause a faster spike.

**Every [GI](#gloss-gi) figure NuMa shows is one you put there.** Nothing looks [GI](#gloss-gi) up automatically, because no nutrient [database](#gloss-database) NuMa draws on carries it — so a food shows a [GI](#gloss-gi) if, and only if, you supplied one, either by typing it in or by picking a row from the bundled reference table (see [Where GI values come from](#gi-source-para) below). Choosing which published value fits a food is a judgment call, and it stays yours; NuMa won't make it for you. Once saved, the value appears in the **GI** column wherever that food is listed — Food Cache, Pantry, food search, a meal's add-food panel — on the food's own page, and in any glycemic load NuMa computes from it.

**What it's good for.** [GI](#gloss-gi) is at its most reliable comparing like with like, where the two foods differ in one respect you're choosing between — this bread against that bread, parboiled rice against sticky rice. But it is genuinely useful across categories too, whenever two foods are candidates for the same job: bread and rice at breakfast really do behave differently, largely because of physical form, and [GI](#gloss-gi) is what tells you so. What *doesn't* survive the comparison is quantity. [GI](#gloss-gi) is measured on a fixed dose of available carbohydrate (usually 50 g) rather than on a serving of food, so two foods with the same [GI](#gloss-gi) can have very different effects at the amounts you'd actually eat. That's what glycemic load is for — see [Glycemic Load](#gl).

**What it doesn't capture.** [GI](#gloss-gi) describes a food eaten alone. Combining foods in a meal (especially adding fat, protein, or fiber) physiologically blunts the blood glucose response to the carbohydrates present, by slowing gastric emptying and glucose absorption. However, this effect is not fully captured by glycemic load ([GL](#gloss-gl)) either — see [Glycemic Load](#gl) for why.

NuMa displays [GI](#gloss-gi) for reference only and does not use it in protein quality calculations.

**Where [GI](#gloss-gi) values come from.**{: #gi-source-para} Neither [USDA](#gloss-usda) nor Open Food Facts[^3] tracks [GI](#gloss-gi), so NuMa can't look it up automatically the way it does for calories or protein — you have to supply it, but NuMa makes that easy. Every food's [Food Cache](#food-cache-web) → **Annotate** page has a **"Look up a GI value from the published reference table"** section: type the food's name (already pre-filled for you), pick which subject population you want — normal glucose tolerance, impaired glucose tolerance/diabetes, or both — and NuMa searches the full published reference table[^8] — about 2,500 foods as shipped, or over 4,000 if you [add the newer edition](#gi-editions) — and lists every plausible match, not just its single best guess. Click **Use this GI value** next to whichever one actually matches your food and its value fills the [GI](#gloss-gi) field; nothing is written until you save the annotation.

The first time you add a new food to your Pantry or a meal, NuMa also offers to prompt you for its [GI](#gloss-gi) value right there, so your data builds up naturally through normal use even without visiting Annotate directly.

#### Normal and impaired — which people a value was measured in {: #gi-populations}

Every search result is labelled with the subject group the value was actually measured in, taken from that row's own entry in the table[^8] rather than inferred from anything else:

* **Normal glucose tolerance** — ordinary healthy volunteers. This is the bulk of the table and the default assumption behind any [GI](#gloss-gi) figure you see quoted anywhere.

* **Impaired glucose tolerance** — people with type 1 or type 2 diabetes, gestational diabetes, or diagnosed impaired glucose tolerance. Where the table gives the number of subjects, NuMa shows that too (`Type 2, n=9`), because a nine-person study and a thirty-person study do not deserve equal weight.

* **Subject group not stated** — the table didn't record who the value was measured in. These appear in *both* the normal and impaired lists rather than being hidden from both, since a value with an unrecorded population is still a real measurement; the label tells you to treat it cautiously.

**If you have normal glucose tolerance**, prefer a normal-tolerance result whenever one exists for your food. Use an impaired one when it's all there is, and treat it as a rough indication rather than a number to plan around.

**If you have diabetes, pre-diabetes or insulin resistance**, the impaired-tolerance values are the ones measured in people like you, and are worth preferring where they exist. See also the [GI](#gloss-gi) caveats in [Appendix C](#appendix-gl-comparison).

By default the lookup searches both populations at once. If you'd rather it default to just one — say, you have diabetes and always want the impaired-tolerance values shown first — set **Glycemic index lookup default** under [Settings](#settings). You can still switch populations for any individual lookup regardless of that default.

#### Method quality, and why some rows are flagged {: #gi-method-quality}

Subject group is one axis; how well the study was run is a separate one, and the table[^8] splits its rows on exactly that. There is an international standard for measuring [GI](#gloss-gi) — [ISO](#gloss-iso) (International Organization for Standardization) 26642:2010 — which sets out how much carbohydrate the test portion must contain, how many people must be tested, and when blood must be sampled.

* Rows from studies that **met** that standard carry no flag. They are the bulk of what you'll see, and they are the ones to trust.

* Rows from studies that **deviated** from it are marked **non-ISO method**. The deviation might be fewer than ten subjects, a test portion with an unusual amount of carbohydrate, an unrepeated reference food, or results whose [standard error](#gloss-standard-error) was wide enough that the average is shaky.

A **non-ISO method** flag is not a warning about the food — it's a warning about the *evidence*. Be especially wary when a flagged value looks extreme, since an implausibly low or high figure is exactly what a tiny or high-variance study tends to produce.

Note that the two things are genuinely independent: most non-ISO rows were still measured in normal-tolerance subjects, and an unflagged row can still have been measured in people with diabetes. That's why NuMa shows them as two separate pieces of information rather than rolling them into one tag.

#### How to read a lookup result {: #gi-result-row}

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

#### What NuMa keeps from a lookup {: #gi-what-is-stored}

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

#### Upgrading to the 2021 tables {: #gi-editions}

NuMa ships with the **2008** edition of the *International Tables of Glycemic Index and Glycemic Load Values*[^8a] — about 2,500 foods. A **2021** edition[^8] exists with over 4,000, and it carries information the 2008 one doesn't: the year each study was run, its [standard error](#gloss-standard-error), the country the food came from, how many people were tested, and whether the study met the international measurement standard.

NuMa can't ship that newer edition, for a straightforward reason. The 2008 edition is Creative Commons licensed, so it can be copied and distributed freely, which is why it's the one built in. The 2021 edition is published under a licence that expressly **permits you to download it and extract data from it for your own non-commercial use**, but **forbids redistributing it**. So NuMa includes the tool that reads it, and you supply the document — which the licence entitles you to do.

**What to do** — it's all in one place, **Settings → 11. Glycemic Index Reference Table**:

1. Open the 2021 article's page at the publisher[^8] (the section links straight to it), find its **Supplementary data** section, and download both PDFs there — Supplemental Table 1 and Supplemental Table 2. NuMa can't fetch them for you: the publisher's site turns away programs, and only a person can collect them.
2. Back in that Settings section, choose both files together (hold Ctrl, or Shift, to pick the second one). The order doesn't matter — NuMa reads which table is which from the PDFs themselves.
3. Click **Build my 2021 GI table**.

It takes about a minute. The section shows a "Building…" message and refreshes itself until it's done, then says how many foods it read. From then on the Annotate page's [GI](#gloss-gi) lookup searches the new table, straight away, with no restart. The PDFs aren't kept, only the table built from them. If you pick the wrong files — the same table twice, or some other document — NuMa says so and changes nothing, and if you already had a 2021 table it stays in use. To rebuild later (a fresh download, say), the same button is there, relabelled **Rebuild**.

That file is yours alone. It isn't shared, uploaded, or included in anything NuMa distributes, and it shouldn't be passed on to anyone else — the same licence that lets you build it is what stops it being handed around.

**What you'll see afterwards.** Results gain a date and the other detail described in [How to read a lookup result](#gi-result-row). A few hundred foods that appear only in the 2008 edition are kept alongside the newer ones, labelled **2008 edition**, so nothing is lost in the upgrade. Those carry no year, standard error or country, because that edition never published them in a form NuMa captured.

One honest caveat about that set: the 2021 authors rewrote most food descriptions — moving brand names around, adding cooking detail — so deciding which 2008 foods 2021 *doesn't* already cover means comparing reworded descriptions, with no shared identifier to match them by. NuMa deliberately errs toward keeping a 2008 row when it can't tell. The cost is the occasional near-duplicate pair in your results, one of them without a date; the cost of the opposite choice would be silently losing foods. If you see such a pair, take the 2021 one.

#### Why these tables instead of the University of Sydney database {: #gi-why-foster-powell}

Two candidate sources exist for bulk [GI](#gloss-gi) data, and they're related but not the same. Brand-Miller — a co-author of the published tables[^8] — also runs the University of Sydney's GI research group, and a great many entries in those tables came from the Sydney group's own lab testing, so there's real lineage and overlap between the two.

But they differ in ways that matter for a bulk local lookup table. The published tables are a fixed, peer-reviewed, citable snapshot: a static document that can be read into a file once and then work offline and identically every time — and in the 2008 edition's case, explicitly Creative Commons licensed, so NuMa can ship it outright. The Sydney [database](#gloss-database) (glycemicindex.com) is a live, continuously updated, searchable website — larger and more current, but a site to query rather than a table with a clear bulk-redistribution license; scraping it for a local table would be a licensing gray area at best.

That's why NuMa's built-in table comes from the published tables, and why glycemicindex.com is listed in [Internet resources](#internet-resources) as a manual look-up fallback rather than something NuMa imports from directly.

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

**[GL](#gloss-gl) is read on two different scales, and mixing them up is the commonest way to misread the number.** A single food, serving, meal or recipe portion goes against the per-serving scale:

| Per-serving [GL](#gloss-gl) | Classification |
|---|---|
| 10 or below | Low |
| 11–19 | Medium |
| 20 or above | High |

A whole day's total is a much larger number and goes against its own scale:

| Daily total [GL](#gloss-gl) | Classification |
|---|---|
| Below 80 | Low |
| 80–120 | Moderate |
| Above 120 | High |

**Treat that second table more loosely than the first.** The per-serving bands are the ones published with the international [GI](#gloss-gi) tables and are well established. The daily bands are a widely-repeated convention rather than a clinically validated target, and expert groups define them inconsistently — the University of Sydney group, for instance, describes a daily [GL](#gloss-gl) under 80 per 2,000 kcal as a *moderate* diet rather than a low one. A day's [GL](#gloss-gl) also rises with how much you eat, so a large or very active person naturally runs higher without that meaning anything is wrong. NuMa shows the daily band for orientation, and repeats this caveat underneath it every time.

NuMa displays [GL](#gloss-gl) in the nutrient summary alongside [GI](#gloss-gi) when carbohydrate data is available, and on a food's own page it shows the [GL](#gloss-gl) of the exact portion you are analyzing — halve the portion and the [GL](#gloss-gl) halves with it while the [GI](#gloss-gi) stays put, which is the whole point of the measure. Like [GI](#gloss-gi), it is shown for reference and does not affect protein quality calculations.

**Averages beat single days.** A single day's [GL](#gloss-gl) swings with whatever happened to be eaten. **Summary → Trend** shows your average daily [GL](#gloss-gl) across the last 7, 14 or 30 days, and the [Nutrient Plot](#nutrient-plot) offers **Daily glycemic load** as a plottable series so you can see the pattern — weekends, late evenings, stressful weeks — instead of a snapshot. Both skip any day whose [GI](#gloss-gi) coverage is incomplete rather than counting it as a low day, and both tell you how many days actually contributed.

For a discussion of how [GL](#gloss-gl) compares to other approaches for evaluating the blood glucose impact of different meal choices — particularly relevant for people managing diabetes — see [Appendix C: GL and Blood Glucose Comparison](#appendix-gl-comparison).


### P. Recommended Dietary Allowances {: #rda}
[RDA](#gloss-rda) values in NuMa come from the Dietary Reference Intakes ([DRI](#gloss-dri)) published by the U.S. National Academies of Sciences, by way of the **NIH** (National Institutes of Health) **ODS** (Office of Dietary Supplements)[^9]. Here is the ODS's own definition, word for word:

> "Recommended Dietary Allowance (RDA): Average daily level of intake sufficient to meet the nutrient requirements of nearly all (97–98%) healthy individuals[^9]."

**Read that carefully — an RDA is not a bare-survival minimum.** It's set high enough that following it meets the needs of nearly everyone in your age/sex group, with margin built in. (The government's actual bare-minimum figure, the amount that meets only the *average* person's need with no safety margin, is called the EAR — Estimated Average Requirement — and NuMa doesn't use it for anything, since it's a population-statistics tool, not a personal target.) NuMa still labels this tier "minimum" in a few places in the interface — meaning "meet or exceed this amount," a directional instruction, not a claim about how large the number itself is — see the color-coding note below and [Daily Nutrient Goals](#goals) for exactly what "minimum," "target," and "limit" each mean as goal types.

When you set a user profile (Settings → User profile), NuMa uses your age, sex, weight, height, and activity level to estimate personalized targets — see [Daily Nutrient Goals](#goals) just below for the age/sex bands behind every mineral and vitamin RDA, not just the two formula-based ones (calories, protein) described here. The calorie estimate uses the Mifflin-St Jeor equation with an activity multiplier. The protein target uses 0.8 g per kg body weight as a baseline minimum, rising to 1.0 g/kg at moderate activity and 1.2 g/kg for active and very active people. That 0.8 g/kg figure comes from nitrogen-balance research underlying the 1989 RDA and the 2005 Dietary Reference Intakes of the **IOM** (Institute of Medicine, the US body that sets these figures; renamed the National Academy of Medicine in 2015)[^60] — and it carries an assumption that matters a great deal to anyone eating mostly plants. The next few paragraphs explain it.

#### The protein target assumes high-quality protein {: #protein-rda-quality}

The **IOM** (Institute of Medicine)[^60] sets 0.8 g/kg for protein **"of mixed quality as typically consumed"**[^60] — meaning the ordinary American diet the research was based on, in which most protein comes from animal sources and is close to completely digestible and complete in its amino acids. The number was never meant to be read as "any 0.8 g/kg of anything." The IOM says so directly, noting that requirements may be higher for diets built on less-digestible plant proteins, and [FAO](#gloss-fao) and the **WHO** (World Health Organization) recommend correcting for protein quality whenever a diet is predominantly plant-based.

Put another way: **the protein target is quietly denominated in reference-quality protein.** And reference-quality protein is precisely what [Digestible Complete Protein](#dcp) measures — protein that is both fully digestible and complete in its essential amino acids. So the honest comparison, for everybody, is [DCP](#gloss-dcp) against the target, not raw grams against the target.

For someone eating meat, eggs and dairy this changes almost nothing. Their pooled [DIAAS](#gloss-diaas) sits near 1.0, so their DCP and their raw protein are nearly the same number and either comparison gives the same answer. That is exactly why the assumption stayed invisible for decades. For someone eating mostly or entirely plants, the two numbers separate — and the raw-gram comparison flatters the result, sometimes badly. A day can show 120% of the protein target on raw grams and under 90% on the protein you can actually use.

**This is why NuMa shows both.** In the nutrient comparison table, the **Protein** row gives your raw intake against the target, and the **(Digestible Complete Protein)** row directly beneath it gives your usable intake against *that same target*. Reading down those two rows tells you, in one glance, how much your protein quality is costing you. The Protein Summary panel on the same page leads with the DCP figure for the same reason.

**There is no separate rule for vegetarians or vegans, and deliberately so.** You might expect NuMa to raise the protein target for a plant-based diet, the way it raises the iron and zinc targets (see [Diet-Aware Bioavailability](#diet-bioavailability)). It doesn't need to. Iron and zinc need that treatment because their absorption penalty is invisible in the nutrient data — a milligram of iron looks identical whatever food it came from. Protein's penalty is not invisible: it *is* the [DIAAS](#gloss-diaas) score, already measured from your actual foods and already built into DCP. A vegetarian eating both plant and animal protein needs no special rule either, because the pooled meal calculation (see [How NutriMagnus scores meal and recipe protein quality](#protein-scoring)) works out the real quality of whatever mixture they actually ate. Raising the target on top of that would count the same penalty twice.

One caveat worth keeping in view: DCP can only be computed from foods that have amino acid data. When some of your foods don't, NuMa marks the DCP row with an asterisk and names the foods it had to leave out, so you know the figure is an understatement rather than the whole story. See [A note on amino acid data](#aa-note-web) for how to fill those gaps.

The nutrient comparison table (shown on food, recipe, meal, and daily-summary pages) shows your intake compared to your targets.

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
                           such goal in Settings → 7. Nutrient Targets; a dash
                           means none is set for that row (see <a href="#optimal">Revised
                           Optimal Targets</a>).
    UL                    Shown only where you're near or over a max limit —
                           see <a href="#maxlimits">Maximum Nutrient Limits</a>.
</pre>

**Reading the two protein rows.** Directly beneath the **Protein** row sits an indented **(Digestible Complete Protein)** row. It is the only place in this table where one nutrient gets two lines, and the two are meant to be read together: same target, same % column, different intake figure. Protein is the raw grams the food data reports; DCP is how much of that your body can actually use, after digestibility and amino acid completeness. The wider the gap between their two percentages, the more your protein quality is costing you — see [The protein target assumes high-quality protein](#protein-rda-quality) for why both are measured against the same goal. An asterisk on the DCP row means one or more of your foods had no amino acid data and had to be left out; a footnote below the table names them, and the real figure is higher than shown.

One column stays blank on the DCP row: **day total %**, on pages that have it. A day's DCP is not the sum of its meals' DCP figures — foods eaten in different meals can still complement each other's amino acids, which a simple sum would miss — so NuMa declines to put a number there rather than show a misleading one. For a whole day's DCP, use the [Daily summary](#analysis-menu-web), where it is calculated properly across everything you ate.

Minimum, Target, and Maximum are mutually exclusive for any one nutrient — each nutrient's [DRI](#gloss-dri) is exactly one of the three kinds, so only one of those three columns is ever filled per row, and the other two show "—". A footer note under every nutrient table spells out each of the four (Minimum, Target, Maximum, UL) with a link back here.

The color coding on % of daily target (and % of Revised Optimal) uses four colors throughout the app: **green** — met (at or above a Minimum, or a comfortable range around a Target); **blue** — near (approaching a Minimum from below, or drifting outside a Target's comfortable range) — a reassuring, "almost there" state, not a warning; **orange** — below minimum (well short of a floor-type nutrient like protein or a vitamin, where more is always fine) — a genuine shortfall, so it gets the warning color; **red** — over the limit (past that nutrient's own Maximum — currently only sodium is set up this way — or, for a Target-type nutrient like calories, far enough over 100% that it's no longer close to the target). A short color legend appears right below any table using these colors.

**Maximum vs. [UL](#gloss-ul) — two different ceilings, easy to conflate.** The Maximum column (sodium today) is that nutrient's own recommended not-to-exceed amount — a lower, more clinically conservative figure than a Tolerable Upper Intake Level. The separate **UL** column (below) is a different thing: the highest amount considered safe for nearly everyone, not a target to actively stay under the way Maximum is. The two never overlap on the same nutrient — sodium has a Maximum figure but no UL column entry, and every nutrient with a UL column entry has no Maximum figure — so you'll never see both filled for one nutrient, but it's worth knowing which one you're looking at. See [Maximum Nutrient Limits](#maxlimits) for the UL column in full.

Nutrients without an established Dietary Reference Intake ([phytonutrients](#gloss-phytonutrients), amino acids) are shown without a % of [RDA](#gloss-rda) figure -- those rows show only the Total amount.

See [daily nutrient goals](#goals) for a full explanation of how each goal is calculated.


### Q. Daily Nutrient Goals {: #goals}
NuMa calculates personalized daily nutrient goals from your user profile (Settings → User profile). Each goal is one of three types:

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
<pre>
    1600 mg/day men, 1100 mg/day women — Adequate Intake for alpha-linolenic
    acid (<a href="#gloss-ala">ALA</a>), the plant-sourced omega-3. See <a href="#omega3">Omega-3 Fatty Acids</a>
    for why this is the only omega-3 with an official goal in NuMa.
</pre>

#### Minerals and vitamins — every age/sex band, in full

All minerals and vitamins use age- and sex-specific values from the Dietary Reference Intakes published by the U.S. National Academies of Sciences[^9]. If your profile's sex is set to "other," NuMa uses the midpoint of the male and female values — except for the handful of nutrients marked below, where the underlying [DRI](#gloss-dri) tables don't publish a distinct value for anything other than male/female, so "other" uses the same value as female.

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

See [RDA](#rda) for a general overview of where these values come from. If the standard [RDA](#gloss-rda) isn't the number you actually want to hit for a given nutrient, see [Revised Optimal Targets](#optimal). If you want to be warned as you approach a personal daily cap, see [Maximum Nutrient Limits](#maxlimits). A single day's numbers are only a snapshot -- see [Nutrient Averages Across Days](#trend) for how to spot a shortfall that persists across many days. For a plain-language description, deeper reading, and outside sources on any individual nutrient by name, see the [Full Nutrient Key](#nutrient-key) (Appendix G).


### R. Nutrient Averages Across Days {: #trend}
Every other [RDA](#gloss-rda) comparison in NuMa -- food, recipe, meal, daily summary -- looks at a single day. That's the right window for "did today's meals cover me," but it's the wrong window for a nutrient that's chronically a little short: one low day is unremarkable, but the same shortfall repeated for two weeks straight is exactly the kind of pattern a single-day view can never show you, because you'd have to remember and compare each day yourself.

**Access it via the "Nutrient averages across days" button on the Daily Summary page.** Choose a window -- last 7, 14, or 30 days -- and NuMa averages your total intake for every tracked nutrient across the days in that window that actually had a meal logged, then compares that average against your RDA (and Revised Optimal / max limits, if configured) using the exact same table, color coding, and diet-aware notes as the daily comparison.

**Only logged days count.** If you ask for a 30-day average but only logged meals on 12 of those days, the average is computed over those 12 days -- unlogged days are treated as "no data," not as a zero-intake day. Diluting the average with days you simply didn't track would understate your real intake and could hide the exact shortfall this view exists to surface. The screen tells you how many logged days went into the average (e.g. "Averaging over 12 logged day(s) out of the last 30").

This is the same B12/iron/zinc-aware analysis described in [Diet-Aware Bioavailability and Deficiency Notes](#diet-bioavailability) -- this averaged view is often where a B12 or iron pattern actually becomes visible, since a single low day rarely triggers concern on its own.

This view does not offer protein complement suggestions -- complementation only matters within the roughly 24-hour window your body actually digests and pools amino acids together, so a suggestion pooled across a week or more of eating isn't something you could act on. For an actionable complement suggestion, use [Protein Complement Suggestions](#comp) on a specific day's summary, a meal, or a recipe.


### S. Nutrient Plot {: #nutrient-plot}
A line plot of one or more nutrients across your logged days, day on the x-axis — useful for spotting a trend visually rather than reading a column of numbers.

**Access it from Analysis → Daily Summary → "Nutrient plot".** Check up to 8 nutrients from the full nutrient list (any nutrient NuMa tracks, not just the ones you've chosen as Meals & Log columns, plus Day [DCP](#gloss-dcp) itself) — Protein, Calories, Carbs, and Fiber are listed first; the checkbox list scrolls vertically below them. **Clear all nutrient checkmarks** above the list unchecks every box in one click, a faster starting point than unchecking a previous selection one at a time when you want to plot a completely different set. Then choose which days to include:

    (blank days-back)         Every logged day, oldest to newest.
    Days back + Ending on     The N days ending on the date you pick
                              (defaults to your most recent logged day).

**Every logged day appears, whether or not its meals are marked complete.** A day with no logged meal at all shows as a **break in the line**, not a false drop to zero, and the line picks up again at the next day with data; a note under the plot says how many such days its span has. Completeness only comes into play through "Always end on last complete day" below.

**Goal and limit reference lines.** Any chosen nutrient with a profile target automatically gets one or two flat horizontal lines drawn across the plot, in that nutrient's own color, so you can see at a glance whether your actual day-to-day intake is tracking toward — or drifting past — where you want it: a **dashed** line for its goal (your [Revised Optimal](#optimal) target if you've set one, otherwise its [RDA](#gloss-rda)/[AI](#gloss-ai)) and a **dotted** line for its maximum limit (a built-in [Tolerable Upper Intake Level](#maxlimits), or your own configured cap if you've set one). Nothing to turn on — just pick a nutrient that has a goal and/or limit set and the line(s) appear; a nutrient with neither configured plots with no reference line at all. A small note under the plot's title spells out which dashed/dotted lines are present.

**Always end on the last complete day.** Checking this box next to the home-page toggle stops "Ending on" from freezing at whatever date was current when you last saved the plot — instead the end date always slides forward to the most recent day whose meals are all marked complete, automatically, which can be today once you've marked today's meals complete. Useful for a Home page plot in particular, since without it the plot would otherwise stay stuck on its original end date until you revisited this page and re-saved it. With this box checked, an earlier day with an incomplete meal is **left out** too, as a break in the line, so a partly logged day can't drag the line down; the note under the Home page plot says how many days that is. If every day in the plot's range has an incomplete meal, there's nothing to draw, and the page says so instead.

**Date labels thin out automatically on a long plot.** Every plotted day still gets a data point, but once there are more than 18 of them, showing every single date's label would crowd them into an unreadable jumble, so only every 2nd, 3rd, etc. date is labeled (always skipping at least one), spaced out enough to stay legible.

If you pick nutrients with different units (e.g. Protein in g alongside Sodium in mg), they still plot together on one y-axis. In that case the y-axis shows no title or numbers at all — once nutrients are on different scales, no single number on a shared axis means the same thing for every line, so printing one would just be misleading. The gridlines are still there for a rough sense of relative up-and-down movement; each line's real values live in its own legend entry instead. Plotting a single nutrient, or several that share a unit and didn't need any scaling, still shows a normal, meaningful numbered axis.

**Scaling happens in two steps, both of which you can override.**

*Step 1 — Scale factor.* If one nutrient's numbers dwarf another's (e.g. Calories next to Protein, or Calcium next to Protein), the smaller one would flatten into a barely-visible wiggle along the bottom. NuMa automatically divides every plotted nutrient except the least up-and-down one by a computed **Scale factor** — a number based on how much each nutrient's values swing over the plotted days — which brings a dominant nutrient's swings down to roughly match the smallest one's. The **Scale factor** field shows this computed value as a placeholder (grayed, e.g. "3.5") and is left blank by default, meaning "use that computed value." Type your own number and click Plot to override it.

*Step 2 — Per-nutrient factors.* A single shared Scale factor can't perfectly equalize more than two nutrients at once — with three or more plotted, one can still end up nearly flat even after step 1. NuMa checks each nutrient again after step 1 and sets a floor at 25% of the most up-and-down nutrient's swing; anything still below that floor gets its own individual multiplier (shown as "×2.4" etc. in its legend entry) to bring it back up to a visibly readable wiggle. Each chosen nutrient gets its own **Per-nutrient factors** field, prefilled the same "blank = use the computed value" way as Scale factor — type a number to override just that one nutrient.

**Highlight nutrient.** Pick which one nutrient always draws solid and (in color mode) red, so the figure you're usually comparing everything else against stands out at a glance — defaults to Day DCP whenever it's one of the chosen nutrients.

**Black & white (printer-friendly).** Check this to preview the plot the way it'll look on a printer that can't print color: every line drawn in black, with the highlighted nutrient solid and every other nutrient in its own dash pattern (dashed, dotted, dash-dot, etc.) instead of a color, so lines stay distinguishable without color at all. The on-screen plot updates the instant you check or uncheck the box — no need to click Plot — so you can compare both looks side by side before deciding.

**Smoothing.** Day-to-day values can be noisy enough to obscure the underlying trend. The **Smoothing (days)** field averages each point with its preceding days — a trailing moving average — to smooth that out; it defaults to 3 days. Set it to 0 to turn smoothing off and see the original, unsmoothed data. A smoothed nutrient's own scaling (steps 1 and 2 above) is calculated from the smoothed data, since that's what's actually on the plot. **Missing days don't shrink the average.** Smoothing uses the days that have data, as if the missing ones weren't there: with 3-day smoothing, a point just after a break averages itself with the two days with data before it, however far back they are. **The first days plotted are smoothed like the rest.** Each point averages its own day with the logged days *before* it, and for the first few days plotted, some of those come from before the plot's start date: NuMa reads them for the averaging but doesn't draw them, so every point, the first included, is averaged over the same number of days. A note under the plot (here and on the Home page) says so, and from which date. If you haven't logged that many days before the plot starts (say, the plot begins with your very first logged day), the first few points are averaged over fewer days and can swing more than the rest of the line; the note then says how many points that affects, so you can read the start of the plot with that in mind.

**Plot title.** Defaults to "Key nutrients, {start date} to {end date}" for whatever range is currently plotted, shown right on the plot itself. Edit the **Plot title** field and click Plot to use your own instead.

**Legend placement.** The legend — the list naming each colored line — is always wrapped horizontally rather than stacked in a tall column, so it never overlaps a data line and stays compact and print-friendly. Where it sits is up to you:

- **Auto (above if it fits)** — the default. The legend goes just below the title and the note about dashed and dotted reference lines while it still fits on a single row (up to four nutrients), and drops below the plot once it would wrap onto two or more rows. A wrapped multi-row block above the plot squeezes the plot itself and reads as a heavy header, which is the case below-the-plot placement handles better.
- **Always above the plot** — keeps it under the title no matter how many nutrients you've picked. The plot area shrinks a little to make room.
- **Always below the plot** — keeps it under the plot no matter how few.

Like Black & white, the on-screen plot updates the instant you change this — no need to click Plot. The setting travels with the plot too: into the print view, a downloaded PNG or SVG, and the Home page copy if you've put this plot there.

**Print or save it.** "Print / Save as [PDF](#gloss-pdf)" opens a stripped-down, print-friendly page with the plot and your browser's print dialog. "Download [PNG](#gloss-png)" and "Download [SVG](#gloss-svg)" save the plot as an image file — see [Plot File Formats](#plot-file-formats) for which one to pick.

**Show this plot on the Home page.** Once you've plotted something, a "Show this plot on the Home page" checkbox appears next to the Plot button. Check it and that exact plot (same nutrients, range, and styling, at a slightly smaller size) shows up near the top of the Home page every time NuMa opens, with an "Edit this plot" link back here. Only one plot can be shown this way at a time — checking a different plot's box replaces whichever one was showing before. Your Nutrient Plot settings (which nutrients, date range, scaling, ...) are remembered automatically the next time you visit this page, even after closing and reopening NuMa — a "Reset to defaults" link appears whenever that happened, in case you'd rather start over.


#### Plot File Formats — PNG vs. SVG {: #plot-file-formats}
Both "Download [PNG](#gloss-png)" and "Download SVG" save the same plot as an image file you can keep, email, or paste into a document — they just store it differently.

**PNG** is a normal photo-style image, a fixed grid of pixels. It opens everywhere without a second thought, and is the safer default if you're not sure what a document or website will accept.

**[SVG](#gloss-svg)** stores the plot as the shapes and lines that drew it, not pixels — so it stays perfectly crisp at any size, whether you zoom way in on screen or print it on a large sheet of paper. PNG images can look blurry or blocky if enlarged; an SVG never will. The trade-off is that a few older programs don't open SVG files directly (most current web browsers, word processors, and image editors do).

**Rule of thumb:** downloading to look at, email, or drop into a typical document — PNG. Need to print it large, or want it to stay sharp if someone else resizes it — SVG.


### T. Per-Day Profile Tracking {: #day-profile}
Your profile isn't fixed forever -- weight, activity level, or even which named profile is active can change over time (illness, travel, a deliberate weight change). But your logged meals stay put. If a past day's [DCP](#gloss-dcp) and RDA comparisons always used *today's* profile, an old day could silently get re-scored against numbers that weren't true of you back then.

**Each logged day is pinned to whichever profile was active the first time a meal was saved for that date.** That pin is a full snapshot -- your age, weight, activity level, and targets as they were that day -- not just a name. So if you later edit that profile's numbers (or switch which profile is active), days already logged keep comparing against the numbers that were true when you logged them. Only a day that has never had a meal saved for it — or one you explicitly reassign — will pick up a different profile.

**Where you see it.** If you maintain more than one named profile, a **Profile** column/line appears next to each day: on the Meals & Log list, the Recent Days list, and the Daily Summary / full-day view. With only one profile configured, this column is hidden since there's nothing to distinguish.

**Changing a day's profile.** Sometimes the automatic pin doesn't match reality -- illness or travel rarely starts exactly at midnight. Open that day's summary and use the **Change** control next to "Profile:" (on the day's Summary or Full Day page) to pick a different saved profile. The day is marked "(manually set)" afterward and its DCP/[RDA](#gloss-rda) numbers recompute immediately against the new pin.

**Nutrient averages across days.** The [Nutrient Averages Across Days](#trend) view spans many days at once, so it scores against the profile pinned to the *most recent* day in the window (today, for the usual "last N days"). If any day inside the window was pinned to a different profile, a note discloses which dates and profile differed, rather than silently blending two profiles' targets into one average.

**Existing data.** If you're upgrading from a version of NuMa that didn't have this feature, every day you'd already logged gets pinned to whichever profile is active the first time you open NuMa after upgrading -- you don't need to open or edit anything for this to happen.


### U. Omega-3 Fatty Acids {: #omega3}
NuMa tracks four omega fatty acids: [ALA](#gloss-ala), EPA, and DHA (all omega-3), and linoleic acid (omega-6). Only one of these four -- ALA -- has an official Adequate Intake, so it's the only one that appears as a Daily Goal: 1600 mg/day for men, 1100 mg/day for women.

**Why not a goal for [EPA](#gloss-epa) and DHA directly?** No U.S. Dietary Reference Intake exists for EPA or DHA intake on their own -- the official guidance covers only total ALA. This matters because ALA is not itself the fatty acid your body mostly uses; it has to be converted into EPA and then DHA, and that conversion is inefficient -- commonly cited at only around 5-10% for EPA, and considerably less for DHA. Two people can hit the same ALA target and land in very different places on EPA/DHA status depending on the rest of their diet, genetics, and sex (conversion tends to be somewhat more efficient in women).

**Why this matters especially for plant-based eaters.** Direct dietary EPA and [DHA](#gloss-dha) come almost entirely from fish, algae, and other seafood. If ALA (from flax, chia, walnuts, hemp, canola and soy oils) is your only omega-3 source, meeting the ALA goal is necessary but may not be sufficient -- your actual EPA/DHA status depends on that inefficient conversion step. Common ways to address this without animal fish: algae-oil supplements (a direct EPA/DHA source independent of the ALA conversion pathway), or simply logging ALA-rich foods generously since the target itself already assumes real-world conversion losses are ahead of it.

**Setting your own EPA+DHA target.** Because there's no official [DRI](#gloss-dri) to compute automatically, NuMa can't put a Daily Goal on the EPA or DHA rows the way it does for ALA. If you want to track against a target anyway -- clinical guidance in the 250-500 mg/day combined EPA+DHA range is common -- set one yourself as a [Revised Optimal target](#optimal) for the EPA and/or DHA rows in Settings → Nutrient targets.

Linoleic acid (omega-6) is tracked for completeness but has no established goal or known deficiency risk in a typical diet -- most diets, plant-based or not, comfortably exceed the [AI](#gloss-ai) for it.


### V. Profile Revised Optimal (Recent Research) Targets {: #optimal}
**A word on terminology, since two different ideas both sound like "optimal":** the standard [RDA](#gloss-rda) (Part 5, Section P) is not a bare minimum — it's already defined to meet the needs of nearly all healthy people in your age/sex group[^9]. What's described in this section is a *different, second* tier: a small number of nutrients where specific, more recent research argues for a target meaningfully *above* even that generous RDA figure. To keep the two clearly apart, NuMa calls this second tier **Revised Optimal (Recent Research)** — never just "optimal" on its own — and the RDA is never relabeled to match it.

The clearest example is Vitamin D: the RDA is 15–20 mcg/day, but a 2011 Endocrine Society clinical practice guideline recommends 37.5–50 mcg/day for adults at risk of deficiency[^12]. Rather than change what "RDA" means, NuMa lets you set your own **Revised Optimal target** for any nutrient, on top of the standard RDA, and tracks both side by side.

Configure Revised Optimal targets in **Settings → 7. Nutrient Targets**. Pick a nutrient, enter your target amount in that nutrient's usual unit, and save. Leave the field blank and save again to clear it. This works for any nutrient NuMa tracks -- not just ones with a standard RDA. Amino acids, [EPA](#gloss-epa)/DHA, and [phytonutrients](#gloss-phytonutrients) have no official [DRI](#gloss-dri) but are still valid Revised Optimal target or [max limit](#maxlimits) candidates; amino acids in particular are more accurately evaluated by the app's [DIAAS](#diaas)-based protein quality scoring (which accounts for total protein intake), so a flat daily gram target here is a coarser measure than that -- useful mainly if you want a simple standalone tripwire for one specific amino acid.

**Loading recommended targets.** Typing values in from scratch is a lot to ask, so the Nutrient targets screen offers a **"load recommended Revised Optimal targets"** button that fills in a small curated set of commonly-cited targets for any of those nutrients you haven't already customized yourself:

| Nutrient | Built-in Revised Optimal default | Source |
|---|---|---|
| Vitamin D | 50 mcg/day | Endocrine Society clinical practice guideline[^12] |
| Omega-3 EPA | 250 mg/day | [ADA](#gloss-ada)/Dietitians of Canada position paper[^13] (250 mg EPA + 250 mg DHA = ~500 mg combined) |
| Omega-3 [DHA](#gloss-dha) | 250 mg/day | Same source[^13] |

These are general population guidance, not personalized medical advice, and every value it loads can still be reviewed and adjusted individually afterward. See [Omega-3 Fatty Acids](#omega3) for why EPA/DHA specifically has no official [DRI](#gloss-dri) to compute automatically. Only these three nutrients have a built-in default today — see [Expanding Revised Optimal (Recent Research) targets](#expand-revised-optimal) in Part 9 for the plan to add more, each with its own citation the same way.

Once you have at least one Revised Optimal target set, every nutrient analysis table (food, recipe, meal, and daily summary) gains a second "Revised Optimal" set of columns next to the standard "RDA" columns -- the same meal %, day total %, and goal columns you already know, computed against your custom target instead of the RDA. Nutrients you have not customized show a dash ("–") in these columns rather than falling back to the RDA value, so it stays obvious which nutrients you've actually personalized.

Revised Optimal targets are per-nutrient, not per-day -- there is no single "optimal profile" to pick, only individual overrides you add nutrient by nutrient. A Revised Optimal target is always the two-sided "target" kind (see [Color coding](#color-coding)), not the "meet or exceed" kind used for the standard RDA: green in a comfortable range around your target, orange approaching that range from either side, blue if well short, red if significantly over — the same logic calories itself uses against the RDA.


### W. Maximum Nutrient Limits {: #maxlimits}
NuMa tracks three tiers of daily maximum, from broadest to narrowest:

- **Sodium's built-in [RDA](#gloss-rda)-tier limit.** Sodium is the one nutrient with a "limit" type right in the standard [RDA](#rda) calculation itself (Part 5, Section Q) — 2300 mg/day, the Chronic Disease Risk Reduction Intake. This is separate from the tier below and isn't configurable.
- **Built-in Tolerable Upper Intake Levels ([UL](#gloss-ul)).** Twelve more nutrients carry a real risk of harm from chronic excess, most often from supplementing rather than food alone. NuMa applies the standard adult UL for these automatically — no setup required — using the same age/sex-band pattern as the RDA table:

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

    Source: [NIH](#gloss-nih) Office of Dietary Supplements / Institute of Medicine Dietary Reference Intake UL summary tables[^9]. Five other tracked nutrients (potassium, thiamin, riboflavin, vitamin B12, vitamin K) simply have no established UL — the [DRI](#gloss-dri) tables mark these "ND" (not determinable from available data), which is different from "no risk at any dose." Magnesium, niacin, and folate are deliberately left out even though the DRI table publishes ULs for them (350 mg, 35 mg, and 1000 mcg respectively): each of those figures applies only to *supplemental* or fortified-food forms, not to the nutrient as it naturally occurs in whole food — niacin's UL guards against a flushing reaction specific to synthetic nicotinic acid/nicotinamide, and folate's guards against synthetic folic acid, neither of which whole-food niacin or folate triggers. NuMa sums whole-food intake for all three, so applying their published ULs here would flag entirely ordinary diets as "over the limit" for a risk that doesn't actually apply to them. If you take a supplement containing any of the three, that supplemental amount is exactly what the real UL is meant to track — use a [custom max limit](#maxlimits) below to watch it.
- **Your own custom max limits.** On top of (or instead of) the built-in defaults, you can set your own personal daily maximum for any nutrient -- useful if your situation calls for a stricter cap than the general guideline, or a cap on a nutrient that has no standard upper limit at all. A custom limit you set always takes precedence over the built-in default for that nutrient.

Configure your own max limits in the same place as Revised Optimal targets: **Settings → 7. Nutrient Targets**.

**Where you see it.** Every nutrient analysis table (food, recipe, meal, daily summary, trend, and the print/[PDF](#gloss-pdf) view) has a **UL** column, far right — whichever of the tiers above applies to that nutrient (your own custom limit if you've set one, otherwise the built-in UL), shown as a plain number when there's nothing to flag. Once a max limit is active for a nutrient — whether it's a built-in default or one you set yourself — NuMa watches your logged intake for the day: when today's total for that nutrient reaches 90% of the limit, the UL column shows a highlighted amber percentage and the whole row is tinted; at or over 100%, both turn red. This check applies to your **day total**, not to any single meal or food in isolation — a max limit is a daily budget, and a single meal being close to it isn't itself meaningful without knowing the rest of the day. On a page with no day-level context (a single food's per-100g view, for instance), the UL column still shows the numeric ceiling itself, just without a live percentage against it.

The max-limit warning is independent of the Revised Optimal target feature -- you can set one, the other, both, or neither for any given nutrient.


### X. Diet-Aware Bioavailability and Deficiency Notes {: #diet-bioavailability}
Your [dietary preference](#diet) setting (Settings → Dietary preferences) is used for more than filtering protein complement suggestions -- it also shapes two parts of your daily [RDA](#gloss-rda) comparison, because a vegetarian or plant-based diet changes not just *what* nutrients you're likely getting, but how much of certain ones your body can actually use.

**Iron and zinc targets are raised on vegetarian and plant-based settings.** Absorbable iron comes in two forms: heme iron (from meat, fish, and poultry, absorbed efficiently) and non-heme iron (from plants, absorbed far less efficiently, and further blocked by phytate in legumes and grains -- see [Antinutrients](#antinutrients)). Zinc absorption is reduced by the same phytate. Rather than silently under-representing this, NuMa raises the iron RDA by 1.8x[^4]<sup>,</sup>[^5] and the zinc RDA by 1.5x[^4]<sup>,</sup>[^6] when your dietary preference is set to Vegetarian or Plant-based only -- figures drawn from the Institute of Medicine's Dietary Reference Intake report and the [NIH](#gloss-nih) Office of Dietary Supplements' fact sheets for these two minerals. This appears as a normal, higher Daily Goal on the RDA comparison and Daily Nutrient Targets screens, with an explanatory note alongside it. Setting your preference back to "All animal foods" returns both targets to their standard values.

**A B12 warning appears for the Plant-based only setting when intake is low.** Vitamin B12 is almost exclusively animal-sourced[^7] -- unlike most nutrient shortfalls, a persistently low B12 reading on a fully plant-based diet isn't something more food logging or dietary variety fixes; it typically means a B12 supplement or B12-fortified food is needed.[^7] NuMa shows this warning only when your dietary preference is Plant-based only *and* today's B12 intake is under 50% of the RDA -- vegetarians (who still eat dairy and eggs) aren't flagged, since those foods are a legitimate B12 source and an occasional low day isn't a structural gap the way it is for a fully plant-based diet. The 50% figure is NuMa's own conservative trigger for surfacing the warning, not a clinical diagnostic threshold -- an actual B12 deficiency is properly diagnosed by a blood test (serum B12, methylmalonic acid, or homocysteine), not by a single day's logged intake.

Both of these are general population guidance based on your stated preference, not personalized medical advice -- if you have a diagnosed deficiency or absorption condition, follow your clinician's specific recommendations instead.

**The protein target is deliberately *not* raised, and that is not an oversight.** It is a fair question why iron and zinc get a multiplier on a plant-based diet while protein — the nutrient this whole program is most concerned about — does not. The difference is whether the penalty is visible in the data. A milligram of iron looks exactly like any other milligram of iron in a food record; nothing in the numbers reveals that the plant-sourced one is absorbed less well, so the only way to account for it is to raise the target. Protein's quality penalty is not hidden that way: it *is* the [DIAAS](#gloss-diaas) score, measured from the amino acid profile of the actual foods you logged, and it is already applied when NuMa computes your [Digestible Complete Protein](#dcp). Raising your protein target on top of that would charge you for the same shortfall twice.

This also answers the harder case, the vegetarian who eats both plant and animal protein and so fits neither rule cleanly. No rule is needed. The pooled meal calculation (see [How NutriMagnus scores meal and recipe protein quality](#protein-scoring)) evaluates whatever mixture you actually ate, so a diet that is half dairy and half legumes produces a quality score that genuinely reflects that mixture — not a category average. What you should watch, on any diet, is the [Digestible Complete Protein](#dcp) row against your protein target, rather than the raw protein row above it. [The protein target assumes high-quality protein](#protein-rda-quality) explains why that is the right comparison for everyone, omnivores included.

### Y. How NutriMagnus scores meal and recipe protein quality {: #protein-scoring}
(This section explains the meal-level method. For background on single-food [DIAAS](#gloss-diaas) and how amino acid ratios work, see [Appendix A](#appendix-protein-quality).)

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

Not every food in the [USDA](#gloss-usda) [database](#gloss-database) has a complete amino acid profile. When an ingredient is missing that data, NuMa runs the meal-level [DIAAS](#gloss-diaas) calculation using only the ingredients for which data exists, and flags the result as an estimate. The digestible [complete protein](#gloss-complete-protein) figure is then computed against only the protein that comes from those data-complete ingredients — so the result remains meaningful rather than artificially inflated.

##### Filling missing AA profiles at analysis time

When a meal contains ingredients without amino acid data, NuMa tells you how many are affected and distinguishes two situations:

- **Inside a recipe**: the ingredient is part of a recipe you logged as a meal item. Fix these by opening the recipe's ingredient editor and replacing or re-fetching the ingredient there.
- **Standalone meal ingredients**: foods you logged directly to the meal (not inside a recipe). These can be replaced on the spot: NuMa asks whether you want to search for a substitute.

If you say yes, for each affected ingredient the program opens a focused search of [USDA](#gloss-usda) [SR](#gloss-sr) Legacy and Foundation foods — the datasets most likely to include full amino acid profiles. The **[AA](#gloss-aa)** column in the results (✓ or ✗) shows at a glance which options have the data you need. Choosing a replacement updates that ingredient for the current analysis. Press Enter to skip an ingredient and leave it excluded from the calculation.

##### Why the first analysis of a meal can be slow

When you analyze a meal for the first time, you may see a "Fetching amino acid data…" message with a brief wait — sometimes several seconds. This is normal. NuMa is going online to download complete amino acid information for each food in the meal that doesn't already have it saved locally. Once downloaded, the data is stored on your computer, so the next time you analyze the same meal it will be fast.

---

## Part 5 — Reading Your Results

*(Reading time: 48 minutes)*

This part explains what the columns, tables, and analysis screens mean.

### A. Getting help {: #help}
Throughout this manual, **Learn more** links appear next to section headings and analysis output. Click any link to jump to the relevant explanation, or use this manual's own search box.

The sections linked from analysis output are:

- [Amino acid estimates in complement suggestions](#comp-estimate) — what "(estimated)" and "(generic estimate)" tags mean
- [Food Cache](#food-cache-web) — fetching missing amino acid data with Claude [AI](#gloss-ai)
- [Amino acid scoring](#aa-scoring) — limiting-amino-acid [DIAAS](#gloss-diaas) scoring method
- [Antinutrients](#antinutrients) — what [antinutrients](#gloss-antinutrient) are and how they appear in output
- [Archiving](#archive) — hiding foods, pantry entries, and recipes from everyday use without losing them
- [Bioavailability](#bioavailability) — [DIAAS](#gloss-diaas) bioavailability table columns
- [Complement suggestions](#comp) — protein [complement food](#gloss-complement-food) suggestions
- [Comparison](#comparison) — comparison ingredient, protein-quality, and nutrient tables (mixes foods and recipes)
- [Custom food profiles](#drafted-foods) — custom food profiles list columns
- [Daily nutrient goals](#goals) — how daily nutrient goals are calculated
- [DCP cap](#dcp-cap) — why [DCP](#gloss-dcp) is sometimes capped below the [DIAAS](#gloss-diaas) projection
- [DIAAS](#diaas) — digestible indispensable amino acid score
- [Diet-aware bioavailability and deficiency notes](#diet-bioavailability) — how dietary preference raises iron/zinc targets and flags low B12
- [Dietary preferences](#diet) — dietary preferences setting
- [Digestibility overrides](#dcp-overrides) — protein digestibility overrides table
- [Digestible complete protein](#dcp) — [DCP](#gloss-dcp) concept and formula
- [Essential amino acids](#aa) — [EAA](#gloss-eaa) reference and the nine indispensable amino acids
- [FAO reference values](#fao) — [FAO](#gloss-fao) 2013 amino acid reference requirement
- [Food annotation](#annotate) — annotate food picker table columns
- [Food Cache](#cached) — [Food Cache](#gloss-food-cache) column guide
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
- [Nutrient plot](#nutrient-plot) — line plot of chosen nutrients across logged days (web)
- [Omega-3 fatty acids](#omega3) — [ALA](#gloss-ala), [EPA](#gloss-epa), [DHA](#gloss-dha), and why only ALA has a Daily Goal
- [Oxalate data](#oxalate) — [oxalate](#gloss-oxalate) data source, enabling, matching, and limitations
- [Per-day profile tracking](#day-profile) — how a logged day stays pinned to the profile active when it was saved, and how to change it
- [Plot File Formats](#plot-file-formats) — [PNG](#gloss-png) vs. [SVG](#gloss-svg), and which to pick when downloading a plot
- [Revised Optimal targets](#optimal) — custom per-nutrient targets above the standard [RDA](#gloss-rda)
- [Protein completeness](#complete) — what makes a protein "complete"
- [Protein quality](#protein-quality) — single-food amino acid ratios table columns
- [RDA](#rda) — daily intake vs. recommended values table
- [Recipe ingredients](#recipe-ingredients) — recipe ingredient list columns
- [Recipes list](#recipes) — recipes list table columns


### B. Reading the output

#### Food Cache — Column Guide {: #cached}
The Food Cache list shows every food you have stored locally, sortable by Name, Type, [DIAAS](#gloss-diaas), or [GI](#gloss-gi) estimate. Columns:

<pre>
    Fetch    Checkbox to select this food for "Fetch missing data from Claude
             AI" — see <a href="#custom-foods">Getting missing amino acid data</a>. That button is only
             colored (actionable) when at least one food in the current list
             is missing amino acid data.

    Compare  Checkbox to add this food to Comparison — see <a href="#compare-checkboxes">Compare selected</a>.
             That button is only colored once 2 or more foods are checked.

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

    Notes    A "Notes ▸" link expands to show any saved notes and curator
             notes (curator notes are typically added by the Claude data-fetch
             workflow) — blank if neither is present.

    Actions  Portions, Refresh, Archive/Restore, and Delete for that row —
             see <a href="#food-cache-web">Food Cache</a> in Part 3.
</pre>

See [Food Cache](#food-cache-web) in Part 3 for the available actions on each row (Portions, Refresh, Archive/Restore, Delete, Prune unused foods) and how to fetch missing amino acid data with Claude [AI](#gloss-ai).


#### Archiving {: #archive}
Archiving lets you keep a food, pantry entry, or recipe without losing it, while hiding it from everyday use: default list views, food search results, and protein complement suggestions. It's meant for things you're not currently using but don't want to delete -- a seasonal ingredient, an old recipe you might revisit, a pantry item you've used up.

Archiving is reversible with the same action, one entry at a time: an **Archive/Restore** button on each row in the Food Cache, My Pantry, and Recipes pages toggles the state; a **Show archived …** / **Hide archived …** button on each of those pages toggles whether archived entries are shown at all. The button is filled in while archived entries are showing and outlined while they're hidden, and NuMa remembers your choice for each page.

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

#### Color coding (meal % and day total % columns) {: #color-coding}
    Green    Met — at or above a minimum, or within the comfortable range
             around a target (e.g. calories), or safely under a limit.
    Orange   Near — approaching a minimum from below, or drifting toward
             the edge of a target's comfortable range, or nearing a limit.
    Blue     Below minimum — well short of a floor-type nutrient (protein,
             most vitamins/minerals), where more is always fine.
    Red      Over the limit — past a Tolerable Upper Intake Level, or, for
             a target-type nutrient like calories, significantly over 100%.

A short Legend line showing all four colors appears right below any table that uses them.

If you have set a Revised Optimal target for any nutrient (Settings → 7. Nutrient Targets) — a higher daily goal of your own, for a nutrient where more recent research recommends more than the standard [RDA](#gloss-rda) — the table gains extra columns for it: **Revised Optimal goal**, plus the matching percentage columns (**% of Revised Optimal**, or **Rev. Opt. meal %** and **Rev. Opt. day %** on a meal). Nutrients you have not set one for show a dash ("–") in those columns. A note under the table explains them too. See [Revised Optimal Targets](#optimal) for details.

If you have configured a custom max limit for a nutrient, its row is highlighted (orange, then red) once today's total is within 10% of that limit. See [Maximum Nutrient Limits](#maxlimits) for details.

[Phytonutrients](#gloss-phytonutrients) (carotenoids, choline, isoflavones, etc.) appear only when [USDA](#gloss-usda) data for that food includes those values -- many foods have none. Amino acids are not in this table; see the Protein Quality section below it.

See [daily nutrient goals](#goals) to see how your daily goals are calculated. See [RDA](#rda) to see the Daily Intake vs. Recommended Values table.


#### Top Contributors Table {: #top-contributors}
Shows on meal and recipe detail pages, just above the Nutrient Analysis Table. Pick any tracked nutrient from the **Rank by** dropdown and see which foods in that meal or recipe supply the most of it, ranked highest to lowest.

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

A **Show** control next to the picker limits the list to the top 5/10/15/20/30 foods, or all of them (defaults to 10); it only offers choices that would actually shorten the list, so a meal with 6 contributors just offers "5" or "All." A "Total, all contributors" row at the bottom of the table always reflects every contributor, even when the list above it is trimmed.

A food logged more than once in the same meal — eaten twice on its own, or appearing both directly and inside a recipe in that meal — is grouped into a single row with its amounts summed, rather than listed as separate duplicate rows. This applies on both the per-meal page and the day-level Analysis rollup.

Ranking by **Protein** is special: instead of raw protein grams, it ranks each food by its own standalone [digestible complete protein](#dcp) ([DCP](#gloss-dcp)) — what that food alone would contribute after accounting for amino acid digestibility and completeness, using the same [DIAAS](#diaas) math as Protein Summary above it, applied to that one food in isolation. A note below the table explains this distinction and links back to Protein Summary. Because combining foods can raise a meal's *actual* DCP above what any single food scores alone — [protein complementarity](#comp) is the whole point of [DIAAS](#gloss-diaas) — this table's total will typically be lower than, and should not be read as equal to, the real meal DCP shown in Protein Summary. Foods with no amino acid data on file don't score a DCP and are omitted from the ranking when Protein is selected.


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

On food and recipe pages, this table also has a [DCP](#gloss-dcp) column. That DCP is just each food's raw protein times one shared meal- or recipe-wide score, so it's not that food's own standalone protein quality — two foods can show the same DCP simply by contributing equal protein, even with very different amino acid profiles, and that shared multiplier is also why sorting by protein and by DCP land on the same order. See [Top Contributors](#top-contributors) for each food's own standalone quality instead.

As with [Top Contributors](#top-contributors), a food logged more than once in the same meal is grouped into one row with its amounts summed, rather than shown as separate duplicate rows.

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
<pre>
    ~est    Estimated from food category average; no measured value for
            this specific food.
    user    You set a custom value (Settings → 6. Protein Digestibility
            Overrides — see <a href="#dcp-overrides">Digestibility overrides</a>).
</pre>

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

<pre>
    - Protein digestibility score (literature DIAAS, 0.00-2.00 scale).
    - A bar proportional to the score.
    - Digestible protein in grams from this portion.
    - Digestible complete protein (when amino acid data is also present).
    - Antinutrient notes when applicable (phytates, oxalates, lectins,
      bound niacin). Each note names the compound, describes the specific
      problem, and lists preparation steps that reduce the effect.
      See <a href="#antinutrients">Antinutrients</a> for a full explanation of what these notes mean.
</pre>

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
The main Meals & Log screen lists your recent meals, 9 at a time by default, sorted by date (most recent first). Change the sort order — Date, Name, Meal [DCP](#gloss-dcp), or Calories — via the sort dropdown; your choice is remembered as the default the next time you open Meals & Log. A **Number shown** field raises or lowers how many meals are listed, and a **Show meals on or before** date filter narrows the list to a cutoff date — both persist in the page's own controls, not as separate "older/newer" pagination links.

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
leftmost); leave a nutrient's position blank to hide it, then click **Save Meals & Log columns**.
Until you save a choice of your own, the columns are Protein, Calories, Carbohydrate, Fiber and
Sugars, in that order; **Restore default columns** puts those back at any time.

The Protein choice here is raw protein. [DCP](#gloss-dcp) (Digestible Complete Protein) isn't a
choice, because both lists always show it in fixed columns of their own.

Values for these columns come from the same computed snapshot as [DCP](#gloss-dcp)
and Calories, so they show -- until computed and n/a if the ingredient data
doesn't cover that nutrient. Use the Calculate button on the Meals & Log screen
(or analyze a meal) to compute them.

The same chosen columns also appear on the Daily Summary's Recent Days table
(Analysis -> Daily Summary), aggregated per day instead of per meal -- so a
day's Sodium column, for example, is the sum of every meal logged that day.

On both lists (web), a column with a unit stacks it onto its own line below
the nutrient's name (e.g. "Vitamin D" over "(mcg)"), matching the built-in
Meal [DCP](#gloss-dcp) / Day DCP / % goal columns -- so each column takes up roughly half
the width it otherwise would.

**Recent Days always shows Protein first, regardless of what you've chosen
above:** the raw, un-adjusted total -- Day DCP is the digestibility-adjusted
figure. This one column isn't part of your 6-column choice and can't be
turned off. Calories, Carbs (carbohydrates -- sugars and starches), and Fiber
are ordinary picks in that same Settings list now, right alongside Protein --
add them back, or leave them off, like any other nutrient; if you'd
separately picked Protein as a Meals & Log column, it's simply not duplicated
on Recent Days.

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
Analysis -> Food use in meals tabulates everything you actually ate across a
set of meals you choose — foods logged on their own, recipes, the
sub-recipes inside them, and every food used inside a recipe. You pick one selection method — one or more date ranges,
or a list of specific meal IDs (not both in the same run) — then choose
whether to include all foods or only protein-containing foods
(more than 0 g of protein per 100 g).

Columns:

    Food        Food or recipe name. Recipe rows are shown in bold.
    Code        The item's code: U = USDA food, UD = user-drafted food,
                R = recipe, OFF/CNF/CoFID/AFCD/CIQUAL = a food from
                that database. A key sits under the table.
    Days used   Number of distinct calendar days on which this food or
                recipe appeared, within the meals you selected.
    Meals       Number of selected meals containing this food or recipe.

Rows are ranked most- to least-used by Days used (ties broken by Meals, then
name), with a bar showing relative frequency.

Recipe items are counted twice: once as the recipe itself, and again as each
of its ingredients (recursively expanded through any nested recipes), so both
the dish and its components show up in the ranking. A sub-recipe inside a
logged recipe gets its own row too, so a recipe you only ever eat as part of
another one is still counted as eaten. A food you eat only inside recipes
is counted the same way.

Recipe rows always show the recipe's *current* name and are grouped by its
stable [ID](#gloss-id) — if you rename a recipe after logging it in meals, this analysis
still finds and merges every occurrence under the new name rather than
splitting them across old and new names or dropping them. Food rows work the
same way: the name shown is always the food's current cached name, even for
a meal logged before you last renamed it.

An expandable **Substitute a food or recipe** panel above the results lets
you bulk-replace one food or recipe with another across the meals currently
selected — see [Substituting a Food or Recipe](#fooduse-substitute).


#### Food Use in Recipes — Column Guide {: #fooduse-recipes}
Analysis -> Food use in recipes tabulates which foods and recipes are used
as *ingredients* across a set of recipes you choose (a recipe used as an
ingredient in another recipe is called a sub-recipe below) — the recipe-book
equivalent of Food Use in Meals. It looks only at your recipe book, not at
what you eat: a recipe you log in meals but never use as an ingredient in
another recipe won't appear here at all. For actual consumption, use
[Food Use in Meals](#fooduse). Pick one selection method: all recipes
(the default), one or more date ranges by when the recipe was created, or a
list of specific recipe IDs, then optionally limit to protein-containing
foods.

Columns:

    Food / Recipe       Food or sub-recipe name. Sub-recipe rows are shown
                        in bold.
    Code                The item's code (U, UD, R, OFF ... — see
                        Food Use in Meals above, or the key under the
                        table).
    Recipes used in     Number of selected (container) recipes whose
                        ingredient list contains this food or sub-recipe,
                        directly or nested inside another sub-recipe.

Rows are ranked most- to least-used, with a bar showing what percentage of
the selected recipes use each item. A sub-recipe used as an ingredient (e.g.
a house dressing used in several salads) gets its own row — its own
ingredients are also listed individually, the same way a directly-added
recipe (or a sub-recipe inside it) on Food Use in Meals shows up both as
itself and as its expanded ingredients.

This page has the same **Substitute a food or recipe** panel as Food Use in
Meals, scoped to ingredients of the recipes currently selected — see
[Substituting a Food or Recipe](#fooduse-substitute).


#### Substituting (Replacing) a Food or Recipe {: #fooduse-substitute}
Both Food Use in Meals and Food Use in Recipes have a **Substitute a food or
recipe** panel that bulk-replaces every occurrence of one food or recipe
with another, restricted to whatever's currently selected on that page (the
same date range(s) or [ID](#gloss-id) list you searched with).

You can also reach this replacement tool directly from a blocked deletion:
if Food Cache or Custom Food Profiles refuses to delete a food because it's
still used in a recipe or a meal, the "swap it for a different food" link in
that message brings you here with those exact recipes/meals already
selected and the food already filled in as the one to replace — you only
need to supply the replacement's code.

This is the tool for the common situation where a rename — or re-adding a
food from a search instead of reusing what was already in your cache — has
left what looks like two different foods, when really it's one food you
just want to consolidate under a single, newer entry. Fill in:

    Replace this   The old item's code (U171477, UD4, R21, OFF3 ...).
    With this      The replacement's code.

The results table below the form shows what's *currently used* in this
selection, not a list of foods you could replace with — it's there so you
can confirm what you're about to change (the item you're replacing, if any,
is marked "replacing this" in that table, with its code beside it). To find
the code of the **replacement** item, look it up on [Food Search](#food-search)
or the Recipes list (both open in a new tab from links right above the
form) — each shows the code in its results.

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
each changed recipe's [DCP](#gloss-dcp) automatically — including cascading up to any
recipe that in turn uses one of them as a sub-recipe.

A recipe can never be substituted into referencing itself; that combination
is silently skipped rather than creating a broken self-reference.

This writes to the [database](#gloss-database) immediately when you click through the
confirmation prompt — there's no automatic undo, so it's worth double-
checking the codes first.


#### Glycemic Load Output {: #glycemic}
Shows the estimated glycemic load ([GL](#gloss-gl)) for a food portion, meal, recipe, or whole day.

The number displayed is the total [GL](#gloss-gl), classified against whichever of the two scales fits what is being shown. A food portion, meal or recipe uses the per-serving scale:

    Low       10 or below (low glycemic impact).
    Medium    11-19.
    High      20 or above.

A whole day (Daily Summary, the day view, and the day printout) uses the daily scale instead, since a day's total is several times larger than any one meal's:

    Low       below 80.
    Moderate  80-120.
    High      above 120.

The daily bands are a convention rather than a validated clinical target, and a day's [GL](#gloss-gl) rises with how much you eat — NuMa says so underneath the number every time it shows one. See [glycemic load](#gl) for the fuller discussion.

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
*One of NuMa's data checks — see [Checking your data](#checking-your-data) for the rest.*

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
Shows all your saved recipes. Sorted by Last accessed by default; use the sort dropdown (not available while a search filter is active) to switch to Name or [DCP](#gloss-dcp)/serving instead. Your choice is remembered as the default the next time you browse recipes.

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

Each row has **Edit**, **Copy**, **Archive/Restore**, and **Delete** buttons. A filter box narrows the list by name; a **Sort by** dropdown switches between Last accessed, Name, and DCP/serving; a **Show archived recipes** button (beside **Show broken recipe references**) reveals archived recipes (shown grayed out with an "Archived" badge — see [archiving](#archive)). A **Broken recipe references** link finds ingredients pointing at a food or recipe no longer in your cache.

See [digestible complete protein](#dcp) for a full explanation of digestible [complete protein](#gloss-complete-protein).


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

Nested recipes ([ID](#gloss-id) = recipe) have their nutrients scaled automatically from their recorded serving count and total weight. Note that a nested recipe's Amount here is always a plain serving count, never a `pN` shortcut — see [Recipes: servings instead of `pN`](#portions-vs-servings) for why recipes and foods work differently here.

**Unsaved recipe-details edits and adding an ingredient.** The Recipe details fields (name, servings, instructions, etc.) at the top of the Edit Recipe page save separately from the ingredient list — clicking "Add to recipe" doesn't normally touch them. If you've changed one of those fields without clicking "Save recipe details" yet and then add an ingredient, a warning appears: adding the ingredient will save those pending changes for you rather than silently discard them. Choose Cancel to go back and finish editing those fields first, or Continue to save them and add the ingredient in one step.


#### USDA Food Search Results {: #food-search}
Listed after a food search. Combines matches from [USDA](#gloss-usda) FoodData Central, Open Food Facts[^3], and your local [Food Cache](#gloss-food-cache).

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
    checkmark or X. On the web app, you can also check a batch of "~checkmark"
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
    CONF.   Checkmark if a confidence/source note is saved. View it from
            the Food Cache.
    Code    The food's code: U (USDA), UD (user-drafted), R (recipe),
            OFF (Open Food Facts) ... — see <a href="#gloss-code">Code</a>.
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
</pre>

To select: click the result. If the food is not yet in your cache, NuMa fetches and saves it automatically.

**Compare selected.**{: #compare-checkboxes} Every row also has a checkbox in its own **Compare** column — check any mix of foods and/or recipes you want, then click **Compare nutrition of selected (up to 8)** above the table to jump straight to [Comparison](#comparison) with those items already added, no need to redo the search there. The same checkbox-and-button pair appears on [Food Cache](#food-cache-web), [My Pantry](#pantry)'s pantry list, and the [Recipes list](#recipes-menu-web) — each jumps into the comparison page from wherever you're already looking at a food or recipe.

**Sort order.** Results can be ordered two ways — a dropdown above the results table lets you switch, and your choice is remembered as the default for next time:

<pre>
    Best match to name (default)   See <a href="#search-ranking">Ordering food search results</a> in
                                    Part 6 for how this ranking works.
    Pantry, Cache, then Other       Same match-quality ranking, but when two
                                    or more results are tied on how well they
                                    matched your search, your own Pantry,
                                    then Cache, then Recipe entries sort
                                    ahead of USDA/OFF/other external results
                                    within that tie. It never lets a weaker
                                    match from your own data outrank a
                                    stronger external match.
</pre>

Both modes group your own Pantry/Food Cache/Recipe matches under their own heading above a divider, with external results below — but that heading reflects where the top-ranked matches happen to sort, not a hard rule; a strong external match can still land ahead of a weak local one under either sort mode.

See [Ordering food search results](#search-ranking) in Part 6 for the full explanation.

**Source filter.** A row of checkboxes next to the search box itself — visible before you've even typed a query, not just after results come back — narrows the list to any combination of sources you check: Pantry, Food Cache, Recipes, [USDA](#gloss-usda) FoodData Central, Open Food Facts, Canadian Nutrient File, CoFID, AFCD, CIQUAL (USDA and Open Food Facts, the two most-used external sources, lead the external group). Check as many as you like; unchecking every box is treated the same as checking them all, since a filter that hides everything isn't useful. Each checkbox is labeled with the short badge used elsewhere plus its full name (e.g. "USDA — USDA FoodData Central") and re-runs the search the moment you check or uncheck it. A **Select all sources** button re-checks every box in one click. A **What are these sources? →** link next to the "Source" label jumps to [Food data — where it comes from and how it is stored](#food-data). Your choice is sticky across every search box that has this filter, the same way the sort-order choice is. It appears next to every food search in the app: the standalone Foods → Search page, Analyze a Food Portion, Convert a Portion, Comparison, My Pantry's "Add a food" search, the Meals & Log "Add Food or Recipe" panel, a recipe's ingredient search, and the two "copy from another food" searches on the Edit Custom Profile page.

**"Did you mean" suggestions on a search with no results.**{: #search-suggestions} Every one of those same search boxes offers likely corrections right next to a "No results" message — e.g. searching "brocoli" suggests **broccoli**. Click a suggestion to re-run the search with it, or press Esc to dismiss the suggestions and keep what you typed. This works fully offline: it checks your own previously searched/cached foods, pantry items, and recipes first, then the food names bundled with the CoFID/[AFCD](#gloss-afcd)/CIQUAL [databases](#gloss-database) — it can't invent a suggestion for a brand name it's never encountered anywhere. It also appears on searches that don't have a Source filter, since they only ever look at your own cached data: [Food Cache](#food-cache-web), [Annotate](#annotate), [Recipes](#recipes-menu-web), [Search meal history](#meal-history), and Custom food profiles' "copy a cached food as a draft" search.

**Omitted-source warning.** Because the Source filter is sticky, a box unchecked once (even by accident, or while narrowing down a different search) stays unchecked everywhere until you re-check it — silently, with no visual difference from a normal search. If that hides a food you expected to see, it can look exactly like a search or ranking bug rather than a filter setting. On the Foods search page and the Meals & Log "Add Food or Recipe" panel, whenever one or more sources are unchecked, a small red note appears next to the Sort by control — **Omitted from search: RECIPE**, for example — naming exactly which ones. Check the Source filter row below to bring them back.

While a live [database](#gloss-database) (USDA, Open Food Facts, or Canadian Nutrient File) is being searched, a status line names exactly which ones it's contacting — just "Searching USDA FoodData Central…" if you've unchecked the other two, for instance. If you've unchecked all three, that line (and the network requests behind it) doesn't appear at all. CoFID, AFCD, and [CIQUAL](#gloss-ciqual) are different: each is a bundled dataset, not a live lookup, so their results appear instantly alongside your own Pantry/Cache/Recipe matches — checking or unchecking any of them never triggers a network wait.

**Result limit.** A "Show up to ___ search results" box next to the Source filter controls how many results are fetched and shown, per source (default 25, up to 500). Type a number and press Enter or click Search to apply it — like the Source filter, your choice is remembered as the default for next time.

See [Food Cache](#cached) for the [Food Cache](#gloss-food-cache) column guide. See [Food Cache](#food-cache-web) to learn how to get missing amino acid data via Claude [AI](#gloss-ai).


#### Comparison Tables {: #comparison}
Shows up to eight foods and/or recipes side-by-side, mixed in any combination, in up to three tables: an ingredient table, a protein-quality table, and a nutrient table. Every comparison is per 100 g of each item — a food's natural unit (grams) and a recipe's (servings) aren't otherwise a comparable amount to judge side by side, so rather than ask you to pick amounts that don't match across items, the page fixes every item at the same 100 g footing.

**How a recipe's 100 g figure is worked out.**{: #comparison-estimate} A food's per-100g nutrients come straight from its cached data — no estimation involved. A recipe has no single "100 g" anything, so NuMa derives one: it adds up the raw weight of every ingredient in the recipe (each direct food ingredient contributes its own entered gram amount; a sub-recipe ingredient contributes its *own* recorded total weight ÷ its own servings, × how many of those servings this recipe uses), then scales the recipe's total nutrients — and, for the ingredient table, each ingredient's own amount — by 100 divided by that summed weight. This is always a fresh sum of the ingredients as entered; it does **not** read the recipe's own "total weight" field on its detail page (a figure you may have set by hand to account for cooking loss, water evaporating, etc.) — only a *sub*-recipe's own total weight feeds in, one level down, when it's used as an ingredient.

If any ingredient's weight can't be determined — a direct ingredient with a blank or zero amount, or a sub-recipe ingredient whose own total weight or servings isn't set — that one ingredient is left out of the sum entirely rather than guessed at. The summed weight is then a lower bound, not the true dish weight, so the recipe's 100 g figures run *higher* than they should (the same nutrient total divided by a too-small weight). NuMa marks this by appending "(estimate)" next to that recipe's name everywhere it appears in these tables, so a higher-than-expected number has a visible reason rather than looking like a data error.

The **ingredient table** has one row per distinct ingredient name across the items you're comparing, one column per item, showing how much of that ingredient goes into 100 g of the finished item (or "--" if it isn't used, or if a recipe's ingredient weights are incomplete). A food entry shows itself as its own single "ingredient" — always "100 g," by definition. Ingredients shared by two or more items are listed first (highlighted) — that's usually the interesting question when comparing recipes: which ingredients differ, and by how much, per 100 g of the finished dish. A sub-recipe used as an ingredient shows its (rescaled) serving count rather than being expanded into its own raw ingredients.

The **protein-quality table** ([DIAAS](#diaas)-based) appears when at least one item has enough amino acid data to score: composite [DIAAS](#gloss-diaas) score, raw protein, digestible complete protein (DCP), DCP as % of raw protein, and the limiting amino acid — all per 100 g of the item, highest value per row highlighted, "--" for an item without enough data.

The **nutrient table** covers Macronutrients, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients), and Amino Acids (groups appear only when at least one item has data for that category), every value per 100 g, highest value per row highlighted in green, sortable by checked nutrients, rows where every item shows "--" hidden automatically. The items you chose are listed above the table — each also shows an **[AA](#gloss-aa)** column indicating at a glance whether it has amino acid data (✓) or not (✗).

**Print comparison table** and **Download [CSV](#gloss-csv)** buttons appear above the nutrient table: Print opens your browser's print dialog with just that comparison table (no nav, search box, or other page chrome); the CSV download gives one row per nutrient and one column per item, ready to open in a spreadsheet.

**Saving a comparison list.**{: #comparison-saved-lists} A **Save this list** box at the bottom of the page names and stores your current set of items; a **Use a saved list** panel at the top — shown even on the empty, no-items-yet view — lets you reload, rename, or delete any list you've saved before, so you don't have to re-search and re-add the same items each time you want to revisit a comparison.

To run a comparison: click **Compare** in the main nav. Search adds both foods (reaching out to [USDA](#gloss-usda)/[OFF](#gloss-off) like any food search) and your own saved recipes. You can save the list under a name for quick reuse in future sessions — previously saved lists are offered at the start of the comparison flow.


#### Annotate a Food {: #annotate}
Your own [GI](#gi) and [DIAAS](#gloss-diaas) estimates for a cached food, plus a short preparation note. Four ways in, all landing on the same page:

- **Foods -> Annotate a Food**, then filter by name and click **Edit** on the food you want.
- **The food's own detail page**, or its [Edit Custom Profile](#drafted-foods) page — both carry an **Add or edit [GI](#gloss-gi) / DIAAS estimates** button, and bring you back when you save.
- **The GI or [DIAAS](#gloss-diaas) figure on an add-food list**, which is itself a link: click it to edit that value, or click the dash where a value would be to add one.
- **The prompt after adding a food** that has neither estimate yet, which offers to take you there.

The list view shows Name, Type, and your current **GI est.** and **DIAAS est.** for every cached food, with a dash where nothing is recorded yet.

What you can set:

<pre>
    GI estimate      Glycemic index (0-100). See <a href="#gi">Glycemic Index</a>.
    DIAAS estimate   Your protein quality estimate (0.00-2.00). Useful for
                     packaged foods that lack amino acid data in USDA. See
                     <a href="#diaas">DIAAS</a>.
    Prep context     A short preparation note (e.g. "boiled 20 min", "raw").
</pre>

**Looking up a GI value instead of typing one.** Open **Look up a GI value from the published reference table** and search it by name. Click anywhere on a result to take its value: the list closes, the GI box fills in, and the **Save annotation** button highlights — the value is not stored until you press it. See [Where GI values come from](#gi) for the table and how to pick a population.

**The two "don't prompt me again" checkboxes** are only for deliberately leaving a value blank. Saving a GI or DIAAS estimate already stops NuMa asking about that one, so you do not need to tick anything to make the prompt stop.

**If you don't record GI values at all**, say so once instead of per food: tick **I do not record glycemic index data** at the foot of **Settings** then **Glycemic Index Reference Table**. NuMa then never asks you for a GI value when you add a food, the per-food GI checkbox disappears as redundant, the GI field itself folds away on this page (still there if you want it), and the notices about which GI reference table is in use stop. Nothing already recorded is deleted or hidden — a GI value you have saved is still shown and still used to work out [glycemic load](#gl) — and un-ticking it puts everything back, including any per-food choices you had made. A food still missing a DIAAS estimate goes on prompting for that, since it is a separate question.

**Saving settles the food.** Whatever you fill in, clicking **Save annotation** means you have dealt with this food: it stops interrupting you when you add it to a meal or the pantry, even if you deliberately left one of the two estimates blank. Come back any time through Annotate a Food to fill in the rest. **Skip for now** is the opposite — it saves nothing, so NuMa asks again the next time you add that food.

**When only one estimate is outstanding**, the prompt says so, and says which. The form always shows both the GI and the DIAAS field, so a prompt that is really about DIAAS would otherwise look identical to the GI prompt you just dealt with. A line above the form names whichever one is already settled, and the two fields are badged **Asking for this one** and **Settled — not being asked about** so there is no guessing.

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


#### Custom Food Profiles List {: #drafted-foods}
Shows the custom food profiles you have created by hand -- products from a label, research table entries, or supplements not in [USDA](#gloss-usda) or Open Food Facts[^3].

Columns:

    #       Row number. Use to select a profile for viewing or editing.
    Name    Food name as you entered it.
    Note    Your optional source or description note.

Custom food profiles are stored in your [Food Cache](#gloss-food-cache) and appear in all food searches alongside [USDA](#gloss-usda) and Open Food Facts[^3] entries. Internally these are called "user-drafted" foods, and in [ID](#gloss-id) columns throughout the program they're shown as "usr" — see the [usr](#gloss-usr) glossary entry.

To edit nutrient data: open the food from [Food Cache](#gloss-food-cache) or this list and click **Edit nutrients**. Editing is done in the [Food Cache](#gloss-food-cache) record itself, not in a separate copy.

**Comparing search results before you copy.** On the edit page, both searches ("Copy nutrient values from another food" and "Estimate amino acids from another food") give each result a **Compare** checkbox. Check the ones you want to weigh up and click **Compare checked foods with this one**: the [Compare](#comparison) page opens with the profile you're editing first and the checked foods beside it, every nutrient side by side per 100 g. Its **← Back to editing …** button at the top brings you back to the section you came from. Any unsaved edits are saved first, as with a search, so the comparison shows the profile as you have it now, and the Undo offer is waiting when you return.

To create a new custom profile: Foods -> Custom Food Profiles -> Create. See [Food Cache](#food-cache-web) for an alternative way to get missing data (e.g. amino acid data from Claude [AI](#gloss-ai) for foods not in [USDA](#gloss-usda)).

**Estimating amino acids by copying from another food.** Whenever you're prompted for a food's amino acid profile (creating a custom food profile, copying a cached food, or editing any food's data), a third option lets you search for and pick a similar food that already has amino acid data, instead of typing values in or pasting from literature. The picked food's amino acids are **scaled to match this food's own protein content** (not copied raw) — a food with less protein than the source gets proportionally less amino acid content, and vice versa — the same scaling already used by hand in this app's built-in curated foods (e.g. amino acids scaled between fresh and dried okara). A note documenting the source food and scale factor is suggested automatically for the Note field. On the web app, the same picker appears as an "Estimate amino acids from another food" panel on the custom-profile edit page ([Custom Food Profiles](#custom-foods)); editing any food's data this way marks it user-drafted, same as any other edit.

On the web app, [Food Search](#food-search) (and Food Cache and Pantry's own ingredient search) has a shortcut into this workflow: every food row shows a **Copy as custom-food draft** link/button. Clicking it duplicates that food as an editable draft and takes you straight to its edit page, [AA](#gloss-aa)-source search box ready — skipping the separate trip through Custom Food Profiles' own "Copy a cached food as a draft" search.


#### My Pantry Table {: #pantry}
Shows the protein sources you have flagged as currently on hand. The Pantry drives the complement advisor -- when NuMa suggests foods to fill an amino acid gap, it checks your pantry first and shows matching foods in a "From your pantry" tier.

Columns:

<pre>
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
            <a href="#cached">Food Cache</a> list — see the DIAAS entry there for
            how the saved-estimate-vs-reference-table value is chosen.
    ARCH    Shown only when archived entries are visible (the show-archived
            toggle) — a dot marks an entry as archived. See <a href="#archive">archiving</a>.
</pre>

Only pantry foods with [AA](#gloss-aa) data (checkmark) appear in complement suggestions. Name-only entries (--) and those without [AA](#gloss-aa) data (X) may still appear if their name matches a built-in complement table entry. Archived pantry entries never appear in complement suggestions.

Actions: **Add a food** ([USDA](#gloss-usda) search or name-only — the search results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns), **Remove**, **Archive/Restore** (see [archiving](#archive)), and an **Edit** button on each row that jumps straight to that food's Food Cache entry for editing. A name-only entry (no USDA link) shows a **Link a food** button instead — search and pick a match to attach real nutrient data to that same pantry row, rather than adding a duplicate.

**Why save just a name?**{: #pantry-name-only} It's a placeholder: it records that you have a food on hand when a search doesn't turn up a good match, you're offline, or you'd rather pick the right match later. To add one, click **Can't find it? Save just the name for now** just under the Pantry search box. A name-only entry has no nutrient data at all, so it can't be analyzed or compared until you link it — but it keeps your pantry list complete in the meantime, and **Link a food** turns it into a full entry without retyping anything.

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

*(Reading time: 31 minutes)*

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

**The short version:** results are ranked first by how many of your search words appear in the name — an item matching every word you typed always outranks one matching only some of them, which always outranks one matching none. Your own Pantry/Food Cache/Recipe matches only sort ahead of [USDA](#gloss-usda)/Open Food Facts/Canadian Nutrient File results when they're tied on that match quality — a genuinely better external match is never buried beneath a weak or coincidental match from your own data. The results table still shows your local matches under their own "From your pantry, food cache, and recipes" heading, with a divider before the external results below, but that's a display grouping over a single relevance-ranked list, not a hard "local always first" rule — the two groups can interleave if a later block of external results actually matches better. (An earlier version of NuMa let pantry/cache items always outrank everything else in the "Pantry, Cache, then Other" sort mode regardless of match quality, so an unrelated pantry item with only a coincidental word match could show up ahead of the food you actually typed. That mode now only breaks ties this way among equally-good matches — see below.)

**Word order matters, too.** If you type more than one search word, NuMa treats the order you typed them in as a signal of what matters most to you. Suppose you search `milk dry instant` because there are two kinds of dry milk — instant and non-instant — and you specifically want the instant kind, but you've put "dry" before "instant" because that's the more important distinguishing word to you. If nothing in your data matches all three words, NuMa prefers a match on `milk` + `dry` over a match on `milk` + `instant`, precisely because you typed "dry" first. In effect, the words you type earlier act as your stated priorities — a partial match that preserves your earlier words beats one that preserves only a later one, even when both partial matches contain the same number of words.

This means you can deliberately front-load your most important search word when you know a food name might be ambiguous or your data might be incomplete — put the word you care most about disambiguating on first, and let NuMa's ranking favor it if a perfect match isn't available.

*(For technically skilled users: the exact algorithm — including how word order is encoded as a simple bitmask comparison — is documented in `README-numa-documentation.md`, under "Searching for a food.")*

**When several results tie on text relevance, USDA data quality breaks the tie before name length does.** A dozen near-identical branded listings (say, a dozen "INSTANT NONFAT DRY MILK" products) can match your search words exactly as well as the one or two Foundation/[SR](#gloss-sr) Legacy foods actually named that — and branded names are often shorter, which used to let them win the final tiebreak even though they're the ones least likely to carry real amino acid data. Ties are now broken by data quality first (Foundation/SR Legacy, then Survey/Experimental, then Branded/Open Food Facts) and only fall back to shorter-name-wins after that, so the reference food most likely to actually answer your question surfaces before its branded look-alikes.

**Your own data is always checked first.** Before NuMa ever reaches out to USDA or Open Food Facts, it checks your local Food Cache and Pantry — a match there appears instantly, with no network round-trip. USDA and Open Food Facts results are still fetched right behind it (not only when the local check comes up empty), so a food newer than your cache, or one you've never looked up before, still turns up — it just takes a moment longer to appear. Once those external results arrive, the whole list (local and external together) is re-ranked by match quality as described above, so a stronger external match can end up ahead of a weaker local one rather than being stuck below it. A 12- or 13-digit barcode ([UPC](#gloss-upc)-A or [EAN](#gloss-ean)-13) skips general search entirely and goes straight to a direct Open Food Facts lookup by that exact code.

**Search result depth.** Plain, unprocessed foods (the ones most likely to carry full amino acid data) can get buried under branded or prepared-dish matches for the same word — USDA's own relevance ranking can push something like "Potatoes, flesh and skin, raw" 15–20 results deep for a plain "potato" search, or return two dozen canned/branded products before a plain cooked bean shows up for "pinto beans." To counter this, NuMa runs a second search pass restricted to Foundation Foods and SR Legacy (USDA's most complete, least processed data), so those results aren't lost in the noise. How many results that second pass fetches is configurable (Settings → 5. USDA [API](#gloss-api) Key → Search result depth) — the default of 25 is enough for the vast majority of searches; set it higher if you still don't see the food you expect, or to 0 to remove the cap entirely (every matching result USDA returns, in one page — a higher number means a slightly slower search).

### D. Editing your data, and what changes as a result {: #editing-consequences}
*How NuMa shows you the effect of a change, including on past days: [Seeing what a fix changed](#data-effects). Every data check: [Checking your data](#checking-your-data).*

NuMa saves some of its results so it doesn't have to work them out again on every page: each recipe's [DCP](#gloss-dcp) per serving, and each meal's DCP, calories and nutrient totals — the figures the Meals & Log list, the Daily Summary's Recent Days table, Nutrient averages across days and Nutrient Plot all read from. Whenever you change something those results were worked out from, NuMa works them out again for you. This section is the list of what follows from what, so an edit never has a consequence you didn't expect. For the other side of the same question — where NuMa fills in data that's missing, rather than recalculating data you've changed — see [Where NuMa fills gaps: estimates and estimation](#filling-gaps).

#### Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it {: #recipe-dcp-cascade}
A recipe can be used as an ingredient inside another recipe — a lentil sauce that shows up in three different dinners, say. Editing and saving that base recipe recalculates its own digestible complete protein ([DCP](#gloss-dcp)) automatically. If it's also used as a sub-recipe ingredient elsewhere, saving it recalculates DCP for every recipe that depends on it too — directly, or through another sub-recipe in between — so a foundational recipe's protein score is never left stale in anything built on top of it. You never need to manually recompute a dependent recipe just because you changed the recipe it's built from.

**Meals that log the recipe follow along too.** Every meal that logs the recipe you changed — or any recipe built on it — has its saved DCP, calories and nutrient totals recalculated as soon as you open your next page in NuMa, so the Meals & Log list and the Daily Summary show the new figures straight away.

A bulk "recompute DCP for all recipes" option still exists on the Recipes list — worth running after a bulk import, or if you suspect stale numbers predating this cascading recalculation.

#### How a meal records a recipe: servings, with grams when they're known {: #recipe-servings-grams}
A meal records how many *servings* of a recipe you ate, not how many grams. That's deliberate: a serving is always defined, but a recipe's weight often isn't. Cooking adds or drives off water, so the raw ingredients' weights don't add up to the cooked dish, and many recipes have an ingredient with no weight at all ("4 t cumin, weight not known").

Wherever a meal's items are listed — the meal page, the day pages, Meal History Search and printouts — a recipe shows its servings and, when NuMa can work it out, the grams too: **1 serving (295 g)**. NuMa can work out what one serving weighs in two ways, in this order:

1. from the recipe's **Total weight**, if you've filled it in on its Edit Recipe page — the most reliable, since you weigh the finished dish;
2. otherwise, from the sum of its ingredients' weights — but only if *every* ingredient has one, because a sum with a piece missing is short by an unknown amount.

If neither works, the amount reads **1 serving (weight unknown)**. Nothing is wrong with the nutrient figures in that case: a recipe's nutrients are worked out per serving, so they don't depend on knowing its weight. A footnote under each list says the same. To get grams shown, enter the recipe's Total weight.

**If a recipe's serving size changes after you've logged it, NuMa asks what you meant.** Change a recipe from 8 servings to 4 and each serving is now twice the food — so every meal that logged "1 serving" of it would quietly count twice as much. To stop that happening unnoticed, NuMa remembers what one serving weighed when you logged it. If that weight changes later (a different servings count, a new Total weight, ingredients added or removed), the meal page shows a yellow note under that item with two buttons:

- **Keep the 295 g I logged** — changes the servings count (to 0.5 servings, in this example) so the meal still holds the amount of food you actually ate. Usually the right choice: you ate what you ate.
- **Use the new serving size** — keeps "1 serving" and accepts the new, different amount. Right if the old serving size was simply wrong.

The day pages and Meal History Search flag the same item with a "review on the meal page" link. A difference of under 1% is ignored as rounding. The note can only appear when both weights are known, so a recipe showing "weight unknown" can't be checked this way — another reason to fill in its Total weight. Typing a new servings amount for the item yourself also settles it, against the serving size as it is now.


#### Editing or changing a food: nutrients, portions, amounts, name {: #food-edit-consequences}
**Editing a food's nutrients updates every recipe and meal that uses it.** Editing a food's nutrients — [copying a nutrient profile from another food](#drafted-foods), estimating its amino acids, refreshing it from [USDA](#gloss-usda), or importing Claude [AI](#gloss-ai)'s answer — immediately recalculates [DCP](#gloss-dcp) for every recipe that uses that food directly, and cascades from there to every recipe built on top of those, the same as editing a recipe itself does. Every meal that logs the food, on its own or inside any of those recipes, is recalculated too. You never need to recompute anything by hand just because you changed a food.

**Editing a food's portions changes nothing you've already entered.** Every amount you type for a food, in a recipe or a meal, is turned into a weight in grams the moment you enter it, and the grams are what NuMa saves. Changing what `p1` means later doesn't touch any amount already entered. How each kind of entry becomes grams:

- **`p1`, `1.5 p1`** — NuMa takes that portion's gram weight *as it is right now* and multiplies it out. A recipe ingredient or meal item saves the portion's description too (e.g. "1 cup, chopped"), not the code `p1`.
- **A volume, like `1/4 cup`** — converted to grams using the food's density, with the volume kept as a label ("52.3 gr (1/4 cup)"). If NuMa doesn't know the food's density, it asks you for a weight instead of guessing.
- **A weight, like `3 oz`** — converted straight to grams.

What that means when you edit a portion afterwards:

- **Nutrient totals don't change.** Past recipe ingredients and logged meal items keep the grams they were entered with.
- **A recipe's ingredient label is a record, not a link.** It shows how you typed the amount at the time. If you change `p1` from "1 cup" to "1 large", an older ingredient line still says "1 cup".
- **A logged meal item keeps what you typed, too.** Meal pages show the grams, with what you typed after them ("41.8 g (1/3 c)"). Meal items entered before October 5, 2026 kept only their grams.
- **Editing an amount re-reads it against today's portions.** Retyping `p1` on an existing line uses whatever `p1` means now, not what it meant when you first entered it.

If a portion's gram weight turns out to have been wrong, fix the portion; Foods → 9 then lists every recipe amount that used it under [Amounts that no longer match](#stale-amounts), ready to update in one click.

**Renaming a food doesn't rename it inside recipes or meals.** Each ingredient line and each logged item keeps the name it had when you added it; its nutrients always come from the food it's *linked* to, whatever name the line shows. (Renaming a *recipe* is different: its new name replaces the old one everywhere it's logged or used as a sub-recipe.) The same goes for an ingredient's own **Edit** popup on the Edit Recipe page — it changes the name the line shows, never which food it's linked to. So if a recipe's nutrients look wrong, check that each ingredient is linked to the food its name says; to link one to a different food, remove the line and add the right food.

**A food still used somewhere can't be deleted.** NuMa refuses to delete a food that a recipe, a logged meal or your pantry still uses, so nothing is ever left pointing at a food that no longer exists. Recipes are different — see [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere).

#### Meals and days {: #meal-edit-consequences}
A meal's or a day's own page always works everything out fresh, from whatever your foods and recipes contain right now. The figures saved for the list views (Meal [DCP](#gloss-dcp), Day DCP, % of goal, calories and the nutrient columns) are brought up to date automatically after any food or recipe edit, as described above. The batch button on [Meals & Log](#meal-columns) that calculates DCP and calories for all meals, or just the last 10 or 30 days, is still there for after a bulk import, or for meals whose figures were saved before this automatic refresh existed (October 2026).

If one of these automatic recalculations ever fails outright, it's reported under [System Issues](#system-issues-howto) in Settings rather than silently leaving old numbers in place.

### E. Entering custom foods and dietary supplements {: #custom-foods}
#### Custom food profiles

When a food isn't in [USDA](#gloss-usda) or Open Food Facts[^3] — or the entry you found is incomplete — create a custom profile from an existing food as a starting point, or from scratch, via Foods → Custom food profiles → Create.

Whichever interface you use, the same fields apply:

- **Name** — what to call this food in searches and meal logs.
- **Supplement mode** (see below) or a normal serving size and unit.
- **Basic macros** — calories, protein, total fat, carbohydrates, fiber, sugars, saturated fat, mono/poly fats, sodium. Always required.
- **Minerals, vitamins, amino acids, and [phytonutrients](#gloss-phytonutrients)** — all optional. For vitamins A, D, and E you can type the amount in [IU](#gloss-iu) (e.g. `400 IU`) and NuMa converts it automatically; amino acids can be entered one-by-one or pasted in as a block from a research table (g per 100 g protein — converted automatically).
- **Note** — document your source or any caveats about the data.

Once saved, the food appears in every search and can be used in meals and recipes exactly like any other food. Edit or delete it from the same place you created it, at any time.

**Editing the `p1`, `p2`, … portion shortcuts.** A food created by copying an existing one carries over that food's saved portions ("1 cup," "1 slice," and so on) exactly as-is — the custom-profile form itself doesn't have a portions editor. To add, remove, or change one, go to that food's [Food Cache](#food-cache-web) entry and use its **Portions** action, the same tool used for any cached food — see [A food's portion or serving-size data looks wrong](#ts-no-piece-portion) for how. This works whether the food started from scratch or as a copy, since a custom profile is still just a food in the cache underneath.

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


### H. Where NuMa fills gaps: estimates and estimation {: #filling-gaps}
*To find the gaps themselves, see [Checking your data](#checking-your-data).*

Food data is never complete — plenty of foods have no amino acid figures, and no food record carries a protein digestibility figure at all. Where a calculation needs a number that isn't there, NuMa either fills it with an estimate from a small built-in list, or leaves the food out and tells you. It never quietly saves a generic estimate into your own data. This is the full list of where estimation happens.

**Protein digestibility — an estimate for every food, every time.** [DCP](#gloss-dcp) needs to know how much of each food's protein your body actually absorbs. Food databases don't record that, so NuMa looks it up by the food's name, in this order:

1. your own figure, if you've entered one for that food ([Protein Digestibility Overrides](#dcp-overrides), Settings → 6);
2. a curated table of about 50 foods and food types, each with a published source;
3. a broad category estimate — isolated plant protein, legume, seed, nut, grain/cereal, or animal protein;
4. failing all of those, a default estimate of 0.82, a deliberately conservative figure for plant protein.

The [Meal Protein Digestibility Analysis](#meal-diaas) shows which of these each food got: a "category estimate" or "default estimate" label means NuMa had nothing specific for it. If you know a better figure for a food you eat often, enter it as an override.

**Amino acids in complement suggestions — a built-in list of 25 protein sources.** To suggest a food that closes an amino acid gap, NuMa needs that food's amino acid figures. When a candidate from your pantry, recipes or food cache has none, NuMa matches its name against a built-in table of 25 common protein sources (soy protein isolate, nutritional yeast, oats and the like) and scales that entry's amino acids to the food's own protein. Such suggestions are tagged "(estimated)" or "(generic estimate)" — see [Amino acid estimates in suggestions](#comp-estimate). This estimate is worked out afresh each time, is never saved, and is used *only* for suggestions — never in a meal's or recipe's DCP.

**Amino acids you estimate yourself.** The "estimate amino acids from another food" tool ([Custom Food Profiles](#drafted-foods)) copies a similar food's amino acid figures, scaled to this food's protein. Unlike the two above, this estimate *is* saved to the food, with a note naming the source, and is then used everywhere — DCP included — just as real data would be. It's your choice of source, which is why it's trusted that far. The same goes for a [DIAAS estimate](#diaas-estimate-table) you record by hand for a packaged food: that one is shown with the food, but NuMa doesn't use it in DCP calculations.

**Where NuMa leaves a food out rather than estimating.** If a food in a meal or recipe has no amino acid figures and isn't covered above, it isn't guessed at — it's left out of DCP, and the page says so: the DCP figure gets a footnote ("the true figure is at least this much"), and [Missing AA profiles](#missing-aa) lists the food. A recipe ingredient with under 1 g of protein (a spice, oil, salt) is left out of the recipe's DCP silently, since it can't change the result meaningfully; a bigger protein source without amino acid figures stops the recipe's DCP being saved at all, so it shows "NC" (not computed) rather than a guess.

**Where NuMa shows "unknown" rather than estimating.** A logged recipe's weight in grams is shown only when it can actually be worked out, never estimated — see [How a meal records a recipe](#recipe-servings-grams).

**Calories — estimated from protein, carbs and fat when a food has none.** A food that arrives with protein, carbohydrate and fat but no calories gets a calorie figure worked out from those three (4, 4 and 9 kcal per gram), marked as an estimate, and replaced by a real figure if its source later supplies one. Meal, recipe and daily-summary pages say what share of their calorie total is estimated. See [Calorie checks](#calorie-checks).

### I. Checking your data {: #checking-your-data}
Every result NuMa gives you is only as good as the food data underneath it. A food with no calorie value quietly adds nothing to every calorie total it's part of; a wrong cup weight is worse still: NuMa works out the food's density from it, and uses that density for *every* volume measure of the food — tablespoons, teaspoons, fluid ounces, any fraction or multiple of a cup — so every such amount you enter for that food, in any recipe or meal, comes out wrong. (Correcting the cup weight fixes amounts entered afterwards; those already entered are listed under [Amounts that no longer match](#stale-amounts).) NuMa checks your data in three places:

- **When data comes in.** Each food is checked the moment it's saved, by whatever route — a [USDA](#gloss-usda) fetch, Open Food Facts, a [CSV](#gloss-csv) or Claude [AI](#gloss-ai) import, or your own typing. Missing calories are filled in as an estimate, and right after you add a food with a problem to a meal or recipe, a note on that page says what's wrong with it.
- **Where you use data.** Food, meal, recipe and daily-summary pages flag what affects the figures you're looking at.
- **In one place, on demand.** **Foods → 9 (Database Integrity and Data Completeness Check)** lists every problem across all your data. The Home page tells you when new problems turn up (see [the reminder](#data-check-reminder) below).

#### Every check, and what to do about it {: #data-checks-list}

| Check | What it catches | Where you see it | What to do |
|---|---|---|---|
| [Broken references](#db-check) | A pantry entry, recipe ingredient or logged meal item pointing at a food or recipe that no longer exists; unreadable stored data | Foods → 9; a Home page banner | Use the fix button for each kind; read its note first, since each has a different effect |
| [Missing nutrient data](#data-completeness) | A food with no values at all for a whole nutrient group (macronutrients, minerals, vitamins, amino acids; omega fats and phytonutrients if you ask) | Foods → 9; the food's own page | Refresh it, ask Claude AI for just the gaps, or mark the gap "not needed" (a spice doesn't need macronutrients) |
| [Calories missing or not adding up](#calorie-checks) | No calorie value; calories far from what the food's protein, carbs and fat imply; calories estimated | Foods → 9; the food's page; a **Calories** note on meal, recipe and summary pages | Refresh from [USDA](#gloss-usda), fill in from another food, or edit the value; alcohol, sugar alcohols and very high fiber can explain a real gap |
| Impossible values | Negative values; more than 100 g of one nutrient per 100 g; protein, carbs and fat adding up to more than 100 g; more sugars than carbohydrate; more of the three fat types than total fat | Foods → 9; the food's page; right after adding it | Correct the value on the food; such data usually came wrong from its source |
| [Amounts that no longer match](#stale-amounts) | A recipe amount typed as a volume or portion ("1/3 c", "p1") whose stored grams differ from what it works out to today | Foods → 9 | Check the food's portions, then update the amounts there in one click |
| [Amounts converted with a generic density](#generic-density) | A volume amount ("2 T") for a food with no cup or spoon weight of its own, converted with a generic density for that kind of food | Recipe and meal pages ("≈ generic" mark), Foods → 9 | Measure the food's cup or spoon weight and add it on its Portions page, then correct the amounts |
| [Old USDA copies](#old-copies) | USDA foods not refreshed in over a year | Foods → 9 | **Refresh from USDA** shows what changed and lets you choose |
| [Missing amino acid data](#missing-aa) | Foods with protein but no amino acid figures, left out of protein quality ([DCP](#gloss-dcp), [DIAAS](#gloss-diaas)) | Foods → 9 (foods you use, most-used first); meal, recipe and food pages; the [AA](#gloss-aa) column in search results, Food Cache and Pantry | Find a Foundation or [SR](#gloss-sr) Legacy version, refresh from USDA, or estimate from a similar food; or tick "not needed" |
| [Missing portion weights](#ts-no-volume-portion) | A food with no cup, spoon or piece weight, so a volume or count can't become grams | Foods → 9 (foods you use, most-used first); recipe pages ("No portion/weight data exists"); when you type an amount | Add the weight once on the food's Portions page; or tick "not needed" if you always weigh it |
| [Duplicate foods](#duplicate-foods) | Two or more foods with the same name, so a fix to one doesn't reach what uses the other | Foods → 9 → **Find duplicate foods** (on request) | Compare them, keep one (the rest are replaced by it everywhere), or mark "not duplicates" |
| [Recipe weight unknown](#recipe-servings-grams) | A logged recipe whose serving weight can't be worked out; a recipe whose serving size changed after you logged it | Meal pages | Enter the recipe's total weight; review the meal as the page suggests |
| [Deleted sub-recipes](#ts-deleted-recipe) | A recipe ingredient or meal item pointing at a recipe that was deleted | Recipes → Broken recipe references; Edit Recipe (offers to relink) | Relink it or remove it |
| [Failed recalculations](#system-issues-howto) | A recipe or meal whose automatic recalculation broke after a change | Settings → 12; a Home page banner | **Retry** |
| [Import checks](#fetch) | Claude AI replies, [CSV](#gloss-csv) files and recipe imports: missing names, non-numbers, unknown nutrients; imports fill only empty values | The import page's "Notes from validation" | Fix the source and import again |
| [Estimates](#filling-gaps) | Where NuMa used an estimate (calories, amino acids, protein digestibility) instead of measured data | Labelled where the figure appears | Replace with real data where you can |

**Right after you add a food.** If a food you've just added to a meal or recipe has a problem from the table above (not merely an estimate), the page you're returned to says so straight away, with a link to the food. That is the cheapest moment to fix it: one food, while you remember what it is.

**The Home page reminder.**{: #data-check-reminder} When new problems appear since you last opened Foods → 9, the Home page says how many, with a link. Opening the check counts as reviewing them, and the note goes away; it comes back only for problems that are new after that. Problems in the starter foods and recipes NuMa comes with never set it off (they're listed on Foods → 9 all the same), so a new install doesn't open with a warning about data you haven't touched. In **Settings → 13 (Data Quality Reminder)** you can turn it off, or ask for a reminder every so many weeks even when nothing is new, as a routine. A monthly look is a sensible habit if you log most days.

#### Seeing what a fix changed {: #data-effects}
Fixing data changes results, sometimes a lot. A missing calorie value on almonds took one day's total from 1,527 to 1,955 kcal. NuMa shows you the effect three ways:

- **"What this change did."** After you refresh a food from [USDA](#gloss-usda), fill it in from another food, save a custom food, import Claude [AI](#gloss-ai)'s data, merge duplicate foods, or update amounts on Foods → 9, the page lists every recipe (per serving) and logged meal whose calories, protein, carbohydrate or fat moved, with before and after figures.
- **How much of a calorie total is measured.** The **Calories** note on a meal, recipe or daily summary leads with the share of its calories that comes from measured values rather than estimates, and names any food with no calorie value at all (whose grams count as zero).
- **Past days change too, and say so.** A logged meal's totals are worked out from its foods' data, so correcting a food rewrites every past day that used it. That's usually what you want, since it makes your history more accurate, but it means a past day's numbers can differ from what you saw then. Meal and Daily Summary pages note when and why their totals were recalculated ("Totals recalculated: 2026-10-03 (Nuts, almonds: its data changed)").

**Amounts that no longer match.**{: #stale-amounts} An amount you type as a volume or portion is turned into grams once, when you enter it (see [Editing or changing a food](#food-edit-consequences)). If the food's portions change later, or NuMa's way of converting does, those grams stay as they were. Foods → 9 lists every recipe and logged meal amount that would come out differently if typed today, with the grams stored and the grams it works out to now (each food has a **portions** link beside it). Check the food's portions first: if a portion weight is itself wrong (a "tsp" that's really a half teaspoon, say), fix it on the food's Portions page, and the "Now" figure follows. Then, for the amounts you tick, choose one of two buttons:

- **Update the ticked amounts to their "Now" grams** — the amount you entered stays; its grams change. Updating a logged meal changes that past day's totals.
- **Keep the ticked amounts as entered** — the stored grams are right (you weighed it, say). NuMa stops listing the amount and shows it under **Kept as entered**, marked with a badge, on Foods → 9 and on the food's Portions page. Tick it there and click **Stop keeping** to review it again. Changing the amount itself also ends the keep.

Amounts typed with their own weight ("42 g", "2 T 15 g") are never listed. A volume with a weight in brackets after it, like "1/3 c (42 gr)", is: older versions of NuMa added that weight themselves, but it may be one you weighed, so check before updating. Updating one drops the bracketed figure.

The food's own **Portions page** shows the same list for that one food, right after you add, change or remove a portion (and whenever any of its amounts still don't match). There, recipe amounts start ticked; logged meals and bracketed-weight amounts start unticked, for you to decide. If you've just reordered portions, amounts entered as `p1`, `p2`… now point at a different portion, so re-enter those rather than updating them.

**Amounts converted with a generic density.**{: #generic-density} When you enter a volume ("1/3 c", "2 T") for a food that has no cup or spoon weight of its own, NuMa converts it with a generic density for that kind of food: protein powders, flours, seeds and so on. That's a reasonable guess, but it is a guess, so recipe pages, Edit Recipe and meal pages mark every such amount **≈ generic\***, with a footnote. Click the mark to go to the food's Portions page, measure the food's actual cup or spoon weight (fill a measuring cup, level it, weigh it), and add it there. The mark then disappears, and the amounts it affects show up under [Amounts that no longer match](#stale-amounts), ready to correct. Foods → 9 lists every food with such amounts, most-used first, under **Amounts converted with a generic density**. An amount with a weight in brackets ("2 T (14.7 gr)") counts too: older versions of NuMa wrote their own conversion that way, so it's most likely the same generic figure, unless you weighed it. A weight you typed yourself ("15 g") is never marked.

**Foods you use with no amino acid data, or no portion weights.** These two lists on Foods → 9 could be long — dozens of foods for a well-used install — so each starts folded up, showing only its count, and lists only foods you actually use in a recipe, a meal or your pantry (an unused food affects no result), most-used first. Open one when you want to work through it. Tick **not needed** for a food that doesn't matter — a sprinkle of cheese with no amino acid data, a food you always weigh — and it stops being counted. Neither list raises the Home page reminder: they're improvements to make when you have time, not errors.

**Duplicate foods.**{: #duplicate-foods} Two copies of one food split your data: correct one and the recipes and meals using the other don't see it. **Find duplicate foods** on Foods → 9 lists foods whose names match once capitals, punctuation, a "\* " starter prefix, "Copy of" and "([FDC](#gloss-fdc) …)" are ignored — names that are merely similar ("Peanut butter, creamy" and "Peanut butter powder") aren't matched. For each group it shows each copy's type, how many nutrient values it has, and where it's used. Click **Compare nutrition** to see them side by side, then **Keep this one** on the better copy (usually the one with more values, or the one you've corrected): every recipe, logged meal and pantry entry using the others switches to it and the others are deleted. Each line keeps its own name and amount, and "what this change did" shows how totals moved. If two foods really are different (raw and cooked, say), click **Not duplicates** and they won't be listed together again; **Show groups marked "not duplicates"** brings them back if you change your mind. A "\* " food is part of NuMa's [starter data](#starter-data); keeping your own copy instead deletes the starter one.

**Old USDA copies.**{: #old-copies} USDA revises its records from time to time. Foods → 9 lists USDA foods you haven't fetched or refreshed in over a year. That isn't a problem in itself; **Refresh from USDA** on the food's page shows whether anything changed and lets you choose what to take.

---

## Part 7 — Essential resources

*(Reading time: 26 minutes)*

---

### A. Food data — where it comes from and how it is stored {: #food-data}
**Six large tables** are NuMa's primary sources of food information:

- **[USDA](#gloss-usda) FoodData Central** — the U.S. government's nutrition [database](#gloss-database), covering hundreds of thousands of whole foods, ingredients, and branded products. This is NuMa's primary source. ([FoodData Central FAQ](https://fdc.nal.usda.gov/faq/))
- **Open Food Facts** — a community-maintained [database](#gloss-database) of packaged and processed food products, especially useful for branded items not found in the [USDA](#gloss-usda) table. ([Open Food Facts](https://world.openfoodfacts.org/discover))
- **Canadian Nutrient File** — Health Canada's reference [database](#gloss-database), particularly good on amino acid coverage. ([Canadian Nutrient File](https://food-nutrition.canada.ca/cnf-fce/?lang=eng))
- **UK CoFID** — ~2,900 UK foods from Public Health England/[DHSC](#gloss-dhsc), bundled into NuMa directly rather than looked up live (it has no [API](#gloss-api) of its own). No amino acid data. ([CoFID](https://www.gov.uk/government/publications/composition-of-foods-integrated-dataset-cofid))
- **Australian [AFCD](#gloss-afcd)** — ~1,600 Australian foods from [FSANZ](#gloss-fsanz), also bundled directly. Has real amino acid data, unlike CoFID. ([AFCD](https://www.foodstandards.gov.au/science-data/monitoringnutrients/afcd))
- **French [CIQUAL](#gloss-ciqual)** — ~3,200 French/European foods from [ANSES](#gloss-anses), also bundled directly. No amino acid data. ([CIQUAL](https://ciqual.anses.fr/))

**[USDA](#gloss-usda) API key.** NuMa accesses FoodData Central through [USDA](#gloss-usda)'s public API. Without a personal key it falls back to a shared demonstration key (DEMO_KEY) that has a tight rate limit — heavy use by any user can exhaust it and cause searches to fail temporarily. Getting your own key is free and takes about a minute:

1. Go to https://fdc.nal.usda.gov/api-key-signup and enter your name and email.
2. [USDA](#gloss-usda) emails you a key immediately.
3. Enter it in NuMa under **Settings → 5. [USDA](#gloss-usda) API Key**, and click **Save key**. The field shows your current key in plain text whenever one is already saved, so you can retrieve it there any time.

Your key is stored on your computer only. Once set, all food searches use your personal key with a much higher rate limit.

**Search result depth** (Settings → 5. USDA API Key) — see [Search result depth](#search-ranking) in Part 6 for what this controls and why.

Every food in these online tables has a unique [ID](#gloss-id) number — think of it as a product code that identifies that one food and nothing else.

**Your [Food Cache](#gloss-food-cache)**{: #FoodCache} is a table stored on your own computer. When you search for a food, NuMa checks your [Food Cache](#gloss-food-cache) first and shows any matches in a fast **[Food cache](#gloss-food-cache)** table before going online. Any food you have looked up before will be there and can be selected instantly, without a network call. If the food is not yet in your cache, the program searches both online tables and shows you a combined list of matches. When you select a food from that list, NuMa saves a copy of its nutrient data in your [Food Cache](#gloss-food-cache) automatically. Over time, most of the foods you normally eat will be in your [Food Cache](#gloss-food-cache) for quick retrieval.

**Edit protection.** Any food you edit manually — through Foods → 5. [Food Cache](#gloss-food-cache) — is marked as user-modified, and its type then reads, for example, "[SR](#gloss-sr) Legacy · user-edited": where it came from, and that you've changed it. NuMa will never silently overwrite a user-modified food with a fresh copy from [USDA](#gloss-usda), even if you search for that food again later. Your edits, custom amino acid values, and notes are permanent unless you change or delete them yourself. When you do ask for fresh data, with **Refresh**, you see it side by side with yours first and choose value by value — see [Refreshing a food, or filling it in from another food](#review-incoming).

NuMa keeps track of *which* values you changed, by remembering what the food's source last supplied. The food's page lists them under **Your changes to this food's original values**, each beside the original. A food is user-edited only while at least one of your changes remains, or while it has a GI, DIAAS or preparation note of yours: change a value back, or take USDA's on a Refresh, and once nothing of yours is left the "user-edited" mark goes away by itself. (A food you edited before NuMa tracked values one by one says so on its page; one Refresh from USDA lets NuMa work out which values are yours.)

**Refreshing a food, or filling it in from another food.**{: #review-incoming} Both open the same review screen: each value that differs is listed with what the food has now beside what's incoming, and only the values you tick are written.

- **Refresh** (Food Cache list, or **Refresh from USDA** on a USDA food's page) fetches USDA's current copy of the food.
- **Fill in nutrients from another food** (on the food's page, for any food that isn't one of your custom profiles) lets you search for a similar food and pick from its values. Your custom profiles have the same search on their Edit page.

What's ticked for you:

- A value that **fills a blank** is always ticked.
- On a Refresh, a value that **differs** is ticked when the food's value is just USDA's older figure, and unticked when it's one you changed (marked **yours**), so yours is kept unless you choose otherwise.
- From another food, a value that differs from one the food already has is unticked.
- Values that are the same on both sides aren't shown, only counted. A value USDA no longer lists is kept, and named so you know.
- **Tick only blanks**, **Tick all** and **Tick none** change every tick at once.

On a Refresh, the food's name, brand and serving size are offered the same way. Your portions are never changed, because logged amounts such as `p1` depend on them; any portion USDA has that the food doesn't is offered as an addition.

Filling in from another food changes the food itself, not a copy, so every meal and recipe using it picks up the new values, and it shows as user-edited afterwards. A Refresh makes the food match USDA wherever you tick USDA's value. If that leaves none of your changes, the food stops being user-edited, and if you leave a differing value unticked, it becomes user-edited. A note above the **Write the ticked values** button tells you before you click.

**Keeping the old version for past meals.**{: #keep-version} Normally a Refresh changes the food everywhere, including meals you logged long ago. When the food itself has changed, for example a product reformulated or USDA revising its figures, tick **Keep this food's current values for meals logged before** and pick a date (today, unless you change it). The food's current values are then kept as an *older version* with its own [code](#gloss-code): the food's code plus a number, e.g. **U171477.1**, with its date added to its type, e.g. "Branded · 2025-07-13". Meals dated before your chosen day switch to that older version, so their totals stay as they were. Later meals and every recipe (a recipe has no date) get the new values. The food's page lists its older versions, and an older version's own page links back to the current one. Older versions stay out of search results, since they're archived. To fold one back into the current food, use **Substitute** on Food Use in Meals (replace U171477.1 with U171477).

**Amino acids from another food are scaled, not copied.** A food with twice the protein of its source would otherwise look twice as complete as it is. So the screen shows the source's amino acids scaled to this food's protein. If you also tick the source's Protein value, the amino acid figures change on the spot to match that protein instead. A food with no protein value at all can't take amino acids until it has one (tick Protein). The food's notes record where the estimate came from. If the food already has some amino acid values, the screen points out that filling only the missing ones mixes two sources.

**Estimates give way to measured values.** NuMa remembers which values came from another food. If a later Refresh brings USDA's own measured figure for one of them, that figure is ticked, even on a food you've edited. The meal page's **Refresh from USDA** goes one step further for amino acids: measured ones replace estimated ones automatically.

The **Refresh from USDA** link on a meal page works on all the meal's foods at once, so it doesn't stop to ask. It fills in missing values only, never replacing one a food already has, then lists any food whose USDA copy also differs on existing values, each with a link to this review.

**Omega fatty acid tracking.** NuMa tracks four individual omega fatty acids — [ALA](#gloss-ala) (plant-based omega-3, found in flaxseed, walnuts, chia), [EPA](#gloss-epa) and [DHA](#gloss-dha) (marine omega-3, found in fish and seafood), and linoleic acid (the main omega-6, found in vegetable oils and nuts). These appear in the nutrient table whenever [USDA](#gloss-usda) data is available. Foods already in your cache that predate this feature are updated automatically the first time you access them — no action needed on your part.

Food enters your [Food Cache](#gloss-food-cache) in four ways:

1. **From [USDA](#gloss-usda)** — you search, find a match, and select it. It is instantly saved into your [Food Cache](#gloss-food-cache).
2. **From Open Food Facts[^3]** — same process; the food is saved the moment you pick it.
3. **By barcode** — in any food search box, type the 12-digit [UPC](#gloss-upc)-A or 13-digit [EAN](#gloss-ean) barcode printed on the product (spaces and hyphens are ignored). NuMa looks the product up on Open Food Facts by barcode and shows it as the one search result — typing the exact barcode is itself the confirmation, so there's no separate "use this?" step; click it like any other search result to add it. This is the fastest way to add packaged foods and dietary supplements — many have an Open Food Facts entry but no [USDA](#gloss-usda) record.
4. **By hand** — you create a custom food profile yourself, entering nutrient values from a product label or research source. These entries go straight into your [Food Cache](#gloss-food-cache) without coming from any online source.

In every case, NuMa saves the food's original ID number alongside its data. That ID is the key that allows everything else in the program to refer back to a specific food unambiguously.

**Adding to [My Pantry](#pantry) doesn't always mean caching.** Picking a real search result when you add a food to your pantry caches it exactly like ways 1–3 above — there's no separate pantry-specific mechanism. But Pantry's **Can't find it? Save just the name for now** option skips the cache entirely: it stores just a name, with no nutrient data, until you later use **Link a food** to attach a real match and cache it. See [My Pantry](#pantry) in Part 5 for the full picture, including how a name-only entry shows up in that table.

**[Food Annotations](#gloss-food-annotation)** are a second table on your computer. They hold extra information you choose to add about a specific food — information that does not exist in either online table:

- **Glycemic index ([GI](#gloss-gi))** — how quickly a food raises blood sugar (scale 0–100). Neither [USDA](#gloss-usda) nor Open Food Facts[^3] provides [GI](#gloss-gi) values, so if you have a figure from a research table or a product source, you can record it here.
- **[DIAAS](#gloss-diaas) estimate** — a protein quality score (scale 0–2.0). NuMa can calculate this automatically for whole foods that have complete amino acid data. For packaged foods where that data is absent, you can record a known [DIAAS](#gloss-diaas) figure here instead — see [Estimating DIAAS by hand for a packaged food](#diaas-estimate-table) for a quick-reference table by protein source.
- **A preparation note** — a short reminder such as "boiled 20 minutes" or "soaked overnight."

Each annotation is linked to one specific food in your [Food Cache](#gloss-food-cache) by that food's ID number. This means two things: you can only annotate a food that is already in your cache, and if you ever remove a food from your cache, its annotation is removed with it automatically.

**Your Recipes** are stored in their own table on your computer. Each recipe holds a list of ingredients, and each ingredient is linked to a specific entry in your [Food Cache](#gloss-food-cache) — by that food's ID. NuMa handles this link automatically: when you add an ingredient to a recipe, it searches your cache and the online tables exactly as it would for any other food search, and caches the result if it isn't stored yet.

A recipe can also include another recipe as one of its ingredients, allowing you to build complex dishes from simpler prepared components. When you log a meal, you can add a portion of a recipe — or a portion of a recipe-within-a-recipe — exactly as you would add a single food.

**[My Pantry](#gloss-my-pantry)** is a short personal list of protein sources you currently have on hand — tofu, lentils, Greek yogurt, and so on. It is a separate table used for one specific purpose: when NuMa suggests foods to fill a protein gap in your diet, it checks your pantry first and moves those foods to the top of the suggestion list. This way the program recommends things you can actually use right now, rather than foods you would need to go and buy.

**How these lists relate — and where to edit.**

Your [Food Cache](#gloss-food-cache), your Pantry, and your Custom Food Profiles are three different windows onto the same underlying data — not three separate stores.

Every food's nutrient data lives in exactly one place: the [Food Cache](#gloss-food-cache). The Custom Food Profiles list is simply a filtered view of your [Food Cache](#gloss-food-cache) showing only the foods you created or edited by hand (internally tagged "user-drafted" — see [usr](#gloss-usr)). The Pantry is a short list of names that each point back to an entry in the [Food Cache](#gloss-food-cache) (when a [USDA](#gloss-usda) link exists).

This means: if you edit a food's nutrients in the [Food Cache](#gloss-food-cache), that change is immediately reflected everywhere — in Custom Food Profiles, in any recipe using that food, in pantry-based analyses, and in annotations. There is no syncing, no duplication, and no risk of one list getting out of step with another.

**To edit nutrient data for any food, always go to Foods → 5. [Food Cache](#gloss-food-cache).** Annotations ([GI](#gloss-gi), [DIAAS](#gloss-diaas) estimates) work the same way: annotate a food once in the [Food Cache](#gloss-food-cache) and the annotation appears everywhere that food is used.

### B. Glossary {: #glossary}
Abbreviations and key terms used in NuMa output and this manual.

---

**AA**{: #gloss-aa}  —  Amino acid. The molecular building blocks of all proteins. See [essential amino acids](#aa).

**ADA**{: #gloss-ada}  —  American Dietetic Association, now the Academy of Nutrition and Dietetics. Co-author, with Dietitians of Canada, of the omega-3 position paper behind NuMa's suggested EPA/DHA targets. See [Omega-3 Fatty Acids](#omega3).

**AFCD**{: #gloss-afcd}  —  Australian Food Composition Database. ~1,600 Australian foods published by [FSANZ](#gloss-fsanz), one of the bundled datasets NuMa searches; it does carry amino acid data. See [Food data](#food-data).

**AI**{: #gloss-ai}  —  Adequate Intake. A nutrient reference value used when a full RDA cannot be established; considered sufficient for most healthy people. Used for fiber in NuMa. See [RDA](#rda).

**ALA**{: #gloss-ala}  —  Alpha-Linolenic Acid. The plant-based omega-3 fatty acid — found in flaxseed, walnuts, and chia — that NuMa tracks alongside EPA and DHA. See [Omega-3 Fatty Acids](#omega3).

**ANSES**{: #gloss-anses}  —  Agence nationale de sécurité sanitaire de l'alimentation (French food safety agency). Publisher of the [CIQUAL](#gloss-ciqual) food composition table bundled with NuMa.

**Antinutrient**{: #gloss-antinutrient}  —  A naturally occurring plant compound that partially blocks the absorption or use of a nutrient. Common examples: phytates (reduce mineral absorption), oxalates (reduce calcium absorption), lectins (interfere with digestion in raw legumes), bound niacin in corn. All can be reduced by appropriate preparation. See [antinutrients](#antinutrients).

**API**{: #gloss-api}  —  Application Programming Interface. A doorway one program uses to fetch data directly from another over the internet, with nobody clicking anything. NuMa uses [USDA](#gloss-usda) FoodData Central's API to look up foods. See [Food data](#food-data).

**Bioavailable protein**{: #gloss-bioavailable-protein}  —  Protein the body can actually absorb and use, accounting for both digestibility and amino acid completeness. More meaningful than the raw protein figure on a nutrition label.

**CGM**{: #gloss-cgm}  —  Continuous Glucose Monitoring. A wearable device that measures blood glucose every few minutes. Discussed in [Appendix C](#appendix-gl-comparison) as the most accurate way to track individual glycemic response.

**CIQUAL**{: #gloss-ciqual}  —  The French food composition table published by [ANSES](#gloss-anses); ~3,480 French and European foods bundled with NuMa. No amino acid data. See [Food data](#food-data).

**Code**{: #gloss-code}  —  The short identifier every food and recipe gets, in one pattern: a few letters saying what kind of item it is, then a number. **U** = USDA FoodData Central food (U171477 — the number is its [FDC ID](#gloss-fdc-id)); **UD** = user-drafted food, one you entered yourself (UD4); **R** = recipe (R21); **OFF**, **CNF**, **CoFID**, **AFCD**, **CIQUAL** = a food from one of the other food databases, numbered 1, 2, 3… in the order you added them (OFF3). A **.1**, **.2** … on the end is an older version of that food, kept for past meals at a Refresh (U171477.1 — see [Keeping the old version](#keep-version)). A food's code never changes, even when you rename or edit it; a **✎** after a code means you've changed that food's data (it is *user-edited* — see [Custom Food Profiles](#drafted-foods)). The Substitute tool accepts codes typed in either upper or lower case. Shown in Code columns, and in parentheses under a food or recipe name — hover over it to see the kind spelled out. See also [ID](#gloss-id).

**CoFID**{: #gloss-cofid}  —  Composition of Foods Integrated Dataset. The UK's national food composition table, ~2,900 foods, published by Public Health England/[DHSC](#gloss-dhsc) and bundled with NuMa. No amino acid data. See [Food data](#food-data).

**Complete protein**{: #gloss-complete-protein}  —  A protein source that supplies all nine essential amino acids at or above FAO reference levels after digestibility adjustment. See [protein completeness](#complete).

**Complement food**{: #gloss-complement-food}  —  A food added to a meal specifically to supply the amino acids that other ingredients are short in. See [complement suggestions](#comp).

**CSV**{: #gloss-csv}  —  Comma-Separated Values. A plain-text spreadsheet format — one line per row, commas between columns — that Excel, Google Sheets, and most spreadsheet programs can open directly. NuMa uses it for exporting and importing Food Cache and recipe data. See [Food Cache](#food-cache-web).

**Database**{: #gloss-database}  —  An organized collection of information, stored so a program can search it and pull out exactly the piece it needs. NuMa works with two kinds. The food databases it looks foods up in: online ones such as [USDA](#gloss-usda) FoodData Central and Open Food Facts, plus the bundled ones that ship with it ([CoFID](#gloss-cofid), [AFCD](#gloss-afcd), [CIQUAL](#gloss-ciqual)). And your own database — a single file on your computer holding your [Food Cache](#gloss-food-cache), pantry, recipes, logged meals and annotations. See [Food data](#food-data).

**DCP**{: #gloss-dcp}  —  Digestible Complete Protein. Grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (all essential amino acids present at adequate levels). See [digestible complete protein](#dcp).

**DHA**{: #gloss-dha}  —  Docosahexaenoic Acid. A marine omega-3 fatty acid — found in fish and seafood — that NuMa tracks alongside ALA and EPA. See [Omega-3 Fatty Acids](#omega3).

**DHSC**{: #gloss-dhsc}  —  Department of Health and Social Care, the UK government department that (with Public Health England) publishes [CoFID](#gloss-cofid), the UK food composition dataset bundled with NuMa.

**DIAAS**{: #gloss-diaas}  —  Digestible Indispensable Amino Acid Score. A score from 0 to 1.5+ measuring how much of a food's protein the body can actually use, accounting for digestibility and amino acid completeness. 1.0 = meets the FAO reference exactly; above 1.0 = excellent; below 1.0 = one or more amino acids are limiting. See [DIAAS](#diaas).

**Digestibility coefficient**{: #gloss-digestibility-coefficient}  —  A number between 0 and 1 representing the fraction of a nutrient that reaches the bloodstream after digestion. NuMa uses true ileal digestibility values from published literature. Eggs and dairy sit near 1.0; whole legumes are typically 0.79–0.85.

**DNA**{: #gloss-dna}  —  Deoxyribonucleic Acid. The molecule in every cell that carries its genetic instructions. Mentioned in the [Full Nutrient Key](#nutrient-key), where several B vitamins are needed to make and repair it.

**DRI**{: #gloss-dri}  —  Dietary Reference Intakes. The system of nutritional reference values published by the U.S. National Academies of Sciences[^9]; the source for RDAs, AIs, and upper intake levels used in NuMa.

**EAA**{: #gloss-eaa}  —  Essential Amino Acid. One of nine amino acids the human body cannot make and must get from food every day: Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine. See [essential amino acids](#aa).

**EAN**{: #gloss-ean}  —  European Article Number, the 13-digit barcode standard used outside North America. Typing one into food search goes straight to an Open Food Facts lookup. See [Ordering food search results](#search-ranking).

**EAR**{: #gloss-ear}  —  Estimated Average Requirement. The intake that meets the needs of the *average* person in a group, with no safety margin — a population-statistics figure, not a personal target. The [RDA](#gloss-rda) is set above it. NuMa does not use the EAR for anything. See [Recommended Dietary Allowances](#rda).

**EPA**{: #gloss-epa}  —  Eicosapentaenoic Acid. A marine omega-3 fatty acid — found in fish and seafood — that NuMa tracks alongside ALA and DHA. See [Omega-3 Fatty Acids](#omega3).

**FAO**{: #gloss-fao}  —  Food and Agriculture Organization of the United Nations. The body that published the 2013 amino acid reference standard used for all protein quality scoring in NuMa. See [FAO reference values](#fao).

**FDC**{: #gloss-fdc}  —  FoodData Central. The USDA's online nutrition [database](#gloss-database) and NuMa's primary food data source. Each food has a unique numeric FDC ID. Website: https://fdc.nal.usda.gov/

**FDC ID**{: #gloss-fdc-id}  —  The unique numeric identifier assigned to each food entry in USDA FoodData Central. You can enter an FDC ID directly at any "Search food or recipe" prompt instead of typing a name.

**Food Cache**{: #gloss-food-cache}  —  Your local [database](#gloss-database) of previously retrieved foods. Searching the cache is instant (no network required); foods are added automatically when you select them from USDA or Open Food Facts[^3] results.

**Food Annotation**{: #gloss-food-annotation}  —  Extra information you attach to a cached food: glycemic index, a DIAAS estimate, or a preparation note. Stored locally; not part of any online [database](#gloss-database).

**FSANZ**{: #gloss-fsanz}  —  Food Standards Australia New Zealand, the agency publishing the [AFCD](#gloss-afcd) food composition [database](#gloss-database) bundled with NuMa.

**GI**{: #gloss-gi}  —  Glycemic Index. A scale from 0 to 100 measuring how quickly a food raises blood glucose relative to pure glucose (100). See [glycemic index](#gi).

**GL**{: #gloss-gl}  —  Glycemic Load. A measure of glycemic impact that combines GI with the actual amount of carbohydrate in a serving. More useful than GI alone for real-world meal comparisons. See [glycemic load](#gl).

**GUI**{: #gloss-gui}  —  Graphical User Interface. A visual, point-and-click interface — this is what NuMa's web app provides (see [Part 3, "Using the Web App"](#part-3-using-the-web-app)).

**IAA**{: #gloss-iaa}  —  Indispensable Amino Acid. The FAO's own term for what this manual calls [EAA](#gloss-eaa) (Essential Amino Acid) — both refer to the same nine amino acids. See [essential amino acids](#aa).

**ID**{: #gloss-id}  —  Identifier. A number that refers to exactly one thing — one food, recipe, or meal — and never changes, even when you rename that thing. NuMa shows IDs in list columns and page titles so you can tell two similarly-named items apart. Foods and recipes show theirs as a [code](#gloss-code) (U171477, UD4, R21, OFF3). See also [FDC ID](#gloss-fdc-id).

**Ileal digestibility**{: #gloss-ileal-digestibility}  —  The fraction of an amino acid absorbed by the end of the small intestine (ileum). DIAAS uses true ileal digestibility, which is more accurate than fecal digestibility for measuring protein available to the body.

**IOM**{: #gloss-iom}  —  Institute of Medicine. The US body whose 2005 report set the Dietary Reference Intakes NuMa uses, including the 0.8 g/kg protein figure; renamed the National Academy of Medicine in 2015. See [The protein target assumes high-quality protein](#protein-rda-quality).

**ISO**{: #gloss-iso}  —  International Organization for Standardization. The independent international body that publishes agreed standards for how things are measured, tested and made. In NuMa it matters for one standard, ISO 26642:2010, which sets out how a [GI](#gloss-gi) study must be run: how much carbohydrate the test portion contains, how many people are tested, and when blood is sampled. Rows in the GI reference tables from studies that deviated from it are flagged **non-ISO method** — a warning about the evidence, not the food. See [Method quality, and why some rows are flagged](#gi-method-quality).

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

**PDF**{: #gloss-pdf}  —  Portable Document Format. A file that keeps its exact page layout wherever it is opened or printed. Every printable page in NuMa can be saved as one through your browser's own Print dialog.

**Phe+Tyr**{: #gloss-phe-tyr}  —  Phenylalanine + Tyrosine. Scored as a combined pair in DIAAS calculations because the body can convert Phenylalanine into Tyrosine.

**Phytonutrients**{: #gloss-phytonutrients}  —  Plant-derived bioactive compounds tracked by NuMa where USDA data exists: beta-carotene, alpha-carotene, lycopene, lutein/zeaxanthin, choline, beta-sitosterol, and isoflavones.

**PNG**{: #gloss-png}  —  Portable Network Graphics. An image file made of a fixed grid of dots, so it blurs if enlarged a lot. The friendlier of the two plot download formats — it opens anywhere. See [Plot File Formats](#plot-file-formats).

**Pooled DIAAS**{: #gloss-pooled-diaas}  —  The meal-level protein quality score computed by summing digestible amino acids across all ingredients before scoring. This captures how foods complement each other in a way that single-food DIAAS cannot. See the section [How NuMa scores meal and recipe protein quality](#protein-scoring).

**RDA**{: #gloss-rda}  —  Recommended Dietary Allowance. The average daily intake sufficient to meet the needs of most healthy adults in a given age and sex group. See [RDA](#rda).

**Reference value**{: #gloss-reference-value}  —  Short for [FAO](#gloss-fao) reference value: how many mg of one specific essential amino acid a person needs per gram of dietary protein, established independently for each of the nine [EAAs](#gloss-eaa). Dividing a food's own mg-of-that-amino-acid-per-gram-of-protein by its reference value produces that amino acid's [DIAAS](#gloss-diaas)-basis score. See [FAO reference values](#fao).

**Standard error**{: #gloss-standard-error}  —  A measure of how much the individual people in a study disagreed with each other, reported alongside an average as "±3" or "±15". A small figure means their results clustered tightly around the average, so that average is a dependable estimate; a large one means they scattered widely, so the average is shaky and could easily have come out differently with a different handful of subjects. It is written **SEM** in the published glycemic index tables (standard error of the mean). See [How to read a lookup result](#gi-result-row).

**SR**{: #gloss-sr}  —  Standard Reference, as in "SR Legacy" — the [USDA](#gloss-usda)'s pre-2019 food composition [database](#gloss-database). Along with Foundation foods, it is the [USDA](#gloss-usda) data type most likely to carry a full amino acid profile. See [Food data](#food-data).

**Sub-recipe**{: #gloss-sub-recipe}  —  A saved recipe used as one ingredient of another recipe — a sauce inside a pasta dish, a spice blend inside a stew. Its amount is given in servings, not grams, and its nutrients are worked out from its own ingredients and folded into the parent, however many levels deep the nesting goes. See [Recipes: Servings Instead of `pN`](#portions-vs-servings) for how a serving's weight is derived.

**SPI**{: #gloss-spi}  —  Soy Protein Isolate. A concentrated plant protein (95%+ protein by weight) with high digestibility (0.95); frequently cited in complement suggestions. See [Appendix D](#comp-appendix).

**SVG**{: #gloss-svg}  —  Scalable Vector Graphics. An image file stored as shapes rather than dots, so it stays perfectly sharp at any size. The better choice for printing a plot large. See [Plot File Formats](#plot-file-formats).

**TID**{: #gloss-tid}  —  True Ileal Digestibility. NuMa's abbreviation for [ileal digestibility](#gloss-ileal-digestibility), used as a column heading in per-ingredient digestibility breakdowns.

**UL**{: #gloss-ul}  —  Tolerable Upper Intake Level. The highest daily intake of a nutrient unlikely to cause harm — NuMa applies built-in ULs for twelve nutrients with a real risk of excess, shown as a column on every nutrient analysis table. See [Maximum Nutrient Limits](#maxlimits).

**UPC**{: #gloss-upc}  —  Universal Product Code, the 12-digit barcode standard used in North America. Typing one into food search goes straight to an Open Food Facts lookup. See [Ordering food search results](#search-ranking).

**USDA**{: #gloss-usda}  —  United States Department of Agriculture. The U.S. government body that publishes FoodData Central, NuMa's primary food data source.

**usr**{: #gloss-usr}  —  User-drafted. Older name for what is now the **UD** prefix of a [code](#gloss-code) (UD4): a food whose nutrient profile you created or edited by hand, rather than one retrieved from USDA or Open Food Facts[^3] — this is what the [Custom Food Profiles](#drafted-foods) list shows.

**WHO**{: #gloss-who}  —  World Health Organization. The United Nations health agency; co-publisher, with the [FAO](#gloss-fao), of the protein and amino acid requirement guidance NuMa's protein quality scoring follows.

### C. Internet resources {: #internet-resources}

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

### D. Using this manual's search {: #search-howto}
Use the sidebar search box near the top of the table of contents.

**By default it searches whole words, not phrases, and requires all of them for something to be considered a "hit".** Type `portion size` and NuMa looks for sections that contain *both* words somewhere — not necessarily next to each other, not in the order you typed them. This is different from typing a whole phrase and expecting an exact match: `edit portion` (as a phrase) will find nothing, because that exact wording never appears anywhere in the manual, even though the idea is covered extensively. If a search comes up empty, the fix is usually to drop a word, not add one — start with just the noun you care about (`portion`), see what comes back, then add a second word only if the list is too long to skim.

**Wrap your search in double quotes for an exact phrase instead.** Typing `"iron and zinc targets"` (quotes included) looks for that literal run of text instead of AND-ing separate words — useful when you're trying to relocate a specific sentence you remember reading, rather than explore a topic. Since it has to match verbatim, an exact-phrase search is more likely to come up empty than the default word search; if it does, drop the quotes and search the same words the normal way.

**Results are sections, not raw text.** Instead of jumping straight to every individual occurrence of your words scattered across the whole manual, search shows you a short list of section headings that contain all of them — click one (or press **Enter** to jump straight to the top match) to open it, and NuMa highlights every matching word within that section so you can see at a glance where they landed. **Enter**/**Shift+Enter** (or the &#x25B2;/&#x25BC; buttons) then step between highlighted words inside that one section, not across the whole document.

**The "Only show things you can do" checkbox** narrows the results further, to sections that contain some instruction — add, edit, change, remove, and similar words — rather than sections that merely *discuss* a topic. Turn it on when you're trying to do something rather than understand something: `portion size` with the box checked skips past conceptual explanations of what a portion is and goes straight to the section that tells you how to add or correct one. It's a heuristic, not a guarantee — a section phrased with an instruction word this checkbox doesn't happen to recognize can still be missed, and unchecking the box always shows you the same results or more, never fewer, so it's worth trying both if the checked list comes up empty.

**The "Match case" and "Whole words only" checkboxes** are for short terms that are also pieces of everyday words. Searching for "AI" (artificial intelligence) normally matches every "ai" in the manual — *main*, *detail*, *said* — which buries the few places that mean what you were looking for. Check **Match case** and it matches only capital "AI"; check **Whole words only** as well, and it no longer matches inside words written in all capitals, such as the titles in the [Recent program updates log](#updates-log), either. **Whole words only** on its own is handy for short abbreviations like [GI](#gloss-gi) and [AA](#gloss-aa), too. Both boxes also apply to "exact phrase" searches and to the highlights inside a section you open.

## Part 8 — Troubleshooting and feedback — reporting problems and offering ideas {: #feedback}

*(Reading time: 19 minutes)*

If something seems broken or confusing, there's a good chance the answer is already below. The topics are grouped by how the problem *feels* rather than which menu it's in, since that's usually how you'll remember it later — and a few topics are listed in more than one group, since the same problem can feel different ways depending on what you were expecting. There aren't so many that you can't just skim the headings if nothing matches at first.

### A. Operating the program

#### The program crashes unexpectedly {: #ts-crash}
If NuMa crashes or freezes, nothing you'd already saved is lost — every action (adding a food, saving a recipe, logging a meal) is written to your data immediately, not held until some later "save" step. It's safe to just restart the program and pick up where you left off.

If a page seems frozen or won't load, try refreshing it first. If that doesn't help, the program running in the background may need restarting — close and relaunch it the way you normally start NuMa.

Either way, [let us know](#feedback) — see ["How to contact help"](#quickhelp) below. This is beta software; a crash almost always means we found a real bug worth fixing, not something you did wrong.

#### You know what you want to do but can't see how to do it {: #ts-findit}
Click any **Learn more** link near a section heading or analysis output — see [Getting help](#help) for the full list of what each one covers.
- Either version: this manual's own search — if you're reading it in the web app, use the sidebar search box (see [Using this manual's search](#search-howto) for how to get good results from it, especially the "Only show things you can do" checkbox); if you're skimming the plain text version, search for a word describing what you're trying to do rather than a menu name.

If you still can't find it, [tell us what you were trying to do](#feedback) in plain language, not what menu item you were looking for. That phrasing is exactly what we need to know whether the feature exists, is named confusingly, or genuinely isn't built yet.

### B. I don't understand...

#### A recipe's "Complete" checkbox doesn't match its protein-completeness score {: #ts-complete-confusion}
A recipe's **Complete** checkbox and its amino-acid completeness score are two unrelated ideas that happen to share the word "complete." **Complete** (the checkbox, see the [Recipes list](#recipes) column guide) is a personal flag you toggle yourself — "I'm done editing this recipe" — it has nothing to do with protein quality. Whether a food or recipe's amino acid profile is **complete** (clears every essential amino acid floor) is a separate calculation shown in its [DCP](#gloss-dcp) and [DIAAS](#gloss-diaas) analysis. A recipe can be marked Complete and still have an incomplete amino acid profile, or the reverse.

#### I set a recipe's servings to 0 and now everything looks different {: #ts-servings-zero}
Setting a recipe's **Servings** field to 0 is a deliberate mode switch, not an error: it tells NuMa you want to analyze the recipe by total weight or volume instead of by serving count — useful for something you haven't decided how to portion yet (a big batch of granola, say). Every "per serving" figure becomes "per 100 g" or "per 100 ml" instead, and [DCP](#gloss-dcp) shows as **NC** (not computed) since there's no serving size to divide by. Set Servings back to any number greater than 0 to return to normal per-serving analysis.

*See also:* [DCP is capped or jumped in a way that doesn't add up](#ts-dcp-cap), [A food or recipe shows an "insufficient amino acid data" warning](#ts-missing-aa), [Oxalate or glycemic index data isn't showing](#ts-oxalate-gi).

### C. I'm confused — something unexpected happened

#### USDA searches got slow, or started failing {: #ts-usda-slow}
Without a personal [USDA API key](#food-data), NuMa shares a demonstration key (`DEMO_KEY`) with every other NuMa user, and its rate limit is tight enough that heavy use by anyone can exhaust it, causing searches to fail temporarily for everyone. A free personal key removes this ceiling and takes about a minute to get — see [Food data — where it comes from and how it is stored](#food-data) for the sign-up steps and where to enter it (Settings, either version).

#### A deleted recipe shows up as "(deleted)" somewhere {: #ts-deleted-recipe}
This is expected, not a bug: deleting a recipe that's used as an ingredient in another recipe doesn't remove that ingredient line — it stays in place, flagged "recipe (deleted)" wherever it appears (ingredient lists, meal history, Food Use in Meals). If you later create a new recipe with a similar or identical name, NuMa offers to relink the old references to it automatically. See [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) for the full behavior and how to browse every currently-broken reference.

*See also:* [I searched for a food I know exists and got nothing](#ts-search-empty), [The food I wanted wasn't at the top of the search results](#ts-search-order), [A meal's DCP isn't showing](#ts-meal-dcp), [A past day's numbers changed after I updated my profile](#ts-day-profile).

### D. I expected to see something, and it's not there

#### A food or recipe shows an "insufficient amino acid data" warning {: #ts-missing-aa}
Some foods — especially branded or prepared products — simply don't have amino acid data published anywhere NuMa can look it up automatically. This isn't a bug; it's a genuine data gap. Two ways to close it: search for a [USDA](#gloss-usda) Foundation or [SR](#gloss-sr) Legacy equivalent (plain/raw foods are far more likely to have full amino acid data than branded ones), or fetch the missing values yourself via Claude [AI](#gloss-ai) — see [Missing amino acid profiles](#missing-aa) and [Food Cache](#food-cache-web).

*See also:* [No brand or equivalent of a food has amino acid data anywhere in USDA](#ts-no-aa-anywhere), for the harder case where neither fix above applies.

#### No brand or equivalent of a food has amino acid data anywhere in USDA {: #ts-no-aa-anywhere}
This is a step beyond [an "insufficient amino acid data" warning](#ts-missing-aa): you've checked, and no brand, no store variant, and no generic [USDA](#gloss-usda) entry for this food carries amino acid data — the whole category is a gap, not just the specific product. "Search for a Foundation/SR Legacy equivalent" doesn't help here because there's no equivalent food with the data you need.

The fix is to stop looking for an equivalent *food* and look instead for an equivalent *ingredient* — something with measured amino acid data whose composition dominates the protein in the food you're trying to estimate. Flour-based baked goods, for instance, get essentially all their protein from the flour; a legume-based product gets essentially all of its protein from that legume. [Estimating amino acids by copying from another food](#drafted-foods) is the tool that turns an ingredient like this into an estimate for your actual food — it scales the ingredient's amino acid values to match your food's own measured protein content automatically, rather than you doing that arithmetic by hand.

If more than one ingredient contributes meaningfully to the protein (a flour blend, for example), blend their profiles first, by mass fraction, before treating the result as a single stand-in. The copy-from-another-food picker copies from one source food at a time, so build the blend as its own custom food profile first — call it a **proxy food**: a temporary, scratch entry that exists only to hold the numbers you'll scale from, not something you'd search for or log a meal against. (If only one ingredient dominates, it's still worth entering as its own proxy food rather than typing numbers straight into the real food — see why below.)

Once you have a proxy food — blended or not — holding the numbers you need, there are two different ways to turn it into a usable estimate for your actual food. Pick whichever fits how you'll use that food going forward:

**Option 1 — create a new, clearly-labeled draft (the general-purpose default).** Foods → Custom Food Profiles → **Copy a cached food as a draft**, pick the real food you're missing [AA](#gloss-aa) data for (it copies that food's full nutrient snapshot — protein included — into a brand-new, independent entry), rename the copy something unambiguous like "Graham Cracker, generic (estimated AA)," then run the AA-copying picker on *that* draft, scaling from your proxy food. Web app: [Food Search](#food-search)'s **Copy as custom-food draft** link does the "copy as draft" half of this step in one click, right from the search results row (also available from Food Cache and Pantry's own ingredient search). Because the original cached food is never touched, USDA can still refresh its full nutrient profile and portions automatically if that entry ever changes. The tradeoff: this new draft doesn't retroactively reach meals or recipes that already reference the *original* food — those keep pointing at the un-estimated entry until you go swap the reference over by hand.

**Option 2 — edit the original food's AA fields directly (a deliberate exception).** If you know you'll always be logging this exact product, editing its AA data in place is often more practical: every past and future meal or recipe that already references it picks up the estimate immediately, with nothing to swap. The cost is real, though — editing *any* of a food's data marks the entire record user-modified, not just the amino acid fields, so NuMa will never again silently refresh its full nutrient profile, portions, or anything else on it from USDA; you're taking permanent manual ownership of that specific record. That's an easy trade when the food is unlikely to gain real measured data any other way — a specific branded product like Nabisco Honey Maid Grahams already has its macronutrients measured and isn't about to grow USDA amino acid data on its own, so there's little future refresh being given up.

**Worked example: graham crackers, no AA data on any brand, made from a 2:1 white-to-whole-wheat flour blend. Nabisco Honey Maid Grahams specifically are already logged in past meals.**

Steps 1–3 build the proxy food and are the same regardless of which option you pick. Steps 4 onward differ — jump to whichever option fits your situation.

Step 1 — pull measured amino acid data for both flours (USDA Foundation/[SR](#gloss-sr) Legacy entries):

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

Step 3 — enter this blend as its own proxy food (Foods → Custom Food Profiles → Create), named something like "Wheat flour blend, 2:1 white:whole wheat (proxy)," with the protein and amino acid values from Step 2 typed in directly.

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

Check your **Dietary Preference** setting (Settings). If it's set to "Plant-based only" or "Vegetarian," foods outside that category are filtered out of *every* search, comparison, and lookup in NuMa — not just from complement suggestions — so a food you know is in [USDA](#gloss-usda)'s [database](#gloss-database) can still return zero results. Temporarily switch to "All animal foods," search, then switch back.

#### The food I wanted wasn't at the top of the search results {: #ts-search-order}
This is usually not a bug — it's the order you typed your search words in. NuMa ranks results first by how many of your search words a name contains, but when there's a tie, it treats the *order* you typed your words in as a signal of priority: matching your earlier words outranks matching your later ones. So searching `milk dry instant` will favor a "milk dry ..." match over a "milk instant ..." match whenever only one of those two words is present in a given result, simply because "dry" was typed before "instant."

If that's not the priority you meant, reorder your search words so the one you care most about comes first — put the word that most distinguishes what you want right after the main food name. See [Ordering food search results](#search-ranking) in Part 6 for the full explanation of how results are ranked.

#### A meal's DCP isn't showing {: #ts-meal-dcp}
[DCP](#gloss-dcp) now computes and saves automatically every time you add, edit, or remove an item — there's no "mark complete" step required for it to appear, and an in-progress meal already contributes to that day's total. (Marking a meal **Complete** still matters for a different reason: a day containing an unmarked meal is flagged "provisional" in Daily Summary, since its total could still change.)

If DCP is still showing as missing, the real cause is the same as [an "insufficient amino acid data" warning](#ts-missing-aa): none of the meal's food items — and for recipe items, the recipe itself — have amino acid data available yet. Add [AA](#gloss-aa) data to at least one ingredient (or analyze the recipe), and DCP fills in immediately without needing to reopen or reanalyze the meal.

#### Oxalate or glycemic index data isn't showing for a food {: #ts-oxalate-gi}
Both are opt-in and off by default — this is a configuration gap, not a bug. [Oxalate data](#oxalate) needs its Settings toggle switched on (one account-wide switch, either version). [Glycemic index](#gi) needs either the built-in reference-table seed or your own annotation on that specific food; NuMa will offer to prompt you for it the first time you add a new food to your Pantry or a meal.

*See also:* [A recipe's "Complete" checkbox doesn't match its protein-completeness score](#ts-complete-confusion).

### E. The numbers don't make sense

#### DCP is capped, or jumped in a way that doesn't add up {: #ts-dcp-cap}
This is the single most common "the math looks wrong" report, and it's almost always correct behavior: [DIAAS](#gloss-diaas) itself is not capped (a high-quality food can score above 1.0), but Digestible Complete Protein (DCP) can never exceed the protein you actually absorbed, so NuMa caps it there when the two disagree. A capped DCP is genuinely good news — it means your limiting amino acid is in strong enough supply that none of your absorbed protein is going to waste. See [Why DCP Is Sometimes Capped Below the DIAAS Projection](#dcp-cap) for the full explanation with a worked example.

#### A past day's numbers changed after I updated my profile {: #ts-day-profile}
This shouldn't happen, and if it does, it's worth [reporting](#feedback) — but first check whether it's actually the documented, intentional behavior: each logged day stays pinned to whichever profile was active *when you logged it*, not whatever profile is active today, specifically so that switching profiles (illness, travel, a deliberate weight change) doesn't silently rescore your history. If the automatic pin doesn't match reality — illness or travel rarely starts exactly at midnight — you can manually reassign which profile a specific day is compared against. See [Per-day profile tracking](#day-profile) for how.

*See also:* [A deleted recipe shows up as "(deleted)" somewhere](#ts-deleted-recipe).

### F. A food's portion or serving-size data looks wrong

Most of what's below isn't NuMa misbehaving, it's a gap or error in the underlying [USDA](#gloss-usda) data NuMa displays. USDA publishes nutrient values reliably, but the *portion* records attached to a food — "1 large," "1 cup, sliced," and so on — are contributed unevenly and sometimes inaccurately. NuMa shows you exactly what USDA supplies; when that's missing or wrong, the fix is to teach NuMa the correct value yourself, once, and it's remembered for every future use of that food. (One entry below — the `pN` shortcut mix-up — is a NuMa naming rule rather than a USDA data gap; it's grouped here because it's still fundamentally a portion-editing question.)

#### A food has no "per piece" or "per egg" portion — only grams {: #ts-no-piece-portion}
Some foods that obviously come in natural units — a whole egg, a piece of fruit, a slice of bread — still have no [USDA](#gloss-usda)-supplied portion for that unit, only the generic per-100-g figures. This happens because USDA's portion records are contributed per food entry, not derived automatically from the food's description, so some entries simply never got one. It's not something NuMa can infer on its own — "1 egg" isn't a fixed weight (USDA's own size grades range from about 38 g for "Small" to 63 g for "Jumbo").

Two fixes: weigh the item once on a kitchen scale and enter that weight directly (`56g`, for instance), or teach NuMa the unit permanently via the food's [Food Cache](#food-cache-web) entry, **Portions** action. Either way, every later analysis, recipe, and meal entry for that food can then use the unit directly (`1 egg`, `2 slices`) instead of a gram weight.

#### A food has a weight portion but no cup/tablespoon equivalent {: #ts-no-volume-portion}
NuMa converts a volume measure (cup, tablespoon, teaspoon) to grams using a *density* estimate for that food — mass per milliliter. [USDA](#gloss-usda) doesn't publish density directly; NuMa derives it first from a cup, tablespoon or teaspoon portion in the food's own record, including one you've set yourself in the Portions editor. Only when the food has no such portion does it fall back to a small built-in table of common foods, mostly dried herbs and spices (see [Portion Input Formats](#portion-formats)). Outside those cases, entering a volume measure will prompt you to weigh the amount and enter the grams yourself — this is expected, not a bug, since guessing a density would silently produce wrong nutrient totals.

If you'll be entering this food by volume repeatedly, teach NuMa the conversion once: weigh a level cup (or tablespoon) of it, then use the same Portions editor as above — the [Food Cache](#food-cache-web) entry's **Portions** action. From then on, cup and tablespoon amounts for that food convert automatically.

#### A food's portion or volume conversion looks flatly wrong {: #ts-bad-portion-data}
Occasionally a [USDA](#gloss-usda) record's portion weight is simply implausible for what it describes — a "1 large" egg listed at a weight that doesn't match a scale, or a "1 cup" measure clearly sized for a different preparation than the one you have. This is a data-entry error on USDA's side, inherited as-is; NuMa doesn't second-guess or adjust USDA's published portion weights, since there'd be no reliable way to tell a genuine correction from a wrong override.

If a portion weight doesn't match what you measure: weigh your actual amount and enter the gram figure directly for that one use, and — if you'll use this food again — replace the bad portion with a corrected one via the same Portions editor (the [Food Cache](#food-cache-web) entry's **Portions** action). Custom portions you add there are yours — they aren't overwritten by a later **Refresh** of the food's nutrient data. If you're confident the USDA source itself is wrong (not just unusual), [let us know](#feedback) — it's worth tracking so other users hit it less often, even though NuMa can't correct USDA's [database](#gloss-database) directly.

*See also:* [Enter food portions as weights, not volume measures, whenever possible](#portion-formats).

#### A food's portion "pN" shortcut points to the wrong portion {: #ts-portion-numbering}
This is not a [USDA](#gloss-usda) data problem, it's a NuMa naming rule that's easy to misread: `p1`, `p2`, … always mean "the food's 1st stored portion, 2nd stored portion, …" in list order — never a portion's own description text. If you add a custom portion and type its own name in the **Description** field — say, you literally type `p1` as the description — that text has no bearing on its shortcut number. A food copied or imported from USDA usually already has a few built-in portions ("oz", "1 cup sliced," and so on) occupying the early slots, so your new one lands further down the list — often `p3` or `p4` — while `p1` still refers to whatever was already first. Typing `p1` in that situation silently applies the *wrong* portion's gram weight, with no error, since `p1` is still a valid shortcut — just not the one you meant.

Two ways to avoid this:

1. **Check the portion list shown right where you type the amount** — Foods, Recipes, and Meals all display the food's full portion set with its real shortcut number next to each entry (e.g. `p1 oz (14.2 g) · p2 1.75" square (3.0 g) · p3 …`) immediately above or below the amount field. Match against that list, not against a portion's name.
2. **Re-check after any portion edit.** Adding, removing, or reordering a food's portions renumbers every `pN` from that point on — so typing `p1` today can give a different weight than it did last week, if you've since added or removed an earlier portion. (Amounts you've already entered are safe: they were saved as grams — see [Editing or changing a food](#food-edit-consequences).) If a `pN` amount doesn't come out the way you expect, re-open that food's [Manage Portions](#food-cache-web) page and count down the list before assuming something's broken.

*See also:* [USDA standard portions and the `pN` shortcut](#portion-formats). A custom food profile copied from an existing food starts with that food's portions carried over unchanged — see [Editing the p1, p2, … portion shortcuts](#custom-foods) — so the same renumbering rule applies there too.

### G. Getting more help {: #quickhelp}

This is extremely easy, and we want you to do it. When you're having a problem the cause is NOT necessarily you! Regardless of the nature of your problem, contacting us gives us essential information needed to make things better for you and also for every other user. We very much want to hear from you if you have a problem.

1. Text Tom at 435-272-3332. Plainly state that you are having a problem with the program. A brief statement of the problem is all I need. With your phone number I can call you back and get complete details of what I need to know to resolve your problem. I will generally call you back immediately. If you prefer a different time, let me know.

2. For non-urgent problems - which generally are improvements you'd like to see - you can also email me. Provide screenshots, if you think that would help. ALWAYS TEXT ME IF YOU SEND AN EMAIL, as I do not check my email daily, and yours easily can get lost in the 100s I get every day.

---

## Part 9 — Possible Additional Features

*(Reading time: 5 minutes)*

Ideas below are listed in their current likely probability of being implemented. User feedback has a major effect on these probabilities!

---

### Expanding Revised Optimal (Recent Research) targets {: #expand-revised-optimal}
☑ **Age/sex-banded [RDA](#gloss-rda) (completed, existing feature)** and ☑ **research-backed maximum nutrient levels (completed 2026-08-11)** are both done — see [Daily Nutrient Goals](#goals) for the full RDA age/sex band table and [Maximum Nutrient Limits](#maxlimits) for all 12 built-in Tolerable Upper Intake Levels, each sourced to the [NIH](#gloss-nih) DRI tables[^9].

☐ **What's still open:** the [Revised Optimal (Recent Research)](#optimal) tier — the *above-RDA* targets, as distinct from the RDA itself — only has built-in defaults for three nutrients today: vitamin D[^12] and [EPA](#gloss-epa)+DHA[^13]. Candidates for a future addition, each needing its own specific citation the way those two already have (not a bulk table import like the RDA/[UL](#gloss-ul) work, since there's no single unified source for "beyond-RDA" targets — see the tradeoff discussed when this feature was scoped):

- **Magnesium** — some research suggests intakes above the RDA support better sleep and muscle function in older adults, though evidence is mixed enough that a single number is harder to defend than vitamin D's.
- **Vitamin K2** (as distinct from K1, which the RDA already covers) — emerging research on cardiovascular and bone benefits, not yet reflected in an official [DRI](#gloss-dri).
- **Choline** — a meaningful fraction of adults fall short of even the [AI](#gloss-ai)-level intake; whether a "revised optimal" above the AI is warranted (versus just meeting the existing RDA) needs its own look.

Each addition means the same three-part exercise done for vitamin D and EPA/[DHA](#gloss-dha): find the specific research consensus (or best available expert-body statement), a real number, and a citation good enough to stand next to the DRI-sourced RDA/UL figures without embarrassment.

### Nesting Carbohydrate and Fat subtypes under their parent nutrient {: #nesting-carb-subtypes}

☑ **Completed 2026-09-19.** Two of NuMa's macronutrient rows are actually parent totals with subordinate rows underneath — Fiber and Sugar are subsets of Carbohydrates, and Saturated/Monounsaturated/Polyunsaturated fat are subsets of Fat, the same relationship a Nutrition Facts label shows by indenting "Dietary Fiber" and "Total Sugars" under "Total Carbohydrate." Every nutrient table in NuMa (food, recipe, meal, daily-summary, and the printable report) now shows those five rows visually indented under their parent instead of as flat, same-looking rows — raised while building the [Full Nutrient Key](#nutrient-key) appendix, which surfaced the same gap. (The Top Contributors nutrient picker and the manual nutrient-entry form were left as-is — a dropdown and a data-entry form don't carry the same visual hierarchy concern a comparison table does.)

### Suggested optimum nutrition profiles by age group

A step beyond the per-nutrient targets above: a small number of pre-built *bundles* of Revised Optimal settings, one per major life stage (e.g. "Adults 65+ bone health," "Endurance athlete") that a user could load all at once instead of setting each nutrient individually. Lower priority than the per-nutrient expansion above, since it depends on that work existing first for enough nutrients to make a bundle meaningfully different from just the [RDA](#gloss-rda).

### Source citations for major assertions in the manual

This is basic. Claims must be backed up, and source citations are how it's done. NuMa is designed around nutrition research findings. To move quickly, these findings have not been referenced in the manual. They will be as soon as possible, which is to say as soon as the program is reliably working for a number of serious users.

### FAO 2013 Amino Acid Reference Values {: #fao-values}

Under development.

[//]: # "develop section"

### Full Nutrient Key

Moved to [Appendix G — Full Nutrient Key](#nutrient-key) now that it's real, not proposed — all five nutrient groups (Macronutrients, Omega Fatty Acids, Minerals, Vitamins, Phytonutrients) are covered there.

[//]: # "develop section"

### Protein ingestion timing

Under development.

[//]: # "develop section"

Resources:

* https://runningmagazine.ca/health-nutrition/could-you-be-timing-your-protein-all-wrong/

### Meal timing

Under development.

[//]: # "develop section"

Resources:

* https://www.theguardian.com/commentisfree/2026/may/05/game-changer-good-health-scientists-we-are-when-we-eat - article by expert

### What else? Well, know this...

#### Your ideas shape what gets built next {: #feature-ideas}

NuMa is an evolving tool, still actively being built out. This part exists to invite you into that process: if there's something NuMa doesn't do yet that would make it more useful to you, we want to hear about it.

No idea is too small, too ambitious, or too specific to your own situation. A feature that seems minor to you may turn out to matter to a lot of other users too — and one that seems highly personal often points to a real gap in the program. Several of NuMa's existing features started out as exactly this: one user's request.

#### How to contribute an idea

Use the same channel as [reporting a problem](#feedback):

1. **Text Tom at 435-272-3332** with a brief description of what you'd like NuMa to do, and why it would help you. He will generally call you back to get the full picture.
2. **Or email**, especially for a longer or more detailed idea — a screenshot or example is welcome if it helps explain what you have in mind. If you email, also send a text, since email isn't checked daily and a good idea shouldn't get lost in it.

There's no such thing as a request that's not worth mentioning. If you're not sure whether NuMa can already do what you want, ask anyway — the answer might be a feature you hadn't found yet, or it might be a real gap worth filling.

### Additional features now implemented

Ideas from this Part that have since been fully built, moved here (heading levels demoted) so the list above stays focused on what's still open.

#### ☑ CSV export and import for foods and recipes (completed 2026-08-11)

Foods and recipes can now both be exported to [CSV](#gloss-csv) and imported back in — on this or another NuMa install — via **Export CSV**/**Import CSV** buttons on the [Food Cache](#food-cache-web) list and on each [recipe](#recipes)'s page. A recipe's export is self-contained: it bundles every sub-recipe and food ingredient's full data along with it, so nothing has to already exist on the receiving end for the import to work, and anything that already matches by name is reused rather than duplicated. See the August 11 entries in [Recent program updates](#updates-log) for full detail.

#### ☑ Plots of individual nutrients consumed daily in relation to RDAs, user-established optimums, and maximum levels (completed 2026-09-19)

The [Nutrient Plot](#nutrient-plot) plots one or more nutrients over a chosen date range, with a dashed reference line for each nutrient's profile goal (Revised Optimal target, or [RDA](#gloss-rda)/[AI](#gloss-ai) where no Optimal is set) and a dotted reference line for its maximum limit (built-in Tolerable Upper Intake Level, or your own configured cap). See the September 19 entry in [Recent program updates](#updates-log) for full detail.

#### ☑ Glycemic index lookup against the full published reference table, by subject population (completed 2026-09-20)

Every food's [Annotate](#gi) page can now search the full ~2,487-entry Foster-Powell glycemic index table[^8] directly — pick normal glucose tolerance, impaired glucose tolerance/diabetes, or both, and NuMa lists every plausible match for you to choose from, rather than a single auto-picked guess. [Settings](#settings) has a matching default so this defaults to your own population without you having to pick it each time. See [Where GI values come from](#gi) and footnote 8 for the full source detail.

## Part 10 — Appendices

*(Reading time: 1 hour)*


### A. Raw protein, protein quality, and protein digestibility {: #appendix-protein-quality}
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

### B. Plant protein sources in your pantry {: #appendix-plant-proteins}
("pantry" here has two meanings: your actual pantry, and the pantry [database](#gloss-database) that is in NuMa (see the Foods dropdown menu), which is a list of foods in your actual pantry.)

This appendix profiles the plant protein sources currently kept in a typical [NuMa](#gloss-numa) pantry, including nutritional yeast, which is not a plant but is grouped here because it fills the same dietary role. For each source: what form it takes, where it comes from, its essential amino acid ([EAA](#gloss-eaa)) strengths and weaknesses relative to the [FAO](#gloss-fao) reference values described in [Appendix A](#appendix-protein-quality), and its typical role in cooking.

The [EAA](#gloss-eaa) notes below describe general tendencies for each food, not a substitute for running the food itself through [NuMa](#gloss-numa). Growing conditions, processing, and the specific [USDA](#gloss-usda) or Open Food Facts[^3] record behind a given entry all shift the exact numbers — use [NuMa](#gloss-numa)'s own amino acid ratio and [DIAAS](#gloss-diaas) output for precise figures. Sourcing and cost information for these foods is addressed separately, not here.

BEFORE GOING ANY FURTHER: You should know that the two most useful foods below (aside from staples like whole wheat flour) are nutritional yeast and hulled hemp seed. Both are incredibly nutritious and useful. Nutritional yeast adds umami to any food, and hulled hemp seed is invaluable when eating legumes.

#### Seeds

**Chia seeds**

- *Form:* tiny oval seeds, black or mottled grey-brown, about 1mm long.
- *Source:* *Salvia hispanica*, a flowering mint-family plant native to Mexico and Guatemala.
- *[EAA](#gloss-eaa) profile:* unusually complete for a plant seed — as worked through in Appendix A, chia clears all nine [EAA](#gloss-eaa) floors, with lysine as its narrowest margin (~1.3× the reference). One of the few standalone-complete plant proteins in this pantry.
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
- *[EAA](#gloss-eaa) profile:* a similar pattern to pecans — lysine limiting, modest sulfur amino acid content — notable mainly for omega-3 ([ALA](#gloss-ala)) content rather than protein quality.
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
- *[EAA](#gloss-eaa) profile:* one of the highest-quality plant proteins available, with high digestibility (~0.95, as noted under "[SPI](#gloss-spi)" in the Glossary) — it clears essentially every [EAA](#gloss-eaa) floor, with methionine/cysteine still its narrowest margin.
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

### C. Glycemic load (GL) and Blood Glucose Comparison {: #appendix-gl-comparison}
Glycemic load is a useful approximation, but no single formula-derived figure reliably predicts an individual's blood glucose response to a mixed meal. Three reasons account for this:

- The fat and protein suppression effect varies by person, by degree of insulin resistance, and by the specific foods involved.
- Most published [GI](#gloss-gi) values were measured in subjects with normal glucose tolerance and may not translate directly to someone with diabetes or insulin resistance. NuMa's built-in reference table[^8] does include a separate set of values measured specifically in subjects with impaired glucose tolerance — see [Where GI values come from](#gi) — but that set is smaller and doesn't exist for every food, so this caveat still applies whenever only a normal-tolerance value is available.
- Individual glucose responses to identical meals vary substantially, even in the same person on different days.

[GL](#gloss-gl) is therefore most reliable when comparing meals of broadly similar composition — two different grain-based breakfasts, for example. When meals differ significantly in fat or protein content, the calculated [GL](#gloss-gl) will understate the difference in actual glycemic impact.

#### Continuous Glucose Monitoring

The practical gold standard today is continuous glucose monitoring ([CGM](#gloss-cgm)) — devices such as the Dexcom G7 or Libre 3 that measure interstitial glucose every few minutes. A person with diabetes can eat a meal, watch their glucose curve in the accompanying app, and directly compare their own real response across different meal choices over time. No formula approaches this for accuracy in individual prediction.

#### Predictive Apps

Some applications (January AI, Levels) go a step further, using machine learning models trained on large [CGM](#gloss-cgm) datasets to predict glucose response to a described meal before it is eaten — effectively personalising the [GI](#gloss-gi) and [GL](#gloss-gl) concepts. These predictions are probabilistic rather than exact, but they represent the closest available alternative to direct measurement.

#### Clinical Practice Without CGM

For clinical guidance without [CGM](#gloss-cgm), dietitians working with people with diabetes typically use carbohydrate counting combined with qualitative judgment about fat and protein content, rather than relying on [GL](#gloss-gl) as a single summary figure. [GL](#gloss-gl) remains a reasonable guide for comparing meals similar in structure, but should not be the deciding number when fat and protein differ significantly between the options being considered.

### D. Why some foods appear only in DIAAS-boosting suggestions {: #comp-appendix}

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

### E. Portion Input Formats {: #portion-formats}
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

#### Recipes: Servings Instead of `pN` {: #portions-vs-servings}

Every `pN` shortcut above belongs to *foods*. Recipes never have a `p1`, `p2`, … list, and that isn't a missing feature — it's because recipes don't need one.

A food is measured in grams, and `pN` exists purely to hide that gram math: `p1` means "don't make me weigh out 1 medium egg myself, just use the preset." A recipe's native unit, by contrast, is already **servings** — so wherever you enter an amount of a recipe (adding it to a meal, or adding it as a nested ingredient inside another recipe), you get a plain **Servings** field, and typing `1` there already means exactly "1 serving." There's no gram math to shortcut, so there's no `pN` to shortcut it with.

That doesn't mean a recipe's per-serving weight is undefined — it's derived automatically from two fields on the Edit Recipe page's Recipe details section: **Number of servings** and **Total yield weight**. Divide one by the other and you get grams per serving, live, the moment both are filled in — nothing extra to set. A recipe with `servings = 21` and `total yield weight = 1942.5 g`, for example, already means "1 serving = 92.5 g" everywhere that recipe is used, without you ever typing 92.5 anywhere.

The one place the literal text `p1` *does* work for a recipe is the [Convert](#convert) tool — type `p1` there for a recipe and it resolves to that same auto-derived "1 serving" weight. That isn't a general recipe feature, though: Convert happens to reuse the same portion-parsing code that handles foods' `pN`, and it treats a recipe's one implicit "1 serving" as if it were portion #1. Everywhere else in the app, just use the Servings field directly.

92.5 g is accurate, but it doesn't say what you're actually holding. If a recipe's serving has a natural real-world name — 1 muffin, 1 cookie, 1 slice — set it in the **Serving description** field, right next to Number of servings on the Edit Recipe page. This doesn't change the math at all; it's a label, not a unit conversion. Once set, it shows up as "(1 serving = 1 muffin)" wherever the recipe's serving count is already shown — the recipe's own page, the Recipes list, Convert's named portion, and next to the Servings field anywhere the recipe is added as an ingredient or meal item.

**Where you see that weight.** Anywhere an amount is given in servings — a recipe added to a meal, or a recipe used as an ingredient inside another recipe (a [sub-recipe](#gloss-sub-recipe)) — NuMa now prints the gram weight beside it, as in "2 servings (500 g)", on screen and on a printed recipe alike. It uses the recipe's stated Total yield weight where you have set one, and otherwise the sum of the ingredients, but only when every ingredient has a usable weight: a partial sum would understate the serving by an unknown amount, so nothing is shown at all in that case.

See also [Recipe Ingredient List](#recipe-ingredients) for where these Servings fields appear, and for the Recipe details fields — including Total yield weight and Total yield volume — on the Edit Recipe page.

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

### F. Worked validation example — meal-level DIAAS for pinto beans + quinoa {: #appendix-diaas-validation}
This appendix lets you verify [NuMa](#gloss-numa)'s protein quality calculation independently. Every step is shown explicitly so you can reproduce it in a spreadsheet or calculator, then compare your result with what [NuMa](#gloss-numa) produces when you enter these two foods as a meal.

#### The two foods

| Food | [FDC ID](#gloss-fdc-id) | Data type | [USDA](#gloss-usda) source |
|------|--------|-----------|-------------|
| Beans, pinto, mature seeds, cooked, boiled, with salt | 173796 | [SR](#gloss-sr) Legacy | https://fdc.nal.usda.gov/food-details/173796/nutrients |
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

#### Step 3 — Applying digestibility to get digestible IAA amounts

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

#### Step 4 — The FAO reference amounts for this meal

The [DIAAS](#gloss-diaas) method scores each pooled digestible [IAA](#gloss-iaa) against how much of that IAA a *reference protein* of equal weight would provide. The reference values, from [FAO](#gloss-fao) Food and Nutrition Paper 92 (2013), Table 6, are expressed in **mg of IAA per gram of total protein** for older children, adolescents, and adults.

The full table is in [FAO 2013 Amino Acid Reference Values](#fao-values), in Part 9. The relevant values are:

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

#### Step 6 — Interpreting the result

A composite [DIAAS](#gloss-diaas) ≥ 1.0 means the meal's protein is fully complete relative to the [FAO](#gloss-fao) reference. Values below 1.0 indicate partial completeness — the lower the value, the more the [limiting amino acid](#gloss-limiting-amino-acid) constrains usable protein.

For this meal:

- **Leucine** is the limiting [IAA](#gloss-iaa) at 0.921. This is not surprising: leucine is the most abundant IAA in animal proteins, but plant proteins generally provide less of it relative to total protein.
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
3. Save the meal and open it. The meal page itself is the analysis screen.
4. Scroll to **Protein Summary** (total protein and DCP) and **Protein Analysis (DIAAS)** (composite score and per-[IAA](#gloss-iaa) ratios), or click those headings in the side outline.

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

### G. Full Nutrient Key {: #nutrient-key}

All five nutrient groups from the Nutrient Analysis table are covered below. Each entry gives a plain-language description of one nutrient NuMa tracks, links to where it's discussed elsewhere in this manual, and a link to a respected outside source for anyone who wants to go deeper than a nutrient table can show. Amino acids aren't repeated here — they already have their own extensive treatment; start at [Essential Amino Acids](#aa).

Every nutrient below matches one of NuMa's own internal data keys one-for-one (shown in *italics*), so a technically inclined reader can cross-reference it directly against the program's data or code.

---

#### Macronutrients

**The indentation below shows the real parent/child relationship among these** — Calories, Protein, Carbohydrates, and Fat are the four independent top-level macronutrients (none is a subset of another); Carbohydrates and Fat each break down further into the sub-rows nested beneath them. NuMa's own nutrient tables (food, recipe, meal, and daily-summary pages, plus the printable report) show this same hierarchy visually too — Fiber, Sugar, and the three fat types are indented under their parent row, the way a Nutrition Facts label does (completed 2026-09-19, see [Part 9](#nesting-carb-subtypes)).

##### Calories {: #key-calories}
*calories* — The energy a food provides, from protein, carbohydrate, fat, and alcohol combined. NuMa estimates your personal daily calorie target using the Mifflin-St Jeor equation and your activity level — see [Daily Nutrient Goals](#goals) for the full calculation and the [RDA](#gloss-rda)/[DRI](#gloss-dri) framework it draws on[^9].

##### Protein {: #key-protein}
*protein_g* — Builds and repairs every cell in the body and is the nutrient NuMa focuses on most closely, since how much of it your body can actually *use* depends on both digestibility and amino acid completeness, not just the gram total on a label. See [Digestible Complete Protein](#dcp) and [Essential Amino Acids](#aa) for how NuMa scores protein quality beyond this raw figure, and [Recommended Dietary Allowances](#rda) for how your target is set. External: MedlinePlus, *Dietary Proteins*[^17].

##### Carbohydrates {: #key-carbs}
*carbs_g* — The body's primary energy source. **Fiber and Sugar below are subsets of this total, not additional to it** — Fiber + Sugar + Starch + a few minor carbohydrate types add up to the Carbohydrates figure, the same relationship a Nutrition Facts label shows by indenting "Dietary Fiber" and "Total Sugars" under "Total Carbohydrate." NuMa uses carbohydrate content, alongside a food's glycemic index, to compute [Glycemic Load](#gl). External: MedlinePlus, *Carbohydrates*[^18].

- **Fiber**{: #key-fiber} — *fiber_g* — The indigestible part of plant carbohydrate. NuMa's figure is [USDA](#gloss-usda)'s "total dietary fiber" — **soluble and insoluble combined**, not insoluble alone. The two behave differently: soluble fiber (oats, beans, apples, citrus) dissolves into a gel that slows digestion and is linked to lower cholesterol and better blood-sugar control; insoluble fiber (whole grains, vegetable skins, wheat bran) adds bulk and speeds transit, supporting digestive regularity. NuMa doesn't split the two because USDA FoodData Central only reports that breakdown for a small fraction of foods — reliably showing it would mean leaving it blank almost everywhere. Fiber is one of the few macronutrients using an Adequate Intake rather than a full [RDA](#gloss-rda) — see [Daily Nutrient Goals](#goals) for what that distinction means for your target. External: MedlinePlus, *Dietary Fiber*[^20].
- **Sugar**{: #key-sugar} — *sugar_g* — Simple carbohydrate — both naturally occurring (fruit, dairy) and added (sweeteners) — that NuMa reports as one combined total. High-sugar foods tend to raise [Glycemic Load](#gl) sharply; see that section for how NuMa weighs sugar's blood-glucose impact against a food's fiber and overall carbohydrate. External: MedlinePlus, *Sweeteners – Sugars*[^21].
- *Starch is not tracked as its own row — USDA rarely reports it as a distinct value, so it stays folded into the Carbohydrates total along with everything else that isn't Fiber or Sugar.*

##### Fat {: #key-fat}
*fat_g* — Total dietary fat. **Saturated, Monounsaturated, and Polyunsaturated fat below are subsets of this total, not additional to it** — the three add up to (approximately) the Fat figure. Fat itself sits at the same level as Protein and Carbohydrates above, not beneath them — it's a third independent macronutrient, not a subset of either. See [Omega-3 Fatty Acids](#omega3) for the specific unsaturated fatty acids NuMa tracks individually and gives their own goals. External: MedlinePlus, *Dietary fats explained*[^19].

- **Saturated fat**{: #key-saturated-fat} — *saturated_fat_g* — The fat subtype most consistently linked to cardiovascular risk when eaten in excess; most dietary guidance favors keeping intake low and replacing it with unsaturated fat where possible. External: Examine.com, *Saturated Fat*[^22].
- **Monounsaturated fat**{: #key-mono-fat} — *mono_fat_g* — Found mainly in olive oil, avocados, and many nuts; generally considered neutral-to-beneficial for cardiovascular health when it displaces saturated fat in the diet. External: MedlinePlus, *Dietary fats explained*[^19].
- **Polyunsaturated fat**{: #key-poly-fat} — *poly_fat_g* — Includes the omega-3 and omega-6 fatty acids NuMa tracks individually — see [Omega-3 Fatty Acids](#omega3) for [ALA](#gloss-ala), [EPA](#gloss-epa), [DHA](#gloss-dha), and linoleic acid specifically, and why ALA is the only one with an official intake goal. External: MedlinePlus, *Dietary fats explained*[^19].

---

#### Omega Fatty Acids

**Grouped below by fatty acid family (omega-3 vs. omega-6) — a real biochemical classification, but not a sum like Carbohydrates/Fat above:** there's no single "total omega-3" figure these three add up to; [ALA](#gloss-ala), [EPA](#gloss-epa), and [DHA](#gloss-dha) are each reported and goal-tracked independently. See [Omega-3 Fatty Acids](#omega3) for the full discussion, including why only ALA has an official intake goal and how the ALA→EPA→DHA conversion pathway works. External (covers this entire group): Linus Pauling Institute, *Essential Fatty Acids*[^23].

##### Omega-3

- **[ALA](#gloss-ala)**{: #key-ala} — *omega3_ala_mg* — Alpha-linolenic acid, the plant-based omega-3 (flaxseed, walnuts, chia, canola and soy oils). The only omega-3 with an official Adequate Intake, so it's the only one of the three with a Daily Goal.
- **[EPA](#gloss-epa)**{: #key-epa} — *omega3_epa_mg* — Eicosapentaenoic acid. No U.S. [DRI](#gloss-dri) exists for EPA on its own; the body makes some from ALA, inefficiently, or gets it directly from fish, algae, and other seafood. Set your own [Revised Optimal target](#optimal) if you want to track it against a number.
- **[DHA](#gloss-dha)**{: #key-dha} — *omega3_dha_mg* — Docosahexaenoic acid, the omega-3 most concentrated in the brain and retina. Like EPA, it has no official DRI and can be tracked against a self-set [Revised Optimal target](#optimal) instead.

##### Omega-6

- **Linoleic acid (LA)**{: #key-la} — *omega6_la_mg* — The essential omega-6 fatty acid. Tracked for completeness; most diets, plant-based or not, comfortably exceed its Adequate Intake, and it has no known deficiency risk in typical eating patterns.

---

#### Minerals

**Grouped below by the standard nutrition-science split between macrominerals (needed in gram-per-day amounts) and trace minerals (needed in milligram or microgram amounts)** — a categorical family, like Omega-3 vs. Omega-6 above, not a sum relationship.

##### Macrominerals

- **Calcium**{: #key-calcium} — *calcium_mg* — Builds and maintains bone, and supports nerve and muscle function. A major dietary source for many people (dairy, fortified plant milks, leafy greens) is undermined by [oxalates](#antinutrients) in some of those same leafy greens — spinach's labeled calcium is largely unabsorbed. External: Linus Pauling Institute, *Calcium*[^24].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: mainly a supplement risk, not a food risk — getting this much from food alone is difficult. [NIH](#gloss-nih) notes higher-dose calcium supplements are linked to a greater risk of kidney stones, and some research ties them to a higher risk of cardiovascular disease[^48].
- **Magnesium**{: #key-magnesium} — *magnesium_mg* — Involved in hundreds of enzyme reactions, including energy production and muscle/nerve function. A candidate for a future [Revised Optimal](#optimal) target above the [RDA](#gloss-rda) — see [Part 9](#expand-revised-optimal) — though the evidence for a specific above-RDA number is less settled than for vitamin D. External: Linus Pauling Institute, *Magnesium*[^25].
- **Phosphorus**{: #key-phosphorus} — *phosphorus_mg* — Works alongside calcium in bone structure and is also central to cellular energy (ATP). Deficiency is rare in any diet with adequate protein, since phosphorus is present in most protein-rich foods. External: Linus Pauling Institute, *Phosphorus*[^26].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: NIH notes high intakes seldom cause problems in otherwise healthy people; the real concern is chronic kidney disease, where the kidneys can't clear excess phosphorus and it builds up in the blood, worsening bone and kidney health[^49].
- **Potassium**{: #key-potassium} — *potassium_mg* — Supports fluid balance, nerve signaling, and healthy blood pressure; typically under-consumed relative to its Adequate Intake in a typical Western diet. External: Linus Pauling Institute, *Potassium*[^27].
- **Sodium**{: #key-sodium} — *sodium_mg* — The one nutrient in NuMa's tables with its own Maximum column entry rather than a Minimum — see [Recommended Dietary Allowances](#rda) for the Maximum-vs-UL distinction and [Maximum Nutrient Limits](#maxlimits) for how NuMa flags approaching it. External: Linus Pauling Institute, *Sodium*[^28].

##### Trace Minerals

- **Iron**{: #key-iron} — *iron_mg* — Carries oxygen in red blood cells. Plant (non-heme) iron absorbs far less efficiently than animal (heme) iron and is further blocked by [phytates](#antinutrients) — NuMa raises the iron [RDA](#gloss-rda) target 1.8× on a Vegetarian or Plant-based dietary preference to reflect this; see [Diet-Aware Bioavailability Notes](#diet-bioavailability)[^4]<sup>,</sup>[^5]. External: Linus Pauling Institute, *Iron*[^29].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: acute overdose (often accidental, in children) can cause severe gastrointestinal damage and organ failure; chronically, people with hemochromatosis (an inherited iron-overload condition) should avoid iron and vitamin C supplements, since excess iron builds up and can damage the liver and heart[^50].
- **Zinc**{: #key-zinc} — *zinc_mg* — Supports immune function and wound healing; absorption is reduced by the same [phytates](#antinutrients) that affect iron. NuMa raises the zinc RDA target 1.5× on a Vegetarian or Plant-based preference — see [Diet-Aware Bioavailability Notes](#diet-bioavailability)[^4]<sup>,</sup>[^6]. External: Linus Pauling Institute, *Zinc*[^30].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: nausea, vomiting, and gastric distress in the short term. Sustained high doses interfere with copper absorption, which can itself cause neurological problems (loss of coordination, numbness, weakness) if it leads to copper deficiency[^51].
- **Iodine**{: #key-iodine} — *iodine_mcg* — Required for thyroid hormone production. Iodized salt is the primary dietary source in most Western diets; those avoiding it (and not eating much seafood or dairy) are the main deficiency risk group. External: Linus Pauling Institute, *Iodine*[^31].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: ironically similar to deficiency — high intakes can trigger goiter and thyroid gland inflammation. Very large single doses (gram-range, essentially unreachable from food) can cause burning of the mouth and throat, fever, and vomiting[^52].
- **Selenium**{: #key-selenium} — *selenium_mcg* — An antioxidant-supporting trace mineral; Brazil nuts are an unusually concentrated source (a couple a day can exceed the daily target). External: Linus Pauling Institute, *Selenium*[^32].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: chronic over-intake causes selenosis — hair loss, brittle nails, a garlic odor on the breath, and nausea are the classic signs; very high intakes can affect the nervous system and, rarely, the heart[^53].

---

#### Vitamins

**Grouped below by the standard fat-soluble vs. water-soluble split** — fat-soluble vitamins are stored in body fat and can build up to toxic levels with excess supplementation; water-soluble vitamins are not stored the same way and excess is typically excreted in urine (vitamin B6 is a partial exception at very high supplemental doses). Again a categorical family, not a sum relationship.

##### Fat-Soluble

- **Vitamin A**{: #key-vitamin-a} — *vitamin_a_mcg* — Supports vision, immune function, and cell growth. NuMa's figure is already expressed in mcg RAE (Retinol Activity Equivalents) — [USDA](#gloss-usda)'s own standardized unit that converts provitamin-A carotenoids (see Beta-carotene and Alpha-carotene under Phytonutrients below) into vitamin-A-equivalent amounts using their own conversion factors, not a simple sum. External: Linus Pauling Institute, *Vitamin A*[^33].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9] (that UL applies to preformed vitamin A specifically, a narrower figure than the mcg RAE total NuMa tracks — see the note there; [NIH](#gloss-nih) notes there's no established UL for beta-carotene and other provitamin-A carotenoids).
    - Risk of excess: getting too much preformed vitamin A (usually from supplements, liver, or certain medicines, rarely from food alone) can cause headache, blurred vision, nausea, dizziness, and coordination problems; long-term excess is also linked to reduced bone strength and, in pregnancy, to birth defects[^54].
- **Vitamin C**{: #key-vitamin-c} — *vitamin_c_mg* — An antioxidant vitamin also needed for collagen synthesis; notably, vitamin C consumed at the same meal significantly improves absorption of non-heme iron from plant foods — see [Antinutrients](#antinutrients). External: Linus Pauling Institute, *Vitamin C*[^34].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: mostly mild — diarrhea, nausea, and stomach cramps at high intakes. In people with hemochromatosis (an iron-overload condition), high-dose vitamin C can worsen iron overload and tissue damage[^55].
- **Vitamin D**{: #key-vitamin-d} — *vitamin_d_mcg* — Supports calcium absorption and bone health. NuMa's built-in [Revised Optimal](#optimal) default goes above the standard [RDA](#gloss-rda) based on Endocrine Society guidance[^12] — see that section for why. External: Linus Pauling Institute, *Vitamin D*[^35].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: essentially a supplement-only risk (sun exposure and food don't cause it). Excess vitamin D drives calcium too high in the blood (hypercalcemia) and urine, which in turn can cause nausea, weakness, and mineral deposits in soft tissue and blood vessels[^56].
- **Vitamin E**{: #key-vitamin-e} — *vitamin_e_mg* — An antioxidant vitamin that protects cell membranes from oxidative damage; found concentrated in nuts, seeds, and vegetable oils. External: Linus Pauling Institute, *Vitamin E*[^36].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: a supplement-only risk — NIH notes no adverse effects from vitamin E in food, only from high-dose supplements. The main concern is bleeding risk, since high doses reduce the blood's ability to clot; this is especially relevant alongside blood-thinning medication like warfarin[^57].
- **Vitamin K**{: #key-vitamin-k} — *vitamin_k_mcg* — Needed for blood clotting and bone metabolism. NuMa tracks vitamin K1 (from the RDA); vitamin K2, a distinct form with separate emerging research on cardiovascular and bone benefits, is not yet reflected in an official [DRI](#gloss-dri) — see [Part 9](#expand-revised-optimal) for that as a candidate future addition. External: Linus Pauling Institute, *Vitamin K*[^37].

##### Water-Soluble

- **Thiamin (B1)**{: #key-thiamin} — *thiamin_mg* — Needed for converting food into energy and for nerve function. Deficiency (beriberi) is rare in a varied diet but historically arose in populations relying heavily on unenriched white rice. External: Linus Pauling Institute, *Thiamin*[^38].
- **Riboflavin (B2)**{: #key-riboflavin} — *riboflavin_mg* — Supports energy production and functions as an antioxidant; widely available in dairy, eggs, meat, and fortified grains, so deficiency is uncommon. External: Linus Pauling Institute, *Riboflavin*[^39].
- **Niacin (B3)**{: #key-niacin} — *niacin_mg* — Involved in energy metabolism and [DNA](#gloss-dna) repair. Corn-based diets can carry a deficiency risk (pellagra) unless the corn is nixtamalized — see **Bound niacin** under [Antinutrients](#antinutrients). External: Linus Pauling Institute, *Niacin*[^40].
- **Vitamin B6**{: #key-b6} — *b6_mg* — Involved in amino acid metabolism and neurotransmitter synthesis. One of the few water-soluble vitamins where very high long-term supplemental doses (not food intake) carry a real toxicity risk (nerve damage). External: Linus Pauling Institute, *Vitamin B6*[^41].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: people almost never get too much B6 from food. Taking high-dose supplements for a year or longer can cause severe, sometimes irreversible nerve damage (loss of control of body movements), along with painful skin patches and extreme sun sensitivity[^58].
- **Folate**{: #key-folate} — *folate_mcg* — Essential for cell division and DNA synthesis; especially critical before and during early pregnancy to prevent neural tube defects. External: Linus Pauling Institute, *Folate*[^42].
- **Vitamin B12**{: #key-b12} — *b12_mcg* — Needed for nerve function and red blood cell formation. Almost exclusively animal-sourced[^7] — NuMa shows a specific low-intake warning on a Plant-based only dietary preference; see [Diet-Aware Bioavailability Notes](#diet-bioavailability). External: Linus Pauling Institute, *Vitamin B12*[^43].

---

#### Phytonutrients

**Grouped below into carotenoids (a defined chemical family) vs. everything else** — again categorical, not a sum. Phytonutrients have no established Dietary Reference Intake, so none of these show a "% of daily target" figure the way vitamins and minerals do — see [Recommended Dietary Allowances](#rda).

##### Carotenoids

- **Beta-carotene**{: #key-beta-carotene} — *beta_carotene_mcg* — A provitamin-A carotenoid (orange/red pigment in carrots, sweet potatoes, squash); the body converts it to vitamin A, feeding into the Vitamin A (RAE) figure above via [USDA](#gloss-usda)'s own conversion factor rather than a simple sum.
- **Alpha-carotene**{: #key-alpha-carotene} — *alpha_carotene_mcg* — A second provitamin-A carotenoid, generally present alongside beta-carotene in orange vegetables, converted to vitamin A less efficiently.
- **Lycopene**{: #key-lycopene} — *lycopene_mcg* — The red carotenoid in tomatoes and watermelon; unlike the two above, it has no vitamin A activity — it's tracked purely for its own antioxidant interest.
- **Lutein + Zeaxanthin**{: #key-lutein} — *lutein_zeaxanthin_mcg* — Carotenoids concentrated in the retina, where they're associated with eye health; found in leafy greens, corn, and eggs. Also no vitamin A activity. External (covers all four carotenoids above): Linus Pauling Institute, *Carotenoids*[^45].

##### Other Phytonutrients

- **Choline**{: #key-choline} — *choline_mg* — Needed for cell membrane structure and neurotransmitter synthesis; a meaningful share of adults fall short of even its Adequate Intake — a candidate for a future [Revised Optimal](#optimal) target, see [Part 9](#expand-revised-optimal). External: Linus Pauling Institute, *Choline*[^44].
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: a fishy body odor is the classic tell (from a choline metabolite excreted in sweat and urine); [NIH](#gloss-nih) also lists low blood pressure, sweating, and liver damage at high intakes, with some research linking very high intakes to cardiovascular risk[^59].
- **Beta-sitosterol**{: #key-beta-sitosterol} — *beta_sitosterol_mg* — A plant sterol structurally similar to cholesterol; dietary intake is associated with modestly lower [LDL](#gloss-ldl) cholesterol. External: Linus Pauling Institute, *Phytosterols*[^47].
- **Isoflavones**{: #key-isoflavones} — *isoflavones_mg* — Plant compounds with mild estrogen-like activity, found mainly in soy; frequently discussed in the context of soy's role in a plant-based diet. External: Linus Pauling Institute, *Soy Isoflavones*[^46].

---

## Part 11 — Recent program updates log {: #updates-log}

*(Reading time: 1 hour, 27 minutes)*


<!-- "Aside from being an update log for the user to access, this section is also used by create_release.py when a release is cut. New dated entries go below the "Insert new updates below here" marker, under today's "#### Month Day updates" heading and beneath the running "#### Next release summary to this point" heading, which sits directly under the marker and above the dated entries; each entry starts with MANUAL: or PROGRAM:, and each also gets a one-line bullet added under that running heading. At release time, create_release.py takes everything between the marker and the nearest "#### Release ... summary" heading as that release's notes, and renames that "Next release summary to this point" heading in place to "#### Release <tag> summary" -- the entries themselves are never rewritten or moved, so the running summary simply becomes that release's summary. The "(dated details below)" suffix is appended only when dated entry sections actually follow the summary. On the release page itself the running heading reads "#### Summary" instead, since work that is "next" in the manual is exactly what that release shipped (create_release.py rewrites that one line in the notes it sends, not in the manual). Once a release is cut, its notes are copied into the GitHub release body permanently -- nothing re-reads the manual afterward, so anything below a release summary heading is safe to prune anytime; it can't retroactively change a past release's notes."-->
<!-- # "If there is nothing pending under the marker at release time, create_release.py falls back to the generic "Automated build from main." message instead of real notes." -->

Program updates, and major manual updates, are logged here. They are grouped by program release dates.

Each entry has a bold-font title and a plain-language description — anywhere from one sentence to a short paragraph — of what you can now do or what changed.

<!-- Many entries also carry a fenced "Scope:" block underneath, with the technical detail (menu path, files touched, root cause). It is developer-facing only: the next comment explains why it is wrapped in an HTML comment and therefore never reaches a reader of the built manual. -->
<!-- Scope blocks below are hidden from the rendered manual (and from GitHub's rendered release notes, which pull this section verbatim -- see scripts/create_release.py) for the reason above: they're developer-facing detail with no value to the average user reading the Recent program updates log. Left visible only in this markdown source for anyone editing it. -->
<!-- Insert new updates below here -->

#### Next release summary to this point (dated details below)

- An amount entered as a portion ("2 p1"), shown as "2 × 1 large egg", can now be saved again from Edit Recipe without changing it; before, NuMa rejected its own wording.
- A food added to a meal now keeps the amount you typed ("1/3 c") as well as its grams, so meal pages show both, the Edit box offers what you typed, and a later portion correction or "≈ generic" mark reaches meal amounts too.
- A new install no longer opens with a warning about data problems in the starter foods and recipes; the Home page now warns only about problems in your own data.
- A food whose calories are flagged but are actually right (vanilla extract, whose calories come from alcohol) now has a **These calories are right** button.
- Open Food Facts foods saved before September 11 now show their carbohydrate; meals that include them are recalculated.
- Nutrient analysis tables now explain their Revised Optimal columns in a note under the table, with a link to the manual.
- Pressing Enter in a box that reloads the page (such as "Base the scale above on" under a complement suggestion), or any button that brings you back to the same page, now leaves you where you were on the page instead of at the top.
- MANUAL: Part 1 now starts with "Download and install the program" (section A); the sections that were A to E are now B to F.
- Nutrient plots now show a break in the line for a day with no data, and pick up again at the next one; with "Always end on last complete day", an earlier day with an incomplete meal is left out the same way instead of dragging the line down. Smoothing uses only the days that have data.
- Nutrient plot smoothing now uses the logged days before the plot's start, so the first points are smoothed like the rest; a note under the plot says how it was smoothed, and when too few earlier days exist, how many points at the start are less smoothed.
- Settings → 9 now shows, under each improved starter food or recipe, exactly what updating would change in your copy (values side by side, your own edits marked), and describes each new one.
- Recipe amounts converted with a generic density (a volume for a food with no cup or spoon weight of its own) are now marked "≈ generic" with a footnote, and Foods → 9 lists those foods so you can measure and add their real weights. Millilitre portions now count as volume portions.
- "Amounts that no longer match" now has a **Keep as entered** button for amounts whose stored grams are right; kept amounts are marked as such on Foods → 9 and the food's Portions page, and can be un-kept. Foods → 9 now also lists volumes with a bracketed weight ("1/3 c (42 gr)").
- Cup, tablespoon and teaspoon amounts now use a food's plain portion rather than a whipped or packed one, so 3/4 c of heavy cream is 179 g, not 90 g.
- USDA portions are now read correctly: a half-cup portion is no longer stored as a whole cup, and USDA "Foundation" foods now come with their portions.
- Changing a food's portion weight now lists, on its Portions page, the recipe and meal amounts entered by volume that the change affects, ready to update in one click; recipes start ticked, past meals unticked.
- Refresh from USDA can keep a food's current values as an older version (U171477.1) for meals logged before a date you choose, so past meals keep what you actually ate then.
- NuMa now knows which of a food's values you changed: the food's page lists them beside the originals, Refresh keeps only those unticked (USDA's updates to the rest are ticked), and a food stops being "user-edited" once none of your changes remain, with a note telling you before you apply.
- A ✎ after a food's code now marks a food you've edited, on every page that shows codes, including the Food Use pages; Find duplicate foods now says "user-edited" too.
- Every food and recipe now has one short code: U171477 for USDA foods, UD4 for foods you entered, R21 for recipes, OFF3 and the like for other databases. Codes replace the old ID numbers throughout, and the Substitute tool takes codes instead of a kind plus an ID number.
- Food Use in Meals now gives a sub-recipe its own row when you eat it inside another recipe, so it counts as eaten; Food Use in Recipes now says it covers your recipe book, not what you eat.
- Starting NuMa now opens its browser tab straight away, showing "Loading NutriMagnus…" until the program is ready.
- Top Contributors no longer shows a food with a small share as "0.0 g": tiny amounts and percentages get extra decimal places (0.04 g, 0.3%).
- Pressing Alt+Shift+M (or clicking Meals & Log) while on a meal now takes you to the Meals & Log list; Settings → 8 has default columns and a **Restore default columns** button; Settings → 7 stays open after **Load recommended…**; Settings → 11–13 have shortcut keys (G, Y, D); and Chromium is listed once under Browser to Launch.
- Foods → 9 now lists the foods you use that have no amino acid data or no portion weights (folded up, most-used first, each with a "not needed" box), and **Find duplicate foods** shows same-named foods so you can keep one or mark them not duplicates; importing Claude AI's data now shows what it changed.
- Data checks: Foods → 9 now also finds impossible values and recipe amounts that no longer match their food's portions (fixable in one click) and lists USDA copies over a year old; the Home page says when new data problems turn up (Settings → 13 turns it off or adds a routine reminder); and adding a food with a problem to a meal or recipe says so right away.
- After you fix a food or an amount, NuMa shows which recipes and logged meals changed and by how much; calorie notes say how much of a total is measured; and past days note when and why their totals were recalculated.
- MANUAL: New section "Checking your data" (Part 6, I) lists every data check NuMa makes: what it catches, where it appears, and what to do about it.
- New calorie checks: a food that arrives with protein, carbs and fat but no calories gets an estimated calorie figure, a food whose calories don't fit its own protein, carbs and fat is flagged, and a meal, recipe or daily summary says when its calorie total includes either kind, or a food with no calories at all.
- Refresh from USDA now shows the food's USDA ID number and which kind of USDA record it is (Branded, SR Legacy, Foundation…), and warns when that doesn't match the type NuMa has on file, so a wrong ID is easy to spot before you take anything.
- Many USDA "Foundation" foods (almonds, walnuts, soy milk, avocado and others) now come in with their calories; before, they arrived with protein, carbs and fat but no calories, so meal and recipe calorie totals came out too low.
- A cup, tablespoon or teaspoon amount now uses the food's own saved portion (say, your 99 g cup) to work out grams, instead of NuMa's built-in table for foods like flour.
- A recipe's page now shows each ingredient's amount the way you entered it ("14.7 g (2 T)"), instead of a guess from the food's saved portions or "No portion/weight data exists".
- On Edit Recipe, adding, editing, moving or removing an ingredient now leaves the page where you had it scrolled, instead of jumping elsewhere.
- Recipes, Food Cache and My Pantry now have a **Show archived …** / **Hide archived …** button in place of the "Show archived" checkbox. Unticking that checkbox didn't hide archived entries again; the button does, and it is filled in while they're showing.
- On Edit Recipe, saving, moving or removing an ingredient while Recipe details has unsaved edits no longer brings up "Leave page?": NuMa asks once, then saves those details for you first, as adding an ingredient already did.
- **Fill in nutrients from another food** now copies amino acids too, scaled to this food's protein, and NuMa remembers they're estimates so USDA's measured values can replace them later.
- Refresh now shows USDA's fresh copy beside the food's own values and lets you tick which to take, keeping your edits unless you choose otherwise; the meal page's **Refresh from USDA** fills in missing values only. A new **Fill in nutrients from another food** button works the same way for any food, not just custom profiles.
- On Annotate a Food, just searching the GI lookup no longer makes **Skip for now** ask about unsaved changes, while a GI value you picked from the lookup but haven't saved now does get that warning.
- On Edit Custom Profile you can check search results and compare them, nutrient by nutrient, with the profile you're editing; the Compare page then has a button straight back to where you were.
- Clicking Delete (or Copy) on a list like Custom Profiles no longer brings up "Leave site?" just because something was typed in that page's "Create a new profile" box or a similar small form.
- A food's page now shows its current DIAAS value (and GI, where the GI line above does not already show it) next to the **Add or edit GI / DIAAS estimates** button, so after annotating a food you can see straight away that the values were saved.
- Running a search (or re-sorting results) with unsaved edits on Edit Custom Profile, Edit Recipe's Recipe details, or a meal's Rename / change date no longer brings up a "Leave site?" warning: NuMa saves your edits first, then tells you so and offers to undo that save.
- A new missing-nutrient-data check (Foods → 9) lists foods with no data for a whole nutrient group; mark a gap "not needed" (say, macronutrients for basil) and NuMa stops raising it. Claude AI prompts now ask only for what's missing, and importing the reply fills gaps without touching values you already have.
- MANUAL: "Editing or changing a food" now explains exactly how a typed amount (`p1`, a cup, an ounce) becomes grams, and what does and doesn't change when you later edit that food's portions.
- Logged recipes now show grams beside their servings wherever a meal is listed (or say "weight unknown" and why), and if a recipe's serving size changes after you've logged it, the meal page asks whether to keep the amount you actually ate.
- MANUAL: A new note, "Where NuMa fills gaps: estimates and estimation", lists every place NuMa estimates missing data — protein digestibility, the 25-food complement list, your own amino acid estimates — and where it leaves a food out instead.
- Editing a food or recipe now also updates the saved figures of every meal that uses it, so the Meals & Log list and Daily Summary no longer show numbers from before the edit; the manual has a new section on what each kind of edit changes.
- MANUAL: Abbreviations in the appendices are now spelled out or linked to the Glossary, section by section, like the rest of the manual; DNA and LDL have new Glossary entries.
- MANUAL: The updates log is now its own Part 11 at the end of the manual, the appendices are relettered A–G, and every Part shows its own reading time under its heading.
- MANUAL: "ISO", the international standard behind the GI lookup's **non-ISO method** flag, is now in the Glossary and linked where it appears.
- Mutation testing run against this week's two most-changed modules: real test gaps closed in glycemic load totals and in the two-food complement pairs.
- MANUAL: Weekly sweep — the Settings overview now lists all twelve numbered sections, the new recipe Notes field is documented, and the updates log is trimmed to the last two weeks.
- **Save recipe details** on the Edit Recipe page works again. Since September 24 it had silently saved nothing — if you edited a recipe's name, servings or instructions since then, check that the change is there.
- A food's page no longer shows the starter-data curation button, which was only ever meant for the program's maintainer.
- A food you've edited now shows where it came from and that you changed it ("SR Legacy · user-edited"), and fetching a food again no longer erases its GI and DIAAS values.
- Clearing starter data now keeps every starter food or recipe you've renamed, edited or annotated, and any starter recipe you still use.
- Loading starter data no longer replaces a food you already have, or deletes the GI and DIAAS values you gave it, and never confuses a recipe of yours with a starter recipe of the same name.
- Starter foods can now come with a glycemic index value already filled in, and "curator notes" that held nothing but commas are gone.
- A food that turns up more than once in a meal — two servings of the same recipe, say — now gets one oxalate row with its amounts added together, instead of one row per serving.
- If you do not record glycemic index data, one tick-box in Settings now stops NuMa asking for GI values altogether, rather than having to say so food by food.
- The home page now tells you when glycemic index lookups are not using your own 2021 table — including when a table you built has gone missing — and Settings has a tick-box to turn those notices off for good if you do not record GI data.
- The manual's search box has two new checkboxes, **Match case** and **Whole words only**, so short terms like "AI" or "GI" can be found without matching every word that contains those letters.
- NuMa now tells you which starter foods and recipes an update adds or improves, both before you install it and the first time it runs, and lets you choose which to take; new installs start with an empty pantry.
- A new setup checklist, linked from the home page and Settings, walks you through first-time setup, or setting up again after losing your data; the manual also now explains how to back up your data.
- Every Settings section is now numbered, 1 to 12, in order; Alt+Shift+0 now opens section 10, Browser to Launch.
- On Windows, the update-available message now links straight to the manual's update steps and names your NuMa folder; after any update, the manual now tells you to refresh open User Manual tabs (F5).
- MANUAL: "Database" is now in the Glossary, and every mention of a database in the manual links to it.
- The 2021 glycemic index tables can now be added from Settings: download the two PDFs, choose them, click **Build** — no command line, and it works in the downloadable program too.
- Every Food Cache row now has an **Add to pantry** button (or shows **In pantry**), and the Food Cache can be sorted by ID.
- The home page's "Current manual version" date now always matches the latest manual edit, instead of lagging until the manual itself was opened.
- The Annotate page's guide to reading a GI lookup result now says plainly that each result is one row of NuMa's own GI database, and the **non-ISO method** explanation is a bullet of its own instead of being buried at the end of the one above it.
- NuMa now says outright which glycemic index reference table it is searching — the bundled 2008 edition or your own locally-built 2021 one — on the Annotate page and in a new Settings section, so a local table's presence, and its silent disappearance, are both visible.
- Adding a food to a meal no longer pops up a browser warning about leaving the page, and an amount typed while the search of outside sources is still running is now kept when those results arrive.
- A whole day's glycemic load is now judged against the daily scale instead of the per-meal one, so an ordinary day no longer reads "High".
- A food's page now shows the glycemic load of the exact portion you are analyzing, not just its GI.
- Daily glycemic load can now be plotted over time, and the Trend page gives your average across the last 7, 14 or 30 days.
- The UK, Australian, French and glycemic index reference tables now actually work in the downloadable program, instead of silently finding nothing.
- MANUAL: "Standard error" is now in the Glossary, so the ±3 beside a looked-up GI value means something.
- The 2021 glycemic index tables — over 4,000 foods, with the year of each study — can now be added to your own copy of NuMa with one command; licensing prevents shipping them built in.
- Annotating a food now settles it: once you save, that food stops interrupting you when you add it, and a prompt about one estimate no longer looks like a repeat of the other.
- The Nutrient Plot legend can now sit above the plot instead of below it, and by default moves itself up there whenever it fits on one line.
- MANUAL: The manual, and NuMa itself, now say "plot" throughout for the thing the Nutrient Plot draws, rather than mixing in "chart".
- MANUAL: Everyday computing abbreviations (CSV, PDF, API, PNG, SVG, ID) are now explained in the Glossary and linked where they appear, rather than assumed known.
- MANUAL: Abbreviations are now spelled out or glossary-linked in every section they appear in, so landing in the middle of the manual no longer leaves you guessing what IOM or WHO means.
- The Digestible Complete Protein row in every nutrient table now shows its percent of your protein target, so you can see at a glance what protein quality is costing you.
- MANUAL: New explanation of why the protein RDA assumes high-quality protein, and why NuMa raises iron and zinc targets for plant-based diets but deliberately does not raise protein.
- The Daily Summary's meal listings now say how much of each food was eaten, instead of showing a bare unit.
- Returning to a long page you were just on now brings it back as you left it — same scroll position, same panels open.
- The yellow quick-return link in the navigation bar no longer sometimes points at a page that answers "Method Not Allowed".
- MANUAL: The Glycemic Index section now says straight out that every GI value is one you supplied, and is more useful about what comparing GI figures can and cannot tell you.
- Hovering a GI figure in any list now shows which reference-table row it came from.
- The oxalate reference-match page now explains its entries the same way, and every entry — there and on a food's page — says whether its value was measured in that food or estimated from a similar one.
- A GI value picked from the reference table now remembers which row it came from, shown under the GI field and on the food's own page, so you can always see what a saved figure is based on.
- The GI lookup on a food's Annotate page now explains its own results right beside the form — what "Impaired" means, what "ref Bread, 2h 76" is telling you, and what NuMa actually saves when you pick a row — with the full account in the manual.

#### Oct 5 updates

**PROGRAM: PORTION AMOUNTS CAN BE RE-SAVED AS SHOWN**

An amount you entered as a portion, like "2 p1", is shown as "2 × 1 large egg", and you can now save it again from Edit Recipe (or a meal's Edit box) exactly as shown. NuMa reads it at that portion's weight today. Before, saving it unchanged failed with "Unit "×" not recognised", so fixing just a note meant retyping the amount. Such amounts are now also checked under Amounts that no longer match. [learn more...](#stale-amounts)

<!--

```
Scope: Recipes -> Edit Recipe (ingredient Edit), Meals -> meal Edit, Foods -> 9 stale amounts.
Files: numa_app/services/portions.py (new match_portion_label(); _parse_portion_input() now wraps
_parse_portion_input_raw()), web/backend.py (_parse_portion_str() wraps _parse_portion_str_raw()
the same way), tests/test_portions.py, tests/test_web.py.
"N × description" is matched first (nothing else reads it); a bare description ("1 large egg",
stored from "p1") only when the normal parse fails. Matches the food's portion by description,
case/spacing ignored; a renamed or removed portion still fails, as before. Side effect:
data_quality.stale_amounts() now checks these labels too (previously unparseable, so skipped);
the owner's DB had 14 such amounts, none stale at the time.
```

-->

**PROGRAM: MEALS KEEP THE AMOUNT YOU TYPED**

When you add a food to a meal as "1/3 c" or "2 p1", NuMa now saves that along with the grams, the way a recipe ingredient always has. Meal pages show it after the grams ("41.8 g (1/3 c)"), the Edit box offers it back, and amounts converted with a generic density are marked "≈ generic". If you later correct the food's cup or portion weight, the meal amount is listed with the recipe amounts it affects, ready to update. Meal items entered before today kept only their grams, so they can't be checked this way. [learn more...](#stale-amounts)

<!--

```
Scope: Meals & Log -> meal page (add food, Edit), Daily Summary, day view, meal history search,
printable meal/day. Files: web/backend.py (meal_add_food and meal_update_item_post store
_parse_portion_str()'s label as meal_items.unit instead of "g"; new _annotate_food_amounts() sets
typed_note / amount_display / generic_density, called from _meal_expand_for_diaas(),
_meal_day_context(), summary, meals_search), web/templates/_food_amount.html (new macro),
meal.html (Edit prefill, "≈ generic" mark + footnote), meal_day.html, summary.html, print.html,
meals_search.html, tests/test_data_quality.py. Same label form as recipes ("0.333333 c",
"2 × large egg"), displayed via _ingredient_amount_display()/_typed_amount_note(); legacy "g"
rows show grams only. data_quality.stale_amounts() and generic_density_in_use() already read
meal_items.unit, so no change there. "Add individual ingredients" of a recipe still stores grams.
```

-->

#### Oct 4 updates

**PROGRAM: NO "DATA PROBLEMS" GREETING ON A NEW INSTALL**

A new install no longer opens with a Home page warning about data problems you've never seen. The starter foods and recipes now come with their own data checks already settled, and anything the checks do find in them is treated as already seen. The Home page warns only about problems in your own foods, recipes and meals. Foods → 9 still lists everything. [learn more...](#checking-your-data)

<!--

```
Scope: Home page DATA CHECK banner; Settings → 9 starter data; starter_data.json;
numa_app/services/demo_data.py, web/backend.py (_mark_starter_problems_seen),
scripts/export_starter_data.py, scripts/refresh_starter_data.py,
scripts/smoke_test_upgrade.py.

Found on the first fresh-install test of the release build: "NuMa found 38
data problems you haven't reviewed yet" -- 24 missing-group gaps (salt has no
vitamins, spices no amino acids), 6 food problems and 8 stale recipe amounts,
all in the starter set. The banner counts anything not in prefs
data_check_seen as new, and a new install's list is empty.

- After seeding, Load starter data, restore and Apply improvements, the scan
  keys belonging to the user's starter copies (food/gap keys by local food
  id, stale keys by owning recipe) are added to data_check_seen.
- Starter foods now ship the curator's food_data_ignores ("ignores") and
  starter recipes the positions of "Keep as entered" amounts ("kept");
  both are loaded with the item. Neither counts towards the "improved
  starter item" hash.
- Curator's data fixed: SALT carbohydrate (1333 g label error) set to 0;
  Foundation butter/olive oil given protein, carbs, calories (and the oil
  its minerals/vitamins) from SR Legacy 173430/171413; tahini's amino acids
  scaled from USDA tahini 169410; four weighed amounts kept; three updated;
  "not needed" set on spice/condiment gaps; two foods both exported as
  "* Sugars, granulated" (169655, 746784) -- recipes resolve ingredients
  by name, so a fresh install linked the cookies to the wrong sugar. The
  export now refuses duplicate names.
- Release guard: tests/test_demo_data.py fails if the shipped starter data
  produces any data-check key in a fresh DB; smoke_test_upgrade.py gains a
  fresh-install scenario that fails if the built binary's Home page shows
  the banner.
```

-->

**PROGRAM: "THESE CALORIES ARE RIGHT" FOR A FOOD WRONGLY FLAGGED**

When a food's calories are flagged as not adding up, but are actually right, its page now has a **These calories are right — stop flagging them** button. Vanilla extract is an example: its calories come mostly from alcohol, which the check can't see. **Check them again** undoes it. [learn more...](#calorie-checks)

<!--

```
Scope: food page data-problem note (_food_quality_note.html), POST
/food/{id}/data-ignore with group=calories_ok; data_quality.CALORIES_OK_KEY
skips calorie_mismatch only (missing calories and impossible values are
still checked). Stored in food_data_ignores alongside "not needed" groups.
```

-->

**PROGRAM: OPEN FOOD FACTS CARBOHYDRATE RESTORED ON OLDER FOODS**

Open Food Facts foods saved before September 11 now show their carbohydrate. Until then it was stored under a misspelled name, so NuMa read those foods as having none. Meals that include them are recalculated.

<!--

```
Scope: db.init_db() migration. nutrients_json (and source_json's nutrients,
so the fix isn't read as a user edit) "carb_g" -> "carbs_g"; the parser was
fixed 2026-09-11 but cached foods never were. Meals using each food,
directly or via a recipe, are flagged stale with a recalc-log reason.
```

-->

**PROGRAM: REVISED OPTIMAL COLUMNS NOW EXPLAINED UNDER THE TABLE**

Once you've set a Revised Optimal goal, every nutrient analysis table (meal, day, recipe, food, averages, printout) now explains its Revised Optimal columns in a note underneath, between the Maximum and UL notes: what the goal is, what the percentages measure, and where to set it. [learn more...](#optimal)

<!--
```
Scope: web/templates/_rda_definition_footer.html: note() now takes
has_optimal and adds a "Revised Optimal goal" paragraph in column order,
between Maximum and UL; every caller (meal, meal_day, summary, recipe_detail,
food_detail, food_analyze_recipe_portion, trend, print) passes has_optimal.
Manual Part 5 table-column key and the "second set of columns" paragraph
rewritten to say what Revised Optimal means and to use its current name.
```
-->

**PROGRAM: PAGE STAYS WHERE YOU WERE AFTER ENTER OR A BUTTON**

Pressing Enter in a box that reloads the page, such as "Base the scale above on" under a complement suggestion, or clicking a button that brings you back to the same page, now leaves you at the same spot on the page instead of jumping to the top.

<!--
```
Scope: web/templates/base.html (page-state memory script). Sitewide: any
same-tab form submit stashes {path, scrollY, time} in sessionStorage; on the
next fresh navigation to the same pathname (within 60 s, no #hash in the URL)
that offset wins over the per-URL remembered offset. Fixes GET forms that
re-run the page with a new query string (complements anchor_grams Enter on
/meal/N), whose new URL had no remembered offset. Skips preventDefault'd
(AJAX) submits and target != _self; forms opt out with data-scroll-top.
```
-->

**MANUAL: PART 1 STARTS WITH INSTALLING NUMA**

Part 1's "Download and install the program" section has moved to the top, as section A, since it's the first thing anyone needs. The sections that followed it are unchanged, but now lettered B to F; G, H and I keep their letters. [learn more...](#install-windows)

**PROGRAM: NUTRIENT PLOT LINES BREAK AT MISSING DAYS**

The plot now runs over every calendar day in its span: a day with nothing logged shows as a break in the line, which picks up again at the next day with data. With **Always end on last complete day**, an earlier day with an incomplete meal is left out the same way, so a partly logged day no longer drags the line down. Smoothing averages over the days that have data, as if the missing ones weren't there. Notes under the plot say how many days are missing and why. [learn more...](#nutrient-plot)

<!--

```
Scope: Summary -> Nutrient Plot; the Home page plot.
Files: db.py (meal_dates_with_incomplete()), web/backend.py (_plot_days(), _apply_smoothing() now
over available points, _smoothed_plot_series() maps onto a calendar axis, _smoothing_info()
gap_days/skipped_incomplete/plotted_days, plot_empty), web/templates/_smoothing_note.html,
nutrient_plot.html, home.html, tests/test_web.py.
Before: the x axis held logged dates only (categorical), so a day with nothing logged vanished and
the line ran straight across it, although the page and manual said it left a gap. Rolling mode
ended on the last complete day but still plotted earlier incomplete days at their partial totals;
the Home caption claimed every day after an incomplete one was left off, which was never so.
Smoothing used an index window that counted nan slots, so a gap would have shrunk the average.
All-incomplete rolling plots keep the page controls (so the mode can be unticked) and say why.
Without rolling, incomplete days are still plotted at what's logged (owner's choice, "for now").
```

-->

**PROGRAM: PLOT SMOOTHING NOW COVERS THE FIRST DAYS PLOTTED**

The Nutrient Plot's smoothing now borrows the logged days just before the plot's start date (used for the averaging, not drawn), so the first points are smoothed like all the others instead of swinging more. A note under the plot, on the Nutrient Plot page and the Home page, says how the plot was smoothed, and, if there aren't enough earlier logged days, how many points at the start are less smoothed. [learn more...](#nutrient-plot)

<!--

```
Scope: Summary -> Nutrient Plot; the Home page plot.
Files: web/backend.py (_smoothing_lead_dates(), _smoothing_info(), _smoothed_plot_series(); page,
image endpoint and index() use them), web/templates/_smoothing_note.html (new), nutrient_plot.html,
home.html, tests/test_web.py.
Before: a trailing average over the plotted dates only, so with n-day smoothing the first n-1
points averaged 1..n-1 days and the start of every line was distorted (worse the longer the
window). The window counts logged days (plot dates are logged days only). Same day, the Home
page's "only extends through the most recent day..." note was widened to the plot's 88% width.
```

-->

**PROGRAM: SEE WHAT A STARTER-DATA UPDATE WOULD CHANGE BEFORE TAKING IT**

In Settings → 9, each improved starter food now shows its values side by side (yours now, the new version), with anything you edited yourself marked **your edit** and any portions that would be added or removed; each improved recipe lists changed fields and ingredients. New starter items get a short description. [learn more...](#starter-data)

<!--

```
Scope: Settings -> 9. Starter Data (Improved in this version; Restore individual starter items);
Home page NEW STARTER ITEMS notice.
Files: numa_app/services/demo_data.py (change_details(), _food_differences(), _recipe_differences(),
_amount_text(), _unstarred(); record_version_changes/pending_changes silent=), web/backend.py
(home + Settings pass silent=_is_curator(); starter_change_details), web/templates/settings.html,
tests/test_web.py, tests/test_demo_data.py.
Details compare the user's current copy with the bundled item over exactly what apply_improvements()
rewrites (food: name, type, GI, nutrients, portions; recipe: name, description, servings,
instructions, ingredients matched without the "* " prefix). "your edit" = db.food_edited_keys().
Curator: running from source (backend._is_curator), changes are recorded silently and pending ones
dropped. The owner got the notice after the 2026-10-04 export; the offered "improvements" were only
the export's "* " name prefix, and olive oil would have lost the 100 milliliter portion the portion
repair had just added (the export predated it).
```

-->

**PROGRAM: AMOUNTS CONVERTED WITH A GENERIC DENSITY ARE MARKED, AND LISTED ON FOODS → 9**

A volume amount for a food with no cup or spoon weight of its own is converted with a generic density for that kind of food. Recipe pages and Edit Recipe now mark each such amount **≈ generic**, with a footnote suggesting you measure the food's real cup or spoon weight and add it on its Portions page; Foods → 9 lists those foods, most-used first. Millilitre portions ("100 ml") now count for volume amounts too. [learn more...](#generic-density)

<!--

```
Scope: Recipes -> recipe page / Edit Recipe; Foods -> 9 (Amounts converted with a generic density).
Files: usda_nutrients.py (density_with_source(); get_density_g_per_ml() now wraps it; milliliter/ml
anchors), usda.py, numa_app/services/portions.py (generic_density_kind()),
numa_app/services/data_quality.py (generic_density_in_use()), web/backend.py (_mark_generic_density()),
web/templates/_generic_density.html (new), recipe_detail.html, recipe_edit.html,
food_cache_db_check.html, tests/test_usda.py, tests/test_data_quality.py.
Derived on each page view from the stored unit text and the food's current portions, never stored,
so adding a real portion clears it and moves the amounts into stale_amounts(). "bracketed" kind:
"2 T (14.7 gr)" stored by older versions (14.7 g = the table's 0.5 g/ml). A typed weight never
counts. The owner's DB at the time: 16 foods, 31 amounts (protein isolates and peanut butter powder
5 each). Olive oil's Foundation "100 milliliter" portion was ignored for density before the ml anchor.
Meals added in the app stored unit "g" (the typed volume was not kept) until Oct 5, when meals
began keeping it.
```

-->

**PROGRAM: KEEP AN AMOUNT AS ENTERED; BRACKETED WEIGHTS LISTED ON FOODS → 9**

When an amount entered by volume no longer matches its food's portions but the stored grams are right (you weighed it), tick it and click **Keep as entered**: NuMa stops listing it and shows it under **Kept as entered**, with a badge, on Foods → 9 and on the food's Portions page, where **Stop keeping** brings it back. Foods → 9 now also lists volumes stored with a weight in brackets ("1/3 c (42 gr)"), unticked. [learn more...](#stale-amounts)

<!--

```
Scope: Foods -> 9 (Amounts that no longer match); Foods -> food -> Manage Portions.
Files: db.py (amount_keeps table; amount_keep/amount_unkeep/amount_keeps), numa_app/services/data_quality.py
(stale_amounts include_kept=, rows carry "kept"; scan() now include_bracketed=True), web/backend.py
(POST /food/cache/db-check/stale-amounts action=update|keep|unkeep; Foods -> 9 kept list),
web/templates/_stale_amounts_form.html (new, shared by both pages), food_cache_db_check.html,
food_cache_portions.html, tests/test_data_quality.py.
A keep is (kind, item_id, stored_g) and holds only while the item's grams still equal stored_g, so
editing the amount ends it. Bracketed rows now raise the Home DATA CHECK reminder once, like any new
problem.
```

-->

**PROGRAM: VOLUME AMOUNTS USE A FOOD'S PLAIN CUP, NOT A WHIPPED OR PACKED ONE**

When a food has several cup or spoon portions, NuMa now works out volume amounts from the plain one, using a "whipped", "packed", "heaping" or "sifted" one only if there's nothing else. [learn more...](#stale-amounts)

<!--

```
Scope: every volume amount entered for a food (recipes, meals, food page).
Files: usda_nutrients.py (get_density_g_per_ml, _QUALIFIED_VOLUME_RE), tests/test_usda.py.
Heavy cream (SR Legacy) lists "cup, whipped" 120 g before "cup, fluid (yields 2 cups whipped)" 238 g;
the first plausible volume portion won, so "3/4 c" came out 90 g instead of 179 g. Qualified
portions are now tried after plain ones; bracketed asides are ignored when classifying, and the
match is word-bounded ("unsifted" / "unpacked" count as plain).
```

-->

**PROGRAM: USDA PORTIONS NOW READ CORRECTLY**

A USDA portion such as "0.5 cup, chopped = 78 g" now keeps its "0.5", so a cup of that food weighs what it should, and USDA "Foundation" foods (granulated sugar, canned diced tomatoes and others) now arrive with their cup and spoon portions. Foods already in your cache were corrected the same day. [learn more...](#stale-amounts)

<!--

```
Scope: every USDA food fetched or refreshed; scripts/repair_usda_portions.py for cached ones.
Files: usda_api.py (usda_portion_description(), get_food_portions_raw()), usda.py,
scripts/repair_usda_portions.py (new), tests/test_usda.py, tests/test_repair_usda_portions.py (new).
Cause: _parse_food read portionDescription or modifier only. SR Legacy puts the amount in its own
field (broccoli, cooked, 168510: amount 0.5, modifier "cup, chopped", 78 g), stored as
"cup, chopped" = 78 g, so "5 c" came out 390 g instead of 780 g. Foundation entries have only
amount + measureUnit ("cup"), so they had no description and were dropped. RACC (reference
serving) entries are skipped. The repair re-fetched the owner's USDA foods: 34 corrected (renamed
only where description and grams matched the old reading exactly; dropped portions appended so
p1/p2... keep their meaning; source copies corrected too, so no food became user-edited — 30
user-edited before and after). 5 ids USDA no longer serves / timed out were left as is.
Backup: numa.db.before-portions-20261004-135318.
```

-->

**PROGRAM: CHANGING A PORTION WEIGHT NOW OFFERS TO UPDATE THE AMOUNTS IT AFFECTS**

When you add, change or remove a portion on a food's Portions page, the page now lists every recipe ingredient and logged meal amount of that food that was entered as a volume or portion and no longer matches, with the grams stored and the grams it works out to now. Recipes start ticked; past meals and amounts with a weight in brackets ("1/3 c (42 gr)") start unticked, for you to decide. [learn more...](#stale-amounts)

<!--

```
Scope: Foods -> food -> Manage Portions; Foods -> 9 (Amounts that no longer match).
Files: numa_app/services/data_quality.py, web/backend.py, web/templates/food_cache_portions.html,
tests/test_data_quality.py.
Cause: recipe/meal grams are fixed at entry. Okara flour's cup was later corrected to 99 g, but
seven recipe lines kept 41.8 g for "1/3 c" (33 g now). The Foods -> 9 check found the two typed
"0.333333 c" but skipped five stored as "1/3 c (42 gr)" (an April-era format that wrote the
computed grams in brackets), treating the bracketed figure as a weight the user typed.
stale_amounts() gains fdc_id= and include_bracketed= (rows carry bracketed/unit_after;
_bracketed_volume() strips a "(N g)" figure when what remains is a volume or portion). Foods -> 9
lists them too (see KEEP AN AMOUNT AS ENTERED above). The Portions page gets
the panel via _portion_amounts_review() on every render; the existing POST
/food/cache/db-check/stale-amounts takes portions_fdc_id to return there, and now writes
unit_after (bracketed figure dropped). The owner's seven okara rows were corrected by hand the
same day (backup numa.db.before-okara-fix-20261004-131411).
```

-->

**PROGRAM: KEEP A FOOD'S OLD VERSION FOR PAST MEALS**

**Refresh from USDA** can now keep the food's current values as an older version for meals logged before a date you choose. Past meals keep counting what you actually ate then, while later meals and recipes get USDA's new figures. Use it when a product is reformulated or USDA revises a food. An older version has its own code: the food's code plus a number, e.g. **U171477.1**. [learn more...](#keep-version)

<!--

```
Scope: db.py "Older versions" section — food_versions table, version ids in
(-9e9, -8e9], create_food_version() copies the foods row (archived, type
"<origin> · <date of the kept values>") and its annotation row, then
re-points meal_items in meals dated before the chosen day; recipes are
untouched. food_versions_of(), meal_items_before(), food_version_info()/
_id(). food_ids: classify_food_id -> "<parent code>.n" (label "Older
version", so no Refresh button), parse_code/code_sort_key/code_source_name
handle ".n". data_quality.duplicate_groups skips versions. Refresh review:
keep_version + keep_before (default today) card, version made before any
write; food page lists versions, version page links to current, success
note after apply. Tests: 5 in tests/test_food_source.py.
```

-->

**PROGRAM: NUMA NOW KNOWS WHICH VALUES YOU CHANGED**

A food you've edited now lists, on its own page, exactly which values you changed, each beside the original. **Refresh from USDA** keeps those values unticked and ticks USDA's updates to everything else. A food stops being user-edited once none of your changes are left, whether you changed a value back or took USDA's. Before you click **Write the ticked values**, a note says when this is about to happen. [learn more...](#review-incoming)

<!--

```
Scope: db.py "Source copy" section — foods.source_json (nutrients, serving
size/unit, portions as the source last supplied), diff_from_source(),
food_edited_keys(), refresh_user_edited() (user_edited now derived: edited
keys or a user annotation), set/snapshot/rebase_food_source(),
rebased_source(), edits_left_after_full_refresh(). cache_food(from_source=
True default; cache_user_supplied_food passes False). Migration backfills
the copy for unedited foods only; previously edited foods keep their flag
via mark_user_edited until a reviewed refresh. incoming_review: mine= per-key
default ticks, TRACKED_META. Review template: "yours" labels, data-tracked
checkboxes, live #edited-status-note. Food page: _your_changes() list.
demo_data.apply_improvements snapshots the starter version. Tests:
tests/test_food_source.py (14); incoming_review/test_web setups now edit
against a source copy.
```

-->

**PROGRAM: EDITED FOODS MARKED BESIDE THEIR CODE**

A food you've edited now shows a **✎** after its code, for example `U2346394 ✎`, wherever codes appear, including the Food Use pages, which have no Type column. Hover over the mark to see "user-edited". The code itself doesn't change, so you can still type it as before. **Find duplicate foods** now shows "· user-edited" in its Type column, as other pages already did. [learn more...](#gloss-code)

<!--

```
Scope: web/backend.py _code_display()/_is_user_edited() (shares food_type()'s
once-per-request user_edited id set); food_id_tag and food_id_short append
the mark + hover title for foods.user_edited = 1. New food_code() global =
bare code for form values (Substitute pre-fill). Food Use Code cells render
via food_id_short; _code_key.html explains the mark. food_duplicates.html
used raw data_type, now food_type(). Tests: pencil-beside-code (and absent
from form value), duplicates page.
```

-->

**PROGRAM: ONE SHORT CODE FOR EVERY FOOD AND RECIPE**

Every food and recipe now shows one short code: **U171477** for a USDA food, **UD4** for a food you entered yourself, **R21** for a recipe, and **OFF3**, **AFCD1** and so on for foods from the other databases. The long negative numbers and the separate ID and Kind columns are gone. On the Food Use pages, a Code column sits beside the name with a key under the table, and the Substitute tool takes codes ("Replace U171477 with R21"). [learn more...](#gloss-code)

<!--

```
Scope: food_ids.classify_food_id() now returns prefixed display codes
(U/UD/R/OFF/CNF/CoFID/AFCD/CIQUAL); CODE_PREFIXES, code_source_name(),
code_sort_key(), parse_code() added. Stored ids unchanged. Outside-source
foods get a short per-source number from a new db.food_codes table, assigned
by trigger trg_foods_assign_code on foods INSERT and backfilled oldest-first
in init_db (_init_food_codes); never deleted, so a re-cached food keeps its
code. food_id_tag now renders "(CODE)" with the source spelled out in a
hover title; export.py likewise. Raw fdc_id/recipe id displays converted to
codes in ~15 templates; "ID"/"FDC ID"/"ID#" headers renamed "Code". Food Use
pages: Code column replaces ID + Kind, _code_key.html footnote, "Code" sort
groups by prefix then number. Substitute forms take old_code/new_code
(parse_code), replacing old_kind/old_id/new_kind/new_id. Food Search's typed
FDC ID input is unchanged. Settings' starter-data lists show each food's code
in this DB (demo_data.starter_status()'s "code"), not the starter id — a custom
starter food is renumbered on load and an outside-source one is numbered
locally, so codes for UD/R/OFF... items differ between installs by design;
starter identity (starter_key, recipe uid, manifest) never used them.
```

-->

**PROGRAM: FOOD USE IN MEALS NOW LISTS SUB-RECIPES YOU ATE**

Analysis -> Food use in meals now gives a sub-recipe its own row when you eat it inside another recipe you logged, so it is counted as eaten, alongside the foods inside it. Food use in recipes now says it covers your recipe book only, not what you eat, and links to Food use in meals for actual consumption. [learn more...](#fooduse)

<!--

```
Scope: Analysis -> Food use in meals / Food use in recipes. db.py
meal_expand_food_items()'s _expand_recipe now emits a ("recipe", ref_recipe_id)
tuple for each live nested sub-recipe before recursing into it (it used to
flatten them away), matching recipe_expand_ingredient_use(). Rows are keyed by
recipe id, so a sub-recipe eaten both directly and nested merges into one row.
Substitution is unchanged: it still only reaches directly-logged meal items.
Description text on both pages and the manual's Column Guides updated. New
test: test_food_use_analysis_lists_nested_subrecipe_eaten_via_meal.
```

-->

#### Oct 3 updates

**PROGRAM: "LOADING NUTRIMAGNUS…" WHILE THE PROGRAM STARTS**

When you start NuMa, its browser tab now opens straight away and shows "Loading NutriMagnus…" until the program is ready, then turns into the Home page by itself, so you can see that something is happening during the few seconds startup takes. If NuMa can't start, the tab says so instead of showing the browser's own "unable to connect" message.

<!--

```
Scope: web/launcher.py (_bind_socket, _LoadingServer, _LOADING_PAGE/_FAILED_PAGE,
main), tests/test_launcher.py; release side: .github/workflows/release.yml,
scripts/create_release.py (_manual_links_ok).

The launcher binds the port first and answers every request with a self-
refreshing (meta refresh, 1 s) loading page from a small accept loop, opens the
browser (no 1.2 s delay any more), imports backend (the slow part), then stops
the loop and hands the SAME listening socket to uvicorn.Server.run(sockets=...),
so no request in between is refused -- it waits in the backlog. launch-web.sh's
wait-for-port loop therefore opens the browser at once too. --reload keeps the
old path (the reloader can't take over a socket bound here). Releases: the
workflow now builds user-manual.html before pytest (the link test needs it), and
create_release.py rebuilds the manual and runs tests/test_link_integrity.py
before touching GitHub, exiting 1 on a broken link. launch-web.sh: polls the port
every 0.1 s (was 0.5 s) and waits for a killed server to free the port instead of a
fixed 0.8 s, so the browser is asked for its tab sooner. On a fast machine a browser
that is slow to open a tab (snap Brave here) can still arrive after startup is done,
in which case the loading page is simply never seen.
```

-->

**PROGRAM: TOP CONTRIBUTORS SHOWS SMALL AMOUNTS INSTEAD OF 0.0**

In a meal's or recipe's Top Contributors table, a food that adds only a little of the nutrient now shows that amount with an extra decimal place or two, such as 0.04 g or 0.003 g, instead of "0.0 g" next to a share of the total. The percentage column works the same way. Anything smaller than 0.001 shows as "<0.001".

<!--

```
Scope: web/templates/_top_contributors.html, web/backend.py (_small_amount Jinja
filter "small_amount"), numa_app/services/top_contributors.py (pct rounded to 4
places instead of 1, so the filter has digits to show; display does the rounding).
```

-->

**PROGRAM: KEYBOARD WAY BACK TO A SECTION'S LIST, AND SETTINGS TIDY-UPS**

Pressing **Alt+Shift+M** (or clicking **Meals & Log**) while you're working on a meal now takes you to the Meals & Log list; coming back from another section still returns you to the meal you left, and the same holds for Recipes, Compare and Settings. In Settings, section 8 now starts with Protein, Calories, Carbohydrate, Fiber and Sugars as columns and has a **Restore default columns** button; section 7 stays open, with focus on it, after **Load recommended Revised Optimal targets** or a Save; sections 11, 12 and 13 open with **Alt+Shift+G**, **Y** and **D**; section 9 says how to get cleared starter data back; and Browser to Launch lists Chromium once. [learn more...](#web-shortcuts)

<!--

```
Scope: web/templates/base.html (nav-memory click handler, fragment-load handler),
web/templates/settings.html (sections 4, 7, 8, 9, 11-13), web/backend.py
(settings ctx, nutrient-target redirects, new POST /settings/meal-nutrients/restore-defaults,
_BROWSER_LABELS), web/launcher.py (_BROWSER_ALTERNATES),
numa_app/services/meal_list_columns.py (DEFAULT_MEAL_LIST_NUTRIENTS, saved_or_default()).

Nav memory: a section link now skips the memory redirect when the current page is
already in that section (key === here) -- previously the remembered page WAS the
current page, so the link and its Alt+Shift key just reloaded it. A URL fragment
naming a <details> now opens it and focuses its <summary> on load; nutrient-target
POSTs redirect to #nutrient-targets and the panel also renders open on those saved=
values. Meals & Log columns: prefs without a "meal_list_nutrients" key get the
defaults (an explicitly saved empty list stays empty). The Protein row is labelled
"Protein (raw, not DCP)" -- it is protein_g, and DCP is a fixed column on both lists,
so the requested "Protein (DCP)" label would have mislabelled it. Chromium: one
"chromium" choice; the launcher tries chromium then chromium-browser, and an old
saved "chromium-browser" pref still validates and shows as that choice. System
Issues uses Y because S is the Settings nav key (first data-ak match wins).
```

-->

**PROGRAM: FOODS YOU USE WITH MISSING DATA, DUPLICATE FOODS, AND WHAT A CLAUDE AI IMPORT CHANGED**

Foods → 9 has two new folded-up lists, foods you actually use that have no amino acid data and those with no portion weights, most-used first, each with a "not needed" box. **Find duplicate foods** lists foods with the same name: compare them, keep the better one (everything using the others switches to it), or mark them "not duplicates" so they aren't listed again. Importing Claude AI's data now shows which recipes and meals it changed. [learn more...](#duplicate-foods)

<!--
```
Scope: data_quality.usage_counts / missing_aa_in_use / missing_portions_in_use
(ignore keys "aa" / "portions" in food_data_ignores; the completeness save
route now accepts "portions" and a back= anchor) / duplicate_groups (_dup_name
normalisation). New /food/cache/duplicates + POST keep (db.merge_food_into:
re-points recipe_ingredients, meal_items, pantry; moves annotations and
oxalate link if the kept food has none; deletes the rest) + POST dismiss
(new table food_duplicate_dismissals, keyed by sorted fdc_ids). Claude import
confirm wrapped in _impact_snapshot; Food Cache page shows _impact_note.
The Food Cache CSV import always creates new foods, so it has no impact to
show. Tests: tests/test_data_quality.py.
```
-->

**PROGRAM: DATA CHECKS: IMPOSSIBLE VALUES, STALE AMOUNTS, OLD USDA COPIES, A HOME PAGE REMINDER, AND A NOTE WHEN YOU ADD A FOOD**

Foods → 9 now catches values that can't be right (more than 100 g of something per 100 g, more sugars than carbohydrate, and so on), lists recipe amounts whose grams no longer match what you typed (with one click to update them), and lists USDA foods not refreshed in a year. The Home page tells you when new problems appear, and adding a food with a problem to a meal or recipe says so on the spot. Settings → 13 turns the Home page note off or adds a routine reminder. [learn more...](#checking-your-data)

<!--
```
Scope: new numa_app/services/data_quality.py (food_issues, impossible_values,
stale_amounts, old_usda_copies, scan with stable issue keys). db-check page:
Food data problems / Amounts that no longer match (POST
/food/cache/db-check/stale-amounts) / USDA copies over a year old; visiting it
saves prefs data_check_seen + data_check_last_seen. Home banner
_data_check_reminder() (prefs data_check_reminder, data_check_reminder_weeks;
Settings 13, POST /settings/data-check-reminder). added_check=<fdc_id> on
meal add + recipe ingredient add redirects -> _food_quality_note.html, also
on the food page. Calorie check also wired into update_cached_food_profile
and demo_data.apply_improvements (missed earlier). Mismatch lower bound now
counts fibre at 0 kcal (cocoa false positive). Tests: tests/test_data_quality.py.
```
-->

**PROGRAM: SEE WHAT A DATA FIX CHANGED**

After you refresh a food from USDA, fill it in from another food, save a custom food, or update amounts on Foods → 9, the page lists every recipe and logged meal whose calories, protein, carbs or fat moved, with before and after figures. Calorie notes on meal, recipe and summary pages now lead with how much of the total comes from measured values, and a meal or day whose totals were recalculated because a food's data changed says when and why. [learn more...](#data-effects)

<!--
```
Scope: web/backend.py _impact_targets/_impact_snapshot/_impact_store/
_impact_pop (one-time token, in-process) + _impact_note.html, wired into
the incoming-review POST, custom-profile edit POST and the stale-amount fix.
db.recipes_using_food (recursive), meals_using_food, recipe_and_ancestors,
meals_using_recipes, mark_meal_stale; new table meal_recalc_log written by
recipe_dcp.cascade_food_change and the stale-amount fix, shown by
_recalc_note.html on meal + day summary. _calorie_warnings() now returns
{items, total_kcal, estimated_pct}.
```
-->

**MANUAL: CHECKING YOUR DATA**

A new section, Part 6 I, "Checking your data", lists every check NuMa makes on your data in one table — what it catches, where you see it, what to do — with the Home page reminder, the note after adding a food, and how NuMa shows the effect of a fix. The sections for each check now link to it. [learn more...](#checking-your-data)

**PROGRAM: CALORIE CHECKS**

NuMa now checks every food's calories against its own protein, carbs and fat. A food that arrives without calories but with those three gets an estimated figure, replaced by the real one if its source later supplies it. A food whose calories are far from what its protein, carbs and fat imply is flagged. Foods → 9 lists them all under a new **Calorie checks** section, and a meal, recipe or daily summary shows a short **Calories** note when its total includes an estimated, doubtful or missing figure. [learn more...](#calorie-checks)

<!--
```
Scope: new numa_app/services/energy_check.py; db._calorie_check() /
_apply_calorie_mark() wrapped around all three foods.nutrients_json writers
(cache_food, merge_user_supplied_nutrients, update_food_nutrients_partial):
fill 4/4/9 + mark "calories" in estimated_keys_json; re-estimate an
unchanged estimate on macro edits; clear mark when a different value
arrives. web/backend.py _calorie_warnings() (meal, recipe via
expand_recipe_ingredients, day) + _calorie_note.html; _calorie_check_rows()
+ #calories section on /food/cache/db-check. Foods with macros marked
"not needed" are skipped; mismatch notes need >= 10 kcal effect.
One-time repair 2026-10-03 on the owner's DB (backup
numa.db.before-calorie-fix-20261003-084401): calories filled from USDA
Atwater energy for 15 Foundation foods; meal 174 1527 -> 1955 kcal.
Tests: tests/test_energy_check.py, test_calorie_note_on_meal_page_and_db_check.
```
-->

#### Oct 2 updates

**PROGRAM: REFRESH FROM USDA SHOWS THE FDC ID AND RECORD TYPE**

The Refresh from USDA review screen now names the USDA record it fetched — its FDC ID number, its type (Branded, SR Legacy, Foundation…) and brand — and warns when that type differs from the one NuMa has on file, a sign the food may be filed under the wrong ID. [learn more...](#review-incoming)

<!--
```
Scope: Food Cache / food page -> Refresh -> /food/{id}/review-incoming?source=usda;
web/backend.py (food_review_incoming: usda_data_type, usda_brand in ctx),
web/templates/food_review_incoming.html (intro paragraph + mismatch note).
Prompted by fdc 1868897 "Ground Flax Seeds": cached as user-drafted SR Legacy
(data actually from SR Legacy 169414), but USDA's record 1868897 is a Branded
Jo-Lee product, so the Data type row read "Branded" with no ID to explain why.
```
-->

**PROGRAM: CALORIES NOW FETCHED FOR USDA FOUNDATION FOODS**

Foods fetched from USDA now always bring their calories when USDA has them. Many of USDA's "Foundation" foods (almonds, walnuts, soy milk, avocado, blueberries and more) report calories in a different way from other USDA foods, which NuMa didn't read, so they arrived with no calories at all and every meal or recipe using them came out too low. Foods already in your Food Cache keep their missing calories until they're refreshed from USDA.

<!--
```
Scope: usda_api._parse_food(). Foundation records often omit Energy
(nutrient id 1008 / number "208") and carry only Energy (Atwater Specific
Factors) 2048 / "958" and/or Energy (Atwater General Factors) 2047 / "957".
Now used for calories when 1008 is absent, Specific before General.
Found via meal 174: 1527 kcal shown vs ~2060 from its own 4/4/9 macros;
almonds/walnuts/soy milk had fat and carbs but no calories. 19 cached foods
affected; 16 recoverable by refresh (Butter 790508, Green onion 2727585 and
OREO 770088 have no energy at USDA at all). Tests: TestParseFood atwater
cases in tests/test_usda.py.
```
-->

**PROGRAM: YOUR OWN CUP AND SPOON WEIGHTS NOW WIN**

When you enter an amount like "1/3 c", NuMa now works out the grams from the food's own saved cup, tablespoon or teaspoon portion, including one you set yourself. Give a flour a 99 g cup and "1/3 c" comes out as 33 g. NuMa's built-in table of typical weights is now used only for a food with no such portion. Amounts already in your recipes and meals keep their saved grams; re-enter one to recalculate it. [learn more...](#portion-formats)

<!--
```
Scope: usda_nutrients.get_density_g_per_ml() — the food's own volume
portions (0.15–1.6 g/ml plausibility check unchanged) are now tried before
_DENSITY_TABLE instead of after. Reported on an okara flour with a
user-set "1 cup" = 99 g: "flour" matched the table (0.53 g/ml), so 1/3 c
stored 41.8 g. Callers: portions._parse_portion_input (typed amounts, both
volume input and the volume annotation on weight input), web/backend.py
density uses. Stored ingredient grams are not recomputed. Tests:
TestGetDensity* in tests/test_usda.py (old table-first test replaced).
```
-->

**PROGRAM: RECIPE PAGE SHOWS INGREDIENT AMOUNTS AS YOU ENTERED THEM**

On a recipe's page, each ingredient's amount now shows the grams NuMa calculates with, followed by what you entered, for example "14.7 g (2 T)". It matches what Edit Recipe shows. Only an ingredient entered in plain grams still gets a hint worked out from the food's saved portions, such as "33 g (1/3 cup)".

<!--
```
Scope: Recipes > a recipe (/recipe/<id>). web/backend.py new
_typed_amount_note() (the typed amount_display minus any gram fragment;
None for grams-only entries), set as ing["typed_note"] in the recipe-detail
context; recipe_detail.html Amount column prefers it over volume_display
(portion_amount_note), which ignored the typed amount and said "No
portion/weight data exists" for foods with no portions even when the user
had entered "2 T". Tests: test_recipe_page_amount_shows_what_was_typed,
test_typed_amount_note.
```
-->

**PROGRAM: EDIT RECIPE KEEPS YOUR PLACE AFTER INGREDIENT CHANGES**

On Edit Recipe, adding, editing, moving or removing an ingredient now leaves the ingredient list where it was on your screen. After an add from the search results, which then clear away, the list comes up into view with your new ingredient in it.

<!--
```
Scope: web/templates/recipe_edit.html scroll-restore script. It restored a
raw scrollY, which drifted whenever content above #sec-ingredients changed
height across the reload (a successful add redirects with q= so the search
results vanish; alerts come and go). Now saves #sec-ingredients'
viewport top and restores that (clamped to 40% of the viewport when it was
off-screen below, i.e. adding from results); re-applied on load + one tick
to beat [autofocus], the first-result focus script and base.html's
#fragment scroll (Move redirects to #sec-ingredients); an error alert above
the section is scrolled into view; saved state expires after 60 s.
```
-->

**PROGRAM: SHOW / HIDE ARCHIVED IS NOW A BUTTON THAT WORKS BOTH WAYS**

Recipes, Food Cache and My Pantry each have a **Show archived …** / **Hide archived …** button, which reloads the list with archived entries shown or hidden. It's filled in while they're showing and outlined while they're hidden, and NuMa remembers your choice for each page. It replaces the "Show archived" checkbox, which couldn't hide archived entries again once ticked. [learn more...](#archive)

<!--
```
Scope: new web/templates/_archived_toggle.html macro, used by recipes.html
(after Show broken recipe references, plus the empty-list branch so an
all-archived list can still be toggled back), food_cache.html (end of the
action-button row), pantry.html. Root cause: an unticked checkbox submits
no show_archived param, so _resolve_bool_pref() returned the saved pref
(True) and the list never changed. The link always sends 0|1. Test:
test_archived_toggle_button_hides_again_after_showing.
```
-->

**PROGRAM: NO "LEAVE PAGE?" WHEN EDITING A RECIPE INGREDIENT**

On Edit Recipe, saving an ingredient's changes (or moving or removing one) while Recipe details above has unsaved edits now asks once whether to save those details too, then saves both. Before, the browser's generic "Leave page?" warning popped up instead.

<!--
```
Scope: web/templates/recipe_edit.html — the pending-details submit hook
matched only /ingredient/add(-recipe); now also /ingredient/<id>/edit,
/move, /remove and /confirm-aa, all of which reload this page. Also checks
res.ok before proceeding and re-baselines the generic dirty guard too.
```
-->

**PROGRAM: FILL IN AMINO ACIDS FROM ANOTHER FOOD, PROPERLY SCALED**

**Fill in nutrients from another food** now brings amino acids across too, scaled to this food's protein rather than copied raw. If you also tick the other food's protein, the amino acid figures update on the spot to match. NuMa remembers that these values, and anything else copied from another food, are estimates, so a later Refresh from USDA ticks USDA's measured figures over them. [learn more...](#review-incoming)

<!--
```
Scope: numa_app/services/aa_estimate.py scaled_aa(); incoming_review.py
nutrient_review(estimated=); web/backend.py review GET (aa_alt, aa_note)
and POST (re-scales ticked aa_ keys to chosen-or-current protein, drops
them with no protein; notes via source_note()); meal_refresh_aa (estimated
AA eligible and replaced); db.py foods.estimated_keys_json +
estimated_keys()/update_estimated_keys(); food_review_incoming.html live
swap on #key-protein_g. Before this, a fill from another food copied AA
raw/unscaled.
```
-->

**PROGRAM: REFRESH AND "FILL IN FROM ANOTHER FOOD" LET YOU CHOOSE VALUE BY VALUE**

Refreshing a food from USDA now shows USDA's current values beside the food's own, and writes only the ones you tick. Values that fill a blank are ticked for you, and on a food you have edited your own values are kept unless you choose otherwise. The same screen powers a new **Fill in nutrients from another food** button on any food's page. It copies chosen values from a similar food into this one, so meals using it pick them up. The meal page's **Refresh from USDA** now only fills in missing values, then lists any food where USDA differs on existing ones so you can review it. [learn more...](#review-incoming)

<!--
```
Scope: Food Cache Refresh, food page (Refresh from USDA, Fill in nutrients
from another food, missing-macros "Try refreshing"), meal Refresh from USDA.
New numa_app/services/incoming_review.py; routes GET/POST
/food/{id}/review-incoming and GET /food/{id}/fill-from; templates
food_review_incoming.html, food_fill_from.html; db.update_food_fields();
merge_user_supplied_nutrients(mark_edited=) so USDA's own values don't mark
a food user-edited. Fixes a real bug: meal_refresh_aa re-cached every
eligible food wholesale via cache_food(), skipping custom foods but not
user-edited ones, silently wiping e.g. Claude-imported values — contrary to
the manual's Edit protection promise. Food Cache Refresh used to replace all
nutrients and clear user_edited. POST /food/cache/{id}/refresh (straight
replacement) remains only for the database check's unreadable-data fix.
Compare's return label also names a fill-from page.
```
-->

**PROGRAM: ANNOTATE'S "UNSAVED CHANGES" WARNING NOW MATCHES WHAT YOU DID**

On Annotate a Food, searching the GI lookup without picking anything no longer counts as an unsaved change, so **Skip for now** just leaves. Picking a GI value from the lookup and then leaving without saving now does get the warning, where before that pick could be lost without notice.

<!--
```
Scope: web/templates/base.html leave guard, food_annotate.html. The GI
lookup's query box and population select sit inside the guarded POST form;
any input/change there set the leave guard dirty. markDirty now ignores
unnamed fields (never submitted, so nothing to save). Conversely usePick()
set #gi_estimate by script, firing no event, so neither dirty tracker saw a
real unsaved pick; it now dispatches a bubbling 'change' (not 'input', whose
listener would clear the just-set gi_source). Verified headlessly: search
only, then Skip, leaves with no prompt; pick, then Skip, prompts.
```
-->

**PROGRAM: COMPARE SEARCH RESULTS WITH THE CUSTOM PROFILE YOU'RE EDITING**

Both searches on Edit Custom Profile now have a **Compare** checkbox on each result. Check a few and click **Compare checked foods with this one** to see them on the Compare page, every nutrient side by side per 100 g, with your profile first. A **← Back to editing …** button at the top of Compare takes you straight back. [learn more...](#drafted-foods)

<!--
```
Scope: Foods → Custom Profiles → Edit (food_custom_edit.html, compare.html,
web/backend.py). New GET /food/custom-profiles/{id}/compare takes pick=
"<fdc_id>|<off_code>" values, puts the profile first, caches non-USDA picks
via _get_or_cache_source_food (Compare can only live-fetch USDA), caps at
_MAX_COMPARE_ITEMS, and redirects to /compare with return_to. Compare now
accepts return_to (_safe_return_to: local paths only), shows the return
button (_compare_return_label names the profile), and threads return_to
through every add/remove/save/load/rename/delete round-trip. Checkboxes use
form="..." because the AA table's rows already hold POST forms. The compare
form is GET, so the leave guard's autosave + Undo applies.
```
-->

**PROGRAM: NO MORE "LEAVE SITE?" WHEN CLICKING DELETE ON A LIST**

Clicking a Delete or Copy button on a page such as Custom Profiles now just does what it says, after its own confirmation, even if there is leftover text in a small form elsewhere on the page. The longer edit forms with the "Data-entered safety" note still warn you before their unsaved edits are lost.

<!--
```
Scope: web/templates/base.html generic dirty-form tracker. Submitting a
tracked form already cleared every dirty flag, but a Delete/Copy button form
has no editable fields so it is untracked, and a dirty "Create a new profile"
name box then tripped beforeunload. New window-level bubble submit listener:
an un-cancelled submit of any form clears dirty flags except on
data-leave-guard forms. Verified headlessly: with text in the Create box,
Delete goes straight through; a dirty Recipe details form still warns.
```
-->

**PROGRAM: A FOOD'S PAGE SHOWS ITS CURRENT GI AND DIAAS VALUES**

Once a food has a GI or DIAAS value, its page shows them on their own line ("DIAAS set at 0.87"), followed by the **Add or edit GI / DIAAS estimates** button. A GI that is set is left off that line, since the GI and GL line higher up already shows it. After you annotate a food and come back, you can see at once that the values took. A food with neither value keeps the button in the main row of buttons, as before. [learn more...](#annotate)

<!--
```
Scope: food detail page (web/templates/food_detail.html, web/backend.py
food-detail context gains diaas_estimate). Status row id="annotation-status"
rendered only when gi_estimate or diaas_estimate is set; the unset one reads
"not set". Test: test_food_detail_shows_current_gi_diaas_beside_annotate_button.
```
-->

**PROGRAM: EDIT PAGES SAVE YOUR EDITS BEFORE A SEARCH, WITH UNDO**

On Edit Custom Profile, Edit Recipe (Recipe details), and a meal's Rename / change date, you can now run a search, or re-sort the results, while you have unsaved edits. NuMa saves those edits first, runs the search, and then shows a note at the top of the page with a button to undo that save, restoring the values the page had before. [learn more...](#web-shortcuts)

<!--
```
Scope: Foods → Custom Profiles → Edit (web/templates/base.html leave guard,
food_custom_edit.html, recipe_edit.html, meal.html, _failsafe_note.html,
_diet_pref_quick.html, _top_contributors.html). The pages' search boxes are
GET forms separate from the guarded POST form, so submitting one navigated
away and tripped the beforeunload "Leave site?" dialog. New opt-in
data-leave-guard-autosave: a GET-form submit while that form is dirty
fetch-POSTs it, re-baselines both dirty trackers (new
numaDirtyGuard.markClean), stashes the page-load form values in
sessionStorage, then submits the search. The next page load shows an Undo
banner that re-posts those values. Opt-in only because Undo is an exact
revert only where the POST rewrites every field from the submission (pinned
by test_custom_profile_autosave_undo_restores_exactly). Recipe edit POST and
meal rename POST were checked and likewise rewrite every submitted field.
Auto-submitting sort selects on those pages switched from form.submit() to
requestSubmit(), since submit() skips the submit event (and so the
autosave) and would still hit "Leave site?". Annotate needs nothing: its
edit view has no page-reloading search (the GI lookup is fetch-based).
```
-->

**PROGRAM: MISSING NUTRIENT DATA CHECK, AND CLAUDE AI FILLS ONLY THE GAPS**

Foods → 9 now also lists every food that has no data for a whole nutrient group — macronutrients, minerals, vitamins, or amino acids, plus omega fatty acids and phytonutrients if you turn those on — with a **not needed** checkbox for gaps that don't matter, like macronutrients for a spice. Check **ask AI** on just the gaps you want help with and build a Claude AI prompt for those, or from the warning on a food's own page: the prompt asks only for each food's missing values, and importing the reply fills those in while keeping everything the food already has. [learn more...](#data-completeness)

<!--
```
Scope: Foods → 9 (/food/cache/db-check, new #completeness section), food
page alert, /food/cache/claude-fetch, /food/cache/claude-import.
New numa_app/services/data_completeness.py (six groups; Macronutrients
missing if any of calories/protein/carbs/fat absent, Amino Acids only with
protein). New food_data_ignores table (fdc_id, group_key, ON DELETE CASCADE)
+ db.food_data_ignores()/set_food_data_ignore(); POST
/food/cache/db-check/completeness and /food/{fdc_id}/data-ignore.
claude_fetch.build_prompt() takes per-food requests -> "provide only:" key
lists, "not needed" group names, rule 8b. Import fix: an existing food
went through cache_food(), which replaced the whole row -- Claude's name,
portions emptied, user_drafted reset to 0 on a custom food, every value
overwritten. Now db.merge_user_supplied_nutrients() fills blank values only
(data_completeness.is_blank: absent, or 0 AA placeholder with protein);
review table shows what would change; "Also replace" checkbox = overwrite.
Food page alert now says which core macros are missing instead of "No
nutrient data available" when the record has other values (FDC 748608
olive oil: fat subtypes but no fat_g/calories).
```
-->

#### Oct 1 updates

**MANUAL: HOW AMOUNTS ARE SAVED, AND WHY EDITING A PORTION IS SAFE**

Every amount you enter for a food is saved as grams on the spot, so changing what `p1` means later leaves your recipes and logged meals exactly as they were. The manual now spells out how each kind of entry is converted and what you'll still see change. [learn more...](#food-edit-consequences)

<!--
```
Scope: user-manual.md — Part 5 "Changing a food" (#food-edit-consequences)
expanded and retitled "Editing or changing a food: nutrients, portions,
amounts, name" so manual search for "editing" ranks it; links added from Part 3 F (Recipes) and G (Meals & Log).
Corrected two errors: the old paragraph said logged meal items keep the
typed portion text (they store grams with unit "g" only — meal_add_food /
meal_replace_food in web/backend.py), and the troubleshooting tip
#ts-portion-numbering said a p1 amount entered last week "can silently mean
something else today" — false; amounts are resolved to grams at entry time
(_parse_portion_str). Renumbering only affects new entries and re-edits.
```
-->

**PROGRAM: LOGGED RECIPES SHOW GRAMS, AND A CHANGED SERVING SIZE NO LONGER SLIPS BY**

Wherever a meal's items are listed — the meal page, the day pages, Meal History Search and printouts — a recipe now reads "1 serving (295 g)", or "1 serving (weight unknown)" when its weight can't be worked out, with a footnote explaining which. If a recipe's serving size changes after you've logged it (say, its servings count goes from 8 to 4), the meal page now flags that item and lets you keep the grams you actually ate or accept the new serving size. [learn more...](#recipe-servings-grams)

<!--
```
Scope: db.py — new meal_items.serving_grams column (grams per serving at log
time); meal_item_set_serving_grams(); search_meal_history() returns it.
web/backend.py — _annotate_recipe_amounts() gives recipe items serving_g,
grams and serving_changed (and lazily records serving_grams when NULL, so
old rows and every add path are covered without touching them);
_serving_weight_changed() ignores <1% / <0.5 g; called from
_meal_expand_for_diaas (meal page, meal print), both day contexts (day page,
summary date, day print) and /meals/search. New POST
/meal/{id}/item/{item_id}/serving-weight (choice=keep rescales servings to
the logged grams; accept keeps servings); editing a recipe item's servings
re-records serving_grams against the current serving.
Templates: new _recipe_amount.html (amount() + weight_note() footnote),
used in meal.html (plus the warning row), meal_day.html, summary.html,
print.html, meals_search.html. Fixes day pages printing "1.0 1 serving".
tests/test_recipe_serving_weight.py.
```
-->

**MANUAL: WHERE NUMA FILLS GAPS: ESTIMATES AND ESTIMATION**

A new note in Part 6 sets out every place NuMa fills in missing data with an estimate — protein digestibility for every food, the built-in list of 25 protein sources behind complement suggestions, amino acids you estimate yourself — and where it leaves a food out or says "unknown" instead. The "Editing your data" section links to it. [learn more...](#filling-gaps)

**PROGRAM: MEALS NOW FOLLOW FOOD AND RECIPE EDITS**

When you edit a food's nutrients, or a recipe, every meal that uses it — directly, inside a recipe, or inside a recipe-within-a-recipe — now has its saved DCP, calories and nutrient totals brought up to date before the next page opens. The Meals & Log list, Recent Days, averages and plots no longer keep showing figures from before the edit until you happen to reopen each meal. A new manual section sets out what every kind of edit changes, including two that change less than you might expect (portions, food renames) and one that changes more (a recipe's number of servings). [learn more...](#editing-consequences)

<!--
```
Scope: db.py — new stale_meals table; mark_meals_stale_for_food(),
mark_meals_stale_for_recipes(), stale_meal_ids(), clear_stale_meal().
numa_app/services/recipe_dcp.py — cascade_food_change() flags meals logging
the food directly; recompute_recipe_dcp() flags meals logging the recipe or
any ancestor it cascaded to (so food -> recipe -> meal is covered too).
web/backend.py — _refresh_stale_meals() drains the table (flag cleared
before each recompute; failures logged to recompute_errors as entity_type
"meal", never raised) and refreshes day % goal for each affected date; run
by an HTTP middleware before every non-static GET. Flagging happens inside
the editing transaction, so the ~20 food-write routes needed no change, and
no nested DB connection is opened mid-write. System Issues Retry now handles
"meal" entries. Previously meals.bcp_g/calories/nutrients_snapshot_json were
only rewritten on opening the meal or via the Meals & Log batch button.
Manual: Part 6 D retitled "Editing your data, and what changes as a result"
(old #recipe-dcp-cascade kept as a sub-heading so existing links hold);
System Issues text now mentions meals.
tests/test_food_cascade.py — TestMealsRefreshAfterChange.
```
-->

#### Sep 30 updates

**MANUAL: APPENDIX ABBREVIATIONS NOW LINKED TO THE GLOSSARY**

Abbreviations in the appendices — IAA, RDA, NIH, EPA and the rest — now link to their Glossary entries within each section, so landing anywhere in an appendix never leaves one unexplained. DNA and LDL are new to the [Glossary](#glossary).

<!--
```
Scope: user-manual.md Part 10 (Appendices A–G) — first use per section of
ALA, SPI, SR, IAA (Steps 2–8), DCP, AA, RDA, DRI, USDA, EPA, DHA, NIH, DNA,
LDL linked to #gloss-*; "FAO FNP 92" expanded inline to "FAO Food and
Nutrition Paper (FNP) 92"; new Glossary entries DNA and LDL.
tests/test_manual_abbreviations.py — now checks everything up to Part 11,
not up to the log's insert marker (which, while the log sat at the head of
Part 10, silently excluded every appendix). Added the appendices' all-caps
label words to _NOT_ABBREVIATIONS, "G7" (Dexcom G7) to _ALLOWED, and
"January AI" (a company) to the AI other-sense pattern.
```
-->

**MANUAL: UPDATES LOG IS NOW PART 11; APPENDICES RELETTERED; READING TIME PER PART**

This Recent program updates log now has a Part of its own, at the end of the manual, so the appendices are no longer buried behind it. They are relettered A–G: protein quality is now Appendix A, the Full Nutrient Key is Appendix G. Every Part also shows how long it takes to read, just under its heading. [learn more...](#appendix-protein-quality)

<!--
```
Scope: user-manual.md — "### A. Recent program updates log" moved from the
head of Part 10 to a new "## Part 11 — Recent program updates log
{: #updates-log}" between Appendix G and Notes; old B–H relettered A–G,
with #appendix-b/-c/-d/-k anchors renamed #appendix-protein-quality,
-plant-proteins, -gl-comparison, -diaas-validation, and all in-body links
and letter references updated (older log entries left as written).
scripts/build_manual.py — per-Part reading time line under every
"## Part N" heading, regenerated each build (comment-stripped words, same
counter as the header total; strip/re-stamp round-trips exactly).
scripts/create_release.py — CHANGELOG_HEADING matches the new heading;
pending range now also ends at a "## " heading. web/backend.py
_CHANGELOG_ANCHOR -> "updates-log". scripts/audit_glossary.py heading
regex accepts ## or ###. tests/test_manual_abbreviations.py stops at
Part 10, keeping its previous coverage. CLAUDE.md, README, version.py
comments updated to say Part 11.
```
-->

**MANUAL: "ISO" IS NOW IN THE GLOSSARY**

The Glossary now explains [ISO](#gloss-iso), the international standards body whose GI measuring standard decides which rows of the GI reference tables carry a **non-ISO method** flag, and each section that mentions it links there.

<!--
```
Scope: user-manual.md -- new #gloss-iso entry (between IOM and IU);
first ISO mention linked in Part 1 Step 4, #gi-method-quality and
#gi-result-row. Flagged by this week's sweep (item 9): 16 uses, spelled
out inline per section but never defined; owner chose a Glossary entry
over inline expansion alone.
```
-->

**PROGRAM: NO VISIBLE CHANGE — MUTATION TESTING CLOSED REAL GAPS IN GLYCEMIC LOAD AND COMPLEMENT PAIRS**

Nothing you can see changed. NuMa's [test suite](#extensive-code-testing) was checked by deliberately planting small errors in the two modules that changed most this week, and the places where the tests would not have noticed are now covered. The most consequential: had the glycemic load of a meal ever started counting only its last food, no test would have caught it.

<!--
```
Scope: tests/test_glycemic_load.py (11 new tests), tests/test_usda.py
(1 new test), README-numa-documentation.md mutation-testing log.
Flagged by the weekly churn check; run at the owner's request.
glycemic_load.py (first full run; 116 new lines since 2026-09-10):
232 mutants, 57 -> 19 survivors, the 19 all equivalent (sqlite3.Row
case-insensitive keys, default-scope strings that fall back to "serving").
Gaps: no test summed two computable items (+= -> = survived on food and
recipe paths); every blocker was last in its list (continue -> break on
all four blocker branches); no-nutrient-data food, no-carbs food, deleted
recipe, 0-servings recipe, blocker tuple contents, meal_line_items()'s
recipe mapping, and rounding of day totals/averages all unexercised.
usda_nutrients.py (27 lines since 2026-09-23, the TID-not-DIAAS change):
1536 mutants, 257 -> 254 survivors. Only new-code survivors: the pairs
tier's first leg losing cand_digestibility and falling back to DIAAS,
masked because every pair test ran at base_digestibility=1.0. New
test_pair_first_leg_is_weighted_by_tid_not_diaas runs at 0.8, where
Oats + Cheddar is a real pair the DIAAS weighting would drop.
```
-->

**MANUAL: WEEKLY SWEEP — SETTINGS OVERVIEW RENUMBERED, RECIPE NOTES DOCUMENTED, LOG TRIMMED**

The [Settings overview](#settings) now lists all twelve sections by number, including Meals & Log columns, Browser to Launch, and the Glycemic Index Reference Table, and says which keyboard shortcut reaches section 10. The recipe **Notes and documentation** field is now described with the rest of the [Edit Recipe](#recipes-menu-web) page. This log now covers the last two weeks only.

<!--
```
Scope: user-manual.md, README.md, CLAUDE.md, README-numa-documentation.md,
tests/test_manual_search_js.py (new), .claude/settings.local.json.
Longer-cadence checks: none due (monthly check next sweep, in October).
Mutation churn check flagged glycemic_load.py and usda_nutrients.py; both
run (entry above). Item 1: CLAUDE.md descriptions for glycemic_load.py
(GL bands, day totals) and demo_data.py (starter identity, manifest)
brought current; numa_gen_prompt.py / numa_import_claude.py marked as
gitignored local tools. Item 2: clean. Item 3: Bootstrap 5.3.8 still
latest. Item 4: Sept 9-15 entries and the v2026-09-14-2336 boundary
pruned (1,093 lines). Item 5: Settings overview (Part 3 I) listed 10
unnumbered sections, now all 12 numbered; Alt+Shift+0 for section 10
added to the shortcut paragraph; recipe Notes and documentation field
(shipped 2026-09-24) had no body mention. Item 6: README.md key features
now cover whole-day GL, GL trend/plot, the buildable 2021 GI table, and
starter foods/recipes with the setup checklist. Item 7: manual search's
Match case / Whole words only had no test; new test_manual_search_js.py
runs build_manual.JS's wordRegex() under Node (skipped without Node).
Item 8: every manual #anchor and app /manual# deep link resolves;
template hrefs all match routes; new external URLs return 200. Item 9:
one bare AI in the new recipe-notes sentence, now glossary-linked
(caught by test_manual_abbreviations). ISO (16 uses, expanded inline in
each section, no glossary entry) flagged to the owner.
```
-->

**PROGRAM: "SAVE RECIPE DETAILS" SAVES AGAIN**

On the Edit Recipe page, the **Save recipe details** button saves your changes again, and the **View recipe** link beside it works. Since September 24 both silently did nothing: clicking Save left your edits unsaved, which is why leaving the page then warned about unsaved changes. If you changed a recipe's name, description, servings, instructions or notes since then, please check that the change is actually there. (Edits were saved if you added an ingredient straight afterwards, since that saves the details first.)

<!--
```
Scope: web/templates/recipe_edit.html. The Save button and View recipe
link sit inside the Recipe details <summary>; a click handler there called
e.preventDefault() to stop the <details> collapsing, which also cancelled
the button's form submission and the link's navigation. Browsers don't
toggle a <details> for a click on a button or link inside its summary, so
the handler was simply removed. Reproduced and verified in Chromium and
Firefox via Playwright against an isolated NUMA_DATA_DIR sandbox: no POST
before, POST and navigation after, <details> stays open. Introduced in
cc3ba18 (2026-09-24), shipped in release v2026-09-24-0941. Regression test
checks the handler is gone (the suite has no browser).
```
-->

#### Sep 29 updates

**PROGRAM: THE STARTER-FOOD CURATION BUTTON IS GONE FROM FOOD PAGES**

A food's page used to show a **Mark as starter food** / **Unmark as starter food** button. It was a tool for choosing NuMa's own starter foods and did nothing useful for anyone else, so the downloadable program no longer shows it.

<!--
```
Scope: web/backend.py (_is_curator(): true only when not sys.frozen;
is_curator() Jinja global; POST /food/{fdc_id}/toggle-starter now 404s in
the packaged program), food_detail.html. Owner's decision 2026-09-29: only
the owner runs from source, so "running from source" is the curator test;
the trade-off is that any other developer running from source sees it too.
```
-->

**PROGRAM: A FOOD SHOWS WHERE IT CAME FROM, AND WHETHER YOU'VE EDITED IT**

A food's type now always says where it came from, and a USDA or Open Food Facts food you've changed says so too: for example "SR Legacy · user-edited". Changing its nutrients or portions, or giving it a glycemic index or DIAAS value, counts as an edit. Before, editing or importing data for a USDA food could replace its type with "User Drafted", losing its origin. Also fixed: fetching a food you already had, for instance by picking it again from USDA search results, could silently erase the GI and DIAAS values you'd given it, and un-archive it. [learn more...](#cached)

<!--
```
Scope: db.py (foods.user_edited + one-time backfill; cache_food() now an
upsert; mark_user_edited, cache_user_supplied_food, user_edited_ids,
is_custom_food_id; update_cached_food_profile / update_food_portions set
the mark), web/backend.py (food_type() Jinja global; annotate save marks),
13 templates (every type display), claude_fetch.py, import_foods.py,
import_json_folder.py, numa_import_claude.py (cache_user_supplied_food),
demo_data.apply_improvements (clears the mark), new
scripts/restore_food_origins.py. Root cause of the annotation loss:
cache_food() used INSERT OR REPLACE, whose delete cascaded to
food_annotations. In the owner's DB, 5 of 9 USDA foods relabelled "User
Drafted" can be recovered from USDA; the other 4 ids (6991, 26126, 192572,
640661) are not USDA records.
```
-->

**PROGRAM: CLEARING STARTER DATA KEEPS WHAT YOU'VE MADE YOUR OWN**

**Clear starter data** now removes only starter items that are still exactly as they were loaded. A starter food or recipe you've renamed (taking the `*` off counts), edited, re-portioned, or given a glycemic index or DIAAS value is kept, and so is a starter recipe you've logged in a meal or used in a recipe of your own. Afterwards, Settings tells you how many items were kept, and why. [learn more...](#starter-data)

<!--
```
Scope: numa_app/services/demo_data.py (clear_demo_data, _food_state /
_recipe_state fingerprints stored in the marker at load, fallback to the
bundled set for older markers, refresh_fingerprints() after
apply_improvements), web/backend.py (clear route passes kept_recipes /
kept_edited), settings.html (result lines, Clear text and confirm dialog),
user-manual.md #starter-data. Previously Clear deleted every starter recipe
and every unreferenced starter food, edited or not, so an edited starter
item was lost; the old Settings text even said edited items would go.
```
-->

**PROGRAM: LOADING STARTER DATA NEVER TOUCHES WHAT YOU ALREADY HAVE**

Loading starter data used to replace any food you already had that was also a starter food, and delete the glycemic index and DIAAS values you'd given it. Now a food you already have is left exactly as it is, and clearing starter data later never removes it. Starter recipes are recognised by a permanent identity rather than by name, so a recipe of your own that happens to share a starter recipe's name is never confused with it, and a starter custom food can no longer land on top of one of your own custom foods. [learn more...](#starter-data)

<!--
```
Scope: numa_app/services/demo_data.py (_food_locations/_recipe_locations,
_insert_food/_create_recipe, _adopt_legacy_copies, ensure_recipe_uid; load,
restore, status, manifest and apply_improvements now all map starter ids to
the user's copies), db.py init_db (foods.starter_key, recipes.starter_uid,
recipes.updated_at + triggers), export_starter_data.py and
refresh_starter_data.py (ship "uid" not source_recipe_id; call init_db).
Root cause: load_demo_data called cache_food() on every starter food, and
its INSERT OR REPLACE deletes and reinserts the row; food_annotations'
ON DELETE CASCADE then dropped the user's annotations. Custom-food ids are a
local counter, so the curator's -3 could overwrite the user's own -3.
Manifest recipes are now keyed by uid; an older name-keyed manifest is
matched by name so the switch reports nothing spurious.
```
-->

**PROGRAM: STARTER FOODS CAN COME WITH GLYCEMIC INDEX VALUES, AND JUNK CURATOR NOTES ARE GONE**

A starter food can now arrive with its glycemic index value already filled in — but only a value NuMa is allowed to share: one from the 2008 international GI tables, or the curator's own estimate. Values from the 2021 tables never ship, because their licence forbids passing them on. Separately, some foods fetched through the Claude AI workflow showed "curator notes" containing nothing but commas; those are cleared the next time NuMa starts, and new imports no longer create them. [learn more...](#starter-data)

<!--
```
Scope: demo_data.py (shippable_gi() allowlist, _write_gi() on load /
restore / apply_improvements; a load or restore never replaces an existing
GI annotation), export_starter_data.py and refresh_starter_data.py (export
the "gi" entry; refresh also now forces pantry []), claude_fetch.py
parse_response() (curator text keeps only lines with letters or digits,
never fence lines), db.py init_db() migration clearing word-less
curator_notes. Root cause of the junk: a reply listing foods as a JSON
array falls to the bare-object fallback, and the separators left behind
(",\n  ,") were saved as curator notes on every food in the batch. The
owner's DB had 14 such foods from two batches (8 and 9 foods); all 14 of
its curator notes were junk. Settings and manual Starter Data text no
longer name specific recipes or claim every food is USDA with full AA data.
```
-->

**PROGRAM: OXALATE TABLE NOW ADDS UP A FOOD THAT APPEARS MORE THAN ONCE**

The Anti-nutrients section's oxalate table now shows each food once, with its grams and milligrams added together across every place it turns up in the meal — two servings of the same recipe, or a food eaten on its own and inside a recipe. The "No oxalate data for" list no longer repeats names either. [learn more...](#antinutrients)

<!--
```
Scope: Meal page / meal print / recipe page Anti-nutrients section;
web/backend.py _oxalate_for_items(), tests/test_web.py.
Quantitative rows were appended per occurrence; they are now merged by
fdc_id (or lowercased name when no id) with amount_g and mg summed, rounded
once at the end. Qualitative list was already deduped; missing list now is.
```
-->

**PROGRAM: YOU CAN NOW TELL NUMA YOU DO NOT RECORD GI DATA, AND IT STOPS ASKING**

Tick **I do not record glycemic index data** at the foot of **Settings** then **Glycemic Index Reference Table** and NuMa stops asking for glycemic index values altogether: adding a food no longer detours to the Annotate page for a GI value, the per-food "don't prompt me for a GI estimate" tick-box disappears as redundant, the GI field folds away on the Annotate page -- still there if you want it -- and the notices about which reference table is in use stop as well. Nothing already recorded is deleted or hidden, a saved GI value is still used to work out glycemic load, and un-ticking it puts everything back, including per-food prompt choices you had made. A food still missing a DIAAS estimate goes on prompting for that, since it is a separate question. [learn more...](#annotate)

<!--
```
Scope: Settings > Glycemic Index Reference Table; Foods > Annotate a Food; the
add-food detour from a meal or the pantry.

The opt-out (prefs gi_opt_out, formerly the notices-only gi_notices_off, read
with a fallback) now gates _missing_annotations(), which is the single choke
point for "what are we still asking about" -- _annotation_prompt_needed() is
built on it, so dropping GI from that list is what turns the setting from
"stop warning me" into "stop asking me". It is the global form of the existing
per-food gi_no_prompt column.

food_annotate_edit_post() carries the stored gi_no_prompt forward while the
opt-out is on, rather than reading it from the form: the tick-box is not
rendered then, and set_food_annotation() overwrites that column on every save,
so an absent checkbox would quietly clear a per-food choice that matters again
the moment the opt-out is switched back off. Enforced in the handler rather
than with a hidden field so a bare POST cannot clear it either.
```
-->

**PROGRAM: THE HOME PAGE NOW TELLS YOU WHEN GI LOOKUPS ARE NOT USING YOUR OWN 2021 TABLE**

If the glycemic index lookup is falling back to the 2008 edition that ships with NuMa, the home page now says so as soon as you start up, with a link straight to the section of Settings that builds the 2021 one. If you had built a 2021 table and NuMa can no longer find it -- moved, renamed or deleted -- that gets a warning of its own, which keeps appearing until the table is back or you dismiss it, because nothing else would have told you. Not interested in GI data at all? A new tick-box at the foot of **Settings then Glycemic Index Reference Table** turns every one of these notices off permanently. [learn more...](#gi-editions)

<!--
```
Scope: Home page; Settings > Glycemic Index Reference Table.
backend.py gains _gi_table_home_notice(), called from index(). Three states:
never built one (informational), built one and lost it (warning), and no
readable table at all (error, not silenceable -- no lookup can return
anything). The lost state is derived from a prefs-recorded
gi_table_last_seen_edition and made sticky via gi_table_lost, since the
2021 -> 2008 transition is otherwise visible for exactly one page load and
would silently soften to the generic message on the next one.

Two independent silencing mechanisms, deliberately: gi_table_notice_dismissed
is "I have read this one" and is cleared automatically whenever a 2021 table
is seen again, so a later disappearance re-arms it; gi_notices_off is the
opt-out for anyone not recording GI data, set from Settings, and suppresses
every state including the unreadable-table one. The opt-out is checked AFTER
the last-seen state is recorded, never instead of it -- a table lost during
an opt-out must still report as lost if notices are turned back on.

Tests drive edition changes through a mutable dict rather than re-patching:
monkeypatch.undo() would also revert use_test_web_prefs' _PREFS_FILE patch
(same monkeypatch instance per test), sending the notice's own prefs writes
to the real prefs.json.
```
-->

**PROGRAM: MATCH CASE AND WHOLE WORDS IN THE MANUAL'S SEARCH**

The manual's sidebar search now has **Match case** and **Whole words only** checkboxes, so you can find "AI" (artificial intelligence) without also matching *main*, *said*, or MAIN. [learn more...](#search-howto)

<!--
```
Scope: User Manual sidebar search -- scripts/build_manual.py (JS + CSS +
HTML template). Section index now keeps original-case text alongside a
lowercased copy (the lowercase copy still drives the "things you can do"
verb check). Query words are no longer lowercased; each becomes a global
RegExp (escaped, flag 'i' unless Match case, wrapped in
(?<![A-Za-z0-9_])...(?![A-Za-z0-9_]) lookarounds for Whole words only --
lookarounds rather than \b so terms starting/ending in punctuation work).
The same regexes drive section filtering, scoring, and in-section
highlighting. Both checkboxes re-run the search on change.
```
-->

**PROGRAM: NUMA TELLS YOU WHAT AN UPDATE CHANGES IN THE STARTER FOODS AND RECIPES**

When a new version adds starter foods or recipes, or improves ones you already have, NuMa now says so. The **UPDATE AVAILABLE** message tells you before you install, and a **NEW STARTER ITEMS** message appears the first time the new version runs. In **Settings → 9. Starter Data**, new items are marked **(new in this version)**, and improved ones are listed for you to update, or keep as they are, item by item. Nothing changes in your data unless you choose it, and something you deleted on purpose is never offered back to you as "new". New installs also now start with an empty pantry, since a pantry is the list of foods *you* keep at home. [learn more...](#starter-data)

<!--
```
Scope: numa_app/services/demo_data.py (starter_manifest, diff_manifests,
record_version_changes, pending_changes, preview_changes,
apply_improvements, decline_improvements, describe_changes; state in
<data dir>/starter_versions.json), update_check.py (fetches the release's
starter_manifest.json asset), scripts/create_release.py (writes and uploads
it), web/backend.py (home + Settings wiring, 3 new POST routes),
home.html, settings.html, export_starter_data.py (pantry always []),
starter_data.json (pantry emptied), tests/conftest.py fixture isolating
starter_versions.json. Previously starter_status() compared only bundled
set vs DB, so "new in this version" and "deleted on purpose" looked the
same, and an improved item the user already had was never noticed.
Improvements apply by UPDATE, not cache_food()'s INSERT OR REPLACE, so ids,
archived flags, annotations and references survive; recipes keep their id.
First run of this version records silently (nothing earlier to compare).
```
-->

**PROGRAM: A SETUP CHECKLIST FOR NEW INSTALLS, AND HOW TO BACK UP YOUR DATA**

Part 1.G of the manual is now a step-by-step setup checklist: the three settings to do first, the ones that can wait, setting up your pantry (starting from the starter foods already there), and — only if you track it — adding glycemic index values to the carbohydrate foods you eat most. It covers setting up again after losing your data, too. Until you've saved a profile, a **NEW TO NUMA?** message on the home page links to the checklist, and Settings links to it at all times. A new **Backing up your data** section says which two folders hold everything you've entered, and how to copy and restore them. [learn more...](#first-setup)

<!--
```
Scope: user-manual.md Part 1.G rewritten (#first-setup), new Part 1.F
subsection #backup; web/templates/home.html (banner shown while
profile_label is empty, i.e. load_profile() is None);
web/templates/settings.html (link under the page heading). Backup
guidance avoids needing NuMa quit: no documented way to quit on Linux
exists yet. Data dirs per platform_utils.get_data_dir/get_config_dir;
gi_data_local.json lives in the data dir, so a backup includes it.
```
-->

**PROGRAM: SETTINGS SECTIONS NUMBERED 1 TO 12**

Every section on the Settings page now has a number, in order: Browser to Launch is 10, Glycemic Index Reference Table is 11, and System Issues is 12. The keyboard shortcut **Alt+Shift+0** now opens section 10; sections 11 and 12 have no shortcut, since the number keys run out. [learn more...](#web-shortcuts)

<!--
```
Scope: web/templates/settings.html. Browser to Launch and the GI table
section had no number; System Issues was "0" so it could own Alt+Shift+0.
Now 10/11/12, with data-ak="0" moved to section 10 (the underlined 0 in
"10"). The Keyboard Shortcuts section's list also gained its missing 9
and 0 rows.
```
-->

**PROGRAM: CLEARER WINDOWS UPDATE STEPS, AND A REMINDER TO REFRESH THE MANUAL**

On Windows, the **UPDATE AVAILABLE** message on the home page now has a link straight to the update steps in this manual, and it shows the exact folder your copy of NuMa runs from, so you don't have to remember where you put it. Those steps now end with the one that's easy to miss: refresh (press F5 in) every browser tab that has the User Manual open. An open manual tab doesn't update itself, so without a refresh it quietly keeps showing the old manual. Linux's "UPDATED" message now gives the same reminder. [learn more...](#update-windows)

<!--
```
Scope: Home page update banners (web/templates/home.html): the Windows
branch (new self_update.windows_exe_dir(), passed as windows_exe_dir by
backend.py's index route) keeps the Download button, adds a manual_link
to #update-windows and the exe folder; the Linux "UPDATED" banner gains
the F5 reminder. user-manual.md Part 1F Windows item g rewritten as five
steps with anchor #update-windows (step 2 now says closing the black
window alone quits, so the manual tab can stay open to read from); item
c's "once-ever" claim corrected, since a replaced unsigned .exe can
re-trigger SmartScreen. Windows locks a running .exe, so is_available()
stays Linux-only. A first draft put the whole procedure in the banner
itself, which told the user to close the very tab they were reading.
```
-->

**MANUAL: "DATABASE" EXPLAINED IN THE GLOSSARY**

The manual talks about databases constantly — the online ones NuMa looks foods up in, the ones bundled with it, and your own. "Database" now has a plain-language Glossary entry explaining all three, and every mention of the word in the manual links to it. [learn more...](#gloss-database)

<!--
```
Scope: user-manual.md Glossary (#gloss-database, between CSV and DCP), plus
links on every prose occurrence of "database(s)" outside Appendix A. Left
unlinked: indented column-legend code blocks, the GI section heading about the
Sydney database, proper names ("Australian Food Composition Database",
"Glycemic Index Database"), and reference/footnote citation titles. This
deliberately departs from the usual one-link-per-passage convention, at the
owner's request.
```
-->

#### Sep 28 updates

**PROGRAM: BUILD THE 2021 GI TABLES FROM SETTINGS**

You can now add the 2021 glycemic index tables — over 4,000 foods, each with the year it was tested — without a command line. Download the two PDFs from the publisher, choose them in **Settings → Glycemic Index Reference Table**, and click **Build my 2021 GI table**. About a minute later the Annotate page's GI lookup is searching them, with no restart. This works in the downloadable program as well, not just from source code. [learn more...](#gi-editions)

<!--
```
Scope: Settings -> Glycemic Index Reference Table; numa_app/services/gi_table_build.py
(new: the parser moved out of scripts/build_gi_data.py, now a thin CLI over it),
gi_lookup.py (user_table_path(), reload()), web/backend.py
(POST /settings/gi-table/build, settings_get), web/templates/settings.html,
requirements.txt (+pdfminer.six), tests/test_build_gi_data.py, tests/test_web.py.
pdftotext (poppler) replaced by pdfminer.six so packaged Windows/Linux builds can
parse -- verified in a PyInstaller onefile probe (139 pages, 2,091 rows). Word y
uses baseline + 0.9*size, not pdfminer's descender-based bbox top, which split
one wrapped name; against the pdftotext build every row's name/GI/SEM/year/
country/subjects/ref matches bar one name pdftotext had wrong (a "Jujubes"
heading glued onto grapefruit). Tables identified from their own "Supplemental
Table N." heading, so upload order is irrelevant. Bad input (same table twice,
not a table, <1,500 rows) raises BuildError and writes nothing; output replaced
atomically. Build runs on a thread (~70 s); Settings reloads itself every 4 s
while running, shows the outcome once. Also fixed: gi_lookup cached its table
for the whole process, so a new/deleted local table was not seen until restart
despite Settings saying otherwise.
```
-->

**PROGRAM: ADD TO PANTRY FROM THE FOOD CACHE, AND SORT IT BY ID**

Each food in the Food Cache now has an **Add to pantry** button that puts it in your Pantry and brings you straight back to the same spot in the list. Foods already there show **In pantry** instead, which opens the Pantry. The Food Cache's "Sort by" list also has a new **ID** choice. [learn more...](#food-cache-web)

<!--
```
Scope: Foods -> Food Cache; web/backend.py (food_cache_get, _FOOD_CACHE_SORT_KEYS,
pantry_add), web/templates/food_cache.html, tests/test_web.py.
The row button posts to the existing /pantry/add with a new optional `next`
field (local paths only; "//host" rejected) so it returns to
/food/cache?q=..&sort=..#food-<fdc_id> instead of /pantry -- also threaded
through the annotation-prompt detour. "In pantry" counts archived pantry rows
too. Rows got id="food-<fdc_id>" for the return anchor. Same session: the
details>summary tint in style.css doubled (#f0f4f8 -> #e1e9f1) so collapsible
headers read as controls; Annotate's GI lookup results now scroll inside
their card instead of spilling over the reading-guide panel.
```
-->

**PROGRAM: HOME PAGE MANUAL DATE STAYS CURRENT**

The "Current manual version" date on the home page now always reflects the latest change to the manual. Before, it could show an older date until you opened the manual itself.

<!--
```
Scope: Home page; web/backend.py home route, tests/conftest.py, tests/test_web.py.
The stamp is read from the built user-manual.html, which only /manual rebuilt
(manual_build.rebuild_manual_if_stale) -- so an edit to user-manual.md showed
up at once in the home-page Preface excerpt (read live from the .md) but not
in the stamp beside it. The home route now runs the same stale-check rebuild
(in a threadpool; a no-op unless the .md is newer) before reading the stamp.
Tests stub the rebuild autouse so none can rewrite the repo's real html.
```
-->

#### Sep 27 updates

**PROGRAM: THE GI LOOKUP GUIDE NAMES THE DATABASE, AND SPLITS OUT ITS NON-ISO NOTE**

The guide beside the GI lookup on a food's Annotate page is now headed **Reading a GI database lookup result**, and opens by saying that each result is one row of NuMa's own GI database -- so "row" is anchored to something concrete before the bullets start using the word. The **non-ISO method** explanation is now a bullet in its own right, rather than extra sentences tacked onto the end of the **tested 1992** bullet above it, where it had no bullet marker of its own and read as a continuation of a different point. [learn more...](#gi-result-row)

<!--

```
Scope: Foods > Annotate a Food, the gi-lookup-guide aside in
web/templates/food_annotate.html.

Heading now reads "Reading a GI database lookup result"; both edition branches'
lead-in paragraphs open with "Each result is one row of NuMa's GI database."
Defining the term once was preferred over substituting "database row" at every
mention: two of the bullets ("the published table's own footnote marker", "which
of that edition's two tables the row sat in") refer to rows of the published
Atkinson tables, not of NuMa's database, and that contrast is the whole point of
those bullets -- blanket substitution would have made them wrong.

The non-ISO text was inside the "tested 1992" <li>, so it rendered as trailing
prose within that bullet with no marker and no break. Split into its own <li>.
Source newlines were not the cause; HTML collapses them.
```

-->

**PROGRAM: NUMA NOW SAYS WHICH GLYCEMIC INDEX TABLE IT IS SEARCHING**

The GI lookup on a food's Annotate page now carries a badge saying which published edition is answering it -- **2021 edition** when you have built your own local copy, **2008 edition** when it is the table bundled with NuMa -- with the food count, the build date and the split between the two editions' rows inside the panel. A new **Glycemic Index Reference Table** section in Settings gives the same account in full, and, if you are on the 2008 baseline, the one command that builds the 2021 tables and every path NuMa will look for the result in. That section opens itself in the 2008 case, since falling back is the state you are least likely to have noticed. The panel's own guide to reading a result now matches whichever edition you actually have, rather than describing the 2008 row shape to everyone. [learn more...](#gi-editions)

<!--
```
Scope: Foods > Annotate a Food; Settings > Glycemic Index Reference Table.
gi_lookup.py gains active_table_info() (edition, path, build date, row counts,
per-edition split, subject-group counts) and local_table_candidates(); both
were unobservable before -- active_table_path() existed but nothing called it,
so an install could silently lose gi_data_local.json and drop back to 2008
with no indication anywhere. backend.py passes gi_table into the annotate and
settings contexts.

The side-panel "Reading a GI lookup result" guide is now edition-aware. Its
"Impaired" bullet was wrong for 2021 rows: it described population as "which
of the two published tables it came from" and folded in few-subjects/wide-
variability, which is 2008 A1/A2 semantics. Under 2021 population is the row's
own Subjects cell and the method concern is the separate non-ISO flag, so the
bullet now splits the two and the worked example shows the row shape the
reader will actually see.

Tests cover both configurations (the suite must pass whether or not the
developer running it has built a local table); verified by temporarily hiding
gi_data_local.json and re-running.
```
-->

**PROGRAM: ADDING A FOOD TO A MEAL NO LONGER WARNS ABOUT LEAVING THE PAGE**

Type an amount, click "Add to meal", and the food is added -- no "Leave site?" dialog to dismiss first. An amount you type while NuMa is still searching USDA and the other outside sources is now kept when those results arrive, too, instead of being quietly cleared, and one you type and then abandon is still warned about as before. [learn more...](#web-shortcuts)

<!--
```
Scope: Meals > a meal > Add Food or Recipe.
Two bugs, both from the search table being built in two passes (local rows
server-rendered, then the whole tbody replaced with the merged local+
external set).

1. base.html's unsaved-changes guard snapshotted every POST form once, at
load. The replace left the forms it was tracking detached-but-dirty, and
their replacements tracked by nothing -- so the submit handler that clears
the dirty set no longer existed on the form being submitted, and
beforeunload fired on a submit the user had just asked for. That script now
exposes window.numaDirtyGuard {track, recheck, prune}; meal.html prunes the
discarded rows and tracks the new ones around the replace. prune() also runs
in beforeunload, so no detached form can pin the warning on.

2. meal.html called snapshotRows() before issuing the fetch rather than in
its .then(), so the "carry field values across the replace" snapshot was
always of untouched fields -- exactly the case it was added for (typing
during the external search) was the one it missed. Moved into .then(), just
above the innerHTML assignment. restoreRows writes values programmatically
and fires no input event, hence numaDirtyGuard.recheck() after it.

Verified with Playwright against an isolated instance: dirty on typing
before and after the merge, value preserved across the merge, cleared on
Add, still set when abandoned.
```
-->

**PROGRAM: DAILY GLYCEMIC LOAD CAN NOW BE TRACKED OVER TIME**

Glycemic load is now something you can watch a trend in, rather than only read one day at a time. The Nutrient Plot offers **Daily glycemic load** as a plottable series alongside the nutrients, and Summary then Trend shows your average daily GL across the last 7, 14 or 30 days with its band. Both leave out any day whose GI coverage is incomplete, rather than counting it as a low day, and both tell you how many days actually went into the figure. A weekly average is the number worth acting on -- a single day swings with whatever happened to be eaten. [learn more...](#gl)

<!--
```
Scope: Summary > Nutrient Plot, Summary > Trend.
numa_app/services/glycemic_load.py gains day_gl_total()/day_gl_totals()/
average_day_gl() plus meal_line_items(), so day-level GL lives beside the
existing per-meal aggregation instead of being re-derived per call site.
backend.py adds _GL_PLOT_KEY ("gl") as a second pseudo-nutrient alongside
_DCP_PLOT_KEY -- GL is not a NUTRIENT_MAP key and has no unit, so it is
excluded from the shared-unit y-axis label and from goal/limit reference
lines (a GL profile target does not exist yet). summary_trend() computes
avg_gl/avg_gl_days/gl_unknown_dates; trend.html renders them with the
skipped dates named. An unknown day is None, never 0.0 -- a partially
annotated day would otherwise understate the average.
```
-->

**PROGRAM: A FOOD'S PAGE NOW SHOWS THE GLYCEMIC LOAD OF THE PORTION YOU ARE LOOKING AT**

When a food has a GI annotation, its page now shows the glycemic load for the exact amount you entered, with its band, next to the GI. Halve the portion and the GL halves while the GI stays put -- which is the whole reason GL is the more useful of the two numbers. The printable version of the page picks it up as well, as its own "Glycemic load" section in the "what to include" list. [learn more...](#gl)

<!--
```
Scope: Foods > any food's detail/analyze-portion page, and its printout.
_food_detail_context() computes gl_portion from the annotated GI and the
already-portion-scaled display_nutrients carbs_g; food_detail.html shows it
beside the GI with the formula spelled out. food_print() wraps it in the
{"total", "blockers"} shape print.html already renders for meals/days/
recipes, and _food_available_sections() offers "glycemic_load".
```
-->

**PROGRAM: A WHOLE DAY'S GLYCEMIC LOAD IS NOW JUDGED ON THE RIGHT SCALE**

The Daily Summary and day view now band a day's total glycemic load against the daily scale -- under 80 low, 80 to 120 moderate, over 120 high -- instead of the per-meal scale, which made practically every real day read "High" and so told you nothing. Underneath the band NuMa now says plainly that the daily figures are a convention rather than a validated clinical target, and that a day's GL rises with how much you eat, so a larger or more active person naturally runs higher. Per-meal, per-recipe and per-food figures are unchanged and still use the per-serving scale; the day view now names that difference so the two numbers are not read against each other by mistake.

<!--
```
Scope: Meals > day view, Summary > Daily Summary, and the day printout.
Six templates each carried their own inline {% if gl.total < 10 %} band
ladder; all now call one gl_band(total, scope) global from
numa_app/services/glycemic_load.py, with gl_band_caveat(scope) supplying the
day-scale disclosure. print.html takes the scope from a new gl_scope context
key (day print sets "day"; everything else defaults to "serving"). Boundary
handling follows how each scale is published -- serving as <=10 / 11-19 /
>=20, day as under 80 / 80-120 / over 120 -- so a serving GL of exactly 10
is Low and exactly 20 is High, while a day GL of exactly 80 is Moderate.
```
-->

**PROGRAM: BUNDLED REFERENCE TABLES NOW REACH THE DOWNLOADABLE PROGRAM**

Searching the UK ([CoFID](#gloss-cofid)), Australian ([AFCD](#gloss-afcd)), French ([CIQUAL](#gloss-ciqual)) and glycemic index reference tables now works in the packaged, downloadable version of NuMa. Previously all four came back empty there — they only ever worked when NuMa was run from its source code — so if you have been wondering why a food search never found anything in those databases, that was why, and it is fixed.

<!--
```
Scope: nutrimagnus.spec (PyInstaller datas), tests/test_packaging_spec.py.

gi_data.json, cofid_data.json, afcd_data.json and ciqual_data.json were all
absent from the spec's datas allowlist, so they were never copied into the
bundle. Each is loaded by its module as Path(__file__).parent / "<name>.json",
which resolves into sys._MEIPASS in a packaged build -- an absent file means
json loading is skipped and the lookup returns an empty pool, with no error.
Invisible in a dev checkout and to the whole test suite, because there
Path(__file__).parent is the repo root where all four exist. Same failure class
as the DISCLAIMER.md omission caught by manual Windows testing 2026-09-13,
which is what that test file was written for; it only covered _PROJECT_ROOT
literals in backend.py, so it could not see this. Extended with
test_every_bundled_reference_dataset_is_in_the_spec, which scans root modules
for that load pattern and requires each file in datas; verified to fail when an
entry is removed.
```
-->

**MANUAL: STANDARD ERROR EXPLAINED IN THE GLOSSARY**

The "±3" shown beside a glycemic index value from the reference table now has a Glossary entry explaining what it tells you — roughly, how much the people in that study disagreed with each other, and therefore how much weight the average deserves. [learn more...](#gloss-standard-error)

<!--
```
Scope: user-manual.md Glossary (#gloss-standard-error), with incoming links from
the GI lookup result walkthrough (#gi-result-row) and the method-quality section
(#gi-method-quality). Notes that the published tables write it as SEM.
```
-->

**PROGRAM: THE 2021 GLYCEMIC INDEX TABLES CAN NOW BE ADDED YOURSELF**

NuMa can now read the 2021 edition of the international glycemic index tables — over 4,000 foods, against about 2,500 in the edition built in — and every result from it tells you the year that study was actually run, so you can see when a value is old enough that the product has probably been reformulated since. Results also gain the study's standard error, how many people it tested, and a **non-ISO method** flag when the study departed from the international measurement standard. It can't ship built in, because that edition's licence permits you to download and extract it but forbids redistributing it; so NuMa includes the tool and you supply the document, which takes one command. [learn more...](#gi-editions)

<!--
```
Scope: Foods → Food Cache → Annotate (GI lookup); scripts/build_gi_data.py
(rewritten), scripts/build_gi_data_2008.py (renamed from build_gi_data.py,
superseded), gi_data.json (reshaped to the new row schema, still 2008-only),
gi_lookup.py, web/templates/food_annotate.html, data-sources/README.md (new),
.gitignore, nutrimagnus.spec, tests/test_build_gi_data.py (new),
tests/test_gi_lookup.py, tests/test_packaging_spec.py.

Source is Atkinson, Brand-Miller, Foster-Powell, Buyken & Goletzke 2021 (AJCN
114:1625-1632, doi:10.1093/ajcn/nqab233), two online supplemental-table PDFs.
4,017 entries parsed (4,018 printed food numbers; 4012 labels the "Tamales"
category heading, not a food). The 2002 Foster-Powell AJCN table was evaluated
and rejected: 2008 superseded it, so it would contribute duplicate names
carrying older values for the same studies.

LICENSING is why this is a local build rather than shipped data. The 2021
article is under the Elsevier user licence: text and data mining for
non-commercial purposes is expressly permitted, redistribution and adaptation
are expressly forbidden, and copyright is held by the American Society for
Nutrition. The 2008 edition NuMa shipped previously is Creative Commons, which
was the basis for embedding it. So build_gi_data.py now writes
gi_data_local.json, which is gitignored and absent from nutrimagnus.spec's
datas; gi_lookup.active_table_path() prefers it (data dir first, then beside the
module) and falls back to the bundled table. A test asserts gi_data.json
contains only edition-2008 rows, and another asserts the spec never bundles the
local file. The article PDFs live in data-sources/ and are gitignored too.

The trap in the 2021 edition: its two tables are split by ISO 26642:2010 method
compliance, NOT by subject population the way 2008's A1/A2 appendices were.
~1,250 rows in the non-compliant table were measured in normal-tolerance
subjects, so population is read from each row's own "Subjects (type & number)"
cell and ISO compliance is a separate `iso` field. Rows whose subject group the
source leaves unstated form a third pool returned for either requested
population rather than withheld from both.

Parser rewritten from `pdftotext -layout` to `-bbox-layout`: a food's name wraps
onto lines both above and below the line carrying its food number (the number is
vertically centred), so no line-ordering rule recovers names from fixed-width
text. Rows are now bounded by the midpoints between consecutive food numbers,
and each cell is read from its own column window located per page from that
page's header block. This removes the 2008 parser's "short, no digits or commas
=> header" category heuristic, which its own docstring admitted got some
category tags wrong. Source quirks handled: the name-column margin differs
between the two tables (76pt vs 62pt); the standardized-portion note's trailing
bare "GL" inverted the real GL column window; two rows carry misprinted numbers
(2211 as "2111", 3536 as "2536") so printed numbers are not a key; sucrose has a
GI of 132, so any cap at 100/110 drops rows.

Merge is deliberate over-inclusion: a 2008 row is dropped only when its name
matches a 2021 name exactly, by containment, or at >=0.85 similarity, since 2021
reworded most descriptions and no shared identifier can join the editions. Exact
matching alone left 1,402 legacy rows of which ~76% were rewordings; the current
rule leaves 369. Fragmentary 2008 names whose category prefix was lost by that
edition's parser ("Type NS (India)" under "Millet") are repaired from the stored
category, and the bundled gi_data.json now carries those repairs.

Year of test is displayed but NOT stored as its own column -- it goes into the
free-text gi_source citation. gi_source strings already saved are never
rewritten: they record where a number came from, and "2008" in them means the
edition, not a measurement date, which for those rows is unrecoverable.
```
-->

**PROGRAM: SAVING AN ANNOTATION SETTLES THAT FOOD FOR GOOD**

Clicking **Save annotation** now means you have dealt with that food, so it stops interrupting you when you add it to a meal or the pantry — even if you deliberately left one of the two estimates blank. Previously the detour was all-or-nothing across GI and DIAAS: save a GI, tick "don't prompt me for a GI estimate for this food again", and the very same food would still stop you on the next add, on a page that looked exactly like the GI prompt you had just dismissed. The prompt also now says which estimate it actually wants, naming the one already settled above the form and badging the two fields **Asking for this one** and **Settled — not being asked about**. **Skip for now** is unchanged: it saves nothing, so NuMa asks again next time. [learn more...](#annotate)

<!--
```
Scope: Foods > Annotate a Food, and the add-food detour from a meal or the
pantry. Root cause: _annotation_prompt_needed() was just
bool(_missing_annotations(ann)), and the two no_prompt flags are per
estimate while the detour is per food, so a food with GI settled and DIAAS
blank re-prompted forever, showing the same full form each time. db.py --
new food_annotations.reviewed column (CREATE TABLE plus the additive
ALTER migration list); set_food_annotation() takes reviewed=True by
default, being the whole-form writer, and the upsert uses
MAX(excluded.reviewed, food_annotations.reviewed) so a later non-review
write (a GI seed import) can never un-settle a food. web/backend.py --
_annotation_prompt_needed() returns False once reviewed is set, before
consulting _missing_annotations(), which still drives what the page says
is outstanding. food_annotate.html -- names the settled estimate above the
form, badges each field, and the checkbox note now explains that Save
settles the food while Skip for now does not. Tests: the old
test_annotation_prompt_stops_once_both_values_are_saved asserted the
behavior being fixed here (GI alone keeps prompting), so it was rewritten
as test_annotation_prompt_stops_once_the_form_is_saved, which also asserts
the page still reports DIAAS outstanding -- settled is not answered. Added
test_annotation_prompt_survives_skip_for_now and
test_annotation_page_names_which_estimate_it_wants.
```
-->

**PROGRAM: THE NUTRIENT PLOT LEGEND CAN SIT ABOVE THE PLOT**

The legend naming each colored line no longer has to sit at the bottom of the plot. A new **Legend placement** picker on the Nutrient Plot page offers Auto, Always above the plot, and Always below the plot. Auto is the default, and puts the legend just under the title and the dashed/dotted reference-line note whenever it fits on a single row — up to four nutrients — dropping it back below the plot once it would wrap. As with Black & white, the plot on screen updates the moment you change it, and your choice follows the plot into the print view, PNG and SVG downloads, and the Home page copy. [learn more...](#nutrient-plot)

<!--
```
Scope: Daily Summary > Nutrient plot. numa_app/services/plotting.py --
line_plot_image() takes legend_pos ("auto"/"top"/"bottom", new
LEGEND_POSITIONS); "top" anchors the legend at loc="lower center",
bbox_to_anchor=(0.5, 1.0) and reserves room for it by padding the subtitle
(LEGEND_TOP_PAD_BASE + LEGEND_TOP_PAD_PER_ROW per wrapped row) and lowering
the axes top, since unlike the below case there is no free margin there to
grow into. "auto" resolves to top while the legend fits one row
(n <= LEGEND_MAX_NCOL), bottom otherwise. web/backend.py -- new
_plot_legend_pos() sanitizes the param to those three values; the "legend"
querystring param is threaded through the nutrient-plot page, image and
print routes, and _nutrient_plot_qs() appends it ONLY when it is top or
bottom, so a home_nutrient_plot_qs saved before this option existed still
compares equal to the recomputed qs and "Show on Home page" does not
silently uncheck itself. nutrient_plot.html -- the picker, plus the
instant-preview script generalized from a list of checkboxes to a list of
{id, param, value()} controls, where a null value means "omit the param".
Tests added: test_plot_legend_placement_auto_switches_at_one_row (renders
byte-identically to explicit top at 4 series and explicit bottom at 5, and
falls back to auto on an unrecognized value) and
test_nutrient_plot_legend_placement_round_trips.
```
-->

**MANUAL: ONE WORD FOR THE THING THE NUTRIENT PLOT DRAWS**

NuMa drew a "plot" in some places and a "chart" in others, for the same picture. It is a plot everywhere now — in the manual, in the Home page wording, and in the on-screen help text.

<!--
```
Scope: user-manual.md (Part 9 Nutrient Plot section, the Step 5 walkthrough,
the PNG/SVG glossary entries, Part 9 index lines), README-numa-documentation.md
(module list, route table, feature description), web/templates/home.html,
web/templates/nutrient_plot.html, web/backend.py and
numa_app/services/plotting.py comments. tests/test_web.py updated for the
changed Home page string. Deliberately untouched: genuine bar-chart
references in the amino-acid table legend, and "chart" inside older dated
changelog entries, which are history.
```
-->

**MANUAL: COMPUTING ABBREVIATIONS ARE EXPLAINED TOO**

Everyday computing abbreviations are no longer assumed to be common knowledge. CSV, PDF, API, PNG, SVG and ID now have plain-language Glossary entries and are linked where they appear, the same as the nutrition abbreviations. The passage listing Linux desktop names (GNOME, KDE and the rest) now says outright that they are Linux desktop environments, so a Windows reader isn't left wondering.

<!--
```
Scope: user-manual.md (5 new Glossary entries plus links) and
tests/test_manual_abbreviations.py (_ALLOWED). Owner's call: NuMa's readers
are people managing their own nutrition, not developers, so the computing
allowlist was wrong in principle. Only "PC" stays exempt -- ordinary
English for a computer. The Linux desktop names stay exempt on the
condition that the passage naming them contextualizes them, which it now
does explicitly; a comment in _ALLOWED records that condition.

Also fixed the same code-block leak as before: the link pass writes into
indented code blocks, where Markdown does not render. 16 such links were
removed after checking the built HTML. The test already excludes those
blocks; the one-off link script did not.
```
-->

**MANUAL: THE WEEKLY MAINTENANCE ITEMS ARE FINDABLE NOW**

The nine weekly-sweep items in README-numa-documentation.md were a bare numbered list at the bottom of a 1,500-line file, invisible to any outline view and impossible to link to. Each is now its own heading, the Table of Contents lists all nine directly, and the longer-cadence checks that used to sit between the heading and item 1 have moved below the items.

<!--
```
Scope: README-numa-documentation.md (Maintenance section restructured, TOC
expanded with Maintenance subsections) and CLAUDE.md (pointer to where the
sweep lives). Items keep their numbers in the heading text -- "#### 8.
Stale internal links" -- so existing "weekly-sweep item 8" references in
test docstrings and the README itself still read correctly, and now
resolve to GitHub anchors (#8-stale-internal-links). Note GitHub does not
support the {: #anchor} attr-list syntax the manual uses, so headings are
the only way to get anchors in this file. All 23 TOC anchors verified
against GitHub's slug rules.
```
-->

**MANUAL: EVERY ABBREVIATION IS NOW EXPLAINED WHERE YOU MEET IT**

The manual is rarely read front to back — a "learn more..." link drops you straight into the middle of it. So an abbreviation that was spelled out three sections earlier was, for you, simply undefined. Now every abbreviation is either spelled out on first use **within the section you are reading** or linked to its Glossary entry, and eleven new Glossary entries have been added (IOM, WHO, NIH, ODS, EAR, SR, UPC, EAN, and the CoFID, AFCD and CIQUAL source agencies). A new automated check keeps it that way.

<!--
```
Scope: user-manual.md throughout, plus tests/test_manual_abbreviations.py
(new) and README-numa-documentation.md (test table; weekly-sweep item 9
rewritten to note the rule is now enforced automatically).

Prompted by a reader landing on #protein-rda-quality and hitting a bare
"IOM". The full name sat one paragraph above, on the far side of a ####
heading — and a heading is a landing point, so the expansion was invisible
from where the reader actually arrived. That also sharpened the definition
of "expanded": the letters and the words must appear together, IOM
(Institute of Medicine), not merely the full name in nearby prose.

The test splits the manual at every heading and requires each abbreviation
to be expanded inline or linked within its own section. Excluded: the
changelog (a dated record, never rewritten), code fences, <pre> blocks and
indented code blocks. _ALLOWED covers genuinely self-evident tokens (file
formats, country codes, paper sizes, vitamin identifiers); _OTHER_SENSE
handles tokens whose meaning is context-dependent — "AI" is Adequate Intake
in the nutrition chapters but artificial intelligence in "Claude AI".

Two defects were caught during the sweep by checking the built HTML rather
than the markdown: 141 links were first written without the "#" in the
anchor, and 28 landed inside indented code blocks, where Markdown does not
render and the reader would have seen raw "DIAAS" text.
Both fixed; the code-block case is now excluded by the test itself.
```
-->

#### Sep 26 updates

**PROGRAM: THE DIGESTIBLE COMPLETE PROTEIN ROW NOW SHOWS ITS PERCENT OF YOUR TARGET**

In every nutrient comparison table, the indented **(Digestible Complete Protein)** row beneath **Protein** now carries its own percent-of-target and goal figures, measured against the same protein target as the raw protein row above it. Reading the two rows together shows, at a glance, how much of your protein your body can actually use — a day can read 120% of target on raw grams and under 90% on usable protein. [learn more...](#protein-rda-quality)

<!--
```
Scope: _nutrient_sections() in web/backend.py, the DCP row branch. The row
already existed but was built with pct/rda_css/rda_minimum all None, so the
only percentage on the page was the raw-protein one, which overstates
adequacy for a plant-heavy diet. Now fills those from rda["protein_g"] using
the same goal-slot and _rda_css logic as the main loop. No template change
needed: the nutrient table renders row.pct generically, so all 8 templates
using it pick this up at once. day_pct is deliberately left None — a day's
DCP is not the sum of its meals' DCP, since cross-meal complementarity would
be lost, so no number is better than a wrong one. Rationale: the IOM protein
RDA is specified for protein "of mixed quality as typically consumed", i.e.
effectively denominated in reference-quality protein, which is what DCP
measures; comparing DCP to it is correct for everyone and near-identical to
raw protein for omnivores. Also fixed in _protein_adequacy(): the intake
value keyed off truthiness while its label keyed off "is not None", so a DCP
of exactly 0.0 showed the raw protein figure under the DCP label.
```
-->

**MANUAL: WHY THE PROTEIN TARGET ASSUMES HIGH-QUALITY PROTEIN**

Part 4's RDA section now explains something that had never been written down: the 0.8 g/kg protein target comes from research on diets in which most protein was animal-sourced and highly digestible, so it is effectively expressed in high-quality protein — which is why Digestible Complete Protein, not raw protein, is the figure to compare against it. A companion passage in the Diet-Aware Bioavailability section explains why NuMa raises iron and zinc targets on a plant-based diet but deliberately does not raise protein: the iron and zinc penalty is invisible in the food data, while protein's penalty is already measured as the DIAAS score. [learn more...](#protein-rda-quality)

<!--
```
Scope: user-manual.md Part 4 Section P (#rda) gains a new "#### The protein
target assumes high-quality protein" subsection (#protein-rda-quality) plus
a note after the column list on reading the two protein rows and why the
day-total % column stays blank on the DCP row; Section X
(#diet-bioavailability) gains two paragraphs on why protein gets no diet
multiplier, including the mixed-diet vegetarian case that pooled meal DIAAS
already handles. New footnote [^60] cites IOM (2005) DRI for the "mixed
quality as typically consumed" wording. Two new anchors added for links that
had no target: #aa-note-web on Part 3 Section K, #analysis-menu-web on
Part 3 Section H.
```
-->

**PROGRAM: MEAL LISTINGS NOW SAY HOW MUCH, NOT JUST WHAT UNIT**

The list of foods under each meal on the Daily Summary, and on a day's detail page, now shows the amount eaten alongside its unit. Every entry there previously read as a bare dash and unit, such as a plain "g", which told you nothing about the portion.

<!--
```
Scope: web/templates/summary.html and meal_day.html, which share this markup.
The item line read {% if it.unit %}{{ it.unit }}{% elif it.amount %}...g{% endif %},
so the amount branch was dead code: meal_items always carries a unit ("g" set
by /meal/{id}/add for foods, "servings" by /meal/{id}/add-recipe for recipes),
so the first branch always won and printed the unit alone. Now prints
amount|round(1) followed by the unit, matching meal.html's own item rows, with
the bare-unit branch kept as a fallback for an amount-less row.
```
-->

**PROGRAM: LONG PAGES COME BACK THE WAY YOU LEFT THEM**

Leaving a long page and coming straight back to it no longer dumps you at the top of a page with every section collapsed again. The Daily Summary, a meal, a recipe and a food's own page now remember how far down you had scrolled and which sections you had open, and restore both when you return. [learn more...](#search-memory)

<!--
```
Scope: web/templates/base.html (new page-state script beside the nav-memory
one), plus data-remember attributes on summary.html (5), meal.html (3),
recipe_detail.html (1), food_detail.html (1). Panel open/closed state is
stored per pathname so changing a filter or date on the page does not reset
it; scroll is stored per pathname+query, since a different query is a
different list. Panels opt in via data-remember: inline edit forms
(details.popup-edit, recipe_detail's "Edit instructions", summary's profile
"Change" popup) are deliberately excluded, because reopening one would
resurface an edit the user closed to discard. Scroll restore is skipped when
the URL carries a #anchor, and on reload/back-forward navigations where the
browser does its own restoration, to avoid the two fighting. All writes are
try/catch wrapped. Panels inside a loop would need the row id in the key;
none of the four pages needed that yet. Audit of the other 11 pages carrying
<details> deferred - settings.html's 13 panels deliberately left alone.
```
-->

**PROGRAM: THE QUICK-RETURN LINK NO LONGER LANDS ON AN ERROR**

The yellow quick-return link in the navigation bar — the one offering to take you back to where you left off in Foods, Recipes or Analysis — now only ever remembers a page you can actually go back to. Previously, if the last thing you did in a section was an action such as deleting a portion from a food, the link could remember that action rather than a page, and clicking it produced a bare `{"detail":"Method Not Allowed"}` instead of taking you anywhere.

<!--
```
Scope: web/templates/base.html nav-memory script; test in tests/test_web.py.
A few action endpoints (POST /food/cache/<id>/portions/delete and /move among
them) render their result page in place instead of redirecting, so the address
bar holds a POST-only URL. The nav-memory script stored window.location as the
section's remembered page unconditionally, so that URL became both the
quick-return chip's href and the section nav link's override target; following
either issued a GET and got 405. The script now gates the two sessionStorage
writes on a server-rendered isGetPage flag (request.method == 'GET'), so
POST-rendered pages are simply never remembered. Fix is general: it covers
every POST-rendered page, not just the portions routes.
```
-->

#### Sep 25 updates

**MANUAL: WHAT THE GLYCEMIC INDEX SECTION SAYS ABOUT ITS OWN VALUES**

The manual's Glycemic Index section no longer says [GI](#gloss-gi) "is shown when data is available", which read as though NuMa found the values itself — it now says plainly that every [GI](#gloss-gi) you see is one you supplied, that choosing which published value fits a food is your judgment call, and where the saved value then shows up. The advice on what [GI](#gloss-gi) is good for has been widened too: comparing bread against rice for breakfast is a perfectly good use of it, and what really doesn't carry across such a comparison is quantity, which is what glycemic load is for. [learn more...](#gi)

**PROGRAM: A GI VALUE'S SOURCE NOW SHOWS IN EVERY GI COLUMN**

Hovering a [GI](#gloss-gi) figure anywhere it is listed — Food Cache, Pantry, food search, Analyze a Food Portion, a meal's add-food panel, Annotate a Food — now shows which reference-table row that figure came from. A number in a column that narrow can't say how much to trust itself. [learn more...](#gi-what-is-stored)

<!--
```
Scope: every listing with a GI column. Two new provenance helpers in
web/backend.py: module-level _ann_source(ann) for the sqlite3.Row builders
(food cache, its refresh-error path, pantry, annotate list, _search_local_results)
and a nested _ann_gi_source(fdc_id) beside each of the two _ann_gi closures
(food-search and meal add-food builders). Both return "" unless a gi_estimate
exists for the source to describe. Templates: _add_food_row.html annot_cell()
takes an optional source argument appended to its existing tooltip, and
_search_result_row / _analyze_portion_result_row / food_cache / pantry /
food_annotate each add a conditional title on the GI cell. One new test walks
six routes.
```
-->

**PROGRAM: THE OXALATE MATCH PAGE NOW EXPLAINS ITS ENTRIES, INCLUDING WHAT WAS ACTUALLY MEASURED**

Correcting a food's oxalate match is now a page you can read: each candidate entry shows its food group and whether its value was measured in that food or estimated from a similar one, and warns you when an entry has only a per-serving figure and so cannot be totalled in a recipe. A guide beside the list explains the serving units, the five category thresholds, and what saving a match actually does. A food's own page now says measured-or-estimated too. [learn more...](#oxalate-row)

<!--
```
Scope: Foods -> a food -> Anti-nutrients -> "correct if wrong" (oxalate-link),
plus the oxalate line on a food page; user-manual.md Part 9 section M.
oxalate.db already carried food_group and the Harvard table asterisk as
directly_measured, and neither had ever been surfaced anywhere. _oxalate_info()
now returns both (documented in its docstring); food_detail.html prints
measured/estimated on the Reference line; oxalate_link.html gains a two-column
layout with a guide aside, per-row group/evidence/per-serving-only subtext, and
a real button label ("Save this oxalate match"). Manual: four new subsections --
oxalate-row, oxalate-categories (both threshold sets, per-100g and per-serving),
oxalate-measured (235 of 433 entries are direct measurements), and
oxalate-what-is-stored. Tests: two new in tests/test_web.py.
```
-->

**PROGRAM: A GI VALUE NOW REMEMBERS WHERE IT CAME FROM**

Pick a GI value off the reference table and NuMa now records the row behind it — which of the two published tables, the entry's own name, and the study's reference food, time period and number — showing that line under the GI field and on the food's own page. Type a value in by hand instead and there is simply no source line, since the old one would no longer describe your number. [learn more...](#gi-what-is-stored)

<!--
```
Scope: Foods -> Food Cache -> Annotate (GI field), a food's detail page;
db.py, web/backend.py, food_annotate.html, food_detail.html, import_gi_seed.py.
New food_annotations.gi_source TEXT column (created in the CREATE TABLE and in
the ALTER-TABLE migration list, so existing DBs pick it up). set_food_annotation()
takes gi_source and forces it to NULL when gi_estimate is None; upsert_food_annotation()
takes it too, and its docstring states that any caller writing gi_estimate must
write gi_source with it -- COALESCE semantics would otherwise strand an old
citation beside a new number (import_gi_seed.py now passes its own source note).
The annotate page carries it in a hidden field that the lookup fills on pick and
an 'input' listener on the GI box clears on a hand edit; the POST trims it to
300 chars. _food_detail_context() returns gi_estimate/gi_source for the line on
the food page. Tests: three new in tests/test_web.py, one verified by mutation.
```
-->

**PROGRAM: THE GI LOOKUP NOW EXPLAINS ITS OWN RESULTS**

The Annotate page now explains its glycemic index lookup results, in the space beside the form: a worked example of a real row — `Beans, dried, boiled, type NS (Italy)16 · GI 20 · Impaired · ref Bread, 2h 76` — with every part of it spelled out, including what "Impaired" is really telling you (that the evidence is weaker, not that the food is different) and what NuMa saves when you pick a row. The manual's Glycemic Index section carries the full version, now split into readable parts. [learn more...](#gi-result-row)

<!--
```
Scope: Glycemic index -> Food Cache -> Annotate (side panel), user-manual.md
Part 9 section N. web/templates/food_annotate.html wraps the annotate card and
a new <aside> in a flex row, filling the previously blank area to the right;
the aside explains the example row part by part and links the three new manual
anchors. Manual: the single dense "Where GI values come from" paragraph is
split, and four #### subsections added -- gi-populations (Table A1 vs A2, with
the point that A2 conflates impaired-tolerance subjects, small-n studies and
high-variance results, plus what to do about it for either reader),
gi-result-row (field-by-field reading of a row, including the table's own
footnote digits glued onto food names by scripts/build_gi_data.py and the UO
"unpublished observations" study codes), gi-what-is-stored (only gi_glucose is
written to the annotation; population/ref/study are display-only, so Prep
context is the place for provenance; no rescaling from the bread-referenced
column, no GL import), and gi-why-foster-powell (the existing bold-lead
paragraph promoted to a heading). No behaviour change beyond the new panel.
```
-->

#### Release v2026-09-24-0941 summary (dated details below)

- Complement suggestions no longer skip over plant foods like sesame seeds, sunflower seeds and oats — a scoring error had been quietly filtering them out in favour of animal foods.
- Printable pages now use dark ink for every line of text — the greyed-out notes and subtitles came out too faint to read on paper.
- The Edit Recipe page has one Save button instead of two: Introduction now saves with everything else in Recipe details, and the button sits up on the "Recipe details" heading row.
- A printed recipe lists each ingredient the way you typed it — "1/2 t", "3 T", "3/4 c" — instead of converting everything to grams.
- A printable analysis of an incomplete protein now says "(limited by Lysine)" rather than just tacking the amino acid's name onto the DCP figure.
- A recipe's step-by-step is now called "Instructions" everywhere — the recipe page, the printout, and the translation preview used to call the same thing "Procedure".
- Every page with a substantial edit form — Edit Recipe, a meal, Edit Custom Profile, Annotate a Food — now carries the same "Data-entered safety" note, and all of them now actually offer to save your typing if you click away before saving.
- Recipe notes now travel with the recipe: they print on the nutritional analysis (at the very bottom), go into the recipe CSV export, and are included in the AI translation.
- Recipes now have a "Notes and documentation" field on the Edit Recipe page, for sources, substitutions, and anything else you want on record.
- Recipes that show "NC (not computed)" in the recipes list are now re-checked automatically when the program starts, so a recipe whose own page shows a real DCP can't keep showing NC in the list.
- MANUAL: Windows installation is now documented — the install section of Part 1 has separate Windows and Linux instructions, with Windows first.

#### Sep 24 updates

**PROGRAM: COMPLEMENT SUGGESTIONS NO LONGER OVERLOOK PLANT FOODS**

Foods like sesame seeds, sunflower seeds, oats and pumpkin seeds now appear as protein-complement suggestions where they belong. A scoring error had been quietly dropping plant foods out of the main suggestion list and pushing them down into the secondary list, so the top suggestions leaned toward eggs, cheese, fish and chicken more than they should have. For a bowl of lentils, four plant complements that close the amino acid gap in a normal-sized serving were being left out entirely. [learn more...](#gloss-diaas)

<!--
```
Scope: usda_nutrients.py (_score_one_complement, suggest_complements),
tests/test_usda.py. The pooled-DIAAS projection used by the "would this
addition reduce digestible protein" guard weighted the base by its true
ileal digestibility but the candidate by its DIAAS SCORE. DIAAS already
folds in a food own limiting-amino-acid ratio, so using it as a
digestibility factor double-counts that shortfall -- sesame is TID 0.84
but DIAAS 0.44. Low-DIAAS plant foods therefore failed the guard while
animal foods (DIAAS approx TID approx 1) were unaffected, a systematic
one-directional bias. It also contradicted _diaas_improver_score, which
has always used TID, so the same food could be rejected by one tier and
recommended by the other. _score_one_complement now takes an explicit
cand_digestibility (TID via diaas.get_digestibility), passed at all three
call sites including both legs of the gap-cascade pair builder; it falls
back to the old behaviour only when no candidate name is available. For a
100 g cooked-lentil base this restores sesame at 22 g, sunflower at 38 g,
oats at 51 g and pumpkin seeds at 55 g to the gap-closer tier. Three
regression tests added (TestComplementCandidateDigestibilityBasis), and
the pair-recompute test updated to mirror the production call. Two new
reference documents, COMPLEMENT-LOGIC.md and COMPLEMENT-WORKED-EXAMPLE.md,
describe the whole selection path in plain English with a hand-checkable
worked example, and scripts/complement_worksheet.py prints every
intermediate figure for any base food so the result can be verified by
hand.
```
-->

**PROGRAM: PRINTABLE PAGES NOW PRINT IN DARK INK THROUGHOUT**

Every line of text on a printable analysis is now dark enough to read on paper. The greyed-out text — ingredient notes, the subtitle under the title, the small explanatory lines — looked fine on screen but came out faint from a real printer. Nothing moved or changed wording; the lighter text is simply darker, and still set apart by being smaller or italic.

<!--
```
Scope: web/templates/print.html stylesheet. .muted now inherits the body ink
(#111) instead of #666; .meta, .dcp-row and .protein-oneline drop their own
greys, as does the translation disclaimer paragraph inline style. The two
semantic status colours stay, because they carry meaning rather than
emphasis, but were darkened (green #146c2e to #0f5222, amber #a05a00 to
#7a4400) so a mono printer renders them as dark ink rather than mid-grey.
A new test walks every colour declaration on a rendered printable page and
fails any whose channels are not all below 0x66, bar that short allow-list.
```
-->

**PROGRAM: ONE SAVE BUTTON ON THE EDIT RECIPE PAGE**

The Introduction box no longer has a Save button of its own — it saves with everything else in Recipe details, so there is one "Save recipe details" button for the whole section and no question about which one to press. That button now sits up on the "Recipe details" heading row rather than taking up a row by itself, and the data-entry safety net covers the Introduction along with every other field in the form.

<!--
```
Scope: web/templates/recipe_edit.html, base.html; web/backend.py; three tests
updated in tests/test_web.py. The Introduction textarea used to belong to a
second, empty <form id="introduction-form"> via the HTML form="" attribute,
posting to its own /recipe/<id>/introduction route -- which also meant it had
to be excluded from the main form dirty tracking (data-leave-guard-ignore)
and needed its own branch in the cross-form submit guard. It is now an
ordinary field of the Recipe details form; recipe_edit_post() takes
introduction as a form field instead of preserving the stored value, and the
now-callerless /introduction route is deleted. The recipe page's own inline
"Save instructions" editor (/recipe/<id>/instructions) is unaffected and
still carries every other text field forward. The single Save button moved
onto the <summary> row, so it sits outside the form and targets it by id
with form=""; base.html's unsaved-changes tracker gained a fallback lookup
for exactly that shape, or such a form would silently lose its "Unsaved
changes" badge, and a click handler stops the button from collapsing the
<details> it now lives on.
```
-->

**PROGRAM: PRINTED RECIPES SHOW THE AMOUNTS YOU ACTUALLY TYPED**

The Ingredients list on a printable recipe now reads "1/2 t" for the salt and "3 T" for the applesauce, exactly as you entered them, instead of converting every line to grams — nobody measures vanilla extract in grams. The gram weights are unchanged and still drive every calculation behind the scenes; they simply are not what gets printed.

<!--
```
Scope: web/backend.py (_ingredient_amount_display(), attached in
_recipe_detail_context), web/templates/print.html Ingredients table.
recipe_ingredients already stores both: amount in grams and unit as the
typed portion string, and portions._ing_amount_display() already rendered
the latter for the Edit Recipe page. The printout now uses it too, via a
wrapper that also resolves a stored "p1" shorthand back to that food's own
portion description, falling back to grams when the portion is gone.
Ingredient amounts are never scaled by the "servings to analyze" widget
(only nutrients are), so an as-typed label can never disagree with what is
printed beside it. The recipe detail page still shows grams plus a volume
hint -- it is an analysis view, not something you cook from. One new test.
```
-->

**PROGRAM: A PRINTOUT NOW SAYS WHAT THE LIMITING AMINO ACID MEANS**

When a printable nutritional analysis shows incomplete protein, it now reads "DCP: 1.4 g - (limited by Lysine)" instead of "DCP: 1.4 g - Lysine", which looked as though the figure itself were somehow Lysine. The Protein Summary section on the same printout says it the same way.

<!--
```
Scope: web/templates/print.html, the protein-oneline header and the
Protein Summary section, both for the pooled meal/recipe DIAAS variant
which previously rendered diaas.limiting_label bare. The single-food
variants already read "Incomplete -- limiting AA: X" and were left alone.
Falls back to "Incomplete" when there is no limiting label, as before.
One new test.
```
-->

**PROGRAM: ONE NAME FOR A RECIPE STEP-BY-STEP: INSTRUCTIONS**

A recipe's step-by-step is called "Instructions" wherever it appears — the recipe page, the printable analysis, and the translation preview all used to head it "Procedure" while the Edit Recipe page called the same box "Instructions". The buttons on the recipe page now read "Edit instructions" and "Save instructions" to match.

<!--
```
Scope: web/templates/recipe_detail.html, print.html, recipe_translate_import.html,
recipe_edit.html; numa_app/services/print_sections.py. Visible labels only. The
sec-procedure element id and the "procedure" PRINT_SECTION_LABELS key keep their
old names on purpose: the id is linked to from the instructions-save redirect,
and the key is what prefs.json stores for the print "what to include" choices,
so renaming it would silently uncheck that section for anyone who had already
chosen it. Both are commented in place to say so.
```
-->

**PROGRAM: THE SAME DATA-ENTRY SAFETY NET ON EVERY EDIT PAGE**

Edit Custom Profile and Annotate a Food now protect your typing the way the Edit Recipe page already did: click a link elsewhere in NuMa with unsaved edits and NuMa asks whether to save them first, leave without saving, or stay and keep editing. All four edit pages (Edit Recipe, a meal, Edit Custom Profile, Annotate a Food) now carry the same "Data-entered safety" note at the top explaining it.

<!--
```
Scope: web/templates/base.html, _failsafe_note.html (new), recipe_edit.html,
meal.html, food_custom_edit.html, food_annotate.html. The link-interception
guard existed only as near-duplicate per-page scripts on recipe_edit.html and
meal.html. It now lives once in base.html, driven by data-leave-guard="<what
the form edits>" on the form, with data-leave-guard-alert (a Saved banner to
drop on first keystroke) and data-leave-guard-ignore (fields inside the form
that submit elsewhere via form="", i.e. the Introduction block) as options,
and window.numaLeaveGuard.isDirty()/markClean() exposed so recipe_edit.html
keeps its extra behavior: submitting the ingredient-add or Introduction form
saves pending Recipe details first. The note text itself is the shared
_failsafe_note.html macro, so note and behavior can't drift apart; a test
asserts every page showing the note also marks a form with data-leave-guard.
Deliberately not added: create-new forms (New Recipe, Add Portion), where
"save first" would mean creating a record the user has not asked for, and
one-click pickers like the oxalate link chooser.
```
-->

**PROGRAM: RECIPE NOTES PRINT, EXPORT, AND TRANSLATE**

The "Notes and documentation" you write for a recipe now follow it everywhere: they print at the very bottom of the printable nutritional analysis (and can be unchecked there like any other section), they travel in the recipe CSV export and come back on import, and the AI recipe translation now translates them too. On the recipe page itself, the notes now sit at the very bottom, after the analysis.

<!--
```
Scope: numa_app/services/print_sections.py, recipe_csv.py, recipe_translate.py;
web/templates/print.html, recipe_detail.html, recipe_translate_import.html;
web/backend.py. "notes" added last in PRINT_SECTION_LABELS and rendered last in
print.html, offered by _recipe_available_sections() only when non-empty. CSV
gains a recipe_notes column (named to avoid colliding with ingredient_notes);
parse_recipes_csv() reads it with .get(), so a CSV exported before the column
existed still imports. RECIPE_TEXT_KEYS gains "notes", which carries it through
prompt-building, validation fallback-to-English, the import preview, and
_render_translated_recipe(). The recipe detail section moved from just after
Procedure to the end of the page, sidebar entry with it. Five new tests.
```
-->

**PROGRAM: RECIPES NOW HAVE A NOTES AND DOCUMENTATION FIELD**

Every recipe can now carry free-form notes — where it came from, sources you consulted, substitutions you have tried, changes to make next time. The box sits just below Instructions on the Edit Recipe page and saves with the "Save recipe details" button; once you have written something, it appears as its own "Notes and documentation" section on the recipe page. [Learn more...](#recipes)

<!--
```
Scope: Edit Recipe (/recipe/<id>/edit), recipe detail (/recipe/<id>); db.py,
web/backend.py, web/templates/recipe_edit.html, web/templates/recipe_detail.html.
New recipes.notes TEXT column, added to the CREATE TABLE for fresh installs
and to the recipes ALTER TABLE migration list for existing databases (adding
a column preserves every existing row; existing recipes get NULL). Threaded
through recipe_create()/recipe_update() as a keyword arg. recipe_update()
writes every text field on every call, so the Instructions and Introduction
save routes now pass the current notes through -- same bug class as the
earlier total_volume/serving_size wipes -- and /recipe/<id>/copy carries
notes to the copy. The detail-page section and its sidebar entry render only
when notes are non-empty. Not wired into the printable analysis vocabulary
(print_sections.py) or recipe CSV export/translation; those stay as they are
for now. Two new tests in tests/test_web.py.
```
-->

**PROGRAM: RECIPES LIST NO LONGER SHOWS "NC" FOR A RECIPE THAT ACTUALLY HAS A DCP**

Every recipe still showing "NC (not computed)" now gets re-checked each time the program starts, so one whose ingredients have since gained the amino acid data it needs picks up its real digestible complete protein figure on its own. Before this, the recipes list could show NC for a recipe whose own page displayed a properly calculated DCP. [Learn more...](#recipes)

<!--
```
Scope: Recipes list (/recipes) vs recipe detail (/recipe/<id>); web/backend.py
lifespan, db.py, import_foods.py, import_json_folder.py, numa_import_claude.py.
Root cause: the recipes list reads the stored recipes.dcp_g column, while the
detail page recomputes DIAAS live on every view, so any recipe whose stored
value was never written (or was cleared while an ingredient lacked AA data)
displayed NC in the list and a real number on its own page. Several food-write
paths overwrite an existing food's nutrients via cache_food() without calling
recipe_dcp.cascade_food_change(), so a food gaining AA data left every recipe
using it stale: the web Claude AI import route (/food/cache/claude-import) and
the three CLI importers (import_foods.py, import_json_folder.py,
numa_import_claude.py) all now cascade. The CSV import needs no cascade — it
only ever creates new fdc_ids, which no recipe can reference yet. For recipes
already left stale by those paths, the web app's startup now runs one repair
pass over db.recipes_missing_dcp() (recipes with dcp_g IS NULL), recomputing
each; genuinely-uncomputable ones (0 servings, or a significant protein
ingredient with no AA data) simply stay NC, and a failure is logged to
recompute_errors rather than blocking startup. Cost is bounded by the number
of NC recipes, not the recipe count. Found on a real database: 2 of 42
recipes were stale this way; both now compute. Three new tests in
tests/test_food_cascade.py cover the Claude-import cascade and both startup
repair outcomes.
```
-->

**MANUAL: WINDOWS INSTALLATION INSTRUCTIONS**

Part 1's "Download and install the program" section now covers Windows as well as Linux, with Windows first since that's what most people will need. It walks through where to put the program file, getting past the two warnings Windows shows for unsigned programs (and why they appear), launching it, pinning it to the Start menu, quitting properly, and updating later without losing your data. [Learn more...](#install-windows)

<!--
```
Scope: user-manual.md Part 1, section F. Section F split into "#### Windows
{: #install-windows}" and "#### Linux {: #install-linux}", Windows first.
The old item e ("what kind of program this is" / browser-tab and sleep
caveats) was platform-neutral, so it moved out of the Linux list into its own
"#### What kind of program this is {: #install-webapp-note}" subsection
serving both, with its Linux-specific "click NuMa's icon" wording generalized.
The "Windows instructions are coming soon" line at the top of F is gone. The
Linux items are otherwise verbatim from before. Windows content reflects the
actual build: a single unsigned PyInstaller one-file nutrimagnus.exe with
console=True (hence the "leave the black window open" instruction), data in
%LOCALAPPDATA%\numa and %APPDATA%\numa per platform_utils.py, so replacing
the .exe is the whole update procedure. The Windows steps give the releases/latest/download/nutrimagnus.exe
link and nothing else -- no releases-page navigation -- verified 200 /
application/octet-stream, so a click downloads rather than opening a page.
No program change, so no version.py bump.
```
-->

#### Release v2026-09-23-2133 summary (dated details below)

- Mutation testing run against the three modules flagged by this week's churn check: six real test gaps found and closed, including one that would have reported a trace-protein food as having confirmed amino acid data.
- MANUAL: Weekly sweep — the Annotate page's manual section rewritten for the web app, several new features documented, and the sweep moved to Wednesday evening / Thursday morning.
- Deleting a food that one of your recipes, meals, or pantry entries still uses is now refused by the database itself, not just by the page you asked from.
- A recipe that uses another recipe as an ingredient can now be starter data; one such recipe was previously dropped from every release without saying so on the Home page.

#### Sep 23 updates

**PROGRAM: NO VISIBLE CHANGE — MUTATION TESTING CLOSED SIX REAL GAPS IN THIS WEEK'S CODE**

Nothing you can see changed. NuMa's [test suite](#extensive-code-testing) was checked by deliberately planting small errors in the three modules that changed most this week and seeing whether the tests noticed; six places where they would not have are now covered. The most consequential: a food with a trace of protein and no amino acid data could have been reported as having confirmed data, the same wrong-checkmark problem fixed twice before in other places.

<!--
```
Scope: tests/test_recipe_nutrients.py, tests/test_complements.py,
tests/test_usda.py, setup.cfg, README-numa-documentation.md (rotation log).
Run against the three modules the 2026-09-23 weekly churn check flagged, per
the documented procedure's "flag it and ask" step -- the deferral offered
first was mine, not the procedure's, and was withdrawn when asked.
recipe_nutrients.py 240->244 killed of 293. Four real gaps: servings <= 0 vs
<= 1 in recipe_serving_grams() (every test used 2+ servings, so the mutant
returned None for every single-serving recipe); its `or "g"` unit default
(a NULL total_weight_unit silently lost the weight); and, twice over, a
`continue` that skips an unusable ingredient becoming `break`, which drops
every ingredient after it -- once in expand_recipe_ingredients() for an
uncached food, once in atomic_recipe_ingredients() for a deleted sub-recipe.
complements.py 1113->1122 killed of 1548; the churn's new _amount_note() went
12 survivors to 3. Its cache lookup was never exercised because every existing
assertion recomputed portions.amount_note() in the test and compared, so
gutting the lookup silently drops the amount hint from every suggestion.
usda_nutrients.py 1265 killed of 1520. aa_indicator()/has_confirmed_aa_data()/
has_macro_data() produced no survivors. One real gap: has_amino_acid_data()'s
"no protein, so AA data is irrelevant" shortcut was tested at exactly 0 and
with the key absent but never just above it.
Two infrastructure fixes found by doing this: mutmut's also_copy in setup.cfg
had gone stale when manual_update.py was added (conftest could not import it
inside the mutant tree), and naming package files individually only works when
a source_path already creates numa_app/ inside mutants/ -- which it does not
when the module under test is at the repo root. also_copy now copies the
package.
Survivors left are equivalent mutants, chiefly sqlite3.Row's case-insensitive
key lookup making ing["FDC_ID"] identical to ing["fdc_id"], plus the scattered
suggest_complements()/build_complement_display() population characterized on
2026-09-10. No "no tests" (zero-coverage) regions in any of the three.
```
-->

**MANUAL: WEEKLY SWEEP — ANNOTATE SECTION REWRITTEN FOR THE WEB, FOUR FEATURES DOCUMENTED, SWEEP DAY MOVED**

This week's maintenance pass. The manual's **Annotate a Food** section still described the old typed-command picker ("type the number to select that food") rather than the web page the app's own Learn more link sends you to — rewritten, and it now covers all four ways to reach Annotate, the GI lookup's click-a-result behavior, and why the two "don't prompt me again" checkboxes are rarely needed. Newly documented: the gram weight shown beside a serving amount, the amino acid status now shown for recipes in search results, and the clickable GI/DIAAS figures on an add-food list. The front-page feature list was claiming NuMa searched two food databases when it searches six. The weekly sweep itself moves from Saturday to Wednesday evening / Thursday morning.

<!--
```
Scope (weekly sweep, 2026-09-23 — first under the new day):
Longer-cadence checks: none due (monthly 09-01, quarterly fixtures 09-11,
glossary 09-16, annual datasets 09-20, full manual audit 09-13).
1 CLAUDE.md drift: version.py was missing from Package Layout despite
  CLAUDE.md carrying a rule about bumping it. Added.
2 NuMa capitalization: 3 prose hits fixed. The same grep caught real drift --
  README described the bundled CIQUAL as the 2020 edition when the 09-20
  annual check had already upgraded it to 2025 (3,484 entries, verified).
3 Vendored Bootstrap: 5.3.8 vendored, 5.3.8 upstream. No action.
4 Changelog pruning: removed the Sep 7 and Sep 6 sections, 168 lines, leaving
  the Sep 9-23 window.
5 Manual consolidation: the CLI-era #annotate section (the last such section
  left -- greps for "Type ?", "^Commands:", "Command line:", a{id} now come
  back clean outside the changelog); plus the three undocumented features
  above.
6 README.md accuracy: food-search bullet named only USDA + OFF against an
  intro paragraph two lines above it that says six sources; GI reference-table
  lookup absent from the feature list entirely.
7 Test coverage: everything from this week had tests except two JS-only
  behaviors. Closed the meal-item scroll restore with an e2e test aimed at the
  action-URL regex that gates the save (finding the right form also confirmed
  the Rename popup correctly does not save an offset). NOT closed: the
  spurious "Leave site?" suppression -- Playwright auto-dismisses beforeunload
  dialogs, so a test asserting "no dialog" would pass for the wrong reason.
8 Links: internal links now covered by tests/test_link_integrity.py (passing).
  External: 23 non-200s across 75 URLs, all bot-gating hosts already known
  from previous sweeps (NIH ODS, examine.com, doi.org, researchgate,
  claude.ai, fdc.nal.usda.gov). No real rot.
9 Glossary: "sub-recipe" was used 20 times in the manual body with no entry --
  added, and linked from the two passages written this week.
Mutation-testing churn check: usda_nutrients.py (+62), complements.py (+61,
  carried over from the 09-20 flag) and recipe_nutrients.py (+44) all flagged
  in the rotation log; triage stays a dedicated session.
Cadence: sweep moved Saturday -> Wednesday evening / Thursday morning, with
  .github/workflows/e2e-tests.yml moved to cron "0 6 * * 4" so its result is
  fresh for the sweep.
Also this session, outside the numbered items: README's Test Suite section
  claimed 733 tests against an actual 1,117 and was missing 13 test files --
  corrected, and two new tests in test_packaging_spec.py now fail if that
  table misses a file or lists a deleted one, so it cannot drift silently
  between monthly accuracy checks again.
```
-->

**PROGRAM: A FOOD IN USE CANNOT BE DELETED, NOW GUARANTEED BY THE DATABASE**

NuMa has refused for some time to delete a food that one of your recipes, meals, or pantry entries still uses, telling you which one is holding it. That refusal now also lives in the database itself, so no future part of the program — or any script, or anything editing the file directly — can get around it and leave a recipe pointing at a food that no longer exists. If you use the Settings toggle to clear starter data, any starter food you have since used in a meal or recipe of your own is now kept instead, and the page tells you how many and why.

<!--
```
Scope: db.py (trg_foods_no_delete_when_referenced in init_db),
numa_app/services/demo_data.py (clear_demo_data), web/backend.py
(settings_demo_data_clear), web/templates/settings.html, tests/test_db.py,
test_demo_data.py, test_web.py, README-numa-documentation.md.
BEFORE DELETE trigger on foods, aborting when a pantry/recipe_ingredients/
meal_items row still references the fdc_id -- the same three conditions
food_references() reports. A trigger, not an FK on recipe_ingredients.fdc_id:
sub-recipe rows store fdc_id 0 (their target is ref_recipe_id, so no food row
can ever match), and adding an FK to an existing table needs a table rebuild
plus repair of every pre-existing orphan, whereas a trigger guards new
deletions and leaves existing damage to check_db_integrity()/
repair_db_integrity(). Application-level checks in the delete routes stay --
they can name the holder, which the trigger cannot.
clear_demo_data() had to change with it: it deleted every starter food
outright, silently orphaning a meal logged with one; under the trigger that
would have aborted the whole clear instead. It now skips still-referenced
foods and returns foods_kept, which the Settings confirmation reports.
Three integrity tests that manufactured orphans BY deleting a referenced food
now write the orphan row directly, since the scenario they simulate is exactly
what is no longer possible.
```
-->

**PROGRAM: A RECIPE BUILT ON ANOTHER RECIPE CAN NOW BE STARTER DATA**

Starter data — the foods, pantry items and recipes a brand-new install arrives with, and that [Settings](#starter-data) can restore individually — now supports a recipe that uses another recipe as one of its ingredients. Marking such a recipe with a leading `*` previously did nothing at all: it was silently left out of every release, along with any food only it used. The sub-recipe travels with it, so restoring the parent on its own brings the sub-recipe too rather than leaving a broken ingredient.

<!--
```
Scope: scripts/export_starter_data.py, numa_app/services/demo_data.py,
scripts/refresh_starter_data.py, numa_app/services/starter_data.json,
tests/test_demo_data.py, test_export_starter_data.py,
test_refresh_starter_data.py, README-numa-documentation.md.
Export is now recursive (_export_recipe): a sub-recipe is exported before its
user, so the recipes list is in dependency order and load_demo_data() always
has the sub-recipe's new id when it links the parent. An unstarred sub-recipe
is auto-included with a NOTE, same as an unstarred ingredient food. Ingredient
entries gained a 4th element, kind ("food"/"recipe"); demo_data._ingredient_parts()
reads a 3-element entry as a food so a pre-nesting starter_data.json still loads.
clear_demo_data() now deletes recipes in REVERSE creation order -- deleting a
sub-recipe first trips the recipe_ingredients.ref_recipe_id foreign key.
restore_selected() widens a selection to the sub-recipe closure and links to an
already-present sub-recipe by name instead of duplicating it.
Also fixed a latent crash found while doing this: db.recipe_delete() leaves the
ingredient row with ref_recipe_id NULL, ref_recipe_deleted 1 and fdc_id 0, which
the export's food branch would have followed into get_cached_food(0) -- that
recipe is now skipped with a warning. refresh_starter_data.py refreshes existing
sub-recipe entries by source id but still defers adding a NEW one to the export,
which is what orders the list. Live effect: starter data goes from 46 foods /
7 recipes to 47 / 8.
```
-->

#### Release v2026-09-23-1718 summary (dated details below)

- A food's own detail and Edit Custom Profile pages now link straight to Annotate, for adding or changing its GI and DIAAS estimates.
- An amount given in servings now shows what it weighs in grams alongside it, on a meal's item list, both recipe ingredient lists, and a printed recipe.
- In the Annotate page's GI lookup you can now click anywhere on a result to use its GI value; the list then closes, leaving the value and the Save button in view.
- Recipes in a search list now show whether they have amino acid data, instead of leaving that column blank.
- The Home page's "see what changed" link now opens the manual at the most recent release's summary, instead of the top of the updates log.
- You are now asked for a missing DIAAS estimate as well as a missing GI, and the GI/DIAAS figures on the add-food list are clickable for editing a value you have already entered.
- The Edit Custom Profile page now has the same Contents sidebar the Food Detail and Daily Summary pages use, for moving straight to any of its nine sections.
- Recipe ingredient amounts shown in cups or tablespoons are now worked out from the food's own portion data, instead of a generic density guess that could be well off.
- Every nutrient column on the Daily Summary's Recent Days table now shows its own "% Goal" figure, and the Date column stays put as you scroll the table sideways.
- The Nutrient Plot page now opens showing the plot you've pinned to the Home page, instead of starting blank and hiding its own "Show on Home page" toggle.
- Adding a recipe as "Individual ingredients" now fully breaks down nested sub-recipes too, instead of adding them as whole-recipe items.
- A recipe result's "Servings" field no longer goes blank when background search results finish loading and merge into the list.
- "Add as individual ingredients" no longer quietly reverts to "Whole recipe" when external search results arrive after you've picked it.
- Manage Portions can now edit a custom portion's description and gram weight in place, keeping its `pN` shortcut unchanged.
- Clicking a food's name from a recipe's ingredient list or a meal's item list now says which recipe or meal that amount came from.
- Leaving unsaved Recipe Details, or a meal's Rename/date edits, now offers you the choice to save first, leave without saving, or stay and keep editing.
- A meal's item list now keeps your scroll position when you add, edit, or remove an item.
- Fixed a spurious "Leave site?" browser warning when adding an ingredient to a meal or recipe.

#### Sep 23 updates

**PROGRAM: REACH ANNOTATE FROM THE FOOD ITSELF**

A food's detail page and its [Edit Custom Profile](#drafted-foods) page now each carry an **Add or edit GI / DIAAS estimates** button that goes straight to that food's [Annotate](#annotate) page and brings you back when you are done. Until now the only ways in were the post-add prompt, the GI/DIAAS cells on an add-food list, and Foods → Annotate followed by filtering for the food by name — so for a food you were already looking at, there was no obvious way at all.

<!--
```
Scope: web/templates/food_detail.html, food_custom_edit.html,
food_annotate.html, tests/test_web.py.
Annotate has always accepted any cached fdc_id, user-drafted ones included
(list_cached_foods/search_cached_foods don't filter on user_drafted) -- the
gap was purely navigational. The ?next= round-trip is the same one the
post-add prompt uses. That prompt's "No X estimate on file yet" paragraph
and its Skip-forever button were gated on `next` alone, so a deliberate
visit to a food that already had both values rendered "No  estimate on file
yet" with an empty join; both are now gated on `next and missing`, and the
return button reads "Back without saving" rather than "Skip for now" when
there is nothing to skip.
```
-->

**PROGRAM: SERVINGS NOW SHOW WHAT THEY WEIGH**

Wherever an amount is given in servings — a recipe added to a meal, or a recipe used as an ingredient inside another recipe — the gram weight of that amount now appears next to it, as in "2 servings (500 g)", on screen and on a printed recipe alike. A serving count on its own says nothing about how much food it is; the weight makes two recipes comparable at a glance. Nothing is shown if the weight can't be worked out, which happens when a recipe has neither a total weight of its own nor a full set of weighable ingredients.

<!--
```
Scope: numa_app/services/recipe_nutrients.py (new recipe_serving_grams()),
web/backend.py (_meal_items_with_nutrients recipe branch, and ref_grams in
_attach_ref_serving_sizes), web/templates/meal.html, recipe_detail.html,
recipe_edit.html, print.html, tests/test_web.py.
recipe_serving_grams() prefers the recipe's own stated total_weight, which
is stored AS TYPED with its unit (only total_volume is normalized, to ml on
save), so it converts via portions._UNIT_TO_GRAMS rather than assuming
grams -- two existing callers do assume grams and are wrong for an oz/lb/kg
recipe. Falls back to db.recipe_compute_weight() but only when that reports
complete: an incomplete sum is a lower bound, and a serving weight quietly
short by an unknown amount is worse than none. The print/export page picks
ref_grams up from the same shared helper, via _recipe_detail_context.
```
-->

**PROGRAM: CLICK ANY GI LOOKUP RESULT TO USE ITS VALUE**

On the [Annotate](#annotate) page, clicking anywhere on a [GI](#gi) lookup result — the food name included — now puts that value in the GI estimate box. The list of matches then disappears and the lookup panel closes, so what you are left looking at is the GI box, which flashes as it fills, and the **Save annotation** button, now highlighted and ready to press. Before, only the small button at the end of the row did anything, and it gave no visible sign it had worked.

<!--
```
Scope: web/templates/food_annotate.html (gi-pick-row + usePick()),
web/static/style.css (.gi-pick-row/.btn-save-pending/.field-just-set),
tests/e2e/test_search_e2e.py.
The click handler was bound to .gi-pick (the button) alone, so a click on
any other cell hit nothing, and the handler's only effect was setting a
field above a collapsed <details> panel -- indistinguishable from a dead
click. Handler now binds to the row; the button stays as the explicit
affordance and rides the same row listener. A confirmation line under the
results was tried first and dropped: it lands below a result list that can
be long enough to scroll it out of sight. Instead the pick empties the
results and sets details.open = false, and the still-unsaved value is
carried by highlighting and focusing #save-annotation-btn.
```
-->

**PROGRAM: RECIPES NOW SHOW THEIR AMINO ACID STATUS IN SEARCH LISTS**

When you search for something to add to a meal or a recipe, or search on the Foods page, the AA column now shows a green checkmark for any recipe whose ingredients carry [amino acid](#gloss-aa) data — the same way it already did for individual foods. Before, that column was simply blank for every recipe, so a recipe with full AA data looked no different from one with none.

<!--
```
Scope: numa_app/services/recipe_nutrients.py (new recipe_aa_indicator()),
web/backend.py (_recipe_aa_status() + the three recipe-row builders:
_search_local_results, _meal_add_food_local_results, recipe_edit_get),
web/templates/recipe_edit.html, tests/test_web.py.
Two of the three recipe-row builders emitted no "aa" key at all, so the
template's aa branches all fell through; the third (Food Search) set
"✓" if dcp_g is not None, a stale-DCP proxy that says nothing about AA
data either way. A recipe has no nutrients dict of its own, so the status
now comes from aa_indicator() over recipe_total_nutrients() -- an empty or
fully uncached recipe totals to {} and reports "⚠", matching an uncached
food. recipe_edit.html also hard-coded an em-dash for recipe rows ahead of
its own aa branches; removed.
```
-->

**PROGRAM: "SEE WHAT CHANGED" NOW OPENS AT THE LAST RELEASE'S SUMMARY**

The "see what changed" link beside the version note on the Home page now takes you straight to the newest release's summary in [Recent program updates](#updates-log) — the list of what the version you are running actually shipped with. Before, it landed at the top of that log, which leads with a running summary of changes that have not been released yet.

<!--
```
Scope: web/backend.py (_latest_release_anchor() beside _manual_link, plus
changelog_anchor in the home context), web/templates/home.html (both
"see what changed" links), tests/test_web.py, tests/test_link_integrity.py.
The anchor can't be a constant: create_release.py renames the running
"Next release summary to this point" heading to "Release <tag> summary" at
release time, so the target id changes with every release. _latest_release_anchor()
regexes the first <h4 id="release-...-summary"> out of the ACTIVE manual html
(baked-in or downloaded), cached on the file's mtime, falling back to
#a-recent-program-updates-log when the log has no release summary in it yet.
test_link_integrity now skips fragments containing "{{" -- a Jinja-computed
anchor can't be resolved statically.
```
-->

**PROGRAM: EDIT A GI OR DIAAS VALUE STRAIGHT FROM THE ADD-FOOD LIST, AND GET ASKED ABOUT DIAAS TOO**

When you add a food and it has no [GI](#gi) estimate yet, NuMa offers you the chance to enter one — and now does the same for a missing [DIAAS](#gloss-diaas) estimate, which it previously never asked about at all. Once a value is saved you are not asked for it again. To change one later, the GI and DIAAS figures in the add-food list are now links: click one to go straight to that food's Annotate page with the value filled in ready to edit, then come back to your search exactly where you left it. A dash in those columns means nothing is recorded yet, and clicking it is how you add one.

<!--
```
Scope: web/backend.py (_missing_annotations() + _annotation_prompt_needed()
replacing _gi_prompt_needed(); both pantry-add and meal-add call sites),
web/templates/_add_food_row.html (annot_cell macro), food_annotate.html,
web/static/style.css (.annot-cell/.annot-cell-empty).
diaas_no_prompt and its Annotate checkbox already existed but nothing ever
read them -- there was no DIAAS prompt to suppress, so that half of the
feature was dead. skip-forever now sets both no_prompt flags, since
suppressing only GI would leave the DIAAS detour firing on every add.
The Annotate page's prompt text now names only what is actually missing,
via the new missing=[] context.
annot_cell uses default('', true) because the cell values arrive in three
shapes: a preformatted string from _ann_gi/_ann_diaas ("" when unset), None
from the barcode/cache row builders, and undefined on recipe rows (no
annotation). An earlier "is none" test silently matched none of them.
```
-->

**PROGRAM: A CONTENTS SIDEBAR ON EDIT CUSTOM PROFILE**

The [Edit Custom Profile](#drafted-foods) page now has the same Contents sidebar the Food Detail and Daily Summary pages use, listing all nine of its sections — the two copy-from-another-food tools, Identity, and each nutrient group. It stays put as you scroll, highlights whichever section you're currently in, and takes you straight there, so you no longer have to scroll a very long page to find one group of fields. Picking a section you've collapsed opens it for you. The page also no longer jumps down to the amino-acid search box when it loads, so the heading, the "Profile saved" confirmation, and the sidebar are all visible when you arrive.

<!--
```
Scope: web/templates/food_custom_edit.html. Adopts the existing analysis-page
sidebar pattern rather than a one-off: layout_class=analysis-page,
main_class=analysis-content, and a sidebar_nav block of
li.sb-item > a.sb-toggle, same as summary.html/food_detail.html. Section ids
renamed to the sec-* convention so the standard scroll-spy ([id^="sec-"] ->
.sb-active) works unchanged; nothing linked to the old #copy-nutrients /
#estimate-aa ids. Nutrient-group anchors are derived in-template from
group.name (lower|replace(' ','-')) rather than added to field_groups, which
is built identically in both the GET and POST handlers. One addition over the
shared pattern: every section here is a <details>, so a jump opens a collapsed
target first, otherwise it lands on a bare summary line.
Also dropped the autofocus on the aa_source_q input: it loaded the page already
scrolled 482px down, hiding the h2, any alert, and the sidebar.
```
-->

#### Sep 22 updates

**PROGRAM: RECIPE INGREDIENT AMOUNTS NO LONGER GUESS CUP/TABLESPOON EQUIVALENTS**

Recipe pages showing an ingredient's amount in cups or tablespoons now calculate that figure only from the food's own known portion data (its p1, p2, etc.), scaling it exactly to whatever amount is in the recipe. Previously this used a generic, name-based density guess that could be quite wrong, and could even openly contradict a portion you'd just edited for that food. When a food has no portion data at all, the recipe page now says so plainly and links straight to where you can add it, instead of guessing — the same policy the [amount-entry side](#ts-no-volume-portion) of NuMa already followed. The same fix applies to protein complement suggestions' "Add to meal/recipe/day" amount hints.

<!--
```
Scope: numa_app/services/portions.py (portion_scaled_display(), portion_amount_note()
replacing volume_hint()/old amount_note()'s _usda.get_density_g_per_ml() guess),
numa_app/services/complements.py (_amount_note() now threads fdc_id through all 7
call sites instead of food_name), web/backend.py (_ingredient_volume_display()).
No template changes needed -- portion_amount_note() returns a markupsafe.Markup
instance for the "no portion data" case so the <a href="/food/cache/{fdc_id}/portions">
edit it here</a> link renders through existing {{ ing.volume_display }}/
{{ f.amount_note }} interpolations without any autoescaping.
```
-->

**PROGRAM: EVERY NUTRIENT ON DAILY SUMMARY'S RECENT DAYS TABLE NOW SHOWS % GOAL**

Every nutrient column on the [Daily Summary](#goals) page's Recent Days table — Protein and any extra nutrient you've picked in Settings — now gets its own "% Goal" figure alongside it: the percentage on top, that date's own target amount underneath in parens, both scored against whichever profile is pinned to that date. Previously only Day DCP had this. The Date column now stays put at the left edge as you scroll the table sideways to see it all.

<!--
```
Scope: web/backend.py's _build_day_rows() (feeds /summary and /summary/{date}),
web/templates/summary.html, web/static/style.css, numa_app/services/meal_list_columns.py.
Per day row, computes profile.compute_rda() once (reused for the existing
Protein-goal figure too, replacing a separate day_profile.protein_target_for_date()
call) and a new day_nutrient_raw_totals() helper (raw floats, alongside the
existing formatted day_nutrient_values()) to get pct = total/rda_val*100 per
key, stored in pct_goal_map. Template: a new pct_goal_cell() macro renders
value/goal as a two-line cell (percent, then "(goal)" below) so adding this
per nutrient column doesn't double the table's width -- also applied to Day
DCP's own %/Goal, replacing its previous two separate columns. Date column
gets position:sticky via a new .sticky-col class, with hover/active-row
background repeated on it (a sticky cell paints over its own background, so
without this it'd go transparent showing scrolled content underneath).
```
-->

#### Sep 21 updates

**PROGRAM: FIXED THE NUTRIENT PLOT PAGE HIDING ITS OWN "SHOW ON HOME PAGE" OPTION**

Opening the [Nutrient Plot](#nutrient-plot) page fresh (not from a saved link) now shows your currently-pinned Home page plot right away, instead of always starting blank. Landing on a blank page like that used to hide the "Show on Home page" toggle entirely (it only appears once something's actually plotted) while still claiming a "different" plot was on the Home page — true of every fresh visit, not just an actual mismatch. Clicking "Remove it from Home page" from that blank state also used to fail outright with an on-screen error; that's fixed too.

<!--
```
Scope: web/backend.py's nutrient_plot_page (GET /summary/nutrient-plot) and
nutrient_plot_home_pref (POST .../home-pref), web/templates/nutrient_plot.html.
Two bugs: (1) a bare landing (no query params) always rendered with
chosen=[]/has_plot=False rather than defaulting to the saved
home_nutrient_plot_qs, so the "Show on Home page" toggle (gated on has_plot)
never appeared even with a Home plot active, and home_plot_enabled_elsewhere
was unconditionally true. Added a hidden submitted=1 marker to the form so a
genuine fresh landing (no marker) redirects to the saved qs, while a real
"submitted with nothing checked" request (marker present) is left alone.
(2) nutrient_plot_home_pref declared qs: str = Form(...) (required); FastAPI
treats a submitted empty-string form value as a MISSING field for a required
Form param (reproduced directly against a minimal FastAPI app), and the
hidden qs field is exactly empty on that blank-landing page -- changed to
Form(default="").
```
-->

**PROGRAM: FIXED A NESTED SUB-RECIPE ADDING ITSELF AS A WHOLE PACKAGE IN "INDIVIDUAL INGREDIENTS" MODE**

Adding a recipe to a meal (or another recipe) as "Individual ingredients" now fully flattens it, even when one of its own ingredients is itself another recipe. Previously that inner recipe was added as its own whole-recipe meal item alongside the real ingredients, instead of being broken down into its own leaf foods too.

<!--
```
Scope: web/backend.py's meal_add_recipe_item (POST /meal/{meal_id}/add-recipe,
mode="ingredients"). It only expanded one level: a direct ingredient with
ref_recipe_id was added via db.meal_add_recipe() (a whole recipe-type meal
item) instead of being recursed into. Now uses the existing shared recursive
flattener, numa_app.services.recipe_nutrients.expand_recipe_ingredients(),
already used for recipe nutrient totaling elsewhere.
```
-->

**PROGRAM: FIXED SERVINGS FIELDS GOING BLANK AFTER A BACKGROUND SEARCH MERGE**

On a meal's Add Food or Recipe search, a recipe result's "Servings" field could reset from its default (or whatever you'd typed) to blank once results from USDA/Open Food Facts/etc. finished loading in the background and merged into the list. Fixed as part of the same-day fix below for "Individual ingredients" losing your pick after that merge.

<!--
```
Scope: web/templates/meal.html's search-api-results merge handler, the
restoreRows() fix added earlier the same day. It called recipeAmtSwitch() to
re-show the right servings/weight/volume panel after the merge replaced the
table, but that function also clears and focuses the newly-active panel's
input as part of its normal "user just switched panels" behavior -- which
ran on every row on every merge, wiping out the very value restoreRows() had
just written back in. Replaced with panel-visibility-only logic that doesn't
touch the input's value.
```
-->

**PROGRAM: FIXED "ADD AS INDIVIDUAL INGREDIENTS" SILENTLY ADDING THE WHOLE RECIPE INSTEAD**

Adding a recipe to a meal (or another recipe) via a search that also includes an external source (USDA, Open Food Facts, CNF, CoFID, AFCD, or CIQUAL) could quietly reset "Individual ingredients" back to the default "Whole recipe" pick if those external results happened to arrive after you'd already chosen it — with no visible sign it happened. Picking "Individual ingredients" is now reliable regardless of when the background search finishes.

<!--
```
Scope: web/templates/meal.html's search-api-results merge handler. It
replaces the whole results tbody with the server's merged+re-sorted HTML
once external sources respond, which was silently discarding any
in-progress row state (the mode radio, amount_mode radio, typed
portion/servings amounts) set before that replace landed. Now snapshots
each row's current field values first (keyed by add/add-recipe + recipe or
food id) and restores them onto the matching row after the replace,
re-running recipeAmtSwitch so a restored amount_mode also shows the right
input panel.
```
-->

**PROGRAM: EDIT A PORTION IN PLACE**

[Manage Portions](#portion-formats) now lets you edit a custom portion's description and gram weight directly in the list — no more deleting it and re-adding it from scratch to fix a typo or a wrong weight. Editing keeps the portion in its position, so its `pN` shortcut doesn't change.

<!--
```
Scope: web/templates/food_cache_portions.html, web/backend.py (new
POST /food/cache/{fdc_id}/portions/edit route). Each row's description/grams
became inline form controls tied to a per-row edit form via the HTML `form=`
attribute; validation mirrors the existing add-portion checks (non-blank
description, positive gram weight).
```
-->

**PROGRAM: RECIPE/MEAL ITEM LINKS SAY WHERE THE AMOUNT CAME FROM**

Clicking a food's name from a recipe's ingredient list or a meal's item list now labels that food-detail page "Recipe ingredient amount: …" or "Meal item amount: …", so it's clear you're looking at one measured amount from that recipe or meal — not a generic 100 g food lookup.

<!--
```
Scope: web/backend.py (food_detail route gained a from_context query param,
validated to "recipe"/"meal"/""), web/templates/food_detail.html (title/h2
prefix), web/templates/recipe_detail.html and meal.html (ingredient/item
links now pass &from_context=recipe / &from_context=meal).
```
-->

**PROGRAM: LEAVING RECIPE/MEAL DETAILS UNSAVED NOW WARNS — AND LETS YOU CHOOSE**

Editing a recipe's Recipe Details, or a meal's Rename/change date fields, and then clicking a link elsewhere in NuMa before saving now prompts you: save those changes first, leave without saving them, or stay and keep editing. Previously an in-app click away could silently lose the edit; closing or refreshing the browser tab itself still shows only your browser's own generic warning, since NuMa can't intervene at that point.

<!--
```
Scope: web/templates/recipe_edit.html, web/templates/meal.html. A dirty flag
on the Recipe Details / rename form is checked on in-app <a> clicks
(intercepted, chained confirm() for save-then-go vs. discard-then-go vs.
stay) and on window.beforeunload (browser's own warning only, no custom
save possible there).
```
-->

**PROGRAM: MEAL ITEM LIST KEEPS YOUR SCROLL POSITION**

Adding, editing, or removing an item on a meal's page no longer jumps you back to the top of the page — it stays scrolled to where you were working, matching how the recipe editor's ingredient list already behaved.

<!--
```
Scope: web/templates/meal.html — added the same sessionStorage
scroll-save/restore pattern recipe_edit.html already had for its ingredient
list, for the add/add-recipe/update/remove/confirm-aa routes.
```
-->

**PROGRAM: FIXED A SPURIOUS "LEAVE SITE?" WARNING WHEN ADDING AN INGREDIENT**

Adding a food or recipe to a meal or recipe could sometimes trigger a "Leave site? Changes you made may not be saved" browser prompt even though nothing was actually lost — most noticeably when adding an item redirected to the Annotate page for missing GI/DIAAS data instead of back to the same page. This no longer happens.

<!--
```
Scope: web/templates/base.html's generic per-form "unsaved changes" tracker.
Submitting any tracked form now clears every tracked form's dirty flag, not
just its own -- a stray dirty flag left on some other untouched-but-modified
search-result row (typed and abandoned, or filled in by browser autofill)
was outliving the submit and firing the beforeunload warning on the
resulting navigation, wherever it redirected to.
```
-->

#### Release v2026-09-21-0647 summary

- MANUAL: The User Manual can now be updated on its own — a separate home-page notice offers a newer manual without needing a program update.

#### Release v2026-09-21-0526 summary (dated details below)

- Nutrient tables now show separate Minimum, Target, and Maximum columns instead of one ambiguous "Daily Target" column.
- The Nutrient Plot has a "Clear all nutrient checkmarks" button, and clearer wording on what "completeness" affects.
- Nutrient tables show the actual RDA/limit number next to the percentage, not just the percentage.
- The Nutrient Plot now draws maximum-limit lines in addition to goal lines.
- New Appendix H: a full nutrient key.
- Fiber, sugar, and the three fat types now show indented under Carbohydrates and Fat in nutrient tables.
- Complement suggestions' graduated amounts can now be pinned to your own chosen serving size.
- Recipe yield volume can now be entered in cups, fluid ounces, etc., not just milliliters.
- Gap-closer suggestions no longer recommend absurd serving sizes.
- Two-step complement food combinations no longer show a combo with no second step.
- A "Check for updates now" link lets you undo a dismissed update notice.
- "Did you mean" can now fix two misspelled words in a search at once.
- Keyboard shortcuts (Alt+Shift+key) no longer go dead while you're typing.
- Dropdown menu numbers (Foods/Recipes/Analysis) are now real keyboard shortcuts.
- "Did you mean" suggestions now appear on every search box, not just some.
- The "Choose fields to copy" page can select or deselect a whole nutrient group at once.
- Edit Custom Profile can copy just the fields you choose from another food, and shows amino-acid status in its search results.
- The manual now opens in its own tab and picks up where you left off.
- The Recent program updates log now marks a clear line for each release, and the summary above that line is what release downloads on GitHub show first.
- Appendix H's Full Nutrient Key now flags which nutrients have a built-in safe-intake ceiling (UL) and summarizes, from NIH, what happens if you exceed it.
- Glycemic index lookup now searches the full ~2,487-entry published reference table, by subject population, instead of a small 62-item starter set.
- The bundled French CIQUAL food database is now the 2025 edition (3,484 foods, up from 3,186), replacing the 2020 edition NuMa shipped with until now.
- Nutrient table color coding: "near" is now blue and "below minimum" is now orange (previously the other way around) — a near-minimum reading is a reassuring state, not a warning one.
- The "Why you can trust NuMa" testing section is simpler to read, and now mentions mutation testing in plain language.
- No visible change: mutation testing found and closed real coverage gaps in two more modules (amino-acid estimation, recipe nutrient aggregation).

##### September 21 program updates

**USER MANUAL NOW UPDATES SEPARATELY FROM THE PROGRAM**

The home page now shows a separate "NEW USER MANUAL AVAILABLE" notice when a newer manual is published, with an **Update manual now** button — no program update, no restart. If the new manual describes features from a newer program than yours, the notice says so. The home page also shows which manual version you have.

<!--
```
Scope: numa_app/services/manual_update.py (new), scripts/publish_manual.py
(new), web/backend.py (/, /manual, /manual-update-now, /manual-notice/ack-banner,
/check-for-updates), web/templates/home.html, numa_app/services/update_check.py,
requirements.txt (+cryptography), tests/test_manual_update.py (new),
tests/test_web.py, tests/test_update_check.py, tests/conftest.py.
The manual is published as a rolling PRERELEASE "manual-latest" (prerelease so
releases/latest and install-linux.sh are unaffected) with three assets:
user-manual.html, manual-manifest.json (stamp, sha256, size, requires_program),
and manual-manifest.sig (Ed25519 over the manifest bytes; private key at
~/.config/numa-signing/manual_signing_key.pem, only the public key is baked
into manual_update.py). Downloads install to <data dir>/manual/, are
re-verified on every serve, and win only while newer than the baked-in
manual's stamp. /manual skips rebuild_manual_if_stale() for downloaded copies
(html-only, no .md). update_check now ignores non-"v" release tags.
Publish with: python scripts/publish_manual.py [--dry-run].
Anchor rule going forward: never remove or rename a manual anchor; keep old
ids as aliases (older programs link into newer manuals).
```
-->

##### September 20 program updates

**MAINTENANCE: WEEKLY SWEEP — BROKEN MANUAL ANCHOR FIXED, TWO UNDOCUMENTED FEATURES ADDED, TWO REAL TEST GAPS CLOSED**

Item 1 (CLAUDE.md drift) found one real gap: the new `gi_lookup.py` module (glycemic index table lookup) was missing from the Package Layout listing — added, along with a docstring correction for `import_gi_seed.py`. Item 2 ("NuMa" capitalization) found two real lowercase slips in prose, fixed. Item 3 (vendored Bootstrap) confirmed still current at 5.3.8. Item 5 (manual consolidation) found two shipped features that had only ever appeared in the changelog: the Settings "Browser to Launch" option, and printable pages' Print layout (Full/Half sheet) and Paper size (US Letter/A4) choices — both now documented in the manual body. Item 7 (test coverage) found and closed two real gaps: `has_confirmed_aa_data()`/`aa_indicator()` (the AA-checkmark fix spanning 8+ call sites, flagged in a past session as a recurring risk area) had zero tests anywhere despite the production code being correct; and `anchor_overrides` (the "pin a complement suggestion's graduated table to your own serving size" feature) likewise had zero coverage. Item 8 (stale links) found a real broken one this time: two changelog entries linked to `#web-shortcuts`, an anchor that never actually existed on the keyboard-shortcuts passage in Part 1 — fixed, and a new automated test (`test_manual_internal_links_resolve_to_real_anchors`) now catches this class of drift going forward instead of relying on the manual sweep alone. External URL check: all non-200s were 403/429/404 from sites already known to bot-gate automated requests (claude.ai, ods.od.nih.gov, examine.com, doi.org, researchgate.net, and — newly confirmed this week — fdc.nal.usda.gov, which 404s even a known-valid food-details URL when fetched by curl) — inconclusive, not real rot. Item 4 pruned this log back to the last two weeks.

<!--
```
Scope: CLAUDE.md (gi_lookup.py added to Package Layout; import_gi_seed.py's
entry corrected to describe its actual 62-item bulk-apply role now that
gi_lookup.py covers the full table), user-manual.md (two "NuMa" capitalization
fixes; #web-shortcuts anchor added to Part 1 Section B's heading; Settings
section gains a "Browser to Launch" subsection; Recipes menu's print
description gains Print layout/Paper size coverage), tests/test_usda.py
(new TestHasConfirmedAaData, 7 tests), tests/test_complements.py (new
test_anchor_overrides_pins_grad_steps_to_a_chosen_serving_size),
tests/test_web.py (new TestParseAnchorOverrides, 5 tests),
tests/test_link_integrity.py (new test_manual_internal_links_resolve_to_real_anchors).
Full suite: 1035 passed (was 1021).
```
-->

**THE BUNDLED FRENCH CIQUAL FOOD DATABASE IS NOW THE 2025 EDITION**

Foods from the French CIQUAL source (used in every food search alongside USDA, Open Food Facts, and the other bundled national tables) now come from ANSES's Ciqual 2025 table instead of Ciqual 2020 — 3,484 foods instead of 3,186, including 298 new entries and updated values throughout. Found via this week's annual static-dataset check (a new yearly Maintenance item — see [Extensive code testing](#extensive-code-testing)); AFCD and CoFID, the other two bundled national tables, were checked the same way and are both still current, no newer edition published for either.

<!--
```
Scope: ciqual_data.json regenerated from ANSES's Ciqual 2025 English-language
XLS export (3,484 records, up from 3,186) via scripts/build_ciqual_data.py.
That script needed updating for two source-format changes in the 2025
export: the data sheet was renamed ("compo" -> "food composition", now
tried in order via a new _SHEET_NAMES fallback tuple) and every column
header cell now wraps its label across embedded newlines instead of one
line (e.g. "Protein\n(g\n100g)" vs 2020's "Protein (g/100g)") — column
matching now goes through a new _normalize_header() (newlines and slashes
both collapsed to plain spaces) so this survives similar reformatting in a
future edition too. The Vitamin B9/folate column split into two variants
this edition (plain "total folates" vs a new DFE-adjusted figure); mapped
to the plain total-folates column, matching 2020's single-column semantics.
A new "Vitamin A activity, retinol equivalent" column was deliberately NOT
adopted for vitamin_a_mcg (still retinol-only, unchanged) — its header's
units read "µg/100mg", inconsistent with every other per-100g column on
the sheet, and using it unverified risked silently mis-scaling vitamin A
by 1000x for every CIQUAL food. user-manual.md, README-numa-documentation.md
(~7,600 -> ~8,000 total static-dataset food-name count), numa_app/services/
search_suggest.py (same count, in a code comment) updated to match the new
totals (CoFID 2,886 + AFCD 1,588 + CIQUAL 3,484). Full test suite (1035
tests, including tests/test_ciqual.py) passes unchanged against the new
data — nothing downstream assumed specific CIQUAL record content.
```
-->

**NUTRIENT TABLE COLOR CODING: NEAR/BELOW MINIMUM COLORS SWAPPED FOR A CALMER FEEL**

Every color-coded "% of daily target" column now shows **near** (70–99% of a minimum) in blue and **below minimum** in orange — the reverse of before. Orange reads as a warning color, but being close to a minimum is a reassuring state, not an alarming one; a genuine shortfall is the state that should carry the warning color. [Learn more...](#rda)

<!--
```
Scope: web/static/style.css — .rda-near and .rda-low swap color values
(#1e40af blue / #c2410c orange, both unchanged as literal colors, just
which status class gets which). Applies everywhere the shared rda-met/
rda-near/rda-low/rda-over classes are used (_rda_legend.html and every
nutrient table); no template or backend change needed since color is the
only thing that moved. Full suite: 1035 passed, unaffected (no test
asserts on literal color values, only on class names).
```
-->

**THE "WHY YOU CAN TRUST NUMA" TESTING SECTION IS SIMPLER TO READ, AND NOW MENTIONS MUTATION TESTING**

Part 2's "Extensive code testing" section (part of "Why you can trust NutriMagnus") no longer names specific tool libraries, test file names, or exact per-tier test counts — that detail wasn't helping a non-technical reader trust the program more, it was just jargon in the way. It now explains, in plain language, what automated testing and mutation testing actually are and why they matter, with a pointer to README-numa-documentation.md for anyone who does want the technical detail. Mutation testing specifically — deliberately planting small errors in the code to check whether the test suite actually notices — had never been mentioned here at all before, despite being a real, ongoing part of how NuMa is verified.

<!--
```
Scope: user-manual.md Part 2 Section E (#data-testing-validation) —
"Extensive code testing" subsection rewritten: dropped Hypothesis/
Playwright links, tests/e2e/ and specific *_properties.py/test_complements.py/
test_claude_fetch.py file names, and the 1,019/90/26/6 sub-counts; added a
plain-language mutation-testing paragraph and a pointer to README's Test
Suite/Maintenance sections for technical detail. "Reliable data sources"
subsection left mostly as-is (a typo, "In additions" -> "In addition",
fixed) — reviewed but judged not actually jargon-heavy, just citation-dense,
which is appropriate for a "why trust" section. README-numa-documentation.md
Test Suite section gained three new subsections that were previously
undocumented there at all: "Property-based tests" (naming Hypothesis and
the three *_properties.py files), "Browser-level end-to-end tests" (naming
Playwright and tests/e2e/), and "Mutation testing" (a short pointer to the
existing, fuller Maintenance-section writeup) — so the technical detail
removed from the manual actually landed somewhere, rather than being lost.
```
-->

**NO VISIBLE CHANGE: MUTATION TESTING FOUND AND CLOSED REAL COVERAGE GAPS IN TWO MORE MODULES**

The weekly sweep's mutation-testing churn check flagged `aa_estimate.py` and `recipe_nutrients.py` (both had real code changes since their last check, from the AA-checkmark fix and the new glycemic-index/complement-anchor work). Triaged this session: `aa_estimate.py`'s AA-scaling error paths and note-formatting helpers went from 13 real gaps to 0; `recipe_nutrients.py`'s complement-merge success path (previously entirely untested) and its recipe-ingredient-expansion skip logic went from 85 to 43 survivors, with the remainder confirmed to be an equivalent-mutant artifact of `sqlite3.Row`'s case-insensitive key lookups rather than real gaps. 37 new tests total. See TESTING-ROADMAP.md item #5 and README-numa-documentation.md's mutation-testing log for the full triage detail.

<!--
```
Scope: tests/test_aa_estimate.py (16 new tests: exact-text error messages,
rounding precision, target/source-protein boundary at exactly 1.0g,
source_note()'s id_part fallback, and full coverage of copy_nutrients_note()
which had none at all). tests/test_recipe_nutrients.py (21 new tests:
best_aa_nutrients()'s merge/scale success path via a real curated-table
entry, ref_protein==0 boundary via monkeypatch; atomic_recipe_ingredients()/
expand_recipe_ingredients()'s continue-vs-break skip branches for a deleted
sub-recipe reference, a zero-serving sub-recipe, an uncached food, empty
cached nutrients, and a sub-recipe scaling to zero protein; sub["servings"]
or 1 defaulting; the "not sub or sub_servings <= 0" vs "and" logic bug;
leaf["fdc_id"] key coverage). No application code changed. Full suite: 1059
passed (was 1035).
```
-->

**LIST PAGES NO LONGER RESET WHEN YOU ARCHIVE OR DELETE A ROW**

Archiving, restoring, or deleting an item from a list — Recipes, My Pantry, Food Cache, a recipe's saved translations, or a saved DIAAS override — used to reload the whole page from scratch, which reset any search, sort order, or "show archived" filter you had set. Now only that one row changes; everything else on the page stays exactly as it was, including your place in a long filtered search. The Recipes list header was also fixed along the way — it read "Selected recipes in internal database" even when nothing was selected; now it just says "Recipes in internal database".

<!--
```
Scope: web/templates/base.html — new shared fetch()-based handler for
forms marked class="js-row-remove" (always removes the closest row) or
class="js-row-archive" (toggles archived state in place — badge, button
label/title, row shading — removing the row only when the enclosing
[data-show-archived] table isn't currently showing archived items); falls
back to a normal form submit if the request fails or the server reports
the action didn't go through (e.g. a blocked Food Cache delete still needs
its full explanation page). web/backend.py — new _is_ajax_row_action()
helper; recipe_delete_post, recipe_archive, pantry_remove, pantry_archive,
food_cache_delete, food_cache_archive, settings_diaas_override_delete, and
recipe_translation_delete now return a small JSON reply instead of a
redirect when that header is present, with existing non-JS behavior
unchanged otherwise. web/templates/recipes.html, pantry.html,
food_cache.html, food_cache_db_check.html, settings.html,
recipe_translate.html, recipe_detail.html — forms wired to the new classes.
Also fixed recipes.html's list header, which read "Selected recipes in
internal database" even though nothing on the page is a "selection" (that
word is used elsewhere for the Compare checkboxes) — now "Recipes in
internal database". Deliberately left meal-item removal and Compare's
remove-from-comparison alone: both already redirect back to an equivalent
state with no data lost, and meal.html's running nutrient totals and
compare.html's per-item columns would need a real re-render on removal
rather than a plain row deletion, so converting those risks showing stale
aggregate numbers in a nutrition app — not worth it for what's currently
just an extra page flash, not the state-loss bug reported here.
```
-->

**FULL NUTRIENT KEY NOW FLAGS EACH NUTRIENT'S SAFE-INTAKE CEILING AND WHAT HAPPENS IF YOU EXCEED IT**

Appendix H's [Full Nutrient Key](#nutrient-key) previously described what each nutrient does but said nothing about its safety ceiling. The twelve nutrients with a built-in Tolerable Upper Intake Level (UL) — calcium, phosphorus, iron, zinc, iodine, selenium, vitamins A, C, D, and E, B6, and choline — now each carry two sub-points: one flagging that the nutrient has a UL and linking to [Maximum Nutrient Limits](#maxlimits) for the number itself, and a second summarizing, in plain language, what NIH says actually happens if you exceed it — from calcium's kidney-stone risk to vitamin B6's nerve-damage risk at sustained high supplemental doses. [Learn more...](#nutrient-key)

<!--
```
Scope: user-manual.md Appendix H (#nutrient-key) — each of the 12 UL-
bearing nutrient entries (Calcium, Phosphorus, Iron, Zinc, Iodine,
Selenium, Vitamin A, Vitamin C, Vitamin D, Vitamin E, Vitamin B6, Choline)
split into a two-item nested sub-list: "Has a built-in Tolerable Upper
Intake Level..." (added first, linking to #maxlimits) and "Risk of
excess: ..." (this entry), each summarizing that nutrient's NIH Office of
Dietary Supplements consumer fact sheet. New footnotes 48-59, one per
nutrient, citing the specific ODS consumer fact sheet URL used (NIH's own
site blocks WebFetch with a 403, so content was pulled via WebSearch
snippets of those pages instead of a direct fetch).
```
-->

**RECENT PROGRAM UPDATES LOG NOW MARKS RELEASE BOUNDARIES**

This log's dated entries are grouped under release boundaries — a heading like "Release v2026-09-14-2336 boundary" marks the last entry that shipped in that release, so it's clear at a glance which entries are already out and which are still pending. The entries still pending sit under a "Next release" heading at the top, with a short plain-language summary bullet for each one; that summary list is what shows up first when you look at a new release download on GitHub.

<!--
```
Scope: user-manual.md Appendix A — every dated entry heading demoted from
h4 (####) to h5 (#####); new h4 "Release <tag> boundary" headings inserted
between releases (only the 2026-09-14 boundary backfilled — earlier
boundaries are not being reconstructed); "Release to be done" heading holds
a running bullet list of one-line summaries for unreleased entries.
scripts/create_release.py — _release_notes_for_today() replaced with
_release_notes(), which now reads the bullet list under "Release to be
done" instead of matching today's date heading; new _roll_release_boundary()
renames that heading to "Release <tag> boundary" and inserts a fresh empty
"Release to be done" above it, called automatically after a release is
created.
```
-->

**GLYCEMIC INDEX LOOKUP NOW SEARCHES THE FULL PUBLISHED REFERENCE TABLE**

Every food's Annotate page can now search the full ~2,487-entry Foster-Powell glycemic index table directly, instead of relying on a small 62-item automatic starter set for common foods. Type the food's name (already filled in for you), choose normal glucose tolerance, impaired glucose tolerance/diabetes, or both, and NuMa lists every plausible match — not just its single best guess — so you pick the right one yourself. A new [Settings](#settings) option sets which population the lookup defaults to. [Learn more...](#gi)

<!--
```
Scope: scripts/build_gi_data.py — new one-time ingest script parsing the two
Foster-Powell/Holt/Brand-Miller online-only appendix PDFs (Table A1, normal
glucose tolerance; Table A2, impaired glucose tolerance/small-n/high-
variance) into gi_data.json (1,879 + 608 entries), via pdftotext -layout
with per-page column-boundary detection (column offsets drift slightly page
to page). gi_lookup.py — new fuzzy name-search module (difflib, same
normalize approach as search_suggest.py/import_gi_seed.py) returning
ranked multi-candidate matches rather than a single best guess; GI values
are read from the glucose-referenced column only (GI, Glucose=100), never
the bread-referenced column; serve size/available carbohydrate/GL are not
captured, since GL is already computed live from a food's own cached
carbohydrate content (numa_app.services.glycemic_load). profile.py — new
UserProfile.glucose_tolerance field ("", "normal", "impaired"). web/
backend.py — new GET /food/annotate/{fdc_id}/gi-lookup JSON endpoint;
settings_post accepts glucose_tolerance. web/templates/food_annotate.html —
new lookup section (search box, population selector, results table with
per-row "Use" buttons that fill the GI field client-side; nothing is
written until the existing Save annotation button is used).
web/templates/settings.html — new Glycemic index lookup default select.
import_gi_seed.py — docstring updated to point at the new full-table web
lookup; its own 62-item exact-match bulk-apply behavior is unchanged.
```
-->

##### September 19 program updates

**NUTRIENT TABLES: SEPARATE MINIMUM, TARGET, AND MAXIMUM COLUMNS**

Earlier today's single "Daily Target" column (added this same day — see below) turned out to still be confusing: it carried whichever DRI figure applied to a nutrient — a floor to meet, a two-sided ideal, or a ceiling not to exceed — under one ambiguous heading, with only a tiny "min"/"target"/"max" tag two columns over to tell them apart. Every nutrient table now has three separate columns instead — **Minimum**, **Target**, **Maximum** — right after Unit; each nutrient's figure lands in exactly one of the three (the other two show "—" for that row), so which kind of number you're looking at is never in question. A footer note under every table explains all four columns (Minimum, Target, Maximum, and the existing UL) with a link back to the manual. [Learn more...](#rda)

<!--
```
Scope: web/backend.py — _nutrient_sections() now computes rda_minimum,
rda_target, rda_maximum (one populated per row, keyed off rda_type) instead
of the single rda_goal field from the same-day earlier entry. web/templates/
_rda_goal_column.html rewritten from a fixed one-column macro to a
parameterized header(label)/cell(value) pair, called 3x per template (once
per column) across all 8 nutrient-table templates. web/templates/
_rda_definition_footer.html rewritten with 4 separate paragraphs (Minimum,
Target, Maximum, UL) replacing the prior single RDA + max-vs-UL note.
user-manual.md Part 4 §P (#rda) rewritten to document the 3-column split.
```
-->

**NUTRIENT PLOT: "CLEAR ALL NUTRIENT CHECKMARKS" BUTTON, AND CLEARER WORDING ON WHAT COMPLETENESS AFFECTS**

A **Clear all nutrient checkmarks** link now sits above the nutrient checklist, unchecking every box in one click instead of one at a time when starting a fresh selection. The page also now always states, up front, that every logged day appears in the plot regardless of whether its meals are marked complete — only a day with no logged meal at all leaves a gap — and that "Always end on last complete day" only ever changes where the plot's trailing edge sits, not which days in between show. That explanation previously existed only as a caption shown on the Home page, and only when that toggle was on; the Nutrient Plot page itself said nothing about completeness at all. [Learn more...](#nutrient-plot)

<!--
```
Scope: web/templates/nutrient_plot.html — new "Clear all nutrient
checkmarks" link (#clear-nutrient-checkmarks) above the checklist, wired to
a small JS handler that unchecks every input[name="nutrients"] without
submitting (deliberately not auto-submitting like the existing Auto links,
since clearing is a starting point for picking a new set, not something to
plot immediately). New always-visible intro paragraph states the actual
date-range behavior (_nutrient_plot_params() in web/backend.py already
built `dates` from every meal_date with at least one meal regardless of its
`complete` flag — db.meal_dates_with_bcp() has no completeness filter — so
this was a documentation gap, not a logic bug; only the "rolling"/Always-
end-on-last-complete-day path, which is off by default, ever excludes
trailing dates, and only past whichever date db.last_complete_meal_date()
resolves to). user-manual.md Part 4 §S (#nutrient-plot) updated to match.
Test added: test_nutrient_plot_clear_nutrients_button_and_gap_note.
```
-->

**NUTRIENT TABLES NOW SHOW THE ACTUAL RDA/LIMIT NUMBER, NOT JUST A PERCENTAGE**

Every nutrient table (food, recipe, meal, day, trend, and print pages) now has a **Daily Target** column showing the actual RDA/AI/limit figure itself — e.g. "1.3 mg" for riboflavin, "2300.0 mg" for sodium — right next to the existing percentage. Previously that number was only reachable by hovering the percentage badge's tooltip, which isn't visible on every device or browser; a badge colored orange or red could look alarming with no way to see what it was actually being measured against. A new note also spells out that a Daily Target row tagged "max" (currently sodium only) is a different, more conservative figure than the separate UL (Tolerable Upper Intake Level) column — the two ceilings are easy to conflate but never appear on the same nutrient. [Learn more...](#rda)

<!--
```
Scope: web/backend.py — _nutrient_sections() computes rda_goal = f"{rda_val:.1f}
{rda_unit}" alongside the existing pct/rda_css_val, added to each row dict (and
the DCP pseudo-row). New shared macro web/templates/_rda_goal_column.html
(header()/cell(), mirroring the existing _ul_column.html pattern) imported
and wired into all 8 nutrient-table templates (meal.html, meal_day.html,
recipe_detail.html, print.html, food_detail.html, summary.html, trend.html,
food_analyze_recipe_portion.html) — new column inserted right after Unit,
gated by has_profile same as the %-of-target column it sits beside.
web/templates/_rda_definition_footer.html gained a second note paragraph
distinguishing a "max"-tagged Daily Target (an RDA-table rda_type=="limit"
row, currently only sodium's 2300 mg CDRR figure from profile.compute_rda)
from the separate UL column (profile.get_max_limits/compute_upper_limits) —
sodium is deliberately excluded from the UL table already, so the two never
overlap on one nutrient, but nothing on the page previously said so.
user-manual.md Part 4 §P (#rda) updated to document the new column and this
same max-vs-UL distinction.
```
-->

**NUTRIENT PLOT NOW SHOWS MAXIMUM LIMIT LINES, NOT JUST GOAL LINES**

The [Nutrient Plot](#nutrient-plot) already drew a dashed reference line for a nutrient's profile goal (Revised Optimal target, or RDA/AI where no Optimal is set). It now also draws a dotted reference line for that nutrient's maximum limit — a built-in Tolerable Upper Intake Level, or your own configured cap if you've set one — for any chosen nutrient that has one. Both lines draw in that nutrient's own line color, so goal and limit stay easy to tell apart from the data line and from each other.

<!--
```
Scope: numa_app/services/plotting.py — line_plot_image() draws a series'
"limit" value as a dotted axhline (existing "goal" stays dashed). web/
backend.py — new _nutrient_plot_limit()/_nutrient_plot_add_limits(),
mirroring _nutrient_plot_goal()/_nutrient_plot_add_goals(), sourced from
profile.get_max_limits() (built-in ULs merged with user max_limits
overrides); wired into the /summary/nutrient-plot/image endpoint alongside
the existing goal attachment. Scale-factor steps (_apply_plot_scale_factor,
_apply_individual_factors) now rescale "limit" the same way they already
rescaled "goal", so the dotted line stays aligned to the data after either
scaling step. Subtitle text picks goal-only/limit-only/both wording
depending on which reference lines are actually present on the chart. This
closes the "Plots of individual nutrients..." item in Part 9 — the
per-nutrient goal/limit data problem it was waiting on (profile.compute_
optimal/compute_rda/get_max_limits) was already solved elsewhere; only the
second reference line was missing. Test added:
test_nutrient_plot_image_renders_limit_lines.
```
-->

**A FOOD'S DIGESTIBLE COMPLETE PROTEIN NOW MATCHES ITS MEAL AND RECIPE VALUES**

A single food's own DCP figure (on its Food Cache detail page and in its Protein Summary/Protein Quality sections) could come out noticeably lower than the same food's contribution shown in a meal's Top Contributors table — for one bread, 2.1 g per 100 g on the food page versus a rate implying 3.8 g per 100 g in a meal. The two were pulling digestibility from different tables and, on the food page, applying an amino-acid-limitation penalty a second time on top of a digestibility figure that already had it baked in. The food page now uses the same digestibility source as meal- and recipe-level DIAAS, so a food's own DCP and its contribution inside a meal or recipe agree.

<!--
```
Scope: web/backend.py — _protein_section() (food_detail route) and
_food_complement_section() now source `digestibility` from
diaas.get_digestibility(food_name, conn) instead of usda_nutrients.get_diaas().
Root cause: usda_nutrients._DIAAS_TABLE stores full, already amino-acid-
balance-adjusted literature DIAAS scores (e.g. bread 0.46, keyed on the same
"bread"/"wheat" keywords diaas.py's _DIGESTIBILITY_TABLE uses for a pure
0.84 true-ileal-digestibility estimate), but _protein_section() treated that
0.46 as raw digestibility and then multiplied by protein_completeness()'s own
freshly-computed limiting-amino-acid ratio, penalizing amino acid limitation
twice. Meal-level diaas.py never had this bug — it always used the pure
digestibility table. export.py's three _render_bioavailability_* single-food
report renderers switched to the same diaas.get_digestibility() call (no conn
available there, so no per-food user override lookup in exported reports)
for consistent numbers between the app and exported reports. Side effect:
diaas.get_digestibility() always returns a value (defaulting to 0.82 for an
unrecognized food name) where usda_nutrients.get_diaas() could return None,
so food_detail.html's now-unreachable "no DIAAS reference for this food"
fallback card was removed — every food with amino acid data now gets a DCP
estimate. Tests updated: test_food_detail_protein_summary_shows_completeness_
without_diaas_reference (renamed, now checks the default-digestibility DCP
instead of the removed fallback text) and
test_unusable_protein_line_absent_for_complete_food (switched its test food
from chicken, whose true digestibility is 0.96, to milk, at 1.00, to keep
testing the zero-unusable-protein suppression case).
```
-->

**NEW: FULL NUTRIENT KEY (APPENDIX H)**

A new appendix gives a plain-language entry for every nutrient NuMa tracks — what it does, where it's discussed elsewhere in this manual, and a link to a respected outside source (mostly the Linus Pauling Institute's Micronutrient Information Center) for anyone who wants to go deeper than a nutrient table can show. All five Nutrient Analysis groups are covered (Macronutrients, Omega Fatty Acids, Minerals, Vitamins, Phytonutrients); amino acids point back to their own existing extensive treatment instead of repeating it. [Learn more...](#nutrient-key)

<!--
```
Scope: user-manual.md — new Part 10 Appendix H (#nutrient-key), replacing
the "under development" Part 9 stub. 40 nutrient entries across 5 groups,
cross-linked to ~15 existing manual sections (RDA, Daily Nutrient Goals,
DCP, Essential Amino Acids, Omega-3, Antinutrients, Diet-Aware
Bioavailability, Maximum Nutrient Limits, Revised Optimal, Glycemic Load).
25 new footnotes ([^17]-[^47]), each an externally-verified URL (fetched
and confirmed live before citing, mostly Linus Pauling Institute
Micronutrient Information Center pages plus a few MedlinePlus and
Examine.com pages for macronutrients). Minerals/Vitamins/Phytonutrients/
Omega groups are sub-grouped by standard nutrition-science families
(macro- vs. trace minerals, fat- vs. water-soluble vitamins, carotenoids
vs. other phytonutrients, omega-3 vs. omega-6) using heading+bullet
nesting; Macronutrients uses the same nesting for the literal subset
relationship (Fiber/Sugar under Carbohydrates, the three fat types under
Fat) — see the separate entry below for that same hierarchy reaching the
app's own nutrient tables. Part 9's old stub now points to this appendix.
```
-->

**FIBER, SUGAR, AND THE THREE FAT TYPES NOW SHOW INDENTED UNDER CARBOHYDRATES AND FAT**

Fiber and Sugar are subsets of Carbohydrates, not additional to it — and Saturated, Monounsaturated, and Polyunsaturated fat are subsets of Fat the same way — the same relationship a Nutrition Facts label shows by indenting those rows under their parent. Every nutrient table in NuMa (food, recipe, meal, daily-summary, and the printable report) now shows that same indentation instead of five flat, same-looking rows. See the new [Full Nutrient Key](#nutrient-key) (Appendix H) for a plain-language description of every nutrient NuMa tracks, including this same parent/child relationship spelled out in full. [Learn more...](#nesting-carb-subtypes)

<!--
```
Scope: web/backend.py — _nutrient_sections() gained a _SUBTYPE_KEYS constant
(fiber_g, sugar_g, saturated_fat_g, mono_fat_g, poly_fat_g) and each row now
carries an is_subtype flag. web/static/style.css gained a .subtype-row
CSS rule (padding-left on the label cell). All 8 nutrient-table templates
(food_detail, recipe_detail, meal, meal_day, summary, trend,
food_analyze_recipe_portion, print) apply the subtype-row class when the
flag is set; print.html carries its own inline copy of the CSS rule since
it doesn't load style.css. New test:
test_nutrient_table_indents_carb_and_fat_subtypes in tests/test_web.py.
New user-manual.md Appendix H (#nutrient-key) built in the same session,
covering all five Nutrient Analysis groups (Macronutrients, Omega Fatty
Acids, Minerals, Vitamins, Phytonutrients) with internal cross-links and
external citations (footnotes 17-47, mostly Linus Pauling Institute
Micronutrient Information Center pages, each URL verified live before
citing).
```
-->

##### September 17 program updates

**YOU CAN NOW PIN A COMPLEMENT SUGGESTION'S GRADUATED AMOUNTS TO YOUR OWN SERVING SIZE**

On a meal, food, or recipe's Complement Suggestions section, each suggestion's 25/50/75/100% graduated table now has a small "Base the scale above on: ___ g" field. Normally that table is scaled off the amount needed to *fully* close the amino acid gap — but for some foods that amount is impractically large (e.g. hundreds of grams of a protein powder), because the food's own ratio of the gapped amino acid to its total protein is only barely above the reference target. Type your own realistic serving size there and the table recalculates around it instead, so you can see the real effect of an amount you'd actually eat.

<!--
```
Scope: numa_app/services/complements.py (build_complement_display gains
anchor_overrides: dict[str, float] param, keyed by suggestion name lowercased;
_grad_steps() takes an anchor_grams override that replaces the math-derived
full_grams as the basis for the 25/50/75/100% fractions, while dig_protein per
step still scales off the food's real per-gram digestible-protein rate; _fmt()
surfaces full_closure_grams when the override differs from the true closure
amount, for the "fully closing this gap would take Ng" note). web/backend.py
adds _parse_anchor_overrides() and threads anchor_name/anchor_grams query-param
lists through _food_detail_context/_food_complement_section (food_detail route),
meal_view, and _recipe_detail_context/recipe_detail route into
_complement_suggestions/build_complement_display. New shared partial
web/templates/_complement_anchor.html renders the input; wired into meal.html,
food_detail.html (which previously had no graduated table at all — added to
match), and recipe_detail.html's suggest_card macros, submitted via the
existing #complements-form GET form alongside ignore_complements. Also fixed a
pre-existing sign-formatting bug (literal "+" prefix concatenated with a
possibly-negative "%.0f"-formatted pct_increase, e.g. "+-8%") across all six
grad_steps/diaas_improver step tables, using "%+.0f" instead.
```
-->

**THE "RECIPE SAVED" BANNER NO LONGER LINGERS OVER UNSAVED EDITS**

On a recipe's Edit page, the green **Recipe saved** banner used to stay up no matter what you typed afterward — implying edits you hadn't saved yet were already saved. It now disappears the instant you touch any field in Recipe details, so it never claims more than it knows.

<!--
```
Scope: web/templates/recipe_edit.html — the existing "unsaved Recipe details"
dirty-tracking script (added for the ingredient-add warning) now also removes
the #recipe-saved-alert element on the first input/change event against
#recipe-details-form.
```
-->

**RECIPE YIELD VOLUME CAN NOW BE ENTERED IN CUPS, FLUID OUNCES, ETC. — NOT JUST MILLILITERS**

The **Total yield volume** field on a recipe's Edit page now has a unit dropdown (mL, L, cup, fl oz, tbsp, tsp) instead of forcing milliliters. The explanation next to it also now spells out what entering this actually does: paired with the yield weight, it lets the [Convert](#convert) tool work out the recipe's density, so you can type an amount in one unit (like "1 cup") and see it converted to another (grams, ounces, servings) on that recipe's Convert page.

<!--
```
Scope: web/templates/recipe_edit.html (total_volume_unit <select>, options ml/l/
cup/floz/tbsp/tsp, expanded help text), web/backend.py recipe_edit_post() (new
total_volume_unit form field, converted to mL via the existing
numa_app.services.portions._VOLUME_TO_ML table before storage — total_volume
is still always persisted in mL internally, matching food_convert_recipe()'s
density calc which assumes mL).
```
-->

**GAP-CLOSER SUGGESTIONS NO LONGER RECOMMEND ABSURD SERVING SIZES**

A [complement suggestion](#comp) that could only close its amino acid gap with an implausibly large amount — hundreds of grams of a concentrated food like protein powder — used to be shown anyway, as long as it stayed under a 500&nbsp;g ceiling that was really just a "not mathematically impossible" check, not a real-world sanity check. That ceiling is now 300&nbsp;g, and when a candidate's full-gap-closing amount would exceed it, the suggestion now falls back to the smaller amount needed to close a lesser amino acid gap it can still reach in a practical serving, rather than showing hundreds of grams of one food as your only option. [Learn more...](#comp)

<!--
```
Scope: usda_nutrients.py — new module constant MAX_PRACTICAL_GAP_CLOSER_GRAMS
(300) replaces the hardcoded literal in _score_one_complement()'s
"grams <= 0 or grams > 500" guard; re-exported via usda.py. suggest_complements()
already iterates candidate target AAs in gap order and falls through to the next
gap when _score_one_complement() returns None for the primary one, so lowering
the cap alone causes foods that fail the primary-gap closure (blocked by the new,
tighter ceiling) to naturally surface their secondary-gap closure instead — no
change needed there. numa_app/services/complements.py's exhausted_msg text
(previously hardcoded "≤ 500 g") now reads the same constant.
```
-->

**TWO-STEP COMBINATIONS NO LONGER SHOWS A COMBO WITH NO SECOND STEP**

The Two-Step Combinations section used to include a "Combination" card even when no Step 2 booster qualified for it — duplicating a suggestion already shown in the ordinary Protein Complement Suggestions list above it, but dressed up as a "combination" with nothing to combine. Those step-1-only entries no longer appear here; they're still visible in the regular Complement Suggestions section where they add real information.

<!--
```
Scope: numa_app/services/complements.py — build_complement_display() only
appends to two_step_combos when two_step_combo()'s returned dict has a
non-None "step2", instead of appending on any non-None combo. Also fixed a
related bug found while investigating: two_step_combo()'s gc_diaas (the pool
DIAAS Step 1 achieves, used as the bar Step 2 must clear) came from
predicted_diaas uncapped, which can mathematically exceed 1.0 when a
combined pool over-supplies every essential amino acid — every other DIAAS
comparison in this file caps at min(1.0, ...), but this one didn't, so an
over-1.0 gc_diaas could make Step 2 structurally impossible (no real
candidate's capped score can ever exceed it) even when a genuine
improvement existed. Now capped the same way.
```
-->

##### September 16 program updates

**A COMPLEMENT FOOD NO LONGER SHOWS UP TWICE IN DIAAS-BOOSTING OPTIONS**

A protein-complement suggestion could appear as two separate cards under [DIAAS-Boosting Options](#comp) on a food, recipe, or meal page — once correctly linked to its real Food Cache entry, and once as an unlinked "generic estimate" duplicate of the very same food. Only the correctly-linked card now shows.

<!--
```
Scope: web/backend.py _web_pantry_candidates() — pantry candidate dicts were
missing their own "fdc_id" key, so a pantry item's DIAAS-improver suggestion
always looked unidentified even when it had real cached nutrient data.
usda_nutrients.py suggest_complements() — the same cached food could also be
pulled into the "general" tier's candidate pool via load_cache_candidates()
whenever its pantry display name didn't literally match the curated
complement table's entry name (e.g. "Nutritional Yeast Flakes (FDC
2411476)" vs. the table's "Nutritional yeast"), producing a second,
independently-scored suggestion for the same fdc_id; general_candidates
construction now skips a curated match whose fdc_id is already present in
pantry_candidates, and the pantry+general DIAAS-improver merge now dedupes
by fdc_id/recipe_id (falling back to name) instead of trusting each pool to
be duplicate-free on its own.
```
-->

**A "CHECK FOR UPDATES NOW" LINK, FOR CHANGING YOUR MIND AFTER DISMISSING ONE**

Dismissed an UPDATE AVAILABLE banner (see below) and want it back — because you changed your mind, or just want to re-check right now instead of waiting for the periodic check? A new **Check for updates now** link sits right next to the version date at the bottom of the home page. It undoes any dismissal and re-checks GitHub immediately; it only appears when no update banner is currently showing.

<!--
```
Scope: numa_app/services/update_check.py — new clear_cache() resets the
module-level check cache. web/backend.py — new POST /check-for-updates
route clears both that cache and prefs.json's update_notice_dismissed_tag
(set to "" rather than deleted, since _save_prefs_file only merges).
web/templates/home.html — "Check for updates now" link/form next to the
version-date line, shown only when update_available is falsy. New test:
tests/test_web.py test_check_for_updates_now_undoes_a_dismissal.
```
-->

**"UPDATE AVAILABLE" NO LONGER DISAPPEARS ON ITS OWN**

The home page's UPDATE AVAILABLE banner used to hide itself again shortly after first appearing — by default, at most once per calendar day — even if you hadn't updated or read it yet. It now stays on every page load, restart included, until you either install the update or check its new **Don't show this again for this version** checkbox (the same pattern as the System Issues banner's "Got it" checkbox). Checking it only dismisses that exact release; a later one still shows. The Settings → Update Notifications daily/weekly/monthly frequency setting is gone — this checkbox replaces it.

<!--
```
Scope: web/backend.py — removed _UPDATE_NOTIFY_FREQ_LABELS/_DAYS,
_VALID_UPDATE_NOTIFY_FREQS, _current_update_notify_frequency(), and the
POST /settings/update-notify-frequency route. _should_show_update_notice()
now just compares the release tag against a new
prefs.json update_notice_dismissed_tag key (set by new POST
/update-notice/ack-banner, mirroring /recompute-errors/ack-banner). Root
cause: the old logic persisted a last-shown date the first time a release
was seen, then suppressed every same-day recheck — so a restart or reload
minutes later (as opposed to the intended "next calendar day") already
hid it, with no way to bring it back short of a new release. web/templates/
home.html (dismiss checkbox + form, removed frequency line), settings.html
(removed "Update Notifications" section). tests/test_web.py: replaced
test_update_notice_frequency_gate_lets_a_newer_release_through with
test_update_notice_keeps_showing_until_dismissed and
test_update_notice_dismiss_checkbox_hides_only_that_release.
```
-->

**"DID YOU MEAN" CAN NOW FIX TWO MISSPELLED WORDS AT ONCE**

Searching for something like `triskitt originle` (two typos) used to only ever suggest a correction for one word at a time — `triscuit originle` or `triskitt original`, both still broken if you clicked them. The first suggestion now fixes every misspelled word in the query together — `triscuit original` — so clicking it actually finds something.

<!--
```
Scope: numa_app/services/search_suggest.py suggest() — previously built one
variant per (word index, candidate) pair, substituting only that one word.
Now collects candidate replacements per out-of-corpus word first, and when
more than one word needs fixing, adds a single combined variant (each
word's best candidate applied at once) ahead of the existing per-word
variants. New test: tests/test_search_suggest.py
test_suggest_corrects_two_misspelled_words_at_once.
```
-->

**A TYPO'D SEARCH WORD NO LONGER SILENTLY GETS DROPPED IN FAVOR OF A GENERIC WORD LIKE "ORIGINAL"**

Searching Food Cache (or any other local search) for something like `triskitt original` used to quietly ignore the misspelled `triskitt` and return hits matched on `original` alone, with no indication anything was wrong — a search that looks like it worked, on a food you didn't actually ask for. That search now correctly finds nothing, and offers the ["Did you mean"](#search-suggestions) correction (`triscuit original`) instead.

<!--
```
Scope: db.py _OR_FALLBACK_STOPWORDS — the any-word OR-fallback search for
user-drafted foods (search_cached_foods()) already excluded generic
prep/state words (raw, cooked, ...) from single-handedly justifying a match,
per the August 27 fix for "orange raw" wrongly surfacing "Raw Brazil Nuts".
Same failure mode, different word category: "original", "organic",
"classic", and "traditional" are near-universal branded-food descriptors
that carry no identifying signal on their own, so they're now excluded too.
New regression test in tests/test_db.py:
test_search_cached_foods_generic_descriptor_word_alone_does_not_trigger_or_fallback.
```
-->

**KEYBOARD SHORTCUTS (ALT+SHIFT+KEY) NO LONGER GO DEAD WHILE YOU'RE TYPING**

The [Alt+Shift navigation shortcuts](#web-shortcuts) (F, R, M, N, S, A, and the Settings section numbers) now keep working even while your cursor is sitting in a text box — which on a data-entry app is most of the time. Previously they silently stopped working the moment any field had focus, so the browser's own default handling took over instead, making the shortcuts feel broken or unreliable in normal use.

<!--
```
Scope: web/templates/base.html — the Alt+Shift keydown handler bailed out
whenever document.activeElement was an INPUT/TEXTAREA/SELECT, before it
could call preventDefault(), so the browser's native handling of that key
combo ran instead. That guard made sense on macOS, where Option(Alt)+Shift+
letter really can insert a special character into a text field, but on
Windows/Linux Alt+Shift+letter never inserts anything, so there was nothing
to protect and it just killed the shortcuts almost all the time, since most
NuMa pages autofocus a text input on load. Narrowed the guard to only apply
on macOS (detected via navigator.platform); Windows/Linux now ignore focus
entirely for this handler, matching the "works in any desktop browser"
claim already in Settings section 4.
```
-->

**FOODS/RECIPES/ANALYSIS KEYBOARD SHORTCUTS NOW WORK WITH A NARROW BROWSER WINDOW**

Pressing Alt+Shift+F, R, or N to jump to the Foods, Recipes, or Analysis dropdown did nothing if your browser window was narrow enough that the main menu had collapsed into the mobile-style hamburger icon (roughly less than 768 pixels wide — a half-screen window on many laptops). The shortcut now expands the menu first, so the dropdown opens and gets focus regardless of window width.

<!--
```
Scope: web/templates/base.html — the Alt+Shift keydown handler's dropdown
branch called target.click() then firstItem.focus() without checking
whether the toggle's ancestor #main-nav (Bootstrap's .navbar-collapse) was
actually expanded. Below the navbar-expand-md breakpoint, #main-nav starts
display:none until its own "show" class is added by the hamburger toggler;
Bootstrap still added "show" to the dropdown-menu itself on click, but a
hidden ancestor kept it invisible, so the subsequent focus() call silently
failed on a display:none descendant. Now checks navCollapse.contains(target)
before the existing click()/focus() logic.

First attempt at the collapse-expand check used
!navCollapse.classList.contains('show'), which turned out to be true on
every press even at full desktop width — navbar-expand-md's CSS forces
the collapse visible there (display:flex !important) without the JS ever
adding "show", so bootstrap.Collapse.show() fired unconditionally,
animating an already-visible element's height from 0 and producing a
visible "opens on top, then drops into place" glitch on every shortcut
press regardless of window width. Fixed by checking
getComputedStyle(navCollapse).display === 'none' instead, which is only
true when the collapse is genuinely hidden (below the breakpoint,
unexpanded). Verified with Playwright: at 1200px a MutationObserver on
#main-nav sees zero attribute/style mutations (Collapse is never
instantiated) and the dropdown opens with no animation; at 600px the
collapse still expands and focus lands correctly. Full test suite: 1008
passed.
```
-->

**DROPDOWN MENU NUMBERS (FOODS/RECIPES/ANALYSIS) ARE NOW REAL SHORTCUTS**

Each item in the Foods, Recipes, and Analysis dropdowns is labeled with a number ("1. Search", "2. Analyze a food portion", ...). Once the menu is open, pressing that plain number key (no Alt/Shift needed) now jumps straight to that item — matching what the numbering already implied. Previously an unhandled digit keypress fell straight through to the browser instead, and in Firefox this could pop up its own "find in page" bar with the digit typed into it, since Firefox treats any unhandled plain character key as the start of a find-as-you-type search. See [Keyboard Shortcuts](#web-shortcuts) in Settings.

<!--
```
Scope: web/templates/base.html — added a second keydown listener alongside
the existing Alt+Shift one: when a plain digit 1-9 is pressed with no
Ctrl/Alt/Meta held and a `.numa-dropdown.show` menu is currently open,
preventDefault() and click() the nth `.dropdown-item` (1-indexed, skipping
the `<hr class="dropdown-divider">` list item so item numbers line up with
the visible "1./2./3." labels). Works whether the menu was opened by mouse
or by the Alt+Shift shortcut. web/templates/settings.html — added a line to
the Keyboard Shortcuts section documenting this. Verified with Playwright:
mouse-opened menu + digit selects the right item, Alt+Shift+F + digit does
too, and a bare digit with no menu open does nothing (doesn't interfere
with normal typing). Full test suite: 1008 passed.
```
-->

**"DID YOU MEAN" SUGGESTIONS NOW APPEAR ON EVERY SEARCH BOX THAT WAS MISSING THEM**

Misspell a search on Food Cache, Annotate a Food, Recipes, Meal History Search, or either of the two food-lookup searches on the Edit Custom Profile page (Copy nutrient values, Estimate amino acids), and you'll now see "Did you mean: ..." suggestions the same way Search, Pantry, Compare, and the other search boxes already did — those six had a "no results" message but were never wired up to actually offer a correction.

<!--
```
Scope: web/templates/food_cache.html, food_annotate.html, meals_search.html,
recipes.html, food_custom_profiles.html, food_custom_edit.html (two search
boxes) — each of these had a no-results branch with no
<span class="search-no-results" data-query data-field> marker element, so
base.html's shared numaInitSearchSuggestions()/`/search/suggestions` (backed
by numa_app/services/search_suggest.py, unchanged) never fired for them.
Added the marker span to each, matching the pattern already used in
search.html, pantry.html, compare.html, recipe_edit.html, meal.html,
food_convert.html, and food_analyze_portion.html. web/templates/
oxalate_link.html's search deliberately excluded — it already always
returns difflib-ranked candidates via oxalate.py's own search_similar()
against a different corpus (the oxalate reference table), so it has no true
zero-result state and wiring the generic suggester in would surface
irrelevant cross-corpus suggestions. No backend/route changes; verified via
FastAPI TestClient against an isolated DB plus the full tests/test_web.py
suite (187 passed).
```
-->

**THE "CHOOSE FIELDS TO COPY" PAGE CAN NOW SELECT OR DESELECT A WHOLE NUTRIENT GROUP AT ONCE**

On [Edit Custom Profile](#drafted-foods)'s "Choose fields to copy" page (see "Edit Custom Profile can now copy just the fields you choose" below), each nutrient group — Macronutrients, Minerals, Vitamins, Amino Acids, and so on — now has its own checkbox in the card header, next to the group's name. Checking or unchecking it selects or deselects every field in that group in one click, instead of clicking each field individually; it also reflects a partially-selected group (a dash rather than a check) if you've hand-picked only some of that group's fields.

<!--
```
Scope: web/templates/food_custom_copy_select.html — each field-group <div
data-field-group> card gets a checkbox (data-group-select-all) in its
card-title. JS: a change listener on that checkbox toggles every
.copy-field-checkbox within the same card; a change listener on each field
checkbox calls syncGroupCheckbox() to keep the group checkbox's checked/
indeterminate state in sync (indeterminate when some-but-not-all of that
group's fields are checked). The page-wide "Select all"/"Select none"
buttons now also resync every group checkbox afterward. tests/test_web.py:
test_custom_profile_copy_nutrients_select_page_lists_source_fields extended
to assert the per-group checkbox markup is present.
```
-->

**A USER-DRAFTED FOOD'S ID NO LONGER SHOWS AS THE NONSENSE LABEL "OFF"**

Several ID columns across the app (Food Cache, Pantry, Compare, Prune, and every food/recipe search-results table) labeled *any* negative food id as "OFF" (Open Food Facts) — including small, ordinary user-drafted food ids that aren't from Open Food Facts at all. A [drafted food](#drafted-foods) now gets its own readable id instead: **UD1**, **UD2**, **UD3**, and so on, assigned in the order each draft was created. Real Open Food Facts, Canadian Nutrient File, CoFID, AFCD, and CIQUAL ids are unaffected — those already had correct, distinct labels; only the fallback that swallowed everything else into "OFF" was wrong.

<!--
```
Scope: numa_app/services/food_ids.py classify_food_id() — the final fallback
branch (fdc_id doesn't match any _SYNTHETIC_ID_RANGES block, i.e. a genuine
user-drafted id from db.next_user_drafted_fdc_id()'s -1, -2, -3, ...
allocation) now returns id_str f"UD{-fdc_id}" instead of the bare negative
number. web/backend.py — new food_id_short() Jinja global (id_str half of
classify_food_id(), for a compact standalone ID column where food_id_tag()'s
full "(#id, SOURCE)" form would duplicate an adjacent Type/Source column).
Replaced six separate ad hoc "fdc_id < 0 ? OFF : fdc_id" template
expressions — the actual bug, present since before the multi-source
(CNF/CoFID/AFCD/CIQUAL) expansion — with food_id_short() calls in
food_cache.html, food_cache_prune.html, compare.html, pantry.html,
_add_food_row.html, recipe_edit.html, and _search_result_row.html. New
tests/test_food_ids.py (6 cases) plus one new web-level regression test in
tests/test_web.py asserting the Food Cache ID column renders "UD3" and
never renders ">OFF<" for a drafted food.
```
-->

**EDIT CUSTOM PROFILE CAN NOW COPY JUST THE FIELDS YOU CHOOSE FROM ANOTHER FOOD, AND SHOWS AMINO ACID STATUS IN ITS SEARCH RESULTS**

"Copy nutrient values from another food" (renamed from "Copy a full nutrient profile") used to be all-or-nothing — picking a source food replaced every value on the profile at once, amino acids included, even if you only wanted to fill in a couple of missing minerals. Clicking a search result now opens a **Choose fields to copy** page listing every nutrient the source food actually has, grouped the same way the edit form is, each with a checkbox (all checked by default) and a side-by-side look at what's on this profile now versus what the source would bring in. Only the fields you leave checked are changed — everything else on the profile stays exactly as it was. Separately, that search results table now shows an AA column, same as the amino-acid estimator's search results below it, so you can see at a glance which candidates actually have amino acid data before picking one.

<!--
```
Scope: web/backend.py — new GET /food/custom-profiles/{fdc_id}/copy-nutrients/select
(renders food_custom_copy_select.html: per-group checkbox list built from
_EDIT_NUTRIENT_GROUPS, restricted to keys the source actually has, each row
showing target_value vs source_value). POST /copy-nutrients now takes
keys: list[str] = Form(default=[]) and merges only those keys into the
target's existing nutrients dict (dict(target_nutrients); updated[k] =
source[k] for k in selected) instead of replacing the whole dict — a food
with no keys selected redirects with nutrients_applied=none_selected
rather than silently doing nothing. New _get_or_cache_source_food() helper
extracted from the (now three) copy-aa/copy-nutrients/-select routes'
duplicated "fetch-and-cache an uncached source" block.
numa_app/services/aa_estimate.py copy_nutrients_note() takes an optional
field_labels list, naming up to 6 fields or falling back to a count, so
the saved Notes text reflects a partial copy instead of always implying a
full-profile one. web/templates/food_custom_edit.html — nutrient_source_results
table gets an AA column (mirroring aa_source_results below it); the
"Use as source" button/confirm() replaced with a plain link to the new
select page. New file: food_custom_copy_select.html. Tests: 3 new in
tests/test_web.py (select page renders source fields, selective copy
merges instead of replacing, no-selection case), 2 existing tests
(test_food_cascade.py, test_web.py) updated to pass explicit keys=... now
that a bare POST is a no-op by design.
```
-->

**THE MISLEADING AMINO-ACID CHECKMARK FIX NOW COVERS EVERY PAGE THAT SHOWS ONE, NOT JUST FOOD SEARCH**

Yesterday's fix for the false "amino acid data confirmed" checkmark (a food with no nutrient data at all showing ✓ instead of a warning) only touched Food Search — Food Cache, Pantry, Compare, the meal "Refresh AA data" action, and both AA-source pickers on the Edit Custom Profile page still had the same bug, using the same unguarded check. All of them now use the same fixed logic. Two consequences beyond the visual checkmark: a food this broken could never be picked up by "Refresh AA data" (it looked done already, so it was silently skipped forever), and a recipe containing it could silently skip the usual complement-table AA fallback for the same reason — both now correctly treat it as needing attention.

Separately, on [Edit Custom Profile](#drafted-foods), the "Copy a full nutrient profile" and "Estimate amino acids" sections have been relabeled so it's clear at a glance (and again in the confirmation prompt when you click) that the first replaces everything on the profile, amino acids included, while the second only ever touches amino acids and leaves the rest of the profile alone.

<!--
```
Scope: usda_nutrients.py — new has_confirmed_aa_data() (has_macro_data()
AND has_amino_acid_data()), the boolean counterpart to aa_indicator() for
call sites that need a plain True/False rather than a ✓/✗/⚠ display
string. Re-exported via usda.py. web/backend.py — food_cache_get(),
food_cache_refresh()'s error-path re-render, pantry_get(),
_search_food_sources() (the AA-source picker's has_aa/button-disable
flag), meal_refresh_aa()'s "already has AA data, skip" gate, and the
Compare page's has_aa flag all switched from has_amino_acid_data() to
has_confirmed_aa_data(). numa_app/services/recipe_nutrients.py
best_aa_nutrients() — same swap, fixing the recipe-level complement
fallback. web/templates/food_custom_edit.html — both <details> summaries,
their descriptions, the "Use as source"/confirm() text, and the AA-picker
button text reworded to name what each action does and does not touch.
```
-->

**THE MANUAL NOW OPENS IN ITS OWN TAB AND PICKS UP WHERE YOU LEFT OFF**

Clicking **Manual** in the main navigation now always opens it in a new browser tab, so you don't lose your place in the app. It also remembers the last section you were reading and scrolls straight back there on your next visit — unless you followed a specific "Learn more" link, which always takes you to that link's own section instead. And the Table of Contents search box is now focused automatically when the page loads, so you can just start typing.

<!--
```
Scope: web/templates/base.html — Manual nav link gets target="_blank"
rel="noopener". scripts/build_manual.py — search-input autofocus()'d on
load (skipped below 1050px, where CSS hides the TOC sidebar, to avoid
popping the mobile keyboard unasked). New localStorage key
numa_manual_last_section, set in the scroll-spy's activate() and read on
load: with no location.hash (a plain nav click) it scrolls to the saved
section; an explicit hash (a deep "Learn more" link) always wins instead.
localStorage rather than sessionStorage since target="_blank" opens a
fresh tab with its own session storage each time.
```
-->

---

## Notes

[^1]: Lippman, D., Stump, M., Veazey, E., Guimarães, S. T., Rosenfeld, R., Kelly, J. H., Ornish, D., & Katz, D. L. (2024). Foundations of Lifestyle Medicine and its Evolution. *Mayo Clinic Proceedings: Innovations, Quality & Outcomes, 8(1)*, 97–111. https://doi.org/10.1016/j.mayocpiqo.2023.11.004

[^2]: U.S. Department of Agriculture, Agricultural Research Service. (2019). *FoodData Central*. https://fdc.nal.usda.gov/

[^3]: Open Food Facts contributors. (2012). *Open Food Facts*. https://world.openfoodfacts.org/

[^4]: Institute of Medicine (US) Panel on Micronutrients. (2001). *Dietary Reference Intakes for Vitamin A, Vitamin K, Arsenic, Boron, Chromium, Copper, Iodine, Iron, Manganese, Molybdenum, Nickel, Silicon, Vanadium, and Zinc*. National Academies Press. https://doi.org/10.17226/10026 — the underlying Dietary Reference Intake report establishing that non-heme iron and phytate-inhibited zinc from plant foods are absorbed less efficiently than from mixed/omnivorous diets; the basis for the NIH fact-sheet figures below.

[^5]: National Institutes of Health, Office of Dietary Supplements. *Iron: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/ — states that because vegetarian diets contain no heme iron and their non-heme iron is less bioavailable, "the RDA for vegetarians is 1.8 times higher than for people who eat meat."

[^6]: National Institutes of Health, Office of Dietary Supplements. *Zinc: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/ — states that "the zinc requirements for vegetarians may be as much as 50% higher than for those who eat meat" because of the reduced bioavailability of zinc from plant-based diets.

[^7]: National Institutes of Health, Office of Dietary Supplements. *Vitamin B12: Fact Sheet for Health Professionals*. https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/ — vitamin B12 occurs naturally only in animal foods. See also Melina, V., Craig, W., & Levin, S. (2016). Position of the Academy of Nutrition and Dietetics: Vegetarian Diets. *Journal of the Academy of Nutrition and Dietetics, 116*(12), 1970–1980. https://doi.org/10.1016/j.jand.2016.09.025 — recommends that vegans obtain vitamin B12 routinely from fortified foods or a supplement, since no reliable unfortified plant source exists. Neither source specifies a "50% of RDA" cutoff for a single day's intake; that trigger is NuMa's own design choice (see main text).

[^8]: Atkinson, Brand-Miller, Foster-Powell, Buyken & Goletzke, "International tables of glycemic index and glycemic load values 2021: a systematic review," *The American Journal of Clinical Nutrition* 114(5):1625–1632 (doi:10.1093/ajcn/nqab233). The newer of the two editions involved. NuMa does not ship it — its licence forbids that — but it can read it into your own copy in a few minutes; see [Upgrading to the 2021 tables](#gi-editions). The published table is actually two online supplemental tables, and the thing to understand about them is that they are split by **how well the study was run, not by who it was run on**: **Supplemental Table 1** holds values from studies whose method was consistent with ISO 26642:2010 (food numbers 1–2091), and **Supplemental Table 2** holds values from studies that deviated from that standard — fewer than ten subjects, an unusual carbohydrate portion, an unrepeated reference food — or whose results varied widely (2092–4018). Most of Table 2 was still measured in normal-glucose-tolerance subjects, so NuMa takes each row's subject group from that row's own "Subjects (type & number)" column and carries ISO compliance as a separate flag; see [Method quality](#gi-method-quality). This is a change from the 2008 edition, whose two appendix tables genuinely were split by population. Values are taken from the glucose-referenced GI column (GI, Glucose=100), matching the scale NuMa uses everywhere else. Glycemic load is not imported from the table at all: the published GL is a *nominal* figure computed from a standardized carbohydrate portion for the whole food category, and the source itself calls it "intended as a guide only", so NuMa computes GL live from a food's own cached carbohydrate content and the amount consumed instead (see [Glycemic Load](#gl)). Each row also publishes its **year of test** and country of food production, which NuMa shows in the lookup — see [How to read a lookup result](#gi-result-row). Licensing: published under the Elsevier user licence, which expressly permits "access, download, copy, translate, text and data mine" for non-commercial purposes but forbids redistribution, reposting and adaptation. That is precisely why NuMa ships the parser and the Creative Commons 2008 edition[^8a] rather than this table: extracting the data for your own use is something the licence allows *you* to do, and the resulting file stays on your machine. Copyright is held by the American Society for Nutrition; permission to distribute would have to come from them via the publisher. (For technically skilled users: table ingestion is `scripts/build_gi_data.py`, producing the local-only `gi_data_local.json`, which `gi_lookup.py` prefers over the bundled `gi_data.json` whenever it exists; lookup/matching logic is `gi_lookup.py`. The 2008 ingest script is kept as `scripts/build_gi_data_2008.py` but is not part of a normal build. A separate, older helper, `import_gi_seed.py`, bulk-applies exact name matches from a small 62-item starter set for automation/demo-data purposes.) Every entry cites its source study by number, listed in the supplemental tables' own footnotes and reference list; a code beginning **UO** means "unpublished observations", for which there is no paper to trace.

[^8a]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2008," *Diabetes Care* 31(12):2281–3. **The edition built into NuMa**, and the one every install has. A Creative Commons–licensed table, which is exactly why it can ship with the program at all. If you add the 2021 edition[^8] yourself, NuMa keeps the few hundred of this edition's foods that 2021 does not appear to cover, labelled **2008 edition** in lookup results — see [Upgrading to the 2021 tables](#gi-editions). Those rows have no year of test, no standard error and no country, because this edition did not publish them in a form NuMa captured; "2008" on such a row is the edition it came from, never the year the food was tested.

[^8b]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2002," *The American Journal of Clinical Nutrition* 76(1):5–56. Deliberately **not** used. It is the direct predecessor of the 2008 table above, which revised and absorbed it, so adding it would mainly contribute duplicate food names carrying older values for the same studies — actively worse than not having them, since the lookup shows you every plausible match to choose between. Listed here only to record that it was considered and why it was rejected.

[^9]: US National Institutes of Health. (2026, July 31). Office of Dietary Supplements—Nutrient Recommendations and Databases. https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

[^10]: NuMa's own curated table of amino-acid profiles for common protein-complement foods — beans, grains, seeds, and a few animal foods included for comparison (`_COMPLEMENT_TABLE` in `usda_nutrients.py`). 23 of the 25 entries cite a specific [USDA](#gloss-usda) FoodData Central SR Legacy record by FDC ID, sourced the same way as the rest of NuMa's nutrient data[^2]; the remaining two (nutritional yeast, pea protein powder) use published amino-acid-composition literature values because no matching USDA record exists for those specific products. NuMa always checks your own food cache for a real match to each entry's food name before falling back to these built-in figures — see [amino acid estimates in complement suggestions](#comp-estimate).

[^11]: Harvard T.H. Chan School of Public Health, Renal and Urology News Oxalate Table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine. https://hsph.harvard.edu/wp-content/uploads/2024/07/OXALATE-TABLE-1.xlsx — NuMa matches foods to this table by name; see [Oxalate data](#oxalate) for enabling it, matching, and limitations.

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


---

## Disclaimer {: #disclaimer}

NuMa is a personal food-record and nutrient-calculation tool, not a source of medical or dietary advice, and it makes no claim about health or illness. Its figures are informed estimates pooled from third-party food [databases](#gloss-database) and checked routinely for internal correctness — they are not a substitute for a physician, registered dietitian, or product label. See the full [Disclaimer](/disclaimer) for details on data accuracy, review practices, and your own responsibility when using this program.

